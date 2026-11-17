#!/usr/bin/env python3
"""Run actual RAM loader state machine using fake register/RAM transport."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
SOURCE=r'''
#include <assert.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <stddef.h>
#define A03_JD9365T_MEMORY_H
struct a03_jd_bus {void*context;void(*delay_us)(void*,unsigned);};
static unsigned calls,ramwrites,starts,stops,delays,reads;static int badid,busy,badcrc,ramfail;
static uint16_t expected;
static int a03_jd_rom_id(struct a03_jd_bus*b,uint16_t*id){(void)b;calls++;*id=badid?0:0x9383;return badid?-2:0;}
static int a03_jd_write(struct a03_jd_bus*b,const uint8_t*p,size_t n){(void)b;calls++;assert(p[0]==0xf2);if(p[1]==0xaa){assert(n==6);return 0;}uint32_t a=((uint32_t)p[1]<<24)|((uint32_t)p[2]<<16)|((uint32_t)p[3]<<8)|p[4];assert(p[5]==1);if(a==0x40008014){if(p[6]==0xf1)starts++;else{assert(p[6]==0);stops++;}}if(a==0x40000200){assert(n==19&&p[18]==3);assert(p[6]==0&&p[10]==16&&p[14]==0);}return 0;}
static int a03_jd_read(struct a03_jd_bus*b,const uint8_t*p,size_t n,uint8_t*out,size_t count){(void)b;calls++;reads++;assert(n==6&&p[0]==0xf3&&p[1]==0x40&&p[2]==0&&p[3]==2&&p[5]==1);if(p[4]==0x1d){assert(count==1);out[0]=busy?1:0;}else{assert(p[4]==0x1a&&count==2);out[0]=(uint8_t)(expected^(badcrc?1:0));out[1]=expected>>8;}return 0;}
static int a03_jd_ram_write(struct a03_jd_bus*b,uint32_t a,const uint8_t*p,size_t n){(void)b;(void)p;calls++;ramwrites++;assert(a==0&&n==16);return ramfail?-1:0;}
static void delay(void*c,unsigned n){(void)c;delays+=n;}
#include "shim/a03/jd9365t-loader.h"
static void reset(void){calls=ramwrites=starts=stops=delays=reads=0;badid=busy=badcrc=ramfail=0;}
int main(void){
 uint8_t image[272]={0};image[3]=15;image[7]=1;image[10]=15;
 for(unsigned i=256;i<272;i++)image[i]=i;
 expected=a03_jd_crc16(image+256,16);image[15]=expected>>8;image[16]=expected;
 struct a03_jd_bus bus={NULL,delay};
 assert(!a03_jd_load_ram(&bus,image,sizeof(image)));assert(ramwrites==1&&starts==1&&stops==1&&delays==52000&&reads==2);
 reset();image[256]^=1;assert(a03_jd_load_ram(&bus,image,sizeof(image))==-2&&!calls);image[256]^=1;
 reset();badid=1;assert(a03_jd_load_ram(&bus,image,sizeof(image))==-3&&calls==1&&!ramwrites&&!starts);
 reset();ramfail=1;assert(a03_jd_load_ram(&bus,image,sizeof(image))==-5&&!starts&&stops==2);
 reset();badcrc=1;assert(a03_jd_load_ram(&bus,image,sizeof(image))==-11&&!starts&&stops==2);
 reset();busy=1;assert(a03_jd_load_ram(&bus,image,sizeof(image))==-9&&!starts&&reads==25&&delays==50000);
 uint8_t p[13]={0};reset();assert(a03_jd_control_write(&bus,0x40000200,p,13)==-1&&!calls);p[12]=7;assert(a03_jd_control_write(&bus,0x40000200,p,13)==-1&&!calls);assert(a03_jd_control_byte(&bus,0x40008004,0xa5)==-1&&!calls);
 puts("PASS actual RAM loader: whole-image gate, ROM gate, stock sequence, RAM-only DMA3, little-endian HW CRC, no start on failure, bounded busy timeout");
}
'''
with tempfile.TemporaryDirectory(prefix='a03-loader-') as d:
 p=Path(d);(p/'test.c').write_text(SOURCE)
 for cc,std,lang in [('clang','c11','c'),('clang++','c++17','c++')]:
  subprocess.run([cc,'-x',lang,'-std='+std,'-Wall','-Wextra','-Werror','-Wno-missing-field-initializers','-fsanitize=address,undefined','-I',str(ROOT),str(p/'test.c'),'-o',str(p/'test')],check=True)
  subprocess.run([str(p/'test')],check=True)
