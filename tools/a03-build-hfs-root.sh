#!/bin/bash
# macOS: build a small HFSX root independently of XNU.
set -euo pipefail
[[ $# == 2 ]] || { echo "usage: $0 ROOT_DIRECTORY OUTPUT.img" >&2; exit 2; }
source_dir=$(cd "$1" && pwd)
output_dir=$(cd "$(dirname "$2")" && pwd)
output="$output_dir/$(basename "$2")"
[[ ! -e "$output" && -f "$source_dir/sbin/launchd" ]] || {
    echo 'Output exists or root is missing sbin/launchd' >&2; exit 1;
}
work=$(mktemp -d)
mounted=0
cleanup() {
    if [[ $mounted == 1 ]]; then hdiutil detach "$work/mount" || return; fi
    # Retain the temporary image on failure for diagnosis.
}
trap cleanup EXIT
mkdir "$work/mount"
hdiutil create -size 32m -fs HFSX -volname A03TestRoot \
    -layout NONE "$work/root.dmg"
hdiutil attach -nobrowse -owners on -mountpoint "$work/mount" "$work/root.dmg"
mounted=1
sudo ditto "$source_dir" "$work/mount"
sudo chown -R 0:0 "$work/mount"
sudo chmod 755 "$work/mount" "$work/mount/sbin" "$work/mount/sbin/launchd"
sync
hdiutil detach "$work/mount"
mounted=0
hdiutil convert "$work/root.dmg" -format UDTO -o "$work/raw"
python3 - "$work/raw.cdr" "$output" <<'PY'
from pathlib import Path
import sys,struct,hashlib
src,out=map(Path,sys.argv[1:]);data=src.read_bytes()
assert data[1024:1026]==b'HX', 'not a raw case-sensitive HFSX volume'
block,count=struct.unpack_from('>II',data,1064)
size=block*count
assert 0<size<=len(data)
assert data[size-1024:size-1022]==b'HX', 'missing alternate HFSX header'
with out.open('xb') as f:f.write(data[:size])
print('HFSX root:',size,'bytes; SHA256',hashlib.sha256(data[:size]).hexdigest())
PY
