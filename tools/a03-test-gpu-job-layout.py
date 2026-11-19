#!/usr/bin/env python3
"""Check actual A03 private GPU table/WRITE_VALUE bytes; no hardware claim."""
from pathlib import Path
import argparse,subprocess,tempfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--mesa-xml',type=Path,help='optional primary Mesa job XML provenance check')
args=parser.parse_args()
if args.mesa_xml:
 tree=ET.parse(args.mesa_xml).getroot()
 def node(tag,name):return next(n for n in tree.findall(tag) if n.get('name')==name)
 def field(name,label):return next(n for n in node('struct',name).findall('field') if n.get('name')==label)
 assert field('Job Header','Type').get('start')=='4:1'
 assert field('Job Header','Index').get('start')=='4:16'
 assert field('Write Value Job Payload','Address').get('start')=='0:0'
 assert field('Write Value Job Payload','Type').get('start')=='2:0'
 assert field('Write Value Job Payload','Immediate Value').get('start')=='4:0'
 assert next(n for n in node('enum','Write Value Type').findall('value') if n.get('name')=='Immediate 64').get('value')=='7'
 assert next(n for n in node('aggregate','Write Value Job').findall('section') if n.get('name')=='Payload').get('offset')=='32'
 assert node('struct','Job Header').get('align')=='128', 'G57 requires v9 schema'
 assert not any(n.get('name')=='Is 64b' for n in node('struct','Job Header').findall('field'))
 print('PASS primary Mesa v9 G57 header/reserved bit/type/index/address/immediate field correspondence')

source='''
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include "a03-gpu-job-layout.h"
static uint64_t walk(void *mem,uint64_t pa,uint64_t va){
 uint64_t table=pa;
 for(unsigned level=0;level<4;level++){
  assert(table>=pa&&table<pa+0x4000);
  uint64_t d=*(uint64_t *)((uint8_t*)mem+(table-pa)+8*((va>>(39-9*level))&511));
  if((d&3)!=3)return 0;
  if(level==3)return (d&0x000000fffffff000ULL)|(va&4095);
  assert(d&0x400);table=d&0x000000fffffff000ULL;
 }
 assert(0);return 0;
}
int main(void){
 uint8_t *mem=aligned_alloc(0x4000,A03_GPU_SCRATCH_SIZE);assert(mem);
 for(unsigned trial=0;trial<1024;trial++){
  uint64_t pa=0x102000000ULL+trial*0x4000ULL;assert(a03_gpu_job_layout(mem,pa));
  assert(walk(mem,pa,A03_GPU_JOB_VA)==pa+0x4000);
  assert(walk(mem,pa,A03_GPU_OUTPUT_VA)==pa+0x5000);
  assert(!walk(mem,pa,0)&&!walk(mem,pa,A03_GPU_JOB_VA-4096)&&!walk(mem,pa,A03_GPU_OUTPUT_VA+4096));
  uint32_t *job=(uint32_t *)(mem+0x4000);
  assert(job[0]==0&&job[4]==0x10004&&job[5]==0&&job[6]==0&&job[7]==0);
  assert(*(uint64_t *)(job+8)==A03_GPU_OUTPUT_VA&&job[10]==7&&job[11]==0);
  assert(*(uint64_t *)(job+12)==A03_GPU_RESULT);
  assert(*(uint64_t *)(mem+0x5000)==A03_GPU_CANARY);
  uint64_t *l3=(uint64_t *)(mem+0x3000);assert((l3[0]&0xfff)==0x457&&(l3[0]&(1ULL<<54)));
 }
 assert(!a03_gpu_job_layout(0,0x102000000ULL));assert(!a03_gpu_job_layout(mem,0));
 assert(!a03_gpu_job_layout(mem,0x102000001ULL));assert(!a03_gpu_job_layout(mem,1ULL<<40));
 assert(!a03_gpu_job_layout(mem+1,0x102000000ULL));free(mem);return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='a03-job-layout-') as d:
 t=Path(d);(t/'test.c').write_text(source)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I',str(ROOT/'tools'),str(t/'test.c'),'-o',str(t/'test')],check=True)
 subprocess.run([str(t/'test')],check=True)
print('PASS A03 GPU AArch64 4KiB tables above4GiB, isolated mapping walk, WRITE_VALUE bytes/canary, bounds, ASan/UBSan')
