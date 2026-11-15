#!/usr/bin/env python3
"""Check actual bounded devnull observer leaves the original uio untouched."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parent.parent
patch=(root/'xnu/a03/0125-a03-bounded-userspace-log.patch').read_text().split('--- a/bsd/conf/Makefile.template',1)[0]
s='\n'.join(l[1:] for l in patch.splitlines() if l.startswith('+') and not l.startswith('+++'))
s=s[s.index('static void'):s.index('#endif')]
pre=r'''
#include <cassert>
#include <cstdint>
#include <cstring>
#include <cstdio>
#include <algorithm>
#define MIN(a,b) std::min<long long>((a),(b))
using std::strcmp;
unsigned enabled=0,duplicates=0,moves=0,frees=0;bool copyfail=false,movefail=false;
const char *name="SpringBoard";
struct uio {long long resid;unsigned offset;};using uio_t=uio*;
long long uio_resid(uio_t u){return u->resid;}
void PE_parse_boot_argn(const char*,uint32_t *out,unsigned){*out=enabled;}
void proc_selfname(char *out,unsigned n){snprintf(out,n,"%s",name);}
uio_t uio_duplicate(uio_t u){duplicates++;return copyfail?nullptr:new uio(*u);}
int uiomove(char *p,int n,uio_t u){moves++;memset(p,'x',n);u->offset+=n;u->resid-=n;return movefail?14:0;}
void uio_free(uio_t u){frees++;delete u;}
'''
tests=r'''
int main(){uio original{1000,7};
a03_devnull_log(&original);assert(!duplicates);
enabled=1;name="other";a03_devnull_log(&original);assert(!duplicates);
name="SpringBoard";copyfail=true;a03_devnull_log(&original);assert(duplicates==1&&!moves&&!frees);
copyfail=false;movefail=true;a03_devnull_log(&original);assert(moves==1&&frees==1);
movefail=false;for(int i=0;i<140;i++)a03_devnull_log(&original);
assert(duplicates==128&&moves==127&&frees==127);
assert(original.resid==1000&&original.offset==7);
name="backboardd";original.resid=0;a03_devnull_log(&original);assert(duplicates==128);
puts("A03 actual devnull observer: opt-in/names/bounds/copy failure and original uio preservation PASS");}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'t.cpp').write_text(pre+s+tests)
 subprocess.run(['c++','-std=c++17','-Wall','-Wextra','-Werror',str(p/'t.cpp'),'-o',str(p/'t')],check=True)
 subprocess.run([str(p/'t')],check=True,stdout=subprocess.DEVNULL)
 print('A03 actual devnull observer: opt-in/names/bounds/copy failure and original uio preservation PASS')
