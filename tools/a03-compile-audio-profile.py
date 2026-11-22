#!/usr/bin/env python3
"""Compile private SC2730 DSP tuning XML into the stock audio_profile layout."""
import argparse
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as ET


def number(node, attribute):
    return int(node.attrib[attribute], 0)


def register_value(node, width):
    fields = list(node) or [node]
    occupied = 0
    value = 0
    for field in fields:
        offset = number(field, 'offset')
        bits = number(field, 'bits')
        field_value = number(field, 'val')
        if offset < 0 or bits <= 0 or offset + bits > width:
            raise ValueError(f'{field.tag}: field exceeds {width}-bit register')
        mask = (1 << bits) - 1
        # Some 16-bit coefficients are written as sign-extended u32 literals.
        if bits == width == 16 and 0xffff8000 <= field_value <= 0xffffffff:
            field_value &= mask
        if not 0 <= field_value <= mask or occupied & (mask << offset):
            raise ValueError(f'{field.tag}: out-of-range or overlapping field')
        occupied |= mask << offset
        value |= field_value << offset
    return value


def compile_profile(root):
    if root.tag not in ('dsp_vbc', 'dsp_smartamp', 'cvs', 'audio_structure'):
        raise ValueError(f'unsupported profile {root.tag}')
    count = number(root, 'num_mode')
    stride = number(root, 'struct_size')
    if not (0 < count <= 256 and 0 < stride <= 65536):
        raise ValueError('invalid profile dimensions')

    modes = {}
    for node in root.iter():
        if 'mode' not in node.attrib:
            continue
        index = number(node, 'mode')
        if not 0 <= index < count or index in modes:
            raise ValueError(f'invalid or duplicate mode {index}')
        data = bytearray()
        base = index * stride
        for register in node.iter():
            if 'id' not in register.attrib:
                continue
            match = re.fullmatch(r'u([1-9][0-9]*)', register.attrib['t'])
            if not match:
                raise ValueError(f'{register.tag}: unsupported register type')
            width = int(match[1])
            offset = number(register, 'id') - base
            if width % 8 or offset != len(data) or offset + width // 8 > stride:
                raise ValueError(f'mode {index} {register.tag}: invalid register layout')
            data.extend(register_value(register, width).to_bytes(width // 8, 'little'))
        if len(data) != stride:
            raise ValueError(f'mode {index}: expected {stride} bytes, got {len(data)}')
        modes[index] = data

    if len(modes) != count:
        raise ValueError(f'expected {count} modes, got {len(modes)}')
    return struct.pack('<16sII', b'audio_profile', count, stride) + b''.join(
        modes[index] for index in range(count)
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xml', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        data = compile_profile(ET.parse(args.xml).getroot())
    except (ValueError, KeyError, ET.ParseError) as error:
        parser.error(str(error))
    with args.output.open('xb') as stream:
        stream.write(data)


if __name__ == '__main__':
    main()
