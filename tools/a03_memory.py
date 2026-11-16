"""Bounded A03 memory profiles; expanded images require a private live DTB."""
import subprocess
import struct
PHYS_BASE = 0x102000000
MEMORY_MIB = (256, 1024)

def memory_size(mib):
    if mib not in MEMORY_MIB:
        raise ValueError('A03 RAM profile must be 256 or 1024 MiB')
    return mib << 20

def validate_live_fdt(path, size):
    """Check banks, every reserved-memory child and the FDT reserve map."""
    if size not in [memory_size(m) for m in MEMORY_MIB]:
        raise ValueError('unsupported RAM profile')
    raw=path.read_bytes()
    if len(raw)<40:raise ValueError('truncated FDT')
    magic,total,_,_,ro,version,last,_,_,_=struct.unpack_from('>10I',raw)
    if magic!=0xd00dfeed or total>len(raw) or version<17 or last>17 or ro<40 or ro+16>total:
        raise ValueError('invalid FDT header')
    def get(node,key,kind='x'):
        return subprocess.check_output(['fdtget','-t',kind,str(path),node,key],text=True).strip()
    def children(node):
        return subprocess.check_output(['fdtget','-l',str(path),node],text=True).splitlines()
    if 'ums9230' not in get('/','compatible','s'):
        raise ValueError('not an ums9230 live tree')
    for node in ['/','/reserved-memory']:
        if get(node,'#address-cells')!='2' or get(node,'#size-cells')!='2':
            raise ValueError('expected 64-bit A03 cells')
    if get('/reserved-memory','ranges'):
        raise ValueError('unsupported memory translation')
    def ranges(node):
        cells=[int(x,16) for x in get(node,'reg').split()]
        if not cells or len(cells)%4:raise ValueError('invalid reg')
        return [((cells[i]<<32)|cells[i+1],(cells[i+2]<<32)|cells[i+3]) for i in range(0,len(cells),4)]
    banks=[]
    for child in children('/'):
        if child.startswith('memory@'):
            if get('/'+child,'device_type','s')!='memory':raise ValueError('invalid memory node')
            banks.extend(ranges('/'+child))
    reserved=[]
    for child in children('/reserved-memory'):
        reserved.extend(ranges('/reserved-memory/'+child))
    for pos in range(ro,total-15,16):
        base,n=struct.unpack_from('>QQ',raw,pos)
        if not base and not n:break
        reserved.append((base,n))
    else:raise ValueError('unterminated reserve map')
    begin,finish=PHYS_BASE,PHYS_BASE+size
    if not any(base<=begin and finish<=base+n for base,n in banks):
        raise ValueError('managed window is outside live RAM')
    if any(n and begin<base+n and base<finish for base,n in reserved):
        raise ValueError('managed window overlaps reserved memory')
    return {'base':hex(begin),'end':hex(finish),'memory_mib':size>>20,
            'banks':[(hex(b),hex(n)) for b,n in banks],'reservations_checked':len(reserved)}
