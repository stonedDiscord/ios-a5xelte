#!/usr/bin/env python3
"""Stage a conservative S8 patch profile from the pinned HEROLTE baseline.

Uses HEROLTE's build configuration through patch 0203. Later S7 UFS, GPU,
PMIC, clock and display programming are excluded. Early framebuffer writes
are redirected into unused low RAM, NOT the unverified physical display.
The profile is for kernel bring-up, not iOS 12/A8 userland compatibility.
"""
import argparse
from pathlib import Path
import shutil

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('destination',type=Path)
a=p.parse_args()
if a.destination.exists():
    p.error('destination exists; refusing to mix patch profiles')
root=Path(__file__).resolve().parent.parent
patches=sorted(p for p in (root/'xnu/patches').glob('*.patch') if int(p.name[:4])<=203)
if not patches or not patches[-1].name.startswith('0203-'):
    p.error('HEROLTE baseline must end at 0203')
a.destination.mkdir(parents=True)
for source in patches:
    shutil.copy2(source,a.destination/source.name)
for source in (root/'xnu/patches').glob('*.sh'):
    shutil.copy2(source,a.destination/source.name)
shutil.copy2(root/'xnu/dreamlte/0204-dreamlte-early-board.patch',a.destination/'0204-dreamlte-early-board.patch')
print(len(patches)+1,'patches staged; MACHINE_CONFIG=HEROLTE; single-core S8 bring-up')
