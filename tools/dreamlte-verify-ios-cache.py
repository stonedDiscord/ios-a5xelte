#!/usr/bin/env python3
"""Check iOS16 plain-arm64 cache's declared parts/UUIDs and core dylib paths.
Read-only; supports an extracted root or raw HFS image. Does not verify
cryptographic signatures, file payload hashes, or runtime compatibility.
Format fields follow Apple's dyld_cache_format.h (dyld_cache_header and
56-byte dyld_subcache_entry with fileSuffix), as used by supplied20A362.
"""
import argparse,importlib.util,json,struct
from pathlib import Path

CACHE='/System/Library/Caches/com.apple.dyld/dyld_shared_cache_arm64'
REQUIRED={'/usr/lib/libSystem.B.dylib','/usr/lib/libobjc.A.dylib',
          '/System/Library/PrivateFrameworks/SpringBoard.framework/SpringBoard',
          '/System/Library/Frameworks/Foundation.framework/Foundation'}

class Directory:
    def __init__(self,root):self.root=root
    def size(self,name):return (self.root/name.lstrip('/')).stat().st_size
    def read(self,name,off,n):
        with (self.root/name.lstrip('/')).open('rb') as f:f.seek(off);return f.read(n)

class Image:
    def __init__(self,path):
        spec=importlib.util.spec_from_file_location('hfs_reader',Path(__file__).with_name('herolte-hfs-read.py'))
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        class Local:
            def __init__(self,path):self.f=path.open('rb')
            def read(self,off,n):self.f.seek(off);return self.f.read(n)
        self.fs=m.HFS(Local(path));self.cat=m.Catalog(self.fs);self.info=m.file_info;self.files={}
    def file(self,name):
        if name not in self.files:
            _,rec=self.cat.lookup(name);self.files[name]=self.info(rec)
        return self.files[name]
    def size(self,name):return self.file(name)[2][0]
    def read(self,name,off,n):
        fid,_,fork=self.file(name);return self.fs.fork_read(fork,off,n,fid)

def verify(access):
    def header(name,uuid=None):
        h=access.read(name,0,512);size=access.size(name)
        if len(h)!=512 or h[:16].rstrip(b'\0 ')!=b'dyld_v1   arm64':
            raise ValueError('bad plain-arm64 cache header: '+name)
        if uuid is not None and h[88:104]!=uuid:raise ValueError('cache UUID mismatch: '+name)
        off,count=struct.unpack_from('<II',h,16)
        sig,length=struct.unpack_from('<QQ',h,40)
        if off<460 or off>4096 or not 0<count<=32 or off+count*32>size:
            raise ValueError('unsupported/truncated cache mappings: '+name)
        if not length or sig>size or length>size-sig:raise ValueError('invalid signature extent: '+name)
        data=access.read(name,off,count*32)
        if len(data)!=count*32:raise ValueError('short mapping table: '+name)
        for i in range(count):
            _,n,f,_,_=struct.unpack_from('<QQQII',data,i*32)
            if f>size or n>size-f:raise ValueError('mapping outside cache file: '+name)
        return h
    h=header(CACHE);off,count=struct.unpack_from('<II',h,392)
    if not 0<count<=128 or off+56*count>access.size(CACHE):raise ValueError('invalid subcache array')
    entries=access.read(CACHE,off,56*count)
    if len(entries)!=56*count:raise ValueError('short subcache array')
    parts=[];seen=set()
    for i in range(count):
        uuid,vm,suffix=struct.unpack_from('<16sQ32s',entries,i*56)
        if b'\0' not in suffix:raise ValueError('unterminated subcache suffix')
        suffix=suffix.split(b'\0')[0].decode('ascii')
        if not suffix.startswith('.') or '/' in suffix or '..' in suffix or suffix in seen:
            raise ValueError('unsafe/duplicate subcache suffix')
        seen.add(suffix);name=CACHE+suffix;header(name,uuid)
        parts.append({'suffix':suffix,'bytes':access.size(name),'uuid':uuid.hex(),'vm_offset':vm})
    symbols=h[400:416]
    if any(symbols):header(CACHE+'.symbols',symbols)
    off,count=struct.unpack_from('<II',h,448)
    if not 0<count<100000 or off+32*count>access.size(CACHE):raise ValueError('invalid image table')
    entries=access.read(CACHE,off,32*count);paths=set()
    for i in range(count):
        pathoff,=struct.unpack_from('<I',entries,i*32+24)
        if pathoff>=access.size(CACHE):raise ValueError('image path outside primary cache')
        path=access.read(CACHE,pathoff,min(4096,access.size(CACHE)-pathoff))
        if b'\0' not in path:raise ValueError('unterminated image path')
        paths.add(path.split(b'\0')[0].decode())
    missing=REQUIRED-paths
    if missing:raise ValueError('core dependencies missing: '+str(sorted(missing)))
    return {'subcaches':parts,'subcache_count':len(parts),'image_count':count,
            'core_dependencies':sorted(REQUIRED),'symbol_uuid_checked':bool(any(symbols)),
            'scope':'declared files/UUIDs/mapping bounds/dependency names; no signature or runtime proof'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path)
    p.add_argument('--hfs-image',action='store_true');a=p.parse_args()
    try:result=verify(Image(a.root) if a.hfs_image else Directory(a.root))
    except (OSError,ValueError,struct.error,AssertionError) as e:p.exit(1,str(e)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
