#!/usr/bin/env python3
"""Exercise actual explicit384/512MHz switching guards and rollback; no phone."""
import argparse
from pathlib import Path
import subprocess,tempfile
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);a=p.parse_args()
s=(a.source/'bsd/dev/a03_gpu.c').read_text();start=s.index('static void a03_gpu_clock_rate(');end=s.index('void a03_gpu_blit_control',start);source=s[start:end]
pre=r'''
#include <stdint.h>
#include <string.h>
#include <assert.h>
typedef uintptr_t vm_offset_t;
static uint32_t bank[7][4096];
static vm_offset_t a03_gpu_regs,a03_gpu_apb,a03_gpu_dvfs,a03_gpu_pll,a03_gpu_pmu,a03_gpu_aon;
static unsigned a03_gpu_job_poisoned,a03_gpu_blit_enabled,a03_gpu_warm_ready,a03_gpu_clock_selector=1,a03_gpu_blit_verified;
static unsigned writes,fail_at,always_fail,updates,supply_pd,supply_voltage;
static uint64_t parent;
static uint32_t a03_gpu_read(vm_offset_t b,unsigned o){assert(b&&o<0x4000);return *(uint32_t *)(b+o);}
static int a03_gpu_update(vm_offset_t b,unsigned o,uint32_t mask,uint32_t v){
 assert(b==a03_gpu_apb&&(o==4||o==8||o==12));assert(mask==1||mask==0x70);assert(o!=12||mask==1);
 updates++;if(updates==fail_at||always_fail)return 0;
 uint32_t *r=(uint32_t *)(b+o);*r=(*r&~mask)|(v&mask);writes++;return 1;
}
static void delay(unsigned n){assert(n==400);}
static int a03_gpu_supply_status(uint32_t*p,uint32_t*v){*p=supply_pd;*v=supply_voltage;return 1;}
static uint64_t a03_gpu_twpll_rate(uint32_t a,uint32_t b,uint32_t c){(void)a;(void)b;(void)c;return parent;}
static int a03_gpu_domain_accessible(uint32_t f,uint32_t s,uint32_t b){return !(f&0x3000000)&&!(s&0x1f0000)&&(b&0x800);}
static int a03_gpu_slot_idle(void){return !a03_gpu_read(a03_gpu_regs,0x18e0)&&!a03_gpu_read(a03_gpu_regs,0x1010);}
'''
tests=r'''
static void reset(void){
 memset(bank,0,sizeof(bank));writes=fail_at=always_fail=updates=supply_pd=a03_gpu_job_poisoned=a03_gpu_blit_enabled=a03_gpu_warm_ready=0;
 supply_voltage=320;parent=1535999998ULL;a03_gpu_clock_selector=1;a03_gpu_blit_verified=9;
 a03_gpu_regs=(uintptr_t)bank[0];a03_gpu_apb=(uintptr_t)bank[1];a03_gpu_dvfs=(uintptr_t)bank[2];a03_gpu_pll=(uintptr_t)bank[3];a03_gpu_pmu=(uintptr_t)bank[4];a03_gpu_aon=(uintptr_t)bank[5];
 bank[0][0]=0x90910010;bank[1][1]=bank[1][2]=0xa0000011;bank[1][3]=0xa0000031;bank[3][0]=1<<18;bank[4][0x500/4]=7<<24;bank[5][0]=0x800;
}
static void refused(void){a03_gpu_clock_rate(2);assert(!writes&&a03_gpu_clock_selector==1&&a03_gpu_blit_verified==9);}
int main(void){
 reset();a03_gpu_clock_rate(2);assert(a03_gpu_clock_selector==2&&a03_gpu_blit_verified==0&&writes==8&&!a03_gpu_job_poisoned);
 assert(bank[1][1]==0xa0000021&&bank[1][2]==0xa0000021&&bank[1][3]==0xa0000031);
 unsigned n=writes;a03_gpu_clock_rate(2);assert(writes==n);
 a03_gpu_clock_rate(1);assert(a03_gpu_clock_selector==1&&bank[1][1]==0xa0000011&&bank[1][2]==0xa0000011);
 for(unsigned v=0;v<512;v++){reset();supply_voltage=v;if(v!=320)refused();}
 reset();supply_pd=8;refused();reset();a03_gpu_blit_enabled=1;refused();reset();a03_gpu_warm_ready=1;refused();reset();a03_gpu_job_poisoned=1;refused();
 reset();bank[3][0]=0;refused();reset();parent=1534999999;refused();reset();parent=1537000001;refused();reset();bank[2][0x38/4]=0x80000;refused();
 const unsigned offsets[]={0x140,0x144,0x150,0x154,0x160,0x164,0x200,0x204,0x210,0x214,0x220,0x224,0x2400,0x2404,0x2428,0x241c,0x2000,0x18e0,0x1010};
 for(unsigned i=0;i<sizeof(offsets)/sizeof(offsets[0]);i++){reset();bank[0][offsets[i]/4]=1;refused();}
 for(unsigned v=1;v<=0x100;v<<=1){if(!(v&0x181))continue;reset();bank[0][0x20/4]=v;refused();}
 for(unsigned r=1;r<=3;r++){reset();bank[1][r]^=0x10;refused();}
 for(unsigned f=1;f<=8;f++){
  reset();fail_at=f;a03_gpu_clock_rate(2);assert(a03_gpu_clock_selector==1&&!a03_gpu_job_poisoned&&a03_gpu_blit_verified==9);
  assert(bank[1][1]==0xa0000011&&bank[1][2]==0xa0000011&&bank[1][3]==0xa0000031);
 }
 reset();always_fail=1;a03_gpu_clock_rate(2);assert(a03_gpu_job_poisoned&&a03_gpu_clock_selector==1);
 reset();a03_gpu_clock_rate(3);assert(!writes);
 return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='a03-rate-') as t:
 t=Path(t);c=t/'test.c';c.write_text(pre+source+tests)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(c),'-o',str(t/'test')],check=True)
 subprocess.run([str(t/'test')],check=True)
print('PASS actual clock switch idle/supply/parent/ownership guards, masked leaf writes, all rollback stages and quarantine; ASan/UBSan')
