#!/usr/bin/env python3
"""Exercise actual transition/error policy without hardware or HID."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
SOURCE=r'''
#include <assert.h>
#include <string.h>
#include "shim/a03/jd9365t-contact-state.h"
struct events {unsigned count,slot,down,x,y;};
static void emit(void*c,unsigned i,int d,unsigned x,unsigned y){struct events*e=(struct events*)c;e->count++;e->slot=i;e->down=d;e->x=x;e->y=y;}
static void point(uint8_t*p,unsigned i,unsigned x,unsigned y){p+=3+i*5;p[0]=x>>8;p[1]=x;p[2]=y>>8;p[3]=y;p[4]=10;}
int main(void){
 struct a03_jd_contact_state s;struct events e;memset(&s,0,sizeof(s));memset(&e,0,sizeof(e));uint8_t p[60];memset(p,255,sizeof(p));p[0]=1;
 point(p,9,720,1600);assert(!a03_jd_contact_update(&s,1,p,60,emit,&e));assert(e.count==1&&e.slot==9&&e.down&&e.x==720&&e.y==1600);
 assert(!a03_jd_contact_update(&s,1,p,60,emit,&e)&&e.count==1);
 point(p,9,0,0);assert(!a03_jd_contact_update(&s,1,p,60,emit,&e)&&e.count==2&&e.down&&e.x==0&&e.y==0);
 assert(a03_jd_contact_update(&s,0,NULL,0,emit,&e)==-1&&e.count==2);
 assert(a03_jd_contact_update(&s,1,p,59,emit,&e)==-1&&e.count==2);
 p[0]=11;assert(a03_jd_contact_update(&s,1,p,60,emit,&e)==-1&&e.count==3&&!e.down);
 for(unsigned i=0;i<10;i++)assert(a03_jd_contact_update(&s,0,NULL,0,emit,&e)==-1&&e.count==3);
 p[0]=1;assert(!a03_jd_contact_update(&s,1,p,60,emit,&e)&&e.count==4&&e.down&&!s.failures);
 memset(p+3,255,50);p[0]=0;assert(!a03_jd_contact_update(&s,1,p,60,emit,&e)&&e.count==5&&!e.down&&e.x==0&&e.y==0);
 assert(!a03_jd_contact_update(&s,1,p,60,emit,&e)&&e.count==5);
 point(p,0,10,20);point(p,9,30,40);p[0]=2;assert(!a03_jd_contact_update(&s,1,p,60,emit,&e)&&e.count==7);
 for(unsigned i=0;i<3;i++)a03_jd_contact_update(&s,0,NULL,0,emit,&e);
 assert(e.count==9&&!s.contacts[0].down&&!s.contacts[9].down);
 assert(a03_jd_contact_update(NULL,1,p,60,emit,&e)==-1);
 assert(a03_jd_contact_update(&s,1,p,60,NULL,&e)==-1);
}
'''
with tempfile.TemporaryDirectory(prefix='a03-jd-contact-') as d:
 p=Path(d);(p/'test.c').write_text(SOURCE)
 for cc,std,lang in [('clang','c11','c'),('clang++','c++17','c++')]:
  subprocess.run([cc,'-x',lang,'-std='+std,'-Wall','-Wextra','-Werror','-Wno-missing-field-initializers','-fsanitize=address,undefined','-I',str(ROOT),str(p/'test.c'),'-o',str(p/'test')],check=True)
  subprocess.run([str(p/'test')],check=True)
print('PASS actual contact policy C/C++ ASan/UBSan: sparse down/move/up, dedup, failed-read quarantine, bounded release, recovery, multitouch')
