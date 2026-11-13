#!/bin/sh
# Static AArch64 Linux executable; no NDK or libc dependency.
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
out=${1:-"$here/out"}
mkdir -p "$out"
clang --target=aarch64-linux-android33 -march=armv8-a -O2 \
    -ffreestanding -fno-builtin -fno-stack-protector -fno-pic -fno-pie \
    -mgeneral-regs-only -mstrict-align -Wall -Wextra -Werror \
    -c "$here/probe.c" -o "$out/probe.o"
clang --target=aarch64-linux-android33 -c "$here/start.S" -o "$out/start.o"
ld.lld -static -e _start --build-id=none -z noexecstack \
    "$out/start.o" "$out/probe.o" -o "$out/a03-el0-probe"
printf '%s\n' "$out/a03-el0-probe"
