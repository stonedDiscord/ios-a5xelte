#!/usr/bin/env python3
"""Package a changed HFS root with an existing A03 kernel; no XNU build or flash."""
import argparse, hashlib, json, subprocess, struct
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('kernel',type=Path);ap.add_argument('root',type=Path)
    ap.add_argument('output',type=Path);ap.add_argument('--adt',type=Path,required=True)
    ap.add_argument('--emmc-readonly',action='store_true',help='opt-in XNU read-only SDMA probe; requires matching ADT node')
    ap.add_argument('--userdata-writable',action='store_true',help='enable USERDATA-only writes; requires --emmc-readonly controller opt-in')
    ap.add_argument('--userdata-root',action='store_true',help='select validated USERDATA HFS root; requires --userdata-writable and kernel root-selection patch; positional root remains small RAM fallback')
    ap.add_argument('--catalog-probe',action='store_true',help='keep RAM HFS root while enabling A03 eMMC for PID1 catalog reads')
    ap.add_argument('--usb-probe',action='store_true',help='print read-only A03 MUSB controller state from XNU')
    ap.add_argument('--emmc-trace',action='store_true',help='print selected high-LBA eMMC reads from XNU')
    ap.add_argument('--base',type=Path,default=ROOT/'backup/galaxy-a03-2026-11-13/firmware/magisk-boot.img')
    a=ap.parse_args();payload=a.output.with_suffix('.payload');manifest=a.output.with_suffix('.json')
    if a.userdata_writable and not a.emmc_readonly:
        ap.error('--userdata-writable requires --emmc-readonly controller opt-in')
    if a.userdata_root and not a.userdata_writable:
        ap.error('--userdata-root requires --userdata-writable')
    if a.catalog_probe and not a.emmc_readonly:
        ap.error('--catalog-probe requires --emmc-readonly')
    if a.emmc_trace and not a.emmc_readonly:
        ap.error('--emmc-trace requires --emmc-readonly')
    if a.catalog_probe and a.userdata_root:
        ap.error('--catalog-probe is a RAM-root diagnostic; do not combine with --userdata-root')
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
    if a.usb_probe:args+=' a03usb_probe=1'
    if a.emmc_trace:args+=' a03emmc_trace=1'
    if a.emmc_readonly:
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        import adt
        tree,end=adt.parse(a.adt.read_bytes())
        nodes=[n for n in tree.children if n.name=='a03-emmc']
        if end!=a.adt.stat().st_size or len(nodes)!=1 or nodes[0].prop('reg')!=struct.pack('<QQ',0x201d0000,0x1000):
            ap.error('--emmc-readonly requires an A03 ADT with the exact controller window')
        args+=' a03emmc=1'
        if a.userdata_writable:args+=' a03emmc_rw=1'
    if a.userdata_root:
        args=args.replace('rd=md0','rd=a03userdata0')+' rootrw=1 a03_unsealed_root=1 ignition_level=1 -nobsdmgroot'
    a.output.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['python3',str(ROOT/'tools/mkpayload.py'),str(a.kernel),str(a.adt),str(payload),'--ramdisk',str(a.root),'--cmdline',args],check=True)
    subprocess.run(['python3',str(ROOT/'tools/a03-xnu-image.py'),str(a.base),str(payload),str(a.output)],check=True)
    sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
    result={'kernel_sha256':sha(a.kernel),'root_sha256':sha(a.root),'boot_sha256':sha(a.output),'cmdline':args}
    with manifest.open('x') as f:json.dump(result,f,indent=2);f.write(chr(10))
    print('Packed existing kernel + HFS root; no phone write:',a.output)
if __name__=='__main__':main()
