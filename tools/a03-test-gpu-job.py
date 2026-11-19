#!/usr/bin/env python3
"""Actual0166 job lifecycle under fake DMA/MMIO; no hardware claim."""
from pathlib import Path
import argparse,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);a=p.parse_args()
with tempfile.TemporaryDirectory(prefix='a03-job-') as tmp:
 t=Path(tmp)
 for name in ('bsd/dev/a03_gpu.c','bsd/kern/sweet_amfi.c'):
  f=t/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes((a.source/name).read_bytes())
 patch=ROOT/'xnu/a03/0166-a03-private-write-value-job.patch';subprocess.run(['git','apply',str(patch)],cwd=t,check=True)
 assert (t/'bsd/dev/a03_gpu_job_layout.h').read_bytes()==(ROOT/'tools/a03-gpu-job-layout.h').read_bytes()
 src=(t/'bsd/dev/a03_gpu.c').read_text();src=chr(10).join(l for l in src.splitlines() if not l.startswith('#include')).replace('__asm__ volatile("dsb sy" ::: "memory");','')
 src=src.replace('uint32_t value = *(volatile uint32_t *)(base + offset);','uint32_t value = fake_read(base, offset);').replace('*(volatile uint32_t *)(a03_gpu_regs + offset) = value;','fake_write(offset, value);')
 layout=(t/'bsd/dev/a03_gpu_job_layout.h').read_text()
 header='''
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <assert.h>
#define ARM64_BOARD_CONFIG_SWEET 1
typedef uintptr_t vm_offset_t;
typedef unsigned long vm_size_t;
static uint32_t bank[7][4096];
static unsigned mode,us,writes,starts,offs,flushes,frees,updates,passed;
static void *allocation;
static int capture(const char*fmt,...){
 char line[1024];va_list ap;va_start(ap,fmt);vsnprintf(line,sizeof(line),fmt,ap);va_end(ap);
 if(strstr(line,"PASS=1"))passed++;return 0;
}
#define printf capture
static void delay(unsigned n){us+=n;assert(us<200000);}
int a03_gpu_supply_status(uint32_t*p,uint32_t*v){*p=0;*v=320;return 1;}
vm_offset_t ml_io_map(vm_offset_t p,vm_size_t n){(void)p;(void)n;assert(0);return 0;}
static void *IOMallocContiguous(vm_size_t n,vm_size_t align,void*p){
 assert(n==0x8000&&align==0x4000&&!p);if(mode==1)return 0;
 assert(!allocation);allocation=aligned_alloc(0x4000,n);assert(allocation);return allocation;
}
static void IOFreeContiguous(void*p,vm_size_t n){assert(!starts&&p==allocation&&n==0x8000);frees++;free(p);allocation=0;}
uint64_t kvtophys(vm_offset_t p){assert(p>=(uintptr_t)allocation&&p<(uintptr_t)allocation+0x8000);return 0x120000000ULL+p-(uintptr_t)allocation+((mode==2&&p>(uintptr_t)allocation+0x2000)?0x4000:0);}
static void FlushPoC_DcacheRegion(vm_offset_t p,vm_size_t n){assert(p==(uintptr_t)allocation&&n==0x8000);flushes++;}
static uint32_t fake_read(vm_offset_t b,unsigned o){
 assert(o<0x4000);if(b==(uintptr_t)bank[3]&&o==0x2428){
  if((mode==3&&updates==1)||(mode==7&&updates>=2))return 1;
 }
 return *(uint32_t *)(b+o);
}
static void fake_write(unsigned o,uint32_t v){
 assert(o<0x3000);writes++;
 if(o==0x50){assert(v==0x2968a819);return;}
 if(o==0x58){bank[3][o/4]=v;return;}
 if(o==0x190){bank[3][0x150/4]=bank[3][0x160/4]=1;return;}
 if(o==0x180){assert(bank[3][0x160/4]);bank[3][0x140/4]=1;return;}
 if(o==0x1c0){offs++;bank[3][0x140/4]=0;return;}
 if(o==0x1d0){bank[3][0x150/4]=0;return;}
 if(o==0x1e0){bank[3][0x160/4]=0;return;}
 if(o==0x2418){assert(v==1);updates++;return;}
 if(o==0x1004){assert(v==0x20002);bank[3][0x1000/4]&=~v;return;}
 if(o==0x18e0&&v==1){
  starts++;assert(flushes==1&&bank[3][0x2430/4]==0x21000006);
  assert(bank[3][0x2400/4]==0x20000000&&bank[3][0x2404/4]==1);
  assert(bank[3][0x2408/4]==0x888d8f88&&bank[3][0x240c/4]==0x4c8d);
  assert(bank[3][0x18c0/4]==0x2000000&&bank[3][0x18d8/4]==0x83300);
  assert(*(uint64_t *)((uint8_t*)allocation+0x5000)==0xa5a55a5adeadbeefULL);
  if(mode==4||mode==6){bank[3][0x18e0/4]=1;bank[3][0x1010/4]=2;return;}
  if(mode==5){bank[3][0x1000/4]=0x20000;bank[3][0x2000/4]=1;return;}
  *(uint64_t *)((uint8_t*)allocation+0x5000)=0x0077ccff003388aaULL;
  *(uint32_t *)((uint8_t*)allocation+0x4000)=1;
  bank[3][0x1000/4]=2;return;
 }
 if(o==0x18e0&&v==0){if(mode!=6)bank[3][0x18e0/4]=0;return;}
 if(o==0x18a0){assert(v==3);if(mode!=6)bank[3][0x1010/4]=0;return;}
 assert(o==0x2430||o==0x2434||o==0x2400||o==0x2404||o==0x2408||o==0x240c||o==0x18c0||o==0x18c4||o==0x18d0||o==0x18d4||o==0x18d8||o==0x18dc);
 bank[3][o/4]=v;
}
'''
 tests='''
static void reset(unsigned m){
 if(allocation)free(allocation);allocation=0;
 memset(bank,0,sizeof(bank));mode=m;us=writes=starts=offs=flushes=frees=updates=passed=0;
 a03_gpu_pmu=(uintptr_t)bank[0];a03_gpu_aon=(uintptr_t)bank[1];a03_gpu_apb=(uintptr_t)bank[2];a03_gpu_regs=(uintptr_t)bank[3];
 a03_gpu_scratch=0;a03_gpu_scratch_pa=0;a03_gpu_job_poisoned=a03_gpu_job_requested=0;
 bank[1][0]=1<<11;bank[0][0x500/4]=7<<24;bank[2][1]=bank[2][2]=0x11;bank[2][3]=0x31;
 bank[3][0]=0x90910010;bank[3][0x100/4]=bank[3][0x110/4]=bank[3][0x120/4]=1;
 bank[3][0x18/4]=1;bank[3][0x1c/4]=2;bank[3][0xc4/4]=4;
 bank[3][0x2408/4]=0x13579bdf;bank[3][0x240c/4]=0x2468ace0;bank[3][0x2430/4]=1;
}
int main(void){
 reset(0);a03_gpu_job();assert(passed==1&&starts==1&&offs==1&&!frees&&flushes==2&&!a03_gpu_job_poisoned);
 assert(bank[3][0x2400/4]==0&&bank[3][0x2404/4]==0&&bank[3][0x2430/4]==1&&bank[3][0x2408/4]==0x13579bdf&&bank[3][0x240c/4]==0x2468ace0);
 for(unsigned m=1;m<=7;m++){
  reset(m);a03_gpu_job();assert(!passed&&!a03_gpu_job_requested);
  if(m==1||m==2)assert(!starts&&offs==1);
  if(m==2)assert(frees==1&&!allocation);
  if(m==3||m==6||m==7){assert(a03_gpu_job_poisoned&&!offs);unsigned n=writes;a03_gpu_job();a03_gpu_cores();a03_gpu_clocks();a03_gpu_power();assert(writes==n);}
  if(m==4)assert(starts==1&&offs==1&&!a03_gpu_job_poisoned);
  if(m==5)assert(starts==1&&offs==1&&a03_gpu_job_poisoned);
  assert(!starts||!frees);
 }
 for(unsigned i=0;i<4;i++){
  reset(0);bank[3][(i==0?0x28:i==1?0x1008:i==2?0x2008:0x2400)/4]=1;a03_gpu_job();assert(!starts&&!allocation);
 }
 reset(0);if(allocation)free(allocation);return 0;
}
'''
 c=t/'test.c';c.write_text(header+layout+src+tests)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(c),'-o',str(t/'test')],check=True)
 subprocess.run([str(t/'test')],check=True)
 subprocess.run(['git','apply','--reverse','--check',str(patch)],cwd=t,check=True)
print('PASS actual0166 allocation/contiguity/AS restore, job result/cache ownership, timeout/fault retirement, quarantine/no-free, ASan/UBSan')
