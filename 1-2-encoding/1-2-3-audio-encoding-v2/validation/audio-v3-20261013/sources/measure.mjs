import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {createCanvas,GlobalFonts} from '@napi-rs/canvas';
const FONT_DIR=process.env.AUDIO_V3_FONT_DIR??path.join(os.homedir(),'Library','Fonts');
for(const [file,face]of [['55-Regular','Alibaba PuHuiTi 3.0 55 Regular'],['115-Black','Alibaba PuHuiTi 3.0 115 Black']])GlobalFonts.registerFromPath(`${FONT_DIR}/AlibabaPuHuiTi-3-${file}.ttf`,face);
const dir=process.argv[2];
if(!dir)throw new Error('Supply the rendered layout directory.');
const output=process.argv[3]??path.join(path.dirname(dir),'text-measurements.json');
const ctx=createCanvas(20,20).getContext('2d');
const findings=[];let measured=0;
for(const file of (await fs.readdir(dir)).filter(f=>f.endsWith('.layout.json')).sort()){
 const doc=JSON.parse(await fs.readFile(`${dir}/${file}`,'utf8'));
 for(const e of doc.elements??[]){
  if(!e.text||!e.style?.fontSize||!e.position)continue;
  ctx.font=`${e.style.bold?'bold ':''}${e.style.fontSize}px "${e.style.typeface}"`;
  const width=Math.max(...e.text.split('\n').map(t=>ctx.measureText(t).width));measured++;
  if(width>e.position.width+3)findings.push({page:doc.slide.index+1,name:e.name,text:e.text,measuredWidth:Math.round(width*100)/100,frameWidth:e.position.width});
 }
}
await fs.writeFile(output,JSON.stringify({measured,findings},null,2));
console.log(JSON.stringify({measured,findings}));
