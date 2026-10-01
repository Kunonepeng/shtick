"""Encode the user-supplied JPEG's decoded RGB once per setting.

This is measured compression evidence, not a restoration of the camera/master
image. Keep the supplied file unchanged; all comparisons start with its RGB.
"""
from pathlib import Path
import hashlib
import json
import sys
from PIL import Image, features

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "demos"))
from compression_lab import photo_evidence

def main():
    original = ROOT / "assets/0000136308_OG.JPG"
    digest = hashlib.sha256(original.read_bytes()).hexdigest()
    folder = ROOT / "assets/evidence"
    with Image.open(original) as im:
        source = im.convert("RGB")
    source.save(folder / "painting-source.png")
    for quality in (80, 20):
        source.save(folder / f"painting-quality{quality}.jpg", quality=quality, subsampling=0)
    # Same facial-detail coordinates, nearest-neighbour x4; no enhancement.
    crop = (368, 310, 560, 438)
    for name, output in [("painting-source.png", "painting-crop-source.png"),
                         ("painting-quality80.jpg", "painting-crop-quality80.png"),
                         ("painting-quality20.jpg", "painting-crop-quality20.png")]:
        with Image.open(folder / name) as im:
            im.convert("RGB").crop(crop).resize((768, 512), Image.Resampling.NEAREST).save(folder / output)
    assert hashlib.sha256(original.read_bytes()).hexdigest() == digest
    report = {"input_file": "assets/0000136308_OG.JPG", "input_sha256": digest,
              "input_bytes": original.stat().st_size, "baseline": "supplied JPEG decoded to RGB",
              "quality": [80, 20], "subsampling": 0, "crop_xywh": [368, 310, 192, 128],
              "crop_magnification": 4, "jpeg_library": features.version_codec("jpg"),
              "evidence": photo_evidence()}
    (ROOT / "sources/photo-evidence.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
