/* Identity-map only the appended probe, plus an alias, using 16K pages.
 * Normal non-cacheable mappings, cache bits off, no peripheral access.
 */
#include <stdint.h>
extern uint64_t a03_l2[2048], a03_l3[2048];
extern volatile uint64_t a03_test_word, a03_mmu_result[12];
extern char a03_boot_probe_entry[], a03_probe_end[];
#define R(r) ({ uint64_t v; __asm__ volatile("mrs %0, " #r : "=r"(v)); v; })
#define W(r,v) __asm__ volatile("msr " #r ", %0" :: "r"((uint64_t)(v)) : "memory")
void a03_mmu16k_test(void)
{
    a03_mmu_result[0]=1;
    a03_mmu_result[1]=R(CurrentEL);
    if (a03_mmu_result[1]!=4) return;
    uintptr_t lo=(uintptr_t)a03_boot_probe_entry & ~16383UL;
    uintptr_t hi=((uintptr_t)a03_probe_end+16383)&~16383UL;
    if ((lo>>25)!=((hi-1)>>25) || hi>(1ULL<<36) ||
        ((uintptr_t)a03_l2&16383) || ((uintptr_t)a03_l3&16383)) return;
    for (unsigned i=0;i<2048;i++) { a03_l2[i]=0; a03_l3[i]=0; }
    for (uintptr_t p=lo;p<hi;p+=16384)
        a03_l3[(p>>14)&2047]=p | 3 | (1UL<<10) | (3UL<<8) | (1ULL<<54);
    a03_l2[lo>>25]=(uintptr_t)a03_l3|3;
    a03_l2[0x40000000UL>>25]=(uintptr_t)a03_l3|3;
    /* 36-bit VA (L2 start), 16K TG0, NC table walk, EPD1, 36-bit PA. */
    uint64_t tcr=28UL|(3UL<<12)|(2UL<<14)|(28UL<<16)|
                 (1UL<<23)|(1UL<<30)|(1UL<<32);
    W(mair_el1,0x44);
    W(tcr_el1,tcr);
    W(ttbr0_el1,(uintptr_t)a03_l2);
    __asm__ volatile("dsb sy; isb; tlbi vmalle1; dsb sy; isb" ::: "memory");
    uint64_t sctlr=R(sctlr_el1)&~((1UL<<2)|(1UL<<12)|(1UL<<19));
    W(sctlr_el1,sctlr|1);
    __asm__ volatile("isb" ::: "memory");
    a03_mmu_result[0]=2;
    a03_mmu_result[2]=R(tcr_el1);
    a03_mmu_result[3]=R(sctlr_el1);
    a03_mmu_result[4]=R(ttbr0_el1);
    uintptr_t alias=0x40000000UL+((uintptr_t)&a03_test_word&0x1ffffff);
    a03_test_word=0x16384a0355aa1234ULL;
    __asm__ volatile("dsb sy; at s1e1r, %0; isb" :: "r"(alias) : "memory");
    uint64_t par=R(par_el1);
    a03_mmu_result[5]=par;
    int ok=!(par&1) && (par&0x0000ffffffffc000ULL)==
        ((uintptr_t)&a03_test_word&0x0000ffffffffc000ULL);
    if (ok) {
        volatile uint64_t *p=(volatile uint64_t *)alias;
        ok=*p==0x16384a0355aa1234ULL;
        *p=0xa03a0316384ULL;
        __asm__ volatile("dsb sy" ::: "memory");
        ok=ok && a03_test_word==0xa03a0316384ULL;
    }
    a03_mmu_result[6]=a03_test_word;
    __asm__ volatile("at s1e1r, %0; isb" :: "r"(0UL) : "memory");
    a03_mmu_result[7]=R(par_el1);
    ok=ok && (a03_mmu_result[7]&1);
    W(sctlr_el1,sctlr);
    __asm__ volatile("isb; tlbi vmalle1; dsb sy; isb" ::: "memory");
    a03_mmu_result[0]=ok?0x16384:0xff;
}
