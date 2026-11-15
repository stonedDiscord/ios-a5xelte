"""Exercise the actual A03 fallback's scope and error propagation on host."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parent.parent
patch = (root / 'xnu/a03/0122-a03-opt-in-hfs-rename-swap.patch').read_text()
# CI uses git apply without --unidiff-zero. Every hunk must carry context;
# otherwise insertions can be relocated silently (failed run43757697658).
hunks = patch.split('@@')[2::2]
assert hunks and all(any(line.startswith(' ') for line in hunk.splitlines())
                     for hunk in hunks), 'git apply requires context in every hunk'
added = '\n'.join(line[1:] for line in patch.splitlines()
                  if line.startswith('+') and not line.startswith('+++'))
start = added.index('/* A03 lab root only:')
end = added.index('\n\t\t\t_err = a03_hfs_rename_swap')
helper = added[start:end]
pre = r'''
#include <assert.h>
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#define ENOTSUP 45
#define VFS_RENAME_SWAP 2
#define MNT_ROOTFS 0x4000
#define MNT_RDONLY 1
#define NULLVP NULL
typedef unsigned vfs_rename_flags_t;
typedef void *vfs_context_t;
struct mount {unsigned mnt_flag;struct {char *f_fstypename,*f_mntfromname;} mnt_vfsstat;};
typedef struct mount *mount_t;
struct vnode {int regular; mount_t mount;};
typedef struct vnode *vnode_t;
static unsigned enabled=1,writable=1,calls,logs;
static int exchange_result;
static int vnode_isreg(vnode_t vp){return vp->regular;}
static mount_t vnode_mount(vnode_t vp){return vp->mount;}
static void PE_parse_boot_argn(const char *name,void *p,size_t size){assert(size==4);*(uint32_t *)p=strcmp(name,"a03_hfs_swap")==0?enabled:writable;}
static int VNOP_EXCHANGE(vnode_t a,vnode_t b,int flags,vfs_context_t ctx){assert(a!=b&&flags==0&&ctx==(void *)1);calls++;return exchange_result;}
static int logline(const char *fmt,...){(void)fmt;logs++;return 0;}
#define printf logline
'''
test = r'''
#undef printf
int main(void){
struct mount m={MNT_ROOTFS,{"hfs","/dev/a03userdata0"}},other=m;
struct vnode a={1,&m},b={1,&m};
#define RUN(e,f,x,y) a03_hfs_rename_swap(e,f,x,y,(void *)1)
assert(RUN(0,2,&a,&b)==0);assert(RUN(13,2,&a,&b)==13);
assert(RUN(45,0,&a,&b)==45);assert(RUN(45,3,&a,&b)==45);
assert(RUN(45,2,NULL,&b)==45);assert(RUN(45,2,&a,NULL)==45);
assert(RUN(45,2,&a,&a)==45);
a.regular=0;assert(RUN(45,2,&a,&b)==45);a.regular=1;
b.regular=0;assert(RUN(45,2,&a,&b)==45);b.regular=1;
a.mount=NULL;assert(RUN(45,2,&a,&b)==45);a.mount=&m;
b.mount=&other;assert(RUN(45,2,&a,&b)==45);b.mount=&m;
m.mnt_flag=0;assert(RUN(45,2,&a,&b)==45);
m.mnt_flag=MNT_ROOTFS|MNT_RDONLY;assert(RUN(45,2,&a,&b)==45);m.mnt_flag=MNT_ROOTFS;
m.mnt_vfsstat.f_fstypename="apfs";assert(RUN(45,2,&a,&b)==45);m.mnt_vfsstat.f_fstypename="hfs";
m.mnt_vfsstat.f_mntfromname="/dev/a03boot0";assert(RUN(45,2,&a,&b)==45);m.mnt_vfsstat.f_mntfromname="/dev/a03userdata0";
for(unsigned i=0;i<3;i+=2){enabled=i;assert(RUN(45,2,&a,&b)==45);}enabled=1;
for(unsigned i=0;i<3;i+=2){writable=i;assert(RUN(45,2,&a,&b)==45);}writable=1;
assert(calls==0&&logs==0);
exchange_result=5;assert(RUN(45,2,&a,&b)==5&&calls==1);
exchange_result=0;assert(RUN(45,2,&a,&b)==0&&calls==2);
for(unsigned i=0;i<100;i++)assert(RUN(45,2,&a,&b)==0);
assert(logs==32);
puts("A03 actual HFS swap fallback: root/device/type/rw/opt-in/file/flags gates, exchange errors and log bound PASS");
}
'''
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory)
    (path / 'test.c').write_text(pre + helper + test)
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror',
                    str(path / 'test.c'), '-o', str(path / 'test')], check=True)
    subprocess.run([str(path / 'test')], check=True)
