/* Opt-in PID1 check for the A03 read-only BSD provider.
 * Read one sector through both raw uiomove and buffered block paths.
 * Attempt a write-only OPEN only: never submit any sector write. */
	.p2align 2
storage_test:
	stp x29, x30, [sp, #-16]!
	stp x20, x21, [sp, #-16]!
	stp x23, x24, [sp, #-16]!
	stp x25, x26, [sp, #-16]!
	sub sp, sp, #512
	mov x29, sp
	adr x21, a03_raw_path
	mov x25, #0x10
	bl a03_read_header
	cbnz x0, a03_test_failed
	adr x1, a03_raw_pass
	adr x2, a03_raw_pass_end
	sub x2, x2, x1
	bl write_console
	adr x21, a03_block_path
	mov x25, #0x20
	bl a03_read_header
	cbnz x0, a03_test_failed
	adr x1, a03_block_pass
	adr x2, a03_block_pass_end
	sub x2, x2, x1
	bl write_console
	/* EROFS=30 required. An unexpectedly successful open is closed. */
	mov x23, #0x30
	adr x0, a03_raw_path
	mov x1, #1
	mov x2, #0
	mov x16, #SYS_open
	svc #0x80
	b.cc a03_write_open_unexpected
	mov x24, x0
	cmp x0, #30
	b.ne a03_test_failed
	adr x1, a03_storage_pass
	adr x2, a03_storage_pass_end
	b a03_storage_report
a03_write_open_unexpected:
	mov x23, #0x31
	mov x24, x0
	mov x16, #6
	svc #0x80
a03_test_failed:
	adr x1, a03_stage_label
	adr x2, a03_stage_label_end
	sub x2, x2, x1
	bl write_console
	mov x0, x23
	bl a03_print_hex
	adr x1, a03_value_label
	adr x2, a03_value_label_end
	sub x2, x2, x1
	bl write_console
	mov x0, x24
	bl a03_print_hex
	adr x1, a03_storage_fail
	adr x2, a03_storage_fail_end
a03_storage_report:
	sub x2, x2, x1
	bl write_console
	add sp, sp, #512
	ldp x25, x26, [sp], #16
	ldp x23, x24, [sp], #16
	ldp x20, x21, [sp], #16
	ldp x29, x30, [sp], #16
	ret

/* x21 path, x29 private512B buffer. Return0 on validated header. */
a03_read_header:
	stp x22, x30, [sp, #-16]!
	mov x23, x25
	mov x0, x21
	mov x1, #0
	mov x2, #0
	mov x16, #SYS_open
	svc #0x80
	b.cs a03_read_open_failed
	mov x20, x0
	add x23, x25, #1
	mov x1, x29
	mov x2, #512
	mov x16, #3
	svc #0x80
	b.cs a03_read_bad
	add x23, x25, #2
	cmp x0, #512
	b.ne a03_read_bad
	ldr x0, [x29]
	add x23, x25, #3
	mov x1, #0x4e41
	movk x1, #0x5244, lsl #16
	movk x1, #0x494f, lsl #32
	movk x1, #0x2144, lsl #48
	cmp x0, x1
	b.ne a03_read_bad
	ldr w0, [x29, #36]
	add x23, x25, #4
	cmp w0, #2048
	b.ne a03_read_bad
	ldr w0, [x29, #40]
	add x23, x25, #5
	cmp w0, #2
	b.ne a03_read_bad
	mov x22, #0
	b a03_read_close
a03_read_bad:
	mov x24, x0
	mov x22, #1
a03_read_close:
	mov x0, x20
	mov x16, #6
	svc #0x80
	mov x0, x22
	ldp x22, x30, [sp], #16
	ret
a03_read_open_failed:
	mov x24, x0
	mov x0, #1
	ldp x22, x30, [sp], #16
	ret

/* Print x0 as sixteen hex digits and newline, using stack-only storage. */
a03_print_hex:
	stp x29, x30, [sp, #-16]!
	sub sp, sp, #32
	mov x9, #16
	mov x10, sp
1:
	lsr x11, x0, #60
	cmp x11, #10
	add x12, x11, #'0'
	add x13, x11, #('a' - 10)
	csel x12, x12, x13, lo
	strb w12, [x10], #1
	lsl x0, x0, #4
	subs x9, x9, #1
	b.ne 1b
	mov w12, #10
	strb w12, [x10]
	mov x1, sp
	mov x2, #17
	bl write_console
	add sp, sp, #32
	ldp x29, x30, [sp], #16
	ret
a03_raw_path:
	.asciz "/dev/ra03boot0"
a03_block_path:
	.asciz "/dev/a03boot0"
a03_storage_pass:
	.ascii "A03 STORAGE PID1 PASS: raw+block BOOT reads, write-open EROFS\n"
a03_storage_pass_end:
a03_storage_fail:
	.ascii "A03 STORAGE PID1 FAIL: inspect kernel SDMA/GPT/device diagnostics\n"
a03_storage_fail_end:
a03_raw_pass:
	.ascii "A03 STORAGE raw BOOT header PASS\n"
a03_raw_pass_end:
a03_block_pass:
	.ascii "A03 STORAGE block BOOT header PASS\n"
a03_block_pass_end:
a03_stage_label:
	.ascii "A03 STORAGE FAIL stage=0x"
a03_stage_label_end:
a03_value_label:
	.ascii "A03 STORAGE FAIL value=0x"
a03_value_label_end:
