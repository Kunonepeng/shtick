# AGENTS.md

## Project: shtick-codex-project

`shtick` is a teaching-content project for Senior High School Information Technology courses.

The name comes from a useful spelling accident:

```text
SHSIC
Senior High School Information technology Course

      ↓ easy to mistype / misread as

SHTICK
```

`shtick` is also an English word for a characteristic routine, style, or recognizable way of doing something. The project name therefore preserves the connection to `SHSIC` while also fitting the goal of developing a distinctive, reusable teaching approach.

The project produces classroom-ready course designs, PPTX decks, Reveal.js reference decks, Jupyter demonstrations, student materials, and supporting source notes.

The priority is not merely to generate files. The priority is to produce material that a teacher can inspect, trust, edit, and use directly in class.

---

# 1. Core writing rule: avoid "AI tone"

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
- appropriate for the students and lesson.

Avoid:

- generic motivational language;
- exaggerated claims;
- repetitive conclusions;
- unnecessary summaries of obvious points;
- formulaic phrases such as “通过……不仅……而且……” unless genuinely needed;
- vague phrases such as “帮助学生更好地理解” without stating what students actually do or understand;
- meta-commentary about content generation;
- consultancy / marketing language;
- decorative headings that do not help the teaching structure.

Prefer concrete classroom language.

For example, avoid:

> 本节课将带领学生深入探索字符编码的奥秘。

Prefer:

> 先让学生观察：同一批字节为什么会显示成不同文字？

---

# 2. Language and technical precision

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

Do not translate technical terms mechanically when the English term is clearer or standard in the curriculum.

Explicitly distinguish concepts that students may confuse, including:

- 字符集 vs 字符编码
- 输入码 vs 键盘扫描码
- Unicode 码位 vs 编码后的 bytes
- 字符身份 vs 字形
- 国标码 vs 机内码
- GB2312-specific behavior vs general character-encoding behavior

If a classroom simplification has an important technical boundary, state that boundary.

---

# 3. Source-of-truth hierarchy

For each lesson or module, use this structure:

```text
course-design.qmd
        ↓
pedagogical source of truth
        ↓
┌───────────────────────────────┐
│                               │
PPTX classroom deck        demo-lab.qmd
│                               │
WPS / PowerPoint           demo-lab.ipynb
│                               │
production presentation    live code demonstration
│
└───────────────┐
                ↓
            slides.qmd
                ↓
        Reveal.js reference deck
```

`course-design.qmd` defines the teaching logic.

The PPTX, Notebook, and Reveal.js versions must remain aligned with its:

- question numbering;
- teaching sequence;
- terminology;
- evidence;
- conclusions.

Do not allow these artifacts to silently diverge.

---

# 4. course-design.qmd: 认知困惑法 + 问题链

`course-design.qmd` must be designed primarily around:

1. **认知困惑法**
2. **问题链**

These are not optional decorations added after the content is written. They should shape the lesson from the beginning.

## 4.1 认知困惑法

Whenever the topic allows it, begin from a phenomenon, contradiction, unexpected result, or limitation that makes the student's current explanation insufficient.

A useful cognitive conflict should:

1. be immediately understandable;
2. allow students to make a plausible prediction;
3. produce evidence that makes the existing model insufficient;
4. create a genuine need for the next concept.

Examples:

```text
ASCII 是 7 bit。
为什么计算机中常常看到 8 bit？
```

```text
在 GB2312 中，“中”占 2 bytes。
为什么换成 UTF-8 后变成 3 bytes？
```

```text
同一批 bytes 没有改变。
为什么解码后却变成乱码？
```

```text
两个同学都使用 3-bit 编码。
为什么对方的 HELLO 仍然解不出来？
```

The purpose is not surprise for its own sake. The conflict must create a reason to learn the next idea.

## 4.2 问题链

A lesson should be organized as a connected sequence of questions.

Each major question should:

- follow naturally from the previous result;
- be slightly more complex than the previous question;
- introduce at most one major new difficulty;
- use evidence or ideas already established;
- produce something needed by the next question;
- move students toward the final model.

Prefer a progression such as:

```text
观察
  ↓
识别
  ↓
比较
  ↓
推断
  ↓
解释
  ↓
设计
  ↓
诊断
  ↓
迁移
```

Avoid a lesson that is mainly:

```text
定义 A
定义 B
定义 C
练习
```

when the concepts can instead emerge from connected problems.

Questions should ask students to:

- predict;
- compare;
- explain a contradiction;
- infer a rule;
- design a solution;
- identify a limitation;
- diagnose a failure;
- transfer a principle to a new situation.

Weak:

> ASCII 是多少位编码？

Better:

> ASCII 有 128 个编码位置。至少需要多少 bit？

Stronger follow-up:

> 既然 ASCII 只需要 7 bit，为什么计算机中常常看到 8 bit？

## 4.3 Major-question design checklist

For every major Q, the design should be able to answer:

```text
Qx 问题是什么？
学生此时已经知道什么？
认知困惑是什么？
学生可能怎样回答？
学生要做什么活动 / 观察什么证据？
关键追问是什么？
学生应该发现什么？
最终抽象出什么概念？
为什么自然进入 Qx+1？
```

A useful structure is:

```markdown
## Qx 问题标题

### 认知起点
### 认知困惑
### 学生任务
### 预期回答
### 追问
### 证据 / Demo
### 形成结论
### 下一问
```

Not every small question needs all of these headings in the final document, but the design must support them.

Preferred lesson rhythm:

```text
认知困惑
   ↓
提出问题
   ↓
学生预测
   ↓
活动 / 实验 / 证据
   ↓
结果与预测冲突
   ↓
追问
   ↓
抽象概念
   ↓
新的、更复杂的问题
   ↓
迁移
   ↓
完整模型
```

---

# 5. Official classroom deck: PPTX

The official classroom presentation format is currently `.pptx`.

Preferred classroom environment:

1. **WPS Presentation**
2. Microsoft PowerPoint

The PPTX version is the production-quality classroom artifact.

It is acceptable to generate PPTX directly. Do not force the production deck through Quarto when doing so reduces presentation quality.

---

# 6. PPTX visual standard: strict compliance

Every production PPTX deck must strictly follow:

`slide-style-guide.md`

This file is a **hard design specification**, not loose inspiration.

At minimum, preserve:

- 16:9 canvas;
- white background;
- violet top and bottom rails;
- Alibaba PuHuiTi 3.0 for native text;
- common title baseline;
- common content working area;
- strong narrative teaching titles;
- evidence-first layouts;
- semantic violet / cyan / red;
- generous white space;
- progressive disclosure through duplicated slides;
- stable geometry across build sequences.

Do not introduce a new visual language unless the project explicitly changes the style guide.

## 6.1 Student-facing content only

The slide itself should contain only information students need to see at that moment.

Student-facing information includes:

- the current problem / question;
- essential evidence;
- diagrams;
- examples;
- short experiment instructions;
- key values;
- the current conclusion;
- labels required to understand the visual.

Do not turn the slide into a teacher handout.

Complementary teacher-facing information belongs in Speaker Notes.

## 6.2 One slide, one current teaching focus

Do not put everything that is eventually true onto one slide.

Prefer a sequence:

```text
Question
   ↓
Evidence
   ↓
Focus
   ↓
Explanation
   ↓
Conclusion
```

If a slide is dense, split it.

Do not solve density by shrinking normal teaching text below the style-guide standard.

## 6.3 Progressive disclosure

Prefer duplicated slides over complicated animation.

Use:

```text
base slide
    ↓
same geometry + current focus
    ↓
same geometry + explanation
    ↓
move focus to next item
```

Between consecutive build slides, change only the intended teaching focus.

Typical changes:

- add / move one red focus rectangle;
- reveal one conclusion;
- add one dark spotlight overlay;
- highlight one bit, byte, region, or timeline stage.

Do not recreate a build slide from scratch if it can be duplicated.

---

# 7. Speaker Notes are mandatory

Every teaching slide must contain Speaker Notes.

Every slide must contain a usable **teacher transcript**: what the teacher can actually say when presenting that slide.

The transcript should not merely repeat visible text.

Example:

```text
Slide:
“汉字真的总是占 2 byte 吗？”

Speaker Notes:
“刚才我们在 GB2312 中看到，一个汉字用了两个字节。
现在我不改这个‘中’字，只改保存规则。
请看 UTF-8 的结果。还是两个字节吗？”
```

Where appropriate, Speaker Notes may also contain:

```text
[教学意图]
[教师逐字稿]
[预期学生回答]
[追问]
[技术注解]
[来源]
[Demo 操作]
```

Not every slide needs every subsection, but every teaching slide needs a transcript.

Research URLs, technical caveats, alternative explanations, likely misconceptions, and other non-student-facing information should normally be placed in Speaker Notes rather than on the slide.

---

# 8. PPTX layout quality assurance

A deck is not complete because the PPTX file was successfully generated.

Every production deck must be visually inspected.

Specifically prevent:

- overlapping text;
- shapes covering text;
- clipped text;
- unexpected Chinese line wrapping;
- text extending outside its intended area;
- overlays obscuring key content;
- inconsistent margins;
- misaligned duplicated slides;
- stretched screenshots;
- auto-fit shrinking key text;
- content entering the violet rails / unsafe margins;
- font substitution changing line breaks.

## 8.1 Required QA workflow

For every production deck:

1. generate the PPTX;
2. render **every slide** to an image;
3. generate a montage of the complete deck;
4. inspect the montage for visual consistency;
5. inspect dense / diagram-heavy / overlay slides individually at full resolution;
6. run programmatic checks for out-of-canvas objects where possible;
7. open the final deck in WPS whenever practical;
8. verify the Speaker Notes;
9. fix all visible layout defects before delivery.

A deck with visible overlap, clipping, broken wrapping, or unstable alignment is not classroom-ready.

## 8.2 Text-box rule

Do not assume a text box fits because the source string fits programmatically.

Chinese wrapping, font substitution, line spacing, WPS rendering, and PowerPoint rendering can change the final layout.

If text wraps incorrectly:

- enlarge the text area;
- shorten the student-facing wording;
- move complementary information to Speaker Notes;
- or split the content into another slide.

Do not reduce normal teaching text simply to force content into a box.

---

# 9. Reveal.js / Quarto deck

A Reveal.js version should still be maintained.

Its current role is:

```text
reference
+ experimentation
+ learning
+ gradual optimization
```

It is **not currently the official classroom presentation format**.

Maintain `slides.qmd` so the project can continue improving:

- CSS typography;
- stable slide geometry;
- progressive disclosure;
- code-output presentation;
- interactive demonstrations;
- reusable classroom layouts;
- browser-based delivery.

The Reveal.js deck must stay aligned with the PPTX in:

- Q numbering;
- teaching sequence;
- terminology;
- evidence;
- conclusions.

It does not need the same slide count or identical implementation.

Do not treat a successful Quarto render as evidence that the deck is presentation-ready.

Until its quality is comparable with the PPTX:

```text
PPTX      = classroom production
Reveal.js = reference / experimental implementation
```

When Reveal.js reaches the required classroom quality, this policy can be revisited.

---

# 10. Jupyter classroom workflow

Use one Jupyter Notebook for one class whenever practical.

Preferred source:

```text
demo-lab.qmd
        ↓
demo-lab.ipynb
```

Use the same Q identifiers as the course design and deck.

Preferred live classroom switching:

```text
PPT / WPS
    ⇄
JupyterLab
```

Avoid extra applications unless they provide important evidence.

For example:

```text
WinHex    = useful real-file evidence
Notebook  = Plan B / manipulation / fallback
```

Small, deterministic code examples may appear directly in the PPTX.

Use Jupyter when the teacher may need to:

- modify input live;
- try a student-suggested character;
- compare encodings;
- inspect bytes;
- rerun an experiment;
- diagnose a result;
- use a software-independent fallback.

General rule:

> **The deck shows the evidence. The Notebook allows the evidence to be manipulated.**

---

# 11. Teaching activities

An activity must have a clear cognitive purpose.

Do not add interaction merely to make the lesson look active.

For each major activity, be able to state:

```text
What does the student do?
What evidence do they produce?
What misconception / question does it expose?
What concept becomes necessary afterward?
```

Prefer short activities that feed directly into the next question.

---

# 12. Technical accuracy

All substantive technical claims should be checked before becoming classroom material.

Important examples:

## ASCII

ASCII is a 7-bit code with 128 positions.

When represented in an 8-bit byte:

```text
0xxxxxxx
```

Do not describe ASCII itself as an 8-bit encoding.

## GB2312

Statements such as:

```text
一个汉字占 2 bytes
两个 byte 的最高位都是 1
```

must be explicitly limited to the traditional GB2312 machine-code model being taught.

Do not generalize this to UTF-8, GB18030, or all Chinese encodings.

## Unicode

Distinguish:

```text
character
code point
encoding
byte sequence
glyph
pixels
```

Example:

```text
你
↓
U+4F60
↓
UTF-8
↓
E4 BD A0
```

`U+4F60` is not the UTF-8 byte representation.

## Input methods

Do not confuse 汉字输入码 with keyboard scan codes.

## Fonts and glyphs

Use this classroom model:

```text
character
↓
font mapping
↓
glyph / outline / bitmap
↓
rasterization
↓
pixels
```

Do not imply that the visible shape itself is the stored character identity.

---

# 13. Research and sources

When factual information depends on a standard, specification, product behavior, or historical fact, verify it.

Prefer:

1. official standards bodies;
2. primary specifications;
3. official technical documentation;
4. reputable institutional sources;
5. high-quality secondary sources where necessary.

Do not silently copy uncertain figures from unsourced diagrams or web posts.

If sources disagree, preserve the distinction rather than forcing a false single answer.

Research URLs normally belong in Speaker Notes or teacher references unless the website itself is teaching evidence.

---

# 14. Typical lesson files

A lesson directory may contain:

```text
course-design.qmd
demo-lab.qmd
slides.qmd

assets/
demos/
references/

<lesson-name>-V3.pptx
```

Roles:

```text
course-design.qmd  → pedagogical source of truth
demo-lab.qmd       → executable classroom demonstrations
slides.qmd         → experimental Reveal.js implementation
*.pptx             → current production classroom deck
assets/            → screenshots, diagrams, evidence
demos/             → reusable supporting code
references/        → supporting source material
```

Avoid creating multiple files with nearly identical purposes unless there is a clear reason.

---

# 15. Definition of done

A lesson is classroom-ready only when:

- the question chain is coherent and progressively challenging;
- cognitive conflict creates a genuine need for the concepts;
- technical claims have been checked;
- student activities have a clear cognitive purpose;
- the PPTX strictly follows `slide-style-guide.md`;
- every slide contains only necessary student-facing information;
- every teaching slide has a Speaker Notes transcript;
- complementary teacher information is in Speaker Notes;
- every slide has been rendered and visually inspected;
- there is no overlap, clipping, accidental wrapping, or broken alignment;
- the final deck has been checked in WPS / PowerPoint when practical;
- Notebook demos have been tested;
- Reveal.js remains aligned as the experimental/reference deck;
- the writing contains no "AI tone".

Successful rendering is not the definition of done.

**Classroom usability is.**
