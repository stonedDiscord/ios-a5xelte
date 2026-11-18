#!/usr/bin/env python3
"""Exercise the actual idle-A75 selector and patch against a BOOT0093 tree."""
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--source', type=Path, required=True)
a = p.parse_args()
patch = ROOT / 'xnu/a03/0161-a03-prefer-idle-a75.patch'
name = Path('osfmk/kern/sched_prim.c')
subprocess.run(['git', 'apply', '--check', str(patch)], cwd=a.source, check=True)
with tempfile.TemporaryDirectory() as tmp:
    t = Path(tmp)
    (t / name).parent.mkdir(parents=True)
    shutil.copyfile(a.source / name, t / name)
    subprocess.run(['git', 'apply', str(patch)], cwd=t, check=True)
    source = (t / name).read_text()
    start = source.index('static boolean_t a03_prefer_a75')
    selector = source[start:source.index('#endif', start)]
    choose = source[source.index('processor_t\nchoose_processor('):]
    assert choose.index('a03_choose_idle_a75(pset, thread)') < choose.index('processor = processor->processor_primary')
    assert 'PE_parse_boot_argn("a03_prefer_a75"' in source
    for mutation in ('thread_bind(', 'processor_start(', 'sched_update_recommended_cores(', 'thread_setrun('):
        assert mutation not in selector
    header = '''#include <assert.h>
#include <stdint.h>
#define FALSE 0
#define TRUE 1
#define BASEPRI_RTQUEUES 97
#define PROCESSOR_NULL ((processor_t)0)
#define PROCESSOR_IDLE 0
typedef int boolean_t;
struct processor { unsigned cpu_id; };
typedef struct processor *processor_t;
struct pset {uint64_t cpu_state_map[1],primary_map,recommended_bitmask,pending_AST_URGENT_cpu_mask,pending_AST_PREEMPT_cpu_mask;};
typedef struct pset *processor_set_t;
struct thread {processor_t bound_processor; int sched_pri;};
typedef struct thread *thread_t;
typedef struct {unsigned num_cpus;struct {unsigned phys_id;}cpus[8];} ml_topology_info_t;
static ml_topology_info_t topology;
static const ml_topology_info_t *ml_get_topology_info(void){return &topology;}
static int lsb_first(uint64_t bits){return bits?__builtin_ctzll(bits):-1;}
static struct processor cpus[8];
static processor_t processor_array[8];
'''
    tests = '''int main(void){
struct pset p={.primary_map=255,.recommended_bitmask=255};
struct thread t={0};topology.num_cpus=8;
for(unsigned i=0;i<8;i++){cpus[i].cpu_id=i;processor_array[i]=&cpus[i];topology.cpus[i].phys_id=i<<8;}
/* Exhaust all idle, recommendation and pending-AST masks. */
a03_prefer_a75=TRUE;
for(unsigned idle=0;idle<256;idle++)for(unsigned rec=0;rec<256;rec++)for(unsigned ast=0;ast<4;ast++){
p.cpu_state_map[0]=idle;p.recommended_bitmask=rec;
p.pending_AST_URGENT_cpu_mask=(uint64_t)ast<<6;
p.pending_AST_PREEMPT_cpu_mask=0;
uint64_t eligible=idle&rec&~p.pending_AST_URGENT_cpu_mask&192;
processor_t expected=eligible?&cpus[lsb_first(eligible)]:0;
assert(a03_choose_idle_a75(&p,&t)==expected);
p.pending_AST_PREEMPT_cpu_mask=p.pending_AST_URGENT_cpu_mask;
p.pending_AST_URGENT_cpu_mask=0;
assert(a03_choose_idle_a75(&p,&t)==expected);
}
p.cpu_state_map[0]=p.recommended_bitmask=255;p.pending_AST_PREEMPT_cpu_mask=0;
assert(a03_choose_idle_a75(&p,&t)==&cpus[6]);
p.primary_map=128;assert(a03_choose_idle_a75(&p,&t)==&cpus[7]);
p.primary_map=63;assert(!a03_choose_idle_a75(&p,&t));p.primary_map=255;
a03_prefer_a75=FALSE;assert(!a03_choose_idle_a75(&p,&t));a03_prefer_a75=TRUE;
t.bound_processor=&cpus[0];assert(!a03_choose_idle_a75(&p,&t));t.bound_processor=0;
t.sched_pri=97;assert(!a03_choose_idle_a75(&p,&t));t.sched_pri=0;
for(unsigned n=0;n<=9;n++){topology.num_cpus=n;assert((a03_choose_idle_a75(&p,&t)!=0)==(n==8));}
topology.num_cpus=8;topology.cpus[6].phys_id=0;assert(!a03_choose_idle_a75(&p,&t));
topology.cpus[6].phys_id=0x600;topology.cpus[7].phys_id=0;assert(!a03_choose_idle_a75(&p,&t));
}'''
    c = t / 'test.c'
    c.write_text(header + selector + tests)
    subprocess.run(['clang', '-std=c11', '-Wall', '-Wextra', '-Werror', '-fsanitize=address,undefined', str(c), '-o', str(t / 'test')], check=True)
    subprocess.run([str(t / 'test')], check=True)
    subprocess.run(['git', 'apply', '--reverse', '--check', str(patch)], cwd=t, check=True)
print('PASS actual idle-A75 selector: 262144 mask combinations, bound/RT/off/topology guards, ASan+UBSan and patch/reverse')
