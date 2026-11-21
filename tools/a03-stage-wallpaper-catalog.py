#!/usr/bin/env python3
"""Supply WallpaperKit's generic catalog path in a staged A03 root."""
import argparse
from pathlib import Path
import plistlib


def check(path, defaults=False):
    with path.open('rb') as stream:
        plist = plistlib.load(stream)
    if defaults:
        value = plist.get('default') if isinstance(plist, dict) else None
        if not isinstance(value, dict) or not isinstance(value.get('wallpaperIdentifier'), int) or not value.get('collectionIdentifier'):
            raise ValueError(f'{path} has no valid default wallpaper')
        return
    order = plist.get('order') if isinstance(plist, dict) else None
    if not isinstance(order, list) or not order or not all(
            isinstance(item, str) and item for item in order):
        raise ValueError(f'{path} has no valid wallpaper order')


def alias(directory, name, target, defaults=False):
    catalog = directory / name
    if catalog.exists() or catalog.is_symlink():
        check(catalog, defaults)
        return
    source = directory / target
    check(source, defaults)
    catalog.symlink_to(source.name)
    check(catalog, defaults)


def stage_poster_extension_point(root):
    identifier = 'com.apple.posterkit.provider'
    framework = '/System/Library/PrivateFrameworks/PosterKit.framework'
    cache = root / 'System/Library/xpc/extensions.plist'
    definition = plistlib.loads(cache.read_bytes())[identifier][framework]
    configuration = definition['EXExtensionPointConfiguration']
    if (definition['NSExtension']['NSExtensionPointIdentifier'] != identifier
            or configuration['EXExtensionPointIsPublic'] is not False
            or configuration['EXRequiredEntitlements'].get(
                'com.apple.runningboard.posterkit.host') is not True):
        raise ValueError('unexpected PosterKit extension point policy')

    directory = root / 'System/Library/ExtensionKit/ExtensionPoints'
    path = directory / f'{identifier}.appexpt'
    record = {identifier: dict(definition['NSExtension'], **configuration)}
    try:
        with path.open('xb') as stream:
            plistlib.dump(record, stream)
    except FileExistsError:
        if plistlib.loads(path.read_bytes()) != record:
            raise ValueError(f'{path} differs from the stock definition')


def stage(root):
    stage_poster_extension_point(root)
    directory = root / 'Library/Wallpaper'
    alias(directory / 'Collections', 'Collections.plist', 'Collections~iphone.plist')
    alias(directory, 'DefaultWallpapers~ipod.plist', 'DefaultWallpapers~iphone.plist', True)
    metadata = directory / 'Collections/iOS_16~iphone.wallpaperCollection/Wallpapers/7400.WWDC_2022-375w-812h@3x~iphone.wallpaper/Wallpaper.plist'
    data = metadata.read_bytes()
    plist = plistlib.loads(data)
    if plist.get('logicalScreenClass') == '375w-812h@3x~iphone':
        original = b'\x5f\x10\x13375w-812h@3x~iphone'
        if len(data) != 536 or data[425:447] != original:
            raise ValueError('unexpected stock wallpaper metadata layout')
        changed = data[:428] + b'240w-533h@3x~iphone' + data[447:]
        expected = dict(plist, logicalScreenClass='240w-533h@3x~iphone')
        if plistlib.loads(changed) != expected:
            raise ValueError('wallpaper metadata edit changed other values')
        metadata.write_bytes(changed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    stage(parser.parse_args().root)
