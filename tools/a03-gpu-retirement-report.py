#!/usr/bin/env python3
"""Decode0192 read-only retirement snapshots without inventing recovery."""
import argparse,json,re
from pathlib import Path
STAGES={1:'Slot retirement or pre-clean AS wait',2:'GPU fault before clean',3:'Stale clean acknowledgement did not clear',4:'GPU fault during clean',5:'Fresh GPU clean completion missing',6:'AS disable completion missing',7:'AS restore completion missing'}
HEX={'irq','mmu','gpu','js','asfault','rawgpu','rawjob','state','next','asstatus','aslo','ashi','cfg'}
POWER={'status','shader','l2','tiler','shadertrans','l2trans','tilertrans'}
SUMMARY={'stage','submitted','done','frame','clock','idle-releases'}
PARTS={'regs':{'irq','mmu','gpu','js','asfault','rawgpu','rawjob','state','next'},
       'as':{'asstatus','aslo','ashi','cfg'},'power':POWER}
def parse(text):
    reports=[];pending=None;seen=set()
    def decode(fields):
        values={key:int(value,16 if key in HEX|POWER else 10) for key,value in fields.items()}
        if values['stage'] not in STAGES:raise ValueError('Unknown retirement stage')
        values['meaning']=STAGES[values['stage']]
        values['translation_retained']=bool(values['aslo'] or values['ashi'])
        values['note']='Failure evidence only; uncertain DMA remains quarantined until reboot'
        return values
    for line in text.replace(chr(13),'').splitlines():
        match=re.fullmatch(r'A03 GPU retirement(?::|-(regs|as|power):) (.*)',line)
        if not match:continue
        pairs=re.findall(r'([a-z][a-z0-9-]*)=([0-9a-fA-F]+)',match[2]);fields=dict(pairs)
        if len(pairs)!=len(fields) or ' '.join(k+'='+v for k,v in pairs)!=match[2]:
            raise ValueError('Malformed retirement snapshot fields')
        part=match[1]
        if part is None:
            if pending is not None:raise ValueError('Incomplete retirement snapshot')
            if set(fields)==SUMMARY|HEX:reports.append(decode(fields))
            elif set(fields)==SUMMARY:pending=fields;seen=set()
            else:raise ValueError('Incomplete or unexpected retirement snapshot fields')
        else:
            if pending is None or part in seen or set(fields)!=PARTS[part]:
                raise ValueError('Unexpected retirement snapshot part')
            pending.update(fields);seen.add(part)
            if seen==set(PARTS):reports.append(decode(pending));pending=None
    if pending is not None:raise ValueError('Incomplete retirement snapshot')
    if not reports:raise ValueError('No retirement snapshot; cannot identify failed guard')
    return reports

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('log',type=Path);a=p.parse_args()
    print(json.dumps(parse(a.log.read_text(errors='replace')),indent=2))
if __name__=='__main__':main()
