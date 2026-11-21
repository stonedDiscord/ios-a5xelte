"""Validate the GPU clean-completion patch is profiled and applies."""
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).parents[1]
patch = root / "xnu/a03/0214-a03-gpu-clean-completion-window.patch"
profile = (root / "tools/a03-build-profile.py").read_text()
assert patch.name in profile
assert "@@ -539,7 +539,9 @@" in patch.read_text()
with tempfile.TemporaryDirectory(prefix="a03-clean-") as d:
    tree = Path(d) / "xnu"
    source = root / "shim/a03/out/ci44950176996-posterboard0213-tree/extracted/xnu"
    shutil.copytree(source, tree)
    subprocess.run(["git", "apply", str(patch)], cwd=tree, check=True)
    text = (tree / "bsd/dev/a03_gpu.c").read_text()
    assert "for(unsigned i=0;i<4000;i++)" in text
print("PASS profiled GPU clean-completion window applies to XNU tree")
