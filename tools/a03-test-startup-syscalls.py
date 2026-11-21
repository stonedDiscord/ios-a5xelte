#!/usr/bin/env python3
"""Exercise actual startup diagnostic selection, cap and user-memory reads."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parent.parent
patch=(root/'xnu/a03/0120-a03-bounded-startup-syscall-evidence.patch').read_text().split('--- a/bsd/conf/')[0]
source='\n'.join(x[1:] for x in patch.splitlines() if x.startswith('+') and not x.startswith('+++'))
source=source[source.index('#if defined(ARM64_BOARD_CONFIG_SWEET)'):source.index('\n\tif (is_saved_state64')]
source=source[:source.rindex('#if defined(ARM64_BOARD_CONFIG_SWEET)')]
# Apply the small follow-up selection extension to the extracted real helper.
follow=(root/'xnu/a03/0126-a03-springboard-startup-evidence.patch').read_text()
assert '+    static unsigned reports[5];' in follow
assert '+    else if (!strcmp(p->p_comm, "SpringBoard")) slot = 4;' in follow
source=source.replace('static unsigned reports[4];','static unsigned reports[5];',1).replace('else if (!strcmp(p->p_comm, "notifyd")) slot = 3;','else if (!strcmp(p->p_comm, "notifyd")) slot = 3;\n    else if (!strcmp(p->p_comm, "SpringBoard")) slot = 4;',1)
with tempfile.TemporaryDirectory() as d:
 q=Path(d)/'bsd/dev/arm/systemcalls.c';q.parent.mkdir(parents=True)
 q.write_text(source)
 subprocess.run(['git','apply','--include=bsd/dev/arm/systemcalls.c',str(root/'xnu/a03/0138-a03-screentime-analytics-evidence.patch')],cwd=d,check=True)
 subprocess.run(['git','apply','--include=bsd/dev/arm/systemcalls.c',str(root/'xnu/a03/0139-a03-filesystem-startup-evidence.patch')],cwd=d,check=True)
 subprocess.run(['git','apply',str(root/'xnu/a03/0198-a03-posterboard-startup-evidence.patch')],cwd=d,check=True)
 subprocess.run(['git','apply',str(root/'xnu/a03/0199-a03-focus-posterboard-path-evidence.patch')],cwd=d,check=True)
 source=q.read_text()
names=['open','open_nocancel','access','mkdir','mkdir_extended','stat64','lstat64','getattrlist','getxattr','__mac_syscall','openat','openat_nocancel','openat_dprotected_np','faccessat','mkdirat','getattrlistat','csops','csops_audittoken','setattrlist','fsetattrlist','setattrlistat','setxattr','fsetxattr']
names += ['unlink', 'fstatat64']
header=r'''
#include <assert.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#define ARM64_BOARD_CONFIG_SWEET 1
#define CS_OPS_ENTITLEMENTS_BLOB 7
#define CS_OPS_DER_ENTITLEMENTS_BLOB 16
typedef uintptr_t user_addr_t;
struct proc {char p_comm[17];};
static unsigned enabled,logs,strings,headers;static uintptr_t last;
static const char *sample_path = "path\nvalue";
static int proc_pid(struct proc *p){(void)p;return 42;}
static void PE_parse_boot_argn(const char *a,void *p,size_t n){assert(!strcmp(a,"a03crash_log")&&n==4);memcpy(p,&enabled,n);}
static int copyinstr(user_addr_t a,char *b,size_t n,size_t *c){assert(c);last=a;strings++;if(a!=0x1000)return 1;assert(n==192);strcpy(b,sample_path);*c=strlen(sample_path)+1;return 0;}
static int copyin(user_addr_t a,void *p,size_t n){last=a;headers++;assert(n==8||n==16||n==24);if(a==0xdead)return 1;memset(p,0,n);if(n==16)((uint64_t *)p)[1]=0x1000;return 0;}
static int logline(const char *f,...){(void)f;logs++;return 0;}
#define printf logline
'''
header+='\n'.join('#define SYS_'+n+' '+str(i+1) for i,n in enumerate(names))+'\n'
tests=r'''
#undef printf
int main(void){
 struct proc p={"backboardd"};uint64_t a[4]={0x1000,0x2000,0,0};
 a03_startup_syscall_log(&p,SYS_open,2,a,0,1);assert(!logs&&!strings);
 enabled=2;a03_startup_syscall_log(&p,SYS_open,2,a,0,1);assert(!logs);
 enabled=1;strcpy(p.p_comm,"unselected");a03_startup_syscall_log(&p,SYS_open,2,a,0,1);assert(!logs);
 strcpy(p.p_comm,"backboardd");a03_startup_syscall_log(&p,SYS_open,0,a,0,1);assert(!logs);
 a03_startup_syscall_log(&p,SYS_open,2,a,0,1);assert(logs==2&&strings==1&&last==0x1000);
 a03_startup_syscall_log(&p,SYS_openat,2,a,0,1);assert(strings==2&&last==0x2000);
 a[1]=7;a[2]=0x3000;a[3]=8;a03_startup_syscall_log(&p,SYS_csops,0,a,0,1);assert(headers==1);
 a[3]=7;a03_startup_syscall_log(&p,SYS_csops,0,a,0,1);assert(headers==1);
 a[0]=a[1]=a[2]=a[3]=0;logs=0;
 for(unsigned i=0;i<1000;i++)a03_startup_syscall_log(&p,99,2,a,0,1);
 assert(logs==188);
 const char *others[]={"containermanager","mediaserverd","notifyd","SpringBoard","analyticsd"};
 for(unsigned k=0;k<5;k++){strcpy(p.p_comm,others[k]);logs=0;
 for(unsigned i=0;i<1000;i++){a03_startup_syscall_log(&p,99,2,a,0,1);}assert(logs==192);}
 /* Fresh slots check actual pointer positions and do not treat fds as paths. */
 strcpy(p.p_comm,"mobileactivation");a[0]=0x1000;a[1]=0x1000;a[2]=0x3000;a[3]=16;
 logs=strings=headers=0;
 a03_startup_syscall_log(&p,SYS_setxattr,13,a,0,1);assert(logs==3&&strings==2&&last==0x1000);
 a[0]=7;a03_startup_syscall_log(&p,SYS_fsetxattr,13,a,0,1);assert(logs==5&&strings==3);
 a[0]=0x1000;a[1]=0x3000;
 a03_startup_syscall_log(&p,SYS_setattrlist,13,a,0,1);assert(headers==1&&last==0x3000);
 unsigned before=strings;a[0]=7;
 a03_startup_syscall_log(&p,SYS_fsetattrlist,13,a,0,1);assert(headers==2&&strings==before);
 a[1]=0x1000;a[2]=0x4000;
 a03_startup_syscall_log(&p,SYS_setattrlistat,13,a,0,1);assert(headers==3&&last==0x4000);
 a[0]=0x1000;a[1]=0x104;a[2]=0x5000;
 a03_startup_syscall_log(&p,SYS___mac_syscall,45,a,0,1);assert(headers==4&&last==0x1000);
 before=strings;a[2]=0xdead;
 a03_startup_syscall_log(&p,SYS___mac_syscall,45,a,0,1);assert(headers==5&&strings==before+1);
 a[0]=0;a[1]=0;a[2]=0;a[3]=0;logs=0;
 for(unsigned i=0;i<1000;i++)a03_startup_syscall_log(&p,99,2,a,0,1);
 assert(logs==185);
 const char *extra[]={"ScreenTimeAgent","dmd"};
 for(unsigned k=0;k<sizeof(extra)/sizeof(extra[0]);k++){strcpy(p.p_comm,extra[k]);logs=0;
 for(unsigned i=0;i<1000;i++)a03_startup_syscall_log(&p,99,2,a,0,1);assert(logs==192);}
 strcpy(p.p_comm,"PosterBoard");logs=0;a[0]=0x1000;a[1]=0x1000;
 for(unsigned i=0;i<1000;i++)a03_startup_syscall_log(&p,SYS_open,2,a,0,1);
 assert(logs==0);
 sample_path="/Library/Wallpaper/DefaultWallpapers~iphone.plist";
 a03_startup_syscall_log(&p,SYS_open,0,a,0,1);assert(logs==1);
 sample_path="/private/var/mobile/Library/PosterBoard/SwitcherConfiguration";
 for(unsigned i=0;i<1000;i++)a03_startup_syscall_log(&p,SYS_openat,2,a,0,1);
 assert(logs==192);
 puts("A03 actual startup diagnostics: opt-in/names/success filter/path argument/headers/xattr/attrlist/datavault/independent 192-report caps PASS");
}
'''
with tempfile.TemporaryDirectory(prefix='a03-startup-') as d:
 p=Path(d);(p/'test.c').write_text(header+source+tests)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p/'test.c'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True)
