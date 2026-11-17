/* Bounded polling SPI primitives for A03 Jadard bring-up.
 * Register behavior follows Samsung's spi-sprd.c; protocol follows JD9365T.
 * No controller reset, pinmux, touch firmware, flash or storage operations.
 * Callers serialize access, provide a running SPI clock and own chip select.
 */
#ifndef A03_JD9365T_SPI_H
#define A03_JD9365T_SPI_H
#include <stddef.h>
#include <stdint.h>

struct a03_jd_bus {
 void *context;
 uint32_t (*read32)(void *, unsigned);
 void (*write32)(void *, unsigned, uint32_t);
 uint8_t (*read8)(void *, unsigned);
 void (*write8)(void *, unsigned, uint8_t);
 void (*delay_us)(void *, unsigned);
};

static inline int a03_jd_wait(struct a03_jd_bus *b, unsigned reg,
    uint32_t mask, uint32_t wanted)
{
 for (unsigned i=0; i<10000; i++) {
  if ((b->read32(b->context,reg)&mask)==wanted) return 0;
  b->delay_us(b->context,1);
 }
 return -1;
}

/* Exactly one Linux-style transfer phase, retaining CS across phases/chunks.
 * Hardware four-wire TX starts on FIFO writes; RX starts via CTL4 bit9.
 */
static inline int a03_jd_phase(struct a03_jd_bus *b,
    const uint8_t *tx, uint8_t *rx, size_t length)
{
 if ((!tx == !rx) || !length || length>256) return -1;
 uint32_t ctl=b->read32(b->context,0x0c)&~0x3000u;
 b->write32(b->context,0x0c,ctl|(tx?0x2000u:0x1000u));
 for (size_t pos=0;pos<length;) {
  unsigned n=(unsigned)(length-pos);if(n>32)n=32;
  b->write32(b->context,0x24,0x300);
  if(tx) {
   b->write32(b->context,0x54,b->read32(b->context,0x54)&~15u);
   b->write32(b->context,0x58,n);
   for(unsigned i=0;i<n;i++)b->write8(b->context,0,tx[pos+i]);
   if(a03_jd_wait(b,0x28,0x100,0x100)||a03_jd_wait(b,0x34,0x100,0))goto fail;
  } else {
   b->write32(b->context,0x5c,b->read32(b->context,0x5c)&~15u);
   b->write32(b->context,0x60,n);
   uint32_t r=b->read32(b->context,0x18)&~0x3ffu;
   b->write32(b->context,0x18,r);
   b->write32(b->context,0x18,r|n);
   b->write32(b->context,0x18,r|n|0x200);
   if(a03_jd_wait(b,0x28,0x200,0x200))goto fail;
   for(unsigned i=0;i<n;i++)rx[pos+i]=b->read8(b->context,0);
  }
  pos+=n;
 }
 b->write32(b->context,0x24,0x300);
 b->write32(b->context,0x0c,ctl);
 return 0;
fail:
 b->write32(b->context,0x0c,ctl);
 return -1;
}

static inline void a03_jd_cs(struct a03_jd_bus *b,int active)
{
 uint32_t v=b->read32(b->context,8)|0xf00u;
 /* Matching Linux set_cs always drives hardware CS0, even spi_device CS1. */
 b->write32(b->context,8,active?v&~0x100u:v);
}

static inline int a03_jd_write(struct a03_jd_bus *b,const uint8_t *p,size_t n)
{
 a03_jd_cs(b,1);int e=a03_jd_phase(b,p,NULL,n);a03_jd_cs(b,0);return e;
}

static inline int a03_jd_read(struct a03_jd_bus *b,const uint8_t *cmd,
    size_t n,uint8_t *out,size_t count)
{
 a03_jd_cs(b,1);int e=a03_jd_phase(b,cmd,NULL,n);
 if(!e)e=a03_jd_phase(b,NULL,out,count);
 a03_jd_cs(b,0);return e;
}

/* Stock diagnostic session: enter, read only ROM ID2/3, always attempt exit.
 * Address0x40008076; bytes83/93 => ROM ID9383. No MCU reset or firmware write.
 * Return distinguishes transport from a readable but different chip ID.
 */
static inline int a03_jd_rom_id(struct a03_jd_bus *b,uint16_t *id)
{
 const uint8_t enter[]={0xf2,0xaa,0x55,0x0f,0xf0,0x68};
 const uint8_t readid[]={0xf3,0x40,0x00,0x80,0x76,0x01};
 const uint8_t leave[]={0xf2,0xaa,0x88,0,0,0};
 uint8_t r[2]={0};
 int e=a03_jd_write(b,enter,sizeof(enter));
 if(!e)e=a03_jd_read(b,readid,sizeof(readid),r,sizeof(r));
 int exit_error=a03_jd_write(b,leave,sizeof(leave));
 if(e||exit_error)return -1;
 *id=(uint16_t)((unsigned)r[0]|((unsigned)r[1]<<8));
 return *id==0x9383?0:-2;
}
#endif
