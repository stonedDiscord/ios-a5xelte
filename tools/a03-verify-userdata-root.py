#!/usr/bin/env python3
"""Verify raw16GiB journaled HFSX image geometry/hash before USERDATA install.
Read-only host operation. Does not replace fsck or validate runtime bootability.
"""
import argparse,hashlib,json,struct
from pathlib import Path


def inspect(path,expected):
    size=path.stat().st_size
    if size!=16<<30:
        raise ValueError('expected exact16GiB raw filesystem (no partition table)')
    with path.open('rb') as f:
        f.seek(1024);h=f.read(512)
        f.seek(size-1024);alt=f.read(512)
        for index,header in enumerate((h,alt)):
            if header[:4]!=b'HX\x00\x05':
                raise ValueError('missing HFSX version5 primary/alternate header')
            attrs,=struct.unpack_from('>I',header,4)
            block,count=struct.unpack_from('>II',header,40)
            journal,=struct.unpack_from('>I',header,12)
            if block<512 or block&(block-1) or block*count!=size:
                raise ValueError('invalid allocation geometry')
            if not attrs&(1<<13) or not 0<journal<count:
                raise ValueError('requires journaled filesystem')
            # Alternate headers need not be rewritten on every unmount. The
            # primary header carries the authoritative clean-unmount bit.
            if index==0 and not attrs&(1<<8):
                raise ValueError('requires cleanly unmounted primary volume header')
        if h[12:16]!=alt[12:16]:
            raise ValueError('primary/alternate journal location mismatch')
        if h[40:48]!=alt[40:48]:
            raise ValueError('primary/alternate geometry mismatch')
        digest=hashlib.sha256();f.seek(0)
        for chunk in iter(lambda:f.read(8<<20),b''):digest.update(chunk)
    actual=digest.hexdigest()
    if actual!=expected.lower():
        raise ValueError('filesystem SHA256 mismatch')
    return {'path':str(path),'bytes':size,'sha256':actual,
            'filesystem':'HFSX','journaled':True,'clean_unmount':True,
            'scope':'geometry/hash only; require clean fsck and iOS file inventory separately'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('image',type=Path);p.add_argument('--sha256',required=True)
    a=p.parse_args()
    try:result=inspect(a.image,a.sha256)
    except (OSError,ValueError,struct.error) as e:p.exit(1,str(e)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
