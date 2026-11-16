#!/usr/bin/env python3
"""Check actual A03 touch builder's normalization, masks and release state."""
from pathlib import Path
import subprocess,tempfile
patch=(Path(__file__).resolve().parents[1]/'xnu/a03/0145-a03-opt-in-usb-hid-events.patch').read_text()
s='\n'.join(l[1:] for l in patch.splitlines() if l.startswith('+') and not l.startswith('+++'))
a=s.index('void\nSweetHIDTouch::touch(');i=s.index('{',a);j=i+1;depth=1
while depth:
 depth+=(s[j]=='{')-(s[j]=='}');j+=1
src=s[a:j]
pre=r'''
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <map>
#include <vector>
using UInt32=uint32_t;using IOFixed=int32_t;
#define TRUE 1
#define SWEET_TOUCH_FINGERS 10
#define kIOHIDDigitizerTransducerTypeHand 1
#define kIOHIDDigitizerTransducerTypeFinger 2
enum { kIOHIDEventFieldDigitizerCollection, kIOHIDEventFieldDigitizerIndex,
kIOHIDEventFieldDigitizerIdentity,kIOHIDEventFieldDigitizerTouch,
kIOHIDEventFieldDigitizerEventMask,kIOHIDEventFieldDigitizerX,
kIOHIDEventFieldDigitizerY,kIOHIDEventFieldDigitizerRange,kIOHIDEventFieldDigitizerButtonMask };
enum {kIOHIDDigitizerEventTouch=1,kIOHIDDigitizerEventRange=2,
kIOHIDDigitizerEventPosition=4,kIOHIDDigitizerEventIdentity=8};
static uint64_t mach_absolute_time(){return 123;}
static int locked,dispatched;static void IOLockLock(void*){assert(!locked);locked++;}
static void IOLockUnlock(void*){assert(locked==1);locked--;}
#define IOLog(...) ((void)0)
struct IOHIDEvent {
 std::map<int,int> value;std::vector<IOHIDEvent*> children;
 static IOHIDEvent *digitizerEvent(uint64_t,unsigned,int,bool range,unsigned buttons,int x,int y){auto p=new IOHIDEvent;p->value[kIOHIDEventFieldDigitizerRange]=range;p->value[kIOHIDEventFieldDigitizerButtonMask]=buttons;p->value[kIOHIDEventFieldDigitizerX]=x;p->value[kIOHIDEventFieldDigitizerY]=y;return p;}
 void setIntegerValue(int k,int v){value[k]=v;}void setFixedValue(int k,int v){value[k]=v;}
 void appendChild(IOHIDEvent *c){children.push_back(c);}
 void release(){} // snapshot ownership is in host test
};
class SweetHIDTouch {
public:
 void *fLock=nullptr;bool fDown[10]={};IOFixed fX[10]={},fY[10]={};
 IOHIDEvent *last=nullptr;
 void touch(int,bool,int,int);
 void dispatchEvent(IOHIDEvent *e){assert(!locked);clear();last=e;dispatched++;}
 void clear(){if(last){for(auto c:last->children)delete c;delete last;last=nullptr;}}
 ~SweetHIDTouch(){clear();}
};
'''
test=r'''
int main(){SweetHIDTouch t;
t.touch(-1,true,1,1);t.touch(10,true,1,1);assert(!dispatched);
t.touch(0,false,0,0);assert(!dispatched);
t.touch(0,true,360,1560);assert(dispatched==1&&t.fDown[0]);
auto e=t.last;assert(e->children.size()==1&&e->value[kIOHIDEventFieldDigitizerX]==32768&&e->value[kIOHIDEventFieldDigitizerY]==63897);
assert(e->value[kIOHIDEventFieldDigitizerTouch]==1&&e->value[kIOHIDEventFieldDigitizerEventMask]==15);
t.touch(0,true,360,1560);assert(dispatched==1);
t.touch(0,true,360,460);assert(dispatched==2&&t.last->value[kIOHIDEventFieldDigitizerEventMask]==4);
t.touch(0,false,360,460);assert(dispatched==3&&!t.fDown[0]);
e=t.last;assert(e->children.size()==1&&!e->value[kIOHIDEventFieldDigitizerTouch]&&!e->value[kIOHIDEventFieldDigitizerRange]&&!e->value[kIOHIDEventFieldDigitizerButtonMask]);
assert(e->value[kIOHIDEventFieldDigitizerEventMask]==3&&!e->children[0]->value[kIOHIDEventFieldDigitizerTouch]);
t.touch(0,false,360,460);assert(dispatched==3);
t.touch(1,true,-1,9999);assert(t.fX[1]==0&&t.fY[1]==65495);
t.touch(0,true,9999,-1);assert(t.fX[0]==65444&&t.fY[0]==0&&t.last->children.size()==2);
t.touch(0,false,719,0);assert(t.last->value[kIOHIDEventFieldDigitizerTouch]==1);
t.touch(1,false,0,1599);assert(!t.last->value[kIOHIDEventFieldDigitizerTouch]&&!locked);
puts("PASS actual touch builder: invalid fingers,720x1600 normalization/clamps, duplicate suppression, move/down/up masks, multi-touch/release");}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'test.cpp';p.write_text(pre+src+test)
 subprocess.run(['clang++','-std=c++17','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
