#!/usr/bin/env python3
"""Test actual pre-write firmware validator using synthetic data only.

Optional private image argument validates locally; no file contents emitted.
"""
from pathlib import Path
import subprocess,tempfile,sys
ROOT=Path(__file__).resolve().parents[1]
SOURCE=r'''
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "shim/a03/jd9365t-firmware.h"
static void entry(uint8_t*p,unsigned offset,unsigned target){p[0]=0;p[1]=offset>>16;p[2]=offset>>8;p[3]=offset;p[4]=0;p[5]=15;p[6]=target>>24;p[7]=target>>16;p[8]=target>>8;p[9]=target;}
int main(int argc,char**argv){
 struct a03_jd_firmware out,saved;uint8_t p[288]={0};p[3]=27;
 for(unsigned i=256;i<288;i++)p[i]=(uint8_t)i;
 entry(p+5,256,0);entry(p+17,272,0x20002000);
 for(unsigned i=0;i<2;i++){uint16_t c=a03_jd_crc16(p+256+16*i,16);p[15+12*i]=c>>8;p[16+12*i]=c;}
 assert(a03_jd_crc16((const uint8_t*)"123456789",9)==0xaee7);
 assert(!a03_jd_firmware_validate(p,sizeof(p),&out)&&out.count==2);saved=out;
 for(size_t n=0;n<sizeof(p);n++)assert(a03_jd_firmware_validate(p,n,&out)==-1);
 assert(!memcmp(&out,&saved,sizeof(out)));
 p[256]^=1;assert(a03_jd_firmware_validate(p,sizeof(p),&out)==-1);p[256]^=1;
 p[5]=1;assert(a03_jd_firmware_validate(p,sizeof(p),&out)==-1);p[5]=0;
 entry(p+17,272,0);assert(a03_jd_firmware_validate(p,sizeof(p),&out)==-1);
 entry(p+17,272,0x40000200);assert(a03_jd_firmware_validate(p,sizeof(p),&out)==-1);
 entry(p+17,272,0xfff8);assert(a03_jd_firmware_validate(p,sizeof(p),&out)==-1);
 assert(a03_jd_firmware_validate(NULL,288,&out)==-1);assert(a03_jd_firmware_validate(p,288,NULL)==-1);
 if(argc>1){FILE*f=fopen(argv[1],"rb");assert(f);uint8_t*blob=(uint8_t*)malloc(81921);assert(blob);size_t n=fread(blob,1,81921,f);assert(!ferror(f)&&feof(f));fclose(f);assert(!a03_jd_firmware_validate(blob,n,&out));printf("Private firmware validates: %zu bytes, %u moves; compatibility unverified\n",n,out.count);free(blob);}
}
'''
with tempfile.TemporaryDirectory(prefix='a03-jd-firmware-') as d:
 p=Path(d);(p/'test.c').write_text(SOURCE)
 for cc,std,lang in [('clang','c11','c'),('clang++','c++17','c++')]:
  subprocess.run([cc,'-x',lang,'-std='+std,'-Wall','-Wextra','-Werror','-Wno-missing-field-initializers','-fsanitize=address,undefined','-I',str(ROOT),str(p/'test.c'),'-o',str(p/'test')],check=True)
  subprocess.run([str(p/'test')]+sys.argv[1:],check=True)
print('PASS actual pre-write firmware validator C/C++ ASan/UBSan: stock moves/CRC, truncation, corruption, RAM bounds/overlap, unknown command')
