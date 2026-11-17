#!/usr/bin/env python3
"""Offline firmware inspector tests using synthetic bytes only."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('firmware', Path(__file__).with_name('a03-inspect-jadard-firmware.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
assert m.crc16(b'123456789') == 0xaee7
image = bytearray(272)
image[3] = 15  # real format has a floor-divided length with remainder 1
image[5:17] = bytes.fromhex('00000100000f200020000000')
image[256:] = bytes(range(16))
image[15:17] = m.crc16(image[256:]).to_bytes(2, 'big')
result = m.inspect(image)
assert len(result['moves']) == 1
assert result['moves'][0]['target'] == 0x20002000
assert result['moves'][0]['size'] == 16

def reject(data):
    try:
        m.inspect(data)
    except ValueError:
        return
    raise AssertionError('invalid image accepted')

for length in range(17):
    reject(image[:length])
reject(image[:-1])
bad = image.copy(); bad[3] = 255; reject(bad)
bad = image.copy(); bad[256] ^= 1; reject(bad)
bad = image.copy(); bad[6:9] = bytes(3); reject(bad)
bad = image.copy(); bad[11:15] = bytes.fromhex('fffffff8'); reject(bad)
print('PASS JD9365T offline inspector: CRC vector, stock move length, truncation, bounds, corruption, wrap')
