from PIL import Image
import numpy as np,json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent.parent
p=root/'assets/pandas.jpg'; im=Image.open(p).convert('RGB'); a=np.asarray(im)
x,y,w,h=280,100,288,288
crop=a[y:y+h,x:x+w].astype(float)
pal=np.array([[36,33,27],[119,118,110],[188,187,179],[242,240,230],[81,76,65],[219,217,206]])
def blocks(n):return crop.reshape(n,h//n,n,w//n,3).mean(axis=(1,3))
def indices(b,p):return ((b[:,:,None,:]-p[None,None,:,:])**2).sum(axis=3).argmin(axis=2)
b8,b16=blocks(8),blocks(16)
m8=indices(b8,pal[:4]);m16=indices(b16,pal[:4]);m6=indices(b16,pal)
# Take an actual pixel at the green iris, with zero-based original-image coordinates.
px,py=422,230
# Actual source pixel grid includes the iris boundary.
zx,zy,zw=417,220,16
D={'source':'assets/pandas.jpg','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sourceSize':list(im.size),'crop':{'x':x,'y':y,'width':w,'height':h},'palette':['#'+''.join(f'{int(t):02X}' for t in c) for c in pal],'paletteRgb':pal.tolist(),'coarse':[''.join(map(str,r)) for r in m8],'fine':[''.join(map(str,r)) for r in m16],'six':[''.join(map(str,r)) for r in m6],'means8':np.round(b8,6).tolist(),'means16':np.round(b16,6).tolist(),'pixel':{'x':px,'y':py,'rgb':a[py,px].tolist(),'binary':[format(int(v),'08b') for v in a[py,px]]},'zoom':{'x':zx,'y':zy,'size':zw,'rgb':a[zy:zy+zw,zx:zx+zw].tolist()},'rowExercise':{'row':6,'firstColumn':5,'lastColumn':12,'indices':m16[5,4:12].tolist(),'codes':[format(int(v),'02b') for v in m16[5,4:12]]},'mse4':float(((b16-pal[m16])**2).mean()),'mse6':float(((b16-pal[m6])**2).mean()),'colorsUsed':[len(set(m8.flat)),len(set(m16.flat)),len(set(m6.flat))]}
(root/'.codex-build/panda-data.json').write_text(json.dumps(D,ensure_ascii=False,indent=2))
print(json.dumps({k:D[k] for k in ['crop','palette','coarse','fine','six','pixel','rowExercise','mse4','mse6','colorsUsed']},ensure_ascii=False,indent=2))
