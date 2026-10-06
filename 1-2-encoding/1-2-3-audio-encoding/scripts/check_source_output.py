"""Check current sources against encoded and generated delivery artifacts."""
from pathlib import Path
from html.parser import HTMLParser
import ast
import base64
import hashlib
import io
import json
import re
import tokenize
import nbformat
from lesson_model import ROOT, compile_plan, load_lesson

checks = []
def check(name, passed):
    checks.append(dict(name=name, passed=bool(passed)))
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

plan = compile_plan()
check('design-derived plan equals delivered plan', plan == json.loads((ROOT/'validation/v4/slide-plan.json').read_text()))
for role in ['teacher', 'student']:
    notebook = nbformat.read(ROOT/f'demo-lab-{role}.ipynb', 4)
    qmd = (ROOT/f'demo-lab-{role}.qmd').read_text()
    blocks = re.findall(r'```\{python\}\n([\s\S]*?)\n```', qmd)
    check(role+' QMD/IPYNB code identity', blocks == [c.source for c in notebook.cells if c.cell_type=='code'])
    check(role+' QMD/IPYNB prose identity', all(c.source in qmd for c in notebook.cells if c.cell_type=='markdown'))
    executed = nbformat.read(ROOT/f'validation/v4/executed/demo-lab-{role}.ipynb', 4)
    check(role+' executed cell sources equal clean delivery', [c.source for c in executed.cells] == [c.source for c in notebook.cells])
for path in sorted((ROOT/'notebooks/staged').glob('*.ipynb')):
    clean = nbformat.read(path, 4)
    executed = nbformat.read(ROOT/'validation/v4/executed'/path.name, 4)
    check(path.name+' executed source identity', [c.source for c in clean.cells] == [c.source for c in executed.cells])

_, questions, model = load_lesson()
student = nbformat.read(ROOT/'demo-lab-student.ipynb', 4)
tree_prompt = next(s['student_prompt'] for s in model['tree']['stages'] if s['id']=='T4')
check('T4 student prompt is neutral in both student formats', tree_prompt in (ROOT/'student-activities-b.qmd').read_text() and any(tree_prompt in c.source for c in student.cells))
check('T4 teacher solution withheld from student text', all('16k的两项证据' not in c.source for c in student.cells) and '16k的两项证据' not in (ROOT/'student-activities-b.qmd').read_text())
check('worksheet Q7 gives no missing-parameter answer', '没有采样率' not in (ROOT/'student-activities-a.qmd').read_text())
for number, title, body in questions:
    required = ['认知起点', '认知困惑', '学生任务', '预期回答', '追问', '提问逐字稿', '教师逐字稿', '形成结论', '下一问']
    check(f'Q{number} design reasoning sections', all('### '+h+'\n' in body for h in required))

class RevealImages(HTMLParser):
    def __init__(self):
        super().__init__(); self.images=[]
    def handle_starttag(self, tag, attrs):
        values=dict(attrs)
        if tag=='section' and 'data-background-image' in values:
            self.images.append(values['data-background-image'])
reveal = RevealImages()
reveal.feed((ROOT/'exports/reference-v4/slides.html').read_text())
check('Reveal has exactly one section per planned stage', len(reveal.images)==len(plan))
for page, data in enumerate(reveal.images, 1):
    actual = hashlib.sha256(base64.b64decode(data.split(',',1)[1])).hexdigest()
    check(f'Reveal stage {page} equals final render', actual==digest(ROOT/f'validation/v4/render/slide-{page:02}.png'))

# Review implementation commentary separately from justified Chinese teaching literals.
language_findings=[]
python_sources=[*sorted((ROOT/'scripts').glob('*.py')),ROOT/'demos/audio_core.py']
for path in python_sources:
    source=path.read_text()
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type==tokenize.COMMENT and re.search(r'[\u4e00-\u9fff]',token.string):
            language_findings.append(dict(file=str(path.relative_to(ROOT)),line=token.start[0],kind='implementation comment'))
    tree=ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node,(ast.Module,ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            text=ast.get_docstring(node)
            if text and re.search(r'[\u4e00-\u9fff]',text):
                language_findings.append(dict(file=str(path.relative_to(ROOT)),line=getattr(node,'lineno',1),kind='docstring'))
for path in [*sorted((ROOT/'scripts').glob('*.mjs')),ROOT/'demos/audio-lab.html']:
    for line_number,line in enumerate(path.read_text().splitlines(),1):
        if line.lstrip().startswith(('//','/*','* ')) and re.search(r'[\u4e00-\u9fff]',line):
            language_findings.append(dict(file=str(path.relative_to(ROOT)),line=line_number,kind='implementation comment'))
check('English implementation comments and docstrings',not language_findings)

report=dict(version='v4',date='2026-10-01',passed=all(c['passed'] for c in checks),checks=checks,language_findings=language_findings,design_sha256=digest(ROOT/'course-design.qmd'),pptx_sha256=digest(ROOT/'exports/1-2-3-audio-encoding-v4-final.pptx'),language_scope='Comments and docstrings scanned; identifiers/developer messages manually reviewed. Chinese teaching labels, exact data and generated teaching prose are permitted literals.',scope='Source/output identity and basic design completeness; semantic, visual and classroom acceptance are separately recorded.')
(ROOT/'validation/v4/source-output-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=report['passed'],checks=len(checks),failures=[c for c in checks if not c['passed']])))
raise SystemExit(0 if report['passed'] else 1)
