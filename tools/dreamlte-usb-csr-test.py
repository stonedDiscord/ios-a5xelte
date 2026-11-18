#!/usr/bin/env python3
"""Exercise actual event-ring CSR guard; modeled reads, no phone access."""
import pathlib
import subprocess
import sys
import tempfile
source = pathlib.Path(sys.argv[1]).read_text()
start = source.index('\tud.evt_pos = 0;')
end = source.index('\n\t/* High speed, address 0 */', start)
block = source[start:end]
code = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#define DREAMLTE 1
#define GEVNTADRLO 0xc400
#define GEVNTADRHI 0xc404
#define GEVNTSIZ 0xc408
#define UD_EVT 0x200
#define UD_EVT_SIZE 0x1000
static struct { uint64_t dma_pa; unsigned evt_pos; } ud;
static unsigned mismatch, failures, proceeded, reads;
static uint32_t dwc_rd(unsigned off) {
    reads++;
    uint32_t value;
    if (off == GEVNTADRLO) value = (uint32_t)(ud.dma_pa + UD_EVT);
    else if (off == GEVNTADRHI) value = (uint32_t)((ud.dma_pa + UD_EVT) >> 32);
    else { assert(off == GEVNTSIZ); value = (1u << 31) | UD_EVT_SIZE; }
    if (off == mismatch) value ^= 1;
    return value;
}
static void dreamlte_usb_ep_failure(unsigned ep, unsigned cmd) {
    assert(ep == 0 && cmd == 0); failures++;
}
static void check(void) {
'''+block+r'''
    proceeded++;
}
int main(void) {
    const uint64_t addresses[] = {0x90000000ull, 0x890000000ull, 0xfffffff0ull};
    const unsigned faults[] = {0, GEVNTADRLO, GEVNTADRHI, GEVNTSIZ};
    for (unsigned a = 0; a < 3; a++) {
        for (unsigned f = 0; f < 4; f++) {
            ud.dma_pa = addresses[a]; ud.evt_pos = 17;
            mismatch = faults[f]; failures = proceeded = reads = 0;
            check();
            assert(ud.evt_pos == 0 && reads == 3);
            assert(failures == (f != 0) && proceeded == (f == 0));
        }
    }
    puts("PASS: actual CSR guard accepts matching 32/64-bit event addresses; each address/size mismatch stops before endpoints");
}
'''
with tempfile.TemporaryDirectory(prefix='dreamlte-csr-') as d:
    p = pathlib.Path(d)
    (p/'test.c').write_text(code)
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', str(p/'test.c'), '-o', str(p/'test')], check=True)
    result = subprocess.run([str(p/'test')], check=True, capture_output=True, text=True)
    print(result.stdout.splitlines()[-1])
