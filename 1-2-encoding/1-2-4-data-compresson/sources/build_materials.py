"""Generate aligned notebook views, editable worksheets and printable PDF.

Run with Python containing Pillow/reportlab. Sources and finished materials stay
in the lesson directory. Never execute this script against another lesson.
"""
from pathlib import Path
import json
import shutil
import sys
import html

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "demos"))
import compression_lab as lab

QUESTIONS = [
    "文件变小，是不是删掉了内容？", "连续重复的颜色，怎样少写一些？",
    "少写以后，怎样证明一个也没丢？", "同一规则，为什么有时反而变大？",
    "相邻值不相同，还能利用它们的关系吗？", "只留近似值，还能找回原数吗？",
    "看起来差不多，能否叫无损？", "同一种误差，哪些任务能接受？",
    "看扩展名，就能判定压缩方式吗？", "怎样在大小限制和信息要求之间选方案？"]

SETUP = '''from pathlib import Path
import sys
from IPython.display import display, Image, HTML
here = Path.cwd().resolve()
candidates = [here, here / "1-2-encoding/1-2-4-data-compresson", *here.parents]
ROOT = next((p for p in candidates if (p / "demos/compression_lab.py").is_file()), None)
if ROOT is None:
    raise FileNotFoundError("请将整个课程文件夹复制到本机，并从该文件夹打开Notebook")
sys.path.insert(0, str(ROOT / "demos"))
from compression_lab import (COLORS, ALTERNATING, GRAY, rle_encode, rle_decode,
    named_runs, opening, predictive, approximate, image_evidence, save_jpeg_trial,
    video_changes, show_comparison_pair)
def show(name, width=384):
    display(Image(filename=str(ROOT / "assets/evidence" / name), width=width))
print("准备完成。按教师指令逐格运行，先写预测。")'''

DEMOS = [
 (1, "D1", "图中有哪些内容可能变化？写下你想检查的对象。", [
    ("先运行：原图与数据量。", 'show("opening-original.png", 256)\nopening(reveal=False)'),
    ("收到预测后：只显示读回图，暂不检验精确相等。", 'show("opening-restored.png", 256)')],
    "4096B→本机实际输出（随包为38B）。本阶段只观察外观，opening(True)留到Q3。不要把两PNG文件大小当颜色数据量。"),
 (2, "D2", "发送者看私有颜色卡。记录规则、短消息、接收者还原结果；比较后再运行。", [
    ("活动后运行编码。", 'encoded = rle_encode(COLORS)\nprint(named_runs(encoded))\nprint("编码的bytes：", list(encoded))'),
    ("先预测还原，再运行。", 'restored = rle_decode(encoded)\nprint("颜色顺序：", [int(v) for v in restored])')],
    "共享例红8绿5蓝3，payload 16B→6B。编号与次数各1B，双方预先共享规则。私有原串只给发送者，避免凭记忆还原。"),
 (3, "D1", "提出一个精确检验方法。应比较哪两个对象？", [
    ("核对方法后运行。", 'print("RLE读回与输入一致：", rle_decode(rle_encode(COLORS)) == COLORS)\nopening(reveal=True)')],
    "4096B读回与输入逐byte一致。不能比较压缩bytes和原bytes，也不能仅看长度或外观。此时揭示无损定义。"),
 (4, "D2", "两串都是16B；相同连续段规则，哪串更省？先数段，再运行。", [
    ("运行两组比较。", 'for name, data in [("连续段", COLORS), ("红绿交替", ALTERNATING)]:\n    result = rle_encode(data)\n    print(name, "输入", len(data), "B；编码", len(result), "B；读回一致", rle_decode(result) == data)')],
    "16B→6B与16B→32B均能准确还原。无损不保证所有输入变小。不要把交替串改成红8绿8。"),
 (5, "D3", "原值120,121,122,121,120,120,121,122。先提规则，再填A2差值、读回末三项。", [
    ("完成表后运行。", 'values = list(GRAY)\npredictive(values)'),
    ("可选：学生提议出现大差值时，先预测能否使用本码表。", 'try:\n    print(predictive([120, 150]))\nexcept ValueError as error:\n    print(error)')],
    "起点8bit＋7×2bit=22bit，装3B补2bit。−1=00，0=01，+1=10。长度、模式、码表未计入。差值没有少项；大差值拒绝，不能推广任意图像。"),
 (6, "D4", "归最近的4的倍数，中点向上、上限252。写两个能恢复为120的原数。", [
    ("完成A2近似表后运行。", 'approximate(GRAY)'),
    ("先将你想到的两个原数填入列表，再检验。", 'candidate_values = []  # 填你想到的两个原数\nif len(candidate_values) == 2:\n    display(approximate(candidate_values))\nelse:\n    print("先填两个原数，再运行检验。")')],
    "120与121同归120。8×6=48bit=6B，还原120,120,124,120,120,120,120,124。此模型不是JPEG，不与初次采样量化混同。"),
 (7, "D5", "先比较中性A/B，再写：看不出变化足以证明数据相同吗？", [
    ("只看图，先收判断。", 'show_comparison_pair()'),
    ("收判断后运行像素与文件大小检验。", 'image_evidence()'),
    ("同坐标放大比较。", 'print("A：同坐标放大")\nshow("crop-source.png", 768)\nprint("B：同坐标放大")\nshow("crop-quality80.png", 768)'),
    ("可选低质量对照；核心课赶时间时跳过。", 'show("crop-quality20.png", 768)'),
    ("可选：改quality并实测，只保存到demos/scratch。", 'save_jpeg_trial(quality=80)')],
    "同一源RGB，384×216。PNG4441B/像素一致；JPEGq80 10766B/28917像素变；q20 6752B/66885像素变。未压缩RGB248832B另列，不是PNG文件大小。quality范围是本库参数，不是通用质量百分比。只认主任务是否仍可获取。"),
]

def cell(kind, source):
    result = {"cell_type": kind, "metadata": {}, "source": source.splitlines(keepends=True)}
    if kind == "code": result.update(execution_count=None, outputs=[])
    return result

def notebooks():
    for role in ("teacher", "student"):
        title = "教师演示" if role == "teacher" else "学生观察与记录"
        cells = [cell("markdown", f"# 数据压缩入门：{title}\n\n45分钟核心课。先预测，再按教师指令运行当前单元。不要提前运行全部单元。\n\n需求：Python 3.10+、JupyterLab、Pillow；IPython由Jupyter提供。离线可运行，不需要widgets。整个课程目录一起复制。")]
        if role == "teacher": cells.append(cell("markdown", "教师控制：Q1隐藏精确比较，Q3才揭示；A1私有颜色卡只给发送者。Q5先收方案，再给A2。第40分钟进入Q10。失败20秒用PPTX静态页。课前清空全部输出。"))
        cells.append(cell("code", SETUP))
        for q, demo, prompt, steps, note in DEMOS:
            cells.append(cell("markdown", f"## Q{q} {QUESTIONS[q-1]} · {demo}\n\n{prompt}\n\n预测／观察：________________\n\n证据／判断：________________"))
            if role == "teacher": cells.append(cell("markdown", "**教师备课与预期结果**\n\n" + note))
            for instruction, code in steps:
                cells.extend([cell("markdown", instruction), cell("code", code)])
        for q in (8,9,10):
            if q == 8: prompt="A3：通知少了日期，程序少了等号（输入60），照片为清楚的浏览副本。逐项判断并写理由。"
            elif q == 9: prompt="依据PNG像素检验与TIFF配置卡，改正‘所有图片压缩都有损’。JPG、TIF、MP3、MPEG分别要补什么条件？"
            else: prompt="A3题目给定结果：限额100KiB；程序A80KiB/完整恢复、B50KiB/删改；照片A110KiB/像素一致、B70KiB/主题清楚。两项任务分别选择，并检查大小与信息要求。"
            cells.append(cell("markdown",f"## Q{q} {QUESTIONS[q-1]}\n\n{prompt}\n\n判断与理由：________________"))
            if role == "teacher": cells.append(cell("markdown", {
                8:"教师结论：通知／源程序本体必须无损；照片题给浏览副本可有损，但换读小字或测量要重评。",
                9:"教师结论：常见JPG照片通常有损；TIF看编码；MP3常见有损音频；MPEG是相关标准组，常见视频编码有损。PNG是图片无损反例。",
                10:"教师结论：程序选A，照片选B。先收40秒出口，课后核对：解压结果vs原输入；外观相似不证明原值一致。"}[q]))
        cells.append(cell("markdown", "## 出口检查\n\n无损判断要比较________与________。\n\n照片看不出变化仍可能有损，因为________。"))
        if role == "teacher":
            cells.extend([cell("markdown", "## 第二课时可选：帧间变化\n\n先预测：保存帧一之后，帧二要更新哪些格？一个2×2块右移一格。不是只保存新位置；旧位置还要清除。此模型不是完整MPEG码流。"), cell("code", "video_changes()")])
            cells.append(cell("markdown", "## D6音频拓展的实施边界\n\n核心45分钟不做音频试听。本包未提供经统一增益、时延对齐的MP3听辨样本。第二课时若做D6，按course-design.qmd的8秒44.1kHz/16bit单声道PCM→128/32kbps规格，用同一源文件各编码一次，记录编码器、增益和时延；不得把音量差当作压缩差。来源与技术边界见课程设计C7。"))
        notebook={"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.10"}},"nbformat":4,"nbformat_minor":5}
        # Stable IDs are supported in nbformat 4.5 and aid later alignment checks.
        for i,c in enumerate(cells): c["id"]=f"{role}-{i:03d}"
        (ROOT/f"demo-lab-{role}.ipynb").write_text(json.dumps(notebook,ensure_ascii=False,indent=1),encoding="utf-8")
        qmd=f'---\ntitle: "数据压缩入门：{title}"\nlang: zh-CN\nformat: html\nexecute:\n  enabled: false\n---\n\n'
        for c in cells:
            source="".join(c["source"])
            qmd += ("```{python}\n"+source+"\n```\n\n") if c["cell_type"]=="code" else source+"\n\n"
        (ROOT/f"demo-lab-{role}.qmd").write_text(qmd,encoding="utf-8")

ACTIVITIES = '''---
title: "数据压缩入门：课堂记录"
lang: zh-CN
format:
  html:
    toc: false
execute:
  enabled: false
---

姓名：________  班级：________  同桌：________

# A1 颜色传话（Q2–Q4）

发送者看教师发的折叠原卡，接收者先不看原卡。发送者60秒写规则和短消息；接收者30秒画回，再展开核对。本页没有原卡答案。

规则：________________________________________________

短消息：______________________________________________

接收者的16格还原：

□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ □

逐位置比较：一致／不一致。若不一致，第一处是第____格。

回到共同例，原16B；编号、次数各1B。连续段编码____B；红绿交替编码____B。

我怎样检查一个也没丢：________________________________

# A2 完整变化与近似（Q5–Q6）

教师收集Q5方案后再打开本页。灰度0–255，每项8bit。先用首值及差值读回。

|位置|1|2|3|4|5|6|7|8|
|---|---|---|---|---|---|---|---|---|
|原值|120|121|122|121|120|120|121|122|
|首值／差值|120|+1|+1|−1|____|____|____|____|
|读回值|____|____|____|____|____|____|____|____|

只看首值与差值，我读回末三个数：____，____，____。

起点8bit，七个差值各2bit：共____bit，装入____B，补____bit。

Q6再用近似规则：归到最近的4的倍数，中点向上取，上限252。

八项代表值：____，____，____，____，____，____，____，____。

两个能归到120的不同原数：____和____。

能／不能唯一恢复，理由：________________________________

# A3 按任务选方案（Q8–Q10）

先确定什么不能改，再检查大小。Q8逐项判可以／不可以／需补条件。

|任务与变化|判断|理由|
|---|---|---|
|通知“本周五”变“本周”|____|________________|
|源程序>=60变>60，输入60|____|________________|
|照片浏览副本，人物与活动清楚|____|________________|

Q9：改正“JPG、TIF、MP3、MPEG都是有损；图片不能无损”：

______________________________________________________

Q10限额100KiB（1KiB=1024B），以下是题目给定结果。

|任务（原120KiB）|方案A|方案B|
|---|---|---|
|源程序，原bytes须完整恢复|无损80KiB，bytes一致|删改50KiB，不能恢复|
|照片浏览，人物主题清楚|无损110KiB，像素一致|有损70KiB，主题清楚|

|任务|选项|大小过关吗|信息过关吗|另一方案为什么不合格|
|---|---|---|---|---|
|源程序|____|____|____|________________|
|照片浏览|____|____|____|________________|

## 独立出口（40秒）

无损判断要比较________________与________________。

照片看不出变化仍可能有损，因为________________________。
'''

def print_pdf():
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.colors import HexColor
    font=Path('/Users/chran/Library/Fonts/AlibabaPuHuiTi-3-55-Regular.ttf')
    pdfmetrics.registerFont(TTFont("Alibaba", str(font)))
    target=ROOT/'exports/print/student-activities.pdf'
    c=canvas.Canvas(str(target),pagesize=A4)
    c.setTitle("数据压缩入门：课堂记录与私有颜色卡")
    W,H=A4
    def text(value,y,size=12): c.setFont('Alibaba',size);c.setFillColor(HexColor('#262626'));c.drawString(42,y,value)
    def heading(title,page):
        c.setFillColor(HexColor('#6251B1'));c.rect(0,H-8,W,8,fill=1,stroke=0)
        text(title,H-60,20);text('姓名：____________  班级：____________  同桌：____________',H-94)
        text(f'数据压缩入门  /  {page}',25,10)
    def rule(y): c.setStrokeColor(HexColor('#bfbfbf'));c.line(42,y,W-42,y)
    def table(rows,y,widths,height=42):
        x=42
        for row in rows:
            xx=x
            for value,width in zip(row,widths):
                c.setStrokeColor(HexColor('#bfbfbf'));c.rect(xx,y-height,width,height,stroke=1,fill=0)
                c.setFont('Alibaba',11);c.setFillColor(HexColor('#262626'))
                for k,line in enumerate(value.split('\n')): c.drawString(xx+6,y-17-k*16,line)
                xx+=width
            y-=height
        return y
    heading('A1 颜色传话',1)
    for value,y in [('发送者看折叠原卡；接收者先不看。先定规则，再传短消息。',H-139),('发送者60秒写消息，接收者30秒画回，再展开卡逐位置比较。',H-165),('规则：',H-215),('短消息：',H-315),('接收者的16格还原（填写红／绿／蓝）：',H-410)]: text(value,y)
    rule(H-270);rule(H-365)
    for i in range(16): c.rect(42+i*31.8,H-463,31.8,31.8)
    text('逐位置比较：一致 / 不一致。第一处不同在第________格。',H-505)
    text('我怎样证明一个也没丢：',H-555);rule(H-611)
    text('原16B；编号、次数各1B（双方共享规则，只比数据部分）。',H-659)
    text('共同例编码________B；红绿交替编码________B。',H-699)
    c.showPage()
    heading('A2 完整变化与近似',2)
    text('Q5先提方案；教师给首值和前三个差值后，再打开本页。',H-138)
    text('灰度0–255，每项8bit。用首值与每次变化完整读回。',H-168)
    table([['位置','1','2','3','4','5','6','7','8'],['原值','120','121','122','121','120','120','121','122'],['首值/差值','120','+1','+1','−1','','','',''],['读回值','','','','','','','','']],H-201,[78]+[54]*8,44)
    text('只看首值与差值，末三个读回值：________，________，________。',H-413)
    text('8 + 7 × 2 = ________ bit；装入________ B，补________ bit。',H-452)
    text('Q6：归到最近的4的倍数，中点向上取，最高只到252。',H-512)
    text('八项代表值：',H-550);rule(H-599)
    text('两个能恢复成120的原数：________ 和 ________。',H-644)
    text('能 / 不能唯一恢复，理由：',H-685);rule(H-735)
    c.showPage()
    heading('A3 按任务选方案',3)
    table([['Q8任务与变化','判断','理由'],['通知“本周五”变“本周”','',''],['源程序>=60变>60；输入60','',''],['照片浏览副本；人物活动清楚','','']],H-137,[252,70,188],39)
    text('Q9：改正“JPG、TIF、MP3、MPEG都是有损；',H-322)
    text('图片不能无损压缩”：',H-344);rule(H-372)
    text('Q10限额100KiB，1KiB=1024B。以下为题目给定结果。',H-395)
    table([['任务（原120KiB）','方案A','方案B'],['源程序\n原bytes须完整恢复','无损80KiB\nbytes一致','删改50KiB\n不能恢复原bytes'],['照片浏览\n人物主题清楚','无损110KiB\n像素一致','有损70KiB\n主题清楚']],H-421,[178,166,166],47)
    text('程序选____；大小过关____；信息过关____。',H-593)
    text('另一方案不合格，因为__________________________________。',H-616)
    text('照片选____；大小过关____；信息过关____。',H-643)
    text('另一方案不合格，因为__________________________________。',H-666)
    text('独立出口（40秒）：无损要比较____________与____________。',H-708)
    text('看不出变化仍可能有损，因为____________________________。',H-745)
    c.showPage()
    heading('教师剪下发放：私有颜色卡',4)
    text('Q2时发放；只给发送者看，下折遮住原串。接收者画完再展开。',H-138)
    for j, card in enumerate([[3]*4+[1]*7+[2]*5,[2]*6+[3]*4+[1]*6]):
        y=H-225-j*230
        text(f'卡{j+1}  发送者原串（不得先给接收者看）',y,14)
        text(' '.join(lab.NAMES[n] for n in card),y-49,12)
        c.setDash(5,4);rule(y-85);c.setDash()
        text('沿虚线向下折；背面写规则与消息。接收者先只看背面。',y-119)
        rule(y-165)
    text('原卡上的次序和次数不投影。不预先印编码答案。',94)
    c.save()

def main():
    notebooks()
    (ROOT/'student-activities.qmd').write_text(ACTIVITIES,encoding='utf-8')
    print_pdf()
    manifest={"question_count":10,"core_minutes":45,"notebooks":["demo-lab-teacher.ipynb","demo-lab-student.ipynb"],"D1":lab.opening(True),"D3":lab.predictive(lab.GRAY),"D4":lab.approximate(lab.GRAY),"D5":lab.image_evidence()}
    (ROOT/'sources/evidence-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Teacher/student notebooks, worksheet source and printable PDF generated.')

if __name__=='__main__': main()
