#!/usr/bin/env python3
"""Exercise the real checker receiver using actual loopback UDP datagrams."""
import ast
from pathlib import Path
import socket
import time

source = (Path(__file__).parent/'dreamlte-usb-check.py').read_text()
tree = ast.parse(source)
function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'receive_console')
namespace = {'socket': socket, 'time': time}
exec(compile(ast.Module(body=[function], type_ignores=[]), '<actual receiver>', 'exec'), namespace)
receive = namespace['receive_console']

def trial(payloads, expected='127.0.0.1'):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as receiver, socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        receiver.bind(('127.0.0.1', 0))
        for payload in payloads:
            sender.sendto(payload, receiver.getsockname())
        return receive(receiver, 0.04, expected)

assert trial([b'DREAM', b'LTE USB: resource ready\n']) == b'DREAMLTE USB: resource ready\n'
assert trial([b'SWEET USB: connected\n']) == b'SWEET USB: connected\n'
assert trial([b'Darwin Kernel Version test\n']).startswith(b'Darwin')
for payloads, peer, expected in [([], '127.0.0.1', 'no UDP'), ([b''], '127.0.0.1', 'no UDP'),
                                ([b'unrelated traffic'], '127.0.0.1', 'no recognized'),
                                ([b'DREAMLTE USB: ready'], '127.0.0.2', 'no UDP')]:
    try:
        trial(payloads, peer)
    except RuntimeError as error:
        assert expected in str(error), error
    else:
        raise AssertionError('invalid capture accepted')
assert "receive_console(listener, a.console_seconds, '192.168.7.2')" in source
assert "listener.bind(('192.168.7.1', 5140))" in source
assert source.index('listener.bind(') < source.index("subprocess.run(['ping'")
print('PASS: actual UDP receiver accepts split XNU markers; rejects silence, empty/foreign datagrams and unrelated text; bounded timeout')
