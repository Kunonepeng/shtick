"""Test relative runtime dependencies in an isolated classroom copy."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import os,sys,json,shutil,tempfile,hashlib
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
COPY=Path(tempfile.mkdtemp(prefix='audio-v4-classroom-')).resolve()
files=[ROOT/'demo-lab-teacher.ipynb',ROOT/'demo-lab-student.ipynb',*list((ROOT/'notebooks/staged').glob('*.ipynb')),ROOT/'demos/audio_core.py',ROOT/'demos/audio-lab.html',*list((ROOT/'assets/audio').glob('*.wav')),ROOT/'exports/1-2-3-audio-encoding-v4-final.pptx',*list((ROOT/'exports/reference-v4').rglob('*'))]
for p in files:
    if p.is_file():
        target=COPY/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
class Dependencies(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ['src','href'] and v:self.links.append(v)
checks=[]
for p in [COPY/'demos/audio-lab.html',COPY/'exports/reference-v4/slides.html']:
    parser=Dependencies();parser.feed(p.read_text())
    for link in parser.links:
        url=urlsplit(link)
        if url.scheme or url.netloc or not url.path:continue
        target=p.parent/unquote(url.path)
        checks.append(dict(file=str(p.relative_to(COPY)),link=link,exists=target.exists()))
        assert target.exists(),target
os.environ['PATH']=str(Path(sys.executable).parent)+os.pathsep+os.environ['PATH']
for role in ['teacher','student']:
    n=nbformat.read(COPY/f'demo-lab-{role}.ipynb',4)
    probe=nbformat.v4.new_code_cell('import json,audio_core,os\nprint(json.dumps(dict(root=str(ROOT.resolve()),cwd=os.getcwd(),module=str(Path(audio_core.__file__).resolve()))))')
    n.cells.append(probe)
    NotebookClient(n,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(COPY)}}).execute()
    observed=json.loads(n.cells.pop().outputs[0].text)
    assert observed['root']==str(COPY),observed
    assert observed['module']==str(COPY/'demos/audio_core.py'),observed
    nbformat.write(n,ROOT/f'validation/v4/executed/copied-{role}.ipynb')
    checks.append(dict(role=role,fresh_kernel=True,shared_module_from_copy=True,**observed))
report={'version':'v4','date':'2026-10-01','passed':True,'pptx_sha256':hashlib.sha256((COPY/'exports/1-2-3-audio-encoding-v4-final.pptx').read_bytes()).hexdigest(),'copy_directory':str(COPY),'copied_file_count':sum(p.is_file() for p in files),'checks':checks,'scope':'Offline relative dependencies and two fresh kernels in a copied directory. File-protocol browser and Windows classroom applications are separate.'}
(ROOT/'validation/v4/copy-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
