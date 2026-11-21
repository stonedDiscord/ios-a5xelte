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
