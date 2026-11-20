#!/usr/bin/env python3
"""Exercise the actual0171 retained RTC path without USB or hardware."""
from pathlib import Path
import subprocess
import tempfile
ROOT = Path(__file__).resolve().parents[1]
patch = (ROOT/'xnu/a03/0171-a03-retained-rtc-boot-time.patch').read_text()
added = '\n'.join(s[1:] for s in patch.splitlines() if s.startswith('+') and not s.startswith('+++'))
source = added[added.index('/* SC2730'):added.index(' if (!adi) adi=ml_io_map')]
assert (ROOT/'xnu/a03/a03_rtc.h').read_text().strip() in source
header = r'''
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
typedef uintptr_t vm_offset_t;
static vm_offset_t adi;
static unsigned adi_runtime_busy, reads, gates, maps, fail, mode;
static uint64_t epoch;
static int adi_read(unsigned reg, uint32_t *v) {
 unsigned sample = reads++ / 6;
 if (fail && reads == fail) return 0;
 uint64_t t = epoch;
 if (mode == 2 && sample == 0) t -= 1;
 if (mode == 3) t += sample;
 switch(reg) {
 case 0x25c: *v=mode==1?0x96:0x6900; break;
 case 0x20c: *v=t/86400; break;
 case 0x208: *v=(t/3600)%24; break;
 case 0x204: *v=(t/60)%60; break;
 case 0x200: *v=mode==4?63:t%60; break;
 default: assert(0);
 }
 return 1;
}
static vm_offset_t ml_io_map(vm_offset_t p, unsigned size) {
 maps++; assert((p==0x64000000 && size==0x1000) || (p==0x64200000 && size==0x40000));
 return fail==100+maps?0:p;
}
static void update(vm_offset_t p,unsigned off,uint32_t clear,uint32_t set) {
 assert(p==0x64000000 && off==8 && !clear && set==(1u<<9)); gates++;
}
'''
tests = r'''
static void reset(void) {
 adi=0;adi_runtime_busy=reads=gates=maps=fail=mode=0;epoch=1795188867;
}
int main(void) {
 uint64_t out;
 reset();out=0;assert(a03_rtc_get_utc(&out) && out==epoch && reads==12 && !adi_runtime_busy);
 assert(a03_rtc_get_utc(&out) && maps==3); /* retained ADI map */
 reset();adi_runtime_busy=1;assert(!a03_rtc_get_utc(&out) && !maps && !reads);
 reset();assert(!a03_rtc_get_utc(0) && !maps);
 for(unsigned i=1;i<=12;i++){reset();fail=i;out=17;assert(!a03_rtc_get_utc(&out) && out==17 && !adi_runtime_busy);}
 for(unsigned i=101;i<=102;i++){reset();fail=i;assert(!a03_rtc_get_utc(&out) && !reads && !adi_runtime_busy);}
 reset();mode=1;assert(!a03_rtc_get_utc(&out));
 reset();mode=2;epoch=1795219200;assert(a03_rtc_get_utc(&out) && out==epoch && reads==18);
 reset();mode=3;assert(!a03_rtc_get_utc(&out) && reads==24);
 reset();mode=4;assert(!a03_rtc_get_utc(&out));
 reset();epoch=553;assert(!a03_rtc_get_utc(&out));
 reset();epoch=1577836800;assert(a03_rtc_get_utc(&out) && out==epoch);
 reset();epoch=4102444799;assert(a03_rtc_get_utc(&out) && out==epoch);
 reset();epoch=4102444800;assert(!a03_rtc_get_utc(&out));
 puts("PASS actual0171 RTC: retained UTC, no USB calls, ADI ownership, bounds, reset rejection, rollover, map/read failures, ASan/UBSan");
}
'''
with tempfile.TemporaryDirectory(prefix='a03-rtc-') as d:
    c=Path(d)/'test.c';c.write_text(header+source+tests)
    subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(c),'-o',d+'/test'],check=True)
    subprocess.run([d+'/test'],check=True)
