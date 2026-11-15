#!/usr/bin/env python3
"""Stage pinned native-16K SWEET core for A03 single-core kernel bring-up.

No Qualcomm storage, USB, power, GPU or Wi-Fi patches. A03 SDMA is opt-in.
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
EXTRA_USERSPACE = {19, 21, 22, 24, 25, 26}
EXTRA_PATCHES = EXTRA_CRYPTO | EXTRA_USERSPACE


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('destination', type=Path)
    p.add_argument('--source', type=Path, help='local pinned SWEET source for offline staging')
    p.add_argument('--ios-userspace', action='store_true',
                   help='add portable XML entitlement/platform-binary support for later iOS trials')
    a = p.parse_args()
    selected = EXTRA_PATCHES | ({35, 36} if a.ios_userspace else set())
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
        patches = [(x.name, x.read_bytes()) for x in sorted((source/'xnu/patches').glob('*.patch')) if int(x.name[:4])<=18 or int(x.name[:4]) in selected]
        stage = (source/'xnu/patches/0020-stage-bearssl.sh').read_bytes()
        pthread_stage = (source/'xnu/patches/0019-stage-libpthread.sh').read_bytes()
        hfs_stage = (source/'xnu/patches/0026-stage-hfs.sh').read_bytes()
    else:
        patches = [(Path(m.name).name, archive.extractfile(m).read()) for m in archive.getmembers()
                   if '/xnu/patches/' in m.name and m.name.endswith('.patch') and
                   (int(Path(m.name).name[:4])<=18 or int(Path(m.name).name[:4]) in selected)]
        member = next(m for m in archive.getmembers() if m.name.endswith('/xnu/patches/0020-stage-bearssl.sh'))
        stage = archive.extractfile(member).read()
        member = next(m for m in archive.getmembers() if m.name.endswith('/xnu/patches/0019-stage-libpthread.sh'))
        pthread_stage = archive.extractfile(member).read()
        member = next(m for m in archive.getmembers() if m.name.endswith('/xnu/patches/0026-stage-hfs.sh'))
        hfs_stage = archive.extractfile(member).read()
    if len(patches)!=(31 if a.ios_userspace else 29):
        raise SystemExit('unexpected core/crypto/userspace patch count')
    (a.destination/'0020-stage-bearssl.sh').write_bytes(stage)
    (a.destination/'0019-stage-libpthread.sh').write_bytes(pthread_stage)
    (a.destination/'0026-stage-hfs.sh').write_bytes(hfs_stage)
    changes = {
        '0003-sweet-framebuffer-serial-console.patch': [('FBCON_SCALE     2', 'FBCON_SCALE     1')],
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
    shutil.copyfile(ROOT/'xnu/patches/0087-a03-cortex-a55-cpu-match.patch', a.destination/'0087-a03-cortex-a55-cpu-match.patch')
    shutil.copyfile(ROOT/'xnu/patches/0088-a03-userspace-provider-codegen.patch', a.destination/'0088-a03-userspace-provider-codegen.patch')
    shutil.copyfile(ROOT/'xnu/patches/0089-a03-hfs-general-register-codegen.patch', a.destination/'0089-a03-hfs-general-register-codegen.patch')
    shutil.copyfile(ROOT/'xnu/patches/0090-a03-readonly-sdma-bsd.patch', a.destination/'0090-a03-readonly-sdma-bsd.patch')
    if a.ios_userspace:
        # Apple mount -P 1 uses bindfs for preboot firmware.
        name = '0037-sweet-config-bindfs.patch'
        shutil.copyfile(ROOT/'xnu/patches'/name, a.destination/name)
        name = '0091-a03-entitlements-general-register-codegen.patch'
        shutil.copyfile(ROOT/'xnu/a03'/name, a.destination/name)
        name = '0092-a03-userdata-root-selection.patch'
        shutil.copyfile(ROOT/'xnu/a03'/name, a.destination/name)
        name = '0093-a03-usb-state-probe.patch'
        shutil.copyfile(ROOT/'xnu/a03'/name, a.destination/name)
        name = '0095-a03-usb-probe-marker.patch'
        shutil.copyfile(ROOT/'xnu/a03'/name, a.destination/name)
        name = '0098-a03-catalog-direct-read.patch'
        shutil.copyfile(ROOT/'xnu/a03'/name, a.destination/name)
        name = '0099-a03-opt-in-unsealed-userdata-root.patch'
        shutil.copyfile(ROOT/'xnu/a03'/name, a.destination/name)
        name = '0100-a03-init-sigtrap-diagnostics.patch'
        shutil.copyfile(ROOT/'xnu/a03'/name, a.destination/name)
        name = '0101-a03-host-info-diagnostics.patch'
        shutil.copyfile(ROOT/'xnu/a03'/name, a.destination/name)
        name = '0102-a03-invalid-reply-diagnostics.patch'
        shutil.copyfile(ROOT/'xnu/a03'/name, a.destination/name)
        name = '0103-a03-usb-cdc-console.patch'
        shutil.copyfile(ROOT/'xnu/a03'/name, a.destination/name)
        name = '0104-a03-post-trap-usb-monitor.patch'
        shutil.copyfile(ROOT/'xnu/a03'/name, a.destination/name)
        for name in ('0105-a03-ios16-provisional-reply-compat.patch',
                     '0106-a03-usb-peripheral-phy-readback.patch',
                     '0107-a03-opt-in-software-keystore.patch',
                     '0108-a03-bounded-daemon-crash-diagnostics.patch',
                     '0109-a03-usb-supply-flat-endpoints.patch',
                     '0110-a03-usb-download-command.patch',
                     '0111-a03-usb-receive-diagnostics.patch',
                     '0112-a03-disabled-watchdog-capability.patch',
                     '0113-a03-usb-pio-takeover.patch',
                     '0114-a03-watchdog-software-boot-stage.patch',
                     '0115-a03-download-control-escape.patch',
                     '0116-a03-deeper-bounded-crash-stack.patch'):
            shutil.copyfile(ROOT/'xnu/a03'/name, a.destination/name)
    (a.destination/'A03-PROFILE.txt').write_text(chr(10).join([
        'SWEET '+SHA+' through 0018; native 16K, arm64, single A55.',
        'Portable crypto 0020/0023/0027/0032/0033 and pinned BearSSL stage script.',
        'A03 GICv3 timer INTID27; logo candidate 0x9e000000 720x1600 stride2880.',
        'Pinned libpthread and mockfs/HFS RAM-root.',
        'Experimental XML entitlements/platform CS_SIGNED support (0035/0036).' if a.ios_userspace else 'Minimal AMFI interface for static test init.',
        'Opt-in A03 SDMA; BOOT reads confirmed0024; USERDATA writes hardware-unverified.', '']))
    print('A03 profile staged:', len(patches)+8+18*int(a.ios_userspace), 'patches; MACHINE_CONFIG=SWEET')


if __name__=='__main__':
    main()
