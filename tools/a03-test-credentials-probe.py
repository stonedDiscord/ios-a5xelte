#!/usr/bin/env python3
"""Check actual read-only credentials probe reference/error/bounds behavior."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1]
p=(root/'xnu/a03/0143-a03-readonly-process-credentials-probe.patch').read_text()
s='\n'.join(l[1:] for l in p.splitlines() if l.startswith('+') and not l.startswith('+++'))
a=s.index('/* Read-only task credential');b=s.index('\n  printf("A03 PROBE help:');src=s[a:b]
pre=r'''
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <assert.h>
#define NGROUPS 16
typedef uint32_t gid_t;
typedef struct {uint8_t b[16];}guid_t;
typedef void *proc_t;typedef void *kauth_cred_t;
#define NOCRED NULL
static int refs,put_count,group_error,guid_error,member_error;static bool no_cred,oversize;
static kauth_cred_t kauth_cred_proc_ref(proc_t p){assert(p==(void*)1);if(no_cred)return NOCRED;refs++;return (void*)2;}
static void kauth_cred_unref(kauth_cred_t *c){assert(*c==(void*)2&&refs==1);refs--;put_count++;*c=NOCRED;}
static int kauth_cred_getgroups(kauth_cred_t c,gid_t *g,size_t *n){assert(c==(void*)2&&refs&&*n==16);if(group_error)return group_error;for(unsigned i=0;i<16;i++)g[i]=i;*n=oversize?100:16;return 0;}
static unsigned kauth_cred_getuid(kauth_cred_t c){assert(c==(void*)2);return 501;}
static unsigned kauth_cred_getgid(kauth_cred_t c){assert(c==(void*)2);return 501;}
static int kauth_cred_getguid(kauth_cred_t c,guid_t *g){assert(c==(void*)2&&refs);if(guid_error)return guid_error;*g=(guid_t){{0}};return 0;}
static int kauth_cred_ismember_gid(kauth_cred_t c,unsigned gid,int *m){assert(c==(void*)2&&refs&&gid==299);if(member_error)return member_error;*m=1;return 0;}
'''
test=r'''
int main(void){no_cred=true;a03_probe_credentials((void*)1,"test",42);assert(!refs&&!put_count);no_cred=false;
a03_probe_credentials((void*)1,"test",42);assert(!refs&&put_count==1);
group_error=5;guid_error=35;member_error=35;a03_probe_credentials((void*)1,"test",42);assert(!refs&&put_count==2);
group_error=guid_error=member_error=0;oversize=true;a03_probe_credentials((void*)1,"test",42);assert(!refs&&put_count==3);
puts("PASS production credential probe: missing cred/error cleanup/group bound/reference release");}
'''
with tempfile.TemporaryDirectory(prefix='a03-creds-') as d:
 f=Path(d)/'test.c';f.write_text(pre+src+test)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(f),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
assert 'if(creds) { a03_probe_credentials(p,name,(int)pid);proc_rele(p);goto out; }' in p
