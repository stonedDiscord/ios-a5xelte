/* Validate a complete private JD9365T RAM firmware before any device write.
 * Format/CRC: Samsung GetMoveInfoNumber/GetHeaderInfo/GetDataCRC16.
 * No bus access. This validates structure, not board/panel compatibility.
 */
#ifndef A03_JD9365T_FIRMWARE_H
#define A03_JD9365T_FIRMWARE_H
#include <stddef.h>
#include <stdint.h>
#define A03_JD_MOVES_MAX 20u
struct a03_jd_move {uint32_t offset,address;uint32_t length;uint16_t crc;};
struct a03_jd_firmware {unsigned count;struct a03_jd_move moves[A03_JD_MOVES_MAX];};
static inline uint16_t a03_jd_crc16(const uint8_t *p,size_t n)
{
 uint16_t crc=0xffff;
 for(size_t i=0;i<n;i++) {
  crc^=(uint16_t)((unsigned)p[i]<<8);
  for(unsigned bit=0;bit<8;bit++)crc=(uint16_t)(((unsigned)crc<<1)^((crc&0x8000)?0x8005u:0));
 }
 return crc;
}
static inline int a03_jd_firmware_validate(const uint8_t *p,size_t size,
    struct a03_jd_firmware *out)
{
 struct a03_jd_firmware next={0};
 if(!p||!out||size<5||size>80u*1024u||p[3]<14||p[3]==255)return -1;
 next.count=(p[3]-2u)/12u;
 size_t end=5+12*next.count;
 if(!next.count||next.count>A03_JD_MOVES_MAX||end>size||end>256)return -1;
 for(unsigned i=0;i<next.count;i++) {
  const uint8_t *e=p+5+12*i;struct a03_jd_move *m=&next.moves[i];
  /* Current stock RAM images use move command0. Unknown commands refused. */
  if(e[0])return -1;
  m->offset=((uint32_t)e[1]<<16)|((uint32_t)e[2]<<8)|e[3];
  m->length=(((uint32_t)e[4]<<8)|e[5])+1;
  m->address=((uint32_t)e[6]<<24)|((uint32_t)e[7]<<16)|((uint32_t)e[8]<<8)|e[9];
  m->crc=(uint16_t)(((unsigned)e[10]<<8)|e[11]);
  if(m->offset<end||m->offset>size||m->length>size-m->offset)return -1;
  uint32_t limit;
  if(m->address<0x10000u)limit=0x10000u;
  else if(m->address>=0x20000000u&&m->address<0x20010000u)limit=0x20010000u;
  else return -1;
  if(m->length>limit-m->address)return -1;
  for(unsigned j=0;j<i;j++) {
   const struct a03_jd_move *a=&next.moves[j];
   if(m->address<a->address+a->length && a->address<m->address+m->length)return -1;
  }
  if(a03_jd_crc16(p+m->offset,m->length)!=m->crc)return -1;
 }
 *out=next;return 0;
}
#endif
