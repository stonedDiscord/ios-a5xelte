#!/usr/bin/env python3
"""Reject misleading paired-copy samples without accessing hardware."""
import importlib.util
import json
from pathlib import Path

spec=importlib.util.spec_from_file_location('paired',Path(__file__).with_name('a03-gpu-paired-benchmark.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
cpu=dict(mode='cpu',cpu_copies=8,gpu_copies=0,fallbacks=0,quarantined=0,mean_copy_ms=1.4,verified=0,completed=0,frames=0)
gpu=dict(cpu,mode='fast',cpu_copies=0,gpu_copies=8,completed=8,frames=8)
for value in [cpu,gpu]:m.validate(value,value['mode'],8)
for change in [dict(gpu_copies=7),dict(cpu_copies=1),dict(fallbacks=1),dict(quarantined=1),dict(verified=1),dict(completed=7),dict(frames=7),dict(mean_copy_ms=None)]:
    try:m.validate(dict(gpu,**change),'fast',8);raise AssertionError(change)
    except RuntimeError:pass
assert m.parse_result('unrelated {invalid} text '+json.dumps(dict(mean_copy_ms=1.5))+' trailing')['mean_copy_ms']==1.5
print('PASS paired benchmark exact counts, mixed modes, faults, warmup and JSON isolation')
