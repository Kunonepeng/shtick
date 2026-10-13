// Browser-only rendering and playback for remote JupyterLab.
// The Python kernel may run on a macOS host; audio always plays on the viewing browser.
const V='#6251B1', P='#8C64E1', C='#00B0F0', GRID='#d9d9e0', GR='#777777', BLACK='#262626';
function el(tag,attrs={},str=''){
  const e=document.createElement(tag);
  for(const [k,v] of Object.entries(attrs)){
    if(k==='class')e.className=v;
    else if(k==='type')e.type=v;
    else e.setAttribute(k,v);
  }
  if(str)e.textContent=str;
  return e;
}
function button(label,fn){ const e=el('button',{},label);e.type='button';e.addEventListener('click',fn);return e; }
function graphBase(canvas,title='',timeMin=0,timeMax=4){
 const g=canvas.getContext('2d'),w=canvas.width,h=canvas.height;
 g.clearRect(0,0,w,h); g.fillStyle='#fff';g.fillRect(0,0,w,h);
 const x0=62,x1=w-24,y0=25,y1=h-44,ym=(y0+y1)/2;
 g.strokeStyle=GRID;g.lineWidth=1;
 for(let k=-1;k<=1;k++){
  let y=ym-k*(y1-y0)*.45;
  g.beginPath();g.moveTo(x0,y);g.lineTo(x1,y);g.stroke();
  g.fillStyle=GR;g.font='15px sans-serif';g.fillText(String(k),18,y+5);
 }
 g.strokeStyle=BLACK;g.beginPath();g.moveTo(x0,y0);g.lineTo(x0,y1);g.lineTo(x1,y1);g.stroke();
 g.fillStyle=BLACK;g.font='15px sans-serif';g.fillText('幅度',9,17);g.fillText('时间 (s)',(x0+x1)/2-25,h-9);
 g.fillStyle=GR;g.fillText(`${timeMin.toFixed(timeMax>1?1:3)} s`,x0,y1+23);
 g.fillText(`${timeMax.toFixed(timeMax>1?1:3)} s`,x1-63,y1+23);
 if(title){g.fillStyle=V;g.font='bold 19px sans-serif';g.fillText(title,x0+12,23);}
 return {g,x0,x1,y0,y1,ym,ymap:v=>ym-v*(y1-y0)*.45,xmap:t=>x0+(t-timeMin)/(timeMax-timeMin)*(x1-x0)};
}
function plotEnvelope(canvas,payload,t){
 const d=graphBase(canvas,'整段录音',0,payload.duration); const {g,xmap,ymap}=d;
 const env=payload.envelope;
 g.strokeStyle=P;g.lineWidth=2;
 for(let i=0;i<env.length;i++){
  const x=xmap(payload.duration*(i+.5)/env.length);
  g.beginPath();g.moveTo(x,ymap(env[i][0]));g.lineTo(x,ymap(env[i][1]));g.stroke();
 }
 g.strokeStyle='#ff0000';g.lineWidth=2.4;
 const x=xmap(Math.min(payload.duration,Math.max(0,t)));
 g.beginPath();g.moveTo(x,d.y0);g.lineTo(x,d.y1);g.stroke();
}
function timeLabel(t){return `${t.toFixed(2)} s`;}
function audioControls(payload,update){
 const row=el('div',{class:'bar'});
 const audio=el('audio',{controls:'',preload:'auto',style:'max-width:740px;width:100%'});
 audio.src='data:audio/wav;base64,'+payload.audio_b64;
 audio.addEventListener('timeupdate',()=>update(audio.currentTime));
 audio.addEventListener('seeked',()=>update(audio.currentTime));
 audio.addEventListener('ended',()=>update(payload.duration));
 row.appendChild(audio);
 return {row,audio};
}
function makePlayer(root,payload,zoom){
 root.appendChild(el('h3',{}, zoom?'Demo B｜放大波形，找到样本点':'Demo A｜听见声音，看见波形'));
 root.appendChild(el('div',{class:'tip'}, zoom?'先观察整段声音，再选择时间位置并放大。小圆点是实际保存的数字样本。':'请点击浏览器里的播放键。红色光标跟随教室电脑的播放进度，而不是Mac音箱。'));
 const overview=el('canvas',{width:'960',height:zoom?'205':'250'});root.appendChild(overview);
 const status=el('div',{class:'readout'},'准备播放。');root.appendChild(status);
 let current=0, raf=0;
 const {row,audio}=audioControls(payload,t=>{current=t;});
 root.insertBefore(row,overview);
 let detail=null,slider=null,zoomChoice=null;
 if(zoom){
  const controls=el('div',{class:'bar'});
  controls.appendChild(el('span',{},'观察时刻'));
  slider=el('input',{type:'range',min:'.01',max:String(payload.duration-.01),step:'.001',value:'.45',style:'width:390px;max-width:80%'});
  controls.appendChild(slider);
  controls.appendChild(el('span',{},'局部显示范围'));
  zoomChoice=el('select');
  [['0.100','100毫秒'],['0.020','20毫秒'],['0.004','4毫秒']].forEach(([v,label])=>{const o=el('option',{value:v},label);if(v==='0.020')o.selected=true;zoomChoice.appendChild(o);});
  controls.appendChild(zoomChoice);root.appendChild(controls);
  detail=el('canvas',{width:'960',height:'215'});root.appendChild(detail);
  root.appendChild(el('div',{class:'small'},'整段图是极值概览；局部小圆点才是实际样本。投影时可用浏览器 F11 全屏。')); 
  slider.addEventListener('input',redraw);zoomChoice.addEventListener('change',redraw);
  overview.addEventListener('click',e=>{const bounds=overview.getBoundingClientRect();const px=(e.clientX-bounds.left)/(bounds.width||1)*overview.width;const relative=Math.max(0,Math.min(1,(px-62)/(overview.width-24-62)));slider.value=String(relative*payload.duration);redraw();});
 }
 function localPlot(){
  if(!detail)return;
  const width=Number(zoomChoice.value),center=Number(slider.value);
  const left=Math.max(0,Math.min(payload.duration-width,center-width/2)),right=left+width;
  const d=graphBase(detail,`局部放大｜${(width*1000).toFixed(0)}毫秒`,left,right);
  const {g,xmap,ymap}=d;
  const start=Math.ceil(left*payload.rate),last=Math.min(payload.samples.length-1,Math.floor(right*payload.rate));
  g.strokeStyle='#999';g.lineWidth=1.3;g.beginPath();
  for(let i=start;i<=last;i++){
    const x=xmap(i/payload.rate),y=ymap(payload.samples[i]);
    if(i===start)g.moveTo(x,y);else g.lineTo(x,y);
  }
  g.stroke();
  // Real samples (not the envelope). Keep markers visually distinct from a connecting guide.
  g.fillStyle=C;
  for(let i=start;i<=last;i++){
    const x=xmap(i/payload.rate),y=ymap(payload.samples[i]);
    g.beginPath();g.arc(x,y,3.2,0,Math.PI*2);g.fill();
  }
 }
 function redraw(){
  const t=audio.currentTime||current;
  plotEnvelope(overview,payload,zoom?Number(slider.value):t);
  if(!zoom)status.textContent=`播放进度 ${timeLabel(t)} / ${timeLabel(payload.duration)}。横轴：时间；纵轴：信号幅度。`;
  else {
    localPlot();
    status.textContent=`整段录音共 ${payload.length.toLocaleString()} 个样本，采样率 ${payload.rate.toLocaleString()} Hz；当前观察时刻 ${Number(slider.value).toFixed(3)} 秒。`;
  }
 }
 let lastDraw=0;
 function animate(now){if(!document.hidden && now-lastDraw>=65){redraw();lastDraw=now;}raf=requestAnimationFrame(animate);}
 redraw();raf=requestAnimationFrame(animate);
 return ()=>{cancelAnimationFrame(raf);audio.pause();audio.removeAttribute('src');};
}
function makeLab(root,payload){
 root.appendChild(el('h3',{},'Demo C｜从采样点到二进制码字'));
 root.appendChild(el('div',{class:'tip'},'同一条输入波形、同一段4毫秒时间；每次只改变一个条件。先让同学预测，再点击。'));
 const buttons=el('div',{class:'bar'}),stageLabels=['① 原波形','② 采样','③ 量化','④ 编码'];
 let stage=0,rate='4000',bits='3',selected=0;
 stageLabels.forEach((label,i)=>buttons.appendChild(button(label,()=>{stage=i;redraw();})));
 root.appendChild(buttons);
 const controls=el('div',{class:'bar'});
 controls.appendChild(el('span',{},'采样率（教学模型）'));
 const rs=el('select');for(const r of ['2000','4000','8000'])rs.appendChild(el('option',{value:r},`${Number(r)/1000} kHz`));rs.value=rate;
 controls.appendChild(rs);controls.appendChild(el('span',{},'量化位数'));
 const bs=el('select');for(const b of ['2','3','4'])bs.appendChild(el('option',{value:b},`${b} bit / ${2**Number(b)}级`));bs.value=bits;
 controls.appendChild(bs);root.appendChild(controls);
 const canvas=el('canvas',{width:'960',height:'350'});root.appendChild(canvas);
 const readout=el('div',{class:'readout'});root.appendChild(readout);
 root.appendChild(el('p',{class:'small'},'2、4、8 kHz仅用于放大观察4毫秒信号，并不是推荐的日常录音参数。紫色方块是量化值；蓝色圆点是采样原值。'));
 rs.addEventListener('change',()=>{rate=rs.value;selected=0;redraw();});
 bs.addEventListener('change',()=>{bits=bs.value;redraw();});
 canvas.addEventListener('click',e=>{if(stage===0)return;const b=canvas.getBoundingClientRect();const x=(e.clientX-b.left)/b.width*canvas.width;const arr=payload.rates[rate];let best=0,dist=Infinity;arr.forEach((a,i)=>{const px=62+a.t_ms/4*(canvas.width-86);let d=Math.abs(x-px);if(d<dist){dist=d;best=i;}});selected=best;redraw();});
 function redraw(){
  [...buttons.children].forEach((x,i)=>x.classList.toggle('active',i===stage));
  const series=payload.rates[rate];
  const d=graphBase(canvas,'同一条波形（4毫秒）',0,.004),{g,x0,x1,ymap}=d;
  const xmap=t=>x0+(t/4)*(x1-x0);
  const n=2**Number(bits);
  if(stage>=2){for(let k=0;k<n;k++){
    let v=-1+(k+.5)*2/n;
    g.strokeStyle='#ded6f8';g.lineWidth=1;
    g.beginPath();g.moveTo(x0,ymap(v));g.lineTo(x1,ymap(v));g.stroke();
  }}
  g.strokeStyle='#777';g.lineWidth=2.2;g.beginPath();
  for(let i=0;i<=420;i++){
    let t=4*i/420,amp=payload.amplitude*Math.sin(2*Math.PI*payload.frequency*t/1000+payload.phase);
    if(i===0)g.moveTo(xmap(t),ymap(amp));else g.lineTo(xmap(t),ymap(amp));
  }
  g.stroke();
  if(stage>=1){series.forEach((p,i)=>{
    let x=xmap(p.t_ms),y=ymap(p.amplitude),q=p.by_bits[bits],qy=ymap(q.quant);
    g.strokeStyle='#e7e7eb';g.lineWidth=1;g.beginPath();g.moveTo(x,32);g.lineTo(x,d.y1);g.stroke();
    if(stage>=2){g.strokeStyle='#ff0000';g.lineWidth=1;g.beginPath();g.moveTo(x,y);g.lineTo(x,qy);g.stroke();g.fillStyle=P;g.fillRect(x-4,qy-4,8,8);}
    g.fillStyle=C;g.beginPath();g.arc(x,y,i===selected?6:4.3,0,Math.PI*2);g.fill();
    if(i===selected){g.strokeStyle='#ff0000';g.lineWidth=2;g.beginPath();g.arc(x,y,9,0,Math.PI*2);g.stroke();}
  });}
  const p=series[selected],q=p.by_bits[bits];
  let info='';
  if(stage===0)info='灰色曲线：同一位置的信号随时间连续变化。它不是声音传播的路线。';
  if(stage===1)info=`采样率 ${Number(rate).toLocaleString()} Hz；4毫秒内记录了 ${series.length} 个采样值。采样并没有改变纵向量化等级。`;
  if(stage===2)info=`量化等级：${n}级；选中样本原值 ${p.amplitude.toFixed(3)} → 代表值 ${q.quant.toFixed(3)}。`;
  if(stage===3)info=`样本 ${selected+1}：量化等级编号 ${q.level} → ${q.binary}（${bits} bit）。每个样本按时间顺序保存。`;
  readout.textContent=info;
 }
 redraw();return ()=>{};
}
export default {
 render({model,el:mount}){
  const root=el('div',{class:'audio-v7'});
  mount.replaceChildren(root);
  const data=model.get('payload'),mode=model.get('mode');
  let cleanup=()=>{};
  if(mode==='player'||mode==='zoom')cleanup=makePlayer(root,data,mode==='zoom');
  else if(mode==='lab')cleanup=makeLab(root,data);
  else root.textContent='未知演示模式';
  return cleanup;
 }
};
