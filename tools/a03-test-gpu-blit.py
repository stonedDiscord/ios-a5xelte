#!/usr/bin/env python3
"""Actual framebuffer GPU lifecycle under fake MMIO/DMA, not hardware evidence."""
from pathlib import Path
import argparse,subprocess,tempfile
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);args=p.parse_args()
fb=(args.source/'iokit/Kernel/arm/SweetFramebuffer.cpp').read_text()
assert 'IOLockLock(fFB->fLock);'+chr(10)+'\t\tfFB->swap(rec);'+chr(10)+'\t\tIOLockUnlock(fFB->fLock);' in fb
assert 'a03_fb_gpu_quarantined_surface=s;' in fb
assert fb.index('if(a03_fb_gpu_quarantined)return;')<fb.index('uint32_t mask = get32(rec, 0x104);')
assert fb.index('int copied=a03_gpu_framebuffer_blit')<fb.index('if(!copied)for (int32_t y = 0; y < h; y++)')
src=(args.source/'bsd/dev/a03_gpu.c').read_text()
src=chr(10).join(l for l in src.splitlines() if not l.startswith('#include')).replace('__asm__ volatile("dsb sy" ::: "memory");','')
src=src.replace('uint32_t value = *(volatile uint32_t *)(base + offset);','uint32_t value = fake_read(base, offset);').replace('*(volatile uint32_t *)(a03_gpu_regs + offset) = value;','fake_write(offset, value);')
layout=''
for name in ['a03_gpu_job_layout.h','a03_gpu_copy_layout.h','a03_gpu_blit_layout.h']:
 layout+=chr(10).join(l for l in (args.source/'bsd/dev'/name).read_text().splitlines() if not l.startswith('#include'))+chr(10)
header=r'''
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
static unsigned mode,us,writes,starts,offs,flushes,frees,updates,passed,cache_commands;
static unsigned expect_cached,cache_failure;
static void check_shader(unsigned specialized);
static uint64_t fake_time;
static uint64_t mach_absolute_time(void){return ++fake_time;}
static void absolutetime_to_nanoseconds(uint64_t t,uint64_t *ns){*ns=t*10;}
static void *allocation;
static int capture(const char*fmt,...){
 char line[1024];va_list ap;va_start(ap,fmt);vsnprintf(line,sizeof(line),fmt,ap);va_end(ap);
 if(strstr(line,"PASS=1"))passed++;return 0;
}
#define printf capture
static void delay(unsigned n){us+=n;assert(us<2000000);}
int a03_gpu_supply_status(uint32_t*p,uint32_t*v){*p=0;*v=320;return 1;}
static uint8_t source_mem[0x800000] __attribute__((aligned(16384)));
static uint8_t dest_mem[0x468000] __attribute__((aligned(16384)));
static uint8_t gpu_dirty[0x468000]; /* cached writes invisible until clean */
static unsigned bad_source,bad_dest,corrupt,noncontiguous;
static uint64_t source_physical(uintptr_t offset){return 0x140000000ULL+(noncontiguous?((offset&~4095ULL)*2+(offset&4095)):offset);}
vm_offset_t ml_io_map(vm_offset_t p,vm_size_t n){(void)p;(void)n;return 0;}
static void *IOMallocContiguous(vm_size_t n,vm_size_t align,void*p){
 assert(n==0x10000&&align==0x4000&&!p);if(mode==1)return 0;
 assert(!allocation);allocation=aligned_alloc(align,n);return allocation;
}
static void IOFreeContiguous(void*p,vm_size_t n){assert(!starts&&p==allocation&&n==0x10000);frees++;free(p);allocation=0;}
uint64_t kvtophys(vm_offset_t p){
 if(p>=(uintptr_t)source_mem&&p<(uintptr_t)source_mem+sizeof(source_mem)){uintptr_t off=p-(uintptr_t)source_mem;if(bad_source==1)return 0x80000000;if(bad_source==2&&off==4095)return 0x140004000ULL;return source_physical(off);}
 if(p>=(uintptr_t)dest_mem&&p<(uintptr_t)dest_mem+sizeof(dest_mem))return bad_dest?0:0x9e000000ULL+p-(uintptr_t)dest_mem;
 assert(allocation&&p>=(uintptr_t)allocation&&p<(uintptr_t)allocation+0x10000);
 return 0x120000000ULL+p-(uintptr_t)allocation+((mode==2&&p>(uintptr_t)allocation+0x2000)?0x4000:0);
}
static void FlushPoC_DcacheRegion(vm_offset_t p,vm_size_t n){assert((p==(uintptr_t)allocation&&n==0x10000)||(p>=(uintptr_t)source_mem&&p+n<=(uintptr_t)source_mem+sizeof(source_mem)));flushes++;}
static uint32_t fake_read(vm_offset_t b,unsigned o){
 assert(o<0x4000);if(b==(uintptr_t)bank[3]&&o==0x2428){
  if((mode==3&&updates==1)||(mode==7&&updates>=2))return 1;
 }
 return *(uint32_t *)(b+o);
}
static uint64_t walk(uint32_t va,int writable){
 uint64_t *root=(uint64_t *)allocation,pa=0x120000000ULL;
 unsigned shifts[]={39,30,21,12};uint64_t d=0;
 for(unsigned level=0;level<4;level++){
  d=root[((uint64_t)va>>shifts[level])&511];assert((d&3)==3);
  if(level<3){uint64_t next=d&0x000000fffffff000ULL;assert(next>=pa&&next<pa+0x10000);root=(uint64_t *)((uint8_t *)allocation+next-pa);}
 }
 assert(d&(1ULL<<54));assert((d&0xc0)==(writable?0x40:0xc0));
 assert(((d>>2)&7)==(expect_cached?0:5));
 return (d&0x000000fffffff000ULL)+(va&4095);
}
static void fake_write(unsigned o,uint32_t v){
 assert(o<0x3000);writes++;
 if(o==0x24){
  assert(v==((1U<<17)|(1U<<8))||v==(1U<<17));
  if(cache_failure!=2)bank[3][0x20/4]&=~v;
  return;
 }
 if(o==0x30){
  assert(v==8&&expect_cached&&starts&&bank[3][0x2400/4]);
  cache_commands++;
  if(cache_failure==3)bank[3][0x20/4]|=1;
  else if(cache_failure==4)bank[3][0x20/4]|=1U<<8;
  else if(cache_failure!=1){memcpy(dest_mem,gpu_dirty,sizeof(dest_mem));bank[3][0x20/4]|=1U<<17;}
  return;
 }
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
  starts++;assert(((uint32_t *)((uint8_t*)allocation+0x4000))[4]==0x10008);assert(flushes==2&&bank[3][0x2430/4]==(expect_cached?0x62000006:0x21000006));
  uint64_t *scratch=(uint64_t *)allocation;
  assert(((scratch[0x3000/8]>>2)&7)==(expect_cached?0:5));
  assert(((scratch[0x3000/8+1]>>2)&7)==(expect_cached?0:5));
  assert(!(scratch[0x3000/8+1]&(1ULL<<54)));
  assert(bank[3][0x2400/4]==0x20000000&&bank[3][0x2404/4]==1);
  assert(bank[3][0x2408/4]==0x888d8f88&&bank[3][0x240c/4]==0x4c8d);
  assert(bank[3][0x18c0/4]==0x2000000&&bank[3][0x18d8/4]==0x83300);

  if(mode==4||mode==6){bank[3][0x18e0/4]=1;bank[3][0x1010/4]=2;return;}
  if(mode==5){bank[3][0x1000/4]=0x20000;bank[3][0x2000/4]=1;return;}
  uint32_t *params=(uint32_t *)((uint8_t *)allocation+0x4200);
  uint32_t *job=(uint32_t *)((uint8_t *)allocation+0x4000);
  unsigned width=params[6],height=params[7],count=width*height;
  unsigned specialized=params[0]==0x04000000&&params[1]==0x05000000&&params[4]==3072&&params[5]==2880&&width==720&&height==1600;
  unsigned local_x=specialized?15:16,pixels=specialized?16:4;
  assert(job[8]==(specialized?0x80000c0e:0x80000c0f)&&job[10]==(specialized?3:(width+63)/64)&&job[11]==(height+3)/4);
  check_shader(specialized);
  unsigned so=params[0]-0x04000000,doff=params[1]-0x05000000;
  unsigned copied=0;
  for(unsigned gy=0;gy<job[11];gy++)for(unsigned gx=0;gx<job[10];gx++)
  for(unsigned ly=0;ly<4;ly++)for(unsigned lx=0;lx<local_x;lx++)
  for(unsigned component=0;component<pixels;component++){
   unsigned y=gy*4+ly,x=(gx*local_x+lx)*pixels+component;
   if(x>=width||y>=height)continue; /* shader's exact bounds before accesses */
   copied++;
   assert(walk(params[0]+y*params[4]+x*4,0)==source_physical(so+y*params[4]+x*4));
   assert(walk(params[1]+y*params[5]+x*4,1)==0x9e000000ULL+doff+y*params[5]+x*4);

   *(uint32_t *)((expect_cached?gpu_dirty:dest_mem)+doff+y*params[5]+x*4)=*(uint32_t *)(source_mem+so+y*params[4]+x*4);
  }
  assert(copied==count);
  if(corrupt)*(uint32_t *)((expect_cached?gpu_dirty:dest_mem)+doff)^=1;

  *(uint32_t *)((uint8_t*)allocation+0x4000)=1;
  if(mode==8)*(uint64_t *)((uint8_t*)allocation+0x5000)=0xa5a55a5adeadbeefULL;
  if(mode==9)*(uint32_t *)((uint8_t*)allocation+0x4000)=0;
  bank[3][0x1000/4]=2;return;
 }
 if(o==0x18e0&&v==0){if(mode!=6)bank[3][0x18e0/4]=0;return;}
 if(o==0x18a0){assert(v==3);if(mode!=6)bank[3][0x1010/4]=0;return;}
 assert(o==0x2430||o==0x2434||o==0x2400||o==0x2404||o==0x2408||o==0x240c||o==0x18c0||o==0x18c4||o==0x18d0||o==0x18d4||o==0x18d8||o==0x18dc);
 bank[3][o/4]=v;
}
'''
tests=r'''
static void reset(unsigned m){
 if(allocation)free(allocation);allocation=0;
 memset(bank,0,sizeof(bank));memset(dest_mem,0x5a,sizeof(dest_mem));
 memset(gpu_dirty,0x5a,sizeof(gpu_dirty));
 for(unsigned i=0;i<sizeof(source_mem)/4;i++)((uint32_t *)source_mem)[i]=i^0x77ccff00;
 mode=m;us=writes=starts=offs=flushes=frees=updates=passed=bad_source=bad_dest=corrupt=noncontiguous=0;
 cache_commands=expect_cached=cache_failure=0;a03_gpu_blit_cached=0;
 a03_gpu_blit_warm=a03_gpu_warm_ready=0;a03_gpu_warm_override=0;
 a03_gpu_pmu=(uintptr_t)bank[0];a03_gpu_aon=(uintptr_t)bank[1];a03_gpu_apb=(uintptr_t)bank[2];a03_gpu_regs=(uintptr_t)bank[3];
 a03_gpu_scratch=0;a03_gpu_scratch_pa=0;a03_gpu_job_poisoned=a03_gpu_job_requested=a03_gpu_owner=0;
 a03_gpu_blit_memory=0;a03_gpu_blit_physical=0;a03_gpu_blit_enabled=1;a03_gpu_blit_frames=0;a03_gpu_blit_verified=0;a03_gpu_blit_verify=1;a03_gpu_blit_completed=0;a03_gpu_blit_ns=0;
 bank[1][0]=1<<11;bank[0][0x500/4]=7<<24;bank[2][1]=bank[2][2]=0x11;bank[2][3]=0x31;
 bank[3][0]=0x90910010;bank[3][0x100/4]=bank[3][0x110/4]=bank[3][0x120/4]=1;
 bank[3][0x18/4]=1;bank[3][0x1c/4]=2;bank[3][0xc4/4]=20;
 bank[3][0x2408/4]=0x13579bdf;bank[3][0x240c/4]=0x2468ace0;bank[3][0x2430/4]=1;
}
static int blit(unsigned w,unsigned h){return a03_gpu_framebuffer_blit((uintptr_t)source_mem,(uintptr_t)dest_mem,0x9e000000,3072,2880,w,h);}
int main(void){
 reset(0);assert(blit(720,1600)==1&&starts==1&&offs==1&&flushes==3&&!a03_gpu_job_poisoned);
 assert(a03_gpu_scratch==0&&a03_gpu_scratch_pa==0&&a03_gpu_blit_frames==1);
 assert(bank[3][0x2400/4]==0&&bank[3][0x2404/4]==0&&bank[3][0x2430/4]==1&&bank[3][0x2408/4]==0x13579bdf);
 us=flushes=starts=offs=0;assert(blit(37,19)==1&&starts==1&&offs==1);
 for(unsigned m=1;m<=7;m++){
  reset(m);int r=blit(37,19);assert(r!=1&&!a03_gpu_job_requested&&!a03_gpu_owner);
  if(m==3||m==5||m==6||m==7){assert(r==-1&&a03_gpu_job_poisoned);unsigned n=writes;assert(blit(37,19)==-1&&writes==n);}
  if(m==4)assert(r==0&&starts==1&&offs==1);
  assert(!starts||!frees);
 }
 reset(0);
 assert(a03_gpu_framebuffer_blit((uintptr_t)source_mem+124,(uintptr_t)dest_mem+2884,0x9e000b44,3072,2880,53,17)==1);
 assert(dest_mem[2883]==0x5a&&dest_mem[2884+53*4]==0x5a);
 assert(!memcmp(source_mem+124,dest_mem+2884,53*4));
 /* Exercise all vector tail lengths on both sides of a 64-pixel group. */
 for(unsigned width=1;width<=270;width++){
  reset(0);expect_cached=1;a03_gpu_blit_control(5);
  assert(a03_gpu_framebuffer_blit((uintptr_t)source_mem+124,(uintptr_t)dest_mem+2884,0x9e000b44,3072,2880,width,5)==1);
  for(unsigned y=0;y<5;y++){
   assert(!memcmp(source_mem+124+y*3072,dest_mem+2884+y*2880,width*4));
   assert(dest_mem[2883+y*2880]==0x5a&&dest_mem[2884+y*2880+width*4]==0x5a);
  }
 }
 reset(0);corrupt=1;assert(blit(37,19)==0&&!a03_gpu_job_poisoned);
 reset(0);bad_source=1;assert(blit(37,19)==0&&!starts);
 reset(0);bad_source=2;assert(blit(37,19)==0&&!starts);
 reset(0);noncontiguous=1;assert(blit(720,1600)==1);
 reset(0);bad_dest=1;assert(blit(37,19)==0&&!starts);
 reset(0);a03_gpu_owner=1;unsigned n=writes;assert(blit(37,19)==-2&&writes==n);a03_gpu_job();assert(writes==n);
 reset(0);a03_gpu_blit_enabled=0;assert(blit(37,19)==0&&!writes);
 for(unsigned w=0;w<=721;w+=721){reset(0);assert(blit(w,19)==0&&!starts);}
 reset(0);assert(blit(37,1601)==0&&!starts);
 reset(0);a03_gpu_blit_control(3);corrupt=1;assert(blit(37,19)==0&&a03_gpu_blit_verified==0); /* fast cannot bypass initial readback */
 reset(0);a03_gpu_blit_control(3);assert(!a03_gpu_blit_verify);
 for(unsigned n=0;n<5;n++){us=flushes=starts=offs=0;assert(blit(37,19)==1);}
 assert(a03_gpu_blit_verified==4&&a03_gpu_blit_completed==5&&a03_gpu_blit_ns>0);
 for(unsigned i=0;i<7;i++)assert(a03_gpu_blit_phase_ns(i)==10);
 assert(a03_gpu_blit_last_ns==80);
 us=flushes=starts=offs=0;corrupt=1;assert(blit(37,19)==1&&a03_gpu_blit_verified==4); /* completed, deliberately not pixel-verified */
 a03_gpu_blit_control(4);assert(a03_gpu_blit_verify);us=flushes=starts=offs=0;corrupt=1;assert(blit(37,19)==0);
 reset(0);expect_cached=1;a03_gpu_blit_control(5);assert(a03_gpu_blit_cached);
 assert(blit(720,1600)==1&&cache_commands==1&&offs==1&&!a03_gpu_job_poisoned);
 for(unsigned i=0;i<3;i++){us=flushes=starts=offs=0;assert(blit(53,17)==1);}
 assert(a03_gpu_blit_verified==4);a03_gpu_blit_control(6);expect_cached=0;
 assert(!a03_gpu_blit_verified&&!a03_gpu_blit_cached);
 for(unsigned failure=1;failure<=4;failure++){
  reset(0);expect_cached=1;a03_gpu_blit_control(5);cache_failure=failure;
  if(failure==2)bank[3][0x20/4]=1U<<17;
  assert(blit(53,17)==-1&&a03_gpu_job_poisoned&&!offs);
  assert(bank[3][0x2400/4]); /* mapping retained until cache ownership proven */
  unsigned before=writes;assert(blit(53,17)==-1&&writes==before);
 }
 reset(0);expect_cached=1;a03_gpu_blit_control(5);a03_gpu_blit_verify=0;
 for(unsigned i=0;i<4;i++){us=flushes=starts=offs=0;assert(blit(53,17)==1);}
 assert(a03_gpu_blit_verified==4);us=flushes=starts=offs=0;corrupt=1;
 a03_gpu_blit_control(6);expect_cached=0;assert(blit(53,17)==0);
 reset(0);expect_cached=1;a03_gpu_blit_control(5);a03_gpu_blit_control(7);
 assert(blit(720,1600)==1&&a03_gpu_warm_ready&&!offs);
 assert(bank[3][0x140/4]==1&&bank[3][0x150/4]==1&&bank[3][0x160/4]==1);
 assert(!bank[3][0x2400/4]&&!bank[3][0x2404/4]);
 us=flushes=starts=0;assert(blit(53,17)==1&&a03_gpu_warm_ready&&!offs);
 a03_gpu_blit_control(0);assert(!a03_gpu_warm_ready&&offs==1&&!a03_gpu_blit_enabled);
 assert(!bank[3][0x140/4]&&!bank[3][0x150/4]&&!bank[3][0x160/4]);
 reset(0);expect_cached=1;a03_gpu_blit_control(5);a03_gpu_blit_control(7);
 assert(blit(53,17)==1);a03_gpu_blit_control(8);
 assert(!a03_gpu_blit_warm&&!a03_gpu_warm_ready&&offs==1);
 reset(0);expect_cached=1;a03_gpu_blit_control(5);a03_gpu_blit_control(7);
 assert(blit(53,17)==1);a03_gpu_blit_control(6);
 assert(!a03_gpu_blit_cached&&!a03_gpu_warm_ready&&offs==1);
 reset(0);expect_cached=1;a03_gpu_blit_control(5);a03_gpu_blit_control(7);
 assert(blit(53,17)==1);us=flushes=starts=0;cache_failure=1;
 assert(blit(53,17)==-1&&a03_gpu_job_poisoned&&!offs);
 unsigned before=writes;a03_gpu_blit_control(0);assert(writes==before);
 reset(0);expect_cached=1;a03_gpu_blit_control(5);a03_gpu_blit_control(7);
 assert(blit(53,17)==1);bank[3][0x200/4]=1;
 us=flushes=starts=0;assert(blit(53,17)==-1&&a03_gpu_job_poisoned&&!offs);
 reset(0);if(allocation)free(allocation);return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='a03-blit-') as temp:
 check=r'''
static void check_shader(unsigned specialized){
 const void *expected=specialized?(const void *)a03_g57_fullscreen_code:(const void *)a03_g57_blit_code;
 assert(!memcmp((uint8_t *)allocation+0x5000,expected,specialized?sizeof(a03_g57_fullscreen_code):sizeof(a03_g57_blit_code)));
}
'''
 temp=Path(temp);c=temp/'test.c';exe=temp/'test';c.write_text(header+layout+check+src+tests)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(c),'-o',str(exe)],check=True)
 subprocess.run([str(exe)],check=True)
print('PASS actual blit geometry/page ownership/strided readback, allocation/AS/timeout/fault/retirement/quarantine/busy; ASan/UBSan, no hardware claim')
