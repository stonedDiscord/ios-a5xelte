#!/usr/bin/env python3
"""Decode0192 read-only retirement snapshots without inventing recovery."""
import argparse,json,re
from pathlib import Path
STAGES={1:'Slot retirement or pre-clean AS wait',2:'GPU fault before clean',3:'Stale clean acknowledgement did not clear',4:'GPU fault during clean',5:'Fresh GPU clean completion missing',6:'AS disable completion missing',7:'AS restore completion missing'}
HEX={'irq','mmu','gpu','js','asfault','rawgpu','rawjob','state','next','asstatus','aslo','ashi','cfg'}
def parse(text):
    reports=[]
    for line in text.replace(chr(13),'').splitlines():
        if not line.startswith('A03 GPU retirement: '):continue
        fields=dict(re.findall(r'([a-z-]+)=([0-9a-fA-F]+)',line))
        required={'stage','submitted','done','frame','clock','idle-releases'}|HEX
        if set(fields)!=required:raise ValueError('Incomplete or unexpected retirement snapshot fields')
        values={key:int(value,16 if key in HEX else 10) for key,value in fields.items()}
        if values['stage'] not in STAGES:raise ValueError('Unknown retirement stage')
        values['meaning']=STAGES[values['stage']]
        values['translation_retained']=bool(values['aslo'] or values['ashi'])
        values['note']='Failure evidence only; uncertain DMA remains quarantined until reboot'
        reports.append(values)
    if not reports:raise ValueError('No0192 retirement snapshot; cannot identify failed guard')
    return reports

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('log',type=Path);a=p.parse_args()
    print(json.dumps(parse(a.log.read_text(errors='replace')),indent=2))
if __name__=='__main__':main()
