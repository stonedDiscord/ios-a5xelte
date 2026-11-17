#!/usr/bin/env python3
"""Exercise the actual 0149 event callback without a device or firmware."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'xnu/a03/0149-a03-explicit-jadard-contact-poll.patch').read_text()
s='\n'.join(l[1:] for l in s.splitlines() if l.startswith('+') and not l.startswith('+++'))
s=s[s.index('extern void sweet_hid_touch'):s.index(' if(strcmp(command,')]
prefix=r'''
#include <assert.h>
#include <stdio.h>
#include <stddef.h>
#define __unused __attribute__((unused))
static unsigned calls,slot_,x_,y_;static int down_;
void sweet_hid_touch(int slot,int down,int x,int y){calls++;slot_=slot;down_=down;x_=x;y_=y;}
'''
test=r'''
int main(void){
 a03_touch_emit_hid=0;a03_touch_emit(NULL,9,1,720,1600);
 assert(!calls&&a03_touch_emit_count==1);
 a03_touch_emit_hid=1;a03_touch_emit(NULL,9,1,720,1600);
 assert(calls==1&&slot_==9&&down_==1&&x_==720&&y_==1600);
 a03_touch_emit(NULL,9,0,720,1600);assert(calls==2&&!down_);
 a03_touch_emit_count=64;a03_touch_emit(NULL,0,1,0,0);
 assert(calls==3&&a03_touch_emit_count==65&&!slot_&&!x_&&!y_);
 puts("PASS actual poll callback: log-only isolation, HID slot/coordinates/down/up, logging cap preserves dispatch");
}
'''
with tempfile.TemporaryDirectory(prefix='a03-poll-dispatch-') as d:
 p=Path(d)/'test.c';p.write_text(prefix+s+test)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
