/* Samsung's relocatable kernel needs the original x0/FDT, x1 and x2. */
.section .text.entry,"ax"
.global s8_probe_entry
s8_probe_entry:
    mov x19, x0
    mov x20, x1
    mov x21, x2
    mov x22, x3
    mov x23, sp
    mov x24, x30
    mrs x25, daif
    msr daifset, #0xf
    adr x9, probe_stack_end
    mov sp, x9
    bl s8_probe
    dsb sy
    ic iallu
    dsb sy
    isb
    mov x0, x19
    mov x1, x20
    mov x2, x21
    mov x3, x22
    mov sp, x23
    mov x30, x24
    msr daif, x25
    b original_entry
.balign 16
.space 8192
probe_stack_end:
