"""Run both notebooks in a real local Jupyter kernel; outputs are validation artifacts only."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
for role in ['teacher','student']:
    n=nbformat.read(ROOT/f'demo-lab-{role}.ipynb',4)
    NotebookClient(n,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
    nbformat.write(n,ROOT/f'.build/demo-lab-{role}-executed.ipynb')
    print(role, 'kernel execution passed',len([c for c in n.cells if c.cell_type=='code']), 'code cells')
