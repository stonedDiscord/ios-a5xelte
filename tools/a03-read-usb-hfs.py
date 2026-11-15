#!/usr/bin/env python3
"""Read files from the A03 read-only USERDATA USB LUN (or an offline HFS image).

Never mounts or writes the source. Reuses the filesystem-only HFS parser;
no donor device path or ADB command is used. Private recovered files stay local.
"""
import argparse
import importlib.util
import os
from pathlib import Path
import stat
import struct

PART_BYTES = 54381228032
SERIAL = 'A03LinuxReaderV11'
DEFAULT = '/dev/disk/by-id/usb-Linux_File-Stor_Gadget_' + SERIAL + '-0:1'


def validate(path):
    path = path.resolve(strict=True)
    st = path.stat()
    if stat.S_ISREG(st.st_mode):
        return path, st
    if not stat.S_ISBLK(st.st_mode):
        raise ValueError('source must be an offline image or validated USB LUN')
    sys = (Path('/sys/dev/block') / f'{os.major(st.st_rdev)}:{os.minor(st.st_rdev)}').resolve(strict=True)
    usb = next((p for p in sys.parents if (p / 'idVendor').exists()), None)
    if usb is None or (usb/'idVendor').read_text().strip() != '1d6b' or (usb/'idProduct').read_text().strip() != '0104' or (usb/'serial').read_text().strip() != SERIAL:
        raise ValueError('wrong USB identity')
    if not (sys/'device').resolve().name.endswith(':1') or (sys/'device/model').read_text().strip() != 'File-Stor Gadget':
        raise ValueError('expected USERDATA LUN1')
    if int((sys/'size').read_text()) * 512 != PART_BYTES or (sys/'ro').read_text().strip() != '1':
        raise ValueError('expected exact read-only USERDATA capacity')
    for line in Path('/proc/self/mountinfo').read_text().splitlines():
        if line.split()[2] == f'{os.major(st.st_rdev)}:{os.minor(st.st_rdev)}':
            raise ValueError('source must be unmounted')
    return path, st


class Source:
    def __init__(self, path):
        path, before = validate(path)
        self.fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC)
        after = os.fstat(self.fd)
        if (before.st_dev, before.st_ino, before.st_rdev) != (after.st_dev, after.st_ino, after.st_rdev):
            raise ValueError('source changed during open')
        self.length = PART_BYTES if stat.S_ISBLK(after.st_mode) else after.st_size

    def read(self, off, n):
        if off < 0 or n < 0 or off > self.length or n > self.length - off:
            raise ValueError('read outside source')
        data = os.pread(self.fd, n, off)
        if len(data) != n:
            raise ValueError('short source read')
        return data


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, default=Path(DEFAULT))
    ap.add_argument('command', choices=['ls', 'stat', 'get'])
    ap.add_argument('path')
    ap.add_argument('output', nargs='?', type=Path)
    a = ap.parse_args()
    if a.command == 'get' and a.output is None:
        ap.error('get requires output')
    spec = importlib.util.spec_from_file_location('hfs', Path(__file__).with_name('herolte-hfs-read.py'))
    hfs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hfs)
    source = Source(a.source)
    fs = hfs.HFS(source)
    cat = hfs.Catalog(fs)
    fid, record = cat.lookup(a.path)
    if a.command == 'ls':
        for name, rec in cat.children(fid):
            typ = hfs.be('h', rec)[0]
            print(('d' if typ == 1 else 'f'), hfs.file_info(rec)[2][0] if typ == 2 else '-', name)
        return
    if record is None or hfs.be('h', record)[0] != 2:
        raise ValueError('expected file')
    fid, mode, fork = hfs.file_info(record)
    exts = fs.all_extents(fork[1], fid, 0)
    size = fork[0]
    if sum(count for _, count in exts) * fs.bs < size:
        raise ValueError('incomplete file extents')
    print('file', fid, oct(mode), size, 'bytes', len(exts), 'extents', flush=True)
    if a.command == 'stat':
        return
    with a.output.open('xb') as out:
        left = size
        for start, count in exts:
            take = min(left, count * fs.bs)
            pos = start * fs.bs
            while take:
                n = min(take, 4 << 20)
                out.write(source.read(pos, n))
                pos += n
                take -= n
                left -= n
            if not left:
                break
    if left:
        raise ValueError('incomplete extraction')
    print('extracted', size, 'bytes to', a.output)


if __name__ == '__main__':
    main()
