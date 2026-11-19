#!/usr/bin/env python3
"""Exercise actual0165 core-power cycle against a stateful fake GPU."""
from pathlib import Path
import argparse,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);a=p.parse_args()
with tempfile.TemporaryDirectory(prefix='a03-cores-') as tmp:
 t=Path(tmp)
 for name in ('bsd/dev/a03_gpu.c','bsd/kern/sweet_amfi.c'):
  target=t/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((a.source/name).read_bytes())
 patch=ROOT/'xnu/a03/0165-a03-gpu-core-power-cycle.patch';subprocess.run(['git','apply',str(patch)],cwd=t,check=True)
 source=(t/'bsd/dev/a03_gpu.c').read_text();source=chr(10).join(l for l in source.splitlines() if not l.startswith('#include')).replace('__asm__ volatile("dsb sy" ::: "memory");','')
 source=source.replace('*(volatile uint32_t *)(a03_gpu_regs + offset) = value;','fake_write(offset, value);')
 header='''
#include <stdint.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
#define ARM64_BOARD_CONFIG_SWEET 1
typedef uintptr_t vm_offset_t;
typedef unsigned long vm_size_t;
static uint32_t bank[7][1024],pd,vol;
static unsigned ticks,writes,offsets[32],values[32],failure;
int a03_gpu_supply_status(uint32_t*p,uint32_t*v){*p=pd;*v=vol;return 1;}
static void delay(unsigned us){ticks+=us;assert(ticks<100000);}
vm_offset_t ml_io_map(vm_offset_t addr,vm_size_t size){(void)addr;(void)size;assert(0);return 0;}
static void fake_write(unsigned off,uint32_t v){
 assert(writes<32);offsets[writes]=off;values[writes++]=v;
 assert(off==0x50||off==0x58||off==0x190||off==0x180||off==0x1c0||off==0x1d0||off==0x1e0);
 if(off==0x50){assert(v==0x2968a819);return;}
 if(off==0x58){assert(writes>=2&&offsets[writes-2]==0x50);bank[3][off/4]=v;return;}
 assert(v==1);
 if(off==0x190){assert(writes>=3&&offsets[writes-2]==0x58);if(failure!=1)bank[3][0x150/4]=bank[3][0x160/4]=1;}
 if(off==0x180){assert(bank[3][0x150/4]&&bank[3][0x160/4]);if(failure!=2)bank[3][0x140/4]=1;}
 if(off==0x1c0){if(failure!=3)bank[3][0x140/4]=0;}
 if(off==0x1d0){assert(!bank[3][0x140/4]);if(failure!=4)bank[3][0x150/4]=0;}
 if(off==0x1e0){assert(!bank[3][0x140/4]);if(failure!=4)bank[3][0x160/4]=0;}
}
'''
 tests='''
static void reset(void){
 memset(bank,0,sizeof(bank));pd=writes=ticks=failure=0;vol=320;
 a03_gpu_pmu=(uintptr_t)bank[0];a03_gpu_aon=(uintptr_t)bank[1];a03_gpu_apb=(uintptr_t)bank[2];a03_gpu_regs=(uintptr_t)bank[3];
 bank[1][0]=1<<11;bank[0][0x500/4]=7<<24;
 bank[2][1]=bank[2][2]=0x11;bank[2][3]=0x31;bank[3][0]=0x90910010;
 bank[3][0x100/4]=bank[3][0x110/4]=bank[3][0x120/4]=1;bank[3][0x58/4]=0x12345678;
}
int main(void){
 reset();a03_gpu_cores();assert(writes==11&&ticks==120);
 assert(offsets[2]==0x190&&offsets[5]==0x180&&offsets[6]==0x1c0&&offsets[7]==0x1d0&&offsets[8]==0x1e0);
 assert(bank[3][0x58/4]==0x12345678&&!bank[3][0x140/4]&&!bank[3][0x150/4]&&!bank[3][0x160/4]);
 for(unsigned i=1;i<=4;i++){reset();failure=i;a03_gpu_cores();assert(writes>0);if(i<3)assert(bank[3][0x58/4]==0x12345678);else assert(bank[3][0x58/4]==0xf01e0078);}
 for(unsigned i=0;i<3;i++)for(unsigned field=0;field<6;field++){
  reset();unsigned off=(field<2?0x100:field<4?0x140:0x200)+i*16+(field%2)*4;
  bank[3][off/4]=2;a03_gpu_cores();assert(!writes);
 }
 reset();pd=8;a03_gpu_cores();assert(!writes);
 reset();vol=224;a03_gpu_cores();assert(!writes);
 reset();a03_gpu_regs=0;a03_gpu_cores();assert(!writes);
 reset();bank[3][0]=0x70930000;a03_gpu_cores();assert(!writes);
 reset();bank[0][0x2c4/4]=1<<25;a03_gpu_cores();assert(!writes);
 reset();bank[3][0x34/4]=1;a03_gpu_cores();assert(!writes);
 reset();bank[3][0x3c/4]=1;a03_gpu_cores();assert(!writes);
 reset();bank[3][0x20/4]=0x80;a03_gpu_cores();assert(!writes);
 return 0;
}
'''
 c=t/'test.c';c.write_text(header+source+tests)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(c),'-o',str(t/'test')],check=True)
 with (t/'log').open('w') as log:subprocess.run([str(t/'test')],stdout=log,check=True)
 subprocess.run(['git','apply','--reverse','--check',str(patch)],cwd=t,check=True)
print('PASS actual0165 vendor key/order, ownership guards, bounded timeouts, shutdown/override restore, ASan/UBSan')
