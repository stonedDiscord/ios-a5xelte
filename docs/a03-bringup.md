# Galaxy A03 SM-A035G initial checkpoint

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

## Current barrier to a first bootloader probe

Stock Android refuses root and raw BOOT/FDT reads. An unlocked-bootloader
property does not supply the original BOOT, validate image acceptance, or
provide a tested restore route. No matching stock image is available in
this branch, and no custom-image reboot or flash was attempted.

Obtain the exact installed firmware BOOT and matching DTB/DTBO or
privileged read access first. Inspect their real formats and hardware
description before writing a bootloader-entry probe. Keep recovery,
bootloaders, vbmeta, EFS/NV and USERDATA intact. A3/A03s/A03 Core and
SM-A035 variants are not interchangeable firmware targets.
