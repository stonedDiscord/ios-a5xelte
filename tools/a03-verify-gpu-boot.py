#!/usr/bin/env python3
"""Verify autonomous GPU startup evidence in one captured A03 console log.

Requires activation, four full readbacks, then a fast completed frame. Rejects
prior host GPU controls or replays. Does not prove physical UI or cable independence.
"""
import argparse,re
from pathlib import Path

def verify(text):
    text=text.replace(chr(13),'')
    marker='A03 GPU boot: cached warm384 defaultwait; four full readbacks before fast copies'
    if text.count(marker)!=1:raise ValueError('Requires exactly one boot-policy activation')
    start=text.index(marker)
    rows=list(re.finditer(r'A03 GPU blit: pixels=([0-9]+) mismatches=([0-9]+) done=([0-9]+) retired=([0-9]+) verify=([0-9]+) PASS=([0-9]+)',text[start:]))
    good=0;end=None
    for row in rows:
        pixels,mismatch,done,retired,readback,passed=map(int,row.groups())
        if (pixels,mismatch,done,retired,passed)!=(1152000,0,1,1,1):raise ValueError('Failed or non-fullscreen boot copy')
        if readback:good+=1
        elif good<4:raise ValueError('Fast copy preceded four full readbacks')
        else:end=start+row.end();break
    if end is None:raise ValueError('Need four full readbacks followed by a fast copy')
    commands=[line.split(' BEGIN ',1)[1] for line in text[:end].splitlines() if line.startswith('A03 PROBE ') and ' BEGIN ' in line]
    for command in commands:
        if command.startswith('gpu ') and command!='gpu blit':raise ValueError('Host GPU control before autonomous proof: '+command)
        if command.startswith('display replay'):raise ValueError('Replay before autonomous proof')
    return dict(full_readbacks=good,fast_copy=True,prior_host_gpu_mutations=0)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('log',type=Path);a=p.parse_args()
    print(verify(a.log.read_text(errors='replace')))
if __name__=='__main__':main()
