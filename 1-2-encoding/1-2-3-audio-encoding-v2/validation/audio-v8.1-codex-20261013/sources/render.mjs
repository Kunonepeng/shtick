import fs from 'node:fs/promises';
import { GlobalFonts } from '@napi-rs/canvas';
import { FileBlob, PresentationFile } from '@oai/artifact-tool';
const dir='/private/tmp/audio-v81-codex-20261013';
for(const [file,family] of [['55-Regular','Alibaba PuHuiTi 3.0 55 Regular'],['115-Black','Alibaba PuHuiTi 3.0 115 Black']]){
  if(!GlobalFonts.registerFromPath(`/Users/chran/Library/Fonts/AlibabaPuHuiTi-3-${file}.ttf`,family))throw new Error(`Font registration failed: ${family}`);
}
const input=process.argv[2]??`${dir}/candidate.pptx`;
const output=process.argv[3]??`${dir}/render`;
const p=await PresentationFile.importPptx(await FileBlob.load(input));
await fs.mkdir(output,{recursive:true});
for(let i=0;i<p.slides.items.length;i++){
 const s=p.slides.items[i];
 const image=await p.export({slide:s,format:'png',scale:1.5});
 await fs.writeFile(`${output}/slide-${String(i+1).padStart(2,'0')}.png`,new Uint8Array(await image.arrayBuffer()));
 const layout=await s.export({format:'layout'});
 await fs.writeFile(`${output}/slide-${String(i+1).padStart(2,'0')}.layout.json`,await layout.text());
}
console.log(JSON.stringify({input,slides:p.slides.items.length,output,fontAliases:GlobalFonts.families.filter(x=>x.family.includes('Alibaba PuHuiTi 3.0 '))}));
