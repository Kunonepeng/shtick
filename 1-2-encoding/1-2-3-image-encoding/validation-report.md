# Image Encoding Materials Validation Report

Updated materials generated and checked in the current container.

## Asset checks

- `assets/test-image.png`: 256×256 RGB.
- Sampling fallback: `sampling-256/64/32/16/8.png`, all 512×512 RGB.
- Quantization fallback: `quant-original/16/2.png`, all 256×256 RGB.
- Seam check on exported fallback files:
  - `quant-16.png`: `(72,40) != (73,40)`.
  - `quant-2.png`: `(72,40) == (73,40)`.
- Q2 files:
  - `q2-high-pixels-blur.png`: 1920×1080.
  - `q2-low-pixels-sharp.png`: 800×600.
- BMP file: `q7-3x2-24bit.bmp` has pixel-data offset 54, 18 bytes color values, 12 bytes/row, 24 bytes pixel array, 78 bytes whole file.

## Notebook checks

Teacher and student notebooks are structured with Q-numbered headings. The teacher notebook contains:

- Q1 · Demo A fixed fallback generation and `show_sampling(n)` for student-requested new sizes.
- Q2 image-size verification.
- Q3 · Demo B image-first reveal, then seam RGB evidence.
- Fallback export and verification cells.
- Q7/Q11 BMP verification.

## Slide checks

PPTX was regenerated with independent question pages before answer/evidence pages. Q0 begins with scrambled cards and is revisited at Q12. Q4, Q6, Q8, and Q9 have neutral question pages before derivation/answer pages. Speaker notes have been expanded with page purpose, spoken script, pauses, expected answers, and transitions.

## Still pending

- Windows 10 + conda `pt` classroom-machine run.
- WPS-specific font and layout validation.
- Final teacher approval of PPTX narration pacing.
