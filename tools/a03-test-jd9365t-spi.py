#!/usr/bin/env python3
"""Run actual bounded SPI/protocol helpers under host ASan/UBSan."""
from pathlib import Path
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[1]
SRC=r'''
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "shim/a03/jd9365t-spi.h"
struct fake {uint32_t regs[32];unsigned tx,rx,delay,cs,fail_at;uint8_t bytes[512];};
static uint32_t r32(void *p,unsigned o){struct fake*f=p;if(o==0x28)return f->fail_at&&f->tx>=f->fail_at?0:0x300;return f->regs[o/4];}
static void w32(void*p,unsigned o,uint32_t v){struct fake*f=p;if(o==8){if(!(v&0x100))f->cs++;}f->regs[o/4]=v;}
static uint8_t r8(void*p,unsigned o){struct fake*f=p;assert(o==0);f->rx++;return f->rx==1?0x83:0x93;}
static void w8(void*p,unsigned o,uint8_t v){struct fake*f=p;assert(o==0&&f->tx<512);f->bytes[f->tx++]=v;}
static void delay(void*p,unsigned n){struct fake*f=p;f->delay+=n;}
int main(void){struct fake f={0};struct a03_jd_bus b={&f,r32,w32,r8,w8,delay};uint16_t id=0;
assert(!a03_jd_rom_id(&b,&id)&&id==0x9383&&f.rx==2&&f.tx==18&&f.cs==3);
const uint8_t expected[]={0xf2,0xaa,0x55,0x0f,0xf0,0x68,0xf3,0x40,0,0x80,0x76,1,0xf2,0xaa,0x88,0,0,0};
assert(!memcmp(expected,f.bytes,sizeof expected));assert((f.regs[2]&0xf00)==0xf00&&!(f.regs[3]&0x3000));
memset(&f,0,sizeof f);f.fail_at=6;id=0xbeef;assert(a03_jd_rom_id(&b,&id)==-1&&id==0xbeef&&f.tx==12&&f.delay==20000);assert((f.regs[2]&0xf00)==0xf00);
memset(&f,0,sizeof f);uint8_t data[256]={0};assert(a03_jd_phase(&b,NULL,NULL,1)==-1);assert(a03_jd_phase(&b,data,data,1)==-1);assert(a03_jd_phase(&b,data,NULL,0)==-1);assert(a03_jd_phase(&b,data,NULL,257)==-1);assert(!f.tx);
assert(!a03_jd_phase(&b,data,NULL,256)&&f.tx==256);assert(!a03_jd_phase(&b,NULL,data,256)&&f.rx==256);
puts("PASS actual Jadard SPI helpers: ROM wire bytes, CS0 framing, paired phases, FIFO chunks, bounded timeout/exit cleanup, invalid lengths");}
'''
with tempfile.TemporaryDirectory(prefix='a03-jdspi-') as d:
 p=Path(d)/'test.c';p.write_text(SRC)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I',str(ROOT),str(p),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
