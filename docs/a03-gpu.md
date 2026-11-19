# A03 GPU acceleration bring-up

The BOOT0098 compositor is software. GPU_ID90910010 and a complete core
power cycle are verified. No completed GPU job, rendered pixel, EAGL/Metal
device or GPU-accelerated SpringBoard frame has been measured.

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
