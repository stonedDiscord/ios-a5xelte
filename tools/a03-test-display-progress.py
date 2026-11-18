#!/usr/bin/env python3
"""Test actual0159 observer and notify result accounting; no display repair claim."""
from pathlib import Path
import argparse, subprocess, tempfile, shutil
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);a=p.parse_args()
patch=ROOT/'xnu/a03/0159-a03-readonly-display-progress-probe.patch'
subprocess.run(['git','apply','--check',str(patch)],cwd=a.source,check=True)
with tempfile.TemporaryDirectory() as temp:
    t=Path(temp)
    for name in ('iokit/Kernel/arm/SweetFramebuffer.cpp','bsd/kern/sweet_amfi.c'):
        out=t/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a.source/name,out)
    subprocess.run(['git','apply',str(patch)],cwd=t,check=True)
    source=(t/'iokit/Kernel/arm/SweetFramebuffer.cpp').read_text()
    helper=source[source.index('/* Independent relaxed atomic'):source.index('/* End A03 display probe helpers. */')]
    body=source[source.index('IOMobileFramebufferUserClient::notify('):source.index('static uint64_t sweet_fb_logged;')]
    body='static void notify('+body.split('(',1)[1]
    header='''#include <stdint.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
static uint64_t mach_absolute_time(){return 123;}
static unsigned logs;
#define IOLog(...) (++logs)
#define SWEET_FB_NOTIFY_TYPES 8
#define MACH_PORT_NULL 0
#define kIOReturnSuccess 0
#define kIOUserNotifyOptionCanDrop 1
#define bzero(p,n) memset(p,0,n)
typedef uint64_t io_user_reference_t, mach_vm_address_t;
typedef int IOReturn;
typedef uint64_t OSAsyncReference64[8];
static uint64_t fFunc[8],fRefcon[8];static int fPort,fTask,result,calls;
#define setAsyncReference64(...) ((void)fTask)
static int sendAsyncResult64WithOptions(uint64_t*,int,uint64_t*,uint32_t,int){calls++;return result;}
'''
    tests='''int main(){uint64_t values[6]={};
notify(8,values,6);notify(5,values,6);assert(a03_display_stats.notifySkipped==2&&!calls);
fFunc[5]=42;fPort=1;result=0;notify(5,values,6);assert(calls==1&&a03_display_stats.notifyOK==1);
result=-7;notify(5,values,6);assert(calls==2&&a03_display_stats.notifyError==1);
assert(a03_display_stats.lastError==(uint32_t)-7&&a03_display_stats.notifyAt==123);
assert(a03_display_stats.notifyAttempt==2);
for(unsigned i=0;i<10000;i++)a03_fb_inc(&a03_display_stats.swapEntered);
assert(a03_fb_read(&a03_display_stats.swapEntered)==10000);
a03_display_probe();assert(logs==4&&calls==2);
}'''
    for forbidden in ('IOLock','setTimeout','memcpy','fPixels','notify('):
        assert forbidden not in helper,forbidden
    assert 'a03_fb_inc(&a03_display_stats.vsyncDone)' in source
    assert 'a03_fb_inc(&a03_display_stats.swapDone)' in source
    assert 'a03_fb_inc(&a03_display_stats.copies)' in source
    f=t/'test.cpp';f.write_text(header+helper+body+tests)
    subprocess.run(['clang++','-std=c++17','-Wall','-Wextra','-Wno-unused-variable','-Wno-unused-parameter','-fsanitize=address,undefined',str(f),'-o',str(t/'test')],check=True)
    subprocess.run([str(t/'test')],check=True)
    subprocess.run(['git','apply','--reverse','--check',str(patch)],cwd=t,check=True)
print('PASS actual display observer/notify accounting ASan+UBSan, no observer locks/writes, patch/reverse')
