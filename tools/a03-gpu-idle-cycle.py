#!/usr/bin/env python3
"""Verify real idle release and cold resumption using retained-frame copies.

Requires already enabled, four-frame qualified0191. No mode/policy/input
changes; each iteration waits for observed automatic power-off, then replays
one copy and checks completion. Not proof of physical touch or visible wake.
"""
import argparse,importlib.util,json,time
from pathlib import Path
from a03_usb_probe import Probe
spec=importlib.util.spec_from_file_location('blit',Path(__file__).with_name('a03-gpu-blit-benchmark.py'))
blit=importlib.util.module_from_spec(spec);spec.loader.exec_module(blit)
POLICY=['enabled','verify','cached','warm','tile_rows','memattr','clock_mhz','poll_spin','idle_timeout_ms']
def validate(before,after):
    if any(before.get(k)!=after.get(k) for k in POLICY):raise RuntimeError('Idle-cycle policy changed')
    if after['quarantined'] or after['fallbacks']!=before['fallbacks']:raise RuntimeError('Idle-cycle fault/fallback')
    if after['completed']<=before['completed']:raise RuntimeError('No cold-resumed GPU copy')
    if after['verified']<before['verified']:raise RuntimeError('Readback qualification reset')
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--log',type=Path,required=True)
    p.add_argument('--cycles',type=int,default=12);a=p.parse_args()
    if not 1<=a.cycles<=64:p.error('cycles must be1..64')
    with a.log.open('rb') as log,Probe() as probe:
        initial=blit.snapshot(probe,log)
        if not initial['enabled'] or initial['verified']<4 or initial.get('idle_timeout_ms')!=100:
            raise RuntimeError('Requires enabled four-frame qualified0191')
        results=[];prior=initial
        for index in range(a.cycles):
            deadline=time.monotonic()+10
            while True:
                time.sleep(.2);idle=blit.snapshot(probe,log)
                if idle['quarantined']:raise RuntimeError('Quarantine during idle wait')
                if not idle['powered'] and (index==0 or idle['idle_releases']>prior['idle_releases']):break
                if time.monotonic()>deadline:raise RuntimeError('Automatic idle release not observed; background activity may prevent idle')
            blit.replay(probe,log,1);after=blit.snapshot(probe,log);validate(idle,after)
            results.append(dict(cycle=index+1,idle_releases=idle['idle_releases'],completed=after['completed'],last_ns=after['last_ns']))
            prior=idle;print('Verified idle/cold-resume cycle '+str(index+1),flush=True)
        print(json.dumps(dict(cycles=results,note='Retained compositor frame, not physical UI or FPS'),indent=2))
if __name__=='__main__':main()
