#!/usr/bin/env python3
"""Emit a userspace HFS importer manifest from three read-only APFS mounts.

Usage: dreamlte-root-manifest.py MOUNT_ROOT GENERATED_FILES > manifest.bin
Copies hard links as independent files. Extended attributes, BSD flags and
timestamps are not preserved. Does not open a phone or flash an image.
"""
import os
from pathlib import Path
import stat
import sys
import re
import unicodedata

mounts, generated = map(Path, sys.argv[1:])
generated.mkdir(parents=True, exist_ok=True)
entries = {}
written = set()

def hfs_name(path):
    # HFS+ uses Unicode3.2 decomposition with these explicit exclusions.
    parts = re.split('([\u2000-\u2fff\uf900-\ufaff\U0002f800-\U0002faff])', path)
    return ''.join(part if i % 2 else unicodedata.ucd_3_2_0.normalize('NFD', part)
                   for i, part in enumerate(parts))

def emit(kind, dest, source='', mode=0o40755, uid=0, gid=0):
    if dest in entries:
        raise RuntimeError(f'duplicate destination: {dest}')
    normalized = hfs_name(dest)
    if normalized in written and kind != 'd':
        raise RuntimeError(f'HFS normalization collision: {dest}')
    written.add(normalized)
    entries[dest] = (kind, source, mode, uid, gid)
    for value in (kind, normalized, source, oct(mode)[2:], str(uid), str(gid)):
        sys.stdout.buffer.write(os.fsencode(value) + b'\0')

def parents(dest):
    parent = str(Path(dest).parent)
    if parent != dest and parent not in entries:
        parents(parent)
        emit('d', parent)

def copy(src, dest, missing_only=False):
    if missing_only and dest in entries and entries[dest][0] != 'd':
        return  # Existing symlink/file supplies this cryptex subtree.
    s = src.lstat()
    kind = 'd' if stat.S_ISDIR(s.st_mode) else 'l' if stat.S_ISLNK(s.st_mode) else 'f' if stat.S_ISREG(s.st_mode) else None
    if not kind:
        raise RuntimeError(f'unsupported source type: {src}')
    if dest not in entries:
        parents(dest)
        emit(kind, dest, os.readlink(src) if kind == 'l' else str(src.resolve()) if kind == 'f' else '', s.st_mode, s.st_uid, s.st_gid)
    elif not missing_only:
        raise RuntimeError(f'overlapping source: {dest}')
    if kind == 'd':
        for child in sorted(src.iterdir()):
            copy(child, dest.rstrip('/') + '/' + child.name, missing_only)

copy(mounts / 'os/root', '/')
for name, label in [('sysos', 'OS'), ('appos', 'App')]:
    dest = '/private/preboot/Cryptexes/' + label
    parents(dest)
    copy(mounts / name / 'root', dest)

# dyld's ignition-level-1 search paths need cryptex content in the OS tree.
# Materialize copies, avoiding unsupported HFS hard-link bookkeeping.
for name in ('sysos', 'appos'):
    copy(mounts / name / 'root', '/', missing_only=True)

def directory(dest, mode, uid=0, gid=0):
    parents(dest)
    # Metadata override for an already imported directory is intentional.
    if dest in entries:
        if entries[dest][0] != 'd':
            raise RuntimeError(f'expected directory: {dest}')
        del entries[dest]
    emit('d', dest, mode=stat.S_IFDIR | mode, uid=uid, gid=gid)

def file(dest, data, mode, uid=0, gid=0):
    parents(dest)
    source = generated / str(len(entries))
    source.write_bytes(data)
    emit('f', dest, str(source.resolve()), stat.S_IFREG | mode, uid, gid)

for dest, mode in [('diagnostics', 0o751), ('uuidtext', 0o755), ('diagnostics/timesync', 0o755)]:
    path = '/private/var/db/' + dest
    directory(path, mode, 272, 272)
    file(path + '/.migrated', b'', 0o644, 272, 272)
directory('/private/var/keybags', 0o700)
file('/private/var/keybags/systembag.kb', b'<?xml version="1.0" encoding="UTF-8"?>\n<plist version="1.0"><dict><key>KeyBagKeys</key><data>U1dFRVQ=</data></dict></plist>\n', 0o600)
print(f'{len(entries)} destinations', file=sys.stderr)
