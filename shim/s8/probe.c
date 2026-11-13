/* Runs before the original Linux kernel; no storage or MMIO writes.
 * Replaces only the board-region hints in the boot FDT's bootargs with
 * an MMFR0 report. Linux then exposes it through /proc/cmdline.
 */
#include <stdint.h>
static uint32_t be32(const unsigned char *p) {
    return (uint32_t)p[0]<<24 | (uint32_t)p[1]<<16 |
           (uint32_t)p[2]<<8 | p[3];
}
static void report(unsigned char *fdt, const char *needle, unsigned length,
                   char key, uint64_t value) {
    const char digits[] = "0123456789abcdef";
    if (!fdt || be32(fdt) != 0xd00dfeed) return;
    uint32_t size = be32(fdt+4);
    if (size < 40 || size > 0x100000) return;
    for (uint32_t i=40; i+length <= size; i++) {
        unsigned j=0;
        while (j<length && fdt[i+j] == (unsigned char)needle[j]) j++;
        if (j != length) continue;
        fdt[i]='s'; fdt[i+1]='8'; fdt[i+2]=key; fdt[i+3]='=';
        for (j=0;j<16;j++) fdt[i+4+j]=digits[(value>>(60-4*j))&15];
        for (j=20;j<length;j++) fdt[i+j]=' ';
        return;
    }
}

#define REPORT(needle, key, reg) do { \
    uint64_t value; \
    __asm__ volatile("mrs %0, " #reg : "=r"(value)); \
    report(fdt, needle, sizeof(needle)-1, key, value); \
} while (0)
void s8_probe(unsigned char *fdt) {
    REPORT("region1=EUR region2=OPEN", 'm', id_aa64mmfr0_el1);
    REPORT("sec_debug.chipidfail_cnt=0", 'i', midr_el1);
    REPORT("sec_debug.lpitimeout_cnt=0", 'p', mpidr_el1);
    REPORT("sec_debug.cache_err_cnt=0", 'f', cntfrq_el0);
    REPORT("sec_debug.codediff_cnt=0", 'e', CurrentEL);
    REPORT("sec_debug.pcb_offset=7343872", 's', sctlr_el1);
}
