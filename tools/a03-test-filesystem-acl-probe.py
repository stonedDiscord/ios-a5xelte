#!/usr/bin/env python3
"""Exercise actual read-only ACL probe, bounds and vnode/ACL cleanup."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1]
# Reuse the stat harness definitions without executing its test runner.
s= (root/'tools/a03-test-filesystem-probe.py').read_text()
ns={};exec(s[s.index("header=r'''"):s.index("tests=r'''")],ns)
header=ns['header'].replace('uint64_t va_fileid,va_supported;','uint64_t va_fileid,va_supported;struct kauth_acl *va_acl;')
header=header.replace('if(get_error)return get_error;', 'a->va_supported=31;a->va_acl=acl_return;if(get_error)return get_error;')
prefix=r'''
#include <stdint.h>
#include <stdbool.h>
#define KAUTH_ACL_MAX_ENTRIES 128
struct kauth_ace {unsigned char ace_applicable[16];unsigned ace_flags,ace_rights;};
struct kauth_acl {unsigned acl_entrycount,acl_flags;struct kauth_ace acl_ace[128];};
typedef struct kauth_acl *kauth_acl_t;
static struct kauth_acl data;static kauth_acl_t acl_return;static unsigned freed;
static void kauth_acl_free(kauth_acl_t p){if(p==&data)freed++;else __builtin_trap();}
'''
# Apply the new patch to the exact stat-helper text used by the first harness.
patch=(root/'xnu/a03/0140-a03-readonly-filesystem-probe.patch').read_text()
source='\n'.join(l[1:] for l in patch.splitlines() if l.startswith('+') and not l.startswith('+++'))
source=source[:source.index('\n  printf("A03 PROBE help:')]
newpatch=(root/'xnu/a03/0141-a03-readonly-filesystem-acl-probe.patch').read_text()
# Only production function diffs; command-dispatch diff is checked separately.
with tempfile.TemporaryDirectory(prefix='a03-acl-') as d:
 d=Path(d)
 # Production helper additions + tiny signature/attribute changes come directly from patch.
 source=source.replace('a03_probe_stat(const char *path)','a03_probe_stat(const char *path, bool with_acl)')
 source=source.replace('    VATTR_WANTED(&va, va_fileid);','    VATTR_WANTED(&va, va_fileid);\n    if (with_acl) VATTR_WANTED(&va, va_acl);')
 lines=newpatch.splitlines();start=next(i for i,l in enumerate(lines) if l.startswith('+    /* vnode_getattr'))
 added=[]
 for l in lines[start:]:
  if not l.startswith('+'):break
  added.append(l[1:])
 assert added and added[-1].startswith('    } else if (with_acl')
 source=source.replace('    vnode_put(vp);','\n'.join(added)+'\n    vnode_put(vp);')
 tests=r'''
int main(void){
 a03_probe_stat("/private/var/noacl",true);assert(!freed&&puts_count==1&&!refs);
 acl_return=&data;data.acl_entrycount=2;data.acl_flags=3;data.acl_ace[1].ace_rights=7;
 a03_probe_stat("/private/var/acl",true);assert(freed==1&&puts_count==2&&!refs);
 data.acl_entrycount=17;a03_probe_stat("/private/var/many",true);assert(freed==2&&puts_count==3&&!refs);
 data.acl_entrycount=129;a03_probe_stat("/private/var/invalid",true);assert(freed==3&&puts_count==4&&!refs);
 get_error=5;a03_probe_stat("/private/var/error",true);assert(freed==4&&puts_count==5&&!refs);get_error=0;
 partial=true;acl_return=NULL;a03_probe_stat("/private/var/unsupported",true);assert(freed==4&&puts_count==6&&!refs);partial=false;
 a03_probe_stat("/private/var/stat",false);assert(freed==4&&puts_count==7&&!refs);
 lookup_error=2;a03_probe_stat("/private/var/missing",true);assert(freed==4&&puts_count==7&&!refs);
 a03_probe_stat("/private/var/../etc",true);assert(puts_count==7);
 assert(lookups==8&&gets==7);
 puts("PASS production ACL probe: none/entries/16 cap/invalid count/error cleanup/unsupported/stat path");
}
'''
 p=d/'test.c';p.write_text(prefix+header+source+tests)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-o',str(d/'test')],check=True)
 subprocess.run([str(d/'test')],check=True)
assert 'a03_probe_stat(command+4, true)' in newpatch
