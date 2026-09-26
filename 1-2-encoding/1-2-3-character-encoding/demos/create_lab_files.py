"""Generate controlled text files for the WinHex character-encoding lab."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

TEXT = "A中B国C文"
(ASSETS / "gb2312-lab.txt").write_bytes(TEXT.encode("gb2312"))
(ASSETS / "utf8-lab.txt").write_bytes(TEXT.encode("utf-8"))

print("generated:")
print(ASSETS / "gb2312-lab.txt")
print(ASSETS / "utf8-lab.txt")
