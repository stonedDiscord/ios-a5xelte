#!/usr/bin/env python3
"""Test actual RAM-only transport helpers with fake SPI register callbacks."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
SOURCE=r'''
#include <assert.h>
#include <string.h>
#include "shim/a03/jd9365t-memory.h"
struct fake {uint32_t r[32];uint8_t tx[2048];unsigned bytes,rx,cs,delays,fail;};
static uint32_t r32(void*c,unsigned o){struct fake*f=(struct fake*)c;return o==0x28?(f->fail?0:0x300):f->r[o/4];}
static void w32(void*c,unsigned o,uint32_t v){struct fake*f=(struct fake*)c;if(o==8&&!(v&0x100))f->cs++;f->r[o/4]=v;}
static uint8_t r8(void*c,unsigned o){struct fake*f=(struct fake*)c;assert(!o);return (uint8_t)f->rx++;}
static void w8(void*c,unsigned o,uint8_t v){struct fake*f=(struct fake*)c;assert(!o&&f->bytes<sizeof(f->tx));f->tx[f->bytes++]=v;}
static void delay(void*c,unsigned n){((struct fake*)c)->delays+=n;}
int main(void){
 struct fake f;memset(&f,0,sizeof(f));struct a03_jd_bus b={&f,r32,w32,r8,w8,delay};uint8_t data[500];for(unsigned i=0;i<500;i++)data[i]=i;
 assert(!a03_jd_ram_write(&b,0x20002000,data,500));assert(f.bytes==518&&f.cs==3);
 const uint8_t h[]={0xf2,0x20,0,0x20,0,1};assert(!memcmp(f.tx,h,6));assert(!memcmp(f.tx+6,data,240));
 assert(f.tx[246]==0xf2&&f.tx[249]==0x20&&f.tx[250]==0xf0);assert(!memcmp(f.tx+252,data+240,240));
 assert(f.tx[492]==0xf2&&f.tx[495]==0x21&&f.tx[496]==0xe0);assert(!memcmp(f.tx+498,data+480,20));
 memset(&f,0,sizeof(f));memset(data,0,sizeof(data));assert(!a03_jd_ram_read(&b,0x20002000,data,500));assert(f.bytes==18&&f.cs==3&&f.rx==500);for(unsigned i=0;i<500;i++)assert(data[i]==(uint8_t)i);
 unsigned before=f.bytes;
 assert(a03_jd_ram_write(&b,0x40000200,data,1)==-1);assert(a03_jd_ram_write(&b,0x20011000,data,1)==-1);
 assert(a03_jd_ram_write(&b,0xfff0,data,17)==-1);assert(a03_jd_ram_read(&b,0x20011ff0,data,17)==-1);
 assert(a03_jd_ram_write(&b,0xffffffff,data,1)==-1);assert(a03_jd_ram_read(&b,0,data,0)==-1);assert(a03_jd_ram_read(&b,0,NULL,1)==-1);assert(f.bytes==before);
 assert(a03_jd_ram_range(0,65536,1));assert(a03_jd_ram_range(0x20000000,65536,1));assert(a03_jd_ram_range(0x20011000,4096,0));
 assert(!a03_jd_ram_range(0,65537,1));assert(!a03_jd_ram_range(0x20010000,1,0));
 memset(&f,0,sizeof(f));f.fail=1;assert(a03_jd_ram_write(&b,0,data,500)==-1);assert(f.bytes==32&&f.cs==1&&f.delays==10000&&(f.r[2]&0xf00)==0xf00);
}
'''
with tempfile.TemporaryDirectory(prefix='a03-jd-memory-') as d:
 p=Path(d);(p/'test.c').write_text(SOURCE)
 for cc,std,lang in [('clang','c11','c'),('clang++','c++17','c++')]:
  subprocess.run([cc,'-x',lang,'-std='+std,'-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I',str(ROOT),str(p/'test.c'),'-o',str(p/'test')],check=True)
  subprocess.run([str(p/'test')],check=True)
print('PASS actual RAM transport C/C++ ASan/UBSan: exact headers/chunks/CS, read/write data, RAM whitelist/bounds, no peripheral writes, bounded failure')
