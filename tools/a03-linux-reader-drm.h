/* Kernel DRM/KMS display, queried objects and allocated dumb buffer only. */
#include <drm.h>
static uint32_t *drm_pixels;
static unsigned drm_width,drm_height,drm_stride;
static int drm_fd=-1;
static void drm_screen_init(void) {
    FILE *f=fopen("/sys/class/drm/card0/dev","r");unsigned maj=0,min=0;
    if(!f)return;
    int n=fscanf(f,"%u:%u",&maj,&min);fclose(f);if(n!=2)return;
    mknod("/dev/dri-card0",S_IFCHR|0600,makedev(maj,min));
    int fd=open("/dev/dri-card0",O_RDWR|O_CLOEXEC);if(fd<0)return;
    struct drm_mode_card_res res={0};
    uint32_t connectors[32],crtcs[32];
    if(ioctl(fd,DRM_IOCTL_MODE_GETRESOURCES,&res)||!res.count_connectors||!res.count_crtcs||
       res.count_connectors>32||res.count_crtcs>32)goto fail;
    res.connector_id_ptr=(uintptr_t)connectors;res.crtc_id_ptr=(uintptr_t)crtcs;
    if(ioctl(fd,DRM_IOCTL_MODE_GETRESOURCES,&res))goto fail;
    for(unsigned i=0;i<res.count_connectors;i++){
        struct drm_mode_get_connector conn={.connector_id=connectors[i]};
        struct drm_mode_modeinfo modes[32];uint32_t encoders[32];
        if(ioctl(fd,DRM_IOCTL_MODE_GETCONNECTOR,&conn)||!conn.count_modes||
           conn.count_modes>32||conn.count_encoders>32)continue;
        conn.modes_ptr=(uintptr_t)modes;conn.encoders_ptr=(uintptr_t)encoders;
        if(ioctl(fd,DRM_IOCTL_MODE_GETCONNECTOR,&conn)||conn.connection!=1)continue;
        unsigned mode=0;
        for(unsigned j=0;j<conn.count_modes;j++)if(modes[j].type&DRM_MODE_TYPE_PREFERRED){mode=j;break;}
        uint32_t crtc=0;
        for(unsigned j=0;j<conn.count_encoders&&!crtc;j++){
            struct drm_mode_get_encoder enc={.encoder_id=encoders[j]};
            if(ioctl(fd,DRM_IOCTL_MODE_GETENCODER,&enc))continue;
            for(unsigned k=0;k<res.count_crtcs;k++)if(enc.possible_crtcs&(1u<<k)){crtc=crtcs[k];break;}
        }
        if(!crtc)continue;
        struct drm_mode_create_dumb dumb={.width=modes[mode].hdisplay,.height=modes[mode].vdisplay,.bpp=32};
        if(!dumb.width||!dumb.height||dumb.width>4096||dumb.height>4096||
           ioctl(fd,DRM_IOCTL_MODE_CREATE_DUMB,&dumb))continue;
        struct drm_mode_fb_cmd fb={.width=dumb.width,.height=dumb.height,.pitch=dumb.pitch,
            .bpp=32,.depth=24,.handle=dumb.handle};
        if(ioctl(fd,DRM_IOCTL_MODE_ADDFB,&fb))continue;
        struct drm_mode_map_dumb map={.handle=dumb.handle};
        if(ioctl(fd,DRM_IOCTL_MODE_MAP_DUMB,&map))continue;
        void *p=mmap(NULL,dumb.size,PROT_READ|PROT_WRITE,MAP_SHARED,fd,(off_t)map.offset);
        if(p==MAP_FAILED)continue;
        struct drm_mode_crtc set={.set_connectors_ptr=(uintptr_t)&connectors[i],.count_connectors=1,
            .crtc_id=crtc,.fb_id=fb.fb_id,.mode_valid=1,.mode=modes[mode]};
        if(ioctl(fd,DRM_IOCTL_MODE_SETCRTC,&set)){munmap(p,dumb.size);continue;}
        drm_pixels=p;drm_width=dumb.width;drm_height=dumb.height;drm_stride=dumb.pitch/4;
        drm_fd=fd;return;
    }
fail:
    close(fd);
}
