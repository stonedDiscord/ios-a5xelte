#!/usr/bin/env python3
"""Verify the actual serial draw gate retains USB spool writes after handoff."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'xnu/a03/0151-a03-gui-panel-console-handoff.patch').read_text()
added='\n'.join(l[1:] for l in s.splitlines() if l.startswith('+') and not l.startswith('+++'))
state=added[added.index('static volatile unsigned a03_fbcon_quiet;'):added.index('    if(a03_fbcon_quiet)return;')]
# The unchanged append precedes the added gate in the real serial function.
assert '    a03_console_append(c);\n+    if(a03_fbcon_quiet)return;' in s
state=state[:state.index('\nextern "C"')] if '\nextern "C"' in state else state
source='''#include <assert.h>
#include <stdint.h>
static unsigned spooled,drawn;
static void a03_console_append(uint8_t c){(void)c;spooled++;}
'''+state+'''
static void transmit(uint8_t c){a03_console_append(c);
'''+ '    if(a03_fbcon_quiet)return;'+'''
 drawn++;}
int main(void){transmit('a');assert(spooled==1&&drawn==1);
 a03_console_panel_quiet();transmit('b');assert(spooled==2&&drawn==1);
 a03_console_panel_quiet();transmit('c');assert(spooled==3&&drawn==1);}
'''
with tempfile.TemporaryDirectory(prefix='a03-panel-') as d:
 p=Path(d)/'test.c';p.write_text(source)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
print('PASS actual panel gate: pre-handoff drawing, post-handoff spool-only, idempotent')
