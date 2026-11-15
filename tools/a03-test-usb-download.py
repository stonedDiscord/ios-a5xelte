#!/usr/bin/env python3
"""Host checks for actual0110 command parser and fixed SC2730 reset sequence."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix='a03-download-') as d:
 d=Path(d)
 for n in ('0103','0104','0106','0109','0110'):
  patch,=(root/'xnu/a03').glob(n+'-*.patch')
  subprocess.run(['git','apply','--include=bsd/dev/a03_usb_console.c',str(patch)],cwd=d,check=True)
 s=(d/'bsd/dev/a03_usb_console.c').read_text()
 parser=s[s.index('static char command_line'):s.index('static vm_offset_t usb;')]
 reset=s[s.index('static int download_reset('):s.index('static int usb_supply(')]
 header=r'''
#include <stdint.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
typedef int boolean_t;
#define FALSE 0
static int ml_set_interrupts_enabled(int e) { return e; }
static int adi=1, fail_read,fail_write,bad_readback;
static unsigned reads,writes,delays;
static uint32_t regs[3], offsets[3],values[3];
static unsigned slot(unsigned reg) {
 switch(reg) { case 0x1bac:return 0;case 0x1bf8:return 1;case 0x1824:return 2; }
 assert(0);return 3;
}
static int adi_read(unsigned reg,uint32_t *v) {
 unsigned n=slot(reg);reads++;if(fail_read && reads==(unsigned)fail_read)return 0;
 *v=regs[n] ^ (bad_readback && writes ? 1:0);return 1;
}
static int adi_write_raw(unsigned reg,uint32_t v) {
 unsigned n=slot(reg);assert(writes<3);offsets[writes]=reg;values[writes++]=v;
 if(fail_write && writes==(unsigned)fail_write)return 0;
 regs[n]=v;return 1;
}
static void delay(unsigned n) { assert(n==1000000);delays++; }
static void clear(void) {
 adi=1;fail_read=fail_write=bad_readback=0;reads=writes=delays=0;
 regs[0]=0xabf0;regs[1]=0x2240;regs[2]=0x3480;
}
'''
 tests=r'''
int main(void) {
 const char *c="download\r\n";while(*c)input_char(*c++);
 assert(download_requested && !command_available);download_requested=0;
 c="downloadx\n";while(*c)input_char(*c++);
 assert(!download_requested);char b[128];assert(a03_usb_debug_command(b,sizeof(b)));
 c="regs\n";while(*c)input_char(*c++);
 c="download\n";while(*c)input_char(*c++);
 assert(download_requested);assert(a03_usb_debug_command(b,sizeof(b))&&!strcmp(b,"regs"));
 clear();assert(!download_reset());assert(writes==3 && delays==1);
 assert(offsets[0]==0x1bac && values[0]==0xab30);
 assert(offsets[1]==0x1bf8 && values[1]==0x2250);
 assert(offsets[2]==0x1824 && values[2]==0x3481);
 for(int i=1;i<=3;i++) { clear();fail_read=i;download_reset();assert(!writes); }
 clear();bad_readback=1;download_reset();assert(writes==1 && !delays);
 clear();fail_write=1;download_reset();assert(writes==1 && !delays);
 clear();fail_write=2;download_reset();assert(writes==2 && !delays);
 clear();adi=0;download_reset();assert(!reads && !writes);
 puts("A03 USB download exact-command/fixed-reset-order/preserved-bits/fail-closed PASS (host only)");
}
'''
 p=d/'test.c';p.write_text(header+parser+reset+tests)
 subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror',str(p),'-o',str(d/'test')],check=True)
 subprocess.run([str(d/'test')],check=True)
