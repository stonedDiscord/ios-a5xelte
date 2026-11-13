/* A03 XNU wrapper: boot at EL2, initialize EL1, no storage writes. */
.section .text.head,"ax"
.global _start
_start:
    b entry
    .long 0
    .quad 0x80000
    .quad 0
    .quad 0xa
    .quad 0,0,0
    .ascii "ARMd"
    .long 0
entry:
    msr daifset,#15
    mov x19,x0
    mrs x0,CurrentEL
    cmp x0,#8
    b.eq from_el2
    cmp x0,#4
    b.ne halt
    b el1
from_el2:
    msr spsel,#1
    adr x0,vectors
    msr vbar_el2,x0
    mov x0,#0x80000000
    msr hcr_el2,x0
    mov x0,#3
    msr cnthctl_el2,x0
    msr cntvoff_el2,xzr
    mov x0,#0x33ff
    msr cptr_el2,x0
    msr hstr_el2,xzr
    msr vttbr_el2,xzr
    mrs x0,midr_el1
    msr vpidr_el2,x0
    mrs x0,mpidr_el1
    msr vmpidr_el2,x0
    mrs x0,icc_sre_el2
    orr x0,x0,#1
    orr x0,x0,#8
    msr icc_sre_el2,x0
    isb
    msr ich_hcr_el2,xzr
    mov x0,#0x0800
    movk x0,#0x30d0,lsl #16
    msr sctlr_el1,x0
    mov x0,#0x3c5
    msr spsr_el2,x0
    adr x0,el1
    msr elr_el2,x0
    isb
    eret
el1:
    msr spsel,#1
    adr x0,vectors
    msr vbar_el1,x0
    adr x0,stack_top
    mov sp,x0
    mov x0,x19
    bl a03_load_xnu
    cbz x0,halt
    mov x16,x0
    mov x0,x1
    dsb sy
    ic iallu
    dsb sy
    isb
    br x16
halt:
    wfe
    b halt
.balign 2048
vectors:
.rept 16
    b halt
    .space 124
.endr
.section .data,"aw"
.balign 16
.space 16384
stack_top:
