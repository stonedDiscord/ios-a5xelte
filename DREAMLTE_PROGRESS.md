# DREAMLTE / Galaxy S8 SM-G950F — active handoff

## 2026-11-13: base changed to HEROLTE

- User requested origin https://github.com/wardevsa/ios-a5xelte.git,
  branch herolte. Origin changed; local dreamlte-bringup branch based on
  ff2c55e19f1a66fb811ed85bd17a21de9fc727bf. Old main and S8 probe commits
  a50b31a/d857f24 remain locally. Donor NOTES.md is historical.
- The requested A8/iOS 12 investigation is superseded for immediate kernel
  bring-up by this explicit repository choice. HEROLTE uses XNU 8796 / iOS
  16 with a 4K kernel; do not claim an iOS 12 image has been prepared.
- Read HEROLTE_PROGRESS.md and docs/herolte-bringup.md for donor behavior,
  but do not apply S7 addresses or its userdata approval to the S8.

## Verified S8 device evidence

Android: LineageOS 15 userdebug, Linux 4.4.302-gfe8224c5a0ac-dirty.
adb root works; kexec_load returned ENOSYS (38). User authorized BOOT test
flashing. Preserve RECOVERY, bootloader, EFS/CPEFS and USERDATA.

The pre-Linux probe was booted twice, returning to Android both times.
Probe 0001 flashed with Heimdall 2.2.2; expanded 0002 via root ADB BOOT write.
0002 readback SHA256:
408a9b18ed9db01063e1a237d747146c0f7b17b593270642de9d159aa5f9a7a6

Recovered through /proc/cmdline:
- MIDR = 0x410fd034: Cortex-A53 r0p4.
- MPIDR = 0x80000100: affinity 0x100.
- CurrentEL = 4: EL1.
- SCTLR_EL1 = 0x30c5183e: MMU off.
- CNTFRQ_EL0 = 0: use verified DT clock 26 MHz.
- MMFR0 = 0x1122: 4K supported; 16K unsupported on boot CPU.

Live DT: main GICv2 GICD 0x10201000, GICC 0x10202000; virtual timer PPI11
(INTID27). PSCI SMC. RAM upper bank 0x880000000+0x80000000 has no live-DT
reserved-memory entry. Initial XNU window limited to first 512 MiB.

S8 framebuffer is only a candidate: cmdline 0xcc000000, Android fb0
1440x2960, stride5760. DECON_F=0x12860000. **No custom scanout verified.**
The loader is headless and XNU early console goes to RAM scratch rather
than making unverified S7 display writes.

## Backups / restore

Ignored backup/galaxy-s8-2026-11-13 contains original boot/recovery/efs/cpefs
images, verified SHA256SUMS, PIT and private device logs. Ignored dtb/
contains live trees. Never add these to git.
- BOOT /dev/block/sda7, 41943040 bytes, PIT ID7.
  SHA256 71fb593969288f3a5a5dc6c4c4da35a53b045650cc293c6e8e4028ac3a7982a5
- RECOVERY /dev/block/sda8, 48234496 bytes, PIT ID8.
  SHA256 a0db11153d9136648358f51e205943578263d0672932d22c8bd40e829fcbfe68
- USERDATA /dev/block/sda24, untouched.

Original BOOT restored and hash matched after 0002; Android reboot requested.
Restore fallback: download mode, heimdall flash --BOOT <verified original>.
Samsung download mode uses VolumeDown+Bixby+Power (not S7 Home).

## New deliverables / checks

- shim/s8: known-working pre-Linux handoff probe and register reporting.
- shim/dreamlte: HEROLTE-derived XNU loader; Clang/LLD build passed,
  PC-relative objects, valid Image header. **Not device-tested.**
  Log page 0x8afff000; early console RAM sink 0x8b000000..0x8c1fffff;
  both outside initrd/FDT and upper-bank XNU RAM, with no DT reservations.
  Failure halts; no unverified PMU recovery sequence is executed.
- tools/mkadt_dreamlte.py: one A53, S8 GIC, upper 512 MiB, no UFS/display/
  GPU/touch/PMIC/Wi-Fi nodes; serialized and parsed assertions passed.
- tools/herolte-pack-boot.py: explicit --chip 8895 added, default remains
  8890; S8 DTBH and original ramdisk preserved byte-for-byte in packing test.
- xnu/dreamlte/0204-dreamlte-early-board.patch: modifies early display sink
  and marker addresses after 0203; dry-run passed on reconstructed headers.
- tools/dreamlte-build-profile.py: 127 patches (donor through 0203 + S8
  overlay). Excludes later S7 MMIO drivers. Build uses MACHINE_CONFIG=HEROLTE.
- Workflow xnu adds board_profile=dreamlte. This is kernel-only bring-up;
  no compatible rootfs assembled, no XNU boot yet, no GUI claim.

GitHub account authenticated, but upstream permission READ. Creating an
account fork for the CI build while preserving origin. Record exact CI IDs,
compile results, hardware observations and restore results below.
