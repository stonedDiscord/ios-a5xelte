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
assert m.report(b,dict(b,gpu_copies=1,gpu_ns=100,fallbacks=1),'fast')['result'].startswith('mixed:')
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
values=iter(['enabled=1 frames=4 pixels=4608000 fallbacks=0 quarantined=0 verify=1 verified=4 completed=4 total-ns=123 last-ns=12','copy timing cpu=28/280ns gpu=4/123ns copy thread-runtime cpu=250ns gpu=90ns'])
assert m.snapshot(None,None)['gpu_runtime_ns']==90
rb=dict(b,cpu_runtime_ns=100,gpu_runtime_ns=200)
ra=dict(rb,cpu_copies=2,cpu_ns=2000,cpu_runtime_ns=700)
assert m.report(rb,ra,'cpu')['mean_submitter_cpu_ms']==0.0003
try:m.report(ra,dict(ra,cpu_runtime_ns=699),'cpu');assert False
except RuntimeError:pass
try:m.report(rb,b,'cpu');assert False
except RuntimeError:pass

values=iter(['','','enabled=1 frames=4 pixels=4608000 fallbacks=0 quarantined=0 verify=1 verified=4 completed=4 total-ns=123 last-ns=12','copy timing cpu=28/280ns gpu=4/123ns'])
assert m.snapshot(None,None)['gpu_ns']==123
busy_calls=[]
def busy_command(*args):
 busy_calls.append(args[-1]);return ''
m.command=busy_command
try:m.snapshot(None,None);assert False
except RuntimeError:pass
assert busy_calls==['gpu blit']*10+['display']
m.command=lambda *args:next(values)

values=iter(['enabled=1 frames=4 pixels=4608000 fallbacks=0 quarantined=0 verify=1 verified=4 completed=4 total-ns=123 last-ns=12 phases-ns: power=1 prepare=2 cache=3 execute=4 retire=5 verify=6 shutdown=7','copy timing cpu=28/280ns gpu=4/123ns'])
phases=m.snapshot(None,None)['last_attempt_phases_ns']
values=iter(['A03 GPU blit: cached=1; four readbacks after policy change enabled=1 frames=4 pixels=4608000 fallbacks=0 quarantined=0 verify=1 verified=4 completed=4 total-ns=123 last-ns=12','copy timing cpu=28/280ns gpu=4/123ns'])
assert m.snapshot(None,None)['cached']==1
values=iter(['A03 GPU blit: cached=1; A03 GPU blit: warm=1 powered=1; enabled=1 frames=4 pixels=4608000 fallbacks=0 quarantined=0 verify=1 verified=4 completed=4 total-ns=123 last-ns=12','copy timing cpu=28/280ns gpu=4/123ns'])
assert m.snapshot(None,None)['powered']==1
values=iter(['A03 GPU blit: tile-rows=16; enabled=1 frames=4 pixels=4608000 fallbacks=0 quarantined=0 verify=1 verified=4 completed=4 total-ns=123 last-ns=12','copy timing cpu=28/280ns gpu=4/123ns'])
assert m.snapshot(None,None)['tile_rows']==16
values=iter(['A03 GPU blit: memattr=2; enabled=1 frames=4 pixels=4608000 fallbacks=0 quarantined=0 verify=1 verified=4 completed=4 total-ns=123 last-ns=12','copy timing cpu=28/280ns gpu=4/123ns'])
assert m.snapshot(None,None)['memattr']==2
values=iter(['A03 GPU blit: clock-mhz=512; enabled=1 frames=4 pixels=4608000 fallbacks=0 quarantined=0 verify=1 verified=4 completed=4 total-ns=123 last-ns=12','copy timing cpu=28/280ns gpu=4/123ns'])
assert m.snapshot(None,None)['clock_mhz']==512
values=iter(['A03 GPU blit: poll-spin=1 gaps=10 gap-ns=100000 enabled=1 frames=4 pixels=4608000 fallbacks=0 quarantined=0 verify=1 verified=4 completed=4 total-ns=123 last-ns=12','copy timing cpu=28/280ns gpu=4/123ns'])
assert m.snapshot(None,None)['poll_spin']==1
pb=dict(b,poll_spin=1,poll_gaps=10,poll_gap_ns=100000)
pa=dict(pb,poll_gaps=14,poll_gap_ns=140000,gpu_copies=1,gpu_ns=100)
assert m.report(pb,pa,'fast')['poll_gaps']==4
try:m.report(dict(pb,poll_spin=0),pa,'fast');assert False
except RuntimeError as error:assert 'GPU poll policy changed' in str(error)

assert m.report(dict(b,clock_mhz=512),dict(b,clock_mhz=512,gpu_copies=1,gpu_ns=100),'fast')['clock_mhz']==512
try:m.report(dict(b,clock_mhz=384),dict(b,clock_mhz=512),'fast');assert False
except RuntimeError as error:assert 'GPU clock policy changed' in str(error)

assert m.report(dict(b,memattr=2),dict(b,memattr=2,gpu_copies=1,gpu_ns=100),'fast')['memattr']==2
try:m.report(dict(b,memattr=0),dict(b,memattr=1),'fast');assert False
except RuntimeError as error:assert 'Pixel cache attribute changed' in str(error)

assert m.report(dict(b,tile_rows=16),dict(b,tile_rows=16,gpu_copies=1,gpu_ns=100),'fast')['tile_rows']==16
try:m.report(dict(b,tile_rows=4),dict(b,tile_rows=16),'fast');assert False
except RuntimeError as error:assert 'Dispatch tile changed' in str(error)

try:m.report(dict(b,warm=0),dict(b,warm=1,powered=1),'fast');assert False
except RuntimeError as error:assert 'Power policy changed' in str(error)
assert m.report(dict(b,cached=1),dict(b,cached=1,gpu_copies=1,gpu_ns=100),'fast')['cached']==1
try:m.report(dict(b,cached=0),dict(b,cached=1),'fast');assert False
except RuntimeError as error:assert 'Cache policy changed' in str(error)
assert phases==dict(power=1,prepare=2,cache=3,execute=4,retire=5,verify=6,shutdown=7)
sample=dict(b,frames=1,gpu_copies=1,gpu_ns=100,last_attempt_phases_ns=phases)
assert m.report(b,sample,'fast')['last_attempt_phases_ms']['execute']==0.000004
assert 'last_attempt_phases_ms' not in m.report(b,sample,'cpu')
assert 'last_attempt_phases_ms' not in m.report(sample,sample,'fast')
m.command=original_command
for reply,valid in [('A03 REPLAY: requested=4 copied=4 elapsed-ns=100 quarantined=0',True),('A03 REPLAY: no accepted frame or quarantined',False),('A03 REPLAY: requested=4 copied=3 elapsed-ns=100 quarantined=0',False),('A03 REPLAY: requested=4 copied=4 elapsed-ns=100 quarantined=1',False)]:
 m.command=lambda *args:reply
 try:assert m.replay(None,None,4)==100;assert valid
 except RuntimeError:assert not valid
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
seq=[];snapshots=[dict(original),dict(original,enabled=1,verify=0),RuntimeError('sample interrupted'),dict(original)]
def interrupted_snapshot(*args):
 value=snapshots.pop(0)
 if isinstance(value,Exception):raise value
 return value
m.snapshot=interrupted_snapshot;m.command=lambda p,l,c:seq.append(c)
with tempfile.NamedTemporaryFile() as f:
 sys.argv=['benchmark','--log',f.name,'--mode','fast','--seconds','1']
 try:m.main();assert False
 except RuntimeError as error:assert str(error)=='sample interrupted'
assert seq[-2:]==['gpu blit verify','gpu blit on']
seq=[];snapshots=[dict(original),dict(original,enabled=0),dict(original,enabled=0,cpu_copies=4,cpu_ns=40000000),dict(original)]
m.snapshot=lambda *args:snapshots.pop(0);m.command=lambda p,l,c:seq.append(c) or ('A03 REPLAY: requested=4 copied=4 elapsed-ns=40000000 quarantined=0' if c=='display replay 4' else '')
with tempfile.NamedTemporaryFile() as f:
 sys.argv=['benchmark','--log',f.name,'--mode','cpu','--replay','4'];m.main()
assert 'display replay 4' in seq and seq[-2:]==['gpu blit verify','gpu blit on']
print('PASS benchmark exact transaction, counter reset/zero-frame handling, mode restoration')
