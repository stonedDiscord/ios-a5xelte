/* Generated from tools/a03-g57-copy-shader.c using Mesa24.3.0.
 * Native Valhall G57/9091 copy: one aligned u32 per global invocation.
 * Host preparation only; execution must be validated on hardware.
 * Binary SHA256: 565e07d886d6f111fac39102242d7175f06f0ba5f6f5b52797f8537d0c6814b7 */
#ifndef A03_GPU_COPY_LAYOUT_H
#define A03_GPU_COPY_LAYOUT_H
#include "a03-gpu-job-layout.h"
static const uint64_t a03_g57_copy_code[16] = {
    0x00b4c00119c0c87cULL,
    0x0110c102002000c0ULL,
    0x0110c20200200000ULL,
    0x00f0c10400c04102ULL,
    0x0091c30000000041ULL,
    0x0060818218000042ULL,
    0x0110c00200300040ULL,
    0x0110c202003000c0ULL,
    0x00f0c20400c04200ULL,
    0x0091c40000000040ULL,
    0x0891c50000000042ULL,
    0x7861410258000044ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
};
static int
a03_gpu_copy_layout(void *memory, uint64_t physical, unsigned words)
{
    if (!words || words > 1024 || !a03_gpu_job_layout(memory, physical)) return 0;
    uint64_t *q = (uint64_t *)memory;
    /* Four data mappings: descriptor(NX), code(RO executable),src(RO NX),dst(RW NX).
     * GPU AttrIndex5=normalNC; CPU transfers ownership via explicit cache flush. */
    q[0x3000/8] = (physical + 0x4000) | (1ULL << 54) | 0x457ULL;
    q[0x3000/8+1] = (physical + 0x5000) | 0x4d7ULL;
    q[0x3000/8+2] = (physical + 0x6000) | (1ULL << 54) | 0x4d7ULL;
    q[0x3000/8+3] = (physical + 0x7000) | (1ULL << 54) | 0x457ULL;
    uint32_t *job = (uint32_t *)((uint8_t *)memory + 0x4000);
    for (unsigned i=0;i<128/4;i++) job[i]=0;
    job[4]=0x00010008; /* v9 compute type4, index1; reservedbit0zero */
    job[8]=0x80000000U; /* group1x1x1, merge allowed */
    job[9]=0x00008001U; /* taskincrement1,axisZ */
    job[10]=words;job[11]=1;job[12]=1;
    *(uint64_t *)(job+26)=0x02000100ULL; /* payload compute.shader */
    *(uint64_t *)(job+28)=0x02000140ULL; /* payload compute.thread_storage */
    uint32_t *program=(uint32_t *)((uint8_t *)memory+0x4100);
    program[0]=0x80000018U; /* shader/compute/32regs */
    program[1]=0x1000U; /* preloadR60 globalInvocationX */
    *(uint64_t *)(program+2)=0x02001000ULL;
    uint32_t *tls=(uint32_t *)((uint8_t *)memory+0x4140);
    tls[1]=31; /* log2(NO_WORKGROUP_MEM); noTLS/WLS */
    uint64_t *code=(uint64_t *)((uint8_t *)memory+0x5000);
    for(unsigned i=0;i<16;i++)code[i]=a03_g57_copy_code[i];
    uint32_t *src=(uint32_t *)((uint8_t *)memory+0x6000);
    uint32_t *dst=(uint32_t *)((uint8_t *)memory+0x7000);
    for(unsigned i=0;i<1024;i++){src[i]=0x10203040U^(i*0x01010101U);dst[i]=0xdeadbeefU;}
    return 1;
}
#endif
