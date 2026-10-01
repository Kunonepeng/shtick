"""Verify the reference's actual embedded images and stage-specific notes."""
from pathlib import Path
from html.parser import HTMLParser
import base64,hashlib,json,re
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'.codex-build/panda-v4'
class ReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__();self.sections=[];self.notes=[];self.inside=False;self.skip=0;self.resources=[]
    def handle_starttag(self,tag,attrs):
        fields=dict(attrs)
        if tag=='section' and 'slide' in fields.get('class','').split():self.sections.append(fields)
        if tag=='aside' and 'notes' in fields.get('class','').split():self.inside=True;self.notes.append([])
        if tag in ('style','script'):self.skip+=1
        for key in ('src','data-background-image'):
            if key in fields and not fields[key].startswith('data:'):self.resources.append(fields[key])
    def handle_data(self,value):
        if self.inside and not self.skip:self.notes[-1].append(value)
    def handle_endtag(self,tag):
        if tag=='aside':self.inside=False
        if tag in ('style','script'):self.skip-=1
path=ROOT/'exports/reference-panda-v4/slides.html'
parser=ReferenceParser();parser.feed(path.read_text())
plan=json.loads((OUT/'slide-plan.json').read_text())['slides']
assert len(parser.sections)==len(parser.notes)==len(plan)==77
assert not parser.resources,parser.resources
normalize=lambda value:re.sub(r'\s+',' ',value).strip()
for index,(section,note,entry) in enumerate(zip(parser.sections,parser.notes,plan),1):
    image=base64.b64decode(section['data-background-image'].split(',',1)[1])
    assert image==(OUT/f'render/slide-{index:02}.png').read_bytes(),index
    assert normalize(''.join(note))==normalize(entry['notes']),(index,'Notes changed in rendering')
result={'status':'pass','date':'2026-10-01','html':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'stages':77,'embedded_images_match_final_render':77,'notes_match_pptx_plan':77,'external_runtime_resources':parser.resources,'browser_check':'Codex in-app browser: cover, T1 summary, T4 final tree, E1 question; slide counter and navigation checked','target_classroom_browser':'unverified'}
(OUT/'reference-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
