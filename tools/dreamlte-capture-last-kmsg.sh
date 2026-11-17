#!/bin/sh
# Capture the Exynos last_kmsg over ADB's existing USB connection.
set -eu

if [ "$#" -ne 1 ]; then
    echo "usage: $0 OUTPUT" >&2
    exit 2
fi

adb wait-for-device
adb shell cat /proc/last_kmsg > "$1"
test -s "$1"
printf 'captured %s bytes to %s\n' "$(wc -c < "$1" | tr -d ' ')" "$1"
