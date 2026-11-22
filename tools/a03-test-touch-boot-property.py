"""Validate private touch firmware can be embedded in the A03 boot ADT."""
from pathlib import Path
import hashlib
import sys
import tempfile
sys.path.insert(0, str(Path(__file__).parents[1] / "tools"))
import adt
import mkpayload

root = Path(__file__).parents[1]
firmware = root / "research/a03-touch-firmware/CPT_Jadard_firmware.bin"
assert len(firmware.read_bytes()) == 79104
assert hashlib.sha256(firmware.read_bytes()).hexdigest() == (
    "8ba14e32cdeacd6763a9700fd5340f9c91763afc2965231148f72f9c1ceea82d")
with tempfile.TemporaryDirectory(prefix="a03-touch-payload-"):
    payload, _ = mkpayload.build(
        "/tmp/a03-ci449589-download/kernel.development.sweet",
        str(root / "shim/a03/out/0094-a75-input.adt"),
        "debug=0x14e serial=3",
        a03_touch_firmware=str(firmware))
    assert len(payload) > 16_700_000
print("PASS private firmware validation and boot-payload embedding")
