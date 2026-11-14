#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p out
case ${A03_EMMC_SNAPSHOT:-0} in
  0) diagnostic= ;;
  1) diagnostic=-DA03_EMMC_SNAPSHOT=1 ;;
  2) diagnostic=-DA03_EMMC_SNAPSHOT=2 ;;
  3) diagnostic=-DA03_EMMC_SNAPSHOT=3 ;;
  4) diagnostic=-DA03_EMMC_SNAPSHOT=4 ;;
  5) diagnostic=-DA03_EMMC_SNAPSHOT=5 ;;
  *) echo 'A03_EMMC_SNAPSHOT must be 0, 1, 2, 3, 4 or 5' >&2; exit 2 ;;
esac
for src in xnu-entry.S xnu-loader.c; do
 clang --target=aarch64-none-elf -march=armv8.2-a -O2 -ffreestanding -fno-builtin -fno-stack-protector -fno-pic -fno-pie -nostdlib -mgeneral-regs-only -mstrict-align -Wall -Wextra -Werror $diagnostic -c "$src" -o "out/$src.o"
done
ld.lld -T xnu-image.ld --build-id=none out/xnu-entry.S.o out/xnu-loader.c.o -o out/a03-xnu-loader.elf
llvm-objcopy -O binary out/a03-xnu-loader.elf out/a03-xnu-loader.Image
# objcopy does not emit trailing linker alignment: pad to payload boundary.
python3 - <<'PYIMAGE'
from pathlib import Path
import subprocess
p=Path('out/a03-xnu-loader.Image')
symbols=subprocess.check_output(['llvm-nm','out/a03-xnu-loader.elf'],text=True)
end=int(next(l.split()[0] for l in symbols.splitlines() if l.endswith(' _image_end')),16)
data=p.read_bytes()
assert len(data)<=end and end%4096==0
p.write_bytes(data+bytes(end-len(data)))
print('A03 loader:',end,'bytes, payload boundary padded')
PYIMAGE
