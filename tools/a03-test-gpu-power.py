#!/usr/bin/env python3
"""Test actual0163 power preflight and ADI ownership using fake hardware."""
import argparse
from pathlib import Path
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--source',type=Path,required=True)
a=p.parse_args()
with tempfile.TemporaryDirectory(prefix='a03-gpu-power-') as tmp:
 t=Path(tmp)
 for name in ('bsd/dev/a03_gpu.c','bsd/dev/a03_usb_console.c','bsd/kern/sweet_amfi.c'):
  out=t/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes((a.source/name).read_bytes())
 patch=ROOT/'xnu/a03/0163-a03-gpu-power-preflight.patch'
 subprocess.run(['git','apply',str(patch)],cwd=t,check=True)
 source=(t/'bsd/dev/a03_gpu.c').read_text()
 source=chr(10).join(line for line in source.splitlines() if not line.startswith('#include'))
 source=source.replace('__asm__ volatile("dsb sy" ::: "memory");','')
 header=r'''
#include <stdint.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
#define ARM64_BOARD_CONFIG_SWEET 1
typedef uintptr_t vm_offset_t;
typedef unsigned long vm_size_t;
static uint32_t banks[6][1024],pd,vsel;
static unsigned maps[6],ticks,fail,stuck;
static int supply_ok;
static void delay(unsigned us){ticks+=us;assert(ticks<=2500);}
int a03_gpu_supply_status(uint32_t *p,uint32_t *v){*p=pd;*v=vsel;return supply_ok;}
vm_offset_t ml_io_map(vm_offset_t addr,vm_size_t size){
 assert(size==4096);
 unsigned n=addr==0x64020000?0:addr==0x64000000?1:addr==0x23000000?2:addr==0x23100000?3:addr==0x23014000?4:addr==0x64014000?5:6;
 assert(n<6);maps[n]++;
 return fail==n+1?0:(uintptr_t)banks[n];
}
'''
 tests=r'''
static void reset(void){
 memset(banks,0,sizeof(banks));memset(maps,0,sizeof(maps));
 a03_gpu_pmu=a03_gpu_aon=a03_gpu_apb=a03_gpu_regs=a03_gpu_dvfs=a03_gpu_topdvfs=0;
 ticks=fail=stuck=pd=0;supply_ok=1;vsel=224;
 banks[1][0]=1<<11;banks[0][0x500/4]=7<<24;
 banks[2][1]=banks[2][2]=banks[2][3]=1;banks[3][0]=0x70930000;
}
int main(void){
 reset();a03_gpu_probe();assert(maps[3]==1); /* sleeping C0 does not block top registers */
 reset();a03_gpu_power();assert(maps[4]&&maps[5]&&maps[3]);assert(ticks==300);
 for(unsigned n=0;n<512;n++){
  reset();vsel=n;a03_gpu_power();
  assert((maps[0]!=0)==(n>=224&&n<=256));
 }
 reset();pd=8;a03_gpu_power();assert(!maps[0]);
 reset();supply_ok=0;a03_gpu_power();assert(!maps[0]);
 reset();banks[0][0x2c4/4]=1<<24;a03_gpu_power();assert(!maps[2]&&!maps[3]);
 reset();banks[0][0x2c4/4]=0x02010102;a03_gpu_power();assert(banks[0][0x2c4/4]==0x10102);
 reset();banks[0][0x2c4/4]=0x02010102;banks[0][0x500/4]|=7<<16;
 a03_gpu_power();assert(!maps[2]&&!maps[3]);assert(ticks==2300);assert(banks[0][0x2c4/4]==0x02010102);
 reset();banks[1][0]=0x002bc2c1;a03_gpu_power();assert(banks[1][0]==0x002bcac1);
 for(unsigned i=1;i<=6;i++){reset();fail=i;a03_gpu_power();}
 for(unsigned i=1;i<=3;i++){reset();banks[2][i]=0;a03_gpu_power();assert(!maps[3]);}
 return 0;
}
'''
 c=t/'test.c';c.write_text(header+source+tests)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(c),'-o',str(t/'test')],check=True)
 with (t/'test.log').open('w') as output:subprocess.run([str(t/'test')],stdout=output,check=True)
 usb=(t/'bsd/dev/a03_usb_console.c').read_text()
 section=usb[usb.index('static volatile unsigned adi_runtime_busy;'):usb.index('static int usb_supply(')]
 h=r'''
#include <stdint.h>
#include <assert.h>
static int adi=1,ok=1,reads,resets,nested;
int a03_gpu_supply_status(uint32_t *,uint32_t *);
static int adi_read(unsigned reg,uint32_t *v){assert(reg==0x181c||reg==0x1854);reads++;*v=reg;return ok;}
static int download_reset_unlocked(void){uint32_t p,v;resets++;nested=a03_gpu_supply_status(&p,&v);return 1;}
'''
 checks=r'''
int main(void){uint32_t p,v;
 assert(a03_gpu_supply_status(&p,&v)&&p==0x181c&&v==0x1854&&reads==2);
 adi_runtime_busy=1;assert(!a03_gpu_supply_status(&p,&v));assert(!download_reset());
 adi_runtime_busy=0;ok=0;assert(!a03_gpu_supply_status(&p,&v)&&!adi_runtime_busy);
 ok=1;assert(download_reset()&&resets==1&&!nested&&!adi_runtime_busy);
 adi=0;assert(!a03_gpu_supply_status(&p,&v));return 0;}
'''
 c.write_text(h+section+checks)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(c),'-o',str(t/'adi')],check=True)
 subprocess.run([str(t/'adi')],check=True)
 subprocess.run(['git','apply','--reverse','--check',str(patch)],cwd=t,check=True)
print('PASS actual0163: rail bounds, sleeping shader vs top domain, timeout/restore, bus-bit preservation, map failures, closed clocks, ADI ownership, ASan/UBSan')
