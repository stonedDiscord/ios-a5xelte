#!/usr/bin/env python3
"""Exercise the actual A03 button debounce and PMIC setup on the host."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
patch = (root / 'xnu/a03/0195-a03-physical-buttons.patch').read_text()
added = '\n'.join(line[1:] for line in patch.splitlines() if line.startswith('+') and not line.startswith('+++'))
code = added[added.index('#define A03_KEY_EIC_DATA'):added.index('static vm_offset_t')]
fixture = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
static unsigned events, last_key, last_down;
static uint32_t mask = 0x100;
static unsigned reads, writes, fail_read, ignore_write;

void sweet_hid_key(int key, int down) {
 events++;
 last_key = key;
 last_down = down;
}
static int adi_read(unsigned reg, uint32_t *value) {
 assert(reg == 0x284);
 if (++reads == fail_read) return 0;
 *value = mask;
 return 1;
}
static int adi_write_raw(unsigned reg, uint32_t value) {
 assert(reg == 0x284 && value == (mask | 0x12));
 writes++;
 if (!ignore_write) mask = value;
 return 1;
}
'''
checks = r'''
int main(void) {
 struct a03_key_state key = {0};
 for (unsigned i = 0; i < 20; i++) a03_key_sample(&key, 0, 1);
 assert(events == 0); /* Power held across boot is ignored. */
 a03_key_sample(&key, 0, 0);
 a03_key_sample(&key, 0, 1);
 a03_key_sample(&key, 0, 0);
 a03_key_sample(&key, 0, 0);
 assert(events == 0);
 a03_key_sample(&key, 0, 1);
 a03_key_sample(&key, 0, 0);
 a03_key_sample(&key, 0, 1);
 assert(events == 0); /* Single-sample bounce is ignored. */
 a03_key_sample(&key, 0, 1);
 assert(events == 1 && last_key == 0 && last_down == 1);
 for (unsigned i = 0; i < 7; i++) a03_key_sample(&key, 0, -1);
 assert(events == 1);
 a03_key_sample(&key, 0, -1);
 assert(events == 2 && last_key == 0 && last_down == 0);
 for (unsigned i = 0; i < 20; i++) a03_key_sample(&key, 0, 1);
 assert(events == 2); /* No phantom press after a bus fault. */
 a03_key_sample(&key, 0, 0);
 a03_key_sample(&key, 0, 0);
 a03_key_sample(&key, 0, 1);
 a03_key_sample(&key, 0, 1);
 a03_key_sample(&key, 0, 0);
 a03_key_sample(&key, 0, 0);
 assert(events == 4 && last_down == 0);

 fail_read = 1;
 assert(!a03_key_pmic_init() && writes == 0);
 fail_read = 0;
 ignore_write = 1;
 assert(!a03_key_pmic_init() && writes == 1 && mask == 0x100);
 ignore_write = 0;
 assert(a03_key_pmic_init() && writes == 2 && mask == 0x112);
 assert(a03_key_pmic_init() && writes == 2);
 puts("PASS A03 physical buttons: debounce, release/rearm, PMIC mask preservation and readback");
}
'''
with tempfile.TemporaryDirectory() as d:
    source = Path(d) / 'buttons.c'
    binary = Path(d) / 'buttons'
    source.write_text(fixture + code + checks)
    subprocess.run(['clang', '-Wall', '-Wextra', '-Werror', '-fsanitize=address,undefined',
                    str(source), '-o', str(binary)], check=True)
    subprocess.run([str(binary)], check=True)
