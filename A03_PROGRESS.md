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
  Clean reboot after restore verified: ADB/root returned, readback hash
  matched, probe markers absent, `sys.boot_completed=1`, bootanim stopped.
  Recovery/EFS/NV and all other
  partitions were not written. Stock BOOT remains available for Odin or
  `heimdall flash --boot <stock-boot.img>` (PIT name is lowercase `boot`).
- User is cloning A03 kernel source into `android_kernel_samsung_a03/`;
  keep the separate source checkout ignored and do not stage it.
- Clone completed at `b48e9ddfd73a` with clean status. Read-only inspection
  of `arch/arm64/kernel/head.S` confirms `stext` calls `el2_setup`, whose
  non-VHE path initializes HCR_EL2 and timer access before entering EL1.
  The source was not changed or included in the parent commit.

### Next step after first probe

Inspect cloned kernel boot entry and live reserved memory, then verify
EL2-to-EL1 transition, timer and GICv3 interrupt delivery with a returning
probe. XNU expects EL1; do not jump directly from the observed EL2. No
display controller writes or XNU memory window have been verified yet.

## 2026-11-13: native 16 KiB donor direction

User proposed using a richer community fork now that the boot A55's raw
MMFR0 confirms 16 KiB support. Adopt native 16 KiB for initial XNU work,
SWEET's GICv3 core with reviewed Topaz generic integration improvements,
instead of continuing the HEROLTE/A5XELTE 4 KiB workaround.

Pinned donor comparison, source URLs and exclusions are recorded in
`docs/a03-donor-selection.md`. Topaz is XNU 8796/iOS 16 too, and its
optional `TOPAZ_4K` path must stay disabled for this direction. Its
Qualcomm/Adreno hardware drivers are not A03 drivers. Actual 16 KiB MMU
operation, other CPUs, EL1 transition and IRQs still need device tests.
This records the target architecture; no A03 XNU build profile or
replacement build has yet been implemented.

## 2026-11-13: EL1/16 KiB round-trip probe 0002 failed to return

- Added opt-in --mmu16k and --elf diagnostic output to the exact A03 image
  builder. Temporary EL2/EL1 vectors, saved registers, masked EL1 entry
  and HVC return; intended mapping uses aligned 16 KiB tables, Normal
  non-cacheable probe RAM, alias read/write and an unmapped-address check.
  No GIC, timer control or peripheral MMIO is written.
- Host build passed warnings-as-errors, linked ELF relocation, entry,
  table/vector alignment, memory bound and kernel/ramdisk/DT preservation
  checks. Preliminary section alignment corrected before device write.
  Candidates 0002/0002b/0002c were host-only; only 0002d was flashed.
- BOOT p39 written/readback verified with 0002d SHA256
  5b6f46f7b23bf813fe558d5717257b3d250067bf8bfbe3ca35300de84b7e6b3e.
- ADB did not return after reboot. User reports bootlooping with brief
  early text described as prtval and whatnot. No exact panic text or
  recovered markers. EL1/16 KiB execution is unproven; root cause unknown.
  Distinguish probe failure from Linux failure after return. CPU capability
  from 0001 remains valid; actual 16 KiB translation is not established.
- Manual Download mode requested to restore verified Magisk BOOT. Restore
  pending USB enumeration; no further experiment until Android is recovered.

### Recovery and root cause of the 0002 bootloop

- User entered stock recovery, then Download mode. Heimdall 2.2.2
  restored only boot from the verified Magisk BOOT: upload 100%, success,
  exit 0, reboot. ADB/root returned and BOOT SHA256 matched 94fa7c53...
  Full boot-complete was subsequently 1 before the next test.
- Preserved dmesg-ramoops-0 and console-ramoops-0 privately under
  live/probe-0002-pstore. Panic was Linux init at 1.69 seconds:
  libfs_avb reported Unknown hash algorithm (empty), then failed to create
  AvbVerifier, mount /system, and panicked attempting to kill init.
- Root cause: the probe reporter replaced androidboot.vbmeta.hash_alg
  (and two other vbmeta arguments) with markers. This was an agent error
  in diagnostic output selection, not evidence of failed 16 KiB hardware.
  Linux did execute after the probe. Mapping success still unverified
  until markers are recovered in the corrected test.
- User explicitly authorized another boot attempt without requiring a
  working phone between each test. Keep writes scoped to BOOT.

### Corrected probe 0003

- --mmu16k now reuses only the six in-place argument slots already tested
  in 0001. AVB, verity and mount arguments are preserved. Host execution
  of the reporter on the saved live FDT with a stubbed EL1 test confirmed
  marker insertion and preservation of essential Android arguments.
- Candidate 0003 SHA256
  39519780c9ceedaaeb922a7921085a331ba5e8f229d0460acc7e10b45d217b72.
  Built, checked alignment, flashed BOOT p39, verified complete readback
  hash and rebooted. Markers now t=status, l=CurrentEL, q=TCR_EL1,
  u=SCTLR_EL1 while enabled, a=alias PAR_EL1, y=EL2 return ESR.
  Device result: **PASS**, all six markers recovered, Android boot-complete
  1 and boot animation stopped. BOOT readback still matches candidate.

```text
a03t=0000000000016384
a03l=0000000000000004
a03q=00000001409cb01c
a03u=0000000030d00801
a03a=4400000081734b00
a03y=000000005a000a03
```

- t=0x16384 is emitted only after alias read, alias write visible through
  identity mapping, and an unmapped VA AT fault check succeed.
- l=4 confirms execution at EL1; TCR 0x1409cb01c gives TG0=2 (16 KiB),
  T0SZ=28 (36-bit VA, L2 start). SCTLR_EL1 M=1, C=I=0 during the test.
- PAR alias output maps to the test word PA 0x81734000 with Normal NC
  attributes. Probe identity RAM was 0x8171c000..0x81738000; alias word
  VA 0x41734000. Only probe pages were mapped.
- ESR_EL2 0x5a000a03 is HVC64 with the expected immediate 0xa03, proving
  the intended return to EL2. Register state restored before Linux entry.
- Actual 16 KiB MMU operation and EL2->EL1->EL2 round trip now verified
  on the boot A55. Caches, GIC/timer interrupts, other CPUs and XNU remain
  untested. Raw support and mapping operation are separate checkpoints.
- Current on-phone BOOT is **successful probe 0003**, retaining Magisk,
  not the unmodified Magisk image. User authorizes ongoing test BOOTs.
  No additional restore reboot needed for this working checkpoint.
- Added tools/a03-test-reporter.py: runs the compiled C reporter against
  private live FDT with stub hardware results; asserts only six approved
  slots change, with all AVB and remaining bytes preserved. Passed.

Next: verify GICv3 system-register access and virtual timer IRQ delivery
at EL1 with a bounded returning probe, then build an A03 native-16K XNU
profile. Do not infer XNU boot or all-core compatibility from 0003.

## 2026-11-13: native-16K build profile and runner correction

- c179b90 stages pinned SWEET core patches 0001..0018 plus newer iig
  compatibility. Patches apply cleanly to xnu-8796.141.3; no kernel built yet.
- 9178d8a replaced retired macOS 14 with macos-15-intel. GitHub's
  runner-images issue 15226 confirms GitHub macOS 14 retirement on
  November 2, 2026. Current README lists macos-15-intel as x64 and
  macos-15 as arm64; host architecture does not select kernel architecture.
- Explicitly set ARCH_CONFIG=ARM64 and check the SWEET kernel artifact
  with lipo for plain arm64. The pinned build script already defaults to
  ARM64; SWEET's machine patch selects ARMv8.2 without arm64e/PAC.
- Add supported macos-26-intel, macos-26 and xcode-27 dispatch choices.
  Alternative runners remain untested. Keep macos-15-intel as default.
- Fix Xcode discovery under pipefail: absence of an Xcode_15 glob could
  otherwise abort before the fallback. Workflow YAML, every embedded
  shell step's syntax and Xcode Python syntax passed local validation.
- Run 43485104681 remained queued before replacement with this fix.
  Local XNU loader/ADT files are still uncommitted work in progress,
  not a validated flash candidate. Phone remains at successful probe 0003.

- Follow-up workflow fix committed as 3cea933 and pushed. Dispatched
  run 43485850320 on macos-15-intel for DEVELOPMENT ARM64 SWEET/a03;
  awaiting runner allocation. No device write in this CI correction.

## 2026-11-13: first successful A03 XNU build and packaged trial

- GitHub Actions run 43485850320 succeeded on macos-15-intel at
  19:06:42 UTC, source 3cea933, Xcode 16.0. Downloaded kernel is Mach-O
  plain arm64 (CPU subtype 0), SHA256
  91d3c7c39571f9403cf15959c4ea2c6bfb949f1818f168d502bc887c0f817dcf.
  This is build success, not device execution or an iOS runtime result.
- Added A03 EL2-to-EL1 wrapper, bounded SWEETXNU segment loader, single-A55
  ADT and exact-base Android BOOT v2 packer. No storage/USB/display-controller
  driver. Logo RAM writes use 0x9e000000, 720x1600, stride 2880; scanout and
  32-bit pixel interpretation remain unverified (stock logo_bpix says 24).
- Corrected proposed RAM window to 0x102000000+0x10000000: 32 MiB aligned
  for XNU bootstrap L2 blocks, above debug-reserved page 0x100000000 and
  within live RAM. The earlier 0x100200000 proposal was not block aligned.
- Loader compiled with warnings as errors, no linked relocations; explicit
  padding matches linker payload boundary. Payload bounds/segment overlap,
  entry, bootargs layout and BOOT ramdisk/DT preservation checks passed.
  Host checks verify Mach-O architecture, ADT single CPU and timer INTID27.
- Candidate shim/a03/out/a03-xnu-0001.img: 64 MiB SHA256
  2313ba806a818748cb5f7b565d52f395270b0b864e07c2334441597e184284fe.
  XNU entry PA 0x10346b488, ADT PA 0x103ff4000. No iOS rootfs attached;
  this trial targets early XNU only. Stale AVB signature needs unlocked boot.
- Before flash: Android boot-complete 1, root works, BOOT resolves to p39,
  current hash matches successful probe 0003. BOOT-only flash pending.

### Trial 0001 written and reboot requested

- Flashed only /dev/block/by-name/boot, verified resolved p39 and exact
  64 MiB size, model and previous probe hash before writing. Uploaded and
  full post-write partition hashes match candidate 2313ba80...84284fe.
- ADB reboot requested successfully. Physical screen report pending;
  no evidence yet of XNU entry, MMU startup or iOS runtime. Recovery,
  bootloaders, vbmeta, EFS/NV and USERDATA were not written.
- ADB absent at the first check. This kernel has no A03 USB driver;
  absent ADB does not distinguish kernel progress from a hang.

### Trial 0001 physical display report: XNU panic path reached

- User transcribed the panic.apple.com report footer, then the exact line
  "handshake structure not initialized" from the phone screen.
- Source match: osfmk/kdp/output_stages/out_shmem.c, panic_spin_shmcon(),
  emits the latter when hwsd_info is NULL. It is a secondary panic-time
  hardware shared-memory debugger diagnostic, not the original panic cause.
- This is user-reported visible XNU panic output after trial 0001, distinct
  from host build success. It establishes XNU execution/display progress;
  no saved kernel log, original panic reason, IRQ success or iOS runtime
  is established. Requested earlier panic(cpu...)/SWEET EARLY PANIC text.
- Keep the current screen intact while reading it. No second BOOT trial
  has been written and no speculative debugger-handshake fix applied.

### Trial 0001 panic symbolicated: missing SHA-1 provider

- User transcribed: panic(cpu 0 caller 0xfffffe0007a3caec), Kernel data
  abort at PC 0xfffffe000790b958. Exact unstripped trial kernel resolves
  caller to sleh_synchronous_sp1 and fault PC to SHA1Init/sha1_init+0x34.
- Disassembly loads g_crypto_funcs from 0xfffffe000722ea18 into x22,
  then faults at ldr x20,[x22,#0x28], the ccsha1_di field. No corecrypto
  kext/provider is installed in this minimal profile. This strongly
  identifies the missing crypto dispatch table; FAR/x22 not transcribed.
- Extend pinned donor selection with portable crypto patches 0020, 0023,
  0027, 0032, 0033, plus 0020-stage-bearssl.sh. SHA-1 fix 0032 depends on
  earlier crypto build rules; remaining selected patches supply legacy
  AES/MD5/SHA-256/384/512 without importing Qualcomm peripheral drivers.
- All five additional patches apply cleanly to the already-patched XNU
  tree. BearSSL staging script successfully fetched its pinned immutable
  7bea48e5e850ab4cafbe68d3765cdaba13a86d6f source locally. Workflow now
  copies this required script along with A03 patches. Rebuild pending.

- Crypto fix committed/pushed be14062; replacement CI run 43491007355
  is in progress on macos-15-intel. Host test compiled the exact donor
  SHA-1 wrapper/context with pinned BearSSL: empty, abc, million-a and
  multi-block binary vectors across chunk lengths 1/63/64/65/4096 all
  matched Python hashlib (20 tests). This validates hash behavior, not
  kernel integration; the CI build/device result remain pending.
- Requested manual Download mode while building, because trial 0001 has
  no ADB driver. No subsequent partition write yet.

### GitHub runner provisioning stalled; switch runner pool

- User reports crypto build 43491007355 never started and cannot cancel.
  API confirms only Set up job in progress since 19:18:53 UTC; no checkout,
  dependency step or compilation. Previous handoff calling it in progress
  described workflow status, not compiler activity. No corrected artifact.
- At 19:55:18 UTC, POST force-cancel returned HTTP 202 Accepted. Immediate
  follow-up still reported in_progress; cancellation not yet confirmed.
  Logs endpoint returned 404 (no available job logs).
- Include runner label in workflow concurrency group so the wedged Intel
  runner cannot hold the alternate ARM pool behind the same branch lock.
  Retry on macos-15 (arm64 host), retaining explicit ARM64 kernel target.
  Both runner labels are supported; this is a host provisioning workaround.

- Runner isolation committed a93ce7e; new run 43496849574 dispatched on
  macos-15 ARM64. User requests starting a new run rather than further
  cancellation attempts. Leave old run alone; new group is independent.

### macOS 15 runner allocation failed; macOS 26 ARM retry

- Run 43496849574 completed failure: job was not acquired by hosted runner
  after multiple attempts, with no steps executed. This is provisioning
  failure, not a kernel compiler error. Earlier 43491007355 now cancelled.
- Dispatched 43499857623 on macos-26 (ARM64 host), retaining ARM64 SWEET
  target and portable crypto fix. Runner/toolchain compatibility remains
  unverified until setup and compilation execute. User prefers macOS 26.
- GitHub status API listed Actions operational when checked; that does not
  establish runner pool availability for this repository. No phone writes.

- At user request, dispatched fresh run 43500930431 on macos-15-intel
  from fc640b7 with A03 portable crypto fix, DEVELOPMENT ARM64 SWEET.
  macOS 26 run was not being acquired; no cancellation requested.

## 2026-11-13: portable-crypto kernel built; trial 0002 flash started

- Run 43500930431 succeeded on macos-15-intel at 20:36:49 UTC, source
  fc640b7. Downloaded plain arm64 kernel SHA256
  94247210aa2c06b2e20f14342e12eb2a7a384d98295d2e73c262403b319a6e0d
  matches CI SHA256SUMS. Disassembly confirms SHA1Init calls br_sha1_init;
  the trial-0001 null crypto table access is absent in this function.
- Packaged first corrected candidate shim/a03/out/a03-xnu-0002.img,
  64 MiB SHA256
  4819988d9641c49008a19c1d47ae8eddc5456ff349c1b8a3b8b94037955b77b8.
  XNU entry PA 0x10346b488; ADT PA 0x103ff8000. Same single-CPU 16K RAM
  window/loader and no rootfs. Packer architecture, segment/entry bounds,
  bootargs layout and original ramdisk/DT preservation checks passed.
- User confirmed Download mode. Heimdall detected USB 04e8:685d. Invoked
  only heimdall flash --boot <trial0002>; protocol initialized, session
  beginning. Transfer/completion and physical screen report still pending.

### Trial 0002 flash blocked before transfer

- First Heimdall invocation initialized protocol, then ended exit 1 after
  Beginning session; no PIT retrieval, BOOT upload or success message.
- Device still detected in Download mode. One verbose retry exited 1:
  Failed to receive handshake response, result -7 (timeout), protocol
  initialization failed. No image transfer began on either invocation.
- Requested physical reset/re-entry into Download mode to establish a
  fresh session. Do not claim candidate 0002 installed. Trial 0001 remains
  the last successfully written BOOT; recovery and other partitions intact.

### Trial 0002 BOOT flash completed after fresh Download session

- User reset/re-entered Download mode. Same candidate SHA256
  4819988d9641c49008a19c1d47ae8eddc5456ff349c1b8a3b8b94037955b77b8
  verified immediately before flash. Heimdall session and PIT retrieval
  succeeded; uploaded only boot to 100%, reported boot upload successful,
  ended session, rebooted device, exit 0. No full partition readback is
  available through this transport; distinguish upload acknowledgement
  from independent readback verification.
- Trial 0002 is now the last successfully uploaded BOOT. User screen
  report requested; crypto fix/runtime progress remains unverified until
  observed. Recovery, bootloaders, EFS/NV and USERDATA were not written.
