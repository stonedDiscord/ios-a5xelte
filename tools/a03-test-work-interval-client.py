#!/usr/bin/env python3
"""Check actual documented unrestricted client-type privilege policy."""
from pathlib import Path
import subprocess,tempfile
p=Path(__file__).resolve().parents[1]/'xnu/a03/0155-a03-unrestricted-client-work-interval.patch'
s='\n'.join(x[1:] for x in p.read_text().splitlines() if x.startswith('+') and not x.startswith('+++'))
s=s[s.index('static bool\na03_wi_unrestricted'):s.index('static void\na03_wi_create_log')]
# Apply the follow-up policy hunk to the actual function under test.
follow=p.with_name('0156-a03-ios16-ca-client-work-interval.patch').read_text()
old='\n'.join(l[1:] for l in follow.splitlines() if l.startswith('-') and not l.startswith('---'))
new='\n'.join(l[1:] for l in follow.splitlines() if l.startswith('+') and not l.startswith('+++'))
assert old in s
s=s.replace(old,new)
pre='''#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
static unsigned a03_wi_client_compat;
#define WORK_INTERVAL_FLAG_UNRESTRICTED 4
#define WORK_INTERVAL_TYPE_MASK 0xf0000000u
#define WORK_INTERVAL_TYPE_DEFAULT 0
#define WORK_INTERVAL_TYPE_COREAUDIO 0x10000000u
#define WORK_INTERVAL_TYPE_CA_CLIENT 0x30000000u
'''
test='''int main(void){
for(unsigned enabled=0;enabled<2;enabled++){
 a03_wi_client_compat=enabled;
 for(unsigned type=0;type<16;type++)for(unsigned low=0;low<256;low++){
  uint32_t flags=(type<<28)|low;
  bool expected=enabled&&(type==3||((low&4)&&(type==0||type==1)));
  assert(a03_wi_unrestricted(flags)==expected);
 }
}
}
'''
with tempfile.TemporaryDirectory() as d:
 f=Path(d)/'test.c';f.write_text(pre+s+test)
 for cc,lang,std in [('clang','c','c11'),('clang++','c++','c++17')]:
  subprocess.run([cc,'-x',lang,'-std='+std,'-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(f),'-o',d+'/test'],check=True)
  subprocess.run([d+'/test'],check=True)
print('PASS actual client policy C/C++ ASan/UBSan: opt-in, implicit CA_CLIENT, restricted DEFAULT/COREAUDIO flags across8192flag cases')
