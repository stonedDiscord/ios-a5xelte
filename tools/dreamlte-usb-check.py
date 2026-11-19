#!/usr/bin/env python3
"""Check the running DREAMLTE ECM gadget; optionally verify its IPv4 link.

Requires PyUSB. Does not configure interfaces, detach drivers or flash devices.
--interface requires an already configured host address 192.168.7.1/24.
--console-seconds also requires identifiable XNU console bytes on UDP5140;
no listener may already own that address/port. --console-log saves validated
bytes only. Neither ping nor enumeration alone proves working console output.
"""
import argparse
import json
from pathlib import Path
import subprocess
import socket
import time
import sys
import usb.core
import usb.util

def receive_console(listener, seconds, expected_peer):
    """Require identifiable XNU text received over the selected UDP link."""
    deadline = time.monotonic() + seconds
    chunks = []
    while time.monotonic() < deadline:
        listener.settimeout(max(0.001, deadline - time.monotonic()))
        try:
            data, peer = listener.recvfrom(65535)
        except socket.timeout:
            break
        if peer[0] == expected_peer and data:
            chunks.append(data)
    data = b''.join(chunks)
    if not data:
        raise RuntimeError('no UDP console data received from the XNU device')
    if not any(marker in data for marker in (b'DREAMLTE ', b'SWEET USB:', b'Darwin Kernel Version')):
        raise RuntimeError('UDP data arrived but contained no recognized XNU console marker')
    return data


p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--interface', help='also verify ping to 192.168.7.2 on this ECM interface')
p.add_argument('--console-seconds', type=float, help='also require XNU UDP5140 console text within this capture window (0 < seconds <= 300)')
p.add_argument('--console-log', type=Path, help='save validated console bytes; requires --console-seconds')
a = p.parse_args()
if a.console_seconds is not None and not (0 < a.console_seconds <= 300):
    p.error('--console-seconds must be greater than zero and at most 300')
if a.console_seconds is not None and not a.interface:
    p.error('--console-seconds requires --interface')
if a.console_log and a.console_seconds is None:
    p.error('--console-log requires --console-seconds')
try:
    devices = list(usb.core.find(find_all=True, idVendor=0x1209, idProduct=0x0001))
    if len(devices) != 1:
        raise RuntimeError(f'expected one test gadget 1209:0001, found {len(devices)}')
    dev = devices[0]
    # GET_DESCRIPTOR over EP0, independently of cached sysfs descriptors.
    descriptor = bytes(dev.ctrl_transfer(0x80, 6, 0x100, 0, 18, timeout=2000))
    if len(descriptor) != 18 or descriptor[4:8] != bytes([2, 0, 0, 64]):
        raise RuntimeError('unexpected ECM device descriptor')
    config = bytes(dev.ctrl_transfer(0x80, 6, 0x200, 0, 255, timeout=2000))
    if len(config) != 80 or config[2:4] != bytes([80, 0]):
        raise RuntimeError('unexpected ECM configuration length')
    interfaces = set()
    endpoints = set()
    offset = 0
    while offset < len(config):
        length, kind = config[offset:offset + 2]
        if length < 2 or offset + length > len(config):
            raise RuntimeError('malformed configuration descriptor')
        d = config[offset:offset + length]
        if kind == 4:
            interfaces.add((d[2], d[3], d[5], d[6]))
        if kind == 5:
            endpoints.add((d[2], d[3] & 3, int.from_bytes(d[4:6], 'little')))
        offset += length
    if not {(0, 0, 2, 6), (1, 0, 10, 0), (1, 1, 10, 0)} <= interfaces:
        raise RuntimeError('ECM interfaces missing')
    if endpoints != {(0x82, 3, 16), (0x81, 2, 512), (1, 2, 512)}:
        raise RuntimeError('unexpected ECM endpoints')
    status = bytes(dev.ctrl_transfer(0x80, 0, 0, 0, 2, timeout=2000))
    configured = bytes(dev.ctrl_transfer(0x80, 8, 0, 0, 1, timeout=2000))
    if status != b'\0\0' or configured != b'\1':
        raise RuntimeError('gadget is not configured or returned unexpected status')
    result = {'usb': 'control transfers PASS', 'bus': dev.bus, 'address': dev.address,
              'ecm_endpoints': sorted(endpoints), 'network': 'not tested'}
    if a.interface:
        net = Path('/sys/class/net') / a.interface
        if not net.exists() or net.resolve().parent.name != 'net':
            raise RuntimeError('network interface does not exist')
        if (net / 'address').read_text().strip().lower() != '02:00:5e:77:ee:01':
            raise RuntimeError('interface MAC is not the DREAMLTE ECM host MAC')
        parent = (net / 'device').resolve()
        while parent != parent.parent and not (parent / 'idVendor').exists():
            parent = parent.parent
        for key, expected in [('idVendor', '1209'), ('idProduct', '0001')]:
            if not (parent / key).exists() or (parent / key).read_text().strip() != expected:
                raise RuntimeError('interface is not attached to the expected USB gadget')
        listener = None
        try:
            if a.console_seconds is not None:
                listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                listener.bind(('192.168.7.1', 5140))
            subprocess.run(['ping', '-n', '-I', a.interface, '-c', '3', '-W', '2', '192.168.7.2'], check=True)
            result['network'] = 'three ICMP request/reply exchanges PASS'
            if listener is not None:
                data = receive_console(listener, a.console_seconds, '192.168.7.2')
                if a.console_log:
                    a.console_log.write_bytes(data)
                result['console'] = {'status': 'XNU UDP text PASS', 'bytes': len(data),
                                     'peer': '192.168.7.2', 'port': 5140}
        finally:
            if listener is not None:
                listener.close()
    print(json.dumps(result, indent=2))
except (RuntimeError, usb.core.USBError, OSError, subprocess.CalledProcessError) as e:
    print(f'DREAMLTE USB check failed: {e}', file=sys.stderr)
    sys.exit(1)
