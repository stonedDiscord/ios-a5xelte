#!/usr/bin/env python3
"""Supply WallpaperKit's generic catalog path in a staged A03 root."""
import argparse
from pathlib import Path
import plistlib


def check(path):
    with path.open('rb') as stream:
        plist = plistlib.load(stream)
    order = plist.get('order') if isinstance(plist, dict) else None
    if not isinstance(order, list) or not order or not all(
            isinstance(item, str) and item for item in order):
        raise ValueError(f'{path} has no valid wallpaper order')


def stage(root):
    directory = root / 'Library/Wallpaper/Collections'
    catalog = directory / 'Collections.plist'
    if catalog.exists() or catalog.is_symlink():
        check(catalog)
        return
    source = directory / 'Collections~iphone.plist'
    check(source)
    catalog.symlink_to(source.name)
    check(catalog)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    stage(parser.parse_args().root)
