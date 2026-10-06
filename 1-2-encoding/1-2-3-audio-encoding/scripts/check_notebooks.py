"""Run both notebooks in a real local Jupyter kernel; outputs are validation artifacts only."""
from pathlib import Path
import os,sys,json
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
os.environ['PATH']=str(Path(sys.executable).parent)+os.pathsep+os.environ['PATH']
environments=[]
def execute(notebook,name):
    probe=nbformat.v4.new_code_cell("import sys,json,numpy,IPython,matplotlib,os\nprint(json.dumps(dict(executable=sys.executable,python=sys.version,numpy=numpy.__version__,IPython=IPython.__version__,matplotlib=matplotlib.__version__,cwd=os.getcwd())))")
    notebook.cells.insert(0,probe)
    NotebookClient(notebook,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
    value=json.loads(notebook.cells.pop(0).outputs[0].text)
    environments.append(dict(notebook=name,**value))
    (ROOT/'validation/v4/kernel-environments.json').write_text(json.dumps(environments,indent=2)+'\n')
(ROOT/'validation/v4/executed').mkdir(parents=True,exist_ok=True)
for role in ['teacher','student']:
    n=nbformat.read(ROOT/f'demo-lab-{role}.ipynb',4)
    execute(n,role)
    nbformat.write(n,ROOT/f'validation/v4/executed/demo-lab-{role}.ipynb')
    print(role, 'kernel execution passed',len([c for c in n.cells if c.cell_type=='code']), 'code cells')

for source in sorted((ROOT/'notebooks/staged').glob('*.ipynb')):
    notebook=nbformat.read(source,4)
    execute(notebook,source.name)
    nbformat.write(notebook,ROOT/'validation/v4/executed'/source.name)
    print(source.name, 'fresh kernel execution passed')
