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
PPTX classroom deck        Jupyter demo sources
│                               │
WPS / PowerPoint           ├── demo-lab-teacher.qmd
│                          │       ↓
│                          │   demo-lab-teacher.ipynb
│                          │
│                          └── demo-lab-student.qmd
│                                  ↓
│                              demo-lab-student.ipynb
│
production presentation    teacher/student demo views
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

## 4.4 Preserve course-design depth during refactoring

Do not shorten `course-design.qmd` merely to make the repository cleaner.

When reviewing or refactoring, preserve:

- pedagogical rationale;
- cognitive-conflict design;
- question-chain logic;
- expected student responses;
- activity intent;
- demo purpose;
- transition logic;
- technical caveats;
- source notes.

If the file becomes too long, move secondary teacher-facing detail into `teacher-guide.qmd`, `appendix.qmd`, or a references section rather than deleting it.

Refactoring may improve structure, naming, and navigation, but it must not reduce the pedagogical information content.

---

# 5. Student-facing vs teacher-facing information

Whenever content is designed, revised, or reviewed, explicitly decide whether each piece of information is:

1. **student-facing**;
2. **teacher-facing**;
3. **shared, but revealed at different times**.

Do not make this decision implicitly.

## 5.1 Student-facing information

Student-facing information is what students need to see **at that moment** to think, observe, act, compare, or form a conclusion.

Typical student-facing content:

- the current question;
- necessary givens;
- experiment / activity instructions;
- evidence needed for reasoning;
- diagrams and examples;
- code that students are expected to read or manipulate;
- the conclusion **after** students have had time to think;
- concise terminology that students need to retain.

Student-facing material should be concise and projection-readable.

## 5.2 Teacher-facing information

Teacher-facing information supports teaching but should not normally occupy student visual space.

Typical teacher-facing content:

- full teaching transcript;
- teaching intention;
- expected student responses;
- likely misconceptions;
- follow-up questions;
- timing advice;
- technical caveats;
- alternative examples;
- troubleshooting steps;
- demo fallback plans;
- source URLs and research notes;
- answers or hints that would spoil the current question;
- implementation details students do not need.

Teacher-facing information belongs primarily in:

- PPTX Speaker Notes;
- `course-design.qmd`;
- `demo-lab-teacher.qmd / .ipynb`;
- teacher reference material.

## 5.3 Review rule

For every significant piece of information, ask:

```text
Does the student need to see this now?
Does it help the student think, or does it tell them what to think?
Will it spoil the question?
Is this mainly guidance for the teacher?
Can it move to Speaker Notes or the teacher notebook?
```

If information is useful to the teacher but not necessary for students at that moment, keep it teacher-facing.

If information reveals the answer, clue, conclusion, or key inference before students have attempted the question, it must not appear on the question slide or student notebook at that stage.

---

# 6. Official classroom deck: PPTX

The official classroom presentation format is currently `.pptx`.

Preferred classroom environment:

1. **WPS Presentation**
2. Microsoft PowerPoint

The PPTX version is the production-quality classroom artifact.

It is acceptable to generate PPTX directly. Do not force the production deck through Quarto when doing so reduces presentation quality.

---

# 7. PPTX visual standard: strict compliance

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

## 7.1 Student-facing content only

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

## 7.2 One slide, one current teaching focus

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

## 7.3 Progressive disclosure

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

## 7.4 Every major question gets a question-only slide

Every major classroom question should first appear on its **own question slide**.

The purpose is to create a clean thinking pause.

The question slide must not expose:

- the answer;
- hints that effectively reveal the answer;
- the conclusion;
- answer-colored emphasis;
- explanatory diagrams that give away the inference;
- completed calculations;
- teacher annotations.

It may include only the information students genuinely need in order to attempt the question:

- the question itself;
- necessary givens;
- a neutral evidence image or table, if required;
- concise task instructions.

Sparse question slides are encouraged.

## 7.5 Question slide → answer slide pairing

The next slide should reveal the answer, explanation, evidence, or worked reasoning.

The answer slide must be created by **duplicating the question slide**, not rebuilding it.

The question itself must remain visually fixed across the transition:

- same font family;
- same font size;
- same weight;
- same x/y position;
- same text-box width and height;
- same line breaks where practical;
- same alignment;
- same surrounding base geometry.

Then add the answer / explanation without moving the question unless there is a compelling layout reason.

Preferred transition:

```text
Question-only slide
        ↓ duplicate
Same question in exactly the same place
+ answer / evidence / explanation
        ↓
optional additional duplicated slides
+ one new focus at a time
```

This is intended to reduce visual noise during slide switching so students perceive the new information, not a shifting layout.

For question/answer pairs, layout stability is more important than squeezing both into a single slide.

---

# 8. Speaker Notes are mandatory

Every teaching slide must contain Speaker Notes.

Every slide must contain a usable **teacher transcript**: what the teacher can actually say when presenting that slide.

The transcript should not merely repeat visible text.

Speaker Notes should begin with the **full classroom question or page purpose**, not only an internal identifier such as `Q3` or `Q9`.

Preferred form:

```text
[问题] ASCII 是 7 bit，为什么计算机中常常看到 8 bit？
[内部编号] Q3
```

The internal Q number is for navigation only. The complete question is the meaningful teaching unit.

Where appropriate, Speaker Notes may contain:

```text
[问题 / 页面目的]
[内部编号]
[教学意图]
[教师逐字稿]
[追问问题]
[预期学生反应]
[形成结论]
[Demo 操作]
[技术注解]
[来源]
```

Not every slide needs every subsection, but every teaching slide needs a transcript.

Research URLs, technical caveats, alternative explanations, likely misconceptions, and other non-student-facing information should normally be placed in Speaker Notes rather than on the slide.

## 8.1 Transcript quality

The transcript should be written as language a teacher can actually say in class.

It should:

- sound natural when spoken aloud;
- create curiosity before giving an explanation;
- invite students to predict, compare, vote, argue, observe, or explain;
- pause for student thinking instead of immediately supplying the answer;
- refer explicitly to what students can see on the slide or in the demo;
- use short transitions that connect the current question to the previous one;
- anticipate common student answers and use them to move the discussion forward;
- keep technical caveats in teacher-facing language rather than crowding the slide;
- preserve a lively classroom rhythm without becoming theatrical or exaggerated.

Avoid transcripts that merely read the slide aloud.

Weak:

> ASCII 是 7 bit。这里显示 8 bit。最高位是 0。

Prefer:

> 先别算。ASCII 明明只有 128 个位置，7 bit 已经够了。那为什么文件里我们偏偏看到 8 bit？多出来的这一位到底从哪儿来的？先看 A，谁能指出那一位在哪里？

## 8.2 Follow-up questions

`追问问题` belongs in Speaker Notes unless students must read it directly.

Follow-up questions should deepen the current reasoning, not introduce unrelated content.

Good follow-up questions help students:

- explain an observation;
- challenge a premature conclusion;
- connect evidence to a concept;
- compare two cases;
- transfer the idea to a new example.

Do not place teacher prompts, expected answers, follow-up questions, technical caveats, or navigation labels such as `Q1-A` on the student-facing slide unless students genuinely need to see them.

The slide shows the learning object.

The Speaker Notes guide the teaching conversation.

---

# 9. PPTX layout quality assurance

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

## 9.1 Required QA workflow

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

## 9.2 Text-box rule

Do not assume a text box fits because the source string fits programmatically.

Chinese wrapping, font substitution, line spacing, WPS rendering, and PowerPoint rendering can change the final layout.

If text wraps incorrectly:

- enlarge the text area;
- shorten the student-facing wording;
- move complementary information to Speaker Notes;
- or split the content into another slide.

Do not reduce normal teaching text simply to force content into a box.

---

# 10. Reveal.js / Quarto deck

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

# 11. Demonstrations and Jupyter classroom workflow

Students generally respond well to demonstrations. Whenever a concept is meaningfully improved by seeing it happen, a demo is encouraged.

Do not add demos merely for entertainment. A demo should provide evidence, expose a misconception, create cognitive conflict, or make an invisible process visible.

Good candidates include:

- bytes changing under different encodings;
- the same bytes producing different text under different decoding rules;
- ASCII / Unicode values;
- image / sound / text digitization;
- input → IME → character → glyph workflows;
- bit-level patterns;
- visual comparisons that are difficult to understand from static prose.

The preferred place for executable demo code is JupyterLab.

## 11.1 Two Notebook versions are required

For a class that uses Jupyter demos, maintain two views:

```text
demo-lab-teacher.qmd
        ↓
demo-lab-teacher.ipynb

demo-lab-student.qmd
        ↓
demo-lab-student.ipynb
```

Use the same Q identifiers and demo identifiers in both versions.

Where practical, share the underlying computation through small reusable functions / modules so the two notebooks do not drift technically.

### Teacher-facing Notebook

The teacher version may contain:

- complete runnable code;
- expected output;
- answers;
- teaching transcript / prompts;
- likely student predictions;
- explanation of what to observe;
- technical caveats;
- troubleshooting notes;
- fallback code;
- optional extensions;
- source references.

It should be optimized for reliable classroom presentation and teacher control.

### Student-facing Notebook

The student version should contain only what students need to participate.

It may contain:

- the question;
- necessary setup;
- short readable code;
- incomplete / editable cells when student manipulation is useful;
- observation prompts;
- spaces for predictions or conclusions;
- outputs that are appropriate to reveal at that stage.

It should not expose teacher-only notes, hidden answers, or conclusions before the intended reveal.

## 11.2 Demo design rule

For every demo, specify:

```text
What question does this demo answer?
What should students predict before running it?
What exactly should students observe?
What should remain hidden until after the run?
What conclusion should students infer?
What is the fallback if the demo fails?
```

A demo should normally sit inside the same cognitive sequence as the lesson:

```text
question
  ↓
prediction
  ↓
run demo
  ↓
observe evidence
  ↓
explain
  ↓
form concept
```

## 11.3 Classroom switching

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

Small, deterministic code examples may also appear directly in the PPTX when the output itself is evidence and no live manipulation is needed.

Use Jupyter when the teacher may need to:

- modify input live;
- try a student-suggested value;
- compare encodings;
- inspect bytes;
- rerun an experiment;
- diagnose a result;
- use a software-independent fallback.

General rule:

> **The deck shows the evidence. The Notebook allows the evidence to be manipulated.**

---

# 12. Teaching activities

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

# 13. Technical accuracy

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

# 14. Research and sources

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

# 15. Typical lesson files

A lesson directory may contain:

```text
course-design.qmd
demo-lab-teacher.qmd
demo-lab-student.qmd
slides.qmd

assets/
demos/
references/

<lesson-name>-V3.pptx
```

Roles:

```text
course-design.qmd       → pedagogical source of truth
demo-lab-teacher.qmd    → teacher-facing executable demonstrations
demo-lab-student.qmd    → student-facing executable demonstrations
slides.qmd              → experimental Reveal.js implementation
*.pptx                  → current production classroom deck
assets/                 → screenshots, diagrams, evidence
demos/                  → reusable supporting code
references/             → supporting source material
```

Avoid creating multiple files with nearly identical purposes unless there is a clear reason.

---

# 16. Definition of done

A lesson is classroom-ready only when:

- the question chain is coherent and progressively challenging;
- cognitive conflict creates a genuine need for the concepts;
- technical claims have been checked;
- student activities have a clear cognitive purpose;
- suitable concepts use demonstrations where demos provide meaningful evidence;
- teacher-facing and student-facing information have been explicitly separated;
- teacher and student Jupyter versions are aligned where Jupyter is used;
- `course-design.qmd` preserves the design rationale and transition logic;
- the PPTX strictly follows `slide-style-guide.md`;
- every major question has a question-only slide before its answer / explanation;
- question/answer slide pairs preserve the question's position, typography, and base geometry;
- every slide contains only necessary student-facing information;
- every teaching slide has Speaker Notes with the full question/page purpose and a usable transcript;
- complementary teacher information is in Speaker Notes;
- every slide has been rendered and visually inspected;
- all native deck text explicitly uses the required Alibaba PuHuiTi 3.0 font family/variant;
- there is no overlap, clipping, accidental wrapping, or broken alignment;
- the final deck has been checked in WPS / PowerPoint when practical;
- Notebook demos have been tested;
- Reveal.js remains aligned as the experimental/reference deck;
- the writing contains no "AI tone".

Successful rendering is not the definition of done.

**Classroom usability is.**
