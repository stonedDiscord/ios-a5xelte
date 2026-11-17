#!/bin/sh
# Build only. Does not package or flash a boot image.
set -eu
cd "$(dirname "$0")"
mkdir -p out
for src in xnu_boot.S xnu_boot.c fbtext.c ../fdt.c; do
    obj="out/$(basename "$src" | tr . _).o"
    clang --target=aarch64-none-elf -c -O2 -ffreestanding -fno-builtin         -fno-stack-protector -fno-pic -fno-pie -nostdlib         -fno-asynchronous-unwind-tables -fno-jump-tables         -mgeneral-regs-only -mstrict-align -mcpu=cortex-a53         -Wall -Wextra -Werror "$src" -o "$obj"
done
ld.lld -static -T image.ld --build-id=none out/xnu_boot_S.o     out/xnu_boot_c.o out/fbtext_c.o out/fdt_c.o -o out/xnu_boot.elf
if llvm-readelf -r out/*_?.o | grep -q ABS64; then
    echo 'absolute relocation in loader' >&2
    exit 1
fi
llvm-objcopy -O binary out/xnu_boot.elf out/xnu_boot.Image
python3 - <<'PY'
from pathlib import Path
b = Path('out/xnu_boot.Image').read_bytes()
assert b[56:60] == b'ARMd'
print('dreamlte loader:',len(b),'bytes; Image header OK; NOT device-tested')
PY
