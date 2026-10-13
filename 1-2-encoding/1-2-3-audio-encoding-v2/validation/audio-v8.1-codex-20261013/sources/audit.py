"""Check the final native slide evidence independently of its authoring code."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as E
from decimal import Decimal
import collections, hashlib, json, math, posixpath, sys, zlib, random

PPTX=Path(sys.argv[1]);OUT=Path(sys.argv[2]);PLAN=Path(sys.argv[3])
plan=json.loads(PLAN.read_text())
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
FONT={'Alibaba PuHuiTi 3.0 55 Regular','Alibaba PuHuiTi 3.0 115 Black'}
checks=[]
def check(label,passed):checks.append({'check':label,'pass':bool(passed)})
def text(node):return ''.join(o.text or '' for o in node.findall('.//a:t',NS))
def shape_name(o):
 n=o.find('p:nvSpPr/p:cNvPr',NS)
 return n.get('name') if n is not None else ''
def named(slide,name):return [o for o in slide.findall('p:cSld/p:spTree/p:sp',NS) if shape_name(o)==name]
def box(o):
 xf=o.find('p:spPr/a:xfrm',NS);a=xf.find('a:off',NS);b=xf.find('a:ext',NS)
 return tuple(int(v)/9525 for v in [a.get('x'),a.get('y'),b.get('cx'),b.get('cy')])
def center(o):
 x,y,w,h=box(o);return x+w/2,y+h/2
def signature(o):
 return tuple(E.tostring(node) if node is not None else b'' for node in [o.find('p:spPr',NS),o.find('p:txBody',NS)])
def target(base,value):return value.lstrip('/') if value.startswith('/') else posixpath.normpath(posixpath.dirname(base)+'/'+value)
with ZipFile(PPTX) as z:
 pr=E.fromstring(z.read('ppt/presentation.xml'));rels=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))
 mapping={r.get('Id'):target('ppt/presentation.xml',r.get('Target')) for r in rels}
 paths=[mapping[v.get('{'+NS['r']+'}id')] for v in pr.find('p:sldIdLst',NS)]
 slides=[E.fromstring(z.read(n)) for n in paths]
 check('slide count matches accepted plan',len(slides)==plan['slideCount'])
 by_source={v.get('source_page',v['page']):slides[v['page']-1] for v in plan['manifest'] if v.get('source_page',v['page']) is not None}
 check('all seventy source pages retained',set(range(1,71)).issubset(by_source))
 for i,s in enumerate(slides,1):
  for name,y in [('top-rail',0),('bottom-rail',709.333333)]:
   x,top,w,h=box(named(s,name)[0]);check(f'{i}: {name} edge and height',abs(x)<.01 and abs(top-y)<.01 and abs(w-1279.967979)<.01 and abs(h-10.666667)<.01)
  title=named(s,'question-title')[0];x,y,w,h=box(title)
  check(f'{i}: title baseline',abs(x-63.84)<.01 and (abs(y-63.84)<.01 or abs(y-222)<.01))
  for rp in s.findall('.//a:rPr',NS):
   for kind in ['latin','ea','cs']:
    v=rp.find('a:'+kind,NS);check(f'{i}: explicit {kind} font',v is not None and v.get('typeface') in FONT)
  check(f'{i}: no shadow',s.find('.//a:outerShdw',NS) is None)
  check(f'{i}: no animation needed',s.find('p:timing',NS) is None)
  relpath=posixpath.join(posixpath.dirname(paths[i-1]),'_rels',posixpath.basename(paths[i-1])+'.rels')
  sr=E.fromstring(z.read(relpath));note_target=next(r.get('Target') for r in sr if r.get('Type').endswith('/notesSlide'))
  note=E.fromstring(z.read(target(paths[i-1],note_target)))
  check(f'{i}: full purpose and transcript',all(v in text(note) for v in ['[问题]',text(title),'[教师逐字稿]']))
 for q,a in [(32,33),(37,38),(39,42),(47,48),(61,62),(66,67)]:
  sq,sa=by_source[q],by_source[a]
  check(f'practice {q}/{a}: title unchanged',signature(named(sq,'question-title')[0])==signature(named(sa,'question-title')[0]))
  check(f'practice {q}/{a}: givens unchanged',signature(named(sq,'practice-givens')[0])==signature(named(sa,'practice-givens')[0]))
 s=by_source[13]
 for rate in [1,2]:
  points=[o for o in s.findall('p:cSld/p:spTree/p:sp',NS) if shape_name(o).startswith(f'sample-{rate}-')]
  check(f'{rate}Hz: one-second point count',len(points)==rate)
  for j,o in enumerate(points):
   tm=(center(o)[0]-235)/840
   check(f'{rate}Hz: actual time {j}',abs(tm-j/rate)<1e-5 and 0<=tm<1)
 check('one-second interval is half open','[0,1)' in text(s))
 s=by_source[18];edges=[box(named(s,f'quant-bin-{j}')[0]) for j in range(8)]
 left=edges[0][0];total=edges[-1][0]+edges[-1][2]-left
 for name,v in [('raw-3.71',Decimal('3.71')),('representative-3.5',Decimal('3.5'))]:
  actual=(center(named(s,name)[0])[0]-left)/total*8
  check(f'quantizer: native {name} coordinate',abs(actual-float(v))<1e-5)
 check('quantizer: independent bin and midpoint',int(Decimal('3.71'))==3 and (Decimal(3)+Decimal(4))/2==Decimal('3.5'))
 check('packing model and actual PCM distinguished','连续打包' in text(by_source[30]) and '不是实际16bit' in text(by_source[30]))
 check('practice 1 independent payload',16000*5*2*8//8==160000 and '160,000' in text(by_source[33]))
 check('practice 2 independent payload and MiB',48000*60*2*16//8==11520000 and round(11520000/1024**2,2)==10.99 and '11,520,000' in text(by_source[38]))
 check('practice 4 independent frame count and GiB',480*320*24//8==460800 and 25*600==15000 and 460800*15000==6912000000 and round(6912000000/1024**3,2)==6.44)
 if plan['stage']>=2:
  for n,expected in [(2,1),(65,2)]:check(f'{n}: generated images embedded',len(by_source[n].findall('p:cSld/p:spTree/p:pic',NS))==expected)
  check('code mapping first sample focus',len(named(by_source[19],'first-sample-focus'))==1 and '011' in text(by_source[19]))
  check('sixteen stored bits have two byte labels',all(named(by_source[26],n) for n in ['stored-byte-1','stored-byte-2','stored-sample-bytes']))
  s=by_source[43]
  for group,count in [(0,6),(1,3)]:check(f'channel {group}: actual sample count',sum(shape_name(o).startswith(f'channel-sample-{group}-') for o in s.findall('p:cSld/p:spTree/p:sp',NS))==count)
  check('channel pair has same-instant focus',len(named(s,'same-instant-stereo'))==1)
  s=by_source[56]
  for k,size in [(0,17),(1,1011)]:
   ratio=box(named(s,f'compressed-bar-{k}')[0])[2]/box(named(s,f'original-bar-{k}')[0])[2]
   check(f'compression {k}: native common-scale ratio',abs(ratio-size/1000)<1e-6)
  check('repeated-data zlib result and recovery',len(zlib.compress(b'A'*1000))==17 and zlib.decompress(zlib.compress(b'A'*1000))==b'A'*1000)
  rng=random.Random(2026);fixture=bytes(rng.randrange(256) for _ in range(1000));check('complex-data zlib result and recovery',len(zlib.compress(fixture))==1011 and zlib.decompress(zlib.compress(fixture))==fixture)
  check('PCM factors multiply rather than imply sequence',len(named(by_source[31],'multiply-sign'))==1 and '存储位宽' in text(by_source[31]))
  check('image/audio comparison has subject headings',all(named(by_source[44],n) for n in ['image-column-heading','audio-column-heading']))
 if plan['stage']>=3:
  tree_entries=[v for v in plan['manifest'] if v.get('tree_level') is not None]
  check('progressive tree levels', [v['tree_level'] for v in tree_entries]==[0,1,2,3,3,4,5])
  previous={}
  for entry in tree_entries:
   s=slides[entry['page']-1];level=entry['tree_level']
   check(f"tree {entry['page']}: established nodes only", sum(shape_name(o).startswith('tree-node-') for o in s.findall('p:cSld/p:spTree/p:sp',NS))==level)
   for k in range(1,level+1):
    for kind in ['node','detail','link']:
     name=f'tree-{kind}-{k}';shape=named(s,name)[0];sig=signature(shape)
     if name in previous:check(f"tree {entry['page']}: {name} fixed",sig==previous[name])
     previous[name]=sig
   if level:check(f"tree {entry['page']}: root native and cue beyond color",bool(named(s,'tree-root')) and ('本次新增' in text(s) or (level==3 and text(named(s,'question-title')[0]).startswith('用证据'))))
  first=[slides[v['page']-1] for v in tree_entries[:4]]
  check('first tree prompts and titles duplicated',all(signature(named(first[0],'tree-summary-prompt')[0])==signature(named(v,'tree-summary-prompt')[0]) and signature(named(first[0],'question-title')[0])==signature(named(v,'question-title')[0]) for v in first[1:]))
  question=by_source[69];reveal=slides[-2]
  check('sampling extension has question then stable reveal',signature(named(question,'question-title')[0])==signature(named(reveal,'question-title')[0]))
  check('question withholds candidate curves',not any(shape_name(o).startswith('alias-wave-') for o in question.findall('p:cSld/p:spTree/p:sp',NS)))
  check('reveal shows both different curves',all(named(reveal,f'alias-wave-{f}') for f in [1,3]))
  check('independent shared-sample values',all(abs(math.cos(2*math.pi*f*t)-v)<1e-10 for f in [1,3] for t,v in [(0,1),(.5,-1),(1,1)]))
  check('sampling extension shares identical sample geometry',all(signature(named(question,f'shared-sample-{k}-{j}')[0])==signature(named(reveal,f'shared-sample-{k}-{j}')[0]) for k in [0,1] for j in range(3)))
  check('compression goal admits larger inputs','目标是减少数据量' in text(by_source[57]) and '目标是减少数据量' in text(by_source[70]))
  check('three native comparison grids retained',sum(shape_name(o).startswith('Rectangle') for o in by_source[60].findall('p:cSld/p:spTree/p:sp',NS))==162)
  for n in [45,55,60]:
   shapes=[o for o in by_source[n].findall('p:cSld/p:spTree/p:sp',NS) if shape_name(o) not in ['top-rail','bottom-rail','question-title']]
   check(f'{n}: content inside horizontal safe margins',all(box(o)[0]>=63.8 and box(o)[0]+box(o)[2]<=1216.1 for o in shapes))
 failures=[r for r in checks if not r['pass']]
 result={'pptx':str(PPTX),'sha256':hashlib.sha256(PPTX.read_bytes()).hexdigest(),'slides':len(slides),'checks':len(checks),'passed':not failures,'failures':failures,'details':checks,'unverified':['WPS/PowerPoint native rendering and notes','Windows remote JupyterLab operation','classroom projection/audio/pacing']}
 OUT.write_text(json.dumps(result,indent=2))
 print(json.dumps({k:v for k,v in result.items() if k!='details'}))
 if failures:sys.exit(1)
