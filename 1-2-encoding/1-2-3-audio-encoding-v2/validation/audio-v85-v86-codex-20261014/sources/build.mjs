import fs from 'node:fs/promises';
import path from 'node:path';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
import {GlobalFonts,createCanvas} from '@napi-rs/canvas';
import {spawnSync} from 'node:child_process';
const SOURCE=path.dirname(new URL(import.meta.url).pathname);
const RECORD=path.resolve(SOURCE,'..');
const ROOT=path.resolve(process.env.AUDIO_BUILD_DIR??path.join(RECORD,'rebuild'));
const LESSON=path.resolve(process.env.AUDIO_LESSON_DIR??path.join(RECORD,'../..'));
await fs.mkdir(ROOT,{recursive:true});await fs.cp(path.join(RECORD,'assets'),path.join(ROOT,'assets'),{recursive:true});await fs.copyFile(path.join(RECORD,'pre-authoring-plan.json'),path.join(ROOT,'pre-authoring-plan.json'));
const PYTHON=process.env.AUDIO_PYTHON??'python3';
const phase=Number(process.argv[2]??0);
const INPUT=phase===0?path.join(LESSON,'1-2-3-audio-encoding-v8.1.codex.pptx'):path.join(ROOT,phase===1?'v85-candidate.pptx':'round1-candidate.pptx');
const F={regular:'Alibaba PuHuiTi 3.0 55 Regular',black:'Alibaba PuHuiTi 3.0 115 Black'};
for(const [file,family] of [['55-Regular',F.regular],['115-Black',F.black]])GlobalFonts.registerFromPath(`/Users/chran/Library/Fonts/AlibabaPuHuiTi-3-${file}.ttf`,family);
const C={rail:'#6251B1',violet:'#8C64E1',cyan:'#007C9B',outlineCyan:'#00B0F0',ink:'#262626',gray:'#808080',grid:'#D7D7DE',red:'#FF0000'};
const p=await PresentationFile.importPptx(await FileBlob.load(INPUT));
const snap=(await p.inspect({kind:'shape,textbox,image',limit:20000,maxChars:6000000})).ndjson.split('\n').filter(Boolean).map(t=>JSON.parse(t));
const sourceSlides=[...p.slides.items];
const priorPlan=phase===0?null:JSON.parse(await fs.readFile(path.join(ROOT,phase===1?'v85-plan.json':'round1-plan.json'),'utf8'));
const keyed=new Map(sourceSlides.map((s,i)=>[phase===0?`p${i+1}`:priorPlan.slides[i].key,s]));
const metadata=new Map(sourceSlides.map((s,i)=>[s,phase===0?{key:`p${i+1}`,base81:i+1,role:'retained'}:{...priorPlan.slides[i]}]));
const s=n=>typeof n==='number'?keyed.get(`p${n}`):n;
const t=o=>String(o.text);
const heading=n=>s(n).shapes.items.find(o=>o.name==='question-title');
const pos=o=>({left:o.position.left,top:o.position.top,width:o.position.width,height:o.position.height});
const deleted=new Set();
function removeWhere(n,fn){const idx=sourceSlides.indexOf(s(n));const ids=snap.filter(e=>!deleted.has(e.id)&&e.slideIndex===idx).filter(e=>fn(p.resolve(e.id),e)).map(e=>e.id);if(ids.length){p.delete(ids);ids.forEach(id=>deleted.add(id));}}
function clear(n){removeWhere(n,o=>!['top-rail','bottom-rail','question-title'].includes(o.name));}
function txt(n,text,x,y,w=1152,h=44,size=29.333,color=C.ink,bold=false,name='text',align='left'){
 const o=s(n).shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0},shadow:'shadow-none'});
 o.text=text;o.text.style={typeface:bold?F.black:F.regular,bold,fontSize:size,color,alignment:align,verticalAlignment:'top',autoFit:'none',wrap:text.includes('\n')?'square':'none',insets:0};return o;
}
function rect(n,x,y,w,h,color=C.grid,fill='none',name='diagram-box',width=1.5){return s(n).shapes.add({geometry:'rect',name,position:{left:x,top:y,width:w,height:h},fill,line:{fill:color,width},shadow:'shadow-none'});}
function curve(n,points,color=C.gray,width=1.5,name='curve'){
 const xs=points.map(v=>v[0]),ys=points.map(v=>v[1]);const x=Math.min(...xs),y=Math.min(...ys),w=Math.max(1,Math.max(...xs)-x),h=Math.max(1,Math.max(...ys)-y);
 return s(n).shapes.add({geometry:'custom',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:color,width},shadow:'shadow-none',customPaths:[{width:w,height:h,commands:points.map((v,i)=>({[i?'lineTo':'moveTo']:{x:v[0]-x,y:v[1]-y}}))}]});
}
function line(n,x1,y1,x2,y2,color=C.grid,width=1.5,name='line'){return curve(n,[[x1,y1],[x2,y2]],color,width,name);}
function dot(n,x,y,color=C.violet,size=12,hollow=false,name='sample'){return s(n).shapes.add({geometry:'ellipse',name,position:{left:x-size/2,top:y-size/2,width:size,height:size},fill:hollow?'#FFFFFF':color,line:{fill:color,width:hollow?2:0},shadow:'shadow-none'});}
function arrow(n,x,y,w=48,color=C.violet,name='arrow'){return s(n).shapes.add({geometry:'rightArrow',name,position:{left:x,top:y,width:w,height:20},fill:color,line:{fill:'none',width:0},shadow:'shadow-none'});}
async function img(n,file,position,crop=null,alt='Supplied source image'){
 const bytes=await fs.readFile(path.join(ROOT,'assets',file));return s(n).images.add({blob:bytes,contentType:'image/png',position,fit:crop?'cover':'contain',...(crop?{crop}:{}),geometry:'rect',alt});
}
function notes(n,stage,script,extra=''){s(n).speakerNotes.text=`[问题] ${t(heading(n))}\n[内部编号] ${metadata.get(s(n))?.key??'VISUAL'}\n[阶段] ${stage}\n[教师逐字稿]\n${script}\n${extra}`;}
function addNotes(n,extra){s(n).speakerNotes.append('\n'+extra);}
function questionPair(n,prepare,show,questionScript,revealScript){
 clear(n);prepare(n);const q=s(n),r=q.duplicate();metadata.get(q).role='question';metadata.set(r,{key:`p${n}-reveal`,base81:n,role:'reveal'});
 notes(q,'提问',questionScript);notes(r,'证据揭示',revealScript);show(r);const idx=order.indexOf(q);order.splice(idx+1,0,r);return r;
}
let order=[...sourceSlides];
const model=t=>.72*Math.sin(10*Math.PI*t+.3);
const samples=[3.71,5.2,7.1,6.4,4.15,2.3,.65,1.4,3.2,4.8];
function countBins(n,x,y,w,h,count,focus=-1){for(let j=0;j<count;j++){rect(n,x+j*w/count,y,w/count,h,j===focus?C.red:C.grid,'none',`bin-${count}-${j}`,j===focus?2.5:1);if(count<=8)txt(n,`L${j}`,x+j*w/count,y+h/2-16,w/count,32,24,C.ink,false,`grade-${count}-${j}`,'center');}for(let j=0;j<=count;j++){if(count>8&&j%2)continue;txt(n,String(8*j/count),x+j*w/count-22,y-36,44,30,24,C.gray,false,`bound-${count}-${j}`,'center');}}
function quantGraph(n,x,y,w,h,bits){
 const count=2**bits,Y=v=>y+h*(1-v/8);line(n,x,y,x,y+h,C.gray,1.2,`quant-y-${bits}`);line(n,x,y+h,x+w,y+h,C.gray,1.2,`quant-x-${bits}`);
 for(let j=0;j<count;j++)line(n,x,Y((j+.5)*8/count),x+w,Y((j+.5)*8/count),C.grid,1,`rep-grid-${bits}-${j}`);
 for(let j=0;j<samples.length;j++){const tx=x+j*w/9,v=samples[j],rep=(Math.floor(v/(8/count))+.5)*(8/count);line(n,tx,Y(v),tx,Y(rep),C.gray,1,`error-${bits}-${j}`);dot(n,tx,Y(v),C.ink,10,true,`raw-${bits}-${j}`);dot(n,tx,Y(rep),bits===3?C.violet:C.outlineCyan,8,false,`quantized-${bits}-${j}`);}
}
if(phase===0){
 // Reuse the supplied physical illustration. It is contextual artwork, not measurement evidence.
 clear(3);heading(3).text='振动怎样把声音传到麦克风？';
 await img(3,'physical-sound-context.png',{left:124,top:247,width:1032,height:464.4});
 txt(3,'音叉振动',128,173,304,48,32,C.violet,true,'fork-label');txt(3,'空气中的声压变化',446,173,443,48,32,C.ink,false,'air-label');txt(3,'麦克风接收',913,173,304,48,32,C.cyan,true,'mic-label');
 // Keep artwork below the rail without implying a measured geometry.
 s(3).images.items[0].position={left:124,top:235,width:1032,height:406};
 notes(3,'解释','请看音叉和麦克风。音叉振动，使空气中的声压发生变化；变化传播到麦克风的位置。先请学生用手势指出“振动源”和“接收位置”。接下来要解释麦克风怎样把这种变化变成电信号。','[图示边界]\n复用v8.4.10的程序示意图，圆弧是传播示意，不是空气质点或声音走过的轨迹。原图等比contain，未改写内容。\n[来源]\nv8.4.10 ppt/media/image4.png；validation/audio-v84-20261013/build_ten_visual_rounds.py 的artwork_tuning_fork。');
 clear(7);heading(7).text='录音与播放，各转换了什么？';
 const rows=[['录音',['声音','电信号','数字样本','文件'],['麦克风','ADC','保存']],['播放',['文件','数字样本','电信号','声音'],['读取／解码','DAC','扬声器']]];
 rows.forEach(([label,items,steps],row)=>{const y=277+row*213;txt(7,label,64,y-70,180,46,32,C.ink,true,`process-label-${row}`);items.forEach((v,k)=>{const x=64+k*306;rect(7,x,y,234,70,k===2?C.outlineCyan:C.grid,'none',`process-node-${row}-${k}`);txt(7,v,x+8,y+15,218,46,29.333,k===2?C.cyan:C.ink,false,`process-text-${row}-${k}`,'center');if(k<3){arrow(7,x+244,y+25,51,C.violet,`process-arrow-${row}-${k}`);txt(7,steps[k],x+181,y+90,184,44,24,C.gray,false,`converter-${row}-${k}`,'center');}});});
 notes(7,'解释','先让学生沿上行读录音过程，再沿下行读播放过程。每个箭头都对应一种操作：麦克风转换、ADC、保存；读取文件后取出样本，经DAC和扬声器播放。追问：电脑文件里保存的是空气振动，还是样本的数字表示？','[模型边界]\n简化链路省略放大、滤波与功率放大等；文件可能需要解码才能得到PCM样本。');
 // Preserve the exact question geometry, then reveal one comparison.
 heading(8).text='波形图的横轴，表示距离还是时间？';
 questionPair(8,q=>{txt(q,'请先判断：图中的起伏描述了什么？',64,166);},async()=>{},'先请学生判断横轴表示什么，给20秒，同桌用一句话说明依据。此时不显示答案图。','两种图讨论不同问题。左图画空间里的传播，右图在固定位置记录信号随时间的变化。请学生分别指出横轴的含义。');
 const spatial=metadata.keys().find?null:null;
 const spReveal=order[order.indexOf(s(8))+1];
 txt(spReveal,'空间里的传播（示意）',64,234,544,46,32,C.violet,true,'space-heading');txt(spReveal,'固定位置的时间记录',672,234,544,46,32,C.cyan,true,'time-heading');
 await img(spReveal,'space-versus-time-source.png',{left:76,top:294,width:512,height:285},{left:0,top:0,right:.51,bottom:0},'Spatial propagation illustration reused from v8.4.10');
 const X=726,Y=435;line(spReveal,X,Y,1178,Y,C.gray,1.4,'time-axis');line(spReveal,X,309,X,564,C.gray,1.4,'amplitude-axis');curve(spReveal,Array.from({length:181},(_,j)=>[X+452*j/180,Y-95*model(j/180)]),C.violet,2.2,'fixed-position-signal');txt(spReveal,'振幅',672,289,84,36,24,C.gray,false,'amplitude-label');txt(spReveal,'时间',1089,567,110,36,24,C.gray,false,'time-label');txt(spReveal,'在一个位置测量，横轴是时间。',672,610,544,44);addNotes(spReveal,'[图示边界]\n左侧复用程序示意图image5的左半部分，等比裁切，无技术数值。右侧是sin(10πt+0.3)的数学示意信号，不是录音实测。');
 heading(12).text='演示B：放大红框，能看到什么？';
 const zoomReveal=questionPair(12,q=>{
  txt(q,'同一数学示意信号；只放大 0.30～0.50 s。',64,166);
  txt(q,'整体：0～1 s',64,235,518,44,32,C.ink,true,'overview-heading');txt(q,'红框区间：0.30～0.50 s',702,235,514,44,32,C.ink,true,'zoom-heading');
  for(const [k,x]of [112,750].entries()){line(q,x,420,x+430,420,C.gray,1.3,`overview-axis-${k}`);line(q,x,304,x,544,C.gray,1.3,`amplitude-axis-${k}`);txt(q,'振幅',x-48,291,88,33,24,C.gray,false,`amplitude-label-${k}`);txt(q,'时间 / s',x+293,561,135,36,24,C.gray,false,`time-label-${k}`);}
  curve(q,Array.from({length:301},(_,j)=>[112+430*j/300,420-105*model(j/300)]),C.gray,1.6,'overview-shared-signal');rect(q,112+430*.3,307,430*.2,226,C.red,'none','selected-window',2.5);arrow(q,603,409,48,C.violet,'zoom-direction');
  for(const [k,x,start,end]of [[0,112,0,1],[1,750,.3,.5]])for(const [j,v]of [start,end].entries())txt(q,v.toFixed(k?2:0),x+j*430-30,532,60,32,24,C.gray,false,`window-tick-${k}-${j}`,'center');
 },r=>{curve(r,Array.from({length:201},(_,j)=>{const tm=.3+.2*j/200;return[750+430*j/200,420-105*model(tm)];}),C.gray,1.6,'zoom-shared-signal');for(let j=15;j<=25;j++){const tm=j/50;dot(r,750+430*(tm-.3)/.2,420-105*model(tm),C.outlineCyan,12,false,`zoom-sample-${j}`);}txt(r,'同一区间、相同纵轴；放大后可分辨11个记录点。',64,610);},'先看左侧全段与红框时刻。请预测放大后会看到什么，停顿20秒。右侧暂不画样本，不提前给出点数。','请核对右图从0.30到0.50秒，与左图红框相同；纵轴比例相同，只有横轴放大。逐个数点，再解释这是一段数字记录，而不是声音传播的路线。');
 addNotes(zoomReveal,'[数学证据]\n共享模型0.72sin(10πt+0.3)。采样时刻j/50，j=15..25，共11个观测点，包含窗口两端。全段[0,1)为50样本；不要把封闭观察窗的11个点当作0.2秒新增11样本。');
 clear(16);heading(16).text='等级编号0～7，一共有几档？';txt(16,'0也是一个编号。请从左到右逐档数。',64,166);countBins(16,152,343,976,112,8);txt(16,'这里有8个等级。下一步再判断3.71落在哪一档。',64,610);
 clear(17);txt(17,'范围 [0,8)，分成8段；先独立判断等级编号。',64,166);countBins(17,152,337,976,112,8);txt(17,'采样原值：3.71',64,496,1152,54,36,C.ink,true,'raw-value');txt(17,'请说明你采用的分档规则。',64,610);notes(17,'提问','请先独立判断3.71的等级编号，并写出规则。所有档的样式相同。不要用“四舍五入”抢答；先说题目怎样定义区间。给20秒后请两人解释。');
 // Restore the missing controlled quantization comparison.
 heading(22).text='同一个3.71，4bit会怎样近似它？';
 const qReveal=questionPair(22,q=>{txt(q,'范围仍为 [0,8)；各档中点作代表值。',64,166);txt(q,'3bit：8档',64,248,544,44,32,C.ink,true,'q3-heading');txt(q,'4bit：16档',672,248,544,44,32,C.ink,true,'q4-heading');countBins(q,96,372,480,112,8);countBins(q,704,372,480,112,16);txt(q,'已知：3bit把3.71近似为3.5。',64,541,544,84,29.333,C.ink,false,'given-q3');txt(q,'4bit对应哪一段？代表值是多少？',672,541,544,84);},r=>{dot(r,704+3.71*60,404,C.red,12,true,'same-raw-3.71');rect(r,704+7*30,372,30,112,C.red,'none','q4-selected-bin',2.5);txt(r,'[3.5,4) 的中点：3.75',672,610,544,44,29.333,C.cyan,true,'q4-representative');},'沿用上一页的幅度范围和中点规则，只改变每样本位数。先请学生找4bit下对应的区间，不显示答案，停顿20秒。','先听学生给出的区间，再揭示红框。[3.5,4)的中点是3.75，用它近似3.71。这里的7是等级编号，3.75是幅度代表值。更细分档没有增加记录时刻。');
 addNotes(qReveal,'[计算]\nΔ=8/16=0.5，floor(3.71/0.5)=7，代表值(7+0.5)×0.5=3.75。3bit中点为3.5。仅为非负幅度教学模型，实际PCM通常使用有符号幅度。');
 heading(24).text='演示C：3bit变4bit，样本点会变多吗？';
 const cReveal=questionPair(24,q=>{txt(q,'输入和采样时刻不变，只改量化位数。',64,166);txt(q,'请预测：记录时刻、代表值、码字长度，哪些会变？',64,336,1152,100,36,C.ink,false,'demo-c-prediction');},r=>{for(let k=0;k<2;k++){const bits=k?4:3;txt(r,`${bits}bit：${2**bits}个代表值`,64,265+k*174,285,46,29.333,C.ink,true,`bitdepth-${bits}`);quantGraph(r,370,235+k*174,804,139,bits);}txt(r,'空心点：同一输入；实心点：量化后的代表值。',64,610);},'先只读实验条件。请每人预测改变位数会不会增加采样时刻，再写出还会改变什么。没有运行前不要用网格或点数给出答案。','对齐上下相同的10个时刻，空心点的输入完全相同。比较实心点可取的纵向位置。请学生解释改变的是幅度分档和码字长度，记录时刻没有增加。');
 addNotes(cReveal,'[数学证据]\n同一10个输入：[3.71,5.2,7.1,6.4,4.15,2.3,0.65,1.4,3.2,4.8]，范围[0,8)，3bit/4bit均为中点量化。本页是控制变量模型，不冒充remote-demos-v7的实际波形。');
 clear(27);heading(27).text='PCM样本和WAV文件，分别指什么？';txt(27,'以装有PCM样本的WAV为例，示意不按字节比例绘制。',64,166);rect(27,64,290,1152,216,C.violet,'none','wav-container',2);txt(27,'WAV文件',82,253,500,44,32,C.violet,true,'wav-label');rect(27,86,315,325,165,C.grid,'none','description-block');txt(27,'格式、采样率、声道\n及其他结构信息',104,350,289,92,29.333,C.ink,false,'metadata-label');txt(27,'PCM样本数据',465,310,720,46,32,C.cyan,true,'payload-label');for(let j=0;j<6;j++){rect(27,465+j*116,381,98,61,C.outlineCyan,'none',`pcm-byte-${j}`);txt(27,`B${j}`,465+j*116,396,98,38,24,C.ink,false,`byte-label-${j}`,'center');}txt(27,'样本数据量 + 文件结构，才是完整文件大小。',64,574);notes(27,'解释','先指出大框表示一个完整WAV文件，里面既有说明信息，也有样本数据。请学生找到采样率和声道在哪里描述，再逐个读样本字节。计算题数的是样本数据，文件结构要另外计入。','[技术边界]\nWAV是RIFF容器，可装其他编码；这里只画含PCM的情况。结构不固定为44Byte，图框宽度不表示实际比例。\n[来源]\nMicrosoft RIFF overview：https://learn.microsoft.com/en-us/windows/win32/xaudio2/resource-interchange-file-format--riff-');
 // Keep the counting formula native, but reinforce its two meanings.
 clear(31);heading(31).text='未压缩PCM的数据量，怎样数出来？';txt(31,'固定存储位宽；计算样本数据，不含文件结构。',64,166);
 txt(31,'每声道采样了多少次？',64,278,515,48,32,C.violet,true,'sample-count-label');txt(31,'采样率 × 秒数',64,358,515,55,36,C.ink,true,'sample-count-factors');
 txt(31,'每个时刻要存多少Byte？',701,278,515,48,32,C.cyan,true,'instant-width-label');txt(31,'声道数 ×（存储位宽 ÷ 8）',701,358,515,86,29.333,C.ink,false,'instant-width-factors');txt(31,'×',593,350,70,64,48,C.ink,true,'count-times-width','center');
 txt(31,'总Byte数＝每声道样本数 × 每时刻Byte数',64,538,1152,48,32,C.violet,true,'pcm-result-formula');txt(31,'先统一为Hz、秒、bit；8 bit＝1 Byte。',64,610);notes(31,'解释','请先解释左右两项各在数什么。左边按每秒每声道的样本数乘秒数，得到每个声道的记录次数；右边数每个时刻所有声道合起来占多少Byte。把两项相乘才得到总量。不要先背五个数字的乘法。','[公式条件]\n未压缩、固定存储位宽、整数样本计数。存储位宽可能大于有效量化位数。真实文件优先从帧数和块对齐读取payload。');
 // Borrow the physical spatial-versus-temporal comparison, while keeping exact structures editable.
 clear(47);heading(47).text='图像和声音，在哪里取样？';txt(47,'图像：空间位置',64,166,544,44,32,C.violet,true,'image-heading');txt(47,'声音：时间点',672,166,544,44,32,C.cyan,true,'audio-heading');
 for(let row=0;row<4;row++)for(let col=0;col<6;col++)rect(47,112+col*60,293+row*60,60,60,C.grid,(row+col)%2?'#D5EBF3':'#A7D5E5',`pixel-${row}-${col}`);
 rect(47,232,353,60,60,C.red,'none','focus-pixel',2.5);txt(47,'6列 × 4行：24个像素',64,557,544,44);
 line(47,706,446,1170,446,C.gray,1.3,'sample-time-axis');curve(47,Array.from({length:151},(_,j)=>[706+464*j/150,422-75*Math.sin(2*Math.PI*j/150)]),C.gray,1.6,'waveform');for(let j=0;j<6;j++)dot(47,706+464*j/5,422-75*Math.sin(2*Math.PI*j/5),C.outlineCyan,12,false,`time-sample-${j}`);txt(47,'6个时刻：6个样本／声道',672,557,544,44);txt(47,'数清“有多少份”，再乘“每份占多少bit”。',64,610);notes(47,'比较','左图先数列与行，每个格子是一个空间位置的像素；右图逐个数时间点，每个点是一个时刻的幅度记录。两者都先数有多少份，再计算每份大小。请学生说出图像和声音的取样位置有何不同。','[模型边界]\n24像素与6样本是计数示意，不是相同信息量或相同采样率的声明。');
 clear(52);heading(52).text='视频文件为什么可能小于6.44 GiB？';txt(52,'相同题设：480×320、24bit／像素、25fps、10分钟、无声。',64,166);txt(52,'逐帧未压缩：约6.44 GiB',64,254,665,48,32,C.ink,true,'uncompressed-given');for(let j=0;j<5;j++){rect(52,64+j*130,356,103,146,C.grid,'none',`raw-frame-${j}`);dot(52,82+j*130+j*13,428,C.outlineCyan,16,false,`ball-${j}`);}arrow(52,770,415,60,C.violet,'file-question-arrow');rect(52,914,333,267,184,C.grid,'none','unknown-file');txt(52,'保存的视频文件',936,355,225,44,29.333,C.ink,false,'file-title','center');txt(52,'？',936,411,225,70,48,C.ink,true,'unknown-size','center');txt(52,'请提出一种解释，并说出还要核对什么条件。',64,610);notes(52,'提问','刚才算出了逐帧未压缩的量。先保证屏幕上的题设不变，再请学生解释为什么一个视频文件可能更小。先收预测，不把压缩算法和帧间变化图提前揭示。','[图示边界]\n只画5张代表帧，不是全部15000帧，也不按存储比例画框。视频文件大小还受编码和封装等影响。');
 heading(61).text='看起来相同，能证明完全恢复吗？';
 const recovery=questionPair(61,q=>{txt(q,'比较对象：原始像素值。请提出一种检验方法。',64,166);txt(q,'原始：4×4像素',64,248,420,44,32,C.ink,true,'original-pixels-title');for(let row=0;row<4;row++)for(let col=0;col<4;col++){const val=(row+col)%2;rect(q,114+col*58,321+row*58,58,58,C.grid,val?'#A7D5E5':'#478FC0',`original-pixel-${row}-${col}`);}txt(q,'恢复后的数据要和什么比较？',64,610);},r=>{for(let group=0;group<2;group++){const x=480+group*358;txt(r,group?'近似恢复':'完整恢复',x,248,320,44,32,C.ink,true,`restore-heading-${group}`);for(let row=0;row<4;row++)for(let col=0;col<4;col++){let val=(row+col)%2;if(group&&row===2&&col===2)val=1-val;rect(r,x+col*58,321+row*58,58,58,C.grid,val?'#A7D5E5':'#478FC0',`restored-${group}-${row}-${col}`);}if(group){rect(r,x+116,437,58,58,C.red,'none','changed-pixel',3);txt(r,'1处不同',x,566,320,40,29.333,C.red,true,'different-count');}else txt(r,'16处逐一相同',x,566,320,40,29.333,C.violet,true,'identical-count');} },'请先看原始4×4像素，独立提出检验方法。只凭远处“看起来一样”够不够？先收方法，再展示恢复结果。','中间16处都与原值相同；右侧至少有一处不同。请学生逐格核对红框位置。区分无损与有损，要检验能否完整恢复原始数据，而不能只凭肉眼相似。');
 addNotes(recovery,'[图示边界]\n这是原生可编辑的概念模型，右侧仅交换一个像素值，不冒充JPEG或某个真实算法的实验输出。实际例证接下来使用源文件/JPEG解码后的RGB数据。');
 heading(66).text='同一张图，JPEG能完全恢复原像素吗？';
 const crop={left:230/640,top:140/350,right:200/640,bottom:50/350};
 const jpegReveal=questionPair(66,q=>{txt(q,'A与B尺寸相同。请观察指定区域，再判断。',64,166);txt(q,'A：原始RGB',170,215,304,38,29.333,C.ink,false,'original-header');txt(q,'B：JPEG解码后的RGB',805,215,410,38,29.333,C.ink,false,'jpeg-header');},()=>{},'先看两幅完整图；它们的尺寸相同。请在红框区域寻找差异，并判断“大小和外观相近”能否证明恢复了所有像素。停顿20秒。','放大同一坐标区域，比较线条与纹理。两边使用相同裁剪、相同倍率和正确长宽比。低质量JPEG的变化只是这个受控例子，不能由肉眼相似推断逐像素完全相等。');
 for(const q of [s(66),jpegReveal])for(const [k,file]of ['original-rgb.png','jpeg-quality3-decoded.png'].entries()){
  const x=k?805:170;await img(q,file,{left:x,top:262,width:304,height:166.25},null,`Same 640x350 RGB image ${k?'decoded after JPEG':'original'}`);rect(q,x+304*230/640,262+166.25*140/350,304*210/640,166.25*160/350,C.red,'none',`roi-${k}`,2);
 }
 for(const [k,file]of ['original-rgb.png','jpeg-quality3-decoded.png'].entries()){const x=k?805:170;await img(jpegReveal,file,{left:x,top:447,width:252,height:192},crop,`Same ROI x230..439 y140..299 ${k?'JPEG decoded':'original'}`);line(jpegReveal,x+304*230/640,428,x,443,C.grid,1.1,`zoom-guide-${k}`);}
 addNotes(jpegReveal,'[证据与来源]\n原图及JPEG解码图直接提取自v8.4.10的ppt/media/image2.png和image3.png。原始RGB为640×350，procedural_picture；JPEG质量3、subsampling=2。ROI=[230,140,440,300)，210×160，PPT原生裁剪至252×192，等比1.2倍。没有生成或伪造压缩痕迹。Pillow JPEG参数文档：https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#jpeg，检索2026-10-14。');
}
// Round-specific repairs are appended only after inspecting each preceding artifact.
if(phase===1){
 // R1-01: Prediction text is stable and outside the plotted evidence.
 const cQ=s(24),cR=keyed.get('p24-reveal');
 for(const v of [cQ,cR]){removeWhere(v,o=>o.name==='demo-c-prediction'||o.name==='text'&&t(o).startsWith('空心点：'));txt(v,'请预测：记录时刻会增加吗？',64,610,1152,44,29.333,C.ink,false,'demo-c-prediction');}
 removeWhere(cR,o=>/^(bitdepth-|quant-|rep-grid-|error-|raw-|quantized-)/.test(o.name));
 dot(cR,81,230,C.ink,12,true,'legend-raw');txt(cR,'同一输入',103,210,220,44,29.333,C.ink,false,'legend-raw-label');dot(cR,425,230,C.violet,11,false,'legend-quantized');txt(cR,'量化后的代表值',447,210,430,44,29.333,C.ink,false,'legend-quantized-label');
 for(let k=0;k<2;k++){const bits=k?4:3,y=286+k*180;txt(cR,`${bits}bit：${2**bits}个代表值`,64,y+28,285,46,29.333,C.ink,true,`bitdepth-${bits}`);quantGraph(cR,370,y,804,110,bits);for(const a of [0,8])txt(cR,String(a),322,y+110*(1-a/8)-17,34,34,24,C.gray,false,`amplitude-${bits}-${a}`,'right');for(let j=0;j<10;j++)txt(cR,String(j),350+j*804/9,y+113,40,30,24,C.gray,false,`sample-index-${bits}-${j}`,'center');}
 addNotes(cQ,'[追问]\n同时预测代表值和码字长度是否改变。');addNotes(cR,'[观察顺序]\n先按空心、实心形状读图例，再核对同编号0～9的时刻。两行纵轴均为0～8。');
 // R1-02: The question has neutral evidence and no absent referent.
 for(const v of [s(8),keyed.get('p8-reveal')]){removeWhere(v,o=>o.name==='text'&&t(o).startsWith('请先判断：'));txt(v,'请先判断：波形的起伏描述了什么？',64,166);}
 const spR=keyed.get('p8-reveal');removeWhere(spR,o=>o.name==='fixed-position-signal');
 for(const v of [s(8),spR])curve(v,Array.from({length:181},(_,j)=>[726+452*j/180,435-95*model(j/180)]),C.gray,2.2,'fixed-position-signal');
 notes(8,'提问','请看灰色波形，只讨论起伏怎样变化。先判断横轴表示空间距离还是经过的时间，并说明理由。给20秒，随后比较两种图。','[图示边界]\n灰色数学示意波形，不标横轴答案。');
 // R1-03: Count before revealing; midpoint question/reveal is a genuine duplicate.
 removeWhere(16,o=>o.name==='text'&&t(o).startsWith('这里有8个等级。'));
 const countR=s(16).duplicate();metadata.get(s(16)).role='question';metadata.set(countR,{key:'p16-reveal',base81:16,role:'reveal'});order.splice(order.indexOf(s(16))+1,0,countR);txt(countR,'编号0～7，共8个等级。',64,610,1152,44,29.333,C.violet,true,'count-result');notes(16,'提问','先从0数到7。请每人写出等级总数，给10秒，不提前说答案。');notes(countR,'证据揭示','听完学生计数，再显示8个等级。等级编号与等级总数相差1，下一页用区间判断原值属于哪一档。');
 removeWhere(17,o=>o.name==='text'||o.name==='raw-value');txt(17,'范围 [0,8)；区间 [n,n+1) 编为Ln，中点作代表值。',64,166);txt(17,'采样原值：3.71',64,496,1152,54,36,C.ink,true,'raw-value');txt(17,'请判断等级编号和代表值，并说明依据。',64,610);
 notes(17,'提问','请先用题目给定的左闭右开区间找到3.71，再写等级编号和区间中点。给20秒，收两种解释；此时不要显示红框和答案。');
 const obsolete=s(18),midR=s(17).duplicate();metadata.set(midR,{key:'p18',base81:18,role:'reveal'});const oldIndex=order.indexOf(obsolete);order[oldIndex]=midR;p.delete(`sl/${obsolete.id}`);keyed.set('p18',midR);
 rect(midR,152+3*122,337,122,112,C.red,'none','selected-L3',2.5);dot(midR,152+3.71*122,365,C.red,12,true,'raw-3.71');dot(midR,152+3.5*122,415,C.violet,12,false,'representative-3.5');txt(midR,'3.71 ∈ [3,4)：等级L3，代表值3.5，码字011。',64,564,1152,40,29.333,C.violet,true,'midpoint-result');notes(midR,'证据揭示','沿用题目的区间规则，3.71位于[3,4)，因此等级编号是3，中点3.5才是幅度代表值。请分别指出空心原值、实心代表值与码字011，避免把编号3当幅度3。','[技术边界]\n非负幅度教学模型，实际PCM可用有符号幅度。');
 // R1-04: Count a small complete PCM example before generalizing.
 heading(31).text='这段PCM，共要保存多少Byte？';
 const pcmR=questionPair(31,q=>{txt(q,'2 Hz、16 bit、双声道、2 s；计算未压缩PCM样本数据。',64,166);txt(q,'不含文件结构。每声道的采样时刻从0 s开始。',64,221);txt(q,'请先画出记录次数，再算每次要存多少Byte。',64,610);},r=>{for(let j=0;j<4;j++){const x=370+j*210;txt(r,`${j*.5} s`,x,276,156,40,29.333,C.gray,false,`pcm-time-${j}`,'center');for(let ch=0;ch<2;ch++){const y=339+ch*102;rect(r,x,y,156,60,C.outlineCyan,'none',`pcm-cell-${ch}-${j}`);txt(r,'2 Byte',x,y+10,156,40,29.333,C.ink,false,`pcm-bytes-${ch}-${j}`,'center');}}
 txt(r,'左声道',64,352,245,44,29.333,C.ink,true,'pcm-channel-0');txt(r,'右声道',64,454,245,44,29.333,C.ink,true,'pcm-channel-1');rect(r,360,329,176,182,C.red,'none','first-instant',2.5);txt(r,'4个时刻 ×（2声道 × 2 Byte）＝16 Byte',64,538,1152,46,32,C.violet,true,'pcm-count-result');},'先独立画图：2秒内每声道记录几次？16bit对应多少Byte？给30秒，请两位学生展示计数。暂不显示网格和答案。','逐列读0、0.5、1、1.5秒，四个时刻。每个时刻同时保存左右两个样本，每样本16bit即2Byte。红框这一列占4Byte，四列共16Byte。然后请学生把计数方法迁移到下一道题。');
 addNotes(pcmR,'[形成结论]\nPCM字节数＝采样率×秒数×声道数×（存储位宽÷8）。左项先数每声道有多少样本；右项再数每时刻所有声道占多少Byte。\n[边界]\n使用[0,2)计时，2s端点不重复计入。未压缩固定16bit存储，不含文件结构；有效量化位数与实际存储位宽可能不同。');
 // R1-05: Preserve concept vocabulary and declare the schematic boundary.
 for(const v of [s(61),keyed.get('p61-reveal')]){removeWhere(v,o=>o.name==='text');txt(v,'像素概念示意。请提出一种完全恢复的检验方法。',64,166);txt(v,'请写出检验步骤。',64,610);}
 const recR=keyed.get('p61-reveal');for(let j=0;j<2;j++){const o=recR.shapes.items.find(o=>o.name===`restore-heading-${j}`);o.text=j?'有损：近似恢复':'无损：完整恢复';o.text.fontSize=29.333;}
 // R1-06: Remove a separator that visually divides an unfinished calculation.
 for(const n of [40,41,50,51])removeWhere(n,o=>!t(o)&&o.position.width>1050&&o.position.height<4&&o.position.top>450&&o.position.top<600);
 // R1-07: Byte-position symbols are distinguished from byte contents.
 txt(27,'每个小框示意1 Byte，B0～B5是字节位置编号。',465,518,735,44,29.333,C.ink,false,'byte-position-explanation');addNotes(27,'[读图]\nB0～B5不是字节内容或十六进制数，只表示示意的前6个字节位置。');

}
if(phase===2){
 // R2-01: Representative values have explicit solid markers; error is a separate focus.
 const quantR=keyed.get('p22-reveal');
 for(const v of [s(22),quantR])for(const name of ['q3-heading','q4-heading']){const o=v.shapes.items.find(o=>o.name===name);o.position={left:o.position.left,top:220,width:o.position.width,height:o.position.height};}
 dot(quantR,96+3.71*60,404,C.red,12,true,'q3-same-raw');dot(quantR,96+3.5*60,452,C.violet,12,false,'q3-midpoint');dot(quantR,704+3.75*60,452,C.outlineCyan,12,false,'q4-midpoint');
 const errorS=quantR.duplicate();metadata.set(errorS,{key:'p22-error',base81:22,role:'comparison'});order.splice(order.indexOf(quantR)+1,0,errorS);
 // Use the central whitespace between the headings and bins, with one shared scale.
 txt(errorS,'近似误差的大小',64,282,380,40,29.333,C.ink,true,'error-heading');rect(errorS,510,278,189,13,C.violet,C.violet,'error-bar-3bit',0);txt(errorS,'3bit：0.21',746,270,400,30,24,C.violet,false,'error-value-3bit');rect(errorS,510,311,36,13,C.outlineCyan,C.outlineCyan,'error-bar-4bit',0);txt(errorS,'4bit：0.04',746,303,400,30,24,C.cyan,false,'error-value-4bit');
 notes(errorS,'比较与归纳','沿用刚才已经算出的两个代表值。原值3.71与3.5相差0.21，与3.75相差0.04。两条长度用同一比例，短条表示这一个样本的近似误差较小。请学生说明为何记录时刻没有增加，幅度近似却更细。','[计算与边界]\n绝对误差|3.71-3.5|=0.21、|3.71-3.75|=0.04；比例900 px/幅度单位。只说明当前样本，不声称任意输入在每种量化规则下逐点误差必然更小。空心点为原值，实心点为中点。');
 addNotes(quantR,'[读图]\n两边空心红点同为3.71；下方实心点分别在3.5与3.75的横向幅度位置。先读区间，再读代表值。');
 // R2-02: Both inputs contribute to both output signals in a native schematic.
 clear(44);txt(44,'编辑时：两条音轨',64,166,430,44,32,C.violet,true,'track-heading');txt(44,'输出时：两个声道',830,166,386,44,32,C.cyan,true,'output-heading');
 const A=t=>.7*Math.sin(2*Math.PI*t),B=t=>.4*Math.sin(6*Math.PI*t+.5);
 for(let j=0;j<2;j++){const y=292+j*192;txt(44,j?'音轨2：背景音乐':'音轨1：诗朗诵',64,y-56,374,44,29.333,C.ink,false,`track-label-${j}`);rect(44,64,y,365,90,C.violet,'none',`track-${j}`);line(44,76,y+45,417,y+45,C.grid,1,`track-axis-${j}`);curve(44,Array.from({length:181},(_,k)=>[76+341*k/180,y+45-47*(j?B:A)(k/180)]),C.violet,1.8,`track-signal-${j}`);txt(44,j?'右声道 R':'左声道 L',850,y-56,366,44,29.333,C.cyan,true,`output-label-${j}`);rect(44,850,y,366,90,C.outlineCyan,'none',`output-${j}`);line(44,862,y+45,1204,y+45,C.grid,1,`output-axis-${j}`);curve(44,Array.from({length:181},(_,k)=>{const tm=k/180;return[862+342*tm,y+45-47*(j?(.4*A(tm)+.6*B(tm)):(.7*A(tm)+.3*B(tm)))];}),C.outlineCyan,1.8,`mixed-signal-${j}`);}
 rect(44,536,375,208,80,C.violet,'none','mix-operation');txt(44,'混音导出',551,395,178,44,29.333,C.ink,true,'mix-label');line(44,429,337,490,337,C.violet,1.5,'merge-upper');line(44,429,529,490,529,C.violet,1.5,'merge-lower');line(44,490,337,490,529,C.violet,1.5,'merge-branch');arrow(44,490,405,40,C.violet,'merge-arrow');line(44,744,415,808,415,C.violet,1.5,'split-shared');line(44,808,337,808,529,C.violet,1.5,'split-branch');arrow(44,809,327,34,C.violet,'left-output-arrow');arrow(44,809,519,34,C.violet,'right-output-arrow');txt(44,'混音示意：两条音轨都参与L、R的混合。',64,610);
 notes(44,'比较','先看两条输入波形，再沿汇合线到混音导出，最后读L、R两条输出。每个输出都是两条音轨的混合，不能把诗朗诵直接等同左声道、音乐直接等同右声道。保持输出声道数不变时，增加编辑音轨不会直接增加未压缩PCM数据量。','[模型边界]\n波形为数学示意，不是诗朗诵/音乐实测。A=0.7sin(2πt)，B=0.4sin(6πt+0.5)。L=0.7A+0.3B，R=0.4A+0.6B。共享t∈[0,1]，四图共享纵轴比例；示意省略采样与文件结构。');
 // R2-03: The frame-rate count has visible, equal time increments.
 for(let j=0;j<5;j++)txt(48,`${(j/25).toFixed(2)} s`,64+j*235.254488,493,210.982,34,24,C.gray,false,`frame-time-${j}`,'center');addNotes(48,'[观察与计数]\n25fps时相邻帧间隔1/25s=0.04s，这里画前5帧，时刻0、0.04、0.08、0.12、0.16s。不是1秒只有5帧。');
 // R2-04: Visual JPEG comparison is followed by an exact corresponding-pixel test.
 const jpegR=keyed.get('p66-reveal');txt(jpegR,'同一红框区域，等比放大',466,394,322,43,24,C.gray,false,'same-roi-label','center');
 const pixelR=jpegR.duplicate();metadata.set(pixelR,{key:'p66-pixel',base81:66,role:'evidence'});order.splice(order.indexOf(jpegR)+1,0,pixelR);
 txt(pixelR,'核对同一像素',468,454,320,44,29.333,C.ink,true,'pixel-check-heading','center');txt(pixelR,'(x=230, y=140)',468,502,320,40,29.333,C.gray,false,'pixel-coordinate','center');txt(pixelR,'A：(79,113,165)',458,550,340,40,29.333,C.ink,false,'pixel-original-value','center');txt(pixelR,'B：(51,108,153)',458,591,340,40,29.333,C.ink,false,'pixel-decoded-value','center');
 notes(pixelR,'精确证据','先观察同一红框区域，再核对原始图与JPEG解码图在同一坐标的RGB值。A是79、113、165，B是51、108、153，只要发现这一处不同，就不能称本例完全恢复了原始RGB数据。请学生用自己的检验步骤解释，避免只说“图片糊了”。','[证据]\n由提取的640×350原始RGB与JPEG解码RGB，用Pillow读取坐标(230,140)。两图同尺寸、同坐标、同ROI [230,140,440,300)，210×160。实际像素值写入原生PPT文本；没有模拟差异。局部放大相对于上方完整图显示比例为252/(304×210/640)=2.526315789倍。图像实体hash见assets-provenance.json与data-evidence.json。');
 // R2-05: Generalize the counting grid, retaining its geometry and conclusion.
 const pcmR=keyed.get('p31-reveal');for(const v of [s(31),pcmR]){const o=v.shapes.items.find(o=>t(o).startsWith('不含文件结构。每声道'));o.text='在 [0,2) 内采样，从0 s开始；不计文件结构。';}
 const result=pcmR.shapes.items.find(o=>o.name==='pcm-count-result');result.position={left:64,top:518,width:1152,height:44};
 const formulaR=pcmR.duplicate();metadata.set(formulaR,{key:'p31-formula',base81:31,role:'generalization'});order.splice(order.indexOf(pcmR)+1,0,formulaR);txt(formulaR,'总Byte数＝采样率×秒数×声道数×（存储位宽÷8）',64,568,1152,37,29.333,C.violet,true,'pcm-general-formula');notes(formulaR,'抽象与迁移','先请学生总结网格怎样计数，再显示公式。采样率乘秒数对应列数；声道数乘每样本Byte数对应一列的容量。请分别指出公式中的项来自哪里，然后进入真实采样率的独立练习。','[条件]\n未压缩固定存储位宽的PCM样本payload，不含容器结构。本例2×2×2×(16÷8)=16Byte。真实文件使用实际样本帧数与存储宽度，不把有效量化位数当存储宽度。');
 // R2-07: Keep the sampling-density comparison within the common content region.
 clear(14);txt(14,'同一信号、同一秒 [0,1)，只改变每秒的采样次数。',64,166);
 for(let k=0;k<2;k++){const rate=k?20:8,Y=320+k*172;txt(14,`${rate} Hz：${rate}个样本`,64,Y-28,260,44,29.333,k?C.cyan:C.violet,true,`density-heading-${rate}`);line(14,350,Y,1176,Y,C.gray,1.2,`density-time-axis-${rate}`);line(14,350,Y-65,350,Y+65,C.gray,1.2,`density-amplitude-axis-${rate}`);txt(14,'振幅',286,Y-69,64,35,24,C.gray,false,`density-amplitude-label-${rate}`);curve(14,Array.from({length:241},(_,j)=>[350+826*j/240,Y-50*.72*Math.sin(4*Math.PI*j/240+.1)]),C.gray,1.7,`density-signal-${rate}`);for(let j=0;j<rate;j++)dot(14,350+826*j/rate,Y-50*.72*Math.sin(4*Math.PI*j/rate+.1),k?C.outlineCyan:C.violet,12,false,`density-sample-${rate}-${j}`);txt(14,'0',330,Y+72,40,32,24,C.gray,false,`density-start-${rate}`,'center');txt(14,'1',1156,Y+72,40,32,24,C.gray,false,`density-end-${rate}`,'center');txt(14,'时间 / s',910,Y+72,170,32,24,C.gray,false,`density-unit-${rate}`);}
 txt(14,'同一秒里记录的次数变多；每样本存储位宽不变时，数据量增加。',64,610);
 notes(14,'比较证据','先核对两行的信号和一秒区间，再分别数8个与20个点。右端1秒不计入这一秒的样本总数。追问变化发生在横向记录时刻还是纵向代表值？这页只改变采样率，保持幅度模型和存储位宽，因此每秒记录更多数据。','[模型]\n共享数学示意0.72sin(4πt+0.1)，0≤t<1。上行j/8，j=0..7；下行j/20，j=0..19；共享横轴宽826、纵轴比例50px/幅度单位。不是现场音频实测。');
 // R2-06: The conversion reminder states the binary unit directly.
 const unit=s(39).shapes.items.find(o=>t(o).startsWith('提醒：1 MB'));unit.text='换算：1 MiB＝1024² Byte。';addNotes(39,'[单位]\n本题使用MiB=1024²Byte。MB=10⁶Byte；保留严格单位写法，不用MB指二进制换算结果。');

}
p.slides.reorder(order.map(v=>`sl/${v.id}`));
const ctx=createCanvas(20,20).getContext('2d');const overflow=[];
for(const [i,sl]of p.slides.items.entries())for(const o of sl.shapes.items){
 o.shadow='shadow-none';if(!t(o))continue;const face=o.text.typeface??F.regular;const size=o.text.fontSize??29.333;ctx.font=`${size}px "${face}"`;for(const str of t(o).split('\n'))if(ctx.measureText(str).width>o.position.width+2&&o.text.wrap==='none')overflow.push({page:i+1,name:o.name,text:str,width:ctx.measureText(str).width,box:o.position.width});
}
await fs.writeFile(path.join(ROOT,`phase${phase}-textfit.json`),JSON.stringify(overflow,null,2));
const stem=phase===0?'v85':phase===1?'round1':'v86';
const OUTPUT=path.join(ROOT,`${stem}-candidate.pptx`);
await (await PresentationFile.exportPptx(p)).save(OUTPUT);
const patched=spawnSync(PYTHON,[path.join(SOURCE,'patch_font_defaults.py'),OUTPUT],{encoding:'utf8'});if(patched.status)throw new Error(patched.stderr);
const plan={version:stem,date:'2026-10-14',slideCount:p.slides.items.length,slides:p.slides.items.map((sl,i)=>({...metadata.get(sl),page:i+1,title:t(heading(sl))}))};
await fs.writeFile(path.join(ROOT,`${stem}-plan.json`),JSON.stringify(plan,null,2));console.log(JSON.stringify({phase,file:OUTPUT,slides:plan.slideCount,textOverflow:overflow.length}));
