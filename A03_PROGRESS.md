# Galaxy A03 SM-A035G — active bring-up

## 2026-11-21 14:31 UTC — Physical button BOOT0127 running

ARM CI44912955041 succeeded at exact a17e9d8. Verified CI source and kernel
SHA256 76e2ab4b5a17b01dcd99c83683004fd5c035507460e1629315dd32bbb8852c1f.
BOOT0127 SHA256
33adcbc910bfcc1cd7ae0ba097bfb9c0401c47196d626689dffde27184dc5b98.
Same eight CPUs, 1984 MiB, ADT and root parameters with a03keys=1 added.
Explicit CDC Download reboot reached Heimdall and BOOT-only upload succeeded.
Sole reader PID30533/session68042, private boot0127-buttons-live.log.
All eight SGI checks pass, retained RTC works, storage ready/unpoisoned.
Button worker start=0, PMIC and GPIO init both 1, and backboardd opened
the HID service. Touch RAM load succeeded with ready A55A and streaming
resumed after one invalid startup slice. At 14:32 UTC iOS had submitted
seven swaps, completed five copies, and requested display sleep (value 0).
No synthetic input was sent. No physical key edges have been captured.
Physical test requested with USB attached first to match key, HID and
display records. The visible wake test with USB unplugged remains pending.

## 2026-11-21 — Physical button candidate

The live SM-A035G DT and matching stock overlay agree on power (SC2730 EIC1
active low), volume down (EIC4 active high), and volume up (AP GPIO125 active
low). Patch 0195 forwards debounced edges to the existing consumer HID service
from a separate kernel thread with `a03keys=1 a03_hid=1`. Polling runs without a
USB connection. Setup uses the stock data mask and input enable registers.
PMIC access uses the existing ADI lock. The worker requires a stable release
before accepting a press and releases/rearms a held key after repeated read
failures. Host sanitizer tests cover those cases and PMIC mask readback.
Both changed C files cross-compile for ARM64 using the previous CI flags.
The host compiler lacks Apple's allocation builtins for the full HID C++
unit. Full XNU CI run 44910781005 (job 136865936423) builds exact
a17e9d8ec339f166273bc6f489021d4e6e1e230a. A private pipeline waits for the
run, verifies sources and packs BOOT0127. Intel job finished Build at
14:03:47 UTC and remained in the linked-kernel verification step for over
eleven minutes. Two complete log downloads matched byte for byte, ending at
the build. No artifacts were published. The alternate macOS ARM run
44912955041, job 136872452726, builds the same commit. Both pipelines remain
live and serialize packaging. Physical screen wake remains pending.

## 2026-11-21: reported SpringBoard freeze, respawn and recovery

User reported a SpringBoard crash/frozen image, then confirmed the image
recovered. Fresh private capture springboard-20261121-live.log contains a
SpringBoard spawn and replacement PID98999 (original boot PID26); no captured
termination signal/reason, so do not assign a cause. PosterBoard repeatedly
crashes with the corpse-limit warning. Read-only GPU status:354041completed,
4verified,0fallback/quarantine,1806idle-releases,powered0; display request0,
all swaps completed. Storage ready1/poisoned0. Replacement SpringBoard sampled.
One explicit USB Home was sent before the user's recovery report: spontaneous
recovery versus Home response cannot be distinguished. Follow-up capture
springboard-20261121-followup.log confirms request1 and copies354521->355975,
GPU0fallback/quarantine. Physical recovery confirmed; no fix or crash-cause
claim. No flash/reboot/GPU controls/replay. Prior capture ended hours earlier;
prior600s soak has samples but no terminal PASS, and is not a completed gate.
Private logs remain ignored. Active goal: physical A03 buttons for sleep wake;
USB Home response is not physical-button support.

## 2026-11-21 03:50UTC: candidate passes first sustained failure point

BOOT0126actualcompositor2095completed/2413440000pixels/4verified,
0fallbackquarantine/idle11; no replay/GPUcontrols. Passes0123's2041failurepoint,
but earlier0125failed10935 so nofixclaim. First600ssoak67126 continues;
1800s/12000copyfollow-up88566queued onlyifcountinsufficient, notonGPUfault.
Sole168765/session9363captureuntil~04:12UTC. Physicalreplypending.

## 2026-11-21 03:48UTC: actual candidate copies advance; duration gate corrected

BOOT0126actualHome/swipe-triggeredcompositor now870GPUcopies/4verified,
0fallbackquarantine/idle9, no replay/GPUmodecontrols. Earlieridle request0
resumed viaexplicitHome; laterHome+swipeup generates sustained~10copies/s.
Thisisnotphysicalinputacceptance. Physicalimage/swipequestionpending.
The600s/12000copy planned gate is too short at observed~10Hz; host observer
nowdefaults1800s, retaining12000additionalcopyrequirement ratherthanlowering
it. Existing600strial continues as an intermediate observation, not expected
tofulfillcountgate. Needlongeractualtrialandfreshreadbacks/idle/paired/physical.
Nohardwarefixclaim. Sole168765/session9363captureuntil~04:12UTC;renewbeforeexpiry.

## 2026-11-21 03:45UTC: BOOT0126 automatic GPU proof passes; actual soak started

Autoboot verifierPASS activation->4full720x1600readbacks->fastcopy, no priorhost
GPUcontrolsorreplays. GPUON/cachedwarm384/defaultwait/tile4/idle100ms; first5
copies/4verified/0fallbackquarantine, idle3/powered0 observed afterretirement.
OneHome beforeproof and secondafterrequest0, thenoneUSBswipeup dispatch to
triggeractualcompositoractivity; nophysicalUIackclaim. Read-onlysoak67126
boot0126-compositor-soak.log started03:45UTC,600s/12000additionalcopiesrequired.
No replay/GPUmodecontrols duringinterval. Needactualprogressandnofailure,
thenfreshreadbacks/idle/paired/physicalgates. Sole168765/session9363loguntil
~04:12UTC. Goalactive;restoredjobendclean remainscandidate/notfixyet.

## 2026-11-21 03:43UTC: BOOT0126 kernel/touch/storage healthy; waiting compositor

All8SGI1PASS/retainedRTC1795232498 read without host sync. Volatile79104byte
FW staged/load0/A55A/config720x1600. Firststartupinvalidslice required one
explicit touchstart retry; streamingON. Storage ready1poison0. GPUdefaultOFF
beforefirstcompositorframe; zero submissions so noautobootproofyet. NoGPU
controls/replayissued. Sole168765/session9363 boot0126-boundary-live.log.
Verifierwaitsession87644 onlyreadslog, failsifquarantine. Needactivation/
4fullreadbacks/fastthen sustainedactualframes. Goalactive/nofixclaim.

## 2026-11-21 03:40UTC: candidate fullCI passes; BOOT0126 flashed

CI44860660965SUCCESS/exactede01ea4ac14ee411c7b5fd49bf4a279030a36c5.
Sixsourcesexact/XNU22.6/RTCunchanged/reverse0194/checksum/SMP/actualCI-source
blit+idlehook+rate+runtime+replayASanUBSanPASS. KernelSHA256
72b1806291eda316a68e07b8ca1cc5cc1e741480ec08228a4d4ce7e5298f754b.
BOOT0126SHA2569ab6b2d81c2fe76079780e3b87afe5f1c44ec6c71cf78eabaaf681136801773b.
Same8CPU/1984MiB/ADT0094/cmd593+a03gpu=1/stockramdiskDT. SyncDownload->
BOOT-onlyHeimdalluploadSUCCESS/reboot. Solecapture/session9363
boot0126-boundary-live.logwaitingCDC. NeedtouchFW/load/start andautomatic
4fullreadbacks->fast BEFOREGPUcontrols/replays; thenlongactualcompositor,
freshreadbacks/idle/pairedCPUoffload/physicalresponse.0193jobendflushcandidate
NOTyetfixclaim.0194boundedfailureevidence. CPU0124restorepreserved. Goalactive.

## 2026-11-21 03:29UTC: candidate CI verified live; artifact pipeline waiting

SameCI44860660965/exactede01ea/job136713035392 verifiedin_progressBuild.
No timeout restart/duplicate. Session34387/PID166002 waits for terminalsuccess,
then exactsource/RTC/reverse0194/checksum/SMP checks, actualCI-source sanitizer
fixtures and0126packing; it NEVER flashes. Phone remainsCPU0124 with sole
capture163479/session31133 until~03:45UTC. Observer now rejects concurrent
replay/GPUcontrols, preventing retainedframe contamination ofactualcopycount.
NewguardsPASS/aa8496a pushed; jobendwriteback-vs-freshackfixture bba5b4cPASS.
Goalactive. Need successfulCI/hardwarevalidation before claimingfix.

## 2026-11-21 03:26UTC: regression proves pixels do not bypass retirement

Expanded actual-code fakeDMA fixture models the restored automatic job-end
writeback independently from explicit CLEAN_INV. It makes panel pixels already
correct, then suppresses fresh explicit completion: driver still returnsfailure,
retains translation/source/scratch, quarantines and skips powerdown. ASanUBSan
PASS. Thus0193 does not accidentally turn correctreadback into retirementproof.
CI44860660965 exactede01ea/job136713035392 remainsin_progressBuild; no restart.

## 2026-11-21 03:21UTC: exact0193/0194 CI running; read-only soak prepared

CI44860660965 exactede01ea4ac14ee411c7b5fd49bf4a279030a36c5,
job136713035392 in_progress Build at03:24UTC. No duplicate.
Actualblit/idlehook/rate/runtime/replayASanUBSan and ARM64 compilation PASS.
Private gpu-boundary0193-work/artifacts.py+pack0126.py pin exactCI/source,
source22.6/RTC/checksum/reverse0194/SMP. Needfullsuccess->artifactactualtests
->BOOT0126. New host compositor-soak observer sends only read-only status,
requires12000additional actual copies over600s by default, failsquarantine/
fallback/policychange/counterregression/insufficientcopies; no replay/input.
GuardfixturesPASS. Realframesarestillrequired; observer alone provesnothing.
CPU0124 now4CPUcopies,request0 afteridle,touchON1024events0/storagehealthy;
this sleep episode is distinctfrom0125GPUstage5. Goalactive/physicalpending.

## 2026-11-21: candidate0193 restores job-boundary clean;0194 bounds diagnostics

Evidence-driven candidate, NOT hardware fix:0193 restores JS1 automatic end
CLEAN_INV (config83300 rather than cached80300), matching pinned vendor default
job-boundary flush policy. The explicit post-retirement CLEAN_INV and fresh
completion acknowledgement remain required. No timeout extension/retry/reset,
AS teardown or quarantine weakening. Restoring a removed optimization tests
whether job-boundary ordering explains stage5; root cause still unproven.
0194 splits failure-only read-only snapshots into four records below255bytes,
including GPU/core-ready/power-transition fields. Parser accepts complete legacy
or complete multipart evidence and rejects truncated/duplicate/missing fields.
ActualGPUcode fakeMMIO/DMA ASanUBSan and ARM64 C compilation PASS; profile140
staged. FullCI and hardware long-compositor/readbacks/idle/physical gates remain.
Phone staysCPU0124. No claim of faster walltime or GPU source rendering.

## 2026-11-21: CPU0124 restored after preserving stage5 evidence

Matching CPU0124 image SHA256869f9c901071ba12359a0613e10c63e158e880baa17debc291d8f13ee90e0190
verified before syncDownload and BOOT-only Heimdall restore; uploadSUCCESS/reboot.
New sole capturePID163479/session31133 boot0124-stage5-recovery-live.log.
All8cores SGI1PASS; retainedRTC1795230903 read without host calendar sync.
PrivatevolatileFW79104 staged/load0/A55A; first invalid startup slice required
one explicit restart, then streamingON. GPU remainsOFF/cached0/powered0/
quarantine0/0copies. Storage ready1poison0. Compositor recovered at03:17UTC: backboardd submitted two actual720x1600
BGRA frames using CPU copies. Physical visibleUI acceptance remains pending.
NoCIrunning. Rootcauseoffreshcleanackfailure remainsunfixed; goalactive.

## 2026-11-21: second BOOT0125 sustained trial reproduces cache-clean failure

Supersedes the preceding no-recurrence checkpoint. After re-enabling the same
cached/warm384MHz fast policy, actual compositor copies advanced10412->10935,
then0192 recorded stage5: fresh GPU CLEAN_INV completion missing. Job completion
was observed (submitted1/done1/irq00000002), JS/state/NEXT/ASstatus were zero,
MMU/ASfault zero, GPU RAW00000600 (clean-completion bit17 absent), AS translation
retained (lo049e4000/hi00000001/cfg62000006). The console truncated the long
snapshot after clock=38; idle-releases is missing, so the strict report parser
correctly rejected it. Do not infer the missing fields from this line. Separate
status confirms10935completed/391verified/67idle-releases/quarantine1/powered1,
0fallback, lastattempt54.064269ms/execute2.374230ms/retire0.

Read-only follow-up confirms vsync callbacks still advance (99779), display
request last-value1, swap entered12391/done12390 and copies12386 stopped; touch
stream remainsON. This failure is not explained by normal display sleep. It
identifies a missing cache-clean acknowledgement, not yet its root cause.
No reset, scratch reclaim, AS teardown, power-down or CPU overwrite was tried
under quarantine. Reboot is required before more GPU trials. Private evidence:
boot0125-retire-soak-live.log and boot0125-retire-secondtrial.log. CPU-control
BOOT0124 remains available. Next: shorten diagnostic records below console
format limits, investigate clean-command completion and retain strict guards.
Basic GPU goal remains active; physical reports of temporary working UI do not
establish sustained reliability.

## 2026-11-21 03:08UTC: sustained diagnostic trial10412copies, no recurrence; leftOFF

BOOT0125actualcompositortrial(no replaysbefore10025completed) passesprevious
2041failurepoint to10025actualGPUcopies afterHome/swipeup. No0192retirement
snapshot/quarantine/fallback. ThenfourrequestedfreshreadbacksPASS; ongoing
compositoractivityinverify1addedmorefullreadbackswhileOFFcommanddeclinedbusy.
Completedemptybusycommandswerenotassumedapplied; boundedexplicitOFFretries
finallyconfirmedOFFpowered0/verify1/10412completed/391verified/63idlereleases,
11994624000pixels,0fallbackquarantine. CPUcopiesresume12andadvancing. Storage
ready1poison0/touchON4367events0 atlasthealthcheck. Physicalimage/swipeacceptance
stillunverified. ThisdoesNOTfix0123:0192onlyread-onlyfailurelogging, original
retirementfailureintermittent/unreproduced. No timeout/cache/guardweakening.

Oldsole159238stoppedbeforeexpiry; newsolecapture/session97940
boot0125-retire-soak-live.loguntil~03:38UTC; originalboot/autobootproof/failure
watchlogboot0125-retire-live.logretainedprivate. NoactiveCI;0124CPUrestore
available. Nextreproductionshouldretain0192snapshotexactstage andregisters,
comparecoldvswarm/loadtimingandownershipratherthanblindtimeouts. Goalactive.

## 2026-11-21 03:00UTC: diagnostic sustained compositor exceeds prior failure point

BOOT0125actualHome+swipeup-triggeredcompositoractivity continues WITHOUT any
staticreplays; at02:59UTC5776GPUcompleted/6653952000pixels/4verified,
0fallbackquarantine,41idlereleases/384pollwaitcachedwarm1. Prior0123failed2041;
thislongerpassdoesNOTestablishfix:0192onlyfailurelogging, rootcauseunknown,
no retirement snapshot emittedyet. Actualsourceframeskeepadvancing request1;
noactualphysicaltouchevents. Needcontinuedcaptureorreproduciblefailurestage.
Sole159238/session38202boot0125-retire-live.loguntil~03:12UTC; renewbeforeexpiry.
NoCI,0124CPUrestoreavailable. Goalactive/physicalacceptancepending.

## 2026-11-21 02:50UTC: diagnostic boot active; actual compositor reproduction ongoing

BOOT0125all8SGI/RTChealthy; volatileFWload0/A55A/touchON1017events0/storage
ready1poison0. Automatic4fullreadbacks->fast/nohostGPUcontrolsverifierPASS.
FirstHomeprecedesrawpower0/noframes; secondHomeafteridleproducesrequest1/
36newframes. OneexplicitUSBswipeup then~249newactualcompositorframes; atlast
snapshot292completed/4verified/0fallbackquarantine, idle-releases11/384wait/
cachedwarm1. This isnewcompositorinput-triggeredactivity, notphysicaltouch
acceptance. Sustainedfailurehasnotyetrecurred; nofixclaim. Needlongeractual
activityand0192failurestage ifitrecurs. NoactiveCI. CPUcontrol0124restoreavailable.
Sole159238/session38202boot0125-retire-live.loguntil~03:12UTC. Goalactive.

## 2026-11-21 02:42UTC: diagnostic0192 CI success; BOOT0125 flashed

CI44856061555 SUCCESS exact2d4bf9085c197989dc30c05491268fad01debeb4.
Sixsourcesexact/RTCunchanged/reverse0192/source22.6/checksum/SMP/actualDMAstage+
vsynchook+rate+runtime+replayASanUBSanPASS. Privateverifierpatchpath corrected
beforevalidation; sourcefullSHA unchanged. KernelSHA256
 afa07d303c865948dc68ac461e5cd0fdb206cc48dfafe2ec64fd85a10caccd38.
BOOTSHA2567a0dbc94cd53ebfcc157381f8524371c0b1c53b968002c2abb62949193e12fa3.
Same8cores1984MiB/ADT0094/cmd593+a03gpu=1/stockramdiskDT. SyncDownload->BOOT-only
HeimdalluploadSUCCESS/reboot. Solecapture/session38202 boot0125-retire-live.log
waitsCDC. NeedtouchFW/load/start/autoboot4readbacks+fast then sustainedactual
Homewakecompositoractivity, notstaticreplayacceptance. Parser555ea32 mapsstage/
registersnapshotandrejectsmissingevidence.0124CPUrestorepreserved. Goalactive.

## 2026-11-21 02:33UTC: CPU-control runtime recovered; exact diagnostic build live

BOOT0124read-onlyGPUstatusOFF/cached0/warm0/powered0/frames0/quarantine0;
nohostGPUsetup. All8SGIverified/retainedRTC initialized. Volatile79104byteFW
staged+loadedresult0/A55A/config720x1600; touchstreamON4events0. Storageready1
poison0. Displaynow2actualCPUcopies/3.385msaggregate,0GPU; firstcompositor
outputrecoveredafterreboot. PhysicalvisibleUIstillunverified. CI44856061555
exact2d4bf90/job136698449738remainsBuild; do notduplicate. Privategpu-retire-work/
artifacts.py+pack0125.py pinexactfullSHA(noimage-numberglobalreplace), RTC,
source/reverse0192/checksum/SMP. NeedfullCI->actualASan->BOOT0125->longactual
compositortrial tocatchfailedretirementstage; nofixclaim.
Sole157092/session91200boot0124-cpu-live.loguntil~03:00UTC. Goalactive.

## 2026-11-21 02:30UTC: CPU control BOOT0124 restored; failure snapshot CI active

Quarantined0123 notreset/reclaimed/CPUoverwritten whilelive. SyncDownload->
BOOT-only0124flashSUCCESS/reboot. Sameexact0123kernel985328ce...ff365ac from
CI44853265071/bc4137c; command584 removesa03gpu=1 soGPUdefaultOFF, other
functionalflags/8cores1984MiB/ADT0094/stockramdiskDTunchanged. BOOTSHA256
869f9c901071ba12359a0613e10c63e158e880baa17debc291d8f13ee90e0190.
Sole157092/session91200 boot0124-cpu-live.logwaitsCDCuntil~03:00UTC; restore
volatiletouchFW/load/start, confirmCPUframes/time/io. NoGPUenableincontrolboot.

Diagnostic0192CI44856061555 exact2d4bf9085c197989dc30c05491268fad01debeb4,
job136698449738in_progressBuild. No duplicate. ActualASanstagefixturesPASS
cachetimeout5/staleack3/cleanfault4/slot1/ASdisable6; allretain/quarantine.
Privategpu-retire-work/artifacts.py+pack0125.py exactrun/sources/RTC/0192/SMP
ready. NeedfullCI->actualartifacttests->BOOT0125->sustainedactualHomecompositor
activityuntilfailure/snapshot. Do nottreatmorestaticreplaysasfix. Goalactive.

## 2026-11-21 02:27UTC: sustained compositor failure supersedes replay acceptance

After64additionalcoldcycles+freshreadbacks+pairedPASS, ONEHome at02:24UTC
triggered1388newactualGPUcompositorcopies(653->2041) over~34s. Thenretirement
unproven logsanddriverquarantinesDMA/preserveswiredscratch+source; panelwrites
suppressed. Status2041completed/2351232000pixels/quarantined1/fallback0,
warm1powered1(retainedbyquarantine). Executephase2.083ms, retire/verify0,
lastattempt56.574ms; exactfailedguard notlogged. USB/time/vsync/touchstream/
storage remainalive. Subsequent synthetic swipe dispatchedafterfailure, noUI
ackclaim. This is NOT merelydisplay sleep: requestlast1, in-flight swap never
finished/copiesstop and GPUquarantineexplicit. ActualsustainedUIacceptanceFAIL.
Noattempttoreset/reclaimDMAorCPUoverwrite underquarantine. Rebootrequired.

0192 addsfailureonlyread-onlyregister snapshot withstage1slot/ASwait,2priorGPU
fault,3staleack,4faultduringclean,5missingfreshclean,6ASdisable,7ASrestore.
No timeout/cache/retirement weakening, reset,retry,powerofforrecovery. Existing
faultinjectiontests exerciseexactstage andretainmappings/suppressshutdown.
ActualASan/ARM64/profile138PASS. NeedfullCI->diagnosticBOOT->reproduceactual
compositorfailure; do notclaimfixedfrommorestaticreplays. PlanCPUcontrolBOOT
restoreusingexact0123kernelwithouta03gpu whilediagnosticbuildruns. Goalactive.

## 2026-11-21 02:24UTC:64more cold cycles and current-image CPU offload PASS

BOOT0123enabledidlepolicy unchanged.64additional observedpoweroff/coldresumes
PASS(completed562..625,releases82..145), mediancold2.650231ms,min2.417576,
max2.954807. FourfreshfullreadbacksaftersoakPASS; restoredfastON/powered0,
629completed/12verified/147releases/0fallbackquarantine,touchON1817events0,
storageready1poison0. Current0123paired3roundsx8PASS: CPUwallmedian1.532567/
GPU2.065918ms; submitterCPU1.533552/GPU0.821230ms(46.45%less). Thisisactual
copyCPUoffload, notfasteranimation/system/renderingCPUclaim. NoactiveCI.

OneexplicitHome+swipeup diagnosticsequence started02:24UTC aftermeasurements
tocollectnewcompositorframes; distinctfromphysicaltouch. Physicalanswerstill
pending. Noextrashader/kernelchangejusttopassreplays. Docsactivecheckpoint
correctedfromstale0119/OFF to0123automaticidlepolicy. Goalactive.
Sole154528/session47211boot0123-idle-live.loguntil~02:42UTC.

## 2026-11-21 02:20UTC: BOOT0123 idle/cold/stress hardware validation complete

512stresscopiesPASS+4freshfullreadbacks,0fallbackquarantine. Meanwall2.055193ms,
submitterCPU0.843793ms. Combinedautoboot/12coldresume/stress final561completed/
646272000pixels/8verified; idle-releases82/powered0 whileenabled1fast. Default
384APB11/11/31,pollwait,impldef0,tile4,cachedwarm1. TouchON1037slices/events0;
storageready1poison0. LeftGPUenabled (unlike priortrials) becauseautomatic
retiredidlepowerrelease now hardwarevalidated. NoactiveCI, worktreecleanbefore
thisrecord. BOOT0123sourcebc4137c/CI44853265071 andexacthashes recordedabove.

Goalstillactive: thisisusefulframebuffercopyCPUoffload withautoboot/idlepower/
coldresume andexplicitOFF, notGPUsource-rendering/MetalEAGL orfasterFPS.
Physicalimage/swipequestionstillunanswered, allrecenttouchtrials0events;
unpluggedrestartunverified; knownPosterBoardcrashes/sleepdisplayhandlingremain
separate. Do notinventphysicalacceptance ormarkgoalcompletefromreplaycounts.
Sole154528/session47211boot0123-idle-live.loguntil~02:42UTC; normalpolicyON,
idlepowered0. NextphysicalUIacceptanceandlongeractualframeobservations; keep
anynewworkgroundedinevidence, avoidshaderchurnorCPUlatency-onlyclaims.

## 2026-11-21 02:19UTC: BOOT0123 autonomous idle release and12cold resumes PASS

NoGPUcontrols/replay beforeactivation->4fullreadbacks->firstfastcopy; autoboot
verifierPASS. At2verifiedframes read-onlystatusshowsidle-releases1/powered0;
at4verified releases2/powered0. ONEHomeafterrawpower0 hasdelayedrawpower1+
fastframes, againrawpower0; noperiodicHome. Twelvehostretainedframecycles each
observeautomaticpowered0 thennewGPUcompletion withunchangedqualification/
mode/rate/poll. Releases5..16, completed34..45, all0fallbackquarantine.
Coldlastcopytimes~2.50-2.69ms. ThisisGPUcoldresumption, notphysicalswipe/UIproof.
64x8stressstartedaftercycles; need4finalfreshreadbacks andidlepowered0health.
Sole154528/session47211boot0123-idle-live.loguntil~02:42UTC. Physicalquestion
pending;touchstreamlatest331events0. Goalactive; Metal/EAGLsource renderingabsent.

## 2026-11-21 02:12UTC: idle-release CI success; BOOT0123 flashed

CI44853265071 SUCCESS exactbc4137cfc886f86155e08a0d95a41bc620122967.
Sixsourcesexact/RTCunchanged/reverse0191/source22.6/checksum/SMP/actualDMA+
vsynchook+rate+runtime+replayASanUBSanPASS. PrivatepackSHAcheckcaught typo
introducedby0122->0123 textreplacementinsidecommitSHA; corrected BEFOREpack,
exactfullSHA revalidated. KernelSHA256
985328ce22bc544bce4528d8adfce7c7d77480d4869c4d93a4c6233aaff365ac.
BOOTSHA2569f03fb56d25a6f4c63a588c865eff094d47ec4abed621cde7c27bba7795c9314.
Same8cores1984MiB/ADT0094/cmd593+a03gpu=1/stockramdiskDT. SyncDownload then
BOOT-onlyHeimdalluploadSUCCESS/reboot. Solecapture/session47211
boot0123-idle-live.log waitsCDC. NOhostGPUcontrols/replaybeforeautobootproof.
RestorevolatiletouchFW/load/start; waitfirstframes; tools/a03-verify-gpu-boot.py,
thenidle-cycle.py12cycles/stress512+freshreadbacks/physicalUI. Hostcyclehelper
b36d9d0parsesidlecounterandrejectspolicy/fault/qualificationchanges. Goalactive.

## 2026-11-21 02:00UTC: idle-release CI active, hardware checkpoint restored

CI44853265071 exactbc4137cfc886f86155e08a0d95a41bc620122967/job136689379518
in_progress; correct13.5/SWEET/A03iOS/macOS26intel/fulltree. Noduplicate.
Privategpu-idle-work/artifacts.py+pack0123.py pinsixsources/RTC/reverse0191/
checksum/SMP; plannedBOOT0123same593bytea03gpu=1. NeedfullCI->actualartifact
ASan(vsynchook+DMA+rate+runtime+replay)->BOOT-only->autobootproof/idlepowered0/
coldresumequalification/stress/physicalUI. Sole150953/session16774/log
boot0122-bootpolicy-live.loguntil~02:19UTC; watchsession3854ci-watch.log.
Current0122restoredexplicitOFFpowered0verify1/384pollwaitcachedwarm1,
549completed/8verified/0fallbackquarantine,touchON1225events0/storageready1
poison0. NoactiveGPUkeepalive. AutonomousstartuphardwarePASS, idle-release
candidateonly, physicalanswerpending. Goalactive.

## 2026-11-21 01:58UTC: bootpolicy stress PASS; idle-release candidate0191

BOOT0122autonomousproof remainsPASS (4fullreadbacks thenfast/nohostGPUcontrol).
64x8stressPASS512copies+4finalfullreadbacks/0fallbackquarantine, meanwall
1.988864ms/submitter0.832096ms. RestoredexplicitOFFpowered0verify1/384pollwait/
cachedwarm1,549completed/632448000pixels/8verified0fault. TouchON1225events0;
storageready1poison0. Physicalanswerpending. WarmGPUstayedpoweredafterraw
power0sleep, so normaldeploymentneedsidlepowerrelease. No source-renderinggain.

0191existingvsynctimer calls nonwaiting sharedowneridlehook UNDERframebufferlock.
After100mswithoutsuccessfulGPUframe, reuseexistingwarm_stop(slot/ASownership
checks) andpoweroffowned sequence. Busyownerskip; poisonedDMAneverpoweredoff;
uncertainASquarantine; nextframeusesexistingcoldstart andretainsqualification.
No newtimer/interrupt/PMIC/PLL orpanelpowersettings. ActualDMAASan deadline/
busy/reacquire/ASquarantine/nooptestsPASS; actualvsynchooklockorder/notify/rearm
ASanPASS; rate/runtime/replaytestsPASS; ARM64GPUAMFIPASS; framebuffer syntaxPASS
withhost-onlyApplebuiltin stubs; profile137PASS. NeedfullCI/BOOT0123autostart+
idlepowered0+newframecoldresume/readbacks/stress/physicalUI. Goalactive.
Sole150953/session16774boot0122-bootpolicy-live.loguntil~02:19UTC.

## 2026-11-21 01:54UTC: BOOT0122 autonomous qualified GPU startup PASS

No hostGPUcontrols/replays beforeactivation. Firstcompositorframe logs0190
cachedwarm384/defaultwait activation, then4full720x1600 readbacks each
mismatches0/done1/retired1/PASS1. iOSrequestsrawpower0sleep after4copies;
ONEHome dispatched, delayedrawpower1 thenfirstverify0copy. LogverifierPASS
{full_readbacks:4,fast_copy:true,prior_host_gpu_mutations:0}. No explicit GPU
initialization/modecommand supplied. This proves host-command-independent
GPUstart with cableconnected; physically unplugged/coldboot independence
remainsunverified. SourceCPUrendering/MetalEAGLunchanged.

Read-onlystatusthen33completed/38016000pixels/4verified/0fallbackquarantine,
enabled1cachedwarm1powered1/384pollwait/impldef0tile4. Storage ready1poison0;
touchstreamON607events0. Physicalquestionpending. New64x8stressstarted after
startup proof, final4freshreadbacksrequired. Sole150953/session16774captures
boot0122-bootpolicy-live.loguntil~02:19UTC. Goalactive; pendingphysicalUI,
sustainedtests/idlepower policy and usefuldeployablebasicGPUoffload.

## 2026-11-21 01:49UTC: qualified boot CI success; BOOT0122 flashed

CI44849933946attempt2 SUCCESS exact e8306f9e90e412a9153a44caf38ea13ed07b0d8a.
Livecompilerlogconfirmedprogress01:44UTC, source22.6.0/sixsourcesexact/RTCunchanged/
reverse0190/checksum/SMP/actualDMA+rate+runtime+replayASanUBSanPASS.
KernelSHA256e8f07f5c2f18afb4a594a8e3c1a82b964064abdcf315ba61c69a841865d1d454.
BOOTSHA2569352488865c3c268234892a5e57e2fde5ccffd80fc84699e2550bfd44ca408bd.
Same8cores1984MiB/ADT0094/stockramdiskDT. Cmd593 removesonly-show_pointers,
appendsa03gpu=1. SyncDownload->BOOT-onlyHeimdalluploadSUCCESS/reboot. Newsole
capture/session16774 boot0122-bootpolicy-live.log waitsCDC. DO NOTsendhostGPU
controls/replays before autonomous activation+4readbacks+fast proof. TouchFW
stage/load/startallowed; display/time/statuspassiveallowed. Needlogverifier,
qualification/stress/physicalUI and normaldeploymentbehavior. Goalactive.

## 2026-11-21 01:43UTC: boot-policy attempt2 verified live; no new hardware artifact

CI44849933946attempt2 exact e8306f9/job136680652501 remainsin_progressBuild
(start01:31:47UTC), verified via jobAPI; no failure/usableartifact yet. Do not
restart/duplicate. Sole148860/session82510 boot0121-bootwait-live.loguntil~02:07UTC;
watchsession5403 gpu-bootpolicy-work/ci-watch-attempt2.log. ActualDMA/runtime/
stresssuccess-restoration/ratefullreport/autonomousproofnegativefixturesPASS.
Privateartifacts.py+pack0122.py ready; sixsources/RTC/reverse0190/source22.6.0/
checksums/SMP and actualASan mandatory beforeflash. BOOT0122cmd593 removes
only-show_pointers and adds a03gpu=1. No hostGPUcommands/replays untilfirst
fourverified+fastcopyproof usingtools/a03-verify-gpu-boot.py. Lastlive0121
GPUOFFpowered0/384pollwaitverify1/698completed16verified0fault,touchON4003
slices0events/storageready1poison0. Physicalresponsepending. Goalactive.

## 2026-11-21 01:37UTC: exact boot-policy rerun compiling; console renewed

44849933946 attempt2/job136680652501 in_progressBuild exacte8306f9. No duplicate.
Autonomousboot verifierf752930 andnegativefixtures PASS; actualDMA/runtime/
pollbenchmarkregressionsrerunPASS. Oldsole144533 intentionallystopped before
expiry; newsole148860/session82510 boot0121-bootwait-live.loguntil~02:07UTC.
Lastlive0121GPUOFFpowered0/384pollwaitverify1/698completed16verified0fault,
touchON4003events0/storageready1poison0. NeedfullCI/artifactverify+actualASan/
pack0122->BOOT-only->NOhostGPUcommands/replayuntil4readbacks+fastproof.
Thenpixelstress/physicalUI. Goalactive; noautonomousstartupclaimyet.

## 2026-11-21 01:30UTC: boot-policy CI network failure; exact failed-job rerun

44849933946 attempt1 terminalFAILURE beforekernelcompilation: git clone of
apple-oss-distributions/libpthread couldnotconnectgithub443 after28020ms.
Subsequentpackagingfailsbecausebuildnotcreated. Not an0190compilerfailure;
noartifactaccepted/nohardwarechange. Explicitghrunrerun--failed same44849933946
requested, exactsourcee8306f9 unchanged. Do notdispatchduplicate/restartlivejob.
Addedautonomousstartup logverifier+negativefixturesf752930: activationonce,
fourfull720x1600readbacks beforefast, nohostGPUcontrols/replaybeforeproof.
DoesnotclaimphysicalUI/cableindependence. BOOT0122privatepack593bytea03gpu=1
ready; needfullCI->artifactASan->BOOT-only->nohostGPUcontrolsuntilproof.
Current0121lastconfirmedGPUOFFpowered0/384pollwaitverify1/touchON; sole144533/
session9510until~01:41UTC. Goalactive; physicalanswerstillpending.

## 2026-11-21 01:24UTC: qualified boot policy CI active

CI44849933946 exacte8306f9e90e412a9153a44caf38ea13ed07b0d8a in_progress,
job136678627018. Correct13.5/DEVELOPMENT/SWEET/A03iOS/macOS26intel/fulltree.
No duplicate/restart. Privategpu-bootpolicy-work/artifacts.py+pack0122.py pin
run/sixsources/RTC/reverse0190/checksum/SMP. BOOT0122plannedcmd593bytes:
removeoptional-show_pointers from599bytebaseline, appenda03gpu=1(8bytes),
allfunctionalflags retained. Nextfullsuccess->actualASan->BOOT-only0122->
NOhostGPUcommands untilfirstframe, thenstatus/readbackqualification/stress/
physicalUI;touchFWhostrestore stillneeded. Current0121confirmed384pollwait/
GPUOFFpowered0verify1cachedwarm1/698completed16verified0fault,touchON/
storagehealthy. Sole144533/session9510until~01:41UTC. Goalactive.

## 2026-11-21 01:23UTC: wait preserves CPU offload; stress PASS; boot policy0190

Actualpoll384comparison: wait CPUwall1.674567/GPU2.078538ms, submitterCPU
1.674889/GPU0.870961ms. Counterspin CPUwall1.722745/GPU2.022442ms, submitter
CPU1.723072/GPU1.934687ms. Thus busyspin removesCPUoffload for littlewallgain;
defaultwait retained. New boundedstress helper runs64x8 acceptedframecopies
thenfourfreshfullreadbacks; actual512fastcopies PASS0fallback/quarantine,
meanwall2.014929ms/submitter0.869928ms, final4readbacksPASS. RestoreOFF/verify
confirmed384APB11/11/31pollwaitcachedwarm1;698completed/804096000pixels/
16verified0fault,touchON1680events0/storageready1poison0. Physicaltrial previously
added10actualGPUframes126vs116 thenrawpower0sleep; noactualtouchevents or
physicalanswer. Goalstillactive, sourceCPUrenderingunchanged.

0190 opt-in a03gpu=1 initializes validated clocks once under sharedowner at
firstcompositorframe; cached/warm384/defaultwait and fastAFTERexistingfourfull
readbacks. Missing/invalidarg preservesdefaultOFF; explicitcontrols override
bootinitialization includingOFFbeforefirstframe; read-onlystatusdoesnotdisable
optin. AnyfailedpreflightkeepsCPU, uncertainDMAstillquarantines. NoUSBneeded
forGPUstart, touchFWstillvolatilehostrestore. CorrectedobsoleteWFEcomment.
ActualDMAASan bootarg/missing/invalid/once/OFF/explicitpolicy/preflightcases,
rateASan/ARM64GPUAMFI/profile136PASS. NeedfullCI/BOOT0122witha03gpu=1and
NOhostGPUcommandsbeforefirstframe to prove deployment. Physicalacceptance
remainspending; nofullscreenGPUsource-rendering/MetalEAGLclaim.

## 2026-11-21 01:18UTC: BOOT0121 measures genuine submitting-thread CPU offload

Fullframe readbacks and two complete384/512 pairedthree8copytrials pass with
0fallback/quarantine. Firsttrial child results valid but top-levelJSON serialization
failed (tuplekey leftover from0188hostedit); originalmode/rate restored before
error. Fixedhostkey+successfulfullmain regression test in3df1c3a; repeatedwhole
hardwaretrial producesvalid finalJSON (boot0121-runtime-rate-retry.log).
Acceptedrepeat384: CPUwall1.396274/GPUwall2.027908ms, submitterCPU1.397245/
GPU0.842947ms(39.7%less).512: CPUwall1.401990/GPUwall1.974293ms, submitterCPU
1.402822/GPU0.812904ms(42.1%less). Priortrial384 submitter1.678303/0.836711,
5121.423759/0.810351. GPU walllatencyremainslonger; this demonstrates CPU
offload for the submitting thread, notFPSgain,total-systemCPU,or source-rendering
acceleration. Clean/setup/poll/readback costs included, blockedtime excluded.

Forphysicaltrial restored384/defaultwait; fourfreshfullreadbacks thenfastON,
116completed/4verified0fallbackquarantine,warm1powered1. ONEHome dispatched,
powerlast1. TouchON964slices/events0; physicalquestionpending. Sole144533/
session9510boot0121-runtime-live.loguntil~01:41UTC. NeedboundedphysicalUI/
sustainedactualframeevidence anddeploymentpolicy. No Metal/EAGL rendering added.

## 2026-11-21 01:10UTC: runtime observer CI success; BOOT0121 flashed

Correctsource CI44846854268 SUCCESS exact3d14c720278607e27fe4142b167a8fc9380e7759.
Wrongsource44846779804 terminalCANCELLED; noacceptedartifact. Sixsourcesmatch/
RTCunchanged/XNU22.6.0/reverse0189/checksum/SMP/actualruntime+DMA+rate+replay
ASanUBSanPASS. KernelSHA256
320e5407e65c1dc826917d27d9a84510aa595563e8e0fc13a12af09dbd99f0ae.
BOOTSHA256a4f3c20b8646e40483344a426f00565aa10cf00d3b2dd6578e8bad15b46a8346.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. SyncDownload->BOOT-only
HeimdalluploadSUCCESS/reboot. Solecapture session9510 boot0121-runtime-live.log
waitsCDC. Needclocks/cachedwarm/touchFW/acceptedframe->GPUOFF->fourreadbacks+
pairedsubmitterCPU/walltime384/512(defaultwait,optionalspin)->restore. Goalactive;
no0189hardwaremeasurement/physicalUI claimyet. Prior0120allreadbacksPASS but
GPU~1.96ms remains aboveCPU~1.67ms. TimerauditfoundcorrectMesa v9dispatch;
noGPUQoS/PLL/PMIC/IRQ changesmade.

## 2026-11-21 00:57UTC: runtime CI queued; BOOT0120 restoration rechecked

Replacement44846854268 exact3d14c72 pending behindwrongsource44846779804.
Bothnormalcancel andforcecancel accepted, butAPI stillreports wrongrunDeps
in_progress; treataslive, no duplicate replacement. Sole138803/session43018
expires~01:14UTC. Rechecked384APB(default), pollwait0/GPUOFFpowered0verify1,
165completed/190080000pixels/0fallbackquarantine, touchON2113slices/events0,
storageready1poison0. Displaylastrequest0 and idle; no periodicHome. Runtime
observer source/test/profile committed3d14c72, docsupdatede918a71. Needexact
fullCI validation/BOOT0121/readbacks+pairedruntime and physicalacceptance.
Goalactive; this turn produces real0188hardwareevidence and nextinstrumentation.

## 2026-11-21 00:55UTC: runtime observer CI dispatched on correct source baseline

Exact0189sourcecommit3d14c720278607e27fe4142b167a8fc9380e7759. Run44846779804
mistakenly usedmacos_version26.0; cancellation explicitlyrequested BEFORE
hardware; noartifactaccepted. Replacement44846854268 uses correct13.5source,
DEVELOPMENT/SWEET/A03/iOSuserspace/macOS26intel/fullbuildtree. Replacement
pending behindcancelledrun; do notduplicate. Privategpu-runtime-work/artifacts.py
andpack0121.py pinexactrun/sixsources/RTC/reverse0189/checksum/SMP. Actualruntime
helper+DMA+replayASan/benchmarkruntime+paired/poll/rate testsPASS; profile135PASS.
Current0120restored384pollwaitGPUOFFpowered0verify1/touchON/storagehealthy,
sole138803/session43018until~01:14UTC. Goalactive; physicalUI and usefulGPU
benefit unproven. NeedfullCI->actualartifacttests->BOOT0121->fourreadbacks+
pairedwall/submitterCPU/runtime comparison, then sustainedphysicaltrial.

## 2026-11-21 00:53UTC: counter polling hardware passes; no latency gain

BOOT0120 accepted384 pollwait/pollspin GPUmedians2.035014/2.029918ms,
pairedCPU1.487668/1.664534ms. At512 GPU1.964975/1.962125ms, pairedCPU
1.667826/1.672461ms. Eachpolicy earnedfourfresh fullreadbacks and three
paired8copyrounds. First384 and first512 trial discarded for extra background
compositor copies; retry logs alone supply accepted numbers. No polling
speedup established; execution remains~1.3ms. Counter gap time measured~10us.
Allacceptedreadbacks done1/retired1/mismatch0, fallback0/quarantine0.
Restored384APB11/11/31/pollwait/GPUOFFpowered0verify1/impldef0/tile4/cachedwarm1;
165completed/190080000pixels/verified0(resetrate). TouchON1086slices/events0;
storageready1poison0. Sole138803/session43018until~01:14UTC. NoactiveCI.
Private384/512-retry logs retain full exactcounter evidence.

0189 adds submitting-thread CPU-runtime counters beside copy wall time,
allowing GPUoffload to be distinguished from synchronouswait overhead. Uses
thread_get_runtime_self absolute ticks, includes sourceclean/setup/poll/readback,
excludes blocked/preempted time, failed/skippedframes excluded likeexisting
copycounters. Not total-system CPU or rendering-cost measurement. Actualhelper/
replay/DMAASan and benchmark parsing/reset testsPASS, profile135PASS. ARM64
C++syntaxcompilePASS with host-only substitutes for three unavailable Apple
XNU typebuiltins; fullCI mandatory, no deployablelocalC++object claim.
Needcommit/fullCI->BOOT0121/readbacks+pairedruntime+walltime->physicalUI.

## 2026-11-21 00:44UTC: polling CI success; BOOT0120 flashed

CI44844162892 SUCCESS exactcc4576ae04936dc1621b7621cc07ba698df31d7f.
Sixsources exactmatch/RTCunchanged/reverse0188/checksum/SMP/actualDMA+rate+
replayASanUBSanPASS. KernelSHA256
cc4ba8509cb88ed4628c5611415c8e0ab651d9b2891bf8a21de0709e4bef7d6b.
BOOTSHA2565f2569fce5b97255d24052e7cc38c6b793b8b932589926ae39a5fd4a10acd508.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. SyncedDownload then BOOT-only
HeimdalluploadSUCCESS/reboot. New sole reader session43018 captures
boot0120-poll-live.log waiting CDC. Need clocks/cachedwarm/touchFW/accepted
frame->GPUOFF->pollwait/pollspin paired384/512 fullreadbacks->restoredefault.
Private submitting-thread runtime observer prepared, notstaged/CI/hardware;
C++ localcompile blocked by baseline Apple-specific header compiler errors.
No hardware0188 performance or physicalUI claim yet. Goal remains active.

## 2026-11-21 00:36UTC: polling rationale corrected after timer-source audit

0188 remains an explicit comparison experiment, not a diagnosed WFE defect.
Read of exact BOOT0119 XNU reveals wfe_timeout_configure/init are invoked in
arm_init and enable CNTKCTL periodic events (nominal1us). Previous claim that
this port has no deadline wake event was too strong. Also ml_delay_should_spin
returns false with default cpu_idle_latency0, allowing delay10us to block and
reschedule in normal thread context. Counter polling can test combined wait/
scheduling overhead but cannot by itself establish broken WFE. No global timer
change is justified. Actual candidate DMA ASan/UBSan rerun PASS00:34UTC. CI
44844162892 still building exactcc4576; kernel candidate unchanged/defaultoff.

## 2026-11-21 00:33UTC: live idle episode supports display sleep

User asks whether stale clock is iOS sleep. BOOT0119 passive display status
shows last raw power request0, swaps143/copies137 stopped at12202384523/
12048499106 absolute ticks, while vsync50953 and kernel time continue. GPU
alreadyOFF/powered0, fallback0/quarantine0; touchstream1/slices2373/events0.
ONE explicit input home dispatch succeeds, records request1 at24473668578.
After about10s swaps439/copies433 and CPUcopies372 (previous76), vsync52834.
No reboot, fake clock/frame, periodic Home or GPU policy change. Strong sleep/
wake correlation for this episode; request enums/panel power transition and
physical visible recovery are not independently confirmed. Existing panel
retains the last image and observer does not implement display power changes.
PosterBoard crashloops remain a separate known problem. CI44844162892 still
building0188; no duplicate/restart. Current reader133832 remains sole owner.

## 2026-11-21 00:30UTC: polling CI active; host restore regression fixed

CI44844162892 in_progress exactcc4576ae04936dc1621b7621cc07ba698df31d7f.
No duplicate/restart. Kernelcandidate unchanged; hostclockhelper mistakenly
editedtuplekey wascaughtbyfailure-restorationtest and fixedcommit a5f75eb;
allhostbenchmarktests rerunPASS. Privategpu-poll-work/artifacts.py+pack0120.py
pinexactrun/sixsources/RTC/reverse0188/checksum/SMP. Needfullsuccess->actualASan/
BOOT-only0120->readbacks+pairedpollwait/pollspin at384and512->restoredefault.
Current0119GPUOFFpowered0/384verify1touchON,sole133832/session39451until~00:48UTC.

## 2026-11-21 00:29UTC: counter-bounded polling candidate0188

Previous goal turn progressed through0182..0187 hardware comparisons and
native16K mapping improvement. Goal remains active. New source audit identifies
machine_delay_until uses WFE with no local deadline event; delay10us may wait
for unrelated interrupts. This can inflate measured GPU execution latency.
0188 explicitpollspin uses architectural-counter bounded10us yield loop ONLY
for framebuffer completion/retirement/cacheclean polling. Defaultpollwait keeps
existingdelay; nointerruptmask/globaltimerchange. Iterationtimeouts, faults,
sourceownership/freshcleancompletion/retirement/quarantine unchanged. Reports
pollgapcount/time; benchmarks rejectmixedpollpolicy. HostactualDMA modes0..7,
helper boundedgap/default/nonframe path, ASanUBSan/ratehelper/ARM64/profile134/
benchmarkregressionsPASS. NeedfullCI/BOOT0120/readbacks+pairedpollwait/pollspin;
hypothesis nothardwareproof. Current0119GPUOFFpowered0/384verify1/touchON.

## 2026-11-21 00:23UTC: BOOT0119 hardware PASS1.969ms; CPU remains faster

Both384/512MHz fourfreshfullreadbacks+threepaired8copyrounds PASS. CPU384
1.672350/1.677052/1.690889ms; GPU3842.064879/2.018956/2.041745ms. CPU512
1.674447/1.399019/1.664846ms; GPU5121.969163/1.977956/1.962942ms. Median
GPU5121.969163 vsCPU1.664846ms, still18.3percent slower. Last512phasepower
0.048769/prepare0.094423/cache0.391807/execute1.309230/retire0.031692ms.
Singleexplicitendcleanworksbutdoesnotmateriallyimprovelatency. No cached
DMAvisibility/retirement failures, fallback0/quarantine0. Pixelreadbacks
compareall1152000pixels; verifiedcounterreset0uponrestoringrate384.

Finalstateconfirmed:384APB11/11/31,GPUOFFpowered0,verify1,impldef0,tile4,
cachedwarm1,61frames/completed61,70272000pixels. Touchstreaming1/389slices/
events0;storageready1/poison0. Solecapture133832/session39451,
boot0119-endflush-live.loguntil~00:48UTC. NoactiveCI, worktreecleanbeforethis
record. BasicGPUcopy isfunctional but measuredbenefit/physicalacceptance
remainunmet; goalactive. No Metal/EAGL source rendering added.

Nextinvestigation should target measured1.31ms GPUexecution +0.39ms CPU
sourceclean without removing ownership/lifetime/cachecompletion guards.
Native16Kmappingoptimization hasactualgain; tile/memattr/sourceclean/rate/
duplicateendflush trials alone do not closeCPUgap. Avoidanotherblindshader
rewrite orclaiming replay FPS/healthyUI. Physicaltouchacceptance pending;
sleepcorrelation andPosterBoardcrashloops remainseparate.

## 2026-11-21 00:17UTC: verified endclean CI success; BOOT0119 trial

CI44840823838 SUCCESS exact7607421e7dfeed0c335aa22ad1c5297f452ce0ca.
Sixsourcesexactmatch/RTCunchanged/reverse0187/checksum/SMP/actualDMA+rate+
replayASanUBSanPASS.
KernelSHA256a99f3c6a963a840ab2ca398807ec91e2ef4913ca7ca0e9c67d962b7edce897f9.
BOOT0119SHA2560319667042b42bfd0fff68be935f3f6bfa6e9b02336016c73da02d69e4cbce39.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. SyncedDownload thenBOOT-only
Heimdalluploadsuccess/reboot00:17UTC. Sole session39451captureboot0119-endflush-live.log
waitsCDC. Needclocks/cachedwarm/FWload/touchON/acceptedframe->GPUOFF->ratebenchmark
384/512(eachfourreadbacks+paired3rounds8copies)->restore384/physicalUI.

## 2026-11-21 00:00UTC: single verified endclean CI active

CI44840823838 in_progress exact7607421e7dfeed0c335aa22ad1c5297f452ce0ca.
No duplicate/restart. Privategpu-endflush-work/artifacts.py+pack0119.py pinexact
run/sixsources/RTC/reverse0187/checksum/SMP. Needfullsuccess->actualASan/
BOOT-only0119->fourreadbacks/pairedrates/executionphase->384restore.
Current0118confirmed384APB11/11/31/GPUOFFpowered0verify1impldef0tile4cachedwarm1,
80completed/verified0(resetrestore),0fallback/quarantine. Sole129991/session2940
boot0118-map16-live.loguntil~00:22UTC;renewifneeded. Goalactive.

## 2026-11-21 local /23:59UTC Nov20: native16K HW PASS; verified endclean0187

BOOT0118 fullframe mappings/readbacksPASS.384pairedGPUmedian2.055985ms.
First512comparison rejected because backgroundCPUcopies36vsrequested8;
original384/OFF restored. Fresh512-only threepairedrounds PASS, GPUmedian
1.982543ms. Mappingprepare~0.062-0.135ms vsprior~0.23ms, so actualgain,
but CPUstillfaster. Allacceptedreplays0fallback/quarantine. Finalrestoration
mustbecheckedagainbeforeidle. Sole129991/session2940boot0118-map16-live.log
until~00:22UTCNov21. No speedupoverCPUorphysicalUIcompletionclaim.

0187 cachedframebufferONLY omitsautomaticJS_CONFIG endflush since existing
explicitfreshGPUCLEAN_INV_CACHES alwayscompletesafterslotretirementbefore
CPUreads/ASdisable/fallback/shutdown. Startclean/invalidate preserved; uncached
andprivatediagnosticskeepautomaticendflush. Vendor79c7c8b jm_hw.c supports
SKIP_CACHE_END andregmap definesend0/noaction. This isNOTomittingfinalcache
ownershiptransfer. Hostmodelwritesstayhiddenuntilfreshcommand8/IRQ17; all
failurequarantinetestsPASS. ActualDMA/ratehelperASan/ARM64GPUAMFI/profile133
PASS. NeedfullCI/hardwarecorrectness/pairedexecutionphase; noHWclaimyet.

## 2026-11-21 local /23:51UTC Nov20: native16K validation CI success; BOOT0118 trial

CI44836868623 SUCCESS exacte8e3dee4d9ffa018199d2f6e975516606fbf9ce5.
Sixsourcesexactmatch/RTCunchanged/reverse0186/checksum/SMP/actualDMA+rate+
replayASanUBSanPASS.
KernelSHA2568e5a69be32acfbf1dd7d88b839ba06250b007775d5c860371c98d543e0eeec11.
BOOT0118SHA256bbb51c88e7ea48d5dbbe017a98eec5859fb99890fb2ad3e4226d3c4b761e70da.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. SyncedDownload thenBOOT-only
Heimdalluploadsuccess/reboot23:51UTC. Sole session2940captureboot0118-map16-live.log
waitsCDC. Needclocks/cachedwarm/FWload/touchON/acceptedframe->GPUOFF->ratebenchmark
384/512(eachfourreadbacks+paired3rounds8copies)->restore384/physicalUI.

## 2026-11-21 local /23:47UTC Nov20: mapping CI still live; capture renewed

CI44836868623/e8e3dee remainsBuild; live23:46:13compileroutput confirmsprogress.
No duplicate/restart. Oldreader125084 intentionallystoppedbeforeexpiry. New
sole129094/session93167boot0117-mapwait-live.loguntil~00:17UTCNov21. Current
0117GPUOFFpowered0/384verify1impldef0tile4cachedwarm1. Needexactfullsuccess/
artifacts.py+pack0118.py->actualASan->BOOT-only->fullreadbacks+pairedrates.
Privategpu-linear-work linearshadercompilesbutexpensiveintegerdivision; not
staged, notCI, nohardwareclaim. Goalactive; noGPUoverCPUspeedupyet.

## 2026-11-21 local /23:27UTC Nov20: native16K validation CI active

CI44836868623 in_progress exacte8e3dee4d9ffa018199d2f6e975516606fbf9ce5.
No duplicate/restart. Privategpu-map16-work/artifacts.py+pack0118.py pinexact
run/sixsources/RTC/reverse0186/checksum/SMP. Needfullsuccess->actualASan/
BOOT-only0118->fullreadbacks+pairedrates/mappingphasetimings->restore384.
Current0117GPUOFFpowered0/384/verify1impldef0tile4cachedwarm1/touchON. Sole
125084/session54578boot0117-clean-live.loguntil~23:49UTC;renewifneeded.

## 2026-11-21 local /23:26UTC Nov20: clean source HW PASS; native16K validation0186

BOOT0117 sourceCleanPoC fullframepasses;384/512eachfourreadbacks+paired3rounds
8copiesPASS0fallback/quarantine. GPUmedians2.201601/2.125841ms vsCPU1.728360/
1.795865ms; no clearcopygainfromCleanPoC and GPUstillnotfasterthanCPU.
Restored384APB11/11/31/GPUOFFpowered0verify1impldef0tile4cachedwarm1,
60completed/verified0(resetrestore),touchON632events0/storageready1poison0.
Sole125084/session54578boot0117-clean-live.loguntil~23:49UTC.

0186 validates CPU-native16KiB pagebase+end once, expandsfour4KiBGPUentries,
and rebuildsallmappings eachframe. No crossframe translationcache/lifetime
change. Sourcevalidrange/alignment/pageend and destinationphysicalextent
checksremain. SurfaceCPU mappings are native16K; noncontiguous nativepages
remain supported. ActualASanDMA tests reflect16K backing, endfault rejection,
noncontiguouspages/fullpagewalk/tails/cachefailure; fullframe source translation
count600 vs prior2400. ARM64GPUAMFI/ratehelperASan/profile132PASS. NeedfullCI/
hardwarecorrectnessandmappingphase+pairedtiming. No performanceclaimyet.

## 2026-11-21 local /23:18UTC Nov20: source clean CI success; BOOT0117 trial

CI44834205541 SUCCESS exact0aeb87285006e112783b5e47bd01e81ef2344591.
Sixsourcesexactmatch/RTCunchanged/reverse0185/checksum/SMP/actualDMA+rate+
replayASanUBSanPASS.
KernelSHA2563262a1d41413690b642e6349c468b0f338f4255deb2da4b783d12408390b3e2c.
BOOT0117SHA256ba7c925dbf9630b899326394d4e49e1ed6a359734fe6c9bfe509748bfa89231e.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. SyncedDownload thenBOOT-only
Heimdalluploadsuccess/reboot23:18UTC. Sole session54578captureboot0117-clean-live.log
waitsCDC. Needclocks/cachedwarm/FWload/touchON/acceptedframe->GPUOFF->ratebenchmark
384/512(eachfourreadbacks+paired3rounds8copies)->restore384/physicalUI.

## 2026-11-21 local /23:06UTC Nov20: source clean CI active

CI44834205541 in_progress exact0aeb87285006e112783b5e47bd01e81ef2344591.
No duplicate/restart. Privategpu-clean-work/artifacts.py+pack0117.py pinexact
run/sixsources/RTC/reverse0185/checksum/SMP. Needfullsuccess->actualDMA/rate
ASan->BOOT-only0117->fullreadbacks/paired384and512comparison. Current0116
restored384/GPUOFFpowered0/verify1/impldef0tile4cachedwarm1/touchON. Sole
122100/session86364boot0116-rate-live.loguntil~23:30UTC;renewifneeded.

## 2026-11-21 local / 2026-11-20 23:05UTC: stock512MHz hardware PASS; clean source0185

BOOT0116 both384/512MHz eachfourfreshreadbacks+paired3rounds8copiesPASS,
0fallback/quarantine. GPUmedians2.192980/2.127711ms vsCPU1.667466/1.663303ms.
512effectsmall; lastshaderexecute1.335ms vs3841.386ms. NoCPUoverGPUbenefit.
Restored384/GPUOFFpowered0/verify1/impldef0/tile4/cachedwarm1. Passiveprobe
confirmsAPB11/11/31.60completed/verified0(resetrestore),touchON643events0,
storageready1poison0. Sole122100/session86364boot0116-rate-live.loguntil~23:30UTC.

0185 replacesONLY sourceCPUFlushPoC withCleanPoC: sourceGPUmappingisRO/NX,
so CPU cache invalidation is unnecessary forGPU ownership. Kernel'snative
nonAppleimplementation emitsdc cvac+dsbsy. Descriptor/job CPUflush, GPUfresh
CLEAN_INV completion, readback/retirement/quarantine remainunchanged. No
skippedsourceclean or coherencyassumption. ActualsourceASanDMA+ratehelper/
ARM64GPUAMFI PASS; fullCI/hardwaretimingrequired. Goalstillactive.

## 2026-11-20: stock512MHz CI success; BOOT0116 trial

CI44831543349 SUCCESS exactce9bc57ce4f8e159a743183a2122181d8e20b2da.
Sixsourcesexactmatch/RTCunchanged/reverse0184/checksum/SMP/actualsourceDMA+
ratehelper+replayASanUBSanPASS.
KernelSHA2561a1ca22bae00d4079f42bcc7a1bc306b3701184176d5ef75adfa30f260afe5dc.
BOOT0116SHA256806327729f3910d482cfb2f9d04d12d8876261e38c58e6bd6ca3025c31a618c2.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. SyncedDownload thenBOOT-only
Heimdalluploadsuccess/reboot22:59UTC. Sole session86364captureboot0116-rate-live.log
waitsCDC. Needclocks/cachedwarm/FWload/touchON/acceptedframe->GPUOFF->ratebenchmark
384/512(eachfourfreshreadbacks+paired3rounds8copies)->restore384/physicalUI.

Private nextcandidate gpu-clean-work replaces ONLY sourceCPU FlushPoC with
CleanPoC (sourceRO GPUmapping), retainingGPUclean/retirement/readback. Actual
sourceDMA+ratehelperASan andARM64crosscompilePASS, not staged/profiled/CIyet.
TrackedtesthasoptionalCleanPoCstub uncommitted; keep until cleanfollowup.

## 2026-11-20: stock512MHz full CI active

22:45UTC CI44831543349 in_progress exactce9bc57ce4f8e159a743183a2122181d8e20b2da.
No duplicate/restart. Privategpu-rate-work/artifacts.py+pack0116.py pinexact
run/sixsources/RTC/reverse0184/checksum/SMP. Needfullsuccess->actualDMA+
ratehelperASan->BOOT-only0116->idleexplicit512/fourreadbacks/pairedCPUfast
and384restore. Current0115GPUOFFpowered0/impldef0/tile4/verify1cachedwarm1/
touchON. Sole118404/session97962until~23:07UTC; renewbeforeexpiryifCIwaiting.

## 2026-11-20: cache policy hardware PASS, no gain; stock512MHz candidate0184

BOOT0115 impldef/cacheall/writealloc eachfourreadbacks+paired3rounds PASS,
0fallback/quarantine. GPUmedians2.213971/2.191000/2.325096ms vsCPU1.428730/
1.535543/1.713596ms. No meaningful cachepolicygain; restoredimpldef0/tile4/
GPUOFFpowered0verify1cachedwarm1,89completed/verified0(resetpolicyrestore),
touchON695events0/storage ready1poison0. Sole118404/session97962 until~23:07UTC.

0184 explicitrate384/rate512 candidate changes ONLY GPUcore/mem parentselector
1(TWPLL/4)->2(TWPLL/3), keeps sysdivide4. Native b48e9dd ums9230-clk.c1590
parents and liveDT OPP512MHz750mV establish stockrate; inheritedrail still
exact1V validated, nevermodified. NoPLL/PMIC/DVFS-table writes. Requires
GPUOFF/no warmowner, allcores/L2/tileroff, idleJS/AS0/cleanIRQ, validatedPLL/
rail/domain/knownleafselectors. Gatesclosed beforeselectorschanged then
vendorenableorder, readbackID; failedstage rollsback masks, uncertainrestore
quarantines. Default384 unchanged, ratechange resetsfourreadbacks.
ActualhelperASanUBSan coversallsupplyvalues,liveowner/core/AS/fault/PLL guards,
eachwritefailure/rollback and quarantine; actualDMA at512fake-MMIO/mismatched
selector rejection, ARM64GPUAMFI/profile130/benchmark regressions PASS.
NeedfullCI/hardware512correctness+pairedcomparison+restore, no speedclaimyet.

## 2026-11-20: pixel cache policy CI success; BOOT0115 trial

CI44828092327 SUCCESS exact3ed3ad339ce0b4edfe23c50370dd8e2134ae9c1e.
Sixsourcesexactmatch/RTCunchanged/reverse0183/checksum/SMP/actualsource
lifecycle+replayASanUBSanPASS.
KernelSHA256b760ef93d481c06a2a1ccf85fd270758aa76503f8f8e42974a58238ace3e9338.
BOOT0115SHA2568c195289534641bb48f0693df6041206348fc2e125d77612c43bab0493adc345.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. SyncedDownload thenBOOT-only
Heimdall uploadsuccess/reboot22:36UTC. Sole session97962capture
boot0115-memattr-live.logwaitsCDC. Needclocks/cachedwarm/GPUONverify1/FWload/
touchON/acceptedframe->a03-gpu-memattr-benchmark.py (fourfreshreadbacksper
policy+paired3rounds8copies+restore). Hosthelper0530738PASS. No0183HWclaimyet.

## 2026-11-20: pixel cache attribute CI active

22:20UTC CI44828092327 queued exact3ed3ad339ce0b4edfe23c50370dd8e2134ae9c1e.
No duplicate/restart. Privategpu-memattr-work/artifacts.py+pack0115.py pinexact
run/sixsources/RTC/reverse0183/checksum/SMP. Needfullsuccess->actualASan/
BOOT-only0115->fourreadbacksperimpldef/cacheall/writealloc->pairedCPUfast.
Current0114GPUOFFpowered0tile4verify1cachedwarm1/touchON;sole114370/session7470
until~22:41UTC. Goalactive; dispatchsizetrialnotfasterthanCPU.

## 2026-11-20: tile hardware comparison PASS, no speed gain; cache attribute0183

BOOT0114 alltiles4/8/16/32 eachpassedfourfreshfullreadbacks+threepaired8copy
rounds. GPUmedians2.186067/2.204730/2.208019/2.254706ms; CPUmedians1.419230/
1.412235/1.422302/1.686197ms. No fallback/quarantine. Larger groups do not
improve thiscopy; tile4 default retained. Afterall restoredtile4/GPUOFF/
powered0/verify1/cachedwarm1,120frames/completed120/verified0(resetontilerestore),
touchON986events0. Sole114370/session7470boot0114-tiles-live.loguntil~22:41UTC.
Firsttrialdiscardedbusy-statusrace; correctedhelper retries onlyEMPTY read-only
status, neverreplay. QualificationthenOFFbeforepaired prevents expensive
backgroundreadbacks racing policyrestore. Hostregression/failurerestorePASS.

0183 explicitgpu blit impldef/cacheall/writealloc selects vendor pixelAttrIndex
0/1/2 onlyincachedmode; default0 unchanged. Vendor79c7c8b regmapUAPI defines
0x88impldef/0x8fforcecacheall/0x8dwritealloc; existingASMEMATTR table already
contains these. SourceRO/NX,destinationRW/NX,boundedpages, sourceflush/freshGPU
CLEAN_INV/retirement/quarantine remain. Policychange resetsfourreadbacks;
quarantinerejectspolicychange. Descriptor/code attributes remainindex0.
ActualsourceASanUBSan allthreepolicies/fullframe+partial/cleanfailure,
ARM64GPUAMFI/profile129/benchmarkisolationtestsPASS. NeedfullCI/hardware;
no newcacheperformancesafetyclaim. Goalactive, noGPUoverCPUspeedupyet.

## 2026-11-20: dispatch tile CI success; BOOT0114 trial

CI44824395202 SUCCESS exact2dc47e3ed8171a73e85c91ba42b5eb6dfbe41771.
Sixsources exacttestedmatch/RTCunchanged/reverse0182/checksum/SMP/actualsource
ASanUBSan lifecycle+replay PASS.
KernelSHA25652f73c0c5fdc087e00e86672d3836b844e6287c514b86ccf9baac4d8f59c3475.
BOOT0114SHA2568e63704cb8c54e4f5e7367ab7d45aed3233abc4b896f5d272762b089b6e690f7.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. SyncedDownload thenBOOT-only
Heimdall uploadsuccess/reboot22:10UTC. Sole session7470capture
boot0114-tiles-live.log waitsCDC. Needclocks/cachedwarm/GPUONverify1/FWload/
touchON->acceptedframe->tools/a03-gpu-tile-benchmark.py--tiles4 8 16 32,
fourreadbackspertile+paired3rounds/8copies+restoration. Hosthelper20072c8
qualification/policyisolation/resultparsing/failurerestorationPASS.

## 2026-11-20: dispatch tile full CI active

21:54UTC CI44824395202 in_progress exact2dc47e3ed8171a73e85c91ba42b5eb6dfbe41771.
No duplicate/restart. Privategpu-tiles-work/artifacts.py+pack0114.py pinexact
run/sixsources/RTC/reverse0182/checksum/SMP. NeedfullCI->BOOT-only0114->four
readbacks for eachtile4/8/16/32 thenpairedtimings. Defaulttile4 unchanged.
Current0113GPUOFFpowered0verify1cachedwarm1/29frames4verified0quarantine,
touchON. Sole109705/session30146until~22:13UTC; renewbeforeexpiryifneeded.

## 2026-11-20: fullscreen dispatch occupancy candidate0182

Continuation audit: previous turn made progress through BOOT0113 hardware,
paired timings and power-request correlation; goal remains incomplete because
GPU copy median2.153ms exceeds CPU1.580ms and physical acceptance is pending.
Currentcapture109705/session30146 stilllive21:51UTC; noactiveCI atstart.

0182 adds explicit gpu blit tile4/tile8/tile16/tile32, fullscreen only.
Default remains4; generic masked-tail dispatch unchanged. Exact shader uses
only global IDs and compiles IDENTICALLY for4 and16 localrows with pinned
Mesa24.3. Changing tile policy requires four fresh readbacks; owner/quarantine
and all cacheclean/retirement/lifetime checks remain. Groups15x4/8/16/32
contain60/120/240/480threads, grid3x400/200/100/50, exact720x1600coverage.
Nativev9 packers for every tile, actualsource ASanUBSan allpolicies+generic
fallback, ARM64GPUAMFI, profile128, benchmark regressions PASS. Benchmarks
reporttile_rows and reject within-interval/acrosspairedround policy changes.
NeedfullCI->BOOT0114->fourreadbacks perpolicy->pairedtiming, noHWclaimyet.

## 2026-11-20: BOOT0113 copy PASS2.15ms; display-power sleep correlation

Actual full720x1600 readbacks PASS0mismatches/done1/retired1, four verified
beforefast. PairedCPU1.668932/1.579903/1.425058ms; GPU2.178379/2.088370/
2.153456ms. MediansGPU2.153456vsCPU1.579903ms: still no speedup. All24fast
replaycopies completed, nofallback/quarantine. Latestbounded45sphysicalUI
trial added ONEactualGPUframe (28->29),2.660769ms/coldpower0.723692ms,
execute1.429230ms, nofault;touchON1115slices/events0. Physicalacceptance
pendinguserreply. RestoredGPUOFF/powered0/verify1/cachedwarm1,29frames/
4verified/completed29,0fallback/quarantine. Storage ready1/poisoned0.

Direct sleep hypothesis evidence now stronger: rawpowerrequest1 at5731465854,
then0 at6688243850, swaps stop54/copies52(last6997166155) whilevsynclive.
GPU alreadyOFF/powered0 atidleinspection. ONEHome dispatch causes new raw
request1 at8583702959 followedbyswap55/copy53 at8583959284. LaterCPU63/
swaps94/copies91, request remains1. This correlates iOS power request0 with
idle cessation and request1 with Home wake. Request enums/completed panel
power transitions are not independently proven; driver still preserves
selector12 error/panelbehavior. Thus sleep likely explains at least this
staleclock episode, not every UI fault. PosterBoard crashloops also remain.
No periodicHome or fakeclock/frame workaround installed.

Private untested NIR load-pipelining experiment stored only under
shim/a03/out/gpu-pipeline-work/fullscreen-experiment.c; tracked generator
restored to validated0180. No newCI or hardwareclaim. NextGPUwork should
use measured phases (~1.43ms execute + mapping/cache ~0.5ms) and find actual
benefit without removing cacheclean/retirement/sourceownership. BasicGPU
copy works, but performance/physicalUI gates remain; goal not complete.
Solecapture109705/session30146boot0113-quarter-live.log until~22:13UTC.

## 2026-11-20: coalesced strips/power observer CI success; BOOT0113 trial

CI44820099545 SUCCESS exactad0c30959b4607e032e77799acb8aa30d464f772.
Sixsources exacttestedmatch, RTCunchanged, reverse0180+0181/checksum/SMP/
actualsource lifecycle+replayASanUBSan+displaymethodtests PASS.
KernelSHA256484a5f787a39116022b8fb1c3f6ab7a886ec71b884443899a43f7de9769bc0ef.
BOOT0113SHA256353872d2202069d8dd05967b58027a7068b6faaf2ca7589422874100697e3be8.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. SyncedDownload, BOOT-only
Heimdall uploadsuccess/reboot21:42UTC. Sole session30146 capture
boot0113-quarter-live.log waitsCDC. Needclocks/cachedwarm/GPUONverify1/
FWload/touchON->fourfullreadbacks->pairedCPUfast/physicalUI. Also display
probe now reports raw power requests; no sleep or0180hardwareclaimyet.

## 2026-11-20: coalesced strips/power observer full CI active

21:25UTC CI44820099545 in_progress exactad0c30959b4607e032e77799acb8aa30d464f772.
No duplicate/restart. Privategpu-quarter-work/artifacts.py+pack0113.py pin
run/SHA/sixsources/RTC/reverse0180+0181/checksum/SMP before BOOT-only0113.
BOOT0112 now explicitlyGPUOFF/powered0,verify1cachedwarm1,33frames9verified/
completed33,0fallback/quarantine;touchON. Lastfast execute1.469769ms, whole
2.172038ms. Current bestpairedGPUmedian2.230663vsCPU1.668356: stillslower.
Solecapture106124/session85627boot0112-full4-live.log until~21:48UTC.
Goalactive; needhardware0180timing/physicalUI and0181sleeprequestevidence.

## 2026-11-20: BOOT0112 fullreadback PASS2.23ms; coalesced strips0180/power observer0181

BOOT0112 actual720x1600 readbacks zero mismatches/done1/retired1, nine
verified copies before fast. Paired CPU1.668356/1.684567/1.503557ms;
GPU2.262365/2.147485/2.230663ms, medianGPU2.230663 vsCPU1.668356ms.
Four-pixel fullscreen improves0111GPU4.10ms but remains slower than CPU.
No fallback/quarantine; touchFW79104/load0/A55A/restart streamON. Need
GPUOFF/powered0 verified before leaving measurement. Sole106124/session85627
boot0112-full4-live.log until~21:48UTC.

0180 exact fullscreen coalesced strips candidate: each15x4 thread copies
four16byte chunks separated by720bytes (180pixels),3x400groups; covers
720pixels exactly without partial tails. Unlike0110/0111 neighboring lanes
remain contiguous. Binary384bytes32regsTLSWLS0, SHAe7fa80c57d8b6affccca27f7e3e7f2ba7c11631d0fa76d778b3e799c2d3fe60e.
PrimaryMesa/actualASanUBSan/ARM64GPUAMFI/profile127 PASS; nohardwareclaim.

0181 observes selector12 one-scalar/no-output display-power requests before
existing shape validation; preserves return status/panel behavior. Matching
20A362 cache symbol _kern_RequestPowerChange at1ad7db4ec sends selector12 via
_IOConnectCallScalarMethod (stub1af7f9018 ->18e147574). Requests recorded as
raw values/timestamps/counter, no assumed enum or sleep-completion claim.
Actual method host test covers valid0/2, malformed/null, preserved errors;
replay regressionPASS. Need fullCI and real request/freeze correlation.

## 2026-11-20: four-pixel fullscreen CI success; BOOT0112 trial

CI44817012332 SUCCESS exactf712f5fd9cc4767f04589ca9e6da2fa7bf02b58b.
SixGPU/replay sources exacttestedmatch, RTC unchanged, reverse0179/checksums/
SMP/actualsource lifecycle+replay ASanUBSan PASS.
KernelSHA2564f28bf12b5dad9e2cac052dac24bc9a87dd10d5b5f18eca852f868dafa865da0.
BOOT0112SHA256f9ab4fab0e643bd5c1c0bca455aaf0dcf1dc3b328ef9040298745df3f1d40d13.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. SyncedDownload then
BOOT-onlyHeimdall uploadsuccess/reboot21:17UTC. Sole session85627 capture
boot0112-full4-live.log waitsCDC; needclocks/cachedwarm/GPUONverify1/
FWload/touchON->4fullreadbacks->pairedCPUfast->physicalUI. No0179HWclaimyet.

## 2026-11-20: four-pixel fullscreen full CI active

21:04UTC CI44817012332 in_progress exactf712f5fd9cc4767f04589ca9e6da2fa7bf02b58b.
Do not duplicate/restart. Privategpu-full4-work/artifacts.py+pack0112.py
prepared; same sixsources/RTC/checksum/reverse0179/SMP gates. BOOT0111
GPUOFFpowered0/verify1cachedwarm1,42frames18verified0fallback/quarantine.
Swaps70/copies66 stop again during idle while vsync24568 continues;
CPU24/GPU42. No Home injected this time; Auto-Lock Never user reply pending.
Capture100435/session31617 until~21:27UTC. Need exactCI->0112 and measured
benefit/physicalUI acceptance. Goal active, speedup not demonstrated.

## 2026-11-20: BOOT0111 correctness PASS; four-pixel fullscreen follow-up0179

BOOT0111 full720x1600 GPU copies: zero mismatches/done1/retired1. Eight
initial verified copies plus paired test completed without fallback/quarantine.
Three eight-copy rounds CPU1.462235/1.450115/1.623726ms; GPU4.100197/
3.982745/4.152413ms. MediansCPU1.462235/GPU4.100197ms: no speedup.
Current GPUOFF/powered0/verify1/cachedwarm1,42frames/18verified/completed42,
fallback0/quarantine0. Touch firmware79104/load0/A55A, restart streamON.

0179 keeps exact guard but changes fullscreen to four contiguous pixels per
thread (15x4 threads,12x400groups). This removes the sixteen-pixel per-thread
stride and extra64bit carry dependency instructions. Binary128bytes/32regs/
TLSWLS0, SHAc4f0ba76ccd62ed3f455b2dc9d02e85276a54251af66a1a6b39b97c5567d545b.
Generic masked four-pixel fallback unchanged. NativeMesa reproduction,
primaryv9 packing/exactguards/actual lifecycleASanUBSan/ARM64GPUAMFI/profile125
PASS. Needs fullCI and hardware comparison; no performance claim yet.
Solecapture100435/session31617boot0111-special-live.log until~21:27UTC.

## 2026-11-20: fullscreen CI success; BOOT0111 trial

CI44813460343 SUCCESS exact8c0fe7cd24e3042d40cd760a139aa31cf93ef55e.
SixGPU/replay sources exact tested match; RTC sources unchanged. Reverse0178,
checksums/SMP/actualsource lifecycle+replay ASanUBSan PASS.
KernelSHA25643b71b0051688134e59a4e659c018095b212b5a3796a4f682f65b4f2d7a2eefe.
BOOT0111SHA2560a51a5cca00d5461f17b11da445fd8a4646f47fee10ae74b612ca22664e0bfe4.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. Synced Download, Heimdall
lowercaseboot uploadsuccess/reboot20:57UTC. Nootherpartitionflashed.
Sole capture session31617 boot0111-special-live.log waitsCDC. Needclocks/
cachedwarm/GPUONverify1/FWload/touchON->4fullreadbacks->pairedCPUfast.

Important idle follow-up: CPU submissions continued46854+ after Home while
GPUOFF, but PosterBoard repeatedly crashes and respawns. Frame progression
alone is not healthy physicalUI proof. Sleep may explain initial stopped
submissions; do not claim all apparent freezes are sleep or rootcause fixed.

## 2026-11-20: fullscreen CI building; capture renewed

20:55UTC CI44813460343 exact8c0fe7c still Build/in_progress. Live log
20:53:58 confirms compilation in bsd/skywalk; no duplicate/restart. Native
Mesa/primaryv9 and actualsource ASanUBSan rerun PASS. No0178 hardware claim.
CPU compositor continues after one20:38Home: swaps46899/copies46895/CPU46854,
GPU41unchangedOFF/powered0/quarantine0. TouchON5110slices/events0. This is
frame-submission evidence, not a fresh physical screen acknowledgement.
Old reader95247 deliberately stopped before expiry. Sole new reader99894/
session67407 -> boot0110-specialwait-live.log until~21:24UTC. Need CI exact
success->gpu-special-work/artifacts.py+pack0111.py->source/checksum/SMP/
actualsourceASanUBSan->BOOT-only0111->fourfullreadbacks->pairedCPUfast.
User Auto-Lock Never observation pending; sleep remains hypothesis.

## 2026-11-20: fullscreen candidate committed; full CI active

Commit8c0fe7cd24e3042d40cd760a139aa31cf93ef55e pushed. CI44813460343
started20:40UTC, in_progress. Do not duplicate/restart. Private exact-run
verifier/pack0111 prepared under gpu-special-work; require full success,
six-source/RTC comparison, reverse0178, checksums/SMP/actualsource ASanUBSan
before BOOT-only trial. Candidate host tests PASS; hardware still untested.

## 2026-11-20: BOOT0110 correctness passes, performance rejected; fullscreen candidate0178

BOOT0110 completed full720x1600 readbacks with zero mismatches and retirement
confirmed. Three paired eight-copy rounds: GPU4.070764/4.002437/4.075817ms;
CPU1.675600/1.919673/1.420379ms. Median GPU4.070764 vs CPU1.675600ms.
Generic sixteen-pixel shader is slower than0175 four-pixel shader; reject it
as a performance improvement. Left GPU OFF, powered0, verify1, cached/warm1;
frames41/verified17/completed41, fallbacks0/quarantine0.

20:35–20:39UTC live follow-up: GPU remains OFF/powered0, touch streaming1,
1249slices/events0, storage ready1/poisoned0. Vsync advances while swaps77/
copies73 stay stopped. Kernel UTC1795207079 agrees with host. ONE explicit
Home (no timeset) resumes swaps734/copies730, CPU copies32->689; GPU stays41.
Sleep remains plausible, not proven: no display-power observation yet.
Requested a controlled user Auto-Lock Never trial; do not periodically Home.

Candidate0178 restores generic four-pixel masked-tail shader and adds a
separate384byte exact720x1600 shader: source offset0/stride3072, destination
offset0/stride2880;15x4 threads,16pixels/thread,3x400 groups, aligned128bit
loads/stores,32regs/TLSWLS0. All other geometry retains bounded generic4.
Both binaries reproduce with pinned Mesa24.3; shader hashes, dispatch/guard
variants and independent primaryv9 packers pass. Actual GPU/AMFI ARM64
cross-compiles and profile124 pass. Actualsource lifecycle/replay ASan/UBSan and benchmark regression tests
PASS; no hardware or speed claim for0178. Goal remains active.

## 2026-11-20: sixteen-pixel CI success; BOOT0110 trial

CI44804438707 SUCCESS exact01e7de1474faf02b8e3c9ee6f9b02c9069929752.
AllsixGPU/replay sourcesexacttestedmatch;RTCunchanged.0177reversecheck/
checksum/SMP/actualsourceASanUBSan(tails1..270)PASS.
KernelSHA256ec18bec3e54e936fa1929003ab200dca63ebe214c571775e83b160b5b4d73eff.
BOOT0110SHA256e16aec53e420384ea58d7d0be9b049aade40f918f1fe7253cefdbd8b723bb793.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. SyncedDownload then
Heimdalllowercaseboot uploadsuccess/reboot. Nootherpartitionflashed.
SolecapturePID95247/session20771boot0110-wide-live.log waitsCDC. Need
clocks/cachedwarm/GPUONverify1/FWload/touchON->4fullreadbacks->paired
CPUfast3rounds. No sixteenpixelhardwareclaimyet.

## 2026-11-20: paired replay baseline; wider CI still active

New tools/a03-gpu-paired-benchmark.py alternatesCPU/fast acrossrounds,
requiresexactreplaycount, nofallback/quarantine/mixedmode/warmup, restored
modeandstablecache/powerpolicy. HostrejectiontestsPASS;commit26a89f1.
Actual0109three8-copyrounds: CPU1.871149/1.608086/1.612682ms;
GPU2.327408/2.323322/2.899240ms. MedianCPU1.612682/GPU2.327408ms;
GPUdoesnotyetbeatCPU. GPU39frames/verified7/completed39/fallback0/
quarantine0, GPUOFFpowered0verify1restored. TouchON7020slices1096events.
20:13UTC CI44804438707 stillBuild/in_progress;watch43210/job136524622008
confirmedactive, logsBlobNotFound. Do notduplicate. Same0110nextgate.

## 2026-11-20: wider-copy build remains live; capture handoff

20:04UTC CI44804438707/exact01e7de1474faf02b8e3c9ee6f9b02c9069929752
still Build/in_progress (job136524622008), watcher43210. Live log endpoint
returnsBlobNotFound whilejobAPIcontinuesactive; thisisnotterminalfailure.
Do notduplicate/restart. Benchreplaycheckebc9559nowrequiresrequestedcount
exactlycopied/noquarantine before reporting; hosttestsPASS.
Oldcapture81787stoppeddeliberatelybeforeexpiry; soleNEWcapture91908/
session21336boot0109-widewait-live.loguntil~20:34UTC. GPUOFFpowered0/
verify1/cachedwarm1/touchON last3119slices15events. Continueexactbuild
->artifacts.py/pack0110.py->BOOT-only0110->fourfullreadbacks->fastCPU
alternatingcomparison. Goalactive; currenthardware2.296msnotyetbeatsCPU.

## 2026-11-20: idle display-sleep hypothesis after another Home wake

User reports clock frozen again on0109, then suggests iOS is sleeping.
At19:56:19UTC kernelUTC1795204579 matches host; GPUOFF/warm1/powered0,
frames15/quarantine0. Vsync67570 advances while swaps62/copies57 stopped.
TouchON3611slices27events. ONEHome dispatch resumes swaps1290/copies1285,
including1270CPUcopies; kernelUTC1795204624 continues. No timeset/reset.
This reproduces stopped compositor updates while GPU is off, with Home
wake recovery. Idle display sleep is now a plausible explanation, not a
proven GPU hang or an RTC failure. Current framebuffer keeps scanning the
last panel buffer and implements neither blanking nor display power-state
handling; an iOS display-off request can therefore look like a frozen
clock. Need direct sleep-state evidence or a controlled Auto-Lock trial
before claiming root cause. Do not inject periodic Home or fabricate frames.

## 2026-11-20: warm hardware PASS2.30ms; sixteen-pixel candidate0177

WideCI44804438707 exact01e7de1474faf02b8e3c9ee6f9b02c9069929752 active;
watch43210. Privategpu-wide-work/artifacts.py+pack0110.py pinfullSHA/run/
sixsources/RTC/reversepatch/checksum. NeedfullCI->0110BOOT-only->cachedwarm
4fullreadbacks->fastCPUtiming. Current0109GPUOFFpowered0/verify1/cached1/
warm1/touchON676slices15physicalevents. Solecapture81787/session58307
until~20:06UTC; revalidateownerbeforeuse. No widehardwareclaimyet.

BOOT0109RTC1795203422/status1795203436;clocksID90910010/cachedwarmON.
FW79104/load0/A55A/touchrestartON. Actualswaps+replay4 full1152000pixels
mismatches0/done1/retired1/verify1/PASS1. Warm1/powered1/verified6.
Fast8mean2.296048ms vsCPU1.735884ms;lastpower0.040730/prepare0.265346/
cache0.388769/execute1.572807/retire0.039653/shutdown0.001076ms.
ExplicitGPUOFFconfirmspowered0/noquarantine;CPUmodeleft. Warmownership
works butstillnospeedupoverCPU. GPU15frames/verified7/fallback0/quarantine0.

0177sixteenpixels/threadfour128bitloads/stores plusboundedscalartails;
full720x1600dispatch3x400groups.1920bytes32regsTLSWLS0/preloadR60R61,
SHA498d013b19f1df298970a639929e3d1180974eb05fc5c5b602a763b6d331ad15.
NativeMesa reproduction/primaryv9packers/ASanUBSan lifecycleandtailguards/
ARM64GPUAMFI/profile123PASS. NeedfullCI->0110->cachedwarm4fullreadbacks
->fastCPUcomparison/physicalUIacceptance. Current0109GPUOFFverify1/warm1
powered0/cached1/touchON. Solecapture81787/session58307.

## 2026-11-20: retained-power CI success; BOOT0109 trial

CI44801549767 SUCCESS exact6948d5ead5fe0dce4d2594ea56e4af96a5b7911e.
AllsixGPU/replay sourcesexacttestedmatch;RTCunchanged.0176reversecheck/
checksum/SMP/actualsourceASanUBSanPASS.
KernelSHA2568914aba61a1e82340141e4f6ded9f20631f23b1aa98deb561c4efea9fdeac43f.
BOOT0109SHA256387e4bd016df228d9d6bc58b9302932aba0bfa6efc6f8c995f55d5b3f55e64a1.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. SyncedDownload then
Heimdalllowercaseboot uploadsuccess/reboot. Nootherpartitionflashed.
SolecapturePID81787/session58307boot0109-warm-live.log waitsCDC. Need
clocks/cached/warm/GPUONverify1/FWload/touchON->4fullreadbacks->fastCPU
timingandexplicitOFFpowershutdown. No warmhardwareclaimyet.

Privatewidecandidate16pixels/thread1920bytes32regs/TLSWLS0 prepared
offprofile ingpu-wide-work; nativeMesa/primaryv9/actuallifecyclePASS.
Useonlyifwarmtimingstillneedsimprovement; no newCIforwideyet.

## 2026-11-20: vector hardware PASS3.54ms; warmownershipcandidate0176

WarmCI44801549767 exact6948d5ead5fe0dce4d2594ea56e4af96a5b7911e active;
watch43109. Privategpu-warm-work/artifacts.py+pack0109.py pinfullSHA/run/
sixsources/RTC/reversepatch/checksum. NeedfullCI->0109->explicitcachedwarm
GPUONverify1->4fullreadbacks->fastCPUcomparison. Current0108GPUOFFverify1/
cached1/touchrestartON. Capture76088/session37152until~19:45UTC;revalidate.

BOOT0108actualswaps+replay4 eachfull1152000pixels/mismatches0/done1/
retired1/verify1/PASS1. Fast8-copymean3.541731ms (execute1.680307ms),
CPU1.405543ms. Vector improvescachedscalar6.170ms butCPUstillfaster.
Power0.748230+shutdown0.579192ms dominate remainingfixedoverhead; mapping
0.155346/cache0.288230/retire0.032653ms. No speedupoverCPUclaim.
Current27GPUframes/31104000pixels/verified19/completed27/fallback0/
quarantine0. GPUOFFverify1/cached1whileoptimizing. Physical42touch events
precededstreamstop(valid14packet); explicitrestartconfirmsON.

0176 explicitgpu blit warm/cold defaultcold keepscoresononlyafterowned
cachedjob+cacheclean+ASretirement+successfulreadback/completion. Eachnext
jobrechecksownership/rail/topology/faults; staleownershipquarantines.
OFF/cold/uncached explicitlyshutdownownedcores/restoresoverride; uncertain
DMA skips shutdown. No voltage/ratechange. HostASanUBSan warmreuse/
off/cold/uncachedshutdown/quarantinerejection+ARM64GPUAMFI/profile122PASS.
NeedfullCI->0109->warmcached4fullreadbacks->fastCPUtiming/physicalUI.
Solecapture76088/session37152boot0108-vector-live.log. Goalactive.

## 2026-11-20: vector CI success; BOOT0108 trial

CI44794488664 SUCCESS exact734646c9f2f438ccf0417b747600060288829c7f.
AllsixuploadedGPU/replay sourcesmatchtestedcandidate;RTCunchanged.0175
reversecheck/checksum/SMP/actualsourceASanUBSan(fullframe/tail1..70)PASS.
KernelSHA2562f995b2b448cfb01455c1278622b030ed91b4fdb4b34c239c1d050ea2d25307e.
BOOT0108SHA2562f656a8de10618f2343b7e6622754a02a359dd96e6ba6fdbfa7433e447ec6983.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. SyncedDownload then
Heimdalllowercaseboot uploadsuccess/reboot. Nootherpartitionflashed.
SolecapturePID76088/session37152boot0108-vector-live.log waitsCDC. Need
clocks/cachedGPUONverify1/FWload/touchON->4fullreadbacks->fastCPUtiming.
No vectorhardwareclaimyet.0107CPUwakecheckpointretained.

## 2026-11-20: BOOT0107 physical UI resumes after one Home

19:01UTCvectorCI44794488664 remainsBuild/in_progress; livejoblog6.3MiB
confirmscompilationthrough18:58:59. Literalerrorlinesareknownoptional
alreadyapplieddonorpatchskips, notcompilerfailures. Do notduplicate.
Oldcapture57854endeddeliberatelybeforeexpiry; soleNEWcapture71717/
session74884boot0107-vectorwait-live.log ownsconsoleuntil~19:31UTC.
GPUOFFverify1/cached1/touchON, last5152slices1670events;CPUframecopies
continue. Expandedtailtestae8377b andcachedresultsdocc83bccc pushed.

User reports frozen/blank duringcachedlivewindow. At18:53UTCGPUwasalready
OFF(afterbenchmarkrestoration), frames18/quarantine0; display61swaps/
56copiesunchanged, touch4034slices1658events, iohealthyandcorrectUTC.
ONEexplicitinputhome then display585swaps/580copies, CPU562/GPUstill18.
Userconfirms"ok now it works". No reboot/flash/timeset. This proves
HomewakeinCPUmode;doesnotproveGPUcausedfreezeorfixedidlewake. Preserve
GPUOFFverify1/touchON. VectorCI44794488664 stillBuild18:54UTC;waitsamejob.

## 2026-11-20: cached hardware PASS and22x gain; vector candidate0175

VectorCI44794488664 exact734646c9f2f438ccf0417b747600060288829c7f active;
watch40061. Privategpu-vector-work/artifacts.py+pack0108.py pinfullSHA/run/
sixsources/RTC/reversepatch/checksum. 30secondcachedfastlivewindowproduced
zeroactualcopies/noevents=>INCONCLUSIVE, restoredGPUOFFverify1. Current
0107frames18/verified10/fallback0/quarantine0, touchON1099slices/events0.
NeedfullCI->0108->cached4fullreadbacks->fastCPUreplaycomparison.

BOOT0107 retainedRTC1795199519/status1795199529, clocksID90910010.
Explicitcached1+GPUONverify1. FW79104/load0/A55A andtouchrestartON.
Actualswaps1/2+replay4 eachfull1152000pixels/mismatches0/done1/retired1/
verify1/PASS1. Cachedpolicyfreshcleancompletionrequired byeveryPASS.
Fast8copies6.170024msmean; lastpower0.697807/prepare0.242384/cache0.392807/
execute4.276961/retire0.032230/verify0.002961/shutdown0.591884ms. About22x
faster thanuncached142.160ms, BUTCPU1.672600ms stillfaster. GoalNOTcomplete.
Current18GPUframes/20736000pixels/verified10/completed18/fallback0/
quarantine0; GPUOFFverify1/cached1leftwhileoptimizing; touchON713slices.

0175nativeG57vectorcopymovesfourpixels/thread via128bitload/store, exact
width/heightguardsandscalar1..3tail. Workgroups12x400 forfullframe.
640bytes/32regs/TLSWLS0/preloadR60R61;SHA9412d199dcb1f8f71a8144e3e4b45036ad6ce045d2c8c07adc3d2d73e890625c.
PinnedMesareproduction/primaryv9packers(assertionsON),actualsourceASanUBSan
paddedgroups/offset53x17/noncontiguous/fault/cacheclean/quarantinePASS.
ActualGPU+AMFIARM64compile/profile121PASS. NeedfullCI->0108BOOT-only->
cachedfourfullreadbacks->fastCPUcompareandphysicalUIacceptance. No vector
hardwareclaimyet. Solecapture57854/session79767boot0107-cache-live.log.

## 2026-11-20: cached CI success; BOOT0107 trial

CI44791438428 SUCCESS exact7e56be7f05428c9672d45d93fa357f32a79d20e2.
SixGPU/replay sources matchtestedcandidate; RTCsourcesunchanged.0174
reversecheck/checksum/SMP/actualsourcecachedDMAASanUBSanPASS.
KernelSHA2563628a0c95fe89a79522528eb6fff261b8c9d0ea5a9a49521bc7eb743174d0dc6.
BOOT0107SHA25644ad2a360a37b405ac3730be13b1e15bab2f77a07289dc50fbf1934a11c37155.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. SyncedDownload then
Heimdalllowercaseboot uploadsuccess/reboot. Nootherpartitionflashed.
SolecapturePID57854/session79767boot0107-cache-live.log waitsCDC. Need
RTC/status/clocks/FWload/touchON, explicitcached+GPUONverify1, four
fullframereadbacks, thenfast/CPUcomparisons. No cachedhardwareclaimyet.
0106CPUmode/userconfirmedclockwake checkpointretained.

## 2026-11-20: frozen clock confirmed; CPU-copy wake restores screen

CPU-onlyfollowup18:26UTC: copies707->3096->6016->7141, thenidleandnew
physicalcontactactivityresumescopies7564 withoutanotherHome. CPUcopies7544,
GPUframesstill20; touchON2585slices277events. Vsyncandkerneltimecontinue,
notificationsattemptsremain0 evenwhileframesadvance. Thusmissingvsync
notificationisnotaloneprovenfreeze cause. Userclockupdateconfirmed;
sustainedGPUUIacceptanceremainsunproven. CachedCI44791438428 stillBuild
at18:27UTC; do notduplicate. Benchmarka708396 nowlabelscachepolicyand
rejectspolicychangeswithinameasurementinterval;hosttestPASS.

User reports frozen/blank/corrupt UI, clock about3minutesbehind. At18:20:10UTC
kernelreadonlytime1795198810 matcheshost exactly; displayedclockisstale.
Vsync28277done, swaps24/copies20 unchanged, GPUframes20/verified12/
quarantine0; touchstream1332slices21events andstoragehealthy. SB26/main
andBB56/main waitmachmsg; no pendingGPUjob. GPUfaultnotestablished.
ExplicitGPUOFF thenONEinputhome down/up (dispatchresult0). Subsequently
swaps711/copies707, including687CPUcopies whileGPUframesremain20. User
confirmsclockupdated. No hosttimeset/reboot/flash. This combinedintervention
doesnotisolateGPUmodefromHomewake or establishpermanentfreezefix. Leave
CPUcopiesenabled(GPUOFF), verify1/touchON forusableUI whilecachedCIbuilds.
Physicalinput/UIacceptanceisnotcompleteforGPUmode.

## 2026-11-20: BOOT0106 isolates job execution; cached candidate0174

Exactcachedcandidate7e56be7f05428c9672d45d93fa357f32a79d20e2 builds
CI44791438428; livewatch32994. Privategpu-cache-work/artifacts.py and
pack0107.py pinsixsources/RTC/fullSHA/run/reversepatch/checksum. NeedfullCI
thenBOOT-only0107, explicitcached andfourfullreadbacks beforefast. Current
0106frames20/verified12/completed20/fallback0/quarantine0/GPUONverify1.
TouchON987slices includes12physicalcontactevents, down294,1598 through
342,1340 thenreportrelease; no injectedgesture. PhysicalUIanswerpending.

RTC1795198340 beforeUSB/readonlystatus1795198352. GPUclocksID90910010,
privateFW79104/load0/A55A/touchrestartON. Firstactualswaps+replay4 each
full1152000pixels/mismatches0/done1/retired1/verify1/PASS1, verified6.
Fast8-copymean142.159783ms. Lastphasepower0.684576/prepare0.296384/
cache0.395576/execute137.267230/retire0.010923/verify0.001153/
shutdown0.596000ms. Fullreadbacklast176.855576ms separately. Thusmapping/
sourcecache/power areNOTdominant; executioninterval(includingpollwaits) is.

0174explicit gpu blit cached/uncached defaultsuncached. Cachedmode uses
pinnedvendorAttrIndex0 fordescriptor/code/source/destination and vendor
writeback/readallocatePTwalks. SourceCPUflush remains. AfterJSretirement,
requirefreshGPUCLEAN_INV_CACHES(cmd8)/IRQbit17 beforeASdisable/readback/
coreoff; timeout/stalebit/reset/fault quarantinesretainedmemory+surface.
Policychangesresetfour-readbackqualification eveniffastrequested.
StatefulhostDMA hidescachedwritesuntilclean, checkspermissions/fullframe/
strided/failure/quarantine/repeatedreuse;ASanUBSanPASS. ActualGPU+AMFI
ARM64compilePASS;120profilePASS. NeedfullCI->0107->cached4fullreadbacks
thenfast/CPUcomparison. No cachedhardware/speedupclaimyet. Current0106
GPUONverify1/touchON remains;solecapture52314/session97698.

## 2026-11-20: phase CI success; BOOT0106 measurement trial

CI44788043452 SUCCESS exacta59bd6a49500d42472d3a62ade7bedb5b68cd7f0.
All six GPU/replay sources exactlymatch testedcandidate; RTC sources
unchanged.0173reversecheck/checksum/SMP/actualsourceASanUBSanPASS.
KernelSHA256881e7b39461d413328f53a23aa8eb18871a963d9c48660758f82329b06b0cdda.
BOOT0106SHA256a4133cfc42af540f7ced8acdfeb04589a054e443cf0d6b4d1297086df16af387.
Same8cores/1984MiB/ADT0094/cmd599/stockramdiskDT; syncedDownload then
Heimdalllowercaseboot upload100percent/success/reboot. Nootherpartition
flashed. SolecapturePID52314/session97698boot0106-phase-live.log waitsCDC.
NeedRTC/status/clocks/blitON/FWload/touchON->4verifiedframes->fastreplay
phasebreakdown. Benchmarknowretains last-attempt phases separately from
batchmeans (hosttest65539f9PASS). Sourcefinding: SweetCPU leavespowergate
latencyzero, soGPUdelay calls mayblock; causalhardwareevidencepending.

## 2026-11-20: BOOT0105 tiled hardware PASS, no speedup; phase candidate0173

PhaseCI44788043452 exacta59bd6a49500d42472d3a62ade7bedb5b68cd7f0 nowactive;
watchsession54706. Privategpu-phase-work/artifacts.py+pack0106.py pinexact
run/SHA and expectedtestedGPU/replay/RTC sources. Waitsamejob, do not
duplicate. Current0105remainsGPUONverify1/touchON; capture49304/session69950
expiresapproximately18:20UTC. No0173hardwareclaimuntilsuccessfulCIand0106.

CDC enumerated after normalstartupdelay. RTC1795197038 beforeUSB and
firstreadonlystatus1795197061; nohostsync. ExplicitclocksID90910010 and
blitON/verify1. PrivateFW79104staged/load0/A55A/config720x1600; initial
startupreportstoppedstream, restartconfirmsON. Actual compositor swaps1/2
plusreplay4 allfull1152000pixels/mismatches0/done1/retired1/PASS1.

Eight-copy fast138.576740ms then139.406908ms; CPU1.410130/1.400726ms;
verify225.107048ms. No meaningful improvement over0104; workgroup scheduling
was NOT established as the limitingfactor. Currentframes33/pixels38016000/
verified17/completed33/fallback0/quarantine0/GPUONverify1. TouchON661slices/
events0; ioReady1/poisoned0. Physicalscreenacceptancepending, noHomeinjected.

0173 adds last-attempt phase intervals for power/preparation/sourcecache/
ASandjob/retirement/readback/shutdown, underexistingowner. No newGPUwrites
or changedDMApolicy. ActualASanUBSan lifecycle/phaseinterval checks and
actualARM64GPU+AMFIcompile/profile119PASS. NeedfullCI->0106->phasehardware
measurement to identify bottleneck before cache/power policy changes.
Capture49304/session69950boot0105-tiled-live.log remains soleowner.

## 2026-11-20: tiled CI success; BOOT0105 hardware trial

CI44784844777 SUCCESS exact3c22c827b79fe88723cbb638439349c3b6af1071.
All six uploadedGPU/replay sources match testedcandidate; bothRTC sources
unchanged from0104.0172reversecheck/checksum/SMP/actualsourceASanUBSanPASS.
KernelSHA2568f294f4da6e227363b0e494802ffa8dd7e2ef7637ee534a3860aa3c475e20e0d.
BOOT0105SHA25640d087fa9dd8f19279e4d067a820c0c5ae6464f1d7c9e0e19c0bfd077b954eff.
Same8cores/1984MiB/ADT0094/cmd599/stockramdiskDT. SyncedDownload reset,
Heimdalldetected then lowercaseboot upload100percent/success/reboot.
No otherpartitionflashed. SolecapturePID49304/session69950 waitsCDC in
boot0105-tiled-live.log. NeedRTC/status/clocks/blitON, privateFWload/touchON,
fourfullframepixelreadbacks, repeatedfast/CPU/verifymeasurement. No tiled
hardware success or speedup claim yet;0104 restore retained.

## 2026-11-20: measured GPU slowdown; tiled dispatch candidate0172

Follow-up17:47UTC: CI44784844777 still Build/in_progress; watcher session55345
is live, not a failed or stopped run. Do not dispatch a duplicate. Retained
baseline8-copy rounds CPU2.171803/1.717081ms, fast138.139721/138.472221ms,
verify231.813774/289.190476ms in privategpu-tiled-work/baseline-results.json.
Current0104 frames52/pixels59904000/verified28/completed52/fallback0/
quarantine0; GPUON/verify1. Touchstream1530slices/events0, so no newphysical
gesture evidence. SolecapturePID46326/session91083 stilllive. Negative
primary-packer fixture rejects intentionally wrong group size. Candidate
3c22c82, expandedtest/handoff91f7fa9, GPUdoc10031ec pushed. Goalactive.

Exact candidate3c22c827b79fe88723cbb638439349c3b6af1071 is building in
CI44784844777 (macos26intel). Private gpu-tiled-work/artifacts.py and
pack0105.py pin run/fullSHA, verify all six GPU/replay sources plus unchanged
RTC sources, reverse patch and artifact checksums before BOOT packaging.
Expanded fakeDMA iterates actual16x4 groups including padded edge lanes;
lifecycle ASanUBSan and replay bounds repeat PASS. No new flash yet.

BOOT0104 fresh single-owner boot0104-gpu-resume.log confirms GPU initially
OFF, 35 CPU copies, healthy storage. Explicit clocks reads ID90910010,
then blitON and four accepted-frame replays each pass all1152000 pixels,
done1/retired1/mismatches0. Eight-copy replay measurements: fast GPU
139.005807ms/copy, CPU1.665466ms/copy, verified GPU211.629668ms/copy.
No fallback/quarantine. These are synchronous copy timings including
scheduling/cache/power overhead, not FPS or physical animation proof.
Current GPU path is substantially slower; acceleration goal remains active.

Candidate0172 replaces1152000 one-thread workgroups with18000 groups of
16x4 threads for720x1600. Native Mesa24.3 shader masks padded X/Y lanes
against exact width/height, including clipped rectangles.256bytes/32regs/
TLSWLS0/preloadR60R61; SHA03409e893339415bbdbe0bc83449712e009f783866bc5c0986c9137ccfb73e0b.
Primary v9 descriptor byte comparison with assertions explicitly enabled,
actual lifecycle ASanUBSan (strided/offset/noncontiguous/fault/quarantine),
actual BSD ARM64 flags and118-patch profile stage PASS. FullCI and hardware
correctness/performance remain required; no tiled hardware claim yet.
Private79104byte touchFW re-staged/load0/A55A; first stream stopped on
startup packet, restart confirms streaming1/slices1. No Home/reboot/flash.


## 2026-11-20: BOOT0104 initializes UTC from the hardware RTC

Full CI44765816216 passed at 44d482d49f951cd782f1c4f454ebeb645b0030a8.
Both RTC sources matched, reverse patch and checksum verified, with the
same eight CPU, 1984 MiB, stock ramdisk and DT configuration. Kernel
SHA256 28d9ad7870e05d4430dd007b90a2ad7ef2662c6f828219019a7eb5403e6171fc.
BOOT SHA256 d0a453c7a6fedf95352d0c734c2a0ff07a9c9a13520a6cc4c3875c60f0fd6dd4.
Heimdall rejected uppercase `BOOT` before transfer. After returning to
Download, lowercase `boot` uploaded successfully and rebooted.

In boot0104-rtc-verified.log, XNU read RTC UTC1795195136 (November 20,
2026 at 17:18:56 UTC) before USB supply setup. The first USB transaction
was read-only `time status` and returned UTC1795195137. No host time set
on this boot. Launchd started with the correct date and UTC-8 presentation.
Physical restart unplugged and local display confirmation are pending.
The old status message describes the USB setter and predates the RTC reader.

## 2026-11-20: boot-time clock reset measured; retained RTC candidate0171

User requires correct time at boot without USB. Fresh single-owner capture
clock-20261120.log tx1 measured UTC553 (January1970), not merely a timezone
offset. Explicit tx2 corrected calendar to1795188867=2026-11-20 15:34:27UTC;
this was volatile only and does NOT satisfy autonomous boot-time setting.
No USB auto-sync feature added. No reboot/flash/partition write yet.

0171 wires PEGetUTCTimeOfDay to the SC2730 retained RTC at ADI64200000,
slavewindow20000/RTC200 from live DT and stock rtc-sc27xx/spi-sprd-adi.
Independent of console bootarg, USB connection, userspace and host clock.
Only ADI bus clock/read-command transactions; no PMIC time/alarm/reset or
storage writes. Shared ADI ownership; bounded double-snapshot consistency,
power-reset marker rejection, field/date bounds; no fabricated fallback date.
Actual source ASan/UBSan tests PASS (rollover, reset, maps/read failures,
ownership,2020..2099); USB C exactCIflagsARM64 compilePASS. Platform C++
local compile blocked by known Apple typed-allocation builtins; fullCI
required. Hardware retained date/bootwithoutUSB still UNVERIFIED.

Replay CI44632519909 succeeded exact7e4ea5b; no0103 deployed here. Current
boot has reset since prior notes; do not assume old capture/touch/GPUstate.
Clock capture started with host access session8921 for600seconds.

0171 implementation commit44d482d49f951cd782f1c4f454ebeb645b0030a8 pushed;
fullCI44765816216 macos26intel active. Superseded44765753773 used oldHEAD
7eaa974 and was cancelled by workflow concurrency; never use its artifacts.
Actual extracted platform hook also passes standalone C/C++ linkage and
success/failure tests. Private0104packer pins44765816216/fullSHA.

## 2026-11-19: ten actual2D GPUframes; replayCI44632519909 active

BOOT0102frames10/pixels11520000/verified10/completed10/fallback0/quarantine0.
Physicalcontact27events precedednewUIframecopies; allfirst8loggedfullreadback
mismatches0/verify1/PASS1, subsequentcounterincrementrequires samechecks.
GPUtotalverifiedns1971117342,last314676730ns. This is realframecopyevidence,
notphysicalscreenacceptance or measuredfastmode speedup. Another30second
fastwindow hadzeroactualframes=>inconclusive;GPUON/verify1restored.

Exact0170 replayCI44632519909 at7e4ea5b is compiling.
Private0103fetch/sourceverifier/packer pinsfullSHA. Replaybenchmark--replay4
selfcheck andmode restorationPASS. NeedfullCI->0103BOOT-only->retainedframe
CPU/verify/fast repeatedmeasurement,then restorefullverify andtouchON.
Currentcapture123073/session98448 live untilapproximately23:15UTC.

## 2026-11-19: BOOT0102 2D hardware PASS; repeatable replay candidate0170

Actual720x1600 swaps1..4 each1152000pixels/mismatches0/done1/retired1/
verify1/PASS1. verified4/completed4/frames4/pixels4608000/fallback0/quarantine0.
Totalverifiedcopy836191307ns; last173059846ns. Firsttwo169.342346ms and
325.702ms include fullreadback/cache/map/power/scheduling, NOTFPSclaim.
Two20second fast/CPUbenchmark windows hadzeroactualcopies despitebounded
swipes; correctlyreported inconclusive andrestoredGPUON/verify1. No fast
hardwarecopyor speedupclaim. TouchON/restoredUTC/iohealthy.

0170 adds explicit display replay1|4|8 oflastacceptedcompositorrecord.
Replays holdexistingswaplock, takefreshsurface references viaactualswap,
nevercreatepixels/surfaces; boundedcount1..8/quarantinebreak. Benchmark
--replay enables same-frame CPU/verify/fast comparison without user timing.
ActualreplaycontrolC++ ASanUBSan bounds/lock/record/quarantinePASS; existing
GPUregressionPASS;GPU/AMFI ARM64compilePASS. NeedfullCIthen0103BOOT-only.
Replayisdiagnosticframe resubmission, notphysicalUIanimation/acceptance.

## 2026-11-19: BOOT0102 running, touch restored, timing parser live

ActualclocksID90910010/gates11,11,31; blitON1/verify1. UTC1795128362synced.
Private79104byteFWstagedvalid0/load0/readyA55A; touchcontinuousON1/slices1
restored. Actual new timing parser readsall0169fields correctly; frames0/
verified0/completed0 atthispoint, so nooptimizedshaderhardwareclaimyet.
GUIstartupstorageadvances5153->6952requests/read731039->1119528sectors,
ioReady1/poisoned0. Solecapture123073/session98448 boot0102-gpu-blit2-live.log.
Awaitfirstfouractual2Dfullreadbackframes beforefastmeasurement. NoHome.
0101physicalinput18events/4GPUframes+28CPUfallback checkpoint retained.

## 2026-11-19:0169 CI success; BOOT0102 2D/timing trial flashed

CI44629497398 SUCCESS exact44b6f27cd4c58ca43c3438a324e5fdeaeb4386c9.
All6 uploaded sources byte-match testedcandidate;0169reversecheck/checksum/
linked2Dverification+CPU-GPUtiming/SMP/actualsourceASanUBSanPASS.
KernelSHA2561609f9aa1564c2690c60d8ec58b1e56607f747ada30b9ca45c87f7555ecb0520.
BOOT0102SHA256be5b980f4e190a23eee80601be1c508ec207f32d8ebd116f0af219fcd44ce223.
Same0094ADT/cmd599/all8/1984MiB/23reservations/SMP103485000/stockramdiskDT.
SyncedDownload ->Heimdalldetect ->BOOT-onlyuploadsuccess/reboot. No other
partitionflashed. Solecapture123073/session98448 boot0102-gpu-blit2-live.log
waitsCDC. Oncequeuedclocks/blitON(defaultverify1)/UTC. NeedprivateFWload/
touchON,actual2Dfullreadbackfourframes,fastmode+CPUtiming andphysicalacceptance.
No actual2D/speedupclaimyet. Keep0101fullframe+fallback checkpoint.

## 2026-11-19: physical swipe delivered; optimizedCI44629497398 active

BOOT0101 touchstream has18 physical contact events: down362,1598 through
421,666 thenreportdrivenrelease; HID1 andSweetHID down/up confirmdelivery.
No synthetic command during that event interval. GPUframes remain4 and
swaps37, so this is physicalinputdelivery, NOT visibleUIresponse evidence.
SpringBoard26 now17threads/mainmach_msgwait;backboardd56 has13threads/main
mach_msgwait. No pendingGPUjob/quarantine. Physicalscreenanswerpending.

0169 exact44b6f27 fullCI44629497398 is Build/in_progress.115patchprofile
stages; private0102artifact/source/packer pinned. Added actualcopybenchmark
helper with exacttransaction/counter-reset/no-frame-inconclusive handling
and finally restoration oforiginalGPUenabled/verificationmode. Selfchecks
pass. NeedsuccessfulCI->0102->4verified2Dframes->fastmode timing/physical
acceptance. Current0101 remainsGPUenabled/touchON/storagehealthy.

## 2026-11-19:0169 2D dispatch, verification policy and timing candidate

BOOT0101 real4frames/4608000pixels remains checkpoint. Prepared0169 uses
native globalX/globalY with width-by-height dispatch instead of expensive
perpixel integer divide/modulo. PinnedMesa shader shrinks768->256bytes,
32regs/TLSWLS0/preloadR60+R61, SHAeb88a77a8595eaf054c5d9d73d69cbbbd3fe689bb358ef2ae7a121c3641d0548.
Fullverification defaultsON; explicit gpu blit fast skips CPUrectangle
readback only after4 verified successfulframes. gpu blit verify restores
fullreadback. Allcompletion/MMU/retirement/lifetimeguards remain mandatory.
Counters distinguish verified/completedframes and total/lastGPU ns;
framebuffer separately tracksCPU/GPUcopyns/counts for comparison. No measured
speedup claim until hardware. Nativehash/primaryv9packers/actualtranslated
DMA fullrect+offset+noncontiguous/fault/timeout/fastpolicy ASanUBSanPASS;
GPU/AMFI ARM64actualflagscompilePASS. NeedfullCIthenBOOT-only0102trial.
Physicalscreenacceptance question stillpending. Current0101blitON/touchON.

## 2026-11-19: four real GPU frames and hardware CPU fallback verified

BOOT0101 actual GPU frames advanced2->4 (4608000 pixels total), each logged
full1152000-pixel readback/mismatches0/done1/retired1/PASS1. NoGPUfault,
fallback or quarantine. Source alternates IOSurface2/3 as GUI progresses.
One bounded synthetic swipe dispatched; input dispatch is not physical proof.

Hardware fallback check: tx2525 gpu blit off atframes4/displaycopies4;
one bounded swipe then tx2528 displaycopies32/swaps37 proves28 CPU copies
while GPUframecounter remained4. tx2529 re-enablesGPU1; touchcontinuousON
1099slices, ioReady1/poisoned0. A subsequent bounded swipe produced no new
swaps in15seconds; not itself a GPU failure. tx2538 stillenabled1/frames4/
pixels4608000/fallbacks0/quarantined0 at22:28UTC. NoHome injected. Physical
screen/touch acceptance remains unanswered. Goalactive; GPUcopybackend and
CPUfallback proven, visible reliability/latency remain unproven.

## 2026-11-19: BOOT0101 actual IOSurface-to-framebuffer GPU blits PASS

After GUI page-in completed, backboardd created720x1600 BGRA IOSurface2
with3072byte stride. Actual swap1 andswap2 each submitted nativeG57 strided
compute directly from retained IOSurface pages to2880stride panel memory:
pixels1152000/mismatches0/done1/retired1/PASS1. tx2501/2504 reports enabled1,
frames2/pixels2304000/fallbacks0/quarantined0. This is actual fullframe GPU
copy+CPUreadback, beyond the isolated1024word test. CPU still renders source
content; Metal/EAGL remains absent. Fullreadback remains enabled, so no
latency/smoothness improvement claimed. Physicalscreenacceptance pending.

tx2502 display swapsentered4/done4/copies2; some swaps had no enabledcopy.
tx2505 ioReady1/poisoned0; tx2506 continuous touchON/slices561/events0.
NoHome injected. Current0101 checkpoint retained, capture111070/session56476
ownsboot0101-gpu-blit-live.log untilapproximately22:50UTC. Needmoreactual
UIframes/physicalgestureevidence, CPUfallbackhardwarecheck, andmeasure
before claiming completedvideoacceleration. Userphysicalstatusasyncpending.

## 2026-11-19: BOOT0101 clocks/blit enabled; GUI still paging in

Actual tx1 gpu clocks enables11/11/31 andID90910010; tx2 gpu blit on
reports enabled1/frames0/fallbacks0/quarantined0. UTC1795126843 synced.
PrivateFW79104stagedvalid0/load0/readyA55A, touchcontinuousON tx2480;
tx2495 streaming1/slices222. AllinputrestoredwithoutHome. ioReady1/poisoned0,
requests advancing4881->8975/readsectors723647->1497513 duringstartup.
SpringBoard26/backboardd56 exist; both initialsinglethread samples wait in
lck_mtx_lock_contended -> emmc_strategy -> clustered page-in, exactlinked
kernel symbolresolution. Vsyncadvances; swaps0/copies0. No GPU framebuffer
job has arrived yet, so no hardwareblit/PASS/latency claim. Awaitactualframe
submissions; physicalscreenstatus requested asynchronously. Solecapture
111070/56476 boot0101-gpu-blit-live.log remainsowner. Goalactive.

## 2026-11-19:0168 fullCI success; BOOT0101 flashed for framebuffer trial

CI44625038530 SUCCESS exact74e1deff53d2dc27bcc769b92b2b37ec70c16cb9.
All6 uploadedGPU/layout/AMFI/framebuffer source files byte-match tested
candidate;0168reversecheck/checksum/linkedmarkers/SMP/actualsourceASanUBSan
PASS. KernelSHA256460bfe0564e4abebded43e9a188434f5403c29aa5cfbbc7268e9ff05e3d1620e.
BOOT0101SHA2563825c66cb24538b35a5fbab1c50644447a3504a6a569bd116a4b167a6c7c8d62.
Same0094ADT/cmd599/all8/1984MiB/23reservations/SMP103485000/stockramdiskDT.
SyncedDownload ->Heimdalldetect ->BOOT-onlyuploadsuccess/reboot. No other
partition flashed. Solecapture111070/session56476 boot0101-gpu-blit-live.log.
AwaitCDC; queuedonce gpu clocks then gpu blit on andUTCsync. NoactualGPU
framebuffer/pixelclaim until completion/readback counters. NeedprivateFW/
load/startleaveON afterreboot.0100/0099/0098restoreskept.

## 2026-11-19:0168 CI44625038530 active; translated DMA tests pass

Authoritative kernel CI44625038530 exact74e1deff53d2dc27bcc769b92b2b37ec70c16cb9
is Build/in_progress. Later commits only improve tests/handoff. No duplicate
workflow.114patch profile stages offline;0168 applies to exact0100 tree.
Private0101 fetch/sourceverifier/packer pin this run and SHA.

Expanded fakeDMA validates actual four-level page walks and RO/RW/NX bits
for every pixel of full720x1600 and clipped53x17 rectangle with124/2884byte
source/destination offsets; neighboring destination canaries unchanged.
PrimaryMesa24.3 v9 full-frame header/payload/program/TLS bytes match.
Actual C GPU+AMFI ARM64 compiles PASS; existing WRITE_VALUE/copy lifecycle
regression passes against new owner-enabled source. C++ fullCI remains gate.
BOOT0100 unchanged; continuous touchON1887slices lastchecked, capture103600.
NeedCIartifact/source/checksum ->0101BOOT-only ->clocks/blit on, actualframe
readback and physicalacceptance. No newhardwareframebuffer claim.

## 2026-11-19:0168 IOSurface-to-framebuffer native GPU candidate

Prepared opt-in gpu blit on/off/status. Shared atomic owner serializes all
live GPU diagnostics and framebuffer submissions; framebuffer swaps also
serialize under the existing lock.64KiB retained contiguous scratch holds
four extra source and four destination4KiB L3 tables (8MiB bounds each).
Source pages validated within managedRAM and RO/NX; destination restricted
to actual9e000000..9e465000 panel extent and verified physical mapping.
Native Mesa24.3 parameterized strided shader is768bytes/32regs/TLSWLS0/
preloadR60; SHA88dab0e057aaf95fb42c64e38e24153c7639487442314ebea89f733ca4abf382.
Source cache flush before GPU access, bounded job retirement, and full
rectangle readback before hardwarePASS. Safe retired failure permits CPU
fallback; possible DMA retains source surface and suppresses future panel
writes until reboot. GPU path defaultsOFF; no new hardware blit claim.

Actualsource ASan/UBSan lifecycle tests cover full720x1600 and strided
rectangles, badpages, allocation/AS failure, timeout, faults, corruption,
quarantine, repeat reuse and busyowner. Native shader hash reproduced.
GPU C compiles with actualCI flags. Local framebuffer C++ compile cannot
validate Apple's missing typed-allocation builtins; fullCI is required.
BOOT0100 six-copy checkpoint/touchON retained; no new flash yet.

## 2026-11-19: BOOT0100 six native copy trials PASS; touch restored

After the first tx2 PASS, five explicit gpu copy transactions2482..2486 each
read all1024 source and destination words correctly (mismatches0/PASS1),
submitted1/done1/retired1/IRQ2/MMU0/ASfault0/exception1, shutdown1/fault0.
This validates repeated offscreen nativeG57 execution and owned allocation
reuse; it does not test IOSurface imports, display writes or visible speedup.

UTC1795125218 synchronized. Private79104byte firmware stagedvalid0, load0/
readyA55A/config720x1600; continuous HID tx2480 enabled and tx2487 confirms
streaming1/slices7/events0. LeaveON. tx2488 ioReady1/poisoned0; tx2489 all8
registered with nonzero user/system ticks, including A75CPU6/7. NoHome sent.
SoleconsolePID103600/session54359, boot0100-gpu-copy-live.log (1800seconds
from approximately21:52UTC). Matching0099/0098/0097restore images retained.

Next milestone: serialize framebuffer/probe GPU ownership, import retained
IOSurface pages read-only plus validated framebuffer pages read/write, use
explicit cache ownership/completion, preserve lifetimes until proven DMA
retirement, and allow CPU fallback only when GPU access has ended. Verify
actual pixel readback and repeated physical UI frames before acceleration
or latency claims. Current AppleCLCD::swap still uses CPU row memcpy.

## 2026-11-19: BOOT0100 first native G57 compute-copy hardware PASS

CI44620376179 SUCCESS exactc6b8c85201bc11af9318780694499dc2b323784b.
UploadedGPU/AMFI/bothlayoutheaders exactmatch;0167reversecheck/checksum/
linkedmarkers/SMPPASS. KernelSHA256e3768bd211b39a054e5eea3a9c7088e802ca6e0360853cbc8a0ac4e7ba8f58b3.
BOOT0100SHA25654b0ca51175418cb88ef409b6dd0059dc27e9e5f7967ef8d0dbe6dd55d62fde4.
Same0094ADT/cmd599/all8/1984MiB/23reservations/SMP103485000/stockramdiskDT.
SyncedDownload needed enumeration wait; no flash on first premature detect.
Then Heimdalldetect/BOOT-onlyupload100percent/success/reboot confirmed.

Actual gpu clocks tx1 enables11/11/31, GPU_ID90910010. gpu copy tx2:
hardwarecompute1024words/mismatches0/PASS1; submitted1/done1/retired1,
IRQ2/MMU0/ASfault0/exception1; corepowered1/shutdown1/fault0. Generic output
field is now code bytes, not WRITE_VALUE output; copy PASS checks source
and destination arrays. ioReady1/poisoned0. This proves native offscreen
compute copy, NOT IOSurface/framebuffer acceleration or physicalUI speedup.
Solecapture103600/session54359 boot0100-gpu-copy-live.log; UTC/FW restoration
underway. Needload/startleaveON, repeatedcopy, then guarded framebuffer path.

## 2026-11-19: reproducible primary compute descriptor verification

Added optional --mesa-build to tools/a03-test-gpu-copy-layout.py. It reuses
pinnedMesa24.3 native compiler settings and independently packs the v9
compute job/header, shader program and local-storage descriptors, requiring
byte equality with the prepared kernel layout. Actual test PASS. Native
shader rebuild again reproduces SHA565e07d886d6f111fac39102242d7175f06f0ba5f6f5b52797f8537d0c6814b7.
Both actual BSD ARM64 source compiles repeat PASS. These are host results.
CI44620376179 remains Build/in_progress at21:42UTC; no new flash/copy claim.
BOOT0099 touch streaming1/slices656; display41swaps/36copies (software).

## 2026-11-19: compute-copy CI identified; BOOT0099 touch restored

The successful job build is CI44617226681. The newly staged0167 compute
copy build is CI44620376179, exact c6b8c85201bc11af9318780694499dc2b323784b;
it was still in the Build step at21:38UTC. No duplicate run dispatched.
Private0100 packer and uploaded-source verifier now pin that exact run/SHA.
Host copy layout and actual0166+0167 lifecycle ASan/UBSan tests repeat PASS.
No compute-copy hardware or framebuffer acceleration claim yet.

BOOT0099 private firmware staging completed79104bytes/valid0. Controller
RAM load result0/readyA55A/config720x1600. The first HID stream stopped after
one malformed startup packet (valid15/16); one explicit restart succeeded.
Transaction2484 confirms streaming1/slices44/events0, and2485 confirms
ioReady1/poisoned0. Continuous touch remains ON; no Home injection.
Existing sole capture97724/4575 remains owner of boot0099-gpu-job-live.log.
Next exact CI artifacts/source/checksums ->0100 BOOT-only ->gpu clocks,
one gpu copy, complete readback/retirement checks; restore UTC/touch.

## 2026-11-19: BOOT0099 first real GPU WRITE_VALUE job PASS

Explicitgpu clocks tx1 ID90910010; gpu job tx2 powersall1 thenactual
submitted1/done1/retired1, JOBIRQ00000002/MMU0/GPUIRQ700/JSstatus0/
ASfault0/headerexception1. Output0077ccff003388aa EXACTexpected PASS1.
Corecyclepowered1/shutdown1/fault0. This provesrealGPUjobexecution and
ownedmemoryreadback, notframebufferacceleration. ioReady1/poisoned0.
All8selected/PSCI1..7rc0. UTC1795124111 synced;FWstaging15986 underway,
needload/startleaveON. Singlecapture97724/4575 boot0099-gpu-job-live.log.

Prepared0167nowstaged afteractualWRITE_VALUEPASS. NativeG57compute1024u32
copylayout/source+destreadback,mismatchtests/Mesav9packermatch/ARM64/
113profilechecksPASS. NeedfullCIthen0100BOOTtrialactualcomputecopy.
GoalstillneedsrepeatcopyandIOSurfaceframebufferintegration/physicalframes.
Keep0099jobcheckpoint+0098/0097restores. Nootherpartitionwrites/Home.

## 2026-11-19: corrected0166 CI success; BOOT0099 flashed

CI44617226681 SUCCESS exact6c810448c1f60e62cee8e8c82262a8e239d8f456.
UploadedGPU/header/AMFI exactmatch+0166reversecheck/checksum/markers/
v9primaryschema+ASanUBSanPASS. KernelSHA256
e83efc2b1b02ce851572005a044b3fc5aea1ea5aec0e5852b199a90310d62f0c.
BOOT0099SHA256ac932ced16813eb99092a39e3147e5b573d69eee5efc23559fdcea3fd2926c17.
Exact0094ADT/cmd599/all8/1984MiB/23reservations/SMP103485000/stockramdiskDT
PASS. SyncedDownload/Heimdalldetect/boot-onlyuploadsuccess/reboot.
Singlecapture4575 awaitsCDCthen1800s boot0099-gpu-job-live.log. Needclocks/
gpu job/health andUTC/privateFW/touchrestore. Noactualjob/pixelclaimyet.
0167computeoffprofile;0098/0097restores retained.

## 2026-11-19: corrected job CI active; native copy prepared off-profile

CorrectedCI44617226681 exact6c810448c1f60e62cee8e8c82262a8e239d8f456 is
Build/in_progress. Prior44615378050 cancelled/supersededpreflash. Private
0099packer/sourceverifier updated toCORRECTEDrun/SHA/artifactpaths.
HostMesa24.3built withlocalglibcC11namecompatibility; native128byteG57copy
shadergenerated/disassembled. Prepared0167copy test(fullpage1024u32),
code/source/destinationpermissions,actualMesa v9packbytecomparison,
ASanUBSanlayout+runtime mismatch tests and2BSDARM64compilesPASS.
0167NOTstagedinprofile; nohardwarejob/compute/acceleratedframeclaim.
Nextcorrected0166artifact/source/checksum->0099BOOT-onlyWRITE_VALUEtrial;
onlyafterhardwarePASS stagecompute.0098/touchON kept;singlecapture82938.

## 2026-11-19: G57 v9 job header corrected before hardware trial

NativeMesa24.3 compiler/disassembly generated128byteG57copyshader
(TLS/WLS0/preloadr60),hostonly. G579091usesarch9/v9 jobheader,notv7:
reservedbit0zero/align128. WRITE_VALUEword4corrected10005->10004;
payloadoffsetsunchanged. Earlierprimaryv7testwasinsufficient. Actualv9XML/
layout/submissionword/ASanUBSan/2BSDcompilePASS. Commit6c81044 supersedes
CI44615378050 BEFOREflash; nojobkernelorjobhardwareyet. CorrectedCI next.
Current0098corepowercheckpoint retained; noaccelerationclaim.

## 2026-11-19:0166 committed and CI44615378050 dispatched

Exactd5bc9d2 fullCI44615378050 queued/running forprivateWRITE_VALUEselftest.
Current0098clock/corepowercheckpointretained;touchcontinuousON839slices,
ioReady1/poisoned0. Nojobhardwareyet. Singlecapture82938/30907 remainsowner.
NextsuccessfulCI/source/checksum ->0099BOOT-only->gpu clocks/gpu job,
thenactualfill/copy/framebufferintegration. Do notmarkgoalcompleteatIDor
corecycleorprivateWRITE_VALUEalone.0098/0097restoresretained.

## 2026-11-19:0166 isolated WRITE_VALUE job candidate tested

BOOT0098corepowercycle hardwarePASS remainscheckpoint; privateFWload0/
readyA55A andcontinuousHIDON1/slice1restored. Nojobonhardwareyet.
0166 adds explicitgpu job throughvalidatedcorecycle. Own32KiBcontiguous
allocation(NULLphysicalarg avoidsbelow4GiBmask);checkevery4KiBgranule+end
withinmanaged1984MiB, retainwiredafteranysubmission. AArch644KiBtables map
onlyjob/outputGPUVA;normalNCpages/NX;CPUcacheflushbefore/afterownership.
AS0/JS1/features/IRQmasks/inheritedstatechecks;boundedASupdate/jobpoll/
ownedJS1hardstop/retirement;disableASandrestorebeforecorepoweroff.
CompletionrequiresdoneIRQ/nofault/headerexception1/exact64bitresult.
Unprovenretirementquarantineswiredscratch,skipscoreshutdownandrefuses
furtheractiveGPUcommandsuntilreboot. NoIOSurface/scanout/userspaceABI.
ActualsourceASanUBSan allocation/contiguity/ownership/ASrestore/cache/
completion/fault/timeout/quarantine/no-freechecksPASS;primaryMesalayout
and2BSDARM64compilesPASS;112profile stage. FullCI/hardwarejobpending.

## 2026-11-19: BOOT0098 GPU core power cycle verified

Explicit gpu clocks tx1 repeats GPU_ID90910010/core11/mem11/sys31.
gpu cores tx2: onresult1 shader1/tiler1/L2=1, PMU08000000; shutdown1,
IRQ00000700 (reset/powerchange), fault0. NoGPUjobsubmitted. This verifies
vendorPWRKEY/OVERRIDE/TILER-L2/SHADER sequence andboundedshutdown onactual
A03, notrendering. ioReady1/poisoned0. UTC1795122077 synced; privateFW
staging18079 underway; needload/start/leaveON afterstaging. Capture82938/
30907 boot0098-gpu-cores-live.log. NextownedoffscreenWRITE_VALUEjob with
AArch644KiBtables/cachemaintenance/completion+retirement+pixelreadback.

## 2026-11-19:0165 CI success; BOOT0098 flashed for core readiness

CI44610344415 SUCCESS exact134902f50941015d3390dd94aa54b5d9894d5963.
Artifactchecksum/exactuploadedGPU+AMFI/0165reversecheck/linkedmarkers/
actualsourceASanUBSanPASS. KernelSHA256
400e7df63ab9d69756404a021008eae4d30ab765a2fa12d5eead500b047be1c7.
BOOT0098SHA256b26ed916c36c5fff7ed7e3ad1335c74e358529ce2dee23547d336fb554fdb523.
Exact0094ADT/cmd599/all8/1984MiB/23reservations/SMP103485000/stockramdiskDT
PASS. SyncedCDCDownload->Heimdalldetect->boot-onlyflashsuccess/reboot.
Singlecapture30907 awaitsCDCthen1800s boot0098-gpu-cores-live.log. Need
passivegpu/clockenable then explicitgpu cores, UTC/privateFW/touchrestore.
Nohardwarecorecycle/jobclaimyet.0097/0096/0095 restoresretained.

## 2026-11-19: core-power CI live; private job format prepared

CI44610344415 exact134902f remainsBuild/in_progress. Existingwatch34005;
current0097clockGPU_ID90910010 remainsreadable;noextrahardwarewrites.
PrimaryMesa24.3pan_props maps9091->G57/TNAx;low0010=r0p1. Vendorr0p1
issues omitTTRX3485 (dummyjobWA neededonr0p0). Joblayoutsharedheader+
hosttestcommitted317329d/dd568aa:1024above4GiB bases/4KiBpagewalk/onlyjob+
outputmapped/canary/WRITE_VALUEimmediate64bytes/bounds underASanUBSanPASS,
plusactualprimaryMesaXMLfieldcorrespondencePASS. Notstagedinkernelyet,
noMMU/jobhardwareclaim. Runtimebuffer/cache/completion/retirementpending.
Private0098packer/exactsourceverifierprepared; needCI->BOOTcorepowertrial.

## 2026-11-19:0165 committed; CI44610344415 dispatched

134902f adds guardedcorepowercycle; exactCI44610344415 queued/running.
Current0097 remainsGPU_ID90910010/clocksenabled, touchcontinuousON;
ioReady1/poisoned0,display7swaps5copies/timer17672. NoHomeinjection,
corepowerrequests/jobs/pixelsorframebufferaccelerationclaim. Next exact
CIartifact/source/checksum ->0098BOOT-only ->explicitcorecycle. Single
capture75107/1149 remainsowner;0097/0096/0095 checkpointsretained.

## 2026-11-19:0165 vendor core-power cycle candidate

0097clockenable persists: repeatedpassiveGPU_ID90910010/status100/core11/
mem11/sys31. TouchcontinuousON495slices0events after firmware restore;
physicalUIunverified. NojobsorGPUcorepower requests onhardwareyet.
0165 explicit gpu cores requires exact90910010/onecoretopology, inherited1V,
topbusclocksON, allready/transitionbitszero and noGPUbusy/fault. Pinnedvendor
mali_kbase_pm_driver.c writesPWR_KEY2968a819/OVERRIDE1f01e0078 beforepoweron;
JMsequencepowersTILER(firstL2implicit), waittiler/L2, thenSHADER+120us.
Allwaitsbounded20ms; shutdownshaderthen tiler/L2,restoreoverrideonlyafter
ready/transitiondrain. Timeoutstillrequestsshutdown; doesnotpretendcancel.
Actualsource statefulfakeMMIO ASanUBSan ordering/ownership/allfailurestages/
shutdownandrestorePASS. GPU+AMFI2BSD ARM64MachOcompilesPASS;111profilestage.
Nojob/MMU/IRQ/PLL/voltagewrites/startupcall. FullCI/hardwarecycle pending.

## 2026-11-19: BOOT0097 GPU clocks and actual GPU_ID verified

Explicit gpu clocks transaction1 succeeds on BOOT0097. Beforecore10/mem10/
sys30; TWPLL0004077b/1d89d89d/0003c005 decodes1535999998Hz (register-derived,
not measured oscilloscope frequency); dvfsstate0. Aftercore11/mem11/sys31,
GPU_ID90910010/status100, shaderpresent1/tilerpresent1/L2present1; highmasks0.
GPUdvfsCGM1003/voltage0. PMUforce10102/state07000000/AON2bcac1 unchanged.
This verifies actual leafclockenable and readable GPUcontrol aperture with
sleepingshader, notGPUjobs/pixels/framebufferacceleration. NoPMIC/PLL/rate/
DVFSwrites. ioReady1/poisoned0. All8PSCIrc0/selected8; UARTinterleavegarbles
completionline but perCPU1..7initSGI records present. UTC1795120343 synced.
Private79104firmwarestagedvalid0/load0/readyA55A; continuousHIDON1/slice1.
SinglecapturePID75107/session1149 ownsboot0097-gpu-clocks-live.log.
Next sourcevalidated tiler/L2/shaderpower (vendorPWRKEY/OVERRIDE sequence),
then driverownedoffscreenjob/pixelreadback andframebufferintegration.
Keep0097clockcheckpoint plus0096/0095restores. NoHome/nootherpartitionwrites.

## 2026-11-19:0164 CI success and BOOT0097 flashed

CI44606600103 SUCCESS exact5e1a464a1a8698ee410b159c42c7f7a903c376b1.
Downloaded artifacts checksumPASS; uploaded GPU/AMFI source exactmatches
localtestedsource,0164reversecheckPASS. Linkedclock/SMP/A75markersPASS.
KernelSHA25621f29fb5e015583a1606b8389e38a1db312f9bafdad04230ef026d2fc2bfc253.
BOOT0097SHA256198c4b151668d11cad5d4131ee08e9a2bceb7ec14505d290492a4dbc677d812b.
Same0094inputADT/599bytecmdline/all8/1984MiB,23reservations/SMP103485000/
stockramdiskDTPASS. ActualASanUBSanclocktestsrepeatPASS. CDCsyncedDownload,
Heimdalldetect and boot-onlyflash100percent/success/reboot.0096/0095restores
retained. Singlecapture1149 awaitsCDC then1800s boot0097-gpu-clocks-live.log.
Needboothealth/gpu clocks transaction, UTC/touchrestore. Noactualclockenable,
GPU_ID/job/accelerationclaim until hardwarelogs. Nootherpartitionflashed.

## 2026-11-19:0164 CI44606600103 running;0096 preserved

Committed5e1a464a1a8698ee410b159c42c7f7a903c376b1; fullCI44606600103
is compiling the110patch A03 profile. No leafclockenable yet. Current0096
all8registered with advancing A75usage (cpu6user1499/sys15785, cpu7user1525/
sys15380); continuousHIDON843slices/13events, display6swaps4copies/timer16500.
NophysicalGUI/accelerationclaim orHome injection. Singlecapture69071/session
54337 remainsowner until~20:39UTC. CIwatch94270 writesci44606600103-watch.log.
Privatepack0097.py prepared and requires exactsuccessfulCI/checksum/markers;
next source/artifactvalidation ->0097BOOT-only ->gpu clocks actualID/readback.

## 2026-11-19: BOOT0096 hardware clocks gated;0164 clock-enable candidate

BOOT0096 all8 initialized/SGI PASS. Actual gpu power transaction1 reads
SC2730pd0000/vsel0140 =>1000000uV; conservative700-800mV guard stops
before PMU/AON/leaf writes. Passive gpu transaction3 confirms topstate0,
C0state7, force00010102/AON002bcac1; core00000010/mem00000010/sys00000030:
allthree bit0 gatesOFF; parentselector1/div1 core+mem, sysdivider4.
No GPU_ID/job/pixel yet. Clock-off evidence is now hardware, not inferred.
UTC1795119037 synced; private79104 firmware staged/valid0, load0/readyA55A,
continuousHIDstart and streaming1/slices1 confirmed; leaveON. ioReady1/
poisoned0. NoHome.0096 capture54337/PID69071 owns live log.

0164 explicit gpu clocks requires exact inherited1V rail, already-on top/
bus, three closed leaf gates and inherited384MHzparent/dividers; decode
TWPLL from read-only645a0000 registers and require lockbit18 plus rate near
1536MHz. No PLL/rate/PMIC/DVFS writes. Enable only leafbit0 core/mem/sys in
vendororder,400us settle, recheckdomain, readGPU_ID; invalidID/mapfailure
restores only owned gates. This preserves bootloader1V, not a new recommended
voltage or measured frequency. Actualsource ASanUBSan PLL/rail/ownership/
map/rollback/leaf-onlychanges PASS;2BSD ARM64MachO compiles PASS;110profile
stage PASS. FullCI/link/hardware clockenable still pending.

## 2026-11-19: BOOT0096 power-preflight trial flashed

Goal resumed. ExactCI44591622019 kernel packaged with unchanged0094 input
ADT/599bytecmdline/all8/1984MiB.23liveRAMreservations, exactkernelpayload
rebuild, uniqueSMPtarget103485000 and stockramdiskDT preservation PASS.
BOOT SHA256ffceaeca9e464146a52a0914483eb43a495f704db9b4807d0c594706491d754e.
CDC Download control ->04e8:685d/Heimdalldetect PASS; lowercase boot-only
upload100percent/success/reboot. Singlecapture54337 awaitsCDC then1800s:
boot0096-gpu-power-live.log. Need boothealth, UTC/touchrestore and explicit
gpu power snapshot. No actualpower/clock/GPU_ID/jobs claim yet.0095/0094/
0093 restores retained; no other partition flashed.

## 2026-11-19:0163 full kernel build and artifacts verified

CI44591622019 completed SUCCESS at exact
b8f8f045548a74483757364ed66dfb68ded2f766. Downloaded kernel/buildtree;
SHA256SUMS PASS. Uploaded a03_gpu.c, a03_usb_console.c and sweet_amfi.c
byte-match locally tested sources;0163 reverse-apply check PASS. Linked
GPU power/clock/sharedtopDVFS guard, A75/display and SMP markers PASS.
Actual0163 ASan/UBSan harness repeats PASS including2048 shader/top/bus
combinations. Kernel SHA256:
76f967658ff3406d2ca41751640f4fc69e40ef899511e0fcab35affee2aa5d5b.
Private artifacts: shim/a03/out/ci44591622019-power and corresponding
-power-tree/extracted. No0096 image packed or flashed in this followup;
no hardwareGPU_ID/clocksetup/jobs/acceleration claim. Goal was paused;
this followup verifies the user's completed-build report only. Next resumed
step: pack/validate0096 from exactkernel, then authorized BOOT-only trial.

## 2026-11-19:0163 committed and full CI dispatched

f3e16bd adds preflight; b8f8f04 adds liveDT AONEB1bit7 guard before
sharedtopDVFS access (never starts sharedCPU/MM voltage controller).
Authoritative CI44591622019 exactb8f8f045548a74483757364ed66dfb68ded2f766
queued/running; supersedes44591419852. All3 actualBSD C ARM64MachO compiles
and sanitizer tests repeatPASS; successfulpreflight leaves leaf/GPU/DVFS
banks unchanged. No newBOOTflash/GPU_ID/actualclocksetup/acceleration claim.
Read-only0095 baseline: sameforce10102/state07000000/AON2bcac1, touchON
1842slices169events, ioReady1/poisoned0; display39swaps34copies timer49905.
Singlecapture1745 gpu-power-baseline-20261119.log1800s from~18:45UTC.
Need exactCI/source/checksum->0096BOOTpack/validate->BOOT-onlypowertrial.

## 2026-11-19: power/clock-first0163 preflight candidate

User directs clock and power setups first. Source review identifies0162
shader-C0/top-domain conflation: core0state7 alone does not prove control
aperture off.0163 gates top state only, pending actual hardware GPU_ID.
Explicit gpu power reads inherited SC2730 rail via bounded ADI (181c bit3,
1854 selector*3125uV), rejects disabled/outside700-800mV; no PMIC writes.
Shared runtimeADI atomic ownership covers GPU reads and Download reset.
Clear only top FORCEbit25 if set,300us then bounded2000us top-state wait,
restore changedforce on timeout; enable only AONbusbit11 if needed.
Snapshot APB clocks/QoS, GPU DVFS and topDVFS; leaf gates/rates/PLLs/votes
remain unchanged pending actual inherited-state validation. No GPU jobs.
Actual source ASan/UBSan rail-bound/top-vs-shader/timeout/restore/map/gates/
ADIownership tests PASS. All3 changed C files compile toARM64MachO using
exact44409726184 BSD flags/generatedheaders; no builtin substitutions.
USBsupply+Download existing host regressions PASS;109patchprofile staged.
Full CI/link/BOOT trial and hardware power/clock setup still pending.

## 2026-11-19: BOOT0095 passive GPU trial reaches closed power-domain guard

Resumed basic acceleration experiment. CI44409726184 completed SUCCESS
2026-11-18 22:29:28UTC at exact15b144586351eb9855f5cab3c9fb446139080720.
Downloaded kernel/buildtree; SHA256SUMS, exact0162 reverse-apply against
uploaded source, linked GPU/SMP/A75/display markers and actual probe
ASan/UBSan tests PASS. Kernel SHA256
f1cf4a5acbdcfe411e47c54de7aab808e8e6f8535d39e0bb2a4ec0e81d9ac5e7.
BOOT0095 SHA256
1946fd8085e2ca8d3ba466b504aeb49e85abb583b87e87c57dad20e6f2bf9f5b.
Exact0094 inputADT/599-byte cmdline/all8/1984MiB; 23 live reservations,
SMP target0x103485000 and stock ramdisk/DT preservation validated.

Heimdall uppercase BOOT rejected before writing; rebooted old image.
Early subsequent detect too soon; final lowercase boot upload100percent
success/reboot. Only boot flashed;0094/0093 restores retained. Single
capture29344/session52219 boot0095-gpu-live.log started~18:32UTC for1800s.
Live exact gpu transaction: pmu-force00010102, pmu-state07000000,
aon-enable002bcac1. Core0 state field7, top0; bus bit11 enabled.
Guard reports power/bus gate closed, GPU aperture untouched. No GPU_ID,
power/clock writes, submitted job or accelerated frame. Need validated
power/voltage/clock sequence before actualGPU_ID/jobs; DMA copy remains
an alternative requiring separate ownership/completion/pixel validation.

All8 registered with usage inclA75; VM65147free16KiBpages/compressor0,
ioReady1/poisoned0. Initialdisplay4swaps/4copies, timer13526; no smoothUI
claim. Touchstream0 after reboot. HostUTC1795113345 synced18:35:45UTC;
private79104-byte firmware staging valid0/loadresult0/readyA55A PASS.
First immediate start returned all-FF packets/error-4 and stopped safely;
one later explicit start succeeds streaming1/slices7/events0, inputstatus3.
Leave continuous HID ON; no Home injection. Physical touch/UI unverified.
Final display6swaps/4copies with advancing timer18913: no frame recovery
claim. Repeated passiveGPU result identical. No new power/clock/job writes.
Resolution unchanged720x1600: XR828x1792 discussed only, not implemented.


## 2026-11-18 22:29 UTC: reboot date regression explained; volatile UTC restored

User rebooted and reports wrong date. Committed0150 is228642b (2026-11-17),
staged in current profile; it implements an explicit RAM calendar setter,
not a persistent hardware RTC. Fresh post-reboot time status=439 seconds,
1970-01-01 00:07:19UTC. Explicit host sync sets1795040955 and a separate
status reads1795040955 =2026-11-18 22:29:15UTC, matching host. This verifies
kernel UTC correction only; physical screen refresh/local timezone pending.
No new BOOT flash, RTC/PMIC or filesystem write, Home injection or touch
firmware reload. Reboot also resets volatile touch state; not checked/restored
in this date-only follow-up. GPU basic-acceleration task remains open.
Persistent RTC/boot-time time source is still unimplemented; do not claim
commit0150 made time survive reboot. Capturedate-reboot-20261118.log90s.

## 2026-11-18: GPU scope clarified to basic acceleration

User says most basic acceleration is sufficient, then asks which existing
kernel code is reusable and how it maps to iOS. Target a hardware fill/copy
and IOSurface-to-framebuffer blit with CPU fallback; full Metal/EAGL is not
required for this milestone. Native Linux register/power/clock knowledge and
DMA descriptors can inform an XNU backend; Linux APIs are not an iOS ABI.
Existing SweetSurface/AppleCLCD plumbing and donor HeroGPU/DRM/EAGL bridge
patterns are reusable with board/generation/page-size/ownership changes.
No percentage estimate is justified. Native A03 source d15a5ccedb590915660c321ee2002bddd463b004
has sprd-dma.c transaction-copy support with36-bit address extension; live
DT AP DMA20410000/4000 and clock phandle13 index3 map public DMA gate
APAHB20400000 bit4. Merely reading source does not validate engine ownership,
transfer completion or scanout integration. No DMA writes/test yet.
CI44409726184 remains building; current0094/touch retained.

## 2026-11-18 22:15 UTC: GPU bring-up0162 candidate; acceleration not implemented

User requests A03 iOS GPU acceleration. BOOT0094 still uses software
IOSurface/framebuffer row copies; no A03 GPU job/backend exists. Read-only
live baseline swap4370/copy4365 at now64239220205, lastcopy32186900935;
timer139171 advances. This is a stale-submission observation, not evidence
GPU work is running or that acceleration alone fixes the activity stall.
No Home injection, reboot, firmware change or partition write during audit.

LiveDT confirms sprd,mali-natt at23100000/1MiB, APB23000000,
DVFS23014000 and shared JOB/MMU/GPU SPI60. Reviewed pinned ums9230 vendor
source79c7c8b238a20393a78ee5f1110991bd4280e143 for power/gates/regmap;
see docs/a03-gpu.md. Do not reuse Exynos/Adreno drivers or claim a measured
GPU model without GPU_ID.0162 adds explicit live-worker gpu command only,
read-only PMU/AON gate checks then APB clock checks and gated GPU_ID/status/
core-present reads. Reject force/auto shutdown and core0/top power states.
No MMIO writes, jobs, startup call, compositor or userspace installation.

Actual probe fake-MMIO ASan/UBSan gate/map/ID/no-register-change tests PASS;
actual CI-derived BSD compiles a03_gpu.c and sweet_amfi.c PASS with generated
headers (local include-dir warnings retained); display/SMP regression PASS.
108-patch profile stage PASS. Commit15b1445 pushed; fullCI44409726184 exact
15b144586351eb9855f5cab3c9fb446139080720 queued. Need exact linked artifact,
source/checksum validation and BOOT-only passive trial before hardware claim.
Existing0094/0093 restore retained; continuous touch remains unchanged.
Follow-up22:16UTC: touchON9571slices/1420events, ioReady1/poisoned0;
VM4397free/2965compressor16KiBpages. Later10461slices, still1420events.
Actualframes remain4370/4365 at timer179928; no latency improvement claim.
Donor Mesa opens missing HeroGPU and falls back to softpipe; audit documents
required scalar/buffer/job/IOSurface backend. GPU object contains no FP/SIMD
operands; same CI compile flags include -mgeneral-regs-only. CI now building.


## 2026-11-18: BOOT0094 physical touch responds after Home, but very slow

User confirms touch responds but very slow after the single Home event.
This verifies physical interaction recovered; do not describe0094 as smooth
or latency-fixed. New real swap/copy2046/2041 ->2235/2230 ->2345/2340.
Last paired ~10.98s interval:110swaps/copies(~10.0/s),37continuous touch
slices x16samples(~53.9samples/s). No physicalevents during that particular
interval; prior eventcount311->427 with contacts recorded. This sampling
shows touch collection runs much faster than frame submission in this
window, not an end-to-end latency measurement or proven sole bottleneck.

A75CPU6/7 usage advances; A55s also work. SpringBoard26/17threads and
backboardd56/19threads mainPCs in event waits; no proof this is a scheduler
hang. Software framebuffer row copies are present; GPU acceleration and
capacity-aware performance tuning remain unimplemented. PosterBoard crash
loop is observed, not proven cause. No speculative poll/scheduler changes,
firmware reload, streamstop or new flash. Leave touchON/all8/A75preference.
Existingcapture135205 remains owner;0093restore retained. Performance issue
remains open; Home is a recovery workaround, not permanent source repair.

## 2026-11-18: BOOT0094 user reports touch failure; frame recovery after Home

At21:34:34 UTC user reports touch not working. Existing singlecapture135205
remains owner. Fresh probes: continuousstream1/slices1034/events311; driver
records physical contacts with hid1, inputstatus3 (providers present, notUI
acknowledgement). Frame timer continues but swaps52/copies47 last ~77seconds
earlier. VM25229free16KiBpages/compressor0; ioReady1/poisoned0; same
SpringBoard26/backboardd56 present. PosterBoard repeated crash observed,
not established as this incident's cause. A75 preference remains enabled.

One explicit inputHome press/release dispatchresult0. Subsequent actual
swap/copy52/47 ->58/53 ->116/111 and fresh physical contacts recorded.
No firmware reload, streamstop, reboot or partition write. Continuoustouch
remainsON1/1083slices before subsequentphysicalreports. This demonstrates
frame submission recovery, not yet physicalUI acceptance or a permanent
rootcause repair; userphysicalswipe question pending. Do not inject periodic
Home. Preserve0094 and0093restore. Continue monitoring freshframes/touch.

## 2026-11-18: BOOT0094 A75 preference active; A75s carry most measured work

Heimdall57520 BOOT-only upload100percent/success/reboot ~21:26UTC. CDC returns
~21:27UTC. Exact bootlog policyrequested1; all8 selected/initCPU/SGI1PASS,
PSCIrc0 for1..7 including A75MPIDR600/700. Physicalbootstrap remains A55CPU0.
First ~10second usage delta: CPU0 user13/system63; CPU1 4/14; CPU2 1/7;
CPU3 2/3; CPU4 1/3; CPU5 2/2; A75CPU6 5/577; A75CPU7 7/532. Both A75s
carry1121/1236=90.7percent of measured busy ticks; all8 have positive user
and system deltas. This verifies actual changed placement/work distribution,
not an equivalent-workload speedup benchmark, fullAMP policy or bootCPU switch.

UTC1795037261 synced at21:27:41UTC. Private79104byte firmware stagedvalid0,
explicitloadresult0/readyA55A, continuousHIDtouchstart restored and leftON.
Streaming1/slices56/events0 at21:28:49; no timedstop helper used. VM97823free
16KiBpages/compressor0, ioReady1/poisoned0/7451requests. SpringBoard26 and
backboardd56 present; initialdisplay swap0/copies0 while userspace starts.
PhysicalUI/speedup/stability remain unverified; screen question pending.
SinglecapturePID135205/session56612 boot0094-usb-initial.log runs3600seconds
from~21:27UTC. Preserve0093/0092/0090restores. No other partition flashed.

## 2026-11-18: A75-preferred BOOT0094 built and verified; BOOT-only trial

FullCI44398834193 SUCCESS exact661d5bb18ba35bddecbdd6c125852e08756f5bbc.
Artifact SHA256, SMP+usage+display+A75policy linked markers and actual uploaded
sched_prim.c reverse-apply/exact local source comparison PASS. Kernel SHA256
abfaf10a56f4eadf2eb358b58a045970ef6ec2539ed4ad26b10dad6f5533c382.
BOOT0094 SHA256
ddb03bf32f46bd2b953ec2a6740703176b83003e94658f029c9ed26e33047aa7.
Exact0093 inputADT/all8/1984MiB/root; cmdline599bytes as documented; packer
exactkernel/payload rebuild, unique secondaryentry0x103485000, live23RAM
reservation validation and stockramdisk/DT preservation PASS.

Explicit syncedCDC Download requested; initialHeimdalldetect was too early
and sent no image. Subsequent04e8:685d plusHeimdalldetect PASS; BOOT-only
flash57520 started. Singlecapture56612 waits120s for CDC, then3600s log
boot0094-usb-initial.log. Needflash result, policyrequested1/all8initSGI,
UTC/privatefwload/touchstartleaveON, usage deltas/display/VM/io. No runtime
activation or UI/speedup claim until evidence.0093/0092/0090 restores retained.

## 2026-11-18: requested A75-first scheduling candidate0161

User asks to make the A75 the main CPU XNU uses. BOOT0093 already runs
all eight cores; firmware enters on A55 MPIDR0 and that path remains intact.
Candidate0161 adds opt-in a03_prefer_a75=1: for unbound, non-realtime wakeups,
choose idle logical CPU6 (A75 MPIDR600), then CPU7 (A75 MPIDR700), before
last-CPU affinity. If neither is eligible, existing scheduling handles all
cores. Bound kernel work, realtime selection, all-core recommendation masks,
DVFS and physical bootstrap CPU remain unchanged. This is an idle-placement
preference, not a boot-CPU migration, exclusive pinning or full AMP scheduler.

Guard requires exact validated eight-node A75 identities. Selection uses the
locked pset idle/primary/recommended masks and excludes pending preemption
ASTs. Actual extracted selector passes262144 mask combinations plus disabled,
bound/RT, primary-mask and topology guards under ASan/UBSan; patch applies
and reverses against exact0093 finaltree. SMP ADT regression and offline107
patch profile staging pass. Full Xcode build/link and hardware still pending;
no speedup or runtime activation claim. Keep0093/0092/0090 restore images,
1984MiB and continuous touch. BOOT-only authorization remains active.
Local sched_prim.c cross-compile PASS using exact0093 CI compiler command,
include order/defines and generated headers; no builtin substitutions.
Committed661d5bb; fullCI44398834193 exact661d5bb18ba35bddecbdd6c125852e08756f5bbc
running macos26intel/a03/SWEET/userspacetrue/buildtreetrue. Private0094 input
ADT equals0093; commandline599bytes: remove startup_debug=1 verbosity flag
from prior598bytes and append a03_prefer_a75=1 (otherwise615 exceeds607).
Fresh0093 read-only cpus shows8 registered with substantial work on all8;
frame swaps27394/copies27388. Existing bounded capture had expired; single
new reader writes ignored boot0093-before-a75.log. No reboot/flash yet.


## 2026-11-18: idle follow-up verifies responsive frames without another Home

Continuation audit rechecked unchanged BOOT0093 and clean worktree, with
single capture PID109369 still live. No rebuild/reboot/flash or input
injection during this check. At21:04:49UTC swaps7051/copies7045; counters
remained there through21:05:55 while physical event count4343 was unchanged.
At21:06:09 physical down/move/up events arrived and swaps7175/copies7169
advanced, without any new USB Home/swipe between those snapshots. User
explicitly confirms "Swipe responds and clock is current" without pressing
a button. At~21:06:42 swaps8736/copies8730, touch streaming1/slices11849/
events4728; io ready1/poisoned0. Real frame copies and physical interaction
are therefore verified after idle as well as immediately after recovery.

The active frame-update incident is resolved by the one earlier Home event;
current interactive behavior passes the requested goal's runtime check.
This is not evidence of a permanent source-level repair or a proven original
root cause. No new kernel image is needed for the observed working state.
All eight cores/1984MiB and continuous touch remain enabled. If the symptom
recurs, compare display activity/timer state and retained scanout before
assuming a global kernel freeze. Do not introduce periodic Home injection.

## 2026-11-18: BOOT0093 physical UI recovers after one Home event

On unchanged all-eight-core BOOT0093, one explicit USB HID Home press/release
returned dispatch result 0. Real display work resumed: swaps 40 -> 44 ->
1026 -> 1373 -> 2777 -> 3785 -> 4878 -> 5667 -> 5872; copied layers
34 -> 38 -> 1020 -> 1367 -> 2770 -> 3779 -> 4872 -> 5661 -> 5866.
Independent snapshots may catch entry one ahead of completion. User first
confirmed screen/clock changed, then confirmed "Touch responds and clock
advances" after a physical gesture. A subsequent explicit USB swipe-up also
returned dispatch result 0. These are actual new frame-copy and physical
interactive UI observations, without a kernel rebuild, reboot or flash.
All eight cores/1984 MiB and continuous physical touch forwarding remain
enabled. No partition writes. BOOT0092/0090 restores remain available.

Notification attempts stay zero while frames advance, disproving missing
VBL registration as a sufficient diagnosis. Exact iOS 16 disassembly and
read-only live state identify the primary display server as an EAGLServer
subclass of IOMFBServer. Its CADisplayTimer pointer was null during the
stall and non-null after Home. Alternative render-server callbacks exist,
so null alone does not establish a kernel timer defect. Sleep/wake/activity
state mismatch is a hypothesis, not proven cause or permanent repair. The
panel retains the last framebuffer; an illuminated old clock is not alone
proof of kernel hang. Do not force notifications/fake selectors or inject
periodic Home as a purported fix. Monitor sustained updates and idle/wake.

Follow-up through ~21:03:43 UTC: swaps/copies advanced to6044/6038,
paused for roughly50seconds, then resumed to6095/6089 and6312/6306 before
a second USB swipe; after that swipe6428/6422. User had already confirmed
responsive physical touch and advancing clock. This verifies recovery across
several minutes, not guaranteed idle/wake reliability. No persistent code
fix applied. Incident recovered; investigate activity/sleep if it recurs.
Touch remains ON (11169slices/3690events at21:03:20); io ready1/poisoned0.

Private evidence stays ignored: boot0093-frame-repair-live.log and
/tmp/a03-frame-watch.log; shared-cache disassembly and memory under /tmp.

## 2026-11-18: frame-update investigation; notification hypothesis revised

User activates the frame-update goal. BOOT0093 retains live USB; single
capture host1272 starts at 20:44 UTC for 3600 seconds after prior reader
expires. Display timer continues while swaps40/copies34 remain stale.
Matching UUID-checked iOS16 20A362 cache shows selector72 notification ABI
matches current kernel, but live backboardd CADeviceUseVBL is0. QuartzCore
selects a software display-timer path, so no registered kernel notifications
alone does not prove cause. No forced-present/blanket-success patch justified.
All eight cores and continuous touch remain enabled; no reboot/flash.
Private read-only disassembly and memory snapshots stay ignored under /tmp
or shim output. Actual frames and physical UI verification are required.

## 2026-11-18: BOOT0093 lock screen frozen at12:11; live display counters narrow stall

User reports stillonlockscreen/clock12:11. At20:15:26->20:15:45UTC livekernel
returns1795032926->1795032945; timezone/displayoffset unestablished, so do not
interpret12:11as actualUTC. All8perCPUuser/systemticks substantial: A75CPU6
user1504/system3856,CPU7user1538/system3431. SameSpringBoard25/17threads and
backboardd56/13threads mainCPU counters advance; sampledmainPCs eventloop.
No capturedSpringBoardpanic/crash. VM14604free16KiBpages/compressor0,
ioReady1/poisoned0; HIDstreamON1532->1592slices/434events. No touchstop,
firmwareload,reboot or flash thisturn. Earlierstartupclaimupdated: physical
lockscreenconfirmed, unlock/homeScreen notconfirmed on0093.

Readonly0159display snapshots now give specificprogress:
vsyncentry/done33647/33647 ->34662/34662;
swapentry/done40/40 unchanged; copiedlayers34 unchanged;
notifyattempts0/errors0/success0, skipped24859->25875.
Lastswap10964001995ticks, copy10730482751ticks; snapshotnow16228702068ticks
at26MHz =>~202.5seconds since submission/~211.5seconds since pixelcopy.
Timeranditscompletioncontinue, but no newframes arrive. Actualnotifyhelper
skipsif callbackzero OR portnull (type5isvalid); currentcounters cannot tell
which missingfield/client. No notifications-type registrationlogcaptured.
This doesNOTprove callbackregistration alonecausestall or abi fix; mayneed
exactuserspaceAPI investigation. Kernelclock/coreavailability notwholefreeze.
Freezeinvestigation remainsdeferred perprioruserinstruction; recordfinding,
no speculative renderingchange/build/flash. Leaveall8/1984MiB/touchON.
Singlecapture97574/host32555 until~20:26UTC; preserveowner.0092/0090kept.

## 2026-11-18: BOOT0093 touch restored; all8 cumulative usage continues advancing

Private79104fwstage valid0/loadresult0/readyA55A; explicitHIDtouchstart and
streamstatus1/slices2/events0. BothHIDclientsopen/inputstatus3. LeavestreamON,
no timedstophelper. Freshcpus all8continueuser/systemadvance: cumulativeA75
CPU6user12/system179,CPU7user13/system105 (earlier1/14,1/11); all6A55also
advance. CPU0stillheaviest, notcapacityaware. VM98312free/21130active/978inactive/
6231wired16KiBpages/compressor0, ioReady1/poisoned0/7956requests. SpringBoard25
still1thread startup at20:08UTC; nohomeUI or speedup claim. No capturedSBpanic/
crash in currentboundedlog. Userphysicalbootreplypending. Capture32555until
~20:26UTC. Noadditionalflash. Freezedeferred;0092/0090restoreskept.

## 2026-11-18: BOOT0093 starts all eight cores and schedules real work on both A75s

BOOT-onlyHeimdall64645 upload100percent/success/reboot~20:05UTC. Singlecapture
32555 waits120s thenCDCreturnsUSB005/019. Actualkernel requests8/selects8;
CPU_ONrc0/initCPU/SGI1OK forCPU1..7 MPIDR100..700 via low0x80081000.
CPU0init/SGIalsoOK. InparticularCPU6/7(A75 byvalidatedliveDT) enterEL1 and
passSGI. No capturedpanic. This is firsthardwareall8init evidence, not yet
physicalGUI/stability/speedup proof. CurrentSpringBoard25sample1thread/startup.

Readonlycpusprobe reports8registered and twofullsnapshots. User/systemtick
deltasCPU0..7:47/891,16/773,15/297,15/97,3/46,3/17,1/14,1/11.
All8havepositiveuserANDsystemdeltas: real userspace/kernel scheduling, not
merelypoweredandparked. A75usageislightinthisstartupwindow; CPU0dominates.
NoA75capacityawareness/pinning/DVFSchangeorbalancedworkloadclaim. Private
rawsnapshots/deltas retainedignored. VM118837free16KiBpages/compressor0,
ioReady1/poisoned0; Applelaunchd/SpringBoardstart. UTC1795032388syncedvolatile.

Private79104fwstaging10055 inprogress; continuousforwardingnotrestoredyet.
Needstagevalid0/load0/A55A/touchstartleaveON andfollow-upVM/io/cpus/UI.
Singlecapture32555 boot0093-usb-initial1200s until~20:26UTC; preserveowner.
Freezedeferred peruser.0092twoA55/0090singleCPUrestores retained.

## 2026-11-18: all-eight-core BOOT0093 artifact verified; BOOT-only trial

FullCI44381915946 SUCCESS exact3cf8d518a55389dfc5323962226a3e67045ca6c7.
Kernelchecksum/SMP+trampoline+usage+displaymarkers and actualsource0160/
0158reversechecksPASS; A75IOKitmatchpresent. Kernel SHA256
f2ad40985314f4bf5d842307f5e897200e29880ab7136fe318400b6682a6e63e.
BOOT0093 SHA256
e3c292092852b96ebf07f4294a45faeaac59f8b7c340a1fde538a45485149831.

Same0092root/1984MiB/lowtrampoline/args exceptcpus8. Exact0092ADTseed/nodes/
CPU0+1preserved; addedCPU2..7 uniquephandles, A75compatiblefor6/7. Eight
liveDTtypes/MPIDRs and23RAMreservations validated. Packerexactkernelpayload
rebuild/uniqueentry0x103485000/stockramdiskDT preservationPASS. HosttestsSMP/
CPUusage/trampolinePASS. HostHeimdalldetectDownload succeeds; authorized
BOOT-onlyflash64645 launched~20:05UTC, nootherpartitionselected. Awaitresult/
singlecapture; no8corehardwareclaimuntilCPU_ON/init/SGI andusageticks.
Afterboot UTC/privatefwstage+load/touchstartleaveON; cpus two snapshots to
measureactualuser/systemwork eachcore. Freezeinvestigationdeferred peruser.
Preserve0092twoCPU/0090singleCPUrestores.

## 2026-11-18: user requests Download while waiting; serial reset succeeds

At19:36UTC freshsingleCDCcapture and EP0time status returns1795030581UTC,
so BOOT0092stillresponds despitefrozendisplay. Explicituserrequested CDC
SEND_BREAK Downloadcontrol sent; XNUCDCdisconnects. Initialimmediatedetect
fails duringtransition; subsequentHeimdalldetect succeeds~19:37UTC.
PhoneleftinDownload awaitingall8build44381915946. No partitionupload/flash,
no wipe. Rebootclearsvolatiletouchfirmware/forwarding; restoreafter nextBOOT.
Privatebefore/downloadlogs retainedunderignoredshim/a03/out. Prior0092/
0090images retained. Needexactall8CI/markers/source/checksum before0093.

## 2026-11-18: user redirects next iteration to all eight cores; freeze deferred

User explicitlyrequestsremainingcores nextiteration; defersdisplayfreeze.
NextBOOT0093 supersedesearlier2A55diagnosticplan: sixA55MPIDR0..500 plus
bothA75MPIDR600/700, cpus8,1984MiB, same0092root/args/lowtrampoline except
CPUcount. Existing0159 passivecounters may remain but nofreezeinvestigation
is prerequisite. No touchstop/reboot/flash thisturn;0092state notfreshlyprobed.

CurrentsecondA55 isregistered throughml_processor_register/processor_start,
normalboundstartupthread and scheduler path, notmerelypowered/parked. Existing
hardwareprovesinit/SGI only; no perCPUworkloaddeltas measured. GenericSMP
scheduler handlesselectedcores aspeers; not yetA75capacityaware or UIpinning.
Added0160 A75IOKitmatch (prior tableonlyA55) and cpus readonlyprobe using
sameprocessor_cpu_load_info/recountticks ashoststatistics, listlock/bounded8,
printingafterunlock. User/system/idletickdeltas willmeasureactualusage.
No schedulingpolicy/clock/DVFSchanges or workloadpinning.

ADTgenerator supports8 withrealA75compatible andliveDTchecks. Existing0092
seed/nodes/CPU0+1preserved; onlyCPU2..7added/uniquephandles. Private0093input
ADTstaged (notbootimage). TestsCPUidentities/extensionpreservation/pass and
actual0160C ASan/UBSan bounds/null/lock/no schedulingmutations/pass/reverse.
Localprocessor.c exactCIcommand hitsLinuxClangmissingAppleXNUtypebuiltins;
no replacementsused, fullXcodebuildrequired. PreprocessorconfirmsSWEET1.
FreshfullCI thenexactsource/linkedmarkers/checksum gates beforeall8BOOTtest;
no claimall8alreadyworking. Preserve0092twoA55 and0090singleCPU restores.

All8fullCI44381915946 exact3cf8d51 dispatchedmacos26intel/a03/SWEET/
userspacetrue/buildtreetrue19:35UTC. Supersedesfreeze-only44381013070;
workflowconcurrency maycancelolderrun. Nextexactsuccess->0093all8packaging.


## 2026-11-18: BOOT0092 displayed image freezes; kernel and event loops progress

User reports clock froze~2minutes before19:24UTC and confirms entireimage
unchanged aftertap/swipe. LivekernelUTC1795029873->1795029924->1795029994
(19:24:33->19:25:24->19:26:34UTC) advances. ContinuousHIDstream1 slices1031->
1203->1441, events138->201; physicaldown/move/upcaptured. LeaveforwardingON.
SameSpringBoard26/mainuser6.388049->6.534259->6.772551seconds and system
30.191126->30.222465->30.274337; backboardd56CPUalsoadvances. No captured
SpringBoardcrash/workintervalfailure. VM36961free16KiBpages/compressor0,
storageReady1/poisoned0. This contradictswholedevicefreeze/OOMkill; no proof
allrendering/timerpathshealthy or eventdeliverythroughUIKit. Notjustslowclock:
userentirephysicalimageunchanged. Do notcall0092 stableGUIcheckpoint.

Matchingplainarm64cache/.symbols symbolication slide5ffc000 identifiesmain
SpringBoard/backboardd PCs mach_msg2_trap+8 ->CFRunLoopservice/run/Specific;
SpringBoardcontinuesGSEventRunModal/UIApplication/SBSystemAppMain. MainCPU
deltasprovewakeup/progress despite sameidlePC. QuartzCore render/IOMFBthreads
sampleinMachwait; oneUIKit animationworker semaphorewait isnotprovenrootcause.
Framebufferlog caps at16layers: lacklaterlogisNOTproofswapsstopped.
Privatecaptures/symbolication remainignored. No reboot/flash/touchstop thisturn.

Prepared0159 readonlydisplaycommand: relaxedatomic vsyncentry/completion/time,
swapentry/completion/time/copycounts, notificationattempt/success/error/skip/
lastresult. Observerneveracquiresdriverlock/readsorwritesframebuffer or forces
present; independentfields nottransactionalsnapshot. Neededtodistinguish
worklooptimerstop, notificationfailure, missingframes or pixelpresentation.
Actualobserver+notifyaccounting C++ASan/UBSan/pass/reverseapplyPASS against
uploaded0092source. Existingrendering/notificationreturnbehaviorunchanged.
MandatoryCI stringsadded. FreshfullCI needed before BOOT0093same2A55/1984MiB/
trampoline test. This is diagnostics, not a freeze fix. Singlecapture83709/
58347expires~19:33UTC; checkreaderownerbeforecontinuation. Preserve0090restore.

0159fullCI44381013070 exactc6b9a554e6bef22557909586d139a7bfd2b7ecfa
dispatched19:29UTCmacos26intel/a03/SWEET/userspacetrue/buildtreetrue; running.


## 2026-11-18: user confirms SpringBoard visible on two-core BOOT0092

User reports "springboard is up" at~19:23UTC. This adds physical visibleGUI
evidence to proven CPU0/CPU1 A55 init/SGI and1984MiB RAM; no measuredspeedup,
A75 use or successfultouchgesture claimed. Freshread-only EP0 confirms current
SpringBoard26/19threads andchangedmainstack; touchstreaming1/757slices/events0,
bothHIDclientsopened. LeaveforwardingON; no touchstop/fwreload/reboot/flash.
VM37237free/57668active/22099inactive/9964wired pages16KiB, compressor0,
compressions0/decompressions0. StorageReady1/poisoned0/23302requests.
No capturedSpringBoardcrash/panic in thisboundedlog; not a longstabilityclaim.
Singlecapture83709/host58347 continues boot0092-usb-initial.log until~19:33UTC.
Current0092 remains2A55/1984MiB; preserveasfirstmulticorevisibleGUI checkpoint.
0090singlecore restore retained. Nextuserresponsiveness/physicalgesturecheck;
A75trial separate after thischeckpoint, no automaticflash started.

## 2026-11-18: BOOT0092 touch restored; two-core userspace startup ongoing

Private79104bytefw stage valid0 and explicitload result0/readyA55A pass.
touchstart requestedHID1; streamstatus1/slices2/events0 then1/42/events0.
LeavecontinuousforwardingON peruserrequest; no timedstophelper. HIDclients
notyetseenopen inboundedcurrentlog; SpringBoard26 sample1thread/startup,
so donotclaimGUIready or touchUIresponse. VM108106free/12483active/588inactive/
5525wired16KiBpages/compressor0; ioReady1/poisoned0/5343requests; userspace
continuesstartup. Initialtime set syntaxrejected; corrected time SECONDS
followedstatus returns1795029580UTC withvolatileclock (19:19:40UTC).
Singlecapture58347 remainsactive until~19:33UTC. No furtherflash.
TwoCPUhardwareinit/SGI success remainsproven; independentperCPUtimercounters,
A75/allcores and measuredlagimprovement remainunproven. Currentkernel0158,
BOOT0092 SHA9dda3af2...0639c4fc.0090restore retained.

## 2026-11-18: BOOT0092 low trampoline starts second A55; two-core XNU/userspace

Heimdall36454 upload100percent/success/reboot~19:17UTC. Singlecapture58347
waits thenCDCreturnsUSB005/017. Exact hardwarelog:
A03 CPU: requested=2 selected=2 (limit=8)
cpu0 MPIDR0 initCPU/SGI1OK.
highentry0x103485000 via loadertrampoline0x80081000.
cpu1 CPU_ON target0x100 entry0x80081000 context1 returnsrc0.
cpu1 entersinitCPU MPIDR100 EL1 IRQs0 then SGI1OK.
Final2CPUsinitialized/SGI1verified line captured (interleaved). User independently
reports bootingandUSBvisible. This proves secondA55execution and bothCPUinit/
selfSGI; not allcores, A75, independenttimermeasurement or GUI speedup.
Prior0091 highentry returned-9; lowentry nowworks, supporting entryrangeissue.

LiveEP0VM/io/ps/streamstatus return. VM121804free/1090active/69inactive/
3989wired16KiBpages/compressor0, ioReady1/poisoned0; launchd andSpringBoard26
start. VolatileUTCsync sent. Private79104firmware staging11918 inprogress;
touch currentlyoff0slices/events0 until explicitload/start. Singlecapture58347
900seconds~19:33UTC; verifyownerbeforeanotherreader. Need finishfwstage/load/
touchstart (leaveenabled), follow-upVM/io/SpringBoard andphysicalresponse.
No additionalflash or protectedpartitionwrite.0090restore retained.

## 2026-11-18: BOOT0092 low-shim trampoline verified; BOOT-only deployment

FullCI44375549972 SUCCESS exact87f1b0ed025f69fef9ee199af70146ab3b385343.
Downloaded checksum/all5linkedSMPmarkers and actualsource0158reversecheckPASS.
Kernel SHA256
bb8316472ac6b3d3afc7dea23a658e309f0da31149931571af6ba59e302dabbb.
BOOT0092 SHA256
9dda3af26e6af6002b69b260d7bbb0b4e74c4b0b33c6ec8aaeefb61f0639c4fc.

Packaged same0091 CPU0/CPU1(2A55),1984MiB/root/exactcommandline/ADTseed.
Onlychosen16bytehandoff appended; loader supplies retainedlowshimaddress and
highentry0x103485000. Exactkernel/payload rebuild matchPASS; originalADT after
removinghandoff identical; stockramdisk/DT unchanged. Parser/trampoline/loader,
CPUADT and liveRAMreservation regressionsPASS. Host detects existingDownload
04e8685d andHeimdall beforeauthorizedBOOT-onlyflash36454 launched. No other
partition selected. Awaitflashresult and singleCDCcapture; nofixclaimyet.
Preserve0090 oneCPU/1984MiBrestore. NeedCPU_ONresult/coreinitSGI/timer evidence
thenUTC/privatefwload/touchstart/VM/io/physicalUI. A75trial stayslater.

## 2026-11-18: BOOT0091 CPU_ON rejected with INVALID_ADDRESS; low-shim candidate0158

User transcribes physical screen panic exactly:
panic: A03 CPU: cpu=1 NOT alive: PSCI CPU_ON rc=-9 @SweetCPU.cpp:248
Linux PSCI ABI header identifies-9 asINVALID_ADDRESS. Verified symbol/payload
computes secondaryentryPA0x103481000, above4GiB. Firmware entry-range rejection
is the leading hypothesis; exact acceptance range is not measured. This is a
real CPU_ON failure before proven secondary execution, not successful SMP or
an SGI/timer timeout. CDC never enumerated. Currentphone remains0091panic.

Prepared0158: existing BOOT-shim low-address16byte ldr/br/literal trampoline,
no arbitrary low-RAM page or MMIO. Packer --smp-kernel checks exactkernel/
payload equality and unique secondarysymbol then appends chosen16bytehandoff.
Loader validates boundedADT and target withinloadedsegment before filling
actualretainedshimPA/target and cacheclean. XNU checks length/lowPA/alignment/
exacthighentry and sendsCPU_ON tolowshim; missingbad handoff panics. Existing
1984MiB/root/CPUtopology unchanged. Firmware may still rejectlowentry or reveal
anotherstartupissue; no hardwarefixclaim. Hosttestimage usesold0157 ONLY to
exercisepackaging, mustNOTflash (no0158 kernelconsumer).

ActualboundedADT parser tests everytruncation,duplicate/length/bounds and
shimencoding/alignment PASS. Loader Clangwarnings-as-errors/linkPASS.
0158 actualCIuploadedsource gitapply/structural/reversePASS;0157ADTs and
memoryguardsPASS. Newrequiredlinkedtrampolinemarker gates freshfullCI.
No phonecommands/partitionwrites this turn. NeedfullCI -> exactartifact/
source/markers/checksum ->0092same2A55+1984MiB with --smp-kernel ->BOOT-only.
0090 oneCPU/1984MiB restore preserved; manualDownload needed frompanic.

FullCI44375549972 exact87f1b0ed025f69fef9ee199af70146ab3b385343
dispatchedmacos26intel/a03/SWEET/userspacetrue/buildtreetrue18:59UTC; running.


## 2026-11-18: BOOT0091 flashed; boot text visible but no CDC, exact error pending

User confirms manualDownload; host04e8685d/detect and0091 imagehash match.
Heimdall95543 BOOT-onlyupload100percent/success/reboot~18:51UTC. No other
partition selected. Singlecapture7441 waited120seconds for exactCDC identity,
then exited "A03 XNU CDC console did not enumerate"; no kernel log captured.
User reports boottext or error on screen. Asked exactlastlines (panic/assert/
CPU/timeout/PSCI); replypending. This establishes visibleboottext, not secondary
CPU execution, successfulCPU_ON or SMP. Do not infer stage or root cause
without text. No subsequentflash/reboot/touchfirmwareload/start/stop sent.
Touch is not restored on0091 because execution has not reached accessibleUSB.
0090 oneCPU/1984MiB restore remains available. Next inspect exactscreenerror;
if diagnostic reflash needed, use onlyBOOT and retain current config/checkpoint.

## 2026-11-18: corrected SMP build verified; BOOT0091 two-core trial

FullCI44367277857 SUCCESS exact91ca41ad5769bc434e47200c9346e3c1777a0a32.
Downloaded kernel checksum/all4linkedSMPmarkers and actualuploadedsource
reverse0157 gitapplycheck PASS. Kernel SHA256
c133c3ea30e6cac90635edc1f6ff7d526a35feedb9d6d99a9e351cf4a4e698c6.
BOOT0091-smp2 SHA256
14b9de7c03a1ea48bdbc6cee3b9c506175e46006a4bc28d9f402c45aaca26a7a.
TwoA55 CPU nodes MPIDR0/100, cpus2,1984MiB. Existing0090ADT nodes/seed
preserved; adds onlyCPU1/uniquephandle, args onlycpus1->2. Loader unchanged
exceptimage_size; stockramdisk/DT identical. LiveDT/memoryguards PASS.

Existing0090 USB enumerated1d6b0104 buttty12s0bytes/SEND_BREAKerrno110;
noDownload. Causeunknown, nowholedevicefreezeclaim. User manually enters
Download; hostdetect04e8685d+Heimdall succeeds. BOOT-onlyflash95543 launched;
no otherpartition selected. Preserve0090restore. Awaitflashresult/capture
CPU_ON+bothcoresinitSGI/timers before SMPsuccess. Then UTC/privatefwload/
touchstart (leaveenabled), VM/io and physicalUI test. No touchstop sent.

## 2026-11-18: green SMP build rejected;0157 context corrected against CI source

Run44357697720 completed SUCCESS exact73b554a. Downloaded kernel checksum
1ef6b6b488cc6d193300aad98244491be301339c4d4053553ef5389079eb6254 passes,
but required A03 CPU startup/PSCI/completion strings are absent. Actual
uploaded source remains singleCPU. Build log explicitly warns0157 skipped:
SweetCPU.cpp:37 patch does not apply. Upstream build.sh warns and continues
on patch-check failure, so green build did not contain requested SMP code.
DO NOT flash this artifact or pair it with cpus2; no0091 image was created.

Root cause: earlier local baseline contained uncommitted diagnostic strings
prefixed0009 CPU while actual staged0085 source uses CPU. Prior local patch
application check therefore did not represent CI source. Corrected22 removed
lines in0157 to match actual uploaded source (11 prefix changes). Plain git
apply, structural assertions and reverse check now pass on actual44357697720
source. Added linked-SMP marker validator and CI gate; regression rejects each
missing marker and the actual incorrect green kernel. No compiler/runtime
success claimed for corrected0157 until fresh fullCI.

Read-only pretest CDC capture attempted; tty opened but EP0 serial discovery
reported console not connected; USB VID/PID remains visible. No reset/flash,
no touch start/stop or firmware load sent. Last verified0090 RAM/touch state
is historical; no fresh runtime status established this turn. Capture ended.

Replacement fullCI44367277857 dispatched exact91ca41ad5769bc434e47200c9346e3c1777a0a32
onmacos-26-intel/a03/SWEET/userspacetrue/buildtreetrue at18:13UTC; running.
It includes corrected0157 and mandatory linked-SMP markers. Next exactsuccess
then source/marker/checksum checks before2A55 BOOT-only packaging/deployment.



## 2026-11-18: SMP CI failed before runner acquisition; alternate pool dispatched

User reports failed build44352036471. GitHub check annotation says:
"The job was not acquired by Runner of type hosted even after multiple attempts".
Job134970001981 has zero steps and conclusioncancelled; overallrunfailure.
No compiler ran, no failed-step log exists and no kernel artifact was produced.
This is runner allocation failure, not evidence0157 compiles or fails.

Dispatched44357697720 on existing workflow optionmacos-26-intel,
boarda03/MACHINE_CONFIGSWEET/ios-userspacetrue/buildtreeuploadtrue at17:21UTC.
Current branch73b554a contains the identical0157 patch fromb6a3a15; only
subsequent handoff docs differ. Need runner acquisition then actual full build
and artifact checks. No phone commands, firmware changes or flash this turn;
last verified BOOT0090=1984MiB/oneCPU/touchforwardingON, currentstateunprobed.

## 2026-11-18: final SMP candidate adds explicit EL2 CPU identity

Secondary reset now copies MIDR/MPIDR into VPIDR/VMPIDR before EL1, matching
boot shim; avoids trusting firmware's virtual identity reset value. Actual
start.s CI-command compile and actual-patch/ADT regression PASS again.
FullCI44352036471 exactb6a3a1582faecab02521ad5a210c580e66090b66 queued;
replaces cancelled44351323590 (concurrency superseded). NoSMPflash scheduled.
Last0090 runtime: VM41986free/57342active/17782inactive/9850wired16KiBpages,
compressor0; eMMCready1/poisoned0; SpringBoard25/24threads; continuousHID
streaming1/1243slices/events0. Physical responsiveness afterRAM change asked;
replypending, no speedup claim. Touch remains enabled. Singlecapture16666/
host21134 deadline~16:51UTC; check owner before next reader.0090/0089/0088
private images retained. Next exactfullCI success -> verify artifacts and
package2A55/cpus2 with1984MiB -> BOOT-only -> eachcore timer/SGI/runtime.

## 2026-11-18: opt-in A03 SMP candidate0157 prepared

Adapted donor0065 CPU_ON/reset/per-CPU publication and targeted SGI path to
actual A03 CPU source; A03 patch profile previously stopped at donor0018.
Live DTB describes A55 MPIDR0..500 and A75 MPIDR600/700, PSCI0.2/SMC.
Candidate has bounded8core topology, default1; ADT packer exposes only1/2/6
A55 trials and validates selected live nodes and conduit. First hardware
candidate must use2A55s before six or A75s. No CPU clock/DVFS changes.
EL2 entry uses A03 boot CPTR0x33ff/HSTR0/ICH_HCR0, not donor reset defaults.
Existing GIC redistributor lookup is local perCPU, not global perCPU state.

ADT identities/state/uniquephandles/roundtrip/default/count guards PASS.
Plain git apply --check on actual extracted A03 source PASS. Exact CI command
local start.s and machine_routines.c compile PASS after refreshing exported
SWEET.h (first try used stale export, undefined limit; corrected). CPU driver
local C++ compile blocked by LinuxClang lacking Apple's allocation builtins;
no fake substitutions used. Exact cpu.c compile command absent in cached log.
Additional cpu.c compile PASS with retargeted machine_routines CI flags
(not exact per-file replay). Full Xcode CI44351323590 dispatched exact
71436b187a5654920f7936ccea488ac0be8e97e7/mac15intel/a03/SWEET/userspace;
queued awaiting runner16:49UTC. Full Xcode CI required before packaging/deployment. No multicore runtime
success claimed. BOOT0090 remains1984MiB/cpus1; continuousHIDstream1
632slices/events0 and SpringBoard25/24threads measured; VMcompressor0.

## 2026-11-18: BOOT0090 expands managed RAM to1984MiB

User requests multicore/full RAM to address severe lag. Current BOOT0089
was cpus=1/1024MiB. Live DTB bank is0x80000000+0xfffff000; checked all23
reservations. Added bounded1984MiB profile at0x102000000..0x17e000000,
retaining about32MiB before live bank end. This is NOT full4GiB: lower
memory contains secure/modem/framebuffer reservations and requires VM holes.
Actual loader predicate/synthetic last-page/bank/header reservation tests and
live-DTB validation PASS; freestanding loader Clang warnings-as-errors/link PASS.

BOOT0090 reuses exact0089 kernel b316c806...bf14 and command line. Payload
changes only header mem_size and chosen dram-size; stock ramdisk/DT preserved.
BOOT SHA256293de28bcf5a6f0c89f66873b5df112abb1ef9e10f0bcddc9604439210990f1a.
Synchronized CDC Download followed by BOOT-only Heimdall upload100percent/
success/reboot at~16:40UTC. No other partition selected. CDC returns; single
capture hostsession21134 writes boot0090-usb-initial.log for600s.
VM117024free/4796active/161inactive/4903wired pages, page-size16384;
later94424free/24725active/1455inactive/6364wired, compressor0/compressions0.
Storage ready1/poisoned0; SpringBoard25 and other iOS processes execute.
This proves increased usable memory, not a measured GUI speedup.

Initially noUSB then freshly enumerated0089 showed startup and touchstream0;
reason for prior reboot unknown. After0090 explicit private79104byte firmware
stage valid0/load0/readyA55A and both HID clients open; touch start restored
continuous HID forwarding, streamstatus1/slices2/events0. Leave enabled per
user request.0089/0088 restore images remain private. SMP candidate separate.

## 2026-11-18: user requests touch remain enabled; timed stop removed

User states touch appears to work when enabled and explicitly requests leaving
it enabled. Terminated only host timed-stream PID12128 with SIGTERM, which
does not execute its Python finally-stop; no kernel stop command was sent.
Follow-up exact streamstatus confirms streaming1/slices974/events38. No timed
HID helper remains. Kernel continuous forwarding is left ON for this boot.
Firmware remains loaded; reboot still requires explicit firmware load/start.

Before this request, three physical home-bar swipes were captured with true
down/movement/up:397,1599->418,648;390,1572->493,568;388,1590->420,312.
User reported no visible response for those swipes. Together with five earlier
tap events this totals38events. Settings opening animation and Preferences283
launch remain proven; Settings content was black with home bar, and successful
home gesture/Settings scrolling are not proven. No captured CA_CLIENT create
diagnostic or work-interval abort on0089; specific0156 runtime path unproven.
Capture93357 continues in boot0089-usb-initial.log until its one-hour deadline.

## 2026-11-18: physical tap launches Settings on BOOT0089

User explicitly reports tapping Settings and seeing its app-opening animation.
The active HID stream records two physical contacts:444,1149 ->449,1152/up
and613,946/up (five events total), with matching SweetHIDTouch down/up logs.
ps independently confirms Preferences283 launched; SpringBoard remains26.
This is the first correlated physical tap -> visible app-launch animation
and actual application process evidence. User then reports black app content
with home bar, still waiting; fully rendered Settings/scrolling is not proven.
Preferences sample shows12threads and main CFRunLoop/GSEvent/UIApplication
event loop. No CA_CLIENT WIcreate diagnostic or work-interval abort captured
yet on0089; do not claim0156 hardware creation path proven merely from silence.

First120s HID window completed306slices/events0 and explicit stop. A600s
window began~16:29UTC (host11069, boot0089-physical-hid-long.log), received
the five events above, and remains active for the requested home-bar swipe.
Capture93357 remains the only tty reader. Firmware is loaded.

## 2026-11-18: BOOT0089 CA-client candidate deployed

CDC returned; single reader93357 is active. Volatile UTC sync read back
1795018860=2026-11-18 16:21:00UTC. Private79104-byte firmware staging valid0
and explicit RAM load result0, readyA55A/config20002AD4/1028/report20011580/60,
geometry720x1600 sensors18/32 all pass. Ten-second log-only idle trial completed
30slices/events0 and explicit stop. Both HID user clients opened; inputstatus3.
SpringBoard26 samples still show startup (one thread, dyld/libobjc/libdispatch
initialization); no HID gesture sent yet. Normal backboardd WIcreate flags
20000000/20000002 return error0/kr0. Actual CA_CLIENT path remains untested.

Full CI44192146474 succeeded for exact fd1fc5e59b7c9f3bee377bb1fb1a7c6541c42e7e.
Downloaded artifact checksum verified; kernel SHA256
b316c806e65c1cf7194012f14b6e2fef7c35782de68cadb783971a225d2cbf14.
BOOT0089 SHA256 d897364f9a6f1c9799472a3d29a816e0be890f4f45b3488eb64bbf43754c999c.
Packaging preserves0088 ADT,1GiB geometry,bootargs and loader except image_size;
wrapper verifies matching stock ramdisk/DT. Both work-interval host tests pass,
including actual policy C/C++ ASan/UBSan8192flag cases.

Initial uppercase --BOOT attempt was rejected because A03 PIT uses lowercase
boot; no partition upload occurred. Synced CDC Download was repeated, then
heimdall flash --boot completed100percent/upload successful/reboot at~16:20UTC.
Single capture hostsession93357 waits for CDC in boot0089-usb-initial.log.
Private firmware reload and runtime CA_CLIENT create/UI response remain pending.
This is successful build/deployment evidence, not a proven touch repair.

## 2026-11-17: exact swipe failure is CA_CLIENT privilege denial

Second aligned0088 swipe391,1597 ->431,572 produces15HIDevents. User first
reports no response then spinner. New diagnostic logs SpringBoard flags
30000000/error1(EPERM)/kr8(KERN_NO_ACCESS), followed by the same Failed to
create work interval exception. This is the privilege-return branch before
kern_work_interval_create, not an allocation attempt/ENOMEM or task-app check.
Explicit stop completes130slices/events15; forwarding off.0155 alone does
not fix UIKit: its request omits the documented UNRESTRICTED bit.

0156 candidate treats CA_CLIENT as implicitly unprivileged under the existing
a03_work_interval opt-in. Other types retain0155 policy. Actual kernel create
still validates CA_CLIENT noGROUP/app-type/single-interval ownership and all
port/lifecycle rules; no fake handle/success. Actual policy C/C++ ASan/UBSan
8192flag cases and reverseapplyPASS. Local kernel C compile uses retargeted
cachedconsole flags, not the missing exact per-file CI command. FullCI next;
app-type validation may reveal another failure, so no runtime fix claim.

FullCI44192146474 exactfd1fc5e59b7c9f3bee377bb1fb1a7c6541c42e7e is
running macos15intel/a03/SWEET/userspace true. Package-only0089 waits exact
SUCCESS/checksum/markers/same0088 configuration; no automatic deployment.

## 2026-11-17: BOOT0088 first swipe no visible response, temporary audio wait

User confirms iOS visible/ready22:35UTC. Explicit60s HID trial receives one
swipe416,1581 ->413,451,18events,178slices, clean stop. User reports no visible
response. No SpringBoard crash or SpringBoard WIcreate diagnostic appears.
Main thread sample after swipe resolves (cache15410000) to AudioToolboxCore
AURegistrationServerConnection::Connect, CADeprecated singleton/IPCAUClient
registration and audio-component findNext. This is a sampled main-thread IPC
wait, not a proven permanent blocker. Subsequent sample~22:37UTC returns to
CFRunLoop/GSEvent/UIApplication main loop. Thus this trial does not exercise
or prove0155 fix. A second90s window14155 begins~22:37:30UTC after that wait;
user asked one aligned swipe, visible response pending. Firmware remains
loaded; no new flash. Normal backboardd WIcreate still succeeds flags20000000/
20000002, error0/kr0. No fabricated success for the missing client path.

## 2026-11-17: BOOT0088 running, firmware loaded, UI still starting

BOOT-only flash17164 completes100percent/success/reboot~22:28UTC. Single
capturePID141846 writes boot0088-usb-initial.log (host41773,2400seconds).
UTC sync1794954586=2026-11-17 22:29:46UTC. Private79104-byte touch firmware
staged/valid0; explicit load0 again passes seven hardware CRCs, readyA55A,
config20002AD4/1028 report20011580/60 geometry720x1600 sensors18/32;
SPI gate/source restored. No touch forwarding enabled on0088 yet.

Both HID clients opened and inputstatus3; ps shows SpringBoard25. First0155
hardware diagnostic: backboardd flags20000000/error0/kr0, confirming normal
privileged create still succeeds. This does not test unrestricted CA-client
policy. User reports Apple logo or boot logs at22:31UTC; wait for actual UI.
streamstatus confirms0slices/events0. Work-interval crash fix remains unproven.

## 2026-11-17: BOOT0088 work-interval candidate fullCI success/deployment

CI44186495805 SUCCESS exact47a92b35332aac7a9c6173e2d57f18125a525c0d.
KernelSHA256 245542b4cdec8f7b26d7b8a20ce7955b706d4d6ac16727b602e3ff2b040cdab2.
BOOTSHA256 1e3309cb2a186fb931fae7bc0e85a6237b77424f7de1b1d9aff6c26afec696f3.
Artifact checksums/0155 marker and0087 configuration preservation pass.
On resume22:28UTC no XNU CDC device, Samsung04E8:685D already enumerated;
Heimdall detect succeeds. Attempted CDC Download sender reports noenumeration,
so it did not request this transition; its cause is not established. Authorized
BOOT-only0088 flash17164 now in progress; no other partition selected.
0155 is still a candidate for the UIKit work-interval abort, not proven fixed.
Next singlecapture/UTC/privatefirmwareload -> WIflags/error/kr -> physicalUI.

## 2026-11-17: displayed clock stale after crash, kernel time advances

User reports clock still2:03 at~22:12UTC/23:12Berlin, about9minutes stale
under the inherited UTC-8-style display offset. Explicit time status returns
1794953574=2026-11-17 22:12:54UTC, so the kernel clock is advancing. ps shows
replacement SpringBoard1079, not crashed26; sample1079 has24threads and the
same CFRunLoop/GSEvent/UIApplication main-loop PCs (cache38858000). Thus
whole-device freeze is contradicted, while user sees a stale GUI clock.
Do not infer fresh display presentation from a live process/event loop.
0155 fullCI44186495805 remains Build. Touch forwarding remains off.

## 2026-11-17: swipe crash enters UIKit event processing; no OOM evidence

User asks whether lag/RAM exhaustion caused the spinner. Captured failure
is an uncaught NSInternalInconsistencyException, explicit Failed to create
work interval, followed by SIGABRT6; no captured jetsam/memory-pressure kill
or allocation failure accompanies it. This does not rule out general memory
pressure or ENOMEM as an underlying create error; actual flags/errno await
0155 diagnostics. Avoid equating this observed abort with an OOM kill.
First-throw frame1C178F7BC resolves with cache slide38858000 to UIKitCore
_UIQOSProcessingBegin+21C; caller1C17910DC resolves _eventFetcherSourceCallback
+A8. This supports physical HID events reaching UIKit processing, beyond
kernel dispatch alone. No successful unlock/app launch is yet proven.

Initial single capturePID128605 exited on its configured deadline; tty owner
was absent before starting new single capture boot0087-usb-after-swipe-crash.log
(hostsession32643). Forwarding remains off.0155CI44186495805 now Build;
package-only hostsession29898 remains the next exact-success artifact gate.

## 2026-11-17: aligned physical HID swipe reaches SpringBoard crash

User explicitly ready22:01UTC. HID120s window captures61events over205slices;
four physical swipe down/move/up sequences reach SweetHIDTouch, e.g.
380,1566 ->454,393. User reports several swipes then loading spinner and
suspects SpringBoard crash. Logs confirm SpringBoard26 SIGABRT with
NSInternalInconsistencyException: Failed to create work interval. This is
strong evidence input triggers UI processing, not successful navigation.
Explicit stop22:03UTC; timed helper later confirmsstreaming0. No polling
errors. Need repair runtime compatibility and repeat physical UI test.

0155 candidate restores documented WORK_INTERVAL_FLAG_UNRESTRICTED policy:
only DEFAULT/COREAUDIO/CA_CLIENT skip privilege with existing a03_work_interval
opt-in; normal kernel create/app-type/lifecycle validation remains. Current
sys_work_interval CREATE2 unconditionally checks privilege despite its header
explicitly documenting this exemption. Supplied SpringBoard XML lacks work-
interval entitlement; backboardd has it. Actual failing CREATE2 flags/errno
were not captured (startup trace cap), so this is a concrete compatibility
candidate, not yet a proven crash fix. Adds bounded create flags/error/kr
logging. Actual policy C/C++ ASan/UBSan8192cases and reverseapplyPASS.

Candidate sys_work_interval.c compiles locally with the existing console C
CI command's target/include/definition environment retargeted to this file;
its own per-file compile command is absent from the cached CI log, so this
is not an exact per-file CI replay. No compiler errors; full Xcode is the
linkage/actual-build gate. FullCI44186495805 exact47a92b3 dispatched with
macos15intel/a03/SWEET/userspace true. Package-only0088 gates exactSUCCESS,
checksums/markers and unchanged0087 config; no automatic flash scheduled.

## 2026-11-17: ten-minute HID window ends cleanly; UI test still pending

Host600second trial ends~21:55UTC, active1760slices/events0 then explicit
stop1761slices/events0 (28176frames). Follow-up streamstatus confirms
streaming0. No stream errors or SWEET HID physical down/up logs occurred in
this interval. This extends continuous idle/stop evidence, not actual event
queue delivery. Earlier log-only physical down/move/28report-driven lifts
remain established; no physical contact arrived during the HID window.
User visible-response question is unanswered. Do not repeat idle windows as
a substitute for an aligned physical HID/UI test. BOOT0087 remains running,
firmwareloaded; singlecapturePID128605 until~22:06UTC. Touch forwardingOFF.

## 2026-11-17: BOOT0087 event loop alive during long HID window

Explicit sample26 while HID streaming shows SpringBoard24threads and main
PC1F7986194, captured cache slide38858000. Matching-cache symbolication
resolves mach_msg2_trap+8 -> CFRunLoop Mach-port service/RunSpecific ->
GSEventRunModal -> UIApplication _run/UIApplicationMain -> SBSystemAppMain.
Thus the current boot is in its event loop; this is not screen/UI evidence.
Live stream status21:46UTC shows246slices/events0, no stream error. Physical
contact/UI reply still pending; do not treat the absence of events as a failed
HID dispatch. Ten-minute hostwindowPID130376 remains live, autostop~21:55UTC.

## 2026-11-17: longer HID gesture window after physical release proof

Completed log-only capture has87logged events:59down/moves before the cap,
28releases, slot0only, x16..719/y83..1587. Final eventcount341 unchanged
by stop confirms no held contact remained. Following120second HID trial
finishes350slices/events0, without errors: no physical contacts arrived in
that interval, so HID delivery remains untested. Started600second HID window
~21:45UTC (hostsession44699), auto-stop~21:55UTC. Visible response question
remains pending. Current capturePID128605 remains live until~22:06UTC.

## 2026-11-17: physical lift transitions confirmed on BOOT0087

Two-minute continuous log-only stream starts~21:40:46UTC; at active status
238slices/events302, contact logs already include25slot0 up transitions
at distinct nonzero coordinates, interleaved with down/motion. Final status
360slices/events341; explicit stop361slices/events341, so stopping adds no
up event. No stream error. This separates real report-driven lift from
synthetic session-final cleanup. Down/motion/up chain is now measured on
physical hardware, with no HID forwarding in this session. First motion
starts385,1545 and moves upward across many coordinates. Full logged range
and release count retained in private capture; motion cap omits later downs.
A two-minute physical HID-forwarding trial starts~21:42:48UTC; visible UI
response asked separately and remains pending. Do not infer UI success from
coordinates or dispatch logs.

## 2026-11-17: BOOT0087 continuous log-only polling works on hardware

BOOT-only flash completed100percent/success/reboot21:35UTC. Single capture
PID128605 writes boot0087-usb-initial.log. UTC sync1794951400 confirms
2026-11-17 21:36:40UTC. Private79104-byte firmware restaged/valid0; explicit
load0 verifies all seven hardware CRCs; readyA55A/config20002AD4/1028,
report20011580/60,720x1600,18/32; gate/source restored.

Timed log-only continuous stream runs30seconds, reaches84slices while active
then stops at85slices (1360frames), events0. No stream error logged. This
proves continuous worker progress across former300frame windows and explicit
stop on actual hardware, with no phantom idle contacts. Both HID clients
open. Ten-second HID-enabled idle trial started next; no physical user input
or UI response claimed. Current screen/readiness question pending.

Ten-second continuous HID idle trial then completes34slices (544frames),
events0, no stream error; active status reports33slices before explicit stop.
No physical input arrived during either baseline. Polling is now stopped.
This verifies continuous HID-enabled idle safety, not actual queue delivery.

## 2026-11-17: continuous touch full CI success, BOOT0087 trial

CI44178262587 SUCCESS exact10b9f9bdff20e8db99f60e9db033f8b08304cfe9.
KernelSHA256 f1709990dacf97ebf89424dec6debf013f0cd9fa9f739d458274c2e9e1bba0df.
BOOTSHA256 b893cd32b30222c8c9f4692dfa49791be6a0869868c0b808f2421fcf02785a25.
Artifact checksums/stream markers verified;0086 ADT/1GiB/bootargs/root,
loader except image_size and stock ramdisk/DT unchanged. SyncedCDC Download
request followed by04E8:685D and Heimdall detect success21:35UTC. Authorized
BOOT-only flash49418 in progress; no other partition selected. Next single
capture/UTC/private volatile firmware load -> continuous log-only physical
lift -> HID/UI test. Build success is not working physical touch evidence.

## 2026-11-17: BOOT0086 first HID-enabled idle baseline

Explicit touch poll2483 completed result0/valid300/events0/hid1, with three
count0/statusFF idle packets and normal SPI gate/source restoration. This is
the first hardware poll with HID forwarding enabled; no actual event was
emitted, so it does not establish HID queue delivery or visible UI response.
Physical lift/user-aligned input still pending. Full0154 CI44178262587 later acquired its runner21:23:28UTC and entered
Build21:25:02UTC; still running21:29UTC. Package-onlyPID124809 remains live.

Added explicit host timed-stream helper for0154: defaults log-only, correlates
BEGIN/END by exact command and worker ID, preserves an existing active stream,
and requests stop in finally even after a lost start acknowledgement. Host
regressions pass transaction correlation/lost-ACK cleanup/existing-stream
preservation. Status probe on0086 correctly shows stream commands absent;
no start sent. Firmware load remains a separate explicit operation.

## 2026-11-17: BOOT0086 SpringBoard main event loop measured

Explicit sample25 at~21:20UTC shows main thread PC1E9B8A194. Matching private
plain-arm64 cache/.symbols UUID-validated symbolication with captured cache
slide2AA5C000 resolves mach_msg2_trap+8, mach_msg_overwrite, CFRunLoop Mach
port service, CFRunLoopRunSpecific, GSEventRunModal, UIApplication _run /
UIApplicationMain and SBSystemAppMain. This establishes a running application
event loop, not a physical screen or touch acknowledgement. Both HID user
clients are open; inputstatus3. No touch HID session sent. Continuous0154
fullCI44178262587 remains queued; packagePID124809 alive, no auto deployment.

## 2026-11-17: explicit continuous touch polling prepared (0154)

0154 adds serialized probe-worker slices of16frames with retained contact
state across slices. touch startcontacts is continuous log-only; touch start
requires the HID provider and forwards events. touch stop releases once;
streamstatus remains available, and uploads/other touch probes are refused
while streaming. SPI registers and gates are restored between slices. ROM,
ready/config/read failures release and stop. No automatic firmware load or
boot-time input. Release events bypass the64-event motion log cap.
Actual poll C11/C++17 ASan/UBSan tests pass retained held states, physical-
style idle release before cleanup, ROM/config-error release. Actual command
policy C ASan/UBSan tests pass provider gating, log-only/HID isolation,
double-start preservation and idempotent stop. Kernel console C cross-compile
and reverse patch dry run pass. Not deployed; BOOT0086 remains current.
Physical lift/HID/UI verification still pending user aligned touch test.

Full CI44178262587 dispatched exact10b9f9bdff20e8db99f60e9db033f8b08304cfe9
on macos15intel/a03/SWEET/userspace true. Package-only watcher prepares0087
from unchanged0086 ADT/bootargs/root/loader/stockramdisk/DT after exact-success
and checksum/stream-marker checks. No automatic deployment scheduled.

Follow-up clean forward patch applies with fuzz0 and reproduces both compiled
files exactly; shared/kernel poll-header equality passes. Final console C
cross-compile and decoder/contact/dispatch/upload ASan/UBSan regressions pass.
A second0086 log-only session2481 again gives300valid/events0/hid0, with the
same three count0/statusFF idle reports. No user-held alignment or HID claim.

## 2026-11-17: BOOT0086 hardware idle reports are clean

BOOT-only flash completed successfully and rebooted; single console capture
PID122914 writes boot0086-usb-initial.log. Host UTC sync1794949748 is
2026-11-17 21:09:08UTC. Private79104-byte firmware restaged with validation0;
explicit RAM load result0 verifies all seven hardware CRCs, readyA55A,
config20002AD4/1028, report20011580/60,720x1600,18/32 sensors.
First log-only contacts session on0153: result0, valid300, events0, hid0.
All three raw idle reports are0000FF followed by57zero bytes. This directly
confirms the zero-count fix removes phantom corner contacts on hardware.
Gate0A02DE00/clock0 restored. Physical down/movement are previously proven;
true lift and HID/UI delivery remain unverified. No touch poll sent yet.
Local timezone remains unresolved; host UTC sync is volatile, not an RTC fix.

Follow-up poll regression exercises a real held->count0/statusFF transition:
release occurs at sample2 of3, before final session cleanup, with one down
and one up only. Actual shared poll code passes C11/C++17 ASan/UBSan.
This is software validation, not physical-lift evidence. Input status on0086
returns3; both HID service user clients opened. User alignment pending.

## 2026-11-17: idle decoder fullCI success; BOOT0086 deployment

CI44173996698 SUCCESS exact896330554fd2683801355f753927d4642716cd18,
0153 zero-count decoder. Kernel81d48ecfc9a800bbb8a76868b14303de16929efdb3c6e2d6afc4701a3cf41ba6.
BOOT221de96d02edb1ac0552057a651c67a1c08ad622aaf76dde9136c6a2a9be8126.
Packaging checksums/markers/same0085 ADT/1GiB/bootargs/root/loader(except
image_size)/stockramdisk/DT verified. SyncedCDC Download and Heimdall detect
21:07UTC; BOOT-only flash67897 in progress. No HID event trial yet. Next
singlecapture->UTC/fw upload/load->idle noevents->physicallift->boundedHID.

## 2026-11-17: physical finger MOVEMENT confirmed on0085

User reports ready for movement test; explicit start instruction immediately
followed by two serialized log-only300frame sessions. Both result0/valid300/
events301/hid0, slot0 coordinates continuously follow movement; first logged
capture x159..553/y397..1282, secondx148..520/y303..1148 (64event log cap).
Raw packets count1, real big-endian coordinates, other slotsFFFF. This proves
physical coordinate motion, not HID/UI response. Session-final up remains
cleanup; true physical lift awaits0153 idle fix. User told release afterward.
No touch poll/HID sent. FullCI44173996698 exact8963305 still builds0086.

## 2026-11-17: zero-count fix full CI dispatched

0153 fullCI44173996698 exact896330554fd2683801355f753927d4642716cd18
macos15intel/a03/SWEET/userspace true dispatched20:53UTC. Package-only70851
/tmp/a03-0086/package.py waits exactSUCCESS/checksum/same0085 config into
0086; no auto deployment. Current0085 stays log-only with known phantom
idle corners. First physical center coordinate proven0084; need0153 to
verify true lift/motion before HID. Single43981 capture ends~21:20UTC.

## 2026-11-17: BOOT0085 raw idle packet explains phantom corners

0085 BOOT-only flash100percent/success/reboot20:49UTC; single43981 capture
boot0085-usb-initial.log1800s. UTC sync1794948632=20:50:32UTC; privatefw
restaged79104/79104 valid0; load0/readyA55A/config/report same as0084.
Explicit log-only contacts2478 with per-sample enter/read/exit shows all three
raw packets0000FF followed by57zero bytes. Whole-packet-zero rejection does
not catch this status-bearing zero-count idle packet. Current0152 therefore
still produces tenzero corners; no HID poll sent. This measures an actual
idle packet, not transport failure or absent firmware. Physical center332,805
previously proven on0084 remains valid evidence.

0153 treats packet count0 as no contacts, copying state but ignoring zero
slot payload. Positive counts still inspect all ten sparse slots, including
valid0,0 points. Actual decoder/contact-state/poll C/C++ ASan/UBSan tests
PASS with measured idle packet and held->idle release; exact kernel C compile
PASS; reverse/plain patch+header equality PASS. Staged for next fullCI; no
runtime fix yet. Need motion/lift/HID/UI validation before declaring touch.

## 2026-11-17: FIRST aligned physical finger coordinate confirmed

On0084 user explicitly holds one finger near center and reports ready.
Immediately triggered log-only contacts2483 at20:47UTC returns300samples,
slot0 at332,805; no other contacts; final bounded release, result0/exit/restored.
This is the first aligned physical contact-coordinate evidence. Session-end
up is synthetic cleanup, not yet a measured physical lift transition.
After asking release, contacts2484 again yields ten(0,0) slots; idle/empty
report handling remains wrong in0149. No HID poll sent on0084.

0152 fullCI44169153500 SUCCESS exactddf412948a9d8c4345c6c66abf4d62268c6f8ba2.
Kernel8b82e60575b1f61350a9ba1ac5a39aa0a487127054e6ca25f7589d3896d87f47.
BOOT2fb6c42ef823c0e6a0bd0923b7945f33a2b566e01d1c148060c682a0c1041a1c.
Package same0084 config/checksums/rawpacket marker verified. SyncedDownload
requested20:48UTC for BOOT-only0085 trial. Next restage/load and rawreport
idle/finger comparison before HID.0084 stableGUI/UTC+physicalcoord kept.

## 2026-11-17: BOOT0084 console ownership physically FIXED

User confirms iOS picture stays visible and boot logs no longer overwrite
it on0084.0151 panel drawing gate now has physical evidence in addition to
full Xcode success; USB log stream remains live. User also replies done to
finger touch/drag/lift test. Two earlier bounded captures both produced only
ten(0,0) slots and releases; exact overlap with user's15s interval is not
measured. No convincing physical coordinate change captured and no HID poll
sent. Keep evidence distinct: stable visible GUI+UTC sync+running firmware
are established, physical digitizer input is not.

## 2026-11-17: empty-report safeguard full CI underway

0152 exact kernel C compile PASS. Full CI44169153500 exactddf412948a9d8c4345c6c66abf4d62268c6f8ba2
dispatched20:25UTC macos15intel/a03/SWEET/userspace true. Package-only48253
/tmp/a03-0085/package.py gates SUCCESS/checksums/packet marker/same0084
config into0085. No auto deployment.0084 no HID poll sent; raw contact
baseline must be resolved before forwarding any real input. UTC continues
advancing and SpringBoard logs now2026-11-17 12:24:47, consistent UTC-8
presentation (timezone identifier still not measured). No physical screen/
finger-test reply yet. Preserve0082 running-firmware/home checkpoint.

## 2026-11-17: BOOT0084 UTC works; first contact samples invalid

BOOT0084 flash success/reboot20:20UTC; single4287 capture waits180/1800s,
boot0084-usb-initial.log. UTC sync result1794946865=2026-11-17 20:21:05UTC;
later status1794947086=20:24:46UTC confirms advancing calendar. Display local
hour/timezone and GUI console-handoff physical result pending question.

Private79104byte candidate reupload valid0; explicit load result0/readyA55A,
config20002AD4/1028/report20011580/60/720x1600/18x32. Two explicit log-only
contacts sessions2478/2479 each return300valid reads but produce ten slots
at(0,0) followed by final releases, no movement. These are NOT accepted as
physical contacts. No touch poll/HID delivery sent. User finger-test question
pending; overlapping actual finger movement not yet confirmed.

0152 rejects wholly zero packets before contact decoder (retains genuine0,0
inside nonzero report), aborts after3bad samples, cycles diagnostic enter/
read/exit each frame like stock ReadRegMulti, logs first3raw packets. Prior
0149 held diagnostic mode across all samples. Actual C/C++ ASan/UBSan tests
includingzero refusal PASS; reverse/plain equality PASS; exact kernel C compile PASS. No reset/scan-enable added without evidence.

## 2026-11-17: poll/UTC/console full Xcode SUCCESS; BOOT0084 trial

CI44165152625 SUCCESS exactd6800e414746e684fa67088a7e9d8f1baf4b3716,
macos15intel, patches0149+0150+0151. Full framebuffer C++ now built with
Xcode; local Apple allocation builtin limitation did not prevent CI.
Kernel SHA256f92711eccf17d614b1bf9b41c990a9cbaf455b8252c55d16154397ae10a49e27.
BOOT SHA25679ef85714da5699d9f69f8828d1edb11232d955bcf32ffe8c5f7d65ab2986fb4.
Package gate verifies checksum/markers/same0082 ADT/1GiB/bootargs/root/
loader(except image_size)/stockramdisk/DT. Earlier44162912240 still builds;
0083 not deployed. Synced CDC Download+Samsung/Heimdall detected20:19UTC.
BOOT-only flash49731 underway. Touch RAM firmware will need restaging after
reboot. Next UTC sync/readback then firmware load/contacts log-only, then
HID physical test. GUI console ownership fix needs physical validation.

## 2026-11-17: console handoff full CI dispatched separately

0151 now staged. Full CI44165152625 exactd6800e414746e684fa67088a7e9d8f1baf4b3716
on macos15intel (separate concurrency pool) includes0149poll+0150UTC+0151
panel gate; does not cancel current44162912240 macos26intel. Package-only
63708 /tmp/a03-0084/package.py waits exact success/checksums then same0082
config as0084. No auto flash. Existing0083 watcher68041 remains for earlier
poll/UTC build. Prefer first verified artifact for contact trial; console fix
may require0084 afterward. Current0082 remains running firmwareA55A/home
reported with intermittent boot-log overlay; physical contacts still untested.

## 2026-11-17: user corrects display report; console overwrite identified

User clarifies SpringBoard picture appears every few seconds, then boot logs
overwrite it; subsequently app icons are visible again after explicit Home.
This is intermittent panel ownership, not a steady clean lock/home display.
0082 touch RAM firmware remains ready/config valid; physical touch untested.

Source identifies framebuffer serial fallback fbcon_transmit_data both spools
USB bytes and draws glyphs directly into shared panel RAM. GUI swaps overwrite
those glyphs temporarily. Existing sweetfb_noconsole path switches to the same
serial fallback and is not a proven fix.0151 prepares a separate drawing gate:
append USB byte first, then return when quiet; call quiet only before copying
validated GUI layer pixels. Early boot logs remain visible, subsequent USB
logs remain captured. No display reset or syscall behavior change.

Actual gate ASan/UBSan spool-only/idempotence tests and exact pe_serial C
compile PASS. Patch reverse/plain equality PASS. Full framebuffer C++ local
compile blocked by known unsupported Apple typed-allocation builtins in
headers; no host substitution used. Full Xcode CI required.0151 NOT staged;
ongoing44162912240 includes0149+0150 only, no console-handoff fix yet.

## 2026-11-17: BOOT0082 event loop and physical clock confirmed

Sample2482/cache36D60000 resolves main thread CFRunLoopRunSpecific,
GSEventRunModal, UIApplicationMain and SBSystemAppMain at19:59UTC. User then
physically confirms clock/lock screen. This now confirms visible UI after
successful RAM-firmware load; it does not confirm physical contact input.
One explicit USB Home sent after confirmation; physical response pending.
0149+0150CI44162912240 remains building. Single23880 capture continues.

## 2026-11-17: epoch date measured in SpringBoard logs

At19:57UTC current0082 SpringBoard logs report1969-12-31 16:06:24, consistent
with Unix-epoch wall time and UTC-8 local presentation. This supports the
zero platform UTC source as cause of wrong date; exact timezone identifier
not measured. Later sample2481 main thread progresses into FontServices/
CoreGraphics glyph rendering (cache36D60000), rather than same earlier
MobileGestalt semaphore. Startup continues; visible clock/home not yet
confirmed for0082. Repeated sections2480 still readyA55A/config720x1600,
18x32 after SPI restoration. No contact polling or input sent.

## 2026-11-17: BOOT0082 physical display still boot output

After successful controller RAM startup the user reports brief Apple logo,
then log output overwriting it. This is not a visible clock/home confirmation.
Fresh ps2478 shows SpringBoard25/backboardd56; sample2479 at19:54UTC shows
SpringBoard main thread semaphore wait through libdispatch/libMobileGestalt
(cache slide36D60000). Not yet measured at application main event loop.
No Home/swipe event sent on0082. Continue startup observation; firmware
load result0/readyA55A/config proof remains separate from display progress.

## 2026-11-17: BOOT0082 temporary touch RAM firmware RUNNING

At19:52UTC baseline touch sections: ROM9383 PASS, ready2317/not-ready,
exit0 and SPI gate0A02DE00/clock0 restored. Private CPT79104byte candidate
SHA2568ba14e32cdeacd6763a9700fd5340f9c91763afc2965231148f72f9c1ceea82d
then staged sequentially over EP0: all bytes acknowledged, fwstatus2476
79104/79104 valid0. No bytes stored to phone filesystem or tracked in git.

Explicit touch load2477 at19:53UTC returns0: all seven hardware RAM CRCs
passed before MCU startup. Subsequent section readyA55A, config20002AD4/1028,
report20011580/60, config720x1600 sensors18/32. Exit0 and original gate/source
restored; workerEND. This is actual firmware execution/config evidence, not
physical contact or HID UI proof. Revision8 candidate now runs on this ROM/
panel path; full compatibility remains unverified. No external flash/pinmux/
display reset used. BOOT0082 still lacks polling and UTC command.

0149+0150 CI44162912240 exactda42e57 remains building. Single23880 capture
boot0082-usb-initial.log1800s. Physical current-screen question sent19:54UTC;
await reply. Next0083 verified BOOT trial then restage/load (volatile) and
explicit log-only contact session before HID input; correct UTC separately.

## 2026-11-17: BOOT0082 flash success; poll/time full CI queued

BOOT0082 upload100percent/success/reboot verified19:50UTC. Single capture
23880 waits180 then1800s into boot0082-usb-initial.log. No other reader.
USB not enumerated yet19:51UTC; no ROM/load command sent after this boot.

0149+0150 full CI44162912240 exactda42e57da7ee15ec8722ae8b40a2882f1b5d896b
started19:50UTC, SWEET/a03/userspace true/macOS26intel/no buildtree upload.
Package-only68041 /tmp/a03-0083/package.py waits exact SUCCESS/checksums,
then preserves0082 payload config in0083. No auto deployment. Current0082
has explicit firmware loader, not poll/time. Physical touch/date correction
still pending hardware validation.

## 2026-11-17: RAM-loader full CI success and0082 deployment

CI44159557034 SUCCESS exactcdafbe19909f1b4b99a1523d57c5dd48957dc24a.
Kernel48e9d057d4d1c1c7e1e9edf1dc059a66e859f045a861cf07db569bcfed3d95e7.
BOOT1d03409238596e1c6f0de830365cfbe12fa02f70e0cba3e0112a7cd1732afce1.
Package gate verifies exact0081 ADT/1GiB/bootargs/root/loader(except image
size)/stockramdisk/DT. Synced CDC Download requested19:49UTC; enumeration
required several seconds before Heimdall detect. BOOT-only flash in progress.
No firmware uploaded yet.0080 home+ROM checkpoint remains available.

0149 bounded contact poll and0150 volatile time sync now staged for the next
full build.0082 itself contains0148 only; time/HID polling not present there.

## 2026-11-17: incorrect displayed date reported; UTC sync prepared

User reports4:19 and December31, unlike actual2026-11-17. Source inspection:
SweetPlatformExpert does not override getGMTTimeOfDay/getUTCTimeOfDay; base
IOPlatformExpert::getGMTTimeOfDay returns0, setGMTTimeOfDay is empty. This
explains missing hardware wall-clock initialization; exact displayed year,
userspace adjustments and timezone are not measured. No time readback exists
in current0081.

0150 prepares explicit time status or time UNIX_UTC_SECONDS in the opted-in
USB worker. Uses XNU calendar setter,2020..2099 range, no automatic setting,
no PMIC/RTC write or hardcoded current date. Host sender supplies current UTC
and verifies matching worker acknowledgement/readback. Volatile only; reboot
persistence/timezone/UI refresh remain unproven. Actual parser/calendar-call
ASan/UBSan tests, exact kernel C compile and reverse/plain equality PASS.
Not yet staged/built/deployed; current phone clock unchanged.0148 loader CI
44159557034 still builds19:48UTC; no firmware upload yet.

## 2026-11-17: bounded poll yields between samples

0149's bus-delay callback now uses IOSleep for whole milliseconds and
IODelay only for submillisecond remainder. This keeps300*16ms explicit poll
waits off a continuous CPU busy loop; microsecond FIFO timeout behavior is
preserved. Actual callback delay-split/dispatch ASan/UBSan tests, exact kernel
C compile and reverse/plain application equality PASS. Private candidate's
config move20002AD4 beginsD00240061220, confirming the offline720x1600/
18x32 gate values; this is not runtime compatibility or running-firmware proof.
0148CI44159557034 still building19:43UTC. Fresh0081 io ready1/poisoned0.

## 2026-11-17: BOOT0081 clock confirmed; bounded poll0149 prepared

User physically confirms clock/lock screen after latest0081 reboot. No Home
or synthetic swipe sent in this followup. Old84861 reader ended; single
23025 now captures boot0081-touch-followup.log1500s from19:36UTC.

0149 adds explicit touch contacts (log-only) and touch poll (existing HID
callback) for max300frames/16ms with ROM9383/readyA55A/exact720x1600/18x32
gates. Config must be DRAM, report exactly60bytes in ERAM. No auto polling.
Three bad samples stop and release; normal completion releases held slots.
Actual callback isolation/down/up/coordinates/log-cap tests ASan/UBSan PASS;
actual helper C/C++ ASan/UBSan PASS including PRAM config rejection. Exact
full kernel C compile PASS; reverse/plain patch+source/header equality PASS.
0149 remains OUT of build profile pending0148 RAM-loader hardware evidence.
CI44159557034 exactcdafbe1 still building19:37UTC; package91490 waits. No
firmware upload or controller RAM load yet. Physical contacts unverified.

## 2026-11-17: bounded contact poll preparation

Standalone unstaged poll helper gates on ROM9383, ready A55A, validated
section ranges, exact720x1600/18x32 config, then at most300frames/16ms each.
No automatic thread/timer. Consecutive3bad reads stop session; final cleanup
releases held contacts and exits. Actual C/C++ ASan/UBSan ROM/ready/config/
frame-cap/failure/no-press/release/exit tests PASS. Firmware must be running
first; no physical reports or HID dispatch wired yet. This does not enable
polling on current0081, whose ERAM ready marker is absent.

## 2026-11-17: explicit RAM-only loader0148 prepared

0081 ERAM not-ready motivates stock HostWritePram implementation.0148 stages
private firmware in bounded80KiB kernel RAM via sequential32byte EP0 hex
chunks; fwstatus validates all moves/CRCs. Separate touch load explicitly
revalidates complete image+ROM9383, disables RTC/scan, clears ready/stops MCU,
writes whitelisted PRAM/DRAM, runs RAM-only DMA command3 and checks each
hardware CRC (little-endian), then resets/starts MCU only after all pass.
No external-flash erase/program command or generic peripheral write allowed.
Failure after stop attempts to keep MCU stopped; always attempts exit and
SPI control/clock restoration. Not a display reset/pinmux operation.

Actual loader C/C++ ASan/UBSan complete-image/ROM gates, sequence, HW CRC,
RAM failure/no-start and50ms busy bound PASS. Actual upload-parser ASan/UBSan
size/offset/hex/atomic-rejection tests PASS. Exact full kernel C compile PASS;
reverse/plain patch application equality PASS. Host upload sender validates
private file and waits worker ack/END per chunk; it never sends load itself.
Full CI44159557034 dispatched exactcdafbe1 at19:31UTC; package-only watcher
91490 waits success/checksum/same0081 config0082. No deployment scheduled.
No firmware embedded/tracked or uploaded yet; rev8 candidate panel/rev5 match
still unverified. Full Xcode CI and explicit temporary RAM trial pending.

## 2026-11-17: BOOT0081 ROM good; ERAM not firmware-ready

Explicit touch sections1 on0081 returns ROM9383/result0, then160byte ERAM
snapshot ready2317 (expected A55A). Section/config dereference refused,
backdoor exit0, original gate0A02DE00/clock0 restored and workerEND. This
shows a successful bounded read without the required firmware-ready marker,
not proof every RAM byte is reliable or why firmware is absent. Stock
JD_ZERO_FLASH path now relevant; no RAM firmware uploaded so far. Current
boot still starting UI; no physical display observation yet for0081.

## 2026-11-17: BOOT0081 read-only section trial flashed

0147 CI44154963110 SUCCESS exact7972a72ff7122185158e973762eeab7a76c237af.
Kernel SHA25671d6e2cecc9304509ed995a48c6956a99f74484fce94419034e22d97a5a827e4.
BOOT SHA2564e5fbb3a4f6bc544c6ab4cb3a5665f92b58473ae31241ba43b15dec494173caa.
Exact0080 ADT/1GiB/bootargs/root/loader(except image_size)/stockramdisk/DT
verified. No firmware embedded or new bootarg. Synced CDC Download; first
immediate detect preceded enumeration, later Samsung+Heimdall detected.
BOOT-only upload100percent/success/reboot~19:26UTC. Current capture84861
waits180USB then480s boot0081-usb-initial.log. Explicit sections command not
yet sent; runtime readiness/contact state unknown.0080 home/ROM restore kept.

## 2026-11-17: pre-write firmware validation prepared

Standalone unstaged C firmware parser validates the entire image before any
future device write:80KiB limit, stock12byte moves, source bounds, command0,
PRAM/DRAM whitelist, nonoverlap and CRC16 on every section. Output unchanged
on rejection. Actual C/C++ ASan/UBSan synthetic corruption/truncation/range/
overlap/unknown-command tests PASS; private79104byte candidate validates7
moves using same C code. Compatibility remains unverified. No firmware data
tracked/embedded, no loader/control sequence enabled or hardware upload.

## 2026-11-17: RAM-only transport preparation

Added unstaged jd9365t-memory.h for later validated RAM firmware/report access.
Writes limited to PRAM00000000..0000FFFF or DRAM20000000..2000FFFF;
read-only ERAM20011000..20011FFF additionally allowed. Whole range checked
before first transfer; no MMIO/peripheral/external-flash write accepted.
Uses verified0146 backdoor protocol,240byte chunks with same-CS6byte header;
returns first transport error, existing SPI timeout/CS cleanup retained.
Actual-helper C/C++ ASan/UBSan chunk/header/address/data/CS/bounds/peripheral-
refusal/timeout tests PASS. No firmware or control session staged/enabled;
this does not prove RAM transfer or contact operation on hardware.

## 2026-11-17: BOOT0080 home icons confirmed after paired Home

At19:14UTC user answers yes, app icons visible after explicit USB Home9.
Worker logged Menu40 down/up with1client/result0. This repeats0079 button/UI
result on0080 after the ROM9383 diagnostic. Confirms recovered visible home
and positive Home input; physical digitizer/contact/HID touch still pending.

## 2026-11-17: BOOT0080 clock confirmed; contact failure policy prepared

User confirms physical iOS clock/lock screen after0080 reboot and successful
ROM probe. Sent one explicit paired USB Home at19:13UTC; physical response
pending. No physical touch or unlocked home claim yet for0080.
Prepared standalone unstaged contact-state adapter: fixed-slot down/move/up,
duplicate suppression; failed/malformed reads never synthesize coordinates,
three consecutive failed samples release held contacts once; valid reports
reset failure count. Threshold is explicit preparatory policy, not measured
controller tolerance. Actual-header C11/C++17 ASan/UBSan sparse/move/release/
bounds/malformed/quarantine/recovery/multi-contact tests PASS. No automatic
polling, timers, HID or bus wiring.0147CI44154963110 remains running.

## 2026-11-17: explicit read-only section session0147 prepared

After hardware ROM9383 proof, added touch sections command to inspect fixed
ERAM20011000/160bytes and conservatively validated firmware-config pointer.
Requires another successful ROM9383 before entering read-only section session.
No firmware loading, reset, pinmux or contact dispatch. Failed reads, invalid
ready/table/lengths, out-of-range DRAM/ERAM entries skip config dereference;
always attempts backdoor exit and restores0146 controller/clocks.
Actual extracted session ASan/UBSan tests PASS for wire addresses, successful
720x1600/18x32 config, entry/read failure, not-ready and refused range cleanup.
Full CI44154963110 dispatched exact7972a72 at19:06UTC; hardware section
read requires that full build and a separately verified BOOT0081.
Exact CI-command full usb_console kernel C compile PASS; reverse/plain patch
application/full source+header equality PASS. Staged0147; full CI pending.

## 2026-11-17: BOOT0080 startup after ROM probe

User physically reports Apple logo/still booting at19:07UTC. Same
SpringBoard25 progresses from objc/dyld mapping to CoreUI asset loading,
then by19:09UTC main sample resolves GSEventRunModal/UIApplication _run/
UIApplicationMain/SBSystemAppMain using captured shared-cache slide1F994000.
Both HID user clients opened; earlier post-ROM io ready1/poisoned0. No
software Home/swipe after reboot; physical current screen confirmation is
pending separately. Event-loop sample alone is not rendered UI/touch proof.
0147 CI44154963110 exact7972a72 running; package-only watcher63480 waits
success/checksum/markers then same0080 config0081, no automatic deployment.

## 2026-11-17: BOOT0080 hardware Jadard ROM9383 confirmed

At19:03UTC exact A03XNUConsole01 returned. Both HID providers registered,
probe worker enabled. Explicit touch status1 reports gate0A02DE00/clock0.
Explicit touch rom2 returns result0 id9383 expected9383 raw0000008A/
sts2000000AA; restored gate0A02DE00/clock0, workerEND. This is fresh XNU
SPI3/CS0/1MHz protocol and controller ROM identity evidence. No reset,
pinmux, GPIO, firmware upload or external-flash operation was performed.
Does NOT prove inherited touch firmware, contact reports or physical input.
Next explicit bounded ERAM ready/section/config read, then matching RAM
firmware only if required. Initial capture2205 remains single reader.

## 2026-11-17: BOOT0080 explicit touch-ROM probe flashed

0146 CI44150337660 SUCCESS exact542f9b5ca51dfda442875485ca1ab319e1863abb.
Checksum-verified kernel5828529da29b5a3f2bfbeba253f2ed42d67f9b99e7ccd86b3a38be1d5b7c88e3.
BOOT0080 SHA25635ca7403585d7a6b28f404dc6a0965bc7f55db4596a4e0e3a5ffeea323dbc5f9.
Exact0079 ADT/1GiB/bootargs/root/loader(except image_size)/stockramdisk/DT
verified. No firmware embedded and no new bootarg; touch status|rom explicit.
Synced CDC Download->Samsung detected->Heimdall --boot only upload100percent/
success/reboot~19:02UTC.0079home and0078clock restore images retained.
Single boot0080-usb-initial.log capture waitsUSB180s then480s. No ROM command
yet; runtime boot/ROM and physical display observations pending separately.

## 2026-11-17: source-guided section decoder prepared

Added standalone unstaged ERAM section decoder using actual stock offsets:
ready LE A55A, DSRAM firmware-config entry3 at+28, ESRAM coordinate entry2
at+152 (complete snapshot160bytes). Enforces successful caller read/ready,
nonzero nonwrapping entries, minimum6byte config and exact60byte report.
Leaves prior output intact on invalid snapshots; does not infer undocumented
count widths, controller RAM whitelist, freshness or power state. C11/C++17
actual-header ASan/UBSan malformed-length/endian/wrap/retention tests PASS.
No bus integration or new firmware operation; next gate remains0146 full CI
44150337660/package0080/status+ROM. Fresh0079 health: input status3,
SpringBoard25/backboardd56 alive, ready1/poisoned0. Ancillary daemon crashes
continue; this bounded health check does not establish a fully stable OS.

## 2026-11-17: offline CPT firmware candidate recovered

0146 full Xcode CI44150337660 is building exact542f9b5. Preserved running
BOOT0079 home menu; no reset, ROM read or new phone write at this milestone.
Privately streamed local Samsung A035GXXS8CYG1 AP/super image, converted sparse
and extracted vendor read-only. CPT_Jadard_firmware.bin is79104bytes, SHA256
8ba14e32cdeacd6763a9700fd5340f9c91763afc2965231148f72f9c1ceea82d.
Stock move-table parsing finds7sections; all software CRC16/8005/FFFF values
match. First PRAM section target0 lengthDC2A CRC E911; six PSRAM sections at
20002000..20002ED8 have valid zero CRC residues. Source firmware revision8
is NOT matched to installed revision5; CRC validity is not compatibility.
Nothing uploaded to touch controller. Private images/source/inspection remain
ignored research/a03-touch-firmware. Added offline inspector plus synthetic
CRC/bounds/corruption/wrap tests; no Apple/Samsung binaries tracked.

## 2026-11-17: explicit SPI3/Jadard ROM probe prepared

Continuing physical-touch goal from confirmed0079 home menu. Added0146
explicit worker commands touch status/read-only clock snapshot and touch rom/
bounded SPI ROM-ID session. No automatic probe, controller reset, GPIO/pinmux,
firmware upload or external-flash operation. SPI3 gate20000000bit8, clock
20010058 mux0/ext26MHz/div1, local SPI divider12 =>1MHz. Saved clock/control
registers restored; busy controller refused; polling bounded10ms per wait.
Stock spi-sprd set_cs selects hardwareCS0 even though DT Jadard node logical
CS1; implementation follows actual driver. Enter/read40008076/exit diagnostic
protocol expects little-endian9383. Preserve inherited reset/pinmux for first
ROM test; timeout is not evidence of absent hardware.

Actual shared SPI helper ASan/UBSan wire/CS/chunk/bounds/timeout cleanup PASS.
Actual0146 probe fake-MMIO ASan/UBSan exact-command/read-only-status/control-
restore/mapfailure/busy/timeout PASS (host-only dsb stand-in). Exact CI-command
full a03_usb_console.c and sweet_amfi.c local kernel C compiles PASS. Reverse/
plain apply and helper source equality PASS; existing report/HID/action tests
PASS. Staged0146 for full Xcode CI; no new flash or hardware ROM read yet.

## 2026-11-17: BOOT0079 physical home menu after explicit USB Home

User reports SpringBoard visible and physical finger swipe has no effect.
This is expected with no physical Jadard/SPI driver wired to HID. Started
single180s capture boot0079-input-ready.log/session33166 after original
capture ended; input status3. Sent one USB swipe while UI physically visible:
worker22 down360,1560/up360,460/result0/END. User explicitly reports no visible
reaction, so digitizer queue consumption/UI touch acceptance still unverified.

Then sent one paired80ms USB Home event. Worker23 logs consumer Menu0x40
down/up, one client, result0/END. User immediately reports "now it went to
the home menu" (~18:23UTC). This is the first physical home-menu report and
positive UI response following explicit software input. It supports the
button delivery path, not digitizer delivery or physical touch support. No
passcode handling, persistent unlock or usable application interaction claim.

Preserve running0079 as home-menu checkpoint,0078 as clock restore. No new
flash/reset/root changes this turn. Next hardware work remains Jadard SPI3
ROM/clock/GPIO, private matching CPT RAM firmware and section discovery,
then actual contact reports into HID. USB swipe failure could also reflect
UI gesture policy on this Home-button profile; do not infer a queue ABI bug
from no visual response alone.

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

At18:16UTC both SweetHIDTouch and SweetHIDButtons open by
IOHIDEventServiceUserClient ->1, with backboardd56 progressing8threads.
Sent ONE explicit input swipeup after those opens: down360,1560 then
up360,460, result0, workerEND. This proves sequence dispatch only; queue
consumption/visible UI reaction/unlock still require evidence. SpringBoard25
last sample still1thread/startup, so gesture may precede UI readiness.
Asked user for current screen and swipe response. No repeated gestures.

User reports still booting/Apple logo after the early gesture: no visible
input result established. Continued read-only samples show SpringBoard25
progressing1to14threads through Siri/CoverSheet initialization, then by
18:19UTC GSEventRunModal/UIApplication _run/UIApplicationMain/SBSystemAppMain
(matching cache slide09450000). Framebuffer swaps reach19; storage ready1/
poisoned0. This restores application-event-loop evidence for0079, not a
physical clock claim. Asked user to confirm current screen before another
gesture. No reset or further gesture.

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
