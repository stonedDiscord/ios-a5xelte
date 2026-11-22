## Latest ringtone result

The user still hears only hiss when tapping a ringtone. The hiss confirms
the external amplifier enable sequence runs. BOOT0179's instrumented
capture contains no HakiosAudio HAL messages or PCM write counters during
the preview. The audio root builder places HakiosAudio.driver and
VirtualAudio.plugin together under /Library/Audio/Plug-Ins/HAL, so the
remaining failure is before the plugin's PCM write path. No storage or
partition changes were made.

## BOOT0179 HAL instrumentation result

CI 45072149425 passed after fixing the HAL ioctl handler's user-address
conversion. BOOT0179 was packaged and flashed to BOOT only. Its image SHA256
is 29693f9e71c26baa00b6074d503ca64a1380995c2557e8e2992c0a6870e9fa52.

The kernel now accepts the plugin diagnostic ioctl and logs HAL messages,
PCM write-call counts and PCM byte counts. The BOOT0179 Settings ringtone
capture still contains no HAL or PCM markers, although mediaserverd and
SpringBoard are alive. Therefore this preview did not reach the plugin
write path. Earlier BOOT0174 data remains the strongest evidence that one
capture submitted 34,528 nonzero-capable frames through the kernel and
activated the amplifier, producing hiss without the ringtone.

The DAC0 VBCIF routing correction remains in BOOT0179. Its audible result
is unverified. The installed root and USERDATA remain intact.

## Ringtone samples reach the kernel; DAC source corrected

During a Settings preview, the live PCM diagnostic counted 34,528 frames
submitted to AP01, including 22,823 nonzero frames. The external speaker
amplifier activated, and the user heard hiss that followed the preview.
They still did not hear the ringtone. DSP startup, speaker depop, AP01
teardown and register restoration all completed successfully.

Review of the stock VBC startup structure found the playback scene was
setting the DAC1 selector ID word instead of DAC0's source value. DAC0
therefore remained on the default IIS source while AP01 received samples.
Patch 0246 selects VBCIF for DAC0 and preserves the unused DAC1 IIS route.

Patch 0245 now reloads the bundled touch firmware after a failed stream,
waits two seconds for firmware startup, then starts HID again. It permits
up to five reloads per boot and cancels pending work on explicit stop.
CI 45069031752 builds d70b734. BOOT-only installation and live tests are
pending. Current BOOT0174 touch was manually reloaded and restarted after
the user reported no response; post-reload physical response awaits a
new test.

## BOOT0174 touch stream stopped after transient errors

During the ringtone capture, the automatic HID stream produced 80 contact
transitions across 1216 slices, then returned error -4 with 0 valid frames
and stopped after releasing held contacts. In the poller, -4 means three
consecutive failed or malformed reads. The capture does not distinguish a
SPI transfer failure from an invalid report. Since one valid HID frame had
already set a boot-done flag, the existing boot worker did not restart the
stopped stream.

An explicit USB `touch start` restored streaming. The latest status showed
streaming=1 at 619 slices. CPU display telemetry showed 17,526 completed
swaps and copies. The user is checking physical response after restart.

Patch 0245 schedules up to five automatic restarts per boot, two seconds
after a failed stream, only when bundled firmware remains loaded and HID is
available. Explicit stop cancels a pending restart. CI 45067521789 builds
35647f2. A BOOT-only trial is pending. Cable-free touch over repeated boots
and sustained input remain unverified.

## BOOT0174 external speaker test

CI 45065385204 passed at bafd519. BOOT0174 is an exact verified XNU
kernel packaged with CPU rendering and bundled touch firmware. The
BOOT-only flash succeeded. Image SHA256
281ffb5756c1d5d774305eb32c42be67ff304d359b5869f73b7ac91dd7bfe92e.

The stock SM-A035G device tree assigns the external speaker amplifier
to active-high GPIO40. The stock audio hook pulses it ten times at
2 microseconds per edge and waits 10 milliseconds. Patch 0244 applies
that sequence around playback and restores the GPIO state afterward.
The direct AP01 tone completed with external amp setup reported enabled,
4800 submitted frames, speaker restoration, and DSP shutdown status zero.
The user is checking whether the tone was audible. Settings ringtone
playback remains unresolved.

The latest post-boot probe reports touch HID streaming active at 1014
slices and 0 events. The user previously confirmed touch was back on
BOOT0173. Physical touch on BOOT0174 is not yet reconfirmed. CPU display
telemetry records 39 completed swaps and 35 CPU copies.

## A03 external speaker amplifier

The direct AP01 probe submitted 4800 tone frames and completed teardown.
The user heard no sound. The live DT identifies active-high GPIO40 for
the external speaker amplifier. The stock 4H10 playback hook uses ten
2 microsecond low/high pulses and a 10 millisecond settling interval.
Patch 0244 adds this sequence and restores the pin after playback.
Patch application passed against the verified tree with 0243 applied.
CI 45065385204 builds bafd519 for the BOOT0174 CPU-rendering trial.

## Touch restored and ringtone playback still silent

The user confirmed touch responds after the HID polling restart on the
CPU-rendered BOOT0172 variant. Settings ringtone previews remain silent.
During a live capture the PCM worker started the DSP and AP01 scene,
reached speaker depop 019f, and later restored the speaker and shut down
the scene successfully. The live worker starts only with queued PCM. A separate bounded AP01
speaker probe submitted 4800 tone frames, restored speaker state and shut
down the DSP scene successfully. The user confirmed the direct test tone was silent.

Patch 0243 reports total and nonzero frames submitted per live playback
session. It applies to the verified BOOT0172 tree. CI 45063949773 builds
d803f59. Use the CPU-rendering boot arguments and bundled touch firmware
for the diagnostic image. Cable-free touch across boots remains unverified.

## CPU rendering with automatic touch startup

On BOOT0124 the user saw lock-screen animation but could not reach Home
using physical input. Repacked the verified BOOT0172 kernel from CI
45045874873 with the GPU flag removed and the bundled touch firmware
retained. BOOT-only flash succeeded. Image SHA256 is
2c6213744a7a4a0255a293169d2b4ff529fe3a51d7ed54361dd35bf8debf5d5f.

The controller reached A55A and started HID polling automatically. Before
a manual diagnostic restart, polling reached 868 slices with zero contact
events. Controller ID 9383 and the 720 by 1600 configuration read back.
Polling was restarted. USB Home and swipe-up returned successful dispatch.
Physical touch, hardware buttons, Home Screen access and cable-free
boot acceptance remain unverified on this image.

## 2026-11-22: Apple-logo report and BOOT-only recovery

The user reported that the display remained at the Apple logo. During the
BOOT0172 session, the live console showed mediaserverd, backboardd and
SpringBoard alive. Display telemetry still showed only four completed GPU
copies. A dispatched Home event did not increase that count. The sampled
console contained no CPU panic.

Sent the documented CDC Download reset and flashed the existing BOOT0124
CPU-control image to BOOT only. Its SHA256 is
869f9c901071ba12359a0613e10c63e158e880baa17debc291d8f13ee90e0190.
GPT, USERDATA and the installed audio root were left intact. After reboot,
XNU, mediaserverd, backboardd and SpringBoard were present. Vsync advanced,
while the first display probes showed no swaps. A later probe counted
five CPU-rendered copies with GPU copies at zero. The next sample stayed at
five, so continuous frame progress is not established. A dispatched Home
event returned success. The user later confirmed the iOS lock screen.
A follow-up probe counted 28 CPU copies and 33 completed swaps.

Current BOOT is 0124 CPU-control. Audio playback remains unverified. The
installed p55 root still contains the audio-enabled image.

## BOOT0172 and installed audio root

Audio root CI 45049709675 passed. The 16 GiB HFSX image has SHA256
594d22a1d0a34a985eff9a7cc529b498fadc4142de91ab9c3d39061ca65bb9ff.
Offline catalog inspection found HakiosAudio.driver and VirtualAudio.plugin
under /Library/Audio/Plug-Ins/HAL. The installer reported a full direct-readback
SHA256 match on GPT-validated USERDATA p55. BOOT0172 was restored afterward.

The live USB process probe completed with mediaserverd (PID 28) and
SpringBoard (PID 26) present. The next capture shows mediaserverd
issuing the HakiosAudio diagnostic ioctl on fd 3, which returned ENODEV.
The A03 PCM device uses eno_ioctl. This strongly indicates the HAL
plug-in ran and obtained a descriptor. PCM writes remain unverified.
The earlier kernel speaker probe reported depop 019f,
submitted 4800 frames with DMA, restored speaker state and completed DSP
shutdown with status zero. Settings playback awaits physical confirmation.

### Earlier audio trials

Offline catalog inspection of root artifact 45044428311 confirmed
VirtualAudio.plugin under /Library/Audio/Plug-Ins/HAL and
HakiosAudio.driver under /System/Library/Audio/Plug-Ins/HAL. This
establishes placement only. Runtime discovery from either directory
remains unverified. Replacement run 45049709675 stages HakiosAudio
beside VirtualAudio. Session 98526 downloads and verifies that image.
Session 2563 checks both bundles in its offline HFSX catalog. The USB
reader still exposes p55, and the host ACL remains outstanding.

Replacement audio-enabled root CI 45049709675 builds 917cfac.
The handset remains in the p55 USB reader while host write access
and the replacement image are pending. Settings playback is unverified.

The first audio-root build placed HakiosAudio in System/Library while
the staged VirtualAudio plug-in lives in Library/Audio/Plug-Ins/HAL.
Do not install artifact 45044428311. Commit 03164c6 records that
unverified placement. Commit 9ce5e79 corrects the builder to stage
HakiosAudio beside VirtualAudio. A replacement audio-root build is
running from this source. The existing writable-reader ACL request
remains pending.

BOOT0172 passed CI 45045874873 and BOOT-only install. It registered
/dev/hakios-audio. The separate hardware probe reported depop ready,
submitted 4800 frames and completed teardown. Acoustic output and
normal Settings playback remain unverified.

Audio root CI 45044428311 passed HFSX verification and the downloaded
16 GiB image matches the artifact SHA256. Keep HakiosAudio in the
System HAL directory specified by its driver source and VirtualAudio
in the Library HAL directory. The phone is running the temporary Linux
reader exposing validated p55 via A03LinuxInstallV11 LUN1. Host access
to that LUN requires the scoped ACL requested from the user. The
audio root image has yet to be written.

BOOT0171 passed CI 45044136063 and BOOT-only install. SC2730 depop
reported 019f and ready=1, AP01 submitted 4800 frames with DMA bits 3,
and speaker restoration and DSP shutdown passed. Acoustic output
remains unverified. Patch 0242 adds the opt-in /dev/hakios-audio
PCM device and feeds the verified route from its queue. BOOT0172 CI
45045874873 builds b0b9189. Session 10666 verifies and installs the
image with a03pcm=1 in place of the verbose kprintf flag. The installed
root still needs the HAL bundle and VirtualAudio routing enabled.

Audio-enabled HFSX root CI 45044428311 uses the new speaker_audio
input at 9f91836. It builds the HAL and stages it with VirtualAudio.
This is an image build only. Keep the current USERDATA filesystem for
in-place deployment. BOOT0171 and the kernel PCM sink remain pending.

BOOT0170 CI 45043422319 was cancelled by branch concurrency before
installation. The replacement BOOT0171 run is 45044136063 at 4b66e96.
Session 23955 verifies the artifact, installs BOOT and captures the
depop result, PCM submission and teardown. The HAL staging fix has
passed local checks. Installed Settings playback remains silent.

Settings ringtone previews remain silent in the latest user test.
Commit fbafc98 stages HakiosAudio.driver in System/Library/Audio/Plug-Ins/HAL
and keeps VirtualAudio enabled for audio-enabled root builds. Shell and
Python syntax checks and a temporary-root routing check passed. The
installed root still needs the bundle and the kernel PCM device.

BOOT0168 submitted 249 frames and ended with both FIFO full flags set.
BOOT0169 enabled the digital DAC during the same test and submitted
4800 frames with the DMA enable bits clear. DSP shutdown and probe
completion passed. The earlier throughput limit was resolved by the
digital DAC setup in this comparison. CI 45043422319 builds 69ad289
for BOOT0170, which holds the analog route during PCM feed and requires
the SC2730 depop-ready bit before submitting the tone. Session 20957
handles verification, BOOT-only install and capture. The HAL bundle
can be staged in local root builds and is still absent from the phone.

BOOT0167 passed CI 45040645597 and BOOT-only install. AP01 submitted
16 stereo frames, DSP shutdown returned zero and the probe completed.
Patch 0239 keeps the digital DAC enabled during the bounded PCM feed and
restores it before audio clock teardown. The local iOS root builder also
accepts the HakiosAudio.driver bundle for staging. The bundle is still
pending installation on the phone, and Settings previews remain silent.

Patch 0238 queues a quiet 1 kHz PCM waveform through the AP01 FIFO
for up to 100 ms and 4800 frames. Patch-stack application passed.
BOOT0168 CI 45041018579 builds e3ffbf6 on macos-26-intel. Session 5179
verifies the artifact and waits for BOOT0167 to finish using the phone.
This trial measures sustained FIFO submission. Speaker output and
iOS Settings playback still require the complete route.

BOOT0166 passed CI 45039447797 and BOOT-only install. Its DSP, analog
mixer write/readback and restore, and 48 kHz DAC checks completed.
BOOT0167 CI 45040645597 builds 44a8e3d. Session 87974 verifies and
installs the image, then runs the stereo FIFO probe. That probe checks
PCM submission and teardown. Settings still needs the kernel playback
device and HAL plug-in connected to the speaker path.

Patch 0237 submits whole stereo PCM frames through the AP01 FIFO and
checks both channels for space before each frame. Mock MMIO checks
passed for zero, partial and full submission, channel order and sample
bit preservation. Patch application and profile staging passed. Commit
0bd0dff awaits a hardware build after the BOOT0166 mixer trial.

BOOT0165 passed CI 45037358504, artifact verification and BOOT-only
install. DSP boot passed. Analog power read back PMU0=2230 with
restored=1. The digital DAC again returned configured=1 and restored=1.
BOOT0166 CI 45039447797 builds ac5df60 to verify the ADie DAC,
DACS and DACL-to-SPKL mixer fields with the speaker amplifier off.
Session 94668 watches build, install and capture. The iOS PCM sink
and audible Settings playback remain pending.

BOOT0164 passed CI 45036949973 and BOOT-only upload. DSP boot passed.
The digital DAC probe configured stereo at 48 kHz and read back
AUD_TOP_CTL=00000005 and AUD_DAC_CTL=000003f1. It reported configured=1
and restored=1. BOOT0165 tests the analog power and reset sequence.
The latest Settings preview was silent and audible playback remains open.

Settings ringtone previews are still silent per the latest physical test.
BOOT0165 adds SC2730 analog DAC power and reset sequencing in patch 0235.
Local patch application and iOS profile staging passed. CI 45037358504
builds 92f68c7 on macos-26-intel so BOOT0164 can finish independently.
Session 25117 verifies the artifact and waits for the BOOT0164 capture
before attempting the BOOT0165 install. Both builds are in progress.
The iOS PCM device and HAL deployment remain pending.

BOOT0163 passed CI 45035381713, artifact/source verification and BOOT-only
upload. Ping and DSP boot passed. The analog probe returned clock
sequence=1, restored=1 and PMU0=0020. The digital probe returned gate
readback 00990000, AUD_TOP_CTL=00000000 and AUD_DAC_CTL=000083f0, then
completed with wake monitor 0, sleep 6 and power 0. BOOT0164 CI
45036949973 at a676273 adds 48 kHz DAC programming and restoration under
the verified gates. Session 45311 watches build, install and capture.
Audible Settings playback remains pending.

BOOT0163 CI 45035381713 builds fd8d629. Patch 0233 uses the stock
SC2730 AGCP AUD and AUDIF gate bits 19 and 20 and the existing DSP wake
sequence before reading AUD_TOP_CTL and AUD_DAC_CTL at 0x56750000.
Patch application against BOOT0161 and iOS profile staging passed.
Dispatching the new run cancelled BOOT0162 CI under the branch concurrency
setting. Session 22013 verifies and installs BOOT0163 and captures the
analog clock trial from 0232 before the new digital read.

Patch 0232 adds a reversible SC2730 DAC and speaker clock trial using
the vendor ANA_CLK0 and ANA_DCL1 fields. It uses the BOOT0161 ADI
readback and reverse-order restore. Patch application against the
BOOT0161 CI source and full iOS profile staging passed. CI 45035123958
builds d244cc3 for BOOT0162. Session 6004 watches the build, checks the
artifact, installs BOOT and captures the probe. The audio plug-in and
speaker output still need end-to-end verification.

BOOT0161 passed CI 45033595131 and BOOT-only upload. The phone answered
ping, reported A55A and requested HID streaming at startup. DSP boot
returned ready. The SC2730 probe completed with clock sequence=1,
restored=1, PMU0=0020, CDC14=0000 and STS11=0000. The enabled clocks
made PMU0 readable with a nonzero value. Physical cable-free touch and
iOS speaker playback remain unverified.

The user tested several ringtone previews in iOS Settings and heard no
audio. The A03 audio plug-in and PCM device are still pending deployment.

BOOT0160 returned zero for the three SC2730 codec registers and logged
A55A followed by an automatic HID stream request. BOOT0161 CI 45033595131
runs patch 0231 to check those registers with the analog clocks enabled.
The existing watcher verifies the build, installs it and captures the
clock and restore results. Cable-free physical touch and audible iOS
playback remain unverified.

BOOT0159 reproduced stereo FIFO progress and completed AP01 restoration
before DSP shutdown. BOOT0160 CI 45032216438 builds the SC2730 ADI
state probe. Session 98821 handles packaging and capture.

User observed BOOT0158 DSP shutdown return status zero, followed by an
implementation-specific CPU7 panic. The host capture ended before that
reply. This places the observed panic after shutdown and supports testing
0229, which moves AP01 and clock cleanup ahead of shutdown. The exact
faulting instruction remains unknown.

BOOT0158 moved both PCM FIFO pointers, then USB stopped responding during cleanup. Physical Download Mode requested. CI 45030688399 and packaging session 98102 cover the cleanup-order change. Audible playback remains unverified.

BOOT0157 confirmed both AP01 enable bits but FIFO pointers stayed static.
BOOT0158 CI 45029089674 adds DSP playback trigger. Session 1354 handles
packaging, BOOT-only install and capture.

BOOT0156 confirmed AP01 access with the VBC clock gates enabled. Both
disabled FIFO pointers stayed static. BOOT0157 CI 45027442043 and
session 64382 test prefill with both AP01 channels enabled.

BOOT0154 found all three VBC clocks gated after DSP wake. BOOT0155
CI 45025021246 builds 6711f54 and session 60525 tests clock acquisition
and a guarded AP01 read. Audible iOS playback remains unverified.

BOOT0153 verified DSP wake after responsive startup. BOOT0154 CI
45023994730 builds the guarded AUDCP AHB clock read in a49c8c7.
Session 13394 handles packaging, install and capture.

BOOT0150 restored after BOOT0151 audio ap panic. USB ping and touch
autostart markers recovered. CI 45022182506 builds a73a5c1, which removes
VBC aperture reads and the untested FIFO write. BOOT0153 packaging
session 64726 waits for CI. Test wake separately after startup.


BOOT0150 is installed. NORMAL_AP01 startup and shutdown each returned
status zero. CI 45020753150 builds the AP wake and FIFO probe.

Patch 0222 adds the AP wake and FIFO status trial after 0221.
BOOT0149 still answers DSP GET while the AP access gate is closed.

BOOT0150 CI 45019384758 builds 255c2fb with a NORMAL_AP01 VBC startup
and shutdown trial. Session 83751 waits for the verified BOOT image,
then captures both DSP replies. BOOT0149 verified two consecutive GETs.

BOOT0149 is installed. DSP boot and two consecutive VBC GETs passed
with status zero. Next port the stock VBC stream setup and PCM path.


BOOT0148 is installed and returned a successful VBC GET after DSP boot.
Patch 0220 prepares repeatable exchanges for stream setup. Audible iOS
playback and cable-free physical touch remain unverified.

BOOT0147 installed and DSP returned AGDSP_BOOT_OK. Touch started from
bundled firmware and passed 49 validated slices before any host touch-start
command. Cable-free physical test requested. CI 45017041887 builds 0219
for the VBC mailbox test. Speaker playback remains pending.

User confirms recovered BOOT0146 touch and requires untethered touch
on every boot. BOOT0147 install watcher session 18882 waits for the
verified combined build. Check automatic HID streaming and physical
touch after cable-disconnected boots, with no host touch commands.

Patch 0219 prepares one fixed DSP VBC GET over the stock audio mailbox
after DSP-ready validation. Host mock and profile staging passed.
BOOT0147 CI 45015846547 remains the next device trial for DSP startup
and delayed touch autostart. No audible playback verified.

BOOT0146 touch recovered live after explicit reload and restart. HID
streaming is active and validated slice counts advance. Physical input
confirmation is pending. Patch 0218 delays and bounds automatic starts
after firmware load, to address the initial all-FF report failures.
Combined DSP and touch CI 45015846547 supersedes 45015450889.
BOOT0147 packaging session 4747 pins 5025d28 and both patches.

BOOT0146 live XNU DSP sample is deep=1 sleep=0 system=7 dsp=7 access=0.
Patch 0217 adds explicit stock-mode DSP startup with the privately
bundled matching revision-5 AGCP image. Host packaging passes. Next
run `audio boot` and verify the DSP's SMSG ready message. CI 45015450889
builds dbeec15. Private prepare-audio-0147.py waits for its artifact.
BOOT0146 touch firmware reports A55A, but automatic streaming failed
twice at its first slice. Audible iOS playback remains pending.

A03 audio bring-up starts from live BOOT0145. mediaserverd PID 28 is
present. Stock evidence identifies VBC v4, SC2730, AP GPIO 40 speaker PA
and DSP-backed 48 kHz routes. Patch 0216 stages a read-only `audio status`
live-worker command for PMU/AON state. CI 45014207915 builds ed3b966
with the corrected Qogirl6 power-field labels. Private
prepare-audio-0146.py pins the build and validates sources before packing.
The stock SMSG ring and ready message are mapped in A03_PROGRESS.md.
Matching revision-5 AGCP firmware and vendor XML are now extracted
privately. The profile compiler reproduces all four stock size records.
Next capture audio status on BOOT0146 and use it to qualify the DSP
initialization path. Audible iOS playback is pending. See A03_PROGRESS.md.

The bundled touch firmware build is available from CI 44967426084 at
`1af663a`. The preceding run, 44966189758, failed on two `SecureDTEntry`
declarations in patch 0215. Both now use XNU's `DTEntry` type. The A03 USB
probe link check passed and CI uploaded the kernel and build tree. Next
checkpoint is BOOT packaging and an on-device touch auto-load test.

BOOT0144 passed CI44950176996 and BOOT-only installation. SHA-256
a24bde626bf494dcb089ee2fa2b2dc92f39c0da22722cc7209b2bfdd02715a2b.
LaunchServices reopened its persisted cache and CollectionsPoster launched.
PosterBoard PID260 created a two-plane b3a8 snapshot surface and stayed
alive through startup and USB Home wake. Display copies rose from 35 to
9055. The capture showed one PosterBoard launch and no PosterBoard crash
through the 21:32 UTC checkpoint, over nine minutes after launch.
Touch firmware reached A55A and streaming remained active. Physical panel
content, physical touch on this boot, and persistent wallpaper selection
were not independently verified. Reader PID203973/session2896.

The stock IOSurface client reads plane width, height, offset, row bytes
and element size at different offsets from the existing XNU result.
0213 corrects the layout at the kernel serialization boundary. Patch
application and profile staging passed. CI44950176996 builds 220d75a.
Private prepare-posterboard-0144.py uses the original BOOT0142 arguments
so the existing LaunchServices database stays in place during the test.

BOOT0143 reseeding allowed CollectionsPoster to launch and PosterBoard to
create snapshot surfaces. PID861 then trapped in CFRetain from
PBUIImageEncoder saveUIImage:error:. The preceding buildCGImage call
can return NULL. The matching IOSurface cache identifies selector 1 as release.
The BaseBoard builder sends b3a8 and w30r through ImageIO
CGImageCreateFromIOSurface. The specific conversion failure is unresolved.
The earlier -2219 error did not appear in this launch. Selection and
survival through startup and wake remain unverified.

BOOT0143 passed CI44945143677 and the BOOT-only upload. SHA-256
aed4f81d51b4ed79fe19bd445a1f62ca047de70405658fb860c5748071c76546.
Cache archive returned 0 and lsd confirmed ENOENT at the original path.
Live PID98 entered MIFilesystemScanner and validated built-in bundles.
At the latest sample the scan had advanced into MobileGestalt call stacks.
The 192-record lsd path cap was reached during Applications enumeration.
PosterBoard launch and provider registration remain unverified.
Touch streaming restored. Sole reader PID186437/session68219.

BOOT0142 passed CI44943875183 and BOOT-only installation. Touch reached
A55A and streaming was verified. Reader PID177195/session35987 captured
lsd opening an existing LaunchServices csstore and accessing Frameworks.
Patch 0212 archives that exact cache with an exclusive rename behind a
private boot argument, so lsd can attempt a fresh seed. CI44945143677
builds c387071. Private prepare-posterboard-0143.py pins the build and
derives the container identifier from the device log. Reseed is untested.

BOOT0141 reproduces the crash. Patch 0211 traces LaunchServices database
paths and the standard built-in scan directories. Patch application and
profile staging passed. CI44943875183 builds 2314b54. Private
prepare-posterboard-0142.py pins the build.

BOOT0141 follow-up: the stock cache has an in-process built-in scanner
in InstalledContentLibrary. Determine whether the live LaunchServices
database reaches the built-in scan, including framework enumeration,
before changing the installd launch policy.

BOOT0141 passed CI44942293405 and BOOT-only installation. SHA-256
9f499bef61da34cc3e066bf967b545187fdc5d206b8f577034c28350c58316ba.
Fallback persisted across reboot (EEXIST). The capture showed no installd
startup or accesses to either provider bundle before PIDs 233 and 332
returned -2219 and trapped at unslid 0x1be3babac. The stock root lacks
mobile_install, lsregister and launchctl at the inspected paths. Touch
returned to A55A with streaming observed at 774 slices. The live reader
is PID168525/session55680. Provider seeding remains unresolved.

Patch 0210 traces installd startup and scoped wallpaper plug-in directory
access. Patch application and A03 profile staging passed. CI44942293405
job136961940025 builds 6749c00. Private prepare-posterboard-0141.py pins
the build. BOOT0140 remains installed.

BOOT0140: the bundle-unit message occurs after _LSExtensionPointAdd
succeeds. Both providers match the staged launchd cache. Inspect the
separate plug-in seeding path instead of treating the unit-0 message as
proof that extension-point creation failed. Root CI44939625136 passed.

BOOT0140 follow-up: CoreServices has separate extension-point and plug-in
registration paths. The stock installd job and executable are present in
the staged root. Live ps showed lsd and pkd with no installd at that sample.
Inspect MobileInstallation framework metadata and plug-in seeding. The
missing process sample does not establish a launch failure.

BOOT0140 passed CI44939996930 and the BOOT-only upload. Image SHA-256
2cf3c36113835d43536a4ecc889740666c764559402321cebd3b6fb5c9b982a0.
The migration returned 0 and lsd PID97 opened the fallback definition.
LaunchServices then reported “Failed to fetch app bundle unit: 0” for
com.apple.posterkit.provider. PosterBoard PID238 still returned -2219 for
both providers and trapped at unslid 0x1be3babac. The prior “Cannot run query” message disappeared in the captured startup,
but both provider coordinators remain unavailable. Investigate the definition's association with a registered
bundle and provider discovery. Touch firmware reported A55A and streaming
reached 588 slices. Sole reader PID152789/session66754 remains active.

BOOT0140 migration candidate 15ed2cc installs the single PosterKit fallback
on the existing writable HFS root through the validated USERDATA p55 gate.
It publishes the complete file with an exclusive rename. Its definition
matches the stock plist. CI44939996930/job136954881102 is building.
Private prepare-posterboard-0140.py pins the build. BOOT0139 is installed.

ACTIVE root CI44939625136 builds 0f4dc39, which stages the stock PosterKit
extension point for fallback enumeration. BOOT0139 still reproduces the
crash. Validate the fallback on USERDATA p55 and check provider discovery,
wallpaper selection, and PosterBoard survival through startup and wake.

ACTIVE BOOT0139 installed, touch ready and streaming, reader PID145876.
LaunchServices cannot read the signed extension-point cache because it
cannot find AMFI (ExtensionKit code 12). Investigate the signed-cache
validator interface and verify provider discovery and wallpaper selection.

ACTIVE BOOT0138 still installed. Patch 0208 mirrors lsd and pkd startup
logs for provider registration. CI44938311489/job136949746962 builds b18d40e.
Private prepare-posterboard-0139.py pins the build. Restore touch after BOOT test.

BOOT0138 reproduced the provider query failure, -2219 setup errors and
the publisher trap. lsd opened the definition and signature. Staged
plist page hashes match. Trace the runtime query authorization and
registration results to identify where the provider is dropped.

ACTIVE BOOT0138 installed from CI44936228950. Touch firmware ready A55A
and streaming. Sole reader PID138503/session66689. Live lsd opens the stock
extension definition plist and signature. Follow its registration and
PosterBoard's query on this boot.

ACTIVE BOOT0137 confirmed error -2219 is the missing provider coordinator.
The staged HFS contains provider declarations and bundles. 0207/54f6f71
traces live registration paths for PosterBoard, lsd and pkd.
CI44936228950/job136943326829 is building. Private prepare-posterboard-0138.py
pins the run. Restore touch after the next BOOT test.

ACTIVE BOOT0137 confirmed 13 physical swipe events while user saw Apple logo.
USB Home later preceded new frame copies. PosterBoard reproduced the publisher
trap. Stderr captures provider discovery query failures and error -2219 for
both Collections and legacy configuration creation. Trace provider registration
and the -2219 return path. WallpaperKit separately rejects default 7400.

ACTIVE BOOT0137 installed from CI44934190387 at 3613443. Touch firmware
reloaded to A55A and streaming remained active after one restart. Zero
contact events at 690 slices. USB Home dispatch succeeded. Await physical
gesture evidence. Sole console reader PID124506/session43309 writes
boot0137-posterboard-live.log. Follow PosterBoard startup and the first
selection attempt through the stderr and persistent store traces.

ACTIVE BOOT0136 touch restored and capture PID116468/session62917 live.
Temporary wallpaper rename succeeds. Persistent ordering and selected
identifier files remain absent and PosterBoard traps. 0206 enables
PosterBoard startup log mirroring. CI44934190387/job136937140024 active
at 3613443. Private prepare-posterboard-0137.py pins the build.
Restore touch after the next reboot.

ACTIVE BOOT0135 opens all default 7400 metadata and the iPhone defaults.
Temporary wallpaper metadata also opens. Store directories exist, ordering
plist returns ENOENT, and the nil selectedLockPath trap persists. Patch 0205
traces persistent store operations and rename destinations. CI44932481949
job136931918601 active at 2ed4ef0. Private prepare-posterboard-0136.py pins it.
BOOT0135 touch restored. Reader PID110201/session80995. Restore touch on 0136.

ACTIVE0134 running, touch restored/load0/A55A/stream1 after one retry.
SolePID102004/session5401 to~17:42UTC;41PosterBoardcrashes17:37. Stock asset
reads succeed but trace192cap exhausted;0204/d81db2b focuses7400 opens.
CI44930944890/job136927206594 live;prepare-posterboard-0135.py pinned.
CollectionsPoster.appex exists but no launch captured. Need default/provider
selection evidence; preserve touch on every reboot.

ACTIVE user reported touch off; live0133 streaming0 confirmed. Restored
private verified FW/load0/A55A; one start retry ->streaming1/49slices/events0,
HIDstatus3. Sole100198/session91285 boot0133-touch-recovery-live.log~17:33UTC.
Restore touch on EVERY following diagnostic boot. AssetCI44929116933success,
BOOT0134exact-source/hash/SMP ready88193cb6...f98725, NOTflashed; phone0133.

ACTIVE BOOT0133 installed; screen-class migration result0/close0 but PIDs232,
317 still trap selectedLockPath nil.46corpse records17:16UTC; sole reader
PID93564/session44663 to~17:21UTC. Asset evidence0203/ae05b15 compiles ARM64;
CI44929116933/job136921631147 active. prepare-posterboard-0134.py pins it.
Next inspect stock asset reads/app logs on0134. No crash fix claim.

ACTIVE BOOT0132 installed, c30a775/CI44925526385 verified. Identity correction
changes live WallpaperKit lookup from ~ipod ENOENT to ~iphone successful.
PosterBoard still traps selectedLockPath nil;131corpse records/reader ended.
0202/0da7315 adapts stock default7400 metadata screen class to240w-533h@3x~iphone;
asset filenames preserved. Actual-stock host test and ARM64 compile pass.
CI44927553296/job136916888173 queued; prepare-posterboard-0133.py pinned.
Next verify CI, BOOT-only0133, migration result and sustained poster survival.

ACTIVE user reports mixed iPod/iPad identity. Found macOS iOS-on-Mac
hw.machine=iPad8,6 and A03 platform expert product=Samsung Galaxy A03,
target=a03, inconsistent with ADT iPhone10,3/D22AP.0201 c30a775 restores
device-tree identity; actual ARM64 C/C++ checks pass. CombinedCI44925526385
job136910842997 active (earlier44924752182 canceled by workflow concurrency).
prepare-posterboard-0132.py pins combined0200+0201; no flash yet/phone0131.

ACTIVE BOOT0131 focused evidence: catalog opens succeed, but requested
DefaultWallpapers~ipod.plist is ENOENT. Stock ~iphone file has default7400.
fd06be0 adds no-overwrite alias in root staging and a03wallpaper migration;
actual ARM64 C and host tests pass. CI44924752182/job136908295678 queued.
Private prepare-posterboard-0132.py pins it. BOOT0131 still installed,
reader ended;58crashes. Need exactCI->BOOT-only0132->default lookup success,
selected wallpaper and sustained PosterBoard service without restart.

ACTIVE focused trace CI44922279998 failed: unavailable strstr declaration.
Corrected d77a047 uses bounded XNU strnstr; host tests and actual ARM64 C
compile pass. Replacement44923242765/job136903620345 is live; private
prepare-posterboard-0131.py pins it. No failed image flashed. BOOT0130 remains.

ACTIVE PosterBoard: BOOT0130 reproduced the selectedLockPath trap with
catalog alias result=0. Broad trace showed absent legacy lock/home JPEGs
and hit its 192-record limit. 0199 records focused success/error wallpaper
paths; CI44922279998/job136900706788 active at 564d2b5. Staged root CI
44918953514 succeeded. BOOT0130 reader ended; crash goal remains open.

ACTIVE PosterBoard still crashes after successful BOOT0129 catalog alias.
Old invalid-order SIGABRT absent; two live crashes now SIGTRAP BRK #0 in
PBFWallpaperPublisher activation, nil selectedLockPath, unslid 0x1be3babac.
49 corpse-limit records in private boot0129-wallpaper-live.log; reader ended.
Patch 0198 ba9000c adds bounded startup syscall evidence. CI44920479585
job136895209891 active. Package next BOOT with the same arguments and alias,
capture first traced PID and correlate failures. No full fix yet.

ACTIVE PosterBoard cause confirmed on BOOT0128: PIDs 248 and 353 SIGABRT
for missing valid order in /Library/Wallpaper/Collections/Collections.plist.
Stock Collections~iphone.plist in the installed-root source has six entries.
cf226d2 adds the staged alias and opt-in migration for existing USERDATA HFS.
Kernel CI44918953970/job136890549051 and root CI44918953514 running.
BOOT0128 remains installed; verify BOOT0129, then check alias result,
stable PosterBoard PID across active use, and no recurring crash.

ACTIVE PosterBoard crash fix. BOOT0127 baseline: 255 corpse-limit records in
eight seconds; deployed detailed logger omitted PosterBoard. Patch 0196 adds
its own two-report slot; exact source apply and host tests pass. ARM CI
44916896554/job136884342088 at aed2d33 is building. After successful CI, private
shim/a03/out/prepare-posterboard-0128.py verifies and packages a BOOT-only
diagnostic. Capture first two crash records and symbolize; diagnostic is not
a fix. Phone remains BOOT0127; no active console reader for this investigation.

ACTIVE 2026-11-21 BOOT0127 lag measured after CDC reappeared. Over 9.821s,
557 vsync callbacks and 98 submitted/completed/copied frames (10/s); display
request on, GPU copy avg 2.223ms, zero quarantine at mid-interval status.
Earlier eight-second live capture logged 263 PosterBoard crashes; follow-up
46 in 15s. Causality unknown. Logs /tmp/a03-lag-host.log and
/tmp/a03-lag-paired.log; readers finished. GPU only copies finished frames.
Next correlate controlled physical input and paired CPU/frame counters, then
test effect of crash churn. No device changes. Button acceptance still pending.

ACTIVE BOOT0127 physical test awaits a person at the phone. The console
reader PID30533 was live at 14:37 UTC. Display request 0, 43 swaps complete,
37 copies, HID provider status 3. No captured physical key transitions.
On resumption verify the current reader, capture physical Power down/up
during display sleep and observe visible wake, then repeat with USB unplugged.

ACTIVE 14:35 UTC BOOT0127 display resumed after request 0 without a recorded
key or synthetic input. At follow-up, 34 swaps completed, 30 copies sampled,
and GPU status advanced to 35 completed with four verified and zero faults.
Do not count this transition as button wake. Sole reader PID30533/session68042
still captures boot0127-buttons-live.log. Await a physical Power press while
display request is 0 and verify visible wake, including with USB unplugged.

ACTIVE BOOT0127 buttons running. ARM CI44912955041 exact a17e9d8 success,
source and hashes verified, BOOT-only Heimdall upload succeeded. Sole console
PID30533/session68042 boot0127-buttons-live.log until about 14:58 UTC.
8/8 SGI, RTC and storage healthy, touch RAM restored and stream ON. Both
button controllers initialized and HID client open. At 14:32 UTC iOS
requested display sleep after five copies. Await physical key edges and
a new display request/copies, then unplugged wake. No synthetic input on
BOOT0127. Restore BOOT0126 is available.

ACTIVE physical button candidate 0195. Live SM-A035G DT and matching stock
source identify EIC1 power, EIC4 volume down, and AP GPIO125 volume up.
Independent worker uses a03keys=1 with existing a03_hid=1 and forwards to HID.
Debounce/fault/PMIC fixtures and ARM64 C compile pass. CI44910781005 job
136865936423 builds exact a17e9d8. Session44638 waits and verifies/pack0127 in
private physical-buttons0195-work. Intel compile passed but the verification
step stalled with no artifacts. Alternate ARM run 44912955041/job136872452726
builds the same SHA and session96022 waits for it. Packaging is serialized
between the two. Inspect authoritative run state before BOOT-only test. Verify paired physical power and volume edges and screen wake with USB
unplugged. BOOT0126 and CPU0124 restore images remain available.

ACTIVE 2026-11-21 SpringBoard froze then user confirmed recovery. Replacement
PID98999 vs original26; fresh capture has spawn but no termination reason.
GPU354041->355975copies/4verified/0fallbackquarantine; storage ready1poison0.
Displayrequest0->1, swaps resume. ONE USB Home preceded recovery report;
spontaneous versus Home-assisted recovery unknown. PosterBoard crash loop
persists. Private springboard-20261121-live.log + followup.log; bounded captures
end automatically. Prior0126capture/soak stopped hours ago, no terminal soakPASS.
No flash/reboot/GPU controls. Goal now physical buttons to wake iOS from sleep;
USB Home does not meet this. Live DT gpio-keys/PMIC EIC and existing HID button
provider are first investigation paths. Preserve current0126 and CPU0124restore.

ACTIVE03:50UTCBOOT0126actualcompositor2095GPUcopies/4verified0fallbackquarantine,
idle11; no replay/GPUcontrols. Sole168765/session9363 boot0126-boundary-live.log
until~04:12UTC. Firstsoak67126boot0126-compositor-soak.log600sfrom03:45requires
12000copiesbut~10Hzcannotreach;intermediateonly. Chainedobserver88566waits
ONLYinsufficientcountterminalthen1800s/12000unchangedgate ->
boot0126-compositor-longsoak.log; noinput/replay/GPUcontrols. Checkhandlesfirst.
Renewsolecapturebeforerunninglongsoakpast04:12(and observerlogpathmustmatch).
Physicalimage/swipequestionpending. NoCI.0193jobendcleanNOTyetfixclaim.
Onquarantineparse0194fourrecordsandretainDMA/noreset/reclaim/poweroff/overwrite.
CPU0124restoreavailable;goalactive/readbacks+idle+paired+physicalstillneeded.

ACTIVE03:45UTCBOOT0126autobootPASS4full+fast/nopriorGPUcontrolsorreplays.
ONcachedwarm384/defaultwait/tile4/idle100;5completed4verified0fault/idle3.
OneHomeafterrequest0+USBswipeupdispatch;actualsoak67126logboot0126-compositor-soak.log
600s/12000additionalrequired nowrunning. NoGPUcontrolsorreplaysduringsoak.
Sole168765/session9363boot0126-boundary-live.loguntil~04:12UTC.
Checksoak+failurelines;onquarantinereadcomplete0194snapshot,NORESET/reclaim/
ASteardown/powerdown/CPUoverwrite. Otherwisefreshreadbacks/idle/paired/physical.
CPU0124restoreavailable. Goalactive/nofixclaim/physicalpending.

ACTIVE03:43UTCBOOT0126runtime:8SGIPASS/RTC1795232498retained,nohostsync.
FWRAM79104load0/A55A;firststartupinvalidslice,onestartretry->touchON.
Storagehealthyready1poison0. GPUstilldefaultOFFbeforefirstcompositorframe;
NOhostGPUcontrols/replays. Sole168765/session9363boot0126-boundary-live.log.
Autobootverifierwaitsession87644pollslogonly;need4full+fastproof.
Thenactualcompositorlongsoak/readbacks/idle/paired/physicalgates;goalactive.
0126CI44860660965/exactede01ea;kernel72b18062...98f754b/BOOT9ab6b2d8...801773b.

ACTIVE03:40UTCBOOT0126boundaryflashedBOOT-onlySUCCESS CI44860660965/exactede01ea.
Sixsources/RTC/reverse0194/checksum/SMP/actualASanPASS. Kernel72b18062...98f754b/
BOOT9ab6b2d8...801773b;same8cores1984MiB/cmd593a03gpu=1.
Solecapture/session9363boot0126-boundary-live.logwaitingCDC;resolvePID.
NeedFWtouchload/start/A55A;NOhostGPUcontrolsorreplaysbeforeautoboot4full+fast
verifierPASS. Thenactualcompositorsoak12000additional/600s/readbacks/idle/
paired/physicalgates. Rootcausecandidate0193restoredjobendclean,0194shortlogs;
NOhardwarefixclaim. CPU0124restoreavailable;goalactive. NoactiveCI.

ACTIVE03:29UTC CI44860660965 exactede01ea/job136713035392 VERIFIEDBuild,
no duplicate/restart. AutoartifactpipelinePID166002/session34387 waits sameCI,
then exactartifacts/source/RTC/reverse0194/checksum/SMP+actualASantests+pack0126;
NOautoFLASH. Watchsession12565 alsoalive; redundantread-onlywatchonly.
CPU0124sole163479/session31133boot0124-stage5-recovery-live.loguntil~03:45UTC.
Latesthosttests bba5b4c modeljobendwriteback andstillrequirefreshack even
correctpixels; aa8496a rejectsconcurrentreplay/GPUcontrols inactualsoak.PASS.
Next inspectsamepipeline/status;onfullsuccessverifylogs/hashthenBOOT-only0126,
touchload/start/autoboot4readbacks+fast WITHOUTpriorcontrols/replays,actual
compositorlongsoak12000additional/600s,readbacks/idle/paired/physicalgates.
Goalactive/nofixclaim. gpu-boundary0193-work only;oldergpu-endflush-workunrelated.

ACTIVE CI44860660965 exactede01ea4ac14ee411c7b5fd49bf4a279030a36c5 /
job136713035392in_progressBuild03:24UTC;NODUPLICATE.0193restorejobendclean+0194bounded
snapshot;hostactualASan/ARM64PASS. gpu-boundary0193-work/artifacts.py+pack0126.py
exactpinsready;needfullsuccess/artifacttests/BOOT0126actualcompositorlongsoak.
Newread-onlya03-gpu-compositor-soak.py12000additionalcopies/600sdefaults,
guardsPASS;noinputorreplay/physicalproof. PhoneCPU0124healthy,request0idle,
sole163479/session31133 boot0124-stage5-recovery-live.log. Goalactive.

ACTIVE candidate0193 restores vendorjobendCLEAN_INV (83300) plus retainedfresh
explicitcleanack;0194splitsfailure-onlyread-onlyrecords<255+powerstate.
ActualASan/ARM64/profile140PASS;needfullCI+hardwarelongactualcompositor,
readbacks/idle/physicalacceptance. NoGPUfixclaim. PhoneCPU0124healthy,
sole163479/session31133 boot0124-stage5-recovery-live.log. Goalactive.
Privatecandidate gpu-boundary0193-work (do not reuse older gpu-endflush-work).

ACTIVE CPU0124BOOT-onlyrestoreSUCCESS aftercapturing0125stage5evidence.
Exactimage869f9c90...90e0190 verified;8SGI/RTC1795230903PASS,FWRAMload0/A55A,
touchONafteronestartretry,GPUOFFpowered0quarantine0/storagehealthy.
Sole163479/session31133 boot0124-stage5-recovery-live.log;2actualCPUframesrecovered03:17UTC.
NoCI. MissingGPUcleanfreshackrootcauseunfixed;quarantined0125clearedbyreboot.
Console255charlimitexplainsincompletesnapshot;shortenrecordsbeforenextbuild.
Goalactive;physicalUItemporarysuccessreportedbut sustainedreliabilityfailed.

ACTIVE latest0125 reproduced retirement failure at10935actualGPUcopies.
0192stage5=missingfreshCLEAN_INVcompletion; jobdone1/JSidle/MMU0/ASfault0,
rawGPU600(no bit17), translationretained. Longprintftruncatedafterclock38;
strictparserrejects(no fabricatedfields). Separate10935/391verified/67idle/
quarantine1/powered1/0fallback. Vsyncadvances/displayrequest1/swapinflight,
so currentfreezeNOTnormalsleep. NOreset/reclaim/ASteardown/poweroff/CPUoverwrite.
Privateboot0125-retire-soak-live.log+secondtrial.log. CPU0124restoreavailable.
Nextshorterdiagnosticrecords+cleancompletionrootcause;goalactive/notfixed.

ACTIVE03:08UTC0125diagnosticactualcompositor10025copies(no replay)no fault,then
4requestedreadbacksPASS+backgroundverifyframes->10412completed391verified,
0fallbackquarantine/idle63. OFFbusydeclinesexplicitlyhandled; confirmedOFFpowered0
verify1,CPUcopiesresume. NOTFIX:0192loggingonly/original0123intermittentfailure
unreproduced/physicalpending. NoCI;0124CPUrestoreavailable. NEWsole/session97940
boot0125-retire-soak-live.loguntil~03:38UTC(old159238stopped);resolvePIDnext.
Originalbootprooflogboot0125-retire-live.logretained. Goalactive;nextfailurestage
captureandrootcausecomparison,notmorestaticreplaycompletionclaims.

ACTIVE03:00UTC0125actualcompositor5776GPUframes/4verified0fault/idle41asof02:59UTC,
NOreplayafterboot. Exceeds0123failure2041but0192loggingonly,NOFIXclaim/rootcause
unknown. Needlongercaptureorreprostage. Sole159238/session38202
boot0125-retire-live.loguntil~03:12UTC(renew).NoCI/0124CPUrestoreavailable.
Goalactive/physicalpending.

ACTIVE02:50UTCBOOT0125diagnosticGPUONauto4readbacks+fastPASS. ActualHomewake+
USBswipeupactivity292completed0fault(4verified),idle11/384waitcachedwarm1.
FWtouchON1017events0/storagehealthy. Needlongeractualactivityuntilstagecapture;
shortpassdoesnotfix0123failure. NoCI,0124CPUrestoreavailable. Sole159238/
session38202boot0125-retire-live.loguntil~03:12UTC.Goalactive/physicalpending.

ACTIVE02:42UTCBOOT0125snapshotBOOT-onlyflashSUCCESS CI44856061555/exact2d4bf90,
sixsources/RTC/reverse0192/checksum/SMP/actualASanPASS. Kernelafa07d30...caccd38/
BOOT7a0dbc94...3e12fa3;same8cores1984MiB/cmd593a03gpu=1. Newsole/session38202
boot0125-retire-live.logwaitingCDC. RestoretouchFW/load/start/autobootproof,
thenactualHomecompositoractivitycatchfailurestage/parser555ea32; nofixclaim.
0124CPUrestoreavailable. Goalactive.

ACTIVE02:33UTC0124CPUcontrolruntimePASS2CPUframes0GPU/OFFpowered0quarantine0;
8coresRTChealthy,FWRAMload0/A55A/touchON,storageready1poison0. Sole157092/
session91200boot0124-cpu-live.loguntil~03:00UTC.0192CI44856061555 exact2d4bf90/
job136698449738Build;norestartduplicate. Privategpu-retire-work/artifacts.py+
pack0125.pyready. NeedfullCI/actualASan->BOOT0125->sustainedactualGPUactivity
snapshotfailurestage.0123failedafter2041copies,notfixed.Goalactive.

ACTIVE02:30UTCCPUcontrol0124BOOT-onlyrestoreSUCCESS;exact0123kernel/noa03gpu=1,
cmd584/8cores1984MiB,BOOT869f9c90...90e0190. Sole157092/session91200
boot0124-cpu-live.logwaitsCDCuntil~03:00UTC. RestoreFWtouch+CPUframeshealth;
DONOTenableGPUincontrol.0123quarantine1after2041actualcopiesrequiresrootcause.
0192snapshotCI44856061555 exact2d4bf9085c197989dc30c05491268fad01debeb4
job136698449738Build/noduplicate. Privategpu-retire-work/artifacts.py+pack0125.py
ready; needexactfullCI+actualASan->BOOT0125->actualcompositorfailurestage.
Goalactive,physicalpending;nofixclaim.

ACTIVE02:27UTC0123SUSTAINEDUIFAIL:Homegenerated1388actualGPUframes653->2041then
retirementunproven/quarantine1; panelwritesstop/source+scratchretained,powered1.
NOTsleep(request1), USB/time/touch/storagealive. NOreset/reclaim/CPUoverwrite.
Needsreboot.0192read-onlyfailurestage/registersnapshotactualASan/ARM64/profile138
PASS; fullCIpending. RestoreCPUcontrolBOOT(exact0123kernel,noa03gpu)whilebuildruns.
Sole154528/session47211until~02:42UTC.Goalactive;physicalquestionpending.

ACTIVE02:24UTC0123additional64coldcycles+4freshreadbacksPASS;medcold2.650231ms.
CurrentimagepairedCPU/GPUwall1.532567/2.065918ms;submitter1.533552/0.821230ms
(46.45%saved). All0fallbackquarantine. BeforeHIDtrial653GPU/24CPUcompleted,
12verified; ONfast/idlepower0/384defaultwait. OneHome+swipeupdiagnosticongoing,
notphysicaltouch. Physicalanswerpending/goalactive/noCI. Sole154528/session47211
boot0123-idle-live.loguntil~02:42UTC. Needphysicalacceptance/actualframehealth.

ACTIVE02:20UTCBOOT0123normalGPUONfast/idlepowered0 validated:autoboot4fullthenfast,
12automaticpoweroff/coldresumes,512stress+4finalreadbacksPASS0fault.561completed/
8verified/82idlereleases; meanstress2.055193wall/0.843793submitterms.384APB11/11/31,
pollwaitimpldef0tile4cachedwarm1. TouchON1037events0/storageready1poison0.
Sole154528/session47211boot0123-idle-live.loguntil~02:42UTC.NoactiveCI.
Sourcebc4137cCI44853265071/kernel985328ce...ff365ac/BOOT9f03fb56...95c9314.
Goalactive:physicalimage/swipeanswerpending/unpluggedbootunverified;sourceCPU
renders/MetalEAGLabsent;nofasterFPSclaim. Nextphysicalacceptance+actualframes.

ACTIVE02:19UTCBOOT0123autoboot4readbacks+fastPASS/nohostGPUcontrols. Idlepower0
observedat2and4verifiedframes.12coldcyclesPASS(releases5..16/completed34..45)
0fault/qualificationretained,lastcoldcopies2.50-2.69ms.64x8stressnowrunning,
needfinal4readbacks/idlehealth. Sole154528/session47211until~02:42UTC.
Physicalquestionpending/noactualtouchyet. Goalactive/sourceCPUrenders.

ACTIVE02:12UTCBOOT0123idleBOOT-onlyflashSUCCESS CI44853265071/bc4137c/sixsources/
RTC/reverse0191/source22.6/checksum/SMP/actualASanPASS. Kernel985328ce...ff365ac/
BOOT9f03fb56...95c9314;same8cores1984MiB/ADT0094/cmd593a03gpu=1.
Newsole/session47211boot0123-idle-live.logwaitsCDC. NOhostGPUcontrols/replayuntil
4readback+fastautobootproof. RestoretouchFW/load/start->autobootverifier->12idle
cycles->stress512+4freshreadbacks->physicalUI. Goalactive.

ACTIVE02:00UTC0191idleCI44853265071 exactbc4137cfc886f86155e08a0d95a41bc620122967
job136689379518in_progress/noduplicate. Privategpu-idle-work/artifacts.py+
pack0123.py sixsources/RTC/0191/SMP; same593bytea03gpu=1. Needfullsuccess->
actualASan->BOOT0123autoboot/idlepower0/coldresume/readbacks/stress/physicalUI.
Sole150953/session16774boot0122-bootpolicy-live.loguntil~02:19UTC;watch3854.
Current0122OFFpowered0verify1/384pollwaitcachedwarm1/549completed8verified0fault,
touchON1225events0/storagehealthy. Autoboot+512stressPASS,physicalpending.Goalactive.

ACTIVE01:58UTC0122autoboot+512stress+4finalreadbacksPASS(mean1.988864wall/0.832096
submitterms),0fault. RestoredOFFpowered0/384pollwaitverify1/549completed8verified,
touchON1225events0/storagehealthy. Sole150953/session16774until~02:19UTC.
0191idle100msreleaseviaexistingvsyncunderfblock/nonwaitingGPUowner/warm_stop;
actualASan deadline/busy/coldresume/ASquarantine/vsynchookPASS,ARM64/profile137.
NeedfullCI->BOOT0123autoboot/idleoff/coldresume/readbacks/stress/physicalUI.
Goalactive/sourceCPUrenders/physicalanswerpending.

ACTIVE01:54UTCBOOT0122autonomousGPUproofPASS:activation->4fullreadbacks->fast,
NOpriorhostGPUcontrols/replay. ONEHomeafterrawpower0causesdelayedrequest1/frames.
Status33completed4verified0fault/cachedwarm1ONpowered1/384pollwait. Cableconnected;
unpluggedbootnotproven.64x8stressnowrunningafterproof. Physicalquestionpending.
Sole150953/session16774boot0122-bootpolicy-live.loguntil~02:19UTC. Needstressfinal
readbacks/physicalUI/idlepowerpolicy;goalactive,sourceCPUrenders/MetalEAGLabsent.

ACTIVE01:49UTCBOOT0122 BOOT-onlyflashSUCCESS CI44849933946attempt2/e8306f9success,
sixsources/RTC/reverse0190/source22.6/checksum/SMP/actualASanPASS.
Kernele8f07f5c...5d1d454/BOOT93524888...ca408bd;cmd593+a03gpu=1,8cores1984MiB.
NEWsolecapture/session16774boot0122-bootpolicy-live.logwaitsCDC. NOhostGPUcontrols/
replaysbeforeautonomous4fullreadback+fastlogproof(tools/a03-verify-gpu-boot.py).
RestoretouchFW/load/start,read-onlydisplay/time/statusallowed. Goalactive.

ACTIVE01:43UTCbootpolicy44849933946attempt2job136680652501 VERIFIEDin_progressBuild
exacte8306f9(start01:31:47). No duplicate/restart. Sole148860/session82510
boot0121-bootwait-live.loguntil~02:07UTC;watch5403ci-watch-attempt2.log.
NextsameCI->privategpu-bootpolicy-work/artifacts.py+actualASan+pack0122.py
->BOOT-only->NOhostGPUcontrol/replaybeforeautonomous4readback+fastproof.
0121lastconfirmedOFFpowered0/384pollwaitverify1/698completed16verified0fault,
touchON4003events0/storagehealthy. Goalactive/physicalanswerpending.

ACTIVE01:37UTC44849933946attempt2job136680652501stillBuild/exacte8306f9; noduplicate.
NEWsole148860/session82510boot0121-bootwait-live.loguntil~02:07UTC(old144533stopped).
Last0121OFFpowered0/384pollwaitverify1/698completed16verified0fault/touchON/
storagehealthy. NeedfullCI->privateartifacts.py/pack0122.py->actualASan->BOOT-only
thenNOhostGPUcontrols/replaybeforeautonomous4readback+fastlogverifierproof.
PhysicalUIpending, goalactive.

ACTIVE01:30UTC0190CI44849933946attempt1FAILEDnetworkclone libpthread github443,
BEFOREkernelcompile. Explicitfailed-jobrerunsame44849933946requested/exacte8306f9.
Noartifactaccepted/nophonechange. Donotdispatchduplicate. Autonomousstartup
verifierf752930negativefixturesPASS; privatepack0122/593bytecmdready. Needfull
success->actualASan->BOOT-only->nohostGPUcommandsuntil4readback+fastproof.
Current0121OFFpowered0/384pollwaitverify1touchON;sole144533/session9510~01:41UTC.
Goalactive.

ACTIVE01:24UTC0190qualifiedbootCI44849933946/e8306f9e90e412a9153a44caf38ea13ed07b0d8a
in_progressjob136678627018. No duplicate. Privategpu-bootpolicy-work/artifacts.py+
pack0122.py exactsources/RTC/0190/SMP; cmd593remove-show_pointers+adda03gpu=1.
Needfullsuccess->actualASan->BOOT0122->NOhostGPUcommandsuntilfirstframe;
thenstatus/fourreadbacks/stress+physicalUI. Current0121GPUOFFpowered0/384/
pollwaitverify1cachedwarm1/698completed16verified0fault,touchON/storagehealthy.
Sole144533/session9510until~01:41UTC.Goalactive.

ACTIVE01:23UTC0121stress512fast+4fullreadbacksPASS,meanwall2.014929/submitter
0.869928ms,0fault. Pollwaitsubmitter0.871vspollspin1.935ms:keepwait. Restored
384pollwaitGPUOFFpowered0verify1cachedwarm1/698completed16verified0fault,
touchON1680events0/storagehealthy. Sole144533/session9510until~01:41UTC.
0190a03gpu=1firstframequalifiedcachedwarm384bootpolicy prepared/actualASan/
ARM64/profile136PASS; needfullCI->BOOT0122+a03gpu=1(nohostGPUcommands)proof.
Physicaltrial10GPUframesthenpower0sleep/noevents;useranswerpending.Goalactive.

ACTIVE01:18UTCBOOT0121validpairedruntime:384CPU/GPUsubmitter1.397245/0.842947ms
(39.7%saved),5121.402822/0.812904(42.1%saved). WallGPU2.028/1.974msremains
aboveCPU1.396/1.402. This isreal submitterCPUoffload,notFPS/system/renderinggain.
Firstreportserializationtuplekeyfixed3df1c3a/testsuccessfullmain; retryfullJSONvalid.
Livephysicaltrial384pollwaitfastONwarm1powered1/116completed4verified0fault,
ONEHome/touchON964events0; physicalquestionpending. Sole144533/session9510
until~01:41UTC. Needphysical+sustainedactualframes+deploymentpolicy;goalactive.

ACTIVE01:10UTCBOOT0121runtime BOOT-onlyflashSUCCESS correctCI44846854268/
3d14c72/fullsource22.6.0/sixsources/RTC/reverse0189/checksum/SMP/actualASanPASS.
Kernel320e5407...d99f0ae/BOOTa4f3c20b...6a8346;same8cores1984MiB/ADT0094/cmd599.
Solecapture/session9510boot0121-runtime-live.logwaitingCDC. Needclocks/cachedwarm/
FWload/touchON/acceptedframe->GPUOFF->pairedwall/submitterCPU384/512/readbacks.
Wrongsource44846779804cancelled; replacementSUCCESS. Goalactive,nobenefitclaim.

ACTIVE00:57UTC runtimeCI44846854268 exact3d14c72 stillPENDING behind44846779804
wrongsource run. Normalcancel andforce-cancel202accepted but wrongrunstill
in_progressDeps; authoritativeAPI notterminal, donotrestartreplacement. Sole
reader138803/session43018until~01:14UTC,liveboot0120-poll-live.log. Current
384pollwaitGPUOFFpowered0verify1/165completed/0fallbackquarantine/touchON2113
slices0events/storageready1poison0. Displaylastrequest0idle; noperiodicHome.
NextpollsameCI->exactartifactvalidation/privatepack0121->BOOT-only->FWtouch/
acceptedframe->fourreadbacks+pairedCPUwall/runtime at384/512. Helpercancompare
pollwait/pollspin; no0188speedgain. Goalremainsactive, physicalacceptancepending.

ACTIVE00:55UTC0189CIreplacement44846854268 exact3d14c720278607e27fe4142b167a8fc9380e7759,
correct13.5source/SWEET/A03/macOS26intel/fulltree. Wrong26.0source44846779804
cancelrequested; donotacceptitsartifacts. Replacementpending; noduplicate.
Privategpu-runtime-work/artifacts.py+pack0121.py pinsixsources/RTC/0189/SMP.
Needfullsuccess->actualASan->BOOT0121->readbacks+wall/submitterCPUcomparison.
Current0120confirmed384pollwaitGPUOFFpowered0verify1touchON/storagehealthy.
Sole138803/session43018until~01:14UTC.Goalactive.

ACTIVE00:53UTC0120 counterpollHWbothratesPASS,nolatencygain:384GPUwait/spin
2.035014/2.029918ms,5121.964975/1.962125ms. Firstsamples rejectedextraCPU/GPU
backgroundcopies; acceptedretryeach4readbacks+3paired8. Restored384pollwait/
GPUOFFpowered0verify1impldef0tile4cachedwarm1/165completed0fallbackquarantine;
touchON1086events0/storagehealthy. Sole138803/session43018until~01:14UTC.
0189submitterCPU-runtimeobserver+parsingtests/profile135/actualASanPASS;
C++syntaxPASShostApplebuiltin substitutionsonly. NeedfullCI/hardware; noCPU
benefit/physicalcompletionclaim. Goalactive.

ACTIVE00:44UTC BOOT0120 BOOT-onlyflashSUCCESS CI44844162892/cc4576success,
sixsources/RTC/reverse0188/checksum/SMP/actualDMA+rate+replayASanPASS.
Kernelcc4ba850...bef7d6b/BOOT5f2569fc...acd508;same8cores1984MiB/ADT0094/cmd599.
Newsole session43018 boot0120-poll-live.log waitsCDC. Needclocks/cachedwarm/
FWload/touchON/acceptedframe->GPUOFF->pairedpollwait/pollspin384and512->restore.
Private runtimeobservernotstaged; C++baselineAppleheadererrors local. Goalactive.

ACTIVE00:36UTC polling rationale correction: exact XNU initializes CNTKCTL
WFE periodic event stream in arm_init. Prior no-wake-event statement unproven.
delay10us can instead thread_block when cpu_idle_latency0; counterpoll compares
combined wait/scheduler overhead, not proof of brokenWFE. 0188/defaultwait
unchanged; actualDMAASan rerunPASS. CI44844162892 stillBuild. Sleep evidence
and Home wake recordedddd8a61; physicalconfirmationpending.

ACTIVE00:33UTC BOOT0119 idle-sleep evidence: rawpower0/swaps143/copies137
stop whilevsync/timealive; GPUalreadyOFFpowered0/fallback0quarantine0. ONE
inputhome->rawpower1->swaps439/copies433about10slater. Supports sleep/wake
forstaleclock; physicalrecoverypending, panelpowersemanticsnotimplemented.
No periodicHome/fakeframes. CI44844162892 stillbuilding0188; no duplicate.

ACTIVE00:30UTC CI44844162892/exactcc4576ae04936dc1621b7621cc07ba698df31d7f
in_progress0188counterpoll. No duplicate. Hostratehelperrestorekeytestfailed,
fixeda5f75eb/allbenchmarktestsrerunPASS; kernelcandidateunchanged.
Privategpu-poll-work/artifacts.py+pack0120.py pinexactrun/sixsources/RTC/
reverse0188/checksum/SMP. Needfullsuccess->actualASan->BOOT-only0120->four
readbacks/pairedpollwait-pollspin/rates->restore. Current0119GPUOFFpowered0/
384verify1touchON;sole133832/session39451until~00:48UTC.Goalactive.

ACTIVEcandidate0188explicitpollspin(counterbounded10usgap) vsdefaultpollwait
(delayusesWFEcanovershootuntilunrelatedIRQ). Framebufferonly; iterationtimeouts/
faults/cacheclean/retirementunchanged. ActualDMAASan+modes0..7/ratehelper/ARM64/
profile134/benchtestsPASS. NeedcommitCI->BOOT-only0120->readbacks/pairedpolicies.
Current0119GPUOFFpowered0/384verify1/touchON,sole133832/session39451until~00:48UTC.
Goalactive; hypothesiscouldexplain1.3msexecutephase,notprovenyet.

ACTIVE00:23UTCNov21 BOOT0119HWbothratesreadbacks+pairedPASS, GPU512median1.969163ms
vsCPU1.664846ms(18.3%slower).384GPU2.041745vsCPU1.677052. Singleexplicitendclean
functionalbutnogreatgain;fallback0quarantine0. Last512execute1.309ms/sourceclean
0.392/setup0.094ms. Currentconfirmed384APB11/11/31/GPUOFFpowered0verify1impldef0
/tile4cachedwarm1,61completed/verified0(resetrestore),touchON389events0/storagehealthy.
Sole133832/session39451boot0119-endflush-live.loguntil~00:48UTC.NoactiveCI.
Validatedcode7607421CI44840823838/kernel a99f3c6a...e897f9/BOOT03196670...cbce39.
Goalactive:needactualGPUbenefit+physicalUIacceptance;sourceCPUrenders/MetalEAGLabsent.
Nexttargetmeasuredexecution+sourcecleancost,keepallownership/cachecompletionguards.
Privatepipeline/linearshaderexperimentsnotstaged.No periodicHome/fakeframes.

ACTIVE0119endflushBOOT-onlyflashSUCCESS00:17UTCNov21 CI44840823838/7607421success/
sixsources/RTC/reverse0187/checksum/SMP/actualDMA+rate+replayASanPASS.
Kernela99f3c6a...e897f9/BOOT03196670...cbce39;same8cores1984MiB/ADT0094/cmd599.
NEWsolecapture/session39451boot0119-endflush-live.logwaitsCDC.Needclocks/cachedwarm/
FWload/touchON/acceptedframe->GPUOFF->ratebenchmark384/512/readbacks+paired
->384restore/physicalUI.Goalactive;no0187hardwareclaimyet.

ACTIVE00:00UTCNov21 CI44840823838/exact7607421e7dfeed0c335aa22ad1c5297f452ce0ca
in_progress0187singleverifiedendclean. No duplicate. Privategpu-endflush-work/
artifacts.py+pack0119.py pinexactrun/sixsources/RTC/reverse0187/checksum/SMP.
Needfullsuccess->actualASan->BOOT-only0119->readbacks+pairedrates->384restore.
Current0118confirmed384APB11/11/31/GPUOFFpowered0verify1impldef0tile4cachedwarm1,
80completedverified0(reset)/0quarantine. Sole129991/session2940until~00:22UTC.
Goalactive; native16Koptimizationimproved512GPUmedian1.983msbutCPUstillfaster.

ACTIVE0118native16KHWreadbackPASSmappingphase~0.06-0.13ms(vs0.23),GPU384median
2.055985ms;512retrymedian1.982543ms. First512runrejectedbackgroundCPU36vs8;
retryvalid/restorationmustcheck. Sole129991/session2940until~00:22UTCNov21.
0187cachedframebufferremovesduplicateautomaticendflushONLY; keepsstartflush+
explicitfreshGPUCLEAN_INVackbeforeCPUread/ASretire/fallback/poweroff. Uncached/
privatediagnosticendflushunchanged. ActualASanDMA/cachefail/ratehelper/ARM64/
profile133PASS. Needcommit/fullCI->BOOT-only0119->readbacks+pairedrates.
Goalactive; stillnoCPUoverGPUspeedup/physicalacceptance.

ACTIVE0118map16BOOT-onlyflashSUCCESS23:51UTCNov20 CI44836868623/e8e3dee success/
sixsources/RTC/reverse0186/checksum/SMP/actualDMA+rate+replayASanPASS.
Kernel8e5a69be...eeec11/BOOTbbb51c88...1e70da; same8cores1984MiB/ADT0094/cmd599.
NEWsolecapture/session2940boot0118-map16-live.logwaitsCDC. Needclocks/cachedwarm/
FWload/touchON/acceptedframe->GPUOFF->ratebenchmark384/512/readbacks+paired
->384restore/physicalUI. Goalactive; no0186hardwareclaimyet.

ACTIVE23:47UTCNov20 CI44836868623/e8e3dee stillBuild;live23:46compilerprogress.
No duplicate. NEWsole129094/session93167boot0117-mapwait-live.loguntil~00:17UTCNov21,
old125084stoppedbeforeexpiry. Current0117GPUOFFpowered0/384verify1impldef0tile4/
cachedwarm1touchON. NeedexactCI->gpu-map16-work/artifacts.py+pack0118.py/
actualASan->BOOT-only0118->fullreadbacks+pairedrates. PrivatelinarshaderNOTstaged.
Goalactive/nospeedupyet.

ACTIVE23:27UTCNov20 CI44836868623/exacte8e3dee4d9ffa018199d2f6e975516606fbf9ce5
in_progress0186native16Kvalidation. No duplicate. Privategpu-map16-work/artifacts.py+
pack0118.py pinexactrun/sixsources/RTC/reverse0186/checksum/SMP. Needfullsuccess
->actualASan->BOOT-only0118->fullreadbacks+pairedrates/mappingphase->384restore.
Current0117GPUOFFpowered0/384verify1impldef0tile4cachedwarm1touchON. Sole125084/
session54578boot0117-clean-live.loguntil~23:49UTC. Goalactive,nospeedupyet.

ACTIVE0117cleanHWreadbacks+pairedPASS0fault;GPU384/512medians2.202/2.126ms vs
CPU1.728/1.796ms. No sourcecleangain. Left384APB11/11/31/GPUOFFpowered0verify1/
impldef0tile4cachedwarm1/60completedverified0(reset),touchON/storagehealthy.
Sole125084/session54578boot0117-clean-live.loguntil~23:49UTC.
0186native16Kpagevalidationcandidateperframe(no persistentmappingcache), expands
4KiBGPUPTEs; sourcebase+end/range/destinationpageend/faulttestsPASS, fullframe
source translations600vs2400. ActualDMAASan/ARM64/ratehelper/profile132PASS.
Needcommit/fullCI->BOOT-only0118->readback+pairedrates/mappingphase. Goalactive.

ACTIVE0117cleanBOOT-onlyflashSUCCESS23:18UTCNov20 CI44834205541/0aeb872 success/
sixsources/RTC/reverse0185/checksum/SMP/actualDMA+rate+replayASanPASS.
Kernel3262a1d4...0b3e2c/BOOTba7c925d...89231e; same8cores1984MiB/ADT0094/cmd599.
NEWsolecapture/session54578boot0117-clean-live.logwaitsCDC. Needclocks/cachedwarm/
FWload/touchON/acceptedframe->GPUOFF->ratebenchmark384/512/fourreadbacks+paired
->384restore/physicalUI. Goalactive; no0185hardwareclaimyet.

ACTIVE23:06UTCNov20 CI44834205541/exact0aeb87285006e112783b5e47bd01e81ef2344591
in_progress0185sourceCleanPoC. No duplicate. Privategpu-clean-work/artifacts.py+
pack0117.py pinexactrun/sixsources/RTC/reverse0185/checksum/SMP. Needfullsuccess
->actualASan->BOOT-only0117->fourreadbacks/paired384and512->restore.
Current0116restored384/GPUOFFpowered0verify1impldef0tile4cachedwarm1touchON.
Sole122100/session86364boot0116-rate-live.loguntil~23:30UTC.Goalactive.

ACTIVE23:05UTC0116HW384/512PASSreadbacks+paired0fault;GPUmedians2.193/2.128ms
CPU1.667/1.663ms,smallrateeffect. Restored384APB11/11/31/GPUOFFpowered0verify1/
impldef0tile4cachedwarm1/60completedverified0(reset),touchON/storagehealthy.
Sole122100/session86364boot0116-rate-live.loguntil~23:30UTC.
0185ONLYsourceCPUFlushPoC->CleanPoC (GPURO/NX,dc cvac+dsbsy); alljobflush/GPU
CLEAN_INV/retirementguardsremain. ActualASanDMA+rate/ARM64PASS;needfullCI/
BOOT-only0117/readback+pairedcomparison. Goalactive,nospeedupyet.

ACTIVE0116rateBOOT-onlyflashSUCCESS22:59UTC CI44831543349/ce9bc57 success/sixsources/
RTC/reverse0184/checksum/SMP/actualDMA+ratehelperASanPASS. Kernel1a1ca22b...afe5dc/
BOOT80632772...a618c2; same8cores1984MiB/ADT0094/cmd599/stockramdiskDT.
NEWsolecapture/session86364boot0116-rate-live.logwaitsCDC. Needclocks/cachedwarm/
FWload/touchON/acceptedframe->GPUOFF->ratebenchmark384/512->384restore.
Privatenextgpu-clean-work sourceCleanPoCvsFlushPoC actualASan/ARM64PASSbut
notstaged/CI; trackedDMA test optionalcleanstubuncommitted. Goalactive.

ACTIVE22:45UTC CI44831543349/exactce9bc57ce4f8e159a743183a2122181d8e20b2da
in_progress0184stock512MHzidlepolicy. No duplicate. Privategpu-rate-work/
artifacts.py+pack0116.py pinexactrun/sixsources/RTC/reverse0184/checksum/SMP.
Needfullsuccess->actualASanDMA+ratehelper->BOOT-only0116->idle512fourreadbacks/
pairedCPUfast->384restore/physicalUI. Current0115GPUOFFpowered0impldef0tile4/
verify1cachedwarm1touchON. Sole118404/session97962until~23:07UTC.
Goalactive,nospeedupyet.

ACTIVE0115allcachepoliciesHWreadback+pairedPASS0fallbackquarantine;GPU~2.19-2.33ms
CPU~1.43-1.71ms. No cachegain; leftimpldef0/tile4/GPUOFFpowered0verify1cachedwarm1,
89completed/verified0(resetrestore),touchON. Sole118404/session97962until~23:07UTC.
0184explicitstock384/512MHzidleparentpolicy prepareddefault384; nativeSamsung
clocksource/liveDToppreview, exactinherited1Vrail(noPMICwrite), noPLL/DVFStable
writes. Idle/coreoff/AS/fault/PLLguards+maskedgate/selectorrollbackASanPASS;
actualDMAfake512/ARM64/profile130/benchtestsPASS. Needcommit/fullCI->artifact/
pack0116->BOOT-only->fourreadbacks512->pairedrates->restore/physicalUI.
Goalactive; noGPUoverCPUspeedupyet.

ACTIVE0115memattrBOOT-onlyflashSUCCESS22:36UTC CI44828092327/3ed3ad3 fullsuccess/
sixsources/RTC/reverse0183/checksum/SMP/actualASanPASS. Kernelb760ef93...3e9338/
BOOT8c195289...adc345; same8cores1984MiB/ADT0094/cmd599/stockramdiskDT.
NEWsolecapture/session97962boot0115-memattr-live.logwaitsCDC. Needclocks/cachedwarm/
GPUONverify1/FWload/touchON/acceptedframe->memattrbenchmarkimpldef/cacheall/
writealloc(eachfourreadbacks+paired3rounds8copies)->restore/physicalUI.
Goalactive; no0183hardwareclaimyet. Preserve0114/0113restore.

ACTIVE22:20UTC CI44828092327 exact3ed3ad339ce0b4edfe23c50370dd8e2134ae9c1e
queued0183pixelcacheattributes. No duplicate. Privategpu-memattr-work/artifacts.py+
pack0115.py pinexactrun/sixsources/RTC/reverse0183/checksum/SMP. Needfullsuccess
->actualASan->BOOT-only0115->fourreadbacks+pairedimpldef/cacheall/writealloc.
Current0114GPUOFFpowered0tile4verify1cachedwarm1/touchON. Sole114370/session7470
boot0114-tiles-live.loguntil~22:41UTC. Goalactive,nospeedupyet.

ACTIVE0114alltilesHWreadback+pairedPASS0fallbackquarantine;GPUmedians4/8/16/32
rows=2.186/2.205/2.208/2.255ms, CPU~1.4-1.7ms. tile4best/default. LeftGPUOFF
powered0verify1tile4cachedwarm1/120completed/verified0(resetrestore),touchON.
Sole114370/session7470boot0114-tiles-live.loguntil~22:41UTC.
0183pixelmemattrimpldef/cacheall/writealloccandidate(index0/1/2 vendorvalues)
prepareddefault0; keepsallflush/cacheclean/retirement/sourceownershipguards.
ActualASanallpolicies+failure/ARM64/profile129/benchtestsPASS. NeedcommitCI
->artifactgates/pack0115->BOOT-only->fourreadbacks+pairedperattr. Goalactive.

ACTIVE0114tilesBOOT-onlyflashSUCCESS22:10UTC CI44824395202/2dc47e3 fullsuccess/
sixsources/RTC/reverse0182/checksum/SMP/actualASanPASS. Kernel52f73c0c...9c3475/
BOOT8e63704c...e690f7; same8cores1984MiB/ADT0094/cmd599/stockramdiskDT.
NEWsolecapture/session7470boot0114-tiles-live.logwaitsCDC. Needclocks/cachedwarm/
GPUONverify1/FWload/touchON/acceptedframe->tilebenchmark4/8/16/32(eachfresh4
readbacks+paired3rounds8copies)->restoration/physicalUI. Hosthelper20072c8PASS.
Goalactive; no0182hardwareclaimyet.

ACTIVE21:54UTC CI44824395202/exact2dc47e3ed8171a73e85c91ba42b5eb6dfbe41771
in_progress0182dispatchtiles. No duplicate. Privategpu-tiles-work/artifacts.py+
pack0114.py pinexactrun/sixsources/RTC/reverse0182/checksum/SMP. Needfullsuccess
->actualASan/pack0114->BOOT-only->fourreadbacks eachtile->pairedCPUfast.
Current0113GPUOFFpowered0verify1cachedwarm1/29frames4verified0quarantine;
touchON. Sole109705/session30146boot0113-quarter-live.loguntil~22:13UTC.
Goalactive; 2.153msGPUvs1.580CPU,physicalUIpending.

ACTIVEcandidate0182fullscreen dispatchtile4/8/16/32 (default4) prepared;
nativev9packers/allpolicy actualASanUBSan/ARM64GPUAMFI/profile128/benchtestsPASS.
Same shaderbytecode(globalIDs), genericfallback unchanged; tilechanges reset
fourreadbacks. Needcommit/fullCI->BOOT-only0114->readbacks/pairedperpolicy.
Current0113GPUOFFpowered0verify1cachedwarm1/29frames4verified0quarantine;
touchON. Sole109705/session30146boot0113-quarter-live.loguntil~22:13UTC.
Goalactive; currentGPUmedian2.153vsCPU1.580ms,physicalacceptancepending.

ACTIVE21:50UTC0113HWfullreadbackPASS; pairedGPUmedian2.153456vsCPU1.579903ms.
GPUcopyworksbutstillnospeedup. LeftGPUOFFpowered0verify1cachedwarm1/29frames/
4verifiedcompleted29/0fallbackquarantine;touchON1115events0/storage ready1poison0.
45sUItrialONEactualGPUframe/noevents;userphysicalreplypending. Sleepcorrelation:
rawpower1->0thenidle/swaps54;ONEHome->rawpower1/swap55thenCPU63/swaps94.
Stronglysupportsidledisplaysleepforstaleclock,butrawenums/panelcompletionnot
proven;PosterBoardcrashloopsalsoexist. No periodicHome/fakeframes installed.
Sole109705/session30146boot0113-quarter-live.loguntil~22:13UTC. NoactiveCI.
Validatedcodead0c309CI44820099545;deployment64988fe;latestevidencecommitnext.
UntestedloadpipelineexperimentPRIVATEgpu-pipeline-work/fullscreen-experiment.c;
trackedgeneratorrestored. NeedactualGPUbenefit/physicalUIbeforegoalcomplete.

ACTIVE0113quarterBOOT-onlyflashSUCCESS21:42UTC CI44820099545/ad0c309 fullsuccess/
sixsources/RTC/reverse0180+0181/checksum/SMP/actualASan+methodtestsPASS.
Kernel484a5f78...9bc0ef/BOOT353872d2...7e3be8; same8cores1984MiB/ADT0094/cmd599.
NEWsolecapture/session30146boot0113-quarter-live.logwaitsCDC. Needclocks/
cachedwarm/GPUONverify1/FWload/touchON->4fullreadbacks->pairedCPUfast/physicalUI.
Display now observes rawselector12powerrequests/time/counter; needhardware
sleepcorrelation. Goalactive; no newperformance/sleepclaimyet.

ACTIVE21:25UTC CI44820099545/exactad0c30959b4607e032e77799acb8aa30d464f772
in_progress0180coalescedstrips+0181readonlypowerrequestobserver. No duplicate.
Privategpu-quarter-work/artifacts.py+pack0113.py pinexactrun/sixsources/RTC/
reverse0180+0181/checksum/SMP. Needfullsuccess->actualASan/methodtests->BOOT-only
0113->fourfullreadbacks->pairedCPUfast/physicalUI+rawpowerrequestcorrelation.
0112leftGPUOFFpowered0verify1cachedwarm1/33frames9verifiedcompleted33/0quarantine,
touchON. Sole106124/session85627boot0112-full4-live.loguntil~21:48UTC.
CurrentbestGPUmedian2.230663vsCPU1.668356ms; goalactive/nospeedupyet.

ACTIVE0112HWfullreadbackPASS9verified;pairedGPUmedian2.230663ms vsCPU1.668356ms,
stillnospeedup. GPUrestoreverify1ONafterbenchmark; turnOFF/powered0beforeidle.
TouchON. Sole106124/session85627boot0112-full4-live.loguntil~21:48UTC.
0180coalescedquarters384bytes/15x4/3x400 candidate+0181readonlypowerrequest
observer(selector12 rawscalar/time/counter;keepsbadargument/panelbehavior).
NativeMesa/primaryv9/actualASanUBSan/ARM64GPUAMFI/profile127/methodtestsPASS.
Needcommit/fullCI->artifactgates/pack0113->BOOT-only->4fullreadbacks->paired/
physicalUI. Needactualpowerrequestcorrelationforsleephypothesis. Goalactive.

ACTIVE0112full4BOOT-onlyflashSUCCESS21:17UTC afterCI44817012332/f712f5f
exactsource/RTC/checksum/reverse0179/SMP/actualASanUBSanPASS. Kernel4f28bf12...
865da0/BOOTf9ab4fab...d40d13; same8cores1984MiB/ADT0094/cmd599/stockramdiskDT.
Solecapture/session85627boot0112-full4-live.log waitsCDC. Needclocks/cachedwarm/
GPUONverify1/FWload/touchON->4fullreadbacks->pairedCPUfast/physicalUI. No0179
hardware/speedclaimyet; goalactive. Preserve0111/0109restore.

ACTIVE21:04UTC CI44817012332/exactf712f5fd9cc4767f04589ca9e6da2fa7bf02b58b
in_progressfourpixel0179. No duplicate. Privategpu-full4-work/artifacts.py+
pack0112.py prepared; needfullsuccess/exactsixsources/RTC/reverse0179/SMP/
checksums/actualASan->BOOT-only0112->fourreadbacks->pairedCPUfast/physicalUI.
0111leftGPUOFFpowered0verify1cachedwarm1/42frames18verified0quarantine;
touchON. Swaps70copies66stoppedidle/vsynclive;noHomeagain/Auto-Lockpending.
Sole100435/session31617boot0111-special-live.loguntil~21:27UTC. Goalactive.

ACTIVE0111 hardwarefullreadbackPASS but medianGPU4.100197ms vsCPU1.462235ms.
GPUOFFpowered0verify1cachedwarm1/42frames18verified0fallbackquarantine;
touchON/FWload0A55A. Sole100435/session31617boot0111-special-live.log.
0179four-pixelfullscreen128bytes/15x4/12x400 groups prepared to remove
sixteenpixelstrideandcarry overhead; nativeMesa/primaryv9/actualASanUBSan/
ARM64/profile125PASS. Needcommit/fullCI->exactartifacts/pack0112->BOOT-only
->fourfullreadbacks->pairedCPUfast/physicalUI. Goalactive,nospeedupyet.

ACTIVE0111fullscreen flashedBOOT-onlySUCCESS20:57UTC afterCI44813460343/
8c0fe7c success/exactsixsources/RTCunchanged/reverse0178/checksum/SMP/
actualsourceASanUBSanPASS. Kernel43b71b00...a2eefe/BOOT0a51a5cc...e0bfe4.
Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT. NEWsolecapture/session31617
boot0111-special-live.log waitsCDC. Needclocks/cachedwarm/GPUONverify1/
FWload/touchON->fourfullreadbacks->pairedCPUfast->physicalUI. Nospeedclaim.
0110CPU continued46854+ afterHome BUTPosterBoardcrashloop, so submissions
arenotphysicalUIhealthproof. Sleep hypothesis remains; Auto-Lockreplypending.

ACTIVE20:55UTC CI44813460343/8c0fe7cd24e3042d40cd760a139aa31cf93ef55e
still Build; live20:53:58bsd/skywalk compilation. No duplicate/restart.
NEWsolecapture99894/session67407boot0110-specialwait-live.loguntil~21:24UTC;
old95247deliberatelystopped. GPUOFFpowered0verify1cachedwarm1,41frames/
17verified/0quarantine;touchON5110events0. ONEHome20:38->CPU46854copies by
20:55, no further input. Sleep/Auto-Lock Never user observation pending.
Host0178nativeMesa/primaryv9/actualASanUBSan reruns PASS. Await exactCI
success then privategpu-special-work/artifacts.py+pack0111.py->source/RTC/
checksum/SMP/actualASan->BOOT-only0111->fourfullreadbacks->paired/physicalUI.
Goalactive; no GPU speedup yet. Currenthardwaregeneric16 slowerthanCPU.

ACTIVE20:40UTC CI44813460343 in_progress exact8c0fe7cd24e3042d40cd760a139aa31cf93ef55e
(fullscreen0178). No duplicate/restart. Private gpu-special-work/artifacts.py
and pack0111.py pin run/SHA/sources/RTC. Await fullsuccess then BOOT-only0111,
four fullreadbacks and pairedCPUfast. Host lifecycle/replay/primaryv9/native
Mesa/ARM64/profile124 all PASS. Current0110 GPUOFFpowered0/touchON.

ACTIVE0110 hardware full-frame readback PASS but GPU median4.070764ms vs
CPU1.675600ms (three paired8-copy rounds); generic16 optimization rejected.
GPUOFF/powered0/verify1/cachedwarm1,41frames/17verified/0fallback/quarantine.
20:39UTC ONEHome resumes swaps77->734/copies73->730 (CPU32->689), kernel
UTC correct. Sleep plausible, not proven; controlled Auto-Lock Never asked.
Solecapture95247/session20771boot0110-wide-live.log expires~20:58UTC.
Candidate0178 exactfullscreen384bytes/15x4/16pixels with generic4 fallback;
nativeMesa reproduction/both primaryv9 descriptor paths/ARM64/profile124
PASS. Lifecycle/replay ASanUBSan and benchmark tests PASS; need fullCI->verify/pack0111
->BOOT-only->fourfullreadbacks->pairedCPUfast->physicalUI trial. No speedup
or goal-complete claim. Preserve0110/0109 and all ownership/cache safety.

ACTIVE0110wide flashedBOOT-onlySUCCESS after44804438707/01e7de1 fullCI/
source/checksum/reversepatch/SMP/ASanUBSanPASS. Kernelec18bec3...d73eff/
BOOTe16aec53...bb793; same8cores1984MiB/ADT0094/cmd599/stockramdiskDT.
Solecapture95247/session20771boot0110-wide-live.log waitsCDC. Needclocks/
cachedwarm/GPUONverify1/FWload/touchON->4fullreadbacks->pairedCPUfast3rounds.
No sixteenpixelhardwareclaimyet. Preserve0109restore.

PREVIOUS20:04UTCwideCI44804438707/01e7de1stillBuild(job136524622008);
UPDATE20:13sameCIstillBuild/watch43210/logsBlobNotFound. Newpairedhelper
26a89f1hosttestsPASS;actual0109CPUmedian1.612682ms/GPU2.327408msacross
three8-copyrounds. GPU39/verified7/fallback0/quarantine0;GPUOFFpowered0/
verify1/cachedwarm1/touchON7020slices1096eventsrestored. Goalnotcomplete.

PREVIOUS20:04UTCwideCI44804438707/01e7de1stillBuild(job136524622008);
watch43210. LogsBlobNotFoundNOTjobfailure. Waitsamejob,no duplicate.
NEWsolecapture91908/session21336boot0109-widewait-live.loguntil~20:34UTC;
old81787deliberatelystopped. GPUOFFpowered0verify1/cachedwarm1/touchON.
Benchreplayexactcountcheckebc9559PASS. NeedCI->verify/pack0110->BOOT-only
->cachedwarm4fullreadbacks->alternatingfastCPU. Goalactive.

PREVIOUS0109idle-sleep investigation19:56UTC: userreportsfrozenclockand
suggestssleep. KernelUTCcorrect/GPUOFFpowered0/quarantine0/vsynclive,
swaps62copies57stopped; ONEHome->swaps1290copies1285(CPU1270).
Framebufferdoesnotblankorhandlepowerstate; sleepcouldleaveoldimagevisible.
HypothesisONLY; needdirectsleepstateorAuto-Lockcontrolledtrial. No periodic
Home workaround. WideCI44804438707stillBuild;preservegoal/testsequence.

PREVIOUS0109warmHARDWAREPASSfullpixels;fast2.296msvsCPU1.736. Warm1powered1
NEWwideCI44804438707 exact01e7de1474faf02b8e3c9ee6f9b02c9069929752
active/watch43210;privategpu-wide-work/artifacts.py+pack0110.py pinexact
sources/RTC/SHA/run. NeedfullCI->0110->cachedwarm4fullreadbacks->fastCPU.
0109leftGPUOFFpowered0verify1/cached1/warm1/touchON676slices15events.
Capture81787/session58307soleowneruntil~20:06UTC;revalidatebeforeuse.

PREVIOUS0109warmHARDWAREPASSfullpixels;fast2.296msvsCPU1.736. Warm1powered1
duringcopies,explicitOFFpowered0PASS/noquarantine. GPU15/verified7/fallback0.
LeftGPUOFFverify1/cached1/warm1powered0/touchON. Solecapture81787/58307.
0177sixteenpixels/thread1920bytes32regsTLS0 nativeMesa/v9/ASanUBSan/ARM64/
profile123PASS. NeedfullCI->0110->cachedwarm4readbacks->fastCPU/physicalUI.
Goalactive,nospeedupoverCPUclaim.

PREVIOUS0109warm flashedBOOT-onlySUCCESS after44801549767/6948d5e fullCI/
exactsource/checksum/reversepatch/SMP/ASanUBSanPASS. Kernel8914aba6...eac43f/
BOOT387e4bd0...5e64a1; same8cores1984MiB/ADT0094/cmd599/stockramdiskDT.
Solecapture81787/session58307boot0109-warm-live.log waitsCDC. Needclocks/
cached/warm/GPUONverify1/FWload/touchON->4fullreadbacks->fastCPUtiming/
explicitOFFpowerrelease. No warmhardwareclaimyet.
Privategpu-wide-work16pixels/threadpreparedOFFPROFILE/nativeMesa/v9/
ASanUBSanPASS;useonlyifwarmstillneedsspeed. No wideCIyet.

PREVIOUS0108vectorHARDWAREPASSfullpixels;fast3.542ms(execute1.680)vsCPU1.406.
NEWwarmCI44801549767 exact6948d5ead5fe0dce4d2594ea56e4af96a5b7911e
active/watch43109. Privategpu-warm-work/artifacts.py+pack0109.py pinexact
sources/RTC/SHA/run. NeedfullCI->0109->cachedwarm4fullreadbacks->fastCPU.
Current0108GPUOFFverify1/cached1/touchrestartON;capture76088/session37152
until~19:45UTC. NospeedupoverCPUorGPUphysicalacceptanceclaimyet.

PREVIOUS0108vectorHARDWAREPASSfullpixels;fast3.542ms(execute1.680)vsCPU1.406.
Power+off1.327msoverhead. GPU27/verified19/fallback0/quarantine0;leftGPUOFF/
verify1/cached1. Touchstoppedvalid14after42events,restartONconfirmed.
0176explicitwarmownership(defaultcold)prepared,ASanUBSan/ARM64/profile122
PASS. NeedfullCI->0109->warmcached4fullreadbacks->fastCPU/physicalUI.
Capture76088/session37152soleowner. Goalactive,nospeedupoverCPUyet.

PREVIOUS0108vector flashedBOOT-onlySUCCESS after44794488664/734646c fullCI/
exactsource/checksum/reversepatch/SMP/ASanUBSanPASS. Kernel2f995b2b...25307e/
BOOT2f656a8d...ec6983; same8cores1984MiB/ADT0094/cmd599/stockramdiskDT.
Solecapture76088/session37152boot0108-vector-live.log waitsCDC. Needclocks/
cachedGPUONverify1/FWload/touchON->4fullreadbacks->fastCPUcomparison.
No vectorhardwareclaimyet;0107CPUwakecheckpointretained.

PREVIOUS0107userconfirmsUIworksafterONEHome18:53UTC. GPUalreadyOFF;stale
NEWcapture71717/session74884boot0107-vectorwait-live.loguntil~19:31UTC;
old57854deliberatelystoppedbeforeexpiry. VectorCI44794488664stillBuild
19:01UTC;livejoblogcompiles18:58:59,optionalpatchskiperrorsNOTcompiler
failure. Waitsame40061watch. GPUOFFverify1/cached1/touchON/CPUframesadvance.

PREVIOUS0107userconfirmsUIworksafterONEHome18:53UTC. GPUalreadyOFF;stale
swaps61/copies56->585/580, CPU562/GPU18/quarantine0. TouchON4092slices/
1670events. Homewakeproven,notGPUfreezeetiology/permanentidlefix. Leave
GPUOFFverify1. VectorCI44794488664/734646c stillBuild18:54;watch40061.
Capture57854/session79767until~19:02UTC. NeedvectorCI->0108->cached4
fullreadbacks->fastCPUcomparison->GPUphysicalUIacceptance.

PREVIOUS0107cachedHARDWAREPASS!6fullframeszeroerrors;fast6.170ms vsuncached
NEWvectorCI44794488664 exact734646c9f2f438ccf0417b747600060288829c7f
active/watch40061. Privategpu-vector-work/artifacts.py+pack0108.py pinsource/
RTC/fullSHA/run. NeedfullCI->0108BOOT-only->cached4fullreadbacks->fastCPU.
30sfastlivewindow0copies=>inconclusive;GPUOFFverify1restored. TouchON1099/0
events;capture57854/session79767until~19:02UTC. PhysicalUIstillpending.

PREVIOUS0107cachedHARDWAREPASS!6fullframeszeroerrors;fast6.170ms vsuncached
142.160ms(22x), BUTCPU1.673msstillfaster. GPU18frames/verified10/fallback0/
quarantine0. LeftGPUOFFverify1/cached1/touchON713slices; capture57854/79767.
0175fourpixels/thread128bitvector+scalartails640bytes/32regs prepared;
nativeMesa/v9packers/actualASanUBSan/ARM64/profile121PASS. NeedfullCI->0108
->cached4verifiedfullframes->fastCPUcompare/physicalUI. Goalnotcomplete.

PREVIOUS0107cached flashedBOOT-onlySUCCESS after44791438428/7e56be7 fullCI/
source/checksum/reversepatch/SMP/ASanUBSanPASS. Kernel3628a0c9...74d0dc6/
BOOT44ad2a36...1c37155; same8cores1984MiB/ADT0094/cmd599/stockramdiskDT.
Solecapture57854/session79767boot0107-cache-live.log waitsCDC. Needclocks/
FWload/touchON/explicitcachedGPUONverify1->4fullreadbacks->fastCPUtiming.
Nocachedhardwareclaimyet.0106CPUwakecheckpointretained.

PREVIOUS0106screenfreeze18:20UTC: host/kerneltimeagree1795198810, stale
FOLLOWUP18:26CPUcopies7544,total7564; physicalinputresumesnewframesafter
idlewithoutanotherHome, touchON2585slices277events. GPUstaysOFFframes20.
Notificationsattempt0whileframesadvance=>notsoleprovenfreeze cause.
CachedCI44791438428 stillBuild18:27;watch32994. Bencha708396policylabelsPASS.

PREVIOUS0106screenfreeze18:20UTC: host/kerneltimeagree1795198810, stale
clock/swaps24/copies20. GPUOFF+ONEHome=>687newCPUcopies; userconfirmsclock
updated. LeaveGPUOFF/verify1/touchON. CombinedwakeisnotcausalGPUfixproof.
CachedCI44791438428 exact7e56be7 stillBuild;watch32994. Needexactsuccess
->verify/0107BOOT-only->restoretouch->cached4verifiedframes->fastCPUtiming.
Capture52314/session97698soleowneruntil~18:42UTC. PhysicalGPUUIgatepending.

PREVIOUS BOOT0106HARDWAREPHASES: fastmean142.160ms; execute137.267ms vs
NEWcachedCI44791438428 exact7e56be7f05428c9672d45d93fa357f32a79d20e2
active/watch32994. Privategpu-cache-work/artifacts.py+pack0107.py pinsources/
RTC/fullSHA/run. NeedfullCI->0107BOOT-only->cached4fullreadbacks->fastCPU.
Current0106GPUONverify1/frames20/verified12/fallback0/quarantine0; touchON
987slices12physicalevents+release. Physicalscreenanswerasyncpending.

PREVIOUS BOOT0106HARDWAREPHASES: fastmean142.160ms; execute137.267ms vs
power0.685/prepare0.296/cache0.396/retire0.011/shutdown0.596ms. Fullreadback
PASS6frames. Candidate0174explicitcachedpolicy+freshGPUclean/invalidate
beforeCPU/ASdisable/off;failurequarantine,fourreadbacksperpolicy. Default
uncached. StatefuldirtyDMA/ASanUBSan/ARM64/profile120PASS. NeedfullCI->0107
->cached4verifiedfullframes->fast/CPUcompare. Current0106GPUONverify1/
touchON;capture52314/session97698soleowner. No speedupclaim.

PREVIOUS BOOT0106phase flashedBOOT-onlySUCCESS after44788043452/a59bd6a
fullCI/source/checksum/reversepatch/SMP/ASanUBSanPASS. Kernel881e7b39...b0cdda/
BOOTa4133cfc...6af387; same8cores1984MiB/ADT0094/cmd599/stockramdiskDT.
Solecapture52314/session97698boot0106-phase-live.log waitingCDC. Needclocks/
blitON/FWload/touchON->4verifiedframes->fastreplayphases. Bench65539f9retains
lastphases. SweetCPUidlelatency0=>delaymayblock, awaitingcausalmeasurement.

PREVIOUS BOOT0105tiled HARDWAREPASS full1152000pixels/noerrors; BUTfast
NEWphaseCI44788043452 exacta59bd6a49500d42472d3a62ade7bedb5b68cd7f0
active/watch54706. Privategpu-phase-work/artifacts.py+pack0106.py pinsource/
run/SHA. Waitsamejob->verify->BOOT-only0106->phasebreakdown. Capture49304/
69950expires~18:20UTC;revalidateowner. Goalactive, noaccelerationclaim.

PREVIOUS BOOT0105tiled HARDWAREPASS full1152000pixels/noerrors; BUTfast
138.577/139.407ms vsCPU1.410/1.401ms=>NOspeedup. GPUONverify1/frames33/
verified17/completed33/fallback0/quarantine0;touchON661slices/events0/iohealthy.
RTCautonomous1795197038. NoHome. Solecapture49304/session69950.
0173 lastattemptphase timings prepared/ASanUBSan+ARM64/profile119PASS;
needfullCI->0106->measurebottleneckbeforechangingcache/powerpolicy.

PREVIOUS BOOT0105tiled flashedBOOT-onlySUCCESS after44784844777/3c22c82
fullCI/source/reversepatch/checksum/SMP/ASanUBSanPASS. Kernel8f294f4d...e20e0d,
BOOT40d087fa...954eff. Same8cores1984MiB/ADT0094/cmd599/stockramdiskDT.
Capture49304/session69950boot0105-tiled-live.log waitsCDC; no otherreader.
NeedRTC/status/clocks/blitON/FWload/touchON->4fullframepixelreadbacks->
repeatedfast/CPU/verifytiming. No tiledhardware/speedupclaimyet.0104restorekept.

PREVIOUS CI44784844777 exact3c22c827b79fe88723cbb638439349c3b6af1071
17:47UTC stillBuild; livewatch55345. Do not duplicate/restart. BOOT0104
frames52/verified28/completed52/fallback0/quarantine0/GPUONverify1.
TouchON1530slices0events; physicalacceptanceasyncpending. SolecapturePID46326
session91083until~18:00UTC. Commits3c22c82/91f7fa9/10031ec pushed.

PREVIOUS CI44784844777 exact3c22c827b79fe88723cbb638439349c3b6af1071
Build in progress. Privategpu-tiled-work/artifacts.py+pack0105.py pinexact
run/SHA/source/checksum/reversepatch/unchangedRTC. NeedfullCI->0105trial.
Expanded16x4paddedDMA/replayASanUBSanPASS. No newflash;0104stillGPUONverify1.

PREVIOUS GPU2026-11-20: BOOT0104 replay4 full1152000pixelsPASS. First real
same-frame benchmark8copies: fast139.006ms, CPU1.665ms, verify211.630ms.
No fallback/quarantine; current GPU is slower, goal NOT complete.0172
16x4 bounded tiled shader prepared (18000groups vs1152000); nativeMesa/
v9packers(assertionsON)/ASanUBSan/ARM64/profile118PASS. NeedfullCI->exact
source/artifact->0105BOOT-only->4fullreadbacks->repeatedCPU/fast/verify
measurement->physicalUIacceptance. Capture91083 ownsboot0104-gpu-resume.log
1800seconds from~17:30UTC; revalidate before using. TouchFWload0/A55A,
restartstreamON verified. GPUON/verify1 restored. NoHome/reboot/flash.

PREVIOUS BOOT0104 passed CI44765816216 and flashed to `boot`. XNU read the
SC2730 UTC1795195136 before USB setup. First read-only status1795195137.
No host time correction on 0104. Capture30364 boot0104-rtc-verified.log.
User unplugged restart and physical display confirmation pending.

PREVIOUSCI44765816216 exact44d482d retainedRTC0171 passed full Xcode.
Private0104packerready; neveruseoldHEAD44765753773. HookC/C++linkagePASS.
Needexactartifact/checksum/source->0104BOOT-only->readRTCbeforehostsync.

ACTIVE2026-11-20 clock task: user requires boot-time UTC WITHOUT USB.
Measured UTC553/January1970 at tx1; volatile tx2 host correction1795188867
only a temporary repair.0171 retainedSC2730 RTC ->PEGetUTCTimeOfDay prepared,
independentofconsole/cable. Read-onlyPMIC/noRTCset/alarm/storagewrites.
ActualASanUBSan/ARM64USBcompilePASS; fullXcode/hardwaregatepending.
NeedfullCI->BOOT-only->retainedRTCUTC beforeanyhostsync->cablefreeboot.
IfretainedRTCinvalid, do not claim fixed or inventdate; measureandreassess.
Currentboothasreset; staleGPU/touch/capturestatebelowisnotcurrentevidence.

PREVIOUSCI44632519909 exact7e4ea5b replay0170 nowSUCCESS. Privateexactartifact/
sourceverifier/pack0103ready. BOOT0102now10real2DGPUframes/11520000pixels,
verified10/completed10/fallback0/quarantine0; touchON985slices27physicalevents.
NeedreplayCI->0103->CPU/fast/verify sameframe measurement. Physicalacceptance
stillpending; noFPSclaim. Capture123073/98448. NoHome.

NEXT0170 acceptedcompositorframeboundedreplay1/4/8 forrepeatabletiming.
BOOT0102actual2DfourfullframesPASS verified4/completed4;fullreadbacktotal
836191307ns/last173059846ns. Fast+CPU20sbenchzeroFrames=>INCONCLUSIVE,
GPUON/verify1restored. NoFPS/speedupclaim. TouchON/iohealthy/capture123073.
ReplayhostC++ASanUBSan+GPUregression/ARM64PASS;needfullCI->0103BOOT-only.
ReplaynotphysicalUIproof. Physicalscreenquestionstillpending. NoHome.

FOLLOWUP22:47UTC BOOT0102clocksID90910010/blitON1/verify1;UTC1795128362.
FWload0/A55A/touchONrestored. Timingparserliveallfields;frames0yet,GUIpaging
storageadvances/iohealthy. Await4verified2Dframes->fasttiming. Capture123073/
98448 soleowneruntil~23:15UTC. NoHome/physicalanswerpending.

ACTIVEBOOT0102 flashedBOOT-onlySUCCESS. CI44629497398/44b6f27 verified.
Kernel1609f9aa...5ecb0520;BOOTbe5b980f...d44ce223. Same8cores/1984MiB/cmd599.
Solecapture123073/session98448 waitingCDC. Onceonlyclocks/blitON/UTCqueued
session34294. NeedFWload/touchON/four2Dverifiedframes/fast+CPUtiming/physical
acceptance. No2Dhardwareclaimyet;0101restoreretained. NoHome/otherpartition.

FOLLOWUP22:36UTC physicalswipe18contactevents/downmovementrelease/HID1
confirmed; GPUframesstill4/swaps37, soUIresponseunproven. SB26now17threads/
BB56now13/mainmach_msgwait. CI44629497398/44b6f27stillBuild. Current0101
GPUON/touchON/storagehealthy. Benchmarkhelper+restorationtestscommitted.
Need0102CI->hardware2D/fasttiming;physicalscreenquestionpending.

ACTIVECI44629497398 exact44b6f27 optimized2Dblit0169 running. Native256byte
shaderpreloadR60R61; selectableverify(defaultON)+CPU/GPUtiming. Private
exactfetch/sourceverifier/pack0102ready. NeedfullCIartifact/source/checksum
then0102BOOT-only->clocks/blitON/4verifiedframes/fastmeasure. Keep0101current
GPU4fullframesPASS/CPUfallback28framesPASS/touchON. Physicalstatuspending.
Capture111070/56476 until~22:50UTC,revalidateownerbeforeuse.

NEXT0169 2Dnativeblit256bytes(no per-pixeldivision),fullverifydefaultON,
explicitgpu blit fast skipsreadbackonlyafter4verifiedframes; verify restores.
AlwaysrequireIRQ/header/MMU/retirement. AddedGPUandCPUcopytimingns/counters.
HosttranslatedDMA/primaryMesa/hash/ARM64PASS. NeedfullCI->0102BOOT-only.
Current0101realGPU4frames4608000pixels/fallbackhardwarePASS/touchON retained.
Physicalscreenquestionpending, noFPS/speedupclaim. Capture111070/56476.

FOLLOWUP22:28UTC BOOT0101 realGPUframes4/pixels4608000 allfullreadbackPASS.
CPUfallbackhardwarePASS: blitOFFframes4,copies4->32 afteronebounded swipe;
thenblitONrestoredtx2529. Currentenabled1/frames4/fallback0/quarantine0.
TouchcontinuousON1099+slices/iohealthy/all8. Threeboundedswipesovertrial,
noHome. Physicalscreenquestionpending; noFPS/smoothnessclaim. Keepgoalactive.
Solecapture111070/56476 until~22:50UTC. Currentcheckpoint0101.

ACTIVE22:24UTC BOOT0101 REALIOSurface->PANELGPUBLITPASS! swap1+2 each
1152000pixels/mismatches0/done1/retired1/PASS1. gpu blit frames2/pixels2304000/
fallback0/quarantine0. GUIactual720x1600BGRA/stride3072->panel2880. CPUsource
renderingunchanged;fullreadbackON(noFPSclaim). iohealthy/touchON561slices.
NeedrepeatedactualUIframes/physicalacceptance+fallbackcheck. Asyncphysical
questionpending; noHomeinjection. Capture111070/56476 until~22:50UTC.
Goalactive, basicbackendworksbutcompletionphysicalgatepending.

FOLLOWUP22:23UTC BOOT0101 clocksID90910010/blitON1, frames0/fallback0/
quarantine0. GUI26/56initialthreads waitemmc_strategy page-in; IOadvances
requests4881->8975,notstalled. UTC1795126843 synced;FWload0/A55A; touchON222
slices. Awaitrealframes, physicalstatusasyncpending. NoHome/extrareset.
Solecapture111070/56476. Nohardwareframebufferclaimyet.

ACTIVEBOOT0101flashedBOOT-onlysuccess. CI44625038530/74e1def exactsource+
checksum/SMP/ASanUBSanPASS. Kernel460bfe05...3d1620e/BOOT3825c66c...c7c8d62.
Sameall8/1984MiB/ADT0094/cmd599. Solecapture111070/session56476 waitingCDC.
Onceonlyqueuedclocks/blitON/UTC(session97522). Needruntimepixelreadback/
framecounters,privateFWload/touchON. NoactualframebufferGPUclaimyet.
0100sixcopycheckpointand0099restoresretained. NoHome/otherpartitionwrite.

ACTIVECI44625038530 exact74e1def framebuffer0168 kernel compiling. DefaultGPU
blitOFF; explicit gpu clocks then gpu blit on after0101. Privateexactrun
fetch/sourceverifier/pack0101prepared. NeedfullCIartifact/source/checksum
thenBOOT-onlytrial, actualreadback+repeatedframes andphysicalacceptance.
BOOT0100sixcopyPASS/touchON retained;capture103600 until~22:22UTC.

NEXT0168 guardedIOSurfaceGPUblit candidate staged: atomicowner/allGPU,
serializedswaps/retainedpages/ROsource/validatedpaneldestination/cacheflush/
boundedretirement/fullreadback/CPUfallbackonlyafterretirement. Quarantine
retainssurfaceandsuppressespanelwrites. DefaultOFF, explicitgpu blit on.
ActualsourceASanUBSan/fullrect/strided/failuretestsPASS; native768bytes
shaderreproduces88dab0e0...a4abf382. NeedfullCI(C++Applebuiltinsunavailable
locally), source/artifactchecks->0101BOOT-only hardwareblittrial.
BOOT0100/touchON/capture103600 retained. NoUIaccelerationclaimyet.

ACTIVEBOOT0100 SIXNATIVECOPYTRIALSPASS (tx2,2482..2486):1024words each,
mismatches0/done1/retired1/IRQ2/MMU0/ASfault0/shutdown1/fault0.
UTC1795125218 synced; privateFWload0/readyA55A; touchON1/slices7 tx2487.
ioReady1/poisoned0/all8registered actualticks. Capture103600/session54359
boot0100-gpu-copy-live.log1800s~21:52UTC; revalidatebeforeuse.
CI44620376179/c6b8c85, BOOT54b0ca51...5d62fde4, kernel e3768bd2...a8f58b3.
NextIOSurface->framebufferGPUblit withserializedownership/cache/lifetimes/
retirement+CPUfallback. CurrentframecopiesstillCPU; noUIaccelerationclaim.
NoHome/nootherpartitionwrite. Keep0100/0099/0098/0097checkpoints.

ACTIVEBOOT0100 NATIVECOMPUTECOPYPASS tx2:1024words/mismatches0/PASS1,
submitted1/done1/retired1/IRQ2/MMU0/ASfault0/exception1/coreoff1/fault0.
CI44620376179/c6b8c85verified;BOOT54b0ca51...5d62fde4. BOOT-onlysuccess.
Sameall8/1984MiB/ADT0094/cmd599. iohealthy. UTC/FWrestoreunderway,need
load/startleaveON. Capture103600/54359 soleowner. Noframebufferacceleration
yet; nextrepeatcopythenIOSurfaceblitwithfallback. Keep0099/0098restores.

FOLLOWUP21:42UTC CI44620376179 stillBuild. Addedreproducible --mesa-build
primaryv9descriptorbytecheck; PASS plusnativecopyshaderhashrepeat+2BSDARM64.
BOOT0099touchON656slices/display41swaps36softwarecopies. NoBOOT0100flashyet.
Solecapture97724/4575 retained.

ACTIVE21:38UTC compute CI44620376179/c6b8c852 still Build; prior44617226681
is the completed WRITE_VALUE hardware-PASS build. No duplicateCI.
BOOT0099 firmware nowloaded0/readyA55A; initialvalid15stopped, restart
confirmedstreaming1/slices44. LeaveON. ioReady1/poisoned0, capture97724/4575.
Private0100packer/sourceverifier pinned exactnewrun/SHA. HostcopytestsPASS.
NeedCIartifact/source/checksum->0100BOOT-only gpu clocks/gpu copy ->readback
andretirement, UTC/FW/touchrestore. Nocomputecopy/framebufferclaimyet.

ACTIVEBOOT0099 WRITE_VALUEHARDWAREPASS tx2:submitted1/done1/retired1,
IRQ2/MMU0/ASfault0/exception1/output77ccff003388aaEXACT. CoreoffPASS/fault0.
Notframebufferaccelerationyet. iohealthy/all8/UTCsynced. FWstage15986needs
load/startleaveON;capture97724/4575.0167computeNOWPROFILEafterjobPASS,
localtests/Mesapackermatch/ARM64/113profilePASS. NeedfullCI->0100copytrial.
Keep0099/0098/0097restores;noHome/nootherpartitionwrites.

ACTIVEBOOT0099 correctedv9jobkernel flashedboot-onlySUCCESS;capture4575.
CI44617226681/6c81044verified. Kernele83efc2b...10d62f0c/BOOTac932ced...
d2926c17;all8/1984MiB/ADT0094/cmd599/SMP/reservations/stockramdiskDTPASS.
NeedCDC->gpu clocks->onegpu job->health/UTC/FWload/touchON. Nojobclaimyet.
0167computeNOTPROFILE;0098/0097restoreskept.

FOLLOWUP21:31UTC corrected44617226681 Build/in_progress; keepwatch54365.
Oldcapture82938expiredconfirmed; soleNEWcapture90065 boot0098-jobwait-live.log
until~22:01UTC. TouchcontinuousON5844slices0events; noreload/stop/Home.
Corrected0099packer/sourceverifierready.0167preparedNOTPROFILE. Nojobyet.

FOLLOWUP21:27UTC correctedCI44617226681 stillBuild; watcher54365.
Nativecopygeneratorreproducedvia tools/a03-build-g57-copy-shader.py actual
Mesa24.3compile/linkcommands;SHA565e07d8...0c6814b7 matchesembeddedcode.
0167remainsOFFPROFILE. Needcorrected0166CI->actualWRITE_VALUEtrialfirst.
Capture82938/30907 nearing21:30expiry; revalidateownerbeforeconsoleuse.

FOLLOWUP21:24UTC corrected44617226681/6c81044 Build/in_progress.
0099packer+sourceverifier NOWupdatedcorrectrun/SHA/artifactpaths; earlier
noteaboutOLDpaths superseded. 0167privateG57compute copy PREPAREDNOTPROFILE.
NativeMesa128bytecode/32regs/preloadR60,TLSWLS0;actualv9packermatch+ASan
layout/runtimecorruptionchecks+ARM64PASS. Need0166actualWRITE_VALUEfirst.
0098corecyclecheckpoint/touchON retained;capture82938/30907 until~21:30UTC.

ACTIVECORRECTEDCI44617226681 exact6c810448c1f60e62cee8e8c82262a8e239d8f456.
Supersedes44615378050(pre-v9bit0) BEFOREhardware;cancelrequestedoldrun.
Needexactcorrectedartifact/source/0166reversecheck->0099BOOT-onlygpu job.
Privatepack0099currentlyreferencesOLD44615378050: UPDATE run/SHA/artifact
paths BEFOREuse. Nativecopygenerator tools/a03-g57-copy-shader.c (hostonly)
produces128bytes/TLSWLS0/preloadr60;privateoutputresearch/a03-mesa-24.3.

CORRECTED0166 commit6c81044: G579091=arch9;v9headerbit0RESERVEDzero.
word4now10004not10005;align128. Payload32/40/48unchanged. Earlier v7test
insufficient. Actualv9XML+ASanUBSan+ARM64PASS;CI44615378050supersededbefore
flash. NeedcorrectedCI.0098stillrunning/touchON. NativeMesa compilerbuilt,
128bytecopyshaderdisassembled/TLSWLS0/preloadr60;hardwarecopypending.

ACTIVECI44615378050 exactd5bc9d2 privatejob0166 queued/running.
BOOT0098corepower powered1/shutdown1 VERIFIED;clocksID90910010;nojobyet.
LatesttouchON839slices0events,ioReady1/poisoned0. Capture82938/30907.
NeedexactCI/source/checksum->0099BOOT-only thenclocks/gpu job;restoreUTC/FW/
touchONafterreboot. Goalnotdone:WRITE_VALUEthenactualfill/copy+framebuffer.

NEXT0166privategpu job candidate tested; BOOT0098corecyclePASSretained.
Own32KiB/check4KiBcontiguity/AS0JS1ownership/AArch64tables/cacheflush/
exactresult+IRQ+header;boundedretirement/restoration;quarantineifuncertain,
neverfreependingDMA;activeGPUcommandsblockedafterpoison. NoIOSurfaceyet.
ActualASanUBSan+primaryMesaXML+2BSDARM64+112profilePASS. NeedfullCI then
0099BOOT-only/clocks/gpu cores check/gpu job. TouchON/FWload0A55Arestored.
Capture82938/30907 owns0098log. Preserve0098/0097restores.

ACTIVE21:01UTC BOOT0098 COREPOWER VERIFIED: tx2powered1/shutdown1,
shader1/tiler1/L2=1whileon/PMU08000000;fault0/IRQ700after. Clocks+ID90910010.
NoGPUjob/renderingyet. iohealthy/UTCsynced. FWstaging18079 inprogress,
needload/startleaveON; capture82938/30907. Nextprivatejob0166.

ACTIVEBOOT0098 flashedboot-onlySUCCESS; capture30907 waitingCDC.
CI44610344415/134902f source/checksum/markers/testsPASS. Kernel400e7df6...
047be1c7;BOOTb26ed916...54fdb523;all8/1984MiB/ADT0094/cmd599/SMPPASS.
Nextpassivegpu->gpu clocks->gpu cores exacttx; thenUTC/FWload/touchON.
Noactualcorepower/jobyet.0097clockcheckpoint+0096/0095restoreskept.

FOLLOWUP20:45UTC44610344415 stillBuild/in_progress; watcher34005live.
Private0098pack+sourceverifier gpu-cores-work ready. Sharedjoblayouthosttests
317329d/dd568aa PASS(includingprimaryMesaXML);notstagedinrunningkernel.
Measured9091identifiesG57/TNAxr0p1;vendorr0p1omitsr0p0dummyjob3485WA.
Nojobhardwareyet. ContinuecorepowerCIandtrialfirst;0097clocksretained.

ACTIVECI44610344415 exact134902f corepower0165 queued/running.
BOOT0097 clocks+GPU_ID90910010 VERIFIED; nojob/pixelaccelerationyet.
LatestioReady1/poisoned0;display7swaps5copies/timer17672. TOUCHON495slices.
NeedexactCI/source/checksum->0098sameADT/cmd599/all8/1984MiBBOOT-only,
passivegpu(requireclocks), gpu clocks ifgated, thenexplicitgpu cores cycle.
Keep75107/1149singlecapture;volatileFWrestoreafteranyreboot.

NEXT0165gpu cores candidate prepared/tested; BOOT0097unchanged.
VendorPWRKEY/OVERRIDEthenTILER+L2readythenSHADER120us;20msboundedwaits,
shutdownreverse/overrideonlyafterdrain. ExactID/topology/ownershipguards.
ActualstatefulMMIOASanUBSan+2BSDARM64+111profilePASS. NeedfullCI->0098BOOT
then gpu/passive beforeexplicitgpu cores. Nojobs/accelerationyet.
Latest0097ID90910010persists/leaf11,11,31; touchON495slices0events.
Singlecapture75107/1149 until~21:01UTC. Preserve0097clockcheckpoint/restores.

ACTIVE20:32UTC BOOT0097 GPUCLOCKS+ID VERIFIED! gpu clocks tx1 ID90910010,
status100/shader1/tiler1/L2=1. core10/mem10/sys30->11/11/31; PLLdecode
1535999998Hz;DVFSCGM1003/voltage0;force10102/state07000000unchanged.
NoPMIC/PLL/rate/DVFSwrites; nojobs/pixels/accelerationyet. iohealthy/all8.
UTCsynced/privateFW79104load0/A55A; TOUCHON1/slice1. Capture75107/1149.
Nextvendorcorepowersequence(PWRKEY2968a819/PWROVERRIDE1f01e0078), bounded
readiness/shutdown;thenownedoffscreenjob. Preserve0097/0096/0095 images.

ACTIVE20:30UTC BOOT0097flashSUCCESS boot-only; capture1149 waitingCDC.
CI44606600103 SUCCESS exact5e1a464/source/checksum/markers/hosttestsPASS.
Kernel21f29fb5...c2bfc253;BOOT198c4b15...77d812b. Sameall8/1984MiB/cmd599/
ADT0094/23reservations/SMPtarget103485000/stockramdiskDTPASS.
NextCDCboothealth->gpu clocks exacttransaction->UTC/privateFW/touchON.
Noactualclocks/GPU_ID/jobs yet;0096/0095restores kept. Nootherpartitionwrite.

FOLLOWUP20:20UTC CI44606600103 exact5e1a464 stillBuild/in_progress;
watch94270confirmedlive, noartifacts yet. Actualmux/dividerguardexhaustion
added f6327fe PASS; codeunchangedfromCI. BOOT0096 remainsall8/touchON;
noGPUclockenableyet. Continueexistingrun, donotdispatchduplicate.
Next source/checksum/markers->privatepack0097.py->BOOT-onlytrial->gpu clocks.

CI44606600103 exact5e1a464 (0164clocks) dispatched; use thisrun next.
Latest0096touchON617slices13events; display6swaps/4copies/timer16500.
NoHome/extraGPUwrites/clockenable yet; touchcollection notphysicalUIproof.
Capture54337/69071 boot0096-gpu-power-live.log ownsconsole until~20:39UTC.
0095/0096loader comparePASS after masking expectedImageimage_sizefield;
stockramdisk/DTexactmatch. Firstnaivecomparefailed solelythatheaderfield.

ACTIVE2026-11-19 BOOT0096 running all8/1984MiB; CLOCKSOFF hardwareconfirmed.
gpu power SC2730pd0/vsel140=1V STOP beforewrites; passivecore10/mem10/sys30,
force10102/state07000000/AON2bcac1. NoGPU_ID/job. TouchFWload0/A55A,
continuousHIDON1/slice1;UTCsynced;iohealthy. Capture54337/PID69071.
0164gpu clocks candidate: exactinherited1V/topon/bus+closedgates/ratesguard,
readonlyTWPLLlock+1536MHzdecode, onlyleafbit0writes,400us/domainrecheck/ID,
invalid/mapfailownedgaterollback. NOvoltage/PLL/rate/DVFSwrites.
ActualASanUBSan+2BSDcompiles+110profilePASS. NeedfullCIthen0097BOOTtrial.

ACTIVE2026-11-19 BOOT0096 flashed boot-only SUCCESS; capture54337.
CI44591622019/b8f8f04 verified;BOOTffceaeca...491d754e; exact0094ADT/cmd599/
all8/1984MiB/SMP103485000/23reservations/stockramdiskDTPASS.
NeedCDC/boothealth->UTC/privatefwload/touchstartleaveON->gpu power snapshot.
Noactualpower/clock/GPU_ID/jobsclaim. Restore0095/0094/0093 retained.

ACTIVE2026-11-19 CI44591622019 SUCCESS, exactb8f8f04; artifactsVERIFIED.
KernelSHA25676f967658ff3406d2ca41751640f4fc69e40ef899511e0fcab35affee2aa5d5b.
Checksums/uploaded3sources byte-match/0163reverseapply/linkedGPU+A75+SMP+
displaymarkers/actualASanUBSanPASS. Artifacts ci44591622019-power and
-power-tree/extracted under ignoredshim/a03/out. No0096pack/flash yet.
GoalPAUSED; userfollowup builddone verified only. Onresume pack/validate0096
then BOOT-onlypower/clocktrial. NoGPU_ID/jobs/accelerationclaim.

ACTIVE CI44591622019 exactb8f8f045548a74483757364ed66dfb68ded2f766
is authoritative0163 build (supersedes44591419852). Need successful linked
artifact/SHA256/uploadedsource reverseapply, pack0096 with0094inputADT and
599bytecmdline/all8/1984MiB, stockramdiskDT/SMP/reservations validation,
BOOT-onlytrial then gpu power snapshots. Noactualclocksetup/GPU_IDyet.
Extra test asserts unchanged leaf/GPU/DVFS banks during successfulpreflight.

FOLLOWUP0163: firstCI44591419852 superseded by topDVFS-clock guard followup.
Source liveDT requires AONEB1bit7 before sharedtopDVFS reads. Addedguard+
ASanUBSan coverage; never startsharedCPU/MMvoltagecontroller fordiagnostic.
Read-only0095 baseline18:46UTC sameforce10102/state07000000/AON2bcac1;
touchON1842slices169events, ioReady1/poisoned0. NoHome/flash/reload.
Singlecapture1745 gpu-power-baseline-20261119.log1800s from~18:45UTC.

ACTIVE2026-11-19 POWER/CLOCK-FIRST0163 candidate, per user direction.
Correct0162 C0/top-domain guard; nohardwareGPU_IDclaim. Explicit gpu power
boundedADI rail observation/noPMICwrites, atomicDownload/ADIownership,
topFORCEclear/300us+2000usboundedwait/timeoutrestore, AONbusenable.
Capture inheritedclocks+GPU/topDVFS; NOleafgate/rate/PLL/voltagevote/jobs.
ActualASanUBSan+all3BSD ARM64compiles+USBregressions+109profilestagePASS.
NeedfullCI/link/sourcevalidation->BOOT-onlytrial->actualsnapshots before
choosingclocksetup. Goalstillbasicactualhardwareblit+framebufferintegration.
0095/0094/0093restores retained. docs/a03-gpu.md details; privatefilesignored.

ACTIVE2026-11-19 GPU passive trial0095: CI44409726184 SUCCESS exact15b1445.
Kernel f1cf4a5a...d9ac5e7; BOOT1946fd80...bf9f5b. Checksum/source/markers/
ASanUBSan/SMP/RAM PASS. Lowercase boot flashed100percent; uppercase BOOT
was rejected prewrite, earlydetect also failed.0094/0093 restores retained.
LiveGPUforce00010102/state07000000/AON002bcac1 => core0state7; guardedSTOP,
GPUapertureuntouched. NoGPU_ID/jobs/acceleration. Need validatedpoweron or
separate validatedDMA copy path. All8/1984MiB/iohealthy; initial4swaps/copies.
CapturePID29344/session52219 boot0095-gpu-live.log1800s from~18:32UTC.
UTCsynced18:35:45UTC; private79104fw valid0/load0/A55A. Immediate first
touchstart error-4/allFF stopped; laterstart streaming1/slices7/inputstatus3,
leftON. PhysicalUIunverified; finaldisplay6swaps/4copies/timer18913. NoHome.
XR828x1792 discussion only; resolution remains720x1600. See A03_PROGRESS.md.

ACTIVE2026-11-18 22:29UTC: user reboot/datewrong.0150 WAS committed228642b,
but volatile host sync only, no persistentRTC. LiveUTC439(1970-01-01)
->hostsync1795040955->independentstatussame(2026-11-18 22:29:15UTC).
KernelUTCcorrected; screen/timezone unverified. No flash/Home/touchreload.
Rebootclearedvolatiletouch; notrestored indatefollowup. GPUtask remainsopen.
Need realRTC or explicitautomatic boot source for persistence, notfixeddate.

SCOPE UPDATE2026-11-18: user says most basic acceleration is enough.
Target one real hardware fill/copy then framebuffer blit with CPU fallback;
full Metal/EAGL/composition backend is not required for this milestone.
Still require actual job completion/pixel readback;0162 is diagnostic only.

ACTIVE 2026-11-18 22:15 UTC: A03 GPU user request;0162 passive candidate built locally.
Commit15b1445 / CI44409726184 exact15b144586351eb9855f5cab3c9fb446139080720.
Read-only gpu live-worker command gates PMUforce+auto/core0+top/AON then
APBcore/mem/sys before GPU_ID. NO power writes/jobs/backend/acceleration.
ActualASanUBSan fakeMMIO+BSDcompile+display/SMP+108profile stage PASS.
Running0094 unchanged/touch leftON; latestframe4370/copies4365 stale timeralive.
Need exactCI/source/checksum->BOOT-only passive probe->actualGPU_ID or gate
block evidence. Keep0094/0093 restores. docs/a03-gpu.md maps resources and
remaining real GPU/IOSurface/EAGL integration gates. Do not call this done.

ACTIVE2026-11-18~21:36UTC0094 physicalTOUCHRESPONDSbutVERYSLOW peruser.
OneHome recoveredframes. Freshswap/copies2235/2230->2345/2340 (~10/s)
vs37touchslices*16/~10.98s (~53.9samples/s). Noeventsinsampledinterval;
priorphysicalevents311->427. Inputcollectionnotobviouslydead; endtoend
latency/renderbottlenecknotyetproven. TouchON/all8/A75preference preserved.
PosterBoardcrashloopobserved; no speculativepoll/DVFS/schedulerpatch.
Capture135205/session56612preserve;0093restorekept; performanceissueOPEN.

ACTIVE2026-11-18 21:34:34 UTC0094 TOUCHFAIL report/frame recovery.
Streaming1/1034slices/311events,inputstatus3,physicalhid1 reports present;
swaps52/copy47stale~77s timeralive. OneexplicitHome result0 ->58/53->116/111.
Physicaltouchreports continue; no reload/stop/reboot/flash. TOUCHON; A75ON.
Physicalswipeconfirmationpending viaasyncquestion; no permanentfixclaim.
PosterBoardcrashloopobserved/causeunknown; SB26/backboardd56present.
Capture135205/session56612existing boot0094-usb-initial.log preserveowner.
Nextframe/touchfollowupanduserreply; no periodicHome;0093restorekept.

FOLLOWUP21:29:38UTC0094 all8usageadvances/A75dominant; touchON1/189slices/0events.
Display swaps/copiesstill0 in startup; nophysicalGUI/speedupclaim. Preserve
singlecapture135205 and waitforuserphysicalscreenreply, notautomaticHome.

ACTIVE2026-11-18~21:29UTC0094A75PREFERENCE RUNNING.
BOOT-onlyflash57520success; policyrequested1/all8initSGI/CPU_ONrc0PASS.
Real~10sdelta A756user5/sys577,A757user7/sys532;90.7%busy onA75s,
all8positiveuser/system. A55physicalbootstrap unchanged; no speedupbenchmark.
UTCsynced/privatefw79104valid0/load0/A55A; TOUCHON1/56slices/events0.
VM97823free/compressor0/ioReady1poisoned0; SB26+backboardd56 present,
initialswap0/copy0 startup. Physicalscreenquestionpending; noGUIclaimyet.
SinglecapturePID135205/session56612 live boot0094-usb-initial.log3600s.
CI44398834193/exact661d5bb;BOOTddb03bf3...33047aa7. Keep0093/0092/0090.

ACTIVE2026-11-18~21:26UTC0094A75BOOT-onlyflash57520 INPROGRESS.
CI44398834193SUCCESS/exact661d5bb/source/checksum/markersPASS.
BOOTddb03bf3...33047aa7/kernelabfaf10a...5533c382. Exact0093ADT/all8/1984MiB,
cmd599 remove startup_debug=1 append a03_prefer_a75=1. PhysicalbootstrapA55
unchanged. SyncedDownload thenHeimdalldetectPASS (firstattempttooearly/no write).
Singlecapture56612 waits120s then3600s boot0094-usb-initial.log. Needresult/
policy1/all8initSGI then UTC/privatefwload/touchstartleaveON/usagedeltas/VMio.
No runtime/speedupclaim; keep0093/0092/0090restores.

ACTIVE2026-11-18 A75 CI44398834193 exact661d5bb RUNNING.
Local exact-CI sched_prim.c compilePASS, selector262144mask sanitizerPASS.
0094 private inputADT=0093 exact; cmd599bytes remove startup_debug=1 then
append a03_prefer_a75=1 (naive append overflows608 ABI). Sameall8/1984MiB.
Fresh0093 all8usage and swaps27394/copies27388; no reboot/flash yet.
Singlecapture session87084 writes boot0093-before-a75.log for3600seconds.
Next exactCI/checksum/linkedmarker/source->0094BOOT-only->restore touchON,
cpus deltas/display/VM/io and userphysical response. Keep0093/0092/0090.

ACTIVE2026-11-18 A75-FIRST candidate0161 prepared per user request.
Opt-in a03_prefer_a75=1 prefers idle CPU6 then7 before last-CPU affinity;
A55 fallback/all8 remain available; RT/bound work and physical A55 bootstrap
unchanged. Exact0093 tree patch/reverse+actual selector262144 masks ASan/UBSan
PASS; SMP ADT regression/profile107 PASS. Full CI/link then0094 same0093
ADT/root/1984MiB/cpus8 plus new arg, BOOT-only test and cpus deltas needed.
No runtime activation/speedup claim. Keep0093/0092/0090 restores and touchON.

ACTIVE 2026-11-18 ~21:07 UTC: BOOT0093 frame-update recovery VERIFIED.
Idle follow-up: no Home or USB swipe injected. Physical gestures resumed
swaps7051/copies7045 ->7175/7169 ->8736/8730. User explicitly confirms
"Swipe responds and clock is current" after idle without pressing a button.
Earlier one Home event recovered original incident. No permanent code fix
or original cause claimed; no build/reboot/flash needed. All8/1984MiB/touchON
preserved; final streaming1/11849slices/4728events, io ready1/poisoned0.
Single capture PID109369 remains live, expires~21:44UTC; bounded watch done.
Goal runtime/physical acceptance met. If recurrence, inspect activity/timers
and stale scanout; do not use periodic synthetic Home as a purported fix.

ACTIVE 2026-11-18 ~21:02 UTC: BOOT0093 physical UI recovered, no flash.
One explicit HID Home restarted swaps/copies (40/34 -> 6428/6422).
User confirms screen changed, then physical touch responds and clock advances.
All eight cores/1984 MiB and continuous touch forwarding stay enabled.
No rebuild/reboot/partition write. Notification attempts remain 0 while real
frames advance; missing VBL registration is not a sufficient root cause.
Primary EAGLServer CADisplayTimer null during stall, non-null after Home;
sleep/wake/activity mismatch is a hypothesis, no permanent repair claim.
Capture PID109369/host1272 expires ~21:44 UTC; bounded watch host14536
records /tmp/a03-frame-watch.log. Bounded check done: frames resumed after
a ~50second quiet interval, then another swipe produced frames. Physical
touch/clock confirmed. Incident recovered; no persistent kernel fix or
guaranteed idle/wake reliability. Investigate activity/sleep if it recurs.

ACTIVEFRAMEGOAL2026-11-18~20:50UTC0093sameall8/touchON/no reset.
Singlecapture1272 boot0093-frame-repair-live3600s. Importantcorrection:
CADeviceUseVBL=0 livebackboardd =>CADisplayTimer fallback. Kernelnotif0not
alonecause.72ABI matches20A362. Tracefallbacktimers/actualserverstate next;
no speculativeforcedpresent. Goalactive fixactualnewframes+physicalUI.

ACTIVE2026-11-18~20:16UTC0093userLOCKSCREENclock12:11FROZEN.
KernelUTC20:15:26->45advances/all8usagepositive/SB25+backboardd56alive.
DISPLAYvsync33647->34662done, swap40/copies34STUCK~3.5min; notifyattempts0,
skips24859->25875 => callbackunset OR portnull, exactwhichunknown.
Timerworks/no newframes; notfixproof. FreezeDEFERRED, no newbuild/flash.
TOUCHON1592slices/434events; vmcompressor0/iohealthy. No touchstop/reboot.
Capture97574/32555until~20:26UTC. Keepall8/1984MiB;0092/0090restorekept.

ACTIVE2026-11-18~20:08UTC0093ALL8running+realuser/kernelusageticks.
A756user12/sys179,A757user13/sys105; allA55alsoadvance;CPU0heaviest.
Privatefw79104stagedvalid0/load0/A55A; TOUCHON1/2slices/events0, bothHIDopen/
inputstatus3. LeaveON. VM/iohealthy/98312free/compressor0. SB25still1thread
startup; noGUI/speedupclaim; userphysicalreplypending. Singlecapture32555
boot0093-usb-initialuntil~20:26UTC. Freezedeferred;noextraflash/0092+0090kept.

ACTIVE2026-11-18~20:07UTC0093 ALL8CORESINIT+USAGEPROVEN. CPU1..7
CPU_ONrc0/initSGIinclA756/7; CPU0OK.8registered/twosnapshotsall8positive
user/systemticks(A756:+1/+14,A757:+1/+11). CPU0dominant; notcapacityaware.
VM/iohealthy/SB25stillstartup. UTCsynced. Privatefwstaging10055inprogress,
needload/A55A/touchstartleaveON. Singlecapture32555 until~20:26UTC.
NoGUI/stability/speedupclaim. Freezedeferred;0092/0090restorekept.

ACTIVE2026-11-18~20:05UTC0093ALL8 BOOT-onlyflash64645 INPROGRESS.
44381915946SUCCESS/exact3cf8d51/checksum/SMPusageA75matching/sourcePASS.
BOOTe3c29209...85149831/kernelf2ad4098...82a6e63e; cpus8(6A55+2A75),
1984MiB/same0092root/lowtrampoline0x103485000target. No8coreclaimyet.
Nextflashresult->singlecapture CPU_ON/initSGI all8->cpususagedeltas,
UTC/privatefwload/touchstartleaveON/VMio. Freezedeferred.0092/0090restorekept.

ACTIVE2026-11-18~19:37UTC PHONEINDOWNLOAD confirmedHeimdalldetect.
Useraskedresetwhilewaiting;0092serial/EP0time replied1795030581 thenexplicit
CDCDownloadrequest/disconnect; initialdetectearlyfails thenPASS. NOFLASH.
Awaitall8CI44381915946/exact3cf8d51->0093all8/1984MiB/lowtrampoline.
Volatiletouchfirmwareclearedbyreboot; reload/start after nextBOOT.0092/0090kept.

ACTIVE19:35UTC ALL8fullCI44381915946 exact3cf8d51 submitted/mac26intel,
a03/SWEET/userspacetrue/buildtreetrue. Supersedesfreeze-only44381013070.
Next0093=cpus8+8realCPUADT/1984MiB/lowtrampoline; newA75match+cpususageprobe.
Needexactsuccess/source/linkedmarkers/checksum thenBOOT-onlytest; notflashed.

ACTIVEUSERDIRECTION2026-11-18 NEXT0093ALL8CORES; FREEZEDEFERRED.
6A55MPIDR0..500+2A75600/700/cpus8/1984MiB/same0092lowtrampoline/root.
0160addsA75IOKitmatch+readonlycpusrecountticks toproveworkdistribution.
CurrentsecondA55normalXNU schedulerregistered (notparked); no usage%measured.
ADT8/liveDT/types/extensionseed+CPU0/1preserved/hosttestsPASS.0093inputADT
stagedprivate; fullCI next, notflashed. Linuxprocessor.ccompileApplebuiltin
blocked; do not claimfullcompile.0159mayremainpassive butnofreezeblocker.
Preserve0092/0090restores/touchON; no newphoneI/O thisturn.

ACTIVE19:29UTC displaydiagnosticfullCI44381013070 exactc6b9a55 RUNNING,
macos26intel/a03/SWEET/userspacetrue/buildtreetrue.0159probesvsync/notify/
swap/copy, notfix. Same0092stillrunning/frozenimage/touchON. Nextexactsuccess
artifacts/source/markers->0093same2A55/1984MiB/lowtrampoline. Noautoflash.

ACTIVE2026-11-18~19:30UTC0092IMAGEFROZEN peruser, kernelUTCadvances,
SB26/backboardd56CPUadvances/mainCFRunLoop, HIDONevents138->201. NoSBcrash/
OOM/compressor; storagehealthy. DoNOTcallstableGUI. No reboot/touchstop.
0159readonlydisplayprogressprobe prepared/testPASS; fullCI next. Needvsync/
notify/swap/copycounters tolocatestall;16cappedoldswaplogsnotconclusive.
Singlecapture83709/58347 boot0092-usb-initial until~19:33UTC; verifyowner.
NextfullCI->same2A55/1984MiB/trampoline0093diagnostics, noA75trialyet.

ACTIVE2026-11-18~19:23UTC USERCONFIRMS SpringBoardUP on0092twoA55/1984MiB.
FreshSB26/19threads/changedstack; TOUCHON1/757slices/events0,bothHIDopen.
VM37237free/compressor0/ioReady1poisoned0. No capturedSBcrash/panic boundedlog.
Preserve0092 firstmulticorevisibleGUI checkpoint; noflash/reboot/touchstop.
Singlecapture83709/host58347 boot0092-usb-initial until~19:33UTC; preserveowner.
Needuserresponsiveness/physicalgestureevidence; A75trialseparate/notstarted.
0090singleCPUrestore retained. No measuredspeedup or A75/allcoreclaim.

ACTIVE2026-11-18~19:20UTC BOOT0092 TWOA55init/SGIverified/1984MiB.
Privatefw79104stagedvalid0/load0/A55A; TOUCHSTREAMON1/42slices/events0,
leaveON/no timedstop. SB26sample1threadstillstartup, noGUIreadyclaim.
VM108106free/compressor0/ioReady1poisoned0. UTC1795029580syncedvolatile
(correcttimeSECONDSsyntax; initialtime set rejected). Singlecapture58347
boot0092-usb-initial900s until~19:33UTC; preserveowner. NeedUIreadiness/
HIDclientopens/physicalresponse and laterA75trial; no newflash requirednow.
0090restore retained; BOOT0092=9dda3af2...0639c4fc/fullCI44375549972.

ACTIVE2026-11-18~19:19UTC0092 TWOA55SUCCESS: CPU_ONrc0 via0x80081000;
cpu1MPIDR100 EL1init+SGI1OK; cpu0SGI1OK/final2CPUinitialized. UserbootingUSB.
VM/io/pslive, launchd/SB26starts, compressor0/ioReady1poisoned0. NotA75/allcores
or measuredGUI speedup. Singlecapture58347 boot0092-usb-initial900s(~19:33UTC).
Privatefwstaging11918 inprogress; needstagevalid0->touchload/A55A->touchstart
leaveON thenVM/io/SBsample/UI. Noautoflash.0090restore retained.

ACTIVE2026-11-18 BOOT0092trampolineflash36454 INPROGRESS/BOOTonly.
FullCI44375549972 SUCCESS/exact87f1b0e/checksum/5SMPmarkers/actualsourcePASS.
BOOT9dda3af2...0639c4fc/kernelbb831647...02dabbb. Same2A55/1984MiB/args/
ADTseed+onlychosenhandoff; lowshim ->high0x103485000. Stockramdisk/DTsame.
HostDownload/detectPASS. Nextflashresult->singlecapture CPU_ON/coreSGItimer
proof; UTC/privatefwload/touchstart/VMio/UI. Preserve0090restore/noSMPclaimyet.

ACTIVE18:59UTC0158fullCI44375549972 exact87f1b0e RUNNING/mac26intel.
CandidateBOOTramtrampoline+XNUconsumer/mandatorymarker included. Needexact
success/source/markers/checksum before0092 --smp-kernel packaging/BOOTtest.
Phone0091panicrc-9; preserve0090restore; noadditionalphoneI/O thisturn.

ACTIVE2026-11-18 BOOT0091panic exactcpu1 CPU_ON rc=-9 (INVALID_ADDRESS).
SecondaryPA0x103481000 >4GiB; firmwareentryrange rejectionlikely/unprovenlimit.
0158 lowtrampoline insideexistingretainedBOOTshim prepared, notarbitraryRAM.
Packer --smp-kernel verifiesexactpayload/symbol; loaderboundedhandoff; XNU
validateslowentry/target. Hostparser/loader/patchtestsPASS; fullCI next.
No hardwarefixclaim; phone0091panic/noCDC, touchnotrestored. Preserve0090.
DO NOTFLASH a03-trampoline-host-test.img (old0157kernel/packagingtestonly).
NextfreshfullCI->0092 twoA55/1984MiB with--smp-kernel->BOOT-onlymanualDownload.

ACTIVE2026-11-18 18:54UTC0091 BOOTflashSUCCESS, noCDC after120s.
Heimdall95543 upload100/success/reboot~18:51; singlecapture7441 exited
noenumeration. Usersees BOOTTEXT/ERROR; exactlastlines requested/pending.
DO NOTCLAIMSMP: noCPU_ON/coreinit/SGI/timerlog. No newreset/reflash since.
Touch/fw notrestored on0091 (USB unavailable), no touchstop command sent.
Need exactscreenerror before fix.0090 oneCPU/1984MiB restore retained.
0091BOOT14b9de7c...ca26a7a/kernelc133c3ea...4e698c6/fullCI44367277857.

ACTIVE2026-11-18~18:52UTC0091-smp2 BOOT-onlyflash95543 INPROGRESS.
44367277857 SUCCESS/exact91ca41a; checksum/4SMPmarkers/actualsource PASS.
BOOT14b9de7c...ca26a7a kernelc133c3ea...4e698c6.2A55/cpus2/1984MiB,
0090ADT+CPU1only,argscpus2only,loaderexceptsize/stockramdisk/DTsame.
UsermanualDownload confirmedhost04e8685d/detect afterUSBtimeout.
Nextflashresult->singlecapture/CPU_ON+2coreSGItimerproof/UTC/fwload/
touchstart/VMio/UI. Preserve0090restore. NoSMP runtimeclaimyet.

ACTIVE18:13UTC correctedSMPfullCI44367277857 exact91ca41a RUNNING,
macos-26-intel/a03/SWEET/userspacetrue/buildtreetrue. MandatorySMPmarkers
nowgateartifact. No0091/no flash; verifyexactsuccess/source/markers/checksum
before2A55trial.0090restore retained. Prior44357697720 kernelREJECTED.

ACTIVE2026-11-18~18:15UTC green44357697720 REJECTED:0157skipped!
Artifactkernel1ef6b6b4...6254 checksumPASS but noSMPmarkers; actualsource
singleCPU. BuildwarnedSweetCPU.cpp37 patchnotapply; no0091image/no flash.
Rootcause localbaseline0009 CPU diagnosticprefix vs CI CPU.0157 corrected
againstactualuploadedsource/gitapply+reverse+structuralPASS. NewlinkedSMP
validator+CIgate rejectsactualbadkernel/missingmarkers. FreshfullCI next.
Pretestttycapture ended, EP0reportednotconnected; no touchstop/reset/write.
Lastverified0090=1984MiB/cpus1/TOUCHON; preserve restore.

ACTIVE2026-11-18 17:21UTC SMPbuild44352036471 failedRUNNERALLOCATION.
Checkannotation: jobnotacquiredbyhostedrunner; zero steps/no compilation.
Replacement44357697720 dispatchedmacos-26-intel/a03/SWEET/userspacetrue/
buildtreetrue exact73b554a (same0157 asb6a3a15, docs-onlylaterchanges).
Needfullbuild/artifacts; noSMPsuccessclaim/noautoflash. No phoneI/O thisturn;
lastverified0090=1984MiB/cpus1/TOUCHON. Preserve0090restore.

ACTIVE2026-11-18~16:51UTC SMPfullCI44352036471 exactb6a3a15 QUEUED.
Supersedes44351323590cancelled. SecondaryVPIDR/VMPIDR nowexplicit; assembly
compile+actualpatch/ADTtestsPASS. NoSMPautoflash. Current0090=1984MiB/1CPU,
VM41986free16KiBpages/compressor0/iohealthy/SB25alive. TOUCHON1243slices/
0events; leaveON. Singlecapture16666/21134expires~16:51; verifyownerbefore
nextreader. Userphysicalspeedreplypending. NextfullCI exactsuccess ->
2A55trial/1984MiB/BOOT-only, preserve0090restore, reloadfw/starttouch.

ACTIVE16:49UTC fullSMP CI44351323590 exact71436b1 QUEUED/mac15intel.
Additionalcpu.c retargetedMachCI compilePASS, notexactperfile.
Current0090=1984MiB/1CPU/TOUCHON. Noautoflash scheduled.

ACTIVE2026-11-18~16:48UTC0157 opt-inSMP candidate ready for fullXcodeCI.
Localexact machine_routines/start assembly PASS; C++Applebuiltinblocked;
actualcpu.c exactcommand missing. ADT1/2/6A55 guards+gitapply PASS.
Firsttrial2A55, retain0090RAM config. Current0090 stillcpus1/1984MiB,
TOUCHON632slices/events0; SB25/24threads; compressor0. Capture21134.
NoSMPsuccessclaim. NeedfullCI thenchecksum/package/BOOTtest.

ACTIVE2026-11-18~16:45UTC BOOT0090 1984MiB RAM hardware boot/VM PASS.
Exact0089 kernel+args; BOOT293de28b...90f1a; cpus1. VM free117024 then94424
16KiBpages/compressor0; storage ready1 poisoned0. Singlecapture21134
boot0090-usb-initial.log600s (~16:50UTC deadline). Privatefw79104 stagedvalid0/
load0/A55A; bothHIDopen; TOUCHSTREAMON verified1/slices2/events0. LeaveON.
Prior0089 freshly rebooted beforetest; causeunknown.0089/0088restorekept.
Multicore0157 candidate being validated separately; noSMPsuccessclaim.
FullRAM requires lowerbank reservationholes;1984MiB is safeupperwindow.

ACTIVE2026-11-18~16:35UTC USERREQUEST LEAVE TOUCH ENABLED. BOOT0089
STREAMON verified974slices/38events after SIGTERM hosttimedPID12128; no
finally-stop/no kernelstop sent; no timedHIDhelperremains. Firmwareloaded.
Do NOT stop forwarding merely to end session. Reboot stillrequiresfwload/start.
PhysicalSettings tap->animation/Preferences283 proven; blackSettingscontent
and3physicalhomebarswipes/noresponse alsoobserved. NoCAclientcreate/abort
captured;0156specificpathunproven. Capture93357 onlyttyreader until~17:20UTC.
Preserve0088restore; no newflash needed for current userrequest.

ACTIVE2026-11-18~16:31UTC BOOT0089 FIRST physicaltap->Settings animation
userconfirmed; stream5events/twotruecontacts+HIDdown/up; Preferences283
launched, SB26alive. Settingscontentblack/homebar; scrollingnotproven.
Preferences12threads/mainCFRunLoop/GSEvent/UIApplication. NoCAclientWI
diagnostic/abortyet, so0156specificcreationstillunproven. HID600s11069
ONuntil~16:39UTC; useraskedphysicalhomebarswipe, replypending.
Capture93357 boot0089-usb-initial.log active; fwloaded. No newflash.

ACTIVE2026-11-18~16:24UTC BOOT0089 CDC/capture93357 ACTIVE, UTCsynced
16:21:00. Private79104fw stagedvalid0/load0/A55A/config720x1600 PASS.
BothHIDclientsopen/inputstatus3. Logonlyidle10s30slices/events0/stopPASS.
SB26 stillstartup1thread dyld/libobjc/libdispatch; normalbackboarddWI0/0.
STREAMOFF, noHIDgestureyet. AwaitUI/startupeventloop then CAclient/result
and visiblegesturetest. Userpostflashscreenquestionpending.

ACTIVE2026-11-18~16:20UTC BOOT0089 flashed successfully using lowercase
heimdall --boot. CI44192146474 SUCCESS exactfd1fc5e; artifact/checksum,
unchanged0088ADT/1GiB/bootargs/loader-except-size PASS. Kernelb316c806...bf14,
BOOTd897364f...c999c. Uppercase --BOOT first rejected BEFOREupload, then
corrected. Singlecapture hostsession93357 waitingCDC, log
shim/a03/out/boot0089-usb-initial.log, host log boot0089-capture-host.log.
Need UTC/privatefwstage+load/inputstatus -> actualWIflags/error/kr on swipe,
physicalvisibleUI.0156fixnotyetproven.0088restore retained. STREAMOFF.

ACTIVE22:40UTC0156fullCI44192146474 exactfd1fc5e RUNNING. Package-only
/tmp/a03-0089/package.py gatesexactSUCCESS/checksums/same0088config.
Noautoflash. Current0088STREAMOFF; physicalswipe reachesUIKit but denied
CAclientflags30000000EPERMbeforeallocation. Need0089runtimeappcheck/result
and visibleUI. Source/testscommitted; nofixclaimyet.

ACTIVE22:40UTC0088 SECONDswipe15events -> WIflags30000000/error1EPERM/
kr8NOACCESS, sameSBabort/user spinner. ExactprivilegedbranchBEFOREcreate,
notENOMEM. STREAMOFF130slices15events.0156implicitCAclientpermissioncandidate
preserveskernelapp/noGROUP/singleWI/lifecyclechecks;8192tests/reversePASS.
NeedfullCI0089 thenBOOT-only/UTC/fwload/oneswipe WIresult. Capture141846
boot0088-usb-initial until~23:09UTC.0155alonefailed; noUIworkingclaim.

ACTIVE22:38UTC0088 visibleiOSconfirmed. FirstHID60s178slices18events/
oneswipe noUIresponse; noSBcrash/noSBWIcreate. MainwaitAudioToolbox AU
registration thenresolvedbacktomainloop~22:37. SECONDHID90s14155 NOWON
/tmp/a03-0088/stream-after-audio-wait.log, useroneswipeasked; inspectWIlogs/
UIreply. CapturePID141846 until~23:09UTC; UTC/fwloaded.0155fixunproven.

ACTIVE22:32UTC0088BOOT-onlyflashSUCCESS. SinglecapturePID141846/
41773 boot0088-usb-initial.log until~23:09UTC. UTCsynced22:29:46, fw79104
valid0/load0/all7CRC/A55A/configPASS. UserstillApplelogo/bootlogs22:31.
STREAMOFF0slices/events0. SB25/inputstatus3/bothclientsopen. WIhardware
backboarddflags20000000/error0/kr0 (normalprivilegedpathPASS). CAclient
fixnotyettested. sample25queued; waitmainloop+physicalUI thenalignedswipe.

ACTIVE22:28UTC0155CI44186495805 SUCCESS/exact47a92b3.0088 checksum/
marker/same0087configPASS; BOOT1e3309cb...696f3/kernel245542b4...cdab2.
PhonealreadyDownload04e8:685d/detectPASS; CDCsenderdidnotconnect (cause
oftransitionunknown). AuthorizedBOOT-onlyflash17164 /tmp/a03-0088/flash.log
running. Nextsinglecapture UTC/fwstage/load WIlogs physicalswipe. NoUI fix
claim yet.0087 physicalHIDreachesUIKit thenWIabort; restore0087/0086kept.

ACTIVE22:13UTC0087 userclock2:03stale~9min. KernelUTCstatus22:12:54
advancing; replacementSpringBoard1079/24threads/mainloopalive. Wholephone
notfrozen; displayedGUIstale. STREAMOFF.0155CI44186495805 stillBuild,
packagePID134153/host29898 waiting0088. SinglecapturePID134536 writes
boot0087-usb-after-swipe-crash.log until~22:37UTC. NeedWI candidate runtime
flags/error/kr and repeatgesture/UI; nofixclaimyet.

ACTIVE22:09UTC0087 touch reachesUIKit eventFetcher/UIQOSProcessingBegin
then explicitWIexception/SIGABRT6. No capturedOOMkill, but actualcreateerrno
notyetknown; donotclaimRAMruledout. User's lag acceptable, spinner confirmed
crash.0155CI44186495805 Build; package29898 /tmp/a03-0088/package.py waits.
STREAMOFF. Oldcapture128605 finished; NEWsinglecapture32643 writes
boot0087-usb-after-swipe-crash.log. NextfullCI->0088BOOTonly->UTC/fwload->
alignedswipe, inspectWIflags/error/kr and userUIresponse.

ACTIVE22:05UTC0155CI44186495805 exact47a92b3 dispatched/mac15intel.
CandidateCcompilePASS(retargeted existingconsoleCIflags, not exactperfile),
8192policycases/reversePASS. Package-only /tmp/a03-0088/package.py gates
exactSUCCESS/checksum/WImarker/same0087config; noautoflash. Current0087
STREAMOFF; physicalHID4swipes61events -> SBabort workinterval/user spinner.
Capture128605 expires~22:06UTC; rotateonlyafterverifiedexit. Neednext0088
actualCREATE2flags/error/kr +repeatgesture, no provenfixyet.

ACTIVE22:06UTC0087 physicalHID61events/fourswipes reached; user sees
spinner, logsSpringBoard26abort Failedtocreateworkinterval. STREAMOFF.
0155candidate documentedUNRESTRICTED default/coreaudio/CAclient privilege
policy +boundedcreateflags/error/kr logs; nofake success. SB lacks entitlement.
Tests8192casesPASS; kernelC compilecheck inprogress36298. NeedfullCI0088,
thenBOOT-only/restagefw/retestgesture. Capture128605 near expiry~22:06UTC.

ACTIVE21:55UTC0087 HID600s COMPLETE/CLEANSTOP1761slices/28176frames/
0events; statusstreaming0. NoHIDphysicaleventarrived. STREAMOFF; do not
restart/reflash to chase idle evidence. Needusergesture+visibleUIreply;
physicaldown/movement/28truelifts alreadyproven logonly. Firmwareloaded,
SpringBoard26 mainloopalive. CapturePID128605 until~22:06UTC; preserve
single-reader discipline if it expires. Current0087 restore0086 retained.

ACTIVE21:48UTC0087 currentSpringBoard26 mainloopverified cache38858000
(machmsg/CFRunLoop/GSEvent/UIApplication/SBSystemAppMain). HID600s hostPID
130376/session44699 live until~21:55UTC. Status246slices/events0, noerrors.
Prior physicaldown/move/28ups proven logonly. ActualHID/UI needs usergesture
and pendingvisible-response reply. CapturePID128605 until~22:06UTC. No new
firmware/reboot/flash needed. Do not count idle0events as a dispatch failure.

ACTIVE21:45UTC0087 HID LONGWINDOW ON for600s/autostop~21:55UTC,
session44699 /tmp/a03-0087/stream-hid-long-window.log. Physicaldown/move/
28trueupsproven logonly361slices/341events; firstHID120s350slices/events0
(nocontactsarrived). ActualHIDdelivery/UI stillpending user gestures/reply.
CapturePID128605 until~22:06. No reboot/fwreloadneeded; source0154 deployed.
Check livewindowbefore changing commands; use streamstatus/stop ifneeded.

ACTIVE21:43UTC0087 TRUE PHYSICAL LIFT PROVEN: logonly120s361slices/
341events;25upalreadylogged whileactive238slices; stopadds0events. Noerrors.
HIDphysical120s session98064 NOWRUNNING /tmp/a03-0087/stream-physical-hid.log.
User asked swipe/tap visibleUI; responsepending. Needinspect HIDevents then
UIreply. CapturePID128605 until~22:06UTC. Firmwareloaded; noflashneeded.

ACTIVE21:40UTC0087 continuous HIDidle10s PASS:33slicesactive->34stopped,
544frames/events0/noerror. Logonly30s85slices1360framesalsoPASS. STREAMOFF.
Physical user screen/readiness replypending; need real down/move/up then
visibleUI. CapturePID128605 until~22:06UTC; firmwarealreadyloaded/A55A.
Next timedcontacts30s aligneduser then timedHID UI. No moreflash needed now.

ACTIVE21:40UTC0087 flashedBOOT-onlySUCCESS. CapturePID128605 live.
UTC1794951400/privatefw79104valid0/load0/all7CRC/A55A/configPASS.
CONTINUOUS logonly30s hardwarePASS:84slicesactive->85stop=1360frames,
events0/noerror. BothHIDclientsopen.10sHIDidle session7908 running; inspect
/tmp/a03-0087/stream-hid-idle.log next. Physical screen/readiness replypending.
Need truephysicalup/HID/UI; no touch successclaim.0086restore preserved.

ACTIVE21:35UTC0154CI44178262587 SUCCESS/exact10b9f9b.0087 packaged/
checksum+markers+same0086config verified; BOOTb893cd32...85a25/kernel
f1709990...a0df. SyncedCDC Download+Heimdall detectPASS. BOOT-onlyflash49418
/tmp/a03-0087/flash.log inprogress. Nextsinglecapture UTC/fwload/startcontacts
physicalup thenHID/UI.0086 restore kept; user physicalalignment reply pending.

ACTIVE21:29UTC0154CI44178262587 exact10b9f9b RUNNING Build step since
21:25UTC (not queued anymore). PackagePID124809 waits exactsuccess0087,
noautodeploy. Current0086 capturePID122914 until~21:38UTC. HIDidle2483
300valid/events0/hid1; actual HID event delivery stillunverified. Timedhost
controls3b61053 pushed/testsPASS; physical user-held/lift/screen reply pending.
Next checkCI/package -> BOOT-only0087 -> UTC/privatefwload -> startcontacts
for physicalup -> HID visible response. Do not claim touch usable yet.

ACTIVE21:24UTC0086 FIRST HID-ENABLED IDLE poll2483 result0/valid300/
events0/hid1, no actual events forwarded. Physical lift/HID/UI stillpending.
0154CI44178262587 queued; packagePID124809 live. Added timed host helper
(a03-usb-touch-stream.py) logonlydefault, exactACK, finally-stop; testsPASS.
Current0086 lacks stream commands; no start sent. User alignment pending.

ACTIVE21:22UTC0086 SpringBoard main loop measured(sample25/symbolicated
cache slide2AA5C000: CFRunLoop/GSEventRunModal/UIApplication/SBSystemAppMain).
BothHIDclientsopen/inputstatus3; touch HID stillneverrun. Secondidle300valid/
0events.0154CI44178262587 queued; packagePID124809 /tmp/a03-0087/package.py
live, noautoflash. CapturePID122914 until~21:38. User heldfinger/screen reply
pending; do not treat old ready as current. Continuous source10b9f9b tested.

ACTIVE21:18UTC0154 fullCI44178262587 exact10b9f9b queued/mac15intel.
Package-only /tmp/a03-0087/package.py gates exactSUCCESS/checksum/markers/
same0086 configuration; noautoflash.0086 remainscurrent/idlezeroevents;
physical lift/HID/UI pending. User heldfinger/screen reply stillpending.

ACTIVE21:19UTC0154 prepared explicit continuous startcontacts/start/stop/
streamstatus on serialized worker,16frame slices preserve heldstate, failure
releases/stops; noautoload. Poll+command ASan/UBSan/kernelC/reversePASS.
Not deployed.0086 idleclean; user heldfinger/screen reply pending. No HID
poll sent. Next fullCI then0087; keep0086 physical baseline available.

ACTIVE21:14UTC0086 inputstatus3/bothHIDclientsopen. Poll C/C++ ASan/UBSan
regression proves count0/statusFF release at sample2 beforecleanup, no extra
up. Hardware idle0events proven; user heldfinger/screen reply pending.
No HID poll sent. CapturePID122914 until~21:38UTC. Docs refreshed; b5e1331.

ACTIVE21:12UTC0086 BOOT-only flash SUCCESS, capturePID122914. UTC synced
1794949748; privatefw79104 validation0/load0/all7CRC/A55A/configPASS.
0153 HARDWARE IDLE FIX PROVEN: log-only300valid/events0/hid0; raw0000FF+
57zero. Physicaldown/motion priorproven; true lift/HID/UI stillpending.
No touch poll yet. Align heldfinger->physical lift next. Singlecapture0086.

ACTIVE21:07UTC0153CI44173996698 SUCCESS/exact8963305.0086 packaged
same0085 config/BOOT221de96d...8126/kernel81d48ecf...1ba6. SyncedDownload
+detected; BOOTflash67897 /tmp/a03-0086/flash.log. Nextcapture/UTC/fwload/
idle+lift/HID. Physicalmotion proven0085, noHID/UI yet. Preserve0084/0085.

ACTIVE20:57UTC0085 PHYSICAL MOVEMENT confirmed: aligned userdrag, TWO
300frame log-only sessions valid300/events301 each, changing slot0x/y,
rawcount1/otherFFFF. No HID. Physical lift stillpending0153(count0fix).
CI44173996698 exact8963305 building/package70851 waits0086. Single43981.

ACTIVE20:54UTC0153CI44173996698 exact8963305 running; package-only70851
/tmp/a03-0086/package.py gates0086 same0085. Current0085 log-only: idle count0
packet0000FF+57zero falsely corners; NEVER touch poll until0153. First physical
heldcenter332,805 on0084 proven. Need lift/move/HID/UI; single43981.

ACTIVE20:53UTC0085 current. UTC synced/fwload0/A55A. Raw idle exactly
0000FF +57zero bytes/count0 -> phantom10corners in0152; NO HID poll sent.
0153 staged count0=no contacts, sparse positive counts retained; tests/
kernelC/applyPASS. Need fullCI0086 then physicalmotion/lift/HID/UI. Physical
center332,805 on0084 proven. Single43981 capture until~21:20UTC.

ACTIVE20:49UTC0084 FIRST PHYSICAL COORD: aligned heldcenter -> slot0
332,805,300samples/result0/finalcleanupup. Physical lift not proven; nextidle
again tenzero slots. NO HID poll.0152CI44169153500 SUCCESS/exactddf4129,
0085 packaged same0084/BOOT2fb6c42e...41a1c. CDC Download3389 requested.
Next detect->BOOTflash->singlecapture->UTC/fwload->rawidle/finger->HID.

ACTIVE20:27UTC0084 user PHYSICALLY CONFIRMS console overwrite FIXED:
iOS picture stays visible; USB logging remains live. Finger test done but
no convincing coordinates (capture overlap unmeasured); no HID poll sent.
0152CI44169153500 exactddf4129 building/package48253 waits0085. Single4287.

ACTIVE20:27UTC0152CI44169153500 exactddf4129 running/mac15intel; package
only48253 gates0085 same0084 config +rawpacket marker. No auto flash.0084
UTC advancing, SB logs now2026-11-17. TWO contact log sessions allzero-like
ten(0,0) slots -> NO HID poll. Pending user finger/screen/overlay answers.
Single4287 capture until~20:51UTC. Earlier0083CI44162912240 still running.

ACTIVE20:25UTC0084 UTC sync/status advancing2026-11-17 works. fw reupload
valid0/load0/A55A/configPASS. contacts2478/2479 log-only tenzero slots ->
NOT physical touch; NO HID poll sent.0152 now staged rejectallzero + each-
frame enter/read/exit+raw3packetlogs; tests/applyPASS, compile97018 result.
User finger-test +screen/overlay questions pending. Single4287 capture.

ACTIVE20:20UTC0084 (0149poll+0150UTC+0151console) CI44165152625 SUCCESS
exactd6800e4, package verified BOOT79ef8571...6fb4/kernel f92711ec...9e27.
SyncedDownload detected; BOOT flash49731 /tmp/a03-0084/flash.log underway.
Next single capture -> UTC sync -> restage fw/load -> contacts -> HID UI.
0082 load0/A55A/home checkpoint kept. No physical contacts proven yet.

ACTIVE20:04UTC0151 staged/fullCI44165152625 exactd6800e4 macos15intel
(separate pool/no cancellation), package63708 waits0084 same0082 baseline.
Earlier0149+0150CI44162912240/mac26 builds; package68041 waits0083. Current
0082 running RAMfwA55A, home reported but console overlay. Single23880.

ACTIVE20:03UTC0082 HOME ICONS visible afterHome2483, but user corrects:
boot logs overwrite SpringBoard between refreshes.0151 prepared fbcon draw
gate after USB append + validatedGUI ownership. Gate tests/C compile/apply
PASS; framebufferCPP blocked known Apple builtins/fullXcode pending. NOT
staged.0149+0150CI44162912240 still builds/package68041; no contact proof.

ACTIVE20:00UTC0082 PHYSICAL CLOCK confirmed after touch firmware load0/
A55A. Sample2482 main event loop proven. One USB Home sent, response pending.
Physical contacts still untested:0149+0150CI44162912240 builds, package68041.
Single23880 capture through~20:21UTC. Preserve0080 and0082 checkpoints.

ACTIVE19:58UTC0082 user logs confirm1969-12-31 16:06 UTC-8-style epoch
date;0150UTC pendingCI. SB sample2481 progresses glyph rendering. Repeat
touch sections2480 stillA55A/config/report PASS after SPI restore. Physical
screen last bootlogs; no Home/swipe.0149+0150CI44162912240 building.

ACTIVE19:55UTC0082 user sees briefApplelogo then boot logs (NOT clock/home).
SB25/bbd56 alive; sample2479 main waits libMobileGestalt semaphore, startup.
Touch RAM load0/readyA55A/config PASS separate from display. No input sent.
CI44162912240 (0149poll+0150UTC) running; package68041. Single23880 capture.

ACTIVE19:54UTC0082 TOUCH FIRMWARE RUNNING. Private79104 upload valid0,
explicit load2477 result0(all7HWCRC pass), readyA55A/config20002AD4/1028/
report20011580/60/720x1600/18x32. Exit0/gate+clock restored/END. NO contact
poll in0082. Single23880 capture; user screen question pending.0149+0150CI
44162912240 exactda42e57 building, package68041 waits0083. Next verified
0083 flash/restage/load -> contacts log -> HID -> physical UI; UTC sync.

ACTIVE19:51UTC0082 flashed BOOT-only100percent/success/reboot. Single23880
capture waits180/1800s boot0082-usb-initial.log. USB not yet; no commands.
Next ROM/sections -> private upload79104+valid0 -> explicit touch load.
0149+0150CI44162912240 exactda42e57 running, package-only68041 gates0083.
Phone date remains wrong pending0150; no firmware upload/load yet.

ACTIVE19:50UTC0148CI44159557034 SUCCESS exactcdafbe1.0082 packaged verified
same0081 config, BOOT1d034092...afce1. CDC synced Download detected; BOOT-only
flash88171 in progress /tmp/a03-0082/flash.log. No firmware uploaded yet.
0149+0150 now staged for next CI; current0082 has loader only. Preserve0080.

ACTIVE19:48UTC user reports wrong4:19/December31. Platform base UTC source
returns0/no RTC override.0150 explicit volatile UTC status/set+host sender
prepared tests/compile/apply PASS, NOT staged/deployed; phone time unchanged.
0148CI44159557034 exactcdafbe1 still building/package91490 waits.0149 ready
but not staged.0081 clock physically visible; single23025 until20:01UTC.

ACTIVE19:43UTC0149 bounded polling now sleeps whole-ms delays; compile,
actual callback delay/dispatch tests and reverse/plain equality PASS. Still
NOT staged in profile. Candidate offlineconfig720x1600/18x32 confirmed.
0148CI44159557034 still running/package91490 waits; no0082/no upload/load.
0081 physical clock confirmed; freshio ready1/poisoned0, reader23025.

ACTIVE19:38UTC0081 CLOCK physically confirmed. Single reader23025 until
~20:01UTC boot0081-touch-followup.log.0149 explicit contacts/log vs poll/HID
prepared+tested+compile/apply equality PASS; NOT staged in build profile.
0148CI44159557034 exactcdafbe1 still building; package91490 gates0082,
NO auto flash. No firmware uploaded/loaded, no physical contacts verified.
Next verified0082 BOOT-only trial -> private staging -> explicit RAM load.

ACTIVE19:35UTC bounded poll helper prepared+unstaged/tests PASS. Requires
ROM+ready/config, max300frames,3failed read stop/final releases; no HID yet.
0148CI44159557034 exactcdafbe1 running/package91490 waits.0081 ROM good/
notready2317; no firmware upload. Capture84861 ends~19:35, check before
new reader. Physical screen question pending.0080 home checkpoint kept.

ACTIVE19:32UTC0148 full CI44159557034 exactcdafbe19909f1b4b99a1523d57c5dd48957dc24a
queued/running. Package-only91490 /tmp/a03-0082/package.py waits exact success/
checksum/markers/same0081 config0082; NO auto deployment.0081 fresh io ready1
poisoned0; current-screen question pending. ROM9383 good, ERAM2317 not-ready.
Single84861 capture ends~19:35; extend after end. No firmware uploaded yet.

ACTIVE19:33UTC0148 explicit RAM-only loader prepared+staged, compile/tests/
apply equality PASS. No CI yet. EP0 fwbegin/fwdata/fwstatus stages80KiB max;
separate load requires all moves/CRC+ROM then stock RAM sequence+HW CRC,
onlyDMA3/no externalflash. Source helpers and upload sender tracked, NO bin.
0081 ROM9383+ERAM2317(notready); firmware not uploaded. Single84861 until
~19:35UTC. Next full CI/package0082 then explicit staged RAM trial.

ACTIVE19:28UTC0081 sections1: ROM9383 PASS, ERAM ready2317!=A55A,
config refused, exit0/restored gate0A02DE00 clock0/END. No firmware loaded.
Need source-guided bounded RAM-only firmware load+section/report path.
Private rev8 CPT candidate CRC7 valid but rev5 match unproven. Current
single84861 capture until~19:35UTC.0080home+ROM restore kept.

ACTIVE19:26UTC0081 flashed BOOT-only success/reboot.0147CI44154963110 exact
7972a72 SUCCESS; kernel71d6e2ce...27e4 BOOT4e5fbb3a...3caa. Same0080 config.
Single capture84861 waits180s/480s boot0081-usb-initial.log (/tmp/a03-0081).
Next worker ready->ONE explicit touch sections; inspect ROM/ready/config/
restoration. NO firmware upload/reset/pinmux.0080 home+ROM checkpoint kept.

ACTIVE19:22UTC0080 reader26068 completed normally. New single reader99340
boot0080-touch-followup2.log600s (/tmp/a03-0080/followup2.log). Home icons
physically confirmed; ROM9383 PASS.0147CI44154963110 remains Build;
package-only63480 exact7972a72 waits. No0081 image/flash yet.

ACTIVE19:18UTC pre-write C firmware validator prepared+unstaged; all source/
RAM/overlap/CRC/command checks before writes. C/C++ ASan tests+private7moves
PASS. No hardware upload/firmware embedded.0147CI44154963110 building,
package63480 waiting.0080 home+ROM9383 good; reader26068 until19:21.

ACTIVE19:16UTC RAM-only transport helper prepared+unstaged with strict
PRAM/DRAM writes, read-only ERAM,240byte chunks. Actual C/C++ ASan tests PASS.
NO hardware RAM operation/firmware upload yet.0147CI44154963110 building;
package63480 waits exact7972a72.0080 home/ROM confirmed; reader26068.

ACTIVE19:14UTC0080 PHYSICAL HOME ICONS confirmed after USB Home9.
ROM9383/probe restoration and visible home both verified on current image.
Physical touch still pending.0147CI44154963110 exact7972a72 building;
package-only63480 waits. Reader26068 single followup. No new input pending.

ACTIVE19:13UTC0080 user confirms physical clock. ONE USB Home sent; response
pending. ROM9383 confirmed earlier. Contact-state failure policy prepared/
unstaged+ASan tests PASS; not physical driver.0147CI44154963110 running,
package63480 waits; single reader26068 followup until~19:21UTC.

ACTIVE19:11UTC0080 follow-up single reader26068 now600s after initial ended.
shim/a03/out/boot0080-touch-followup.log (/tmp/a03-0080/followup.log).
Fresh io ready1/poisoned0, SB25 still app event loop. User current-screen
question pending (last logo19:07).0147CI44154963110 building; watcher63480.

ACTIVE19:09UTC0080 SB25 now event loop GSEventRunModal/UIApplication/SBMain
(cache slide1F994000). User last saw logo19:07; new screen question pending.
No input after reboot.0147CI44154963110 exact7972a72 building; package-only
watcher63480 /tmp/a03-0081/package.py gates success+same0080 config0081.
NO automatic flash. Current capture2205 ends~19:11:42; extend only after ends.

ACTIVE19:06UTC0147 full CI44154963110 exact7972a72ff7122185158e973762eeab7a76c237af
queued macos-26-intel/SWEET/a03/userspace, upload_buildtree=false. Do NOT
duplicate. No0081 packaged yet.0080 touch ROM9383 PASS; preserve checkpoint.
Physical current-screen question pending; no Home/swipe sent after reboot.

ACTIVE0147 touch sections prepared+staged: ROM-gated fixedERAM160byte read,
validated config pointer only. No reset/firmware/contact events. Exact kernel
C compile+actual-session ASan/UBSan tests+apply equality PASS. Need full CI.
0080 ROM9383 already confirmed, restored controls, storage ready1 poisoned0;
both HID clients opened. Single capture2205 remains. Physical touch pending.

ACTIVE19:04UTC0080 HARDWARE ROM9383 PASS. touch status1 gate0A02DE00/clock0;
touch rom2 result0/id9383/raw8A/sts2AA/restored gate+clock exact/END.
SPI3 inherited pins/reset/CS0/1MHz works. No firmware/reset/pinmux write.
Next explicit ERAM section readiness/config/contact read patch0147; no
physical touch proof. Single capture2205 until~19:11UTC; outputs/tmp/a03-0080.

ACTIVE2026-11-17~19:02UTC BOOT0080 flashed BOOT-only successful/reboot.
CI44150337660 exact542f9b5 SUCCESS, kernel5828529d...88e3 BOOT35ca7403...c5f9.
Same0079 config/ADT/loader/ramdisk/DT; no firmware/new arg. Single capture
/tmp/a03-0080/capture.log->shim/a03/out/boot0080-usb-initial.log waits180s,
480s capture. Next USB worker ready->touch status then ONE touch rom;
inspect exact ID/restoration/health. No ROM yet.0079/0078 restore retained.

ACTIVE~18:53UTC prepared standalone section decoder+actual-header C/C++
ASan/UBSan tests PASS; NOT staged/no bus or firmware operations. Fresh0079
status3/SpringBoard25/backboardd56 alive/storage ready1 poisoned0; other
daemon crashes persist.0146CI44150337660 still Build. Package-only watcher
76572 waits exact542f9b5 success then checksum/markers/same0079 config0080;
NO automatic deployment. Script/log/tmp/a03-0080; no duplicate watcher.

ACTIVE2026-11-17~18:45UTC0146 CI44150337660 exact542f9b5 Building.
Offline rev8 CPT firmware extracted privately;79104bytes SHA8ba14e32...a82d,
7move-section CRCs pass. Installed revision5 compatibility NOT established;
NO controller upload/phone write. New offline inspector+synthetic tests PASS.
Next full CI success->verify exact artifact/package0080 same0079 config->
BOOT-only test explicit touch status then ROM. Running0079 home preserved.

ACTIVE0146 explicit touch status|rom prepared+staged. Bounded SPI3/1MHz
Jadard ROM9383 probe only; no reset/pinmux/firmware/external-flash operations.
Clock/control restoration, busy refusal; follow stock hardwareCS0 despite
logicalCS1 node. Actual helper+probe ASan/UBSan tests PASS; exact CI C compiles
usb_console+sweet_amfi PASS; reverse/plain apply equality PASS. Need full CI
then same0079 config BOOT0080, explicit status then ROM, inspect result.
0079 home menu preserved for now; physical touch remains unimplemented.

ACTIVE2026-11-17~18:23UTC0079 PHYSICAL HOME MENU after explicit USB Home.
User finger swipe inert(no physical driver); ready-screen USB swipe22 also
no visible reaction. Then USB Home23 Menu0x40 down/up1client/result0/END;
user immediately "now it went to the home menu". Positive button/UI evidence,
NOT physical touch or digitizer delivery proof. Preserve running0079 and
0078clock restore; no reset/flash this turn. Current single capture33166
boot0079-input-ready.log180s ends~18:25UTC. Fresh ps/io requested.
Next physical Jadard SPI3/ROM/CPT RAM-firmware/section/report driver;
see docs/a03-touch.md. USB swipe policy/queue acceptance still unresolved.

ACTIVE18:19UTC0079 SpringBoard25 main now GSEventRunModal/UIApplication
_run/UIApplicationMain/SBSystemAppMain (cache slide09450000), framebuffer
swaps19; io ready1/poisoned0. User earlier reported Apple logo during first
swipe; no visible reaction proven. New screen confirmation pending BEFORE
another gesture. No reset. Capture52487 remains live until~18:22UTC.

ACTIVE18:16UTC0079: both HID services opened successfully by user clients;
backboardd56 now8threads. ONE explicit swipeup down360,1560/up360,460
result0/END after opens. Dispatch proof only; UI reaction/consumption/unlock
unverified. SpringBoard25 last sample1thread startup; user screen+reaction
questions pending. Do not claim physical touch works or auto-repeat gesture.
Single capture52487 remains boot0079-usb-initial.log, ends~18:22UTC.

ACTIVE2026-11-17 18:13UTC BOOT0079 HID trial flashed successfully via
heimdall --boot only after synced CDC Download. CI43969089570 exact2d4ffd7;
kernel1960b8a7...705e9a, BOOT97f50f70...f17aea. Exact0078 ADT/1GiB/loader
(except image_size)/stockramdisk/DT; only+a03_hid=1.0078 has no RAMDisk;
actual USERDATA-root setup preserved. Capture52487 waits180 then480s,
shim/a03/out/boot0079-usb-initial.log (stdout/tmp/a03-0079/capture.txt).
USB returned18:14UTC: buttons+touch registered, input status3 confirmed.
Backboardd56 startup1to3threads/SpringBoard25; no client open yet18:15UTC.
Need actual HID client open BEFORE explicit swipe, then user
physical response. No gesture yet.0078 restore retained. Physical touch
hardware preparation separate: docs/a03-touch.md; decoder tests pass.

ACTIVE2026-11-17 TOUCH: saved Android evidence selects Jadard JD9365T/CPT,
SPI3@20150000/CS1/10MHz; stock zero-flash RAM firmware required path.
Standalone unstaged60byte contact decoder+C/C++ASan/UBSan PASS; existing HID
tests PASS. See docs/a03-touch.md. Exact0145CI43969089570/2d4ffd7 SUCCESS
2026-11-16T22:42:24Z. No0079 manifest locally, old/tmp0079 watchers absent.
Neither A03/Samsung USB currently enumerates; NO flash/reset/input this turn.
Next reconnect/identify kernel, verify HID/client+explicit swipe, then physical
SPI/ROM/RAM-firmware/report path. Clock checkpoint0078 retained; touch and
unlocked home unverified. Older ACTIVE entries below are historical.

ACTIVE22:29UTC0078 fresh SB26 main remains application event loop;
backboardd56/analytics91 alive, io ready1/poisoned0. Physical clock confirmed,
no unlocked home/touch proof. Short45s capture59755 ends before gated0079.
0145CI43969089570 exact2d4ffd7 Build22:28; existing0079package48074/deploy34846/
scheduler54018 retained. No gesture automatically; inspect HID/client first.
Local compiler helper now supports exact C++/IOKit/libkern command replay;
regression PASS, Apple builtin baseline limitations explicitly reported.

ACTIVE0079 deployment34846 now scheduled behind exact0145CI43969089570
success+package48074/checksum/same0078 config only+a03_hid=1. No flash yet.
Status/read-only scheduler54018 waits worker, NO gesture automatically.
Need HID service registration/backboard client open, then bounded Home/swipe
and physical result. Current0078 capture ended normally, image preserved.
Added actual touch ASan tests+sender/docs; no Home screen/input proof.
CI exact2d4ffd7 in Build22:27. Keep watchers, no duplicate build/readers.

ACTIVE0145 CI43969089570 exact2d4ffd7a44eab34178a13295b0ad3a337044e453
building22:20UTC; package-only48074 /tmp/a03-0079/watch-package.py gates
exact success/checksum/markers, adds only+a03_hid=1 (598bytes). No deployment
or reset scheduled: preserve0078 physical iOS clock checkpoint. New input
status/home/swipeup available only after0145 build+flash; not current phone.
0143 staged with0145;0144vault NOT staged. Current followup28890/PID214760.
SB26 eventloop, analytics91/activation467 recent ps alive. ScreenTime vault45.
Need CI then runtime HID registration/client open/input and physical home proof.

ACTIVE0145 USB HID input prepared+staged(defaultoff), no CI/flash yet.
Portable donor queue/services only, no hardware touch. input status/home/
swipeup exact bounded worker actions;720x1600.0143 creds staged too;0144 lab
vault NOT staged. Host actual action ASan+full C helper compile+full C++
syntax checks with HOST-ONLY Apple builtin shim PASS; no clean exact C++
claim.0145 source equality/plain apply/reverse PASS. Need full Xcode CI.
0078 remains clock UI/event loop, followup28890 single reader240s. Analytics91
alive; activation now467(no crash evidence); ScreenTime vault45 confirmed.
User swipe question pending. No home/unlock proof, no new reset scheduled.

ACTIVE0078~22:10 SB26 main now GSEventRunModal/UIApplication _run/
UIApplicationMain/SBSystemAppMain: application event loop, physical clock
reported. Unlock/home/input still unverified; swipe question pending.
No new reset. Reader206943 live, analytics91/activation134/ScreenTime121
retain PIDs.0144 lab vault candidate committed NOT staged/enabled.

ACTIVE0078~22:09UTC USER SEES iOS CLOCK (first UI beyond logo). Preserve
running phone; no new reboot scheduled. Home/unlock/touch not yet verified;
async swipe question pending. SB26 progresses Biome→IconServices→UILabel→
Gestalt/HMF;720x1600 swaps6–19. Fresh ps analytics91/mobileactivation134
survive, actual runloop samples, prior fatal access failures absent so far.
Same ACL metadata includingLibrary000;0142 enabled. ScreenTime121 CoreData
loading; dmd vault45 persists. Reader206943/43872 and probes89317 retained.
Optional0144 lab vault metadata helper locally tested NOT staged or enabled;
0143 likewise. Goal remains actual unlocked home screen.

ACTIVE0078 BOOT-only upload successful/reboot22:03UTC after exact0142
CI43963988043 success. Kernel90d84532d5acc3b5731bf568106e91c1ba7de95863efcecea2b659f3a3913ef9;
BOOT5e84e96c22d10a195ebcd593df9a5a21434fe62ac0e8fe36739a9c7d0894761b.
Only+a03_compat_uuid=1; unchanged1GiB/root/ADT. Existing43872 readerPID206943
waitsUSB180 then660s; scheduler89317 retained. No USB return at22:04UTC.
Need fresh ps repeated analytics/activation survival and SB stack.0143 creds
probe prepared NOT included. Vault remains separate. Home goal unverified.

ACTIVE22:01UTC0142 CI43963988043 exact1e206d5 still Build. Existing0078
package32985/deploy43872/probes89317 retained;0077 capture ended normally.
No0078 flash yet. Need actual analytics/activation survival and SB sample.
ScreenTime live vault directory501:501/0755/flags0/noACL; matching library
requires0x104 plus UF_DATAVAULT and com.apple.rootless owner xattr. Added
read-only ABI regression+docs/a03-service-crashes.md; all checks PASS.
No fake success/vault implementation.0143 creds diagnostic prepared/tested,
not staged/currentCI. No home screen; goal remains active.

ACTIVE0142 CI43963988043 exact1e206d5f8695d0a393de9b0d1e45cc1c57d17759
building21:50UTC.0078 package32985/deploy43872/ACL scheduler89317 retained:
/tmp/a03-0078/{watch-package,deploy,schedule-probes}.py. Gates exact success,
checksum/same0077 config, only+a03_compat_uuid=1(588bytes), old reader end;
then synced Download, BOOT-only0078 flash/capture660s. NO0078 flash yet.
0077 reader47410 and ACL43860 remain. Live actual group299 permit ACEs
confirmed; candidate fixes translation only, preserve groups/rights.
ScreenTime missing data-vault API remains separate. No home screen verified.

ACTIVE0077 actual ACL confirmed21:49UTC: activation+OSAnalytics roots
2 permits group compatUUID...012b(systemusers299), Library inherited permit
same299 rights3ffe flags71. Library mode000 intentional ACL; NO chmod.
0142 now staged/defaultoff for NEXT CI; helper ASan+kernel-functions compile
PASS; full file Apple builtins baseline limitation. Need exact fullCI then
0078 same config plusa03_compat_uuid=1; actual runtime group grants still test.
0077 reader47410/ACL43860 live. ScreenTime vault ENOTSUP separate; home unproven.

ACTIVE0077 BOOT-only upload successful/reboot confirmed21:47UTC after
verified0141 CI43961834933. Existing reader47410 waitsUSB180s then660s
boot0077-usb-initial.log; ACL scheduler43860 retained. No new USB evidence yet.
Need actual activation/OSAnalytics ACLs;0142 local UUID candidate NOT staged.
No root/protected partition changes. Home screen goal unverified.

ACTIVE0141 CI43961834933 exactbd84c3b SUCCESS21:46UTC. Verified0077
BOOT2db3ebac42ac32bc2c0d941368dc921ae432218c7449aab76505b14757118826,
kerneld6c024750fff02fab0060e100d0ad07a5cfa4198447e152b8604639fd341d015.
Deploy47410 started synced Download after0076 reader ended; flash pending
at21:46:53UTC. ACL scheduler43860 retained, package53238 finished.
0142 identity candidate helper+4wrappers exact kernel flags compile PASS;
full credential file baseline/candidate same73 Apple builtins errors. NOT
staged/enabled; needs0077 ACL evidence. Home screen still unproven.

ACTIVE0142 identity UUID candidate prepared+committed, NOT staged/enabled.
Helper Clang ASan/UBSan/apply equality PASS; full credential compile blocked
by unchanged73 Apple builtins errors (baseline=candidate). Needs actual0141
ACL evidence first.0141 CI43961834933 exactbd84c3b still Build21:45UTC;
0077 package53238/deploy47410/ACL43860 retained.0076 capture ended normally.
Do not duplicate watchers. No home screen; SB26 last activation XPC wait.

ACTIVE0076~21:39 SB26 NOW activation wait (MadGate), past MC checkIn;
tccd37/profiled100 alive. Library -2:-2/000 repeated. CONFIG_EXT_RESOLVER
actually enabled but staged launchd no memberd/opendirectoryd; fail-closed
GUID ACL evaluation plausible, pending actual0141 ACLs. No permission bypass.
Existing0141 CI43961834933/package53238/deploy47410/probe43860 retained;
no0077 flash.0076 reader84806/stat86888 remain. Home unproven.

ACTIVE0076 live stat: activation container0:0/0755 flags0; OSAnalytics
SystemGroup0:0/0755 flags0, Library -2:-2/000 flags0. Mount1480d000 excludes
NOUSERXATTR. ACL dependence possible; MCM uses systemusers299 inclmobile/
analyticsd. No chmod/bypass. ScreenTime exact vault45 repeats; analytics
EACCES/NULL repeats. SB26 currently MC checkIn; no home-screen proof.
0141 CI43961834933 exactbd84c3b building.0077 package53238/deploy47410/
ACL scheduler43860 retained. Deployment waits exact success+package+0076
reader end then BOOT-only flash. NO0077 flash yet.0076 reader84806 live.
0076 stat scheduler86888 corrected101byte CoreAnalytics path to parent-only.
Need actual ACL/GUID access repair. Private logs ignored; no root mutation.

ACTIVE0076 BOOT-only upload successful/reboot confirmed21:33UTC after
exact0140 CI43959202597 success+unchanged config verification. Reader84806
now waitsUSB180s then660s capture boot0076-usb-initial.log; stat scheduler51114
retained. No USB runtime evidence yet. Need live modes/owners of analytics
and activation paths, then root-cause repair.0141 tested ACL next-build only.
Home screen unproven; no root/protected partition writes.

ACTIVE0076 CI43959202597 exact65cc580 SUCCESS21:32UTC; package verified,
BOOT SHA5b24a68639cc0df952e3b8cc51c6aed5069d9a396a22b4a17f831b2b4b9ff353,
kernelbb342c79786b5f605c54544a4350021e9a2138177530a7818b80773e156bc78a.
Deploy84806 waiting short0075 status reader82251 (60s ends~21:33), then synced
Download/BOOT-only upload. Stat scheduler51114 retained. No0076 flash yet.
0075~21:32 sample25 still activation XPC, VM free2616/compressor2474pages,
storage ready1 poisoned0.0141 ACL inspection prepared/tested NOT0076.
Home menu remains unproven. Do not duplicate readers/watchers.

ACTIVE0141 ACL probe prepared for NEXT build, NOT0076. Actual helper
ASan/UBSan + full sweet_amfi.c exact Clang + plain apply equality PASS.
Regular stat unaffected; acl prints bounded16 ACEs and frees allocation.
0075 fresh sample25 21:26UTC confirms MadGate getActivationState wait;
activation EACCES blocker again. Initial capture ended normally.
Existing0140 CI43959202597 exact65cc580 still building21:31UTC, package57048,
deploy84806 and stat scheduler51114 retained. No0076 flash yet. No duplicate
CI/readers; inspect0076 uid/gid/mode/flags before repair. Home unproven.

ACTIVE0075 ScreenTime terminating assertion now captured twice: Failed to
 enable data vault: Operation not supported (45), Sandbox0x104 fd3 owner
remotemanagementd. Analytics actual Library/CoreAnalytics stat/open EACCES13
precedes NULL strlen. Need0076 stat ownership before permission repair.
0140 CI43959202597 exact65cc580 still building21:25UTC. Deployment84806/
PID182276 now scheduled and gated on exact success+verified package+old reader
end; will reset to Download and BOOT-only0076 flash. Stat scheduler51114
waits up to1800s for0076 worker; six paths then SB/vm/io. Package57048 retained.
0075 still running/no0076 flash at this checkpoint. Single reader64839.
No broad Sandbox success/permissions changes; home screen still unproven.

ACTIVE0075 runtime: analytics stat/open EACCES13 at osanalytics group
15C54419-7736-4C62-B119-1C994A4F8444/Library[/CoreAnalytics] then strlenNULL;
activation setxattr EACCES13 on Data/System/51E6AD4E-3CED-47F7-B6EC-
51E7034B24DA. Full chunked nested errno/path confirmed. ScreenTime122
Sandbox0x104 ENOTSUP fd3 ownerremotemanagementd; sample in rootless_log
socket connect before assertion. SB25 currently MC checkIn wait,tccd37 survives.
0140 CI43959202597 exact65cc580 building; package-only57048 for0076.
0075 reader64839 and read-only scheduler19502 retained. No0076 reset/flash.
Need actual filesystem uid/gid/mode flags from0140 before permission repair;
no broad bypass. Home screen unproven. See newest A03_PROGRESS evidence.

ACTIVE0075 CI43955738619 exact2f78691 SUCCESS. Verified same0074 config,
BOOT-only flash/reboot21:17UTC. Image SHA890b3491...460a31/kernel26b09528...
Boot0075 reader/deploy64839/PID169581 waitsUSB180 then captures660s.
Need0138/0139 live ScreenTime/analytics/activation xattr evidence and SB
progress.0140 prepared/read-only stat NOT included. No second tty reader.
No root/protected writes; home-screen goal unproven.

ACTIVE0140 prepared for NEXT build only: read-only worker stat /private/var/
PATH actual uid/gid/mode/flags/fileid/mountflags, local exact Clang+ASan/UBSan
PASS. Current0139 CI43955738619/deploy64839/package62827 retained unchanged;
NO0075 flash yet.0074 container63 query sample completes; not proof deadlock.
VM compressor2911/free2922pages; storage ready1/poisoned0. Need0139 boot
runtime xattr errno/path, ScreenTime assertion, analytics failure. Home unproven.

ACTIVE0075 CI43955738619 Build21:08UTC exact2f78691. Package62827/PID167795
and deploy64839/PID169581 live. Deploy waits verified exact success+same0074
config+reader end, then synced CDC Download, authorized BOOT-only upload and
660s capture. NO0075 flash yet.0074 initial reader ended normally; short
status67339 currently60s. SB26/tccd37/containermanager63/profiled103 alive.
Activation backup exclusion decoded setxattr com.apple.metadata:com_apple_
backup_excludeItem ->22byte com.apple.MobileBackup; need actual path/errno.
ScreenTime exact assertion and analytics container failure remain pending.
Do not duplicate watchers/readers. Home-screen goal unverified.

ACTIVE0139 CI43955738619 exact2f78691552a541b5c9ee56c06ee6a4c08e308096
in progress21:01UTC. Package-only watcher /tmp/a03-0075/watch-package.py
will verify exact CI success then prepare0075 using same0074 configuration;
NO automatic flash/reset in this watcher.0074 existing reader retained.
Next runtime trial needs0138+0139 results for ScreenTime assertion, analytics
path errno, activation backup-exclusion path/errno. Home screen unproven.

ACTIVE0139 tested filesystem/crash diagnostics prepared.0074 SB26 still
MadGate getActivationState sync XPC; mobileactivation crashes setting backup
exclusion, Cocoa513 permission, actual path/POSIX errno truncated/unproven.
ScreenTime/analytics still crashing;0138 live detail not in0074.0139 adds
setxattr/attrlist/datavault fd-owner evidence and short annotation chunks.
Actual helpers ASan/UBSan PASS; full systemcalls+exception exact Clang PASS;
plain reverse/reapply hash equality PASS. No reset/flash during investigation.
Need full CI then same-config0075 and verify actual failures. Home unproven.

ACTIVE0074 CI43951369485 exacta4d660c SUCCESS, verified BOOT-only flash/
reboot20:52UTC. Watcher14214/PID154025 now waitsUSB/captures660s initial log.
BOOT SHA95d093c1...84814e. Same0073 1GiB/args/ADT/loader/root. Need0137
mobileactivation detailed crash, actualSB wait/home screen.0138 diagnostics
prepared in git but NOT in0074. Do not open second tty reader.

ACTIVEWAIT0137 CI43951369485 Build live20:47UTC; watcher154025/14214
retained. Extra static evidence: rootless_convert_to_datavault opens dir,
Sandbox0x104 args{int64fd,owner}; policy ENOTSUP explains dmd live error,
ScreenTime same call ownerremotemanagementd still candidate pending0138.
No blanket-success/no state changes. Offline image empty SystemGroup is
NOT current-phone filesystem evidence. Home-menu unproven.

ACTIVE0138 investigation prepared, NOT in running0137 CI43951369485.
analyticsd exact crashes strlen(NULL) from OSASystemConfiguration pathCATasking
fileSystemRepresentation; OSAnalytics root systemgroup.com.apple.osanalytics
+ /Library/CoreAnalytics lookup/setup, actual failure errno unknown.
ScreenTime binary data-vault assertion candidate, live reason unproven.
0138 adds ScreenTime2crash slot +analyticsd192startup errors. ASan/UBSan
helpers +exact systemcalls Clang PASS; kern_exit Apple builtin limitation.
Keep existing0074 watcher14214/PID154025 and CI unchanged;0138 next build
can include actual0074 activation diagnosis. No new flash yet/home unproven.

ACTIVE0137 CI43951369485 exacta4d660cbf786f5a5d66e4036f94a124b04518d97
running. Watch-deploy14214 /tmp/a03-0074/watch-deploy.py waits exact success,
packages same0073 loader/ADT/args/root, waits prior reader finish, synced
CDC Download then BOOT-only0074/capture660s. No0074 flash yet. Keep watcher.
0073 tccd fixed/survives; SB now MobileActivation getActivationState wait;
mobileactivation crash loop needs0137 bounded details. Screen report asked.
Home screen unproven; no activation-state or Apple binary changes.

ACTIVE0073 live tccd37 survives, ops22/1 accepted! SB25 moved past MC
migration, now13threads/main MobileActivation getActivationState sync XPC.
mobileactivation crash loop not covered detailed selector. Prepared0137
bounded2 crash reports for exact truncated mobileactivation name; helper
ASan/UBSan PASS, full-file local Clang blocked unchanged Apple kalloc builtins.
Need full CI then0074 diagnostics. Capture90578/88152 still live0073,
cache slide13424000. No physical home-menu evidence. No reset yet.

ACTIVECOPYINSTR corrected0136 commitc9a358b pushed, CI43946625323 exact
c9a358b7c068a5fca9a628e6ae2a03ecf879f7c4 in progress(Deps). Existing
Download detected. Watch/deploy session88152/PID90578 /tmp/a03-0073/
watch-deploy.py waits same exact successful CI, packages with exact0072
ADT/1GiB/args/loader/stockDT, verifies then BOOT-only flashes0073 and captures
660s. Log watch-deploy.log/flash.log/capture.stderr. No new flash yet.
Do not duplicate watcher. Plain reverse/reapply source equality+Clang and
corrected RED/GREEN regression PASS. Need runtime ops22/1+tccd survival,
SB migration progress+actual physical home screen (unproven).

ACTIVE0072 user physical panic PCfffffe000746e938 resolves exact kernel
copyinstr+18 str xzr,[x3];0136 passed NULL lencopied, concrete caller bug.
Fixed to local copied output; corrected regression RED old/GREEN fixed,
ASan/UBSan + op2 + full exact Clang compile PASS. Phone in Download,
heimdall detect PASS. Need commit/push/fullCI then0073; no flash yet.
Home screen unproven. Detailed evidence newest A03_PROGRESS entry.

ACTIVE0072 20:05:47UTC passive retry51868 TERMINAL: no console within180s.
No retry file/USB or Samsung device; no button reboot/screen report received.
Prior USB reset exhausted descriptor retries. No capture/probe left running.
Need physical phone recovery or screen report to continue runtime testing;
0136 profile runtime/home screen still unproven. Prior evidence below.

ACTIVE0072 first trial USB/log ceased19:56:34UTC before tccd sandbox call.
60s SB26 dyld page-in/emmc mutex; tccd37 dyld, both samples END. No0136
op22/1 runtime proof/no GUI. EP0 serial timeout-7, not access; new udev
permissions verified. USB interface reset20:00 failed descriptor/address,
ENODEV. Await user physical screen + conditional button reboot request.
Old capture/deploy ended, old scheduler83348 stopped. Passive retry51868
wait180s/capture600s boot0072-usb-retry-passive.log; DO NOT open second tty.
No new build/fix; built-in180s sample still enabled. Home screen unproven.

ACTIVE0072 CI43940554508 exact1f0d037 SUCCESS, package verified; BOOT-only
upload successful/reboot19:53UTC. Image SHA84c84ae3...616d0a. Exact0071
1GiB loader/ADT/root/args except0136 kernel +a03_sandbox_profiles=1.
Deploy46231/PID82365 now waits USB and captures660s boot0072-usb-initial.log;
probe83348/1741 retained waits real worker, samples60/180/300/540s. Do not
open second tty reader. Need verify new udev permissions, tccd ops22/1,
tccd survival and SB/profiled migration progress; home screen unproven.

ACTIVE0071 19:44UTC fresh probes19..23 confirm SB25 main exact same CPU/
stack since19:30 (MC migration wait ->profiled109 ->TCC XPC). SB8threads,
no tccd in fresh ps. Host storage ready1/poisoned0. Private status1944 log.
CI43940554508 for0136 remains in progress; retained package/deploy/probe
watchers, no0072 flash. Short status capture finished, tty reader released.
Apple logo reported; no home screen. See newest A03_PROGRESS evidence.

ACTIVE0136 CI43940554508 still Build19:41UTC, watch/package/deploy handles
retained. Added read-only probe scheduler1741 /tmp/a03-0072/probe.py waits
for actual0072 worker then current ps/vm/io/SB/profiled/tccd/lsd at60/180/
300/540s. Own output probe.log; never opens tty or resets phone. Existing
udev rule installed matches repo; new-enumeration permissions need runtime
check. No0072 flash yet. Home screen pending all runtime gates.

ACTIVE0136 CI43940554508 Build still live19:38UTC. Existing package watcher
73118/PID81847 retained; deploy watcher46231/PID82365 now waiting for its
verified package. /tmp/a03-0072/deploy.py gates exact successful CI+SHA,
manifest/image/loader/ADT/args then synced CDC Download and BOOT-only flash;
waits for no other tty reader, captures660s. No phone reset/flash yet.
Frozen0134+git apply0135/0136 exactly matches compiled full source; tests PASS.
Do not duplicate/restart watchers on observation timeout. Logs watch.log,
deploy.log,flash.log,capture.stderr under/tmp/a03-0072. Home menu unproven.

ACTIVE0136 CI43940554508 Build confirmed in progress; package watcher
session73118 /tmp/a03-0072/watch.py alive, log/tmp/a03-0072/watch.log.
Watcher only packages after exact successful SHA; NEVER flashes. When CI
finishes inspect manifest/image before CDC Download reset+BOOT-only flash.
0071 latest16/17 still SB MC migration ->profiled TCC XPC wait. No new flash.

ACTIVE0136 CI43940554508 exact1f0d037 running macos-26-intel, runner
acquired/checkout/profile step passed. Full build pending. Local helper
ASan/UBSan + exact sweet_amfi compile + existing op2/live-probe tests PASS.
Prepared /tmp/a03-0072/package.py requires exact successful SHA/checksums,
marker/arch, identical0071 loader/ADT/root/args except new profile bootarg.
0071 remains running; no reset until verified package. Home menu unproven.

ACTIVE0136 scoped tccd named-profile query22/install1 candidate locally
ASan/UBSan + full-file exact CI-command Clang + plain git apply PASS.
Explicit lab NO enforcement, a03_sandbox_profiles=1(default0) plus existing
sandbox-disabled policy; tccd/com.apple.tccd only, unknown ops stay ENOTSUP.
Need full CI then0072 exact0071 1GiB loader/ADT/root plus new kernel+arg.
0071 running SB->profiled109->TCC wait; no home screen/phone changes.

ACTIVE0071 19:30UTC SB25 PASSED LS wait, now7threads/main sync MCProfile
migration while shouldShowCloudConfigurationUI. profiled109 worker waits TCC
_tccd_send_message/TCCAccessSetOverride. Existing tccd profile-not-found
crash loop now concrete downstream candidate. Unsupported Sandbox query22
was decoded; verify install ABI before scoped lab-mode support, no blanket
success. Capture75768 current65s ends normally. No home menu/user saw logo.
No reboot/phone writes; next fix evidence-backed TCC startup compatibility.

ACTIVE0071 ACL restored: ps/vm/io/sample25+100+129 complete. lsd100 now9
threads incl semaphore wait to symbolicate; activation133,icons129. SB main
still LS wait. vm compressor0, active26190/inactive27710/wired8503/free3119.
Capture41818 boot0071-usb-live-probes.log120s. Persistent exact-device udev
rule prepared+udevadm verify PASS, user must install/reload/trigger per docs.
No home-screen proof/no phone writes. Need follow lsd semaphore stack.

ACTIVE0071 19:17UTC access audit: libusb Probe still fails-3 on current
USB005/010 root:root0664. Same requested ACL missing over3goal turns.
All4automatic SpringBoard samples already captured; no further automatic
lsd snapshots exist. Capture30397/process74624 confirmed alive and logging;
leave it and phone running. Need user apply narrow setfacl then resume ps,
vm/io and current lsd/dependency samples. No home-menu proof; goal blocked
on live-probe permission rather than repeated blind flashes/API bypasses.

ACTIVE0071 all4passes180/300/420/540s main+LS XPC CPU/stacks identical.
Need EP0 ACL USB005/010 (pending user), ps/current lsd sample next.
Capture30397 still live660s. No home menu. tccd disassembly confirms named
Sandbox query22 unsupported -> compile-file fallback -> profile-not-found;
not established cause of LS wait; no bypass/functional change made.

ACTIVE0071 pass1(~300s) main+LS XPC CPU/full stacks EXACTLY unchanged
since180s. More memory advances early init but LS reseeding still blocks.
Capture30397 alive660s for remaining passes. EP0 ACL005/010 pending user;
next probe ps/vm/io then lsd (new PID). tccd profile-not-found crash loop.
No home screen; preserve running state. Code0c8cc37/documentation committed.

ACTIVE0071 pass0(~180s) SB25 already4threads/ControlCenter+LS reseeding wait;
0070 all4passes180..540s stayed1thread in initializers. Earlier progress,
not causal speed-factor or home proof.3BGRA swaps. slide24614000.
Initial capture32671 completed; continuation30397 live660s retains passes.
Need new USB005/010 ACL (requested) to sample lsd/prove runtime pages.

ACTIVE0071 CDC live, actual iOS services/SpringBoard25 start, no panic.
Capture32671 initial180s ongoing. New USB005/010 EP0 denied-3; narrow ACL
requested async; tty logs unaffected. Need page-count + SB/lsd live samples;
built-in180s sample should arrive independently. No home-screen evidence.

ACTIVE0071 1GiB BOOT-only uploaded100percent/success/reboot, runtime pending.
Capture32671 waits120s CDC then180s boot0071-usb-initial.log. SHA3c748207...835e3.
Exact0070 kernel/root/args/seed,2payload bytes change RAM256->1024MiB.
LiveDT bank/reservation validation + predicate tests/loader Clang PASS.
No3GiB at fixed base: bank end17ffff000; max~2016MiB, holes need VM work.
0070 lsd DID leave IconServices wait to app scan after last stall check;
MobileActivation waits LS while lsd requests activation (possible cycle).
Need0071 runtime before further changes. No home menu/protected writes.

ACTIVE0070 18:59UTC confirms persistent SB stall: main+XPC thread CPU/
stacks exactly unchanged versus18:49..18:50 (~9min), not ongoing startup.
lsd101 IconServices+activation request stacks/CPU unchanged too. Fresh ps
now sees iconservicesagen438/mobileactivation413; sample these next.
Kernel/EP0 responsive; tccd436+analyticsd441 crash/respawn. Storage healthy.
Read-only boot0070-usb-stall-check.log seq29..33; no reboot/flash/root writes.

ACTIVE0070 late18:49..18:50UTC: SB25 now4threads, past objc initializers.
Main waits unfair lock in LSContextInitCommon/LSApplicationRecord while
ControlCenter module metadata loads; thread1 sync XPC _LSCopyServerStore.
lsd1016threads: bundle registration waits IconServices invalidation; another
explicit database-finish-seeding wait; separate sync MobileActivation request.
Current blocker is LS database/service readiness; underlying failing dependency
not isolated. Late90s capture60737 boot0070-usb-late-probes.log. Swap10 does
not prove home menu. No new writes/topology changes. See A03_PROGRESS.md.

ACTIVE0070 live EP0 hardware SUCCESS after ACL: ping/vm/io/ps/threads25/
threads56 BEGIN/END with CDC output ongoing. Initial660s501877bytes/all4
samples complete; live240s capture8740 boot0070-usb-live-probes.log active.
SB25 one thread still objc initializers: eMMC page-in mutex waits, one
runnable sample.20.6168s:7654pageins/4495reactivations/2368compressions/
1750decompressions,108.07MiB reads; swap0,driver healthy.256MiB working-set
churn is supported; larger RAM benefit not tested. Need validate stock DT
RAM/reservations then controlled bigger-window test (loader/ADT/packer all
hardcode256MiB). No SMP/root/protected partition changes/no home-screen proof.

ACTIVE0070 CDC logs live/worker start0 enabled1; SpringBoard PID25.
Capture71796660s boot0070-usb-initial.log active >350KiB. EP0 libusb open
fails-3: root:root0664 /dev/bus/usb/005/008; sudo -n needs password.
User asked for sudo setfacl -m u:stoned:rw on that exact node. Await actual
ping/threads25/vm/io responses. No console-probe runtime/home-screen claim.

ACTIVE0070 BOOT-only upload100percent/success/reboot. CI43918800523 SUCCESS
exact520d2a7,4source/checksum/probe symbols verified. BOOT846a19e9...e0d77.
Loader0069 identical except image_size, ADT identical, only add a03_probe=1.
Capture71796660s waits CDC boot0070-usb-initial.log. Need EP0 actual ping/
threads/vm/io then SpringBoard root cause. Protected partitions/root unchanged.
No home screen yet.

ACTIVE retry43918800523 exact520d2a7 acquired macos-26-intel runner;
Set up job passed/checkout running. Full build pending. No phone writes.

ACTIVE43914475835 was runner allocation failure, not compiler failure:
job133464838955 zero steps/no logs/no runner; annotation "The job was not
acquired by Runner of type hosted even after multiple attempts". All4local
Clang checks PASS again. Retry corrected0135 on macos-26-intel pool; no new
source fix/no phone writes. Need full CI then validated BOOT/live probes.

ACTIVE corrected0135 commit1b3fdc1 pushed; CI43914475835 dispatched only
after exact per-file local Clang checks passed. Full CI/runtime pending.

ACTIVE0135 fix:43910152567 failed undeclared vm_map_read_user in BSD.
Moved bounded read into Mach exception.c bridge; exact per-file CI command
replay reproduces old failure and all4corrected objects PASS (~2s). New tool
tools/a03-check-kernel-objects.py preserves defs/includes/warnings and rejects
no errors silently. Sanitizer/PTY/CDC/sampler and patch equality PASS.
Need corrected full CI link before BOOT0070/probing. No flash/home screen.

ACTIVE0135 exact0751d9c pushed; CI43910152567 in progress. Four real
kernel objects PASS plus actual PTY host test: logs drain while probe send
blocks. Old-sha accidental43910063052 cancelled, no deployment. Device is
Download. Need CI success/frozen4source checks, BOOT0070 with only extra
arg a03_probe=1 versus0069, then ping/threads/vm/io replies. No home menu.

ACTIVE2026-11-16 live0135 monitor implemented/tested, not deployed yet.
EP0 vendor0xa3 ->4slots/separate kernel probe worker; separate host sender
retains tty drain. a03_probe=1. ping/ps/vm/io/threads PID (no user reads),
sample PID/mem PID ADDR COUNT (may sleep). No task stop/memory writes.
Host sanitizer tests/4real arm64 objects PASS; full CI/runtime pending.
0069 incomplete: only pass0, eMMC mutex during dyld page-in; old io_ticks
include yield intervals, not exclusive service. Device Download; cause unknown.
Need0135 BOOT test then live threads/vm/io. No SpringBoard home screen.
Preserve protected partitions/root.

ACTIVE0069 BOOT-only100percent/success/reboot22:49UTC. CI43770218935
SUCCESSf1b31e1,20sources/loader/ADT/args match. BOOTbb20a474...3850ee.
Capture245564660s boot0069-usb-initial.log waits CDC. Test0133 read16KiB
mutex yield +0134 SamsungGalaxyA03/a03 names; baseline0068 all4page-in
mutex waits. Need actual CPU/wait progression comparison; no GUI proof.
Batch off, memory256MiB/CPU1/root unchanged.

ACTIVE0068 complete660s502735bytes SHAad1bb41db9fca94ed049284f810644874f1d3ee38257b7cfe43b14414495087c.
All4samples same eMMC mutex/page-in wait; final CPU user.025/system13.45,
runnable118.09s.3swaps/no home-screen proof. No active CDC capture.
0069 CI43770218935 Build live; package7359/deploy58959 wait verified20
frozen-source matches + identical loader/ADT/args. Need hardware fairness.

ACTIVE0068 first3 samples180/300/420 all eMMC mutex page-in wait;
SB system5.71/8.38/10.99s, runnable59.4/80.7/99.3s, advances objc pass2.
CI43770218935 exactf1b31e1 read fairness/A03 identity builds.0069 package
7359 verifies20sources frozen0134 and identical0068 loader/ADT/args;
deploy58959 waits verified package +0068 capture239781 normal completion.
No measured fairness effect/home screen yet. CPU count1/memory256MiB stay.

ACTIVE0068 first stack proves SpringBoard controller mutex wait during
cluster_pagein, event=a03_emmc_lock+8. Not XPC timeout. CACHE_CTRL0 means
flush-batching benefit absent. IO~81.56s/8192requests excludes lock wait.
0133 read16KiB lck_mtx_yield fairness +0134 A03 product/target name prepared,
actual handler handoff tests/2kernel objects/plain apply/profile PASS.
Not deployed;0068 capture239781660s still live. Need compare next samples.
Redmi text is actual inherited product-name leak; SWEET internal names stay.

ACTIVE0068 BOOT-only100percent/success/reboot22:30UTC. CI43768648670
SUCCESS9816151,20frozen sources/loader/ADT/args match. BOOTbd6682dc...81582.
Capture239781660s boot0068-usb-initial.log waits USB; sample180/300/420/540
includes CPU times and kernel WAIT traces. Resolve with exact0068 kernel
and tools/a03-symbolicate-kernel-waits.py. Batch off; no root/SMP changes.
No home screen. Need actual blocking kernel call before next functional fix.

ACTIVE0067 late180s complete30411bytes SHA34011d2f76b428bef7fc9a1d7901806dd144cbfb9623064e187a4fa22390613b.
7more swaps4..10; analyticsd231 generic crash. No GUI content proof.
0132 CI43768648670 Build passed/artifacts uploading; package59465 +
deploy65357 pending exact20sources/loader/ADT/args. No current capture.

ACTIVE user dmd crash confirmed: dmd153 SIGABRT, Foundation exception
Failed to enable data vault: Operation not supported (45). Missing API
support evidence, not CPU overload proof; no dependency/GUI conclusion.
Second analyticsd PID221 (prior197 was transcription error).0068 CI
43768648670 still Build; package59465/deploy65357 waiters live.

ACTIVE0067 complete660s493437bytes SHA133fe88ab43b53d08c42020bbd453c0d30736b6da183939585f67fdbf4c7efb3.
Four passes show slow SpringBoard initializers, one thread state9, no home
screen.32HOST reports/3swaps. analyticsd195/197 and tccd189 crashes traced.
0132 CI43768648670 exact9816151 Build live; package0068 session59465 waits
20frozen-source expected0132 and identical0067 loader/ADT/args (batch off).
No active CDC capture. Next0068 kernel waits/CPU times, not presumed IO fix.

ACTIVE0067 pass2/420s SpringBoard25 advances to libobjc map_images_nolock,
still state9/one thread; earlier same180/300s PC not permanent deadlock proof.
analyticsd null strlen SIGSEGV and tccd189 profile-not-found SIGABRT captured.
0132 CI43768648670 exact9816151 running, package0068 session59465 waits
20frozen-source expected0132 + identical0067 loader/ADT/args (batch off).
0067 capture233456660s active; final pass540s pending. No home screen.

ACTIVE0067 sample0/1: SpringBoard25 single thread state9 WAIT|UNINT,
identical PC1c188ed9c/dyld hasThreadLocalVariables and libSystem_initializer
stack120s apart. Not CPU-saturation proof; need kernel wait. Backboardd
progresses and3swaps. analyticsd195 SIGSEGV/null captured (expanded tracer).
0132 CPU times/wait event/continuation/bounded nofault kernel frames prepared,
real kernel object/plain apply PASS.0131 stays off. Capture233456660s live.

ACTIVE0067 BOOT-only100percent/success/reboot22:11UTC. CI43766598769
SUCCESSc2c3837,19frozen sources/loader/ADT/sole sample arg verified.
BOOTfcaa5d1f...15f14. Capture233456660s boot0067-usb-initial.log active;
need GUI samples180/300/420/540s, symbolicate with captured cache slide.
Private helper /tmp/a03-symbolicate-samples.py ready.0131 absent/off,
no SMP/root changes, no home-screen proof. Target actual blocking service.

ACTIVE0066 continuation180 complete11406bytes SHAeb85be80...932e99,
generic analyticsd225 crash, no custom CRASH.0067 CI43766598769 passed
Build, packaging. Deploy waiter38683 runs only after package19exact-source/
loader/ADT/sole sample arg/hash checks, captures660s. No current CDC reader.
0131 dispatch stopped; wait-state evidence priority. No home screen.

ACTIVE CPU0 question verified: cpus=1; SweetCPU hard-enforces one CPU,
startCPU KERN_NOT_SUPPORTED, self-SGI only. cpus=8 alone will not work.
SMP requires A03 topology/PSCI secondary entry/per-core IRQ/timer/cross-IPIs.
No SMP change made; CPU contention plausible but no proven logo blocker.
0067 thread sampler remains priority.0131 auto-dispatch stopped.

ACTIVE user doubts I/O-bound hypothesis. No measurement established it.
Priority is0067 GUI thread snapshots to distinguish IPC/service wait from
CPU work; do not deploy0131 storage candidate as presumed fix. Stopped
0131 auto-dispatch waiter230570 before CI launch.0131 remains tested,
committed/off by default only. Existing CI43766598769 builds0129/0130;
package0067 waits success.0066 continuation180s230775 active.

ACTIVE0066 initial360 complete554548bytes SHAf4b0c37894802553dd2ca66e0ebccf1b56c0cc5618e0f741be0c1f5d42e6a6c6.
selector3 success/3full-screen swaps; no custom/generic crashes within capture.
No home-screen proof.0131 committed75ecd42, frozen20sources. Dispatch15508
waits prior CI43766598769 before starting speed optimization build. Need
batch-off/on actual CACHE_CTRL/I/O tick comparison, not quiet-log claims.

ACTIVE speed optimization priority:0131 opt-in a03emmc_batch=1 batches
card-cache flush per buffered request, retains CMD24/status per sector,
flush-before-completion and raw durability. CACHE_CTRL unknown until new
probe log; optimization conditional on enabled card cache. Bounded8-line
I/O tick/sector counters added for profiling. Host MMIO/BSD error/bounds,
real kernel object compile, plain-apply exact equality/profile staging PASS.
Not in0066/0067. Need0131 CI after43766598769 finishes (avoid cancellation),
then identical batch-off/on BOOT builds and device timing. No speedup claim.
0066 still capture360s; selector3 success and3 actual swaps now recorded.

ACTIVE0066 BOOT-only upload100percent/success/reboot and CDC return verified.
CI43765717894 SUCCESS2a79856;15 frozen sources/loader/ADT/args verified.
BOOT82df93a9...1d2e4.360s capture227343 boot0066-usb-initial.log active.
0065 continuation deliberately stopped~168s; analyticsd226/dmd194 crashes.
CI43766598769 exactc2c3837 builds0129 sampler+0130 HOST logging cap;
package0067 session46921 waits19 frozen sources, only add a03_sample=1.
No0067 flash, measured speedup or SpringBoard home-screen proof.

ACTIVE user confirms logo-only, slow with HOST MIG spam.0130 now caps
normal HOST logs8/site(4sites)+separate16errors, actual host/kernel objects/
plain apply PASS; no IPC behavior changes.0065 initial1694 HOST lines78KB.
0127/0128 CI43765717894 SUCCESS;0066 package63560 downloading/checking.
Need build0129+0130 next for quiet logs and actual GUI thread snapshots.
No runtime speedup/home screen claimed.0065 continuation85699 still active.

ACTIVE0065 initial360 complete554042bytes SHA3228ff83...15dfb:3 swaps,
5 actual SpringBoard syscalls, no custom/generic crash lines, no A03 USER.
Continuation300s85699 active boot0065-usb-continuing.log. CI43765717894
exact2a79856 still Build; package0066 session63560 waits15 exact sources
and identical loader/ADT/args.0129 samplerb99a671 prepared/tested, absent
that build. No home screen. Latest commits pushed, private logs ignored.

ACTIVE0065 live: actual SpringBoard25 startup syscalls now visible; Sandbox
op2 succeeds, AMFI5a103, mkdir/dev22, libdispatch query2; no proven blocker.
No A03 USER lines yet. Capture56741 ongoing360s. CI43765717894 builds0066.
0129 prepared bounded read-only thread sampler (24threads/12frames,4passes,
180s then120s), no lock-held user reads, host/kernel objects/plain apply PASS.
Not in0065/0066; preserve frozen snapshots. Home screen unverified.

ACTIVE0065 BOOT-only100percent/success/reboot~21:49UTC. CI43764128179
SUCCESS736d3b3;14 sources/loader/ADT/sole a03_userlogs=1 verified.
BOOTbba5c86c...5151e. Deploy56741 waits CDC then360s boot0065-usb-initial.log;
inspect A03 USER SpringBoard/backboard and A03 START SpringBoard.
Follow-up0127/0128 CI43765717894 exact2a79856 building; package0066 session
63560 waits15 sources frozen expected0128 and identical args/ADT/loader.
No0066 flash/root rewrite. Expanded crash names not yet on device.

ACTIVE0064 fresh180s completed24497bytes SHA9d836d9d...96d05, generic
analyticsd165/tccd172 crash lines; swaps4..9 continue.0128 now covers tccd
as well,14 bounded slots; host/kernel syntax PASS. CI43764128179 Build
passed, artifacts uploading; package0065 session34897 waiting success.
No capture running now; USB CDC remains. No SpringBoard home-screen proof.

CORRECTION:0064 continuation contains generic corpse crash lines for dmd126
and analyticsd157 despite zero custom CRASH. User confirms analytics crash;
new180s75436 captures analyticsd165 crash plus swaps4..6. USB live. Do not
say no crashes globally: old0108 name filter omitted analyticsd/dmd.
0128 adds bounded independent slots, host/kernel/plain-apply tests PASS;
not in CI43764128179/0065. SpringBoard dependency impact unproven.

ACTIVE0064 continuation300s completed8093bytes SHAeb640a7a...d3004,
zero CRASH/new FB/SURF/SB/backboard spawn. No capture currently running;
USB CDC remains. CI43764128179 exact736d3b3 still Build; package34897
live waits then14 source/loader/ADT/only a03_userlogs=1 checks. Deploy0065
script prepared /tmp/a03-deploy0065.sh, not executed. No GUI proof.
0127 default-surface correction c15b532 stays isolated from0065 diagnostics.

ACTIVE0064 initial360 complete504774bytes SHAdec6bfa0...dc352: zero CRASH,
4 WI grants/3 full-screen swaps, single SB/backboard spawn authorization.
Continuation300s18693 active boot0064-usb-continuing.log. CI43764128179
still Build;0065 package34897 waits success. No home-screen proof.

ACTIVE0064 reaches three full-screen swaps,4 entitled WI grants, no CRASH.
New repeated499 op6/len38 ENOTSUP is work_interval_instance_start (not
workload config); exact wrappers update7/finish8, all absent current XNU.
No hint bypass/remap. Wait actual0125/0126 runtime diagnostics before
choosing functional fix; CI43764128179 building.0127 surface fix committed
c15b532, not in that build. Existing snapshots frozen per candidate.

ACTIVE0064 runtime grants backboardd entitled work-interval privilege;
zero CRASH so far, initial360s still active. GUI unverified.0127 local
candidate fixes selector3: exact wrapper sends canvas dimensions, not layer;
accept native or undiscovered-zero values, reject conflicting geometry.
Host actual-method, kernel syntax/object and plain apply equality PASS.
Not in0125/0126 CI43764128179/expected0126 snapshot. Preserve0065 isolation.

ACTIVE0064 BOOT-only upload100percent/success/reboot~21:30UTC. USB CDC
returned; deployment87223 captures360s boot0064-usb-initial.log. Need see
A03 Sandbox entitled work-interval grant and eventual swaps/GUI behavior.
Follow-up0125/0126 CI43764128179 exact736d3b3 builds; package0065 session34897
waits success and14 frozen source/loader/ADT/only a03_userlogs=1 checks.
No0065 flash; root unchanged and protected partitions preserved.

ACTIVE0064 package verified CI43762755721 SUCCESS640a2a1,12 exact sources,
identical loader(except size)/ADT/root; sole arg a03_work_interval=1.
BOOTf98965ef...13d05. CDC reset from0063 worked; Download observed.
Deploy87223 BOOT-only then360s capture boot0064-usb-initial.log. Need check
upload result, entitled work-interval grant, CRASH/swaps/SpringBoard evidence.
0063 late capture interrupted deliberately4006bytes SHA3d8b239d...3d687,
zero CRASH.0125/0126 remain unflashed follow-up diagnostics.

ACTIVE0063 extended600s completed90815bytes SHA07d49975...d4193, zero
CRASH, swaps4..11. Capture stopped normally, CDC remains; no GUI proof.
0124 CI43762755721 still Build21:28UTC, package54915 live.0126 follow-up
adds SpringBoard to bounded startup syscall evidence; actual-source host,
kernel syntax and plain apply equality PASS. Not in0124.0125/0126 local
tree differs from frozen0124 comparison snapshot; retain isolation.

ACTIVE handoff:0063 still running USB CDC; user sees Apple logo and logs
confirm11 full-screen BGRA swaps, zero CRASH through extended capture's
latest86767-byte snapshot. Extended600s session79994 still active at read.
0124 CI43762755721 exact640a2a1 in Build. Package0064 session54915 waits
success; expected12 source files frozen /tmp/a03-expected0124/xnu, package
script now reads that snapshot (local working tree additionally has0125).
0064 sole arg addition a03_work_interval=1; no flash yet.0125 committed
75148a0 after7441628/10da93e, host and real syntax/object tests PASS; full
two-file plain git apply equality PASS. Not in0124 CI. Root unchanged.
Next: let current capture finish, verify0124 artifacts/package, BOOT-only
0064 test, capture long enough to compare entitlement grant and GUI progress.
Do not mark SpringBoard complete from logo/frame submission alone.

NEXT diagnostic0125 prepared/tested: opt-in a03_userlogs observer on
SpringBoard/backboardd /dev/null writes, duplicate-uio only, bounded/sanitized;
not in0124 CI43762755721 or running0063. Keep0124 test isolated first.

ACTIVE0124 CI43762755721 exact640a2a1 running; package0064 session54915
waits success and12 source/loader/ADT/sole a03_work_interval checks.
0063 continuation300s complete136106bytes SHA9cc39598...96b51, zero CRASH,
three full-screen swaps. User sees Apple logo. Extended600s79994 captures;
leave0063 running while building. No new flash/home screen proof. Selector29
is GetDisplayArea; its Unsupported did not prevent later swaps.

ACTIVE0063 user physically sees Apple logo; continuation confirms three
full-screen720x1600 BGRA swaps by backboardd, zero CRASH at latest read.
Leave running while collecting. Home screen unverified.0124 candidate
adds opted-in work-interval privilege only for current validated entitlement;
stock backboardd has it. Host compile/tests pending, no new flash.

ACTIVE0063 runtime: initial120s422685bytes SHAa5d459ca...25aab9,
zero CRASH; IOCoreSurfaceRoot/AppleCLCD registered720x1600. MobileGestalt
size/dot-pitch calls succeed. Backboardd DOES reach FB selector29(out8),
Unsupportede00002c7; no swaps or GUI verified. Also mkdir220 Caches EACCES13
and work_interval_ctl499 op4 EPERM1. Diagnose exact ABI/permission causes,
no generic-success bypass. Continuation49374/300s still running at read;
75586-byte snapshot no CRASH/new FB calls. USB CDC present, no new flash.
See latest A03_PROGRESS entry; previous pending-runtime notes are historical.

ACTIVE0063 flashed BOOT-only100percent/success/reboot21:08UTC. CI43760748014
SUCCESSee1307c;12 source/loader/ADT-only-disp0/arg-only-a03_display checks
PASS. Imagedd217cf6...68f230. CDC Download control from0062 worked again.
Deploy/capture28481 waits CDC then120s; inspect A03 SURF/FB/CRASH logs.
No GUI or provider-registration runtime evidence yet. Protected parts intact.

Earlier0123 CI43760748014 fromee1307c live. Package0063 session55131
waits success, compares12 exact sources, preserves0062 loader/ADT except
disp0 and only adds a03_display=1.0062 continuation300s completed6887bytes
SHA3a713cf9...cd809, no CRASH; CDC remains. Full display runtime unproven.

Earlier0123 display/surface candidate prepared for full CI. Native720x1600,
exact iOS16.0 swap400 ABI, opt-in a03_display=1, unknown selectors unsupported;
panel PA/stride/depth gates and64MiB allocation/96MiB wiring caps. Actual
copier tests, four real kernel C++ compiles, plain git apply equality PASS.
0062 stays CDC; continuation2668 ends300s normally. No display flash yet.

Earlier0062 runtime: three HFS exchanges error0; no atomic-save failures
in initial100s, personas created; one SpringBoard/backboard exec each and
zero bounded CRASH records.371425bytes SHAa929c52f...92640. Continuation2668
captures300s. No GUI proof. Next display ABI adaptation; keep0062 running.

Earlier0062 BOOT-only uploaded100percent/success/reboot20:47UTC.
Corrected0122 CI43759153171 SUCCESS28b8b81; six exact CI sources and
0061 loader/ADT/only a03_hfs_swap=1 addition verified. Image0f63d63f...8cd24.
Capture/deploy82030 waits CDC then100s; inspect root HFS exchange and
UMD/container/backboard/SpringBoard. Later display ABI mismatch recorded
in A03_PROGRESS: iOS16.0 swap input400 vs donor46c. No GUI proof.

Earlier resumed SpringBoard goal 2026-11-15. Samsung Download detected.
Corrected0122 CI43759153171 at28b8b81 is live in Build; package0062
session17809 waits successful CI and exact source/loader/ADT/argument checks.
HFS scope regression PASS. Next verified0062 BOOT-only; no new flash yet.
0061 bounded no-crash window does not establish stable SpringBoard/display.

Historical pause: CI43757697658 FAILED: zero-context0122 patch
misplaced call at file scope under git apply. Restored contextual hunks;
fresh plain git apply full-source equality, host scope checks and kernel
compile PASS. Regression rejects zero-context hunks. No retry CI/flash.
0061 running: Sandbox op2 succeeds; initial100s no CRASH records, single
media/backboard exec each; UMD swap ENOTSUP persists.0062 never flashed.
Old package0062 session91355 exited on failure. Continuation45257 may end
normally; retain private logs. Next when resumed: CI corrected0122 once.

ACTIVE0061 flashed BOOT-only100percent/success/reboot20:21UTC. CI43756243470
SUCCESSd640287; exact source/loader/ADT/arg checks PASS. Capture190652
waits USB then100s; deploy session10796. Need observe0121 Sandbox scalar
check and media/backboard/container progression.0122 not in0061; locally
validated/committed038d3f1, no new CI yet. Host was already Download.

ACTIVE0122 prepared: opt-in HFS SWAP -> existing VNOP_EXCHANGE scoped to
writable HFS /dev/a03userdata0 root and a03emmc_rw=1. Actual-source host
checks, kernel compile, patch equality PASS; hardware pending. First finish
existing0121 CI43756243470/package0061 and isolated Sandbox boot. No swap
arg in0061. No additional CI yet. Cross-reference remains below.

ACTIVE cross-reference: docs/a03-userspace-cross-reference.md.
A5 nil-container crash improved after HFS swap0117; A03 omits0052.
A03 retains external ACL resolver, omits work-interval grant. SWEET45263be
matches pinned donor; HakiOS63fc2b4 uses XNU8796.121.2.0121 CI unchanged.

ACTIVE0121 CI43756243470 fromd640287 running; package0061 session16037.
0060 capture83189 complete494160bytes; media null listener/backboard nil
path persist. Sandbox op2 errno103 proven.0061 adds only explicit sandbox
check-mode arg, pending verified CI/package then authorized BOOT-only test.
Candidate sweet_amfi.c in /tmp/a03-ci0053 includes0121 now; avoid stale
0059/0060 full-tree comparisons against that changed file.

ACTIVE0121:0060 proves Sandbox op2 ENOPOLICY103 in all four targets.
Opt-in a03_sandbox_disabled=1 scalar-check policy prepared/tested/kernel
compile PASS; unknown ops ENOTSUP. Need CI then0061, only add that arg.
0060 capture83189 ongoing; exact nil-path backboardd crash persists.

ACTIVE0060 BOOT-only upload100percent; CI43754890342 PASS39eef98.
Capture83189 waiting USB then100s via newgrp uucp; no ACL needed.
Exact0059 loader/ADT/args/root preserved. Need0120 actual syscall errors
before choosing correction; stable GUI unproven.0059 control Download works.

# iOS 16 on sweet (Redmi Note 10 Pro, SM7150) - working notes

ACTIVE0120 CI43754890342 running; package0060 process180250 live.
Read-only exact launchd/cache confirms missing Sandbox op2 -> IPC159 path;
need runtime syscall evidence before policy correction. notifyd service
name matches root plist; media notify8(disabled) differs from9(bootstrap).

ACTIVE0120 bounded startup syscall evidence locally tested/compiled. Next CI
then0060 preserving0059 loader/ADT/args/root;0059 USB currently running.
Target actual system-container lookup failure errno/IPC/entitlement evidence.
No repair claim. Use newgrp uucp capture/control, no ACL request required.

ACTIVE0059 exact backboardd reason: NSURL initFileURLWithPath nil string,
NSInvalidArgumentException. Startup first resolves system-container caches;
BaseBoard defaultPath converts BSSystemSharedDirectoryForCurrentProcess to URL,
container_system_path_for_identifier failure can return nil. Not fixed yet.
Backboardd XML entitlement system-container=true. Original root parent dirs
exist. Need actual container lookup failure. Media null dictionary persists.
0059 running; USB accessible via newgrp uucp (account already in group,
agent inherited groups stale). Use that for capture/control, no ACL ask.

ACTIVE0059 BOOT-only flash SUCCESS19:42UTC; CI43752732761 PASS.
Exact0058 loader/ADT/args/root retained. Capture2930 waits900s then100s,
private boot0059-usb-initial.log. CoreFoundation reason annotation pending.
USB-triggered Download worked again from0058. No physical mode ask needed.

ACTIVE0119 CI43752732761 from4e22af5.0059 packaging18939 waits success,
then exact source/loader/ADT/args.0058 running, USB tty accessible. Capture
77592 complete; initial log private. Use control Download when image ready.

ACTIVE0058 USB capture works: libc++abi confirms uncaught NSException, no
reason text.0119 adds Foundation/CoreFoundation/QuartzCore/libsystem_c owners
(max6 selected), tests/kernel compile PASS. Next CI then0059;0058 running,
tty open. Use working --download-control when next image ready, no mode ask.

ACTIVE0058 flashed BOOT-only100%/success/reboot19:26UTC; CI43751227542 PASS.
Image09f5350cbf8acffabf08a9d14b261241a38f8bd8777e7e9bef655f6b08fa7b69.
Exact0057 loader/ADT/args/root retained. Annotation diagnostic capture77592
waits tty up to900s then100s; private boot0058-usb-initial.log. Runtime pending.
User wants no routine wait updates; only results or needed input.

ACTIVE0118 CI43751227542 from7e5ecb7; supersedes43751096298.
Shared-cache nonzero __TEXT fileoff handled/tested; kernel compile PASS.
Next BOOT0058; phone Download already. Preserve0057 loader/ADT/args/root.

ACTIVE0118: bounded read-only Mach-O __crash_info reader prepared/tested;
local exception.c compile PASS. Need full CI then BOOT0058 preserving0057
loader/ADT/args/root. Host already detects Download; do not ask user again.
Target backboardd termination reason; media null dictionary persists.
USB control Download hardware-confirmed0057; bulk RX remains broken.

ACTIVE0057 CONTROL DOWNLOAD HARDWARE SUCCESS19:06UTC: --download-control
returned0, CDC disconnected, repeated Heimdall detect PASS. No ACK text in
control log (queued logs); transition verified. Bulk RX remains broken.
0057 deeper crash captured: backboard main+a354/aa20, windowserver dispatch_once;
original thrown-site unwound. Media null dictionary persists; WDT disabled
selector0/stage255 confirmed. Root/protected parts retained.
Image3f1d1ac4b3f6978402389aac406b5efbe7c1c5e42b4149ca38352c20c050144d.

CURRENT0055: USB IN works, PIO takeover did NOT fix RX (0800/count1 zero).
0115 explicit --download-control -> CDC SEND_BREAKffff bypasses bulk OUT
to same sync/reset worker. Combined0114+0115 CI43746383199 from3a3f19a
queued; supersedes43746031809.0056 pending. Need physical Download once.

CURRENT0055 installed BOOT-only100%/success/reboot. CI43744564237 PASS.
Image2cf20091b428f9043fd3a77b09903df0de3f4c3ab0b337c3d9dd1549d1043aec.
Exact0054 loader/ADT/args preserved; watchdog opt-in OFF. Capture99106 waits
240s then100s for PIO takeover/RX/download evidence. Later0114 watchdog CI
43746031809 frome55d573 running. Root preserved.

CURRENT: user confirms physical Download, host detect PASS. CI43744564237
(0112+0113) building.0055 MUST omit a03_watchdog_disabled=1:0114 software
PMU prerequisite is later commita4b45ea, locally validated but not in this
CI.0055 is USB-only activation test.0114 needs later full CI before enabling.

NEXT: combined0112+0113 CI43744564237 from62736e7; supersedes watchdog-only.
0055 needs exact0054 ADT/loader/args; watchdog remains off, no root rewrite.
Next physical Download when build ready; no functional reset claim yet.

RX0054: csr0800 DMAMODE survives, unsolicited count1 zero packets.
0113 PIO takeover locally tested (30 DMA enables clear+readback, CSR clear,
double flush); next combined CI includes0112 watchdog; root preserved.

ACTIVE:0054 flashed and CDC enumerated after50s; capture16470 waiting ACL.
User asked scoped setfacl again.0112 watchdog CI43744288276 from5eee9b2
running. Need install0055 later +a03_watchdog_disabled=1 after USB fix.

CURRENT0054 flashed BOOT-only100%/success/reboot; capture16470 waiting.
0112 opt-in disabled-watchdog capability locally tested; full CI pending.
0053 watchdogd missing IOWatchdog confirmed by runtime PC+matching BRK.
SpringBoard main CADisplay assertion decoded; no display patch yet.

CURRENT: CI43742555051 SUCCESS; BOOT0054 receive-diagnostic ready UNFLASHED.
Image e5082d921d19c084b63d0f46a2c369dda665e10b1196cf0f4e0d2b633614511a.
Exact CI source matches tested source;0053 loader/ADT/args preserved.
Await user physical Download; async request pending.0053 download has no
ACK/reset; need0054 RX state/packet evidence before next correction.

ACTIVE0053: USB reattached47s after flash;356191byte capture saved.
Download command hardware test FAILED: no ACK/reset despite host queue0.
Root retained;0053 still running, USB logs available.0111 receive diagnostics
CI43742555051 running fromf28fc71; do not claim reboot command functional.0108 watchdogd PC is
main Mach-O+0xb308, bt+0x58a4/+0x770c. Exact logs private.

ACTIVE 2026-11-15: BOOT0053 installed BOOT-only, upload100%/success/reboot.
Combined CI43740528122 PASS from69882d3. Image SHA256
bca699fb0e9c0ffdb164394898a6b38b19744d48d547d58466aec4dfd82c2377.
0052 loader/ADT retained, args only +a03crash_log=1, USERDATA root retained.
0110 adds exact USB command download outside PID1 hold, sync then fixed
SC2730 reset matching stock Linux. Host cumulative parser/supply/reset tests
PASS. USB capture33059 waiting; hardware reset still UNVERIFIED.


ACTIVE combined0108+0110 CI43740528122 from69882d3. Local crash/download tests and kernel compile PASS; BOOT0053 after CI.0052 lacks download command; initial physical Download entry needed.
ACTIVE iOS boot goal:0108 crash evidence completed/locally validated against
exact0052; mediaserverd/configd/lockdownd included, two reports per name.
Next full CI/BOOT0053 adds only kernel diagnostics +a03crash_log=1, retains
working0109 USB/root/loader/ADT. Need USB capture of reasons/PCs before fixes.


CURRENT USB0052 BULK LOG TRANSFER CONFIRMED after user tty ACL fix.
45second capture289235 bytes/5002 lines: private
shim/a03/out/boot0052-usb-perms-fixed.log. Supply PD1->0, voltage d2 retained;
configuration1 resets2 setups14. Actual XNU USB logs now available.
Crash lines confirm backboardd19/mediaserverd43/watchdogd17/configd8/lockdownd3
in that capture; no exact cause/PC. No stable GUI claim, no new flash.
Additional300s capture79265 writes boot0052-usb-continuing.log privately.
0108 remains unvalidated WIP; preserve it. See latest A03_PROGRESS.md.


USB0052 NOW ENUMERATES: host17:06:17UTC full-speed1d6b:0104,
A03XNUConsole01, cdc_acm ttyACM0. Bulk logs still unverified: EACCES.
User asked to run sudo setfacl -m u:stoned:rw /dev/ttyACM0 (sudo password
required; agent cannot execute). Then capture to NEW private log via
python3 tools/a03-usb-console.py --wait 5 --duration 60 --output PATH.
No reflash needed. Exact deployed USB source/general-regs flags verified.


CURRENT BOOT0052 USB candidate flashed BOOT-only100%/success/reboot.
CI43737353634 PASS from13baa99, kernel ae813082...81be, image26ef37cc...ade0.
Exact0051 loader/ADT/args retained; root preserved. Initial host no attach;
await supply before/after or failure, CORE/config/reset/setup screen lines.
Capture63236 /tmp/a03-boot0052-usb-capture.log (120s enumeration wait).
No hardware USB success yet.0108 remains unvalidated local WIP.


USB CI43737353634 running from13baa99 (0109;0108 WIP excluded).
Local real Mach-O object compile PASS.0052 will retain exact0051 ADT/cmdline,
USERDATA root, no RAMDisk. Await CI artifact and physical Download mode.


ACTIVE 2026-11-15: user resumed for XNU USB.0109 corrects matching-Linux gaps:
ANA_EB, explicit SC2730 USB3.3V supply/readback, flat endpoint registers,
USB pin mux and inherited host-force. Host CDC/supply/monitor tests and exact
CI BSD arm64 syntax PASS; no USB hardware claim yet. Next full CI, package
BOOT0052 preserving0051 root/args, BOOT-only test and host capture.
0108 daemon diagnostics stays local WIP; excluded from USB build/commit.


STOPPED AT USER REQUEST (2026-11-15). BOOT0051 still installed, root preserved.
Physical: watchdogd, backboardd and SpringBoard explicitly reported crashing;
output continues. Spawn lines: fairplayd, mDNSResponder, repeated xpcproxy;
bluetoothd/identityservicesd also appear. These latter names are not confirmed
crashes or successful startup. Launchd orchestrates daemons; no stable GUI.
Exact crash reasons/PCs absent; USB CDC still not enumerating.
Uncommitted WIP0108 bounded crash diagnostics + profile/workflow staging;
NOT validated/deployed. Syntax attempt blocked by absent ~/swift/usr/bin/clang
(after fixing old CI path privately). No CI0052/image/flash. Actual backboardd
imported ReVa /backboardd, not inspected. See final A03_PROGRESS.md entry for
scratch paths and validation needed. Preserve WIP; resume only when asked.


AUDIT0051: actual16.0 watchdogd connector0x1000057bc requires IOWatchdog,
open type1; exact deployed kernel nm confirms absent. Candidate root cause,
not yet observed specific error. Selector0=false selects own disabled/exit0
path. wdt_test is too late/internal gated/NVRAM-dependent; not a fix alone.
No provider/new build/flash yet pending screen evidence and other names.

CURRENT BOOT0051 user: Process[576] crashed watchdogd; Too many corpses being
created; output continues. Daemon orchestration reached beyond cache loader,
but unstable userspace. Exact watchdog error/other names requested; leave boot
running. Actual16.0 watchdogd extracted for ReVa; no speculative new flash.
USB0051 capture ended100s timeout/no CDC. Root preserved.

CURRENT BOOT0051 flashed BOOT-only100%/success/reboot after host Download
confirmation. Image fbe87658...fad23, same0050 kernel +literal
launchd_unsecure_cache=1. User reported prior bootloop during Download entry.
Await cache-loader/next screen lines or reboot state; no successful sustained
bootstrap claim. USB capture76745 at /tmp/a03-boot0051-usb-capture.log pending.
Root preserved; no host USERDATA/GPT/protected-partition write.

ACTIVE BOOT0050 physical: launchd_cache_loader abort Unable to find AMFI;
SIGABRT boot-task failure. Advanced past prior keybag failure; sustained
bootstrap unproven. ReVa actual16.0 loader confirms literal
launchd_unsecure_cache=1 skips absent AMFI IOKit trust registration via its
built-in lab path. BOOT0051 prepared, same0050 kernel/loader/ADT/root/font;
only cmdline + Android digest changed, full image comparison PASS.
SHA fbe8765853e9b542c61505b0fa2c677ee014311d50bf18e9be3ac932a11fad23.
Await physical Download transition (host not detected); then BOOT-only flash.
No root rewrite; no new AMFI service/full trust enforcement claim. USB unproven.

CURRENT BOOT0050 flashed BOOT-only100%/success/reboot. CI43730049732 PASS.
Kernel623931b2...384f3; image39b29808...72f19.0049 args+software keystore=1.
Provider symbols + actual boot-arg gate verified. Await user A03 AKS and
System Keybag loaded/final error lines; async question pending. Capture36560
/tmp/a03-boot0050-usb-capture.log ended100s timeout/no USB. Exact CI provider
source+general-regs flag audited. Await screen; root preserved, runtime unproven.

CURRENT0049 physical: keybagd fatal failed to load system bag, options
warning. Passed prior firmware mount failure; sustained boot unproven.
Kernel lacks AppleKeyStore; ReVa confirms actual iOS16 selector0/open and
14/get_system ABI.0107 local tests PASS; CI43730049732 running from09e658f.
Next0050 adds a03_software_keystore=1; root already has lab systembag plist.
Download detected; CI43730049732 Build active. No0050 flash yet.

CURRENT BOOT0049 flashed BOOT-only100%/success/reboot. CI43727113402 PASS;
kernel7cc96acf...651cb, image d93f2325...d1c18. Real bindfs_mount/vfsops
independently verified. Same0048 cmdline/root. Await final screen/mount-phase
progression; async question pending. Capture63535 to /tmp/a03-boot0049-usb-capture.log;
private console log only created if tty enumerates. Capture ended100s timeout/no USB. Await screen; no sustained boot proof.

CURRENT0048 physical: launchd runs boot task mount-phase-1, exits74 after
firmware bind mount ENODEV19. Old pthread trap passed; sustained boot not yet.
Kernel lacks bindfs_vfsops; A03 omitted portable donor0037. Profile now stages
0037, exact config apply PASS, CI gate requires symbol. CI43727113402 running fromfb777a0; next0049 BOOT-only.
No root reinstall. Download ready confirmed by user+host; USB console still absent.

CURRENT0048 audit: exact CI43724877490 ipc_port.c/.h +USB source match
locally tested files byte-for-byte; debug-hold call in actual kern_exit.c.
No USB/Download detected. Await pending screen report; no further flash or
USERDATA change justified until runtime evidence. Goal launchd still active.

CURRENT BOOT0048 flashed BOOT-only100%/success/reboot; CI43724877490 PASS.
Kernel f7f873be...0f5b4, image e9f8ee1d...6c6626.0047 args+ opt-in reply
compatibility=1. Markers + actual predicate disassembly verified. Capture
session45847 logs /tmp/a03-boot0048-usb-capture.log; private output
shim/a03/out/boot0048-usb-console.log if tty enumerates. Await user's screen
USB PHY/CORE/config/reset/setup + final launchd/TRAP lines. Root preserved.
USB capture45847 ended120s timeout/no enumeration; host journal only
Download disconnect. Await physical screen; no runtime improvement proven.

NEXT0048:0105 opt-in iOS16 SDK16 provisional reply compatibility only;
0106 matching A03 peripheral PHY/trim correction + register/counter logs.
Cross-compile/exact patch/192-case predicate/CDC/parser PASS. CI43724877490 running fromf8ecc37.
Add a03_ios16_provisional_reply=1 to0047 args. No new flash/root write.

CURRENT0047 evidence: construct4000/rv0/name603; invalid reply type21,
entry1/bits38200000/semantics3/dest4. Proven provisional-vs-strict rejection
before MIG, not missing receive right. CDC starts but host100s timeout/no USB.
Next scoped iOS16 reply compatibility + matching PHY audit. Hold unconfirmed.
Root preserved; launchd main unproven.

CURRENT: BOOT0047 flashed BOOT-only100%/success/reboot. Corrected CI43722354348
PASS; kernel e4b5d6cf...03752, BOOT b6b3e90b...8b8bb; USB/monitor/reply
markers independently verified. Args0046+console=1/debug_hold=1. Host capture
session91167 to shim/a03/out/boot0047-usb-console.log; check enumeration next.
No hardware USB/hold proof yet. Root preserved, launchd main unproven.


ACTIVE corrected CI43722354348 at8d25855: exact-source USB context fixed,
all USB/monitor/reply strings now required in CI.43720286686 artifact
contains0102 only (0103/0104 skipped), rejected/no flash. Device Download.


IMPORTANT:43720286686 green but USB0103+monitor0104 SKIPPED; DO NOT FLASH.
Artifact marker gate caught it; no phone write. Fixed context against exact
CI tree, sequential git apply PASS. CI now requires USB+hold marker strings.
Next corrected build, then BOOT0047 with args + console/hold. Device Download.


ACTIVE CI43720286686 at94edf70 (monitor+CDC+reply diagnostics), pending.
Supersedes43719832882 USB-only. Device Download detected. Next0047 after
PASS, add a03usb_console=1 a03debug_hold=1; start host capture first.
No new flash yet. Actual USB/monitor responsiveness unproven.


NEXT combined0102/0103/0104: buffered CDC + post-SIGTRAP inspection hold.
a03usb_console=1 a03debug_hold=1. USB OUT help/regs/bt/mem/panic; no shell
or resume. Local compile/protocol/parser/patch PASS; runtime unproven.
CI43719832882 builds USB only; supersede with monitor-inclusive build.


ACTIVE BUILD CI43719832882 at5694793: combined USB console + reply tracing.
Earlier43719778245/43719205319 superseded/cancelled. Download detected.
Final host checks PASS. Next BOOT0047 args0046+a03usb_console=1; launch
host tty capture before BOOT-only flash. Actual USB hardware unproven.


NEXT: combined0102 reply-right diagnostics +0103 USB CDC console mirror.
Local compile/patch/protocol PASS; USB hardware unproven. Add a03usb_console=1
in next BOOT0047. Screen retained; spool256KiB; serialA03XNUConsole01;
host tools/a03-usb-console.py. CI43719205319 builds0102 only; combine next.


CURRENT: user msg2 options0x200000003,size40,remote0x503,reply0x603;
no MIG. Invalid reply before dispatch.0102 logs reply rights/semantics and
PID1 port construct. Local two-file compile and patch checks PASS.
Next full build/BOOT0047; retain0046 args/root/font. No bypass.


CURRENT BOOT0046 physical evidence: x0=x8=0x10000009 =
MACH_SEND_INVALID_REPLY. host port x22=0x503; same pthread BRK after
unsliding PC by0x164d8000. Await A03 HOST msg2/MIG/priority lines;
investigate MIG reply TSD/right setup, do not bypass IPC validation.
User confirms XNU font fine. Root preserved; launchd main unproven.


CURRENT 2026-11-15: BOOT0046 flashed BOOT-only100%/success/reboot.
CI43717108507 PASS, kernel61b680de...bce7e; BOOTa813167e...4f205.
Adds0101 host_info/MIG/msg2 and preserved error x0/x8, host port x22 logs;
same0045 args/root/1x font. Await user A03 HOST and new TRAP register line.
Actual SIGTRAP is cached libpthread HOST_PRIORITY_INFO initialization;
error still unknown. Root preserved; no sustained launchd/main proof yet.


NEXT BUILD:0101 adds preserved host_info error x0/x8 and host port x22,
msg2/MIG/host count diagnostics. Local four-file compile PASS.
CI43717108507 running frome0e58a2; next package BOOT0046 on PASS.
Diagnostics only, no forced-success or security bypass. Download not detected.


CURRENT 2026-11-15: BOOT0045 trap symbolicated exactly: cached libpthread
PC0x1cdcfdf5c BRK#1, "BUG IN LIBPTHREAD: host_info() failed".
Observed slide0x19274000; LR0x1cdcf441c. ReVa caller0x1cdcf4050 sends
HOST_PRIORITY_INFO(flavor5), count8. Investigating Mach/kernel reply;
no bypass or new root install justified. Phone remains crashed XNU0045.
Next: establish error/host port/MIG response and fix cause, BOOT0046 test.
No launchd main success proven. Full16GiB verified root preserved.


CURRENT 2026-11-15 12:55UTC = XNU BOOT0045 flashed BOOT-only100%/success/reboot.
CI43714631683 PASS; kernel80cdfc51...c2653, BOOTa348ba5b...ad5a0.
Contains1x XNU font and pre-coredump SIGTRAP PC/LR, dyld/main bases, slide,
x19 text and frames. Same0044 args. Await user's A03 TRAP screen lines and
font-size confirmation; no actual launchd main success proven. Root preserved.

BUILD FIX: CI43712255840 failed due opaque Mach structs in BSD diagnostic.
Moved helper to osfmk/kern/exception.c; BSD only passes pid under SIGTRAP guard.
Exact failed buildtree/compile flags local syntax PASS for both affected C
files. Small-font retained. Corrected CI43714631683 queued at714d2da;
next package BOOT0045 after successful link, then BOOT-only test.
Current phone remains RO USB status0015; no new XNU flash yet.

ReVa audit saved: docs/a03-launchd-trap-analysis.md; exact live binaries
/ dyld and /launchd analyzed locally. Multiple distinct trap paths remain.
NEXT: scoped initproc SIGTRAP diagnostic0100 added before core dump;
prints PC/LR, dyld/main bases, cache slide, x19 text, instruction and frames.
Live read-only inventory PASS:40 subcaches/UUIDs,2663 images; launchd/dyld
bytes match pinned root. No core file exists. dyld_halt BRK0x5fcd0 retains
message in x19, but actual trap site UNKNOWN. Keep smaller font in next build.
Combined build CI43712255840 at3580c5b supersedes font-only43711774561.
No trust-cache bypass justified yet; missing-cache warning falls back to UID.

CURRENT BOOT = RO Linux USB status0015 (BOOT-only flash succeeded).
BOOT0044 advanced to dyld shared_region requests, then SIGTRAP namespace2/5.
Trust-cache warning falls back to root ownership; do not assume causal.
/cores/core.1 ABSENT in live read-only HFS catalog; /cores empty. USB reader
working, host ACL available. New tools/a03-read-usb-hfs.py reads guarded LUN1.
User wants XNU font half size, NOT USB: fixed A03 pinned0003 profile scale2->1.
CI43711774561 running from a92aa20; next package BOOT0045 with0044 args,
then Download/BOOT-only test. Actual launchd main execution still unproven.

CURRENT 2026-11-15 11:53UTC = BOOT0044 flashed BOOT-only100%/success/reboot.
SHA2f2dc75f...7f3131; same CI43708471929 kernel plus DEVELOPMENT iOS exec
option unentitled_ios_sim_launch=1 and launchdsuffix=release. Fixes observed
0043 EXEC WRONG_PLATFORM gate. Await physical allowing-spawn/launchd/dyld/panic
lines; no actual launchd userspace success proven yet. User asked via async.
Full16GiB root remains verified; no reinstall. Protected partitions untouched.

CURRENT: BOOT0043 screen panic launchd CS_KILLED namespace9/code0xe.
Exact XNU source identifies EXEC WRONG_PLATFORM, not invalid code page. Root
mount now passes; actual launchd userspace execution remains unproven. Prepare
BOOT0044 ready UNFLASHED SHA2f2dc75f...7f3131; same CI43708471929 kernel
+ unentitled_ios_sim_launch=1 and
launchdsuffix=release. Await Download; only BOOT update needed. No root reflash.

CURRENT 2026-11-15 11:48UTC = XNU0043 flashed BOOT-only/upload100%/reboot.
CI43708471929 PASS, kernel00c7cd3a...45018, BOOTedb76b9d...101e7e.
Adds a03_unsealed_root=1 with validated writable USERDATA rootdev guard;
fixes0042's post-mount root authentication panic. User asked for last screen
lines. Await actual HFS/launchd/panic evidence; no launchd success claim yet.
Do not reinstall fully verified16GiB root. Protected partitions intact.

CURRENT: XNU0042 mounts repaired USERDATA root, then panics at
bsd_init.c:946 rootvp not authenticated after mounting (user screen report).
No launchd execution yet. Added scoped unsealed-root patch0099, explicit
a03_unsealed_root=1, validated writable rootdev required; next build/BOOT-only
test. Commitd447b11 / CI43708471929 queued;96 host guard cases and GPT/BSD
harnesses PASS. Full16GiB root remains verified; do not reinstall it.

CURRENT BOOT11:16UTC = XNU0042, BOOT-only upload100%/success/reboot after
full16GiB root repair/readback and user confirmation nonzero catalog under
Linux. Await screen HFS/launchd output; user asked via async tool. Do not
repeat root install. USB status0015 display works (user verified counters).
Protected partitions intact. Apple launchd execution still unproven.


USB STATUS SCREEN VERIFIED: user sees read2MiB/written0MiB on0015. Counters
are per boot;16GiB root remains independently verified. Await Download for
XNU0042 BOOT-only retry toward actual Apple launchd execution.


CURRENT BOOT11:14UTC = RO USB status0015, BOOT upload100%/reboot/USB enumerated.
Full16GiB USERDATA root readback passed earlier. Await user's screen result
for new status/counters; then Download and XNU0042 BOOT-only launchd trial.


VERIFIED ROOT 2026-11-15 11:13UTC: session63894 exited0 FULL DEVICE READBACK
PASS eb72c14a9cf4aab30a8b49afda745a1b342dc877263d3b6a39901d95c89da108.
Entire16GiB root now matches source via O_DIRECT; catalog header/root correct.
No more root reflash needed absent new evidence. Current BOOT installer0011.
User asked visible USB status; status0015 RO image12915ef3...5c5ad4f ready,
unflashed. Await Download, flash status0015 BOOT-only, inspect screen/USB;
then boot XNU0042 (6c729a41...c6115) to test actual launchd. Protected
partitions intact. No Apple launchd runtime proof yet.


11:04UTC LIVE UPDATE: session63894 completed16GiB write (551.6s), now full
O_DIRECT readback (first1GiB done). Do not reboot/flash until FULL DEVICE
READBACK PASS. Next after pass: status0015 RO USB screen test, then XNU0042.


INSTALL LIVE 2026-11-15 10:54UTC: process session63894 is writing verified
16GiB root to exact validated USB USERDATA LUN1 /dev/sdc, serialA03LinuxInstallV11.
At10:58UTC ~6.5GiB written; do not reboot/flash. Follow same handle until
terminal result; full O_DIRECT SHA readback required. Catalog bytes now match
source locally but this is not full install proof. User requested visible USB
status; corrected DRM query arrays and added live state/counters. Host-only
status0014 RO/RW images built, unflashed; test after install/verification.


CURRENT 2026-11-15 10:53UTC: Linux USB storage works after absolute configfs
symlink fix. Independent host reads prove installed catalog header/root zero.
Current BOOT=installer0011 SHA7acfc1f50d01b86a760408f8fa748618429a07cdb8eeeecf64cb96e54986ccdb,
BOOT-only upload100%/reboot. USB serialA03LinuxInstallV11, LUN0=/dev/sdb1MiBRO,
LUN1=/dev/sdc54381228032bytesRW (only GPT-validated USERDATAp55, not whole card).
Await user host ACL r on sdb and rw on sdc; no root install started yet.
Run tools/a03-install-usb-root.py with rebuilt16GiB image and --write after
ACL; pinned source hash and USB identity/capacity/mount guards mandatory;
full O_DIRECT readback hash required. Device stays in installer for2hours.
Then return Download and flash XNU0042/0041 BOOT-only to test actual launchd.
No Apple launchd yet. Keep protected partitions intact.


LATEST 2026-11-15 10:46UTC: user read Linux mailbox: GPT CRCbb4c2987,
USERDATA start15929344 and CATALOG_HEADER@0x2cd82000 first32 all zero.
Independent stock Linux confirms installed catalog contents wrong, agreeing
with XNU. Reverified host16GiB root SHAeb72c14a...89da108. Remaining report
error link mass storage: ENOENT traced to configfs resolving relative target
from cwd. Fixed to absolute target; host candidate reader0009 SHA
8891c2434ab430f321ec9e49ec1bcb422561bc2deaf177fba267c745235dd2d3.
Await Download for BOOT-only USB retest; read-only LUN still enforced.
Current BOOT remains report viewer0001; no launchd execution.


CURRENT BOOT UPDATE 2026-11-15 10:43UTC: reader7 returned to Download;
report viewer0001 flashed BOOT-only/upload100%/success/reboot. Await screen
A03 STOCK LINUX REPORT or last mailbox/GPT failure line. Viewer halts before
XNU, does not write USERDATA and has no USB. Commits d9ff094/c381f54 saved.


## Latest A03 state — Linux diagnostic mailbox, 2026-11-15 10:40UTC

Reader5's automatic return to Download was observed by user and host: custom
stock-Linux PID1 executes. No Apple launchd result. USB/display still absent;
reader6 DRM trial also produced no visible text. Reader7 is currently flashed
(BOOT-only upload100%/reboot). It attempts a4096-byte report at validated
USERDATA offset16GiB, beyond HFS root, then returns to Download. Mailbox write
success unproven. NEXT: flash shim/a03/out/a03-linux-report-0001.img BOOT-only
SHA37030f0f68def716322a8f5e042b02b22a11dea72432467bb0e28741ad8eb412;
this pre-XNU shim validates GPT, reads mailbox, verifies magic/CRC, shows text
and halts. No other partition is authorized. Earlier no-USERDATA-write claims
refer only to pre-reader7 tests. Detailed hashes in A03_PROGRESS.md.


## Current A03 handoff — 2026-11-15, Linux reader pending

Current BOOT is Linux reader0001, NOT XNU0042. BOOT-only upload100%/reboot
succeeded; user reports Samsung logo; no USB. Linux init execution unproven.
V1 had an unjustified partition179:55 assumption, now fixed using sysfs.
Latest UNFLASHED reader0004: shim/a03/out/a03-linux-reader-0004.img SHA256
59ecbf0d2de5d58e77c36e6ae8e498c7e956b507f9c2f72221b5474a8e56db42.
Unchanged stock kernel/DT, no Android init or USERDATA mount, existing GPT
validator, partition O_RDONLY, USB RAM report LUN0 + read-only USERDATA LUN1.
FB0 output attempted using queried geometry. Host compile/GPT/BSD checks pass.
Next: return phone to Download, flash reader0004 BOOT-only and compare catalog
bytes using Linux MMC. No USERDATA/protected write this session. Matching
Magisk restore and XNU0042 remain available. Apple launchd has not run.

Latest photos confirm XNU0042 direct catalog-header CMD17 at0x1097c10 returns
zeros. Its second probe address0x1097d22 was wrong: node274*8192 gives relative
0x2cfa6000 / absolute LBA0x1098d30. Patch0098 fixed, needs fresh CI build.
Catalog-header zero evidence unaffected. Full evidence in A03_PROGRESS.md.


Latest BOOT0042 output identifies the A03 USB state: `A03 USB: AON
EB1=001eb8f3 RST1=00000000 PHY_TEST=00000000 PHY_CTRL=0000000a CTRL1=00000000
CLK_REF=00000000`, then `MUSB clock gated; controller not accessed`. AON reset
is released but the MUSB reference clock is disabled, so XNU USB is not yet a
usable diagnostic channel. The screen still reports HFS mount error 5; keep
USB clock bring-up separate from the catalog/eMMC investigation.

## Active A03 handoff — 2026-11-14

Latest screenshot `IMG_20261115_004550_780.jpg` still shows the same HFSX
catalog failure: GPT/USERDATA/BSD root and volume header pass, but catalog
node 0 is all zero (`offset #0 invalid`, BTOpenPath error 5). It is from the
older BOOT0031 diagnostic and does not include the direct catalog-root probe
added in `66af3d4`. Workflow `43655138104` is building the next BOOT-only
probe; wait for its output before any further USERDATA write.

Workflow `43656529029` succeeded after fixing `0098`'s malformed hunk. BOOT
candidate `a03-xnu-0042-d7c03ad.img` SHA256
`6c729a41d931fd2d151d42aaccf005b57d972206d410fbce7cb46da3a42c6115` was
uploaded BOOT-only via Heimdall to 100% and the phone rebooted. It includes
the direct reads at absolute LBAs `0x1097c10` and `0x1097d22`; await their
bytes. No USERDATA or protected partition write occurred.

Kernel-source audit of `android_kernel_samsung_a03/drivers/mmc/host/sprd-sdhcr11.{c,h}` found the existing SDMA command encoding was already correct: Linux's `set_trans_and_cmd()` produces `(cmd<<24)|0x003a0011` for a single-block read (data-present + R1 + read + DMA). The loader now follows two source-backed details that were missing: it enables SDHCI v4 64-bit system-address mode via HOST_CTRL2 (0x3e) bit 13, as Linux does in `sprd_sdhc_set_64bit_addr()`, and programs block size with the controller's 16-bit write at 0x04 (`0x7200`) before the 32-bit block count. Host build `A03_EMMC_SNAPSHOT=5 sh shim/a03/build-xnu.sh` passes. This is not yet device evidence; flash a BOOT-only diagnostic and inspect the new controller mode/SDMA result before changing USERDATA.

Corrected XNU build 43641820579 (commit 4e4873e) succeeded with the A03 USB/direct-catalog gates. Kernel SHA256 `f19877e2842a7cff12433efd770910174307decae7d6c92c6ab39142d03454a5`. Packaged local USERDATA-root candidate `shim/a03/out/a03-xnu-0040.img` with the verified iOS root and `rd=a03userdata0 rootrw=1`; image SHA256 `94e18760fe23c75b48f0ac17e1af42cde93d493645b2d3b9a8bfe348b709a9a2`. No device write yet; Download-mode state is required before a BOOT-only flash.

BOOT0040 was subsequently flashed BOOT-only after a clean Download-mode retry. Heimdall transferred the full 64 MiB image to `boot` at 100% and reported `boot upload successful`, then rebooted. USERDATA, GPT, recovery, bootloaders, EFS and NV were not written. At the first 10-second check no ADB or USB diagnostic enumeration was present; physical XNU/display output is still required. 

Workflow 43651725931 passed after repairing the dependent patch hunks and all A03 link gates (USB, direct catalog, and USERDATA-root guard). Kernel SHA256 `a3d8125d0a49290116a4ba1e3d7e1fe2d98276f5be4cf6f8df5f3840b356091d`. BOOT0041 was packaged with the emmc-enabled ADT and flashed BOOT-only; image SHA256 `428deca6e75ccccf1a38b0deada5ae152d756b045effe2ac1da05dcc55b67c35`. Heimdall reached 100% and rebooted. USERDATA/GPT/recovery/bootloaders/EFS/NV were untouched. Await physical or USB runtime evidence.

BOOT0041 screenshot `IMG_20261115_002428_609.jpg` identifies the remaining failure: XNU storage validation and USERDATA root selection pass, then HFS reports `hfs_swap_BTNode: offset #8 invalid`, `blockSize 0x200`, and catalog B-tree error 5. The local decompressed 17 GiB image used for the earlier USERDATA flash was sparse/zero-filled at catalog fork byte `0x2cd82000`. Rebuilding from the recorded gzip artifact restores prefix `00000000000000000100000300000003` and full SHA256 `eb72c14a9cf4aab30a8b49afda745a1b342dc877263d3b6a39901d95c89da108`. Next action is USERDATA-only reflash of the rebuilt image, then BOOT0041; no XNU storage code change is indicated.

CI optimization commit `6d0edaa` now caches the pinned `darwin-xnu-build`
checkout and the macOS 13.5 `KDK_13.5_22G74.kdk` (compressed under
`.kdk-cache`), while retaining ccache and parallel make. The first run after
this change seeds both caches; later A03 builds should avoid the XNU clone and
KDK DMG/install work. Kernel verification and BOOT-only bring-up scope are
unchanged.

BOOT0038 (commit da135e5; source 322bcba) was uploaded BOOT-only after workflow 43633349828 succeeded. Kernel SHA256 9cf66f9624b94a8a7b0f5837027ab5fcf016c70111869f33b5231572d94f4c6f; image SHA256 875033bc9c0948421919ea0e8bc41b94fbff3d7903a11c075b49e52403f740c4. Its eMMC trace is restricted to USERDATA base 0xf31000 and expected catalog LBA 0x1097c10; UIO prints the first four requests and catalog-window offsets around 0x2cd82000. Heimdall uploaded only boot at 100% and rebooted. No new photo is present in /home/stoned/ocr; the only photo remains BOOT0037's older broad trace. Await BOOT0038 screen output, especially A03 eMMC UIO and catalog-range TRACE lines.


BOOT0032 (`4ace15fb349f9c669f4a6bd51c5c7c84c25cb47f5ae0a1b05d37bfa65cdab287`)
was uploaded BOOT-only and rebooted. User reports raw/block catalog still
zero, both HFS headers `48580005800021004846534a00000081` (HFSX), and SWEET PID1
alive. This confirms readable HFSX header and storage data disagreement; no
HFS mount, launchd or SpringBoard. No USERDATA write was made.

Correction: inspection of workflow43620198151's actual build-tree proves it
omitted patch0093 (`a03_usb.c`, file-list entry and init call absent); its
`a03_ios_userspace` input was false. BOOT0032 therefore had no MUSB probe, so
“A03 USB nowhere visible” is expected and gives no controller-state evidence.
Workflow43622283937 did stage0093 with `a03_ios_userspace=true`, but its
build script silently skipped the patch because the `bsd/dev/mem.c` context
had one fewer tab than the target; its successful kernel still lacks the
probe. Fixed 0093 and verified `git apply --check` against the actual
post-0092 build tree. Added a workflow post-build gate requiring
`A03 USB: AON` in the kernel. XNU run43623709272 PASS; log confirms patch0093
applied and build-tree includes `bsd/dev/a03_usb.c`. Kernel hash
`8611e248a6b6ade4c95e9c77649d18b0d95cb8beba8a1cfc1e09263b37d9f006` contains
the probe strings. BOOT0033 (`48eb01ea5428c3e2eab9e5c69c4c7cedb9013d6ec9b6baf3b6612ab4862bf842`)
was uploaded BOOT-only and rebooted; it runs RAM HFS root, eMMC read-only,
catalog/header tests and the MUSB state probe. Await screen `A03 USB:` and
catalog/header results. Host currently sees no Download/ADB device. Preserve
GPT, recovery, bootloaders, EFS/NV; continue BOOT-only trials. MUSB
enumeration/log channel is not yet implemented.

LATEST BOOT0033 REPORT: raw/block catalog remain zero; raw/block HFS headers
both begin `48580005800021004846534a00000081` (HFSX); SWEET PID1 remains alive.
No `A03 USB:` register lines were supplied. Local image catalog prefix is
known at relative `0x2cd82000` (LBA `0x166c10`, absolute card LBA `0x1097c10`),
so next storage diagnostic should read adjacent catalog sectors and print both
LBA forms. This distinguishes an incomplete USERDATA transfer from a high-LBA
SDMA/address fault. No iOS root, launchd or SpringBoard result.

Added opt-in XNU eMMC trace patch0094, gated by `a03emmc_trace=1`, to print
absolute command LBA and first four data bytes for high-LBA reads. It changes no
storage state and applies to the corrected post-0092 build tree. Packer/profile
have the trace flag. Workflow43625945895 linked the trace strings; BOOT0034
was flashed BOOT-only and rebooted. The reported local image's expected
catalog bytes remain nonzero; physical trace output is still missing.

BOOT0035 deployed from workflow43627631857 (kernel
`3a53e8216150a78584022c5a9cb2ab696241ff72292d83cee71175e7e2b09bad`, image
`0956a223313ef84cd09744f7a0b20d135e9aa52518400576f986195c9594666d`). It adds
the UIO offset trace and an unconditional USB probe-entry marker. Heimdall
uploaded BOOT-only successfully and rebooted; await `A03 eMMC UIO`, `TRACE`,
and `A03 USB` lines. No USERDATA/protected write.

NEW PHOTO162431: XNU reports root a03userdata0 (major2/minor1), enters
vfs_mountroot, then invalid catalog B-tree fileID4 / BTOpenPath error5 /
hfs_mountroot errno5 / cannot mount root errno19. eMMC later reports ready,
USERDATA RW and BOOT RO. Root selection is confirmed; HFS mount and userspace
are not. No Apple launchd/SpringBoard claim. Added opt-in RAM-root PID1
catalog probe: pread 512 bytes at USERDATA offset0x2cd82000 via raw+block,
print first16, compare known image prefix. Root CI43611194283 PASS.
BOOT0027 prepared SHA79bea0b10029b368b763e5d6bc12340b3cd52b825dce6db3e3a204b7b5dc20fc,
root SHA525293710b033e7d149d600a6d41d51fe18cdc3b8bbc784bdca9e2795938827b;
kernel43602657100 reused, SHA124d32ca...605f1d80. Heimdall detected
Download USB and one live PIT read confirmed60-entry SPRD PIT/USERDATA ID55.
Subsequent PIT/flash protocol attempts time out at handshake (Result -7),
before transfer. No partition write. Need clean Download USB session, then
flash BOOT only, compare raw/block catalog bytes before changing USERDATA.

USB reset re-enumerated the A03. BOOT0027 then transferred100% to `boot`
(`boot upload successful`) and `close-pc-screen --resume` rebooted it. No
USERDATA/GPT/recovery/bootloader/EFS/NV write. Eight seconds later no
Download/ADB USB had re-enumerated; no catalog/PID1/HFS/userspace evidence.

Correction: BOOT0027 selected USERDATA as root, so HFS failure could precede
the diagnostic PID1. Prepared BOOT0028 with `rd=md0` RAM root plus `a03emmc=1`
and the same read-only catalog probe. SHA
`e99ec4100f5a00028b5d24fc29b80e1e1ab5acd74c447af8100062923ede38ae`.
New photo165241 again shows invalid catalog B-tree, HFS
mount failure and no userspace; it adds no raw/block bytes. Lower diagnostics
show BSD eMMC devices ready. A03 returned to Download; BOOT0028 transferred
100% to `boot`, then reboot completed. Ten seconds later no Download/ADB
enumeration. Await screen log for RAM-root PID1 raw/block catalog result;
do not alter USERDATA before that comparison.

USER PID1 RESULT: BOOT0028 printed raw and block catalog first16 as MISMATCH
with sixteen zero bytes. Both reads completed at offset0x2cd82000; verified
image bytes there are 00000000000000000100000300000003. This isolates the
failure below HFS and implicates SDMA/addressing or installed USERDATA data.
No USERDATA write occurred. Next read/compare volume header at offset1024,
then inspect partition-LBA translation before rewriting the filesystem.

USER PID1 RESULT: BOOT0028 catalog probe printed raw and block first16 both
MISMATCH plus 16 zero bytes. Reads completed but returned all-zero data at
offset0x2cd82000, while verified image bytes there are
00000000000000000100000300000003. This isolates the failure below HFS and
implicates SDMA/addressing or installed USERDATA contents. Correct the probe
constant (the prior expected bytes were wrong), then read volume header at
offset1024 before any USERDATA rewrite.

BOOT0029 fixes that expected catalog prefix and was flashed BOOT-only from
CI root43613676224. SHA
`fffe78294bb3639f1db0fa1caf6420c0ec44649a160fea18f108a6ba00d900a6`.
Reboot completed; after10s no Download/ADB. Await corrected probe output.
PHOTO170949 confirms BOOT0029 reached XNU RAM root: `BSD root: md0`, HFS
mounted `A03TestRoot`, BSD/devfs completed, and `SWEET userspace: init
running as PID 1` / `still alive` appeared. eMMC reports GPT CRC
bb4c2987/bb4c2987 and BOOT+USERDATA devices ready. This proves XNU/PID1,
not iOS launchd/SpringBoard or USERDATA HFS. BOOT0029 lacked explicit
catalog_probe input; workflow43614257862 is dispatched for that test.

Workflow43614257862 completed catalog-enabled root. BOOT0030 packaged with
root SHA3b71db2687bfe6de8a3096157d973271de8f78e3817457aad05d8ad8595af519,
image SHAa4b545af50a80a5613c461e0e02404b784d489778af22d1a27bb66190c6d28fc.
Phone was not in Download after PHOTO170949, so no flash yet; USERDATA
untouched. Flash BOOT0030 only when Download returns.

BOOT0030 was then uploaded100% to `boot` and rebooted with Heimdall.
USERDATA/protected partitions untouched. After8s no Download/ADB; await
display/PID1 catalog output.

User reports PHOTO171705 still shows catalog bytes zero. Raw/block reads
complete but return zeros at offset0x2cd82000; no header result yet. Added
opt-in header probe at USERDATA offset1024, locally compiled in header-only
and combined modes. See BOOT0031 below for the CI build and BOOT-only flash.
Inspect partition-LBA/SDMA transfer addressing and obtain raw/block HFS-header
evidence before any USERDATA rewrite. No HFS mount, iOS launchd, or SpringBoard
result.

Header+catalog CI43615216691 PASS. Root SHA b266c456151780842025a1e14137f5b416650d2feca71677dc34a13131f34893.
BOOT0031 SHA ea83109030122cc23a7055e85f828f6a93fa479cd3262307f4ca3029cf3bade3,
kernel43602657100, cmdline rd=md0 a03emmc=1. Heimdall PIT read succeeded and
only lowercase `boot` uploaded100%; reboot completed. USERDATA/protected
partitions untouched. USB absent after reboot. Await physical raw/block HFS
header and catalog output; do not infer mount or SpringBoard.

After PHOTO171705, BOOT0031 output: user reports catalog still zero; HFS
header raw first16 `48580005800021004846534a00000081`, and block reports HFSX;
SWEET PID1 remains alive. This proves the expected volume header is present
at USERDATA offset1024, but the catalog-sector mismatch remains. Restored the
known Magisk BOOT only while attempting a direct Android raw-sector check.
Correction: this replaced the XNU shim; no shim was reflashed afterward, so
the recovery boot is expected and says nothing about XNU or Android `/data`.

Image artifact `a03-ios16-root.img.gz` from CI43604313047 was downloaded and
decompressed outside git. Full raw SHA
`eb72c14a9cf4aab30a8b49afda745a1b342dc877263d3b6a39901d95c89da108`; fsck.hfsplus
-fn PASS. Direct bytes: header@0x400=`48580005800021004846534a00000081`,
catalog@0x2cd82000=`00000000000000000100000300000003` (allocation block183682,
4096-byte blocks). Reflashed exact image to USERDATA only; display showed
`SW REV CHECK FAIL : [userdata]`, transfer nonetheless reached100% and
reported `userdata upload successful`. No readback, so catalog contents on
device remain unknown. The transfer rebooted the phone; current recovery
boot has Magisk BOOT, not the shim. Return to Download, flash BOOT0031 only,
and rerun the read-only catalog/header test. No GPT/recovery/bootloader/EFS/NV
write.

Returned to Download after the USERDATA reflash. BOOT0031 was re-flashed to
`boot` only (same SHA ea83109030122cc23a7055e85f828f6a93fa479cd3262307f4ca3029cf3bade3);
PIT read and upload100%/`boot upload successful`, then reboot. Waiting for
post-reflash catalog/header output. This is the required XNU shim after the
Magisk restore; no other partition was written.

User requested USB in XNU to eliminate photo transcription. A03 is Qogirl6
MUSB (`sprd,qogirl6-musb`) at0x64900000, PHY0x64570000, AON APB0x64000000;
Linux source confirms `dr-mode=peripheral` and OTG UTMI clock gate APB_EB1
bit8. Do not reuse donor DWC3/Qualcomm code. Added opt-in read-only kernel
register probe patch0093 plus `--usb-probe` boot-arg support, validated patch
application after0090/0092. It is not enumeration or data transport yet.
Build/device check the probe, then implement MUSB EP0 and a bulk vendor
channel for logs/sectors. Post-reflash BOOT0031 catalog result is still
missing; no USB-related flash has occurred.

BOOT0026 and the USERDATA image were installed as described below. The
162431 photo proves the phone subsequently booted far enough to reach XNU's
HFS root-mount path; current physical/USB state is unknown. USERDATA
ID55 16GiB HFSX upload100%, then BOOT0026 upload100%. Heimdall logged
`userdata upload successful` and `boot upload successful`; no independent
partition readback/hash. USERDATA image SHAeb72c14a...89da108 and full
read-only fsck/catalog/cache/binary/hash checks PASS. BOOT0026 SHA
e012784bf236bae131029b02c0a5239546081eebb039852e9de64a465528086b.
Kernel43602657100 SHA124d32ca...605f1d80; cmdline rd=a03userdata0,
a03emmc_rw=1, rootrw=1, ignition_level=1, -nobsdmgroot.
Both writes authorized, no GPT/recovery/bootloaders/EFS/NV touched.
Heimdall close-pc-screen protocol init failed; --resume retry and BOOT-only
reflash/normal reboot also failed session startup. USB disappeared after the
physical key power-cycle and had not re-enumerated by15:23UTC. The later
162431 photo establishes a subsequent XNU boot attempt and failed HFS mount;
it does not establish current USB state. Avoid another write until state is
known. Apple launchd/SpringBoard runtime not observed. Preserve0024,0025 and
stock Magisk restore94fa7c53...15e9ce7.

MILESTONE0025 USER CONFIRMED USERDATA WRITE PASS changed/readback/restored/
fsync sector16GiB, raw+block BOOT reads/write-open EROFS PASS. Preserve0024
and0025. No eMMC filesystem mount/Apple launchd/SpringBoard established yet.
Scope authorized USERDATAp55 +BOOT; preserve GPT/recovery/bootloaders/EFS/NV.
Local readonly source APFS-FUSE remains research/a03-ios16-source/{os,sysos}/root.

MILESTONE0024 USER CONFIRMED: raw+block BOOT-header read/write-open EROFS
PID1 PASS. XNU SDMA/cache/BSD read path established. Preserve0024 image
SHAa4240b22...73b53b9c, kernel43598578558/root43597035152. Still HFS RAM
static init, no USERDATA filesystem root/Apple launchd/SpringBoard. Next
locate supplied iOS assets and adapt root+portable entitlements, then
Apple userspace and graphics. No new flash; BOOT-only scope retained.
Earlier pending physical-result entries below are historical.


Offline root inventory tools/a03-inspect-ios-root.py added; actual test
root correctly fails dynamic-launchd requirement. No iOS source assets in
checked local paths; need existing IPSW/root location. Profile AMFI0025
lacks donor0035/0036 entitlement/platform/CS_SIGNED support. No device
output/new photo in latest check;0024 physical result still required.

CURRENT0024 FLASHED: fresh Heimdall PIT/boot100%/upload success/reboot exit0.
Image SHA256a4240b2222a59099fe436a6b33348b9c6ebbed768d9a98ec2f00168e73b53b9c.
No independent readback. Corrected d_psize512 kernel43598578558 SUCCESS;
same diagnostic root43597035152. Await raw+block header PASS and full
PID1 storage PASS/write-open EROFS, or exact stage/value/panic. Current
root is HFS RAM test init; no Apple launchd/eMMC-root/iOS GUI. Prior READY
and live-CI notes historical.


0024 READY: CI43598578558 SUCCESS; kernel SHA6880a6c0...d30dc41.
Compiled emmc_psize512 verified, integer-only storage+uiomove retained.
Image shim/a03/out/a03-xnu-0024-sector-size.img SHA256
a4240b2222a59099fe436a6b33348b9c6ebbed768d9a98ec2f00168e73b53b9c.
Same diagnostic root43597035152, ADT+a03emmc=1 rd=md0. Next BOOT-only
flash and physical raw+block/EROFS PASS. Current0023. Older CI notes historical.

FIX39d7a06 PUSHED; kernel CI43598578558 confirmed live/Deps. Phone
Download available. Reuse diagnostic root43597035152(hash revalidated).
On CI success inspect integer-only storage code and emmc_psize512, package
0024 with opt-in ADT+a03emmc=1 rd=md0, BOOT-only test. No new flash yet.

0023 USER stage21/value16 = buffered read EINVAL. Raw BOOT header passed
by diagnostic control flow. Root cause confirmed in specfs: d_psize means
sector bytes, ours returned partition count131072>PAGE_SIZE. Fix512,
capacity still DKIOCGETBLOCKCOUNT; no hardware changes. Host sanitizer
16K request+callback regression passes and rejects old code. Patch sync/
dry-run + GPT pass. Next corrected XNU CI, reuse root43597035152 for0024.
Current0023. Full block+EROFS storage PASS pending.


CURRENT0023 FLASHED: Heimdall boot100%/success/reboot exit0. Image
shim/a03/out/a03-xnu-0023-storage-stage.img SHA256
31a19aeb5aa25bccbd18a577bd38694e60dddc10bd8cdee664b974610e28d143.
Same corrected kernel43590138639; diagnostic root43597035152 verified
fsck/catalog/hash. Await raw/block PASS lines and FAIL stage/value in hex.
Stages10..15 raw,20..25 block: open/read errno, short bytes, magic,
page size, header version.30 write-open errno(expected1e),31 unexpected
write-open success. No sector write. Prior pending root/build notes historical.


ROOT DIAGNOSTIC CI43597035152 at64a3cf8 SUCCESS(storage_probe=true).
Actual ARM64 emulation PASS+14 failure stages; default init unchanged.
Fresh Download USB detected. Reuse kernel43590138639, package0023 once
root fsck/catalog hash verified. No new flash.

0022 USER REPORT: static PID1 prints generic A03 STORAGE PID1 FAIL.
No raw/block PASS established, no new panic reported. Preparing root-only
stage/value diagnostics for0023 with unchanged corrected kernel43590138639.
Need exact syscall/check failure before hardware changes. Current0022.
Prior pending physical-result lines below are historical.


CURRENT0022 FLASHED: Heimdall PIT/boot100%/successful upload/reboot exit0.
Image SHA256df392a526999866b4c170dbc612955a900952191519223d0f444635a597c4a34.
No independent readback. Await physical A03 STORAGE PID1 PASS:
raw+block BOOT reads, write-open EROFS; or exact panic/last line.
Raw uiomove fix3f77331, kernel CI43590138639 SUCCESS. Same verified HFS
RAM root; no Apple launchd/eMMC-root result. Prior READY notes historical.


CORRECTED0022 READY: CI43590138639 SUCCESS; raw uiomove call verified,
integer-only storage text, BSD/GPT tests pass. Image
shim/a03/out/a03-xnu-0022-sdma-uiomove.img SHA256
df392a526999866b4c170dbc612955a900952191519223d0f444635a597c4a34.
Same verified root43588996330; explicit ADT+a03emmc=1 rd=md0. Restore
hash verified, fresh Download detected. Next BOOT-only flash; current
0021 panic. Await physical raw+block PID1 PASS or exact failure.
Prior CI/pending0021 entries below are historical.


Fix3f77331 PUSHED; corrected-kernel CI43590138639 confirmed live/Deps.
Phone Download USB available; no new flash. Reuse root43588996330
(hash verified), explicit emmc ADT and a03emmc=1 rd=md0. Once CI passes,
download kernel, inspect storage integer-only code/call to uiomove, package
0022 and BOOT-only test. Current0021 panic PC proves strategy copy reached;
full storage PID1 PASS pending.


0021 PANIC user PCfffffe00074d8fb0 maps exact kernel to emmc_strategy
byte store into buf_map raw user pointer, after data_read success. Local
XNU buf_map leaves noncluster b_datap unchanged; physio uses user iovec.
Fix raw cdev to uiomove, reject B_PHYS in buffered strategy; hardware
sequence unchanged. Host actual-handler ASan/UBSan tests + GPT pass.
Next CI corrected kernel, reuse verified HFS root43588996330, package0022.
Current0021; no complete storage PID1 PASS/Apple launchd yet.


Latest0021 FLASHED: Heimdall PIT/boot100%/successful upload/reboot exit0.
Current0021 SHA2567753f418de5b7dd8c5db245e49c439d743c76691ee350a96d6fac22c289aafe7.
No independent readback. Await XNU SDMA probe/DMA PA/GPT result0/nodes
and A03 STORAGE PID1 PASS raw+block BOOT/EROFS-open or exact failure.
HFS RAM root retained; no eMMC writes, Apple launchd or iOS GUI yet.
Earlier READY/current0020 notes historical. CI43588264792 and root
43588996330 succeeded; kernel+root packaging evidence d238751.


XNU43588264792 PASSED; storage text verified integer-only.0021 READY
shim/a03/out/a03-xnu-0021-sdma-bsd.img SHA256
7753f418de5b7dd8c5db245e49c439d743c76691ee350a96d6fac22c289aafe7.
Normal loader + verified HFS storage-test root43588996330, explicit ADT
node+a03emmc=1 rd=md0. Fresh Download detected; next BOOT-only flash.
Await XNU DMA PA/GPT result/nodes and PID1 raw+block/EROFS PASS. Current
0020. No XNU SDMA behavior or Apple launchd yet. Older CI notes historical.


Root43588996330 SUCCESS: HFSX fsck clean, catalog launchd exact storage
test init hash979becf2...65cd0d. Root under shim/a03/out/root-43588996330/.
XNU43588264792 remains live/in_progress/Build. Packer --emmc-readonly
requires exact ADT node and adds a03emmc=1; rd=md0 retained. No flash.


XNU SDMA run43588264792 at b3d9772 is in_progress/Build (verified).
Opt-in PID1 raw+block BOOT-header/EROFS-open check prepared; compiles
without relocations, default init hash unchanged. Next root workflow with
storage_probe=true, download kernel on success, inspect a03_emmc codegen,
package with --emmc-readonly ADT + a03emmc=1 rd=md0. Current0020 PASS.
No XNU SDMA/runtime claim yet; do not flash while CI/artifact unverified.


XNU integration staged (NOT BUILT/FLASHED): profile0090 adds opt-in
a03emmc=1 plus explicit ADT --emmc-readonly node, private permanent DMA
page/cache maintenance, bounded retained-state SDMA, GPT validation and
read-only BOOT/USERDATA BSD nodes. Keep rd=md0/HFS RAM root. High-address
DMA (>4GiB), XNU cache/MMU and BSD access remain physically untested.
Timeout poisons reader permanently; no reset/retry/card configuration or
sector writes. Local patch/ADT/parser checks pass; next CI compile.
Current0020 confirmed storage identity PASS + BOOT512-byte match; gap7.


MILESTONE0020 USER CONFIRMED: STORAGE IDENTITY PASS, BOOT HEADER +512
PAYLOAD BYTES MATCH; USERDATA tail gap7 sectors. GPT integrity/ranges/
identities and current BOOT sample verified. Not full BOOT readback or
XNU driver yet. Current0020 paused before XNU. Next: opt-in bounded SDMA
XNU reader with cache/physical-address handling, preserve HFS RAM root.
All non-BOOT partitions preserved. Prior pending0020 notes historical.


Latest0020 FLASHED: Heimdall protocol/PIT/boot100%/reboot exit0. Current
BOOT0020, no independent readback. SHA256
e7b647a5d7ff4fd7658bd4cedc8c77010652762306fb62dfd54c43d7b1ade896.
Code/tests4046c65. Await photo lower rows64..78: GPT CRC/result, BOOT header
+512 payload-byte match or failure and USERDATA tail-gap value.0019 proves
array CRCbb4c2987 + partition ranges; only exact-end assumption was wrong.
No XNU provider/Apple runtime yet. Prior prepared/current0019 notes historical.


0019 photo IMG_20261114_115151_999.jpg CONFIRMS GPT array CRCbb4c2987
match, all bounds/nonoverlap, boot/start/size/index and userdata/start/index.
Only mismatch80: unsupported assumption userdata ends exactly last-usable.
0020 removes exact-end requirement (bounds remain), prints tail gap and
proceeds to current BOOT header+512-byte sample comparison. Actual-C tests
including legal tail gaps pass; no relocs/SIMD, exact0012 payload unchanged.
Ready shim/a03/out/a03-xnu-0020-gpt-boot.img SHA256
e7b647a5d7ff4fd7658bd4cedc8c77010652762306fb62dfd54c43d7b1ade896.
Current0019; fresh Download detected. Prior pending0019 notes historical.


Latest0019 FLASHED successfully: fresh detect, verified SHA256
1cf7617b30af133355a64c884c3250602ebeffc3b96f552f33f86b62ca4d6388,
Heimdall PIT/boot100%/reboot exit0; no independent readback. Current0019.
Code/tests6a71956. Await photo lower rows64..77: array CRCs/result, BOOT
and USERDATA starts/counts, identity mismatch bitmask, zero-based indices,
last usable.0018 result3 remains unresolved; no XNU storage provider yet.
Prior PREPARED/NOT FLASHED/current0018 notes below historical.


0018 physical photo IMG_20261114_114702_077.jpg: GPT header CRC matches,
array storedbb4c2987/computed0/result3. Parser stopped on identity before
finishing array; computed0 is unset, not a real CRC. BOOT compare not reached.
0019 prepared to finish CRC and show mismatch mask + actual starts/counts/
indices/last usable; constraints unchanged, read-only bounded SDMA. Candidate
shim/a03/out/a03-xnu-0019-gpt-details.img SHA256
1cf7617b30af133355a64c884c3250602ebeffc3b96f552f33f86b62ca4d6388.
Host actual-C tests, Werror, no relocs/SIMD, exact0012 payload pass. Fresh
Download detected; BOOT-only flash next. Current0018. Prior notes historical.


Latest0018 FLASHED: Heimdall --resume PIT/boot100%/reboot successful, exit0.
Current BOOT0018 image SHA256
2b6683c9cd2d29a1536a7037b02d5e681b038a6ddb32ed457218cc42029d0d67.
No independent readback. Code/tests commit9327668. Await physical full
screen through row77: GPT array CRCs/result, BOOT+USERDATA starts/counts,
BOOT header and512 payload-byte match or guard/failure. No runtime success
inferred from flash. XNU storage provider and Apple runtime remain pending.
Prior PREPARED/NOT FLASHED notes below are historical.


Latest0018 PREPARED: mode5 primary-GPT entry CRC/range/overlap checks, live
PIT boot483328+131072/index38 and userdata15929344/index54, then current
BOOT header plus512 payload bytes. Bounded read-only CMD17, pauses before
XNU. Host C parser malformed-input tests and modes0/3/4/5 Werror builds pass;
no relocs/SIMD, exact0012 kernel/HFS payload unchanged. Image
shim/a03/out/a03-xnu-0018-gpt-boot.img SHA256
2b6683c9cd2d29a1536a7037b02d5e681b038a6ddb32ed457218cc42029d0d67.
NOT FLASHED yet. Private live/current.pit retrieved --no-reboot; active
Download session needs --resume for next BOOT-only flash. Request full
screen through row77 after test. No XNU block provider/Apple launchd yet.
Prior handoffs below historical.


MILESTONE0017 confirmed by photo IMG_20261114_113809_312.jpg: SDMA reads
EXT_CSD + user-area LBA0/1. EXT REV8 PARTITION_CONFIG8 SECTOR_COUNT0747c000
DATA_SECTOR_SIZE0; MBRaa55; GPT header stored/computed CRC040a1bb6 MATCH.
All CMD8/17 R1900 INT2 PRESENT01f000f0. First validated eMMC sector access!
Current0017 paused before XNU; no new flash or writes.0012 HFS RAM PID1
remains separate checkpoint; no XNU block provider/Apple launchd/GUI yet.
Next read-only: bounded GPT array CRC/labels/sizes validation, then known
BOOT sector match against CURRENT0017 image (BOOT changed since backups).
Do not use Magisk BOOT bytes as expected current content. Keep storage
writes disabled, preserve all non-BOOT partitions. Local downstream source
is authoritative; unsupported generic PIO route superseded by SDMA.
Prior pending-runtime notes below are historical.

Latest0017 SDMA diagnostic FLASHED: reviewed v2 SHA matched
3b15409996e43a52729383f1c06f37bbe242d04c5fa9958732899ac22ed3c8a4,
heimdall detect/PIT/boot100%/reboot successful, exit0. No readback.
Current0017. Await physical metadata/GPT results or fail-stage/poll/DMA
WORDS COPIED/buffer-address values; no SDMA data success inferred yet.
Prior NOT FLASHED language below is historical.

Latest0016 report: fail2(read-ready),seen3,last2,present01f000f0,FIFO0,
enable037f000b,command083a0013. No data success. Downstream sprd_send_cmd
always sets if_dma=1; no PIO data path. Generic PIO assumption was wrong.
Live transfer-mode0x13 vs requested0x10 corroborates need for DMA path.
Prepared0017 mode4 using sprd_sdmd_mode register sequence: SDMA select0,
v4 buffer0x58/5c, aligned dedicated512B loader buffer, read direction only.
Require MMU/cacheoff/version4/HOST2v4+64bit, bounded poll, halt after trial.
CMD13->EXT_CSD->guarded LBA0/1 and GPT CRC unchanged; no card/storage writes.
READY NOT FLASHED: shim/a03/out/a03-xnu-0017-sdma-read-v2.img SHA256
3b15409996e43a52729383f1c06f37bbe242d04c5fa9958732899ac22ed3c8a4.
Non-v2 candidate superseded, never flashed. No Download USB at check.
Next fresh Download, BOOT-only flash v2; request metadata or fail stage,
DMA WORDS COPIED/buffer address/poll lines. No CI/kernel build needed.
Evidence/reference local android_kernel_samsung_a03 only. Current0016.
Prior handoffs are historical.

Latest0016 FLASHED successfully: detected, SHA verified
830bf41e70460aeed768aaf0af86fcbf1caf175d1eb3ecb435d37f78e3a41fb9,
Heimdall PIT/boot100%/reboot exit0, no independent readback. Current0016.
Await full-screen photo including low rows65..71: FAIL STAGE, POLL SEEN,
POLL LAST, POLL PRESENT, FIFO WORDS, INT ENABLE LIVE, COMMAND LIVE.
No runtime claim yet; NOT FLASHED notes below are historical.

Latest physical0015 photo IMG_20261114_112553_338.jpg: CMD13 OK, CMD8
READ R1=900 INT=2 PRESENT01f000f0, EXT_CSD FAILED/STOPPED. Transfer-complete
bit without error bits, but helper failure; stage/FIFO progress unknown.
No EXT_CSD or sector success. Do not claim read-ready was absent yet.
0016 READY NOT FLASHED: shim/a03/out/a03-xnu-0016-pio-stage.img SHA256
830bf41e70460aeed768aaf0af86fcbf1caf175d1eb3ecb435d37f78e3a41fb9.
Same guarded PIO path, extra fail-stage/seen/last/PRESENT/FIFO count/live
enable+command diagnostics at screen rows65..71. Need full-screen photo.
No Download USB now; user must re-enter. Then BOOT-only flash0016.
Host compile/no-relocs/integer-only/exact kernel+root payload verified;
no CI. Current BOOT0015. Reference only local android_kernel_samsung_a03.
Prior handoffs below are historical.

Latest0015 FLASHED, boot100%/reboot/exit0, SHA256
94c7832e02d5452410bfc2c82fc83f389a514f4f869b61c2897de682d8a18197.
User confirms0014 CMD13 INT1 RESPONSE900 PRESENT01f000f0 and glyph fix.
RCA1 responds ready/TRAN. Mode3 now fresh CMD13 -> EXT_CSD CMD8 PIO ->
only if user partition/512-byte sectors/capacity/revision guards pass,
CMD17 LBA0/LBA1 with MBR signature/GPT header CRC checks. No card config
changes, DMA, resets or storage writes. All references local cloned A03
Linux source as user requested. Each poll bounded, stop on failure.
Await screen EXT REV/PARTITION_CONFIG/SECTOR_COUNT/DATA_SECTOR_SIZE,
READ R1/INT/PRESENT, MBR and GPT CRC or final failure marker/photo.
Trial pauses before XNU. No PIO/sector success inferred yet. Same0012
kernel/HFS payload; no CI. Host CRC checked against zlib, build/codegen
checked. Only BOOT written, no independent readback;0012 fallback retained.
Prior trial handoffs follow as history.

Latest: BOOT0014 CMD13 diagnostic FLASHED, Heimdall detected device, image
hash matched17b1299ee4387b52eeba7a1a25c15a85495a5b9e5a9f2d76896a6f11ac42f48f,
PIT/upload boot100%/reboot all successful, exit0; no independent readback.
Await user CMD13 INT/RESPONSE/PRESENT/result or guard-skip/partial line,
and glyph orientation. Intentional pause before XNU. No runtime result yet.
Prior preparation notes follow; NOT FLASHED language below is historical.

0013 physical snapshot RECEIVED (all values in A03_PROGRESS.md). MMIO works,
PRESENT01f000f0 CLOCK7 HOST20 HOST23005 VERSION4 ARG10000 CMD0b1a RSP900.
Interpretation: clock enabled/stable, no inhibit,8-bit HS200, retained
TRAN+ready response; candidate RCA1 not yet confirmed. Not sector access.
User reports mirrored glyphs: loader MSB-first font rendering corrected.
0014 prepared, NOT FLASHED (no Download USB at check), SHA256
17b1299ee4387b52eeba7a1a25c15a85495a5b9e5a9f2d76896a6f11ac42f48f.
shim/a03/out/a03-xnu-0014-emmc-status.img, opt-in A03_EMMC_SNAPSHOT=2.
One guarded CMD13 SEND_STATUS, one-second/iteration bound; snapshots plus
INT/RESPONSE/PRESENT; no card-state change/sector reads/DMA/storage writes.
Mode2 DOES write command/interrupt registers; mode1 remains snapshot-only.
Reuses exact0012 kernel/HFS payload, pauses before XNU, no CI. Next: fresh
Download and authorized BOOT-only flash0014; request result and glyph check.

Historical0013 flash handoff follows:

Latest trial: BOOT0013-emmc-snapshot flashed/rebooted via Heimdall exit0,
SHA256 c7465260e94e8ace4505595d254d8f5f589671a2c14bfec85575466e5d1836ae.
Physical result now recorded above. Opt-in A03_EMMC_SNAPSHOT=1 loader-only diagnostic
reads 14 selected registers at PA0x201d0000 before XNU; no MMIO stores,
FIFO reads, resets or card commands. Deliberately pauses with all values
on screen; request a photo/transcription, including any final read marker.
Does NOT boot XNU in this trial. Existing0012 kernel/root payload unchanged,
normal loader builds exclude diagnostic. BOOT0012 HFS/PID1 fallback retained.
Next: interpret VERSION/CLOCK/PRESENT/HOST2/COMMAND/RESPONSE0 before any
read-only card command; don't assume RCA/selected partition/card state.

Latest2026-11-14: HFS kernel CI43536143024 PASSED(source16b3177).
Kernel SHA256 c4c4e4a707ca4da82bd68318dfd187d7984d65fe4482999775e329af65ba942a.
Named HFS mount/read/register + BSD/pthread funcs verified SIMD-free.
Root32MiB HFSX fsck clean; catalog/sbin/launchd exact static init match.
BOOT0012-hfs FLASHED successfully, SHA256
4951efd8eae4493980ba0b9fdb7495bfb2a06f88e44206f603f5c7ff1814b60d.
RAM root0x104078000/32MiB; ADT0x106078000; entry0x10347c488.
Manifest shim/a03/out/a03-xnu-0012-hfs.json. Exact segment/payload verified.
User confirmed Download; USB detected. Heimdall boot100%, success, reboot,
exit0. Current BOOT0012; no independent readback. User now confirms md0/rmd0,
A03TestRoot HFS mount, /sbin/launchd, static test PID1 and heartbeat.
This establishes HFS RAM-root userspace execution. Previous0011 mockfs
PID1 is retained as fallback. No Apple launchd/SpringBoard/GUI yet.
Root edits reuse kernel; no XNU rebuild. Compiler cache seeded1050misses,
0hits, saved; warm reuse untested. Preserve all non-BOOT partitions.
This is test HFS root, not Apple launchd/iOS GUI. eMMC work still pending.
Linux root builder added: mkfs.hfsplus -s, temporary loop mount, root-owned
rsync copy, unmount/fsck, existing-kernel packaging. Local init matches
working SHA256 exactly. Formatter HasFolderCount defect reproduced and
repaired on a fresh temporary image; read-only fsck then passes. Complete
Linux copy/mount test awaits interactive sudo (noninteractive password
unavailable); docs/a03-filesystem.md has terminal commands. No new flash.
Next hardware checkpoint: bounded read-only eMMC register/state inspection
at 0x201d0000, then validated block reads; preserve all non-BOOT partitions.

Current branch: `a03-bringup`, from `64b1067`. Connected device is now a
Galaxy A03 SM-A035G (UNISOC T606/ums9230), not the S8 described below.
Read `A03_PROGRESS.md` and `docs/a03-bringup.md`. A locally built static
ARM64 EL0 diagnostic ran on Android and printed `A03_EL0_PROBE_OK`; timer
26 MHz. User then supplied matching revision-5 firmware and authorized
proceeding. BOOT-only Magisk flash succeeded via Odin4; Android returned,
Magisk setup/root works, and live BOOT/recovery/EFS/NV/DTBO/vbmeta backups
have matching device hashes. First pre-Linux probe 0001 booted and returned
six cmdline markers: EL2, A55 r2p0, MMFR0 0x101122 (4K/16K), 26 MHz. User
confirmed Android home/lock screen. Restored Magisk BOOT, readback hash
matched; clean reboot confirmed (`sys.boot_completed=1`, bootanim stopped).
No XNU yet. User's separate kernel clone b48e9ddfd73a is clean; its head.S
has the expected EL2 setup. Next: prove EL2-to-EL1 and GIC/timer before XNU.
See A03 progress for hashes, live RAM/reservations and exact test results.

A03 donor direction: native 16 KiB SWEET/GICv3 core plus reviewed Topaz
generic improvements; see `docs/a03-donor-selection.md` for pinned
sources. Do not keep HEROLTE's 4 KiB workaround or enable Qualcomm
peripheral drivers. Both inspected donors remain XNU 8796/iOS 16.

Previous S8 handoff and SWEET donor history remain below as historical reference.

## Active S8 handoff — 2026-11-13

Current work is on dreamlte-bringup, based on origin/herolte from
wardevsa/ios-a5xelte (ff2c55e). Read DREAMLTE_PROGRESS.md and
 docs/dreamlte-bringup.md for the S8, including verified CPU probes,
backups, new loader, build profile and outstanding CI/boot checks.
Original local main retains d857f24 and the earlier S8 handoff.
The SWEET/Redmi history below is donor reference, not S8 evidence.


## a5xelte fork handoff (2026-10-20)

The Samsung SM-A510F branch has a separate dated record in `A5XELTE_PROGRESS.md` and a donor replacement map in `docs/a5xelte-migration-map.md`. Its 4 KiB XNU boots four Exynos7580 cores with SGI1 verified, mounts an iOS 16 HFSX root from USERDATA, and executes launchd, SpringBoard and backboardd. A graphical SpringBoard frame remains unverified. The latest recovered log confirms backboardd has its stock system-container XML entitlement, yet it crashes after receiving a missing container path; `lsd` also aborts in system-group container URL initialization. The HFS `RENAME_SWAP` fallback was SWEET-only despite A5XELTE usermanagerd reporting ENOTSUP for atomic keybag writes. Patch `0117` enables the existing fallback for A5XELTE, and its four-core BOOT image was written to p10; the runtime log is pending. Recovery and EFS remain untouched. The SWEET notes below are donor history, not Samsung device results.

## Agent handoff / active work (2026-10-15, latest)

### >>> UPDATE 2026-10-18 (read first, then the 10-17 handoff below) <<<

**STATE at end of 2026-10-18 (evening):**
- On the phone: userdata = **image v15** (`/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v15.img/.simg`; = v14 + `/private/var/preferences/SystemConfiguration/preferences.plist` with one network service "USB Ethernet": Interface DeviceName ue0 Type Ethernet, IPv4 Manual 192.168.7.2/24 router 192.168.7.1, DNS 1.1.1.1 8.8.8.8, set "Automatic" as CurrentSet). Fallback image v14 (v12/v13 deleted).
- Kernels: **0078** = all 8 cores (`cpus=8`, cpu6/7 = A76, homogeneous SMP; mkadt now emits 8 CPU nodes; ADT `shim/out/sweet-0078hi.adt`); **0079** = display off/on via IOMFB selector 12 kern_RequestPowerChange(state) (fade over 6 vsyncs, then black; verified: power button gives "SWEET FB: display off/on"); **0080** = `SWEET NET: <proc> route add/delete/change ...` and `... add/delete address ...` trace (built, `shim/out/shim-boot-0080s.img`, NOT booted yet).
- **Internet over USB: not working yet.** Host side is ready (temporary iptables: FORWARD accept for 192.168.7.0/24 + MASQUERADE, comment "ios-sweet"; lost on host reboot). With v15 the phone sent no DNS and no outbound traffic (only mDNS/ARP) -> configd probably did not apply the service (or did, without default route/DNS). Next: boot 0080s on v15, watch `SWEET NET` lines (does configd add 192.168.7.2 / default route on ue0?). If configd ignores ue0 (not an IOKit IONetworkInterface; configd 1241.140.6 source in `research/configd-1241`, SCNetworkInterface createInterface needs IONetworkInterface -> controller (IOMACAddress, SelfNamed) -> bus), add IOKit stand-ins and/or rename the ifnet to en*.
- Live log listener (`nc -ukl 5140`) may still be running, writing `logs/live-0078s.txt`.

**LIVE LOG over USB (0077, boot 0077s): no more recovery round-trips.** Boot an image with `sweetusb=2`, run `tools/sweet-usbnet.sh logs/live-NAME.txt` on the PC: it waits for the phone's CDC-ECM interface, sets 192.168.7.1/24 (sudo) and prints/saves the kernel console the phone streams every 100 ms as UDP to 192.168.7.1:5140 (starts with the last 64 KiB). `ping 192.168.7.2` checks the link. Current image: `shim/out/shim-boot-0077s.img` (kernel 0077, ADT sweet-0069hi, cpus=6, sweetfb_noconsole=1, sweetfb_hz=30, sweetusb=2). The recovery pull (`tools/sweet-log-pull.sh`) is still the way after a panic/hang before USB comes up.

**🎉 USB networking works (boot 0076s, 18:24 local): `ping 192.168.7.2` from the PC answers in ~1 ms, 0 % loss (200-packet burst, 1500-byte frames, 512/1024-byte frames).** 0075: CDC-ECM function (bulk 0x81/0x01, interrupt 0x82 NETWORK_CONNECTION; host MAC 02:00:5e:77:ee:01) + kernel ethernet ifnet `ue0` (legacy output, header strip like if_fake) with 192.168.7.2/24 set from the kernel (proto_plumb + SIOCAIFADDR on an in-kernel socket). 0076: received frames into one cluster mbuf (mbuf_allocpacket gave a first mbuf of length 0 -> panic "Failed mbuf validity check: len -14"). Host side (Linux cdc_ether, interface `enp0s20f0u3u1`): `nmcli dev set IF managed no; sudo ip addr add 192.168.7.1/24 dev IF; sudo ip link set IF up`. Boot image `shim/out/shim-boot-0076s.img` (`sweetusb=2`). iOS itself does not see ue0 yet (configd needs an IONetworkInterface in IOKit).

**USB device mode works (boot 0074s, 17:45 local): the host enumerates the phone at high speed as `1209:0001 ios-sweet "Sweet iOS (USB bring-up)"`.** 0072 read-only probe: ABL leaves the USB30_PRIM GDSC and all 7 USB clocks on, DWC3 v3.20a (GSNPSID 0x5533320a) in device mode (GCTL 0x00112000), halted (DCTL RUN_STOP 0, DSTS 0x00d3de04), event buffer still at ABL's 0xfdfc8000, QUSB2 PHY alive. 0073 (`sweetusb=2`): DCTL soft reset, own event buffer (polled, interrupt masked), ep0 DEPSTARTCFG/SETEPCONFIG/SETTRANSFRESOURCE, setup TRB, RUN_STOP; control-transfer state machine as Linux ep0.c; descriptors: vendor class, no data endpoints. It ran but no event came: **0074** forces the VBUS session in the Qualcomm wrapper (QSCRATCH 0xa6f8800: HS_PHY_CTRL |= UTMI_OTG_VBUS_VALID(20)|SW_SESSVLD_SEL(28), SS_PHY_CTRL |= LANE0_PWR_PRESENT(24), as Linux dwc3_qcom_vbus_override_enable) -> connect + enumeration. Image `shim/out/shim-boot-0074s.img`. Black Phone app: main thread waits in -[VMVoicemailManager fetchAccounts] (sync XPC; voicemail needs the modem).

**Navigation works (boot 0071s on v14, log `logs/boot-0071s.txt`):** swipe up from the bottom edge returns to the home screen; app switcher works. Two fixes: **0070** pid_hibernate (syscall 435 was nosys on the macOS config -> SIGSYS killed SpringBoard in -[SBToAppsWorkspaceTransaction _didComplete] when an app left the foreground; the only CONFIG_EMBEDDED-only entry in syscalls.master); **0071** touches starting within 48 px of an edge carry kIOHIDDigitizerEventFromEdgeTip (UIKit `_UIEventHIDTouchEdgeTypeForHIDEvent` reads the digitizer EventMask 0xb0007 bits 0x800/0x1000/0x2000/0x40000). Diagnosed, not fixed: Settings (Preferences) SIGTRAP in PodcastsUI func_1cdc47c58: force-unwrap of `URL.volumeTotalCapacity` (nil on our HFS+ root). Phone/Photos/Messages show black (MobilePhone launches, no crash) - next: stack samples via boot-arg `sweetsample=MobilePhone,MobileSlideShow,MobileSMS,SpringBoard` (image `shim/out/shim-boot-0071s.img`).

**🎉🎉 MILESTONE 2026-10-18 ~15:30 local: iOS 16.7 SPRINGBOARD HOME SCREEN ON THE PHONE** (boot `shim/out/shim-boot-0069s.img` = kernel 0069 + ADT `shim/out/sweet-0069hi.adt`, image **v14**; log `logs/boot-0069s-v14-HOMESCREEN.txt`). Home screen with a few apps, Settings opens, Control Center / lock screen / notification center work, touch + buttons work, 6 A55 cores (`cpus=6`), `sweetfb_noconsole=1 sweetfb_hz=30`. Known issue: cannot leave Settings (home gesture / AssistiveTouch home do nothing) - to investigate.
What it took today (in order): 0058 HID services (Apple IOHIDFamily-1915 user client), 0059 iPhone X identity (hw.product etc.), 0060 SPMI keys + GENI touch, 0061 1125x2436 presented display, 0062 RPMh L11C touch power + IOPMPowerSource battery, 0063 GENI FIFO packing (Goodix GT9896), 0064 PRIV_WORK_INTERVAL grant (SpringBoard "Failed to create work interval"), 0065 SMP via PSCI (6 A55), 0066 crash map regions, 0067 console mute without cons_ops write, 0068 IOSurface lookup of an already-mapped surface returns base -1 (backboardd snapshot crash), 0069 UFS log flush 10 s. Image v13: CommCenter removed from launchd.plist, BKNoWatchdogs. **Image v14** = v13 + Setup skipped (`/var/mobile/Library/Preferences/com.apple.purplebuddy.plist` SetupDone/SetupFinishedAllSteps true, SetupVersion 11, daemonizeNeedsToRun false; purplebuddy.notbackedup mini-buddy flags false; managedconfiguration.notbackedup LockdownActivationIndicatesCloudConfigurationAvailable false; springboard MCForceShowCloudConfigurationUI false) + mobileactivationd data ark seeded (`/private/var/containers/Data/System/D90C94C4-F94E-4FCF-8A28-A93BE3846D8E/Library/internal/data_ark.plist`, -ActivationState Activated etc.) + MediaToolbox D22/D221/Default SubServerConfiguration StartRecorderServer=false (mediaserverd crash loop: portrait-filter prewarm called NULL GL). **Activation:** ADT /chosen certificate-production-status 0, effective-production-status-ap 0, certificate-security-mode 1, effective-security-mode-sep 1 -> mobileactivationd's native Hactivation branch (Codex `codex/activation/report.md`; alternative 4-byte daemon patch documented there). Fallback image v13; v12 deleted.

**🎉 TOUCH WORKS (boot 0063u on image v13, 2026-10-18 ~13:15 local):** tapping (i) on Setup's Hello opens the device-info sheet; swipe-up is recognised (spinner, then back to Hello - under investigation). Chain: RPMh L11C vote (0062, `bsd/dev/sweet_rpmh.c`) -> GT9896 @0x5d on GENI SE7 (0063 fixed FIFO packing: register address went out byte-swapped) -> sweet_hid_touch -> SweetHIDTouch -> backboardd. Battery icon OK (0062 SweetBattery IOPMPowerSource, static 100 %). **Image v13** (= v12 + CommCenter jobs removed from launchd.plist + `BKNoWatchdogs`=true and `FBLaunchWatchdogExceptions{com.apple.purplebuddy:100}` in /var/mobile/Library/Preferences/com.apple.springboard.plist): Setup no longer killed by the scene-create watchdog (it blocked in CoreTelephony getSubscriptionInfo -> CommCenter, Codex `codex/setup/report.md`; that report also lists how to skip Setup: SetupDone/SetupFinishedAllSteps/SetupVersion=11 in com.apple.purplebuddy.plist + activation check). v9 deleted, fallback = v12. Input latency ~1 min with 1 CPU -> Codex task 11 = SMP via PSCI (`codex/smp/`).

**INPUT WORKS (boot 0060u on a freshly flashed v12, log `logs/boot-0060u.txt`):** power, volume up, volume down reach iOS (PMIC -> sweet_keys.c -> SweetHIDButtons -> backboardd). Power locks/unlocks (screen "off" shows the kernel console because the panel never really turns off). **Device identity fixed: iPhone X** (home indicator, Face-ID-style Setup). Earlier test (0059u, `sweethidtest=15` fake Home presses) advanced Setup from Hello to the language list.
- **0058** HID: `iokit/Kernel/arm/hid/`: IOHIDEventServiceUserClient + IOHIDEventServiceQueue + IOHIDEvent compiled UNCHANGED from Apple IOHIDFamily-1915.140.3 (= exact version of the iOS 16.7 IOHIDLib, clone in `research/iohid-1915`) over our minimal IOHIDEventService (SweetHID.cpp: SweetHIDButtons consumer page 0x0C power 0x30 / vol 0xE9/0xEA / menu 0x40; SweetHIDTouch digitizer collections). C hooks `sweet_hid_key(key, down)` (0 power, 1 vol+, 2 vol-, 3 home) and `sweet_hid_touch(finger, down, x, y)`. HID logs go to IOLog. Boot-arg `sweethidtest=N` = fake Home press every N s.
- **0059** identity: hw.machine/hw.model/hw.target/hw.product from the ADT (macOS-config kernel used to answer "iPad8,6"/"Redmi Note 10 Pro"). mkadt: root compatible `D22AP|iPhone10,3|xiaomi,sweet|...`, model iPhone10,3, target-type D22, `/product` copied from the real D22AP device tree (`research/ipsw-x/d22ap.adt`, extracted from the IPSW, NOT in git), `/buttons home-button-type 2`. Codex report `codex/mg/report.md`: MG ProductType = sysctl **hw.product** (unrecognized -> iPod), HWModelStr = hw.target, HomeButtonType = `/buttons/home-button-type`; disk cache `/private/var/containers/Shared/SystemGroup/systemgroup.com.apple.mobilegestaltcache/Library/Caches/com.apple.MobileGestalt.plist` (keyed by build + UUID only -> stale iPod answers survived; reflashed clean v12 to clear it).
- **0060** drivers by Codex (`codex/input/hw-report.md`): `bsd/dev/sweet_keys.c` (SPMI arbiter v5 observer reads, PON 0x810 bits KPDPWR/RESIN SID0, PM6150L GPIO2 SID4 0xc110; works), `bsd/dev/sweet_touch.c` (GENI SE7 I2C @0xa84000, starts 45 s after boot). Touch result: SE7 fw ok (proto 3) but **0x5d and 0x38 both time out -> touch IC unpowered** (L11C LDO needs an RPMh vote). Codex task 8 = RPMh client (`codex/rpmh/`), task 7 = battery (`codex/battery/`).
- **0061** (CI 39117078444): red status bar "rdar:45025538" = UIKit "No status bar visual provider for screen" (360x800 pt is no real iPhone). AppleCLCD now presents **1125x2436** (iPhone X) and shows the centered 1080x2400; touch mapped the same; ADT canvas 1125x2436. `sweetfb_native=1` reverts.
- Images: `shim/out/shim-boot-0060b.img` (0060 + /buttons ADT `sweet-0060hi.adt`). Next: 0061 image with ADT from current mkadt.

### >>> HANDOFF 2026-10-17 late (read this first) <<<

**STATE: iOS 16.7 Setup.app "Hello" screen is ON THE PHONE** (boot `shim/out/shim-boot-0057u.img` on image v12). Photo `/run/media/dipa/android/ios-sweet-work/MILESTONE-setup-hello-2026-10-17.jpg`. SpringBoard + backboardd + Setup run; nothing crashes in the GUI path. Remaining crash/relaunch loops: installcoordinationd (should be fixed by 0057, unverified), mediaserverd (VirtualAudio removed in v12, unverified), mobileactivationd (~100/boot, not analysed), bluetoothd + fairplayd.H2 relaunch constantly (no hardware).

**What is on the phone now:** userdata = image **v12** (`/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v12.img` + `.simg` + `.sha256`; v9 kept as fallback, v8/v10/v11 deleted or superseded). Kernel **0057** (`xnu/out-0057`, CI `39067532732`). ADT **`shim/out/sweet-0057hi.adt`** (QEMU twin `research/q0057-hi.adt`). Boot image **`shim/out/shim-boot-0057u.img`**. Boot args: `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress rd=ufsroot0 unentitled_ios_sim_launch=1 ignition_level=1 wdt_test=no_user_checkin ufsrw=1 rootrw=1 launchd_unsecure_cache=1 wdt=-1`.

**Build a phone image** (kernel K, ADT A): `python3 tools/mkpayload.py $K $A shim/out/payload-X.bin --cmdline "$B" && (cd shim && ./build.sh ../shim/out/payload-X.bin && cp out/shim-boot.img out/shim-boot-X.img)` then check `python3 tools/unpack_bootv2.py shim/out/shim-boot-X.img shim/out/check-X && cmp shim/out/check-X/ramdisk shim/out/payload-X.bin`. QEMU smoke test: `python3 tools/mkpayload.py $K research/q0057-hi.adt $S/csq/payloadX.bin --ramdisk $S/csq/root-fork.img --cmdline "debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress rd=md0"` + `PATH=~/swift/usr/bin:$PATH python3 tools/qemu-sweet.py ... --secs 40 --kernel $K --fail-on-panic` (S = scratchpad; root-fork.img lives in the session scratchpad csq/ dir and may be gone in a new session).

**Kernel workflow:** edit `research/bt28/xnu/...` (keep the pre-edit copy in `research/preNNNN/`), syntax check `python3 tools/xnu-cc.py research/run28.log research/bt28 <file>`, make `xnu/patches/NNNN-*.patch` with `diff -u pre bt28 | sed` path rewrite, add new/changed files to `research/check-patch-order.py` list, run it (must say applied + MATCH), commit + push -> GitHub Actions `xnu` builds (~8 min) -> `gh run download <id> -R dipa-studio/ios-sweet -n xnu-kernel -D xnu/out-NNNN`. **Repo is PUBLIC since 2026-10-17** (private macOS runner minutes ran out: "recent account payments have failed"); public = free runners. Commit trailer: only `Co-Authored-By: dipa-studio <183933817+dipa-studio@users.noreply.github.com>`.

**Phone workflow (user does buttons, Claude runs commands):**
- Boot test kernel: phone in fastboot -> `fastboot boot shim/out/shim-boot-X.img`. NEVER `fastboot getvar`.
- **Read logs WITHOUT filming:** after a test the user holds Power+VolDown -> fastboot -> `fastboot boot recovery/recovery.img` (OrangeFox, temp) -> wait for `adb shell true` -> `tools/sweet-log-pull.sh /run/media/dipa/android/ios-sweet-work/logs/<name>.txt` (reads the 4 MiB console ring the kernel keeps in the last 1025 blocks of userdata; patch 0047). Then `adb reboot bootloader` brings the phone back to fastboot without the user.
- **Flash a root image:** `fastboot flash -S 512M userdata <img>.simg` (7 min, 25 chunks). After a big flash the Xiaomi ABL fastboot hangs: next `fastboot boot` stalls at "Sending" -> the USER must re-enter fastboot by hand (Power+VolDown). Do not retry commands against the hung ABL. A flash right after `adb reboot bootloader` once failed on chunk 1 (USB protocol error): just retry. User must NOT unplug during flash (once interrupted at 25/25 -> reflash).
- **Edit the phone root without reflashing (same-length only):** find the file's raw offset in the local image (it is one extent; search the image for its first 4 KiB), compare with `adb exec-out dd if=/dev/block/sda34 ...`, then `adb push` changed 4 KiB blocks and `dd of=/dev/block/sda34 seek=... conv=notrunc,fsync`, read back. Recovery kernel has no hfsplus.
- **Pull the whole phone root** (12 min): `adb exec-out "dd if=/dev/block/sda34 bs=1048576 count=16384" > img`; mount ro with udisksctl or `sudo mount -t hfsplus -o loop,ro`. To write into a pulled image: `sudo fsck.hfsplus -fy` first (volume is never cleanly unmounted -> Linux mounts ro even with -o force), then `sudo mount -t hfsplus -o loop,force`.
- Making images: copy latest img with `cp --sparse=always`, mount rw with force, change, `sync; umount`, `sha256sum`, `img2simg`. Keep only the latest image + one fallback on the SSD (/home is ~98% full; big work files live in `/run/media/dipa/android/ios-sweet-work/`, old kernels/images archived in `.../ios-sweet-work/archive/`).

**Diagnostics built into the kernel (all SWEET-only):** persistent console log (0047, boot-arg sweetlog=0 off; flush every ~1 s); `|name| text` copies of /dev/null writes for processes in `sweetnull` (default backboardd,SpringBoard; 0048); `IOK name:` IOKit lookup/open trace for `sweetiolog` (default backboardd,SpringBoard; 0049/0054, 400 lines max); `SWEET Sandbox: proc op N` (0050); `STR ...` heap text dump on SIGABRT/SIGTRAP for `sweetscan` (default backboardd,SpringBoard; 0051/0053) - this is how NSException/BSAssert reasons were found; `SMP name tN pc .. bt ..` user stack sampler for `sweetsample` (default SpringBoard,backboardd; first at 90 s then every 120 s, 40 samples, 16 frames; 0054/0055); `SWEET FB: N swaps` every 1000 swaps; `CRASH name ...` crash reports (0043/0044). Symbolicate cache addresses with `ipsw dyld a2s research/dsc/dyld_shared_cache_arm64 <addr - slide>`; main-binary addresses: addr - mh + 0x100000000.

**Patches added today (0046-0057, all CI-built):** 0046 IOSurface (IOCoreSurfaceRoot) + IOMobileFramebuffer (AppleCLCD on /arm-io/disp0) + arm-io nubs; 0047 persistent log; 0048 /dev/null tee; 0049 IOKit trace; 0050 permissive "Sandbox" MAC policy; 0051/0053 heap text on crash; 0052 RENAME_SWAP via exchangedata on HFS; 0054/0055 sampler, swap counter, AKS selectors 35 (extended device state = 17) and 101; 0056 panel copy from the vsync timer at 10 Hz (sweetfb_hz) instead of every swap; 0057 no config_ext_resolver (ACL group entries resolve without memberd). ADT (tools/mkadt.py): /arm-io/disp0, /chosen/display-scale 3, /chosen/unique-chip-id (synthetic 0x5357454554000001) + chip-id 0x8015 -> IOPlatformUUID A9683613-3704-53F2-95D0-98A8FB574E78. Image v9-v12: /private/var/containers/{Bundle,Data/System,Shared/SystemGroup,Temp}; launchd.plist StandardOut/ErrorPath renamed to ...PatX (pointing jobs at /dev/console stops them launching: EACCES); v12: LastSystemVersion=20H392 in plain /var/mobile/Library/Preferences/com.apple.migration.plist (stops the 1-hour data migration that ran every boot), VirtualAudio.plugin moved to /Library/Audio/Plug-Ins/HAL.disabled/.

**Codex helper** (`codex exec --skip-git-repo-check -m gpt-6.1-sol -c model_reasoning_effort=high -s workspace-write -C /run/media/dipa/android/ios-sweet-work/codex -o OUT "$(cat task.md)" < /dev/null`, run detached with setsid nohup; config already defaults to gpt-6.1-sol high). Reports in `/run/media/dipa/android/ios-sweet-work/codex/`: mediaserverd-report.md, installcoordinationd-report.md (-> 0057), ufs-performance.md (ranked UFS speed plan), **ufs/0058-sweet-ufs-faster.patch** (READY, not yet applied: ufslogsecs default 10 s log flush batching, optional ufscache=1 directional cache ops, optional ufswait=1 spin-then-sleep; syntax-checked, host-stub verified; see ufs/README.md). Apply it as patch 0058 after review.

**Claude safety-classifier note:** several messages about QuartzCore renderer selection / writing an HFS reader tool were cut off by an automatic classifier (false positives, user agrees). Keep those topics short or let them be; they are not blockers now (rendering already works).

**NEXT STEPS (in order):**
1. **Input** (Setup stuck on Hello): touch + power + volume as IOHIDEventService/IOHIDDevice services backboardd matches (log shows backboardd matching IOHIDDevice with DeviceUsagePairs and IOService with HIDServiceSupport=true). Phone hardware: Goodix/Focaltech touch over I2C/SPI (check live DT `dtb/`), buttons via PMIC (pon) and GPIO keys. Start with a fake HID service (e.g. power button via a timer or boot-arg) to learn the ABI, then real drivers.
2. **Device identity**: MobileGestalt reports iPod + Home button. Add /product node / product-type (iPhone10,3, D22AP), device class iPhone, home-button-less (Face ID) properties in mkadt; find exact MG keys (MGIOMFBSupport.c, `IODeviceTree:/product` lookups seen in backboardd trace).
3. **Battery**: AppleSmartBattery/IOPMPowerSource style service (status bar shows empty red battery).
4. Apply Codex 0058 (UFS speed), consider cpus>1, check whether installcoordinationd/mediaserverd loops are gone, analyse mobileactivationd.
5. Hide kernel console over the GUI when not debugging: boot-arg sweetfb_noconsole=1 (but then panics are not on screen).

- **🎉 MILESTONE: iOS GUI ON THE PHONE - Setup.app "Hello" screen (2026-10-17 ~21:30 UTC, boot 0057u on image v12).** Photo: `/run/media/dipa/android/ios-sweet-work/MILESTONE-setup-hello-2026-10-17.jpg` (animated "dobar d(an)" hello lettering, status bar "iPod" + battery icon, bottom "Pritisnite Home za otvaranje" = "Press Home to open" (locale hr), (i) button). Rendered by iOS 16.7 SpringBoard/Setup through CoreAnimation -> backboardd -> kernel IOSurface (IOCoreSurfaceRoot) -> kernel AppleCLCD swaps -> ABL panel memory. What made it: data migration finally skipped (v12: `LastSystemVersion` 20H392 in the plain `/var/mobile/Library/Preferences/com.apple.migration.plist`; ADT `/chosen/unique-chip-id` + `chip-id` for IOPlatformUUID), 0057 (no ext resolver -> ACL containers work), plus everything before (0046 display/IOSurface, 0050 Sandbox policy, display-scale 3, containers dirs, RENAME_SWAP, AKS 35/101, 10 Hz present).
  **Missing (next work, in rough order):**
  - **Input: no touch, no power button, no volume buttons** (no HID drivers; backboardd looks for IOHIDDevice / HIDServiceSupport services). Setup is stuck on "Hello".
  - **Device identity: it thinks it is an iPod with a Home button** (status bar "iPod", "Press Home to open"): MobileGestalt has no product/model identity (no /product node, product-type, etc.) - give it iPhone10,3 / home-button-less (Face ID class) identity.
  - **No battery detection** (no battery/charger/PMIC service; status bar battery shows empty/red).
  - Locale came up Croatian (hr) - harmless.
  - Performance: cpus=1, polled UFS (Codex UFS patch in progress: `codex/ufs/`), backboardd presents at 60 Hz.
- **README refreshed (2026-10-17):** read the full notes and updated the public overview through patch 0045, v7 hardware observations and prepared v8 diagnostics. Documents real Apple userspace, the missing display/IOSurface GUI work, limited security services, highmem, persistent userdata root, current tooling and build examples. Documentation only; no kernel build, tests, flashing or phone boot performed.

- **v11 still migrated (boot 0056u, 20:32 UTC, `logs/boot-0056u-v11.txt`).** On iOS kCFPreferencesCurrentHost lands in the plain plist: all DMEnvironment setters (setLastBuildVersionPref, setUserDataDispositionPref, ...) use CurrentHost and the phone's `/var/mobile/Library/Preferences/com.apple.migration.plist` holds DMUserDataDisposition; datamigrator's XPC service runs with `_RoleAccount: mobile`. **Image v12** = v11 + `LastSystemVersion` = 20H392 added to that plain `com.apple.migration.plist` (keeps DMUserDataDisposition, 501:501 0600) + `/Library/Audio/Plug-Ins/HAL/VirtualAudio.plugin` moved to `/Library/Audio/Plug-Ins/HAL.disabled/` (Codex: stops the mediaserverd SIGSEGV loop; untested). **installcoordinationd loop explained (Codex `codex/installcoordinationd-report.md`):** os_crash "Failed to create data directory" EACCES for `/private/var/containers/Shared/SystemGroup/systemgroup.com.apple.installcoordinationd/Library/InstallCoordination`: `Library`/`Library/Caches` in the container are ACL-only (uid/gid 0xfffffffe, mode 0000, ACE for group GUID ...012B = gid 299 systemusers); with `config_ext_resolver` the kernel asks an identity resolver (memberd/opendirectoryd) that iOS does not run -> EWOULDBLOCK -> ACE skipped -> EACCES. **Patch 0057**: drop config_ext_resolver from FILESYS_BASE (compatibility UID/GID<->GUID mapping is used instead), likely fixes other ACL-protected containers too. Codex task 3: UFS driver performance design (`codex/ufs-performance.md`).
- **mediaserverd SIGSEGV loop explained (Codex report `/run/media/dipa/android/ios-sweet-work/codex/mediaserverd-report.md`):** the fault (FAR 0x390) is in the HAL plug-in `/Library/Audio/Plug-Ins/HAL/VirtualAudio.plugin/VirtualAudio` (ApplyBeamFormerPreference <- VirtualAudio_PlugIn::SetPropertyData <- HALS_AHPPlugIn::ObjectSetPropertyData <- AudioObjectSetPropertyData <- MediaExperience vaemVADSerializationListener): the default virtual audio device ('vdef', VirtualAudioDevice_Default) does not exist (no audio hardware/driver, no /product/audio). Proposed workaround for GUI bring-up: move VirtualAudio.plugin out of /Library/Audio/Plug-Ins/HAL/ in the next root image (untested). v11 reflashed OK after an interrupted flash (USB unplugged at chunk 25/25). Codex task 2: installcoordinationd crash loop.
- **ROOT CAUSE of the endless migration: no IOPlatformUUID (2026-10-17).** datamigrator's `-[DMMigrator isMigrationNeededWithBuildVersion:lastBuildVersion:clientPID:]` gets lastBuildVersion from `-[DMEnvironment lastBuildVersionPref]` = `CFPreferencesCopyValue("LastSystemVersion", "com.apple.migration", kCFPreferencesCurrentUser, kCFPreferencesCurrentHost)` -> a ByHost file. The phone had `/var/mobile/Library/Preferences/com.apple.migration.plist` (only DMUserDataDisposition) and NO `Preferences/ByHost` directory at all. On arm XNU publishes IOPlatformUUID (gethostuuid) only from `/chosen/unique-chip-id` (8 bytes) + `/chosen/chip-id` (4 bytes) (IOPlatformExpertDevice::generatePlatformUUID, called from IOPlatformExpert::start); the SWEET ADT had neither, so every CurrentHost preference write failed. Fix: mkadt adds `unique-chip-id` = 0x5357454554000001 (synthetic) and `chip-id` = 0x8015 -> UUID `A9683613-3704-53F2-95D0-98A8FB574E78` (same SHA1 namespace computation as the kernel). ADT `shim/out/sweet-0057hi.adt`, boot image `shim/out/shim-boot-0056u.img` (0056 kernel + 0057hi ADT, QEMU OK). **Image v11** = v10 + `Preferences/ByHost/com.apple.migration.<UUID upper and lower>.plist` {LastSystemVersion: 20H392} (501:501, dir 0755 files 0600). Flashing v11 2026-10-17 ~20:10 UTC. Codex (gpt-6.1-sol high) analysing the mediaserverd SIGSEGV loop in `/run/media/dipa/android/ios-sweet-work/codex/` (report `mediaserverd-report.md`).
- **v10 did NOT stop the migration (boot 0056n on v10, 19:18 UTC, `logs/boot-0056n-v10.txt`):** datamigrator + migrationpluginwrapper ran again, backboardd drew the progress UI (13000+ swaps in ~5 min). So `com.apple.DataMigration.plist`/LastSystemVersion is not the deciding input. What is known about the decision (datamigrator XPC service `DataMigration.framework/XPCServices/com.apple.datamigrator.xpc/com.apple.datamigrator`, strings): `Migration sentinel present. Migration necessary.` (sentinel `/private/var/datamigrator/migrate`, created and removed by datamigrator itself; absent in v10), `System build version changed from %@ to %@. Migration necessary.` / `...unchanged... not necessary`, `Disposition dictionary with build version %@ is out of date relative to current build version %@`, `SyntheticDidUpgrade`, DMUserDataDispositionManager; previous build source not found yet (not in the binary's plain strings; likely in DataMigration.framework's DMUserDataDispositionManager / preferences domain `com.apple.migration`). backboardd calls `DMPerformMigrationIfNeeded` and holds SpringBoard in `checkInAndWaitForDataMigration` until it returns. NEXT: find where the previous build version / disposition dictionary is stored (disassemble DataMigration.framework DMUserDataDispositionManager + datamigrator's isMigrationNeeded path), write it into the image; or get datamigrator's os_log out (OS_ACTIVITY_DT_MODE needs a launchd env change).
- **Data migration never records completion -> skip it (image v10, 2026-10-17).** Boot 0056n (18:16 UTC, `logs/boot-0056n.txt`, 30 min): 10 Hz panel copies, backboardd still presents at ~60 Hz (107k swaps), SpringBoard still in `BKSSystemShellService _checkIn` at sample 14. Every migration run takes 1+ hour on cpus=1 and repeats each boot. DataMigration decides from `/var/mobile/Library/Preferences/com.apple.DataMigration.plist` key `LastSystemVersion` (vs ProductBuildVersion 20H392); the pulled phone root (21:01 local) had NO such file. **v10** = that pulled phone state + fsck.hfsplus -fy (volume was marked not cleanly unmounted -> Linux mounts it read-only even with -o force; fsck found only hard-link counts + minor volume header, repaired) + `com.apple.DataMigration.plist` {LastSystemVersion: 20H392} (501:501 0600). `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v10.img` (+ .sha256, .simg); v8 files deleted, v9 kept as fallback.
- **Repo made PUBLIC (2026-10-17, user request) so GitHub-hosted macOS runners are free:** the 0056 CI run was refused ("recent account payments have failed or your spending limit needs to be increased"). Checked before: no device dumps, serials, IMEI or Apple binaries in the history (.gitignore keeps backup/, dtb/, recovery/, research/ out); commit author emails are public now. 0056 rerun `39056660104` passed -> `xnu/out-0056`, QEMU OK, image `shim/out/shim-boot-0056n.img` booted 18:16 UTC.
- **Boot 0055n (17:16 UTC, ~65 min, `logs/boot-0055n.txt`): migration bar reached 99% in ~30 min (was ~60), then crawled.** Root cause of the slowness: backboardd presents the progress UI at ~58 Hz (**167,000 swaps in ~48 min**) and AppleCLCD copied the full 10 MB frame into the panel on every swap -> ~600 MB/s memcpy on the single CPU (cpus=1), starving everything (polled UFS I/O too). Sampler (16 frames): **SpringBoard waits in `-[BKSSystemShellService _checkIn]`** (synchronous BSXPC call to backboardd, from FBSystemShellInitialize <- SBSystemAppMain) - backboardd holds the system shell check-in until the data migration ends, so the migration is the gate to SpringBoard UI. **Patch 0056**: swap only records the latest swap record; the vsync timer copies it to the panel every 60/sweetfb_hz ticks (default 10 Hz); `SWEET FB: N swaps` every 1000.
- **Boot 0054n (16:53 UTC, ~12 min, `logs/boot-0054n.txt`, patch 0054 sampler):** the data migration runs AGAIN on every boot (it completed once in the 0053s run) - completion is not being recorded. backboardd keeps swapping the progress UI (3700+ swaps in ~10 min, `SWEET FB: N swaps`). Sample during migration: SpringBoard main thread blocked in a synchronous XPC call (`mach_msg2_trap <- dispatch_mach_send_and_wait_for_reply <- xpc_connection_send_message_with_reply_sync <- -[BSXPCServiceConnectionMessage _sendSynchronously:] <- BSXPCServiceConnectionProxy ...`). Unsupported AKS selectors seen: 101 `aks_assert_consume`, 93 `aks_get_internal_info`, 34 `_aks_stash_load` (datamigrator), **35 `aks_get_extended_device_state`** (SpringBoard, chronod, remindd, searchd, symptomsd...). **Patch 0055**: AKS 35 answered like 17 (same DER device state), 101 succeeds; sampler backtraces 16 frames, 40 samples (~80 min).
- **MILESTONE: FIRST iOS PIXELS ON THE PANEL (boot 0053s long run, 15:33 UTC, ~60 min; photos IMG_20261017_183029/183222/183419; log `/run/media/dipa/android/ios-sweet-work/logs/boot-0053s-long.txt`, 407 KB, 1428 flushes).** The iOS data-migration boot screen (Apple logo + progress bar) was shown and the bar advanced to full in ~60 minutes. It is drawn by **backboardd through our kernel display path**: `SWEET SURF: backboardd create id 2/3 1080x2400 fmt 0x42475241 (BGRA) bpe 4 bpr 4352 size 10452992 keys 11`, IOSurface sels 9, 27, 5, 34 and traps 2/3 (lock/unlock), IOMFB SwapBegin (4) / SwapEnd (5, 1132-byte struct) / GetLayerDefaultSurface (3) / 68 / 55, then `SWEET FB: swap N layer 0 surface 2|3 1080x2400 ... a 0,0 1080x2400 b 0,0 1080x2400` alternating (double buffering; only the first 16 swaps are logged). Triggered by `com.apple.datamigrator` (AKS sels 101/93/34 return unsupported) and `com.apple.migrationpluginwrapper`. Probably ProgressUI-style CoreGraphics drawing into IOSurfaces (no GPU used). After the migration: SpringBoard and backboardd stay up (exec once each, no crash), nothing new drawn; crash loops only for mediaserverd, installcoordinationd, mobileactivationd (~108 each in the hour); bluetoothd and fairplayd.H2 relaunch constantly (no hardware). Kernel console text overlays the image (sweetfb_noconsole=1 would hide it).
- **MILESTONE: SpringBoard and backboardd both stay up (boot 0053s on v9, 15:29 UTC, `logs/boot-0053s.txt`).** With /chosen/display-scale = 3: `exec SpringBoard` once, `exec backboardd` once, no CRASH for either; MobileGestaltHelper reads IOMFB size/dot pitch; backboardd opens AppleCLCD (sels 57,15,22,29,33,79,74 as before). No IOSurface creates and no swaps: backboardd keeps polling `IOProviderClass IOAcceleratorES` (-> 0 found) and AGXAccelerator/IOAcceleratorESLegacy - no GPU, so no CoreAnimation renderer yet. Log goes quiet after ~47 s (only 47 flushes): the system idles. NEXT WALL: CoreAnimation rendering without a GPU (CPU path) so the window server produces frames.
- **SpringBoard's invalid mode = scale 0 (boot 0053n, 15:19 UTC, `logs/boot-0053n.txt`, heap scan):** `FBSDisplayMode cannot be configured as requested : <FBSDisplayMode: ...; infxinf@0x (1080x2400/0) 60Hz sRGB SDR>` - pixel size and 60 Hz are fine, scale is 0. libMobileGestalt (MGIOMFBSupport.c, sub_19c560a54) reads `display-scale` (u32, default 0) and `display-rotation` from **IODeviceTree:/chosen**, pixel size via IOMobileFramebufferGetDisplaySize (MobileGestaltHelper sel 8/28 in the log). mkadt now adds `/chosen/display-scale` = 3 (1080x2400 @3x = 360x800 pt). ADT `shim/out/sweet-0054hi.adt` (QEMU `research/q0054-hi.adt`), image `shim/out/shim-boot-0053s.img` = 0053 kernel + 0054hi ADT. Possible catch: MobileGestalt may have cached scale 0 in `/private/var/containers/Shared/SystemGroup/systemgroup.com.apple.mobilegestaltcache/...`.
- **MILESTONE: backboardd survives and opens the display (boot 0052n on v9, 15:07 UTC, `logs/boot-0052n.txt`).** No `CRASH backboardd`. It walks `IODeviceTree:/arm-io` children, matches IOMobileFramebuffer, `open AppleCLCD type 0 -> 0x0`, calls IOMFB selectors 57, 15, 22, 29, 33, 79 (GetBlock, out 1580/40), 74 (SupportedFrameInfo), 12, 6, 27, 17, 84, 50; opens IOCoreSurfaceRoot (sel 13); looks for AGXAccelerator / IOAcceleratorES / IOAcceleratorESLegacy (none, repeatedly), `IODeviceTree:/product` (none, repeatedly), `/buttons`, aop-smart-cover, IOPMrootDomain. No swaps yet. **SpringBoard now gets past display discovery** and dies (sig 5) in `-[FBSDisplayMode _initWithWidth:height:preferredScale:scaleOverride:refreshRate:gamut:hdr:rotation:virtual:validityCheck:]+580` <- `_initWithCADisplayMode:scale:rotation:` <- `FBSDisplayConfiguration _initWithImmutableDisplay:` <- `FBSDisplaySource initWithDisplay:` <- `FBSDisplayMonitor` (slide 0x14504000): "FBSDisplayMode cannot be configured as requested". Checks: width/height >= 2, preferredScale > 0, scaleOverride >= 0, refreshRate non-zero, valid gamut/HDR/rotation. Suspects: refresh rate 0 (IOMFB timing blocks answered with zeros) and/or scale 0 (MobileGestalt main-screen-scale; no /product node in the ADT). **Patch 0053**: heap text scan also on SIGTRAP and for SpringBoard (default sweetscan list backboardd,SpringBoard) to read the exact mode description.
- **Image v9 (2026-10-17) = v8 + `/private/var/containers/{Bundle,Data/System,Shared/SystemGroup,Temp}` (root:wheel 0755; on iOS these live on the data volume, absent from the rootfs) + launchd.plist with StandardOutPath/StandardErrorPath renamed to ...PatX (the in-place phone fix; daemons' stdout reaches the log via the 0048 /dev/null tee).** `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v9.img` SHA256 aa9f9139...6e67, `.simg` 12,145,303,864 bytes; written through `sudo mount -t hfsplus -o loop,force`. **Patch 0052** (`xnu/patches/0052-sweet-hfs-rename-swap.patch`, CI `39042761826` -> `xnu/out-0052`, QEMU OK, image `shim/out/shim-boot-0052n.img`): vn_rename falls back to VNOP_EXCHANGE when VNOP_RENAMEX(RENAME_SWAP) returns ENOTSUP for two regular files on one volume (HFS exchange swaps data and cnode descriptors = swap semantics). Flashing v9 started 2026-10-17 ~15:00 UTC.
- **backboardd EXCEPTION FOUND (boot 0051n, 14:41 UTC, `logs/boot-0051n.txt`, patch 0051 heap scan):** `*** Terminating app due to uncaught exception 'NSInvalidArgumentException', reason: '*** -[NSURL initFileURLWithPath:]: nil string parameter'`. First-throw stack (slide 0x337f0000): `+[NSURL fileURLWithPath:]` <- `-[BSSystemContainerForCurrentProcessPathProvider libraryPath]` <- `cachesPath` <- backboardd main+0x1d858 (StartWindowServer, shader cache path). BaseBoard: libraryPath = `BSSystemSharedResourcesDirectoryForIdentifier` = `BSSystemSharedDirectoryForIdentifier(id)` + "/Library"; that calls `container_system_path_for_identifier` (libsystem_containermanager -> `_container_legacy_lookup` -> containermanagerd XPC), which returned NULL (BaseBoard logs "Error getting shared system container ..."). With 0050 the sandbox denials are gone. containermanagerd.log.0 in the pulled (pre-0050) image: "Did not receive any persona attributes", "Expected to find at least one persona", notify_register_dispatch failed 9; `/private/var/containers` does NOT exist in the root image (on iOS it lives on the data volume). usermanagerd does create kernel personas 99/199/1000, but fails to save `/private/var/keybags/usersession.kb` and `persona.kb`: "Failed to atomically swap writing file: Operation not supported (45)" (HFS has no RENAME_SWAP). NEXT: create `/private/var/containers` (and check what containermanagerd needs for system group containers), fix or emulate RENAME_SWAP on HFS, then re-check backboardd.
- **Disk housekeeping (2026-10-17):** /home was at 4 GiB free. Moved (not deleted) `xnu/out-0010..0044` and old `shim/out/*.img`/`payload-*.bin` (everything before 0046) to `/run/media/dipa/android/ios-sweet-work/archive/{xnu,shim-out}` (6.3 GiB); /home now 8.7 GiB free. Large work files (phone-root.img 16 GiB, logs, tracev3 dumps) live in `/run/media/dipa/android/ios-sweet-work/`. **Patch 0051** (`xnu/patches/0051-sweet-crash-heap-strings.patch`, CI `39041440935`): on SIGABRT of a process in boot-arg `sweetscan` (default backboardd) the crash log prints heap text runs as `STR ...` (to find the NSException reason). Boot 0051n 14:41 UTC.
- **Boot 0049n (14:11 UTC, `logs/boot-0049n.txt`, patch 0049 trace): backboardd's IOKit lookups before it dies** (each run): `IODeviceTree:/arm-io/pearl-sep` -> none, matching ApplePearlSEPDriver -> none, `IOService:/IOResources/AppleKeyStore` open OK, matching IOHIDDevice (DeviceUsagePairs) / `HIDServiceSupport` notifications, `usb-drd,t8027` notification; **never any IOMobileFramebuffer / display lookup** - the exception happens before display detection. launchd (tracev3) shows backboardd's mach lookups denied with `error = 159: Sandbox restriction`: com.apple.mobilegestalt.xpc, com.apple.iohideventsystem, com.apple.system.notification_center, com.apple.logd, containermanagerd, ACCHWComponentAuthService, oscard. libsystem_sandbox uses `__mac_syscall("Sandbox", op, arg)` (ops: 1 init, 2 check, 3 note, 4 container path, 5/6/7/8 extensions, 0x15 check_bulk, ...); with no policy named "Sandbox" every call gets ENOPOLICY. **Patch 0050** (`xnu/patches/0050-sweet-sandbox-policy.patch`): built-in permissive MAC policy "Sandbox" in sweet_amfi.c (mpo_policy_syscall returns 0, container/extension ops ENOENT; logs first use of each op as `SWEET Sandbox: proc op N`).
- **Phone root pulled (16 GiB, 12 min, `adb exec-out dd if=/dev/block/sda34`) to `/run/media/dipa/android/ios-sweet-work/phone-root.img` (loop-mounted ro at /run/media/dipa/iOSRoot).** No .ips crash reports. logd tracev3 (Persist, LZ4 `bv41` blocks, decompressed strings in `ios-sweet-work/tracev3/all.txt`): /private/var/db/uuidtext is EMPTY so only launchd's own messages are readable. Findings: v8 launch failure = `Service could not initialize: posix_spawn(/usr/libexec/backboardd), error 0xd - Permission denied` (xpcproxy exit 78) - /dev/console not openable for the mobile user; backboardd[98] spawned `com.apple.MTLCompilerService` before SIGABRT; **launchd denies many mach lookups with `error = 159: Sandbox restriction`** (mediaserverd -> com.apple.backboard.display.services, remoted, mobiletimerd -> sleepd, identityservicesd -> apsd) and **tccd exits OS_REASON_SANDBOX "profile not found"** - no Sandbox kext/profiles on SWEET; likely cause of many daemon crash loops (next wall after the display). CF's uncaught-exception text never reaches stderr for daemons (no CF handler; libc++abi prints only the type). **Patch 0049** (`xnu/patches/0049-sweet-iokit-trace.patch`): `IOK name: ...` console lines for registry path lookups, child iterators, matching (with result count/class), matching notifications and IOServiceOpen of the processes in boot-arg `sweetiolog` (default backboardd), max 400 lines.
- **CONFIRMED: launchd StandardOut/ErrorPath=/dev/console stops backboardd from launching.** After the in-place rename (boot 0047n-b, log `logs/boot-0047n-b.txt`) backboardd launches again and dies as on v7: sig 6, `___pthread_kill <- abort <- demangling_terminate_handler <- _objc_terminate <- std::terminate <- _dispatch_client_callout <- _dispatch_once_callout <- main+0x9334` (window-server dispatch_once). It never opened AppleCLCD or IOCoreSurfaceRoot (no `SWEET FB/SURF: backboardd` lines) -> throws before/at display detection. **Patch 0048** (`xnu/patches/0048-sweet-devnull-tee.patch`, CI `39037749668` -> `xnu/out-0048`, image `shim/out/shim-boot-0048n.img`): writes to /dev/null by processes named in boot-arg `sweetnull` (default `backboardd,SpringBoard`) are printed as `|name| text`. Boot 0048n (13:48 UTC, log `logs/boot-0048n.txt`): only `|backboardd| libc++abi: terminating due to uncaught exception of type NSException` (CF's reason line goes to os_log, not stderr, despite CFLOG_FORCE_STDERR/OS_ACTIVITY_DT_MODE). Next: pull the whole 16 GiB root from recovery (`adb exec-out dd if=/dev/block/sda34`) to `/run/media/dipa/android/ios-sweet-work/phone-root.img` and read ReportCrash .ips files / logd tracev3 for the exception reason.
- **Persistent log WORKS (boot 0047n on v8, 13:31 UTC; pulled from OrangeFox: 70 KB, 111 flushes, `/run/media/dipa/android/ios-sweet-work/logs/boot-0047n.txt`).** In 3 min **backboardd was never exec'd** (v7 ran it), ~70 bare `exec xpcproxy`, SpringBoard loops on FBSDisplayMonitor (no display), mediaserverd sig 11 loop, locationd, lockdownd sig 5. Suspect the v8 plist (StandardOut/ErrorPath=/dev/console on backboardd). **In-place plist edit from recovery (no reflash):** launchd.plist is one extent at image/partition byte offset 0x1e025f000 (195 blocks; verified bytes identical on phone vs local v8 mount); renamed StandardOutPath->StandardOutPatX and StandardErrorPath->StandardErrorPatX (same length, both jobs) in blocks 68 and 105 via `adb push` + `dd of=/dev/block/sda34 seek=... conv=notrunc,fsync`, read back VERIFIED. Phone now differs from local v8 image in those 2 blocks (files in `/run/media/dipa/android/ios-sweet-work/`). Test boot 0047n 13:38:42 UTC. Recovery kernel has no hfsplus (raw block edits only).
- **Patch 0047: persistent console log (CI `39036478663` -> `xnu/out-0047`, QEMU no panic; phone image `shim/out/shim-boot-0047n.img` = 0047 + sweet-0046hi.adt + 0045n cmdline).** `_cnputs` (all console output: kernel printf + daemons' /dev/console) also appends to a 4 MiB ring in sweet_ufs.c; after the UFS partition is ready and writable (ufsrw=1) a thread writes new ring blocks + header to the LAST 1025 blocks (4 KiB) of userdata every ~1 s and SYNCHRONIZE CACHE (prints `SWEET LOG: console log to the last 4100 KiB ...`). Read: phone to fastboot -> `fastboot boot recovery/recovery.img` (OrangeFox) -> `tools/sweet-log-pull.sh OUT.txt` (adb dd of that area + `tools/sweet-log.py`). Not yet verified on the phone. Panics after the last flush are not in it (screen still shows them). 2x font attempt reverted: XNU's v_scale only scales the progress icon.
- **Boot 0046n on v8 (13:05 UTC, VID_20261017_150522_HSR_120):** phone prints `SWEET SURF: IOCoreSurfaceRoot registered` and `SWEET FB: AppleCLCD 1080x2400 stride 4320 at 0x9c000000, default surface 1` (nubs + match work on hardware). Visible userspace: early boot tasks, launchd_cache_loader, `exec SpringBoard`; no `exec backboardd` / `SWEET FB: backboardd` line seen in the readable frames (video blurry). Frame 00:47: lower half of the screen shows OLDER console text (16:01:12) below newer lines -> unconfirmed hint that a swap copied an old snapshot of the panel (CA reads the default/displayed surface = panel memory). SpringBoard still dies in `-[FBSDisplayMonitor _initWithBookendObserver:transformer:]+1160` (sig 5, slide 0x30960000). **Shim: 2x console font** (`shim/loader.c` Video.v_depth scale field = 1) so phone videos are readable; image `shim/out/shim-boot-0046b.img` = 0046n + 2x font.
- **Patch 0046: built-in IOSurface + IOMobileFramebuffer (2026-10-17, offline, NOT phone-tested).** `xnu/patches/0046-sweet-iosurface-iomfb.patch`: new `iokit/Kernel/arm/SweetSurface.{h,cpp}` (IOCoreSurfaceRoot + IOSurfaceRootUserClient: sel 13/0/4/34/35, traps 0-5, wired buffers mapped into the caller, per-client refs) and `SweetFramebuffer.cpp` (AppleCLCD : IOMobileFramebuffer on /arm-io/disp0: sizes, swap = CPU copy of enabled layers into the ABL panel memory, 60 Hz vsync via sendAsyncResult64WithOptions(CanDrop), panel memory published as the default IOSurface, kernel text console paused on the first swap only with `sweetfb_noconsole=1` (default keeps the console: pausing switches it to serial and would hide panics)); SweetPlatformExpert creates nubs for /arm-io children (not gic) attached to the platform expert (IOPlatformDevice::compareName casts its provider to IOPlatformExpert, so nubs under the arm-io nub never matched - first CI build showed that in QEMU). mkadt: /arm-io/disp0 {device_type display-subsystem, compatible sweet,display, canvas-width 1080, canvas-height 2400}. CI `39021572169` -> `xnu/out-0046`. **QEMU** (`research/q0046-hi.adt`, RAM disk init, msgbuf): `SWEET SURF: IOCoreSurfaceRoot registered`, `SWEET FB: AppleCLCD 1080x2400 stride 4320 at 0x9c000000, default surface 1`, init alive, no panic. Phone image **`shim/out/shim-boot-0046n.img`** (SHA256 9c4d2fe9..., CI `39024108588` with the review fixes: swap bounds check, zeroed 64-bit async ref, port release, 1.5 GiB wired budget, ref leak/race fixes; QEMU re-checked) = 0046 kernel + `shim/out/sweet-0046hi.adt` + the 0045n cmdline; boot it on image v8 (backboardd/SpringBoard log to console) and film. Expected new console lines: `SWEET SURF: <proc> create id ...`, `SWEET FB: backboardd sel N ...`, `SWEET FB: swap ...`. Open question for the next wall: QuartzCore's IOMFB server builds its renderer from Metal first (`CAMetalContextCreate`), GLES only when enabled; how the CPU renderer gets selected on a device without a GPU is not yet established.
- **IOSurface values ABI (offline RE, `/run/media/dipa/android/ios-sweet-work/iosurface-values.md`) - TODO in SweetSurface (0046 only accepts and drops values, so IOSurfaceCopyValue always returns NULL):** sel 9 SetValue in = {u32 id, u32 pad, IOCFSerialize([value, key]) or ([dict] = merge)}, sel 0xb RemoveValue in = {u32 id, u32 pad, key\0} (empty key = remove all); both out 4 bytes = new generation, client accepts only (gen+2)|1. Kernel after each change: gen = (gen+2)|1 (odd, never 0) -> state+0x20, serialized size (>=1) -> state+0x28. sel 0xa in {u32 id, u32 0, u8 0}, out {u32 ?, u32 gen, serialized non-bulk dict}; too small -> 0xe00002db + needed size (client retries x16). sel 0x1b in 0x88: bulk struct 0x70 @0, u64 valid size @0x70, u64 changed mask @0x78, u32 id @0x80 -> copy masked fields into state+0x30 (bit0 32B @0, bit1 16B @0x20, bit2 8B @0x30, bits3-10 1B @0x38..0x3f, bits11-14 24B @0x40/4B @0x58/8B @0x5c/1B @0x64).
- **IOMFB display matching confirmed (offline RE, `/run/media/dipa/android/ios-sweet-work/iomfb-match.md`):** the framework never matches on "AppleCLCD"; any registered IOMobileFramebuffer subclass works. `iomfb_match_callback` reads only `dfr`/`AppleTV`/`external` (CFBoolean, service itself, no parents); internal main display = all absent/false (type 0, name "primary"). Display count = /arm-io children whose device_type starts with "display-subsystem" (count 0 -> CreateDisplayList returns NULL; more nodes than services -> 30 s wait). IOMobileFramebufferOpen fails only on IOServiceOpen failure; canvas-width/height read as 4-byte CFData from the IOService-plane parent (optional). CopyProperty = IORegistryEntrySearchCFProperty on the service only. Patch 0046 (disp0 node, `external`=false, AppleCLCD : IOMobileFramebuffer) fits all of this.
- **IOMobileFramebuffer swap + notification ABI (2026-10-17, offline).** Swap record = fb+0x18, **0x46c bytes**, zeroed by SwapBegin and sent whole by `kern_SwapEnd` = IOConnectCallStructMethod(sel 5, rec, 0x46c, no output). **SwapBegin** = sel 4, no input, 1 scalar out = swap id (stored at rec+0x50). `kern_SwapSetLayer(fb, layer<4, IOSurfaceRef, CGRect a, CGRect b, flags)`: rec+0x54+4*layer = **IOSurface id**; rec+0x104 bit layer = layer enabled (rec+0x108 bit cleared); rect a (int x,y,w,h, scaled) at rec+0x64+16*layer, rect b at rec+0xc4+16*layer; rec+0x114+4*layer = transform from flags&0xf; flag bits 5/31/6/7/8/9 set bytes rec+0x2ca/0x2cc/0x2e3/0x2e5/0x2e6/0x467+layer. A NULL surface only sets the enable bit with zero id. SwapWait = sel 6 scalars [swap id, timeout, 0].
  - **Notifications**: `IOMobileFramebufferScheduleWithDispatchQueue`/`GetRunLoopSource` create an IONotificationPort and `IOConnectSetNotificationPort(conn, type, port, 0)` (kernel `registerNotificationPort`). `kern_EnableNotifications(fb, type, cb, ctx)` = **sel 72 scalars [NotifyCallbackFuncs[type], fb, type, 0]** -> the kernel keeps an async reference {port, func, refcon=fb} per type and fires it with `sendAsyncResult64`. Types: 0 HotPlug, 1 Power, 3 FrameInfo (args[0] = mask of 31-bit keys, args[1] u32, then values), 4 CRC, **5 Vsync**: 6 args, each a 32-bit half in a u64 slot: (ts lo, ts hi), (t2 lo, hi) passed through the time-ingest helper, (t3 lo, hi); the framework then calls the client's vsync callback(fb, ts, t2', t3, ctx). Vsync callbacks are dropped while the notification port has queued messages.

- **IOSurface.framework user-client ABI reversed (2026-10-17, offline, step 2 of the GUI plan).** `ipsw dyld disass research/dsc/dyld_shared_cache_arm64 --image IOSurface` (selector scan script: scratchpad `selscan.py`).
  - Connect (`_iosConnectInitalize`, pthread_once): `IOServiceGetMatchingService(IOServiceNameMatching("IOCoreSurfaceRoot"))`, retried with sleep(1) up to 241 times (a missing service stalls every client ~4 min, no crash); `IOServiceOpen(type 0)`; then **sel 13** (no inputs, struct out 0x18 bytes = `_ioSurfaceLimits`) and requires u16 at out+0x16 == 1 (ABI version); out+0 = offset/plane-base alignment mask, out+4 = bytes-per-row alignment mask (used as (x+m)&~m), +0..+0x14 also copied into IOSurface remote-method init, otherwise logs and closes the connection.
  - **Create = sel 0**: scalar in [parent id or 0], struct in = `IOCFSerialize(props, kIOCFSerializeToBinary)` (OSUnserializeBinary format; keys IOSurfaceWidth/Height/BytesPerRow/BytesPerElement/PixelFormat/AllocSize/PlaneInfo/CacheMode/IsGlobal/...), struct out **0xa68 bytes** ("lock result"). **Lookup = sel 4**: scalar in [id], same struct out. LookupFromMachPort = sel 0x22 (scalar in [port name]); CreateMachPort = sel 0x23 (scalar in [id, options], scalar out [port name]).
  - Lock result (copied to client+0x68, size 0x68 + planes*0x80, min 0xe8): 0x00 u64 base address **mapped in the caller's task**; 0x08 u64 task VA of a per-surface shared state page (+0 u64 registry id, +8/+0xa u16 bound accel ids, +0xc u32 seed, +0x14 u8 tiled, +0x20 u32 value generation, +0x24 YCbCr matrix, +0x28 u32 non-bulk values size, +0x2d u8 displayable, +0x2e u8 sysmem-only, +0x30 0x70 bytes bulk attachments); 0x10 u64 task VA of timestamp page (4 u64 indexed timestamps, +0x20 detach code); 0x18 u32 surface id; 0x1c u32 alloc size; 0x20 width; 0x24 height; 0x28 bytes per row; 0x2c buffer offset; 0x30 pixel format; 0x34 u32 (dcache flush length); 0x38 plane count; 0x40 u16 bytes/element; 0x42 u8 element width; 0x43 u8 element height; 0x44 cache mode; 0x4c u8 subsampling; 0x4d u8 prohibit-use count; 0x50 parent id; 0x54 slice count; 0x58 u64 trace id; 0x60 u64 protection options; planes[n] at 0x68+n*0x80 (+0 width, +4 height, +8 bytes/row, +0xc offset, +0x14 size, +0x18 u16 bpe, +0x1a/+0x1b u8 element w/h, +0x1c u8 component count, +0x1d address format, +0x54 u8 compression type (non-zero -> no CPU base address)).
  - **Traps** (IOConnectTrapN -> `IOUserClient::getTargetAndTrapForIndex`): 0 IncrementUseCount(id, category), 1 DecrementUseCount(id, category), 2 **Lock**(id, options, &seed_out), 3 **Unlock**(id, options, &seed_out), 4 Release(id), 5 Release after a failed create/lookup setup (id).
  - Other selectors: 5 SetYCbCrMatrix, 6 WrapClientImage, 7 WrapClientMemory, 9 SetValue (serialized), 0xa UpdateNonBulkValueCache (struct in 9), 0xb RemoveValue, 0xc BindAccel, 0x11 SetSurfaceNotify (async), 0x12 RemoveSurfaceNotify, 0x13 Log, 0x14 SetPurgeable, 0x15 SetOwnership, 0x16 SetTiled, 0x18 SetTimestamp, 0x19 GetTileFormat, 0x1a CopyDataValueBytes, 0x1b SetBulkAttachments (struct 0x88), 0x1e/0x2e-0x31 (via outlined helpers), 0x1f SetCompressedTileDataRegionMemoryUsed, 0x20 GetGraphicsCommPageAddress, 0x21 SetIndexedTimestamp, 0x24-0x26/0x2d IOSurfaceAccelerator, 0x27-0x29 shared events, 0x2a SignalEvent, 0x2b Set/InitDetachModeCode, 0x2c SetOwnershipIdentity, 0x32-0x34 data properties.
  - => SWEET kernel service: class/name **IOCoreSurfaceRoot** + IOSurfaceRootUserClient; minimum = sel 13, 0, 4, 9/0xa/0xb (values), traps 0-5, 0x22/0x23 later for cross-process surfaces (CA sends surfaces to backboardd by mach port). Memory: IOBufferMemoryDescriptor per surface, mapped into each task with createMappingInTask; ids from a global table.

- **Image v8: daemon logs on the console.** `tools/patch-launchd-plist.py IN OUT LABEL...` rewrites launchd.plist (binary, plistlib): renames every `_PanicOnCrash` to `_PanicOnCrasX` and gives the listed jobs `StandardOutPath`/`StandardErrorPath` `/dev/console` (devfs console is 0622, writable by mobile) plus `OS_ACTIVITY_DT_MODE=YES` (os_log mirrored to stderr) and `CFLOG_FORCE_STDERR=1`. v8 = v7 + that plist for com.apple.backboardd and com.apple.SpringBoard, written through the mount (796310 bytes, root:80 0644), SHA256 in `ios16-root-20H392-v8.img.sha256`, `.simg` ready; boot with `shim/out/shim-boot-0045n.img`. Goal: see backboardd's uncaught exception text and the window server's display probing. ODDITY (unresolved): the v5 raw-image rename at offset 0x1e025f000 is present in the v5-v7 image bytes, but the plist read through a Linux mount of v7 still had the original `_PanicOnCrash` keys; filefrag shows the file as one extent. Never patch file contents through raw offsets again; write through the mount.
- **IOMobileFramebuffer.framework reversed (step 1 of the GUI plan).** `ipsw dyld disass research/dsc/dyld_shared_cache_arm64 --image IOMobileFramebuffer`.
  - Display discovery (`IOMobileFramebufferCreateDisplayList` -> `getDisplayListNumber`): iterates children of `IODeviceTree:/arm-io`, counts nodes whose `device_type` is "display-subsystem" or "ext-display-subsystem" (or `compatible` "paravirtualizedgraphics,gpu"); then `iomfb_populate_display_infos` adds an IOServiceAddMatchingNotification(IOServiceFirstMatch, **IOServiceMatching("IOMobileFramebuffer")**) and runs the run loop up to 30 s until that many services matched. `iomfb_match_callback` reads service properties `dfr`, `AppleTV`, `external` (CFBoolean) and names displays (external ones "%s-%d").
  - `IOMobileFramebufferOpen(service, task, type, &fb)`: `__ioMobileFramebufferAlloc` (CFPreferences com.apple.iokit.IOMobileGraphicsFamily: canvas_width/height, override_display_width/height, override_panel_width/height, benchmark, enable_ktrace), `IOServiceOpen(service, task, type)` (GetMainDisplay passes type 0), `getEDTProperty` reads `canvas-width`/`canvas-height` from the service's IODeviceTree parent, then fills a table of `kern_*` function pointers.
  - User client selectors (`kern_*` -> IOConnectCall*): 3 _kern_GetLayerDefaultSurface[ScalarMethod_stub]; 4 _kern_SwapBegin[ScalarMethod_stub]; 5 _kern_SwapEnd[StructMethod_stub]; 6 _kern_SwapWaitWithTimeout[ScalarMethod_stub] _kern_SwapWait[ScalarMethod_stub]; 7 _kern_GetID[ScalarMethod_stub]; 8 _kern_GetDisplaySize[ScalarMethod_stub]; 10 _kern_SetTVOutMode[ScalarMethod_stub]; 11 _kern_SetWSSInfo[ScalarMethod_stub]; 12 _kern_RequestPowerChange[ScalarMethod_stub]; 13 _kern_EnableStatistics[ScalarMethod_stub]; 14 _kern_SetFlags[ScalarMethod_stub]; 15 _kern_SetDebugFlags[ScalarMethod_stub]; 16 _kern_SetTVOutSignalType[ScalarMethod_stub]; 17 _kern_SetGammaTable[StructMethod_stub]; 18 _IOMobileFramebufferIsMainDisplay[ScalarMethod_stub]; 19 _kern_SetWhiteOnBlackMode[ScalarMethod_stub]; 20 _kern_SwapSignal[ScalarMethod_stub]; 22 _kern_SetDisplayDevice[ScalarMethod_stub]; 23 _kern_SetDigitalOutMode[ScalarMethod_stub]; 24 _kern_GetHDCPDownstreamState[StructMethod_stub]; 25 _kern_GetDigitalOutState[ScalarMethod_stub]; 26 _kern_printDisplayRegs[ScalarMethod_stub]; 27 _kern_GetGammaTable[StructMethod_stub]; 28 _kern_GetDotPitch[ScalarMethod_stub]; 29 _kern_GetDisplayArea[StructMethod_stub]; 30 _kern_EnableDisableDithering[ScalarMethod_stub]; 31 _kern_SetUnderrunColor[ScalarMethod_stub]; 33 _kern_EnableDisableVideoPowerSavings[ScalarMethod_stub]; 34 _kern_SetVideoDACGain[ScalarMethod_stub]; 35 _kern_SetLine21Data[ScalarMethod_stub]; 41 _IOMobileFramebufferEnableMirroring[ScalarMethod_stub]; 42 _IOMobileFrameBufferGetMirroringCapability[StructMethod_stub]; 43 _IOMobileFramebufferSetRenderingAngle[StructMethod_stub]; 44 _IOMobileFramebufferSetMirrorContentRegion[StructMethod_stub]; 47 _kern_HDCPSendRequest[ScalarMethod_stub]; 48 _kern_HDCPGetReply[ScalarMethod_stub]; 49 _kern_SurfaceIsReplaceable[ScalarMethod_stub]; 50 _kern_SetBrightnessCorrection[ScalarMethod_stub]; 51 _kern_SetColorRemapMode[ScalarMethod_stub]; 52 _kern_SwapCancel[ScalarMethod_stub]; 53 _IOMobileFramebufferSetCanvasSize[ScalarMethod_stub]; 54 _IOMobileFramebufferGetMatrix[Method_stub]; 55 _IOMobileFramebufferSetMatrix[Method_stub]; 56 _IOMobileFramebufferKernelTests[StructMethod_stub]; 57 _kern_GetColorRemapMode[ScalarMethod_stub]; 66 _kern_SPLCSetBrightness[ScalarMethod_stub]; 67 _kern_SPLCGetBrightness[ScalarMethod_stub]; 68 _kern_SetParameter[Method_stub]; 69 _kern_SwapSetColorMatrix[StructMethod_stub]; 72 _kern_DisableNotifications[ScalarMethod_stub] _kern_EnableNotifications[ScalarMethod_stub]; 73 _kern_ChangeFrameInfo[ScalarMethod_stub]; 74 _kern_SupportedFrameInfo[Method_stub]; 75 _kern_FactoryPortal[StructMethod_stub]; 77 _kern_GetCurrentAbsoluteTime[ScalarMethod_stub]; 78 _kern_SetBlock[Method_stub]; 79 _kern_GetBlock[Method_stub]; 80 _kern_GetLinkQuality[ScalarMethod_stub]; 81 _kern_SwapCancelAll[ScalarMethod_stub]; 82 _kern_GetProtectionOptions[ScalarMethod_stub]; 83 _kern_CopyLayerDisplayedSurface[ScalarMethod_stub]; 84 _kern_SetContrast[StructMethod_stub]; 85 _kern_GetBufBlock[Method_stub]; 86 _IOMFBGainEncoderFinishEncoding[Method_stub]; UNKNOWN {}
  - => Kernel needs: an `/arm-io` child node with device_type "display-subsystem" (+ canvas-width/height) and an IOService of class **IOMobileFramebuffer** (subclass name match) attached under it, opened with type 0, implementing at least GetDisplaySize(8), IsMainDisplay(18), GetID(7), GetLayerDefaultSurface(3), SwapBegin(4)/SwapEnd(5 struct)/SwapWait(6), Enable/DisableNotifications(72), frame info(73/74), CopyLayerDisplayedSurface(83), plus IOSurface for the swapped buffers. NEXT: CoreAnimation's AppleDisplay/IOMFBDisplay usage of these (constructor, first swap, vsync), then IOSurface.framework's IOSurfaceRoot selectors.
- **GUI PLAN (decided 2026-10-16): CPU rendering + kernel IOMobileFramebuffer.** User: CPU rendering is fine for now (goal = prove the GUI runs), may later research an Apple-style GPU driver for the Adreno 618 -> keep display output and renderer separable. QuartzCore findings (symbols from the cache's .symbols subcache: `ipsw dyld symaddr research/dsc/dyld_shared_cache_arm64 --image QuartzCore`; strings: `ipsw dyld macho ... QuartzCore --strings`):
  - Renderers: `sw_new_context` (CA::OGL::SWContext, full CPU renderer incl. blur, images, IOSurface-backed surfaces, make_buffer_current(WindowServer::Surface)), `gles_new_context`, `metal_new_context`, `new_null_context`. Env knobs include CA_ENABLE_OGL, CA_DISPLAY_TYPE, CA_FORCE_LOCAL_SERVER, CA_FORCE_TIMER, CA_CANVAS_WIDTH/HEIGHT, CA_MAIN_DISPLAY_SCALE/ORIENTATION, CA_DISABLE_RENDER, CA_ALWAYS_RENDER (selection logic not traced yet).
  - `-[CAWindowServer _detectDisplays]` (0x1884e3150) iterates static tables `open_funcs`/`count_funcs` = AppleCLCDDisplay, AppleRGBOutDisplay, AppleWirelessDisplay only; each `count()` = `display_count_of_type(IOMFBDisplayType)` over **`IOMobileFramebufferCreateDisplayList()`**, `open(i)` = `create_display_of_type` -> `CA::WindowServer::AppleDisplay(CFString name, ..., IOMFBDisplayType)` (an IOMFBDisplay driven by IOMFBServer: vsync_callback, frame_info_callback, swaps). `CA::WindowServer::VirtualDisplay` exists but is never auto-detected (explicit API only). => the main display MUST come from an IOMobileFramebuffer kernel service.
  - NEXT: reverse IOMobileFramebuffer.framework: IOMobileFramebufferCreateDisplayList / IOMobileFramebufferOpen (service matching, display type property), the user-client selectors used by IOMFBServer (display size/modes, swap begin/set-layer/end with IOSurface ids, vsync notifications), then the IOSurface kernel side (IOSurfaceRoot user client: create/lookup/lock, memory mapping) that both IOMFB swaps and CA surfaces need. Kernel: SWEET IOMobileFramebuffer service that copies the swapped IOSurface to the 1080x2400 framebuffer at 0x9c000000.
- **logd fixed; backboardd = DISPLAY WALL (boot 0045n on v7, 21:08:57 UTC, frames VID_20261016_230850 00:55-01:28, slide 0x4c3ec000, `research/crash-0045n-v7.txt`).** No `CRASH logd` any more; new daemons run (runningboardd, WirelessRadioManagerd, networkserviceproxy, dasd, cloudpaird, magicswitchd, atc, askpermissiond, ManagedSettingsAgent, containermanagerd uses AKS 0/17). New: locationd sig 11 at CFRunLoopAddSource+132 (NULL source) from its main+0x2af138 in a dispatch_once. **backboardd** sig 6: abort <- std::terminate <- _objc_terminate <- dispatch_once <- main+0x9334 = the "start %{public}@..." wrapper (0x100009264) for **"window server"** (block 0x10000a770 -> dispatch_once body 0x10001d7f0 = StartWindowServer): MTLSetShaderCachePath, `[CAWindowServer serverWithOptions:@{kCAWindowServerDisableUpdatesOnMainDisplay: @YES}]`, `setRendererFlags:`, **`mainDisplay`** -> `displayId` -> `[CADisplay displayWithDisplayId:]`, setWindowServerDisplay:, bounds, pointScale, currentMode, preferredScale, nativeOrientation, touchScales... With no display, mainDisplay is nil and it throws. (HID system and GS start fine before it.) SpringBoard dies on the same missing display (FBSDisplayMonitor). QuartzCore display backends (from the cache's .symbols subcache, `ipsw dyld str`): `CA::WindowServer::AppleCLCDDisplay` (IOMobileFramebuffer hardware) and **`CA::WindowServer::VirtualDisplay`** (open(), new_server, clone_update). `CA_DISPLAY_TYPE` and `CA_FORCE_LOCAL_SERVER` strings exist in QuartzCore but have no direct xref (likely read via a table of CA_* env names). NEXT: find how CA::WindowServer::Server enumerates displays (IOMobileFramebuffer services vs VirtualDisplay / CA_DISPLAY_TYPE) and choose: (a) kernel IOMobileFramebuffer service + IOSurface, or (b) a VirtualDisplay rendered by CA's CPU path (CA::OGL::SW) and copied to the framebuffer.
- **watchdogd + CommCenter + identityservicesd fixed (boot 0045n on v6, 20:41:30 UTC, frames VID_20261016_224133 00:39-01:13, slide 0x20fec000).** `SWEET WDT: watchdogd sel 0 in 0/0 out 1/0 -> ok`, no watchdogd/CommCenter/identityservicesd crashes (CommCenter/identityservicesd now call AKS 0/17/7). usermanagerd boot task runs (UMD_INIT creates primary session uid 501 "mobile", personas 99 System and 199 Default registered with the kernel); `Failed to atomically swap writing file /private/var//keybags/usersession.kb: Operation not supported (45)` (HFS lacks the atomic swap rename; non-fatal so far). Remaining: SpringBoard (FBSDisplayMonitor, no display), backboardd (uncaught exception), mediaserverd, lockdownd (crash inside obfuscated code, main+0x4c1b4?), logd. **logd**: main+0x18160 = `BUG IN LIBTRACE: Failed to migrate directory` from 0x10001801c(dir 0): 0x100016538 requires the dir to exist with uid/gid/mode from the table at 0x10002df14 (0: /private/var/db/diagnostics 272:272 0751, 1: /private/var/db/uuidtext 272:272 0755, 2: /private/var/db/diagnostics/timesync 272:272 0755) plus a `.migrated` file, else XPC "operation 6" to a helper and crash. **Image v7** = v6 + those dirs/markers (also in mkiosroot.sh), SHA256 in `ios16-root-20H392-v7.img.sha256`, `.simg` ready. Boot with `shim/out/shim-boot-0045n.img`.
- **Exit-reason text works (boot 0044n, frames VID_20261016_221726 00:32-00:53, slide 0x22d5c000).** CommCenter/identityservicesd: `couldn't dlopen libobjc-trampolines.dylib: dlopen(/usr/lib/libobjc-trampolines.dylib, 0x0106): tried: '/usr/lib/libobjc-trampolines.dylib' (no such file, not in dyld cache)`: the file only exists in the OS cryptex and dyld does not search cryptexes at ignition_level=1. 19 cryptex files have no root counterpart (OS: DriverKit dyld cache + .symbols, VisualTestKit, libffi-trampolines, libobjc-trampolines, libstdc++ 6.0.9 + 2 symlinks; App: SafariSupport.bundle, AuthenticationServicesAgent, com.apple.Safari.History, passwordbreachd, safarifetcherd, webbookmarksd, webinspectord, webpushd) -> hard-linked (symlinks copied: Linux hfsplus cannot hard-link symlinks); `tools/mkiosroot.sh` does it generically. watchdogd still crashed: the `-wdt_no_pmu` / `/arm-io/wdt no-pmu` check (0x10000a01c) only runs when os_variant_has_internal_diagnostics; otherwise 0x100009b18 looks up IOServiceMatching("IOService") + IOPropertyMatch {IOPMUPrimary: 1} (NSConstantDictionary) and crashes if absent, then IORegistryEntrySetCFProperty(boot stage 0xff) (failure only logged). Patch **0045**: IOWatchdog sets IOPMUPrimary = 1 and accepts setProperties; CI `38961814194` -> `xnu/out-0045`. **Image v6** = v5 + the 19 cryptex links, SHA256 7c610c6a...297a, `ios16-root-20H392-v6.simg` (full flash needed). Boot image `shim/out/shim-boot-0045n.img` (0045 + sweet-0044hi.adt). Still open: SpringBoard (no display), backboardd (uncaught exception, reason none), mediaserverd (Fig NULL dict), logd (main+0x18160), lockdownd (main+0x4c1b4).
- **System survives daemon crashes (boot 0043p, video frames VID_20261016_215006 00:25/00:42/00:54).** With the v5 plist patch no panic: launchd keeps launching (runningboardd, powerd, tccd, healthd, peopled, cryptexd, routined, aksd, mediaremoted, familynotificationd, nanoprefsyncd, navd, cloudpaird, passd, amsaccountsd, accessoryupdaterd, wcd ...). Shared cache slide that boot 0x406b4000 (`research/crash-0043p.txt`). watchdogd still crashed at main+0xb82c from the PMU step: `-wdt_no_pmu` is only honored when os_variant_has_internal_diagnostics; customer builds read `no-pmu` from IODeviceTree:/arm-io/wdt (IORegistryEntrySearchCFProperty) -> mkadt adds /arm-io/wdt {no-pmu}. **cryptexd** sig 6: abort_with_payload <- os_crash_fmt <- `__darwin_arm_secure_boot_chip.cold.7` ("panic: failed to get crypto algorithm") <- `_img4_chip_select_personalized_ap`: reads /chosen use-ddi-secure-boot, allow-ecid-mismatch, crypto-hash-method ("sha1" | "sha2-384"), /chosen/asmb lp-smb0/1 -> mkadt adds crypto-hash-method "sha2-384". **identityservicesd** sig 6 = same `_objc_fatal` in imp_implementationWithBlock as CommCenter (block trampolines; message needed). lockdownd sig 5 at main+0x4c1b4. Patch **0044**: crash report adds `CRASH name reason ns N code X: text` (exit reason description = abort_with_payload text). CI `38959096811` -> `xnu/out-0044`, QEMU OK. Image `shim/out/shim-boot-0044n.img` = 0044 + `shim/out/sweet-0044hi.adt` (wdt no-pmu, crypto-hash-method) + cmdline (wdt=-1, no -wdt_no_pmu).
- **First symbolicated daemon crashes (boot 0043u on journaled v4, 19:38:53 UTC; video frame chat image 36; transcribed in `research/crash-0043u.txt`; shared cache slide 0x40d60000 for every process).** (Gemini's video transcription invented values, use frames only.) `tools/sweet-crash.py research/dsc/dyld_shared_cache_arm64 x research/crash-0043u.txt`:
  - **watchdogd** pc main+0xb82c (`_os_crash` trap helper) from 0x100009bb0 = set PMU boot stage via IORegistry (no PMU) -> fix: boot-args `wdt=-1 -wdt_no_pmu` (Apple's own test mode writes "%s wdt=-1 -wdt_no_pmu"; watchdogd logs "skipping setting PMU boot stage because -wdt_no_pmu found in boot-args or no-pmu found in EDT"). Kernel effect of wdt=-1: sched hygiene debug off, zone_exhausted_timeout -1 (harmless).
  - **SpringBoard** sig 5 in `-[FBSDisplayMonitor _initWithBookendObserver:transformer:]+1160` <- `+[FBDisplayManager sharedInstance]` <- `FBSystemShellInitialize` <- `SBSystemAppMain`: no main display. GUI WALL: display service (IOMobileFramebuffer / CoreAnimation display).
  - **backboardd** sig 6: abort <- std::terminate <- _objc_terminate (uncaught exception; message not shown).
  - **CommCenter** sig 6: `_objc_fatal` in `imp_implementationWithBlock` (from `+[_PFRoutines initialize]`, CoreData): objc block trampolines cannot be allocated -> likely kernel gap (trampoline page remap); will hit many processes.
  - **mediaserverd** sig 11: CFDictionaryGetValue(NULL) in FigNotificationListenerStartNotifications (routing session manager).
  - **logd** sig 5 at its main+0x18160 (bt main+0x9dfc); lockdownd sig 5 (not yet symbolicated).
  - Image v5 = v4 + launchd.plist (`/System/Library/xpc/launchd.plist`, contiguous at image offset 0x1e025f000, 1456980 bytes) with the 7 `_PanicOnCrash` keys renamed `_PanicOnCrasX` in place (raw image patch, no metadata change) -> `diff-v4-v5.simg` = 7 blocks; v5 SHA256 78f96974...185a. Boot image `shim/out/shim-boot-0043p.img` = 0043 + `wdt=-1 -wdt_no_pmu`.
- **0043 console crash reports (QEMU verified); image `shim/out/shim-boot-0043u.img`; NEXT: flash v4 + boot 0043u.** Boot 0042u (video photo IMG_20261016_211646): short exec lines work; watchdogd crashes with NO `SWEET WDT:` line (fails before its first IOWatchdog call: lookup or IOServiceOpen, or elsewhere); lockdownd, SpringBoard, mediaserverd, CommCenter, identityservicesd, backboardd, watchdogd all crash repeatedly ("Too many corpses being created" = corpse limit, no crash reports). AKS callers: lockdownd (0, 7), imagent/sleepd (0, 17, 7), backboardd (0, 17), UserEventAgent (0, 7, 102, 103 -> unsupported). Patch **0043**: `sweet_crash_log` (osfmk/kern/exception.c, called from proc_prepareexit for crash exits on the current proc) prints `CRASH name[pid] sig S code (exc<<32|code) sub X slide SR mh MH`, `CRASH name pc lr sp fp far`, `CRASH name bt` (10 fp frames); AKS sel 103 notify_state_is_set -> 0. CI `38954520419` -> `xnu/out-0043`. QEMU test: init forks, child `brk #1`: `CRASH launchd[2] sig 5 code 0x600000001 sub 0x1000004f0 slide 0x0`, pc correct, parent keeps running (pid 1 crashes panic before proc_prepareexit, so test with a child). `tools/sweet-crash.py CACHE ROOT [report]` symbolicates typed-in CRASH lines (`ipsw dyld a2s` with addr - slide; main binary offsets = addr - mh + 0x100000000).
- **v3 reflashed 18:50-18:55 UTC (`research/flash-userdata-v3b.log`, 24/24 OKAY); 0042u booted 19:01:17 UTC on the clean disk (`research/boot0042u-2.log`), SLOW MO VID pending (watchdogd failure reason).** ABL hangs on the first `fastboot boot` after every big flash; user re-enters fastboot. User gave standing approval to reflash/boot without asking (memory standing-flash-approval). Commits now end with `Co-Authored-By: dipa-studio <183933817+dipa-studio@users.noreply.github.com>` (user request; never a Claude trailer).
  - watchdogd flow: connect_to_kext (0x100005408): IOServiceGetMatchingService("IOWatchdog") fails -> "failed to discover" + _os_crash; IOServiceOpen(type 1) fails -> "IOServiceOpen failed with error : 0x%x" + _os_crash. Then sel 0 (out 1 scalar): 0 -> "userspace monitoring disabled", 0x100009bb0, sleep 2, exit(0); nonzero -> "userspace monitoring enabled", normal operation.
  - **Image v4 (JOURNALED):** `tools/mkiosroot.sh` now does `mkfs.hfsplus -J`, mounts with `-o loop,force`, adds the /System/Library/Caches/com.apple.dyld hard links (44) and /private/var/keybags/systembag.kb (0700/0600 root). Built from the IPSW dmgs (OS 087-86698-044, SystemOS 087-86593-047, AppOS 087-86715-047) -> `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v4.img` SHA256 fba4aeae...ec0f9 + `.simg`. Header: attr 0x80002100 (unmounted, journaled), journal info block 129, journal 8 MiB at 532480 flagged need-init. Linux `fsck.hfsplus -n` reports "Volume header needs minor repair" on any fresh journaled volume even after -y (quirk). QEMU: 64 MB journaled test root (`rd=md0 rootrw=1`, 0042 kernel): `hfs: Initializing the journal (joffset 0x3000 sz 0x80000)` -> mounted -> init runs, no panic. NEXT: flash v4 (full), boot 0042u.
- **SPRINGBOARD STARTS (boot 0041u 18:39:53 UTC, photo IMG_20261016_204142).** backboardd, bluetoothd, fairplayd.H2, SpringBoard (pid 111, crashed: "Too many corpses"), xpcproxy run; `SWEET AKS: backboardd sel 0 -> 0`, `sel 17 in 1/0 out 0/4096 -> 0`. Panic: watchdogd[113] exited, namespace 2 subcode 5 (SIGTRAP = its _os_crash): watchdogd crashes on purpose when IOServiceGetMatchingService("IOWatchdog") fails ("connect_to_kext() unexpectedly failed") or IOServiceOpen(type 1) fails ("IOServiceOpen failed with error"); IOWatchdog DOES register (QEMU msgbuf: `SWEET WDT: IOWatchdog registered`), cause not on screen yet -> need video. Note `wdt_test=no_user_checkin` makes watchdogd log "detected testing boot-args to not run, exiting" (path not reached here?). **HFS CORRUPTION:** `hfs_swap_BTNode: offset #0 invalid (0xBC1D) (blockSize 0x2000 numRecords 81)`, `node=19677 fileID=4` (catalog), `hfs_mark_inconsistent` repeated. Likely cause: non-journaled HFS + unclean panics while writing (0038e wrote a 2.7 GB core then panicked; every boot since ends in panic). Plan: reflash v3 (clean), longer term HFS journaling. Patch **0042**: one short `exec NAME` console line instead of the 3-line "Allowing spawn of iOS binary" notice; CI `38949451276` -> `xnu/out-0042`; image `shim/out/shim-boot-0042u.img` (same cmdline as 0041u).
- **LAUNCHD DAEMONS RUN (boot 0039u, 18:29:13 UTC, photo IMG_20261016_203052).** With `launchd_unsecure_cache=1` all boot tasks pass and launchd starts LaunchDaemons (pids > 100: identityservicesd 114 and lockdownd 106 crash, "Too many corpses being created"). Fatal: `watchdogd: ERROR: failed to discover watchdog KEXT service` -> exit (namespace 2 = signal, subcode 5) -> `_PanicOnCrash` panic. watchdogd: IOServiceMatching("IOWatchdog"), IOServiceOpen type 1, IOConnectCallScalarMethod sel 0/1 (check in)/3/4 (disable/enable userspace monitoring)/5, IOConnectCallStructMethod sel 2 (1 KiB in) and 9 (small out); VM path ("detected virtual machine environment and no watchdog KEXT found, exiting...") only when it detects a VM. Console also flooded with `hfs: set hardlink bit on vol=iOSRoot cnid=321318` (Linux-made hard links lack kHFSHasLinkChainBit; repaired only in memory on each lookup). Patches **0040** (`iokit/Kernel/arm/SweetWatchdog.cpp`: IOWatchdog + IOWatchdogUserClient, all selectors succeed with zeroed outputs, each logged once as `SWEET WDT: ...`) and **0041** (sweet_hfs hfs_catalog.c: the three link-repair printfs limited to 8 per boot); CI `38948245372` PASSED -> `xnu/out-0041` (QEMU regression OK). Image `shim/out/shim-boot-0041u.img` (0041 + sweet-0038hi.adt + ufsrw rootrw + launchd_unsecure_cache=1) booted 18:39:53 UTC (`research/boot0041u.log`), photo pending.
- **v3 FLASHED + keybag passes; next wall AMFI (launchd_cache_loader).** User said "flash, nothing to lose": `fastboot -S 512M flash userdata ios16-root-20H392-v3.simg` 17:51:52-17:57:01 UTC, 24/24 chunks OKAY (`research/flash-userdata-v3.log`). userdata = v3 (SHA256 fa84274c...22df) until the next rw boot. ABL fastboot then hung ("Sending" forever, `reboot bootloader` timed out) until the user re-entered fastboot by hand (common Xiaomi ABL crash). Boot 0038e 18:06:15 UTC (`research/boot0038e-3.log`), photos IMG_20261016_200812/200838: keybag OK, then boot tasks tzinit (`Bad zoneinfo link`, resets to system partition, OK), finish-restore, finish-demo-restore, sysstatuscheck, prng_seedctl (`failed to load kernel prng seed`, `failed to load virtual random (-147)`, AllowCrash), auearlyboot, then **launchd_cache_loader: `abort: Unable to find AMFI`** -> 2.7 GB core written to /cores in 91 s -> launchd panic `launchd_cache_loader[22] exited -- exit reason namespace 7 subcode 0x1`. launchd_cache_loader: SecStaticCodeCheckValidity of /System/Library/xpc/launchd.plist with detached .sig, then IOServiceMatching("AppleMobileFileIntegrity") + IOServiceOpen type 0 + IOConnectCallMethod sel 6 (1 scalar = 1, struct in = cdhash) = trust the cdhash, then sends the cache to launchd. Boot-arg `launchd_unsecure_cache=1` skips signature + AMFI ("Using unsecure cache"); the value is parsed with strtoul base 10 (helper 0x100002da8), so a path = 0 = off: boot 0039w (18:17:13 UTC, `=/System/Library/xpc/launchd.plist`, photo IMG_20261016_202008) still aborted `Unable to find AMFI` (core dump now skipped: `Failed to generate core file ... error 14`, so 0039 works). Image `shim/out/shim-boot-0039u.img` uses `launchd_unsecure_cache=1`. Patch **0039**: do_coredump = 0 on SWEET (kern.coredump sysctl still works); CI `38945267341` -> `xnu/out-0039` (_do_coredump now in __common). Image `shim/out/shim-boot-0039w.img` = 0039 + sweet-0038hi.adt + ufsrw rootrw + `launchd_unsecure_cache=/System/Library/xpc/launchd.plist`. TODO later: real AppleMobileFileIntegrity IOService (sel 6 trust cdhash etc.).
- **Image v3 ready, awaiting user "flash".** Boot 0038w 17:38:10 UTC, photo (chat image 30): `SWEET AKS: keybagd sel 0 -> 0x0`, `sel 14 out 1/0 -> 0x0` (x2), `MKB_INIT: mount is with NO CPROTECT ... does not support Data Protection`, `System Keybag loaded`; then keybagd still opens /private/var/keybags/systembag.kb (0x100012d3c, for BackupKeyBagKeys) -> ENOENT, `no-effaceable-storage` not set -> `Can't load the keybag. tears in rain... Time to die` -> `FATAL KEYBAG ERROR: kb_load` -> reboot -> Halt/Restart Timed Out panic. Fix: ADT `/defaults/no-effaceable-storage` (mkadt.py; `shim/out/sweet-0038hi.adt`, `research/q0038-hi.adt`, QEMU OK) + file `/private/var/keybags/systembag.kb` (0600 root, dir 0700; XML plist {KeyBagKeys: data}). **v3 image** `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392-v3.img` = v2 + that file, fsck OK, SHA256 fa84274c...22df; `ios16-root-20H392-v3.simg` (img2simg: zero blocks become FILL chunks, so a full flash overwrites every block the rw boots changed). Flash: `fastboot -S 512M flash userdata ios16-root-20H392-v3.simg`, then boot `shim/out/shim-boot-0038e.img` (0038 + sweet-0038hi.adt + ufsrw=1 rootrw=1).
- **0038 AppleKeyStore (CI 38938744130 PASSED -> `xnu/out-0038`; QEMU msgbuf: `SWEET AKS: AppleKeyStore registered (no passcode, unlocked)`; phone image `shim/out/shim-boot-0038w.img` booted 17:38:10 UTC, `research/boot0038w.log`, photo pending).** QEMU full kernel log trick (fb.txt is only the last screen): `llvm-nm KERNEL | grep _msgbufp` -> `--hmp "x /1gx ADDR"` gives struct msgbuf address (static, 0xfffffe0007b56678 on 0038) -> `--hmp "x /3gx STRUCT"` gives bufc (3rd quad) -> `--hmp "memsave BUFC 0x20000 \"FILE\""` (quote the file name), `tr -d "\0" < FILE`. Same inputs give the same addresses. Boot 0037w 17:08:35 UTC, photo IMG_20261016_191052: bindfs fixed mount; mount-phase-1/2 pass; `cc_fips_test` boot task: all corecrypto FIPS POST tests PASSED in userspace; then keybag boot task `keybagd --init`: `MKB_INIT: FATAL KEYBAG ERROR: failed to load system bag`, `Could not get options entry from the device tree` (x2, IODeviceTree:/options = NVRAM, non-fatal), `REBOOTING INTO RECOVERY MODE` -> reboot -> panic `Halt/Restart Timed Out @IOPlatformExpert.cpp:884` (no restart path on SWEET).
  - keybagd (static libaks): load_devicebag (0x100012c30) calls aks_get_system (sel 14, 0-1 scalar in, 1 out) and loads /private/var/keybags/systembag.kb only if the result is 0xe00002f0 (NotFound); any other error -> fatal; SUCCESS -> skip the file (userspace-reboot path). systembag.kb is a plist {KeyBagKeys}; decrypted with effaceable storage unless IODeviceTree:/defaults has `no-effaceable-storage`. Image has no /private/var/keybags. has_data_protection: statfs of /private/var; no cprotect on our HFS -> device-bag volume mapping skipped.
  - libaks connection: IORegistryEntryFromPath / IOServiceMatching("AppleKeyStore"), IOServiceOpen type 0, then selector 0 (no args) must succeed.
  - **AppleKeyStore selector map (iOS 16.7 AppleKeyStore.framework, via `ipsw dyld disass`):** 0 open, 2 create_bag, 3 save_bag, 4 unload_bag, 5 set_system_with_passcode, 6 load_bag, 7 get_lock_state (1 in, 1 out; bit 2 = unlocked since boot), 9 unlock_device, 10 wrap_key, 11 unwrap_key, 12 unlock_bag/test_stashed_kek, 13 lock_bag, 14 get_system, 15 change_secret_se, 16 internal_state, 17 get_device_state (1 in, struct out <=4K: DER SET of SEQUENCE{UTF8 key, INTEGER}: ss state, sls lock_state (MKBGetDeviceLockState returns it), sb backoff, sbo, sfa failed attempts, sfao, sgs generation, sas assertions, sgpe grace, srcd countdown, sr reserved), 18 recover_with_escrow_bag, 19 obliterate_class_d, 20 drain_backup_keys, 21/22 set/clear_backup_bag, 23 get_bag_uuid, 24 rewrap_key_for_backup, 26/27 assert_hold/drop, 30/31 set/get_configuration, 33-37 stash, 38 auth_token_create, 40 generation, 41 fdr_hmac_data, 42 verify_password, 43 _aks_operation, 44 remote_session, 49/50 signing keys, 51/53/54 stash enable/persist/escrow, 55 unload_session_bags, 57/58 remote peer, 59-62 smartcard, 63 migrate_s_key, 65 set_keybag_for_volume_with_cookie_persona, 66/67 sync bags, 68 copy_volume_cookie_persona, 69-73 se_*, 74-79/84/85/99 fv_* (FileVault/VEK), 80/81 absinthe, 82 make_public_backup_bag, 83 drop_auxiliary_auth, 86 kext get/set options, 87 invalidate_bag, 88-91/94/95/106/107 se_*, 92 lower_iteration_count, 93 get_internal_info, 96-98/117 keybag_persona create/list/delete, 100/101 assert promote/consume, 102/103 notify_state set/is_set, 104 fairplay, 105 change_secret_epilogue, 108 delete_xart_leak, 110-113 backup volume, 114 sealed_hashes_set, 115 prewarm_sps, 118-128 AKSIdentity*/AKSGetLastUser.
  - Patch **0038**: `iokit/Kernel/arm/SweetKeyStore.cpp` (class AppleKeyStore on IOResources, IOUserClientClass AppleKeyStoreUserClient; personality in KernelConfigTables.cpp): 0/4/5/9/12/13/26/27/55/102 success, 14 -> handle 0, 7 -> 0x4, 17 -> DER state (ss 4, sls 0), others kIOReturnUnsupported; logs `SWEET AKS: <proc> sel N arg0 in a/b out c/d -> ret` for every call.
  - Tools: shared cache copied to `research/dsc/` (git-ignored; ipsw needs a writable dir for its .a2s symbol cache); `ipsw dyld disass research/dsc/dyld_shared_cache_arm64 --image AppleKeyStore|MobileKeyBag`; scratchpad `annot2.py BIN DIS FIXUPS` annotates llvm-objdump output with strings and import names (`ipsw macho info --fixups`).
- **0037 bindfs (phone boot 0037w pending photo).** Boot 0036mw 16:57:47 UTC, photo IMG_20261016_190102: WRITABLE ROOT WORKS: `/dev/ufsroot0 on / (hfs, local, noatime)` after mount_hfs update (GetMasterBlock EBUSY harmless), coredump of mount written to /cores (rw). Then `mount: failed to mount /private/preboot/5CBE3601.../usr/standalone/firmware -> ...: Operation not supported by device (19)` -> exit 74 -> launchd panic `mount[2] exited`. Cause: the macOS-derived config had nullfs but no bindfs (ENODEV = unknown fs type). Caller passes env 0 -> bind not required, ENOENT (missing source dir) tolerated. Patch **0037** adds `bindfs` to FILESYS_BASE in MASTER.arm64.sweet; CI `38936550483` -> `xnu/out-0037` (bindfs_vfsops present; QEMU probe regression OK). Image `shim/out/shim-boot-0037w.img` (0037 + sweet-0036hi.adt + ufsrw=1 rootrw=1) booted 17:08:35 UTC (`research/boot0037w.log`). NOTE: userdata has now been modified by rw boots; it no longer equals the v2 image, so sparsediff with v2 as OLD is not safe any more (full reflash or a new baseline needed).
- **0036 phone: launchd boot tasks run; mount -P 1 needs /chosen/boot-manifest-hash.** Boot 0036hr 16:15:32 UTC, photo IMG_20261016_185236: platform check passes; fsck boot task runs (`fsck: not booting main or diagnostic OS. Skipping fsck on OS container`); mount-phase-1: `failed to get filesystem info` x2 (no IODeviceTree:/filesystems/fstab, non-fatal), `mount: data volume missing, but not required in env: 0`, mount_hfs update of /: `GetMasterBlock: Error 16 opening /dev/ufsroot0` (EBUSY, mounted block dev, non-fatal) then mount() EROFS (read-only boot) -> `mount: / failed with 1`; then `failed to get boot-manifest-hash` -> errx exit 66 -> launchd panic `mount[3] exited`. /sbin/mount: fn 0x100005f90 reads IODeviceTree:/chosen boot-manifest-hash (hex), bindfs-mounts /private/preboot/<HEX>/usr/standalone/firmware (ENOENT tolerated unless required). `tools/mkadt.py` now adds `boot-manifest-hash` = SHA-384("sweet boot manifest") (5CBE3601...5205). ADTs `shim/out/sweet-0036hi.adt`, `research/q0036-hi.adt` (QEMU probe OK, csops 0x26000001). Image `shim/out/shim-boot-0036mw.img` (0036 + new ADT + ufsrw=1 rootrw=1), booted 16:57:47 UTC (`research/boot0036mw.log`): FIRST WRITABLE BOOT of userdata (restore source: v2 image on SSD).
- **0036 CS_SIGNED (phone boot 0036hr pending photo).** Phone boot 0035hr 2026-10-16 15:57:02 UTC (`research/boot0035hr.log`, photo IMG_20261016_180249): highmem works on hardware; shared cache maps (trust-cache warnings only), Apple launchd runs (`Darwin Bootstrapper Version 7.0.0`, `entering ondemand mode`), starts boot task fsck, then userspace panic `boot task is not a platform binary (fsck, /sbin/fsck)`. launchd+0x3fea0: `csops(pid, CS_OPS_STATUS)` must have bit 0x04000000. Cause: nothing set CS_SIGNED (AMFI does it in vnode_check_signature), so csproc_get_blob() returns NULL for every process and csops never reports CS_PLATFORM_BINARY (also breaks per-process cdhash/entitlement queries). QEMU probe init (`csops` status printer, scratchpad csq/) on 0035: `0x02000001`; patch **0036** (`*cs_flags |= CS_SIGNED` in the SWEET AMFI hook), CI `38929635791` -> `xnu/out-0036`: `0x26000001`. Images `shim/out/shim-boot-0036hr.img` / `-0036hw.img` (same cmdlines as 0035). 0036hr booted 16:15:32 UTC (`research/boot0036hr.log`). Next launchd boot tasks (embedded __config plist): fsck -qL and mount -P 1/2 (RequireSuccess); no /etc/fstab on the image.
- **0035 ENTITLEMENTS + PLATFORM BINARIES (QEMU verified).** `xnu/patches/0035-sweet-amfi-entitlements-platform-binaries.patch`: new `iokit/Kernel/arm/SweetEntitlements.cpp` (OSObject subclass: OSDictionary from OSUnserializeXML of the signature's XML entitlements + original XML for CS_OPS_ENTITLEMENTS_BLOB); `bsd/kern/sweet_amfi.c` answers queryEntitlementBoolean/String(+WithProc, string also matches array members), copyEntitlementAsOSObject(+WithProc, retained), asdict (retained), get_xml (kalloc_data copy); built-in MAC policy "SWEET AMFI" (registered from bsd_init before vfs/exec) with mpo_vnode_check_signature: every signed binary on the MNT_ROOTFS mount gets CS_PLATFORM_BINARY (stand-in for AMFI's static trust cache: iOS system binaries are ad-hoc, cd_flags 0x2, platform byte 0), and attaches entitlements ONLY for the writable copy (cs_blob != csb_ro_addr; revalidation passes the RO blob). LESSON: first version attached in adjustContextWithoutMonitor -> QEMU `unable to adjust OSEntitlements context without monitor: 53` because ubc_cs_convert_to_multilevel_hash (4K-page signatures on 16K kernel) sets csb_entitlements_blob = NULL; ALL iOS 16 binaries (launchd, backboardd, SpringBoard) use 4K code pages, so this would have broken launchd on the phone. Boot-arg `sweet_amfi_debug=1` logs `SWEET AMFI: <ident>: N entitlements (test: ...)`. `tools/mkinit.py OBJ OUT [ENTS.plist]` adds an XML entitlements blob (special slot -5; default output byte-identical). QEMU `research/q0035-ent` (RAM disk `research/root-hfs-ent.img`, init with 3 test entitlements, highmem): `org.sweet.init: 3 entitlements (test: bool 1 string 1 array 1)` then init PID 1. MAC policies loaded: 0034 = 1, 0035 = 2 (QMP `mac_policy_list`). CI `38909807230` -> `xnu/out-0035`. Phone images: `shim/out/shim-boot-0035hr.img` (highmem, ro), `-0035hw.img` (highmem, +ufsrw=1 rootrw=1), `-0035r.img` (low mem fallback).
- **PHONE TEST ORDER (updated):** 0035hr -> if instant reset, 0035r -> then 0035hw.

- **HIGHMEM: XNU in the upper DDR bank, ~3.95 GiB (was 1.2 GiB).** Live FDT memory = <0x80000000 2G> + <0x1_00000000 0xfcc00000>; all fixed reserved-memory carve-outs are in the low bank (highest: ramdump_fb 0xaf000000, rmtfs ~0xfde01000), dynamic pools have alloc-ranges <= 0xffffffff, UFS node has no `iommus` (Linux DMAs anywhere). `tools/mkadt.py --highmem` sets /chosen dram-base 0x100000000 dram-size 0xfcc00000; `tools/mkpayload.py` now takes phys_base/mem_size from the ADT (default payloads byte-identical, verified); `tools/qemu-sweet.py` sizes -m from the payload (8G for highmem). Patch **0034** (`0034-sweet-ufs-dma-above-4g.patch`): UFS refuses DMA memory above 4G without UFSHCI CAP.64AS (bit 24), logs `DMA at 0x...`. CI `38905889883` success -> `xnu/out-0034`. **QEMU verified** (`research/q0034-hi`, ADT `research/q0034-hi.adt` --qemu --highmem, HFS RAM disk): phys_base 0x100000000, init PID 1 heartbeat, no panic; `max_mem` = `mem_size` = 0xfcc00000 read via QMP (`research/q0034-hi-mem`). Phone images: `shim/out/shim-boot-0034hr.img` (read-only) / `-0034hw.img` (+ufsrw=1 rootrw=1), ADT `shim/out/sweet-0034hi.adt` (asmb SIP + sweet-ufs + highmem). PHONE RISK: unknown runtime TZ/XPU protection in the upper bank would show as an instant reset; fall back to 0033r/w. Watchdog ruled out for the overnight reset: msm-watchdog bark is 20 s (qcom,bark-time 0x4e20) yet panic screens stay up for many minutes.

- **Offline research 2026-10-16 (user away, phone unavailable). Images rebuilt** `shim/out/shim-boot-0033r.img` / `-0033w.img` now also carry `wdt_test=no_user_checkin`. NEXT ON PHONE: boot 0033r (expect past in6_nigroup), then 0033w (first writes: rw root fixes HFS link-chain bits itself and gives /var for launchd sockets /var/run/syslog, /var/run/lockdown.sock).
- **launchd.plist** (`/System/Library/xpc/launchd.plist`, compiled; 532 daemons, 66 RunAtLoad/KeepAlive, list in scratchpad `early-daemons.txt`). `_PanicOnCrash` daemons: containermanagerd/usermanagerd (InternalOnly), lockdownd/remoted/trustd/remotepairingdeviced (AutomationOnly), **watchdogd unconditional** (KeepAlive SuccessfulExit=false). watchdogd needs IOKit `IOWatchdog` kext service; if absent it exits only when `kern.hv_vmm_present` (ADT `/defaults/vmm-present`, hvg_sysctl.c) or with boot-arg `wdt_test=no_user_checkin` ("detected testing boot-args to not run, exiting"; reads kern.bootargs). Using the boot-arg (vmm-present would change many daemons; keep as an option).
- **GUI path research (QuartzCore in the shared cache, `ipsw dyld str CACHE STR`, ~10 s/search):** CA::WindowServer has IOMFBServer/IOMFBDisplay (Apple DCP/IOMobileFramebuffer), AppleCLCDDisplay, AppleRGBOutDisplay, **VirtualServer/VirtualDisplay** and **MemorySurface**, EAGLServer. Renderers: CA::OGL::MetalContext, GLContext and a **CPU software rasterizer CA::OGL::SW** (samplers/blend modes; "image is too large for software renderer"). Env knobs: `CA_ENABLE_OGL`, `CA_DISPLAY_TYPE`, `CA_FORCE_LOCAL_SERVER` (249 CA_* vars). Hypothesis (unverified): backboardd's render server could run a VirtualServer/MemorySurface with the SW renderer and we copy the surface to the ABL framebuffer -> needs disassembly of CA::WindowServer server creation. Expected other GUI walls: IOSurface (closed-source kext; needs a reimplementation), IOMobileFramebuffer user client, IOHID touch events, AppleKeyStore/keybag (SEP) for lock state, MobileGestalt answers (AppleCLCD etc.).

- **0032r RESULT (boot 05:07:50 UTC, `research/boot0032r.log`, photo IMG_20261016_071200): SHARED CACHE MAPPED, LAUNCHD RUNS.** With SIP relaxed (ADT asmb) the `not in trust cache` lines are only warnings for every subcache (.31 ... .42.dyldlinkedit); no SIP rejection; libSystem loads; launchd configures networking (`skip attaching fsw to lo0 using legacy TX model`) -> kernel data abort far 0x28 in `SHA1Init` (symbolized as sha1_init) from `in6_nigroup` (IPv6 on lo0): g_crypto_funcs NULL. Kernel addresses are unslid: `~/swift/usr/bin/llvm-symbolizer --obj=KERNEL ADDR` works directly.
- **0032** BearSSL SHA-1 (`0032-sweet-bearssl-sha1.patch`), **0033** BearSSL SHA-384/512 (`0033-sweet-bearssl-sha384-sha512.patch`, BearSSL ctx stored in SHA512_CTX, static-asserted to fit; ubc_subr.c uses SHA-384 for code directories). `0020-stage-bearssl.sh` now also stages hash/sha1.c, hash/sha2big.c, codec/{dec,enc}{32,64}be.c. CI `38854909053` success (0032-only run `38854802073` superseded). Kernel `xnu/out-0033` (SHA1Init -> _br_sha1_init verified by disassembly; nm symbols have a leading underscore). Images (ADT sweet-0032): `shim/out/shim-boot-0033r.img` (read-only), `shim-boot-0033w.img` (+ufsrw=1 rootrw=1). Still NULL g_crypto_funcs users: des, chacha20poly1305, rsa, aesxts, rand, flow_divert.
- `research/check-patch-order.py` now skips patches touching CI-staged sweet_hfs sources (0031) instead of stopping.

- **0031r RESULT (boot 05:03:52 UTC 2026-10-16, `research/boot0031r.log`, photo IMG_20261016_070508): SHARED CACHE FOUND.** dyld now opens `dyld_shared_cache_arm64` (v2 image hard links), kernel refuses to map it: `shared_region: ... map(...'dyld_shared_cache_arm64'): not in trust cache` -> `vnode is not SIP-protected` (vm_unix.c: macOS arm64 path needs trust cache, else root-owned + SF_RESTRICTED unless CSR_ALLOW_UNRESTRICTED_FS) -> `dyld cache '(null)' not loaded: syscall to map cache into shared region failed` -> libSystem not loaded -> coredump to /cores fails error 30 (EROFS) -> panic initproc failed -> "MACH Reboot" (spins; screen kept). Lots of `hfs: set hardlink bit on vol=iOSRoot cnid=... linkid=...` spam (Linux-made hard links lack the link-chain bit; read-only mount cannot persist the fix). FIX: ADT `/chosen/asmb` with `lp-sip0`=0x6f (u64; incl. CSR_ALLOW_UNRESTRICTED_FS) and `lp-sip1`=1 (unauthenticated root), `tools/mkadt.py` -> `shim/out/sweet-0032.adt`. Images with kernel 0031: `shim/out/shim-boot-0032r.img` (read-only) and `shim-boot-0032w.img` (+ufsrw=1 rootrw=1).

- **2026-10-16 morning:** userdata now = **v2** image (`diff-v1-v2.simg` flashed 21:06:50 UTC 2026-10-15, OKAY, `research/flash-userdata-diff-v2.log`); future diffs use `ios16-root-20H392-v2.img` as OLD. Booted `shim-boot-0029k.img` (ignition_level=1) right after (`research/boot0029k-v2.log`); **no photo** (user asleep). Next morning the phone was in PixelOS recovery = some hardware reset (ABL then booted Android, which cannot use userdata). OBSERVATION: our kernel cannot reset the SoC itself (`PE_halt_restart` is never set; reboot/halt print "MACH Reboot"/"CPU halted" and spin), so the reset came from outside XNU: Qualcomm watchdog or a TZ/XPU violation. Unknown which; re-boot 0029k and watch/video until the reset. Do NOT tap factory reset/format data in recovery (would wipe the iOS image).
- **0030** (`xnu/patches/0030-sweet-ufs-writes.patch`, CI `38852655542`): UFS WRITE(10) + read-modify-write for partial 4 KiB blocks + SYNCHRONIZE CACHE (DKIOCSYNCHRONIZE), only with boot-arg `ufsrw=1`; `ufs_write_blocks` re-checks partition bounds before every write (only place data goes out).
- **0031** (`xnu/patches/0031-sweet-read-write-root.patch`, CI `38852837176`): boot-arg `rootrw=1` clears MNT_RDONLY before the root mount (no data volume on sweet: /private/var is on the root; image has no /etc/fstab); Apple HFS accepts a dirty non-journaled ROOT read-write on SWEET (logs "mounting dirty non-journaled root read-write"). Later: journaled HFS for crash safety. Kernel `xnu/out-0031` (CI `38852837176` success, 5m31s; 0030 run cancelled by the newer push). Boot images (phone ADT `sweet-0028.adt`, ramdisk byte-matched): `shim/out/shim-boot-0031r.img` = 0029k args (read-only, ignition_level=1) and `shim/out/shim-boot-0031w.img` = same + `ufsrw=1 rootrw=1`. PLAN: boot 0031r first and film until the reset (diagnose overnight reset), then 0031w (first ever writes to userdata; v2 image on the SSD is the restore source). `research/check-patch-order.py` cannot check 0031 (staged sweet_hfs files are not in its index); CI stage scripts run first, so CI is the check.

- **ignition_level=1 result** (boot 21:01:39 UTC, `research/boot0029k.log`, photo IMG_20261015_230308): preboot/cryptex stages skipped (need >= 2/3), `dylib_cache: finding shared cache on system volume: ignition level = 1, search root fd = 4, subpath = System/Library/Caches/com.apple.dyld/` -> not found -> `ignition boot failed: 19` -> no shared cache -> libSystem not loaded. FIX IN PROGRESS: image v2 = copy of the flashed image + `/System/Library/Caches/com.apple.dyld/` with HARD LINKS to the 44 cryptex cache files (no extra space; avoids symlink-following doubts), then `tools/sparsediff.py ios16-root-20H392.img ios16-root-20H392-v2.img diff.simg` and flash only the diff. Boot with `ignition_level=1` (shim-boot-0029k.img).
- **ignition_level=0 result** (boot 20:58:07 UTC, `research/boot0029j.log`, photo IMG_20261015_230037): all stages skipped as "ignition level insufficient" (hello/preboot/cryptex1 sniff >= 2, select os cryptex path/graft >= 3, **dyld_cache >= 1**), `ignition boot failed: 89`, "ignition partially disabled", then same `Library not loaded: /usr/lib/libSystem.B.dylib (no such file, no dyld cache)`. => dyld gets the shared cache directory from ignition's dyld_cache stage. Next: `ignition_level=1` (`shim/out/shim-boot-0029k.img`) to skip preboot/cryptex stages but run dyld_cache; its log "finding shared cache on %s ... subpath = %s" will show where it searches. If it searches rootfs /System/Library/Caches/com.apple.dyld, add a symlink there (image rebuild; consider a diff-only sparse flash tool to avoid rewriting 12 GB).
- **APPLE dyld/launchd RUNNING (libignition) with `unentitled_ios_sim_launch=1`** (boot 20:53:24 UTC, `research/boot0029i.log`, photo IMG_20261015_225617): kernel prints "Allowing spawn of iOS binary ... boot-arg set to true"; `shared_region: ... check_np ... vm_shared_region_start_address() failed` (no region yet, normal); dyld's built-in **libignition** (Darwin Ignition Sequence 1.0.0, libignition-51~1974; prints rd=ufsroot0, hardware target sweet, ignition level 0x5, platform 0x2, boot spec local, 7 stages): `hello from launchd.1` -> `preboot: mounting preboot` -> `failed to lookup preboot: 25` (ENOTTY: looks for a separate Preboot volume by role) -> ignition fails -> dyld `Library not loaded: /usr/lib/libSystem.B.dylib ... (no such file, no dyld cache)` -> launchd exit -> panic initproc failed. dyld boot-args found via strings: `ignition_level`, `ignition_force_dylib_root` (forced rootfs/livefs/cryptex fallback), `ignition_halt_after`, `ignition_live_app_graft`; dyld cache search paths include /System/Cryptexes/OS, /System/Volumes/Preboot/Cryptexes/OS/, /private/preboot/Cryptexes/OS/ (present in our image). Next try `ignition_level=0` (`shim/out/shim-boot-0029j.img`).
- **APPLE launchd EXECUTED FROM UFS (2026-10-15).** Flashed iOS image: `img2simg` -> `ios16-root-20H392.simg` (12.1 GB) then `fastboot -S 512M flash userdata ...simg` (24 chunks, 307 s, `research/flash-userdata-ios16.log`; a raw-image flash was killed by earlyoom at 2.6 GB RSS - always flash the sparse image). ABL fastboot hung on getvar after the flash; power+vol-down fixed it. Boot 0029u 20:49:04 UTC (`research/boot0029u-ios16.log`), photo IMG_20261015_225134: `hfs: mounted iOSRoot` -> load_init_program /sbin/launchd -> panic `unexpected SIGKILL of launchd (CS_KILLED) with reason -- namespace 9 code 0xe` = OS_REASON_EXEC / EXEC_EXIT_REASON_WRONG_PLATFORM: our kernel is XNU_TARGET_OS_OSX, iOS-platform binaries are "alien" and refused unless spawn attr platform set or DEVELOPMENT TUNABLE `unentitled_ios_sim_launch`. Next try: same kernel, cmdline + `unentitled_ios_sim_launch=1` (`shim/out/shim-boot-0029i.img`). LONGER TERM: macOS-config kernel marks iOS maps alien (vm_map_mark_alien) and differs from iOS in many policies; an iPhoneOS-config kernel build may eventually be needed.
- **iOS 16 ROOT IMAGE BUILT:** `/run/media/dipa/android/ios-sweet-ipsw/ios16-root-20H392.img` (16 GiB case-sensitive HFS+, label iOSRoot, 12 GB used, fsck OK after `fsck.hfsplus -y` rewrote 32 non-ASCII localized WorkflowKit Shortcut names Linux decomposes differently). Built by `tools/mkiosroot.sh OS.dmg SYSTEMOS.dmg APPOS.dmg OUT.img [SIZE]` (needs sudo; apfs-fuse as root; OS dmg is UDIF -> link must end .dmg). Contents: iPhone X 20H392 OS root + SystemOS cryptex at /private/preboot/Cryptexes/OS (so /System/Cryptexes/OS -> cache, 44 files, dyld_v1 arm64) + AppOS at .../App. /sbin/launchd and /usr/lib/dyld root:wheel 0755. NEXT: (confirm) `fastboot flash userdata ios16-root-20H392.img` (auto-sparse), boot 0029u (rd=ufsroot0) -> Apple launchd attempt.
- **MILESTONE ON HARDWARE: BOOT FROM INTERNAL FLASH.** 0029 CI `38797924912` PASSED, `xnu/out-0029` SHA256 `a68bc847...2a37`. Image `shim/out/shim-boot-0029u.img` (payload-0029u = 0029 kernel + `shim/out/sweet-0028.adt` + `rd=ufsroot0`, NO RAM disk). Boots 20:01:34 and 20:12:37 UTC (`research/boot0029u*.log`), photo IMG_20261015_221403: `SWEET UFS: "userdata" on LUN 0: first block 0x2b8c00, 109643 MiB, read-only` -> `BSD root: ufsroot0, major 1, minor 0` -> `hfs: mounted SweetRoot on device b(1, 0)` -> `SWEET: root volume is not authenticated (error 25); continuing unsealed` -> `load_init_program ... /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` -> heartbeat (ran for minutes unattended). userdata currently holds the 8 MB `research/root-hfs.img`. NEXT: build a multi-GB HFS+ image with the iOS 16 (iPhone X 20H392) userland (OS rootfs + SystemOS cryptex contents incl. dyld shared cache at /System/Library/Caches/com.apple.dyld; preserve modes/owners/symlinks; decompress LZBITMAP via apfs-fuse), flash it to userdata (sparse, needs user OK), then try Apple's dyld/launchd. Driver is read-only (root mounts RDONLY), fine for first launchd attempts.
- **userdata FLASHED with the 8 MB HFS test volume** (user said "flash it", 2026-10-15 19:53:17 UTC, `research/flash-userdata-hfs-test.log`: `fastboot flash userdata research/root-hfs.img` OKAY; pre-checks: one sweet device, partition-size:userdata 0x1AC4BFB000, partition-type f2fs, image fsck OK, SHA256 3626ea69...). Android userdata is now destroyed (expected/approved). Boot 0028u at 19:53:20 (`research/boot0028u-hfs.log`), photo IMG_20261015_215541: `BSD root: ufsroot0` -> **`hfs: mounted SweetRoot on device b(1, 0)` from internal UFS** -> panic `rootvp not authenticated after mounting @bsd_init.c:931` (arm64 macOS-config requires FSIOC_KERNEL_ROOTAUTH sealed root for non-ramdisk roots). Patch **0029** (`dd1c284`): SWEET logs `SWEET: root volume is not authenticated (error N); continuing unsealed` instead of panicking (Apple configs keep the panic; pivot_root still requires auth). CI **`38797924912`** running. Next: download out-0029, phone image with sweet-0028.adt + rd=ufsroot0 (no RAM disk), boot -> expect init from UFS.
- **UFS ROOT DRIVER VERIFIED ON HARDWARE (read-only).** 0028 CI `38796139570` PASSED, `xnu/out-0028` SHA256 `8b981640...9da6`; QEMU HFS RAM-disk regression `research/q0028-hfs` still runs init. Phone boot 2026-10-15 19:50:24 UTC (`research/boot0028u.log`, image `shim/out/shim-boot-0028u.img`, phone ADT `shim/out/sweet-0028.adt` with /sweet-ufs, NO RAM disk, `rd=ufsroot0`), photos IMG_20261015_215151/215220: `SWEET UFS: "userdata" on LUN 0: first block 0x2b8c00, 109643 MiB, read-only` -> `BSD root: ufsroot0, major 1, minor 0` -> `hfs_ValidateHFSPlusVolumeHeader: unknown Volume Signature : f188` (Android-encrypted data, as expected) -> `cannot mount root, errno = 19`, kernel retries mountroot (no panic). Nothing written to flash. NEXT (destructive, needs user confirmation right before): `fastboot flash userdata research/root-hfs.img` (8 MB HFS with test init) then boot rd=ufsroot0 -> expect init from internal flash.
- **PATCH 0028 (`33aceac`): XNU read-only UFS root device**, CI **`38796139570`** running (next artifacts xnu/out-0028, research/bt29, run29.log). `bsd/dev/sweet_ufs.c`: reuses ABL's UFSHCI state (like the shim probe), takes over UTRL at a kmem_alloc_contig region (DMA layout: UTRL 0x0, UCD 0x1000, 1 MiB bounce 0x4000), verifies UTRLBA readback before any doorbell, IE=0 polled, one SCSI cmd at a time on LUN0 (TUR x3, READ(10) via bounce, PRDT 256 KiB chunks), flush_dcache64 by PA around each command (host not dma-coherent per DT), finds GPT partition by name (`ufsroot=` boot-arg, default `userdata`), exposes `/dev/ufsroot0`/`rufsroot0` (512-byte logical sectors, physical 4 KiB, DKIOC* ioctls), refuses writes (EROFS). IOKitBSDInit: `rd=ufsroot0` -> sweet_ufs_rootdev() (lazy init) else panic. ADT: `tools/mkadt.py` adds `/sweet-ufs` reg <0x1d84000 0x3000> for the PHONE only (not --qemu). Local compile OK, imports resolve. Sandbox research/bt28 (pre0028 originals). FIRST PHONE TEST PLAN (non-destructive): boot 0028 with phone ADT + `rd=ufsroot0` and NO RAM disk: expect `SWEET UFS: "userdata" on LUN 0: first block 0x2b8c00, 109643 MiB` + `BSD root: ufsroot0`, then root mount failure (userdata is still Android-encrypted) -> panic. That validates the driver before flashing an HFS image into userdata (needs explicit user confirmation at that time).
- **SUPERSEDES the 64 GiB iosroot GPT plan: user said "u can delete android" (2026-10-15).** Use the existing `userdata` partition (LUN0 sda34, 4K LBA 0x2B8C00, 0x1AC4B MiB ~107 GiB) directly as the iOS root: NO GPT changes. Keep bootloaders, recovery (OrangeFox), modem/persist/fsg/modemst untouched. Write the HFS image later with `fastboot flash userdata` (sparse, auto-split under the 768 MiB limit). Android will no longer boot normally (expected; reinstallable). Order: XNU UFS driver first, read-only against the current GPT; flash only once it can locate userdata. Nothing erased yet.
- **DECIDED (user, 2026-10-15): 64 GiB `iosroot` on LUN0 (sda), taken from userdata (wipes Android user data; Android/super kept).** Planned GPT (4K LBAs): userdata 0x2B8C00..0xD7D6FF (~43 GiB, keep type/unique GUIDs and attributes); iosroot 0xD7D700..0x1D7D6FF (0x1000000 blocks = 64 GiB, 1 MiB aligned); backup GPT area unchanged. Procedure: user backs up phone data -> boot OrangeFox recovery (adb) -> back up GPT (sgdisk --backup + raw dd of LBA 0-5 and last 6 blocks) to research/ -> sgdisk edit -> Format Data -> verify Android boots to setup. NOT EXECUTED YET.
- **INTERNAL UFS WORKS FROM THE SHIM (read-only), user authorized internal-UFS approach incl. flashing (2026-10-15, "i allow everything").** Shim probe `shim/ufs.c` (commit `12ed3ed` + filter): ufshc@1d84000 is UFSHCI 2.1 (ver 0x210, cap 0x1587031F, 32 slots), ABL leaves HCE=1, HCS=0x10F (device present, lists ready, UIC ready); probe takes over UTRL at its own buffer (verifies UTRLBA readback before any doorbell), TEST UNIT READY/READ CAPACITY/READ(10) all succeed. LUN0 = 0x1D7D800 x 4 KiB (~126.6 GB), valid GPT (64 entries at LBA 2). Photos IMG_20261015_212916/213325/213429. Big LUN0 partitions (start in 4K LBAs / MiB): super 0xCA00/0x2200 (8.5 GiB), logdump 0x22CA00/64, minidump 0x230A00/128, rawdump 0x238A00/128, recovery 0x240C00/128, cache 0x248C00/384 ext4, exaid 0x260C00/384, cust 0x278C00/1024 ext4, **userdata 0x2B8C00/0x1AC4B MiB (~107 GiB), fs unreadable = encrypted (metadata encryption)**. cache..cust contiguous = only 1.75 GiB (too small for iOS ~10+ GiB). Plan needing user consent: shrink userdata in GPT (wipes Android data) and add an `iosroot` partition at the end of LUN0. LUNs 1-5 not listed yet (sdb..sdf backed up in backup/lun).
- **fastboot limit measured (2026-10-15, read-only getvar):** `max-download-size: 805306368` (768 MiB); `max-fetch-size` unsupported; `is-userspace: no` (ABL fastboot). A `fastboot boot` image (shim+kernel+RAM disk) must be < 768 MiB, so the 2.5 GiB iOS shared cache cannot ride in the boot RAM disk even if XNU gets all RAM. Real userland needs storage access (UFS driver, or USB host) or a much smaller cache. Unlocking full RAM is still needed later (GUI).
- **iOS 16 USERLAND SOURCE (Claude, 2026-10-15).** Chose **iPhone X (iPhone10,3/10,6, D22/D221AP)** iOS **16.7.16 (20H392)** over iPhone 8: same A11 (no PAC -> plain arm64, runs on Kryo 470/ARMv8.2), last iOS for A11; X userland is home-button-less and tall-screen (1125x2436 vs sweet 1080x2400), better fit for later GUI. Note the X has its OWN SystemOS cryptex (different digest from iPhone 8's). IPSW URL in `research/ipsw-x/URL.txt` (+ BuildManifest). Images on the user's external SSD (NOT in git, do not format that disk: it holds the user's photos): `/run/media/dipa/android/ios-sweet-ipsw/iPhone10,3_16.7.16_20H392/` — `087-86593-047.dmg` = Cryptex1,SystemOS (2,743,074,816 B), `087-86698-044.dmg` = OS rootfs (4,730,814,044 B), both zip CRC-32 verified, plus Firmware/*.root_hash/.trustcache/.mtree. AppOS cryptex is 087-86715-047.dmg (10 MB, same as iPhone 8).
  - Images are raw APFS; files use LZBITMAP (decmpfs type 14). 7z cannot decode. Tools: `ipsw` 3.1.738 (AUR ipsw-bin, user-approved) needs apfs-fuse on Linux; **apfs-fuse** built in user space (system cmake broken: cmake 4.4.4 wants libjsoncpp.so.27, jsoncpp 1.9.6 installed = partial upgrade, NOT fixed) with pip cmake + `-DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_CXX_FLAGS="-include cstdint"`, installed to `~/.local/bin/apfs-fuse` (+apfs-dump-quick). Mount via a comma-free symlink (apfs-fuse splits options on ',' in `iPhone10,3`; exFAT has no symlinks -> put link elsewhere): `apfs-fuse LINK/087-86698-044.dmg MNT` -> `MNT/root/...`; unmount `fusermount3 -u MNT`.
  - Verified from headers: `dyld_shared_cache_arm64` magic `dyld_v1   arm64`; `/sbin/launchd`, `/usr/lib/dyld` = cputype 0x100000c subtype 0 (plain arm64). libSystem exists only inside the cache.
  - **BLOCKER for real userland via RAM disk:** shared cache = 3.10 GiB in 44 files (~2.5 GiB without the 592 MB `.symbols`), but the kernel manages only 1.20 GiB (0xb0000000..0xfd000000). Options: (A) give XNU the phone's full ~6 GB (banks 0x80000000+2G and 0x100000000+0xfcc00000, carve-out holes need pmap support) AND check fastboot max-download-size for a multi-GB boot image; (B) storage driver (Qualcomm UFS) to read a root from flash (no flashing allowed: would need a file/partition strategy); (C) run against individual dylibs extracted from the cache (uncertain).
- **MILESTONE ON HARDWARE: HFS+ ROOT FILESYSTEM -> PID 1.** Boot 2026-10-15 18:22:12 UTC (`research/boot0027b.log`, image `shim/out/shim-boot-0027b.img`), photo `IMG_20261015_202334.jpg`: `BSD root: md0` -> `hfs: mounted SweetRoot on device b(1, 0)` -> `load_init_program: attempting to load /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` -> repeated `SWEET init: still alive`, no panic. Kernel 0027 (built-in Apple OSS HFS + BearSSL MD5), init with SP alignment fix. NEXT: real iOS 16 userland on the HFS image (dyld, libSystem/dyld shared cache, launchd). Known gaps: entitlements (none granted), SHA-1/SHA-384/512 providers, no storage driver (RAM disk only), root mounted read-only.
- **PHONE HFS ROOT (0027) + SIGBUS ROOT-CAUSED.** Phone boot 2026-10-15 17:49:06 UTC (`research/boot0027.log`, photo `IMG_20261015_200031.jpg`): `hfs: mounted SweetRoot on device b(1, 0)` (HFS works on hardware), init printed its first line, then `pid 1 exited -- exit reason namespace 2 subcode 0xa` = SIGNAL/SIGBUS -> `initproc failed to start` panic. Diagnostic boot 18:08:13 UTC (`research/boot0027d.log`, image `shim/out/shim-boot-0027d.img`, diag init `research/diag-init` from scratch diag-init.S with [a][b][c] markers, `cs_debug=1`; photo `IMG_20261015_201547.jpg`): output `PID [a][b]` then SIGBUS -> fault at first `strb w21,[sp]`; no code-signing messages. Cause: kernel enters a static binary with sp at argc, not necessarily 16-aligned (depends on arg/apple string lengths, differs mockfs vs HFS); EL0 SP alignment check -> EXC_ARM_SP_ALIGN -> SIGBUS (sleh handle_sp_align). QEMU does not enforce SP alignment. NOT a kernel bug: real binaries start in dyld which aligns. Fix `1a8fc15`: sweet-init aligns sp at entry. Rebuilt `research/root-hfs.img`, QEMU `research/q0027-hfs2` OK. Phone image `shim/out/shim-boot-0027b.img` SHA256 `098ba46c...c5c` (payload-0027b, ramdisk match check-0027b) ready, awaiting FASTBOOT. Lesson: Assembly `;` is a comment in Apple arm64 asm (use .macro, not ;-joined #define).
- **HFS ROOT WORKS (QEMU).** 0027 CI `38779441895` PASSED, `xnu/out-0027` SHA256 `a8643886...5f6a`. QEMU `research/q0027-hfs` (RAM disk = `research/root-hfs.img`, rd=md0): `BSD root: md0` -> `hfs: mounted SweetRoot on device b(1, 0)` -> `load_init_program: attempting to load /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` + heartbeat, no panic. Phone image `shim/out/shim-boot-0027.img` (payload-0027 = 0027 kernel + sweet-0021.adt + root-hfs.img + rd=md0, ramdisk byte-match check-0027) ready; awaiting FASTBOOT for phone test.
- **HFS ROOT WORK (Claude), patches 0026-0027.**
  - 0026 (`f0e990c` + link fix `64c96f4`): Apple OSS **hfs-627.100.6** (commit `31d5ec238dfab485e78a9a30b8b92d13e8914f03`, paired with xnu-8796.141.3 in macos-135 release.json) staged by `xnu/patches/0026-stage-hfs.sh` into `bsd/sweet_hfs` (core + hfs_encodings; AppleKeyStore include/key prototypes guarded by CONFIG_PROTECT; SDK TargetConditionals copied). New config option `sweet_hfs` (MASTER + MASTER.arm64.sweet); 40 `optional sweet_hfs` files; Makefile.template foreach adds `_CFLAGS_ADD = -include sweet_hfs_compat.h -I...` (MUST come after kernel -D flags; compat undefs BSD/XNU_KERNEL_PRIVATE and the CONFIG_* HFS tests so kext-config.h decides: macOS profile, no content protection). `sweet_hfs_iokit.c` replaces hfs_iokit.cpp/hfs_encodings_kext.cpp: `sweet_hfs_register()` called in bsd_init after vfsinit (encodings init, vfs_fsadd VFS_TBLCANMOUNTROOT, zones, sysctls); is_ejectable 0, iterate_media none, serial KERN_NOT_SUPPORTED, OSKextGetCurrentLoadTag -> kOSKextInvalidLoadTag (renamed via compat macro). hfs_encodings' own `hfs_allocated` renamed per object (separate kexts on Apple; first CI `38777325964` failed on that duplicate at link). mockfs now validates Mach-O magic (its TODO) so non-Mach-O roots fall through to HFS (new fs entries come AFTER mockfs in vfsconf). CI `38778133720` PASSED, `xnu/out-0026` SHA256 `0b49170c...701a`, prints `SWEET HFS: hfs-627.100.6 registered`.
  - HFS+ image: `research/root-hfs.img` (8 MB, mkfs.hfsplus from AUR hfsprogs installed with user approval; loop-mounted with sudo; /sbin/launchd = research/sweet-init, /dev; fsck.hfsplus OK). QEMU `research/q0026-hfs`: `BSD root: md0` then data abort in MD5Init from hfs_getvoluuid (mount computes volume UUID).
  - 0027 (`14bf2b7`): 0020 stager also copies BearSSL hash/md5.c + codec/dec32le.c/enc32le.c; `corecrypto_md5.c` SWEET branch converts MD5_CTX <-> br_md5_context around br_md5_* calls; wrappers sweet_md5.c/sweet_dec32le.c/sweet_enc32le.c. Host test 40/40 match md5sum. CI **`38779441895`** running.
  - Local tooling: `tools/xnu-cc.py` has `XNU_CC_POST` (flags after logged ones). Sandbox `research/bt28/xnu` = 0025 CI tree + 0026/0027 edits; originals `research/pre0026`, `research/pre0027`. HFS local objects `research/hfs-objs`. Checker entries updated to bt28.
  - SHA-1 / SHA-384/512 still have no provider.
- **MILESTONE ON HARDWARE: USERSPACE PID 1 RUNS ON THE PHONE.** Boot 2026-10-15 17:16:00 UTC (`research/boot0025.log`: send OKAY0.410s, boot OKAY0.135s), image `shim/out/shim-boot-0025.img` SHA256 `9dbfa0b1...89db0`. Photo `IMG_20261015_191733.jpg`: `BSD root: md0` -> `load_init_program: attempting to load /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` -> repeated `SWEET init: still alive` (5 s heartbeat), no panic. Kernel 0025 + mockfs RAM disk + built-in no-entitlements AMFI. No flashing performed.
- **NEXT (toward real iOS userland):** real root filesystem with real binaries. Options: (a) build Apple OSS `hfs` (macOS 13.5 tag `hfs-627.100.6`) into SWEET like libpthread, then an HFS RAM disk image; (b) iOS 16 dyld + libSystem/dyld shared cache from the IPSW (needs APFS or repacking onto HFS). Expected hurdles: entitlements (sweet_amfi grants none), SHA-1/MD5/SHA-384/512 providers (BearSSL), missing kexts/daemons. Current init is a static test program, not launchd.
- **MILESTONE: USERSPACE RUNS (QEMU).** 0025 CI `38774788048` PASSED, `xnu/out-0025` SHA256 `5496069b...4877`. QEMU `research/q0025-rd` (150 s, no panic): `BSD root: md0` -> `load_init_program: attempting to load /sbin/launchd` -> `*** SWEET userspace: init running as PID 1 ***` -> `SWEET init: still alive` every 5 s. Exec, ad-hoc SHA-256 code signature, syscalls, devfs /dev/console, select timeouts all work. Phone image prepared: `shim/out/shim-boot-0025.img` 16,515,072 bytes SHA256 `9dbfa0b15140c0bd733a16c4f727f6a7df44a8741f98d8e266d5f2fa4f689db0` (payload-0025 = 0025 kernel + sweet-0021.adt + research/sweet-init + rd=md0; ramdisk byte-match check-0025). Waiting for user to put phone in FASTBOOT.
- **0024 CI `38773277811` PASSED**, `xnu/out-0024` SHA256 `a0ba964b...4348`. QEMU `research/q0024-rd` and **PHONE (boot 2026-10-15 17:05:55 UTC, `research/boot0024.log`, image `shim/out/shim-boot-0024.img` SHA256 `cf3dac86...6964`, 16,510,976 bytes, payload `shim/out/payload-0024.bin` = 0024 kernel + `shim/out/sweet-0021.adt` + RAM disk `research/sweet-init` + rd=md0; ramdisk byte-match `check-0024`)** agree: `Added memory device md0`, `BSD root: md0`, `load_init_program: attempting to load /sbin/launchd`, then data abort in accelerate_entitlement_queries (PC 0x...77d2458, FAR 0x1a0) = NULL AMFI interface. Photo `IMG_20261015_190715.jpg`. RAM disk root is physically verified.
- **0025 (`2518c79`)**: new `bsd/kern/sweet_amfi.c` registers a built-in AMFI interface at EARLY_BOOT/MIDDLE: no entitlements (adjustContextWithoutMonitor succeeds without creating a context, queries KERN_DENIED, copies NULL/KERN_NOT_FOUND, get_xml/transmuted false); WithMonitor KERN_NOT_SUPPORTED; OSEntitlements_query and query_context_to_object panic explicitly (CoreEntitlements closed; no kernel caller); TrustCache version 0 (0015 keys on trust_cache_rt==NULL, img4 absent -> still unavailable); CoreEntitlements table zero (PMAP_CS only). Compiles locally; checker updated (bt27 entries). CI **`38774788048`** running. Next artifacts `xnu/out-0025`, `research/bt29`, `research/run29.log`. Real iOS binaries will need real entitlements later (no OSS CoreEntitlements exists).
- **0021-0024 RAM-disk-root iteration (Claude), QEMU only so far, no new phone boot since 0020.** Each kernel tested with `tools/mkpayload.py KERNEL research/q0021.adt OUT --ramdisk research/sweet-init --cmdline "debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress rd=md0"` then `tools/qemu-sweet.py OUT DIR --secs 150 --kernel KERNEL --fail-on-panic` (PATH needs ~/swift/usr/bin for llvm-nm). Fresh ADTs: `research/q0021.adt` (QEMU), `shim/out/sweet-0021.adt` (phone).
  - 0021 CI `38769532000` PASSED, `xnu/out-0021` SHA256 `2b7500a1...962e`, `research/bt25`/`run25.log`. QEMU `research/q0021-rd`: md0 root, then assert `iomediaClass` in IOService::publishHiddenMedia.
  - 0022 (`20ece9c`, publishHiddenMedia without IOMedia class) CI `38770666158` PASSED, `xnu/out-0022` SHA256 `a4d0e787...30c5`, `research/bt26`/`run26.log`. QEMU `research/q0022-rd`: data abort in SHA256_Init (NULL g_crypto_funcs) from vm_kernel_addrhash_internal.
  - 0023 (`c8089d1`, libkern SHA256_Init/Update/Final use built-in ccsha256_ltc_di + ccdigest_init/update on SWEET; also serves code-signing SHA-256; SHA-1/MD5/SHA-384/512 still have NO provider - BearSSL from 0020 could supply them later) CI `38771876423` PASSED, `xnu/out-0023` SHA256 `d763fed7...1003`, `research/bt27`/`run27.log`. QEMU `research/q0023-rd`: **mockfs mounted md0, `load_init_program: attempting to load /sbin/launchd`**, then panic `mockfs_fsnode_vnode failed to create fictitious pages ... rvalue = 5` (mockfs.c:351).
  - 0024 (`3293c80`): mockfs used memdev mi_base (4K page number of a VIRTUAL kernel address for IOKit RAMDisk, truncated to 32 bits) << PAGE_SHIFT as a physical address. Now zero-copy pager mapping only when mi_phys (with 4K units); virtual md uses pagein/blockmap/strategy -> memdev bcopy. memdev's own mdPhys path assumes 4K ppnums (unsafe on 16K arm64), so do NOT switch the RAMDisk to physical. CI **`38773277811`** running. Next artifacts `xnu/out-0024`, `research/bt28`, `research/run28.log`.
  - Sandboxes: bt25/bt26/bt27 contain the next patch's edited files; pristine copies in `research/pre0022`..`pre0024`.
- **PATCH 0021 (Claude): RAM disk root via mockfs -> first userspace program.** Commits `9c37771` (initial; CI `38768500280` FAILED: mockfs_fsnode.c kfree_type(mockfs_fsnode_t) typed-alloc static assert; local xnu-cc stubs `__builtin_xnu_types_compatible` so it can't catch this) and `193772f` (fix), CI **`38769532000`** running: https://github.com/dipa-studio/ios-sweet/actions/runs/38769532000. Next artifacts: `xnu/out-0021`, `research/bt25`, `research/run25.log`.
  - Kernel: `config/MASTER.arm64.sweet` FILESYS_BASE += `mockfs` (XNU's built-in FS: root device is itself a Mach-O, served as /sbin/launchd, plus /dev for devfs). Upstream mockfs bit-rot fixed: kalloc_type/kfree_type used the POINTER typedef mockfs_fsnode_t (nodes were 8 bytes) -> `struct mockfs_fsnode`. `IOService::setRootMedia` asserted IOBlockStorageDriver class exists (IOStorageFamily absent): SWEET-only, a missing class means root=NULL (same as IOSetImageBoot); Apple path keeps assert. All 21 patches apply (`research/check-patch-order.py`); 5 TUs compile locally with -DMOCKFS (`research/mockfs-objs`), imports resolve vs 0020 kernel. Sandbox `research/bt24/xnu` now holds 0021 versions of those 3 files; pristine 0020 copies in `research/pre0021`.
  - Tools: `tools/mkpayload.py --ramdisk IMAGE` appends IMAGE as an extra payload segment right after the kernel, moves kernel_end past it (shim unchanged: ADT+boot_args follow it, image stays below topOfKernelData), and adds ADT `/chosen/memory-map` `RAMDisk`=<phys,size>. Boot with `rd=md0`. Without --ramdisk output is byte-identical to existing 0020 QEMU and phone payloads (verified). `tools/sweet-init.S` + `tools/mkinit.py`: PIC static init (open /dev/console, print PID, heartbeat every 5 s via select, never exits) wrapped into a static arm64 Mach-O (__PAGEZERO, __TEXT@0x100000000, LC_UNIXTHREAD, ad-hoc SHA-256 CodeDirectory v0x20400, 4K pages). Build: `~/swift/usr/bin/clang -target arm64-apple-ios16.0 -c tools/sweet-init.S -o X.o && tools/mkinit.py X.o research/sweet-init` (ld64.lld cannot link static iOS). Signature not verified by a real codesign; the kernel will tell.
  - QEMU with 0020 kernel + RAM disk (`research/q0020-rd.bin`, rd=md0, 150 s `research/q0020-rd150`): `Added memory device md0`, **`BSD root: md0, major 1, minor 0`** (plumbing works), then the setRootMedia assert (now fixed in 0021). NOTE: QEMU needs >60 s to reach IOFindBSDRoot (60 s run showed nothing after stf0; likely RTC/inittodr wait), so use --secs 150.
  - NEXT: download 0021, QEMU 150 s with ramdisk; expect mockfs mount then init exec -> `*** SWEET userspace: init running as PID 1 ***`. Then phone boot with same payload (phone ADT shim/out/sweet-0020.adt pattern + --ramdisk + rd=md0).
- **0020 PHONE RESULT (user transcription of screen, 2026-10-15): KERNEL INIT COMPLETE, WAITING FOR ROOT.** After Skywalk self-tests PASSED, kminit, ifnet_attach lo0/gif0/stf0, screen prints `BSD`, then `Waiting on <dict><key>IOProviderClass</key><string>IOMedia</string><key>Content</key><string>Apple_HFS</string></dict>` and `Failed to write boot-picker-bringup-reason to NVRAM.` No panic. This is IOFindBSDRoot waiting for a root device (none exists); NVRAM warning is expected (no NVRAM driver). QEMU `cpu_idle` snapshot is presumably the same wait (not GDB-confirmed; milestone GDB run was cancelled by user since phone answered it). Draft `research/check-milestones20.gdb` (hbreaks inittodr/vfs_mountroot/IOFindBSDRoot/bsd_utaskbootstrap) left uncommitted/ignored.
- **NEXT MILESTONE: root filesystem -> launchd.** Plan: (1) RAM disk: shim places an image in RAM, ADT /chosen/memory-map `RAMDisk` entry, boot-arg `rd=md0` (XNU md driver). (2) HFS is a separate kext on Apple; build Apple OSS `hfs` (tag paired with macOS 13.5 in distribution-macOS macos-135 release.json) into SWEET like libpthread 0019. APFS is closed. (3) Minimal HFS image with iOS 16 launchd (later: dyld/shared cache; AMFI/code-signing absent will be a later hurdle). User's end goal is full iOS GUI.
- **0020 (AES) VERIFIED + PHONE BOOTED (Claude took over after Codex usage limit).** Actions `38765422261` (`ab9e23f`) PASSED; kernel `xnu/out-0020/kernel.development.sweet` checksum OK; buildtree `research/bt24`, log `research/run24.log`. Actual-kernel AES checks PASS (`research/check-aes20.gdb` / `.log`, 12 extra CBC cases match OpenSSL). 45s QEMU `research/q0020`: no panic, zero unknown glyphs, past old TCP/AES panic -> Skywalk self-tests PASSED -> bsd_autoconf kminit -> ifnet_attach lo0/gif0/stf0; final snapshot PC in `cpu_idle` (idle or waiting; NOT yet diagnosed, could be root-device wait). Image `shim/out/shim-boot-0020.img` 16,461,824 bytes SHA256 `775200cb02d95fc750981516b79d91dcdc96184bbe67a38f9d57c59b4a391828`, ramdisk byte-matches `payload-0020.bin` (`check-0020`). **Phone temporarily booted 2026-10-15 16:10:00 UTC**: one FASTBOOT product sweet, send OKAY0.407s, boot OKAY0.134s, total0.549s, exit0 (`research/boot0020.log`). Awaiting user photo; do not reboot the phone before it. NEXT: read photo; diagnose what QEMU waits on after stf0 (GDB backtrace of threads / longer run). Codex's STOP request below is complete.
- User requests STOP after completing the current0020 AES iteration (Actions/QEMU/phone), then leave a precise committed handoff for another AI. User says FASTBOOT ready again after0019 photo. Do not start a new blocker fix after this iteration.
- Goal: iOS16-generation XNU on Redmi Note10Pro sweet/SM7150. Always commit, use gh/Actions for kernel builds, keep this handoff current. Temporary fastboot boot only; preserve Android/backups. No userland/root filesystem boot yet.
- **Patch0020 update:** initial `e71098d` / Actions `38765012466` superseded by scalar-only compile flags. Added -mgeneral-regs-only to all six provider/BearSSL TUs and corecrypto_aes.c; object disassembly now confirms no SIMD. Updated implementation `ab9e23f`, Actions `38765422261` queued/running: https://github.com/dipa-studio/ios-sweet/actions/runs/38765422261. Do not launch another run. portable BearSSL AES CBC and legacy one-block ECB wired directly into SWEET corecrypto_aes.c. Genuine bitslice implementation, no CPU AES/SIMD requirement, heap or fake global crypto table. Source fetched by `0020-stage-bearssl.sh` from official BearSSL git at immutable `7bea48e5e850ab4cafbe68d3765cdaba13a86d6f`; MIT license retained, downloaded source stays out of git. Kernel limits include adapter only. All128/192/256-bit keys, CBC encrypt/decrypt, copied contexts, in-place/out-of-place; zero block count and size overflow handled, invalid keys clear context. Seven TUs compile to arm64 objects (`research/aes-objs`), imports resolve, all20 patches apply and sources match (`research/patch0020-check.log`). Sandbox `research/bt23/xnu`, originals `research/pre0020`. NEXT: Actions then actual-kernel NIST/random CBC/ECB checks and >=45s QEMU before another phone boot. Next artifacts out-0020 / bt24 / run24.log. 0020 updated CI pending. Local sources/checks match the scalar-only patch.
- **Latest built kernel0019**, implementation `256d3f0`, patches0001-0019. Actions `38763072907` PASSED (4m5s): https://github.com/dipa-studio/ios-sweet/actions/runs/38763072907. Kernel `xnu/out-0019/kernel.development.sweet`, SHA256 `a27df7568f03fb541cf0e8024c0a594fa178a85054fcf9eba29158cbd4c5ecc0`; checksum verified. Log/source `research/run23.log` / `research/bt23` (no nested .git). Seven pthread source/build/header files and staged adaptations byte-match local compile inputs.
- **0019 hardware photo received** `IMG_20261015_175306.jpg`: pthread registration visible, passes mbinit and DLIL checksum/scheduling, same AES fault as QEMU: PC`0xfffffe00079174e0` (`aes_encrypt_key128`), LR`0xfffffe000767c3a4` (`tcp_init`), FAR0x78, x8=0. Disassembly proves NULL g_crypto_funcs->ccaes_cbc_encrypt. Photo processed; no more0019 observation pending. General crypto table remains absent, other hash/mode operations may still fault after0020. DO NOT bypass TCP or install fake crypto. XNU already contains SHA256/HMAC implementations; AES source there is a dispatch wrapper. Full future provider interface libkern/libkern/crypto/register_crypto.h. Apple/corecrypto default README describes evaluation-only licensing, so no external corecrypto was fetched or staged; BearSSL selected for this portable AES integration.
- **0019 pthread FIXED in QEMU and observed beyond its init on phone**: 45s QEMU `research/q0019`, zero unknown glyphs, then AES panic. Actual-kernel API checks PASS `research/check-pthread19.gdb` / `.log`, guest `research/q0019-api`: function/callback table identity, actual provider pthread_init returns, locks/global hash/threadcall/typed zones initialized, thread_selfid via syscall shim + buffer bounds, process hash init/delete via shims restores NULL. Monitor quit prints expected remote-disconnect after PASS. All fixture guests stopped.
- **0019 provider**: genuine Apple libpthread-514.100.2 commit `a6c70ca0e544347a0377babf748f831577ec24f9`, exact paired release with xnu8796.141.3 in distribution-macOS/macos-135/release.json (`research/macos-135-release.json`). 0019 shell stage runs before patches (workflow copies *.sh); three SWEET wrapper TUs use kext BSD header view, vm_fault_external, renamed provider-side pthread_kern/current_uthread; register real function table at EARLY_BOOT SECOND, real pthread_init later. Stager applies bounded address casts, zero user addresses, proper panic format. SWEET opaque ksyn storage enlarged48->56 for trailing kwe_uth, checked with provider static assertion. Local pre-CI TargetConditionals fixture was syntax-only; artifact bt23 carries actual SDK header and CI is authoritative.
- **Phone0019 temporarily booted** 2026-10-15 15:51:36 UTC: exactly one FASTBOOT/product sweet verified; send OKAY0.406s, boot OKAY0.134s, total0.546s, exit0 (`research/boot0019.log`). Image `shim/out/shim-boot-0019.img`, 16,457,728 bytes, SHA256 `19429a57e486b856880df9e27327ed488e0139345311fdb0350974e72103a9a1`. Phone ADT/payload `shim/out/sweet-0019.adt` / `payload-0019.bin` timer19, unpacked ramdisk byte-match (`check-0019`). EntryPA0xb146b488, kernelendPA0xb2000000, boot_argsPA0xb2004000/top0xb2008000. Last user FASTBOOT+USB reply preceded this boot; do not assume phone is still in FASTBOOT.
- **CPU0018 physically verified** by `IMG_20261015_173951 (2).jpg`: boot CPU0 registered, real SGI1 verified, initialization complete -> BSD/MAC/mbinit -> old pthread-table panic. SweetCPU uses legacy IOCPU, ml_processor_register/processor_start/initCPU, real SGI1 clears SIGPdisabled before max CPUs completion; no forced flags/skipped waits. CPU APIs and two-CPU rejection passed (`research/check-cpu18.gdb`, `q0018-api`, `q0018-smp`). Single core; SMP/suspend unsupported. CURRENT SWEET has NO USE_APPLEARMSMP.
- QEMU next run: generate fresh `tools/mkadt.py research/q0020.adt --qemu` (timer27), mkpayload with `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress`, then `tools/qemu-sweet.py PAYLOAD OUT --secs 45 --kernel KERNEL --fail-on-panic`. 12s can miss later panics because IORTC waits30s. Runner snapshot only: panic exit2, blank/incomplete exit3; absence of panic does not mean complete boot. Qualcomm XPU/ABL/panel and phone SMC PSCI require hardware checks.
- Local checker `tools/xnu-cc.py research/run23.log research/bt23 FILTER --per-file`, XNU_CC_OBJDIR for objects. For new BearSSL TUs add XNU_CC_EXTRA with -I bt23/xnu/libkern/crypto/sweet_bearssl/{inc,src}. Patch checker `research/check-patch-order.py` uses temporary upstream index; source fixtures/artifacts ignored under research. GDB mask registers to unsigned64, use function-entry manual-call return traps, discard manipulated guests. No QEMU guest intentionally left running.

## Session log and earlier handoffs (superseded by the active summary above)

### Prior 0019 transition notes (superseded)

- Goal: iOS 16 generation XNU on sweet. Always commit completed work, use gh/Actions for kernel builds, keep this handoff current. Temporary fastboot boot only; preserve Android/backups.
- **0019 build PASSED** Actions `38763072907` (4m5s), implementation `256d3f0`. Kernel `xnu/out-0019/kernel.development.sweet`, SHA256 `a27df7568f03fb541cf0e8024c0a594fa178a85054fcf9eba29158cbd4c5ecc0`; checksum verified. Log/source `research/run23.log` / `research/bt23`; all seven patched files and staged provider adaptations match local compile inputs. Prefer bt23 as the next baseline.
- **0019 pthread FIXED in QEMU**: 45s run `research/q0019` registers provider, passes mbinit, DLIL SUM16 checks and DLIL thread scheduling. Actual-kernel GDB checks `research/check-pthread19.gdb` / `.log` PASS: function/callback table identity, real _pthread_init returns, locks/global hash/cleanup threadcall/typed zones non-NULL, thread_selfid via actual syscall shim with output bounds, process hash init/delete through actual shims restores NULL. Guest stopped after tests; no fixture left running. GDB monitor quit prints expected remote disconnect after PASS.
- **Current next blocker:** QEMU0019 panic data abort FAR0x78 at `aes_encrypt_key128` PC`0xfffffe00079174e0`, called by `tcp_init` LR`0xfffffe000767c3a4`. Disassembly confirms `g_crypto_funcs == NULL`, loading ccaes_cbc_encrypt at+0x78. General crypto registration is still absent; DO NOT bypass TCP or supply fake crypto. Next integrate a genuine compatible crypto implementation/provider (AES first needed here, other digest/mode APIs also used). XNU contains SHA256/HMAC but no AES implementation; its corecrypto_aes.c is a dispatch wrapper. Full crypto table is in libkern/libkern/crypto/register_crypto.h.
- **0019 phone image prepared and verified**, user reports FASTBOOT+USB again; exactly one device/product sweet verified. `shim/out/shim-boot-0019.img`, 16,457,728 bytes, SHA256 `19429a57e486b856880df9e27327ed488e0139345311fdb0350974e72103a9a1`; unpacked ramdisk matches phone payload (`shim/out/check-0019`, `payload-0019.bin`, `sweet-0019.adt`, timer19). EntryPA0xb146b488; kernelendPA0xb2000000; boot_argsPA0xb2004000/top0xb2008000. Usual debug cmdline cpus=1/-noprogress. **Temporarily booted 2026-10-15 15:51:36 UTC**: send OKAY0.406s, boot OKAY0.134s, total0.546s, exit0 (`research/boot0019.log`). User asked for photo after45s. Await the photo; DO NOT reboot again before observation. Bootloader acceptance only; no0019 physical progress observed yet.
- **Hardware photo confirms 0018 progress** (`IMG_20261015_173951 (2).jpg`): real phone prints `SWEET CPU: boot CPU 0 registered, SGI1 verified, initialization complete`, enters BSD/MAC, reaches `mbinit: done`, then the same missing-pthread-function-table panic as QEMU at pthread_shims.c:318. CPU completion/interrupt delivery is now physically observed. The photo was received; no further phone boot performed yet.
- **Patch0019 committed/pushed `256d3f0`; Actions `38763072907` queued/running:** https://github.com/dipa-studio/ios-sweet/actions/runs/38763072907. Do not launch a duplicate. genuine Apple OSS libpthread-514.100.2 provider (immutable commit `a6c70ca0e544347a0377babf748f831577ec24f9`), paired with xnu-8796.141.3 by Apple's `distribution-macOS/macos-135/release.json` (`research/macos-135-release.json`). `0019-stage-libpthread.sh` fetches/stages it before patches; workflow now copies shell scripts too. SWEET-only wrappers compile all three real kernel sources, rename provider-side symbols, use kext header view and vm_fault_external, register the real function table at EARLY_BOOT SECOND. Existing pthread_init then runs the actual provider initialization. No pthread wait/syscall is bypassed. Source staging includes bounded explicit address casts/zero user addresses and panic-format fixes. SWEET kernel opaque ksyn storage enlarged from48 to56 bytes to contain this provider's trailing kwe_uth, with a provider size assertion. Local compile of three provider TUs plus pthread_shims/kern_fork passed; imports resolve and provider exports do not collide with existing kernel symbols. All19 patches apply and changed sources match (`research/patch0019-check.log`). Source sandbox `research/bt22/xnu`, originals `research/pre0019`, objects `research/pthread-objs`. Local TargetConditionals fixture only has target macros for syntax; CI stages the real macOS SDK header and is authoritative. Next Actions artifacts: out-0019 / bt23 / run23.log; run QEMU >=45 seconds. 0019 CI is pending; no 0019 QEMU run yet.
- **Latest kernel implementation `e7d9550`, patches0001-0018; CI `38760004398` PASSED (3m56s)**: https://github.com/dipa-studio/ios-sweet/actions/runs/38760004398. No build is pending. Kernel `xnu/out-0018/kernel.development.sweet`, SHA256 `b3c8d59acc88f93a2c836eb2527a05ed4fbaac7c580a2ea8c3b795137f4aadf1`; checksum verified. Source/log `research/bt22` / `research/run22.log` (baseline for patch0019; no nested .git). New driver/config sources match CI exactly.
- **CPU wait FIXED in QEMU**: SweetCPU uses legacy IOCPU, validates single boot CPU, ml_processor_register -> processor_start -> initCPU real SGI1 -> scheduler/IOKit completion -> ml_set_max_cpus. It does NOT force a flag or skip a wait. CPU APIs passed: Running CPU0, processor_array[0] association, SGI signalling enabled, name, unsupported secondary-start error (`research/check-cpu18.gdb` / `.log`, `research/q0018-api`). Single-core only; SMP and suspend unsupported. Two-CPU topology fails explicitly (`research/q0018-smp`).
- **Next blocker reproduced in 45s QEMU** (`research/q0018-long`, zero unknown glyphs): BSD initialization reaches MAC framework, network mcache and `mbinit: done`, then **`pthread kernel extension not loaded (function table is NULL). @pthread_shims.c:318`**. Do not bypass pthread_init: find/integrate the matching open-source libpthread kernel implementation and register its real function table. A 12s run `research/q0018` looked panic-free before the 30s IORTC wait elapsed; use >=45s or GDB checkpoints for the next iteration. No userland/root filesystem boot yet.
- **Phone 0018 TEMPORARILY BOOTED** 2026-10-15 **15:31:15 UTC**: exactly one FASTBOOT device verified product sweet; send OKAY0.400s, boot OKAY0.134s, total0.539s, exit0. Local log `research/boot0018.log`. This confirms bootloader acceptance only. User was asked for a photo; await it, DO NOT reboot the phone again before their observation. No flashing performed.
- Current hardware image `shim/out/shim-boot-0018.img`, **16,437,248 bytes**, SHA256 **`b7a23595d143a76c72c9fe2cfcc5d77a8f16987b5af1a2703bbffdfa6922908c`**. Phone ADT/payload `shim/out/sweet-0018.adt` / `shim/out/payload-0018.bin` (timer19), unpacked ramdisk exactly matches payload (`shim/out/check-0018`). EntryPA0xb146b488; kernelendPA0xb1ffc000; boot_argsPA0xb2000000/top0xb2004000. Command line `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress`.
- QEMU payload/ADT `research/q0018.bin` / `research/q0018.adt` (timer27). Run `python3 tools/qemu-sweet.py research/q0018.bin research/NEW-OUT --secs 45 --kernel xnu/out-0018/kernel.development.sweet --fail-on-panic`; fresh ADT seed for a new payload. Output fb.png/fb.txt/regs.txt/qemu.log/result.json. Visible panic exit2; blank/incomplete decode exit3; no_panic_observed is snapshot-only, not successful boot. -noprogress prevents the graphical indicator corrupting console text. Qualcomm XPU/bootloader/panel and SMC PSCI still need physical validation.
- Patches0014-0017 fixed PRNG registration/direct SHA256, explicit unavailable trust-cache service with rejected loads/no matches, built-in SweetPlatformExpert, and timer PPI from ADT (phone19/default19, QEMU27). All their checks/artifacts are preserved in the history below. CURRENT SWEET has NO USE_APPLEARMSMP; do not assume gCPUIC/gAIC/gPMGR AppleARMSMP globals exist.
- Local single-file checker: tools/xnu-cc.py research/run22.log research/bt22 FILTER --per-file, output via XNU_CC_OBJDIR. Patch checker `research/check-patch-order.py` applies all18 via temporary index, matches sandbox sources. Sandbox for0018 `research/bt21/xnu`, originals `research/pre0018`, objects `research/cpu-objs`. First compiler issues were missing machine/atomic.h and nonexistent getNameSymbol; fixed and both TUs compiled successfully before CI. Fixtures/artifacts under research are local-only/ignored.
- GDB: mask int(register)&((1<<64)-1) for unsigned kernel pointers; use function-entry manual-call return traps, discard manipulated guests. No QEMU fixture is intentionally left running.

### Earlier active handoff snapshot (superseded)


- **0018 milestone:** Actions `38760004398` PASSED (3m56s), checksums passed, new CPU/build files byte-match CI tree. Kernel `xnu/out-0018/kernel.development.sweet`, SHA256 `b3c8d59acc88f93a2c836eb2527a05ed4fbaac7c580a2ea8c3b795137f4aadf1`; log/tree `research/run22.log` / `research/bt22`. QEMU `research/q0018` 12s: boot CPU registered, SGI1 verified, CPU initialization complete, **BSD initialization entered** (copyright, MAC framework, buffer headers), no panic/zero unknown glyphs. Direct CPU API checks PASS (`research/check-cpu18.gdb`, `.log`, `research/q0018-api`): CPU0 Running, processor matches processor_array[0], real SGI enabled, CPU name correct, secondary-start returns KERN_NOT_SUPPORTED. Two-CPU ADT correctly panics before registration (`research/q0018-smp`). Longer 45s run `research/q0018-long` still running; next BSD wait/fault not yet identified.
- **Prepared 0018 phone image:** `shim/out/shim-boot-0018.img`, 16,437,248 bytes, SHA256 `b7a23595d143a76c72c9fe2cfcc5d77a8f16987b5af1a2703bbffdfa6922908c`. Phone ADT/payload `shim/out/sweet-0018.adt` / `shim/out/payload-0018.bin`, usual debug args with cpus=1 and -noprogress. Unpacked ramdisk byte-compared (`shim/out/check-0018`). Entry PA remains 0xb146b488; kernel end PA 0xb1ffc000, boot_args 0xb2000000/top0xb2004000. User reports FASTBOOT+USB ready; read-only check found exactly one product sweet. NEXT: temporary fastboot boot of this verified image, record send/boot results, then await hardware photo without rebooting again.
- Patch 0018 committed/pushed **`e7d9550`**; Actions **`38760004398`** queued/running: https://github.com/dipa-studio/ios-sweet/actions/runs/38760004398. Do not launch a duplicate run.
- Active continuation: patch **0018** implemented in `iokit/Kernel/arm/SweetCPU.cpp` + arm64 source list + exact qcom,kryo470 personality. Keeps legacy IOCPU, accepts ONLY the single boot CPU, fills ml_processor_info from parsed topology with CPU object as cpu_id, calls ml_processor_register and processor_start. initCPU sends SGI1 via ICC_SGI1R_EL1 and waits (1-second deadline) for real cpu_signal_handler to clear SIGPdisabled. Only after successful startup calls ml_cpu_init_completed/cpusRunning and publishes completion/max CPUs. Secondary startup/suspend are explicitly unsupported. Local C++ compile passed for both TUs (`research/cpu-objs`), all imports resolve, object contains dsb ishst / ICC_SGI1R / isb; all18 patches apply in order and match sources. Sandbox `research/bt21/xnu`, originals `research/pre0018`; next CI artifacts should use `xnu/out-0018`, `research/bt22`, `research/run22.log`. User has the phone available; first run QEMU, then prepare/temporarily boot useful hardware progress.
- Goal: iOS 16 generation XNU on Redmi Note 10 Pro / sweet. User wants persistent progress, commits, kernel builds via `gh` Actions, and this handoff kept current across agent switches. Temporary `fastboot boot` only; preserve Android and backups.
- Latest kernel implementation: **`aa3f991`**, patches **0001-0017**. All four new Actions builds PASSED: 0014 `38748543058` (4m0s), 0015 `38749549779` (4m3s), 0016 `38750733996` (4m3s), 0017 **`38751507437` (4m7s)**. Latest: https://github.com/dipa-studio/ios-sweet/actions/runs/38751507437. No build is pending.
- **Current blocker: CPU initialization has no SWEET CPU driver.** QEMU registers SweetPlatformExpert, then kernel_bootstrap_thread waits in **kperf_init_early -> ml_wait_max_cpus**. Confirmed via actual-kernel GDB call stack (`research/locate-cpu-wait2.log` / `.symbols`) and normal-run `max_cpus_initialized == 2` (MAX_CPUS_WAIT). Do not force the flag or remove the wait. Next implement real CPU registration and completion using XNU's CPU/processor interfaces. CURRENT SWEET uses legacy IOCPU (`USE_APPLEARMSMP` is absent); enabling AppleARMSMP is a separate architectural change requiring GIC/PMGR services. No userland/root filesystem boot yet.
- Fixed this session: PC=0 unregistered PRNG callback (0014, built-in HMAC-SHA256 provider + direct entropy/write_random hashing); absent Image4/AMFI trust-cache service (0015, unavailable runtime, loads rejected and queries no-match); missing platform driver (0016, SweetPlatformExpert exact personality); incorrect QEMU timer IRQ (0017, validated ADT PPI property, phone default19/QEMU27).
- **Latest kernel** `xnu/out-0017/kernel.development.sweet`, SHA256 `055a80190ab998b4df9203f1102072dcc78faad1779a537a514e522b682b582f`. Buildtree/log **`research/bt21` / `research/run21.log`**; all nine changed C/C++/header/config files byte-match local checked sources. Checksums passed. Entry PA `0xb146b488`, kernel end PA `0xb1ff4000`. Preferred baseline for patch 0018: `research/bt21/xnu` (no nested .git).
- **QEMU verified**: `research/q0017-noprogress` ran **30 seconds**, no visible panic, **zero unknown glyphs**, IRQ exceptions returned normally (4 IRQs, tickless idle). It still waits for CPU completion, so this is NOT a completed boot. Earlier 15s run `research/q0017` captured 122 IRQs, timer value27, GICR_ISENABLER0 `0x08000002`, and CPU WAIT; graphical progress overlay corrupted 13 glyphs. Add **`-noprogress`** to keep the console readable. New runner classifies incomplete/blank decoding explicitly (exit3 with --fail-on-panic), visible panic exits2. Snapshot-only; use regs/GDB to diagnose stalls.
- Current QEMU payload/ADT: **`research/q0017-noprogress.bin` / `research/q0017.adt`**. Run: `python3 tools/qemu-sweet.py research/q0017-noprogress.bin research/NEW-OUT --secs 30 --kernel xnu/out-0017/kernel.development.sweet --fail-on-panic`. Generate fresh seed with mkadt for a new payload. QEMU virt models generic ARM execution, not Qualcomm XPU/bootloader/panel or the phone's SMC PSCI conduit.
- **Prepared phone image**: **`shim/out/shim-boot-0017.img`**, 16,416,768 bytes, SHA256 `51ff7fe30b4a6668c3452ffe1da922c5ac30cb8de60625c2a652587ecbd0ec92`. Phone ADT/payload `shim/out/sweet-0017.adt` / `shim/out/payload-0017.bin` (timer19). Unpacked ramdisk exactly matches payload (`shim/out/check-0017`). Command line **`debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam -noprogress`**. NOT sent to phone this session: known CPU-driver wait should be addressed in QEMU first. Last actual phone boot remains 0013; user's latest photo `IMG_20261015_160033.jpg` confirmed the old PRNG PC=0 panic.
- Direct QEMU/GDB API checks: PRNG 600-byte chunking, buffer bounds, changing output, zero-length reads/writes, user reseed, contended refresh, generator1 init/output PASS again on latest0017 (`research/check-prng17.gdb` / `.log`, guest `research/q0017-api`). Trust-cache unavailable-service/argument/output cases PASS on0015 (`research/check-trustcache.gdb` / `.log`). Platform registration + target/product normal/truncated/zero/null/bounds PASS on0016 (`research/check-platform.gdb`, `research/check-platform3.log`). Different platform ID correctly retains IOPanicPlatform fallback (`research/q0016-negative`). Timer PPI32 and size2 correctly panic (`research/q0017-badppi`, `research/q0017-badsize`); omitted property selects19 (`research/q0017-default`). These are API/bring-up checks, not crypto certification or SMP scheduling validation.
- Local checker **`research/check-patch-order.py`** verifies all17 patches and changed source equality using a temporary upstream git index. Fixtures/logs/artifacts under research are local-only and ignored. For GDB unsigned kernel pointers, mask `int(register_value) & ((1<<64)-1)`; x30/x29 may be rendered signed. Stop at a function entry for manual-call return traps, and discard each manipulated guest after API tests. All fixture QEMU guests have been stopped.


- User wants persistent progress toward iOS 16, commits for completed changes, builds through `gh` / GitHub Actions.
- Keep this file current at every milestone so another agent can resume immediately, including when usage limits interrupt a session.
- Patch 0017 committed/pushed `aa3f991`, Actions `38751507437` running: https://github.com/dipa-studio/ios-sweet/actions/runs/38751507437. Next artifacts: xnu/out-0017, research/bt21, research/run21.log. Do not duplicate.
- Patch 0016 kernel downloaded/checksum verified: SHA256 `d06336c54baa06e0df6561a8bd7df98a9b9f7502c9381c62d1a44c045cd1ce46`, `xnu/out-0016/kernel.development.sweet`; buildtree/log `research/bt20` / `research/run20.log`. QEMU `research/q0016` (10s) prints platform expert registered, zero unknown glyphs, no panic observed BUT stalls (timer mapping still wrong until 0017). Direct actual-kernel GDB tests passed for registered instance and target/product names, including maxLength=1/0 and NULL, sentinels intact (`research/check-platform.gdb`, `research/check-platform3.log`, `research/q0016-api3`). First two fixture attempts used premature/wrong return breakpoints; discarded, corrected fixture uses start-return observation then a function-entry return trap. No phone boot yet.
- Patch 0016 CI `38750733996` PASSED (4m3s); artifacts not yet downloaded/booted. Patch 0017 prepared to fix QEMU timer fidelity BEFORE interpreting future no-panic/stall runs: actual `qemu-system-aarch64 -M virt,gic-version=3,dumpdtb=research/qemu-virt.dtb ...` timer property has virtual PPI 11 => INTID 27, while phone uses INTID 19. Kernel formerly hardcoded 19. New optional /arm-io/gic virtual-timer-intid property selects the PPI (validate exact u32 and 16..31); missing property retains phone default 19. One RO-late global drives GIC enable and sleh_irq dispatch. tools/mkadt.py emits phone19/QEMU27. Both C TUs compile (`research/timer-objs`), ADT serialize/parse checks confirm values/addresses, all 17 patches apply and match. Sandbox `research/bt19/xnu`, originals `research/pre0017`; initial local sleh compile failed due read-only exported header not updated, fixed export and BOTH recompiled successfully. CI exports normally.
- Architecture correction for next agent: CURRENT SWEET board_config does NOT define USE_APPLEARMSMP; it compiles the legacy IOCPU path, not cpu_boot_thread/IOPMGR AppleARMSMP. Existing roadmap mentions AppleARMSMP as a future approach. Do not look for gCPUIC/gAIC/gPMGR globals in the current kernel: they are absent. Determine the actual CPU-init wait after platform registration before choosing the next driver architecture.
- Patch 0016 committed/pushed as `0dcdf5c`; Actions `38750733996` running: https://github.com/dipa-studio/ios-sweet/actions/runs/38750733996. Next artifacts: `xnu/out-0016`, `research/bt20`, `research/run20.log`.
- Patch 0016 implemented: new `iokit/Kernel/arm/SweetPlatformExpert.cpp`, arm64 source list, built-in personality in KernelConfigTables.cpp guarded by ARM64_BOARD_CONFIG_SWEET. Matches only xiaomi,sweet at score 10000, keeps IOPanicPlatform fallback for other hardware. Uses IODTPlatformExpert base initialization/power domain and createNubs CPU logical-ID annotation; overrides top-level publishing because base requires nonexistent Apple NVRAM /options. Publishes real CPU/top-level nodes, provides bounded target/product names, and registers the platform service. GIC/PMGR and arm-io child-bus drivers remain separate work. Both C++ TUs compile (`research/platform-objs`), all imports resolve against 0015/own objects, all 16 patches apply and sources match. Sandbox `research/bt19/xnu`; originals `research/pre0016`. NEXT: full Actions/QEMU; inspect CPU boot waits after the platform registers, do not equate absence of panic with successful boot.
- Patch 0015 CI `38749549779` PASSED (4m3s), checksum verified. Kernel `xnu/out-0015/kernel.development.sweet`, SHA256 `ca1b424a596c7058550ad1659080a333e7643270f019656401d80bf2b876645f`; buildtree/log `research/bt19` / `research/run19.log`. QEMU `research/q0015` (10s, zero unknown glyphs) passes trust-cache handling and machine lockdown, then panics `Unable to find driver for this platform: "xiaomi,sweet" @IOPlatformExpert.cpp:2319` (IOPanicPlatform fallback). Next concrete work: add a built-in SWEET IODTPlatformExpert personality/class; keep the fallback for mismatched platforms. No phone boot yet.
- Direct trust-cache API checks PASSED in the actual 0015 kernel under QEMU/GDB (`research/check-trustcache.gdb`, `research/check-trustcache.log`, `research/q0015-api`): runtime pointers NULL, hash/UUID queries return NOT_FOUND, typed/untyped/legacy loads return NOT_SUPPORTED, capabilities outputs zero and bounds preserved, invalid-argument cases still reject. Second PRNG check also verifies contended refresh returns immediately (`research/check-prng2.log`, `research/q0014-api2`).
- Patch 0015 committed/pushed `8f851d4`, Actions run `38749549779` running: https://github.com/dipa-studio/ios-sweet/actions/runs/38749549779. Do not duplicate.
- Direct PRNG API checks passed in the REAL 0014 kernel under QEMU/GDB, stopped before trust-cache init (`research/check-prng.gdb`, log `research/check-prng.log`, guest `research/q0014-api`). Invoked read_random for 600 bytes (chunking and buffer sentinel intact), repeated output differed, zero-length read/write succeeded, write_random(64-byte input) succeeded, secondary generator 1 initialized and generated distinct output. QEMU log has no exceptions during these checks; guest was discarded after the tests. This tests API behavior, not a cryptographic certification or SMP scheduling.
- Patch 0015 implemented in `bsd/kern/kern_trustcache.c`: SWEET with missing Image4/AMFI marks both runtime pointers NULL and logs service unavailability. Existing static loader handles NULL. Public load APIs return KERN_NOT_SUPPORTED; hash/UUID queries return KERN_NOT_FOUND; capabilities outputs are zero with KERN_NOT_SUPPORTED. Invalid-input checks remain, and Apple paths/available-provider initialization retain existing behavior. No trust is granted. Local arm64 compile passed (`research/trustcache-objs`), all 15 patches apply and sources match. Sandbox `research/bt18/xnu`, baseline `research/pre0015`. Next: Actions/QEMU and direct unavailable-service API checks using GDB.
- Patch 0014 CI `38748543058` PASSED (4m0s), artifact checksum passed. Kernel `xnu/out-0014/kernel.development.sweet`, SHA256 `741de20c851755d333759d7e668346f3edb4f325efac4cc7c142d80d1f5ff75c`; buildtree/log `research/bt18` / `research/run18.log`. QEMU run `research/q0014` (10s, zero unknown glyphs) prints `SWEET PRNG: HMAC-SHA256 registered`, passes commpage initialization, loads vnguard policy, THEN panics `image4 interface not available @kern_trustcache.c:253`. PC=0 fault FIXED IN QEMU. No new phone boot performed.
- Next work: SWEET currently has neither AppleImage4 nor AMFI. `trust_cache_runtime_init` unconditionally requires both; unlike BCM2837, SWEET enters this startup path. Investigate an explicitly unavailable trust-cache runtime with rejected loads/no query matches while providers are absent; preserve all Apple-platform checks. Merely skipping the startup call would leave later AMFI/IMG4 dereferences unsafe. Existing load_static_trust_cache already handles trust_cache_rt == NULL.
- QEMU runner now supports `--kernel MATCHING_KERNEL --fail-on-panic`: runtime font extraction from the payload produces exact `fb.txt`, plus `result.json`; a visible panic returns 2. Baseline 0013 re-run `research/q0013-text` detects the same NULL callback panic with zero unknown glyphs. Synthetic glyph roundtrip (including literal `?`) and invalid-VA rejection passed. Screen rows remain circular, not a full log; `no_panic_observed` does not prove successful boot. README has the invocation.
- Patch 0014 committed/pushed as `be61f99`; Actions run `38748543058` is running: https://github.com/dipa-studio/ios-sweet/actions/runs/38748543058. Do not start a duplicate build.
- 2026-10-15 active: hardware photo `IMG_20261015_160033.jpg` confirms the same PC=0 instruction-fetch abort as QEMU (LR `0xfffffe0007443fe4` = read_random). Independently reproduced with kernel 0013 in `research/q0013` (8-second run); prior allocator fix works. Latest tooling commit reviewed: `8d66d2d`.
- Patch 0014 implemented: registers a built-in HMAC-SHA256 DRBG provider at EARLY_BOOT/FIRST, before commpage creation. A shared mutex serializes output/reseed across CPUs (correctness first; no per-CPU scaling yet), initgen validates CPU identities, refresh uses try-lock and the existing entropy filter/health tests. SWEET entropy accumulation and write_random now use the built-in SHA256 directly; no incomplete g_crypto_funcs table is registered. The existing bootloader-seed requirement remains enforced.
- Local validation: both PRNG translation units compile to arm64 objects in `research/prng-objs`; no SHA256 wrapper imports remain. All 14 patches apply in CI order and resulting PRNG sources match local inputs. Sandbox `research/bt17/xnu`, originals `research/pre0014`, checker `research/check-patch-order.py`. NEXT: Actions kernel build, download to `xnu/out-0014`, run the QEMU payload before requesting another phone boot. Baseline QEMU ADT/payload are `research/q0013.adt` / `research/q0013.bin`.
- 2026-10-15 08:15 QEMU EMULATION WORKS (`tools/qemu-sweet.py`, see "QEMU emulation" below). Patch 0013 VERIFIED in QEMU: boot passes kmem_crypto_init and ulock_initialize. NEXT BLOCKER (reproduced in QEMU, expected on hardware too): `pmap_create_commpages -> random() -> RandomULong -> read_random -> prng_funcs.refresh == NULL` (instruction fetch abort at pc 0, lr read_random+0x34). Nobody calls `register_and_init_prng` (closed corecrypto kext does it on Apple). Fix = patch 0014: SWEET-registered cckprng_funcs provider (osfmk/prng/prng_random.c); note random_cpu_init also panics while !prng_ready. The 07:26 hardware boot of 0013 will most likely show this same panic.
- Previous hardware boot: patch 0013 (`a3a46e2`) CI `38686345689` PASSED (3m44s), image `shim/out/shim-boot-0013.img` was temporarily booted on 2026-10-15 at 05:26 UTC: send OKAY (0.407s), boot OKAY (0.134s), total 0.546s. Superseded by the hardware/QEMU PC=0 observation and patch 0014 work above.
- Latest kernel implementation commit: `8f851d4`. Latest successful kernel CI: `38749549779` (patch 0015), https://github.com/dipa-studio/ios-sweet/actions/runs/38749549779.
- CURRENT image: `shim/out/shim-boot-0013.img`, 16,412,672 bytes, SHA256 `110d1c46aee4b60253db24b6535e9781c4cf0fd25ca2a70e9016cf81378cea25`. Kernel `xnu/out-0013/kernel.development.sweet`, SHA256 `f0b1d375995316c550ce7014ff234d8271e9b9ac2857795ceff41b76ba2cd740`, plain arm64. CI log confirms 0013 applied; checksums passed. Entry PA `0xb146b488`, kernel end PA `0xb1ff4000`.
- Current log/buildtree: `research/run17.log`, `research/bt17` (extracted, no nested .git; preferred baseline for patch 0014). Payload/ADT: `shim/out/payload-0013.bin`, `shim/out/sweet-0013.adt` (includes /defaults). Unpacked ramdisk byte-compared with payload in `shim/out/check-0013`.
- Patch-0012 original image: `shim/out/shim-boot-0012.img`, 16,412,672 bytes, SHA256 `cf4b8ec4a65a51888d71c17d09cd0831d6b761b90e2531fdb8e575c32f4fd24a`. Kernel `xnu/out-0012/kernel.development.sweet`, SHA256 `69b78f49f6459cc63a0af44e7cf73c1779ef72130ef72b12ae86c88183ffc742`; checksums passed and sweet_early_relocate symbol present. Entry PA remains `0xb146b488`, kernel end PA `0xb1ff4000`.
- Patch-0012 log/tree: `research/run16.log`, `research/bt16` (extracted, no nested .git; preferred baseline for next patch). CI log confirms 0012 applied. Payload `shim/out/payload-0012.bin`, ADT `shim/out/sweet-0012.adt`; packed ramdisk byte-compared with payload in `shim/out/check-0012`.
- Active payload command line: `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam`.
- Latest observed photo: `/home/dipa/Downloads/IMG_20261015_071346.jpg` (local only). Stages 9 (kernel framebuffer VA), 10 (TTBR0 off/TLB flush), 11 (physmap table pointers) and 12 (calling pmap_bootstrap) all visible. Persistent diagnostics are VERIFIED ON HARDWARE.
- pmap.c:1987 is the assert after SecureDTLookupEntry(NULL, "/defaults", &entry). The pmap-max-asids property itself is optional; an empty /defaults uses XNU's MAX_ASIDS. Do not bypass the assertion or guess an ASID limit.
- Previous payload-only fix image: `shim/out/shim-boot-0012-defaults.img`, SHA256 `3ff61a268853c6ea7cbf284833f1346a1d791980ca366b6e1a215a86e040512b` (16,412,672 bytes). Same kernel/CI as 0012; ADT 2516 bytes (`shim/out/sweet-0012-defaults.adt`), root /defaults present with no ASID override. Payload `shim/out/payload-0012-defaults.bin`; unpacked ramdisk exactly matches payload (`shim/out/check-0012-defaults`). This boot reached the allocator crypto NULL-pointer fault below.
- Latest hardware photo: `/home/dipa/Downloads/IMG_20261015_071608.jpg` (local only). Normal serial framebuffer console works. VM bootstrap/zone initialization, logging, scheduler, IPC, KDP and ulock_initialize print before the kmem_crypto_init data abort. gPanicBase warnings are expected because PLATFORM_PANIC_LOG_DISABLED is configured, and are not the faulting call.
- Faulting instruction: `ldr x0, [x8, #0x150]` in crypto_random_kmem_ctx_size; x8 = NULL g_crypto_funcs. Source: libkern/crypto/corecrypto_rand.c and osfmk/vm/vm_kern.c:2448. rand.h explicitly permits NON-cryptographic kmem RNGs, but requires no locking in generation and context size <=256. Do not substitute read_random here: the global PRNG provider is also unregistered and kmem generation must remain lock-free. early_random may seed contexts during single-CPU bootstrap; it uses the built-in HMAC-SHA256 DRBG with the host-generated ADT seed.
- Patch 0013 keeps the replacement entirely private to vm_kern.c: SplitMix64 state is 8 bytes per CPU/sizeclass, initialized using early_random. Uniform selection uses rejection sampling to avoid modulo bias. Other platforms retain the original corecrypto calls; SWEET's generic crypto APIs/registration remain untouched. Reference: https://prng.di.unimi.it/splitmix64.c (Sebastiano Vigna, public domain).
- Validation: vm_kern.c compiles to arm64 (`research/kmem-rng-objs`, using `research/run16.log` + `research/bt16`). Undefined symbols include early_random and NO crypto_random_* references. All 13 patches apply in CI order and match the checked source. Original saved as `research/vm_kern.pre0013.c`.
- RNG host checks: extracted actual new helper in `research/kmem-rng-check.c`; 16,384 outputs match the author's downloaded reference (`research/splitmix64-reference.c`), 147,456 bounded outputs satisfy their limits (including 1 and UINT64_MAX), and a forced rejection advances correctly. Full kernel crypto services and the registered kernel PRNG provider remain future work; this patch only supplies the allocator RNG contract.
- Patch-0011 artifacts: kernel `xnu/out-0011/kernel.development.sweet`, log `research/run15.log`, extracted buildtree `research/bt15` (no nested .git). CI log confirms patch 0011 applied; artifact checksums passed. Kernel is plain arm64, entry VA `0xfffffe000746b488` -> PA `0xb146b488`, kernel end PA still `0xb1ff4000`.
- Patch-0011 image: 16,412,672 bytes, SHA256 `29ad5cbfc752473de4af2c471a24a8b34f92da4bff5afec65c614b90cd3ad53a`. Kernel SHA256 `8ac3a956894b09f7bd0d890de8c5de38c65513287feb1e1bcd12db8ca772ee5c`. Payload/ADT in `shim/out/payload-0011.bin`, `shim/out/sweet-0011.adt`. Header unpacked/checked in `shim/out/check-0011`.
- First patch-0011 attempt timed out waiting for FASTBOOT; superseded by the successful send/boot recorded above. Do not repeat the boot before the user reports the current screen.
- Patch-0011 photo: `/home/dipa/Downloads/IMG_20261015_070218.jpg` (local only). Visible stages 1-8 and old red shim text; entry PA B146B488, boot args PA B1FF8000 / top B1FFC000. No evidence yet locating execution after stage 8.
- Patch-0012 sandbox: `research/bt15/xnu` (NO nested .git). Proposed permanent debug VA: VM_MIN_KERNEL_ADDRESS + ARM_TT_L2_SIZE, in the reserved gap below gVirtBase and above low globals; map the same PA framebuffer as Normal-NC in the final TTBR1 before arm_vm_physmap_init changes phystokv(). Keep the early panic sink until normal kprintf startup.
- Patch 0012 validation: all 4 changed C translation units compiled to arm64 objects in `research/post-ttbr0-objs`; internal header export added to osfmk/arm64/Makefile and recreated locally in EXPORT_HDRS for pe_serial.c. All 12 patches apply in CI order and match all 6 edited files. Baselines are saved under `research/pre0012/`.
- Actual mapping-helper host model (`research/early-map-check.c`, barrier stubbed only for host compilation) confirms: VA `0xfffffe0002000000`, L1 index 2016, L2 index 1; descriptor `0x006000009c000605` = framebuffer PA, Normal-NC, outer-shareable, EL1 RW, PXN+UXN. All other L2 entries preserved. The gap is excluded by ARM_LARGE_MEMORY's pmap_virtual_region(0).
- Next boot command line MUST add `-enable_kprintf_spam`: DEVELOPMENT disables kprintf_output by default even when DB_KPRT is set (`pexpert/arm/pe_kprintf.c`). Planned command line: `debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam`.

### Patch 0012 screen legend (after original stages 1-8)
- 9: kernel framebuffer VA live; 10: TTBR0 off / TLB flushed; 11: physmap pointers rebound.
- 12: calling pmap_bootstrap; 13: pmap_bootstrap returned; 14: early I/O page tables ready; 15: arm_vm_init returned.
- 16: calling serial_init; 17: fbcon config read / mapping; 18: fbcon mapping returned; 19: serial_init returned; 20: kprintf startup complete.
- Normal serial initialization clears the screen, so earlier stages may disappear before 19. If serial exists, early console disables after 20; otherwise early panic output stays enabled.
- Local source sandbox: `research/bt13/xnu` (git baseline `623b060`, patches 0001-0008 already in baseline; uncommitted export edits correspond to patch 0009). Preserve those edits when producing patch 0010.
- Previous compile log/tree: `research/run13.log`, `research/bt13`; previous kernel: `xnu/out/kernel.development.sweet`. New successful log/tree: `research/run14.log`, `research/bt14`; new kernel: `xnu/out-0010/kernel.development.sweet`.
- Current device access: patch-0012 image was temporarily started from FASTBOOT; no adb connection is expected. Never flash partitions for bring-up; use `fastboot boot` with the shim image.
- Patch `0010` lives in `xnu/patches/0010-sweet-early-framebuffer-debug.patch`. Its exact compiled sources are under `research/bt13/xnu`; generated objects are in `research/early-objs`.
- Local checks passed: all 5 changed/new translation units compiled to arm64 Mach-O objects; new console only imports `_doprnt` and `iso_font` (both exist in the previous kernel). All 10 patches applied to a temporary upstream git index in CI order, and all 7 resulting changed source files matched the local compile inputs.
- Reproduce changed-file compilation: `XNU_CC_OBJDIR="$PWD/research/early-objs" python3 tools/xnu-cc.py research/run13.log research/bt13 arm_init.c arm_vm_init.c kern/debug.c arm64/start.s osfmk/arm64/sweet_early.c --per-file` (create the output directory first). The helper now accepts explicit new source paths absent from the old artifact's Makefiles and rejects empty selections.
- Device command result: `adb reboot bootloader`, then `timeout 30s fastboot boot shim/out/shim-boot-0010.img`: send OKAY (16028 KB), boot OKAY, total 0.541s. This confirms bootloader acceptance only, not XNU progress.
- The successful boot above was on 2026-10-14. On 2026-10-15, `timeout 45s fastboot boot ...` timed out waiting for a device; no image was sent. Boot image SHA256 rechecked and unchanged. No new build is needed to repeat the trial.
- Earlier retry: `timeout 90s fastboot boot shim/out/shim-boot-0010.img` timed out (exit 124). This is superseded by the successful 2026-10-15 repeat boot recorded above; do not repeat it until the user reports the screen.
- User observation confirms MMU-on C entry, platform expert, CPU topology/bootstrap, startup bootstrap and cpu_init all complete. Failure is within arm_vm_physmap_init (non-XNU_MONITOR branch), before stage 8 / TTBR0 teardown. Old red shim text remains behind the early console; this is expected because only written rows are cleared.
- New edit/compile sandbox is `research/bt14/xnu` (extracted artifact, NO nested .git; `git diff` there would act on the parent project). Use a saved baseline file / generated unified diff, or explicitly initialize a local baseline before editing. `research/bt13/xnu` does have its own baseline git repo.
- Exact user-reported panic: `arm_vm_init.c:1606 Assertion failed: (temp_ptov_table[ptov_index - 1].va + temp_ptov_table[ptov_index - 1].len) <= physmap_end`.
- Root cause: MacOSX build sets `ARM_LARGE_MEMORY=1`; `XNU_MONITOR` is off. Block alignment in arm_vm_physmap_slide can add gaps, but the non-PPL large-memory physmap_end omitted the padding already present in the small-memory branch. Patch 0011 reserves PTOV_TABLE_SIZE*ARM_TT_TWIG_SIZE (8*32MB) in both the aperture bound and its L1 allocation; monitor/PPL builds retain zero padding. The assertion is preserved.
- Validation: `arm_vm_init.c` compiled to an arm64 object using `research/run14.log` + `research/bt14` (object in `research/physmap-objs`). All 11 patches apply in CI order and produce exactly that source. Host harness `research/physmap-check.c` extracts the real XNU slide function with page-table-write stubs: all 65,536 page-aligned slides within 1GB checked against the current kernel memory layout; old bound fails 65,504 cases, padded bound fails zero; worst overrun 0x1ffc000 bytes. Baseline source saved as `research/arm_vm_init.pre0011.c`.
- CI: https://github.com/dipa-studio/ios-sweet/actions/runs/38638702083 (success; artifacts and full log downloaded).
- New image: `shim/out/shim-boot-0010.img` (16,412,672 bytes, SHA256 `ed2c270e0081bad5ff517be415f9bfe8805463aea7866732203fa97ac737e64e`). Previous image preserved as `shim/out/shim-boot-pre0010.img`.
- New kernel SHA256: `3ee05270cc291c49589a101678f904b1b69cb2f2575e05398bce8a4e052f409a`. Artifact checksums passed; arm64 (not arm64e), early-console symbols present. Payload entry VA `0xfffffe000746a488` -> PA `0xb146a488`; kernel end PA `0xb1ff4000`. Command line remains `debug=0xc serial=3 cpus=1 keepsyms=1`.

### Patch 0010 screen legend
- Bottom-left white 64x32 tile: assembly entered `start_first_cpu`, before page tables/MMU.
- Text `SWEET EARLY 1`: entered `arm_init` with MMU on; 2: platform expert done; 3: CPU topology done; 4: CPU bootstrap done; 5: startup bootstrap done; 6: CPU init done; 7: entering `arm_vm_init`; 8: leaving bootstrap TTBR0.
- `SWEET EARLY PANIC:` prints a copy of panic arguments before normal panic handling needs per-CPU/thread state.
- In patches 0010/0011 the console disabled before TTBR0 invalidation; patch 0012 replaces that with a persistent kernel VA alias and diagnostics through normal serial/kprintf startup (see its legend above).
- Screen contents require a physical observation from the user: adb cannot capture a framebuffer after Android has been replaced by a bare-metal kernel.

## QEMU emulation (2026-10-15)
- `tools/mkadt.py OUT.adt --qemu` = same ADT with QEMU virt GICD 0x08000000 / GICR 0x080a0000 / CNTFRQ 62.5 MHz.
- `tools/qemu-sweet.py PAYLOAD OUTDIR [--secs N] [--hmp "x /8gx ADDR"] [--gdb]`: host-side copy of shim/loader.c
  (segments + ADT + boot_args at their PAs, 6-instruction stub sets x0 and jumps), `-M virt,gic-version=3 -cpu cortex-a76`
  (same ID_AA64MMFR0 as Kryo 470), 4G RAM so 0x9c000000 fb and 0xb0000000 kernel are plain RAM.
  Outputs `fb.png` (the screen), `regs.txt`, `qemu.log` (exceptions with ESR/FAR/ELR). `--gdb` halts with a stub on :1234
  (system `gdb` + `set architecture aarch64`, `hbreak *VA` works with the MMU on).
- Not emulated: Qualcomm XPUs, ABL, real panel, PSCI conduit (QEMU virt uses hvc). Hardware still decides those.
- Example: `python3 tools/mkadt.py /tmp/q.adt --qemu && python3 tools/mkpayload.py xnu/out-0013/kernel.development.sweet /tmp/q.adt /tmp/pq.bin --cmdline 'debug=0xc serial=3 cpus=1 keepsyms=1 -enable_kprintf_spam' && python3 tools/qemu-sweet.py /tmp/pq.bin /tmp/q`

## Layout
- `backup/`  partition dumps + full sdb..sdf LUNs, `SHA256SUMS` (all verified on-device == local)
- `dtb/`     live FDT (from OrangeFox), PixelOS boot.img dtb, dtbo, dts versions
- `shim/`    bare-metal boot shim (`./build.sh` -> `out/shim-boot.img`)
- `research/` mainline sm7150 dts, XNU pe_fiq.c etc, PocketDarwin patches
- `tools/unpack_bootv2.py`

## Device access
- No root in PixelOS 17 (user build, adb root disabled). Root = `fastboot boot recovery/recovery.img` (OrangeFox R12.0_2, temp boot, not flashed).
- `fastboot boot` works for stock boot.img, OrangeFox, and our shim.
- Shim resets itself via PSCI SYSTEM_RESET; IMEM restart_reason 0x77665500 is seen
  (bootreason=bootloader) but ABL still boots Android, so it does not stop in fastboot.

## Hardware facts (live DT + shim measurements)
- Framebuffer (ABL cont splash): 0x9c000000, 1080x2400, stride 4320, a8r8g8b8, panel is DSC *video* mode (no kick needed).
- RAM: 0x80000000+2G, 0x100000000+0xfcc00000. Live reserved-memory = PixelOS base dtb + sweet dtbo fixups.
- GICv3: GICD 0x17a00000, GICR 0x17a60000 (stride 0x20000, 8 PEs). GICD_TYPER 0x007B041D: SecurityExtn=1 (DS=0).
  ABL leaves GICD_CTLR = 0x10 (ARE_NS on, groups off). Writing 0x13 reads back 0x12: EnableGrp1A (bit1) is the one that matters.
- GIC Group 1 VERIFIED (shim 2c): vtimer INTID 19 = 30 IRQs/300ms, ptimer INTID 18 = 30, SGI 1 to self = 10/10.
  ICC_SRE=1 already, ICC_CTLR 0x8440, priority/enable writes stick. GICR_IGROUPR0 and GICD_IGROUPRn read 0 from NS
  even though Group 1 delivery works (RAZ in NS view) - do not use them as a health check.
  INTID 28 shows pending constantly (unknown PPI 12).
- Timer 19.2 MHz. Qualcomm PPI numbering: secure-phys/phys/virt/hyp = PPI 1/2/3/0 -> vtimer INTID 19, ptimer 18 (NOT 27/30).
- PSCI 1.1 via SMC, SMCCC 1.1. CPU_ON ok; SYSTEM_SUSPEND and SYSTEM_RESET2 unsupported.
- SMP: CPU_ON works for all 7 secondaries (MPIDR 0x81000n00).
- Entry EL1, MMU off, x0 = DTB (magic ok). ID_AA64MMFR0 = ...101122: 16K granule YES, 4K YES.
- No serial console: debug UART SE is in SPI mode on sweet. Screen is the only debug channel.

## XNU implications
- XNU GICv3 path (pexpert/arm/pe_fiq.c, VMAPPLE) puts the timer (PPI 27) in Group 0 = FIQ. With SecurityExtn=1,
  Group 0 is secure -> impossible from NS EL1. Need: Group 1 IRQ, ICC_IGRPEN1, INTID 19, and the timer handled in the IRQ path.
- XNU VMAPPLE PSCI uses `hvc`; sweet needs `smc`.
- PocketDarwin NonAppleGenericCpu.patch only swaps -mcpu=apple-h7 for -march=armv8-a.

## Milestone 3 (2026-10-14): 16K MMU verified
- ABL loads the Image at 0x80080000 (base 0x80000000 + 0x80000) regardless of text_offset=0.
- 16K granule, T0SZ=28 (L2 start, 32MB blocks), MAIR 0x44ff00, TCR 0x1409CB51C, PARange=2 (40-bit PA).
- Only own image pages WB (Qualcomm XPUs: never map carve-outs cacheable); fb Normal-NC; rest Device.
- AT S1E1R checks all as expected; unmapped -> translation fault L2.
- Fill fb: 110 ms (MMU off) -> 3.5 ms (NC). Memory loop 70 ms -> 0.7 ms. vtimer + SGI IRQs still fine with MMU on.

## XNU loader design notes (xnu-8796)
- Entry: `_start` -> `start_first_cpu`, x0 = boot_args (PA), MMU off, EL1. boot_args: Revision/Version 2,
  virtBase/physBase/memSize/topOfKernelData, Boot_Video (fb 0x9c000000, rowBytes 4320, 1080x2400, depth 32),
  deviceTreeP/Length (ADT), CommandLine[608], bootFlags, memSizeActual.
- start.s maps [kernel mach header .. physBase+memSize) with cacheable BLOCKS. On Qualcomm every XPU carve-out
  must therefore lie below the kernel: use physBase = 0xb0000000 (above ramdump_fb 0xaf000000+16M,
  cdsp_sec, qseecom), end before rmtfs 0xfde01000 -> memSize ~0x4d000000 for bring-up.
- Base ADT: iPhone 8 d20ap DeviceTree from iOS 16.7.16 IPSW (tools/remotezip.py + tools/adt.py; LZFSE payload).
  Template values are empty: the loader must fill chosen/*, memory-map, cpu*/reg etc. like iBoot.
- XNU build: GitHub Actions (dipa-studio/ios-sweet, xnu.yml) via blacktop/darwin-xnu-build, MACOS_VERSION=13.5.
  New-clang fixes in xnu/patches; Xcode 16 iig is incompatible (IORPC.kernelContent) -> macos-14 runner, oldest Xcode.

## Kernel architecture plan (SWEET machine config)
- First stock build (VMAPPLE) is arm64e (PAC). Kryo 470 = ARMv8.2, no PAC -> SWEET must build plain arm64
  (HAS_APPLE_PAC is only defined for __arm64e__, so arm64 drops PAC automatically).
- Template: VMAPPLE (16K pages, GICv3 code in pe_fiq.c) minus APPLEVIRTUALPLATFORM hypercalls/paravirt PAC,
  plus BCM2837 (generic ARM: no APPLE_ARM64_ARCH_FAMILY Apple sysregs). Do not link the KDK lib<cfg>.os.*.a.
- Timer: XNU expects it on FIQ (sleh_fiq -> rtclock_intr). SWEET: GIC Group 1, so sleh_irq must ack ICC_IAR1,
  route INTID 19 to the same timer path, SGIs to cpu_signal_handler, EOI via ICC_EOIR1.
- SMP/interrupts: open-source AppleARMSMP (USE_APPLEARMSMP) needs an IOInterruptController (AIC role) and an
  IOPMGR (CPU power -> PSCI CPU_ON via SMC). Plan: built-in IOKit classes (SweetGIC, SweetPMGR, platform
  expert) compiled into the kernel and matched via iokit/KernelConfigTables.cpp -> no closed kexts needed.
- Debug: xnu patch 0003 sweet-fbcon = kprintf drawn on the framebuffer (ADT node "sweet-fbcon").
- ADT /arm-io ranges must not map to parent 0 (pe_arm_get_soc_base_phys()==0 disables serial): use parent 0x1000000.

## Status 2026-10-14 late: first XNU boot attempt
- SWEET kernel builds (CI run 38635343732, patches 0001-0009). Verified offline: arm64, no PAC, no >v8.2 code,
  70300 classic relocs all in range (slide 0 = no loader work), entry = __start.
- Boot: shim loader worked (initrd 0x846F0000-0x855FE3E0, BOOTARG 0xB1FF8000, JUMP 0xB146A488) but screen stayed
  red -> xnu died/hung before serial_init (fbcon). kprintf is a no-op before STARTUP_SUB_KPRINTF.
- Historical next-step plan (patch 0010, now implemented and built; see active handoff above): early fb debug channel
  1. start.s start_first_cpu (after mov x20,x0 / mov x21,#0): PA marker band (MMU off, direct store to 0x9c000000).
  2. start.s after both create_bootstrap_mapping calls: add ONE block entry to the existing V=P L2 table
     (x25 + 2*PGBYTES; do NOT call create_bootstrap_mapping again: fb and RAM share L1 entry 0, it would replace
     the L2 table). Entry = TYPE_BLOCK|VALID|SH(OUTER)|ATTRINDX(CACHE_ATTRINDX_WRITECOMB=1)|AF|PNX|NX|0x9c000000,
     index = (va & ARM_TT_L2_INDEX_MASK) >> ARM_TT_L2_SHIFT.
  3. new osfmk/arm64/sweet_early.c (+files.arm64 entry): sweet_early_mark(n) colored bands at screen bottom and
     sweet_early_putc using iso_font via VA=PA while the bootstrap TTBR0 is live; disable before
     arm_vm_init's set_mmu_ttb(invalid_ttep) (arm_vm_init.c:2148).
  4. markers in arm_init after PE_init_platform, ml_parse_cpu_topology, cpu_bootstrap, kernel_startup_bootstrap,
     cpu_init, before arm_vm_init.
  5. panic hook at top of panic_trap_to_debugger: va_copy + _doprnt(fmt, &copy, sweet_early_putc, 16).
  Verify with tools/xnu-cc.py (compile+symbols) and patch-order simulation before the single CI run.
## Active A03 handoff — 2026-11-21

GPU acceleration remains disabled by default after BOOT0125 reached a
stage-5 cached CLEAN_INV timeout during sustained compositor copies. Added
candidate patch xnu/a03/0214-a03-gpu-clean-completion-window.patch, which
extends the completion poll window before quarantining retained mappings.
Host check tools/a03-test-gpu-clean-retry.py passes. No CI or hardware
validation has been run for 0214. Next authorized step is a BOOT-only CI
build and trial, preserving recovery, bootloaders, EFS/NV and USERDATA.
CI44957509219 completed successfully with userspace staging disabled. The
corrected userspace-enabled run is CI44958900136 from the same source.
