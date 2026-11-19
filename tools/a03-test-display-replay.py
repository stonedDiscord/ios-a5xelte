#!/usr/bin/env python3
"""Exercise actual bounded replay control logic; no hardware display claim."""
from pathlib import Path
import argparse,subprocess,tempfile
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);a=p.parse_args()
s=(a.source/'iokit/Kernel/arm/SweetFramebuffer.cpp').read_text();start=s.index('extern "C" void a03_display_replay(unsigned count);');end=s.index('bool'+chr(10)+'IOMobileFramebufferUserClient::initWithTask',start);body=s[start:end]
header=r'''
#include <cassert>
#include <cstdint>
#include <cstring>
#include <cstdarg>
#define SWEET_FB_SWAP_REC_SIZE 0x400
static unsigned locked,calls,fail_after,logs;
static bool a03_fb_gpu_quarantined;
static uint64_t tick;
static struct {uint64_t copies;} a03_display_stats;
static uint64_t a03_fb_read(uint64_t*p){return *p;}
static uint64_t mach_absolute_time(){return ++tick;}
static void absolutetime_to_nanoseconds(uint64_t t,uint64_t*n){*n=t*10;}
static void IOLockLock(void*){assert(!locked);locked=1;}
static void IOLockUnlock(void*){assert(locked);locked=0;}
static int IOLog(const char*,...){logs++;return 0;}
struct AppleCLCD{
 void *fLock;bool fReplayValid;uint8_t fReplayRecord[0x400];
 void swap(const uint8_t*rec){assert(locked&&rec!=fReplayRecord&&!memcmp(rec,fReplayRecord,0x400));calls++;a03_display_stats.copies++;if(calls==fail_after)a03_fb_gpu_quarantined=true;}
};
static AppleCLCD *a03_replay_fb;
'''
tests=r'''
int main(){
 a03_display_replay(4);assert(!calls&&!locked);
 AppleCLCD fb{};a03_replay_fb=&fb;a03_display_replay(4);assert(!calls&&!locked);
 fb.fReplayValid=true;for(unsigned i=0;i<0x400;i++)fb.fReplayRecord[i]=i;
 for(unsigned n:{0U,9U,0xffffffffU}){a03_display_replay(n);assert(!calls&&!locked);}
 a03_display_replay(4);assert(calls==4&&a03_display_stats.copies==4&&!locked);
 calls=0;fail_after=2;a03_display_replay(8);assert(calls==2&&a03_fb_gpu_quarantined&&!locked);
 a03_display_replay(8);assert(calls==2&&!locked&&logs>=7);return 0;
}
'''
header='#include <initializer_list>'+chr(10)+header
with tempfile.TemporaryDirectory(prefix='a03-replay-') as tmp:
 tmp=Path(tmp);c=tmp/'test.cpp';exe=tmp/'test';c.write_text(header+body+tests)
 subprocess.run(['clang++','-std=c++17','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(c),'-o',str(exe)],check=True);subprocess.run([str(exe)],check=True)
assert 'memcpy(fReplayRecord,rec,sizeof(fReplayRecord));fReplayValid=true;' in s
assert 'a03_replay_fb=this;' in s
print('PASS actual replay bounds/lock/accepted-record/quarantine/break; ASan/UBSan, no hardware claim')
