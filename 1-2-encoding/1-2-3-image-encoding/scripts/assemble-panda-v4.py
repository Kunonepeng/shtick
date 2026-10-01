"""Preserve the reviewed native seed and assemble authoritatively planned additions."""
from pathlib import Path
import hashlib,json,re,zipfile,xml.etree.ElementTree as ET,html
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'.codex-build/panda-v4'
P='http://schemas.openxmlformats.org/presentationml/2006/main'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG='http://schemas.openxmlformats.org/package/2006/relationships'
CT='http://schemas.openxmlformats.org/package/2006/content-types'
NS={'p':P,'a':A,'r':R}
for prefix,uri in [('p',P),('a',A),('r',R)]: ET.register_namespace(prefix,uri)
def encode(tree):
    if tree.tag.startswith('{'+PKG+'}'): ET.register_namespace('',PKG)
    elif tree.tag.startswith('{'+CT+'}'): ET.register_namespace('',CT)
    return ET.tostring(tree,encoding='utf-8',xml_declaration=True)
def read_model(text):
    return json.loads(re.search(r'<!-- panda-v4-model:start -->\s*```json\s*([\s\S]*?)```',text).group(1))
def question_fields(text):
    result={}
    for match in re.finditer(r'^# (Q\d+) (.+)\n([\s\S]*?)(?=^# |\Z)',text,re.M):
        result[match[1]]={'title':match[2],**dict(re.findall(r'\*\*([^*]+)\*\*：([^\n]+)',match[3]))}
    return result
def notes_text(blob):
    t=ET.fromstring(blob)
    body=next(sp for sp in t.findall('.//p:sp',NS) if sp.find('p:nvSpPr/p:nvPr/p:ph',NS) is not None and sp.find('p:nvSpPr/p:nvPr/p:ph',NS).get('type')=='body')
    return '\n'.join(''.join(n.text or '' for n in p.findall('.//a:t',NS)) for p in body.findall('p:txBody/a:p',NS))
def write_notes(blob,text):
    t=ET.fromstring(blob)
    body=next(sp for sp in t.findall('.//p:sp',NS) if sp.find('p:nvSpPr/p:nvPr/p:ph',NS) is not None and sp.find('p:nvSpPr/p:nvPr/p:ph',NS).get('type')=='body')
    tx=body.find('p:txBody',NS)
    for child in list(tx): tx.remove(child)
    ET.SubElement(tx,f'{{{A}}}bodyPr');ET.SubElement(tx,f'{{{A}}}lstStyle')
    for line in text.splitlines():
        para=ET.SubElement(tx,f'{{{A}}}p');run=ET.SubElement(para,f'{{{A}}}r');pr=ET.SubElement(run,f'{{{A}}}rPr',{'sz':'1400'})
        for family in ['latin','ea','cs']:ET.SubElement(pr,f'{{{A}}}{family}',{'typeface':'Alibaba PuHuiTi 3.0 55 Regular'})
        ET.SubElement(run,f'{{{A}}}t').text=line
    return encode(t)
def replace_field(note,label,value):
    pattern=rf'^\[{re.escape(label)}\][^\n]*'
    return re.sub(pattern,f'[{label}] {value}',note,flags=re.M)
design=(ROOT/'course-design.qmd').read_text();model=read_model(design);fields=question_fields(design)
seed=ROOT/model['seed']
assert hashlib.sha256(seed.read_bytes()).hexdigest()==model['seed_sha256'],'Reviewed seed changed'
base_plan=json.loads((ROOT/'sources/panda-v3-slide-plan.json').read_text())
extra_plan=json.loads((OUT/'additions-plan.json').read_text())
with zipfile.ZipFile(seed) as z: files={name:z.read(name) for name in z.namelist()}
with zipfile.ZipFile(OUT/'additions.pptx') as z: extra={name:z.read(name) for name in z.namelist()}
notes={};plan=[];order=[]
# Current pedagogical fields update the spoken script only when the page is that main question.
for entry in base_plan['slides']:
    n=entry['slide'];q=entry['q'];key=f'ppt/notesSlides/notesSlide{n}.xml';note=notes_text(files[key]);f=fields.get(q,{})
    if entry['title']==f.get('title') and entry['stage'] in ('question','answer'):
        label='提问页教师逐字稿' if entry['stage']=='question' else '揭示页教师逐字稿'
        if label in f: note=replace_field(note,'教师逐字稿',f[label])
        for lab,source in [('下一问','下一问'),('技术注解','技术边界')]:
            if source in f: note=replace_field(note,lab,f[source])
    note=replace_field(note,'内部编号',entry.get('task_id',q)+' / '+entry['stage'])
    note=note.replace('panda-v3-audit.md','panda-v4-audit.md').replace('.codex-build/panda-data.json','.codex-build/panda-v4/data.json')
    if n==63:note=replace_field(note,'教师逐字稿','课后完成这三题。第一题写判断最少固定码长的不等式，第二题列式并写单位，第三题用原始信息解释。这是补充作业；刚才的E1已在课堂独立收答。答案保留在教师材料，学生完成后再核对。')
    if n in model['optional_base_slides']:note+='\n[45分钟路径] 可选页，默认跳过本问及其揭示；加课时才保留思考和反馈。'
    for cp in model['checkpoints']:
        if n==cp['after']:note+=f"\n[下一步] 进入{cp['id']}，先收集学生总结和证据，再逐枝更新知识树。"
    notes[n]=note;files[key]=write_notes(files[key],note)
    order.append(n);plan.append({**entry,'base_slide':n,'optional':n in model['optional_base_slides'],'withheld':'答案、后续结论与教师参考' if entry['stage']=='question' else '后续问题答案','focus':entry['visible'],'tree_checkpoint':None})
    for new in [e for e in extra_plan if e['after']==n]:
        new_number=63+new['extra'];order.append(new_number);plan.append({**new,'slide':None,'base_slide':None,'optional':False,'tree_checkpoint':new['q'] if new['q'].startswith('T') else None})
        notes[new_number]=notes_text(extra[f"ppt/notesSlides/notesSlide{new['extra']}.xml"])
# New pages contain explicit native shapes and no external media dependencies.
content=ET.fromstring(files['[Content_Types].xml']);rels=ET.fromstring(files['ppt/_rels/presentation.xml.rels']);pres=ET.fromstring(files['ppt/presentation.xml']);slide_ids=pres.find('p:sldIdLst',NS)
base_ids={i+1:child for i,child in enumerate(list(slide_ids))}
for e in extra_plan:
    k=e['extra'];n=63+k
    for kind in ['slides','notesSlides']:
        stem='slide' if kind=='slides' else 'notesSlide'
        src=f'ppt/{kind}/{stem}{k}.xml';dst=f'ppt/{kind}/{stem}{n}.xml';files[dst]=extra[src]
        sr=f'ppt/{kind}/_rels/{stem}{k}.xml.rels';dr=f'ppt/{kind}/_rels/{stem}{n}.xml.rels';t=ET.fromstring(extra[sr])
        for rel in t:
            typ=rel.get('Type').split('/')[-1]
            if typ=='notesSlide':rel.set('Target',f'../notesSlides/notesSlide{n}.xml')
            elif typ=='slide':rel.set('Target',f'../slides/slide{n}.xml')
            elif typ=='slideLayout':rel.set('Target','../slideLayouts/slideLayout1.xml')
            elif typ=='notesMaster':rel.set('Target','../notesMasters/notesMaster1.xml')
            else:raise ValueError(f'Unexpected addition relationship: {typ}')
        files[dr]=encode(t)
        ET.SubElement(content,f'{{{CT}}}Override',{'PartName':'/'+dst,'ContentType':f'application/vnd.openxmlformats-officedocument.presentationml.{"slide" if kind=="slides" else "notesSlide"}+xml'})
    rid=f'rIdPandaV4{n}';ET.SubElement(rels,f'{{{PKG}}}Relationship',{'Id':rid,'Type':R+'/slide','Target':f'slides/slide{n}.xml'})
    base_ids[n]=ET.Element(f'{{{P}}}sldId',{'id':str(256+n),f'{{{R}}}id':rid})
for child in list(slide_ids):slide_ids.remove(child)
for n in order:slide_ids.append(base_ids[n])
files['ppt/presentation.xml']=encode(pres);files['ppt/_rels/presentation.xml.rels']=encode(rels);files['[Content_Types].xml']=encode(content)
if 'docProps/app.xml' in files:
    t=ET.fromstring(files['docProps/app.xml'])
    for child in t:
        if child.tag.endswith('}Slides'):child.text=str(len(order))
    files['docProps/app.xml']=encode(t)
with zipfile.ZipFile(OUT/'candidate.pptx','w',zipfile.ZIP_DEFLATED) as z:
    for name in sorted(files):z.writestr(name,files[name])
for index,(e,part) in enumerate(zip(plan,order),1):e['slide']=index;e['part_slide']=part;e['notes']=notes[part];e['evidence']=e.get('source') or ('course-design.qmd C4a '+e['q'] if e['tree_checkpoint'] else 'course-design.qmd E1');e['activity_distribution']={13:'A: Q6/T1, Q7-read, T2, Q15/Q16',56:'B: Q18/T3 and Q21/T4',74:'E1: independent exit assessment'}.get(index)
mapping={e['base_slide']:e['slide'] for e in plan if e['base_slide'] is not None}
pairs=[[mapping[a],mapping[b]] for a,b in base_plan['pairs']]
for q in ['T1','T2','T3','T4','E1']:
    pages=[e['slide'] for e in plan if e['q']==q];pairs.extend([[a,b] for a,b in zip(pages,pages[1:])])
(OUT/'slide-plan.json').write_text(json.dumps({'slides':plan,'pairs':pairs,'order':order,'base_mapping':mapping},ensure_ascii=False,indent=2))
# Reveal uses version-bound final rendering: one static page per PPTX build, with matching notes.
header='''---\npagetitle: "图像编码：熊猫v4参考"\nlang: zh-CN\nformat:\n  revealjs:\n    width: 1280\n    height: 720\n    transition: none\n    slide-number: true\n    embed-resources: true\n    margin: 0\n    background-color: "#FFFFFF"\n---\n'''
sections=[]
for e in plan:
    reference_notes='\n'.join(line.rstrip() for line in e['notes'].splitlines())
    sections.append(f"\n## {{background-image=\".codex-build/panda-v4/render/slide-{e['slide']:02}.png\" background-size=\"contain\"}}\n\n<!-- page={e['slide']} q={e['q']} stage={e['stage']} -->\n\n::: notes\n{reference_notes}\n:::\n")
(ROOT/'slides.qmd').write_text(header+''.join(sections))
(OUT/'assembly.json').write_text(json.dumps({'slide_count':len(plan),'seed_sha256':model['seed_sha256'],'candidate_sha256':hashlib.sha256((OUT/'candidate.pptx').read_bytes()).hexdigest(),'visible_seed_slide_parts_unchanged':63,'base_mapping':mapping},indent=2))
print(json.dumps({'slides':len(plan),'pairs':len(pairs),'candidate':str(OUT/'candidate.pptx')}))
