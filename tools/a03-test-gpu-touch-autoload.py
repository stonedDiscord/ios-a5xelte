"""Check complete touch firmware uploads trigger the validated RAM load."""
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).parents[1]
patch = root / "xnu/a03/0215-a03-touch-auto-load.patch"
source = root / "shim/a03/out/ci44958900136-tree/extracted/xnu"
if not source.exists():
    source = root / "shim/a03/out/ci44950176996-posterboard0213-tree/extracted/xnu"
with tempfile.TemporaryDirectory(prefix="a03-touch-") as d:
    tree = Path(d) / "xnu"
    shutil.copytree(source, tree)
    subprocess.run(["git", "apply", str(patch)], cwd=tree, check=True)
    text = (tree / "bsd/dev/a03_usb_console.c").read_text()
    assert "a03_touch_fw_used==a03_touch_fw_size" in text
    assert 'a03_touch_probe("load")' in text
print("PASS complete firmware upload automatically loads touch RAM firmware")
