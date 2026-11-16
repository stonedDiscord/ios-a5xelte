#!/usr/bin/env python3
"""Evaluate captured A03 container ACEs with the actual XNU ACL evaluator.

Pass an extracted XNU root. Credential membership is controlled test input;
this verifies UUID conversion does not itself grant group membership.
"""
from pathlib import Path
import subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
if len(sys.argv)!=2:raise SystemExit('usage: a03-test-identity-acl.py XNU_SOURCE')
xnu=Path(sys.argv[1]);s=(xnu/'bsd/kern/kern_authorization.c').read_text()
a=s.index('int\nkauth_acl_evaluate(');b=s.index('\n/*\n * Perform ACL inheritance',a);evaluator=s[a:b]
p=(root/'xnu/a03/0142-a03-opt-in-local-identity-uuid.patch').read_text();p='\n'.join(l[1:] for l in p.splitlines() if l.startswith('+') and not l.startswith('+++'));a=p.index('static int\na03_compat_id_uuid(');b=p.index('\n#endif',a);helper=p[a:b]
header=r'''
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <arpa/inet.h>
typedef uint32_t id_t;typedef struct{uint8_t b[16];}guid_t;
typedef struct cred {id_t uid;bool group299;} *kauth_cred_t;
#define KAUTH_DEBUG(...) ((void)0)
#define KAUTH_WKG_NOT 0
#define KAUTH_WKG_OWNER 1
#define KAUTH_WKG_GROUP 2
#define KAUTH_WKG_NOBODY 3
#define KAUTH_WKG_EVERYBODY 4
#define KAUTH_AEVAL_IS_OWNER 1
#define KAUTH_AEVAL_IN_GROUP 2
#define KAUTH_AEVAL_IN_GROUP_UNKNOWN 4
#define KAUTH_ACE_KINDMASK 15
#define KAUTH_ACE_PERMIT 1
#define KAUTH_ACE_DENY 2
#define KAUTH_ACE_ONLY_INHERIT 256
#define KAUTH_ACE_GENERIC_ALL (1<<21)
#define KAUTH_ACE_GENERIC_EXECUTE (1<<22)
#define KAUTH_ACE_GENERIC_WRITE (1<<23)
#define KAUTH_ACE_GENERIC_READ (1<<24)
#define KAUTH_RESULT_ALLOW 1
#define KAUTH_RESULT_DENY 2
#define KAUTH_RESULT_DEFER 3
#define TRUE 1
#define FALSE 0
struct kauth_ace {guid_t ace_applicable;unsigned ace_flags,ace_rights;};
typedef struct kauth_ace *kauth_ace_t;
typedef struct kauth_acl_eval {kauth_ace_t ae_acl;int ae_count;unsigned ae_requested,ae_residual;int ae_result,ae_found_deny,ae_options;unsigned ae_exp_gall,ae_exp_gread,ae_exp_gwrite,ae_exp_gexec;} *kauth_acl_eval_t;
static unsigned a03_compat_uuid;
'''
wrappers=r'''
static int kauth_cred_getguid(kauth_cred_t c,guid_t *g){bool handled;int e=a03_compat_id_uuid(false,true,&c->uid,g,&handled);return handled?e:EWOULDBLOCK;}
static int kauth_wellknown_guid(guid_t *g){(void)g;return KAUTH_WKG_NOT;}
static int kauth_guid_equal(guid_t *a,guid_t *b){return !memcmp(a,b,16);}
static int kauth_cred_ismember_guid(kauth_cred_t c,guid_t *g,int *yes){bool handled;id_t id;int e=a03_compat_id_uuid(true,false,&id,g,&handled);if(!handled)return EWOULDBLOCK;if(e)return e;*yes=id==299&&c->group299;return 0;}
'''
test=r'''
static int check(struct cred *c,struct kauth_ace *aces,unsigned count,unsigned rights){struct kauth_acl_eval e={.ae_acl=aces,.ae_count=count,.ae_requested=rights};assert(!kauth_acl_evaluate(c,&e));return e.ae_result;}
int main(void){struct cred analytics={263,true},mobile={501,true},other={502,false};
struct kauth_ace root_aces[2]={{{{0xab,0xcd,0xef,0xab,0xcd,0xef,0xab,0xcd,0xef,0xab,0xcd,0xef,0,0,1,0x2b}},0x161,0x3ffe},{{{0xab,0xcd,0xef,0xab,0xcd,0xef,0xab,0xcd,0xef,0xab,0xcd,0xef,0,0,1,0x2b}},1,0x624}};
struct kauth_ace library=root_aces[0];library.ace_flags=0x71;
assert(check(&analytics,&library,1,2)==KAUTH_RESULT_DEFER);
a03_compat_uuid=1;
assert(check(&analytics,&library,1,2)==KAUTH_RESULT_ALLOW);
assert(check(&other,&library,1,2)==KAUTH_RESULT_DEFER);
assert(check(&mobile,root_aces,2,0x400)==KAUTH_RESULT_ALLOW);
assert(check(&other,root_aces,2,0x400)==KAUTH_RESULT_DEFER);
assert(check(&mobile,root_aces,2,0x80000000)==KAUTH_RESULT_DEFER);
library.ace_flags=2;assert(check(&analytics,&library,1,2)==KAUTH_RESULT_DENY);
puts("PASS actual XNU ACL evaluator: captured group299 grant works only for supplied members; unrelated users/rights denied or deferred");}
'''
with tempfile.TemporaryDirectory(prefix='a03-identity-acl-') as d:
 p=Path(d)/'test.c';p.write_text(header+helper+wrappers+evaluator+test)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
