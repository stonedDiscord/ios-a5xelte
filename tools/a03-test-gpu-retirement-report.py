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
