# Image Generation Prompts for Teaching Decks

**Status:** Reusable production prompt library for `shtick`.

This file defines the preferred prompt structure for generated teaching illustrations.

Core rule:

> **Generated images illustrate; native diagrams and real screenshots prove.**

Use generated imagery for situations, analogies, cognitive conflict, and human context. Use real screenshots or primary sources for evidence. Use native PPT shapes/tables/code for exact technical structures.

---

## 1. Prompt-writing contract

Before generating an image, write:

```text
Teaching purpose:
What should students notice, feel curious about, or understand from the image?

Slide role:
Question / cognitive conflict / analogy / transition / context

Intended placement:
Full-width hero / left column / right column / background

Aspect ratio:
16:9 / 4:3 / 1:1 / portrait
```

Then use this prompt structure:

```text
Create a classroom teaching illustration for a high-school information technology lesson.

Teaching purpose:
[ONE SENTENCE describing what students should notice or wonder about.]

Subject / scene:
[Describe the people, objects, or situation.]

Composition:
[Describe where the main subjects sit in the frame.]
[Specify deliberate empty space for PowerPoint text or annotations.]
[Specify intended aspect ratio.]

Visual style:
clean modern educational illustration
white or very light neutral background
minimal visual clutter
clear silhouettes and readable visual relationships
serious but friendly high-school classroom tone
consistent with a white technical teaching deck

Important constraints:
no explanatory text
no Chinese labels
no binary strings
no byte values
no arrows
no legends
no conclusions
no logos
no watermark
no decorative borders
no gradient background
no corporate infographic cards

Do not invent technical evidence.
Precise labels and technical annotations will be added later as native PowerPoint objects.
```

---

## 2. Cognitive-conflict hero image

Use when the slide opens a question and the illustration should create curiosity without revealing the answer.

### Exact reusable prompt

```text
Create a classroom teaching illustration for a high-school information technology lesson.

Teaching purpose:
Make students immediately notice an unexpected computing situation and want to explain why it happened, without revealing the technical cause.

Subject / scene:
A high-school student is using a computer and sees an unexpected result on the screen. The student's expression should show curiosity and mild confusion, not panic or frustration.

Composition:
The computer screen is the main visual focus.
Place the student slightly to the right of center.
Leave generous clean negative space in the upper-left and left-center areas for a PowerPoint question title and later native annotations.
Wide 16:9-compatible composition.

Visual style:
clean modern educational illustration
white or very light neutral background
minimal visual clutter
clear classroom setting
serious but friendly
subtle depth, not glossy
consistent with a white technical teaching deck

Important constraints:
no explanatory text
no Chinese labels
no binary strings
no byte values
no arrows
no legends
no conclusions
no logos
no watermark
no decorative borders
no gradient background
no corporate infographic cards

Do not invent technical evidence.
Any precise text or technical result on the computer screen will be added later as a native PowerPoint overlay.
```

---

## 3. Two-student comparison / secret-code activity

Use when two people apply different rules or mappings.

### Exact reusable prompt

```text
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
```

---

## 4. Mojibake / garbled-text mystery

Use for a character-encoding opening hook.

### Exact reusable prompt

```text
Create a clean conceptual illustration for a high-school information technology lesson about character encoding.

Teaching purpose:
Create a mystery: a student expected normal Chinese text but the computer appears to show unreadable or garbled text, prompting the question of where the representation went wrong.

Subject / scene:
A high-school student looks at a computer screen expecting a normal message.
The screen should visually suggest corrupted or garbled text, but the image itself should not contain readable technical strings or a specific encoding example.
The student's expression is curious and puzzled rather than upset.

Composition:
Make the computer display the dominant visual object.
Place the student toward the right side.
Leave substantial clean negative space on the upper-left side for a PowerPoint question title.
Wide 16:9 composition.

Visual style:
clean modern educational illustration
white or very light neutral background
minimal visual clutter
modern classroom
serious but approachable
consistent with a white technical teaching deck

Important constraints:
no readable Chinese sentence
no exact mojibake string
no byte values
no binary strings
no arrows
no explanatory labels
no conclusions
no logos
no watermark
no decorative frame
no gradient background

The real mojibake string and technical evidence will be overlaid later as native PowerPoint text.
```

---

## 5. Limited keyboard → many Chinese characters

Use to motivate IME / 输入码 conceptually.

### Exact reusable prompt

```text
Create a conceptual classroom illustration for a high-school information technology lesson about Chinese text input.

Teaching purpose:
Help students notice the mismatch between a keyboard with a limited number of keys and the huge number of Chinese characters a user may want to enter.

Subject / scene:
A student sits at a normal computer keyboard.
Visually suggest a very large space of possible Chinese characters beyond the keyboard, without showing a literal technical mapping or readable character chart.
The scene should make the limited keyboard feel small compared with the large choice space.

Composition:
Keyboard and hands in the lower-left or center-left.
A broad open area to the right representing many possible character choices.
Leave room for native PowerPoint labels and arrows.
Wide 16:9-compatible composition.

Visual style:
clean modern educational illustration
white or very light neutral background
minimal visual clutter
clear visual contrast between the small physical keyboard and the large conceptual choice space
serious but friendly
consistent with a white technical teaching deck

Important constraints:
no explanatory text
no readable character chart
no pinyin labels
no arrows
no code points
no byte values
no logos
no watermark
no decorative borders
no gradient background

The teacher will add the labels “输入码”, “IME”, and “字符” later as native PowerPoint objects.
```

---

## 6. Abstract analogy / same identity, different representations

Use only as a conceptual analogy. Do not use it instead of the real byte comparison.

### Exact reusable prompt

```text
Create a conceptual educational illustration for a high-school information technology lesson.

Teaching purpose:
Suggest that one underlying identity can be represented in several different external forms, preparing students to distinguish a character's identity from its encoded byte representation.

Subject / scene:
Show one simple central object or identity and several clearly different representation paths leading outward.
Keep the representation paths abstract rather than technical.
The image should communicate “one thing, multiple representations” without showing code points, bytes, or encoding names.

Composition:
One central subject with three visually distinct outward representation areas.
Leave generous white space around the composition for native PowerPoint labels.
Wide horizontal layout.

Visual style:
minimal educational illustration
white background
simple native-looking geometry
restrained visual language
no glossy infographic style
consistent with a technical classroom deck

Important constraints:
no text
no arrows with labels
no Unicode values
no byte values
no encoding names
no logos
no watermark
no decorative cards
no gradient background

The exact character, code point, encoding names, arrows, and byte sequences will be added later as native PowerPoint objects.
```

---

## 7. Prompt record template for a lesson

Create or append to:

`assets/generated/image-prompts.md`

Use:

```markdown
## IMG-01 — <short name>

**Slide / Q:**  
**Teaching purpose:**  
**Slide role:**  
**Intended placement:**  
**Aspect ratio:**  

### Exact prompt

<PASTE THE COMPLETE PROMPT VERBATIM>

### Post-generation edits

- crop:
- background removal:
- native PPT labels added:
- other:
```

Do not rewrite the prompt after the image has been accepted. Preserve the prompt that actually produced the production asset.

---

## 8. Review checklist before using a generated image

- Does this image have a clear teaching purpose?
- Is generated imagery the right source, rather than a real screenshot or native technical diagram?
- Does the image avoid pretending to be factual evidence?
- Are all precise technical values and labels native PPT objects?
- Is there enough negative space for the intended slide title/annotation?
- Does the image integrate with the white Violet-Rail visual language?
- Are there any incidental details that could teach something technically false?
- Is the exact production prompt preserved?
