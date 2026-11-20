#!/usr/bin/env python3
"""Exercise actual passive MUIC helper against guarded MMIO banks."""
import pathlib
import subprocess
import sys
import tempfile

source = pathlib.Path(sys.argv[1]).read_text()
start = source.index('static bool\ndreamlte_muic_gate_ready')
end = source.index('/* Samsung CAL exynos_cal_usbphy', start)
helper = source[start:end]
assert 'usb_wr' not in helper and 'dwc_wr' not in helper
code = r'''
#include <stdint.h>
#include <stdbool.h>
#include <assert.h>
#include <stdio.h>
typedef uintptr_t vm_offset_t;
static vm_offset_t dreamlte_muic_cmu=1, dreamlte_muic_gpio=2, dreamlte_muic_i2c=3;
static uint32_t bus, pclk, gpio, syncgate;
static unsigned pinreads, i2creads, cmureads;
/* Explicit oracle: CG_VAL, MANUAL, AUTO bits index this table.
 * Require observed CG_VAL and Samsung ra_get_gate(pass=1). */
static bool ready(uint32_t v) {
 const bool allowed[8]={false,true,false,true,false,false,false,true};
 unsigned i=((v>>21)&1)|(((v>>20)&1)<<1)|(((v>>28)&1)<<2);
 return v!=0xffffffffu && allowed[i];
}
static uint32_t usb_rd(vm_offset_t base, unsigned off) {
 if(base==1) {
  cmureads++;
  switch(off) {
   case 0x100:return bus; case 0x20cc:return pclk; case 0x2028:return gpio;
   case 0x2044:return syncgate; case 0x20d0:case 0x3068:return 0;
   default:assert(0);
  }
 }
 assert(!(bus&(1u<<7)) && bus!=0xffffffffu && ready(syncgate));
 if(base==2) {assert(ready(gpio));assert(off==0xc0||off==0xc4||off==0xc8);pinreads++;}
 else {assert(base==3 && ready(pclk));assert(off==0||off==0x40||off==0x44||off==0x70||off==0x60||off==0x64||off==0x68||off==0x6c);i2creads++;}
 return 0;
}
'''+helper+r'''
int main(void) {
 uint32_t gates[9];
 for(unsigned i=0;i<8;i++) gates[i]=((i&1)?1u<<21:0)|((i&2)?1u<<20:0)|((i&4)?1u<<28:0);
 gates[8]=0xffffffffu;
 for(unsigned i=0;i<9;i++) assert(dreamlte_muic_gate_ready(gates[i])==ready(gates[i]));
 uint32_t buses[]={0,1u<<4,1u<<7,0xffffffffu};
 for(unsigned b=0;b<4;b++) for(unsigned g=0;g<9;g++)
 for(unsigned p=0;p<9;p++) for(unsigned y=0;y<9;y++) for(unsigned maps=0;maps<8;maps++) {
  bus=buses[b];gpio=gates[g];pclk=gates[p];syncgate=gates[y];
  dreamlte_muic_cmu=(maps&1)?1:0;dreamlte_muic_gpio=(maps&2)?2:0;dreamlte_muic_i2c=(maps&4)?3:0;
  cmureads=pinreads=i2creads=0;dreamlte_muic_preflight("model");
  bool common=(maps&1)&&b<2&&ready(syncgate);
  assert(cmureads==((maps&1)?6u:0u));
  assert(pinreads==((common&&(maps&2)&&ready(gpio))?3u:0u));
  assert(i2creads==((common&&(maps&4)&&ready(pclk))?8u:0u));
 }
}
'''
with tempfile.TemporaryDirectory() as directory:
    path = pathlib.Path(directory)
    (path / 'test.c').write_text(code)
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', str(path / 'test.c'), '-o', str(path / 'test')], check=True)
    subprocess.run([str(path / 'test')], check=True, stdout=subprocess.DEVNULL)
print('PASS: 23328 actual-helper combinations; gated/unstable/unmapped banks refused; reads allowlisted')
