#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Demonstrate spatial sampling, palette quantization, and fixed-length encoding.

Use Python's standard library and unrounded precomputed RGB means.
The optional teaching route is 8x8/4 colors, 16x16/4 colors, then 16x16/6 colors.
Chinese string literals are student-facing interface labels.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
import tkinter as tk
import tkinter.font as tkfont

APP_DIR = Path(__file__).resolve().parent
DATA_PATH = APP_DIR / "panda_samples.json"

FRAME_VIOLET = "#6251B1"
ACCENT_VIOLET = "#8C64E1"
FOCUS_RED = "#FF0000"
TITLE_BLACK = "#262626"
BODY_BLACK = "#000000"
MUTED_GRAY = "#808080"
GRID_GRAY = "#D9D9D9"
WHITE = "#FFFFFF"

SUPPORTED_GRIDS = (8, 16)
SUPPORTED_LEVELS = (4, 6)
DEFAULT_GRID = 8
DEFAULT_LEVELS = 4


def bits_for_levels(levels: int) -> int:
    return max(1, math.ceil(math.log2(levels)))


def nearest_palette(rgb: list[float], palette: list[list[int]]) -> tuple[int, list[int], float]:
    """Return (index, palette_rgb, squared_rgb_distance)."""
    best_i = 0
    best_d = None
    for i, p in enumerate(palette):
        d = sum((rgb[k] - p[k]) ** 2 for k in range(3))
        if best_d is None or d < best_d:
            best_i, best_d = i, d
    return best_i, palette[best_i], float(best_d or 0)


def codeword(index: int, levels: int) -> str:
    return format(index, f"0{bits_for_levels(levels)}b")


def self_test() -> None:
    assert DATA_PATH.exists(), "Missing panda_samples.json"
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    assert tuple(data["supported_grids"]) == SUPPORTED_GRIDS
    assert tuple(data["supported_levels"]) == SUPPORTED_LEVELS
    assert len(data["palette_rgb"]) >= 6

    for n in SUPPORTED_GRIDS:
        rows = data["grids"][str(n)]
        assert len(rows) == n and all(len(row) == n for row in rows)
        for row in rows:
            for rgb in row:
                assert len(rgb) == 3
                assert all(isinstance(v, (int, float)) and 0 <= v <= 255 for v in rgb)

    assert bits_for_levels(4) == 2
    assert bits_for_levels(6) == 3
    assert 8 * 8 * 2 == 128
    assert 16 * 16 * 2 == 512
    assert 16 * 16 * 3 == 768

    ex = data["row_exercise"]
    row = data["grids"]["16"][ex["row"] - 1][ex["first_column"] - 1 : ex["last_column"]]
    got = [nearest_palette(rgb, data["palette_rgb"][:4])[0] for rgb in row]
    assert got == ex["indices"], (got, ex["indices"])
    assert [codeword(i, 4) for i in got] == ex["codes"]

    print("SELF-TEST PASS")
    print("source:", data["source"])
    print("crop:", data["crop"])
    print("grids: 8×8, 16×16")
    print("palette choices: 4, 6")
    print("runtime dependencies: Python stdlib only")


class Demo:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("熊猫怎样变成二进制数据？｜图像数字化课堂演示")
        self.root.configure(bg=WHITE)
        self.root.minsize(900, 680)

        try:
            self.root.state("zoomed")
        except tk.TclError:
            sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.root.geometry(f"{sw}x{sh}+0+0")

        self.data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        self.grid_n = DEFAULT_GRID
        self.levels = DEFAULT_LEVELS
        self.selected_row = 1
        self.selected_col = 2

        sw = self.root.winfo_screenwidth()
        self.compact = sw < 1150
        self.canvas_size = 360 if self.compact else 448

        self.font_family = self._font()
        self.title_font = (self.font_family, 26, "bold")
        self.body_font = (self.font_family, 13)
        self.body_bold = (self.font_family, 13, "bold")
        self.small_font = (self.font_family, 11)
        self.code_font = (self.font_family, 16, "bold")

        self.grid_buttons: dict[int, tk.Button] = {}
        self.level_buttons: dict[int, tk.Button] = {}

        self._build()
        self._bind()
        self.refresh()

    def _font(self) -> str:
        families = set(tkfont.families(self.root))
        for f in (
            "Alibaba PuHuiTi 3.0",
            "Microsoft YaHei UI",
            "Microsoft YaHei",
            "PingFang SC",
            "Arial",
        ):
            if f in families:
                return f
        return "TkDefaultFont"

    def _build(self) -> None:
        tk.Frame(self.root, bg=FRAME_VIOLET, height=7).pack(fill="x")

        header = tk.Frame(self.root, bg=WHITE)
        header.pack(fill="x", padx=24, pady=(14, 6))
        tk.Label(
            header, text="熊猫怎样变成二进制数据？",
            font=self.title_font, fg=TITLE_BLACK, bg=WHITE
        ).pack(side="left")
        tk.Label(
            header, text="采样 → 量化 → 编码",
            font=(self.font_family, 17, "bold"),
            fg=ACCENT_VIOLET, bg=WHITE
        ).pack(side="left", padx=(20, 0), pady=(4, 0))
        tk.Label(
            header, text="先预测，再只改变一个参数。",
            font=self.small_font, fg=MUTED_GRAY, bg=WHITE
        ).pack(side="right", pady=(8, 0))

        controls = tk.Frame(self.root, bg=WHITE)
        controls.pack(fill="x", padx=24, pady=(2, 8))

        tk.Label(
            controls, text="采样分辨率", font=self.body_bold,
            fg=BODY_BLACK, bg=WHITE
        ).pack(side="left")
        for n in SUPPORTED_GRIDS:
            b = tk.Button(
                controls, text=f"{n}×{n}", font=self.body_font,
                bd=1, relief="solid", padx=12, pady=4, cursor="hand2",
                command=lambda v=n: self.set_grid(v)
            )
            b.pack(side="left", padx=(8, 0))
            self.grid_buttons[n] = b

        tk.Label(
            controls, text="可用颜色", font=self.body_bold,
            fg=BODY_BLACK, bg=WHITE
        ).pack(side="left", padx=(30, 0))
        for n in SUPPORTED_LEVELS:
            b = tk.Button(
                controls, text=f"{n} 色", font=self.body_font,
                bd=1, relief="solid", padx=12, pady=4, cursor="hand2",
                command=lambda v=n: self.set_levels(v)
            )
            b.pack(side="left", padx=(8, 0))
            self.level_buttons[n] = b

        tk.Button(
            controls, text="重置", font=self.small_font,
            bd=1, relief="solid", padx=10, pady=4,
            bg=WHITE, fg=MUTED_GRAY, command=self.reset
        ).pack(side="right")

        main = tk.Frame(self.root, bg=WHITE)
        main.pack(pady=(4, 4))

        left = tk.Frame(main, bg=WHITE)
        left.grid(row=0, column=0, padx=(0, 24))
        tk.Label(
            left, text="采样后的 RGB 样本", font=self.body_bold,
            bg=WHITE, fg=BODY_BLACK
        ).pack(pady=(0, 6))
        self.sample_canvas = tk.Canvas(
            left, width=self.canvas_size, height=self.canvas_size,
            bg=WHITE, highlightthickness=1,
            highlightbackground=GRID_GRAY, cursor="crosshair"
        )
        self.sample_canvas.pack()
        self.sample_canvas.bind("<Button-1>", self.on_click)

        middle = tk.Frame(main, bg=WHITE, width=110)
        middle.grid(row=0, column=1)
        middle.grid_propagate(False)
        tk.Label(middle, text="", bg=WHITE).pack(pady=90)
        tk.Label(
            middle, text="量化\n+\n编码",
            font=(self.font_family, 18, "bold"),
            fg=ACCENT_VIOLET, bg=WHITE, justify="center"
        ).pack()
        tk.Label(
            middle, text="→",
            font=(self.font_family, 30, "bold"),
            fg=ACCENT_VIOLET, bg=WHITE
        ).pack(pady=(4, 0))

        right = tk.Frame(main, bg=WHITE)
        right.grid(row=0, column=2, padx=(24, 0))
        tk.Label(
            right, text="量化后的数字图像", font=self.body_bold,
            bg=WHITE, fg=BODY_BLACK
        ).pack(pady=(0, 6))
        self.digital_canvas = tk.Canvas(
            right, width=self.canvas_size, height=self.canvas_size,
            bg=WHITE, highlightthickness=1,
            highlightbackground=GRID_GRAY, cursor="crosshair"
        )
        self.digital_canvas.pack()
        self.digital_canvas.bind("<Button-1>", self.on_click)

        tk.Frame(self.root, bg=FRAME_VIOLET, height=2).pack(
            fill="x", padx=24, pady=(8, 6)
        )

        info = tk.Frame(self.root, bg=WHITE)
        info.pack(fill="x", padx=28, pady=(0, 8))
        info.grid_columnconfigure(0, weight=1)
        info.grid_columnconfigure(1, weight=1)
        if not self.compact:
            info.grid_columnconfigure(2, weight=1)

        self.cell_label = self._info_label(info, bold=True)
        self.sample_label = self._info_label(info)
        self.quant_label = self._info_label(info)
        self.code_label = tk.Label(
            info, text="", font=self.code_font,
            bg=WHITE, fg=ACCENT_VIOLET, anchor="w"
        )
        self.data_label = self._info_label(info)
        self.rule_label = tk.Label(
            info, text="", font=self.small_font,
            bg=WHITE, fg=MUTED_GRAY, anchor="w"
        )

        if self.compact:
            self.cell_label.grid(row=0, column=0, sticky="w")
            self.quant_label.grid(row=0, column=1, sticky="w", padx=(18, 0))
            self.sample_label.grid(row=1, column=0, sticky="w", pady=(3, 0))
            self.code_label.grid(row=1, column=1, sticky="w", padx=(18, 0), pady=(3, 0))
            self.data_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 0))
            self.rule_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(2, 0))
        else:
            self.cell_label.grid(row=0, column=0, sticky="w")
            self.sample_label.grid(row=1, column=0, sticky="w", pady=(3, 0))
            self.quant_label.grid(row=0, column=1, sticky="w", padx=(24, 0))
            self.code_label.grid(row=1, column=1, sticky="w", padx=(24, 0), pady=(3, 0))
            self.data_label.grid(row=0, column=2, sticky="w", padx=(24, 0))
            self.rule_label.grid(row=1, column=2, sticky="w", padx=(24, 0), pady=(3, 0))

        tk.Frame(self.root, bg=FRAME_VIOLET, height=7).pack(fill="x", side="bottom")

    def _info_label(self, parent: tk.Widget, bold: bool = False) -> tk.Label:
        return tk.Label(
            parent, text="",
            font=self.body_bold if bold else self.body_font,
            bg=WHITE, fg=BODY_BLACK, anchor="w"
        )

    def _bind(self) -> None:
        self.root.bind("1", lambda e: self.set_grid(8))
        self.root.bind("2", lambda e: self.set_grid(16))
        self.root.bind("q", lambda e: self.set_levels(4))
        self.root.bind("w", lambda e: self.set_levels(6))
        self.root.bind("<Control-r>", lambda e: self.reset())

    def reset(self) -> None:
        self.grid_n = DEFAULT_GRID
        self.levels = DEFAULT_LEVELS
        self.selected_row = 1
        self.selected_col = 2
        self.refresh()

    def set_grid(self, n: int) -> None:
        if n == self.grid_n:
            return
        yr = (self.selected_row + 0.5) / self.grid_n
        xr = (self.selected_col + 0.5) / self.grid_n
        self.grid_n = n
        self.selected_row = min(n - 1, int(yr * n))
        self.selected_col = min(n - 1, int(xr * n))
        self.refresh()

    def set_levels(self, n: int) -> None:
        if n != self.levels:
            self.levels = n
            self.refresh()

    def on_click(self, event: tk.Event) -> None:
        cell = self.canvas_size / self.grid_n
        self.selected_col = min(self.grid_n - 1, max(0, int(event.x / cell)))
        self.selected_row = min(self.grid_n - 1, max(0, int(event.y / cell)))
        self.refresh_selection()

    def _palette(self) -> list[list[int]]:
        return self.data["palette_rgb"][: self.levels]

    @staticmethod
    def _hex(rgb: list[float]) -> str:
        vals = [max(0, min(255, int(round(v)))) for v in rgb]
        return "#{:02x}{:02x}{:02x}".format(*vals)

    def refresh(self) -> None:
        self._buttons()
        self._draw_samples()
        self._draw_quantized()
        self.refresh_selection()

    def _buttons(self) -> None:
        for n, b in self.grid_buttons.items():
            active = n == self.grid_n
            b.configure(
                bg=ACCENT_VIOLET if active else WHITE,
                fg=WHITE if active else BODY_BLACK,
                activebackground=ACCENT_VIOLET if active else WHITE,
                activeforeground=WHITE if active else BODY_BLACK,
            )
        for n, b in self.level_buttons.items():
            active = n == self.levels
            b.configure(
                bg=ACCENT_VIOLET if active else WHITE,
                fg=WHITE if active else BODY_BLACK,
                activebackground=ACCENT_VIOLET if active else WHITE,
                activeforeground=WHITE if active else BODY_BLACK,
            )

    def _draw_samples(self) -> None:
        self.sample_canvas.delete("all")
        rows = self.data["grids"][str(self.grid_n)]
        cell = self.canvas_size / self.grid_n
        for r, row in enumerate(rows):
            for c, rgb in enumerate(row):
                self.sample_canvas.create_rectangle(
                    c * cell, r * cell, (c + 1) * cell, (r + 1) * cell,
                    fill=self._hex(rgb), outline=GRID_GRAY, width=1
                )

    def _draw_quantized(self) -> None:
        self.digital_canvas.delete("all")
        rows = self.data["grids"][str(self.grid_n)]
        pal = self._palette()
        cell = self.canvas_size / self.grid_n
        for r, row in enumerate(rows):
            for c, rgb in enumerate(row):
                _, q, _ = nearest_palette(rgb, pal)
                self.digital_canvas.create_rectangle(
                    c * cell, r * cell, (c + 1) * cell, (r + 1) * cell,
                    fill=self._hex(q), outline=GRID_GRAY, width=1
                )

    def refresh_selection(self) -> None:
        self._focus(self.sample_canvas)
        self._focus(self.digital_canvas)

        rgb = self.data["grids"][str(self.grid_n)][self.selected_row][self.selected_col]
        pal = self._palette()
        idx, q, dist2 = nearest_palette(rgb, pal)
        bits = bits_for_levels(self.levels)
        code = codeword(idx, self.levels)
        total_bits = self.grid_n * self.grid_n * bits

        self.cell_label.configure(
            text=f"选中：第 {self.selected_row + 1} 行，第 {self.selected_col + 1} 列"
        )
        self.sample_label.configure(
            text="采样均值 RGB ≈ ({:.2f}, {:.2f}, {:.2f})".format(*rgb)
        )
        self.quant_label.configure(
            text=f"量化：→ 颜色编号 {idx}  RGB = ({q[0]}, {q[1]}, {q[2]})"
        )
        self.code_label.configure(text=f"编码：{idx} → {code}")
        self.data_label.configure(
            text=f"位深度 {bits} bit/像素；总计 {total_bits:,} bit = {total_bits // 8:,} B"
        )
        states = 2 ** bits
        if states == self.levels:
            rule = f"{bits} bit 有 {states} 种状态，刚好表示 {self.levels} 种颜色。"
        else:
            rule = f"{bits} bit 有 {states} 种状态，本实验使用其中 {self.levels} 种。"
        self.rule_label.configure(text=rule)

    def _focus(self, canvas: tk.Canvas) -> None:
        canvas.delete("focus")
        cell = self.canvas_size / self.grid_n
        x0 = self.selected_col * cell
        y0 = self.selected_row * cell
        canvas.create_rectangle(
            x0 + 1, y0 + 1, x0 + cell - 1, y0 + cell - 1,
            outline=FOCUS_RED, width=3, tags="focus"
        )


def main() -> None:
    if "--self-test" in sys.argv:
        self_test()
        return
    if not DATA_PATH.exists():
        raise SystemExit("Missing panda_samples.json")
    root = tk.Tk()
    Demo(root)
    root.mainloop()


if __name__ == "__main__":
    main()
