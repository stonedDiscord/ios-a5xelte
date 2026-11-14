/* Read the first catalog B-tree sector through both USERDATA BSD nodes. */
	.p2align 2
a03_catalog_test:
	stp	x29, x30, [sp, #-16]!
	stp	x20, x21, [sp, #-16]!
	stp	x22, x23, [sp, #-16]!
	sub	sp, sp, #528
	mov	x29, sp
	adr	x20, a03_catalog_raw_path
	mov	w21, #0
a03_catalog_next:
	mov	x0, x20
	mov	x1, #0
	mov	x2, #0
	mov	x16, #SYS_open
	svc	#0x80
	b.cs	a03_catalog_open_fail
	mov	x22, x0
	mov	x0, x22
	mov	x1, x29
	mov	x2, #512
	mov	x3, #0x2000
	movk	x3, #0x2cd8, lsl #16
	mov	x16, #SYS_pread
	svc	#0x80
	b.cs	a03_catalog_read_fail
	cmp	x0, #512
	b.ne	a03_catalog_read_fail
	mov	x0, x22
	mov	x16, #6
	svc	#0x80
	cmp	w21, #0
	adr	x1, a03_catalog_raw_label
	adr	x2, a03_catalog_raw_label_end
	b.eq	1f
	adr	x1, a03_catalog_block_label
	adr	x2, a03_catalog_block_label_end
1:
	sub	x2, x2, x1
	bl	write_console
	mov	x9, #0
	adr	x10, a03_catalog_expected
2:
	ldrb	w11, [x10, x9]
	ldrb	w12, [x29, x9]
	cmp	w11, w12
	b.ne	a03_catalog_mismatch
	add	x9, x9, #1
	cmp	x9, #16
	b.ne	2b
	adr	x1, a03_catalog_match
	adr	x2, a03_catalog_match_end
	b	3f
a03_catalog_mismatch:
	adr	x1, a03_catalog_mismatch_text
	adr	x2, a03_catalog_mismatch_text_end
3:
	sub	x2, x2, x1
	bl	write_console
	mov	x9, #0
	mov	x10, x29
	sub	sp, sp, #48
4:
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
	b.ne	4b
	mov	w11, #10
	strb	w11, [sp, #32]
	mov	x1, sp
	mov	x2, #33
	bl	write_console
	add	sp, sp, #48
	cmp	w21, #0
	b.ne	5f
	adr	x20, a03_catalog_block_path
	mov	w21, #1
	b	a03_catalog_next
5:
	b	a03_catalog_done
a03_catalog_open_fail:
	mov	x23, x0
	b	a03_catalog_error
a03_catalog_read_fail:
	mov	x23, x0
	mov	x0, x22
	mov	x16, #6
	svc	#0x80
a03_catalog_error:
	adr	x1, a03_catalog_error_text
	adr	x2, a03_catalog_error_text_end
	sub	x2, x2, x1
	bl	write_console
	mov	x0, x23
	bl	a03_print_hex
a03_catalog_done:
	add	sp, sp, #528
	ldp	x22, x23, [sp], #16
	ldp	x20, x21, [sp], #16
	ldp	x29, x30, [sp], #16
	ret

a03_catalog_raw_path:	.asciz "/dev/ra03userdata0"
a03_catalog_block_path:	.asciz "/dev/a03userdata0"
a03_catalog_raw_label:	.ascii "A03 CATALOG raw first16="
a03_catalog_raw_label_end:
a03_catalog_block_label:	.ascii "A03 CATALOG block first16="
a03_catalog_block_label_end:
a03_catalog_match:	.ascii " MATCH\n"
a03_catalog_match_end:
a03_catalog_mismatch_text:	.ascii " MISMATCH\n"
a03_catalog_mismatch_text_end:
a03_catalog_error_text:	.ascii "A03 CATALOG read/open error=0x"
a03_catalog_error_text_end:
a03_catalog_expected:
	/* HFSX node 0 from the verified iOS 16 image at allocation block 183682. */
	.byte 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00
	.byte 0x01,0x00,0x00,0x03,0x00,0x00,0x00,0x03
