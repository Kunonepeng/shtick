# Slide Style Guide

**Reference deck:** `上1-2-3-1 字符编码.pptx`  
**Style name:** **Violet-Rail Technical Explainer / 紫色轨道式技术讲解风格**  
**Primary use:** 高中信息科技、Python / CS 入门、概念讲解、技术史与原理课件  
**Font family:** **Alibaba PuHuiTi 3.0**
**Status:** **Canonical production specification** for WPS / PowerPoint classroom decks in this project.

> This guide is a normalized extraction of the reference deck's recurring visual language. It keeps the deck's strongest signatures while treating imported screenshot colors, one-off artwork, and occasional dense/small-text slides as content artifacts rather than core style rules.

---

## 1. Style identity

The deck is a **minimal, classroom-oriented technical explainer** built around five traits:

1. **White canvas + violet top/bottom rails** — almost no decorative chrome; the master-frame lines provide the visual identity.
2. **Large, bold, left-aligned teaching titles** — titles are usually questions, claims, or conceptual prompts rather than generic section names.
3. **Evidence-heavy visuals** — screenshots, historical photos, tables, standards pages, diagrams, and code/binary examples are central to the explanation.
4. **Semantic color, not decorative color** — violet marks important concepts, cyan distinguishes a second technical category, and red means “look here now.”
5. **Progressive disclosure by duplicated slides** — instead of relying on complicated animation, consecutive slides reuse the same composition and move a red focus box or dark spotlight overlay to the next concept.

The overall feeling should be **clear, rigorous, modern, and teacher-led**, not corporate, playful, glossy, or card-heavy.

---

## 2. Reference-deck anatomy (descriptive)

The figures in this section record where the style came from. They are **not** targets for a new lesson. Determine a new deck's slide count, question sequence, and necessary layouts from `course-design.qmd`. Do not inspect, copy, or match the reference deck merely because it is named here; use it only when the task expressly calls for it.

- **Canvas:** 16:9 widescreen, **13.333 × 7.5 in**.
- **44 slides** in the reference deck.
- **43/44 slides** use the same **Title + Content** layout; only the opening slide uses the title-slide layout.
- The deck therefore behaves like a **single disciplined teaching canvas**, not a collection of many unrelated PowerPoint templates.
- The reference file contains many native shapes plus a large number of screenshots/images; visuals are treated as teaching evidence rather than decoration.

### Core master geometry

| Element | Position / size | Rule |
|---|---:|---|
| Top rail | rectangle `x=0`, `y=0`, `w=13.333`, `h=8 pt` | `#6251B1` |
| Bottom rail | rectangle `x=0`, `y=7.5 in − 8 pt`, `w=13.333`, `h=8 pt` | `#6251B1` |
| One-line slide title | `x=0.665`, `y=0.665`, `w≈12.0`, `h≈0.77 in` | Left aligned; see the two-line variant in §3.3 |
| Main content area | `x=0.665`, `y=1.63`, `w≈12.0`, `h≈5.21 in` | One-line title default; two-line title starts content at `y=2.25 in` |
| Left/right safe margin | `≈0.67 in` | Keep native content inside this margin unless a screenshot intentionally bleeds wider |

The rail rectangles meet the canvas edges exactly. Eight points is approximately `0.1111 in`, so the bottom rail starts at approximately `y=7.3889 in`. Their visual centerlines stay close to the reference positions of `0.05` and `7.45 in`. Do not place rail objects outside the slide canvas; edge-aligned rectangles give the same full-width appearance and pass overflow checks.

---

## 3. Typography

### 3.1 Font family and weights

Use **Alibaba PuHuiTi 3.0** throughout native slide content.

Preferred variants seen in the deck:

- **Alibaba PuHuiTi 3.0 115 Black** — titles, strong labels, large callouts
- **Alibaba PuHuiTi 3.0 85 Bold** — dense technical emphasis, code-related explanation, secondary strong text
- **Alibaba PuHuiTi 3.0 55 Regular** — body copy, captions, explanatory text

The expected font files are `AlibabaPuHuiTi-3-115-Black.ttf`, `AlibabaPuHuiTi-3-85-Bold.ttf`, and `AlibabaPuHuiTi-3-55-Regular.ttf`. Check the face resolved by WPS / PowerPoint or the rendering tool; a font name stored in the PPTX does not prove that the renderer used it. If **85 Bold** is substituted, use **115 Black** for strong emphasis or **55 Regular** for ordinary text, then render again. Do not accept an unrelated fallback font silently.

Do **not** mix in another Chinese UI font for native content. Imported website screenshots may naturally contain other fonts; those are evidence, not part of the slide theme.

> Implementation note: explicitly set Alibaba PuHuiTi 3.0 in slide masters and generated text objects. Do not depend only on the PowerPoint theme-font metadata or system fallback.

### 3.2 Type scale

| Role | Font | Size | Color / treatment |
|---|---|---:|---|
| Cover title | 115 Black | **60 pt** | Near-black; optionally highlight one key word in accent violet |
| Cover subtitle | 55 Regular | **37 pt** | ~50% gray (`#808080`), centered |
| Standard slide title | 115 Black | **36 pt** | Near-black (`≈#262626`), left aligned |
| Standard body | 55 Regular | **22 pt** | Black |
| Strong content label | 115 Black | **24 pt** | Black / white depending on background |
| Technical bold body | 85 Bold; 115 Black if 85 Bold does not resolve | **22 pt** | Black |
| Spotlight / thesis overlay | 115 Black | **32–36 pt** | White on dark translucent panel |
| Dense diagram / timeline text | 85 Bold or 55 Regular | **14 pt** | Black; use sparingly |
| Nonessential source / micro-note | 55 Regular | **12–14 pt** | Gray or black; never the only text students must read |

### 3.3 Master text behavior

**Standard slide title**

- one-line box: `x=0.665`, `y=0.665`, `w≈12.0`, `h≈0.77 in`
- 36 pt, 115 Black
- left aligned
- 100% line spacing
- slightly expanded character spacing (reference master uses approximately **+3 pt**)
- no bullet
- color is slightly softened from pure black (`≈#262626`)

If the title does not fit on one line, first shorten the wording without changing the teaching question. If two lines remain necessary, use a **two-line title variant**: keep `x=0.665`, `y=0.665`, `w≈12.0`, and 36 pt Black; set title-box height to `1.35 in` and start the main content at `y=2.25 in`. Set the line break deliberately. Keep that break, title box, and shifted content geometry identical across the question/answer pair. If the two-line variant still does not fit, split the teaching focus across slides. Never use auto-fit or a smaller title merely to force it into the box. Apply the approximate +3 pt character spacing only when the title still fits at 36 pt.

**Standard body text**

- 22 pt, 55 Regular
- 130% line spacing at first level
- approximately 10 pt paragraph spacing after first-level paragraphs
- slightly expanded character spacing (reference master uses approximately **+1.5 pt**)
- default bullet is a solid circle `●`
- black text on white

### 3.4 Title-writing style

Titles are part of the teaching narrative. Prefer:

- **Questions:** `UTF-8, UTF-16, UTF-32，谁更优秀？`
- **Claims:** `Morse Code是一种字符编码方式。`
- **Problem framing:** `世界上的其它字符，怎么办？`
- **Conceptual contrast:** `Unicode决定“字符对应哪个数字”，UTF决定“这个数字怎么变成0/1字节”。`

Avoid generic titles such as `背景介绍`, `知识点`, `第三部分` unless necessary.

### 3.5 Emphasis inside titles and body

Use emphasis selectively:

- Accent violet for the single concept students should retain.
- Bold/Black for terms, values, or conclusions.
- Keep English technical terms (`ASCII`, `Unicode`, `UTF-8`, `IME`) in the same Alibaba family rather than switching to a separate Latin font.
- Avoid italics and decorative underlines.

---

## 4. Color system

### 4.1 Core palette

| Semantic role | Hex | Usage |
|---|---|---|
| **Frame Violet** | `#6251B1` | Top and bottom master rails only; stable deck identity |
| **Teaching Accent Violet** | `#8C64E1` | Key terms, active concepts, arrows, outlined bits/boxes, highlighted headings |
| **Technical Cyan** | `#00B0F0` | Secondary category in outlines, arrows, and large highlights |
| **Readable Cyan Text** | `#007C9B` | Essential cyan text on white; same semantic category, darker for projection |
| **Focus Red** | `#FF0000` | Temporary focus rectangle, selected region, current timeline stage; never decorative |
| **Title near-black** | `≈#262626` | Standard titles |
| **Body black** | `#000000` | Main explanatory copy |
| **Muted gray** | `≈#808080` | Cover subtitle, secondary labels/captions |
| **White** | `#FFFFFF` | Background and text on dark overlays |

### 4.2 Dark spotlight overlay

The reference deck repeatedly uses a near-black translucent rectangle to de-emphasize the existing slide while showing one strong white conclusion.

Recommended implementation:

- Fill: near-black (`#171717` to `#222222`)
- Opacity: **80–90%**
- No visible border
- Text: white, 32–36 pt, 115 Black
- Use as a **temporary teaching spotlight**, not a permanent card style

On a white background this appears visually around dark charcoal (`#2D2D2D–#454545` depending on opacity).

### 4.3 Semantic color rules

- **Violet = concept / relationship / retained knowledge**
- **Cyan = second technical dimension / alternate representation**
- On white, `#00B0F0` has about **2.48:1** contrast. Use `#007C9B` (about **4.82:1**) for cyan words or values students must read; keep bright cyan for outlines, arrows, or large nonessential marks.
- **Red = current attention target only**
- If red appears everywhere, the focus system stops working.
- Yellow/orange/green from screenshots or imported diagrams are **not** theme colors unless the lesson itself requires them.

---

## 5. Composition and spacing

### 5.1 Default hierarchy

Every slide should normally contain only three hierarchy levels:

1. **Teaching title** at top
2. **Primary visual or concept structure** in the middle
3. **One explanatory layer** — caption, bullets, labels, or spotlight statement

Avoid adding multiple competing card rows, badges, decorative icons, gradients, and unnecessary shadows.

### 5.2 White space

Negative space is an active teaching device in this deck.

- Sparse question slides are allowed to contain **only a title**.
- Do not “fill empty space” just because it is available.
- The most important visual should have breathing room around it.

### 5.3 Alignment

- Default alignment is **left** for titles and prose.
- Center alignment is reserved for:
  - cover title/subtitle
  - small labels beneath image grids
  - compact numeric/range bars
  - focused statements when used as a deliberate spotlight
- Use consistent vertical baselines across image grids and comparison columns.

### 5.4 Columns

Recommended native compositions:

- **2-column:** image/evidence on one side, explanation on the other
- **3–4 visual columns:** examples of languages, symbols, or categories, with labels below
- **4-step horizontal flow:** evenly spaced stages with short headings and arrows
- **Full-width evidence image:** screenshot/infographic with subsequent focus slides

Avoid a generic corporate “six equal cards” layout; it is not part of this visual language.

---

## 6. Master-frame treatment

The **top and bottom violet rails are non-negotiable** for normal slides.

- Color: `#6251B1`
- Thickness: 8 pt (approximately `0.1111 in`)
- Top rail: filled rectangle at `x=0`, `y=0`, `w=13.333`, `h=8 pt`
- Bottom rail: filled rectangle at `x=0`, `y=7.5 in − 8 pt`, `w=13.333`, `h=8 pt`
- Both rails meet the canvas edge and stay within the canvas; do not use an off-canvas line stroke to simulate bleed
- No additional colored sidebar, logo banner, or footer bar
- No visible slide number/footer in the reference visual style

This thin two-rail frame gives the deck a recognizable identity while leaving the rest of the canvas neutral.

---

## 7. Student-facing vs teacher-facing content

Every piece of information should be classified before it is placed.

### 7.1 Student-facing content

The slide itself contains only what students need to see **at that moment** to think, predict, observe, compare, calculate, discuss, or form a conclusion.

Typical student-facing content:

- the current question;
- necessary givens;
- neutral evidence required to attempt the question;
- diagrams and examples;
- concise experiment/activity instructions;
- code students are expected to read or manipulate;
- key values;
- the conclusion only **after** students have had time to think.

A slide is not a teacher handout.

### 7.2 Teacher-facing content

Move teacher guidance to Speaker Notes rather than occupying student visual space.

Typical teacher-facing content:

- internal navigation identifiers such as `Q1-A`, `Q3`, `Q9`;
- teaching intention;
- teacher transcript;
- expected student responses;
- follow-up questions;
- misconceptions;
- timing;
- technical caveats;
- source URLs;
- demo instructions and fallback plans;
- troubleshooting;
- answers or hints that would spoil the current question.

Before putting information on the slide, ask:

```text
Does the student need to see this now?
Does it help the student think, or tell the student what to think?
Will it spoil the question?
Is it mainly guidance for the teacher?
```

If it is useful to the teacher but unnecessary for the student at that moment, keep it in Speaker Notes.

---

## 8. Question-only slide and answer slide

Every major classroom question should first appear on its **own question slide**.

The purpose is to create a clean thinking pause.

### 8.1 Question slide

The question slide must not expose:

- the answer;
- clues that effectively reveal the answer;
- the conclusion;
- completed calculations;
- answer-colored emphasis;
- explanatory diagrams that give away the inference;
- teacher annotations or follow-up prompts.

It may contain only:

- the question itself;
- necessary givens;
- a neutral evidence image/table if the question cannot be attempted without it;
- concise task instructions.

Sparse question slides containing only the question title are encouraged.

### 8.2 Answer / explanation slide

Create the next slide by **duplicating the question slide**, not by rebuilding it.

Keep the question visually fixed:

- same wording;
- same font family and weight;
- same font size;
- same x/y position;
- same text-box width and height;
- same alignment;
- same line breaks where practical;
- same surrounding base geometry.

Then reveal the answer, evidence, explanation, or worked reasoning.

Preferred pattern:

```text
Question-only slide
        ↓ duplicate
Same question in exactly the same place
+ answer / evidence / explanation
        ↓ duplicate if needed
+ one additional teaching focus
```

The transition should minimize visual noise so students notice the **new information**, not a shifting layout.

---

## 9. Image and screenshot language

### 9.1 Images are evidence

Images are used to answer a teaching question:

- historical photo → establishes context
- standards webpage screenshot → proves a formal standard exists
- character chart → makes an abstract encoding concrete
- code/binary table → shows structure
- multilingual examples → demonstrates the limitation of a local character set

Do not add stock imagery merely to make a slide “more visual.”

### 9.2 Image treatment

- Use clean rectangular crops.
- Preserve source aspect ratio whenever possible.
- Avoid drop shadows, glossy frames, thick rounded borders, and decorative photo masks.
- White space around images is preferable to decorative containers.
- If a source screenshot already has a strong visual frame, let it stand on its own.
- Check screenshots at actual slide size. If students must read values that are too small, recreate the relevant excerpt as a native table or diagram and put the source in Speaker Notes.

### 9.3 Multi-image comparison

For 3–4 examples in one row:

- use equal or optically balanced heights
- align top and bottom edges
- put a short centered label below each image
- use muted gray for labels unless one example is active
- do not add background cards behind every image

### 9.4 Screenshot focus box

A signature technique is the **3 pt red focus rectangle**.

Use:

- stroke: `#FF0000`
- width: **3 pt**
- fill: none
- square corners

Purpose: identify the exact part of a screenshot, infographic, character table, or timeline being discussed **on this slide**.

### 9.5 Generated teaching illustrations

Generated imagery is allowed, but it must serve a specific teaching purpose.

Use this decision rule:

| Need | Preferred visual source |
|---|---|
| Prove a fact, standard, software behavior, or historical artifact | Real screenshot / primary-source image |
| Show exact technical relationships, values, bytes, code, or labels | Native PPT diagram / table / code |
| Create a situation, analogy, cognitive conflict, or human context | Generated illustration |

Core rule:

> **Generated images illustrate; native diagrams and real screenshots prove.**

For generated illustrations:

- define the teaching purpose before generation;
- generate for the intended slide crop/aspect ratio;
- prefer white or very light neutral backgrounds that integrate with the Violet-Rail canvas;
- keep composition simple and leave deliberate negative space for native PPT labels;
- normally do **not** ask the image model to render Chinese explanatory text, binary strings, byte values, arrows, legends, or conclusions;
- add all precise teaching labels and annotations as native PPT objects;
- do not use generated software UI or generated standards pages as evidence;
- use clean rectangular crops with no shadow, glossy frame, decorative mask, or card background;
- verify that incidental visual details do not introduce technical misconceptions;
- preserve the exact prompt used to generate every production image.

Prompt provenance should be stored in the slide's Speaker Notes under `[图片生成提示词]` and/or in a lesson-local `assets/generated/image-prompts.md`.

Use the reusable prompt patterns and examples in `image-generation-prompts.md`.

---

## 10. Progressive disclosure / “build” technique

This is one of the strongest signatures of the deck.

### Preferred implementation

Instead of complex PowerPoint animation:

1. Duplicate the previous slide.
2. Keep the base visual fixed.
3. Add or move a **red focus box**, **dark spotlight panel**, or **white thesis statement**.
4. Advance to the next slide.

This creates a controlled teaching sequence and remains robust when exported to PDF, viewed online, or generated programmatically.

### Typical sequence

**Base slide → Focus slide → Explanation slide → Next focus**

Examples of this pattern in the reference deck include:

- ASCII control vs printable regions
- keyboard → IME → code point → byte sequence → glyph rendering
- Unicode definition and purpose
- Unicode-space utilization
- UTF historical timeline and successive engineering problems

### Rule

Only **one new teaching focus** should change between consecutive build slides.

---

## 11. Native diagrams

### 11.1 Relationship diagram

Use simple semantic shapes rather than decorative infographics.

Typical language:

- cloud / organic shape = abstract character set
- code table / screenshot = concrete encoding table
- simple arrow = mapping or transformation
- double-headed arrow = relationship or mapping in both directions
- violet text/arrow = currently important concept

Keep fills white or none; use outlines and typography to carry the structure.

### 11.2 Process flow

For a 4-step technical process:

- horizontal sequence
- short numbered headings, e.g. `1. 输入码`, `2. IME翻译→码位`
- arrows between stages
- supporting text directly below each stage
- use violet for key intermediate concepts and values
- keep the flow visually linear; do not force everything into boxes

### 11.3 Bit / binary explanation

The deck's technical diagrams use **outline-first** styling:

- bits in small white boxes
- 3 pt violet/cyan/red outlines for important positions
- black for ordinary digits
- accent color only on the changed or significant bit(s)
- use monospaced alignment behavior visually, but keep Alibaba PuHuiTi 3.0 as the actual deck font unless a true code font is necessary for readability

### 11.4 Timelines

- thin neutral horizontal line
- small year/event groups above or below
- compact labels (often 14 pt)
- selected era outlined with a **red 3 pt rectangle**
- detailed explanation appears below or in a dark overlay
- keep the timeline visible across successive slides so students retain temporal context

---

## 12. Slide archetypes / recipes

### A. Cover slide

**Use for:** lesson/module opening.

- White background + violet rails
- Centered title, 60 pt Black
- Highlight one keyword in `#8C64E1`
- Subtitle 37 pt Regular, gray
- Large amount of negative space
- No image required

### B. Question + hero evidence

**Use for:** creating curiosity.

- 36 pt question title
- one dominant image or illustration below
- minimal extra text
- visual should directly embody the question

### C. Historical context slide

**Use for:** person, invention, origin story.

- thesis-like title across the top
- one historical image + one supporting diagram/table
- highlight the key term in violet
- keep captions small and factual

### D. Definition / mapping slide

**Use for:** `字符集 ↔ 编码方式`, `Unicode ↔ UTF`.

- title
- left-side abstract set/cloud
- right-side encoding table or list
- simple arrow(s) between them
- violet for the currently introduced concept
- little or no decorative fill

### E. Category/range slide

**Use for:** ASCII ranges, code-point regions.

- title
- large horizontal range bars / category labels
- explanatory arrows down to evidence/table
- focus rectangle around the relevant region
- repeat the slide to move attention to the next region

### F. Technical design-insight slide

**Use for:** “ASCII design trick,” bit manipulation, binary structure.

- declarative title
- one explanatory sentence under title
- evidence table on left
- compact bit diagram on right
- use violet/cyan outlines on important bits only

### G. Practice / exercise slide

**Use for:** short in-class reasoning task.

- title framed as an instruction/question
- split into 2 columns if comparing two cases
- code/binary lines aligned cleanly
- answer can be revealed on a duplicated follow-up slide

### H. Multi-language / multi-example slide

**Use for:** breadth or limitation demonstrations.

- 3–4 images in one row
- labels below each image
- consistent crop heights
- no cards behind images
- optional red focus box on the subset currently discussed

### I. Process flow slide

**Use for:** input → transformation → output.

- four stages across the canvas
- short step title + concise explanation + example/value per step
- arrows between steps
- key terms in violet
- duplicate for a full-flow spotlight slide if needed

### J. Website / standards evidence slide

**Use for:** standards body, official tool, technical specification.

- title explains what the evidence proves
- large screenshot, often full width or dominant
- Source URL small and unobtrusive unless students must use it; follow §17 for student-action links
- next slide can place a dark overlay or red focus box over the relevant region

### K. Sparse pause / debate slide

**Use for:** reset attention before a major comparison.

- 36 pt question title only
- keep the rest of the slide blank
- no decorative filler

### L. Timeline + problem/solution sequence

**Use for:** evolution of standards/technology.

- title + one-line thesis in violet
- persistent timeline in upper third
- lower area contains the current era's engineering context/problem
- successive slides move the red focus box along the timeline
- dark overlay introduces the “problem that forced the next solution”

### M. Summary slide

**Use for:** synthesis of a long technical sequence.

- summary title
- compact table/timeline/comparison below
- retain the same visual language as the teaching slides; do not switch to a new decorative “conclusion template”

---

## 13. Callouts and overlays

### Strong dark thesis callout

Use when the instructor needs to stop the narrative and state the main conclusion.

- dark translucent rectangle
- white 32–36 pt Black text
- one sentence, preferably 1–2 lines
- align left unless the statement is intentionally centered
- no border
- provide enough vertical headroom for Chinese line wrapping in WPS / PowerPoint
- if the statement wraps unexpectedly, enlarge the box, shorten the wording, or split the slide; do not shrink the key statement merely to make it fit

### Red focus outline

Use only to indicate **where to look**.

- `#FF0000`, 3 pt, no fill
- never use as a generic card border

### Violet outline

Use to indicate a **conceptual group or changed bit**, not a temporary attention target.

- `#8C64E1`, 3 pt
- white/no fill

### Cyan outline

Use when a second technical category must be visually distinct from violet.

- `#00B0F0`, 3 pt
- white/no fill

---

## 14. Content-density rules

The deck sometimes intentionally becomes dense in later technical/history slides, but that should be treated as an exception.

### Preferred density

- one main idea per slide
- body text normally 22 pt
- 14 pt only for timelines, data labels, source details, or content that is already supported by a strong visual hierarchy
- keep paragraphs short; convert long explanations into a build sequence

### Do not copy these as defaults

- 14 pt as normal body text
- full paragraphs covering most of the slide
- tiny text embedded in screenshots as the only source of meaning
- several simultaneous red focus boxes

If students must read it from the back of a classroom, enlarge it or split it into another slide.

---

## 15. Language and instructional tone

The reference deck is **Chinese-first with precise English technical vocabulary**.

Recommended pattern:

- Chinese explanation + original English technical name where useful
- preserve common abbreviations (`ASCII`, `Unicode`, `UTF`, `IME`, `Code Point`)
- explain the *why* before the formal definition when possible
- use rhetorical questions to create transitions
- make contrasts explicit: `字符集` vs `字符编码方式`, `码位` vs `字节`, `Unicode` vs `UTF`

The visual style works best when the written content follows a **problem → evidence → abstraction → explanation → recap** rhythm.

---

## 16. Speaker Notes

Every teaching slide must contain Speaker Notes.

Speaker Notes are the **teacher-facing teaching script**, not optional annotations.

### 16.1 Start with the full question / page purpose

At the beginning of the notes, write the complete classroom question or page purpose. Do not use only an internal identifier.

Preferred:

```text
[问题]
ASCII 是 7 bit，为什么计算机中常常看到 8 bit？

[内部编号]
Q3
```

Avoid:

```text
Q3
```

Internal Q numbers are navigation metadata for the teacher and normally should not appear on the student-facing slide.

### 16.2 Recommended note structure

Use the relevant parts of:

```text
[问题 / 页面目的]
[内部编号]
[教学意图]
[教师逐字稿]
[预期学生反应]
[追问问题]
[形成结论]
[Demo 操作]
[技术注解]
[来源]
```

Not every slide needs every subsection, but every teaching slide needs a usable transcript.

### 16.3 Transcript quality

The transcript should sound like language a teacher can actually say aloud.

It should:

- sound natural rather than formal or generated;
- create curiosity before giving the explanation;
- invite students to predict, compare, vote, argue, observe, calculate, or explain;
- include pauses for thinking;
- respond to likely student answers and use them to move the lesson forward;
- refer to what students are seeing on the slide or in the demo;
- connect naturally to the previous and next question;
- keep technical caveats teacher-facing when students do not need them yet.

Do not merely read the slide aloud.

Weak:

> “ASCII 是 7 bit。这里显示 8 bit。最高位是 0。”

Better:

> “先别算。ASCII 明明只有 128 个位置，7 bit 已经够了。那为什么文件里我们偏偏看到 8 bit？多出来的这一位到底从哪儿来的？先看 A，谁能指出那一位在哪里？”

### 16.4 Follow-up questions

Follow-up questions normally belong in Speaker Notes unless students must read them directly.

Use follow-up questions to:

- explain an observation;
- challenge a premature conclusion;
- connect evidence to a concept;
- compare two cases;
- transfer the idea to a new situation.

---

## 17. Source and citation behavior

- Put research/source URLs primarily in **speaker notes** when they are for instructor reference.
- If students must visit a site, show a short URL or QR code with a human-readable address at **22 pt or larger**. Keep the full URL in Speaker Notes.
- If a webpage screenshot is evidence, a visible source address may be **12–14 pt** as provenance only; students should not have to read or type that small text to complete the task.

---

## 18. What is NOT part of the core style

Do not infer theme rules from imported content.

The following may appear in the reference deck but should **not** become global style rules:

- colors inside screenshots of standards websites
- colors inside AI-generated or historical illustrations
- grayscale historical photos
- third-party infographic palettes
- webpage fonts
- decorative icon styles from external images

The native deck style remains **white + violet rails + black Alibaba typography + violet/cyan/red semantic annotation**.

---

## 19. Do / Don't

### Do

- use the same master frame on every normal slide
- use Alibaba PuHuiTi 3.0 consistently
- keep slide titles strong and narrative
- use images as evidence
- use red only as a moving focus marker
- duplicate slides for progressive disclosure
- preserve generous white space
- use simple arrows, rectangles, cloud shapes, and labels
- make one conceptual change per build slide

### Don't

- use gradient backgrounds
- add corporate-style rounded cards everywhere
- add shadows/glows merely for decoration
- use many unrelated accent colors
- use red as a general brand color
- center all body text
- switch fonts for English technical terms
- fill every empty area
- rely on animation for essential meaning
- shrink normal body copy to 14 pt just to fit more content

---

## 20. Quick implementation spec for automated slide generation

Use this block as a compact generation contract:

```text
CANVAS
- 16:9, 13.333 x 7.5 in
- background #FFFFFF
- top rail: filled #6251B1 rectangle x=0, y=0, w=13.333, h=8 pt
- bottom rail: filled #6251B1 rectangle x=0, y=7.5 in - 8 pt, w=13.333, h=8 pt
- rails meet the edges without extending outside the canvas

FONT
- Alibaba PuHuiTi 3.0 only for native deck text
- check the rendered font, not only the PPTX font name
- if 85 Bold is substituted, use 115 Black for emphasis or 55 Regular for ordinary text and rerender
- cover: 115 Black 60 pt; subtitle 55 Regular 37 pt gray
- slide title: 115 Black 36 pt, near-black #262626, left
- body: 55 Regular 22 pt, black, 1.3 line spacing
- strong label: 115 Black 24 pt
- spotlight: 115 Black 32–36 pt white
- nonessential micro/timeline/source: 12–14 pt; student-action URL: 22 pt minimum

GRID
- standard left margin 0.665 in
- one-line title: x=0.665, y=0.665, w≈12.0, h≈0.77 in; content starts y≈1.63 in
- two-line title: same x/y/w and 36 pt, h=1.35 in; content starts y=2.25 in
- keep the chosen title variant and line break fixed across a question/answer pair
- keep most content inside x=0.665..12.665 and y=1.63..6.84 for one-line titles
- for two-line titles, keep most content inside x=0.665..12.665 and y=2.25..6.84

COLORS
- frame violet #6251B1
- teaching violet #8C64E1
- technical cyan #00B0F0 for outlines/arrows; readable cyan text #007C9B on white
- focus red #FF0000
- title #262626
- body #000000
- muted gray #808080

ANNOTATION
- focus rectangle: no fill, red #FF0000, 3 pt
- conceptual outline: no fill, violet #8C64E1, 3 pt
- secondary outline: no fill, cyan #00B0F0, 3 pt
- spotlight overlay: near-black, 80–90% opacity, no border

STYLE
- white-space heavy
- technical/evidence-driven
- no shadows/gradients/card grids
- simple native geometry
- screenshots/photos are rectangular and unornamented
- progressive disclosure via duplicated slides, not required animations
```

---

## 21. Layout QA workflow

A generated deck is **not finished** merely because the PPTX file was created successfully.

Production acceptance requires visual inspection.

### 21.1 Slide plan before production

Make a one-row-per-slide plan from `course-design.qmd` before building the PPTX. Use the plan to check the teaching sequence, not to duplicate the full course design.

| Slide / build ID | Q ID and stage | Student sees now | Hold for later / Speaker Notes | Evidence, source, and focus target |
|---|---|---|---|---|
| `Q2-question` | Q2 · question | ASCII 表局部、寻找 `A` 的任务 | `A` 的码值与计算过程 | `A` 所在行列 |
| `Q2-answer` | Q2 · answer | 同一表格，加上 `A` 的行列合成 | Q3 的 7 bit / 8 bit 解释 | `A` 所在行列与新计算式 |

Use `question`, `evidence`, `focus`, `answer`, or `transition` for teaching stages. For a cover or exit slide, use `opening` or `exit` and record its page purpose in place of a Q ID. Before building, check that:

- every major Q has a question-only slide before its answer;
- each question slide contains the givens needed to attempt it, with no answer, effective hint, or teacher prompt;
- each reveal adds one current teaching focus while keeping the question and base geometry fixed;
- every significant item has an explicit student-facing or teacher-facing destination;
- each screenshot, table, and red focus mark has a stated teaching purpose and a readable target;
- technical claims, dates, and process diagrams match `course-design.qmd`; sources are available for claims that need them.

### 21.2 Required workflow

For every production PPTX:

1. build the deck from the slide plan;
2. compare the finished slide order and reveal stages with the slide plan and `course-design.qmd`;
3. render **every slide** to an image;
4. generate a full-deck montage;
5. inspect the montage for consistency;
6. inspect dense, diagram-heavy, question/answer, and overlay slides individually at full resolution; check that each red focus mark encloses the intended evidence;
7. run programmatic checks for out-of-canvas objects, rail geometry, font assignments, Speaker Notes presence, and stable question/answer coordinates where possible;
8. verify that all native text objects explicitly use the required Alibaba PuHuiTi 3.0 variant;
9. check the **rendered font** on Chinese, Latin, numeric, and symbol text; inspect the font list in a PDF export where available and check representative slides in WPS / PowerPoint. If a variant is substituted, apply the approved fallback in §3.1 and render again;
10. verify that question/answer pairs preserve their base geometry, including the chosen one-line or two-line title variant;
11. review student-visible text for premature answers and teacher-only instructions; verify that every teaching slide has usable Speaker Notes;
12. compare technical claims, dates, and process diagrams with the source design and cited references;
13. open the final deck in **WPS Presentation whenever practical** and check the actual classroom rendering;
14. fix all visible defects before delivery.

### 21.3 Deck acceptance record

Copy this compact record into the delivery note. Mark each row `pass`, `fail`, or `unverified`, with the evidence or reason. Resolve failures before calling the deck classroom-ready.

| Check | Result / evidence |
|---|---|
| Slide order, Q IDs, and reveal stages match the plan and `course-design.qmd` | |
| Question slides contain no premature answer or teacher-only text | |
| Evidence is readable and each red focus mark identifies its intended target | |
| Every slide was rendered; montage and dense slides were inspected | |
| Geometry, rails, fonts, and question/answer stability passed structural checks | |
| Speaker Notes, technical claims, dates, and sources were checked | |
| Final PPTX was inspected in WPS / PowerPoint | |

If the WPS / PowerPoint check was not practical, mark that row `unverified` and say why; a PDF or other renderer does not establish how the classroom app will display the file.

### 21.4 Reject these defects

A production deck is not classroom-ready if it contains:

- overlapping text;
- text covered by shapes;
- clipping;
- unexpected Chinese wrapping;
- content outside its intended text box;
- content entering the violet rails or unsafe margins;
- unintended font substitution, especially one that changes line breaks or hierarchy;
- stretched screenshots;
- inconsistent title positions;
- question/answer geometry drift;
- auto-fit shrinking important text;
- dark overlays with insufficient height for the statement.

### 21.5 Text-box rule

Do not assume a text box fits because the source string fits programmatically.

WPS and PowerPoint may wrap Chinese differently because of font availability, line spacing, and rendering differences.

When a text block does not fit:

1. enlarge the text box;
2. shorten the student-facing wording;
3. move complementary material to Speaker Notes;
4. or split the content across slides.

Do **not** reduce normal teaching text below the style standard merely to force it into the available space.

Successful rendering is not the definition of done. **Classroom usability is.**

---

## 22. Quality-control checklist

Before accepting a generated slide, verify:

- [ ] Violet top and bottom rail rectangles meet the canvas edges and do not extend outside it.
- [ ] All native text explicitly uses Alibaba PuHuiTi 3.0, and the rendered font has been checked for substitution.
- [ ] Title is 36 pt Black and uses the specified one-line or two-line geometry without auto-fit.
- [ ] Normal body text is not below 22 pt unless it is legitimately timeline/source/micro text.
- [ ] One clear visual focus exists.
- [ ] Violet, cyan, and red are being used semantically, not decoratively.
- [ ] Essential cyan text on white uses the darker readable cyan; bright cyan is limited to outlines, arrows, or large highlights.
- [ ] Red appears only on the item students should inspect now.
- [ ] Images are evidence and are not placed in decorative cards.
- [ ] Generated images are used only for illustration/analogy/context, not as substitutes for factual evidence or exact technical diagrams.
- [ ] Every production generated image has a preserved exact prompt and a stated teaching purpose.
- [ ] Precise labels, byte values, arrows, and conclusions are native PPT objects rather than baked into generated imagery.
- [ ] There are no unnecessary gradients, drop shadows, glows, or rounded UI panels.
- [ ] If the slide is part of a build sequence, the base geometry remains fixed across slides.
- [ ] The slide can still be understood when exported to PDF with no animation.
- [ ] Imported screenshots do not redefine the deck's native palette or font system.
- [ ] The title advances the teaching story rather than merely naming a topic.
- [ ] Question-only slides do not leak answers, clues, conclusions, or teacher prompts.
- [ ] Question/answer slide pairs keep the question typography and geometry fixed.
- [ ] Internal Q labels and follow-up questions are teacher-facing unless students genuinely need them.
- [ ] Every teaching slide has a usable Speaker Notes transcript beginning with the full question/page purpose.
- [ ] A URL students must visit is readable from the classroom; full research URLs remain in Speaker Notes.
- [ ] Dense or wrapping-prone text has enough vertical headroom for WPS / PowerPoint.
- [ ] The full deck has been rendered, montaged, and visually inspected before delivery.

---

## 23. One-sentence style definition

> **A white, violet-framed technical teaching deck using bold Alibaba PuHuiTi 3.0 typography, evidence-rich screenshots/diagrams, semantic violet–cyan–red annotation, and slide-by-slide progressive focus to explain abstract computing concepts clearly.**
