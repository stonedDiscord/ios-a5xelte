# A03 iOS16 service crash investigation

Evidence below comes from BOOT0075–0078 on the Galaxy A03. Private logs and
Apple artifacts remain outside git. These are separate failures; neither
successful kernel builds nor the physical Apple logo prove a home screen.

## analyticsd: ACL identity lookup, then a NULL tasking path

The actual failing calls are stat64 on the OSAnalytics system group's
Library/CoreAnalytics (EACCES 13), followed by open on Library (EACCES 13).
Path setup fails and CoreAnalytics later calls strlen(NULL). The container
path was returned successfully; initial container lookup is not the proven
failure.

BOOT0077's read-only ACL probe found Library mode 000, uid/gid -2, with an
inherited permit ACE for compatibility UUID abcdefabcdefabcdefabcdef0000012b
(GID 299, systemusers). Its container root has two permit ACEs for the same
group. This is intentional ACL-backed access, not justification for chmod.
The staged group database lists _analyticsd and mobile in systemusers.

CONFIG_EXT_RESOLVER is enabled, but no memberd/opendirectoryd job is staged.
Patch 0142 adds opt-in translation of the exact local UID/GID UUID format
already implemented by matching Libinfo and XNU's resolver-disabled branch.
It preserves membership and rights checks. Tests with the actual ACL evaluator
grant the captured rights only when supplied group 299 membership is present.
Live supplementary-group inspection remains pending; BOOT0078 service survival
is recorded below.
MobileActivation's backup-exclusion setxattr EACCES has the same ACL identity
dependency. CI 43963988043 builds this patch; BOOT0078 enables its boot argument.

## ScreenTimeAgent: missing data-vault conversion

Repeated terminating annotation: `Failed to enable data vault: Operation not
supported (45)`. The failing mac_syscall is Sandbox operation 0x104 with
`{int64_t fd; user_addr_t owner;}`, fd 3 and owner remotemanagementd. The signed
ScreenTimeAgent XML contains boolean entitlement
com.apple.rootless.storage.remotemanagementd. Dmd requests the same operation
with owner dmd and fails separately.

BOOT0077 live metadata for /private/var/mobile/Library/Application Support/
com.apple.remotemanagementd: uid/gid 501, directory mode 0755, flags 0, no ACL.
The guessed com.apple.dmd sibling returned ENOENT; that does not identify
dmd's actual directory. No metadata was changed.

The matching libsystem_sandbox code establishes additional ABI requirements:

- rootless_check_datavault_flag tests UF_DATAVAULT (0x80). With an owner
  argument it reads the com.apple.rootless xattr and compares its length and
  bytes to that owner.
- rootless_convert_to_datavault opens O_EVTONLY, sends operation 0x104, and
  only on success recursively traverses the tree and ORs 0x80 into BSD flags.
- HFS stores BSD flags and XNU inherits UF_DATAVAULT during child creation
  and relevant rename paths. Those mechanisms alone do not enforce vault
  entitlement access: this port has no implementation of that Sandbox policy.

Returning success from 0x104 alone would therefore omit owner metadata and
access enforcement. A future implementation must validate the descriptor and
owner entitlement, persist coherent owner/flag state on validated USERDATA,
handle repeat calls and partial errors, and define enforcement for descendants
and rename/link operations. No such implementation is claimed or enabled.

Reproduce the static ABI checks (read-only):

    python3 tools/a03-check-datavault-abi.py PATH_TO_MATCHING_HFS_ROOT_IMAGE

This script intentionally rejects a different instruction layout. It does
not execute Apple code or establish live protection behavior.

## BOOT0078 runtime follow-up

On 2026-11-16 at approximately 22:09 UTC, repeated ps observations retain
analyticsd PID 91 and MobileActivation PID 134; their sampled main threads
are in CF runloops. Earlier fatal access failures have not recurred in this
capture so far, while the original ACL metadata is unchanged. SpringBoard
progresses past its earlier activation wait, reaches UI layout, and the user
reports an iOS clock screen. This is not yet unlocked home-screen proof.
ScreenTimeAgent PID 121 was loading its CoreData model at that first sample,
but subsequently reached the same unsupported-vault assertion around 22:14 UTC
and restarted repeatedly. Its failure is not repaired by the identity change.
At 22:29 UTC a fresh capture still finds analyticsd 91, backboardd 56 and
SpringBoard 26. SpringBoard's main thread resolves to the UIApplication event
loop again. MobileActivation had changed from PID 134 to 467 earlier, without
a captured crash record, so unchanged PID or continuous survival is not claimed.
Generic PosterBoard crashes also appear; their cause is not yet established.

Patch 0144 prepares an explicitly labelled lab metadata compatibility path
for ScreenTime's exact owner/path, with entitlement, uid, root and normal
filesystem authorization checks. It writes real owner metadata/flags and
rejects relabels. It provides NO Apple vault access enforcement. It is not
staged, enabled or running on the phone. Preserve BOOT0078 while validating
the new UI checkpoint. Host fault-injection tests and local full-file Clang
checks cover this candidate only; they do not prove runtime behavior.
