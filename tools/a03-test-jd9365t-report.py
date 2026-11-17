#!/usr/bin/env python3
"""Exercise the actual preparatory Jadard decoder with ASan/UBSan."""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = r'''
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "shim/a03/jd9365t-report.h"

static void point(uint8_t *p, unsigned slot, unsigned x, unsigned y)
{
    p += 3 + slot * 5;
    p[0] = x >> 8; p[1] = x; p[2] = y >> 8; p[3] = y; p[4] = 42;
}

int main(void)
{
    uint8_t packet[60];
    struct a03_jd9365t_report r, saved;
    memset(packet, 0xff, sizeof(packet));
    packet[0] = 0;
    assert(!a03_jd9365t_decode(packet, sizeof(packet), &r));
    for (unsigned i = 0; i < 10; i++) assert(!r.contacts[i].down);
    packet[0] = 1;
    point(packet, 9, 360, 1560); /* sparse slot, never use count as loop bound */
    assert(!a03_jd9365t_decode(packet, sizeof(packet), &r));
    assert(r.reported_count == 1 && r.contacts[9].down);
    assert(r.contacts[9].x == 360 && r.contacts[9].y == 1560);
    assert(r.contacts[9].width == 42 && !r.contacts[0].down);
    point(packet, 9, 360, 460);
    assert(!a03_jd9365t_decode(packet, sizeof(packet), &r));
    assert(r.contacts[9].y == 460);
    packet[0] = 10;
    for (unsigned i = 0; i < 10; i++) point(packet, i, i * 72, i * 160);
    point(packet, 0, 0, 0); point(packet, 9, 720, 1600);
    for (unsigned i = 0; i < 5; i++) packet[53 + i] = 20 + i;
    assert(!a03_jd9365t_decode(packet, sizeof(packet), &r));
    for (unsigned i = 0; i < 10; i++) assert(r.contacts[i].down);
    assert(r.contacts[9].x == 720 && r.contacts[9].y == 1600);
    for (unsigned i = 0; i < 5; i++) assert(r.state[i] == 20 + i);
    point(packet, 1, 721, 10); point(packet, 2, 10, 1601);
    assert(!a03_jd9365t_decode(packet, sizeof(packet), &r));
    assert(!r.contacts[1].down && !r.contacts[2].down);
    memset(packet + 3, 0xff, 50); packet[0] = 0;
    assert(!a03_jd9365t_decode(packet, sizeof(packet), &r));
    for (unsigned i = 0; i < 10; i++) assert(!r.contacts[i].down);
    memcpy(&saved, &r, sizeof(r));
    for (size_t n = 0; n <= 61; n++) {
        if (n == 60) continue;
        assert(a03_jd9365t_decode(packet, n, &r) == -1);
        assert(!memcmp(&r, &saved, sizeof(r)));
    }
    assert(a03_jd9365t_decode(NULL, 60, &r) == -1);
    assert(a03_jd9365t_decode(packet, 60, NULL) == -1);
    for (unsigned count = 11; count <= 255; count++) {
        packet[0] = count;
        assert(a03_jd9365t_decode(packet, 60, &r) == -1);
        assert(!memcmp(&r, &saved, sizeof(r)));
    }
    puts("PASS Jadard decoder: sparse/ten contacts, big endian, move/release,"
         " inclusive bounds, state bytes, null/length/count rejection");
}
'''


def main():
    with tempfile.TemporaryDirectory(prefix='a03-jadard-') as directory:
        source = Path(directory) / 'test.c'
        source.write_text(SOURCE)
        for compiler, standard in (('clang', 'c11'), ('clang++', 'c++17')):
            binary = Path(directory) / compiler
            subprocess.run([compiler, '-x', 'c++' if compiler == 'clang++' else 'c',
                            '-std=' + standard, '-Wall', '-Wextra', '-Werror',
                            '-Wno-missing-field-initializers',
                            '-fsanitize=address,undefined', '-I', str(ROOT),
                            str(source), '-o', str(binary)], check=True)
            subprocess.run([str(binary)], check=True)


if __name__ == '__main__':
    main()
