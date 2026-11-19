#!/usr/bin/env python3
"""Host-only validation of G57 copy mappings/descriptor bounds and shader bytes."""
from pathlib import Path
import argparse,re,hashlib,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--mesa-build',type=Path,help='optional pinned Mesa24.3 build with generated v9_pack.h')
args=parser.parse_args()
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

if args.mesa_build:
 build=args.mesa_build.resolve()
 import json,shlex
 info=json.loads(subprocess.check_output(['meson','introspect',str(build),'--projectinfo']))
 assert info['version']=='24.3.0',info['version']
 commands=json.loads((build/'compile_commands.json').read_text())
 entry=next(c for c in commands if c['file'].endswith('/compiler/cmdline.c'))
 compile_args=entry.get('arguments') or shlex.split(entry['command'])
 filtered=[];skip=False
 for item in compile_args:
  if skip:skip=False;continue
  if item in ('-o','-MF','-MQ','-MT'):skip=True;continue
  if item in ('-MD','-MMD','-c') or item.endswith('/compiler/cmdline.c'):continue
  filtered.append(item)
 with tempfile.TemporaryDirectory(prefix='a03-copy-mesa-pack-') as tmp:
  tmp=Path(tmp);source=tmp/'test.c';exe=tmp/'test'
  source.write_text('#include <assert.h>\n#include <stdint.h>\n#include <stdlib.h>\n#include <string.h>\n#include "panfrost/lib/genxml/v9_pack.h"\n#include "a03-gpu-copy-layout.h"\nint main(void){\n void *mem=aligned_alloc(0x4000,A03_GPU_SCRATCH_SIZE);assert(mem);\n assert(a03_gpu_copy_layout(mem,0x120000000ULL,1024));\n uint32_t expected[32]={0};\n struct MALI_JOB_HEADER h={MALI_JOB_HEADER_header,.type=MALI_JOB_TYPE_COMPUTE,.index=1};\n MALI_JOB_HEADER_pack(expected,&h);\n struct MALI_COMPUTE_PAYLOAD p={MALI_COMPUTE_PAYLOAD_header,.workgroup_size_x=1,.workgroup_size_y=1,.workgroup_size_z=1,.allow_merging_workgroups=true,.task_increment=1,.task_axis=MALI_TASK_AXIS_Z,.workgroup_count_x=1024,.workgroup_count_y=1,.workgroup_count_z=1,.compute={.shader=0x02000100ULL,.thread_storage=0x02000140ULL}};\n MALI_COMPUTE_PAYLOAD_pack(expected+8,&p);assert(!memcmp(expected,(uint8_t*)mem+0x4000,128));\n struct MALI_SHADER_PROGRAM s={MALI_SHADER_PROGRAM_header,.stage=MALI_SHADER_STAGE_COMPUTE,.register_allocation=MALI_SHADER_REGISTER_ALLOCATION_32_PER_THREAD,.preload={.r48_r63=0x1000},.binary=0x02001000ULL};\n MALI_SHADER_PROGRAM_pack(expected,&s);assert(!memcmp(expected,(uint8_t*)mem+0x4100,32));\n struct MALI_LOCAL_STORAGE l={MALI_LOCAL_STORAGE_header};MALI_LOCAL_STORAGE_pack(expected,&l);assert(!memcmp(expected,(uint8_t*)mem+0x4140,32));\n free(mem);return 0;\n}\n')
  subprocess.run(filtered+['-I'+str(ROOT/'tools'),str(source),'-o',str(exe)],cwd=build,check=True)
  subprocess.run([str(exe)],check=True)
 print('PASS primary Mesa24.3 v9 compute/header/shader/local-storage packers byte-match; no hardware claim')
