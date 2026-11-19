#!/usr/bin/env python3
from pathlib import Path
import importlib.util,sys,io,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
spec=importlib.util.spec_from_file_location('benchmark',str(ROOT/'tools/a03-gpu-blit-benchmark.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
fields=['frames','pixels','fallbacks','verified','completed','cpu_copies','cpu_ns','gpu_copies','gpu_ns']
b={k:0 for k in fields};b['quarantined']=0
a=dict(b,cpu_copies=10,cpu_ns=100000000)
r=m.report(b,a,'cpu');assert r['mean_copy_ms']==10 and r['cpu_copies']==10
assert m.report(b,b,'fast')['mean_copy_ms'] is None
try:m.report(a,b,'cpu');assert False
except RuntimeError:pass
class Probe:
 def __init__(self,log):self.log=log
 def send(self,cmd):
  position=self.log.tell()
  self.log.write(b'A03 PROBE 3 BEGIN unrelated'+bytes([10])+b'A03 PROBE 3 END'+bytes([10]))
  self.log.write(b'A03 PROBE 4 BEGIN '+cmd.encode()+bytes([13,10])+b'correct reply'+bytes([13,10])+b'A03 PROBE 4 END'+bytes([13,10]))
  self.log.seek(position)
with tempfile.TemporaryFile() as log:assert m.command(Probe(log),log,'display').strip()=='correct reply'
values=iter(['enabled=1 frames=4 pixels=4608000 fallbacks=0 quarantined=0 verify=1 verified=4 completed=4 total-ns=123 last-ns=12','copy timing cpu=28/280ns gpu=4/123ns'])
original_command=m.command;m.command=lambda *args:next(values)
assert m.snapshot(None,None)['gpu_ns']==123
m.command=original_command
original=dict(b,enabled=1,verify=1)
for mode in ['cpu','verify','fast']:
 seq=[];snapshots=[dict(original),dict(original,enabled=int(mode!='cpu'),verify=int(mode=='verify') if mode!='cpu' else 1),dict(original,enabled=int(mode!='cpu'),verify=int(mode=='verify') if mode!='cpu' else 1),dict(original)]
 class Context:
  def __enter__(self):return self
  def __exit__(self,*args):pass
 m.Probe=Context;m.snapshot=lambda *args:snapshots.pop(0);m.command=lambda p,l,c:seq.append(c)
 m.time.sleep=lambda seconds:None
 with tempfile.NamedTemporaryFile() as f:
  sys.argv=['benchmark','--log',f.name,'--mode',mode,'--seconds','1'];m.main()
 assert seq[-2:]==['gpu blit verify','gpu blit on']
print('PASS benchmark exact transaction, counter reset/zero-frame handling, mode restoration')
