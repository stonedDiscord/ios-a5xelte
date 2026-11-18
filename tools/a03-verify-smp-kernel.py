#!/usr/bin/env python3
"""Reject a green A03 build whose opt-in SMP patch was skipped."""
import argparse
from pathlib import Path

MARKERS = (
    b'A03 CPU: requested=%u selected=%u (limit=%u)',
    b'A03 CPU: cpu=%u CPU_ON target=0x%x entry_pa=0x%llx context=%u',
    b'A03 CPU: cpu=%u PSCI CPU_ON rc=%d',
    b'A03 CPU: %u/%u CPUs initialized, SGI1 verified',
)


def verify(kernel):
    missing = [marker.decode() for marker in MARKERS if marker not in kernel]
    if missing:
        raise ValueError('A03 SMP code missing from linked kernel: ' + '; '.join(missing))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kernel', type=Path)
    args = parser.parse_args()
    try:
        verify(args.kernel.read_bytes())
    except ValueError as error:
        parser.exit(1, str(error) + chr(10))
    print('PASS linked A03 SMP CPU registration/startup/PSCI/completion markers')


if __name__ == '__main__':
    main()
