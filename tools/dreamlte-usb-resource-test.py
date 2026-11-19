#!/usr/bin/env python3
"""Check actual source-derived transfer-resource allocation order and failures."""
import pathlib
import re
import subprocess
import sys
import tempfile

source = pathlib.Path(sys.argv[1]).read_text()
match = re.search(r'dreamlte_usb_resources\(void\)\s*\{', source)
assert match
opening = source.index('{', match.start())
depth, end = 1, opening + 1
while depth:
    depth += (source[end] == '{') - (source[end] == '}')
    end += 1
function = source[match.start():end]
critical = function[function.index('if (ud_epcmd(0, DEPCMD_DEPSTARTCFG'):function.index('printf("DREAMLTE USB: STARTCFG completed')]
assert 'printf(' not in critical, 'framebuffer output during resource allocation'
cmd = source[source.index('ud_epcmd(unsigned ep,'):source.index('/* Samsung gadget.c start_config')]
prefix = cmd[:cmd.index('dwc_wr(DEPCMDPAR0')]
assert 'printf(' not in prefix and 'dreamlte_usb_clocks_print(' not in prefix
code = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#define DEPCMD_DEPSTARTCFG 9
#define DEPCMD(n) (0xc80c + 0x10*(n))
#define DEPCMD_SETTRANSFRESOURCE 2
static unsigned in_count, out_count, calls, fail_at;
static unsigned eps[33], cmds[33];
static uintptr_t dreamlte_phy;
static uint32_t usb_rd(uintptr_t base, unsigned off) {
    assert(base == dreamlte_phy);
    assert(off == 0x10 || off == 0x0c || off == 0x28);
    return off == 0x0c ? 0x10 : 0;
}
static uint32_t dwc_rd(unsigned off) {
    if (off == DEPCMD(0)) return 9;
    assert(off == 0xc14c);
    return (in_count << 18) | ((in_count + out_count) << 12);
}
static int ud_epcmd(unsigned ep, uint32_t cmd, uint32_t p0, uint32_t p1, uint32_t p2) {
    assert(calls < 33 && !p1 && !p2);
    assert(p0 == (cmd == DEPCMD_SETTRANSFRESOURCE));
    eps[calls] = ep; cmds[calls] = cmd;
    return ++calls == fail_at ? -1 : 0;
}
'''
code += 'static int\n' + function + '\n'
code += r'''
int main(void) {
    for (in_count = 0; in_count <= 17; in_count++) {
        for (out_count = 0; out_count <= 17; out_count++) {
            calls = 0; fail_at = 0;
            int valid = in_count >= 3 && in_count <= 16 && out_count >= 2 && out_count <= 16;
            int result = dreamlte_usb_resources();
            if (!valid) { assert(result == -1 && calls == 0); continue; }
            assert(result == 0 && calls == 1 + in_count + out_count);
            assert(eps[0] == 0 && cmds[0] == DEPCMD_DEPSTARTCFG);
            for (unsigned n = 0; n < out_count; n++) {
                assert(eps[1+n] == 2*n && cmds[1+n] == DEPCMD_SETTRANSFRESOURCE);
            }
            for (unsigned n = 0; n < in_count; n++) {
                assert(eps[1+out_count+n] == 2*n+1 && cmds[1+out_count+n] == DEPCMD_SETTRANSFRESOURCE);
            }
            unsigned total = calls;
            for (fail_at = 1; fail_at <= total; fail_at++) {
                calls = 0;
                assert(dreamlte_usb_resources() == -1 && calls == fail_at);
            }
        }
    }
    puts("PASS: all endpoint count combinations and every resource-command failure stop; STARTCFG precedes unique resource assignments");
}
'''
with tempfile.TemporaryDirectory(prefix='dreamlte-resources-') as temp:
    path = pathlib.Path(temp)
    (path / 'test.c').write_text(code)
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', str(path / 'test.c'), '-o', str(path / 'test')], check=True)
    result = subprocess.run([str(path / 'test')], check=True, capture_output=True, text=True)
    print(result.stdout.splitlines()[-1])
