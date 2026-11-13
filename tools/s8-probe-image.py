#!/usr/bin/env python3
"""Insert a pre-Linux CPU probe into a backed-up legacy Samsung BOOT image.

No XNU yet: the probe records MMFR0 in the FDT bootargs and then enters the
unchanged Android kernel. Original ramdisk and Samsung DTBH are preserved.
The appended probe occupies Linux BSS only before Linux initializes it.
"""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import tempfile

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('original', type=Path)
p.add_argument('output', type=Path)
a = p.parse_args()
b = a.original.read_bytes()
if b[:8] != b'ANDROID!':
    p.error('not an Android boot image')
h = struct.unpack_from('<10I', b, 8)
ks, _, rs, _, ss, _, _, page, ds, _ = h
if page != 2048 or ss or not ds or ds > 1048576:
    p.error('expected S8 legacy Samsung layout, not a v1/v2 header')
def align(n, size=page):
    return (n+size-1)//size*size
ko = page
ro = ko+align(ks)
do = ro+align(rs)
kernel = b[ko:ko+ks]
ramdisk = b[ro:ro+rs]
dtb = b[do:do+ds]
if len(dtb) != ds or dtb[:4] != b'DTBH' or kernel[56:60] != b'ARMd':
    p.error('missing Samsung DTBH or ARM64 Image header')
insn, = struct.unpack_from('<I', kernel)
if insn & 0xfc000000 != 0x14000000:
    p.error('kernel entry must be an unconditional B')
imm = insn & 0x3ffffff
entry = (imm - (1<<26) if imm & (1<<25) else imm)*4
if not 64 <= entry < ks:
    p.error('original entry is outside kernel')
probe_off = align(ks,16)
root = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix='s8-probe-') as tmp:
    t = Path(tmp)
    for name in ('probe.S','probe.c'):
        subprocess.run(['clang','--target=aarch64-none-elf','-O2',
                        '-ffreestanding','-fno-builtin','-fno-stack-protector',
                        '-mgeneral-regs-only','-mstrict-align','-fno-pic',
                        '-Wall','-Wextra','-Werror','-c',
                        str(root/'shim/s8'/name),'-o',str(t/(name+'.o'))],check=True)
    (t/'probe.ld').write_text('ENTRY(s8_probe_entry) SECTIONS { . = '+str(probe_off)+
        '; .text : { *(.text.entry) *(.text*) *(.rodata*) } '
        '/DISCARD/ : { *(.comment) *(.note*) *(.eh_frame*) } }')
    subprocess.run(['ld.lld','-T',str(t/'probe.ld'),
                    '--defsym=original_entry='+str(entry),
                    str(t/'probe.S.o'),str(t/'probe.c.o'),'-o',str(t/'probe.elf')],check=True)
    subprocess.run(['llvm-objcopy','-O','binary',str(t/'probe.elf'),str(t/'probe.bin')],check=True)
    probe = (t/'probe.bin').read_bytes()
newkernel = bytearray(kernel + bytes(probe_off-ks) + probe)
struct.pack_into('<I',newkernel,0,0x14000000 | (probe_off//4))
image_size, = struct.unpack_from('<Q',kernel,16)
if len(newkernel) > image_size:
    p.error('probe exceeds kernel declared memory size')
header = bytearray(b[:page])
struct.pack_into('<I',header,8,len(newkernel))
# Android legacy boot ID: kernel, ramdisk, second; Samsung also includes DT.
sha = hashlib.sha1()
for data in (newkernel,ramdisk,b'',dtb):
    sha.update(data)
    sha.update(struct.pack('<I',len(data)))
header[576:608] = sha.digest()+bytes(12)
out = bytearray(header)
for data in (newkernel,ramdisk,dtb):
    out.extend(data)
    out.extend(bytes(align(len(data))-len(data)))
out.extend(b'SEANDROIDENFORCE')
if len(out)>len(b):
    p.error('new image exceeds original partition size')
out.extend(bytes(len(b)-len(out)))
nro = page+align(len(newkernel))
ndo = nro+align(rs)
assert out[nro:nro+rs] == ramdisk
assert out[ndo:ndo+ds] == dtb
assert newkernel[4:ks] == kernel[4:]
assert len(out) == len(b)
a.output.parent.mkdir(parents=True,exist_ok=True)
a.output.write_bytes(out)
print('Original entry:',hex(entry),'probe:',hex(probe_off),'bytes:',len(probe))
print('Preserved original kernel except first B; ramdisk and DTBH identical.')
print('SHA256',hashlib.sha256(out).hexdigest(),a.output)
