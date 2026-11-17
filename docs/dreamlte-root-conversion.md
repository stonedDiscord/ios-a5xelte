# S8 userspace IPSW conversion

The user authorizes the converted iOS root on existing USERDATA/sda24,
58,556,678,144 bytes. Never flash the raw IPSW archive. Keep Apple images,
mounts, converted images and device dumps ignored. Do not restore Android.
Deployment does not prove that the unfinished S8 UFS driver can mount it.

The local20H392 IPSW contains OS087-86698-044.dmg,
SystemOS087-86593-047.dmg and AppOS087-86715-047.dmg. The three read-only
APFS-FUSE mounts are under research/dreamlte/root/mounts/{os,sysos,appos}.
The root generator follows tools/mkiosroot.sh's layout: base OS, both
cryptexes under private/preboot/Cryptexes, missing libraries/cache at the
root search paths, logd stores and the donor plaintext keybag.

The host lacks passwordless sudo. tools/dreamlte-hfs-import.c writes an HFSX
image without a writable mount. It uses planetbeing/libdmg-hfsplus at
7ac55ec64c96f7800d9818ce64c79670e7f02b67, with
tools/dreamlte-hfs-utf8.patch applied. That patch fixes UTF-8 decoding and
32-bit allocation offsets above4GiB. Build the hfs target in Release mode;
the importer uses a bounded shared mmap and flushes it before completion.

    git -C LIBRARY apply /absolute/path/tools/dreamlte-hfs-utf8.patch
    cmake -S LIBRARY -B LIBRARY/build-release -DCMAKE_BUILD_TYPE=Release -DCMAKE_POLICY_VERSION_MINIMUM=3.5
    cmake --build LIBRARY/build-release --target hfsplus -j4
    cc -O2 -Wall -Wextra -I LIBRARY/includes tools/dreamlte-hfs-import.c LIBRARY/build-release/hfs/libhfs.a LIBRARY/build-release/common/libcommon.a -lz -o IMPORTER
    python3 tools/dreamlte-root-manifest.py MOUNTS GENERATED > manifest.bin
    truncate -s 32G root.img
    mkfs.hfsplus -s -b 4096 -v iOSRoot root.img
    IMPORTER root.img < manifest.bin
    fsck.hfsplus -f -n root.img

Use fresh output files; the importer refuses existing non-directory entries.
Do not run fsck while the importer is writing. Never flash an interrupted
image. Current conversion intentionally starts non-journaled: the extracted
Ubuntu hfsprogs540.1 formatter's journaled image reports a minor header issue
even before import, while its non-journaled image passes a read-only check.
Journal setup must be resolved before treating this as a durable writable
runtime root.

Numeric UID/GID, full POSIX modes, file contents and symlinks are preserved.
HFS Unicode3.2 decomposition is applied with Apple's excluded ranges, and
normalization collisions abort generation. Hard links are copied as separate
files. Extended attributes, BSD flags and timestamps are not yet preserved;
do not claim a metadata-complete Apple restore. APFS compression is decoded
by APFS-FUSE; copying its compression xattr would be incorrect.

Smoke checks passed for file mode0751/UID272/GID272, absolute symlink,
accented and supplementary Unicode names, plus forced allocation above4GiB,
with clean non-journaled HFSX fsck. Full-image fsck, extracted launchd/cache
hashes and size/partition checks are still required before any USERDATA flash.
Installed Heimdall2.2.2 on64-bit Linux uses64-bit total-byte packets and
unsigned-long file offsets, reviewed against its v2.2.2 source. Preserve the
PIT; never use --repartition or --skip-size-check.

The completed20H392 image passed full read-only fsck. Extracted launchd and
43 cache components match their mounted-source SHA256 values. The HFS-image
cache prerequisite checker also passes all42 declared subcache UUIDs,
mapping bounds, symbols UUID and core dependency names (2710 images).
Raw image SHA256:
`35427cc9d9f40b6383afabf1b0f5370ebc4f85a42d3f079708b6548121dca3e7`.

Raw USERDATA upload failed at the first sequence confirmation; USERDATA may
be partial. An Android sparse container was generated with img2simg:

    img2simg root.img root.sparse.img

Its15,409,217,756-byte file expands to the exact same32GiB image SHA256
(RAW/FILL chunks, no omitted blocks). The subsequent --resume retry failed
to begin a session, sending no payload. Physical Download Mode re-entry is
required to clear this failed session before another upload. No successful
USERDATA deployment has been observed yet.
