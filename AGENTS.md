# AGENTS.md

## Project: shtick-codex-project

`shtick` is a teaching-content project for developing classroom-ready information technology / computer science materials.

The project produces teaching designs, classroom slides, Jupyter demonstrations, student learning materials, and supporting source notes.

The priority is not simply to generate content. The priority is to produce material that a teacher can inspect, trust, edit, and use directly in class.

---

# 1. Core principles

## 1.1 Avoid "AI tone"

All content in this project must avoid recognizable AI-generated writing patterns.

Write as a careful teacher, textbook editor, or curriculum designer would write.

Preferred qualities:

- direct;
- specific;
- concise;
- technically precise;
- classroom-oriented;
- natural Chinese;
- clear argumentative structure;
- appropriate for the actual students and lesson.

Avoid:

- generic motivational language;
- exaggerated claims;
- unnecessary summaries of obvious points;
- repetitive conclusions;
- formulaic phrases such as “通过……不仅……而且……” unless genuinely needed;
- excessive headings created only to make text look structured;
- vague phrases such as “帮助学生更好地理解” without explaining what students actually do or understand;
- meta-commentary about the content-generation process;
- phrases that sound like product marketing or consultancy writing.

Do not write things such as:

> 本节课将带领学生深入探索……

when a more natural version is:

> 先让学生观察同一串字节为什么会显示成不同文字。

Prefer concrete classroom language over abstract educational slogans.

---

# 2. Language

## 2.1 Default language

Teaching materials are Chinese-first.

Keep established technical terms and abbreviations in English where appropriate, for example:

- ASCII
- Unicode
- UTF-8
- IME
- Code Point
- byte
- bit
- glyph
- encode / decode

Do not translate technical terms mechanically if the English term is clearer or is normally used in the curriculum.

## 2.2 Precision

Explicitly distinguish concepts that students may confuse.

Examples:

- 字符集 vs 字符编码
- 输入码 vs 键盘扫描码
- Unicode 码位 vs 编码后的 bytes
- 字符身份 vs 字形
- 国标码 vs 机内码
- GB2312-specific behavior vs general character-encoding behavior

If a simplified classroom statement has an important technical boundary, state the boundary.

---

# 3. Source of truth

For each lesson or module, use the following hierarchy.

```text
course-design.qmd
        ↓
teaching structure / questions / activities / technical model
        ↓
┌───────────────────────────────┐
│                               │
PPTX classroom deck        demo-lab.qmd
│                               │
WPS / PowerPoint           demo-lab.ipynb
│                               │
primary presentation       live code demonstration
│
└───────────────┐
                ↓
            slides.qmd
                ↓
        Reveal.js reference deck