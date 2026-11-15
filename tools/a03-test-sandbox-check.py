from pathlib import Path
import tempfile,subprocess
root=Path(__file__).resolve().parent.parent
patch=(root/'xnu/a03/0121-a03-opt-in-sandbox-check-api.patch').read_text()
added='\n'.join(x[1:] for x in patch.splitlines() if x.startswith('+') and not x.startswith('+++'))
src=added[:added.index('static const struct mac_policy_ops a03_sandbox_mac_ops')]
assert 'call != 2' in src
assert 'a03_sandbox_disabled == 1' in added
assert '"a03_sandbox_disabled", 0' in added
assert '.mpc_name = "Sandbox"' in added

pre=r'''
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
'''
test=r'''
#undef printf
int main(void){struct proc p={"launchd"};
int unsupported[]={-1,0,1,3,4,5,6,0x43,999};
for(unsigned i=0;i<sizeof(unsupported)/sizeof(*unsupported);i++)assert(a03_sandbox_check_syscall(&p,unsupported[i],0x1000)==ENOTSUP);
assert(reads==0&&writes==0);
input_error=EFAULT;assert(a03_sandbox_check_syscall(&p,2,0x1000)==EFAULT&&writes==0);
input_error=0;output_address=0;assert(a03_sandbox_check_syscall(&p,2,0x1000)==EFAULT&&writes==0);
output_address=0x2000;output_error=EFAULT;assert(a03_sandbox_check_syscall(&p,2,0x1000)==EFAULT&&output_value==99);
output_error=0;assert(a03_sandbox_check_syscall(&p,2,0x1000)==0&&output_value==0);
for(unsigned i=0;i<1000;i++){output_value=99;assert(a03_sandbox_check_syscall(&p,2,0x1000)==0&&output_value==0);}assert(logs==32);
puts("A03 actual lab sandbox op2: unsupported operations, copyin/copyout faults, null output, full64-bit allow and logging cap PASS");}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'test.c').write_text(pre+src+test)
 subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror',str(p/'test.c'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True)
