#!/usr/bin/env python3
"""Run the actual EP0 request and PMU reset helpers with modeled hardware."""
import pathlib,re,subprocess,sys,tempfile
s=pathlib.Path(sys.argv[1]).read_text()
def function(name):
    m=re.search(r'\b'+name+r'\([^;{}]*\)\s*\{',s);assert m
    a=s.index('{',m.start());b=a+1;d=1
    while d:
        d+=(s[b]=='{')-(s[b]=='}');b+=1
    return re.sub(r'__asm__ volatile\("[^"\n]*" ::: "memory"\);','',s[m.start():b])
code=r'''
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>
#define DREAMLTE 1
#define UD_SETUP 0
#define UD_DATA 64
#define DCFG 0
#define TRBCTL_DATA 0
#define EP0_WAIT_STATUS2 1
#define EP0_DATA 2
static uint8_t dma[512];
static struct { uintptr_t dma; bool data_in,configured; unsigned data_alt,state; void *lock; bool tx_busy; } ud;
static uint8_t ud_dev_desc[1],ud_cfg_desc[1];
static unsigned dreamlte_reboot_pending,dreamlte_reboot_mode,dreamlte_reboot_delay,stalled,starts;
#define DSTS 0
#define EP_RX 2
#define EP_TX 3
#define DEPCMD_SETEPCONFIG 1
#define EP0_SETUP 0
#define EP0_WAIT_STATUS3 3
#define EP0_STATUS 4
#define TRBCTL_STATUS2 0
#define TRBCTL_STATUS3 0
static void ud_rx_done(void) {}
static void ud_tx_kick_locked(void) {}
static void lck_mtx_lock(void*p) {(void)p;}
static void lck_mtx_unlock(void*p) {(void)p;}
static void ud_start_setup(void) {}
static void ud_sync(unsigned a,unsigned b) {(void)a;(void)b;}
static void ud_epcmd(unsigned a,unsigned b,unsigned c,unsigned d,unsigned e) {(void)a;(void)b;(void)c;(void)d;(void)e;}
static uintptr_t dreamlte_usb_pmu;
static uint32_t pmu[1024];
static uint32_t usb_rd(uintptr_t p,unsigned off) {return *(uint32_t*)(p+off);}
static uint32_t dwc_rd(unsigned o) {(void)o;return 0;}
static void dwc_wr(unsigned o,uint32_t v) {(void)o;(void)v;}
static void ud_configure(void) {}
static void ud_notify_connected(void) {}
static void ud_link_event(bool b) {(void)b;}
static unsigned ud_string(unsigned i,void*p) {(void)i;(void)p;return 0;}
static void ud_stall(void) {stalled++;}
static void ud_start(unsigned e,unsigned b,unsigned n,unsigned c) {(void)e;(void)b;(void)n;(void)c;starts++;}
'''
code += 'static int dreamlte_usb_console_read(uint8_t r,uint16_t v,uint16_t i,uint16_t l,uint8_t*d) {(void)r;(void)v;(void)i;(void)l;(void)d;return -1;}\n'
code += 'static int dreamlte_usb_dp_pullup(bool enable) {(void)enable;return 0;}\n'
code+='static void\n'+function('ud_setup')+'\nstatic void\n'+function('dreamlte_usb_reboot')+'\nstatic void\n'+function('ud_event')+r'''
int main(void) {
 ud.dma=(uintptr_t)dma;
 for(unsigned flags=0;flags<16;flags++) for(unsigned mode=1;mode<=2;mode++) {
  ud.state=EP0_STATUS;dreamlte_reboot_pending=mode;dreamlte_reboot_mode=dreamlte_reboot_delay=0;
  ud_event((1u<<1)|(1u<<6)|(flags<<12));
  if(flags&3u) assert(dreamlte_reboot_mode==0 && dreamlte_reboot_delay==0);
  else assert(dreamlte_reboot_mode==mode && dreamlte_reboot_delay==100 && !dreamlte_reboot_pending);
 }
 for(unsigned type=0;type<=1;type++) {
  dreamlte_reboot_pending=dreamlte_reboot_mode=dreamlte_reboot_delay=2;
  ud_event(1u|(type<<8));
  assert(!dreamlte_reboot_pending&&!dreamlte_reboot_mode&&!dreamlte_reboot_delay);
 }

 for(unsigned type=0;type<256;type++) for(unsigned req=0x50;req<=0x51;req++)
 for(unsigned value=0;value<3;value++) for(unsigned idx=0;idx<2;idx++) for(unsigned len=0;len<2;len++) {
  memset(dma,0,sizeof dma);stalled=starts=0;dreamlte_reboot_pending=99;
  dma[0]=type;dma[1]=req;dma[2]=value;dma[4]=idx?0x95:0;dma[5]=idx?0x88:0;dma[6]=len?8:0;
  ud_setup();
  bool reset=type==0x40 && req==0x51 && value<=1 && idx && !len;
  bool caps=type==0xc0 && req==0x50 && !value && idx && len;
  assert(dreamlte_reboot_pending==(reset?value+1:0));
  if(reset) assert(!stalled && !starts && ud.state==EP0_WAIT_STATUS2);
  if(caps) assert(!stalled && starts==1 && !memcmp(dma+UD_DATA,"DUSB\1\3\0\0",8));
 }
 dreamlte_usb_pmu=(uintptr_t)pmu;
 for(unsigned mode=0;mode<4;mode++) {
  memset(pmu,0,sizeof pmu);dreamlte_usb_reboot(mode);
  if(mode==1||mode==2) {
   assert(pmu[0x808/4]==0x12345678 && pmu[0x80c/4]==(mode==2?0x12345671u:0x12345670u));
   assert(pmu[0x400/4]==1);
  } else for(unsigned i=0;i<1024;i++) assert(!pmu[i]);
 }
 puts("PASS: actual EP0 capability/reboot request validation and PMU normal/download flags");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=pathlib.Path(d);(p/'test.c').write_text(code)
 subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror',str(p/'test.c'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True,stdout=subprocess.DEVNULL)
event=function('ud_event');assert 'dreamlte_reboot_pending && !(status & 3u)' in event
assert event.index('case EP0_STATUS:') < event.index('dreamlte_reboot_delay = 100;')
assert event.count('dreamlte_reboot_pending = dreamlte_reboot_mode = dreamlte_reboot_delay = 0;')==2
print('PASS: actual request validation/PMU helpers; all16 completion flag combinations and both modes; reset/disconnect cancellation')
