// Native editable production deck. All question/reveal wording and notes derive from course-design.qmd.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const require=createRequire(path.join(ROOT,'.build','package.json'));
const {Presentation,PresentationFile}=await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const W=1280,H=720;
const C={rail:'#6251B1',v:'#8C64E1',c:'#007C9B',r:'#FF0000',ink:'#262626',grey:'#737373',grid:'#D8D8DF'};
const F={body:'Alibaba PuHuiTi 3.0 55 Regular',title:'Alibaba PuHuiTi 3.0 115 Black'};
const p=Presentation.create({slideSize:{width:W,height:H}});
const md=await fs.readFile(path.join(ROOT,'course-design.qmd'),'utf8');
const plan=JSON.parse(await fs.readFile(path.join(ROOT,'validation/v4/slide-plan.json'),'utf8'));
const model=JSON.parse(md.match(/# C8 [\s\S]*?```json\n([\s\S]*?)\n```/)[1]);
function section(body,name){return (body.match(new RegExp('^### '+name+'\\n([\\s\\S]*?)(?=^### |(?![\\s\\S]))','m'))?.[1]??'').trim();}
function text(s,t,x,y,w=1152,h=48,size=29.333,color=C.ink,strong=false,name='text'){
 const o=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 o.text=t;o.text.style={typeface:strong?F.title:F.body,fontSize:size,color,bold:false,autoFit:'none',wrap:'none',verticalAlignment:'top',insets:{left:0,right:0,top:0,bottom:0}};
 return o;
}
function rect(s,x,y,w,h,fill='none',stroke=C.grid,width=1,name='box'){
 return s.shapes.add({geometry:'rect',name,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width}});
}
function line(s,x1,y1,x2,y2,color=C.grid,width=1,name='line'){
 const x=Math.min(x1,x2),y=Math.min(y1,y2),w=Math.max(1,Math.abs(x2-x1)),h=Math.max(1,Math.abs(y2-y1));
 return s.shapes.add({geometry:'custom',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:color,width},customPaths:[{width:w,height:h,commands:[{moveTo:{x:x1-x,y:y1-y}},{lineTo:{x:x2-x,y:y2-y}}]}]});
}
function pathCurve(s,pts,color=C.v,width=3,name='waveform'){
 const xs=pts.map(x=>x[0]),ys=pts.map(x=>x[1]);const x=Math.min(...xs),y=Math.min(...ys),w=Math.max(...xs)-x,h=Math.max(1,Math.max(...ys)-y);
 s.shapes.add({geometry:'custom',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:color,width},customPaths:[{width:w,height:h,commands:pts.map((v,i)=>({[i?'lineTo':'moveTo']:{x:v[0]-x,y:v[1]-y}}))}]});
}
function dot(s,x,y,color=C.r,size=10){s.shapes.add({geometry:'ellipse',name:'sample',position:{left:x-size/2,top:y-size/2,width:size,height:size},fill:color,line:{fill:'#FFFFFF',width:1}});}
function frame(s,title){
 s.background.fill='#FFFFFF';rect(s,0,0,W,10.666,C.rail,'none',0,'top-rail');rect(s,0,H-10.666,W,10.666,C.rail,'none',0,'bottom-rail');
 text(s,title,63.84,63.84,1152,74,48,C.ink,true,'question-title');
}
function waveform(s,{x=120,y=330,w=1000,h=150,samples=0,axes=true,label=true}={}){
 line(s,x,y,x+w,y,C.grid,1.5,'zero-line');line(s,x,y-h/2-15,x,y+h/2+20,C.ink,1.5,'amplitude-axis');
 pathCurve(s,Array.from({length:241},(_,i)=>[x+i*w/240,y-.8*Math.sin(4*Math.PI*i/240+.3)*h/2]),C.v,3);
 if(samples){for(let k=0;k<samples;k++)dot(s,x+k*w/samples,y-.8*Math.sin(4*Math.PI*k/samples+.3)*h/2);}
 if(label){text(s,'0',x-20,y+h/2+28,40,34,24);text(s,'1 s',x+w-28,y+h/2+28,65,34,24);}
}
function resultLines(s,lines,y=385,size=29.333){
 line(s,64,y-24,1216,y-24,C.grid,1);
 lines.forEach((t,i)=>text(s,t,64,y+i*66,1152,52,size,i===0?C.v:C.ink,i===0,'answer-'+i));
}

const built=new Map();let lastTree=null;
function neutral(slide,row){
 const n=row.q;
 if(row.id.includes('-B'))return;
 if(n===2)waveform(slide,{x:160,y:440,w:950,h:160,label:false});
 if(n===3)waveform(slide,{x:160,y:385,w:950,h:155,label:true});
 if(n===6)[0,1,2,3].forEach((v,i)=>text(slide,String(v),240+i*220,296,130,48,40,C.ink,true,'level-'+i));
 if(n===7){[0,1,2,3].forEach((v,i)=>rect(slide,260+i*185,308,132,52,'none',C.grid,1,'code-box'));['00','01','10','11'].forEach((v,i)=>text(slide,v,275+i*185,314,115,43,32));}
 if(n===13){text(slide,'L',125,350,50,48,32);text(slide,'R',125,430,50,48,32);[0,1,2].forEach(i=>{rect(slide,240+i*260,352,150,48);rect(slide,240+i*260,432,150,48);text(slide,`时刻${i+1}`,240+i*260,295,210,45,29.333);});}
}
function evidence(slide,row,base){
 const n=row.q;const answers=row.visible.slice(base.visible.length);
 if(row.id.includes('-B')){resultLines(slide,answers);return;}
 let y=385;
 if(n===2)y=560;
 if(n===3){for(let k=0;k<12;k++)dot(slide,160+k*950/12,385-.8*Math.sin(4*Math.PI*k/12+.3)*155/2);y=558;}
 if(n===5){['−0.62','−0.10','0.38','0.84'].forEach((v,i)=>text(slide,v,115+i*280,325,245,42,29.333));['−0.75','−0.25','0.25','0.75'].forEach((v,i)=>text(slide,`↓  ${v}`,115+i*280,385,245,42,29.333,C.v,true));y=485;}
 if(n===6){['00','01','10','11'].forEach((v,i)=>text(slide,v,240+i*220,358,130,48,40,C.v,true));y=453;}
 if(n===7)y=425;
 if(n===13){[0,1,2].forEach(i=>{text(slide,`L${i+1}`,265+i*260,359,105,40,29.333,C.v);text(slide,`R${i+1}`,265+i*260,439,105,40,29.333,C.c);});y=540;}
 if(n===10){
  const w=440,cy=390,scale=78;
  for(const [x,bits,color] of [[120,2,C.v],[690,4,C.c]]){
   text(slide,`${bits} bit：${2**bits}级`,x,280,470,43,32,color,true);
   line(slide,x,cy,x+w,cy);
   pathCurve(slide,Array.from({length:241},(_,i)=>[x+w*i/240,cy-.68*Math.sin(4*Math.PI*i/240+.3)*scale]),C.grey,2,'reference-wave');
   for(let k=0;k<48;k++){const z=.68*Math.sin(4*Math.PI*k/48+.3),i=Math.floor((z+1)*2**bits/2),q=-1+(i+.5)*2/2**bits,xx=x+w*k/48;line(slide,xx,cy-z*scale,xx,cy-q*scale,C.r,2,'quantization-error');dot(slide,xx,cy-q*scale,color,8);}
  }
  y=532;
 }
 if(n===2){text(slide,answers[0],64,y,1152,47,32,C.v,true);text(slide,answers[1],64,y+60,1152,47,29.333);}
 else if(n===3){text(slide,answers[0],64,y,1152,45,29.333,C.v,true);text(slide,answers[1],64,y+54,1152,45,29.333);}
 else if(n===13){text(slide,answers[1],64,y,1152,47,29.333);text(slide,answers[2],64,y+59,1152,47,29.333,C.v,true);}
 else if(n===5 || n===10){text(slide,answers[1],64,y,1152,45,29.333,C.v,true);text(slide,answers[2],64,y+58,1152,45,29.333);}
 else if(row.id==='Q15-answer'){answers.forEach((t,i)=>text(slide,t,64,451+i*66,1152,52,29.333,i===0?C.v:C.ink,i===0));}
 else resultLines(slide,answers,y);
}
function treeNode(slide,node){
 const o=rect(slide,node.x,node.y,node.w,node.h,'#FFFFFF',C.v,2,'tree-'+node.id);
 text(slide,node.label,node.x+12,node.y+4,node.w-24,node.h-8,29.333,C.ink,false,'tree-label-'+node.id);
 return o;
}
function clearFocus(slide){
 for(const o of slide.shapes.items){if(o.name==='tree-focus')o.line={fill:'none',width:0};if(o.name==='tree-new')o.text='';}
}
for(const row of plan){
 let slide;
 if(row.stage==='opening'){
  slide=p.slides.add();frame(slide,'音频数字化');
  const heading=slide.shapes.items.find(x=>x.name==='question-title');heading.text='';
  text(slide,'音频数字化',90,114,1100,110,80,C.ink,true);
  text(slide,'一段声音怎样变成\n二进制数据？',90,264,1100,175,65,C.ink,true);
  text(slide,'从波形到未压缩 PCM WAV',90,512,1100,75,49.333,C.grey);
 }else if(row.stage.startsWith('tree')){
  if(row.stage==='tree-summary'){
   if(lastTree){slide=lastTree.duplicate();clearFocus(slide);slide.shapes.items.find(o=>o.name==='question-title').text=row.title;}
   else{slide=p.slides.add();frame(slide,row.title);treeNode(slide,model.tree.root);}
  }else{
   slide=built.get(row.pair).duplicate();clearFocus(slide);
   const node=model.tree.nodes.find(n=>n.id===row.focus);const target=treeNode(slide,node);
   const source=slide.shapes.items.find(o=>o.name==='tree-'+node.parent);
   slide.shapes.connect(source,target,{kind:'elbow',fromSide:node.id==='constraints'?'bottom':'right',toSide:'left',line:{fill:C.v,width:2}});
   rect(slide,node.x-4,node.y-4,node.w+8,node.h+8,'none',C.r,4,'tree-focus');
   text(slide,'新增',node.x+node.w+6,node.y+16,60,40,29.333,C.ink,true,'tree-new');
  }
  lastTree=slide;
 }else if(row.pair){
  const base=plan.find(x=>x.id===row.pair);slide=built.get(row.pair).duplicate();evidence(slide,row,base);
 }else{
  slide=p.slides.add();frame(slide,row.title);row.visible.forEach((t,i)=>text(slide,t,64,169+i*53,1152,47,29.333,C.ink,false,'given-'+i));neutral(slide,row);
 }
 slide.speakerNotes.textFrame.setText(row.notes+'\n[来源]\ncourse-design.qmd C3–C8；assets/audio-manifest.json；https://www.analog.com/media/en/training-seminars/tutorials/MT-002.pdf；https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf；https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/ns-mmeapi-waveformatex');
 slide.moveTo(p.slides.items.length-1);
 built.set(row.id,slide);
}
await fs.mkdir(path.join(ROOT,'.build/v4'),{recursive:true});
const candidate=path.join(ROOT,'.build/v4/audio-candidate.pptx');
await(await PresentationFile.exportPptx(p)).save(candidate);
await fs.writeFile(path.join(ROOT,'validation/v4/deck-map.json'),JSON.stringify({version:model.version,slides:p.slides.items.length,roster:plan.map(r=>({page:r.page,id:r.id,q:r.q,stage:r.stage,pair:r.pair,tree_nodes:r.tree_nodes}))},null,2)+'\n');
console.log(JSON.stringify({slides:p.slides.items.length,candidate}));
