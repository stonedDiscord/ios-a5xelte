#!/usr/bin/env python3
"""Host-exercise actual A03 pixel copier and inspect opt-in display staging."""
from pathlib import Path
import subprocess,tempfile,sys,struct
root=Path(__file__).resolve().parent.parent
patch=(root/'xnu/a03/0123-a03-opt-in-ios16-display-surface.patch').read_text()
parts=patch.split('+++ b/iokit/Kernel/arm/SweetFramebuffer.cpp\n',1)[1].split('--- ',1)[0]
source='\n'.join(x[1:] for x in parts.splitlines() if x.startswith('+'))
start=source.index('static uint32_t\nget32(');end=source.index('\nbool\nIOMobileFramebufferUserClient::initWithTask',start)
helper=source[start:end]
pre=r'''
#include <cassert>
#include <cstdint>
#include <cstring>
#include <cstdio>
using std::memcpy;
#define IOLog(...) ((void)0)
#define kPEDisableScreen 0
#define SWEET_FB_LAYERS 4
#define SWEET_FB_FORMAT_BGRA 0x42475241
#define OSSafeReleaseNULL(s) do {if(s){s->release();s=nullptr;}}while(0)
struct PE_Video {};
static bool PE_parse_boot_argn(const char *,void *,size_t){return false;}
static void PE_current_console(PE_Video *){}
static void PE_initialize_console(PE_Video *,int){}
struct Memory{uint64_t size;uint64_t getLength(){return size;}};
struct SweetSurface {
 uint32_t width=4,height=4,bytesPerRow=16,offset=0,bytesPerElement=4,pixelFormat=SWEET_FB_FORMAT_BGRA;
 unsigned elementWidth=1,elementHeight=1;Memory *memory;uintptr_t addr;
 uintptr_t kernelAddress(){return addr;}void release(){}
};
static SweetSurface *selected;
static SweetSurface *sweet_surface_copy(uint32_t id){return id==7?selected:nullptr;}
struct AppleCLCD {
 bool fConsolePaused=false;SweetSurface *fSurface=nullptr;uintptr_t fPixels;
 uint32_t fWidth=4,fHeight=4,fRowBytes=16;
 void swap(const uint8_t *rec);
};
'''
tests=r'''
static void put(uint8_t *b,unsigned off,uint32_t v){memcpy(b+off,&v,4);}
int main(){
 uint32_t src[16],dst[18];for(unsigned i=0;i<16;i++)src[i]=i+1;
 Memory memory{64};SweetSurface surface;surface.memory=&memory;surface.addr=(uintptr_t)src;selected=&surface;
 AppleCLCD fb;fb.fPixels=(uintptr_t)(dst+1);uint8_t rec[0x400]={};
 auto reset=[&](){for(auto &x:dst)x=0xdeadbeef;};
 put(rec,0x104,1);put(rec,0x54,7);put(rec,0xc4+8,4);put(rec,0xc4+12,4);
 reset();fb.swap(rec);assert(dst[0]==0xdeadbeef&&dst[17]==0xdeadbeef);assert(!memcmp(dst+1,src,64));
 surface.pixelFormat=0;reset();fb.swap(rec);assert(dst[1]==0xdeadbeef);surface.pixelFormat=SWEET_FB_FORMAT_BGRA;
 surface.bytesPerElement=2;fb.swap(rec);assert(dst[1]==0xdeadbeef);surface.bytesPerElement=4;
 memory.size=63;fb.swap(rec);assert(dst[1]==0xdeadbeef);memory.size=64;
 put(rec,0x104,0);fb.swap(rec);assert(dst[1]==0xdeadbeef);put(rec,0x104,1);
 put(rec,0xc4,3);put(rec,0xc4+4,3);reset();fb.swap(rec);assert(dst[16]==1&&dst[15]==0xdeadbeef&&dst[17]==0xdeadbeef);
 put(rec,0x54,8);reset();fb.swap(rec);assert(dst[1]==0xdeadbeef);
 puts("A03 actual display copier: BGRA/type/extent/mask/lookup/clipping/sentinels PASS");
}
'''
assert '#define SWEET_FB_SWAP_REC_SIZE          0x400' in source
assert 'args->structureInputSize != SWEET_FB_SWAP_REC_SIZE' in source
assert 'ret = kIOReturnUnsupported;' in source
assert source.count('PE_parse_boot_argn("a03_display"')==1
assert 'fPhys != 0x9e000000ULL' in source
assert 'SweetSurface.cpo_CFLAGS_ADD += -mgeneral-regs-only' in patch
with tempfile.TemporaryDirectory(prefix='a03-display-') as d:
 p=Path(d);(p/'test.cpp').write_text(pre+helper+tests)
 subprocess.run(['c++','-std=c++17','-Wall','-Wextra','-Werror','-Wno-unused-variable',str(p/'test.cpp'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True)
 sys.path.insert(0,str(root/'tools'));import mkadt_a03
 for enabled in (False,True):
  adt=mkadt_a03.build(True,enabled);io=next(n for n in adt.children if n.name=='arm-io');nodes=[n for n in io.children if n.name=='disp0'];assert len(nodes)==int(enabled)
  if enabled:
   props={k:v for k,f,v in nodes[0].props};assert props['compatible']==b'a03,display\0';assert struct.unpack('<I',props['canvas-width'])==(720,);assert struct.unpack('<I',props['canvas-height'])==(1600,)
print('A03 display opt-in ADT, exact geometry, general-register flags and unsupported selector checks PASS')
