# Galaxy A03 SM-A035G — active bring-up

## 2026-11-17: BOOT0079 HID trial flashed after USB reconnect

A03 console re-enumerated as exact A03XNUConsole01. Single40s read-only
capture touch-reconnect-20261117.log returned live ps SpringBoard26 and
backboardd56; input status unknown command confirms current kernel lacks
0145 command (not proof of exact boot image). No gesture sent on old kernel.

Downloaded exact successful0145 CI43969089570 artifact; SHA256SUMS verified
kernel1960b8a764f690b7c6d8f7d184de76c693add08cb28a3585bdf3e42f68705e9a.
Packaged0079 from0078 exact ADT/1GiB/loader(except image_size)/stock ramdisk/
stockDT, adding only a03_hid=1. Existing0078 payload has NO RAMDisk property
or RAM-root segment; preserved actual USERDATA-root configuration rather than
inferring RAM fallback from historical notes. No0144 lab-vault change.
BOOT SHA25697f50f70b82dfe5596226f21a3b29c7e16991de5ff2b3be0c5044dfe38f17aea.

Requested normal synced CDC Download; Samsung Download enumerated. Heimdall
--boot only upload100%/successful and reboot confirmed~18:13UTC. Single
capture session52487 waitsUSB180s then480s boot0079-usb-initial.log. Runtime
HID registration/client open/gesture and physical response still pending.
0078 restore image retained. No other partition flashed.

USB returned~18:14UTC. Fresh0079 logs show exact a03_hid=1 bootargs, buttons
and touch registered; explicit input status result3 confirms both providers.
Backboardd56 progressing1to3threads in startup samples; SpringBoard25 live.
No HID client open observed yet at18:15UTC; no gesture dispatched.

## 2026-11-17: physical touch preparation; Jadard/CPT evidence recovered

User prioritizes touch after SpringBoard clock milestone. Rechecked exact
0145 CI43969089570 SHA2d4ffd7a44eab34178a13295b0ad3a337044e453: completed
SUCCESS2026-11-16T22:42:24Z. Build only; no0079 manifest found locally.
Current USB enumeration has neither A03 console nor Samsung device; old
/tmp/a03-0079 directory absent. Prior watchers are historical, not live proof.
No reset, flash, firmware operation or gesture performed this session.

Saved2026-11-13 Android dmesg has repeated Jadard JDTP successful feature
commands and lcd_jd9365t_cpt_mipi_hdp; matching Samsung HS03 source selects
CPT_Jadard_firmware.bin/JD9365T(ROM constant9383). Saved DT places Jadard on
SPI3 20150000/CS1/10MHz,10contacts720x1600; alternative controller nodes also
exist. Strong saved controller evidence, NOT fresh XNU ROM read. Stock uses
JD_ZERO_FLASH and firmware-discovered report address; display initialization
does not prove touch RAM firmware exists at XNU entry.

Added standalone unstaged shim/a03/jd9365t-report.h60byte coordinate decoder
and C11/C++17 ASan/UBSan regression: big-endian/sparse10slots/down-move-up/
inclusivebounds/state/null-length-count handling PASS. Existing actual HID
builder/actions ASan tests PASS; git diff check PASS. No bus/MMIO/provider
wiring claimed. docs/a03-touch.md records source anchors and next SPI/ROM/
RAM-firmware/HID checkpoints. Physical touch/unlock still unverified.

## 2026-11-16: 22:29 UTC clock checkpoint rechecked; local C++ command replay

Fresh BOOT0078 read-only capture boot0078-clock-check.log retains SpringBoard26,
backboardd56 and analyticsd91. SB main again resolves mach_msg/CFRunLoopRun/
GSEventRunModal/UIApplication _run/UIApplicationMain/SBSystemAppMain using
matching cache slide44b14000: application event loop, not startup wait.
Storage ready1/poisoned0; free2388/compressor5308 pages of16KiB. ScreenTime
and PosterBoard generic crash records persist; do not infer every daemon
works from SpringBoard rendering. Physical user clock report remains the
UI evidence; no unlocked home or touch verification. No reset during check.

Extended exact CI-command local compiler helper to C++ driver detection and
IOKit/libkern working directories, keeping flags/includes and reporting
unsupported Apple builtins honestly. Synthetic command-remapping regression
and Python syntax PASS. Baseline exact SweetKeyStore compilation still fails
on host Apple allocation builtins; host-only syntax stand-ins are never added
by this helper. Existing0145CI43969089570 still Build at22:28; exact gated
0079 package/deploy/status watchers retained, no duplicate CI or gesture.

## 2026-11-16: 22:26 UTC gated0079 deployment and input regression checks

0145 CI43969089570 exact2d4ffd7 still building; retained package48074.
Now scheduled deploy34846: independently gates exact CI success/checksum/
unchanged configuration, only+a03_hid=1, waits old reader, synced Download,
BOOT-only0079 then660s capture. No flash yet. Read-only/status scheduler54018
waits actual0079 worker then status/ps/SB/backboard/vm/io; NO automatic Home
or gesture. Runtime client registration/open must be inspected first.

Added tools/a03-usb-input.py exact status/home/swipeup EP0 sender, opens no
tty; help+Python syntax PASS. Added actual touch-builder ASan/UBSan regression:
720x1600 scaling/clamps, duplicate suppression, down/move/up masks,
multifinger release/state PASS. Existing action tests PASS. Documented
requirements/limitations in docs/a03-usb-input.md. Input dispatch does not
prove queue delivery or unlock; physical home screen still required.

0078 followup capture ended normally; latest SB26 event loop, analytics91,
activation467. No crash for those three across initial+followup capture;
ScreenTime repeated unsupported-vault assertion. Preserve0078 image for
restore; no root filesystem changes or non-BOOT writes in upcoming trial.

## 2026-11-16: HID client entitlement verified in matching backboardd

Read-only extraction of matching backboardd signed XML confirms boolean
com.apple.hid.system.user-access-service=true, exactly the portable HID
user client's retained access requirement. This removes an untested entitlement
assumption; service registration, connection and event delivery still require
new kernel runtime.0145 CI43969089570 retained, no duplicate or new flash.
0079 package-only48074/PID216636 retained. No input command on current0078.

## 2026-11-16: 22:20 UTC0145 CI43969089570; package-only watcher

Exact2d4ffd7a44eab34178a13295b0ad3a337044e453 full Xcode CI43969089570
in_progress, Deps22:20. Existing new package-only watcher48074 at
/tmp/a03-0079/watch-package.py gates exact successful CI/SHA/artifact checksum,
HID+creds markers, no lab-vault marker; prepares0079 with only+a03_hid=1
on same0078 ADT/1GiB/root/loader/ramdisk/DT (598bytes<608). No deployment
or reboot scheduled; preserve running physical clock checkpoint. Need full
CI success before input-provider runtime trial. Input host tests pass,
all4full C++ syntax checks with documented host-only Apple builtin stand-ins
pass, exact full C helper compile pass; original Apple builtins require CI.

0078 followup28890 readerPID214760 still captures at22:21; latest SB26
UIApplication event loop, analytics91, activation467 retain recent ps PIDs;
ScreenTime known vault failure remains. No home-screen or touch proof.

## 2026-11-16: prepared0145 explicit USB HID input for clock-screen checkpoint

Confirmed current A03 profile contains no HID service/touch/button provider;
physical swipe cannot be assumed supported. Ported portable donor0058 HID
queue/event services only (no Qualcomm hardware). Opt-in a03_hid=1 gates
registration;720x1600 normalization; no periodic Home timer. Existing USB
worker accepts exact input status/home/swipeup, with bounded paired press/
release or336ms swipe+release; USB polling remains separate. Dispatch return
is not user-interface acknowledgement. Standard HID user-client entitlement
check retained.0143 read-only credentials staged too;0144 vault NOT staged.

Local arm64 exact flags expose unsupported Apple type builtins in common
headers; NOT claiming clean unmodified full-file Clang. Host-only builtin
substitutions (never in CI/kernel) then compile all four full C++ files.
This caught real FP sensor API errors under general-register-only; unused
floating-point methods removed, keyboard/digitizer integer/fixed fields
retained with original wire layouts. C helper full exact compile PASS;
actual actions ASan/UBSan bounds/releases and patch apply/reverse/full source
equality PASS. Full Xcode CI required. No new build/flash yet at22:20UTC.

0078 reader initial capture ended normally; followup28890 captures240s,
no reboot. SB26 still UIApplication event loop. Analytics91 retains PID;
MobileActivation now467 instead134 but no detailed/generic crash observed,
so do not claim unchanged PID or indefinite survival. ScreenTime121 actual
vaultENOTSUP assertion captured~22:14; earlier model-loading sample merely
delayed reaching that known failure. Clock reported; home/input unverified.

## 2026-11-16: 22:10 UTC SpringBoard reaches application event loop

BOOT0078 SB26 latest main sample resolves GSEventRunModal → UIApplication
_run → UIApplicationMain/SBSystemAppMain. Together with user's physical
clock report this establishes running SpringBoard UI beyond startup waits,
but not an unlocked home screen or working input. Repeated ps keep analytics91,
activation134, ScreenTime121; no detailed/generic crash for those services
observed in current capture yet. ScreenTime may still reach vault later;
no claim fixed. Existing single reader206943 remains live, no reset scheduled.

## 2026-11-16: BOOT0078 physical iOS clock; analytics/activation survive

At~22:09UTC user reports "i see the iOS clock onscreen". This is the first
physical UI report beyond Apple logo, consistent with a clock/lock screen;
not yet proof of unlocked home screen or touch. Preserve this BOOT0078,
no further reboot scheduled. USB returned005/028~22:04UTC, reader206943.

Repeated fresh ps retain analyticsd91 and mobileactivation134 through22:09;
actual samples show both main threads in CF runloops, rather than earlier
fatal startup paths. No analytics/activation crash observed in current
capture so far. ACL modes/owners/ACE data unchanged inclLibrary000/-2 and
systemusers299 permits.0142 repair therefore removes the previous observed
startup failure without chmod. Continue checking survival over capture.

SB26 samples progress from dyld to BiomeStorage temporary-file XPC, then
IconServices initialization/image requests, UIKit UILabel layout and later
MobileGestalt/HMFoundation. Framebuffer swaps6–19 at720x1600 appear. Thus
samples show active startup progression, not same activation wait. ScreenTime
121 still loading CoreData model at22:08; dmd117 already vaultENOTSUP crash.
No claim ScreenTime vault issue repaired by0142. Storage ready1/poisoned0,
VM22:09 free4991pages, compressor0; goal still unlocked home screen.

Prepared optional0144 lab ScreenTime metadata helper, NOT staged/CI/enabled:
exact owner/entitlement/mobileUID/root/path gates; real com.apple.rootless
xattr+UF_DATAVAULT writes through normal authorization; preserves flags and
rejects relabel. Explicit lab NO vault enforcement, not Apple vault support.
Actual helper fault injection ASan/UBSan+full sweet_amfi.c local exact Clang
PASS. Kept off phone to preserve new UI checkpoint and isolate0142 result.

## 2026-11-16: 22:03 UTC0142 CI succeeds; BOOT0078 uploaded

CI43963988043 exact1e206d5f8695d0a393de9b0d1e45cc1c57d17759 SUCCESS.
Verified kernel90d84532d5acc3b5731bf568106e91c1ba7de95863efcecea2b659f3a3913ef9,
BOOT5e84e96c22d10a195ebcd593df9a5a21434fe62ac0e8fe36739a9c7d0894761b.
Same0077 ADT/1GiB/ramdisk/root/stockDT/loader(except image_size), adds only
 a03_compat_uuid=1. Existing deploy43872 performed synced CDC Download,
BOOT-only upload successful100%, reboot confirmed. Single readerPID206943
waitsUSB180s then660s capture boot0078-usb-initial.log. Scheduler89317 waits
worker then ACL/SB/vm/io probes. No USB return yet at22:04UTC; do not infer
service survival from missing log.0143 not included. No home screen verified.

## 2026-11-16: ScreenTime vault owner ABI and live directory state verified

BOOT0077 read-only ACL probe confirms ScreenTime directory at /private/var/
mobile/Library/Application Support/com.apple.remotemanagementd is501:501,
0755, flags0, no ACL. Guessed com.apple.dmd sibling ENOENT is not proof of
actual dmd directory. No filesystem mutation. Matching cache check helper
now pins Sandbox0x104, UF_DATAVAULT0x80, recursive flag OR, and owner check's
com.apple.rootless xattr string/instructions. Actual rootless check compares
xattr length/bytes with requested owner; success requires coherent owner
metadata as well as flags. HFS persists flags and VFS inherits them, but no
vault entitlement enforcement exists in this port. No success-only bypass.

Added docs/a03-service-crashes.md and read-only
 tools/a03-check-datavault-abi.py. Matching HFS root check, Python syntax,
git diff check and existing actual UUID/ACL sanitizer regressions PASS.
Analytics failure remains Library EACCES then NULL strlen; exact0142 CI
43963988043 still Build at22:01UTC. Existing0078 package/deploy/probe watchers
retained;0077 capture ended normally, no0078 flash yet.0143 credentials probe
prepared but unstaged. Home-screen goal remains active/unverified.

## 2026-11-16: prepared0143 read-only task credentials, not staged in0142 CI

Prepared creds PID worker command to inspect live uid/gid/supplementary groups,
actual credential UUID lookup errno/value and systemusers299 membership.
References released on all paths; group count clampedNGROUPS; no credential,
policy or filesystem mutation. This answers remaining live-group assumption
if0142 translation alone does not resolve access. NOT staged in0142 CI or
next0078; no added build/reset. Exact full sweet_amfi.c local kernel Clang,
actual helper ASan/UBSan reference/error/bounds tests, full plain-apply source
equality PASS. Current0077 reader/0142CI/0078watchers unchanged.

ScreenTime matching signed XML includes boolean com.apple.rootless.storage.
remotemanagementd; static libsystem_sandbox success path sets UF_DATAVAULT
on descendants after successful0x104. Merely returning0 would leave required
filesystem state absent; no pretend-success implementation made.

## 2026-11-16: captured ACL regression verifies authorization remains scoped

Added tools/a03-test-identity-acl.py: extracts actual XNU kauth_acl_evaluate,
uses committed0142 UUID helper and the exact0077 captured ACEs. Clang ASan/
UBSan PASS: analytics263 with supplied group299 membership gains Library
list access; mobile501 with supplied299 gains root-container write-xattr;
unrelated user without299 and unrelated rights still DEFER, explicit deny
still DENY. Default-off fails closed as observed. These supplied credential
groups are test inputs, not proof of phone supplementary groups or survival.
Also compiled actual TUNABLE plus helper/four wrappers with exact kernel
flags successfully. Full0142 CI43963988043 still building; no0078 flash.

## 2026-11-16: 21:50 UTC0142 CI and isolated BOOT0078 watchers

CI43963988043 exact1e206d5f8695d0a393de9b0d1e45cc1c57d17759 underway.
Package32985 /tmp/a03-0078/watch-package.py verifies exact successful CI,
checksums, kernel identity marker, unchanged0077 loader/ADT/1GiB/root/DT;
adds only a03_compat_uuid=1 (total588bootarg bytes<608). Deployment43872
/tmp/a03-0078/deploy.py independently verifies manifest+CI+only expected arg,
waits0077 reader then synced Download and authorized BOOT-only flash/capture.
Read-only scheduler89317 /tmp/a03-0078/schedule-probes.py waits worker and
samples ACL metadata/SB/vm/io at four stages. No0078 upload yet. Current0077
reader47410 and ACL scheduler43860 retained, no duplicate readers/builds.
Need verify actual analyticsd and MobileActivation survival plus SB progress;
ScreenTime requires separate real data-vault support. No home screen proven.

## 2026-11-16: 21:49 UTC BOOT0077 ACLs confirm local group299 grants

USB returned~21:48UTC, dedicated-worker ACL probes complete five paths.
Both activation and OSAnalytics container roots have2 permit ACEs for
abcdefabcdefabcdefabcdef0000012b (compatibility GID299 systemusers):
ACE0 flags0x161 rights0x3ffe, ACE1 flags0x1 rights0x624. OSAnalytics Library
(-2:-2/mode000) has1 inherited permit ACE for SAME GID299, flags0x71,
rights0x3ffe. Parent Data/System and Shared/SystemGroup have no ACL.
Thus the mode000 Library is intentional ACL-backed access, not evidence
it should be world-readable or chowned. No metadata mutation performed.

Matching UUIDs confirm0142 translation candidate is relevant: kernel external
resolver otherwise cannot decode those local account UUIDs, failing closed.
Staged0142 in next build profile, default disabled; next BOOT0078 should add
only a03_compat_uuid=1 after exact successful full CI. Group membership/ACL
rights remain the authorization mechanism; this repairs identity format only.
Need verify runtime analytics/activation survival and actual SB progress.
ScreenTime data-vault API is a separate unresolved missing implementation.

## 2026-11-16: 21:47 UTC BOOT0077 ACL diagnostics deployed

Synced CDC Download succeeded. Heimdall BOOT-only upload100%/successful and
reboot confirmed. Verified0141 kernel/unchanged configuration above.
Existing47410 waitsUSB180s then660s capture; ACL scheduler43860 retained.
Actual ACL records pending;0142 not included. No protected partition/root
mutation, no rendered home screen established.

## 2026-11-16: 21:46 UTC0141 CI succeeds and BOOT0077 packaged

CI43961834933 exactbd84c3ba60d72de9cd3742a5b8221c5827c533c3 SUCCESS.
BOOT SHA2562db3ebac42ac32bc2c0d941368dc921ae432218c7449aab76505b14757118826;
kernel SHA256d6c024750fff02fab0060e100d0ad07a5cfa4198447e152b8604639fd341d015.
Package verified exact checksum/MachO/ACL marker and unchanged0076 config:
ADT/1GiB/args/loader(except image_size)/ramdisk/stockDT.0142 NOT included.
Existing47410 began synced Download after0076 capture end; upload pending
at21:46:53UTC. ACL scheduler43860 retained. Need actual ACEs; no home screen.

## 2026-11-16: prepared0142 local identity UUID candidate, not staged/enabled

Prepared0142 source candidate for explicit a03_compat_uuid=1 (default0),
SWEET-only local UID/GID compatibility UUID conversion matching both staged
Libinfo and existing CONFIG_EXT_RESOLVER=0 kernel algorithm. Four conversion
wrappers handle only recognized local UUID prefixes and UID/GID encoding;
unknown UUIDs retain resolver behavior, wrong-type local UUID returnsENOENT.
No membership grants, hardcoded account allowlist, ACL skips, Apple patches,
disk writes, or activation fabrication. Not added to build profile or current
0141 CI; enable only after actual ACLs confirm relevant UUIDs.

Actual helper Clang ASan/UBSan PASS default/exact opt-in, UID501/GID299 known
vectors, type mismatch, unknown UUID and0/UINT32_MAX round trips. Full source
plain git apply reverse/reapply equality PASS. Full kern_credential.c local
compile is NOT PASS: baseline and candidate both produce identical73 normalized
errors from Apple's unsupported __builtin_xnu_type_* allocation builtins;
no new candidate diagnostics. Extracted actual helper+four changed wrappers
compile successfully with exact kernel CI flags/includes and arm64 target
(outside unrelated allocation-builtin code). Full Xcode CI still required
before deployment.
BOOT0076 capture ended normally~21:45UTC. Existing0141 CI43961834933 and0077
package53238/deploy47410/ACL scheduler43860 retained. No0077 flash yet.

## 2026-11-16: matching Libinfo uses compatibility UUIDs, membership APIs limited

Read-only matching cache analysis identifies exported mbr_uid_to_uuid /
mbr_gid_to_uuid. Their backend constructs UID prefixffffeeeeddddccccbbbbaaaa
and GID prefixabcdefabcdefabcdefabcdef, appending big-endian32-bit ID. This
matches XNU's existing CONFIG_EXT_RESOLVER=0 compatibility branch exactly.
The supplied iOS Libinfo mbr_check_membership variants directly return5;
no Apple binary modified. Enabled kernel external GUID lookup is therefore
a strong mismatch candidate; actual0141 ACEs still needed to select repair.
Keep source-level group semantics/credentials, not a blanket allow policy.

## 2026-11-16: 21:39 UTC BOOT0076 again reaches activation wait

Fresh SB26 samples after MC checkIn now resolve MadGate getActivationState: /
MAEGetActivationStateWithError using captured slide13614000. Tccd37 and
profiled100 remain in ps. Activation backup-xattr EACCES13 continues and
ScreenTime exact vault45 exception repeats. Root storage remains usable;
these are runtime service blockers, not evidence of still doing generic boot.
0141 ACL CI43961834933 remains in progress; package/deploy/probe watchers
unchanged, no0077 upload.0076 read-only stat repeats Library -2:-2/mode000.

Source investigation: CONFIG_EXT_RESOLVER is actually enabled. Its GUID
lookups call an external resolver on cache miss; staged launchd has no
opendirectoryd/memberd job. ACL evaluator fails closed when it cannot resolve
caller/ACE membership. MCM explicitly constructs a systemusers ACE. This is
an ACL-resolution hypothesis pending actual ACL records; it is not proven
by mode000 alone. Existing no-resolver kernel branch provides compatibility
UID/GID UUID translation, but no configuration or permission change made.

## 2026-11-16: BOOT0076 live ownership/modes;0141 ACL CI queued

USB returned~21:34UTC, cache slide13614000, SpringBoard26 this boot. First
stat probes complete through dedicated worker, no second console reader.
Actual activation container51E6AD4E-3CED-47F7-B6EC-51E7034B24DA uid0/gid0,
mode040755 flags0 fileid308200. OSAnalytics SystemGroup15C54419-7736-4C62-
B119-1C994A4F8444 root uid0/gid0 mode040755 flags0 fileid308235; its Library
uid/gid4294967294(-2), mode040000(no POSIX permissions), flags0 fileid308237.
Repeated probes retain same values. Both parent container classes uid0/gid0
0755; var/mobile/Library uid/gid501 mode0711. Mountflags1480d000 does NOT
contain MNT_NOUSERXATTR01000000. Immutable flags absent on measured targets.

This establishes actual access metadata, not that chmod is the right repair:
MCM _CreateSystemUserACEInACL uses literal systemusers; staged group299
includes mobile and _analyticsd. Mode000 may intentionally rely on ACLs.
Need actual ACEs and kernel GUID/group resolution rather than broad bypass.
Analyticsd92/152/173 again stat/open EACCES13 then NULL strlen. ScreenTime
actual data-vault ENOTSUP assertion repeats. No permission changes performed.

Fixed private scheduler issue: CoreAnalytics full path is101bytes, exceeds
0140's100byte guard. First scheduler logged AssertionError after the three
useful probes. Removed that path (parent Library is inspectable), restarted
as86888; subsequent stages continue, no kernel/console failure implicated.
Fresh0076 SB26~21:37 main MCProfileConnection checkIn; container63 sample
completes with worker checking item existence. Not proof of deadlock/home.

Started0141 full CI43961834933 exactbd84c3ba60d72de9cd3742a5b8221c5827c533c3
at21:36UTC after local exact Clang/sanitizers/plain-apply verification.
Package-only53238 /tmp/a03-0077/watch-package.py retained; deployment47410
/tmp/a03-0077/deploy.py waits exact success+verified same0076 config+reader
end, then synced Download and authorized BOOT-only0077,660s capture.
ACL scheduler43860 waits worker and probes five failing/parent paths plusSB.
No0077 flash yet. Current0076 reader84806 retained; no protected/root writes.

## 2026-11-16: 21:33 UTC BOOT0076 read-only filesystem diagnostics deployed

Prior status reader ended; synced CDC Download succeeded. Heimdall BOOT-only
upload reached100%, reported successful and reboot. Verified image/build
hashes and same1GiB/ADT/arguments/root/loader configuration above. Deployment
84806 now waitsUSB180s then660s initial capture; scheduler51114 retained for
six actual failing/parent path stat probes. Runtime USB/metadata pending at
this checkpoint. No root/protected partition writes; home screen unproven.

## 2026-11-16: 21:32 UTC0140 CI succeeds and BOOT0076 package verified

CI43959202597 exact65cc5807244657e6ff1014894734a7106b2eee54 SUCCESS.
Kernel SHA256bb342c79786b5f605c54544a4350021e9a2138177530a7818b80773e156bc78a;
BOOT0076 SHA2565b24a68639cc0df952e3b8cc51c6aed5069d9a396a22b4a17f831b2b4b9ff353.
Exact checksum/MachO/stat marker and unchanged0075 ADT/1GiB/args/loader
(except image_size)/ramdisk/stockDT verified. No0141 in this build.
Deployment84806 waits final60s0075 status reader82251 then authorized
synced CDC Download/BOOT-only flash and660s capture. Stat scheduler51114
retained. No0076 upload yet at this checkpoint.
Fresh0075 sample25 retains same MadGate synchronous activation wait;
VM free2616/compressor2474pages, storage ready1 poisoned0. No home screen.

## 2026-11-16: prepared0141 ACL inspection; fresh SB activation wait

21:26UTC0075 ps/sample25 completes with12threads. Matching cache symbolication
confirms main synchronous XPC through MadGate getActivationState:, exported
MAEGetActivationStateWithError. Thus this boot has now moved past the earlier
MC checkIn wait and reaches the MobileActivation permission blocker too.
Storage ready1/poisoned0; no home-screen evidence. Initial660s capture ended
normally, releasing tty;0076 watcher remains gated on existing0140 CI.

Offline matching passwd/group identify analyticsd uid/gid263, mobile501;
_analyticsusers250 and systemusers299 include both. These are staged account
facts, not live supplementary-group evidence. MCM contains explicit ACL and
ownership setup code, so mode alone may not explain EACCES. No guessed chmod.

Prepared0141 adds optional read-only acl /private/var/PATH alongside stat,
with existing bounded/path/no-follow-final/worker gates. Requests va_acl,
prints count/flags and at most16 ACE GUID/rights/flags, frees returned ACL on
success/error and releases vnode. Invalid counts>128 never indexed. Regular
stat does not request ACL. No access-policy or disk mutation. This patch is
NOT in ongoing0140 CI43959202597/BOOT0076; it is staged for next build only.
Actual helper ASan/UBSan tests PASS for none/entries/cap/invalid/error cleanup/
unsupported/ordinary stat. Full sweet_amfi.c exact CI-command local Clang PASS;
plain git apply reverse/reapply full source equality PASS. Rechecked0140,
startup diagnostics and crash-annotation sanitizer suites PASS. No new CI
started for0141 yet; use0076 stat evidence first. Private logs stay ignored.

## 2026-11-16: BOOT0075 ScreenTime exact assertion confirmed;0076 deployment queued

The initial capture now includes ScreenTimeAgent122 and268 SIGABRT with
actual NSInternalInconsistencyException: "Failed to enable data vault:
Operation not supported (45)". This confirms the previously static candidate:
Sandbox0x104 fd3 ownerremotemanagementd fails before the terminating assertion.
Dmd independently has the same missing API. The earlier rootless_log socket
wait was temporary, not evidence that ScreenTime remained alive indefinitely.

Analyticsd91/146/167 repeats stat64 EACCES13 on CoreAnalytics then open EACCES13
on Library before its NULL strlen crash. This is a separate filesystem access
failure. Actual directory ownership/mode/flags remain pending0140; no broad
chmod, errno suppression or data-vault pretend-success implemented.

Corrected handoff:0076 deployment IS now scheduled via84806/PID182276,
/tmp/a03-0076/deploy.py. It checks exact successful CI43959202597 SHA65cc580,
verified unchanged-config package, waits prior reader completion, then synced
CDC Download and authorized BOOT-only flash, followed by660s capture.
At21:25UTC CI remains in Build; no0076 flash yet. Package57048 retained.
Started read-only stat scheduler51114 /tmp/a03-0076/schedule-probes.py,1800s
worker wait then30/180/300/540s stages inspecting six failing/parent paths and
SB sample/vm/io through EP0. Existing0075 single reader remains untouched.
No USERDATA/protected partition mutation; home-screen goal remains unverified.

## 2026-11-16: BOOT0075 confirms analytics+activation EACCES, ScreenTime vault ENOTSUP

USB reenumerated005/022, ordinary access/capture resumed21:18UTC. New cache
slide16a60000, SB25 (not26; one initial manual sample26 was runningboardd,
subsequent ps resolves25). Existing capture/deploy64839 remains single reader.

Analyticsd91 exact same NULL strlen crash, now preceded by stat64(338) EACCES13
for /private/var/containers/Shared/SystemGroup/15C54419-7736-4C62-B119-1C994A4F8444/
Library/CoreAnalytics, then open(5) EACCES13 on its Library parent. Container
root lookup therefore produced an actual path; directory access/setup fails.
Do not label container lookup NULL as the proven root cause. Need actual uid/
gid/mode/flags on parent and path; no permission bypass implemented.

Mobileactivation129/136 setxattr236 EACCES13 exactly at
/private/var/containers/Data/System/51E6AD4E-3CED-47F7-B6EC-51E7034B24DA,
attr com.apple.metadata:com_apple_backup_excludeItem,22byte MobileBackup value.
Chunked annotation works: Cocoa513 contains nested NSPOSIXErrorDomain13,
full path, SourceLine248/main. First container itself is failing; not inferred
from Cocoa number anymore. Need ownership/permissions rather than guessed fix.

ScreenTimeAgent122 creates/opens /var/mobile/Library/Application Support/
com.apple.remotemanagementd, mac_syscall Sandbox0x104 returns45 ENOTSUP,
fd3, owner remotemanagementd confirmed. Sample122 shows standalone+21dec
(call rootless_convert_to_datavault) ->rootless_log, blocked connecting os_log
Unix socket(_unp_connect mutex), so final assertion still not emitted at sample.
API-level failure is live-confirmed; assertion candidate supported, not yet
captured as actual terminating annotation. Dmd same0x104 ENOTSUP ownerdmd.
Tccd37 profile ops22/1 succeed. SB25 sample~21:21 main MCProfileConnection
checkIn wait, later activation wait not yet reestablished in this boot.

Started0140 CI43959202597 exact65cc5807244657e6ff1014894734a7106b2eee54
for tested read-only filesystem stat probe, to inspect actual permission state.
It is in progress; package-only57048 /tmp/a03-0076/watch-package.py will verify
success and package same0075 config. No0076 deployment/reset scheduled yet.
Read-only EP0 scheduler19502 retains60/180/300/540s probes for0075. No root/
protected-partition changes. Actual home-screen goal still unverified.

## 2026-11-16: 21:17 UTC BOOT0075 diagnostic deployed after successful0139 CI

CI43955738619 exact2f78691552a541b5c9ee56c06ee6a4c08e308096 SUCCESS.
Package checksum/Mach-O/diagnostic markers and unchanged0074 ADT/1GiB/args/
loader(except image_size)/ramdisk/stockDT verified. Kernel SHA256
26b09528fc564a84b5a97b721b48d0db8a9cb0a72efe29fc98da8b5fb7b02fc8;
BOOT0075 SHA256890b3491f6ea7b1fa229e75568d97376dc83279ec70ebad58103d05983460a31.
Synced CDC Download succeeded, then Heimdall BOOT-only upload100%/successful,
reboot confirmed21:17UTC. Deployment64839/PID169581 now waitsUSB180s then
captures660s boot0075-usb-initial.log. Do not open another tty reader.
0138/0139 included; prepared0140 read-only stat NOT in this kernel. Need
runtime ScreenTime annotation, analytics error path, activation backup xattr
actual path/errno and SB progress. No root/protected partition changes.
Home screen remains unproven.

## 2026-11-16: 21:11 UTC container query sample and prepared0140 read-only stat

Fresh0074 sample63 completes: containermanager63 alive3threads, main event
loop, worker handling MCMContainerClassCache cacheEntryForIdentifier via
MCMContainerFactory/MCMCommandQuery. Sample alone does not establish service
deadlock. VM compressor2911pages, free2922pages; storage ready1,poisoned0.
Analytics/ScreenTime/activation continue crash loops. No reboot made for probes.

Prepared0140 (NOT included current0139 CI43955738619) adds dedicated-worker
stat /private/var/PATH <=100bytes, rejects dot traversal, performs vnode_lookup
no-follow-final, vnode_getattr, vnode_put. Prints actual uid/gid/mode/flags/
fileid/mountflags only if supported; retains errors and no writes/xattr values.
This is diagnostic path-prefix validation, not a security boundary against
intermediate symlinks. Actual helper ASan/UBSan PASS incl lookup/getattr errors
and vnode cleanup, invalid paths, unsupported fields; full sweet_amfi.c exact
CI-command local Clang PASS after replacing unavailable kernel strstr with
explicit dot-component parsing (first follow-up compile caught it). Plain
reverse/reapply exact source equality PASS. Prior0135 transport/task tests and0136 profile
tests PASS. Source patch prepared separately for next evidence-driven build;
current0139 compilation/deployment remains unchanged, no duplicate CI.

## 2026-11-16: 21:08 UTC0139 CI compiling; same-config0075 deployment gated

CI43955738619 exact2f78691552a541b5c9ee56c06ee6a4c08e308096 observed Build
in progress. Package watcher62827/PID167795 remains live and separately
prepares0075 only after exact successful CI and checksum verification.
Deployment64839/PID169581 now waits manifest+same exact successful CI,
validates boot checksum/size and unchanged0074 ADT/1GiB/args/loader/ramdisk/DT,
waits existing tty capture end, then synced CDC Download and authorized
BOOT-only upload0075, followed by660s capture. No0075 reset/flash yet.
Prior0074 initial reader ended normally; short status67339 captures60s
without reader competition. Fresh ps shows SB26,tccd37,containermanager63,
profiled103 alive; detailed crash loops remain. Home menu unproven.

Exact cache CoreServicesInternal pathURLPropertyProviderSetValues at
180fb3f0c..3f30 sets com.apple.metadata:com_apple_backup_excludeItem to
22-byte com.apple.MobileBackup using setxattr, options1(no-follow), then
removes legacy com.apple.MobileBackup attribute. Stub186e17174 resolves
libsystem_kernel setxattr1bf131c6c. Thus next activation trace should identify
this xattr and actual path/errno rather than assume setattrlist failure.
Four nonnil startup paths correspond com.apple.mobileactivationd,
systemgroup.com.apple.regulatory_images,systemgroup.com.apple.pisco.suinfo,
systemgroup.com.apple.mobileactivationd; missing paths have a separate fatal
branch. Launchd runs MA/ScreenTime as mobile and analyticsd as _analyticsd.
This static evidence does not prove current vnode ownership/errno or analytics
container success. Private decoded artifacts/tmp/a03-0075, no Apple changes.

## 2026-11-16: BOOT0074 activation backup-exclusion failure; tested0139 evidence

Live0074 detailed crashes mobileactivation138/147 both SIGTRAP at standalone
0x1001c6804 (explicit brk), caller0x10004bd00. Annotation: Failed to set
backup exclusion on container path; underlying NSCocoaErrorDomain513
permission failure. Exact binary main loops four container paths, reads
NSURLIsExcludedFromBackupKey, then setResourceValue(true); false returns to
fatal helper. Actual failing path/POSIX errno still unknown: current256-byte
annotation is itself truncated by console record length before its tail.

Read-only EP0 ps/sample26 at21:00UTC used existing capture, no second tty
reader/reset. SB26 still12threads, main MadGate getActivationState sync XPC;
ScreenTimeAgent362/371 and analyticsd359 still crash. No home-screen evidence.
ScreenTime data-vault candidate and analytics NULL path diagnosis above remain
accurately scoped; no new runtime proof of their underlying filesystem error.

Prepared0139 includes existing0138 in next staged profile and adds independent
192-report startup slots for mobileactivation/ScreenTimeAgent/dmd, failed
setxattr/fsetxattr attr names, setattrlist/fsetattrlist/at bitmaps, and Sandbox
0x104 fd/owner ABI. All reads bounded with non-NULL copyinstr length pointers;
no errno, policy, activation state, Apple binary or filesystem behavior edits.
Crash annotations emit160-byte chunks up to1024 bytes to retain nested errors
without console record truncation; existing two-reports-per-name gate retained.

Actual-source helper tests ASan/UBSan PASS, including invalid pointer handling,
independent caps, fd-vs-path selection, long NSError through256-byte record cap.
Fixed pre-existing test-harness pointer arithmetic UB exposed by sanitizer.
Exact CI-command full-file local Clang PASS for systemcalls.c and exception.c.
Plain git apply reverse/reapply exact source hash equality PASS. Full CI still
required; kern_exit selector0138 prior helper PASS, Apple builtin limitation
for its local full compile remains. No0139 flash yet;0074 remains running.

## 2026-11-16: 20:52 UTC BOOT0074 diagnostic deployed after full CI success

CI43951369485 exacta4d660cbf786f5a5d66e4036f94a124b04518d97 completed
successfully. Existing watcher14214/PID154025 verified artifact/checksum,
identical0073 ADT/1GiB/args/loader/stockDT. BOOT SHA256
95d093c1950d9e016eb5d3913aca057f2219e24805e5e2309cba41874884814e;
kernel SHA25684ff3512223a5b78da530aba538d08d6900f46423f0cd875afc758d795608edb.
Synced CDC Download succeeded; Heimdall BOOT-only upload successful and
reboot confirmed20:52UTC. No protected-partition/root changes. Same watcher
now waiting USB then captures660s boot0074-usb-initial.log. Need detailed
mobileactivation crash;0138 ScreenTime/analytics diagnostics not in this boot.
Actual home screen remains unverified.

## 2026-11-16: data-vault API decoded while retaining running0137 CI

Matching cache export libsystem_sandbox rootless_convert_to_datavault at
1cdc4ec74 opens the directory, builds16byte {sign-extended fd, owner string}
and invokes mac_syscall("Sandbox",0x104,&args). Current lab Sandbox handler
supports op2 and scoped tccd ops1/22;0x104 remains ENOTSUP. Thus dmd's live
"Failed to enable data vault: Operation not supported" has an API-level
explanation; ScreenTime exact binary calls this same API with owner
remotemanagementd, but its live crash still requires0138 report. Do not
blanket-success0x104 or imply real data-vault enforcement exists.

Offline rebuilt root SystemGroup/DataSystem container directories are empty;
this is pre-runtime image state, NOT proof about actual USERDATA after boots.
No root modifications made. Existing CI43951369485 still Build observed;
watcher154025 retained, no extra build or phone reset. Private decoded API
under/tmp/a03-0074/rootless-exports.txt. Actual home screen unverified.

## 2026-11-16: analyticsd NULL tasking path decoded; ScreenTime candidate

User requests investigation of ScreenTimeAgent and analyticsd while0137 CI
runs. Exact0073 analyticsd91/167 both SIGSEGV, FAR0, PC1e107ede4 resolves
__platform_strlen+4. Matching extracted binary LR offsets57ac/49d28 decode
C++ string construction from [OSASystemConfiguration.sharedInstance
pathCATasking].fileSystemRepresentation without NULL check. Caller uses
file:tasking. Chained import523 resolves class OSASystemConfiguration;
selector refs resolve sharedInstance/pathCATasking/fileSystemRepresentation.
Matching OSAnalytics cache pathCATasking calls pathContainerRoot then
ensureUsablePath with component /Library/CoreAnalytics. Container root calls
container_system_group_path_for_identifier(NULL,
"systemgroup.com.apple.osanalytics",&error). Nil return can originate container
lookup or directory setup; exact runtime errno is not yet established. No
claim this is CPU instruction incompatibility or same cause as ScreenTime.

ScreenTimeAgent generic crash repeats, detailed selector omitted it. Exact
binary includes data-vault setup: rootless_convert_to_datavault(path,
"remotemanagementd") at100021de8; nonzero branches to assertion reporting
"Failed to enable data vault: %@ (%d)" at100021ea8. This is a concrete static
candidate consistent with separate dmd observed data-vault failures, NOT a
proven ScreenTimeAgent live crash reason. Need actual crash annotations.

Prepared0138 adds ScreenTimeAgent independent2-report crash slot and
analyticsd independent192-report existing startup syscall diagnostics. No
behavior/errno/activation changes. Actual cumulative helpers ASan/UBSan PASS;
full systemcalls.c exact CI-command Clang PASS; patch reverse-check PASS.
Kern_exit.c full local compile retains known Apple builtin limitation.
0138 not in currently running0137 CI43951369485, watcher14214/PID154025
retained; no extra CI/reset/flash triggered. Private extracted/disassembly
artifacts under/tmp/a03-0074. Home-screen goal remains unproven.

## 2026-11-16: MobileActivation diagnostic CI queued with gated BOOT0074

Pusheda4d660cbf786f5a5d66e4036f94a124b04518d97; CI43951369485 observed
in progress. Watch/deploy14214 /tmp/a03-0074/watch-deploy.py waits exact
successful build, packages identical0073 configuration with new diagnostic
kernel, waits existing reader ends, uses synced CDC Download and BOOT-only
flash0074, then660s capture. No new flash yet. Asked physical screen state.
Existing0073 USB/runtime remains live; no activation state/binary edits.

## 2026-11-16: BOOT0073 fixes tccd startup; current SpringBoard activation wait

CI43946625323 exactc9a358b succeeded. Existing watcher verified kernel/image,
BOOT-only upload/reboot21:27:09local. Image SHA256
be94b6edff5af25fb5563151b5f31d7cb9ac3d79a1d6d314b08dc157ce481f21;
kernel ead441439b3b5da4881aa859b1777ee7d11b9e6ca0b8dbd794fe757542c4e32a.
Live0073 confirms tccd37 named profile op22 and op1 accepted; process stays
alive7threads and no reported tccd crash. New cache slide13424000. Earlier
SB25 MCProfileConnection checkIn stack advanced; latest main13threads is now
MobileActivation MadGate getActivationState -> getActivationState ->
MAEGetActivationStateWithError, synchronous XPC. Do not call old migration/
TCC wait current blocker. Profiled108 now7threads and no old TCC worker wait;
other waits include lockdown_set_value and CFPreferences flushManagedSources.
Mobileactivation generic corpse reports repeatedly crash PIDs150..295.
Existing detailed crash selector omits this truncated16char process name.
VM compressor0; storage ready1 poisoned0. No physical home-screen evidence.

Prepared0137 selects mobileactivation for existing bounded2 crash reports;
no service behavior or activation-state changes. Actual-source helper test
with cumulative0128/0137 ASan/UBSan PASS. Full-file replay Clang attempted
but unavailable Apple-specific __builtin_xnu_type_summary/signature/compatible
in unchanged allocator macros; do not claim full local compile PASS.
Full CI required. Existing0073 capture remains single reader, no reset yet.

## 2026-11-16: corrected copyinstr fix building for BOOT0073

Pushedc9a358b7c068a5fca9a628e6ae2a03ecf879f7c4; CI43946625323 in
progress, Deps observed. Plain reverse/reapply0136 byte-for-byte source
comparison PASS after full-file Clang validation. Watch/deploy88152/PID90578
/tmp/a03-0073/watch-deploy.py waits exact successful CI; packages unchanged
0072 ADT/1GiB/args/loader/stockDT, verifies artifact+image, requires existing
Download+no reader, flashes BOOT only then captures660s. No0073 flash yet.
No live-probe scheduler added; read passive startup evidence first. Actual
profile ops22/1, tccd survival, SB migration and home screen remain gates.

## 2026-11-16: user reports BOOT0072 kernel panic; copyinstr caller fixed

Physical report: panic kernel data abort PC0xfffffe000746e938. Verified exact
0072 kernel against manifest SHAa7085e03...2090; llvm-nm/llvm-objdump resolve
copyinstr+0x18, instruction str xzr,[x3]. Matching arm64/copyio.c immediately
writes *lencopied=0 unconditionally. New0136 helper incorrectly supplied NULL
for lencopied, a concrete defect consistent with reported panic. Full panic
LR/FAR/registers unavailable, so caller attribution is inferred from defect
and address rather than a captured backtrace. No prior USB sample established
this panic; user's physical evidence changes diagnosis from unexplained stall.

Fixed helper to pass address of local size_t copied. Original host test had
incorrectly asserted NULL output; replaced with non-NULL assertion plus actual
length-output stores. Corrected regression fails old helper SIGABRT and passes
fixed helper ASan/UBSan; prior scalar Sandbox test PASS. Full sweet_amfi.c
exact CI-command arm64 Clang PASS. Updated patch reverse-apply check PASS.
Phone now Samsung Download USB005/017, heimdall detect PASS. No new flash yet.
Next full CI and corrected BOOT0073 with same0072 payload settings.

## 2026-11-16: 20:05 UTC passive retry wait expires without device return

Existing capture51868/PID88668 was verified live while waiting, then exited1
with no console after180s. No retry log was created; neither XNU USB nor
Samsung Download device present. No physical screen/restart report received.
No replacement capture or build started; no live probe/capture remains.
Runtime continuation requires physical recovery or actual screen observation.
0136 runtime and actual home screen remain unverified.

## 2026-11-16: BOOT0072 first trial stops responding before profile test

USB005/012 and ttyACM0 re-enumerated root:uucp0660+ with installed rule;
EP0 ps/vm/io worked without manual ACL, confirming persistent permissions.
Initial0072 capture shows exact opt-in bootarg and SpringBoard26/cache slide
4d0a4000. At60s worker sample main is still dyld forEachDOFSection/prepare;
kernel wait emmc_strategy mutex during executable page-in. tccd37 has one
thread still in dyld preparation, not reached sandbox_init. No named-profile
op22/op1 marker, no tccd sandbox crash and no home-menu proof yet.

Last log write19:56:34UTC,446417bytes. Both60s samples ended normally and
subsequent services/logs continued, then output ceased. At180/300s scheduler
failed identification; direct libusb serial request returns-7(timeout), not
ACL denial. Host USB remains active with no disconnect before recovery;
this does NOT establish whether kernel, USB worker or phone power stalled.
No A03 SAMPLE begin from built-in180s sampler reached captured output.
Read-only probe code inspected; no demonstrated deadlock/root cause found.

At20:00:27UTC attempted exact-serial USBDEVFS_RESET (USB interface only,
no phone reset/storage writes). Descriptor reads repeatedly timed out-110,
address failed-62; reset returned ENODEV and host attempts re-enumeration.
Capture ended normally on USB disconnect. Requested physical screen state
and conditional Side+VolDown restart if stalled, leave any home/setup screen
running. Awaiting user. Stopped obsolete probe scheduler83348 to avoid new
commands on restart; passive retry capture session51868 waits180s then600s,
boot0072-usb-retry-passive.log. Built-in sampler remains in flashed image.
Need retry evidence before claiming0136 succeeds/fails or making new fix.

## 2026-11-16: 19:53 UTC BOOT0072 full CI and BOOT upload pass

CI43940554508 exact1f0d037501c381d61debcb0a84a19d1bb4f8fcaa completed
successfully. Existing package watcher verified artifact SHA256SUMS,
plain-arm64 header, linked0136 marker, identical0071 ADT/1GiB memory,
loader except image_size and stock ramdisk/DT. New boot SHA256
84c84ae35cafa8ba1467947ccf01d7c6bf8d7c0fad906fd4f323e3c8f6616d0a;
kernel SHA256a7085e03d3acf022fa7ae524af1a3e2fd6e68fc0d86ddcab1d7889848a362090.
Only new command-line argument a03_sandbox_profiles=1. Gated deployment
used synced CDC Download then heimdall flash --boot only; log confirms
boot upload successful and Rebooting device. No protected-partition writes.
Session46231 now captures0072 for660s after USB enumeration (wait180s).
Probe scheduler83348 awaits actual worker then60/180/300/540s snapshots.
Runtime tccd survival, migration progress and physical home menu unproven.

## 2026-11-16: 19:44 UTC fresh live status confirms same migration/TCC wait

Read-only0071 EP0 probes19..23 captured privately in
shim/a03/out/boot0071-usb-status1944.log. SpringBoard25 now8threads but main
CPU remains exactly user0.345264/system13.641375/runnable88.511870 and
same full stack as19:30UTC. Exact cache slide24614000 symbolication confirms
MCProfileConnection waitForMigrationIncludingPostRestoreMigration ->
activationRecordIndicatesCloudConfigurationIsAvailableAndKeyExists ->
shouldShowCloudConfigurationUI, synchronous XPC wait. Profiled109 worker
still _tccd_send_message -> TCCAccessSetOverride; no tccd in fresh process
list. Initial0071 log records tccd abort namespace25/profile not found.
System activity continues, but main SpringBoard startup has not advanced
for at least14minutes. Apple logo is physical observation, not home menu.
Storage ready1/poisoned0; VM compressor2347pages (~36.7MiB), no swap.
CI43940554508 exact0136 still in progress. Existing package/deploy/probe
watchers retained, no0072 flash yet. Capture ended; no tty reader retained.

## 2026-11-16: 0136 scoped tccd named-profile candidate locally validated

Current0071 runtime chain SB -> profiled -> TCC motivated decoded API repair.
Matching libsandbox query22 copies one pointer; successful query constructs
named profile {name,0,0}, sandbox_apply issues op1 with those3words. Added
0136 scoped to exact process name tccd and profile com.apple.tccd, existing
a03_sandbox_disabled=1 policy plus new a03_sandbox_profiles=1(default0).
Both ops copy in bounded arguments; names use64byte copyinstr; pointer/fault/
long-name errors propagate. Binary profile op0, non-null message/length,
other names/callers/operations remain unsupported. This explicitly lab-only
profile implements NO sandbox enforcement; not production privacy isolation.
16 bounded reports. No Apple binaries/TCC replies/activation state modified.

Actual helper ASan/UBSan tests opt-in1-only, faults/null/long name, exact
8/24byte ABI, caller/name restriction, bytecode rejection,16log cap PASS.
Existing0121 op2 tests PASS. Exact per-file CI-command Clang compile of full
sweet_amfi.c PASS. Plain git apply/reverse/reapply exact source equality PASS.
Full CI/link/runtime still required; no new BOOT/reset/root writes yet.

## 2026-11-16: 19:30 UTC SpringBoard passes LS; now profile migration/TCC wait

User physically reports Apple logo with continuing output (not home screen).
Fresh live0071 probes8..15 show same SpringBoard25 now7threads and main CPU
advanced to user0.345264/system13.641375/runnable88.511870s. It has LEFT the
previous ControlCenter/LSContextInitCommon wait. Exact slide24614000 resolves
main stack to MCProfileConnection waitForMigrationIncludingPostRestoreMigration:
waitUntilCompleted:completion: -> activationRecordIndicatesCloudConfiguration
IsAvailableAndKeyExists: -> shouldShowCloudConfigurationUI. Main waits sync
NSXPC reply; repeated8/14 stack/CPU unchanged over~30s. Do not continue to
report LS seeding as current SpringBoard blocker. lsd100 is now5threads,
old seeding worker absent; separate MobileActivation request wait remains.
MobileActivation old133 gone; current multiple PIDs crash/respawn in log.

Profiled109 sampled3threads. Worker sync XPC stack resolves TCC framework
_tccd_send_message -> TCCAccessSetOverride path; main in runloop. This gives
current chain SpringBoard managed-configuration migration -> profiled -> TCC
request, concurrent with hardware-observed tccd profile-not-found crash loop
previously decoded to unsupported Sandbox named-profile query22. It is now
a concrete dependency to investigate, not proof that fixing tccd alone yields
home screen. Fresh VM compressor1220pages/~19MiB, storage ready1 poisoned0.
Current65s capture75768 boot0071-usb-current.log. No new phone writes/reset.
Need implement correctly bounded lab-mode named-profile API semantics after
checking exact profile install ABI; do not blanket-success unknown operations.

## 2026-11-16: EP0 access restored; persistent host rule prepared

User applied USB005/010 ACL. Actual0071 ps/vm/io/sample25/sample100/
sample129 responses confirm resumed live access. VM wired8503/free3119/
active26190/inactive27710 pages, compressor0/compressions0/decompressions0;
page-size16384. Expanded RAM is used without earlier compressor churn.
SpringBoard main remains at same LS initialization wait; lsd now PID100,
mobileactivation133, iconservicesagen129. Current lsd sample has9threads,
including a semaphore wait requiring symbolication; keep following this
rather than assume the old0070 service wait is identical. Live120s capture
41818 boot0071-usb-live-probes.log. No home-menu success or phone writes.

Added tools/udev/60-a03-xnu-console.rules for exact VID1d6b/PID0104/serial
A03XNUConsole01, usb_device and tty rules, groupuucp/mode0660/uaccess.
Host user already belongs to uucp; rule filename precedes seat-late ACL.
udevadm262 verify PASS. Rule prepared in repository, NOT installed into/etc;
installation/reload/targeted trigger commands in docs/a03-usb-console.md.
No broad gadget/Download permissions added. Prior goal access blocker removed;
full homescreen objective remains unfinished.

## 2026-11-16: all0071 timed passes confirm LS wait; tccd cause decoded

Built-in samples180/300/420/540s complete across0071 initial/continuation
logs. SpringBoard main and LS synchronous-XPC worker full user stacks and
CPU counters match exactly across all4passes. FrontBoard process-registration
workers also block behind initialization; this does not establish an
independent FrontBoard failure. No home menu observed. Live probe EP0 still
fails access until requested ACL on USB005/010 is applied; ordinary CDC
capture30397 remains live, so preserve current boot for lsd sampling.

Read-only disassembly of matching standalone tccd proves0x100015684 calls
sandbox_init("com.apple.tccd",1,&error); nonzero return branches to
abort_with_reason namespace25. Matching libsandbox sandbox_compile_named
0x1cf4454d4 calls mac_syscall("Sandbox",22,&name); error falls back to
sandbox_compile_file, which rejects non-absolute profile names. A03 currently
supports only op2, so unsupported named-profile query explains tccd's
profile-not-found rather than proving a missing on-disk profile file.
Matching cache libsystem_sandbox init then uses sandbox_apply for successful
compilation. No profile-query/install implementation or userspace bypass
made; must not claim tccd crash is proven cause of LS seeding wait.
Private extracted binaries/disassembly stay under/tmp/a03-0070, outside git.
Next required observation remains current lsd and dependencies via live ps/
sample after narrow USB ACL. RAM is not presumed sufficient to fix services.

## 2026-11-16: BOOT0071 pass1 still waits on LaunchServices

Second built-in sampler pass at~300s captured in continuation30397.
SpringBoard main and XPC-worker CPU counters and full saved user stacks
exactly match pass0 at~180s. Thus expanded-memory boot reaches app startup
earlier but the database reseeding dependency remains stalled for at least
120s. Other services continue executing; tccd repeatedly aborts with known
profile-not-found reason, dmd data-vault ENOTSUP and analyticsd crash also
persist. No causal link from those crashes to LS stall established.
EP0 node005/010 ACL still missing at19:11UTC; user request pending. Keep
capture30397 running for remaining automatic passes; do not reset merely
because live probe permission is missing. Next ps + sample lsd after ACL.

## 2026-11-16: BOOT0071 first timed sample progresses substantially sooner

Completed initial180s CDC capture: SpringBoard25 has4threads at sampler
pass0 (~180s from sampler start), already in ControlCenter module metadata
and LSContextInitCommon. Its XPC worker explicitly symbolicates to
LAUNCH_SERVICES_IS_RESEEDING_ITS_DATABASE_AND_MAY_BLOCK -> LSCopyServerStore.
Backboardd also has a synchronous wait on that LS path. Cache slide24614000.
By comparison0070 pass0/1/2/3 (180/300/420/540s) all retained1SpringBoard
thread in initializers. This is earlier application-initialization progress
with1GiB; not a controlled speed factor (persistent root caches also changed
between boots) and not proof database seeding now completes.0071 main CPU
user0.152033/system9.990684/runnable83.997187s at pass0.3BGRA swaps observed,
not home-menu content. Need next samples / lsd dependency probe after ACL.
Continuation capture30397 live660s boot0071-usb-continuation.log retains
remaining timed passes. No repeat flash, topology or root changes.

## 2026-11-16: BOOT0071 runtime reached userspace; new EP0 ACL needed

CDC enumerated as1d6b:0104 at USB005/010; initial capture32671 is live.
Actual0071 kernel starts probe worker, surface/display providers and
SpringBoard25, backboardd56, mediaserverd28 and other iOS services. Ongoing
log output at19:08UTC; no kernel panic or home-menu proof. Cannot yet confirm
runtime RAM page count or sample current SpringBoard: libusb open error-3,
new usbfs node root:root0664 without prior device's ACL. Requested only
sudo setfacl -m u:stoned:rw /dev/bus/usb/005/010. Normal tty capture remains
functional and built-in timed samples are independent of this permission.
No reboot/reflash while awaiting observation. Code0c8cc37 pushed.

## 2026-11-16: BOOT0071 controlled 1 GiB RAM test uploaded

BOOT0070 dependency probes34..42: IconServices438 directory enumeration
advanced to idle; lsd101 registration thread subsequently leaves IconServices
XPC wait and enters LSDatabaseRebuildContext registerItems / installed-content
app scanning, sampled in eMMC page-in mutex. Thus not a proven permanent
IconServices deadlock. MobileActivation413 main synchronously requests LS
store while lsd has a synchronous MobileActivation request: possible cycle,
not proof the active seeding thread cannot finish. SpringBoard main still waits.

Live DTB RAM reg is0x80000000+0xfffff000 (runtime-corrected stock template
advertises more and must not be used as actual installed RAM). Checked all23
reserved-memory children plus empty header reserve map: highest reservation
ends0x100001000. New1GiB window0x102000000..0x142000000 is inside live RAM
and avoids all reservations. Retain fixed base, singleCPU, exact0070 kernel,
root, command line, RAMDisk and ADT seed. Payload differs by only2bytes:
header mem_size and chosen dram-size. Loader now accepts only256/1024MiB;
host packer requires private live DTB validation for expanded size and checks
ADT/header agreement. Real loader predicate compiled/tested, synthetic bank/
reserved-child/header-reservation rejection tests PASS; loader full Clang
warnings-as-errors cross-compile/link PASS. No full XNU CI needed (unchanged).

BOOT0071 SHA2563c7482072d5bc03c6e6d96a61f90233e8749fe0f9ad2ee2d7531a1eab32835e3.
Verified exact packaged payload and unchanged ramdisk/DT/AVB tail.0070 CDC
Download reset synced filesystems; Heimdall detected, PIT read succeeded,
BOOT-only upload100percent/success/reboot. Capture32671 waits120s for CDC,
then180s boot0071-usb-initial.log. Runtime pending, no1GiB kernel/home-menu
success yet. No protected partitions or host USERDATA writes.

User asks3GB: does not fit fixed upper window; actual bank ends0x17ffff000,
leaving~2016MiB above current base.3GiB requires additional lower-bank RAM
with explicit secure/modem/framebuffer reservation holes and kernel VM/loader
support; cannot safely set memSize=3GiB at existing base. Check0071 first.

## 2026-11-16: 18:59 UTC repeat confirms persistent SpringBoard service stall

Fresh read-only EP0 ps/sample25/sample101/vm/io completed (seq29..33),
recorded privately in boot0070-usb-stall-check.log. Compared with18:49..18:50
UTC samples, SpringBoard25 main and synchronous-XPC thread have exactly
unchanged CPU times, PCs, stacks and waits after roughly9minutes. All4
SpringBoard thread CPU counters remain unchanged. lsd101 IconServices
registration and MobileActivation request threads also retain identical
CPU counters/stacks. This supports a persistent launch dependency stall,
not continuing SpringBoard initialization; system itself remains responsive.
Fresh ps now lists iconservicesagen438 and mobileactivation413, correcting
the earlier bounded absence observation: service presence alone does not
establish initialization or successful XPC replies. tccd436/analyticsd441
crashes and respawns observed; no new root-cause attribution. Storage
ready1/poisoned0, pageins1490175, compressor5871pages. No home-menu success.
No reset/flash/root writes. Next inspect438/413 and their dependencies.

## 2026-11-16: late0070 SpringBoard advances to LaunchServices database wait

Fresh EP0 samples at18:49..18:50UTC show same SpringBoard PID25 now4threads,
not the earlier single-thread objc initializer. Main thread user0.306551s/
system197.242155s/runnable1441.332378s, blocked __ulock_wait via
_os_unfair_lock_lock_slow. Exact cache slide2c5b0000 symbolication shows
_LSContextInitCommon -> LSApplicationRecord initialization -> ControlCenter
CCSModuleRepository module metadata/filtering. Thread1 waits synchronous
NSXPC reply from _LSCopyServerStore. Repeated sample23/26 main+thread1
stacks and CPU times unchanged over this short interval. This is current
service-wait evidence, distinct from earlier sustained page-in stalls.

lsd PID101 sampled6threads. One waits synchronous IconServices bundle-cache
invalidation during LSBundleRecordBuilder registerBundleRecord and
_LSServerBundleRegistration. Another explicitly symbolicates to
_LAUNCH_SERVICES_CLIENTS_ARE_WAITING_FOR_THE_DATABASE_TO_FINISH_SEEDING.
A separate thread synchronously calls MobileActivation copyActivationRecord.
These identify database seeding/service dependencies; do not establish which
is permanently broken or justify bypassing activation/service replies.
Other lsd main path in install-progress journal recovery. No lsd crash proof.
Late console includes full-screen swap10, not evidence of home-menu content.
VM compressor5755pages (~89.9MiB), pageins1302628 cumulative; storage healthy.
Read-only late90s capture60737 boot0070-usb-late-probes.log. No new BOOT,
root/partition/memory changes. Need follow lsd dependencies rather than assume
SpringBoard still stuck before its own initialization or RAM alone fixes all.

## 2026-11-16: EP0 live probes hardware-confirmed; sustained paging churn

User granted current-device USB ACL. ping/vm/io/ps/threads25/threads56 all
ACK and execute BEGIN/END on BOOT0070 while normal CDC output continues.
Thus dedicated live monitor and host transport work on hardware. New capture
8740: boot0070-usb-live-probes.log (240s); initial660s capture completed
501877bytes with all4sampler passes. SpringBoard25 remains one thread;
first3initial samples wait eMMC mutex/page-in, last waits vm_fault_page.
Live samples repeatedly wait eMMC mutex, with one runnable state4 snapshot.
Exact kernel symbolication confirms emmc_strategy -> cluster_pagein. Cache
slide2c5b0000 resolves user PC1ac676d48 to objc header_info::getHeaderInfoRW
+2c and1ac6739d4 to map_images_nolock+1b0. Slow initializer progress, not a
proven fixed deadlock or SpringBoard IPC/service wait. No home-screen proof.

Live host-monotonic7168.409660..7189.026487 (~20.6168s):7654pageins,
4495reactivations,2368compressions,1750decompressions;221318read sectors
(~108.07MiB,~5.24MiB/s),2027requests,2524write sectors. Snapshot initial
~95MiB wired,~61MiB compressor,~65MiB external/file-backed; free~20MiB.
Swapins/swapouts0 throughout; driver ready1 poisoned0. This establishes
heavy paging/compression/reactivation activity in256MiB profile concurrent
with SpringBoard page-in waits. Suggests working-set churn; does not isolate
physical media saturation, quantify refaults of identical pages or prove
more RAM alone completes GUI. Counter elapsed ticks include yields and must
not be used as exclusive media time. Next compare a validated larger RAM
window after checking stock DT usable/reserved ranges; current loader/ADT/
packer each explicitly require256MiB, so bootarg alone cannot increase RAM.
No root/partition/memory topology change made during these read-only probes.

## 2026-11-16: BOOT0070 CDC logs/worker live; EP0 host permission blocked

Exact A03 diagnostic CDC enumerated; normal660s capture71796 active at
boot0070-usb-initial.log (>350KiB). Runtime A03 PROBE worker start0 enabled1
confirmed; SpringBoard PID25 starts. This proves worker creation and normal
log streaming, not command execution. libusb open rejects host access -3:
/dev/bus/usb/005/008 is root:root0664. sudo -n requires a password. Asked
user for narrow current-device ACL: sudo setfacl -m u:stoned:rw followed by
that exact node path. No broader permission changes or sudo workaround.
Need ACK plus actual ping/threads25/vm/io BEGIN/END. Capture can continue
without EP0 permission. Protected partitions/root unchanged; no GUI proof.

## 2026-11-16: BOOT0070 live-probe build passed and BOOT-only deployed

CI43918800523 SUCCESS exact520d2a7 on macos-26-intel. All4changed source
files match locally compiled0135; checksum manifest/linked probes verified.
Kernel SHA256
5d9f9bf33fce018cabb55deff6139f98eb44cb60fd05d054fdf238a2720ccc3c.
BOOT0070 SHA256
846a19e9f630e950edcb3fa35f24dac32b0f38cd74aaaf4732df32cce38e0d77.
Same0069 loader except image_size; ADT identical; sole argument addition
is a03_probe=1. USERDATA root unchanged. Fresh Heimdall PIT successful;
only lowercase boot uploaded100percent, upload successful/reboot confirmed.
Capture71796 waits CDC,660s boot0070-usb-initial.log. Need actual EP0
ping/threads/vm/io before monitor or GUI success claims. No recovery/GPT/
EFS/NV/root rewrite and no home screen established.

## 2026-11-16: corrected0135 CI failed runner allocation before compilation

CI43914475835 workflow reports failure, but job133464838955 is cancelled
with zero steps, empty runner_name and no logs. Check-run annotation explicitly:
"The job was not acquired by Runner of type hosted even after multiple attempts".
17:04:42..17:19:42UTC allocation window; no compile/link result from this run.
Re-ran all four exact-command local Clang object checks: PASS. No source fix
justified by this infrastructure failure. Retry uses supported macos-26-intel
pool rather than the unavailable macos-15-intel pool. No phone writes.
Retry43918800523 exact520d2a7 acquired macos-26-intel: Set up job passed,
checkout running. Full build result pending.

## 2026-11-16: fix0135 BSD/Mach API visibility; exact-command local compile gate

CI43910152567 failed in sweet_amfi.c:478: vm_map_read_user undeclared.
The function is MACH_KERNEL_PRIVATE; previous local object checks reused a
different file command and did not faithfully reproduce BSD include visibility.
Corrected by bounded a03_probe_read_user wrapper in Mach exception.c; BSD calls
that declared bridge rather than private vm_map API. No extra Mach defines.

Added tools/a03-check-kernel-objects.py replaying each file's own CI Clang
command with path/compiler remapping, original definitions/header order and
warning policy. Extracted failed-run generated headers/source; local Clang
reproduced the exact original error before editing. Corrected sweet_amfi.c,
a03_usb_console.c,a03_emmc.c,exception.c all compile to Apple arm64 objects
in~2s, retaining general-register flags and correct BSD/Mach visibility.
Actual transport/dispatcher ASan/UBSan and PTY nonblocking-log tests PASS;
existing CDC/sampler PASS; plain patch apply/four compiled-source matches PASS.
Full CI link/runtime still required; no device flash or home-screen claim.
Correction committed/pushed1b3fdc1; CI43914475835 dispatched after local gate.

## 2026-11-16: live USB probes implemented; SpringBoard page-in wait confirmed

Exact0069 capture has only sampler pass0 (438539bytes, last update Nov15
22:54UTC), SpringBoard26 one thread state9 in same a03_emmc_lock+8 via
cluster_pagein. User PC stays dyld TLS initializer. Not a complete660s test
or fairness success. Device currently Samsung Download, not CDC; transition
cause unknown.0068 four samples remain stronger repeated-wait evidence.
256MiB memory pressure is a hypothesis pending counters.0133 causes old
io_ticks to include yield intervals;5288062222ticks is not exclusive controller
hold time and cannot be compared that way with0068. No home-screen proof.

User requests simpler probing that leaves console usable.0135 adds private
EP0 commands,4slot queue/dedicated kernel worker and separate host sender;
USB polling/log drain independent. Opt-in a03_probe=1. ping/help/ps/vm/io/
threads PID/sample PID/mem PID HEX HEXCOUNT. threads skips faulting user
backtraces; sample/mem may sleep in probe worker. No memory/register writes,
task stop/resume or new partition operations. BEGIN/END sequence records,
strict request/length/ASCII checks, overflow discard and full-queue rejection.
Actual host ASan/UBSan transport/dispatcher PASS; existing CDC/PID1 monitor/
Download/sampler PASS. Four actual arm64 objects compile using exact0069
headers. Full CI/device validation pending. Private artifacts stay ignored.

Commit0751d9c pushed. Exact CI43910152567 building0135. Accidental dispatch
43910063052 targeted old f1e1601 because initial git commit was blocked by
read-only .git; cancelled without deployment. Required commit/push retried
with elevated filesystem access and succeeded. Real host PTY test proves
log delivery while a simulated control transfer is blocked. No device proof.

## 2026-11-15:0069 read-lock fairness and A03 identity deployed

CI43770218935 SUCCESS exactf1b31e1;20frozen sources expected0134 match.
Loader identical except image_size, ADT/args identical0068. Kernel SHA256
95478c050f54fe62a9e684fdcf8e33f16570367f49efe97814b2a1c8f29befd2;
BOOTbb20a4743ff035343032a6f71f53ba69c3b7ce64455bcd72b033cb2a7b3850ee.
CDC Download reset succeeded; BOOT-only100percent/upload success/reboot
~22:49UTC. Capture245564660s boot0069-usb-initial.log waits USB. Need
compare four GUI kernel waits/CPU times with0068 and actual A03 name lookup.
No speedup/home-screen claim; no root/GPT/protected partition/SMP changes.

## 2026-11-15:0068 baseline capture completed; all four page-in mutex waits

660s completed502735bytes SHA256
ad1bb41db9fca94ed049284f810644874f1d3ee38257b7cfe43b14414495087c. All four SpringBoard samples180/300/420/540s
wait in emmc_strategy mutex during cluster_pagein. Final user0.024999s,
system13.448565s/runnable118.094361s.3full-screen swaps, no GUI completion
proof. CACHE_CTRL0 excludes flush batching benefit; no bulk encryption
setup evidence. Physical media saturation not established from lock waits.
0133 read fairness test CI43770218935 still Build;0069 packaging/deploy
waiters live. No current capture; protected partitions/root unchanged.

## 2026-11-15:0068 three samples repeat controller lock wait

Pass0/1/2 (180/300/420s) all resolve to same eMMC mutex in page-in.
SpringBoard user CPU0.017560/0.019297/0.022635s; system5.714774/8.379390/
10.986783s; runnable59.395987/80.684104/99.274449s. PC changes at pass2 to
objc map_images_nolock, so slow progression persists. These samples identify
lock contention but do not prove all elapsed time has the same cause.
0133/0134 CI43770218935 exactf1b31e1 running; package0069 session7359
checks20frozen-source expected0134, identical0068 ADT/args/loader. Deploy
waiter58959 awaits verified package and normal0068 capture completion.
No additional CPU/clock/memory/storage-format changes. Runtime effect pending.

## 2026-11-15:0068 identifies storage mutex wait; Redmi product leak fixed locally

First kernel snapshot: SpringBoard26 state9 waits in lck_mtx_lock_contended
from emmc_strategy -> spec_strategy -> buf_strategy -> VNOP_STRATEGY ->
cluster_io -> cluster_pagein. Event7c425a8 equals exact kernel a03_emmc_lock
7c425a0+8. This identifies this sample's wait as controller mutex contention,
not an XPC timeout.120s was sampler cadence, not measured timeout length.
Thread CPU user0.017560s/system5.714774s/runnable59.395987s; no saturation
conclusion. Actual CACHE_CTRL=0 means0131 flush batching has no benefit on
this boot. First8192requests939039read/6379write sectors, I/O lock-held
2120578835ticks at26MHz (~81.56s), excluding lock wait.

Prepared0133 read fairness: lck_mtx_yield after each completed16KiB within
buffered reads, letting waiting faulting processes acquire controller; all
sector DMA/register restoration done before handoff. Writes retain existing
serialization/durability. Actual production handler test verifies33sector
read one handoff, writes none; two real kernel objects and plain apply exact
complete-file equality PASS. Hardware effect pending.

User correctly sees Redmi Note10Pro: inherited SweetPlatformExpert hardcodes
getProductName and getTargetName, used in MediaExperience/MediaToolbox lookup
paths.0134 replaces product with Samsung Galaxy A03 and target a03; no
matching-compatible/Apple userland identity or hardware register change.
SWEET internal class/build names remain donor implementation identifiers.
0133/0134 not yet deployed. Kernel-wait resolver fixed for Mach-O S/s symbols
and partial log lines; sampler kernel line may truncate, retain valid frames.

## 2026-11-15:0068 kernel-wait/CPU-time boot deployed

CI43768648670 SUCCESS exact981615130da8f1c0539f3cd2a203899ba3af96c7.
Twenty frozen-source matches PASS, loader identical except image_size,
ADT/args identical0067; a03emmc_batch absent (off). Kernel SHA256
ac02efc2564ccb4c81c92c5fb5b306802b28d1d5f27f0afda91522d94dab4ccb;
BOOTbd6682dcf68e43ddfcac1330d6863dadfe00ea74931a8113cd9c257df1d81582.
CDC Download reset succeeded; BOOT-only100percent/upload success/reboot
~22:30UTC.660s capture239781 waits CDC then timed GUI samples with
A03 CPU/A03 WAIT lines. No root rewrite, protected partition or SMP changes.
No home-screen proof. Kernel traces resolve with exact0068 artifact using
tools/a03-symbolicate-kernel-waits.py. No earlier log file reused.

## 2026-11-15:0067 late180s continues rendering;0132 Build passed

Late capture completed30411bytes SHA256
34011d2f76b428bef7fc9a1d7901806dd144cbfb9623064e187a4fa22390613b. Seven additional full-screen swaps4..10;
generic analyticsd231 corpse crash. Rendering progress alone does not prove
home-screen content. No GUI thread samples after bounded final pass540s.
CI43768648670 Build passed and artifacts uploading;0068 package59465 and
BOOT-only deployment65357 remain pending exact checks. No current capture.

## 2026-11-15: user-reported dmd crash has explicit data-vault failure

0067 full capture confirms dmd153 SIGABRT. Foundation annotation records
NSInternalInconsistencyException: Failed to enable data vault: Operation
not supported (45). This is an explicit missing/unsupported data-vault
operation, not evidence of CPU overload. No successful implementation or
SpringBoard dependency impact established; do not silently return success.
Correction: second traced analyticsd PID is221, not197 in prior entries.
CI43768648670 remains Build;0068 kernel wait/CPU-time package/deploy waiters
remain active. Goal still SpringBoard visible, not daemon crash suppression.

## 2026-11-15:0067 complete660s; four samples, no GUI completion proof

Capture completed493437bytes SHA256
133fe88ab43b53d08c42020bbd453c0d30736b6da183939585f67fdbf4c7efb3.
Four sampler passes180/300/420/540s: SpringBoard25 remains one thread,
state9; last two show same libobjc map_images_nolock stack. It progresses
between middle samples, no permanent-deadlock conclusion.3frame swaps.
HOST normal diagnostics capped32total as designed; no speedup inferred.
Analyticsd195/197 SIGSEGV and tccd189 profile-not-found SIGABRT captured.
0132 CI43768648670 exact9816151 live Build;0068 package59465 awaits20exact
sources and identical0067 args/ADT/loader. No active CDC capture now.

## 2026-11-15:0067 third sample proves slow initializer progress

Pass2 (420s) SpringBoard25 still one thread state9, but PC moves from dyld
hasThreadLocalVariables to libobjc map_images_nolock (unslid1800c39d4),
through _objc_init/libdispatch_init/libSystem_initializer. Thus earlier
identical180/300s snapshots do not establish permanent deadlock. Need
kernel wait/CPU time evidence, not presumed I/O or CPU cause.
Analyticsd195/197 null strlen SIGSEGV captured; tccd189 SIGABRT reason
namespace25: com.apple.tccd: profile not found. Separate from GUI outcome.
0132 real kernel object compiles/plain-apply equality PASS; CI43768648670
exact981615130da8f1c0539f3cd2a203899ba3af96c7 building. Package0068 session
59465 uses20frozen sources expected0132, identical0067 args/ADT/loader,
so request batching remains off. Old0068 waiter231182 stopped.

## 2026-11-15:0067 captures persistent SpringBoard initialization wait

Sampler passes0/1 (180/300s) record same SpringBoard25 sole thread, same
PC/LR/SP/full12frame chain and state9 (TH_WAIT|TH_UNINT). Matching cache
slide1e524000 symbolicates PC1c188ed9c to dyld MachOFile::hasThreadLocalVariables,
LR RuntimeState::initialize and stack through libSystem_initializer, dyld
initializers/prepare/start. PC instruction is ldrb [x0,#0x1a]; saved user PC
alone does not identify kernel wait or prove disk wait. Backboardd changes
from objc class initialization to its executable;3frame swaps occur.
This is persistent wait evidence, not proof of CPU saturation or I/O cause.

Expanded crash tracer now records analyticsd195 SIGSEGV/null FAR with full
stack and annotations. No SpringBoard crash or home-screen evidence.
Prepared0132 adds cumulative thread user/system/runnable times plus wait
event/continuation and bounded12frame kernel stack copied no-fault only for
waiting threads, within their kernel stack bounds and thread lock at splsched.
No printf/user reads while locks held. Real kernel object compile and plain
apply exact equality PASS. Runtime pending.0131 remains off by default.

## 2026-11-15:0067 GUI sampler BOOT-only deployment verified

CI43766598769 SUCCESS exactc2c38372fe44efe11c268d1e18ce0f571a4c7a42.
Nineteen frozen-source comparisons PASS; loader identical except image_size,
ADT identical, sole new arg a03_sample=1. Kernel SHA256
5216ea6e4558446308961d645f92a5307ce7da9fed70add174c701ebc8f05f8f;
BOOTfcaa5d1fe75eb335850430b400473761d99c48b1c58cd5e54490636bd6215f14.
CDC Download reset succeeded; BOOT upload100percent/success/reboot confirmed
~22:11UTC.660s boot0067-usb-initial.log capture233456 active. Need sampler
at180/300/420/540s to inspect actual GUI waits.0131 absent; no root rewrite,
SMP change or performance claim. No SpringBoard home-screen proof.

## 2026-11-15:0066 continuation confirms another analyticsd crash

180s continuation completed11406bytes SHA256
eb85be80ff887e1991435f3817c1d77b8e72adc8f2d819a1bde94ac259932e99.
Generic corpse record confirms analyticsd225 crash; no custom CRASH emitted.
Expanded exception logger is still not complete coverage of every process
termination path. Initial360s no-crash observation applies only to that log.
0067 CI43766598769 now past Build, packaging artifacts; deployment waiter
38683 will BOOT-only flash after19 exact sources/loader/ADT/args/hash checks.
No active CDC reader.0131 dispatch stopped; GUI sampler stays priority.

## 2026-11-15: user asks about CPU0; SMP explicitly unsupported

Verified running cmdline cpus=1 and actual SweetCPU.cpp: start rejects
non-boot CPU identity, panics if topology num_cpus!=1; startCPU returns
KERN_NOT_SUPPORTED; signalCPU supports self-SGI only. Therefore changing
bootarg to cpus=8 is not an SMP implementation. Stock DT describes PSCI0.2
SMC, but secondary firmware startup on this XNU port is unverified. Need
A03 topology/MPIDRs, secondary entry/per-CPU setup, per-core GIC/timers and
cross-core IPI routing before multi-core boot. Single-core CPU contention
is plausible, not established as logo-only blocker; thread sampler first.
No CPU topology/bootarg/hardware changed for this question.

## 2026-11-15: prioritize wait-state evidence over unmeasured I/O hypothesis

User suspects slowdown is not I/O bound. No device timing established an
I/O bottleneck; per-sector code alone is insufficient evidence. Stopped
0131 auto-dispatch before launch; candidate remains off by default and
committed. Priority stays0067 read-only GUI thread snapshots, identifying
whether SpringBoard is running or waiting on IPC/service initialization.
No new storage optimization deployed. CI43766598769 still building.

## 2026-11-15:0066 initial capture complete; default-surface ABI accepted

360s capture completed554548bytes SHA256
f4b0c37894802553dd2ca66e0ebccf1b56c0cc5618e0f741be0c1f5d42e6a6c6.
Backboardd selector3 now succeeds with2scalar inputs;3full-screen BGRA
swaps confirmed. Five SpringBoard startup syscall records, no A03 USER.
No custom CRASH or generic corpse lines in this bounded capture only.
User's latest physical observation remains logo-only; no home-screen proof.

0131 speed candidate committed75ecd42; dispatch waiter15508 will start CI
once43766598769 completes, avoiding workflow concurrency cancellation.
Frozen20-source expected0131 retained. Need batch-off baseline first to
measure actual CACHE_CTRL and I/O time, then batch-on comparison.

## 2026-11-15: speed optimization priority;0131 durable request batching

User clarifies actual speed optimization is priority, not quiet logs.
Inspected live candidate eMMC path: synchronous single512-byte CMD17 reads,
CMD24 writes plus CMD13 status; enabled card cache additionally flushed per
sector. Runtime CACHE_CTRL not previously recorded, so enabled-cache cost
on this phone remains unproven. Current CPU/memory remain1/256MiB.

Implemented opt-in a03emmc_batch=1: buffered USERDATA writes may defer card
cache flush until end of current BSD request, while retaining per-sector
CMD24/status checks and flushing before buf_biodone. No cross-request dirty
cache retained on success. Raw writes retain old per-sector durability.
On later write/read error, previously submitted sectors are flushed if the
controller remains usable; failed flush acknowledges zero durable bytes,
poisons controller and never retries. No timing/clock/GPT/write-scope changes.
16KiB fake request now32sector writes/one flush, versus32flushes when card
cache enabled. This is operation-count evidence, not measured device speedup.

0131 also prints actual CACHE_CTRL and bounded aggregate I/O sector/tick
counters (max8 lines), allowing hardware profiling and batch-off/on tests.
Actual-production MMIO and BSD handler host tests PASS, including bounds,
partial failures and flush failure; real kernel object compile PASS;
plain git apply exact complete-file equality PASS; profile staging PASS.
Not in running0066 or already-building0067 CI43766598769. New CI pending
completion of existing run to avoid concurrency cancellation. Need baseline
and batch-enabled hardware comparison; no speedup/home-screen claim.

## 2026-11-15:0066 BOOT-only deployment verified;0130 CI building

CI43765717894 SUCCESS exact2a79856ddc1b10878616bd8ec2979c5331fbfc76.
Fifteen sources match frozen expected0128; loader identical except image_size,
ADT and arguments identical to0065. Kernel SHA256
49fbaaa86c10e2342f62bc6822b363511aafdf78ac5b858e90dc28621bb3d77a;
BOOT82df93a96158b68cc437adea61dc77f2cb01fef5abd177e1047c857799b1d2e4.
BOOT-only upload100percent/success/reboot confirmed; USB CDC returned,
360s boot0066-usb-initial.log capture active. Includes0127 default-surface
ABI correction and0128 expanded crash evidence; runtime result pending.
No root rewrite or protected-partition writes. No home-screen proof.

0065 continuation deliberately interrupted after approximately168s before
reset:5281bytes SHA256853497e12751ce559f0c6d8c6acadd6b95f8f5dfc331b482b5dea217127edb00.
Generic corpse lines confirm analyticsd226 and dmd194 crashes. Earlier
initial360s no-crash observation must not be extended to this continuation.

CI43766598769 exactc2c38372fe44efe11c268d1e18ce0f571a4c7a42 builds0129
GUI thread sampler plus0130 HOST diagnostic cap. Package0067 waits CI and
nineteen frozen-source checks; only intended new bootarg a03_sample=1.
No0067 flash yet; no measured speedup claimed.

## 2026-11-15: user reports logo-only and excessive HOST logging;0130 cap

User still sees only the Apple logo and reports slowness amid repeated
A03 HOST MIG messages.0065 initial capture contains1694 HOST lines,
78772bytes of554042 total. These are successful recurring host-info IPC,
not crash evidence; synchronous printf costs may contribute, but runtime
speedup is not established. No home-screen success claimed.

Prepared0130 caps each of four normal HOST logging sites at8reports and
reserves independent16failure reports. No host/Mach IPC decisions, arguments,
reply contents or syscall results change. Actual-source budget/saturation
host tests, three real kernel syntax/object compiles and plain git apply
complete-file equality PASS.0129 thread sampler and0130 not yet deployed.
0127/0128 CI43765717894 now SUCCESS;0066 package63560 is downloading/checking.

## 2026-11-15:0065 diagnostic initial capture complete

360s capture completed554042bytes SHA256
3228ff83c72f5731a18f15e4ac88015aad259e552cc146b89d88b432a8e15dfb.
Three full-screen swaps, five SpringBoard25 syscall records, zero custom
CRASH and zero generic crashed lines in this bounded capture. No A03 USER
messages; observer does not prove stdout activity. No home-screen proof.
Follow-up300s capture85699 active boot0065-usb-continuing.log.0127/0128
CI43765717894 exact2a79856 still Build;0066 package63560 awaits success.
0129 sampler committedb99a671, real three-object compile/host gating/plain
apply equality PASS, not in active build. Use after isolated0066 evidence
if startup wait remains. Expanded analyticsd/dmd/tccd tracing not live yet.

## 2026-11-15:0065 confirms SpringBoard execution;0129 thread evidence prepared

Live0065 logs actual SpringBoard25 syscalls: Sandbox scalar check succeeds,
AMFI op0x5a ENOPOLICY103, mkdir /dev EINVAL22 and missing libdispatch path
query ENOENT2. These are evidence of execution, not established fatal causes.
No A03 USER lines emitted so far; /dev/null observer may have no input.
No home-screen proof. Capture56741 still ongoing;0127/0128 CI43765717894
builds independently.

Prepared opt-in0129 bounded thread snapshots for SpringBoard/backboardd:
first at180s, four passes120s apart; max24threads and12frames/thread. Holds
thread refs/register snapshots under task_lock, drops lock before printf or
vm_map_read_user; retains/releases map/thread refs, no suspend/user writes.
Read is racy diagnostic evidence, not debugger-consistent. Worker/process
selection and timing host harness PASS; three real kernel syntax/object
compiles and plain git apply complete three-file equality PASS. No new
thread sampler in running0065 or active0066 CI. Full runtime pending.

## 2026-11-15:0065 GUI diagnostic boot uploaded;0127/0128 CI active

CI43764128179 SUCCESS exact736d3b3. Fourteen downloaded source checks PASS
against frozen0126 snapshot.0065 loader unchanged except image_size,
ADT/root identical, sole added arg a03_userlogs=1. Kernel SHA256
4581ff40e48b05d059455576e3ec7d547619dc76c0123be69b2859ae357dfae6;
BOOTbba5c86c43c1a096f8b54d590102d8cf2ca80b2e4d47727e97a62523fcd5151e.
CDC Download reset from0064 worked; BOOT-only upload100percent/success/
reboot~21:49UTC. Deployment56741 waits USB then360s initial log.

Follow-up0127 surface dimensions +0128 analyticsd/dmd/tccd crash evidence
CI43765717894 started exact2a79856. Frozen15-source snapshot at
/tmp/a03-expected0128/xnu; package0066 session63560 waits successful CI,
exact sources and identical loader/ADT/arguments. No0066 flash. Root and
protected partitions unchanged; physical SpringBoard GUI still unverified.

## 2026-11-15: further analyticsd/tccd crash evidence

Fresh180s0064 capture completed24497bytes SHA256
9d836d9dfa4f4353d02965174cab08f501e06536655e26cc7b1d25ff9f796d05.
Generic corpse lines confirm analyticsd165 and tccd172 crashes; six further
full-screen swaps4..9 occur in this capture. Thus the system continues
rendering despite these crashes, without proving dependency independence
or SpringBoard success.0128 extended to tccd too (14 independent bounded
slots total); actual-source selection/saturation host test and real kernel
syntax compile PASS. No daemon suppression.0125/0126 CI43764128179 now
uploading artifacts after successful Build;0065 package34897 still waits.

## 2026-11-15: user-reported analyticsd crash confirmed; correct crash scope

User reports analyticsd crashed. Review finds existing completed0064
continuation has Process[126] crashed: dmd and Process[157] crashed:
analyticsd (Too many corpses being created), despite zero custom CRASH
records. Earlier statements implying zero crashes globally were too broad:
0108 monitors only11 selected names and excluded these daemons. Relauch
records also show analyticsd repeated. Keep distinction explicit.

New180s capture75436 boot0064-usb-analytics-report.log records further
analyticsd165 crash plus swaps4..6. USB remains live; no evidence yet these
analytics crashes directly kill SpringBoard/backboardd. Prepared0128 to add
independent two-report slots for analyticsd/dmd to existing crash diagnostics.
Actual-source host name/gate/saturation tests, real kernel syntax compile
and plain git apply complete-file equality PASS. No daemon disabled or
return code changed. Not in active0125/0126 CI43764128179, still Build.

## 2026-11-15:0064 continuation complete; diagnostic build still active

Additional300s capture completed8093bytes SHA256
eb640a7a1ce2933a97069f10a38b6dc38b39c297837d43a5937ba01978dd3004.
Zero CRASH, zero new framebuffer/surface calls or SpringBoard/backboardd
spawn authorization.0064 remains USB CDC. Combined bounded captures do not
establish a rendered home screen. CI43764128179 exact736d3b3 is still
in Build; package34897 remains waiting. Next verified0065 BOOT-only adds
only bounded userspace logs and SpringBoard startup syscall evidence.
0127 remains a separately committed/tested default-surface correction,
not included in this diagnostic build. Current regression suite passes.

## 2026-11-15:0064 initial360s capture complete

Completed504774bytes SHA256
dec6bfa097c7ab88876237faa6c26937f71d40b55c6c856fa9e39fff5f4dc352.
Zero CRASH, four entitlement grants, three full-screen swaps. Repeated
instance-start op6 ENOTSUP persists; no claim this hint failure is fatal.
Backboardd/SpringBoard each have a single spawn authorization. Continued
300s capture18693 now active in boot0064-usb-continuing.log. Diagnostic
CI43764128179 still in Build;0064 left running. No home-screen proof.

## 2026-11-15:0064 reaches frame submission; instance notification ABI gap

0064 live capture now records three successful full-screen swaps, four
entitled work-interval grants, zero CRASH, and repeated syscall499 op6
ENOTSUP45 with instance buffer length0x38. Earlier commentary called this
workload configuration; exact libsystem_kernel decode corrects that:
work_interval_instance_start1bf1348b4 sends6, update1bf12e5b0 sends7,
finish1bf131390 sends8; all pass0x38-byte instance data. These operations
are absent from the current open-source XNU sys_work_interval switch.
Instance_alloc1bf139d28 stores WI ID at0, create flags at30; setters store
start10,finish18,deadline20. This is not SET_WORKLOAD_ID(op0xb). No generic
success/ABI remap added; exact semantics need further review or evidence
that these hint failures block GUI. Stock open-source8792.41.9 source also
omits instance operations.0125/0126 diagnostic CI43764128179 remains Build.

## 2026-11-15:0064 grants actual work interval; default-surface ABI correction

Live0064 capture records A03 Sandbox: backboardd entitled work-interval
privilege granted, with no observed syscall499 EPERM afterwards and zero
CRASH so far. This proves0124's actual grant path, not full GUI success.
Initial360s capture remains active; no swaps yet at this observation.

Exact iOS16.0 _kern_GetLayerDefaultSurface1ad7daf08 checks layer0 in
userspace, then sends two widened uint32 canvas dimensions at client+484.
Initialization1ad7d9890 reads canvas-width/canvas-height provider properties
into484/488 (CFString backing1ad7e0911/91e); SetDisplaySize1ad7d7fb4 also
sets these from dimensions.0123's input0==0 layer guard was incorrect.
Prepared0127 to accept native720/1600 dimensions (or zero for undiscovered
provider dimensions), reject conflicting nonzero geometry, and return the
existing validated physical-surface port. No new allocation or generic
selector success. Actual-source method tests, kernel syntax/object compile
and plain apply full-file equality PASS. Not yet in CI43764128179/0065.

## 2026-11-15: BOOT0064 upload success; GUI diagnostic CI started

BOOT-only upload reached100percent, reported success and reboot around
21:30UTC. USB CDC re-enumerated1d6b:0104; initial360s capture now growing
in boot0064-usb-initial.log (deployment87223). No runtime result inferred
before userspace reaches the relevant call. Root/ADT preserved.

Follow-up0125/0126 diagnostic CI43764128179 started exact736d3b3 while
0064 runs. Package0065 session34897 waits successful CI,14 source checks
against frozen /tmp/a03-expected0126/xnu, identical loader/ADT and sole
additional a03_userlogs=1. Diagnostics preserve syscall/devnull decisions.
No0065 flash;0124's isolated runtime observation takes priority.

## 2026-11-15:0124 full CI success and verified0064 package

CI43762755721 SUCCESS from640a2a1. Twelve downloaded source comparisons
against frozen0124 source PASS.0064 loader unchanged excluding image_size,
ADT identical, root unchanged; sole added arg a03_work_interval=1.
Kernel SHA2567a20a47f23c1ec5e7c6774e823012ae95431389ff86512b8c5443e0007f4e1b4.
BOOT SHA256f98965ef3f0f05f98a18ff36cd5dea9834869d5308b799445786022f36113d05.
Late0063 capture intentionally stopped before reset:4006bytes SHA256
3d8b239decc650bfb4c6c3e47908da3d7ea970615110277e69d28fb85063d687,
zero CRASH. CDC Download-control reset succeeds; Samsung Download now
observed. Deployment87223 proceeds authorized BOOT-only flash, then360s
initial capture. Upload/runtime result pending; no home-screen proof.

## 2026-11-15: extended0063 capture complete; SpringBoard diagnostic coverage

Extended600s capture completed90815bytes SHA256
07d49975277cea6c77336f72ec247d922d68b31d626abd169634c330f13d4193.
Zero CRASH; eight additional swaps4..11, no repeated SpringBoard/backboardd
spawn authorization. USB CDC still enumerated. No home-screen observation.
0124 CI43762755721 still in Build at21:28UTC; package54915 remains live.

Existing0120 startup syscall diagnostics omitted SpringBoard itself.
Prepared0126 to add a fifth independent192-report slot, preserving the
existing opt-in/error filter/path/header logic and syscall decisions.
Actual-source host tests include SpringBoard's independent cap; real kernel
syntax compile and plain git apply full-file equality PASS.0125/0126 are
follow-up diagnostics, absent from0124 CI and running0063. Guide refreshed
to distinguish physical Apple logo from SpringBoard success (8396f6e).

## 2026-11-15: extended0063 rendering continues during0124 build

Extended capture now includes swaps4..11 from alternating720x1600 BGRA
surfaces2/3, zero CRASH in latest86767-byte snapshot. Capture600s remains
active; no final hash claimed. Physical observation remains Apple logo.
0124 CI43762755721 is authoritatively in Build; package54915 remains live.
Frozen expected0124 sources now reside /tmp/a03-expected0124/xnu so later
independent0125 local edits cannot contaminate exact CI comparisons.

0125 followup includes mem.o general-register codegen; complete two-file
plain git apply equality, real syntax/object compile and actual-source
observer tests PASS. Latest commit75148a0 pushed. Neither0124 nor0125 has
been hardware-tested yet; no new flash/root rewrite/protected write.

## 2026-11-15: bounded userspace-log observer0125 prepared

While0063 remains running and0124 CI builds, prepared an independent opt-in
read-only /dev/null observer for SpringBoard/backboardd. It copies at most
255bytes from a duplicated uio, at most128writes/process. Original uio and
/dev/null success/error behavior stay unchanged, including diagnostic-copy
failure. Control bytes sanitized. Actual-source tests cover disabled/name/
bounds/failures/original-uio preservation; real kernel syntax/object compile
and plain git apply complete-file equality PASS. Not in running0063 or
active0124 CI; hardware untested. Intended to expose startup messages that
would otherwise be discarded, if the entitlement test still stalls.

## 2026-11-15: BOOT0063 five-minute continuation complete;0124 CI active

Continuation300s completed136106bytes SHA256
9cc3959853e7f7698f46860079c84422aa1771cdd50af9e64ce8b7e06ab96b51,
zero CRASH, no repeated SpringBoard/backboardd spawn authorization, three
successful full-screen swaps. Physical Apple-logo report remains the visible
milestone, not a home screen. Extended600s capture79994 now running in
boot0063-usb-extended.log;0063 is left running during the build.

0124 committed640a2a1; full CI43762755721 running exact commit. Real
sweet_amfi.c syntax and object generation PASS, actual-source privilege
tests PASS, plain git apply complete-file equality PASS. Package0064
session54915 waits CI success then checks12 exact source files, identical
loader(except image_size)/ADT/root and sole argument a03_work_interval=1.
No0064 flash yet. Selector29 decoded as GetDisplayArea with8-byte structure
output; existing Unsupported did not prevent later logo/frame submission.
Do not assume all unsupported selectors or the Caches denial are fatal.

## 2026-11-15: physical Apple logo and actual framebuffer swaps

User reports the phone now shows an Apple logo. Continuation0063 USB log
now records backboardd SwapBegin/SwapEnd success and three full-screen
720x1600 BGRA swaps from allocated surfaces2/3 (bpr3072). This is stronger
than provider registration and aligns with physical display observation;
it does not establish that SpringBoard's home screen has loaded. Earlier
no-swap assessments were bounded observations superseded by this capture.
The same boot remains running to allow further initialization.

Exact stock backboardd XML entitlement includes boolean
com.apple.private.kernel.work-interval=true. CREATE2 op4 reaches kernel
priv_check_cred(PRIV_WORK_INTERVAL), but the A03 Sandbox policy currently
has no privilege-grant hook. Preparing opted-in0124 to grant only this
privilege to the current credential with that validated boolean entitlement;
other privileges/credentials retain existing decisions. Actual-source host
tests pass opt-in/credential/privilege/entitlement negative cases and the
bounded log path. Real kernel syntax/object compile and plain git apply
full-file equality PASS; profile stages0124. No new flash yet.

## 2026-11-15: BOOT0063 runtime reaches the display provider

Initial120s USB capture completed422685bytes SHA256
a5d459ca584ab49f3679244893655e6e3319c5496c08f16e8fc704411025aab9.
Zero CRASH records; one SpringBoard/backboardd spawn authorization each.
IOCoreSurfaceRoot registered; AppleCLCD reports720x1600 stride2880 at
0x9e000000, default surface1. MobileGestaltHelper selectors8(display size)
and28(dot pitch) return success. Backboardd reaches framebuffer selector29
with8-byte structure output and receives Unsupported0xe00002c7. No swap
submission or rendered SpringBoard established. This corrects the earlier
initial-capture assessment that backboardd had not opened the framebuffer.

Backboardd56 still records mkdir_extended220 EACCES13 for its resolved
system-container Library/Caches. It also records work_interval_ctl499
operation4 EPERM1. These are observed failures, not yet proven causes of
missing GUI; selector29 meaning/required behavior also needs exact ABI
review. No broad permission or selector-success bypass applied.

Continuation300s capture is still running at this observation; its current
75586-byte snapshot has zero CRASH and no additional framebuffer calls.
Do not treat a growing log hash/length as a completed capture. USB CDC
1d6b:0104 remains enumerated. HFS atomic-save repair and display-provider
registration are concrete progress, not proof of a visible home screen.
Private logs remain ignored; no additional flash or partition write.

## 2026-11-15: display candidate BOOT0063 deployed

CI43760748014 SUCCESS exactee1307c. Twelve downloaded source comparisons
PASS.0062 loader retained except image_size; ADT only adds disp0 and removing
it byte-matches0062; sole boot argument a03_display=1. Kernel SHA256
cf24c083bf9a2c29735e01ce8ae860b4d8d4091b4f029007f751f369b8d98797.
BOOT SHA256 dd217cf6bf20263d35db9ddf182d5d2fceea2be7d3476a6fb62c49fb7268f230.
0062 CDC Download-control reset succeeded again: CDC disconnected and
Heimdall detected Download. BOOT-only upload100percent/success/reboot21:08UTC.
Deploy/capture28481 waits CDC then120s, private boot0063-usb-initial.log.
No root rewrite or protected-partition write. Provider registration, GUI and
SpringBoard runtime results pending.

## 2026-11-15: later0062 container access evidence and selector tests

Additional120s capture193407bytes SHA256
fcfe7772b22177916d749fabeba33880ddfc217a6de35f627c3e4c24133debc3.
Zero CRASH, zero new SpringBoard/backboard spawns, four successful HFS
exchanges and no atomic-save failures. Backboardd56 now records an actual
mkdir_extended syscall220 EACCES13 on its resolved system-container
Library/Caches. This is concrete permission failure, not proof that the
external ACL resolver is its cause. Existing CONFIG_EXT_RESOLVER differs
from donor; no permission bypass/removal applied to0123 test.

Added actual-source external-method host test for scalar input/output
counts, null buffers, exact400 swap versus3ff/46c, invalid notification type,
layer0 restriction and unknown selector propagation. PASS. Four real Mach-O
objects generated with general-register codegen.0123 CI43760748014 still
running exactee1307c; later test/docs commits do not alter kernel candidate.

## 2026-11-15: display CI43760748014 running; BOOT0062 extended window

0123 commit ee1307c pushed; full CI43760748014 active. Package0063
session55131 waits exact run success then12 exact source comparisons.
It parses0062 ADT and adds only disp0; removing it must byte-match original.
Loader check and sole argument addition a03_display=1 required before test.
No0063 flash yet.0062 remains USB CDC. Its additional300s capture completed
6887bytes SHA2563a713cf9cdb7eada55228938f0eb4b475cbe0b7eddb61ebcc8a8b6cf96fcd809,
zero CRASH records. This still does not prove a GUI or running SpringBoard.
Exact IOSurface lookup selector4/port lookup34 use one scalar input and
a68-byte output; create selector0 also one scalar input/a68 output. Port
lookup checks base=-1 to reuse cached client, supporting applied0068 fix.

## 2026-11-15: opt-in display/surface candidate0123 prepared

Adapted pinned SWEET0046 software IOSurface/framebuffer provider, plus0068
cached lookup reference correction, for exact observed iOS16.0 swap400 ABI.
No Qualcomm MMIO. Explicit a03_display=1 gates service startup/nub; ADT
--display adds only a03,display720x1600 node. Framebuffer start checks exact
9e000000/720/1600/2880/depth32 boot video. Unknown external selectors return
Unsupported rather than generic-success buffers. Scalar shapes/type0 and
exact swap input checked; pixel copier accepts BGRA4byte elements only.
Allocation64MiB and total wiring96MiB caps fit current256MiB kernel window
better than donor1536MiB cap. No GPU/touch or active hardware vsync claim.

Actual copier host test covers source extent, mask, missing surface, format,
element size, clipping and destination sentinels. Opt-in ADT tests PASS.
Four actual kernel C++ files compile with general-register flags; plain
git apply yields exact full files. Profile staging, Python compile and diff
checks PASS. Full CI/hardware pending;0062 remains running. No GUI proof.

## 2026-11-15: BOOT0062 confirms HFS atomic-save repair

USB CDC returned and initial100s capture completed371425bytes, SHA256
a929c52f3a5946526b1024fbeeba5e1487d9be979a680fb084ee92388e092640.
Three A03 HFS root regular-file RENAME_SWAP exchange results are0; zero
Failed to atomically lines, versus two failures in0061. UMD creates system,
default and universal personas. One SpringBoard and one backboardd spawn
authorization; zero CRASH records in this bounded window. Spawn/absence of
crashes is not proof of stable process/display. Notification registration8
persists. Continuation session2668 reads300s;0062 stays running.

Exact SwapSetLayer1ad7d68dc uses object+18 as transmitted record: swap ID
object+68 => record+50; surface ID object+6c => record+54; source rect
object+7c => record+64; destination object+dc => record+c4; mask object+11c
=> record+104. These match donor offsets despite smaller total400 bytes.
EnableNotifications1ad7daaf8 sends selector72 with four scalar inputs;
GetID1ad7db130 sends selector7 with one output. IOSurface client helper
1a291cc10 references a68-byte lock result, consistent with donor size.
Read-only ABI evidence supports a scoped display-provider adaptation next,
not a claim that donor generic-success selectors or A03 scanout are tested.

## 2026-11-15: corrected0122 deployed as BOOT0062

CI43759153171 SUCCESS from28b8b81. Six source comparisons against validated
local tree PASS, including kpi_vfs.c contextual patch.0061 loader excluding
image_size, ADT and root retained; sole boot-argument addition a03_hfs_swap=1.
Kernel SHA256 e54b8712b0af529e253bd3b20864754e8621e6f9722a920130898029ff5386a8.
BOOT SHA256 0f63d63fcd2cc20796f97931ee88b56ec84c62ca5715cd8c6b05ace5e448cd24.
Already present Download device; Heimdall boot-only reached100percent,
reported upload success and reboot20:47UTC. Deploy/capture session82030 waits
for CDC then100s, private boot0062-usb-initial.log. No host USERDATA/protected
partition write. HFS runtime effect and SpringBoard remain to be measured.

## 2026-11-15: resumed goal; corrected HFS build and display ABI review

Current host revalidation finds Samsung04e8:685d Download, no ADB/CDC.
Corrected0122 CI43759153171 is building exact28b8b81; package0062 session17809
waits this run and checks six CI source files, loader, ADT and sole added
argument a03_hfs_swap=1. HFS actual-source regression passes again. No0062
flash yet. Previous goal turn made progress correcting CI patch application.

Read-only exact iOS16.0/20A362 cache review also exposes a later display ABI
incompatibility: IOMobileFramebuffer kern_SwapEnd1ad7d6568 sends selector5
with1024-byte (0x400) input at1ad7d6588. Donor0046 requires at least0x46c.
GetDisplaySize1ad7d78e8 requests selector8 with two scalar outputs;
GetLayerDefaultSurface1ad7daf08 requests selector3 with two scalar inputs
and one output, consistent with the donor for those calls. Private disassembly
in /tmp/a03-iomfb-*.txt; Apple bytes stay ignored. Current A03 profile omits
0046 and mkadt_a03.py removes disp0, so no display service is being claimed.
Need decode exact swap layout before adapting donor display/surface code;
blindly selecting0046 would fail this demonstrated ABI check. This review
does not prove backboardd/server recovery, physical GUI or SpringBoard.


## 2026-11-15: independent Linux reader; corrected catalog root address

Current photos IMG_20261115_012537_763.jpg/012540_967/012610_175 confirm
BOOT0042 direct CMD17 at absolute catalog LBA0x1097c10 returns sixteen zero
bytes. GPT CRC matches bb4c2987. HFS node0 still fails. This bypasses BSD/HFS
but cannot yet separate on-card contents from SDMA behavior.

Found second diagnostic address error: local B-tree root=274, nodeSize=8192.
Actual root relative offset=0x2cd82000+274*8192=0x2cfa6000, absolute
LBA0x1098d30. Previous0x1097d22 added node index as sectors. Patch0098 fixed;
not rebuilt/flashed. Local root first32:
0000000000000000000300400000001a00000001000a0041003000330069004f.
Catalog-header zero evidence is unaffected by this correction.

Added tools/a03-linux-reader-image.py and tools/a03-linux-reader-init.c:
unchanged matching stock Linux kernel/DT, static init instead of Android
init, no USERDATA mount, all partition opens O_RDONLY. Existing GPT
CRC/range/identity validator and sysfs device numbers gate reads/export.
Configfs mass-storage LUN0 is RAM diagnostic text; validated USERDATA LUN1
is read-only, set before backing file. FB0 display uses queried geometry.
This is a storage diagnostic toward launchd, not replacement iOS userspace.

Reader0001 BOOT SHA256:
6ff699daf728b0a1b451fcdaf2d154e2ee092f93d76495a6dd02abbe7aaf61a4.
Heimdall BOOT-only upload100%, success and reboot; initial sandbox USB-open
failure occurred before protocol, escalated retry succeeded. User reports
Samsung logo; no USB reader. Linux init execution is UNPROVEN. V1 incorrectly
assumed partition device179:55; CONFIG_MMC_BLOCK_MINORS=8 and extended device
numbers make that unjustified. V1 validation failure could not expose report.
Fixed device-number discovery, report-on-validation-failure and FB0 output.

Latest UNFLASHED candidate shim/a03/out/a03-linux-reader-0004.img SHA256:
59ecbf0d2de5d58e77c36e6ae8e498c7e956b507f9c2f72221b5474a8e56db42.
Original kernel SHA256 retained:
1d1266f15bb8f0f1f9f501fc763c0c7451aa7cdc7db04693ea3d5d49c2646d90.
Static AArch64 -Wall -Wextra -Werror build PASS; newc entries/modes/ELF,
unchanged kernel/DT checked. GPT parser and BSD harnesses PASS; Python compile
and diff checks PASS. No Download/reader USB at last check. Next: return to
Download, flash reader0004 BOOT-only, inspect report and USERDATA catalog.
No USERDATA/protected-partition write this session. No launchd/SpringBoard.

## 2026-11-15: latest catalog failure remains below userspace

Screenshot `IMG_20261115_004550_780.jpg` shows GPT CRC validation, USERDATA
selection, BSD root `a03userdata0`, and HFSX volume-header recognition all
passing. HFS then reads catalog node 0 as zero (`hfs_swap_BTNode: offset #0
invalid (0x0000)`, `BTOpenPath` error 5, root mount errno 19). No launchd or
SpringBoard evidence is present. This image predates the direct catalog-root
probe in commit `66af3d4`; workflow `43655138104` is building a BOOT-only
diagnostic that reads both the catalog fork and declared root node directly.
No USERDATA write is indicated until those bytes are compared with the local
image.

## 2026-11-15: direct catalog-root diagnostic deployed

Workflow `43656529029` succeeded from commit `31d9bc2`; the corrected `0098`
patch linked. Packaged BOOT candidate `a03-xnu-0042-d7c03ad.img` has SHA256
`6c729a41d931fd2d151d42aaccf005b57d972206d410fbce7cb46da3a42c6115` and
uses the emmc-enabled ADT with USERDATA root selection, USB probe and eMMC
trace. Heimdall detected Download mode and uploaded only PIT entry `boot` to
100%, then rebooted. USERDATA, GPT, recovery, bootloaders, EFS and NV were
untouched. Await direct catalog-fork/root-node output.

The resulting USB probe reported `A03 USB: AON EB1=001eb8f3 RST1=00000000
PHY_TEST=00000000 PHY_CTRL=0000000a CTRL1=00000000 CLK_REF=00000000` followed
by `MUSB clock gated; controller not accessed`. AON reset is released, but
the reference clock is disabled, so no MUSB register evidence or USB
transport is available yet. HFS still fails with error 5; this USB state does
not identify the catalog read failure.

## 2026-11-14: SDMA source audit

Compared `shim/a03/xnu-loader.c` with the installed T606 Linux driver
(`android_kernel_samsung_a03/drivers/mmc/host/sprd-sdhcr11.c/.h`). The
existing command value `0x003a0011` was confirmed correct for a single-block
read: data-present, R1 response, read and SDMA. The loader was corrected to
mirror two controller setup details from Linux: enable SDHCI v4 64-bit system
address mode through HOST_CTRL2 (0x3e) bit 13, and write the 512-byte block
size as a 16-bit `0x7200` value before the 32-bit block count. Host build
passes with `A03_EMMC_SNAPSHOT=5`; no device flash or USERDATA write has been
made for this audit. Commit `f98d116`.

## 2026-11-14: corrected kernel candidate

XNU workflow 43641820579 succeeded from commit `4e4873e`; the linked A03
USB/direct-catalog gates passed. Kernel SHA256 is
`f19877e2842a7cff12433efd770910174307decae7d6c92c6ab39142d03454a5`.
Using the verified iOS root image, I packaged
`shim/a03/out/a03-xnu-0040.img` with `rd=a03userdata0 rootrw=1` and the
existing USERDATA write-enabled path. Image SHA256 is
`94e18760fe23c75b48f0ac17e1af42cde93d493645b2d3b9a8bfe348b709a9a2`.
This is a host artifact only; no device write has been made for it.

## 2026-11-14: BOOT0040 written

After a transient Heimdall protocol-init failure and USB re-enumeration, the
candidate was transferred only to PIT entry `boot`. Heimdall reached 100%,
reported `boot upload successful`, and rebooted the device. No USERDATA, GPT,
recovery, bootloader, EFS or NV write occurred. Ten seconds after reboot the
host saw neither ADB nor a USB diagnostic device; this does not distinguish a
displayed XNU panic, a storage-root stall, or a silent early hang. Await
physical output or later USB evidence before claiming iOS userspace progress.

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

### 2026-11-14: iOS16.0 HFSX USERDATA installed; BOOT0026 flashed

- After final source/geometry/fsck/cache checks, Heimdall2.2.2 transferred
  the exact16GiB HFSX image to lowercase PIT `userdata` ID55, without PIT,
  repartition, or reboot. Progress100%, `userdata upload successful`.
  The transfer does not independently read back/hash USERDATA.
- Heimdall `--resume` then downloaded fresh PIT and wrote only BOOT0026;
  progress100%, `boot upload successful`, no reboot. Image SHA256
  e012784bf236bae131029b02c0a5239546081eebb039852e9de64a465528086b.
  Cmdline selects rd=a03userdata0, a03emmc_rw=1, rootrw=1,
  ignition_level=1, -nobsdmgroot; opt-in Apple entitlements profile.
- Both upload results are host/device protocol confirmations, not partition
  readback. Phone remains Download after both --no-reboot operations. Next
  user-controlled hardware power-on/reboot, observe kernel HFS mount and
  userspace output/panic; no SpringBoard/runtime claim until observed.
- First hardware reboot attempt via `heimdall close-pc-screen` failed protocol
  initialization; `--resume` retry and BOOT-only reflash with normal reboot
  also failed session startup. Device remained detected in Download mode.
  No third flash occurred and USERDATA root was not changed. Physical
  Download-mode key power-cycle requested; boot/runtime result pending.
- After the failed Heimdall reboot attempts, host observations at15:22 UTC:
  USB device disappeared from Download mode; no Samsung USB or ADB interface
  has re-enumerated through15:23 UTC. This is not evidence of a successful
  boot or panic; display/serial result is still needed. Avoid further flashes
  until its physical state is known.

### 2026-11-14: XNU selects USERDATA; HFS catalog read fails

- User supplied photo `IMG_20261114_162431_124.jpg`. The visible XNU log
  identifies `a03userdata0` as BSD root (major2/minor1), enters
  `vfs_mountroot`, then reports an invalid catalog B-tree node (fileID4),
  `BTOpenPath` error5, `hfs_mountroot failed: 5`, and `cannot mount root,
  errno = 19`. Later diagnostics show eMMC ready, USERDATA read/write and
  BOOT read-only. This confirms root selection and the failed HFS mount; it
  does not establish successful Apple launchd or SpringBoard execution.
- The image was locally verified before upload, but Heimdall did not read
  USERDATA back. The log alone cannot distinguish an incomplete transfer,
  raw/block read mapping issue, or HFS interpretation issue.
- Added opt-in `catalog_probe` to `a03-root.yml`. Its RAM-root PID1 helper
  reads 512 bytes at USERDATA byte offset `0x2cd82000` (catalog fork starts
  at allocation block183682 * 4096) via `pread` on raw and block USERDATA
  nodes, prints each observed first16 bytes, and marks whether they match
  `00000000000001000003000000011200` from the verified image. Read-only;
  it does not alter the installed filesystem or storage driver behavior.
- Local AArch64 assembly and `mkinit.py` validation passed, producing a
  16,635-byte diagnostic PID1. Not yet run under XNU or on the phone. Next:
  build the diagnostic root, use the known root-selection kernel, and
  compare both reported prefixes with the image before changing HFS or
  storage code. Physical USB/device state remains unconfirmed.

### 2026-11-14: catalog diagnostic BOOT0027 prepared; flash transport failed

- Pushed diagnostic implementation as `0f23cbc` and dispatched root build
  `43611194283` with `catalog_probe=true`; completed successfully. Downloaded
  32MiB HFSX RAM-root artifact SHA256
  `525293710b033e7d149d600a6d41d51fe18cdc3b8bbc784bdca9e2795938827b`.
- Reused root-selection kernel from successful XNU run `43602657100`,
  SHA256 `124d32ca8812840a171e127c6a24dfaf5da85530eec810aa3f0f4e30605f1d80`,
  A03 ADT `a03-0025-write.adt`, and verified Magisk BOOT base. Packaged
  `shim/a03/out/a03-xnu-0027-catalog-read.img`, SHA256
  `79bea0b10029b368b763e5d6bc12340b3cd52b825dce6db3e3a204b7b5dc20fc`.
  Cmdline selects `rd=a03userdata0` with writable USERDATA root selection;
  the diagnostic HFS image remains in the payload as the RAM disk. Catalog
  reads themselves are read-only.
- Heimdall detected Samsung Download USB. A full live PIT read succeeded
  once (Spreadtrum tag, 60 entries, USERDATA ID55); subsequent PIT and BOOT
  sessions failed protocol initialization. Verbose flash result:
  `Failed to receive handshake response. Result: -7`. No PIT selection or
  image transfer occurred; BOOT and USERDATA were not written in these
  attempts. Restore BOOT SHA256 remains
  `94fa7c5347b00e49fe1dc60a4edae958ddd5dac9accdbcddbeb743b5215e9ce7`.
- Next hardware step is restore a clean Download-mode USB session (physically
  reconnect/re-enter Download mode), then flash only BOOT0027 and capture
  PID1 raw/block catalog bytes. Do not rewrite USERDATA before comparing
  those bytes against the verified image. No iOS HFS mount, launchd or
  SpringBoard success yet.

### 2026-11-14: BOOT0027 transferred and reboot requested

- After host USB reset/re-enumeration, Heimdall initialized successfully,
  downloaded the PIT (one recoverable empty-bulk warning), uploaded only
  `a03-xnu-0027-catalog-read.img` to lowercase `boot` at 100%, and reported
  `boot upload successful`. USERDATA and all protected partitions were not
  written.
- `heimdall close-pc-screen --resume` completed `Rebooting device`. Eight
  seconds later neither Download nor ADB USB was visible. This is not
  evidence of PID1, catalog output, HFS mount, launchd or SpringBoard.

### 2026-11-14: corrected catalog probe packaging

- BOOT0027 selected `rd=a03userdata0`, so a failed HFS mount could prevent
  its PID1 diagnostic from running. Added `--catalog-probe` to
  `tools/a03-pack-root.py` and prepared BOOT0028 with the same eMMC provider
  enabled but `rd=md0`, preserving the independently verified RAM HFS root.
  This lets PID1 read USERDATA catalog bytes without requiring HFS to mount
  USERDATA first.
- BOOT0028 SHA256 is
  `e99ec4100f5a00028b5d24fc29b80e1e1ab5acd74c447af8100062923ede38ae`.
  Kernel/root/ADT inputs are unchanged and catalog reads remain read-only.

### 2026-11-14: second HFS catalog failure photo

- User supplied `IMG_20261114_165241_152.jpg`. The visible log again names
  BSD root `a03userdata0` (major2/minor1), enters `vfs_mountroot`, and reports
  invalid catalog B-tree node0 (`blockSize 0x200`, zero records),
  `BTOpenPath` error5, HFS mount failure5 and root errno19. A repeated
  attempt reports catalog node offset8 invalid (`0x8888`) and HFS error3;
  HFS marks the volume inconsistent. The photo's lower diagnostic includes
  `A03 eMMC: BOOT + USERDATA BSD devices ready; RAM root unchanged`.
- This is another failed USERDATA root mount, not launchd/SpringBoard. It
  still provides no raw/block catalog bytes and does not prove whether the
  image transfer, sector read, or HFS mapping is responsible. BOOT0028's
  RAM-root catalog diagnostic remains the next discriminator, but has not
  been flashed. Latest host check had no Download/ADB USB enumeration.

### 2026-11-14: BOOT0028 catalog probe returned zero data

- User reports BOOT0028 PID1 output: both raw and block reads at USERDATA
  byte offset `0x2cd82000` completed but returned sixteen zero bytes and
  reported `MISMATCH`.
- The verified 16GiB HFSX image contains
  `00000000000000000100000300000003` at that offset. Therefore both BSD
  interfaces agree on an all-zero sector; this is below HFS and points to
  eMMC SDMA/addressing or the installed USERDATA contents. No write was
  performed by the probe.
- The probe's expected constant has been corrected to the verified bytes.
  Before any USERDATA rewrite, add a read of the HFS volume header at byte
  offset1024 and compare it with the verified image, then inspect the driver
  partition-LBA arithmetic.

### 2026-11-14: RAM-root catalog probe returned zero sectors

- User supplied the BOOT0028 PID1 output: both
  `A03 CATALOG raw first16` and `A03 CATALOG block first16` report
  `MISMATCH` followed by sixteen zero bytes. Both interfaces therefore
  completed a 512-byte read at USERDATA-relative byte offset `0x2cd82000`,
  but returned an all-zero sector rather than the verified image's actual
  HFSX catalog prefix `00000000000000000100000300000003`.
- This is decisive storage-path evidence below HFS: raw and buffered BSD
  paths agree on zero data. It rules out a catalog parser-only issue and
  points to eMMC SDMA/addressing, partition offset, or on-device transfer
  contents. No USERDATA write was performed by the probe.
- The probe's original expected prefix was also corrected to the verified
  image bytes. Further reads should include the HFS volume header at byte
  offset1024 to distinguish an empty/offset partition from a catalog-only
  problem. Do not rewrite USERDATA until those reads and the driver address
  calculation are reconciled.

### 2026-11-14: BOOT0028 RAM-root catalog probe flashed

- A03CORE reappeared in Download mode. Verified BOOT0028 SHA, then Heimdall
  initialized, downloaded PIT (recoverable empty-bulk warning), uploaded
  only lowercase `boot` at100%, and reported `boot upload successful`.
  No USERDATA or protected partition write.
- `heimdall close-pc-screen --resume` completed reboot. Ten seconds later
  neither Download nor ADB USB was enumerated. No host console/catalog bytes
  are available yet; physical screen report is pending. BOOT0028 selects the
  validated RAM root (`rd=md0`) with eMMC enabled, so its PID1 probe can run
  independently of a USERDATA HFS mount.

### 2026-11-14: BOOT0029 corrected catalog comparison flashed

- CI root build `43613676224` includes the corrected actual catalog prefix
  `00000000000000000100000300000003`. BOOT0029 SHA256:
  `fffe78294bb3639f1db0fa1caf6420c0ec44649a160fea18f108a6ba00d900a6`.
- Heimdall downloaded PIT and uploaded only lowercase `boot` at100%, then
  `close-pc-screen --resume` completed reboot. USERDATA and protected
  partitions were untouched. Ten seconds later no Download/ADB interface was
  visible. Await display/PID1 output for the corrected catalog result.

### 2026-11-14: RAM-root XNU and PID1 confirmed

- User supplied `IMG_20261114_170949_912.jpg`. The display log shows
  `BSD root: md0`, HFS mounted `A03TestRoot`, BSD/devfs initialization, and
  `SWEET userspace: init running as PID 1` followed by repeated `still alive`.
  It also shows eMMC GPT result0 with CRC `bb4c2987/bb4c2987` and BOOT plus
  USERDATA BSD devices ready.
- This is the first confirmed XNU RAM-root and PID1 userspace run on A03. It
  is not an iOS root, launchd, SpringBoard, or USERDATA HFS mount result.
- BOOT0029 came from the default root workflow and did not include the
  explicit catalog probe input. Catalog-enabled workflow `43614257862` is
  dispatched for the next read-only BOOT test.

### 2026-11-14: catalog-enabled BOOT0030 prepared

- Workflow `43614257862` completed successfully with `catalog_probe=true`.
  The corrected RAM-root artifact SHA256 is
  `3b71db2687bfe6de8a3096157d973271de8f78e3817457aad05d8ad8595af519`.
- Packaged BOOT0030 with the verified kernel, A03 ADT and stock BOOT base;
  image SHA256 is
  `a4b545af50a80a5613c461e0e02404b784d489778af22d1a27bb66190c6d28fc`.
  It retains `rd=md0` and eMMC-enabled read-only catalog probing.
- The phone was not in Download mode after the PID1 photo, so BOOT0030 was
  not flashed. USERDATA remains untouched. Next hardware step is BOOT-only
  BOOT0030 transfer when Download mode returns.

### 2026-11-14: BOOT0030 catalog-enabled probe flashed

- A03CORE returned to Download mode. Heimdall downloaded PIT and uploaded
  only BOOT0030 to lowercase `boot` at100%, reporting `boot upload successful`.
  `close-pc-screen --resume` then completed reboot. USERDATA and all protected
  partitions were untouched.
- Eight seconds later no Download or ADB USB interface was visible. Await a
  display photo containing the catalog probe output; no iOS userspace claim
  is made from this reboot alone.

### 2026-11-14: BOOT0030 catalog probe still reads zero

- User reports `IMG_20261114_171705_276.jpg` shows the catalog still reads
  zero. This is consistent with BOOT0028's completed raw and block reads
  returning sixteen zero bytes instead of the verified image prefix. It does
  not establish the HFS volume-header contents or explain whether USERDATA
  was written at the expected byte offset.
- Added opt-in `A03_HEADER_TEST` to read512 bytes at USERDATA-relative offset
  1024 through raw and block nodes, print the first16 bytes, and check the HFSX
  `HX` signature. Local `clang` and `tools/mkinit.py` pass for header-only and
  combined catalog+header modes; `git diff --check` passes.
- This header probe has not yet run in CI or on the device. USERDATA and
  protected partitions remain unchanged. Next, reconcile partition-relative
  SDMA LBA translation and header bytes before considering another filesystem
  write. No HFS mount, Apple launchd, or SpringBoard result is established.
- Header/catalog root CI workflow `43615216691` passed. RAM-root image SHA256
  `b266c456151780842025a1e14137f5b416650d2feca71677dc34a13131f34893`.
  BOOT0031 uses existing kernel `43602657100`, the verified A03 ADT, and the
  known Magisk BOOT base; its SHA256 is
  `ea83109030122cc23a7055e85f828f6a93fa479cd3262307f4ca3029cf3bade3`.
  Cmdline retains `rd=md0 a03emmc=1`; both probes are read-only.
- Heimdall detected Download mode, downloaded PIT, uploaded only lowercase
  `boot` to100%, reported `boot upload successful`, and rebooted. USERDATA,
  GPT, recovery, bootloaders and EFS/NV were not written. No Download/ADB USB
  interface was present immediately after reboot. Await the device display
  for raw/block header bytes and catalog result; no HFS root or iOS userspace
  is established.
- User reports the subsequent verified Magisk BOOT-only restore booted into
  Android recovery rather than Android. Heimdall uploaded only `boot` at100%
  and rebooted. ADB briefly enumerated as unauthorized, then disappeared;
  there is no rooted Android shell to read USERDATA directly. Correction:
  the Magisk BOOT restore replaced the XNU shim, and no shim was flashed
  afterward; therefore this recovery boot is not evidence about XNU or an
  Android `/data` mount failure. Reflash BOOT0031 after returning to Download.
- User returned the A03 to Download mode for a diagnostic test. The retained
  CI image was decompressed outside the repository and verified at16GiB with
  SHA256 `eb72c14a9cf4aab30a8b49afda745a1b342dc877263d3b6a39901d95c89da108`.
  Direct image inspection confirms the HFSX header prefix at byte1024 and the
  expected catalog B-tree prefix `00000000000000000100000300000003` at
  USERDATA-relative byte `0x2cd82000`; `fsck.hfsplus -fn` reports the volume
  OK. The catalog offset is allocation block183682 *4096.
- Reflashed only USERDATA ID55 with that exact16GiB image. Heimdall downloaded
  PIT; phone displayed `SW REV CHECK FAIL : [userdata]` during transfer, then
  Heimdall reached100% and reported `userdata upload successful`. It rebooted
  the phone. There is no independent storage readback; the reflash does not
  prove catalog bytes on-device. GPT, BOOT, recovery, bootloaders, EFS and NV
  were not written in this operation.
- The phone then booted into recovery because the prior BOOT contents were
  the Magisk restore. XNU was not active. Current USB state is not Download
  mode. Return to Download, flash BOOT0031 only, and compare the read-only raw
  and block catalog bytes to distinguish an incomplete original USERDATA
  upload from a high-LBA XNU SDMA read fault.
- User returned the phone to Download mode. Reflashed the already-verified
  BOOT0031 image (`ea83109030122cc23a7055e85f828f6a93fa479cd3262307f4ca3029cf3bade3`)
  to lowercase `boot` only. Heimdall downloaded PIT, uploaded BOOT at100%,
  reported `boot upload successful`, and rebooted. No other partition was
  written. Download/ADB are absent immediately after reboot; awaiting the
  read-only raw/block catalog and header output. No iOS HFS mount or Apple
  userspace is established by the transfer.

### 2026-11-14: A03 XNU USB diagnostic path identified

- User requested USB access from XNU to replace photo transcription with
  direct logs/data. The live A03 device tree identifies a Spreadtrum
  `sprd,qogirl6-musb` peripheral controller at `0x64900000`, with the
  Qogirl6 HS PHY at `0x64570000` and AON APB registers at `0x64000000`.
  Linux's matching `musb_sprd.c` and `phy-sprd-qogirl6.c` confirm the role,
  clock gate (`APB_EB1` bit8), PHY reset, and analog initialization. Older
  SWEET DWC3/Qualcomm USB patches do not match this A03 hardware.
- Added opt-in XNU patch `0093-a03-usb-state-probe.patch`. It reads AON
  clock/reset/PHY state and, only when the MUSB clock is enabled, reads
  non-interrupt MUSB identity/state registers. It performs no register writes
  and avoids interrupt status registers that may clear on read. Boot arg
  `a03usb_probe=1` gates the probe; `a03-pack-root.py --usb-probe` adds it.
  The A03 profile stages it after the opt-in USERDATA root-selection patch.
- Validated patch application after A03 patches0090 and0092 against the local
  pinned XNU baseline; profile staging and Python syntax pass. This is only a
  safe state probe, not USB enumeration or a host data channel. XNU build and
  device validation remain pending. Next extend the MUSB endpoint0/device
  path and a simple host protocol so XNU can stream logs and sector reads.
- BOOT0031's post-USERDATA-reflash catalog result remains unknown. No new
  device write was performed for the USB work.

### 2026-11-14: post-reflash HFS header present, catalog still zero

- User reports the catalog still reads zero in both raw and block views. The
  raw HFS header begins `48580005800021004846534a00000081` (HFSX); the block
  view has the same HFS header, and SWEET PID 1 remains alive. This confirms
  the USERDATA HFSX volume header is readable through both XNU paths, while
  the catalog read at `0x2cd82000` still disagrees with the verified image.
- The report did not identify the exact BOOT image running, so it cannot yet
  be tied conclusively to BOOT0031 or the opt-in MUSB state probe. It does not
  establish an HFS mount or Apple userspace. No new device write was made.
- Linux source review confirms the MUSB peripheral cannot be assumed ready
  from the controller clock alone: Qogirl6 setup also powers/configures the
  analog PHY, supplies VBUS-valid, selects UTMI width and resets the core.
  Headers confirm the probe's AON offsets (`APB_EB1=0x4`, `RST1=0x10`, PHY
  registers `0x204`-`0x214`) and OTG clock bit8. The opt-in XNU build that
  includes the read-only MUSB state probe is workflow `43620198151`, still
  in progress at handoff. USB enumeration/log transport is not implemented.
- Host now detects Samsung Download USB (`04e8:685d`). `heimdall detect`
  succeeds and a fresh `heimdall print-pit --no-reboot` succeeds: live PIT
  reports SPRD8735, 60 entries, USERDATA ID55 at block15929344 with count0
  (dynamic remainder). The phone remains in Download mode; no flash or other
  device write was performed. This gives a ready BOOT-only test state once a
  validated image is packaged.

### 2026-11-14: BOOT0032 RAM-root storage probe deployed

- XNU workflow `43620198151` completed successfully. Kernel
  `kernel.development.sweet` SHA256:
  `1d2c74ac9de5266203e5068a2b402fe604ddc3666e92b63ee56a01bb0171bb26`.
- Packaged BOOT0032 from that kernel, verified 32MiB RAM HFS root SHA
  `b266c456151780842025a1e14137f5b416650d2feca71677dc34a13131f34893`,
  matching A03 eMMC ADT, and verified Magisk BOOT base. Image SHA256:
  `4ace15fb349f9c669f4a6bd51c5c7c84c25cb47f5ae0a1b05d37bfa65cdab287`.
  Cmdline enables `a03usb_probe=1 a03emmc=1` and keeps `rd=md0`; USERDATA
  writes remain disabled. The RAM-root PID1 runs catalog/header diagnostics.
  The USB argument was present, but the actual kernel did not link the probe
  (see correction below).
- Heimdall's first attempts failed before transfer during USB protocol setup.
  After Download-mode USB re-enumeration, Heimdall freshly initialized,
  downloaded PIT and uploaded only lowercase `boot` to100%, reporting
  `boot upload successful`. No USERDATA, GPT, recovery, bootloader, EFS or NV
  write occurred. `close-pc-screen --resume` completed reboot, exit0.
- Twelve seconds after reboot neither Download nor ADB USB was enumerated.
  This does not establish XNU USB enumeration. Physical BOOT0032 display and
  catalog/header output were pending at that time. A host-visible XNU USB data
  channel is still not implemented.
- User subsequently reports catalog raw/block still zero, both HFS header
  reads begin `48580005800021004846534a00000081`, and `SWEET init: still alive`.
  This matches successful RAM-root/PID1 execution with a readable HFSX
  volume header but catalog data disagreement. Host check after reboot still
  has no A03 Download or ADB device. User did not include the `A03 USB:`
  probe lines in this report, so controller clock/PHY state remains unknown.
- Correction: inspection of workflow `43620198151`'s actual build-tree
  artifact shows `bsd/dev/a03_usb.c`, the 0093 file-list entry, and the
  `IOKitBSDInit` call are all absent. Its kernel has no `A03 USB:` cstrings.
  The `a03_ios_userspace` input was false, so BOOT0032 did **not** contain the
  MUSB probe; the user's `A03 USB nowhere visible` is expected and cannot be
  used as controller-state evidence. BOOT0032's RAM-root storage diagnostics
  remain valid. Corrected workflow `43622283937` was dispatched from commit
  `8ad196a` with `a03_ios_userspace=true`, board `a03`, machine `SWEET`,
  DEVELOPMENT and macOS 13.5. It staged 0093, but completed with the patch
  silently skipped: its `bsd/dev/mem.c` context had one fewer tab than the
  target. The resulting artifact again lacks `bsd/dev/a03_usb.c`, the init
  call and `A03 USB:` strings. This was a false-positive build for the probe;
  BOOT0032 remained current until the later corrected BOOT0033 test below.
- Corrected 0093's context to match the target tab alignment. `git apply
  --check` now passes against the actual post-0092 source from workflow
  43622283937's build-tree artifact. Added a workflow post-build check that
  fails an A03 iOS-userspace build if its kernel lacks `A03 USB: AON`. XNU
  build `43623709272` completed successfully from commit `eb7dd77` with
  `a03_ios_userspace=true`; the gate passed. CI log confirms patch0093 applied,
  build-tree contains `xnu/bsd/dev/a03_usb.c`, and the kernel contains the
  `A03 USB: AON`, clock-gated, map-failed and MUSB-state strings. Kernel SHA256
  `8611e248a6b6ade4c95e9c77649d18b0d95cb8beba8a1cfc1e09263b37d9f006`.
- Packaged BOOT0033 using RAM root
  `b266c456151780842025a1e14137f5b416650d2feca71677dc34a13131f34893`,
  A03 eMMC ADT, verified Magisk BOOT base, and cmdline
  `rd=md0 a03usb_probe=1 a03emmc=1`. Image SHA256
  `48eb01ea5428c3e2eab9e5c69c4c7cedb9013d6ec9b6baf3b6612ab4862bf842`.
- Fresh Download detection and Heimdall protocol/PIT succeeded. Heimdall
  uploaded only lowercase `boot` to100% and reported `boot upload successful`,
  then rebooted. No USERDATA or protected partition was written. Twelve
  seconds later neither Download nor ADB was enumerated. BOOT0033's physical
  `A03 USB:` and catalog/header output are pending. USB state probe is linked;
  actual MUSB enumeration/log channel is still not implemented.
- User now confirms BOOT0033 repeats the storage result: raw and block catalog
  remain zero; raw and block HFS headers both begin
  `48580005800021004846534a00000081` and identify HFSX; SWEET PID1 remains
  alive. No `A03 USB:` lines were supplied, so the linked probe has not yet
  yielded physical register values. This is not an iOS root, launchd or
  SpringBoard boot.
- The verified local 16GiB image still contains catalog prefix
  `00000000000000000100000300000003` at relative `0x2cd82000`; the same
  offset is LBA `0x166c10` within USERDATA and absolute card LBA
  `0x1097c10` using the live GPT/PIT start. Both values fit the driver’s
  32-bit command argument. Next diagnostic should read adjacent known
  nonzero catalog sectors and print absolute/relative LBA, separating an
  on-device USERDATA transfer gap from a high-LBA SDMA/read-address fault.
- Added opt-in patch0094 (`a03emmc_trace=1`) to print successful reads at
  LBA >= `0x100000`, including absolute LBA and first four bytes. This will
  expose the exact command LBA used for the catalog read without enabling
  writes or changing controller timing. It applies cleanly to the corrected
  post-0092 source; profile and packer now expose the trace flag.
- XNU workflow `43625945895` was dispatched from commit `e130de1` with the
  A03/SWEET DEVELOPMENT profile and iOS-userspace patches, including0094;
  it completed successfully and its trace strings were verified in the
  kernel. Phone remained on BOOT0033 until the BOOT0034 flash below.
- Workflow `43625945895` completed successfully. Patch0094 is linked; the
  kernel contains `A03 eMMC TRACE` and `A03 USB: AON` strings. Kernel SHA256
  `8d4cdf854e6d887549a62010832e75bec8daa7467da06637714974089cd8f1df`.
- Packaged BOOT0034 with RAM root, catalog/header probes, MUSB state probe and
  `a03emmc_trace=1`; image SHA256
  `8f5f6fc40784bb80332dd8fc5fd0d68c73d6ed7a075e104a95d4b918443ec395`.
  Fresh Download/PIT succeeded and Heimdall uploaded only BOOT to100%, then
  rebooted. No USERDATA or protected partition write. Host had no Download or
  ADB enumeration 12 seconds later; physical trace lines are pending.
- Workflow `43627631857` completed successfully with patches0093-0096. Its
  kernel contains `A03 USB: probe entered` and `A03 eMMC UIO`; kernel SHA256
  `3a53e8216150a78584022c5a9cb2ab696241ff72292d83cee71175e7e2b09bad`.
  BOOT0035 SHA256 is
  `0956a223313ef84cd09744f7a0b20d135e9aa52518400576f986195c9594666d`.
  Heimdall uploaded BOOT0035 BOOT-only at100% and rebooted; no USERDATA or
  protected partition write. UIO and USB marker output are pending.
- The preceding BOOT0034 trace reported `CMD17 lba=f3101f resp=900
  data=00000000`, while the verified catalog should be absolute LBA
  `0x1097c10`. BOOT0035 adds an earlier `A03 eMMC UIO: off=... lba=...`
  print and an unconditional `A03 USB: probe entered` marker to identify
  whether the offset is lost before cdev I/O or whether the earlier trace was
  from the block path. BOOT0035 was uploaded BOOT-only and rebooted; output is
  pending. No USERDATA write.
- User reports a new eMMC trace: `cmd=17 lba=f3101f resp=900 data=00000000`.
  This is USERDATA base `0xf31000` plus `0x1f` sectors, hence byte offset
  `0x3e00`, while the tested catalog request is byte offset `0x2cd82000`
  (relative LBA `0x166c10`, expected absolute LBA `0x1097c10`). This trace
  alone does not prove where the offset changed; BOOT0035's UIO line is still
  needed to distinguish `pread`/specfs translation from the device handler.
- Inspection found `emmc_psize()` returned 512, although XNU block-device
  `d_psize` is the partition capacity in DEV_BSIZE sectors. Changed it to
  report validated BOOT/USERDATA sector counts, with INT_MAX saturation, and
  updated the A03 profile to stage patch0097 after the UIO trace patch. The
  host harness now checks each node's reported capacity; `python3
  tools/a03-test-bsd-storage.py` passes, including large buffered reads and
  raw UIO boundary cases. This is a plausible specfs geometry defect, not yet
  proven as the sole source of the observed 0x3e00 offset; retain the UIO
  trace in the next BOOT diagnostic. No device write was made.
- XNU workflow `43630138690` completed successfully from commit `c5768cb` on
  macOS 15 Intel. Kernel SHA256:
  `3801f139a203256b448d36cc43df369365cb3f1259570f2cb86a41d5d9fd84af`.
  Its strings include `A03 eMMC UIO`, `A03 eMMC TRACE`, and the USB probe
  marker. Packaged BOOT0036 as
  `shim/a03/out/a03-xnu-0036-psize-trace.img` using the validated A03 ADT,
  RAM HFS root, catalog/USB/high-LBA trace flags, and the existing Magisk BOOT
  base. Image SHA256:
  `34334f75b76dc5de4ce0256ce3d2ec49afba295f63c8b8870f1cefced3fb9256`.
  Candidate remains unflashed; no USERDATA or protected partition write.
- BOOT0036 was flashed BOOT-only with Heimdall after a successful Download-mode
  detection and PIT read. Upload reached 100% and reported `boot upload
  successful`; Heimdall rebooted the phone. No USERDATA, GPT, recovery,
  bootloader, EFS or NV partition was written. Fifteen seconds later the host
  had no Download or ADB enumeration; physical display and UIO/TRACE output
  are pending. This does not establish an XNU or iOS userspace result.
- User reports BOOT0036 still prints the HFS header successfully and produces
  many high-LBA eMMC trace lines whose payload bytes are `00`. This confirms
  the trace path executes, but the requested UIO offset/LBA line remains the
  needed discriminator. Inspection of the actual XNU `specfs` source shows
  `d_psize` is the device block size (`v_specsize`), so the experimental
  partition-capacity patch0097 was incorrect and has been removed; `512` is
  restored. The storage harness passes again with the original geometry.
- User reports the high-LBA trace is driving the other messages off-screen.
  Bounded the next diagnostic: patch0094 now emits at most 12 high-LBA trace
  lines, and patch0096 emits at most 12 UIO offset/LBA lines, including the
  initial low-offset requests. This keeps the HFS header, catalog result and
  decisive offset transition visible without changing storage behavior.
- XNU workflow `43631882575` completed successfully from `97cce65`; bounded
  trace kernel SHA256 is
  `d244b4b8e13a2c6df67e8eac6c2775613f580469de42cd55dbcae357a0d76d2e`.
  Packaged BOOT0037 with image SHA256
  `63ac4449549fe476b92ca74b4c4364632a2e2e46d66d003a6217921bb2a7dbb9`.
  Heimdall detected Download mode, read the PIT, uploaded only `boot` to
  100%, reported `boot upload successful`, and rebooted. No other partition
  was written. Host Download/ADB enumeration was absent after reboot; user
  output for the bounded UIO/TRACE lines is pending.
- Refined the next diagnostic after the trace flood: low-level output now
  covers only USERDATA base (`0xf31000`) and the expected catalog range around
  `0x1097c10`, with a 24-line cap. UIO output keeps the first four requests
  and any request in the catalog 64KiB window around byte offset
  `0x2cd82000`, also capped at 24. This directly tests whether the catalog
  offset reaches BSD/eMMC without scrolling unrelated HFS traffic away.
- OCR of `/home/stoned/ocr/IMG_20261114_203813_383.jpg` confirms that photo
  is BOOT0037's older broad trace: it shows `f31013` through `f3101f`, then a
  second `f3100a` sequence, and no `A03 eMMC UIO:` lines. It cannot evaluate
  the catalog-focused changes in `322bcba`; workflow `43633349828` is the
  first build containing those changes and has not yet been flashed.
- Workflow `43633349828` built commit `322bcba` successfully. Kernel SHA256:
  `9cf66f9624b94a8a7b0f5837027ab5fcf016c70111869f33b5231572d94f4c6f`.
  Packaged BOOT0038 with catalog-focused trace, image SHA256
  `875033bc9c0948421919ea0e8bc41b94fbff3d7903a11c075b49e52403f740c4`.
  Heimdall detected Download mode, read the PIT, uploaded only `boot` to
  100%, reported success, and rebooted. No other partition was written.
  Host Download/ADB enumeration is absent after reboot; the new screen photo
  should contain the catalog-window UIO/LBA evidence.
- OCR of `/home/stoned/ocr/IMG_20261114_205400_349.jpg` shows BOOT0038 did
  reach RAM-root PID1 and still reports raw/block catalog `MISMATCH`, while
  both HFS headers remain valid HFSX. The photo contains no catalog-window
  UIO/TRACE or direct-read result, so it cannot distinguish BSD offset loss
  from an on-card zero region. Added patch0098 to perform one kernel-side
  `CMD17` at verified absolute catalog LBA `0x1097c10` immediately after GPT
  validation and print its first 16 bytes. This bypasses specfs, uio and HFS;
  its single line is the next required discriminator. No device write.
- XNU workflow `43639229337` built commit `917e2f3` successfully. The final
  kernel SHA256 is
  `285850a93c11e4fd991289861b6d1333b7b5e339982bd7d84ab2b754734eccf7`;
  workflow gates passed and kernel strings contain exactly the expected
  `A03 CATALOG direct`, `A03 eMMC UIO`, and `A03 eMMC TRACE` diagnostics.
  Packaged BOOT0039 with RAM HFS root and read-only storage diagnostics;
  image SHA256
  `4588ae7fa46e8b9a445bc42e0a7063ff91a3988868a6f9631d3b746da9133b97`.
  Download mode/PIT succeeded and Heimdall uploaded only `boot` to 100%,
  reported success, then rebooted. No USERDATA or protected partition write.
  After reboot there is no host Download/ADB enumeration and no newer photo
  in `/home/stoned/ocr`; direct catalog bytes remain unobserved.

## 2026-11-15: BOOT0041 corrected provider and ADT

Workflow `43651725931` succeeded from commit `cd137a8`; link gates confirmed
the A03 USB probe, direct catalog diagnostic, and USERDATA-root panic guard
are present in the kernel. Kernel SHA256 is
`a3d8125d0a49290116a4ba1e3d7e1fe2d98276f5be4cf6f8df5f3840b356091d`.
BOOT0041 image SHA256 is
`428deca6e75ccccf1a38b0deada5ae152d756b045effe2ac1da05dcc55b67c35`.
It was flashed only to `boot`, reached 100% and rebooted. USERDATA, GPT,
recovery, bootloaders, EFS and NV were untouched. Runtime iOS progress is
not yet observed.

### Linux reader5 proves PID1; reader7 mailbox deployed

Reader0004 BOOT-only upload100%/reboot succeeded; user saw only Samsung logo.
Reader0005 SHA92c057c4175682495ffa28f21dc2165bdac22b0a7e59eabe80cdfaa0e4030410
also uploaded BOOT-only. Its explicit Linux reboot(RESTART2,download) after
observation fired: user reported spontaneous return to Download; host confirmed
04e8:685d at10:36UTC. This establishes custom Linux init execution, independent
of XNU, not Apple launchd. Reader0006 adds DRM/KMS dumb-buffer output using
queried connector/CRTC/mode; flashed BOOT-only, user still saw no text.

Reader0007 SHA4d9b83a1bd1a849727fba2908644fbc379c0ef628653745f2ccb8ab6ef2545b9
flashed BOOT-only/upload100%/reboot at~10:40UTC. It saves a4096-byte report
at USERDATA-relative16GiB only after GPT CRC/identity validation; this is an
intentional authorized USERDATA write beyond the16GiB HFS root. USB remains
read-only. Actual mailbox write success is not yet proven. It returns to
Download after observation; next flash shim/a03/out/a03-linux-report-0001.img
SHA37030f0f68def716322a8f5e042b02b22a11dea72432467bb0e28741ad8eb412
BOOT-only to display magic/CRC-checked report through pre-Linux framebuffer.
Snapshot6 halts before XNU and reads only the bounded validated mailbox.
Host reader0008 adds explicit mailbox capacity guard; unflashed SHA
46149eb8297f255926dcc29f8a006956ace65f6f1c9b26677e703698fcb83750.
Host compilation, GPT and BSD harnesses pass. No protected partition write.


### Linux report viewer deployed, 10:43UTC

Reader7 returned to Download; host confirmed04e8:685d. Flashed report viewer
shim/a03/out/a03-linux-report-0001.img BOOT-only; upload100%/success/reboot.
No new USERDATA write by viewer. It halts before XNU, awaiting physical
A03 STOCK LINUX REPORT text or the mailbox/GPT failure line. Current BOOT is
the report viewer. Commits d9ff094 and c381f54 contain reader and mailbox work.
Reader0008 remains unflashed. Host sees no USB on viewer by design.


## 2026-11-15 10:46UTC: independent Linux confirms installed catalog zeros

User read the CRC-verified Linux mailbox viewer: GPT CRC=bb4c2987,
USERDATA start15929344, CATALOG_HEADER at relative0x2cd82000 first32 all zero.
This agrees with XNU direct CMD17 and isolates the catalog failure to installed
USERDATA contents rather than the XNU BSD/HFS path. Reported sector count was
transcribed10621336; do not adopt that as authoritative geometry without
reading full report (existing test fixture106213336). Full host rebuilt-image
16GiB SHA256 reverified eb72c14a9cf4aab30a8b49afda745a1b342dc877263d3b6a39901d95c89da108.

User supplied remaining report error: link mass storage: No such file or
directory. Stock Linux fs/configfs/symlink.c get_target uses kern_path on
symlink argument before link creation, resolving relative paths from process
cwd rather than the link parent. Replaced relative target with absolute
/config/usb_gadget/a03/functions/mass_storage.0. Reader0009 host build PASS,
SHA8891c2434ab430f321ec9e49ec1bcb422561bc2deaf177fba267c745235dd2d3.
Await Download mode for BOOT-only test. USB export remains read-only;
existing4096-byte USERDATA mailbox behavior unchanged. No launchd yet.


### USB storage transport works; independent catalog verification

Fixed absolute configfs symlink, built/flashed reader0010 BOOT-only
SHAa2d3439e754ff3f422c6c6c083afbd3b0d800779d703bc7c640a9d15934d7dac.
USB1d6b:0104 enumerated; host LUN0=1MiB RAM report, LUN1=54381228032-byte
USERDATA, both read-only, serialA03LinuxReaderV9. User granted host read ACL
only to /dev/sdb and /dev/sdc. Direct host reads of RAM report and USERDATA
confirm GPT CRCbb4c2987, start15929344, sectors106213336, valid HFSX header
and all-zero32-byte catalog header/root at0x2cd82000/0x2cfa6000. This proves
installed image contents, not XNU read translation, block HFS/launchd.

Added explicit --userdata-writable build profile: only GPT-validated p55 LUN
becomes writable, no whole card exported, RAM report remains read-only.
Installer0011 SHA7acfc1f50d01b86a760408f8fa748618429a07cdb8eeeecf64cb96e54986ccdb.
Added tools/a03-install-usb-root.py with exact USB identity/LUN/capacity,
mount/target guards, pinned16GiB source hash, full write/fsync/O_DIRECT
readback SHA256. Direct hash routine checked on host; regular target refused.
User returned phone to Download for authorized root install. Install actual
write remains pending; do not claim USERDATA repaired until full readback.


### 10:54UTC: verified USB USERDATA root install started

Installer0011 BOOT-only upload100%/reboot succeeded. Host enumerates LUN0RO,
LUN1RW with expected serialA03LinuxInstallV11 and54381228032-byte capacity.
User granted targeted host read/write ACL. Guarded installer process
session63894 verified pinned source SHA and identity, then began16GiB write.
Live catalog header/root bytes now match source after those offsets were
written; full install/fsync/O_DIRECT hash still pending. Do not reboot or
flash while this process remains active.

User requested visible working status in USB mode. Found DRM GETRESOURCES
and GETCONNECTOR second queries retained nonzero framebuffer/encoder/property
counts but supplied NULL arrays; fixed all bounded output arrays, prefer DRM
over unavailable/inactive FB0, retain failure stage in diagnostic report.
Added status heading plus live UDC state, read/written MiB counters and uptime.
Builds with -Wall -Wextra -Werror pass. New UNFLASHED RO status0014 SHA
 eb3266449946ec0719cd14b242aefcaf983b90141db943c43fc83d2a20c386bd
and RW status0014 SHA
8826ce374112caef531593a887e459efea243c9c5f038a143f6ea17d5c4547ae.
On-screen result still requires device verification; current install continues
on0011. Host fsck.hfsplus -fn of rebuilt source reports A03iOSRoot OK.


Status follow-up0015 adds page-flip commit after redraw for command-mode
panels. Host build PASS, unflashed RO SHA
12915ef3306eb148f93e789f06bc3dd97c6c647dbba98a2850301efed5c5ad4f,
RW SHAe4039f111fbe8cfbd0591272f78a593aab7abd0724d769e3746069347eac2c0d.
Current installer remains0011 while16GiB transfer is active; no interruption.


11:03UTC: installer completed exactly16384MiB writes in551.6seconds and
entered full O_DIRECT readback. Same live process63894; verification pending.
No reboot/BOOT flash until process terminates with matching hash.


## 2026-11-15 11:13UTC: full USERDATA root install independently verified

Guarded installer session63894 exited0 after16384MiB writes, fsync and full
O_DIRECT readback. Device SHA256 equals pinned source:
eb72c14a9cf4aab30a8b49afda745a1b342dc877263d3b6a39901d95c89da108.
Readback catalog header first32:
00000000000000000100000300000003000001120009196c0000248d00000001;
root node274 first32:
0000000000000000000300400000001a00000001000a0041003000330069004f.
Exactly16GiB written through GPT-validated p55-only USB LUN, no whole-card
export, protected partitions unchanged. Source fsck read-only PASS. This is
now full installed-byte proof, not merely Heimdall transport success.

Current BOOT remains installer0011; no Apple launchd result yet. Next user
returns Download for BOOT-only RO status0015 display test, then XNU0042 boot
with repaired root. Never rerun installer just because physical output is
missing; image is fully verified. Status0015 on-screen behavior unproven.


11:14UTC: user returned Download after completed/verified install. RO
status0015 flashed BOOT-only/upload100%/success/reboot. USB1d6b:0104
re-enumerated. Await physical status-heading/counter confirmation; full root
remains verified. No HFS root mount/launchd retest yet.


USB status display VERIFIED: user reports visible read2MiB/written0MiB on
status0015. These are current-boot block counters, not total historical install
bytes; installer0011 previously completed/passed full16GiB readback. This
fulfills visible USB working-status request. Next XNU0042 BOOT-only trial on
verified root; user asked to return Download. No launchd runtime yet.


## 2026-11-15 11:16UTC: XNU0042 retry after verified root repair

User confirmed RO status0015 catalog was no longer zero, then returned to
Download. Heimdall detected, protocol/PIT passed, uploaded only BOOT0042
(6c729a41d931fd2d151d42aaccf005b57d972206d410fbce7cb46da3a42c6115)
to100%/success and rebooted. USERDATA not reflashed by this operation; full
root remains previously verified. Await new HFS/launchd screen evidence.
Known0042 second-root diagnostic LBA is obsolete/wrong; catalog-header direct
read valid. No Apple launchd runtime claim until current boot output proves it.


## 2026-11-15: verified root reaches root-vnode authentication

User reports XNU0042 panic(cpu 0 caller 0xfffffe0007acec5c):
rootvp not authenticated after mounting @bsd_init.c:946. Source places this
after successful vfs_mountroot, VFS_ROOT, and rootvnode installation. Thus
the repaired USERDATA HFS root now mounts; Apple launchd has not run yet.
The A03 minimal profile omitted donor0029 unsealed-root support. Added
0099 with explicit a03_unsealed_root=1 and exact validated writable USERDATA
rootdev guard; other roots retain the original authentication panic. Packer
sets the opt-in only with --userdata-root. CI checks its linked marker.
No filesystem reinstall is indicated. BOOT0042 remains current pending build.

Host validation:0099 applies cleanly to extracted CI bsd_init.c; actual added
C guard compiled in both board configurations and passed96 cases (auth result,
opt-in presence/value, provider validity and rootdev mismatch). Existing GPT
and BSD storage harnesses PASS. Commitd447b11 pushed; kernel CI43708471929
queued on macos-15-intel with A03 iOS userspace profile. No new BOOT write yet.

Offline-equivalent profile staging also PASS (45 patches):0099 present with
exact source bytes and0098 corrected root LBA0x1098d30. Host independently
detects Samsung Download USB and Heimdall confirms Device detected. CI is
restoring dependencies before compilation. Current BOOT remains0042.


## 2026-11-15 11:48UTC: scoped unsealed-root XNU0043 flashed

CI43708471929 success at d447b1198a4a0c45ec18006835a04f0f302bf1a6.
Plain arm64 kernel SHA256:
00c7cd3a5653d533e12d79d531fb68d201d9052ef9527f18ab22089a6b845018.
Linked scoped unsealed-root diagnostic verified. Packaged with same0042
ADT/boot arguments plus a03_unsealed_root=1, no RAM disk or root rewrite.
BOOT0043 SHA256:
edb76b9dcd3804c4e3f359ca7eafbf1b0260a7c16a9143c88f67e27ff2101e7e.
Heimdall protocol/PIT successful; uploaded only boot to100%, reported boot
upload successful, rebooted. GPT/recovery/bootloaders/EFS/NV untouched.
Await physical screen result after unsealed-root line; actual Apple launchd
execution is still unproven. Full16GiB root remains independently verified.


## 2026-11-15: BOOT0043 passes mount; iOS exec platform gate rejects launchd

User reports panic(cpu 0 caller 0xfffffe0007ad5a20): unexpected SIGKILL of
launchd (CS_KILLED), namespace9 code0xe, description none. In exact extracted
XNU source reason.h namespace9=OS_REASON_EXEC,14=WRONG_PLATFORM. process_signature
in kern_exec.c rejects PLATFORM_IOS exec with no spawn attributes unless
no-sandbox entitlement or DEVELOPMENT unentitled_ios_sim_launch is enabled.
This is not invalid-page signature failure (namespace3/code2), and the process
name does not prove launchd instructions ran. Root mount/auth override advanced.
Existing DEVELOPMENT tunable unentitled_ios_sim_launch=1 permits this path;
package same verified kernel with that flag and launchdsuffix=release. Packer
adds these only with --userdata-root. No filesystem reinstall/rebuild needed.

BOOT0044 packaged, UNFLASHED:
shim/a03/out/a03-xnu-0044.img SHA256
2f2dc75f240c7f0729e02d9d6eb79087050ff600fdefe4855cddde229b7f3131.
Compared entire0044 vs0043 payload: identical outside608-byte cmdline field.
Compiled kernel contains unentitled_ios_sim_launch tunable and allowing-spawn
path; source confirms DEVELOPMENT enables it. Flags select /sbin/launchd and
existing validated USERDATA. Await user Download transition; no USB visible
at final host check, no new device write since0043. Actual launchd instruction
execution remains unproven until next boot output.


## 2026-11-15 11:53UTC: BOOT0044 iOS exec-option trial flashed

User returned Download; independently detected with Heimdall. Reverified
BOOT0044 SHA2562f2dc75f240c7f0729e02d9d6eb79087050ff600fdefe4855cddde229b7f3131.
Protocol/PIT successful; only boot uploaded to100%, boot upload successful,
rebooted. Same CI43708471929 kernel, adds existing DEVELOPMENT tunable
unentitled_ios_sim_launch=1 and launchdsuffix=release. Root not reinstalled;
GPT/recovery/bootloaders/EFS/NV untouched. Await screen result for iOS exec,
dyld or next panic. Launchd user-instruction execution remains unproven.


## 2026-11-15: BOOT0044 reaches dyld, SIGTRAP; XNU font correction

User observed shared_region mapping requests from pid1(launchd), including
not-in-trust-cache warnings, followed by namespace2/code5 exit and writing
core to /cores/core.1. This proves userspace dyld activity in the launchd task,
not sustained Apple launchd main execution. Namespace2=SIGNAL,5=SIGTRAP.
Source vm_unix.c falls back to root ownership on missing trust cache; warning
alone is not mapping-failure evidence. User let dump finish then Download.
Flashed RO USB status0015 BOOT-only100%/success/reboot. Validated USERDATA
USB connected with host read permission already available. Read-only catalog
inspection: /cores exists but is EMPTY; /cores/core.1 is absent, likewise no
launchd log file. Cannot claim core recovery; dump completion text unknown.
Added tools/a03-read-usb-hfs.py with exact reader USB identity/LUN1/RO/capacity
checks, source O_RDONLY and local image mode. Parser portion reused without
any donor device path. Offline launchd stat and on-device directory reads pass.

User clarified font request applies to XNU, not USB. Found pinned donor0003
has FBCON_SCALE2 while local donor patch already has1; A03 pulls pinned donor,
so local patch was not used. A03 profile now transforms pinned2 to1, yielding
8x16 cells /90columns x100rows at720x1600 instead of16x32 /45x50. USB untouched.
New font is source-only until next kernel build and BOOT test.

XNU font build CI43711774561 started from a92aa205a02b28f38a03e8247eba22c1a87faa99,
A03 iOS userspace profile / DEVELOPMENT / SWEET / macos-15-intel. Staged0003
verified FBCON_SCALE1. At720x1600 this is90columns x100rows (four times old
character capacity). Current device stays in RO USB status0015 until build
passes and user returns Download. No new XNU flash yet.


## 2026-11-15: live dyld/cache audit and pre-coredump trap logging

Read-only USB audit validates all40 declared subcache files, UUIDs, mapping
bounds, symbol UUID and2663 image paths. Live launchd SHA314a84ce...bb5f666
and dyld SHAe5768eb0...691873 match pinned rebuilt root bytes. This checks
inventory/selected file bytes, not every cache payload hash or runtime success.
Private extracted binaries/reports remain in ignored out/launchd-trap-audit.
Disassembly identifies dyld_halt BRK at image offset0x5fcd0 with formatted
message retained in x19, plus other pthread/libplatform BRK sites. SIGTRAP
alone cannot distinguish them. Added0100 to print actual PC/LR/SP/FP, main
and dyld bases, cache slide, instruction, bounded x19 string and6 bounded
frames before initproc core dump, which left no catalog file last time.
Source reads user memory with copyin/copyinstr only; kern_exit receives
-mgeneral-regs-only. No trust-cache bypass or iOS binary edits. Includes
small-font change in same next kernel build. Runtime trap location pending.

Combined smaller-font + SIGTRAP capture CI43712255840 dispatched at3580c5b,
DEVELOPMENT/A03 iOS userspace, buildtree upload enabled for compile auditing.
It supersedes font-only CI43711774561 via existing workflow concurrency.
0100 dry-run applies with zero fuzz to extracted CI sources. Device remains
RO USB status0015; no new XNU candidate flashed. Await build/runtime evidence.


ReVa MCP now used on exact live dyld/launchd binaries; both imported/analyzed
and saved locally without version control. ReVa confirms _dyld_halt BRK0x5fcd0
versus dyld4::halt abort_with_payload namespace6, and pthread thread_selfid
assertion BRK0x147a8. launchd main entry0x100014038 includes early wake-monitor
assertion, another possible trap. None identifies actual runtime PC yet.
Documented reproducible candidates/limits in docs/a03-launchd-trap-analysis.md.
No Apple binary edits. Combined diagnostic CI43712255840 still building.


## 2026-11-15: fix SIGTRAP diagnostic compile failure

CI43712255840 failed compiling kern_exit.c: incomplete struct task at task
image-info/main-header fields and incomplete struct vm_shared_region at slide.
BSD headers expose opaque types; original diagnostic placement was incorrect.
Moved full helper into osfmk/kern/exception.c (MACH_KERNEL_PRIVATE), leaving
BSD only a proc/current-thread/SIGTRAP guard and scalar-pid call. Per-object
-mgeneral-regs-only now applies to exception.o. No diagnostic removed, no
opaque-layout casts. Smaller font remains. Downloaded exact failed buildtree
and recovered982 compile commands; local Clang syntax checks of modified
bsd/kern/kern_exit.c and osfmk/kern/exception.c both PASS using actual component
flags/headers. Patch applies with zero fuzz. Full CI/link/runtime still needed.
Current phone BOOT remains RO Linux USB status0015; no device write for fix.

Corrected CI43714631683 queued from714d2da7a4a4fc37fe1ae45c1a85476572d037da,
DEVELOPMENT/A03 iOS userspace/macOS15 Intel. Includes1x XNU font and full
pre-coredump trap helper. No new kernel success or hardware result yet.


## 2026-11-15 12:55UTC: smaller-font SIGTRAP diagnostic BOOT0045 deployed

Corrected CI43714631683 PASS at714d2da. Kernel SHA256:
80cdfc510fb2236ee37fa4198cf88b8b1761335c8c9d76a13ffd0f0994fc2653.
Linked A03 TRAP pid/x19 markers verified. Packaged with0044 args, same
emmc ADT, no RAM root; BOOT0045 SHA256:
a348ba5b5915058f3fcba5be7a03881cd2082da2757263f3c47aad37c24ad5a0.
User confirmed Download; independent Heimdall detection/protocol/PIT pass.
Only boot uploaded100%, boot upload successful and rebooted. No root reinstall
or GPT/recovery/bootloader/EFS/NV write. Await actual smaller-font confirmation
and A03 TRAP PC/dyld/x19 diagnostic; launchd main execution remains unproven.

## 2026-11-15: BOOT0045 SIGTRAP identified in cached libpthread

User reports pid1 PC=0x1e6f71f5c, LR=0x1e6f6841c,
SP=0x16b31ab30, FP=0x16b31ac00, main=0x104ae4000,
dyld=0x104c30000, cache_slide=0x19274000, x19=0x16b31bde8,
instruction=0xd4200020. Subtracting the measured cache slide gives
PC=0x1cdcfdf5c and LR=0x1cdcf441c in libsystem_pthread.
The pinned cache .23 has BRK #1 at that exact PC, following storage of
"BUG IN LIBPTHREAD: host_info() failed" and the error value in crash info.
ReVa analysis of a private TEXT-only extraction (295 functions) resolves
the caller to initialization at0x1cdcf4050: host_info(host,5,buffer,&count),
count initially8, failure branches at0x1cdcf40f4 to0x1cdcf4418.
Flavor5 is HOST_PRIORITY_INFO; XNU's structure is eight integer_t fields.
This identifies the assertion but not yet why host_info returns failure.
TEXT-only import omits DATA/LINKEDIT; external call names need separate
verification. No new flash/root write; launchd main remains unproven.

Added0101 diagnostics: trap x0/x8 (the assertion preserves its error in x8),
x20/x21/x22 (x22 holds host port in this initializer), msg2 request options,
host_info request host validity/count, MIG request/reply status/size.
No return values or security checks changed. Four affected source files pass
local syntax checks using recovered CI commands (environment/header warnings
remain). Full CI/link/runtime validation pending. Physical Download absent.
Direct cached branch stubs also resolve to libsystem_kernel host_info at
0x1bf1361a4, message ID200, and host-self target0x1bf1307f8.

Diagnostic CI43717108507 started frome0e58a2. Await link result, then
package BOOT0046 with0045 args; user asked to prepare Download after dump.

## 2026-11-15: BOOT0046 host-info diagnostic deployed

CI43717108507 PASS frome0e58a2f1ec89c07f44bc421947829571e82170b.
Kernel SHA25661b680debd48d1a3439f1b7eb6f6e876b4b2690b7210dfacba6ff968ea4bce7e;
all five expected diagnostic markers present. Exact four-file patch reverse/
forward roundtrip passes with zero fuzz. Packaged with same0044/0045 args,
ADT and verified Magisk base, no RAM root. BOOT0046 SHA256:
a813167e3fc63556108e8dfa7cb55c2100994790701b2fdb8308aeff6994f205.
Heimdall detected Download; boot upload100%, success and reboot. Only BOOT
was flashed; full verified USERDATA root preserved. Retains1x XNU font.
User asked for A03 HOST request/reply and A03 TRAP x0/x8/x22 values.
No new physical runtime result yet; launchd main remains unproven.

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

## 2026-11-15: USB console mirror implemented for next BOOT test

User requests simultaneous XNU screen+USB logs. Added opt-in0103 CDC ACM
full-speed PIO peripheral and256KiB serial spool, guarded capture tool and
protocol test. Register setup grounded in matching A03 Linux Qogirl6 PHY/
MUSB sources. Screen remains, no storage operation. IRQ-masked single-core
spool; polling kernel thread; no USB DMA. PMIC state preserved. Descriptor/
control-request harness PASS; exact patch zero-fuzz roundtrip PASS; three
local component compiles PASS, general-register driver/spool. Enumeration/
transport UNPROVEN. docs/a03-usb-console.md records limits/reproduction.
Retain0102 reply-right diagnostics; no IPC validation bypass.

Combined USB/reply-right CI43719832882 queued from5694793; supersedes
43719778245 and43719205319 (cancelled by newer dispatch). Added bounded
10s enumeration wait +1s drain before initproc, so early host failure can
be captured. Updated patch roundtrip + final driver compile + protocol PASS.
Download mode detected. Next download successful kernel, package0047 with
 a03usb_console=1, start host tty capture, then BOOT-only flash/test.

## 2026-11-15: opt-in post-trap USB inspection monitor

User requests ability to investigate userspace after launchd crashes.0104
adds a03debug_hold=1: current initproc SIGTRAP exit pauses before coredump/
panic, sleeping between commands to keep USB worker/scheduler alive. Dying
thread executes copyin against its own still-live task map. Commands help,
regs,bt,mem HEX [HEXCOUNT<=100],panic (continue normal fatal exit). No shell,
resume, task execution, memory writes or launchd restart claim. USB OUT line
queue and host capture interactive/command support added. Local three-file
compile PASS; parser/queue harness PASS; exact patch zero-fuzz roundtrip PASS.
USB hardware remains unproven. Combine0102/0103/0104 for next0047 candidate.

Monitor-inclusive CI43720286686 at94edf70 queued/pending. Supersedes USB-only
43719832882. Download detected. Next successful kernel=>BOOT0047 with
 a03usb_console=1 a03debug_hold=1, then host capture and BOOT-only trial.

## 2026-11-15: rejected incomplete CI artifact; fixed USB patch context

CI43720286686 reports success but artifact marker audit disproves USB/monitor
inclusion. Build log explicitly skips0103 (BSD Makefile context included
local-only kern_exit CFLAGS) then0104 (missing USB source). Kernel32a1bc73...
is NOT a USB/monitor candidate. No flash occurred. A malformed no-args host
packaging attempt made only private files; discarded both never-flashed
0047 image/payload. Corrected0103 against exact downloaded CI source; BOTH
0103/0104 now pass git apply --check and application in sequence. Added CI
required string checks for reply diagnostics, USB console and hold monitor,
so skipped requested features cause failure. Next corrected full build.

Corrected CI43722354348 started at8d25855, includes required feature gates.

## 2026-11-15: corrected BOOT0047 USB/monitor trial deployed

CI43722354348 PASS at8d25855. Independent artifact SHA/feature-marker check
PASS: kernele4b5d6cf1caa027476f41d8bf2a3231647053c5ce19ceb906f32f10d1c103752.
BOOT0047 SHAb6b3e90bf5cbeb1a8770d6ce7d41ba184e00d9d813fe04402c394c874e68b8bb.
Same0046 args+ a03usb_console=1 a03debug_hold=1, no RAM root. Started host
capture session91167 before BOOT-only Heimdall upload100%/success/reboot.
No USERDATA/GPT/protected-partition write. Await enumeration/screen evidence;
no USB or monitor hardware success established yet. Root remains verified.

## 2026-11-15: BOOT0047 identifies provisional/strict reply mismatch

User reports CDC startup marker and PID1 signal exit2/5. Host capture waited
100 seconds without enumeration; startup alone is not USB transport proof.
Physical IPC trace: construct flags=4000 rv=0 name=603; invalid name=603
type=21 entry=1 bits=38200000 semantics=3 dest_semantics=4. Receive right
exists and MAKE_SEND_ONCE is correct. Provisional reply semantics3 conflict
with kernel-object strict semantics4. Exact ipc_right_copyin_check_reply
rejects this through __ip_strict_reply_port_semantics_violation for a
platform binary; no MIG host_info handler runs. This explains error10000009
and cached libpthread assertion. Investigating narrow iOS16 compatibility
policy; do not force host_info success or change reply right ownership.
Monitor hold is still physically unconfirmed. Verified root preserved.

Candidate0105 scopes provisional reply compatibility to opt-in boot arg,
PLATFORM_IOS2/SDK major16 and actual provisional reply ports. Original
receive-right/disposition/MIG checks retained. launchd Mach-O SDK16 verified.
Candidate0106 mirrors matching A03 Linux peripheral PHY pulldowns/reserved
bits and board-specific eye trim04b3d1c0; adds PHY/core readbacks and reset/
setup counts. No PMIC writes. Three changed consumers cross-compile PASS;
exact-source sequential apply PASS; CDC/parser and192-case predicate PASS.
Next full CI, BOOT0048 +a03_ios16_provisional_reply=1; hardware unproven.

Full build CI43724877490 started fromf8ecc37; Download mode detected.
No0048 flash yet.

Additional host audit: deployed0047 _proc_prepareexit disassembly branches
to _a03_init_trap_log then _a03_init_debug_hold before coredump. Both symbols
are linked; hardware hold still unconfirmed. Cumulative0103+0104+0106 CDC
protocol/command test PASS, all four IPC/USB source consumers compile PASS.
Build43724877490 remains running; Download detected. Root untouched.

## 2026-11-15: BOOT0048 reply compatibility + PHY trial deployed

CI43724877490 SUCCESS fromf8ecc3747c33fd5046ead5465519d9452c8f7fd9.
Kernel SHAf7f873bef453343675a53ac829f69b555c0797b732f739cc77cdbfb1bc50f5b4.
Required markers independently checked; linked strict predicate disassembly
calls proc_sdk/proc_platform and checks IOS2/SDK16 before the exception.
BOOT0048 SHAe9f8ee1df066a7b9e4fd0db131f8a4c11df5b70215eafad5fa8daf60fd6c6626.
Uses0047 args plus a03_ios16_provisional_reply=1. Host capture45847 started
before Heimdall BOOT-only upload100%/success/reboot. USERDATA/root/GPT and
protected partitions untouched. Await physical logs and USB enumeration;
no runtime host_info/launchd improvement or USB success claimed yet.

BOOT0048 capture45847 completed with120-second enumeration timeout:
A03 XNU CDC console did not enumerate. Host kernel journal shows only
Download disconnect, no subsequent USB attach. Await physical PHY/CORE and
IPC/launchd output before further code changes; not evidence about host_info.

## 2026-11-15: BOOT0048 deployed-source audit

Previous goal turn made progress: scoped reply compatibility implemented,
full CI passed and BOOT0048 flashed; runtime outcome remains unverified.
Downloaded exact CI43724877490 buildtree. ipc_port.c, ipc_port.h and
bsd/dev/a03_usb_console.c byte-match the locally tested sources; actual
kern_exit.c contains the debug-hold call. This rules out skipped/stale patches
for these changes. Physical screen report is pending; no USB endpoint and
no Download device currently visible. Do not infer whether host_info passed
or flash a further trial without new device evidence. Additional read-only
Linux audit identifies USB muxAON+374 and vendor OTG_EXT_CSR+34b as potential
readback points; no observed wrong values or justified new MMIO writes.

## 2026-11-15: BOOT0048 reaches launchd boot tasks; missing bindfs

User reports userspace panic: boot task failure: mount-phase-1, exit74;
preceding error failed to mount /usr/standalone/firmware, Operation not
supported by device(19). This is launchd boot-task execution beyond the
libpthread host_info assertion, not sustained successful boot. Exact0048
kernel nm has nullfs_vfsops but NO bindfs_vfsops. A03 iOS profile omitted
portable donor0037; matching prior donor evidence reports the same bindfs
ENODEV/exit74 failure. Enable actual bindfs VFS, not suppress mount failure.
0037 exact deployed config apply PASS; add required linked-symbol CI gate.
Root stays installed; only new kernel BOOT needed. USB remains unproven.

CI43727113402 started fromfb777a0; portable bindfs profile staging PASS.

ReVa confirms exact mounted-root /sbin/mount0x100006544 calls bindfs; errno19
is not the tolerated optional ENOENT case and reaches errx via sysexit_np.
Code signature contains bindfs-allow entitlement=true; retain that check.
Private mount binary remains ignored. This narrows fix to config, not root.

All three bindfs source files cross-compile against the recovered XNU CI
headers/flags: bind_subr.c, bind_vfsops.c, bind_vnops.c PASS. Full new config
link/registration remains for CI and phone validation. Bring-up guide's
current-status introduction updated to distinguish observed boot tasks from
sustained launchd or GUI success. No new device write.

User confirms Download mode ready for0049; host detection agrees. Candidate
retains0048 cmdline exactly. Apple's own arm64/iPhoneOS config includes
bindfs, and vfs_conf.c registers the real filesystem when BINDFS is enabled.
CI43727113402 remains in Build; no0049 flash yet.

## 2026-11-15: BOOT0049 bindfs trial deployed

CI43727113402 SUCCESS fromfb777a08b1fa2a95de423a5682e4a6964f319359.
Kernel SHA7cc96acf62d08ed10177a4f78fd1cce6a0a681f5f37600575d343066890651cb.
Independent nm confirms bindfs_mount and bindfs_vfsops. Retained reply/USB/
monitor strings and bindfs entitlement-check string verified. Cmdline is
byte-identical0048. BOOT0049 SHAd93f2325738e1a971bb12d2f4e6d592665967e8898b3f2e194981b2e0aad1c18.
Capture63535 started before Heimdall BOOT-only upload100%/success/reboot.
No root reinstall or host USERDATA/GPT/protected-partition write. Await
physical mount-phase progression or next boot-task failure; no sustained
launchd/bootstrap completion claim yet. USB remains hardware-unproven.

BOOT0049 host capture ended100s timeout without enumeration; host journal
only records Download disconnect. Await user screen report; USB startup
cannot yet replace physical transcription. No further trial justified until
mount task outcome is observed.

## 2026-11-15: BOOT0049 reaches keybag initialization

User reports FATAL KEYBAG ERROR: failed to load system bag, plus missing
options device-tree entry. This advances past mount-phase firmware failure;
not sustained bootstrap success. Exact0049 nm has no AppleKeyStore class.
ReVa on pinned iOS16.0 keybagd: connector1aac8 matches AppleKeyStore and
opens type0, calls selector0. get_system1b7d0 sends selector14 with0/1 input
and1 output scalar. Entry calls this twice; failure reaches fatal system-bag
message. NVRAM/options diagnostic occurs in recovery/error handling, not
proof that adding an empty options node fixes loading. Existing root has
systembag.kb mode0600,227bytes; no reinstall indicated.

Candidate0107 adapts donor software AKS, opt-in a03_software_keystore=1,
explicit lab/no-SEP marker, only system bag0 supported; nonzero bags return
NotFound. No key wrapping implemented, unknown selectors Unsupported.
Adds independent IOKit provider/personality/source and general-register
codegen. Build/runtime validation pending. Private binaries ignored.

0107 exact CI-source patch application PASS; SweetKeyStore and config tables
cross-compile with general regs PASS. Host test compiles the actual provider
with stub IOKit: opt-in registration, selector14 argument bounds/system0,
lock state, Unsupported key-wrapping/unknown, DER output bounds/descriptors
PASS. Profile stages54patches including0107. Full CI and hardware pending.

Full build CI43730049732 started from09e658ffdbec16be4ec26087503dc0ceb88efa93.
Actual deployed ADT defaults/no-effaceable-storage=1 confirmed.

Host Download mode now detected for0050. Additional actual16.0 ReVa audit:
selector7 lock state is1 scalar in/1 out. Root systembag plist parses with
KeyBagKeys data5bytes (lab seed, not SEP-encrypted material). Boot trial uses
in-memory software system bag; does not claim these5bytes are cryptographic
keys. Existing defaults/no-effaceable-storage=1 selects plain plist loading.
CI43730049732 has entered Build; no0050 device flash yet.

## 2026-11-15: BOOT0050 software-AKS trial deployed

CI43730049732 SUCCESS from09e658ffdbec16be4ec26087503dc0ceb88efa93.
Kernel SHA623931b29ead3451e0d799450a8ed815da8605262c452c9150d5ce5da5d384f3.
Independent nm confirms AppleKeyStore::start, user-client externalMethod and
retained bindfs_vfsops. Required AKS/reply/USB/monitor strings present;
actual start disassembly calls PE_parse_boot_argn and checks enable==1.
BOOT0050 SHA39b298088a5633c0af00b76adaad96ffe5063c22a561a234e9d3f07183a72f19.
Same0049 args plus a03_software_keystore=1. Host capture36560 started before
Heimdall BOOT-only100%/success/reboot. USERDATA root/GPT/protected partitions
not rewritten. Await A03 AKS registration/selectors and keybagd result.
No hardware provider success, sustained launchd or GUI completion claimed.

Post-deployment source audit: exact CI43730049732 SweetKeyStore.cpp matches
host-tested source byte-for-byte, actual IOKit Makefile includes general-regs
flag. Capture36560 ended100s timeout/no enumeration. No AKS runtime outcome
yet; pending screen report required before another provider change.

## 2026-11-15: BOOT0050 reaches launchd_cache_loader; BOOT0051 prepared

User reports abort: Unable to find AMFI, followed by boot task failure
launchd_cache_loader / SIGABRT, caller0xfffffe0007add2f8. This advances beyond
the preceding keybag task; specific AKS selector/success logs were not reported.
Sustained bootstrap and USB CDC transport remain unproven.

ReVa on the actual installed iOS16.0 launchd_cache_loader confirms helper
0x100002414 reads kern.bootargs, tests launchd_unsecure_cache= via helper
0x100002dc8 (strtoul base10), and on nonzero logs Using unsecure cache before
calling common cache-loading helper0x1000028e8. It skips detached-signature
and AppleMobileFileIntegrity service/open/selector6 trust registration.
The observed abort is the missing-service branch0x100003074. Existing kernel
AMFI policy hooks do not provide that IOKit service. This is a loader lab
option, not implementation of full AMFI/trust enforcement.

Prepared BOOT0051 from exact0050 payload; only adds literal
launchd_unsecure_cache=1. Kernel remains CI43730049732 SHA623931b2...384f3.
Image SHA256 fbe8765853e9b542c61505b0fa2c677ee014311d50bf18e9be3ac932a11fad23.
Compared complete images: loader identical; payload identical outside cmdline;
ramdisk/DT/tail identical. Android header digest updated by verified packer.
No new CI needed, no root reinstall or device write yet. Host Download absent;
physical Download transition requested. Next: BOOT-only flash and observe
cache-loader completion/next actual error. Do not preemptively stub daemons.

## 2026-11-15: BOOT0051 cache-loader option deployed

User reports prior image bootlooped while attempting Download buttons, then
confirms ready. Host independently detected Download mode. Rechecked0051
SHA256 fbe8765853e9b542c61505b0fa2c677ee014311d50bf18e9be3ac932a11fad23
and cmdline with literal launchd_unsecure_cache=1. Heimdall BOOT-only upload
reached100%, reported boot upload successful and rebooted. No host USERDATA,
GPT, recovery, bootloader or EFS/NV write. Same0050 kernel/root/font retained.
USB capture session76745 started before flash; host log is
/tmp/a03-boot0051-usb-capture.log, private tty output if enumerated is
shim/a03/out/boot0051-usb-console.log. Physical cache-loader outcome and
sustained bootstrap still pending; requested last screen lines/reboot state.

## 2026-11-15: BOOT0051 starts daemons; repeated watchdogd crashes

User reports Process[576] crashed: watchdogd, Too many corpses being created,
and says output continues. This is evidence of launchd daemon orchestration
beyond the cache-loader boot-task failure, but not healthy/stable userspace.
The direct Using unsecure cache log was not transcribed. The exact watchdogd
reason and whether other services also crash are pending screen evidence.
USB capture0051 ended100s timeout without CDC enumeration.
Extracted actual installed iOS16.0 watchdogd privately for ReVa; donor service
is reference only until actual ABI/failure is inspected. No new flash/root write.

Actual16.0 watchdogd ReVa: entry0x1000076c0 calls connector0x1000057bc
before examining monitoring/test args. Connector matches IOWatchdog, opens
type1; missing service leads to failed-to-discover then fatal helper unless
VM detection succeeds. nm on deployed0050/0051 kernel shows no IOWatchdog
symbols (AppleKeyStore::start and bindfs_vfsops do exist). This identifies a
missing prerequisite, but no direct watchdog error/PC has yet been reported.
Selector0 asks enabled with one scalar output; false takes the daemon's own
monitoring-disabled path and sleep2/exit0 helper0x1000076a8. The donor generic
accept-all stub is not deployed. wdt_test=no_user_checkin is checked only
after service connection/enabled query, behind internal-diagnostics gating,
and touches NVRAM; do not propose it as a standalone missing-service fix.
Next: collect current failure line/other daemon names; then implement scoped
opt-in lab IOWatchdog only if supported by crash evidence, preserving actual
unsupported selectors and reporting that hardware watchdog is not provided.

## 2026-11-15: BOOT0051 additional daemon observations; user requested stop

User subsequently reports backboardd crashing, then SpringBoard crashing.
They observe Allowing spawn of iOS binary for fairplayd, mDNSResponder and
xpcproxy; xpcproxy appears most repeatedly, with bluetoothd and
identityservicesd also appearing. Only watchdogd, backboardd and SpringBoard
were explicitly reported crashing. Spawn lines alone do not establish that
fairplayd/mDNSResponder/xpcproxy/bluetoothd/identityservicesd crashed or stayed
alive. No exact crash PC/reason/stack yet, and no GUI or stable userspace proof.
BOOT0051 remains installed; no additional flash or root rewrite occurred.

Actual root backboardd was extracted privately and imported/analyzed in ReVa
as /backboardd; no functions inspected yet. Donor display/HID failures are
reference hypotheses, not A03 diagnoses. ReVa watchdogd audit remains as above.

UNFINISHED LOCAL WORK (not validated, not deployed):
- xnu/a03/0108-a03-bounded-daemon-crash-diagnostics.patch adds opt-in
  a03crash_log=1 selected-daemon signal/reason/register/6-frame reports,
  saturating two reports per selected name, independent of corpse capacity.
- tools/a03-build-profile.py and .github/workflows/xnu.yml have uncommitted
  staging/linked-marker edits for0108. No CI dispatched, no0052 image.
- First local syntax attempt matched no commands because helper uses old
  donor CI path. Private normalized log /tmp/a03-43720286686-normalized.log
  fixes matching; retry could not execute compiler because expected
  /home/stoned/swift/usr/bin/clang does not exist. No compile success claimed.
- Scratch /tmp/a03-buildcheck-43712255840/xnu contains0108 working edits;
  bsd Makefile baseline was recovered from exact0050 CI before adding flag.
- Before using0108: inspect/recount hunks and actual p_comm truncation,
  review bounded logging, apply against exact0050 source, find toolchain,
  compile both C files, test rate limit/gating, then full CI + linked checks.
  Do not flash unfinished patch. Missing IOWatchdog service remains likely
  watchdog prerequisite, not a confirmed reason for all daemon crashes.

User explicitly requested notes and stop. Work stopped after this handoff;
no further build/flash/device transition requested. Resume only on user request.

## 2026-11-15: XNU USB source audit and0109 candidate

User resumed work specifically to obtain XNU USB logs instead of reading the
screen. BOOT0051 still has no host USB enumeration; its initialized message
is not physical attach evidence. No device currently visible in host lsusb.

Audited matching local Samsung source and private live DT (not staged):
phy-sprd-qogirl6.c probe requires ANA_EB alongside OTG_UTMI_EB; init explicitly
sets/enables3300000uV VDDUSB33. Existing XNU omitted ANA_EB and inherited an
unverified PMIC rail. musb_sprd.c has no MUSB_INDEXED_EP quirk, so Linux uses
flat endpoint registers0x100+ep*16, unlike XNU's indexed0x10 aperture.

Added0109: missing analog gate; bounded ADI read/address-echo validation;
SC2730 USB-only voltage/power setup with preserved unrelated bits and verified
readback; flat EP0/bulk/interrupt registers; USB pin mux selection; clear
vendor host-force and20ms soft detach. ADI writes allowlisted to regulator
unlock1bd0, USB PD19e8 and USB voltage19ec only. Live DT uses sharkl5 fallback
ADI window0x20000/address echo and no ADI hwlock. No partition operations.

Local exact0050/0051 USB patch apply/reverse PASS; clang23 arm64 Mach-O kernel
syntax with actual CI BSD flags and -mgeneral-regs-only PASS. Cumulative CDC
protocol/flat-bank checks, monitor parser and bounded ADI/supply emulation
PASS. Supply tests exercise no-op rail state, preserved bits, allowlist,
busy/FIFO timeouts, bad address echo and failed readback. Hardware success
remains unproven; next full build and BOOT-only test. Keep0108 crash-diagnostic
WIP and its local staging edits out of this USB build/commit.


Full USB build CI43737353634 dispatched from13baa99.0108 WIP was deliberately
excluded from the committed profile/CI gate (local working changes preserved).
Real local Mach-O object compile of0109 also PASS with -mgeneral-regs-only.
BOOT0052 packaging will reuse exact0051 ADT and command line.0051 payload
has no RAMDisk segment (corrected initial packaging assumption); installed
validated USERDATA root is retained without host rewrite.

Additional cumulative CDC regression PASS: bus reset clears configuration/
address and rebuilds independent flat banks; SET_ADDRESS waits for completed
EP0 status; bulk EP1 accesses leave EP0 CSR untouched. No hardware claim.

## 2026-11-15: BOOT0052 USB supply/flat-register candidate deployed

CI43737353634 SUCCESS from13baa99, including linked USB supply/flat-ep marker
gates. Kernel SHA256 ae813082d1fced07d068b33b5cd0a31705293934fab04abe1db54ee59daa81be.
BOOT0052 SHA25626ef37ccfced6ff9f7689675c7c8bbbcdc7ab72ed10bdbf06a515b22cb34ade0.
Exact0051 loader (masking image_size), ADT and cmdline preserved;0051 payload
was independently reproduced byte-for-byte before replacing only the kernel.
No RAMDisk. Existing USERDATA root retained; no host root rewrite.

User confirmed Download ready; host Heimdall detect independently succeeded.
BOOT-only upload reached100%, boot upload successful, reboot. No GPT,
USERDATA, recovery, bootloader or EFS/NV write. Host journal initially shows
only Download disconnect, no USB attach/ttyACM. Capture63236 waits120seconds
at /tmp/a03-boot0052-usb-capture.log; private tty log if enumerated would be
shim/a03/out/boot0052-usb-console.log. Requested new physical supply before/
after or failure, CORE and configuration/reset/setup lines to discriminate
remaining failure. No hardware USB success claimed.

BOOT0052 USB ENUMERATION CONFIRMED at2026-11-15 17:06:17UTC:
host xhci reports new full-speed device1d6b:0104, manufacturer A03 diagnostic,
product A03 XNU console, serialA03XNUConsole01; Linux cdc_acm binds ttyACM0.
This is actual XNU USB descriptor/configuration/CDC-driver success. It does
not yet establish bulk log transfer or interactive monitor response.

Capture63236 found the exact device but open failed EACCES: ttyACM0 is
root:uucp0660; current user lacks uucp. Scoped sudo setfacl attempt refused
because sudo requires password. Asked user to run only
sudo setfacl -m u:stoned:rw /dev/ttyACM0, then resume capture. Empty private
capture files do not contain kernel logs. No host credential requested.
Exact deployed CI USB source matches tested source byte-for-byte; BSD
Makefile confirms -mgeneral-regs-only. No more phone flash indicated.


## 2026-11-15: BOOT0052 XNU console data transfer confirmed

User corrected host tty permissions and reports mediaserverd/backboardd/
watchdogd crashing. Exact-identity host capture then successfully opened
/dev/ttyACM0 and saved289235 bytes/5002 lines over45seconds to ignored
shim/a03/out/boot0052-usb-perms-fixed.log; SHA256
f28a19c9883862ac8a8736c932cf265f82888b9086ea6ad2286e61a6217848c9.
Capture includes buffered startup plus continuing userspace output, with
an incomplete opening fragment. Actual XNU USB bulk console transfer is now
proven, not merely enumeration. No interactive monitor/panic service claim.

Captured supply before pd=0001 vol=00d2, after pd=0000 vol=00d2 proves the
inherited USB rail was powered down and XNU enabled it at retained3.3V.
PHY trim04b3d1c0 ctl1=1c010000 ctl2=0 sel=6; CORE power50 devctl98 hwvers0200
ext00; EB1=001eb9f3 ref=00a3ffab mux0; configuration1 resets2 setups14.
0109 combined changes work; their separate contributions remain unisolated.

Captured crash-line counts: backboardd19, mediaserverd43, watchdogd17,
configd8, lockdownd3. Counts describe this log, not all exits: early crashes
may lack the corpse-limit message. Exact causes/signals/PCs not logged.
Backboardd AKS selectors0/17 return0 before a crash; that alone is not its
cause. Several earlier filesystem/persona warnings exist, but no causality
established. No new provider/stub/change justified solely by these names.

Started an additional300second capture79265 to ignored
shim/a03/out/boot0052-usb-continuing.log (host stderr/stdout
/tmp/a03-boot0052-usb-continuing.log). BOOT0052/root remain installed; no
phone writes/reboot in this follow-up.0108 WIP preserved, not deployed.

## 2026-11-15: resume iOS boot goal with USB crash evidence

User asks to advance iOS boot using the working USB tooling. Finished0108
against exact deployed0052 sources: opt-in a03crash_log=1, two saturating
reports per selected daemon, before corpse limits. Added actually observed
mediaserverd/configd/lockdownd; corrected identityservicesd p_comm truncation
to16characters. Prints signal/exception, exit reason, user PC/LR/SP/FP/FAR,
cache slide/main header, up to6frames and bounded printable x19 text.
Read-only diagnostics do not bypass exits or create providers.

Actual-source boot-gate/name/two-report saturation tests PASS, exact0052
patch apply/reverse PASS, both affected C files arm64 kernel syntax using
actual CI flags plus -mgeneral-regs-only PASS. Existing0108 profile/workflow
WIP now validated for this diagnostic build; full CI/runtime still pending.
Next0053 uses0052 loader/ADT/root/args plus a03crash_log=1. No root rewrite.

Full diagnostic build CI43739909683 dispatched fromc3d3c98. Working USB0109
retained; runtime crash reasons pending. No0053 flash yet.

Added read-only tools/a03-symbolicate-cache.py for the next USB crash PCs:
validates matching cache/subcache/symbol UUIDs, tests actual executable
Mach-O segment membership, reports image/base/offset and nearest preceding
local symbol. Explicitly labels local-symbol proximity, not a proven function
boundary (exports may intervene). Reproduces independently established0045
pthread assertion:1e6f71f5c-slide19274000=1cdcfdf5c, libsystem_pthread,
___pthread_init.cold.3+24. Apple assets stay ignored. Actual watchdogd ReVa
fatal helper10000b2f4 independently resolves missing IOWatchdog lookup to
os_crash message and BRK; current runtime cause still awaiting0053 evidence.


## USB Download command0110

Exact download line handled by worker outside PID1 hold; filesystem sync then stock Linux SC2730 restart:1bac lowbyte30 preserving high,1bf8 bit4,1824 bit0. Fixed bounded ADI operations with prerequisite/readback checks; no arbitrary register interface. Supply allowlist unchanged. Host parser/reset tests and kernel arm64 compile PASS; runtime reset unverified. Combined0108+0110 CI43740528122 from69882d3 supersedes crash-only43739909683. BOOT0052 lacks command; initial physical Download needed.


## 2026-11-15: BOOT0053 Download command installed

Combined CI43740528122 SUCCESS from69882d3. Kernel SHA256
566611c65c26e5c9b37cc136de8171d5163363431f0aac4208ef9d250f2f1d7e.
BOOT0053 image SHA256
bca699fb0e9c0ffdb164394898a6b38b19744d48d547d58466aec4dfd82c2377.
Independent image checks:0052 loader (excluding image_size) and ADT exact;
args only add a03crash_log=1; Download acknowledgement present. Cumulative
CDC/supply and actual-source fixed reset/parser tests PASS.

Heimdall detected physical Download mode; authorized BOOT-only upload reached
100%, reported boot upload successful and rebooted. No host USERDATA, GPT,
recovery, bootloader, EFS/NV write. New USB capture started before flash,
waiting for enumeration. Download reset and crash diagnostics hardware
results pending; no new runtime or stable iOS claim.

BOOT0053 USB reappeared47seconds after flash; host access available without
another user request.60second capture356191bytes/4848lines, SHA256
a0079227c49284a19ec67ef0c1971b1ad79877888bf3220336466b030c3b6cc5,
private boot0053-usb-initial.log.0108 reports watchdogd SIGTRAP at main image
offset0xb308 (both launches), bt offsets0x58a4/0x770c. Runtime now supplies
exact PCs; other daemon reasons remain pending.

Hardware Download command FAILED: normal host tool, newline-reset retry and
slow-byte retry gave no acknowledgement/reset. Host TIOCOUTQ drained to0;
USB IN continues. No evidence that reset sequence was reached. Do not claim
Download works.0111 adds first4 RX packet byte logs and first4 periodic RX
CSR/count/indexed/FIFO state snapshots to isolate transport before PMIC.
Host test now exercises actual poll_usb FIFO->parser with split download
line and rejects oversized packets. Kernel syntax compile PASS.

Receive-diagnostic CI43742555051 started fromf28fc71. BOOT0053 remains
installed; next diagnostic not yet built/flashed.

Additional0053 follow-up capture reports SpringBoard SIGTRAP at
0x1b1da39a4, cache slide0x16e0c000 -> FrontBoardServices+0x579a4, nearest
local symbol -[FBSDisplayMonitor _initWithBookendObserver:transformer:]+0x488.
Caller0x1b8315768 -> FrontBoard+0x50768, nearest local symbol
___34+[FBDisplayManager sharedInstance]_block_invoke+0x100. These identify
crashing code, not a proven missing-provider diagnosis. Identityservices
SIGABRT also captured. USB Download work remains active.

Five-minute0053 follow-up saved306913bytes to private
shim/a03/out/boot0053-usb-followup.log. Two reports each for SpringBoard
and identityservices; bounded counter saturation confirmed in this capture.
USB IN continues while Download acknowledgements remain absent.

CI43742555051 SUCCESS fromf28fc71; BOOT0054 RX diagnostic packaged but
UNFLASHED. Kernel SHA256
75e7d098a2353a443e1d585be530e974a38a9d1feebf63b54b59653f6a2ac25b.
Image SHA256
e5082d921d19c084b63d0f46a2c369dda665e10b1196cf0f4e0d2b633614511a.
Independent check confirms0053 loader/ADT/args retained and exact CI USB
source equals locally tested source. No RAMDisk/root rewrite. Host still
sees CDC, not Download; physical transition requested for next BOOT test.
No working Download-command claim.

## 2026-11-15: runtime causes narrowed; BOOT0054 deployed

BOOT0053 watchdogd PC main+0xb308 matches BRK at actual iOS16 watchdogd
0x10000b308: connect_to_kext unexpectedly failed, unable to lookup watchdog
KEXT service. This is now runtime-confirmed missing IOWatchdog, not only
a string-based candidate. Its selector0 boolean false takes existing
userspace-monitoring-disabled cleanup/exit path.0112 adds opt-in
a03_watchdog_disabled=1 service, open type1 only, selector0 false only;
unknown selectors unsupported and argument shapes checked. No hardware
watchdog/check-in success fiction. Host actual-source gate/type/shape tests
and two kernel C++ syntax compiles PASS; full build/runtime pending.

SpringBoard trap0x19af979a4 (unslid) decodes assertion: failed to find the
main CADisplay. Branch comes from nil result in FBSDisplayMonitor init;
this identifies missing display discovery, not enough for an arbitrary
display stub. Apple code extracted/read only under private /tmp files.

Host detected physical Download. BOOT0054 e5082d92...4511a flashed only
boot,100percent/success/reboot; no host USERDATA or protected writes.
Capture16470 waits240seconds for USB, then90seconds. Need RX state/packet
evidence and Download retry.

0054 CDC enumeration confirmed50s after flash; new tty requires ACL.
Capture16470 remains waiting; user asked scoped setfacl.0112 full CI
43744288276 running from5eee9b2. No watchdog hardware success yet.

0054 USB capture opened after user ACL correction. RX diagnostics report
four unsolicited packets csr0803 count1 data00, then repeated flat/indexed
csr0800 count0, FIFO03/address0010; TX2004. Explicit newline/download10byte
write still no ACK/reset. Linux defines0800 RX DMAMODE; inherited DMA state
was not cleared by current startup.0113 disables enable bit0 of documented
30 SPRD channels with readback, clears endpoint DMA CSR state and double
flushes EP1 as Linux gadget init. Actual cumulative host test verifies all
30 channel enables clear while other bits remain, split command reception;
exact kernel C syntax PASS. Runtime effect unproven.

Combined0112+0113 CI43744564237 from62736e7 supersedes watchdog-only
43744288276. BOOT0054 installed,0055 pending.90second0054 capture297403bytes
SHA2569e2116fabf4ffc628b3b6672d7dd4efe5618587be2c608dc87f6b0bb57f5ef4a.
Source observation is RX DMAMODE left set; it does not yet prove DMA enable
was active or that clearing it alone fixes console commands.

Further read-only cache tracing: FBS init sends CADisplay displays then
firstObject; nil branches to exact main-CADisplay assertion. QuartzCore
+[CADisplay displays] calls ensure_displays; discovery uses CASGetDisplays
through com.apple.CARenderServer bootstrap port. Therefore nil list is not
yet direct proof of missing IOMobileFramebuffer: backboardd render-server
health and display discovery need tracing before provider implementation.

0054 additional crash PCs: mediaserverd SIGSEGV/FAR0 at runtime18dbed1b0
minus slide0bf3c000 = CoreFoundation181cb11b0; caller1954f2ea4 in
FigNotificationListenerStartNotifications. Backboardd SIGABRT stack passes
libobjc objc_terminate and libc++abi terminate path; underlying exception
reason not printed. Neither supports an arbitrary hardware-provider fix.

Read-only watchdogd audit found additional prerequisite before selector0:
0x100009d08 requires IOPropertyMatch IOPMUPrimary, and disabled cleanup writes
IOPMUBootStage255. Customer build ignores internal-only -wdt_no_pmu.0114
provides strict one-key integer0..255 software bookkeeping property, no
PMU hardware writes, unknown property dictionaries unsupported.0112 alone
will remain disabled in the next USB-only test. Host property shape/range
tests and kernel C++ syntax PASS. Full build/runtime pending.

User confirms Download ready again; host detects it. Combined CI43744564237
remains building.0055 will preserve0054 arguments, keeping0112 disabled
until0114 is fully built. Later workflow marker gate now requires PIO and
watchdog software-stage strings. No new flash after0054 yet.

## BOOT0055 isolated USB PIO takeover test

CI43744564237 SUCCESS from62736e7. Image SHA256
2cf20091b428f9043fd3a77b09903df0de3f4c3ab0b337c3d9dd1549d1043aec.
Exact CI USB source equals tested source;0054 loader/ADT/args preserved,
0112 opt-in remains OFF pending0114 full build. BOOT-only upload100percent,
success/reboot. No host root/protected write. Capture99106 waiting240s for
enumeration then100s. Watchdog0114 CI43746031809 frome55d573 started.

BOOT0055 kernel SHA256
f527d6df8be4cf30d0082ad4d89263a70a205295067c558bd97b3d11f5c630b8.

BOOT0055 enumerated46s after flash; capture opened with ACL available.
PIO takeover logs RXCSR0800 despite writes clearing DMA mode. First4 RX
packets still count1/data00; newline/download10bytes no ACK/reset. This
contradicts the claim that simply clearing inherited DMA fixes input.
Capture375665bytes/5183lines SHA256
f72be59d47bff337666edb26eece67bd22dfc1bd0c9425aa99c93a4a9e6097b0.

0115 adds explicit CDC SEND_BREAK valueffff/index0 escape to same bounded
sync/reset worker. Host --download-control uses Linux TIOCSBRK5427, only
when explicitly requested. Ordinary capture/CDC open and break-clear0 do
not trigger reset. EP0 setup path works for enumeration; reset still must
be hardware tested. Bulk command remains for eventual RX repair. Actual
protocol positive/clear-break tests and kernel syntax PASS.

Combined0114+0115 build43746383199 from3a3f19a queued; requested cancellation
of older43746031809 before packaging. BOOT0055 installed, reset unresolved.

Symbolication correction: image LC_SYMTAB exports put mediaserverd unslid
181cb11b0 in CFDictionaryGetValue+0x48, not a proven CFRetain function.
Matching instruction ldr x8,[x0] with captured FAR0 establishes null dictionary
passed by FigNotificationListenerStartNotifications+0x38. Extended tool
reports nearest local AND exported symbols, retaining proximity caveat.
No Apple binary edits. Need trace listener initialization before patching.

## 2026-11-15: BOOT0056 control Download and watchdog test deployed

CI43746383199 SUCCESS from3a3f19a. Exact downloaded USB/watchdog sources
match locally tested source. Loader excluding image_size and ADT equal0055;
args only add a03_watchdog_disabled=1; no RAMDisk or root rewrite.
Kernel SHA2566f4e9160a2dbe76a54dbf4d14cbb2ad841f419aaefb90a8ac058f4148a7cc19b.
Image SHA2569ec37ad159f9d16f0b1ba2deafdba09021e9aea3c877c89978d1d751ad09b880.
BOOT-only upload100percent/success/reboot at18:39UTC. USB enumerated within
55seconds; new tty access is denied. Capture21837 waits240s then100s; user
asked scoped ACL once. Control reset and disabled-watchdog runtime pending.
No host USERDATA/GPT/recovery/bootloader/EFS/NV write.

All USB/watchdog host suites and crash/symbolication suites PASS. Extended
actual-source control test rejects wrong type/request/value/interface/length;
only exact indefinite SEND_BREAK requests reset. Matching local Linux CDC
break callback maps nonzero state to0xffff, clear to0.

## 2026-11-15: bounded deeper exception trace prepared

BOOT0056 initial capture21837 expired on verified EACCES; USB remains present,
no watchdog/reset runtime conclusion. Replacement capture92355 waits900s for
access, then100s, writing private boot0056-usb-access.log. No repeat ACL request.

Backboardd0054/0055 traces stop at six frames inside Objective-C/C++ terminate;
0116 extends only the existing read-only frame walker to24frames/544bytes.
Existing bootarg/name selection/two-report cap, checked copyin/alignment and
strictly increasing frame pointers retained. Actual patched walker host tests
cover24-frame cap, null/unaligned FP, failed copy and nonincreasing chain PASS;
exact kernel exception.c general-register syntax compile PASS. Not deployed.

Full0116 CI43748416531 dispatched fromf30d070; BOOT0056 retained.
No extra flash before its pending watchdog/control-reset evidence.

BOOT0056 access restored18:45UTC; waiting capture92355 opened automatically.
Runtime confirms A03 WDT registration, selector0 disabled response and software
boot stage255 on two watchdogd launches. No CRASH watchdogd in current capture;
this validates the disabled path, not active watchdog functionality. Backboardd
SIGABRT and mediaserverd null-dictionary crash persist. Control reset test next.

BOOT0056 final100second capture313123bytes/4857lines SHA256
f30aecb9e0fd6a2b0eabcc10443474ca838db056b46526c26717290f08b82283.
Explicit --download-control FAILED at host ioctl with EOPNOTSUPP before any
reset ACK; phone remains CDC. Descriptor advertises ACM0x02, lacking CAP_BRK.
Linux v6.18 cdc-acm acm_tty_break_ctl explicitly rejects without CAP_BRK0x04;
matching local4.14 does not have this check.0117 changes ACM capabilities
0x02->0x06, retaining descriptors otherwise. Actual descriptor test asserts
0x06; cumulative host test and kernel general-register syntax compile PASS.
No evidence PMIC reset worker was reached. Full build/hardware retry required.

Combined0116+0117 CI43748823542 dispatched from1ab9e92; cancellation of
0116-only43748416531 requested. Physical Download requested once for0057.
BOOT0056 remains installed; no new partition write after that test.

Read-only backboardd startup trace: entry10000a684 dispatches windowserver
block10000b758 -> once block10001c4d8. This initializes CAWindowServer with
kCAWindowServerDisableUpdatesOnMainDisplay, queries CADisplay.mainDisplay,
and explicitly logs a headless path if either display/server display is nil.
Thus absent main CADisplay is not by itself proof of the backboardd SIGABRT.
Need0116 deeper runtime stack to identify actual thrown-exception origin.
Host now detects Download again18:49UTC; do not request another transition.

Further read-only media trace: manager init1954ee604 stores result of
+[ARPRoutePredictor routePredictor] at derived storage+18 (1954ee908).
Class/key loaded via dlopen AirPlayRoutePrediction and dlsym at1954f76b0.
Framework is present in the exact plain-arm64 cache. ARP init1ccb54b48 has
a nil-return path when notify_register_dispatch fails (call1ccb54cf0; branch
1ccb54d00). This is a candidate cause, not runtime proof; need deeper crash
state or notification diagnostics before changing IPC behavior.

## 2026-11-15: BOOT0057 corrected break descriptor deployed

CI43748823542 SUCCESS from1ab9e92. Downloaded USB/exception sources equal
local tested sources;0056 loader/ADT/arguments preserved, no RAMDisk/root
rewrite. Kernel SHA2569f176b5e0a983f06507fa3ed8806c64f8e7ea525056b4d9a2551c774b07b2d3a.
Image SHA2563f1d1ac4b3f6978402389aac406b5efbe7c1c5e42b4149ca38352c20c050144d.
BOOT-only upload100percent/success/reboot19:03UTC. CDC enumerated within58s;
user restored tty ACL and capture60997 opened. Sysfs actual descriptors now
contain ACM capabilities06. WDT selector0 disabled/software stage255 persists.
90second initial capture running; deeper crash/reset evidence pending.
No host USERDATA/GPT/recovery/bootloader/EFS/NV write.

BOOT0057 final90second capture360618bytes/4921lines SHA256
c89236085e9f7cdb2849e789ea83ffea6e5760980be493eec59f389052428b60.
Deeper backboardd trace reaches main+0xa354 and+0xaa20,
through dispatch_once; exact entry call10000aa1c dispatches windowserver.
Exception unwinding removes original thrown-site frames before terminate.
Mediaserverd still null dictionary; WDT disabled path still confirmed.

HARDWARE DOWNLOAD SUCCESS: explicit --download-control returned0; CDC
disconnected and Heimdall immediately detected Download at19:06UTC, repeated
detect PASS. Private control capture6528bytes/105lines SHA256
931b5a5340e0cde1cb742295a2e8e57fa40ac3403652f408dfcc0bca9761d58d.
ACK text not captured (earlier queued logs consumed the drain), so evidence is
host request success plus actual CDC->Download transition, not ACK visibility.
Bulk line download remains unproven/broken; use explicit control command.

## 2026-11-15: bounded Mach-O crash annotations prepared (0118)

BOOT0057 remains installed; host confirms Download mode, no tty currently.
0118 extends the existing opt-in/two-report crash logger with current-task
read-only Mach-O __crash_info collection for main image, libc++abi and libobjc.
No fixed Apple addresses: dyld image-array prefix follows local kdp_dyld.h;
Mach-O __TEXT mapping supplies slide and validated section supplies location.
Only version5 annotations, message/message2; 2048 images,128 load commands,
64KiB commands,128 sections and255-character sanitized text bounds. copyin
failures/overflow/malformed metadata stop reads. Existing root untouched.
Exact root libc++abi section version5 verified read-only; fatal routine writes
its termination message at annotation+8 before abort. This is diagnostic;
no underlying backboardd/media repair claimed. Actual-source synthetic parser
layout/slide/message2/sanitization/truncation/malformed/fault/overflow tests,
existing crash/USB-download/watchdog tests and exception.c general-register
kernel compile PASS. Full CI and hardware capture pending.

Full0118 CI43751227542 from7e5ecb7 supersedes43751096298 (cancel requested).
Read-only exact-cache check found shared-cache __TEXT fileoff is nonzero;
parser corrected before deployment and regression explicitly exercises this.
No BOOT0058 flash yet; phone remains in Download. Earlier0057 UMD notify8
is NOT proof of mediaserverd notification failure: it can originate in a
process that intentionally disables notifications; media candidate unproven.

## 2026-11-15: BOOT0058 annotation diagnostic deployed

CI43751227542 SUCCESS from7e5ecb7. Downloaded exception.c/USB source matches
locally tested source. Exact0057 loader (except image_size), ADT and args
preserved; no RAMDisk/root rewrite. Kernel SHA256
0c82adf788ece8d17d61c781a44efb7d1f78ed6df2375b5dfd5ed8d013ec570b.
Image SHA25609f5350cbf8acffabf08a9d14b261241a38f8bd8777e7e9bef655f6b08fa7b69.
BOOT-only Heimdall upload100percent/success/reboot19:26UTC. Capture77592
waits900s then100s into private boot0058-usb-initial.log. Runtime pending.
No host USERDATA/GPT/recovery/bootloader/EFS/NV write.
User requests silence during routine CI waits; only results/needed input.

BOOT0058 CDC enumerated, user ACL restored; capture77592 opened. Runtime
annotation scan reaches455 loaded backboardd images, both selected libraries.
libc++abi v5 annotation1: "terminating with uncaught exception of type NSException"
on both backboardd reports. This confirms diagnostic execution but gives no
exception reason. Libobjc has no __crash_info in this cache. Read-only exact
cache inspection identifies v5 sections in Foundation/CoreFoundation/QuartzCore
and libc abort path sets libsystem_c annotation at1dd8f8430.0119 extends only
selected image paths to these four owners (max6 matches total); bounds and
no-user-write behavior retained. Actual-source selector tests exercise all6
paths/unselected rejection; parser and exception.c kernel compile PASS.
Media null dictionary and configd null+54 persist; WDT disabled path remains.
No stable GUI claim. Next combined build pending;0058 running, tty accessible.

BOOT0058 final100s capture: 300945bytes/4678lines,
SHA25607ec8085b129c122fdab54f1dc51a7065152b899b21a93f21453925e84b5155d.
Combined0119 CI43752732761 from4e22af5 queued;0059 packaging waits on success
and exact source/loader/ADT/args checks.0058 remains running; tty accessible.

Read-only exact CoreFoundation uncaught handler181d40368 confirms reason
collection route: call181d40598 converts formatted exception diagnostic, then
181d405a0 stores pointer at1dd6d5fd0 = __crash_info+8 (section1dd6d5fc8).
Thus0119 CoreFoundation selector targets the actual exception reason owner,
not speculative display behavior. Next runtime must verify whether handler
ran and populated it; no Apple userspace mutation.

Media dictionary clarified by exact-cache read-only code/CFString decoding:
FigNotificationListenerCreate1954f2c90 constructs a mutable dictionary with
notificationCenter/observedObject/notificationName/serializationQueue keys.
StartNotifications1954f2e6c first reads notificationCenter at1954f2ea0;
matching captured LR1954f2ea4 and CFDictionaryGetValue FAR0 prove the entire
listener dictionary pointer is NULL, not an absent key or on-disk plist.
Constructor returns NULL for absent predictor/object or notification name;
which input is missing remains runtime-unproven (allocation failure also
not excluded). Do not silently replace dictionary or fake notify success.

## 2026-11-15: BOOT0059 framework annotations deployed

CI43752732761 SUCCESS from4e22af5. Exact downloaded exception/USB sources
match local validated source;0058 loader (except image_size), ADT and args
preserved. Kernel17418f77ff7b185b31fd6cb1783a0a0246ef2685dd726c0ec3c1112bc22a98a8.
Imagec03d24d795070925e8a18ba2a972124ce2faca53a82e46ac5434f87eaa61bd87.
0058 --download-control returned0 and Heimdall detected Download again.
0059 BOOT-only upload100percent/success/reboot19:42UTC; capture2930 waits
900s then100s, private boot0059-usb-initial.log. No root/other partition write.
Need CoreFoundation annotation runtime reason, not just libc++abi type.

BOOT0059 capture group access solved without sudo: /etc/group already lists
stoned in uucp, but inherited agent supplementary groups omit it. newgrp uucp
launches capture with existing authorized membership. Initial ACL wait2930
terminated; capture4638 opened immediately, no user ACL required. Use newgrp
for future captures and control reset; no persistent permission change.
Final100s log 298400bytes/4757lines SHA256
87c779288a2dc194423cb5cc7b87ccb002706f86590ad1a13f4e8fc4cb08564b.

BREAKTHROUGH: both backboardd reports CoreFoundation annotation1 explicitly
NSInvalidArgumentException: "*** -[NSURL initFileURLWithPath:]: nil string parameter".
libc++abi generic exception and libc abort annotations agree. This is not yet
fixed. Read-only startup once block10001c4d8 first asks BSPathProviderFactory
system container provider -> cachesPath -> path, before CAWindowServer.
BaseBoard defaultPath18d96606c calls BSSystemSharedDirectoryForCurrentProcess
then NSURL fileURLWithPath. That directory derives from
container_system_path_for_identifier via18d957d04; failure returns nil.
Candidate is system-container resolution, not proof absent display causes abort.
Exact backboardd embedded XML includes com.apple.security.system-container=true.
Original host root contains containers/Data/System and Shared/SystemGroup;
current phone state can differ. Need container lookup failure details, not
invented paths or blind root rewrite. Media null dictionary still persists.

## 2026-11-15: bounded startup failure evidence prepared (0120)

Previous goal turn made progress: BOOT0059 captured exact nil-path exception.
Current root cause remains unproven: original parent directories and embedded
backboardd system-container entitlement are present, but live container query
can fail for IPC/permissions/entitlement or another prerequisite. Do not invent
paths, bypass constructor failures or mutate Apple user code.
0120 logs read-only syscall return evidence for backboardd/containermanagerd/
mediaserverd/notifyd under existing a03crash_log=1.192 reports/name per boot;
only errors plus successful csops/MAC queries. Captures errno/result/PC/4args,
bounded sanitized path for known pathname syscalls; entitlement query first
8 output bytes only when buffer length permits. No errno/user-state changes.
Actual-source host selection/gating/path/header/cap test PASS; systemcalls.c
kernel general-register compile PASS. Full CI/hardware pending;0059 retained.

Read-only follow-up confirms exact IPC-denial mechanism in this userspace:
launchd1000165f4 calls sandbox_check_by_audit_token and permits only return0;
service resolver10002cefc returns159 when that wrapper denies mach-lookup.
Exact cache sandbox_check_by_audit_token1cdc4cd98 builds the request passed
to1cdc4cf10, which invokes __mac_syscall("Sandbox",2,arg) at1cdc4d0e8.
Op2 request first64-bit word is pointer to zero-initialized64-bit result;
nonzero syscall return maps to-1, successful call returns result!=0.
Current compiled sweet_amfi.c registers only SWEET AMFI, and mac_base.c
returns ENOPOLICY103 when no matching policy exists. This establishes an
unimplemented API, not yet which failing media/container request hits it.
Do not substitute broad success for unknown profile/token/data operations.

Media notify path independently traced: notify_register_dispatch1a93336dc
enters1a9333518 -> register helper1a933662c -> initialization1a9337828/
1a9337008. Its bootstrap lookup block1a9336fb8 requests exact service
com.apple.system.notification_center; failed lookup produces notify9.
Init disabled flag instead produces8; these must not be conflated. Original
root notifyd launch plist advertises that exact MachService. Runtime media
failure still unproven; pending0120 boot has bounded syscall diagnostics.

## 2026-11-15: BOOT0060 startup syscall diagnostic deployed

CI43754890342 SUCCESS from39eef988e961424e8ba254bc539daa449437abe6.
Packaged sources exception/USB/systemcalls/bsd Makefile match local validated
through0120. Exact0059 loader(except image_size), ADT and args preserved;
no RAMDisk/root rewrite. Kernel SHA256
 eb4d7433147aa6148fd9a942e7fefe25f0fb8d35d401babb33a50988ffc0cc92
Image SHA256
 2736fe2a13ac3cb7d16d881c5b505509a574f7f6f60219ee665551e7800f757a
0059 control Download reset disconnected CDC; subsequent Heimdall detect
PASS after transition delay.0060 BOOT-only upload100percent; runtime pending.
Capture83189 waits900s then100s via newgrp uucp into private
boot0060-usb-initial.log. No host USERDATA/protected partition write.

BOOT0060 BOOT upload success/reboot confirmed; CDC capture opened without
ACL change. Actual0120 traces now prove mediaserverd/backboardd/notifyd/
containermanagerd all receive syscall381 errno103 ENOPOLICY for Sandbox op2.
Other recorded operations include Sandbox op4 and AMFI op90; do not give
unknown data-returning operations fake success. Container csops_audittoken
op16 succeeds with nonzero DER header; blanket missing-entitlement claim
unsupported. Backboardd still aborts with exact nil NSURL path exception.

0121 implements only decoded Sandbox op2 scalar check for explicit
 a03_sandbox_disabled=1 lab no-sandbox boot mode(default0).
It copies in result pointer and copies out64-bit allow0; copyin/copyout
errors propagate. Every other policy operation returns ENOTSUP, including
profile installation, container paths and extension tokens. No Apple
userspace patch.32 bounded reports, policy registration only for value1.
Actual-source host tests unsupported ops/faults/null/result width/log cap
PASS; sweet_amfi.c general-register kernel compile PASS. Full CI/runtime
required. This repairs an observed missing API, not a claim media is fixed.

BOOT0060 initial100s capture completed:494160bytes/6744splitlines SHA256
038949c56f1d04a6d70c716f9d86a84cedb68de223ed866bea0273f303f93278.
Runtime cache slide08074000. Two bounded backboardd reports retain nil URL
exception; two media SIGSEGV reports retain null listener dictionary. Logged
syscall286 ESRCH is gettid(no per-thread override), not missing process:
actual kern_prot.c explicitly defines that expected case. Avoid treating
all diagnostic errno lines as blockers. Bootloader/USERDATA unchanged.
0121 CI43756243470 running fromd640287. Package0061 session16037 waits for
success and exact source check; will preserve0060 loader/ADT/root and add
only a03_sandbox_disabled=1. No0061 flash until full build/package verified.

## 2026-11-15: requested cross-reference with other phone ports

Compared A5 historical8c3900f(0117), tracked HEROLTE0200/0201, exact SWEET
checkout45263be and HakiOS63fc2b4. Source/runtime matrix in
 docs/a03-userspace-cross-reference.md.
A5 same nil BaseBoard URL plus UMD atomic-save ENOTSUP; after0117 recovered
window has5BGRA swaps without those failures. A03 omits donor0052 HFS swap,
0057 external ACL resolver removal,0064 work-interval grant, and until0121
Sandbox0050 functionality. Actual generated Makefile has EXT_RESOLVER.
HakiOS XNU8796.121.2 vs our8796.141.3; broad Sandbox stub not copied.
Staged A03 SystemVersion confirmed16.0/20A362, not donor16.7.16/20H392.
Other repositories inspected only; no phone USERDATA write.

## 2026-11-15: scoped HFS atomic-swap candidate (0122)

Cross-reference established A5's same nil system-container NSURL/UMD ENOTSUP
pattern improved with donor HFS swap support. Prepared0122 using existing
HFS VNOP_EXCHANGE only after VNOP_RENAMEX returns ENOTSUP for exactly SWAP.
Requires two distinct regular vnodes on the same writable HFS root mounted
from /dev/a03userdata0, plus explicit a03_hfs_swap=1 AND a03emmc_rw=1.
Other mounts/flags/types/errors retain existing behavior; exchange errors
propagate. HFS journal/locking remain existing implementation.32 bounded
result logs. This does not rewrite the root image or add partition access.
Actual-source host gates/error/log tests PASS; real kpi_vfs.c arm64 kernel
compile PASS; exact patch application/source comparison PASS. Hardware
pending. Existing0121 CI43756243470/package0061 remain independent and
unchanged; do not enable swap in0061. New CI not started at this milestone.

## 2026-11-15: isolated Sandbox test BOOT0061 flashed

CI43756243470 SUCCESS fromd6402879ba93371caed2338256e86e1c78e867e3.
Kernel SHA25643cfd51d9940e6788b49b646325e113a90457890bc047ee5737159852ade4786.
Image SHA256a3976e921bf2be0f6c8e1b6259747a45702ab5283112452c399d074b919098bf.
Exact CI exception/USB/systemcalls/Makefile/AMFI source comparison PASS.
0060 loader(except image_size), ADT and root retained; only boot argument
addition a03_sandbox_disabled=1.0122 HFS fallback is NOT in this kernel.
Host already detected Download; BOOT-only upload100percent/success/reboot
confirmed20:21UTC. Capture190652 waits900s then100s through newgrp uucp.
Runtime result pending. No host USERDATA/protected-partition write.

## 2026-11-15: 0122 CI failure diagnosed; paused after correction

CI43757697658 from1d37d6c FAILED. Zero-context patch conversion038d3f1
was wrong for CI's git apply: the fallback call landed at file scope near
kpi_vfs.c6429, producing implicit-int and undefined flags/fvpp/tvpp/ctx.
Earlier local GNU patch equality did not exercise CI's application tool.
Restored three context lines in every hunk. Applied with plain git apply
in a fresh temporary repository: exact full-file equality against the
compiled candidate PASS. Actual-source scope tests and real kernel compile
rechecked. Added regression rejecting context-free hunks. No retry CI or
flash while user goal is paused. BOOT0062 was never packaged/flashed.

BOOT0061 initial100s capture completed372141bytes/5038LF lines SHA256
944d7ea11bc437d62f3f680760d17d136ae2fe93bc2f4f9e3e0a7eb5861d1d1f.
All four target processes show Sandbox op2 errno0; no CRASH records in this
window and one media/one backboard exec, versus two bounded crashes each
and three execs each in0060. This is bounded progress, not stable GUI proof.
UMD atomic-swap ENOTSUP45 persists twice. Unknown Sandbox op4 remains45.
Continuation capture45257 was started before pause; no reset requested.
