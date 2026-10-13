import fs from 'node:fs/promises';
import path from 'node:path';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
import {GlobalFonts,createCanvas} from '@napi-rs/canvas';
import {spawnSync} from 'node:child_process';

const ROOT=path.dirname(new URL(import.meta.url).pathname);
const stage=Number(process.argv[2]??1);
const F={regular:'Alibaba PuHuiTi 3.0 55 Regular',black:'Alibaba PuHuiTi 3.0 115 Black'};
for(const [file,family] of [['55-Regular',F.regular],['115-Black',F.black]])GlobalFonts.registerFromPath(`/Users/chran/Library/Fonts/AlibabaPuHuiTi-3-${file}.ttf`,family);
const C={rail:'#6251B1',violet:'#8C64E1',cyan:'#007C9B',outlineCyan:'#00B0F0',ink:'#262626',gray:'#808080',grid:'#D7D7DE',red:'#FF0000'};
const input=stage===1?path.join(ROOT,'baseline.pptx'):path.join(ROOT,`round${stage-1}-after.pptx`);
const p=await PresentationFile.importPptx(await FileBlob.load(input));
const W=p.slides.items[0].frame.width;
const snap=(await p.inspect({kind:'shape,textbox',limit:12000,maxChars:5000000})).ndjson.split('\n').filter(Boolean).map(t=>JSON.parse(t));
const baseline=JSON.parse(await fs.readFile(path.join(ROOT,'baseline-inspection.json'),'utf8'));
const manifest=[];
const t=o=>String(o.text);
const slide=n=>p.slides.items[n-1];
const find=(n,value)=>slide(n).shapes.items.find(o=>t(o)===value);
const title=n=>slide(n).shapes.items.find(o=>o.name==='question-title');
const body=n=>slide(n).shapes.items.filter(o=>t(o)&&o.name!=='question-title');
const deletedIds=new Set();
function removeWhere(n,predicate){
 const ids=snap.filter(e=>!deletedIds.has(e.id)&&e.slideIndex===n-1&&['shape','textbox'].includes(e.kind)).filter(e=>predicate(p.resolve(e.id))).map(e=>e.id);
 if(ids.length){p.delete(ids);ids.forEach(id=>deletedIds.add(id));}
}
function clear(n){removeWhere(n,o=>!['top-rail','bottom-rail','question-title'].includes(o.name));}
function txt(n,text,x,y,w=1152,h=44,size=29.333,color=C.ink,bold=false,name='text',align='left'){
 const o=slide(n).shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0},shadow:'shadow-none'});
 o.text=text;o.text.style={typeface:bold?F.black:F.regular,bold,fontSize:size,color,alignment:align,verticalAlignment:'top',autoFit:'none',wrap:'none',insets:0};return o;
}
function rect(n,x,y,w,h,color=C.grid,fill='none',name='diagram-box',width=1.5){return slide(n).shapes.add({geometry:'rect',name,position:{left:x,top:y,width:w,height:h},fill,line:{fill:color,width},shadow:'shadow-none'});}
function curve(n,points,color=C.gray,width=1.5,name='curve'){
 const xs=points.map(v=>v[0]),ys=points.map(v=>v[1]);const x=Math.min(...xs),y=Math.min(...ys),w=Math.max(1,Math.max(...xs)-x),h=Math.max(1,Math.max(...ys)-y);
 return slide(n).shapes.add({geometry:'custom',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:color,width},shadow:'shadow-none',customPaths:[{width:w,height:h,commands:points.map((v,i)=>({[i?'lineTo':'moveTo']:{x:v[0]-x,y:v[1]-y}}))}]});
}
function line(n,x1,y1,x2,y2,color=C.grid,width=1.5,name='line'){return curve(n,[[x1,y1],[x2,y2]],color,width,name);}
function dot(n,x,y,color=C.violet,size=12,hollow=false,name='sample'){return slide(n).shapes.add({geometry:'ellipse',name,position:{left:x-size/2,top:y-size/2,width:size,height:size},fill:hollow?'#FFFFFF':color,line:{fill:color,width:hollow?2:0},shadow:'shadow-none'});}
function arrow(n,x,y,w=48,color=C.violet,name='mapping-arrow'){return slide(n).shapes.add({geometry:'rightArrow',name,position:{left:x,top:y,width:w,height:20},fill:color,line:{fill:'none',width:0},shadow:'shadow-none'});}
function append(n,text){slide(n).speakerNotes.append('\n'+text);}
const shortTitles={
 2:'文字、图像能编码，声音呢？',8:'波形图是声音的传播路线吗？',9:'演示A：红线向右，表示什么？',10:'只能留下有限个数字，该在哪些时刻取样？',11:'每隔相同时间，取一个幅度值',12:'演示B：放大后，能看见采样点吗？',14:'提高采样率，时间轴上的什么变了？',15:'采样值可能是3.71，怎样记录？',18:'量化：用有限代表值近似样本',19:'10个样本，怎样依次编码？',20:'3.71为什么写成011，而不是100？',23:'采样率与量化位数，分别控制什么？',24:'演示C：3bit变4bit，样本点会变多吗？',26:'3bit模型与16bit实际存储',28:'播放时，数字样本怎样变成声音？',30:'先数样本，再数bit，最后换成Byte',41:'编辑音轨与输出声道，有什么不同？',45:'连续的图片，怎样让我们看到运动？',46:'10分钟、25fps，要保存多少帧？',49:'视频文件为什么可能小于6.44 GiB？',50:'刚才计算的是逐帧未压缩数据量',52:'“中国”重复100次，怎样写得更短？',54:'两份都是1000Byte，压缩后谁更小？',55:'演示D：同样1000Byte，压缩后会相同吗？',56:'同样原始大小，压缩结果为何不同？',58:'无损与有损：按什么区分？',59:'ZIP、MP3、WAV、MP4，是同一层吗？',60:'相同尺寸的三幅图，谁容易无损压缩？',64:'MP3、JPG再用RAR压缩，会怎样？',68:'离开课堂前，解释三个为什么',70:'可选拓展：编码与压缩不同'
};
const questions=new Set([2,10,15,17,32,37,39,47,49,54,61,66,68]);
const practicePairs=[[32,33],[37,38],[39,42],[47,48],[61,62],[66,67]];

if(stage===1){
 for(let n=1;n<=70;n++){
  const s=slide(n);const layout=JSON.parse(await fs.readFile(path.join(ROOT,'baseline-render',`slide-${String(n).padStart(2,'0')}.layout.json`),'utf8'));
  for(const o of s.shapes.items)o.shadow='shadow-none';
  const rails=s.shapes.items.filter(o=>o.position.width>1250&&o.position.height<14).sort((a,b)=>a.position.top-b.position.top);
  for(const [i,o]of rails.entries()){o.name=i?'bottom-rail':'top-rail';o.position={left:0,top:i?709.333333:0,width:W,height:10.666667};o.line={fill:'none',width:0};o.fill=C.rail;}
  for(const e of layout.elements.filter(e=>e.text)){
   const o=s.shapes.items.find(o=>o.name===e.name);if(!o)throw new Error(`Missing original shape ${n} ${e.name}`);
   const isTitle=e.text===layout.elements.find(e=>e.text).text;const isCover=n===1||n===35;
   const simple=/^[01]+$/.test(e.text)||/^\d+$/.test(e.text)||['振幅','时间'].includes(e.text);
   let size=e.style.fontSize,color=e.style.color,bold=!!e.style.bold;
   if(color?.toUpperCase()==='#00B0F0')color=C.cyan;
   if(color?.toUpperCase()==='#6251B1')color=C.violet;
   if(!simple&&!isCover&&!isTitle)size=Math.max(size,bold?29.333:29.333);
   o.text=e.text;
   o.text.style={typeface:bold?F.black:F.regular,bold,fontSize:size,color,alignment:e.style.alignment??'left',verticalAlignment:'top',wrap:'square',autoFit:'none',insets:0};
   if(isTitle){o.name='question-title';o.position={left:63.84,top:isCover?222:63.84,width:1152,height:isCover?120:74};o.text=shortTitles[n]??e.text.replace(/[。.]$/u,'');o.text.style={typeface:F.black,bold:true,fontSize:isCover?80:48,color:C.ink,alignment:isCover?'center':'left',verticalAlignment:'top',autoFit:'none',wrap:'none',insets:0};}
   else if(isCover){o.position={left:63.84,top:390,width:1152,height:78};o.text.style={typeface:F.regular,fontSize:49.333,color:C.gray,alignment:'center',autoFit:'none',wrap:'none',insets:0};}
   else if(e.position.top>590){o.text.style={typeface:F.regular,bold:false,fontSize:29.333,color:C.ink,autoFit:'none',wrap:'none',insets:0};}
  }
  const oldNotes=s.speakerNotes.text;
  const purpose=t(title(n));
  s.speakerNotes.text=`[问题] ${purpose}\n[内部编号] V81-${String(n).padStart(2,'0')}\n[阶段] ${questions.has(n)?'提问／独立作答':n===1||n===35?'课时开场':'证据／解释'}\n[教师逐字稿]\n${oldNotes}`;
 }
 // Separate axis labels from headings and traces while retaining native evidence.
 for(const n of [8,9,12,13,14,23,69]){
  const axes=slide(n).shapes.items.filter(o=>t(o)==='振幅');
  const times=slide(n).shapes.items.filter(o=>t(o)==='时间');
  for(const o of [...axes,...times]){o.fill='#FFFFFF';o.bringToFront();o.text.fontSize=24;}
  if(n===8){axes[0].position={left:116,top:213,width:100,height:32};times[0].position={left:1090,top:517,width:100,height:32};}
  if(n===9){times[0].position={left:1085,top:523,width:100,height:32};}
  if(n===12){for(let k=0;k<axes.length;k++)axes[k].position={left:k?700:105,top:286,width:100,height:32};for(let k=0;k<times.length;k++)times[k].position={left:k?1095:515,top:489,width:100,height:32};}
  if(n===14){axes.forEach((o,k)=>o.position={left:64,top:k?414:195,width:50,height:32});}
  if(n===23){times[0].position={left:990,top:475,width:110,height:32};const q=find(n,'量化位数\n幅度方向');if(q)q.position={left:935,top:205,width:215,height:85};}
  if(n===69){axes.forEach((o,k)=>o.position={left:64,top:k?414:194,width:50,height:32});}
 }
 // Correct the one-second sampling evidence: use a half-open interval.
 clear(13);
 txt(13,'同一段信号；统计区间 [0,1)，不计右端点。',64,166,1152,44,29.333);
 const sampleModel=t=>.68*Math.sin(2*Math.PI*t+.4);
 for(const [k,rate]of [1,2].entries()){
  const y=k?415:235,h=85,x=235,w=840,Y=v=>y+(1-v)*h/2;
  txt(13,`${rate} Hz`,64,y+23,150,44,32,k?C.cyan:C.violet,true,`rate-${rate}`);
  line(13,x,Y(0),x+w,Y(0),C.gray,1.2,`time-axis-${rate}`);
  curve(13,Array.from({length:151},(_,j)=>{const tm=j/150;return[x+w*tm,Y(sampleModel(tm))];}),C.gray,1.8,`same-signal-${rate}`);
  for(const tm of [0,.5,1]){line(13,x+tm*w,y+h+4,x+tm*w,y+h+10,C.gray,1,`tick-${rate}-${tm}`);txt(13,String(tm),x+tm*w-30,y+h+17,60,30,24,C.gray,false,`time-${rate}-${tm}`,'center');}
  for(let j=0;j<rate;j++){const tm=j/rate;line(13,x+tm*w,Y(0),x+tm*w,Y(sampleModel(tm)),C.grid,1.1,`sample-stem-${rate}-${j}`);dot(13,x+tm*w,Y(sampleModel(tm)),k?C.outlineCyan:C.violet,14,false,`sample-${rate}-${j}`);}
  txt(13,'时间 / s',1090,y+h+13,130,34,24,C.gray,false,`time-unit-${rate}`);
 }
 txt(13,'采样率：每秒、每声道采集的样本数。',64,610,1152,42);
 append(13,'[模型边界]\n图为同一数学示意信号，不是实际录音建议；只用来数记录时刻。1Hz取t=0；2Hz取t=0、0.5s；区间[0,1)。示意不证明重建或听感。');
 // Align a quantization representative to 3.5 rather than its grade number 3.
 clear(18);txt(18,'范围 [0,8)；按 [n,n+1) 分档。',64,166);
 const qx=160,qw=120;
 for(let j=0;j<8;j++){rect(18,qx+j*qw,285,qw,102,j===3?C.red:C.grid,'none',`quant-bin-${j}`,j===3?3:1);txt(18,`L${j}`,qx+j*qw,407,qw,40,28,j===3?C.violet:C.gray,j===3,`quant-grade-${j}`,'center');}
 for(let j=0;j<=8;j++)txt(18,String(j),qx+j*qw-30,245,60,32,24,C.gray,false,`quant-boundary-${j}`,'center');
 const rawX=qx+3.71*qw,repX=qx+3.5*qw;
 dot(18,rawX,321,C.red,15,true,'raw-3.71');line(18,rawX,318,rawX,230,C.red,1.3,'raw-label-guide');txt(18,'原值 3.71',rawX+15,209,240,42,29.333,C.ink,true,'raw-value-label');
 dot(18,repX,365,C.outlineCyan,15,false,'representative-3.5');line(18,repX,370,repX,388,C.cyan,1.3,'representative-guide');
 txt(18,'等级编号 L3；对应代表值 3.5',320,496,760,48,32,C.violet,true,'quant-mapping','center');
 txt(18,'编号表示哪一档；代表值用于近似原幅度。',64,610,1152,42);
 append(18,'[图示条件]\n横坐标表示输入幅度，区间[3,4)归为L3；以中点3.5近似3.71。等级编号3不是幅度代表值3.5。Demo C使用另一个幅度范围，不混用数值。');
 // Give the file-header and sample captions their own columns.
 const h=find(27,'采样率、声道等说明');if(h){h.text='采样率、声道\n等参数';h.position={left:98,top:405,width:270,height:95};h.text.wrap='square';}
 const d=body(27).find(o=>t(o).startsWith('例如：'));if(d)d.position={left:450,top:405,width:700,height:80};
 // Clarify the bit-packed teaching model before actual PCM storage calculations.
 txt(30,'3bit教学模型：码字连续打包；不是实际16bit PCM文件。',64,156,1152,42,29.333,C.ink,false,'packed-model-condition');
 const packedCount=body(30).find(o=>t(o).startsWith('2 样本/秒'));if(packedCount)packedCount.position={...packedCount.position,top:218,height:56};
 append(30,'[计数边界]\n这里8个3bit码字连续打包为24bit，即3Byte，不包含结构或填充。实际PCM容量使用每样本存储位宽；不能把真实16bit PCM文件按有效3bit计算。');
 // Replace dense one-line arithmetic with the intended counting sequence.
 for(const [q,a]of practicePairs){
  for(const n of [q,a]){const b=body(n)[0];b.name='practice-givens';b.position={left:82.56,top:177.6,width:1118.4,height:q===66?270:185};b.text.style={typeface:F.regular,fontSize:36,color:C.ink,wrap:'square',autoFit:'none',insets:0};}
 }
 const work={33:['每声道：16,000 × 5＝80,000 个样本','每样本：8 bit ÷ 8＝1 Byte','双声道：80,000 × 2 × 1＝160,000 Byte'],38:['每声道：48,000 × 60＝2,880,000 个样本','每样本：16 bit ÷ 8＝2 Byte','总量：2,880,000 × 2声道 × 2＝11,520,000 B','换算：11,520,000 ÷ 1024² ≈ 10.99 MiB'],48:['单帧：480 × 320 × 24 ÷ 8＝460,800 B','帧数：25 × 10 × 60＝15,000 帧','总量：460,800 × 15,000＝6,912,000,000 B','换算：6,912,000,000 ÷ 1024³ ≈ 6.44 GiB']};
 for(const [key,lines]of Object.entries(work)){
  const n=Number(key);removeWhere(n,o=>t(o)&&o.name!=='question-title'&&o.name!=='practice-givens');
  lines.forEach((v,k)=>txt(n,v,86,369+k*50,1120,42,29.333,C.ink,false,`calculation-step-${k}`));
  const ans=n===33?'答案：160,000 Byte':n===38?'答案：约10.99 MiB':'答案：约6.44 GiB';txt(n,ans,86,594,1120,48,36,C.violet,true,'practice-answer');
 }
 // Remove legacy outline effects and orphan punctuation in the compression comparison.
 for(const label of ['无损压缩','有损压缩']){const o=find(58,label);removeWhere(58,v=>t(v)===label);txt(58,label,label.startsWith('无')?86.4:675.84,182.4,533,58,37.333,label.startsWith('无')?C.violet:C.cyan,false,'compression-kind-'+label);}
 for(const o of body(58))if(t(o).startsWith('还原以后')){o.text=t(o).includes('无法')?'解码后不能完全恢复原始数据。\n适合：允许一定失真的音视频。':'解压后与原始数据完全一致。\n适合：文档、程序、精确备份。';o.text.style={typeface:F.regular,fontSize:29.333,color:C.ink,wrap:'square',autoFit:'none',insets:0};}
 body(68).forEach((o,k)=>{o.position={left:82.56,top:205+k*150,width:1120,height:70};o.text.style={typeface:F.black,bold:true,fontSize:32,color:C.ink,autoFit:'none',wrap:'none',insets:0};});
 const deliberateBreaks={
  40:['采样率没变，位数没变，时长没变，\n输出的声道数也没变。','录音里多了一份音乐，\n是不是就需要多一份音频数据？'],
  50:['利用帧间相似和更有效的编码，\n数据可能显著减小'],
  51:['同样容量的手机或硬盘，\n可以保存更多数据。','需要传输的数据更少，\n通常能更快下载或播放。'],
  63:['对图像进行近似表示。\n\n文件可能明显更小，\n但不能逐像素完全还原。'],
  64:['有些重复或不重要的信息\n被更简洁地表示，文件大幅减小。','可进一步利用的冗余通常较少，\nRAR再压往往收效不大。'],
  65:['优先考虑信息完整、能够恢复，\n以及可靠保存。','优先兼顾流畅度、延迟，\n声音画面质量和传输量。'],
  70:['让连续声音能够用数字样本记录；\n也包括后续数据表示。','用更少的比特表达\n相同或近似相同的信息。']
 };
 for(const [key,values]of Object.entries(deliberateBreaks)){
  const n=Number(key);const old=body(n).filter(o=>o.position.top>250&&o.position.top<590&&o.position.width>450&&t(o).length>12);
  if(n===50||n===63){old[old.length-1].text=values[0];}
  else old.forEach((o,k)=>{if(values[k])o.text=values[k];});
 }
}

if(stage===2){
 const prompts=JSON.parse(await fs.readFile(path.join(ROOT,'image-prompts.json'),'utf8'));
 // Meaningful situation imagery remains separate from exact technical evidence.
 clear(2);txt(2,'文字 → 编码',64,225,550,60,37.333,C.violet,true,'known-text');txt(2,'图像 → 编码',64,335,550,60,37.333,C.cyan,true,'known-image');txt(2,'声音 → ？',64,445,550,60,44,C.ink,true,'current-question');
 txt(2,'手机为什么能把说话声保存成文件？',64,610,1152,44,29.333,C.ink,false,'recording-question');
 const files=['voice-recording-context.png','document-backup-context.png','video-call-context.png'];
 for(let i=0;i<files.length;i++){
  const bytes=await fs.readFile(path.join(ROOT,'images',files[i]));const n=i===0?2:65;
  if(i===1){clear(65);txt(65,'重要文档长期备份',64,167,544,54,32,C.violet,true,'backup-title');txt(65,'实时视频通话',672,167,544,54,32,C.cyan,true,'call-title');}
  slide(n).images.add({blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:'image/png',alt:prompts[i].name,fit:'contain',position:i===0?{left:670,top:166,width:536,height:402}:{left:i===1?64:672,top:241,width:544,height:294},geometry:'rect'});
  append(n,`[图片生成提示词]\n${prompts[i].id}；用途：情境插图，不作为技术或软件事实证据。\n${prompts[i].prompt}\n[图片编辑]\n使用原图，等比contain，无拉伸、无二次编辑；精确标签为原生PPT对象。`);
 }
 txt(65,'优先：信息完整、能恢复、可靠保存。',64,551,544,80,29.333,C.ink,false,'backup-criteria');
 txt(65,'兼顾：延迟、流畅度、质量与传输量。',672,551,544,80,29.333,C.ink,false,'call-criteria');
 // Make one sample's index-to-code mapping easy to follow.
 rect(19,291,179,67,259,C.red,'none','first-sample-focus',3);
 append(19,'[观察顺序]\n先只看红框内的第一个样本：顺序1，量化等级3，等长码字011。让学生沿列互读，再看其余九列；不是把3bit当作幅度值。');
 // Relate sixteen stored bits to two byte groups, without changing their values.
 txt(26,'8bit＝1B',500,365,165,42,29.333,C.cyan,true,'stored-byte-1');txt(26,'8bit＝1B',500,435,165,42,29.333,C.cyan,true,'stored-byte-2');txt(26,'共16bit＝2B',684,535,460,44,29.333,C.cyan,true,'stored-sample-bytes');
 // Draw the many-to-mix-to-output relation rather than implying track/channel pairing.
 clear(41);txt(41,'编辑时：两条音轨',64,166,430,44,32,C.violet,true);txt(41,'输出时：两个声道',830,166,386,44,32,C.cyan,true);
 for(const [k,label]of ['音轨1：诗朗诵','音轨2：背景音乐'].entries()){rect(41,64,275+k*160,365,76,C.violet,'none',`track-${k}`);txt(41,label,83,295+k*160,325,44,29.333,C.ink,false,`track-label-${k}`);}
 rect(41,536,353,208,76,C.violet,'none','mix-operation');txt(41,'混音导出',551,373,178,44,29.333,C.ink,true,'mix-label','center');
 for(const [k,label]of ['左声道 L','右声道 R'].entries()){rect(41,850,275+k*160,366,76,C.outlineCyan,'none',`output-${k}`);txt(41,label,867,295+k*160,330,44,29.333,C.cyan,true,`output-label-${k}`);line(41,744,391,808,391,C.violet,2,`split-${k}`);line(41,808,391,808,313+k*160,C.violet,2,`split-branch-${k}`);arrow(41,809,303+k*160,34);}
 line(41,429,313,490,313,C.violet,2,'merge-upper');line(41,429,473,490,473,C.violet,2,'merge-lower');line(41,490,313,490,473,C.violet,2,'merge-branch');arrow(41,490,381,40);
 txt(41,'两条音轨共同参与混音；输出仍可为 L、R 两路。',64,610);
 // Show three equal instants on both channel examples.
 clear(43);txt(43,'相同采样率、存储位宽与时长；这里只改变声道数。',64,166);
 const labels=[['双声道','L','R'],['单声道','单路']];
 labels.forEach((group,k)=>{const left=k?706:96;txt(43,group[0],left,250,420,48,32,k?C.cyan:C.violet,true,`channel-group-${k}`);group.slice(1).forEach((label,row)=>{txt(43,label,left,335+row*110,72,44,29.333,C.ink,true,`channel-label-${k}-${row}`);for(let j=0;j<3;j++){rect(43,left+105+j*96,325+row*110,70,62,k?C.outlineCyan:C.violet,'none',`channel-sample-${k}-${row}-${j}`);txt(43,(row?-.3+j*.2:.2+j*.1).toFixed(1),left+107+j*96,339+row*110,66,40,24,C.ink,false,`channel-value-${k}-${row}-${j}`,'center');}});for(let j=0;j<3;j++)txt(43,`t${j}`,left+105+j*96,300,70,32,24,C.gray,false,`channel-instant-${k}-${j}`,'center');});
 rect(43,195,321,83,180,C.red,'none','same-instant-stereo',3);txt(43,'同一时刻：2个样本',96,542,420,44,29.333,C.violet,true,'two-samples');txt(43,'同一时刻：1个样本',706,542,510,44,29.333,C.cyan,true,'one-sample');txt(43,'其他条件相同：单声道的PCM样本数据量为原来一半。',64,610);
 append(43,'[计数模型]\n三个时刻t0/t1/t2，双声道共6个样本，单声道3个。各值是计数示意，不是音轨混音结果，也不规定立体声转单声道的混音算法。');
 // Use a common scale for the actual compression-size comparison.
 clear(56);
 for(const [k,label,size,color]of [[0,'A：重复的内容',17,C.violet],[1,'B：复杂的内容',1011,C.cyan]]){
  const x=k?672:64;txt(56,label,x,167,544,54,32,color,true,`compression-header-${k}`);txt(56,'原始：1000 Byte',x,253,544,42,29.333,C.ink,false,`original-count-${k}`);rect(56,x,304,500,30,'none','#D7D7DE',`original-bar-${k}`,0);txt(56,`压缩后：${size} Byte`,x,385,544,44,32,color,true,`compressed-count-${k}`);rect(56,x,443,500*size/1000,30,'none',color,`compressed-bar-${k}`,0);
  if(k){rect(56,x+500,443,500*11/1000,30,'none',C.red,'extra-eleven-bytes',0);txt(56,'比原始多11 Byte',x,500,544,42,29.333,C.red,false,'compression-extra');}
 }
 txt(56,'同一比例尺；解压后都能逐字节恢复原始数据。',64,610);append(56,'[比例尺]\n两列原始1000B均为500px；17B为8.5px；1011B为505.5px，多11B为5.5px。数值仅对应本次zlib实验；不是普遍压缩率。');
 // Group the PCM formula by what is being counted.
 clear(31);txt(31,'未压缩、固定存储位宽；先算样本数量，再算每份大小。',64,166);
 txt(31,'每声道样本数',64,276,480,46,32,C.violet,true,'count-heading');txt(31,'采样率 × 秒数',64,344,480,48,36,C.ink,true,'count-factors');
 txt(31,'同一时刻的数据量',684,276,532,46,32,C.cyan,true,'width-heading');txt(31,'声道数 ×（存储位宽 ÷ 8）',684,344,532,96,29.333,C.ink,false,'width-factors');
 txt(31,'×',582,337,64,68,48,C.ink,true,'multiply-sign','center');
 txt(31,'PCM样本字节数＝每声道样本数 × 每时刻字节数',64,523,1152,54,32,C.violet,true,'payload-equation');txt(31,'Hz用每秒计数；时长用秒；8 bit＝1 Byte。',64,610);
 append(31,'[公式条件]\n固定宽度未压缩PCM，使用实际存储位宽，不使用有效量化模型位数。每声道样本数优先由实际帧数读取；本例整数时长用fs×秒数。样本数据不含文件结构。');
 // Give the image/audio comparison explicit subject columns.
 txt(44,'图像：空间采样',331,166,410,44,29.333,C.violet,true,'image-column-heading');txt(44,'声音：时间采样',777,166,439,44,29.333,C.cyan,true,'audio-column-heading');
 const rows=[['取样位置','二维：行×列的像素','一维：时间点'],['描述的量','像素的颜色信息','声音信号振幅'],['数据量','像素数×每像素位数','样本数×每样本位数']];
 for(let k=0;k<rows.length;k++)for(let j=0;j<3;j++){const o=find(44,rows[k][j]);if(o)o.position={left:j===0?78:j===1?331:777,top:249+k*116,width:j===0?220:430,height:52};}
}

// Later rounds must repair findings in their own reviewed candidate.
if(stage===3){
 // Filled after the second-round visual audit.
}

const ctx=createCanvas(20,20).getContext('2d');const oversized=[];
for(let n=1;n<=70;n++){
 const s=slide(n);
 manifest.push({page:n,title:t(title(n)),source_title:baseline.slides[n-1].title,source_xml:baseline.slides[n-1].xml_path,stage:questions.has(n)?'question':'evidence',practice_pair:practicePairs.find(v=>v.includes(n))??null});
 ctx.font=`bold ${n===1||n===35?80:48}px "${F.black}"`;const width=ctx.measureText(t(title(n))).width;if(width>1152)oversized.push({page:n,text:t(title(n)),width});
}
if(oversized.length)throw new Error('Title overflow: '+JSON.stringify(oversized));
await (await PresentationFile.exportPptx(p)).save(path.join(ROOT,`round${stage}-after.pptx`));
const patched=spawnSync('/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',[path.join(ROOT,'patch_font_defaults.py'),path.join(ROOT,`round${stage}-after.pptx`)],{encoding:'utf8'});
if(patched.status!==0)throw new Error(patched.stderr);
await fs.writeFile(path.join(ROOT,`round${stage}-plan.json`),JSON.stringify({version:'audio-v8.1.codex-20261013',stage,slideCount:70,baseline_sha256:baseline.sha256,manifest},null,2));
await fs.writeFile(path.join(ROOT,`round${stage}-presentation.json`),JSON.stringify(p.toProto()));
console.log(JSON.stringify({stage,slides:p.slides.items.length,file:path.join(ROOT,`round${stage}-after.pptx`)}));
