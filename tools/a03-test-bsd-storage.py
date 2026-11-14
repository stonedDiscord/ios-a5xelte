#!/usr/bin/env python3
"""Run the actual A03 BSD request handlers against a deterministic fake disk.

This does not emulate XNU, MMIO, DMA, caches or the phone. It checks
request boundaries, write rejection and completion/residual behavior.
"""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = (ROOT/'xnu/a03/a03_emmc.c').read_text()
    # Extract production handlers verbatim, replacing only OS/hardware APIs.
    begin = source.index('static uint32_t part_first(')
    end = source.index('static int emmc_ioctl(', begin)
    handlers = source[begin:end]
    ioctl_end = source.index('/* XNU specfs', end)
    handlers += source[end:ioctl_end]
    raw_begin = source.index('static int emmc_read(')
    raw_end = source.index('static const struct bdevsw', raw_begin)
    handlers += source[raw_begin:raw_end]
    size_begin = source.index('static int emmc_psize(')
    size_end = source.index(chr(10), size_begin)
    handlers += source[size_begin:size_end] + chr(10)
    stub = r'''
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define __unused __attribute__((unused))
typedef unsigned dev_t;
typedef unsigned long u_long;
typedef char *caddr_t;
struct proc;
#define minor(d) (d)
#define FWRITE 2
#define B_READ 1
#define B_PHYS 0x20
#define ENXIO 6
#define EROFS 30
#define EINVAL 22
#define EIO 5
#define ENOTTY 25
#define ENOMEM 12
enum {DKIOCGETBLOCKSIZE=1,DKIOCGETPHYSICALBLOCKSIZE,DKIOCSETBLOCKSIZE,
      DKIOCGETBLOCKCOUNT,DKIOCISWRITABLE,DKIOCGETMAXBLOCKCOUNTREAD,
      DKIOCGETMAXBLOCKCOUNTWRITE,DKIOCSYNCHRONIZECACHE,DKIOCSYNCHRONIZE};
#define MIN(a,b) ((a)<(b)?(a):(b))
struct request {
    dev_t dev;int flags,error,completed,mapped;int64_t block;
    uint32_t count,resid;char data[16896];
};
typedef struct request *buf_t;
static struct {
    bool ready,poisoned,writable;
    struct {uint32_t boot,boot_count,userdata,userdata_count;} gpt;
} ae;
static int a03_emmc_lock,lock_depth,read_calls,fail_call,map_fail;
static int write_calls,write_fail;static uint32_t write_lba;static unsigned char written[512];
static uint32_t requested[40];
struct uio {int64_t offset,resid;unsigned copied;int fail;char data[16896];};
typedef struct uio *uio_t;
static bool copying_in;
static uio_t uio_duplicate(uio_t u) {uio_t c=malloc(sizeof(*c));if(c)*c=*u;return c;}
static void uio_free(uio_t u) {free(u);}
static void uio_update(uio_t u,unsigned n) {u->offset+=n;u->resid-=n;u->copied+=n;}
static int64_t uio_offset(struct uio *u) {return u->offset;}
static int64_t uio_resid(struct uio *u) {return u->resid;}
static int uiomove(const char *p,int n,struct uio *u) {
    assert(lock_depth==0);assert(n>0);assert(u->copied+(unsigned)n<=sizeof(u->data));
    if(u->fail)return 14;
    if(copying_in)memcpy((char *)p,u->data+u->copied,(unsigned)n);
    else memcpy(u->data+u->copied,p,(unsigned)n);
    u->copied+=(unsigned)n;
    u->resid-=n;u->offset+=n;return 0;
}
static uint32_t buf_count(buf_t b) {return b->count;}
static dev_t buf_device(buf_t b) {return b->dev;}
static int buf_flags(buf_t b) {return b->flags;}
static int64_t buf_blkno(buf_t b) {return b->block;}
static void buf_setresid(buf_t b,uint32_t n) {b->resid=n;}
static void buf_seterror(buf_t b,int n) {b->error=n;}
static void buf_biodone(buf_t b) {b->completed++;}
static int buf_map(buf_t b,caddr_t *p) {
    if(map_fail)return -1;
    b->mapped++;*p=b->data;return 0;
}
static void buf_unmap(buf_t b) {assert(b->mapped==1);b->mapped--;}
static void lck_mtx_lock(int *p) {(void)p;assert(lock_depth++==0);}
static void lck_mtx_unlock(int *p) {(void)p;assert(--lock_depth==0);}
static int data_read(unsigned cmd,uint32_t lba,unsigned char *p) {
    assert(lock_depth==1);assert(cmd==17);assert(read_calls<40);
    requested[read_calls++]=lba;
    if(read_calls==fail_call)return EIO;
    for(unsigned i=0;i<512;i++)p[i]=(unsigned char)(lba+i);
    return 0;
}
static int data_write(uint32_t lba,const unsigned char *p) {
    assert(lock_depth==1);assert(ae.writable);
    assert(lba>=ae.gpt.userdata&&lba-ae.gpt.userdata<ae.gpt.userdata_count);
    write_calls++;if(write_calls==write_fail)return EIO;
    write_lba=lba;memcpy(written,p,512);return 0;
}
'''
    tests = r'''
static struct request req(dev_t dev,int64_t block,uint32_t n,int flags) {
    struct request b={.dev=dev,.block=block,.count=n,.flags=flags};
    memset(b.data,0xa5,sizeof(b.data));
    read_calls=0;fail_call=0;map_fail=0;return b;
}
static void check_done(struct request *b,int error,uint32_t resid,int reads) {
    assert(b->completed==1);assert(b->error==error);assert(b->resid==resid);
    assert(b->mapped==0);assert(lock_depth==0);assert(read_calls==reads);
}
int main(void) {
    ae.ready=true;ae.gpt.boot=483328;ae.gpt.boot_count=131072;
    ae.gpt.userdata=15929344;ae.gpt.userdata_count=106213336;
    assert(emmc_open(0,0,0,NULL)==0);
    assert(emmc_open(1,FWRITE,0,NULL)==EROFS);
    assert(emmc_open(2,0,0,NULL)==ENXIO);
    assert(emmc_close(0,0,0,NULL)==0);
    uint32_t geometry=0;uint64_t capacity=0;
    assert(emmc_ioctl(0,DKIOCGETBLOCKSIZE,(caddr_t)&geometry,0,NULL)==0&&geometry==512);
    assert(emmc_ioctl(1,DKIOCGETPHYSICALBLOCKSIZE,(caddr_t)&geometry,0,NULL)==0&&geometry==512);
    assert(emmc_ioctl(0,DKIOCSETBLOCKSIZE,(caddr_t)&geometry,FWRITE,NULL)==0);
    geometry=4096;
    assert(emmc_ioctl(0,DKIOCSETBLOCKSIZE,(caddr_t)&geometry,FWRITE,NULL)==EINVAL);
    assert(emmc_ioctl(0,DKIOCGETBLOCKCOUNT,(caddr_t)&capacity,0,NULL)==0&&capacity==ae.gpt.boot_count);
    assert(emmc_ioctl(1,DKIOCGETBLOCKCOUNT,(caddr_t)&capacity,0,NULL)==0&&capacity==ae.gpt.userdata_count);
    geometry=1;
    assert(emmc_ioctl(0,DKIOCISWRITABLE,(caddr_t)&geometry,0,NULL)==0&&geometry==0);
    assert(emmc_ioctl(0,DKIOCGETMAXBLOCKCOUNTWRITE,(caddr_t)&capacity,0,NULL)==0&&capacity==0);
    assert(emmc_ioctl(0,DKIOCGETMAXBLOCKCOUNTREAD,(caddr_t)&capacity,0,NULL)==0&&capacity==128);
    assert(emmc_ioctl(2,DKIOCGETBLOCKCOUNT,(caddr_t)&capacity,0,NULL)==ENXIO);
    assert(emmc_ioctl(0,999,(caddr_t)&capacity,0,NULL)==ENOTTY);
    /* XNU specfs d_psize returns the device block size. */
    assert(emmc_psize(0)==512&&emmc_psize(1)==512&&emmc_psize(2)==-1);
    ae.ready=false;assert(emmc_psize(0)==-1);ae.ready=true;
    const unsigned page_size=16384;
    unsigned sector_size=(unsigned)emmc_psize(0);
    assert(sector_size<=page_size&&page_size%sector_size==0);
    unsigned bscale=page_size/sector_size;assert(bscale==32);
    struct request page=req(0,0,bscale*sector_size,B_READ);
    emmc_strategy(&page);check_done(&page,0,0,32);
    assert(requested[0]==ae.gpt.boot&&requested[31]==ae.gpt.boot+31);
    for(unsigned i=0;i<page_size;i++)
        assert((unsigned char)page.data[i]==(unsigned char)(ae.gpt.boot+i/512+i%512));
    assert((unsigned char)page.data[page_size]==0xa5);
    struct request b=req(0,0,1025,B_READ);emmc_strategy(&b);
    check_done(&b,0,0,3);assert(requested[0]==ae.gpt.boot);
    assert(requested[2]==ae.gpt.boot+2);
    for(unsigned i=0;i<1025;i++)
        assert((unsigned char)b.data[i]==(unsigned char)(ae.gpt.boot+i/512+i%512));
    assert((unsigned char)b.data[1025]==0xa5);
    b=req(1,4,512,B_READ);emmc_strategy(&b);check_done(&b,0,0,1);
    assert(requested[0]==ae.gpt.userdata+4);
    b=req(0,131071,512,B_READ);emmc_strategy(&b);check_done(&b,0,0,1);
    b=req(0,131072,0,B_READ);emmc_strategy(&b);check_done(&b,0,0,0);
    b=req(0,131072,1,B_READ);emmc_strategy(&b);check_done(&b,EINVAL,1,0);
    b=req(0,131071,513,B_READ);emmc_strategy(&b);check_done(&b,EINVAL,513,0);
    b=req(0,-1,512,B_READ);emmc_strategy(&b);check_done(&b,EINVAL,512,0);
    b=req(0,INT64_MAX,512,B_READ);emmc_strategy(&b);check_done(&b,EINVAL,512,0);
    b=req(0,INT64_C(1)<<55,512,B_READ);emmc_strategy(&b);check_done(&b,EINVAL,512,0);
    b=req(2,0,512,B_READ);emmc_strategy(&b);check_done(&b,ENXIO,512,0);
    b=req(0,0,512,0);emmc_strategy(&b);check_done(&b,EROFS,512,0);
    b=req(0,0,512,B_READ|B_PHYS);emmc_strategy(&b);check_done(&b,EINVAL,512,0);
    b=req(0,0,512,B_READ);map_fail=1;emmc_strategy(&b);check_done(&b,EIO,512,0);
    b=req(0,0,1024,B_READ);fail_call=2;emmc_strategy(&b);check_done(&b,EIO,512,2);
    assert((unsigned char)b.data[512]==0xa5);
    b=req(0,0,1024,B_READ);fail_call=1;emmc_strategy(&b);check_done(&b,EIO,1024,1);
    struct uio u={.offset=511,.resid=514};
    read_calls=0;fail_call=0;
    assert(emmc_read(0,&u,0)==0&&u.resid==0&&u.copied==514&&read_calls==3);
    for(unsigned i=0;i<514;i++)assert((unsigned char)u.data[i]==
        (unsigned char)(ae.gpt.boot+(511+i)/512+(511+i)%512));
    u=(struct uio){.offset=(int64_t)ae.gpt.boot_count*512-1,.resid=2};
    read_calls=0;assert(emmc_read(0,&u,0)==0&&u.copied==1&&u.resid==1&&read_calls==1);
    read_calls=0;assert(emmc_read(0,&u,0)==0&&read_calls==0);
    u=(struct uio){.offset=-1,.resid=512};assert(emmc_read(0,&u,0)==EINVAL);
    u=(struct uio){.offset=INT64_MAX,.resid=512};assert(emmc_read(0,&u,0)==EINVAL);
    u=(struct uio){.offset=0,.resid=-1};assert(emmc_read(0,&u,0)==EINVAL);
    u=(struct uio){.resid=512,.fail=1};read_calls=0;
    assert(emmc_read(0,&u,0)==14&&u.resid==512&&read_calls==1&&lock_depth==0);
    u=(struct uio){.resid=1024};read_calls=0;fail_call=2;
    assert(emmc_read(1,&u,0)==EIO&&u.resid==512&&u.copied==512);
    ae.writable=true;copying_in=true;fail_call=0;read_calls=0;
    assert(emmc_open(0,FWRITE,0,NULL)==EROFS);
    assert(emmc_open(1,FWRITE,0,NULL)==0);
    assert(emmc_ioctl(1,DKIOCISWRITABLE,(caddr_t)&geometry,0,NULL)==0&&geometry==1);
    assert(emmc_ioctl(0,DKIOCISWRITABLE,(caddr_t)&geometry,0,NULL)==0&&geometry==0);
    u=(struct uio){.offset=512,.resid=512};memset(u.data,0x39,512);
    assert(emmc_write(1,&u,0)==0&&u.resid==0&&write_calls==1);
    assert(write_lba==ae.gpt.userdata+1&&written[511]==0x39);
    u=(struct uio){.resid=512,.fail=1};
    assert(emmc_write(1,&u,0)==14&&u.resid==512&&write_calls==1);
    u=(struct uio){.resid=512};write_fail=2;
    assert(emmc_write(1,&u,0)==EIO&&u.resid==512&&u.offset==0);
    assert(emmc_write(0,&u,0)==EROFS);
    u=(struct uio){.offset=1,.resid=512};assert(emmc_write(1,&u,0)==EINVAL);
    u=(struct uio){.offset=(int64_t)ae.gpt.userdata_count*512,.resid=512};
    assert(emmc_write(1,&u,0)==EINVAL);
    b=req(1,0,513,0);memset(b.data,0x57,513);write_fail=0;write_calls=0;
    emmc_strategy(&b);check_done(&b,0,0,1);assert(write_calls==2);
    assert(written[0]==0x57&&written[1]==(unsigned char)(ae.gpt.userdata+2));
    b=req(0,0,512,0);emmc_strategy(&b);check_done(&b,EROFS,512,0);
    assert(emmc_ioctl(1,DKIOCSYNCHRONIZECACHE,NULL,0,NULL)==0);
    ae.writable=false;copying_in=false;write_calls=0;
    ae.poisoned=true;assert(emmc_read(0,&u,0)==ENXIO);
    assert(emmc_open(0,0,0,NULL)==ENXIO);
    b=req(0,0,512,B_READ);emmc_strategy(&b);check_done(&b,ENXIO,512,0);
    ae.poisoned=false;ae.ready=false;
    b=req(0,0,512,B_READ);emmc_strategy(&b);check_done(&b,ENXIO,512,0);
    puts("PASS: actual BSD handlers; BOOT/USERDATA translation, bounds, overflow,");
    puts("writes rejected without reads, partial errors, map failure, lock/completion balance");
    puts("raw uiomove: unaligned/multisector, EOF, invalid offsets, copy fault and partial I/O");
    puts("specfs geometry: 512-byte sectors, separate partition capacities, full16KiB buffered read");
}
'''
    with tempfile.TemporaryDirectory(prefix='a03-bsd-') as directory:
        path = Path(directory)
        (path/'test.c').write_text(stub+handlers+tests)
        subprocess.run(['clang','-std=c11','-O1','-g','-Wall','-Wextra',
                        '-Werror','-fsanitize=address,undefined',str(path/'test.c'),
                        '-o',str(path/'test')],check=True)
        subprocess.run([str(path/'test')],check=True)


if __name__ == '__main__':
    main()
