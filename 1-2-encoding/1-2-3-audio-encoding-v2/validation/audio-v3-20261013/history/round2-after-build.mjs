import fs from 'node:fs/promises';
import path from 'node:path';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
import { GlobalFonts } from '@napi-rs/canvas';

const DIR = '/private/tmp/audio-v3-production-20261013';
const F = {body:'Alibaba PuHuiTi 3.0 55 Regular', title:'Alibaba PuHuiTi 3.0 115 Black'};
for (const [file, alias] of [['55-Regular',F.body],['115-Black',F.title]]) {
  GlobalFonts.registerFromPath(`/Users/chran/Library/Fonts/AlibabaPuHuiTi-3-${file}.ttf`,alias);
}
const C = {rail:'#6251B1',violet:'#8C64E1',cyan:'#007C9B',red:'#FF0000',ink:'#262626',gray:'#808080',grid:'#D7D7DE',white:'#FFFFFF'};
const p = Presentation.create({slideSize:{width:1280,height:720}});
const manifest = [];
const sources = {
  sampling:'Analog Devices, MT-002, What the Nyquist Criterion Means to Your Sampled Data System Design. https://www.analog.com/media/en/training-seminars/tutorials/MT-002.pdf ; retrieved 2026-10-12.',
  quant:'Analog Devices, MT-001, Quantization Noise Model, p1. https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf ; retrieved 2026-10-12.',
  pcm:'Microsoft, WAVEFORMATEX: nChannels, nSamplesPerSec, nBlockAlign, wBitsPerSample. https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/ns-mmeapi-waveformatex ; retrieved 2026-10-12.',
  midi:'The MIDI Association, About MIDI, Part 1: Overview. https://midi.org/about-midi-part-1overview ; retrieved 2026-10-12.',
  wma:'Microsoft, Windows Media Codecs: Standard, Professional and Lossless. https://learn.microsoft.com/en-us/windows/win32/medfound/windows-media-codecs ; retrieved 2026-10-12.',
};
function txt(s,t,x,y,w=1152,h=46,size=29.333,color=C.ink,strong=false,name='text',alignment='left') {
  const o=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  o.text=t;
  o.text.style={typeface:strong?F.title:F.body,fontSize:size,color,bold:strong,autoFit:'none',wrap:'none',alignment,verticalAlignment:'top',insets:{left:0,right:0,top:0,bottom:0}};
  return o;
}
function box(s,x,y,w,h,stroke=C.grid,fill='none',width=1,name='box') {
  return s.shapes.add({geometry:'rect',name,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width}});
}
function curve(s,points,color=C.ink,width=2.3,name='curve') {
  const xs=points.map(v=>v[0]),ys=points.map(v=>v[1]);
  const x=Math.min(...xs),y=Math.min(...ys),w=Math.max(1,Math.max(...xs)-x),h=Math.max(1,Math.max(...ys)-y);
  return s.shapes.add({geometry:'custom',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:color,width},customPaths:[{width:w,height:h,commands:points.map((v,i)=>({[i?'lineTo':'moveTo']:{x:v[0]-x,y:v[1]-y}}))}]});
}
function line(s,x1,y1,x2,y2,color=C.grid,width=1,name='line') {return curve(s,[[x1,y1],[x2,y2]],color,width,name);}
function dot(s,x,y,color=C.violet,size=11,hollow=false,name='sample') {
  return s.shapes.add({geometry:'ellipse',name,position:{left:x-size/2,top:y-size/2,width:size,height:size},fill:hollow?C.white:color,line:{fill:color,width:hollow?2:0}});
}
function arrow(s,x,y,w=64,color=C.violet) {
  return s.shapes.add({geometry:'rightArrow',name:'mapping-arrow',position:{left:x,top:y,width:w,height:24},fill:color,line:{fill:'none',width:0}});
}
function frame(s,title) {
  s.background.fill=C.white;
  box(s,0,0,1280,10.666,'none',C.rail,0,'top-rail');
  box(s,0,709.334,1280,10.666,'none',C.rail,0,'bottom-rail');
  txt(s,title,63.84,63.84,1152,74,48,C.ink,true,'question-title');
}
function table(s,values,x,y,w,h,widths=null,name='evidence-table') {
  const t=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,values,...(widths?{columnWidths:widths}:{})});
  t.name=name;
  t.styleOptions={headerRow:false,bandedRows:false,bandedColumns:false};
  t.borders.assign({style:'solid',fill:C.grid,width:1.2});
  for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){
    const a=t.getCell(r,c);a.fill=C.white;
    a.text.style={typeface:r===0?F.title:F.body,fontSize:29.333,bold:r===0,color:r===0?C.violet:C.ink,autoFit:'none',wrap:'none',alignment:'center',verticalAlignment:'middle',insets:{left:8,right:8,top:8,bottom:8}};
  }
  return t;
}
function notes(s,id,stage,purpose,script,extra='',source='') {
  const content=`[问题] ${purpose}\n[内部编号] ${id}\n[阶段] ${stage}\n[教师逐字稿]\n${script}${extra?'\n'+extra:''}${source?'\n[来源]\n'+source:''}`;
  s.speakerNotes.textFrame.setText(content);
}
function page(id,title,stage,script,extra='',source='') {
  const s=p.slides.add();frame(s,title);notes(s,id,stage,title,script,extra,source);
  manifest.push({page:p.slides.items.length,id,stage,title,pair:null});return s;
}
function reveal(base,id,stage,script,extra='',source='') {
  const before=p.slides.items.indexOf(base)+1;
  const s=base.duplicate();s.moveTo(p.slides.items.length-1);
  const title=manifest[before-1].title;
  notes(s,id,stage,title,script,extra,source);
  manifest.push({page:p.slides.items.length,id,stage,title,pair:before});return s;
}
function result(s,a,b='',y=560){y=Math.min(y,b?560:610);txt(s,a,64,y,1152,44,29.333,C.violet,true,'answer-1');if(b)txt(s,b,64,y+49,1152,44,29.333,C.ink,false,'answer-2');}

// The teaching waveform is a reproducible mathematical illustration, not a recording.
const amplitudes=[-.38,.12,.86,.91,.62,.08,-.38,-.46,-.71,-.13];
const knots=[...amplitudes,.12];
function amplitude(t) {
  const u=Math.max(0,Math.min(10,t*2)),i=Math.min(9,Math.floor(u)),v=u-i;
  const a=knots[Math.max(0,i-1)],b=knots[i],c=knots[i+1],d=knots[Math.min(10,i+2)];
  return Math.max(-.98,Math.min(.98,.5*((2*b)+(-a+c)*v+(2*a-5*b+4*c-d)*v*v+(-a+3*b-3*c+d)*v*v*v)));
}
function quant(v,bits) {
  const levels=2**bits,step=2/levels,index=Math.min(levels-1,Math.max(0,Math.floor((v+1)/step)));
  return {index,representative:-1+(index+.5)*step,step,code:index.toString(2).padStart(bits,'0')};
}
const q2=amplitudes.map(v=>quant(v,2)),q3=amplitudes.map(v=>quant(v,3));
function plot(s,{x=150,y=250,w=960,h=245,rate=0,bits=null,focus=-1,caption='',axes=true}={}) {
  const X=t=>x+t*w/5,Y=v=>y+(1-v)*h/2;
  if(bits!==null){
    for(let i=0;i<2**bits;i++){
      const a=-1+(i+.5)*2/2**bits;line(s,x,Y(a),x+w,Y(a),C.grid,1,'quantization-level');
      txt(s,a.toFixed(bits===2?2:3),x-68,Y(a)-12,61,28,18.666,C.gray,false,'level-value','right');
    }
  }
  line(s,x,y-12,x,y+h+8,C.ink,1.5,'amplitude-axis');
  line(s,x,Y(0),x+w+12,Y(0),C.gray,1,'zero-baseline');
  line(s,x,y+h+8,x+w+12,y+h+8,C.ink,1.5,'time-axis');
  curve(s,Array.from({length:201},(_,i)=>[X(i/40),Y(amplitude(i/40))]),bits===null?C.ink:C.gray,2.5,'original-waveform');
  if(axes){
    txt(s,'时间 / s',x+w-110,y+h+43,130,34,24,C.ink,false,'time-label');
    for(let t=0;t<=5;t++){line(s,X(t),y+h+8,X(t),y+h+15,C.ink,1);txt(s,String(t),X(t)-14,y+h+18,30,31,24,C.ink,false,'time-tick','center');}
  }
  if(rate){
    const n=5*rate;
    for(let k=0;k<n;k++){const t=k/rate,v=amplitude(t);line(s,X(t),Y(0),X(t),Y(v),C.violet,2);dot(s,X(t),Y(v),C.violet,11);}
  }
  if(bits!==null){
    const qq=amplitudes.map(v=>quant(v,bits));
    amplitudes.forEach((a,k)=>{
      const xx=X(k/2),yy=Y(a),zz=Y(qq[k].representative);
      line(s,xx,yy,xx,zz,k===focus?C.red:C.violet,k===focus?4:2,'quantization-error');
      dot(s,xx,yy,C.ink,10,true,'original-sample');
      box(s,xx-5,zz-5,10,10,'none',C.violet,0,'quantized-sample');
      if(k===focus)box(s,xx-15,Math.min(yy,zz)-14,30,Math.abs(yy-zz)+28,C.red,'none',3,'current-focus');
    });
  }
  if(caption)txt(s,caption,x,y-48,w,40,29.333,C.ink,true,'plot-caption');
  return {X,Y};
}
const MODEL='[技术注解]\n归一化幅度数学示意：十个控制点为 −0.38、0.12、0.86、0.91、0.62、0.08、−0.38、−0.46、−0.71、−0.13；时刻 k/2，k=0…9。曲线按 Catmull-Rom 插值，5s处补0.12，只供观察，不是实测录音。采样比较均使用[0,5)区间，不重复计右端点。图中连线不是实际扬声器输出。';
const QUANT='[技术注解]\n模型范围[-1,1)，均匀分成2ⁿ档，使用每档中点作代表值。边界归入上档，越界截到端档。等级编号与代表幅度不同；无符号编号不等于真实16bit有符号PCM字节。量化误差为输入与代表值的绝对差。固定范围且未削波时，误差上界为步长的一半；不同位数的每个样本不一定都严格改善。';
// Native diagrams and staged transcripts for the audio-encoding v3 revision.
const EXTRA = {
  khan:'Khan Academy, Converting analog data to binary. https://www.khanacademy.org/computing/computers-and-internet/xcae6f4a7ff015e7d:digital-information/xcae6f4a7ff015e7d:representing-analog-data-in-binary/a/converting-analog-data-to-binary ; retrieved 2026-10-13. Visual sequencing adapted; all values independently calculated.',
  dsp:'McClellan and Schafer, DSP First, Lecture 9, Sampling & Aliasing, slides 7–9, 12 and 20–22. https://dspfirst.gatech.edu/archives/lectures/DSPFirst-L09-pp4.pdf ; retrieved 2026-10-13.',
  phet:'PhET team, teaching with simulations, Sound example, p6. https://phet.colorado.edu/publications/physics%20teacher_finalwithpicts.pdf ; retrieved 2026-10-13. The diagram here is a native teaching schematic, not a simulation screenshot.',
  xiph:'Xiph.Org, Digital Show & Tell, Stairsteps. https://wiki.xiph.org/Videos/Digital_Show_and_Tell ; retrieved 2026-10-13. Discrete samples are distinguished from reconstruction and sample-and-hold.',
};
const BASELINE_HASH='ab329b5af80bfb9593ece665c38209aa4828c4c50727d09118955b1504a00815';
function bracket(s,x1,x2,y,label,color=C.gray,name='count-bracket') {
  line(s,x1,y-8,x1,y,color,1.5,name);line(s,x1,y,x2,y,color,1.5,name);line(s,x2,y-8,x2,y,color,1.5,name);
  txt(s,label,x1,y+10,x2-x1,38,26.667,color,false,name+'-label','center');
}
function bits(s,code,x,y,count=code.length,cell=28,color=C.violet,name='bit-group') {
  for(let i=0;i<count;i++){
    box(s,x+i*(cell+2),y,cell,38,color,'none',1.5,name+'-'+i);
    txt(s,code[i]??'',x+i*(cell+2),y+3,cell,32,29.333,C.ink,false,name+'-digit-'+i,'center');
  }
}
function treeBase(id,prompt,established,script) {
  const s=page(id,prompt,'学生总结',script,'[课堂操作]\n先收学生总结及图上证据，再翻到树揭示。未来节点和关系不出现；已建立的节点、关系和几何在后续阶段不变。');
  box(s,64,184,212,86,C.violet,'none',2.4,'tree-root');txt(s,'声音数字化',78,208,184,43,32,C.ink,true,'tree-root-label','center');
  for(let i=0;i<established;i++)treeBranch(s,i,false);
  return s;
}
const branches=[
  ['采样','按时刻取值','采样率 × 时长','每声道有多少样本'],
  ['量化','幅度取有限等级','固定范围：等级数决定步长','等级越多，步长越小'],
  ['编码','用码字表示等级','等级编号 → 等长码字','本课编码可以不压缩'],
  ['PCM计数','先数样本，再数byte','每声道样本数 × 声道数','× 每样本字节数 → 数据量'],
];
function treeBranch(s,i,fresh) {
  const y=184+i*116;
  line(s,276,227,300,227,C.violet,2,'tree-root-connection');line(s,300,227,300,y+43,C.violet,2,'tree-trunk-'+i);line(s,300,y+43,324,y+43,C.violet,2,'tree-relationship-'+i);
  box(s,324,y,348,86,C.violet,'none',2,'tree-node-'+i);
  txt(s,branches[i][0],342,y+8,310,36,29.333,C.ink,true,'tree-heading-'+i);
  txt(s,branches[i][1],342,y+46,310,34,29.333,C.ink,false,'tree-detail-'+i);
  arrow(s,690,y+31,44,C.violet);
  txt(s,branches[i][2],754,y+8,462,36,29.333,C.ink,true,'tree-relation-label-'+i);
  txt(s,branches[i][3],754,y+46,462,36,29.333,C.ink,false,'tree-relation-detail-'+i);
  if(fresh){box(s,320,y-4,896,94,C.red,'none',3,'new-tree-focus');txt(s,'新增',568,y+10,85,32,24,C.ink,true,'new-tree-label');}
}
function expandedSample(s,x,y,answer=false,name='stored-sample') {
  for(let i=0;i<16;i++)box(s,x+i*27,y,27,40,i===8?C.cyan:C.violet,'none',1,name+'-bit-'+i);
  line(s,x+8*27,y-5,x+8*27,y+45,C.cyan,3,name+'-byte-boundary');
  bracket(s,x,x+8*27,y+48,answer?'8 bit＝1 B':'8 bit',C.violet,name+'-byte-1');
  bracket(s,x+8*27,x+16*27,y+48,answer?'8 bit＝1 B':'8 bit',C.cyan,name+'-byte-2');
  if(answer)txt(s,'一个16 bit样本＝2 B',x,y+104,432,43,29.333,C.violet,true,name+'-answer','center');
}
function secondsGrid(s,{channels=1,y=305,width=940,x=210,blank=true}={}) {
  line(s,x,y-18,x+width,y-18,C.ink,1.3,'recording-time-axis');
  for(let sec=0;sec<2;sec++){
    const xx=x+sec*width/2;
    txt(s,`第${sec+1}秒`,xx,y-68,width/2,38,29.333,C.ink,true,'second-label-'+sec,'center');
    for(let ch=0;ch<channels;ch++){
      const yy=y+ch*88;
      for(let k=0;k<4;k++){
        const sx=xx+16+k*106;
        if(k===2){txt(s,'…',sx,yy+3,66,45,32,C.gray,false,'omitted-samples','center');continue;}
        box(s,sx,yy,78,54,ch===0?C.violet:C.cyan,'none',2,'stored-sample-cell');
        line(s,sx+39,yy,sx+39,yy+54,ch===0?C.violet:C.cyan,1.2,'two-byte-divider');
        if(!blank) {txt(s,'1B',sx+1,yy+14,37,30,22.667,C.ink,false,'byte-label','center');txt(s,'1B',sx+40,yy+14,37,30,22.667,C.ink,false,'byte-label','center');}
      }
    }
    bracket(s,xx+12,xx+width/2-12,y+channels*88-17,'每声道8,000个样本',C.gray,'second-count-'+sec);
  }
  for(let ch=0;ch<channels;ch++)txt(s,channels===1?'单声道':ch===0?'左声道 L':'右声道 R',64,y+ch*88+12,140,42,29.333,C.ink,true,'channel-name-'+ch);
  txt(s,'只画部分样本；每个时刻，每声道保存一个16 bit值。',64,y+channels*88+44,1152,43,29.333,C.gray,false,'schematic-count-boundary');
}

let s=page('opening','声音的数字化','开场','先看同一段声音的两份文件，提出可检验的猜测。接着沿同一波形追踪采样、量化和码字，再数这些记录占多少字节。学生纸笔作答，教师操作课件。','[课堂条件与时间]\n先修：二进制、bit/byte、简单坐标图；45分钟，教师示范、学生纸笔。建议：开场与波形4分钟；采样及T1 6分钟；量化及T2 8分钟；编码及T3 6分钟；格式比较2分钟；PCM计数、双声道、文件与开场闭环10分钟；采样限制及T4 7分钟；独立退出2分钟。主要阶段50页；附录为可选，不计入45分钟。思考、同桌核对与总结包含在预算内，实际课堂节奏未验证。第18分钟进入编码，第26分钟开始计数模型，第28分钟进入实际PCM计数，第36分钟完成开场闭环，第43分钟独立退出。若超时，跳过裸采样混叠的深入讨论与全部附录，使用带限条件完成频率判断；不取消树总结、开场闭环和独立退出。PPTX静态图即可完成必要推理；音频播放可选，失败30秒切换图示。\n[版本与来源]\n本版是用户指定v2的独立课堂修订，保持原版与v2不变。具体图示依据用户接受的审阅建议及相邻课程的技术边界；相邻course-design.qmd和正式v4课堂包没有重写，也不把本版静默提升为其正式版本。\n[可观察目标]\n学生能标时间/幅度轴，数半开区间中的采样时刻，按规则选量化代表值并计算误差，互读等长码字，说明每个PCM因子的计数对象，区别样本数据/完整文件与声音频率/采样率。退出题独立检验声道和编码边界。');
s.shapes.items.find(o=>o.name==='question-title').text='';txt(s,'声音的数字化',160,220,960,112,80,C.ink,true,'cover-title','center');txt(s,'采样、量化、编码与存储',160,378,960,74,49.333,C.gray,false,'cover-subtitle','center');

s=page('Q1','同一段声音，为什么文件大小不同？','提问','A、B都六秒，都是未压缩PCM WAV。请独立写一个猜测和理由，再与同桌交换。我保留两条猜测，现在不公布记录参数。','[活动]\n个人20秒，同桌10秒，保留两条可检验猜测。可选试听固定音量、匿名A/B；听不出差异不影响推理。两份是同一已解码音乐片段的重处理，不是首次ADC录音；来源AAC已有的信息损失不能恢复。',sources.pcm);
txt(s,'同一段6秒声音；两份均为未压缩PCM WAV。',64,170,1152,44);txt(s,'先写猜测和理由，暂不看记录参数。',64,222,1152,44);table(s,[['文件','完整文件大小'],['A','529,244 B'],['B','96,044 B']],225,280,830,230,[210,620]);
let a=reveal(s,'Q1','阶段回应','可以确认：时长相同、都未压缩，数据量仍然不同。先保留猜测，接下来找出电脑记录了哪些数据，再用实际参数核对。','[保留答案]\n不在本页说出A/B采样率或PCM公式。');result(a,'同样长、同为未压缩，数据量仍可不同。','先找出电脑记录了什么，再核对猜测。',565);

s=page('Q2','这条波形的横轴和纵轴分别表示什么？','提问','曲线在记录哪种变化？请指出横轴、纵轴，找一个零线下方的时刻。是同一位置的不同时刻，还是不同位置？先说理由。',MODEL);
txt(s,'麦克风把同一位置的声压变化转换为电信号。',64,170,1152,44);plot(s,{x:160,y:255,w:950,h:205,axes:false});txt(s,'横轴：________',660,491,440,43,29.333,C.ink,false,'axis-x-placeholder');txt(s,'纵轴：________',64,491,510,43,29.333,C.ink,false,'axis-y-placeholder');
a=reveal(s,'Q2','揭示','横轴是时间，纵轴是信号幅度。取教室中同一个位置，声压随时间变化，麦克风将它转成电信号，再画出时间波形。曲线不是空气在空间中走过的路线；负值是相对基准的负偏差，不是负音量。',MODEL+'\n[图示目的]\n下面链条是因果示意，不是实测设备界面；固定位置与时间变化明确区分。',EXTRA.phet);
a.shapes.items.find(o=>o.name==='axis-x-placeholder').text='横轴：时间';a.shapes.items.find(o=>o.name==='axis-y-placeholder').text='纵轴：信号幅度';
txt(a,'同一位置',64,570,240,40,29.333,C.ink,true,'pressure-location');txt(a,'声压随时间变化',64,615,300,38,26.667,C.ink,false,'pressure-change');arrow(a,340,590,50);txt(a,'麦克风',435,570,230,40,29.333,C.ink,true,'microphone');txt(a,'转换为电信号',435,615,270,38,26.667,C.ink,false,'electrical-change');arrow(a,750,590,50);txt(a,'时间波形',845,570,300,40,29.333,C.violet,true,'waveform-view');txt(a,'零线下方是负偏差',845,615,360,38,26.667,C.ink,false,'negative-boundary');

s=page('Q3','5秒内每秒取1次，怎样安排采样时刻？','提问','从零秒开始，每秒取一次，记录区间不包括五秒端点。请先写出取值时刻，再圈出曲线上对应的位置，思考十五秒。',MODEL+'\n[预期反应]\n可能重复计入5s，先让学生说明时间区间。');txt(s,'从0s开始；记录[0,5)，不计5s端点。',64,170,1152,44);plot(s,{x:160,y:255,w:950,h:235});
a=reveal(s,'Q3','揭示','零、一、二、三、四秒，共五个样本。采样是在指定时刻读取幅度，使时间记录离散；这时还没有把幅度限制到有限等级。',MODEL,EXTRA.xiph);
for(let k=0;k<5;k++){line(a,160+k*190,372.5,160+k*190,255+(1-amplitude(k))*117.5,C.violet,2,'sampling-stem');dot(a,160+k*190,255+(1-amplitude(k))*117.5,C.violet,12);}
result(a,'采样：按指定时刻读取信号幅度。','本例0、1、2、3、4s，共5个样本。',587);
s=page('Q4','采样率加倍，改变了什么？','提问','同一五秒波形，右端点不计。先数两个图的样本，再说哪些条件不变、哪个参数改变。不先评价听感。',MODEL);txt(s,'相同输入、相同时长；只改每秒取值次数。',64,167,1152,44);plot(s,{x:150,y:270,w:440,h:170,rate:1,caption:'每秒取1次'});plot(s,{x:745,y:270,w:440,h:170,rate:2,caption:'每秒取2次'});
a=reveal(s,'Q4','揭示','左边五个，右边十个。采样率数的是每秒每声道的样本数。相同时长下采样率加倍，样本数加倍；图只证明记录更密，不证明听感必然更好。','[边界]\n1/2Hz为慢速计数模型，不是可用的音乐录音参数。实际声音频率与采样率必须分开；后面用纯音诊断。',sources.sampling);result(a,'1 Hz：5个样本；2 Hz：10个样本。','采样率＝每秒每声道取得的样本数。',577);
s=treeBase('T1','采样率与时长，怎样决定记录数量？',0,'先用零到四秒和左右点数，总结每秒取多少次、取几秒，怎样得到每声道样本数。收两条带图上证据的回答，再更新树。');a=reveal(s,'T1','树揭示','采样在指定时刻取幅度；采样率乘时长，得到每声道的样本数。右边箭头写的是这条计数关系，不是声音传播方向。');treeBranch(a,0,true);

s=page('Q5','按4个等级，给这些幅度找代表值','提问','按左表的规则归档，用每档中点代表幅度。独立填四个代表值，四十秒后同桌核对理由，暂时不写二进制。',QUANT,sources.quant);txt(s,'范围[-1,1)；均匀分档，边界归入上档。',64,170,1152,45);table(s,[['幅度区间','代表值','编号'],['[-1, -0.5)','−0.75','0'],['[-0.5, 0)','−0.25','1'],['[0, 0.5)','0.25','2'],['[0.5, 1)','0.75','3']],64,250,660,280,[290,230,140]);table(s,[['输入幅度','代表值'],['−0.38',''],['0.12',''],['0.86',''],['−0.71','']],784,250,432,280,[216,216]);
a=reveal(s,'Q5','揭示','四个代表值依次为负零点二五、零点二五、零点七五、负零点七五。量化将幅度近似为有限等级；代表幅度和等级编号不同。保留你改过的记录，接下来比较近似值与原值。',QUANT,sources.quant);['−0.25','0.25','0.75','−0.75'].forEach((v,i)=>{a.tables.items[1].getCell(i+1,1).value=v;a.tables.items[1].getCell(i+1,1).text.style={typeface:F.title,fontSize:29.333,color:C.violet,bold:true};});result(a,'量化：把输入幅度近似为有限个等级。','代表值是近似值；编号只是这一档的标签。',598);
s=page('Q6','只增加等级数，哪些量没变？','提问','两边十个时刻、输入与范围相同。黑色空心点为输入，紫色方点为保存的代表值。先找不变的条件，再观察相邻等级间隔。',QUANT+'\n'+MODEL,sources.quant);txt(s,'相同10个时刻、相同输入、相同幅度范围。',64,167,1152,44);plot(s,{x:155,y:260,w:425,h:168,bits:2,focus:6,caption:'4个等级'});plot(s,{x:750,y:260,w:425,h:168,bits:3,focus:6,caption:'8个等级'});dot(s,88,526,C.ink,11,true);txt(s,'输入幅度',108,509,210,42);box(s,378,522,11,11,'none',C.violet,0);txt(s,'代表值',403,509,180,42);line(s,685,526,723,526,C.red,4);txt(s,'本次观察的误差',745,509,410,42);
a=reveal(s,'Q6','揭示','没有多取时刻，也没有改变输入。范围固定，四档步长零点五，八档零点二五。右边两个点太接近，下一页把同一个样本放大，用数值核对误差。',QUANT,sources.quant);result(a,'时刻、输入和范围不变；等级间隔变小。','接着放大同一个样本，核对误差。',593);
function errorInset(s,x,y,input,rep,label,answer=false) {
  const X=v=>x+(v+0.5)/0.3*420;
  txt(s,label,x,y-52,420,42,32,C.ink,true,'error-inset-heading');line(s,x,y+70,x+420,y+70,C.gray,1.4,'amplitude-ruler');
  for(const value of [-.5,-.4,-.3,-.2]){line(s,X(value),y+66,X(value),y+78,C.gray,1);txt(s,String(value),X(value)-38,y+86,76,34,24,C.gray,false,'inset-scale','center');}
  dot(s,X(input),y+70,C.ink,14,true,'inset-input');box(s,X(rep)-6,y+64,12,12,'none',C.violet,0,'inset-representative');
  txt(s,'输入 −0.38',x,y+148,420,40,29.333,C.ink,false,'inset-input-label');txt(s,`代表值 ${rep===-.25?'−0.25':'−0.375'}`,x,y+195,420,40,29.333,C.violet,false,'inset-representative-label');
  const bb=bracket(s,X(input),X(rep),y+25,'',C.gray,'inset-error');
  const lab=s.shapes.items.findLast(o=>o.name==='inset-error-label');lab.position={left:x,top:y+35,width:420,height:38};lab.text='误差＝？';
}
s=page('Q7','同一个幅度，两次量化的误差各是多少？','提问','图上还是三秒处输入负零点三八的样本，现在只放大幅度方向。两个尺子范围相同，请算输入与代表值的绝对差，独立二十秒。',QUANT+'\n[图示]\n两幅横轴都表示幅度，不表示时间；以同一比例放大局部范围[-0.5,-0.2]。点的竖直位置只用于放置标记。',sources.quant);txt(s,'局部放大：这里的横轴表示幅度，两图使用同一标尺。',64,170,1152,44);errorInset(s,120,300,-.38,-.25,'4个等级');errorInset(s,750,300,-.38,-.375,'8个等级');
a=reveal(s,'Q7','揭示','左边绝对差零点一三，右边零点零零五。这一个样本八档更接近输入。固定范围、均匀分级、无过载时，步长减小，误差上界减小；并不保证每一点都严格改善。附录留有可核对反例。',QUANT,sources.quant);
for(const o of a.shapes.items.filter(o=>o.name==='inset-error-label'))o.text=o.position.left<600?'误差 0.13':'误差 0.005';result(a,'本例：0.13 与 0.005。','固定范围均匀量化：步长减小，误差上界减小。',599);
s=treeBase('T2','量化增加了哪些幅度选择？',1,'请用归档表、双图和局部误差说明量化改变哪一维；为什么固定范围时等级数决定步长？先收解释和证据，再更新树。');a=reveal(s,'T2','树揭示','新增幅度的有限等级和等级数与步长的关系。采样分支保持不变；一个处理时刻，另一个处理幅度。');treeBranch(a,1,true);

function levelCodes(s,count,x,y,show=false){
  const n=count===4?2:3;
  for(let k=0;k<count;k++){
    const col=k%4,row=Math.floor(k/4),xx=x+col*112,yy=y+row*142;
    if(!show)txt(s,String(k),xx,yy,92,35,29.333,C.ink,true,'level-index','center');
    if(show)bits(s,k.toString(2).padStart(n,'0'),xx+(92-(n*30-2))/2,yy+47,n,28,C.violet,'level-code');
  }
}
s=page('Q8','4级和8级，分别至少需要几bit？','提问','每个编号都用同样长的码字。左边零到三，右边零到七，至少需要几位才能区分？先独立写理由，二十秒后交流。','[阶段控制]\n题目仅列必要编号，不显示二进制码字和答案位数。');txt(s,'4个等级：编号0–3',100,192,470,45,32,C.ink,true,'four-level-heading');txt(s,'8个等级：编号0–7',715,192,500,45,32,C.ink,true,'eight-level-heading');levelCodes(s,4,100,290);levelCodes(s,8,715,290);line(s,640,182,640,565,C.grid,1.4,'comparison-divider');
a=reveal(s,'Q8','揭示一','一位只有两个码字，二位有四个。四档需要二位，零也写零零。八档请同学继续解释，下一页再核对。','[保留]\n本页只揭示四档。');levelCodes(a,4,100,290,true);txt(a,'4级 → 2 bit',100,553,500,46,32,C.violet,true,'four-level-answer');
let b=reveal(a,'Q8','揭示二','三位提供八种等长码字，覆盖八档。一般n位有二的n次方种码字。这里表示的是等级编号，不把幅度纵轴换成二进制；真实文件还要看实际存储宽度。','[扩展]\n非2的幂的等级数，最少等长位数为ceil(log2 L)。主线只用4/8。',sources.quant);levelCodes(b,8,715,290,true);txt(b,'8级 → 3 bit',715,553,500,46,32,C.violet,true,'eight-level-answer');txt(b,'n bit可提供2的n次方个码字。',64,620,1152,36,29.333,C.ink,false,'code-capacity');
function waveformCodes(s,show=false){
  const pp=plot(s,{x:205,y:250,w:960,h:174,bits:3,caption:''});
  for(let k=0;k<10;k++){
    const xx=pp.X(k/2),yy=pp.Y(q3[k].representative);
    txt(s,String(q3[k].index),k===0?xx+18:xx-18,yy-35,36,32,26.667,C.ink,true,'sample-grade-'+k,'center');
    line(s,xx,444,xx,488,C.grid,1,'sample-code-guide');
    bits(s,show?q3[k].code:'',xx-44,502,3,28,C.violet,'sample-code-'+k);
  }
  txt(s,'码字',64,505,80,42,29.333,C.ink,true,'code-row-label');
}
s=page('Q9','这十个等级，怎样写成等长码字？','提问','回到同一条波形的八级量化结果。点旁是等级编号，下方每个空组都留三位。写出十个码字，再与同桌互读，看能否读回编号。前导零不能省。',QUANT+'\n'+MODEL+'\n[活动]\n独立20秒，同桌互读前五个或后五个。码字下方的时间顺序与波形采样点对应。');txt(s,'点旁为等级编号；8级，每个样本使用3 bit码字。',64,170,1152,44);waveformCodes(s,false);
a=reveal(s,'Q9','揭示','下方每组三位对应上方一个采样时刻。依次为零一零、一零零、一一一、一一一、一一零、一零零、零一零、零一零、零零一、零一一。最后编号三就是零一一。编码按约定表示等级，这里没有压缩。','[完整序列]\n2,4,7,7,6,4,2,2,1,3 → 010,100,111,111,110,100,010,010,001,011。共30bit教学码字，不意味着实际WAV按3bit打包。真实PCM后面使用16bit存储宽度。\n'+QUANT,EXTRA.khan);
for(let k=0;k<10;k++)for(let bit=0;bit<3;bit++)a.shapes.items.find(o=>o.name===`sample-code-${k}-digit-${bit}`).text=q3[k].code[bit];box(a,205+9*96-49,497,98,48,C.red,'none',3,'last-code-focus');result(a,'同一时刻的代表值 → 等级编号 → 码字。','3 → 011；本课编码可以不压缩。',592);
s=treeBase('T3','时刻、幅度和码字，各解决什么问题？',2,'请沿旧分支回看：时刻怎样选，幅度怎样近似？再用码字互读说明编码增加了什么约定。收集总结后更新树。');a=reveal(s,'T3','树揭示','新增等级编号到等长码字的表示约定。采样与量化分支保留；编码不自动等于压缩。');treeBranch(a,2,true);

function formatPaths(s,answer=false){
  txt(s,'录音样本',80,246,260,45,32,C.ink,true,'recorded-route');txt(s,'按时刻保存幅度',80,295,280,43,29.333,C.ink,false,'recorded-content');arrow(s,370,269,52);txt(s,answer?'PCM：音频编码':'编码方法？',455,246,345,45,32,answer?C.violet:C.ink,true,'audio-encoding-slot');txt(s,answer?'本课：未压缩PCM':'怎样表示这些数据？',455,295,450,43,29.333,C.ink,false,'codec-example-slot');arrow(s,914,269,52);box(s,990,232,226,116,C.gray,'none',2,'container-outline');txt(s,answer?'WAV：容器':'文件包装？',1002,250,202,42,29.333,answer?C.violet:C.ink,true,'container-slot','center');txt(s,answer?'本课装PCM':'格式与数据',1002,300,202,34,26.667,C.ink,false,'pcm-container-example','center');
  txt(s,'演奏事件',80,431,260,45,32,C.ink,true,'event-route');txt(s,'音符、时长、乐器',80,480,300,43,29.333,C.ink,false,'event-content');arrow(s,370,454,52);txt(s,answer?'MIDI指令':'指令格式？',455,431,345,45,32,answer?C.cyan:C.ink,true,'midi-slot');txt(s,'由合成器解释',455,480,340,43,29.333,C.ink,false,'synthesizer');arrow(s,914,454,52);txt(s,'产生声音',998,431,218,45,32,C.ink,true,'synthesized-sound');
}
s=page('Q10','这些名称在录音流程的哪一层？','提问','WAV、PCM、MP3、WMA、MIDI对应的层次相同吗？上面从录音样本出发，下面从演奏事件出发。先把名称放进适合的位置，说出理由。','[学生起点]\n已经建立样本与码字。路径展示必要内容类别，空位留给学生判断；避免把文件扩展名直接当编码方法。',sources.pcm+'\n'+sources.midi+'\n'+sources.wma);txt(s,'WAV、PCM、MP3、WMA、MIDI',64,166,1152,44);formatPaths(s,false);
a=reveal(s,'Q10','揭示','PCM表示样本，MP3是有损音频编码，WMA是编码家族。WAV是文件包装容器，本课里面保存PCM，也可装其他编码。MIDI保存演奏指令，由合成器产生声音，并不保存这次录音的样本波形。','[图示边界]\n上方箭头表示数据层次。上方只绘制本课PCM装入WAV的例子；MP3/WMA分类另列在下方，不连向WAV。容器与编码不是两个连续音频变换。WMA不同成员可能有损或无损。',sources.pcm+'\n'+sources.midi+'\n'+sources.wma);
for(const [name,text] of [['audio-encoding-slot','PCM：音频编码'],['codec-example-slot','本课：未压缩PCM'],['container-slot','WAV：容器'],['pcm-container-example','本课装PCM'],['midi-slot','MIDI指令']])a.shapes.items.find(o=>o.name===name).text=text;result(a,'MP3／WMA：音频编码；MIDI：演奏指令。','',612);
s=page('Q11','MP3一定压缩到原来的1/10吗？','提问','相同时长，只比较数据，不计文件结构开销。已知PCM每秒位数和本例MP3固定码率，请算比例。如果改变码率，比例会保持不变吗？','[条件]\nPCM 44.1kHz、16bit、双声道：1411200bit/s；MP3固定128000bit/s。比较估计数据码率，不承诺实际完整文件比值或听感。');txt(s,'相同时长；只比较数据，不计文件结构开销。',64,170,1152,44);txt(s,'PCM：1,411,200 bit/s',64,280,1152,46,32,C.ink,true);txt(s,'MP3：128,000 bit/s（本例固定码率）',64,420,1152,46,32,C.ink,true);
a=reveal(s,'Q11','揭示','相同时长约去，比例约百分之九点一。两条数据条按码率比例绘制，能看到本例为什么接近十分之一，但这个比例随参数与码率改变。','[计算]\n128000/1411200=0.0907029478，四舍五入9.1%。此图不表达听感质量。');box(a,64,342,1060,36,'none',C.violet,0,'pcm-rate-bar');box(a,64,482,1060*128000/1411200,36,'none',C.cyan,0,'mp3-rate-bar');result(a,'128,000 ÷ 1,411,200 ≈ 9.1%。','比例取决于参数与码率，不能固定为1/10。',590);

s=page('Q12-A','这8个样本一共占多少byte？','提问','先用可以画全的计数模型：每秒四次、两秒、单声道、每个样本十六bit。上面按时间排了八个样本；下面展开其中一个，每格一bit。请数一个样本多少byte，再数整段。','[时间与模型]\n4Hz只用于画全计数，不能据此推断真实音乐听感。样本时刻k/4，k=0…7，记录[0,2)。所有样本实际存16bit，内容是否相同不改变固定宽度。',sources.pcm);txt(s,'计数模型：4 Hz、2 s、16 bit / 样本、单声道。',64,170,1152,44);
for(let k=0;k<8;k++){const x=178+k*126;txt(s,String(k/4),x,265,108,33,24,C.gray,false,'toy-time-'+k,'center');box(s,x,318,108,63,C.violet,'none',2,'toy-sample-'+k);txt(s,'16 bit',x,334,108,35,29.333,C.ink,false,'toy-width-'+k,'center');}txt(s,'时间 / s',64,265,108,35,24,C.gray,false,'toy-time-unit');line(s,178,303,1170,303,C.gray,1.2,'toy-timeline');txt(s,'展开一个样本：每格1 bit',64,432,1152,43,29.333,C.ink,true,'toy-expand-heading');expandedSample(s,370,488,false,'toy-expanded');
a=reveal(s,'Q12-A','揭示','十六格每八格组成一个byte，所以一个样本两byte。两秒八个样本，一共十六byte。先数对象，再写式子；换成八千Hz时仍是这套结构，只是每秒样本更多。','[学生证据]\n纸上圈两个8bit组，写8×2B=16B。',sources.pcm);for(const name of ['toy-expanded-byte-1-label','toy-expanded-byte-2-label'])a.shapes.items.find(o=>o.name===name).text='8 bit＝1 B';txt(a,'8个样本 × 2 B / 样本＝16 B',64,614,1152,40,29.333,C.violet,true,'toy-total');
s=page('Q12','2秒单声道PCM，需要多少样本数据？','提问','前面的三bit表示教学模型的等级编号；这个PCM文件实际每样本保存十六bit。现在每秒每声道八千个样本，记录两秒。图只画部分样本。请独立写出样本数、每样本byte数和总byte数，三十秒后核对。','[计数对象]\n单声道每个时刻一个值；fs×t=整数帧数，本例16000帧；真实文件采用16bit，不把之前3bit等级模型当存储宽度。N、每帧宽度、总量依次揭示。',sources.pcm);txt(s,'8,000 Hz｜2 s｜实际存储16 bit / 样本｜单声道',64,170,1152,44,32);secondsGrid(s,{y:315});
a=reveal(s,'Q12','样本数揭示','先数记录：一秒八千个，两秒一万六千个。这一步数的是样本，先不直接把它当byte。','[阶段控制]\n只核对总样本数，保留总byte数。',sources.pcm);txt(a,'8,000 个/秒 × 2 秒＝16,000个样本。',64,514,1152,40,29.333,C.violet,true,'answer-1');
b=reveal(a,'Q12','存储宽度揭示','每个样本十六bit，就是两个byte。现在把一万六千个样本，每个占两个byte相乘。请先写你的结果，下一页才核对。','[阶段控制]\n单声道一帧一个样本，2B/帧。不给完整文件大小。',sources.pcm);for(const o of b.shapes.items.filter(o=>o.name==='answer-1'))o.text.style={...o.text.style,color:C.ink};txt(b,'16 bit / 样本 ÷ 8＝2 B / 样本',64,564,1152,40,29.333,C.violet,true,'sample-width-answer');
let c=reveal(b,'Q12','总量揭示','一万六千个样本乘每个两byte，三万二千byte。也可以一秒八千乘两，得到一万六千byte每秒，再乘两秒。两条计数路径的单位都能对消。','[独立核对]\n16000×2B=32000B；8000samples/s×2B/sample=16000B/s，再×2s。公式只计固定宽度未压缩PCM样本数据。',sources.pcm);a=c;
// Keep the earlier counts fixed; add the total in the open central band.
for(const o of a.shapes.items.filter(o=>['answer-1','sample-width-answer'].includes(o.name)))o.text.style={...o.text.style,color:C.ink};txt(a,'16,000个样本 × 2 B / 样本＝32,000 B',64,614,1152,40,32,C.violet,true,'pcm-payload-result');
s=page('Q12-B','增加右声道，哪些记录多了一份？','提问','保持八千Hz、两秒和十六bit。现在每个时刻同时保存左、右两个值。单声道刚才三万二千byte；双声道样本数据是多少？指出图上对应的新增记录，二十秒独立列式。','[给定]\n每声道参数一致，时间对齐，固定宽度整数PCM。双声道数据量翻倍，不代表响度或音质翻倍。',sources.pcm);txt(s,'8,000 Hz｜2 s｜实际存储16 bit / 样本｜双声道',64,170,1152,44,32);secondsGrid(s,{channels:2,y:292});
a=reveal(s,'Q12-B','揭示','看红框中的同一个时刻：左两byte、右两byte，一帧四byte。一万六千帧乘四byte，六万四千byte。样本总数也可按一万六千乘二声道计。增加的是同一时刻另一声道的值，不是录制时间翻倍。','[术语]\nframe是一时刻所有声道样本的组合。本课先用“同一时刻”说明，再引入帧，不要求学生额外背术语。',sources.pcm);box(a,222,288,86,150,C.red,'none',3,'stereo-current-frame');result(a,'每个时刻：2 B＋2 B＝4 B。','16,000 × 4＝64,000 B（样本数据）。',587);

function fileBlocks(s,answer=false) {
  const rows=[['RIFF结构',12,64,190],['fmt结构',24,274,200],['data块头',8,494,180],['PCM样本数据',32000,694,522]];
  for(const [label,count,x,w]of rows){box(s,x,307,w,115,label==='PCM样本数据'?C.violet:C.gray,'none',2,'file-block');txt(s,label,x+10,324,w-20,38,29.333,C.ink,true,'file-block-label','center');txt(s,answer?`${count.toLocaleString('en-US')} B`:label==='PCM样本数据'?'32,000 B':'？ B',x+10,372,w-20,38,29.333,C.ink,false,'file-block-count-'+count,'center');}
  bracket(s,64,674,440,answer?'本例结构信息：12＋24＋8＝44 B':'结构信息',C.gray,'file-overhead-bracket');bracket(s,694,1216,440,'样本数据：32,000 B',C.violet,'file-payload-bracket');txt(s,'结构示意，不按字节比例绘制。',64,533,1152,43,29.333,C.gray,false,'file-not-to-scale');
}
s=page('Q13','算出32,000 B，完整文件一定同样大吗？','提问','刚才只数样本，别人播放还需要读取格式信息。图把这个简单WAV的结构分开，先猜完整大小会不会相同，再说明多了什么。','[题目控制]\n结构名是必要背景，具体结构大小和完整大小待核对后揭示。不是所有WAV都使用本例布局。',sources.pcm);txt(s,'本例：8kHz、2秒、16bit、单声道PCM WAV。',64,170,1152,44);fileBlocks(s,false);
a=reveal(s,'Q13','文件证据','本例RIFF结构十二byte，fmt结构二十四byte，data块头八byte，共四十四byte。样本三万二千byte，加起来三万二千零四十四。只是这个简单文件的结构，不推广到所有WAV。','[真实证据]\nassets/audio/size-check-8000-2s-16-mono.wav：16000帧，2B/帧，PCM样本32000B；RIFF 12B、fmt chunk24B、data header8B、数据32000B，总32044B。结构采用字节读取独立核对。其他WAV可能有额外chunk、填充或不同格式。',sources.pcm);for(const [count,text]of [[12,'12 B'],[24,'24 B'],[8,'8 B']])a.shapes.items.find(o=>o.name===`file-block-count-${count}`).text=text;a.shapes.items.find(o=>o.name==='file-overhead-bracket-label').text='本例结构：12＋24＋8＝44 B';result(a,'32,000 B＋本例44 B＝32,044 B。','44 B属于本例，不能概括所有WAV。',592);
s=page('Q1-return','用样本数解释开场A、B的大小差异','提问','回到开场猜测。两份六秒、十六bit、单声道，只有采样率不同。分别数样本，算样本数据，再检查能否解释开场完整大小。','[课堂闭环]\n独立列式20秒，回看保留猜测，收一个修改或支持的理由。数据来自同一已解码音乐片段，不代表首次ADC或恢复来源AAC。',sources.pcm);txt(s,'相同：6秒、16 bit、单声道；不同：采样率。',64,170,1152,44);txt(s,'A：44,100 Hz；完整文件529,244 B',64,285,1152,47,32,C.ink,true,'opening-A-parameters');txt(s,'B：8,000 Hz；完整文件96,044 B',64,439,1152,47,32,C.ink,true,'opening-B-parameters');
a=reveal(s,'Q1-return','闭环揭示','A二十六万四千六百个样本，乘两byte为五十二万九千二百。B四万八千个样本，乘两byte为九万六千。数据条按样本数据量比例画出。各加本例四十四byte，得到开场大小。请修改原猜测，并说图上的哪条证据支持它。','[独立证据]\nA=44100×6×2=529200B，B=8000×6×2=96000B；两者本例完整文件均多44B。条长比529200/96000=5.5125，完整文件比并非严格等于采样率比。',sources.pcm);box(a,64,347,1040,32,'none',C.violet,0,'opening-A-payload-bar');box(a,64,501,1040*96000/529200,32,'none',C.cyan,0,'opening-B-payload-bar');txt(a,'264,600个样本 × 2 B＝529,200 B',64,388,1152,40,29.333,C.violet,true,'opening-A-payload');txt(a,'48,000个样本 × 2 B＝96,000 B',64,548,1152,40,29.333,C.cyan,true,'opening-B-payload');txt(a,'两份本例各加44 B结构信息，回到开场大小。',64,625,1152,40,29.333,C.ink,false,'opening-closure');

function aliasPlot(s,{x=225,y=270,w=890,h=90,freq=6000,caption='6 kHz'}={}) {
  const X=t=>x+t/.0005*w,Y=v=>y+(1-v)*h/2;
  txt(s,caption,64,y+16,110,43,32,C.ink,true,'signal-frequency');line(s,x,Y(0),x+w,Y(0),C.gray,1,'alias-zero');curve(s,Array.from({length:401},(_,i)=>{const t=i*.0005/400;return[X(t),Y(Math.cos(2*Math.PI*freq*t))];}),C.ink,2,'alias-input-'+freq);
  for(const v of [1,0,-1])txt(s,v===1?'+1':v===0?'0':'−1',184,Y(v)-12,34,24,20,C.gray,false,'alias-amplitude-value','right');
  for(let k=0;k<5;k++){const t=k/8000;line(s,X(t),Y(0),X(t),Y(Math.cos(2*Math.PI*freq*t)),C.gray,1.2,'alias-stem');dot(s,X(t),Y(Math.cos(2*Math.PI*freq*t)),C.violet,10,false,'alias-sample-'+k);txt(s,String(k*.125),X(t)-40,y+h+15,80,31,24,C.gray,false,'alias-time','center');}
}
s=page('Q14','不同波形，为什么可能留下相同样本？','提问','两个等幅余弦信号，一个六千Hz，一个两千Hz。相同八千Hz采样，在零点开始，观察每个紫点。两份记录能区分输入吗？先逐点比较，不先用规则替代观察。','[诊断模型]\n故意不先低通，直接采样，x(t)=cos(2πft)，t=k/8000，k=0…4。观察闭区间0–0.5ms的五个点，不用它计算录音帧数。两信号起始相位相同；cos(2π6000n/8000)=cos(2π2000n/8000)，均1,0,-1,0,1。图为原生数学证据，不是实测示波器，也不是正常重采样流程。',EXTRA.dsp+'\n'+sources.sampling);txt(s,'诊断：同幅同相余弦信号，8 kHz直接取样。',64,170,1152,44);txt(s,'归一化幅度',225,216,250,30,24,C.gray,false,'alias-amplitude-unit');aliasPlot(s,{y:254,freq:6000,caption:'6 kHz'});aliasPlot(s,{y:406,freq:2000,caption:'2 kHz'});txt(s,'时间 / ms',1080,533,150,36,24,C.gray,false,'alias-time-unit');
a=reveal(s,'Q14','证据揭示','采样点都为一、零、负一、零、一。不同的连续波形产生相同离散记录，这叫混叠，光看这些样本不能区分原来的频率。正常录音不能照这个故意省略滤波的诊断模型操作，下一页核对频率条件。','[边界]\n等幅同相余弦特例只展示混叠存在，不由五个点推导完整采样定理。相位不同要相应匹配。直接取样与先滤波必须分开。',EXTRA.dsp);result(a,'两组样本相同：1、0、−1、0、1。','不同输入可能无法区分：混叠。',604);
s=page('Q14-B','8kHz采样能保留6kHz纯音吗？','提问','给定基带带限条件：理想采样率大于最高频率两倍。声音六千Hz、采样八千Hz，能否满足？先分别指出振动次数和记录次数。','[学生任务]\n将有来源的技术规则作为条件给出，不声称从上一页五点推导定理。独立代入15秒。',sources.sampling);txt(s,'带限信号；理想条件：fs > 2 × fmax。',64,170,1152,44);txt(s,'声音6 kHz；采样8 kHz。',64,225,1152,44);line(s,150,386,1150,386,C.ink,1.6,'frequency-axis');for(let k=0;k<=8;k+=2){const x=150+k*125;line(s,x,378,x,394,C.gray,1.2,'frequency-tick');txt(s,String(k),x-30,405,60,36,26.667,C.ink,false,'frequency-tick-label','center');}txt(s,'声音频率 / kHz',910,458,306,40,29.333,C.ink,false,'frequency-unit');line(s,900,386,900,292,C.ink,2,'six-khz-component');txt(s,'6 kHz输入',798,253,220,38,29.333,C.ink,true,'input-frequency','center');
a=reveal(s,'Q14-B','条件揭示','八千没有大于一万二千。用八千采样，理想边界四千Hz，六千超过它。正常流程先用低通限制输入频率，再采样；六千分量不能保留。实际滤波还要留过渡带，不说突然完美截断，也不把听不见当数学绝对零。','[独立计算]\nfs=8000，要求fmax<4000；6000不满足。若需保留6kHz，fs>12000且采用适当滤波。前页裸采样会混叠，本页正常滤波移除越界频率；不是同一个输入输出结论。',sources.sampling);line(a,650,281,650,386,C.red,3,'nyquist-boundary');txt(a,'fs/2＝4 kHz边界',453,487,410,40,29.333,C.red,true,'nyquist-label');result(a,'正常流程：先限制频率，再采样。','6 kHz超过4 kHz边界，不能保留。',593);
s=treeBase('T4','怎样把记录参数与数据量连起来？',3,'用每秒点数、每个样本两个byte和双声道两行，说明总量怎样数。再区分样本数据与完整文件，先总结证据，再更新最后一条关系。');a=reveal(s,'T4','树揭示','新增PCM计数：每声道样本数乘声道数，再乘每样本实际字节数。采样分支提供数量，存储宽度提供每份记录大小；完整文件另计结构。三条已知关系位置不变。','[公式边界]\n固定宽度、未压缩PCM；实际帧数优先。本课16bit=2B；有效量化等级和实际容器宽度不同。',sources.pcm);treeBranch(a,3,true);
s=page('Q15','独立退出题：列式，并改写一句话','独立评价','独立六十秒，不讨论。第一题双声道，列byte计数式，并圈出哪个因子代表同一时刻两份值。第二题改写错误说法并给本课例子。先收齐纸条，再揭示。','[评分，暂不朗读]\n16kHz×2s×2声道×2B=128000B，因子与单位2分；解释声道因子1分；说明编码可以不压缩并举3bit码字例1分。漏声道回到左右两行；漏换B回到16格；把编码等同压缩回到码字互读。',sources.pcm);txt(s,'① 16kHz、2秒、16bit、双声道未压缩PCM。',64,205,1152,50,32);txt(s,'求样本数据量（B）；圈出声道因子。',64,278,1152,48);txt(s,'② 改写：“声音编码的目的就是压缩文件。”',64,405,1152,50,32);txt(s,'用本课一个例子说明理由。',64,477,1152,48);txt(s,'独立60秒；先交纸条，再核对。',64,590,1152,48,29.333,C.ink,true);
a=reveal(s,'Q15','评价揭示','纸条已经收齐。每秒每声道一万六千，两秒、两声道、每个两byte，十二万八千byte。算式中标明两声道的因子就是要圈出的那一项。编码是按约定表示数据，可以不压缩；比如本课等级三写零一一。根据收来的理由，记录需要回到哪张图再解释。','[课堂记录]\n记录错误类型、独立证据、实际时间。下列附录可选，超时全部不讲。',sources.pcm);txt(a,'16,000 × 2秒 × 2声道 × 2 B＝128,000 B',64,342,1152,44,29.333,C.violet,true,'exit-answer-1');txt(a,'编码可以不压缩；例如3 → 011。',64,538,1152,44,29.333,C.violet,true,'exit-answer-2');

const mainSlideCount=p.slides.items.length;
s=page('Q7-A','80分和60分，为什么会同属B？','可选附录提问','主线已经结束，只有学生仍难理解有限分档时使用这个类比。按左表，两个不同分数为什么有同一等级？请先说分档规则，再解释丢掉什么信息。','[可选与边界]\n非均匀成绩区间仅类比多值映射同一标签，不用于推导均匀量化误差界；不占45分钟主线预算。');table(s,[['等级','整数分数'],['A','90–100'],['B','60–89'],['C','0–59']],85,275,560,260,[220,340]);table(s,[['分数','等级'],['80',''],['60','']],735,320,460,195,[230,230]);
a=reveal(s,'Q7-A','可选附录揭示','两个都落在六十到八十九，都是B。只留下等级，不能恢复原来的精确分数。这个类比说明有限标签，不说明实际声音波形或均匀量化误差公式。','[可选]\n不追加第五档活动，避免脱离音频主线。');a.tables.items[1].getCell(1,1).value='B';a.tables.items[1].getCell(2,1).value='B';result(a,'不同分数可能映射为同一等级。','只有等级，不能恢复原来的精确分数。',597);
s=page('Q7-B','等级更多，每个样本都一定更接近吗？','可选附录提问','用同一模型中的另一个真实样本核对。输入负零点七一，四档代表负零点七五，八档代表负零点六二五。分别算误差，然后检查“每一点都更接近”是否成立。','[可选]\n主线保留误差上界结论；本页只在学生把它扩大为每点必然改善时使用。固定范围[-1,1)，均匀中点量化。',sources.quant);txt(s,'同一输入−0.71；范围、时刻与均匀分级规则不变。',64,170,1152,44);table(s,[['等级数','代表值','绝对误差'],['4','−0.75',''],['8','−0.625','']],180,285,920,240,[240,340,340]);
a=reveal(s,'Q7-B','可选附录揭示','四档误差零点零四，八档零点零八五，这一点反而更远。减小的是误差上界，从零点二五到零点一二五，不是每个样本的误差。请把过强的总结改成带条件的结论。','[独立核对]\nabs(-.71+.75)=.04；abs(-.71+.625)=.085。4级步长.5，半步长.25；8级步长.25，半步长.125。两者各自都不超过各自界。',sources.quant);a.tables.items[0].getCell(1,2).value='0.04';a.tables.items[0].getCell(2,2).value='0.085';result(a,'本例8档误差更大；两者都未超过各自上界。','误差上界减小，不等于每一点都更接近。',590);

await fs.mkdir(DIR,{recursive:true});
await (await PresentationFile.exportPptx(p)).save(path.join(DIR,'candidate.pptx'));
await fs.writeFile(path.join(DIR,'plan.json'),JSON.stringify({version:'audio-v3-20261013',mainSlideCount,baselineHash:BASELINE_HASH,manifest,amplitudes,q2,q3},null,2));
await fs.writeFile(path.join(DIR,'presentation.json'),JSON.stringify(p.toProto()));
console.log(JSON.stringify({slides:p.slides.items.length,mainSlideCount,candidate:path.join(DIR,'candidate.pptx')}));
