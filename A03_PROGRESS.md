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

### Trial 0002 user-transcribed startup output

User reports the following visible lines (no new panic reason supplied):

    Error!! gPanicBase is still not initialized
    kdp_core zlib memory 0x8000
    Serial requested
    iBoot version: a03-shim
    "name" not a kext
    "AAPL,phandle" not a kext
    calling mpo_policy_init for vnguard
    Security policy loaded: Guarded vnode policy

- Source debug_log_init() in osfmk/kern/debug.c prints the gPanicBase
  warning and returns when no panic buffer exists; it does not panic.
- OSKext::createExcludeListFromBooterData() logs non-kext ADT properties
  and continues its loop. These messages alone do not identify a fault.
- security/mac_base.c prints Security policy loaded after the policy init
  callback completes. This confirms visible startup/policy progress in
  trial 0002; no new SHA1Init panic reported. Exact final boot stage,
  IRQ operation, root wait or a later panic remains unverified.
- Requested whether display stops there or additional lines follow.
  No speculative warning-suppression patch or additional flash performed.

### Trial 0002 stalls at policy output; use existing startup trace

- User confirms screen stays at Security policy loaded: Guarded vnode
  policy. No later panic or root-wait output reported. Last displayed line
  does not identify the exact stalled function.
- Source kernel_bootstrap_thread() registers vnguard after enabling
  interrupts, then proceeds to DTrace, trust-cache init and lockdown.
  These steps cannot be distinguished from this transcription alone.
- Found existing tracing: startup_debug=1 enables kernel bootstrap and
  initializer logs. DEVELOPMENT requires -enable_kprintf_spam to actually
  emit kprintf output; previous trial omitted this. -show_pointers retains
  useful initializer addresses for symbolication.
- Packaged host-only trial 0003-trace from SAME corrected kernel and ADT;
  only command-line changes: -enable_kprintf_spam startup_debug=1
  -show_pointers. No additional source patch or CI required.
  Image shim/a03/out/a03-xnu-0003-trace.img, SHA256
  14bcd388383700ed4818e6c6f80de5a8ddb15b7d8746e3996a7d29fec58ec98f.
  Host packer checks passed. Requested fresh Download mode; not flashed yet.

### Trial 0003-trace successfully uploaded

- User confirmed fresh Download session. Verified host candidate hash
  14bcd388383700ed4818e6c6f80de5a8ddb15b7d8746e3996a7d29fec58ec98f;
  Heimdall retrieved PIT, uploaded only boot to 100%, reported successful,
  rebooted, exit 0. Independent partition readback unavailable.
- Current BOOT is trial 0003-trace. Requested final 5-10 physical display
  lines, particularly bootstrap step/initializer address or panic. Runtime
  outcome remains pending. No other partition write.

### Trial 0003-trace progresses past policy and trust-cache initialization

User transcribed (minor spelling differences preserved in original chat):

    kernel_bootstrap: mac_policy_initmatch
    kernel_bootstrap: vnguard_policiy_init
    calling mpo_policy_init for vnguard
    Security policy loaded: Guarded vnode policy (vnguard)
    kernel_bootstrap: dtrace_early_init
    kernel_bootstrap: trust_cache_init
    SWEET: trust caches unavailable (Image4/AMFI not installed)
    kernel_startup_initialize_upto: reached phas

- Existing trace flags work. Earlier policy line was not the exact stop:
  subsequent DTrace and trust-cache paths were reached. Missing trust-cache
  provider is explicitly handled by selected patch 0015; this message does
  not alone imply a panic or need to bypass security initialization.
- In startup.c the reached-phase message after trust-cache init corresponds
  to kernel_startup_initialize_upto(STARTUP_SUB_LOCKDOWN), whose enum is
  unsigned ~0u and printed with %d (expected -1). The user has not yet
  supplied the end of the line, so exact completion remains unconfirmed.
- Next normal checkpoints are OSKextRemoveKextBootstrap, machine_lockdown,
  XNUPOST and PE_lockdown_iokit. Requested full final line/continuations
  and any later text before choosing another code change. Do not infer
  which call hangs from a truncated console string. Current BOOT unchanged.

### Trial 0003-trace final line confirmed physically incomplete

- User confirms final line is literally kernel_startup_initialize_upto:
  reached phas[e], with the e obscured by cracked glass and no continuation
  or text below. User entered a fresh Download session. Do not keep asking
  for an absent phase number; it was not merely omitted in transcription.
- Prepare A03 patch 0084: polling serial_putc checkpoints without kprintf
  formatting/lock/os_log path around lockdown callbacks, kext bootstrap
  cleanup, machine lockdown, XNUPOST and IOKit matching. Replaces the
  lockdown-phase formatted completion line with a short polling marker;
  after lockdown phase use polling bootstrap labels as well. Interrupt
  mask state saved/restored around each marker. Does not skip startup calls.
- The literal partial string suggests logging stall but is not proof of
  one; diagnostic bypass changes logging/timing and must be assessed on
  device. Patch applied locally, profile stages it. New CI build pending.
- Current phone in Download mode with trial 0003-trace last written. No
  additional BOOT flash yet; preserve recovery/EFS/NV/other partitions.

- Diagnostic patch committed/pushed ac2b362. New CI run 43507759809
  queued on macos-15-intel. Phone ready in Download; no diagnostic
  binary available yet and no additional flash performed.

### Trial 0004-poll: diagnostic kernel built and BOOT uploaded

- CI 43507759809 succeeded at 21:22:51 UTC (source ac2b362), plain arm64
  diagnostic kernel SHA256
  59cae8432f5664f083b771517eb3d1bebfe575ae9520b0a7b9136dc2a14fab41
  matches CI manifest. Checkpoint labels present; disassembly of
  a03_startup_checkpoint confirms polling serial_putc and interrupt state
  save/restore calls. Compiler unrolled the literal prefix into character
  calls, so searching for contiguous A03 STEP string alone was insufficient.
- Built shim/a03/out/a03-xnu-0004-poll.img with same native16K loader,
  ADT and trace flags. 64 MiB SHA256
  9328ed5ee0ac16d1449f15bd75e589586c468e19fa57750a7732a5d440999e23.
  XNU entry PA 0x10346c488, ADT PA 0x103ffc000. Packer checks passed.
- Phone remained in user-confirmed fresh Download mode. Host image hash
  rechecked; Heimdall retrieved PIT, uploaded boot to 100%, reported boot
  upload successful, rebooted device, exit 0. No independent readback.
- Current BOOT is trial 0004-poll. Requested final A03 STEP marker/panic
  or partial line from display. No runtime result yet; only BOOT written.

### Trial 0004-poll last marker: before LOCKDOWN callbacks

- User transcribed DTrace, trust-cache unavailable, then exactly
  A03 STEP before LOCKDOWN callbacks, with no later marker supplied.
- This brackets output but does not establish a failing callback: the
  marker helper still called ml_set_interrupts_enabled(enabled) after
  printing. Source shows that routine may run AST_URGENT scheduling before
  returning; the dispatcher itself has not yet been proven entered.
- Refine patch 0084: polling markers save/mask/restore DAIF directly,
  avoiding scheduling/debug paths in the helper; clear interrupt-mask
  timing accounting before restoring an originally enabled state, matching
  the slow-console exemption used in kprintf. This is diagnostic timing
  behavior only; it does not disable IRQs across startup callbacks.
- Add dispatcher-entry, current phase, cursor/end, callback address/argument
  and callback-return polling markers for LOCKDOWN. Avoid formatted
  initializer logging for that phase. No initializer or lockdown skipped.
- Extracted helper compiles locally for arm64-apple-darwin with warnings
  as errors; patch application and profile staging pass. Kernel integration
  and runtime still need CI/BOOT test. No new phone write yet.

- Refined diagnostic committed efb2834 and dispatched as CI 43511333915
  on macos-15-intel; awaiting corrected diagnostic artifact.

### Trial 0005-dispatch built and uploaded

- CI 43511333915 succeeded at 21:47:43 UTC (efb2834). Plain arm64
  kernel SHA256 matches artifact manifest:
  9113ca66a34808b5007fdf1ed54c318867b356d7ebb3422ccc19bb68db739f7c.
- Verified dispatcher/phase/callback labels. Disassembly confirms polling
  marker uses direct DAIF access and serial_putc, without a call to
  ml_set_interrupts_enabled. This validates code generation, not runtime.
- Packaged shim/a03/out/a03-xnu-0005-dispatch.img, 64 MiB SHA256
  1e47cec3f89e1d343f52cf3309993e480c568a6123437201bb36da8fff1829e2.
  Host packer checks passed, entry PA 0x10346c488, ADT PA 0x103ffc000.
- Download-mode USB detected. Host image hash rechecked before BOOT-only
  flash; Heimdall retrieved PIT, uploaded boot 100%, reported success,
  rebooted device, exit 0. No independent partition readback via Heimdall.
- Current BOOT is 0005-dispatch. Requested final A03 STEP lines/addresses
  or panic. Runtime outcome pending. No other partition written.

### Trial 0005-dispatch still stops at pre-dispatch marker

- User reports trust caches unavailable followed by A03 STEP before
  LOCKDOWN callbacks. No entered-dispatcher/phase/callback marker appears.
- Disassembly verifies marker returns after direct DAIF restore. The only
  post-output helper work is optional ml_spin_debug_clear_self, direct DAIF
  restoration and return. The clear helper only zeros current-thread debug
  timestamps; a pending interrupt upon restoration remains a hypothesis.
  This does not prove a callback, timer or IRQ is defective.
- Added opt-in a03_lockdown_mask=1 diagnostic (default false): saves DAIF,
  masks IRQ/FIQ before pre-dispatch marker, reports saved DAIF, read-only
  Group1 HPPIR and CNTV_CTL, executes the dispatcher with existing per-call
  markers, then restores original DAIF immediately after dispatcher and
  reports restoration. Does not skip callbacks or leave IRQs disabled for
  IOKit startup. Masking can change timing/semantics: diagnostic only.
- Patch reverse-application/profile staging pass. Phone USB currently in
  Download mode; no additional image written. Next kernel build pending.

- Opt-in diagnostic committed 0b21f6a, CI 43514823420 dispatched on
  macos-15-intel. Package its test with a03_lockdown_mask=1; otherwise
  default behavior stays unmasked. No candidate artifact/flash yet.

### Trial 0006-irq: scoped IRQ diagnostic built and uploaded

- CI 43514823420 succeeded (source 0b21f6a). Plain arm64 kernel SHA256
  b1700f3a60891a0cbd252c07fa89dff06ca0e49f453d860052737cddf699bde7
  matches CI manifest. Opt-in tunable and mask/register/restoration labels
  present. No device result inferred from host labels.
- Packaged shim/a03/out/a03-xnu-0006-irq.img with a03_lockdown_mask=1
  verified in payload command line. Same ADT and loader, 64 MiB SHA256
  593adffb16338a24f73cfa62d4827b1d2c048bd0f212232659d0fb003e4e276c.
  Host packer checks passed; entry 0x10346c488, ADT 0x103ffc000.
- Phone detected in Download mode. Host image hash rechecked; Heimdall
  retrieved PIT, uploaded boot to 100%, reported success, rebooted, exit 0.
  No independent partition readback. Only BOOT written.
- Current BOOT is trial 0006-irq. Requested register/callback/restoration
  markers, panic or partial line. Scoped mask experiment outcome pending.

### Trial 0006 display result and diagnostic formatter correction

- User reports exactly trust caches unavailable followed by
  A03 STEP diagnostic IRQ mask active. No saved DAIF or later line.
- Inspection of the built 0006 address formatter found automatic stack
  buffer zeroing using movi v0 and stp q0. That is unsafe for an early
  kernel diagnostic with FP/SIMD unavailable; a trap here is a hypothesis,
  not a recovered panic or proof of the original startup stall's cause.
- Earlier extracted-helper checks used -mgeneral-regs-only but the actual
  startup translation unit did not. Those checks missed this difference.
- Patch 0084 now streams label/hex digits directly to serial_putc without
  an automatic buffer. Its A03-only patch set also adds
  startup.o_CFLAGS_ADD += -mgeneral-regs-only to the kernel make template.
  No startup callback is skipped; the opt-in IRQ experiment is retained.
- Reverse patch validation and A03 profile staging passed. Extracted
  helpers compiled for arm64-apple-darwin at O2 with stack protection,
  automatic zero initialization and -mgeneral-regs-only: 147 instructions,
  no FP/SIMD register operands. Full CI artifact still requires inspection.
- Current device BOOT remains 0006-irq. No new phone write in this step.

- Fix 5a4cca7 pushed. CI 43517629744 acquired macos-15-intel and started. Inspect actual helper disassembly before packaging trial 0007.

### Trial 0007-nosimd: verified artifact, BOOT uploaded

- CI 43517629744 succeeded at source 5a4cca7, plain arm64. Kernel SHA256
  bc4431d7fb9727fb7d3cb750d1bf9f4a413bfae144ebf6075b58e6b8c9e3b386
  matches artifact SHA256SUMS.
- Actual Mach-O disassembly checked across complete symbol bounds:
  a03_startup_checkpoint 42 instructions; a03_startup_address 97 instructions.
  Both have DAIF operations, serial_putc calls and return, no FP/SIMD operands.
  This validates the corrected artifact, not the cause of the previous hang.
- Packaged shim/a03/out/a03-xnu-0007-nosimd.img, 64 MiB, SHA256
  82ca0e5aea66bb4f8892cdc232d041b34cabd0b619bae0ba420432fff0dd7603.
  Same ADT, loader and trace args including a03_lockdown_mask=1. Host bounds
  checks passed; entry PA 0x10346c488, ADT PA 0x103ffc000. No rootfs attached.
- User confirmed Download mode; USB detected 04e8:685d. Heimdall retrieved
  PIT, uploaded boot to 100%, reported successful upload, rebooted, exit 0.
  Only BOOT written; no independent partition readback.
- Current BOOT is 0007-nosimd. Requested final register/callback/panic or
  partial display lines. Physical runtime evidence pending.

### Trial 0007 physical display evidence: past lockdown into IOKit

- Inspected user photo IMG_20261113_233441_353.jpg directly (private local
  photo, not added to git). Physical bottom lines are trust caches unavailable and diagnostic IRQ
  mask active, as the user explicitly confirmed afterward. Later startup
  milestones are visible above them. No panic is visible in this photo.
- Visible diagnostics: saved DAIF ends in 0200 (upper digits partly
  obscured); pending Group1 00000000000003ff; virtual timer ctl
  0000000000000001; phase before 0000000000000010; cursor and end both
  fffffe0007c00a88. Thus this dispatcher invocation had no remaining entries.
- Visible completion markers: LOCKDOWN init callbacks done, after LOCKDOWN
  callbacks, restoring original IRQ mask, original IRQ mask restored,
  after kext bootstrap cleanup, after machine lockdown, after XNUPOST,
  after IOKit matching, SWEET starting device-tree platform expert, and
  SWEET platform expert registered. XNUPOST reports No POST boot-arg set;
  its return does not establish that the POST test suite ran.
- Trial 0007 demonstrably progresses past the former diagnostic stop. This
  is consistent with the SIMD correction, though the opt-in IRQ mask is
  still enabled and has not been independently removed for comparison.
- IOKit matching is asynchronous; platform-expert registration alone does
  not locate the next stall. The photo does not establish bsd_init/root
  mounting/userspace entry. Next diagnostic area: vm_set_restrictions,
  kperf_init_early and bsd_init entry, plus CPU service publication/waits.
- No additional build or phone write from this photo inspection. Current
  BOOT remains 0007-nosimd; no rootfs/storage/USB driver yet.

### User clarification: physical bottom lines remain the IRQ marker

- User confirms the bottom two lines remain SWEET trust caches unavailable
  and A03 STEP diagnostic IRQ mask active, beneath all other text. Preserve
  that observation separately from the inferred chronological order.
- Checked actual console source pexpert/arm/pe_serial.c: fbcon_newline
  advances row modulo fbcon_rows, clears that row AND the following row;
  it does not scroll. The photo shows a blank band after platform expert
  registered, then earlier startup output below. This fits a wrapped ring
  display, with platform registration most recently written in that pass.
- A single still photo cannot exclude a repeated boot or other output
  history. Do not call the physical bottom lines absent or assume an
  unobserved reset. The visible later milestones establish that a pass
  reached them, but the exact current execution location remains unproven.
- No build or flash performed for this clarification.

### Trial 0008 normal IRQ comparison and CPU/BSD diagnostic preparation

- Found actual 0007 SweetCPU::start code uses movi v0 and eight q0 stores
  to zero ml_processor_info_t before ml_processor_register. Same unsafe
  SIMD pattern as the corrected startup formatter. Not yet proven reached.
- kperf_init_early calls ml_wait_max_cpus, which sleeps until CPU driver
  publishes ml_set_max_cpus; no CPU completion marker appears in the photo.
  CPU registration/codegen is a concrete next suspect, not a proven fault.
- Added A03-only patch 0085: general-register codegen for SweetCPU.cpo,
  kperf.o and bsd_init.o, polling markers for CPU identity/registration,
  processor_start/SGI test/max-CPU publication, VM/kperf/BSD entry and BSD
  initialization stages. No CPU/interrupt tests or startup waits bypassed.
  Patch reverse application/profile staging pass; full compile pending.
- While preparing CI, packaged existing verified 0007 kernel without
  a03_lockdown_mask, leaving its default false. Trial 0008-unmasked SHA256
  998cf4de4d0f8d35c8e1ed5547a3da54d50ce23b9d1e0921425d938151ee2b81.
  Same ADT/loader/trace args otherwise, host bounds checks passed.
- User put phone into Download mode; Heimdall retrieved PIT, uploaded boot
  100%, reported success, rebooted, exit 0. Only BOOT written, no independent
  readback. Current BOOT 0008-unmasked; screen result pending.
- Route to userspace: establish CPU/timer scheduling and BSD startup;
  use RAM-backed mockfs/static test init to prove PID1/syscalls first;
  then filesystem and actual iOS userspace/display dependencies. Test init
  is not iOS SpringBoard. Existing tools/mkinit.py and sweet-init.S reusable.

- CPU/BSD patch committed f5236cf; CI 43521738983 acquired runner and is in progress. Built private static arm64 test init (16635 bytes), SHA256 f5de3714ff95e6a3b9ece30723f677de0f3f74ec5eb985a00c5ae872f0ac9bf1; not attached/flashed/executed.

- User reports trial 0008 reaches platform expert registered followed by two newlines. Normal IRQ masking thus reaches the same visible milestone as 0007; no need established for scoped masking. CPU/BSD CI remains in Build. No further phone write.

### 2026-11-14: trial 0009 CPU diagnostic uploaded; BSD build flag corrected

- CI 43521738983 passed at f5236cf. Plain arm64 kernel SHA256
  5709f594f7f7129d27ff07767d5e74a82071e59a5d5aad6157559599ef8fcf31
  matches artifact manifest. Actual complete-symbol checks found no SIMD in
  checkpoint/address (42/97 instructions), SweetCPU::start/initCPU (200/65),
  and kperf_init_early (32). CPU/BSD diagnostic labels present.
- Artifact inspection caught that bsd_init STILL uses SIMD: its object flag
  was incorrectly placed in osfmk's make template; BSD uses a separate one.
  Do not claim BSD codegen fixed in this artifact. Added profile patch 0086
  moving that flag into bsd/conf/Makefile.template. Reverse patch check and
  profile staging pass; rebuilt artifact verification pending.
- Packaged 0009-cpubsd with normal IRQ masking, same ADT/loader/trace flags,
  no rootfs. Image SHA256
  26cf151d8b52ed9977e62e80d1535c46b900b2dae90a44ad27fd9ddb7d000edb.
  Host checks passed; entry PA 0x103470488, ADT PA 0x104000000.
- Download-mode USB detected. BOOT-only Heimdall upload reached 100%, success,
  reboot, exit 0. No independent readback. Current BOOT 0009-cpubsd, usable
  to establish CPU publication/kperf progress, with known BSD codegen defect.
- Asked user for 0009 CPU/SGI/kperf/BSD markers or photo. Runtime pending.

- BSD correction committed/pushed 31c628a, CI 43524594391 dispatched on macos-15-intel. Inspect bsd_init actual codegen before next package.

### 0009 result: kperf CPU wait; CPU match mismatch found

- User reports 0009 before VM restrictions, after VM restrictions, then
  before kperf CPU wait (transcribed 009). No after-wait marker supplied.
  kperf_init_early immediately calls ml_wait_max_cpus; source waits until
  CPU driver calls ml_set_max_cpus. Current execution PC not recovered.
- Found definite configuration defect: A03 ADT CPU compatible is
  arm,cortex-a55 + ARM,v8, while built-in SweetCPU IONameMatch is solely
  qcom,kryo470. Therefore its intended compatible match cannot select the
  A03 CPU; SIMD fix alone cannot cause that driver to attach.
- Added A03-only profile patch 0087 matching arm,cortex-a55 and reporting
  Cortex-A55 instead of donor Kryo 470. Keep real DT identity and all CPU
  registration/SGI validation/waits. No forced CPU-completion publication.
- Patch reverse validation passes. Rebuild includes existing BSD flag fix
  0086; inspect CPU match and BSD codegen in resulting artifact.
- Current phone BOOT remains 0009, no further device write in this step.

- CPU-match fix committed/pushed 4e90279. New CI 43526118698 dispatched on macos-15-intel, includes BSD fix 0086. Ignore old BSD-only build for next flash.

### 2026-11-14: trial 0010 CPU-match build verified and BOOT uploaded

- CI 43526118698 passed at source 4e90279. Plain arm64 kernel SHA256
  f3b7de775b74b27d17c89c19081e5a9488988c8161292a7b75266e43c2b340f8
  matches artifact manifest. Actual personality matches arm,cortex-a55;
  old qcom,kryo470 personality absent. BSD/CPU marker strings present.
- Complete symbol disassembly checked: checkpoint/address 42/97,
  SweetCPU::start/initCPU 200/65, kperf_init_early 32, bsd_init 1008
  instructions. No FP/SIMD operands in these functions. This specifically
  verifies that 0086 applied BSD's compiler flag in the correct make target.
- Packaged 0010-cpumatch, normal IRQ masking, same ADT/loader/trace args,
  no rootfs. Image SHA256
  7af08504a558c1517bf996535cb0670ddbded54f2157ebc85d9e93eb3f231543.
  Host checks passed; entry PA 0x103470488, ADT PA 0x104000000.
- User confirmed fresh Download mode, USB detected 04e8:685d. Heimdall
  retrieved PIT, uploaded boot 100%, success, reboot, exit 0. BOOT only;
  no independent partition readback. Current BOOT 0010-cpumatch.
- Requested CPU registration/SGI/publication, after-kperf/BSD or panic
  lines/photo. Diagnostic labels still say 0009. Runtime result pending.

### 2026-11-14: trial 0010 photo confirms CPU + BSD, missing pthread provider

- Directly inspected private photo IMG_20261114_005550.jpg. Visible:
  CPU initialization complete; SWEET CPU boot CPU 0 registered, SGI1
  verified, initialization complete. BSD progresses through credentials,
  buffer init, IOKitInitializeTime, vfsinit, mbinit (64 MB pool), audit,
  knote/eventhandler init and calling aio_init.
- Exact visible primary panic: cpu 0 caller 0xfffffe0007a62a50:
  pthread kernel extension not loaded (function table is NULL).
  @pthread_shims.c:318. Subsequent handshake structure not initialized is
  debugger fallout, not a replacement root cause. No root/userspace yet.
- Source pthread_init explicitly panics when pthread_functions is NULL.
  A03 profile excluded donor 0019 built-in pthread provider. This is a
  missing required integration, not a reason to skip pthread_init/aio_init.
- Expanded pinned donor selection with 0019 libpthread provider plus pinned
  0019 staging script (Apple libpthread commit a6c70ca0e544347a0377babf748f831577ec24f9),
  0021/0022/0024 mockfs RAM-root support and 0025 minimal AMFI interface.
  These are generic test-userspace integrations, no Qualcomm drivers.
  AMFI provider returns no entitlements; it does not grant privileges.
- Added 0088 general-register codegen for new pthread/AMFI/mockfs objects.
  Donor patches apply locally, 0088 reverse check/profile staging/Python
  syntax checks pass. Full integration compile still pending.
- Next trial intended to attach prepared static test init via --ramdisk,
  rd=md0. This proves PID1/syscalls if successful; it is not iOS launchd
  or SpringBoard. No additional phone write yet. Current BOOT remains 0010.

- Integration committed/pushed a8e2da7; CI 43530972730 dispatched on macos-15-intel. Verify pthread registration provider and BSD codegen before test-init packaging.

### 2026-11-14: trial 0011 pthread/RAM-init build verified and BOOT uploaded

- CI 43530972730 passed at a8e2da7. Plain arm64 kernel SHA256
  00028c59d5c543c32e2c13e1e6229ede236140027a205c79c1e003a9f5ea585d
  matches artifact manifest. Cortex-A55 match and pthread registration
  string present. Built-in pthread startup entry and mockfs symbols present.
- Actual complete-symbol disassembly checked SIMD-free: checkpoint 42,
  CPU start 200, BSD init 1008, pthread register/start 26/10, AMFI register 9,
  mockfs_mountroot 97, provider __pthread_init 47 instructions. These checks
  validate named functions, not all future paths or runtime registration.
- Packaged 0011-pid1 with prepared static arm64 test init as --ramdisk,
  rd=md0, normal IRQ masking and existing trace arguments. RAM image at
  PA 0x104008000, padded size 0x8000; ADT PA 0x104010000; entry 0x103470488.
  Init SHA256 f5de3714ff95e6a3b9ece30723f677de0f3f74ec5eb985a00c5ae872f0ac9bf1.
  Init segment byte-match and exact payload embedded in BOOT verified.
- BOOT image SHA256
  4bdf15d5a4c66321783f193d5c72fef33bbebd520eb07087da8b650e9b6fb0c9.
  Packer host bounds checks passed. This contains a test executable served
  by mockfs, not a real iOS filesystem/launchd/SpringBoard.
- USB was Download mode 04e8:685d. Heimdall retrieved PIT, uploaded boot
  100%, reported success, rebooted, exit 0. Only BOOT written; no independent
  readback. Current BOOT 0011-pid1; asked for pthread/md0/PID1/heartbeat
  or panic lines/photo. No userspace success inferred before device report.

### 2026-11-14 MILESTONE: A03 XNU userspace PID 1 runs

- User reports trial 0011 displays load_init_program attempting
  /usr/appleinternal/sbin/launchd.development, then /sbin/launchd, then
  *** SWEET userspace: init running as PID 1 *** and
  SWEET init: still alive (minor transcription typos in user message).
- This is on-device evidence of mockfs RAM-root execution, test init at
  PID1, user/kernel syscall transitions and console writes. The still-alive
  message is produced after the test program's select timeout; one report
  does not establish long-duration stability or sustained interrupt rates.
- It is the static test executable provided as the RAM disk, not Apple's
  launchd or an iOS graphical interface. The development-launchd candidate
  message is a search attempt; fallback /sbin/launchd successfully executes.
- Missing pthread registration panic is no longer blocking this boot.
  Current BOOT remains 0011-pid1; no further image or partition write.
- Next real-iOS dependencies: accessible filesystem containing launchd,
  dyld/shared cache and services; A03 eMMC/block transport (donor UFS is
  Qualcomm-specific); generic HFS/code-signing/entitlement integration;
  framebuffer/IOSurface and display services before any GUI claim. Current
  managed RAM window is 256 MiB, unsuitable for assuming full root fits in
  RAM. No authorization inferred to write non-BOOT partitions.

### 2026-11-14: filesystem split and first HFS trial preparation

- User requests filesystem work with no complete XNU rebuild per file edit.
  Integrated pinned generic donor 0026 HFS provider/staging script and A03
  0089 general-register codegen for all HFS objects. Local patch application,
  reverse check, profile staging and Python syntax pass. Full CI pending.
- Added independent a03-root workflow: macOS constructs raw 32 MiB HFSX
  test root with static init; no XNU build. Added a03-pack-root.py to combine
  existing kernel/ADT + changed root, preserving exact BOOT wrapper and
  recording hashes, with no flash. Root contents optional overlay a03-root/.
- XNU workflow now uses supported CCACHE=ccache plus compiler/profile/config
  scoped persistent cache. First build cold; reuse/statistics unproven until
  subsequent runs. It still configures/links; not a saved make object tree.
- eMMC controller from live DT: sprd,sdhc-r11p1, PA0x201d0000 size0x1000,
  SPI10/INTID42, 8bit. Linux sprd-sdhcr11 driver. USERDATA mmcblk0p55.
  No MMIO probe or storage command/write yet. Read-only block access needs
  separate controller/clock/card-state validation. Donor UFS not selected.
- New docs/a03-filesystem.md records packaging/next block checkpoint.
  Current phone still working BOOT0011; no additional flash in this phase.

- Filesystem/cache split pushed as 9e73e9e. Initial kernel dispatch failed
  HTTP422 Actions disabled; user reenabled Actions. Retry kernel run
  43534803374 queued at 9e73e9e. New a03-root workflow dispatch is not yet
  registered on default branch (404); trigger its existing branch push
  event with a workflow update instead of editing default branch.

### Independent HFS root workflow verified (no XNU rebuild)

- First root CI43534898103 failed: hdiutil -format cannot create a blank
  image. Correction 06b2679 incorrectly used -type UDRW, failed in
  CI43535056579. Fixed d1ca9ab by omitting the unnecessary type/format and
  using hdiutil's default writable image creation with -layout NONE.
- Root-only CI43535227249 PASSED, root job 24 seconds, no kernel build.
  Downloaded artifact shim/a03/out/root-43535227249/a03-test-root.img:
  32MiB raw HFSX, SHA256
  b886b433b988b410cd643683b93db1553d769ecddaf6ca73af3c68e910dbed1e.
  Manifest hash, primary/alternate HX signatures and volume size verified.
- HFS-capable kernel CI43534803374 remains queued. Do not attach this real
  filesystem to old mockfs-only kernel and claim HFS support. No phone
  flash or non-BOOT write performed. BOOT0011 remains working checkpoint.

- User reports pending-job stall and AUR ldid build failure. CI43534803374
  had status queued with jobs=[]; started fresh same-runner kernel
  CI43536143024, now in Build. No manual cancellation needed.
- hfsprogs/ccache/apfs-fuse/dmg2img now installed. Reproduced ldid compile
  errors against OpenSSL4 in a /tmp copy of AUR-prepared source. Compiling
  with installed OpenSSL3 headers/libs succeeds. Local ignored tool at
  shim/a03/out/host-tools/ldid, linked libcrypto.so.3, successfully signs
  disposable init copy and prints CDHash. No original init/system change.

### 2026-11-14: HFS kernel verified; trial 0012 prepared, not flashed

- CI43536143024 passed at source16b3177. Plain arm64 kernel SHA256
  c4c4e4a707ca4da82bd68318dfd187d7984d65fe4482999775e329af65ba942a
  matches manifest. Full-symbol disassembly SIMD-free: HFS register86,
  mountfs1103, vnop_read215, mockfs_mountroot139, BSD init1009,
  pthread register26 instructions. Named function checks only.
- Root artifact from CI43535227249 passes host fsck.hfsplus -n, including
  extents/catalog/hierarchy/xattrs/bitmap. Read-only Python HFS catalog
  lookup resolves /sbin/launchd, mode100755, exact16635-byte test init match.
- Packaged fixed kernel +32MiB HFSX via tools/a03-pack-root.py, no kernel
  rebuild for packaging. BOOT0012-hfs SHA256
  4951efd8eae4493980ba0b9fdb7495bfb2a06f88e44206f603f5c7ff1814b60d.
  RAM rootPA0x104078000 size0x2000000; ADTPA0x106078000;
  entryPA0x10347c488. Packer bounds/exact root segment/BOOT payload pass.
- First compiler-cache run:1050 cacheable calls,0hits/1050misses; cache
  saved successfully. Warm reuse not yet measured; no claimed hit speedup.
- Phone absent from USB/ADB at check. Asked user fresh Download mode.
  NO0012 flash yet; current BOOT remains working0011-pid1. Non-BOOT intact.

### 2026-11-14: BOOT 0012 HFS filesystem test flashed

- User confirmed fresh Download ready. USB04e8:685d detected; host image
  hash rechecked against manifest:
  4951efd8eae4493980ba0b9fdb7495bfb2a06f88e44206f603f5c7ff1814b60d.
- Heimdall retrieved PIT, uploaded boot100%, reported successful upload,
  rebooted device, exit0. Only BOOT written; no independent readback.
- Current BOOT0012-hfs contains verified 32MiB HFSX RAM root and test init.
  Asked user HFS mount/PID1/heartbeat/panic lines or photo. Runtime pending;
  previous mockfs0011 PID1 success is not proof this HFS trial mounted.

### 2026-11-14 MILESTONE: HFSX RAM root mounts and executes PID 1

- User physically reports BOOT 0012: Added memory device md0/rmd0;
  BSD root md0, major 1, minor 0; hfs mounted A03TestRoot on b(1,0);
  load_init_program attempts /sbin/launchd; SWEET userspace init running
  as PID 1; SWEET init still alive. Names normalized from transcription.
- This confirms the real HFSX RAM filesystem mounted and supplied the
  static test executable as PID 1. It is not Apple launchd, SpringBoard
  or an iOS GUI; persistent eMMC access is still unimplemented.
- Current BOOT remains 0012-hfs, SHA256
  4951efd8eae4493980ba0b9fdb7495bfb2a06f88e44206f603f5c7ff1814b60d.
  No further phone writes are needed to record this result.
- Root file edits can reuse kernel c4c4e4a707ca4da82bd68318dfd187d7984d65fe4482999775e329af65ba942a
  with a03-pack-root.py. Adding Linux HFSX creation removes macOS CI
  from that loop; kernel changes still need the separate XNU build.

### 2026-11-14: BOOT 0013 read-only eMMC snapshot flashed

- User authorized continuing toward eMMC and confirmed Download mode.
  USB 04e8:685d detected. Added opt-in A03_EMMC_SNAPSHOT=1 to the local
  loader build; normal builds exclude it. No XNU rebuild or CI required.
- The diagnostic runs at EL1 before XNU, reads 14 explicit controller
  registers at live-DT PA0x201d0000 using Linux-reference access widths:
  PRESENT, CLOCK, HOST, POWER, HOST2, VERSION, ARG, COMMAND, RESPONSE0,
  INT_STATE, INT_ENABLE, SIGNAL, DLL_CFG and DLL_DELAY. No FIFO read,
  card command, reset, clock change or controller/storage write.
- It prints a pre-access marker and each hex result, then deliberately
  pauses at A03 EMMC SNAPSHOT COMPLETE - PAUSED FOR PHOTO. This trial
  does not enter XNU/PID1; a fault/stall can leave the last read marker.
- Freestanding compile passes warnings-as-errors; actual diagnostic
  disassembly has integer-only code and byte/halfword/word MMIO loads.
  Linked loader has no relocations; register labels use inline arrays
  rather than unrebased absolute pointers in static data.
- BOOT0013 SHA256
  c7465260e94e8ace4505595d254d8f5f589671a2c14bfec85575466e5d1836ae.
  Manifest shim/a03/out/a03-xnu-0013-emmc-snapshot.json. Exact unchanged
  BOOT0012 kernel/HFS payload byte-match verified inside the new wrapper.
- Heimdall retrieved PIT, uploaded only boot100%, reported successful
  upload and reboot, exit0. No independent partition readback. Physical
  register results pending user photo/transcription. No eMMC reads of
  card sectors or functional block-device claim yet. BOOT0012 retained.

### 2026-11-14: BOOT 0013 physical snapshot received; 0014 prepared

User transcribed all 14 values from the phone:

```text
PRESENT=0x01f000f0 CLOCK=0x00000007 HOST=0x00000020
POWER=0x00000000 HOST2=0x00003005 VERSION=0x00000004
ARG=0x00010000 COMMAND=0x00000b1a RESPONSE0=0x00000900
INT_STATE=0x00000000 INT_ENABLE=0x027f000d SIGNAL=0x027f000d
DLL_CFG=0xef250b23 DLL_DELAY=0xd5c0c07f
```

- Confirms pre-XNU MMIO reads on hardware. Against the local A03 Linux
  register definitions: no command/data inhibit (PRESENT bits0/1 clear),
  internal/stable/card clock bits set, 8-bit HOST, HS200 HOST2 mode5,
  host version4 (4.10). POWER0 is not proof the card is unpowered: Linux
  labels that register unused. Retained response0x900 encodes TRAN plus
  ready-for-data; this is historical response, not a fresh status result.
- ARG suggests candidate RCA1 from an addressed CMD11. Do not assume
  selected hardware partition or verified sector access from these values.
- User reports every glyph horizontally mirrored. Loader used bit0 as
  leftmost pixel against an MSB-first font. Changed to 0x80>>bit and clear
  each rendered row so replaced labels leave no trailing characters.
- Prepared 0014 using A03_EMMC_SNAPSHOT=2, no XNU rebuild. It snapshots
  first, then issues at most one CMD13 SEND_STATUS using retained argument
  only if clock/inhibit/empty interrupt status/argument/addressed-command/
  retained TRAN+ready guards pass. No CMD6/7/0, sector reads, DMA, reset,
  clock programming or storage writes. This mode DOES write command and
  interrupt-control registers; original enables restored after polling.
- Poll bounded to one counter-second and 10 million iterations. Displays
  CMD13 INT/RESPONSE/PRESENT, pauses before XNU, no reset/retry on failure.
  Actual integer-only loader disassembly, no relocations and unchanged
  kernel/HFS payload byte-match verified; corrected F glyph host-rendered.
- BOOT0014 SHA256
  17b1299ee4387b52eeba7a1a25c15a85495a5b9e5a9f2d76896a6f11ac42f48f.
  Image/manifest shim/a03/out/a03-xnu-0014-emmc-status.{img,json}.
  NOT flashed: phone absent from Download USB at check, still0013.

### 2026-11-14: BOOT 0014 CMD13 diagnostic flashed

- User reports heimdall detect succeeds; independently detected device
  and rechecked image SHA256 against manifest:
  17b1299ee4387b52eeba7a1a25c15a85495a5b9e5a9f2d76896a6f11ac42f48f.
- Heimdall protocol/PIT succeeded, uploaded only boot100%, reported
  successful upload, rebooted and exited0. No independent readback.
- Current BOOT0014. Await physical CMD13 INT/RESPONSE/PRESENT and result
  (or guard-skip/final partial marker), plus confirmation of glyph fix.
  Diagnostic deliberately pauses before XNU. No fresh card response or
  sector-read success is inferred from the successful flash.

### 2026-11-14: CMD13 succeeds; BOOT 0015 read trial flashed

- User reports CMD13 INT=0x00000001, RESPONSE=0x00000900,
  PRESENT=0x01f000f0. Fresh command-complete response confirms ready/TRAN
  at the retained RCA1; no inhibit bits. User confirms glyphs now correct.
  This does not establish sector access or selected hardware partition.
- User reminded us to use android_kernel_samsung_a03; all new command,
  PIO/FIFO, block-count and EXT_CSD definitions checked against that
  local checkout (sprd-sdhcr11, sdhci, mmc_ops, include/linux/mmc/mmc.h).
- Added opt-in mode3, BOOT0015: revalidate fresh CMD13, read 512-byte
  EXT_CSD via CMD8 PIO, display revision/partition config/sector count/
  data-sector-size. Only if user partition selected, 512-byte sectors,
  plausible modern revision and capacity: CMD17 LBA0 then LBA1. No CMD6,
  selection, DMA, clock/reset programming, multi-block access or writes.
- Checks MBR signature then EFI PART GPT header, current LBA1, bounded
  header size and header CRC32. No full GPT table/backup identity check
  yet. CRC match would be first internally validated sector reads only.
- Each event wait bounded to one second/10 million iterations, no retry
  on error. Restores interrupt enables and block registers; pauses before
  XNU with results. Hardware behavior of new PIO path remains unproven.
- Host verifies warning-clean build, integer-only disassembly/no linked
  relocations, exact0012 kernel/root payload match, actual C CRC helper
  against zlib for92/512-byte synthetic headers. No XNU build required.
- BOOT0015 SHA256
  94c7832e02d5452410bfc2c82fc83f389a514f4f869b61c2897de682d8a18197.
  Manifest shim/a03/out/a03-xnu-0015-emmc-read.json. Detected Download USB.
  Heimdall PIT/boot100%/upload/reboot successful, exit0; BOOT only, no
  independent readback. Current0015, physical results pending.

### 2026-11-14: photo confirms 0015 EXT_CSD path fails; 0016 prepared

- Read user's local IMG_20261114_112553_338.jpg (private /home/stoned/ocr).
  CMD13 INT1/RESPONSE900/PRESENT01f000f0 again. CMD8 READ R1=0x00000900,
  READ INT=0x00000002, READ PRESENT=0x01f000f0, then EXT_CSD FAILED -
  STOPPED, NO RETRY. Bottom says READ PROBE COMPLETE / NO DMA OR STORAGE
  WRITES. No EXT_CSD fields, MBR or GPT displayed; no sector-read success.
- Important: final interrupt2 is transfer-complete, without error bits.
  The helper nevertheless returned failure. 0015 does not expose which
  wait failed or whether any FIFO words were read, so neither successful
  PIO data reception nor missing read-ready event can yet be concluded.
- Rechecked local cloned sprd-sdhcr11 driver interrupt handling and sdhci
  FIFO definitions; no online reference needed. Prepared0016 with same
  command/transfer logic, adding fail-stage, accumulated/last poll status,
  last sampled PRESENT, FIFO-word count, live enable/command diagnostics.
  These appear at rows65..71; photo must include lower screen.
- No speculative register-mode/reset/clock/card changes. Read-only CMD8/
  CMD17 whitelist and guards retained. Host integer-only disassembly,
  no linked relocations, exact0012 payload and normal build verified.
- BOOT0016 SHA256
  830bf41e70460aeed768aaf0af86fcbf1caf175d1eb3ecb435d37f78e3a41fb9.
  shim/a03/out/a03-xnu-0016-pio-stage.{img,json}. No XNU rebuild.
  NOT flashed: Download USB absent at check. Current phone remains0015.

### 2026-11-14: BOOT 0016 polling-stage diagnostic flashed

- User confirmed Download ready; heimdall detect independently succeeded.
  Image SHA256 rechecked against manifest:
  830bf41e70460aeed768aaf0af86fcbf1caf175d1eb3ecb435d37f78e3a41fb9.
- Heimdall protocol/PIT succeeded, uploaded only boot100%, reported
  successful upload/reboot and exit0. No independent readback.
- Current BOOT0016; await failure-stage, POLL SEEN/LAST/PRESENT, FIFO
  WORDS, INT ENABLE LIVE and COMMAND LIVE (rows65..71), plus any EXT_CSD
  or GPT results. Runtime pending; no PIO success inferred from flash.

### 2026-11-14: 0016 identifies unsupported PIO assumption; SDMA trial ready

- User transcribed FAIL STAGE2 (read-ready wait), POLL SEEN3, LAST2,
  PRESENT01f000f0, FIFO WORDS0, INT ENABLE LIVE037f000b, COMMAND LIVE083a0013.
  Command-complete and transfer-complete occurred without sampled buffer-
  ready; zero FIFO words read. No usable EXT_CSD/sector data established.
- COMMAND low transfer-mode bits read back0x13 although probe requested
  0x10; DMA-enable and block-count-enable read set. Read-ready enable0x20
  also reads clear despite attempted enable. This contradicts treating
  generic SDHCI PIO as a validated path on this IP. Exact hardware cause
  is not proven, but downstream code supplies a supported DMA route.
- User correctly points to cloned downstream source. sprd_send_cmd sets
  if_dma=1 for every data command; no PIO data path. sprd_sdmd_mode selects
  SDMA and programs v4 buffer address0x58/0x5c. Existing code had inspected
  downstream register definitions but wrongly borrowed generic PIO.
- Prepared mode4/BOOT0017 following that single-buffer SDMA setup, not
  copying GPL driver implementation. Whitelist still CMD8/read CMD17 only,
  CMD13 guard first; metadata/user-partition/MBR/GPT guards retained.
  Host DMA select0; single read transfer0x11; v4 count at0; 512-byte
  loader-owned aligned buffer, initialized sentinel, not stack memory.
  Require MMU/data cache off, observed v4/64bit HOST2 bits and version4.
  DMA is FROM card INTO RAM only; no storage writes/config commands.
- Bounded command/transfer waits, no retry/reset on failure. Buffer stays
  reserved and loader halts even if transfer times out. Restore original
  DMA address/host selection only after inhibit bits clear. Reads verify
  sentinel changed before interpreting metadata; no success claim yet.
- Actual integer-only code, no relocations, aligned buffer beyond downward
  stack/below loader end, exact0012 kernel/HFS payload verified. Normal
  loader and older mode3 compile. No XNU build/CI.
- Reviewed candidate is shim/a03/out/a03-xnu-0017-sdma-read-v2.img SHA256
  3b15409996e43a52729383f1c06f37bbe242d04c5fa9958732899ac22ed3c8a4.
  Earlier non-v2 host candidate superseded, never flashed. No Download
  USB now;0017 NOT flashed. Current phone remains0016.

### 2026-11-14: BOOT 0017 SDMA diagnostic flashed

- User confirmed Download ready; heimdall detect succeeded. Rechecked
  reviewed v2 image SHA256 against manifest:
  3b15409996e43a52729383f1c06f37bbe242d04c5fa9958732899ac22ed3c8a4.
- Heimdall protocol/PIT successful, uploaded only boot100%, reported
  upload success/reboot, exit0. No independent partition readback.
- Current BOOT0017. Await EXT_CSD/MBR/GPT or failure diagnostics,
  including DMA WORDS COPIED, buffer address and poll/status markers.
  SDMA behavior and card data remain unverified until physical report.

### 2026-11-14 MILESTONE: first eMMC sector reads, GPT header CRC matches

- Inspected user's private photo IMG_20261114_113809_312.jpg. BOOT0017
  shows CMD13 INT1/RESPONSE900/PRESENT01f000f0, then successful CMD8
  and two CMD17 transactions (each READ R1=900, INT2, PRESENT01f000f0).
- EXT REV=0x00000008; PARTITION_CONFIG=0x00000008 (access bits0 = user
  area); SECTOR_COUNT=0x0747c000; DATA_SECTOR_SIZE=0x00000000.
  LBA0 MBR SIGNATURE=0x0000aa55. LBA1 GPT HEADER CRC STORED and COMPUTED
  both0x040a1bb6; final GPT HEADER CRC MATCH - FIRST SECTORS READ.
- This is physical evidence of eMMC metadata and user-area sector0/1
  reads via single-buffer SDMA into loader RAM, not merely command status
  or a host simulation. Bounds/MBR/GPT header checksum guards passed.
  No sector writes, partition selection changes or non-BOOT flash.
- Distinguish scope: no GPT entry-array CRC/partition-name validation,
  full BOOT-backup comparison, XNU block provider, filesystem on eMMC or
  Apple launchd yet. Trial deliberately pauses before XNU.0012 remains
  the separate HFS RAM-root/static PID1 checkpoint.
- Current phone remains0017; no new flash. Next bounded read-only test:
  parse/checksum primary GPT entry array, check boot/userdata labels and
  sizes against captured PIT/by-name evidence, then compare a known BOOT
  sector with the exact currently flashed0017 image (not old Magisk BOOT).
  Only after identity/reads validate should XNU block integration start.

### 2026-11-14: 0018 GPT/current-BOOT validation prepared

- Revalidated clean starting worktree at37285d9 and successful0017 evidence.
  Read live PIT through Heimdall download-pit --no-reboot; private current.pit.
  BOOT identifier39/start483328/count131072; USERDATA identifier55/start15929344,
  PIT count0 means remainder, not a verified zero-length partition.
  PIT SGPT location appears based on a smaller capacity than EXT_CSD; parser
  permits a bounded backup GPT within media rather than assuming last LBA.
- Mode5 reuses validated single-sector SDMA setup, CMD8/13/17 only. After
  capacity and GPT-header CRC checks: at most32 primary entry-array sectors,
  CRC over exact entry count, nonempty GUID/range/overlap checks, UTF16 boot
  index38 and userdata index54 matching live PIT/by-name evidence. USERDATA
  must end at last-usable; never read its contents or write card sectors.
- Then reads BOOT header and one complete immutable payload sector against
  THIS running image (0018 replaces0017). Checks Android magic/kernel size/
  v2/page2048 and all512 bytes at BOOT-relative sector97524. This is a sampled
  BOOT identity check, not a full64MiB partition readback or cryptographic hash.
- Actual freestanding C parser passed synthetic valid/partial-array CRC and
  I/O-failure/range/overlap/PIT-ID/missing-label/malformed-header tests. Modes
  0/3/4/5 compile Werror;0018 no linked relocations or SIMD instructions. Exact
 0012 kernel/HFS payload retained SHA256a8f977a5bd0f00bfb24b7452aa38795a728f393e40201f7ddfd34b6ff8f38e75.
- Candidate shim/a03/out/a03-xnu-0018-gpt-boot.img SHA256
  2b6683c9cd2d29a1536a7037b02d5e681b038a6ddb32ed457218cc42029d0d67.
  Manifest beside image. Restore Magisk BOOT hash verified. NOT flashed yet;
  live Download session retained after PIT retrieval, flash needs --resume.
  Trial intentionally pauses before XNU; runtime GPT/BOOT success unproven.

### 2026-11-14: 0018 GPT/current-BOOT diagnostic flashed

- Commit9327668 contains loader/parser and actual-C host tests. Resumed
  live Download session from PIT read. Heimdall retrieved PIT, uploaded only
  boot100%, reported boot upload successful/reboot, exit0. No independent
  partition readback. Flashed candidate SHA256
  2b6683c9cd2d29a1536a7037b02d5e681b038a6ddb32ed457218cc42029d0d67.
- Current BOOT0018. Await physical screen through row77: GPT array stored/
  computed CRC, result code, boot/userdata start/count, BOOT header/payload
  match or exact guard/failure. No GPT-entry/known-BOOT runtime success yet.
  Only BOOT was written; no filesystem/card-sector writes by probe, no
  recovery/bootloader/EFS/NV/USERDATA writes. XNU provider still pending.

### 2026-11-14: 0018 photo identifies identity rejection; 0019 prepared

- Inspected IMG_20261114_114702_077.jpg.0018 reads EXT_CSD/MBR/header
  again; GPT header CRC040a1bb6 matches. GPT ARRAY CRC STORED=bb4c2987;
  COMPUTED=00000000; RESULT=3(identity). Computed zero is the initialized
  diagnostic field because parser returned before completing array, not
  evidence of a computed CRC mismatch. No BOOT comparison reached.
- Exact failing identity condition unproven: boot index/start/length or
  userdata index/start/end. Do not weaken constraints by guessing.0019
  accumulates identity mismatch bits while finishing bounded array CRC,
  prioritizes a CRC error, then prints actual starts/counts/zero-based
  indices/last usable. Mismatch still stops before BOOT comparison/XNU.
- Bitmask:1 duplicate boot,2 boot index,4 boot start,8 boot size,16 duplicate
  userdata,32 userdata index,64 userdata start,128 userdata end!=last usable.
  No new commands, storage writes, card config, reset or clock changes.
- Actual C regression tests pass, including complete CRC on identity error
  and CRC-error priority; Werror/no-relocs/no-SIMD, exact0012 payload verified.
  Candidate shim/a03/out/a03-xnu-0019-gpt-details.img SHA256
  1cf7617b30af133355a64c884c3250602ebeffc3b96f552f33f86b62ca4d6388.
  Prepared only at this entry. Fresh Download USB available.

### 2026-11-14: 0019 flashed, physical mismatch details pending

- Fresh Heimdall detect succeeded; candidate hash independently rechecked.
  Heimdall protocol/PIT/only boot100%/upload success/reboot exit0. No
  independent readback. Current BOOT0019 SHA256
  1cf7617b30af133355a64c884c3250602ebeffc3b96f552f33f86b62ca4d6388.
- Await photo lower rows64..77: stored/computed array CRC, result, BOOT
  and USERDATA start/count, identity bitmask, indices, last usable. Code
  commit6a71956. No GPT-array/BOOT runtime success inferred from upload.
  XNU integration remains gated on resolving actual identity evidence.

### 2026-11-14: 0019 proves GPT array integrity; tail-end guard corrected

- Inspected IMG_20261114_115151_999.jpg. GPT ARRAY stored/computed both
  bb4c2987. Result3 with identity mask80: ONLY userdata-end==last-usable
  failed. BOOT start00076000/count00020000/index26; USERDATA start00f31000/
  index36. Indices are zero-based hex, matching p39/p55 and live PIT.
  Last usable0747bfde; photographed USERDATA count appears0654afdb (small
  tail gap). Exact gap will be printed directly in0020, avoid relying on OCR.
- All entry-array sectors/CRC, nonempty unique-GUID presence, partition
  non-overlap and bounds checks completed. This does not prove BOOT bytes
  or XNU storage access:0019 intentionally stopped before BOOT comparison.
- Root cause of identity rejection is an unsupported parser assumption:
  PIT count0/remainder does not establish USERDATA ends at last-usable.
  Permit a tail gap while retaining verified start/index, range/overlap/
  CRC checks. No partition data or geometry changed.0020 prints tail gap,
  then checks current BOOT header and512 immutable payload bytes.
- Actual-C regressions now include legal tail gaps and still reject
  out-of-bounds/overlap/identity/CRC errors. Werror/no-relocs/no-SIMD and
  exact0012 kernel/HFS payload verified. Ready0020 candidate SHA256
  e7b647a5d7ff4fd7658bd4cedc8c77010652762306fb62dfd54c43d7b1ade896
  at shim/a03/out/a03-xnu-0020-gpt-boot.img. Not flashed at this entry.

### 2026-11-14: 0020 GPT/current-BOOT probe flashed

- Code/tests commit4046c65. Fresh Download detected; candidate SHA256
  e7b647a5d7ff4fd7658bd4cedc8c77010652762306fb62dfd54c43d7b1ade896.
  Heimdall protocol/PIT/only boot100%/successful upload/reboot exit0.
  No independent readback. Current BOOT0020.
- Await physical result rows64..78: array CRCs/result, BOOT header +512
  payload-byte match or exact failure, and directly printed USERDATA tail
  gap.0019 already proves array integrity;0020 sampled BOOT read is pending.
  Trial pauses before XNU. No non-BOOT partition was written; no storage
  writes by diagnostic. XNU block provider and Apple runtime remain pending.

### 2026-11-14 MILESTONE: 0020 storage identity passes

- User transcribed0020: USERDATA TAIL GAP SECTORS=00000007, STORAGE
  IDENTITY PASS, BOOT HEADER +512 PAYLOAD BYTES MATCH. This proves full
  primary entry-array CRC/range/non-overlap/identity validation followed
  by current BOOT header and exact512-byte immutable payload sample.
- USERDATA leaves7 sectors before last usable; earlier count transcription
  from0019 was uncertain. Do not use that OCR count as exact geometry.
  No full64MiB BOOT hash/readback, XNU DMA/block access or eMMC filesystem
  mount is established. Current0020 pauses before XNU. Next integrate
  bounded read-only SDMA into XNU while retaining known HFS RAM root.

### 2026-11-14: first opt-in XNU SDMA/BSD implementation staged

- Added xnu/a03/a03_emmc.c and profile patch0090 with the same guarded
  retained-state CMD13, EXT_CSD, single-block SDMA CMD17 sequence. Mapping
  requires explicit /a03-emmc ADT reg201d0000+1000 AND a03emmc=1. Normal
  ADT lacks this node. IOFindBSDRoot calls probe, rd=md0 remains RAM-root.
- XNU owns a permanent contiguous page, translates VA using kvtophys,
  checks512-byte physical continuity/boundary, cleans+invalidates before
  FROM_DEVICE DMA and invalidates only after completion. Allocation is in
  XNU's upper bank (above4GiB); controller64bit mode required. High-address
  DMA/cache/MMU behavior is not yet physically tested. No low-bank guessing.
- Single mutex serializes BSD reads. Fresh GPT header/array/identity and
  BOOT header checks precede read-only block/char nodes a03boot0/ra03boot0
  and a03userdata0/ra03userdata0. Write open/strategy/write syscall rejected.
  Timeout/error poisons reader, masks controller IRQ and retains DMA page
  permanently, no reset/retry/free or further command. Device nodes remain
  absent on initialization failure; RAM-root startup can continue.
- Local patch dry-run against current prepared XNU, actual GPT tests, ADT
  default/opt-in gating and Python syntax passed. Full XNU compile pending;
  no new flash. Current0020 is confirmed loader storage checkpoint only.

### 2026-11-14: SDMA kernel CI and userspace verification prepared

- b3d9772 pushed; XNU run43588264792 confirmed in_progress/Build.
  No device flash; current0020 remains hardware identity checkpoint.
- Added opt-in A03_STORAGE_TEST static PID1 check: reads512 BOOT header
  bytes via /dev/ra03boot0(physio) and /dev/a03boot0(buffered), verifies
  Android magic/v2/page2048 on both, then requires write-only OPEN return
  EROFS. Never issues a write syscall to block storage. Heartbeat survives
  failure. Root workflow storage_probe=true builds this variant separately.
- Linux ARM64 assembly and mkinit no-relocation/signature checks pass.
  Default init remains byte-identical SHA256f5de3714ff95e6a3b9ece30723f677de0f3f74ec5eb985a00c5ae872f0ac9bf1.
  Runtime test unverified, HFS root artifact still to build.

- Root run43588996330 at890055e PASSED; downloaded HFSX image SHA256
  a1be341789ae438c00cc9a91999e8b4a923be1b7636924bf2b958a39599b0b76,
  read-only fsck clean. Catalog/sbin/launchd mode100755 and contents match
  local storage-test init SHA256979becf2f180d35c1b397b232754db884742f8818824f56e7bed2c7a4165cd0d.
  XNU43588264792 remains verified in_progress/Build. Added guarded packer
  --emmc-readonly option; missing-node rejection tested before any output.

### 2026-11-14: XNU SDMA build succeeds; BOOT0021 prepared

- XNU run43588264792 PASSED atb3d9772. Downloaded plain ARM64 subtype0
  kernel SHA2564784e6ef2ee3dd0c709c37a23cd0a325bf15cce9bb4cda86d91d02d00af6ba09.
  Entire storage text range a03_emmc_probe..emmc_write checked for SIMD;
  all integer-only (1544 disassembly lines). Host build is not DMA proof.
- Packaged verified storage-test HFSX root43588996330 with normal loader
  (no pre-XNU diagnostic), opt-in ADT /a03-emmc, a03emmc=1 rd=md0.
  BOOT0021 shim/a03/out/a03-xnu-0021-sdma-bsd.img SHA256
  7753f418de5b7dd8c5db245e49c439d743c76691ee350a96d6fac22c289aafe7.
  Entry10347c488/root104080000+2000000/ADT106080000; exact loader-payload
  bytes, architecture and gated command line verified. Fresh Download
  detected; no flash at this entry.
- Expected first runtime evidence: XNU SDMA probe, DMA PA (above4GiB), GPT
  result0 CRCbb4c2987/bb4c2987, BSD nodes ready, HFS RAM PID1, then A03
  STORAGE PID1 PASS raw+block BOOT reads/write-open EROFS. Report actual
  failure/last line rather than inferring success from absent USB.

### 2026-11-14: BOOT0021 XNU read-only SDMA/BSD trial flashed

- Reviewed image SHA7753f418de5b7dd8c5db245e49c439d743c76691ee350a96d6fac22c289aafe7
  and Magisk restore hash rechecked. Fresh Heimdall protocol/PIT, upload
  only boot100%, boot upload successful/reboot exit0. No independent readback.
- Current BOOT0021. Await physical XNU DMA PA/GPT validation/nodes and
  A03 STORAGE PID1 PASS (raw+block BOOT reads, write-open EROFS), or exact
  error/last line. No runtime SDMA/BSD success inferred from flash.
  No non-BOOT partition written; root remains HFS RAM image. Apple launchd/
  SpringBoard and eMMC filesystem root remain future checkpoints.

### 2026-11-14: 0021 panic localized to raw user-buffer store; fix prepared

- User reports kernel data abort PCfffffe00074d8fb0. Verified exact0021
  kernel SHA4784e6ef...af6ba09. PC is emmc_strategy+1c4, instruction
  strb w11,[x12,w10,uxtw], copying a successful data_read result into
  buf_map-returned destination. Execution passed GPT/BOOT initialization,
  node registration and a CMD17 data_read in strategy. This is stronger
  XNU progress evidence, but no complete userspace storage PASS yet.
- Local XNU vfs_bio.c buf_map_range_internal returns b_datap unchanged
  for non-B_CLUSTER. kern_physio supplies the user iovec address and
  B_PHYS; direct kernel stores through that user pointer are invalid.
  Root cause is our raw-path copy integration, not evidence of SDMA failure.
  FAR/ESR/registers were not supplied; exact fault syndrome unverified.
- Raw cdev now reads into512-byte kernel stack sector and calls uiomove
  in caller context, outside hardware mutex. Buffered strategy retains
  buf_map but explicitly rejects B_PHYS. No DMA/MMIO/card sequence changes.
- Added sanitizer-backed host harness extracting production handlers
  verbatim. Covers partition translation, bounds/overflow, write rejection,
  map failure, read failures/residuals/completion/mutex balance; raw unaligned
  multisector/EOF/negative+huge offsets/copyout fault/partial I/O. All pass.
  Harness is not a XNU/MMIO/DMA emulator. Patch dry-run and GPT tests pass.
  Current phone0021 panic; corrected kernel build next, no new flash yet.

- Fix3f77331 pushed; XNU CI43590138639 confirmed live/in_progress (Deps).
  Same root43588996330 hash revalidated, no root rebuild. Phone is in
  Download mode, detected via USB; wait for corrected kernel before0022.

### 2026-11-14: corrected raw-copy kernel passes CI; BOOT0022 prepared

- XNU CI43590138639 at3f77331 completed SUCCESS. Plain ARM64 subtype0
  kernel SHA25676b35546dba70b0e67cafd7ce77d6418409410424780c4f599a850e1c37acf41.
  Storage text is integer-only; emmc_read calls uiomove atfffffe00074d9354.
  Production-handler ASan/UBSan and GPT tests pass.
- BOOT0022 shim/a03/out/a03-xnu-0022-sdma-uiomove.img SHA256
  df392a526999866b4c170dbc612955a900952191519223d0f444635a597c4a34.
  Same verified HFSX root43588996330, normal loader (snapshot env absent),
  explicit emmc ADT and a03emmc=1 rd=md0. Exact loader/payload bytes,
  BOOT v2 bounds, root and restore hashes verified. Fresh Download detected.
- No0022 flash at this entry. Next authorized BOOT-only trial expects
  A03 STORAGE PID1 PASS: raw+block BOOT reads, write-open EROFS.
  Current0021 panic; no Apple launchd or eMMC filesystem-root claim.

### 2026-11-14: BOOT0022 corrected raw uiomove trial flashed

- Heimdall fresh protocol/PIT succeeded, uploaded only boot to100%,
  reported boot upload successful, rebooted and exited0. No independent
  readback. Current0022 SHA256
  df392a526999866b4c170dbc612955a900952191519223d0f444635a597c4a34.
- Await physical A03 STORAGE PID1 PASS: raw+block BOOT reads, write-open
  EROFS, or exact panic/last line. Build/flash success does not establish
  corrected raw copy or buffered-read runtime success. HFS RAM root remains;
  no Apple launchd/iOS GUI or eMMC filesystem-root result. No non-BOOT writes.

### 2026-11-14: BOOT0022 reaches PID1 but storage self-test fails

- User reports A03 STORAGE PID1 FAIL (generic diagnostic). This establishes
  static PID1 execution with0022 instead of the0021 raw-copy panic, but
  does not identify raw/block/open/read/header/EROFS stage. No storage
  userspace PASS inferred. Exact SDMA/GPT kernel lines are not yet supplied.
- Adding root-only stage/value diagnostics and independent raw/block header
  PASS markers. Reuse corrected kernel43590138639; no hardware-driver
  change or XNU rebuild needed to expose the failure.

- Diagnostic init64a3cf8 assembled with no relocations. Optional Unicorn
  executes actual ARM64 instructions through PASS and all14 failure stages,
  preserving exact stage/value and confirming console-only write syscalls.
  Default init remains byte-identical. Diagnostic init SHA256
  a3afcaaf5d8a56a73610f0252234753ea510569e1594b913e000ae7d13b900cc.
- storage_probe=true root workflow43597035152 at64a3cf8 SUCCESS; duplicate
  push43597035468 cancelled by concurrency. Fresh Download USB detected.

- Root43597035152 read-only fsck clean; catalog launchd100755 exactly
  matches diagnostic init SHAa3afcaaf...3b900cc. Root SHA256
  9d27cf4f09df5ee7a1dc122fb265aedea1f9a578db38be4467fdf64cb99fd0a4.
  BOOT0023 shim/a03/out/a03-xnu-0023-storage-stage.img SHA256
  31a19aeb5aa25bccbd18a577bd38694e60dddc10bd8cdee664b974610e28d143.
  Exact loader/payload verified, same kernel43590138639, opt-in ADT and
  a03emmc=1 rd=md0; restore hash verified. Ready for BOOT-only trial.

- BOOT0023 FLASHED: fresh Heimdall protocol/PIT, boot-only upload100%,
  upload successful/reboot exit0. No independent readback. Await raw/block
  PASS lines plus exact FAIL stage/value (hex) or complete storage PASS.
  This is root diagnostics only; no hardware-driver change, XNU rebuild
  or non-BOOT write. Actual storage failure remains undiagnosed until
  physical output arrives.

### 2026-11-14: BOOT0023 isolates buffered-read EINVAL; sector-size fix

- User reports FAIL stage0x21/value0x16: block-device read errno22/EINVAL.
  Diagnostic control flow reaches block read only after raw open/read and
  BOOT magic/page2048/header-v2 validation succeeded. Thus0023 establishes
  XNU SDMA plus raw uiomove BOOT-header reads; full block/EROFS PASS pending.
- Source diagnosis: specfs set_blocksize calls bdevsw.d_psize and stores
  its return as v_specsize (bytes per sector). Native memdev mdevsize
  returns mdSecsize. Our callback incorrectly returned partition sector
  count131072, so spec_read rejected devBlockSize>PAGE_SIZE before I/O.
- Corrected emmc_psize to512 for ready valid minors; capacity remains
  DKIOCGETBLOCKCOUNT. No SDMA/MMIO/card-sequence changes. Embedded0090
  source exact-match and patch dry-run pass. Host actual-handler ASan/UBSan
  adds callback checks and complete16KiB/32-sector buffered request; passes,
  and demonstrably rejects the original callback. GPT tests pass.
- Reuse diagnostic root43597035152 for next corrected-kernel BOOT0024.
  Current0023; no new flash or complete storage PID1 PASS yet.

- Fix39d7a06 pushed; corrected XNU run43598578558 confirmed live/Deps.
  Reuse root43597035152 SHA9d27cf4f...99fd0a4 (revalidated), keep
  a03emmc=1 rd=md0 and opt-in ADT. Restore hash revalidated; phone
  Download mode available. Wait for existing CI; do not redispatch.
  Next download/inspect kernel, package0024, BOOT-only flash and require
  physical raw+block BOOT/EROFS PASS. Current0023 remains diagnostic.

- While existing CI43598578558 remains live/Build, expanded actual-handler
  sanitizer coverage to disk ioctls:512-byte logical/physical sizes,
  accepted512/rejected4096 set-size, independent BOOT/USERDATA capacities,
  read/write limits and readonly/invalid ioctl behavior. Full16KiB buffered
  request passes. Diagnostic root revalidated with read-only fsck and
  actual ARM64 PASS+14 failure-stage emulation;0024 ADT prepared only.
  Kernel artifact still pending; current phone remains0023 Download.

### 2026-11-14: sector-size correction built; BOOT0024 ready

- XNU run43598578558 at39d7a06 completed SUCCESS. Plain ARM64 subtype0
  kernel SHA2566880a6c035baf67e2023033c81e0716670b9f4e7e0ad853e8392ab5b4d30dc41.
  Storage text integer-only; raw uiomove call retained. emmc_psize compiled
  mov w8,#0x200 atfffffe00074d9180, conditional512/-1 as intended.
- BOOT0024 shim/a03/out/a03-xnu-0024-sector-size.img SHA256
  a4240b2222a59099fe436a6b33348b9c6ebbed768d9a98ec2f00168e73b53b9c.
  Same verified diagnostic root43597035152, normal loader, opt-in ADT
  a03emmc=1 rd=md0. Exact payload bytes/header/bounds and restore hash
  verified; BSD sanitizer geometry/full16K and GPT regressions pass.
- Ready for authorized BOOT-only test. Current0023; complete storage
  PID1 PASS or exact next failure still requires physical evidence.

### 2026-11-14: BOOT0024 sector-size correction flashed

- Fresh Heimdall protocol/PIT, upload only boot100%, boot upload successful,
  reboot and exit0. No independent readback. Current0024 SHA256
  a4240b2222a59099fe436a6b33348b9c6ebbed768d9a98ec2f00168e73b53b9c.
- Await physical raw/header PASS, block/header PASS, then A03 STORAGE PID1
  PASS raw+block BOOT reads/write-open EROFS, or exact stage/value/panic.
  CI/tests/flash alone do not establish full storage runtime success.
  Root remains diagnostic HFS RAM; no Apple launchd/eMMC filesystem-root
  or iOS GUI. No non-BOOT partition written.

### 2026-11-14: offline iOS root prerequisite inventory prepared

- BOOT0024 physical result still pending; no new image or device write.
  No ADB/Samsung USB or new photo observed in this check.
- Added read-only tools/a03-inspect-ios-root.py to inventory plain-arm64
  dynamic launchd/dyld/SpringBoard, version/jobs and primary cache header.
  It rejects the actual static test root; synthetic fixtures exercise
  arm64e/malformed rejection and rooted absolute/escaping/looped symlinks.
  This does not verify Apple provenance, signing, complete dependencies
  or bootability. Local iOS source assets remain absent in checked paths.
- Current profile still minimal AMFI0025; donor portable0035/0036 services
  are not integrated. No real Apple launchd or iOS GUI result inferred.

### 2026-11-14 MILESTONE: BOOT0024 XNU BSD storage PID1 PASS

- User confirms A03 STORAGE PID1 PASS: raw+block BOOT read, write-open
  EROFS. Current0024 image SHA256
  a4240b2222a59099fe436a6b33348b9c6ebbed768d9a98ec2f00168e73b53b9c.
  Kernel43598578558, diagnostic root43597035152.
- Test requires512-byte raw and buffered BOOT reads, Android magic,
  page2048/header-v2 and write-only raw open returning EROFS. This proves
  XNU SDMA/cache/BSD-to-userspace BOOT reads with d_psize512 corrected.
  Buffered specfs requests16KiB internally; PID1 checks512 bytes only.
- No full BOOT hash, USERDATA userspace read/mount, eMMC filesystem root,
  Apple launchd or SpringBoard result. Root is HFS RAM/static diagnostic
  init. No sector write submitted or non-BOOT permission implied.
- Preserve0024. Next locate supplied iOS assets, adapt real-root access
  and portable entitlement/platform-binary services, then validate Apple
  launchd/dyld before SpringBoard/backboardd graphics integration.
  No additional flash needed for this milestone.

### 2026-11-14: USERDATA filesystem/write support explicitly authorized

- User requests filesystem preparation and write support, accepts loss of
  disposable phone data and recovery through Download mode. Scope new
  filesystem writes to validated USERDATA p55, preserving GPT, recovery,
  bootloaders and EFS/NV. No wipe requested or required.
- Implement opt-in USERDATA-only SDMA writes, completion/status and cache
  flush handling, leaving BOOT nodes read-only. Real Apple source asset
  location is still needed; current0024 storage checkpoint remains intact.

- USERDATA-only CMD24 support staged behind a03emmc_rw=1. Default reads
  unchanged; BOOT nodes always readonly. Lowest write layer rechecks GPT
  USERDATA bounds. Raw writes require512-byte alignment and duplicate uio
  before copyin, advancing original only after device completion. Buffered
  writes serialize partial-sector read/modify/write. CMD24 transfer complete
  plus CMD13 ready/TRAN required; any failure poisons permanently/no retry.
- Write enable currently requires EXT_CSD CACHE_CTRL=0; enabled card cache
  refuses writes rather than falsely acknowledge an unimplemented flush.
  Synchronize ioctls are no-op only under this no-card-cache write contract.
  Host ASan/UBSan BSD and actual CMD24 fake-register tests pass; not physical
  hardware proof. Apple-userspace profile remains optional/default off.
- Matching iOS16.7.16/20H392 iPhone10,2 IPSW found via ipsw.me metadata,
  downloading from Apple's CDN privately to research/ipsw. Expected SHA256
  b3882291a92ecf8763239a026813b3bafae66b7e317dee67011d90c202ccafef.
  No USERDATA write/format or new flash performed yet.

### 2026-11-14: cached-write completion and real iOS root preparation

- Extend opt-in USERDATA writes to known CACHE_CTRL=1 cards: every CMD24
  completes transfer, then CMD6 WRITE_BYTE FLUSH_CACHE=1 waits R1b busy
  completion, then fresh CMD13 ready/TRAN. Unknown encoding refused.
  No cache-enable/timing change. Earlier cache-disabled restriction above
  describes the previous revision. Host tests cover cached/noncached
  sequences and terminal failure at each completion stage; not hardware proof.
- Apple CDN iPhone10,2 iOS16.7.16/20H392 IPSW downloaded privately;
  SHA256 b3882291a92ecf8763239a026813b3bafae66b7e317dee67011d90c202ccafef
  verified. Manifest d21ap OS087-86694-044.dmg, SystemOS087-86588-047.dmg,
  AppOS087-86715-047.dmg. No downloaded Apple binaries tracked.
- Add macOS-only filesystem builder/workflow: pinned source, owner-preserving
  staging on16GiB journaled HFSX, portable donor filesystem tweaks, required
  dynamic plain-arm64 launchd/dyld/SpringBoard/cache inventory and fsck.
  This prepares an image only; execution/CI result not yet established.
- Current phone0024 in Download mode; no new flash or USERDATA write.
  Kernel43600857274 still building earlier no-card-cache revision.

### 2026-11-14: supplied iOS16.0 source located; write diagnostic prepared

- User identifies iPhone10,3,iPhone10,6_16.0_20A362_Restore.ipsw, found at
  repository root but ignored. SHA256 matches public metadata:
  a99575ccdab8bd576e16bc08efe0f8a5c18f0e7bdea522376235f5d5332acc19.
  d22ap manifest confirmed OS098-08778-001, SystemOS098-09479-001,
  AppOS098-09552-001. Filesystem workflow now uses this supplied build;
  16.7.16 download run43601400573 cancelled to avoid duplicate staging.
- Kernel43600857274 SUCCESS: earlier guarded write implementation and
  optional portable entitlement profile compile. Cache-flush revision still
  needs full build. Current phone0024; no new flash or USERDATA write.
- Add separately opt-in static PID1 USERDATA test: save512B at relative
  16GiB (beyond planned16GiB root), XOR pattern, readback, restore, verify,
  fsync. Bounds enforced again by driver. Failure attempts restore if saved;
  poisoned controller can prevent restoration. Never claims PASS on failure.

- Opt-in diagnostic root CI43601678578 SUCCESS at a9251a7. Downloaded
  HFSX image SHA2567a2379b0b6699cb9751b861456f3d22170527e7fb2f46332bd79cc37220dfc4d.
  Read-only fsck clean; catalog init mode0755 and bytes exactly match
  locally emulated diagnostic. ARM64 emulation passes success plus syscall
  errors, short I/O, mismatch, restore failure and fsync failure; original
  read-only diagnostic retains success+14 exact-stage failure coverage.
- Cache-flush kernel CI43601676154 and supplied-source filesystem root
  CI43601667181 live. No new phone write/flash; current0024 preserved.
- Supplied16.0 source revealed donor tweak script hardcoded16.7.16 build
  metadata. Fix migration/activation seeds to read staged SystemVersion;
  host checks cover both builds. Restart filesystem job for this correction.
- Prepare optional0092 direct USERDATA root selection plus guarded rootrw
  (validated writable USERDATA device only; HFS journal checks unchanged).
  RAM-root default preserved.0090+0092 patch application passes baseline.
  Packager exposes explicit --userdata-root, retaining small RAM payload.
  Not included in live43601676154 and not yet fully compiled or booted.

- Filesystem43602020594 reached source APFS mounts/verified checksums, then
  failed at hdiutil create: UDRW is not a valid -type argument. Remove it
  (default writable UDIF, matching tested small-root builder) and rebuild.
  No filesystem artifact or phone write resulted from this failure.

### 2026-11-14: BOOT0025 USERDATA write diagnostic flashed

- Cache-flush kernel43601676154 SUCCESS at a9251a7, SHA256
  1186c33171c20fb66de7236ea0401a7fc614158c25c9e7c559a9429ee72fedf7.
  Storage disassembly operands integer-only; CMD24/CMD6flush/CMD13 constants
  verified. Early broad SIMD regex falsely matched instruction hex d2800000;
  instruction-operand-only check passes. Artifact plain-arm64 subtype0.
- Root43601678578 SHA2567a2379b0b6699cb9751b861456f3d22170527e7fb2f46332bd79cc37220dfc4d
  passed read-only fsck/catalog/exact emulated-init checks.
- BOOT0025 shim/a03/out/a03-xnu-0025-userdata-write.img SHA256
  051304ad437d305cdd77890dbffb3f73763c74e26f2a24355ce1bab951b4dd3c.
  rd=md0 a03emmc=1 a03emmc_rw=1; diagnostic sector USERDATA-relative16GiB.
  Supplied D22AP product identity extracted privately into research/ipsw-x;
  A03 hardware nodes retained. Current restore hash94fa7c53...15e9ce7 verified.
- Heimdall fresh protocol/PIT, boot100%/upload successful/reboot exit0.
  No independent readback. On-device diagnostic may now write one USERDATA
  sector and restore it; physical result pending. No full filesystem flashed.
  Await A03 USERDATA WRITE PASS, or exact WRITE FAIL stage/value/panic.
- Filesystem43602020594 failed invalid hdiutil -type; fixed default UDIF and
  canonical /private mount paths. Superseded43602464223 cancelled; corrected
  supplied16.0 HFSX root43602490133 live. Root-selection kernel43602657100
  dispatched at051206f (includes0092);0025 itself retains RAM root.

### 2026-11-14 MILESTONE: BOOT0025 USERDATA writes physically confirmed

- User reports A03 STORAGE block BOOT header PASS, A03 USERDATA WRITE PASS:
  changed/readback/restored/fsync sector at16GiB, then A03 STORAGE PID1 PASS:
  raw+block BOOT reads/write-open EROFS. Image051304ad...1b4dd3c,
  kernel43601676154/root43601678578.
- Actual XNU raw USERDATA pread/pwrite, modified-sector readback, restoration
  readback and fsync succeeded. BOOT raw write-only open remains EROFS.
  The driver completes each write before acknowledging it; physical report
  does not reveal CACHE_CTRL, so CMD6 execution specifically is not inferred.
- This confirms single-sector physical writes in the validated USERDATA
  range. Full filesystem install/mount, buffered filesystem writes, real
  Apple launchd and SpringBoard remain unverified. Current0025 static PID1.
- Continue supplied16.0 root43602490133 and root-selection kernel43602657100,
  verify artifacts, install only USERDATA then BOOT root-selection trial.

- USERDATA root-selection kernel43602657100 at051206f SUCCESS, SHA256
  124d32ca8812840a171e127c6a24dfaf5da85530eec810aa3f0f4e30605f1d80.
  Plain-arm64 subtype0; storage/root predicates integer-only. Direct root
  availability/writable predicates also host-tested for readonly/notready/
  wrong-device/poisoned states. Default profile unaffected.
- Prepared BOOT0026 shim/a03/out/a03-xnu-0026-userdata-root.img SHA256
  e012784bf236bae131029b02c0a5239546081eebb039852e9de64a465528086b.
  Explicit rd=a03userdata0 rootrw=1 ignition_level=1 -nobsdmgroot;
  small diagnostic RAM image retained in payload. NOT FLASHED: USERDATA
  filesystem must be installed first. Filesystem43602490133 still staging.
  Phone Download detected after user returned it there; current0025.
- Add read-only tools/a03-verify-userdata-root.py final install guard for
  exact16GiB rawHFSX primary/alternate geometry, clean journal flags/hash.
  Does not replace fsck or iOS file inventory. Actual filesystem artifact
  validation pending; correctly rejects small nonjournaled diagnostic root.

- Filesystem43602490133 completed staging:16GiB HFSX,10GiB used/~298k
  inodes. Inventory PASS: actual dynamic arm64 launchd/dyld/SpringBoard,
 16.0/20A362,526 launchd jobs, primary arm64 cache header (subcache coverage
  still limited). Root detached and raw conversion completed. Final macOS
  fsck_hfs on regular-file path failed ENOTTY; no artifact/install resulted.
  Fix final check to attach raw image readonly/nomount and fsck its raw
  device, then detach. Rebuild needed; phone remains Download/current0025.

- Corrected root build43604313047 atfb27fcf queued/live; superseded43604260923
  cancelled after adding completed-conversion retention on final-check
  failure. This avoids repeating all staging merely to diagnose verification.
  Require fsck/logs/host image guard before USERDATA install. Phone remains
  Download/current0025; BOOT0026 ready but not flashed.

- Local readonly APFS-FUSE views of supplied20A362 OS/SystemOS opened under
  ignored research/a03-ios16-source/{os,sysos}/root (no phone access).
  Actual Mach-O load commands confirm launchd uses libSystem/libobjc;
  SpringBoard also uses SpringBoard.framework/Foundation.
- Add a03-verify-ios-cache.py for directory/rawHFS access: actual source
  passes40 declared subcache UUIDs, symbols UUID, mapping/signature extent
  bounds and2663-image table containing four core dependency paths. Injected
  missing part/UUID mismatch/out-of-file mapping rejected. No cryptographic
  signature validation or runtime proof. Run against final HFS artifact too.

- Actual supplied launchd/SpringBoard signatures contain XML entitlement
  slots as supported by optional0035; dyld has a code signature without
  entitlements. No cryptographic trust claim. Root43604313047 rechecked
  live/staging; phone Download detected. No new flash this continuation.

- Checked installed Heimdall2.2.2 grimler fork (64-bit host) against its
  exact v2.2.2 source d9554e7fa30a00abed7f0ac86b10e63c2c3b8e20, ignored
  research/a03-heimdall-2.2.2. Transfer file size/progress use64-bit unsigned
  long/ftello; TotalBytesPacket explicitly sends low/high32bits. Actual
  packet class test encodes16GiB and16GiB+BOOT without truncation. Original
  upstream's32-bit fileSize does not describe this installed fork.
- Existing PIT identifies lowercase userdata, ID55, start15929344, count0
  (dynamic remainder); fork skips partition-size check when PIT count0.
  Final image16GiB must be bounded against validated GPT USERDATA separately.
  No --skip-size-check or repartition option needed. No new phone write.

- Root43604313047 is terminal FAILURE in final fsck invocation, with a
  retained completed artifact14118636510 (5657683395bytes). Log shows
  literal escaped path \/dev\/rdisk8 reached fsck, so fsck did not inspect
  the volume. Use portable prefix removal /dev/r${check_device#/dev/}
  instead of escaped replacement (macOS bash3.2 keeps replacement escapes).
  Shell syntax and exact /dev/disk8 -> /dev/rdisk8 expansion checked.
- Artifact download18144 live, temporary ZIP grew past4GiB; no source build
  restart. Root contents/inventory unchanged by this invocation fix. Run
  Linux read-only fsck, HFSX geometry/SHA, core-binary/source and full declared
  cache checks locally before any USERDATA flash. Phone remains Download.

### 2026-11-14: real iOS16.0 USERDATA root verified locally, ready to install

- Downloaded retained root43604313047 artifact14118636510, decompressed
  exact17179869184bytes. SHA256 matches CI output:
  eb72c14a9cf4aab30a8b49afda745a1b342dc877263d3b6a39901d95c89da108.
- Linux fsck.hfsplus -fn (forced READ ONLY, unlike -n which skips journaled
  volumes) checks extents/catalog/hardlinks/hierarchy/xattrs/bitmap/header;
  volume A03iOSRoot appears OK, exit0. No repair or image modification.
- HFSX primary and alternate geometry4096*4194304; journal block129. Primary
  attrs80002100 clean/journaled, alternate80002000 journaled with older
  unmount flag. Guard originally overrequired both headers' clean bit;
  corrected authoritative primary cleanliness, both journal flags/location
  and both geometries. Actual image passes SHA/geometry; dirty primary,
  missing alternate journal flag, journal-pointer mismatch tests reject.
- Actual HFS catalog/data forks: launchd/dyld/SpringBoard SHA256/length/mode
 0755/uid0/gid0 exactly match supplied IPSW source. HFS version16.0/20A362,
 526 launchd jobs. Full declared cache check passes40subcache UUIDs, symbols
  UUID, mapping/signature extents,2663image table/four core dependencies.
  These remain file checks, not cryptographic signature/runtime proof.
- Fresh Download detected; BOOT0026/kernel/stock-Magisk restore hashes
  revalidated.16GiB image33554432sectors fits verified USERDATA106213336
  sectors (54381228032bytes). Ready USERDATA-only install then BOOT0026.
