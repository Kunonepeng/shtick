"""Convert human-maintained QMD sources to clean notebooks without execution."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]


def cell_digest(notebook) -> str:
    content = [(cell.cell_type, cell.source) for cell in notebook.cells]
    return hashlib.sha256(json.dumps(content, ensure_ascii=False).encode()).hexdigest()


def main() -> None:
    for role in ("teacher", "student"):
        source = ROOT / f"demo-lab-{role}.qmd"
        target = source.with_suffix(".ipynb")
        if target.exists():
            previous = nbformat.read(target, as_version=4)
            recorded = previous.metadata.get("panda_lab", {}).get("cell_sha256")
            if recorded != cell_digest(previous):
                raise RuntimeError(f"Move notebook edits into its QMD source before rebuilding: {target.name}")
            if any(cell.get("outputs") for cell in previous.cells):
                raise RuntimeError(f"Preserve executed notebook separately before rebuilding: {target.name}")
        with tempfile.TemporaryDirectory(prefix="panda-notebook-build-") as directory:
            temporary = Path(directory) / target.name
            subprocess.run(["quarto", "convert", str(source), "--output", str(temporary)], check=True)
            notebook = nbformat.read(temporary, as_version=4)
        notebook.nbformat_minor = max(5, notebook.nbformat_minor)
        if notebook.cells and notebook.cells[0].cell_type == "markdown":
            notebook.cells[0].source = re.sub(r"\A---\n.*?\n---\n\s*", "", notebook.cells[0].source, count=1, flags=re.S)
        for i, cell in enumerate(notebook.cells):
            cell.id = f"{role}-{i:03d}"
            if cell.cell_type == "code":
                cell.outputs = []
                cell.execution_count = None
        notebook.metadata["kernelspec"] = {
            "display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"
        }
        notebook.metadata["panda_lab"] = {
            "role": role, "source": source.name,
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "cell_sha256": cell_digest(notebook), "deck_version": "panda-v4-20261011"
        }
        nbformat.validate(notebook)
        nbformat.write(notebook, target)
        print(f"Generated {target.name}: {len(notebook.cells)} cells; outputs cleared")


if __name__ == "__main__":
    main()
