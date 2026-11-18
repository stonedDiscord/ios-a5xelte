#!/usr/bin/env python3
"""Host-only A03 XNU wrapper packer; BOOT-only, exact Magisk base required."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import importlib.util
import adt
from a03_memory import PHYS_BASE, MEMORY_MIB, memory_size, validate_live_fdt

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('probe', ROOT/'tools/a03-probe-image.py')
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('base', type=Path)
    ap.add_argument('payload', type=Path)
    ap.add_argument('output', type=Path)
    ap.add_argument('--smp-kernel', type=Path, help='exact kernel Mach-O used in payload; install loader SMP handoff')
    ap.add_argument('--memory-dtb', type=Path, help='live A03 DTB, required for expanded RAM')
    a = ap.parse_args()
    b = a.base.read_bytes()
    assert hashlib.sha256(b).hexdigest() == probe.BASE_SHA256, 'wrong base BOOT'
    assert not a.output.exists(), 'refusing existing output'
    subprocess.run(['sh', str(ROOT/'shim/a03/build-xnu.sh')], check=True)
    loader = (ROOT/'shim/a03/out/a03-xnu-loader.Image').read_bytes()
    payload = a.payload.read_bytes()
    assert payload[:8] == b'SWEETXNU'
    version, count = struct.unpack_from('<II', payload, 8)
    base, entry, ao, al, end, phys, mem = struct.unpack_from('<7Q', payload, 16)
    assert version == 1 and 0 < count <= 32
    assert phys == PHYS_BASE and mem in tuple(memory_size(m) for m in MEMORY_MIB)
    if mem != memory_size(256) and a.memory_dtb is None:
        ap.error('expanded RAM requires --memory-dtb live A03 DTB')
    if a.memory_dtb:
        print('Live RAM validation', validate_live_fdt(a.memory_dtb, mem))
    assert base <= entry < end and end-base < mem
    assert ao <= len(payload) and al <= len(payload)-ao and al <= 0x100000
    assert (end-base+al+16383)//16384*16384+16384 <= mem
    tree, parsed = adt.parse(payload[ao:ao+al])
    assert parsed == al
    chosen = next(n for n in tree.children if n.name == 'chosen')
    assert chosen.prop('dram-base') == struct.pack('<Q', phys)
    assert chosen.prop('dram-size') == struct.pack('<Q', mem)
    if a.smp_kernel:
        from mkpayload import build
        # Rebuilding with the exact ADT/cmdline proves kernel symbol provenance.
        command=payload[0x48:0x2a8].split(bytes(1))[0].decode('ascii')
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            original=Path(tmp)/'original.adt';original.write_bytes(payload[ao:ao+al])
            rebuilt,_=build(str(a.smp_kernel),str(original),command)
        assert rebuilt==payload, 'SMP kernel does not match payload'
        symbols=subprocess.check_output(['llvm-nm',str(a.smp_kernel)],text=True)
        matches=[int(line.split()[0],16) for line in symbols.splitlines() if line.endswith(' _sweet_secondary_entry')]
        assert len(matches)==1, 'missing unique SMP entry symbol'
        target=phys+matches[0]-base
        assert target>=phys and target<phys+mem and not target&3
        assert chosen.prop('a03-smp-trampoline') is None
        chosen.props.append(('a03-smp-trampoline',0,struct.pack('<QQ',0,target)))
        replacement=adt.serialize(tree)
        # mkpayload places ADT last; never overwrite a following object.
        assert len(payload)-ao-al<16 and not any(payload[ao+al:])
        payload=bytearray(payload[:ao])+replacement
        payload.extend(bytes((-len(payload))%16))
        al=len(replacement);struct.pack_into('<Q',payload,0x28,al)
        assert (end-base+al+16383)//16384*16384+16384<=mem
        print('SMP high entry',hex(target),'via loader-owned low BOOT trampoline')
    else:
        assert chosen.prop('a03-smp-trampoline') is None, 'SMP handoff must be generated from --smp-kernel'

    assert payload[0x48+607] == 0
    ranges = []
    entry_found = False
    for i in range(count):
        va, size, off, fs = struct.unpack_from('<4Q', payload, 0x2a8+i*32)
        assert base <= va and va-base+size <= end-base and fs <= size
        assert off <= len(payload) and fs <= len(payload)-off
        assert all(not size or not ts or va+size <= tv or tv+ts <= va for tv, ts in ranges)
        ranges.append((va, size))
        entry_found |= va <= entry < va+fs
    assert entry_found
    kernel = bytearray(loader+payload)
    struct.pack_into('<Q', kernel, 16, len(kernel))
    ks, _, rs, _, ss, _, _, page, version = struct.unpack_from('<9I', b, 8)
    assert b[:8] == b'ANDROID!' and version == 2 and page == 2048 and ss == 0
    rds, rdo = struct.unpack_from('<IQ', b, 1632)
    ds, = struct.unpack_from('<I', b, 1648)
    assert rds == rdo == 0
    align = lambda n: (n+page-1)//page*page
    ro = page+align(ks)
    ramdisk = b[ro:ro+rs]
    dt = b[ro+align(rs):ro+align(rs)+ds]
    out = bytearray(b[:page])
    struct.pack_into('<I', out, 8, len(kernel))
    digest = hashlib.sha1()
    for part in (kernel, ramdisk, b'', b'', dt):
        digest.update(part)
        digest.update(struct.pack('<I', len(part)))
    out[576:608] = digest.digest()+bytes(12)
    for part in (kernel, ramdisk, dt):
        out.extend(part)
        out.extend(bytes(align(len(part))-len(part)))
    out.extend(b'SEANDROIDENFORCE'+bytes(1))
    original_size = len(out)
    magic, major, minor, _, vo, vs = struct.unpack_from('>4sIIQQQ', b, len(b)-64)
    assert magic == b'AVBf' and vo+vs <= len(b)-64
    out.extend(bytes((-len(out)) % 4096))
    new_vo = len(out)
    out.extend(b[vo:vo+vs])
    assert len(out) <= len(b)-64, 'exceeds BOOT partition'
    out.extend(bytes(len(b)-64-len(out)))
    out.extend(struct.pack('>4sIIQQQ', magic, major, minor, original_size, new_vo, vs)+bytes(28))
    nr = page+align(len(kernel))
    assert out[nr:nr+rs] == ramdisk and out[nr+align(rs):nr+align(rs)+ds] == dt
    assert len(out) == len(b) == 67108864
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_bytes(out)
    print('SHA256', hashlib.sha256(out).hexdigest())
    print('XNU entry PA', hex(phys+entry-base), 'ADT PA', hex(phys+end-base))
    print('Host candidate only; stale AVB signature requires unlocked device.')


if __name__ == '__main__':
    main()
