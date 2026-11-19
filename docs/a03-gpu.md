# A03 GPU acceleration bring-up

The running BOOT0095 compositor is software. No A03 GPU ID, completed GPU
job, rendered pixel, EAGL/Metal device or GPU-accelerated SpringBoard frame
has been measured. An A75 scheduling preference does not supply a GPU driver.

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
4. IOSurface import, cache maintenance, fences and a guarded GPU copy with
   CPU fallback, followed by an iOS EAGL/CoreAnimation rendering backend.
5. Verify repeated physical UI frames use that backend and measure latency.
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
