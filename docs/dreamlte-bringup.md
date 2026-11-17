# S8 adaptation from HEROLTE

The S7 donor already solves 4K XNU, ARMv8.0 without LSE, GICv2 and the
Samsung legacy BOOT wrapper. It does not supply an S8 hardware port.

Start with DREAMLTE_PROGRESS.md. Only BOOT test writes are authorized.
The existing Android kernel and ramdisk remain the restore checkpoint.

## Local build / validation

    sh shim/dreamlte/build.sh
    python3 tools/mkadt_dreamlte.py shim/out/dreamlte.adt
    python3 tools/dreamlte-build-profile.py research/dreamlte-patches

The workflow uses the profile generator instead of staging all later S7
patches when board_profile=dreamlte and machine_config=HEROLTE are chosen.
Output kernel is still named kernel.development.herolte; the profile, not
that filename, determines which board header was built.

When `research/ipsw-x/d22ap.adt` is available, the builder retains its
non-placeholder `/product` properties so the iOS 16.7.16 D22AP userspace sees
the expected iPhone X product identity. Keep that Apple-derived tree ignored.

Package only after a successful S8-profile kernel build:

    python3 tools/mkpayload.py KERNEL shim/out/dreamlte.adt shim/out/dreamlte-payload.bin --cmdline 'debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress'
    python3 tools/herolte-pack-boot.py pack backup/galaxy-s8-2026-11-13/boot.img shim/dreamlte/out/xnu_boot.Image shim/out/dreamlte-xnu.img --chip 8895 --append shim/out/dreamlte-payload.bin --partition-size 41943040

A loader-only packaging smoke test exists in shim/out but has no XNU
payload; never flash it. The loader currently halts on failure and logs in
RAM. The loader now records a read-only DWC3 core snapshot alongside the
existing RAM trace. After Android returns, capture that trace over the same
USB cable with:

    tools/dreamlte-capture-last-kmsg.sh backup/galaxy-s8-2026-11-13/last-kmsg-latest.txt

This recovers logs after a trial; it is not a live USB gadget console. A live
stream still requires an Exynos PHY bring-up and DWC3 endpoint implementation.
No disk log writes are performed by the phone.

For the first kernel, leave all roots and MMIO probes disabled. A wait for
root is expected; no USERDATA writes or iOS GUI is part of that checkpoint.
Later work: S8 DECON/DSIM scanout, bounded UFS reads, rootfs compatibility,
then touch/keys/PMIC. S7 clock, GPU and Wi-Fi routines must not run on S8.

## Portable A03 updates (2026-11-16)

See [dreamlte-a03-port.md](dreamlte-a03-port.md) for the pinned A03 review,
complete feature/dependency map, host verification and optional boot modes.
The profile now stages133 patches including S8 overlays0205-0212. This adds
portable diagnostics and scoped compatibility; S8 storage/display/USB still
require their own device bring-up. The original CI43434858911 succeeded.
