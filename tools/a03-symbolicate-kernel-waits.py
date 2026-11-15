#!/usr/bin/env python3
"""Resolve bounded A03 WAIT kernel traces using the exact unslid kernel.

The A03 flat loader boots the statically rebased kernel without KASLR.
Use only its matching kernel artifact; the log alone cannot verify identity.
"""
import argparse
import bisect
from pathlib import Path
import re
import subprocess


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('kernel', type=Path)
    ap.add_argument('log', type=Path)
    a = ap.parse_args()
    output = subprocess.check_output(['llvm-nm', '-n', '--defined-only', str(a.kernel)], text=True)
    symbols = []
    for line in output.splitlines():
        match = re.fullmatch(r'([0-9a-fA-F]+) [tTsS] (.+)', line)
        if match:
            symbols.append((int(match[1], 16), match[2]))
    symbols.sort()
    addresses = [x[0] for x in symbols]
    for line in a.log.read_text(errors='replace').splitlines():
        if 'A03 WAIT ' not in line:
            continue
        print(line)
        match = re.search(r'continuation ([0-9a-f]+) kbt(.*)', line)
        if not match:
            continue
        tokens=[]
        for token in match[2].split():
            if not re.fullmatch(r'[0-9a-f]{16}',token):
                break
            tokens.append(token)
        for token in [match[1]] + tokens:
            address = int(token, 16)
            i = bisect.bisect_right(addresses, address) - 1
            if i >= 0 and address - symbols[i][0] < 0x10000:
                print(f'  {address:x} {symbols[i][1]}+0x{address-symbols[i][0]:x}')
            else:
                print(f'  {address:x} unresolved')


if __name__ == '__main__':
    main()
