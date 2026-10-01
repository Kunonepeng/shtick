"""Execute in-memory copies; keep delivered notebooks cleared of answers."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient
import json
ROOT=Path(__file__).resolve().parents[1]
report=[]
for role in ['teacher','student']:
    nb=nbformat.read(ROOT/f'demo-lab-{role}.ipynb',as_version=4)
    nbformat.validate(nb)
    NotebookClient(nb,timeout=60,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
    outputs=sum(len(c.get('outputs',[])) for c in nb.cells)
    report.append({'role':role,'code_cells':sum(c.cell_type=='code' for c in nb.cells),'outputs_in_test_copy':outputs,'pass':True})
    print(role,'execution passed')
(ROOT/'validation/notebook-execution.json').write_text(json.dumps(report,indent=2))
