# AGENTS.md

## Project: shtick-codex-project

`shtick` produces Senior High School Information Technology course designs, PPTX decks, Reveal.js references, Jupyter demos, and student materials. `SHSIC` is easily mistyped as `SHTICK`, an English word suggesting a distinctive teaching approach.

Produce inspectable, trustworthy, editable classroom materials. **Must** is mandatory; **should/prefer** is recommended; **may** is optional. Apply rules within scope; report unmet obligations.

## 0. Start here

### 0.1 Authorities and required reading

Read this file and applicable lesson-local instructions, then the documents governing the task:

| Concern | Authority / required reading |
|---|---|
| Project workflow, teaching obligations, code language, acceptance | This `AGENTS.md` |
| Lesson content, questions, evidence, conclusions, knowledge-tree stages | Lesson-local `course-design.qmd` |
| PPTX typography, geometry, colors, layouts, visual QA | [Slide Style Guide](slide-style-guide.md), for PPTX creation, revision, or review |
| Generated-illustration prompts and provenance | [Image Generation Prompts](image-generation-prompts.md), when creating, inserting, or reviewing generated images |
| Current package, editable sources, generation and validation | Lesson entry document and relevant scripts |

Use the existing lesson `README.md`, `CLASSROOM-PACKAGE.md`, or course-design entry section. Course design governs teaching; the style guide governs visuals. Generators, old decks, compatibility notes, and prior checks cannot override either. Inspect a named reference deck only when expressly requested.

Honor user scope and resolve routine choices from these authorities. Seek clarification only for unresolved conflicts materially affecting the outcome; continue independent work. A new visual language requires an explicit project decision.

### 0.2 Task workflow

1. Inspect status; preserve existing user changes.
2. Identify lesson, current versions, entry document, and task type.
3. Locate edit points, generators, writes (including ignored/untracked outputs), and checks.
4. Edit within scope; check alignment and affected deliverables.
5. Review the diff; report evidence, limits, and pending work.

- **Audit:** inspect the requested package; report evidence, impact, and proposals. Keep files unchanged unless fixes were requested.
- **Documentation:** check wording, obligations, references, and diff. An `AGENTS.md` edit needs no lesson build.
- **Design revision:** preserve depth; check outcomes, questions, evidence, tree stages, assessment, and timing. Synchronize within scope; name pending outputs.
- **Production change:** update sources/outputs and perform alignment/QA. Every delivered PPTX revision requires full-deck rendering and visual inspection.

A completed narrow task does not establish classroom readiness. Keep cleanup, publication, and unrelated changes within authorization.

## 1. Writing: natural and precise

Write as a careful teacher, textbook editor, or curriculum designer: direct, specific, concise, technically precise, and appropriate to the learners.

Avoid generic motivation, exaggerated claims, repetitive summaries, generation commentary, marketing language, and decorative headings. Avoid formulaic “通过……不仅……而且……” unless needed. Replace “帮助学生更好地理解” with what students actually do or understand.

Avoid:

> 本节课将带领学生深入探索字符编码的奥秘。

Prefer:

> 先让学生观察：同一批字节为什么会显示成不同文字？

## 2. Teaching language and code language

### 2.1 Chinese-first teaching materials

Teaching prose is Chinese-first. Preserve standard English terms where clearer: ASCII, Unicode, UTF-8, IME, Code Point, byte, bit, glyph, encode / decode. Do not translate mechanically.

Distinguish 字符集 / 字符编码, 输入码 / 键盘扫描码, Unicode 码位 / encoded bytes, 字符身份 / 字形, 国标码 / 机内码, and GB2312-specific / general encoding behavior. State important boundaries of classroom simplifications.

### 2.2 English code and comments are required

Code and code comments **must use English by default**. Use English for identifiers, comments, docstrings, and developer-facing messages. This covers standalone scripts and code embedded in QMD files, Notebooks, slides, and demonstrations, including generated code.

Permit non-English text only for strong teaching/technical reasons: Chinese student-facing labels, encoding examples, original quotations, or exact test data. Preserve necessary Chinese literals/evidence; document non-obvious exceptions in teacher material.

Keep Chinese teaching explanations/instructions in prose cells, slide text, or notes. Audience language alone does not justify Chinese implementation comments.

Review source and generated code, distinguishing justified literals from implementation commentary. Non-ASCII matches alone are not violations. Fix within scope and report remaining work.

## 3. Teaching authority, generation, and alignment

### 3.1 Pedagogical authority

`course-design.qmd` defines teaching logic. PPTX, teacher/student demos, activities, knowledge trees, and Reveal.js must agree with it on:

- Q IDs/subquestions, sequence, and terminology;
- givens, examples, evidence, units, and technical boundaries;
- prediction, observation, explanation, and reveal stages;
- knowledge-tree nodes, relationships, and checkpoints;
- conclusions, learning outcomes, and assessment.

### 3.2 Actual generation dependencies

Verify generation paths: QMD → IPYNB and PPTX → Reveal are not universal. Generators may own both QMD and IPYNB, making QMD an output.

Verify the source/output ownership and build order in the entry document (§15) against scripts. Generator-embedded teaching text must follow the course design.

### 3.3 Safe regeneration

Inspect generator/check writes, including exports and reports. Preserve human edits in tracked, untracked, and ignored outputs before replacement; incorporate them into the correct source. Retain original assets and separate trial writes from accepted evidence.

Prefer source/generator fixes. Record necessary output patches with artifact, reason, change, and regeneration survival; revalidate. Preserve prior reviewed versions' identity/evidence.

### 3.4 Alignment and known divergence

In existing lesson records, map each major Q to PPTX pages/builds, Notebook Q/D sections, activities, Reveal sections, and tree checkpoints.

Compare meaning: givens, example values, evidence, reveal order, conclusions, and stage-specific notes. Matching IDs or counts alone does not prove alignment.

Record each difference's versions/locations, teaching impact, compatibility arrangement, and remaining reconciliation. Reconcile against the course design within scope. Compatibility notes do not establish alignment.

## 4. Course design: 认知困惑法 + 问题链 + 知识树

These methods must shape the lesson from the beginning. The question chain establishes concepts; the progressively revealed knowledge tree consolidates them.

### 4.1 Learners, outcomes, and assessment

State prerequisites, duration, roles, equipment/software, projection/audio/network needs, and preparation; distinguish assumptions from observed conditions.

Map outcomes to Q/activity, observable action, student evidence, and acceptable performance. Include independent transfer/exit assessment and responses to persistent misconceptions; volunteer answers alone are insufficient.

### 4.2 Cognitive conflict

Whenever the topic allows, begin with an understandable phenomenon, contradiction, unexpected result, or limitation. Let students make a plausible prediction; use evidence to expose the limits of their explanation and create a need for the next concept.

Examples:

- ASCII 是 7 bit。为什么计算机中常常看到 8 bit？
- 在 GB2312 中，“中”占 2 bytes。为什么换成 UTF-8 后变成 3 bytes？
- 同一批 bytes 没有改变。为什么解码后却变成乱码？
- 两个同学都使用 3-bit 编码。为什么对方的 HELLO 仍然解不出来？

### 4.3 Questions and identifiers

A **major question** establishes a concept, relationship, limitation, or transferable method through a student attempt followed by evidence/explanation. Identify major questions in the design and slide plan.

A **subquestion** develops that task; a separate inference needing a thinking pause also requires question-only/reveal treatment. Brief follow-ups may stay in notes. Relabeling cannot exempt a major task.

Use stable Q and corresponding demo/activity IDs; synchronize all affected materials when renumbering. Each major question should follow from the previous result, become progressively more demanding, introduce at most one major new difficulty, use established evidence, and produce something needed next.

Prefer observation → comparison → inference → explanation → design → diagnosis → transfer over unrelated definitions.

Weak: “ASCII 是多少位编码？”

Better: “ASCII 有 128 个编码位置。至少需要多少 bit？”

Follow-up: “既然 ASCII 只需要 7 bit，为什么计算机中常常看到 8 bit？”

### 4.4 Major-question checklist

For every major Q, the design must answer:

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

Suggested headings: 认知起点、认知困惑、学生任务、预期回答、追问、证据 / Demo、形成结论、下一问. Smaller questions may omit headings, not the reasoning.

Use question → prediction → activity/evidence → compare with prediction → follow-up → abstraction → next question → transfer. Insert student summaries and tree reveals at connected-question checkpoints.

### 4.5 Mandatory progressively revealed knowledge tree

**Every lesson must include a progressively revealed knowledge tree** showing the concepts learned and relationships established through discussion.

After a connected group of questions:

1. Ask students to summarize what they have established and cite evidence.
2. Use their responses to form a concise, accurate summary.
3. Reveal the corresponding tree nodes and relationships.
4. Clearly highlight newly learned knowledge while keeping previously established knowledge visible.

Reveal only established knowledge. Neutral opening question labels are allowed; future nodes/answers and the completed tree must remain hidden.

Define tree structure, node/relationship meanings, Qs, summary prompts, reveal stages, and time in `course-design.qmd`; shared tree data must follow it.

Use native editable PPTX text, shapes, and connectors. Duplicate stages with earlier nodes fixed, readable, and visible. Mark new nodes/relationships using existing semantic colors and focus conventions, plus cues beyond color. Reveal one focus per build.

Align deck, Reveal.js, and relevant teacher/student materials. Notebook/worksheet summary spaces may replace diagrams while preserving reveal timing. Release the completed tree only after establishing its conclusions.

Notes must collect student summaries before each update. Budget checkpoint time and review tree presence, accuracy, reveal order, geometry, and highlighting.

### 4.6 Feasible lesson timing

Budget thinking, discussion, instructions, activities, demos, observation, application switching, tree summaries, and assessment. Include cumulative checkpoints, optional extensions, and cut points that preserve essential reasoning and independent assessment.

Set a demo-failure threshold/fallback. Preserve thinking pauses when trimming. Planned duration is an estimate; record observed pacing separately.

### 4.7 Preserve design depth

Do not shorten `course-design.qmd` merely to tidy the repository. Preserve pedagogical rationale, cognitive conflict, question-chain logic, expected responses, activity intent, demo purpose, transitions, tree logic, technical caveats, and sources.

Move secondary teacher detail to a guide, appendix, or references only within scope, leaving a clear reference. Refactoring must not reduce pedagogical information content.

## 5. Student-facing and teacher-facing information

Classify significant content as student-facing, teacher-facing, or shared at different stages; record placement/reveal timing in the design or slide plan.

Students see current questions, necessary givens, concise instructions, evidence, diagrams, and code they inspect/manipulate. Reveal conclusions and tree additions after reasoning.

Keep intent, scripts, expected responses, follow-ups, timing, technical elaboration, troubleshooting, fallbacks, sources, and later answers in notes, the design, teacher Notebooks, or references.

Ask whether students need it now, whether it supports reasoning, and whether it spoils the question. Keep internal IDs/teacher annotations off slides unless needed for student action. Show conditions essential to correct reasoning; keep complementary caveats teacher-facing. Student material must be concise and projection-readable.

## 6. Official classroom deck: PPTX

`.pptx` is the production classroom format, primarily for **WPS Presentation**, with Microsoft PowerPoint as the alternative. Direct generation is acceptable; do not force production through Quarto at the expense of quality or editability.

Teaching slides cover questions, evidence, explanations, activities, trees, and assessment. Every delivered slide, including covers/transitions/backups, needs notes for its question/page purpose.

## 7. PPTX production requirements

### 7.1 Canonical visual specification

Read and strictly follow [slide-style-guide.md](slide-style-guide.md). Its detailed typography, geometry, palette, density, and QA requirements are mandatory. Preserve:

- 16:9 white canvas and violet top/bottom rails;
- explicit Alibaba PuHuiTi 3.0 variants on all native text;
- common title baseline and content area;
- narrative teaching titles, evidence-first layouts, and generous white space;
- semantic violet / cyan / red, one current teaching focus, and stable builds.

Use the guide's title variants and approved Alibaba-family fallback; verify rendered fonts. Code text follows both native-font rules and §2.2.

### 7.2 Question and reveal stages

Use the style guide §21.1 slide plan: Q/stage, visible/withheld content, notes, evidence, focus, and tree checkpoints.

Every major Q must first appear on its own **question-only slide** with only necessary givens, neutral evidence, and concise instructions. Exclude answers, effective hints, completed calculations, answer-colored emphasis, revealing diagrams, and teacher annotations. Sparse question slides are encouraged.

Create the next answer/evidence/explanation slide by **duplicating the question slide**. Preserve wording, font family/size/weight, x/y position, box dimensions, alignment, line breaks, and base geometry. Reveal one additional focus per subsequent duplicate.

Prefer duplicated slides over complex animation; essential meaning must survive static export. Tree builds retain established nodes and focus attention on newly learned concepts/relationships.

### 7.3 Density and deviations

If content does not fit, enlarge the area, shorten wording without changing the question, move complementary detail to notes, or split the focus. Do not shrink normal teaching text or use auto-fit to force a fit. Apply title variants consistently across paired slides.

First revise both paired slides together to preserve geometry. Record any necessary deviation's slides, reason, alternatives, and validation. Recording it does not waive requirements; unresolved deviations remain acceptance issues absent an explicit project/user decision.

### 7.4 Evidence and generated illustrations

Classify each visual:

| Purpose | Approach |
|---|---|
| Factual evidence: standards, software, exact output, historical records | Real screenshots, original assets, primary sources, or reproducible experimental evidence |
| Exact structures, knowledge trees, labels, bytes, tables, calculations | Native editable PPT shapes, tables, text/code, and connectors |
| Situation, analogy, human context, cognitive conflict | Generated illustration may be appropriate |

**Generated images illustrate; native diagrams and real screenshots prove.** Verify native diagram values and relationships too.

For every generated image:

1. State its teaching purpose before prompting; specify slide region, composition, and aspect ratio.
2. Follow [image-generation-prompts.md](image-generation-prompts.md), normally without explanatory text, technical labels, arrows, byte values, or conclusions.
3. Add precise annotations as native PPT objects. Use clean rectangular visuals without decorative frames, shadows, glow, or cards; check for technical misconceptions.
4. Preserve the exact production prompt, image ID, slide/Q, purpose, composition/aspect ratio, and post-generation edits.

Store provenance in lesson-local `assets/generated/image-prompts.md` and/or `[图片生成提示词]` notes. Do not reconstruct prompts afterward. Generated tables, software UI, standards pages, code output, or historical documents must not substitute for factual evidence.

## 8. Speaker Notes and transcripts

Every slide must have a usable transcript beginning with its full question/page purpose, not just a Q ID:

```text
[问题] ASCII 是 7 bit，为什么计算机中常常看到 8 bit？
[内部编号] Q3
[阶段] 提问
[教师逐字稿]
```

Use relevant sections such as `[教学意图]`, `[预期学生反应]`, `[追问问题]`, `[形成结论]`, `[Demo 操作]`, `[技术注解]`, and `[来源]`; no arbitrary word count is required.

A **usable transcript** uses natural speech, visible evidence, student actions, pauses, likely responses, and transitions. Add value beyond reading the slide; keep a lively, untheatrical rhythm.

Match the stage:

- **Question:** invite prediction, comparison, or explanation; allow thinking; do not speak the answer.
- **Evidence / reveal:** respond to attempts and explain newly available evidence.
- **Tree summary:** collect student summaries, then identify new nodes/relationships and their connections.
- **Assessment / exit:** collect independent responses before revealing answers.

Never copy an answer-bearing script unchanged into question notes. Separate spoken text from teacher references held for later. Review wording/timing, not just presence.

Follow-ups should explain observations, test premature conclusions, connect evidence, compare, or transfer. Keep source URLs, troubleshooting, alternatives, and complementary caveats teacher-facing.

## 9. PPTX QA and acceptance evidence

### 9.1 Production workflow

For every production deck created or revised, follow the style guide §21.2:

1. Compare the deck with the design/slide plan, including Q order, reveals, and tree checkpoints.
2. Render **every slide** to images and generate a full-deck montage.
3. Inspect the montage and every slide; inspect dense, diagram-heavy, paired, overlay, and tree builds individually at full resolution.
4. Where feasible, check canvas bounds, rails, fonts, notes, and paired/build geometry programmatically. Verify actual rendered fonts across Chinese, Latin, numbers, and symbols.
5. Review student-visible content, stage-specific transcripts, tree additions, code-language exceptions, technical accuracy, and evidence readability.
6. Inspect actual WPS rendering and notes whenever practical; identify PowerPoint checks separately when used.
7. Fix visible defects and recheck the final version. Refresh rendered evidence after deck changes.

Reject overlap, obscured/clipped text, accidental wrapping, unsafe margins, stretched screenshots, unreadable evidence, unstable alignment, and auto-fit shrinking essential text. Text-box dimensions alone do not prove a fit.

### 9.2 Acceptance record

Use the **Deck acceptance record** in [slide-style-guide.md](slide-style-guide.md), §21.3, in delivery notes. Extend existing lesson records rather than duplicating reports.

Record `pass`, `fail`, or `unverified` with version/path, method, evidence, and limits. Explain inapplicable checks. Separate these layers:

| Layer | Evidence |
|---|---|
| Teaching alignment | Q/content mapping, reveal/tree order, assessment and timing review |
| Structural checks | Commands and results for relevant package, geometry, font, notes, and path checks |
| Rendering / human inspection | Renderer/version, full-deck images/montage, full-resolution inspection, defects/rechecks |
| Notebook execution | Both roles, fresh kernel, environment, working directory, results/executed copies |
| Classroom applications | Actual WPS/PowerPoint layout/notes and JupyterLab visibility, controls, output layout |
| Classroom conditions | Projection, audio where used, activity completion, observed pacing |

Identify the delivered version/copy, environment/date, and hash where practical. Revalidate changed artifacts.

PDF rendering does not verify WPS; opening a file does not verify layout; Python execution does not verify JupyterLab UI; a timing budget does not verify classroom pace.

Resolve failures before acceptance. Record unavailable checks as `unverified`, with reason/action. Locally validated delivery must state limits; **classroom-ready** requires applicable classroom checks to pass.

## 10. Reveal.js / Quarto reference deck

Maintain `slides.qmd`/Reveal.js for reference and experiments with typography, geometry, disclosure, code output, interactions, and browser delivery. Changing its production role requires an explicit project decision.

Align Q IDs, sequence, terminology, evidence, conclusions, and tree checkpoints with the course design/PPTX. Page counts may differ. Preserve student/teacher separation and reveal timing. Follow the actual generation path when editing.

A successful Quarto render does not establish presentation readiness. Inspect output and dependencies for the requested reference-delivery checks.

## 11. Demonstrations and Jupyter workflow

### 11.1 Demo design

Prefer JupyterLab when manipulating inputs, comparing encodings, inspecting bytes, or rerunning experiments provides meaningful evidence. Demos should expose misconceptions, create cognitive conflict, or make invisible processes observable.

For each demo, specify Q/D IDs, student prediction, exact observation target, information withheld until running, intended inference, and fallback. Use question → prediction → run → observe → explain → concept.

Small deterministic examples may appear in PPTX when no live manipulation is needed. Prefer PPT/WPS ⇄ JupyterLab; use extra applications such as WinHex only for important evidence, with a Notebook/static fallback.

### 11.2 Teacher and student versions

Jupyter lessons require teacher/student QMD/IPYNB views following §3.2, with aligned Q/D IDs and computations. Share reusable functions/modules where practical.

Teacher views may contain complete code, expected output, answers, scripts, predictions, observation guidance, caveats, troubleshooting, fallbacks, extensions, and sources. Optimize for preparation and teacher control.

Student views contain current questions, setup, readable/editable code, prediction/observation prompts, and staged outputs. Exclude premature conclusions and teacher answers. State who operates and who observes.

Apply English-code rules (§2.2) to both versions and shared modules. Put Chinese teaching prompts in prose cells. Include summary opportunities at tree checkpoints without exposing later nodes.

### 11.3 Execution and clean delivery

1. Document Python/kernel, packages, working directory, relative assets, and classroom dependencies separately from build dependencies.
2. Use reproducible fixtures and explicit seeds where needed; state tolerances/version dependence.
3. Inspect writes and preserve human edits before execution/regeneration. Keep trial writes away from accepted evidence.
4. Execute both versions from **fresh kernels** in the documented directory and sequence, with suitable recorded timeouts. Check observations as well as exceptions. Test an intended completion path separately for incomplete student cells.
5. Store executed copies/logs as validation evidence. Deliver clean Notebooks with stale outputs/execution counts cleared where they would spoil the lesson; retain only intended initial evidence.
6. Verify delivered/generated notebooks match their sources and shared computations.

If kernel execution is blocked, report the cause. Sequential Python-cell execution validates only Python logic, not kernel, widget, or JupyterLab behavior; keep those checks unverified.

### 11.4 Projection and fallback

Check actual JupyterLab code/parameter visibility, labels, scrolling, controls, comparison scales, and simultaneous evidence display. Hidden-input tags/collapse metadata alone prove nothing about display.

Test staged operation as well as full execution. Do not leave later student answers visible from a prior run.

Provide essential demos' offline evidence, relative assets, and copying instructions. Verify the same conclusion and state lost capabilities. Use the failure threshold; avoid classroom installs/prolonged troubleshooting.

**The deck shows the evidence. The Notebook allows the evidence to be manipulated.**

## 12. Activities and accessibility

Activities must specify student actions, produced evidence, exposed misconception/question, and the next needed concept, plus roles, grouping, materials, response collection, and time. Control student/teacher material distribution. Prefer short activities feeding the next question or tree summary.

Essential distinctions, including tree additions, need labels, position, outlines, or relationships beyond color. Check projected readability; enlarge, excerpt, or split dense evidence. Provide visual/textual alternatives to sound and offline alternatives to network/live demos. Unsupported sensory judgments cannot be the sole route to a conclusion.

## 13. Technical accuracy

Verify substantive claims before classroom use. State model boundaries, assumptions, units, input conditions, and conclusion scope.

### 13.1 Character encoding

- **ASCII:** 7-bit, 128 positions; represented in an 8-bit byte as `0xxxxxxx`. Do not call ASCII itself 8-bit.
- **GB2312:** “一个汉字占 2 bytes” and “两个 byte 的最高位都是 1” are limited to the traditional GB2312 machine-code model taught here, not UTF-8, GB18030, or all Chinese encodings.
- **Unicode:** distinguish character, code point, encoding, bytes, glyph, pixels. `你 → U+4F60 → UTF-8 → E4 BD A0`; the code point is not the UTF-8 byte representation.
- **Input:** 汉字输入码 differs from keyboard scan codes.
- **Display:** classroom model `character → font mapping → glyph / outline / bitmap → rasterization → pixels`. Visible shape is not stored character identity; add boundaries when needed.

### 13.2 Image, audio, compression, and calculations

- Identify what is measured: pixels/samples, encoded bytes, payload, or complete file. State included overhead; do not mix counting conventions.
- Distinguish teaching models and reprocessed digital media from real physical processes/formats. Preserve source history and limitations.
- Separate visual/auditory similarity from exact recovery. Define and directly test the equality target for losslessness claims.
- State units, bit/byte conversions, dimensions, sample/channel counts, storage widths, rounding, and formula conditions as applicable.
- Control comparisons: shared input, changed parameter, fixed conditions, and observation limits. One example does not prove a universal rule.
- Preserve originals and record transformations. Reproduce calculations and independently check key results; generator/checker agreement may share the same mistaken assumption.

## 14. Research and provenance

Verify standards, specifications, product behavior, and history using standards bodies, primary specifications, official documentation, reputable institutions, then strong secondary sources. Reject unsourced figures; preserve source disagreements.

Link claims to sources/calculations in existing records: title/version/date, URL/section/page, web retrieval date, supported claim, and qualifications. Calculations need inputs, method/script, units, and result.

For reused media, record origin, attribution, permitted use/permission status, and transformations. Preserve originals; use hashes where practical. Do not invent permission or assume user-supplied assets are cleared for public redistribution.

Research URLs belong primarily in teacher material. Student-action links follow the style guide §17. Generated-image provenance also follows §7.4.

## 15. Lesson entry document and file roles

Every lesson package must designate one entry document. Prefer its existing README/package guide. Record:

- exact current PPTX/companion paths and historical, draft, and reference roles;
- editable sources, generated outputs, owning generators, and build order;
- commands, working directories, expected outputs, overwrite behavior;
- build/classroom dependencies and supported environments;
- tracked/ignored deliverables and how to recreate/package them;
- classroom operation, reveal order, assets to copy, and fallbacks;
- version-bound validation evidence, known divergence, and pending checks.

Verify this record against actual files. Do not select production solely by filename numbering or modification time, or silently promote a draft/validation copy.

File roles: `course-design.qmd` is teaching authority; `demo-lab-teacher.qmd / .ipynb` and `demo-lab-student.qmd / .ipynb` are the two demo views; `slides.qmd` is the Reveal.js reference; the designated `.pptx` is the classroom deck. Declare source/output ownership for each view.

Use `assets/` for evidence/media, `demos/` for shared code, and `references/` for sources. Build code may live in `scripts/`, `sources/`, or repository `tools/`; keep version-bound results in the existing validation location. Avoid empty folders, competing guides, and machine-specific classroom runtime paths.

## 16. Completion and classroom readiness

### 16.1 Task completion

Review scope, preserved work, diff, and references; run relevant checks such as `git diff --check`. Report evidence and pending work. Documentation edits do not claim lesson testing; design edits identify pending synchronization; production changes require §9.2.

### 16.2 Lesson acceptance

Classroom readiness requires all applicable checks to pass:

- [ ] Prerequisites, equipment, outcomes, student evidence, and independent assessment are defined.
- [ ] Cognitive conflict, progressive questions, purposeful activities/demos, design rationale, and technical boundaries are preserved.
- [ ] Every lesson has a correct, progressively revealed knowledge tree after student summaries; new concepts/relationships are highlighted and earlier knowledge stays visible.
- [ ] Q/D IDs, evidence, conclusions, reveals, and tree checkpoints align; divergence is resolved.
- [ ] Timing includes thinking, switching, summaries, and assessment, with feasible cut points.
- [ ] Student/teacher separation prevents premature answers in slides, Notebooks, spoken scripts, and handouts.
- [ ] PPTX meets the style/font rules, question-only requirement, and duplicated reveals with stable geometry.
- [ ] Every slide has its full question/purpose and a usable stage-specific transcript in notes.
- [ ] Every slide is rendered/inspected; dense, paired, overlay, and tree builds receive detailed QA; defects are fixed.
- [ ] Both Notebooks are aligned, tested from fresh kernels, clean for delivery, and checked in the projected UI.
- [ ] Code/comments, identifiers, docstrings, and developer messages use English by default; strong exceptions are justified, with non-obvious reasons documented.
- [ ] Claims, calculations, recovery tests, assumptions, and provenance are checked; generated images illustrate with preserved purposes, exact prompts, and edits.
- [ ] Color-independent cues and necessary offline/audio/demo alternatives are usable.
- [ ] Reveal.js, current package/source ownership, and delivered-version validation records are aligned.
- [ ] Applicable classroom app, projection/audio, and pacing checks pass; unverified checks qualify delivery status.
- [ ] Writing is natural, precise, and free of AI tone.
