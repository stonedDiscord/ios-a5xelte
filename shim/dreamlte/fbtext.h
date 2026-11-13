/* Early S8 loader runs headless: firmware scanout is not yet verified. */
#pragma once
#include <stdint.h>
static inline uint32_t hero_fb_enable(void) { return 0; }
static inline void hero_fb_text(unsigned row, const char *s) { (void)row; (void)s; }
static inline void hero_fb_hex(unsigned row, const char *s, uint64_t value) {
    (void)row; (void)s; (void)value;
}
