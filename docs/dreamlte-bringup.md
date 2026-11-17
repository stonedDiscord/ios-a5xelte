# S8 adaptation from HEROLTE

The S7 donor already solves 4K XNU, ARMv8.0 without LSE, GICv2 and the
Samsung legacy BOOT wrapper. It does not supply an S8 hardware port.

Start with the latest entry in DREAMLTE_PROGRESS.md. BOOT test writes and
the converted IPSW root on existing USERDATA/sda24 are explicitly authorized.
The user prohibits restoring Android. Preserve GPT, RECOVERY, bootloaders,
EFS/CPEFS and all other partitions.

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
payload; never flash it. The loader halts on failure and logs in RAM.
Candidate0214 adds loader, early XNU and normal serial framebuffer output;
its physical scanout remains unverified. Do not restore Android for RAM-log
recovery. A live USB connection still requires verification of Exynos PHY
initialization and DWC3 endpoint/DMA operation. See dreamlte-usb.md.

The current candidate uses dreamlteusb=2 for guarded firmware-state takeover.
A wait for root is expected because the S8 UFS driver is unfinished. Root
conversion/deployment does not establish runtime mounting or an iOS GUI.
Later work: verified DECON/DSIM scanout, bounded UFS reads, rootfs compatibility,
then touch/keys/PMIC. S7 clock, GPU and Wi-Fi routines must not run on S8.

## Portable A03 updates (2026-11-16)

See [dreamlte-a03-port.md](dreamlte-a03-port.md) for the pinned A03 review,
complete feature/dependency map, host verification and optional boot modes.
The profile now stages135 patches including S8 overlays0205-0214. This adds
portable diagnostics and scoped compatibility; S8 storage/display/USB still
require their own device bring-up. The original CI43434858911 succeeded.
