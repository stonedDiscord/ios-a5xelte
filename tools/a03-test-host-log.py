#!/usr/bin/env python3
"""Exercise actual HOST log budgets, independent sites and saturation."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parent.parent
patch=(root/'xnu/a03/0130-a03-bound-host-mig-diagnostics.patch').read_text()
part=patch.split('+++ b/osfmk/kern/host.c',1)[1].split('--- a/osfmk/kern/ipc_kobject.c',1)[0]
s='\n'.join(l[1:] for l in part.splitlines() if l.startswith('+'))
a=s.index('boolean_t a03_host_log_allowed');b=s.index('#endif',a);s=s[a:b]
pre='#include <assert.h>\n#include <stdbool.h>\n#include <stdio.h>\ntypedef int boolean_t;\n#define TRUE 1\n#define FALSE 0\n'
tests=r'''
int main(void){
assert(!a03_host_log_allowed(99,FALSE));assert(!a03_host_log_allowed(99,TRUE));
for(unsigned site=0;site<4;site++){
 for(unsigned i=0;i<8;i++)assert(a03_host_log_allowed(site,FALSE));
 for(unsigned i=0;i<10000;i++)assert(!a03_host_log_allowed(site,FALSE));
}
for(unsigned i=0;i<16;i++)assert(a03_host_log_allowed(i%4,TRUE));
for(unsigned i=0;i<10000;i++)assert(!a03_host_log_allowed(i%4,TRUE));
puts("A03 actual HOST diagnostics: four independent8-report budgets, separate16 failures, saturation PASS");}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'t.c').write_text(pre+s+tests)
 subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror',str(p/'t.c'),'-o',str(p/'t')],check=True)
 subprocess.run([str(p/'t')],check=True)
