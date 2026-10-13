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
function graphBase(canvas,title='',timeMin=0,timeMax=4,rightMargin=24){
 const g=canvas.getContext('2d'),w=canvas.width,h=canvas.height;
 g.clearRect(0,0,w,h); g.fillStyle='#fff';g.fillRect(0,0,w,h);
 const x0=62,x1=w-rightMargin,y0=25,y1=h-44,ym=(y0+y1)/2;
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
function buildQuantizerRows(bits) {
 const levels=2**Number(bits), result=[];
 for(let code=0;code<levels;code++){
  const low=-1+2*code/levels, high=-1+2*(code+1)/levels, rep=(low+high)/2;
  result.push({code,low,high,rep,binary:code.toString(2).padStart(Number(bits),'0')});
 }
 return result;
}
function quantRange(r,last) {
 return '['+r.low.toFixed(3)+', '+r.high.toFixed(3)+(last?']':')');
}
function makeLab(root,payload) {
 root.appendChild(el('h3',{},'Demo C｜从采样点到二进制码字'));
 root.appendChild(el('div',{class:'tip'},'固定同一条输入波形与4毫秒窗口。每次只改变一个条件：先预测，再观察。'));
 const buttons=el('div',{class:'bar'}),stageLabels=['① 原波形','② 采样','③ 量化','④ 编码'];
 let stage=0,rate='4000',bits='3',selected=0;
 stageLabels.forEach((label,i)=>buttons.appendChild(button(label,()=>{stage=i;draw();})));
 root.appendChild(buttons);
 const controls=el('div',{class:'bar'});
 controls.appendChild(el('label',{},'采样率（教学模型）'));
 const rs=el('select');
 ['2000','4000','8000'].forEach(r=>rs.appendChild(el('option',{value:r},(Number(r)/1000)+' kHz')));
 rs.value=rate;
 controls.appendChild(rs);
 controls.appendChild(el('label',{},'量化位数'));
 const bs=el('select');
 ['2','3','4'].forEach(b=>bs.appendChild(el('option',{value:b},b+' bit / '+(2**Number(b))+'级')));
 bs.value=bits;
 controls.appendChild(bs);
 root.appendChild(controls);
 const canvas=el('canvas',{width:'1020',height:'392'});
 root.appendChild(canvas);
 const legend=el('div',{class:'audio-legend'});
 [['原始波形','#777777','line'],['采样点',C,'dot'],['量化值',P,'square'],['等级线',V,'dash'],['选中及误差','#e34444','line']].forEach(([name,color,kind])=>{
  const lab=el('span',{class:'legend-item'});
  const mark=el('span',{class:'legend-mark '+kind,style:'--mark:'+color});
  lab.appendChild(mark);lab.appendChild(el('span',{},name));legend.appendChild(lab);
 });
 root.appendChild(legend);
 const readout=el('div',{class:'readout'});root.appendChild(readout);
 const codetitle=el('h4',{},'全部样本的二进制编码（按时间先后）');
 const codeStrip=el('div',{class:'code-strip'});
 root.appendChild(codetitle);root.appendChild(codeStrip);
 const tabletitle=el('h4',{},'各等级的输入范围与代表值');
 const tableWrap=el('div',{class:'quant-table-scroll'});
 root.appendChild(tabletitle);root.appendChild(tableWrap);
 root.appendChild(el('p',{class:'small'},'注意：2 / 4 / 8 kHz 只用于放大观察4毫秒的教学模型，不是日常录音参数。'));
 function refreshCodes(series){
  codeStrip.replaceChildren();
  if(stage<3){codeStrip.appendChild(el('span',{class:'small'},'进入④ 编码后，这里才显示每个样本对应的码字。'));return;}
  series.forEach((p,i)=>{
   const q=p.by_bits[bits];
   const chip=button('',()=>{selected=i;draw();});
   chip.className='code-chip'+(i===selected?' selected':'');
   chip.setAttribute('aria-label','选择第'+(i+1)+'个样本，编码'+q.binary);
   chip.appendChild(el('span',{class:'small'},'点'+(i+1)));
   chip.appendChild(el('b',{},q.binary));
   codeStrip.appendChild(chip);
  });
 }
 function refreshTable(rows,chosen){
  const table=el('table',{class:'quant-table'}),head=el('thead'),thead=el('tr');
  ['等级','输入幅度范围','量化代表值','二进制码字'].forEach(s=>thead.appendChild(el('th',{},s)));
  head.appendChild(thead);table.appendChild(head);
  const tbody=el('tbody');
  rows.forEach((row,i)=>{
   const tr=el('tr',{class:(i===chosen&&stage>=2)?'highlight':''});
   tr.appendChild(el('td',{},'L'+row.code));
   tr.appendChild(el('td',{},quantRange(row,i===rows.length-1)));
   tr.appendChild(el('td',{},row.rep.toFixed(3)));
   tr.appendChild(el('td',{},row.binary));
   tbody.appendChild(tr);
  });
  table.appendChild(tbody);tableWrap.replaceChildren(table);
 }
 function draw(){
  [...buttons.children].forEach((b,i)=>b.classList.toggle('active',i===stage));
  const series=payload.rates[rate], rows=buildQuantizerRows(bits),n=rows.length;
  selected=Math.min(selected,series.length-1);
  // The plot reserves 116 pixels on the right for non-overlapping level labels.
  const d=graphBase(canvas,'同一条波形（4毫秒）',0,.004,116);
  const {g,x0,x1,ymap}=d;
  const xmap=ms=>x0+(ms/4)*(x1-x0);
  const active=series[selected].by_bits[bits];
  if(stage>=2){
   rows.forEach((row,i)=>{
    const y=ymap(row.rep);
    g.strokeStyle=i===active.level?V:'#aa8ceb';
    g.lineWidth=i===active.level?2.8:1.8;
    g.setLineDash([9,5]);g.beginPath();g.moveTo(x0,y);g.lineTo(x1,y);g.stroke();g.setLineDash([]);
    g.fillStyle=i===active.level?V:'#6e579f';
    g.font=i===active.level?'bold 12px sans-serif':'12px sans-serif';
    g.fillText('L'+i+'  '+row.rep.toFixed(2),x1+10,y+4);
   });
  }
  g.strokeStyle=GR;g.lineWidth=2.6;g.beginPath();
  for(let i=0;i<=600;i++){
   const t=4*i/600,amp=payload.amplitude*Math.sin(2*Math.PI*payload.frequency*t/1000+payload.phase);
   if(i===0)g.moveTo(xmap(t),ymap(amp));else g.lineTo(xmap(t),ymap(amp));
  }
  g.stroke();
  if(stage>=1)series.forEach((p,i)=>{
   const x=xmap(p.t_ms),y=ymap(p.amplitude),q=p.by_bits[bits],qy=ymap(q.quant);
   g.strokeStyle='#dedee4';g.lineWidth=1;g.beginPath();g.moveTo(x,d.y0);g.lineTo(x,d.y1);g.stroke();
   if(stage>=2){
    g.strokeStyle=i===selected?'#dc3030':'#ecb5b5';g.lineWidth=i===selected?2.2:1.1;
    g.beginPath();g.moveTo(x,y);g.lineTo(x,qy);g.stroke();
    g.fillStyle=P;g.fillRect(x-5,qy-5,10,10);
   }
   g.fillStyle=C;g.beginPath();g.arc(x,y,i===selected?6:4.6,0,Math.PI*2);g.fill();
   if(i===selected){g.strokeStyle='#e23e3e';g.lineWidth=2.2;g.beginPath();g.arc(x,y,9,0,Math.PI*2);g.stroke();}
  });
  const p=series[selected],q=p.by_bits[bits],row=rows[q.level];
  const text=stage===0?'灰色曲线表示同一位置的信号随时间变化，不是声音在空气中传播的路线。':
             stage===1?'采样：'+Number(rate).toLocaleString()+' Hz；4毫秒内记录 '+series.length+' 个点。改变采样率，只会改变横向取样点数量。':
             stage===2?'样本'+(selected+1)+'：原值 '+p.amplitude.toFixed(3)+' 落在 '+quantRange(row,q.level===n-1)+'，所以量化为 L'+q.level+'，代表值 '+q.quant.toFixed(3)+'。':
             '样本'+(selected+1)+'：原值 '+p.amplitude.toFixed(3)+' → L'+q.level+' → '+q.quant.toFixed(3)+' → '+q.binary+'（'+bits+' bit）。';
  readout.textContent=text;
  if(stage>=2)refreshTable(rows,q.level);else tableWrap.replaceChildren(el('span',{class:'small'},'进入③ 量化后，展示对应范围、代表值与码字。'));
  refreshCodes(series);
 }
 rs.addEventListener('change',()=>{rate=rs.value;selected=0;draw();});
 bs.addEventListener('change',()=>{bits=bs.value;draw();});
 canvas.addEventListener('click',e=>{
  if(stage===0)return;
  const box=canvas.getBoundingClientRect();
  const x=(e.clientX-box.left)*canvas.width/box.width;
  const x0=62,x1=canvas.width-116,arr=payload.rates[rate];
  let nearest=0,dist=Infinity;
  arr.forEach((p,i)=>{let dd=Math.abs(x-(x0+(p.t_ms/4)*(x1-x0)));if(dd<dist){nearest=i;dist=dd;}});
  selected=nearest;draw();
 });
 draw();return ()=>{};
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
