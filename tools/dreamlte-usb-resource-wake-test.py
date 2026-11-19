#!/usr/bin/env python3
"""Exercise actual resource-command wake code with modeled MMIO, not hardware."""
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
    return re.sub(r'__asm__ volatile\("[^"\n]*" ::: "memory"\);', '', source[match.start():end])

code = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
typedef uintptr_t vm_offset_t;
#define DREAMLTE 1
#define DEPCMD_SETTRANSFRESOURCE 2
#define DEPCMD_CMDACT (1u << 10)
#define DEPCMDPAR0(n) (0xc808 + 0x10*(n))
#define DEPCMDPAR1(n) (0xc804 + 0x10*(n))
#define DEPCMDPAR2(n) (0xc800 + 0x10*(n))
#define DEPCMD(n) (0xc80c + 0x10*(n))
static uint32_t regs[0x10000/4], phyregs[0x100/4];
static uintptr_t dreamlte_phy;
static unsigned writes, polls, settles, waits, failures, mode;
static uint32_t initial;
static char output[4096];
static int capture(const char *fmt, ...) {
    va_list args; va_start(args, fmt);
    int n = vsnprintf(output + strlen(output), sizeof(output) - strlen(output), fmt, args);
    va_end(args);
    /* Model CLK31 changing during timeout console output, after polling. */
    if (mode == 11 && strstr(fmt, "timeout")) phyregs[4] |= 1u << 31;
    return n;
}
#define printf capture
static void dwc_wr(unsigned off, uint32_t value) {
    assert(off < sizeof(regs)); regs[off/4] = value; writes++;
}
static uint32_t dwc_rd(unsigned off) {
    assert(off >= DEPCMD(0) && off <= DEPCMD(31));
    polls++;
    if (mode == 7 && polls == 3) phyregs[4] |= 1u << 31;
    if (mode == 10 && settles && polls == 2) phyregs[4] |= 1u << 31;
    if ((mode == 0 || mode == 7) && settles)
        regs[off/4] &= ~DEPCMD_CMDACT;
    return regs[off/4];
}
static uint32_t usb_rd(uintptr_t base, unsigned off) {
    assert(base == dreamlte_phy && off < sizeof(phyregs));
    if (mode == 2 && settles && off == 0x10) return phyregs[4] | (1u << 31);
    return phyregs[off/4];
}
static void delay(unsigned us) {
    if (us == 500) { settles++; assert(settles == 1); }
    else { assert(us == 1); waits++; }
}
static void dreamlte_usb_ep_failure(unsigned ep, uint32_t cmd) {
    (void)ep; (void)cmd; failures++;
}
'''
code += 'static int\n' + function('dreamlte_usb_post_reset_wake') + '\n'
code += 'static int\n' + function('ud_epcmd') + '\n'
code += r'''
static void reset(unsigned next) {
    memset(regs, 0, sizeof(regs)); memset(phyregs, 0, sizeof(phyregs));
    writes = polls = settles = waits = failures = 0; mode = next;
    memset(output, 0, sizeof(output));
    dreamlte_phy = (uintptr_t)phyregs; initial = 0x801b0048;
    phyregs[4] = initial; phyregs[3] = 0x10;
    if (mode == 3) phyregs[0x6c/4] = 1;
    if (mode == 4) phyregs[4] |= 2;
    if (mode == 5) phyregs[3] = 0;
    if (mode == 7 || mode == 8 || mode == 11) phyregs[4] &= ~(1u << 31);
    if (mode == 9) phyregs[4] = 0xffffffff;
}
int main(void) {
    for (unsigned m = 0; m <= 11; m++) {
        reset(m);
        unsigned ep = m == 6 ? 2 : 0;
        int result = ud_epcmd(ep, 2, 1, 0, 0);
        assert(writes == 4); /* Parameters once, CMDACT once. */
        assert(regs[DEPCMDPAR0(ep)/4] == 1);
        assert(regs[DEPCMDPAR1(ep)/4] == 0 && regs[DEPCMDPAR2(ep)/4] == 0);
        if (m == 0 || m == 7) {
            assert(result == 0 && settles == 1 && !failures);
            assert(phyregs[4] == (initial & ~(1u << 31)));
        } else {
            assert(result == -1 && failures == 1);
            if (m == 1 || m == 10) assert(settles == 1 && waits == 1000);
            if (m == 2) assert(settles == 1 && waits == 0);
            if (m == 3 || m == 4 || m == 5 || m == 9) {
                assert(!settles && !waits);
                assert(phyregs[4] == (m == 4 ? initial | 2 : m == 9 ? 0xffffffff : initial));
            }
            if (m == 6 || m == 8 || m == 11) assert(!settles && waits == 1000);
        }
        if (m == 8 || m == 11) {
            assert(strstr(output, "DREAMLTE USB POLL: first=001b0048 last=001b0048 exit=001b0048 n=1000 wake=0"));
            assert(phyregs[4] == (m == 11 ? initial : initial & ~(1u << 31)));
        }
        if (m == 1 || m == 10) assert(strstr(output, "n=1000 wake=1"));
        if (m == 6) assert(!strstr(output, "DREAMLTE USB POLL:"));
        assert(phyregs[3] == (m == 5 ? 0 : 0x10));
        assert(phyregs[0x6c/4] == (m == 3));
    }
    puts("PASS: actual active-resource wake; immediate/delayed suspend, completion/refusal/persistent/recurrent suspend, unrelated endpoints; one wake maximum, command never reissued, pre-log snapshot survives console-time suspend");
}
'''
with tempfile.TemporaryDirectory(prefix='dreamlte-resource-wake-') as tmp:
    path = pathlib.Path(tmp)
    (path/'test.c').write_text(code)
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', str(path/'test.c'), '-o', str(path/'test')], check=True)
    result = subprocess.run([str(path/'test')], capture_output=True, text=True, check=True)
    print(result.stdout.splitlines()[-1])
