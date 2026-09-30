from pathlib import Path
root=Path(__file__).resolve().parent
old=(root/'build-v4.mjs').read_text()
helpers=old[old.index('function rect'):old.index('const extra=')]
start=helpers.index('function flower(');end=helpers.index('const imgs=')
helpers=helpers[:start]+helpers[end:]
helpers=helpers.replace('[4,5,20,22,25]','[22,25]')
helpers=helpers.replace("C.ink,F.bold,'center')}));}","((mode==='number'&&+n<2)?'#FFFFFF':C.ink),F.bold,'center')}));}")
head="""import fs from 'node:fs/promises';
import path from 'node:path';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const root='/Users/chran/repo/shtick/1-2-encoding/1-2-3-image-encoding-v2';
const P=Presentation.create({slideSize:{width:1280,height:720}});
const F={regular:'Alibaba PuHuiTi 3.0 55 Regular',black:'Alibaba PuHuiTi 3.0 115 Black',bold:'Alibaba PuHuiTi 3.0 115 Black'};
const C={ink:'#262626',violet:'#6251B1',accent:'#8C64E1',cyan:'#007C9B',red:'#FF0000',grid:'#C8C3D5',muted:'#808080'};
const D=JSON.parse(await fs.readFile(path.join(root,'.codex-build/panda-data.json'),'utf8'));
const qs=JSON.parse(await fs.readFile(path.join(root,'.codex-build/lesson-teaching-v4.json'),'utf8'));
const palette=D.palette,four=D.coarse,fine=D.fine,six=D.six;
const plan=[],pairs=[];
"""
(root/'build-panda.mjs').write_text(head+helpers)
(root/'panda-reused-cases.txt').write_text(old[old.index(' case 13:'):old.index(' case 15:')]+old[old.index(' case 18:'):old.index('\n }\n}',old.index(' case 18:'))])
(root/'panda-homework.txt').write_text(old[old.index("const hw=frame('课后练习')"):old.index("await fs.writeFile(path.join(root,'.codex-build/lesson-teaching-v4.json')")])
