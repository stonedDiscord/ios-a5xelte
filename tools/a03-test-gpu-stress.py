#!/usr/bin/env python3
"""Reject invalid retained-frame stress evidence; no device access."""
import importlib.util,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
spec=importlib.util.spec_from_file_location('stress',Path(__file__).with_name('a03-gpu-stress.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
b=dict(cached=1,warm=1,tile_rows=4,memattr=0,clock_mhz=384,poll_spin=0,quarantined=0,fallbacks=0,completed=4,verified=4)
a=dict(b,completed=516)
m.validate(b,a,512,False)
for change in [dict(cached=0),dict(quarantined=1),dict(fallbacks=1),dict(completed=515),dict(verified=5),dict(poll_spin=1)]:
 try:m.validate(b,dict(a,**change),512,False);assert False
 except RuntimeError:pass
m.validate(b,dict(b,completed=8,verified=8),4,True)
try:m.validate(b,dict(b,completed=8,verified=7),4,True);assert False
except RuntimeError:pass
print('PASS stress policy/complete-copy/fault/fallback/fresh-readback validation')
# Exercise both terminal readbacks and restoration after a replay failure.
from contextlib import redirect_stdout
from io import StringIO
import tempfile
original=dict(b,enabled=0,verify=1,cpu_copies=0,cpu_ns=0,gpu_copies=0,gpu_ns=0,frames=0,pixels=0,total_ns=0,last_ns=0,poll_gaps=0,poll_gap_ns=0,powered=0)
before=dict(original,enabled=1,verify=0)
after=dict(before,frames=8,pixels=9216000,completed=12,gpu_copies=8,gpu_ns=16000000)
qbefore=dict(after,verify=1);qafter=dict(qbefore,frames=12,pixels=13824000,completed=16,verified=8,gpu_copies=12,gpu_ns=120000000)
class Context:
 def __enter__(self):return self
 def __exit__(self,*args):pass
m.Probe=Context;m.time.sleep=lambda *args:None
for fail in [False,True]:
 seq=[];replays=[];snapshots=[original,before,original] if fail else [original,before,after,qbefore,qafter,original]
 m.blit.snapshot=lambda *args:snapshots.pop(0)
 m.blit.command=lambda p,l,c:seq.append(c)
 def replay(p,l,count):
  replays.append(count)
  if fail:raise RuntimeError('replay failed')
  return count
 m.blit.replay=replay;output=StringIO()
 with tempfile.NamedTemporaryFile() as f,redirect_stdout(output):
  sys.argv=['stress','--log',f.name,'--batches','1']
  if fail:
   try:m.main();assert False
   except RuntimeError as error:assert str(error)=='replay failed'
  else:m.main()
 assert not snapshots and seq[-3:]==['gpu blit off','gpu blit verify','gpu blit off']
 assert replays==([8] if fail else [8,4])
 if not fail:assert '"final_full_readbacks": 4' in output.getvalue()
print('PASS complete stress success/final readbacks and replay-failure mode restoration')
