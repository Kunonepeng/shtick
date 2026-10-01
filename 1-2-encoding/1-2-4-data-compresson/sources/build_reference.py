"""Produce a Reveal reference from the exact reviewed classroom deck.

python sources/build_reference.py <pptx> <render-folder>
Images are rendered slide evidence, not generated illustrations. Notes stay
teacher-facing. Re-run after any PPTX edit; do not hand-edit rendered evidence.
"""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import json
import shutil
import sys
ROOT=Path(__file__).resolve().parents[1]
PPTX=Path(sys.argv[1]).resolve()
RENDER=Path(sys.argv[2]).resolve()
DEST=ROOT/'assets/reference'
DEST.mkdir(exist_ok=True)
plan=json.loads((ROOT/'sources/slide-plan.json').read_text())
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
qmd='''---
pagetitle: "数据压缩入门：PPTX参考版"
lang: zh-CN
format:
  revealjs:
    width: 1280
    height: 720
    margin: 0
    center: false
    controls: true
    progress: false
    slide-number: false
    transition: none
    background-transition: none
    overview: true
execute:
  enabled: false
---

<!-- Reference rendered from the reviewed PPTX. Do not use as the production deck. -->
'''
with ZipFile(PPTX) as z:
    for row in plan:
        i=row['slide']
        original=RENDER/f'slide-{i:02d}.png'
        if not original.is_file(): raise FileNotFoundError(original)
        name=f'slide-{i:02d}.png'
        shutil.copyfile(original,DEST/name)
        xml=ET.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml'))
        notes='\n\n'.join(t.text or '' for t in xml.findall('.//a:t',ns))
        qmd+=f'\n## {{background-image="assets/reference/{name}" background-size="contain"}}\n\n<!-- {row["q"]} · {row["stage"]}: {row["visible"]} -->\n\n::: notes\n{notes}\n::: \n'
(ROOT/'slides.qmd').write_text(qmd,encoding='utf-8')
md='# PPTX逐页计划（教师侧）\n\n|页|问题与阶段|学生此时看到|留到之后／备注|证据|\n|---|---|---|---|---|\n'
for row in plan:
    md+=f'|{row["slide"]}|{row["q"]} · {row["stage"]}|{row["visible"]}|{row["hidden"]}|{row["evidence"]}|\n'
(ROOT/'sources/slide-plan.md').write_text(md,encoding='utf-8')
print(f'Reveal source and {len(plan)} reviewed slide images generated.')
