#!/usr/bin/env python3
"""Exercise actual bounded USB input actions and exact command decoder."""
from pathlib import Path
import subprocess,tempfile
p=(Path(__file__).resolve().parents[1]/'xnu/a03/0145-a03-opt-in-usb-hid-events.patch').read_text()
s='\n'.join(l[1:] for l in p.splitlines() if l.startswith('+') and not l.startswith('+++'))
a=s.index('extern "C" int a03_hid_action(unsigned action);');b=s.index('\n/*',a+1) if '\n/*' in s[a+1:] else -1
# Function ends before next added source file's include; balance braces.
a=s.index('extern "C" int a03_hid_action(unsigned action) {',a);i=s.index('{',a);depth=1;j=i+1
while depth:
 depth+=(s[j]=='{')-(s[j]=='}');j+=1
src=s[a:j]
pre=r'''
#include <cassert>
#include <cstdio>
static void *gSweetButtons,*gSweetTouch;
static int keys,touches,delay_ms,last_y;
static void sweet_hid_key(int k,int d){assert(k==3&&d==(keys==0));keys++;}
static void sweet_hid_touch(int f,int d,int x,int y){assert(f==0&&x==360&&y>=460&&y<=1560);assert(d==(touches<21));if(touches&&d)assert(y==last_y-55);last_y=y;touches++;}
static void IOSleep(unsigned ms){assert(ms==16||ms==80);delay_ms+=ms;}
'''
test=r'''
int main(){assert(a03_hid_action(0)==0);assert(a03_hid_action(1)==-1);assert(a03_hid_action(2)==-1);assert(!keys&&!touches&&!delay_ms);gSweetButtons=(void*)1;assert(a03_hid_action(0)==1);assert(!a03_hid_action(1)&&keys==2&&delay_ms==80);gSweetTouch=(void*)2;assert(a03_hid_action(0)==3);assert(!a03_hid_action(2)&&touches==22&&last_y==460&&delay_ms==416);assert(a03_hid_action(999)==-2&&touches==22);puts("PASS actual USB input actions: disabled/missing providers, status, paired Home, bounded swipe/release, unknown action");}
'''
with tempfile.TemporaryDirectory() as d:
 f=Path(d)/'test.cpp';f.write_text(pre+src+test)
 subprocess.run(['clang++','-std=c++17','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(f),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
assert 'if (false)' not in s and 'sweethidtest' not in s
assert 'enabled != 1' in s and '"a03_hid"' in s
assert 'getDoubleValue(' not in s and 'setDoubleValue(' not in s
assert '/ 720' in s and '/ 1600' in s
assert 'dispatch, not UI acknowledgement' in s
