# Galaxy A03 SM-A035G bring-up

As of 2026-11-14, BOOT0024 is flashed with the corrected XNU sector-size
callback and the same storage diagnostic RAM root. BOOT0023 established
raw BOOT-header reads, then failed buffered read with EINVAL because
d_psize returned partition count instead of sector bytes. Kernel
CI43598578558 passed; compiled512-byte return, host regressions and
BOOT upload verified. User now confirms full raw+block BOOT-header/EROFS PID1 PASS.
BOOT0020 established GPT integrity/partition identity and a
matching current-BOOT header plus512-byte payload sample; USERDATA has a
7-sector tail gap. BOOT0012 separately established HFS RAM-root/static
PID1 execution. Apple launchd, an eMMC filesystem root and iOS GUI are
not established. See the latest A03_PROGRESS.md entry for authoritative
image hashes and runtime evidence; the instructions below retain earlier
checkpoint reproduction details, not claims about the currently flashed image.

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
