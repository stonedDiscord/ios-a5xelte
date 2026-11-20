#!/usr/bin/env python3
"""Retrieve the retained DREAMLTE startup console over read-only USB EP0."""
import argparse
from pathlib import Path
import struct
import sys

import usb.core


def read_console(dev):
    header = bytes(dev.ctrl_transfer(0xc0, 0x52, 0, 0x8895, 8, timeout=2000))
    if len(header) != 8 or header[:4] != b'DLOG':
        raise RuntimeError(f'unsupported console response: {header!r}')
    size, = struct.unpack('<I', header[4:])
    if size > 0x200000:
        raise RuntimeError(f'invalid console size: {size}')
    result = bytearray()
    while len(result) < size:
        offset = len(result)
        length = min(512, size - offset)
        chunk = bytes(dev.ctrl_transfer(0xc0, 0x53, offset & 0xffff,
                                       offset >> 16, length, timeout=2000))
        if len(chunk) != length:
            raise RuntimeError(f'short console read at {offset}: {len(chunk)}/{length}')
        result.extend(chunk)
    return bytes(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='private log path (must not exist)')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output already exists')
    devices = list(usb.core.find(find_all=True, idVendor=0x1209, idProduct=0x0001))
    if len(devices) != 1:
        raise RuntimeError(f'expected exactly one XNU gadget, found {len(devices)}')
    result = read_console(devices[0])
    with args.output.open('xb') as output:
        output.write(result)
    print(f'Saved {len(result)} retained console bytes to {args.output}')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, usb.core.USBError, OSError) as error:
        sys.exit(str(error))
