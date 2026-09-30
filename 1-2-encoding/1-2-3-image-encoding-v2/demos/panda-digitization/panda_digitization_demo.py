#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""熊猫图像数字化课堂演示

目标：用一个可交互界面展示“采样 → 量化 → 编码”。
运行时仅依赖 Python 标准库（tkinter / json / pathlib）。

课堂建议：
1. 先用 8×8、4 灰度，让学生预测“怎样更接近原图？”
2. 只把采样改为 16×16，观察空间细节变化。
3. 保持 16×16，只把灰度级改为 6，观察量化变化。
4. 点击任意格子，查看“样本平均 RGB → 灰度 → 量化值 → 二进制码字”。
"""

from __future__ import annotations

import json
import math
import struct
import sys
from pathlib import Path
import tkinter as tk
import tkinter.font as tkfont

APP_DIR = Path(__file__).resolve().parent
IMAGE_PATH = APP_DIR / "panda_demo.png"
SMALL_IMAGE_PATH = APP_DIR / "panda_demo_small.png"
DATA_PATH = APP_DIR / "panda_samples.json"

# Violet-Rail visual language from the deck
FRAME_VIOLET = "#6251B1"
ACCENT_VIOLET = "#8C64E1"
FOCUS_RED = "#FF0000"
TITLE_BLACK = "#262626"
BODY_BLACK = "#000000"
MUTED_GRAY = "#808080"
GRID_GRAY = "#D9D9D9"
LIGHT_GRAY = "#F2F2F2"
WHITE = "#FFFFFF"

SOURCE_SIZE = 448
LARGE_CANVAS_SIZE = 448
SMALL_CANVAS_SIZE = 384
DEFAULT_GRID = 8
DEFAULT_LEVELS = 4
SUPPORTED_GRIDS = (8, 16, 32, 64)
SUPPORTED_LEVELS = (2, 4, 6, 16, 256)


def read_png_size(path: Path) -> tuple[int, int]:
    """Read PNG dimensions without third-party libraries."""
    with path.open("rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"不是有效 PNG：{path.name}")
    return struct.unpack(">II", header[16:24])


def bits_for_levels(levels: int) -> int:
    """Fixed-length code: minimum integer bits needed for N levels."""
    return max(1, math.ceil(math.log2(levels)))


def rgb_to_gray(rgb: tuple[int, int, int] | list[int]) -> int:
    r, g, b = rgb
    # Standard perceptual luma approximation; rounded to 0..255.
    return max(0, min(255, round(0.299 * r + 0.587 * g + 0.114 * b)))


def quantize_gray(gray: int, levels: int) -> tuple[int, int]:
    """Map 0..255 grayscale to an equally spaced discrete level.

    Returns (level_index, display_gray_value).
    """
    if levels < 2:
        raise ValueError("levels 必须 >= 2")
    idx = round(gray * (levels - 1) / 255)
    q = round(idx * 255 / (levels - 1))
    return idx, q


def codeword(index: int, levels: int) -> str:
    bits = bits_for_levels(levels)
    return format(index, f"0{bits}b")


def format_bytes(bit_count: int) -> str:
    if bit_count % 8 == 0:
        b = bit_count // 8
        return f"{b:,} B"
    return f"{bit_count / 8:.2f} B"


def self_test() -> None:
    """Headless validation for classroom deployment."""
    assert IMAGE_PATH.exists(), "缺少 panda_demo.png"
    assert DATA_PATH.exists(), "缺少 panda_samples.json"
    assert read_png_size(IMAGE_PATH) == (SOURCE_SIZE, SOURCE_SIZE)
    assert SMALL_IMAGE_PATH.exists(), "缺少 panda_demo_small.png"
    assert read_png_size(SMALL_IMAGE_PATH) == (SMALL_CANVAS_SIZE, SMALL_CANVAS_SIZE)

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    assert data["image_size"] == [SOURCE_SIZE, SOURCE_SIZE]
    assert tuple(data["supported_grids"]) == SUPPORTED_GRIDS
    assert tuple(data["supported_levels"]) == SUPPORTED_LEVELS

    for n in SUPPORTED_GRIDS:
        rows = data["grids"][str(n)]
        assert len(rows) == n
        assert all(len(row) == n for row in rows)
        for row in rows:
            for rgb in row:
                assert len(rgb) == 3
                assert all(isinstance(v, int) and 0 <= v <= 255 for v in rgb)

    expected_bits = {2: 1, 4: 2, 6: 3, 16: 4, 256: 8}
    for levels, expected in expected_bits.items():
        assert bits_for_levels(levels) == expected
        for gray in (0, 1, 64, 127, 128, 192, 254, 255):
            idx, q = quantize_gray(gray, levels)
            assert 0 <= idx < levels
            assert 0 <= q <= 255
            cw = codeword(idx, levels)
            assert len(cw) == expected
            assert set(cw) <= {"0", "1"}

    # Deck-aligned data-size checks.
    assert 8 * 8 * bits_for_levels(4) == 128
    assert 16 * 16 * bits_for_levels(4) == 512
    assert 16 * 16 * bits_for_levels(6) == 768

    print("SELF-TEST PASS")
    print(f"source image: {IMAGE_PATH.name} {SOURCE_SIZE}×{SOURCE_SIZE}")
    print(f"small display image: {SMALL_IMAGE_PATH.name} {SMALL_CANVAS_SIZE}×{SMALL_CANVAS_SIZE}")
    print("grids:", ", ".join(f"{n}×{n}" for n in SUPPORTED_GRIDS))
    print("levels:", ", ".join(map(str, SUPPORTED_LEVELS)))
    print("runtime dependencies: Python stdlib only")


class DigitizationDemo:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("熊猫怎样变成二进制数据？｜图像数字化课堂演示")
        self.root.configure(bg=WHITE)
        self.root.minsize(920, 700)

        # Maximized by default on Windows; safe fallback elsewhere.
        try:
            self.root.state("zoomed")
        except tk.TclError:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            self.root.geometry(f"{sw}x{sh}+0+0")

        self.data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

        # Use a smaller display asset only when the screen is narrow. Sampling data
        # still comes from the same 448×448 source image, so concepts/data stay identical.
        sw = self.root.winfo_screenwidth()
        self.compact_layout = sw < 1150
        if self.compact_layout:
            self.canvas_size = SMALL_CANVAS_SIZE
            display_path = SMALL_IMAGE_PATH
        else:
            self.canvas_size = LARGE_CANVAS_SIZE
            display_path = IMAGE_PATH
        self.photo = tk.PhotoImage(file=str(display_path))

        self.grid_n = DEFAULT_GRID
        self.levels = DEFAULT_LEVELS
        self.selected_row = 1  # 第2行
        self.selected_col = 2  # 第3列，呼应课件中的示例

        self.font_family = self._choose_font_family()
        self.title_font = (self.font_family, 26, "bold")
        self.subtitle_font = (self.font_family, 15)
        self.body_font = (self.font_family, 13)
        self.body_bold = (self.font_family, 13, "bold")
        self.small_font = (self.font_family, 11)
        self.code_font = (self.font_family, 16, "bold")

        self.grid_buttons: dict[int, tk.Button] = {}
        self.level_buttons: dict[int, tk.Button] = {}

        self._build_ui()
        self._bind_keys()
        self.refresh_all()

    def _choose_font_family(self) -> str:
        families = set(tkfont.families(self.root))
        preferred = [
            "Alibaba PuHuiTi 3.0",
            "Alibaba PuHuiTi 3.0 55 Regular",
            "Microsoft YaHei UI",
            "Microsoft YaHei",
            "PingFang SC",
            "Arial",
        ]
        for family in preferred:
            if family in families:
                return family
        return "TkDefaultFont"

    def _build_ui(self) -> None:
        # Top rail
        tk.Frame(self.root, bg=FRAME_VIOLET, height=7).pack(fill="x", side="top")

        header = tk.Frame(self.root, bg=WHITE)
        header.pack(fill="x", padx=24, pady=(14, 6))
        tk.Label(
            header,
            text="熊猫怎样变成二进制数据？",
            font=self.title_font,
            fg=TITLE_BLACK,
            bg=WHITE,
        ).pack(side="left")
        tk.Label(
            header,
            text="采样 → 量化 → 编码",
            font=(self.font_family, 17, "bold"),
            fg=ACCENT_VIOLET,
            bg=WHITE,
        ).pack(side="left", padx=(20, 0), pady=(4, 0))
        tk.Label(
            header,
            text="先预测，再只改变一个参数。",
            font=self.small_font,
            fg=MUTED_GRAY,
            bg=WHITE,
        ).pack(side="right", pady=(8, 0))

        controls = tk.Frame(self.root, bg=WHITE)
        controls.pack(fill="x", padx=24, pady=(2, 8))

        tk.Label(
            controls, text="采样分辨率", font=self.body_bold, fg=BODY_BLACK, bg=WHITE
        ).pack(side="left")
        for n in SUPPORTED_GRIDS:
            btn = tk.Button(
                controls,
                text=f"{n}×{n}",
                font=self.body_font,
                bd=1,
                relief="solid",
                padx=10,
                pady=4,
                cursor="hand2",
                command=lambda value=n: self.set_grid(value),
            )
            btn.pack(side="left", padx=(8, 0))
            self.grid_buttons[n] = btn

        tk.Label(
            controls, text="灰度级数", font=self.body_bold, fg=BODY_BLACK, bg=WHITE
        ).pack(side="left", padx=(28, 0))
        for levels in SUPPORTED_LEVELS:
            btn = tk.Button(
                controls,
                text=str(levels),
                font=self.body_font,
                bd=1,
                relief="solid",
                padx=10,
                pady=4,
                cursor="hand2",
                command=lambda value=levels: self.set_levels(value),
            )
            btn.pack(side="left", padx=(8, 0))
            self.level_buttons[levels] = btn

        tk.Button(
            controls,
            text="重置",
            font=self.small_font,
            bd=1,
            relief="solid",
            padx=10,
            pady=4,
            bg=WHITE,
            fg=MUTED_GRAY,
            activebackground=LIGHT_GRAY,
            command=self.reset,
        ).pack(side="right")

        # Main visual region
        main = tk.Frame(self.root, bg=WHITE)
        main.pack(pady=(4, 4))

        left = tk.Frame(main, bg=WHITE)
        left.grid(row=0, column=0, padx=(0, 26))
        tk.Label(left, text="原图 + 采样网格", font=self.body_bold, bg=WHITE, fg=BODY_BLACK).pack(pady=(0, 6))
        self.original_canvas = tk.Canvas(
            left,
            width=self.canvas_size,
            height=self.canvas_size,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground=GRID_GRAY,
            cursor="crosshair",
        )
        self.original_canvas.pack()
        self.original_canvas.create_image(0, 0, anchor="nw", image=self.photo, tags="image")
        self.original_canvas.bind("<Button-1>", self.on_canvas_click)

        middle = tk.Frame(main, bg=WHITE, width=100)
        middle.grid(row=0, column=1, padx=0)
        middle.grid_propagate(False)
        tk.Label(middle, text="", bg=WHITE).pack(pady=95)
        tk.Label(
            middle,
            text="采样\n+\n量化",
            font=(self.font_family, 18, "bold"),
            fg=ACCENT_VIOLET,
            bg=WHITE,
            justify="center",
        ).pack()
        tk.Label(
            middle,
            text="→",
            font=(self.font_family, 30, "bold"),
            fg=ACCENT_VIOLET,
            bg=WHITE,
        ).pack(pady=(3, 0))

        right = tk.Frame(main, bg=WHITE)
        right.grid(row=0, column=2, padx=(26, 0))
        tk.Label(right, text="数字图像", font=self.body_bold, bg=WHITE, fg=BODY_BLACK).pack(pady=(0, 6))
        self.digital_canvas = tk.Canvas(
            right,
            width=self.canvas_size,
            height=self.canvas_size,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground=GRID_GRAY,
            cursor="crosshair",
        )
        self.digital_canvas.pack()
        self.digital_canvas.bind("<Button-1>", self.on_canvas_click)

        # Explanation / inspector strip
        sep = tk.Frame(self.root, bg=FRAME_VIOLET, height=2)
        sep.pack(fill="x", padx=24, pady=(8, 6))

        info = tk.Frame(self.root, bg=WHITE)
        info.pack(fill="x", padx=28, pady=(0, 8))
        info.grid_columnconfigure(0, weight=1)
        info.grid_columnconfigure(1, weight=1)
        if not self.compact_layout:
            info.grid_columnconfigure(2, weight=1)

        self.cell_label = tk.Label(info, text="", font=self.body_bold, bg=WHITE, fg=BODY_BLACK, anchor="w")
        self.sample_label = tk.Label(info, text="", font=self.body_font, bg=WHITE, fg=BODY_BLACK, anchor="w")
        self.quant_label = tk.Label(info, text="", font=self.body_font, bg=WHITE, fg=BODY_BLACK, anchor="w")
        self.code_label = tk.Label(info, text="", font=self.code_font, bg=WHITE, fg=ACCENT_VIOLET, anchor="w")
        self.data_label = tk.Label(info, text="", font=self.body_font, bg=WHITE, fg=BODY_BLACK, anchor="w")
        self.state_label = tk.Label(info, text="", font=self.small_font, bg=WHITE, fg=MUTED_GRAY, anchor="w")

        if self.compact_layout:
            self.cell_label.grid(row=0, column=0, sticky="w")
            self.quant_label.grid(row=0, column=1, sticky="w", padx=(18, 0))
            self.sample_label.grid(row=1, column=0, sticky="w", pady=(3, 0))
            self.code_label.grid(row=1, column=1, sticky="w", padx=(18, 0), pady=(3, 0))
            self.data_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 0))
            self.state_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(2, 0))
        else:
            self.cell_label.grid(row=0, column=0, sticky="w")
            self.sample_label.grid(row=1, column=0, sticky="w", pady=(3, 0))
            self.quant_label.grid(row=0, column=1, sticky="w", padx=(24, 0))
            self.code_label.grid(row=1, column=1, sticky="w", padx=(24, 0), pady=(3, 0))
            self.data_label.grid(row=0, column=2, sticky="w", padx=(24, 0))
            self.state_label.grid(row=1, column=2, sticky="w", padx=(24, 0), pady=(3, 0))

        # Bottom rail
        tk.Frame(self.root, bg=FRAME_VIOLET, height=7).pack(fill="x", side="bottom")

    def _bind_keys(self) -> None:
        # 1..4 switch sampling grid; Q/W/E/R/T switch levels.
        grid_keys = {"1": 8, "2": 16, "3": 32, "4": 64}
        level_keys = {"q": 2, "w": 4, "e": 6, "r": 16, "t": 256}
        for key, value in grid_keys.items():
            self.root.bind(key, lambda event, v=value: self.set_grid(v))
        for key, value in level_keys.items():
            self.root.bind(key, lambda event, v=value: self.set_levels(v))
        self.root.bind("<Control-r>", lambda event: self.reset())

    def reset(self) -> None:
        self.grid_n = DEFAULT_GRID
        self.levels = DEFAULT_LEVELS
        self.selected_row = 1
        self.selected_col = 2
        self.refresh_all()

    def set_grid(self, n: int) -> None:
        if n == self.grid_n:
            return
        # Preserve roughly the same spatial location when grid density changes.
        y_ratio = (self.selected_row + 0.5) / self.grid_n
        x_ratio = (self.selected_col + 0.5) / self.grid_n
        self.grid_n = n
        self.selected_row = min(n - 1, max(0, int(y_ratio * n)))
        self.selected_col = min(n - 1, max(0, int(x_ratio * n)))
        self.refresh_all()

    def set_levels(self, levels: int) -> None:
        if levels == self.levels:
            return
        self.levels = levels
        self.refresh_all()

    def on_canvas_click(self, event: tk.Event) -> None:
        cell = self.canvas_size / self.grid_n
        col = min(self.grid_n - 1, max(0, int(event.x / cell)))
        row = min(self.grid_n - 1, max(0, int(event.y / cell)))
        self.selected_row = row
        self.selected_col = col
        self.refresh_selection()

    def _rgb_for_cell(self, row: int, col: int) -> list[int]:
        return self.data["grids"][str(self.grid_n)][row][col]

    def refresh_all(self) -> None:
        self._refresh_buttons()
        self.draw_original_grid()
        self.draw_digital()
        self.refresh_selection()

    def _refresh_buttons(self) -> None:
        for n, btn in self.grid_buttons.items():
            active = n == self.grid_n
            btn.configure(
                bg=ACCENT_VIOLET if active else WHITE,
                fg=WHITE if active else BODY_BLACK,
                activebackground=ACCENT_VIOLET if active else LIGHT_GRAY,
                activeforeground=WHITE if active else BODY_BLACK,
            )
        for levels, btn in self.level_buttons.items():
            active = levels == self.levels
            btn.configure(
                bg=ACCENT_VIOLET if active else WHITE,
                fg=WHITE if active else BODY_BLACK,
                activebackground=ACCENT_VIOLET if active else LIGHT_GRAY,
                activeforeground=WHITE if active else BODY_BLACK,
            )

    def draw_original_grid(self) -> None:
        self.original_canvas.delete("grid")
        cell = self.canvas_size / self.grid_n
        # Draw only the sampling lattice; image itself remains unchanged.
        for i in range(1, self.grid_n):
            p = i * cell
            self.original_canvas.create_line(p, 0, p, self.canvas_size, fill=GRID_GRAY, width=1, tags="grid")
            self.original_canvas.create_line(0, p, self.canvas_size, p, fill=GRID_GRAY, width=1, tags="grid")
        self.original_canvas.tag_raise("grid")

    def draw_digital(self) -> None:
        self.digital_canvas.delete("all")
        rows = self.data["grids"][str(self.grid_n)]
        cell = self.canvas_size / self.grid_n
        for r, row in enumerate(rows):
            for c, rgb in enumerate(row):
                gray = rgb_to_gray(rgb)
                _, q = quantize_gray(gray, self.levels)
                color = f"#{q:02x}{q:02x}{q:02x}"
                x0 = c * cell
                y0 = r * cell
                x1 = (c + 1) * cell
                y1 = (r + 1) * cell
                self.digital_canvas.create_rectangle(
                    x0,
                    y0,
                    x1,
                    y1,
                    fill=color,
                    outline=GRID_GRAY,
                    width=1,
                    tags="cell",
                )

    def refresh_selection(self) -> None:
        self._draw_focus(self.original_canvas)
        self._draw_focus(self.digital_canvas)

        rgb = self._rgb_for_cell(self.selected_row, self.selected_col)
        gray = rgb_to_gray(rgb)
        idx, q = quantize_gray(gray, self.levels)
        bits = bits_for_levels(self.levels)
        cw = codeword(idx, self.levels)
        total_bits = self.grid_n * self.grid_n * bits
        states = 2 ** bits

        self.cell_label.configure(
            text=f"选中：第 {self.selected_row + 1} 行，第 {self.selected_col + 1} 列"
        )
        self.sample_label.configure(
            text=f"样本平均 RGB = ({rgb[0]}, {rgb[1]}, {rgb[2]})；灰度 ≈ {gray}"
        )
        self.quant_label.configure(
            text=f"量化：{gray} → 颜色编号 {idx}（灰度值 {q}）"
        )
        self.code_label.configure(text=f"编码：{idx} → {cw}")
        self.data_label.configure(
            text=f"位深度 {bits} bit / 像素；总计 {total_bits:,} bit = {format_bytes(total_bits)}"
        )
        if self.levels == states:
            state_text = f"{bits} bit 可表示 {states} 种状态，全部使用。"
        else:
            state_text = f"{bits} bit 可表示 {states} 种状态，本实验使用 {self.levels} 种。"
        self.state_label.configure(text=state_text)

    def _draw_focus(self, canvas: tk.Canvas) -> None:
        canvas.delete("focus")
        cell = self.canvas_size / self.grid_n
        x0 = self.selected_col * cell
        y0 = self.selected_row * cell
        x1 = (self.selected_col + 1) * cell
        y1 = (self.selected_row + 1) * cell
        canvas.create_rectangle(
            x0 + 1,
            y0 + 1,
            x1 - 1,
            y1 - 1,
            outline=FOCUS_RED,
            width=3,
            tags="focus",
        )
        canvas.tag_raise("focus")


def main() -> None:
    if "--self-test" in sys.argv:
        self_test()
        return

    # Fail early with clear messages if deployment files are incomplete.
    if not IMAGE_PATH.exists() or not SMALL_IMAGE_PATH.exists() or not DATA_PATH.exists():
        missing = [p.name for p in (IMAGE_PATH, SMALL_IMAGE_PATH, DATA_PATH) if not p.exists()]
        raise SystemExit("缺少演示文件：" + ", ".join(missing))

    root = tk.Tk()
    DigitizationDemo(root)
    root.mainloop()


if __name__ == "__main__":
    main()
