#!/usr/bin/env python3
"""Exercise actual explicit UTC command parsing; no device access."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
p=(ROOT/'xnu/a03/0135-a03-live-usb-probes.patch').read_text()
p='\n'.join(l[1:] for l in p.splitlines() if l.startswith('+') and not l.startswith('+++'))
start=p.index('static int a03_probe_number(');end=p.index('static ',start+12)
# Reuse exact number/end parsers from the currently patched source below.
# Their implementation is stable across0135 and the current source.
end=p.index('static ',p.index('static int a03_probe_end',start)+12)
parsers=p[start:end]
s=(ROOT/'xnu/a03/0150-a03-explicit-volatile-utc-sync.patch').read_text()
s='\n'.join(l[1:] for l in s.splitlines() if l.startswith('+') and not l.startswith('+++'))
s=s[s.index('/* Explicit volatile'):s.index(' else if(!strncmp(command,"time ')]
s=s[:s.index('\n}')+3]
prefix=r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef uint64_t clock_sec_t;typedef unsigned clock_usec_t;
static unsigned sets;static uint64_t utc=17;
static void clock_set_calendar_microtime(clock_sec_t s,clock_usec_t u){assert(!u);utc=s;sets++;}
static void clock_get_calendar_microtime(clock_sec_t*s,clock_usec_t*u){*s=utc;*u=0;}
'''
test=r'''
int main(void){a03_probe_time("status");assert(!sets&&utc==17);
 const char*bad[]={"","0","-1","1577836799","4102444800","1794945000 junk","18446744073709551616","9999999999999999999999999999"};
 for(unsigned i=0;i<sizeof(bad)/sizeof(bad[0]);i++){a03_probe_time(bad[i]);assert(!sets&&utc==17);}
 a03_probe_time("1794945000");assert(sets==1&&utc==1794945000ULL);
 a03_probe_time("1577836800");assert(sets==2&&utc==1577836800ULL);
 a03_probe_time("4102444799");assert(sets==3&&utc==4102444799ULL);
 puts("PASS actual UTC sync: status read-only, bounded Unix UTC, malformed/overflow rejection, calendar setter");}
'''
with tempfile.TemporaryDirectory(prefix='a03-time-') as d:
 p=Path(d)/'test.c';p.write_text(prefix+parsers+s+test)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
