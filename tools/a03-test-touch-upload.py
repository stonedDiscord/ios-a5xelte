#!/usr/bin/env python3
"""Exercise actual0148 upload parser; no firmware or device required."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'xnu/a03/0148-a03-explicit-jadard-ram-load.patch').read_text()
s='\n'.join(l[1:] for l in s.splitlines() if l.startswith('+') and not l.startswith('+++'))
s=s[s.index('/* Host transfers'):s.index(' if(a03_touch_upload(command))')]
prefix=r'''
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "shim/a03/jd9365t-firmware.h"
'''
test=r'''
int main(void){
 assert(!a03_touch_upload("rom"));assert(a03_touch_upload("fwbegin 256"));assert(a03_touch_fw_size==256&&!a03_touch_fw_used);
 const char*bad[]={"fwbegin ","fwbegin 0","fwbegin 81921","fwbegin 9999999999999999999999999999999999","fwbegin 256 extra","fwdata ","fwdata 0","fwdata 0 ","fwdata 0 a","fwdata 0 zz","fwdata 1 00","fwdata 99999999999999999999999999999999 00"};
 for(unsigned i=0;i<sizeof(bad)/sizeof(bad[0]);i++){assert(a03_touch_upload(bad[i]));assert(a03_touch_fw_size==256&&!a03_touch_fw_used);}
 assert(a03_touch_upload("fwdata 0 00aaff"));assert(a03_touch_fw_used==3&&a03_touch_firmware[0]==0&&a03_touch_firmware[1]==0xaa&&a03_touch_firmware[2]==0xff);
 assert(a03_touch_upload("fwdata 0 11")&&a03_touch_fw_used==3);
 assert(a03_touch_upload("fwstatus"));assert(a03_touch_upload("fwbegin 512")&&!a03_touch_fw_used&&a03_touch_fw_size==512);
 puts("PASS actual upload parser: bounded size/offset/hex, atomic rejection, sequential chunks, status/restart");}
'''
with tempfile.TemporaryDirectory(prefix='a03-upload-') as d:
 p=Path(d)/'test.c';p.write_text(prefix+s+test)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I',str(ROOT),str(p),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
