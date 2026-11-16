/* A03 live RAM ends at 0x17ffff000; reservations end at 0x100001000.
 * Keep the existing aligned base and two explicitly supported profiles. */
#ifndef A03_MEMORY_PROFILE_H
#define A03_MEMORY_PROFILE_H
#include <stdint.h>
static inline int a03_memory_profile_valid(uint64_t base, uint64_t size)
{
    return base == UINT64_C(0x102000000) &&
        (size == UINT64_C(0x10000000) || size == UINT64_C(0x40000000));
}
#endif
