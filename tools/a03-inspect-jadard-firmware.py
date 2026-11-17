#!/usr/bin/env python3
"""Inspect a private JD9365T RAM image; never access a device or load firmware.

Matches the Samsung HostWritePram move-table and software CRC implementation.
A valid image does not establish compatibility with the connected panel.
"""
import argparse
import hashlib
import json
from pathlib import Path


def crc16(data):
    value = 0xffff
    for byte in data:
        value ^= byte << 8
        for _ in range(8):
            value = ((value << 1) ^ (0x8005 if value & 0x8000 else 0)) & 0xffff
    return value


def inspect(data):
    if len(data) < 5 or data[3] == 0xff or data[3] < 14:
        raise ValueError('missing or invalid move table')
    count = (data[3] - 2) // 12  # exact stock GetMoveInfoNumber rule
    end = 5 + count * 12
    if end > 256 or end > len(data):
        raise ValueError('truncated move table')
    moves = []
    for index in range(count):
        entry = data[5 + index * 12:17 + index * 12]
        offset = int.from_bytes(entry[1:4], 'big')
        size = int.from_bytes(entry[4:6], 'big') + 1
        target = int.from_bytes(entry[6:10], 'big')
        expected = int.from_bytes(entry[10:12], 'big')
        if offset < end or offset + size > len(data):
            raise ValueError(f'move {index}: source outside payload')
        if target + size > 0x100000000:
            raise ValueError(f'move {index}: target wraps')
        actual = crc16(data[offset:offset + size])
        if actual != expected:
            raise ValueError(f'move {index}: CRC mismatch {actual:04x}/{expected:04x}')
        moves.append(dict(command=entry[0], offset=offset, size=size,
                          target=target, crc16=f'{expected:04x}'))
    return dict(size=len(data), sha256=hashlib.sha256(data).hexdigest(),
                moves=moves, compatibility='unverified; offline validation only')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('firmware', type=Path)
    args = parser.parse_args()
    try:
        result = inspect(args.firmware.read_bytes())
    except ValueError as error:
        parser.exit(1, str(error) + chr(10))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
