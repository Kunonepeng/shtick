from pathlib import Path
import sys,math
from PIL import Image,ImageDraw
folder=Path(sys.argv[1]);files=sorted(folder.glob('slide-*.png'));w,h=320,204;c=Image.new('RGB',(w*5,h*math.ceil(len(files)/5)),'#eeeeee');d=ImageDraw.Draw(c)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGB');im.thumbnail((320,180));x=i%5*w;y=i//5*h;c.paste(im,(x,y+20));d.text((x+6,y+4),str(i+1),fill='black')
c.save(sys.argv[2]);print(len(files))
