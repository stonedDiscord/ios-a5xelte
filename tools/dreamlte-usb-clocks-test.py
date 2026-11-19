#!/usr/bin/env python3
"""Test actual read-only CMU snapshots and command-time capture placement."""
import pathlib
import re
import subprocess
import sys
import tempfile
source=pathlib.Path(sys.argv[1]).read_text()
def function(name):
    match=re.search(r'\b'+name+r'\([^;{}]*\)\s*\{',source)
    assert match
    at=source.index('{',match.start());end=at+1;depth=1
    while depth:
        depth+=(source[end]=='{')-(source[end]=='}');end+=1
    return source[match.start():end]
struct=re.search(r'struct dreamlte_usb_clocks \{[^}]+\};',source).group()
code=r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
typedef uintptr_t vm_offset_t;
static vm_offset_t dreamlte_fsys_cmu=0x11000000, dreamlte_top_cmu=0x15a80000;
static vm_offset_t dreamlte_usb_pmu=0x16480000, dreamlte_usb_refsel=0x10e50070;
static unsigned reads;
static const unsigned offsets[]={0x100,0x180,0x2078,0x207c,0x2080,0x3044,0x1068,0x1864,0x206c,0x704,0x0c};
static uint32_t usb_rd(vm_offset_t base,unsigned offset) {
    assert(reads<11 && offset==offsets[reads]);
    assert(base==(reads<6?dreamlte_fsys_cmu:reads<9?dreamlte_top_cmu:reads==9?dreamlte_usb_pmu:dreamlte_usb_refsel));
    return ++reads;
}
'''+struct+'\nstatic void\n'+function('dreamlte_usb_clocks_capture')+'\nstatic void\n'+function('dreamlte_usb_clocks_print')+r'''
int main(void) {
    struct dreamlte_usb_clocks v;
    dreamlte_usb_clocks_capture(&v);
    assert(reads==11 && v.busmux==1 && v.usbmux==2 && v.aclk==3 && v.ref==4 && v.suspend==5 && v.qch==6 && v.mux==7 && v.div==8 && v.gate==9 && v.isolation==10 && v.refsel==11);
    dreamlte_usb_clocks_print("sample",&v);assert(reads==11);
    puts("PASS: actual CMU capture reads eleven pinned registers including isolation/reference selector; logging never re-reads MMIO; entry/exit captures precede command/timeout output");
}
'''
command=function('ud_epcmd')
assert command.count('dreamlte_usb_clocks_capture(&resource_clocks);')==2
assert command.index('dreamlte_usb_clocks_capture')<command.index('dwc_wr(DEPCMDPAR0')
assert command.rindex('dreamlte_usb_clocks_capture')<command.index('printf("SWEET USB: ep%u cmd 0x%x timeout')
assert command.index('"prelog-exit"')>command.index('timeout')
assert 'volatile uint32_t *' not in function('dreamlte_usb_clocks_capture')
with tempfile.TemporaryDirectory(prefix='dreamlte-clocks-') as tmp:
    p=pathlib.Path(tmp);(p/'test.c').write_text(code)
    subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror',str(p/'test.c'),'-o',str(p/'test')],check=True)
    result=subprocess.run([str(p/'test')],check=True,capture_output=True,text=True)
    print(result.stdout.splitlines()[-1])
