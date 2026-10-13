"""Browser-rendered classroom demos: no anywidget or Jupyter widgets extension needed.

The Mac Jupyter kernel prepares the audio and samples. Each newly-executed output
contains its own HTML element and browser-side JavaScript. The browser audio
player plays on the Windows classroom computer, not the Mac.
"""
from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4
from IPython.display import HTML, Javascript, display

from .core import lab_data, player_data

HERE = Path(__file__).resolve().parent


class BrowserDemo:
    def __init__(self, mode: str, payload: dict):
        self.mode, self.payload = mode, payload
        self.target = "audio_demo_" + uuid4().hex
        self._cleanup = None

    def _ipython_display_(self):
        """Display on cell execution, using normal trusted HTML/JS outputs."""
        css = (HERE / "style.css").read_text(encoding="utf-8")
        js = (HERE / "frontend.js").read_text(encoding="utf-8")
        # The original JS module finishes with the AnyWidget adapter.
        # Its standalone DOM functions above the adapter need no extra frontend.
        prelude, marker, _ = js.partition("\nexport default")
        if not marker:
            raise RuntimeError("frontend.js missing expected export adapter")
        mount = json.dumps(self.target)
        mode = json.dumps(self.mode)
        data = json.dumps(self.payload, ensure_ascii=False, separators=(",", ":"))
        display(HTML(f'<style>{css}</style><div id="{self.target}"></div>'))
        display(Javascript(
            "(function(){\n" + prelude + "\n"
            + f"const mount = document.getElementById({mount});\n"
            + "if (!mount) throw Error('Missing classroom demo container');\n"
            + "const root = el('div',{class:'audio-v7'}); mount.replaceChildren(root);\n"
            + f"const data={data}; const mode={mode};\n"
            + "if(mode==='player'||mode==='zoom')makePlayer(root,data,mode==='zoom');\n"
            + "else if(mode==='lab')makeLab(root,data);\n"
            + "})();"
        ))


def listening_demo():
    return BrowserDemo("player", player_data(detail=False))


def zoom_demo():
    return BrowserDemo("zoom", player_data(detail=True))


def encoding_lab():
    return BrowserDemo("lab", lab_data())
