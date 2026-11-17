#!/usr/bin/env python3
"""Verify the exact DREAMLTE sources and linked code before a BOOT trial.

Usage: dreamlte-verify-ci.py KERNEL_ARTIFACT_DIR BUILDTREE_TGZ
This is a build-content check, not evidence of working hardware.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('kernel_dir', type=Path)
p.add_argument('buildtree', type=Path)
a = p.parse_args()
root = Path(__file__).resolve().parent.parent
expected = json.loads((root / 'tools/dreamlte-ci-source-hashes.json').read_text())
kernel = a.kernel_dir / 'kernel.development.herolte'
checksum = hashlib.sha256(kernel.read_bytes()).hexdigest()
checks = (a.kernel_dir / 'SHA256SUMS').read_text().splitlines()
assert f'{checksum}  {kernel.name}' in checks, 'kernel artifact checksum mismatch'
profile = json.loads((a.kernel_dir / 'DREAMLTE-PROFILE.json').read_text())
assert profile['board'] == 'dreamlte' and profile['page_size'] == 4096
for patch in sorted((root / 'xnu/dreamlte').glob('*.patch')):
    assert profile['files'].get(patch.name) == hashlib.sha256(patch.read_bytes()).hexdigest(), \
        f'profile differs from reviewed overlay: {patch.name}'
with tarfile.open(a.buildtree) as archive:
    for name, digest in expected['sources'].items():
        data = archive.extractfile('xnu/' + name).read()
        assert hashlib.sha256(data).hexdigest() == digest, f'compiled source mismatch: {name}'
symbols = subprocess.check_output(['llvm-nm', str(kernel)], text=True)
names = {line.split()[-1] for line in symbols.splitlines() if line.split()}
for symbol in expected['symbols']:
    assert symbol in names, f'linked symbol missing: {symbol}'
print(json.dumps({'build_content': 'PASS', 'kernel_sha256': checksum,
                  'source_files': len(expected['sources']),
                  'linked_symbols': len(expected['symbols']),
                  'runtime': 'not tested'}, indent=2))
