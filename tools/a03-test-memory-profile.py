#!/usr/bin/env python3
"""Host RAM guards: actual loader predicate plus synthetic/live DT reservations."""
from pathlib import Path
import argparse, ctypes, subprocess, tempfile
from a03_memory import PHYS_BASE, MEMORY_MIB, memory_size, validate_live_fdt
ROOT=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser();p.add_argument('--live-dtb',type=Path);a=p.parse_args()
with tempfile.TemporaryDirectory() as tmp:
    t=Path(tmp)
    (t/'guard.c').write_text('#include "memory-profile.h"\nint check(uint64_t b,uint64_t n){return a03_memory_profile_valid(b,n);}\n')
    subprocess.run(['clang','-Wall','-Wextra','-Werror','-shared','-fPIC','-I',str(ROOT/'shim/a03'),str(t/'guard.c'),'-o',str(t/'guard.so')],check=True)
    lib=ctypes.CDLL(str(t/'guard.so'));lib.check.argtypes=[ctypes.c_uint64,ctypes.c_uint64]
    for mib in MEMORY_MIB:assert lib.check(PHYS_BASE,memory_size(mib))==1
    for b,n in ((PHYS_BASE,0),(PHYS_BASE,512<<20),(PHYS_BASE,2<<30),(PHYS_BASE+4096,1<<30),(0,1<<30)):
        assert lib.check(b,n)==0
    def dt(reg='0 0x80000000 0 0xfffff000',reserve='1 0 0 0x1000',extra=''):
        source='/dts-v1/; '+extra+' / { compatible="sprd,ums9230"; #address-cells=<2>; #size-cells=<2>; memory@80000000 {device_type="memory"; reg=<'+reg+'>;}; reserved-memory {#address-cells=<2>; #size-cells=<2>; ranges; debug@100000000 {reg=<'+reserve+'>;};};};'
        (t/'test.dts').write_text(source)
        subprocess.run(['dtc','-q','-I','dts','-O','dtb','-o',str(t/'test.dtb'),str(t/'test.dts')],check=True)
        return t/'test.dtb'
    for mib in MEMORY_MIB:
        assert validate_live_fdt(dt(),memory_size(mib))['memory_mib']==mib
    # Check the final page, shorter banks and FDT header reservations.
    for f in (lambda:dt(reg='0 0x80000000 0 0xfdffffff'),
              lambda:dt(reserve='1 0x7dffc000 0 0x4000'),
              lambda:dt(extra='/memreserve/ 0x17dffc000 0x4000;')):
        try:validate_live_fdt(f(),memory_size(1984))
        except ValueError:pass
        else:raise AssertionError('unsafe expanded RAM accepted')
    validate_live_fdt(dt(reserve='1 0x7e000000 0 0x4000'),memory_size(1984))
    for f in (lambda:dt(reg='0 0x80000000 0 0x90000000'),lambda:dt(reserve='1 0x2000000 0 0x1000'),lambda:dt(extra='/memreserve/ 0x120000000 0x1000;')):
        try:validate_live_fdt(f(),1<<30)
        except ValueError:pass
        else:raise AssertionError('unsafe RAM accepted')
if a.live_dtb:
    for mib in MEMORY_MIB:print(validate_live_fdt(a.live_dtb,memory_size(mib)))
print('PASS loader profile predicate, bank bounds and both reservation mechanisms')
