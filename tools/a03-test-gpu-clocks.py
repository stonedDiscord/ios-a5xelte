#!/usr/bin/env python3
"""Exercise0164 inherited clock gates, PLL decode and rollback (host only)."""
from pathlib import Path
import argparse,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);a=p.parse_args()
with tempfile.TemporaryDirectory(prefix='a03-clocks-') as tmp:
 t=Path(tmp)
 for name in ('bsd/dev/a03_gpu.c','bsd/kern/sweet_amfi.c'):
  target=t/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((a.source/name).read_bytes())
 patch=ROOT/'xnu/a03/0164-a03-inherited-gpu-clock-gates.patch'
 subprocess.run(['git','apply',str(patch)],cwd=t,check=True)
 source=(t/'bsd/dev/a03_gpu.c').read_text()
 source=chr(10).join(l for l in source.splitlines() if not l.startswith('#include')).replace('__asm__ volatile("dsb sy" ::: "memory");','')
 header='''
#include <stdint.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
#define ARM64_BOARD_CONFIG_SWEET 1
typedef uintptr_t vm_offset_t;
typedef unsigned long vm_size_t;
static uint32_t bank[7][1024],pd,vol;
static unsigned maps[7],fail,ticks;
int a03_gpu_supply_status(uint32_t*p,uint32_t*v){*p=pd;*v=vol;return 1;}
static void delay(unsigned us){ticks+=us;assert(ticks<=2400);}
vm_offset_t ml_io_map(vm_offset_t addr,vm_size_t size){
 assert(size==4096);
 unsigned n=addr==0x64020000?0:addr==0x64000000?1:addr==0x23000000?2:addr==0x23100000?3:addr==0x23014000?4:addr==0x64014000?5:addr==0x645a0000?6:7;
 assert(n<7);maps[n]++;return fail==n+1?0:(uintptr_t)bank[n];
}
'''
 tests='''
static void reset(void){
 memset(bank,0,sizeof(bank));memset(maps,0,sizeof(maps));fail=ticks=pd=0;vol=320;
 a03_gpu_pmu=a03_gpu_aon=a03_gpu_apb=a03_gpu_regs=a03_gpu_dvfs=a03_gpu_topdvfs=a03_gpu_pll=0;
 bank[0][0x500/4]=7<<24;bank[1][0]=1<<11;
 bank[2][1]=bank[2][2]=0x10;bank[2][3]=0x30;
 bank[3][0]=0x70930000;
 /* Fractional1536MHz:59 +1/13, represented by nearest23bit fraction. */
 bank[6][0]=(1<<18)|3;bank[6][1]=(59U<<23)|645278;
}
int main(void){
 reset();assert(a03_gpu_twpll_rate(bank[6][0],bank[6][1],0)>1535999900ULL);
 assert(a03_gpu_twpll_rate(60<<5,0,0)==1560000000ULL);
 assert(a03_gpu_twpll_rate(60<<5,0,1<<13)==780000000ULL);
 reset();uint32_t before[7][1024];memcpy(before,bank,sizeof(before));a03_gpu_clocks();
 assert(bank[2][1]==0x11&&bank[2][2]==0x11&&bank[2][3]==0x31&&maps[3]);
 before[2][1]|=1;before[2][2]|=1;before[2][3]|=1;
 assert(!memcmp(before,bank,sizeof(before)));assert(ticks==400);
 for(unsigned n=0;n<512;n++){reset();vol=n;a03_gpu_clocks();assert((maps[3]!=0)==(n==320));}
 reset();pd=8;a03_gpu_clocks();assert(!maps[0]);
 reset();bank[0][0x2c4/4]=1<<25;a03_gpu_clocks();assert(!maps[2]);
 reset();bank[0][0x500/4]|=7<<16;a03_gpu_clocks();assert(!maps[2]);
 reset();bank[6][0]&=~(1<<18);a03_gpu_clocks();assert(!maps[3]&&bank[2][1]==0x10);
 reset();bank[6][1]=60U<<23;a03_gpu_clocks();assert(!maps[3]);
 reset();bank[4][0x38/4]=0x80000;a03_gpu_clocks();assert(!maps[3]);
 for(unsigned reg=1;reg<=3;reg++){
  reset();bank[2][reg]|=1;a03_gpu_clocks();assert(!maps[3]);
  reset();bank[2][reg]^=0x10;a03_gpu_clocks();assert(!maps[3]);
 }
 for(unsigned reg=1;reg<=2;reg++)for(unsigned sel=0;sel<8;sel++)for(unsigned div=0;div<8;div++){
  reset();bank[2][reg]=(sel<<4)|(div<<8);a03_gpu_clocks();
  assert((maps[3]!=0)==(sel==1&&div==0));
 }
 for(unsigned div=0;div<8;div++){reset();bank[2][3]=div<<4;a03_gpu_clocks();assert((maps[3]!=0)==(div==3));}
 for(unsigned n=1;n<=7;n++){if(n==6)continue;reset();fail=n;a03_gpu_clocks();assert(bank[2][1]==0x10&&bank[2][2]==0x10&&bank[2][3]==0x30);}
 for(unsigned n=0;n<2;n++){reset();bank[3][0]=n?UINT32_MAX:0;a03_gpu_clocks();assert(bank[2][1]==0x10&&bank[2][2]==0x10&&bank[2][3]==0x30);}
 return 0;
}
'''
 c=t/'test.c';c.write_text(header+source+tests)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(c),'-o',str(t/'test')],check=True)
 with (t/'log').open('w') as log:subprocess.run([str(t/'test')],stdout=log,check=True)
 subprocess.run(['git','apply','--reverse','--check',str(patch)],cwd=t,check=True)
print('PASS actual0164 PLL decoding, inherited rail/rates/ownership, leaf-only writes, failures/rollback, ASan/UBSan')
