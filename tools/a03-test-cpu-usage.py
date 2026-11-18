#!/usr/bin/env python3
"""Exercise actual0160 bounded CPU observer with fake recount sources."""
from pathlib import Path
import subprocess,tempfile,shutil
ROOT=Path(__file__).resolve().parents[1]
patch=ROOT/'xnu/a03/0160-a03-readonly-per-cpu-usage.patch'
import argparse
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);a=p.parse_args()
subprocess.run(['git','apply','--check',str(patch)],cwd=a.source,check=True)
with tempfile.TemporaryDirectory() as tmp:
    t=Path(tmp)
    for name in ('osfmk/kern/processor.c','bsd/kern/sweet_amfi.c','iokit/KernelConfigTables.cpp'):
        target=t/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a.source/name,target)
    subprocess.run(['git','apply',str(patch)],cwd=t,check=True)
    s=(t/'osfmk/kern/processor.c').read_text()
    start=s.index('/* Same recount-backed tick source')
    end=s.index('#endif',start);s=s[start:end]
    for forbidden in ('processor_start(', 'thread_bind(', 'sched_processor_enable('):assert forbidden not in s
    header='''#include <stdint.h>
#include <assert.h>
#define MAX_CPUS 8
#define CPU_STATE_MAX 4
#define CPU_STATE_USER 0
#define CPU_STATE_SYSTEM 1
#define CPU_STATE_IDLE 2
#define CPU_STATE_NICE 3
#define LCK_GRP_NULL 0
#define PROCESSOR_NULL 0
typedef uint32_t natural_t;
struct processor {unsigned cpu_id;};typedef struct processor* processor_t;
static struct processor storage[8];static processor_t processor_array[8];
static unsigned processor_count,processor_list_lock,locked,calls,printed;
static void simple_lock(unsigned*p,int g){(void)p;(void)g;assert(!locked);locked=1;}
static void simple_unlock(unsigned*p){(void)p;assert(locked);locked=0;}
static void processor_cpu_load_info(processor_t p,natural_t*t){assert(locked);calls++;t[0]+=p->cpu_id+1;t[1]+=2;t[2]+=3;}
#define printf(...) (assert(!locked), printed++)
'''
    tests='''int main(){
for(unsigned count=0;count<=12;count++){
 processor_count=count;calls=printed=0;
 for(unsigned i=0;i<8;i++){storage[i].cpu_id=i;processor_array[i]=&storage[i];}
 a03_cpu_usage_probe();unsigned bounded=count>8?8:count;
 assert(!locked&&calls==bounded&&printed==bounded+1);
}
processor_count=8;processor_array[6]=0;calls=printed=0;
a03_cpu_usage_probe();assert(calls==7&&printed==9&&!locked);
}'''
    f=t/'test.c';f.write_text(header+s+tests)
    subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(f),'-o',str(t/'test')],check=True)
    subprocess.run([str(t/'test')],check=True)
    table=(t/'iokit/KernelConfigTables.cpp').read_text();assert "'IONameMatch'     = 'arm,cortex-a75'" in table
    assert 'else if(!strcmp(command,"cpus"))a03_cpu_usage_probe();' in (t/'bsd/kern/sweet_amfi.c').read_text()
    subprocess.run(['git','apply','--reverse','--check',str(patch)],cwd=t,check=True)
print('PASS actual CPU observer bounds/locking/no scheduler mutations ASan+UBSan, A75 match, patch/reverse')
