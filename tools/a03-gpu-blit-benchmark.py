#!/usr/bin/env python3
"""Measure actual framebuffer copy deltas from an existing single console log.

Requires0169. Does not flash, reset, inject input, stop touch or open the tty.
Mode changes are explicit, bounded, and restored in finally. Generate real UI
activity during the interval; a zero-frame sample is inconclusive.
"""
import argparse,json,re,time
from pathlib import Path
from a03_usb_probe import Probe


def command(probe,log,cmd,timeout=25):
    log.seek(0,2);probe.send(cmd);data=b'';deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
        data+=log.read();clean=data.replace(bytes([13]),b'')
        begin=re.search(rb'A03 PROBE ([0-9]+) BEGIN '+re.escape(cmd.encode())+bytes([10]),clean)
        if begin:
            end=re.search(rb'A03 PROBE '+begin[1]+rb' END'+bytes([10]),clean[begin.end():])
            if end:return clean[begin.end():begin.end()+end.start()].decode(errors='replace')
        time.sleep(.02)
    raise RuntimeError('No exact completion for '+cmd+'; command not resent')


def snapshot(probe,log):
    gpu=command(probe,log,'gpu blit');display=command(probe,log,'display')
    fields=re.search(r'enabled=([0-9]+) frames=([0-9]+) pixels=([0-9]+) fallbacks=([0-9]+) quarantined=([0-9]+)',gpu)
    policy=re.search(r'verify=([0-9]+) verified=([0-9]+) completed=([0-9]+) total-ns=([0-9]+) last-ns=([0-9]+)',gpu)
    timing=re.search(r'copy timing cpu=([0-9]+)/([0-9]+)ns gpu=([0-9]+)/([0-9]+)ns',display)
    if not(fields and policy and timing):raise RuntimeError('Missing0169 counters or GPU busy; no measurement')
    keys=['enabled','frames','pixels','fallbacks','quarantined','verify','verified','completed','total_ns','last_ns','cpu_copies','cpu_ns','gpu_copies','gpu_ns']
    return dict(zip(keys,map(int,fields.groups()+policy.groups()+timing.groups())))


def report(before,after,mode):
    delta={k:after[k]-before[k] for k in ['frames','pixels','fallbacks','verified','completed','cpu_copies','cpu_ns','gpu_copies','gpu_ns']}
    for k,v in delta.items():
        if v<0:raise RuntimeError('Counter reset/wrap in '+k+'; discard interval')
    n=delta['cpu_copies'] if mode=='cpu' else delta['gpu_copies']
    elapsed=delta['cpu_ns'] if mode=='cpu' else delta['gpu_ns']
    delta.update(mode=mode,mean_copy_ms=elapsed/n/1000000 if n else None,quarantined=after['quarantined'])
    if not n:delta['result']='inconclusive: no actual frame copies'
    elif after['quarantined']:delta['result']='failed: GPU quarantined'
    elif mode=='fast' and delta['verified']:delta['result']='mixed: initial verification included; repeat after warmup'
    else:delta['result']='measured actual copies; elapsed time includes scheduling, cache and completion overhead'
    return delta


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--log',type=Path,required=True)
    p.add_argument('--mode',choices=['cpu','verify','fast'],required=True)
    p.add_argument('--seconds',type=float,default=15);a=p.parse_args()
    if not 1<=a.seconds<=60:p.error('--seconds must be1..60')
    with a.log.open('rb') as log,Probe() as probe:
        original=snapshot(probe,log)
        if original['quarantined']:raise RuntimeError('GPU quarantined; no mode change')
        try:
            if a.mode=='cpu':command(probe,log,'gpu blit off')
            else:
                command(probe,log,'gpu blit '+a.mode);command(probe,log,'gpu blit on')
            before=snapshot(probe,log)
            if before['enabled']!=(a.mode!='cpu'):raise RuntimeError('Mode did not take effect')
            if a.mode!='cpu' and before['verify']!=(a.mode=='verify'):raise RuntimeError('Verification policy did not take effect')
            print('Measuring '+a.mode+' for '+str(a.seconds)+' seconds; use the phone now.',flush=True)
            time.sleep(a.seconds)
            after=snapshot(probe,log);print(json.dumps(report(before,after,a.mode),indent=2),flush=True)
        finally:
            command(probe,log,'gpu blit '+('verify' if original['verify'] else 'fast'))
            command(probe,log,'gpu blit '+('on' if original['enabled'] else 'off'))
            restored=snapshot(probe,log)
            if restored['enabled']!=original['enabled'] or restored['verify']!=original['verify']:raise RuntimeError('Mode restoration not confirmed; inspect gpu blit status')
            print('Original GPU mode restored.',flush=True)


if __name__=='__main__':main()
