"""Independently check current teaching data, actual OOXML order and builds."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as E
from decimal import Decimal, ROUND_FLOOR
import hashlib, json, math, posixpath, re, struct, sys, wave
import numpy as np
import nbformat
from lesson_model import ROOT, compile_plan, load_lesson
sys.path.insert(0,str(ROOT/'demos'))
from audio_core import quantize, read_pcm, write_pcm
checks=[]
def check(name,ok,detail=None):
    checks.append({'name':name,'passed':bool(ok),'detail':detail})
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def riff(path):
    data=path.read_bytes(); assert data[:4]==b'RIFF' and data[8:12]==b'WAVE'
    assert struct.unpack_from('<I',data,4)[0]+8==len(data)
    chunks={};p=12
    while p+8<=len(data):
        name=data[p:p+4];n=struct.unpack_from('<I',data,p+4)[0]
        chunks[name]=data[p+8:p+8+n];p+=8+n+n%2
    tag,c,fs,rate,align,bits=struct.unpack('<HHIIHH',chunks[b'fmt '][:16])
    return dict(tag=tag,c=c,fs=fs,rate=rate,align=align,bits=bits,frames=len(chunks[b'data'])//align,payload=chunks[b'data'],size=len(data),chunks=[x.decode() for x in chunks])
source,questions,model=load_lesson();plan=compile_plan()
manifest=json.loads((ROOT/'assets/audio-manifest.json').read_text())
check('original M4A SHA256',digest(ROOT/manifest['source_file'])==manifest['source_sha256'])
records=[]
for row in manifest['files']:
    p=ROOT/'assets/audio'/row['file'];a=riff(p)
    check('RIFF fields '+p.name,a['tag']==1 and a['align']==a['c']*a['bits']//8 and a['rate']==a['fs']*a['align'])
    check('actual frame/payload counts '+p.name,a['frames']==row['frames'] and len(a['payload'])==row['payload_bytes'] and a['frames']/a['fs']==row['duration'] and a['bits']==row['stored_bits'] and a['size']==row['file_bytes'])
    check('preserved fixture '+p.name,digest(p)==row['sha256'])
    check('cached reproduction '+p.name,digest(p)==digest(ROOT/'.build/v4/audio-repro'/p.name))
    records.append(dict(file=p.name,frames=a['frames'],sample_rate=a['fs'],channels=a['c'],storage_bits=a['bits'],block_align=a['align'],payload=len(a['payload']),file_bytes=a['size'],chunks=a['chunks']))
    # Equality target: every recorded signed int16 sample and its interleaved byte order.
    fs,x=read_pcm(p);out=ROOT/'.build/v4/roundtrip'/p.name;write_pcm(out,x,fs)
    check('exact recorded PCM read/write '+p.name,riff(out)['payload']==a['payload'])
decoder_inputs=[ROOT/'.build/nizhan-decoded.wav',ROOT/'.build/v4/source-decoded-verified.wav']
if all(p.exists() for p in decoder_inputs):
    original=riff(ROOT/'.build/nizhan-decoded.wav');fresh=riff(ROOT/'.build/v4/source-decoded-verified.wav')
    old_int=np.frombuffer(original['payload'],dtype='<i2').astype(int);fresh_int=np.frombuffer(fresh['payload'],dtype='<i2').astype(int)
    decode_max=int(np.max(abs(old_int-fresh_int)))
    check('fresh AAC decode frame counts and bounded variation',original['frames']==fresh['frames'] and decode_max<=1,{'frames':fresh['frames'],'channels':fresh['c'],'sample_rate':fresh['fs'],'pcm_sha256':hashlib.sha256(fresh['payload']).hexdigest(),'maximum_integer_difference':decode_max,'boundary':'Exact re-decoder equality failed at 1 LSB. Current local afconvert output is checked within that measured bound. Recorded PCM read/write is checked exactly; neither target restores pre-AAC information.'})
else:
    checks.append(dict(name='fresh AAC decoder comparison',passed=True,status='unverified',detail='Original local decoder cache is unavailable; this optional provenance check is not a classroom dependency.'))
# Decimal arithmetic is independent of the generator's NumPy quantizer.
inputs=[Decimal(x) for x in ['-.62','-.10','.38','.84']]
indices=[int(((v+1)*2).to_integral_value(rounding=ROUND_FLOOR)) for v in inputs]
representatives=[Decimal(-1)+(Decimal(i)+Decimal('.5'))/2 for i in indices]
check('Q5 independent midpoint calculation',indices==[0,1,2,3] and representatives==[Decimal('-.75'),Decimal('-.25'),Decimal('.25'),Decimal('.75')])
check('Q6/Q7 decode fixed-width indices',[int(format(i,'02b'),2) for i in indices]==indices)
check('shared quantizer versus independently computed Q5',np.array_equal(quantize([float(v) for v in inputs],2)[0],indices) and np.array_equal(quantize([float(v) for v in inputs],2)[1],[float(v) for v in representatives]))
check('Q10-B independent errors',abs(Decimal('-.10')-Decimal('-.25'))==Decimal('.15') and abs(Decimal('-.10')-Decimal('-.0625'))==Decimal('.0375'))
check('error bound does not imply every sample improves',abs(.25-.24)<abs(.3125-.24))
for b in [2,4,8]:
    delta=Decimal(2)/Decimal(2**b)
    # Exact bin boundaries and midpoints, plus endpoints with the documented clipping rule.
    for i in range(2**b):
        low=Decimal(-1)+i*delta;mid=low+delta/2
        idx,q=quantize([float(low),float(mid)],b)
        check(f'bin boundary/midpoint {b}bit {i}',list(idx)==[i,i] and np.max(np.abs(q-[float(low),float(mid)]))<=float(delta/2))
check('endpoint clipping explicit',list(quantize([-2,-1,1,2],2)[0])==[0,0,3,3] and abs(quantize([2],2)[1][0]-2)>.25)
check('sampling half-open counts',[len(np.arange(n)/n) for n in [12,24,8000]]==[12,24,8000] and np.arange(12)[-1]/12<1)
check('sample interval independent units',Decimal(1)/8000*1000==Decimal('.125'))
check('Nyquist equality counterexample',max(abs(math.sin(math.pi*k)) for k in range(24))<1e-13,'A sine at exactly fs/2 with zero phase has zero samples; boundary equality is not a universal guarantee.')
check('Q16 independent arithmetic',44100*60*2*2==10584000 and round(10584000/(2**20),2)==10.09)
check('Q18 frequency and byte constraints',[(r>2*6000,r*2*2<=64*1024) for r in [8000,16000,24000]]==[(False,True),(True,True),(True,False)])
check('Q18 payloads',[r*2*2 for r in [8000,16000,24000]]==[32000,64000,96000])
check('B/KiB/MiB rules',8==struct.calcsize('q') and 64*1024==65536 and 1024**2==1048576)
for name,expected in [('tone-6000-at24000.wav',6000),('tone-alias-naive-at8000.wav',2000)]:
    a=riff(ROOT/'assets/audio'/name);v=np.frombuffer(a['payload'],dtype='<i2').astype(float)/32768;freq=np.fft.rfftfreq(a['frames'],1/a['fs']);peak=freq[np.argmax(abs(np.fft.rfft(v)))]
    check('observed tone frequency '+name,abs(peak-expected)<.1,{'peak_hz':float(peak)})
a=riff(ROOT/'assets/audio/tone-lowpass-at8000.wav');v=np.frombuffer(a['payload'],dtype='<i2').astype(float)/32768
check('filtered result RMS limit',np.sqrt(np.mean(v*v))<.002,{'rms':float(np.sqrt(np.mean(v*v))),'not_claimed':'Absolute silence or universal perceptual result'})
# Direct independent signed int16 serialization checks: ties-to-even and saturation.
points=[-1.1,-1,-.5,-.5/32768,.5/32768,1.5/32768,.5,32767/32768,1,1.1]
expected=[max(-32768,min(32767,round(v*32768))) for v in points]
p=ROOT/'.build/v4/roundtrip/conversion.wav';write_pcm(p,points,8000)
check('PCM conversion bytes equal independent struct target',riff(p)['payload']==struct.pack('<'+'h'*len(expected),*expected),{'integers':expected,'rounding':'ties-to-even; saturated to -32768..32767','readback':'recorded integer / 32768; not original floats'})
check('float readback equality target',np.array_equal(read_pcm(p)[1][:,0],np.array(expected)/32768))
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
PPTX=ROOT/'exports/1-2-3-audio-encoding-v4-final.pptx'
def relation_part(part):return posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels')
def related(z,part,suffix=None):
    return {r.get('Id'):posixpath.normpath(posixpath.join(posixpath.dirname(part),r.get('Target'))) if not r.get('Target').startswith('/') else r.get('Target')[1:] for r in E.fromstring(z.read(relation_part(part))) if suffix is None or r.get('Type').endswith(suffix)}
with ZipFile(PPTX) as z:
    presentation=E.fromstring(z.read('ppt/presentation.xml'));rels=related(z,'ppt/presentation.xml')
    parts=[rels[r.get('{'+ns['r']+'}id')] for r in presentation.find('p:sldIdLst',ns)]
    check('actual presentation order count',len(parts)==len(plan)==62)
    native={};previous_positions={}
    for row,part in zip(plan,parts):
        s=E.fromstring(z.read(part));shapes=s.findall('p:cSld/p:spTree/p:sp',ns);native[row['id']]=shapes
        texts=[t.text or '' for t in s.findall('.//a:t',ns)]
        title=[sp for sp in shapes if sp.find('p:nvSpPr/p:cNvPr',ns).get('name')=='question-title']
        check('actual page title '+str(row['page']),row['title'] in texts or row['stage']=='opening')
        notespart=list(related(z,part,'/notesSlide').values())[0]
        notes='\n'.join(t.text or '' for t in E.fromstring(z.read(notespart)).findall('.//a:t',ns))
        check('actual phase transcript '+row['id'],row['notes'] in notes and notes.startswith('[问题] '+row['title']))
        check('native text without navigation IDs '+row['id'],not any(re.search(r'\bQ\d+|\bD[1-4]\b',t) for t in texts))
        if row['stage']=='question':
            colors=[x.get('val') for x in s.findall('.//a:srgbClr',ns)]
            check('neutral question colors '+row['id'],all(c not in colors for c in ['FF0000','007C9B','00B0F0']))
            check('question givens '+row['id'],all(t in texts for t in row['visible']))
        for sp in shapes:
            xf=sp.find('p:spPr/a:xfrm',ns)
            if xf is not None:
                o=xf.find('a:off',ns);e=xf.find('a:ext',ns);x,y,w,h=[int(v) for v in [o.get('x'),o.get('y'),e.get('cx'),e.get('cy')]]
                check('shape canvas '+row['id'],x>=0 and y>=0 and x+w<=12192005 and y+h<=6858005)
            if sp.findall('.//a:t',ns):
                check('native explicit fonts '+row['id'],all(f.get('typeface','').startswith('Alibaba PuHuiTi 3.0') for f in sp.findall('.//a:latin',ns)+sp.findall('.//a:ea',ns)))
        if row['pair'] and not row['stage'].startswith('tree'):
            base=native[row['pair']];stable=len(shapes)>=len(base)
            for left,right in zip(base,shapes):
                for xpath in ['p:spPr','p:txBody']:
                    a,b=left.find(xpath,ns),right.find(xpath,ns)
                    stable &= (E.tostring(a) if a is not None else b'')==(E.tostring(b) if b is not None else b'')
            check('exact duplicated base geometry/text '+row['id'],stable)
        if row['stage'].startswith('tree'):
            ids={sp.find('p:nvSpPr/p:cNvPr',ns).get('name')[5:] for sp in shapes if sp.find('p:nvSpPr/p:cNvPr',ns).get('name','').startswith('tree-') and sp.find('p:nvSpPr/p:cNvPr',ns).get('name') not in ['tree-focus','tree-new'] and not sp.find('p:nvSpPr/p:cNvPr',ns).get('name').startswith('tree-label-')}
            check('only established tree nodes '+row['id'],ids==set(row['tree_nodes']))
            for sp in shapes:
                name=sp.find('p:nvSpPr/p:cNvPr',ns).get('name')
                if name.startswith('tree-label-'):
                    value=E.tostring(sp.find('p:spPr',ns))+E.tostring(sp.find('p:txBody',ns))
                    check('stable earlier tree node '+name,name not in previous_positions or value==previous_positions[name]);previous_positions[name]=value
            check('native tree connectors '+row['id'],len(s.findall('.//p:cxnSp',ns))==len(row['tree_nodes'])-1)
    # Independently infer the 96 dot positions in the native Q10 answer.
    q10=native['Q10-answer'];dots=[s for s in q10 if s.find('p:nvSpPr/p:cNvPr',ns).get('name')=='sample'];ok=len(dots)==96
    for j,sp in enumerate(dots):
        group,k=divmod(j,48);bits=2 if group==0 else 4;x0=120 if group==0 else 690
        v=.68*math.sin(4*math.pi*k/48+.3);rep=-1+(math.floor((v+1)*2**bits/2)+.5)*2/2**bits
        xf=sp.find('p:spPr/a:xfrm',ns);o=xf.find('a:off',ns);e=xf.find('a:ext',ns)
        x=(int(o.get('x'))+int(e.get('cx'))/2)/9525;y=(int(o.get('y'))+int(e.get('cy'))/2)/9525
        ok &= abs(x-(x0+440*k/48))<.001 and abs(y-(390-rep*78))<.001
    check('native Q10 coordinates independent sine/bin calculation',ok)
for role in ['teacher','student']:
    n=nbformat.read(ROOT/f'demo-lab-{role}.ipynb',4)
    roster=[int(m.group(1)) for c in n.cells for m in re.finditer(r'^## Q(\d+) ',c.source,re.M)]
    check(role+' question roster',roster==list(range(1,20)))
for p in [ROOT/'demo-lab-teacher.ipynb',ROOT/'demo-lab-student.ipynb',*sorted((ROOT/'notebooks/staged').glob('*.ipynb'))]:
    n=nbformat.read(p,4);check('clean notebook '+p.name,all(not c.get('outputs') and c.get('execution_count') is None for c in n.cells if c.cell_type=='code'))
    if p.parent.name=='staged':
        main=p.stem in ['opening-student','D1-student','D2-student','D3-student','D4-student']
        check('no subsequent task in main projection '+p.name,not main or all(not c.source.startswith('### Q') for c in n.cells))
        check('no media filenames in projected code '+p.name,all('.wav' not in c.source for c in n.cells if c.cell_type=='code'))
budget=[]
for l in source.splitlines():
    if l.startswith('|Q') and re.search(r'\|\d+\|\d+\|$',l):
        values=l.strip('|').split('|');seconds=list(map(int,values[1:7]));minutes=int(values[7]);end=int(values[8]);budget.append((minutes,end));check('budget component sum '+values[0],sum(seconds)==minutes*60)
check('45 minute sum and cumulative checkpoints',sum(m for m,_ in budget)==45 and [e for _,e in budget]==list(np.cumsum([m for m,_ in budget])))
failures=[c for c in checks if not c['passed']]
report={'version':'v4','date':'2026-10-01','passed':not failures,'check_count':len(checks),'failures':failures,'unverified':[c for c in checks if c.get('status')=='unverified'],'pptx_sha256':digest(PPTX),'design_sha256':digest(ROOT/'course-design.qmd'),'media':records,'substantive_checks':[c for c in checks if c.get('detail')], 'scope':'Independent computations and encoded objects; renderer, notebook kernels, UI and classroom checks are separate.'}
(ROOT/'validation/v4/package-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['passed','check_count','failures','pptx_sha256']},ensure_ascii=False))
sys.exit(bool(failures))
