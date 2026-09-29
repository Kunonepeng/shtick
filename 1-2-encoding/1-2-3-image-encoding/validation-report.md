# Image Encoding Materials Validation Report

Updated materials were generated and checked in the current container after the PPTX reveal-order review.

## Asset checks

- `assets/test-image.png`: 256×256 RGB.
- Sampling fallback: `sampling-256/64/32/16/8.png`, all 512×512 RGB.
- Quantization fallback: `quant-original/16/2.png`, all 256×256 RGB.
- Seam check on exported fallback files:
  - `quant-16.png`: `(72,40) != (73,40)`.
  - `quant-2.png`: `(72,40) == (73,40)`.
- Q2 files generated from the same synthetic scene:
  - `q2-high-pixels-blur.png`: 1920×1080, intentionally blurred.
  - `q2-low-pixels-sharp.png`: 800×600, sharp.
- BMP file: `q7-3x2-24bit.bmp` has pixel-data offset 54, 18 bytes color values, 12 bytes/row, 24 bytes pixel array, and 78 bytes whole file.

## Notebook checks

Teacher and student notebooks should use Q-numbered headings. The teacher version should contain:

- Q1 · Demo A fixed fallback generation and `show_sampling(n)` for student-requested new sizes.
- Q2 image-size verification.
- Q3 · Demo B image-first reveal, then seam RGB evidence.
- Fallback export and verification cells.
- Q7/Q11 BMP verification.

The student version should keep the prediction/observation order and avoid revealing seam RGB values before students have interpreted the images.

## Slide checks

The regenerated PPTX uses independent question pages before evidence/answer pages:

- Q0 begins with scrambled cards; the target order is revisited at Q12.
- Q4, Q6, Q8, and Q9 have neutral question pages before derivation/answer pages.
- Q8 answer highlight appears only after calculation.
- Q2 evidence uses actual 1920×1080 and 800×600 files.
- Q3 seam evidence uses actual RGB tuples from `(72,40)` and `(73,40)`.
- Speaker notes were expanded with page purpose, spoken script, pauses, expected answers, and transitions.

## Reveal.js reference

`slides.qmd` has been added as a lightweight Reveal.js reference version aligned with the PPTX question chain. It is not a replacement for the styled classroom PPTX.

## Still pending

- Commit/update of binary classroom artifacts in GitHub must be verified after upload: PPTX and regenerated PNG assets are binary files.
- Windows 10 + conda `pt` classroom-machine run.
- WPS-specific font and layout validation.
- Final teacher approval of PPTX narration pacing.
