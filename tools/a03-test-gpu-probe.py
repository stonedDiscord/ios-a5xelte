#!/usr/bin/env python3
"""Exercise actual0162 passive GPU gating against fake read-only registers."""
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--source', type=Path, required=True)
a = p.parse_args()
patch = ROOT / 'xnu/a03/0162-a03-passive-gpu-probe.patch'
subprocess.run(['git', 'apply', '--check', str(patch)], cwd=a.source, check=True)
with tempfile.TemporaryDirectory(prefix='a03-gpu-test-') as tmp:
    t = Path(tmp)
    for name in ('bsd/conf/files', 'bsd/conf/Makefile.template', 'bsd/kern/sweet_amfi.c'):
        out = t / name
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(a.source / name, out)
    subprocess.run(['git', 'apply', str(patch)], cwd=t, check=True)
    source = (t / 'bsd/dev/a03_gpu.c').read_text()
    source = '\n'.join(line for line in source.splitlines() if not line.startswith('#include'))
    assert 'a03_gpu.o_CFLAGS_ADD += -mgeneral-regs-only' in (t/'bsd/conf/Makefile.template').read_text()
    assert 'else if(!strcmp(command,"gpu"))a03_gpu_probe();' in (t/'bsd/kern/sweet_amfi.c').read_text()
    for forbidden in ('ml_io_unmap(', 'write32(', 'IOWrite', 'IODelay(', 'IOSleep(', 'while (', 'for ('):
        assert forbidden not in source, forbidden
    header = r'''
#include <stdint.h>
#include <stdarg.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
#define ARM64_BOARD_CONFIG_SWEET 1
typedef uintptr_t vm_offset_t;
typedef unsigned long vm_size_t;
static uint32_t pmu[1024], aon[1024], apb[1024], gpu[1024];
static unsigned maps[4], logs, fail;
static uint32_t snapshot[4][1024];
vm_offset_t ml_io_map(vm_offset_t addr, vm_size_t size) {
 assert(size==0x1000);
 unsigned n=addr==0x64020000?0:addr==0x64000000?1:addr==0x23000000?2:addr==0x23100000?3:4;
 assert(n<4);maps[n]++;if(fail==n+1)return 0;
 return (uintptr_t)(n==0?pmu:n==1?aon:n==2?apb:gpu);
}
static int capture(const char *fmt, ...) { assert(fmt && !strstr(fmt,"\\n"));logs++;return 0; }
#define printf capture
'''
    tests = r'''
static void reset(void) {
 memset(maps,0,sizeof(maps));memset(pmu,0,sizeof(pmu));memset(aon,0,sizeof(aon));
 memset(apb,0,sizeof(apb));memset(gpu,0,sizeof(gpu));
 a03_gpu_pmu=a03_gpu_aon=a03_gpu_apb=a03_gpu_regs=0;logs=fail=0;
 aon[0]=1<<11;apb[1]=apb[2]=apb[3]=1;gpu[0]=0x90930000;
}
static void save(void) {memcpy(snapshot[0],pmu,sizeof(pmu));memcpy(snapshot[1],aon,sizeof(aon));memcpy(snapshot[2],apb,sizeof(apb));memcpy(snapshot[3],gpu,sizeof(gpu));}
static void unchanged(void) {assert(!memcmp(snapshot[0],pmu,sizeof(pmu)));assert(!memcmp(snapshot[1],aon,sizeof(aon)));assert(!memcmp(snapshot[2],apb,sizeof(apb)));assert(!memcmp(snapshot[3],gpu,sizeof(gpu)));}
int main(void) {
 reset();save();a03_gpu_probe();unchanged();assert(maps[0]==1&&maps[1]==1&&maps[2]==1&&maps[3]==1&&logs==4);
 a03_gpu_probe();unchanged();assert(maps[0]==1&&maps[1]==1&&maps[2]==1&&maps[3]==1&&logs==8);
 for(unsigned bit=0;bit<10;bit++){reset();pmu[0x500/4]=1U<<(bit<5?24+bit:16+bit-5);save();a03_gpu_probe();unchanged();assert(!maps[2]&&!maps[3]&&logs==2);}
 reset();pmu[0x2c4/4]=1<<25;save();a03_gpu_probe();unchanged();assert(!maps[2]&&!maps[3]);
 reset();pmu[0x2c4/4]=1<<24;save();a03_gpu_probe();unchanged();assert(!maps[2]&&!maps[3]);
 reset();aon[0]=0;save();a03_gpu_probe();unchanged();assert(!maps[2]&&!maps[3]);
 for(unsigned i=1;i<=3;i++){reset();apb[i]=0;save();a03_gpu_probe();unchanged();assert(maps[2]&&!maps[3]&&logs==3);}
 for(unsigned i=1;i<=4;i++){reset();fail=i;save();a03_gpu_probe();unchanged();if(i<4)assert(!maps[3]);}
 reset();gpu[0]=0;save();a03_gpu_probe();unchanged();assert(logs==3);
 reset();gpu[0]=UINT32_MAX;save();a03_gpu_probe();unchanged();assert(logs==3);
 /* Exhaust every combination of relevant power/bus bits. */
 for(unsigned off=0;off<2;off++)for(unsigned state=0;state<1024;state++)for(unsigned bus=0;bus<2;bus++)
 assert(a03_gpu_domain_accessible(off<<25,((state&31)<<24)|((state>>5)<<16),bus<<11)==(!off&&!state&&bus));
 return 0;
}
'''
    c = t / 'test.c'
    c.write_text(header + source + tests)
    subprocess.run(['clang', '-std=c11', '-Wall', '-Wextra', '-Werror', '-fsanitize=address,undefined', str(c), '-o', str(t/'test')], check=True)
    subprocess.run([str(t/'test')], check=True)
    subprocess.run(['git','apply','--reverse','--check',str(patch)],cwd=t,check=True)
print('PASS actual passive GPU probe: read-only fake MMIO, power/bus/clock gates, map failures/reuse, invalid IDs, ASan/UBSan, patch/reverse')
