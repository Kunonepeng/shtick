"""Set project font defaults in theme/master/notes; preserve explicit slide run faces."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from xml.etree import ElementTree as E
import os
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'.build/audio-candidate.pptx'
A='http://schemas.openxmlformats.org/drawingml/2006/main';PNS='http://schemas.openxmlformats.org/presentationml/2006/main'
E.register_namespace('a',A);E.register_namespace('p',PNS);E.register_namespace('r','http://schemas.openxmlformats.org/officeDocument/2006/relationships')
REG='Alibaba PuHuiTi 3.0 55 Regular';BLACK='Alibaba PuHuiTi 3.0 115 Black'
records={}
with ZipFile(P) as z:
 for item in z.infolist():
  raw=z.read(item.filename)
  if item.filename.startswith('ppt/') and item.filename.endswith('.xml') and ('theme/' in item.filename or 'Master' in item.filename or item.filename.startswith('ppt/notesSlides/') or item.filename=='ppt/presentation.xml'):
   tree=E.fromstring(raw)
   for name,face in [('majorFont',BLACK),('minorFont',REG)]:
    for font in tree.findall(f'.//{{{A}}}{name}'):
     for kind in ['latin','ea','cs']:
      child=font.find(f'{{{A}}}{kind}')
      if child is None:child=E.SubElement(font,f'{{{A}}}{kind}')
      child.set('typeface',face)
   for pr in tree.findall(f'.//{{{A}}}defRPr')+tree.findall(f'.//{{{A}}}rPr'):
    for kind in ['latin','ea','cs']:
     child=pr.find(f'{{{A}}}{kind}')
     if child is None:child=E.SubElement(pr,f'{{{A}}}{kind}')
     if not child.get('typeface','').startswith('Alibaba PuHuiTi'):child.set('typeface',REG)
   raw=E.tostring(tree,encoding='utf-8',xml_declaration=True)
  records[item.filename]=raw
out=P.with_suffix('.fontfixed.pptx')
with ZipFile(out,'w',ZIP_DEFLATED) as z:
 for name,data in records.items():z.writestr(name,data)
os.replace(out,P)
print('Theme, master, notes and presentation defaults set to Alibaba PuHuiTi 3.0')
