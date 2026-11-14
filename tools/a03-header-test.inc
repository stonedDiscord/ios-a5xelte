/* Read the primary HFSX volume header at USERDATA-relative byte offset 1024. */
	.p2align 2
a03_header_test:
	stp	x29, x30, [sp, #-16]!
	stp	x20, x21, [sp, #-16]!
	stp	x22, x23, [sp, #-16]!
	sub	sp, sp, #528
	mov	x29, sp
	adr	x20, a03_header_raw_path
	mov	w21, #0
a03_header_next:
	mov	x0, x20
	mov	x1, #0
	mov	x2, #0
	mov	x16, #SYS_open
	svc	#0x80
	b.cs	a03_header_open_fail
	mov	x22, x0
	mov	x0, x22
	mov	x1, x29
	mov	x2, #512
	mov	x3, #1024
	mov	x16, #SYS_pread
	svc	#0x80
	b.cs	a03_header_read_fail
	cmp	x0, #512
	b.ne	a03_header_read_fail
	mov	x0, x22
	mov	x16, #6
	svc	#0x80
	cmp	w21, #0
	adr	x1, a03_header_raw_label
	adr	x2, a03_header_raw_label_end
	b.eq	1f
	adr	x1, a03_header_block_label
	adr	x2, a03_header_block_label_end
1:
	sub	x2, x2, x1
	bl	a03_header_print16
	ldrh	w0, [x29]
	mov	w1, #0x5848
	cmp	w0, w1
	adr	x1, a03_header_hx
	adr	x2, a03_header_hx_end
	b.eq	2f
	adr	x1, a03_header_bad
	adr	x2, a03_header_bad_end
2:
	sub	x2, x2, x1
	bl	write_console
	cmp	w21, #0
	b.ne	3f
	adr	x20, a03_header_block_path
	mov	w21, #1
	b	a03_header_next
3:
	b	a03_header_done
a03_header_open_fail:
	mov	x23, x0
	b	a03_header_error
a03_header_read_fail:
	mov	x23, x0
	mov	x0, x22
	mov	x16, #6
	svc	#0x80
a03_header_error:
	adr	x1, a03_header_error_text
	adr	x2, a03_header_error_text_end
	sub	x2, x2, x1
	bl	write_console
	mov	x0, x23
	bl	a03_print_hex
a03_header_done:
	add	sp, sp, #528
	ldp	x22, x23, [sp], #16
	ldp	x20, x21, [sp], #16
	ldp	x29, x30, [sp], #16
	ret

/* x1 label, x2 label length, x29 data buffer. */
a03_header_print16:
	stp	x29, x30, [sp, #-16]!
	stp	x24, x25, [sp, #-16]!
	sub	sp, sp, #48
	mov	x24, x1
	mov	x25, x2
	mov	x0, x19
	mov	x1, x24
	mov	x2, x25
	mov	x16, #SYS_write
	svc	#0x80
	mov	x9, #0
	mov	x10, x29
1:
	ldrb	w11, [x10, x9]
	lsr	w12, w11, #4
	and	w13, w11, #15
	cmp	w12, #10
	add	w14, w12, #'0'
	add	w15, w12, #('a' - 10)
	csel	w14, w14, w15, lo
	add	x17, sp, x9, lsl #1
	strb	w14, [x17]
	cmp	w13, #10
	add	w14, w13, #'0'
	add	w15, w13, #('a' - 10)
	csel	w14, w14, w15, lo
	add	x16, sp, #1
	add	x17, x16, x9, lsl #1
	strb	w14, [x17]
	add	x9, x9, #1
	cmp	x9, #16
	b.ne	1b
	mov	w11, #10
	strb	w11, [sp, #32]
	mov	x0, x19
	mov	x1, sp
	mov	x2, #33
	mov	x16, #SYS_write
	svc	#0x80
	add	sp, sp, #48
	ldp	x24, x25, [sp], #16
	ldp	x29, x30, [sp], #16
	ret

a03_header_raw_path:	.asciz "/dev/ra03userdata0"
a03_header_block_path:	.asciz "/dev/a03userdata0"
a03_header_raw_label:	.ascii "A03 HFS header raw first16="
a03_header_raw_label_end:
a03_header_block_label:	.ascii "A03 HFS header block first16="
a03_header_block_label_end:
a03_header_hx:	.ascii " HFSX\n"
a03_header_hx_end:
a03_header_bad:	.ascii " NOT-HX\n"
a03_header_bad_end:
a03_header_error_text:	.ascii "A03 HFS header read/open error=0x"
a03_header_error_text_end:
