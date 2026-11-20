/* Native G57 strided BGRA/u32 copy, generated with Mesa24.3.0.
 * SHA256 9412d199dcb1f8f71a8144e3e4b45036ad6ce045d2c8c07adc3d2d73e890625c; TLS/WLS0,32regs,preloadR60/R61. */
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
    0x00b4c40119c0c83cULL,
    0x00f0c50480c00204ULL,
    0x00b4c3010043c005ULL,
    0x0110c602000200c0ULL,
    0x0091c700000000c0ULL,
    0x006086f468000046ULL,
    0x501fc03000003443ULL,
    0x00b4c30111c0c97cULL,
    0x00a0c000000a403dULL,
    0x10a8c00000000340ULL,
    0x00a8c00000004046ULL,
    0x00a0c100000a417dULL,
    0x00a8c10000004341ULL,
    0x00a8c10000004147ULL,
    0x0110c30000000304ULL,
    0x00f0c30480c00243ULL,
    0x501fc03000000743ULL,
    0x0091c20000000040ULL,
    0x0091c300000000c0ULL,
    0x006082f8b8000042ULL,
    0x0091c00000000041ULL,
    0x2091c100000000c0ULL,
    0x0061420838000040ULL,
    0x501fc010000022c0ULL,
    0x501fc03000000745ULL,
    0x0091c60000000000ULL,
    0x0091c700000000c0ULL,
    0x0060838258000046ULL,
    0x0091c60000000001ULL,
    0x1091c700000000c0ULL,
    0x0061430298000046ULL,
    0x501fc010000000c0ULL,
    0x0110c30000000104ULL,
    0x00f0c30480c00203ULL,
    0x501fc03000000b03ULL,
    0x0110c30000000400ULL,
    0x00f0c50400c00003ULL,
    0x0091c60000000003ULL,
    0x2091c70000000045ULL,
    0x0060838218000046ULL,
    0x0110c50000000401ULL,
    0x00f0c60400c00105ULL,
    0x0091c80000000045ULL,
    0x0891c90000000046ULL,
    0x0061430258000048ULL,
    0x501fc010000000c0ULL,
    0x0110c30000000244ULL,
    0x00f0c20480c04203ULL,
    0x501fc03000000942ULL,
    0x0110c20000000800ULL,
    0x00f0c00400c04002ULL,
    0x3091c30000000040ULL,
    0x0060808298000042ULL,
    0x0110c20000000801ULL,
    0x00f0c10400c04102ULL,
    0x2091c30000000041ULL,
    0x0061400218000042ULL,
    0x501fc010000000c0ULL,
    0x501fc010000001c0ULL,
    0x7800c00000000000ULL,
    0x7800c00000000000ULL,
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
/* Exact full-screen shader SHA256 c4f0ba76ccd62ed3f455b2dc9d02e85276a54251af66a1a6b39b97c5567d545b; 15x4 threads, four pixels/thread. */
static const uint64_t a03_g57_fullscreen_code[] = {
    0x00b4c00111c0c97cULL,
    0x0110c100000c00c0ULL,
    0x00a0c100000a413dULL,
    0x0110c10400000041ULL,
    0x00a8c10000000041ULL,
    0x0110c200000b40c0ULL,
    0x00a0c200000a427dULL,
    0x0110c20500000042ULL,
    0x00a8c00000004042ULL,
    0x0091c20000000041ULL,
    0x0091c300000000c0ULL,
    0x006082f838000042ULL,
    0x0891c100000000c0ULL,
    0x7861420878000040ULL,
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
    /* 64 threads per 16x4 group; each copies four pixels with masked tails. */
    job[8]=0x80000c0fU;
    job[10]=(width+63)/64;job[11]=(height+3)/4;
    ((uint32_t *)((uint8_t *)memory+0x4100))[1]=0x3000U; /* preload globalX/Y */
    uint64_t *code=(uint64_t *)((uint8_t *)memory+0x5000);
    for(unsigned i=0;i<sizeof(a03_g57_blit_code)/8;i++)code[i]=a03_g57_blit_code[i];
    uint32_t *params=(uint32_t *)((uint8_t *)memory+0x4200);
    params[0]=A03_GPU_BLIT_SOURCE_VA+source_offset;
    params[1]=A03_GPU_BLIT_DEST_VA+destination_offset;
    params[4]=source_stride;params[5]=destination_stride;params[6]=width;params[7]=height;
    if(!source_offset && !destination_offset && source_stride==3072 && destination_stride==2880 && width==720 && height==1600) {
        job[8]=0x80000c0eU;job[10]=12;job[11]=400;
        for(unsigned i=0;i<sizeof(a03_g57_fullscreen_code)/8;i++)code[i]=a03_g57_fullscreen_code[i];
    }
    return 1;
}
#endif
