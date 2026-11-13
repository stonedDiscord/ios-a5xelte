#!/usr/bin/env python3
"""Host regression check for the A03 MMU reporter on a private live FDT.

Stubs hardware test results; does not emulate EL1 or verify CPU translation.
Confirms reporting leaves every other byte of the live FDT unchanged.
"""
import argparse
import ctypes
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
SLOTS = (
    (b'androidboot.em.model=SM-A035G', b't', 0x16384),
    (b'androidboot.pcbainfo=EU_PCBA3_DCAM_MP', b'l', 4),
    (b'androidboot.carrierid.param.offset=9437644', b'q', 0x1409cb01c),
    (b'androidboot.sales.param.offset=9437648', b'u', 0x30d00801),
    (b'androidboot.sn.param.offset=9437392', b'a', 0x4400000081734b00),
    (b'androidboot.ddrsize.range=[4096,5120)', b'y', 0x5a000a03),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('fdt', type=Path)
    args = parser.parse_args()
    raw = args.fdt.read_bytes()
    if len(raw) < 40 or raw[:4] != bytes.fromhex('d00dfeed'):
        parser.error('expected a live FDT')
    total, = struct.unpack_from('>I', raw, 4)
    if total > len(raw):
        parser.error('truncated FDT')
    expected = bytearray(raw)
    for needle, key, value in SLOTS:
        if raw.count(needle) != 1:
            parser.error('expected one verified marker slot: ' + needle.decode())
        offset = raw.index(needle)
        marker = b'a03' + key + b'=' + format(value, '016x').encode()
        expected[offset:offset+len(needle)] = marker.ljust(len(needle), b' ')
    with tempfile.TemporaryDirectory(prefix='a03-report-test-') as tmp:
        t = Path(tmp)
        (t/'stub.c').write_text(
            'volatile unsigned long a03_mmu_result[12]; '
            'void a03_test_el1(void) {'
            'a03_mmu_result[0]=0x16384; a03_mmu_result[1]=4; '
            'a03_mmu_result[2]=0x1409cb01cUL; '
            'a03_mmu_result[3]=0x30d00801; '
            'a03_mmu_result[5]=0x4400000081734b00UL; '
            'a03_mmu_result[10]=0x5a000a03; }')
        subprocess.run(['clang','-shared','-fPIC','-DA03_MMU16K',
                        '-Wall','-Wextra','-Werror',
                        str(ROOT/'shim/a03/boot-probe.c'),str(t/'stub.c'),
                        '-o',str(t/'reporter.so')],check=True)
        lib = ctypes.CDLL(str(t/'reporter.so'))
        lib.a03_boot_probe.argtypes = [ctypes.c_void_p]
        buf = ctypes.create_string_buffer(raw)
        lib.a03_boot_probe(buf)
        assert buf.raw[:len(raw)] == expected, 'unexpected FDT mutation'
        # Malformed/truncated header inputs must not be modified.
        for invalid in (bytes(40), raw[:39], raw[:4]+bytes.fromhex('00200000')+raw[8:]):
            buf = ctypes.create_string_buffer(invalid)
            lib.a03_boot_probe(buf)
            assert buf.raw[:len(invalid)] == invalid
    print('PASS: only six approved slots changed; AVB and all other FDT bytes preserved')


if __name__ == '__main__':
    main()
