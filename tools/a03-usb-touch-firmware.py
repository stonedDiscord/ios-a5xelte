#!/usr/bin/env python3
"""Upload a validated private firmware to kernel staging RAM over EP0.

Requires0148 and an existing single-reader console log. Does NOT issue load.
The separate touch load command changes controller RAM/MCU state explicitly.
"""
import argparse
import importlib.util
from pathlib import Path
import time
from a03_usb_probe import Probe


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('firmware',type=Path)
    parser.add_argument('--log',type=Path,required=True,help='live console log from existing reader')
    args=parser.parse_args()
    spec=importlib.util.spec_from_file_location('inspect_fw',Path(__file__).with_name('a03-inspect-jadard-firmware.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    data=args.firmware.read_bytes();info=module.inspect(data)
    if not 256<=len(data)<=81920:parser.error('requires256..81920bytes')
    print('Staging candidate SHA256 '+info['sha256']+'; board compatibility unverified',flush=True)
    with args.log.open('rb') as log,Probe() as probe:
        log.seek(0,2)
        def send(command,expected):
            start=log.tell();probe.send(command)
            deadline=time.monotonic()+15
            block=b''
            while time.monotonic()<deadline:
                block+=log.read()
                if b'A03 TOUCH upload rejected' in block or b'A03 TOUCH upload bad size' in block:
                    raise RuntimeError('kernel refused chunk; no further chunks sent')
                # Wait for both acknowledgement and workerEND before next send.
                if expected.encode() in block and b' END' in block:return
                time.sleep(.01)
            raise RuntimeError('missing acknowledgement at log offset '+str(start)+'; stopped')
        send('touch fwbegin '+str(len(data)),'A03 TOUCH upload begin '+str(len(data)))
        for offset in range(0,len(data),32):
            part=data[offset:offset+32];next_offset=offset+len(part)
            send('touch fwdata '+str(offset)+' '+part.hex(),'A03 TOUCH upload next '+str(next_offset))
            if next_offset%4096==0 or next_offset==len(data):print(str(next_offset)+'/'+str(len(data)),flush=True)
        send('touch fwstatus','A03 TOUCH upload '+str(len(data))+'/'+str(len(data))+' valid=0')
    print('Staging validated. No controller load sent.',flush=True)


if __name__=='__main__':
    main()
