from __future__ import annotations

from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = ROOT / "sources" / "pics-of-deck-image-encoding.zip"
OUT_DIR = ROOT / "assets" / "original-screenshots"

VALID_NUMBERS = list(range(1, 12)) + list(range(13, 28))


def main() -> None:
    if not ZIP_PATH.exists():
        raise FileNotFoundError(f"Source zip not found: {ZIP_PATH}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(ZIP_PATH) as zf:
        members = {Path(name).name: name for name in zf.namelist() if not name.startswith("__MACOSX/")}

        missing = []
        for n in VALID_NUMBERS:
            filename = f"Snip20260929_{n}.png"
            member = members.get(filename)
            if member is None:
                missing.append(filename)
                continue

            target = OUT_DIR / filename
            with zf.open(member) as src, target.open("wb") as dst:
                shutil.copyfileobj(src, dst)

    if missing:
        raise RuntimeError("Expected screenshots missing from source zip: " + ", ".join(missing))

    unexpected = sorted(
        p.name for p in OUT_DIR.glob("Snip20260929_*.png")
        if p.name not in {f"Snip20260929_{n}.png" for n in VALID_NUMBERS}
    )
    for name in unexpected:
        (OUT_DIR / name).unlink()

    print(f"Prepared {len(VALID_NUMBERS)} screenshots in {OUT_DIR}")
    print("Note: source numbering intentionally has no Snip20260929_12.png")


if __name__ == "__main__":
    main()
