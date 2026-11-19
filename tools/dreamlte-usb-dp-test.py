#!/usr/bin/env python3
"""Actual Samsung DP pull-up helper: field preservation, invalid-read refusal and placement."""
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
#include <stdio.h>
#include <assert.h>
typedef uintptr_t vm_offset_t;
static uint32_t regs[64];
static vm_offset_t dreamlte_phy;
static unsigned reads, bad;
static uint32_t usb_rd(vm_offset_t base,unsigned off) {
 assert(base==(uintptr_t)regs && off==8);reads++;
 uint32_t v=regs[2];return bad&&reads==2?v^(1u<<9):v;
}
'''
code+='static int\n'+function('dreamlte_usb_dp_pullup')+r'''
int main(void) {
 assert(dreamlte_usb_dp_pullup(false)==-1);
 dreamlte_phy=(uintptr_t)regs;
 for(unsigned i=0;i<65536;i++) for(unsigned enabled=0;enabled<2;enabled++) {
  uint32_t original=(i*2654435761u)&~(1u<<31);
  regs[2]=original;reads=0;bad=0;
  assert(dreamlte_usb_dp_pullup(enabled)==0 && reads==2);
  uint32_t expected=enabled?original|(1u<<9):original&~(1u<<9);
  assert(regs[2]==expected && !((original^regs[2])&~(1u<<9)));
 }
 regs[2]=0xffffffffu;reads=0;assert(dreamlte_usb_dp_pullup(true)==-1&&reads==1&&regs[2]==0xffffffffu);
 regs[2]=0x660;reads=0;bad=1;assert(dreamlte_usb_dp_pullup(false)==-1);
}
'''
with tempfile.TemporaryDirectory() as d:
 p=pathlib.Path(d);(p/'test.c').write_text(code)
 subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror',str(p/'test.c'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True,stdout=subprocess.DEVNULL)
startup=function('sweet_usb_gadget_start');assert startup.index('dreamlte_usb_resources()')<startup.index('dreamlte_usb_dp_pullup(false)')<startup.index('dwc_wr(DCTL, dwc_rd(DCTL) | DCTL_RUN_STOP)')
event=function('ud_event');reset=event[event.index('if (type == 1)'):event.index('else if (type == 2)')];assert reset.index('dwc_wr(DCFG')<reset.index('dreamlte_usb_dp_pullup(true)')
connect=event[event.index('else if (type == 2)'):event.index('else if (type == 0)')];assert 'speed == 0 && dreamlte_usb_dp_pullup(false)' in connect
print('PASS: actual DP helper131072 preservation cases, invalid/mismatch refusal and source-backed reset/connect/start placement')
