#!/usr/bin/env python3
"""Fuse v8.1.codex + v8.4.10 and conduct ten consecutive visual refinements.
Every round is derived from the immediately preceding saved PPTX and audited.
This uses only two committed, authentic GitHub decks.
"""
from pathlib import Path
from io import BytesIO
import hashlib, json, math, copy
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE,MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
OUT=HERE/"rounds"
OUT.mkdir(parents=True,exist_ok=True)
BASE=ROOT/"1-2-3-audio-encoding-v8.1.codex.pptx"
REF=ROOT/"1-2-3-audio-encoding-v8.4.10.pptx"
V=RGBColor(98,81,177); A=RGBColor(140,100,225)
CYAN=RGBColor(0,176,240); DKCYAN=RGBColor(0,124,155)
INK=RGBColor(38,38,38); GR=RGBColor(125,125,125)
RED=RGBColor(228,46,46); WHITE=RGBColor(255,255,255)
LT=RGBColor(230,230,236); SHADE=RGBColor(246,243,255)
FONT="Alibaba PuHuiTi 3.0 55 Regular"; BOLD="Alibaba PuHuiTi 3.0 115 Black"
W=13.333;H=7.5
base=Presentation(BASE);ref=Presentation(REF)
assert len(base.slides)==77,len(base.slides)
assert len(ref.slides)==70,len(ref.slides)
source_titles=[next((s.text.strip() for s in sl.shapes if s.has_text_frame and s.text.strip()),"") for sl in base.slides]
assert "连续的图片" in source_titles[47]
def box(sl,x,y,w,h,fill=None,border=None,width=1):
 s=sl.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
 if fill:s.fill.solid();s.fill.fore_color.rgb=fill
 else:s.fill.background()
 if border:s.line.color.rgb=border;s.line.width=Pt(width)
 else:s.line.fill.background()
 # Switch off shape-theme shadows; diagrams should not look like cards.
 for elem in s._element.xpath('.//a:effectRef'):
  elem.set('idx','0')
 return s
def text(sl,val,x,y,w,h,size=21,color=INK,bold=False,center=False):
 s=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
 f=s.text_frame;f.clear();f.word_wrap=True
 f.margin_left=f.margin_right=Pt(0);f.margin_top=f.margin_bottom=Pt(0)
 f.vertical_anchor=MSO_ANCHOR.MIDDLE
 for i,row in enumerate(str(val).split("\n")):
  p=f.paragraphs[0] if not i else f.add_paragraph()
  p.text=row;p.font.name=BOLD if bold else FONT;p.font.size=Pt(size)
  p.font.bold=bold;p.font.color.rgb=color
  p.space_after=Pt(2)
  if center:p.alignment=PP_ALIGN.CENTER
 return s
def line(sl,x1,y1,x2,y2,color=A,pt=2):
 s=sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x1),Inches(y1),Inches(x2),Inches(y2))
 s.line.color.rgb=color;s.line.width=Pt(pt);return s
def circ(sl,x,y,r,color=CYAN,border=None):
 s=sl.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x-r), Inches(y-r), Inches(2*r), Inches(2*r))
 s.fill.solid();s.fill.fore_color.rgb=color
 s.line.fill.background() if border is None else None
 if border:s.line.color.rgb=border
 return s
def n(sl,msg):
 s=sl.notes_slide.notes_text_frame
 s.text=s.text.strip()+"\n\n【视觉说明】"+msg
def image_from_ref(sl,source_number,x,y,w,h):
 originals=[s for s in ref.slides[source_number-1].shapes if s.shape_type==13]
 assert originals,source_number
 b=originals[0].image.blob
 sh=sl.shapes.add_picture(BytesIO(b),Inches(x),Inches(y),width=Inches(w),height=Inches(h))
 sh.name="融合证据图_v8.4.10_原页"+str(source_number)
 return sh
def cover(sl,x,y,w,h):
 return box(sl,x,y,w,h,WHITE)
def marker(sl,label,x,y,w=3.0,color=A):
 text(sl,label,x,y,w,.36,17,color,True)
def persist(p,filename,meta):
 dest=ROOT/filename if filename.startswith("1-2") else OUT/filename
 p.save(dest)
 check=Presentation(dest)
 assert len(check.slides)==77
 assert all(sl.has_notes_slide and len(sl.notes_slide.notes_text_frame.text.strip())>35 for sl in check.slides)
 with ZipFile(dest) as z:assert z.testzip() is None
 hashes=[hashlib.sha256(sh.image.blob).hexdigest() for sl in check.slides for sh in sl.shapes if sh.shape_type==13]
 payload={"filename":dest.name,"bytes":dest.stat().st_size,"sha256":hashlib.sha256(dest.read_bytes()).hexdigest(),"slides":len(check.slides),"speaker_notes":77,"pictures":len(hashes),"picture_sha256":hashes[:20],"change":meta}
 (HERE/(dest.stem+".audit.json")).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
 print("VALIDATED",dest.name,meta, flush=True)
 return dest
def reopen(dest): return Presentation(dest)

# v8.5: Codex retains all 77 originally structured slides, tree-builds,
# exercise/reveal sequence and illustrative scenarios. Borrow only visuals
# where v8.4.10 adds distinct evidence, rather than decorating every slide.
p=base
s=p.slides[2];image_from_ref(s,3,2.12,3.00,8.90,3.18)
n(s,"复用v8.4.10声源图；上面已有的声源→空气→耳朵框为结构，图片帮助看到音叉与麦克风，波弧代表传播示意，不是波形传播路线。")
s=p.slides[7];cover(s,.78,1.71,11.8,4.03);image_from_ref(s,8,2.02,2.10,9.20,3.95)
marker(s,"空间里：扰动传到记录点",1.17,1.80,5.5)
marker(s,"固定位置：信号随时间变化",7.04,1.80,5.6)
n(s,"借用v8.4.10空间传播与固定测点时间波形的对照，前半是空间快照，后半不是声音弯曲路线。")
s=p.slides[26];cover(s,.78,2.06,11.73,3.64);image_from_ref(s,27,1.20,2.30,10.9,3.38)
marker(s,"描述如何解释音频数据",1.28,2.18,4.05)
marker(s,"保存一系列数字样本",5.04,2.18,6.70,DKCYAN)
n(s,"借用v8.4.10文件结构图；文件头是必要的格式信息，PCM样本是内容。每个小格仅为示意，不承诺WAV固定44Byte。")
s=p.slides[65];cover(s,.78,1.82,11.75,4.27)
marker(s,"左：原始局部（放大）",1.15,2.15,5.1)
marker(s,"右：低质量JPEG（放大）",7.0,2.15,5.15,DKCYAN)
image_from_ref(s,63,1.18,2.66,10.90,3.05)
n(s,"借用v8.4.10同一局部的BMP/JPG示例；解释刻意极端的JPEG实验质量不代表常见JPG都如此模糊，且JPEG压缩情况受内容参数影响。")
p.core_properties.title="声音数字化与压缩 v8.5.gpt｜Codex结构 × v8.4.10教学证据图"
p.core_properties.subject="高中信息科技：融合图示与两课时问题链"
dest=persist(p,"1-2-3-audio-encoding-v8.5.gpt.pptx","融合Codex 77页学习结构与v8.4.10四项有效视觉证据（3/8/27/66）")

# Ten distinct visual improvement rounds; each pass is read from the prior PPTX.
ROUND_DETAILS=[
 ("P0","第48页五帧运动球全部同位置，形成错误视觉证据","重绘同一球在连续五帧内的明显位置变化"),
 ("P1","第13页采样数量虽正确但点数与概念联系不够醒目","标注同一秒窗口内1个与2个采样点"),
 ("P1","第16页八级量化线数量正确，但等级分组难一眼确认","加入0～7总共8级的侧边指示"),
 ("P1","第18页样本3.71、等级L3、代表值3.5缺少误差方向提示","显示原值→代表值及误差的简短数值关系"),
 ("P1","第19页十组码字标签过小，首组注意目标不够稳定","将第一组的L3→011单独放大，避免丢失对应关系"),
 ("P1","第24页4 bit与3 bit横纵控制变量混淆风险","增加采样点数量不变、纵向等级增多的并列提示"),
 ("P1","第46页双声道与单声道同一时刻记录数量需要更直接的计数","加入“每时刻2个样本/1个样本”的固定颜色对照"),
 ("P1","第52页视频数据量认知冲突纯文字，不容易看见数量差异","增加无损计算值与实际文件大小待解释的疑问尺"),
 ("P1","第61页无损/有损主要是文字，信息是否一致较抽象","用三幅像素格画出原始、无损一致、有损有差别"),
 ("P2","第66页BMP/JPG实验已具视觉对照，但必要的比较条件不够显眼","突出“同一裁剪区域、实验性极低JPEG质量”，防止以图代结论"),
]

for i,(rank,problem,solution) in enumerate(ROUND_DETAILS,1):
 prev=dest
 p=reopen(prev)
 slide_no=[48,13,16,18,19,24,46,52,61,66][i-1]
 s=p.slides[slide_no-1]
 if i==1:
  cover(s,.65,2.01,11.96,3.99)
  for j in range(5):
   x=.77+j*2.45
   box(s,x,2.34,2.20,2.17,LT,WHITE)
   # Same box and size in each frame, changing only ball x position.
   xx=x+.31+.34*j
   circ(s,xx,3.41,.16,CYAN)
   text(s,f"第{j+1}帧",x,4.56,2.2,.45,17,GR,center=True)
  text(s,"同一个球，位置随着时间由左向右变化。",1.28,5.22,10.8,.56,23,A,True,center=True)
  n(s,"上一版第48页五帧的球处于同一水平位置，无法观察运动。本轮用相同边框坐标重绘，球心每帧向右变化；先预测下一帧球将在哪里。")
 if i==2:
  text(s,"在1秒内：1个采样点",9.38,2.43,3.24,.48,18,A,True)
  text(s,"在1秒内：2个采样点",9.38,4.17,3.24,.48,18,DKCYAN,True)
  n(s,"明确[0,1)秒、右端点不重复记。演示1 Hz取1点，2 Hz取2点；此为慢速教学模型。")
 if i==3:
  box(s,10.7,2.76,1.74,2.30,SHADE,A)
  text(s,"L0–L7",10.87,3.07,1.38,.52,22,A,True,center=True)
  text(s,"共 8 级",10.87,3.95,1.38,.55,19,INK,True,center=True)
  n(s,"此页只建立8个等级编号，暂不揭示需要3bit，以便后续由学生推导。")
 if i==4:
  text(s,"原值3.71 → 代表值3.50",8.30,5.98,4.24,.43,19,A,True)
  n(s,"区间[3,4)对应L3，代表值为3.5，绝对差为0.21；这是本例量化误差，不是所有量化算法必然的结果。")
 if i==5:
  box(s,3.04,5.19,7.26,.99,SHADE,A)
  text(s,"样本1：等级 L3 → 3 bit码字 011",3.18,5.40,7.0,.52,23,A,True,center=True)
  n(s,"先看整行十组数据，再聚焦第一个样本，教师问三位码字如何由等级编号得到，不把它误看为样本数量。")
 if i==6:
  text(s,"横向：采样时刻不变；纵向：等级从8级增至16级",2.15,6.04,9.1,.42,18,A,True,center=True)
  n(s,"采样时刻相同，改变量化位数，横向样本点数量不变；更密集的是纵向可选择的代表值。")
 if i==7:
  box(s,.80,5.39,5.54,.65,SHADE,A)
  text(s,"双声道：每时刻2个样本",.98,5.48,5.10,.44,19,A,True)
  box(s,6.68,5.39,5.54,.65,RGBColor(241,250,255),CYAN)
  text(s,"单声道：每时刻1个样本",6.86,5.48,5.10,.44,19,DKCYAN,True)
  n(s,"同一个时刻双声道需要两个样本，单声道一个样本。讨论仍需固定采样率、位数、时长才能得出样本字节数减半。")
 if i==8:
  # Preserve uncertainty: question must not disclose a fabricated encoded file size.
  box(s,1.1,4.58,5.16,1.10,SHADE,A)
  text(s,"逐帧未压缩估算",1.30,4.72,4.7,.37,19,A,True,center=True)
  text(s,"约 6.44 GiB",1.31,5.10,4.7,.40,22,INK,True,center=True)
  box(s,7.12,4.58,5.11,1.10,RGBColor(241,250,255),DKCYAN)
  text(s,"实际压缩文件",7.27,4.72,4.74,.37,19,DKCYAN,True,center=True)
  text(s,"为什么可能小得多？",7.27,5.10,4.74,.40,22,INK,True,center=True)
  n(s,"数值仅是本课逐帧未压缩的理论计算；不虚构“普通视频”必定多少MB，由压缩原理解释差别。")
 if i==9:
  # Self-contained small pixel demonstration; same pixels for original and lossless,
  # one deliberately changed pixel for lossy approximation.
  colors=[RGBColor(48,125,184),RGBColor(92,174,213),RGBColor(164,204,229)]
  for group,label in enumerate(["原始","无损恢复","有损近似"]):
   x=1.60+4.05*group
   text(s,label,x,3.76,3.0,.4,21,A if group<2 else DKCYAN,True,center=True)
   for r in range(4):
    for c in range(8):
     k=(r*5+c*3)%3
     if group==2 and (r,c) in {(0,6),(2,3),(3,5)}:k=(k+1)%3
     box(s,x+.34*c,4.33+.35*r,.33,.33,colors[k])
  text(s,"逐格一致",4.93,5.83,2.35,.39,18,A,True)
  text(s,"部分细节变化",9.06,5.83,2.50,.39,18,DKCYAN,True)
  n(s,"像素图只是数学示意：原始与无损恢复逐值一致，有损近似允许不同。不能据此讲解JPEG的实际DCT步骤。")
 if i==10:
  box(s,1.52,5.83,10.30,.53,SHADE,LT)
  text(s,"对照条件：同一局部放大 · JPEG极低质量只为放大差别",1.66,5.88,10.04,.42,18,A,True,center=True)
  n(s,"该图使用同一局部而非两张毫不相关的图；极端压缩用于观察差别，不推断所有JPEG都严重失真。")
 dest=persist(p, f"round-{i:02d}.pptx",{"round":i,"rank":rank,"problem":problem,"fix":solution,"source_file":prev.name})
 # Re-read saved source as input to the next round (not a fresh baseline).

# Final standalone v8.6 is a byte-for-byte copy of the 10th reviewed version.
final=ROOT/"1-2-3-audio-encoding-v8.6.gpt.pptx"
final.write_bytes(dest.read_bytes())
with ZipFile(final) as z:assert z.testzip() is None
assert hashlib.sha256(final.read_bytes()).hexdigest()==hashlib.sha256(dest.read_bytes()).hexdigest()
print("FINAL",str(final),final.stat().st_size,flush=True)
