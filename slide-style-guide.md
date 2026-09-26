# Slide Style Guide

**Style name:** Violet-Rail Technical Explainer / 紫色轨道式技术讲解风格  
**Primary use:** 高中信息科技、Python / CS 入门、概念讲解、技术史与原理课件  
**Font family:** Alibaba PuHuiTi 3.0

This guide is the mandatory visual specification for production PPTX decks in this project.

---

## 1. Style identity

The deck is a minimal, classroom-oriented technical explainer built around five traits:

1. **White canvas + violet top/bottom rails**.
2. **Large, bold, left-aligned teaching titles**.
3. **Evidence-heavy visuals**: screenshots, tables, standards pages, diagrams, code, binary examples.
4. **Semantic color**: violet for concepts, cyan for alternate technical category, red for current focus.
5. **Progressive disclosure by duplicated slides**.

The overall feeling should be clear, rigorous, modern, and teacher-led. Avoid corporate, glossy, playful, card-heavy styles.

---

## 2. Canvas and master geometry

Use 16:9 widescreen, **13.333 × 7.5 in**.

| Element | Position / size | Rule |
|---|---:|---|
| Top rail | y ≈ 0.05 in, full bleed | 8 pt, `#6251B1` |
| Bottom rail | y ≈ 7.45 in, full bleed | 8 pt, `#6251B1` |
| Slide title | x=0.665, y=0.665, w≈12.0, h≈0.77 in | Left aligned |
| Main content area | x=0.665, y=1.63, w≈12.0, h≈5.21 in | Default working region |
| Left/right safe margin | ≈0.67 in | Keep native content inside this margin |

Rails must extend slightly beyond slide edges so they bleed cleanly.

No visible slide number/footer in the production visual style.

---

## 3. Typography

Use **Alibaba PuHuiTi 3.0** throughout native slide content.

Preferred variants:

- Alibaba PuHuiTi 3.0 115 Black — titles, strong labels, large callouts.
- Alibaba PuHuiTi 3.0 85 Bold — technical emphasis.
- Alibaba PuHuiTi 3.0 55 Regular — body copy, captions, explanations.

Do not mix another Chinese UI font for native slide content. Imported screenshots may contain other fonts because they are evidence.

| Role | Font | Size | Color / treatment |
|---|---|---:|---|
| Cover title | 115 Black | 60 pt | Near-black |
| Cover subtitle | 55 Regular | 37 pt | Gray `#808080` |
| Standard slide title | 115 Black | 36 pt | Near-black `#262626` |
| Standard body | 55 Regular | 22 pt | Black |
| Strong content label | 115 Black | 24 pt | Black / white |
| Technical bold body | 85 Bold | 22 pt | Black |
| Spotlight / thesis overlay | 115 Black | 32–36 pt | White on dark panel |
| Dense diagram / timeline text | 85 Bold or 55 Regular | 14 pt | Use sparingly |
| Source / micro-note | 55 Regular | 12–14 pt | Gray / black |

Do not reduce normal teaching text below 22 pt merely to make content fit. Split the slide.

---

## 4. Title-writing style

Titles are part of the teaching narrative. Prefer questions, claims, contradictions, or conceptual contrasts.

Good examples:

- `ASCII 是 7 bit，为什么计算机中常常看到 8 bit？`
- `汉字真的总是占 2 byte 吗？`
- `同一个“你”，为什么可以对应不同的 byte sequence？`

Avoid generic titles such as `知识点`, `背景介绍`, `第三部分` unless they have a structural purpose.

---

## 5. Color system

| Semantic role | Hex | Usage |
|---|---|---|
| Frame Violet | `#6251B1` | Top/bottom rails only |
| Teaching Accent Violet | `#8C64E1` | Key concepts, arrows, bit boxes, highlighted headings |
| Technical Cyan | `#00B0F0` | Secondary representation/category |
| Focus Red | `#FF0000` | Current attention target only |
| Title near-black | `#262626` | Titles |
| Body black | `#000000` | Main text |
| Muted gray | `#808080` | Captions / secondary labels |
| White | `#FFFFFF` | Background and text on dark overlays |

Semantic rules:

```text
Violet → concept / relationship / retained knowledge
Cyan   → second technical dimension / alternate representation
Red    → where students should look right now
```

Red is not decorative. Normally there should be only one current red focus.

---

## 6. Composition

Every slide should normally have only three hierarchy levels:

1. Teaching title.
2. Primary visual or concept structure.
3. One explanatory layer.

Avoid:

- grids of rounded cards;
- decorative icons;
- gradients;
- shadows;
- glass effects;
- large colored sidebars;
- dashboard layouts;
- excessive badges;
- unrelated accent colors.

White space is an active teaching device. Do not fill empty space because it is available.

---

## 7. Student-facing content

Slides contain only what students need to see at that moment:

- current question;
- necessary givens;
- essential evidence;
- diagrams;
- examples;
- short experiment instructions;
- key values;
- conclusion after students have had time to think.

Teacher-facing material belongs in Speaker Notes:

- teaching transcript;
- expected answers;
- misconceptions;
- technical caveats;
- source URLs;
- troubleshooting;
- answers or hints that would spoil the question.

A slide is not a teacher handout.

---

## 8. Question-only slide and answer slide

Every major question should first appear on a **question-only slide**.

The question slide must not expose:

- the answer;
- clues that effectively reveal the answer;
- the conclusion;
- completed calculations;
- explanatory diagrams that give away the inference.

The next slide reveals answer/evidence/reasoning. It must be created by duplicating the question slide and preserving the question's:

- font family;
- font size;
- weight;
- x/y position;
- text box width and height;
- alignment;
- line breaks where practical;
- surrounding base geometry.

Preferred pattern:

```text
Question-only slide
        ↓ duplicate
Same question in exactly the same place
+ answer / evidence / explanation
        ↓ duplicate
+ one new focus at a time
```

This reduces visual noise during slide switching.

---

## 9. Progressive disclosure

Prefer duplicated slides over complicated animation.

Use:

```text
base slide
    ↓
same geometry + red focus
    ↓
same geometry + explanation
    ↓
move focus to next item
```

Only one major teaching focus should change between consecutive build slides.

This is especially important for:

- ASCII tables;
- binary / bit structures;
- WinHex screenshots;
- input → IME → character → glyph flows;
- Unicode / UTF explanations;
- standards timelines.

---

## 10. Evidence visuals

Images, screenshots, standards pages, tables, and code are evidence, not decoration.

Use clean rectangular crops. Preserve aspect ratio. Avoid drop shadows, thick rounded borders, glossy frames, and decorative masks.

Screenshot focus box:

- stroke: `#FF0000`;
- width: 3 pt;
- fill: none;
- square corners.

The red box should identify the exact part being discussed on this slide.

---

## 11. Dark spotlight overlay

Use a dark overlay only as a temporary teaching spotlight.

- Fill: `#171717` to `#222222`.
- Opacity: 80–90%.
- No border.
- Text: white, 32–36 pt, 115 Black.
- Provide enough vertical height to prevent clipping in WPS / PowerPoint.

Do not compress large conclusions into a too-short box. If it wraps, enlarge the box, shorten wording, or split the slide.

---

## 12. Speaker Notes

Every teaching slide must contain Speaker Notes.

Notes must include a usable teacher transcript. They may also contain:

```text
[教学意图]
[教师逐字稿]
[预期学生回答]
[追问]
[技术注解]
[来源]
[Demo 操作]
```

Do not crowd the student slide with information that belongs in Speaker Notes.

---

## 13. Layout QA

A generated deck is not finished until it is visually checked.

Before delivery:

1. Render every slide to an image.
2. Generate a montage.
3. Inspect the montage.
4. Inspect dense/diagram-heavy slides at full resolution.
5. Check for objects outside the slide canvas.
6. Open in WPS whenever practical.
7. Verify Speaker Notes.
8. Fix all visible layout defects.

Reject decks with:

- overlap;
- clipping;
- text covered by shapes;
- unexpected wrapping;
- content entering rails or unsafe margins;
- stretched screenshots;
- inconsistent alignment;
- auto-fit shrinking key text.

Successful rendering is not the definition of done. Classroom usability is.
