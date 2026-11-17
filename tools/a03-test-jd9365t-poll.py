#!/usr/bin/env python3
"""Run actual bounded poll state machine against fake complete reports."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
SOURCE=r'''
#include <assert.h>
#include <string.h>
#include <stdint.h>
#include <stddef.h>
#define A03_JD9365T_MEMORY_H
struct a03_jd_bus{void*context;void(*delay_us)(void*,unsigned);};
static unsigned writes,reads,samples,events,downs,ups,delaytotal;static unsigned upsample;static int badid,notready,badconfig,failframes,pramconfig,zero,idleafterfirst;
static int a03_jd_rom_id(struct a03_jd_bus*b,uint16_t*i){(void)b;*i=0x9383;return badid?-1:0;}
static int a03_jd_write(struct a03_jd_bus*b,const uint8_t*p,size_t n){(void)b;assert(n==6&&p[0]==0xf2&&p[1]==0xaa);writes++;return 0;}
static int a03_jd_ram_range(uint32_t a,size_t n,int w){(void)n;return w?a==0x20002000:a==0x20011200;}
static void put(uint8_t*p,uint32_t v){for(unsigned i=0;i<4;i++)p[i]=v>>(i*8);}
static int a03_jd_ram_read(struct a03_jd_bus*b,uint32_t a,uint8_t*p,size_t n){(void)b;reads++;memset(p,0,n);if(a==0x20011000){assert(n==160);p[0]=0x5a;p[1]=notready?0:0xa5;put(p+28,pramconfig?0x2000:0x20002000);put(p+32,64);put(p+152,0x20011200);put(p+156,60);}else if(a==0x20002000){assert(n==6);p[0]=0xd0;p[1]=2;p[2]=0x40;p[3]=6;p[4]=badconfig?0:18;p[5]=32;}else{assert(a==0x20011200&&n==60);samples++;if(idleafterfirst&&samples>1){p[2]=0xff;return 0;}if(zero)return 0;if(failframes&&samples>1)return -1;memset(p,255,n);p[0]=1;p[3]=0;p[4]=10;p[5]=0;p[6]=(uint8_t)samples;p[7]=5;}return 0;}
static void delay(void*c,unsigned n){(void)c;delaytotal+=n;}
static void emit(void*c,unsigned i,int d,unsigned x,unsigned y){(void)c;assert(i==0&&x==10&&y);events++;if(d)downs++;else {ups++;upsample=samples;}}
#include "shim/a03/jd9365t-poll.h"
static void reset(void){writes=reads=samples=events=downs=ups=delaytotal=upsample=0;badid=notready=badconfig=failframes=pramconfig=zero=idleafterfirst=0;}
int main(void){struct a03_jd_bus b={NULL,delay};unsigned valid=999;
 assert(!a03_jd_poll(&b,3,emit,NULL,&valid));assert(valid==3&&downs==3&&ups==1&&writes==9&&delaytotal==48000);
 reset();assert(a03_jd_poll(&b,301,emit,NULL,&valid)==-1&&!writes&&!reads);
 reset();badid=1;assert(a03_jd_poll(&b,3,emit,NULL,&valid)==-2&&!writes&&!reads);
 reset();notready=1;assert(a03_jd_poll(&b,3,emit,NULL,&valid)==-3&&writes==2&&!samples&&!events&&valid==0);
 reset();badconfig=1;assert(a03_jd_poll(&b,3,emit,NULL,&valid)==-3&&writes==2&&!samples&&!events);
 reset();pramconfig=1;assert(a03_jd_poll(&b,3,emit,NULL,&valid)==-3&&writes==2&&!samples&&!events);
 reset();idleafterfirst=1;assert(!a03_jd_poll(&b,3,emit,NULL,&valid));assert(valid==3&&downs==1&&ups==1&&upsample==2&&events==2);
 reset();struct a03_jd_contact_state state={{{0,0,0,0}},0};
 assert(!a03_jd_poll_slice(&b,1,&state,0,emit,NULL,&valid));assert(downs==1&&!ups&&state.contacts[0].down);
 assert(!a03_jd_poll_slice(&b,1,&state,0,emit,NULL,&valid));assert(downs==2&&!ups&&state.contacts[0].down);
 idleafterfirst=1;assert(!a03_jd_poll_slice(&b,1,&state,0,emit,NULL,&valid));assert(ups==1&&!state.contacts[0].down&&upsample==3);
 idleafterfirst=0;assert(!a03_jd_poll_slice(&b,1,&state,0,emit,NULL,&valid));assert(downs==3&&ups==1);
 badid=1;assert(a03_jd_poll_slice(&b,1,&state,0,emit,NULL,&valid)==-2);assert(ups==2&&!state.contacts[0].down&&!valid);
 badid=0;assert(!a03_jd_poll_slice(&b,1,&state,0,emit,NULL,&valid));assert(downs==4&&ups==2);
 notready=1;assert(a03_jd_poll_slice(&b,1,&state,0,emit,NULL,&valid)==-3);assert(ups==3&&!state.contacts[0].down);
 reset();zero=1;assert(a03_jd_poll(&b,300,emit,NULL,&valid)==-4&&samples==3&&!valid&&!events&&writes==9);
 reset();failframes=1;assert(a03_jd_poll(&b,300,emit,NULL,&valid)==-4&&samples==4&&valid==1&&downs==1&&ups==1&&writes==11);
}
'''
with tempfile.TemporaryDirectory(prefix='a03-jd-poll-') as d:
 p=Path(d);(p/'test.c').write_text(SOURCE)
 for cc,std,lang in [('clang','c11','c'),('clang++','c++17','c++')]:
  subprocess.run([cc,'-x',lang,'-std='+std,'-Wall','-Wextra','-Werror','-Wno-missing-field-initializers','-fsanitize=address,undefined','-I',str(ROOT),str(p/'test.c'),'-o',str(p/'test')],check=True)
  subprocess.run([str(p/'test')],check=True)
print('PASS actual bounded poll: ROM/ready/config gates, frame cap, no failed-read presses, consecutive-failure stop, measured idle release before cleanup, continuing slices retain contacts, ROM/config failure releases, final release/exit')
