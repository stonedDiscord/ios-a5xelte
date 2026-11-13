# Galaxy A03 SM-A035G initial checkpoint

Probe 0003 successfully ran EL1 with actual 16 KiB translation and returned
through EL2 to Android on 2026-11-13. It is the current working BOOT, with
Magisk retained. Probe 0002d bootlooped because its reporter removed an
AVB argument needed by init; that reporter bug is fixed. See the latest
A03_PROGRESS.md entry for exact results and hashes.

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
