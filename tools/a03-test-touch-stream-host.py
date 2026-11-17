#!/usr/bin/env python3
"""Verify host transaction correlation and stop-after-lost-start behavior."""
import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('stream', ROOT/'tools/a03-usb-touch-stream.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class Log(io.BytesIO):
    pass

class Probe:
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def send(self, value):
        self.sent = value
        # An unrelated earlier worker END must not complete this transaction.
        data = (b'A03 PROBE 2 END\nA03 PROBE 9 BEGIN touch streamstatus\n'
                b'A03 TOUCH streaming=0 slices=0 events=0\nA03 PROBE 9 END\n')
        pos = self.log.tell(); self.log.write(data); self.log.seek(pos)

p = Probe(); p.log = Log()
assert 'streaming=0' in m.command(p, p.log, 'streamstatus')
assert p.sent == 'touch streamstatus'

with tempfile.NamedTemporaryFile() as log:
    calls=[]
    def command(probe, logfile, value, timeout=20):
        calls.append(value)
        if value == 'streamstatus': return 'A03 TOUCH streaming=0 slices=0 events=0\n'
        if value == 'startcontacts': raise RuntimeError('simulated lost start ACK')
        if value == 'stop': return 'A03 TOUCH stream stopped slices=1 events=0; released\n'
        raise AssertionError(value)
    with patch.object(m, 'Probe', Probe), patch.object(m, 'command', command), patch.object(sys, 'argv', ['stream', '--log', log.name]), contextlib.redirect_stdout(io.StringIO()):
        try: m.main()
        except RuntimeError as e: assert 'lost start ACK' in str(e)
        else: raise AssertionError('lost ACK must fail visibly')
    assert calls == ['streamstatus','startcontacts','stop'], calls
    calls.clear()
    def active(probe, logfile, value, timeout=20):
        calls.append(value)
        return 'A03 TOUCH streaming=1 slices=100 events=2\n'
    with patch.object(m, 'Probe', Probe), patch.object(m, 'command', active), patch.object(sys, 'argv', ['stream', '--log', log.name]):
        try: m.main()
        except RuntimeError as e: assert 'existing stream active' in str(e)
        else: raise AssertionError('existing stream must be preserved')
    assert calls == ['streamstatus'], calls
print('PASS host stream: exact transaction END, cleanup after lost start ACK, preserve existing stream')
