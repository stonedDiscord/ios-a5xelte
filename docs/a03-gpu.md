# A03 GPU acceleration bring-up

## Active checkpoint — November 21, 2026

BOOT0123 failed sustained compositor activity after2041completedGPUcopies.
One Home wake generated1388newGPUframes after diagnostic copies, then the
retirement guard quarantined scratch/source mappings and suppressed panel
writes. This supersedes earlier static-stress/idle-cycle passes as evidence of
sustained UI reliability. The failure is GPU quarantine, distinct from earlier
idle display-sleep episodes. Exact failing stage was not yet logged.

CPU-control BOOT0124 uses the same validated kernel with a03gpu=1 removed.
BOOT0125/CI44856061555 adds read-only failure-stage/register diagnostics without
changing retirement/cache timeouts, quarantine or reset behavior. Its sustained
trial reached10025actualcompositorcopies without recurrence; subsequent requested
and background full readbacks also passed. It is left GPUOFF pending root cause.
No failure snapshot appeared, so the earlier intermittent failure remains unresolved.
The goal remains incomplete. Source rendering remains CPU-only; full Metal/EAGL
is deferred under the requested basic milestone. Earlier paired tests prove CPU
offload, not sustained physical acceptance or faster animation.

The following optimization table and dated checkpoints are historical evidence;
use the latest A03_PROGRESS.md and NOTES.md for running-device state.

| Controlled test | GPU median | Result |
| --- | --- | --- |
| BOOT0114 tile rows4/8/16/32 |2.186 /2.205 /2.208 /2.255ms| Larger tiles do not help |
| BOOT0115 impldef/cacheall/writealloc |2.214 /2.191 /2.325ms| Retain default impldef |
| BOOT0116 clock384/512MHz |2.193 /2.128ms| Small clock effect |
| BOOT0117 clean-only CPU source,384/512MHz |2.202 /2.126ms| No measured latency gain |
| BOOT0118 native16K mapping validation,384/512MHz |2.056 /1.983ms| Setup reduced; still above CPU |
| BOOT0119 single verified endclean,384/512MHz |2.042 /1.969ms| CPU medians1.677 /1.665ms |

Each accepted comparison uses four fresh full-frame readbacks and three
alternating eight-copy CPU/GPU rounds. The first BOOT0118 512MHz run was
rejected for extra background CPU copies;1.983ms is the uncontaminated retry.
These are historical synchronous copy timings, not animation FPS. All accepted
trials have zero fallbacks/quarantine. Before0190 they used explicit cached/warm
operation with GPUOFF between trials; BOOT0123 uses the opt-in policy above.

0187 passes hardware full readback and paired timings in BOOT0119. Cached
framebuffer jobs omit the duplicate automatic end flush while preserving start
invalidation and the independently acknowledged GPU CLEAN_INV after slot
retirement. CPU readback, AS disable, fallback and shutdown remain after that
completion. The source read-only mapping is cleaned to PoC; descriptor/job
flushes remain. The last512MHz attempt measured1.309ms execution,0.392ms
source/descriptor cache preparation and0.094ms mapping setup. GPU512MHz
was18.3% slower than its pairedCPU median, so BOOT0119 was left OFF.
See A03_PROGRESS.md and NOTES.md for the current reader, image hashes and
unfinished physical UI/performance gates.

BOOT0120 / CI44844162892 / cc4576ae adds explicit counter-bounded polling.
Fresh full-frame readbacks pass for both polling policies at both rates. At
384MHz, wait/spin GPU medians are 2.035/2.030ms; at512MHz they are1.965/1.962ms.
These differences do not establish a useful gain. The first attempt at each rate
was rejected for background copies; accepted retries retain exact counts.
Keep default pollwait: existing XNU already initializes a periodic WFE event
stream, and these results do not establish a WFE bug. BOOT0120 was left OFF.

0189 added submitting-thread CPU-runtime counters alongside wall time. Its
subsequent BOOT0121 validation follows; these counters do not measure total
system CPU or source rendering.

BOOT0121 / CI44846854268 /3d14c72 now measures submitting-thread CPU
runtime as well as elapsed copy time. In the repeated full comparison:

| Rate | CPU wall | GPU wall | CPU submitter | GPU submitter |
| --- | --- | --- | --- | --- |
|384MHz|1.396ms|2.028ms|1.397ms|0.843ms|
|512MHz|1.402ms|1.974ms|1.403ms|0.813ms|

That is39.7/42.1% less submitting-thread CPU time, with higher elapsed latency.
This establishes copy offload, not faster animation, total-system CPU reduction
or GPU source rendering. Both policies passed fresh full pixel readbacks and
three paired eight-copy rounds, with zero fallback/quarantine. An earlier valid
trial had a final host-report serialization error after restoration;3df1c3a fixes
that key and adds a full-success regression. The complete retry emits valid JSON.
At that checkpoint physical acceptance and deployment policy remained pending;
BOOT0122/0123 validate deployment below. Physical acceptance is still pending.

BOOT0122 / CI44849933946 attempt2 /e8306f9 validates automatic startup via
a03gpu=1: the first compositor frames activate cached/warm384MHz/defaultwait,
four full readbacks pass before a fast frame, and the log verifier confirms no
prior host GPU controls or replays. One Home press followed the observed idle
power-down request. This is host-command independence with USB connected;
physically unplugged boot and visible UI correctness remain unverified.
Its512-copy stress passes with four final readbacks, wall1.989ms and submitting
thread0.832ms per copy, zero fallback/quarantine. Warm power remains on during
idle, so BOOT0122 was left OFF pending0191 hardware validation. BOOT0123
uses the existing serialized vsync timer to release
retired owned GPU power after100ms; it never powers down quarantined DMA.

BOOT0123 / CI44853265071 /bc4137c validates0191 automatic idle release.
Automatic startup again passes four full readbacks before fast frames, without
host GPU controls/replay. Twelve cycles observe powered0 before each resumed
GPU copy; cold copies take about2.50-2.69ms. A512-copy stress plus four final
full readbacks passes, zero fallback/quarantine, meanwall2.055ms and submitting
threadCPU0.844ms. Read-only final status is enabled1/powered0,82idle releases,
561completed/8verified, default384MHz/pollwait/impldef0/tile4/cachedwarm1.

The experimental opt-in is a03gpu=1 in the BOOT payload. Sustained0123 failure
means it is not a validated normal deployment. Without it,
GPU copy defaults OFF; an explicit control overrides boot initialization.
An existing vsync timer releases only retired owned power after100ms idle;
quarantined DMA is never powered down. The next frame uses the checked cold
start and retains qualification. The kernel source is unchanged by host controls;
remove a03gpu=1 or issue gpu blit off to select CPU copying. This is framebuffer
copy offload, not Metal/EAGL rendering or a demonstrated animation-FPS gain.
Physical swipe/image acceptance and an unplugged reboot remain unverified.
Touch RAM firmware still requires the existing host restoration after reboot.

Use the existing single-reader log with these bounded comparison tools:

    python3 tools/a03-gpu-tile-benchmark.py --log LOG
    python3 tools/a03-gpu-memattr-benchmark.py --log LOG
    python3 tools/a03-gpu-rate-benchmark.py --log LOG

They qualify policies and restore the original mode, refusing faults, incomplete
replays, changed policies, mixed CPU/GPU intervals or background copies.
The kernel's read-only status may be retried on a completed empty busy reply;
a replay is never resent automatically.

0181 observes raw display-power requests:1 ->0 around idle cessation, then
Home ->1 followed by CPU frames. Sleep is a likely explanation for that stale
clock episode. Panel blanking and completed power transitions remain
unimplemented/unproven; PosterBoard crashes are a separate known issue.

The following dated checkpoints are retained as bring-up history.

## Cached hardware checkpoint and remaining work

BOOT0107 from CI44791438428 (7e56be7) passes repeated full-frame pixel
readback with cached GPU mappings and explicit clean/invalidate completion.
The eight-copy fast mean is 6.170 ms, versus 142.160 ms with uncached
mappings on BOOT0106. CPU replay copies still take 1.673 ms. This proves
a large improvement to the GPU path; it does not yet prove acceleration
over the CPU backend or sustained physical UI reliability.

Phase measurements place about 137 ms of the uncached path in execution,
with CPU cache maintenance, page-table preparation and power transitions
each below 1 ms. Cached execution falls to about 4.277 ms; total copy
latency still includes mapping, power-up/shutdown and completion.
Full CPU pixel verification is a separate, expensive bring-up check.

The explicit `gpu blit cached` / `gpu blit uncached` policy defaults to
uncached and resets four-frame pixel qualification when changed. Cached
descriptor, code and pixel mappings use the pinned vendor's AttrIndex0;
page-table walks use writeback/read-allocate policy. Source CPU flushing
is preserved. After slot retirement, a fresh GPU clean-and-invalidate
completion is mandatory before readback, AS disable, CPU fallback or core
shutdown. A timeout, stale completion, reset or fault quarantines retained
memory and the IOSurface. Host tests hide dirty GPU writes until completion.

Candidate0175 copies four pixels per thread using native 128-bit loads and
stores, with exact bounds and scalar tails. The pinned Mesa compiler
reproduces its 640-byte binary, 32 registers, no TLS/WLS and X/Y preloads.
Primary v9 descriptor checks and source lifecycle tests cover offsets,
all tail lengths across group boundaries, noncontiguous pages and cache
failure quarantine. CI44794488664 builds 734646c; hardware validation is
still required. The running phone is left in CPU-copy mode while building.

A stale clock on BOOT0106 was a stopped display image: kernel UTC matched
the host. GPU OFF plus one Home press resumed thousands of CPU frame
copies, and the user confirmed the clock updated. Later physical input
resumed CPU frames after idle without another Home. This combined wake
does not isolate the cause or establish a permanent freeze fix.

## Current measurement, 2026-11-20

BOOT0104 includes the bounded accepted-compositor-frame replay command.
Four initial full-frame replays each passed all 1,152,000 source/destination
pixel comparisons. The first eight-copy measurements were 139.006 ms per
fast GPU copy, 211.630 ms with full readback, and 1.665 ms for CPU copies.
Repeated baseline rounds measured fast GPU 138.140/138.472 ms and CPU
2.172/1.717 ms. No fallback or quarantine occurred. These measurements
include synchronous scheduling, mapping, cache and power overhead; they
measure copies, not visible animation FPS. The existing path is slower than
CPU copies, so hardware execution alone does not complete acceleration.

Candidate0172 changes the shader from one-thread groups to 16x4 groups,
reducing full-frame workgroups from 1,152,000 to 18,000. Exact width/height
checks mask padded edge lanes before memory access. The native Mesa24.3
compiler reproduces the 256-byte shader, with no TLS/WLS, 32 registers and
global X/Y preloads. Primary v9 packers match with C assertions explicitly
enabled; a negative fixture confirms a mismatched group descriptor fails.
Host lifecycle tests cover padded groups, clipped/offset and noncontiguous
sources, retirement, faults and quarantine. CI44784844777 builds exact
3c22c827b79fe88723cbb638439349c3b6af1071. Hardware correctness and a
repeated latency comparison remain required before enabling it as normal
operation. Physical UI acceptance remains separate.

Reproduce the shader using an existing pinned Mesa24.3 native build:

```sh
python3 tools/a03-build-g57-copy-shader.py MESA_BUILD NEW_OUTPUT_DIR --blit
python3 tools/a03-test-gpu-blit-layout.py --mesa-build MESA_BUILD
```

With a single existing console reader and an accepted compositor frame,
run `tools/a03-gpu-blit-benchmark.py --log LOG --mode cpu --replay 8`,
then repeat for `verify` and `fast`. The helper restores the original
enable/readback policy after each measurement. Fast mode still requires
four successful full-readback frames first. Replays are diagnostic copies
of an accepted frame, not evidence of new physical UI input or animation.

## Earlier framebuffer checkpoint

BOOT0101 now copies actual IOSurface content into panel memory with the
native G57 compute shader. Four full720x1600 BGRA frames each pass
1152000-pixel source/destination readback with zero mismatches, done1 and
retired1. Counter: frames4/pixels4608000/fallbacks0/quarantined0.

CI44625038530 at74e1def, exact uploaded sources/checksums and BOOT-only
deployment are verified. Source rendering remains on the CPU; no Metal/EAGL
implementation exists. Full readback is enabled for bring-up; speedup is
unmeasured. Hardware CPU fallback also copied28 frames with GPU disabled, then GPU mode
was restored. Physical UI acceptance and latency measurements remain
pending before declaring the basic acceleration goal complete.

## Hardware passive result, 2026-11-19

BOOT0095 from successful CI44409726184/exact15b1445 passed artifact checksum,
uploaded-source reverse-apply, linked marker and host sanitizer checks, then
flashed to boot only. Exact live gpu transaction returns PMU force00010102,
state07000000, AON enable002bcac1: core0 state7/top0 and bus bit11 enabled.
The guard stops before mapping GPU/APB. GPU_ID is still unmeasured. No power
writes, jobs, pixels or acceleration are established. Next GPU gate is a
source-validated power/voltage/clock sequence; a DMA blit is a separate path.

## Hardware evidence and sources

The private live A03 DT identifies /soc/mm/gpu@23100000 as sprd,mali-natt:
GPU 0x23100000/0x100000; GPU APB 0x23000000/0x3000; GPU DVFS APB
0x23014000/0x3000. JOB/MMU/GPU all name SPI60 (GIC INTID92), a shared
interrupt; do not copy Exynos interrupt numbers. The clock gates are core
APB+4 bit0, memory APB+8 bit0 and system APB+12 bit0. The parent bus gate
is AON 0x64000000 bit11. PMU 0x64020000+0x2c4 bit25 is top force shutdown;
PMU+0x500 bits28:24 describe GPU core0 state and bits20:16 GPU top state.
Bit24 of the force register enables auto shutdown, also rejected by the probe.
Addresses/masks come from live DT plus the reviewed register/clock sources
below. The marketing GPU identity still needs an actual GPU_ID read.

Reviewed implementation reference (same ums9230/qogirl6 family, different
phone; not automatic proof of A03 behavior):
realme-kernel-opensource/realme_C31_C35_narzo50A-Prime-AndroidR-kernel-source
commit79c7c8b238a20393a78ee5f1110991bd4280e143:

- drivers/clk/sprd/ums9230-clk.c (gate bits and clock parent/divider layout)
- drivers/kernel_modules/gpu/natt/mali/platform/qogirl6/mali_kbase_config_qogirl6.c
  (power then source/bus/core/memory/system clocks, bin-specific DVFS and QoS)
- drivers/kernel_modules/gpu/natt/mali/platform/qogirl6/gpu,qogirl6-{regs,mask}.h
- drivers/kernel_modules/gpu/natt/mali/gpu/mali_kbase_gpu_regmap_uapi.h
  (read-only GPU_ID/status/core-present offsets)

Stock live DT regulator/DVFS binning must govern any future active power-on.
Do not copy the Exynos T720/T880 power sequence or its job descriptors into
this device. Existing gpu/mesa and gpu/eagl code is donor-specific and has
not been adapted or installed for A03.

## 0162 passive candidate

Adds an explicit gpu command to the existing a03_probe=1 live worker.
No startup call, register writes, reset, power-on, clock/DVFS change, GPU IRQ,
page table, job, user client or compositor change. The command first reads
PMU/AON; a closed power/bus gate or enabled auto shutdown stops before mapping
APB or GPU. Closed core/memory/system gates stop before mapping GPU. PMU/AON are checked again
before the GPU read. If readable, logs raw GPU_ID, status and core-present
masks. Zero/all-ones ID stops further GPU reads. Permanent mappings are
reused by the single worker, matching existing A03 drivers; never unmap an
ml_io_map mapping. This is a staged probe, not acceleration.

Actual source host tests cover gate combinations, each missing clock,
map failures/reuse, invalid IDs and unchanged fake register banks under
ASan/UBSan. Actual BSD compile commands from0094 compile a03_gpu.c and
sweet_amfi.c with generated CI headers; no builtin substitutions. Full
Xcode link and hardware execution remain separate gates.

## Current requested milestone

User clarified on2026-11-18 that the most basic acceleration is sufficient.
Target a verified hardware fill/copy and then a framebuffer blit with CPU
fallback. Full Metal/EAGL rendering is deferred. A diagnostic register read
still does not meet this smaller milestone. Consider the A03 2D/DMA engines
only with separately validated ownership, address translation and completion.

## Acceptance order

1. BOOT-only passive probe; retain0094/0093 restores and continuous touch.
2. If GPU is off, implement validated power/voltage/bus/clock sequencing,
   bounded waits and fault snapshots; then verify actual GPU_ID.
3. Driver-owned private GPU mappings and one completed offscreen job, with
   actual pixel readback and fault checks. A register read is not rendering.
4. IOSurface import, cache maintenance, fences and a guarded hardware copy
   to framebuffer with CPU fallback. Full EAGL/Metal remains deferred.
5. Verify repeated physical UI frames use that copy backend and measure latency.
   A private clear or software Mesa renderer does not satisfy this goal.

## Userspace audit on 2026-11-18

The existing gpu/mesa/herodrm.c opens the HeroGPU service. Its parameter
bridge expects HeroGPU scalar selectors and returns that device's GPU ID,
shader/tiler/L2/AS/job-slot masks and texture/thread limits to Panfrost.
A03 currently publishes no HeroGPU service or equivalent buffer/job API.
The existing Mesa target first tries hardware then selects softpipe (with a stderr message)
when unavailable. An OSMesa/EAGL test merely creating a context is therefore
insufficient evidence: retain the actual renderer string and prove completed
hardware jobs. Do not install these S7 libraries to claim A03 acceleration.
The A03 bridge must also handle XNU16KiB pages versus GPU page-table geometry,
IOSurface lifetimes, per-client isolation and synchronization.

## Power and clock preflight0163 (2026-11-19)

User directs power/clock setup first. Review found0162 conflates shader C0
power (PMU state bits28:24) with GPU top-domain power (bits20:16). The Mali
platform sequence powers top and enables clocks before kbase powers shader
cores.0163 gates register access on top only; a sleeping shader alone is not
evidence that the control aperture is inaccessible. Source-based correction
pending hardware verification, not a GPU_ID claim.

Explicit gpu power observes SC2730 DCDC_GPU via existing bounded ADI:
POWER_PD_SW181c bit3, VOL1854 bits8:0 x3125uV. Live DT marks the rail
always-on and lowest OPP384MHz/700mV. Reject disabled supply or inherited
voltage outside700-800mV; never write PMIC. Runtime ADI reads and Download
reset share atomic ownership; startup USB supply precedes both workers.

Sequence: reject auto-shutdown ownership, clear only PMU2c4 FORCE bit25 if
needed, wait300us then poll top state up to2000us, enable AON bus bit11 if
needed, capture inherited APB core/mem/sys and QoS, GPU DVFS index/idle/map0/
update/bypass/voltage/clock/state and topDVFS MM control/tuning. A top timeout
restores only a force bit this command cleared and never accesses APB/GPU.
Leaf clock gates, rate selectors/dividers, PLLs, voltage votes, QoS and jobs
remain unchanged until inherited states are validated.0163 implements top
power setup and clock preflight, not complete clock setup or acceleration.
The passive gpu command remains write-free.

References: native Samsung kernel checkout b48e9dd (clock driver, SC2730
regulator, qogirl6 headers), vendor79c7c8b above (platform sequence/GPU DVFS
register map). Vendor T606 table removes768MHz and retunes GPLL to650MHz;
do not copy generic850MHz. Index0 uses384MHz/700mV without high-bin voltage
map changes. Hardware DVFS ownership/rail/clocks require BOOT-only trial.

The0163 host harness exhausts all2048 shader/top/bus combinations against
actual passive code and checks every fake register bank remains unchanged.
It also covers supply selector bounds, top timeout/force restore, missing
sharedtopDVFS clock, map failures and shared runtimeADI exclusion. These
checks prove software guards under the model, not electrical behavior.

## BOOT0096 hardware and0164 inherited-clock candidate

Actual SC2730 selector0140 reads1.0V;0163 power command refuses it and
makes no power/clock writes. Separate passive GPU probe confirms top on,
shader asleep and APB core10/mem10/sys30: all leaf gates off. ActualGPU_ID
still unmeasured. Touch firmware/continuous forwarding restored after reboot.

0164 adds explicit gpu clocks. It accepts only the exact inherited1V rail,
already-on top/bus, three closed leaf gates and measured parent/dividers.
Native ums9230 clock source defines selector1 asTWPLL/4, core/memdivide1,
sysdivide4. ReadonlyTWPLL config is decoded using nativePLL fields; require
lockbit18 and parent near1536MHz. Enable only core/mem/sysbit0 in vendor
order, wait400us, recheckdomain, readGPU_ID. InvalidID/mapfailure restores
ownedleafgates. No voltage/rate/PLL/DVFS/job writes. It preserves inherited
1V for this bounded bringup stage; it does not establish1V as the correct
runtimeOPP. FullCI and hardware verification remain required.

## BOOT0097 hardware milestone

Explicit gpu clocks enabled APBcore/mem/sys bit0:10/10/30 ->11/11/31.
Actual GPU_ID90910010/status100, shader/tiler/L2present1 (highmasks0).
TWPLL registers0004077b/1d89d89d/0003c005 decode1535999998Hz; CGM1003.
This proves clock gating/control register access, not jobs or acceleration.
NoPLL/rate/voltage/DVFS writes. Next power step follows pinned vendor
backend/gpu/mali_kbase_pm_driver.c: before each power-on PWR_KEY050 gets
2968a819, PWR_OVERRIDE1 at058 getsF01E0078; tiler power brings firstL2,
waittiler+L2, then shader power and120us delay. Needboundedhardwarevalidation
and ownership/rollback before job submission. Do not reuse donor PMIC/MMIO.

##0165 core-power cycle candidate

Explicit gpu cores validates measuredID90910010, one-core masks, exact
inherited1V/top/bus/clockstate, no inheritedready/transitions and noGPUfault.
VendorPWRKEY/OVERRIDE precede TILERon; firstL2 follows tiler automatically.
Waittiler/L2, thenSHADERon+120us. Bounded20ms polls; shutdownshaderfirst,
thenTILER/L2; restore prioroverride only after allready/transitionsdrain.
Timeoutstillrequests shutdown. NoMMU/jobs/IRQ configuration or startupcall.
Actualsource statefulfakeMMIO tests and ARM64compile pass; hardware pending.

## Private job layout preparation (host only)

The shared host header tools/a03-gpu-job-layout.h prepares32KiB owned
scratch: four4KiB GPU page tables, one descriptor page, one output page.
The ARM64 host remains16KiB; physical allocations must be16KiB aligned
and verified contiguous before this builder is used. No fixed physical
scratch address or reserved carveout is assumed. Only GPUVA02000000 job
and02001000 output map; page-table pages themselves are inaccessible via
GPUVA. AArch64 descriptors useAF/RW/AttrIndex5(normalNC)/NX. Invalidentries2.

Sources: pinned vendor mmu/mali_kbase_mmu_mode_aarch64.c and
mmu/backend/mali_kbase_mmu_jm.c; Mesa mesa-24.3.0 src/panfrost/lib/genxml/v7.xml
Job Header/Write Value Job Payload (header32bytes, type2/index1, payload
address32,type40,immediate64value48). Header is a byte-layout builder only,
not a driver and not staged in kernel. Hostsanitizer pagewalk verifies1024
physical bases above4GiB, invalidneighbors, exact jobbytes/canary andbounds.
No hardware MMU mapping or job was submitted. Core power hardware gate
and runtime ownership/cache/completion/retirement still must be satisfied.

Measured90910010 matches Mesa mesa-24.3.0 pan_props.c product9091=G57/TNAx.
Vendor gpu_id.h calls modelTNAX. Revision low0010 isr0p1, whose pinned
issue list omitsTTRX3485 (r0p0 needs dummy-job workaround); do not assume
all Valhall revisions need the private valhall-1691526 blob. Shader quirks
and full render jobs still require their own validation. Primary XML field
correspondence is optionally tested with --mesa-xml PRIVATE/v7.xml.

##0166 private WRITE_VALUE job candidate

Explicit gpu job extends the hardwarevalidated corecycle with owned32KiB
contiguous scratch and AArch644KiBtables. Verifyeachgranule/endphysical,
normalNCGPUdata+explicitCPUcacheflush, AS0/JS1ownership andIRQmaskszero.
Retainwiredscratchafteranysubmission. BoundedASupdate/jobwait/JS1hardstop;
requireJS_STATEsnapshotinactive/NEXTzero, thenASdisable/update/restore
beforecorepoweroff. IRQdone+nofault+headerexception1+exactimmediate64output
are requiredforPASS. Unprovenretirementquarantineswiredmemory, skipscore
offandrefusesfurtheractivecommandsuntilreboot. NoGPUreset/scanout/IOSurface
or arbitraryaddresscommands. Actualstatefulhosttests+ARM64compilePASS;
fullCI/actualhardwarejobpending. AWRITE_VALUEisnotframebufferacceleration.

## G57 v9 header correction before hardware submission

Mesa pan_arch(9091)=9. v9 WRITE_VALUE header has reservedbit0=0 and128byte
alignment; v7 Is64b bit0=1 does not apply. The earlier v7 field check was
insufficient. Correct jobword4 is00010004 (type2/index1), not00010005.
Payload offsets32/40/48 remain unchanged. Actual v9 schema now required by
host test; actual fake submission asserts correctedword. No priorjobkernel
flashed; CI44615378050 superseded beforehardwaretrial. NativeMesa24.3
compiler built locally (hostC11compatibilityonly), generated128byteG57
copyshader TLS/WLS0/preloadr60. Hostpreparation, nothardwarecopyexecution.

##0167 prepared native G57 compute copy (not in build profile)

HostNIRgenerator uses Mesa24.3compiler for9091,128byteValhallbinary,
32registers/TLS0/WLS0/noFAU/preloadR60. Oneu32 perglobalinvocation copies
GPUVA02002000->02003000. tools/a03-gpu-copy-layout.h containsderivedcode
andSHA256; mapsdescriptorNX/codeRO-exec/sourceRO-NX/destinationRW-NX.
Countlimited1..1024 withonepageeach. Compute/header/program/TLS descriptor
bytes match actual Mesa-generatedv9packers. ASanUBSanallcounts/permissions/
canaries+actualruntimefakeDMA success/sourcecorruption/destinationmismatch
checksPASS;2BSDARM64compilesPASS. Patch0167 isPREPARED ONLY, notstagedin
A03profile, nohardwarecomputeclaim. Corrected0166 WRITE_VALUE mustpass first.

Reproduce nativecopybinary from configured pinnedMesa24.3build:
python3 tools/a03-build-g57-copy-shader.py MESA_BUILD NEW_OUTPUT_DIR
Builder reusesMesa'sactualcompile/linkcommands, rejectsotherMesaversions,
andchecksderivedcodeSHA256565e07d886d6f111fac39102242d7175f06f0ba5f6f5b52797f8537d0c6814b7.
ReproductionPASS. LocalglibcC23once_flag/call_oncecollision wasresolved
onlyinignoredMesacheckout byrenamingMesaemulationidentifiers; noPanfrost
compilerinstructionlogicchanged. No phonecomputeexecutionclaim.

## BOOT0099 first hardware job PASS

Correctedv9 WRITE_VALUE tx2:submitted1/done1/retired1,IRQ2/MMU0/ASfault0,
headerexception1,output0077ccff003388aaequalsimmediatevalue. Corepoweroff
PASS/fault0. This isrealhardwarejob/readback, notprivateCPUzeroing.
NoIOSurface/scanoutaccelerationyet.0167nativecomputecopy stagedonlyafter
thishardwaregate; fullCIandactualcopyreadbackremainrequired.

##0168 retained IOSurface framebuffer candidate

Explicit gpu blit on enables the guarded native strided-copy backend; the
default is off. gpu blit reports verified frames/pixels/fallback/quarantine.
All GPU entry points share one atomic owner. AppleCLCD retains the source
surface during synchronous submission/readback; uncertain DMA keeps that
retain indefinitely and disables panel writes until reboot. Busy frames are
skipped. Validated source pages are RO/NX; only the fixed panel extent is
writable. CPU fallback follows proven retirement, never a pending timeout.
Full rectangle readback is enabled for bring-up, so no speedup is promised.
Native shader generation and host MMIO tests are not hardware-blit evidence.

##0169 2D and selectable readback candidate

Dispatch width-by-height with native global X/Y removes per-pixel division.
The pinned shader is256bytes,32registers,noTLS/WLS,preloadR60/R61. Full
readback defaults on; explicit gpu blit fast omits it after four successful
verified frames. gpu blit verify restores full checks. Completion, MMU fault
and retirement checks always apply. Counters report verified/completed frames
and CPU/GPU copy nanoseconds. Candidate tests do not prove speedup.


## 2026-11-20 measured framebuffer-copy status

This is GPU-assisted framebuffer copying. CoreAnimation still renders the
source surfaces on the CPU; Metal/EAGL support is outside this milestone.
All timings below are synchronous copy latency, including scheduling, cache
maintenance and setup, rather than physical frame rate.

| BOOT | Copy policy | Measured GPU latency | CPU comparison |
| --- | --- | --- | --- |
| 0106 | uncached scalar | 142.160 ms | CPU faster |
| 0107 | cached scalar, fresh GPU cache clean | 6.170 ms | 1.673 ms |
| 0108 | cached four-pixel vectors | 3.542 ms | 1.406 ms |
| 0109 | four-pixel vectors, explicit retained power | 2.327 ms median, three rounds | 1.613 ms median |
| 0110 | generic sixteen-pixel vectors, retained power | 4.071 ms median, three rounds | 1.676 ms median |

BOOT0110 full720x1600 readbacks pass with zero mismatches, completed jobs and
retirement. Its generic sixteen-pixel shader is rejected as a performance
optimization. GPU copying remains opt-in and currently OFF. It has not yet
shown a speed benefit over the CPU.

0178 restores the bounded generic four-pixel shader and adds an exact
fullscreen shader with fixed GPU VAs04000000/05000000, source stride3072,
destination stride2880, offsets0, dimensions720x1600. It dispatches3x400
workgroups of15x4 threads, each copying16 pixels. Any guard mismatch uses
the generic shader and its masked tails. The specialized384byte binary has
32 registers, no TLS/WLS, and SHA256
4fda1c5c52971205f7ad8510eda5ca96faa122ae8e399bdb8a6df29155a96cb6.

Reproduce both binaries using the pinned native Mesa24.3.0 build:

    python3 tools/a03-build-g57-copy-shader.py MESA_BUILD NEW_GENERIC --blit
    python3 tools/a03-build-g57-copy-shader.py MESA_BUILD NEW_FULLSCREEN --fullscreen
    python3 tools/a03-test-gpu-blit-layout.py --mesa-build MESA_BUILD
    python3 tools/a03-test-gpu-blit.py --source PATCHED_XNU

Host checks cover separate shader identities, exact specialized guards,
generic dispatch/tails, primary Mesa v9 descriptor packing, full page-table
translation, cached writes hidden until GPU clean completion, source ownership,
retirement/quarantine, and warm power ownership. They are not evidence of
0178 hardware performance. Exact commit8c0fe7cd24e3042d40cd760a139aa31cf93ef55e
is building in CI44813460343. Require artifact/source verification, BOOT-only
test, four full readbacks, paired CPU/GPU timings and physical UI acceptance.

A stale clock is a separate investigation. While GPU copying is OFF and
powered0, vsync and kernel time continue but compositor submissions can stop.
One explicit Home resumes CPU frames. The current framebuffer does not
implement panel blanking or display power-state handling, so iOS sleep may
leave the last clock image visible. That remains a hypothesis pending a
controlled Auto-Lock Never trial or direct display-power evidence. Do not
simulate progress with periodic Home presses or repeated old-frame copies.


BOOT0111 follow-up: specialized sixteen-pixel copies pass full readback but
paired medians remain GPU4.100ms vs CPU1.462ms. It is not a speed improvement.
0179 changes only the exact fullscreen shader to four pixels/thread,15x4
threads and12x400 groups (128bytes,32regs,TLSWLS0). Neighboring lanes now
copy contiguous16byte units. Generic4 fallback and all safety checks remain.
Its SHA256 is c4f0ba76ccd62ed3f455b2dc9d02e85276a54251af66a1a6b39b97c5567d545b.
Host reproduction/packers/lifecycle/ARM64/profile125 pass; hardware pending.


BOOT0112 hardware: full readbacks pass; paired GPU median2.231ms versus
CPU1.668ms. 0180 tests four coalesced180pixel strips per row, reusing each
thread across four strips while preserving contiguous accesses among lanes.
It remains exact-fullscreen only; generic fallback and lifecycle are unchanged.
0181 independently observes raw iOS16 display-power requests (selector12,
one scalar). It preserves current return codes and panel behavior; observing
a request is not evidence of a completed power transition or a freeze fix.


BOOT0113 hardware results: coalesced strips pass full readback; three paired
rounds yield medianGPU2.153ms versus CPU1.580ms. No speedup is established.
The explicit live UI trial completes one additional GPU frame with no faults,
but no touch events arrive during that window; physical acceptance is pending.
GPU copying is left OFF/powered0, verification ON, cached/warm policy retained.

The0181 observer now records a raw power-request sequence1 ->0 during idle,
with compositor submissions stopping. One explicit Home produces request1
immediately followed by new CPU frames. This strongly supports display sleep
as an explanation for the stale clock in that episode. It does not establish
the enum definitions or a completed panel power transition, and PosterBoard
crashloops remain a separate issue. The driver still does not blank the panel
or change the existing selector12 return status. No periodic wake is installed.
