/* Explicit opt-in destructive USERDATA diagnostic. One sector at relative
 * 16GiB (immediately beyond the planned16GiB root) is saved, changed, read
 * back, restored and rechecked. Never touches BOOT/GPT. Requires rw kernel.
 * On failure after a write attempt, make one best-effort restore; the driver
 * may already be poisoned. PASS requires full restore/readback/fsync. */
	.p2align 2
a03_userdata_test:
	stp x29, x30, [sp, #-16]!
	stp x20, x21, [sp, #-16]!
	stp x22, x27, [sp, #-16]!
	stp x25, x26, [sp, #-16]!
	stp x28, xzr, [sp, #-16]!
	sub sp, sp, #1536
	mov x21, sp
	add x22, sp, #512
	add x27, sp, #1024
	mov x28, #0 /* original sector not yet saved */
	mov x25, #0 /* first failure stage, zero means success */
	mov x23, #0x40
	adr x0, a03_userdata_path
	mov x1, #O_RDWR
	mov x2, #0
	mov x16, #SYS_open
	svc #0x80
	b.cs a03_userdata_failed
	mov x20, x0
	mov x23, #0x41
	mov x1, x21
	mov x16, #153
	bl a03_userdata_io
	b.cs a03_userdata_failed
	mov x28, #1
	/* Change every byte, so an unchanged or stale read cannot pass. */
	mov x9, #0
	mov w11, #0xa5
1:
	ldrb w10, [x21, x9]
	eor w10, w10, w11
	strb w10, [x22, x9]
	add x9, x9, #1
	cmp x9, #512
	b.ne 1b
	mov x23, #0x42
	mov x1, x22
	mov x16, #154
	bl a03_userdata_io
	b.cs a03_userdata_failed
	mov x23, #0x43
	mov x1, x27
	mov x16, #153
	bl a03_userdata_io
	b.cs a03_userdata_failed
	mov x23, #0x44
	mov x1, x22
	bl a03_userdata_compare
	cbnz x0, a03_userdata_failed
	b a03_userdata_restore

a03_userdata_failed:
	mov x25, x23
	mov x26, x0
	cbz x28, a03_userdata_report_fail

a03_userdata_restore:
	mov x23, #0x45
	mov x1, x21
	mov x16, #154
	bl a03_userdata_io
	b.cs a03_userdata_restore_failed
	mov x23, #0x46
	mov x1, x27
	mov x16, #153
	bl a03_userdata_io
	b.cs a03_userdata_restore_failed
	mov x23, #0x47
	mov x1, x21
	bl a03_userdata_compare
	cbnz x0, a03_userdata_restore_failed
	mov x23, #0x48
	mov x0, x20
	mov x16, #95 /* fsync */
	svc #0x80
	b.cs a03_userdata_restore_failed
	mov x0, x20
	mov x16, #6
	svc #0x80
	cbnz x25, a03_userdata_report_fail
	adr x1, a03_userdata_pass
	adr x2, a03_userdata_pass_end
	b a03_userdata_report

a03_userdata_restore_failed:
	/* Report restore failure in preference to the triggering error. */
	mov x25, x23
	mov x26, x0
a03_userdata_report_fail:
	adr x1, a03_write_stage
	adr x2, a03_write_stage_end
	sub x2, x2, x1
	bl write_console
	mov x0, x25
	bl a03_print_hex
	adr x1, a03_value_label
	adr x2, a03_value_label_end
	sub x2, x2, x1
	bl write_console
	mov x0, x26
	bl a03_print_hex
	adr x1, a03_userdata_fail
	adr x2, a03_userdata_fail_end
a03_userdata_report:
	sub x2, x2, x1
	bl write_console
	add sp, sp, #1536
	ldp x28, xzr, [sp], #16
	ldp x25, x26, [sp], #16
	ldp x22, x27, [sp], #16
	ldp x20, x21, [sp], #16
	ldp x29, x30, [sp], #16
	ret

/* x1=buffer, x16=pread/pwrite; return carry on syscall error/short I/O. */
a03_userdata_io:
	mov x0, x20
	mov x2, #512
	mov x3, #0x400000000
	svc #0x80
	b.cs 1f
	cmp x0, #512
	b.ne 2f
	/* cmp equality sets carry; return carry CLEAR for success. */
	cmp x0, #513
1:
	ret
2:
	cmp x0, #0 /* any unsigned value >=0 sets carry */
	ret

/* Compare readback x27 to expected x1. Nonzero byte index+1 on mismatch. */
a03_userdata_compare:
	mov x0, #0
1:
	ldrb w9, [x1, x0]
	ldrb w10, [x27, x0]
	add x0, x0, #1
	cmp w9, w10
	b.ne 2f
	cmp x0, #512
	b.ne 1b
	mov x0, #0
2:
	ret

a03_userdata_path:
	.asciz "/dev/ra03userdata0"
a03_userdata_pass:
	.ascii "A03 USERDATA WRITE PASS: changed/readback/restored/fsync sector at16GiB\n"
a03_userdata_pass_end:
a03_userdata_fail:
	.ascii "A03 USERDATA WRITE FAIL: check stage; restore may be incomplete\n"
a03_userdata_fail_end:
a03_write_stage:
	.ascii "A03 USERDATA WRITE FAIL stage=0x"
a03_write_stage_end:
