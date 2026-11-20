#!/usr/bin/env python3
"""Validate native strided-copy layout and optional pinned Mesa v9 packers."""
from pathlib import Path
import argparse,hashlib,json,re,shlex,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mesa-build',type=Path);a=p.parse_args()
header=(ROOT/'tools/a03-gpu-blit-layout.h').read_text()
words=[int(x,16) for x in re.findall(r'0x([0-9a-f]{16})ULL,',header)]
assert len(words)==240
assert hashlib.sha256(b''.join(w.to_bytes(8,'little') for w in words)).hexdigest()==re.search(r'SHA256 ([0-9a-f]{64})',header)[1]
source=r'''
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include "a03-gpu-blit-layout.h"
int main(void){
 void *m=aligned_alloc(0x4000,A03_GPU_BLIT_SIZE);assert(m);
 assert(a03_gpu_blit_layout(m,0x120000000ULL,124,2884,3072,2880,720,1598));
 uint64_t *q=m;uint32_t *j=(uint32_t *)((char *)m+0x4000),*p=(uint32_t *)((char *)m+0x4200);
 assert(j[4]==0x10008&&j[8]==0x80000c0f&&j[10]==3&&j[11]==400&&p[0]==0x400007c&&p[1]==0x5000b44&&p[4]==3072&&p[5]==2880&&p[6]==720&&p[7]==1598);
 /* Ceil dispatch and exact shader bounds for every width and sampled heights. */
 for(unsigned w=1;w<=720;w++)for(unsigned h=1;h<=1600;h+=17){
  assert(a03_gpu_blit_layout(m,0x120000000ULL,0,0,3072,2880,w,h));
  assert(j[10]==(w+255)/256&&j[11]==(h+3)/4&&p[6]==w&&p[7]==h);
 }
 assert(a03_gpu_blit_layout(m,0x120000000ULL,124,2884,3072,2880,720,1598));
 assert(q[0x3000/8+2]==2&&q[0x3000/8+3]==2);
 for(unsigned i=0;i<4;i++){assert(q[0x2000/8+32+i]==(0x120008000ULL+i*4096+0x403));assert(q[0x2000/8+40+i]==(0x12000c000ULL+i*4096+0x403));}
 for(unsigned i=0x8000/8;i<0x10000/8;i++)assert(q[i]==2);
 assert(!memcmp((char *)m+0x5000,a03_g57_blit_code,sizeof(a03_g57_blit_code)));
 assert(!a03_gpu_blit_layout(m,0x120000000ULL,4096,0,3072,2880,720,1600));
 assert(!a03_gpu_blit_layout(m,0x120000000ULL,0,0,3072,2880,0,1600));
 assert(!a03_gpu_blit_layout(m,0x120000000ULL,0,0,65536,2880,720,1600));
 uint64_t sl,dl;assert(a03_gpu_blit_geometry(0x100000,0x200000,0x9e000000,3072,2880,720,1600,&sl,&dl));
 assert(sl==4915008&&dl==4608000);
 assert(!a03_gpu_blit_geometry(0x100000,0x200000,0x9e000004,3072,2880,720,1600,&sl,&dl));
 assert(!a03_gpu_blit_geometry(0x100000,0x200000,0x9e000000,3072,2884,720,1600,&sl,&dl));
 free(m);return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='a03-blit-layout-') as temp:
 temp=Path(temp);c=temp/'test.c';exe=temp/'test';c.write_text(source)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I'+str(ROOT/'tools'),str(c),'-o',str(exe)],check=True)
 subprocess.run([str(exe)],check=True)
 if a.mesa_build:
  build=a.mesa_build.resolve();info=json.loads(subprocess.check_output(['meson','introspect',str(build),'--projectinfo']));assert info['version']=='24.3.0'
  entries=json.loads((build/'compile_commands.json').read_text());entry=next(e for e in entries if e['file'].endswith('/compiler/cmdline.c'))
  args=entry.get('arguments') or shlex.split(entry['command']);flags=[];skip=False
  for item in args:
   if skip:skip=False;continue
   if item in ['-o','-MF','-MQ','-MT']:skip=True;continue
   if item in ['-c','-MD','-MMD'] or item.endswith('/compiler/cmdline.c'):continue
   flags.append(item)
  primary=(ROOT/'tools/a03-test-gpu-copy-layout.py').read_text()
  # Reuse the independent primary-packer C fixture with blit count/layout.
  import ast
  tree=ast.parse(primary)
  fixture=next(n.args[0].value for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='write_text' and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str) and 'MALI_COMPUTE_PAYLOAD p=' in n.args[0].value)
  fixture=fixture.replace('a03-gpu-copy-layout.h','a03-gpu-blit-layout.h').replace('a03_gpu_copy_layout(mem,0x120000000ULL,1024)','a03_gpu_blit_layout(mem,0x120000000ULL,0,0,3072,2880,720,1600)').replace('A03_GPU_SCRATCH_SIZE','A03_GPU_BLIT_SIZE').replace('.workgroup_count_x=1024','.workgroup_count_x=720').replace('.workgroup_count_y=1,','.workgroup_count_y=1600,').replace('.r48_r63=0x1000','.r48_r63=0x3000')
  fixture=fixture.replace('.workgroup_size_x=1,','.workgroup_size_x=16,').replace('.workgroup_size_y=1,','.workgroup_size_y=4,').replace('.workgroup_count_x=720,','.workgroup_count_x=45,').replace('.workgroup_count_y=1600,','.workgroup_count_y=400,')
  fixture=fixture.replace('.workgroup_count_x=45,','.workgroup_count_x=3,')
  c.write_text(fixture);subprocess.run(flags+['-UNDEBUG','-I'+str(ROOT/'tools'),str(c),'-o',str(exe)],cwd=build,check=True);subprocess.run([str(exe)],check=True)
print('PASS strided blit geometry/mapping guards/shader hash and selected primary Mesa v9 descriptors; no hardware claim')
