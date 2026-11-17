/* JD9365T backdoor RAM transport. Caller owns an entered session and SPI bus.
 * RAM writes accept only PRAM[0,10000) or DRAM[20000000,20010000).
 * No peripheral registers, external flash commands or MCU controls here.
 */
#ifndef A03_JD9365T_MEMORY_H
#define A03_JD9365T_MEMORY_H
#include "jd9365t-spi.h"
static inline int a03_jd_ram_range(uint32_t address,size_t n,int write)
{
 uint32_t end;
 if(!n||n>0x10000)return 0;
 if(address<0x10000u)end=0x10000u;
 else if(address>=0x20000000u&&address<0x20010000u)end=0x20010000u;
 else if(!write&&address>=0x20011000u&&address<0x20012000u)end=0x20012000u;
 else return 0;
 return n<=end-address;
}
static inline int a03_jd_ram_read(struct a03_jd_bus *b,uint32_t address,
    uint8_t *out,size_t n)
{
 if(!b||!out||!a03_jd_ram_range(address,n,0))return -1;
 while(n) {
  uint8_t c[]={0xf3,(uint8_t)(address>>24),(uint8_t)(address>>16),
      (uint8_t)(address>>8),(uint8_t)address,1};
  size_t chunk=n>240?240:n;
  if(a03_jd_read(b,c,sizeof(c),out,chunk))return -1;
  address+=(uint32_t)chunk;out+=chunk;n-=chunk;
 }
 return 0;
}
static inline int a03_jd_ram_write(struct a03_jd_bus *b,uint32_t address,
    const uint8_t *data,size_t n)
{
 if(!b||!data||!a03_jd_ram_range(address,n,1))return -1;
 while(n) {
  uint8_t c[246]={0xf2,(uint8_t)(address>>24),(uint8_t)(address>>16),
      (uint8_t)(address>>8),(uint8_t)address,1};
  size_t chunk=n>240?240:n;
  for(size_t i=0;i<chunk;i++)c[6+i]=data[i];
  if(a03_jd_write(b,c,chunk+6))return -1;
  address+=(uint32_t)chunk;data+=chunk;n-=chunk;
 }
 return 0;
}
#endif
