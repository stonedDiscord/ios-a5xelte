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
