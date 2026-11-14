/* Opt-in PID1 check for the A03 read-only BSD provider.
 * Read one sector through both raw physio and buffered block paths.
 * Attempt a write-only OPEN only: never submit any sector write. */
	.p2align 2
storage_test:
	stp x29, x30, [sp, #-16]!
	stp x20, x21, [sp, #-16]!
	sub sp, sp, #512
	mov x29, sp
	adr x21, a03_raw_path
	bl a03_read_header
	cbnz x0, a03_test_failed
	adr x21, a03_block_path
	bl a03_read_header
	cbnz x0, a03_test_failed
	/* EROFS=30 required. An unexpectedly successful open is closed. */
	adr x0, a03_raw_path
	mov x1, #1
	mov x2, #0
	mov x16, #SYS_open
	svc #0x80
	b.cc a03_write_open_unexpected
	cmp x0, #30
	b.ne a03_test_failed
	adr x1, a03_storage_pass
	adr x2, a03_storage_pass_end
	b a03_storage_report
a03_write_open_unexpected:
	mov x16, #6
	svc #0x80
a03_test_failed:
	adr x1, a03_storage_fail
	adr x2, a03_storage_fail_end
a03_storage_report:
	sub x2, x2, x1
	bl write_console
	add sp, sp, #512
	ldp x20, x21, [sp], #16
	ldp x29, x30, [sp], #16
	ret

/* x21 path, x29 private512B buffer. Return0 on validated header. */
a03_read_header:
	stp x22, x30, [sp, #-16]!
	mov x0, x21
	mov x1, #0
	mov x2, #0
	mov x16, #SYS_open
	svc #0x80
	b.cs a03_read_open_failed
	mov x20, x0
	mov x1, x29
	mov x2, #512
	mov x16, #3
	svc #0x80
	b.cs a03_read_bad
	cmp x0, #512
	b.ne a03_read_bad
	ldr x0, [x29]
	mov x1, #0x4e41
	movk x1, #0x5244, lsl #16
	movk x1, #0x494f, lsl #32
	movk x1, #0x2144, lsl #48
	cmp x0, x1
	b.ne a03_read_bad
	ldr w0, [x29, #36]
	cmp w0, #2048
	b.ne a03_read_bad
	ldr w0, [x29, #40]
	cmp w0, #2
	b.ne a03_read_bad
	mov x22, #0
	b a03_read_close
a03_read_bad:
	mov x22, #1
a03_read_close:
	mov x0, x20
	mov x16, #6
	svc #0x80
	mov x0, x22
	ldp x22, x30, [sp], #16
	ret
a03_read_open_failed:
	mov x0, #1
	ldp x22, x30, [sp], #16
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
