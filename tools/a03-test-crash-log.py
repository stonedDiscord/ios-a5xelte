#!/usr/bin/env python3
"""Test actual0108 selection/gating/saturation without a device."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parent.parent
patch=(root/'xnu/a03/0108-a03-bounded-daemon-crash-diagnostics.patch').read_text()
part=patch.split('+++ b/bsd/kern/kern_exit.c',1)[1].split('--- a/osfmk',1)[0]
added='\n'.join(l[1:] for l in part.splitlines() if l.startswith('+'))
a=added.index('static bool\na03_should_log_daemon_crash');b=added.index('\n#endif',a)
source=added[a:b]
# Apply the contextual follow-up before extracting the tested helper.
with tempfile.TemporaryDirectory() as d:
 q=Path(d)/'bsd/kern/kern_exit.c';q.parent.mkdir(parents=True)
 # Preserve original line offsets using the real helper's0108 source layout.
 q.write_text('\n'*1843+source+'\n')
 subprocess.run(['git','apply',str(root/'xnu/a03/0128-a03-analytics-crash-evidence.patch')],cwd=d,check=True)
 subprocess.run(['git','apply',str(root/'xnu/a03/0137-a03-mobileactivation-crash-evidence.patch')],cwd=d,check=True)
 source=q.read_text()
header=r'''
#include <assert.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdatomic.h>
#include <string.h>
#include <signal.h>
#include <stdio.h>
static uint32_t enabled;
static void PE_parse_boot_argn(const char *arg,void *value,unsigned size) {
 assert(!strcmp(arg,"a03crash_log") && size==sizeof(enabled));
 memcpy(value,&enabled,size);
}
'''
tests=r'''
int main(void) {
 const char *names[]={"watchdogd","backboardd","SpringBoard","launchd","xpcproxy",
 "bluetoothd","identityservices","fairplayd.H2","mediaserverd","configd","lockdownd","analyticsd","dmd","tccd","mobileactivation"};
 assert(!a03_should_log_daemon_crash("mediaserverd",SIGABRT));
 enabled=2;assert(!a03_should_log_daemon_crash("mediaserverd",SIGABRT));enabled=1;
 assert(!a03_should_log_daemon_crash("unknown",SIGABRT));
 assert(!a03_should_log_daemon_crash("watchdogd",SIGTERM));
 for(unsigned i=0;i<sizeof(names)/sizeof(names[0]);i++) {
  assert(strlen(names[i])<=16);
  assert(a03_should_log_daemon_crash(names[i],SIGABRT));
  assert(a03_should_log_daemon_crash(names[i],SIGSEGV));
  for(unsigned j=0;j<10000;j++)assert(!a03_should_log_daemon_crash(names[i],SIGTRAP));
 }
 assert(!a03_should_log_daemon_crash("fairplayd",SIGKILL));
 puts("A03 crash log actual-source boot gate/name selection/two-report saturation PASS");
}
'''
with tempfile.TemporaryDirectory(prefix='a03-crash-test-') as d:
 p=Path(d)/'test.c';p.write_text(header+source+tests)
 subprocess.run(['clang','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-o',d+'/test'],check=True)
 subprocess.run([d+'/test'],check=True)
