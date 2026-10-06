"""Auxiliary font-metric check; visual rendering remains required."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as E
from fontTools.ttLib import TTFont
import hashlib
import json
import re
import os

ROOT = Path(__file__).resolve().parents[1]
PPTX = ROOT / 'exports/1-2-3-audio-encoding-v4-final.pptx'
FONT_DIR = Path(os.environ.get('AUDIO_FONT_DIR',str(Path.home() / 'Library/Fonts')))
fonts = {
    'Alibaba PuHuiTi 3.0 115 Black': TTFont(FONT_DIR / 'AlibabaPuHuiTi-3-115-Black.ttf'),
    'Alibaba PuHuiTi 3.0 55 Regular': TTFont(FONT_DIR / 'AlibabaPuHuiTi-3-55-Regular.ttf')
}
ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
issues, lines = [], 0
with ZipFile(PPTX) as z:
    for name in z.namelist():
        if not re.fullmatch(r'ppt/slides/slide\d+.xml', name):
            continue
        for shape in E.fromstring(z.read(name)).findall('.//p:sp', ns):
            extent = shape.find('p:spPr/a:xfrm/a:ext', ns)
            if extent is None:
                continue
            limit = int(extent.get('cx')) / 12700
            for para in shape.findall('p:txBody/a:p', ns):
                width = 0
                has_text = False
                for run in para.findall('a:r', ns):
                    text = run.find('a:t', ns).text or ''
                    has_text |= bool(text)
                    style = run.find('a:rPr', ns)
                    face = style.find('a:latin', ns).get('typeface')
                    font = fonts[face]
                    cmap = font.getBestCmap()
                    size = int(style.get('sz')) / 100
                    for char in text:
                        if ord(char) not in cmap:
                            issues.append({'part': name, 'missing_glyph': char})
                            continue
                        width += font['hmtx'][cmap[ord(char)]][0] / font['head'].unitsPerEm * size
                if has_text:
                    lines += 1
                    if width > limit + 0.5:
                        issues.append({'part': name, 'width_pt': width, 'limit_pt': limit})
result = {'lines': lines, 'issues': issues, 'passed': not issues,
          'pptx_sha256': hashlib.sha256(PPTX.read_bytes()).hexdigest(),
          'scope': 'Horizontal glyph metrics only; no native WPS layout acceptance.'}
(ROOT / 'validation/v4/text-fit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False))
raise SystemExit(bool(issues))
