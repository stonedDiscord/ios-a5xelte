#!/usr/bin/env python3
"""Observe actual compositor GPU progress; never replay frames or inject input.

Uses the existing sole console reader. Requires enabled/qualified fast copies.
Stops on quarantine, fallback, policy change, or counter regression. A pass only
establishes the observed interval, never physical image/input or source rendering.
"""
import argparse,importlib.util,json,re,time
from pathlib import Path
from a03_usb_probe import Probe
spec=importlib.util.spec_from_file_location('blit',Path(__file__).with_name('a03-gpu-blit-benchmark.py'))
blit=importlib.util.module_from_spec(spec);spec.loader.exec_module(blit)
POLICY=['enabled','verify','cached','warm','tile_rows','memattr','clock_mhz','poll_spin','idle_timeout_ms']
COUNTERS=['completed','verified','fallbacks','frames','cpu_copies','gpu_copies','idle_releases']
def validate(before,after):
    if after['quarantined']:raise RuntimeError('GPU quarantine: retain evidence and reboot; no recovery attempted')
    if after['fallbacks']!=before['fallbacks']:raise RuntimeError('GPU fallback during compositor interval')
    if any(before.get(k)!=after.get(k) for k in POLICY):raise RuntimeError('GPU policy changed during compositor interval')
    if any(after[k]<before[k] for k in COUNTERS):raise RuntimeError('Counter regression during compositor interval')
def validate_observed_commands(text):
    for command in re.findall(r'^A03 PROBE [0-9]+ BEGIN (.*)$',text.replace(chr(13),''),re.M):
        if command.startswith('display replay') or (command.startswith('gpu ') and command!='gpu blit'):
            raise RuntimeError('Concurrent replay/GPU control invalidates compositor observation: '+command)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--log',required=True,type=Path)
    p.add_argument('--seconds',type=int,default=600)
    p.add_argument('--interval',type=int,default=20)
    p.add_argument('--minimum-copies',type=int,default=12000)
    a=p.parse_args()
    if not 1<=a.seconds<=3600 or not 1<=a.interval<=60 or a.minimum_copies<1:p.error('seconds1..3600, interval1..60, minimum-copies>=1')
    with a.log.open('rb') as log,a.log.open('rb') as evidence,Probe() as probe:
        evidence.seek(0,2);observed=b''
        initial=blit.snapshot(probe,log)
        print(json.dumps(dict(kind='initial',snapshot=initial)),flush=True)
        if not initial['enabled'] or initial['verify'] or initial['verified']<4 or initial['quarantined']:
            raise RuntimeError('Requires healthy enabled fast mode with four full readbacks')
        started=time.monotonic();previous=initial
        while True:
            remaining=a.seconds-(time.monotonic()-started)
            if remaining<=0:break
            time.sleep(min(a.interval,remaining))
            current=blit.snapshot(probe,log)
            print(json.dumps(dict(kind='sample',elapsed_seconds=time.monotonic()-started,snapshot=current)),flush=True)
            observed+=evidence.read();validate_observed_commands(observed.decode(errors='replace'))
            validate(previous,current);previous=current
        count=previous['completed']-initial['completed']
        if count<a.minimum_copies:raise RuntimeError('Insufficient actual GPU compositor copies: '+str(count))
        print(json.dumps(dict(kind='result',completed_copies=count,observed_seconds=time.monotonic()-started,
            idle_releases=previous['idle_releases']-initial['idle_releases'],
            note='Observed GPU copy interval only; no replay/input sent, no physical UI or FPS claim')),flush=True)
if __name__=='__main__':main()
