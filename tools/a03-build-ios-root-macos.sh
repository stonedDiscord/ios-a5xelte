#!/bin/bash
# Build a local journaled HFSX iOS root. Never accesses a phone or partition.
set -euo pipefail
[[ $# == 2 && $(uname -s) == Darwin ]] || { echo 'usage (macOS): script IPSW OUTPUT.img' >&2; exit 2; }
ipsw=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
output=$(cd "$(dirname "$2")" && pwd)/$(basename "$2")
[[ ! -e $output ]] || { echo 'output exists' >&2; exit 1; }
repo=$(cd "$(dirname "$0")/.." && pwd)
work=$(mktemp -d)
# hdiutil reports physical /private/var paths; keep mount checks consistent.
work=$(cd "$work" && pwd -P)
check_device=
cleanup() {
    build_status=$?
    if [[ -n $check_device ]]; then hdiutil detach "$check_device" || true; fi
    for name in root appos sysos os; do
        if mount | grep -F " on $work/$name (" >/dev/null; then hdiutil detach "$work/$name" || true; fi
    done
    # Retain a completed conversion even if final device verification fails.
    # CI logs/conclusion remain authoritative about whether fsck passed.
    if [[ $build_status != 0 && -f $work/raw.cdr && ! -e $output ]]; then
        mv "$work/raw.cdr" "$output"
        shasum -a 256 "$output" > "$output.sha256"
        echo 'Converted image retained for diagnosis; final verification FAILED.'
    fi
    echo "Build workspace retained: $work"
}
trap cleanup EXIT
python3 - "$ipsw" "$work" <<'PY'
import sys,zipfile,plistlib,hashlib
from pathlib import Path
p=Path(sys.argv[1]);h=hashlib.sha256()
with p.open('rb') as f:
 for b in iter(lambda:f.read(8<<20),b''):h.update(b)
sources={
 'a99575ccdab8bd576e16bc08efe0f8a5c18f0e7bdea522376235f5d5332acc19':('20A362','d22ap'),
 'b3882291a92ecf8763239a026813b3bafae66b7e317dee67011d90c202ccafef':('20H392','d21ap')}
assert h.hexdigest() in sources,'wrong IPSW'
build,device=sources[h.hexdigest()]
with zipfile.ZipFile(p) as z:
 m=plistlib.loads(z.read('BuildManifest.plist'))
 assert m['ProductBuildVersion']==build
 identity=next(i for i in m['BuildIdentities'] if i['Info']['DeviceClass']==device)
 for key,name in [('OS','os'),('Cryptex1,SystemOS','sysos'),('Cryptex1,AppOS','appos')]:
  source=identity['Manifest'][key]['Info']['Path'];print(key,source,flush=True)
  with z.open(source) as src,(Path(sys.argv[2])/(name+'.dmg')).open('xb') as dst:
   import shutil;shutil.copyfileobj(src,dst,8<<20)
PY
for name in os sysos appos; do
    mkdir "$work/$name"
    hdiutil attach -readonly -nobrowse -owners on -mountpoint "$work/$name" "$work/$name.dmg"
done
hdiutil create -size 16g -fs HFSX -fsargs '-J' -volname A03iOSRoot -layout NONE "$work/root.dmg"
mkdir "$work/root"
hdiutil attach -nobrowse -owners on -mountpoint "$work/root" "$work/root.dmg"
# Reuse portable file staging only; no donor hardware or partition tool.
sudo env STAGE_FULL=1 STAGE_ALL_APPS=1 bash "$repo/tools/a5xelte-stage-ios-root.sh" "$work/os" "$work/sysos" "$work/appos" "$work/root"
sudo python3 "$repo/tools/sweet-root-tweaks.py" "$work/root"
sudo python3 "$repo/tools/a03-stage-wallpaper-catalog.py" "$work/root"
python3 "$repo/tools/a03-inspect-ios-root.py" "$work/root" | tee "$output.inventory.json"
sync
hdiutil detach "$work/root"
hdiutil convert "$work/root.dmg" -format UDTO -o "$work/raw"
# macOS fsck_hfs requires a device ioctl; a regular-file path fails ENOTTY.
hdiutil attach -readonly -nomount -plist "$work/raw.cdr" > "$work/check-device.plist"
check_device=$(python3 - "$work/check-device.plist" <<'PYDEVICE'
import plistlib,sys
with open(sys.argv[1],'rb') as f:p=plistlib.load(f)
devices=[e['dev-entry'] for e in p['system-entities'] if 'dev-entry' in e]
assert len(devices)==1,devices # raw layoutNONE HFSX, no partition table
print(devices[0])
PYDEVICE
)
sudo fsck_hfs -fn "/dev/r${check_device#/dev/}"
hdiutil detach "$check_device"
check_device=
mv "$work/raw.cdr" "$output"
shasum -a 256 "$output" > "$output.sha256"
echo 'Local iOS root prepared; no phone write. Runtime boot remains unverified.'
