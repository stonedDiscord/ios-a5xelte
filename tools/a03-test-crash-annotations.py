#!/usr/bin/env python3
"""Run actual 0118 annotation reader against bounded synthetic user mappings."""
from pathlib import Path
import subprocess
import tempfile
root = Path(__file__).resolve().parent.parent
patch = (root/'xnu/a03/0118-a03-bounded-crash-annotations.patch').read_text()
source = '\n'.join(x[1:] for x in patch.splitlines() if x.startswith('+') and not x.startswith('+++'))
# Apply the follow-on selector extension to the actual extracted helper.
with tempfile.TemporaryDirectory(prefix='a03-annotation-patch-') as directory:
    d=Path(directory);p=d/'osfmk/kern/exception.c';p.parent.mkdir(parents=True)
    p.write_text(source)
    subprocess.run(['git','apply','--unidiff-zero',str(root/'xnu/a03/0119-a03-framework-crash-annotations.patch')],cwd=d,check=True)
    subprocess.run(['git','apply','--include=osfmk/kern/exception.c',str(root/'xnu/a03/0139-a03-filesystem-startup-evidence.patch')],cwd=d,check=True)
    source=p.read_text()
source = source[source.index('/* Read current-task'):source.index('\n\ta03_crash_annotations(name, task->')]
header = r'''
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
 memcpy(out,memory+(address-0x100000),size);return 0;
}
static int copyinstr(user_addr_t address,char *out,size_t size,vm_size_t *copied) {
 for(size_t i=0;i<size;i++){if(copyin(address+i,out+i,1))return 1;if(!out[i]){*copied=i+1;return 0;}}
 return 1;
}
static int logline(const char *format,...) {
 va_list ap;char record[256];va_start(ap,format);int result=vsnprintf(record,sizeof(record),format,ap);va_end(ap);assert(result>=0&&(size_t)result<sizeof(record));assert(strlen(output)+strlen(record)<sizeof(output));strcat(output,record);
 if(strstr(format,"annotation%u:"))messages++;
 return result;
}
#define printf logline
'''
tests = r'''
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
 a03_crash_image("test",0x100000);assert(messages==2);assert(strstr(output,"termination reason"));assert(strstr(output,"second message"));
 /* Reproduce a nested NSError longer than a single console record. */
 info[4]=0;memset(memory+8192,'A',400);strcpy((char*)memory+8592,"NSPOSIXErrorDomain Code=13 path=/private/var/test");
 output[0]=0;messages=0;a03_crash_image("mobileactivation",0x100000);
 assert(messages==3&&strstr(output,"NSPOSIXErrorDomain Code=13")&&strstr(output,"path=/private/var/test"));
 messages=0;info[0]=4;a03_crash_image("test",0x100000);assert(!messages);info[0]=5;
 info[1]=UINT64_MAX;info[4]=0;a03_crash_image("test",0x100000);assert(!messages);
 info[1]=0x102000;memset(memory+8192,'A',1024);output[0]=0;a03_crash_image("test",0x100000);assert(messages==7&&strstr(output,"[bounded]")&&strstr(output,"[continued]"));
 messages=0;seg->cmdsize=8;a03_crash_image("test",0x100000);assert(!messages);seg->cmdsize=152;
 seg->nsects=129;a03_crash_image("test",0x100000);assert(!messages);seg->nsects=1;
 sec->size=UINT64_MAX;a03_crash_image("test",0x100000);assert(!messages);sec->size=64;
 mh->ncmds=129;reads=0;a03_crash_image("test",0x100000);assert(reads==1);mh->ncmds=1;
 uint32_t *all=(void*)(memory+12288);all[0]=17;all[1]=2049;((uint64_t*)all)[1]=0x103100;
 reads=0;a03_crash_annotations("test",0x103000,16,0);assert(reads==1);
 all[1]=1;uint64_t *image=(void*)(memory+12544);image[0]=0x100000;image[1]=0x103200;
 strcpy((char*)memory+12800,"/usr/lib/libc++abi.dylib");output[0]=0;messages=0;
 a03_crash_annotations("test",0x103000,16,0);assert(messages==7&&strstr(output,"images 1 matches 1"));
 all[1]=2048;((uint64_t*)all)[1]=UINT64_MAX-8;reads=0;a03_crash_annotations("test",0x103000,16,0);assert(reads==1);

 /* Real shared caches put annotations in a separate __DATA segment. */
 all[1]=1;((uint64_t*)all)[1]=0x103100;
 mh->ncmds=2;mh->sizeofcmds=224;seg->cmdsize=72;seg->nsects=0;
 struct segment_command_64 *data=(void*)(memory+104);
 memset(data,0,152);data->cmd=LC_SEGMENT_64;data->cmdsize=152;
 strcpy(data->segname,"__DATA");data->vmaddr=0x2000;data->vmsize=64;data->nsects=1;
 sec=(void*)(memory+176);strcpy(sec->sectname,"__crash_info");strcpy(sec->segname,"__DATA");sec->addr=0x2000;sec->size=64;
 output[0]=0;messages=0;a03_crash_annotations("test",0x103000,16,0);
 assert(messages==7&&strstr(output,"images 1 matches 1"));

 const char *paths[]={"/usr/lib/libc++abi.dylib","/usr/lib/libobjc.A.dylib",
 "/usr/lib/system/libsystem_c.dylib","/System/Library/Frameworks/Foundation.framework/Foundation",
 "/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation",
 "/System/Library/Frameworks/QuartzCore.framework/QuartzCore"};
 for(unsigned k=0;k<6;k++) {strcpy((char*)memory+12800,paths[k]);output[0]=0;messages=0;
 a03_crash_annotations("test",0x103000,16,0);assert(messages==7&&strstr(output,"matches 1"));}
 strcpy((char*)memory+12800,"/unselected.dylib");output[0]=0;messages=0;
 a03_crash_annotations("test",0x103000,16,0);assert(!messages&&strstr(output,"matches 0"));
 puts("A03 actual annotation parser: layout/slide/messages/sanitization/caps/malformed/fault/overflow PASS");
}
'''
with tempfile.TemporaryDirectory(prefix='a03-annotations-') as directory:
    d=Path(directory)
    (d/'test.c').write_text(header+source+tests)
    subprocess.run(['clang','-fsanitize=address,undefined','-std=c11','-Wall','-Wextra','-Werror',str(d/'test.c'),'-o',str(d/'test')],check=True)
    subprocess.run([str(d/'test')],check=True)
