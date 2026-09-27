#!/usr/bin/env python3
import argparse, json, math, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ap=argparse.ArgumentParser()
ap.add_argument('render_dir')
ap.add_argument('--data', required=True)
ap.add_argument('--out', required=True)
args=ap.parse_args()
rdir=Path(args.render_dir)
data=json.loads(Path(args.data).read_text(encoding='utf-8'))
files=sorted(rdir.glob('slide-*.png'), key=lambda p:int(re.search(r'(\d+)$',p.stem).group(1)))
if not files:
    raise SystemExit('No rendered slide PNGs found')
cols=5
thumb_w=360
first=Image.open(files[0]).convert('RGB')
ratio=first.height/first.width
thumb_h=round(thumb_w*ratio)
label_h=28
rows=math.ceil(len(files)/cols)
canvas=Image.new('RGB',(cols*thumb_w,rows*(thumb_h+label_h)),'white')
draw=ImageDraw.Draw(canvas)
for i,p in enumerate(files):
    im=Image.open(p).convert('RGB')
    im.thumbnail((thumb_w,thumb_h))
    x=(i%cols)*thumb_w+(thumb_w-im.width)//2
    y=(i//cols)*(thumb_h+label_h)
    canvas.paste(im,(x,y))
    draw.text((x+5,y+thumb_h+4),f'Slide {i+1}',fill='black')
canvas.save(args.out,'JPEG',quality=72,optimize=True)
