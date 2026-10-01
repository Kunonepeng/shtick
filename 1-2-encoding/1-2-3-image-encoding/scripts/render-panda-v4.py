"""Render all final slides and reject font substitution before accepting evidence."""
from pathlib import Path
import argparse,json,os,re,subprocess,tempfile,shutil
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'.codex-build/panda-v4'
parser=argparse.ArgumentParser();parser.add_argument('--font-dir',required=True,type=Path);parser.add_argument('--soffice',default='soffice');parser.add_argument('--input',type=Path);args=parser.parse_args()
source=args.input or ROOT/'exports/1-2-3-image-encoding-panda-v4.pptx'
assert source.exists(),f'Missing PPTX: {source}'
for filename in ['AlibabaPuHuiTi-3-115-Black.ttf','AlibabaPuHuiTi-3-55-Regular.ttf']:assert (args.font_dir/filename).exists(),f'Missing required font: {filename}'
with tempfile.TemporaryDirectory(prefix='panda-v4-render-') as trial:
    trial=Path(trial);config=trial/'fonts.conf';cache=trial/'cache';cache.mkdir()
    config.write_text(f'<?xml version="1.0"?><fontconfig><dir>{args.font_dir.resolve()}</dir><cachedir>{cache}</cachedir></fontconfig>')
    env={**os.environ,'FONTCONFIG_FILE':str(config)}
    cmd=[args.soffice,f'-env:UserInstallation={(trial/"profile").as_uri()}','--headless','--convert-to','pdf','--outdir',str(trial),str(source.resolve())]
    result=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=90);assert result.returncode==0,result.stderr
    pdf=trial/(source.stem+'.pdf');assert pdf.exists(),result.stdout+result.stderr
    font_names=sorted(set(x.decode() for x in re.findall(rb'/BaseFont\s*/([^\s/]+)',pdf.read_bytes())))
    assert font_names and all('AlibabaPuHuiTi' in name and ('115' in name or '55' in name) for name in font_names),font_names
    subprocess.run(['pdftoppm','-png','-r','120',str(pdf),str(trial/'slide')],check=True,capture_output=True,timeout=90)
    images=sorted(trial.glob('slide-*.png'));assert len(images)==77,len(images)
    render=OUT/'render';render.mkdir(exist_ok=True)
    for i,image in enumerate(images,1):shutil.copyfile(image,render/f'slide-{i:02}.png')
    shutil.copyfile(pdf,OUT/'final-render.pdf')
    for start in range(0,len(images),12):
        sheet=Image.new('RGB',(1600,750),'white');draw=ImageDraw.Draw(sheet)
        for i,image in enumerate(images[start:start+12]):
            im=Image.open(image).convert('RGB');im.thumbnail((400,225));x=(i%4)*400;y=(i//4)*250;sheet.paste(im,(x,y));draw.text((x+5,y+228),f'Slide {start+i+1:02}',fill='black')
        sheet.save(render/f'montage-{start//12+1}.jpg',quality=90)
    version=subprocess.run([args.soffice,'--version'],capture_output=True,text=True,check=True).stdout.strip()
    record={'input':str(source.relative_to(ROOT)),'renderer':version,'pages':len(images),'resolution':list(Image.open(images[0]).size),'font_dir':str(args.font_dir),'fonts':font_names,'font_substitution':'none','human_inspection':'pending'}
    (OUT/'render-fonts.json').write_text(json.dumps(record,indent=2));(OUT/'render.log').write_text(result.stdout+result.stderr);print(json.dumps(record))
