"""Independent package checks: evidence arithmetic, file payloads, synchronization and slide pairing."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as E
import hashlib, json, re, sys, wave
from urllib.parse import urlsplit, unquote
import numpy as np
import nbformat
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'demos'))
from audio_core import quantize,codes,read_pcm,pcm_info,payload_size
checks=[]
def check(name,ok,detail=''):
    checks.append(dict(name=name,passed=bool(ok),detail=detail))
md=(ROOT/'course-design.qmd').read_text()
q_bodies={int(n):body for n,body in re.findall(r'^## Q(\d+) .+\n([\s\S]*?)(?=^## Q\d+ |^# C6)',md,re.M)}
def design_section(body,name):
    m=re.search(r'^### '+name+r'\n([\s\S]*?)(?=^### |\Z)',body,re.M)
    return m.group(1).strip() if m else ''
timing=re.findall(r'^\|Q[^|]+\|[^|]+\|(\d+)\|第(\d+)分钟\|',md,re.M)
check('45-minute budget and checkpoints',len(timing)==8 and sum(int(t) for t,_ in timing)==45 and list(np.cumsum([int(t) for t,_ in timing]))==[int(end) for _,end in timing])
opening=design_section(q_bodies[1],'投影提问')
for label,name in [('A','music-44100-16-mono.wav'),('B','music-8000-16-mono.wav')]:
    actual=(ROOT/'assets/audio'/name).stat().st_size
    check('opening actual file size '+label,f'{label}：{actual:,}B' in opening)
check('opening hides parameter answer',not re.search(r'44\.1k|8kHz|16bit|采样率',opening))
for html in [ROOT/'demos/audio-lab.html', ROOT/'exports/reference/slides.html']:
    check('offline HTML exists '+html.name,html.exists())
    if html.exists():
        for link in set(re.findall(r'(?:src|href)=[\"\x27]([^\"\x27]+)',html.read_text())):
            parsed=urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target=html.parent/unquote(parsed.path)
            check('offline dependency '+parsed.path,target.exists())
manifest=json.loads((ROOT/'assets/audio-manifest.json').read_text())
check('original audio SHA256 preserved',hashlib.sha256((ROOT/manifest['source_file']).read_bytes()).hexdigest()==manifest['source_sha256'])
for row in manifest['files']:
    p=ROOT/'assets/audio'/row['file'];info=pcm_info(p)
    check('PCM payload '+p.name,info['payload_bytes']==info['frames']*info['channels']*info['stored_bits']//8)
    check('audio metadata '+p.name,all(info[k]==row[k] for k in info))
    check('audio SHA256 '+p.name,hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'])
idx,q=quantize([-.62,-.10,.38,.84],2)
check('four-sample quantization',np.array_equal(idx,[0,1,2,3]) and np.allclose(q,[-.75,-.25,.25,.75]))
check('fixed-width codes',codes(idx,2)==['00','01','10','11'])
check('one-minute arithmetic',payload_size(44100,60,16,2)==10584000)
check('MiB conversion',round(10584000/1024**2,2)==10.09)
check('budget example',[payload_size(fs,2,16,1) for fs in [8000,16000,24000]]==[32000,64000,96000] and 64000<=64*1024<96000)
check('homework arithmetic',payload_size(22050,10,16,1)==441000 and 2**8/2**4==16)
# Bound on quantization error within the unclipped model range.
xs=np.linspace(-.99,.99,20000)
for b in [2,4,8]:
    _,z=quantize(xs,b);check(f'quantizer error bound {b}bit',np.max(np.abs(z-xs))<=1/2**b+1e-12)
for name,expected in [('tone-6000-at24000.wav',6000),('tone-alias-naive-at8000.wav',2000)]:
    fs,x=read_pcm(ROOT/'assets/audio'/name);f=np.fft.rfftfreq(len(x),1/fs);peak=f[np.argmax(np.abs(np.fft.rfft(x[:,0])))];check('tone spectral peak '+name,abs(peak-expected)<1, str(peak))
_,filtered=read_pcm(ROOT/'assets/audio/tone-lowpass-at8000.wav')
check('normal anti-alias lowpass removes 6kHz',np.sqrt(np.mean(filtered**2))<.002)
for role in ['teacher','student']:
    n=nbformat.read(ROOT/f'demo-lab-{role}.ipynb',4)
    headings=[int(m.group(1)) for c in n.cells for m in re.finditer(r'^## Q(\d+) ',c.source,re.M)]
    check(role+' notebook Q roster',headings==list(range(1,20)))
    check(role+' notebook has no saved outputs',all(not c.get('outputs') for c in n.cells if c.cell_type=='code'))
    check(role+' notebook source-hidden metadata',all(c.metadata.get('jupyter',{}).get('source_hidden') is True for c in n.cells if c.cell_type=='code'))
    check(role+' notebook Demo IDs',all(any(did in c.metadata.get('tags',[]) for c in n.cells if c.cell_type=='code') for did in ['D1','D2','D3','D4']))
    if role=='student':check('student no teacher notes/answers',all('教师逐字稿' not in c.source and '教师答案' not in c.source and '技术结论：' not in c.source for c in n.cells))
q_titles=re.findall(r'^## Q\d+ (.+)',md,re.M)
check('source 19 questions',len(q_titles)==19)
check('student-visible sampling condition', '带限信号：采样率须高于最高频率的2倍。' in md)
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
pptx=ROOT/'exports/1-2-3-audio-encoding-v3-final.pptx'
if pptx.exists():
 with ZipFile(pptx) as z:
    slides=[E.fromstring(z.read(f'ppt/slides/slide{i}.xml')) for i in range(1,41)]
    check('deck 40 slides',len([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml',n)])==40)
    for i,s in enumerate(slides,1):
        texts=[t.text or '' for t in s.findall('.//a:t',ns)]
        check('native student text no internal IDs '+str(i),not any(re.search(r'\bQ\d+(?:-A)?\b|\bD[1-4]\b',t) for t in texts))
        for sp in s.findall('.//p:sp',ns):
            for font in sp.findall('.//a:latin',ns)+sp.findall('.//a:ea',ns):
                if sp.findall('.//a:t',ns):check('font slide '+str(i),font.get('typeface','').startswith('Alibaba PuHuiTi 3.0'))
            xfrm=sp.find('p:spPr/a:xfrm',ns)
            if xfrm is not None:
                off=xfrm.find('a:off',ns);ext=xfrm.find('a:ext',ns)
                if off is not None and ext is not None:
                    x,y,cx,cy=map(int,[off.get('x'),off.get('y'),ext.get('cx'),ext.get('cy')])
                    check('canvas bounds slide '+str(i),x>=0 and y>=0 and x+cx<=12192000+5 and y+cy<=6858000+5)
        note=E.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml'))
        note_text='\n'.join(t.text or '' for t in note.findall('.//a:t',ns))
        check('speaker transcript slide '+str(i),'[教师逐字稿]' in note_text and ('[问题]' in note_text or '[页面目的]' in note_text) and len(note_text)>120)
        if 2<=i<=39:
            number=i//2
            expected_script=design_section(q_bodies[number],'提问逐字稿' if i % 2 == 0 else '教师逐字稿')
            actual_script=note_text.split('[教师逐字稿] ',1)[1].split('\n[',1)[0]
            check('current phase transcript slide '+str(i),expected_script==actual_script)
            if i % 2 == 0:
                check('question and reveal scripts differ Q'+str(number),expected_script!=design_section(q_bodies[number],'教师逐字稿'))
    # Native 48-sample quantization dots must equal the independent NumPy model.
    qs=slides[20];dots=[sp for sp in qs.findall('p:cSld/p:spTree/p:sp',ns) if (sp.find('p:nvSpPr/p:cNvPr',ns) is not None and sp.find('p:nvSpPr/p:cNvPr',ns).get('name')=='sample')]
    match=len(dots)==96
    for j,sp in enumerate(dots):
        group,k=divmod(j,48);bits=2 if group==0 else 4;x0=120 if group==0 else 690
        value=.68*np.sin(4*np.pi*k/48+.3);_,valueq=quantize([value],bits)
        xf=sp.find('p:spPr/a:xfrm',ns);off=xf.find('a:off',ns);ex=xf.find('a:ext',ns)
        cx=(int(off.get('x'))+int(ex.get('cx'))/2)/9525;cy=(int(off.get('y'))+int(ex.get('cy'))/2)/9525
        match &= abs(cx-(x0+440*k/48))<.001 and abs(cy-(390-valueq[0]*78))<.001
    check('native Q10 quantization matches 48-sample computation',match)
    for n in range(1,20):
        q,a=slides[2*n-1],slides[2*n]
        qsh=q.findall('p:cSld/p:spTree/p:sp',ns);ash=a.findall('p:cSld/p:spTree/p:sp',ns)
        stable=True
        for left,right in zip(qsh,ash):
            # Native duplicate has its own creation IDs; shape geometry and text are exact.
            for xpath in ['p:spPr','p:txBody']:
                l,r=left.find(xpath,ns),right.find(xpath,ns)
                stable &= (E.tostring(l) if l is not None else b'')==(E.tostring(r) if r is not None else b'')
        check('pair fixed geometry/text Q'+str(n),stable and len(ash)>=len(qsh))
        texts=[t.text or '' for t in q.findall('.//a:t',ns)]
        check('question title Q'+str(n),q_titles[n-1] in texts)
        check('all current givens Q'+str(n),all(line in texts for line in design_section(q_bodies[n],'投影提问').splitlines() if line))
        # No answer accents are painted on the initial question.
        colors=[x.get('val') for x in q.findall('.//a:srgbClr',ns)]
        check('question no answer/focus color Q'+str(n),all(c not in colors for c in ['FF0000','007C9B','00B0F0']))
else:check('final PPTX exists',False)
failed=[c for c in checks if not c['passed']]
result=dict(check_count=len(checks),failures=failed,passed=not failed,source_sha256=manifest['source_sha256'],pptx_sha256=hashlib.sha256(pptx.read_bytes()).hexdigest() if pptx.exists() else None)
(ROOT/'validation/package-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
sys.exit(bool(failed))
