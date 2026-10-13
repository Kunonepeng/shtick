#!/usr/bin/env python3
"""Build v5 from the REAL v4 PPTX in this repository.
Keeps all 60 existing slides/notes and appends classroom explanations/exercises.
"""
from pathlib import Path
import math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "1-2-3-audio-encoding-v4.pptx"
OUT = ROOT / "1-2-3-audio-encoding-v5.pptx"
p = Presentation(str(SRC))
assert len(p.slides) == 60, f"v4 baseline expected 60 slides, got {len(p.slides)}"

V = RGBColor(98,81,177)
A = RGBColor(140,100,225)
C = RGBColor(0,176,240)
BLACK = RGBColor(38,38,38)
GRAY = RGBColor(112,112,112)
L = RGBColor(225,225,230)
WHITE = RGBColor(255,255,255)
SOFT = RGBColor(250,248,255)
FONT = "Alibaba PuHuiTi 3.0 55 Regular"
HEAVY = "Alibaba PuHuiTi 3.0 115 Black"

def rect(s,x,y,w,h,fill=None,stroke=None,width=1):
    sh=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
    if fill: sh.fill.solid(); sh.fill.fore_color.rgb=fill
    else: sh.fill.background()
    if stroke: sh.line.color.rgb=stroke; sh.line.width=Pt(width)
    else: sh.line.fill.background()
    return sh

def line(s,x1,y1,x2,y2,col=A,width=2):
    sh=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x1),Inches(y1),Inches(x2),Inches(y2))
    sh.line.color.rgb=col; sh.line.width=Pt(width)
    return sh

def text(s,value,x,y,w,h,size=22,bold=False,col=BLACK,align=None):
    sh=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    f=sh.text_frame; f.clear(); f.word_wrap=True
    f.margin_left=f.margin_right=Pt(0); f.margin_top=f.margin_bottom=Pt(0)
    for j,t in enumerate(value.split("\n")):
        pg=f.paragraphs[0] if j==0 else f.add_paragraph()
        pg.text=t; pg.space_before=Pt(0); pg.space_after=Pt(4)
        if align is not None: pg.alignment=align
        pg.font.name=HEAVY if bold else FONT
        pg.font.size=Pt(size); pg.font.bold=bold; pg.font.color.rgb=col
    return sh

def new(title,notes):
    s=p.slides.add_slide(p.slide_layouts[min(6, len(p.slide_layouts)-1)])
    for ph in list(s.placeholders):
        sh=ph._element; sh.getparent().remove(sh)
    rect(s,0,0,13.333,.09,V)
    rect(s,0,7.41,13.333,.09,V)
    text(s,title,.67,.66,12,.72,36,True)
    s.notes_slide.notes_text_frame.text=notes
    return s

def item(s,heading,body,x,y,w,num=None):
    if num is not None:
        text(s,str(num),x,y,.48,.55,25,True,A); x+=.52;w-=.52
    text(s,heading,x,y,w,.46,24,True,A)
    text(s,body,x,y+.62,w,1.12,20)
    
def bottom(s,msg,y=6.55):
    line(s,.8,y-.15,12.5,y-.15,L,1)
    text(s,msg,.84,y,11.8,.55,21,True,A)

def problems(n,q,answer,explain,notes=""):
    title="练习题 "+str(n)
    nq=new(title,"让学生先独立思考1分钟，再请同学解释理由。"+notes)
    text(nq,q,.88,1.93,11.65,2.60,25,False)
    line(nq,.9,4.9,12.35,4.9,L,1.5)
    text(nq,"先预测 / 列式，再说明理由。",.9,5.3,11,.65,22,True,A)
    na=new(title,"答案页。先听学生解释，再揭示；追问哪个概念决定答案。"+notes)
    text(na,q,.88,1.93,11.65,2.60,25,False)
    line(na,.9,4.65,12.35,4.65,L,1.5)
    text(na,answer,.95,4.92,11.4,.56,25,True,A)
    text(na,explain,.95,5.57,11.4,1.45,20)
    return nq,na

# 61: transition
s=new("声音已经数字化了，为什么还要压缩？",
      "连接前半段PCM数字化与后半段压缩。学生先回顾：采样、量化、编码完成后，文件大小由什么决定？新问题是怎样在保存信息的同时减少数据。")
text(s,"声音 → 采样 → 量化 → 编码 → PCM数据",.9,1.95,11.8,.73,26,True)
line(s,1,3.05,12.0,3.05,A,3)
item(s,"已经回答的问题","声音怎样变成可存储的0和1？",.9,3.6,5.55)
item(s,"接下来追问","为什么文件会很大？怎样减小数据量？",7,3.6,5.42)
bottom(s,"本次重点：计算数据量 → 识别可压缩信息 → 区分无损和有损。")

# 62: four factors
s=new("PCM数据量，究竟由哪四个因素决定？",
      "回看原v4的PCM数据量推导。逐个询问：采样率、每样本位数、声道数、时长如何决定总比特数。kHz换算1000，Byte换算8。")
parts=[("采样率","每秒每声道取样多少次"),("量化位数","每个样本使用多少bit"),
       ("声道数","同一时刻记录几路"),("时长","持续多少秒")]
for k,(a,b) in enumerate(parts):
    x=.86+(k%2)*6.2;y=1.76+(k//2)*1.70
    text(s,a,x,y,5.3,.48,25,True,A)
    text(s,b,x,y+.58,5.4,.72,21)
line(s,.86,5.30,12.45,5.30,L,1.5)
text(s,"字节数 = 采样率 × 位数 × 声道数 × 秒数 ÷ 8",.87,5.57,11.6,.60,26,True)
bottom(s,"注意：1 kHz = 1000 Hz；1 Byte = 8 bit。",6.66)

# 63-64: audio size exercise
problems(1,
 "录制1分钟未压缩双声道PCM音频：\n采样率48,000 Hz，量化位数16 bit。\n样本数据量约多少MB？（按1 MB = 1024² B）",
 "答案：≈ 10.99 MB（课堂取约10.98 MB）",
 "48,000 × 16 × 2 × 60 ÷ 8 = 11,520,000 B\n11,520,000 ÷ 1024 ÷ 1024 ≈ 10.99",
 "重点检查学生能否解释四个数；严格来说除以1024²后的单位是MiB，课堂资料称MB。WAV头部有少量开销。")

# 65: tracks and channels
s=new("多加一条“音轨”，就是多加一个“声道”吗？",
      "此页制造有价值的分歧：编辑器里的音轨只是用于分层组织素材；声道是每时刻需存储的独立输出声音数据。两条音轨混合后仍可输出立体声，不必变为四声道。")
text(s,"编辑工程：两条音轨",.85,1.86,5.50,.52,26,True,A)
text(s,"导出音频：两个声道",7.2,1.86,5.25,.52,26,True,C)
for i,(lab,color) in enumerate((("朗诵人声",A),("背景音乐",C))):
    y=2.83+i*.97
    rect(s,.85,y,4.9,.59,stroke=color,width=2)
    text(s,lab,1.13,y+.11,4.2,.35,22)
line(s,6.17,3.38,6.75,3.38,A,3)
text(s,"混合",6.17,3.65,.85,.38,19,True,A)
for i,(lab,color) in enumerate((("左声道 L",C),("右声道 R",C))):
    y=2.83+i*.97
    rect(s,7.35,y,4.72,.59,stroke=color,width=2)
    text(s,lab,7.66,y+.11,4.0,.35,22)
text(s,"音轨 = 编辑时分几层",.9,5.18,5.4,.6,24,True)
text(s,"声道 = 输出时有几路",7.15,5.18,5.4,.6,24,True)
bottom(s,"混音能改变声音内容，却不一定改变采样率、位数、声道数或时长。")

# 66-67: track exercise
problems(2,
 "一段5分钟的44.1 kHz、16 bit、双声道诗朗诵，\n新增一条等时长背景音乐音轨。\n保持PCM参数不变，混音导出后数据量怎样变化？",
 "答案：未压缩样本数据量不变。",
 "因为采样率、位数、声道数、时长都不变。\n新增“音轨”≠新增“声道”。",
 "教师可让学生投票“变大／不变／变小”，再要求用容量公式检验。结论只对题设的未压缩PCM与固定参数成立；压缩文件不一定大小相同。")

# 68 image/audio comparison
s=new("图像与声音，如何做同一种数字化思考？",
      "连接前面图像编码已有知识。图像对空间网格取样，声音对时间位置取样；图像位深度与PCM量化位数都限定每个样本的信息表示。")
heads=[("比较维度",.85,3),("图像",3.6,4.1),("声音",8.02,4.5)]
for a,x,w in heads: text(s,a,x,1.9,w,.52,24,True,A)
rows=[
 ("在哪里取样","二维空间网格","一维时间轴"),
 ("取样多少","宽×高：像素数","每秒：采样率"),
 ("每个值多细","位深度","量化位数"),
 ("数据量思路","像素数×位深度","采样率×秒数×声道×位数")]
for i,(a,b,c) in enumerate(rows):
    y=2.70+i*.81
    line(s,.9,y-.13,12.2,y-.13,L,1)
    text(s,a,.85,y,2.6,.6,19,True)
    text(s,b,3.6,y,4.15,.6,19)
    text(s,c,8.02,y,4.35,.6,19)
bottom(s,"共同点：先采样，再将样本量化并编码；数据量取决于样本数×每样本位数。",6.55)

# 69: video bridge from third transcript
s=new("为什么连续播放静态图像，会让我们看到运动？",
      "来自第三份课堂记录：视频可看作按时间排列的图像帧。不要把0.024秒当作所有人的严格视觉阈值。用翻页动画的经验建立图像帧与帧率概念。")
for i,word in enumerate(("画面1","画面2","画面3","画面4")):
    x=.80+i*3.08
    rect(s,x,2.15,2.7,2.1,stroke=A,width=2)
    text(s,word,x+.30,2.97,2.2,.57,26,True,A,PP_ALIGN.CENTER)
    if i<3: line(s,x+2.72,3.20,x+3.02,3.20,C,3)
text(s,"每秒播放25帧 → 帧率25 fps",.88,4.97,11.8,.70,28,True)
bottom(s,"视频的数字化记录：一帧一帧图像按时间顺序排列，通常还配有音频。")

# 70-71: video problem
problems(3,
 "10分钟无声、未压缩视频：\n每帧480 × 320像素，24 bit/像素，每秒25帧。\n样本数据量约多少GiB？",
 "答案：约6.44 GiB（课堂可近似记为6.4 GB）。",
 "单帧：480×320×24÷8 = 460,800 B\n总帧数：25×600 = 15,000帧\n总量：6,912,000,000 B ÷ 1024³ ≈ 6.44 GiB",
 "学生先说明“视频数据量＝单帧图片数据量×总帧数”，再计算。此例特意无声，忽略容器头部和压缩。")

# 72 why compression
s=new("为什么我们刷的10分钟视频，通常远小于6.4 GiB？",
      "认知冲突。问学生：刚才公式错了吗？引导认识容量估算是未压缩数据量；常见视频会使用编码压缩以减少存储和网络传输负担。")
text(s,"未压缩：每帧几乎都完整保存",.90,1.84,11.2,.58,26,True)
for k in range(8):
    rect(s,.94+k*.78,2.75,.67,1.35,stroke=A,width=1.3)
text(s,"大量重复和相似的信息",8.0,3.11,4.2,.66,22)
line(s,1,4.64,12.0,4.64,L,2)
text(s,"观察：连续画面之间，哪些地方可能没有变化？",.93,5.04,11.6,.73,25,True,A)
bottom(s,"新问题：能不能更聪明地编码，少保存一些重复或不重要的信息？",6.43)

# 73 objectives
s=new("压缩有两个直接目的。",
      "学生用手机内存不够、网速慢的日常情境作例子。尽量说全两个目的：节约存储空间、降低传输数据量和时间；还需考虑压缩/解压开销。")
item(s,"① 节约存储空间","同样容量的手机、U盘、硬盘，能够保存更多文件。",.97,2.06,11.2)
item(s,"② 提高传输效率","网络上需要传送的数据更少；通常有助于更快完成传输。",.97,4.22,11.2)
bottom(s,"压缩关注的是“表示一份内容需要多少bit”，不是给文件“挤压体积”。")

# 74 essence
s=new("压缩的本质：换一种更节省的编码。",
      "用简单可还原的示例讲解无损编码思路，注意“AAAAAA→A×6”只是一种概念演示，不是RAR真实算法；有损压缩可能舍弃难以察觉的细节。")
text(s,"AAAAAA",1.20,2.15,4.5,.92,43,True)
line(s,5.4,2.7,7.4,2.7,A,3)
text(s,"A × 6",8.15,2.17,3.6,.92,41,True,A)
text(s,"重复很多次的内容",.91,3.87,5.1,.61,24)
text(s,"用规则和次数来表示",7.8,3.87,4.6,.61,24)
bottom(s,"压缩 = 对数据重新编码；越多内容能用更短规则表达，通常越容易压缩。")

# 75 lossless/lossy
s=new("无损压缩与有损压缩，判别标准是什么？",
      "以能否恢复压缩前数据为判别标准。ZIP/RAR属于常见无损归档格式；MP3通常是有损音频；JPG通常为有损图像；MP4是容器，常装有损视频，主线可用“常见MP4视频”这一说法。")
text(s,"无损压缩",.85,1.88,5.5,.58,28,True,A)
text(s,"有损压缩",6.88,1.88,5.5,.58,28,True,C)
line(s,6.49,1.8,6.49,6.0,L,2)
text(s,"还原后与原数据完全一致。",.87,2.91,5.4,1.06,23,True)
text(s,"例：ZIP、RAR",.87,4.29,5.25,.72,23)
text(s,"适合：程序、文档、源文件备份",.87,5.22,5.45,.89,21)
text(s,"还原后不能与原数据完全一致。",6.91,2.91,5.4,1.06,23,True)
text(s,"例：MP3、JPG、常见MP4视频",6.91,4.29,5.25,.83,22)
text(s,"适合：可接受一定失真的多媒体",6.91,5.22,5.4,.89,21)
bottom(s,"先问“必须完全恢复吗？”再决定采用哪种压缩方案。",6.59)

# 76 redundancy
s=new("哪一种图像更容易被无损压缩？",
      "比较相同尺寸和位深度的纯色、色块、复杂图像。引导归纳冗余和规律，而不是认为“颜色少必然”对任意压缩算法成立。")
for i,(lab,colors) in enumerate((
    ("A 纯色",[A]*48),
    ("B 色块",[A if j//6<4 else C for j in range(48)]),
    ("C 细节变化",[A if (j*11)%7<3 else C for j in range(48)]))):
    x=.77+i*4.24
    text(s,lab,x,1.96,3.6,.52,26,True)
    for j,color in enumerate(colors):
        xx=x+(j%8)*.39
        yy=2.74+(j//8)*.39
        rect(s,xx,yy,.36,.36,color)
    text(s,("重复最多","部分重复","变化很多")[i],x,5.42,3.6,.55,22,True,A if i==0 else GRAY)
bottom(s,"相同大小的未压缩位图，用无损算法处理时，A通常最容易压缩。")

# 77-78 picture problem
problems(4,
 "两个大小相同的BMP位图：\nA是纯色图，B是彩色风景图。\n分别转换为RAR压缩文件后，哪个通常更小？为什么？",
 "答案：A（纯色图）通常更小。",
 "A中规律和重复信息更多，冗余度更高。\nRAR可用更短的方式表示这些重复数据。",
 "使用“通常”，因为不同数据与压缩器细节可能影响实际字节数。让学生说出冗余度，而非只报字母。")

# 79 re-compress
s=new("有损压缩过的文件，再压一次就会小很多吗？",
      "课堂类比已脱水衣物。提醒：再次采用有损编码不一定保持音质，可能累计失真；采用归档压缩对已经高度压缩的MP3、JPG通常帮助有限。")
item(s,"第一次压缩","例如由PCM转成MP3，原本可以省下大量数据。",.94,1.90,11.5)
item(s,"再次压缩","已有压缩表示通常缺少易利用的冗余，大小未必明显减少。",.94,3.80,11.5)
bottom(s,"重要取舍：文件大小、还原质量、处理时间，不可能只看一个指标。")

# 80-81 classification exercise
problems(5,
 "下列典型用途适合哪种压缩？\n① 源代码长期备份；② 网络音乐播放；\n③ 存放一份需要逐字还原的文档。",
 "答案：①无损 ②通常有损 ③无损。",
 "ZIP/RAR保留原字节；MP3等有损音频编码可减少数据量。\n但音乐也可以选FLAC等无损方式。",
 "考察场景选择，不要让学生误以为所有音频只能有损、所有图像都必须有损。")

# 82-83 comprehensive
problems(6,
 "判断并解释：\nA. 给音频多加一条音轨，未压缩PCM数据量一定翻倍。\nB. 相同参数下，时长加倍，PCM数据量加倍。\nC. 已经是MP3的文件，再用RAR压缩通常收益很小。",
 "答案：A错；B对；C通常对。",
 "A把“音轨”误当“声道”；B直接用PCM数据量公式；\nC因为编码后的MP3通常已去除许多可压缩冗余。",
 "让学生解释三个答案背后的不同知识：音轨与声道、容量公式、冗余。")

# 84 final recap
s=new("收束：从声音的0和1，到可管理的文件",
      "请学生离开课堂前解释三件事：采样量化编码各解决什么？PCM大小由哪四因素决定？无损和有损如何选择？视频算式是拓展迁移。")
text(s,"声音数字化",.90,1.78,3.52,.55,25,True,A)
text(s,"连续信号 → 采样 → 量化 → 编码 → PCM",.91,2.43,11.6,.67,23)
line(s,.92,3.32,12.2,3.32,L,1.2)
text(s,"大小为什么不同？",.90,3.67,4.8,.55,25,True,A)
text(s,"采样率 × 量化位数 × 声道数 × 时间（再换单位）",.91,4.30,11.5,.63,22)
line(s,.92,5.17,12.2,5.17,L,1.2)
text(s,"怎样减小文件？",.90,5.52,4.8,.52,25,True,A)
text(s,"压缩重新编码：无损可完全还原；有损允许信息差异。",.91,6.08,11.8,.65,21)

assert len(p.slides)==84
assert all(s.notes_slide.notes_text_frame.text.strip() for s in p.slides)
OUT.parent.mkdir(parents=True,exist_ok=True)
p.save(str(OUT))
print("Built",len(p.slides),"slides:",OUT,OUT.stat().st_size,"bytes")
