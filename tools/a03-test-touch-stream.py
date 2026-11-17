#!/usr/bin/env python3
"""Exercise actual continuous stream command policy without MMIO or firmware."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
patch=(ROOT/'xnu/a03/0154-a03-explicit-continuous-touch-poll.patch').read_text()
with tempfile.TemporaryDirectory(prefix='a03-stream-') as d:
 p=Path(d); (p/'bsd/dev').mkdir(parents=True)
 # Inspect complete added/context function bodies from the patch under test.
 lines=[]
 for l in patch.splitlines():
  if l.startswith('--- a/bsd/dev/a03_jd9365t_poll.h'):break
  if l.startswith('@@') or l.startswith('+++') or l.startswith('---'):continue
  if l.startswith('+') or l.startswith(' '):lines.append(l[1:])
 s='\n'.join(lines)
 stop=s[s.index('static void a03_touch_stream_stop'):s.index('/* Host transfers')]
 policy=s[s.index(' if(!strcmp(command,"stop"))'):s.index(' if(a03_touch_upload(command))return;')]
 prefix=r'''
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "shim/a03/jd9365t-contact-state.h"
static unsigned a03_touch_emit_count,a03_touch_emit_hid,a03_touch_packet_count;
static unsigned a03_touch_streaming,a03_touch_stream_slices,provider=2,hids;
static struct a03_jd_contact_state a03_touch_stream_state;
static int a03_hid_action(unsigned n){(void)n;return provider;}
static void a03_touch_emit(void*c,unsigned i,int down,unsigned x,unsigned y){(void)c;(void)i;(void)x;(void)y;assert(!down);a03_touch_emit_count++;if(a03_touch_emit_hid)hids++;}
'''
 test=r'''
int main(void){provider=0;command("start");assert(!a03_touch_streaming);
 command("startcontacts");assert(a03_touch_streaming&&!a03_touch_emit_hid);
 a03_touch_stream_state.contacts[0].down=1;command("stop");assert(!a03_touch_streaming&&a03_touch_emit_count==1&&!hids);
 provider=2;command("start");assert(a03_touch_streaming&&a03_touch_emit_hid&&!a03_touch_emit_count);
 a03_touch_stream_state.contacts[0].down=1;command("start");assert(a03_touch_stream_state.contacts[0].down);
 command("fwbegin 500");assert(a03_touch_streaming);command("stop");assert(!a03_touch_streaming&&hids==1);
 command("stop");assert(hids==1);command("streamstatus");}
'''
 src=prefix+stop+'\nstatic void command(const char *command){'+policy+'}\n'+test
 (p/'test.c').write_text(src)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I',str(ROOT),str(p/'test.c'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True)
print('PASS actual stream command policy: provider gate, log-only start, retained state, stop releases once, upload isolation')
