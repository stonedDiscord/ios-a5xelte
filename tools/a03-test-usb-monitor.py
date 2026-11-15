#!/usr/bin/env python3
"""Host-only monitor parser/queue regression from staged patch0104."""
from pathlib import Path
import subprocess,tempfile
p=(Path(__file__).resolve().parent.parent/'xnu/a03/0104-a03-post-trap-usb-monitor.patch').read_text()
added='\n'.join(l[1:] for l in p.splitlines() if l.startswith('+') and not l.startswith('+++'))
queue=added[added.index('int a03_usb_debug_command'):added.index(' if(csr&1)')]
parse=added[added.index('static int\na03_debug_hex'):added.index('void\na03_init_debug_hold')]
header='''#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
typedef int boolean_t;
#define FALSE 0
static int ml_set_interrupts_enabled(int x) { return x; }
'''
tests='''int main(void) {
 const char *s=" 0xfffffe0001234567 100";uint64_t v;
 assert(a03_debug_hex(&s,&v)&&v==0xfffffe0001234567ULL);
 assert(a03_debug_hex(&s,&v)&&v==256);
 s="0x";assert(!a03_debug_hex(&s,&v));
 s="10000000000000000";assert(!a03_debug_hex(&s,&v));
 s="xyz";assert(!a03_debug_hex(&s,&v));
 char b[128];assert(!a03_usb_debug_command(b,sizeof(b)));
 const char *c="regs\\n";while(*c)input_char(*c++);
 assert(a03_usb_debug_command(b,sizeof(b))&&!strcmp(b,"regs"));
 assert(!a03_usb_debug_command(b,sizeof(b)));
 c="mem 1234 40\\r\\n";while(*c)input_char(*c++);
 assert(a03_usb_debug_command(b,sizeof(b))&&!strcmp(b,"mem 1234 40"));
 c="btx\\b\\n";while(*c)input_char(*c++);
 assert(a03_usb_debug_command(b,sizeof(b))&&!strcmp(b,"bt"));
 puts("A03 USB monitor hex parser/command queue PASS (host only)");
}'''
with tempfile.TemporaryDirectory(prefix='a03-monitor-') as d:
 f=Path(d)/'test.c';f.write_text(header+queue+parse+tests)
 subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror',str(f),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
