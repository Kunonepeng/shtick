"""Package QA: run assertions, source alignment and PPTX structural audit.

python validation/check_package.py <pptx> <report.json>
Use a Python environment with Pillow. This is separate from visual review.
"""
from pathlib import Path
import json
import sys
import re
from zipfile import ZipFile
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'demos'))
import compression_lab as lab
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}

def audit(pptx):
    issues=[]
    def check(condition,message):
        if not condition: issues.append(message)
    # Demonstration edge cases that can invalidate the teaching conclusion.
    for source in [b'',lab.COLORS,lab.ALTERNATING,bytes([1])*256,bytes(range(256))]:
        check(lab.rle_decode(lab.rle_encode(source))==source,'RLE did not recover the input')
    for invalid in [b'\x01',b'\x01\x00']:
        try: lab.rle_decode(invalid)
        except ValueError: pass
        else: issues.append('Malformed RLE accepted')
    check(len(lab.rle_encode(lab.COLORS))==6 and len(lab.rle_encode(lab.ALTERNATING))==32,'D2 size drift')
    check(lab.predictive(lab.GRAY)['完整恢复'],'D3 readback mismatch')
    check(lab.predictive(lab.GRAY)['payload_B']==3,'D3 packing drift')
    try: lab.predictive([120,150])
    except ValueError: pass
    else: issues.append('D3 silently accepts unsupported deltas')
    check(lab.approximate(lab.GRAY)['代表值']==[120,120,124,120,120,120,120,124],'D4 values drift')
    check(lab.approximate([120,121])['代表值']==[120,120],'D4 many-to-one evidence failed')
    check(lab.approximate([255])['代表值']==[252],'D4 saturation failed')
    check(lab.video_changes()['变化格数']==4 and lab.video_changes()['完整恢复'],'Video model failed')
    manifest=json.loads((ROOT/'sources/evidence-manifest.json').read_text())
    check(manifest['D5']==json.loads(json.dumps(lab.image_evidence())),'Packaged image evidence drift')
    notebooks={}
    for role in ['teacher','student']:
        doc=json.loads((ROOT/f'demo-lab-{role}.ipynb').read_text())
        headings=[]; codes=[]
        for c in doc['cells']:
            source=''.join(c['source'])
            headings+=re.findall(r'^## (Q\d+) ',source,re.M)
            if c['cell_type']=='code':
                codes.append(source)
                check(not c.get('outputs') and c.get('execution_count') is None,f'{role} contains pre-run output')
        check(headings==[f'Q{i}' for i in range(1,11)],f'{role} Q numbering mismatch')
        check('opening(reveal=False)' in '\n'.join(codes),f'{role} initial D1 reveals equality')
        check('show_comparison_pair()' in codes, f'{role} Q7 initial cell leaks image filenames')
        check(not any('六个数据bytes' in code for code in codes),f'{role} RLE cell contains a size answer before run')
        check(any('candidate_values = []' in code for code in codes),f'{role} Q6 supplies the two original numbers in advance')
        notebooks[role]=codes
    check(notebooks['teacher'][:-1]==notebooks['student'],'Teacher/student core code drift')
    plan=json.loads((ROOT/'sources/slide-plan.json').read_text())
    with ZipFile(pptx) as z:
        presentation=ET.fromstring(z.read('ppt/presentation.xml'))
        size=presentation.find('p:sldSz',NS)
        check((size.get('cx'),size.get('cy'))==('12192000','6858000'),'Canvas size mismatch')
        slides=sorted([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml',n)],key=lambda n:int(re.search(r'slide(\d+)',n)[1]))
        check(len(slides)==len(plan),'Slide plan count differs')
        titles={};question_slides=[];note_lengths=[];fonts=set();native_tables=[]
        for i,name in enumerate(slides,1):
            xml=ET.fromstring(z.read(name)); row=plan[i-1]
            for shape in xml.findall('.//p:sp',NS):
                ident=shape.find('.//p:cNvPr',NS)
                name_=ident.get('name')
                xfrm=shape.find('p:spPr/a:xfrm',NS)
                if xfrm is not None:
                    off=xfrm.find('a:off',NS);ext=xfrm.find('a:ext',NS)
                    x,y,cx,cy=[int(v) for v in (off.get('x'),off.get('y'),ext.get('cx'),ext.get('cy'))]
                    check(x>=-2 and y>=-2 and x+cx<=12192002 and y+cy<=6858002,f'Slide {i} out of canvas: {name_}')
                    if name_=='top-rail': check((x,y,cx,cy)==(0,0,12192000,101600),f'Slide {i} top rail differs')
                    if name_=='bottom-rail': check((x,y,cx,cy)==(0,6756400,12192000,101600),f'Slide {i} bottom rail differs')
                    if name_ not in ('top-rail','bottom-rail'):
                        check(y+cy<=6255000,f'Slide {i} below content safe area: {name_}')
                if name_=='question-title':
                    signature=ET.tostring(shape)
                    if row['stage']=='question': titles[row['q']]=signature;question_slides.append((i,row['q']))
                    elif row['q'] in titles and row['stage'] not in ('conclusion','exit','exit-answer'):
                        check(signature==titles[row['q']],f'Slide {i} question geometry changed')
                if row['stage']=='question':
                    lines=shape.findall('.//a:ln/a:solidFill/a:srgbClr',NS)
                    check(not any(v.get('val')=='FF0000' for v in lines),f'Slide {i} question has red answer focus')
            for rpr in xml.findall('.//a:rPr',NS):
                for tag in ['a:latin','a:ea','a:cs']:
                    node=rpr.find(tag,NS)
                    if node is not None: fonts.add(node.get('typeface'))
                if rpr.get('sz'): check(int(rpr.get('sz'))>=2200,f'Slide {i} body text under22pt')
            note=ET.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml'))
            notes='\n'.join(n.text or '' for n in note.findall('.//a:t',NS))
            note_lengths.append(len(notes))
            check('[教师逐字稿]' in notes and len(notes)>200,f'Slide {i} notes incomplete')
            check('[问题 / 页面目的]' in notes,f'Slide {i} notes lack full purpose')
            if xml.findall('.//a:tbl',NS): native_tables.append(i)
        check([q for _,q in question_slides]==[f'Q{i}' for i in range(1,11)],'Question slide Q chain mismatch')
        check(fonts <= {'Alibaba PuHuiTi 3.0 55 Regular','Alibaba PuHuiTi 3.0 115 Black'},f'Unexpected fonts: {fonts}')
    return {'pptx':str(pptx),'slides':len(slides),'question_slides':question_slides,'native_table_slides':native_tables,'fonts':sorted(fonts),'minimum_notes_characters':min(note_lengths),'D1':lab.opening(True),'D5':lab.image_evidence(),'issues':issues,'pass':not issues}

if __name__=='__main__':
    result=audit(Path(sys.argv[1]).resolve())
    Path(sys.argv[2]).write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['pass'] else 1)
