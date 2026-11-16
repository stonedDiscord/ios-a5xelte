#!/usr/bin/env python3
"""Cumulative EP0/queue and actual live-dispatch tests, no device claim."""
from pathlib import Path
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]

def run(source,header,tests,directory,name):
    p=directory/(name+'.c');p.write_text(header+source+tests)
    subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror',
                    '-Wno-unused-function','-Wno-unused-variable',
                    '-fsanitize=address,undefined',str(p),'-o',str(p.with_suffix(''))],check=True)
    subprocess.run([str(p.with_suffix(''))],check=True)

with tempfile.TemporaryDirectory(prefix='a03-probe-test-') as d:
    d=Path(d)
    numbers=('0103','0104','0106','0109','0110','0111','0113','0115','0117','0135')
    for n in numbers:
        patch,=(ROOT/'xnu/a03').glob(n+'-*.patch')
        subprocess.run(['git','apply','--include=bsd/dev/a03_usb_console.c',str(patch)],cwd=d,check=True)
    s=(d/'bsd/dev/a03_usb_console.c').read_text()
    import re
    s=re.sub(r'^#include .*\n','',s,flags=re.M)
    s=s.replace('__asm__ volatile("dsb sy" ::: "memory");','')
    a=s.index('/* Live DT uses sharkl5');b=s.index('static unsigned le16(',a);s=s[:a]+s[b:]
    a=s.index('static uint8_t r8(');b=s.index('static void update(',a)
    s=s[:a]+'''static unsigned char regs[8192], fifo[512], rx[256];static unsigned fifo_n,rx_pos;
static uint8_t r8(unsigned o) { if(o==0x20)return rx[rx_pos++];return regs[o]; }
static uint16_t r16(unsigned o) { return regs[o]|(regs[o+1]<<8); }
static void w8(unsigned o,uint8_t v) { if(o==0x20)fifo[fifo_n++]=v;else regs[o]=v; }
static void w16(unsigned o,uint16_t v) { regs[o]=v;regs[o+1]=v>>8; }
'''+s[b:]
    s=s[:s.index('static void worker(')]+'\n#endif\n'
    h='''#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#define ARM64_BOARD_CONFIG_SWEET 1
#define __unused __attribute__((unused))
#define FALSE 0
typedef uintptr_t vm_offset_t;typedef size_t vm_size_t;typedef int boolean_t,wait_result_t;
static int ml_set_interrupts_enabled(int x) { return x; }
static size_t strlcpy(char *d,const char *s,size_t n) { size_t z=strlen(s);if(n){size_t k=z<n-1?z:n-1;memcpy(d,s,k);d[k]=0;}return z; }
static unsigned executed,drained;
void a03_live_probe(const char *s) { (void)s;executed++; }
static void IOSleep(unsigned n) { (void)n; }
unsigned a03_console_read(unsigned char *p,unsigned n) { (void)p;(void)n;drained++;return 0; }
'''
    tests=r'''
static void request(const char *command) {
 unsigned n=strlen(command);unsigned char req[]={0x40,0xa3,0,0,0,0,(unsigned char)n,0};
 setup(req);assert(control_out==2);
 unsigned off=0;
 while(off<n) {
  unsigned size=n-off<64?n-off:64;memcpy(rx,command+off,size);rx_pos=0;
  ep_write(0,8,size);ep_write(0,2,1);poll_usb();off+=size;
 }
}
int main(void) {
 usb=(uintptr_t)regs;configured=probe_enabled=1;
 request("ping");assert(probe_count==1&&!executed&&!control_out&&ep_read(0,2)==0x48);
 char command[128];assert(probe_dequeue(command)&&!strcmp(command,"ping"));
 char longcmd[128];memset(longcmd,'x',127);longcmd[127]=0;request(longcmd);
 assert(probe_dequeue(command)&&strlen(command)==127);
 for(unsigned i=0;i<4;i++)request("vm");
 assert(probe_count==4&&!probe_enqueue("extra"));
 unsigned char full[]={0x40,0xa3,0,0,0,0,4,0};setup(full);
 assert(!control_out&&ep_read(0,2)==0x60);
 /* Even a full queue cannot stop the original IN drain path. */
 ep_write(0,2,0);ep_write(1,2,0);unsigned before=drained;poll_usb();assert(drained==before+1);
 while(probe_dequeue(command))assert(!strcmp(command,"vm"));
 /* Strict request identity, length and opt-in. */
 for(unsigned i=0;i<8;i++) {
  unsigned char bad[]={0x40,0xa3,0,0,0,0,4,0};bad[i]^=0x80;
  setup(bad);assert(!control_out&&ep_read(0,2)==0x60);
 }
 probe_enabled=0;setup(full);assert(!control_out&&!probe_enqueue("ping"));probe_enabled=1;
 /* A newline or NUL cannot inject an additional command. */
 setup(full);memcpy(rx,"a\nbc",4);rx_pos=0;ep_write(0,8,4);ep_write(0,2,1);poll_usb();
 assert(!control_out&&!probe_count&&ep_read(0,2)==0x60);
 /* A prematurely short packet must not leave a partial command pending. */
 setup(full);memcpy(rx,"pi",2);rx_pos=0;ep_write(0,8,2);ep_write(0,2,1);poll_usb();
 assert(!control_out&&!probe_count&&ep_read(0,2)==0x60);
 /* Reset aborts an incomplete control command. */
 setup(full);regs[0x0a]=4;ep_write(0,2,0);poll_usb();regs[0x0a]=0;assert(!control_out&&!configured);
 configured=1;assert(reset_count==1&&setup_count>8);
 /* Legacy hold commands and Download remain independent. */
 const char *p="regs\nprobe ping\n";while(*p)input_char(*p++);
 assert(a03_usb_debug_command(command,sizeof(command))&&!strcmp(command,"regs"));
 assert(probe_dequeue(command)&&!strcmp(command,"ping"));
 p="download\n";while(*p)input_char(*p++);assert(download_requested);download_requested=0;
 for(unsigned i=0;i<140;i++)input_char('x');input_char('\n');assert(!command_available&&!probe_count);
 assert(!executed);puts("PASS EP0 strict setup, split127-byte command, queue-full log drain, reset, disabled, malformed data, legacy isolation");
}
'''
    run(s,h,tests,d,'transport')

# Host-side validation has no device access.
import sys
sys.path.insert(0,str(ROOT/'tools'))
from a03_usb_probe import validate
assert validate('sample 26')==b'sample 26'
for command in ('','x'*128,'ping\n','a\x00b','é'):
    try:validate(command)
    except (ValueError,UnicodeError):pass
    else:raise AssertionError(command)
print('PASS host command validation')

# Compile and execute the production command dispatcher against task/map stubs.
patch=(ROOT/'xnu/a03/0135-a03-live-usb-probes.patch').read_text()
part=patch.split('+++ b/bsd/kern/sweet_amfi.c',1)[1].split('--- a/bsd/dev/a03_emmc.c',1)[0]
source='\n'.join(line[1:] for line in part.splitlines() if line.startswith('+'))
source=source[source.index('/* Only the dedicated'):]
header=r'''
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <limits.h>
#define TASK_NULL NULL
#define PROC_NULL NULL
#define VM_MAP_NULL NULL
#define KERN_SUCCESS 0
#define PROC_RETURNED 0
#define PROC_RETURNED_DONE 1
#define PROC_ALLPROCLIST 1
#define PROC_NOWAITTRANS 4
#define HOST_VM_INFO64_COUNT 40
#define PAGE_SIZE 16384
struct proc { int pid; };typedef struct proc *proc_t;
typedef void *task_t;typedef void *vm_map_t;typedef int kern_return_t;typedef size_t vm_size_t;
typedef struct {unsigned free_count,active_count,inactive_count,wire_count,external_page_count,compressor_page_count;
 unsigned long long faults,pageins,pageouts,reactivations,compressions,decompressions,swapins,swapouts;} vm_statistics64_data_t;
static struct proc process={26};static unsigned references,samples,reads,maps,io_calls;static bool missing,task_missing,read_error;
static int proc_pid(proc_t p){return p->pid;}
static void proc_name(int pid,char *s,size_t n){assert(pid==26);snprintf(s,n,"SpringBoard");}
static proc_t proc_find(int pid){if(pid!=26||missing)return NULL;references++;return &process;}
static int proc_rele(proc_t p){assert(p==&process&&references);references--;return 0;}
static task_t proc_task(proc_t p){assert(p==&process);return task_missing?NULL:(void*)1;}
static vm_map_t get_task_map_reference(task_t t){assert(t==(void*)1);maps++;return (void*)2;}
static void vm_map_deallocate(vm_map_t m){assert(m==(void*)2&&maps);maps--;}
static int vm_map_read_user(vm_map_t m,uint64_t addr,void *buf,size_t n){assert(m==(void*)2&&n<=256&&addr+n>=addr);reads++;memset(buf,0x42,n);return read_error?5:0;}
void a03_sample_task(const char *name,int pid,task_t t){assert(!strcmp(name,"SpringBoard")&&pid==26&&t==(void*)1);samples++;}
void a03_probe_task(const char *name,int pid,task_t t,bool user){(void)user;a03_sample_task(name,pid,t);}
void a03_emmc_probe_stats(void){io_calls++;}
static int vm_stats(void *v,unsigned *count){assert(*count==40);memset(v,0,sizeof(vm_statistics64_data_t));return 0;}
static void proc_iterate(unsigned flags,int(*cb)(proc_t,void*),void *arg,void *f,void *x){assert(flags==5&&!f&&!x);cb(&process,arg);}
'''
tests=r'''
int main(void){
 a03_live_probe("ping");a03_live_probe("help");a03_live_probe("ps");a03_live_probe("vm");a03_live_probe("io");assert(io_calls==1);
 a03_live_probe("sample 26");assert(samples==1&&!references);
 a03_live_probe("threads 26");assert(samples==2&&!references);
 a03_live_probe("mem 26 1000 100");assert(reads==1&&!maps&&!references);
 const char *bad[]={"sample 0","sample -1","sample 26x","sample 2147483648","sample 26 trailing","mem 26 ffffffffffffffff 2","mem 26 1000 101","mem 26 1000 0","mem 26 0x 10","mem 26 1000 10 rubbish","mem 26 10000000000000000 1","resume 26"};
 for(unsigned i=0;i<sizeof(bad)/sizeof(bad[0]);i++)a03_live_probe(bad[i]);
 assert(samples==2&&reads==1&&!references&&!maps);
 read_error=true;a03_live_probe("mem 26 1000 1");assert(reads==2&&!maps&&!references);
 missing=true;a03_live_probe("sample 26");missing=false;task_missing=true;a03_live_probe("sample 26");assert(samples==2&&!references);
 puts("PASS production live dispatcher, bounds/overflow/trailing rejection, missing task and failed-read reference cleanup");
}
'''
with tempfile.TemporaryDirectory(prefix='a03-dispatch-test-') as d:
    run(source,header,tests,Path(d),'dispatcher')
