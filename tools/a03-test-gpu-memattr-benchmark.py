#!/usr/bin/env python3
"""Reject unqualified or mixed pixel cache comparisons; no device access."""
import importlib.util
import json
from pathlib import Path
import sys
root=Path(__file__).resolve().parent;sys.path.insert(0,str(root))
spec=importlib.util.spec_from_file_location('tile',root/'a03-gpu-memattr-benchmark.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
b=dict(memattr=1,tile_rows=4,enabled=1,verify=1,quarantined=0,fallbacks=0,verified=0,completed=0,cached=1,warm=1)
a=dict(b,verified=4,completed=4)
m.qualified(b,a,1)
for change in [dict(memattr=0),dict(enabled=0),dict(verify=0),dict(quarantined=1),dict(fallbacks=1),dict(verified=3),dict(completed=3),dict(cached=0),dict(warm=0),dict(tile_rows=8)]:
 try:m.qualified(b,dict(a,**change),1);raise AssertionError(change)
 except RuntimeError:pass
expected=dict(cpu_median_ms=1.5,gpu_median_ms=2.1,samples=[dict(tile_rows=8)])
assert m.paired_result('junk {bad} '+json.dumps(dict(mean_copy_ms=1))+' '+json.dumps(expected))==expected
try:m.paired_result(json.dumps(dict(mean_copy_ms=1)));raise AssertionError('partial child accepted')
except RuntimeError:pass
# Exercise the complete failure path, confirming restoration after a partial replay.
import tempfile
original=dict(b,enabled=0,verify=1,memattr=0)
seq=[];snapshots=[original,dict(b),original]
class Context:
 def __enter__(self):return self
 def __exit__(self,*args):pass
m.Probe=Context;m.blit.snapshot=lambda *args:snapshots.pop(0)
m.blit.command=lambda p,l,c:seq.append(c)
def fail(*args):raise RuntimeError('partial replay')
m.blit.replay=fail
with tempfile.NamedTemporaryFile() as f:
 sys.argv=['tile','--log',f.name,'--policies','cacheall']
 try:m.main();raise AssertionError('partial replay accepted')
 except RuntimeError as error:assert str(error)=='partial replay'
assert seq[-4:]==['gpu blit off','gpu blit impldef','gpu blit verify','gpu blit off']
print('PASS cache qualification, policy isolation, complete result parsing and failure restoration')
