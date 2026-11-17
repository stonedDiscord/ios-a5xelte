#!/usr/bin/env python3
"""Explicit continuous A03 touch trial using an existing single-reader log.

Requires0154. Firmware must already be staged and loaded. Never loads firmware,
flashes partitions, or opens the console tty. Default mode is log-only.
"""
import argparse
from pathlib import Path
import re
import time
from a03_usb_probe import Probe


def command(probe, log, value, timeout=20):
    """Wait for this exact worker transaction, not an unrelated END line."""
    log.seek(0, 2)
    probe.send('touch ' + value)
    deadline = time.monotonic() + timeout
    data = b''
    while time.monotonic() < deadline:
        data += log.read()
        begin = re.search(rb'A03 PROBE (\d+) BEGIN touch ' +
                          re.escape(value.encode()) + rb'\r?\n', data)
        if begin:
            end = re.search(rb'A03 PROBE ' + begin[1] + rb' END\r?\n',
                            data[begin.end():])
            if end:
                return data[begin.end():begin.end() + end.start()].decode(errors='replace')
        time.sleep(.02)
    raise RuntimeError('missing completion for touch ' + value + '; no retry sent')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--log', type=Path, required=True, help='existing live console capture')
    ap.add_argument('--mode', choices=('contacts', 'hid', 'status', 'stop'), default='contacts')
    ap.add_argument('--duration', type=float, default=30, help='trial seconds before explicit stop')
    args = ap.parse_args()
    if not 1 <= args.duration <= 3600:
        ap.error('duration must be1..3600seconds')
    with args.log.open('rb') as log, Probe() as probe:
        if args.mode in ('status', 'stop'):
            reply = command(probe, log, 'streamstatus' if args.mode == 'status' else 'stop')
            print(reply, end='')
            expected = 'A03 TOUCH streaming=' if args.mode == 'status' else 'A03 TOUCH stream stopped'
            if expected not in reply:
                raise RuntimeError('continuous polling unavailable; requires0154')
            return
        status = command(probe, log, 'streamstatus')
        state = re.search(r'A03 TOUCH streaming=(\d+)', status)
        if not state:
            raise RuntimeError('continuous polling unavailable; requires0154')
        if state[1] != '0':
            raise RuntimeError('existing stream active; use --mode status or --mode stop')
        start = 'start' if args.mode == 'hid' else 'startcontacts'
        # If the start acknowledgement is lost, still request a stop: the EP0
        # command may already have taken effect. Never resend start.
        try:
            reply = command(probe, log, start)
            print(reply, end='', flush=True)
            expected = 'A03 TOUCH stream requested hid=' + ('1' if args.mode == 'hid' else '0')
            if expected not in reply:
                raise RuntimeError('stream start refused; see transaction above')
            print('Trial running for ' + str(args.duration) + ' seconds; touch, move, and lift now.', flush=True)
            deadline = time.monotonic() + args.duration
            while time.monotonic() < deadline:
                time.sleep(min(.1, max(0, deadline-time.monotonic())))
            print(command(probe, log, 'streamstatus'), end='', flush=True)
        finally:
            reply = command(probe, log, 'stop')
            print(reply, end='', flush=True)
            if 'A03 TOUCH stream stopped' not in reply:
                raise RuntimeError('stream stop not acknowledged')


if __name__ == '__main__':
    main()
