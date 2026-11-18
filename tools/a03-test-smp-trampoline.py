#!/usr/bin/env python3
"""Exercise actual loader ADT parser, bounds and shim trampoline encoding."""
import ctypes, struct, subprocess, sys, tempfile
from pathlib import Path
import adt, mkadt_a03
ROOT=Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory() as tmp:
    t=Path(tmp)
    (t/'test.c').write_text('#include "smp-trampoline.h"'+chr(10)+'''int check(unsigned char *p,uint32_t n){unsigned char *h=0; if(!a03_dt_smp_handoff(p,n,&h))return -1;return h?(int)(h-p):0;}''')
    subprocess.run(['clang','-Wall','-Wextra','-Werror','-shared','-fPIC','-I',str(ROOT/'shim/a03'),str(t/'test.c'),'-o',str(t/'test.so')],check=True)
    lib=ctypes.CDLL(str(t/'test.so'));lib.check.argtypes=[ctypes.c_void_p,ctypes.c_uint32]
    def check(b):
        buf=ctypes.create_string_buffer(b);return lib.check(buf,len(b))
    tree=mkadt_a03.build(memory_mib=1984,cpu_count=2)
    original=adt.serialize(tree);assert check(original)==0
    chosen=next(n for n in tree.children if n.name=='chosen')
    prop=('a03-smp-trampoline',0,struct.pack('<QQ',0,0x103481000))
    chosen.props.append(prop);blob=adt.serialize(tree);offset=check(blob)
    assert offset>0 and blob[offset:offset+16]==prop[2]
    for length in range(len(blob)):assert check(blob[:length])==-1,length
    assert check(blob+bytes(4))==-1
    chosen.props.append(prop);assert check(adt.serialize(tree))==-1;chosen.props.pop()
    chosen.props[-1]=('a03-smp-trampoline',0,bytes(8));assert check(adt.serialize(tree))==-1
    for offset in (0,4,40):
        bad=bytearray(blob);struct.pack_into('<I',bad,offset,0xffffffff);assert check(bytes(bad))==-1

# Verify0158 with CI's application mechanism against the actual0157 buildtree.
import argparse, shutil
parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path);args=parser.parse_args()
if args.source:
    patch=ROOT/'xnu/a03/0158-a03-loader-owned-smp-trampoline.patch'
    subprocess.run(['git','apply','--check',str(patch)],cwd=args.source,check=True)
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);name=Path('iokit/Kernel/arm/SweetCPU.cpp')
        (root/name).parent.mkdir(parents=True);shutil.copyfile(args.source/name,root/name)
        subprocess.run(['git','apply',str(patch)],cwd=root,check=True)
        source=(root/name).read_text()
        assert 'const void *value = NULL;' in source
        assert 'handoff[1] != (uint64_t)entry' in source
        assert source.index('entry = (vm_offset_t)handoff[0]')<source.index('int32_t rc = sweet_psci_cpu_on')
        subprocess.run(['git','apply','--reverse','--check',str(patch)],cwd=root,check=True)
subprocess.run(['sh',str(ROOT/'shim/a03/build-xnu.sh')],check=True)
symbols=subprocess.check_output(['llvm-nm',str(ROOT/'shim/a03/out/a03-xnu-loader.elf')],text=True)
addresses={line.split()[-1]:int(line.split()[0],16) for line in symbols.splitlines() if len(line.split())==3}
code=(ROOT/'shim/a03/out/a03-xnu-loader.Image').read_bytes();at=addresses['a03_smp_trampoline']
assert at%16==0 and addresses['a03_smp_target']==at+8
assert struct.unpack_from('<IIQ',code,at)==(0x58000050,0xd61f0200,0)
print('PASS actual ADT parser all truncations/duplicates/lengths, low trampoline encoding/alignment and loader build')
