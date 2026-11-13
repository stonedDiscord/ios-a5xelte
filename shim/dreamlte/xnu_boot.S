/* SPDX-License-Identifier: GPL-2.0-only
 * dreamlte (SM-G950F) S-Boot Image wrapper that hands off to 4 KiB XNU.
 * Adapted from shim/a5xelte/xnu_boot.S. No storage accesses. Errors are
 * recorded in RAM; failure halts without touching PMU or storage.
 */
.section .text.head, "ax"
.global _start
_start:
    b entry
    .long 0
    .quad 0x80000            /* text_offset: replaced by the packer */
    .quad 0                  /* image_size: replaced by the packer */
    .quad 0                  /* flags: replaced by the packer */
    .quad 0, 0, 0
    .byte 0x41, 0x52, 0x4d, 0x64
    .long 0

entry:
    msr daifset, #15
    mov x19, x0              /* FDT from S-Boot */
    mrs x20, CurrentEL
    mrs x21, sctlr_el1
    /* Log page 0x8afff000, below the XNU RAM window; XNU marks +0x100. */
    ldr x13, =0x8afff000
    mov x14, x13
    add x15, x13, #4096
inval_log:
    dc ivac, x14
    add x14, x14, #64
    cmp x14, x15
    b.lo inval_log
    dsb sy
    mov x14, x13
zero_log:
    stp xzr, xzr, [x14], #16
    cmp x14, x15
    b.lo zero_log
    ldr x14, =0x31304d4145524458 /* "HXNERO01" */
    str x14, [x13]
    str x20, [x13, #8]
    str x21, [x13, #16]
    str x19, [x13, #24]
    adr x14, _start
    str x14, [x13, #32]
    adr x14, hero_boot_stack_top
    mov sp, x14
    mov x0, x19
    mov x1, x13
    mov x2, x20
    mov x3, x21
    bl hero_prepare_xnu
    ldr x13, =0x8afff000
    cbz x0, fail
    mov x16, x0
    ldr x0, [x13, #136]       /* boot_args physical address (log[17]) */
    /* C cleaned the copied ranges and the log. XNU's entry needs MMU off. */
    mrs x14, sctlr_el1
    bic x14, x14, #1
    bic x14, x14, #4
    bic x14, x14, #0x1000
    msr sctlr_el1, x14
    isb
    br x16
fail:
    /* Halt on failure: S8 PMU recovery handoff is not device-verified. */
halt:
    wfe
    b halt
    .ltorg

.section .data, "aw"
.balign 16
hero_boot_stack:
    .space 8192
hero_boot_stack_top:
