#!/usr/bin/env python3
"""Exercise actual DREAMLTE overlay helpers on the host; no hardware claim.

Adapted from build/a03-bringup f1e1601 regression cases. Compile the helper
bodies extracted from the staged contextual patch, with fake kernel APIs.
"""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
PATCH = ROOT / 'xnu/dreamlte/0205-dreamlte-a03-portable-bringup.patch'


def added_source(path):
    part = PATCH.read_text().split('+++ b/' + path + '\n', 1)[1].split('--- a/', 1)[0]
    return '\n'.join(line[1:] for line in part.splitlines() if line.startswith('+'))


def run(name, path, start, end, language, header, checks):
    source = added_source(path).split(start, 1)[1].split(end, 1)[0]
    source = start + source
    with tempfile.TemporaryDirectory(prefix='dreamlte-test-') as directory:
        d = Path(directory)
        file = d / ('test.' + language)
        file.write_text(header + source + checks)
        compiler = ['c++', '-std=c++17'] if language == 'cpp' else ['cc', '-std=c11']
        subprocess.run(compiler + ['-Wall', '-Wextra', '-Werror', str(file), '-o', str(d/'test')], check=True)
        subprocess.run([str(d/'test')], check=True)
    print(name + ': PASS')


def main():
    run('sandbox', 'bsd/kern/sweet_amfi.c',
        'static int\ndreamlte_sandbox_check_syscall', '\n#else', 'c',
        r'''
#include <assert.h>
#include <stdint.h>
#include <stdbool.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#undef ENOTSUP
#define ENOTSUP 45
typedef uintptr_t user_addr_t;
struct proc {char p_comm[17];};
static unsigned reads,writes,logs;static int input_error,output_error;static uintptr_t output_address=0x2000;static uint64_t output_value=99;
static int copyin(user_addr_t a,void *d,size_t n){reads++;assert(a==0x1000&&n==8);if(input_error)return input_error;memcpy(d,&output_address,n);return 0;}
static int copyout(const void *v,user_addr_t a,size_t n){writes++;assert(a==0x2000&&n==8);if(output_error)return output_error;memcpy(&output_value,v,n);return 0;}
static int proc_pid(struct proc *p){(void)p;return 42;}
static void proc_name(int pid,char *buf,size_t len){assert(pid==42);snprintf(buf,len,"launchd");}
static int logline(const char *f,...){(void)f;logs++;return 0;}
#define printf logline
''',
        r'''
#undef printf
int main(void){struct proc p={"launchd"};
int unsupported[]={-1,0,1,3,4,5,6,0x43,999};
for(unsigned i=0;i<sizeof(unsupported)/sizeof(*unsupported);i++)assert(dreamlte_sandbox_check_syscall(&p,unsupported[i],0x1000)==ENOTSUP);
assert(reads==0&&writes==0);
input_error=EFAULT;assert(dreamlte_sandbox_check_syscall(&p,2,0x1000)==EFAULT&&writes==0);
input_error=0;output_address=0;assert(dreamlte_sandbox_check_syscall(&p,2,0x1000)==EFAULT&&writes==0);
output_address=0x2000;output_error=EFAULT;assert(dreamlte_sandbox_check_syscall(&p,2,0x1000)==EFAULT&&output_value==99);
output_error=0;assert(dreamlte_sandbox_check_syscall(&p,2,0x1000)==0&&output_value==0);
for(unsigned i=0;i<1000;i++){output_value=99;assert(dreamlte_sandbox_check_syscall(&p,2,0x1000)==0&&output_value==0);}assert(logs==32);
puts("DREAMLTE actual lab sandbox op2: unsupported operations, copyin/copyout faults, null output, full64-bit allow and logging cap PASS");}
''')
    run('work interval', 'bsd/kern/sweet_amfi.c',
        'static TUNABLE(uint32_t, dreamlte_work_interval', '\n#else', 'cpp',
        r'''
#include <cassert>
#include <cstdio>
#include <cerrno>
#include <cstdint>
#define TUNABLE(type,name,key,value) type name=value
#define PRIV_WORK_INTERVAL 77
#define __ATOMIC_RELAXED 0
using kauth_cred_t=void*;
void *cred=(void*)1; bool entitled=false; unsigned queries=0;
void *kauth_cred_get(){return cred;} void *current_proc(){return (void*)2;}
void *sweet_proc_entitlements(void *p){assert(p==(void*)2);return (void*)3;}
bool sweet_entitlements_bool(void *e,const char*){assert(e==(void*)3);queries++;return entitled;}
void proc_selfname(char *p,unsigned n){snprintf(p,n,"backboardd");}
''',
        r'''
int main(){
assert(dreamlte_sandbox_priv_grant(cred,PRIV_WORK_INTERVAL)==EPERM&&queries==0);
dreamlte_work_interval=1;
assert(dreamlte_sandbox_priv_grant(cred,99)==EPERM&&queries==0);
assert(dreamlte_sandbox_priv_grant((void*)4,PRIV_WORK_INTERVAL)==EPERM&&queries==0);
assert(dreamlte_sandbox_priv_grant(cred,PRIV_WORK_INTERVAL)==EPERM&&queries==1);
entitled=true;
for(int i=0;i<20;i++)assert(dreamlte_sandbox_priv_grant(cred,PRIV_WORK_INTERVAL)==0);
entitled=false;assert(dreamlte_sandbox_priv_grant(cred,PRIV_WORK_INTERVAL)==EPERM);
puts("DREAMLTE actual MAC grant: opt-in/current credential/exact privilege/boolean entitlement and bounded reports PASS");}
''')
    run('HOST budget', 'osfmk/kern/host.c',
        'boolean_t dreamlte_host_log_allowed', '\n#endif', 'c',
        r'''#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
typedef int boolean_t;
#define TRUE 1
#define FALSE 0
''',
        r'''
int main(void){
assert(!dreamlte_host_log_allowed(99,FALSE));assert(!dreamlte_host_log_allowed(99,TRUE));
for(unsigned site=0;site<4;site++){
 for(unsigned i=0;i<8;i++)assert(dreamlte_host_log_allowed(site,FALSE));
 for(unsigned i=0;i<10000;i++)assert(!dreamlte_host_log_allowed(site,FALSE));
}
for(unsigned i=0;i<16;i++)assert(dreamlte_host_log_allowed(i%4,TRUE));
for(unsigned i=0;i<10000;i++)assert(!dreamlte_host_log_allowed(i%4,TRUE));
puts("DREAMLTE actual HOST diagnostics: four independent8-report budgets, separate16 failures, saturation PASS");}
''')
    run('crash selection', 'bsd/kern/kern_exit.c',
        'static bool\ndreamlte_should_log_daemon_crash', '\n#endif', 'c',
        r'''
#include <assert.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdatomic.h>
#include <string.h>
#include <signal.h>
#include <stdio.h>
static uint32_t enabled;
static void PE_parse_boot_argn(const char *arg,void *value,unsigned size) {
 assert(!strcmp(arg,"dreamltecrash_log") && size==sizeof(enabled));
 memcpy(value,&enabled,size);
}
''',
        r'''
int main(void) {
 const char *names[]={"watchdogd","backboardd","SpringBoard","launchd","xpcproxy",
 "bluetoothd","identityservices","fairplayd.H2","mediaserverd","configd","lockdownd","analyticsd","dmd","tccd"};
 assert(!dreamlte_should_log_daemon_crash("mediaserverd",SIGABRT));
 enabled=2;assert(!dreamlte_should_log_daemon_crash("mediaserverd",SIGABRT));enabled=1;
 assert(!dreamlte_should_log_daemon_crash("unknown",SIGABRT));
 assert(!dreamlte_should_log_daemon_crash("watchdogd",SIGTERM));
 for(unsigned i=0;i<sizeof(names)/sizeof(names[0]);i++) {
  assert(strlen(names[i])<=16);
  assert(dreamlte_should_log_daemon_crash(names[i],SIGABRT));
  assert(dreamlte_should_log_daemon_crash(names[i],SIGSEGV));
  for(unsigned j=0;j<10000;j++)assert(!dreamlte_should_log_daemon_crash(names[i],SIGTRAP));
 }
 assert(!dreamlte_should_log_daemon_crash("fairplayd",SIGKILL));
 puts("DREAMLTE crash log actual-source boot gate/name selection/two-report saturation PASS");
}
''')
    run('crash annotations', 'osfmk/kern/exception.c',
        '/* Read current-task', 'void dreamlte_daemon_crash_log', 'c',
        r'''
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <string.h>
#include <stdio.h>
#include <stdarg.h>
#include <assert.h>
typedef uintptr_t user_addr_t;
typedef size_t vm_size_t;
#define MH_MAGIC_64 0xfeedfacf
#define CPU_TYPE_ARM64 0x100000c
#define LC_SEGMENT_64 0x19
struct mach_header_64 {uint32_t magic,cputype,cpusubtype,filetype,ncmds,sizeofcmds,flags,reserved;};
struct load_command {uint32_t cmd,cmdsize;};
struct segment_command_64 {uint32_t cmd,cmdsize;char segname[16];uint64_t vmaddr,vmsize,fileoff,filesize;uint32_t maxprot,initprot,nsects,flags;};
struct section_64 {char sectname[16],segname[16];uint64_t addr,size;uint32_t offset,align,reloff,nreloc,flags,reserved1,reserved2,reserved3;};
static unsigned char memory[16384];
static unsigned reads, messages;
static char output[2048];
static int copyin(user_addr_t address,void *out,size_t size) {
 reads++;
 if(address<0x100000 || size>sizeof(memory) || address-0x100000>sizeof(memory)-size)return 1;
 memcpy(out,memory+address-0x100000,size);return 0;
}
static int copyinstr(user_addr_t address,char *out,size_t size,vm_size_t *copied) {
 for(size_t i=0;i<size;i++){if(copyin(address+i,out+i,1))return 1;if(!out[i]){*copied=i+1;return 0;}}
 return 1;
}
static int logline(const char *format,...) {
 va_list ap;va_start(ap,format);int result=vsnprintf(output+strlen(output),sizeof(output)-strlen(output),format,ap);va_end(ap);
 if(strstr(format,"annotation%u:"))messages++;
 return result;
}
#define printf logline
''',
        r'''
#undef printf
int main(void) {
 struct mach_header_64 *mh=(void*)memory;
 struct segment_command_64 *seg=(void*)(memory+32);
 struct section_64 *sec=(void*)(memory+32+72);
 uint64_t *info=(void*)(memory+4096);
 mh->magic=MH_MAGIC_64;mh->cputype=CPU_TYPE_ARM64;mh->ncmds=1;mh->sizeofcmds=152;
 seg->cmd=LC_SEGMENT_64;seg->cmdsize=152;strcpy(seg->segname,"__TEXT");seg->vmaddr=0x1000;seg->vmsize=8192;seg->filesize=8192;seg->fileoff=0x2eca000;seg->nsects=1;
 strcpy(sec->sectname,"__crash_info");strcpy(sec->segname,"__TEXT");sec->addr=0x2000;sec->size=64;
 info[0]=5;info[1]=0x102000;info[4]=0x102100;
 strcpy((char*)memory+8192,"termination\nreason");strcpy((char*)memory+8448,"second message");
 dreamlte_crash_image("test",0x100000);assert(messages==2);assert(strstr(output,"termination reason"));assert(strstr(output,"second message"));
 messages=0;info[0]=4;dreamlte_crash_image("test",0x100000);assert(!messages);info[0]=5;
 info[1]=UINT64_MAX;info[4]=0;dreamlte_crash_image("test",0x100000);assert(!messages);
 info[1]=0x102000;memset(memory+8192,'A',256);output[0]=0;dreamlte_crash_image("test",0x100000);assert(messages==1&&strstr(output,"[bounded]"));
 messages=0;seg->cmdsize=8;dreamlte_crash_image("test",0x100000);assert(!messages);seg->cmdsize=152;
 seg->nsects=129;dreamlte_crash_image("test",0x100000);assert(!messages);seg->nsects=1;
 sec->size=UINT64_MAX;dreamlte_crash_image("test",0x100000);assert(!messages);sec->size=64;
 mh->ncmds=129;reads=0;dreamlte_crash_image("test",0x100000);assert(reads==1);mh->ncmds=1;
 uint32_t *all=(void*)(memory+12288);all[0]=17;all[1]=2049;((uint64_t*)all)[1]=0x103100;
 reads=0;dreamlte_crash_annotations("test",0x103000,16,0);assert(reads==1);
 all[1]=1;uint64_t *image=(void*)(memory+12544);image[0]=0x100000;image[1]=0x103200;
 strcpy((char*)memory+12800,"/usr/lib/libc++abi.dylib");output[0]=0;messages=0;
 dreamlte_crash_annotations("test",0x103000,16,0);assert(messages==1&&strstr(output,"images 1 matches 1"));
 all[1]=2048;((uint64_t*)all)[1]=UINT64_MAX-8;reads=0;dreamlte_crash_annotations("test",0x103000,16,0);assert(reads==1);

 /* Real shared caches put annotations in a separate __DATA segment. */
 all[1]=1;((uint64_t*)all)[1]=0x103100;
 mh->ncmds=2;mh->sizeofcmds=224;seg->cmdsize=72;seg->nsects=0;
 struct segment_command_64 *data=(void*)(memory+104);
 memset(data,0,152);data->cmd=LC_SEGMENT_64;data->cmdsize=152;
 strcpy(data->segname,"__DATA");data->vmaddr=0x2000;data->vmsize=64;data->nsects=1;
 sec=(void*)(memory+176);strcpy(sec->sectname,"__crash_info");strcpy(sec->segname,"__DATA");sec->addr=0x2000;sec->size=64;
 output[0]=0;messages=0;dreamlte_crash_annotations("test",0x103000,16,0);
 assert(messages==1&&strstr(output,"images 1 matches 1"));

 const char *paths[]={"/usr/lib/libc++abi.dylib","/usr/lib/libobjc.A.dylib",
 "/usr/lib/system/libsystem_c.dylib","/System/Library/Frameworks/Foundation.framework/Foundation",
 "/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation",
 "/System/Library/Frameworks/QuartzCore.framework/QuartzCore"};
 for(unsigned k=0;k<6;k++) {strcpy((char*)memory+12800,paths[k]);output[0]=0;messages=0;
 dreamlte_crash_annotations("test",0x103000,16,0);assert(messages==1&&strstr(output,"matches 1"));}
 strcpy((char*)memory+12800,"/unselected.dylib");output[0]=0;messages=0;
 dreamlte_crash_annotations("test",0x103000,16,0);assert(!messages&&strstr(output,"matches 0"));
 puts("DREAMLTE actual annotation parser: layout/slide/messages/sanitization/caps/malformed/fault/overflow PASS");
}
''')
    run('sampler worker', 'bsd/kern/sweet_amfi.c',
        'extern void dreamlte_sample_task', '\n#endif', 'cpp',
        r'''
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
void dreamlte_sample_task(const char *name,int pid,task_t task){assert(pid==25&&task);assert(!strcmp(name,"SpringBoard")||!strcmp(name,"backboardd"));samples++;}
int tsleep(void*,int,const char*,int ticks){assert(ticks==(sleeps?120:180)*hz);sleeps++;return 0;}
void proc_iterate(unsigned flags,int(*cb)(proc_t,void*),void *arg,void*,void*){assert(flags==1);iterations++;proc ps[]={{"SpringBoard",(void*)1},{"backboardd",(void*)2},{"other",(void*)3},{"SpringBoard",nullptr}};for(auto &p:ps){current=&p;assert(cb(&p,arg)==0);}}
void PE_parse_boot_argn(const char*,uint32_t *out,unsigned){*out=enabled;}
int kernel_thread_start(void(*fn)(void*,int),void*,thread_t *out){assert(fn);starts++;*out=(void*)4;return 0;}
void thread_deallocate(thread_t t){assert(t==(void*)4);releases++;}
''',
        r'''
int main(){dreamlte_gui_sample_start();assert(!starts);enabled=2;dreamlte_gui_sample_start();assert(!starts);enabled=1;dreamlte_gui_sample_start();assert(starts==1&&releases==1);dreamlte_sample_worker(nullptr,0);assert(iterations==4&&samples==8&&sleeps==5);puts("DREAMLTE actual GUI sampler: opt-in, selected processes, null tasks, four passes and bounded timing PASS");}
''')


if __name__ == '__main__':
    main()
