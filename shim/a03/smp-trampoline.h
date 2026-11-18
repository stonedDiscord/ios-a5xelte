/* Bounded native ADT traversal for the loader-owned SMP trampoline handoff. */
#ifndef A03_SMP_TRAMPOLINE_H
#define A03_SMP_TRAMPOLINE_H
#include <stdint.h>
static inline uint32_t a03_dt_u32(const unsigned char *p)
{
    return (uint32_t)p[0] | ((uint32_t)p[1]<<8) |
        ((uint32_t)p[2]<<16) | ((uint32_t)p[3]<<24);
}
static inline int a03_dt_name(const unsigned char *p, const char *name)
{
    unsigned i=0;
    while (name[i]) { if (i>=31 || p[i]!=(unsigned char)name[i]) return 0; i++; }
    return p[i]==0;
}
/* chosen property is two u64s: shim entry PA (loader fills), kernel entry PA. */
static inline int a03_dt_smp_node(unsigned char *dt, uint32_t size,
    uint32_t *offset, unsigned depth, int chosen, unsigned char **handoff)
{
    uint32_t off=*offset;
    if (depth>16 || off>size || size-off<8) return 0;
    uint32_t props=a03_dt_u32(dt+off), children=a03_dt_u32(dt+off+4);
    off+=8;
    if (props>(size-off)/36 || children>size/8) return 0;
    /* ADT name is an ordinary property; locate before inspecting chosen. */
    uint32_t start=off;
    for (uint32_t i=0;i<props;i++) {
        if (off>size || size-off<36) return 0;
        uint32_t raw=a03_dt_u32(dt+off+32), len=raw&0x7fffffff;
        if (len>size-off-36 || len>UINT32_MAX-3) return 0;
        uint32_t padded=(len+3)&~3u;
        if (padded>size-off-36) return 0;
        if (depth==1 && a03_dt_name(dt+off,"name") && len==7 &&
            dt[off+36]=='c' && dt[off+37]=='h' && dt[off+38]=='o' &&
            dt[off+39]=='s' && dt[off+40]=='e' && dt[off+41]=='n' && !dt[off+42]) chosen=1;
        off+=36+padded;
    }
    uint32_t end=off;off=start;
    for (uint32_t i=0;i<props;i++) {
        uint32_t raw=a03_dt_u32(dt+off+32),len=raw&0x7fffffff;
        if (chosen && depth==1 && a03_dt_name(dt+off,"a03-smp-trampoline")) {
            if (raw!=16 || *handoff) return 0;
            *handoff=dt+off+36;
        }
        off+=36+((len+3)&~3u);
    }
    off=end;
    for (uint32_t i=0;i<children;i++) {
        if (!a03_dt_smp_node(dt,size,&off,depth+1,0,handoff)) return 0;
    }
    *offset=off;return 1;
}
static inline int a03_dt_smp_handoff(unsigned char *dt, uint32_t size, unsigned char **handoff)
{
    uint32_t offset=0;*handoff=0;
    return a03_dt_smp_node(dt,size,&offset,0,0,handoff) && offset==size;
}
static inline uint64_t a03_smp_u64(const unsigned char *p)
{
    return (uint64_t)a03_dt_u32(p) | ((uint64_t)a03_dt_u32(p+4)<<32);
}
static inline void a03_smp_put64(unsigned char *p,uint64_t value)
{
    for (unsigned i=0;i<8;i++) p[i]=(unsigned char)(value>>(i*8));
}
#endif
