#!/usr/bin/env python3
"""Run the actual 0147 section-read session using a constrained fake bus."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
p=(ROOT/'xnu/a03/0147-a03-explicit-jadard-section-read.patch').read_text()
s='\n'.join(l[1:] for l in p.splitlines() if l.startswith('+') and not l.startswith('+++'))
s=s[s.index('/* Bounded read-only'):s.index(' if(strcmp(command,')]
prefix=r'''
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "shim/a03/jd9365t-sections.h"
struct a03_jd_bus {int unused;};
static unsigned writes,reads;static int fail,notready,invalid;
static int a03_jd_write(struct a03_jd_bus*b,const uint8_t*p,size_t n){(void)b;assert(n==6&&p[0]==0xf2&&p[1]==0xaa);if(writes==0)assert(p[2]==0x55&&p[5]==0x68);else assert(p[2]==0x88&&p[5]==0);writes++;return fail==1?-1:0;}
static void put(uint8_t*p,uint32_t n){for(unsigned i=0;i<4;i++)p[i]=n>>(8*i);}
static int a03_jd_read(struct a03_jd_bus*b,const uint8_t*p,size_t n,uint8_t*out,size_t count){(void)b;assert(n==6&&p[0]==0xf3&&p[5]==1);reads++;if(fail==2)return -1;memset(out,0,count);if(reads==1){assert(count==160&&p[1]==0x20&&p[2]==1&&p[3]==0x10&&p[4]==0);out[0]=0x5a;out[1]=notready?0:0xa5;put(out+28,invalid?0x40008000:0x20002000);put(out+32,64);put(out+152,0x20011200);put(out+156,60);}else{assert(reads==2&&count==6&&p[1]==0x20&&p[2]==0&&p[3]==0x20&&p[4]==0);out[0]=0xd0;out[1]=2;out[2]=0x40;out[3]=6;out[4]=18;out[5]=32;}return 0;}
'''
test=r'''
int main(void){struct a03_jd_bus b={0};a03_touch_sections(&b);assert(writes==2&&reads==2);
for(int mode=1;mode<=4;mode++){writes=reads=0;fail=mode<=2?mode:0;notready=mode==3;invalid=mode==4;a03_touch_sections(&b);assert(writes==2);assert(reads==(mode==1?0:1));}
puts("PASS actual section session: enter/read/config/exit, fixed addresses, no config on malformed/range/transport failure, cleanup");}
'''
with tempfile.TemporaryDirectory(prefix='a03-sections-session-') as d:
 p=Path(d)/'test.c';p.write_text(prefix+s+test)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I',str(ROOT),str(p),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
