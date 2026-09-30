"""Check real kernel outputs for the two D4 reveals against independent WAV reads."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import wave
import nbformat

ROOT = Path(__file__).resolve().parents[1]
class Rows(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows=[]; self.current=[]; self.cell=None
    def handle_starttag(self,tag,attrs):
        if tag=='tr': self.current=[]
        if tag in ['td','th']: self.cell=''
    def handle_data(self,data):
        if self.cell is not None: self.cell+=data
    def handle_endtag(self,tag):
        if tag in ['td','th']:
            self.current.append(self.cell); self.cell=None
        if tag=='tr': self.rows.append(self.current)

passed = []
def expected(label,name):
    path=ROOT/'assets/audio'/name
    with wave.open(str(path),'rb') as w:
        fs=w.getframerate(); frames=w.getnframes(); bits=w.getsampwidth()*8; channels=w.getnchannels()
    return [label,f'{fs:,}',f'{frames/fs:g}',str(bits),str(channels),f'{frames*bits*channels//8:,}',f'{path.stat().st_size:,}']
for role in ['teacher','student']:
    executed=nbformat.read(ROOT/f'.build/demo-lab-{role}-executed.ipynb',4)
    original=nbformat.read(ROOT/f'demo-lab-{role}.ipynb',4)
    assert [c.source for c in executed.cells if c.cell_type=='code']==[c.source for c in original.cells if c.cell_type=='code']
    parts=[]
    for stage,names in [('size',[('2秒样例','size-check-8000-2s-16-mono.wav')]),
                        ('opening',[('开场A','music-44100-16-mono.wav'),('开场B','music-8000-16-mono.wav')])]:
        cell=next(c for c in executed.cells if c.cell_type=='code' and f"show_pcm_evidence('{stage}')" in c.source)
        htmls=[o.data['text/html'] for o in cell.outputs if o.output_type in ['display_data','execute_result'] and 'text/html' in o.data]
        assert len(htmls)==1 and htmls[0].count('<table')==1
        parser=Rows(); parser.feed(htmls[0])
        assert parser.rows[1:]==[expected(label,name) for label,name in names]
        if stage=='size': assert '开场A' not in htmls[0] and '开场B' not in htmls[0]
        parts.append(htmls[0]); passed.append(f'{role} {stage}: one table, measured values correct')
    if role=='student':
        page='<!doctype html><meta charset="utf-8"><title>D4实际内核输出复查</title><style>body{font-family:sans-serif;margin:32px;line-height:1.5}section{margin-bottom:48px}h2{font-size:28px}</style>'
        page+=''.join(f'<section><h2>阶段{i+1}：课堂分别运行</h2>{h}</section>' for i,h in enumerate(parts))
        (ROOT/'.build/review-2026-10-01/d4-evidence.html').write_text(page)
result={'passed':True,'checks':passed,'scope':'Real local kernel outputs, not Windows JupyterLab GUI acceptance.',
        'design_sha256':hashlib.sha256((ROOT/'course-design.qmd').read_bytes()).hexdigest()}
(ROOT/'validation/review-evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
