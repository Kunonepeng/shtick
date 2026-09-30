import fs from 'node:fs/promises';
import path from 'node:path';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const root = '/Users/chran/repo/shtick/1-2-encoding/1-2-3-image-encoding-v2';
const out = path.join(root, '.codex-build', 'candidate.pptx');
const source = path.join(root, 'assets', 'original-screenshots');
const P = Presentation.create({slideSize:{width:1280,height:720}});
const C={violet:'#6251B1',accent:'#8C64E1',cyan:'#007C9B',red:'#FF0000',ink:'#262626',muted:'#777777',white:'#FFFFFF',grid:'#D7D4EA',flower:'#D82D32',yellow:'#F2D23C',green:'#3BAE60',pink:'#EE686A',orange:'#F29438'};
const F={black:'Alibaba PuHuiTi 3.0 115 Black',bold:'Alibaba PuHuiTi 3.0 85 Bold',regular:'Alibaba PuHuiTi 3.0 55 Regular'};
const noLine={style:'solid',fill:'none',width:0};
function rect(s,x,y,w,h,fill='none',stroke='none',sw=0){return s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{style:'solid',fill:stroke,width:sw}})}
function text(s,value,x,y,w,h,size=30,color=C.ink,font=F.regular,align='left'){
  const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:noLine});
  sh.text=String(value); sh.text.style={typeface:font,fontSize:size,bold:font!==F.regular,color,alignment:align,verticalAlignment:'middle',autoFit:'none',wrap:'square',insets:{left:0,right:0,top:0,bottom:0}};
  return sh;
}
function frame(s,title){s.background.fill=C.white;rect(s,0,0,1280,11,C.violet);rect(s,0,709,1280,11,C.violet);text(s,title,64,60,1152,80,48,C.ink,F.black)}
function notes(s,purpose,id,talk,sourceRef,caveat=''){s.speakerNotes.textFrame.setText(`[问题 / 页面目的] ${purpose}\n[内部编号] ${id}\n[教师逐字稿] ${talk}\n[来源] 2026-09-29 原课逐字稿与课件照片；${sourceRef}。${caveat?`\n[技术注解] ${caveat}`:''}`)}
function line(s,x1,y1,x2,y2,color=C.accent,sw=3){const a=s.shapes.add({geometry:'line',position:{left:Math.min(x1,x2),top:Math.min(y1,y2),width:Math.abs(x2-x1),height:Math.abs(y2-y1),horizontalFlip:x2<x1,verticalFlip:y2<y1},fill:'none',line:{style:'solid',fill:color,width:sw}});return a}
function cell(s,x,y,size,fill,stroke=C.grid){rect(s,x,y,size,size,fill,stroke,1.5)}
const four=['010','121','010','030'];
const fine=['001100','011110','112211','112211','011110','001100','033330','000300'];
const six=['004400','041140','412215','512214','051150','004400','033330','000300'];
const colors={'0':C.white,'1':C.flower,'2':C.yellow,'3':C.green,'4':C.pink,'5':C.orange};
function grid(s,rows,x,y,size,mode='color'){
  for(let r=0;r<rows.length;r++)for(let c=0;c<rows[r].length;c++){
    const v=rows[r][c],px=x+c*size,py=y+r*size;cell(s,px,py,size,mode==='blank'?C.white:colors[v]);
    if(mode==='number')text(s,v,px,py,size,size,size*.52,C.ink,F.bold,'center');
  }
}
function swatches(s,x,y,size=62){[['白',C.white],['红',C.flower],['黄',C.yellow],['绿',C.green]].forEach(([n,c],i)=>{cell(s,x+i*130,y,size,c);text(s,n,x+i*130,y+size+12,size,30,25,C.ink,F.regular,'center')})}
function label(s,t,x,y,w=300,size=26,color=C.muted){text(s,t,x,y,w,42,size,color,F.regular)}
const images={};
for(const n of [4,5,20,22,25])images[n]=new Uint8Array(await fs.readFile(path.join(source,`Snip20260929_${n}.png`)));
function image(s,n,x,y,w,h,crop){s.images.add({blob:images[n],contentType:'image/png',alt:`原课课堂照片 ${n}`,position:{left:x,top:y,width:w,height:h},fit:'contain',...(crop?{crop}:{})})}
function makeTitleSlide(){const s=P.slides.add();s.background.fill=C.white;rect(s,0,0,1280,11,C.violet);rect(s,0,709,1280,11,C.violet);text(s,'图像编码',165,235,950,110,80,C.ink,F.black,'center');text(s,'从花朵到二进制图像',250,365,780,70,45,C.muted,F.regular,'center');notes(s,'图像编码','Q0','上节课讨论字符怎样进入计算机。今天换一种熟悉的信息：我们拍到的图像。先请大家想，手机里保存的花和眼前的花是一回事吗？','逐字稿 00:00:00–00:00:43，Snip 1')}
const qs=[
{id:1,title:'照片不断放大，会发生什么？',given:'先预测，再观察。',kind:'zoom',src:'00:00:43–00:02:48；Snip 3–5',ask:'先看这张花的照片。把它不断放大，你觉得会看到更多细节，还是会看到别的东西？请先说出预测。',tell:'现在看实际放大结果：边缘逐渐变糊，再放大能看到一个个纯色小方格。原课在这里请学生说出“像素”。接着问：这些像素从哪里来？'},
{id:2,title:'相机怎样“看到”一朵花？',given:'先观察花朵，再想光从哪里来。',kind:'camera',src:'00:02:48–00:06:12；Snip 6–7',ask:'我们先不谈文件。为什么眼睛能看见花？光照到花以后去了哪里？相机拍照是不是也要接收光？',tell:'光照到花，反射光进入眼睛，也可以进入相机。为了想清楚采集过程，把相机简化成横向 3 个、纵向 4 个光敏位置。每个位置只负责采集一小块信息。'},
{id:3,title:'横向 3 个、纵向 4 个，怎样写分辨率？',given:'横向 3 个采样位置；纵向 4 个采样位置。',kind:'resolution',src:'00:06:12–00:06:45；Snip 7–8',ask:'先数一数：总共有多少个采样位置？如果只写 12，能不能知道横向和纵向分别有几个？',tell:'总数是 12，但记录图像的空间排列时要写 3×4。这一步采集样本叫采样；横向像素数乘纵向像素数表示分辨率。'},
{id:4,title:'采样后，每个格子的颜色怎样记录？',given:'花朵已经划成 3×4 个格子。',kind:'quantize',src:'00:06:45–00:09:00；Snip 8–9',ask:'网格已经划好，但格子里还没有可保存的值。四种颜色怎样变成计算机下一步能处理的数？',tell:'先用四种颜色近似每格的主要颜色，再约定白 0、红 1、黄 2、绿 3。得到的数字矩阵是 010、121、010、030。用有限的数描述采样结果，这一步叫量化。'},
{id:5,title:'四种颜色需要几个 bit？',given:'3×4 个格子，颜色有白、红、黄、绿。',kind:'bits4',src:'00:09:00–00:13:35；Snip 9–10',ask:'有人会按 12 个格子想，也有人会按 4 种颜色想。现在给单个格子的颜色编码，到底需要区分多少种状态？至少几位？',tell:'2 bit 有 00、01、10、11 四种状态，刚好给四种颜色编号。原课堂学生参与的是位数判断；后面的逐格替换由教师说明。'},
{id:6,title:'把颜色编号换成二进制，叫什么？',given:'白 0、红 1、黄 2、绿 3。',kind:'encode',src:'00:13:35–00:14:46；Snip 10',ask:'前一步得到 0、1、2、3。计算机中怎样表示它们？这一步和前面的采样、量化是什么关系？',tell:'把量化后的数值转换为二进制表示，叫编码。现在串起来：采样、量化、编码。一个像素颜色用了 2 bit，所以这幅四彩图的位深度是 2。'},
{id:7,title:'怎样让数字花更接近原图？',given:'目前只有 3×4 个格子，仍使用 4 种颜色。',kind:'morepixels',src:'00:14:46–00:17:43；Snip 11 缩略图',ask:'3×4 的花还能认出来，但边缘很粗。先说办法。若有人提出增加颜色，先记下；这轮只改变采样点数量。',tell:'横向从 3 增到 6，纵向从 4 增到 8，颜色仍是四种，位深度仍是 2。比较边缘，格子变小，表示更细。注意这说的是重新采集同一对象，不是把已有图像简单插值放大。',caveat:'增加真实空间采样通常保留更多细节；插值放大不会凭空恢复原始信息。'},
{id:8,title:'位图和矢量图放大后有什么不同？',given:'把两类图都放大，观察边缘。',kind:'bitmapvector',src:'00:17:43–00:18:51；逐字稿',ask:'刚才的花由格子组成。若继续放大它，边缘会怎样？再想另一种能持续保持清晰边缘的图。',tell:'位图由像素点阵构成，放大后能看到格子；矢量图用可重新绘制的图形描述边界，改变显示尺寸时可以保持清晰边界。原课堂这段比较很短，考试范围主要看位图。'},
{id:9,title:'分辨率不变，还能怎样改进颜色？',given:'保持 6×8 个位置不变。',kind:'morecolors',src:'00:18:51–00:20:37；Snip 11 缩略图',ask:'这轮不能再改格子数量。四种颜色还是有些粗糙，接下来改什么？若要表示六种颜色，两位还够吗？',tell:'把可选颜色从四种增加到六种，2²=4 不够，2³=8 足够，所以位深度变成 3。这里的六色网格是根据课堂照片视觉重建，不冒充原课每格精确数据。',caveat:'更多颜色只在同一量化任务、其他条件相近时通常减小颜色近似误差。'},
{id:10,title:'三轮花朵实验说明了什么？',given:'先回忆每轮只改了什么，再填写结论。',kind:'summary',src:'00:20:37–00:22:29；Snip 11、13',ask:'先看三幅花。第一轮建立什么模型？第二轮改了什么？第三轮又改了什么？请先完成学案空格。',tell:'核对：图像编码经过采样、量化、编码。提高真实采样的分辨率，格子更小；在同一量化任务中增加颜色等级，位深度通常变大。位深度 n 最多表示 2ⁿ 种状态。'},
{id:11,title:'同一场景，照片大小为什么不同？',given:'比较 3×4·2 bit、6×8·2 bit、6×8·3 bit。',kind:'payload',src:'00:22:29–00:25:14；Snip 14–15',ask:'三幅图来自同一个思想实验。每个格子要占几位？格子总数又有多少？先算三幅图各需多少 bit。',tell:'依次是 24、96、144 bit。总位数等于像素总数乘每个像素的位数，也就是分辨率乘位深度。课堂中用“一人两块巧克力乘人数”的类比。'},
{id:12,title:'要用 B 表示数据量，怎样换算？',given:'1 B = 8 bit。',kind:'bytes',src:'00:25:14–00:26:28；Snip 15–16',ask:'前一页得到的是 bit。如果题目要求 Byte，应该怎么换？换成 KiB、MiB 又要怎样做？',tell:'像素数据量 B = 横向像素数 × 纵向像素数 × 位深度 ÷ 8。再除以 1024 得 KiB，再除以 1024 得 MiB。公式计算的是理想连续排列的像素有效载荷。',caveat:'BMP 完整文件还可能有文件头、信息头、调色板和行填充。参见 https://learn.microsoft.com/en-us/windows/win32/gdi/bitmap-storage'},
{id:13,title:'黑白、16 色、256 色各要几 bit？',given:'位深度 n 最多区分 2ⁿ 种状态。',kind:'colorsbits',src:'00:26:28–00:28:25；Snip 17–18',ask:'先别看答案。黑白只有两种状态，需要几位？16 色和 256 色分别找哪个 2 的幂？',tell:'黑白 1 bit，16 色 4 bit，256 色 8 bit。若分辨率是 M×N，代入前页公式即可得到理想像素数据量。'},
{id:14,title:'24 位 RGB 怎样表示丰富的颜色？',given:'R、G、B 是三个颜色通道。',kind:'rgb',src:'00:28:25–00:31:13；Snip 19',ask:'三个通道要组成 24 bit，每个通道分到几位？一个通道最多有多少个等级？',tell:'R、G、B 各 8 bit，共 24 bit。每通道 256 级，组合总数是 256³，也就是 2²⁴。课堂把三个通道比作调色。'},
{id:15,title:'一个 RGB 像素真正保存了什么？',given:'软件显示 R=220、G=95、B=15。',kind:'rgbpixel',src:'00:30:06–00:31:13；Snip 20',ask:'软件用十进制显示通道数值。计算机内部保存时，用的是十进制字符，还是三个通道的二进制位？',tell:'这三个值分别能写成 8 位二进制：220 是 11011100，95 是 01011111，15 是 00001111。一个像素合计 24 bit，也就是 3 bytes。'},
{id:16,title:'500×333 的 24 位图像有多大？',given:'分辨率 500×333；位深度 24 bit。',kind:'compute',src:'00:31:13–00:33:09；Snip 20',ask:'先算像素总数，再乘每像素 24 位。题目若要求 B 或 KiB，别忘记单位转换。',tell:'500×333×24 = 3,996,000 bit；除以 8 是 499,500 B；再除以 1024 约为 487.79 KiB。原课堂展示约 487 KB 的 BMP 文件，只作历史课堂对照。',caveat:'499,500 B 是理想像素有效载荷，不等于 BMP 完整文件大小。BMP 含头部和可能的填充。https://learn.microsoft.com/en-us/windows/win32/gdi/bitmap-storage'},
{id:17,title:'照片放大为什么会糊？',given:'回到开头那张照片。',kind:'blur',src:'00:33:09–00:33:39；Snip 21',ask:'现在用“像素”和“分辨率”回答开头的问题。把已经拍好的位图放大，究竟多出了什么？',tell:'原照片只有有限像素。放大时原有像素被拉大，并没有得到新的原始细节，所以边缘会显得粗糙。原课给出的直接建议是拍摄时适当提高分辨率。'},
{id:18,title:'AI 怎样补出照片的缺损部分？',given:'先观察破损区与完好区。',kind:'repair',src:'00:33:39–00:37:19；Snip 22–25',ask:'照片有大片缺损。请观察剩下的脸、衣服和背景，猜哪些线索能用来推断缺失处。',tell:'原课用四步连接本课：识别缺损、匹配规律、补充像素、再给像素颜色并编码。修复结果是推断的内容，不能当成重新采集的历史真实细节。',caveat:'原课“重新采样”是教学类比，不是所有修复算法的必经步骤。OpenCV 将 inpainting 描述为重建选定区域：https://docs.opencv.org/4.x/df/d3d/tutorial_py_inpainting.html'},
{id:19,title:'什么叫模拟量？',given:'观察自然界中的温度、声音和光。',kind:'analog',src:'00:37:19–00:41:41；Snip 26',ask:'温度会不会只能取整度？一段声音的强弱变化是跳着发生，还是可以连续变化？',tell:'原课把时间或空间上连续变化的物理量称为模拟量。这里强调关键词“连续”。温度、声音、光照强度都是课堂举过的例子。'},
{id:20,title:'数字量与模拟量有什么不同？',given:'观察 0、1 两种状态。',kind:'digital',src:'00:41:41–00:43:11；Snip 27',ask:'前一页的曲线可以取许多中间值。现在如果只允许 0 或 1，两种状态之间能直接存一个任意中间数吗？',tell:'在本课简化模型里，数字量使用离散状态；0 和 1 是两个明确的符号。计算机中的图像文件最终以数字数据表示。',caveat:'离散的层次与采样方式有关；课堂示意用于区分连续变化与有限状态，不等于所有数字信号只有两个电平。'},
{id:21,title:'图像怎样从模拟量变成数字量？',given:'自然界中的光 → ？ → 图像数据',kind:'digitize',src:'00:43:11–00:43:32；Snip 27',ask:'回顾整节课：花朵反射的光怎样一步步变成计算机能保存的数据？请把中间三个词按顺序说出来。',tell:'自然界中的光经采样、量化、编码，得到计算机可表示的数字图像。这一过程叫信息数字化。后续再学习数字与模拟信号之间的转换。'}
];
function givens(s,value){text(s,value,89,168,1095,50,32,C.accent,F.bold)}
function questionVisual(s,q){
  if(q.id===1){image(s,4,460,260,360,320);return}
  if(q.id===2){image(s,4,815,188,305,410);return}
  if(q.id===3){grid(s,['000','000','000','000'],500,255,72,'blank');label(s,'横向 3 个',510,565,300);return}
  if(q.id===4){grid(s,four,500,270,70,'blank');swatches(s,70,560,55);return}
  if(q.id===5){swatches(s,345,300,76);return}
  if(q.id===6){grid(s,four,520,270,70,'number');return}
  if(q.id===7){grid(s,four,460,275,70);label(s,'3×4 · 四种颜色',455,570,360);return}
  if(q.id===9){grid(s,fine,485,265,42);label(s,'6×8 · 四种颜色',470,625,370);return}
  if(q.id===10){grid(s,four,160,345,45);grid(s,fine,530,345,24);grid(s,six,865,345,24);return}
  if(q.id===11){['3×4 × 2 bit = ？','6×8 × 2 bit = ？','6×8 × 3 bit = ？'].forEach((v,i)=>text(s,v,300,270+i*90,680,70,39,C.ink,F.bold));return}
  if(q.id===12){text(s,'24 bit      96 bit      144 bit',180,335,920,75,44,C.ink,F.bold,'center');return}
  if(q.id===13){table(s,['颜色数','2','16','256'],[['位深度','？','？','？']],165,300,950,76,true);return}
  if(q.id===14){['R','G','B'].forEach((v,i)=>text(s,v,245+i*320,330,180,100,76,[C.flower,C.green,'#244BB8'][i],F.black,'center'));return}
  if(q.id===15){image(s,20,410,220,480,350);return}
  if(q.id===16){text(s,'500 × 333 × 24 bit',250,320,780,90,54,C.ink,F.bold,'center');return}
  if(q.id===17){image(s,4,490,255,300,330);return}
  if(q.id===18){image(s,22,255,210,770,405,{left:0.02,top:0.02,right:0.16,bottom:0.05});return}
  if(q.id===21){text(s,'自然界中的光',135,360,370,75,39,C.ink,F.bold);text(s,'？   ？   ？',525,360,320,75,44,C.accent,F.bold);text(s,'图像数据',920,360,250,75,39,C.ink,F.bold);return}
}
function table(s,header,rows,x,y,w,rowH,blank=false){const cols=header.length,cw=w/cols;[header,...rows].forEach((row,r)=>row.forEach((v,c)=>{rect(s,x+c*cw,y+r*rowH,cw,rowH,r===0?'#F0ECFA':C.white,C.grid,1.5);text(s,v,x+c*cw+8,y+r*rowH+4,cw-16,rowH-8,r===0?25:28,r===0?C.ink:(blank&&c>0?C.accent:C.ink),r===0?F.bold:F.regular,'center')}))}
function answerVisual(s,q){
 switch(q.id){
  case 1:image(s,5,88,200,750,430);text(s,'放大后看到像素格',860,315,320,140,40,C.accent,F.black);break;
  case 2:image(s,4,78,205,275,390);text(s,'光',392,322,75,55,37,C.ink,F.bold);text(s,'→',473,315,80,60,50,C.accent,F.bold);text(s,'花反射光',565,310,230,70,35,C.ink,F.bold);text(s,'→',805,315,80,60,50,C.accent,F.bold);grid(s,['000','000','000','000'],925,250,55,'blank');label(s,'光敏位置 3×4',908,510,300,24);break;
  case 3:grid(s,['000','000','000','000'],120,240,74,'blank');text(s,'3 × 4 = 12 个采样点',500,285,690,88,52,C.accent,F.black);text(s,'分辨率记作 3×4，保留横向和纵向。',500,410,680,110,34,C.ink,F.regular);break;
  case 4:grid(s,four,100,270,66);grid(s,four,550,270,66,'number');text(s,'4 色近似',90,555,330,60,34,C.ink,F.bold);text(s,'010 / 121 / 010 / 030',520,555,660,60,34,C.accent,F.bold);break;
  case 5:table(s,['颜色','白','红','黄','绿'],[['编号','0','1','2','3'],['二进制','00','01','10','11']],100,250,1080,95);text(s,'2 bit → 4 种状态',390,560,550,70,46,C.accent,F.black,'center');break;
  case 6:text(s,'采样',130,280,250,100,58,C.ink,F.black,'center');text(s,'→',390,285,95,90,65,C.accent,F.bold,'center');text(s,'量化',495,280,250,100,58,C.ink,F.black,'center');text(s,'→',750,285,95,90,65,C.accent,F.bold,'center');text(s,'编码',855,280,250,100,58,C.accent,F.black,'center');text(s,'四种颜色：每个像素 2 bit，位深度为 2。',185,480,900,95,36,C.ink,F.regular,'center');break;
  case 7:grid(s,four,155,245,67);grid(s,fine,780,245,39);label(s,'3×4 · 4 色 · 2 bit',140,570,380,28);label(s,'6×8 · 4 色 · 2 bit',760,570,390,28);break;
  case 8:grid(s,fine,160,268,43);text(s,'位图：放大后可见像素格',90,615,510,50,28,C.ink,F.regular);rect(s,845,260,210,210,'none',C.accent,3);const e=s.shapes.add({geometry:'ellipse',position:{left:875,top:290,width:150,height:150},fill:'none',line:{style:'solid',fill:C.accent,width:5}});text(s,'矢量图：重新绘制边界',735,615,500,50,28,C.ink,F.regular);break;
  case 9:grid(s,fine,165,245,40);grid(s,six,795,245,40);label(s,'6×8 · 4 色 · 2 bit',125,595,420,28);label(s,'6×8 · 6 色 · 3 bit',755,595,425,28);break;
  case 10:text(s,'采样  →  量化  →  编码',145,240,980,85,52,C.accent,F.black,'center');text(s,'分辨率 ↑ ：格子更小，形状更细',120,370,1040,70,38,C.ink,F.regular,'center');text(s,'颜色等级 ↑ ：位深度通常更大',120,460,1040,70,38,C.ink,F.regular,'center');text(s,'n bit 最多表示 2ⁿ 种状态',120,550,1040,70,38,C.ink,F.regular,'center');break;
  case 11:table(s,['分辨率','位深度','总 bit'],[['3×4','2','24'],['6×8','2','96'],['6×8','3','144']],125,220,1030,88);text(s,'总 bit = 分辨率 × 位深度',180,600,920,65,44,C.accent,F.black,'center');break;
  case 12:text(s,'像素数据量（B）',165,250,950,70,44,C.ink,F.black,'center');text(s,'= 横向像素数 × 纵向像素数 × 位深度 ÷ 8',105,345,1070,90,41,C.accent,F.bold,'center');text(s,'B ÷ 1024 = KiB     KiB ÷ 1024 = MiB',160,495,970,80,31,C.ink,F.regular,'center');break;
  case 13:table(s,['颜色数','2','16','256'],[['位深度','1 bit','4 bit','8 bit'],['像素数据量（B）','M×N÷8','M×N×4÷8','M×N×8÷8']],90,250,1100,95);break;
  case 14:['R','G','B'].forEach((v,i)=>{rect(s,155+i*335,260,260,150,[C.flower,C.green,'#244BB8'][i]);text(s,`${v}  8 bit`,165+i*335,290,240,90,40,C.white,F.black,'center')});text(s,'8 + 8 + 8 = 24 bit',245,455,790,70,46,C.ink,F.bold,'center');text(s,'256³ = 2²⁴ 种颜色',245,555,790,65,39,C.accent,F.bold,'center');break;
  case 15:image(s,20,70,220,540,355);text(s,'R  220  →  11011100',650,250,540,70,34,C.flower,F.bold);text(s,'G   95  →  01011111',650,355,540,70,34,C.green,F.bold);text(s,'B   15  →  00001111',650,460,540,70,34,'#244BB8',F.bold);text(s,'合计 24 bit = 3 bytes',650,565,550,60,32,C.ink,F.bold);break;
  case 16:text(s,'500 × 333 × 24 = 3,996,000 bit',105,225,1070,75,41,C.ink,F.bold,'center');text(s,'÷ 8 = 499,500 B',230,365,820,80,51,C.accent,F.black,'center');text(s,'≈ 487.79 KiB',230,500,820,85,51,C.ink,F.black,'center');break;
  case 17:grid(s,four,150,255,75);text(s,'有限像素被拉大',580,300,600,80,47,C.accent,F.black);text(s,'放大不会增加原始细节',580,405,600,90,36,C.ink,F.regular);break;
  case 18:image(s,25,92,215,1090,350);text(s,'缺损区域的内容来自推断和重建',190,575,900,65,35,C.accent,F.bold,'center');break;
  case 19:wave(s,false);text(s,'连续变化',850,300,330,75,47,C.accent,F.black);text(s,'时间或空间上可取中间值',785,400,390,105,31,C.ink,F.regular);break;
  case 20:wave(s,true);text(s,'离散的 0 / 1 状态',790,300,400,75,43,C.accent,F.black);text(s,'本课用二进制解释图像文件',790,400,400,100,29,C.ink,F.regular);break;
  case 21:const a=['自然界的光','采样','量化','编码','数字图像'];a.forEach((v,i)=>{text(s,v,45+i*245,320,210,86,i===0||i===4?33:39,i===4?C.accent:C.ink,i===4?F.black:F.bold,'center');if(i<4)text(s,'→',245+i*245,320,50,85,43,C.accent,F.bold,'center')});text(s,'信息数字化',420,495,440,90,50,C.accent,F.black,'center');break;
 }
}
function wave(s,digital){rect(s,75,275,645,240,'none',C.grid,2);line(s,95,485,690,485,C.muted,2);if(digital){const ys=[425,425,315,315,425,425,315,315,425];for(let i=0;i<ys.length-1;i++){let x1=115+i*72,x2=115+(i+1)*72;line(s,x1,ys[i],x2,ys[i],C.cyan,5);if(ys[i]!==ys[i+1])line(s,x2,ys[i],x2,ys[i+1],C.cyan,5)}}else{let last=null;for(let i=0;i<=75;i++){const x=110+i*7.5,y=400-75*Math.sin(i*.15);if(last)line(s,last[0],last[1],x,y,C.cyan,4);last=[x,y]}}}
makeTitleSlide();
for(const q of qs){
  const ask=P.slides.add();frame(ask,q.title);givens(ask,q.given);questionVisual(ask,q);notes(ask,q.title,`Q${q.id}-问`,q.ask,q.src,q.caveat);
  const ans=P.slides.add();frame(ans,q.title);answerVisual(ans,q);notes(ans,q.title,`Q${q.id}-答`,q.tell,q.src,q.caveat);
  if(q.id===18){const extra=P.slides.add();frame(extra,q.title);['识别破损区域','参照完好区域推断','补出像素内容','写入颜色数据'].forEach((v,i)=>{text(extra,`${i+1}. ${v}`,165,205+i*99,930,85,37,i===3?C.accent:C.ink,i===3?F.black:F.bold)});notes(extra,q.title,'Q18-续','原课堂把修复分成扫描识别、规律匹配、重新采样、重新量化编码。讲授时先按原课顺序说清，再提醒自己：这里的“重新采样”是课堂类比，算法实际是在已有图像中推断缺损区域。','00:34:11–00:37:19；Snip 23–24','OpenCV inpainting 重建选定区域；https://docs.opencv.org/4.x/df/d3d/tutorial_py_inpainting.html')}
}
const hw=P.slides.add();frame(hw,'课后练习');text(hw,'完成新发讲义第二页的图像编码练习。',125,305,1030,105,48,C.ink,F.black,'center');notes(hw,'完成新发讲义第二页的图像编码课后练习','Q22','今天先到这里。请完成新发讲义第二页的图像编码课后练习。做题时先分清题目问的是颜色数、位深度，还是以 bit、B、KiB 表示的数据量。','逐字稿 00:43:32–结束');
await (await PresentationFile.exportPptx(P)).save(out);
console.log(JSON.stringify({slides:P.slides.items.length,out}));
