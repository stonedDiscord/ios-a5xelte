#!/usr/bin/env python3
"""Minimal A03 single-A55 native-16K ADT; no storage/peripheral drivers."""
import argparse
from pathlib import Path
import os
import adt
import mkadt as sweet

PHYS_BASE=0x102000000  # 32 MiB aligned for XNU's bootstrap L2 block mappings.
MEM_SIZE=0x10000000

def build():
    root=sweet.build(seed=os.urandom(64),qemu=True)
    def prop(n,k,v):
        n.props=[(a,f,v if a==k else b) for a,f,b in n.props]
    by={n.name:n for n in root.children}
    chosen=by['chosen'];prop(chosen,'dram-base',sweet.u64(PHYS_BASE));prop(chosen,'dram-size',sweet.u64(MEM_SIZE))
    prop(chosen,'firmware-version',sweet.cstr('a03-shim'))
    cp=by['cpus'].children[0]
    prop(cp,'compatible',sweet.cstr('arm,cortex-a55')+sweet.cstr('ARM,v8'))
    prop(cp,'reg',sweet.u32(0));prop(cp,'timebase-frequency',sweet.u32(26000000))
    prop(cp,'fixed-frequency',sweet.u32(26000000));prop(cp,'peripheral-frequency',sweet.u32(26000000))
    prop(cp,'clock-frequency',sweet.u32(1600000000))
    io=by['arm-io'];io.children=[n for n in io.children if n.name!='disp0']
    gic=next(n for n in io.children if n.name=='gic')
    prop(gic,'reg',sweet.u64(0x10000000-sweet.SOC_BASE,0x20000,0x10040000-sweet.SOC_BASE,0x100000))
    prop(gic,'virtual-timer-intid',sweet.u32(27))
    fb=by['sweet-fbcon'];prop(fb,'reg',sweet.u64(0x9e000000,0xab0000))
    prop(fb,'width',sweet.u32(720));prop(fb,'height',sweet.u32(1600));prop(fb,'stride',sweet.u32(2880))
    return root

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=Path);a=p.parse_args()
    blob=adt.serialize(build());root,end=adt.parse(blob);assert end==len(blob)
    assert not any(n.name=='sweet-ufs' for n in root.children)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(blob)
    print('A03 ADT',len(blob),'bytes; 256 MiB upper-bank window; single A55')
