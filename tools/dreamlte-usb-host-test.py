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
has_core_timing = 'dreamlte_usb_core_timing' in source
has_phy_power = 'dreamlte_usb_phy_power_up' in source
has_link_wake = 'dreamlte_usb_link_wake' in source
has_reset_wake = 'Reapply after DCTL reset as well' in source

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

if 'DREAMLTE USB: session LINK=' in source:
    startup = function('sweet_usb_gadget_start')
    sessions = [m.start() for m in re.finditer(r'\bdreamlte_usb_vbus\(\);', startup)]
    reset = startup.index('dwc_wr(DCTL, DCTL_CSFTRST)')
    timing = startup.index('dreamlte_usb_core_timing(dwc)')
    endpoints = startup.index('dreamlte_usb_resources()')
    assert len(sessions) == 2 and sessions[0] < reset < timing < sessions[1] < endpoints
    print('PASS: session-valid before reset and reasserted before endpoint commands')

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
static unsigned delays;
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
if has_link_wake:
    code += '#define HAS_LINK_WAKE 1\n'
    code += 'static void delay(unsigned us) { assert(us == 500 || us == 10 || us == 1000); delays++; }\n'
    code += 'static int\n' + function('dreamlte_usb_link_wake') + '\n'
if has_phy_power:
    code += '#define HAS_PHY_POWER 1\nstatic int\n' + function('dreamlte_usb_phy_power_up') + '\n'
code += 'static int\n' + function('dreamlte_usb_prepare') + '\n'
if has_core_timing:
    code += '#define HAS_CORE_TIMING 1\n'
    if has_reset_wake:
        code += '#define HAS_RESET_WAKE 1\n'
    code += 'static void\n' + function('dreamlte_usb_core_timing') + '\n'
code += 'static void\n' + function('dreamlte_usb_vbus') + '\n'
code += 'static void\n' + function('sweet_usb_probe') + '\n'
code += r'''
static void reset(void) {
    memset(core, 0, sizeof(core)); memset(phy, 0, sizeof(phy));
    maps = starts = phy_reads = delays = 0; dreamlte_phy = 0;
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
    reset(); core[0xc704/4] = 1u << 30; sweet_usb_probe();
    assert(maps == 1 && !phy_reads && !starts);
    reset(); phy[0] = 0x010101; phy[0x14/4] = 2; sweet_usb_probe();
    assert(!starts && core[0xc110/4] == 0x30c11004);
    reset(); phy[0] = 0x010101; phy[0x0c/4] = 3; sweet_usb_probe();
    assert(!starts && core[0xc110/4] == 0x30c11004);
    reset(); phy[0] = 0xffffffff; sweet_usb_probe(); assert(!starts);
#if defined(HAS_CORE_TIMING)
    reset(); core[0xc200/4] = 1u << 31; sweet_usb_probe();
    assert(!starts && !dreamlte_phy && core[0xc110/4] == 0x30c11004);
    reset(); core[0xc110/4] |= 1u << 11; sweet_usb_probe();
    assert(!starts && !dreamlte_phy);
#endif
    for (unsigned shifted = 0; shifted < 2; shifted++) {
        reset(); unsigned off = shifted ? 4 : 0;
        phy[0] = shifted ? 0x010101 : 0;
        phy[(off+0x04)/4] = 0x41000000;
        phy[(off+0x08)/4] = 0xa000001c;
#if defined(HAS_CORE_TIMING)
        core[0xc200/4] = 0x40102540;
#endif
        sweet_usb_probe(); assert(starts == 1 && maps == 2);
        assert(dreamlte_phy == (uintptr_t)phy + off);
        assert(core[0xc110/4] == 0x30c12004);
#if defined(HAS_CORE_TIMING)
        assert(core[0xc200/4] == 0x40102400);
        core[0xc110/4] |= 0xc0;
#ifdef HAS_RESET_WAKE
        /* Model the low-power defaults observed after0220 link reset. */
        core[0xc200/4] = 0x40102540;
#endif
        dreamlte_usb_core_timing((uintptr_t)core);
        assert(core[0xc110/4] == 0x80e92004);
#ifdef HAS_RESET_WAKE
        assert(core[0xc200/4] == 0x40102400);
        for (unsigned bit = 0; bit < 32; bit++) {
            unsigned before = 1u << bit;
            core[0xc200/4] = before;
            dreamlte_usb_core_timing((uintptr_t)core);
            assert(core[0xc200/4] == (before & ~0x140u));
        }
#endif
        for (unsigned bits = 0; bits < 32; ++bits) {
            unsigned before = 1u << bits;
            core[0xc110/4] = before;
            dreamlte_usb_core_timing((uintptr_t)core);
            unsigned after = core[0xc110/4];
            assert((after & (0x1fffu << 19)) == (4125u << 19));
            assert(!(after & 0xc0));
            assert((after & ~((0x1fffu << 19) | 0xc0u)) ==
                (before & ~((0x1fffu << 19) | 0xc0u)));
        }
#endif
        dreamlte_usb_vbus();
        assert(phy[(off+0x04)/4] == 0x41000180);
        assert(phy[(off+0x08)/4] == 0xa0000640);
#ifdef HAS_LINK_WAKE
        assert(delays == 5);
        assert(phy[(off+0x34)/4] == 0x3e00);
        for (unsigned bit = 0; bit < 32; bit++) {
            uint32_t before = 1u << bit;
            phy[(off+0x34)/4] = before;
            phy[(off+0x04)/4] = 0x08000000;
            assert(dreamlte_usb_link_wake((uintptr_t)phy+off) == 0);
            assert(phy[(off+0x34)/4] == (before | 0x3e00));
            assert(phy[(off+0x04)/4] == 0x08000000);
        }
#ifdef HAS_PHY_POWER
        for (unsigned bit = 0; bit < 32; bit++) {
            uint32_t before = (1u << bit) | 0xcu;
            phy[(off+0x28)/4] = before;
            assert(dreamlte_usb_phy_power_up((uintptr_t)phy+off) == 0);
            assert(phy[(off+0x28)/4] == (before & ~0xcu));
        }
        phy[(off+0x28)/4] = 0xcu;
        assert(dreamlte_usb_phy_power_up((uintptr_t)phy+off) == 0);
        assert(phy[(off+0x28)/4] == 0);
        for (unsigned bit = 0; bit < 6; bit++) {
            phy[(off+0x6c)/4] = 1u << bit;
            phy[(off+0x28)/4] = 0xcu;
            unsigned prior_power = delays;
            assert(dreamlte_usb_phy_power_up((uintptr_t)phy+off) == -1);
            assert(phy[(off+0x28)/4] == 0xcu && delays == prior_power);
        }
        phy[(off+0x6c)/4] = 0;
        phy[(off+0x28)/4] = 0xffffffffu;
        assert(dreamlte_usb_phy_power_up((uintptr_t)phy+off) == -1);
        assert(phy[(off+0x28)/4] == 0xffffffffu);
#endif
        phy[(off+0x34)/4] = 0x7c00;
        assert(dreamlte_usb_link_wake((uintptr_t)phy+off) == 0);
        assert(phy[(off+0x34)/4] == 0x7e00);
        phy[(off+0x6c)/4] = 1u << 3;
        unsigned prior = delays;
        assert(dreamlte_usb_link_wake((uintptr_t)phy+off) == -1);
        assert(delays == prior && phy[(off+0x34)/4] == 0x7e00);
        phy[(off+0x6c)/4] = 0;
        phy[(off+0x04)/4] |= 1u << 28;
        assert(dreamlte_usb_link_wake((uintptr_t)phy+off) == -1);
        assert(delays == prior);
#endif
    }
    puts("PASS: actual S8 wrapper refusal paths, device mode, PHY layout and VBUS masks");
}
'''
with tempfile.TemporaryDirectory(prefix='dreamlte-usb-test-') as tmp:
    path = pathlib.Path(tmp)
    (path / 'test.c').write_text(code)
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', str(path / 'test.c'), '-o', str(path / 'test')], check=True)
    subprocess.run([str(path / 'test')], check=True)
