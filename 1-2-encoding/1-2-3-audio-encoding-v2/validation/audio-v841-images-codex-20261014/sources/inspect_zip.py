"""Inspect ordered native slide objects and notes without modifying a deck."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as E
import posixpath,json,hashlib,sys
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def target(base,value):return value.lstrip('/') if value.startswith('/') else posixpath.normpath(posixpath.dirname(base)+'/'+value)
def text(node):return '\n'.join(''.join(x.text or ''for x in p.findall('.//a:t',ns))for p in node.findall('.//a:p',ns)).strip()
f=Path(sys.argv[1]);out=Path(sys.argv[2]);slides=[]
with ZipFile(f)as z:
 pr=E.fromstring(z.read('ppt/presentation.xml'));rl=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'));m={v.get('Id'):target('ppt/presentation.xml',v.get('Target'))for v in rl};paths=[m[v.get('{'+ns['r']+'}id')]for v in pr.find('p:sldIdLst',ns)]
 for i,name in enumerate(paths):
  s=E.fromstring(z.read(name));objs=[];rels=E.fromstring(z.read(posixpath.join(posixpath.dirname(name),'_rels',posixpath.basename(name)+'.rels')));rm={v.get('Id'):target(name,v.get('Target'))for v in rels if v.get('TargetMode')!='External'}
  for o in s.findall('p:cSld/p:spTree/*',ns):
   meta=o.find('.//p:cNvPr',ns);xfrm=o.find('p:spPr/a:xfrm',ns);box=None
   if xfrm is not None:
    a=xfrm.find('a:off',ns);b=xfrm.find('a:ext',ns)
    if a is not None and b is not None:box=[int(v)/9525 for v in [a.get('x'),a.get('y'),b.get('cx'),b.get('cy')]]
   blip=o.find('.//a:blip',ns);image=rm.get(blip.get('{'+ns['r']+'}embed'))if blip is not None else None
   objs.append({'kind':o.tag.split('}')[-1],'name':meta.get('name')if meta is not None else '', 'id':meta.get('id')if meta is not None else '', 'text':text(o),'box':box,'image':image,'fonts':[v.get('typeface')for v in o.findall('.//a:latin',ns)],'font_sizes':[int(v.get('sz'))/100 for v in o.findall('.//a:rPr',ns)if v.get('sz')]})
  nt=next(v.get('Target')for v in rels if v.get('Type').endswith('/notesSlide'));note=E.fromstring(z.read(target(name,nt)));notes=text(note)
  texts=[o['text']for o in objs if o['text']];slides.append({'page':i+1,'xml':name,'title':texts[0]if texts else '', 'texts':texts,'objects':objs,'notes':notes})
 result={'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'size_emu':pr.find('p:sldSz',ns).attrib,'slides':slides,'media':[{ 'path':n,'sha256':hashlib.sha256(z.read(n)).hexdigest(),'bytes':len(z.read(n))}for n in z.namelist()if n.startswith('ppt/media/')],'fonts':sorted(set(v for s in slides for o in s['objects']for v in o['fonts']))}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in result.items()if k!='slides'and k!='media'},ensure_ascii=False));print('Slide count:',len(slides),'Media count:',len(result['media']));print('\n'.join(f"{s['page']:02}: {s['title']}"for s in slides))
