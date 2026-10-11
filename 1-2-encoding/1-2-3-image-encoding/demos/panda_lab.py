"""Reproducible notebook experiments for the frozen panda image-encoding deck.

Chinese literals are student-facing labels; implementation text is English.
The image is an existing decoded JPEG, not a physical camera measurement.
"""

from __future__ import annotations

import base64
import hashlib
import html
import io
from pathlib import Path

import numpy as np
from PIL import Image
from IPython.display import HTML, display

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "pandas.jpg"
SOURCE_SHA256 = "f6679d0c7f119ec953e44be6912f03b2bd35bd032e27579241562b1bb46b5186"
CROP = (280, 100, 288, 288)
PALETTE = np.array([
    [36, 33, 27], [119, 118, 110], [188, 187, 179],
    [242, 240, 230], [81, 76, 65], [219, 217, 206],
], dtype=np.uint8)


def positive_integer(value: int, name: str) -> int:
    """Reject floats and booleans instead of silently rounding parameters."""
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return int(value)


def load_source() -> Image.Image:
    """Verify the original asset before computing experimental evidence."""
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError("Source image hash differs from the frozen lesson fixture")
    with Image.open(SOURCE) as image:
        return image.convert("RGB")


def sample_blocks(width: int = 8, height: int | None = None) -> np.ndarray:
    """Return unrounded RGB means, indexed [row, column, channel]."""
    width = positive_integer(width, "width")
    height = positive_integer(width if height is None else height, "height")
    x, y, w, h = CROP
    if w % width or h % height:
        raise ValueError("Grid dimensions must divide the 288 by 288 source region")
    image = np.asarray(load_source(), dtype=np.float64)[y:y + h, x:x + w]
    return image.reshape(height, h // height, width, w // width, 3).mean(axis=(1, 3))


def quantize(means: np.ndarray, levels: int = 4) -> np.ndarray:
    """Use squared RGB distance; argmin resolves ties to the lowest index."""
    levels = positive_integer(levels, "levels")
    if levels > len(PALETTE):
        raise ValueError("The lesson palette contains at most six colors")
    values = np.asarray(means, dtype=float)
    if values.ndim != 3 or values.shape[-1] != 3 or not np.isfinite(values).all():
        raise ValueError("Samples must be a finite height by width by 3 array")
    if np.any((values < 0) | (values > 255)):
        raise ValueError("RGB samples must be between 0 and 255")
    distances = ((values[:, :, None, :] - PALETTE[None, None, :levels, :]) ** 2).sum(axis=3)
    return distances.argmin(axis=2)


def minimum_bits(colors: int) -> int:
    """Return the shortest fixed code width for at least two color states."""
    colors = positive_integer(colors, "colors")
    if colors < 2:
        raise ValueError("This classroom model requires at least two colors")
    return (colors - 1).bit_length()


def encode(indices: np.ndarray, bits: int) -> list[str]:
    """Encode row-major indices, preserving leading zeros in every word."""
    bits = positive_integer(bits, "bits")
    values = np.asarray(indices)
    if values.size == 0 or not np.issubdtype(values.dtype, np.integer):
        raise ValueError("Indices must be a nonempty integer array")
    if np.any((values < 0) | (values >= 2 ** bits)):
        raise ValueError("An index does not fit the specified fixed code width")
    return [format(int(value), f"0{bits}b") for value in values.ravel(order="C")]


def decode(words: list[str], width: int, height: int, bits: int, levels: int = 4) -> np.ndarray:
    """Decode only the recorded indices using explicit dimensions and rules."""
    width, height = positive_integer(width, "width"), positive_integer(height, "height")
    bits, levels = positive_integer(bits, "bits"), positive_integer(levels, "levels")
    if levels > len(PALETTE) or levels > 2 ** bits:
        raise ValueError("The specified code width and lesson palette cannot represent all declared colors")
    if len(words) != width * height:
        raise ValueError("Word count must equal width times height")
    if any(not isinstance(w, str) or len(w) != bits or set(w) - {"0", "1"} for w in words):
        raise ValueError("Every word must contain exactly the specified number of binary digits")
    values = [int(w, 2) for w in words]
    if any(v >= levels for v in values):
        raise ValueError("A codeword has no entry in the selected color table")
    return np.array(values, dtype=int).reshape(height, width)


def payload(width: int, height: int, bits: int) -> dict:
    """Separate ideal bit payload from continuous packing into whole bytes."""
    width, height = positive_integer(width, "width"), positive_integer(height, "height")
    bits = positive_integer(bits, "bits")
    count = width * height * bits
    return {"pixels": width * height, "bits": count, "ideal_B": count / 8,
            "packed_B": (count + 7) // 8, "KiB": count / 8 / 1024}


def check_budget(width: int, height: int, bits: int, colors: int, budget_B: int) -> dict:
    """Check capacity and whole-byte packing independently."""
    colors, budget_B = positive_integer(colors, "colors"), positive_integer(budget_B, "budget_B")
    result = payload(width, height, bits)
    result.update(capacity=2 ** bits, capacity_ok=2 ** bits >= colors,
                  size_ok=result["packed_B"] <= budget_B)
    result["valid"] = result["capacity_ok"] and result["size_ok"]
    return result


def rgb_image(indices: np.ndarray) -> Image.Image:
    """Render indices through the fixed lesson palette without interpolation."""
    values = np.asarray(indices)
    if values.ndim != 2 or not np.issubdtype(values.dtype, np.integer):
        raise ValueError("Image indices must be a two-dimensional integer array")
    if np.any((values < 0) | (values >= len(PALETTE))):
        raise ValueError("An index has no palette entry")
    return Image.fromarray(PALETTE[values])


def png_measurement(indices: np.ndarray, levels: int = 4) -> dict:
    """Measure a real indexed PNG and test recovered indices and RGB pixels."""
    values = np.asarray(indices)
    levels = positive_integer(levels, "levels")
    rgb_image(values)
    if levels > len(PALETTE) or np.any(values >= levels):
        raise ValueError("Indices must fit the selected lesson palette")
    bits = next(b for b in (1, 2, 4, 8) if 2 ** b >= levels)
    image = Image.fromarray(values.astype(np.uint8)).convert("P")
    image.putpalette(PALETTE.ravel().tolist() + [0] * (768 - PALETTE.size))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", bits=bits)
    encoded = buffer.getvalue()
    with Image.open(io.BytesIO(encoded)) as restored:
        indices_equal = np.array_equal(values, np.asarray(restored))
        rgb_equal = np.array_equal(np.asarray(rgb_image(values)), np.asarray(restored.convert("RGB")))
    return {"file_B": len(encoded), "PNG_index_bits": encoded[24],
            "indices_equal": indices_equal, "RGB_equal": rgb_equal}


def image_uri(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def show_images(images: list[tuple[str, Image.Image]], size: int = 290) -> None:
    """Display equal-size evidence panels with readable student-facing captions."""
    panels = []
    for title, image in images:
        enlarged = image.resize((size, size), Image.Resampling.NEAREST)
        panels.append(f'<div><p style="font-size:19px;font-weight:600">{html.escape(title)}</p>'
                      f'<img alt="{html.escape(title)}" src="{image_uri(enlarged)}" width="{size}" height="{size}"></div>')
    display(HTML('<div style="display:flex;gap:24px;flex-wrap:wrap;color:#262626">' + ''.join(panels) + '</div>'))


def show_sampling(left_grid: int = 8, right_grid: int = 16, levels: int = 4) -> None:
    """Hold palette and photographed region fixed while changing sample count."""
    panels = []
    for n in (left_grid, right_grid):
        panels.append((f"{n}×{n}，均使用{levels}色", rgb_image(quantize(sample_blocks(n), levels))))
    show_images(panels)


def show_quantization(levels: int = 6) -> None:
    """Hold the same 16 by 16 means fixed while changing available colors."""
    means = sample_blocks(16)
    show_images([("16×16，4色", rgb_image(quantize(means, 4))),
                 (f"16×16，{levels}色", rgb_image(quantize(means, levels)))])


def show_palette(levels: int = 4, bits: int | None = None) -> None:
    levels = positive_integer(levels, "levels")
    if levels > len(PALETTE):
        raise ValueError("The lesson palette contains at most six colors")
    if bits is not None and 2 ** positive_integer(bits, "bits") < levels:
        raise ValueError("The specified fixed code width cannot represent all colors")
    rows = []
    for i, color in enumerate(PALETTE[:levels]):
        hex_color = "#" + ''.join(f"{int(v):02x}" for v in color)
        word = "—" if bits is None else encode(np.array([i]), bits)[0]
        rows.append((i, f'<span style="display:inline-block;width:70px;height:25px;background:{hex_color};border:1px solid #777"></span>',
                     tuple(map(int, color)), word))
    show_table(["编号", "代表色", "RGB", "码字"], rows, raw_columns={1})


def show_table(headers: list[str], rows: list, raw_columns: set | None = None) -> None:
    raw_columns = set() if raw_columns is None else raw_columns
    style = 'style="padding:8px 16px;border-bottom:1px solid #d9d9d9;text-align:left"'
    head = ''.join(f'<th {style}>{html.escape(str(v))}</th>' for v in headers)
    body = ''.join('<tr>' + ''.join(f'<td {style}>{str(v) if i in raw_columns else html.escape(display_value(v))}</td>'
                                  for i, v in enumerate(row)) + '</tr>' for row in rows)
    display(HTML(f'<table style="font-size:18px;border-collapse:collapse;color:#262626"><thead style="color:#6251b1"><tr>{head}</tr></thead><tbody>{body}</tbody></table>'))


def display_value(value) -> str:
    """Format teaching values without NumPy implementation representations."""
    if isinstance(value, np.generic):
        return display_value(value.item())
    if isinstance(value, (tuple, list, np.ndarray)):
        return '(' + ', '.join(display_value(v) for v in value) + ')'
    if isinstance(value, bool):
        return "是" if value else "否"
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def show_row(row: np.ndarray, bits: int | None = None) -> None:
    """Display a horizontal row without the full-matrix reading burden."""
    values = np.asarray(row, dtype=int).reshape(1, -1)
    rgb_image(values)
    words = encode(values, bits) if bits else []
    rows = [("位置", [str(j + 1) for j in range(values.size)]),
            ("编号", [str(int(v)) for v in values.ravel()])]
    if bits:
        rows.append(("码字", words))
    cell_style = 'style="width:65px;min-width:65px;padding:7px 0;text-align:center;border:1px solid #d9d9d9"'
    # Keep each color directly above its number and fixed-length codeword.
    swatches = ''.join(f'<td aria-label="代表色编号{int(v)}" style="width:65px;min-width:65px;height:50px;border:1px solid #777;background:#{"".join(f"{int(c):02x}" for c in PALETTE[v])}"></td>'
                       for v in values.ravel())
    body = '<tr><th style="width:72px">颜色</th>' + swatches + '</tr>'
    body += ''.join('<tr><th style="width:72px;text-align:left">' + label + '</th>'
                    + ''.join(f'<td {cell_style}>{v}</td>' for v in cells) + '</tr>' for label, cells in rows)
    display(HTML('<table style="font-size:21px;border-collapse:collapse;table-layout:fixed">' + body + '</table>'))


def exit_feedback(bits, byte_count, fits, reason: str, submitted: bool = False) -> dict:
    """Give diagnostic feedback only after a complete independent submission."""
    if not submitted:
        return {"已提交": False, "提示": "先独立交答；收齐后再把submitted改为True核对。"}
    if bits is None or byte_count is None or not isinstance(fits, bool) or not isinstance(reason, str) or not reason.strip():
        return {"已提交": False, "提示": "四项答案尚未填全；先补充算式与完整文件的理由。"}
    expected_bits = minimum_bits(5)
    expected_bytes = payload(12, 10, expected_bits)["ideal_B"]
    capacity_ok = isinstance(bits, (int, np.integer)) and not isinstance(bits, bool) and bits == expected_bits
    bytes_ok = isinstance(byte_count, (int, float, np.number)) and not isinstance(byte_count, bool) and byte_count == expected_bytes
    budget_ok = fits == (expected_bytes <= 50)
    return {"已提交": True,
            "固定码长": "核对通过" if capacity_ok else "再比较2的幂与所需颜色数。",
            "像素数据量": "核对通过" if bytes_ok else "再检查像素数、每像素bit和bit/B换算。",
            "预算判断": "核对通过" if budget_ok else "用最终数据量与最多预算比较。",
            "计算三项正确数": int(capacity_ok) + int(bytes_ok) + int(budget_ok),
            "完整文件理由": "人工核对：是否区分像素码字与PNG结构、压缩；程序不判定自由文本。"}


def show_zoom() -> None:
    """Compare the same recorded grid displayed at two sizes."""
    image = rgb_image(quantize(sample_blocks(8), 4))
    display(HTML(f'<div style="display:flex;align-items:flex-start;gap:30px"><div><p>同一份8×8数据</p><img alt="8×8小显示" src="{image_uri(image.resize((144,144),Image.Resampling.NEAREST))}" width="144"></div>'
                 f'<div><p>只扩大显示尺寸</p><img alt="8×8大显示" src="{image_uri(image.resize((288,288),Image.Resampling.NEAREST))}" width="288"></div></div>'))


def show_decoded(words: list[str], width: int, height: int) -> np.ndarray:
    indices = decode(words, width, height, 2, 4)
    image = rgb_image(indices).resize((width * 75, height * 75), Image.Resampling.NEAREST)
    display(HTML(f'<p style="font-size:20px">横{width} × 纵{height}</p><img alt="按指定尺寸解码的像素图" src="{image_uri(image)}" width="{image.width}" height="{image.height}">'))
    show_table(["行", "颜色编号（从左到右）"], [(i + 1, ' '.join(map(str, row))) for i, row in enumerate(indices)])
    return indices


def signal_samples(count: int = 6) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Use an explicitly mathematical continuous function, not sensor evidence."""
    count = positive_integer(count, "count")
    if count < 2:
        raise ValueError("At least two sample positions are required")
    positions = np.linspace(0, 1, count)
    values = 1.5 + 1.2 * np.sin(2 * np.pi * positions + 0.3)
    levels = np.clip(np.floor(values + 0.5), 0, 3).astype(int)
    return positions, values, levels


def show_signal(count: int = 6, stage: str = "sample") -> None:
    import matplotlib.pyplot as plt
    if stage not in {"sample", "quantize"}:
        raise ValueError("stage must be sample or quantize")
    positions, values, levels = signal_samples(count)
    dense = np.linspace(0, 1, 800)
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.plot(dense, 1.5 + 1.2 * np.sin(2 * np.pi * dense + 0.3), color="#6251b1", label="Continuous function (model)")
    ax.scatter(positions, values, s=85, color="#00a8b5", label="Samples", zorder=3)
    if stage == "quantize":
        ax.scatter(positions, levels, s=85, marker="s", color="#d52727", label="Four-level values", zorder=4)
        for x, y, q in zip(positions, values, levels):
            ax.plot([x, x], [y, q], '--', color="#999999")
    ax.set(xlabel="Position / time (normalized)", ylabel="Value (model units)", ylim=(-0.2, 3.5), yticks=range(4))
    ax.tick_params(labelsize=13)
    ax.legend(loc="upper right", fontsize=11)
    fig.tight_layout()
    display(fig)
    plt.close(fig)
