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

Original BOOT restored and hash matched after 0002; Android rebooted,
sys.boot_completed=1. ADB returned to unprivileged mode.
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
- tools/dreamlte-build-profile.py: 128 patches (donor through 0203 + S8
  overlays 0204/0205). Excludes later S7 MMIO drivers. Build uses
  MACHINE_CONFIG=HEROLTE.
- Workflow xnu adds board_profile=dreamlte. This is kernel-only bring-up;
  no compatible rootfs assembled, no XNU boot yet, no GUI claim.

GitHub account authenticated, but upstream permission READ. Creating an
account fork for the CI build while preserving origin. Record exact CI IDs,
compile results, hardware observations and restore results below.

## CI / repository milestone

- Initial S8 implementation commit: d9e3b434b7462d0dc452aa11feef327b755f9888.
- Authenticated account has READ access upstream; created fork
  stonedDiscord/ios-a5xelte, remote build. Origin remains wardevsa/ios-a5xelte.
- Fork default branch set to dreamlte-bringup so workflow_dispatch is found.
- CI run 43434858911, job 131917216434 (macos-15-intel), profile dreamlte,
  machine config HEROLTE, DEVELOPMENT, commit d9e3b43. Started; result pending.
- No XNU flash performed. Loader-only packaging is a host test only.

## 2026-11-13: diagnostic recovery path verified

- Optional probe 0003 wrote `DREAMLTE pre-Linux last_kmsg probe 0003` into the
  Exynos snapshot kernel-log region before entering unchanged Linux.
- After reboot, root ADB recovered the exact marker from `/proc/last_kmsg`.
  This proves a pre-Linux loader can leave a small diagnostic marker for later
  recovery; it is not an XNU boot result.
- Restored the verified stock BOOT; readback SHA256 is
  `71fb593969288f3a5a5dc6c4c4da35a53b045650cc293c6e8e4028ac3a7982a5`.

## 2026-11-16: A03 progress reviewed and portable work adapted

- Reviewed build/a03-bringup at f1e16010e5a1b7d94657a867158a81bad0788682.
  A03 BOOT0069 deployment and0068 page-in mutex/CPU-time evidence are donor
  observations, not S8 results. No verified A03 home screen/input was recorded.
- Added S8 overlay0205 with bounded daemon/annotation/startup/IPC diagnostics,
  task snapshots including kernel waits/CPU times, opt-in iOS16 provisional
  replies, scoped scalar Sandbox API and entitlement-gated work intervals.
  All optional boot modes default off. Existing donor software providers are
  retained without registering A03 duplicates. Full scope/dependency map:
  docs/dreamlte-a03-port.md.
- Kept measured S8 4K/A53/EL1/GICv2 and upper512MiB RAM profile. No UNISOC
  MMIO, eMMC/GPT/root paths, USB download/reset sequences or A03 write
  authorization imported. USERDATA/protected partitions untouched.
- Staging produces128 patches and a hash/provenance manifest. CI now checks
  ARM64 and linked S8 diagnostics. Root tweaks use actual staged OS version;
  local compile helper supports fork-specific CI paths and clang override.
- Previous S8 CI43434858911 is now confirmed SUCCESS (not pending). Downloaded
  its exact build tree/log privately for validation; no new S8 boot evidence.
- Host regression suites PASS: actual-code Sandbox unsupported ops/user-copy
  errors, entitlement grant gates, bounded crash selection/annotations,
  HOST budgets and sampler process selection/four-pass timing.
- Local arm64 objects:13 initial translation units plus4 IPC/IOKit units
  compiled, zero failures, with -mgeneral-regs-only. Expected DREAMLTE trap,
  crash and sampler symbols present in the exception object. Plain git apply
  and whole-file comparison against pristine CI sources verified separately.
- Loader build and minimal ADT generation PASS. No phone flash/root write
  performed. Full updated kernel CI result will be recorded below.

- Port commit53686534f052c8bdf28764edff3ac4e259536e2e pushed to build fork.
  Full S8 CI run43879179527 (macos-15-intel, DEVELOPMENT/HEROLTE,
  board_profile=dreamlte) started; outcome pending.
  https://github.com/stonedDiscord/ios-a5xelte/actions/runs/43879179527
- Whole-overlay validation: plain git apply on pristine CI files produced
  all16 complete files byte-identical to the locally compiled source inputs.

- Also ported read-only root prerequisite inspection, matching-cache UUID/
  dependency verification and local/exported cache symbolication under
  tools/dreamlte-* names. Synthetic exported-symbol/redacted/bounds tests
  PASS without Apple data; no root image or installer deployed.

- Additional regression PASS:192 strict/provisional reply combinations
  exercise the actual patched predicate. Kernel-wait symbolication resolved
  an exact Mach-O object symbol for both continuation/frame and retained
  valid frames before a truncated log tail. No runtime claim from these tests.

### Full CI43879179527 failure and correction

- Run failed in ipc_kmsg.c4336: expected expression. The new bounded-log
  extern declaration preceded the existing empty statement after the
  invalid_reply label. Apple Clang16 rejects that placement; local Clang23
  accepted it as a language extension. Moved the extern after the statement.
- This was a compile failure, not a kernel/phone result. Retry required.

- Corrective commit527db60 pushed. CI retry43890925469 queued with the same
  S8 DEVELOPMENT/HEROLTE profile; result pending.
  https://github.com/stonedDiscord/ios-a5xelte/actions/runs/43890925469
- Corrected overlay plain-apply/full16-file equality PASS. All15 local C
  translation-unit checks PASS with explicit -std=gnu11 and
  -mgeneral-regs-only; two IOKit C++ objects passed the earlier check.

## 2026-11-17: caught up with Nov 16 A03 branch

- Fetched build/a03-bringup through ebb9eb4 (2026-11-16 23:31 +0100).
  BOOT0078 evidence is a physical iOS clock/lock-screen report and
  SpringBoard UIApplication event-loop samples, not an unlocked home or
  verified touch. analyticsd/backboardd remain in followup samples;
  ScreenTime vault assertion and PosterBoard crashes persist.
- A03 0145 USB/HID input candidate passed CI43969089570 and host action/touch
  tests. The latest committed handoff still queues BOOT0079; no provider,
  client or physical input delivery result is recorded.
- A03's 1GiB window is validated against its own live RAM/reservations;
  0142 local UID/GID UUID mapping matches its Libinfo; 0144 root metadata
  writer remained unstaged. These device-specific changes were not copied.
- Reviewed 0135–0145. Read-only VFS/credential probes depend on A03's USB
  command path; DREAMLTE still needs console recovery before those probes can
  be useful. Generic HID builder results do not test S8 touch hardware.
- Updated the adaptation map in docs/dreamlte-a03-port.md. DREAMLTE retry
  CI43890925469 succeeded: kernel build, profile marker checks and A53 LSE
  scan passed with zero LSE instructions. It built overlay0205 at527db60;
  no S8 boot/GUI test followed. CI:
  https://github.com/stonedDiscord/ios-a5xelte/actions/runs/43890925469

## 2026-11-17: persistent early XNU trace prepared

- Rechecked the connected SM-G950F: Android completed boot, ADB shell is root,
  and BOOT /dev/block/sda7 still matches the verified stock hash from Nov 13.
  RECOVERY, EFS/CPEFS and USERDATA remain untouched.
- The 20H392 IPSW is iPhone10,3/10,6 (d22ap), iOS 16.7.16. Its BuildManifest
  identifies OS image 087-86698-044.dmg and DeviceTree.d22ap.im4p. These are
  donor assets, not S8 runtime evidence. ReVa currently reports no open
  programs/project files, and the kernelcache import did not complete.
- Added draft overlay0206 to map only the two verified Exynos snapshot blocks
  and append loader/XNU early-stage text to the `last_kmsg` buffer. The trial
  reuses the previously verified 0x91200200 cursor and 0x91a00000..0x91c00000
  log area; no disk or protected-partition writes are added. Snapshot capture
  stops at XNU's existing stage-7 low-map teardown.
- Local validation: overlay applies to the exact CI43890925469 build tree;
  modified `start.s` and `sweet_early.c` compile with zero failures using the
  recovered CI commands. DREAMLTE profile stages129 patches. Loader rebuild
  and minimal ADT generation pass. ReVa imported and analyzed the loader ELF;
  its snapshot writer checks the verified buffer bounds and persists through
  the ARM data cache. ReVa cannot import the kernelcache/IMG4 file formats.
- Full S8 profile CI44047499178 SUCCESS (DEVELOPMENT/HEROLTE,
  board_profile=dreamlte, commit da1a8b1). Kernel build, DREAMLTE checks and
  Cortex-A53 LSE scan passed. Kernel artifact SHA256 is in its private
  `SHA256SUMS`; it is kept outside Git at `/tmp/dreamlte-ci44047499178`.
- Packaged BOOT candidate `shim/out/dreamlte-xnu-0206.img`, SHA256
  `7635350bc14ee2cbcb983f668e6f53d34d3c6ad5a7ce7ba01c23b054ca4efca8`;
  18,423,824 bytes, within the 41,943,040-byte S8 BOOT partition. S8 chip
  8895 DTBH, stock ramdisk, empty second stage and DTBH are preserved. This is
  a kernel-only XNU entry test; no rootfs is assembled.
- BOOT-only trial flash succeeded via Heimdall 2.2.2. The phone rebooted from
  download mode, then stopped enumerating over USB (neither Android ADB nor
  Heimdall download mode is currently visible). The screen is unobserved and
  no XNU entry marker has yet been recovered; treat boot progress as unknown.
  The next required hardware action is VolumeDown+Power forced restart, then
  VolumeDown+Bixby+Power to re-enter download mode, restore the original BOOT,
  boot Android, and read `/proc/last_kmsg`. Do not attempt another flash until
  the verified original hash is restored.
- Extracted the matching `DeviceTree.d22ap.im4p` to ignored
  `research/ipsw-x/d22ap.adt`. Inspection found its 66-property `/product`
  node reports iPhone X. The DREAMLTE ADT builder had been deleting this node;
  changed it to retain the donor's non-placeholder product properties for the
  eventual 20H392 userspace identity. This does not alter Exynos memory/GIC
  hardware data. Product-aware ADT round-trip and S8 RAM/CPU assertions PASS.
- Packaged a separate product-aware candidate at
  `shim/out/dreamlte-xnu-0207.img`, SHA256
  `9e48ccafd2d00e7e1ad3a4cd9c3cef785e72cf4f23c19f28ecf0a7acd0001ce4`.
  Stock Samsung ramdisk, second stage, and DTBH match byte-for-byte; candidate
  fits BOOT. The connected phone returned to rooted Android after 0206;
  `/dev/block/sda7` matched the original BOOT hash before the next trial.
- Recovered 0206 `/proc/last_kmsg` to ignored
  `backup/galaxy-s8-2026-11-13/last-kmsg-0206.txt`. The XNU trace shows entry,
  platform setup, CPU topology, CPU bootstrap, startup bootstrap and CPU init;
  its last marker is `entering arm_vm_init`. This is evidence of reaching
  `arm_vm_init`, not of it returning. The phone's next Android boot confirms
  the trial returned to Android; the exact failure point inside VM init is
  unknown.
- Flashed 0207 to BOOT only with Heimdall 2.2.2. PIT/session completed and
  Heimdall reported `BOOT upload successful`; after its reboot the phone is
  currently absent from both ADB and Heimdall. 0207 XNU progress is unknown,
  and its `/proc/last_kmsg` has not yet been recovered. The latest known stock
  BOOT hash was verified immediately before this flash. No RECOVERY,
  bootloader, EFS/CPEFS or USERDATA writes were made.
- Next: force-restart with VolumeDown+Power, enter download mode with
  VolumeDown+Bixby+Power, restore the verified stock BOOT and verify its hash,
  then boot Android and capture 0207 `/proc/last_kmsg` before another trial.
- Download mode returned. Restored stock BOOT with Heimdall 2.2.2, booted
  Android, and verified `/dev/block/sda7` SHA256
  `71fb593969288f3a5a5dc6c4c4da35a53b045650cc293c6e8e4028ac3a7982a5`.
  Captured ignored `backup/galaxy-s8-2026-11-13/last-kmsg-0207.txt` (47,375
  bytes). Its final XNU marker is also `entering arm_vm_init`; it has the same
  platform/CPU milestones as 0206 and no VM-init return. Thus preserving the
  donor `/product` identity did not advance the observed kernel boot.
- Added draft overlay0208 to keep the S8 RAM logger active beyond stage7,
  mark VM window/page-table setup and `arm_vm_physmap_init`, then disable it
  immediately before the TTBR0 switch. This distinguishes a stall in physmap
  setup from a failure during translation-table replacement. Patch dry-run
  passes against the exact 0206 CI build tree. Profile stages130 patches.
- Full S8 profile CI44057485509 SUCCESS (DEVELOPMENT/HEROLTE,
  board_profile=dreamlte, commit 0f083da). Profile checks and Cortex-A53 LSE
  scan passed. Kernel artifact SHA256 is in its private `SHA256SUMS`, kept
  outside Git at `/tmp/dreamlte-ci44057485509`.
- Packaged BOOT candidate `shim/out/dreamlte-xnu-0208.img`, SHA256
  `94eadeea8a7fe7af5168558af83acdfc4768f442e17c2633db96c0e890c5799d`,
  18,427,920 bytes, within the 41,943,040-byte S8 BOOT partition. Kernel
  strings contain all four VM milestones. Stock ramdisk, second stage and
  DTBH match byte-for-byte; DTBH identifies chip8895. The stock BOOT hash was
  verified immediately before flashing.
- Flashed 0208 to BOOT only with Heimdall 2.2.2; it reported
  `BOOT upload successful`. After reboot, neither ADB nor Heimdall currently
  detects the phone. Screen and XNU progress are unknown; 0208 last_kmsg is
  not yet recovered. Next: force restart (VolumeDown+Power), enter download
  mode (VolumeDown+Bixby+Power), restore original BOOT and verify its hash,
  boot Android, and retrieve `/proc/last_kmsg` before planning another trial.
  RECOVERY, bootloader, EFS/CPEFS and USERDATA remain untouched.
- Download mode returned. Restored verified stock BOOT with Heimdall 2.2.2,
  booted Android, and confirmed `/dev/block/sda7` hash
  `71fb593969288f3a5a5dc6c4c4da35a53b045650cc293c6e8e4028ac3a7982a5`.
  Captured ignored `backup/galaxy-s8-2026-11-13/last-kmsg-0208.txt` (47,554
  bytes). After the 0208 markers for completed VM window/page tables,
  `arm_vm_physmap_init` entry, and `physmap ready; switching TTBR0`, there is
  no post-switch marker. The trace does not establish whether the fault is in
  TTBR0 replacement or in the logger's deliberate shutdown before it.
- Added draft overlay0209 to relocate the bounded RAM logger and early output
  pointers through `phystokv()` after the TTBR0 switch, then use existing
  stage10-13 markers through `pmap_bootstrap`. Patch dry-run passes against
  the exact CI44057485509 source tree. Profile now stages131 patches.
- Full S8 profile CI44071890093 SUCCESS (DEVELOPMENT/HEROLTE,
  board_profile=dreamlte, commit 908e843). Profile checks and Cortex-A53 LSE
  scan passed. Kernel SHA256 `e5781fcec2d37436317c91167c7426c41eaacf66d1e9e8f30dd6fca64d5913f4`,
  stored outside Git in `/tmp/dreamlte-ci44071890093`.
- Packaged candidate `shim/out/dreamlte-xnu-0209.img`, SHA256
  `1ac1f91771e2e4fffe8535ee2d5338114309be248a6e3e57c2a03188ec3be347`,
  18,427,920 bytes, within the S8 BOOT partition. Kernel strings include
  post-TTBR markers; stock ramdisk, second stage and DTBH match byte-for-byte.
  Android reported boot complete and `/dev/block/sda7` matched the stock
  hash immediately before the trial.
- Flashed 0209 to BOOT only via Heimdall 2.2.2. It reported
  `BOOT upload successful`. The phone is currently absent from ADB, USB and
  Heimdall after reboot; screen and XNU progress are unknown. Next: return to
  download mode, restore and hash-check stock BOOT, boot Android, and collect
  `/proc/last_kmsg` before deciding the next kernel change. Protected
  partitions and USERDATA remain untouched.

## 2026-11-17: DWC3 logging probe 0210

- Restored stock BOOT after 0209, verified its SHA256 as
  `71fb593969288f3a5a5dc6c4c4da35a53b045650cc293c6e8e4028ac3a7982a5`,
  booted rooted Android and captured its 47,578-byte `/proc/last_kmsg` over
  ADB USB. The XNU trace still ends at `physmap ready; switching TTBR0`.
- Android reports Exynos DWC3 at `0x10c00000`, Samsung PHY at `0x10e00000`,
  and high-speed UDC mode. The donor A03 console uses a different MUSB PHY;
  its PHY init/reset sequence is not portable. Existing SWEET DWC3 EP0 code
  is a reference for a future S8 transport. A full DWC3 gadget/stream is not
  implemented by this probe.
- Added a guarded, read-only DWC3 register snapshot to the DREAMLTE loader
  trace (`GSNPSID`, `GCTL`, `DCTL`, `DSTS`, `DCFG`) and an ADB USB helper for
  retrieving `/proc/last_kmsg` after Android returns. The helper was tested
  against the current phone. No DWC3/PHY writes were added.
- Loader build passed. Candidate `shim/out/dreamlte-xnu-0210.img` is
  18,427,920 bytes, SHA256
  `f0cf2d324e00813bed697b9d4bf857fcc290c2de054a5f93eeec2f9166fc1cd1`.
  It contains the existing 0209 kernel payload; stock ramdisk, empty second
  stage, DTBH and Exynos8895 entry match byte-for-byte. It fits the 41,943,040
  byte BOOT partition.
- After verifying the stock BOOT hash, flashed candidate 0210 to BOOT only
  with Heimdall 2.2.2; upload succeeded. The phone stopped enumerating after
  reboot and remained absent from ADB and Heimdall for 45 seconds. Heimdall
  then detected download mode; restored stock BOOT and confirmed
  `/dev/block/sda7` SHA256
  `71fb593969288f3a5a5dc6c4c4da35a53b045650cc293c6e8e4028ac3a7982a5`.
  Android completed boot, and the 47,726-byte trace was captured with the
  ADB helper to ignored `last-kmsg-0210.txt`.
- 0210 trace reports `GSNPSID=0x5533280a`, `GCTL=0x30c12004`, `DCTL=0`,
  `DSTS=0x00520004`, and `DCFG=0x00080804`, then the same XNU milestones as
  0209, ending at `physmap ready; switching TTBR0`. These raw loader-time
  DWC3 reads confirm access to the controller block, not USB enumeration or
  stream operation. RECOVERY, bootloaders, EFS/CPEFS and USERDATA remain
  untouched.

## 2026-11-17: correct snapshot mappings after TTBR0 (0211)

- Revalidated rooted Android boot complete, stock BOOT hash and recovered
  0210 trace (47,726 bytes). This continuation makes source progress; the
  previous trial also yielded new DWC3 register evidence.
- Found a concrete diagnostic bug in0209: `phystokv()` rejects the snapshot
  cursor/buffer and RAM framebuffer sink, which are below `gPhysBase` and
  outside the managed upper-bank RAM. Its illegal-PA path calls panic.
  Thus the missing stage10 cannot establish a TTBR hardware failure.
- Overlay0211 installs two explicit WB/XN kernel block aliases for the
  already-used snapshot regions before physmap initialization. Relocation
  uses these aliases, never phystokv on low RAM. DREAMLTE putc now appends
  every character (stage numbers, newlines, panic formatting included) and
  skips the unverified framebuffer sink. Donor behavior remains unchanged.
- Validation: dry-run against exact0209 source passes; profile stages132
  patches; both modified translation units compile to ARM64 objects with
  gnu11/general-register-only flags. Actual mapping-helper host check passes
  for both descriptors, cursor/buffer offsets and preserved neighbor slots.
  Loader rebuild passes. Full CI and device test remain required.
- Phone remains in Android with verified stock BOOT; no new flash performed.
- Fix commit660745e pushed to build fork. Full S8 CI44085718513 is queued,
  job134047808756 (macos-15-intel), exact head
  660745e28657cd55e51d69a37b8a22dd0e1e1951. Live watch session87525.
  https://github.com/stonedDiscord/ios-a5xelte/actions/runs/44085718513
  Superseded dispatch44085601704 used0210; do not use its kernel for0211.
- Rechecked Android USB: UDC10c00000.dwc3 reports high-speed/configured.
  This is Android's transport; bare XNU USB enumeration remains unverified.
- During CI, captured the live Android debugfs DWC3 regdump privately and
  reviewed Exynos8895 Linux PHY/wrapper source at3cfb914658ab. Recorded
  measured core state, DMA upper-address evidence, Exynos VBUS override,
  PHY version-dependent register-base adjustment and next transport gates in
  docs/dreamlte-usb.md. No PHY or controller writes were performed.
- CI44085718513 re-polled by GitHub API: job134047808756 is in progress,
  Build active; dependency/setup steps succeeded. Watch33999 subsequently
  hit a network timeout, not a terminal build result. Continue polling this
  exact run rather than dispatching a replacement. No new BOOT flash yet.

## 2026-11-17: opt-in S8 ECM transport candidate0212

- Previous turn made progress through measured USB/source evidence; exact
  CI44085718513 remains live in its Build step (not a failed/stale job).
- Added0212: reuses the donor DWC3 ECM endpoint/network code under DREAMLTE,
  substitutes S8 core mapping and Exynos PHY VBUS setup, and hooks BSD network
  startup before root discovery. No donor UFS or disk log startup is called.
  Default dreamlteusb=0 does nothing; =1 reads core state; =2 attempts takeover
  only for the measured ID and stopped core/awake PHY. Cold clock/reset PHY
  bring-up remains necessary if those firmware-state preconditions fail.
- Actual staged wrapper host test PASS for opt-in/read-only paths, invalid ID,
  running core, PHY reset/suspend refusal, version-dependent register layout,
  device-mode selection and preserved-bit VBUS writes. Both modified BSD
  translation units compile to ARM64 objects with gnu11/general-register-only
  flags. USB object has no unresolved donor sweet_log symbols. Profile stages
  133 patches. These checks do not prove endpoint/PHY/DMA operation on S8.
- 0212 is not in CI44085718513 (which intentionally builds0211). Keep its
  result/artifact separate; test0211 first, then build0212 for a USB trial.
  Phone is still on stock Android; no new BOOT flash in this continuation.

## 2026-11-17: 0211 BOOT trial

- CI44085718513 SUCCESS at exact660745e: kernel build, DREAMLTE profile
  verification and Cortex-A53 LSE scan all passed. Downloaded exact kernel/
  buildtree and full log privately under /tmp/dreamlte-ci44085718513.
  Kernel SHA256 d6fed9f8a40695d70226f4c58bea6970fb0e0c826c5674faff83c19a1d4c1bbd.
- Packaged shim/out/dreamlte-xnu-0211.img, 18,427,920 bytes, SHA256
  3cf785959bfd645bdcc7edfa2554c6a84dca475f1058076be0ed35172f7034c0.
  Exact profile contains0211 and excludes0212; kernel checksum verified.
  Stock ramdisk/second/DTBH match byte-for-byte; chip8895 and BOOT fit pass.
- Root Android boot complete and stock /dev/block/sda7 hash verified
  immediately before adb reboot download. Heimdall2.2.2 BOOT-only upload
  succeeded and rebooted. ADB, Heimdall and USB enumeration are now absent;
  no runtime0211 marker recovered yet. Screen unobserved.
- Requested physical forced restart/download mode so original BOOT can be
  restored, hash-checked and Android last_kmsg recovered before another trial.
  No RECOVERY, bootloader, EFS/CPEFS or USERDATA writes performed.
- ECM candidate0212 committed9f90d9f/84f0922 and pushed; pristine artifact
  plain-apply and whole-file comparison match locally compiled BSD sources.
  It is not yet full-CI/device tested. Do not confuse it with this0211 trial.

## 2026-11-17: recovered0211; caught silently skipped overlays

- User reports Samsung logo during0211, then returned phone to Download
  Mode. Restored stock BOOT with Heimdall, booted Android solely to retrieve
  diagnostics, rooted ADB and verified stock /dev/block/sda7 SHA256. Captured
  47,734-byte last-kmsg-0211.txt privately; final marker still TTBR0 boundary.
- CRITICAL correction to prior claims: extracted actual CI44085718513 source
  does NOT contain0209 or0211. Its manifest lists staged patches, not applied
  patches. The compiler used0208-era logger, which explains missing digits/
  newlines. Thus this trial did not execute0211; its green CI/profile checks
  were insufficient proof of the intended patch set. Earlier0209/0210 also
  need to be interpreted as0208-era kernel diagnostics.
- Reproduced0209 rejection with the build system's actual git apply --check.
  Its short-context hunks worked with GNU patch (including fuzz) but failed
  git apply. Regenerated0209 with full context from exact artifact source;
  now plain git apply accepts0209,0211 and0212 in sequence. Four resulting
  sources match local ARM64 compile inputs (after normalizing logger indent).
- CI now fails immediately if a DREAMLTE overlay cannot apply, requires
  linked snapshot/USB symbols plus actual mapping helper in compiled source,
  and runs the wrapper host test against staged USB source. Embedded workflow
  Python and modified dxb bash syntax validated. This closes the false-green
  gate before any further phone trial.
- Cancelled obsolete0212 run44090286065 (997a740) because it could silently
  skip the same logger fixes. A corrected combined logger+USB CI is next.
  No new flash until that verified build; stock BOOT is restored. Android is
  a diagnostic recovery checkpoint, not the target runtime. User explicitly
  emphasized progressing to running XNU with USB.
- Corrective commit5ac173d pushed; combined logger/USB CI44091780583
  dispatched at exact5ac173d (DEVELOPMENT/HEROLTE, dreamlte, macos-15-intel).
  https://github.com/stonedDiscord/ios-a5xelte/actions/runs/44091780583
  Poll this run; inspect actual sources and linked symbols before packaging
  the next candidate with dreamlteusb=2.

## 2026-11-17: persistent console and correct4K alias range (0213)

- Prior goal turn made source/build-gate progress. Revalidated exact combined
  CI44091780583 live in Build and Android connection; no new flash performed.
- Found snapshot alias used VM_MIN_KERNEL_ADDRESS, which differs from
  LOW_GLOBAL_BASE_ADDRESS in the actual4K non-large-memory kernel. The
  latter's L2 tables are initialized and its8MiB range is VM-reserved. Changed
  0211 alias to LOW_GLOBAL_BASE_ADDRESS+2MiB (cursor) /+4MiB (buffer), avoiding
  an uninitialized L1 slot. The former host model assumed ARM_LARGE_MEMORY;
  it did not validate this actual build layout.
- Added0213: keep bounded snapshot output active through stage20 and normal
  kernel lifetime, register it as serial output without framebuffer writes.
  This closes the diagnostic gap between pmap and BSD USB startup.
- Five modified translation units compile to ARM64 objects (gnu11/general
  regs only). Plain git apply on fresh exact CI source plus full five-file
  comparison to compile inputs PASS. USB wrapper host checks still PASS.
  Profile stages134 patches; CI also checks linked snapshot serial provider.
- Added host live-USB checker for real EP0 descriptors/status/configuration,
  ECM interface identity and optional three ping replies. Help/syntax and
  missing-device reporting checked; no hardware pass claimed.
- Cancelled44091780583 before flashing because this address/console fix is
  needed for the meaningful USB trial. Corrected combined build follows.
- Corrected combined logger/USB/serial commitfe42384 pushed. CI44094150615
  dispatched for DEVELOPMENT/HEROLTE dreamlte on macos-15-intel.
  https://github.com/stonedDiscord/ios-a5xelte/actions/runs/44094150615
  Exact source/kernel inspection remains required before USB-enabled BOOT.
  Final Android boot-complete/stock BOOT hash check passed; all protected
  partitions and USERDATA remain untouched.

## 2026-11-17: USB0213 trial; new user direction and framebuffer0214

- User explicitly prohibits restoring Android again. Do not flash stock BOOT
  for log recovery. User additionally authorizes converting the local IPSW
  and flashing the converted iOS filesystem to existing USERDATA/sda24.
  Preserve partition table, RECOVERY, bootloaders and EFS/CPEFS. USERDATA was
  measured at58,556,678,144 bytes before leaving Android.
- CI44094150615 SUCCESS. Actual five complete source hashes and six linked
  symbols verified, matching reviewed0213 inputs (not just patch staging).
  Kernel SHA2564bb81128dbc81c320f53e20a1d2d6521f988bd446a75b2422364beb848976f5f.
  New reusable content verifier rejects older false-green artifacts.
- Packaged0213 with dreamlteusb=2, candidate SHA256
  3fdc26f35563267c167ed865bc6da99508dc4684857b53f27c147ea70b04ea1d,
  18,427,920 bytes. Stock header/ramdisk/DTBH preserved. BOOT-only Heimdall
  upload successful. User reports Samsung Galaxy logo; no host USB gadget.
  Runtime markers unavailable;0213 remains installed. Android NOT restored.
- Local IPSW iPhone10,3,iPhone10,6_16.7.16_20H392_Restore.ipsw identified,
  d22ap OS087-86698-044.dmg, SystemOS087-86593-047.dmg, AppOS087-86715-047.dmg.
  All extracted privately to research/dreamlte/root/assets. Built APFS-FUSE
  locally and mounted all three read-only; launchd and arm64 dyld cache exist.
  Conversion to HFSX/root staging and USERDATA flash remain unfinished.
- User requested framebuffer console based on kernel source. Reviewed
  Exynos8895 dpu decon_reg_set_trigger/regs-decon.h at3cfb914658ab:
  DECON_F0x12860000, trigger+0x70, HW enable bit0, mask bit4, auto-mask bit12.
  S7 trigger bits are not valid S8 enable sequence. Buffer0xcc000000 is
  supplied by live s3cfb.bootloaderfb; measured1440x2960/stride5760.
- Added loader fbtext and overlay0214: early framebuffer output until TTBR0
  retirement, then RAM-only gap until serial init maps scanout with
  ml_io_map_wcomb and mirrors normal output to both RAM and display.
  Loader builds; three affected ARM64 compile checks and plain git apply/
  full-source equality pass. Physical scanout still needs trial verification.
  No claim that source addresses alone prove displayed output or live USB.

## 2026-11-17: framebuffer bootstrap mapping correction

- CI44111718665 at ae6094f succeeded, but is NOT approved for flashing:
  review found0214 moved framebuffer from L1 slot2 to slot3 while0206
  still installed snapshot descriptors in the framebuffer L2. This loses
  snapshot low aliases after MMU enable. No phone write used that artifact.
- Corrected0214 to allocate a separate low-RAM L2 for snapshot cursor/log.
  The current profile fits the eight-page bootstrap allocation. Exact0213
  artifact plus plain git apply matches all seven reviewed complete sources;
  start.s now joins the mandatory source-hash check. Corrected actual start.s
  compiles to ARM64. Previous local start.s sandbox lacked0206; it was
  replaced with the actual artifact source before this check.
- Expanded USB source map through Exynos8895 CMU/FSYS0 gates, Q-channel,
  reference selector and PMU isolation; see docs/dreamlte-usb.md. No new
  PMU/clock writes or successful USB runtime claimed. Phone remains in
  Download Mode on0213 BOOT; no Android restoration performed.

## 2026-11-17: converted20H392 root passes host validation

- Corrected framebuffer full CI44115872187 dispatched at7e95994; now Build
  in progress. Poll that exact run;44111718665 is superseded. No new BOOT
  flash yet. Phone is visible in Download Mode; Android was not restored.
- Added userspace HFSX conversion tools. Patched private libdmg-hfsplus
  UTF-8 decoding and allocation offsets above4GiB; forced high-offset/Unicode
  smoke image passes fsck. Original full attempts were rejected before flash
  due to these issues and cryptex symlink traversal; final generator skips
  already-supplied symlink subtrees. No phone write used incomplete images.
- Final root image research/dreamlte/root/ios-16.7.16-20H392-hfsx.img is
  34,359,738,368 bytes, below measured58,556,678,144-byte USERDATA. Full
  read-only fsck PASS. Extracted launchd and all43 dyld-cache components
  match source SHA256 byte-for-byte (44 comparisons). Mode/UID/GID checks
  passed for launchd, logd markers and plaintext keybag. Root has both
  cryptexes; hard links are materialized as copies.
- Image is non-journaled; xattrs/BSD flags/timestamps are not preserved.
  These conversion limits are documented in docs/dreamlte-root-conversion.md.
  No claim of metadata-complete restore, runtime mounting or userspace boot.
- Heimdall2.2.2 source inspected:64-bit total-byte packet and64-bit host
  unsigned-long offsets handle this image size. USERDATA write is explicitly
  authorized; preserve PIT and all other partitions. Flash remains pending
  until final image checksum is recorded.

- Further0214 source review added required command-mode frame requests:
  DECON SHADOW_REG_UPDATE_REQ+0x60 bit31 before HW unmask at+0x70, matching
  decon_reg_update_req_and_unmask. Loader presents after drawing; early XNU
  maps DECON's L1 slot0 (seven of eight bootstrap pages total); normal serial
  maps DECON MMIO and presents each character. Three affected ARM64 files
  compile; all seven complete source hashes match plain apply to actual0213.
  CI44115872187 lacks this frame-request change and is superseded.
- Converted root SHA25635427cc9d9f40b6383afabf1b0f5370ebc4f85a42d3f079708b6548121dca3e7.
  Raw USERDATA Heimdall upload failed at its first sequence confirmation
  (reported0%); session end failed too. USERDATA may be partially written;
  do not claim deployment success or restore Android. USB still Download
  Mode. Requested phone-side error text; converting the same validated HFSX
  image to Android sparse format and checking expanded hash before retry.

- Final framebuffer CI44119574729 dispatched at9498204. This is the required
  frame-request+separate-L2 build; poll exact run without replacement.
- Android sparse image15,409,217,756B passed complete expanded-image SHA256
  equality to the validated32GiB HFSX. Sparse USERDATA retry with --resume
  failed to begin session (no payload sent). Asked for physical forced restart
  and re-entry to Download Mode to reset the failed raw-upload USB session.
  Pending user physical action; no Android restoration/other partition write.

- Additional read-only HFS-image cache prerequisite check PASS: all42 declared
  subcache UUIDs, mapping bounds, symbols UUID and required core dependency
  names; cache has2710 image entries. This supplements full content hashes
  without claiming signature/runtime verification.

## 2026-11-17: source-derived USB2 wake/timing follow-up

- Previous turn classified as progress (framebuffer fixes, validated root and
  attempted USERDATA transport). Re-polled exact CI44119574729 at9498204: now
  in_progress, Build active. No restart or replacement dispatched. Phone
  still enumerates Download Mode; physical session reset response pending.
- Further pinned Linux core.c review found existing takeover omits USB2
  ENBLSLPM/SUSPHY clear and post-reset suspend-clock scale. Prepared0215
  outside the active profile under xnu/dreamlte-next: guard core/USB2 PHY
  reset, preserve board config while waking USB2 before reset, set GCTL
  PWRDNSCALE=4125 for measured/live-DT66MHz after reset, clear vendor bits6/7.
- Actual wrapper host checks PASS for both0214 and0215, including all32 GCTL
  bit preservation cases and new reset refusals. 0x30c12004 becomes0x80e92004,
  agreeing with prior working Android dump. Plain apply/full-source equality
  PASS; modified USB translation unit ARM64 compile PASS (gnu11/general regs).
  These are host/source results, not S8 enumeration. No new phone write.
-0215 intentionally not part of CI44119574729 or current source-hash manifest.
  First test0214 display, then promote0215/update hashes/build if warranted.
  Next USB source SHA256df5d49b67402780ee2b3f347197b80c407a4c81598593cb8916082cda262770b.

## 2026-11-17: read-only Download Mode session recovery check

- Re-polled exact framebuffer CI44119574729: in_progress, Build active at
  job134168348363 (started16:06UTC). This is a verified wait, not a stopped
  build; no restart dispatched. Prepared0215 remains outside active profile.
- Tested a fresh read-only download-pit --no-reboot handshake to avoid
  unnecessarily requiring physical buttons. It failed sending the handshake;
  no PIT downloaded and no partition payload sent. Host PyUSB reset_device
  subsequently returned ENOENT/Entity not found; phone now absent from lsusb.
  These operations cannot establish a recovered flashing session. Existing
  physical Download Mode re-entry request remains necessary. No Android
  restoration or additional BOOT/USERDATA/protected partition write occurred.
- Host live gadget checker still finds no1209:0001. Objective remains
  unachieved: no verified framebuffer trial, XNU USB enumeration or transfers.

## 2026-11-17: exact-run artifact preparation waiting on CI

- Previous turn made new recovery evidence; current continuation revalidated
  CI44119574729 still in_progress/Build and phone absent from USB. No reset
  response yet. No new CI, firmware or partition writes.
- Started sequential host preparation session71698: wait for exact9498204
  CI44119574729 success, download kernel/buildtree under
  research/dreamlte/ci-44119574729, verify all seven actual source hashes and
  linked symbols, rebuild loader/ADT and package shim/out/dreamlte-xnu-0214.img
  with dreamlteusb=2. It writes prepared-boot.json only after all checks pass.
  It performs no flash. Preparation is waiting on the confirmed-live CI;
  do not restart due to an observation timeout. Watch session13877 also lives.

## 2026-11-17: exact framebuffer0214 candidate ready; hardware blocked

- CI44119574729 SUCCESS at9498204f7e3446d523d4420fcdef683f4e07f5d5.
  Build, profile verification and Cortex-A53 LSE scan passed. Preparation
  session71698 completed successfully; exact artifacts under
  research/dreamlte/ci-44119574729. Kernel SHA256
  2c76fa250cc0c9c38f17d17f75ac7b8470d74bb8580e2aebcd2760bea5bf4214.
- tools/dreamlte-verify-ci.py PASS for all seven actual compiled source
  hashes and six linked symbols. Packaged shim/out/dreamlte-xnu-0214.img,
  18,432,016 bytes, SHA256
  fa8b862c1eb4e054ca581d45cc5957f7327b8f4cfd3432375471d49aa85a14b3.
  Exact appended payload uses dreamlteusb=2. Independent comparison verifies
  stock ramdisk/second/DTBH and load/header fields unchanged, chip8895,
  fit within41,943,040-byte BOOT. This is prepared, NOT flashed/runtime proven.
- Phone remains absent from USB. The physical Download Mode/session-reset
  blocker has persisted across more than three consecutive goal turns.
  Fresh read-only handshake and host USB reset both failed; no new writes.
  All currently useful independent preparation is complete. Goal blocked
  pending user physical re-entry to Download Mode and phone-side error text.
- Next hardware actions remain authorized: sparse converted root to USERDATA
  with --no-reboot, then verified0214 BOOT (resume same successful session).
  Never restore Android. Verify visible loader/XNU text and actual host
  enumeration/control transfers/bidirectional data before claiming success.
  Prepared0215 stays outside the active profile pending diagnostic evidence.
