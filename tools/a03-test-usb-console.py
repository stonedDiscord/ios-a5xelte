#!/usr/bin/env python3
"""Host-only checks of A03 CDC descriptors/EP0 decisions; no hardware claim."""
from pathlib import Path
import re,subprocess,tempfile
root=Path(__file__).resolve().parent.parent
# Test the cumulative deployed source, including OUT monitor and PHY changes.
with tempfile.TemporaryDirectory(prefix='a03-cdc-source-') as d:
 for name in ('0103-a03-usb-cdc-console.patch',
              '0104-a03-post-trap-usb-monitor.patch',
              '0106-a03-usb-peripheral-phy-readback.patch'):
  subprocess.run(['git','apply','--include=bsd/dev/a03_usb_console.c',
                  str(root/'xnu/a03'/name)],cwd=d,check=True)
 source=(Path(d)/'bsd/dev/a03_usb_console.c').read_text()
source=re.sub(r'^#include .*\n','',source,flags=re.M)
source=source.replace('__asm__ volatile("dsb sy" ::: "memory");','')
start=source.index('static uint8_t r8(');end=source.index('static void update(',start)
source=source[:start]+'''static unsigned char regs[8192], fifo[512];static unsigned fifo_n;
static uint8_t r8(unsigned o) { return regs[o]; }
static uint16_t r16(unsigned o) { return regs[o]|(regs[o+1]<<8); }
static void w8(unsigned o,uint8_t v) { if(o==0x20)fifo[fifo_n++]=v;else regs[o]=v; }
static void w16(unsigned o,uint16_t v) { regs[o]=v;regs[o+1]=v>>8; }
'''+source[end:]
# Hardware startup and thread body are outside this protocol test.
source=source[:source.index('static void worker(')]+'\n#endif\n'
header='''#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <assert.h>
#define ARM64_BOARD_CONFIG_SWEET 1
typedef uintptr_t vm_offset_t;typedef size_t vm_size_t;typedef int boolean_t;
#define FALSE 0
static boolean_t ml_set_interrupts_enabled(boolean_t enabled) { return enabled; }
unsigned a03_console_read(unsigned char *p,unsigned n) { (void)p;(void)n;return 0; }
'''
tests='''
int main(void) {
 assert(sizeof(device_desc)==18);assert(sizeof(config_desc)==67);
 assert(le16(config_desc+2)==sizeof(config_desc));
 unsigned interfaces=0,eps=0;
 for(unsigned o=0;o<sizeof(config_desc);o+=config_desc[o]) {
  assert(config_desc[o]>=2 && o+config_desc[o]<=sizeof(config_desc));
  interfaces+=config_desc[o+1]==4;eps+=config_desc[o+1]==5;
 }
 assert(interfaces==2 && eps==3);
 unsigned char getdev[8]={0x80,6,0,1,0,0,18,0};setup(getdev);
 assert(fifo_n==18 && !control_active && r16(0x12)==0x0a);
 fifo_n=0;unsigned char getcfg[8]={0x80,6,0,2,0,0,255,0};setup(getcfg);
 assert(fifo_n==64 && control_active);control_send();assert(fifo_n==67 && !control_active);
 fifo_n=0;getcfg[6]=64;setup(getcfg);assert(fifo_n==64 && !control_active && r16(0x12)==0x0a);
 unsigned char setaddr[8]={0,5,12,0,0,0,0,0};setup(setaddr);
 assert(address_valid && address_pending==12 && r16(0x12)==0x48);
 unsigned char setcfg[8]={0,9,1,0,0,0,0,0};setup(setcfg);assert(configured==1);
 unsigned char setline[8]={0x21,0x20,0,0,0,0,7,0};setup(setline);assert(control_out);
 unsigned char setdtr[8]={0x21,0x22,1,0,0,0,0,0};setup(setdtr);assert(r16(0x12)==0x48);
 fifo_n=0;unsigned char getstr[8]={0x80,6,2,3,9,4,255,0};setup(getstr);assert(fifo_n==32);
 unsigned char bad[8]={0x80,6,0,99,0,0,1,0};setup(bad);assert(r16(0x12)==0x60);
 assert(setup_count==9);
 input_char('r');input_char('e');input_char('g');input_char('s');input_char('\\n');
 char cmd[128];assert(a03_usb_debug_command(cmd,sizeof(cmd)) && cmd[0]=='r');
 puts("A03 cumulative CDC descriptor/control-request/command checks PASS (host only)");
}
'''
with tempfile.TemporaryDirectory(prefix='a03-cdc-test-') as d:
 p=Path(d)/'test.c';p.write_text(header+source+tests)
 subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Wno-unused-function','-Wno-unused-variable',str(p),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
