/* Decode the stock JD9365T ERAM section layout without bus/MMIO access.
 * Snapshot starts at 0x20011000. Source: Samsung ChipInfoInit/ReadSectionInfo.
 * A valid table is not evidence of fresh contacts or authorization to read
 * arbitrary entries; caller must validate controller RAM ranges separately.
 */
#ifndef A03_JD9365T_SECTIONS_H
#define A03_JD9365T_SECTIONS_H
#include <stddef.h>
#include <stdint.h>

#define A03_JD_SECTIONS_SIZE 160u /* through ESRAM coordinate entry2 */
struct a03_jd_section { uint32_t address, length; };
struct a03_jd_sections {
 struct a03_jd_section firmware_config, coordinate_report;
};
static inline uint32_t a03_jd_le32(const uint8_t *p)
{
 return (uint32_t)p[0]|((uint32_t)p[1]<<8)|((uint32_t)p[2]<<16)|((uint32_t)p[3]<<24);
}
static inline int a03_jd_section_entry(const uint8_t *p,
    struct a03_jd_section *out, uint32_t minimum)
{
 uint32_t a=a03_jd_le32(p),n=a03_jd_le32(p+4);
 if(!a || n<minimum || n-1>UINT32_MAX-a)return -1;
 out->address=a;out->length=n;return 0;
}
/* Counts are not interpreted: stock reads fixed entries and does not define
 * their byte widths in this path. Require ready marker and complete buffers.
 * Coordinate length must match the separately validated 60-byte decoder.
 */
static inline int a03_jd_decode_sections(const uint8_t *p,size_t n,
    struct a03_jd_sections *out)
{
 struct a03_jd_sections next;
 if(!p||!out||n<A03_JD_SECTIONS_SIZE||p[0]!=0x5a||p[1]!=0xa5)return -1;
 if(a03_jd_section_entry(p+4+3*8,&next.firmware_config,6) ||
    a03_jd_section_entry(p+136+2*8,&next.coordinate_report,60) ||
    next.coordinate_report.length!=60)return -1;
 *out=next;return 0;
}
#endif
