#!/usr/bin/env python3
"""Host-only tests of actual opt-in watchdog provider."""
from pathlib import Path
import tempfile,subprocess
root=Path(__file__).resolve().parent.parent
header=r'''
#include <cassert>
#include <cstdint>
#include <cstring>
#include <cstdarg>
#define ARM64_BOARD_CONFIG_SWEET 1
#define OSDeclareDefaultStructors(x)
#define OSDefineMetaClassAndStructors(x,y)
#define APPLE_KEXT_OVERRIDE override
#define __unused __attribute__((unused))
#define kIOUserClientClassKey 0
using UInt32=unsigned;using task_t=void*;using IOReturn=int;
struct OSObject{virtual ~OSObject()=default;};
struct OSNumber:OSObject{uint64_t v;OSNumber(uint64_t n):v(n){}uint64_t unsigned64BitValue(){return v;}};
struct OSDictionary:OSObject{unsigned count=1;OSObject *value=nullptr;unsigned getCount(){return count;}OSObject* getObject(const char*key){return strcmp(key,"IOPMUBootStage")?nullptr:value;}};
#define OSDynamicCast(t,o) dynamic_cast<t*>(o)
struct IOExternalMethodDispatch{};
struct IOExternalMethodArguments {unsigned scalarInputCount=0,structureInputSize=0;void* structureInputDescriptor=nullptr;unsigned scalarOutputCount=1;uint64_t* scalarOutput=nullptr;unsigned structureOutputSize=0;void* structureOutputDescriptor=nullptr;};
enum{kIOReturnSuccess=0,kIOReturnUnsupported=-1,kIOReturnBadArgument=-2,kIOReturnNoMemory=-3};
unsigned enable=0,registered=0;bool parent=true;
void PE_parse_boot_argn(const char*,void*p,unsigned){memcpy(p,&enable,4);}
void IOLog(const char*,...){}
class IOService {public:virtual bool start(IOService*){return parent;}void setProperty(int,const char*){}bool setProperty(const char*,uint64_t,unsigned){return true;}bool setProperty(const char*,OSObject*){return true;}virtual int setProperties(OSObject*){return -1;}void registerService(){registered++;}};
class IOUserClient:public IOService{public:virtual bool initWithTask(task_t,void*,UInt32,OSDictionary*){return parent;} virtual int clientClose(){return 0;}virtual int externalMethod(uint32_t,IOExternalMethodArguments*,IOExternalMethodDispatch*,OSObject*,void*){return -1;}void terminate(){}};
'''
tests=r'''

int main() {
 IOWatchdog p;assert(!p.start(nullptr));
 enable=2;assert(!p.start(nullptr));enable=1;parent=false;assert(!p.start(nullptr));
 parent=true;assert(p.start(nullptr)&&registered==1);
 A03WatchdogUserClient c;assert(!c.initWithTask(nullptr,nullptr,0,nullptr));
 assert(c.initWithTask(nullptr,nullptr,1,nullptr));
 IOExternalMethodArguments a;uint64_t v=99;a.scalarOutput=&v;
 auto call=[&](unsigned s){return c.externalMethod(s,&a,nullptr,nullptr,nullptr);};
 assert(call(0)==0&&v==0);
 for(unsigned s=1;s<32;s++){v=99;assert(call(s)==kIOReturnUnsupported&&v==99);}
 a.scalarInputCount=1;assert(call(0)==kIOReturnBadArgument);a.scalarInputCount=0;
 a.scalarOutputCount=0;assert(call(0)==kIOReturnBadArgument);a.scalarOutputCount=1;
 a.structureInputSize=1;assert(call(0)==kIOReturnBadArgument);a.structureInputSize=0;
 a.structureOutputSize=1;assert(call(0)==kIOReturnBadArgument);a.structureOutputSize=0;
 a.structureInputDescriptor=&v;assert(call(0)==kIOReturnBadArgument);a.structureInputDescriptor=nullptr;
 a.structureOutputDescriptor=&v;assert(call(0)==kIOReturnBadArgument);a.structureOutputDescriptor=nullptr;
 a.scalarOutput=nullptr;assert(call(0)==kIOReturnBadArgument);
 assert(c.externalMethod(0,nullptr,nullptr,nullptr,nullptr)==kIOReturnBadArgument);
 OSDictionary dict;OSNumber stage(255);dict.value=&stage;assert(p.setProperties(&dict)==0);stage.v=256;assert(p.setProperties(&dict)==kIOReturnBadArgument);dict.count=2;assert(p.setProperties(&dict)==kIOReturnUnsupported);assert(p.setProperties(nullptr)==kIOReturnUnsupported);
 assert(c.clientClose()==0);return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='a03-watchdog-') as d:
 d=Path(d)
 subprocess.run(['git','apply','--include=iokit/Kernel/arm/A03Watchdog.cpp',str(root/'xnu/a03/0112-a03-disabled-watchdog-capability.patch')],cwd=d,check=True)
 subprocess.run(["git","apply",str(root/"xnu/a03/0114-a03-watchdog-software-boot-stage.patch")],cwd=d,check=True)
 source=(d/'iokit/Kernel/arm/A03Watchdog.cpp').read_text()
 source=chr(10).join(x for x in source.splitlines() if not x.startswith('#include'))
 p=d/'test.cpp';p.write_text(header+source+tests)
 subprocess.run(['c++','-std=c++17','-Wall','-Wextra','-Werror',str(p),'-o',str(d/'test')],check=True)
 subprocess.run([str(d/'test')],check=True)
 print('A03 watchdog gate/type/disabled/shape/unsupported PASS (host only)')
