#!/usr/bin/env python3
"""Check actual submitting-thread runtime accounting; no hardware claim."""
from pathlib import Path
import argparse,subprocess,tempfile
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);a=p.parse_args()
s=(a.source/'iokit/Kernel/arm/SweetFramebuffer.cpp').read_text()
start=s.index('static void a03_fb_record_runtime(');end=s.index('/* End A03 display probe helpers. */',start)
helper=s[start:end]
pre='''#include <cstdint>
#include <cassert>
static uint64_t runtime;
static uint64_t thread_get_runtime_self(){return runtime;}
static void absolutetime_to_nanoseconds(uint64_t t,uint64_t*n){*n=t*10;}
static struct{uint64_t cpuRuntimeNs,gpuRuntimeNs;}a03_display_stats;
'''
tests='''int main(){
 runtime=300;a03_fb_record_runtime(false,100);
 assert(a03_display_stats.cpuRuntimeNs==2000&&!a03_display_stats.gpuRuntimeNs);
 runtime=700;a03_fb_record_runtime(true,200);
 assert(a03_display_stats.cpuRuntimeNs==2000&&a03_display_stats.gpuRuntimeNs==5000);
 a03_fb_record_runtime(true,700);assert(a03_display_stats.gpuRuntimeNs==5000);
}
'''
assert '#include <kern/thread.h>' in s
begin=s.index('uint64_t runtimeBegin=thread_get_runtime_self();')
submit=s.index('int copied=a03_gpu_framebuffer_blit',begin)
record=s.index('a03_fb_record_runtime(copied!=0,runtimeBegin);',submit)
assert begin<submit<s.index('if(copied<0)',submit)<record<s.index('if(copied){a03_fb_inc',record)
assert 'if(!copied)for' in s[submit:record]
assert 'copy thread-runtime cpu=%lluns gpu=%lluns; submitting thread only' in s
with tempfile.TemporaryDirectory(prefix='a03-runtime-') as tmp:
 t=Path(tmp);c=t/'test.cpp';c.write_text(pre+helper+tests)
 subprocess.run(['clang++','-std=c++17','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(c),'-o',str(t/'test')],check=True)
 subprocess.run([str(t/'test')],check=True)
print('PASS actual copy runtime accounting/routing and failed-frame exclusion; ASan/UBSan, no hardware claim')
