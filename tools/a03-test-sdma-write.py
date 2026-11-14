#!/usr/bin/env python3
"""Exercise production USERDATA CMD24 bounds/sequence with fake registers, not hardware."""
from pathlib import Path
import subprocess,tempfile
s=(Path(__file__).resolve().parents[1]/'xnu/a03/a03_emmc.c').read_text()
a=s.index('static int data_write(');b=s.index('/* Minor0',a)
code=r'''
#include <stdint.h>
#include <stdbool.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#define EIO 5
#define EROFS 30
#define ENXIO 6
static struct {bool writable,poisoned,cache_enabled;uint32_t sectors,rca;uint64_t pa;uintptr_t regs,dma;struct {uint32_t userdata,userdata_count;} gpt;} ae;
static unsigned char mmio[4096],dma[512];static uint32_t values[1024],commands[4];
static unsigned writes,ncmd,npoll,failpoll,syncs;
static void barrier(void) {}
static uint32_t rd(unsigned off) {return values[off/4];}
static void wr(unsigned off,uint32_t v) {
 writes++;
 if(off==0x30)values[off/4]&=~v;
 else values[off/4]=v;
 if(off==0xc) {assert(ncmd<4);commands[ncmd++]=v;values[0x10/4]=0x900;}
}
static void dma_sync(bool before) {assert(before);syncs++;}
static bool poll(unsigned mask) {(void)mask;return ++npoll!=failpoll;}
'''
test=r'''
static void reset(void) {
 memset(&ae,0,sizeof(ae));memset(values,0,sizeof(values));memset(mmio,0,sizeof(mmio));
 ae.writable=true;ae.sectors=10000;ae.gpt.userdata=1000;ae.gpt.userdata_count=100;
 ae.rca=0x10000;ae.pa=0x104000000;ae.regs=(uintptr_t)mmio;ae.dma=(uintptr_t)dma;
 mmio[0xfe]=4;values[0x3c/4]=0x30000000;writes=ncmd=npoll=failpoll=syncs=0;
}
int main(void) {
 unsigned char sector[512];memset(sector,0xa9,512);
 reset();ae.writable=false;assert(data_write(1000,sector)==EROFS&&writes==0);
 reset();assert(data_write(999,sector)==EIO&&writes==0);
 assert(data_write(1100,sector)==EIO&&writes==0);
 reset();ae.poisoned=true;assert(data_write(1000,sector)==EIO&&writes==0);
 reset();assert(data_write(1000,sector)==0);assert(syncs==1&&ncmd==2);
 assert(commands[0]==0x183a0001&&commands[1]==0x0d1a0000);
 assert(memcmp(dma,sector,512)==0&&!ae.poisoned);
 reset();ae.cache_enabled=true;assert(data_write(1000,sector)==0);
 assert(ncmd==3&&commands[0]==0x183a0001&&commands[1]==0x061b0000&&commands[2]==0x0d1a0000);
 for(unsigned i=1;i<=5;i++) {
  reset();ae.cache_enabled=true;failpoll=i;assert(data_write(1000,sector)==EIO&&ae.poisoned);
 }
 for(unsigned i=1;i<=3;i++) {
  reset();failpoll=i;assert(data_write(1099,sector)==EIO&&ae.poisoned);
  unsigned prev=writes;assert(data_write(1000,sector)==EIO&&writes==prev);
 }
 puts("PASS production CMD24: USERDATA-only bounds, DMA copy, CMD24/status, terminal failure/no retries");
}
'''
with tempfile.TemporaryDirectory(prefix='a03-write-') as t:
 p=Path(t);(p/'t.c').write_text(code+s[a:b]+test)
 subprocess.run(['clang','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p/'t.c'),'-o',str(p/'t')],check=True)
 subprocess.run([str(p/'t')],check=True)
