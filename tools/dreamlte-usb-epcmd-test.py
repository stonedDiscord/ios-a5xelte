#!/usr/bin/env python3
"""Test actual EP command completion/error flow with modeled MMIO, not hardware."""
import pathlib
import re
import subprocess
import sys
import tempfile

source = pathlib.Path(sys.argv[1]).read_text()


def function(name):
    match = re.search(r'\b' + name + r'\([^;{}]*\)\s*\{', source)
    assert match, name
    opening = source.index('{', match.start())
    depth, end = 1, opening + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[match.start():end]


code = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#define DREAMLTE 1
#define GCTL 0xc110
#define DCTL 0xc704
#define DSTS 0xc70c
#define DALEPENA 0xc720
#define DEPCMDPAR0(n) (0xc808 + 0x10*(n))
#define DEPCMDPAR1(n) (0xc804 + 0x10*(n))
#define DEPCMDPAR2(n) (0xc800 + 0x10*(n))
#define DEPCMD(n) (0xc80c + 0x10*(n))
#define DEPCMD_CMDACT (1u << 10)
static uint32_t regs[0x10000/4];
static uint32_t phyregs[0x100/4];
static uintptr_t dreamlte_phy;
static unsigned writes, delays, mode, reads, logs;
static char output[4096];
static int capture(const char *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    size_t used = strlen(output);
    int result = vsnprintf(output + used, sizeof(output) - used, fmt, args);
    va_end(args);
    logs++;
    return result;
}
#define printf capture
static void dwc_wr(unsigned off, uint32_t value) {
    assert(off < sizeof(regs)); regs[off/4] = value; writes++;
}
static uint32_t dwc_rd(unsigned off) {
    assert(off < sizeof(regs));
    if (off >= 0xc80c && off <= 0xc9fc && (off & 0xf) == 0xc) {
        reads++;
        if (mode != 2 && reads >= 3) {
            regs[off/4] &= ~DEPCMD_CMDACT;
            regs[off/4] |= mode << 12;
        }
    }
    return regs[off/4];
}
static void delay(unsigned n) { assert(n == 1); delays++; }
'''
has_phy_snapshot = 'DREAMLTE USB PHY:' in source
if has_phy_snapshot:
    code += r'''
static uint32_t usb_rd(uintptr_t base, unsigned off) {
    assert(base == dreamlte_phy && base == (uintptr_t)phyregs);
    assert(off < sizeof(phyregs));
    return phyregs[off/4];
}
'''
has_snapshot = 'dreamlte_usb_ep_failure' in source
if has_snapshot:
    code += 'static void\n' + function('dreamlte_usb_ep_failure') + '\n'
code += 'static int\n' + function('ud_epcmd') + '\n'
code += r'''
static void reset(unsigned next) {
    memset(regs, 0, sizeof(regs)); memset(output, 0, sizeof(output));
    writes = delays = reads = logs = 0; mode = next;
    for (unsigned i = 0; i < sizeof(phyregs)/sizeof(phyregs[0]); i++)
        phyregs[i] = 0xa5000000u | i;
    dreamlte_phy = (uintptr_t)phyregs;
}
int main(void) {
    for (unsigned ep = 0; ep < 32; ep++) {
        reset(0);
        assert(ud_epcmd(ep, 9, 0x11, 0x22, 0x33) == 0);
        assert(writes == 4 && delays == 2 && logs == 0);
        assert(regs[DEPCMDPAR0(ep)/4] == 0x11);
        assert(regs[DEPCMDPAR1(ep)/4] == 0x22);
        assert(regs[DEPCMDPAR2(ep)/4] == 0x33);
        reset(1);
        assert(ud_epcmd(ep, 1, 0x44, 0x55, 0x66) == -1);
        assert(writes == 4 && delays == 2 && strstr(output, "status 1"));
#ifdef HAS_SNAPSHOT
        assert(strstr(output, "PAR0=00000044"));
#ifdef HAS_PHY_SNAPSHOT
        assert(logs == 8 && strstr(output, "Q=a500000d SEL=a500001b"));
#else
        assert(logs == 5);
#endif
#endif
        reset(2);
        assert(ud_epcmd(ep, 2, 1, 0, 0) == -1);
        assert(writes == 4 && delays == 1000 && strstr(output, "timeout"));
#ifdef HAS_SNAPSHOT
        assert(strstr(output, "DREAMLTE USB FAIL:"));
#ifdef HAS_PHY_SNAPSHOT
        assert(logs == 8 && strstr(output, "DREAMLTE USB PHY:"));
        for (unsigned i = 0; i < sizeof(phyregs)/sizeof(phyregs[0]); i++)
            assert(phyregs[i] == (0xa5000000u | i));
        reset(2); dreamlte_phy = 0;
        assert(ud_epcmd(ep, 1, 0, 0, 0) == -1);
        assert(writes == 4 && logs == 6 && !strstr(output, "DREAMLTE USB PHY:"));
#else
        assert(logs == 5);
#endif
#endif
    }
    puts("PASS: actual EP command parameter writes, delayed completion, status failure and bounded timeout; failure snapshots never write MMIO");
}
'''
with tempfile.TemporaryDirectory(prefix='dreamlte-epcmd-') as tmp:
    path = pathlib.Path(tmp)
    (path / 'test.c').write_text(code)
    command = ['cc', '-std=c11', '-Wall', '-Wextra', '-Werror']
    if has_snapshot:
        command.append('-DHAS_SNAPSHOT=1')
    if has_phy_snapshot:
        command.append('-DHAS_PHY_SNAPSHOT=1')
    subprocess.run(command + [str(path / 'test.c'), '-o', str(path / 'test')], check=True)
    subprocess.run([str(path / 'test')], check=True)
