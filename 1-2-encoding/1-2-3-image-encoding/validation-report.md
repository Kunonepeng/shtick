# Image Encoding Materials Validation Report

Generated locally in this environment after executing the teacher and student notebooks and rendering the PPTX. Windows 10 + conda `pt` classroom validation is still required.

## Generated files

- `assets/test-image.png` — 256×256 RGB
- `assets/fallback/sampling-256.png`, `sampling-64.png`, `sampling-32.png`, `sampling-16.png`, `sampling-8.png` — all 512×512 RGB
- `assets/fallback/quant-original.png`, `quant-16.png`, `quant-2.png` — all 256×256 RGB
- `assets/q7-3x2-24bit.bmp` — 3×2, 24-bit BMP, 78 bytes
- `notebooks/image-encoding-teacher.ipynb`
- `notebooks/image-encoding-student.ipynb`

## Verified conditions

- Sampling fallback images: 5 files × 512×512 RGB
- Quantization fallback images: original / 16 / 2 → 256×256 RGB
- Seam evidence:
  - 16 colors → seam (72,40) != (73,40): (255, 0, 0) != (0, 255, 0)
  - 2 colors → seam (72,40) == (73,40): (71, 42, 71) == (71, 42, 71)
- BMP evidence:
  - pixel-data offset = 54 bytes
  - color values = 18 bytes
  - stored row size = 12 bytes/row
  - pixel array = 24 bytes
  - whole file = 78 bytes
  - top-row red pixel bytes at offset 66 = `00 00 FF`

## Remaining validation

- Run teacher and student notebooks on classroom Windows 10 + conda `pt` from the lesson directory.
- Open the PPTX in WPS / PowerPoint and confirm Alibaba PuHuiTi 3.0 font resolution.

## PPTX validation

- `image-encoding-v1.pptx` generated with 18 slides and 18 speaker-notes slides.
- Converted successfully to PDF with LibreOffice in this environment.
- Rendered to PNG montage for visual inspection.

## Notebook execution

- `notebooks/image-encoding-teacher.ipynb` executed successfully in this environment from the lesson directory.
- `notebooks/image-encoding-student.ipynb` executed successfully in this environment from the lesson directory.
- Demo B file-level optional BMP check reported `24 bpp` and `196662 bytes` for 256 / 16 / 4 / 2-color outputs.
