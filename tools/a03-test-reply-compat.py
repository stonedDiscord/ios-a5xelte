#!/usr/bin/env python3
"""Exercise the actual patched strict-reply predicate; no runtime claim."""
from pathlib import Path
import itertools
import subprocess
import tempfile
patch=(Path(__file__).resolve().parent.parent/'xnu/a03/0105-a03-ios16-provisional-reply-compat.patch').read_text()
# Reconstruct the changed function hunk with its original context.
hunk=patch.split('@@ -3436,',1)[1].split('--- a/',1)[0]
source='\n'.join(line[1:] for line in hunk.splitlines()[1:] if line.startswith(('+',' ')))
source=source[source.index('boolean_t'):source.index('#if CONFIG_ROSETTA')]+'''
       && !proc_is_simulated(current_proc());
}
'''
header='''#include <stdbool.h>
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
#define ARM64_BOARD_CONFIG_SWEET 1
#define FALSE false
typedef bool boolean_t; typedef void *proc_t;
static bool a03_ios16_provisional_reply, platform_binary, simulated;
static uint32_t platform_value,sdk_value;
static proc_t current_proc(void) { return 0; }
static void *current_task(void) { return 0; }
static uint32_t proc_platform(proc_t p) { (void)p;return platform_value; }
static uint32_t proc_sdk(proc_t p) { (void)p;return sdk_value; }
static bool task_get_platform_binary(void *p) { (void)p;return platform_binary; }
static bool proc_is_simulated(proc_t p) { (void)p;return simulated; }
'''
rows=[]
for enabled,provisional,plat,sdk,binary,sim in itertools.product([0,1],[0,1],[1,2,7],[0,15,16,17],[0,1],[0,1]):
 expected=bool(binary and not sim and not(enabled and provisional and plat==2 and sdk==16))
 rows.append(f'a03_ios16_provisional_reply={enabled}; platform_value={plat}; sdk_value={sdk}u<<16; platform_binary={binary}; simulated={sim}; assert(__ip_strict_reply_port_semantics_violation({provisional})=={int(expected)});')
with tempfile.TemporaryDirectory(prefix='a03-reply-test-') as d:
 p=Path(d)/'test.c';p.write_text(header+source+'\nint main(void) {\n'+'\n'.join(rows)+'\nputs("A03 strict/provisional reply compatibility: 384 cases PASS (host only)");}\n')
 subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror',str(p),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
