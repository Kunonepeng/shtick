"""从course-design生成Notebook与Reveal源；不修改教学依据。"""
from pathlib import Path
import re, json, textwrap
import nbformat as nb
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'course-design.qmd').read_text()
questions=re.findall(r'^## Q(\d+) (.+)\n([\s\S]*?)(?=^## Q\d+ |^# C6)',source,re.M)
def section(body,name):
    match=re.search(r'^### '+name+r'\n([\s\S]*?)(?=^### |\Z)',body,re.M)
    return match.group(1).strip() if match else ''
setup="""from pathlib import Path
import sys
# 从课程目录或其demos目录启动均可；不使用当前用户的绝对路径。
ROOT = Path.cwd()
if not (ROOT / 'demos' / 'audio_core.py').exists():
    if (ROOT.parent / 'demos' / 'audio_core.py').exists(): ROOT = ROOT.parent
    else: raise RuntimeError('请从1-2-3-audio-encoding课程目录打开Notebook')
sys.path.insert(0, str(ROOT / 'demos'))
from audio_core import plot_sampling, plot_quantization, show_audio, pcm_info, quantize, codes
from IPython.display import display, IFrame
"""
demos={
 '3':('D1','plot_sampling(12, False)','plot_sampling(12, True)\nplot_sampling(24, True)'),
 '8':('D2',"show_audio('music-44100-16-mono.wav')\nshow_audio('music-8000-16-mono.wav')", "show_audio('tone-6000-at24000.wav')\nshow_audio('tone-lowpass-at8000.wav')"),
 '10':('D3','plot_quantization(2, False)',"plot_quantization(2, True)\nplot_quantization(4, True)\nshow_audio('music-22050-effective4-stored16-mono.wav')\nshow_audio('music-22050-16-mono.wav')"),
 '17':('D4',"# 先预测公式结果与完整文件大小是否相同。", "info = pcm_info(ROOT / 'assets/audio/size-check-8000-2s-16-mono.wav')\ndisplay(info)")}
for role in ['teacher','student']:
    cells=[nb.v4.new_markdown_cell('# 音频数字化\n\n'+('教师演示与备课视图。课堂只投影题目／输出，先清空旧输出，折叠教师说明和代码。' if role=='teacher' else '课堂观察／课后阅读视图；不要求现场运行。先在纸上预测，再由教师揭示证据。')),
           nb.v4.new_code_cell(setup,metadata={'tags':['setup','hide-input']})]
    for n,title,body in questions:
        cells.append(nb.v4.new_markdown_cell(f'## Q{n} {title}\n\n'+section(body,'投影提问')+'\n\n预测：________\n\n观察后解释：________'))
        if role=='teacher':
            cells.append(nb.v4.new_markdown_cell('**教师说明（不投影）**\n\n'+section(body,'教师逐字稿')+'\n\n追问：'+section(body,'追问')+'\n\n技术结论：'+section(body,'形成结论'),metadata={'tags':['teacher-only']}))
        if n == '1':
            cells.append(nb.v4.new_markdown_cell('### 开场试听：A、B；先听，暂不揭示参数。'))
            cells.append(nb.v4.new_code_cell("from IPython.display import HTML\ndisplay(HTML('<p>A</p>'))\nshow_audio('music-44100-16-mono.wav')\ndisplay(HTML('<p>B</p>'))\nshow_audio('music-8000-16-mono.wav')",metadata={'tags':['opening','hide-input']}))
        if n in demos:
            did,before,after=demos[n]
            cells.append(nb.v4.new_markdown_cell(f'### {did} 先预测，后运行'))
            cells.append(nb.v4.new_code_cell(before,metadata={'tags':[did,'before-reveal']}))
            cells.append(nb.v4.new_markdown_cell('**等待讨论。下面单元只在完成预测后运行。**'))
            cells.append(nb.v4.new_code_cell(after,metadata={'tags':[did,'after-prediction']}))
    if role=='teacher':
        cells += [nb.v4.new_markdown_cell('## 离线实验台备用\n需要逐个读点动画时使用；嵌入加载失败则用PPTX静态图与预制WAV。'),nb.v4.new_code_cell("display(IFrame(src='demos/audio-lab.html', width='100%', height=720))",metadata={'tags':['fallback']})]
    cells.append(nb.v4.new_markdown_cell('## 课后练习\n\n1. 22.05kHz、16bit、单声道10秒，样本数据量是多少B？\n2. 4bit变成8bit，等级数变成几倍？\n3. 把8kHz录音转换成48kHz，能恢复未记录的6kHz吗？'))
    if role=='teacher':cells.append(nb.v4.new_markdown_cell('教师答案：441,000B；16倍；不能恢复未记录或已丢失的信息。'))
    notebook=nb.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.11'}})
    nb.write(notebook,ROOT/f'demo-lab-{role}.ipynb')
    qmd=['---',f'title: "音频数字化：{ "教师演示" if role=="teacher" else "学生观察" }"','lang: zh-CN','jupyter: python3','execute:','  enabled: false','format: html','---','']
    for cell in cells:
        if cell.cell_type=='markdown':qmd.append(cell.source+'\n')
        else:qmd.append('```{python}\n'+cell.source+'\n```\n')
    (ROOT/f'demo-lab-{role}.qmd').write_text('\n'.join(qmd)+'\n')
# Reveal includes same Q title, neutral givens and separate answer slides; no teacher guidance.
slides=['---','title: "音频数字化"','lang: zh-CN','format:','  revealjs:','    slide-level: 2','    theme: simple','    css: styles.css','    transition: none','    controls: true','execute:','  enabled: false','---','']
for n,title,body in questions:
    slides.extend([f'## {title}',section(body,'投影提问').replace('\n','\n\n'),''])
    if n in ['2','3']:slides.append(f'![](assets/fallback/Q{n}-question.png){{height=330}}\n')
    slides.extend([f'## {title}',section(body,'投影提问').replace('\n','\n\n'),'\n::: {.reveal-answer}',section(body,'揭示').replace('\n','\n\n'),':::',''])
slides.extend(['## 课后练习','22.05kHz、16bit、单声道10秒，样本数据量是多少B？','\n4bit变成8bit，等级数变成几倍？','\n8kHz录音转48kHz，能恢复未记录的6kHz吗？'])
(ROOT/'slides.qmd').write_text('\n'.join(slides)+'\n')
# Paper activity sheet without answers or teacher-only source notes.
activity=['---','title: "音频数字化课堂活动单"','lang: zh-CN','format:','  html:','    toc: false','    embed-resources: true','---','','姓名：________　班级：________','']
for n in ['3','5','6','7','16','18','19']:
    _,title,body=next(q for q in questions if q[0]==n)
    activity.extend([f'## Q{n} {title}',section(body,'投影提问').replace('\n','\n\n'),''])
    if n == '3': activity.append('![](assets/fallback/Q3-question.png){width=95%}\n')
    activity.extend(['我的记录／算式：','\n____________________________','\n____________________________','\n我的解释：____________________________',''])
(ROOT/'student-activities.qmd').write_text('\n'.join(activity)+'\n')
print(json.dumps({'questions':len(questions),'notebooks':2,'reveal':'slides.qmd','worksheet':'student-activities.qmd'}))
