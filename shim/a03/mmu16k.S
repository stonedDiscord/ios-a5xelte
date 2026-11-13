/* Temporary EL2->EL1->EL2 round trip. No MMIO, interrupts stay masked.
 * EL1 HVC and synchronous faults return through our temporary EL2 vector.
 */
.section .text,"ax"
.global a03_test_el1
.type a03_test_el1,%function
a03_test_el1:
    stp x29, x30, [sp, #-96]!
    stp x19, x20, [sp, #16]
    stp x21, x22, [sp, #32]
    stp x23, x24, [sp, #48]
    stp x25, x26, [sp, #64]
    stp x27, x28, [sp, #80]
    adr x26, a03_saved_regs
    mrs x0, CurrentEL
    cmp x0, #8
    b.ne a03_test_skip
    mrs x0, sctlr_el2
    tbnz x0, #0, a03_test_skip
    mrs x0, hcr_el2
    str x0, [x26, #0]
    mrs x0, cnthctl_el2
    str x0, [x26, #8]
    mrs x0, cntvoff_el2
    str x0, [x26, #16]
    mrs x0, vbar_el2
    str x0, [x26, #24]
    mrs x0, cptr_el2
    str x0, [x26, #32]
    mrs x0, spsr_el2
    str x0, [x26, #40]
    mrs x0, elr_el2
    str x0, [x26, #48]
    mrs x0, sp_el1
    str x0, [x26, #56]
    mrs x0, sctlr_el1
    str x0, [x26, #64]
    mrs x0, tcr_el1
    str x0, [x26, #72]
    mrs x0, ttbr0_el1
    str x0, [x26, #80]
    mrs x0, ttbr1_el1
    str x0, [x26, #88]
    mrs x0, mair_el1
    str x0, [x26, #96]
    mrs x0, vbar_el1
    str x0, [x26, #104]
    mrs x0, par_el1
    str x0, [x26, #112]
    mov x0, sp
    str x0, [x26, #120]
    adr x0, a03_el2_vectors
    msr vbar_el2, x0
    mov x0, #0x80000000 /* HCR.RW, VM and trap controls off */
    msr hcr_el2, x0
    mov x0, #3
    msr cnthctl_el2, x0
    msr cntvoff_el2, xzr
    mov x0, #0x33ff
    msr cptr_el2, x0
    mov x0, #0x0800
    movk x0, #0x30d0, lsl #16 /* SCTLR_EL1 RES1, MMU/cache off */
    msr sctlr_el1, x0
    adr x0, a03_el1_vectors
    msr vbar_el1, x0
    adr x0, a03_el1_stack_end
    msr sp_el1, x0
    mov x0, #0x3c5 /* masked EL1h */
    msr spsr_el2, x0
    adr x0, a03_el1_entry
    msr elr_el2, x0
    dsb sy
    isb
    eret
a03_el1_entry:
    bl a03_mmu16k_test
    hvc #0xa03
    b .
/* All unexpected vectors also terminate the test, preserving fault info. */
.balign 2048
a03_el2_vectors:
.rept 16
    b a03_el2_return
    .space 124
.endr
.balign 2048
a03_el1_vectors:
.rept 16
    b a03_el1_fault
    .space 124
.endr
a03_el1_fault:
    mrs x0, esr_el1
    mrs x1, far_el1
    adr x2, a03_mmu_result
    str x0, [x2, #64]
    str x1, [x2, #72]
    mov x0, #0xee
    str x0, [x2]
    mrs x0, sctlr_el1
    bic x0, x0, #1
    msr sctlr_el1, x0
    isb
    hvc #0xa04
    b .
a03_el2_return:
    adr x26, a03_saved_regs
    /* Restore SP even if the fault came from the EL2 current-SP0 slot. */
    msr spsel, #1
    ldr x0, [x26, #120]
    mov sp, x0
    adr x2, a03_mmu_result
    mrs x0, esr_el2
    str x0, [x2, #80]
    mrs x0, elr_el2
    str x0, [x2, #88]
    mrs x0, sctlr_el1
    bic x0, x0, #1
    msr sctlr_el1, x0
    dsb sy
    isb
    tlbi alle1
    dsb sy
    isb
    ldr x0, [x26, #72]
    msr tcr_el1, x0
    ldr x0, [x26, #80]
    msr ttbr0_el1, x0
    ldr x0, [x26, #88]
    msr ttbr1_el1, x0
    ldr x0, [x26, #96]
    msr mair_el1, x0
    ldr x0, [x26, #104]
    msr vbar_el1, x0
    ldr x0, [x26, #112]
    msr par_el1, x0
    ldr x0, [x26, #64]
    msr sctlr_el1, x0
    ldr x0, [x26, #56]
    msr sp_el1, x0
    ldr x0, [x26, #8]
    msr cnthctl_el2, x0
    ldr x0, [x26, #16]
    msr cntvoff_el2, x0
    ldr x0, [x26, #32]
    msr cptr_el2, x0
    ldr x0, [x26, #40]
    msr spsr_el2, x0
    ldr x0, [x26, #48]
    msr elr_el2, x0
    ldr x0, [x26, #24]
    msr vbar_el2, x0
    ldr x0, [x26, #0]
    msr hcr_el2, x0
    isb
a03_test_skip:
    ldp x19, x20, [sp, #16]
    ldp x21, x22, [sp, #32]
    ldp x23, x24, [sp, #48]
    ldp x25, x26, [sp, #64]
    ldp x27, x28, [sp, #80]
    ldp x29, x30, [sp], #96
    ret
.balign 16
a03_saved_regs:
.space 128
.space 8192
a03_el1_stack_end:
/* File-backed storage: included in the append, no BSS initialization needed. */
.balign 16384
.global a03_l2
a03_l2: .space 16384
.global a03_l3
a03_l3: .space 16384
.global a03_test_word
a03_test_word: .quad 0
.global a03_mmu_result
a03_mmu_result: .space 96
