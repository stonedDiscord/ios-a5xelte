#!/usr/bin/env python3
"""Exercise the actual optional ScreenTime lab metadata helper with fault injection.

This tests API control flow and metadata, not Apple vault access enforcement.
"""
from pathlib import Path
import subprocess
import tempfile

patch = (Path(__file__).resolve().parents[1] /
         'xnu/a03/0144-a03-opt-in-lab-screentime-vault-metadata.patch').read_text()
added = '\n'.join(line[1:] for line in patch.splitlines()
                  if line.startswith('+') and not line.startswith('+++'))
start = added.index('static int\na03_sandbox_lab_vault(')
end = added.index('\n    if (call == 0x104)', start)
source = added[start:end]
pre = r'''
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>
#include <stdio.h>
#include <errno.h>
#undef ENOTSUP
#define ENOTSUP 45
#define ENOATTR 93
#define MNT_ROOTFS 1
#define UF_DATAVAULT 0x80
#define UIO_SYSSPACE 1
#define UIO_READ 1
#define UIO_WRITE 2
#define XATTR_CREATE 2
#define KAUTH_VNODE_WRITE_EXTATTRIBUTES 0x400
#define UIO_STACKBUF(name,n) uint64_t name[8]
typedef uintptr_t user_addr_t;
typedef void *vnode_t; typedef void *mount_t; typedef void *vfs_context_t;
typedef unsigned kauth_action_t;
struct proc {int unused;};
struct vnode_attr {unsigned va_uid,va_flags,active,supported;};
#define va_uid_BIT 1
#define va_flags_BIT 2
#define VATTR_INIT(v) memset(v,0,sizeof(*(v)))
#define VATTR_WANTED(v,f) ((v)->active|=f##_BIT)
#define VATTR_SET(v,f,x) ((v)->f=(x),(v)->active|=f##_BIT)
#define VATTR_IS_SUPPORTED(v,f) ((v)->supported&f##_BIT)
static unsigned a03_lab_vault,uid=501,owner_uid=501,flags;
static int fail_copy,fail_string,fail_fd,fail_path,fail_attr,fail_authattr,
 fail_auth,fail_getx,fail_setx,fail_flags,puts_count,writes,sets,reads;
static bool entitled=true,directory=true,mounted=true,rootfs=true,rd_present=true,
 wrong_root,wrong_path,wrong_owner,unsupported,unsupported_set,fail_uio,fail_iov,has_xattr;
static char saved_owner[64];static size_t saved_size;
static unsigned requested_fd=3;
static int copyin(user_addr_t a,void *d,size_t n){assert(a==0x1000&&n==16);reads++;if(fail_copy)return EFAULT;uint64_t x[2]={requested_fd,0x2000};memcpy(d,x,n);return 0;}
static int copyinstr(user_addr_t a,char *d,size_t n,size_t *c){assert(a==0x2000&&n==64);if(fail_string)return EFAULT;const char *s=wrong_owner?"other":"remotemanagementd";*c=strlen(s)+1;memcpy(d,s,*c);return 0;}
static void *sweet_proc_entitlements(struct proc *p){assert(p);return (void*)1;}
static bool sweet_entitlements_bool(void *p,const char *s){assert(p==(void*)1&&!strcmp(s,"com.apple.rootless.storage.remotemanagementd"));return entitled;}
static vfs_context_t vfs_context_current(void){return (void*)2;}
static void *vfs_context_ucred(vfs_context_t c){assert(c==(void*)2);return c;}
static unsigned kauth_cred_getuid(void *c){assert(c==(void*)2);return uid;}
static int vnode_getfromfd(vfs_context_t c,int fd,vnode_t *p){assert(c==(void*)2&&fd==3);if(fail_fd)return EBADF;*p=(void*)3;return 0;}
static mount_t vnode_mount(vnode_t p){assert(p==(void*)3);return mounted?(void*)4:NULL;}
static int vnode_isdir(vnode_t p){assert(p==(void*)3);return directory;}
static unsigned vfs_flags(mount_t m){assert(m==(void*)4);return rootfs?1:0;}
static int PE_parse_boot_argn(const char *s,char *d,size_t n){assert(!strcmp(s,"rd")&&n==32);snprintf(d,n,"%s",wrong_root?"other":"a03userdata0");return rd_present;}
static int vn_getpath(vnode_t v,char *s,int *n){assert(v==(void*)3&&*n==256);if(fail_path)return EIO;snprintf(s,*n,"%s",wrong_path?"/other":"/private/var/mobile/Library/Application Support/com.apple.remotemanagementd");return 0;}
static int vnode_getattr(vnode_t v,struct vnode_attr *a,vfs_context_t c){assert(v==(void*)3&&c==(void*)2&&a->active==3);if(fail_attr)return EIO;a->supported=unsupported?0:3;a->va_uid=owner_uid;a->va_flags=flags;return 0;}
static int vnode_authattr(vnode_t v,struct vnode_attr *a,kauth_action_t *x,vfs_context_t c){assert(v==(void*)3&&c==(void*)2&&a->va_flags==(flags|0x80));*x=0x800;return fail_authattr?EACCES:0;}
static int vnode_authorize(vnode_t v,vnode_t d,kauth_action_t x,vfs_context_t c){assert(v==(void*)3&&!d&&c==(void*)2&&x==0xc00);return fail_auth?EACCES:0;}
struct uio {void *data;size_t size;int direction;};typedef struct uio *uio_t;static struct uio io;
static uio_t uio_createwithbuffer(int n,int off,int space,int dir,void *b,size_t size){assert(n==1&&!off&&space==1&&b&&size==64);if(fail_uio)return NULL;io=(struct uio){.direction=dir};return &io;}
static int uio_addiov(uio_t u,user_addr_t p,size_t n){assert(u==&io);if(fail_iov)return EINVAL;u->data=(void*)p;u->size=n;return 0;}
static int vn_getxattr(vnode_t v,const char *name,uio_t u,size_t *size,int opt,vfs_context_t c){assert(v==(void*)3&&c==(void*)2&&!strcmp(name,"com.apple.rootless")&&!opt&&u->direction==1&&u->size==64);if(fail_getx)return EIO;if(!has_xattr)return ENOATTR;memcpy(u->data,saved_owner,saved_size);*size=saved_size;return 0;}
static int vn_setxattr(vnode_t v,const char *name,uio_t u,int opt,vfs_context_t c){assert(v==(void*)3&&c==(void*)2&&!strcmp(name,"com.apple.rootless")&&opt==2&&u->direction==2);sets++;if(fail_setx)return EEXIST;memcpy(saved_owner,u->data,u->size);saved_size=u->size;has_xattr=true;writes++;return 0;}
static int vnode_setattr(vnode_t v,struct vnode_attr *a,vfs_context_t c){assert(v==(void*)3&&c==(void*)2&&a->active==2);if(fail_flags)return EIO;a->supported=unsupported_set?0:2;if(!unsupported_set)flags=a->va_flags;return 0;}
static void vnode_put(vnode_t v){assert(v==(void*)3);puts_count++;}
'''
test = r'''
static int run(void){struct proc p={0};return a03_sandbox_lab_vault(&p,0x1000);}
int main(void){
assert(run()==ENOTSUP&&!reads);a03_lab_vault=2;assert(run()==ENOTSUP&&!reads);a03_lab_vault=1;
fail_copy=1;assert(run()==EFAULT);fail_copy=0;
requested_fd=UINT_MAX;assert(run()==EBADF);requested_fd=3;
fail_string=1;assert(run()==EFAULT);fail_string=0;
wrong_owner=true;assert(run()==ENOTSUP);wrong_owner=false;
entitled=false;assert(run()==EPERM);entitled=true;
uid=0;assert(run()==EPERM);uid=501;
fail_fd=1;assert(run()==EBADF&&!puts_count);fail_fd=0;
#define REJECT(flag,err) do{int n=puts_count;flag=1;assert(run()==err&&puts_count==n+1&&!writes&&!flags);flag=0;}while(0)
directory=false;assert(run()==EPERM);directory=true;
mounted=false;assert(run()==EPERM);mounted=true;
rootfs=false;assert(run()==EPERM);rootfs=true;
rd_present=false;assert(run()==EPERM);rd_present=true;
REJECT(wrong_root,EPERM);REJECT(wrong_path,EPERM);REJECT(fail_path,EIO);
REJECT(fail_attr,EIO);REJECT(unsupported,ENOTSUP);
owner_uid=0;assert(run()==EPERM);owner_uid=501;
REJECT(fail_authattr,EACCES);REJECT(fail_auth,EACCES);
REJECT(fail_uio,ENOMEM);REJECT(fail_iov,EINVAL);REJECT(fail_getx,EIO);REJECT(fail_setx,EEXIST);
assert(!writes&&!flags);
fail_flags=1;assert(run()==EIO&&writes==1&&flags==0&&has_xattr);fail_flags=0;
assert(saved_size==strlen("remotemanagementd")&&!memcmp(saved_owner,"remotemanagementd",saved_size));
flags=0x400;assert(run()==0&&flags==0x480&&writes==1);int n=sets;
assert(run()==0&&sets==n&&flags==0x480);
saved_owner[0]='X';assert(run()==EPERM&&flags==0x480&&sets==n);saved_owner[0]='r';
saved_size++;assert(run()==EPERM&&sets==n);saved_size--;
unsupported_set=1;assert(run()==ENOTSUP&&sets==n);unsupported_set=0;
printf("PASS actual lab vault helper: optin/entitlement/uid/fd/root/path/ownership/auth gates; faults; owner metadata; flag preservation; retries; no relabel\n");
}
'''
with tempfile.TemporaryDirectory(prefix='a03-vault-') as directory:
    path = Path(directory) / 'test.c'
    path.write_text(pre + source + test)
    subprocess.run(['clang', '-std=c11', '-Wall', '-Wextra', '-Werror',
                    '-fsanitize=address,undefined', str(path), '-o', directory + '/test'], check=True)
    subprocess.run([directory + '/test'], check=True)
