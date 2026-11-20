#!/usr/bin/env python3
"""Alternate CPU/fast accepted-frame replays using one existing console log.

No flash, reset, synthetic input, surface creation or cache/power policy
changes. Each child restores its original enable/readback policy.
"""
import argparse
import json
from pathlib import Path
import statistics
import subprocess
import sys


def parse_result(output):
    decoder=json.JSONDecoder()
    for pos,char in enumerate(output):
        if char!='{':continue
        try:value,_=decoder.raw_decode(output[pos:])
        except ValueError:continue
        if isinstance(value,dict) and 'mean_copy_ms' in value:return value
    raise RuntimeError('Child did not report a copy measurement')


def validate(result,mode,count):
    key='cpu_copies' if mode=='cpu' else 'gpu_copies'
    other='gpu_copies' if mode=='cpu' else 'cpu_copies'
    if result['mode']!=mode or result[key]!=count or result[other] or result['fallbacks'] or result['quarantined']:
        raise RuntimeError('Mixed or incomplete replay interval; discard paired trial')
    if result['mean_copy_ms'] is None or result['mean_copy_ms']<=0:
        raise RuntimeError('No positive copy timing')
    if mode=='fast' and (result['verified'] or result['completed']!=count or result['frames']!=count):
        raise RuntimeError('Fast replay included verification or incomplete jobs')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--log',type=Path,required=True)
    p.add_argument('--rounds',type=int,choices=range(2,7),default=3)
    p.add_argument('--replay',type=int,choices=[4,8],default=8)
    a=p.parse_args();results=[];policy=None
    for index in range(a.rounds):
        for mode in (['cpu','fast'] if index%2==0 else ['fast','cpu']):
            run=subprocess.run([sys.executable,str(Path(__file__).with_name('a03-gpu-blit-benchmark.py')),
                '--log',str(a.log),'--mode',mode,'--replay',str(a.replay)],capture_output=True,text=True)
            print(run.stdout,end='',flush=True)
            if run.returncode:raise RuntimeError(run.stderr or 'Benchmark failed')
            if 'Original GPU mode restored.' not in run.stdout:raise RuntimeError('Mode restoration absent')
            result=parse_result(run.stdout);validate(result,mode,a.replay)
            current=(result.get('cached'),result.get('warm'),result.get('tile_rows'))
            if policy is not None and current!=policy:raise RuntimeError('Policy changed across paired rounds')
            policy=current;result['round']=index+1;results.append(result)
    cpu=[r['mean_copy_ms'] for r in results if r['mode']=='cpu']
    gpu=[r['mean_copy_ms'] for r in results if r['mode']=='fast']
    print(json.dumps(dict(cpu_ms=cpu,gpu_ms=gpu,cpu_median_ms=statistics.median(cpu),
        gpu_median_ms=statistics.median(gpu),cpu_over_gpu=statistics.median(cpu)/statistics.median(gpu),
        note='Accepted-frame synchronous copy timing, not physical animation FPS',samples=results),indent=2))


if __name__=='__main__':main()
