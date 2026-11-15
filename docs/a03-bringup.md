# Galaxy A03 SM-A035G bring-up

As of 2026-11-15, XNU BOOT0050 boots the verified 16GiB HFSX root on
validated USERDATA p55 and reaches Apple's launchd_cache_loader boot task.
The preceding provisional-reply, firmware bindfs and keybag failures have
been passed. Current physical error is abort: Unable to find AMFI, followed
by launchd_cache_loader SIGABRT. The kernel has no AppleMobileFileIntegrity
IOKit service. ReVa confirms the actual iOS16.0 loader's built-in
launchd_unsecure_cache=1 lab path skips signature/trust registration.
BOOT0051 is flashed BOOT-only with that additional argument, same0050 kernel.
Cache-loader outcome and sustained bootstrap remain pending. Software AppleKeyStore remains an explicit opt-in lab
provider without SEP/passcode protection. No sustained successful bootstrap
or GUI is established. The USB CDC console has not enumerated.

See the latest A03_PROGRESS.md entry and top active handoff in NOTES.md for
exact artifacts and runtime observations. Older sections below preserve
checkpoint reproduction and should not be read as current-device status.

Historical probe0003 ran EL1 with actual16KiB translation and returned
through EL2 to Android on2026-11-13. Probe0002d bootlooped because its
reporter removed an AVB argument needed by init; that bug is fixed.

Read `A03_PROGRESS.md` first. The A03 is UNISOC ums9230/T606, not an
Exynos phone. Do not boot donor S8/S7/A5 images or reuse their MMIO,
partition paths, image wrappers or partition-write authorization.

## Reproduce the running Android diagnostic

```sh
python3 tools/a03-diagnose.py --run-probe
```

Requires host Python 3, ADB, Clang and LLD. No Android NDK or libc is used.
The script verifies model SM-A035G and platform ums9230, collects selected
facts into ignored `backup/galaxy-a03-YYYY-MM-DD/diagnostics.json`, builds
the probe, and runs it in Android's `/data/local/tmp`. Select a device with
`--serial` if needed. Omitting `--run-probe` only collects evidence.

The diagnostic prints timer frequency, virtual counter and Linux's EL0
views of MIDR/MMFR0. A successful run ends in `A03_EL0_PROBE_OK`. Linux
can emulate/filter ID-register reads; the MMFR0 output is **not evidence
of the physical CPU's supported page granules**. The CPU can migrate
between reads. This executable is not bootable as a Linux Image.

## First pre-Linux probe (verified on device)

Magisk BOOT from the supplied matching revision-5 firmware now boots, root
works, and verified live backups are stored privately. The first returning
probe also booted and reported all six register markers through cmdline.
See `A03_PROGRESS.md` for image hashes, exact results and restore state.

```sh
python3 tools/a03-probe-image.py \
  backup/galaxy-a03-2026-11-13/firmware/magisk-boot.img \
  shim/a03/out/a03-boot-probe-NEW.img
```

This host-only builder refuses any base except the verified Magisk BOOT
SHA256, and refuses an existing output path. It preserves the raw kernel
except first entry branch, appends its temporary stack/code within the
kernel's declared BSS, and copies ramdisk/DT bytes. AVB signatures remain
stale, like the supplied Magisk image; do not use on a locked device.

The probe parses `/chosen/bootargs` with bounded FDT reads and replaces
six verified diagnostic/identity hints in place without resizing the FDT.
Markers a03m/i/p/e/s/f carry MMFR0, MIDR, MPIDR, CurrentEL, SCTLR_EL1 and
CNTFRQ respectively. It preserves boot arguments x0..x3, SP, LR and DAIF,
then branches back to the original kernel entry. It performs no MMIO or
storage writes. Restore Magisk BOOT after collecting evidence.

Actual boot entry is **EL2**, unlike the Samsung Exynos donors. Probe 0003
established the EL1 transition and actual 16 KiB mapping before returning
to EL2 and Linux. GIC/timer interrupts are the next checkpoint. Keep recovery,
bootloaders, vbmeta and EFS/NV intact; no wipe is required for these tests.
A03s/A03 Core and other variants are not interchangeable firmware targets.

## Reproduce the successful 16 KiB host build

```sh
python3 tools/a03-test-reporter.py backup/galaxy-a03-2026-11-13/live/live.dtb
python3 tools/a03-probe-image.py \
  backup/galaxy-a03-2026-11-13/firmware/magisk-boot.img \
  shim/a03/out/a03-boot-probe-NEW.img --mmu16k \
  --elf shim/a03/out/a03-boot-probe-NEW.elf
```

The EL1 test uses Normal NC pages, MMU enabled and caches disabled.
Success t=0x16384 means alias read/write and unmapped-VA AT check passed.
Other markers: l=CurrentEL, q=TCR, u=SCTLR with MMU on, a=alias PAR,
y=EL2 return ESR (expected HVC64 0x5a000a03). The reporter regression
check stubs hardware results; it tests FDT mutation, not MMU emulation.

## First XNU-only trial (2026-11-13)

CI run 43485850320 produced a plain arm64 XNU 8796 DEVELOPMENT kernel.
See A03_PROGRESS.md for its SHA256, exact device write and observations.
To reproduce host packaging with that private downloaded artifact:

    python3 tools/mkadt_a03.py shim/a03/out/a03.adt
    python3 tools/mkpayload.py xnu/out-a03-43485850320/kernel.development.sweet shim/a03/out/a03.adt shim/a03/out/xnu-first.payload --cmdline 'debug=0x14e serial=3 cpus=1 keepsyms=1 -v -noprogress'
    python3 tools/a03-xnu-image.py backup/galaxy-a03-2026-11-13/firmware/magisk-boot.img shim/a03/out/xnu-first.payload shim/a03/out/a03-xnu-NEW.img

The packer builds the freestanding EL2-to-EL1 loader and preserves the
verified BOOT v2 base's ramdisk and DT table. Only the kernel component
is replaced. It retains stale AVB metadata, as accepted by the unlocked
phone, and refuses any other base or an existing output path. XNU RAM
starts at 0x102000000 (32 MiB aligned), size 256 MiB. All payload segment
and entry bounds are checked before any copy. BOOT p39 is the only
partition authorized for these trials; retain matching stock/Magisk restore.

This profile has no rootfs or A03 storage/USB drivers. Absent ADB is not
proof of kernel progress. The 0x9e000000 logo RAM display candidate and
32-bit format are unverified; a blank screen is inconclusive too.

For a DEVELOPMENT startup stall, first add the existing boot arguments
-enable_kprintf_spam startup_debug=1 -show_pointers when generating the
payload. startup_debug alone does not override DEVELOPMENT kprintf
suppression. This exposes initializer addresses without a kernel rebuild.
A final printed policy line alone does not prove the next function hung.

## Authorized USERDATA write/root preparation (2026-11-14)

The user authorized filesystem preparation on USERDATA p55. BOOT remains
read-only through the XNU provider; preserve GPT/recovery/bootloaders/EFS/NV.
The existing `--emmc-readonly` option is the legacy controller opt-in name;
`a03-pack-root.py --userdata-writable` separately enables `a03emmc_rw=1`.
Every write is bounded again against validated GPT USERDATA geometry.
CMD24 completes transfer, CMD6 FLUSH_CACHE handles enabled card cache,
and fresh CMD13 checks ready/TRAN. A failed command permanently disables
further I/O; host fake-MMIO tests do not establish hardware success.

`a03-root.yml` input `userdata_write_probe=true` builds a diagnostic that
saves one sector at USERDATA-relative16GiB, writes an XOR pattern, reads it
back, restores the sector and verifies it, then fsyncs. It uses the raw node
and requires the writable kernel. This location is beyond the proposed
16GiB HFS image; original Android USERDATA is disposable under authorization.
A restore failure is reported explicitly. Device evidence is still required.

`a03-ios-root.yml` stages the supplied iPhone X iOS16.0/20A362 source as a
16GiB journaled HFSX image. The builder verifies a pinned IPSW hash, preserves
owners, copies stock applications and cryptex files, applies portable donor
filesystem tweaks using the actual staged version, inventories dynamic
plain-arm64 launchd/dyld/SpringBoard/cache prerequisites, and runs fsck.
This workflow never writes a phone. Apple assets remain ignored/transient.

The optional `--ios-userspace` profile also stages0092, selecting the BSD
USERDATA device directly for explicit `rd=a03userdata0` without waiting for
an absent IOMedia service. `rootrw=1` clears read-only only for the validated,
write-enabled USERDATA device. HFS dirty-volume/journal checks remain active.
`a03-pack-root.py --userdata-root` adds these arguments while retaining the
small RAM image in the payload; repackage without the flag to use RAM root.
This root-selection revision requires a fresh full build and runtime test.
No Apple launchd or SpringBoard execution is established by image preparation.


## Independent stock-Linux reader (2026-11-15)

Build BOOT-only diagnostic with matching verified Magisk base:

    python3 tools/a03-linux-reader-image.py shim/a03/out/a03-linux-reader-NEW.img

Requires aarch64-linux-gnu-gcc/static libc. Kernel/DT unchanged; only initramfs
replaced. No Android init/fstab or USERDATA mount. Existing GPT CRC/range/
identity validator gates reads/export. USB mass-storage LUN0 is a1MiB RAM
file containing raw diagnostic text; validated USERDATA LUN1 is read-only.
No partition opens writable and no repair/write mode. FB0 output uses queried
Linux geometry. Host builds do not prove execution or USB enumeration; consult
A03_PROGRESS.md for current flashed candidate and runtime evidence.


Reader revision7 adds one authorized diagnostic write: a4096-byte CRC-protected
report at USERDATA-relative16GiB, immediately beyond the16GiB HFS volume.
Requires successful existing GPT validation and sufficient partition capacity;
never writes GPT or other partitions. USB export stays read-only. Reader5
established init execution through its timed return to Download mode; display
and USB output remained unavailable. Reader7 returns similarly after45seconds.
To display its saved report through the known shim framebuffer:

    A03_EMMC_SNAPSHOT=6 python3 tools/a03-xnu-image.py BASE PAYLOAD OUTPUT

This profile validates GPT, reads only the bounded mailbox, checks magic/CRC,
displays text and halts before XNU. It is not an XNU/launchd execution test.


## Linux USB root installation

The configfs function symlink must use an absolute target: this4.14 kernel
resolves symlink input from process cwd before creating the configfs link.
The fixed reader enumerated1d6b:0104 and exported report/USERDATA successfully.
Explicit --userdata-writable changes only validated USERDATA LUN1 to RW;
LUN0 stays RO, no whole-card LUN. Writable profile serialA03LinuxInstallV11.
It waits2hours after UDC bind; default reader remains RO and waits15minutes.

    python3 tools/a03-linux-reader-image.py OUTPUT --userdata-writable
    python3 tools/a03-install-usb-root.py VERIFIED_ROOT_IMAGE --write

Installer accepts only the pinned16GiB root SHA and exact USB LUN identity/
54381228032-byte partition capacity, rejects mounts/wrong device, writes
exactly16GiB, fsyncs and verifies a full O_DIRECT readback SHA. The existing
4KiB diagnostic mailbox beyond16GiB remains separate. Host block permissions
must permit the read/write; do not grant access to any host disk. Device
assignment can change after USB reconnect; recheck model/serial/LUN each time.


USB status image revision0014 fixes bounded DRM resource/connector output
arrays and prefers DRM/KMS. It draws mode, UDC state, partition read/written
MiB and uptime. Status counters are Linux block-sector counters, not host-side
hash verification or iOS progress. On-screen display requires runtime testing.
