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
- tools/dreamlte-build-profile.py: 127 patches (donor through 0203 + S8
  overlay). Excludes later S7 MMIO drivers. Build uses MACHINE_CONFIG=HEROLTE.
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
