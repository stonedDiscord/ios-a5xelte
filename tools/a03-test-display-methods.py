#!/usr/bin/env python3
"""Exercise actual patched display external methods with host IOKit stubs."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parent.parent
patch=(root/'xnu/a03/0123-a03-opt-in-ios16-display-surface.patch').read_text()
part=patch.split('+++ b/iokit/Kernel/arm/SweetFramebuffer.cpp\n',1)[1].split('--- ',1)[0]
p='\n'.join(x[1:] for x in part.splitlines() if x.startswith('+'))
# Apply every contextual hunk before extracting the actual method body.
with tempfile.TemporaryDirectory() as d:
 q=Path(d)/'iokit/Kernel/arm/SweetFramebuffer.cpp';q.parent.mkdir(parents=True);q.write_text(p+'\n')
 subprocess.run(['git','apply',str(root/'xnu/a03/0127-a03-default-surface-dimensions.patch')],cwd=d,check=True)
 p=q.read_text()
start=p.index('static uint64_t sweet_fb_logged;');src=p[start:p.rindex('#endif')]
pre=r'''
#include <cassert>
#include <cstdint>
#include <cstring>
#include <cstdio>
using std::memcpy;
#define __unused __attribute__((unused))
#define APPLE_KEXT_OVERRIDE
#define IOLog(...) ((void)0)
#define MACH_PORT_NULL 0
#define SWEET_FB_SWAP_REC_SIZE 0x400
#define SWEET_FB_NOTIFY_TYPES 8
#define SWEET_FB_DOT_PITCH 270
using IOReturn=int;using IOLock=int;using OSObject=int;using IOExternalMethodDispatch=int;
constexpr int kIOReturnSuccess=0,kIOReturnBadArgument=1,kIOReturnUnsupported=2;
constexpr unsigned kSweetFBGetLayerDefaultSurface=3,kSweetFBSwapBegin=4,kSweetFBSwapEnd=5,kSweetFBSwapWait=6,kSweetFBGetID=7,kSweetFBGetDisplaySize=8,kSweetFBIsMainDisplay=18,kSweetFBGetDotPitch=28,kSweetFBNotifications=72;
void IOLockLock(IOLock*){} void IOLockUnlock(IOLock*){} void proc_selfname(char*,unsigned){}
void bzero(void *p,size_t n){memset(p,0,n);}
struct IOExternalMethodArguments{const uint64_t *scalarInput=nullptr;uint64_t *scalarOutput=nullptr;uint32_t scalarInputCount=0,scalarOutputCount=0;const void *structureInput=nullptr;void *structureOutput=nullptr,*structureInputDescriptor=nullptr,*structureOutputDescriptor=nullptr;uint32_t structureInputSize=0,structureOutputSize=0;};
struct AppleCLCD{void *fSurface=nullptr;IOLock *fLock=nullptr;uint32_t fSwapID=0,fWidth=720,fHeight=1600;unsigned swaps=0;void swap(const uint8_t *p){assert(p[0]==0x42);swaps++;}};
uint64_t sweet_surface_port_in_task(void*,void*){return 7;}
struct IOMobileFramebufferUserClient {AppleCLCD *fFB;void *fTask=nullptr;uint64_t fFunc[8]={},fRefcon[8]={};IOReturn externalMethod(uint32_t,IOExternalMethodArguments*,IOExternalMethodDispatch*,OSObject*,void*);};
'''
tests=r'''
int main(){AppleCLCD fb;IOMobileFramebufferUserClient c;c.fFB=&fb;IOExternalMethodArguments a;
auto call=[&](unsigned s){return c.externalMethod(s,&a,nullptr,nullptr,nullptr);};
assert(c.externalMethod(8,nullptr,nullptr,nullptr,nullptr)==kIOReturnBadArgument);
uint64_t out[3]={99,99,99},in[4]={};a.scalarOutput=out;a.scalarOutputCount=2;assert(call(8)==0&&out[0]==720&&out[1]==1600&&out[2]==99);
a.scalarOutputCount=1;assert(call(8)==kIOReturnBadArgument);a.scalarOutput=nullptr;assert(call(7)==kIOReturnBadArgument);
a.scalarOutput=out;assert(call(4)==0&&out[0]==1);assert(call(18)==0&&out[0]==1);assert(call(28)==0&&out[0]==270);
a.scalarInput=in;a.scalarInputCount=2;in[0]=720;in[1]=1600;assert(call(3)==0&&out[0]==7);in[0]=0;in[1]=0;assert(call(3)==0&&out[0]==7);in[0]=721;assert(call(3)==kIOReturnUnsupported);in[0]=720;in[1]=1599;assert(call(3)==kIOReturnUnsupported);in[1]=1600;
a.scalarInputCount=0;a.scalarOutputCount=0;uint8_t rec[0x400]={0x42};a.structureInput=rec;a.structureInputSize=sizeof(rec);assert(call(5)==0&&fb.swaps==1);
a.structureInputSize=0x3ff;assert(call(5)==kIOReturnBadArgument);a.structureInputSize=0x46c;assert(call(5)==kIOReturnBadArgument);a.structureInputSize=0x400;a.structureInput=nullptr;assert(call(5)==kIOReturnBadArgument);
a.structureInputSize=0;a.scalarInputCount=4;in[0]=10;in[1]=11;in[2]=5;assert(call(72)==0&&c.fFunc[5]==10&&c.fRefcon[5]==11);in[2]=8;assert(call(72)==kIOReturnBadArgument);
a.scalarInputCount=0;assert(call(999)==kIOReturnUnsupported);
puts("A03 actual external method: exact scalar shapes, canvas-dimension defaults, swap400/null guards, notifications and unknown selector propagation PASS");}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'t.cpp').write_text(pre+src+tests);subprocess.run(['c++','-std=c++17','-Wall','-Wextra','-Wno-unused-variable','-Werror',str(p/'t.cpp'),'-o',str(p/'t')],check=True);subprocess.run([str(p/'t')],check=True)
