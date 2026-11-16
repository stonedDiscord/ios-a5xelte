#!/usr/bin/env python3
"""Send one bounded input command through EP0, without opening the console tty.

Requires the A03 HID provider and a03_hid=1. Read results from the existing
USB console capture. A transfer acknowledgement means queued, not completed.
"""
import argparse
from a03_usb_probe import Probe


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('status', 'home', 'swipeup'))
    args = parser.parse_args()
    with Probe() as probe:
        probe.send('input ' + args.action)
    print('Queued input ' + args.action + '; inspect the existing console capture for completion.')
    print('Dispatch success does not establish that the UI received or acted on the event.')


if __name__ == '__main__':
    main()
