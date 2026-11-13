# Galaxy A03 SM-A035G — active bring-up

## 2026-11-13: branch and first on-device diagnostic

- Branch `a03-bringup`, based on `64b1067` (`dreamlte-bringup`).
- Connected phone identified through ADB as **SM-A035G**, device `a03`,
  product `a03nseea`, platform `ums9230`, hardware `ums9230_25c10`.
- `/proc/cpuinfo` reports UNISOC T606: six Cortex-A55 (part `0xd05`,
  variant 2, revision 0) and two Cortex-A75 (part `0xd0a`, variant 3,
  revision 1). This is a different SoC from every Samsung donor here.
- Android 13 user build; security patch 2024-01-01; kernel
  `4.14.199-27193134-abA035GXXS5CXA1`.
- Boot state properties: `ro.boot.flash.locked=0`, vbmeta `unlocked`,
  verified boot `orange`. These are Android-reported properties, not a
  demonstrated custom-image acceptance result.
- ADB shell is uid 2000. `adb root` is refused by the production build;
  `su` is absent. BOOT, raw FDT, device-tree properties, pstore and block
  sizes are permission-denied. No usable backup obtained.

## First code actually running on the A03

`shim/a03` builds a freestanding, statically linked AArch64 **Android EL0**
diagnostic with Clang/LLD and no libc/NDK dependency. Built with warnings
as errors, pushed to `/data/local/tmp/a03-el0-probe`, and executed via ADB.
It returned exit status 0 and:

```text
CNTFRQ_EL0=0x00000000018cba80
MIDR_EL1_LINUX_VIEW=0x00000000412fd050
ID_AA64MMFR0_EL1_LINUX_VIEW=0x00000000ff000000
A03_EL0_PROBE_OK
```

Timer frequency is 26,000,000 Hz. The virtual counter was readable. MIDR
identifies the executing A55. Linux's EL0 MMFR0 view masks the granule
fields; **do not interpret it as physical 4K/16K support**. Boot exception
level, raw MMFR0, GIC, PSCI and usable RAM remain unverified.

This establishes the local toolchain/ADB execution checkpoint only.
**No custom boot image, boot shim, XNU kernel or iOS runtime has run.**
No partitions were written, and no reboot was requested.

## Observed partition links — not write instructions

- BOOT: `/dev/block/mmcblk0p39`
- RECOVERY: `/dev/block/mmcblk0p40`
- DTBO: `/dev/block/mmcblk0p41`
- vendor_efs: p10; sec_efs: p11
- USERDATA: p55

Partition sizes and contents are not backed up or verified. Preserve all
partitions. Existing S8/S7/A5 BOOT flash permissions and packaging tools
do not establish an A03 image format or restore procedure.

## Next concrete checkpoint

1. Obtain the exact installed stock BOOT plus its DTB/DTBO and an applicable
   restore route, using privileged access or matching firmware. Keep all
   dumps/private evidence ignored. Do not unlock again or wipe the phone.
2. Inspect actual BOOT header/compression/signing, DT hardware layout and
   reserved memory. No Exynos display, reset, storage or GIC addresses.
3. Build and host-validate an A03 pre-Linux probe which returns to the
   original kernel, with a recoverable marker and register report.
4. Before a partition test, obtain explicit A03 BOOT-only authorization
   with the image and verified stock restore artifact ready to review.

Reproduction and scope: `docs/a03-bringup.md`. Ignored diagnostic output:
`backup/galaxy-a03-2026-11-13/diagnostics.json`.

## 2026-11-13: matching firmware and first BOOT flash

- User supplied stock firmware and a Magisk-patched AP archive under
  `/run/media/stoned/schrott/Handy/a03/`, authorized proceeding and stated
  that phone data is disposable. No wipe or non-BOOT write was needed.
- Installed PDA/bootloader `A035GXXS5CXA1` matches the supplied revision-5
  AP. Revision-8 firmware under `newer/` was not used.
- Extracted original and patched BOOT, DTB/DTBO and vbmeta into ignored
  `backup/galaxy-a03-2026-11-13/firmware/`. Stock BOOT is 67,108,864 bytes,
  SHA256 `4e58b96e4ef6e913f51bdcea4a34ef9787c4c23f85295ed050dc4bb736e852f0`.
- Patched BOOT is the same length, SHA256
  `94fa7c5347b00e49fe1dc60a4edae958ddd5dac9accdbcddbeb743b5215e9ce7`.
  Stock and Magisk kernel SHA256 both
  `1d1266f15bb8f0f1f9f501fc763c0c7451aa7cdc7db04693ea3d5d49c2646d90`.
- Android header v2, page 2048, raw ARM64 kernel 23,717,904 bytes,
  text offset 0x80000, declared memory size 0x1ac0000; original branch
  target offset 0x1200000. DTB component is an Android DT table with one
  FDT, not Samsung Exynos DTBH. BOOT carries an AVB footer.
- Prepared **BOOT-only** Odin tar files for patched and stock restore.
  Entered download mode via ADB. Odin4 1.2.1 transferred only boot.img,
  reached 100%, closed connection, exit 0. No AP-wide archive flashed.
  Heimdall is now available as `/usr/bin/heimdall`, version 2.2.2.
- Android returned, `sys.boot_completed=1`; Magisk 27 daemon and `su`
  appeared. Initial root request refused because manager was missing.
  Installed matching Magisk 27.0 APK from its upstream GitHub release.
  User confirmed successful boot and Magisk additional setup in progress.
  Root access and live partition backups remain pending that setup.
- No vbmeta/DTBO/recovery/EFS/NV/USERDATA writes and no custom pre-Linux
  probe yet. The supplied patched vbmeta has flags 3, stock flags 0;
  neither was flashed in this test.

### Stock DT evidence (not yet live DT verified)

- GICv3: distributor 0x10000000+0x20000; redistributors
  0x10040000+0x100000, stride 0x20000.
- PSCI compatible arm,psci-0.2, SMC conduit.
- Timer DT PPIs secure-phys 13, nonsecure-phys 14, virtual 11, hypervisor
  10; virtual INTID 27. Runtime IRQ delivery is untested.
- Template memory spans 0x80000000+0x200000000; bootloader may fix this
  for actual installed RAM. **Do not use it as verified usable RAM.**
- Numerous reserved ranges include modem, trusted OS, ramoops and DDR
  diagnostics. Choose any XNU memory window only after live-DT capture.

## 2026-11-13: first pre-Linux probe succeeded

- Magisk setup completed and user granted shell superuser access. Verified
  `uid=0`, SELinux context magisk. No vbmeta change was required.
- Pulled BOOT, recovery, vendor_efs, sec_efs, prodnv, l_fixnv1, l_fixnv2,
  DTBO and vbmeta into ignored `backup/galaxy-a03-2026-11-13/live/`.
  Every dump length and SHA256 matched its on-device block device;
  `manifest.json` records hashes. Live BOOT matched supplied Magisk image;
  live vbmeta matched stock flags-0 image. Binary transport needs
  `stty raw -echo` inside Magisk su, which otherwise allocated a PTY and
  expanded LF into CRLF. Initial corrupt host dumps were replaced and
  verified; no corrupted dump was flashed.
- Captured live FDT, dmesg, cmdline, iomem and mounts privately. Live RAM:
  0x80000000+0xfffff000 (4 GiB minus 4 KiB), not stock template's 8 GiB.
  Live initrd 0xa0000000..0xa01055fb. GICv3 agrees with stock DT.
- Added A03-specific pre-Linux shim and exact-base image builder. Probe
  appends 10,189 bytes at kernel offset 0x169e810, within the original
  declared 0x1ac0000 memory size; preserves original kernel except first
  branch, ramdisk and Android DT-table bytes. Repairs legacy boot ID and
  moves stale AVB block/footer. No Exynos wrapper, MMIO or storage driver.
- Probe image `shim/a03/out/a03-boot-probe-0001.img`, 67,108,864 bytes,
  SHA256 `a5e829e54b857c250ad1e594c294635313ad6e13e7cf303fe922598dabb727b0`.
  Written to BOOT p39 using root ADB, full readback hash matched, rebooted.
- All six markers recovered from `/proc/cmdline` after Android returned:

```text
a03m=0000000000101122
a03i=00000000412fd050
a03p=0000000081000000
a03e=0000000000000008
a03s=0000000030d00800
a03f=00000000018cba80
```

These establish raw MMFR0 0x101122 (4K and 16K translation granules
supported), Cortex-A55 r2p0, MPIDR 0x81000000, **entry at EL2**,
SCTLR_EL1 0x30d00800 (EL1 MMU disabled) and timer frequency 26 MHz.
SCTLR_EL2 was not sampled; do not infer its entire state from SCTLR_EL1.
User physically confirmed Android lock/home screen; Android boot-complete
later read 1. This is custom pre-Linux code execution, **not XNU boot**.

- Restored known-working Magisk BOOT and independently verified readback
  SHA256 `94fa7c5347b00e49fe1dc60a4edae958ddd5dac9accdbcddbeb743b5215e9ce7`.
  Requested a clean reboot after restore. Recovery/EFS/NV and all other
  partitions were not written. Stock BOOT remains available for Odin or
  `heimdall flash --boot <stock-boot.img>` (PIT name is lowercase `boot`).
- User is cloning A03 kernel source into `android_kernel_samsung_a03/`;
  keep the separate source checkout ignored and do not stage it.

### Next step after first probe

Inspect cloned kernel boot entry and live reserved memory, then verify
EL2-to-EL1 transition, timer and GICv3 interrupt delivery with a returning
probe. XNU expects EL1; do not jump directly from the observed EL2. No
display controller writes or XNU memory window have been verified yet.
