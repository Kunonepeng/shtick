"""Verify rendered student sheets withhold later answers and exit parameters."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'.codex-build/panda-v4'
class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__();self.skip=0;self.text=[];self.resources=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'):self.skip+=1
        fields=dict(attrs)
        if tag in ('script','img','link'):
            for key in ('src','href'):
                if key in fields and not fields[key].startswith(('data:','#')):self.resources.append(fields[key])
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.skip-=1
    def handle_data(self,value):
        if not self.skip:self.text.append(value)
master=(ROOT/'activities/panda-v4-student.md').read_text()
records={};texts={}
for key in ('a','b','exit'):
    source=ROOT/f'activities/panda-v4-student-{key}.md'
    html=ROOT/f'exports/activities-panda-v4/activities/panda-v4-student-{key}.html'
    body=re.search(rf'<!-- stage-{key}:start -->\s*([\s\S]*?)\s*<!-- stage-{key}:end -->',master).group(1)
    assert source.read_text().endswith(body+'\n'),key
    parser=VisibleText();parser.feed(html.read_text());assert not parser.resources,parser.resources
    texts[key]=' '.join(' '.join(parser.text).split())
    records[key]={'source':str(source.relative_to(ROOT)),'html':str(html.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'html_sha256':hashlib.sha256(html.read_bytes()).hexdigest()}
assert '11 11 01 00 00 01 11 00' not in texts['a']
assert '11 11 01 00 00 01 11 00' in texts['b']
assert '12×10' not in texts['a']+texts['b']
assert '12×10' in texts['exit']
assert not re.search(r'45\s*B|最少3\s*bit|至少3\s*bit',texts['exit'])
assert not (ROOT/'exports/activities-panda-v4/activities/panda-v4-student.html').exists(),'Unstaged master must not be in student exports'
record={'status':'pass','date':'2026-10-01','sheets':records,'distribution':{'a':'Q6','b':'Q18','exit':'E1 page 74'},'no_early_q7_answer_or_exit_data':True,'generated_sources_match_master':True,'external_runtime_resources':[],'browser_layout_evidence':'panda-v4-audit.md: all three views inspected in Codex in-app browser','physical_printing':'unverified'}
(OUT/'activity-check.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'pass','student_sheets':3,'later_data_withheld':True}))
