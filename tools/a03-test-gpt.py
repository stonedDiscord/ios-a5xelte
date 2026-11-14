#!/usr/bin/env python3
"""Exercise the actual freestanding GPT parser with synthetic/malformed media."""
import ctypes as C
from pathlib import Path
import struct
import subprocess
import tempfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
SECTORS = 0x0747c000


def main():
    with tempfile.TemporaryDirectory(prefix='a03-gpt-') as tmp:
        src = Path(tmp)/'test.c'
        src.write_text('''#include "gpt-readonly.h"
struct media {const unsigned char *data;unsigned calls,fail;};
static unsigned rd(void *v,uint32_t lba,unsigned char *out) {
 struct media *m=v;m->calls++;
 if(lba<2||lba>=34||m->calls==m->fail)return 0;
 for(unsigned i=0;i<512;i++)out[i]=m->data[(lba-2)*512+i];
 return 1;
}
int check(const unsigned char *header,const unsigned char *data,
 unsigned fail,unsigned *calls,unsigned *computed) {
 struct a03_gpt g;struct media m={data,0,fail};
 if(!a03_gpt_header(header,0x0747c000,&g))return -1;
 unsigned r=a03_gpt_entries(&g,rd,&m,computed);*calls=m.calls;return r;
}
''')
        libpath = Path(tmp)/'test.so'
        subprocess.run(['clang','-shared','-fPIC','-O2','-Wall','-Wextra',
                        '-Werror','-I',str(ROOT/'shim/a03'),str(src),
                        '-o',str(libpath)],check=True)
        check = C.CDLL(str(libpath)).check
        check.argtypes = [C.c_char_p,C.c_char_p,C.c_uint,
                          C.POINTER(C.c_uint),C.POINTER(C.c_uint)]
        check.restype = C.c_int
        entries = bytearray(16384)

        def entry(index,name,start,end):
            off = index*128
            entries[off:off+16] = bytes(range(1,17))
            entries[off+16:off+32] = bytes([index+1])*16
            struct.pack_into('<QQ',entries,off+32,start,end)
            name = (name+'\0').encode('utf-16le')
            entries[off+56:off+56+len(name)] = name

        entry(38,'boot',483328,614399)
        entry(54,'userdata',15929344,SECTORS-34)

        def header(data,count=128):
            h = bytearray(512)
            struct.pack_into('<8sIIIIQQQQ16sQIII',h,0,b'EFI PART',
                             0x10000,92,0,0,1,SECTORS-1,2048,SECTORS-34,
                             bytes(range(16)),2,count,128,
                             zlib.crc32(data[:count*128]))
            struct.pack_into('<I',h,16,zlib.crc32(h[:92]))
            return h

        def run(h,data,expected,fail=0):
            calls,crc = C.c_uint(),C.c_uint()
            result = check(bytes(h),bytes(data),fail,C.byref(calls),C.byref(crc))
            assert result == expected,(result,expected)
            return calls.value,crc.value

        assert run(header(entries),entries,0)==(32,zlib.crc32(entries))
        assert run(header(entries,55),entries,0)==(14,zlib.crc32(entries[:55*128]))
        for fail in (1,16,32):
            assert run(header(entries),entries,1,fail)[0]==fail
        bad = bytearray(entries);bad[1000]^=1
        run(header(entries),bad,4)
        for off,val in ((38*128+32,0),(38*128+40,SECTORS),
                        (54*128+32,483328)):
            bad = bytearray(entries);struct.pack_into('<Q',bad,off,val)
            run(header(bad),bad,2)
        bad = bytearray(entries);struct.pack_into('<Q',bad,38*128+32,483329)
        assert run(header(bad),bad,3)==(32,zlib.crc32(bad))
        # An identity discrepancy must not hide an array-integrity failure.
        h = header(bad);bad[1000]^=1;run(h,bad,4)
        bad = bytearray(entries)
        struct.pack_into('<Q',bad,54*128+40,SECTORS-35)
        assert run(header(bad),bad,0)==(32,zlib.crc32(bad))
        # Device0019 validates a GPT with USERDATA ending before last-usable.
        struct.pack_into('<Q',bad,54*128+40,SECTORS-38)
        assert run(header(bad),bad,0)==(32,zlib.crc32(bad))
        bad = bytearray(entries);bad[54*128+56]=ord('x')
        run(header(bad),bad,5)
        bad = bytearray(entries);bad[38*128:39*128]=bytes(128)
        run(header(bad),bad,5)
        # Header errors with recomputed CRC exercise geometry, not CRC alone.
        for off,fmt,value in ((8,'I',0),(12,'I',513),(20,'I',1),
                              (24,'Q',2),(32,'Q',SECTORS),
                              (48,'Q',SECTORS),(72,'Q',2047),
                              (80,'I',129),(84,'I',256)):
            bad = header(entries);struct.pack_into('<'+fmt,bad,off,value)
            struct.pack_into('<I',bad,16,0)
            struct.pack_into('<I',bad,16,zlib.crc32(bad[:92]))
            run(bad,entries,-1)
        bad = header(entries);bad[16]^=1;run(bad,entries,-1)
        print('PASS: actual C parser; CRC, partial array, read failures, ranges,')
        print('overlaps, PIT identity, missing labels and malformed headers')


if __name__ == '__main__':
    main()
