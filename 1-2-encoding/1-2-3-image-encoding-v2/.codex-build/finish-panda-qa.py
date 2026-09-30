from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,hashlib,pdfplumber
r=Path(__file__).resolve().parent.parent;t=Path('/private/tmp/panda-qa');out=r/'.codex-build/qa-panda-v1';out.mkdir(exist_ok=True)
files=sorted(t.glob('slide-*.png'));assert len(files)==56
for f in files:shutil.copy2(f,out/f.name)
shutil.copy2(t/'candidate-panda.pdf',out/'slides.pdf')
for k in range(0,len(files),12):
 c=Image.new('RGB',(1600,750),'#dddddd');draw=ImageDraw.Draw(c)
 for j,f in enumerate(files[k:k+12]):
  im=Image.open(f);im.thumbnail((400,225));x=j%4*400;y=j//4*250;c.paste(im,(x,y));draw.text((x+12,y+228),f.stem,fill='black')
 c.save(out/f'montage-{k//12+1}.jpg',quality=93)
with pdfplumber.open(out/'slides.pdf') as pdf:
 fonts=sorted({c['fontname'].split('+')[-1] for p in pdf.pages for c in p.chars})
 assert fonts==['AlibabaPuHuiTi_3_115_Black','AlibabaPuHuiTi_3_55_Regular']
v=json.loads((r/'.codex-build/validation-panda-v1.json').read_text());s=json.loads((r/'.codex-build/structural-panda.json').read_text())
report=f'''# 熊猫版PPTX检查记录

日期：2026-09-30。

## 交付文件

`exports/1-2-3-image-encoding-panda-v1.pptx`

SHA-256：`{hashlib.sha256((r/'exports/1-2-3-image-encoding-panda-v1.pptx').read_bytes()).hexdigest()}`

## 已完成的检查

|项目|结果|
|---|---|
|教学顺序|Q0–Q22，沿用course-design.qmd的问题链|
|素材与计算变更|详见panda-deck-design.md，8×8→16×16，四色→六色|
|页数|56|
|问题／答案配对|25组，程序核对所有原问题页对象的几何、题目文字与样式，全部一致|
|Speaker Notes|56页均以完整问题／页面目的开头，均含教师逐字稿；最短194字|
|画布／轨道|16:9；上下8pt紫色轨道；无越界对象|
|字体|所有原生文本明确使用Alibaba PuHuiTi 3.0 115 Black或55 Regular|
|实际渲染字体|PDF文本仅出现AlibabaPuHuiTi_3_115_Black和AlibabaPuHuiTi_3_55_Regular|
|编辑性|10页含原生表格，网格、编号、码字、框线、图示、正文均为原生PPT对象|
|包完整性|0 finding|
|布局检查|0 finding，0 warning|
|回读|artifact-tool成功导入最终PPTX，56页|
|计算|三轮128/512/768bit与16/64/96B；读码8格16bit；RGB138/179/111；500×333练习全部核对|
|图像来源|内嵌熊猫原JPEG和原课两张人物修复证据；原花图截图未嵌入|
|源文件保护|熊猫原图哈希未变；旧课堂PPTX和课程设计未改动|

## 视觉检查

1. 用本地LibreOffice渲染全部56页为PDF，再输出1600×900逐页PNG。
2. 检查完整5张缩略总览，逐页查看全部56张PNG。
3. 重点核对裁切与网格范围一致性、编号／二进制矩阵、8格读码条、原生表格、RGB像素、文件大小说明和修复照片。
4. 调整底部工作区留白、封面字号、码字与色条的逐格对齐后，重新渲染全部页面，复查改动页。
5. 最终PPTX与已检查candidate字节相同。

检查材料：`.codex-build/qa-panda-v1/slides.pdf`、`slide-01.png`至`slide-56.png`、`montage-1.jpg`至`montage-5.jpg`。

机器结果：`.codex-build/validation-panda-v1.json`、`.codex-build/structural-panda.json`。包验证不代替内容与视觉检查；通用表格算术检查未覆盖课堂算式，本次由专项算式检查及逐页核对补充。

## 尚未验证

本次未在WPS／Microsoft PowerPoint界面进行实机放映检查，也未在教室投影设备检查颜色区分度与后排可读性。已完成的是本地LibreOffice渲染和原生PPTX结构检查。课堂电脑需安装对应Alibaba PuHuiTi 3.0字体，字体未嵌入文件。

本版所有课堂证据均已嵌入，不依赖现场网络或额外Notebook。原图重复使用是控制同一实验对象和逐步揭示的教学需要。
'''
(r/'panda-pptx-quality-report.md').write_text(report)
print(json.dumps({'rendered_slides':len(files),'montages':5,'fonts':fonts,'qa_folder':str(out)},ensure_ascii=False))
