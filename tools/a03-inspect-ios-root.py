#!/usr/bin/env python3
"""Inspect required iOS files in an extracted root; never writes or flashes.

This is a file/architecture prerequisite check, not proof of Apple provenance,
complete dependencies, valid signatures, kernel compatibility or runtime boot.
Absolute symlinks resolve within the supplied root, never the host root.
"""
import argparse
import json
import plistlib
import struct
from pathlib import Path


def rooted(root, name):
    todo = name.split('/')
    parts = []
    links = 0
    while todo:
        part = todo.pop(0)
        if part in ('', '.'):
            continue
        if part == '..':
            if not parts:
                raise ValueError('path escapes supplied root')
            parts.pop()
            continue
        candidate = root.joinpath(*parts, part)
        if candidate.is_symlink():
            links += 1
            if links > 40:
                raise ValueError('symlink loop')
            target = str(candidate.readlink())
            if target.startswith('/'):
                parts = []
            todo = target.split('/') + todo
        else:
            parts.append(part)
    result = root.joinpath(*parts)
    if not result.is_file():
        raise ValueError('missing regular file: ' + name)
    return result


def macho(path, kind):
    with path.open('rb') as stream:
        header = stream.read(32)
        if len(header) != 32:
            raise ValueError('truncated Mach-O')
        magic, cpu, sub, ftype, count, size, _, _ = struct.unpack('<8I', header)
        if (magic, cpu, sub & 0xffffff, ftype) != (0xfeedfacf, 0x100000c, 0, kind):
            raise ValueError('requires thin plain arm64 Mach-O of expected type')
        if size > 1048576 or count > size // 8 or 32 + size > path.stat().st_size:
            raise ValueError('invalid load-command bounds')
        commands = stream.read(size)
    offset = 0
    linker = None
    for _ in range(count):
        if offset + 8 > size:
            raise ValueError('truncated load command')
        cmd, length = struct.unpack_from('<II', commands, offset)
        if length < 8 or length % 8 or length > size - offset:
            raise ValueError('invalid load-command length')
        command = commands[offset:offset + length]
        if cmd == 0xe:
            if length < 16:
                raise ValueError('truncated dynamic linker command')
            start, = struct.unpack_from('<I', command, 8)
            if not 12 <= start < length or bytes([0]) not in command[start:]:
                raise ValueError('invalid dynamic linker path')
            linker = command[start:].split(bytes([0]), 1)[0].decode()
        offset += length
    if offset != size:
        raise ValueError('load-command count/size mismatch')
    if kind == 2 and linker != '/usr/lib/dyld':
        raise ValueError('expected dynamic executable using /usr/lib/dyld; static test init cannot satisfy this')
    if not path.stat().st_mode & 0o111:
        raise ValueError('missing executable permission')
    return {'architecture': 'arm64', 'linker': linker, 'uid': path.stat().st_uid}


def inspect(root):
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError('expected extracted or mounted root directory')
    checks = []
    def check(name, action):
        try:
            checks.append({'path': name, 'ok': True, 'details': action(rooted(root, name))})
        except (OSError, ValueError, struct.error, plistlib.InvalidFileException) as error:
            checks.append({'path': name, 'ok': False, 'error': str(error)})
    for name, kind in [('/sbin/launchd', 2), ('/usr/lib/dyld', 7),
                       ('/System/Library/CoreServices/SpringBoard.app/SpringBoard', 2)]:
        check(name, lambda p, kind=kind: macho(p, kind))
    def version(path):
        with path.open('rb') as stream:
            data = plistlib.load(stream)
        if not isinstance(data, dict) or any(not isinstance(data.get(k), str) for k in ('ProductVersion', 'ProductBuildVersion')):
            raise ValueError('missing system version/build strings')
        return {k: data[k] for k in ('ProductVersion', 'ProductBuildVersion')}
    check('/System/Library/CoreServices/SystemVersion.plist', version)
    def jobs(path):
        with path.open('rb') as stream:
            data = plistlib.load(stream)
        if not isinstance(data, dict) or not isinstance(data.get('LaunchDaemons'), dict) or not data['LaunchDaemons']:
            raise ValueError('missing launch daemon job dictionary')
        return {'jobs': len(data['LaunchDaemons'])}
    check('/System/Library/xpc/launchd.plist', jobs)
    def cache(path):
        with path.open('rb') as stream:
            header = stream.read(16)
        if header.rstrip(bytes([0]) + b' ') != b'dyld_v1   arm64':
            raise ValueError('requires plain arm64 shared cache header')
        return {'bytes': path.stat().st_size, 'scope': 'primary header only; subcache/dependency completeness unverified'}
    check('/System/Library/Caches/com.apple.dyld/dyld_shared_cache_arm64', cache)
    return {'root': str(root), 'prerequisites_ok': all(c['ok'] for c in checks), 'checks': checks,
            'scope': 'File prerequisites only; no Apple provenance, signature, subcache, entitlement or runtime validation.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    try:
        result = inspect(args.root)
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + chr(10))
    print(json.dumps(result, indent=2))
    return 0 if result['prerequisites_ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
