# A03 filesystem development

BOOT 0011 is the working static mockfs PID1 checkpoint. Keep it as fallback.

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

First prove the HFS volume mounts from RAM and executes the same test PID1.
Then inspect bootloader-retained controller/clock/card state and implement
bounded, read-only eMMC access, validate GPT and block reads against host
backups, and only then expose a BSD block device. Do not reset/reconfigure
clocks, assume a card RCA, or issue storage writes from guessed state.
No non-BOOT partition is authorized for the current trials. A real iOS root
will need storage plus later signing/entitlement/display work.

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
