# A03 filesystem development

BOOT 0012 is the working HFSX RAM-root/PID1 checkpoint, confirmed by the
user on 2026-11-14: md0/rmd0 registered, A03TestRoot mounted, /sbin/launchd
executed and the static init printed its PID1 banner and heartbeat. This
is test userspace, not Apple's launchd or an iOS interface. Keep BOOT 0011
(mockfs PID1) as the earlier fallback.

## Separate the kernel from its root image

- Kernel: pinned HFS provider 0026 + A03 0089, built once through xnu.yml.
- Files: a03-root.yml creates a 32 MiB raw HFSX root with static test init.
  This workflow never builds XNU. Optional a03-root/ contents overlay the
  test root; do not commit Apple binaries.
- Repack locally with an existing downloaded HFS-capable kernel:

    python3 tools/a03-pack-root.py KERNEL ROOT.img shim/a03/out/NEW.img --adt shim/a03/out/a03-0002.adt

The tool refuses existing outputs, checks root bounds, retains the pinned
BOOT base, and writes a hash manifest. It does not flash. Files/bootargs
only require packaging, not a kernel build. The 32 MiB cap keeps this trial
within BOOT/256 MiB RAM limits; it is not a full iOS root.

## Local Linux filesystem loop

The same builder now supports Linux using hfsprogs, rsync and a kernel
with hfsplus support. Run from an interactive terminal; sudo is required
to mount the temporary image and set Unix ownership. No device partitions
are mounted or written by this builder. Output paths must not already exist.

```sh
mkdir -p shim/a03/out/linux-root/{sbin,dev,private/var/tmp}
clang -target arm64-apple-ios16.0 -c tools/sweet-init.S -o shim/a03/out/linux-root-init.o
python3 tools/mkinit.py shim/a03/out/linux-root-init.o shim/a03/out/linux-root/sbin/launchd
# Edit/add files under shim/a03/out/linux-root, then:
bash tools/a03-build-hfs-root.sh shim/a03/out/linux-root shim/a03/out/root-NEW.img
python3 tools/a03-pack-root.py xnu/out-a03-43536143024/kernel.development.sweet shim/a03/out/root-NEW.img shim/a03/out/a03-root-NEW.img --adt shim/a03/out/a03-0002.adt
```

Linux init compilation reproduces the exact working 16635-byte binary,
SHA256 f5de3714ff95e6a3b9ece30723f677de0f3f74ec5eb985a00c5ae872f0ac9bf1.
The local hfsprogs formatter omits the HFSX root HasFolderCount flag; the
builder repairs its new temporary volume and checks it before mounting.
Formatting/repair/read-only fsck were tested here. End-to-end Linux copying
is pending interactive sudo authentication; this agent's noninteractive
attempt could not obtain a password. The successful BOOT 0012 root came
from the independent macOS root job. That job remains a working fallback.

XNU CI uses its native CCACHE make variable and a persistent compiler cache,
keyed by runner/compiler/profile/configuration with a commit-specific save.
A first build fills the cache. Subsequent changes can reuse unchanged
compilations; generated headers, linking and dependency setup still run.
This is compiler caching, not restored make-object incremental state.

## Storage facts and next checkpoint

Live DT and Samsung kernel source agree on eMMC controller
sprd,sdhc-r11p1, MMIO 0x201d0000, span 0x1000, GIC SPI10 (INTID42),
8-bit bus, HS400/HS200 support. Linux driver is
 drivers/mmc/host/sprd-sdhcr11.c and .h. Live by-name identifies USERDATA as
/dev/block/mmcblk0p55; BOOT is p39. These are not Qualcomm UFS.

HFS mount and test PID1 execution are now confirmed. Next inspect
bootloader-retained controller/clock/card state and implement
bounded, read-only eMMC access, validate GPT and block reads against host
backups, and only then expose a BSD block device. Do not reset/reconfigure
clocks, assume a card RCA, or issue storage writes from guessed state.
No non-BOOT partition is authorized for the current trials. A real iOS root
will need storage plus later signing/entitlement/display work.

BOOT 0013 uses a local loader-only snapshot to inspect retained eMMC state:

```sh
A03_EMMC_SNAPSHOT=1 python3 tools/a03-xnu-image.py backup/galaxy-a03-2026-11-13/firmware/magisk-boot.img shim/a03/out/a03-xnu-0012-hfs.payload shim/a03/out/NEW-snapshot.img
```

The option reads only the explicitly listed controller registers and pauses
before XNU so a photo preserves the values. It sends no card commands and
does not read sectors. The reused payload is unchanged. Ordinary packaging
without the environment option retains the normal XNU boot path. The
current snapshot register results are pending a physical screen report.

## CachyOS ldid compatibility

The current AUR ldid-2.1.5-procursus7 source fails against this host's
OpenSSL4 headers (opaque ASN1_STRING plus const API changes). The installed
openssl-3 package provides compatible headers and libcrypto.so.3.
Building the already prepared source with these overrides succeeded:

    make LIBCRYPTO_INCLUDES=-I/usr/include/openssl-3 LIBCRYPTO_LIBS='-L/usr/lib/openssl-3 -lcrypto'

A tested local executable is shim/a03/out/host-tools/ldid (ignored). It
ad-hoc signed a disposable copy of the test init and printed its CDHash.
No system package files or original test-init image were modified. Our
static init tool already generates its own signature; ldid is optional
for that checkpoint. Use a maintained package fix for a system install.
