/* Contact transition policy; caller provides verified complete coordinate
 * reports and serializes calls. No timers, bus access or HID side effects.
 * Three consecutive failed/malformed reads release held contacts once.
 */
#ifndef A03_JD9365T_CONTACT_STATE_H
#define A03_JD9365T_CONTACT_STATE_H
#include "jd9365t-report.h"
struct a03_jd_contact_state {
 struct a03_jd9365t_contact contacts[A03_JD9365T_CONTACTS];
 unsigned failures;
};
typedef void (*a03_jd_contact_emit)(void *,unsigned,int,unsigned,unsigned);
static inline int a03_jd_contact_update(struct a03_jd_contact_state *state,
    int read_ok,const uint8_t *packet,size_t size,
    a03_jd_contact_emit emit,void *context)
{
 struct a03_jd9365t_report next;
 if(!state||!emit)return -1;
 if(!read_ok||a03_jd9365t_decode(packet,size,&next)) {
  if(state->failures<3)state->failures++;
  if(state->failures==3) {
   for(unsigned i=0;i<A03_JD9365T_CONTACTS;i++) {
    struct a03_jd9365t_contact *p=&state->contacts[i];
    if(p->down){emit(context,i,0,p->x,p->y);p->down=0;}
   }
  }
  return -1;
 }
 state->failures=0;
 for(unsigned i=0;i<A03_JD9365T_CONTACTS;i++) {
  struct a03_jd9365t_contact *old=&state->contacts[i],*n=&next.contacts[i];
  if(old->down!=n->down || (n->down&&(old->x!=n->x||old->y!=n->y)))
   emit(context,i,n->down,n->down?n->x:old->x,n->down?n->y:old->y);
  *old=*n;
 }
 return 0;
}
#endif
