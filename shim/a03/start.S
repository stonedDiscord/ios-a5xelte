/* Android EL0 diagnostic entry, not a bootloader entry. */
.section .text.entry,"ax"
.global _start
.type _start, %function
_start:
    bl a03_probe_main
    mov x8, #93
    svc #0
.size _start, .-_start
.section .note.GNU-stack,"",%progbits
