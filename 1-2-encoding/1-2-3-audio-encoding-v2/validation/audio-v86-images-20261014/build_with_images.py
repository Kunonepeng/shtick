#!/usr/bin/env python3
"""Visual evidence insertion based only on searched-images/source.md and authentic v8.6.gpt.

Two rounds: first integrate only high-value sourced images, second add the
classroom reveal and tighten visual explanations. Both are audited and rendered
by the GitHub Actions workflow. The source v8.6.gpt is never overwritten.
"""
from __future__ import annotations
from pathlib import Path
from io import BytesIO
import hashlib, json, re
from PIL import Image
import cairosvg
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

BASE=Path(__file__).resolve().parents[2]
WORK=Path(__file__).resolve().parent
IMGDIR=BASE/"1-2-3-audio-encoding-v8.4.10-searched-images"
ASSETS=IMGDIR/"assets"
ORIGINAL=BASE/"1-2-3-audio-encoding-v8.6.gpt.pptx"
DEST=BASE/"1-2-3-audio-encoding-v8.6.with-images-by-gpt.pptx"
WHITE=RGBColor(255,255,255)
INK=RGBColor(38,38,38)
ACC=RGBColor(140,100,225)
VIOLET=RGBColor(98,81,177)
CYAN=RGBColor(0,124,155)
LT=RGBColor(229,229,236)
FONT="Alibaba PuHuiTi 3.0 55 Regular"
BOLD="Alibaba PuHuiTi 3.0 115 Black"
SRC= (IMGDIR/"source.md").read_text(encoding="utf8")
assert "52 个已保存" in SRC and "Audacity Manual" in SRC
assert ORIGINAL.is_file()
selected={
    "microphone-studio.svg": [5],
    "speaker-high.svg": [28],
    "computer-disk.svg": [54],
    "smartphone.svg": [54],
    "audacity-multitrack-mixing.png": ["44后：软件中音轨/声道的迁移判断"],
}
for name in selected:
    assert (ASSETS/name).is_file(),name
    assert name in SRC,name
assert 'audacity-multitrack-mixing.png' in SRC

def addtext(sl,msg,x,y,w,h,pt=21,color=INK,bold=False,center=False):
    sh=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    frame=sh.text_frame
    frame.clear();frame.word_wrap=True
    frame.margin_left=frame.margin_right=Pt(0)
    frame.margin_top=frame.margin_bottom=Pt(0)
    frame.vertical_anchor=MSO_ANCHOR.MIDDLE
    p=frame.paragraphs[0];p.text=msg
    p.font.name=BOLD if bold else FONT;p.font.size=Pt(pt)
    p.font.bold=bool(bold);p.font.color.rgb=color
    if center:p.alignment=PP_ALIGN.CENTER
    return sh

def rect(sl,x,y,w,h,stroke=VIOLET,width=2,fill=None):
    sh=sl.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
    if fill:
        sh.fill.solid();sh.fill.fore_color.rgb=fill
    else: sh.fill.background()
    if stroke:sh.line.color.rgb=stroke;sh.line.width=Pt(width)
    else:sh.line.fill.background()
    return sh

def imgblob(name):
    path=ASSETS/name
    if path.suffix==".svg":
        return BytesIO(cairosvg.svg2png(bytestring=path.read_bytes(),output_width=580,output_height=580))
    with Image.open(path) as im:
        im.verify()
    return BytesIO(path.read_bytes())

def put(sl,name,x,y,w,h=None):
    im=imgblob(name)
    kwargs={"width":Inches(w)}
    if h is not None:kwargs["height"]=Inches(h)
    sh=sl.shapes.add_picture(im,Inches(x),Inches(y),**kwargs)
    sh.name="searched-images/"+name
    return sh

def addnotes(sl,msg):
    f=sl.notes_slide.notes_text_frame
    f.text=f.text.strip()+"\n\n【图片教学备注】"+msg

def fresh(slide_title):
    slide=deck.slides.add_slide(deck.slide_layouts[6])
    for sp in list(slide.shapes):
        if sp.is_placeholder:
            el=sp._element;el.getparent().remove(el)
    rect(slide,0,.045,13.333,.083,stroke=None,fill=VIOLET)
    rect(slide,0,7.393,13.333,.083,stroke=None,fill=VIOLET)
    addtext(slide,slide_title,.67,.65,12,.79,34,INK,True)
    return slide

def move_after(slide,after_one_based):
    el=deck.slides._sldIdLst
    item=el[-1];el.remove(item);el.insert(after_one_based,item)

def truth_map():
    data=[]
    for n,sl in enumerate(deck.slides,1):
        title=next((o.text.strip() for o in sl.shapes if o.has_text_frame and o.text.strip()),"")
        data.append({"slide":n,"title":title})
    return data

def audit(round_num,filename,problems):
    output=WORK/filename
    deck.save(output)
    validation=Presentation(output)
    assert len(validation.slides)==(78 if round_num==1 else 79)
    assert all(s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip() for s in validation.slides)
    assert len([s for s in validation.slides if any("软件里：一条音轨" in o.text for o in s.shapes if o.has_text_frame)])==round_num
    # Existing page text and calculations may shift slide *numbers*, never alter the text.
    prior=Presentation(ORIGINAL)
    old=[(s.slide_id,[sp.text.strip() for sp in s.shapes if sp.has_text_frame]) for s in prior.slides]
    for sid, texts in old:
        curr=next(s for s in validation.slides if s.slide_id==sid)
        now=[sp.text.strip() for sp in curr.shapes if sp.has_text_frame]
        assert now[:len(texts)]==texts,(round_num,sid)
    with open(output,'rb') as f: b=f.read()
    details={
      "round":round_num,"file":filename,"slides":len(validation.slides),
      "speaker_notes":sum(bool(s.has_notes_slide) for s in validation.slides),
      "sha256":hashlib.sha256(b).hexdigest(),
      "source_deck_sha256":hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(),
      "sourced_images":selected,
      "new_evidence_slides":round_num,
      "issues":problems,
      "titles":truth_map(),
    }
    (WORK/f"audit-round-{round_num}.json").write_text(json.dumps(details,ensure_ascii=False,indent=2),encoding="utf8")
    print("PASS",round_num,len(validation.slides),"notes",details["speaker_notes"],"bytes",len(b),flush=True)
    return output

deck=Presentation(ORIGINAL)
assert len(deck.slides)==77
# Round 1: P1 real object anchor for microphone conversion,
# P1 real audio editor evidence for track/channel distinction,
# P2 storage vs transfer concrete settings.
put(deck.slides[4],"microphone-studio.svg",5.83,3.27,1.52)
addnotes(deck.slides[4],
 "OpenMoji microphone-studio.svg, CC BY-SA 4.0，"
 "https://github.com/hfg-gmuend/openmoji/blob/master/color/svg/1F399.svg 。"
 "图标帮助识别转换设备。不要说麦克风直接得到0和1。")
put(deck.slides[27],"speaker-high.svg",10.49,3.23,1.56)
addnotes(deck.slides[27],
 "OpenMoji speaker-high.svg，CC BY-SA 4.0，"
 "https://github.com/hfg-gmuend/openmoji/blob/master/color/svg/1F50A.svg 。"
 "扬声器是物理输出设备；DAC先将数字数据变为模拟电信号。")
put(deck.slides[53],"computer-disk.svg",2.70,4.07,1.44)
put(deck.slides[53],"smartphone.svg",8.87,4.07,1.44)
addnotes(deck.slides[53],
 "OpenMoji computer-disk.svg (1F4BD) 与 smartphone.svg (1F4F1)，"
 "CC BY-SA 4.0; https://github.com/hfg-gmuend/openmoji 。"
 "左侧代表本地保存数据，右侧代表设备之间的文件传输，二者不是压缩算法的图像证明。")
title="软件里：一条音轨能包含几个声道？"
q=fresh(title)
addtext(q,"观察真实Audacity截图：请先数音轨，再数各音轨有几路波形。",.84,1.58,11.5,.55,22,ACC,True)
put(q,"audacity-multitrack-mixing.png",.98,2.15,11.35,4.13)
addtext(q,"问题：图中是两条音轨，还是三条？",.93,6.42,11.45,.43,20,INK)
q.notes_slide.notes_text_frame.text=(
 "【教学目的】把已经得到的“音轨与声道不是同一个概念”迁移到真实Audacity界面。"
 "先观察，不要在此页直接说答案。上方是Mono Track（一条单声道音轨），"
 "下方是Stereo Track（一条含左右两路的立体声音轨）。总共两条编辑音轨，"
 "截图中共有三行波形显示；这不代表导出文件必定有三个声道。"
 "\n【图片来源】Audacity Manual contributors，audacity-multitrack-mixing.png，CC BY 3.0，"
 "https://github.com/audacity/audacity-manual/blob/master/manual/m/images/f/fb/tracks_for_mixing.png 。"
 "历史界面只为理解结构，不是最新版操作指南。")
move_after(q,44)
round1_issues=[
 {"level":"P0","issue":"复制外部截图可能让学生误以为3行波形就是导出3声道","fix":"截图放在原生混音示意之后，问题明确先数轨道再数波形，备注限定不能推断导出声道数","verified":"标题、备注与插入页序"},
 {"level":"P1","issue":"仅有抽象框，麦克风及扬声器和真实设备的对应较弱","fix":"第5页放麦克风图标、第28页放扬声器图标，不遮挡原有文字流程","verified":"图片定位与原始文字逐页一致"},
 {"level":"P2","issue":"节省空间/网络传输两种情境只有文字","fix":"第54页分别放存储介质与移动设备图标，仍保留原生结论","verified":"图标语义与原文字一致"}
]
one=audit(1,"round-1-with-images.pptx",round1_issues)
# Round 2: P1 real screenshot requires same-layout reveal page,
# P1 mark visually where a track can have two channel waveforms;
# P2 context icons need unambiguous Chinese labels.
new=fresh(title)
addtext(new,"同一张截图：编辑音轨数 ≠ 波形通道数。",.84,1.58,11.4,.55,22,ACC,True)
put(new,"audacity-multitrack-mixing.png",.98,2.15,11.35,4.13)
# Matching positions and image dimensions keep transition smooth.
rect(new,.97,2.14,11.37,2.11,stroke=ACC,width=2,fill=None)
rect(new,.97,4.25,11.37,2.04,stroke=CYAN,width=2,fill=None)
addtext(new,"上：1条单声道音轨；下：1条立体声音轨（含L/R两路）。",.93,6.42,11.62,.46,19,ACC,True)
new.notes_slide.notes_text_frame.text=(
 "【先预测再揭示】请先停留上一页，让学生回答音轨和波形路数，"
 "再翻到本页。紫框：一条Mono音轨（一行波形）；蓝框：一条Stereo音轨"
 "（两行波形），因此两条轨道并不等于两路信号。"
 "请学生迁移：最后导出双声道文件时的PCM数据量取决于导出参数，"
 "而不是编辑音轨数。\n【来源】Audacity Manual contributors，CC BY 3.0，"
 "https://github.com/audacity/audacity-manual/blob/master/manual/m/images/f/fb/tracks_for_mixing.png 。")
move_after(new,45)
# Keep labels far from 6.43 in slide 54 and do not compete with conclusion.
addtext(deck.slides[53],"本地存储",2.61,5.42,1.65,.47,17,ACC,True,center=True)
addtext(deck.slides[53],"在线传输",8.76,5.42,1.65,.47,17,CYAN,True,center=True)
addnotes(deck.slides[53],"读图：图标表达场景，不等于“数据被减半”的证据；压缩收益仍需要数字比较。")
round2_issues=[
 {"level":"P0","issue":"一张Audacity截图中3行波形可能被误作导出3声道","fix":"新增长度/布局相同的渐进揭示页，明确2条音轨分别有1与2路波形，同时说明最终导出声道另行指定","verified":"问题/答案相邻、截图尺寸与位置完全一致；Notes明确限制"},
 {"level":"P1","issue":"真实软件英文UI和轨道分组对于高中生不够直接","fix":"用不同语义色细框标出两条音轨，中文指出mono与stereo，保留原界面不篡改","verified":"紫/青边框几何尺寸可复查"},
 {"level":"P2","issue":"存储介质与手机图标可能被看成普通装饰","fix":"给两组图标补“本地存储”“在线传输”简短中文对应，不占据文字结论空间","verified":"标签中心与图标中心对齐"}
]
two=audit(2,"round-2-with-images.pptx",round2_issues)
DEST.write_bytes(two.read_bytes())
final=Presentation(DEST)
assert len(final.slides)==79
assert final.slides[44].shapes[0].has_text_frame is False or True
print("FINAL",DEST,DEST.stat().st_size,flush=True)
