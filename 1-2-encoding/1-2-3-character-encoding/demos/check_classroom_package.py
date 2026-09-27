"""Pre-class verification for the v6-2 classroom package."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

EXPECTED = {
    "gb2312-lab.txt": "41 D6 D0 42 B9 FA 43 CE C4",
    "utf8-lab.txt": "41 E4 B8 AD 42 E5 9B BD 43 E6 96 87",
}

required = [
    ROOT / "1-2-3-character-encoding-v6-2.pptx",
    ROOT / "demo-lab-teacher.ipynb",
    ROOT / "demo-lab-student.ipynb",
    ROOT / "teacher-guide.qmd",
    ROOT / "worksheets" / "character-encoding-exit-ticket.pdf",
]

failures = []
print("Python:", sys.version.split()[0])

for path in required:
    if path.exists():
        print("OK  ", path.relative_to(ROOT))
    else:
        print("MISS", path.relative_to(ROOT))
        failures.append(f"missing {path.name}")

for name, expected in EXPECTED.items():
    path = ASSETS / name
    if not path.exists():
        print("MISS", path.relative_to(ROOT))
        failures.append(f"missing {name}")
        continue
    actual = path.read_bytes().hex(" ").upper()
    if actual == expected:
        print("OK  ", name, actual)
    else:
        print("FAIL", name, actual)
        failures.append(f"wrong bytes in {name}")

checks = [
    ("ASCII A", "A".encode("ascii").hex().upper(), "41"),
    ("GB2312 中", "中".encode("gb2312").hex().upper(), "D6D0"),
    ("UTF-8 你", "你".encode("utf-8").hex().upper(), "E4BDA0"),
    ("UTF-16BE 你", "你".encode("utf-16-be").hex().upper(), "4F60"),
    ("UTF-32BE 你", "你".encode("utf-32-be").hex().upper(), "00004F60"),
    ("UTF-16BE U+1F600", chr(0x1F600).encode("utf-16-be").hex().upper(), "D83DDE00"),
]
for label, actual, expected in checks:
    if actual == expected:
        print("OK  ", label, actual)
    else:
        print("FAIL", label, actual, "expected", expected)
        failures.append(label)

if failures:
    print("\nCHECKS FAILED:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("\nALL CHECKS PASSED")
