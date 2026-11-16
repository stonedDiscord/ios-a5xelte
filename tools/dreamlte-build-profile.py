#!/usr/bin/env python3
"""Stage a conservative S8 patch profile from the pinned HEROLTE baseline.

Uses HEROLTE's build configuration through patch 0203. Later S7 UFS, GPU,
PMIC, clock and display programming are excluded. Early framebuffer writes
are redirected into unused low RAM, NOT the unverified physical display.
The profile is for kernel bring-up, not iOS 12/A8 userland compatibility.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('destination',type=Path)
a=p.parse_args()
if a.destination.exists():
    p.error('destination exists; refusing to mix patch profiles')
root=Path(__file__).resolve().parent.parent
patches=sorted(p for p in (root/'xnu/patches').glob('*.patch') if int(p.name[:4])<=203)
if len(patches) != 126 or not patches[-1].name.startswith('0203-'):
    p.error('HEROLTE baseline must end at 0203')
overlays=sorted((root/'xnu/dreamlte').glob('*.patch'))
if [p.name for p in overlays[:2]] != [
        '0204-dreamlte-early-board.patch',
        '0205-dreamlte-a03-portable-bringup.patch']:
    p.error('required DREAMLTE board and portable overlays are missing')
a.destination.mkdir(parents=True)
for source in patches:
    shutil.copy2(source,a.destination/source.name)
for source in (root/'xnu/patches').glob('*.sh'):
    shutil.copy2(source,a.destination/source.name)
for source in overlays:
    shutil.copy2(source,a.destination/source.name)
(a.destination/'DREAMLTE-PROFILE.json').write_text(json.dumps({
    'board': 'dreamlte', 'machine_config': 'HEROLTE', 'page_size': 4096,
    'donor': 'ff2c55e19f1a66fb811ed85bd17a21de9fc727bf through 0203',
    'a03_reference': 'f1e16010e5a1b7d94657a867158a81bad0788682',
    'files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(a.destination.iterdir())},
}, indent=2)+'\n')
print(len(patches)+len(overlays),'patches staged; MACHINE_CONFIG=HEROLTE; single-core S8 bring-up')
