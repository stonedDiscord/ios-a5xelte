/* Native G57 strided BGRA/u32 copy, generated with Mesa24.3.0.
 * SHA256 88dab0e057aaf95fb42c64e38e24153c7639487442314ebea89f733ca4abf382; TLS/WLS0,32regs,preloadR60. */
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
    0x086080e630000040ULL,
    0x0090c30000190002ULL,
    0x009cc30000000043ULL,
    0x0110c44f7ffffec0ULL,
    0x00b2c30400c04443ULL,
    0x0090c300c01c0043ULL,
    0x00a0c400000a0302ULL,
    0x00a8c400000144c0ULL,
    0x0090c50030140004ULL,
    0x0090c40000140044ULL,
    0x0090c60000140003ULL,
    0x00a0c700000a0506ULL,
    0x00a0c600000a0446ULL,
    0x0090c80030140003ULL,
    0x00a0c500000a4508ULL,
    0x00a0c400000a4448ULL,
    0x00a1c800200507c0ULL,
    0x00a8c80000004806ULL,
    0x00f0c60400c04608ULL,
    0x00a8c50000004645ULL,
    0x00a1c600200504c0ULL,
    0x00a8c60000004608ULL,
    0x00f0c60400c04846ULL,
    0x0090c70030140047ULL,
    0x00a8c50000004745ULL,
    0x00a8c50000004645ULL,
    0x0090c40030140044ULL,
    0x00a8c40000004445ULL,
    0x00a8c30000004443ULL,
    0x0090c40030140003ULL,
    0x0090c30000140043ULL,
    0x0090c5000014003cULL,
    0x00a0c600000a0405ULL,
    0x00a0c500000a0345ULL,
    0x0090c7003014003cULL,
    0x00a0c400000a4407ULL,
    0x00a0c300000a4347ULL,
    0x00a1c700200506c0ULL,
    0x00a8c70000004705ULL,
    0x00f0c50400c04507ULL,
    0x00a8c40000004544ULL,
    0x00a1c500200503c0ULL,
    0x00a8c50000004507ULL,
    0x00f0c50400c04745ULL,
    0x0090c60030140046ULL,
    0x00a8c40000004644ULL,
    0x00a8c40000004544ULL,
    0x0090c30030140043ULL,
    0x00a8c30000004344ULL,
    0x00a0c400000a0203ULL,
    0x00a8c4000001447cULL,
    0x00a8c50000010204ULL,
    0x00f0c60280c00204ULL,
    0x0150c4004544c006ULL,
    0x00a8c50000010204ULL,
    0x00f0c20280c04204ULL,
    0x0150c4004544c002ULL,
    0x0110c500000001c0ULL,
    0x0150c60005c0c046ULL,
    0x0150c20045c0c042ULL,
    0x00a8c30000004643ULL,
    0x00a8c20000004243ULL,
    0x00a0c000000a4002ULL,
    0x00a0c100000a4142ULL,
    0x00b4c20119c0c844ULL,
    0x00a8c00000000240ULL,
    0x00a8c10000004241ULL,
    0x0110c202000200c0ULL,
    0x0091c300000000c0ULL,
    0x106082f468000042ULL,
    0x00a8c00000004042ULL,
    0x00a8c10000004143ULL,
    0x0091c20000000040ULL,
    0x0091c300000000c0ULL,
    0x0060808298000042ULL,
    0x0091c20000000041ULL,
    0x2091c300000000c0ULL,
    0x7861400218000042ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
    0x0000000000000000ULL,
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
    job[10]=width*height;
    uint64_t *code=(uint64_t *)((uint8_t *)memory+0x5000);
    for(unsigned i=0;i<sizeof(a03_g57_blit_code)/8;i++)code[i]=a03_g57_blit_code[i];
    uint32_t *params=(uint32_t *)((uint8_t *)memory+0x4200);
    params[0]=A03_GPU_BLIT_SOURCE_VA+source_offset;
    params[1]=A03_GPU_BLIT_DEST_VA+destination_offset;
    params[4]=source_stride;params[5]=destination_stride;params[6]=width;
    return 1;
}
#endif
