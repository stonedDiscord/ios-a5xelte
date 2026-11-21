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


def stage(root):
    directory = root / 'Library/Wallpaper'
    alias(directory / 'Collections', 'Collections.plist', 'Collections~iphone.plist')
    alias(directory, 'DefaultWallpapers~ipod.plist', 'DefaultWallpapers~iphone.plist', True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    stage(parser.parse_args().root)
