#!/usr/bin/env python3
"""Read-only regression checks for the matching iOS16 data-vault ABI.

This checks instructions and metadata names, not Apple Sandbox semantics or
successful runtime conversion. No files inside the root image are modified.
"""
import argparse
import importlib.util
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path, help='matching rebuilt HFS iOS16 root')
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location(
        'symbols', Path(__file__).with_name('a03-symbolicate-cache.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    access = module.cache.Image(args.image)
    symbols = module.Symbols(access)
    checks = {
        # rootless_mkdir_datavault passes UF_DATAVAULT to mkdir_protected.
        0x1cdc4ec64: '03108052',
        # convert_to_datavault selects Sandbox operation 0x104.
        0x1cdc4ecc8: '81208052',
        # check_datavault_flag selects bit 0x80.
        0x1cdc4d2e4: '02108052',
        # check_protected_flag loads the com.apple.rootless xattr name.
        0x1cdc4d5d4: '010000d021c83591',
        # Successful conversion's recursive walk ORs bit 0x80 before chflags.
        0x1cdc4edd0: '01011932',
    }
    for address, expected in checks.items():
        actual = symbols.read(address, len(expected) // 2).hex()
        if actual != expected:
            raise SystemExit(f'ABI mismatch at {address:#x}: {actual} != {expected}')
    expected = b'com.apple.rootless\0'
    if symbols.read(0x1cdc4fd72, len(expected)) != expected:
        raise SystemExit('data-vault owner xattr name mismatch')
    print('PASS matching iOS16 ABI: Sandbox 0x104, UF_DATAVAULT 0x80, '
          'com.apple.rootless owner xattr, recursive flag propagation')
    print('This is static evidence; it does not establish runtime conversion '
          'or data-vault access enforcement.')


if __name__ == '__main__':
    main()
