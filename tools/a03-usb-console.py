#!/usr/bin/env python3
"""Capture the A03 XNU CDC ACM console to stdout and a private local log.
Only opens a tty with exact diagnostic serial + VID/PID. Optional monitor
commands are sent only when explicitly requested; no partition access.
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
    ap.add_argument('--command',action='append',default=[],help='monitor command; repeat for multiple commands')
    ap.add_argument('--interactive',action='store_true',help='forward terminal input to USB monitor')
    a=ap.parse_args();deadline=time.monotonic()+a.wait;dev=None
    while dev is None:
        dev=find()
        if dev:break
        if time.monotonic()>=deadline:raise RuntimeError('A03 XNU CDC console did not enumerate')
        time.sleep(.25)
    # A newly enumerated tty can need the host ACL fix before it is openable.
    # Keep waiting for this exact identity within the original wait budget.
    flags=(os.O_RDWR if a.command or a.interactive else os.O_RDONLY)|os.O_NOCTTY|os.O_NONBLOCK
    permission_reported=False
    while True:
        try:
            fd=os.open(dev,flags)
            break
        except PermissionError:
            if time.monotonic()>=deadline:raise
            if not permission_reported:
                print('Waiting for access to '+dev+'; grant this user a tty ACL',file=sys.stderr)
                permission_reported=True
            time.sleep(.25)
            dev=find()
            if dev is None:raise RuntimeError('A03 console disconnected while waiting for access')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    print('Capturing '+dev+' to '+str(a.output),file=sys.stderr)
    try:
        log=a.output.open('xb')
    except OSError:
        os.close(fd)
        raise
    with log:
        try:
            attr=termios.tcgetattr(fd);attr[0]=attr[1]=attr[3]=0
            attr[2]=termios.CS8|termios.CREAD|termios.CLOCAL
            attr[4]=attr[5]=termios.B115200
            attr[6][termios.VMIN]=1;attr[6][termios.VTIME]=0
            termios.tcsetattr(fd,termios.TCSANOW,attr)
            for command in a.command:
                if len(command)>126 or any(ord(c)<32 or ord(c)>126 for c in command):
                    raise RuntimeError('Commands must contain at most126 printable ASCII characters')
                payload=(command+'\n').encode('ascii')
                offset=0
                while offset<len(payload):
                    _,writable,_=select.select([],[fd],[],2)
                    if not writable:raise RuntimeError('USB command write timeout')
                    offset+=os.write(fd,payload[offset:])
                # The monitor holds one pending line; allow it to consume each.
                time.sleep(.1)
            deadline=time.monotonic()+a.duration
            while time.monotonic()<deadline:
                inputs=[fd]+([sys.stdin] if a.interactive else [])
                ready,_,_=select.select(inputs,[],[],min(1,max(0,deadline-time.monotonic())))
                if a.interactive and sys.stdin in ready:
                    line=sys.stdin.readline()
                    if not line:a.interactive=False
                    else:
                        data=line.encode('ascii',errors='replace');offset=0
                        while offset<len(data):
                            _,writable,_=select.select([],[fd],[],2)
                            if not writable:raise RuntimeError('USB command write timeout')
                            offset+=os.write(fd,data[offset:])
                    ready=[item for item in ready if item is not sys.stdin]
                if not ready:continue
                b=os.read(fd,65536)
                if not b:break
                log.write(b);log.flush();sys.stdout.buffer.write(b);sys.stdout.buffer.flush()
        finally:os.close(fd)

if __name__=='__main__':
    try:main()
    except (OSError,RuntimeError) as e:sys.exit(str(e))
