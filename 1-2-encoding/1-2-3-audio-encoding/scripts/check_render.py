"""Inspect a local 40-page PDF render and retain montage/fallback evidence."""
from pathlib import Path
import hashlib
import json
import shutil
from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / '.build/render-final/1-2-3-audio-encoding-v1.pdf'
reader = PdfReader(PDF)
fonts = set()
for page in reader.pages:
    resources = page['/Resources'].get_object()
    for font in resources.get('/Font', {}).get_object().values():
        fonts.add(str(font.get_object()['/BaseFont']))
assert len(reader.pages) == 40
assert fonts and all('AlibabaPuHuiTi' in name for name in fonts), fonts
assert all(page.extract_text().strip() for page in reader.pages)
pngs = sorted(PDF.parent.glob('slide-*.png'))
assert len(pngs) == 40
for batch in range(4):
    montage = Image.new('RGB', (1280, 1930), '#eeeeee')
    draw = ImageDraw.Draw(montage)
    for offset, path in enumerate(pngs[batch*10:(batch+1)*10]):
        image = Image.open(path).convert('RGB')
        assert image.size == (1600, 900), image.size
        image.thumbnail((620, 349))
        col, row = offset % 2, offset // 2
        x, y = 10 + col*640, 10 + row*386
        draw.text((x, y), str(batch*10+offset+1), fill='black')
        montage.paste(image, (x, y+22))
    montage.save(ROOT / f'validation/montage-{batch+1}.png')
for demo, slide in [('D1', 7), ('D2', 17), ('D3', 21), ('D4', 35)]:
    shutil.copyfile(pngs[slide-1], ROOT / f'assets/fallback/{demo}.png')
shutil.copyfile(pngs[20], ROOT / 'validation/preview-quantization.png')
result = {
    'pages': len(reader.pages), 'rendered_images': len(pngs),
    'embedded_fonts': sorted(fonts), 'all_pages_have_text': True,
    'pptx_sha256': hashlib.sha256((ROOT / 'exports/1-2-3-audio-encoding-v1.pptx').read_bytes()).hexdigest(),
    'pdf_sha256': hashlib.sha256(PDF.read_bytes()).hexdigest(),
    'passed': True,
    'scope': 'Local LibreOffice rendering; Windows WPS/PowerPoint acceptance is separate.'
}
(ROOT / 'validation/render-checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False))
