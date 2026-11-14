#!/usr/bin/env python3
# Optional Unicorn test of assembled init with stubbed Darwin syscalls; no device access.
import struct, sys
from unicorn import Uc,UC_ARCH_ARM64,UC_MODE_ARM,UC_HOOK_INTR
from unicorn.arm64_const import *
b=open(sys.argv[1],'rb').read();base=0x100000000
regs=[UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2]
def run(stage=None,value=5):
 u=Uc(UC_ARCH_ARM64,UC_MODE_ARM);u.mem_map(base,0x10000);u.mem_write(base,b);u.mem_map(0x200000000,0x10000);u.reg_write(UC_ARM64_REG_SP,0x20000fff0);out=[];fds={}
 def hook(u,n,data):
  call=u.reg_read(UC_ARM64_REG_X16);a=[u.reg_read(r) for r in regs];err=False;r=0
  if call==5:
   path=bytes(u.mem_read(a[0],80)).split(bytes([0]))[0].decode()
   if path=='/dev/console':r=3
   elif a[1]==1:r=value if stage==0x30 else 6 if stage==0x31 else 30;err=stage!=0x31
   else:
    st=0x10 if path=='/dev/ra03boot0' else 0x20
    if stage==st:r=value;err=True
    else:r=4 if st==0x10 else 5;fds[r]=st
  elif call==3:
   st=fds[a[0]];r=512
   if stage==st+1:r=value;err=True
   elif stage==st+2:r=value
   else:
    data=bytearray(512);data[:8]=b'ANDROID!';struct.pack_into('<II',data,36,2048,2)
    if stage==st+3:struct.pack_into('<Q',data,0,value)
    if stage==st+4:struct.pack_into('<I',data,36,value)
    if stage==st+5:struct.pack_into('<I',data,40,value)
    u.mem_write(a[1],bytes(data))
  elif call==4:
   assert a[0]==3,'storage write attempted';out.append(bytes(u.mem_read(a[1],a[2])).decode());r=a[2]
  elif call==20:r=1
  elif call==93:u.emu_stop();return
  elif call!=6:raise AssertionError(call)
  u.reg_write(UC_ARM64_REG_X0,r);flags=u.reg_read(UC_ARM64_REG_NZCV);u.reg_write(UC_ARM64_REG_NZCV,(flags&~(1<<29))|((1<<29) if err else 0))
 u.hook_add(UC_HOOK_INTR,hook);u.emu_start(base+0x400,base+0x4000,count=200000);s=''.join(out)
 if stage is None:assert 'A03 STORAGE PID1 PASS:' in s,s
 else:assert f'stage=0x{stage:016x}' in s and f'value=0x{(6 if stage==0x31 else value):016x}' in s and 'A03 STORAGE PID1 FAIL:' in s,s
 return s
print(run())
for stage in [*(0x10+i for i in range(6)),*(0x20+i for i in range(6)),0x30,0x31]:run(stage)
print('PASS actual ARM64 instructions: success +14 exact stage/value failures; console-only writes')
