ENTRY(_start)
SECTIONS
{
    . = 0;
    .text : { KEEP(*(.text.head)) *(.text*) }
    .rodata : { *(.rodata*) }
    /* Stack/data are stored in the raw Image; build-xnu.sh pads alignment. */
    .data : { *(.data*) *(.bss*) *(COMMON) }
    . = ALIGN(4096);
    _image_end = .;
    /DISCARD/ : { *(.note*) *(.comment*) *(.eh_frame*) }
}
