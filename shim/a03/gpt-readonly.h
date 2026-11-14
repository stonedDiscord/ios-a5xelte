/* Bounded primary-GPT validation. No I/O or card-state changes here. */
#ifndef A03_GPT_READONLY_H
#define A03_GPT_READONLY_H
#include <stdint.h>
struct a03_gpt {
    uint32_t array_lba, count, array_crc, first, last;
    uint32_t boot, boot_count, userdata, userdata_count;
};
static uint32_t a03_le32(const unsigned char *p) {
    return p[0]|((uint32_t)p[1]<<8)|((uint32_t)p[2]<<16)|((uint32_t)p[3]<<24);
}
static uint64_t a03_le64(const unsigned char *p) {
    return a03_le32(p)|((uint64_t)a03_le32(p+4)<<32);
}
static uint32_t a03_crc_update(uint32_t crc,const unsigned char *p,unsigned n) {
    for(unsigned i=0;i<n;i++) {
        crc^=p[i];
        for(unsigned b=0;b<8;b++)crc=(crc>>1)^(0xedb88320u&(0u-(crc&1)));
    }
    return crc;
}
static unsigned a03_gpt_header(const unsigned char *p,uint32_t sectors,struct a03_gpt *g) {
    unsigned n=a03_le32(p+12);
    if(a03_le64(p)!=0x5452415020494645ULL||a03_le32(p+8)!=0x10000||
       n<92||n>512||a03_le32(p+20)||a03_le64(p+24)!=1||sectors<3)return 0;
    uint32_t crc=a03_crc_update(~0u,p,16);
    const unsigned char z[4]={0,0,0,0};
    crc=a03_crc_update(crc,z,4);crc=a03_crc_update(crc,p+20,n-20);
    if(~crc!=a03_le32(p+16))return 0;
    uint64_t first=a03_le64(p+40),last=a03_le64(p+48),array=a03_le64(p+72);
    uint64_t backup=a03_le64(p+32);
    uint32_t count=a03_le32(p+80);
    /* The A03 layout uses 128-byte entries, at most 128 (32 sectors). */
    if(a03_le32(p+84)!=128||count<55||count>128||array<2||
       first>=last||backup>=sectors||backup<=last||first>=sectors||
       array>=first||(count+3)/4>first-array||
       (count+3)/4>=backup-last)return 0;
    *g=(struct a03_gpt){(uint32_t)array,count,a03_le32(p+88),
        (uint32_t)first,(uint32_t)last,0,0,0,0};
    return 1;
}
static unsigned a03_gpt_name(const unsigned char *entry,const char *name) {
    for(unsigned i=0;i<36;i++) {
        if(entry[56+i*2]!=(unsigned char)*name||entry[57+i*2])return 0;
        if(!*name)return 1;
        name++;
    }
    return 0;
}
/* Reader returns a single 512-byte sector, stopping immediately on failure.
 * Error 1=read, 2=range/overlap, 3=identity, 4=array CRC, 5=missing labels. */
static unsigned a03_gpt_entries(struct a03_gpt *g,
    unsigned (*read_sector)(void *,uint32_t,unsigned char *),void *context,
    uint32_t *computed) {
    unsigned char sector[512];
    uint32_t starts[128],ends[128],crc=~0u;unsigned used=0;
    for(unsigned i=0;i<g->count;i++) {
        if(!(i%4)) {
            if(!read_sector(context,g->array_lba+i/4,sector))return 1;
            unsigned remain=g->count-i;
            crc=a03_crc_update(crc,sector,remain<4?remain*128:512);
        }
        const unsigned char *e=sector+(i%4)*128;unsigned type=0,guid=0;
        for(unsigned j=0;j<16;j++) {type|=e[j];guid|=e[16+j];}
        if(!type)continue;
        uint64_t start=a03_le64(e+32),end=a03_le64(e+40);
        if(!guid||start<g->first||end>g->last||end<start)return 2;
        for(unsigned j=0;j<used;j++)if(start<=ends[j]&&starts[j]<=end)return 2;
        starts[used]=(uint32_t)start;ends[used++]=(uint32_t)end;
        if(a03_gpt_name(e,"boot")) {
            if(g->boot||i!=38||start!=483328||end-start+1!=131072)return 3;
            g->boot=(uint32_t)start;g->boot_count=(uint32_t)(end-start+1);
        }
        if(a03_gpt_name(e,"userdata")) {
            if(g->userdata||i!=54||start!=15929344||end!=g->last)return 3;
            g->userdata=(uint32_t)start;g->userdata_count=(uint32_t)(end-start+1);
        }
    }
    *computed=~crc;
    if(*computed!=g->array_crc)return 4;
    if(!g->boot||!g->userdata)return 5;
    return 0;
}
#endif
