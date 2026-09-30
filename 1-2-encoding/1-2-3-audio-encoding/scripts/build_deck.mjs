// Native editable production deck. All question/reveal wording and notes derive from course-design.qmd.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const require=createRequire(path.join(ROOT,'.build','package.json'));
const {Presentation,PresentationFile}=await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const W=1280,H=720;
const C={rail:'#6251B1',v:'#8C64E1',c:'#15B5CE',r:'#E65050',ink:'#262626',grey:'#737373',grid:'#D8D8DF'};
const F={body:'Alibaba PuHuiTi 3.0 55 Regular',title:'Alibaba PuHuiTi 3.0 115 Black'};
const p=Presentation.create({slideSize:{width:W,height:H}});
const md=await fs.readFile(path.join(ROOT,'course-design.qmd'),'utf8');
const parts=[...md.matchAll(/^## Q(\d+) (.+)\n([\s\S]*?)(?=^## Q\d+ |^# C6)/gm)];
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
const intro=p.slides.add();intro.background.fill='#FFFFFF';rect(intro,0,0,W,10.666,C.rail,'none',0);rect(intro,0,H-10.666,W,10.666,C.rail,'none',0);
text(intro,'音频数字化',90,114,1100,110,80,C.ink,true);
text(intro,'一段声音怎样变成\n二进制数据？',90,264,1100,175,65,C.ink,true);
text(intro,'从波形到未压缩 PCM WAV',90,512,1100,75,49.333,C.grey);
intro.speakerNotes.textFrame.setText('[页面目的] 从图像数字化迁移到音频数字化。\n[教师逐字稿] 上节课我们用有限位置和有限颜色记录熊猫。今天这段音乐没有看得见的像素，要找出记录它的规则。先听同一段声音的两个版本，保留你的猜测。\n[课堂条件] 45分钟；教师Windows/WPS/JupyterLab演示，学生纸笔讨论。音频已离线预制，播放前检查音量。\n[来源] 用户指定熊猫v3课件仅作教学组织参考；音乐为用户提供《逆战》45–51秒片段。');
const roster=[];
for(const part of parts){
 const n=Number(part[1]),title=part[2],body=part[3];
 const givens=section(body,'投影提问').split('\n').filter(Boolean),answers=section(body,'揭示').split('\n').filter(Boolean);
 const q=p.slides.add();frame(q,title);
 givens.forEach((t,i)=>text(q,t,64,169+i*53,1152,47,29.333,C.ink,false,'given-'+i));
 // Neutral evidence on question pages contains no solved calculation, focus color or answer.
 if(n===2)waveform(q,{x:160,y:440,w:950,h:160,label:false});
 if(n===3)waveform(q,{x:160,y:385,w:950,h:155,label:true});
 if(n===6){[0,1,2,3].forEach((v,i)=>{text(q,String(v),240+i*220,296,130,48,40,C.ink,true,'level-'+i);});}
 if(n===7){[0,1,2,3].forEach((v,i)=>rect(q,260+i*185,308,132,52,'none',C.grid,1,'code-box'));['00','01','10','11'].forEach((v,i)=>text(q,v,275+i*185,314,115,43,32));}
 if(n===13){text(q,'L',125,350,50,48,32);text(q,'R',125,430,50,48,32);[0,1,2].forEach(i=>{rect(q,240+i*260,352,150,48,'none',C.grid,1);rect(q,240+i*260,432,150,48,'none',C.grid,1);text(q,`时刻${i+1}`,240+i*260,295,210,45,29.333);});}
 q.speakerNotes.textFrame.setText(`[问题] ${title}\n[内部编号] Q${n} 提问页\n[课堂当前动作] 先保持提问页，等待预测／讨论，不提前翻到答案。\n[教师逐字稿] ${section(body,'教师逐字稿')}\n[认知起点] ${section(body,'认知起点')}\n[认知困惑] ${section(body,'认知困惑')}\n[学生任务] ${section(body,'学生任务')}\n[预期学生反应] ${section(body,'预期回答')}\n[追问问题] ${section(body,'追问')}\n[Demo操作] ${section(body,'Demo 操作')||'无需现场运行。'}\n[显隐] 学生作答前不展示揭示内容。技术边界与来源不投影。`);
 const a=q.duplicate(); // Actual duplication preserves every pre-existing object and title.
 let y=385;
 if(n===2)y=560;
 if(n===3){for(let k=0;k<12;k++)dot(a,160+k*950/12,385-.8*Math.sin(4*Math.PI*k/12+.3)*155/2);y=558;}
 if(n===5){
  ['−0.62','−0.10','0.38','0.84'].forEach((v,i)=>text(a,v,115+i*280,325,245,42,29.333,C.ink));
  ['−0.75','−0.25','0.25','0.75'].forEach((v,i)=>text(a,`↓  ${v}`,115+i*280,385,245,42,29.333,C.v,true));y=485;
 }
 if(n===6){['00','01','10','11'].forEach((v,i)=>text(a,v,240+i*220,358,130,48,40,C.v,true));y=453;}
 if(n===7)y=425;
 if(n===13){[0,1,2].forEach(i=>{text(a,`L${i+1}`,265+i*260,359,105,40,29.333,C.v);text(a,`R${i+1}`,265+i*260,439,105,40,29.333,C.c);});y=540;}
 // Q10 uses real mathematical samples; both comparisons share sample times and amplitude range.
 if(n===10){
  const x0=120,x1=690,w=440,cy=390,scale=78;
  for(const [x0a,bits,color] of [[x0,2,C.v],[x1,4,C.c]]){
   text(a,`${bits} bit：${2**bits}级`,x0a,280,470,43,32,color,true);
   line(a,x0a,cy,x0a+w,cy,C.grid,1);
   const pts=Array.from({length:241},(_,i)=>[x0a+w*i/240,cy-.68*Math.sin(4*Math.PI*i/240+.3)*scale]);pathCurve(a,pts,C.grey,2,'reference-wave');
   for(let k=0;k<48;k++){const z=.68*Math.sin(4*Math.PI*k/48+.3),ind=Math.floor((z+1)*2**bits/2),r=-1+(ind+.5)*2/2**bits,xx=x0a+w*k/48;line(a,xx,cy-z*scale,xx,cy-r*scale,C.r,2,'quantization-error');dot(a,xx,cy-r*scale,color,8);}
  }
  text(a,'同一时刻、同一幅度范围；红色线段表示近似误差',64,494,1152,45,29.333,C.ink);y=566;
 }
 if(n===2){text(a,'声压变化 → 麦克风 → 电信号',64,y,1152,47,32,C.v,true);text(a,'横轴：时间；纵轴：信号幅度',64,y+60,1152,47,29.333);}
 else if(n===3){text(a,answers[0],64,y,1152,45,29.333,C.v,true);text(a,answers[1],64,y+54,1152,45,29.333);}
 else if(n===13){text(a,answers[1],64,y,1152,47,29.333);text(a,answers[2],64,y+59,1152,47,29.333,C.v,true);}
 else if(n===5){text(a,answers[1],64,y,1152,45,29.333,C.v,true);text(a,answers[2],64,y+58,1152,45,29.333);}
 else if(n===10){text(a,answers[1],64,y,1152,45,29.333,C.v,true);text(a,answers[2],64,y+53,1152,45,29.333);}
 else resultLines(a,answers,y);
 const source=n<=12?'https://wiki.analog.com/university/courses/electronics/text/chapter-20\nhttps://www.analog.com/media/en/training-seminars/tutorials/MT-002.pdf\nhttps://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf':'https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/ns-mmeapi-waveformatex\nhttps://docs.python.org/3/library/wave.html';
 a.speakerNotes.textFrame.setText(`[问题] ${title}\n[内部编号] Q${n} 揭示页\n[教师逐字稿] ${section(body,'教师逐字稿')}\n[形成结论] ${section(body,'形成结论')}\n[追问问题] ${section(body,'追问')}\n[预期学生反应] ${section(body,'预期回答')}\n[Demo操作] ${section(body,'Demo 操作')||'使用课件证据，无需现场运行。'}\n[下一问] ${section(body,'下一问')}\n[技术注解] ${n===10?'有效2/4/8bit量化模型装在16bit PCM中，按真实文件位数计数。':n===8?'正常降采样先低通；纯音低通后消失不等于出现混叠。fs>2fmax是带限理想条件，真实需滤波余量。':n===17?'32,000B为实际payload，44B仅该简单WAV开销，不概括所有WAV。':n===14?'WAV是容器，本课仅未压缩整数PCM；M4A解码为PCM不恢复已丢失信息。':section(body,'形成结论')}\n[来源] ${source}\n[证据文件] assets/audio-manifest.json\n[完整备课依据] course-design.qmd Q${n}及C3–C5。`);
 roster.push({q:n,title,questionSlide:2*n,answerSlide:2*n+1,givens,answers});
}
const end=p.slides.add();frame(end,'课后练习');
['1. 22.05kHz、16bit、单声道，10秒有多少B样本数据？','2. 4bit改为8bit，等级数变成原来的几倍？','3. 8kHz录音转为48kHz，能恢复未记录的6kHz吗？','计算写出单位；解释写出条件。'].forEach((t,i)=>text(end,t,64,210+i*94,1152,58,29.333,i===3?C.v:C.ink));
end.speakerNotes.textFrame.setText('[页面目的] 课后迁移，检验采样率、量化位数与样本数据量。\n[教师逐字稿] 三题分别检查计数、等级和信息能否恢复。第一题写全四个参数和除以八，后两题必须写理由。\n[教师答案] 441,000B；16倍；不能恢复当初未记录或已丢失的内容。\n[技术注解] 只计未压缩PCM样本数据；不含WAV头。');
await fs.mkdir(path.join(ROOT,'.build/render-artifact'),{recursive:true});
const candidate=path.join(ROOT,'.build/audio-candidate.pptx');
await(await PresentationFile.exportPptx(p)).save(candidate);
await fs.writeFile(path.join(ROOT,'validation/deck-map.json'),JSON.stringify({slides:40,roster},null,2)+'\n');
// Every native slide is rendered. Full-size individual PNGs are retained for audit.
for(let i=0;i<p.slides.items.length;i++){
 const b=await p.export({slide:p.slides.items[i],format:'png',scale:1.5});
 await fs.writeFile(path.join(ROOT,'.build/render-artifact',String(i+1).padStart(2,'0')+'.png'),new Uint8Array(await b.arrayBuffer()));
}
console.log(JSON.stringify({slides:p.slides.items.length,questions:roster.length,candidate}));
