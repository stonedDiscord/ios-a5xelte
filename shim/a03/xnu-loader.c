/* Minimal bounded SWEETXNU loader for A03. Storage/peripheral drivers absent. */
#include <stdint.h>
#include "memory-profile.h"
#include "smp-trampoline.h"
#include "../font.h"
struct segment { uint64_t va,size,off,filesize; };
struct payload { char magic[8]; uint32_t version,count; uint64_t base,entry,adtoff,adtlen,end,phys,mem; char cmdline[608]; struct segment seg[]; };
struct video {uint64_t base,display,stride,width,height,depth;};
struct bootargs {uint16_t rev,version;uint64_t virt,phys,mem,top;struct video video;uint32_t machine;uint64_t dt;uint32_t dtlen;char cmdline[608];uint64_t flags,actual;};
struct handoff {uint64_t entry,args;};
_Static_assert(sizeof(struct bootargs)==736,"boot args");
_Static_assert(__builtin_offsetof(struct bootargs,cmdline)==108,"command line offset");
_Static_assert(__builtin_offsetof(struct payload,seg)==0x2a8,"segment offset");
extern char _start[],_image_end[],a03_smp_trampoline[],a03_smp_target[];
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
#if A03_EMMC_SNAPSHOT >= 2
static uint32_t emmc_read32(unsigned off) {
    uint32_t v=*(volatile uint32_t*)(0x201d0000UL+off);
    __asm__ volatile("dsb sy"::: "memory");return v;
}
static void emmc_write32(unsigned off,uint32_t v) {
    *(volatile uint32_t*)(0x201d0000UL+off)=v;
    __asm__ volatile("dsb sy"::: "memory");
}
static uint16_t emmc_read16(unsigned off) {
    uint16_t v=*(volatile uint16_t*)(0x201d0000UL+off);
    __asm__ volatile("dsb sy"::: "memory");return v;
}
static void emmc_write16(unsigned off,uint16_t v) {
    *(volatile uint16_t*)(0x201d0000UL+off)=v;
    __asm__ volatile("dsb sy"::: "memory");
}
static void hexline(const char *label,uint32_t value,unsigned row) {
    char line[80];unsigned n=0;
    while(*label && n<65)line[n++]=*label++;
    line[n++]='=';line[n++]='0';line[n++]='x';
    for(int shift=28;shift>=0;shift-=4)line[n++]="0123456789abcdef"[(value>>shift)&15];
    line[n]=0;text(line,row);
}
static unsigned emmc_status_probe(void) {
    uint32_t argument=emmc_read32(0x08),state=emmc_read32(0x24);
    uint32_t modecmd=emmc_read32(0x0c),clock=emmc_read32(0x2c);
    uint32_t oldstatus=emmc_read32(0x30),response=emmc_read32(0x10);
    unsigned cmd=modecmd>>24;
    /* RCA is only a candidate retained from the observed addressed command.
     * Probe it with SEND_STATUS, never a state-changing selection command. */
    if((state&3)||(clock&7)!=7||oldstatus||!(argument>>16)||
       (argument&0xffff)||(cmd!=11 && cmd!=13)||
       (response&0x1f00)!=0x0900) {
        text("CMD13 SKIPPED - RETAINED STATE GUARD FAILED",24);return 0;
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
    uint32_t fresh=emmc_read32(0x10);
    hexline("CMD13 RESPONSE",fresh,27);
    hexline("CMD13 PRESENT",emmc_read32(0x24),28);
    emmc_write32(0x34,enable);
    emmc_write32(0x30,status&0xffff8001u);
    emmc_write32(0x38,signal);
    if((status&0xffff8001u)==1)text("CMD13 RESPONSE RECEIVED - CHECK CARD STATUS",30);
    else text("CMD13 FAILED/TIMED OUT - NO RESET OR RETRY",30);
    return (status&0xffff8001u)==1 && (fresh&0xffffe180u)==0x100u &&
        (fresh&0x1e00u)==0x800u && !(emmc_read32(0x24)&3);
}
#if A03_EMMC_SNAPSHOT >= 3
/* Local references: A03 sprd-sdhcr11.{c,h}, sdhci.{c,h}, mmc_ops.c.
 * Read-only command whitelist; mode3 PIO, mode4 downstream SDMA path. */
static uint32_t poll_seen, poll_last, poll_present;
#if A03_EMMC_SNAPSHOT >= 5
#include "gpt-readonly.h"
static uint32_t read_limit=1;
#endif
#if A03_EMMC_SNAPSHOT >= 4
/* Dedicated loader-owned buffer stays allocated even after a timeout.
 * EL1 identity access with MMU and data cache off is checked before DMA.
 * 512-byte alignment prevents crossing the SDMA 512K boundary. */
static volatile uint32_t dma_buffer[128] __attribute__((aligned(512)));
#endif
static unsigned emmc_poll(unsigned mask) {
    uint64_t start,now,freq;
    __asm__ volatile("mrs %0,cntpct_el0":"=r"(start));
    __asm__ volatile("mrs %0,cntfrq_el0":"=r"(freq));
    for(unsigned i=0;i<10000000;i++) {
        uint32_t s=emmc_read32(0x30);
        poll_seen|=s;poll_last=s;poll_present=emmc_read32(0x24);
        if(s&0xffff8000u)return 0;
        if((s&mask)==mask)return 1;
        __asm__ volatile("mrs %0,cntpct_el0":"=r"(now));
        if(now-start>=freq)return 0;
    }
    return 0;
}
static unsigned emmc_data_read(unsigned cmd,uint32_t arg,uint32_t *buf,unsigned row) {
    if((cmd!=8 && cmd!=17)||(cmd==8 && arg)||
       (cmd==17 && arg>
#if A03_EMMC_SNAPSHOT >= 5
       read_limit
#else
       1
#endif
       )||(emmc_read32(0x24)&3)||emmc_read32(0x30))return 0;
    uint32_t enable=emmc_read32(0x34),signal=emmc_read32(0x38);
    uint32_t block=emmc_read32(0x04),count=emmc_read32(0x00);
#if A03_EMMC_SNAPSHOT >= 4
    uint64_t sctlr;__asm__ volatile("mrs %0,sctlr_el1":"=r"(sctlr));
    uint32_t host=emmc_read32(0x28),host2=emmc_read32(0x3c);
    uintptr_t target=(uintptr_t)dma_buffer;
    /* Match the observed v4/64-bit-address configuration, preserve timing. */
    /* Linux enables the v4 64-bit system address mode through HOST_CTRL2
     * bit 13 (the 16-bit register at 0x3e).  Keep the same mode even though
     * this probe's buffer currently lies below 4 GiB. */
    uint16_t ctrl2=emmc_read16(0x3e);
    if(!(ctrl2&0x2000u)) {
        /* sprd_sdhc_set_64bit_addr(host, 1), done by Linux reset_ios. */
        emmc_write16(0x3e,(uint16_t)(ctrl2|0x2000u));
        ctrl2=emmc_read16(0x3e);
    }
    if((sctlr&5)||(host2&0x30000000u)!=0x30000000u||
       !(ctrl2&0x2000u)||
       (*(volatile uint16_t*)0x201d00feUL)!=4||(target&511)||
       (target&0x7ffff)>0x7fe00u)return 0;
    uint32_t addrlo=emmc_read32(0x58),addrhi=emmc_read32(0x5c);
    for(unsigned i=0;i<128;i++)dma_buffer[i]=0xa5a5a5a5u;
    __asm__ volatile("dsb sy"::: "memory");
    /* sprd_sdmd_mode: DMA select=0, v4 address at 0x58/0x5c. */
    *(volatile uint8_t*)0x201d0028UL=(uint8_t)(host&~0x18u);
    __asm__ volatile("dsb sy"::: "memory");
    emmc_write32(0x58,(uint32_t)target);
    emmc_write32(0x5c,(uint32_t)((uint64_t)target>>32));
#endif
    emmc_write32(0x38,0);
    emmc_write32(0x34,enable|0x037f8033u);
    /* sprd_sdhc_set_blk_size(): a 16-bit write, preserving the adjacent
     * block-count halfword at 0x06. */
    emmc_write16(0x04,0x7200u); /* one 512-byte block, boundary 512K */
    emmc_write32(0x00,1); /* v4 32-bit block-count register, DMA disabled */
    emmc_write32(0x08,arg);
    hexline("READ CMD",cmd,row);
    poll_seen=0;poll_last=0;poll_present=0;
#if A03_EMMC_SNAPSHOT >= 4
    emmc_write32(0x0c,(cmd<<24)|0x003a0011u); /* single-block READ + DMA */
#else
    emmc_write32(0x0c,(cmd<<24)|0x003a0010u); /* R1 + data, read, single, PIO */
#endif
    unsigned ok=emmc_poll(1);
    unsigned stage=ok?2:1, words=0;
    uint32_t response=emmc_read32(0x10);
    hexline("READ R1",response,row+1);
    if(response&0xffffe080u) {ok=0;stage=4;}
#if A03_EMMC_SNAPSHOT >= 4
    if(ok) {emmc_write32(0x30,1);stage=3;ok=emmc_poll(2);}
    if(ok) {
        __asm__ volatile("dsb sy"::: "memory");
        unsigned changed=0;
        for(unsigned i=0;i<128;i++) {
            buf[i]=dma_buffer[i];changed|=buf[i]^0xa5a5a5a5u;words++;
        }
        ok=changed!=0;stage=ok?0:6;
    }
#else
    if(ok) {emmc_write32(0x30,1);ok=emmc_poll(0x20);if(ok)stage=3;}
    if(ok) {
        for(unsigned i=0;i<128;i++) {buf[i]=emmc_read32(0x20);words++;}
        emmc_write32(0x30,0x20);ok=emmc_poll(2);
        if(ok)stage=0;
    }
#endif
    uint32_t status=emmc_read32(0x30);
    hexline("READ INT",status,row+2);
    hexline("READ PRESENT",emmc_read32(0x24),row+3);
    if(emmc_read32(0x24)&3) {ok=0;stage=5;}
    if(!ok) {
        hexline("FAIL 1CMD 2READY 3DONE 4R1 5BUSY 6BUFFER",stage,65);
        hexline("POLL SEEN",poll_seen,66);
        hexline("POLL LAST",poll_last,67);
        hexline("POLL PRESENT",poll_present,68);
#if A03_EMMC_SNAPSHOT >= 4
        hexline("DMA WORDS COPIED",words,69);
        hexline("DMA BUFFER LOW",(uint32_t)target,72);
        hexline("DMA BUFFER HIGH",(uint32_t)((uint64_t)target>>32),73);
#else
        hexline("FIFO WORDS",words,69);
#endif
        hexline("INT ENABLE LIVE",emmc_read32(0x34),70);
        hexline("COMMAND LIVE",emmc_read32(0x0c),71);
    }
    emmc_write32(0x34,enable);
    emmc_write32(0x30,status&0xffff8033u);
#if A03_EMMC_SNAPSHOT >= 4
    /* On busy/error retain dedicated DMA address and buffer, then halt. */
    if(!(emmc_read32(0x24)&3)) {
        emmc_write32(0x58,addrlo);emmc_write32(0x5c,addrhi);
        *(volatile uint8_t*)0x201d0028UL=(uint8_t)host;
        __asm__ volatile("dsb sy"::: "memory");
    }
#endif
    emmc_write32(0x04,block);emmc_write32(0x00,count);
    emmc_write32(0x38,signal);
    return ok;
}
static uint32_t le32(const unsigned char *p) {
    return p[0]|((uint32_t)p[1]<<8)|((uint32_t)p[2]<<16)|((uint32_t)p[3]<<24);
}
static uint32_t header_crc(const unsigned char *p,unsigned n) {
    uint32_t crc=~0u;
    for(unsigned i=0;i<n;i++) {
        crc^=(i>=16 && i<20)?0:p[i];
        for(unsigned b=0;b<8;b++)crc=(crc>>1)^(0xedb88320u & (0u-(crc&1)));
    }
    return ~crc;
}
#if A03_EMMC_SNAPSHOT >= 5
static unsigned gpt_sector(void *context,uint32_t lba,unsigned char *sector) {
    (void)context;uint32_t words[128];
    if(!emmc_data_read(17,lba,words,44))return 0;
    for(unsigned i=0;i<512;i++)sector[i]=((unsigned char*)words)[i];
    return 1;
}
static void emmc_gpt_probe(const unsigned char *header,uint32_t sectors) {
    struct a03_gpt g;uint32_t crc=0;
    if(!a03_gpt_header(header,sectors,&g)) {
        text("GPT GEOMETRY/CRC GUARD FAILED",64);
        hexline("GPT BACKUP LBA LOW",a03_le32(header+32),65);
        hexline("GPT FIRST USABLE LOW",a03_le32(header+40),66);
        hexline("GPT LAST USABLE LOW",a03_le32(header+48),67);
        hexline("GPT ARRAY LBA LOW",a03_le32(header+72),68);
        hexline("GPT ENTRY COUNT",a03_le32(header+80),69);
        hexline("GPT ENTRY SIZE",a03_le32(header+84),70);return;
    }
    read_limit=sectors-1;
    unsigned result=a03_gpt_entries(&g,gpt_sector,0,&crc);
    if(result==1) {text("GPT ARRAY READ FAILED - SEE DMA DIAGNOSTICS",77);return;}
    hexline("GPT ARRAY CRC STORED",g.array_crc,64);
    hexline("GPT ARRAY CRC COMPUTED",crc,65);
    hexline("GPT RESULT 0PASS 1IO 2RANGE 3ID 4CRC 5LABEL",result,66);
    if(result && result!=3)return;
    hexline("BOOT FIRST LBA",g.boot,67);hexline("BOOT SECTORS",g.boot_count,68);
    hexline("USERDATA FIRST LBA",g.userdata,69);
    hexline("USERDATA SECTORS",g.userdata_count,70);
    if(g.userdata_count)hexline("USERDATA TAIL GAP SECTORS",
        g.last-(g.userdata+g.userdata_count-1),78);
    if(result==3) {
        hexline("IDENTITY MISMATCH BITMASK",g.identity_errors,71);
        hexline("BOOT GPT INDEX ZERO BASED",g.boot_index,72);
        hexline("USERDATA GPT INDEX ZERO BASED",g.userdata_index,73);
        hexline("GPT LAST USABLE LBA",g.last,74);
        text("0020 IDENTITY STOP - CRC CHECK COMPLETED",76);return;
    }
    text("GPT ARRAY CRC + PIT BOOT/USERDATA MATCH",71);
    uint32_t words[128];const unsigned char *b=(const unsigned char*)words;
#if A03_EMMC_SNAPSHOT == 6
    /* Only read the mailbox inside validated USERDATA, beyond the HFS root. */
    if(g.userdata_count<33554432u+8u)return;
    unsigned char mailbox[4096];
    for(unsigned i=0;i<8;i++){
        if(!emmc_data_read(17,g.userdata+33554432u+i,words,44))return;
        for(unsigned j=0;j<512;j++)mailbox[i*512+j]=b[j];
    }
    if(a03_le64(mailbox)!=0x3730474f4c333041ULL){text("NO LINUX MAILBOX MAGIC",4);return;}
    unsigned length=a03_le32(mailbox+8);
    if(length>4080||~a03_crc_update(~0u,mailbox+16,length)!=a03_le32(mailbox+12)){
        text("LINUX MAILBOX CRC FAILED",4);return;
    }
    text("A03 STOCK LINUX REPORT - CRC VERIFIED",2);
    char line[90];unsigned column=0,row=4;
    for(unsigned i=0;i<length&&row<95;i++){
        unsigned ch=mailbox[16+i];
        if(ch==10||column==88){line[column]=0;text(line,row++);column=0;if(ch==10)continue;}
        line[column++]=(ch>=32&&ch<=126)?ch:'?';
    }
    if(column){line[column]=0;text(line,row);}
    for(;;)__asm__ volatile("wfe");
#endif
    uint64_t kernel=*(const uint64_t*)(_start+16);
    if(!emmc_data_read(17,g.boot,words,44))return;
    if(a03_le64(b)!=0x2144494f52444e41ULL||a03_le32(b+8)!=kernel||
       a03_le32(b+36)!=2048||a03_le32(b+40)!=2) {
        text("BOOT HEADER MISMATCH",73);return;
    }
    /* Compare THIS image's immutable payload, since the flash replaces 0017. */
    uint64_t relative=4+kernel/512-1;
    if(kernel<512||relative>=g.boot_count)return;
    if(!emmc_data_read(17,g.boot+(uint32_t)relative,words,44))return;
    const unsigned char *expected=(const unsigned char*)_start+(relative-4)*512;
    unsigned diff=0;for(unsigned i=0;i<512;i++)diff|=b[i]^expected[i];
    hexline("BOOT PAYLOAD RELATIVE SECTOR",(uint32_t)relative,73);
    text(diff?"BOOT PAYLOAD SECTOR MISMATCH":"BOOT HEADER + 512 PAYLOAD BYTES MATCH",74);
    if(!diff)text("0020 STORAGE IDENTITY PASS - NO STORAGE WRITES",76);
}
#endif
static void emmc_read_probe(void) {
    uint32_t buf[128];
    text("READ EXT_CSD - NO CARD CONFIGURATION CHANGES",32);
    if(!emmc_data_read(8,0,buf,34)) {text("EXT_CSD FAILED - STOPPED, NO RETRY",39);return;}
    const unsigned char *p=(const unsigned char*)buf;
    uint32_t sectors=le32(p+212);
    hexline("EXT REV",p[192],39);hexline("PARTITION_CONFIG",p[179],40);
    hexline("SECTOR_COUNT",sectors,41);hexline("DATA_SECTOR_SIZE",p[61],42);
    if((p[179]&7)||p[61]||p[192]<5||p[192]>8||sectors<2) {
        text("SECTOR READ SKIPPED - EXT_CSD GUARD",44);return;
    }
    if(!emmc_data_read(17,0,buf,44)) {text("LBA0 FAILED - STOPPED",49);return;}
    hexline("MBR SIGNATURE",p[510]|((uint32_t)p[511]<<8),49);
    if(p[510]!=0x55||p[511]!=0xaa) {text("MBR GUARD FAILED - STOPPED",50);return;}
    if(!emmc_data_read(17,1,buf,51)) {text("LBA1 FAILED - STOPPED",56);return;}
    unsigned n=le32(p+12);
    if(le32(p)!=0x20494645u||le32(p+4)!=0x54524150u||
       n<92||n>512||le32(p+24)!=1||le32(p+28)) {
        text("GPT HEADER GUARD FAILED",56);return;
    }
    uint32_t stored=le32(p+16),calculated=header_crc(p,n);
    hexline("GPT HEADER CRC STORED",stored,56);
    hexline("GPT HEADER CRC COMPUTED",calculated,57);
    text(stored==calculated?"GPT HEADER CRC MATCH - FIRST SECTORS READ":"GPT HEADER CRC MISMATCH",59);
#if A03_EMMC_SNAPSHOT >= 5
    if(stored==calculated)emmc_gpt_probe(p,sectors);
#endif
}
#endif
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
#if A03_EMMC_SNAPSHOT >= 5
    text("A03 EMMC 0020 GPT + CURRENT BOOT VALIDATION",3);
#elif A03_EMMC_SNAPSHOT == 4
    text("A03 EMMC 0017 SDMA READ - DOWNSTREAM PATH",3);
#elif A03_EMMC_SNAPSHOT == 3
    text("A03 EMMC 0016 PIO POLL-STAGE DIAGNOSTIC",3);
#elif A03_EMMC_SNAPSHOT == 2
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
#if A03_EMMC_SNAPSHOT >= 3
    if(emmc_status_probe())emmc_read_probe();
    text("READ PROBE COMPLETE - PAUSED FOR PHOTO",61);
#if A03_EMMC_SNAPSHOT >= 4
    text("SDMA TO PRIVATE RAM - NO STORAGE WRITES",62);
#else
    text("NO DMA OR STORAGE WRITES",62);
#endif
#elif A03_EMMC_SNAPSHOT == 2
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
    if(!a03_memory_profile_valid(p->phys,p->mem)||p->entry<p->base||p->end<p->base||p->end-p->base>=p->mem||p->entry>=p->end||p->adtlen>0x100000||!p->adtlen||p->cmdline[607])return fail;
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
    unsigned char *smp=0;
    if(!a03_dt_smp_handoff((unsigned char*)dt,(uint32_t)p->adtlen,&smp))return fail;
    if(smp) {
        uint64_t target=a03_smp_u64(smp+8);
        uintptr_t low=(uintptr_t)a03_smp_trampoline;
        if(a03_smp_u64(smp)!=0 || low<UINT64_C(0x80000000) || low>=UINT64_C(0x100000000) || (low&15))return fail;
        unsigned found=0;
        for(unsigned i=0;i<p->count;i++) {
            const struct segment *s=&p->seg[i];
            uint64_t begin=p->phys+s->va-p->base;
            if(target>=begin && target-begin<s->filesize && !(target&3))found=1;
        }
        if(!found)return fail;
        a03_smp_put64((unsigned char*)a03_smp_target,target);
        a03_smp_put64(smp,low);
        clean(low,(uintptr_t)a03_smp_target+8);
    }

    volatile struct bootargs *a=(volatile struct bootargs*)ba;
    a->rev=2;a->version=2;a->virt=p->base;a->phys=p->phys;a->mem=p->mem;a->top=ba+16384;
    a->video=(struct video){0x9e000000,1,2880,720,1600,32};
    a->dt=p->base+dt-p->phys;a->dtlen=p->adtlen;a->actual=p->mem;
    for(unsigned i=0;i<608;i++)a->cmdline[i]=p->cmdline[i];
    clean(dt,ba+16384);
    text("JUMP TO XNU 8796 - NATIVE 16K",1);
    return (struct handoff){p->phys+p->entry-p->base,ba};
}
