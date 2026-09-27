#!/usr/bin/env python3
"""Build the complete classroom companion package for v6-2.

Production deck baseline:
    1-2-encoding/1-2-3-character-encoding/
    1-2-3-character-encoding-v6-2.pptx

Generated artifacts:
- teacher-guide.qmd
- demo-lab-teacher.ipynb
- demo-lab-student.ipynb
- controlled WinHex lab files
- Unicode/UTF fallback demo
- package preflight script
- generated-image prompt provenance
- editable Q14/exit-ticket source
- printable Q14/exit-ticket PDF
"""

from pathlib import Path
import textwrap

import nbformat as nbf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import mm

REPO = Path(__file__).resolve().parents[1]
LESSON = REPO / "1-2-encoding" / "1-2-3-character-encoding"
ASSETS = LESSON / "assets"
GENERATED = ASSETS / "generated"
DEMOS = LESSON / "demos"
WORKSHEETS = LESSON / "worksheets"

for p in [ASSETS, GENERATED, DEMOS, WORKSHEETS]:
    p.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# Classroom runbook
# ---------------------------------------------------------------------

TEACHER_GUIDE = r'''---
title: "1-2-3 字符编码：课堂执行指南"
subtitle: "Baseline: 1-2-3-character-encoding-v6-2.pptx"
format:
  html:
    toc: true
    toc-depth: 3
    toc-title: "课堂导航"
---

# 0. 使用基线

本指南假定正式课堂课件为：

\`\`\`text
1-2-3-character-encoding-v6-2.pptx
\`\`\`

课堂展示以 WPS / PowerPoint 为主，JupyterLab 与 WinHex 用于提供可操作证据。

核心模型：

\`\`\`text
输入并显示：
键盘输入 → 输入码 / IME → 字符 / code point → 字体映射 → glyph → pixels

保存、传输并读取：
字符 / code point → encode → bytes → decode → 字符 / code point
→ 字体映射 → glyph → pixels
\`\`\`

## v6-2 兼容说明

\`v6-2\` 中“中文编码标准为什么不断扩展？”位于 Unicode / UTF 之前。当前
\`course-design.qmd\` 把 Unicode / UTF 放在中文编码标准扩展之前。**本指南按 v6-2
的实际页序上课**，不在课堂中临时重排。

另一个差异是：v6-2 的 Unicode 页面以“中 / U+4E2D”为主要视觉样本，而当前课程设计以
“你 / U+4F60”为主要锚点。Notebook 同时保留“中”和“你”：先用“中”衔接 PPT，再用“你”
作为迁移验证。

---

# 1. 课前准备

1. 用 WPS 打开 \`1-2-3-character-encoding-v6-2.pptx\`，检查字体、换行和 Speaker Notes。
2. 打开 JupyterLab：
   - \`demo-lab-teacher.ipynb\`
   - \`demo-lab-student.ipynb\`
3. 运行：

\`\`\`bash
python 1-2-encoding/1-2-3-character-encoding/demos/create_lab_files.py
python 1-2-encoding/1-2-3-character-encoding/demos/check_classroom_package.py
\`\`\`

4. 用 WinHex 分别打开：
   - \`assets/gb2312-lab.txt\`
   - \`assets/utf8-lab.txt\`
5. 清除 Notebook 已运行输出，避免提前泄露后续答案。

---

# 2. 课堂切换地图

| PPT 页 | 问题 / 环节 | 建议工具 | 教师动作 |
|---|---|---|---|
| 2–3 | Q0 乱码悬念 | PPT；Notebook Q0 可选 | 先猜故障位置，不解释 bytes |
| 4–8 | Q1-A 私人编码表 | PPT + 纸笔活动 | 只交换 bit 串，不交换映射表 |
| 9–13 | Q1-B 字符集容量 | PPT | 先确定字符集，再谈映射 |
| 14–17 | Q2 ASCII 查表 | PPT | 让学生真正查表 |
| 18–19 | Q3 7 bit 与 1 byte | Notebook Q3 | 先看 7-bit，再看 8-bit 存储 |
| 20–21 | Q4 ASCII 规律 | PPT | 用差值和区间形成规律 |
| 22–24 | Q5 设计汉字编码 | PPT | 迁移“字符集 + 映射”思想 |
| 25–26 | Q6 文件中的汉字 | WinHex / Notebook Q6 | 观察真实 bytes |
| 27–28 | Q7 国标码与机内码 | WinHex / Notebook Q6–Q7 | 比较 \`56 50\` 与 \`D6 D0\` |
| 29–30 | Q8 汉字总是 2 bytes 吗 | Notebook Q8 | 对比 GB2312 与 UTF-8 |
| 31–32 | Q9 输入到显示 | PPT / Notebook Q9 可选 | 强调 IME 在字符确定之前 |
| 33–34 | 中文标准扩展 | PPT | 只讲标准扩展逻辑 |
| 35–36 | Unicode 字符身份 | Notebook Q10 | 先用“中”接 PPT，再用“你”迁移 |
| 37–38 | 码位与 bytes | Notebook Q11-A | 同一码位，不同 UTF 表示 |
| 39–40 | UTF-8/16/32 | Notebook Q11-B / \`demo_unicode_utf.py\` | **补足 code unit 概念** |
| 41–42 | 乱码揭秘 | Notebook Q13 | 同一批 bytes，不同 decode |
| 43–44 | 重建两条路径 | worksheet | 学生先独立填 |
| 45 | 三句话解释字符编码 | PPT + worksheet | 出口检查 |

---

# 3. 关键演示

## ASCII

\`A\`：

\`\`\`text
7-bit: 1000001
1 byte: 01000001
\`\`\`

结论：字符值没有变化，只是在一个 byte 中保存时左侧补 0。

## WinHex / GB2312

样本文字：

\`\`\`text
A中B国C文
\`\`\`

预期 bytes：

\`\`\`text
GB2312: 41 D6 D0 42 B9 FA 43 CE C4
UTF-8 : 41 E4 B8 AD 42 E5 9B BD 43 E6 96 87
\`\`\`

Q7：

\`\`\`text
“中”国标码：56 50
传统机内码：D6 D0
\`\`\`

只在传统 GB2312 双字节机内码模型下解释“每个 byte + 0x80”。

## 输入 / IME

\`\`\`text
n、i → 输入码 ni → IME 选“你” → 字符确定 → glyph → pixels
\`\`\`

不要把文件 \`encode → decode\` 强行塞进即时键盘显示路径。

## Unicode

先衔接 v6-2：

\`\`\`text
中 → U+4E2D
\`\`\`

再迁移：

\`\`\`text
你 → U+4F60
\`\`\`

code point 回答“这是哪个字符”，不是固定的文件 bytes。

## UTF-8 / UTF-16 / UTF-32

Q11-B 必须补足：

\`\`\`text
UTF-8  → 8-bit code unit
UTF-16 → 16-bit code unit
UTF-32 → 32-bit code unit
\`\`\`

再用 \`U+1F600\` 反驳“UTF-16 每个字符永远 2 bytes”。

## 乱码

\`\`\`text
E4 BD A0 E5 A5 BD

UTF-8 decode → 你好
GBK decode   → 浣犲ソ
\`\`\`

核心追问：**bytes 有没有变？**

---

# 4. Q14 学生任务

发放：

\`\`\`text
worksheets/character-encoding-exit-ticket.pdf
\`\`\`

学生先独立重建：

\`\`\`text
输入并显示：
键盘输入 → 输入码 / IME → 字符 / code point
→ 字体映射 → glyph → pixels

保存并读取：
字符 / code point → encode → bytes → decode
→ 字符 / code point → 字体映射 → glyph → pixels
\`\`\`

不要先投影完整答案。

---

# 5. 故障替代

## WinHex 不可用

切换 \`demo-lab-student.ipynb → Q6–Q7\`。

## JupyterLab 不可用

直接使用 PPT 已准备的固定证据，不临时下载工具。

## 时间不足

优先保留：

\`\`\`text
Q0 → Q1 → Q3 → Q6/Q7 → Q8 → Q9 → Unicode/UTF → 乱码 → Q14
\`\`\`

ASCII 规律与标准时间线可以压缩，但不要删掉 Unicode/UTF、乱码诊断与最终重建。
'''
(LESSON / "teacher-guide.qmd").write_text(TEACHER_GUIDE, encoding="utf-8")

# ---------------------------------------------------------------------
# Image prompt provenance
# ---------------------------------------------------------------------

IMAGE_PROMPTS = r'''# Generated Image Prompts — Character Encoding v6-2

**Deck baseline:** \`1-2-3-character-encoding-v6-2.pptx\`

> **Generated images illustrate; native diagrams and real screenshots prove.**

## Provenance status

The exact historical prompts that produced the illustrations already embedded in v6-2 are not available in the project record.
The prompts below are the **canonical regeneration prompts** from this point forward.

If an image is regenerated and accepted for production, preserve the exact prompt that produced it and change its status to
\`production prompt recorded\`.

---

## IMG-01 — Mojibake opening

**Slide / Q:** slide 2 / Q0  
**Teaching purpose:** Create curiosity about why expected text can appear garbled without implying the technical cause.  
**Slide role:** cognitive-conflict opening  
**Intended placement:** right-side hero illustration  
**Aspect ratio:** wide landscape

### Exact canonical regeneration prompt

Create a clean classroom teaching illustration for a high-school information technology lesson about character encoding.

Teaching purpose:
Make students immediately notice that expected text on a computer can appear unreadable or garbled, and make them want to explain why, without revealing the encoding mechanism.

Subject / scene:
A high-school student is looking at a desktop computer screen. The student expected normal Chinese text, but the screen visually suggests garbled or unreadable text. The student looks curious and mildly puzzled, not upset.

Composition:
Place the student and computer on the right half of the frame.
Make the computer display the main visual focus.
Leave generous clean white negative space on the left and upper-left for a PowerPoint question title.
Wide 16:9-compatible composition.

Visual style:
clean modern educational illustration
white or very light neutral background
minimal visual clutter
serious but friendly high-school classroom tone
clear silhouettes
subtle depth
consistent with a white technical teaching deck

Important constraints:
no readable Chinese sentence
no exact mojibake string
no binary strings
no byte values
no arrows
no explanatory labels
no conclusions
no logos
no watermark
no decorative border
no gradient background
no corporate infographic cards

Do not invent technical evidence.
The real mojibake string and all precise labels will be added later as native PowerPoint text.

### Post-generation edits

- crop to preserve left-side title space;
- add the real question and exact mojibake string as native PPT text;
- do not bake technical values into the image.

---

## IMG-02 — Secret-code exchange

**Slide / Q:** slide 4 / Q1-A  
**Teaching purpose:** Show two students attempting to exchange a coded message while each holds a private mapping table.  
**Slide role:** activity setup / analogy  
**Intended placement:** centered two-person illustration with open middle space  
**Aspect ratio:** wide landscape

### Exact canonical regeneration prompt

Create a classroom teaching illustration for a high-school information technology lesson about character encoding.

Teaching purpose:
Show that two students can both use short binary codes yet still fail to understand each other if their character-to-code mappings are different.

Subject / scene:
Two high-school students sit facing each other across a desk.
Each student has a small private codebook or mapping sheet.
The sheets should visually suggest that both students are using the same small set of letters but have organized the mappings differently.

Composition:
Place one student on the left and one on the right.
Leave a large clean empty region in the center for the teacher to add a binary message later in PowerPoint.
Keep the private codebook sheets visible but do not render readable technical mappings.
Wide 16:9-compatible composition.

Visual style:
clean modern educational illustration
white background
minimal visual clutter
friendly but serious classroom tone
simple geometry
clear visual separation between the two students
consistent with a white technical teaching deck

Important constraints:
no readable code tables
no binary strings
no explanatory text
no Chinese labels
no arrows
no legends
no conclusions
no logos
no watermark
no decorative borders
no gradient background
no corporate infographic cards

Precise mappings and binary values will be added later as native PowerPoint objects.

### Post-generation edits

- preserve the empty center region;
- add actual code table and bit string with native PPT objects;
- use red/violet focus marks only in PPT, not in the generated image.

---

## Future record template

\`\`\`markdown
## IMG-XX — <short name>

**Slide / Q:**  
**Teaching purpose:**  
**Slide role:**  
**Intended placement:**  
**Aspect ratio:**  
**Status:** production prompt recorded

### Exact prompt

<PASTE THE COMPLETE PROMPT VERBATIM>

### Post-generation edits

- crop:
- background removal:
- native PPT labels added:
- other:
\`\`\`
'''
(GENERATED / "image-prompts.md").write_text(IMAGE_PROMPTS, encoding="utf-8")

# ---------------------------------------------------------------------
# Controlled lab assets
# ---------------------------------------------------------------------

TEXT = "A中B国C文"
(ASSETS / "gb2312-lab.txt").write_bytes(TEXT.encode("gb2312"))
(ASSETS / "utf8-lab.txt").write_bytes(TEXT.encode("utf-8"))

ASSET_README = r'''# Encoding lab assets

These files support \`1-2-3-character-encoding-v6-2.pptx\`.

Generate / regenerate:

\`\`\`bash
python 1-2-encoding/1-2-3-character-encoding/demos/create_lab_files.py
\`\`\`

Both represent:

\`\`\`text
A中B国C文
\`\`\`

Expected bytes:

\`\`\`text
gb2312-lab.txt
41 D6 D0 42 B9 FA 43 CE C4

utf8-lab.txt
41 E4 B8 AD 42 E5 9B BD 43 E6 96 87
\`\`\`

Generated-image provenance:

\`\`\`text
assets/generated/image-prompts.md
\`\`\`
'''
(ASSETS / "README.md").write_text(ASSET_README, encoding="utf-8")

# ---------------------------------------------------------------------
# Demo scripts
# ---------------------------------------------------------------------

CREATE_LAB = '''"""Generate controlled text files for the WinHex character-encoding lab."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

TEXT = "A中B国C文"
(ASSETS / "gb2312-lab.txt").write_bytes(TEXT.encode("gb2312"))
(ASSETS / "utf8-lab.txt").write_bytes(TEXT.encode("utf-8"))

print("generated:")
print(ASSETS / "gb2312-lab.txt")
print(ASSETS / "utf8-lab.txt")
'''
(DEMOS / "create_lab_files.py").write_text(CREATE_LAB, encoding="utf-8")

UNICODE_DEMO = '''"""Q10-Q11 fallback demo for v6-2. No third-party packages required."""

SAMPLES = [
    ("A", "A"),
    ("中", "中"),
    ("你", "你"),
    ("U+1F600", chr(0x1F600)),
]

def hex_bytes(text, encoding):
    return text.encode(encoding).hex(" ").upper()

def utf16be_units(text):
    raw = text.encode("utf-16-be")
    return [raw[i:i+2].hex().upper() for i in range(0, len(raw), 2)]

def utf32be_units(text):
    raw = text.encode("utf-32-be")
    return [raw[i:i+4].hex().upper() for i in range(0, len(raw), 4)]

print("=== Unicode character identity ===")
for label, ch in SAMPLES:
    print(f"{label:<10} -> U+{ord(ch):04X}")

print("\\n=== Same code point, different UTF bytes ===")
for label, ch in SAMPLES:
    print(f"\\n{label}  U+{ord(ch):04X}")
    print("  UTF-8    :", hex_bytes(ch, "utf-8"))
    print("  UTF-16BE :", hex_bytes(ch, "utf-16-be"))
    print("  UTF-32BE :", hex_bytes(ch, "utf-32-be"))

print("\\n=== Code-unit view ===")
print("UTF-8   : 8-bit code units")
print("UTF-16  : 16-bit code units")
print("UTF-32  : 32-bit code units")
print()
print(f"{'sample':<10} {'code point':<11} {'UTF-8 units':<18} {'UTF-16 units':<18} {'UTF-32 units'}")
print("-" * 88)
for label, ch in SAMPLES:
    u8 = [f"{b:02X}" for b in ch.encode("utf-8")]
    u16 = utf16be_units(ch)
    u32 = utf32be_units(ch)
    print(f"{label:<10} U+{ord(ch):04X}      {' '.join(u8):<18} {' '.join(u16):<18} {' '.join(u32)}")

print("\\nKey observation:")
print("- U+1F600 uses TWO 16-bit UTF-16 code units: D83D DE00.")
print("- Therefore UTF-16 does not mean 'every character is 16 bits'.")
'''
(DEMOS / "demo_unicode_utf.py").write_text(UNICODE_DEMO, encoding="utf-8")

PREFLIGHT = '''"""Pre-class verification for the v6-2 classroom package."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

EXPECTED = {
    "gb2312-lab.txt": "41 D6 D0 42 B9 FA 43 CE C4",
    "utf8-lab.txt": "41 E4 B8 AD 42 E5 9B BD 43 E6 96 87",
}

required = [
    ROOT / "1-2-3-character-encoding-v6-2.pptx",
    ROOT / "demo-lab-teacher.ipynb",
    ROOT / "demo-lab-student.ipynb",
    ROOT / "teacher-guide.qmd",
    ROOT / "worksheets" / "character-encoding-exit-ticket.pdf",
]

failures = []
print("Python:", sys.version.split()[0])

for path in required:
    if path.exists():
        print("OK  ", path.relative_to(ROOT))
    else:
        print("MISS", path.relative_to(ROOT))
        failures.append(f"missing {path.name}")

for name, expected in EXPECTED.items():
    path = ASSETS / name
    if not path.exists():
        print("MISS", path.relative_to(ROOT))
        failures.append(f"missing {name}")
        continue
    actual = path.read_bytes().hex(" ").upper()
    if actual == expected:
        print("OK  ", name, actual)
    else:
        print("FAIL", name, actual)
        failures.append(f"wrong bytes in {name}")

checks = [
    ("ASCII A", "A".encode("ascii").hex().upper(), "41"),
    ("GB2312 中", "中".encode("gb2312").hex().upper(), "D6D0"),
    ("UTF-8 你", "你".encode("utf-8").hex().upper(), "E4BDA0"),
    ("UTF-16BE 你", "你".encode("utf-16-be").hex().upper(), "4F60"),
    ("UTF-32BE 你", "你".encode("utf-32-be").hex().upper(), "00004F60"),
    ("UTF-16BE U+1F600", chr(0x1F600).encode("utf-16-be").hex().upper(), "D83DDE00"),
]
for label, actual, expected in checks:
    if actual == expected:
        print("OK  ", label, actual)
    else:
        print("FAIL", label, actual, "expected", expected)
        failures.append(label)

if failures:
    print("\\nCHECKS FAILED:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("\\nALL CHECKS PASSED")
'''
(DEMOS / "check_classroom_package.py").write_text(PREFLIGHT, encoding="utf-8")

# ---------------------------------------------------------------------
# Notebooks
# ---------------------------------------------------------------------

def md(s):
    return nbf.v4.new_markdown_cell(textwrap.dedent(s).strip())

def code(s):
    return nbf.v4.new_code_cell(textwrap.dedent(s).strip())

COMMON_Q3 = """
ch = "A"
code_value = ord(ch)
ascii_byte = ch.encode("ascii")[0]
print(f"Character        : {ch}")
print(f"Decimal code     : {code_value}")
print(f"Hex code         : 0x{code_value:02X}")
print(f"ASCII 7-bit code : {code_value:07b}")
print(f"Stored in 1 byte : {ascii_byte:08b}")
print(f"MSB              : {(ascii_byte >> 7) & 1}")
"""

COMMON_GB = """
text = "A中B国C文"
def bits(byte): return f"{byte:08b}"
def msb(byte): return (byte >> 7) & 1

print("GB2312 bytes:", text.encode("gb2312").hex(" ").upper())
print()
print(f"{'字符':<4}{'Hex':<10}{'Bytes':<8}{'Binary':<22}{'MSB'}")
print("-" * 60)
for ch in text:
    raw = ch.encode("gb2312")
    hex_bytes = " ".join(f"{b:02X}" for b in raw)
    binary = " ".join(bits(b) for b in raw)
    msbs = " ".join(str(msb(b)) for b in raw)
    print(f"{ch:<4}{hex_bytes:<10}{len(raw):<8}{binary:<22}{msbs}")
"""

COMMON_Q9 = """
from IPython.display import display, HTML

english = [
    ("键盘输入", "按下 A"),
    ("字符确定", "字符 A"),
    ("字形信息", "font → glyph A"),
    ("显示", "pixels → A"),
]
chinese = [
    ("键盘输入", "按下 n、i"),
    ("输入码", "ni"),
    ("输入法", "IME → 选择“你”"),
    ("字符确定", "字符“你”"),
    ("字形信息", "font → glyph 你"),
    ("显示", "pixels → 你"),
]

def flow(title, items, accent):
    blocks = []
    for label, value in items:
        blocks.append(
            f'<div style="border:2px solid {accent};padding:9px 12px;margin:6px 0;background:white">'
            f'<div style="font-size:13px;color:#666">{label}</div>'
            f'<div style="font-size:18px;font-weight:700">{value}</div></div>'
        )
    return f'<div style="width:46%"><h3>{title}</h3>' + '<div style="text-align:center">↓</div>'.join(blocks) + '</div>'

display(HTML(
    '<div style="display:flex;gap:28px;justify-content:space-between">'
    + flow("英文字符 A", english, "#6251B1")
    + flow("中文字符 你", chinese, "#FF0000")
    + '</div>'
))
"""

COMMON_Q11A = """
for ch in ["中", "你"]:
    print(f"Character : {ch}")
    print(f"Code point: U+{ord(ch):04X}")
    for label, encoding in [
        ("UTF-8", "utf-8"),
        ("UTF-16BE", "utf-16-be"),
        ("UTF-32BE", "utf-32-be"),
    ]:
        print(f"  {label:<9} {ch.encode(encoding).hex(' ').upper()}")
    print()
"""

COMMON_Q11B = """
samples = [("A", "A"), ("你", "你"), ("U+1F600", chr(0x1F600))]

def utf16_units(ch):
    raw = ch.encode("utf-16-be")
    return [raw[i:i+2].hex().upper() for i in range(0, len(raw), 2)]

def utf32_units(ch):
    raw = ch.encode("utf-32-be")
    return [raw[i:i+4].hex().upper() for i in range(0, len(raw), 4)]

for label, ch in samples:
    print(f"{label:<10} U+{ord(ch):04X}")
    print("  UTF-8 bytes    :", ch.encode("utf-8").hex(" ").upper())
    print("  UTF-16BE units :", " ".join(utf16_units(ch)))
    print("  UTF-32BE unit  :", " ".join(utf32_units(ch)))
    print()
"""

teacher_cells = [
    md("""# 字符编码 · 教师演示实验

**课堂基线：** \`1-2-3-character-encoding-v6-2.pptx\`

v6-2 用“中 / U+4E2D”衔接 Unicode；当前课程设计用“你 / U+4F60”作为概念锚点。
课堂先接 PPT，再用“你”做迁移。"""),
    md("## 课前检查"),
    code("""import sys
print("Python:", sys.version.split()[0])
assert "A".encode("ascii") == b"A"
assert "中".encode("gb2312").hex().upper() == "D6D0"
assert "你".encode("utf-8").hex().upper() == "E4BDA0"
assert chr(0x1F600).encode("utf-16-be").hex().upper() == "D83DDE00"
print("Encoding checks: OK")"""),
    md("# Q0 乱码悬念\n只展示现象；完整机制留到 Q13。"),
    code("""text = "你好"
print("原文：", text)
raw = text.encode("utf-8")
print("乱码：", raw.decode("gbk"))"""),
    md("# Q3 ASCII：7 bit 与 1 byte"),
    code(COMMON_Q3),
    md("# Q6–Q7 GB2312 机内码\nWinHex 不稳定时使用；结论限于传统 GB2312 双字节模型。"),
    code(COMMON_GB + '\nprint("\\n国标码 56 50 → 传统机内码 D6 D0：每个 byte + 0x80")'),
    md("# Q8 同一个汉字：GB2312 vs UTF-8"),
    code("""ch = "中"
for encoding in ["gb2312", "utf-8"]:
    raw = ch.encode(encoding)
    print(f"{encoding:<8} bytes = {raw.hex(' ').upper():<10} length = {len(raw)}")"""),
    md("# Q9 英文输入与中文输入\n即时显示路径不强行加入文件 encode → decode。"),
    code(COMMON_Q9),
    md("# Q10 Unicode：怎样确认是同一个字符？"),
    code("""for ch in ["A", "中", "你"]:
    cp = ord(ch)
    print(f"{ch}  decimal={cp:<6}  hex=0x{cp:X}  Unicode=U+{cp:04X}")"""),
    md("**结论：** code point 解决“这是哪个字符”；bytes 与 glyph 是另外两层。"),
    md("# Q11-A 同一码位，文件 bytes 一定相同吗？"),
    code(COMMON_Q11A),
    md("# Q11-B 8、16、32 是每个字符的位数吗？\n重点：8 / 16 / 32 指 **code unit 宽度**。"),
    code('print("UTF-8  : 8-bit code units")\nprint("UTF-16 : 16-bit code units")\nprint("UTF-32 : 32-bit code units")\nprint()\n' + COMMON_Q11B),
    md("**技术注解：** U+1F600 在 UTF-16 中使用两个 16-bit code units：D83D DE00。课堂无需手算代理对。"),
    md("# Q13 乱码揭秘"),
    code("""text = "你好"
raw = text.encode("utf-8")
print("UTF-8 bytes       :", raw.hex(" ").upper())
print("按 UTF-8 正确解码 :", raw.decode("utf-8"))
print("按 GBK 错误解码   :", raw.decode("gbk"))"""),
    md("# Q14 两条路径重建\n切回 \`worksheets/character-encoding-exit-ticket.pdf\`，学生先独立完成。"),
]

student_cells = [
    md("""# 字符编码 · 学生演示实验

**课堂基线：** \`1-2-3-character-encoding-v6-2.pptx\`

只运行教师指定的单元格，不要提前运行后面的内容。"""),
    md("# Q0 乱码悬念\n先观察，不解释。"),
    code('print("原文：", "你好")\nprint("乱码：", "浣犲ソ")'),
    md("> 记录：错误可能发生在哪一层？"),
    md("# Q3 ASCII：7 bit 与 1 byte"),
    code(COMMON_Q3),
    md("> 思考：\`1000001\` 与 \`01000001\` 有什么关系？"),
    md("# Q6–Q7 GB2312 bytes 观察"),
    code(COMMON_GB),
    md("记录：ASCII 和 GB2312 汉字分别用了几个 bytes？MSB 有什么特征？比较 56 50 与 D6 D0。"),
    md("# Q8 同一个汉字：GB2312 vs UTF-8"),
    code("""ch = "中"
for encoding in ["gb2312", "utf-8"]:
    raw = ch.encode(encoding)
    print(f"{encoding:<8} bytes = {raw.hex(' ').upper():<10} length = {len(raw)}")"""),
    md("> 思考：同一个“中”，为什么 byte 数不同？"),
    md("# Q9 英文输入与中文输入"),
    code(COMMON_Q9),
    md("记录：中文输入比英文多了哪一层？字符确定以后为什么还需要字形信息？"),
    md("# Q10 为什么需要共同的字符身份？"),
    code('for ch in ["A", "中", "你"]:\n    print(f"{ch}  Unicode=U+{ord(ch):04X}")'),
    md("> 思考：U+XXXX 是文件 bytes 吗？"),
    md("# Q11-A 同一码位，文件 bytes 一定相同吗？"),
    code(COMMON_Q11A),
    md("> 记录：哪一项保持不变？哪一项随 UTF 形式改变？"),
    md("# Q11-B 8、16、32 是每个字符的位数吗？"),
    code(COMMON_Q11B),
    md("""记录：

1. U+1F600 在 UTF-16 中用了几个 16-bit 单元？
2. “UTF-16 = 每个字符固定 16 bit”成立吗？
3. 名称里的 8、16、32 更可能指什么？"""),
    md("# Q13 乱码揭秘"),
    code("""text = "你好"
raw = text.encode("utf-8")
print("UTF-8 bytes       :", raw.hex(" ").upper())
print("按 UTF-8 正确解码 :", raw.decode("utf-8"))
print("按 GBK 错误解码   :", raw.decode("gbk"))"""),
    md("> 记录：bytes 有没有改变？错误发生在哪一步？"),
    md("# Q14 两条路径重建\n暂停 Notebook，完成 worksheet。"),
]

def write_nb(cells, path, role):
    nb = nbf.v4.new_notebook(cells=cells)
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
        "shtick": {
            "production_deck": "1-2-3-character-encoding-v6-2.pptx",
            "role": role,
        },
    }
    nbf.write(nb, path)

write_nb(teacher_cells, LESSON / "demo-lab-teacher.ipynb", "teacher")
write_nb(student_cells, LESSON / "demo-lab-student.ipynb", "student")

# ---------------------------------------------------------------------
# Worksheet source + PDF
# ---------------------------------------------------------------------

WORKSHEET_QMD = r'''---
title: "字符编码 - Q14 重建与出口检查"
format: pdf
---

姓名：____________________    班级：____________________    日期：____________________

# 一、重建两条路径

## 1. 输入并显示

请填入：\`键盘输入\`、\`输入码 / IME\`、\`字符 / code point\`、\`字体映射\`、\`glyph / 字形\`、\`pixels\`

\`\`\`text
[                 ]
        ↓
[                 ]
        ↓
[                 ]
        ↓
[                 ]
        ↓
[                 ]
        ↓
[                 ]
\`\`\`

## 2. 保存、传输并读取

请填入：\`字符 / code point\`、\`encode\`、\`bytes\`、\`decode\`、\`字符 / code point\`、
\`字体映射\`、\`glyph / 字形\`、\`pixels\`

# 二、三题出口检查

1. 输入法解决什么问题？
2. Unicode code point 与 UTF-8 / UTF-16 / UTF-32 有什么区别？
3. 同一批 bytes 为什么可能显示成乱码？
'''
(WORKSHEETS / "character-encoding-exit-ticket.qmd").write_text(WORKSHEET_QMD, encoding="utf-8")

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
pdf_path = WORKSHEETS / "character-encoding-exit-ticket.pdf"
c = canvas.Canvas(str(pdf_path), pagesize=A4)
W, H = A4
left, right, top = 18*mm, 18*mm, 17*mm

def txt(x, y, s, size=10.5):
    c.setFont("STSong-Light", size)
    c.drawString(x, y, s)

txt(left, H-top, "字符编码 - Q14 重建与出口检查", 17)
txt(left, H-top-10*mm, "姓名：________________    班级：________________    日期：________________", 10.5)

y = H-top-22*mm
txt(left, y, "一、重建两条路径", 13)
y -= 9*mm
txt(left, y, "1. 输入并显示", 11.5)
y -= 7*mm
txt(left, y, "请填入：键盘输入、输入码 / IME、字符 / code point、字体映射、glyph / 字形、pixels", 9.3)
y -= 10*mm

box_w, box_h, cx = 55*mm, 9*mm, left+23*mm
for i in range(6):
    c.rect(cx, y-box_h, box_w, box_h, stroke=1, fill=0)
    if i < 5:
        c.line(cx+box_w/2, y-box_h, cx+box_w/2, y-box_h-5*mm)
        ax, ay = cx+box_w/2, y-box_h-5*mm
        c.line(ax, ay, ax-1.5*mm, ay+2*mm)
        c.line(ax, ay, ax+1.5*mm, ay+2*mm)
    y -= 15*mm

y -= 2*mm
txt(left, y, "2. 保存、传输并读取", 11.5)
y -= 7*mm
txt(left, y, "请填入：字符 / code point、encode、bytes、decode、字符 / code point、字体映射、glyph / 字形、pixels", 9.1)
y -= 9*mm

bw, bh, gap, x0 = 38*mm, 9*mm, 6*mm, left
for row in range(2):
    xs = [x0+i*(bw+gap) for i in range(4)]
    for i, x in enumerate(xs):
        c.rect(x, y-bh, bw, bh, stroke=1, fill=0)
        if i < 3:
            c.line(x+bw, y-bh/2, x+bw+gap-1*mm, y-bh/2)
            ax, ay = x+bw+gap-1*mm, y-bh/2
            c.line(ax, ay, ax-2*mm, ay+1.5*mm)
            c.line(ax, ay, ax-2*mm, ay-1.5*mm)
    if row == 0:
        x_last = xs[-1]+bw/2
        c.line(x_last, y-bh, x_last, y-bh-5*mm)
        c.line(x_last, y-bh-5*mm, x0+bw/2, y-bh-5*mm)
        c.line(x0+bw/2, y-bh-5*mm, x0+bw/2, y-bh-10*mm)
        ax, ay = x0+bw/2, y-bh-10*mm
        c.line(ax, ay, ax-1.5*mm, ay+2*mm)
        c.line(ax, ay, ax+1.5*mm, ay+2*mm)
        y -= 16*mm
    else:
        y -= 13*mm

txt(left, y, "二、三题出口检查", 13)
y -= 8*mm
questions = [
    "1. 输入法解决什么问题？",
    "2. Unicode code point 与 UTF-8 / UTF-16 / UTF-32 有什么区别？",
    "3. 同一批 bytes 为什么可能显示成乱码？",
]
for q in questions:
    txt(left, y, q, 10.5)
    y -= 6*mm
    for _ in range(2):
        c.line(left, y, W-right, y)
        y -= 7*mm
    y -= 2*mm

c.setFont("STSong-Light", 8)
c.drawRightString(W-right, 9*mm, "课堂基线：1-2-3-character-encoding-v6-2.pptx")
c.save()

# ---------------------------------------------------------------------
# Root package readme
# ---------------------------------------------------------------------

README = r'''# Character Encoding Classroom Package

Production baseline:

\`\`\`text
1-2-3-character-encoding-v6-2.pptx
\`\`\`

Companion artifacts:

- \`teacher-guide.qmd\`
- \`demo-lab-teacher.ipynb\`
- \`demo-lab-student.ipynb\`
- \`assets/gb2312-lab.txt\`
- \`assets/utf8-lab.txt\`
- \`assets/generated/image-prompts.md\`
- \`demos/demo_unicode_utf.py\`
- \`demos/check_classroom_package.py\`
- \`worksheets/character-encoding-exit-ticket.qmd\`
- \`worksheets/character-encoding-exit-ticket.pdf\`

Before class:

\`\`\`bash
python 1-2-encoding/1-2-3-character-encoding/demos/create_lab_files.py
python 1-2-encoding/1-2-3-character-encoding/demos/check_classroom_package.py
\`\`\`

Then open the production PPTX and the two role-specific notebooks.
'''
(LESSON / "CLASSROOM-PACKAGE.md").write_text(README, encoding="utf-8")

print("Character-encoding classroom package generated.")
