#!/usr/bin/env python3
"""Synthetic symbolication tests; no Apple data required."""
import importlib.util,struct
from pathlib import Path
spec=importlib.util.spec_from_file_location("symbols",Path(__file__).with_name("a03-symbolicate-cache.py"));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
s=m.Symbols.__new__(m.Symbols);s.images=[(0x1000,"/test")];s.entries={};s.symbolfile="symbols";s.localoff=s.nlistoff=0;s.strsize=0
b=bytearray(0x3000)
struct.pack_into("<8I",b,0,0xfeedfacf,0x100000c,0,6,3,168,0,0)
struct.pack_into("<II16sQQQQIIII",b,32,25,72,b"__TEXT",0x1000,0x1000,0,0x1000,5,5,0,0)
struct.pack_into("<II16sQQQQIIII",b,104,25,72,b"__LINKEDIT",0x3000,0x1000,0x2000,0x1000,1,1,0,0)
struct.pack_into("<6I",b,176,2,24,0x2000,3,0x2100,64)
struct.pack_into("<IBBHQ",b,0x2000,1,15,1,0,0x1100)
struct.pack_into("<IBBHQ",b,0x2010,8,15,1,0,0x1120)
struct.pack_into("<IBBHQ",b,0x2020,19,15,1,0,0x1140)
b[0x2100:0x211f]=b"\0_first\0<redacted>\0_after\0".ljust(31,b"\0")
s.read=lambda va,n:bytes(b[va-0x1000:va-0x1000+n])
class Empty:
 def read(self,name,off,n):assert n==0;return b""
s.access=Empty()
r=s.resolve(0x1130);assert r["nearest_exported_symbol"]=="_first" and r["distance_from_exported_symbol"]=="0x30"
assert "error" in s.resolve(0x4000)
struct.pack_into("<I",b,184,0x5000)
try:s.resolve(0x1130)
except ValueError:pass
else:raise AssertionError("bad table bounds accepted")
print("Cache exported-symbol/redacted/bounds/membership PASS")
