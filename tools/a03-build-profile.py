#!/usr/bin/env python3
"""Stage pinned native-16K SWEET core for A03 single-core kernel bring-up.

No Qualcomm storage, USB, power, GPU or Wi-Fi patches. No iOS rootfs yet.
"""
import argparse
import hashlib
import io
from pathlib import Path
import shutil
import tarfile
import urllib.request

SHA = '45263bee51df4a0f55cdf9c649af886399488ddb'
ROOT = Path(__file__).resolve().parent.parent
EXTRA_CRYPTO = {20, 23, 27, 32, 33}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('destination', type=Path)
    p.add_argument('--source', type=Path, help='local pinned SWEET source for offline staging')
    a = p.parse_args()
    if a.destination.exists():
        p.error('destination exists')
    if a.source:
        source = a.source
        archive = None
    else:
        data = urllib.request.urlopen('https://codeload.github.com/dipa-studio/ios-sweet/tar.gz/'+SHA).read()
        archive = tarfile.open(fileobj=io.BytesIO(data), mode='r:gz')
        source = None
    a.destination.mkdir(parents=True)
    if source:
        patches = [(x.name, x.read_bytes()) for x in sorted((source/'xnu/patches').glob('*.patch')) if int(x.name[:4])<=18 or int(x.name[:4]) in EXTRA_CRYPTO]
        stage = (source/'xnu/patches/0020-stage-bearssl.sh').read_bytes()
    else:
        patches = [(Path(m.name).name, archive.extractfile(m).read()) for m in archive.getmembers()
                   if '/xnu/patches/' in m.name and m.name.endswith('.patch') and
                   (int(Path(m.name).name[:4])<=18 or int(Path(m.name).name[:4]) in EXTRA_CRYPTO)]
        member = next(m for m in archive.getmembers() if m.name.endswith('/xnu/patches/0020-stage-bearssl.sh'))
        stage = archive.extractfile(member).read()
    if len(patches)!=23:
        raise SystemExit('expected 18 core and 5 portable crypto patches')
    (a.destination/'0020-stage-bearssl.sh').write_bytes(stage)
    changes = {
        '0004-sweet-machine-config.patch': [('SWEET_VTIMER_INTID        19','SWEET_VTIMER_INTID        27')],
        '0010-sweet-early-framebuffer-debug.patch': [
            ('0x9c000000','0x9e000000'),('2368 * 4320','1568 * 2880'),
            ('#4320','#2880'),('1080u','720u'),('2400u','1600u'),('4320u','2880u')],
        '0012-sweet-keep-debug-console-after-ttbr0.patch': [
            ('0x9c000000','0x9e000000'),('1080u','720u'),('2400u','1600u'),('4320u','2880u'),
            ('stage * 48','stage * 32'),('(stage + 1) * 48','(stage + 1) * 32')],
    }
    for name, data in patches:
        text = data.decode()
        for old, new in changes.get(name, []):
            if old not in text:
                raise SystemExit('missing expected replacement '+name+': '+old)
            text = text.replace(old, new)
        (a.destination/name).write_text(text)
    # Current runner iig compatibility; not a board/peripheral patch.
    shutil.copyfile(ROOT/'xnu/patches/0083-xcode27-iig-kernel-content.patch', a.destination/'0083-xcode27-iig-kernel-content.patch')
    shutil.copyfile(ROOT/'xnu/patches/0084-a03-lockdown-polling-checkpoints.patch', a.destination/'0084-a03-lockdown-polling-checkpoints.patch')
    shutil.copyfile(ROOT/'xnu/patches/0085-a03-cpu-bsd-checkpoints.patch', a.destination/'0085-a03-cpu-bsd-checkpoints.patch')
    shutil.copyfile(ROOT/'xnu/patches/0086-a03-bsd-general-register-codegen.patch', a.destination/'0086-a03-bsd-general-register-codegen.patch')
    (a.destination/'A03-PROFILE.txt').write_text(chr(10).join([
        'SWEET '+SHA+' through 0018; native 16K, arm64, single A55.',
        'Portable crypto 0020/0023/0027/0032/0033 and pinned BearSSL stage script.',
        'A03 GICv3 timer INTID27; logo candidate 0x9e000000 720x1600 stride2880.',
        'No rootfs/storage/peripheral drivers. Display needs device test.', '']))
    print('A03 profile staged:', len(patches)+4, 'patches; MACHINE_CONFIG=SWEET')


if __name__=='__main__':
    main()
