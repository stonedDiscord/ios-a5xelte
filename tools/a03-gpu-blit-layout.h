/* Native G57 strided BGRA/u32 copy, generated with Mesa24.3.0.
 * SHA256 03409e893339415bbdbe0bc83449712e009f783866bc5c0986c9137ccfb73e0b; TLS/WLS0,32regs,preloadR60/R61. */
#ifndef A03_GPU_BLIT_LAYOUT_H
#define A03_GPU_BLIT_LAYOUT_H
#include "a03-gpu-copy-layout.h"
#define A03_GPU_BLIT_SIZE 0x10000U
#define A03_GPU_BLIT_SPAN 0x800000U
#define A03_GPU_BLIT_SOURCE_VA 0x04000000U
#define A03_GPU_BLIT_DEST_VA 0x05000000U
static const uint64_t a03_g57_blit_code[] = {
    0x0110c002000210c0ULL,
    0x0091c100000000c0ULL,
    0x086080f838000040ULL,
    0x00f0c30480c0433dULL,
    0x00f0c20480c0423cULL,
    0x00b4c2010043c042ULL,
    0x0110c302000200c0ULL,
    0x0091c40000000043ULL,
    0x0091c500000000c0ULL,
    0x006084f468000044ULL,
    0x501fc03000000e42ULL,
    0x00b4c20119c0c87cULL,
    0x00a0c000000a403dULL,
    0x10a8c00000000240ULL,
    0x00a8c00000004044ULL,
    0x00a0c100000a417dULL,
    0x00a8c10000004241ULL,
    0x00a8c10000004145ULL,
    0x0091c20000000040ULL,
    0x0091c300000000c0ULL,
    0x0060808298000042ULL,
    0x0091c20000000041ULL,
    0x2091c300000000c0ULL,
    0x0061400218000042ULL,
    0x501fc010000001c0ULL,
    0x7800c00000000000ULL,
    0x7800c00000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
};
/* Geometry is bounded before arithmetic, division or page-table construction. */
static int a03_gpu_blit_geometry(uintptr_t source, uintptr_t destination,
    uint64_t physical, unsigned source_stride, unsigned destination_stride,
    unsigned width, unsigned height, uint64_t *source_length, uint64_t *destination_length)
{
    if (!source || !destination || ((source | destination | physical) & 3) ||
        !width || width > 720 || !height || height > 1600 ||
        source_stride < width * 4 || source_stride > 65536 ||
        destination_stride != 2880 || physical < 0x9e000000ULL ||
        physical >= 0x9e000000ULL + 4608000) return 0;
    *source_length = (uint64_t)(height-1)*source_stride + width*4;
    *destination_length = (uint64_t)(height-1)*destination_stride + width*4;
    return *source_length <= A03_GPU_BLIT_SPAN - (source & 4095) &&
        *destination_length <= 0x9e000000ULL + 4608000 - physical &&
        source <= UINTPTR_MAX - *source_length && destination <= UINTPTR_MAX - *destination_length;
}
static int a03_gpu_blit_layout(void *memory, uint64_t physical,
    unsigned source_offset, unsigned destination_offset, unsigned source_stride,
    unsigned destination_stride, unsigned width, unsigned height)
{
    if (!memory || source_offset >= 4096 || destination_offset >= 4096 ||
        ((source_offset | destination_offset) & 3) || !width || width > 720 ||
        !height || height > 1600 || source_stride < width*4 || source_stride > 65536 ||
        destination_stride < width*4 || destination_stride > 65536 ||
        (uint64_t)(height-1)*source_stride+width*4 > A03_GPU_BLIT_SPAN-source_offset ||
        (uint64_t)(height-1)*destination_stride+width*4 > A03_GPU_BLIT_SPAN-destination_offset ||
        !a03_gpu_copy_layout(memory,physical,1)) return 0;
    uint64_t *q=(uint64_t *)memory;
    for(unsigned i=0x8000/8;i<A03_GPU_BLIT_SIZE/8;i++)q[i]=2;
    q[0x3000/8+2]=q[0x3000/8+3]=2;
    for(unsigned i=0;i<4;i++) {
        q[0x2000/8+32+i]=(physical+0x8000+i*4096)|0x403ULL;
        q[0x2000/8+40+i]=(physical+0xc000+i*4096)|0x403ULL;
    }
    uint32_t *job=(uint32_t *)((uint8_t *)memory+0x4000);
    /* 64 threads per 16x4 group; shader masks padded edge lanes. */
    job[8]=0x80000c0fU;
    job[10]=(width+15)/16;job[11]=(height+3)/4;
    ((uint32_t *)((uint8_t *)memory+0x4100))[1]=0x3000U; /* preload globalX/Y */
    uint64_t *code=(uint64_t *)((uint8_t *)memory+0x5000);
    for(unsigned i=0;i<sizeof(a03_g57_blit_code)/8;i++)code[i]=a03_g57_blit_code[i];
    uint32_t *params=(uint32_t *)((uint8_t *)memory+0x4200);
    params[0]=A03_GPU_BLIT_SOURCE_VA+source_offset;
    params[1]=A03_GPU_BLIT_DEST_VA+destination_offset;
    params[4]=source_stride;params[5]=destination_stride;params[6]=width;params[7]=height;
    return 1;
}
#endif
