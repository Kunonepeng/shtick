"""Render the exact delivered deck, retain every page, and record actual PDF fonts."""
from pathlib import Path
import os
import subprocess
import hashlib
import json
from PIL import Image, ImageDraw
from pypdf import PdfReader
from lesson_model import ROOT, compile_plan

out=ROOT/'validation/v4/render';out.mkdir(parents=True,exist_ok=True)
fontconfig=ROOT/'validation/v4/fontconfig.xml'
font_dir=Path(os.environ.get('AUDIO_FONT_DIR', str(Path.home()/'Library/Fonts')))
fontconfig.write_text(f'<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig><dir>{font_dir}</dir><cachedir>/tmp/audio-v4-font-cache</cachedir></fontconfig>\n')
env=dict(os.environ,FONTCONFIG_FILE=str(fontconfig))
soffice=os.environ.get('AUDIO_SOFFICE','/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/soffice')
pptx=ROOT/'exports/1-2-3-audio-encoding-v4-final.pptx'
run=subprocess.run([soffice,'-env:UserInstallation=file:///tmp/audio-v4-lo-profile','--headless','--convert-to','pdf','--outdir',str(out),str(pptx)],env=env,capture_output=True,text=True,check=True)
(ROOT/'validation/v4/render.log').write_text(run.stdout+run.stderr)
pdf=out/(pptx.stem+'.pdf')
subprocess.run(['pdftoppm','-png','-r','120',str(pdf),str(out/'slide')],check=True,capture_output=True)
reader=PdfReader(pdf);fonts=set()
for page in reader.pages:
    for font in page['/Resources'].get_object().get('/Font',{}).get_object().values():fonts.add(str(font.get_object()['/BaseFont']))
images=sorted(out.glob('slide-*.png'))
assert len(images)==len(reader.pages)==len(compile_plan())
assert fonts and all('AlibabaPuHuiTi' in f for f in fonts),fonts
for batch in range((len(images)+9)//10):
    montage=Image.new('RGB',(1280,1930),'#eeeeee');draw=ImageDraw.Draw(montage)
    for offset,png in enumerate(images[batch*10:(batch+1)*10]):
        im=Image.open(png).convert('RGB');im.thumbnail((620,349));x=10+(offset%2)*640;y=10+(offset//2)*386
        draw.text((x,y),str(batch*10+offset+1),fill='black');montage.paste(im,(x,y+22))
    montage.save(out/f'montage-{batch+1}.jpg',quality=90)
report={'passed':True,'pptx_sha256':hashlib.sha256(pptx.read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':len(images),'dimensions':list(Image.open(images[0]).size),'actual_fonts':sorted(fonts),'renderer':subprocess.check_output([soffice,'--version'],env=env,text=True).strip(),'scope':'Local PDF renderer and fonts; WPS, PowerPoint and projector remain separate.'}
(ROOT/'validation/v4/render-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
