#!/usr/bin/env python3
"""Build a returning pre-Linux probe in the exact verified A03 Magisk BOOT.

Host-only. Preserves ramdisk and DT table bytes; AVB signatures
become stale, as with the supplied Magisk image. Requires unlocked device.
"""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import tempfile
import shutil

BASE_SHA256 = '94fa7c5347b00e49fe1dc60a4edae958ddd5dac9accdbcddbeb743b5215e9ce7'
ROOT = Path(__file__).resolve().parent.parent


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('base', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--mmu16k', action='store_true', help='test EL1 and a 16K mapping before Linux')
    p.add_argument('--elf', type=Path, help='keep linked diagnostic ELF in a private output directory')
    a = p.parse_args()
    b = a.base.read_bytes()
    if hashlib.sha256(b).hexdigest() != BASE_SHA256:
        p.error('requires exact verified A035GXXS5CXA1 Magisk base')
    if a.output.exists():
        p.error('output exists; choose another private path')
    if a.elf and a.elf.exists():
        p.error('ELF output exists')
    ks, _, rs, _, ss, _, _, page, version = struct.unpack_from('<9I', b, 8)
    assert b[:8] == b'ANDROID!' and version == 2 and page == 2048 and not ss
    kernel = b[page:page+ks]
    assert kernel[56:60] == b'ARMd'
    insn, = struct.unpack_from('<I', kernel)
    assert insn & 0xfc000000 == 0x14000000
    entry = (insn & 0x3ffffff)*4
    assert entry == 0x1200000
    # Append beyond the original file (including its relocation data), within
    # declared kernel BSS. Linux clears BSS only after our return.
    probe_off = (ks+15)&~15
    with tempfile.TemporaryDirectory(prefix='a03-probe-') as tmp:
        t = Path(tmp)
        names=['boot-entry.S','boot-probe.c']
        if a.mmu16k:
            names += ['mmu16k.S','mmu16k.c']
        for name in names:
            subprocess.run(['clang','--target=aarch64-none-elf','-march=armv8-a',
                '-O2','-ffreestanding','-fno-builtin','-fno-stack-protector',
                '-mgeneral-regs-only','-mstrict-align','-fno-pic',
                '-Wall','-Wextra','-Werror',*(['-DA03_MMU16K'] if a.mmu16k else []),
                '-c',str(ROOT/'shim/a03'/name),
                '-o',str(t/(name+'.o'))],check=True)
        (t/'probe.ld').write_text('ENTRY(a03_boot_probe_entry) SECTIONS { . = '+
            str(probe_off)+'; .entry : { *(.text.entry) } '+
            '.text : { *(.text*) *(.rodata*) } '+
            'a03_probe_end = .; '+
            '/DISCARD/ : { *(.comment) *(.note*) *(.eh_frame*) } }')
        subprocess.run(['ld.lld','-T',str(t/'probe.ld'),
            '--defsym=original_entry='+str(entry),*[str(t/(n+'.o')) for n in names],
            '-o',str(t/'probe.elf')],check=True)
        subprocess.run(['llvm-objcopy','-O','binary',str(t/'probe.elf'),
                        str(t/'probe.bin')],check=True)
        probe = (t/'probe.bin').read_bytes()
        if a.elf:
            a.elf.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(t/'probe.elf',a.elf)
    image_size,=struct.unpack_from('<Q',kernel,16)
    assert len(probe)<0x20000 and probe_off+len(probe)<image_size
    newkernel=bytearray(kernel+bytes(probe_off-ks)+probe)
    struct.pack_into('<I',newkernel,0,0x14000000 | (probe_off//4))
    # Android v2 ID covers kernel/ramdisk/second/recovery_dtbo/dtb.
    align=lambda n:(n+page-1)//page*page
    ro=page+align(ks)
    rds,rdo=struct.unpack_from('<IQ',b,1632)
    ds,=struct.unpack_from('<I',b,1648)
    assert rds==0 and rdo==0
    dt=ro+align(rs)
    ramdisk=b[ro:ro+rs];dtb=b[dt:dt+ds]
    out=bytearray(b[:page])
    struct.pack_into('<I',out,8,len(newkernel))
    digest=hashlib.sha1()
    for part in (newkernel,ramdisk,b'',b'',dtb):
        digest.update(part);digest.update(struct.pack('<I',len(part)))
    out[576:608]=digest.digest()+bytes(12)
    for part in (newkernel,ramdisk,dtb):
        out.extend(part);out.extend(bytes(align(len(part))-len(part)))
    out.extend(b'SEANDROIDENFORCE'+bytes(1))
    original_size=len(out)
    # Retain the supplied stale AVB block at a new aligned offset. Unlocked
    # firmware already accepted its stale boot signature with Magisk.
    footer=struct.unpack_from('>4sIIQQQ',b,len(b)-64)
    _,major,minor,_,vb_off,vb_size=footer
    out.extend(bytes((-len(out))%4096));new_vb_off=len(out)
    out.extend(b[vb_off:vb_off+vb_size])
    assert len(out)<=len(b)-64
    out.extend(bytes(len(b)-64-len(out)))
    out.extend(struct.pack('>4sIIQQQ',b'AVBf',major,minor,original_size,new_vb_off,vb_size)+bytes(28))
    new_ro=page+align(len(newkernel));new_dt=new_ro+align(rs)
    assert out[new_ro:new_ro+rs]==ramdisk and out[new_dt:new_dt+ds]==dtb
    assert newkernel[4:ks]==kernel[4:] and len(out)==len(b)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(out)
    print('probe offset',hex(probe_off),'bytes',len(probe),'original entry',hex(entry))
    print('SHA256',hashlib.sha256(out).hexdigest())
    print('Host candidate only; ramdisk/DT bytes unchanged; AVB signature stale.')


if __name__=='__main__':
    main()
