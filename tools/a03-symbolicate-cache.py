#!/usr/bin/env python3
"""Resolve plain-arm64 iOS16 cache PCs using its matching .symbols file.

Read-only HFS image/extracted-root access. Addresses default to unslid;
--slide subtracts a captured cache slide. Does not resolve standalone images.
Reports nearest preceding local and exported symbols, not proven containing
functions; exported symbols can occur between local symbols.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import struct

spec = importlib.util.spec_from_file_location('cache', Path(__file__).with_name('a03-verify-ios-cache.py'))
cache = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cache)


class Symbols:
    def __init__(self, access):
        self.access = access
        h = access.read(cache.CACHE, 0, 512)
        if h[:16].rstrip(b'\0 ') != b'dyld_v1   arm64':
            raise ValueError('requires matching plain-arm64 cache')
        self.base, = struct.unpack_from('<Q', h, 224)
        off, count = struct.unpack_from('<II', h, 392)
        names = [cache.CACHE]
        for i in range(count):
            uuid, _, suffix = struct.unpack('<16sQ32s', access.read(cache.CACHE, off + i * 56, 56))
            suffix = suffix.split(b'\0')[0].decode('ascii')
            if not suffix.startswith('.') or '/' in suffix or '..' in suffix:
                raise ValueError('unsafe subcache name')
            name = cache.CACHE + suffix
            if access.read(name, 88, 16) != uuid:
                raise ValueError('subcache UUID mismatch')
            names.append(name)
        self.maps = []
        for name in names:
            hh = access.read(name, 0, 32)
            off, count = struct.unpack_from('<II', hh, 16)
            for i in range(count):
                va, size, fileoff, _, _ = struct.unpack('<QQQII', access.read(name, off + i * 32, 32))
                self.maps.append((va, size, fileoff, name))
        self.images = []
        off, count = struct.unpack_from('<II', h, 448)
        for i in range(count):
            address, _, _, pathoff, _ = struct.unpack('<QQQII', access.read(cache.CACHE, off + i * 32, 32))
            path = access.read(cache.CACHE, pathoff, 4096).split(b'\0')[0].decode()
            self.images.append((address, path))
        self.images.sort()
        self.symbolfile = cache.CACHE + '.symbols'
        sh = access.read(self.symbolfile, 0, 512)
        if sh[88:104] != h[400:416]:
            raise ValueError('symbols UUID mismatch')
        self.localoff, localsize = struct.unpack_from('<QQ', sh, 72)
        no, nc, so, ss, eo, ec = struct.unpack('<6I', access.read(self.symbolfile, self.localoff, 24))
        if no + nc * 16 > localsize or so + ss > localsize or eo + ec * 16 > localsize:
            raise ValueError('local-symbol bounds invalid')
        self.nlistoff, self.stroff, self.strsize = no, so, ss
        self.entries = {}
        for i in range(ec):
            dyliboff, first, count = struct.unpack('<QII', access.read(self.symbolfile, self.localoff + eo + i * 16, 16))
            if first + count > nc:
                raise ValueError('symbol index outside table')
            self.entries[self.base + dyliboff] = (first, count)

    def read(self, va, size):
        for base, length, off, name in self.maps:
            if base <= va and va + size <= base + length:
                return self.access.read(name, off + va - base, size)
        raise ValueError('unmapped cache address ' + hex(va))

    def resolve(self, pc):
        # Confirm executable segment membership, not just the nearest header.
        for address, path in reversed(self.images):
            if address > pc:
                continue
            h = self.read(address, 32)
            magic, _, _, _, count, size, _, _ = struct.unpack('<8I', h)
            if magic != 0xfeedfacf or size > 1024 * 1024:
                continue
            commands = self.read(address + 32, size)
            offset = 0
            found = False
            linkedit = symtab = None
            for _ in range(count):
                cmd, length = struct.unpack_from('<II', commands, offset)
                if length < 8 or offset + length > len(commands):
                    raise ValueError('invalid Mach-O command bounds')
                if cmd == 0x19:
                    start, span = struct.unpack_from('<QQ', commands, offset + 24)
                    initprot, = struct.unpack_from('<I', commands, offset + 60)
                    found |= bool(initprot & 4 and start <= pc < start + span)
                    if commands[offset+8:offset+24].rstrip(bytes(1)) == b"__LINKEDIT":
                        linkedit = struct.unpack_from("<4Q", commands, offset+24)
                elif cmd == 2:
                    symtab = struct.unpack_from("<4I", commands, offset+8)
                offset += length
            if not found:
                continue
            result = {'pc': hex(pc), 'image': path, 'image_base': hex(address), 'image_offset': hex(pc-address)}
            first, count = self.entries.get(address, (0, 0))
            data = self.access.read(self.symbolfile, self.localoff + self.nlistoff + first * 16, count * 16)
            best = None
            for i in range(count):
                nameoff, kind, sect, desc, value = struct.unpack_from('<IBBHQ', data, i*16)
                if kind & 0xe0 or kind & 0x0e != 0x0e or not sect or not address <= value <= pc:
                    continue
                if best is None or value > best[0]:
                    best = value, nameoff
            if best is not None and best[1] < self.strsize:
                value, no = best
                name = self.access.read(self.symbolfile, self.localoff + self.stroff + no,
                                        min(2048, self.strsize-no)).split(b'\0')[0].decode(errors='replace')
                result.update(nearest_local_symbol=name, local_symbol_address=hex(value),
                              distance_from_local_symbol=hex(pc-value))
            # The cache Mach-O symbol table retains exports omitted by local symbols.
            if linkedit is not None and symtab is not None:
                linkva, linksize, fileoff, filesize = linkedit
                no, nc, so, ss = symtab
                if nc > 1000000 or filesize > linksize or no < fileoff or so < fileoff or no+nc*16 > fileoff+filesize or so+ss > fileoff+filesize:
                    raise ValueError("invalid image symbol-table bounds")
                symbols = self.read(linkva+no-fileoff, nc*16)
                best_export = None
                for nameoff, kind, sect, desc, value in struct.iter_unpack("<IBBHQ", symbols):
                    if kind & 0xe0 or kind & 0x0e != 0x0e or not kind & 1 or not sect or not address <= value <= pc or nameoff >= ss:
                        continue
                    if best_export is None or value > best_export[0]:
                        name = self.read(linkva+so-fileoff+nameoff, min(2048, ss-nameoff)).split(bytes(1))[0].decode(errors="replace")
                        if name and name != "<redacted>":best_export = value, name
                if best_export is not None:
                    value, name = best_export
                    result.update(nearest_exported_symbol=name, exported_symbol_address=hex(value), distance_from_exported_symbol=hex(pc-value))
            return result
        return {'pc': hex(pc), 'error': 'no executable cache image contains this address'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('root', type=Path)
    p.add_argument('addresses', nargs='+', type=lambda x: int(x, 0))
    p.add_argument('--hfs-image', action='store_true')
    p.add_argument('--slide', type=lambda x: int(x, 0), default=0)
    a = p.parse_args()
    symbols = Symbols(cache.Image(a.root) if a.hfs_image else cache.Directory(a.root))
    for address in a.addresses:
        if address < a.slide:
            p.error('address precedes slide')
        print(json.dumps(symbols.resolve(address-a.slide)))


if __name__ == '__main__':
    main()
