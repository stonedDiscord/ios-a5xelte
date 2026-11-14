/* Minimal bounded SWEETXNU loader for A03. Storage/peripheral drivers absent. */
#include <stdint.h>
#include "../font.h"
struct segment { uint64_t va,size,off,filesize; };
struct payload { char magic[8]; uint32_t version,count; uint64_t base,entry,adtoff,adtlen,end,phys,mem; char cmdline[608]; struct segment seg[]; };
struct video {uint64_t base,display,stride,width,height,depth;};
struct bootargs {uint16_t rev,version;uint64_t virt,phys,mem,top;struct video video;uint32_t machine;uint64_t dt;uint32_t dtlen;char cmdline[608];uint64_t flags,actual;};
struct handoff {uint64_t entry,args;};
_Static_assert(sizeof(struct bootargs)==736,"boot args");
_Static_assert(__builtin_offsetof(struct bootargs,cmdline)==108,"command line offset");
_Static_assert(__builtin_offsetof(struct payload,seg)==0x2a8,"segment offset");
extern char _start[],_image_end[];
static void copy(uintptr_t d,uintptr_t s,uint64_t n) {for(uint64_t i=0;i<n;i++)((volatile unsigned char*)d)[i]=((volatile const unsigned char*)s)[i];}
static void zero(uintptr_t d,uint64_t n) {for(uint64_t i=0;i<n;i++)((volatile unsigned char*)d)[i]=0;}
static void clean(uintptr_t a,uintptr_t b) {uint64_t ctr;__asm__ volatile("mrs %0,ctr_el0":"=r"(ctr));uintptr_t line=4UL<<((ctr>>16)&15);for(a&=~(line-1);a<b;a+=line)__asm__ volatile("dc cvac,%0"::"r"(a):"memory");__asm__ volatile("dsb sy":::"memory");}
static void text(const char *s,unsigned row) {
    /* RAM logo candidate only. No display-controller register writes. */

    volatile uint32_t *fb=(volatile uint32_t*)0x9e000000UL;
    for(unsigned y=0;y<16;y++)for(unsigned x=0;x<720;x++)
        fb[(row*16+y)*720+x]=0xff000000;
    for(unsigned x=0;s[x]&&x<90;x++)for(unsigned y=0;y<16;y++)for(unsigned bit=0;bit<8;bit++)
        fb[(row*16+y)*720+x*8+bit]=(font8x16[(unsigned char)s[x]-32][y]&(0x80u>>bit))?0xffffffff:0xff000000;
    __asm__ volatile("dsb sy":::"memory");
}
#ifdef A03_EMMC_SNAPSHOT
#if A03_EMMC_SNAPSHOT == 2
static uint32_t emmc_read32(unsigned off) {
    uint32_t v=*(volatile uint32_t*)(0x201d0000UL+off);
    __asm__ volatile("dsb sy"::: "memory");return v;
}
static void emmc_write32(unsigned off,uint32_t v) {
    *(volatile uint32_t*)(0x201d0000UL+off)=v;
    __asm__ volatile("dsb sy"::: "memory");
}
static void hexline(const char *label,uint32_t value,unsigned row) {
    char line[80];unsigned n=0;
    while(*label && n<65)line[n++]=*label++;
    line[n++]='=';line[n++]='0';line[n++]='x';
    for(int shift=28;shift>=0;shift-=4)line[n++]="0123456789abcdef"[(value>>shift)&15];
    line[n]=0;text(line,row);
}
static void emmc_status_probe(void) {
    uint32_t argument=emmc_read32(0x08),state=emmc_read32(0x24);
    uint32_t modecmd=emmc_read32(0x0c),clock=emmc_read32(0x2c);
    uint32_t oldstatus=emmc_read32(0x30),response=emmc_read32(0x10);
    unsigned cmd=modecmd>>24;
    /* RCA is only a candidate retained from the observed addressed command.
     * Probe it with SEND_STATUS, never a state-changing selection command. */
    if((state&3)||(clock&7)!=7||oldstatus||!(argument>>16)||
       (argument&0xffff)||(cmd!=11 && cmd!=13)||
       (response&0x1f00)!=0x0900) {
        text("CMD13 SKIPPED - RETAINED STATE GUARD FAILED",24);return;
    }
    hexline("CMD13 CANDIDATE ARG",argument,24);
    uint32_t enable=emmc_read32(0x34),signal=emmc_read32(0x38);
    emmc_write32(0x38,0); /* poll; CPU IRQs already masked */
    emmc_write32(0x34,enable|0x000f8001u);
    emmc_write32(0x08,argument);
    text("CMD13 SEND_STATUS - WAIT MAX 1 SECOND",25);
    /* Atomic transfer-mode/command write: no data phase, no DMA. */
    emmc_write32(0x0c,0x0d1a0000u);
    uint64_t start,now,freq;
    __asm__ volatile("mrs %0,cntpct_el0":"=r"(start));
    __asm__ volatile("mrs %0,cntfrq_el0":"=r"(freq));
    uint32_t status=0;
    for(unsigned i=0;i<10000000;i++) {
        status=emmc_read32(0x30);
        if(status&0xffff8001u)break;
        __asm__ volatile("mrs %0,cntpct_el0":"=r"(now));
        if(now-start>=freq)break;
    }
    hexline("CMD13 INT",status,26);
    hexline("CMD13 RESPONSE",emmc_read32(0x10),27);
    hexline("CMD13 PRESENT",emmc_read32(0x24),28);
    emmc_write32(0x34,enable);
    emmc_write32(0x30,status&0xffff8001u);
    emmc_write32(0x38,signal);
    if((status&0xffff8001u)==1)text("CMD13 RESPONSE RECEIVED - CHECK CARD STATUS",30);
    else text("CMD13 FAILED/TIMED OUT - NO RESET OR RETRY",30);
}
#endif
/* Register addresses/widths checked against the A03 live DT and Linux
 * sprd-sdhcr11.h. No FIFO read, controller write, reset or card command.
 * Run before XNU takes ownership; pause so its console cannot erase evidence.
 * A pre-access marker identifies the register if a bus access faults/stalls.
 */
static void emmc_snapshot(void) {
    static const struct { char name[12]; unsigned off, width; } regs[] = {
        {"PRESENT",0x24,4}, {"CLOCK",0x2c,2},
        {"HOST",0x28,1}, {"POWER",0x29,1},
        {"HOST2",0x3e,2}, {"VERSION",0xfe,2},
        {"ARG",0x08,4}, {"COMMAND",0x0e,2},
        {"RESPONSE0",0x10,4}, {"INT_STATE",0x30,4},
        {"INT_ENABLE",0x34,4}, {"SIGNAL",0x38,4},
        {"DLL_CFG",0x200,4}, {"DLL_DELAY",0x204,4}
    };
#if A03_EMMC_SNAPSHOT == 2
    text("A03 EMMC 0014 SNAPSHOT + GUARDED CMD13",3);
#else
    text("A03 EMMC 0013 READ-ONLY SNAPSHOT PA 201d0000",3);
#endif
    for(unsigned i=0;i<sizeof(regs)/sizeof(regs[0]);i++) {
        char line[80]; unsigned n=0;
        for(const char *s=regs[i].name;*s;s++)line[n++]=*s;
        line[n++]=' ';line[n++]='r';line[n++]='e';line[n++]='a';
        line[n++]='d';line[n++]=0;
        text(line,5+i);
        uintptr_t addr=0x201d0000UL+regs[i].off;
        __asm__ volatile("dsb sy"::: "memory");
        uint32_t value;
        if(regs[i].width==1)value=*(volatile uint8_t*)addr;
        else if(regs[i].width==2)value=*(volatile uint16_t*)addr;
        else value=*(volatile uint32_t*)addr;
        __asm__ volatile("dsb sy"::: "memory");
        n-=5;line[n++]='=';line[n++]='0';line[n++]='x';
        for(int shift=28;shift>=0;shift-=4)line[n++]="0123456789abcdef"[(value>>shift)&15];
        line[n]=0;text(line,5+i);
    }
#if A03_EMMC_SNAPSHOT == 2
    emmc_status_probe();
    text("STATUS PROBE COMPLETE - PAUSED FOR PHOTO",32);
    text("NO SECTOR READS OR STORAGE WRITES",33);
#else
    text("A03 EMMC SNAPSHOT COMPLETE - PAUSED FOR PHOTO",21);
    text("NO CARD COMMANDS OR STORAGE WRITES ISSUED",22);
#endif
    for(;;)__asm__ volatile("wfe");
}
#endif
struct handoff a03_load_xnu(uintptr_t fdt) {
    (void)fdt;
    struct handoff fail={0,0};text("A03 XNU LOADER - EL1",0);
    uintptr_t src=(uintptr_t)_image_end,limit=(uintptr_t)_start+*(uint64_t*)(_start+16);
    if(limit<src||limit-src<0x2a8||limit-src>0x3000000)return fail;
    const struct payload *p=(const struct payload*)src;
    const char *magic="SWEETXNU";for(unsigned i=0;i<8;i++)if(p->magic[i]!=magic[i])return fail;
    uint64_t len=limit-src;
    if(p->version!=1||!p->count||p->count>32||0x2a8+p->count*32>len||p->adtoff>len||p->adtlen>len-p->adtoff)return fail;
    if(p->phys!=0x102000000UL||p->mem!=0x10000000UL||p->entry<p->base||p->end<p->base||p->end-p->base>=p->mem||p->entry>=p->end||p->adtlen>0x100000||!p->adtlen||p->cmdline[607])return fail;
    unsigned entry_found=0;
    for(unsigned i=0;i<p->count;i++) {
        const struct segment *s=&p->seg[i];
        if(s->va<p->base||s->size>p->mem||s->va-p->base>p->mem-s->size||s->filesize>s->size||s->off>len||s->filesize>len-s->off)return fail;
        if(s->va-p->base+s->size>p->end-p->base)return fail;
        if(p->entry>=s->va&&p->entry-s->va<s->filesize)entry_found=1;
        for(unsigned j=0;j<i;j++) {
            const struct segment *t=&p->seg[j];
            if(s->size&&t->size&&s->va<t->va+t->size&&t->va<s->va+s->size)return fail;
        }
    }
    uintptr_t dt=p->phys+p->end-p->base,ba=(dt+p->adtlen+16383)&~16383UL;
    if(ba<dt||ba+16384>p->phys+p->mem)return fail;
    if(!entry_found)return fail;
#ifdef A03_EMMC_SNAPSHOT
    emmc_snapshot();
#endif
    for(unsigned i=0;i<p->count;i++) {
        const struct segment *s=&p->seg[i];
        uintptr_t dst=p->phys+s->va-p->base;
        copy(dst,src+s->off,s->filesize);zero(dst+s->filesize,s->size-s->filesize);clean(dst,dst+s->size);
    }
    copy(dt,src+p->adtoff,p->adtlen);zero(ba,16384);
    volatile struct bootargs *a=(volatile struct bootargs*)ba;
    a->rev=2;a->version=2;a->virt=p->base;a->phys=p->phys;a->mem=p->mem;a->top=ba+16384;
    a->video=(struct video){0x9e000000,1,2880,720,1600,32};
    a->dt=p->base+dt-p->phys;a->dtlen=p->adtlen;a->actual=p->mem;
    for(unsigned i=0;i<608;i++)a->cmdline[i]=p->cmdline[i];
    clean(dt,ba+16384);
    text("JUMP TO XNU 8796 - NATIVE 16K",1);
    return (struct handoff){p->phys+p->entry-p->base,ba};
}
