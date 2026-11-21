#!/usr/bin/env python3
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('retire',Path(__file__).with_name('a03-gpu-retirement-report.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
line='A03 GPU retirement: stage=5 submitted=1 done=1 irq=00000002 mmu=00000000 gpu=00000100 js=00000000 asfault=00000000 rawgpu=00000000 rawjob=00000000 state=00000000 next=00000000 asstatus=00000000 aslo=20000000 ashi=00000001 cfg=62000006 frame=2041 clock=384 idle-releases=157'
r=m.parse(line)[0];assert r['stage']==5 and r['frame']==2041 and r['aslo']==0x20000000 and r['translation_retained']
for stage in range(1,8):assert m.parse(line.replace('stage=5','stage='+str(stage)))[0]['meaning']==m.STAGES[stage]
for bad in ['A03 GPU job: retirement unproven',line.replace('stage=5','stage=8'),line.replace(' cfg=62000006',''),line+' extra=1']:
 try:m.parse(bad);assert False
 except ValueError:pass
print('PASS retirement stage/raw-register decoding, missing snapshot and malformed evidence rejection')

summary='A03 GPU retirement: stage=5 submitted=1 done=1 frame=10935 clock=384 idle-releases=67'
regs='A03 GPU retirement-regs: irq=00000002 mmu=00000000 gpu=00000600 js=00000000 asfault=00000000 rawgpu=00000600 rawjob=00000000 state=00000000 next=00000000'
asline='A03 GPU retirement-as: asstatus=00000000 aslo=049e4000 ashi=00000001 cfg=62000006'
power='A03 GPU retirement-power: status=00000000 shader=00000001 l2=00000001 tiler=00000001 shadertrans=00000000 l2trans=00000000 tilertrans=00000000'
records=[summary,regs,asline,power]
assert all(len(x+'\n')<255 for x in records)
split='\nnoise\n'.join(records)
r=m.parse(split)[0];assert r['stage']==5 and r['frame']==10935 and r['rawgpu']==0x600 and r['shader']==1 and r['translation_retained']
assert len(m.parse(split+'\n'+line))==2
for bad in [summary,summary+'\n'+regs,summary+'\n'+asline+'\n'+power,split+'\n'+power,summary+'\n'+regs+'\n'+regs,split.replace('stage=5','stage=8'),line[:255],summary+' stage=5',summary+' junk',split.replace('shader=00000001','shader=00000001 unknown=1')]:
 try:m.parse(bad);assert False,bad
 except ValueError:pass
print('PASS bounded multipart records, legacy records, missing/duplicate/truncated/malformed field rejection')
