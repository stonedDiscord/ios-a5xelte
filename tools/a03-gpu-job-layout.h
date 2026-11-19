/* A03 GPU private WRITE_VALUE layout, no MMIO or allocation.
 * Sources: pinned vendor AArch64 MMU and Mesa24.3 v9.xml, docs/a03-gpu.md.
 * Host uses16KiB pages; GPU tables use4KiB granules independently. */
#ifndef A03_GPU_JOB_LAYOUT_H
#define A03_GPU_JOB_LAYOUT_H
#include <stdint.h>
#define A03_GPU_SCRATCH_SIZE 0x8000U
#define A03_GPU_JOB_VA 0x02000000ULL
#define A03_GPU_OUTPUT_VA (A03_GPU_JOB_VA + 0x1000ULL)
#define A03_GPU_OUTPUT_OFF 0x5000U
#define A03_GPU_JOB_OFF 0x4000U
#define A03_GPU_CANARY 0xa5a55a5adeadbeefULL
#define A03_GPU_RESULT 0x0077ccff003388aaULL
static int
a03_gpu_job_layout(void *memory, uint64_t physical)
{
    if (!memory || ((uintptr_t)memory & 7U) || !physical ||
        (physical & 0x3fffULL) || physical > (1ULL << 40) - A03_GPU_SCRATCH_SIZE)
        return 0;
    uint64_t *q = (uint64_t *)memory;
    for (unsigned i = 0; i < A03_GPU_SCRATCH_SIZE / 8; i++) q[i] = 0;
    /* ARM descriptors: invalid=2, table=3|AF. Only two data pages mapped;
     * tables themselves are not reachable through GPU virtual addresses. */
    for (unsigned i = 0; i < 0x4000U / 8; i++) q[i] = 2;
    q[0] = (physical + 0x1000) | 0x403ULL;
    q[0x1000 / 8] = (physical + 0x2000) | 0x403ULL;
    q[0x2000 / 8 + ((A03_GPU_JOB_VA >> 21) & 511)] = (physical + 0x3000) | 0x403ULL;
    /* AttrIndex5=normal NC, AP=RW, AF=1, L3 page=3, NX=1. */
    q[0x3000 / 8] = (physical + A03_GPU_JOB_OFF) | (1ULL << 54) | 0x457ULL;
    q[0x3000 / 8 + 1] = (physical + A03_GPU_OUTPUT_OFF) | (1ULL << 54) | 0x457ULL;
    uint32_t *job = (uint32_t *)((uint8_t *)memory + A03_GPU_JOB_OFF);
    /* Mesa v9 header:type2/index1; bit0 is reserved zero. Payload32:VA,40:type7,48:value. */
    job[4] = 0x00010004U;
    *(uint64_t *)(job + 8) = A03_GPU_OUTPUT_VA;
    job[10] = 7; /* immediate64 */
    *(uint64_t *)(job + 12) = A03_GPU_RESULT;
    *(uint64_t *)((uint8_t *)memory + A03_GPU_OUTPUT_OFF) = A03_GPU_CANARY;
    return 1;
}
#endif
