/* Android/Linux EL0 diagnostic. No storage or MMIO access.
 * Linux may emulate ID registers: these are not raw boot CPU readings.
 */
typedef unsigned long u64;
static long write_stdout(const char *text, u64 length)
{
    register long x0 __asm__("x0") = 1;
    register const char *x1 __asm__("x1") = text;
    register u64 x2 __asm__("x2") = length;
    register long x8 __asm__("x8") = 64;
    __asm__ volatile("svc #0" : "+r"(x0) : "r"(x1), "r"(x2), "r"(x8) : "memory", "cc");
    return x0;
}
static int print(const char *text)
{
    u64 length = 0;
    while (text[length]) ++length;
    while (length) {
        long written = write_stdout(text, length);
        if (written == -4) continue; /* EINTR */
        if (written <= 0) return 1;
        text += written;
        length -= (u64)written;
    }
    return 0;
}
static int print_register(const char *name, u64 value)
{
    static const char digits[] = "0123456789abcdef";
    char hex[20] = "0x0000000000000000\n";
    for (unsigned i = 0; i < 16; ++i)
        hex[2 + i] = digits[(value >> (60 - 4 * i)) & 15];
    return print(name) || print(hex);
}
int a03_probe_main(void)
{
    u64 value;
    if (print("A03 EL0 diagnostic v1 (Android userspace, not XNU or a boot probe)\n")) return 1;
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(value));
    if (print_register("CNTFRQ_EL0=", value)) return 1;
    __asm__ volatile("mrs %0, cntvct_el0" : "=r"(value));
    if (print_register("CNTVCT_EL0=", value)) return 1;
    __asm__ volatile("mrs %0, midr_el1" : "=r"(value));
    if (print_register("MIDR_EL1_LINUX_VIEW=", value)) return 1;
    __asm__ volatile("mrs %0, id_aa64mmfr0_el1" : "=r"(value));
    if (print_register("ID_AA64MMFR0_EL1_LINUX_VIEW=", value)) return 1;
    return print("A03_EL0_PROBE_OK\n");
}
