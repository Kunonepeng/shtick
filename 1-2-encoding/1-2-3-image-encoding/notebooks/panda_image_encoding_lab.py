"""Browser-based panda digitization demonstration for the frozen 85-slide lesson.

The lesson's existing panda_lab module is the sole numerical authority.
The browser only presents precomputed image samples, palette indices and codes.
"""
from __future__ import annotations

import base64
import io
import json
from pathlib import Path
from uuid import uuid4

from IPython.display import HTML, Javascript, display

from demos import panda_lab as lab

HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "f6679d0c7f119ec953e44be6912f03b2bd35bd032e27579241562b1bb46b5186"
SUPPORTED_GRIDS = (8, 16)
SUPPORTED_LEVELS = (4, 6)


def build_payload() -> dict:
    """Compute all displayed states with the identical rules as panda_lab."""
    original = lab.load_source()
    x, y, width, height = lab.CROP
    crop = original.crop((x, y, x + width, y + height))
    buffer = io.BytesIO()
    crop.save(buffer, format="PNG")
    preview = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")
    states = {}
    for grid in SUPPORTED_GRIDS:
        means = lab.sample_blocks(grid)
        states[str(grid)] = {}
        for levels in SUPPORTED_LEVELS:
            indices = lab.quantize(means, levels)
            bits = lab.minimum_bits(levels)
            states[str(grid)][str(levels)] = {
                "samples": means.tolist(),
                "indices": indices.tolist(),
                "codes": lab.encode(indices, bits),
                "bits": bits,
                "pixel_count": grid * grid,
                "ideal_payload_bits": grid * grid * bits,
            }
    return {
        "preview": preview,
        "crop": {"x": x, "y": y, "width": width, "height": height},
        "palette": lab.PALETTE.tolist(),
        "states": states,
        "fixture_sha256": EXPECTED_SHA256,
        "model_notice": "这是对已有数字JPEG的解码像素进行的教学模拟，不是真实相机的连续光场采集。",
    }


def self_check() -> dict:
    """Check sample layout, code mapping, bit capacity and fixed data contract."""
    if lab.SOURCE_SHA256 != EXPECTED_SHA256:
        raise AssertionError("Fixture hash contract changed.")
    payload = build_payload()
    fixture_path = HERE.parent / "demos" / "panda-digitization" / "panda_samples.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    assert fixture["source_sha256"] == EXPECTED_SHA256
    assert fixture["crop"] == dict(zip(("x", "y", "width", "height"), lab.CROP))
    assert fixture["palette_rgb"] == payload["palette"]
    for grid in SUPPORTED_GRIDS:
        expected_rows = fixture["grids"][str(grid)]
        computed_rows = payload["states"][str(grid)]["4"]["samples"]
        assert len(expected_rows) == len(computed_rows)
        for expected_row, computed_row in zip(expected_rows, computed_rows):
            for expected_pixel, computed_pixel in zip(expected_row, computed_row):
                assert all(abs(a - b) < 1e-8 for a, b in zip(expected_pixel, computed_pixel))
    for grid in SUPPORTED_GRIDS:
        reference_samples = lab.sample_blocks(grid)
        for levels in SUPPORTED_LEVELS:
            state = payload["states"][str(grid)][str(levels)]
            bits = state["bits"]
            assert bits == (2 if levels == 4 else 3)
            assert state["pixel_count"] == grid ** 2
            assert len(state["samples"]) == grid
            assert all(len(row) == grid for row in state["samples"])
            assert len(state["indices"]) == grid
            assert all(len(row) == grid for row in state["indices"])
            assert len(state["codes"]) == grid ** 2
            assert state["ideal_payload_bits"] == grid * grid * bits
            for row_index in range(grid):
                for column in range(grid):
                    actual = state["samples"][row_index][column]
                    expected = reference_samples[row_index, column].tolist()
                    assert actual == expected
                    idx = state["indices"][row_index][column]
                    assert 0 <= idx < levels
                    word = state["codes"][row_index * grid + column]
                    assert word == format(idx, f"0{bits}b")
    return {
        "status": "PASS",
        "grid_sizes": list(SUPPORTED_GRIDS),
        "palette_sizes": list(SUPPORTED_LEVELS),
        "states_checked": 4,
        "real_fixture_verified": True,
    }


def launch(config: dict | None = None) -> None:
    """Display an isolated, directly interactive JupyterLab browser visualization."""
    config = dict(config or {})
    if not 0 <= int(config.get("stage", 0)) <= 3:
        raise ValueError("stage must be in 0..3")
    if int(config.get("grid", 8)) not in SUPPORTED_GRIDS:
        raise ValueError("grid must be 8 or 16")
    if int(config.get("levels", 4)) not in SUPPORTED_LEVELS:
        raise ValueError("levels must be 4 or 6")
    features = config.get("features", [])
    if not isinstance(features, list) or not all(isinstance(f, str) for f in features):
        raise ValueError("features must be a list of strings")
    payload = build_payload()
    root_id = "panda_enc_" + uuid4().hex
    css = (HERE / "panda-image-encoding-ui.css").read_text(encoding="utf-8")
    javascript = (HERE / "panda-image-encoding-ui.js").read_text(encoding="utf-8")
    display(HTML(f'<style>{css}</style><div id="{root_id}"></div>'))
    display(Javascript(
        "(function(){\n" + javascript + "\n" +
        f"const root=document.getElementById({json.dumps(root_id)});\n" +
        "if(!root) throw Error('Panda image demo root missing');\n" +
        f"const payload={json.dumps(payload, ensure_ascii=False, separators=(',', ':'))};\n" +
        f"const config={json.dumps(config, ensure_ascii=False, separators=(',', ':'))};\n" +
        "mountPandaEncoding(root,payload,config);\n})();"
    ))
