#!/usr/bin/env python3
"""Exercise the actual A03 entitlement-gated MAC privilege grant on host."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parent.parent
patch=(root/'xnu/a03/0124-a03-entitled-work-interval.patch').read_text()
s='\n'.join(l[1:] for l in patch.splitlines() if l.startswith('+') and not l.startswith('+++'))
s=s[s.index('static TUNABLE'):s.index('    .mpo_priv_grant')]
s=s[:s.index('static const struct mac_policy_ops')] if 'static const struct mac_policy_ops' in s else s
pre=r'''
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
'''
tests=r'''
int main(){
assert(a03_sandbox_priv_grant(cred,PRIV_WORK_INTERVAL)==EPERM&&queries==0);
a03_work_interval=1;
assert(a03_sandbox_priv_grant(cred,99)==EPERM&&queries==0);
assert(a03_sandbox_priv_grant((void*)4,PRIV_WORK_INTERVAL)==EPERM&&queries==0);
assert(a03_sandbox_priv_grant(cred,PRIV_WORK_INTERVAL)==EPERM&&queries==1);
entitled=true;
for(int i=0;i<20;i++)assert(a03_sandbox_priv_grant(cred,PRIV_WORK_INTERVAL)==0);
entitled=false;assert(a03_sandbox_priv_grant(cred,PRIV_WORK_INTERVAL)==EPERM);
puts("A03 actual MAC grant: opt-in/current credential/exact privilege/boolean entitlement and bounded reports PASS");}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'test.cpp').write_text(pre+s+tests)
 subprocess.run(['c++','-std=c++17','-Wall','-Wextra','-Werror',str(p/'test.cpp'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True)
