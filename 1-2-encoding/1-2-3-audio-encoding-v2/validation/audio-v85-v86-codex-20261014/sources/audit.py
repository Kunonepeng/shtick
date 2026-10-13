"""Independently audit PPTX structures and classroom counting models."""
import hashlib,json,math,posixpath,re,sys,os
from collections import Counter
from decimal import Decimal
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as E
from PIL import Image
R=Path(os.environ.get('AUDIO_BUILD_DIR',str(Path(__file__).parent.parent)));stem=sys.argv[1];plan=json.loads((R/f'{stem}-plan.json').read_text());deck=R/f'{stem}-candidate.pptx'
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
checks=[]
def check(name,ok,evidence):checks.append({'check':name,'status':'pass'if ok else'fail','evidence':evidence})
def text(n):return '\n'.join(''.join(v.text or ''for v in par.findall('.//a:t',ns))for par in n.findall('.//a:p',ns)).strip()
def target(base,t):return t.lstrip('/')if t.startswith('/')else posixpath.normpath(posixpath.dirname(base)+'/'+t)
def box(n):
 x=n.find('p:spPr/a:xfrm',ns)
 if x is None:return None
 o=x.find('a:off',ns);e=x.find('a:ext',ns)
 return [int(v)/9525 for v in [o.get('x'),o.get('y'),e.get('cx'),e.get('cy')]]
def approx(a,b):return abs(a-b)<.002
with ZipFile(deck)as z:
 pr=E.fromstring(z.read('ppt/presentation.xml'));rels=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'));rm={v.get('Id'):target('ppt/presentation.xml',v.get('Target'))for v in rels};paths=[rm[v.get('{'+ns['r']+'}id')]for v in pr.find('p:sldIdLst',ns)]
 check('Slide count and canvas',len(paths)==plan['slideCount']and pr.find('p:sldSz',ns).attrib=={'cx':'12191695','cy':'6858000'},[len(paths),pr.find('p:sldSz',ns).attrib])
 slides={};nodes={}
 for loc,name in zip(plan['slides'],paths):
  root=E.fromstring(z.read(name));objs=[v for v in root.findall('p:cSld/p:spTree/*',ns)if v.tag.rsplit('}',1)[-1]in('sp','pic')];slides[loc['key']]=objs;nodes[loc['key']]=root
  def named(name):return next((o for o in objs if o.find('.//p:cNvPr',ns).get('name')==name),None)
  for rail,y in [('top-rail',0),('bottom-rail',709.333333)]:
   o=named(rail);b=box(o);check(f"p{loc['page']} {rail}",all(approx(v,w)for v,w in zip(b,[0,y,1279.967979,10.666667])),b)
  title=named('question-title');b=box(title);check(f"p{loc['page']} title baseline",all(approx(v,w)for v,w in zip(b[:3],[63.84,222 if loc['key']in ['p1','p38']else 63.84,1152])),b)
  check(f"p{loc['page']} canvas bounds",all((b:=box(o))is None or(b[0]>=-.1 and b[1]>=-.1 and b[0]+b[2]<=1280.1 and b[1]+b[3]<=720.1)for o in objs),'All owned shapes/images within canvas')
  fonts=[v.get('typeface')for v in root.findall('.//a:latin',ns)+root.findall('.//a:ea',ns)+root.findall('.//a:cs',ns)];check(f"p{loc['page']} explicit font families",bool(fonts)and all(v in ['Alibaba PuHuiTi 3.0 55 Regular','Alibaba PuHuiTi 3.0 115 Black']for v in fonts),sorted(set(fonts)))
  relpath=posixpath.join(posixpath.dirname(name),'_rels',posixpath.basename(name)+'.rels');rels=E.fromstring(z.read(relpath));nt=next(v.get('Target')for v in rels if v.get('Type').endswith('/notesSlide'));notes=text(E.fromstring(z.read(target(name,nt))));check(f"p{loc['page']} stage transcript",'[问题]'in notes and text(title)in notes and '[教师逐字稿]'in notes,notes[:130])
 def name(o):return o.find('.//p:cNvPr',ns).get('name')
 def named(k,n):return next(o for o in slides[k]if name(o)==n)
 def signatures(k):
  out=Counter()
  for o in slides[k]:
   c=E.fromstring(E.tostring(o));meta=c.find('.//p:cNvPr',ns);meta.attrib.pop('id',None);meta.attrib.pop('name',None)
   for child in list(meta):meta.remove(child)
   # Relationship IDs may change on duplicated images, so compare native geometry and text separately.
   if c.tag.endswith('pic'):
    out[('image',tuple(box(c)or[]),E.tostring(c.find('p:blipFill/a:srcRect',ns))if c.find('p:blipFill/a:srcRect',ns)is not None else b'')]+=1
   else:out[('shape',E.tostring(c))]+=1
  return out
 pairs=[('p8','p8-reveal'),('p12','p12-reveal'),('p16','p16-reveal'),('p17','p18'),('p22','p22-reveal'),('p24','p24-reveal'),('p31','p31-reveal'),('p61','p61-reveal'),('p66','p66-reveal')]
 for a,b in pairs:
  if a in slides and b in slides:check(f'Stable duplicated reveal {a} -> {b}',not(signatures(a)-signatures(b)),'Question native objects remain identical in the reveal; one additional evidence focus')
 for a,b in [('p32','p33'),('p40','p41'),('p42','p45'),('p50','p51'),('p64','p65'),('p69','p70')]:
  q=[(text(o),box(o))for o in slides[a]if text(o)and name(o)!='question-title' and (box(o)or[0,1000])[1]<330]
  ans=[(text(o),box(o))for o in slides[b]if text(o)and name(o)!='question-title' and (box(o)or[0,1000])[1]<330]
  check(f'Exercise givens stable {a} -> {b}',q==ans,[q,ans])
 check('Source conceptual sequence retained',all(f'p{i}'in slides for i in range(1,78)),[s['key']for s in plan['slides']])
 # Model checks use actual exported positions, rather than importing author functions.
 q=slides['p24-reveal'];vals=[Decimal(v)for v in ['3.71','5.2','7.1','6.4','4.15','2.3','.65','1.4','3.2','4.8']]
 for bits,y in [(3,286),(4,466)]:
  for j,v in enumerate(vals):
   raw=box(named('p24-reveal',f'raw-{bits}-{j}'));rep=box(named('p24-reveal',f'quantized-{bits}-{j}'));step=Decimal(8)/(2**bits);level=int(v//step);rv=(Decimal(level)+Decimal('.5'))*step
   check(f'Input {bits}bit sample {j}',approx(raw[0]+raw[2]/2,370+j*804/9)and approx(raw[1]+raw[3]/2,y+110*(1-float(v)/8)),[float(v),raw])
   check(f'Midpoint {bits}bit sample {j}',approx(rep[0]+rep[2]/2,370+j*804/9)and approx(rep[1]+rep[3]/2,y+110*(1-float(rv)/8)),[float(rv),rep])
  check(f'{bits}bit grid levels',sum(name(o).startswith(f'rep-grid-{bits}-')for o in q)==2**bits,'8 and 16 same-range levels')
 check('Neutral L3 question',not any(name(o)in ['selected-L3','raw-3.71','representative-3.5']for o in slides['p17']),'No answer marker in question')
 check('3.71 caption occurs once',sum(text(o)=='采样原值：3.71'for o in slides['p17'])==1 and sum(text(o)=='采样原值：3.71'for o in slides['p18'])==1,'Question and reveal each one original-value caption')
 check('PCM counting grid',sum(name(o).startswith('pcm-cell-')for o in slides['p31-reveal'])==8 and sum(name(o).startswith('pcm-time-')for o in slides['p31-reveal'])==4,'4 instants x 2 channels x 2 bytes = 16 bytes')
 for key,need in [('p33','160,000'),('p41','11,520,000'),('p51','6,912,000,000')]:check(f'Worked result {key}',any(need in text(o)for o in slides[key]),need)
 check('Independent PCM/video arithmetic',16000*5*2*(8//8)==160000 and 48000*60*2*(16//8)==11520000 and 480*320*(24//8)*25*600==6912000000,{'audio_MiB':11520000/1024**2,'video_GiB':6912000000/1024**3})
 check('Zoom sample times',sum(name(o).startswith('zoom-sample-')for o in slides['p12-reveal'])==11,'11 points j=15..25, observing closed 0.30..0.50s window')
 for j in range(15,26):
  b=box(named('p12-reveal',f'zoom-sample-{j}'));tm=j/50;check(f'Zoom exact sample {j}',approx(b[0]+b[2]/2,750+430*(tm-.3)/.2)and approx(b[1]+b[3]/2,420-105*.72*math.sin(10*math.pi*tm+.3)),tm)
 # Earlier native tree branches keep their exact geometry through the staged builds.
 tree=['p35','p36','p37','p72','p73','p74'];prev=[]
 for k in tree:
  cur=[(name(o),text(o),box(o))for o in slides[k]if name(o).startswith(('tree-node-','tree-label-','tree-edge-'))]
  check(f'Knowledge tree remains editable {k}',bool(cur)and not any(o.tag.endswith('pic')for o in slides[k]),len(cur))
  check(f'Knowledge tree established geometry {k}',all(v in cur for v in prev),len(prev));prev=cur
 check('JPEG assets preserved byte-for-byte',all(hashlib.sha256((R/'assets'/f).read_bytes()).hexdigest()in [hashlib.sha256(z.read(n)).hexdigest()for n in z.namelist()if n.startswith('ppt/media/')]for f in ['original-rgb.png','jpeg-quality3-decoded.png']),['Original PNG asset bytes in PPTX'])
 if stem=='v86':
  for rate,y in [(8,320),(20,492)]:
   check(f'Sampling density count {rate}Hz',sum(name(o).startswith(f'density-sample-{rate}-')for o in slides['p14'])==rate,rate)
   for j in range(rate):
    b=box(named('p14',f'density-sample-{rate}-{j}'));tm=j/rate;check(f'Sampling density exact point {rate}Hz {j}',approx(b[0]+b[2]/2,350+826*tm)and approx(b[1]+b[3]/2,y-50*.72*math.sin(4*math.pi*tm+.1)),tm)
  check('Sampling density safe body',all((box(o)or[0,720])[1]>=156 for o in slides['p14']if name(o)not in ['top-rail','bottom-rail','question-title']),'All body objects start at or below y=166')
  for a,b in [('p22-reveal','p22-error'),('p31-reveal','p31-formula'),('p66-reveal','p66-pixel')]:check(f'Additional focus retains geometry {a} -> {b}',not(signatures(a)-signatures(b)),'Duplicate base retained exactly')
  a=box(named('p22-error','error-bar-3bit'));b=box(named('p22-error','error-bar-4bit'));check('Error comparison common scale',approx(a[2]/b[2],float(Decimal('.21')/Decimal('.04'))),[a[2],b[2]])
  for key in ['p40','p41']:check(f'Binary size unit {key}',all('MB'not in text(o)for o in slides[key])and any('MiB'in text(o)for o in slides[key]),'MiB retained in question and answer')
  a=Image.open(R/'assets/original-rgb.png').convert('RGB');b=Image.open(R/'assets/jpeg-quality3-decoded.png').convert('RGB');v1=a.getpixel((230,140));v2=b.getpixel((230,140));check('JPEG exact pixel proof',v1==(79,113,165)and v2==(51,108,153)and any('(79,113,165)'in text(o)for o in slides['p66-pixel'])and any('(51,108,153)'in text(o)for o in slides['p66-pixel']),[v1,v2])
  check('Formula linked to storage width',any('存储位宽'in text(o)for o in slides['p31-formula']),[text(o)for o in slides['p31-formula']if name(o)=='pcm-general-formula'])
  for j in range(5):check(f'25fps timestamp {j}',text(named('p48',f'frame-time-{j}'))==f'{j/25:.2f} s',j/25)
  for ch,y in [(0,292),(1,484)]:
   o=named('p44',f'mixed-signal-{ch}');xf=box(o);pts=o.findall('p:spPr/a:custGeom/a:pathLst/a:path/*',ns);xy=[]
   for pt in pts:
    v=pt.find('a:pt',ns)
    if v is not None:xy.append((int(v.get('x'))/9525+xf[0],int(v.get('y'))/9525+xf[1]))
   check(f'Mix output native waveform {ch}',len(xy)==181,len(xy))
for name,expected in json.loads((R/'pre-authoring-plan.json').read_text())['sources'].items():
 f=Path('/Users/chran/repo/shtick/1-2-encoding/1-2-3-audio-encoding-v2')/('1-2-3-audio-encoding-v8.1.codex.pptx'if name=='v81'else'1-2-3-audio-encoding-v8.4.10.pptx');check(f'Original preserved {name}',hashlib.sha256(f.read_bytes()).hexdigest()==expected,expected)
failed=[v for v in checks if v['status']=='fail'];out={'deck':deck.name,'sha256':hashlib.sha256(deck.read_bytes()).hexdigest(),'checks':checks,'passed':len(checks)-len(failed),'failed':len(failed),'classroom_apps':'unverified','notebook_execution':'not applicable: unchanged outside deck-only scope'};(R/f'{stem}-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({'passed':out['passed'],'failed':failed},ensure_ascii=False));sys.exit(bool(failed))
