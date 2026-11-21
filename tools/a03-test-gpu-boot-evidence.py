#!/usr/bin/env python3
"""Reject incomplete or host-driven automatic-start claims; no phone access."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('boot',Path(__file__).with_name('a03-verify-gpu-boot.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
marker='A03 GPU boot: cached warm384 defaultwait; four full readbacks before fast copies'+chr(10)
verified='A03 GPU blit: pixels=1152000 mismatches=0 done=1 retired=1 verify=1 PASS=1'+chr(10)
fast=verified.replace('verify=1','verify=0')
good=marker+verified*4+fast
assert m.verify(good)['full_readbacks']==4
assert m.verify('A03 PROBE 1 BEGIN gpu blit'+chr(10)+good)['prior_host_gpu_mutations']==0
for bad in [marker+verified*3+fast,marker+verified*4,good+marker,good.replace('mismatches=0','mismatches=1',1),good.replace('done=1','done=0',1),good.replace('retired=1','retired=0',1)]:
 try:m.verify(bad);assert False
 except ValueError:pass
for command in ['gpu clocks','gpu blit on','gpu blit cached','display replay 4']:
 try:m.verify('A03 PROBE 4 BEGIN '+command+chr(10)+good);assert False
 except ValueError:pass
assert m.verify(good+'A03 PROBE 5 BEGIN gpu blit off'+chr(10))['fast_copy']
print('PASS autonomous GPU evidence, four-readback order, failed-job and prior-host-control rejection')
