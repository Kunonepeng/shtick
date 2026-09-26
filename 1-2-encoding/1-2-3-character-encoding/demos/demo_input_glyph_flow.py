"""Q9: Visualize English vs Chinese input from keyboard to screen.

Run:
    python demo_input_glyph_flow.py

No third-party packages are required. If Tkinter is unavailable, the script
falls back to a text-mode comparison.
"""

ENGLISH = [
    ("键盘输入", "按下 A"),
    ("字符确定", "直接确定字符 A"),
    ("输入法", "无需 IME"),
    ("字符身份", "A / U+0041"),
    ("字形信息", "font → glyph A"),
    ("显示", "pixels → A"),
]

CHINESE = [
    ("键盘输入", "按下 n、i"),
    ("输入层", "输入码 ni"),
    ("输入法", "IME 候选：你 / 尼 / 泥 / …"),
    ("字符身份", "选择“你” / U+4F60"),
    ("字形信息", "font → glyph 你"),
    ("显示", "pixels → 你"),
]


def text_mode() -> None:
    print("英文字符 A".ljust(34) + "中文字符 你")
    print("=" * 72)
    for left, right in zip(ENGLISH, CHINESE):
        l = f"{left[0]}：{left[1]}"
        r = f"{right[0]}：{right[1]}"
        print(l.ljust(34) + r)
    print("\n关键区别：")
    print("1. 英文 A 通常可由按键直接确定字符。")
    print("2. 中文“你”通常先输入输入码 ni，再由 IME 确定字符。")
    print("3. 两者在显示前都需要字形信息（font / glyph）。")


def gui_mode() -> None:
    import tkinter as tk

    root = tk.Tk()
    root.title("Q9：英文字符和汉字，从键盘到屏幕有什么不同？")
    root.geometry("1200x760")
    root.minsize(960, 650)

    canvas = tk.Canvas(root, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    state = {"step": 0}
    max_step = len(ENGLISH) - 1

    def draw() -> None:
        canvas.delete("all")
        w = max(canvas.winfo_width(), 960)
        h = max(canvas.winfo_height(), 650)

        canvas.create_rectangle(0, 0, w, 8, fill="#6251B1", outline="")
        canvas.create_rectangle(0, h - 8, w, h, fill="#6251B1", outline="")

        canvas.create_text(
            55, 52,
            anchor="w",
            text="英文字符和汉字，从键盘到屏幕有什么不同？",
            font=("Arial", 25, "bold"),
            fill="#262626",
        )

        left_x = w * 0.28
        right_x = w * 0.72
        canvas.create_text(left_x, 112, text="英文字符 A", font=("Arial", 20, "bold"))
        canvas.create_text(right_x, 112, text="中文字符 你", font=("Arial", 20, "bold"))

        start_y = 175
        gap = 72
        box_w = min(390, w * 0.34)
        box_h = 48

        for i, (en, zh) in enumerate(zip(ENGLISH, CHINESE)):
            y = start_y + i * gap
            active = i == state["step"]
            outline = "#FF0000" if active else "#8C64E1"
            width = 3 if active else 2

            for x, item in ((left_x, en), (right_x, zh)):
                canvas.create_rectangle(
                    x - box_w / 2, y - box_h / 2,
                    x + box_w / 2, y + box_h / 2,
                    outline=outline, width=width, fill="white",
                )
                label = f"{item[0]}：{item[1]}"
                canvas.create_text(
                    x, y, text=label, width=box_w - 24,
                    font=("Arial", 15, "bold" if active else "normal"),
                    fill="#262626",
                )

            if i < max_step:
                next_y = start_y + (i + 1) * gap
                for x in (left_x, right_x):
                    canvas.create_line(
                        x, y + box_h / 2,
                        x, next_y - box_h / 2,
                        arrow=tk.LAST, fill="#6251B1", width=2,
                    )

        canvas.create_text(
            w / 2, h - 105,
            text="中文输入多了“输入码 → IME”这一步；英文和中文最终都需要“字形信息 → 像素”才能显示。",
            font=("Arial", 16, "bold"),
            fill="#262626",
        )

        canvas.create_text(
            55, h - 48,
            anchor="w",
            text=f"Step {state['step'] + 1}/{max_step + 1}    Space / →：下一步    ←：上一步    R：重置",
            font=("Arial", 13),
            fill="#808080",
        )

    def next_step(event=None):
        state["step"] = min(max_step, state["step"] + 1)
        draw()

    def prev_step(event=None):
        state["step"] = max(0, state["step"] - 1)
        draw()

    def reset(event=None):
        state["step"] = 0
        draw()

    root.bind("<space>", next_step)
    root.bind("<Right>", next_step)
    root.bind("<Left>", prev_step)
    root.bind("r", reset)
    root.bind("R", reset)
    root.bind("<Configure>", lambda event: draw())

    draw()
    root.mainloop()


if __name__ == "__main__":
    try:
        gui_mode()
    except Exception as exc:
        print(f"GUI unavailable ({exc}). Switching to text mode.\n")
        text_mode()
