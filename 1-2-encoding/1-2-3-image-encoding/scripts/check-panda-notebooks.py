"""Check provenance, independent fixtures, clean sources, and fresh kernels."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import io
import json
import os
import re
import shutil
import sys
import tempfile
import tokenize
from pathlib import Path

import nbformat
import numpy as np
from jupyter_client import AsyncKernelManager
from nbclient import NotebookClient
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from demos import panda_lab as lab

DECK = ROOT / "1-2-3-image-encoding-panda-v4-20261011.pptx"
DECK_SHA256 = "aa2661338514e717294236bdad42c0bbba8acfa370148a53f9c89ab156c1521b"
REPORT = ROOT / "validation" / "notebooks-20261011"


class CurrentPythonKernel(AsyncKernelManager):
    """Start the kernel with the checker's Python, independent of PATH."""

    def format_kernel_cmd(self, extra_arguments=None):
        command = super().format_kernel_cmd(extra_arguments)
        return [sys.executable] + command[1:]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(notebook) -> str:
    content = [(cell.cell_type, cell.source) for cell in notebook.cells]
    return hashlib.sha256(json.dumps(content, ensure_ascii=False).encode()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--round", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9-]+", args.round):
        raise ValueError("Round name must use lowercase letters, digits, and hyphens")
    destination = REPORT / args.round
    if destination.exists():
        raise FileExistsError("Use a new round name to preserve earlier evidence")
    destination.mkdir(parents=True)
    results = []

    def check(name, condition):
        results.append({"check": name, "status": "pass" if bool(condition) else "fail"})

    def rejects(name, operation):
        try:
            operation()
        except ValueError:
            check(name, True)
        else:
            check(name, False)

    check("frozen_deck_hash", sha(DECK) == DECK_SHA256)
    check("original_image_hash", sha(lab.SOURCE) == lab.SOURCE_SHA256)
    image = lab.load_source()
    check("image_dimensions", image.size == (886, 1000))
    check("Q15_RGB", image.getpixel((422, 230)) == (138, 179, 111))
    palette = lab.PALETTE.tolist()
    reference = json.loads((ROOT / "demos/panda-digitization/panda_samples.json").read_text())
    check("palette_matches_existing_demo", palette == reference["palette_rgb"])
    x, y, w, h = lab.CROP
    crop = image.crop((x, y, x + w, y + h))
    for n in (8, 16):
        means = lab.sample_blocks(n)
        check(f"means{n}_match_existing_fixture", np.allclose(means, reference["grids"][str(n)], rtol=0, atol=1e-10))
        independent = []
        size = 288 // n
        for row in range(n):
            samples = []
            for column in range(n):
                block = [crop.getpixel((column * size + dx, row * size + dy))
                         for dy in range(size) for dx in range(size)]
                samples.append([sum(p[c] for p in block) / len(block) for c in range(3)])
            independent.append(samples)
        check(f"means{n}_independent_pixel_sums", np.allclose(means, independent, rtol=0, atol=1e-10))
        for colors in (4, 6):
            expected = [[min(range(colors), key=lambda i: sum((rgb[c] - palette[i][c]) ** 2 for c in range(3)))
                         for rgb in row] for row in independent]
            check(f"indices{n}_{colors}_independent_search", np.array_equal(lab.quantize(means, colors), expected))
    coarse = lab.quantize(lab.sample_blocks(8), 4)
    fine = lab.quantize(lab.sample_blocks(16), 4)
    check("Q6_fourth_row", coarse[3].tolist() == [3, 3, 2, 0, 1, 2, 1, 1])
    words = lab.encode(fine[5, 4:12], 2)
    check("Q7_read_Q18_fixed_words", words == ["11", "11", "01", "00", "00", "01", "11", "00"])
    for width, height in ((4, 2), (2, 4), (8, 1), (1, 8)):
        recovered = lab.decode(words, width, height, 2)
        check(f"Q18_{width}x{height}_round_trip", lab.encode(recovered, 2) == words)
    check("three_payloads", [lab.payload(w, h, b)["ideal_B"] for w, h, b in [(8, 8, 2), (16, 16, 2), (16, 16, 3)]] == [16, 64, 96])
    check("Q16_payload", lab.payload(500, 333, 24)["ideal_B"] == 499500)
    check("Q16_KiB", math_close(lab.payload(500, 333, 24)["KiB"], 487.79296875))
    check("non_byte_aligned_payload", lab.payload(3, 1, 2)["ideal_B"] == 0.75 and lab.payload(3, 1, 2)["packed_B"] == 1)
    check("budget_B_D", [lab.check_budget(*p, colors=4, budget_B=32)["valid"] for p in [(16,16,2),(16,8,2),(16,16,1),(8,8,2)]] == [False,True,False,True])
    check("E1_fixed_model", lab.minimum_bits(5) == 3 and lab.payload(12, 10, 3)["ideal_B"] == 45)
    png = lab.png_measurement(fine, 4)
    check("PNG_real_IHDR_bits", png["PNG_index_bits"] == 2)
    check("PNG_exact_recorded_indices", png["indices_equal"])
    check("PNG_exact_recorded_RGB", png["RGB_equal"])
    rejects("reject_mismatched_dimensions", lambda: lab.decode(words, 3, 3, 2))
    rejects("reject_missing_leading_zero", lambda: lab.decode(["1"] * 8, 4, 2, 2))
    rejects("reject_nonbinary", lambda: lab.decode(["2x"] * 8, 4, 2, 2))
    rejects("reject_missing_palette_entry", lambda: lab.decode(["11"] * 8, 4, 2, 2, 3))
    rejects("reject_insufficient_code_width", lambda: lab.encode(np.array([4]), 2))
    rejects("reject_fractional_grid", lambda: lab.sample_blocks(8.5))
    rejects("reject_unequal_blocks", lambda: lab.sample_blocks(7))
    rejects("reject_boolean_dimension", lambda: lab.payload(True, 8, 2))
    rejects("reject_inconsistent_decode_capacity", lambda: lab.decode(words, 4, 2, 2, 6))
    rejects("reject_fractional_PNG_indices", lambda: lab.png_measurement(np.array([[1.5]]), 4))
    rejects("reject_PNG_missing_palette_entry", lambda: lab.png_measurement(np.array([[4]]), 4))
    rejects("reject_PNG_unsupported_lesson_palette", lambda: lab.png_measurement(np.array([[0]]), 7))
    five_png = lab.png_measurement(np.array([[0, 1, 2, 3, 4]], dtype=int), 5)
    check("five_color_PNG_uses_four_bits", five_png["PNG_index_bits"] == 4 and five_png["RGB_equal"])
    pending = lab.exit_feedback(3, 45, True, "文件还含结构信息", False)
    check("E1_feedback_withheld_before_submission", not pending["已提交"] and "45" not in str(pending))
    check("E1_incomplete_submission_withheld", not lab.exit_feedback(3, None, True, "", True)["已提交"])
    check("E1_completed_feedback", lab.exit_feedback(3, 45, True, "文件还含结构和压缩", True)["计算三项正确数"] == 3)
    check("E1_wrong_capacity_diagnosed", lab.exit_feedback(2, 45, True, "文件还含结构和压缩", True)["固定码长"] != "核对通过")
    check("display_hides_numpy_types", "np." not in lab.display_value((np.float64(198.11), np.uint8(188))))

    executed = {}
    for role in ("teacher", "student"):
        source = ROOT / f"demo-lab-{role}.qmd"
        path = source.with_suffix(".ipynb")
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        check(f"{role}_source_hash", notebook.metadata.panda_lab.source_sha256 == sha(source))
        check(f"{role}_cell_digest", notebook.metadata.panda_lab.cell_sha256 == digest(notebook))
        check(f"{role}_clean_outputs", all(not c.get("outputs") and c.get("execution_count") is None for c in notebook.cells if c.cell_type == "code"))
        check(f"{role}_no_visible_frontmatter", not notebook.cells[0].source.startswith("---"))
        code = '\n'.join(c.source for c in notebook.cells if c.cell_type == "code")
        ast.parse(code)
        comments = [t.string for t in tokenize.generate_tokens(io.StringIO(code).readline) if t.type == tokenize.COMMENT]
        check(f"{role}_English_implementation_comments", all(c.isascii() for c in comments))
        if role == "student":
            prose = '\n'.join(c.source for c in notebook.cells if c.cell_type == "markdown")
            check("student_no_teacher_blocks", "教师操作与追问" not in prose and "[参考答案]" not in prose)
            check("student_no_precomputed_challenge_words", "11 11 01 00 00 01 11 00" not in prose)
            check("student_E1_independent_first", "answer_bits = None" in code and "answer_bytes = None" in code)
        client = NotebookClient(notebook, kernel_name="python3", kernel_manager_class=CurrentPythonKernel,
                                timeout=60, startup_timeout=60, resources={"metadata": {"path": str(ROOT)}})
        try:
            client.execute()
            errors = [output for cell in notebook.cells for output in cell.get("outputs", []) if output.output_type == "error"]
            check(f"{role}_fresh_kernel", not errors)
        except Exception as error:
            check(f"{role}_fresh_kernel", False)
            (destination / "execution-failure.json").write_text(json.dumps({"type": type(error).__name__, "message": str(error), "results": results}, ensure_ascii=False, indent=2))
            raise
        finally:
            nbformat.write(notebook, destination / f"{role}-executed.ipynb")
        executed[role] = notebook
    completed = nbformat.read(ROOT / "demo-lab-student.ipynb", as_version=4)
    for cell in completed.cells:
        if cell.cell_type != "code":
            continue
        if cell.source.startswith("#| label: d10-reveal"):
            cell.source = cell.source.replace("width, height = 4, 2", "width, height = 2, 4")
        if cell.source.startswith("#| label: e1"):
            cell.source = cell.source.replace("answer_bits = None", "answer_bits = 3").replace("answer_bytes = None", "answer_bytes = 45")
            cell.source = cell.source.replace("answer_fits = None", "answer_fits = True").replace('answer_file_reason = ""', 'answer_file_reason = "还需要PNG文件结构与压缩信息，像素码字量不是完整文件长度。"')
            cell.source = cell.source.replace("submitted = False", "submitted = True")
    with tempfile.TemporaryDirectory(prefix="panda-independent-classroom-") as directory:
        copy_root = Path(directory)
        (copy_root / "assets").mkdir()
        (copy_root / "demos").mkdir()
        shutil.copy2(lab.SOURCE, copy_root / "assets/pandas.jpg")
        shutil.copy2(ROOT / "demos/panda_lab.py", copy_root / "demos/panda_lab.py")
        proof = nbformat.v4.new_code_cell('assert "panda-independent-classroom-" in str(lab.ROOT)\nassert read_back == challenge_words\nassert restored.shape == (4, 2)\nassert feedback["计算三项正确数"] == 3\nprint("STUDENT_COMPLETION_AND_PORTABLE_COPY_PASS")')
        completed.cells.append(proof)
        NotebookClient(completed, kernel_name="python3", kernel_manager_class=CurrentPythonKernel,
                       timeout=60, startup_timeout=60, resources={"metadata": {"path": str(copy_root)}}).execute()
        nbformat.write(completed, destination / "student-completed-portable-executed.ipynb")
    check("student_completed_alternate_dimensions_and_portable_copy", True)
    implementation_paths = [ROOT / "demos/panda_lab.py", Path(__file__), ROOT / "scripts/build-panda-notebooks.py"]
    for path in implementation_paths:
        tokens = tokenize.generate_tokens(io.StringIO(path.read_text()).readline)
        check(f"English_comments_{path.name}", all(t.string.isascii() for t in tokens if t.type == tokenize.COMMENT))
        tree = ast.parse(path.read_text())
        docs = [ast.get_docstring(node) for node in ast.walk(tree) if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef))]
        check(f"English_docstrings_{path.name}", all(text.isascii() for text in docs if text))
    check("frozen_deck_hash_after_execution", sha(DECK) == DECK_SHA256)
    metadata = {"round": args.round, "python": sys.version, "executable": sys.executable,
                "working_directory": str(ROOT), "deck_sha256": sha(DECK), "PNG_example": png,
                "packages": {name: importlib.metadata.version(name) for name in ["numpy", "Pillow", "matplotlib", "nbformat", "nbclient", "ipykernel", "jupyterlab"]},
                "results": results}
    (destination / "checks.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2))
    failures = [r for r in results if r["status"] == "fail"]
    print(json.dumps({"checks": len(results), "failures": failures, "evidence": str(destination)}, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


def math_close(a, b):
    return abs(a - b) < 1e-10


if __name__ == "__main__":
    main()
