# A03 userspace cross-reference (2026-11-15)

Patch numbers belong to each port's series: A03 0117 is USB ACM break
capability; A5XELTE 0117 is HFS atomic rename. They are not matching versions.

## Version and provenance

| Tree | Inspected source | Distinction |
| --- | --- | --- |
| A03 | kernel d640287; XNU8796.141.3, HFS627.100.6 | BOOT0060 uses iPhone X iOS16.0/20A362, verified from staged SystemVersion.plist.0121 CI43756243470 pending. |
| A5XELTE | historical atomic-rename commit8c3900f; progress entries0116–0117 | Recorded iPhone8Plus iOS16.7.16 crash has exact same nil NSURL system-container failure. |
| HEROLTE | tracked0200/0201 board/AMFI patches and progress | Inherits A5XELTE flag/shared portable fixes; Sandbox registration and later Hello/home-screen recorded. |
| SWEET | /home/stoned/Documents/GitHub/ios-sweet at45263be | Exact donor revision pinned by tools/a03-build-profile.py.0050/0052/0057/0064 added source matches our copies. |
| HakiOS | /home/stoned/Documents/GitHub/hakios-xnu-kernel at63fc2b4 | VERSION2.3.4-hakios, Darwin22.5.0/XNU8796.121.2; not an ABI-identical replacement. |

## Portable differences

| Facility | Other ports | A03 evidence |
| --- | --- | --- |
| Sandbox API | Donor0050 registers Sandbox; A5 historic0106/HEROLTE0201 bridge registration. Most requests succeed, selected paths/tokens ENOENT. | Profile omitted0050. BOOT0060 proves op2 ENOPOLICY103 in media/backboard/container/notify.0121 implements decoded scalar check only, explicit a03_sandbox_disabled=1, unknown ops ENOTSUP. Runtime pending. |
| HFS RENAME_SWAP | Donor0052 uses VNOP_EXCHANGE after ENOTSUP for two regular files on one mount. A5 0117 extends SWEET guard to A5XELTE; HEROLTE inherits flag. | Not selected. BOOT0059 UMD cannot save persona.kb/usersession.kb, ENOTSUP45. Strong next candidate after isolated Sandbox test. |
| External ACL resolver | Donor0057 removes config_ext_resolver. A5 0085/HEROLTE0200 FILESYS_BASE omit it. Donor records unavailable memberd resolver breaking group ACL entries. | A03 MASTER.arm64.sweet includes it; generated bsd Makefile confirms -DCONFIG_EXT_RESOLVER. Proven build difference, not yet an observed A03 EACCES cause. |
| Work intervals | Donor0064 grants PRIV_WORK_INTERVAL via Sandbox mpo_priv_grant; included in A5 lineage/HEROLTE shared source. | Profile omits0064;0121 has no privilege hook. sys_work_interval.c requires privilege1008 for non-root CREATE2. Later UI prerequisite, not captured null-listener cause. |

## Comparable hardware evidence

A5XELTE_PROGRESS.md 0116 confirms backboardd's system-container entitlement
but nil NSURL abort and UMD manifest saves failing ENOTSUP. After0117 its
recovered window shows one backboardd exec, one SpringBoard exec, five BGRA
swaps, and no nil-URL/UMD ENOTSUP in that window. This supports testing the
portable filesystem fix; it does not prove A03 will behave identically.

SWEET NOTES.md records the same BaseBoard libraryPath/cachesPath exception
at0051. Sandbox correction removed IPC denials but not that exception.
Creating container parents and HFS swap support preceded0052 backboardd
surviving/display opens. A03 staged root already has those parents, and
BOOT0060 records mkdir EEXIST for /private/var/containers. No blind root rewrite.

SWEET's later mediaserverd failures were in VirtualAudio HAL and camera
prewarm calling null GL. A03 currently faults earlier in
CFDictionaryGetValue(NULL), called by FigNotificationListenerStartNotifications
while waiting for AirPlay predictions. Later donor workarounds do not prove
this failure's cause.

## HakiOS reference

xnu/files/bsd/kern/kern_minimac.c registers AMFI/Sandbox, grants
PRIV_WORK_INTERVAL, and checks other privileges against signature entitlements.
Request4 derives a container path from CFFIXED_USER_HOME in the target's
argument/environment area. Useful for app extensions; not a demonstrated
fix for A03 system-container XPC lookup. Other requests mostly return0
without outputs. Its own docs/driver-review/policy-glue.md notes unwritten
extension buffers. Do not transplant generic-success API behavior.

No hardware/MMIO/USB/storage/partition/display implementation is portable
merely because userspace is similar. Only A03 is connected for these tests.

## Next checks

1. Complete existing0121 CI/BOOT0061 and measure actual service progress.
2. Adapt/test HFS atomic-swap fallback with A03 filesystem/writable-root
   guards; verify persona saves and backboardd lifecycle.
3. Reconcile ACL resolver/work-interval support against actual failures.
