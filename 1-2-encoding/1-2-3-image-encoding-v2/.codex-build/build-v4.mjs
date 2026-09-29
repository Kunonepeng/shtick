import fs from 'node:fs/promises';
import path from 'node:path';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
import {qs} from './lesson-data-v4.mjs';
const root='/Users/chran/repo/shtick/1-2-encoding/1-2-3-image-encoding-v2';
const P=Presentation.create({slideSize:{width:1280,height:720}});
const F={regular:'Alibaba PuHuiTi 3.0 55 Regular',black:'Alibaba PuHuiTi 3.0 115 Black',bold:'Alibaba PuHuiTi 3.0 115 Black'};
const C={ink:'#262626',violet:'#6251B1',accent:'#8C64E1',cyan:'#007C9B',red:'#FF0000',grid:'#C8C3D5',muted:'#808080'};
const palette=['#FFFFFF','#E01826','#F6D934','#35AE3D','#AA1825','#F58B29'];
const four=['010','121','010','030'];
const fine=['001100','011110','112211','112211','011110','001100','033330','000300'];
// Six-color reconstruction is illustrative: the source does not resolve every cell.
const six=['001100','014410','145211','112541','014410','001100','033330','000300'];
const plan=[];const pairs=[];
function rect(s,x,y,w,h,fill='none',stroke='none',width=0){return s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width,style:'solid'}})}
function text(s,t,x,y,w,h,size=29.333,color=C.ink,font=F.regular,align='left'){
 const sh=s.shapes.add({geometry:'textbox',name:'text-'+s.shapes.items.length,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});sh.text=String(t);sh.text.style={typeface:font,fontSize:size,color,bold:font!==F.regular,alignment:align,verticalAlignment:'middle',wrap:'square',autoFit:'none',insets:{left:0,right:0,top:0,bottom:0}};return sh;
}
function line(s,x1,y1,x2,y2,color=C.grid,width=2){return s.shapes.add({geometry:'line',position:{left:Math.min(x1,x2),top:Math.min(y1,y2),width:Math.abs(x2-x1),height:Math.abs(y2-y1),horizontalFlip:x2<x1,verticalFlip:y2<y1},line:{fill:color,width,style:'solid'}})}
function ellipse(s,x,y,w,h,fill,stroke='none',width=0){s.shapes.add({geometry:'ellipse',position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width,style:'solid'}})}
function frame(title){const s=P.slides.add();s.background.fill='#FFFFFF';rect(s,0,0,1280,10.666667,C.violet);rect(s,0,709.333333,1280,10.666667,C.violet);text(s,title,63.84,63.84,1152,73.92,48,C.ink,F.black);return s;}
function grid(s,rows,x,y,z,mode='color') {rows.forEach((row,r)=>[...row].forEach((n,c)=>{rect(s,x+c*z,y+r*z,z,z,mode==='binary'?'#FFFFFF':palette[+n],C.grid,1);if(mode==='number'||mode==='binary')text(s,mode==='binary'?(+n).toString(2).padStart(2,'0'):n,x+c*z,y+r*z,z,z,mode==='binary'?30:32,C.ink,F.bold,'center')}));}
function flower(s,x,y,w,h,mesh=false){
 const k=w/300;const e=(a,b,c,d,col)=>ellipse(s,x+a*k,y+b*k,c*k,d*k,col);
 rect(s,x+145*k,y+190*k,12*k,195*k,palette[3]);e(40,310,113,45,palette[3]);e(155,297,105,45,palette[3]);
 for(let i=0;i<8;i++){const a=i*Math.PI/4;e(105+75*Math.cos(a),115+75*Math.sin(a),90,100,palette[1]);}
 e(100,108,100,105,palette[2]);e(118,129,10,14,palette[5]);e(147,143,10,14,palette[5]);e(172,165,10,14,palette[5]);e(128,176,10,14,palette[5]);
 if(mesh){for(let c=0;c<=3;c++)line(s,x+c*w/3,y,x+c*w/3,y+h,C.ink,1.5);for(let r=0;r<=4;r++)line(s,x,y+r*h/4,x+w,y+r*h/4,C.ink,1.5);}
}
const imgs={};for(const n of [4,5,20,22,25])imgs[n]=new Uint8Array(await fs.readFile(path.join(root,'assets/original-screenshots',`Snip20260929_${n}.png`)));
function img(s,n,x,y,w,h,crop){s.images.add({blob:imgs[n],contentType:'image/png',alt:`原课照片 Snip20260929_${n}`,position:{left:x,top:y,width:w,height:h},fit:'contain',...(crop?{crop}:{})});}
function table(s,values,x,y,w,h){const t=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,values});t.borders.assign({fill:C.grid,width:1,style:'solid'});for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){const cell=t.getCell(r,c);cell.fill=r===0?'#F0ECFA':'#FFFFFF';cell.text.style={typeface:r===0?F.bold:F.regular,fontSize:29.333,color:C.ink,bold:r===0,alignment:'center',verticalAlignment:'middle',autoFit:'none'};}return t;}
function replaceField(s,name,value,size=34){const sh=s.shapes.items.find(x=>x.name===name);sh.text=value;sh.text.style={typeface:F.black,fontSize:size,bold:true,color:C.accent,verticalAlignment:'middle',autoFit:'none',insets:{left:0,right:0,top:0,bottom:0}};}
function revealCells(s,values){const t=s.tables.items[0];for(const [r,c,v] of values){t.getCell(r,c).value=v;t.getCell(r,c).text.style={typeface:F.bold,fontSize:29.333,color:C.accent,bold:true,alignment:'center',verticalAlignment:'middle',autoFit:'none'};}}
function right(s,lines){lines.forEach((v,i)=>text(s,v,660,265+i*105,525,88,i===0?40:32,i===0?C.accent:C.ink,i===0?F.black:F.regular));}
function swatches(s,x,y,arr=palette.slice(0,4),z=54){arr.forEach((col,i)=>rect(s,x+i*(z+32),y,z,z,col,C.grid,1));}
const extra={
1:{expected:'可能说“更清楚”“变模糊”“看到小方格”。接受预测，证据出现后再命名像素。',follow:'放大是得到新的细节，还是放大已有信息？先留下问题。',task:'预测放大结果，观察真实软件放大截图，指出一个像素格。',transition:'看到了格子；下一步追问格子如何从眼前的花得到。'},
2:{expected:'学生可能说眼睛看到了花，也可能提出像素越高越好。把话题拉回反射光与采集。',follow:'感光的是相机的图像传感器，镜头主要负责成像。',task:'解释光如何从花进入眼睛或相机；先提出“像素能否盲目增加”的悬问。',transition:'把传感器简化为横向3个、纵向4个位置，开始采样。'},
3:{expected:'12是总数量，3×4还能说明横向和纵向排列。',follow:'2×6和3×4总数相同，形状相同吗？',task:'数位置并比较“12”与“3×4”的信息差别。',transition:'位置确定了，还要决定每个位置用什么数记录。'},
4:{expected:'用颜色名、编号；也可能想保留格子内所有细节。强调本轮每格只留一个代表色。',follow:'这一格同时有两种颜色时，我们是否保留了全部信息？',task:'看红花和四彩图，说明近似；读颜色编号与数字矩阵。',transition:'编号还要转换成二进制，才能讨论每格需要多少位。'},
5:{expected:'原课出现3位、4位，甚至把12个格子当作状态数。也有学生答2位，并给出00/01/10/11的四色映射。',follow:'现在给一个像素的颜色编码，要区分12个位置，还是4种颜色？',task:'判断最少位数，再口头给白、红、黄、绿编码。',transition:'有了颜色码表，再由教师逐格替换，命名编码和位深度。'},
6:{expected:'学生可说编码，但可能把整图24bit当成位深度。',follow:'位深度描述一个像素，还是整幅图？',task:'跟随教师将0/1/2/3替换成00/01/10/11，回顾三步骤。',transition:'图像能保存了，但粗糙的花形制造新的问题。'},
7:{expected:'增加格子、提高分辨率；位深度不变，因为仍有4种颜色。',follow:'第四行先辨颜色，再用码表读出二进制；不要把颜色编号直接当成二进制。',task:'比较3×4与6×8，保持颜色数不变；读6×8第四行的编码。',transition:'点阵图引出位图概念，再探索另一条改进途径。'},
8:{expected:'位图边缘出现格子；矢量边界可随显示大小重新绘制。',follow:'本课随后计算的对象是哪一类图？',task:'比较两类图形的放大边缘；把讨论收回位图。',transition:'回到6×8花朵，保持位置不变再改变颜色。'},
9:{expected:'增加颜色；6种状态需3bit，而不是6bit。',follow:'2bit可区分几种？3bit有8个码字，为什么6种也够？',task:'比较四/六色；判断最少3bit。六色逐格编码由教师说明，不要求学生复原照片。',transition:'三轮实验结束，用学案空格把改变的变量和结果分清。'},
10:{expected:'采样、量化、编码；分辨率提高；颜色等级增加；n位最多2^n种。',follow:'第二轮变了哪个量？第三轮又保持了什么？',task:'在纸上填写投影空格，逐项口头核对。',transition:'更细、更丰富都要付出存储代价，回收“像素能否盲目增加”的悬问。'},
11:{expected:'学生可能只相加；使用人数乘每人巧克力的原课类比解释相乘。',follow:'像素数相当于人数，位深度相当于每人份数；结果单位是什么？',task:'依次列出三组乘法，不急于背公式，再归纳总bit。',transition:'从bit换成B，让公式的单位完整。'},
12:{expected:'除以8；进一步按1024换算。',follow:'题目求bit时还要除以8吗？求KiB时还需要哪一步？',task:'把24/96/144bit转成3/12/18B，归纳通式。',transition:'用不同颜色数练习寻找位深度再代公式。'},
13:{expected:'黑白1bit、16色4bit、256色8bit；M×N是像素数。',follow:'颜色数与位深度是一回事吗？',task:'填写位深度和B单位算式，不要求约分。',transition:'24位真彩色沿用同一公式，但需要解释24的构成。'},
14:{expected:'24位最多2^24种，数据量M×N×24÷8；RGB各8位、各256级。',follow:'三个通道各256级，是相加还是相乘？',task:'先补24位真彩色一列，再解释RGB三个通道和组合。',transition:'用Photoshop显示的具体像素检验24位模型。'},
15:{expected:'软件为人显示十进制，存储采用二进制；每通道补足8位。',follow:'G和B前面的0可以在这个固定宽度模型里省掉吗？',task:'读取R220/G95/B15，并观察三个8位二进制值。',transition:'从一个像素的3bytes，计算整幅500×333图像。'},
16:{expected:'有人遗漏除8或除1024。正确结果499500B≈487.79KiB。',follow:'公式算的是像素有效载荷，文件头等信息算进去了吗？',task:'先独立列式和计算，再看原课文件属性作为量级对照。',transition:'回到开场，用像素解释放大；存储代价解释像素不应盲目追高。'},
17:{expected:'把有限像素放大，并未增加采集到的原始细节。',follow:'拍摄时提高真实采样分辨率，与拍好后放大是同一件事吗？',task:'解释模糊，并给出拍摄时适当提高分辨率的建议。',transition:'如果原图的信息已经缺失，AI又是怎样补出内容的？'},
18:{expected:'学生会提到周边图像、规律、模型；原课有学生报告修复效果不好。',follow:'补得像原样，是否证明恢复了拍摄时的真实细节？',task:'观察破损和修复对照，结合周边内容推测修复思路。',transition:'把花、像素和数据重新放回“连续与离散”的统一模型。'},
19:{expected:'温度、声波随时间；压强、光照例子随空间。',follow:'两次测量之间是否仍可有温度值？连续不只是“画线不断”。',task:'先分类四个原课例子，再辨认连续变化。',transition:'采样后的有限位置与量化后的有限等级，引出数字量。'},
20:{expected:'数字数据采用离散状态；0/1是编码符号，不表示只能存数值0和1。',follow:'多个bit组成码字后，能不能表示220？',task:'比较连续曲线与采样位置、有限等级、二进制码字的关系。',transition:'回扣花朵思想实验，完整说出信息数字化过程。'},
21:{expected:'采样、量化、编码，得到数字图像；称为信息数字化。',follow:'哪个环节决定采样位置，哪个环节决定有限的颜色等级？',task:'口头补完整条链，再解释每个步骤做了什么。',transition:'课后用补充练习检查位深度、数据量和放大解释。'}
};
const changes={
1:{tell:'现在看实际放大的结果：先是细节看不清，继续放大可以看到一个个颜色小格。谁能指出其中一个格子？这些图像单元叫像素。注意这是一张位图，接下来我们讨论它的像素怎样从眼前的花得到。'},
8:{tell:'左边用像素点阵表示边缘，放大后格子也被放大；右边保留的是可重新绘制的图形描述，可以按新的显示尺寸绘出边界。我们接下来继续讨论位图的数据。矢量图最终在屏幕上显示时也会被栅格化，并不是屏幕没有像素。'},
11:{tell:'第一幅有12个像素，每个2bit，所以是3×4×2=24bit。好比40个人每人两块巧克力，总数要用40×2。第二幅像素多了，每格位数没变，得到96bit；第三幅每格改成3bit，得到144bit。请自己把共同结构说出来：像素总数乘每像素位数。这也解释了更高分辨率和更高位深度的存储代价。'},
17:{tell:'这张照片只有有限的像素。放大时已有像素被拉大或通过插值产生中间值，但没有重新采到场景细节。若目标是拍摄后还能放大查看，可以在拍摄时适当提高真实采样分辨率，同时考虑存储量、镜头、对焦等条件。接下来，如果信息已经缺失，AI补出来的又是什么？'},
2:{title:'相机怎样“看到”一朵花？',given:'把眼前的红花变成可以保存的数据。',tell:'看左边这朵红花。我们看到它，是因为花反射的光进入眼睛；相机也要接收这些光。光经过镜头成像，由图像传感器感光。今天把复杂的相机简化成12个采样位置，每个位置只记录局部信息。先留下一个问题：位置越多就一定越好吗？等算存储量时再回答。'},
3:{title:'为什么写 3×4，而不只写 12？',given:'横向3个位置，纵向4个位置。'},
4:{given:'每格只用白、红、黄、绿中的一种颜色近似。',tell:'看中间的方格花：同一个格子里原本可能有多种颜色，这里只用一种代表色近似，所以细节会丢失。再给四种颜色约定编号：白0、红1、黄2、绿3。右边每个位置就能用有限的数值记录。这个把采样结果映射到有限等级的过程叫量化。颜色编号是本实验的表示办法，不是相机内部通用的调色板。'},
5:{given:'每个像素只能取白、红、黄、绿中的一种颜色。',tell:'先看一个像素要区分的状态：是四种颜色，不是整幅图的十二个位置。1bit只有0和1两种状态，不够；2bit有00、01、10、11，刚好够。现在请按白、红、黄、绿的顺序给它们编码。我们采用白00、红01、黄10、绿11；只要约定一致，也能采用其他对应关系。'},
6:{title:'怎样编码？位深度又是多少？',given:'颜色编号为0、1、2、3；采用固定长度的二进制码。',tell:'我来把每一个颜色编号替换为刚才的二进制码。注意每个格子都写满两位，0写成00，1写成01。现在这幅图已经能表示成二进制数据。将量化值变成码字叫编码；每个像素颜色用2bit描述，所以位深度是2，而不是全图的24bit。回头看：先采样，再量化，最后编码。'},
7:{tell:'左边3×4，右边6×8，两幅图显示在相近的区域。新图的采样位置更多，每格更小，花形可以表示得更细。我们只改变采样密度，四种颜色没有改变，所以每格仍然需要2bit。这里表示重新采集同一对象；把拍好的旧图直接放大，并不会自动得到新的真实细节。'},
9:{tell:'格子的位置没有改变，两幅图都是6×8。右边可以用更多颜色等级表示花瓣和花心，量化时有更多选择。先把“形状更细”与“颜色更丰富”分开。接下来判断：六种颜色，原来的2bit够不够？不要把颜色数直接当成位深度。'},
10:{tell:'第一轮建立了采样、量化、编码的流程。第二轮保持颜色数不变，提高采样分辨率，让形状表达更细；第三轮保持位置不变，增加可用颜色。请对照你填的词逐项核对。我们比较的是同一对象、相同显示大小；不把“像素多”当成任何照片都更清晰的保证。'},
14:{given:'R、G、B三个通道，各使用8bit。',tell:'每个通道8bit，可以取0到255，共256级。三个通道的等级独立组合，所以一共有256×256×256种组合，等于2的24次方。每个像素的总位数是8+8+8=24。这里说的是不带透明通道的24位RGB模型；软件中的“8位/通道”不要误读成整像素只有8位。'},
16:{tell:'先核对式子：500×333是像素数，乘24得到bit，除8得到499500B，再除1024约487.79KiB，按整数四舍五入约488KiB。我们算的是像素数据量。下一页再看原课的487KB文件属性，它只能帮助比较量级，不能用来证明精确相等。'},
18:{tell:'先指出破损区，再观察周围还留下哪些线索。模型可以利用周边内容和学到的图像规律推断缺损处，给这些位置补上颜色数据。右边是原课展示的修复结果。看起来合理，并不能证明补出的部分就是原来的真实细节。这也能解释同学为什么会遇到“修得不像”的情况。'},
19:{given:'温度、声波、海水压强、光照强度。',tell:'温度和声波的这两个例子主要看随时间的变化；海水压强随深度、光照强度随位置的例子主要看随空间的变化。我们用连续变化的物理量描述这些现象，称为模拟量。时间和空间是观察的自变量；关键在连续变化，不是所有例子都同时依赖时间和空间。'},
20:{given:'回看图像：有限的采样位置，有限的颜色等级。',tell:'采样把空间位置离散化，量化把每个位置的值映射到有限等级，再用码字表示。例如00、01、10、11是四种码字；每一位只有0或1，但多个位能够表示许多不同数值。数字量强调离散表示，不能理解成计算机只能存0和1两个数值。'},
21:{given:'自然界中的光 → ？ → 数字图像',tell:'现在请完整说出这条链：光经过采样、量化、编码，成为可以存储的数字图像。采样解决在哪些位置取样，量化解决怎样用有限等级表示，编码解决怎样写成码字。这就是信息数字化。分辨率和位深度决定本课简化模型里的像素数据量，也分别影响空间细节和颜色表达。'}
};
for(const q of qs)Object.assign(q,changes[q.id]||{},extra[q.id]);
function note(s,q,stage,talk){s.speakerNotes.textFrame.setText(`[问题 / 页面目的] ${q.title}\n[内部编号] Q${q.id}${stage==='question'?'—提问':stage==='answer'?'—揭示':'—'+stage}\n[教学意图] ${q.task}\n[教师逐字稿] ${talk}\n[预期学生反应] ${q.expected}\n[追问问题] ${q.follow}\n[下一问] ${q.transition}\n[课堂操作] ${stage==='question'?'停留20–40秒；先听预测或理由，再翻页。':'逐项指向证据；确认学生说出理由后继续。'} 本课全程可离线；软件截图已嵌入。\n[来源] PDF课堂逐字稿 ${q.src}；编号为重建导航，不是原课页面编号。\n[技术注解] ${q.caveat||''} ${q.id===2?'感光元件位于图像传感器；本图忽略滤色阵列、去马赛克等过程。':''}${q.id===9?'六色网格是教学示意重建，不能当作原课逐格精确矩阵；不据此考查编码。':''}${q.id===12?'1024B=1KiB。https://physics.nist.gov/cuu/Units/binary.html':''}${q.id===14?'RGB位数参考 https://helpx.adobe.com/photoshop/using/bit-depth.html':''}`);}
function register(s,q,stage,visible,talk){note(s,q,stage,talk);plan.push({slide:P.slides.items.indexOf(s)+1,q:'Q'+q.id,stage,title:q.title,visible,hidden:'教师逐字稿、预期反应、追问、技术注解、来源见Speaker Notes',source:q.src});}
function pair(q,base,add,desc,answerDesc){const a=frame(q.title);base(a);register(a,q,'question',desc,q.ask);const n=P.slides.items.length;const b=a.duplicate();b.moveTo(n);add(b);register(b,q,'answer',answerDesc,q.tell);pairs.push([n,n+1]);return b;}
function continuation(q,base,add,desc,talk){const a=base.duplicate();a.moveTo(P.slides.items.length-1);add(a);register(a,q,'evidence',desc,talk);return a;}
const cover=frame('图像编码');text(cover,'一朵花怎样变成二进制数据？',90,280,1100,110,57,C.ink,F.black,'center');flower(cover,560,435,120,160);cover.speakerNotes.textFrame.setText('[问题 / 页面目的] 从字符编码转入图像编码\n[内部编号] Q0\n[教师逐字稿] 前面我们讨论了字符怎样输入、保存和显示。今天换成照片：眼前一朵花和手机里保存的花有什么关系？先不急着回答，下一页看一张真实照片，把它不断放大。\n[来源] PDF逐字稿00:00:00–00:00:43；Snip1。花朵为参照Snip6绘制的可编辑示意。');plan.push({slide:1,q:'Q0',stage:'opening',title:'图像编码',visible:'课程标题与红花示意',source:'00:00–00:43；Snip1'});
for(const q of qs){let ans;
 switch(q.id){
 case 1:ans=pair(q,s=>{img(s,4,90,200,315,405);text(s,'预测：会出现什么？',90,610,450,45);},s=>{img(s,5,465,205,710,390);text(s,'像素：位图中的一个图像单元',485,615,690,45,32,C.accent,F.bold);},'原向日葵照片；预测任务','原照片不动，右侧加入真实软件放大证据与像素名称');break;
 case 2:ans=pair(q,s=>{flower(s,120,215,270,360);text(s,q.given,90,605,900,48);},s=>{text(s,'反射光 → 镜头 → 图像传感器',500,265,700,70,35,C.accent,F.bold);text(s,'用有限位置采集光的信息',500,395,680,70,35);text(s,'每个位置记录局部信息',500,505,680,70,35);},'原生红花思想实验对象','保持红花，揭示反射光与传感器关系');break;
 case 3:ans=pair(q,s=>{flower(s,115,220,270,360,true);text(s,'横向3个；纵向4个',90,610,480,44);},s=>{right(s,['3×4 = 12 个位置','3×4保留横向与纵向','采集样本：采样']);},'红花叠3×4网格，必要位置条件','原网格固定，揭示总数、分辨率与采样');break;
 case 4:ans=pair(q,s=>{flower(s,80,235,225,300,true);grid(s,four,430,235,75);text(s,'每格只留一种代表色',80,585,660,50);text(s,'怎样给颜色编号？',780,195,410,65,34);},s=>{grid(s,four,870,280,60,'number');text(s,'白0  红1  黄2  绿3',770,560,440,50,30,C.accent,F.bold);text(s,'有限等级表示：量化',770,615,440,45,30,C.accent,F.bold);},'原花、四彩图、编号问题','添加数字矩阵，颜色图与数字图并列');break;
 case 5:ans=pair(q,s=>{text(s,q.given,90,180,1100,55);table(s,[['颜色','白','红','黄','绿'],['二进制','？','？','？','？']],90,300,1100,180);},s=>{revealCells(s,[[1,1,'00'],[1,2,'01'],[1,3,'10'],[1,4,'11']]);text(s,'2 bit 有 4 种状态，刚好够用',180,550,950,80,43,C.accent,F.black,'center');},'四色空编码表；不显示位数','在同一表内填入2bit码字');break;
 case 6:ans=pair(q,s=>{grid(s,four,140,250,78,'number');text(s,'每格要写几个bit？',90,610,450,45);},s=>{grid(s,four,695,250,78,'binary');text(s,'编码：量化值 → 码字',630,180,560,50,33,C.accent,F.bold);text(s,'位深度：每像素 2 bit',630,610,560,45,33,C.accent,F.bold);},'颜色编号矩阵与位深度问题','添加同布局二进制矩阵与位深度');continuation(q,ans,s=>{text(s,'采样\n↓\n量化\n↓\n编码',440,275,190,275,32,C.accent,F.bold,'center');},'回顾三步骤','先指红花的网格，再指颜色编号，最后指二进制。三个动作分别是采样、量化、编码。原课由教师完成整幅矩阵替换，学生看对应关系；不把这一段说成学生独立编完了全图。');break;
 case 7:ans=pair(q,s=>{grid(s,four,140,235,88);text(s,'3×4 · 4色 · 2bit',90,615,520,45,32);},s=>{grid(s,fine,785,235,44);text(s,'6×8 · 4色 · 2bit',715,615,480,45,32,C.accent,F.bold);},'3×4基线；提出改进办法','右侧增加6×8；保持颜色和显示区域大小');{
 const rowq={...q,title:'第四行，怎样写成二进制？',ask:'从上往下数到第四行。先说六个格子的颜色，再按码表从左到右读出二进制。注意这次要读的是码字，不是颜色的编号。',tell:'这一行先是两个红色，再两个黄色，最后两个红色。红色01，黄色10，所以整行是01、01、10、10、01、01，共12bit。这次学生只读一行；其他各行按同一规则处理。'};
 pair(rowq,s=>{grid(s,fine,125,215,45);rect(s,125,350,270,45,'none',C.red,4);text(s,'白00  红01  黄10  绿11',490,240,700,60,32);text(s,'从左到右读第四行',490,340,700,60,35);},s=>{text(s,'01  01  10  10  01  01',490,455,710,80,40,C.accent,F.black);text(s,'6个像素，每个2bit，共12bit',490,560,710,60,32);},'第四行红框，四色码表','添加该行六个二进制码字');}break;
 case 8:ans=pair(q,s=>{text(s,'位图',120,215,380,65,40,C.ink,F.bold);text(s,'矢量图',735,215,380,65,40,C.ink,F.bold);text(s,'放大后，边缘会怎样？',100,600,1000,55,36);},s=>{grid(s,['00011','00110','01100','11000','10000'],145,315,42);line(s,780,515,990,305,C.accent,7);text(s,'像素点阵',380,465,230,60,32);text(s,'重新绘制边界',935,465,260,60,32);},'两类图名称与放大问题','揭示阶梯像素与矢量线边缘');break;
 case 9:ans=pair(q,s=>{grid(s,fine,145,230,45);text(s,'6×8 · 4种颜色',105,615,470,45,32);},s=>{grid(s,six,785,230,45);text(s,'6×8 · 6种颜色',725,615,470,45,32,C.accent,F.bold);},'6×8四色图；保持位置不变','新增六色示意，分辨率不变');{
 const depth={...q,title:'六种颜色，至少需要几个 bit？',ask:'现在不看花有多少个格子，只看一个格子有六种可能。先试两位，再试三位，哪一个最少而且够用？',tell:'2的2次方是4，小于6，不够；2的3次方是8，大于等于6，够用。最少3bit，可以选用其中6个码字，另外2个不用。这里不要说所有8个码字都必须出现在图像里。'};
 pair(depth,s=>{swatches(s,190,285,palette,80);text(s,'保持6×8个位置不变',100,190,950,55,32);},s=>{text(s,'2² = 4 < 6 ≤ 8 = 2³',240,445,850,80,48,C.accent,F.black);text(s,'最少3bit；8个码字中使用6个',240,560,900,65,34);},'六色样本与分辨率','揭示不等式和最少位数');}break;
 case 10:ans=pair(q,s=>{grid(s,four,90,220,35);grid(s,fine,295,220,18);grid(s,six,500,220,18);text(s,'编码三步：',90,435,280,55,34);text(s,'① ______  ② ______  ③ ______',355,435,850,55,34).name='flow-blanks';text(s,'分辨率提高，同样区域内的格子怎样变化？',90,540,1100,65,34);},s=>{replaceField(s,'flow-blanks','① 采样     ② 量化     ③ 编码');text(s,'格子更小，空间细节表达更细',90,610,1100,45,32,C.accent,F.bold);},'三轮缩略图、三步骤填空、分辨率问题','填三步骤，揭示分辨率结论');{
 const sum={...q,title:'颜色种类、位深度怎样联系？',ask:'继续填写：六种颜色比四种需要更多bit。现在把例子推广，n个bit最多有多少种不同码字？',tell:'位深度n最多表示2的n次方种颜色。想容纳更多颜色时，要看原来的位数是否已不够；只有超过原容量才必须增加位数。本实验从4到6种颜色，位深度从2到3。'};
 pair(sum,s=>{text(s,'本实验：4种颜色 → 6种颜色',90,215,1100,70,38);text(s,'位深度：______ → ______',90,340,1100,70,38).name='depth-blanks';text(s,'位深度为n，最多表示',90,465,570,70,38);text(s,'______',660,465,200,70,38).name='color-count-placeholder';text(s,'种颜色',880,465,260,70,38);},s=>{replaceField(s,'depth-blanks','位深度：2 bit → 3 bit',38);const field=s.shapes.items.find(sh=>sh.name==='color-count-placeholder');field.text='2ⁿ';field.text.style={typeface:F.black,fontSize:44,bold:true,color:C.accent,verticalAlignment:'middle',autoFit:'none',insets:{left:0,right:0,top:0,bottom:0}};},'颜色与位深度填空','相同位置补2、3与2的n次方');}break;
 case 11:ans=pair(q,s=>{table(s,[['分辨率','位深度','总bit'],['3×4','2','？'],['6×8','2','？'],['6×8','3','？']],90,220,1100,330);},s=>{revealCells(s,[[1,2,'3×4×2 = 24'],[2,2,'6×8×2 = 96'],[3,2,'6×8×3 = 144']]);text(s,'总bit = 像素总数 × 每像素的位数',130,585,1040,70,37,C.accent,F.bold,'center');},'三例条件与总bit空格','三例乘法和一般关系');break;
 case 12:ans=pair(q,s=>{text(s,'1 B = 8 bit',90,185,1100,60,35);text(s,'24 bit → ___ B    96 bit → ___ B    144 bit → ___ B',90,285,1100,70,32).name='byte-blanks';},s=>{replaceField(s,'byte-blanks','24 bit → 3 B       96 bit → 12 B       144 bit → 18 B',32);text(s,'像素数据量（B）= 横向×纵向×位深度÷8',90,410,1100,90,39,C.accent,F.bold);text(s,'B ÷1024 = KiB       KiB ÷1024 = MiB',90,555,1100,60,32);},'B与bit条件；三例空格','相同位置填字节数，推导B公式');break;
 case 13:ans=pair(q,s=>{table(s,[['图像','黑白','16色','256色'],['颜色数','2','16','256'],['位深度','？','？','？'],['数据量（B）','？','？','？']],90,225,1100,350);text(s,'三幅图的分辨率均为M×N',90,615,1100,45,32);},s=>{revealCells(s,[[2,1,'1'],[2,2,'4'],[2,3,'8'],[3,1,'M×N×1÷8'],[3,2,'M×N×4÷8'],[3,3,'M×N×8÷8']]);},'原课三类图的练习表','填位深度和未压缩像素数据量');break;
 case 14:{const rgbq={...q,title:'24位真彩色，最多有多少种颜色？',ask:'刚才已经算过黑白、16色和256色。现在直接给位深度24，请写出最多颜色数，再列M×N图像的像素数据量。先不用求出颜色数的十进制值。',tell:'24位最多表示2的24次方种颜色，数据量是M×N×24除8字节。计算方法完全相同。为什么照片常用24位？下一页看红、绿、蓝三个通道怎样组成它。'};pair(rgbq,s=>{table(s,[['分辨率','位深度','最多颜色数','像素数据量（B）'],['M×N','24','？','？']],90,300,1100,190);},s=>{revealCells(s,[[1,2,'2²⁴'],[1,3,'M×N×24÷8']]);},'24位与分辨率条件','填写颜色数与B算式');}
 ans=pair(q,s=>{['R','G','B'].forEach((v,i)=>{text(s,v,145+i*360,270,270,90,64,[palette[1],'#218029','#3157B7'][i],F.black,'center');text(s,'8 bit',145+i*360,375,270,65,38,C.ink,F.bold,'center')});},s=>{text(s,'每通道256级，取值0–255',140,470,1030,60,35,C.accent,F.bold,'center');text(s,'8×3 = 24 bit       256³ = 2²⁴ 种',140,565,1030,65,41,C.accent,F.black,'center');},'RGB各8bit；问组合','揭示256级、24bit与组合总数');break;
 case 15:ans=pair(q,s=>{img(s,20,80,235,540,390,{left:0,top:0.06,right:0.35,bottom:0});text(s,'R = 220    G = 95    B = 15',80,180,1090,50,34);text(s,'在计算机里怎样表示？',680,255,500,65,35);},s=>{['R  11011100','G  01011111','B  00001111'].forEach((t,i)=>text(s,t,680,360+i*75,500,60,39,i===0?C.accent:C.ink,F.bold));text(s,'24 bit = 3 bytes',680,610,500,45,34,C.accent,F.bold);},'Photoshop局部与RGB十进制值；裁去文件属性','增加三个8位码；保持软件证据不动');break;
 case 16:ans=pair(q,s=>{text(s,'500×333像素；每像素24bit',90,205,1100,65,38);text(s,'求未压缩像素数据量，以B和KiB表示。',90,305,1100,65,35);},s=>{text(s,'500 × 333 × 24 ÷ 8 = 499,500 B',90,410,1100,75,43,C.accent,F.bold);text(s,'499,500 ÷ 1024 ≈ 487.79 KiB',90,540,1100,75,43,C.accent,F.bold);},'独立计算条件；无属性截图','逐步列式与准确结果');{
 const s=frame('公式计算的是像素数据量');text(s,'计算：499,500 B ≈ 487.79 KiB',90,195,1100,60,36);img(s,20,90,290,600,325);text(s,'文件属性：487 KB',740,300,455,65,31);text(s,'文件还可能包含\n头部、调色板、行填充。',740,395,455,120,31);text(s,'像素数据量 ≠ 完整文件大小',740,565,455,65,31,C.accent,F.bold);register(s,{...q,title:'公式计算的是像素数据量'},'evidence','计算后才展示文件属性；区分像素与完整文件','原课把487KB作为公式验证。请注意，我们算出的487.79KiB不能四舍五入成487；截图也没有给出精确字节数。完整文件除了像素还可能有头部和填充。这个例子用于比较量级，课堂公式限定在未压缩像素数据量。');}break;
 case 17:ans=pair(q,s=>{img(s,4,115,200,300,410);text(s,'拍摄时提高分辨率，和拍好后放大一样吗？',90,615,1100,45,32);},s=>{right(s,['已有像素被放大','放大不增加原始细节','拍摄时适当提高分辨率']);},'回到原照片，比较两个动作','增加有限像素和拍摄建议');break;
 case 18:ans=pair(q,s=>{img(s,22,90,225,490,365,{left:0.02,top:0.02,right:0.16,bottom:0.05});text(s,'缺损处可以根据什么来推断？',90,610,1100,50,33);},s=>{img(s,25,700,225,410,365,{left:0.5,top:0.16,right:0.05,bottom:0});text(s,'修复结果（示例）',680,170,505,50,29.333,C.muted);},'破损照片与推断问题','保持破损照，添加原课修复结果');{
 const s=frame('用四步理解照片修复');['识别：区分破损与完好区域','匹配：利用周边内容和图像规律','补全：推断缺损处的像素内容','表示：得到颜色数据并编码保存'].forEach((v,i)=>text(s,v,110,205+i*97,1080,70,36,i===2?C.accent:C.ink,i===2?F.bold:F.regular));register(s,{...q,title:'用四步理解照片修复'},'evidence','四步课堂解释，采用准确的补全措辞','先找到损坏的位置，再利用完好区和图像规律推断缺的内容，给这些位置补上像素颜色并保存。原课把第三步称为“重新采样”，这里按它的教学意图说成“补全像素”。它不是相机重新看到过去，也不是所有AI算法都固定经过这四步。下一步回到花朵：自然光和计算机中的图像，表示方式有什么差别？');}break;
 case 19:ans=pair(q,s=>{table(s,[['例子','主要观察的变化'],['温度','？'],['声波','？'],['海水压强','？'],['光照强度','？']],90,215,1100,350);text(s,'哪些随时间？哪些随空间？',90,610,1100,50,34);},s=>{revealCells(s,[[1,1,'随时间'],[2,1,'随时间'],[3,1,'随深度（空间）'],[4,1,'随位置（空间）']]);},'四个原课例子与时间/空间分类','填写分类，不混淆自变量');{
 const s=frame('模拟量的关键：连续变化');line(s,140,530,780,530,C.ink,2);line(s,140,530,140,235,C.ink,2);text(s,'时间',680,555,130,50,30);text(s,'温度',85,175,200,50,30);let last;for(let i=0;i<60;i++){const x=155+i*10,y=460-1.6*i-38*Math.sin(i/10);if(last)line(s,last[0],last[1],x,y,C.cyan,4);last=[x,y];}text(s,'两次测量之间，\n仍有连续变化的温度。',830,280,370,150,32);text(s,'示意曲线',90,615,400,40,22,C.muted);register(s,{...q,title:'模拟量的关键：连续变化'},'evidence','有坐标含义的连续温度示意','假设这条线表示温度随时间的变化。我们即使没有在某个时刻测量，物理量也不会因为没人读数就不存在；这个模型描述连续变化。原课还举电流和电压承载模拟信号的例子。不要把“任意点有值”当作严格的数学连续性定义，本课只建立连续与离散表示的直观区别。');}break;
 case 20:ans=pair(q,s=>{text(s,'采样位置：',100,245,300,60,36);[0,1,2,3,4].forEach(i=>ellipse(s,425+i*140,265,14,14,C.ink));text(s,'可用颜色：',100,365,300,60,36);swatches(s,420,370);text(s,'这些结果怎样保存？',100,535,1050,60,36);},s=>{text(s,'有限位置',425,295,730,50,31,C.accent,F.bold);text(s,'有限等级',820,370,340,50,31,C.accent,F.bold);text(s,'00、01、10、11：离散码字',100,605,1080,50,34,C.accent,F.bold);},'有限采样位置与四色','在原证据上解释离散与码字');break;
 case 21:ans=pair(q,s=>{text(s,'自然界的光',90,280,340,75,42,C.ink,F.bold);text(s,'数字图像',880,280,300,75,42,C.ink,F.bold);text(s,'中间经历了哪三步？',390,405,700,70,38);},s=>{text(s,'采样 → 量化 → 编码',395,280,470,75,36,C.accent,F.bold);text(s,'信息数字化',415,540,560,80,48,C.accent,F.black);},'起点与终点，回顾三步骤','揭示信息数字化链');break;
 }
}
const hw=frame('课后练习');text(hw,'1. 一幅图只用6种颜色，最少需要几bit？',90,210,1100,80,35);text(hw,'2. 800×600的24位RGB图像，像素数据量是多少B？',90,330,1100,90,35);text(hw,'3. 把图像宽、高都放大2倍，就得到了新细节吗？',90,465,1100,90,35);text(hw,'说明理由；计算时写出单位。',90,610,1100,45,32,C.accent,F.bold);hw.speakerNotes.textFrame.setText('[问题 / 页面目的] 课后检查位深度、像素数据量和放大的边界\n[内部编号] Q22\n[教师逐字稿] 今天先完成这三题。第一题请写判断位数的不等式；第二题写清像素数、每像素位数和单位转换；第三题用“原始信息”解释。原课布置的是新发讲义第二页，但源资料没有那张讲义，这三题是重建版补充题，可直接抄在纸上作答。\n[参考答案] 1. 3bit，4<6≤8。2. 800×600×24÷8=1440000B。3. 没有；插值增加像素数量，不等于增加真实采集的细节。\n[来源] 原课作业位置00:43:32以后；题目为重建补充，不冒充原题。');plan.push({slide:P.slides.items.length,q:'Q22',stage:'exit',title:'课后练习',visible:'三道可直接完成的补充练习',source:'原课作业位置；题目重建补充'});
await fs.writeFile(path.join(root,'.codex-build/lesson-teaching-v4.json'),JSON.stringify(qs,null,2));
await fs.writeFile(path.join(root,'.codex-build/slide-plan-v4.json'),JSON.stringify({slides:plan,pairs},null,2));
await fs.writeFile(path.join(root,'pptx-slide-plan.md'),'# 图像编码课堂PPTX逐页计划\n\n所有问答页均调用原问题页的duplicate()后增加揭示内容；页码按最终PPTX顺序。教师讲述、追问、误解、技术边界和来源进入备注。\n\n|页|问题|阶段|学生此刻看到|证据来源|\n|---:|---|---|---|---|\n'+plan.map(r=>`|${r.slide}|${r.q} ${r.title}|${r.stage}|${r.visible}|${r.source}|`).join('\n')+'\n');
await (await PresentationFile.exportPptx(P)).save(path.join(root,'.codex-build/candidate-v4.pptx'));
console.log(JSON.stringify({slides:P.slides.items.length,pairs:pairs.length}));
