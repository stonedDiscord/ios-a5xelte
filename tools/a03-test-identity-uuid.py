from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1]
patch=(root/'xnu/a03/0142-a03-opt-in-local-identity-uuid.patch').read_text()
s='\n'.join(l[1:] for l in patch.splitlines() if l.startswith('+') and not l.startswith('+++'))
start=s.index('static int\na03_compat_id_uuid(');end=s.index('\n#endif',start);src=s[start:end]
pre=r'''
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>
#include <errno.h>
#include <arpa/inet.h>
typedef uint32_t id_t;typedef struct {uint8_t bytes[16];} guid_t;
static unsigned a03_compat_uuid;
'''
test=r'''
int main(void){bool handled;guid_t g;uint32_t id=501,out=0x12345678;memset(&g,0x11,sizeof(g));
assert(!a03_compat_id_uuid(false,true,&id,&g,&handled)&&!handled&&g.bytes[0]==0x11);
a03_compat_uuid=2;assert(!a03_compat_id_uuid(false,true,&id,&g,&handled)&&!handled);
a03_compat_uuid=1;assert(!a03_compat_id_uuid(false,true,&id,&g,&handled)&&handled);
assert(!memcmp(g.bytes,"\xff\xff\xee\xee\xdd\xdd\xcc\xcc\xbb\xbb\xaa\xaa\0\0\1\xf5",16));
assert(!a03_compat_id_uuid(false,false,&out,&g,&handled)&&handled&&out==501);
out=999;assert(a03_compat_id_uuid(true,false,&out,&g,&handled)==ENOENT&&handled&&out==999);
id=299;assert(!a03_compat_id_uuid(true,true,&id,&g,&handled)&&handled);
assert(!memcmp(g.bytes,"\xab\xcd\xef\xab\xcd\xef\xab\xcd\xef\xab\xcd\xef\0\0\1\x2b",16));
assert(!a03_compat_id_uuid(true,false,&out,&g,&handled)&&handled&&out==299);
assert(a03_compat_id_uuid(false,false,&out,&g,&handled)==ENOENT&&handled);
memset(&g,0x44,sizeof(g));out=123;assert(!a03_compat_id_uuid(false,false,&out,&g,&handled)&&!handled&&out==123);
for(unsigned group=0;group<2;group++)for(uint64_t v=0;v<=UINT32_MAX;v=v?UINT32_MAX+1ULL:UINT32_MAX){id=(uint32_t)v;assert(!a03_compat_id_uuid(group,true,&id,&g,&handled)&&handled);assert(!a03_compat_id_uuid(group,false,&out,&g,&handled)&&handled&&out==id);}
puts("PASS actual compat UUID helper: default off/exact optin/UID/GID vectors/roundtrip/type mismatch/unknown UUID/boundary IDs");}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'test.c';p.write_text(pre+src+test);subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-o',d+'/test'],check=True);subprocess.run([d+'/test'],check=True)
