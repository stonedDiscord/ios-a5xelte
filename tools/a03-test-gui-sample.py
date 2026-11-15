#!/usr/bin/env python3
"""Exercise the actual sampler process selection, opt-in and bounded worker."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parent.parent
patch=(root/'xnu/a03/0129-a03-bounded-gui-thread-snapshots.patch').read_text()
part=patch.split('+++ b/bsd/kern/sweet_amfi.c',1)[1].split('--- a/bsd/kern/bsd_init.c',1)[0]
s='\n'.join(l[1:] for l in part.splitlines() if l.startswith('+'))
s=s[s.index('extern void a03_sample_task'):]
pre=r'''
#include <cassert>
#include <cstdint>
#include <cstring>
#include <cstdio>
#define __unused __attribute__((unused))
#define PROC_RETURNED 0
#define TASK_NULL nullptr
#define PZERO 0
#define PROC_ALLPROCLIST 1
#define KERN_SUCCESS 0
using task_t=void*;using thread_t=void*;using wait_result_t=int;using kern_return_t=int;
struct proc{const char *name;task_t task;};using proc_t=proc*;
unsigned enabled=0,starts=0,releases=0,samples=0,sleeps=0,iterations=0;int hz=100;
int proc_pid(proc_t){return 25;}void proc_name(int,char *out,unsigned n);
proc_t current=nullptr;
void proc_name(int,char *out,unsigned n){snprintf(out,n,"%s",current->name);}
task_t proc_task(proc_t p){return p->task;}
void a03_sample_task(const char *name,int pid,task_t task){assert(pid==25&&task);assert(!strcmp(name,"SpringBoard")||!strcmp(name,"backboardd"));samples++;}
int tsleep(void*,int,const char*,int ticks){assert(ticks==(sleeps?120:180)*hz);sleeps++;return 0;}
void proc_iterate(unsigned flags,int(*cb)(proc_t,void*),void *arg,void*,void*){assert(flags==1);iterations++;proc ps[]={{"SpringBoard",(void*)1},{"backboardd",(void*)2},{"other",(void*)3},{"SpringBoard",nullptr}};for(auto &p:ps){current=&p;assert(cb(&p,arg)==0);}}
void PE_parse_boot_argn(const char*,uint32_t *out,unsigned){*out=enabled;}
int kernel_thread_start(void(*fn)(void*,int),void*,thread_t *out){assert(fn);starts++;*out=(void*)4;return 0;}
void thread_deallocate(thread_t t){assert(t==(void*)4);releases++;}
'''
tests=r'''
int main(){a03_gui_sample_start();assert(!starts);enabled=2;a03_gui_sample_start();assert(!starts);enabled=1;a03_gui_sample_start();assert(starts==1&&releases==1);a03_sample_worker(nullptr,0);assert(iterations==4&&samples==8&&sleeps==5);puts("A03 actual GUI sampler: opt-in, selected processes, null tasks, four passes and bounded timing PASS");}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'t.cpp').write_text(pre+s+tests)
 subprocess.run(['c++','-std=c++17','-Wall','-Wextra','-Werror',str(p/'t.cpp'),'-o',str(p/'t')],check=True)
 subprocess.run([str(p/'t')],check=True)
# Read-side invariants are in the compiled real kernel snapshot implementation.
part=patch.split('+++ b/osfmk/kern/exception.c',1)[1].split('--- a/bsd/kern/sweet_amfi.c',1)[0]
s='\n'.join(l[1:] for l in part.splitlines() if l.startswith('+'))
assert 'snap[24]' in s and 'i < 12' in s
assert s.index('task_unlock(task)') < s.index('vm_map_read_user')
assert 'thread_reference(thread)' in s and 'thread_deallocate(snap[t].thread)' in s
assert 'get_task_map_reference(task)' in s and 'vm_map_deallocate(map)' in s
assert 'task_suspend' not in s and 'vm_map_write_user' not in s
