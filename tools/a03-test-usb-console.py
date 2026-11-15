#!/usr/bin/env python3
"""Host-only checks of A03 CDC descriptors/EP0 decisions; no hardware claim."""
from pathlib import Path
import re,subprocess,tempfile
root=Path(__file__).resolve().parent.parent
# Test the cumulative deployed source, including OUT monitor and PHY changes.
with tempfile.TemporaryDirectory(prefix='a03-cdc-source-') as d:
 for name in ('0103-a03-usb-cdc-console.patch',
              '0104-a03-post-trap-usb-monitor.patch',
              '0106-a03-usb-peripheral-phy-readback.patch',
              '0109-a03-usb-supply-flat-endpoints.patch',
              '0110-a03-usb-download-command.patch',
              '0111-a03-usb-receive-diagnostics.patch',
              '0113-a03-usb-pio-takeover.patch',
              '0115-a03-download-control-escape.patch'):
  subprocess.run(['git','apply','--include=bsd/dev/a03_usb_console.c',
                  str(root/'xnu/a03'/name)],cwd=d,check=True)
 source=(Path(d)/'bsd/dev/a03_usb_console.c').read_text()
source=re.sub(r'^#include .*\n','',source,flags=re.M)
source=source.replace('__asm__ volatile("dsb sy" ::: "memory");','')
a=source.index('/* Live DT uses sharkl5');b=source.index('static unsigned le16(',a)
source=source[:a]+source[b:]
start=source.index('static uint8_t r8(');end=source.index('static void update(',start)
source=source[:start]+'''static unsigned char regs[8192], fifo[512], rx_fifo[128];static unsigned fifo_n, rx_pos;
static uint8_t r8(unsigned o) { if(o==0x24)return rx_fifo[rx_pos++];return regs[o]; }
static uint16_t r16(unsigned o) { return regs[o]|(regs[o+1]<<8); }
static void w8(unsigned o,uint8_t v) { if(o==0x20)fifo[fifo_n++]=v;else regs[o]=v; }
static void w16(unsigned o,uint16_t v) { regs[o]=v;regs[o+1]=v>>8; }
'''+source[end:]
# Hardware startup and thread body are outside this protocol test.
source=source[:source.index('static void worker(')]+'\n#endif\n'
header='''#include <stdint.h>
#include <string.h>
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
 usb=(uintptr_t)regs;
 for(unsigned i=0;i<30;i++){uint32_t value=0x1001;memcpy(regs+0x1c04+i*0x20,&value,4);}
 assert(pio_takeover());
 for(unsigned i=0;i<30;i++){uint32_t value;memcpy(&value,regs+0x1c04+i*0x20,4);assert(value==0x1000);}
 assert(ep_read(1,2)==0 && ep_read(1,6)==0);
 assert(ep_reg(0,2)==0x102 && ep_reg(1,6)==0x116 && ep_reg(2,2)==0x122);
 assert(sizeof(device_desc)==18);assert(sizeof(config_desc)==67);
 assert(le16(config_desc+2)==sizeof(config_desc));
 unsigned interfaces=0,eps=0;
 for(unsigned o=0;o<sizeof(config_desc);o+=config_desc[o]) {
  assert(config_desc[o]>=2 && o+config_desc[o]<=sizeof(config_desc));
  interfaces+=config_desc[o+1]==4;eps+=config_desc[o+1]==5;
 }
 assert(interfaces==2 && eps==3);
 unsigned char getdev[8]={0x80,6,0,1,0,0,18,0};setup(getdev);
 assert(fifo_n==18 && !control_active && ep_read(0,2)==0x0a);
 fifo_n=0;unsigned char getcfg[8]={0x80,6,0,2,0,0,255,0};setup(getcfg);
 assert(fifo_n==64 && control_active);control_send();assert(fifo_n==67 && !control_active);
 fifo_n=0;getcfg[6]=64;setup(getcfg);assert(fifo_n==64 && !control_active && ep_read(0,2)==0x0a);
 unsigned char setaddr[8]={0,5,12,0,0,0,0,0};setup(setaddr);
 assert(address_valid && address_pending==12 && ep_read(0,2)==0x48);
 unsigned char setcfg[8]={0,9,1,0,0,0,0,0};setup(setcfg);assert(configured==1);
 assert(ep_read(1,0)==64 && ep_read(1,4)==64 && ep_read(2,0)==16);
 assert(ep_read(1,2)==0x2048 && ep_read(1,6)==0x90 && ep_read(2,2)==0x2048);
 unsigned char setline[8]={0x21,0x20,0,0,0,0,7,0};setup(setline);assert(control_out);
 unsigned char setdtr[8]={0x21,0x22,1,0,0,0,0,0};setup(setdtr);assert(ep_read(0,2)==0x48);
 fifo_n=0;unsigned char getstr[8]={0x80,6,2,3,9,4,255,0};setup(getstr);assert(fifo_n==32);
 unsigned char bad[8]={0x80,6,0,99,0,0,1,0};setup(bad);assert(ep_read(0,2)==0x60);
 assert(setup_count==9);
 /* A reset must clear address/configuration and rebuild independent banks. */
 regs[0x0a]=4;poll_usb();regs[0x0a]=0;
 assert(reset_count==1 && !configured && !address_valid && regs[0]==0);
 assert(ep_read(1,0)==64 && ep_read(2,0)==16);
 /* SET_ADDRESS is committed only after the EP0 status transaction ends. */
 setup(setaddr);poll_usb();assert(address_valid && regs[0]==0);
 ep_write(0,2,0);poll_usb();assert(!address_valid && regs[0]==12);
 /* Bulk EP1 activity cannot overwrite EP0 CSR in the flat mapping. */
 setup(setcfg);ep_write(0,2,0);ep_write(1,6,0);ep_write(1,2,1);
 poll_usb();assert(ep_read(0,2)==0 && ep_read(1,2)==1);

 /* Exercise real poll_usb FIFO -> parser delivery, including split packets. */
 memcpy(rx_fifo,"down",4);rx_pos=0;ep_write(1,8,4);ep_write(1,6,1);poll_usb();
 assert(!download_requested && rx_pos==4 && ep_read(1,6)==0);
 memcpy(rx_fifo,"load\\n",5);rx_pos=0;ep_write(1,8,5);ep_write(1,6,1);poll_usb();
 assert(download_requested && rx_pos==5 && ep_read(1,6)==0);download_requested=0;
 /* Invalid oversized packet is drained but cannot request a reset. */
 memset(rx_fifo,'x',65);memcpy(rx_fifo,"download\\n",9);rx_pos=0;
 ep_write(1,8,65);ep_write(1,6,1);poll_usb();assert(!download_requested && rx_pos==65);
 unsigned char resetctl[8]={0x21,0x23,0xff,0xff,0,0,0,0};
 setup(resetctl);assert(download_requested && ep_read(0,2)==0x48);download_requested=0;
 resetctl[2]=resetctl[3]=0;setup(resetctl);assert(!download_requested);
 input_char('r');input_char('e');input_char('g');input_char('s');input_char('\\n');
 char cmd[128];assert(a03_usb_debug_command(cmd,sizeof(cmd)) && cmd[0]=='r');
 puts("A03 cumulative CDC descriptor/control-request/command checks PASS (host only)");
}
'''
with tempfile.TemporaryDirectory(prefix='a03-cdc-test-') as d:
 p=Path(d)/'test.c';p.write_text(header+source+tests)
 subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Wno-unused-function','-Wno-unused-variable',str(p),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
