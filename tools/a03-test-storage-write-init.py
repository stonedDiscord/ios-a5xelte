#!/usr/bin/env python3
"""Emulate actual opt-in write diagnostic; inject failures and verify restoration."""
import struct,sys
from unicorn import Uc,UC_ARCH_ARM64,UC_MODE_ARM,UC_HOOK_INTR
from unicorn.arm64_const import *
image=open(sys.argv[1],'rb').read();base=0x100000000
original=bytes(range(256))*2

def run(fault=None,short=False,mismatch=False):
 u=Uc(UC_ARCH_ARM64,UC_MODE_ARM);u.mem_map(base,0x10000);u.mem_write(base,image)
 u.mem_map(0x200000000,0x10000);u.reg_write(UC_ARM64_REG_SP,0x20000fff0)
 disk=original;out=[];io=0;writes=[]
 def hook(u,n,data):
  nonlocal disk,io
  call=u.reg_read(UC_ARM64_REG_X16)
  a=[u.reg_read(r) for r in (UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3)]
  err=False;r=0
  if call==5:
   path=bytes(u.mem_read(a[0],80)).split(b'\0')[0].decode()
   if path=='/dev/console':r=3
   elif path=='/dev/ra03boot0' and a[1]==1:err=True;r=30
   elif path in ('/dev/ra03boot0','/dev/a03boot0'):r=4
   elif path=='/dev/ra03userdata0':
    if fault=='open':err=True;r=5
    else:r=7
   else:raise AssertionError(path)
  elif call==3:
   assert a[0]==4
   data=bytearray(512);data[:8]=b'ANDROID!';struct.pack_into('<II',data,36,2048,2)
   u.mem_write(a[1],bytes(data));r=512
  elif call in (153,154):
   assert a[0]==7 and a[2:]==[512,16<<30],a
   io+=1;r=512
   if fault==io:
    if short:r=256
    else:err=True;r=5
   elif call==153:
    data=disk
    if mismatch and io==3:data=bytes([disk[0]^1])+disk[1:]
    u.mem_write(a[1],data)
   else:
    disk=bytes(u.mem_read(a[1],512));writes.append(disk)
  elif call==95:
   assert a[0]==7
   if fault=='fsync':err=True;r=5
  elif call==4:
   assert a[0]==3,'unexpected non-console write'
   out.append(bytes(u.mem_read(a[1],a[2])).decode());r=a[2]
  elif call==20:r=1
  elif call==93:u.emu_stop();return
  elif call!=6:raise AssertionError(call)
  u.reg_write(UC_ARM64_REG_X0,r)
  flags=u.reg_read(UC_ARM64_REG_NZCV)
  u.reg_write(UC_ARM64_REG_NZCV,(flags&~(1<<29))|((1<<29) if err else 0))
 u.hook_add(UC_HOOK_INTR,hook);u.emu_start(base+0x400,base+0x4000,count=300000)
 text=''.join(out)
 if fault is None and not mismatch:
  assert 'A03 USERDATA WRITE PASS:' in text,text
  assert writes==[bytes(x^0xa5 for x in original),original]
 else:
  assert 'A03 USERDATA WRITE FAIL' in text and 'A03 USERDATA WRITE PASS:' not in text,text
 if fault!=4:assert disk==original,'original sector not restored'
 return text
print(run())
for fault in ['open',1,2,3,4,5,'fsync']:run(fault)
for fault in range(1,6):run(fault,short=True)
run(mismatch=True)
print('PASS actual ARM64 write test: exact USERDATA offset, saved/changed/readback/restored; error/short/mismatch paths')
