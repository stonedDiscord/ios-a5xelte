#!/usr/bin/env python3
"""A03 native-16K ADT; single A55 default, explicit validated SMP trials."""
import argparse
from pathlib import Path
import os
import copy
import struct
import adt
import mkadt as sweet
from a03_memory import PHYS_BASE, MEMORY_MIB, memory_size, validate_live_fdt


def configure_cpu_count(root,cpu_count):
    """Extend an existing A03 ADT without replacing its seed or other nodes."""
    if cpu_count not in (1,2,6,8):
        raise ValueError('unsupported A03 CPU count')
    cpus=next(n for n in root.children if n.name=='cpus')
    if not 1<=len(cpus.children)<=cpu_count:
        raise ValueError('cannot shrink or replace an existing CPU topology')
    for core,node in enumerate(cpus.children):
        expected=b'arm,cortex-a75' if core>=6 else b'arm,cortex-a55'
        if node.prop('reg')!=sweet.u32(core << 8) or not node.prop('compatible').startswith(expected):
            raise ValueError('unexpected existing A03 CPU identity')
    cp=cpus.children[0]
    def prop(n,k,v):
        n.props=[(a,f,v if a==k else b) for a,f,b in n.props]
    # Match live ums9230 Aff1 numbering; retain the single-CPU default.
    def phandles(n):
        values=[struct.unpack('<I',v)[0] for k,f,v in n.props if k=='AAPL,phandle']
        for child in n.children:values.extend(phandles(child))
        return values
    next_phandle=max(phandles(root),default=0)+1
    for core in range(len(cpus.children), cpu_count):
        sibling=copy.deepcopy(cp)
        for key,value in [('name',sweet.cstr('cpu'+str(core))),
                          ('reg',sweet.u32(core << 8)),('cpu-id',sweet.u32(core)),
                          ('compatible',sweet.cstr('arm,cortex-a75' if core>=6 else 'arm,cortex-a55')+sweet.cstr('ARM,v8')),
                          ('AAPL,phandle',sweet.u32(next_phandle+core-1)),
                          ('cluster-core-id',sweet.u32(core)),
                          ('l2-cache-id',sweet.u32(core)),
                          ('state',sweet.cstr('stopped'))]:
            prop(sibling,key,value)
        cpus.children.append(sibling)


def build(emmc=False, display=False, memory_mib=256, cpu_count=1):
    if cpu_count not in (1, 2, 6, 8):
        raise ValueError("A03 CPU trial supports 1, 2, 6 or 8 cores (six A55 + two A75)")
    mem_size=memory_size(memory_mib)
    root=sweet.build(seed=os.urandom(64),qemu=True)
    def prop(n,k,v):
        n.props=[(a,f,v if a==k else b) for a,f,b in n.props]
    by={n.name:n for n in root.children}
    chosen=by['chosen'];prop(chosen,'dram-base',sweet.u64(PHYS_BASE));prop(chosen,'dram-size',sweet.u64(mem_size))
    prop(chosen,'firmware-version',sweet.cstr('a03-shim'))
    cp=by['cpus'].children[0]
    prop(cp,'compatible',sweet.cstr('arm,cortex-a55')+sweet.cstr('ARM,v8'))
    prop(cp,'reg',sweet.u32(0));prop(cp,'timebase-frequency',sweet.u32(26000000))
    prop(cp,'fixed-frequency',sweet.u32(26000000));prop(cp,'peripheral-frequency',sweet.u32(26000000))
    prop(cp,'clock-frequency',sweet.u32(1600000000))
    configure_cpu_count(root,cpu_count)
    io=by['arm-io'];io.children=[n for n in io.children if n.name!='disp0']
    if display:
        io.children.append(sweet.node('disp0', [('device_type',sweet.cstr('display-subsystem')),
            ('compatible',sweet.cstr('a03,display')),('canvas-width',sweet.u32(720)),
            ('canvas-height',sweet.u32(1600))]))
    gic=next(n for n in io.children if n.name=='gic')
    prop(gic,'reg',sweet.u64(0x10000000-sweet.SOC_BASE,0x20000,0x10040000-sweet.SOC_BASE,0x100000))
    prop(gic,'virtual-timer-intid',sweet.u32(27))
    fb=by['sweet-fbcon'];prop(fb,'reg',sweet.u64(0x9e000000,0xab0000))
    prop(fb,'width',sweet.u32(720));prop(fb,'height',sweet.u32(1600));prop(fb,'stride',sweet.u32(2880))
    if emmc:
        root.children.append(sweet.node('a03-emmc', [('reg',sweet.u64(0x201d0000,0x1000))]))
    return root

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=Path);p.add_argument('--emmc-readonly',action='store_true');p.add_argument('--display',action='store_true',help='opt-in A03 iOS16 framebuffer nub (0123 required)');p.add_argument('--memory-mib',type=int,choices=MEMORY_MIB,default=256);p.add_argument('--memory-dtb',type=Path);p.add_argument('--cpu-count',type=int,choices=(1,2,6,8),default=1);a=p.parse_args()
    if a.cpu_count!=1:
        if a.memory_dtb is None:p.error('SMP trial requires --memory-dtb')
        import subprocess
        for core in range(a.cpu_count):
            node='/cpus/cpu@'+format(core << 8,'x')
            get=lambda key,kind:subprocess.check_output(['fdtget','-t',kind,str(a.memory_dtb),node,key],text=True).strip()
            if get('compatible','s')!=('arm,cortex-a75' if core>=6 else 'arm,cortex-a55') or get('enable-method','s')!='psci' or [int(v,16) for v in get('reg','x').split()]!=[0,core << 8]:
                p.error('unexpected live A03 CPU topology')
        conduit=subprocess.check_output(['fdtget','-t','s',str(a.memory_dtb),'/psci','method'],text=True).strip()
        if conduit!='smc':p.error('A03 CPU_ON requires SMC conduit')
    if a.memory_mib!=256 and a.memory_dtb is None:p.error('expanded RAM requires --memory-dtb')
    if a.memory_dtb:print(validate_live_fdt(a.memory_dtb,memory_size(a.memory_mib)))
    blob=adt.serialize(build(a.emmc_readonly,a.display,a.memory_mib,a.cpu_count));root,end=adt.parse(blob);assert end==len(blob)
    assert not any(n.name=='sweet-ufs' for n in root.children)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(blob)
    print('A03 ADT',len(blob),'bytes;',a.memory_mib,'MiB upper-bank window;',a.cpu_count,'CPU nodes (six A55 maximum; remaining A75; SMP needs0157/0158)')
