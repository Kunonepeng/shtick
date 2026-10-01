"""Rebuild exact teaching data without overwriting historical evidence."""
from pathlib import Path
import json,re,hashlib
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'course-design.qmd').read_text()
model=json.loads(re.search(r'<!-- panda-v4-model:start -->\s*```json\s*([\s\S]*?)```',text).group(1))
p=model['data'];source=ROOT/p['source'];image=Image.open(source).convert('RGB');pixels=np.asarray(image)
x,y,w,h=p['crop'];crop=pixels[y:y+h,x:x+w].astype(float);palette=np.asarray(p['palette_rgb'])
means={n:crop.reshape(n,h//n,n,w//n,3).mean(axis=(1,3)) for n in (8,16)}
def indices(n,levels):return ((means[n][:,:,None,:]-palette[None,None,:levels,:])**2).sum(axis=3).argmin(axis=2)
coarse,fine,six=indices(8,4),indices(16,4),indices(16,6)
hash_value=hashlib.sha256(source.read_bytes()).hexdigest();px,py=p['pixel'];zx,zy,size=p['zoom']
rows=lambda a:[''.join(map(str,row)) for row in a]
data={'source':p['source'],'sha256':hash_value,'sourceSize':list(image.size),'crop':dict(zip(('x','y','width','height'),p['crop'])),'paletteRgb':p['palette_rgb'],'palette':['#'+''.join(f'{v:02X}' for v in rgb) for rgb in p['palette_rgb']],'coarse':rows(coarse),'fine':rows(fine),'six':rows(six),'means8':means[8].tolist(),'means16':means[16].tolist(),'pixel':{'x':px,'y':py,'rgb':pixels[py,px].tolist(),'binary':[format(int(v),'08b') for v in pixels[py,px]]},'zoom':{'x':zx,'y':zy,'size':size,'rgb':pixels[zy:zy+size,zx:zx+size].tolist()},'rowExercise':{'row':6,'firstColumn':5,'lastColumn':12,'indices':fine[5,4:12].tolist(),'codes':[format(int(v),'02b') for v in fine[5,4:12]]},'mse4':float(((means[16]-palette[fine])**2).mean()),'mse6':float(((means[16]-palette[six])**2).mean())}
out=ROOT/'.codex-build/panda-v4';out.mkdir(parents=True,exist_ok=True);(out/'data.json').write_text(json.dumps(data,indent=2))
demo_path=ROOT/'demos/panda-digitization/panda_samples.json';demo=json.loads(demo_path.read_text());demo['grids']={str(n):means[n].tolist() for n in (8,16)};demo['note']='Unrounded block means drive quantization; only displayed RGB values are rounded. This is a teaching model applied to an existing decoded JPEG.';demo_path.write_text(json.dumps(demo,ensure_ascii=False,indent=2))
print(json.dumps({'source_sha256':hash_value,'rgb':data['pixel']['rgb'],'mse4':data['mse4'],'mse6':data['mse6']}))
