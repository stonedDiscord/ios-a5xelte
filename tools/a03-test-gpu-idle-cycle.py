#!/usr/bin/env python3
"""Reject misleading idle-cycle evidence without device access."""
import importlib.util,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
spec=importlib.util.spec_from_file_location('idle',Path(__file__).with_name('a03-gpu-idle-cycle.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
b=dict(enabled=1,verify=0,cached=1,warm=1,tile_rows=4,memattr=0,clock_mhz=384,poll_spin=0,idle_timeout_ms=100,quarantined=0,fallbacks=0,completed=4,verified=4)
a=dict(b,completed=5);m.validate(b,a)
for change in [dict(enabled=0),dict(warm=0),dict(quarantined=1),dict(fallbacks=1),dict(completed=4),dict(verified=3)]:
 try:m.validate(b,dict(a,**change));assert False
 except RuntimeError:pass
# Actual loop must see an idle release between each resumed job.
import tempfile
from contextlib import redirect_stdout
from io import StringIO
class Context:
 def __enter__(self):return self
 def __exit__(self,*args):pass
m.Probe=Context;m.time.sleep=lambda *args:None
initial=dict(b,powered=0,idle_releases=1,last_ns=1)
seq=[initial,initial,dict(initial,completed=5,powered=1),dict(initial,completed=5,idle_releases=2),dict(initial,completed=6,idle_releases=2,powered=1)]
m.blit.snapshot=lambda *args:seq.pop(0);replays=[]
m.blit.replay=lambda p,l,n:replays.append(n)
with tempfile.NamedTemporaryFile() as f,redirect_stdout(StringIO()) as output:
 sys.argv=['idle','--log',f.name,'--cycles','2'];m.main()
assert not seq and replays==[1,1] and 'Verified idle/cold-resume cycle 2' in output.getvalue()
print('PASS idle-cycle policy/fault/qualification and actual two-cycle control flow')
