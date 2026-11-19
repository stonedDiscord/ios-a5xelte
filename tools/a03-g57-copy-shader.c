/* Host-only NIR generator for measured G57 product9091, Mesa24.3.0.
 * Produces one u32 copy per global invocation, fixed private testGPUVAs.
 * Not a kernel/phone executable. Build/link with pinned Mesa compiler and
 * util/NIR libraries; output requires independent hardware verification. */
#include <stdio.h>
#include "compiler/nir/nir_builder.h"
#include "panfrost/compiler/bifrost_compile.h"
#include "panfrost/compiler/valhall/disassemble.h"
#include "util/u_dynarray.h"
int main(int argc,char **argv){
 if(argc!=2)return 2;
 glsl_type_singleton_init_or_ref();
 nir_builder b=nir_builder_init_simple_shader(MESA_SHADER_COMPUTE,&bifrost_nir_options_v9,"a03_g57_copy_u32");
 b.shader->info.workgroup_size[0]=1;b.shader->info.workgroup_size[1]=1;b.shader->info.workgroup_size[2]=1;
 nir_def *id=nir_channel(&b,nir_load_global_invocation_id(&b,32),0);
 nir_def *offset=nir_u2u64(&b,nir_ishl_imm(&b,id,2));
 nir_def *src=nir_iadd(&b,nir_imm_int64(&b,0x02002000ULL),offset);
 nir_def *dst=nir_iadd(&b,nir_imm_int64(&b,0x02003000ULL),offset);
 nir_def *value=nir_load_global(&b,src,4,1,32);
 nir_store_global(&b,dst,4,value,1);
 struct panfrost_compile_inputs in={.gpu_id=0x9091,.no_ubo_to_push=true};
 struct pan_shader_info info={0};struct util_dynarray binary;util_dynarray_init(&binary,NULL);
 bifrost_preprocess_nir(b.shader,in.gpu_id);
 bifrost_compile_shader_nir(b.shader,&in,&binary,&info);
 fprintf(stderr,"bytes=%u regs=%u tls=%u wls=%u preload=%llx push=%u\n",binary.size,info.work_reg_count,info.tls_size,info.wls_size,(unsigned long long)info.preload,info.push.count);
 FILE *f=fopen(argv[1],"wb");if(!f)return 3;fwrite(binary.data,1,binary.size,f);fclose(f);
 disassemble_valhall(stdout,(const uint64_t*)binary.data,binary.size,true);
 util_dynarray_fini(&binary);ralloc_free(b.shader);glsl_type_singleton_decref();return 0;
}
