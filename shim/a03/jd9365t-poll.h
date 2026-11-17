/* Explicit bounded contact poll session; no scheduling or firmware loading.
 * Caller owns a ROM9383 bus with running firmware. Frame read errors cannot
 * produce contacts; three consecutive failed samples release all contacts.
 */
#ifndef A03_JD9365T_POLL_H
#define A03_JD9365T_POLL_H
#include "jd9365t-memory.h"
#include "jd9365t-sections.h"
#include "jd9365t-contact-state.h"
#ifndef A03_JD_POLL_TRACE
#define A03_JD_POLL_TRACE(i,p) ((void)0)
#endif
static inline int a03_jd_poll_slice(struct a03_jd_bus *b,unsigned frames,
    struct a03_jd_contact_state *state,int release,
    a03_jd_contact_emit emit,void *context,unsigned *valid_out)
{
 if(valid_out)*valid_out=0;
 if(!b||!b->delay_us||!state||!emit||!frames||frames>300)return -1;
 uint16_t id;if(a03_jd_rom_id(b,&id)) {
  for(unsigned i=0;i<3;i++)(void)a03_jd_contact_update(state,0,NULL,0,emit,context);
  return -2;
 }
 const uint8_t enter[]={0xf2,0xaa,0x55,0x0f,0xf0,0x68};
 const uint8_t leave[]={0xf2,0xaa,0x88,0,0,0};
 uint8_t table[160],config[6],packet[60];struct a03_jd_sections sections;
 int result=-3;unsigned valid=0;
 if(a03_jd_write(b,enter,sizeof(enter)))goto done;
 if(a03_jd_ram_read(b,0x20011000,table,sizeof(table))||
    a03_jd_decode_sections(table,sizeof(table),&sections))goto done;
 if(sections.firmware_config.address<0x20000000u||
    !a03_jd_ram_range(sections.firmware_config.address,sections.firmware_config.length,1)||
    sections.coordinate_report.address<0x20011000u||
    !a03_jd_ram_range(sections.coordinate_report.address,60,0))goto done;
 if(a03_jd_ram_read(b,sections.firmware_config.address,config,sizeof(config))||
    ((unsigned)config[0]|((unsigned)config[1]<<8))!=720||
    ((unsigned)config[2]|((unsigned)config[3]<<8))!=1600||config[4]!=18||config[5]!=32)goto done;
 if(a03_jd_write(b,leave,sizeof(leave)))goto done;
 result=0;
 for(unsigned i=0;i<frames;i++) {
  /* Match stock ReadRegMulti: enter/read/exit each sample, letting the
   * firmware run outside diagnostic mode between frames. */
  int ok=!a03_jd_write(b,enter,sizeof(enter));
  if(ok)ok=!a03_jd_ram_read(b,sections.coordinate_report.address,packet,sizeof(packet));
  if(a03_jd_write(b,leave,sizeof(leave)))ok=0;
  if(ok) {
   A03_JD_POLL_TRACE(i,packet);
   unsigned nonzero=0;
   for(unsigned j=0;j<sizeof(packet);j++)nonzero|=packet[j];
   /* A wholly zero report cannot establish ten real corner contacts. A
    * genuine (0,0) slot remains valid within a nonzero complete packet. */
   if(!nonzero)ok=0;
  }
  if(!a03_jd_contact_update(state,ok,packet,sizeof(packet),emit,context))valid++;
  else if(state->failures>=3){result=-4;break;}
  b->delay_us(b->context,16000);
 }
done:
 if(a03_jd_write(b,leave,sizeof(leave))&&!result)result=-5;
 /* Continuing slices retain contacts; stopping or any failed slice releases
  * once. Ordinary bounded diagnostics preserve their final-release policy. */
 if(release||result)for(unsigned i=0;i<3;i++)
  (void)a03_jd_contact_update(state,0,NULL,0,emit,context);
 if(valid_out)*valid_out=valid;
 return result;
}
static inline int a03_jd_poll(struct a03_jd_bus *b,unsigned frames,
    a03_jd_contact_emit emit,void *context,unsigned *valid_out)
{
 struct a03_jd_contact_state state={{{0,0,0,0}},0};
 return a03_jd_poll_slice(b,frames,&state,1,emit,context,valid_out);
}
#endif
