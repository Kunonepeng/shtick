# Image Encoding Materials Validation Report

Updated after review of the full lesson folder.

## Asset checks

- `assets/test-image.png`: 256×256 RGB.
- Sampling fallback: `sampling-256/64/32/16/8.png`, all 512×512 RGB. These are the exact images used for Q1 PPTX evidence pages.
- Quantization fallback: `quant-original/16/2.png`, all 256×256 RGB.
- Seam check on exported fallback files:
  - `quant-16.png`: `(72,40) != (73,40)`.
  - `quant-2.png`: `(72,40) == (73,40)`.
- Q2 files rebuilt with the same 4:3 aspect ratio and scene framing:
  - `q2-high-pixels-blur.png`: 1600×1200, Gaussian blur radius 10.
  - `q2-low-pixels-sharp.png`: 800×600, sharp.
- BMP file: `q7-3x2-24bit.bmp` has pixel-data offset 54, 18 bytes color values, 12 bytes/row, 24 bytes pixel array, 78 bytes whole file.

## Notebook checks

Teacher and student notebooks are structured with Q-numbered headings. The teacher notebook contains:

- Q1 · Demo A fixed fallback generation and `show_sampling(n)` for student-requested new sizes.
- Q2 image generation and size verification.
- Q3 · Demo B image-first reveal, then seam RGB evidence.
- Q6 · Demo C RGB → bits.
- Fallback export and verification cells.
- Q7/Q11 BMP verification.
- Optional BMP `biBitCount` checks for quantization outputs.

## Slide checks

PPTX was regenerated with fixed-question transitions. Evidence/answer slides retain the exact question title and position, then add evidence in the content area. Q0 begins with scrambled cards; Q12 first reuses the unordered cards, then reveals the chain. Q4 question page no longer gives away the 4-bit result. Q2 uses same-aspect-ratio images. Speaker notes include page purpose, spoken script, pauses, expected answers, and transitions.

## Reveal.js reference

`slides.qmd` is aligned with the PPTX question/reveal order and uses the rebuilt Q2 images.

## Still pending

- Windows 10 + conda `pt` classroom-machine run.
- WPS-specific font and layout validation.
- Final teacher approval of PPTX narration pacing.
