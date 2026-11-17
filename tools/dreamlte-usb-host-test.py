#!/usr/bin/env python3
"""Exercise the actual staged DREAMLTE USB wrapper with modeled MMIO.
Usage: dreamlte-usb-host-test.py PATH/TO/xnu/bsd/dev/sweet_usb.c
No phone access. Checks opt-in/ID/running/cold-PHY refusal and Exynos writes.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

source = pathlib.Path(sys.argv[1]).read_text()

def function(name):
    match = re.search(r'\b' + name + r'\([^;{}]*\)\s*\{', source)
    assert match, name
    start = match.start()
    opening = source.index('{', start)
    depth = 1
    end = opening + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return re.sub(r'__asm__ volatile\("[^"\n]*" ::: "memory"\);', '', source[start:end])

code = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef uintptr_t vm_offset_t;
#define DWC3_PA 0x10c00000
#define DWC3_SIZE 0x10000
static uint32_t core[0x10000 / 4], phy[0x100 / 4];
static vm_offset_t dreamlte_phy;
static unsigned maps, starts, phy_reads;
static int mode;
static vm_offset_t ml_io_map(uintptr_t pa, unsigned size) {
    maps++;
    if (pa == DWC3_PA && size == DWC3_SIZE) return (uintptr_t)core;
    assert(pa == 0x10e00000 && size == 0x100);
    return (uintptr_t)phy;
}
static uint32_t usb_rd(vm_offset_t base, uint32_t off) {
    uintptr_t addr = base + off;
    if (addr >= (uintptr_t)core && addr < (uintptr_t)(core + 0x10000/4))
        return *(uint32_t *)addr;
    assert(addr >= (uintptr_t)phy && addr < (uintptr_t)(phy + 0x100/4));
    phy_reads++;
    return *(uint32_t *)addr;
}
static void PE_parse_boot_argn(const char *key, int *out, unsigned size) {
    assert(!strcmp(key, "dreamlteusb") && size == sizeof(mode)); *out = mode;
}
static void sweet_usb_gadget_start(vm_offset_t dwc) {
    assert(dwc == (uintptr_t)core); starts++;
}
'''
code += 'static int\n' + function('dreamlte_usb_prepare') + '\n'
code += 'static void\n' + function('dreamlte_usb_vbus') + '\n'
code += 'static void\n' + function('sweet_usb_probe') + '\n'
code += r'''
static void reset(void) {
    memset(core, 0, sizeof(core)); memset(phy, 0, sizeof(phy));
    maps = starts = phy_reads = 0; dreamlte_phy = 0;
    core[0xc120/4] = 0x5533280a;
    core[0xc110/4] = 0x30c11004;
}
int main(void) {
    reset(); mode = 0; sweet_usb_probe(); assert(!maps && !starts);
    reset(); mode = 3; sweet_usb_probe(); assert(!maps && !starts);
    reset(); mode = 1; sweet_usb_probe(); assert(maps == 1 && !phy_reads && !starts);
    reset(); mode = 2; core[0xc120/4] = 0xffffffff; sweet_usb_probe();
    assert(maps == 1 && !phy_reads && !starts);
    reset(); core[0xc704/4] = 1u << 31; sweet_usb_probe();
    assert(maps == 1 && !phy_reads && !starts);
    reset(); phy[0] = 0x010101; phy[0x14/4] = 2; sweet_usb_probe();
    assert(!starts && core[0xc110/4] == 0x30c11004);
    reset(); phy[0] = 0x010101; phy[0x0c/4] = 3; sweet_usb_probe();
    assert(!starts && core[0xc110/4] == 0x30c11004);
    reset(); phy[0] = 0xffffffff; sweet_usb_probe(); assert(!starts);
    for (unsigned shifted = 0; shifted < 2; shifted++) {
        reset(); unsigned off = shifted ? 4 : 0;
        phy[0] = shifted ? 0x010101 : 0;
        phy[(off+0x04)/4] = 0x51000000;
        phy[(off+0x08)/4] = 0xa000001c;
        sweet_usb_probe(); assert(starts == 1 && maps == 2);
        assert(dreamlte_phy == (uintptr_t)phy + off);
        assert(core[0xc110/4] == 0x30c12004);
        dreamlte_usb_vbus();
        assert(phy[(off+0x04)/4] == 0x51000180);
        assert(phy[(off+0x08)/4] == 0xa0000640);
    }
    puts("PASS: actual S8 wrapper refusal paths, device mode, PHY layout and VBUS masks");
}
'''
with tempfile.TemporaryDirectory(prefix='dreamlte-usb-test-') as tmp:
    path = pathlib.Path(tmp)
    (path / 'test.c').write_text(code)
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', str(path / 'test.c'), '-o', str(path / 'test')], check=True)
    subprocess.run([str(path / 'test')], check=True)
