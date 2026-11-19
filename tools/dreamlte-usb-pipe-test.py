#!/usr/bin/env python3
"""Exercise actual revision-scoped PIPE config, preservation and refusal."""
import pathlib,re,subprocess,sys,tempfile
source=pathlib.Path(sys.argv[1]).read_text()
match=re.search(r'\bdreamlte_usb_pipe_config\([^;{}]*\)\s*\{',source);assert match
at=source.index('{',match.start());end=at+1;depth=1
while depth:
 depth+=(source[end]=='{')-(source[end]=='}');end+=1
function=re.sub(r'__asm__ volatile\("[^"\n]*" ::: "memory"\);','',source[match.start():end])
code=r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef uintptr_t vm_offset_t;
static uint32_t regs[0x10000/4];
static unsigned bad_readback;
static uint32_t usb_rd(vm_offset_t base,unsigned off) {
 assert(base==(uintptr_t)regs);
 assert(off==0xc120 || off==0xc704 || off==0xc2c0);
 uint32_t v=regs[off/4];
 return off==0xc2c0 && bad_readback ? v & ~(1u<<28) : v;
}
'''+ 'static int\n'+function+r'''
int main(void) {
 for(unsigned i=0;i<33;i++) {
  memset(regs,0,sizeof(regs));regs[0xc120/4]=0x5533280a;
  uint32_t before=i==32?0x010c0002:1u<<i;
  regs[0xc2c0/4]=before;
  int result=dreamlte_usb_pipe_config((uintptr_t)regs);
  if(before&(1u<<31)) assert(result==-1 && regs[0xc2c0/4]==before);
  else assert(!result && regs[0xc2c0/4]==(before|(1u<<28)));
  for(unsigned n=0;n<sizeof(regs)/sizeof(*regs);n++)
   if(n!=0xc120/4 && n!=0xc2c0/4) assert(!regs[n]);
 }
 for(unsigned i=0;i<6;i++) {
  memset(regs,0,sizeof(regs));regs[0xc120/4]=i==0?0xffffffff:i==1?0x5533250a:0x5533280a;
  regs[0xc704/4]=i==2?1u<<31:i==3?1u<<30:0;
  uint32_t before=i==4?0xffffffff:0x010c0002;regs[0xc2c0/4]=before;bad_readback=i==5;
  assert(dreamlte_usb_pipe_config((uintptr_t)regs)==-1);
  assert(regs[0xc2c0/4]==(i==5?(before|1u<<28):before));
 }
 puts("PASS: actual PIPE config sets only bit28; all other bits preserved; wrong ID, running/reset, all-ones and readback mismatch refuse");
}
'''
start=source.index('static void\nsweet_usb_gadget_start(vm_offset_t dwc)')
startup=source[start:]
assert startup.index('dwc_wr(DCTL, DCTL_CSFTRST)')<startup.index('dreamlte_usb_pipe_config(dwc)')<startup.index('dreamlte_usb_resources()')
with tempfile.TemporaryDirectory(prefix='dreamlte-pipe-') as tmp:
 p=pathlib.Path(tmp);(p/'test.c').write_text(code)
 subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror',str(p/'test.c'),'-o',str(p/'test')],check=True)
 result=subprocess.run([str(p/'test')],capture_output=True,text=True,check=True);print(result.stdout.splitlines()[-1])
