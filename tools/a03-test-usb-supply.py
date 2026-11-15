#!/usr/bin/env python3
"""Exercise cumulative XNU USB supply code against a bounded ADI model.

No hardware claim. Tests exact rail writes, preserved bits, address echo,
busy/FIFO timeouts, rejected writes and failed physical readback.
"""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix='a03-usb-supply-') as directory:
    directory = Path(directory)
    for number in ('0103', '0104', '0106', '0109', '0110'):
        patch, = (ROOT / 'xnu/a03').glob(number + '-*.patch')
        subprocess.run(['git', 'apply', '--include=bsd/dev/a03_usb_console.c',
                        str(patch)], cwd=directory, check=True)
    source = (directory / 'bsd/dev/a03_usb_console.c').read_text()
    start = source.index('static int adi_read(')
    end = source.index('static unsigned le16(', start)
    source = source[start:end]
    a = source.index('/* Matches sprd_adi_restart_handler')
    b = source.index('static int usb_supply(', a)
    source = source[:a] + source[b:]
    header = r'''
#include <stdint.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
typedef uintptr_t vm_offset_t;
static vm_offset_t adi;
static uint32_t pmic[0x2000/4], command, write_reg[8], write_value[8];
static unsigned writes, reads, delays;
static int bad_echo, busy, full, drop_write, map_fail;
static void delay(unsigned us) { assert(us<=1000);delays++; }
static vm_offset_t ml_io_map(vm_offset_t address,unsigned size) {
 assert(address==0x64200000 && size==0x40000);return map_fail?0:1;
}
static uint32_t adi_read32(unsigned off) {
 reads++;assert(reads<20000);
 if(off==0x30)return full?0x800:0x400;
 assert(off==0x2c);
 if(busy)return 0x80000000;
 return ((((command&0x1ffff)>>2)^bad_echo)<<16)|pmic[(command&0x1ffff)/4];
}
static void adi_write32(unsigned off,uint32_t value) {
 if(off==0x28) { assert(value>=0x64220000 && value<0x64222000);command=value;return; }
 assert(off==0x21bd0 || off==0x219e8 || off==0x219ec);
 assert(writes<8);write_reg[writes]=off-0x20000;write_value[writes++]=value;
 if(!drop_write)pmic[(off-0x20000)/4]=value;
}
static void reset(void) {
 memset(pmic,0,sizeof(pmic));writes=reads=delays=0;
 bad_echo=busy=full=drop_write=map_fail=0;
 pmic[0x19e8/4]=0xa501;pmic[0x19ec/4]=0x5a00|200;
}
'''
    tests = r'''
int main(void) {
 reset();assert(usb_supply());assert(writes==3);
 assert(write_reg[0]==0x1bd0 && write_value[0]==0x6e7f);
 assert(write_reg[1]==0x19ec && write_value[1]==(0x5a00|210));
 assert(write_reg[2]==0x19e8 && write_value[2]==0xa500);
 reset();pmic[0x19e8/4]=0xa500;pmic[0x19ec/4]=0x5ad2;
 assert(usb_supply() && !writes);
 reset();pmic[0x19ec/4]=0x5ad2;assert(usb_supply() && writes==2);
 assert(write_reg[1]==0x19e8);
 reset();pmic[0x19e8/4]=0xa500;assert(usb_supply() && writes==2);
 assert(write_reg[1]==0x19ec);
 reset();bad_echo=1;assert(!usb_supply() && !writes);
 reset();busy=1;assert(!usb_supply() && !writes && delays==2000);
 reset();full=1;assert(!usb_supply() && !writes && delays==2000);
 reset();drop_write=1;assert(!usb_supply());
 reset();map_fail=1;assert(!usb_supply() && !writes && !reads);
 reset();assert(!adi_write(0x1820,0));assert(!adi_write(0x19e4,0));
 assert(!writes && !reads);
 puts("A03 USB supply allowlist/preserved-bits/timeout/readback checks PASS (host only)");
}
'''
    test = directory / 'test.c'
    test.write_text(header + source + tests)
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror',
                    str(test), '-o', str(directory / 'test')], check=True)
    subprocess.run([str(directory / 'test')], check=True)
