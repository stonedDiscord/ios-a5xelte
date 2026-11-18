#!/usr/bin/env python3
"""Check A03 ADT CPU identities and actual SMP patch application."""
from pathlib import Path
import argparse, importlib.util, struct, subprocess, sys, tempfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
import adt, mkadt_a03
ROOT=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser();p.add_argument('--source',type=Path);a=p.parse_args()
for count in (1,2,6):
    tree=mkadt_a03.build(memory_mib=1984,cpu_count=count)
    cpus=next(n for n in tree.children if n.name=='cpus').children
    assert len(cpus)==count
    for i,node in enumerate(cpus):
        assert node.name=='cpu'+str(i)
        assert node.prop('reg')==struct.pack('<I',i<<8)
        assert node.prop('compatible').startswith(b'arm,cortex-a55')
        assert node.prop('state')==(b'running'+bytes(1) if i==0 else b'stopped'+bytes(1))
    def ph(n):
        values=[v for k,f,v in n.props if k=='AAPL,phandle']
        for c in n.children:values.extend(ph(c))
        return values
    values=ph(tree);assert len(values)==len(set(values))
    blob=adt.serialize(tree);assert adt.parse(blob)[1]==len(blob)
for count in (0,3,7,8):
    try:mkadt_a03.build(cpu_count=count)
    except ValueError:pass
    else:raise AssertionError('unsupported CPU trial accepted')
if a.source:
    patch=ROOT/'xnu/a03/0157-a03-opt-in-psci-smp.patch'
    # Plain git apply is the actual CI patch mechanism.
    subprocess.run(['git','apply','--check',str(patch)],cwd=a.source,check=True)
    import shutil
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        files=('iokit/Kernel/arm/SweetCPU.cpp','osfmk/arm64/cpu.c',
               'osfmk/arm64/machine_routines.c','osfmk/arm64/start.s',
               'pexpert/pexpert/arm64/SWEET.h')
        for name in files:
            target=root/name;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(a.source/name,target)
        subprocess.run(['git','apply',str(patch)],cwd=root,check=True)
        cpu=(root/files[0]).read_text()
        assert 'target->getCPUNumber()' in cpu
        assert 'topology->cpus[logical].phys_id' in cpu
        assert 'processor_start(cpu->machProcessor)' in cpu
        assert 'cpu_start() discards' in cpu and 'if (rc != 0)' in cpu
        assert cpu.index('ml_cpu_init_completed();')>cpu.index('startup timeout')
        asm=(root/files[3]).read_text()
        assert '0x33ff' in asm and 'HSTR_EL2' in asm and 'ICH_HCR_EL2' in asm
        assert 'HAS_CLUSTER || defined(SWEET)' in asm
        topology=(root/files[2]).read_text()
        assert '!cpus_boot_arg_present || cpu_boot_arg == 0' in topology
        subprocess.run(['git','apply','--reverse','--check',str(patch)],cwd=root,check=True)
print('PASS A03 CPU identities, state, unique phandles, roundtrip/default and trial bounds')
