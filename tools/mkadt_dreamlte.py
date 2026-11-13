#!/usr/bin/env python3
"""Minimal dreamlte ADT for the HEROLTE-derived 4K kernel bring-up.

One verified boot A53; upper 512 MiB RAM window has no live DT reservation.
No UFS, GPU, PMIC, touch, Wi-Fi or framebuffer driver nodes are published.
This is a kernel-only tree, not a configured iOS root or Apple A8 identity.
"""
import argparse
from pathlib import Path
import os
import adt
from mkadt import build as donor_build, cstr, node, u32, u64
from mkadt_herolte import child, set_prop

DRAM_BASE, DRAM_SIZE = 0x880000000, 0x20000000
SOC_BASE = 0x10000000

def build():
    root = donor_build(seed=os.urandom(64), qemu=True)
    set_prop(root, 'compatible', cstr('samsung,a5xelte') +
             cstr('samsung,dreamlte') + cstr('samsung,exynos8895') + cstr('AppleARM'))
    set_prop(root, 'model', cstr('SM-G950F'))
    set_prop(root, 'target-type', cstr('DREAMLTE'))
    set_prop(root, 'target-sub-type', cstr('DREAMLTE'))
    root.children = [n for n in root.children if n.name not in
                     ('sweet-fbcon','sweet-ufs','product','buttons')]
    chosen = child(root,'chosen')
    set_prop(chosen,'dram-base',u64(DRAM_BASE))
    set_prop(chosen,'dram-size',u64(DRAM_SIZE))
    set_prop(chosen,'firmware-version',cstr('dreamlte-entry'))
    set_prop(chosen,'system-firmware-version',cstr('dreamlte-entry'))
    cpus = child(root,'cpus')
    cpu0 = child(cpus,'cpu0')
    cpus.children = [cpu0]
    set_prop(cpu0,'compatible',cstr('arm,cortex-a53')+cstr('ARM,v8'))
    set_prop(cpu0,'reg',u32(0x100))
    for prop in ('timebase-frequency','fixed-frequency','peripheral-frequency'):
        set_prop(cpu0,prop,u32(26000000))
    set_prop(cpu0,'clock-frequency',u32(1690000000))
    arm_io = child(root,'arm-io')
    set_prop(arm_io,'device_type',cstr('dreamlte-io'))
    set_prop(arm_io,'compatible',cstr('samsung,exynos8895-io')+cstr('arm-io'))
    set_prop(arm_io,'ranges',u64(0,SOC_BASE,0xf0000000))
    arm_io.children = [node('gic',[
        ('compatible',cstr('arm,cortex-a15-gic')),
        ('interrupt-controller',cstr('master')),
        ('virtual-timer-intid',u32(27)),
        ('reg',u64(0x10201000-SOC_BASE,0x1000,0x10202000-SOC_BASE,0x1000)),
    ])]
    return root

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    a=p.parse_args()
    blob=adt.serialize(build())
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(blob)
    print(a.output, len(blob),'bytes; kernel-only, single A53, 4K target')
