#!/usr/bin/env python3
"""Actual named-profile helper: no device/API enforcement claims."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1]
p=(root/'xnu/a03/0136-a03-tccd-lab-named-profile.patch').read_text()
s='\n'.join(x[1:] for x in p.splitlines() if x.startswith('+') and not x.startswith('+++'))
s=s[:s.index('    if (call == 1 || call == 22)')]
pre=r'''
#include <assert.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdarg.h>
#undef ENOTSUP
#define ENOTSUP 45
#define TUNABLE(t,n,s,v) t n=v
typedef uintptr_t user_addr_t;
struct proc {const char *name;};
static uint64_t request[3]={0x2000,0,0};
static int input_error,string_error;static unsigned reads,strings,logs;
static size_t read_size;static const char *profile="com.apple.tccd";
static int copyin(user_addr_t addr,void *out,size_t n){assert(addr==0x1000);reads++;read_size=n;if(input_error)return input_error;memcpy(out,request,n);return 0;}
static int copyinstr(user_addr_t addr,char *out,size_t n,void *len){assert(addr==0x2000&&n==64&&len==NULL);strings++;if(string_error)return string_error;snprintf(out,n,"%s",profile);return 0;}
static int proc_pid(struct proc *p){(void)p;return 42;}
static void proc_name(int pid,char *out,size_t n){assert(pid==42);extern const char *procname;snprintf(out,n,"%s",procname);}
const char *procname="tccd";
static int logline(const char *fmt,...){(void)fmt;logs++;return 0;}
#define printf logline
'''
test=r'''
#undef printf
int main(void){struct proc p={"tccd"};
assert(a03_sandbox_named_profile(&p,22,0x1000)==ENOTSUP&&reads==0);
a03_sandbox_profiles=2;assert(a03_sandbox_named_profile(&p,1,0x1000)==ENOTSUP&&reads==0);
a03_sandbox_profiles=1;input_error=EFAULT;assert(a03_sandbox_named_profile(&p,22,0x1000)==EFAULT&&strings==0);
input_error=0;request[0]=0;assert(a03_sandbox_named_profile(&p,22,0x1000)==EFAULT);
request[0]=0x2000;request[1]=1;assert(a03_sandbox_named_profile(&p,1,0x1000)==ENOTSUP);
request[1]=0;request[2]=1;assert(a03_sandbox_named_profile(&p,1,0x1000)==ENOTSUP);
request[2]=0;string_error=ENAMETOOLONG;assert(a03_sandbox_named_profile(&p,22,0x1000)==ENAMETOOLONG);
string_error=EFAULT;assert(a03_sandbox_named_profile(&p,1,0x1000)==EFAULT);
string_error=0;profile="com.apple.other";assert(a03_sandbox_named_profile(&p,22,0x1000)==ENOTSUP);
profile="com.apple.tccd";procname="other";assert(a03_sandbox_named_profile(&p,1,0x1000)==ENOTSUP);
procname="tccd";assert(a03_sandbox_named_profile(&p,22,0x1000)==0&&read_size==8);
assert(a03_sandbox_named_profile(&p,1,0x1000)==0&&read_size==24);
for(int i=0;i<100;i++)assert(a03_sandbox_named_profile(&p,22,0x1000)==0);
assert(logs==16);
puts("PASS tccd-only lab profile: opt-in, exact ABI, copy faults, bounded names, bytecode rejection, log cap");}
'''
with tempfile.TemporaryDirectory() as d:
 f=Path(d)/'test.c';f.write_text(pre+s+test)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(f),'-o',str(f.with_suffix(''))],check=True)
 subprocess.run([str(f.with_suffix(''))],check=True)
assert 'if (call == 1 || call == 22) return a03_sandbox_named_profile' in p
assert 'if (call != 2) return ENOTSUP;' in p
