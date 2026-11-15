/* BOOT-only independent reader using matching stock Linux.
 * Never mounts USERDATA. USB is read-only; after GPT validation, writes
 * only the 4 KiB diagnostic mailbox at USERDATA offset16GiB. */
#define _GNU_SOURCE
#include <sys/mount.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <linux/reboot.h>
#include <linux/fb.h>
#include "../shim/font.h"
#include "../shim/a03/gpt-readonly.h"
#include <sys/stat.h>
#include <sys/sysmacros.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <stdarg.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "a03-linux-reader-drm.h"
static char report[16384];
static size_t used;
static void screen(void) {
    static uint32_t *pixels;
    static struct fb_fix_screeninfo fix;
    static struct fb_var_screeninfo var;
    if(!pixels){
        FILE *f=fopen("/sys/class/graphics/fb0/dev","r");
        unsigned maj=0,min=0;
        if(!f){
            if(!drm_pixels)drm_screen_init();
            if(!drm_pixels)return;
            pixels=drm_pixels;fix.line_length=drm_stride*4;
            var.xres=drm_width;var.yres=drm_height;
            goto draw;
        }
        int n=fscanf(f,"%u:%u",&maj,&min);fclose(f);if(n!=2)return;
        mknod("/dev/fb0",S_IFCHR|0600,makedev(maj,min));
        int fd=open("/dev/fb0",O_RDWR|O_CLOEXEC);if(fd<0)return;
        if(ioctl(fd,FBIOGET_FSCREENINFO,&fix)||ioctl(fd,FBIOGET_VSCREENINFO,&var)||
           var.bits_per_pixel!=32||fix.line_length<var.xres*4||
           (uint64_t)(var.yoffset+var.yres)*fix.line_length>fix.smem_len){close(fd);return;}
        void *map=mmap(NULL,fix.smem_len,PROT_READ|PROT_WRITE,MAP_SHARED,fd,0);
        close(fd);if(map==MAP_FAILED)return;pixels=map;
    }
draw:;
    unsigned cols=var.xres/8,rows=var.yres/16,row=0,col=0;
    if(!cols||!rows)return;
    for(size_t i=0;i<used&&row<rows;i++){
        unsigned c=(unsigned char)report[i];
        if(c==10){row++;col=0;continue;}
        if(c<32||c>126)c='?';
        for(unsigned y=0;y<16;y++)for(unsigned x=0;x<8;x++){
            size_t offset=(size_t)(var.yoffset+row*16+y)*(fix.line_length/4)+var.xoffset+col*8+x;
            pixels[offset]=(font8x16[c-32][y]&(0x80u>>x))?0xffffffff:0xff000000;
        }
        if(++col==cols){col=0;row++;}
    }
}
static void logmsg(const char *fmt, ...) {
    va_list ap; va_start(ap, fmt);
    size_t start=used;
    int n=vsnprintf(report+used,sizeof(report)-used,fmt,ap); va_end(ap);
    if(n>0)used+=(size_t)n<sizeof(report)-used?(size_t)n:sizeof(report)-used-1;
    int fd=open("/dev/kmsg",O_WRONLY|O_CLOEXEC);
    if(fd>=0){dprintf(fd,"A03 reader: %s",report+start);close(fd);}
    screen();
}
static int put(const char *p,const char *v) {
    int fd=open(p,O_WRONLY|O_CLOEXEC);
    if(fd<0){logmsg("open %s: %s\n",p,strerror(errno));return -1;}
    ssize_t n=write(fd,v,strlen(v));int e=errno;close(fd);
    if(n!=(ssize_t)strlen(v)){logmsg("write %s: %s\n",p,strerror(e));return -1;}
    return 0;
}
static int get(const char *p,char *out,size_t size) {
    int fd=open(p,O_RDONLY|O_CLOEXEC);if(fd<0)return -1;
    ssize_t n=read(fd,out,size-1);close(fd);if(n<0)return -1;out[n]=0;return 0;
}
static int dir(const char *p) {
    if(!mkdir(p,0755)||errno==EEXIST)return 0;
    logmsg("mkdir %s: %s\n",p,strerror(errno));return -1;
}
static unsigned disk_sector(void *context,uint32_t lba,unsigned char *out) {
    int fd=*(int *)context;
    return pread(fd,out,512,(off_t)lba*512)==512;
}
static void sample(int fd,uint64_t off,const char *name) {
    unsigned char b[512];ssize_t n=pread(fd,b,sizeof(b),(off_t)off);
    logmsg("%s offset=0x%llx read=%ld first32=",name,(unsigned long long)off,(long)n);
    if(n==sizeof(b))for(unsigned i=0;i<32;i++)logmsg("%02x",b[i]);
    logmsg("\n");
}
int main(void) {
    mount("tmpfs","/dev","tmpfs",MS_NOSUID,"mode=0755");
    mknod("/dev/null",S_IFCHR|0666,makedev(1,3));
    mknod("/dev/kmsg",S_IFCHR|0600,makedev(1,11));
    mount("proc","/proc","proc",MS_NOSUID|MS_NODEV|MS_NOEXEC,NULL);
    mount("sysfs","/sys","sysfs",MS_NOSUID|MS_NODEV|MS_NOEXEC,NULL);
    mount("tmpfs","/run","tmpfs",MS_NOSUID|MS_NODEV,"mode=0700");
    logmsg("A03_LINUX_READER_V7 PID=%ld; USERDATA read-only; no Android init\n",(long)getpid());
    char buf[256];
    int validated=0;
    uint64_t part_sectors=0;
    for(unsigned t=0;t<15;t++){
        if(!get("/sys/class/block/mmcblk0p55/dev",buf,sizeof(buf)))break;
        sleep(1);
    }
    unsigned maj=0,min=0;
    if(get("/sys/class/block/mmcblk0p55/dev",buf,sizeof(buf))||
       sscanf(buf,"%u:%u",&maj,&min)!=2||!maj){
        logmsg("REFUSE: missing/unexpected mmcblk0p55 identity\n");goto usb_setup;
    }
    mknod("/dev/mmcblk0p55",S_IFBLK|0400,makedev(maj,min));
    if(get("/sys/class/block/mmcblk0p55/start",buf,sizeof(buf))||strtoull(buf,NULL,10)!=15929344ULL){
        logmsg("REFUSE: USERDATA start differs from validated A03 GPT\n");goto usb_setup;
    }
    if(get("/sys/class/block/mmcblk0p55/size",buf,sizeof(buf))){
        logmsg("REFUSE: USERDATA size unavailable\n");goto usb_setup;
    }
    part_sectors=strtoull(buf,NULL,10);
    if(get("/sys/class/block/mmcblk0/dev",buf,sizeof(buf))||
       sscanf(buf,"%u:%u",&maj,&min)!=2||!maj){
        logmsg("REFUSE: missing parent mmcblk0 identity\n");goto usb_setup;
    }
    if(get("/sys/class/block/mmcblk0/size",buf,sizeof(buf))){
        logmsg("REFUSE: parent capacity unavailable\n");goto usb_setup;
    }
    uint64_t sectors=strtoull(buf,NULL,10);
    mknod("/dev/mmcblk0",S_IFBLK|0400,makedev(maj,min));
    int disk=open("/dev/mmcblk0",O_RDONLY|O_CLOEXEC);unsigned char h[512];
    struct a03_gpt g;uint32_t crc=0;
    if(disk<0||sectors>UINT32_MAX||!disk_sector(&disk,1,h)||
       !a03_gpt_header(h,(uint32_t)sectors,&g)||
       a03_gpt_entries(&g,disk_sector,&disk,&crc)||g.userdata_count!=part_sectors){
        logmsg("REFUSE: GPT CRC/identity/geometry mismatch\n");
        if(disk>=0)close(disk);
        goto usb_setup;
    }
    close(disk);
    logmsg("GPT validated CRC=%08x USERDATA start=%u sectors=%u\n",crc,g.userdata,g.userdata_count);
    int data=open("/dev/mmcblk0p55",O_RDONLY|O_CLOEXEC);
    if(data<0){logmsg("USERDATA open: %s\n",strerror(errno));goto usb_setup;}
    sample(data,1024,"HFSX_HEADER");sample(data,0x2cd82000ULL,"CATALOG_HEADER");
    sample(data,0x2cfa6000ULL,"CATALOG_ROOT_NODE_274");close(data);
    validated=1;
usb_setup:
    if(mount("configfs","/config","configfs",MS_NOSUID|MS_NODEV|MS_NOEXEC,NULL)){
        logmsg("configfs mount: %s\n",strerror(errno));goto idle;
    }
    if(dir("/config/usb_gadget/a03"))goto idle;
    if(put("/config/usb_gadget/a03/idVendor","0x1d6b")||put("/config/usb_gadget/a03/idProduct","0x0104"))goto idle;
    if(dir("/config/usb_gadget/a03/strings/0x409"))goto idle;
    if(put("/config/usb_gadget/a03/strings/0x409/manufacturer","A03 bringup")||
       put("/config/usb_gadget/a03/strings/0x409/product","A03 USERDATA READ ONLY")||
       put("/config/usb_gadget/a03/strings/0x409/serialnumber","A03LinuxReaderV7"))goto idle;
    if(dir("/config/usb_gadget/a03/configs/c.1")||dir("/config/usb_gadget/a03/functions/mass_storage.0"))goto idle;
    int rf=open("/run/report.bin",O_CREAT|O_RDWR|O_CLOEXEC,0600);
    if(rf<0)goto idle;
    if(ftruncate(rf,1048576)||pwrite(rf,report,used,0)!=(ssize_t)used){close(rf);goto idle;}
    close(rf);
    if(put("/config/usb_gadget/a03/functions/mass_storage.0/lun.0/ro","1")||
       put("/config/usb_gadget/a03/functions/mass_storage.0/lun.0/file","/run/report.bin"))goto idle;
    if(validated){
        if(dir("/config/usb_gadget/a03/functions/mass_storage.0/lun.1")||
           put("/config/usb_gadget/a03/functions/mass_storage.0/lun.1/ro","1")||
           put("/config/usb_gadget/a03/functions/mass_storage.0/lun.1/removable","1")||
           put("/config/usb_gadget/a03/functions/mass_storage.0/lun.1/file","/dev/mmcblk0p55"))goto idle;
    }
    if(symlink("../../functions/mass_storage.0","/config/usb_gadget/a03/configs/c.1/mass_storage.0")){
        logmsg("link mass storage: %s\n",strerror(errno));goto idle;
    }
    for(unsigned t=0;t<15;t++){
        DIR *d=opendir("/sys/class/udc");struct dirent *de;
        if(d){
            while((de=readdir(d)))if(de->d_name[0]!='.'){
                logmsg("binding UDC %s\n",de->d_name);
                if(!put("/config/usb_gadget/a03/UDC",de->d_name)){closedir(d);goto idle;}
            }
            closedir(d);
        }
        sleep(1);
    }
    logmsg("No UDC bound\n");
idle:
    /* Explicit A03 USERDATA diagnostic mailbox at16GiB, beyond HFS root.
     * GPT identity/CRC and sysfs bounds were validated before this gate. */
    if(validated&&part_sectors>=33554432ULL+8){
        unsigned char mailbox[4096]={0};
        memcpy(mailbox,"A03LOG07",8);
        uint32_t length=used<sizeof(mailbox)-16?used:sizeof(mailbox)-16;
        memcpy(mailbox+8,&length,4);memcpy(mailbox+16,report,length);
        uint32_t crc=~a03_crc_update(~0u,mailbox+16,length);memcpy(mailbox+12,&crc,4);
        int out=open("/dev/mmcblk0p55",O_WRONLY|O_CLOEXEC|O_SYNC);
        if(out>=0){
            if(pwrite(out,mailbox,sizeof(mailbox),16ULL<<30)!=(ssize_t)sizeof(mailbox)||fsync(out))
                logmsg("MAILBOX WRITE FAILED\n");
            close(out);
        }
    }
    /* Return to Download after observation, proving init execution even if
     * gadget/display setup failed. Linux restart handler only; no block writes. */
    logmsg("Returning to Download in 45 seconds\n");
    for(unsigned t=0;t<45;t++){screen();sleep(1);}
    syscall(SYS_reboot,LINUX_REBOOT_MAGIC1,LINUX_REBOOT_MAGIC2,
            LINUX_REBOOT_CMD_RESTART2,"download");
    for(;;)pause();
}
