#!/usr/bin/env python3
"""Package a changed HFS root with an existing A03 kernel; no XNU build or flash."""
import argparse, hashlib, json, subprocess, struct
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('kernel',type=Path);ap.add_argument('root',type=Path)
    ap.add_argument('output',type=Path);ap.add_argument('--adt',type=Path,required=True)
    ap.add_argument('--base',type=Path,default=ROOT/'backup/galaxy-a03-2026-11-13/firmware/magisk-boot.img')
    a=ap.parse_args();payload=a.output.with_suffix('.payload');manifest=a.output.with_suffix('.json')
    for f in [a.output,payload,manifest]:
        if f.exists():ap.error('refusing existing output '+str(f))
    for f in [a.kernel,a.root,a.adt,a.base]:
        if not f.is_file():ap.error('missing input '+str(f))
    data=a.root.read_bytes()
    if len(data)<1536 or data[1024:1026] not in (b'H+',b'HX'):
        ap.error('root must be a raw HFS+/HFSX volume')
    block,count=struct.unpack_from('>II',data,1064)
    if block<512 or block&(block-1) or block*count!=len(data):ap.error('invalid root volume bounds')
    if len(data)>32*1024*1024:ap.error('RAM-root trial limited to 32 MiB; full iOS needs storage')
    args='debug=0x14e serial=3 cpus=1 keepsyms=1 -v -noprogress -enable_kprintf_spam startup_debug=1 -show_pointers rd=md0'
    a.output.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['python3',str(ROOT/'tools/mkpayload.py'),str(a.kernel),str(a.adt),str(payload),'--ramdisk',str(a.root),'--cmdline',args],check=True)
    subprocess.run(['python3',str(ROOT/'tools/a03-xnu-image.py'),str(a.base),str(payload),str(a.output)],check=True)
    sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
    result={'kernel_sha256':sha(a.kernel),'root_sha256':sha(a.root),'boot_sha256':sha(a.output),'cmdline':args}
    with manifest.open('x') as f:json.dump(result,f,indent=2);f.write(chr(10))
    print('Packed existing kernel + HFS root; no phone write:',a.output)
if __name__=='__main__':main()
