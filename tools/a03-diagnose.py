#!/usr/bin/env python3
"""Collect private A03 evidence; optionally build/run the Android EL0 probe.

Never reads other phones or writes partitions. Output defaults to ignored
backup/ because device diagnostics can contain identifying information.
"""
import argparse
import datetime
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serial', help='ADB target when multiple devices are connected')
    parser.add_argument('--run-probe', action='store_true')
    args = parser.parse_args()
    adb = ['adb'] + (['-s', args.serial] if args.serial else [])

    def shell(command):
        result = subprocess.run(adb + ['shell', command], capture_output=True,
                                text=True, timeout=30, check=False)
        return dict(exit_code=result.returncode, stdout=result.stdout.strip(),
                    stderr=result.stderr.strip())

    model = shell('getprop ro.product.model')
    if model['exit_code'] or model['stdout'] != 'SM-A035G':
        parser.error('Expected connected SM-A035G; refusing another or ambiguous device')
    platform = shell('getprop ro.board.platform')
    if platform['stdout'] != 'ums9230':
        parser.error('Expected ums9230; refusing an unverified platform')
    evidence = {'captured_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'model': model, 'platform': platform}
    commands = {
        'identity': 'id',
        'kernel': 'uname -a',
        'android': 'getprop ro.build.version.release',
        'security_patch': 'getprop ro.build.version.security_patch',
        'bootloader_locked': 'getprop ro.boot.flash.locked',
        'vbmeta_state': 'getprop ro.boot.vbmeta.device_state',
        'verified_boot': 'getprop ro.boot.verifiedbootstate',
        'build_type': 'getprop ro.build.type',
        'boot_completed': 'getprop sys.boot_completed',
        'partitions': 'ls -l /dev/block/by-name',
        'midr_cpu0': 'cat /sys/devices/system/cpu/cpu0/regs/identification/midr_el1',
        'root_binary': 'command -v su',
        'boot_readable': 'test -r /dev/block/by-name/boot',
        'fdt_readable': 'test -r /sys/firmware/fdt',
    }
    for name, command in commands.items():
        evidence[name] = shell(command)
    if args.run_probe:
        subprocess.run(['sh', str(ROOT / 'shim/a03/build-probe.sh')], check=True)
        subprocess.run(adb + ['push', str(ROOT / 'shim/a03/out/a03-el0-probe'),
                              '/data/local/tmp/a03-el0-probe'], check=True, timeout=30)
        probe = shell('chmod 755 /data/local/tmp/a03-el0-probe && /data/local/tmp/a03-el0-probe')
        evidence['el0_probe'] = probe
    folder = ROOT / 'backup' / ('galaxy-a03-' + evidence['captured_utc'][:10])
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / 'diagnostics.json'
    output.write_text(json.dumps(evidence, indent=2) + '\n')
    print('Private evidence:', output)
    if args.run_probe:
        print(evidence['el0_probe']['stdout'])
        if probe['exit_code'] or 'A03_EL0_PROBE_OK' not in probe['stdout']:
            raise SystemExit('EL0 probe did not complete; inspect private diagnostics')


if __name__ == '__main__':
    main()
