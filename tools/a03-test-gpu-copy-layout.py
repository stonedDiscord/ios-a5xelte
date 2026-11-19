#!/usr/bin/env python3
"""Host-only validation of G57 copy mappings/descriptor bounds and shader bytes."""
from pathlib import Path
import re,hashlib,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
header=(ROOT/'tools/a03-gpu-copy-layout.h').read_text()
expected=re.search('Binary SHA256: ([0-9a-f]{64})',header)[1]
words=[int(x,16) for x in re.findall('0x([0-9a-f]{16})ULL,',header)]
assert len(words)==16
assert hashlib.sha256(b''.join(w.to_bytes(8,'little') for w in words)).hexdigest()==expected
source='''
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include "a03-gpu-copy-layout.h"
int main(void){
 uint8_t *mem=aligned_alloc(0x4000,A03_GPU_SCRATCH_SIZE);assert(mem);
 for(unsigned n=1;n<=1024;n++){
  uint64_t pa=0x120000000ULL;assert(a03_gpu_copy_layout(mem,pa,n));
  uint32_t *j=(uint32_t *)(mem+0x4000);assert(j[4]==0x10008&&j[8]==0x80000000&&j[9]==0x8001&&j[10]==n&&j[11]==1&&j[12]==1);
  assert(*(uint64_t *)(j+26)==0x02000100&&*(uint64_t *)(j+28)==0x02000140);
  uint64_t *l3=(uint64_t *)(mem+0x3000);
  for(unsigned i=0;i<4;i++)assert((l3[i]&0x000000fffffff000ULL)==pa+0x4000+i*0x1000);
  assert(l3[0]&(1ULL<<54));assert(!(l3[1]&(1ULL<<54)));assert((l3[1]&0xc0)==0xc0);
  assert((l3[2]&0xc0)==0xc0&&(l3[2]&(1ULL<<54)));assert((l3[3]&0xc0)==0x40&&(l3[3]&(1ULL<<54)));
  assert(l3[4]==2);assert(!memcmp(mem+0x5000,a03_g57_copy_code,128));
  uint32_t *s=(uint32_t *)(mem+0x6000),*d=(uint32_t *)(mem+0x7000);
  for(unsigned i=0;i<1024;i++)assert(s[i]==(0x10203040U^(i*0x01010101U))&&d[i]==0xdeadbeefU);
 }
 assert(!a03_gpu_copy_layout(mem,0x120000000ULL,0));assert(!a03_gpu_copy_layout(mem,0x120000000ULL,1025));
 free(mem);return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='a03-copy-layout-') as d:
 t=Path(d);(t/'test.c').write_text(source)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I',str(ROOT/'tools'),str(t/'test.c'),'-o',str(t/'test')],check=True)
 subprocess.run([str(t/'test')],check=True)
print('PASS G57 copy descriptor/counts/mapping permissions/source-destination guards/shader identity, ASan/UBSan; no hardware claim')
