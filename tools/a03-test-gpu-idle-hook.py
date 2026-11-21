#!/usr/bin/env python3
"""Check the real vsync idle hook executes under framebuffer serialization."""
from pathlib import Path
import argparse,subprocess,tempfile
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);a=p.parse_args()
s=(a.source/'iokit/Kernel/arm/SweetFramebuffer.cpp').read_text()
start=s.index('void'+chr(10)+'AppleCLCD::vsyncFired(');end=s.index('void'+chr(10)+'AppleCLCD::addClient',start)
body=s[start:end]
assert body.count('a03_gpu_idle_tick();')==1
assert body.index('IOLockLock(fb->fLock)')<body.index('a03_gpu_idle_tick();')<body.index('IOLockUnlock(fb->fLock)')
assert 'extern "C" void a03_gpu_idle_tick(void);' in s
pre=r'''
#include <cstdint>
#include <cassert>
#define SWEET_FB_NOTIFY_VSYNC 5
#define SWEET_FB_VSYNC_US 16667
static bool locked;static unsigned calls,notifies,timers;
struct OSObject{};
struct IOTimerEventSource{void setTimeoutUS(unsigned n){assert(n==16667&&!locked);timers++;}};
struct IOMobileFramebufferUserClient{void notify(unsigned,uint64_t*,unsigned){assert(locked&&calls);notifies++;}};
struct Clients{IOMobileFramebufferUserClient client;unsigned getCount(){return 1;}OSObject*getObject(unsigned){return (OSObject*)&client;}};
struct AppleCLCD:OSObject{uint64_t fVsyncCount=0;void*fLock=nullptr;Clients*fClients;static void vsyncFired(OSObject*,IOTimerEventSource*);};
static struct{uint64_t vsyncEntered,vsyncDone,vsyncAt;}a03_display_stats;
static void a03_fb_inc(uint64_t*p){(*p)++;}
static void a03_fb_set(uint64_t*p,uint64_t v){*p=v;}
static uint64_t mach_absolute_time(){return 200;}
static void IOLockLock(void*){assert(!locked);locked=true;}
static void IOLockUnlock(void*){assert(locked);locked=false;}
static void a03_gpu_idle_tick(){assert(locked);calls++;}
'''
test='int main(){AppleCLCD fb;Clients clients;fb.fClients=&clients;IOTimerEventSource timer;AppleCLCD::vsyncFired(&fb,&timer);assert(calls==1&&notifies==1&&timers==1&&a03_display_stats.vsyncDone==1&&!locked);}'
with tempfile.TemporaryDirectory() as d:
 d=Path(d);c=d/'test.cpp';c.write_text(pre+body+test)
 subprocess.run(['clang++','-std=c++17','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(c),'-o',str(d/'test')],check=True)
 subprocess.run([str(d/'test')],check=True)
print('PASS actual vsync idle hook lock ordering, notification and timer rearm; ASan/UBSan')
