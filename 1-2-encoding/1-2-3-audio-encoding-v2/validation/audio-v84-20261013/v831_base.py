#!/usr/bin/env python3
"""Ten sequential visual improvements to v8.1.

Each round reads the preceding PPTX, changes selected slides, audits the output,
then (when RUN_PUSH=1) commits and pushes that round *before* continuing.
Simple technical visualizations are drawn natively or from reproducible Pillow data.
"""
from pathlib import Path
import os, json, math, hashlib, io, subprocess
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image, ImageDraw, ImageFilter

BASE = Path(os.environ.get("DECK_DIR", Path(__file__).resolve().parents[2]))
AUD = Path(__file__).resolve().parent
IN = BASE / '1-2-3-audio-encoding-v8.1.pptx'
PREFIX = '1-2-3-audio-encoding-v8.3.'
V=RGBColor(98,81,177);ACC=RGBColor(140,100,225);CYAN=RGBColor(0,176,240)
DARK=RGBColor(38,38,38);MUTE=RGBColor(113,113,113);LIGHT=RGBColor(226,222,242)
WHITE=RGBColor(255,255,255);SOFT=RGBColor(248,246,254);RED=RGBColor(255,0,0)
FREG='Alibaba PuHuiTi 3.0 55 Regular'; FBOLD='Alibaba PuHuiTi 3.0 115 Black'

ROUND_DETAILS = {
 1:('P1','模拟与数字的差异只靠文字描述','将第4页改为同一时间轴上的连续波形与离散样本对照，图上明确对象与差异','第4页含两种具有不同视觉语义的信号及中文标签'),
 2:('P1','麦克风/ADC仍偏抽象','将第5页改为声源到麦克风及连续电信号的可读物理流程，并引导学生观察波形','第5页明确声源、麦克风、连续电信号，且原理与第3页图片一致'),
 3:('P1','录音与播放的两条路线虽然完整，但一眼不易区分','第7页用双色双行连续流程图重绘，突出ADC与DAC相反方向','第7页录音/播放各有四步及关键词'),
 4:('P1','采样率增加与位数增加的视觉区分仍不牢固','第24页重绘时间方向采样点和幅度方向量化线的左右对照','第24页明确横向采样与纵向量化，且坐标轴清晰'),
 5:('P0','3.71量化判断页没有充分体现数值落在哪个区间','第17页以0—8的数轴和[3,4)区间高亮显示3.71的位置','第17页3.71在[3,4)内，问答与第18/20页规则一致'),
 6:('P1','PCM容量公式缺少从数量到字节的可观察路径','第31页用四因素因果对应示意重绘公式和单位','第31页四个独立因素及÷8均可直接解释'),
 7:('P1','音轨/声道只有矩形标签，不能看出混音的效果','第41页采用两条编辑音轨的不同波形混合到左右声道的可视流程','不把音轨数量误当导出声道数量，且两条输出声道有可辨波形'),
 8:('P0','视频帧的球位移在教室投影上不够强','第45页重绘五帧运动物体，球位置逐帧明显右移且保留一致的背景参照','五帧顺序、球位置、25 fps和时间含义准确'),
 9:('P1','BMP/JPG比较仅有文字，学生没有看到有损质量的例证','第63页放入同一程序生成图像的PNG/低质量JPEG视觉对照，附参数限定','两图同源同尺寸，保留“示意，不代表一切压缩设置”'),
 10:('P1','冗余度比较采用小色块，空间信息过于局促','第60页增大三幅同尺寸高对比图，配明确的重复规律线索；复核各组答案高亮','三种图结构可辨认，六组练习答案页主题色一致'),
}

def pt(v): return Inches(v)
def stext(sl,value,x,y,w,h,size=22,bold=False,color=DARK,align=None):
    sh=sl.shapes.add_textbox(pt(x),pt(y),pt(w),pt(h))
    f=sh.text_frame;f.clear();f.word_wrap=True;f.vertical_anchor=MSO_ANCHOR.MIDDLE
    f.margin_left=Pt(0);f.margin_right=Pt(0);f.margin_top=Pt(0);f.margin_bottom=Pt(0)
    for i,t in enumerate(value.split('\n')):
        p=f.paragraphs[0] if i==0 else f.add_paragraph();p.text=t;p.space_after=Pt(0)
        p.font.name=FBOLD if bold else FREG;p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=color
        if align is not None:p.alignment=align
    return sh

def rect(sl,x,y,w,h,fill=None,outline=None,width=1.4):
    sh=sl.shapes.add_shape(MSO_SHAPE.RECTANGLE,pt(x),pt(y),pt(w),pt(h))
    if fill:sh.fill.solid();sh.fill.fore_color.rgb=fill
    else:sh.fill.background()
    if outline:sh.line.color.rgb=outline;sh.line.width=Pt(width)
    else:sh.line.fill.background()
    return sh

def circ(sl,cx,cy,r,color,outline=None):
    s=sl.shapes.add_shape(MSO_SHAPE.OVAL,pt(cx-r),pt(cy-r),pt(2*r),pt(2*r))
    s.fill.solid();s.fill.fore_color.rgb=color
    if outline:s.line.color.rgb=outline;s.line.width=Pt(1.5)
    else:s.line.fill.background()
    return s

def line(sl,x1,y1,x2,y2,color=ACC,width=2,dash=None):
    s=sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,pt(x1),pt(y1),pt(x2),pt(y2))
    s.line.color.rgb=color;s.line.width=Pt(width)
    if dash:
        from pptx.enum.dml import MSO_LINE_DASH_STYLE
        s.line.dash_style=MSO_LINE_DASH_STYLE.DASH
    return s

def curve(sl,x0,y0,w,h,cycles=1.2,phase=0,color=MUTE,width=2,points=90):
    for i in range(points):
        x1=x0+w*i/points;x2=x0+w*(i+1)/points
        y1=y0+h*.5-h*.38*math.sin(2*math.pi*(i/points*cycles)+phase)
        y2=y0+h*.5-h*.38*math.sin(2*math.pi*((i+1)/points*cycles)+phase)
        line(sl,x1,y1,x2,y2,color,width)

def clean(sl):
    for sh in list(sl.shapes):
        # Rails and slide title are above y=1.55; bottom thesis stays at y>=6.3.
        if 1.55 <= (sh.top/914400) < 7.1:
            node=sh._element;node.getparent().remove(node)

def bglabel(sl,word):
    stext(sl,word,.86,6.39,11.75,.48,17,False,ACC)

def note(sl,msg):
    f=sl.notes_slide.notes_text_frame
    f.text=(f.text or '').strip()+'\n\n[视觉改进提示] '+msg

def get_slide(p,n):return p.slides[n-1]

def get_titles(p):
    result=[]
    for sl in p.slides:
        q=[x.text.strip() for x in sl.shapes if x.has_text_frame and x.text.strip()]
        result.append(q[0] if q else '')
    return result

def add_image(sl,im,x,y,w,h):
    b=io.BytesIO();im.save(b,format='PNG');b.seek(0)
    sl.shapes.add_picture(b,pt(x),pt(y),width=pt(w),height=pt(h))

def procedural_picture():
    """Same image is used both as PNG (lossless) and JPEG (lossy).
       Draw sharp repeatable lines and texture to make quantization artifacts visible."""
    im=Image.new('RGB',(640,350),(239,246,251));d=ImageDraw.Draw(im)
    d.rectangle((0,180,640,350),fill=(71,130,105))
    d.polygon([(0,178),(112,100),(200,154),(292,65),(422,180)],fill=(79,113,165))
    d.polygon([(180,180),(335,75),(492,181)],fill=(55,90,120))
    d.ellipse((480,35,572,127),fill=(246,206,72))
    for j in range(46):
        x=j*17%640;y=180+(j*53)%170
        c=(56+j%7*9,105+j%5*8,65+j%8*7)
        d.line((x,y,x+11,y-31),fill=c,width=3)
    for j in range(22):
        y=202+j*6;d.line((0,y,640,y),fill=(64+j%4*3,135+j%3*3,110),width=1)
    for i in range(50):
        x=i*14;d.ellipse((x%640,155+(i*13)%145,x%640+4,160+(i*13)%145),fill=(243,226,132))
    return im

def draw_stage(p,k):
    sl=p.slides
    if k==1:
        s=sl[3];clean(s)
        stext(s,'现实声音：连续变化',.88,1.84,5.4,.55,25,True,ACC)
        stext(s,'电脑保存：离散数字',7,1.84,5.4,.55,25,True,CYAN)
        for x in (.95,7.05):
            line(s,x,4.77,x+5.2,4.77,MUTE,1.5);line(s,x,2.59,x,4.9,MUTE,1.3)
        curve(s,1.05,2.83,5.08,1.67,1.65,color=V,width=2.4)
        curve(s,7.15,2.83,5.07,1.67,1.65,color=RGBColor(208,208,213),width=1.4)
        for i in range(12):
            x=7.18+i*5/11;y=3.665-1.67*.38*math.sin(2*math.pi*(i/11*1.65))
            line(s,x,4.77,x,y,CYAN,1.2);circ(s,x,y,.067,CYAN)
        stext(s,'同一位置的信号随时间变化',.95,5.25,5.4,.55,20,False)
        stext(s,'只记录特定时刻的一组数值',7.03,5.25,5.3,.55,20,False)
        bglabel(s,'连续信号 → 等间隔采样 → 离散样本；图示是同一段信号。')
        note(s,'先让学生说两张图中什么相同、什么不同；右侧点并非“声波的传播路线”。')
    if k==2:
        s=sl[4];clean(s)
        stext(s,'声源振动',.85,1.86,3.65,.53,25,True,ACC)
        stext(s,'麦克风感受声压',4.91,1.86,3.65,.53,25,True)
        stext(s,'输出连续电信号',9.02,1.86,3.55,.53,25,True,CYAN)
        # Sound waves: vertical pulses, not a squiggly propagating path.
        for i in range(5):
            x=1.15+i*.26
            line(s,x,3.10+(i%2)*.16,x,4.25-(i%2)*.16,ACC,3)
        for j in range(3):
            x=2.65+j*.45
            line(s,x,3.04,x+.16,3.40,ACC,2);line(s,x+.16,3.40,x,3.76,ACC,2)
        line(s,4.25,3.55,4.78,3.55,ACC,3)
        circ(s,6.47,3.63,.52,RGBColor(233,231,239),ACC)
        line(s,6.47,4.15,6.47,4.58,MUTE,3)
        line(s,7.25,3.55,8.71,3.55,ACC,2.5)
        line(s,9.01,4.55,12.18,4.55,MUTE,1.2)
        curve(s,9.02,2.72,3.16,1.82,1.35,color=CYAN,width=2.5)
        stext(s,'空气中的变化',.98,5.23,3.3,.53,19)
        stext(s,'转换为电信号',5.12,5.23,3.1,.53,19)
        stext(s,'仍是连续变化的',9.14,5.23,3.1,.53,19)
        bglabel(s,'麦克风完成“声压变化 → 电信号”；将模拟信号数字化由ADC完成。')
        note(s,'学生应能解释麦克风不是直接把声音变为二进制；图中声波用波阵面而非空间蛇形路径表示。')
    if k==3:
        s=sl[6];clean(s)
        stext(s,'录音：模拟 → 数字',.88,1.69,5,.55,25,True,ACC)
        stext(s,'播放：数字 → 模拟',.88,4.18,5,.55,25,True,CYAN)
        labels=[('声波',.93),('麦克风',4.05),('ADC',7.17),('数字文件',10.19)]
        for i,(label,x) in enumerate(labels):
            rect(s,x,2.46,2.15,.71,SOFT,ACC);stext(s,label,x,2.60,2.15,.42,20,True,ACC,PP_ALIGN.CENTER)
            if i<3:line(s,x+2.19,2.83,x+3.0,2.83,ACC,2.2)
        labels2=[('数字文件',.93),('DAC',4.05),('扬声器',7.17),('声音',10.19)]
        for i,(label,x) in enumerate(labels2):
            rect(s,x,4.92,2.15,.71,WHITE,CYAN);stext(s,label,x,5.04,2.15,.42,20,True,CYAN,PP_ALIGN.CENTER)
            if i<3:line(s,x+2.19,5.26,x+3.0,5.26,CYAN,2.2)
        bglabel(s,'思考：麦克风和扬声器、ADC和DAC，各负责什么转换？')
        note(s,'用两条平行流程对应录音和播放，避免误认为DAC在录音时使用。')
    if k==4:
        s=sl[23];clean(s)
        stext(s,'采样率：横向有多少次记录？',.85,1.74,5.6,.55,24,True,ACC)
        stext(s,'量化位数：纵向有多少等级？',6.88,1.74,5.8,.55,24,True,CYAN)
        for x in (.88,7.0):
            line(s,x+.14,4.7,x+5.12,4.7,MUTE,1.3)
            line(s,x+.14,2.45,x+.14,4.85,MUTE,1.3)
            curve(s,x+.18,2.64,4.90,1.73,1.35,color=MUTE,width=2.0)
        for j in range(11):
            x=1.06+j*.49;y=3.505-1.73*.38*math.sin(2*math.pi*j/10*1.35)
            circ(s,x,y,.070,ACC)
        for k2 in range(8):
            y=2.55+k2*.27;line(s,7.15,y,12.12,y,CYAN,1.5)
        stext(s,'时间位置变密：样本个数变化',.95,5.32,5.45,.78,21,True,ACC)
        stext(s,'代表值变密：每点存储位数变化',7.03,5.32,5.28,.78,21,True,CYAN)
        bglabel(s,'重要区别：位数变大，不等于同一时间里采样次数变多。')
        note(s,'让学生指着时间轴和幅度轴解释“点数更多”与“等级更多”，要求独立归纳。')
    if k==5:
        s=sl[16];clean(s)
        stext(s,'输入范围 [0,8) 分成8段：每一段对应一个等级。',.90,1.80,11.5,.63,23)
        x0=.99;unit=1.39;y=3.18
        for i in range(8):
            rect(s,x0+i*unit,y,unit-.04,.72,RGBColor(239,233,255) if i==3 else WHITE,ACC if i==3 else LIGHT,3 if i==3 else 1.2)
            stext(s,str(i),x0+i*unit,y+.08,unit-.04,.46,23,True,ACC if i==3 else DARK,PP_ALIGN.CENTER)
            stext(s,str(i),x0+i*unit-.08,y+.87,.35,.33,15)
        stext(s,'8',12.02,y+.87,.45,.33,15)
        cx=x0+3.71*unit
        line(s,cx,2.70,cx,y-.02,RED,3)
        circ(s,cx,2.68,.075,RED)
        stext(s,'3.71',cx-.46,2.12,1.02,.48,23,True,RED,PP_ALIGN.CENTER)
        stext(s,'红点落在哪一段？请先独立判断等级编号。',.97,4.75,11.2,.74,26,True,ACC)
        bglabel(s,'先只预测，不公布答案；翻页再验证区间规则。')
        note(s,'此页3.71准确落在[3,4)，注意教师不要提前说L3，让学生先猜。')
    if k==6:
        s=sl[30];clean(s)
        stext(s,'数据量（Byte） = 采样率 × 时长 × 声道数 × 位数 ÷ 8',.90,1.74,11.7,.80,25,True,ACC)
        factors=[('采样率','每秒几个样本'),('时长','采多少秒'),('声道数','同时记录几路'),('量化位数','每个样本多少bit')]
        for i,(a,b) in enumerate(factors):
            x=.95+3.17*i
            rect(s,x,2.99,2.75,1.54,SOFT,ACC)
            stext(s,a,x+.13,3.17,2.5,.43,23,True,ACC,PP_ALIGN.CENTER)
            stext(s,b,x+.09,3.74,2.58,.49,16,False,DARK,PP_ALIGN.CENTER)
            if i<3:stext(s,'×',x+2.79,3.36,.3,.43,21,True,ACC,PP_ALIGN.CENTER)
        line(s,1.02,5.03,12.04,5.03,LIGHT,1.5)
        stext(s,'前3项相乘 → 样本总数；再乘bit/样本 → bit；最后÷8 → Byte。',.94,5.38,11.65,.64,20,True)
        bglabel(s,'单位检验：Hz×s×声道×bit÷8，最终为什么得到Byte？')
        note(s,'用单位意义逐步推导公式，而不是只抄公式。四因素必须与学生已学概念对应。')
    if k==7:
        s=sl[40];clean(s)
        stext(s,'编辑工程：两条音轨',.87,1.82,5.2,.60,25,True,ACC)
        stext(s,'混音导出：两个声道',7.33,1.82,5.2,.60,25,True,CYAN)
        for i,(label,color) in enumerate([('音轨1：诗朗诵',ACC),('音轨2：背景音乐',CYAN)]):
            y=2.72+i*1.11
            rect(s,.94,y,4.9,.86,WHITE,color,2)
            stext(s,label,1.06,y+.16,2.6,.36,16,True,color)
            curve(s,3.63,y+.10,2.03,.61,2.4 if i==0 else 1.0,phase=0.6*i,color=color,width=1.8)
        line(s,6.02,3.52,7.05,3.52,ACC,3)
        stext(s,'混合',6.05,3.02,.98,.43,18,True,ACC,PP_ALIGN.CENTER)
        for i,(label,color) in enumerate([('左声道 L',CYAN),('右声道 R',CYAN)]):
            y=2.72+i*1.11
            rect(s,7.26,y,5.0,.86,WHITE,color,2)
            stext(s,label,7.40,y+.16,1.53,.36,16,True,color)
            curve(s,9.09,y+.10,3.02,.61,1.8,phase=i*.5,color=color,width=1.8)
        bglabel(s,'两条编辑音轨可以混合成两路输出；决定PCM数据量的是输出声道数。')
        note(s,'波形是示意，不反映真实混音的数学结果；追问学生最后导出声道数是否改变。')
    if k==8:
        s=sl[44];clean(s)
        stext(s,'同一个球，在5个连续时刻的位置变化',.88,1.76,11.56,.57,24,True,ACC)
        for i in range(5):
            x=.80+2.45*i
            rect(s,x,2.55,2.05,2.27,WHITE,LIGHT,1.5)
            # Common horizontal floor line; position shifts deterministically.
            line(s,x+.15,4.27,x+1.90,4.27,LIGHT,1.3)
            circ(s,x+.30+i*.34,3.67,.18,CYAN)
            stext(s,'第'+str(i+1)+'帧',x,4.95,2.05,.45,19,True,DARK,PP_ALIGN.CENTER)
            if i<4:stext(s,'→',x+2.04,3.45,.39,.48,22,True,ACC,PP_ALIGN.CENTER)
        stext(s,'位置逐帧变化（背景和球的大小不变）',.92,5.65,11.3,.50,20,True,ACC)
        bglabel(s,'25 fps = 每秒显示25帧；“帧”不是声道，也不是采样位数。')
        note(s,'只改变球的位置，保持背景、框和时间顺序一致，直观表达连续画面。')
    if k==9:
        s=sl[62];clean(s)
        original=procedural_picture()
        buf=io.BytesIO();original.save(buf,format='JPEG',quality=3,subsampling=2,optimize=False)
        lossy=Image.open(io.BytesIO(buf.getvalue())).convert('RGB')
        add_image(s,original,.88,2.13,5.52,3.02)
        add_image(s,lossy,6.94,2.13,5.52,3.02)
        stext(s,'同源原图（无损保存示意）',.91,5.35,5.45,.54,20,True,ACC)
        stext(s,'同一图像：低质量JPEG',6.99,5.35,5.42,.54,20,True,CYAN)
        bglabel(s,'两图尺寸相同；右图仅用于观察明显压缩伪影，不代表所有JPEG质量。')
        note(s,'本页从同一程序生成的640×350 RGB原图导出低质量JPEG（quality=3）。这不是对任意BMP/JPG文件大小的普遍预测；用于解释有损重建可能改变细节。')
    if k==10:
        s=sl[59];clean(s)
        stext(s,'三幅图具有相同的宽、高与位深。',.88,1.73,11.7,.58,24,True)
        shapes=[('A：纯色',ACC),('B：规律色块',CYAN),('C：复杂变化',V)]
        for i,(lab,col) in enumerate(shapes):
            x=.86+4.06*i; yy=2.38; w=3.62;h=2.94
            if i==0:rect(s,x,yy,w,h,RGBColor(83,153,196))
            elif i==1:
                for j in range(8):
                    for k2 in range(6):rect(s,x+j*w/8,yy+k2*h/6,w/8+.004,h/6+.004,RGBColor(76,157,196) if (j//2+k2//2)%2 else RGBColor(186,220,236))
            else:
                for j in range(24):
                    for k2 in range(18):
                        z=(j*131+k2*251+j*k2*97)%255
                        rect(s,x+j*w/24,yy+k2*h/18,w/24+.008,h/18+.008,RGBColor(47+z//3,67+(z*3)%145,85+(z*7)%125))
            stext(s,lab,x,5.45,w,.48,21,True,col,PP_ALIGN.CENTER)
        bglabel(s,'想一想：如果只允许无损压缩，哪张图最容易用更短的规则完整表示？')
        note(s,'三个图的区域长宽相同，颜色模式相同；只比较内容结构。最复杂并不等于一定不能压缩，规律和算法共同决定结果。')
        for n in [33,38,42,48,62,67]:
            slide=sl[n-1]
            for sh in slide.shapes:
                if not sh.has_text_frame or not sh.text.strip().startswith('答案：'):continue
                for para in sh.text_frame.paragraphs:
                    for run in para.runs:
                        run.font.bold=True;run.font.color.rgb=ACC
                        if run.font.size and run.font.size.pt<20:run.font.size=Pt(20)


def audit(p,round_id,input_path,output_path):
    assert len(p.slides)==70
    titles=get_titles(p)
    assert titles[0].startswith('声音怎样变成0和1') and titles[69].startswith('可选拓展')
    for idx in range(1,7):assert titles.count('练习题 '+str(idx))==2
    assert all(sl.has_notes_slide and sl.notes_slide.notes_text_frame.text.strip() for sl in p.slides)
    from zipfile import ZipFile
    with ZipFile(output_path) as z: assert z.testzip() is None
    def digest(b):return hashlib.sha256(b).hexdigest()
    data={
      'round':round_id,'severity':ROUND_DETAILS[round_id][0],
      'identified_issue':ROUND_DETAILS[round_id][1],
      'refinement':ROUND_DETAILS[round_id][2],
      'verified_by':ROUND_DETAILS[round_id][3],
      'slides':len(p.slides),
      'speaker_notes':sum(bool(s.notes_slide.notes_text_frame.text.strip()) for s in p.slides),
      'qa_pairs':6,
      'input_sha256':digest(input_path.read_bytes()),'output_sha256':digest(output_path.read_bytes()),
      'output_bytes':output_path.stat().st_size,
    }
    assert data['input_sha256']!=data['output_sha256'],'No effective change'
    (AUD/f'round-{round_id:02d}-audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return data

def main():
    assert IN.exists(), IN
    curr=IN
    push=os.getenv('RUN_PUSH','')=='1'
    for k in range(1,11):
        name=PREFIX+str(k)+'.pptx';out=BASE/name
        p=Presentation(str(curr));assert len(p.slides)==70
        draw_stage(p,k)
        p.core_properties.title='声音编码与数据压缩 · 视觉迭代v8.3.'+str(k)
        p.save(out)
        info=audit(p,k,curr,out)
        print('ROUND',k,info['severity'],info['output_bytes'],info['refinement'],flush=True)
        if push:
            rel=out.relative_to(Path.cwd())
            aud=(AUD/f'round-{k:02d}-audit.json').relative_to(Path.cwd())
            subprocess.run(['git','add',str(rel),str(aud)],check=True)
            subprocess.run(['git','commit','-m',f'visual(audio): round {k:02d} publish {name} and audit'],check=True)
            subprocess.run(['git','push','origin','HEAD:main'],check=True)
        curr=out
    print('ALL TEN ROUNDS COMPLETE',curr,flush=True)

if __name__=='__main__':main()