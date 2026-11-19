#!/usr/bin/env python3
"""Reboot a running DREAMLTE XNU phone through its local USB control endpoint."""
import argparse
import sys
import time
import usb.core


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=['status', 'normal', 'download'])
    p.add_argument('--timeout', type=float, default=30, help='seconds to verify USB re-enumeration')
    a = p.parse_args()
    if not 1 <= a.timeout <= 120:
        p.error('--timeout must be between 1 and 120 seconds')
    devices = list(usb.core.find(find_all=True, idVendor=0x1209, idProduct=0x0001))
    if len(devices) != 1:
        raise RuntimeError(f'expected exactly one XNU gadget, found {len(devices)}')
    dev = devices[0]
    ports, bus, address = dev.port_numbers, dev.bus, dev.address
    cap = bytes(dev.ctrl_transfer(0xc0, 0x50, 0, 0x8895, 8, timeout=2000))
    if cap != b'DUSB\x01\x03\x00\x00':
        raise RuntimeError(f'unsupported reboot capability: {cap!r}')
    print('DREAMLTE USB reboot protocol v1: normal + download supported', flush=True)
    if a.mode == 'status':
        return
    dev.ctrl_transfer(0x40, 0x51, int(a.mode == 'download'), 0x8895, b'', timeout=2000)
    print(f'{a.mode} reboot request acknowledged; waiting for same USB port', flush=True)
    deadline = time.monotonic() + a.timeout
    while time.monotonic() < deadline:
        vid, pid = (0x04e8, 0x685d) if a.mode == 'download' else (0x1209, 0x0001)
        for new in usb.core.find(find_all=True, idVendor=vid, idProduct=pid):
            if new.bus == bus and new.port_numbers == ports and new.address != address:
                print(f'PASS: {a.mode} mode enumerated as {vid:04x}:{pid:04x}', flush=True)
                return
        time.sleep(0.25)
    raise RuntimeError(f'request accepted, but {a.mode} re-enumeration was NOT verified')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, usb.core.USBError) as e:
        sys.exit(str(e))
