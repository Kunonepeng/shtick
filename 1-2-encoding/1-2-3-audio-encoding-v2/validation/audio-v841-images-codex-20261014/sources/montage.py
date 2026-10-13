"""Make a montage in numeric teaching order, including pages above 99."""
from pathlib import Path
from PIL import Image,ImageDraw
import sys,math
root=Path(sys.argv[1]);files=sorted(root.glob('slide-*.png'),key=lambda p:int(p.stem.split('-')[-1]))
canvas=Image.new('RGB',(1600,204*math.ceil(len(files)/5)),'#eeeeee');draw=ImageDraw.Draw(canvas)
for i,f in enumerate(files):
    im=Image.open(f).convert('RGB');im.thumbnail((320,180));x=i%5*320;y=i//5*204
    canvas.paste(im,(x,y+20));draw.text((x+6,y+4),str(int(f.stem.split('-')[-1])),fill='black')
canvas.save(sys.argv[2]);print(len(files))
