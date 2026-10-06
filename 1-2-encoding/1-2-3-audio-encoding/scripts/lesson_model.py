"""Read the teaching authority and compile stage-specific delivery plans."""
from pathlib import Path
import re
import json
ROOT = Path(__file__).resolve().parents[1]

def section(body, name):
    match = re.search(r'^### ' + re.escape(name) + r'\n([\s\S]*?)(?=^### |\Z)', body, re.M)
    return match.group(1).strip() if match else ''

def load_lesson():
    source = (ROOT / 'course-design.qmd').read_text()
    questions = [(int(n), title, body) for n, title, body in re.findall(
        r'^## Q(\d+) (.+)\n([\s\S]*?)(?=^## Q\d+ |^# C6)', source, re.M)]
    model = json.loads(re.search(r'# C8 [\s\S]*?```json\n([\s\S]*?)\n```', source)[1])
    return source, questions, model

def compile_plan():
    source, questions, model = load_lesson()
    plan = []
    def add(identifier, q, stage, title, visible, script, evidence, focus='', withheld=None, pair=None, nodes=None):
        note = f'[問題] {title}\n[内部编号] {identifier}\n[阶段] {stage}\n[教师逐字稿]\n{script}'
        note = note.replace('[問題]', '[问题]')
        row = dict(page=len(plan)+1, id=identifier, q=q, stage=stage, title=title,
                   visible=visible, withheld=withheld or [], notes=note, evidence=evidence,
                   focus=focus, pair=pair, tree_nodes=nodes or [])
        plan.append(row)
        return row
    add('opening', None, 'opening', '音频数字化', ['一段声音怎样变成二进制数据？', '从波形到未压缩 PCM WAV'],
        '回想上节课怎样用有限位置与颜色记录图像。今天先听同一段音乐的两个版本，保留一个可以核对的猜测。准备纸笔，课堂由我操作演示，你们记录依据。', '用户提供的音乐及计算模型')
    established = ['root']
    for q, title, body in questions:
        givens = section(body, '投影提问').splitlines()
        answers = section(body, '揭示').splitlines()
        question = add(f'Q{q}-question', q, 'question', title, givens, section(body, '提问逐字稿'),
                       f'course-design Q{q}; ' + (f'D{ {3:1,8:2,10:3,17:4}[q] }' if q in [3,8,10,17] else '题面与原生证据'),
                       withheld=answers)
        # References and anticipated responses are held teacher-side, after the spoken question.
        question['notes'] += '\n[教师参考，不在提问阶段朗读]\n' + section(body, '认知起点') + '\n[预期反应]\n' + section(body, '预期回答')
        if q == 15:
            first = add('Q15-count', q, 'evidence', title, givens+answers[:1],
                        '核对一秒一路的fs个样本，再乘时长和声道数。先只数总共有多少个数，暂不换成字节。', '逐层样本计数', '样本总数', answers[1:], question['id'])
            answer = add('Q15-answer', q, 'answer', title, givens+answers, section(body, '教师逐字稿'), '逐层样本计数', 'bit换成B', pair=first['id'])
        else:
            answer = add(f'Q{q}-answer', q, 'answer', title, givens+answers, section(body, '教师逐字稿'),
                         question['evidence'], '当前问题结论', pair=question['id'])
        answer['notes'] += '\n[形成结论]\n'+section(body,'形成结论')+'\n[追问问题]\n'+section(body,'追问')+'\n[下一问]\n'+section(body,'下一问')+'\n[Demo操作与技术参考，不投影]\n'+section(body,'Demo 操作')
        for task in model['subtasks']:
            if task['after'] != q: continue
            a = add(task['id']+'-question', q, 'question', task['title'], task['givens'],
                    task['question_script'], task['evidence'], withheld=task['answers'])
            add(task['id']+'-answer', q, 'answer', task['title'], task['givens']+task['answers'],
                task['answer_script'], task['evidence'], '独立推理结果', pair=a['id'])
        for stage in model['tree']['stages']:
            if stage['after'] != q: continue
            previous = add(stage['id']+'-summary', q, 'tree-summary', stage['prompt'], [],
                           stage['collect']+'先请学生说，留出总结停顿。追问“哪项观察或记录支持你？”收集后才逐次更新树。',
                           'Q'+str(q)+'之前的学生记录', '学生总结', stage['new'], nodes=established.copy())
            for node_id in stage['new']:
                established.append(node_id)
                node = next(n for n in model['tree']['nodes'] if n['id']==node_id)
                current = add(stage['id']+'-'+node_id, q, 'tree-reveal', stage['prompt'], [],
                              '依据刚才学生的总结，现在只补这一项：'+node['label'].replace('\n','，')+'。连接表示'+node['meaning']+'。请学生指对应证据，再和先前节点联系；下一次翻页才增加下一项。',
                              ' / '.join('Q'+str(x) for x in node['qs']), node_id, pair=previous['id'], nodes=established.copy())
                previous=current
    add('homework', None, 'homework', '课后练习', ['1. 22.05kHz、16bit、单声道，10秒有多少B样本数据？', '2. 4bit改为8bit，等级数变成原来的几倍？', '3. 8kHz录音转为48kHz，能恢复未记录的6kHz吗？', '计算写出单位；解释写出条件。'],
        '三题分别检查计数、等级和信息能否恢复。先独立写出参数与依据，下次核对。\n[教师答案，作答后提供] 441,000B；16倍；不能恢复未记录或已丢失内容。', 'C6', withheld=['课后练习答案'])
    return plan

if __name__ == '__main__':
    target=ROOT/'validation/v4/slide-plan.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(compile_plan(),ensure_ascii=False,indent=2)+'\n')
    print(f'Compiled {len(compile_plan())} slide stages from course-design.qmd')
