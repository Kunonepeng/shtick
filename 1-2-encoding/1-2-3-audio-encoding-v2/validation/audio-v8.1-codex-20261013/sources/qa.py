"""Run local deck checks, montages, and render comparisons."""
from pathlib import Path
import sys,subprocess,json,hashlib,math
from PIL import Image,ImageDraw
r=Path(__file__).parent;stage=int(sys.argv[1]);node='/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node';py=sys.executable
ppt=r/f'round{stage}-after.pptx';renders=r/f'round{stage}-render';tools=Path('/Users/chran/.codex/plugins/cache/openai-primary-runtime/presentations/26.1011.11113/skills/presentations/container_tools')
commands=[[py,str(r/'audit.py'),str(ppt),str(r/f'round{stage}-audit.json'),str(r/f'round{stage}-plan.json')],[node,str(r/'measure.mjs'),str(renders),str(r/f'round{stage}-measurements.json')],[py,str(tools/'inspect_presentation_layout_geometry.py'),str(ppt),'--expected-slide-size-emu','12191695,6858000','--validate-heading-fit','--validate-bullet-geometry','--approved-font-family','Alibaba PuHuiTi 3.0 55 Regular','--approved-font-family','Alibaba PuHuiTi 3.0 115 Black','--fail-on-findings']]
for i,cmd in enumerate(commands):
 result=subprocess.run(cmd,text=True,capture_output=True)
 if i==2:(r/f'round{stage}-after-geometry.json').write_text(result.stdout)
 print(result.stdout[:1000]);assert result.returncode==0,result.stderr[-1500:]
files=sorted(renders.glob('slide-*.png'));cw,ch=320,204;canvas=Image.new('RGB',(cw*5,ch*math.ceil(len(files)/5)),'#eeeeee');d=ImageDraw.Draw(canvas)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGB');im.thumbnail((320,180));x=(i%5)*cw;y=(i//5)*ch;canvas.paste(im,(x,y+20));d.text((x+8,y+3),str(i+1),fill='black')
canvas.save(r/f'round{stage}-montage.png')
comparison=[]
if stage>1:
 plan=json.loads((r/f'round{stage}-plan.json').read_text());old=r/f'round{stage-1}-render'
 for item in plan['manifest']:
  source=item.get('source_page',item['page']);page=item['page']
  if source is not None:
   fn=f'slide-{page:02}.png';oldfn=f'slide-{source:02}.png';same=hashlib.sha256((renders/fn).read_bytes()).digest()==hashlib.sha256((old/oldfn).read_bytes()).digest();comparison.append({'page':page,'source_page':source,'pixel_identical':same})
 (r/f'round{stage}-render-comparison.json').write_text(json.dumps(comparison,indent=2));print('Changed original pages:',[v['source_page']for v in comparison if not v['pixel_identical']])
