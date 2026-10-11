"""Create offline evidence and role-separated classroom archives from checked files."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import zipfile
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args()
    evidence = ROOT / "validation/notebooks-20261011" / args.evidence
    checks = json.loads((evidence / "checks.json").read_text())
    if any(row["status"] != "pass" for row in checks["results"]):
        raise ValueError("Export requires passing notebook evidence")
    notebook = nbformat.read(evidence / "student-executed.ipynb", as_version=4)
    sections = []
    latest_title = "实验准备"
    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            matches = re.findall(r"^## (.+)$", cell.source, flags=re.M)
            if matches:
                latest_title = matches[-1]
        else:
            pieces = []
            for output in cell.get("outputs", []):
                data = output.get("data", {})
                if "text/html" in data:
                    pieces.append(data["text/html"])
                elif "image/png" in data:
                    pieces.append(f'<img alt="{html.escape(latest_title)}" style="max-width:100%" src="data:image/png;base64,{data["image/png"]}">')
                elif output.output_type == "stream" and "font cache" not in output.text:
                    pieces.append('<pre>' + html.escape(output.text) + '</pre>')
            sections.append('<details><summary>' + html.escape(latest_title) + '</summary>' + ''.join(pieces) + '</details>')
    fallback = ROOT / "fallback/teacher-evidence.html"
    fallback.parent.mkdir(exist_ok=True)
    if fallback.exists() and '<!-- panda-notebook-generated -->' not in fallback.read_text():
        raise RuntimeError("Preserve human fallback edits before export")
    content = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<title>图像编码｜教师离线证据</title>
<style>body{max-width:1100px;margin:28px auto;padding:0 20px;font:20px/1.5 "Alibaba PuHuiTi 3.0",sans-serif;color:#262626;background:white}h1{border-bottom:5px solid #6251b1}summary{cursor:pointer;font-weight:bold;padding:12px 0;color:#6251b1}details{border-bottom:1px solid #ddd;padding-bottom:12px}pre{white-space:pre-wrap;font-size:22px}img{image-rendering:pixelated}table{max-width:100%}</style>
<!-- panda-notebook-generated -->
<h1>图像编码｜教师离线证据</h1>
<p>对应85页冻结版。先在PPTX提问、收学生回答，再展开当前证据。其余保持折叠，不提前分发本文件。</p>
<p>图像为已有JPEG的再处理；曲线为数学模型。只计像素码字的B与完整PNG文件长度分开。保存读回检验目标是已量化像素。E1先提交，再回到PPTX81–82页反馈。</p>
'''
    fallback.write_text(content + ''.join(sections) + '</html>')
    export = ROOT / "exports/notebooks-20261011"
    export.mkdir(parents=True, exist_ok=True)
    common = ["demo-lab-student.ipynb", "demos/panda_lab.py", "assets/pandas.jpg", "requirements-notebook.txt"]
    for role in ("teacher", "student"):
        target = export / f"panda-notebooks-{role}-20261011.zip"
        if target.exists():
            raise FileExistsError("Preserve earlier archives before exporting a new kit")
        files = common + (["demo-lab-teacher.ipynb", "demo-lab-teacher.qmd", "demo-lab-student.qmd",
                           "README-notebooks-20261011.md", "fallback/teacher-evidence.html"] if role == "teacher" else [])
        manifest = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in files}
        with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name in files:
                archive.write(ROOT / name, arcname=name)
            instructions = (
                "# 图像编码Notebook课堂副本\n\n"
                "保留assets/与demos/的相对位置，从解压目录启动python -m jupyter lab .，选择已安装依赖的Python内核。\n\n"
                "先运行准备单元；每题先写预测或算式，再逐单元运行。不要Run All。E1先交答，收齐后才开启反馈。\n\n"
                "本包不含PPTX。对应1-2-3-image-encoding-panda-v4-20261011.pptx（85页），页码见Notebook标题。\n\n"
                "依赖为requirements-notebook.txt，课前安装；课堂无需网络。原素材由用户提供，公开再分发许可未确认。\n"
            )
            if role == "teacher":
                instructions += "\n课堂投影学生版；教师版、离线结果用于教师备课／受控揭示，不提前给学生。详细流程见README-notebooks-20261011.md。\n"
            archive.writestr("START-HERE.md", instructions)
            archive.writestr("manifest.json", json.dumps({"role": role, "deck_sha256": checks["deck_sha256"], "files": manifest}, indent=2))
        print(f"Exported {target.name}")
    print(f"Generated {fallback.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
