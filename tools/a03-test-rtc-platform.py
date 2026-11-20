from pathlib import Path
import subprocess
import tempfile
import argparse
p0=argparse.ArgumentParser()
p0.add_argument('source',type=Path,help='candidate IOPlatformExpert.cpp')
p=p0.parse_args().source.read_text()
start=p.index('void'+chr(10)+'PEGetUTCTimeOfDay(')
end=p.index(chr(10)+'void'+chr(10)+'PESetUTCTimeOfDay',start)
fn=p[start:end]
pre=r'''
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
typedef uint64_t clock_sec_t;
typedef unsigned clock_usec_t;
typedef unsigned clock_nsec_t;
#define ARM64_BOARD_CONFIG_SWEET 1
#define NSEC_PER_SEC 1000000000
#define NSEC_PER_USEC 1000
#define kprintf printf
struct Platform { void getUTCTimeOfDay(clock_sec_t *s,clock_nsec_t *n) {*s=0;*n=0;} };
static Platform *gIOPlatform;
extern "C" {
'''
post=r'''
}
extern "C" void set_ok(int);
int main(){clock_sec_t s=0;clock_usec_t u=99;set_ok(1);PEGetUTCTimeOfDay(&s,&u);assert(s==1795188867&&u==0);set_ok(0);PEGetUTCTimeOfDay(&s,&u);assert(s==0&&u==0);}
'''
c=r'''
#include <stdint.h>
static int ok;
void set_ok(int value){ok=value;}
int a03_rtc_get_utc(uint64_t *p){if(!ok)return 0;*p=1795188867;return 1;}
'''
with tempfile.TemporaryDirectory(prefix='a03-platform-') as d:
 t=Path(d);(t/'hook.cpp').write_text(pre+fn+post);(t/'rtc.c').write_text(c)
 subprocess.run(['clang','-c',str(t/'rtc.c'),'-o',str(t/'rtc.o')],check=True)
 subprocess.run(['clang++','-Wall','-Wextra','-Werror',str(t/'hook.cpp'),str(t/'rtc.o'),'-o',str(t/'test')],check=True)
 subprocess.run([str(t/'test')],check=True)
 print('PASS actual platform hook: C/C++ linkage, retained UTC success, original fallback on failure')
