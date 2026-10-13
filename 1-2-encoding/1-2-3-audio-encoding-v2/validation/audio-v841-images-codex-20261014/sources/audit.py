"""Check the delivered copy independently of its authoring calculations."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from decimal import Decimal
from PIL import Image
from io import BytesIO
import sys,json,hashlib,posixpath,math

deck, plan_file, source, output = map(Path,sys.argv[1:5])
plan=json.loads(plan_file.read_text()); checks=[]
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def check(name,passed,evidence=''): checks.append({'check':name,'status':'pass' if passed else 'fail','evidence':evidence})
def text(node):return '\n'.join(''.join(p.xpath('.//a:t/text()',namespaces=NS))for p in node.findall('.//a:p',NS)).strip()
def sig(node):
    t=text(node);x=node.find('p:spPr/a:xfrm',NS)
    if not t or x is None:return None
    return (t,tuple(sorted(x.find('a:off',NS).attrib.items())),tuple(sorted(x.find('a:ext',NS).attrib.items())),tuple(v.get('typeface')for v in node.findall('.//a:latin',NS)))
def target(base,ref):return ref.lstrip('/') if ref.startswith('/')else posixpath.normpath(posixpath.join(posixpath.dirname(base),ref))
def relpath(part):return posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels')
with ZipFile(deck)as z,ZipFile(source)as original:
    check('Source deck unchanged',hashlib.sha256(source.read_bytes()).hexdigest()==plan['sourceSha256'],plan['sourceSha256'])
    pr=E.fromstring(z.read('ppt/presentation.xml'));size=pr.find('p:sldSz',NS)
    check('Wide canvas',size.get('cx')=='12191695' and size.get('cy')=='6858000',dict(size.attrib))
    check('Ordered slide count',len(pr.find('p:sldIdLst',NS))==plan['slideCount'],plan['slideCount'])
    check('Original teaching order preserved',[s['basePage']for s in plan['slides']if s['key'].startswith('p')]==list(range(1,71)))
    bykey={};source_images=[]
    for entry in plan['slides']:
        part=entry['xml'];slide=E.fromstring(z.read(part));tree=slide.find('p:cSld/p:spTree',NS);bykey[entry['key']]=tree
        rels=E.fromstring(z.read(relpath(part)));rm={r.get('Id'):target(part,r.get('Target'))for r in rels if r.get('TargetMode')!='External'}
        ids=[n.get('id')for n in tree.findall('.//p:cNvPr',NS)]
        check(entry['key']+' unique object IDs',len(ids)==len(set(ids)))
        bounds=[]
        for o in tree:
            x=o.find('p:spPr/a:xfrm',NS)
            if x is None:continue
            off=x.find('a:off',NS);ext=x.find('a:ext',NS)
            if off is None or ext is None:continue
            a,b,w,h=(int(off.get('x')),int(off.get('y')),int(ext.get('cx')),int(ext.get('cy')))
            if min(a,b)<-4 or a+w>12191699 or b+h>6858004:bounds.append([a,b,w,h])
        check(entry['key']+' canvas bounds',not bounds,bounds)
        for rid,y in [('2',0),('3',6756400)]:
            o=next(o for o in tree if o.find('.//p:cNvPr',NS)is not None and o.find('.//p:cNvPr',NS).get('id')==rid)
            x=o.find('p:spPr/a:xfrm',NS);a=x.find('a:off',NS);b=x.find('a:ext',NS)
            check(entry['key']+' rail '+rid,a.get('x')=='0'and abs(int(a.get('y'))-y)<=1 and b.get('cx')=='12191695'and b.get('cy')=='101600')
        families=[f.get('typeface')for f in tree.xpath('.//a:latin|.//a:ea|.//a:cs',namespaces=NS)]
        check(entry['key']+' native fonts',bool(families) and all(f.startswith('Alibaba PuHuiTi 3.0 ')for f in families),sorted(set(families)))
        note_part=next(target(part,r.get('Target'))for r in rels if r.get('Type').endswith('/notesSlide'))
        notes=text(E.fromstring(z.read(note_part)))
        check(entry['key']+' stage transcript',notes.startswith('[问题]')and '[教师逐字稿]'in notes and len(notes)>100)
        visible='\n'.join(text(o)for o in tree)
        check(entry['key']+' teacher prompt withheld','先只预测，不公布答案' not in visible)
        for pic in tree.findall('p:pic',NS):
            blip=pic.find('p:blipFill/a:blip',NS);media=rm[blip.get('{'+NS['r']+'}embed')];im=Image.open(BytesIO(z.read(media)))
            crop=pic.find('p:blipFill/a:srcRect',NS);edges={k:int(crop.get(k,'0'))/100000 if crop is not None else 0 for k in ['l','r','t','b']}
            iw=im.width*(1-edges['l']-edges['r']);ih=im.height*(1-edges['t']-edges['b']);box=pic.find('p:spPr/a:xfrm/a:ext',NS)
            ratio=(int(box.get('cx'))/int(box.get('cy')))/(iw/ih)
            check(entry['key']+' picture aspect '+media,abs(ratio-1)<.012,ratio)
    for entry in plan['slides']:
        if entry['role']!='question':continue
        qtree=bykey[entry['key']];rtree=bykey['p'+str(entry['basePage'])]
        qa={sig(o)for o in qtree if sig(o)};ra={sig(o)for o in rtree if sig(o)}
        missing=[v[0]for v in qa-ra]
        check(entry['key']+' stable question/givens',not missing,missing)
        if entry['basePage']not in {17,19,21,22,29,36,43,53,59,63,65,12,24,69}:
            check(entry['key']+' clean thinking pause',len(qa)==1,len(qa))
    for stage in range(1,7):
        tree=bykey['tree'+str(stage)];names=[n.get('name')for n in tree.findall('.//p:cNvPr',NS)]
        node_names=[n for n in names if 'tree-node-'in n]
        check('tree'+str(stage)+' one new node',len(node_names)==stage,len(node_names))
        if stage>1:
            previous={sig(o)for o in bykey['tree'+str(stage-1)]if sig(o)}
            current={sig(o)for o in tree if sig(o)}
            check('tree'+str(stage)+' established text stable',previous<=current)
    for n in original.namelist():
        if n.startswith('ppt/media/'):check('Preserved source media '+n,z.read(n)==original.read(n))

calculations={'exercise1_bytes':16000*8*2*5//8,'exercise2_bytes':48000*16*2*60//8,'exercise3_bytes':44100*16*2*300//8,'video_frame_bytes':480*320*24//8,'video_frames':25*60*10}
calculations['exercise2_MiB']=str((Decimal(calculations['exercise2_bytes'])/Decimal(1024**2)).quantize(Decimal('.01')))
calculations['video_GiB']=str((Decimal(calculations['video_frame_bytes']*calculations['video_frames'])/Decimal(1024**3)).quantize(Decimal('.01')))
check('Independent PCM/video arithmetic',calculations['exercise1_bytes']==160000 and calculations['exercise2_MiB']=='10.99'and calculations['video_GiB']=='6.44',calculations)
check('Independent midpoint quantization',Decimal('3.71')-Decimal('3.5')==Decimal('.21')and Decimal('3.75')-Decimal('3.71')==Decimal('.04'))
check('Independent alias equality',all(abs(math.cos(2*math.pi*t)-math.cos(6*math.pi*t))<1e-12 for t in [0,.5,1]))
result={'deck':str(deck),'sha256':hashlib.sha256(deck.read_bytes()).hexdigest(),'passed':sum(c['status']=='pass'for c in checks),'failed':sum(c['status']=='fail'for c in checks),'checks':checks}
output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='checks'}));print(json.dumps([c for c in checks if c['status']=='fail'],ensure_ascii=False));sys.exit(bool(result['failed']))
