"""Check the bounded GPU cache-clean retry stays before quarantine."""
from pathlib import Path
p = Path(__file__).parents[1] / "xnu/a03/0214-a03-gpu-clean-retry.patch"
s = p.read_text()
assert "for(unsigned attempt=0;attempt<2&&!clean;attempt++)" in s
assert "if(!clean&&attempt==0)" in s
assert s.index("a03_gpu_write(0x30,8);") < s.index("retire_stage=5;")
assert "idempotent request" in s
assert "@@ -539,9 +539,17 @@" in s
print("PASS bounded cache-clean retry before GPU quarantine")
