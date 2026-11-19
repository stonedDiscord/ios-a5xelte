# DREAMLTE / Galaxy S8 SM-G950F — active handoff

## 0234 physical result: quiet resource path still times out — 2026-11-19

User reports from0234:
    SWEET USB: ep0 cmd 0x2 timeout
    DREAMLTE USB POLL: first=001b0048 last=001b0048 exit=001b0048 n=1000 wake=0
    SWEET USB: endpoint 0 setup failed

Removing framebuffer output between STARTCFG and resource allocation did
not advance initial EP0 SETTRANSFRESOURCE. CLK31 remained clear at every
sample and pre-log exit, and no wake was attempted. This rejects the added
inter-command printing as a sufficient explanation/fix; it does not prove
all timing effects impossible or that clocks/PHY are electrically healthy.
No endpoint-resource progress or working USB console.0234 remains installed.
Result recorded; user asks for an explanation of last change, not a new
flash. Next evidence-based candidate is read-only PMU isolation/reference
selector sampling; no register write policy or next CI selected yet.


0234 bounded host observation completed:60 sysfs samples over120.14s,
no1209:0001 at any sample. Evidence saved privately in exact-run directory
host-observation.json. Current physical screen result still pending; no
reflash/new build. Goal active, not achieved. Next action depends on0234
resources/running or failed-command/POLL report already requested.


## 0234 host absent; remaining PHY prerequisite audit — 2026-11-19

Previous goal turn made progress:0234 source compiled, exact CI passed and
verified BOOT flashed. This continuation rechecked installed artifact/source
hash and host: no1209:0001/ECM and no Download Mode; no live build/flash.
Physical0234 endpoint/POLL result remains pending; do not replace its BOOT
before observing the timing trial. Host absence alone cannot locate failure.

Source audit: the exact0234 kernel maps CMUs and PHY, but never maps/reads
PMU USB isolation0x16480704 or PHY reference selector0x10e5007c. Pinned
Samsung phy_power_on releases PMU bit0; change_refclk applies the DT-selected
bit24 reference path before CAL initialization. Their current hardware state
is unknown; configured CMU gates do not prove either prerequisite. If0234
repeats resource timeout, read these two prerequisites before changing them;
do not blindly add PLL/reference or isolation writes. Corrected old map's
USB user-mux busy bit16 to bit7 per pinned cmucal-sfr.c; top mux busy stays16.

Reachability clarification: in exact0233/0234 source, CMU prelog-exit is
printed only after ud_epcmd times out and resource_clock is true; that
predicate requires ep0/cmd2/PAR0=1/PAR1=PAR2=0. Thus the user's0233 prelog-exit
lines imply this timeout path by code inspection. The raw0233 cmd/POLL
values remain unreported; this inference must stay separate from observations.


## 0234 verified and BOOT flashed; timing trial result pending — 2026-11-19

Exact CI44509055685 SUCCESS at560236930010a5b7b80065f17100b1bb60ba7248.
11sources/9symbols/51diagnostics/profile verified PASS. Kernel SHA256
fd856fbdb4477fea6813235a5ee4e93b1703e7c817058df5b7695691050615cc.
BOOT shim/out/dreamlte-xnu-0234.img,18,464,784B,SHA256
98805c1984e2e9fb281cf43a79422f6b0246be34db875ac8602887d1930ff037.
Original BOOT components/header/payload/fit/hash PASS. Download Mode065
accepted BOOT100%; Heimdall exit0/reboot. Only BOOT written.
Artifacts, manifest and flash log research/dreamlte/ci-44509055685.
Host immediately post-flash has no1209:0001 or ECM. Physical result pending.
Requested resources/running or current failed-command/POLL; keep this boot
visible. No new CI/preparation/flash live. No USB console success claimed.


0234 CI44509055685 dispatched at560236930010a5b7b80065f17100b1bb60ba7248.
Actual ARM64 compilation, wrapper/EP/resource/CSR/wake/clocks/PIPE/console
models and exact0233-source patch equality PASS. New resource regression
rejects pre-command console output. Manifest11sources/9symbols/51strings.
Preparation research/dreamlte/prepare-0234.py verifies exact run/head and
packages original BOOT components; never flashes. Download Mode065 ready.
0233 remains installed until verified0234 image exists. No USB success.


## 0234 removes framebuffer delay in resource setup — 2026-11-19

0233 PIPE change latched but endpoint setup still failed. Pinned Samsung
gadget.c and upstream v6.12 have no console output between STARTCFG and
resource allocation. XNU printed STARTCFG, three CMU lines and resource
entry there.0234 defers STARTCFG output until resources complete and
removes entry printing. Read-only entry snapshot, pre-timeout capture,
command values/order, one-issue rule and failure/POLL/CMU output remain.
This tests timing/interference; it is not an established root cause.
No new clock, PHY, CMU, reset or DMA policy. Hardware untested.
Host sees fresh Samsung Download Mode device065; no new flash yet.


## 0233 physical PIPE bit28 latches; endpoint setup still fails — 2026-11-19

User confirms PIPE config010c0002->110c0002. CMU prelog-exit unchanged:
BUSMUX10 USBMUX10 QCH003f0003; ACLK/REF/SUSP00200000;
TOPMUX2 DIV7 GATE00200000; endpoint0 setup failed.
DIS_RXDETP3 setting matches saved Android PIPE state but does not resolve
endpoint setup. These enabled clock-register settings still do not measure
oscillation/PLL lock or prove DMA. Current failed-command/POLL not included;
do not silently treat an earlier build's cmd2 result as a0233 observation.
Reverified exact0233 CI SUCCESS/source/profile11/9/52 PASS; host no1209:0001
and no ECM interface.0233 installed. No new build/flash selected pending
remaining source/command audit. Preserve current boot and protected partitions.


## Host console success gate added;0233 physical result pending — 2026-11-19

Previous goal turn made progress: verified0233 BOOT flash, exact image and
handoff committed. Current recheck still no1209:0001 or Download Mode;
EP0 checker reports zero gadgets. No current phone console text or PIPE
readback supplied. Do not infer0233 repeated0231's cmd2 failure, or reflash
before its physical result. No live CI/flash.0233 remains installed.

Enhanced tools/dreamlte-usb-check.py with optional bounded --console-seconds
and --console-log: requires exact ECM identity, EP0 checks, ping and actual
identifiable XNU UDP text from192.168.7.2. Real loopback tests PASS for split
markers, data equality, empty/foreign/unrelated packets and timeout; CLI
rejects invalid duration/missing interface. Host-only change; no new kernel
or hardware claim. Working USB console remains unverified and goal active.


## 0233 verified and BOOT flashed; PIPE trial result pending — 2026-11-19

Exact CI44503956468 SUCCESS at63349a0f3aae1f34cc282465b28748a9f7a4b193.
Preparation2652 finished;11sources/9symbols/52diagnostics/profile PASS.
Kernel SHA256ca505ccd8d0cd6e7ae69717a2384360b4c4366ee8218501c67be533d1ea194be.
BOOT shim/out/dreamlte-xnu-0233.img,18,464,784B,SHA256
1cc6b8bb73f31da1a90e41a1dc449a4487f1bd4ceff449ee78124e8f2fd23486.
Original BOOT components/header/payload/fit/hash PASS. Fresh Download
Mode064 accepted BOOT100%; Heimdall exit0/reboot. Only BOOT written.
Exact artifacts/reviewed manifest/flash log research/dreamlte/ci-44503956468.
Host post-flash no1209:0001 or Download Mode; EP0 checker fails absence.
Requested PIPE config before/after and resources/running or failed command/
POLL from this same boot.0233 installed; physical bit28/readback and endpoint
progress unverified. No USB console success. No live CI/preparation/flash.
Preserve current boot until physical result; no non-BOOT partition write.


User clarifies WHEN READY was a joke and confirms Download Mode.
Host sees fresh04e8:685d device064.0233 CI44503956468/head63349a0
still building; preparation2652 waits exact artifacts. No handshake/flash.


0233 CI44503956468 dispatched at63349a0f3aae1f34cc282465b28748a9f7a4b193.
Preparation research/dreamlte/prepare-0233.py waits exact run/head,
verifies11sources/9symbols/52strings and packages; never flashes.
User says WHEN READY: signal after image verification; do not assume phone
is in Download Mode.0232 installed; physical0233 effects remain untested.


0233 candidate matches pinned Samsung core.c dwc3_core_config:
for revisions>=2.50a set GUSB3PIPECTL.DIS_RXDETP3(bit28). Previously
reported firmware PIPE010c0002 lacks it; saved configured Android dump
PIPE110c0002 has it. This is a real source/state difference, not proof of
the cause of resource timeout. Apply only on exact measured2.80a ID with
DCTL.RUN/CSFTRST clear and PIPE reset clear; set only28, require exact
readback. Insert after existing device reset, before endpoint setup.
No CMU/PMU/PHY tuning, clock-rate change, reset retry or command reissue.
Actual ARM64 compile PASS; new source-derived PIPE preservation/refusal
suite and wrapper/EP/resource/CSR/wake/clocks/console suites PASS. Plain
patch from exact0232 compiled source equals reviewed source. Manifest
11sources/9symbols/52strings.0232 installed; full0233 CI next, untested.


## 0232 physical CMU gates enabled; endpoint setup still fails — 2026-11-19

User reports exact prelog-exit snapshot:
BUSMUX=00000010 USBMUX=00000010 QCH=003f0003
ACLK=00200000 REF=00200000 SUSP=00200000
TOPMUX=00000002 DIV=00000007 GATE=00200000
followed by SWEET USB: endpoint 0 setup failed.
Pinned cmucal-sfr.c decodes user mux bit4=1; USB mux busy bit7=0;
ACLK/reference/suspend and top gate CG_VAL21=1; Q-channel enable0 and
CLOCK_REQ1 both set. TOPMUX selector2 names DIV_PLL_SHARED2_DIV2;
divider field7 is present. These are configured/enabled readbacks, not
measurements of clock oscillation, PLL lock, actual rate or DMA activity.
No evidence here supports blindly enabling these already-enabled gates.
Current0232 failed-command number/POLL were not supplied in this report;
0231 cmd2 timeout must not be silently promoted to a same-boot0232 fact.
Host still no1209:0001 gadget.0232 remains installed; no new flash/build.
Next audit command/core initialization against pinned Samsung source;
preserve current boot and all non-BOOT partitions. USB console not working.


## 0232 verified and BOOT flashed; clock-tree readback pending — 2026-11-19

Exact CI44498181713 SUCCESS at06cbc9be260d56e6be65e042cd5e96ab151335b3.
11sources/9symbols/50diagnostics/profile verified PASS. Kernel SHA256
eac30f38bf278fef6e1fdb53064ca560170884b87bbd36fb02f65806c86ebbe5.
BOOT shim/out/dreamlte-xnu-0232.img,18,464,784B,SHA256
cfd6796ea3d702e22c53ef05719ebb1d9327c4774b7ae147aad677a1fc16b9c0.
Original BOOT components/header/payload/fit/hash PASS. Fresh Download
Mode063 accepted BOOT100%; Heimdall exit0/reboot. Only BOOT written.
Artifacts/reviewed manifest/log research/dreamlte/ci-44498181713.
0232 installed; no host1209:0001 or Download Mode after flash; checker
fails gadget absence. Requested three CMU prelog-exit lines, or last
persistent line if earlier stop. This trial adds read-only clock snapshots,
not a proven endpoint fix. Physical clock reads and USB console unverified.
Keep current boot visible. No live CI/preparation/flash; no Android restore.


User confirms fresh Download Mode ready; host sees04e8:685d device063.
0232 exact CI44498181713/head06cbc9b still Build in progress. Preparation
16096 waits exact artifacts; no handshake or flash yet. Preserve fresh mode.


0232 CI44498181713 dispatched at06cbc9be260d56e6be65e042cd5e96ab151335b3.
Preparation research/dreamlte/prepare-0232.py waits exact head/run,
verifies11sources/9symbols/50strings and packages, never flashes.
Fresh Download Mode requested;0231 installed, no0232 physical test yet.
0231 host watcher ended after20min with no matching ECM interface.


0232 adds read-only nine-register USB clock-tree snapshots from pinned
cmucal-sfr.c: FSYS0 BUS/USB user mux, USB ACLK/reference/suspend gates,
USB link Q-channel; top USB mux/divider/gate. Only after opt-in2, correct
DWC3 ID and stopped-core check are CMU windows mapped. Capture at resource
entry and before any timeout console printing; print saved values only.
No new clock/gate/PHY/PMU/reset writes or endpoint reissue. New CMU mapped
reads are source-supported but not yet tested on the phone.
Actual ARM64 object and new source-derived CMU offset/base/order/read-only
model PASS; existing wrapper/EP/resource/CSR/wake/console models PASS.
Plain overlay from exact0231 source matches reviewed source. Manifest
11sources/9symbols/50strings.0231 installed. Next full CI, then verified
BOOT-only trial; physical0232 snapshots/USB functionality untested.


## 0231 physical bus match; first resource cmd2 still times out — 2026-11-19

User confirms bus bursts22220001->22220009, then ep0cmd0x2 timeout.
POLL first=001b0048 last=001b0048 exit=001b0048 n=1000 wake=0.
The Samsung INCR16 setting latches but does not resolve first resource.
CLK31 stays clear across all1000 sampled polls and pre-log exit; no wake
was triggered. Stop treating later failure-dump bit31 as the sampled cause.
No1209:0001/ECM interface or working console.0231 remains installed.
Next read the pinned FSYS0/upstream USB clock mux/gate/Q-channel state
at resource entry and timeout before console output; no blind gate writes.
Do not request another identical full DWC3/PHY dump.


## 0231 exact CI passed; BOOT flashed; USB still absent — 2026-11-19

CI44493674078 SUCCESS at5b94db771f4c1404e3400cded1796cabd85466d9.
Exact11-source/9-symbol/47-diagnostic/profile verification PASS, including
linked RAM readers and UDP sender. Kernel SHA256
2e28df029b20dc6cea6c8d867de0dddb5918a98b589ed3526beeaaf94725a202.
BOOT shim/out/dreamlte-xnu-0231.img,18,464,784B,SHA256
780144a38c5e180c7014a777053c81e8cbffa2ebe4350daf94162cd5518f4222.
Original BOOT components/header/payload/fit/hash PASS. One buildtree TLS
transfer failed, preserved privately; exact-run retry verified successfully.
Fresh Download Mode062 accepted BOOT100%; Heimdall exit0/reboot. Only
BOOT written. Artifacts/manifests/flash log research/dreamlte/ci-44493674078.
0231 installed. Host post-flash no1209:0001 ECM gadget or Download Mode;
EP0 checker fails absence. Requested physical bus-bursts readback and
resources/running or command/POLL result. No working USB console claimed.
Host watcher11376 is bounded20min and captures only exact ECM identity;
its log research/dreamlte/check-0231-host.log. Assigning host IP may require
user sudo (host sudo-n unavailable); do EP0 check first if gadget appears.
Do not reboot current0231 before its physical result; no live CI/flash.


0231 CI44493674078 dispatched at5b94db771f4c1404e3400cded1796cabd85466d9.
Preparation research/dreamlte/prepare-0231.py waits exact run/head,
verifies11sources/9symbols/47strings and packages, never flashes.
Host confirms fresh Download Mode062; no handshake/flash yet.0230 remains
installed. Await exact build verification, then authorized BOOT-only trial.


## 0230 physical pre-log clock awake;0231 console/bus candidate — 2026-11-19

User reports exact POLL first=001b0048 last=001b0048 exit=001b0048
n=100 wake=0. Preserve n=100 as supplied; verified0230 code loops1000
samples, so count transcription differs and is not silently normalized.
CLK31 is clear at all reported pre-log samples; no in-command wake fired.
Thus later failure-dump bit31 is not evidence of suspend during the sampled
command. This trial does not establish the remaining clock tree or DMA.

0231 enables the previously excluded UDP5140 log sender using bounded S8
RAM-trace readers, without donor UFS/disk dependencies. Reader supports
empty/invalid/saturated cursors, bounded chunks, no printf or allocation.
Sender commits its cursor only after a full successful send; failed/short
sends retry the same chunk. Physical network delivery remains unverified.
Also applies pinned Samsung core.c dwc3_core_config INCR|INCR16 burst
setting after device reset: measured22220001 becomes22220009, matching
saved Android regdump. All AXI cache fields preserved. This source-backed
bus prerequisite is a hypothesis for resource progress, not a proven fix.
No new PHY/CMU/PMU/mux policy and no repeated reset/command reissue.

Actual ARM64 objects for both edited units PASS; nm confirms RAM-reader
exports and USB sender with no sweet_log/sweet_ufs imports. Actual reader/
sender model checks full/error/short transfers and byte equality; bus-bit
preservation, wrapper/EP/resource/CSR/wake models PASS. Plain overlay from
exact0230 compiled sources equals reviewed source. Manifest11sources/
9symbols/47strings.0230 stays installed; fresh Download Mode requested.
Full0231 CI next; no0231 flash or USB success yet.

## 0230 verified and BOOT flashed; pre-log POLL trace pending — 2026-11-19

Exact CI44486941058 SUCCESS at105d9746d00b514d1779bab9cecacbc89c5255f2.
Resumed exact preparation;11sources/6symbols/46diagnostics/profile PASS.
Kernel SHA25655f67792aaa1989cda7e7905ba1451b062a51b96c1c8d8fcbbce2f1e57f84644.
BOOT shim/out/dreamlte-xnu-0230.img,18,464,784B,SHA256
7fd09f38c3c4f1e8dd4e35794efdb0f1679d78975742e1369efa466e9d45a8e9.
Original BOOT components/header, payload, partition fit and hash PASS.
Fresh Download Mode061 accepted BOOT100%; Heimdall exit0/reboot. Only
BOOT written. First sandbox attempt failed before protocol/device open,
wrote nothing; authorized host-access retry succeeded. Logs and reviewed
manifest: research/dreamlte/ci-44486941058. Preparation resume log private.
Host post-flash no1209:0001 gadget or Download Mode. Requested new POLL
first/last/exit/n/wake line and any suspend/wake refusal, not old full dump.
0230 installed; physical effect/USB console unverified. No live CI/flash.
Keep this boot visible while waiting for its diagnostic evidence.

0230 CI44486941058 dispatched at105d9746d00b514d1779bab9cecacbc89c5255f2.
Preparation55579/script research/dreamlte/prepare-0230.py waits exact
run/head, downloads/verifies11sources/6symbols/46strings and packages;
never flashes. Log research/dreamlte/prepare-0230.log. Fresh Download Mode
requested; no more0229 trace needed.0229 installed;0230 hardware untested.


## 0229 full fault unchanged; active-wake outcome unreported — 2026-11-19

User reports cmd2 timeout/reg402/PAR0=1/PAR1/2=0; GCTL80e92004
GSTS3e800000 USB2=40102400 DCTL0 DSTS00520000 EN0;
CORE PIPE010c0002 HW3=10420085 BUS22220001/300; DCFG80800 HW1=0160c93b;
EVT82ca6000/000000008/80001000/0 (transcribed high word numerically8);
TEST0 PHYPIPE10 LINK08000180 UTMI660 CLK801b0048 Q7e00 SEL0.
No resource suspend/wake lines were included; do not infer they never ran.
User notes the same failure values repeated six times;0229 did not resolve
resource setup. Exact CI/source verification repeated PASS. Host no gadget.

Audit finds failure PHY reads occur after timeout print and eight snapshot
prints. Thus CLK31 at failure does not establish its value during polling;
console delay can separate those observations. ARM64 object retains actual
volatile CLK reads and bit31 branch. Next diagnostic captures first/last/
exit CLK and wake count before any timeout logging, prints one summary
after the fault dump. No new PHY policy/register write selected.0229 stays
installed until a verified BOOT-only next trial; preserve current boot.


0230 diagnostic captures first/last/exit CLK and sample/wake counts before
any timeout printing, emits one POLL summary after the fault snapshot.
Retains0229 one-shot wake policy; adds read-only observations, no new PHY
register policy. Source-derived model explicitly simulates bit31 changing
during timeout console output and verifies pre-log samples stay clear.
ARM64 object compile, wrapper/EP/resource/CSR/wake suites PASS; plain
patch/full-source equality PASS. Manifest11sources/6symbols/46strings.
0229 exact source manifest archived. Full CI next;0229 installed.


## 0229 partial physical trace: resource entry awake — 2026-11-19

User reports:

    DREAMLTE USB: post-reset wake CLK=001b0048->001b0048 PIPE=00000010
    DREAMLTE USB: resource-entry CLK=001b0048

Post-reset helper again makes no clock change; CLK31 is clear immediately
before first EP0 transfer-resource parameter/CMDACT writes. In this build
resource-entry occurs after STARTCFG returns success. No resource-suspend
poll, in-command wake, completion or timeout result has yet been supplied.
Do not infer those diagnostics absent, a hang, or a successful wake from
this partial report. Host recheck finds no1209:0001 or Download Mode.
Asked whether resource-entry is the final persistent line or what follows.
0229 remains installed/visible; no new build or phone write selected.


## 0229 verified and BOOT flashed; active-command wake trace pending — 2026-11-19

Exact CI44483460784 SUCCESS at168c141d7c3170de929f5f0242f2e79c7bea5d5c.
Preparation96832 complete;11sources/6symbols/45diagnostics/profile PASS.
Kernel SHA25692591f27bf78f4b5cef06bf57f60530391491ac61ef2f7d6020407e2d6c46ac3.
BOOT shim/out/dreamlte-xnu-0229.img,18,464,784B,SHA256
3057c7df5adad8230c597cd88500ffa186e549c2ae51c2a4d939775b0ebbc95f.
Original BOOT ramdisk/second/DT/header fields, fit and independent hash PASS.
Fresh Download Mode060 accepted BOOT100%; Heimdall exit0/reboot. Only
BOOT written. Exact artifacts/reviewed source manifest/flash log:
research/dreamlte/ci-44483460784. Private prepared manifest marked flashed.
Post-flash host no1209:0001 gadget or Download Mode device. Requested
resource-entry CLK, first suspend poll, guarded wake and resource/running
or timeout/failure PHY lines. Physical effect pending; no USB success.
0229 installed; no live CI/preparation/flash. Preserve current visible boot.
No Android, USERDATA or protected-partition write.


## 0228 complete fault: CLK31 returns after endpoint entry — 2026-11-19

User same-boot trace: STARTCFG reg9 completed; ep0cmd2 timeout/reg402;
PAR0=1/PAR1=0/PAR2=0; GCTL80e92004 GSTS3e800000 USB2=40102400;
DCTL0 DSTS00520000 EN0; CORE PIPE010c0002 HW3=10420085
BUS22220001/300; DCFG80800 HW1=0160c93b;
EVT82ca6000/000000008/80001000/0 (high word numerically8);
TEST0 PHYPIPE10 LINK08000180 UTMI660 CLK801b0048 Q7e00 SEL0.

CLK31 was clear at endpoint entry and set at the failure snapshot.
Thus0228 narrows the transition to after endpoint-entry; it does not
identify exactly when, which agent changes it, or prove it causes cmd2
failure. Clearing it only after DCTL reset did not resolve resource setup.
Next candidate will observe the first resource command and try at most
one guarded Samsung CAL bit31 clear while that same command is active;
never reissue an active command or loop controller reset. Preserve other
PHY fields and existing reset/mux/free-clock guards. No USB success.


0229 candidate observes first EP0 resource entry and each active-command
poll until first CLK31 assertion. At most once it calls the existing
post-reset wake helper (strict reset/mux/free-clock/all-ones guards,
clear only31,500us,exact readback), then keeps polling the same command.
It never reissues parameters/CMDACT or resets the controller. A failed
wake refuses immediately; repeated suspend does not cause repeated writes.
This is a causal experiment based on0228 transition, not a proven fix.
Actual ARM64 object compile, wrapper/EP/resource/CSR models and new
source-derived resource-wake suite PASS; plain overlay/full-source equality
PASS. New model tests immediate/delayed suspend, completion, persistent
readback/recurrent suspend, guards, unrelated endpoints and four command
writes only. Manifest11sources/6symbols/45diagnostics;0228 manifest archived.
0228 installed. Asked fresh Download Mode; full CI next. No new flash.


0229 full CI44483460784 dispatched at168c141d7c3170de929f5f0242f2e79c7bea5d5c.
Preparation96832/script research/dreamlte/prepare-0229.py waits exact
run/head, downloads, verifies11sources/6symbols/45strings and packages;
never flashes. Log research/dreamlte/prepare-0229.log. Fresh Download Mode
request pending;0228 installed. Physical0229 effect untested.

User confirms fresh Download Mode ready. Host sees04e8:685d at device060.
0229 exact CI44483460784/head168c141 still building; preparation96832
continues waiting exact run. No protocol handshake or flash yet. Preserve
fresh mode for verified BOOT-only upload when build/image checks finish.



## 0228 STARTCFG succeeds; first resource command times out — 2026-11-19

User follows the awake-clock checkpoints with exact text:

    DREAMLTE USB: STRATCFG completed reg=00000009
    SWEET USB: ep0 cmd 0x2 timeout

STRATCFG is the user's transcription; compiled marker is STARTCFG.
STARTCFG completes with reg9, then the first EP0 SETTRANSFRESOURCE command
still times out. CLK31 was clear at endpoint entry; the0228 failure-time
CLK/PAR/core snapshot has not yet been supplied. This rules out a stop at
the reset-wake guard or STARTCFG for this boot, not later clock gating.
No resources assigned or working USB established. Review command/core
initialization against pinned Samsung source;0228 remains installed.


## 0228 physical clock checkpoints — 2026-11-19

User reports from installed0228:

    DREAMLTE USB: pre-reset CLK=001b0048 PIPE=00000010 TEST=00000000
    DREAMLTE USB: post-reset wake CLK=001b0048->001b0048 PIPE=00000010
    DREAMLTE USB: endpoint-entry CLK=001b0048 PIPE=00000010 TEST=00000000

CLK31 remains clear at these three checkpoints, free UTMI clock stays
selected and TEST power-down bits stay clear at pre-reset/endpoint-entry.
The post-reset helper performs no CLK write for this sample: before equals
awake. Thus this report does not reproduce0227's later CLK31 reassertion
or show that the new clear fixed an endpoint. Endpoint-entry is printed
before STARTCFG; command completion, resources and USB remain unverified.
Host recheck sees no1209:0001 gadget or Download Mode device. Requested
following STARTCFG/resources/running or timeout/failure/PHY lines from this
same boot. Keep0228 visible; no new candidate, flash or partition write.


## 0228 verified and BOOT flashed — 2026-11-19

CI44477847371 SUCCESS at b7c84d8154cf734dfdb41fbfcf1b178e144690ab.
Preparation76070 complete;11 sources/6 symbols/42 diagnostics/profile PASS.
Kernel SHA256 c67861458b1e82317dd95e791763010a8c71fae4bb0359c7eecf3a0eb711cda7.
BOOT shim/out/dreamlte-xnu-0228.img,18,448,400B,SHA256
0092510b75f8b05e7ea1fc733d1d587a7d16b9e2ccf7309bf96f32084fceedfd.
Original BOOT components/header preserved; fit/independent hash PASS.
Fresh Download Mode059 accepted BOOT100%; Heimdall exit0/reboot.
Only BOOT written. Exact artifacts/reviewed source manifest/flash log:
research/dreamlte/ci-44477847371. Private prepared manifest updated.
Post-flash host: no1209:0001 gadget; lsusb also shows no Download Mode.
Physical pre-reset/post-reset wake/endpoint-entry clock and first command
trace requested, pending. No USB functionality established.0228 installed;
no live CI/preparation/flash. Next act on same-boot physical trace.
No Android or non-BOOT partition write.


## 2026-11-19:0227 free clock retained, link-controlled suspend returns

- User0227 physical: ep0cmd2 timeout/reg402/PAR0=1/PAR1=0/PAR2=0;
  GCTL80e92004 GSTS3e800000 USB2=40102400 DCTL0 DSTS00520000 EN0;
  CORE PIPE010c0002 HW3=10420085 BUS22220001/300; DCFG80800 HW1=0160c93b;
  EVT82ca8000/000000008/80001000/0 as transcribed (high word numerically8);
  PHY TEST0 PIPE10 LINK08000180 UTMI660 CLK801b0048 Q7e00 SEL0.
-0227 proceeds through the retention guard and power-up into endpoint
  setup. Free UTMI clock remains selected, power-down bits remain clear,
  but first resource command still active. No USB functionality established.
-CLK bit31 EN_UTMISUSPEND is set again at failure although clock helper
  requires it clear before returning. Exact point of restoration unknown:
  power-up, device reset or later hardware action. Source contains no later
  explicit CLK write. Next inspect/reassert only this Samsung CAL wake bit
  after device reset and add pre/post-reset snapshots to distinguish timing.
- No host gadget/Download Mode at inspection;0227 installed. No live CI,
  preparation or phone write. Preserve all non-BOOT partitions.


-0228 candidate clears only EN_UTMISUSPEND(bit31) after DCTL reset and
  existing core timing, preserves all other CLK bits, waits500us, requires
  exact readback. Refuses asserted port reset/nonprimary mux/missing free
  clock/all-ones registers. Adds pre-reset and endpoint-entry CLK/PIPE/TEST
  snapshots to locate restoration. No new reset/PLL/reference/mux sequence.
- Actual ARM64 object compile, wrapper/EP/resource/CSR suites and plain
  overlay/full-source equality PASS. Modeled bit31 restore cleared, all
  unrelated bits preserved; forced readback reassertion and reset/mux/clock
  refusal stop.11sources/6symbols/42strings.0227 own manifest archived.
  Fresh Download Mode059 confirmed; no handshake/flash. Full CI next.


- Full0228 CI44477847371 atb7c84d8 dispatched. Preparation76070/script
  research/dreamlte/prepare-0228.py waits exact head/run, downloads,
  verifies11sources/6symbols/42strings and packages; never flashes.
  Fresh Download Mode059 untouched. No physical0228 effect claimed.

## 2026-11-18:0227 verified and BOOT flashed; continuation trace pending

- Exact CI44331761587 SUCCESS atb11e4f62e81cfb01eeef11d27c1fce7244c473b9.
  Preparation15325 completed.11 sources/6 symbols/38 diagnostics/profile
  PASS. Kernel SHA256d0b770e5d09c70d287a7bd7c3d0a0ce101a3a940490e1e2bbd096430936a5ca0.
- BOOT shim/out/dreamlte-xnu-0227.img,18,448,400B,SHA256
  08c9565fdac4d803fdef4434e720d51c0ffe15f84479024d3d69f3ce00ff8dbb.
  Original BOOT components/header preserved; fit/independent hash PASS.
- Fresh Download Mode058 accepted BOOT100%, Heimdall exit0/reboot.
  Only BOOT written;0227 installed. Exact artifacts/source manifest/flash
  log research/dreamlte/ci-44331761587.
- Requested full clock/power/resource/FAIL trace. Predicted continuation
  after bit4 mismatch remains physically unverified; USB remains unverified.
  No live CI/prep. No Android/USERDATA/protected-partition write.

## 2026-11-18:0226 clock trial stopped at RETENABLEN readback;0227 continuation

- User reports only line PHY clock CLK=801b0049->001b0048
  PIPE=00000000->00000010, then no later USB output. The0226 function's
  exact after != awake guard rejects solely bit4 (RETENABLEN) not latching,
  so it returns before PHYTEST power-up/DWC3 endpoint setup. This report is
  not evidence of a cmd failure in0226.
-0227 retains all0226 writes and strict checks of port reset, common/ref SSP
  controls and free UTMI clock. It tolerates bit4 readback difference while
  logging it; preserves source-requested bit4 write. Thus tests whether the
  hardware can proceed through measured power-up/resource setup without
  weakening reset/PIPE checks. No additional clock/PHY register writes.
- Actual ARM64 object recompile PASS; wrapper models now explicitly simulate
  ignored bit4 and assert continuation, as well as the exact observed sample
  and existing refusal paths; EP/resource/CSR suites PASS. Plain patch/full
  source equality PASS. Manifest11 sources/6 symbols/38 strings.0226 own
  manifest already archived. Installed0226; request fresh Download Mode;
  no0227 CI/flash yet, no USB functionality claim.


- Full0227 CI44331761587 atb11e4f6 dispatched. Preparation15325/script
  research/dreamlte/prepare-0227.py waits exact head/run, downloads,
  verifies11sources/6symbols/38strings and packages; never flashes.
  Request fresh Download Mode; do not overwrite current physical evidence.

## 2026-11-18:0226 verified and BOOT flashed; clock trace pending

- Exact CI44324136923 SUCCESS at42d14a1dc97111ef63ee395158ff48e9e3ab60b7.
  Preparation44451 completed exact downloads/source verification/packaging.
  11 sources/6 symbols/38 diagnostics/profile PASS. Kernel SHA256
  b20ffad5cdf626b3166e24b46fa8214dab0b7e5539b696972f835eb3a1bbda5f.
- BOOT shim/out/dreamlte-xnu-0226.img,18,448,400B,SHA256
  a66f43216e55fbe89766809bcb1810cc065ee8d5c8d89e2417894274c93c2142.
  Original BOOT components/header preserved; fit/independent image hash PASS.
- User confirmed Download Mode; host fresh057 accepted BOOT100%, Heimdall
  exit0/reboot. Only BOOT written;0226 installed. Exact artifact/reviewed
  manifest/flash log research/dreamlte/ci-44324136923.
- Requested PHY clock before/after, PHY power, first resource command and
  failure CSR/PHY lines. Predicted CLK001b0058/PIPE10 remain unverified.
  USB functionality unverified; no live CI/preparation. No Android restore,
  USERDATA or protected-partition write.

## 2026-11-18:0225 power awake but cmd2 stuck;0226 common/free clock trial

- User exact0225: ep0cmd2 timeout/reg402, PAR0=1/PAR1/2=0;
  GCTL80e92004 GSTS3e800000 USB2=40102400 DCTL0 DSTS00520000 EN0;
  PIPE010c0002 HW3=10420085 BUS22220001/300; DCFG80800 HW1=0160c93b;
  EVT82cad000/000000008/80001000/0 as transcribed (extra high-word zero
  retained as text, numerically8); TEST0/PHYPIPE0; LINK08000180 UTMI660
  CLK801b0049 Q7e00 SEL0. Power clear alone did not advance first resource.
- Pinned Samsung8895 get_phyinfo selects version01.1.1,CLKCORE and
  common_block_disable=false. CAL ss_enable clears CLK bits31/0, sets
  RETENABLEN4/REF_SSP_EN19 and PHYPIPE free-clock bit4 under PORTRESET;
  outer enable waits10us then releases reset before power release.
-0226 applies these controls on strict observed primary mux/CLKCORE only,
  preserving reference selector/frequency, divider, PLL and SSC tuning.
  Adds500us settle and exact readbacks; predicts CLK801b0049->001b0058,
  PHYPIPE0->10. Does not map/write secondary banks/CMU/PMU or change mux.
  This is a source-supported hypothesis, not demonstrated clock readiness.
- Actual ARM64 compile; wrapper/EP/resource/CSR suites; plain patch equality
  PASS. Wrapper covers both layouts, unrelated bit preservation, physical
  sample, wrong reference/reset/mux/all-ones refusal. Manifest11sources/
  6symbols/38strings.0225 own reviewed manifest archived. Full CI next;
 0225 installed, physical Download Mode request sent, no new flash.


- Full0226 CI44324136923 at42d14a1 dispatched. Preparation44451/script
  research/dreamlte/prepare-0226.py waits exact head/run, downloads,
  verifies11sources/6symbols/38strings and packages; never flashes.
  Download Mode request pending. No physical0226 effect claimed.

## 2026-11-18:0225 PHY power release confirmed; exact endpoint fault pending

- User reports PHY power TEST0000000c->00000000 SEL00000000 and
  subsequent power snapshot TEST00000000 PIPE00000000, followed by
  endpoint0 setup failed. Thus targeted power-bit release physically
  succeeded and stayed clear through the reported failure snapshot.
- This does not establish PHY clock/PLL readiness or working endpoints.
  Current0225 failed command/status/PAR/core snapshot not yet supplied;
  requested exact ep0 command and USB FAIL lines from this same boot.
  Do not carry0224 cmd2 failure forward as an observed0225 command.
- Host currently no1209:0001/no Download Mode. No live build/preparation/
  flashing processes, new candidate or phone write. Installed0225.
  Continue pinned-source clock/reset review while awaiting exact fault.


- Reverified installed0225 exact artifact PASS:11 source hashes/6 symbols/
  36 diagnostics/active profile. Source review finds further CAL setup
  differences: ss_enable clears PHYCLKRST EN_UTMISUSPEND(bit31), applies
  version-dependent COMMONONN(bit0), enables RETENABLEN(bit4), and sets
  PHYPIPE PHY_CLOCK_SEL(bit4). Last measured CLK801b0049/PIPE0 differ, but
  these are coupled reference/reset-path controls, not proof of next cause.
  Do not apply an isolated clock-selection write before current command
  trace and required reference/reset sequencing are established.

## 2026-11-18:0225 verified and BOOT flashed; PHY wake trace pending

- Exact CI44316294206 SUCCESS at6943dd9061b0993cdcbd5917e9260547303e43b3.
  Preparation14190 completed downloads/verification/packaging.11 sources,
  6 symbols/36 diagnostic strings/active profile PASS. Kernel SHA256
  a97dc9b6b188ee9467c831f53c624f8934dfbbfb07c0c2133d08ab0c376e492b.
- BOOT shim/out/dreamlte-xnu-0225.img,18,448,400B,SHA256
  5e947432783858d583842bd83025cea68d7f3cebf30565bedddf72115aaebf79.
  Original BOOT components/header preserved; fit/independent image hash PASS.
- User confirmed Download Mode; host fresh056 accepted BOOT100%, Heimdall
  exit0/reboot. Only BOOT written;0225 installed. Exact artifacts/reviewed
  source manifest/flash log research/dreamlte/ci-44316294206.
- Requested PHY power TEST before/after plus resources/running or failure
  lines, or last3 if earlier stop. Predicted c->0 and endpoint progress not
  yet physically confirmed. No live CI/preparation remains; USB unverified.
  No Android restoration, USERDATA or protected-partition write.

## 2026-11-18:0224 PHY power-down confirmed;0225 primary wake candidate

- User supplies omitted0224 lines: DCFG00080800 HW1=0160c93b;
  EVT82cad000/00000008/80001000/00000000; PHY TEST0000000c PIPE00000000.
  Pinned Samsung header defines PHYTEST bits2/3 as POWERDOWN_HSP/SSP.
  Both asserted despite reset/sleep clear. This is a concrete missing
  prerequisite, not proof that clearing it alone solves endpoint execution.
-0225 follows exynos_cal_ss_power_down(info,1): clear only primary PHYTEST
  bits2/3, settle1000+500us, readback exact preserved fields. Supports only
  observed SEL lower6bits0; refuses other mux/reset selections/all-ones
  TEST. Existing QACT/link reset precedes power release; existing session/
  device reset follow. Post-reset power bits must remain clear or stop.
  No PLL/reference/port mux/CMU/PMU/secondary bank changes.
- Actual ARM64 object compile, wrapper/EP/resource/CSR suites PASS. Wrapper
  tests both register layouts, all32 unrelated bit preservation, observed
  c->0 and mux/all-ones refusal. Plain overlay/full-source equality PASS.
  Manifest11 sources/6 symbols/36 diagnostics;0224 own manifest archived.
- Installed0224; no host gadget or Download Mode. Asked user to return to
  Download Mode while full0225 CI builds. No new phone write yet.


- Full0225 CI44316294206 at6943dd9 dispatched. Preparation14190/script
  research/dreamlte/prepare-0225.py waits exact head/run, downloads,
  verifies11 sources/6 symbols/36 strings and packages; never flashes.
  Keep current physical evidence separate from predicted TESTc->0.

User confirms Download Mode ready; host sees fresh056/04e8:685d. No
handshake or flash before0225 verification. CI44316294206 still running.

## 2026-11-18:0224 event CSR and STARTCFG physically verified

- User reports0224 session LINK08000180/UTMI660 before endpoints; event
  CSR verified DMA82cad000/00000008,size80001000. This verifies register
  readback of owned event-ring setup, not bus-master DMA or host traffic.
- STARTCFG completed reg00000009. First EP0 SETTRANSFRESOURCE remains
  active00000402 with PAR0=1/PAR1=0/PAR2=0. GCTL80e92004 GSTS3e800000
  USB2=40102400; DCTL0,DSTS00520000,EN0; PIPE010c0002 HW3=10420085
  BUS22220001/300; PHY LINK08000180 UTMI660 CLK801b0049 Q7e00 SEL0.
  Initial ID5533280a/GCTL30c12004/DSTS00520004, PHYversion10000,
  CLK801b0049/UTMI60; link wake Q7e00/LINK08000000/SEL0;
  soft reset1ms/DCFG80804. Endpoint0 setup failed; no USB success.
- Submitted trace omits the new USB CSR and USB POWER lines between CORE
  and PHY. Requested those exact lines or explicit absence. Their values
  remain unknown; do not infer powered PHY from cleared sleep/reset bits.
- Installed0224; host no gadget/Download Mode at inspection. No live CI,
  new candidate or flash. Continue source review while awaiting missing
  readbacks; do not repeat identical diagnostic flash or change power blindly.


- Reverified installed0224 exact CI artifact:11 complete source hashes,
  6 symbols/33 diagnostics/profile PASS. Linked CSR/POWER strings and staged
  failure helper contain both requested lines. Their omission from submitted
  text does not establish absence on screen. Source comparison confirms
  Samsung start_config sends STARTCFG then SETTRANSFRESOURCE(param0=1,
  param1/2=0) before SETEPCONFIG, matching this trial. No basis to revert
  resource order or claim malformed parameters from the current trace.

## 2026-11-18:0224 verified and BOOT flashed; CSR/power trace pending

- Exact CI44308837527 SUCCESS at2c39e75540432a9fd362c9f605543a2224c96deb.
  Preparation87930 completed exact-run downloads, source verification and
  packaging.11 sources/6 symbols/33 diagnostics/active profile PASS.
  Kernel SHA256d3d0cce0dfd55ed54e5ff75b09840ee1d9a499dc4e65ba380a90984f829d019e.
- BOOT shim/out/dreamlte-xnu-0224.img,18,448,400B,SHA256
  973887c7ac074f6789f75bca5849865372ac3ab1400b617e00e98adbedad8c58.
  Original ramdisk/second/DT/header preserved; fit/independent hash PASS.
- Fresh Download Mode055 accepted BOOT100%, Heimdall exit0/reboot;0224
  installed. Only BOOT written. Private exact artifacts/reviewed manifest/
  flash log research/dreamlte/ci-44308837527. No live CI/preparation remains.
- Requested event CSR verified/mismatch, STARTCFG completed, USB CSR and
  USB POWER lines (or last3 lines on earlier stop). Physical outcome pending;
  USB functionality unverified.0223 session-valid retained but resource
  cmd2 stuck remains last physical USB evidence. No Android/USERDATA writes.

## 2026-11-18:0223 reaches USB; session-valid confirmed, resource still stuck

- User physical0223 trace reaches USB, superseding phase5 as the current
  visible stopping point. This does not explain0222's earlier phase5 report.
- ID5533280a GCTL30c12004 DSTS00520004; PHYversion00010000 CLK801b0049
  UTMI60; link wake Q7e00 LINK08000000 SEL0. Reset1ms/DCFG00080804.
  USB2CFG40102400/GCTL80e92004; EP0 resource cmd2 times out reg402,
  PAR0=1/PAR1=0/PAR2=0; GSTS3e800000 DCTL0 DSTS00520000 EN0.
  CORE PIPE010c0002 HW3=10420085 BUS22220001/00000300.
  Failure PHY LINK08000180 UTMI00000660 CLK801b0049 Q7e00 SEL0.
- Session-valid override bits physically retained through failure, unlike
  earlier LINK08000000/UTMI60. That ordering change alone does not resolve
  first transfer-resource command. STARTCFG returns; resource CMDACT stays
  set. No enumeration/control/data success. Installed0223; no new writes.
- Next compare remaining controller configuration/reset/clock prerequisites
  with pinned Samsung sources before selecting another narrowly tested trial.


-0224 diagnostic candidate verifies real event-ring address/size CSR
  readback before endpoint commands, stopping on mismatch without retry.
  Adds failure DCFG/HW1/event ring plus PHYTEST/PHYPIPE reads and completed
  STARTCFG register. No new clock/power/reset programming. Actual ARM64,
  wrapper, EP/resource/CSR guard suites PASS; plain patch/full source PASS.
  CSR tests cover32/64-bit addresses and each mismatch. Manifest11 sources/
  33 diagnostics;0223 own reviewed manifest already archived. Full CI next.


- Full0224 CI44308837527 at2c39e75 dispatched. Preparation87930/script
  research/dreamlte/prepare-0224.py checks exact head, waits same run,
  downloads each artifact into clean transfer destination on terminal
  errors, verifies11 sources/6 symbols/33 strings and packages; never
  flashes. Fresh Download Mode055 untouched. No USB success claimed.

## 2026-11-18:0223 verified and BOOT flashed; VM trace pending

- Exact CI44298522029 SUCCESS at d5f6472b35b456acbaa95c0716be23533066a2ea.
  Original preparation26124 exited terminally on TLS artifact download;
  retry70483 hit existing kernel-file collision after network errors.
  Narrowed buildtree-only preparation25298 completed; no replacement CI.
- Eleven actual sources/six symbols/twenty-eight diagnostics/active profile
  PASS. Kernel SHA25632291c02b546143bfc39bb61c09170afb2fbe9c94a44f14ab014282de659550f.
  BOOT shim/out/dreamlte-xnu-0223.img,18,448,400B,SHA256
  dd65dd0a0fa476de64c12ff15245383c6d7073fee94b73ecc2f8912c772e35ce.
  Original BOOT components/header preserved; fit and independent hash PASS.
- Fresh Download Mode054 accepted BOOT100%, Heimdall exit0/reboot.
  Only BOOT written;0223 now installed. Artifacts/own reviewed manifest/log
  under research/dreamlte/ci-44298522029. Requested last three visible lines,
  especially DREAMLTE VM markers. Physical result pending; USB unverified.
-0222 report remains persistent phase5/no later text, before USB.0223 only
  adds VM checkpoints, preserving0222 USB sequence. No Android restoration,
  USERDATA or protected-partition writes. No live CI/preparation remains.

## 2026-11-18:0222 persistent phase5 stop;0223 VM checkpoints

- User explicitly confirms last persistent line on0222 was
  kernel_startup_initialize_upto: reached phase 5, with no later text.
  Source marks completion of STARTUP_SUB_PMAP_STEAL within vm_page_bootstrap,
  before BSD/USB.0222 session-order change has no physical execution evidence.
-0223 adds bounded DREAMLTE-only kprintf checkpoints after phase5, around
  pmap_free_pages, bucket/lock allocation and initialization, vm_tag_init and
  pmap_startup. Enables existing VM stage logger, including boot-page retire.
  No allocator, memory-map, startup bypass or USB programming change.
- Both actual ARM64 translation units compile; all12 diagnostics present in
  objects. Plain overlay application equals reviewed complete sources.
  Reverified0222 artifact before archiving own reviewed-source manifest.
  Current verifier extends to11 complete sources/28 linked diagnostics.
- Installed0222; fresh Download Mode054 remains untouched. Full0223 CI next;
  build/physical outcome and USB success remain unproven.


- Full0223 CI44298522029 dispatched at
  d5f6472 (exact head is checked by preparation). Preparation26124/script
  research/dreamlte/prepare-0223.py waits exact run, verifies11 sources/
  6 symbols/28 linked diagnostics and packages preserved-component BOOT;
  never flashes. Log alongside; Download Mode054 still untouched.

## 2026-11-18:0222 verified and flashed; session trace pending

- Exact CI44285281557 SUCCESS at b4062f27e271a9b60f6c3d317868f27c51ef4012.
  Preparation24221/PID61310 handled transient GitHub TLS poll errors;
  download62796 and verification/packaging completed, no replacement CI.
- Nine complete source hashes/six symbols/sixteen linked diagnostics and
  active profile PASS. Kernel SHA256
  070715aeb2c711e17e516bbb2fc5c852df15bdb71e5faa58d34688c2416b39ab.
  BOOT shim/out/dreamlte-xnu-0222.img,18,448,400B,SHA256
  46d86841ccadddafc0c5da984b5fd73c6c696456641c847d7c6bef12e46eb57f.
  Original BOOT components/header retained; fit/independent image hash PASS.
- Fresh Download Mode053 accepted BOOT100%, Heimdall exit0/reboot. Installed
  BOOT0222; only BOOT written. Artifacts/manifests/flash log under
  research/dreamlte/ci-44285281557. Immediate host no1209:0001/no ECM.
- Requested session LINK/UTMI before endpoints, then resources/FAIL/CORE/PHY
  or running/events. Physical session-bit effect and USB success unproven.
  No live CI/preparation; no Android restoration or other partition writes.

## 2026-11-18:0221 wake retained;0222 corrects session-valid ordering

- User0221 physical report: ID5533280a/GCTL30c12004/DSTS00520004;
  PHYversion00010000 CLK801b0049 UTMI60; Q7e00 LINK08000000 SEL0;
  soft reset done1ms GCTL30c12004 DCFG4; post-timing USB2=40102400
  GCTL80e92004. First resource ep0cmd2 remains active402, PAR0=1/PAR1=0/
  PAR2=0; GSTS3e800000 DCTL0 DSTS00520000 EN0; PIPE010c0002 HW3=10420085
  BUS22220001/300; PHY LINK08000000 UTMI60 CLK801b0049 Q7e00 SEL0.
  Reset-order fix retained wake mask but did not solve command execution.
- Pinned Samsung CAL asserts LINK FORCE_BVALID/FORCE_VBUSVALID and UTMI
  VBUSVLDEXTSEL/VBUSVLDEXT during PHY init before DCTL/endpoint commands.
  Our existing helper ran after failed endpoint setup, so physical LINK/UTMI
  have no session-valid bits.0222 moves existing helper before DCTL reset,
  reasserts after reset before endpoints, prints session readback. No new
  power/PLL/clock writes; retained reset-wake and QACT changes. This is a
  source-derived ordering hypothesis, not demonstrated hardware root cause.
- Actual ARM64 compile, wrapper ordering/masks and EP/resource tests PASS;
  plain patch/full-source match PASS. Reverified0221 then archived own source
  manifest; promoted0222/current manifest16 strings.0221 remains installed,
  fresh Download Mode053 ready, no new flash. Full CI next.

- Full0222 CI44285281557 at b4062f27e271a9b60f6c3d317868f27c51ef4012
  dispatched. Preparation24221/script research/dreamlte/prepare-0222.py
  waits exact run, retries transient API poll failures, verifies nine sources/
  six symbols/sixteen linked diagnostics and packages BOOT; never flashes.
  Keep Download Mode053 fresh, no new write before verification.

## 2026-11-18:0221 verified and flashed; physical reset-wake test pending

- Exact CI44276126788 SUCCESS at3e18153bae65d8386c824e42cbb66a32b8968084.
  Original preparation58444 exited after GitHub poll failure, confirmed
  terminal before retry. Retry53993 added same-run poll-error handling,
  downloaded/verified and completed packaging; no replacement CI run.
- Nine complete source hashes/six symbols/fifteen linked diagnostics/profile
  PASS. Kernel SHA2561135da14873d81cba5a9e4dd573a9db9e04e022a41b979400b60b6a3ddf7afbf.
  BOOT shim/out/dreamlte-xnu-0221.img,18,448,400B,SHA256
  69d063af00bee0e864b94f9557f4559a991a6b91b8488b3f89864b4f31a193a3.
  Original BOOT components/header retained; payload/partition fit and
  independent image hash PASS before flash.
- Fresh Download Mode052 accepted BOOT100%, Heimdall exit0/reboot. Installed
  BOOT0221; only BOOT written. Exact artifacts/manifests/flash log under
  research/dreamlte/ci-44276126788. Immediate host no1209:0001 gadget.
- Requested USB2CFG post-reset line and resources/FAIL/CORE/PHY or events.
  Actual retention of40102400 and successful resource setup still unproven.
  No Android restoration or protected/USERDATA writes. Goal remains active.

## 2026-11-18:0220 QACT confirmed; reset restores USB2 low-power bits

- User0220 physical report: ID5533280a/GCTL30c12004/DSTS00520004;
  PHY version00010000 CLK801b0049 UTMI60; link wake Q7e00 LINK08000000 SEL0.
  Failure ep0cmd2 reg402 PAR0=1/PAR1=0/PAR2=0; GCTL80e92004 GSTS3e800000
  USB2=40102540 DCTL0 DSTS00520000 EN0; PIPE010c0002 HW3=10420085
  BUS22220001/300; PHY LINK08000000 UTMI60 CLK801b0049 Q7e00 SEL0.
- QACT changed as intended, but first resource command still active.
  USB2 now has ENBLSLPM/SUSPHY restored (0x140), unlike0219's40102400.
  Existing clear precedes new link reset and DCTL reset; reapply afterward.
  This isolates a reset-order regression, not proof of sole USB root cause.
-0221 clears only USB2 bits8/6 immediately after link wake and again in
  post-DCTL-reset timing setup before any endpoint command. Preserves all
  other USB2 board fields and retains QACT/reset flow and failure snapshots.
  Actual ARM64 compile, modeled reset-default/all32-bit preservation, wrapper,
  EP and resource suites PASS; plain patch/full-source equality PASS.
 0220 exact artifact reverified, expected manifest archived before0221
  promotion/source hash update. No new flash;0220 installed, Download Mode052.

- Full0221 CI44276126788 at3e18153bae65d8386c824e42cbb66a32b8968084
  dispatched. Preparation session55332/script research/dreamlte/prepare-0221.py
  waits exact run, verifies nine sources/six symbols/fifteen diagnostics then
  packages preserved-component BOOT; never flashes. Log alongside. Keep
  Download Mode052 fresh until prepared-manifest/hash checks pass.

## 2026-11-18:0220 verified and BOOT flashed

- Exact CI44270585173 SUCCESS at a1ea67a281f8009de43e974490a974927ef4a8ca.
  Preparation96056/PID56313 and download57495 completed. Nine complete
  source hashes/six symbols/fifteen linked diagnostics/profile checks PASS.
  Kernel SHA256b0f0724bcf1584fbc81fce66b5eb8fb407635cbd085a0a15cdbfa82215958b88.
- BOOT shim/out/dreamlte-xnu-0220.img,18,448,400B,SHA256
  918a116e78dd148c5d5727ff396c16d7ddb86e9720f7ee143c916d9cd92f7df0.
  Original ramdisk/second/DTBH/header retained; payload/partition fit and
  independent manifest/image hash PASS before write.
- Fresh Download Mode051 accepted BOOT100%, Heimdall exit0/reboot. Installed
  BOOT now0220. Private artifacts/manifests/flash log ci-44270585173 under
  research/dreamlte. Only BOOT written; no Android restoration/other write.
- Immediate host zero1209:0001/no ECM interface; journal shows051 disconnect
  10:19:39 CET, no new enumeration in observed window. Requested link-wake
  Q/LINK/SEL, resources-assigned and FAIL/CORE/PHY or running/event lines.
  Physical0220 sequence effect pending. No USB success inferred from CI.

## 2026-11-18:0220 CI success; artifact transfer live

- Exact CI44270585173 at a1ea67a281f8009de43e974490a974927ef4a8ca
  terminal SUCCESS. Preparation session96056/PID56313 remains live, child
  gh download57495 transferring artifacts. Observed rchar increased from
  19,208,157 to22,121,664 bytes; slow transfer is not a terminal failure.
- Phone remains fresh Download Mode051/04e8:685d. No handshake/flash yet.
  Installed BOOT still0219;0220 prepared-boot.json not yet produced. Wait
  for exact-source/symbol/15-string/package and independent hash checks
  before authorized BOOT-only flash. No replacement CI/download started.

## 2026-11-18:0219 physical PHY snapshot;0220 source-derived wake

- User physical0219 dump: ep0 cmd2 reg00000402; PAR0=1/PAR1=0/PAR2=0;
  GCTL80e92004,GSTS3e800000,USB2=40102400,DCTL0,DSTS00520000,EN0;
  PIPE010c0002,HW3=10420085,BUS22220001/00000300;
  PHY LINK08000000,UTMI00000060,CLK801b0949,Q00007c00,SEL00000000.
- STARTCFG completed; first OUT EP0 SETTRANSFRESOURCE now remains active.
  Thus changing resource/config order did not solve command execution.
  Q has DIS_ID0/VBUS/BVALID/LINKGATE bits set but FORCE_QACT(bit9) clear;
  SEL PIPE-clock bit3 clear selects measured primary bank. Reset/UTMI sleep
  bits clear do not prove functional link clocks. Host still no gadget.
-0220 follows pinned Samsung exynos_cal_usbphy_q_ch(enable=1): disable
  automatic QACT sources, force QACT after prescribed500us delays, pulse
  LINK_SW_RESET with10us delay, then existing DCTL reset. Retains unrelated
  Q bits, port mux, PLL/reference/tuning. Refuses secondary PIPE clock or
  preasserted link reset. Predicted Q7c00->7e00 is not yet physical evidence.
- Actual ARM64 translation-unit compile PASS; actual wrapper/EP/resource
  modeled suites PASS, both PHY register layouts, all32 Q-bit preservation,
  primary selection/refusal and physical sample covered. Plain patch/full
  reviewed-source equality PASS.0220 promoted, source manifest updated with
  fifteenth linked marker after archiving verified0219 manifest privately.
  No new hardware write;0219 remains installed. Full CI next.

- Full0220 CI44270585173 confirmed in_progress at
  a1ea67a281f8009de43e974490a974927ef4a8ca. Preparation session96056
  waits on this exact run, verifies nine sources/six symbols/fifteen linked
  strings and packages preserved-component BOOT; never flashes. Private
  script/log research/dreamlte/prepare-0220.py and .log. Fresh Download Mode
  requested. Keep live run unchanged; no hardware success claim.

## 2026-11-18:0219 post-flash host observation

- Rechecked actual USB devices and control-transfer checker after0219:
  no1209:0001 gadget and no Download Mode. Host kernel journal over the
  observed fifteen-minute window shows Download Mode050 disconnect at
  09:41:44 CET, with no subsequent enumeration/descriptor failure messages.
  This supports absence of a host-visible reconnect, not a proven PHY cause
  or physical kernel stopping point. Current0219 screen trace is still needed.
- CI44265115339 terminal SUCCESS; preparation53546 has exited after verified
  packaging. There is no live job to classify as a verified wait now. Last
  goal turn made progress via verified0219 BOOT flash. No new build, USB
  sequence change, flash or protected-partition write in this observation.

## 2026-11-18:0219 exact build verified and BOOT flashed

- Prior goal turn was a verified wait on live CI/preparation. This turn exact
  CI44265115339 SUCCESS at41f5575831f48c6796d71024d220915ae9b14587.
  Source/profile/symbol/string verification PASS: nine complete source hashes,
  six linked symbols and fourteen linked diagnostics. Kernel SHA256
  ea0a8e9d5678f4c3a39b7f92d60a750553cc73678d67b637c1e626cc0664cf40.
- Preparation65521/PID53546 completed; original BOOT components/header kept,
  payload/partition fit and independent prepared-manifest hash checked.
  BOOT shim/out/dreamlte-xnu-0219.img,18,448,400B,SHA256
  b555a272b1859e176944657ad896891be857d2cb17f4c1aaa1fbe4b6cb63c9d9.
- Fresh Download Mode050 accepted BOOT100%, Heimdall exit0/reboot. Only BOOT
  written. Exact artifacts/manifests/flash log research/dreamlte/ci-44265115339.
  Current installed BOOT0219 supersedes0218. Physical0218 trace not received.
- Immediate host no1209:0001; no physical USB success. Requested four USB FAIL
  lines, one USB CORE and two USB PHY lines, plus resources-assigned marker
  if present.0219 adds read-only failure snapshots, not functional PHY fix.
  No Android restoration or USERDATA/protected-partition write this trial.

## 2026-11-18:0219 diagnostics promoted for full build

- Prior goal turn progressed by preparing/test-compiling read-only PHY/core
  diagnostics and expanding command tests; no working USB claim. Current
  host still sees no gadget and0218 screen report is pending.
- Promoted0219 into active profile to prepare a verified next trial without
  waiting to start its build. No USB sequence change, clock/reset write or
  new map. Actual ARM64 compilation and all three modeled suites PASS.
- Archived0218 own expected source manifest with its private CI artifacts
  before updating current manifest to0219 and14 linked diagnostic strings.
  Staged source now0219.0218 remains installed; no new phone write.

- Full0219 CI44265115339 at41f5575831f48c6796d71024d220915ae9b14587
  confirmed in_progress. Preparation session65521 waits for this exact run,
  then verifies nine sources/six symbols/fourteen diagnostic strings, retains
  original BOOT components and packages0219; it never flashes automatically.
  Private script/log research/dreamlte/prepare-0219.py and .log. Active
  profile generator stages140 patches. Do not restart this live build.

## 2026-11-18: prepared read-only PHY failure diagnostics after0218

- Rechecked host after0218 flash: no1209:0001, so physical USB is still
  unverified. Screen report requested in prior turn remains pending. Prior
  turn made progress through verified full build/package/BOOT flash.
- Pinned Samsung CAL forces QACT and pulses LINK_SW_RESET during PHY enable;
  current firmware takeover does neither. This is a source difference only,
  not established cause. Prepared0219 outside active profile adds failure-only
  PIPE/HW3/BUS and already-mapped PHY LINK/UTMI/CLK/Q/SEL readbacks. No new
  mappings, writes, resets or retries. No replacement build/flash started.
- Actual0219 ARM64 USB translation unit PASS; active0218 source restored
  SHA2560382ae5a0ca1260ea41efba3048229de2b513a6012c53eab85e6408332749250.
  Plain patch equals reviewed full source; wrapper/resource tests PASS.
  Expanded EP command suite covers all32 physical endpoints, parameter
  writes/completion/status/timeout, missing PHY map and unchanged PHY words.
  Both active0218 and prepared0219 pass. Physical PHY state is not measured.

## 2026-11-18:0218 verified and flashed; physical result pending

- Exact CI44261810052 SUCCESS at94e4d744b76110d0f330544bc27ad6fef228a822.
  Nine complete sources/six symbols/eleven linked diagnostics and active
  overlay/profile hashes PASS. Kernel SHA256
  488e2b10493c7cee0643399e024222b77bd6ce506e657532741cffe823535c4f.
- Preparation session12913 completed. BOOT0218 size18,448,400B/SHA256
  70f47645eb7f5c0ba40a6d9384b4c3d4654d7e82cd1b24620111a99da2cb47d4.
  Preserved original ramdisk/second/DTBH/header fields and checked BOOT fit;
  independent manifest/hash check PASS. Wrapper/command/resource suites PASS.
- Fresh Download Mode049 accepted BOOT0218:100%, Heimdall exit0/reboot.
  Flash log and manifests: research/dreamlte/ci-44261810052. Only BOOT written.
  Immediate host checker finds zero1209:0001 devices; no enumeration or
  transfer success. Requested resources-assigned/failure lines or final
  startup lines. Current installed BOOT is0218;0217 is superseded.
- This trial tests Samsung resource-before-configuration ordering. A passed
  build/model test is not a hardware fix. Physical report remains pending.
  USERDATA unchanged by this trial; earlier deployment remains incomplete.

## 2026-11-18:0217 physical endpoint snapshot recovered

- User reports DREAMLTE USB FAIL: ep0 cmd1 reg00000401; PAR0=00000200,
  PAR1=00000500,PAR2=00000000; GCTL80e92004,GSTS3e800000,USB2=40102400;
  DCTL00000000,DSTS00520000,EN00000000. Exact values are physical reports,
  not readback through a working gadget. Host still sees no USB device.
- DEPCMD.CMDACT(bit10) remains set, so zero status bits are not a successful
  completion. PAR0 decodes64-byte packets; PAR1 enables expected completion/
  not-ready events for OUT EP0. GCTL device mode2, USB2 reset/SUSPHY/ENBLSLPM
  clear, GSTS CSR_TIMEOUT(bit5) clear. This excludes none of the unmeasured
  PHY clock/electrical dependencies. DCTL stopped/DSTS halted and no enabled
  endpoints are expected at this pre-RUN failed-configuration stage.
- Prior Android GHWPARAMS3=10420085 decodes16 IN/16 OUT endpoints;0218's
  bounded allocation covers that layout. Source review confirms Samsung
  clears RAMCLKSEL before setup; PIPE selection is later on SS connect,
  not evidence for changing the current USB2 pre-configuration clock mux.
- Keep live0218 CI44261810052 unchanged. Next hardware test is the already
  reviewed resource-before-config sequence, with0217 snapshots retained.

## 2026-11-18:0218 resource-order candidate promoted

- Reverified exact0217 artifact before changing manifest; archived its own
  reviewed hash manifest privately.0217 physical register report pending.
- Promoted source-derived0218 ordering into active profile: initial STARTCFG
  followed by one resource per implemented endpoint before SETEPCONFIG.
  Resource-count/failure-position and command tests pass on active source.
  Earlier actual ARM64 compile passed for identical prepared source. Added
  resource test to full CI and required linked resources-assigned marker.
  No new hardware write or enumeration claim;0217 remains installed.
- Full0218 CI44261810052 live at94e4d744b76110d0f330544bc27ad6fef228a822.
  Preparation session12913 waits for exact run then checks nine actual
  sources/six symbols/eleven linked diagnostics and BOOT packaging. Script
  research/dreamlte/prepare-0218.py and .log; no automatic flash.

## 2026-11-18:0217 diagnostics verified and flashed

- Exact CI44259521488 SUCCESS at a947a493d424c503224c594a3b9ba046b7967fc1.
  Artifact checks PASS: nine complete sources, six symbols, ten diagnostic
  strings and all active patch/profile hashes. Kernel SHA256
  7d1766187df0abb4f3fa322e1bd1ce0dfcf38ffbd743a537cdf1d881e75be3ea.
- Preparation session27807 completed. BOOT0217 size18,448,400B/SHA256
  9eef68eb87d3ea23b5e631a3d9e7256b7f6c6d81398eec75a642cba4aa33f0ad.
  Original BOOT components/header preserved, payload/partition fit checked.
- Fresh Download Mode048 accepted BOOT0217:100%, Heimdall exit0/reboot.
  Current phone now runs0217 candidate, not0215. Immediate host gadget check
  finds zero1209:0001. Requested four DREAMLTE USB FAIL register lines or
  last three startup lines. Runtime endpoint snapshot pending; no USB pass.
  Only BOOT written; no new USERDATA/protected writes or Android restoration.
  Private artifacts/manifests/flash log research/dreamlte/ci-44259521488.
  Prepared0218 remains outside active profile and not included in this trial.

## 2026-11-18:0215 reaches USB; exact command failure identified

- User now reports soft reset done after9ms, GCTL80c12004/DCFG00000004;
  USB2CFG40102400 and post-timing GCTL80e92004; ep0 cmd0x1 timeout; EP0
  setup failed; then Apple_HFS media wait. This supersedes the apparent
  earlier0215 display stop: IOKit/BSD reached USB and root discovery.
- Short-circuit EP sequence establishes DEPSTARTCFG(cmd9) completed, then
  first OUT EP0 SETEPCONFIG(cmd1) timed out; transfer-resource commands had
  not run. USB2 wake/timing writes are visible, not sufficient for USB.
- Pinned Samsung gadget.c differs in resource ordering: start_config sends
  DEPSTARTCFG then SETTRANSFRESOURCE to every implemented hardware endpoint
  before SETEPCONFIG. Donor currently configures before resource assignment
  and repeats STARTCFG for data endpoints. Candidate change requires actual
  sequence tests/full build; ordering is a source difference, not proven cause.
  Existing0217 CI44259521488 remains live; do not replace it.
- Prepared0218 outside active profile: GHWPARAMS3-derived IN/OUT counts,
  bounded/ECM capability guards, STARTCFG then one resource per implemented
  physical endpoint, before EP configuration. No repeated data STARTCFG.
  Actual resource helper tested across324 count combinations and every
  command-failure position; existing wrapper/EP command suites PASS. Actual
  ARM64 USB unit compiles; staged source restored to0217 hash f2420dd5...
  No cold PHY writes or hardware success inferred; full build still needed.

## 2026-11-18: startup trace reaches PE_lockdown_iokit;0217 checkpoints

- User reports last startup-trace line kernel_bootstrap: PE_lockdown_iokit.
  This demonstrates execution beyond the version banner. It does not prove
  the call blocks: next vm restrictions/kperf/BSD steps have sparse logging.
- Source PE_lockdown_iokit performs a scalar zone flag assignment then
  StartIOKitMatching; root matching allocates an IOWorkLoop/registers service.
  Added DREAMLTE-only checkpoints before/after matching, return, VM CPU
  restrictions, kperf and BSD entry; enables existing BSD init checkpoints
  and brackets throttle_init. No bypass of IOKit, scheduler or root logic.
- Promoted0216 failure-only endpoint snapshots alongside0217; no USB
  initialization sequence change. Four actual ARM64 translation units PASS
  (pe_init/startup/bsd_init/sweet_usb). Exact0215 artifact plus plain patches
  matches all four reviewed complete files. Both USB wrapper and actual
  endpoint completion/status/timeout tests PASS; new test added to CI gate.
- Current phone still has0215 startup_debug=1; host sees no gadget.0217
  requires full CI and exact artifact verification before a new BOOT trial.
- Code commita947a493d424c503224c594a3b9ba046b7967fc1 pushed. Full0217
  CI44259521488 dispatched and confirmed queued. Preparation session27807
  waits on this exact run then verifies nine sources/six symbols, preserves
  stock BOOT components and packages0217 with startup_debug=1/dreamlteusb=2.
  Private script/log research/dreamlte/prepare-0217.py and .log; never flashes.
- Continuation verified live CI44259521488/job134649187730 in Build and
  preparation session27807/PID49363. Phone absent from host USB; requested
  Download Mode ahead of next trial. No new flash. Consolidated active S8
  NOTES handoff to remove contradictory superseded statuses; byte-for-byte
  donor tail unchanged. Goal remains active; no USB completion claim.
- Added pre-flash linked-string gate for ten required0217/0216 checkpoint
  messages in addition to nine complete source hashes and six symbols. All
  ten strings present in actual local ARM64 objects; old0215 kernel lacks
  them. Exact0217 preparation will run updated verifier after download.
  CI44259521488 remains live/Build; no rebuild/replacement or phone write.

## 2026-11-18: framebuffer0214 boots to USB endpoint setup

- Fresh Download Mode session accepted verified framebuffer0214 BOOT:
  Heimdall upload reached100%, exited0 and rebooted. Log archived privately
  at research/dreamlte/ci-44119574729/heimdall-boot-0214.log. Installed BOOT
  SHA256 fa8b862c1eb4e054ca581d45cc5957f7327b8f4cfd3432375471d49aa85a14b3.
- User reports visible `SWEET USB: endpoint 0 setup failed`. This verifies
  physical framebuffer text and XNU reaching gadget EP0 setup, after DCTL
  reset. The combined failure message does not identify which EP command
  failed; preceding command/status or timeout line is still needed. Host
  sees no gadget. No USB enumeration/transfer or userspace success claimed.
- Android was not restored. Latest trial wrote only BOOT; converted USERDATA
  deployment remains unsuccessful as documented below.
- USB2 wake/timing0215 promoted into xnu/dreamlte at5439710; actual reviewed
  source hash updated. Full CI44256127913 at5439710 is in_progress (Build).
  Do not replace that run merely due to polling timeout.0215 is not flashed.

- Continuation classified as progress: added prepared0216 failure-only EP
  register snapshots outside active profile and actual-function EP command
  tests.0215/0216 command parameter writes, delayed completion, status error
  and bounded timeout pass across six physical endpoints; diagnostics add no
  MMIO writes.0216 USB translation-unit ARM64 compile PASS; staged0215 source
  restored and its df5d49b... hash rechecked. No new hardware trial claimed.
- Exact0215 CI44256127913 remains live/in_progress. Preparation session67425
  waits for that exact5439710 run, then downloads and verifies seven compiled
  sources/six linked symbols before packaging a separate0215 BOOT. Script
  research/dreamlte/prepare-0215.py; log prepare-0215.log; it never flashes.
  User's preceding EP command/status screen line remains pending.

- Additional physical report: Waiting on IOProviderClass IOMedia Content
  Apple_HFS, then Failed to write boot-picker-bringup-reason to NVRAM.
  Actual IOKitBSDInit.cpp confirms default Apple_HFS media matching and the
  latter message in BSD_BOOTFAIL_MEDIA_MISSING handling. This establishes
  execution beyond synchronous USB setup into root discovery, not a mounted
  filesystem. USB setup returns on error; root progress does not prove USB.
  No S8 UFS root provider exists yet and USERDATA deployment is incomplete.
  NVRAM failure is a secondary missing-media diagnostic, not a demonstrated
  cause of the EP0 setup failure. Host still has no gadget.

- Fresh host evidence on continuation: phone returned to Download Mode
  (04e8:685d), with no host reset required. Retried explicitly authorized
  converted sparse USERDATA upload using --no-reboot after checking sparse
  header, exact file size and32GiB expanded fit within measured partition.
  Protocol/session/PIT succeeded; first sequence confirmation failed at0%,
  then end-session failed. Heimdall exit1; log root/heimdall-userdata-sparse-
  fresh-20261118.log under private research/dreamlte. No BOOT/protected write
  in this retry. USERDATA may be partial; no deployment success claimed.
  Requested exact phone-side Download Mode error before any further retry.
- CI44256127913 at5439710 remains authoritatively in_progress/Build;
  preparation PID47387/session67425 remains live. No replacement dispatched.

- User reports no new text after failed sparse upload and will re-enter
  Download Mode. Host now sees fresh USB device046/04e8:685d. Exact0215
  CI44256127913 SUCCESS at5439710; preparation session67425 is downloading
  the exact kernel/buildtree, then verifying actual content before packaging.
  No further USERDATA attempt or BOOT write until candidate checks complete.

## 2026-11-18: USB0215 verified, flashed; runtime report pending

- New0215 physical report: last visible line Darwin Kernel Version22.6.8,
  much less output than0214. Host has no gadget. Do not classify0215 as an
  EP0 failure without its trace. Source startup.c prints version at entry
  to kernel_bootstrap, before scale_setup/vm_mem_bootstrap and much earlier
  than BSD USB probe. Visible stop is not proof of the precise CPU halt.
- Streaming comparison of every xnu/ file in exact0214 and0215 buildtrees
  finds only bsd/dev/sweet_usb.c changed; no added/deleted source files.
  ADTs byte-identical. USB changes execute after networking initialization,
  so they do not directly execute before the reported version line.
- Packaged same verified0215 kernel/ADT/loader with existing startup_debug=1
  to expose startup phases without source changes. Candidate
  shim/out/dreamlte-xnu-0215-startup.img,18,432,016B,SHA256
  6ddd75d186a5d8881a47d65bcc9266314e48ae5907c799b8455f338c1826cacc.
  BOOT component/header preservation and exact payload PASS; not flashed.
  Requested Download Mode re-entry.0216 remains prepared, not promoted.

- Fresh Download Mode device047 arrived. Startup-trace0215 BOOT above
  rehashed then flashed successfully:100%, Heimdall exit0/reboot. Exact log
  ci-44256127913/heimdall-boot-0215-startup.log. Current BOOT is now0215
  plus startup_debug=1; same verified kernel, no source/USB change in trial.
  Immediate host check finds no gadget; requested last three startup lines.
  BOOT only; no Android restoration or new USERDATA/protected write.

- CI44256127913 SUCCESS at5439710b649202ada57dbef4fd50e061d57f18ed. Exact
  artifact verification PASS: seven complete compiled source hashes, six
  linked symbols and all active patch/profile hashes. Kernel SHA256
  d0359a2566c1c9048c17f7c9f0d107ad10c428b5bc41870abb87ad35a790080a.
- Preparation session67425 completed0. Separate BOOT0215 is18,432,016B,
  SHA2565a484fa65b5e4ba3039562cd1bde43cea68faba732e19d4b7ba8391dd4fff17f.
  Original ramdisk/second/DTBH/header fields preserved and payload/BOOT fit
  verified; dreamlteusb=2. Exact manifests/logs in private ci-44256127913.
- Fresh Download Mode device046 accepted BOOT-only0215: Heimdall100%, exit0,
  upload/reboot successful.0215 now replaces0214. No USERDATA or protected
  write in this flash; no Android restoration. Host immediate check finds
  zero1209:0001; asked user for USB2CFG/reset/EP command and last screen line.
  Physical enumeration/transfers remain unproven; root deployment incomplete.


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
