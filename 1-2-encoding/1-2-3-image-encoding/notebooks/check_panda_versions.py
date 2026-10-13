"""Repeatable static/notebook/data checks for panda-image-encoding versions.

Run from any directory: python notebooks/check_panda_versions.py
Requires the existing lesson requirements and nbformat.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import nbformat

HERE = Path(__file__).resolve().parent
COURSE = HERE.parent
sys.path.insert(0, str(COURSE))
sys.path.insert(0, str(HERE))

from panda_image_encoding_lab import self_check

VERSIONS = ["v0", "v1"] + [f"v1.{index}" for index in range(1, 11)]
FEATURE_ROUNDS = [
    "largeType",
    "fixedAlignment",
    "paletteLegend",
    "sampleMagnifier",
    "codeFocus",
    "highContrast",
    "responsiveAid",
    "focusMarker",
    "questionEmphasis",
    "largeTargets",
]


def verify_notebooks() -> None:
    accumulated = []
    for version in VERSIONS:
        path = HERE / f"panda-image-encoding-{version}.ipynb"
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        assert notebook.metadata.panda_demo_version == version, version
        ids = [cell.id for cell in notebook.cells]
        assert len(ids) == len(set(ids)), version
        assert all(cell.execution_count is None and not cell.outputs
                   for cell in notebook.cells if cell.cell_type == "code"), version
        code = "\n".join(cell.source for cell in notebook.cells
                         if cell.cell_type == "code")
        assert "launch(" in code, version
        if version != "v0":
            assert "self_check()" in code, version
            assert len(notebook.cells) == 6, version
        if version.startswith("v1."):
            round_number = int(version.split(".")[1])
            expected = FEATURE_ROUNDS[:round_number]
            if round_number == 10:
                expected += ["projectionCompact"]
            assert notebook.metadata.panda_visual_round == round_number, version
            assert list(notebook.metadata.panda_visual_features) == expected, version
            assert json.dumps(expected) in code, version
        print(f"PASS {version}: notebook schema, clean outputs, configuration")


def verify_frontend_source() -> None:
    frontend = (HERE / "panda-image-encoding-ui.js").read_text(encoding="utf-8")
    css = (HERE / "panda-image-encoding-ui.css").read_text(encoding="utf-8")
    for flag in FEATURE_ROUNDS + ["projectionCompact"]:
        assert f"features.has('{flag}')" in frontend, flag
    assert "function mountPandaEncoding" in frontend
    assert "aria-label" in frontend and "aria-pressed" in frontend
    assert ".panda-demo" in css and "pd-codeband" in css
    node = shutil.which("node")
    if node:
        subprocess.run([node, "--check", str(HERE / "panda-image-encoding-ui.js")],
                       check=True, capture_output=True, text=True)
        print("PASS JavaScript syntax (node --check)")
    else:
        print("NOT RUN JavaScript syntax: node is not installed")
    print("PASS frontend source feature coverage")


def main() -> None:
    print("Python data-contract verification:", self_check())
    verify_notebooks()
    verify_frontend_source()
    print("PASS: static and numerical checks. Browser rendering remains untested.")


if __name__ == "__main__":
    main()
