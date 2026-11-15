#!/usr/bin/env python3
"""Test the actual A03 software-AKS request dispatcher with host IOKit stubs."""
from pathlib import Path
import re,subprocess,tempfile
p=(Path(__file__).resolve().parent.parent/'xnu/a03/0107-a03-opt-in-software-keystore.patch').read_text()
s='\n'.join(l[1:] for l in p.split('+++ b/iokit/Kernel/arm/SweetKeyStore.cpp\n',1)[1].split('--- a/',1)[0].splitlines() if l.startswith('+'))
s=re.sub(r'^#include .*\n','',s,flags=re.M)
header=r'''
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#define ARM64_BOARD_CONFIG_SWEET 1
#define APPLE_KEXT_OVERRIDE override
#define __unused __attribute__((unused))
#define OSDeclareDefaultStructors(name)
#define OSDefineMetaClassAndStructors(name,base)
#define kIOUserClientClassKey "IOUserClientClass"
#define IOLog(...) ((void)0)
using IOReturn=int;
constexpr int kIOReturnSuccess=0,kIOReturnNoSpace=1,kIOReturnBadArgument=2,kIOReturnUnsupported=3,kIOReturnNotFound=4;
static uint32_t enabled;
static void PE_parse_boot_argn(const char*,void*p,size_t){*(uint32_t*)p=enabled;}
static void proc_selfname(char*p,size_t n){snprintf(p,n,"host-test");}
struct OSObject {};
struct IOService:OSObject { bool registered=false;virtual bool start(IOService*){return true;}void setProperty(const char*,const char*){}void registerService(){registered=true;} };
struct IOMemoryDescriptor { uint8_t b[256];size_t length=256;size_t getLength(){return length;}size_t writeBytes(size_t off,const void*src,size_t n){memcpy(b+off,src,n);return n;} };
struct IOExternalMethodArguments { uint64_t *scalarInput=nullptr,*scalarOutput=nullptr;uint32_t scalarInputCount=0,scalarOutputCount=0;IOMemoryDescriptor *structureInputDescriptor=nullptr,*structureOutputDescriptor=nullptr;void*structureOutput=nullptr;uint32_t structureInputSize=0,structureOutputSize=0,structureOutputDescriptorSize=0; };
struct IOExternalMethodDispatch {};
struct IOUserClient:IOService {virtual IOReturn clientClose(){return 0;} virtual IOReturn externalMethod(uint32_t,IOExternalMethodArguments*,IOExternalMethodDispatch*,OSObject*,void*){return 0;}void terminate(){} };
'''
tests=r'''
int main(){
 AppleKeyStore service;enabled=0;assert(!service.start(nullptr)&&!service.registered);enabled=1;assert(service.start(nullptr)&&service.registered);
 AppleKeyStoreUserClient client;IOExternalMethodArguments a;uint64_t in=0,out=99;a.scalarInput=&in;a.scalarOutput=&out;
 auto call=[&](unsigned sel){return client.externalMethod(sel,&a,nullptr,nullptr,nullptr);};
 assert(call(0)==0);assert(call(14)==kIOReturnBadArgument);
 a.scalarOutputCount=1;assert(call(14)==0&&out==0&&a.scalarOutputCount==1);
 in=501;a.scalarInputCount=1;a.scalarOutputCount=1;assert(call(14)==kIOReturnNotFound);
 in=0;a.scalarInputCount=2;assert(call(14)==kIOReturnNotFound);a.scalarInputCount=1;
 a.scalarOutputCount=0;assert(call(7)==kIOReturnBadArgument);a.scalarOutputCount=1;assert(call(7)==0&&out==4);
 for(unsigned sel:{2u,3u,6u,10u,11u,999u}) assert(call(sel)==kIOReturnUnsupported);
 uint8_t b[256];memset(b,0xaa,sizeof b);a.structureOutput=b;a.structureOutputSize=sizeof b;assert(call(17)==0);
 unsigned n=a.structureOutputSize;assert(b[0]==0x31&&b[1]==n-2&&a.scalarOutputCount==0&&b[n]==0xaa);
 a.structureOutputSize=1;assert(call(17)==kIOReturnNoSpace);
 IOMemoryDescriptor desc;a.structureOutputDescriptor=&desc;assert(call(17)==0&&a.structureOutputDescriptorSize==n&&memcmp(desc.b,b,n)==0);
 desc.length=1;assert(call(17)==kIOReturnNoSpace);
 puts("A03 software AKS opt-in/system-bag/unsupported/DER bounds checks PASS (host only)");
}
'''
with tempfile.TemporaryDirectory(prefix='a03-aks-test-') as d:
 f=Path(d)/'test.cpp';f.write_text(header+'\n#include <initializer_list>\n'+s+'\n'+tests)
 subprocess.run(['c++','-std=c++17','-Wall','-Wextra','-Wno-unused-variable','-Wno-unused-but-set-variable',str(f),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
