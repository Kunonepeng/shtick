"""Independently validate image evidence, native edits, and staged disclosure."""
from pathlib import Path
from collections import Counter
import json,re,zipfile,hashlib,xml.etree.ElementTree as ET,math,importlib.util
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'.codex-build/panda-v4'
A='http://schemas.openxmlformats.org/drawingml/2006/main';P='http://schemas.openxmlformats.org/presentationml/2006/main';NS={'a':A,'p':P}
text=(ROOT/'course-design.qmd').read_text();model=json.loads(re.search(r'<!-- panda-v4-model:start -->\s*```json\s*([\s\S]*?)```',text).group(1));data=json.loads((OUT/'data.json').read_text());plan=json.loads((OUT/'slide-plan.json').read_text())
# Use pixel loops rather than the builder's array reshape/reduction.
p=model['data'];im=Image.open(ROOT/p['source']).convert('RGB');pixels=im.load();x,y,w,h=p['crop'];palette=p['palette_rgb'];means={};matrices={}
for n in (8,16):
    cell_w,cell_h=w//n,h//n;grid=[]
    for row in range(n):
        grid_row=[]
        for col in range(n):
            sums=[0,0,0]
            for yy in range(y+row*cell_h,y+(row+1)*cell_h):
                for xx in range(x+col*cell_w,x+(col+1)*cell_w):
                    rgb=pixels[xx,yy]
                    for channel in range(3):sums[channel]+=rgb[channel]
            grid_row.append([value/(cell_w*cell_h) for value in sums])
        grid.append(grid_row)
    means[n]=grid
    for levels in (4,6):
        matrices[n,levels]=[''.join(str(min(range(levels),key=lambda i:sum((rgb[c]-palette[i][c])**2 for c in range(3)))) for rgb in row) for row in grid]
for n in (8,16):
    assert max(abs(a-b) for row1,row2 in zip(means[n],data['means'+str(n)]) for rgb1,rgb2 in zip(row1,row2) for a,b in zip(rgb1,rgb2))<1e-12
assert matrices[8,4]==data['coarse'];assert matrices[16,4]==data['fine'];assert matrices[16,6]==data['six']
assert list(pixels[422,230])==[138,179,111]
assert data['pixel']['binary']==['10001010','10110011','01101111']
assert data['fine'][5][4:12]=='33100130'
assert '3310'+'0130'=='33'+'10'+'01'+'30'=='33100130'
assert 8*8*2//8==16 and 16*16*2//8==64 and 16*16*3//8==96
assert 500*333*24//8==499500 and round(499500/1024,2)==487.79
assert (12*10*3)//8==45 and 2**2<5<=2**3
assert [n for n,(width,height,bits) in zip('ABCD',[(16,16,2),(16,8,2),(16,16,1),(8,8,2)]) if 2**bits>=4 and width*height*bits<=32*8]==['B','D']
# Compare the optional demo's own distance function across all supported states.
spec=importlib.util.spec_from_file_location('panda_demo',ROOT/'demos/panda-digitization/panda_digitization_demo.py');demo_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(demo_module)
demo=json.loads((ROOT/'demos/panda-digitization/panda_samples.json').read_text())
for n in (8,16):
    assert demo['grids'][str(n)]==means[n]
    for levels in (4,6):
        rows=[''.join(str(demo_module.nearest_palette(rgb,palette[:levels])[0]) for rgb in row) for row in demo['grids'][str(n)]]
        assert rows==matrices[n,levels]
# Check the matrices preserved in the pedagogical source.
for heading,key in [('8×8四色','coarse'),('16×16四色','fine'),('16×16六色','six')]:
    section=text.split('## '+heading,1)[1].split('\n## ',1)[0];rows=re.findall(r'^([0-5]{8,16})$',section,re.M);assert rows==data[key],heading
candidate=OUT/'candidate.pptx';final=ROOT/'exports/1-2-3-image-encoding-panda-v4.pptx';artifact=final if final.exists() else candidate;seed=ROOT/model['seed']
with zipfile.ZipFile(candidate) as z: trial_files={name:z.read(name) for name in z.namelist()}
with zipfile.ZipFile(artifact) as z: final_files={name:z.read(name) for name in z.namelist()}
assert trial_files==final_files,'Candidate and delivered OOXML parts differ'
with zipfile.ZipFile(candidate) as z:files={name:z.read(name) for name in z.namelist()}
with zipfile.ZipFile(seed) as z:base={name:z.read(name) for name in z.namelist()}
assert len(plan['slides'])==77
for i in range(1,64):assert files[f'ppt/slides/slide{i}.xml']==base[f'ppt/slides/slide{i}.xml']
for name in base:
    if name.startswith('ppt/media/'):assert files[name]==base[name]
allowed={'Alibaba PuHuiTi 3.0 115 Black','Alibaba PuHuiTi 3.0 55 Regular'}
roots={e['slide']:ET.fromstring(files[f"ppt/slides/slide{e['part_slide']}.xml"]) for e in plan['slides']}
def geometry(child):
    xf=child.find('.//a:xfrm',NS)
    if xf is None:xf=child.find('.//p:xfrm',NS)
    return None if xf is None else (xf.attrib,[(n.tag,n.attrib) for n in xf])
for first,last in plan['pairs']:
    a=list(roots[first].find('p:cSld/p:spTree',NS));b=list(roots[last].find('p:cSld/p:spTree',NS))
    assert len(b)>=len(a),(first,last)
    ga=Counter(json.dumps(geometry(child),sort_keys=True) for child in a if geometry(child) is not None)
    gb=Counter(json.dumps(geometry(child),sort_keys=True) for child in b if geometry(child) is not None)
    assert not (ga-gb),(first,last,'geometry')
    # Match the actual title instead of z-order: new connectors are exported behind shapes.
    title=plan['slides'][first-1]['title']
    def find_title(children):
        return next(c for c in children if ''.join(n.text or '' for n in c.findall('.//a:t',NS))==title)
    ta,tb=find_title(a),find_title(b)
    assert geometry(ta)==geometry(tb) and ET.tostring(ta.find('p:txBody',NS))==ET.tostring(tb.find('p:txBody',NS)),(first,last,'title')
font_names=set();note_scripts={};connector_counts={};small_captions=[]
for e in plan['slides']:
    t=roots[e['slide']]
    for family in t.findall('.//a:latin',NS)+t.findall('.//a:ea',NS)+t.findall('.//a:cs',NS):
        name=family.get('typeface');font_names.add(name);assert name in allowed,name
    for run in t.findall('.//a:r',NS):
        props=run.find('a:rPr',NS);visible=run.find('a:t',NS)
        if props is not None and visible is not None and visible.text:
            size=int(props.get('sz','0'))/100
            if size<22:
                assert size==16.5 and visible.text=='概念示意',(e['slide'],size,visible.text)
                small_captions.append({'slide':e['slide'],'text':visible.text,'pt':size,'role':'Nonessential concept-diagram caption'})
    for xf in t.findall('.//a:xfrm',NS)+t.findall('.//p:xfrm',NS):
        off=xf.find('a:off',NS);ext=xf.find('a:ext',NS)
        if off is not None and ext is not None:
            xx,yy=int(off.get('x')),int(off.get('y'));ww,hh=int(ext.get('cx')),int(ext.get('cy'));assert xx>=0 and yy>=0 and xx+ww<=12192001 and yy+hh<=6858001,(e['slide'],xx,yy,ww,hh)
    nt=ET.fromstring(final_files[f"ppt/notesSlides/notesSlide{e['part_slide']}.xml"])
    body=next(sp for sp in nt.findall('.//p:sp',NS) if sp.find('p:nvSpPr/p:nvPr/p:ph',NS) is not None and sp.find('p:nvSpPr/p:nvPr/p:ph',NS).get('type')=='body')
    note='\n'.join(''.join(n.text or '' for n in para.findall('.//a:t',NS)) for para in body.findall('p:txBody/a:p',NS))
    assert note==e['notes'],(e['slide'],'Actual notes differ from the plan')
    assert note.startswith('[问题 / 页面目的]') and '[教师逐字稿]' in note
    script=re.search(r'\[教师逐字稿\]\s*(.*?)(?=\n\[|\Z)',note,re.S).group(1);assert len(script)>25
    note_scripts[e['slide']]=script
    if e['tree_checkpoint']:
        connector_counts[e['slide']]=len(t.findall('.//p:cxnSp',NS));assert connector_counts[e['slide']]==e['nodes']
        names=[n.get('name') for n in t.findall('.//p:cNvPr',NS)];node_ids=[name[5:] for name in names if name and name.startswith('node-')];assert node_ids==[n['id'] for n in model['nodes'][:e['nodes']]],(e['slide'],node_ids)
        assert not t.findall('.//p:pic',NS)
for first,last in plan['pairs']:assert note_scripts[first]!=note_scripts[last],(first,last,'same spoken script')
# Verify the actual native pixel rectangles in the delivered base, not only JSON fixtures.
def grid_colors(base_page,gx,gy,size,n):
    page=next(e['slide'] for e in plan['slides'] if e['base_slide']==base_page);found={}
    for shape in roots[page].findall('.//p:sp',NS):
        xf=shape.find('p:spPr/a:xfrm',NS)
        if xf is None:continue
        off=xf.find('a:off',NS);ext=xf.find('a:ext',NS)
        if off is None or ext is None:continue
        xx,yy=int(off.get('x'))/9525,int(off.get('y'))/9525;ww,hh=int(ext.get('cx'))/9525,int(ext.get('cy'))/9525
        c,r=round((xx-gx)/size),round((yy-gy)/size)
        if 0<=r<n and 0<=c<n and abs(xx-(gx+c*size))<.01 and abs(yy-(gy+r*size))<.01 and abs(ww-size)<.01 and abs(hh-size)<.01:
            color=shape.find('p:spPr/a:solidFill/a:srgbClr',NS);assert color is not None;found[r,c]=color.get('val').upper()
    assert len(found)==n*n,(base_page,len(found))
    return [''.join(str(data['palette'].index('#'+found[r,c])) for c in range(n)) for r in range(n)]
assert grid_colors(16,105,215,48,8)==data['coarse'];assert grid_colors(16,745,215,24,16)==data['fine'];assert grid_colors(22,745,205,24,16)==data['six']
# Read the rendered native reconstruction cells back into exactly the recorded codewords.
def read_native_rectangle(base_page,gx,gy,columns,rows):
    page=next(e['slide'] for e in plan['slides'] if e['base_slide']==base_page);cells={}
    for shape in roots[page].findall('.//p:sp',NS):
        xf=shape.find('p:spPr/a:xfrm',NS);color=shape.find('p:spPr/a:solidFill/a:srgbClr',NS)
        if xf is None or color is None:continue
        off=xf.find('a:off',NS);ext=xf.find('a:ext',NS)
        xx,yy=int(off.get('x'))/9525,int(off.get('y'))/9525
        col,row=round((xx-gx)/40),round((yy-gy)/40)
        if 0<=col<columns and 0<=row<rows and abs(xx-gx-col*40)<.01 and abs(yy-gy-row*40)<.01 and int(ext.get('cx'))==40*9525 and int(ext.get('cy'))==40*9525:
            cells[row,col]=data['palette'].index('#'+color.get('val').upper())
    assert len(cells)==columns*rows
    return ' '.join(format(cells[r,c],'02b') for r in range(rows) for c in range(columns))
recorded_codewords='11 11 01 00 00 01 11 00'
reconstructions=[read_native_rectangle(51,210,440,4,2),read_native_rectangle(51,840,440,2,4),read_native_rectangle(52,990,310,4,2)]
assert reconstructions==[recorded_codewords]*3,reconstructions
old_demo=json.loads((ROOT/'references/panda-samples-pre-v4.json').read_text())
rounded_differences={}
for n,levels in [(8,4),(16,4),(16,6)]:
    old=[''.join(str(demo_module.nearest_palette(rgb,palette[:levels])[0]) for rgb in row) for row in old_demo['grids'][str(n)]]
    rounded_differences[f'{n}x{n}/{levels}']=sum(a!=b for row_a,row_b in zip(old,matrices[n,levels]) for a,b in zip(row_a,row_b))
assert list(rounded_differences.values())==[0,0,0]
mse={}
for levels in (4,6):
    mse[levels]=sum((rgb[c]-palette[int(matrices[16,levels][r][col])][c])**2 for r,row in enumerate(means[16]) for col,rgb in enumerate(row) for c in range(3))/(16*16*3)
assert round(mse[4],2)==281.17 and round(mse[6],2)==192.27
assert round(100*(mse[4]-mse[6])/mse[4],2)==31.62
assert means[16][9][12]==[78.25,73.31481481481481,68.39814814814815]


# Reference sections preserve the exact order and reveal stages.
reference=(ROOT/'slides.qmd').read_text();tags=re.findall(r'page=(\d+) q=(\w[\w-]*) stage=(\w+)',reference);assert tags==[(str(e['slide']),e['q'],e['stage']) for e in plan['slides']]
report={'status':'pass','artifact':str(artifact.relative_to(ROOT)),'artifact_sha256':hashlib.sha256(artifact.read_bytes()).hexdigest(),'candidate_parts_equal_delivered':True,'candidate_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),'slides':77,'pairs':len(plan['pairs']),'fonts':sorted(font_names),'normal_body_minimum_pt':22,'small_caption_exceptions':small_captions,'unchanged_seed_visible_parts':63,'tree_connector_counts':connector_counts,'independent_method':'Pillow RGB decode plus integer channel sums per block; independently inspect native pixel fills and geometry','rgb':[138,179,111],'payload_B':[16,64,96],'Q16_B':499500,'Q16_KiB':round(499500/1024,2),'exit_B':45,'demo_states_checked':4,'native_decoding_roundtrips':reconstructions,'rounded_fixture_differences':rounded_differences,'Q9_RGB_MSE':mse,'Q9_MSE_reduction_percent':round(100*(mse[4]-mse[6])/mse[4],2),'kernel_check':'not applicable: current lesson uses native PPTX and optional Tk, no Jupyter','classroom_apps':'unverified','projection_and_pacing':'unverified'}
(OUT/'technical-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False))
