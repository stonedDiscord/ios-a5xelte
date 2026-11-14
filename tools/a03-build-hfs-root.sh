#!/bin/bash
# Linux/macOS: build a small HFSX root independently of XNU.
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
host=$(uname -s)
cleanup() {
    if [[ $mounted == 1 ]]; then
        case $host in
            Darwin) hdiutil detach "$work/mount" || return ;;
            Linux) sudo umount "$work/mount" || return ;;
        esac
    fi
    # Retain the temporary image on failure for diagnosis.
}
trap cleanup EXIT
mkdir "$work/mount"
case $host in
Linux)
    for tool in mkfs.hfsplus fsck.hfsplus rsync mount umount sudo python3; do
        command -v "$tool" >/dev/null || { echo "Missing tool: $tool" >&2; exit 1; }
    done
    # Authenticate before formatting; unattended callers must cache sudo first.
    sudo -v
    truncate -s 32M "$work/root.img"
    mkfs.hfsplus -s -b 4096 -v A03TestRoot "$work/root.img"
    # hfsprogs 540.1 omits HFSX's root HasFolderCount flag on this host.
    # Repair only this newly created temporary volume, then verify read-only.
    fsck.hfsplus -fy "$work/root.img"
    fsck.hfsplus -n "$work/root.img"
    sudo mount -t hfsplus -o loop,rw "$work/root.img" "$work/mount"
    mounted=1
    sudo rsync -a --chown=0:0 -- "$source_dir/" "$work/mount/"
    sudo chown 0:0 "$work/mount"
    sudo chmod 755 "$work/mount" "$work/mount/sbin" "$work/mount/sbin/launchd"
    sync
    sudo umount "$work/mount"
    mounted=0
    fsck.hfsplus -n "$work/root.img"
    raw="$work/root.img"
    ;;
Darwin)
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
    raw="$work/raw.cdr"
    ;;
*) echo "Unsupported host: $host" >&2; exit 1 ;;
esac
python3 - "$raw" "$output" <<'PY'
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
