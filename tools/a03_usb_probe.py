"""Private EP0 command transport for the opt-in A03 live probe worker.

Uses libusb without claiming/detaching CDC interfaces. Results remain on the
ordinary console stream. A successful transfer means queued, not completed.
"""
import ctypes as C
import ctypes.util


def validate(command):
    data = command.encode('ascii')
    if not 1 <= len(data) <= 127 or any(c < 32 or c >= 127 for c in data):
        raise ValueError('probe command requires 1..127 printable ASCII bytes')
    return data


class Descriptor(C.Structure):
    _fields_ = [('length', C.c_uint8), ('type', C.c_uint8),
                ('usb', C.c_uint16), ('device_class', C.c_uint8),
                ('subclass', C.c_uint8), ('protocol', C.c_uint8),
                ('packet', C.c_uint8), ('vendor', C.c_uint16),
                ('product', C.c_uint16), ('version', C.c_uint16),
                ('manufacturer', C.c_uint8), ('name', C.c_uint8),
                ('serial', C.c_uint8), ('configurations', C.c_uint8)]


class Probe:
    def __init__(self):
        path = ctypes.util.find_library('usb-1.0')
        if not path:
            raise RuntimeError('libusb-1.0 is required for EP0 probes')
        self.lib = lib = C.CDLL(path)
        self.context = C.c_void_p()
        self.handle = C.c_void_p()
        signatures = {
            'init': ([C.POINTER(C.c_void_p)], C.c_int),
            'exit': ([C.c_void_p], None),
            'get_device_list': ([C.c_void_p, C.POINTER(C.POINTER(C.c_void_p))], C.c_ssize_t),
            'free_device_list': ([C.POINTER(C.c_void_p), C.c_int], None),
            'get_device_descriptor': ([C.c_void_p, C.POINTER(Descriptor)], C.c_int),
            'open': ([C.c_void_p, C.POINTER(C.c_void_p)], C.c_int),
            'close': ([C.c_void_p], None),
            'get_string_descriptor_ascii': ([C.c_void_p, C.c_uint8, C.c_void_p, C.c_int], C.c_int),
            'control_transfer': ([C.c_void_p, C.c_uint8, C.c_uint8, C.c_uint16,
                                  C.c_uint16, C.c_void_p, C.c_uint16, C.c_uint], C.c_int),
        }
        for name, (args, result) in signatures.items():
            fn = getattr(lib, 'libusb_' + name)
            fn.argtypes, fn.restype = args, result
        if lib.libusb_init(C.byref(self.context)):
            raise RuntimeError('libusb initialization failed')
        devices = C.POINTER(C.c_void_p)()
        count = lib.libusb_get_device_list(self.context, C.byref(devices))
        try:
            if count < 0:
                raise RuntimeError('USB device enumeration failed')
            for i in range(count):
                desc = Descriptor()
                if lib.libusb_get_device_descriptor(devices[i], C.byref(desc)):
                    continue
                if (desc.vendor, desc.product) != (0x1d6b, 0x0104):
                    continue
                handle = C.c_void_p()
                error = lib.libusb_open(devices[i], C.byref(handle))
                if error:
                    raise RuntimeError('cannot open A03 USB device: libusb error ' + str(error))
                serial = C.create_string_buffer(128)
                n = lib.libusb_get_string_descriptor_ascii(handle, desc.serial, serial, 128)
                if n < 0 or serial.raw[:n] != b'A03XNUConsole01':
                    lib.libusb_close(handle)
                    continue
                if self.handle.value:
                    lib.libusb_close(handle)
                    raise RuntimeError('multiple matching A03 consoles')
                self.handle = handle
            if not self.handle.value:
                raise RuntimeError('A03 XNU console not connected')
        except BaseException:
            if count >= 0:
                lib.libusb_free_device_list(devices, 1)
                count = -1
            self.close()
            raise
        finally:
            if count >= 0:
                lib.libusb_free_device_list(devices, 1)

    def send(self, command):
        data = validate(command)
        buf = C.create_string_buffer(data)
        n = self.lib.libusb_control_transfer(self.handle, 0x40, 0xa3, 0, 0,
                                             buf, len(data), 2000)
        if n != len(data):
            raise RuntimeError('probe transfer failed (' + str(n) +
                               '); kernel needs 0135 and a03_probe=1; queue may be full')

    def close(self):
        if self.handle.value:
            self.lib.libusb_close(self.handle)
            self.handle = C.c_void_p()
        if self.context.value:
            self.lib.libusb_exit(self.context)
            self.context = C.c_void_p()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
