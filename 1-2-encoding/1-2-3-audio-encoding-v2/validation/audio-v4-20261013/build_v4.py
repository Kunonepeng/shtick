#!/usr/bin/env python3
"""Build audio encoding v4 from the preserved v3. No edits to v3."""
from __future__ import annotations
import math, os, wave, struct, re
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.xmlchemy import OxmlElement

SRC=Path(os.environ.get('V3_PPTX','1-2-encoding/1-2-3-audio-encoding-v2/1-2-3-audio-encoding-v3.pptx'))
OUT=Path(os.environ.get('V4_PPTX','1-2-encoding/1-2-3-audio-encoding-v2/1-2-3-audio-encoding-v4.pptx'))
ASSET=OUT.parent/'audio-v4-assets'
VIO=RGBColor(98,81,177); ACC=RGBColor(140,100,225); CYAN=RGBColor(0,176,240)
RED=RGBColor(255,0,0); INK=RGBColor(38,38,38); MUTED=RGBColor(105,105,105)
GRAY=RGBColor(175,175,175); LIGHT=RGBColor(229,229,234); WHITE=RGBColor(255,255,255)
REG='Alibaba PuHuiTi 3.0 55 Regular'; BLACK='Alibaba PuHuiTi 3.0 115 Black'

p=Presentation(SRC)
assert len(p.slides)==54, f'Expected 54 slides in v3, found {len(p.slides)}'

def rect(sl,x,y,w,h,fill=None,outline=None,width=1):
    sh=sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb=fill or WHITE
    if outline: sh.line.color.rgb=outline; sh.line.width=Pt(width)
    else: sh.line.fill.background()
    return sh

def line(sl,x1,y1,x2,y2,color=ACC,width=1.7):
    a=sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    a.line.color.rgb=color; a.line.width=Pt(width); return a

def tx(sl,text,x,y,w,h,size=22,bold=False,color=INK,align=None,font=None):
    s=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    s.text_frame.clear();s.text_frame.word_wrap=True
    s.text_frame.margin_left=Pt(0);s.text_frame.margin_top=Pt(0);s.text_frame.margin_right=Pt(0);s.text_frame.margin_bottom=Pt(0)
    for idx,l in enumerate(text.split('\n')):
        q=s.text_frame.paragraphs[0] if idx==0 else s.text_frame.add_paragraph()
        q.text=l;q.space_before=Pt(0);q.space_after=Pt(2)
        if align is not None:q.alignment=align
        q.font.name=font or (BLACK if bold else REG);q.font.size=Pt(size);q.font.bold=bold;q.font.color.rgb=color
    return s

def base(title,note):
    sl=p.slides.add_slide(p.slide_layouts[min(6,len(p.slide_layouts)-1)]);
    for placeholder in list(sl.placeholders):
        node=placeholder._element; node.getparent().remove(node)
    rect(sl,0,0,13.333,.09,VIO);rect(sl,0,7.41,13.333,.09,VIO)
    tx(sl,title,.67,.65,12,.85,36,True)
    sl.notes_slide.notes_text_frame.text=note
    return sl

def spot(sl,x,y,color=ACC,r=.055):
    a=sl.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x-r),Inches(y-r),Inches(2*r),Inches(2*r))
    a.fill.solid();a.fill.fore_color.rgb=color;a.line.fill.background()

def waveline(sl,x,y,w,h,cycles=1.5,amp=.75,color=INK,width=2.1,phase=0,steps=90):
    px=None
    for i in range(steps+1):
        t=i/steps; pos=(x+w*t, y+h/2-h*amp/2*math.sin(2*math.pi*cycles*t+phase))
        if px: line(sl,px[0],px[1],pos[0],pos[1],color,width)
        px=pos

def arrow(sl,x1,y,x2,color=ACC):
    line(sl,x1,y,x2-.12,y,color,2.5)
    a=sl.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x2-.15), Inches(y-.075), Inches(.18), Inches(.15))
    a.fill.solid();a.fill.fore_color.rgb=color;a.line.fill.background()

def notes_append(index,text):
    s=p.slides[index-1]; n=s.notes_slide.notes_text_frame; n.text=n.text+'\n\n【v4演示补充】'+text

def rename_title(index, old_part, replacement):
    s=p.slides[index-1]
    for sh in s.shapes:
        if not sh.has_text_frame:continue
        if old_part in sh.text:
            # Keep the existing title run's formatting and text box geometry.
            runs=[r for pg in sh.text_frame.paragraphs for r in pg.runs]
            if runs:
                runs[0].text=replacement
                for r in runs[1:]:r.text=''
            else:sh.text=replacement
            return
    raise AssertionError(f'title not found on slide {index}: {old_part}')

# First repair a terminology error without changing its paired layout.
rename_title(23,'十个等级','这10个样本，怎样写成等长码字？')
rename_title(24,'十个等级','这10个样本，怎样写成等长码字？')
notes_append(23,'本图是10个采样时刻、8个量化等级、10组3bit码字，不是10个量化等级。让学生先标出一个样本的编号，再写成3bit。')
notes_append(24,'10个样本×3bit=30bit属于演示性定长编码。本例不是实际16bit PCM；下一页之后有模型与实际存储的桥梁。')
notes_append(5,'零线表示相对参考信号的零偏差；负值不是“负的响度”。可用手势指向零线上下两侧。')
notes_append(9,'这一幅是便于观察的极低采样率模型，不是正常录音参数。采样率是每秒每声道取样次数；它与声音信号自身的频率不是同一量。')
notes_append(17,'可播放随本版一起提交的audio-v4-assets/quantization-3bit.wav与quantization-16bit.wav。两者同样16kHz采样率、相同音源与播放电平，仅示意均匀量化宽度差异；不要据此断言16bit任何时候都可听辨地更好。')
notes_append(29,'PCM 1,411,200bit/s来自44,100样本/秒 × 16bit/样本 × 2声道。MP3示例为固定128kbit/s；比率不是MP3固有常数。')
notes_append(30,'先问：两个码率从何而来？区分PCM原始码率与压缩码率；压缩比依设置而变化。')
notes_append(41,'可播放audio-v4-assets/sampling-44100.wav与sampling-8000.wav。均由同一带高频成分的实验声源生成；8kHz版本在降低采样率之前先低通限制频率，不是直接丢弃样本。')
notes_append(46,'第43-44页为不预滤波的直接采样诊断，用来说明混叠；正常录音需在采样前抗混叠滤波。')

# Add v4 visual evidence slides. They inherit the same rail/Alibaba palette.
insertions=[]

def add_origin():
    s=base('为什么麦克风能画出一条“声音曲线”？',
    '预计1分钟。先让学生观察/预测：麦克风接收了什么变化？分三步揭示：声源振动使空气局部声压变化；麦克风把它转换成变化的电信号；屏幕固定位置绘出“电信号幅度-时间”。图不是声音沿空间蜿蜒传播的轨迹。'
    '教师追问：横轴为什么是时间？零线下方是否没有声音？')
    tx(s,'声源振动',.7,1.9,3,.5,25,True)
    tx(s,'空气的疏密变化',4.1,1.9,3.5,.5,25,True)
    tx(s,'麦克风 / 电信号',9.0,1.9,3.5,.5,25,True)
    # sound source and air pressure bars
    rect(s,1.1,3.0,.26,1.5,ACC);rect(s,1.36,3.25,.16,1.0,CYAN)
    for i in range(14):
        x=4.15+i*.22; th=.028+(.035 if i in (2,3,7,8,12,13) else 0)
        line(s,x,3.16,x,4.35,GRAY,1 if th<.04 else 3)
    rect(s,9.3,2.9,.17,1.5,ACC);rect(s,9.48,3.08,.18,1.13,CYAN)
    arrow(s,2.75,3.7,3.75);arrow(s,7.6,3.7,8.75)
    tx(s,'同一位置的信号幅度随时间变化',.75,5.25,11,.55,23,False,ACC)
    waveline(s,4.3,5.95,5,.7,cycles=2.2,amp=.85)
    line(s,4.3,6.3,9.3,6.3,GRAY,1)
    tx(s,'时间 →',9.5,6.05,2,.3,16)
    insertions.append((5,s))

def add_sampling_vs_quant():
    s=base('采样率与量化等级，究竟改变了哪一个方向？',
    '预计1.5分钟。先独立预测：提高采样率时会增加哪些点？只提高量化等级时，横向取样位置是否变化？'
    '观察两图：左图展示横向取样间隔变化；右图展示纵向候选幅度等级变密。用同一输入波形，刻意只改变一个参数。'
    '不要把高采样率直接等同于必然更高的主观音质。')
    tx(s,'① 改采样率：时间位置变密',.75,1.77,5.8,.42,24,True)
    tx(s,'② 改量化等级：幅度选择变密',7.0,1.77,5.5,.42,24,True)
    for x in (.86,7.1):
        waveline(s,x,2.7,5.18,2.2,cycles=1.35,amp=.7,color=INK)
        line(s,x,3.8,x+5.18,3.8,GRAY,.9)
    for rate,y,c in ((5,3.8,ACC),(11,4.7,CYAN)):
        # left: two aligned sample time rows under one input wave
        for i in range(rate):
            xx=.86+i*5.18/(rate-1)
            yy=3.8-2.2*.7/2*math.sin(2*math.pi*1.35*i/(rate-1))
            spot(s,xx,yy,c,.055)
    # right: same horizontal sampling times, more amplitude candidates
    for ct,c in ((4,GRAY),(8,CYAN)):
        xx=7.1 if ct==4 else 10.0
        for j in range(ct):
            yy=2.95+j*1.55/(ct-1)
            line(s,xx,yy,xx+2.15,yy,c,.9)
    tx(s,'时间（横向）',.75,5.48,5.55,.4,20,False,MUTED)
    tx(s,'幅度（纵向）',7.0,5.48,5.55,.4,20,False,MUTED)
    tx(s,'采样：何时取值；量化：用哪个有限的值表示。',.75,6.16,12,.5,22,True,ACC)
    insertions.append((9,s))

def add_quant_audio():
    s=base('同一段声音，量化等级变多以后会怎样？',
    '预计1.5分钟。教师先示范/播放audio-v4-assets/quantization-3bit.wav和quantization-16bit.wav。'
    '同一实验音源、同一采样率和时长、同一播放电平，只改均匀量化的精细程度。'
    '学生先预测，再听，观察代表值是否更靠近原始曲线。听感因声音和设备而异，不声称每个差别都一定可听见。')
    tx(s,'实验：固定采样率，只改变每个样本的量化精度。',.75,1.75,11.9,.55,22)
    waveline(s,.9,2.55,11.5,2.35,cycles=2.3,amp=.7,color=GRAY,width=2)
    line(s,.9,3.72,12.4,3.72,LIGHT,1)
    for i in range(23):
        x=.9+11.5*i/22
        yy=3.72-2.35*.7/2*math.sin(2*math.pi*2.3*i/22)
        levels=[2.95,3.46,3.98,4.49]
        yq=min(levels,key=lambda v:abs(v-yy))
        line(s,x,yy,x,yq,ACC,1)
        spot(s,x,yq,ACC,.055)
    tx(s,'灰线：原始信号     紫点：少量化等级的代表值     细线：量化误差',.9,5.20,11.8,.46,20)
    tx(s,'先预测 → 再试听 → 对照波形解释',.9,6.05,11,.5,24,True,ACC)
    insertions.append((17,s))

def add_model_bridge():
    s=base('课堂上的3 bit，与真实录音的16 bit矛盾吗？',
    '预计1分钟。学生先说：为什么前面3bit，此处又是16bit？'
    '左边是8级量化的教学玩具模型，右边是常见线性PCM存储样本示例。每样本16bit对应2B，本课不要求学生学会16bit有符号数或字节序细节。'
    '强调：量化等级和样本存储位宽相关，但不能把所有音频编码都理解为这种PCM定长存储。')
    tx(s,'课堂模型',.85,1.9,5.2,.55,26,True)
    tx(s,'实际PCM示例',7.1,1.9,5.2,.55,26,True)
    tx(s,'8级 → 3 bit / 样本',.85,2.72,5.6,.5,22,color=ACC)
    tx(s,'65,536种16 bit码型 / 样本',7.1,2.72,5.4,.6,21,color=CYAN)
    for i in range(3):
        rect(s,.85+i*.92,3.55,.87,.87,outline=ACC,width=2)
        tx(s,str([0,1,1][i]),1.16+i*.92,3.68,.3,.44,26,True)
    for i in range(16):
        rect(s,7.05+i*.32,3.55,.30,.83,outline=CYAN,width=1)
    tx(s,'3格只是在教学中方便看清编码过程',.85,4.76,5.7,.9,19,color=MUTED)
    tx(s,'16格 = 2 byte / 样本',7.05,4.76,5.5,.55,21,color=CYAN)
    tx(s,'样本存储位宽不同，不等于采样率不同。',.85,6.05,11.4,.5,23,True,ACC)
    insertions.append((26,s))

def add_playback():
    s=base('录下来的0和1，怎样再次变成声音？',
    '预计1分钟。先预测：计算机读到010、111等码字后，扬声器会直接发出0和1吗？'
    '逐步解释：解码得到样本数值；数字模拟转换及输出滤波产生连续变化的电信号；扬声器将信号变化转成声音。'
    '不要把连接样本的折线或阶梯图当成实际模拟重建波形；还原并非必然完全等于原输入。')
    labels=[('PCM数值','一组数字样本'),('解码 / DAC','转成输出信号'),('输出滤波','连续变化的信号'),('扬声器','重新听到声音')]
    for i,(a,b) in enumerate(labels):
        x=.78+i*3.13
        rect(s,x,2.35,2.60,1.55,outline=ACC,width=2)
        tx(s,a,x+.10,2.67,2.37,.52,23,True,ACC,PP_ALIGN.CENTER)
        tx(s,b,x+.10,3.26,2.37,.42,16,color=MUTED,align=PP_ALIGN.CENTER)
        if i<3:arrow(s,x+2.63,3.14,x+3.0)
    tx(s,'数字码字',.87,4.70,2.4,.36,20)
    tx(s,'010  111  011',.87,5.15,3.0,.48,22,True)
    waveline(s,7.42,4.76,4.35,1.06,cycles=2,amp=.75,color=INK)
    tx(s,'播放波形不是把样本点机械地连成折线。',.87,6.23,11.6,.44,22,True,ACC)
    insertions.append((26,s))

def add_alias_path():
    s=base('为何“直接取样”与“正常录音”要分开讨论？',
    '预计1分钟。联系前面6kHz输入、8kHz取样得到2kHz混叠的诊断例。'
    '上排是不带抗混叠滤波的直接取样，可能无法区分6kHz和2kHz信号。'
    '下排是正常流程：先滤掉超过可保留范围的高频，再采样。此时6kHz成分被抑制，并非神奇地变成保真录音。'
    '学生说出：为什么必须先限制最高信号频率？')
    tx(s,'诊断实验：不预滤波',.8,1.84,10,.5,25,True)
    for i,(lab,xx) in enumerate([('6 kHz输入',.8),('8 kHz直接取样',5.10),('可能混叠',9.72)]):
        rect(s,xx,2.55,2.66,.80,outline=ACC,width=1.5)
        tx(s,lab,xx+.07,2.75,2.52,.45,19,True,ACC,PP_ALIGN.CENTER)
    arrow(s,3.52,2.96,4.77);arrow(s,7.85,2.96,9.44)
    line(s,.8,3.89,12.43,3.89,LIGHT,1)
    tx(s,'正常录音：先限制频率',.8,4.16,10,.5,25,True)
    for lab,xx in [('6 kHz输入',.8),('低通滤波',4.16),('8 kHz采样',7.49),('抑制该高频',10.58)]:
        rect(s,xx,4.92,2.25,.84,outline=CYAN,width=1.5)
        tx(s,lab,xx+.04,5.16,2.15,.40,17,True,CYAN,PP_ALIGN.CENTER)
    arrow(s,3.11,5.35,4.0,color=CYAN);arrow(s,6.5,5.35,7.32,color=CYAN);arrow(s,9.85,5.35,10.42,color=CYAN)
    tx(s,'8 kHz采样时，理想可保留频率范围低于4 kHz。',.80,6.30,12,.48,21,True,ACC)
    insertions.append((44,s))

add_origin();add_sampling_vs_quant();add_quant_audio();add_model_bridge();add_playback();add_alias_path()

# Change logical slide order without copying/removing slide relationships. The list itself owns the display order.
# Capture the original 54 slide id nodes before adding new slides; insertion positions are original v3 page numbers.
ids=list(p.slides._sldIdLst)
orig=ids[:54]; new=ids[54:]
assert len(new)==len(insertions)==6
ordered=[]
for idx,node in enumerate(orig,1):
    ordered.append(node)
    ordered += [new[j] for j,(after,_) in enumerate(insertions) if after==idx]
root=p.slides._sldIdLst
for el in list(root):root.remove(el)
for el in ordered:root.append(el)

# Four reproducible, safe-volume demonstration assets. Using standard library only.
def create_wave(path,sr,seconds,levels=None,lowpass=False):
    n=int(sr*seconds); data=[]
    for i in range(n):
        t=i/sr
        # controlled synthesized source with low harmonics and a quieter high-frequency component
        v=(.48*math.sin(2*math.pi*440*t)+.21*math.sin(2*math.pi*880*t))
        if not lowpass: v+=.16*math.sin(2*math.pi*5600*t)
        # fade in/out to avoid a click
        v*=min(1.,t/.045,(seconds-t)/.045)
        v=max(-.94,min(.94,v))
        if levels:
            step=2/levels
            index=max(0,min(levels-1,int((v+1)/step)))
            v=-1+(index+.5)*step
        data.append(int(v*32767))
    path.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr)
        f.writeframes(struct.pack('<'+'h'*n,*data))

# identical experiment source frequencies; lower-rate version has high component removed pre-sampling.
create_wave(ASSET/'sampling-44100.wav',44100,2.0,lowpass=False)
create_wave(ASSET/'sampling-8000.wav',8000,2.0,lowpass=True)
create_wave(ASSET/'quantization-3bit.wav',16000,2.0,levels=8,lowpass=True)
create_wave(ASSET/'quantization-16bit.wav',16000,2.0,levels=None,lowpass=True)

OUT.parent.mkdir(parents=True,exist_ok=True)
p.save(OUT)
check=Presentation(OUT)
assert len(check.slides)==60
assert all(sl.notes_slide.notes_text_frame.text.strip() for sl in check.slides), 'Missing speaker notes'
assert '这10个样本' in '\n'.join(s.text for s in check.slides[26].shapes if s.has_text_frame) # old 23 + 4 inserts
print('V4_DONE',OUT,OUT.stat().st_size,'pages',len(check.slides),'notes',60,'assets',len(list(ASSET.glob('*.wav'))))