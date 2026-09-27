# Slide Style Guide

**Reference deck:** `上1-2-3-1 字符编码.pptx`  
**Style name:** **Violet-Rail Technical Explainer / 紫色轨道式技术讲解风格**  
**Primary use:** 高中信息科技、Python / CS 入门、概念讲解、技术史与原理课件  
**Font family:** **Alibaba PuHuiTi 3.0**

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

## 2. Reference-deck anatomy

- **Canvas:** 16:9 widescreen, **13.333 × 7.5 in**.
- **44 slides** in the reference deck.
- **43/44 slides** use the same **Title + Content** layout; only the opening slide uses the title-slide layout.
- The deck therefore behaves like a **single disciplined teaching canvas**, not a collection of many unrelated PowerPoint templates.
- The reference file contains many native shapes plus a large number of screenshots/images; visuals are treated as teaching evidence rather than decoration.

### Core master geometry

| Element | Position / size | Rule |
|---|---:|---|
| Top rail | `y ≈ 0.05 in`, full bleed | 8 pt, `#6251B1` |
| Bottom rail | `y ≈ 7.45 in`, full bleed | 8 pt, `#6251B1` |
| Slide title | `x=0.665`, `y=0.665`, `w≈12.0`, `h≈0.77 in` | Left aligned |
| Main content area | `x=0.665`, `y=1.63`, `w≈12.0`, `h≈5.21 in` | Default working region |
| Left/right safe margin | `≈0.67 in` | Keep native content inside this margin unless a screenshot intentionally bleeds wider |

**Important:** the rails should extend slightly beyond the slide edges so they visually bleed cleanly from edge to edge.

---

## 3. Typography

### 3.1 Font family and weights

Use **Alibaba PuHuiTi 3.0** throughout native slide content.

Preferred variants seen in the deck:

- **Alibaba PuHuiTi 3.0 115 Black** — titles, strong labels, large callouts
- **Alibaba PuHuiTi 3.0 85 Bold** — dense technical emphasis, code-related explanation, secondary strong text
- **Alibaba PuHuiTi 3.0 55 Regular** — body copy, captions, explanatory text

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
| Technical bold body | 85 Bold | **22 pt** | Black |
| Spotlight / thesis overlay | 115 Black | **32–36 pt** | White on dark translucent panel |
| Dense diagram / timeline text | 85 Bold or 55 Regular | **14 pt** | Black; use sparingly |
| Source / URL / micro-note | 55 Regular | **12–14 pt** | Gray or black |

### 3.3 Master text behavior

**Standard slide title**

- 36 pt, 115 Black
- left aligned
- 100% line spacing
- slightly expanded character spacing (reference master uses approximately **+3 pt**)
- no bullet
- color is slightly softened from pure black (`≈#262626`)

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
| **Technical Cyan** | `#00B0F0` | Secondary category, alternate bit/encoding distinction |
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
- Width: 8 pt
- Top rail: almost flush to top edge
- Bottom rail: almost flush to bottom edge
- No additional colored sidebar, logo banner, or footer bar
- No visible slide number/footer in the reference visual style

This thin two-rail frame gives the deck a recognizable identity while leaving the rest of the canvas neutral.

---

## 7. Image and screenshot language

### 7.1 Images are evidence

Images are used to answer a teaching question:

- historical photo → establishes context
- standards webpage screenshot → proves a formal standard exists
- character chart → makes an abstract encoding concrete
- code/binary table → shows structure
- multilingual examples → demonstrates the limitation of a local character set

Do not add stock imagery merely to make a slide “more visual.”

### 7.2 Image treatment

- Use clean rectangular crops.
- Preserve source aspect ratio whenever possible.
- Avoid drop shadows, glossy frames, thick rounded borders, and decorative photo masks.
- White space around images is preferable to decorative containers.
- If a source screenshot already has a strong visual frame, let it stand on its own.

### 7.3 Multi-image comparison

For 3–4 examples in one row:

- use equal or optically balanced heights
- align top and bottom edges
- put a short centered label below each image
- use muted gray for labels unless one example is active
- do not add background cards behind every image

### 7.4 Screenshot focus box

A signature technique is the **3 pt red focus rectangle**.

Use:

- stroke: `#FF0000`
- width: **3 pt**
- fill: none
- square corners

Purpose: identify the exact part of a screenshot, infographic, character table, or timeline being discussed **on this slide**.

---

## 8. Progressive disclosure / “build” technique

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

## 9. Native diagrams

### 9.1 Relationship diagram

Use simple semantic shapes rather than decorative infographics.

Typical language:

- cloud / organic shape = abstract character set
- code table / screenshot = concrete encoding table
- simple arrow = mapping or transformation
- double-headed arrow = relationship or mapping in both directions
- violet text/arrow = currently important concept

Keep fills white or none; use outlines and typography to carry the structure.

### 9.2 Process flow

For a 4-step technical process:

- horizontal sequence
- short numbered headings, e.g. `1. 输入码`, `2. IME翻译→码位`
- arrows between stages
- supporting text directly below each stage
- use violet for key intermediate concepts and values
- keep the flow visually linear; do not force everything into boxes

### 9.3 Bit / binary explanation

The deck's technical diagrams use **outline-first** styling:

- bits in small white boxes
- 3 pt violet/cyan/red outlines for important positions
- black for ordinary digits
- accent color only on the changed or significant bit(s)
- use monospaced alignment behavior visually, but keep Alibaba PuHuiTi 3.0 as the actual deck font unless a true code font is necessary for readability

### 9.4 Timelines

- thin neutral horizontal line
- small year/event groups above or below
- compact labels (often 14 pt)
- selected era outlined with a **red 3 pt rectangle**
- detailed explanation appears below or in a dark overlay
- keep the timeline visible across successive slides so students retain temporal context

---

## 10. Slide archetypes / recipes

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
- URL small and unobtrusive unless the URL is itself a learning resource
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

## 11. Callouts and overlays

### Strong dark thesis callout

Use when the instructor needs to stop the narrative and state the main conclusion.

- dark translucent rectangle
- white 32–36 pt Black text
- one sentence, preferably 1–2 lines
- align left unless the statement is intentionally centered
- no border

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

## 12. Content-density rules

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

## 13. Language and instructional tone

The reference deck is **Chinese-first with precise English technical vocabulary**.

Recommended pattern:

- Chinese explanation + original English technical name where useful
- preserve common abbreviations (`ASCII`, `Unicode`, `UTF`, `IME`, `Code Point`)
- explain the *why* before the formal definition when possible
- use rhetorical questions to create transitions
- make contrasts explicit: `字符集` vs `字符编码方式`, `码位` vs `字节`, `Unicode` vs `UTF`

The visual style works best when the written content follows a **problem → evidence → abstraction → explanation → recap** rhythm.

---

## 14. Source and citation behavior

- Put research/source URLs primarily in **speaker notes** when they are for instructor reference.
- Put URLs visibly on the slide only when students are expected to visit the tool/site or when the webpage itself is evidence in the lesson.
- Visible URLs should be 12–14 pt and visually secondary.

---

## 15. What is NOT part of the core style

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

## 16. Do / Don't

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

## 17. Quick implementation spec for automated slide generation

Use this block as a compact generation contract:

```text
CANVAS
- 16:9, 13.333 x 7.5 in
- background #FFFFFF
- top rail #6251B1, 8 pt, full bleed at y≈0.05 in
- bottom rail #6251B1, 8 pt, full bleed at y≈7.45 in

FONT
- Alibaba PuHuiTi 3.0 only for native deck text
- cover: 115 Black 60 pt; subtitle 55 Regular 37 pt gray
- slide title: 115 Black 36 pt, near-black #262626, left
- body: 55 Regular 22 pt, black, 1.3 line spacing
- strong label: 115 Black 24 pt
- spotlight: 115 Black 32–36 pt white
- micro/timeline/source: 12–14 pt

GRID
- standard left margin 0.665 in
- standard title top 0.665 in
- main content starts y≈1.63 in
- keep most content inside x=0.665..12.665 and y=1.63..6.84

COLORS
- frame violet #6251B1
- teaching violet #8C64E1
- technical cyan #00B0F0
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

## 18. Quality-control checklist

Before accepting a generated slide, verify:

- [ ] Violet top and bottom rails are present and identical to the master.
- [ ] All native text uses Alibaba PuHuiTi 3.0.
- [ ] Title is 36 pt Black and aligned to the common title baseline.
- [ ] Normal body text is not below 22 pt unless it is legitimately timeline/source/micro text.
- [ ] One clear visual focus exists.
- [ ] Violet, cyan, and red are being used semantically, not decoratively.
- [ ] Red appears only on the item students should inspect now.
- [ ] Images are evidence and are not placed in decorative cards.
- [ ] There are no unnecessary gradients, drop shadows, glows, or rounded UI panels.
- [ ] If the slide is part of a build sequence, the base geometry remains fixed across slides.
- [ ] The slide can still be understood when exported to PDF with no animation.
- [ ] Imported screenshots do not redefine the deck's native palette or font system.
- [ ] The title advances the teaching story rather than merely naming a topic.

---

## 19. One-sentence style definition

> **A white, violet-framed technical teaching deck using bold Alibaba PuHuiTi 3.0 typography, evidence-rich screenshots/diagrams, semantic violet–cyan–red annotation, and slide-by-slide progressive focus to explain abstract computing concepts clearly.**
