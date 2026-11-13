/* Pre-Linux register report. No MMIO/storage access or FDT resizing.
 * Replace only /chosen/bootargs tokens already observed on this A03.
 */
#include <stdint.h>
#ifdef A03_MMU16K
extern void a03_test_el1(void);
extern volatile uint64_t a03_mmu_result[12];
#endif
static uint32_t be32(const unsigned char *p)
{
    return (uint32_t)p[0]<<24 | (uint32_t)p[1]<<16 | (uint32_t)p[2]<<8 | p[3];
}
static int equal(const unsigned char *a, const char *b, unsigned n)
{
    for (unsigned i=0;i<n;i++) if (a[i] != (unsigned char)b[i]) return 0;
    return 1;
}
static unsigned char *bootargs(unsigned char *fdt, uint32_t *length)
{
    if (!fdt || be32(fdt)!=0xd00dfeed) return 0;
    uint32_t size=be32(fdt+4), p=be32(fdt+8), strings=be32(fdt+12);
    if (size<40 || size>0x100000 || p<40 || p>size || strings>=size) return 0;
    int depth=0, chosen=0;
    while (p<=size-4) {
        uint32_t token=be32(fdt+p); p+=4;
        if (token==1) {
            uint32_t start=p;
            while (p<size && fdt[p]) p++;
            if (p==size) return 0;
            depth++;
            if (depth==2 && p-start==6 && equal(fdt+start,"chosen",6)) chosen=depth;
            p=(p+4)&~3U;
        } else if (token==2) {
            if (depth==chosen) chosen=0;
            if (--depth<0) return 0;
        } else if (token==3) {
            if (p>size-8) return 0;
            uint32_t len=be32(fdt+p), off=be32(fdt+p+4); p+=8;
            if (len>size-p || off>=size-strings) return 0;
            uint32_t name=strings+off;
            if (chosen==depth && chosen && size-name>=9 &&
                equal(fdt+name,"bootargs",9)) {
                *length=len; return fdt+p;
            }
            p=(p+len+3)&~3U;
        } else if (token!=4) return 0;
    }
    return 0;
}
static void report(unsigned char *args, uint32_t size, const char *needle,
                   unsigned length, char key, uint64_t value)
{
    static const char digits[]="0123456789abcdef";
    if (length<22) return;
    for (uint32_t i=0;i+length<size;i++) {
        if ((i && args[i-1]!=' ') || !equal(args+i,needle,length) ||
            (args[i+length] && args[i+length]!=' ')) continue;
        args[i]='a'; args[i+1]='0'; args[i+2]='3'; args[i+3]=key;
        args[i+4]='=';
        for (unsigned j=0;j<16;j++) args[i+5+j]=digits[(value>>(60-4*j))&15];
        for (unsigned j=21;j<length;j++) args[i+j]=' ';
        return;
    }
}
#define REPORT(needle,key,reg) do { uint64_t value; \
    __asm__ volatile("mrs %0, " #reg : "=r"(value)); \
    report(args,size,needle,sizeof(needle)-1,key,value); } while (0)
void a03_boot_probe(unsigned char *fdt)
{
    uint32_t size=0;
    unsigned char *args=bootargs(fdt,&size);
    if (!args) return;
#ifndef A03_MMU16K
    REPORT("androidboot.em.model=SM-A035G",'m',id_aa64mmfr0_el1);
    REPORT("androidboot.pcbainfo=EU_PCBA3_DCAM_MP",'i',midr_el1);
    REPORT("androidboot.carrierid.param.offset=9437644",'p',mpidr_el1);
    REPORT("androidboot.sales.param.offset=9437648",'e',CurrentEL);
    REPORT("androidboot.sn.param.offset=9437392",'s',sctlr_el1);
    REPORT("androidboot.ddrsize.range=[4096,5120)",'f',cntfrq_el0);
#else
    a03_test_el1();
#define RESULT(needle,key,index) report(args,size,needle,sizeof(needle)-1,key,a03_mmu_result[index])
    /* Reuse only the six slots already tested in probe 0001. AVB and
     * verity arguments are required by Android init and must survive. */
    RESULT("androidboot.em.model=SM-A035G",'t',0);
    RESULT("androidboot.pcbainfo=EU_PCBA3_DCAM_MP",'l',1);
    RESULT("androidboot.carrierid.param.offset=9437644",'q',2);
    RESULT("androidboot.sales.param.offset=9437648",'u',3);
    RESULT("androidboot.sn.param.offset=9437392",'a',5);
    RESULT("androidboot.ddrsize.range=[4096,5120)",'y',10);
#undef RESULT
#endif
}
