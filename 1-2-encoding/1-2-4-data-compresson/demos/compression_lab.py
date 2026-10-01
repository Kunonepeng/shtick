"""Shared, deterministic classroom computations. Python 3.10+ and Pillow.

These are explicit teaching models; predictive/quantization models are not JPEG.
No network, widgets, shell commands or audio codecs are required.
"""
from pathlib import Path
from itertools import groupby
import hashlib
import json
import zlib
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
COLORS = bytes([1] * 8 + [2] * 5 + [3] * 3)
ALTERNATING = bytes([1, 2] * 8)
GRAY = [120, 121, 122, 121, 120, 120, 121, 122]
NAMES = {1: "红", 2: "绿", 3: "蓝"}

def rle_encode(data):
    result = bytearray()
    for value, group in groupby(bytes(data)):
        count = sum(1 for _ in group)
        while count:
            n = min(count, 255)
            result.extend((value, n))
            count -= n
    return bytes(result)

def rle_decode(encoded):
    if len(encoded) % 2 or any(n == 0 for n in encoded[1::2]):
        raise ValueError("需要完整的编号／次数对，次数为1–255")
    return b"".join(bytes([v]) * n for v, n in zip(encoded[::2], encoded[1::2]))

def named_runs(encoded):
    return "  ".join(f"{NAMES.get(v, v)}{n}" for v, n in zip(encoded[::2], encoded[1::2]))

def opening(reveal=False):
    original = COLORS * 256
    compressed = zlib.compress(original)
    result = {"输入数据B": len(original), "编码数据B": len(compressed)}
    if reveal:
        restored = zlib.decompress(compressed)
        result.update({"解压数据B": len(restored), "解压结果与原输入逐byte一致": restored == original})
    return result

def pack(bits):
    if not bits or set(bits) - {"0", "1"}:
        raise ValueError("需要非空二进制串")
    padded = bits + "0" * (-len(bits) % 8)
    return bytes(int(padded[i:i+8], 2) for i in range(0, len(padded), 8))

def predictive(values):
    values = list(values)
    if not values or any(not 0 <= v <= 255 for v in values):
        raise ValueError("需要0–255的灰度值")
    deltas = [b-a for a, b in zip(values, values[1:])]
    codes = {-1: "00", 0: "01", 1: "10"}
    if any(d not in codes for d in deltas):
        raise ValueError("本课2bit码表只接受−1、0、＋1；此输入需其他编码")
    bits = f"{values[0]:08b}" + "".join(codes[d] for d in deltas)
    payload = pack(bits)
    # Decode the packed payload, not the original list.
    decoded_bits = "".join(f"{b:08b}" for b in payload)[:len(bits)]
    decoded = [int(decoded_bits[:8], 2)]
    reverse = {v: k for k, v in codes.items()}
    for i in range(8, len(decoded_bits), 2):
        decoded.append(decoded[-1] + reverse[decoded_bits[i:i+2]])
    return {"起点": values[0], "差值": deltas, "有效bit": len(bits),
            "payload_B": len(payload), "补位bit": -len(bits) % 8,
            "读回": decoded, "完整恢复": decoded == values}

def approximate(values):
    values = list(values)
    if any(not 0 <= v <= 255 for v in values):
        raise ValueError("灰度需在0–255之间")
    levels = [min(63, (v+2)//4) for v in values]
    bits = "".join(f"{v:06b}" for v in levels)
    payload = pack(bits)
    decoded_bits = "".join(f"{b:08b}" for b in payload)[:len(bits)]
    restored = [int(decoded_bits[i:i+6], 2)*4 for i in range(0, len(bits), 6)]
    return {"原值": values, "等级编号": levels, "代表值": restored,
            "有效bit": len(bits), "payload_B": len(payload), "完整恢复": restored == values}

def image_evidence():
    """Read packaged full files and compare decoded RGB pixels.

    Use the bundled source fixture so notebook and deck use exactly the same
    pixels even if Pillow's default drawing font changes between installations.
    """
    folder = ROOT / "assets" / "evidence"
    with Image.open(folder / "test-source.png") as image:
        source = image.convert("RGB")
    raw = source.tobytes()
    records = []
    for name in ("test-source.png", "test-quality80.jpg", "test-quality20.jpg"):
        path = folder / name
        with Image.open(path) as image:
            decoded = image.convert("RGB")
        data = decoded.tobytes()
        changed = sum(raw[i:i+3] != data[i:i+3] for i in range(0, len(raw), 3))
        records.append({"文件": name, "完整文件B": path.stat().st_size,
                        "尺寸": decoded.size, "变化像素": changed,
                        "回读像素一致": raw == data})
    return {"未压缩RGB数据B": len(raw), "像素总数": source.width*source.height,
            "结果": records}

def show_comparison_pair():
    """Neutral display: do not leak filename/format before the Q7 prediction."""
    from IPython.display import display, Image as DisplayImage
    for label, name in [('A', 'test-source.png'), ('B', 'test-quality80.jpg')]:
        print(label)
        display(DisplayImage(filename=str(ROOT/'assets/evidence'/name), width=384))

def save_jpeg_trial(quality=80):
    """Optional live parameter trial. Never overwrite the packaged evidence."""
    if not isinstance(quality, int) or not 1 <= quality <= 95:
        raise ValueError("quality使用1–95的整数")
    folder = ROOT / "demos" / "scratch"
    folder.mkdir(exist_ok=True)
    output = folder / f"trial-quality{quality}.jpg"
    with Image.open(ROOT / "assets/evidence/test-source.png") as image:
        source = image.convert("RGB")
    source.save(output, quality=quality, subsampling=0)
    with Image.open(output) as image:
        restored = image.convert("RGB")
    return {"quality": quality, "完整文件B": output.stat().st_size,
            "回读像素一致": source.tobytes() == restored.tobytes(), "路径": str(output)}

def video_changes():
    """Two exact 8x4 frames: a 2x2 block moves right by one position."""
    first = [0] * 32
    second = [0] * 32
    for y in (1, 2):
        for x in (2, 3): first[y*8+x] = 1
        for x in (3, 4): second[y*8+x] = 1
    updates = [(i, b) for i, (a, b) in enumerate(zip(first, second)) if a != b]
    restored = first.copy()
    for i, value in updates: restored[i] = value
    return {"帧一": first, "帧二": second, "更新": updates,
            "变化格数": len(updates), "完整恢复": restored == second}

if __name__ == "__main__":
    print(json.dumps({"D1": opening(True), "D2": {"原B": len(COLORS),
        "编码B": len(rle_encode(COLORS)), "反例B": len(rle_encode(ALTERNATING))},
        "D3": predictive(GRAY), "D4": approximate(GRAY), "D5": image_evidence()},
        ensure_ascii=False, indent=2))
