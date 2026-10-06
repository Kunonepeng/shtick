"""Generate role views, classroom stages, Reveal source and staged worksheets."""
from pathlib import Path
import argparse
import base64
import json
import nbformat as nb
from lesson_model import ROOT, load_lesson, section, compile_plan

parser=argparse.ArgumentParser()
parser.add_argument('--rendered-slides',type=Path)
args=parser.parse_args()
source, questions, model=load_lesson()
plan=compile_plan()
(ROOT/'validation/v4/slide-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
setup="""from pathlib import Path
import sys
ROOT = Path.cwd()
while not (ROOT / 'demos' / 'audio_core.py').exists():
    if ROOT == ROOT.parent:
        raise RuntimeError('Start the kernel inside the audio lesson directory')
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT / 'demos'))
from audio_core import plot_sampling, plot_quantization, plot_quantization_compare
from audio_core import show_waveform, show_recorded_values
from audio_core import show_quantization_evidence, show_audio, show_pcm_evidence, show_opening
from audio_core import show_frequency_baseline, show_frequency_result, show_quantization_audio
"""
def prose(value):return nb.v4.new_markdown_cell(value)
def code(value,*tags):return nb.v4.new_code_cell(value,metadata={'tags':list(tags),'jupyter':{'source_hidden':True}})
def wait():return prose('**先写预测或解释，等待讨论；下一单元只在作答后运行。**')
def task_cells(task,role):
    cells=[prose('### '+task['id']+' '+task['title']+'\n\n'+'\n\n'.join(task['givens'])+'\n\n我的预测／算式：________'),wait()]
    if role=='teacher': cells.append(prose('教师参考（不投影）：'+task['answer_script']))
    return cells

def group(q,title,body,role):
    cells=[prose(f'## Q{q} {title}\n\n'+section(body,'投影提问')+'\n\n预测：________\n\n观察后解释：________')]
    if role=='teacher':cells.append(prose('教师参考（不投影）：\n\n提问稿：'+section(body,'提问逐字稿')+'\n\n作答后解释稿：'+section(body,'教师逐字稿')+'\n\n追问：'+section(body,'追问')))
    if q==1:cells += [wait(),code('show_opening()','opening','after-prediction')]
    if q==3:cells += [code('show_waveform()','D1','before-reveal'),wait(),code('show_recorded_values()','D1','after-prediction')]
    if q==8:cells += [wait(),code("show_frequency_baseline()",'D2','baseline')]
    if q==10:cells += [code('plot_quantization(2, False)','D3','before-reveal'),wait(),code('plot_quantization_compare()','D3','after-prediction')]
    if q==17:cells += [wait(),code("size_evidence = show_pcm_evidence('size')",'D4','size','after-prediction')]
    for task in model['subtasks']:
        if task['after']!=q:continue
        cells += task_cells(task,role)
        if q==8:cells.append(code("show_frequency_result()",'D2','after-prediction'))
        if q==10:cells += [code('quantization_evidence = show_quantization_evidence()','D3','error-measurement'),prose('图比较2bit／4bit；下面试听比较4bit有效模型／16bit基准。两份均为22.05kHz、单声道、16bit存储。'),code("show_quantization_audio()",'D3','audio-comparison')]
        if q==17:cells.append(code("opening_evidence = show_pcm_evidence('opening')",'D4','opening-revisit','after-prediction'))
    for stage in model['tree']['stages']:
        if stage['after']==q:
            prompt=stage['collect'] if role=='teacher' else stage.get('student_prompt',stage['collect'])
            cells.append(prose('### '+stage['id']+' 总结与证据\n\n'+prompt+'\n\n我的总结：________\n\n依据：________'))
    return cells

def save_notebook(cells,path):
    notebook=nb.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'audio_version':'v4'})
    path.parent.mkdir(parents=True,exist_ok=True);nb.write(notebook,path)
    return notebook

def qmd_view(notebook,role):
    lines=['---',f'title: "音频数字化：{role}"','lang: zh-CN','jupyter: python3','execute:','  enabled: false','format:','  html:','    code-fold: true','---','']
    for cell in notebook.cells:lines.append(cell.source+'\n' if cell.cell_type=='markdown' else '```{python}\n'+cell.source+'\n```\n')
    return '\n'.join(lines).rstrip()+'\n'
for role in ['teacher','student']:
    cells=[prose('# 音频数字化\n\n'+('教师备课与试跑；教师说明不投影。' if role=='teacher' else '完整学生阅读版，含后续题面。课堂仅投影notebooks/staged中当前阶段，仍由教师操作。')),code(setup,'setup')]
    for q,title,body in questions:cells += group(q,title,body,role)
    if role=='teacher':cells += [prose('## 可选与备用\n24点仅时间允许时运行；HTML只显示指定阶段，不追加第五个核心Demo。'),code("plot_sampling(24, True)\nfrom IPython.display import display, IFrame\ndisplay(IFrame(src='/files/demos/audio-lab.html?stage=D1', width='100%', height=720))",'optional','fallback')]
    cells.append(prose('## 课后练习\n\n22.05kHz、16bit、单声道10秒有多少B样本数据？\n\n4bit变8bit，等级数变为几倍？\n\n8kHz转48kHz能恢复未记录的6kHz吗？'))
    if role=='teacher':cells.append(prose('教师答案（课后作答后提供）：441,000B；16倍；不能恢复未记录或已丢失信息。'))
    n=save_notebook(cells,ROOT/f'demo-lab-{role}.ipynb')
    (ROOT/f'demo-lab-{role}.qmd').write_text(qmd_view(n,'教师' if role=='teacher' else '学生'))
stage_count=0
for q,name in [(1,'opening'),(3,'D1'),(8,'D2'),(10,'D3'),(17,'D4')]:
    _,title,body=next(x for x in questions if x[0]==q)
    current=group(q,title,body,'student')
    split=next((i for i,c in enumerate(current) if c.cell_type=='markdown' and c.source.startswith('### Q')),len(current))
    save_notebook([prose('# 当前课堂证据：'+title+'\n\n由教师操作；先预测、再逐单元运行。不要Run All。'),code(setup,'setup')]+current[:split],ROOT/f'notebooks/staged/{name}-student.ipynb')
    stage_count+=1
    if split<len(current):
        save_notebook([prose('# 当前子问题：'+name+'-B\n\n主问题建立结论后才打开本文件；逐单元操作。'),code(setup,'setup')]+current[split:],ROOT/f'notebooks/staged/{name}-B-student.ipynb')
        stage_count+=1

head=['---','title: "音频数字化课堂活动单"','lang: zh-CN','format:','  html:','    embed-resources: true','    css: worksheet.css','---','','姓名：________　班级：________','']
segments={'a':[],'b':[],'exit':[]}
for q in [3,5,6,7,10,16,18,19]:
    _,title,body=next(x for x in questions if x[0]==q)
    stage='a' if q<8 else 'exit' if q==19 else 'b'
    givens=section(body,'投影提问') if q!=7 else '只有四个已编码样本，能确定播放时长吗？课堂短口答并记依据；画时间轴留作课后拓展。'
    content=[f'## Q{q} {title}',givens,'']
    if q==3:content.append('![](assets/fallback/Q3-question.png){width=95%}\n')
    if q==5:content += ['|样本值|近似值|Q6码字（学到编码后填写）|','|---|---|---|','|−0.62|________|________|','|−0.10|________|________|','|0.38|________|________|','|0.84|________|________|']
    if q==6:content.append('填写上一表码字，再互读查回代表值。')
    if q==10:content += ['### Q10-B 误差核对','原值−0.10；2bit代表值−0.25，4bit代表值−0.0625。分别算绝对差。','2bit误差：________　4bit误差：________']
    if q==16:content.append('采样率：________Hz；时长：________s；存储位数：________bit；声道数：________。')
    if q==18:content += ['靠窗先查8k，另一位先查24k，再合查16k。','|采样率|频率条件及理由|样本数据B|容量条件|','|---|---|---|---|','|8kHz|________|________|________|','|16kHz|________|________|________|','|24kHz|________|________|________|']
    if q==19:content.append('独立60秒：必改③，再选①或②；每项写一条依据。收卷前不交换。')
    content += ['我的记录／算式：____________________________','', '我的解释与依据：____________________________','']
    segments[stage]+=content
for stage in model['tree']['stages']:
    where='a' if stage['id']=='T1' else 'b'
    segments[where] += ['## '+stage['id']+' 总结与证据',stage.get('student_prompt',stage['collect']),'我的总结：____________________________','依据：____________________________','']
# The combined worksheet is a teacher assembly source, not an early student handout.
(ROOT/'student-activities.qmd').write_text('\n'.join(head+['教师组合源：课堂按A／B／exit分发，不整份提前发。']+sum(segments.values(),[])).rstrip()+'\n')
for stage,content in segments.items():(ROOT/f'student-activities-{stage}.qmd').write_text('\n'.join(head+content).rstrip()+'\n')
answers=['# 音频课堂活动：教师核对与收集','A在Q3分发；B在Q10主问题揭示后、Q10-B前分发；exit在Q19分发。先收全班独立答卷，再公开答案。','Q5：−0.75、−0.25、0.25、0.75；Q6：00、01、10、11，读回的是代表值。','Q10-B：0.15、0.0375；一个样本不证明每点都严格改善。','Q16：10,584,000B；MiB列式正确即达标，近似10.09。','Q18：8k为32,000B但频率不足；16k为64,000B两项通过；24k为96,000B超容量。','Q19：③须分别改容器与公式两项并引用真实差额；①或②至少一项正确。①每秒每声道记录次数，非声音频率；②2^16=65,536。','分项记录：量化/码字、四参数/单位、频率/容量、退出诊断。只报答案无依据需追问；C1列出持续误解的回应。']
(ROOT/'student-activities-teacher.md').write_text('\n\n'.join(answers)+'\n')
slides=['---','pagetitle: "音频数字化参考"','lang: zh-CN','format:','  revealjs:','    slide-level: 2','    theme: simple','    width: 1280','    height: 720','    margin: 0','    menu: false','    css: reveal-v4.css','    transition: none','execute:','  enabled: false','---','']
for row in plan:
    slides += ['## '+row['title'],f'<!-- {row["id"]} -->','']
    if args.rendered_slides:
        image=args.rendered_slides/f'slide-{row["page"]:02}.png'
        slides[-3]='## '+row['title']+' {background-image="data:image/png;base64,'+base64.b64encode(image.read_bytes()).decode()+'" background-size="contain"}'
    else:
        slides += row['visible']
        if row['tree_nodes']:
            slides += [model['tree']['root']['label'].replace('\n','：')]+[x['label'].replace('\n','：') for x in model['tree']['nodes'] if x['id'] in row['tree_nodes']]
    slides += ['::: {.notes}',row['notes'],':::','']
(ROOT/'slides.qmd').write_text('\n'.join(slides).rstrip()+'\n')
print(json.dumps({'version':'v4','slides':len(plan),'role_notebooks':2,'classroom_notebooks':stage_count,'worksheet_segments':3}))
