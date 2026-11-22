#!/bin/bash
# Build the mediaserverd HAL plug-in for the iPhone X iOS 16 root.
set -euo pipefail
if [[ $# != 1 ]]; then
    echo "usage: $0 OUTPUT_DIRECTORY" >&2
    exit 2
fi
src=$(cd "$(dirname "$0")" && pwd)
out=$1
mkdir -p "$out"
sdk=$(xcrun --sdk iphoneos --show-sdk-path)
xcrun --sdk iphoneos clang -target arm64-apple-ios16.0 -isysroot "$sdk" \
    -O2 -bundle -I"$src" "$src/audio_plugin.c" -o "$out/HakiosAudio" \
    -framework CoreFoundation -lm
cp "$src/audio_plugin.plist" "$out/Info.plist"
plutil -lint "$out/Info.plist"
codesign -s - -f "$out/HakiosAudio"
codesign --verify --strict "$out/HakiosAudio"
