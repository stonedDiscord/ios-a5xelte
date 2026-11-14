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
snapshot is confirmed on hardware; exact values are in A03_PROGRESS.md.
Clock is enabled/stable, no inhibit bits, 8-bit HS200. The retained
response indicates TRAN/ready, but it is not a fresh card status.

Mode A03_EMMC_SNAPSHOT=2 prepares trial0014: snapshot followed by one
guarded CMD13 SEND_STATUS to the retained candidate RCA. It writes only
controller command/interrupt registers, restores interrupt enables and
pauses after a bounded poll. No sector read, DMA, reset, card selection or
storage write. Interpret its response before implementing block reads.
Loader glyph rendering now uses the font's MSB-first bit order to correct
the individually mirrored characters reported on trial0013.

Trial0014 fresh CMD13 returned INT1/RSP900/PRESENT01f000f0; RCA1 ready/TRAN
and glyph orientation confirmed. Trial0015 (A03_EMMC_SNAPSHOT=3) adds
bounded read-only PIO: EXT_CSD first, then only if user partition selected
with 512-byte sectors, CMD17 LBA0/LBA1. Checks MBR signature and GPT header
CRC32; does not validate the GPT entry array or provide a BSD block driver.
Register/command references are the local android_kernel_samsung_a03 tree.
0015 photo reports CMD8 R1=900/INT2/PRESENT01f000f0 followed by failure.
Transfer-complete without error bits is not sufficient to claim buffer
reception: the failed stage/FIFO count were not visible in0015. Trial0016
keeps the read path and adds stage/status/FIFO diagnostics at rows65..71,
pending flash. No XNU rebuild or extra controller reconfiguration.

0016 confirms fail-stage2/read-ready, FIFO0, seen interrupt3/final2.
Downstream sprd_send_cmd always enables DMA for data; it has no PIO path.
Live transfer mode also reads0x13 rather than requested0x10. Trial0017
uses mode4, following sprd_sdmd_mode's single-buffer SDMA registers:
HOST DMA select0, v4 count0x00, buffer0x58/0x5c, read transfer0x11.
DMA writes only a dedicated loader-owned512B RAM buffer; commands still
read-only. No card configuration, sector write, clock change or reset.
MMU/cache/version/address guards and bounded polls precede parsing; metadata
must pass before LBA0/1.0017-sdma-read-v2 flashed and physically confirmed:
EXT revision8, partition config8 (user area selected), sector count0747c000,
512-byte sectors, MBRaa55, GPT header CRC040a1bb6 matches computed value.
This proves metadata and first-sector reads via SDMA, not yet a mounted
eMMC filesystem or XNU block driver. Next validate GPT entry-array CRC,
partition identities/bounds and known current BOOT bytes before integration.

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

## XNU read-only SDMA integration (2026-11-14, runtime pending)

Trial0020 validates primary GPT entries/CRC, BOOT and USERDATA identities,
then matches the current BOOT header and512 immutable payload bytes. User
reports a7-sector gap after USERDATA before last-usable; a gap is legal and
not evidence of corrupt geometry. This remains a loader checkpoint.

A03 profile patch0090 adds an opt-in BSD reader using the validated SDMA
register sequence. It maps only201d0000+1000, allocates a permanent private
contiguous page and performs cache maintenance before/after device writes
to RAM. Unlike the loader trial, this runs with the XNU MMU/cache and DMA
above4GiB; those behaviors need physical validation. Any command failure
disables the reader permanently and retains its DMA buffer.

The first integration trial keeps `rd=md0` and the known HFS RAM root.
Both an ADT node and `a03emmc=1` are required; ordinary ADTs omit the node.
Read-only `/dev/a03boot0` and `/dev/ra03boot0` expose BOOT, with USERDATA
on minor1 as `/dev/a03userdata0` and `/dev/ra03userdata0`. No storage write
command is implemented. USERDATA does not become the root automatically.

Prepare the ADT and package only after kernel and root artifacts validate:

```sh
python3 tools/mkadt_a03.py shim/a03/out/NEW-emmc.adt --emmc-readonly
python3 tools/a03-pack-root.py KERNEL ROOT.img shim/a03/out/NEW.img \
  --adt shim/a03/out/NEW-emmc.adt --emmc-readonly
```

Dispatch `a03-root.yml` with `storage_probe=true` for the matching PID1
test. It reads one BOOT header through raw and buffered BSD paths, checks
Android magic/v2/page2048, and requires write-only open to return EROFS.
It never submits a storage write; the normal heartbeat continues after
either PASS or FAIL. A successful root build alone does not establish
XNU DMA, BSD reads or real Apple launchd execution.

### Raw BSD user-copy correction

Trial0021's reported data-abort PCfffffe00074d8fb0 resolves in its exact
kernel to emmc_strategy's destination byte store after successful SDMA
read. XNU buf_map leaves a noncluster buffer's b_datap unchanged, and
physio supplies a user address: direct kernel stores were incorrect.
The corrected raw cdev uses uiomove in caller context after each bounded
read, outside the hardware mutex. Buffered strategy rejects B_PHYS.
Run python3 tools/a03-test-bsd-storage.py for actual-handler host ASan/
UBSan boundary, partial-I/O and copy-fault checks. These tests do not
emulate XNU or hardware. Reuse the same verified storage-test root for
the corrected-kernel trial; no filesystem rebuild is required.

### PID1 failure-stage diagnostics (root-only update)

BOOT0022 reached static PID1 but the user reports generic storage FAIL.
The diagnostic init now prints separate raw/block header PASS lines and
hexadecimal stage/value on failure. Base0x10 is raw, base0x20 is block:
+0 open errno, +1 read errno, +2 short byte count, +3 observed magic,
+4 observed page size, +5 observed header version. Stage0x30 is the
write-only-open errno (expected30 decimal/EROFS);0x31 is an unexpected
successful write-only open, with the returned descriptor. No sector write
is attempted. Heartbeat continues after failure.

Compile sweet-init.S with -DA03_STORAGE_TEST, wrap with mkinit.py, then
optionally run tools/a03-test-storage-init.py INIT_MACHO (Python unicorn).
Instruction emulation covers PASS and all14 failure stages with stubbed
Darwin syscalls; it does not emulate XNU/device behavior. Default init
remains byte-identical. Rebuild only a03-root.yml(storage_probe=true),
then reuse corrected kernel43590138639 and the opt-in emmc ADT.

### XNU block-device sector-size correction

BOOT0023 reports stage0x21/value0x16 (buffered read/EINVAL), after raw
BOOT header validation passed. XNU specfs set_blocksize interprets d_psize
as bytes per sector, matching native memdev's mdSecsize return. Returning
partition sector count made v_specsize131072 exceed PAGE_SIZE16384 and
blocked spec_read before strategy. A03 now returns512; block count remains
available through DKIOCGETBLOCKCOUNT. Actual-handler sanitizer tests cover
the callback contract and a full16KiB/32-sector buffered transfer. Physical
validation of this correction remains pending the next kernel trial.
