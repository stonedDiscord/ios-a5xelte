/* Temporary RAM-only startup, following stock HostWritePram.
 * No external-flash erase/program commands. Validate ALL moves before bus
 * access. Caller identifies ROM9383, owns SPI and provides bounded delay.
 * On failure after stop, keep touch MCU stopped rather than run partial RAM.
 */
#ifndef A03_JD9365T_LOADER_H
#define A03_JD9365T_LOADER_H
#include "jd9365t-memory.h"
#include "jd9365t-firmware.h"
static inline int a03_jd_control_write(struct a03_jd_bus *b,uint32_t a,
    const uint8_t *p,size_t n)
{
 /* Only exact stock RAM-start/CRC controls. No generic peripheral writes. */
 if(!b||!p)return -1;
 int allowed=(n==1&&(a==0x40000042u||a==0x4000810du||a==0x4000020eu||
     a==0x20011000u||a==0x40008014u||a==0x40008016u||a==0x40008012u||a==0x40000217u)) ||
     (n==2&&a==0x40000218u)||(n==13&&a==0x40000200u&&p[12]==3);
 if(!allowed)return -1;
 uint8_t c[19]={0xf2,(uint8_t)(a>>24),(uint8_t)(a>>16),(uint8_t)(a>>8),(uint8_t)a,1};
 for(size_t i=0;i<n;i++)c[6+i]=p[i];
 return a03_jd_write(b,c,n+6);
}
static inline int a03_jd_control_byte(struct a03_jd_bus *b,uint32_t a,uint8_t v)
{ return a03_jd_control_write(b,a,&v,1); }
static inline int a03_jd_control_read(struct a03_jd_bus *b,uint32_t a,uint8_t *p,size_t n)
{
 if(!((a==0x4000021du&&n==1)||(a==0x4000021au&&n==2)))return -1;
 uint8_t c[]={0xf3,(uint8_t)(a>>24),(uint8_t)(a>>16),(uint8_t)(a>>8),(uint8_t)a,1};
 return a03_jd_read(b,c,sizeof(c),p,n);
}
static inline void a03_jd_put32(uint8_t *p,uint32_t n)
{ for(unsigned i=0;i<4;i++)p[i]=(uint8_t)(n>>(i*8)); }
static inline int a03_jd_load_ram(struct a03_jd_bus *b,const uint8_t *data,
    size_t size)
{
 struct a03_jd_firmware f;
 if(a03_jd_firmware_validate(data,size,&f))return -2;
 uint16_t id=0;if(a03_jd_rom_id(b,&id))return -3;
 const uint8_t enter[]={0xf2,0xaa,0x55,0x0f,0xf0,0x68};
 const uint8_t leave[]={0xf2,0xaa,0x88,0,0,0};
 int e=a03_jd_write(b,enter,sizeof(enter));
 if(e)goto done;
 if(a03_jd_control_byte(b,0x40000042,0)||a03_jd_control_byte(b,0x4000810d,0)||
    a03_jd_control_byte(b,0x4000020e,0)||a03_jd_control_byte(b,0x20011000,0)||
    a03_jd_control_byte(b,0x40008014,0)||a03_jd_control_byte(b,0x40008016,0x5a)) {e=-4;goto done;}
 for(unsigned i=0;i<f.count;i++) {
  struct a03_jd_move *m=&f.moves[i];uint8_t params[13],crcbytes[2];
  if(a03_jd_ram_write(b,m->address,data+m->offset,m->length)){e=-5;goto done;}
  const uint8_t initial[]={0xff,0xff};
  if(a03_jd_control_write(b,0x40000218,initial,2)||a03_jd_control_byte(b,0x40000217,1)){e=-6;goto done;}
  a03_jd_put32(params,m->address);a03_jd_put32(params+4,m->length);a03_jd_put32(params+8,m->address);params[12]=3;
  if(a03_jd_control_write(b,0x40000200,params,13)){e=-7;goto done;}
  unsigned attempt;
  for(attempt=0;attempt<25;attempt++) {
   uint8_t status;b->delay_us(b->context,2000);
   if(a03_jd_control_read(b,0x4000021d,&status,1)){e=-8;goto done;}
   if(!(status&1))break;
  }
  if(attempt==25){e=-9;goto done;}
  if(a03_jd_control_read(b,0x4000021a,crcbytes,2)){e=-10;goto done;}
  /* Stock CRC_CODE_POSITION: low byte0/high byte1. */
  if(((unsigned)crcbytes[0]|((unsigned)crcbytes[1]<<8))!=m->crc){e=-11;goto done;}
 }
 if(a03_jd_control_byte(b,0x40008012,0xa5)||a03_jd_control_byte(b,0x40008016,0xa5)||
    a03_jd_control_byte(b,0x40008014,0xf1)){e=-12;goto done;}
 b->delay_us(b->context,50000);
 e=0;
done:
 if(e) {
  /* Best effort stop: never deliberately start a partially loaded image. */
  (void)a03_jd_control_byte(b,0x40008014,0);
  (void)a03_jd_control_byte(b,0x40008016,0x5a);
 }
 if(a03_jd_write(b,leave,sizeof(leave))&&!e)e=-13;
 return e;
}
#endif
