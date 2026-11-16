#!/usr/bin/env python3
"""Exercise actual read-only data-tree stat helper and vnode cleanup."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1]
patch=(root/'xnu/a03/0140-a03-readonly-filesystem-probe.patch').read_text()
source='\n'.join(l[1:] for l in patch.splitlines() if l.startswith('+') and not l.startswith('+++'))
source=source[:source.index('\n  printf("A03 PROBE help:')]
header=r'''
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
typedef void *vnode_t;typedef void *vfs_context_t;
struct vnode_attr {unsigned va_uid,va_gid,va_mode,va_flags;uint64_t va_fileid,va_supported;};
#define VATTR_INIT(p) memset(p,0,sizeof(*(p)))
#define VATTR_WANTED(p,a) ((void)(p))
#define VATTR_IS_SUPPORTED(p,a) ((p)->va_supported==31)
static unsigned lookups,gets,puts_count,refs;static int lookup_error,get_error;static bool partial;
static vfs_context_t vfs_context_kernel(void){return (void*)1;}
static int vnode_lookup(const char *p,int flags,vnode_t *out,vfs_context_t c){assert(!flags&&c==(void*)1&&strstr(p,"/private/var/")==p);lookups++;if(lookup_error)return lookup_error;*out=(void*)2;refs++;return 0;}
static int vnode_getattr(vnode_t p,struct vnode_attr *a,vfs_context_t c){assert(p==(void*)2&&refs&&c==(void*)1);gets++;if(get_error)return get_error;a->va_uid=501;a->va_gid=501;a->va_mode=0755;a->va_flags=0;a->va_fileid=123;a->va_supported=partial?1:31;return 0;}
static void vnode_put(vnode_t p){assert(p==(void*)2&&refs==1);puts_count++;refs--;}
static void *vnode_mount(vnode_t p){assert(p==(void*)2&&refs);return (void*)3;}
static uint64_t vfs_flags(void *p){assert(p==(void*)3);return 0x123;}
'''
tests=r'''
int main(void){
 a03_probe_stat("/private/var/containers/Data/System/test");assert(lookups==1&&gets==1&&puts_count==1&&!refs);
 lookup_error=2;a03_probe_stat("/private/var/missing");assert(lookups==2&&gets==1&&puts_count==1&&!refs);lookup_error=0;
 get_error=5;a03_probe_stat("/private/var/fail");assert(lookups==3&&gets==2&&puts_count==2&&!refs);get_error=0;
 partial=true;a03_probe_stat("/private/var/partial");assert(lookups==4&&gets==3&&puts_count==3&&!refs);
 a03_probe_stat("/private/var/../../System");a03_probe_stat("/private/var/..");a03_probe_stat("/private/var/.");a03_probe_stat("/System/Library");a03_probe_stat("");a03_probe_stat("/private/vars/test");assert(lookups==4);
 char path[128]="/private/var/";memset(path+13,'a',101);path[114]=0;a03_probe_stat(path);assert(lookups==4);
 puts("PASS production filesystem probe: bounded data paths, no-follow lookup, attributes/support, lookup/getattr failure cleanup");
}
'''
with tempfile.TemporaryDirectory(prefix='a03-stat-') as d:
 p=Path(d)/'test.c';p.write_text(header+source+tests)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
