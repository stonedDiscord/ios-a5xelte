#!/usr/bin/env python3
"""Capture the A03 XNU CDC ACM console to stdout and a private local log.
Only opens a tty with exact diagnostic serial + VID/PID. No phone writes.
"""
import argparse,os,select,sys,termios,time
from pathlib import Path

def find():
    found=[]
    for tty in Path('/sys/class/tty').glob('ttyACM*'):
        for parent in (tty/'device').resolve().parents:
            try:
                identity=((parent/'idVendor').read_text().strip(),
                          (parent/'idProduct').read_text().strip(),
                          (parent/'serial').read_text().strip())
            except OSError:continue
            if identity==('1d6b','0104','A03XNUConsole01'):found.append('/dev/'+tty.name)
            break
    if len(found)>1:raise RuntimeError('Multiple matching A03 console devices')
    return found[0] if found else None

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=Path('shim/a03/out/usb-console-'+time.strftime('%Y%m%d-%H%M%S')+'.log'))
    ap.add_argument('--wait',type=float,default=120,help='seconds to wait for enumeration')
    ap.add_argument('--duration',type=float,default=300,help='maximum capture seconds')
    a=ap.parse_args();deadline=time.monotonic()+a.wait;dev=None
    while dev is None:
        dev=find()
        if dev:break
        if time.monotonic()>=deadline:raise RuntimeError('A03 XNU CDC console did not enumerate')
        time.sleep(.25)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    print('Capturing '+dev+' to '+str(a.output),file=sys.stderr)
    with a.output.open('xb') as log:
        fd=os.open(dev,os.O_RDONLY|os.O_NOCTTY|os.O_NONBLOCK)
        try:
            attr=termios.tcgetattr(fd);attr[0]=attr[1]=attr[3]=0
            attr[2]=termios.CS8|termios.CREAD|termios.CLOCAL
            attr[4]=attr[5]=termios.B115200
            attr[6][termios.VMIN]=1;attr[6][termios.VTIME]=0
            termios.tcsetattr(fd,termios.TCSANOW,attr)
            deadline=time.monotonic()+a.duration
            while time.monotonic()<deadline:
                ready,_,_=select.select([fd],[],[],min(1,max(0,deadline-time.monotonic())))
                if not ready:continue
                b=os.read(fd,65536)
                if not b:break
                log.write(b);log.flush();sys.stdout.buffer.write(b);sys.stdout.buffer.flush()
        finally:os.close(fd)

if __name__=='__main__':
    try:main()
    except (OSError,RuntimeError) as e:sys.exit(str(e))
