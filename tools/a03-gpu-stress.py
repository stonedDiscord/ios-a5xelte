#!/usr/bin/env python3
"""Stress copies of a retained compositor frame; not a physical UI/FPS test.

Uses one existing console reader, never injects input, and restores mode.
Requires four existing full readbacks. Ends with four new full readbacks.
No cache/rate/poll/power policy changes. Each replay is bounded to eight copies.
"""
import argparse,importlib.util,json,sys,time
from pathlib import Path
from a03_usb_probe import Probe
spec=importlib.util.spec_from_file_location('blit',Path(__file__).with_name('a03-gpu-blit-benchmark.py'))
blit=importlib.util.module_from_spec(spec);spec.loader.exec_module(blit)
POLICIES=['cached','warm','tile_rows','memattr','clock_mhz','poll_spin']
def validate(before,after,minimum,verify):
    if any(before.get(k)!=after.get(k) for k in POLICIES):raise RuntimeError('Stress policy changed')
    if after['quarantined'] or after['fallbacks']!=before['fallbacks']:raise RuntimeError('Stress fault/fallback')
    if after['completed']-before['completed']<minimum:raise RuntimeError('Stress completion shortfall')
    if verify and after['verified']-before['verified']<minimum:raise RuntimeError('Stress readback shortfall')
    if not verify and after['verified']!=before['verified']:raise RuntimeError('Stress unexpectedly included readback')
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--log',type=Path,required=True)
    p.add_argument('--batches',type=int,default=64);a=p.parse_args()
    if not 1<=a.batches<=256:p.error('batches must be1..256')
    with a.log.open('rb') as log,Probe() as probe:
        original=blit.snapshot(probe,log)
        if original['quarantined'] or original['verified']<4:raise RuntimeError('Requires healthy four-frame qualification')
        try:
            blit.command(probe,log,'gpu blit fast');blit.command(probe,log,'gpu blit on')
            before=blit.snapshot(probe,log)
            if not before['enabled'] or before['verify']:raise RuntimeError('Fast mode did not take effect')
            for i in range(a.batches):
                blit.replay(probe,log,8)
                if (i+1)%8==0:print('Completed batches '+str(i+1)+'/'+str(a.batches),flush=True)
                time.sleep(.02)
            after=blit.snapshot(probe,log);validate(before,after,a.batches*8,False)
            result=blit.report(before,after,'fast')
            blit.command(probe,log,'gpu blit verify');qbefore=blit.snapshot(probe,log)
            blit.replay(probe,log,4);qafter=blit.snapshot(probe,log);validate(qbefore,qafter,4,True)
            result['final_full_readbacks']=qafter['verified']-qbefore['verified']
            print(json.dumps(result,indent=2),flush=True)
        finally:
            blit.command(probe,log,'gpu blit off')
            blit.command(probe,log,'gpu blit '+('verify' if original['verify'] else 'fast'))
            blit.command(probe,log,'gpu blit '+('on' if original['enabled'] else 'off'))
            restored=blit.snapshot(probe,log)
            if any(restored.get(k)!=original.get(k) for k in POLICIES+['enabled','verify']):
                raise RuntimeError('Stress original policy restoration not confirmed')
            print('Original GPU mode restored.',flush=True)
if __name__=='__main__':main()
