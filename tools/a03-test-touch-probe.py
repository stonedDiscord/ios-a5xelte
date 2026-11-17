#!/usr/bin/env python3
"""Check actual 0146 probe command gates and register restoration on the host.

Only the ARM dsb instruction is substituted for host compilation. This fake
MMIO test cannot establish pinmux, clocks, bus response or real device access.
"""
from pathlib import Path
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[1]
patch=(ROOT/'xnu/a03/0146-a03-explicit-jadard-rom-probe.patch').read_text()
s='\n'.join(line[1:] for line in patch.splitlines() if line.startswith('+') and not line.startswith('+++'))
s=s[s.index('/* Explicit A03 SPI3'):s.index('/* Bounded polling SPI primitives')]
s=s[:s.index('extern void a03_touch_probe', 1)]
s=s.replace('#include "a03_jd9365t_spi.h"','#include "shim/a03/jd9365t-spi.h"')
s=s.replace('__asm__ volatile("dsb sy" ::: "memory");','/* host-only dsb stand-in */')
prefix=r'''
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
typedef uintptr_t vm_offset_t;
#define __unused __attribute__((unused))
static uint32_t apb[3072],clockregs[1024],spiregs[1024];
static unsigned maps,delays;static int mapfail;
static vm_offset_t ml_io_map(vm_offset_t p,size_t n){maps++;if(mapfail)return 0;assert(n==0x1000||n==0x3000);if(p==0x20000000)return (uintptr_t)apb;if(p==0x20010000)return (uintptr_t)clockregs;assert(p==0x20150000);return (uintptr_t)spiregs;}
static void IODelay(unsigned n){delays+=n;}
'''
test=r'''
int main(void){
a03_touch_probe("invalid");a03_touch_probe("rom extra");assert(!maps);
a03_touch_probe("status");assert(maps==2&&!apb[0x400]&&!clockregs[0x58/4]);
clockregs[0x58/4]=0x302;apb[0]=0x100;spiregs[0x28/4]=0x300;spiregs[0x34/4]=0;
unsigned regs[]={4,8,0xc,0x10,0x14,0x18,0x1c,0x20,0x40,0x4c,0x54,0x58,0x5c,0x60};
for(unsigned i=0;i<sizeof(regs)/sizeof(regs[0]);i++)spiregs[regs[i]/4]=0xabc000+i;
uint32_t saved[1024];memcpy(saved,spiregs,sizeof(saved));
a03_touch_probe("rom");assert(clockregs[0x58/4]==0x302);assert(maps==3);assert(delays==10);
for(unsigned i=0;i<sizeof(regs)/sizeof(regs[0]);i++)assert(spiregs[regs[i]/4]==saved[regs[i]/4]);
/* Transfer timeout still restores every saved control register and clock. */
spiregs[0x28/4]=0;a03_touch_probe("rom");assert(delays==20020&&clockregs[0x58/4]==0x302);
for(unsigned i=0;i<sizeof(regs)/sizeof(regs[0]);i++)assert(spiregs[regs[i]/4]==saved[regs[i]/4]);
/* Refuse busy without changing control state. */
spiregs[0x34/4]=0x100;a03_touch_probe("rom");assert(clockregs[0x58/4]==0x302);
for(unsigned i=0;i<sizeof(regs)/sizeof(regs[0]);i++)assert(spiregs[regs[i]/4]==saved[regs[i]/4]);
/* Map failure exits before dereferencing a missing MMIO mapping. */
a03_touch_apb=a03_touch_clk=0;mapfail=1;a03_touch_probe("rom");
puts("PASS actual touch probe: exact commands, status read-only, ROM control restore, timeout/busy/map-failure cleanup");}
'''
with tempfile.TemporaryDirectory(prefix='a03-touchprobe-') as d:
 p=Path(d)/'test.c';p.write_text(prefix+s+test)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I',str(ROOT),str(p),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
