#!/usr/bin/env python3
"""Compile the actual section decoder with synthetic stock-layout tables."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
SOURCE=r'''
#include <assert.h>
#include <string.h>
#include "shim/a03/jd9365t-sections.h"
static void put(uint8_t *p,uint32_t v){for(unsigned i=0;i<4;i++)p[i]=v>>(8*i);}
int main(void){
 uint8_t p[160]={0};struct a03_jd_sections r,saved;
 p[0]=0x5a;p[1]=0xa5;
 put(p+28,0x20002000);put(p+32,64);
 put(p+152,0x20011200);put(p+156,60);
 assert(!a03_jd_decode_sections(p,sizeof(p),&r));
 assert(r.firmware_config.address==0x20002000 && r.firmware_config.length==64);
 assert(r.coordinate_report.address==0x20011200 && r.coordinate_report.length==60);
 saved=r;
 for(size_t n=0;n<160;n++)assert(a03_jd_decode_sections(p,n,&r)==-1);
 assert(!memcmp(&r,&saved,sizeof(r)));
 assert(a03_jd_decode_sections(NULL,160,&r)==-1);
 assert(a03_jd_decode_sections(p,160,NULL)==-1);
 p[0]=0xa5;p[1]=0x5a;assert(a03_jd_decode_sections(p,160,&r)==-1);
 p[0]=0x5a;p[1]=0xa5;
 put(p+32,5);assert(a03_jd_decode_sections(p,160,&r)==-1);put(p+32,64);
 for(unsigned n=0;n<256;n++){if(n==60)continue;put(p+156,n);assert(a03_jd_decode_sections(p,160,&r)==-1);}
 put(p+156,60);put(p+152,0);assert(a03_jd_decode_sections(p,160,&r)==-1);
 put(p+152,0xfffffff0);assert(a03_jd_decode_sections(p,160,&r)==-1);
 assert(!memcmp(&r,&saved,sizeof(r)));
}
'''
with tempfile.TemporaryDirectory(prefix='a03-sections-') as directory:
 p=Path(directory);(p/'test.c').write_text(SOURCE)
 for cc,std,language in [('clang','c11','c'),('clang++','c++17','c++')]:
  subprocess.run([cc,'-x',language,'-std='+std,'-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I',str(ROOT),str(p/'test.c'),'-o',str(p/'test')],check=True)
  subprocess.run([str(p/'test')],check=True)
print('PASS actual section decoder: LE ready/addresses, fixed slots, lengths, bounds, wrap, unchanged failure output; C/C++ ASan/UBSan')
