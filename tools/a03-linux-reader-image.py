#!/usr/bin/env python3
"""Build BOOT-only Linux USERDATA reader; matching stock kernel/DT unchanged."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[1]
BASE_SHA='94fa7c5347b00e49fe1dc60a4edae958ddd5dac9accdbcddbeb743b5215e9ce7'
def cpio(files):
    out=bytearray()
    for ino,(name,mode,data) in enumerate(files+[('TRAILER!!!',0,b'')],1):
        name=name.encode()+bytes(1)
        fields=(ino,mode,0,0,1,0,len(data),0,0,0,0,len(name),0)
        out+=b'070701'+''.join(f'{v:08x}' for v in fields).encode()+name
        out+=bytes(-len(out)%4);out+=data;out+=bytes(-len(out)%4)
    return bytes(out)
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output',type=Path)
    ap.add_argument('--base',type=Path,default=ROOT/'backup/galaxy-a03-2026-11-13/firmware/magisk-boot.img')
    a=ap.parse_args()
    if a.output.exists():ap.error('refusing existing output')
    b=a.base.read_bytes()
    if hashlib.sha256(b).hexdigest()!=BASE_SHA:ap.error('wrong verified A03 base')
    ks,_,old_rs,_,ss,_,_,page,version=struct.unpack_from('<9I',b,8)
    assert b[:8]==b'ANDROID!' and page==2048 and version==2 and ss==0
    align=lambda n:(n+page-1)//page*page
    ds=struct.unpack_from('<I',b,1648)[0]
    assert struct.unpack_from('<IQ',b,1632)==(0,0)
    kernel=b[page:page+ks];dt_off=page+align(ks)+align(old_rs);dt=b[dt_off:dt_off+ds]
    with tempfile.TemporaryDirectory(prefix='a03-linux-reader-') as temp:
        binary=Path(temp)/'init'
        subprocess.run(['aarch64-linux-gnu-gcc','-static','-Os','-Wall','-Wextra','-Werror',
                        str(ROOT/'tools/a03-linux-reader-init.c'),'-o',str(binary)],check=True)
        ramdisk=cpio([(n,0o40755,b'') for n in ('dev','proc','sys','config','run')]+[('init',0o100755,binary.read_bytes())])
    out=bytearray(b[:page]);struct.pack_into('<I',out,16,len(ramdisk));digest=hashlib.sha1()
    for part in (kernel,ramdisk,b'',b'',dt):
        digest.update(part);digest.update(struct.pack('<I',len(part)))
    out[576:608]=digest.digest()+bytes(12)
    for part in (kernel,ramdisk,dt):out+=part+bytes(align(len(part))-len(part))
    out+=b'SEANDROIDENFORCE'+bytes(1);original_size=len(out)
    magic,major,minor,_,vo,vs=struct.unpack_from('>4sIIQQQ',b,len(b)-64)
    assert magic==b'AVBf' and vo+vs<=len(b)-64
    out+=bytes(-len(out)%4096);new_vo=len(out);out+=b[vo:vo+vs]
    assert len(out)<=len(b)-64
    out+=bytes(len(b)-64-len(out));out+=struct.pack('>4sIIQQQ',magic,major,minor,original_size,new_vo,vs)+bytes(28)
    assert len(out)==len(b)==67108864 and out[page:page+ks]==kernel
    new_dt=page+align(ks)+align(len(ramdisk));assert out[new_dt:new_dt+ds]==dt
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(out)
    print('BOOT-only Linux reader:',a.output)
    print('kernel SHA256',hashlib.sha256(kernel).hexdigest())
    print('BOOT SHA256',hashlib.sha256(out).hexdigest())
    print('USERDATA is unmounted and exported read-only; no Android init.')
if __name__=='__main__':main()
