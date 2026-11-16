# A03 progress applied to DREAMLTE

Reference: `build/a03-bringup` at
`f1e16010e5a1b7d94657a867158a81bad0788682` (2026-11-15).
The A03 is a UNISOC T606 device with native 16K support, GICv3, eMMC/SDMA
and a different USB controller. DREAMLTE remains the Exynos8895, 4K,
GICv2, single-A53 profile. Do not merge the A03 machine/loader profile.

A03 BOOT0069 has a successful kernel build and BOOT deployment. BOOT0068
captured four SpringBoard page-in waits at the eMMC mutex, with cumulative
CPU/runnable times. Backboardd submitted full-screen frames, and the user
reported an Apple logo. Home screen/input and the performance effect of
0069's read-lock yield remain unverified in that branch's latest record.
None of these are S8 hardware results.

## Adaptation map

| A03 work | DREAMLTE application |
| --- | --- |
| 0084–0089 early checkpoints/code generation | Existing S8 early markers retained. General-register code generation added in the correct BSD, osfmk and IOKit make components and HFS objects. A03's optional interrupt-mask experiment is not imported. |
| 0087 A55 match, EL2 transition, 16K loader | S8 measured A53/EL1 and existing 4K loader retained. |
| 0090/0092/0094/0096/0098/0099 SDMA, root selection, catalog/direct reads, unsealed mount | Requires an S8 UFS provider and validated geometry. No eMMC controller or A03 USERDATA path imported; S8 USERDATA stays untouched. |
| 0091 XML entitlement provider code generation | Applied to SweetEntitlements. Existing donor XML/platform-binary support retained. |
| 0100/0101 init trap and HOST/MIG evidence | Ported with DREAMLTE names, including pre-core-dump launchd trap registers. |
| 0102 invalid reply and port construction evidence | Ported with a shared bounded failure-report budget. |
| 0105 iOS16 provisional reply compatibility | Opt-in `dreamlte_ios16_provisional_reply=1`; requires provisional reply, iOS platform and SDK major16. Normal receive-right/disposition checks remain. |
| 0107 software key store | Already inherited in 0038. No A03 duplicate provider registered. This supplies no SEP/passcode protection. |
| 0108/0116/0118/0119/0128 daemon crashes | Ported: two reports per selected daemon, 24 frames, bounded version5 Mach-O crash annotations and explicit exit reasons before corpse limits. Includes analyticsd/dmd/tccd. |
| 0093/0095/0103/0104/0106/0109–0111/0113/0115/0117 USB console/PHY/download | UNISOC registers, endpoint setup and reset sequence excluded. Requires S8 DWC3/PHY investigation. No A03 download command or PMU write imported. |
| 0112/0114 watchdog stand-in | Donor already has a software watchdog provider. A03 disabled-watchdog capability and boot-stage behavior require a matching runtime ABI test; not a hardware watchdog implementation. |
| 0120/0126 startup syscalls | Ported: opt-in selected-process errno, path and entitlement-header evidence. No syscall result changes. |
| 0121 scalar Sandbox API | Replaces broad donor success on DREAMLTE: explicit lab opt-in, copies out the decoded 64-bit op2 result; unknown operations return ENOTSUP. |
| 0122 HFS atomic swap | Already inherited in 0052/0117. A03's device-name gate cannot be used without S8 storage. No filesystem writes performed. |
| 0123/0127 software surfaces/display | Existing 0046/0047/0068 providers retained. Donor selector3 already accepts dimensions without interpreting them as a layer index. No S8 framebuffer node published until scanout is verified. |
| 0124 work-interval grant | Replaces broad donor grant on DREAMLTE: explicit opt-in, calling credential, exact privilege and validated boolean entitlement. Requires the lab Sandbox policy. |
| 0125 userspace logs | Opt-in bounded duplicate-uio inspection of GUI writes to /dev/null; original write consumption retained. |
| 0129/0132 GUI snapshots | Ported: four timed passes, up to24 threads and12 frames, retained task-map/thread references, reads/printing after task unlock, no-fault bounded waiting kernel stacks, user/system/runnable times. |
| 0130 HOST diagnostic budgets | Ported: eight normal reports per site, separate16 failure budget; IPC decisions unchanged. |
| 0131/0133 durable batching/read-lock fairness | Specific to A03 eMMC. S8 has no ported UFS provider to optimize; no measured S8 speedup claimed. |
| 0134 platform product name | S8 donor already uses IODTPlatformExpert's ADT model/compatible rather than hardcoded Redmi names. SM-G950F/DREAMLTE remain in its ADT. |
| Root-image tools | Portable root tweaks now read actual SystemVersion build/version, as on A03. A03 installers, pinned firmware/root hashes, GPT validators and write authorization are not S8 tools. |
| CI | Explicit ARM64 target, linked S8 diagnostic-symbol/string checks, hash manifest in artifacts. Existing A53 LSE scan retained. A03's disabled/truncated KDK-cache workaround is not needed here. |

The implementation is the S8-only overlay
`xnu/dreamlte/0205-dreamlte-a03-portable-bringup.patch`, after0204. The
stager now includes both overlays:128 patches total. Each generated
`DREAMLTE-PROFILE.json` records the reference commits and file hashes.
Other board profiles do not stage these overlays.

## Reproduce host verification

```sh
python3 tools/dreamlte-test-portable.py
python3 tools/dreamlte-test-reply-compat.py
python3 tools/dreamlte-build-profile.py /tmp/dreamlte-patches-NEW
sh shim/dreamlte/build.sh
python3 tools/mkadt_dreamlte.py /tmp/dreamlte-NEW.adt
```

The helper tests compile actual overlay code with fake kernel APIs: unsupported
Sandbox operations and user-copy faults, entitlement/credential/privilege
gates, crash selection and saturation, malformed annotation mappings, HOST
budgets and four-pass sampler selection/timing. These are host tests, not
hardware or scheduler simulation.

The exact previous S8 CI43434858911 build tree provides generated headers
for local arm64 object compilation. `tools/xnu-cc.py` accepts `XNU_CC` and
`XNU_CI_DXB` overrides; the latter for this fork is
`/Users/runner/work/ios-a5xelte/ios-a5xelte/dxb`. Set
`XNU_CC_POST=-mgeneral-regs-only`. Objects and downloaded trees stay ignored.
Use plain `git apply` to verify the overlay against a pristine build-tree
copy, and compare complete resulting files with the compiled inputs.

## Runtime options and remaining S8 prerequisites

Keep the initial kernel-only command line from dreamlte-bringup.md. All
new optional runtime modes default off:

| Argument | Effect |
| --- | --- |
| `dreamltecrash_log=1` | Bounded selected-daemon crashes and startup syscall evidence |
| `dreamlte_sample=1` | Four GUI task snapshots at180/300/420/540seconds |
| `dreamlte_userlogs=1` | Bounded GUI /dev/null log capture |
| `dreamlte_ios16_provisional_reply=1` | Scoped older-userspace reply compatibility |
| `dreamlte_sandbox_disabled=1` | Lab scalar-check Sandbox policy; no profile/token/path emulation |
| `dreamlte_work_interval=1` | Entitled work-interval grant through that policy |

Do not enable userspace modes as a substitute for a working S8 rootfs.
`tools/dreamlte-symbolicate-kernel-waits.py KERNEL LOG` resolves traces
against the exact matching linked kernel, without a KASLR slide.

Next device milestones remain: connect kernel console output to the verified
Exynos snapshot recovery path, recover an actual S8 XNU boot, then validate
S8 scanout and bounded UFS reads before preparing a compatible root. The
existing snapshot probe proves a marker survives into Linux last_kmsg; it
does not yet transport XNU console output. BOOT-only trials are authorized;
USERDATA, RECOVERY, EFS/CPEFS and bootloaders remain preserved.

## Read-only userspace tooling

The portable A03 root/cache inspection and symbolication tools are also
available under DREAMLTE names. These inspect supplied host files; they
never install a root or write the phone:

```sh
python3 tools/dreamlte-inspect-ios-root.py EXTRACTED_ROOT
python3 tools/dreamlte-verify-ios-cache.py EXTRACTED_ROOT
python3 tools/dreamlte-symbolicate-cache.py EXTRACTED_ROOT 0xADDRESS --slide 0xSLIDE
python3 tools/dreamlte-test-symbolicate-cache.py
```

Cache tools additionally accept `--hfs-image` for a host HFS image. Use the
matching cache/subcache/symbol UUIDs and captured user cache slide. Their
file/architecture/UUID checks do not prove S8 kernel or runtime compatibility.
No Apple assets are included in the repository.
