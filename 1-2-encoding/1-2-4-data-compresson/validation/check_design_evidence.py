"""Verify the numerical evidence in this design, not classroom UI behavior.

Run: python validation/check_design_evidence.py
Requires Pillow for the real PNG/JPEG comparison. No network or audio encoder.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import zlib
from itertools import groupby
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version, features


ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"


def rle_encode(data: bytes) -> bytes:
    encoded = bytearray()
    for value, group in groupby(data):
        count = sum(1 for _ in group)
        while count:
            chunk = min(count, 255)
            encoded.extend((value, chunk))
            count -= chunk
    return bytes(encoded)


def rle_decode(data: bytes) -> bytes:
    if len(data) % 2:
        raise ValueError("RLE requires complete value/count pairs")
    if any(count == 0 for count in data[1::2]):
        raise ValueError("RLE counts must be 1..255")
    return b"".join(bytes((value,)) * count
                    for value, count in zip(data[::2], data[1::2]))


def pack_bits(bits: str) -> bytes:
    assert bits and set(bits) <= {"0", "1"}
    padded = bits + "0" * (-len(bits) % 8)
    return bytes(int(padded[i:i + 8], 2) for i in range(0, len(padded), 8))


def unpack_bits(payload: bytes, valid_bits: int) -> str:
    assert len(payload) == math.ceil(valid_bits / 8)
    all_bits = "".join(f"{value:08b}" for value in payload)
    assert set(all_bits[valid_bits:]) <= {"0"}
    return all_bits[:valid_bits]


def predictive_bits(values: list[int]) -> str:
    assert values and all(0 <= value <= 255 for value in values)
    codes = {-1: "00", 0: "01", 1: "10"}
    deltas = [b - a for a, b in zip(values, values[1:])]
    if any(delta not in codes for delta in deltas):
        raise ValueError("The classroom code supports only -1, 0, +1")
    return f"{values[0]:08b}" + "".join(codes[delta] for delta in deltas)


def decode_predictive(bits: str) -> list[int]:
    assert len(bits) >= 8 and (len(bits) - 8) % 2 == 0
    codes = {"00": -1, "01": 0, "10": 1}
    decoded = [int(bits[:8], 2)]
    for offset in range(8, len(bits), 2):
        code = bits[offset:offset + 2]
        if code not in codes:
            raise ValueError("Reserved delta code 11")
        value = decoded[-1] + codes[code]
        if not 0 <= value <= 255:
            raise ValueError("Decoded gray value outside 0..255")
        decoded.append(value)
    return decoded


def test_image() -> Image.Image:
    """Exact synthetic test chart; no photographs or generated evidence."""
    image = Image.new("RGB", (384, 216), "white")
    for x in range(384):
        gray = round(x * 255 / 383)
        for y in range(140):
            image.putpixel((x, y), (gray, gray, gray))
    draw = ImageDraw.Draw(image)
    for x in range(8, 245, 4):
        draw.line((x, 148, x, 207), fill=(20, 30, 40), width=1)
    font = ImageFont.load_default(size=18)
    draw.text((260, 151), "CODE 8B3", fill=(15, 15, 15), font=font)
    draw.text((260, 176), "012345", fill=(20, 80, 140), font=font)
    draw.rectangle((260, 200, 355, 201), fill=(30, 30, 30))
    return image


def file_record(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": str(path.relative_to(ROOT.parent)), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def main() -> None:
    FIXTURES.mkdir(exist_ok=True)
    colors = bytes([1] * 8 + [2] * 5 + [3] * 3)
    alternating = bytes([1, 2] * 8)
    encoded = rle_encode(colors)
    assert list(encoded) == [1, 8, 2, 5, 3, 3]
    assert len(colors) == 16 and len(encoded) == 6
    assert len(rle_encode(alternating)) == 32
    assert rle_decode(encoded) == colors
    assert rle_decode(rle_encode(alternating)) == alternating
    private_cards = [bytes([3] * 4 + [1] * 7 + [2] * 5),
                     bytes([2] * 6 + [3] * 4 + [1] * 6)]
    for card in private_cards:
        assert len(card) == 16 and len(rle_encode(card)) == 6
        assert card != colors and rle_decode(rle_encode(card)) == card
    assert rle_decode(rle_encode(bytes([1] * 256))) == bytes([1] * 256)
    assert len(rle_encode(bytes([1] * 256))) == 4
    assert rle_decode(rle_encode(b"")) == b""
    faulty = colors[:8] + bytes([3]) + colors[9:]
    first_difference = next(i for i, (a, b) in enumerate(zip(colors, faulty)) if a != b)
    assert len(faulty) == len(colors) and first_difference == 8
    blackwhite_lengths = [len(rle_encode(bytes(map(int, s))))
                          for s in ["0000000011111111", "0101010101010101"]]
    assert blackwhite_lengths == [4, 32]

    original = colors * 256
    compressed = zlib.compress(original)
    restored = zlib.decompress(compressed)
    assert len(original) == 4096 and restored == original
    raw_path = FIXTURES / "opening-colors.raw"
    compressed_path = FIXTURES / "opening-colors.zlib"
    raw_path.write_bytes(original)
    compressed_path.write_bytes(compressed)
    palette = {1: (210, 35, 45), 2: (20, 135, 90), 3: (35, 85, 195)}
    for name, data in [("opening-original.png", original),
                       ("opening-restored.png", restored)]:
        image = Image.new("RGB", (64, 64))
        image.putdata([palette[value] for value in data])
        image.save(FIXTURES / name)

    gray = [120, 121, 122, 121, 120, 120, 121, 122]
    deltas = [b - a for a, b in zip(gray, gray[1:])]
    bits = predictive_bits(gray)
    packed = pack_bits(bits)
    assert len(bits) == 22 and len(packed) == 3
    assert decode_predictive(unpack_bits(packed, len(bits))) == gray
    try:
        predictive_bits([120, 150])
    except ValueError:
        rejects_large_delta = True
    else:
        raise AssertionError("Large delta silently accepted")

    # Integer nearest-multiple model, tie upward, saturate the last level.
    levels = [min(63, (value + 2) // 4) for value in gray]
    lossy_bits = "".join(f"{level:06b}" for level in levels)
    lossy_payload = pack_bits(lossy_bits)
    decoded_bits = unpack_bits(lossy_payload, 48)
    decoded_gray = [int(decoded_bits[i:i + 6], 2) * 4
                    for i in range(0, 48, 6)]
    assert decoded_gray == [120, 120, 124, 120, 120, 120, 120, 124]
    assert len(lossy_payload) == 6 and decoded_gray != gray
    assert min(63, (120 + 2) // 4) == min(63, (121 + 2) // 4)
    assert min(63, (255 + 2) // 4) * 4 == 252

    source = test_image()
    source.save(FIXTURES / "test-source.png")
    source_bytes = source.tobytes()
    with Image.open(FIXTURES / "test-source.png") as png:
        png_equal = png.convert("RGB").tobytes() == source_bytes
    assert png_equal
    jpeg_records = []
    crop_box = (260, 150, 356, 198)
    source.crop(crop_box).resize((768, 384), Image.Resampling.NEAREST).save(
        FIXTURES / "crop-source.png")
    for quality in (80, 20):
        path = FIXTURES / f"test-quality{quality}.jpg"
        source.save(path, quality=quality, subsampling=0)
        with Image.open(path) as saved:
            decoded = saved.convert("RGB")
        decoded_bytes = decoded.tobytes()
        assert len(decoded_bytes) == len(source_bytes)
        changed_pixels = sum(source_bytes[i:i + 3] != decoded_bytes[i:i + 3]
                             for i in range(0, len(source_bytes), 3))
        assert decoded.size == source.size and changed_pixels > 0
        assert decoded.tobytes() != source_bytes
        crop = decoded.crop(crop_box)
        assert crop.size == (96, 48)
        crop.resize((768, 384), Image.Resampling.NEAREST).save(
            FIXTURES / f"crop-quality{quality}.png")
        jpeg_records.append({**file_record(path), "quality": quality,
                             "subsampling": 0, "size": list(decoded.size),
                             "changed_pixels": changed_pixels, "pixel_equal": False})

    # Independently evaluate the curriculum's arithmetic and decision predicates.
    source_cases = [(80, True), (50, False)]
    photo_cases = [(110, True), (70, True)]
    source_eligible = [size <= 100 and faithful for size, faithful in source_cases]
    photo_eligible = [size <= 100 and usable for size, usable in photo_cases]
    assert source_eligible == [True, False] and photo_eligible == [False, True]
    assert (60 >= 60) is True and (60 > 60) is False
    assert 120 / 10 == 12 and 80 / 10 == 8
    assert 44100 * 8 * 16 // 8 == 705600
    assert sum([3, 6, 4, 4, 5, 5, 5, 4, 4, 5]) == 45
    assert sum([30, 90, 60, 30, 30, 40, 20]) == 300
    assert sum([5, 10, 10, 10, 7, 3]) == 45

    result = {
        "status": "passed",
        "scope": "design numerical and codec prototypes; not notebook, WPS or classroom acceptance",
        "environment": {"python": platform.python_version(), "pillow": pillow_version,
                        "zlib": zlib.ZLIB_RUNTIME_VERSION, "jpeg": features.version_codec("jpg")},
        "D1": {"input": file_record(raw_path), "compressed": file_record(compressed_path),
               "restored_bytes": len(restored), "bytes_equal": restored == original},
        "D2": {"raw_bytes": len(colors), "rle_bytes": len(encoded),
               "pairs": list(zip(encoded[::2], encoded[1::2])),
               "reduction_percent": (1 - len(encoded) / len(colors)) * 100,
               "alternating_raw_bytes": 16, "alternating_rle_bytes": 32,
               "roundtrip_equal": True, "count256_encoded_bytes": 4,
               "private_activity_cards": [list(card) for card in private_cards],
               "homework_rle_bytes": blackwhite_lengths},
        "D3": {"source": gray, "deltas": deltas, "valid_bits": len(bits),
               "packed_bytes": len(packed), "padding_bits": 2,
               "roundtrip_equal": True, "rejects_large_delta": rejects_large_delta},
        "D4": {"levels": levels, "valid_bits": len(lossy_bits),
               "packed_bytes": len(lossy_payload), "reconstructed": decoded_gray,
               "collision_inputs": [120, 121], "collision_output": 120},
        "D5": {"source": file_record(FIXTURES / "test-source.png"),
               "size": list(source.size), "uncompressed_rgb_bytes": len(source_bytes),
               "png_pixel_equal": png_equal, "jpeg": jpeg_records,
               "crop_xywh": [260, 150, 96, 48], "fixture_type": "synthetic exact test chart"},
        "D6": {"status": "specification_only", "pcm_payload_bytes": 705600,
               "mp3_encode_or_listen_test": False},
        "Q10": {"given_scenario_not_measured_files": True,
                "source_program_eligible_A_B": source_eligible,
                "photo_eligible_A_B": photo_eligible,
                "transfer_payload_seconds_original_compressed": [12, 8]},
        "Q3": {"faulty_length_equal": True, "first_difference_one_based": first_difference + 1},
        "time_budget_minutes": {"core": 45, "optional_second_period": 45},
        "design_sha256": hashlib.sha256((ROOT.parent / "course-design.qmd").read_bytes()).hexdigest(),
    }
    (ROOT / "design-evidence.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "D1_bytes": [len(original), len(compressed)],
                      "D3_bits_bytes": [len(bits), len(packed)],
                      "D4_bits_bytes": [len(lossy_bits), len(lossy_payload)],
                      "D5_png_bytes": result["D5"]["source"]["bytes"],
                      "D5_jpeg": [{"quality": r["quality"], "bytes": r["bytes"],
                                    "changed_pixels": r["changed_pixels"]} for r in jpeg_records]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
