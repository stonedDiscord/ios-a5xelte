#!/usr/bin/env python3
"""Exercise the actual bounded crash walker with synthetic user memory."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix='a03-stack-') as directory:
    d = Path(directory)
    target = d/'osfmk/kern/exception.c'
    target.parent.mkdir(parents=True)
    patch = (root/'xnu/a03/0108-a03-bounded-daemon-crash-diagnostics.patch').read_text()
    section = patch.split('+++ b/osfmk/kern/exception.c', 1)[1].split('--- a/bsd/conf/', 1)[0]
    source = '\n'.join(line[1:] for line in section.splitlines() if line.startswith('+'))
    target.write_text(source+'\n')
    subprocess.run(['git', 'apply', '--unidiff-zero', str(root/'xnu/a03/0116-a03-deeper-bounded-crash-stack.patch')], cwd=d, check=True)
    source = target.read_text()
    walker = source[source.index('char line[544];'):source.index('\n}\n#endif')]
    header = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef uintptr_t user_addr_t;
static uint64_t frames[32][2];
static unsigned reads, fail_at;
static int copyin(user_addr_t address, void *out, size_t size) {
 assert(address >= (uintptr_t)frames && address < (uintptr_t)(frames+32));
 assert(size == 16);
 if (++reads == fail_at) return 1;
 memcpy(out, (void *)address, size); return 0;
}
static void walk(uint64_t fp) { const char *name = "backboardd";
'''
    tests = r'''
}
int main(void) {
 for(unsigned i=0;i<32;i++) {frames[i][0]=(uintptr_t)(frames+i+1);frames[i][1]=0x100000000ULL+i;}
 walk((uintptr_t)frames);assert(reads==24);
 reads=0;walk(0);assert(reads==0);
 walk((uintptr_t)frames+1);assert(reads==0);
 fail_at=3;walk((uintptr_t)frames);assert(reads==3);
 fail_at=0;reads=0;frames[0][0]=(uintptr_t)frames;walk((uintptr_t)frames);assert(reads==1);
 reads=0;frames[0][0]=0;walk((uintptr_t)frames);assert(reads==1);
 puts("A03 actual crash walker24-frame cap/alignment/copy failure/nonmonotonic PASS");
}
'''
    test = d/'test.c'
    test.write_text(header+walker+tests)
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', '-Wno-format', str(test), '-o', str(d/'test')], check=True)
    subprocess.run([str(d/'test')], check=True)
