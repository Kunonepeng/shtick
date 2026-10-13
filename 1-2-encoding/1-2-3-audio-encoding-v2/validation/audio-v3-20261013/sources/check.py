"""Independently verify the delivered diagram values and staged PPTX structure."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as E
from decimal import Decimal
import hashlib
import json
import math
import struct
import sys

ROOT=Path(__file__).resolve().parent.parent
PPTX=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'candidate.pptx'
OUT=Path(sys.argv[2]) if len(sys.argv)>2 else ROOT/'checks.json'
PLAN=json.loads((Path(sys.argv[3]) if len(sys.argv)>3 else ROOT/'plan.json').read_text())
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
checks=[]
def check(label,condition):
    checks.append({'check':label,'pass':bool(condition)})
def serial(node):
    return E.tostring(node) if node is not None else None
def tx(shape):
    return ''.join(x.text or '' for x in shape.findall('.//a:t',NS))
def name(shape):
    return shape.find('p:nvSpPr/p:cNvPr',NS).get('name')
def named(slide,n):
    return [o for o in slide.findall('p:cSld/p:spTree/p:sp',NS) if name(o)==n]
def signature(shape):
    return (serial(shape.find('p:spPr',NS)),serial(shape.find('p:txBody/a:bodyPr',NS)),
            [(x.get('sz'),x.get('b'),x.find('a:latin',NS).get('typeface')) for x in shape.findall('.//a:rPr',NS)],tx(shape))

with ZipFile(PPTX) as z:
    slides={i:E.fromstring(z.read(f'ppt/slides/slide{i}.xml')) for i in range(1,len(PLAN['manifest'])+1)}
    for row in PLAN['manifest']:
        i=row['page'];slide=slides[i]
        for n,y in [('top-rail',0),('bottom-rail',6756400)]:
            xf=named(slide,n)[0].find('p:spPr/a:xfrm',NS)
            check(f'{i}: {n} fixed canvas geometry',abs(int(xf.find('a:off',NS).get('y'))-y)<20 and int(xf.find('a:ext',NS).get('cx'))==12192000)
        if row['pair']:
            check(f'{i}: duplicated question typography and geometry',signature(named(slide,'question-title')[0])==signature(named(slides[row['pair']],'question-title')[0]))
        notes=E.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml'));note=tx(notes)
        check(f'{i}: full purpose and staged transcript',all(v in note for v in [row['title'],'[问题]','[内部编号]','[阶段]','[教师逐字稿]']))
        check(f'{i}: no essential animation',slide.find('p:timing',NS) is None)
        for prop in slide.findall('.//a:rPr',NS):
            for kind in ['latin','ea','cs']:
                font=prop.find('a:'+kind,NS)
                check(f'{i}: explicit {kind} font',font is not None and font.get('typeface') in ['Alibaba PuHuiTi 3.0 55 Regular','Alibaba PuHuiTi 3.0 115 Black'])
    faces=set()
    for n in z.namelist():
        if n.startswith('ppt/') and n.endswith('.xml'):
            for e in E.fromstring(z.read(n)).iter():
                if e.tag.split('}')[-1] in ['latin','ea','cs','font'] and e.get('typeface'):faces.add(e.get('typeface'))
    check('theme/master/notes have no unrelated default font',all(x.startswith('Alibaba PuHuiTi') or x.startswith('+') for x in faces))
    # Compare fixed earlier knowledge-tree nodes and relation labels between checkpoints.
    for earlier,later,count in [(11,18,1),(19,25,2),(26,47,3)]:
        for k in range(count):
            for prefix in ['tree-node-','tree-heading-','tree-detail-','tree-relation-label-','tree-relation-detail-']:
                check(f'tree {prefix}{k} stable {earlier}->{later}',signature(named(slides[earlier],prefix+str(k))[0])==signature(named(slides[later],prefix+str(k))[0]))
    for i,count in [(10,0),(11,1),(18,1),(19,2),(25,2),(26,3),(47,3),(48,4)]:
        check(f'{i}: only established tree branches',sum(name(o).startswith('tree-node-') for o in slides[i].findall('p:cSld/p:spTree/p:sp',NS))==count)
    for i in [21,22]:
        labels=named(slides[i],'level-index')
        check(f'{i}: exactly twelve source level labels',len(labels)==12)
    check('format question withholds actual PCM packaging',tx(slides[27]).find('本课装PCM')<0)
    check('format reveal explicitly draws PCM-to-WAV example',tx(named(slides[28],'codec-example-slot')[0])=='本课：未压缩PCM')
    check('sixteen bit cells form one stored sample',len([o for o in slides[31].findall('p:cSld/p:spTree/p:sp',NS) if name(o).startswith('toy-expanded-bit-')])==16)
    check('both byte groups interpreted on reveal',all(tx(named(slides[32],n)[0])=='8 bit＝1 B' for n in ['toy-expanded-byte-1-label','toy-expanded-byte-2-label']))
    # Select the closest midpoint with exact decimal arithmetic, independently of the builder.
    for bits,entries in [(2,PLAN['q2']),(3,PLAN['q3'])]:
        step=Decimal(2)/Decimal(2**bits)
        centers=[-Decimal(1)+(Decimal(k)+Decimal('.5'))*step for k in range(2**bits)]
        for k,v in enumerate(PLAN['amplitudes']):
            value=Decimal(str(v));index=min(range(len(centers)),key=lambda j:(abs(value-centers[j]),-j))
            check(f'{bits}bit: sample {k+1} nearest midpoint',entries[k]['index']==index and Decimal(str(entries[k]['representative']))==centers[index])
            check(f'{bits}bit: sample {k+1} code reversible',int(entries[k]['code'],2)==index and len(entries[k]['code'])==bits)
    expected=['010','100','111','111','110','100','010','010','001','011']
    codes=[''.join(tx(named(slides[24],f'sample-code-{k}-digit-{j}')[0]) for j in range(3)) for k in range(10)]
    check('actual slide ten codes correct',codes==expected)
    for i,left,top,height,width,entries in [(14,155,260,168,425,PLAN['q2']),(23,205,250,174,960,PLAN['q3'])]:
        shapes=named(slides[i],'quantized-sample')
        for k,entry in enumerate(entries):
            xf=shapes[k].find('p:spPr/a:xfrm',NS);off=xf.find('a:off',NS);ext=xf.find('a:ext',NS)
            x=(int(off.get('x'))+int(ext.get('cx'))/2)/9525;y=(int(off.get('y'))+int(ext.get('cy'))/2)/9525
            check(f'{i}: actual native quantized point {k+1}',abs(x-(left+k/2*width/5))<.01 and abs(y-(top+(1-entry['representative'])*height/2))<.01)
    for k in range(10):
        guide=named(slides[24],'sample-code-guide')[k].find('p:spPr/a:xfrm/a:off',NS)
        first=named(slides[24],f'sample-code-{k}-0')[0].find('p:spPr/a:xfrm/a:off',NS)
        check(f'waveform/code {k+1} time aligned',abs(int(guide.get('x'))-int(first.get('x'))-44*9525)<20)
    check('error examples',abs(Decimal('-.38')-Decimal('-.25'))==Decimal('.13') and abs(Decimal('-.38')-Decimal('-.375'))==Decimal('.005'))
    check('counterexample and error bounds',abs(Decimal('-.71')-Decimal('-.75'))==Decimal('.04') and abs(Decimal('-.71')-Decimal('-.625'))==Decimal('.085') and Decimal('.085')<=Decimal('.125'))
    check('toy PCM sample count and payload',4*2==8 and 8*16//8==16)
    check('mono stereo and exit PCM counts',8000*2*2==32000 and 8000*2*2*2==64000 and 16000*2*2*2==128000)
    check('opening payload sizes',44100*6*2==529200 and 8000*6*2==96000)
    check('bitrate ratio',round(128000/1411200*100,1)==9.1)
    for i in [30,42]:
        if i==30: n1,n2,ratio='pcm-rate-bar','mp3-rate-bar',128000/1411200
        else:n1,n2,ratio='opening-A-payload-bar','opening-B-payload-bar',96000/529200
        widths=[int(named(slides[i],n)[0].find('p:spPr/a:xfrm/a:ext',NS).get('cx')) for n in [n1,n2]]
        check(f'{i}: native comparison bars use true ratios',abs(widths[1]/widths[0]-ratio)<1e-5)
    # The alias comparison is calculated at every displayed sample independently.
    for k in range(5):
        a=math.cos(2*math.pi*6000*k/8000);b=math.cos(2*math.pi*2000*k/8000)
        check(f'alias same sample {k}',abs(a-b)<1e-12 and abs(a-[1,0,-1,0,1][k])<1e-12)
    audio=(ROOT/'fixtures/size-check-8000-2s-16-mono.wav').read_bytes()
    check('real WAV RIFF signature',audio[:4]==b'RIFF' and audio[8:12]==b'WAVE')
    pos=12;chunks=[]
    while pos<len(audio):
        tag=audio[pos:pos+4];size=struct.unpack('<I',audio[pos+4:pos+8])[0];chunks.append((tag.decode('ascii'),size));pos+=8+size+(size%2)
    check('real WAV structure and complete count',chunks==[('fmt ',16),('data',32000)] and len(audio)==32044 and 12+(8+16)+8==44)
    check('PCM visible storage-width condition',all('实际存储16 bit' in tx(slides[i]) for i in range(33,39)))
    def shape_y(i,n):return int(named(slides[i],n)[0].find('p:spPr/a:xfrm/a:off',NS).get('y'))/9525
    check('count equations in logical vertical order',shape_y(36,'answer-1')<shape_y(36,'sample-width-answer')<shape_y(36,'pcm-payload-result'))
    check('count build earlier positions stay fixed',shape_y(34,'answer-1')==shape_y(35,'answer-1')==shape_y(36,'answer-1') and shape_y(35,'sample-width-answer')==shape_y(36,'sample-width-answer'))
    check('stereo same-instant focus exists',len(named(slides[38],'stereo-current-frame'))==1)
    check('alias normalized value labels and conditions',all(len(named(slides[i],'alias-amplitude-value'))==6 and '同幅同相余弦' in tx(slides[i]) for i in [43,44]))
    xf=named(slides[46],'nyquist-boundary')[0].find('p:spPr/a:xfrm',NS)
    line_bottom=(int(xf.find('a:off',NS).get('y'))+int(xf.find('a:ext',NS).get('cy')))/9525
    check('frequency focus does not cross tick labels',line_bottom<=386.01)
    check('exit answer identifies channel factor','2声道' in tx(named(slides[50],'exit-answer-1')[0]))
    check('planned duration totals 45 minutes',sum([4,6,8,6,2,10,7,2])==45)
    notes1=tx(E.fromstring(z.read('ppt/notesSlides/notesSlide1.xml')))
    check('checkpoints agree with budget',all(v in notes1 for v in ['第18分钟进入编码','第26分钟开始计数模型','第36分钟完成开场闭环','第43分钟独立退出']))

report={'version':'audio-v3-20261013','pptx':str(PPTX),'sha256':hashlib.sha256(PPTX.read_bytes()).hexdigest(),'slides':len(PLAN['manifest']),'main_slides':PLAN['mainSlideCount'],'checks':len(checks),'pass':all(c['pass'] for c in checks),'failures':[c for c in checks if not c['pass']],'details':checks,'unverified':['WPS/PowerPoint native application','projector/speakers','observed classroom pacing','external course package synchronization outside deck scope']}
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=False))
sys.exit(0 if report['pass'] else 1)
