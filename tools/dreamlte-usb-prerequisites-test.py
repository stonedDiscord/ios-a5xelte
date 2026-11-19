#!/usr/bin/env python3
"""Exercise actual isolation/reference writes, preservation, ordering and refusal."""
import pathlib,re,subprocess,sys,tempfile
s=pathlib.Path(sys.argv[1]).read_text();m=re.search(r'\bdreamlte_usb_prerequisites\([^;{}]*\)\s*\{',s);assert m
a=s.index('{',m.start());b=a+1;depth=1
while depth:
 depth+=(s[b]=='{')-(s[b]=='}');b+=1
f=re.sub(r'__asm__ volatile\("[^"\n]*" ::: "memory"\);','',s[m.start():b])
code=r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef uintptr_t vm_offset_t;
static uint32_t core[0x10000/4],pmu[0x1000/4],ref[4];
static vm_offset_t dreamlte_usb_pmu,dreamlte_usb_refsel;
static unsigned bad,iso_reads,ref_reads;
static uint32_t usb_rd(vm_offset_t base,unsigned off) {
 if(base==(uintptr_t)core) {assert(off==0xc120||off==0xc704);return core[off/4];}
 if(base==dreamlte_usb_pmu) {assert(off==0x704);iso_reads++;return pmu[off/4] & ~(bad==1 && iso_reads>1?1u:0u);}
 assert(base==dreamlte_usb_refsel&&off==0xc);ref_reads++;
 if(ref_reads>1) assert(iso_reads==2 && (pmu[0x704/4]&1));
 return ref[3]&~(bad==2&&ref_reads>1?1u<<24:0u);
}
'''+ 'static int\n'+f+r'''
static void reset(void) {
 memset(core,0,sizeof(core));memset(pmu,0,sizeof(pmu));memset(ref,0,sizeof(ref));
 core[0xc120/4]=0x5533280a;dreamlte_usb_pmu=(uintptr_t)pmu;dreamlte_usb_refsel=(uintptr_t)ref;
 bad=iso_reads=ref_reads=0;
}
int main(void) {
 for(unsigned bit=0;bit<33;bit++) {
  reset();uint32_t x=bit==32?0:1u<<bit;pmu[0x704/4]=ref[3]=x;
  assert(!dreamlte_usb_prerequisites((uintptr_t)core));
  assert(pmu[0x704/4]==(x|1u)&&ref[3]==(x|1u<<24));
  for(unsigned n=0;n<sizeof(pmu)/4;n++) if(n!=0x704/4) assert(!pmu[n]);
  for(unsigned n=0;n<3;n++) assert(!ref[n]);
 }
 for(unsigned mode=0;mode<7;mode++) {
  reset();
  if(mode==0)core[0xc120/4]=0xffffffff;
  if(mode==1)core[0xc704/4]=1u<<31;
  if(mode==2)core[0xc704/4]=1u<<30;
  if(mode==3)pmu[0x704/4]=0xffffffff;
  if(mode==4)ref[3]=0xffffffff;
  if(mode>=5)bad=mode-4;
  uint32_t x=pmu[0x704/4],y=ref[3];
  assert(dreamlte_usb_prerequisites((uintptr_t)core)==-1);
  if(mode<5)assert(pmu[0x704/4]==x&&ref[3]==y);
  if(mode==5)assert(pmu[0x704/4]==1&&ref[3]==0&&ref_reads==1);
  if(mode==6)assert(pmu[0x704/4]==1&&ref[3]==1u<<24);
 }
 puts("PASS: actual prerequisite masks preserve unrelated bits; stopped/ID/all-ones guards; isolation verified before reference; failed readback stops");
}
'''
probe=s[s.index('void\nsweet_usb_probe(void)'):s.index('#else\nvoid\nsweet_usb_probe(void)')]
assert probe.index('if (id !=')<probe.index('dreamlte_usb_prerequisites(dwc)')<probe.index('!dreamlte_usb_prepare(dwc)')
with tempfile.TemporaryDirectory(prefix='dreamlte-prereq-') as tmp:
 p=pathlib.Path(tmp);(p/'test.c').write_text(code)
 subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror',str(p/'test.c'),'-o',str(p/'test')],check=True)
 r=subprocess.run([str(p/'test')],capture_output=True,text=True,check=True);print(r.stdout.splitlines()[-1])
