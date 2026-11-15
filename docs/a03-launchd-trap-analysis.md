# A03 launchd-task SIGTRAP investigation

Observed on BOOT0044: pid 1 requests shared-region mappings, then exits with
OS_REASON_SIGNAL (2), signal SIGTRAP (5). No core.1 was found in the live
read-only USERDATA HFS catalog after the user reported dump completion.
This proves dyld activity in the launchd task, not launchd main-loop success.

## Binary evidence from ReVa, 2026-11-15

Imported live USERDATA binaries into the local Ghidra project as /dyld and
/launchd with version control disabled. Analysis completed and saved (dyld:
2713 functions; launchd:3370). Private binaries remain ignored. Their hashes
match the pinned root: dyld e5768eb084e29b0ebdab8b55ce3505d988f5e1a3caf6e17a715fedf7e2691873;
launchd314a84ce1540ba36ea8a30f1f47941c67aa0cebb3bee26a2c591b39a1bb5f666.
Addresses below are image-relative for dyld, preferred VA for launchd;
subtract observed runtime load addresses before comparing a future trap.

- dyld _dyld_halt at0x5fc58 formats a diagnostic, stores its pointer in
  crash-info storage0x841c0 and executes BRK at0x5fcd0. Assembly preserves the
  message in x19. Several ignition/cryptex error paths reach this function.
- dyld dyld4::halt at0x171b0 is a different termination path: it copies text
  into error_string0x84af0 and dyld_all_image_infos.errorMessage (+0x38),
  calls abort_with_payload with namespace6 (DYLD). It is not by itself proof
  of a raw SIGTRAP. Callers include missing libdyld, missing executable entry,
  dependency diagnostics and shared-cache configuration failures.
- dyld __pthread_set_self at0x1474c has BRK0x147a8 when thread_selfid fails;
  it records the failure string at0x841c0. Additional libplatform/lock BRKs
  exist. No actual trap address has been observed yet.
- launchd LC_MAIN points to0x100014038. Early entry marks
  kern.initproc_spawned, installs an os_crash callback, validates pid1/stdout,
  initializes descriptors and logging, then configures memory/wake policies.
  A proc_disable_wakemon failure invokes os_crash and reaches a BRK in the
 0x1000145ac vicinity. This is a candidate, not an observed failure.

## Filesystem and kernel evidence

Live cache inventory passes40 declared subcache UUIDs/mapping bounds,
symbol-cache UUID and2663 image paths. Does not establish all cache payload
hashes or successful mapping. launchd and dyld byte comparisons pass.

Exact XNU vm_unix.c falls back from missing trust-cache membership to root
ownership checks. A not-in-trust-cache line alone does not prove the mapping
failed. Do not bypass this based on the warning alone.

## Next measurement

Patch0100 logs initproc SIGTRAP before coredump: PC/LR/SP/FP, main/dyld load
bases, cache slide, instruction, bounded x19 text and six frame pointers.
Use its observed address/message to distinguish loader failure, pthread/
libplatform assertion, launchd assertion or another crash. Combined build
43712255840 includes0100 and smaller XNU font. No binary patch is justified
until that runtime evidence exists.

## BOOT0045: observed libpthread assertion

The runtime PC0x1e6f71f5c minus cache slide0x19274000 is0x1cdcfdf5c;
LR0x1e6f6841c unslides to0x1cdcf441c. Both lie in cached
/usr/lib/system/libsystem_pthread.dylib, base0x1cdcef000.
Cache .23 file0x2fa1f5c contains200020d4 (BRK#1). The assertion at
0x1cdcfdf38 stores "BUG IN LIBPTHREAD: host_info() failed" and sign-extended
w0 into crash-info, then traps. The caller initializes count8 and invokes
host_info(host,5,buffer,&count); nonzero return branches to this assertion.
Kernel flavor5 is HOST_PRIORITY_INFO, also count8. This supersedes the
unresolved candidate paths above; why the call fails remains under audit.

ReVa program /libsystem_pthread.text-only.dylib is an offline TEXT-only
extraction from the pinned cache with a rewritten standalone header;
295 functions analyzed/saved. It is not an intact dylib and absent data or
linkedit must not be treated as actual zero data or unresolved runtime code.
Apple bytes and generated disassembly remain private/ignored.

Added0101 diagnostics: trap x0/x8 (the assertion preserves its error in x8),
x20/x21/x22 (x22 holds host port in this initializer), msg2 request options,
host_info request host validity/count, MIG request/reply status/size.
No return values or security checks changed. Four affected source files pass
local syntax checks using recovered CI commands (environment/header warnings
remain). Full CI/link/runtime validation pending. Physical Download absent.
Direct cached branch stubs also resolve to libsystem_kernel host_info at
0x1bf1361a4, message ID200, and host-self target0x1bf1307f8.

## 2026-11-15: BOOT0046 identifies invalid reply right; font confirmed

User reports PC0x1e41d5f5c, cache_slide0x164d8000 (unslid PC0x1cdcfdf5c,
same cached pthread host_info assertion), dyld0x102898000,
x19=0x16d60bde8, x0=x8=0x10000009, x20=0x102921e00,
x21=0x16d60bdf0, x22=0x503, instruction0xd4200020,
frames0x1e425c778/0x10289ebdc/0x1028edd08.
XNU message.h defines0x10000009 as MACH_SEND_INVALID_REPLY, not invalid
destination (0x10000003). x22 retains the host port name0x503. This narrows
the failure to reply-right transport/validation; host_info handler failure is
not established. Requested A03 HOST msg2/MIG lines to identify reply name.
User explicitly confirms XNU font is now fine. No new flash/root write yet.

## 2026-11-15: host_info request rejected before MIG dispatch

User supplies A03 HOST msg2 options=0x200000003 size40 remote0x503 reply0x603;
no MIG output. Combined send/receive, kobject call; cached host_info uses
MAKE_SEND_ONCE reply disposition. With observed MACH_SEND_INVALID_REPLY,
next measure receive-right lookup/type/semantics and port construction.
Added0102 diagnostics for ID200 invalid-reply branches, snapshotting entry
bits/semantics under existing space lock and printing after unlock; PID1
mach_port_construct logs flags/status/name. No validation bypass or forced
success. Both affected files locally compile using exact CI headers/flags;
patch reverse/forward roundtrip zero-fuzz PASS. No new phone write yet.

## BOOT0047: rejection identified, compatibility candidate0105

User's exact trace: construct flags4000 rv0 name603; invalid reply603,
type21 (MAKE_SEND_ONCE), entry1, bits38200000, semantics3, destination4.
The RECEIVE right is present. IPC rejects provisional reply semantics3
against strict kernel-object semantics4 before MIG dispatch. Kernel XNU22.6
strictness applies to platform binaries; live launchd LC_BUILD_VERSION is
PLATFORM_IOS2, minOS16.0, SDK16.0. Its libsystem_kernel mig_get_reply_port
uses MPO_PROVISIONAL_REPLY_PORT4000. This is the measured compatibility
mismatch behind MACH_SEND_INVALID_REPLY10000009 and the pthread BRK.

Candidate0105 introduces opt-in a03_ios16_provisional_reply=1. Only
PLATFORM_IOS processes with SDK major16 and an actual provisional reply
port are exempt from strict-vs-provisional rejection. Ordinary ports remain
rejected; receive-right checks, dispositions, regular reply semantics,
MIG dispatch and host_info implementation remain unchanged. This preserves
the real host_info operation rather than returning synthetic success.
Host predicate matrix and cross-compile pass; runtime fix remains unproven.

## BOOT0048: libpthread blocker passed; mount boot-task failure

Physical screen now reports launchd userspace panic: mount-phase-1 exited74,
failed to mount /usr/standalone/firmware, Operation not supported by device19.
This demonstrates launchd reached boot-task orchestration after0105, not
successful sustained boot. Kernel0048 has nullfs_vfsops but no bindfs_vfsops.
The A03 profile excluded portable donor0037-sweet-config-bindfs.patch.

ReVa /mount imported from the verified local root, no private Apple bytes
tracked. Function0x100006544 calls mount("bindfs", target,0x100019,source).
Failure is tolerated only for errno2/ENOENT when not required. Otherwise
0x1000068b4 calls errx with strerror(errno) and the reported diagnostic;
0x100006694 ->0x100004c60 maps errno through sysexit_np. This directly
connects missing VFS type ENODEV19 to the fatal mount boot task.
The actual mount signature has com.apple.private.bindfs-allow=true.

Enable the real bindfs implementation by staging0037, retaining entitlement
and VFS error checks. Exact config application passes; CI43727113402 builds
fromfb777a0, with an explicit linked bindfs_vfsops gate. Next BOOT0049 retains
0048 arguments/root; no filesystem reinstall or binary patch required.

## BOOT0049: keybag stage and software AKS candidate

Physical report: FATAL KEYBAG ERROR failed to load system bag; missing
options entry. Kernel has no AppleKeyStore provider. Actual iOS16.0 keybagd
was extracted read-only from pinned root and imported in ReVa /keybagd.
Connector0x10001aac8 opens AppleKeyStore type0 then selector0. Function
0x10001b7d0 calls selector14, optional input system ID and one scalar output.
Entry0x100012704 invokes this at0x100012bac and0x100012c44; a non-success
result reaches failed-to-load-system-bag fatality. Function0x100012090
queries IODeviceTree:/options for NVRAM writes; fatal handler calls it to
record keybagd and auto-boot=false, explaining the warning after failure.
Do not mistake this warning for proof that an empty options node fixes AKS.

Candidate0107 adapts the existing donor software provider, opt-in via
 a03_software_keystore=1. This is a disposable-data lab service, not SEP,
passcode protection or key wrapping. Only system bag0 is represented;
unknown selectors/wrap/unwrap Unsupported; nonzero bag IDs NotFound.
The caller ABI for open/get-system matches actual16.0. Existing root has
systembag.kb mode0600,227bytes and inherited no-effaceable-storage ADT.
No root reinstall or NVRAM storage change is required for this trial.
Exact CI-source patch application, both IOKit cross-compiles and host
request-dispatch/DER bounds/opt-in tests PASS; runtime is not yet proven.
