#!/usr/bin/env python3
"""Install verified iOS root through the A03's USERDATA-only Linux USB LUN.

No whole-card access. Refuses wrong USB identity/capacity, mounted devices,
source hash mismatch and read-only target. Full readback hash is mandatory.
"""
import argparse
import fcntl
import hashlib
import json
import mmap
import os
from pathlib import Path
import stat
import struct
import time

ROOT_SHA='eb72c14a9cf4aab30a8b49afda745a1b342dc877263d3b6a39901d95c89da108'
ROOT_BYTES=16<<30
PART_BYTES=54381228032
SERIAL='A03LinuxInstallV11'
TARGET='/dev/disk/by-id/usb-Linux_File-Stor_Gadget_'+SERIAL+'-0:1'

def digest(fd,length):
    h=hashlib.sha256();offset=0
    while offset<length:
        chunk=os.pread(fd,min(8<<20,length-offset),offset)
        if not chunk:raise ValueError('short read at '+str(offset))
        h.update(chunk);offset+=len(chunk)
    return h.hexdigest()

def direct_digest(fd,length):
    flags=fcntl.fcntl(fd,fcntl.F_GETFL)
    fcntl.fcntl(fd,fcntl.F_SETFL,flags|os.O_DIRECT)
    h=hashlib.sha256();offset=0;buf=mmap.mmap(-1,8<<20)
    try:
        while offset<length:
            take=min(len(buf),length-offset)
            view=memoryview(buf)[:take]
            try:
                n=os.preadv(fd,[view],offset)
                if n!=take:raise ValueError('short direct read at '+str(offset))
                h.update(view)
            finally:view.release()
            offset+=take
            if offset%(512<<20)==0:print(f'READBACK {offset//(1<<20)}/16384 MiB',flush=True)
    finally:
        buf.close();fcntl.fcntl(fd,fcntl.F_SETFL,flags)
    return h.hexdigest()

def identity(path,writing):
    resolved=path.resolve(strict=True)
    st=resolved.stat()
    if not stat.S_ISBLK(st.st_mode):raise ValueError('target must be a block device')
    sys=Path('/sys/dev/block')/f'{os.major(st.st_rdev)}:{os.minor(st.st_rdev)}'
    real=sys.resolve(strict=True)
    if '/usb' not in str(real) or real.joinpath('device/model').read_text().strip()!='File-Stor Gadget':
        raise ValueError('target is not a USB file-storage LUN')
    if not real.joinpath('device').resolve().name.endswith(':1'):raise ValueError('target is not LUN1')
    usb=next((p for p in real.parents if (p/'idVendor').exists()),None)
    if usb is None or (usb/'idVendor').read_text().strip()!='1d6b' or (usb/'idProduct').read_text().strip()!='0104' or (usb/'serial').read_text().strip()!=SERIAL:
        raise ValueError('wrong USB vendor/product/serial')
    if int(real.joinpath('size').read_text())*512!=PART_BYTES:raise ValueError('wrong validated USERDATA capacity')
    if writing and real.joinpath('ro').read_text().strip()!='0':raise ValueError('target is read-only')
    for line in Path('/proc/self/mountinfo').read_text().splitlines():
        if line.split()[2]==f'{os.major(st.st_rdev)}:{os.minor(st.st_rdev)}':raise ValueError('target is mounted')
    if any(real.glob(resolved.name+'[0-9]*')):raise ValueError('unexpected nested partitions')
    return resolved,st.st_rdev

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('image',type=Path)
    ap.add_argument('--target',type=Path,default=Path(TARGET))
    ap.add_argument('--write',action='store_true',help='authorized write of exactly16GiB to validated USERDATA LUN')
    a=ap.parse_args()
    if a.image.stat().st_size!=ROOT_BYTES:ap.error('requires exact16GiB source')
    src=os.open(a.image,os.O_RDONLY)
    actual=digest(src,ROOT_BYTES)
    if actual!=ROOT_SHA:raise ValueError('source SHA256 mismatch: '+actual)
    target,rdev=identity(a.target,a.write)
    fd=os.open(target,(os.O_RDWR if a.write else os.O_RDONLY)|os.O_CLOEXEC|os.O_EXCL)
    if os.fstat(fd).st_rdev!=rdev:raise ValueError('target changed during open')
    block_bytes=struct.unpack('Q',fcntl.ioctl(fd,0x80081272,bytes(8)))[0]
    if block_bytes!=PART_BYTES:raise ValueError('kernel capacity mismatch')
    source_header=os.pread(src,512,1024)
    target_header=os.pread(fd,512,1024)
    if source_header[:4]!=b'HX'+bytes((0,5)) or target_header[:4]!=source_header[:4]:
        raise ValueError('expected installed HFSX header missing')
    if source_header[40:48]!=target_header[40:48]:raise ValueError('HFS allocation geometry mismatch')
    print(json.dumps({'target' :str(target),'partition_bytes':block_bytes,'source_sha256':actual,'write':a.write}),flush=True)
    if a.write:
        start=time.monotonic();offset=0
        while offset<ROOT_BYTES:
            chunk=os.pread(src,min(4<<20,ROOT_BYTES-offset),offset)
            if not chunk:raise ValueError('source short read')
            done=0
            while done<len(chunk):
                n=os.pwrite(fd,chunk[done:],offset+done)
                if n<=0:raise ValueError('target short write')
                done+=n
            offset+=len(chunk)
            if offset%(256<<20)==0:print(f'WRITE {offset//(1<<20)}/16384 MiB elapsed={time.monotonic()-start:.1f}s',flush=True)
        os.fsync(fd)
        # Aligned O_DIRECT reads bypass host cache without privileged BLKFLSBUF.
        actual=direct_digest(fd,ROOT_BYTES)
        if actual!=ROOT_SHA:raise ValueError('DEVICE READBACK SHA256 MISMATCH: '+actual)
        print('FULL DEVICE READBACK PASS '+actual,flush=True)
    print('CATALOG_HEADER '+os.pread(fd,32,0x2cd82000).hex(),flush=True)
    print('CATALOG_ROOT '+os.pread(fd,32,0x2cfa6000).hex(),flush=True)
    os.close(fd);os.close(src)

if __name__=='__main__':main()
