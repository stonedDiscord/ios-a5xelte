# DREAMLTE USB bring-up evidence

## Current status: 0239 hardware

Build 0239 verified buttonless entry to Samsung Download Mode on the S8:

```sh
sudo python3 tools/dreamlte-usb-reboot.py download --timeout 30
```

Run this from the working XNU USB connection. The tool checks that the
same physical port returns as Samsung `04e8:685d`. The transition writes
no partitions. XNU console output is only available while XNU is running.

On 0238, a normal reboot was acknowledged, but USB did not return within
120 seconds. A cable replug on that boot restored enumeration, host IP,
ping and XNU console output. Its console showed no bus reset or connection
until the replug. On 0239, the normal reboot also failed to restore USB
within 120 seconds; replug restored the link and its console showed 198
bytes. See [DREAMLTE_PROGRESS.md](../DREAMLTE_PROGRESS.md) for the evidence.

0239 successfully reaches its USB poller after a manual restart, but can
stall in page array mapping on its first boot. On the observed restart, the
device-side log reported a reset and connection; the host still saw no
attachment until the user replugged the cable. The replugged boot passed
EP0, ping and XNU console checks. A normal USB reboot was acknowledged, but
the device did not re-enumerate on the same port within 120 seconds. After
replugging, the USB Download Mode command also passed on 0239 and the same
physical port returned as `04e8:685d` without button input.

## 0237 USB reconnect and buttonless reboot candidate — 2026-11-19

Previous goal turn established working0236 USB. This turn installs persistent
host networking and adds an EP0 reboot protocol. Host was still1209:0001/068,
with generic NetworkManager shared192.168.42.1 plus manually added7.1.
Installed DREAMLTE-XNU-USB profile, MAC-bound02:00:5e:77:ee:01, static
192.168.7.1/24, autoconnect priority100, no default route/DNS/IPv6. Actual
EP0 and3/3 ping PASS after activation. Reconnect selected the same profile;
full phone reboot recovery still requires physical verification. Console
helper no longer disables NetworkManager. Idempotent installer:
sudo tools/dreamlte-usb-host.sh

0237 adds strict device-vendor EP0 capability0x50/index8895 and reboot0x51:
value0 normal/value1 download, zero payload. Reset armed only after
successful EP0 status completion, delayed100 poll ticks; USB reset or
disconnect cancels. Samsung pinned3cfb914 sec_reboot.c/sec_ext.h supply
INFORM2=12345678 and INFORM3=12345670(normal)/12345671(download), offsets
808/80c; live reboot node PMU16480000; exynos_reboot.c SWRESET offset400.
Only volatile PMU writes, no partition writes. Omits Linux ACPM/DFD
coordination: successful hardware reset/bootloader mode is UNPROVEN.
Host tool checks capability first, then same-port re-enumeration:
sudo python3 tools/dreamlte-usb-reboot.py normal
sudo python3 tools/dreamlte-usb-reboot.py download
Use status for a read-only capability query.

Actual ARM64 compile, nine USB source-derived suites, RAM console sender
and UDP receiver suites PASS.0236 remains installed. One initial manual
Download Mode entry requested because0236 lacks the command. No new flash.
Preserve RECOVERY/bootloaders/EFS/CPEFS/USERDATA and all non-BOOT partitions.
Goal stays active until normal reboot restores USB automatically and USB
download command physically enumerates Samsung04e8:685d.


## 0236 WORKING XNU USB console verified — 2026-11-19

User reports prerequisites ISOL00000000->00000001 and
REFSEL00000000->01000000; SWEET USB running DSTS00920001 after0ms,
DMA882cae000. Host now enumerates1209:0001 device068 with CDC-ECM
interface enp0s20f0u3, expected MAC02:00:5e:77:ee:01 and verified USB parent.
Host initially had192.168.42.1; added192.168.7.1/24 and brought interface up
using available noninteractive sudo. No new flash or partition writes.

Actual sudo host checker PASS: device/config descriptors, status and active
configuration over EP0; exact ECM endpoints;3/3 ICMP replies from192.168.7.2
with0% loss;2373 bytes identifiable XNU SWEET USB event/setup text received
from192.168.7.2 on UDP5140 over30seconds. No USB-console success inferred
from build or ping alone: captured text includes GET_DESCRIPTOR/GET_STATUS/
GET_CONFIGURATION handling. Output log and full checker result remain private
at research/dreamlte/ci-44526044672/xnu-usb-console.log and
host-console-check.log; updated prepared-boot.json records log hash/results.

Working checkpoint0236 CI44526044672/sourcebf796ff, BOOT SHA256
7e1ec3f1e5da1a365302b894ebb0d1469126f32daad6fc2f78568cc0c0c1d36d.
Preserve this installed BOOT. Both missing prerequisite fields were corrected
in one trial, so success does not isolate their individual contributions.
The transport is USB Ethernet carrying kernel output, not CDC serial and
not an interactive shell. Host listener: tools/sweet-usbnet.sh LOGFILE
(configures192.168.7.1 and listens UDP5140; sudo required for interface).
Reverify: sudo python3 tools/dreamlte-usb-check.py --interface enp0s20f0u3
--console-seconds 30 --console-log <private-path>. Interface name may change;
match expected MAC and USB parent. Stop any other5140 listener before checker.
Goal completion gates enumeration/control/bidirectional data/XNU text PASS.
UFS mounting, iOS userspace and GUI are separate and remain unverified.


## 0236 verified and BOOT flashed; prerequisite-enable result pending — 2026-11-19

Exact CI44526044672 SUCCESS atbf796ffd38b3d065ad7e6da9d51ae761e32643cb.
11sources/9symbols/55diagnostics/profile PASS. Kernel SHA256
d56e41c899bf18364ea79f3597d8e6ef8beea10abad20d0dae00b580e1399703.
BOOT shim/out/dreamlte-xnu-0236.img,18,464,784B,SHA256
7e1ec3f1e5da1a365302b894ebb0d1469126f32daad6fc2f78568cc0c0c1d36d.
Original BOOT components/header/payload/fit/hash PASS. User confirms ready;
fresh Download Mode067 accepted BOOT100%, Heimdall exit0/reboot. Only BOOT
written. Exact artifacts/manifest/log research/dreamlte/ci-44526044672.
Immediately host has no1209:0001/ECM. Requested prerequisites ISOL/REFSEL
before/after and resources/running or failure/POLL; refusal/mismatch if
stopped earlier. New masked writes physically unverified; no USB success.
0236 installed, no live CI/preparation/flash. Keep this boot for evidence.


0236 CI44526044672 dispatched atbf796ffd38b3d065ad7e6da9d51ae761e32643cb.
Actual ARM64 compile; eight source-derived USB suites including new
prerequisite preservation/order/refusal checks; RAM reader/sender suite;
exact0235-source overlay equality PASS. Manifest11sources/9symbols/55strings.
Preparation research/dreamlte/prepare-0236.py verifies exact head/run,
source/profile and preserved BOOT components, never flashes. Fresh Download
Mode requested;0235 installed. New writes and USB operation untested.


## 0235 isolation/reference fields zero;0236 implements prerequisites — 2026-11-19

User reports DREAMLTE PREREQ inherited and prelog-exit both ISOL00000000,
REFSEL00000000. This supersedes the earlier apparent pmap-only stop as the
latest observed progress: USB probe and initial resource timeout path ran.
Do not infer how the earlier stop cleared or invent current POLL values.
Pinned Samsung PHY power-on releases PMU bit0; PHY init applies DT refsel
bit24 before CAL. Both measured prerequisite fields were missing.
0236 sets only PMU0x16480704 bit0 and selector0x10e5007c bit24 before the
existing PHY initialization, after exact ID/opt-in/stopped-core guards.
Reads both before writing, refuses all-ones, verifies isolation before
reference and exact reference readback before proceeding. No PLL/rate/
CMU/mux-policy tuning, endpoint reorder, timeout extension or retry.
Source-backed missing initialization, not proof of the cmd2 root cause.
0235 still installed; new hardware writes untested. BOOT-only trial next.


## 0235 last visible marker is pmap_startup entry — 2026-11-19

User reports DREAMLTE VM: pmap_startup enter and confirms it remains the
last visible line after30seconds. No USB/prerequisite line reported. Host
has no1209:0001 and no Download Mode. This locates the last observed output
before BSD USB initialization; it does not prove the exact instruction
that stopped execution or distinguish a VM stall from loss of output.
Exact0234/0235 compiled archives have identical vm_resident.c, arm_vm_init.c,
vm_init.c and startup.c.0235 code change is in sweet_usb.c, whose new
register reads execute later; no evidence those reads executed on this boot.
Image hash reverified. Next test: fresh restart of the same verified0235
BOOT to determine reproducibility before adding VM instrumentation or
attributing this to a USB register read. No new flash/build performed.
Preserve all non-BOOT partitions; console goal remains unachieved.


## 0235 verified and BOOT flashed; prerequisite readbacks pending — 2026-11-19

Exact CI44518477291 SUCCESS atc202064b5256360ee698b61d6bc9ebe71df1d19c.
11sources/9symbols/52diagnostics/profile PASS. Kernel SHA256
b387742111243afa2e59018df28c369426ac535dd67d4053bd6abbce10b08d60.
BOOT shim/out/dreamlte-xnu-0235.img,18,464,784B,SHA256
21c864542c8adf8fe47f251a7e8a76141d9adb6fb6d85400fed51d5cc94507b2.
Original BOOT components/header/payload/fit/hash PASS. Fresh Download
Mode066 accepted BOOT100%; Heimdall exit0/reboot. Only BOOT written.
Exact artifacts/manifest/flash log research/dreamlte/ci-44518477291.
Immediately afterward no1209:0001. Physical new reads unverified; requested
DREAMLTE PREREQ inherited and prelog-exit ISOL/REFSEL lines or last visible
line if earlier stop. No new clock/PMU/reference writes in this trial.
0235 installed; no live CI/preparation/flash. Working console unverified.
Keep this boot until physical report. CI took longer than0234 and had
transient API failures; same exact run completed without restart.


0235 exact CI44518477291 dispatched atc202064b5256360ee698b61d6bc9ebe71df1d19c.
Preparation research/dreamlte/prepare-0235.py verifies exact head/run,
source/profile and packages preserved BOOT components; never flashes.
Download Mode066 ready.0234 installed until verified0235 image is available.
Physical isolation/reference readbacks and USB console remain unverified.


## 0235 prerequisite probe prepared — 2026-11-19

0234 physical cmd2 timeout/POLL001b0048 all1000/wake0 is recorded.0235
adds read-only PMU USB isolation0x16480704 and PHY reference selector
0x10e5007c to existing clock snapshots: inherited before PHY setup and
pre-timeout before any framebuffer error printing. New line:
DREAMLTE PREREQ <stage>: ISOL=<value> REFSEL=<value>.
Expected fields from pinned Samsung/live DT: ISOL bit0=1 (isolation
released), REFSEL bit24=1. These readbacks are not clock measurements.
Mappings occur only after opt-in2/exact2.80a/stopped-core guards. No new
MMIO writes, command-order change, reset retry or active command reissue.
New read accesses untested on device. All seven USB source-derived suites,
RAM console suite, actual ARM64 compile and exact0234 overlay equality PASS.
Manifest11sources/9symbols/52diagnostics. Fresh Download Mode066 visible.
0234 installed; next exact CI and BOOT-only trial. USB console not working.


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

Source review at pinned8895 revision3cfb914658ab077aef9ed500aa4a583782971fbf:
gadget.c dwc3_send_gadget_ep_cmd writes PAR0/PAR1/PAR2 then CMDACT and
polls for completion (500 one-us delays); XNU uses that ordering and1000
one-us polls. dwc3_gadget_set_xfer_resource sets PAR0=NUM_XFER_RES(1),
PAR1/2=0. start_config issues STARTCFG(0) then transfer resources before
SETEPCONFIG. Thus neither reordering the first two commands nor extending
the timeout is supported by a newly identified difference here.
core.c reset_check clears GCTL RAMCLKSEL bits7:6, as current XNU does;
gadget.c switches RAMCLKSEL later on connection-done, so moving that
switch before the failed resource command would depart from this source.
Failure-time PHY snapshot is the next discriminating existing diagnostic;
no new register change selected solely from the two command lines.


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


##0227 bit31 restoration;0228 post-reset wake candidate

0227 physical first resource cmd2 remains402/PAR0=1. TEST0/PHYPIPE10,
CLK801b0048, retained session bits and event CSR. Helper required CLK31
clear earlier; restoration point unknown.0228 logs pre-reset and endpoint
states, clears only link-controlled suspend CLK31 after DCTL reset, waits
500us and requires exact readback. No new reset/reference/PLL/mux change.
ARM64/models PASS; hardware effect unverified. Download Mode059 ready.

##0227 verified hardware trial

CI44331761587 SUCCESS; source/profile and preserved BOOT packaging checks
PASS. Fresh Download Mode058 accepted BOOT100%,exit0/reboot; only BOOT
written. Physical continuation after RETENABLEN guard pending; no USB pass.

##0226 RETENABLEN readback;0227 guard correction

User's last0226 USB line: CLK801b0049->001b0048, PIPE0->10. The exact
source guard compares all CLK bits and therefore returns because requested
RETENABLEN bit4 did not latch. It exits before PHY power-up, so there is no
0226 endpoint-command result.0227 keeps the bit4 write/log but masks only
that readback bit; continues to require reset/common/ref controls and PIPE
free-clock readback. This probes further sequence progress without relaxing
the measured reset/clock routing checks. ARM64 and modeled ignored-bit4/
refusal tests PASS; runtime pending.

##0226 verified hardware trial

CI44324136923 SUCCESS,11-source/6-symbol/38-diagnostic profile checks pass.
Fresh Download Mode057 accepted BOOT100%,exit0/reboot; only BOOT written.
Physical free-clock/PHY power/resource result pending. No USB success claim.

##0225 cmd2 persists;0226 common-block/free-clock candidate

Physical0225 TEST0 yet first resource cmd2 active402/PAR0=1; CLK801b0049,
PHYPIPE0. Samsung8895 CAL uses common_block_disable=false/CLKCORE and
under PORTRESET clears CLK31/0,sets4/19,selects PHYPIPE free UTMI clock4,
waits10us,releases reset then powers PHY.0226 preserves measured reference/
PLL/SSC/divider fields while applying these controls on primary/CLKCORE
only. Exact readback after500us; predicts CLK001b0058/PHYPIPE10. No
secondary bank/CMU/PMU/mux changes. ARM64 and modeled suites PASS;
physical clock/endpoint result remains unverified.

##0225 physical power-bit result

User confirms TEST0000000c->00000000/SEL0 and later TEST0/PIPE0, followed
by endpoint0 setup failed. Primary power-bit release works; no endpoint or
USB traffic success. Exact failed command from0225 requested;0224 cmd2
must not be treated as a measured0225 result. Clock/PLL readiness unproven.

##0225 verified hardware trial

CI44316294206 SUCCESS;11source/6symbol/36string/profile and original BOOT
component/fit/hash checks PASS. Fresh Download Mode056 BOOT100%,exit0/reboot.
Only BOOT written. Physical PHYTEST release/resource progress pending;
no USB success inferred. Exact hashes/artifacts in active handoff.

##0224 confirmed PHY power-down;0225 targeted release

Physical0224 CSR: DCFG80800/HW1=0160c93b; EVT82cad000/8/80001000/0.
POWER TEST=c PIPE=0. Pinned CAL header defines bits2/3 POWERDOWN_HSP/SSP;
both asserted.0225 clears only these primary-bank bits after existing link
wake, preserves other fields, waits1000+500us, checks exact readback and
refuses nonprimary mux (SEL low6bits nonzero). Post-device-reset power bits
must stay clear or startup stops. No PLL/clock/PMU/secondary changes.
ARM64, modeled preservation/refusal and existing USB suites PASS; hardware
result untested. Root cause remains a hypothesis until physical progress.

##0224 physical CSR result

User confirms event CSR verified DMA82cad000/00000008,size80001000 and
STARTCFG completed reg9; first resource cmd2 remains active402, PAR0=1,
PAR1/2=0. LINK08000180/UTMI660 retained. Event-ring register readback does
not prove bus-master DMA. USB CSR/POWER lines omitted in submitted report;
requested exact values or explicit absence. No USB success or new flash.

##0224 verified hardware trial

CI44308837527 SUCCESS,11 compiled sources/6 symbols/33 strings/profile
verified. Fresh Download Mode055 accepted0224 BOOT100%, exit0/reboot.
Only BOOT written. Event CSR/STARTCFG/CSR/POWER physical report pending;
no USB functionality established. See active handoff for exact hashes.

##0223 physical result;0224 CSR/power diagnostic candidate

0223 reaches USB; phase5 stop did not recur. Session bits now retained:
LINK08000180/UTMI660, Q7e00,CLK801b0049. Still first EP0 resource cmd2
active402, PAR0=1, others0; GCTL80e92004/GSTS3e800000/USB2=40102400,
DCTL0,DSTS00520000,EN0. DCFG after reset80804. No USB success.

0224 checks the actual event ring address/size readbacks before endpoint
commands (Samsung core.c reset_check checks event-address CSR access).
On mismatch it stops without a new reset or endpoint write. Adds failure
DCFG/HW1/event-ring and already-mapped PHYTEST/PHYPIPE readbacks to check
unmeasured power-down and CSR state; logs completed STARTCFG register.
No new power/clock/reset programming. Actual ARM64 compile, wrapper,
EP-command/resource tests and plain-patch/full-source equality PASS.
Physical effect untested; this is diagnostic, not a claimed USB fix.

##0222 hardware trial (2026-11-18)

Exact CI44285281557 SUCCESS with9 sources/6 symbols/16 diagnostics and
BOOT packaging verified. Download Mode053 accepted0222 BOOT100%/exit0/
reboot. Only BOOT written. Host no1209:0001/no ECM. Physical session
LINK/UTMI before endpoints and later commands/events requested. No physical
USB success established; session-order change remains a hypothesis.

##0221 physical result;0222 session-valid ordering

Physical0221 USB2CFG40102400/Q7e00 retained, reset1ms/GCTL30c12004/DCFG4,
but first SETTRANSFRESOURCE cmd2 reg402 still times out. PHY LINK08000000
UTMI60 lacks session-valid bits: current helper ran only after failed setup.
Pinned CAL sets FORCE_BVALID/VBUSVALID and VBUSVLDEXTSEL/EXT during PHY init
before device reset/endpoints.0222 moves existing helper before DCTL reset,
reasserts after reset and prints LINK/UTMI before commands. No new PLL/power
sequence; root cause remains a hypothesis. Actual ARM64/three host suites
PASS, full CI44285281557 dispatched. Download Mode053 ready;0221 installed.

##0221 hardware trial (2026-11-18)

Exact CI44276126788 SUCCESS,9 sources/6 symbols/15 diagnostics and BOOT
packaging verified. Fresh Download Mode052 accepted0221 BOOT100%, exit0,
reboot. Only BOOT written. Host no1209:0001; physical USB2CFG/resource/event
trace requested. Actual post-reset wake retention and USB success unproven.

##0220 physical result and0221 reset-order correction

User confirms Q7e00 LINK08000000 SEL0, but ep0cmd2 still active (reg402).
USB2=40102540 restores ENBLSLPM/SUSPHY bits8/6; prior0219 was40102400.
PHY version00010000,CLK801b0049,UTMI60. QACT took effect without solving
resource assignment.0221 reapplies the existing Samsung USB2 wake mask after
link reset and again after DCTL reset, before endpoints. No new tuning/mux
writes. Actual ARM64 compile and reset-default/bit-preservation tests PASS.
Full CI44276126788 dispatched; installed0220, no physical0221 success yet.

##0220 hardware trial (2026-11-18)

Exact CI44270585173 SUCCESS; nine source hashes/six symbols/fifteen linked
markers and BOOT packaging verified. Fresh Download Mode051 accepted0220
BOOT100%, Heimdall exit0/reboot. Host no1209:0001/ECM yet. Requested physical
link-wake Q/LINK/SEL and subsequent command diagnostics. Source-derived
QACT/link reset remains a hypothesis until runtime readbacks/progress arrive.
Only BOOT written; no Android restoration. Older candidate states follow.

##0219 PHY evidence and0220 wake candidate (2026-11-18)

Physical0219: ep0 cmd2 reg402, PAR0=1/PAR1=0/PAR2=0; PIPE010c0002,
HW3=10420085,BUS22220001/300; PHY LINK08000000,UTMI60,CLK801b0949,
Q7c00,SEL0. STARTCFG completes but first SETTRANSFRESOURCE stays active.
Resource-before-config ordering did not fix command execution. FORCE_QACT
bit9 is clear despite automatic QACT sources disabled. This is evidence
for testing Samsung CAL enable sequence, not proof of the root cause.

0220 applies exynos_cal_usbphy_q_ch(enable=1) before existing DCTL reset:
500us waits, force QACT,10us LINK_SW_RESET pulse. Primary clock bank only;
refuses secondary PIPE clock/preasserted link reset; retains port mux,
reference/PLL tuning and unrelated bits. Modeled sample Q7c00 becomes7e00.
Actual ARM64 compile and wrapper/EP/resource suites PASS. Full
CI44270585173 live; not flashed. Existing0219 physical diagnostics retained.

##0217 endpoint command snapshot (2026-11-18)

Phone reports ep0 cmd1 reg00000401; PAR0=00000200/PAR1=00000500/PAR2=0;
GCTL80e92004/GSTS3e800000/USB2=40102400; DCTL0/DSTS00520000/DALEPENA0.
CMDACT remains set, so this is incomplete SETEPCONFIG, not status0 success.
Parameters encode64-byte OUT EP0 with expected events. Device mode is2;
USB2 reset/SUSPHY/ENBLSLPM and GSTS CSR timeout are clear. Stopped/halted
state is expected before the later RUN request. No USB enumeration proof.
0218 follows Samsung resource-before-config ordering; full CI44261810052
succeeded and BOOT0218 is now installed; physical result pending. Prior GHWPARAMS3=10420085 has16 IN/16 OUT, within candidate bounds.

## Current diagnostic trial (2026-11-18)

Latest:0219 exact CI44265115339 at41f5575 SUCCESS; nine source hashes,
six symbols and fourteen linked diagnostic strings verified. Fresh Download
Mode050 accepted BOOT0219 (100%, exit0/reboot). No host1209:0001 gadget;
physical four FAIL, one CORE and two PHY lines requested. No runtime PHY
or USB pass. Earlier0218 trial details below remain historical context.


0218 exact CI44261810052 at94e4d74 succeeded. Nine compiled sources,
six linked symbols and eleven diagnostic strings verified; BOOT uploaded
100%, Heimdall exit0/reboot. Host still sees no1209:0001 gadget; physical
resource-assigned or endpoint-failure report is pending. The resource-order
change follows Samsung gadget.c but has no demonstrated hardware success.
Earlier version/PE_lockdown_iokit apparent stops are superseded by physical
0215/0217 output reaching USB setup and Apple_HFS root discovery.

Prepared0219 outside active profile adds failure-only reads of DWC3 PIPE,
GHWPARAMS3 and bus config, plus the already-mapped PHY bank LINK/UTMI/CLK,
PHYRESUME(Q) and PHYSELECTION. Pinned Samsung CAL forces QACT and pulses
link reset before endpoint setup; the current takeover path does neither.
This source difference is a hypothesis, not proof of a clock fault. Read
those fields before changing Q-channel/port/reset behavior. No additional
MMIO writes or mappings in0219; actual ARM64 compile and modeled suites pass.

## Physical framebuffer evidence (2026-11-18)

Verified0214 BOOT flashed successfully and the user reads
`SWEET USB: endpoint 0 setup failed` on the phone. This establishes normal
XNU framebuffer output and execution past the DCTL soft-reset guard into
the five-command EP0 configuration sequence. The preceding command/status
or timeout line is required to isolate the failing operation. No host gadget
is present. Do not infer a working PHY, DMA or enumeration from this message.

0215 adds Samsung core.c USB2 ENBLSLPM/SUSPHY clearing and post-reset
66MHz GCTL timing; commit5439710, full CI44256127913 succeeded. Actual
wrapper host tests pass again on2026-11-18. Reviewed gadget.c uses the same
EP command register layout, CMDACT/status fields and EP0 configuration bits;
the failure is not yet evidence of an incorrect register address.

The target is a USB connection from the running S8 shim/XNU, with host-side
transfer verification. Android ADB recovery of last_kmsg is diagnostic support;
it does not meet that target.

## Measured controller state (2026-11-17)

Live DT identifies DWC3 at `0x10c00000`, IRQ SPI337 (INTID369), PHY windows
`0x10e00000+0x100` and `0x10e10000+0x100`, and a reference-clock selector
at `0x10e50070+0x10` (offset0xc, mask/value0x1000000). DWC3 clocks are
`aclk`/`sclk`; PHY clocks are `ext_xtal`/`aclk`. Both nodes declare
`is_not_vbus_pad`. DT permits SuperSpeed; current Android USB is high-speed.

The0210 pre-XNU snapshot and current Android debugfs regdump differ:

| Register | Loader0210 | Android configured |
| --- | --- | --- |
| GSNPSID | 0x5533280a | 0x5533280a |
| GCTL | 0x30c12004 | 0x80e92004 |
| DCTL | 0x00000000 | 0x8c000000 |
| DSTS | 0x00520004 | 0x00825188 |
| DCFG | 0x00080804 | 0x004808d4 |

Android also reports `GUSB2PHYCFG(0)=0x40102540`,
`GUSB3PIPECTL(0)=0x110c0002`, `GSBUSCFG0=0x22220009`,
`GSBUSCFG1=0x300`, `DALEPENA=0xf`. Its event ring has a nonzero upper
address word (`0x8`), so the working Android controller can DMA above4GiB.
This does not prove all shim DMA choices or XNU cache attributes are valid.
The private complete dump is in the ignored S8 backup directory. Do not
reuse Android's event-ring or endpoint DMA addresses after replacing Linux.

Loader DCTL.RUN_STOP is clear and DSTS.DEVCTRLHLT is set. Core register
access works, but this does not establish PHY readiness or an active USB link.

## Exynos-specific source reference

Reviewed Linux source from
[exynos8895/android_kernel_samsung_universal8895](https://github.com/exynos8895/android_kernel_samsung_universal8895/tree/3cfb914658ab077aef9ed500aa4a583782971fbf),
lineage-19.1 commit `3cfb914658ab077aef9ed500aa4a583782971fbf`:

- `drivers/usb/dwc3/dwc3-exynos.c`: Exynos8895 clock wrapper.
- `drivers/phy/phy-exynos-usbdrd.c`: selects PHY version01.1.1,
  CLKCORE reference, second register bank, GPIO-selected port and optional
  tuning. Power-on separately removes PMU isolation.
- `drivers/phy/phy-samsung-usb3-cal.c`:
  `samsung_exynos_cal_usb3phy_enable` checks the PHY version register and
  may advance the register base by4; sets q-channel/mux/reference clock;
  asserts port reset, delays10us, releases reset, delays500us; releases
  force-sleep/suspend and DP/DM pulldowns. With `is_not_vbus_pad`, it sets
  LINKSYSTEM FORCE_BVALID/FORCE_VBUSVALID and PHYUTMI VBUSVLDEXTSEL/
  VBUSVLDEXT. It clears DRVVBUS and sets OTGDISABLE. These settings are
  different from the donor Qualcomm QSCRATCH VBUS override.

These sources locate the required sequence; they are not proof that the
current phone runs precisely this source revision. Before a new PHY write
trial, inspect its register layout/version and preserve the device-specific
clock, GPIO port and reference selection. A blind copy of the S7, Qualcomm
or UNISOC initialization is not a validated Exynos8895 implementation.

## Next implementation gates

First recover reliable XNU output across the VM switch (0211 CI/trial).
Then implement S8 core/PHY initialization and a polled DWC3 gadget using
owned DMA buffers and explicit cache maintenance. The existing
`0073-sweet-usb-device-ep0.patch` provides a DWC3 control-transfer reference;
its Qualcomm clock/PHY accesses are not S8 code. Verify host enumeration,
control transfers, and bidirectional data while shim/XNU is running before
claiming working USB. Preserve all non-BOOT partitions.

## Opt-in ECM candidate0212

Overlay0212 enables the inherited polled DWC3 CDC-ECM transport for DREAMLTE
and starts it after BSD network initialization, before root-device discovery.
It never calls the donor UFS initialization or its disk-backed log stream.
`dreamlteusb=0` (default) performs no controller accesses; `=1` reports core
state; `=2` attempts firmware-state takeover for the measured DWC3 ID only.
It refuses a running core, PHY port reset or forced sleep/suspend. It sets
DWC3 device mode and uses the Exynos PHY VBUS masks above. Cold PHY clock/
isolation/reset initialization still needs device evidence and implementation.

The candidate initializes USB2 EP0 with64-byte packets and rejects malformed
or oversized event counts. Existing ECM configuration uses kernel interface
`ue0` at192.168.7.2/24; a host must configure192.168.7.1/24. Enumeration and
bidirectional transfer (for example ARP plus ping) must be measured on S8.
No runtime success is claimed from compilation or host modeling.

## Source-derived cold-start register map (2026-11-17)

Further review of the same pinned Linux revision resolves the clock and
isolation dependencies below. These addresses are implementation references;
none of these new clock/PMU writes has been tested on XNU.

| Dependency | Physical address / field | Source |
| --- | --- | --- |
| USB DRD isolation release | PMU `0x16480704`, bit0 set | live PMU node; phy-exynos-usbdrd.h and pipe3_phy_isol |
| PHY reference selector | `0x10e5007c`, bit24 set | live usbphy-refclk and change_refclk |
| FSYS0 USB clock user mux | `0x11000180`, select bit4, busy bit7 | cmucal-sfr.c / cmucal-node.c |
| USB link Q-channel | `0x11003044`, enable bit0, request bit1 | cmucal-sfr.c / clk-exynos8895.c |
| USB ACLK gate | `0x11002078`, manual bit20, value bit21 | cmucal-sfr.c |
| USB reference gate | `0x1100207c`, manual bit20, value bit21 | cmucal-sfr.c |
| USB suspend gate | `0x11002080`, manual bit20, value bit21 | cmucal-sfr.c |
| Upstream USB clock mux/divider/gate | CMU `0x15a81068` / `0x15a81864` / `0x15a8206c` | cmucal-sfr.c |

Live DT clock IDs `0x2ca` and `0x2bf` select GATE_USBTV_USB30DRD_LINK
and USBDRD30. PHY version01.1.1 uses CLKCORE, common_block_disable=false,
and an initial port0 selection overridden by the board GPIO. Do not infer a
port from cable orientation alone. PHY register-version adjustment shifts
both banks by4 when the first version word is nonzero.

The CAL sequence first handles Q-channel and link reset, preserves/selects
the PHY port mux, configures reference source/frequency under PORTRESET,
waits10us before releasing reset, powers both PHY banks for1ms then powers
down the unused bank, waits500us, releases sleep/suspend/pulldowns, and sets
the device VBUS overrides. PHYRESUME Q-channel forcing has500us delays;
it is separate from the FSYS0 clock-controller Q-channel above. Full cold
initialization must also retain board tuning and upstream clock rates.
Candidate0213 only attempts the already-awake PHY path; a refusal is not
evidence of broken USB endpoints. Framebuffer0214 is intended to expose
that refusal or an earlier kernel failure without restoring Android.

Host wrapper check against a staged source tree:

    python3 tools/dreamlte-usb-host-test.py PATH/TO/xnu/bsd/dev/sweet_usb.c

The test compiles the actual wrapper/PHY functions with modeled MMIO. It
checks default-off/read-only behavior, ID/running/reset/suspend refusal,
version-dependent register offsets, preserved control bits and VBUS masks.
It does not emulate the DWC3 endpoint/DMA engine or test PHY electrical state.
0211 must first be flashed/recovered using its own exact CI artifact; do not
claim that its kernel contains0212 merely because the local profile does.

Overlay0213 retains snapshot output after pmap bootstrap and registers a
RAM-backed serial console so normal kernel printf reaches the same bounded
buffer during BSD/USB setup. Snapshot aliases use LOW_GLOBAL_BASE_ADDRESS
plus2MiB/4MiB, within the reserved low-globals range. VM_MIN_KERNEL_ADDRESS
is a different L1 range on this4K non-large-memory kernel and is unsuitable.
No framebuffer, UART or storage accesses are needed for this console.

For a running gadget, `python3 tools/dreamlte-usb-check.py` issues real EP0
GET_DESCRIPTOR/GET_STATUS/GET_CONFIGURATION requests. After configuring the
host ECM interface at192.168.7.1/24, add `--interface NAME` to require its
USB parent/MAC identity and three ICMP request/reply exchanges. This helper
has only been checked for syntax/help and correct absence reporting so far;
no running S8 gadget has passed it yet.

## Host console completion check

After the exact ECM interface is configured at192.168.7.1/24, stop any
other UDP5140 listener and run:

    python3 tools/dreamlte-usb-check.py --interface INTERFACE --console-seconds 60 --console-log research/dreamlte/xnu-usb-console.log

This requires real EP0 transfers, three ping replies and identifiable
XNU UDP5140 text from192.168.7.2, saving validated bytes privately. Enumeration
or ping alone is not a console pass. A full bounded capture waits its window;
60seconds includes the poller's periodic30second status if no new boot text
remains. The receiver has actual loopback UDP tests, including split markers,
wrong peer, unrelated traffic, empty datagrams and silence. This host test
is not evidence of phone delivery;0233 has not enumerated at latest check.
