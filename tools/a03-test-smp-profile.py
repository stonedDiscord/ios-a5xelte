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
print('PASS A03 CPU identities, state, unique phandles, roundtrip/default and trial bounds')
