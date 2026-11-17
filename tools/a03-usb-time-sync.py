#!/usr/bin/env python3
"""Explicitly sync A03 volatile UTC from host; requires0150 and live capture."""
import argparse,re,time
from pathlib import Path
from a03_usb_probe import Probe

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--log',type=Path,required=True,help='existing single-reader console log')
    ap.add_argument('--status',action='store_true',help='read current UTC without changing it')
    args=ap.parse_args()
    with args.log.open('rb') as log,Probe() as probe:
        log.seek(0,2)
        sent=int(time.time())
        if not 1577836800<=sent<=4102444799:ap.error('host UTC outside2020..2099')
        command='time status' if args.status else 'time '+str(sent)
        probe.send(command)
        block=b'';deadline=time.monotonic()+15
        while time.monotonic()<deadline:
            block+=log.read()
            begin=re.search(rb'A03 PROBE (\d+) BEGIN '+re.escape(command.encode())+rb'\r?\n',block)
            if begin:
                end=re.search(rb'A03 PROBE '+begin[1]+rb' END\r?\n',block[begin.end():])
                if end:
                    result=block[begin.end():begin.end()+end.start()]
                    value=re.search(rb'A03 PROBE time UTC=(\d+) usec=(\d+)',result)
                    if not value:raise RuntimeError('UTC command failed: '+result.decode(errors='replace'))
                    utc=int(value[1])
                    if not args.status and abs(utc-sent)>15:raise RuntimeError('UTC readback differs from host')
                    print('Device UTC '+str(utc)+' = '+time.strftime('%Y-%m-%d %H:%M:%S UTC',time.gmtime(utc)))
                    print('Volatile sync only; display timezone and persistence are not verified.')
                    return
            time.sleep(.01)
        raise RuntimeError('missing UTC command acknowledgement; no retry sent')

if __name__=='__main__':main()
