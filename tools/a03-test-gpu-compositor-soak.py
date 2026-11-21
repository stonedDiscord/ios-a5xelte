#!/usr/bin/env python3
"""Guard real compositor observations against false success; no hardware claim."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('soak',Path(__file__).with_name('a03-gpu-compositor-soak.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
a=dict(enabled=1,verify=0,cached=1,warm=1,tile_rows=4,memattr=0,clock_mhz=384,poll_spin=0,idle_timeout_ms=100,
       completed=20,verified=4,fallbacks=0,frames=20,cpu_copies=2,gpu_copies=20,idle_releases=3,quarantined=0)
m.validate(a,{**a,'completed':24,'frames':24,'gpu_copies':24,'idle_releases':4})
for field,value in [('quarantined',1),('fallbacks',1),('completed',19),('verified',3),('enabled',0),('verify',1),('cached',0),('warm',0),('clock_mhz',512)]:
 try:m.validate(a,{**a,field:value});assert False,field
 except RuntimeError:pass
source=Path(m.__file__).read_text()
assert 'blit.replay(' not in source and 'blit.command(' not in source
print('PASS compositor soak counter/policy/quarantine guards and read-only operation')
