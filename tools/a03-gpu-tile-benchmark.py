#!/usr/bin/env python3
"""Qualify and compare explicit fullscreen dispatch policies on one live boot.

Uses an existing sole console reader. Does not flash, reset, change cache or
power policy, or inject input. Each tile earns four full readbacks before the
paired fast/CPU comparison. Restores the original tile and enable/readback mode.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from a03_usb_probe import Probe
spec=importlib.util.spec_from_file_location('blit',ROOT/'a03-gpu-blit-benchmark.py')
blit=importlib.util.module_from_spec(spec);spec.loader.exec_module(blit)


def paired_result(output):
    decoder=json.JSONDecoder()
    for pos,char in enumerate(output):
        if char!='{':continue
        try:value,_=decoder.raw_decode(output[pos:])
        except ValueError:continue
        if isinstance(value,dict) and 'cpu_median_ms' in value and 'samples' in value:
            return value
    raise RuntimeError('Paired comparison did not report complete results')


def qualified(before,after,tile):
    if before.get('tile_rows')!=tile or after.get('tile_rows')!=tile:
        raise RuntimeError('Dispatch tile did not take effect')
    if not before['enabled'] or not before['verify'] or not after['enabled'] or not after['verify']:
        raise RuntimeError('Qualification requires enabled full readback')
    if after['quarantined'] or after['fallbacks']!=before['fallbacks']:
        raise RuntimeError('Fault or fallback during tile qualification')
    if after['verified']-before['verified']<4 or after['completed']-before['completed']<4:
        raise RuntimeError('Tile did not earn four fresh readbacks')
    for key in ['cached','warm','memattr','clock_mhz','poll_spin']:
        if before.get(key)!=after.get(key):raise RuntimeError('Policy changed during qualification')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--log',type=Path,required=True)
    p.add_argument('--tiles',type=int,nargs='+',choices=[4,8,16,32],default=[4,8,16,32])
    p.add_argument('--rounds',type=int,choices=range(2,7),default=3)
    a=p.parse_args();results=[]
    with a.log.open('rb') as log,Probe() as probe:
        original=blit.snapshot(probe,log)
        if original['quarantined'] or original.get('tile_rows') not in [4,8,16,32]:
            raise RuntimeError('Requires healthy0182 dispatch status')
        try:
            for tile in a.tiles:
                blit.command(probe,log,'gpu blit off')
                blit.command(probe,log,'gpu blit tile'+str(tile))
                blit.command(probe,log,'gpu blit verify')
                blit.command(probe,log,'gpu blit on')
                before=blit.snapshot(probe,log)
                blit.replay(probe,log,4)
                after=blit.snapshot(probe,log);qualified(before,after,tile)
                # Pair children restore OFF, avoiding expensive background
                # readbacks racing the next status/control transaction.
                blit.command(probe,log,'gpu blit off')
                if blit.snapshot(probe,log)['enabled']:
                    raise RuntimeError('GPU OFF did not take effect before paired trial')
                run=subprocess.run([sys.executable,str(ROOT/'a03-gpu-paired-benchmark.py'),
                    '--log',str(a.log),'--rounds',str(a.rounds),'--replay','8'],capture_output=True,text=True)
                print(run.stdout,end='',flush=True)
                if run.returncode:raise RuntimeError(run.stderr or 'Paired benchmark failed')
                result=paired_result(run.stdout)
                if len(result['samples'])!=a.rounds*2 or any(s.get('tile_rows')!=tile for s in result['samples']):
                    raise RuntimeError('Incomplete or mixed tile comparison')
                result['tile_rows']=tile;results.append(result)
                print('Qualified tile'+str(tile)+' paired comparison complete.',flush=True)
        finally:
            blit.command(probe,log,'gpu blit off')
            blit.command(probe,log,'gpu blit tile'+str(original['tile_rows']))
            blit.command(probe,log,'gpu blit '+('verify' if original['verify'] else 'fast'))
            blit.command(probe,log,'gpu blit '+('on' if original['enabled'] else 'off'))
            restored=blit.snapshot(probe,log)
            if any(restored.get(k)!=original.get(k) for k in ['enabled','verify','tile_rows','cached','warm','memattr','clock_mhz','poll_spin']):
                raise RuntimeError('Original tile/mode restoration not confirmed; inspect live status')
            print('Original dispatch tile and GPU mode restored.',flush=True)
    print(json.dumps(dict(note='Accepted-frame synchronous copy latency, not physical FPS',tiles=results),indent=2))


if __name__=='__main__':main()
