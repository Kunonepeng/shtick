// Native editable PPTX. Rebuild: node sources/build_deck.mjs <round-name>
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {Presentation, PresentationFile} from '@oai/artifact-tool';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SKILL = '/Users/chran/.codex/plugins/cache/openai-primary-runtime/presentations/26.921.10847/skills/presentations';
const PYTHON = '/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';
process.env.RUNTIME_NODE_MODULES ||= '/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const round = process.argv[2] || 'draft-1';
const build = path.join(ROOT, '.build', round);
await fs.mkdir(build, {recursive:true});
const P = Presentation.create({slideSize:{width:1280,height:720}});
const REG='Alibaba PuHuiTi 3.0 55 Regular', BLACK='Alibaba PuHuiTi 3.0 115 Black';
const C={violet:'#6251B1',accent:'#8C64E1',cyan:'#00B0F0',ink:'#262626',read:'#007C9B',red:'#FF0000',gray:'#808080'};
const plan=[], tableOwners=[];
const tree=JSON.parse(await fs.readFile(path.join(ROOT,'sources/knowledge-tree.json'),'utf8'));
const photo=JSON.parse(await fs.readFile(path.join(ROOT,'sources/photo-evidence.json'),'utf8')).evidence;
const [photoPNG,photoJPG]=photo['结果'];
const fmt=n=>n.toLocaleString('en-US');
function findSlide(q,stage){return P.slides.items[plan.findIndex(r=>r.q==='Q'+q && r.stage===stage)];}
const questions=[
 ['文件变小，是不是删掉了内容？','文件变小，是不是删掉了内容？'],
 ['连续重复的颜色，怎样少写一些？','连续重复的颜色，怎样少写一些？'],
 ['少写以后，怎样证明一个也没丢？','少写以后，怎样证明一个也没丢？'],
 ['同一规则，为什么有时反而变大？','同一规则，为什么有时反而变大？'],
 ['相邻值接近，怎样完整记录？','相邻值不相同，还能利用它们的关系吗？'],
 ['只留近似值，还能找回原数吗？','只留近似值，还能找回原数吗？'],
 ['看起来差不多，能否叫无损？','看起来差不多，能否叫无损？'],
 ['同一种误差，哪些任务能接受？','同一种误差，哪些任务能接受？'],
 ['看扩展名，就能判定压缩方式吗？','看扩展名，就能判定压缩方式吗？'],
 ['大小和信息要求，怎样同时满足？','怎样在大小限制和信息要求之间选方案？']
];
const sources={3:'https://datatracker.ietf.org/doc/rfc1951/',4:'https://datatracker.ietf.org/doc/rfc1951/',5:'https://www.w3.org/TR/png-3/',7:'https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html\nhttps://www.w3.org/Graphics/JPEG/itu-t81.pdf',9:'https://helpx.adobe.com/photoshop/desktop/save-and-export/export-files-to-different-formats/file-compression-in-photoshop.html\nhttps://www.mpeg.org/standards/MPEG-1/\nhttps://www.iis.fraunhofer.de/content/dam/iis/de/doc/ame/conference/AES-17-Conference_mp3-and-AAC-explained_AES17.pdf'};
function box(s,name,x,y,w,h,fill='none',stroke='none',line=0){return s.shapes.add({geometry:'rect',name,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:line}});}
function text(s,name,value,x,y,w,h,pt=22,color='#000000',strong=false,align='left'){
 const t=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 t.text=value;t.text.style={typeface:strong?BLACK:REG,fontSize:pt*4/3,color,alignment:align,verticalAlignment:'middle',autoFit:'none',wrap:'square',lineSpacing:1.3,insets:{top:0,right:0,bottom:0,left:0}};return t;
}
function base(title){const s=P.slides.add();s.background.fill='#FFFFFF';box(s,'top-rail',0,0,1280,32/3,C.violet);box(s,'bottom-rail',0,720-32/3,1280,32/3,C.violet);text(s,'question-title',title,63.84,63.84,1152,73.92,36,C.ink,true);return s;}
function notes(s,q,stage,transcript,teacher=''){
 const full=q?questions[q-1][1]:stage;
 s.speakerNotes.textFrame.setText(`[问题 / 页面目的] ${full}\n[内部编号] ${q?'Q'+q:'收束'} · ${stage}\n[教学意图] ${stage==='question'?'先收预测与方法，再揭示证据。':'让学生用本页证据修正判断；等待学生说出理由。'}\n[教师逐字稿] ${transcript}\n[教师提示] ${teacher}\n[课堂控制] 本页学生可见内容只限当前阶段。演示失败20秒换本页静态证据。45分钟：Q1 3、Q2 6、Q3 4、Q4 4、Q5 5、Q6 5、Q7 5、Q8 4、Q9 4、Q10 5分钟。\n[来源] course-design.qmd；demos/compression_lab.py；${sources[q]||'本课明确约定的教学模型／题目条件'}`);
}
function record(s,q,stage,visible,hidden,evidence){plan.push({slide:plan.length+1,q:q?'Q'+q:'收束',stage,visible,hidden,evidence});return s;}
function question(q,transcript,visible,evidence=''){let s=base(questions[q-1][0]);notes(s,q,'question',transcript);return record(s,q,'question',visible,'答案、结论、计算结果与纠错提示留待复制揭示页及备注',evidence);}
function reveal(source,q,stage,transcript,visible,hidden='',evidence=''){const s=source.duplicate();notes(s,q,stage,transcript,hidden);return record(s,q,stage,visible,hidden,evidence);}
async function img(s,name,file,x,y,w,h){s.images.add({name,blob:new Uint8Array(await fs.readFile(path.join(ROOT,'assets/evidence',file))),contentType:file.endsWith('.jpg')?'image/jpeg':'image/png',alt:name,fit:'contain',position:{left:x,top:y,width:w,height:h}});}
function line(s,values,y,label=''){
 if(label)text(s,'row-label-'+y,label,64,y,110,52);
 values.forEach((v,i)=>{
  const b=box(s,'value-'+y+'-'+i,180+i*63,y,58,52,['#D2232D','#14875A','#2355C3'][v-1]||'#eeeeee');
  b.text=['','红','绿','蓝'][v]||String(v);
  b.text.style={typeface:REG,fontSize:22*4/3,color:'#FFFFFF',alignment:'center',verticalAlignment:'middle',autoFit:'none',insets:{top:0,right:0,bottom:0,left:0}};
 });
}
function colors(s,values,y,label='',focus=-1){line(s,values,y,label);if(focus>=0)box(s,'focus-color',178+focus*63,y-2,62,56,'none',C.red,4);}
function gray(s,values,y){values.forEach((v,i)=>{const x=64+i*141;const h=v.toString(16).padStart(2,'0');box(s,'gray-'+y+'-'+i,x,y,125,64,'#'+h+h+h);text(s,'gray-label-'+y+'-'+i,''+v,x,y+74,125,45,22,'#000000',false,'center');});}
function table(s,name,values,x,y,w,h,widths){const t=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,values,columnWidths:widths});t.borders.assign({fill:'#D6D1E6',width:1,style:'solid'});for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){let z=t.getCell(r,c);z.fill=r===0?'#F0EDF7':'#FFFFFF';z.text.style={typeface:r===0?BLACK:REG,fontSize:22*4/3,color:'#000000',alignment:'left',verticalAlignment:'middle',autoFit:'none',wrap:'square',insets:{left:8,right:8,top:6,bottom:6}};}tableOwners.push(plan.length);return t;}
let previousTree;
function knowledge(stage){
 const cp=tree.checkpoints[stage];
 const page=previousTree?previousTree.duplicate():base(cp.title);
 if(previousTree)page.moveTo(P.slides.items.length-1);
 page.shapes.items.find(t=>t.name==='question-title').text=cp.title;
 if(!previousTree){
  text(page,'tree-root',tree.root,64,351,190,84,28,C.ink,true);
  box(page,'tree-trunk-horizontal',254,392,55,2,C.accent);
  box(page,'tree-trunk',307,202,2,375,C.accent);
  for(const b of tree.branches){
   box(page,'tree-branch-link-'+b.id,309,b.y+18,29,2,C.accent);
   text(page,'tree-branch-'+b.id,b.label,340,b.y,181,36,24,C.ink,true);
  }
 }
 // Duplicate the last tree: learned labels and connectors remain fixed.
 for(const shape of [...page.shapes.items]){
  if(shape.name.startsWith('tree-focus-')||shape.name==='tree-summary')shape.delete();
 }
 for(const leaf of tree.leaves.filter(n=>n.stage===stage)){
  text(page,'tree-leaf-'+leaf.id,leaf.text,630,leaf.y,584,36,22,C.ink);
  box(page,'tree-leaf-link-'+leaf.id,592,leaf.y+18,26,2,C.cyan);
 }
 for(const b of tree.branches){
  const known=tree.leaves.filter(n=>n.branch===b.id && n.stage<=stage);
  if(known.length && !page.shapes.items.some(n=>n.name==='tree-stem-'+b.id)){
   box(page,'tree-stem-'+b.id,590,Math.min(b.y+18,known[0].y+18),2,Math.max(b.y+18,known.at(-1).y+18)-Math.min(b.y+18,known[0].y+18)+2,C.cyan);
   box(page,'tree-parent-link-'+b.id,523,b.y+18,69,2,C.cyan);
  }else if(known.length){
   const t=page.shapes.items.find(n=>n.name==='tree-stem-'+b.id);
   t.position={left:590,top:Math.min(b.y+18,known[0].y+18),width:2,height:Math.max(b.y+18,known.at(-1).y+18)-Math.min(b.y+18,known[0].y+18)+2};
  }
 }
 if(stage>0)for(const b of tree.branches){
  const fresh=tree.leaves.filter(n=>n.stage===stage && n.branch===b.id);
  if(fresh.length)box(page,'tree-focus-'+b.id,623,fresh[0].y+2,591,fresh.at(-1).y-fresh[0].y+35,'none',C.red,3);
 }
 const summaries=['学到哪里，\n就补到哪里。','无损不保证\n每份数据\n都变小。','看起来相似，\n不能证明\n原值相同。','媒体接受有损，\n需要质量达标。','大小和信息\n两项要求\n都要满足。'];
 text(page,'tree-summary',summaries[stage],64,510,240,140,22,C.read,true);
 notes(page,0,cp.title,`${cp.prompt}先留八秒请一位同学归纳，再用红框核对刚学到的节点。${cp.summary}四条主枝的位置一直不动。已经学过的节点保留，尚未建立的结论继续留空。今天学到的不只是几个格式名，要能说明怎样省空间、怎样验证还原，以及怎样检查用途。`, `知识树阶段${stage}；${cp.after}之后显示。本页不提前公布后续叶节点。阶段0用20秒；阶段1至3各30秒；终图30秒。全部计入原有Q1、Q4、Q7、Q9、Q10预算。红框仅标本次新学节点。具体格式的用途与边界回看Q9表。`);
 record(page,0,'knowledge-'+stage,stage?'已学知识树＋红框新节点＋阶段结论':'数据压缩根节点与四条中性问题主枝','未学叶节点不显示；详细边界与组织提问在备注',`knowledge-tree.json；${cp.after}`);
 previousTree=page;return page;
}
const col=[...Array(8).fill(1),...Array(5).fill(2),...Array(3).fill(3)],alt=Array.from({length:16},(_,i)=>i%2+1),gv=[120,121,122,121,120,120,121,122];

let s=base('数据压缩入门');text(s,'cover-title','文件变小，\n信息去哪了？',64,196,1152,224,60,C.ink,true);text(s,'cover-subtitle','Data compression 101',64,457,1120,100,37,C.gray);notes(s,0,'开场：从文件大小提出问题','前面算过数据需要多少空间。今天先看一个反常现象：文件一下小了很多，图却还能还原。请保留你的第一反应，后面我们用数据来检查。先不要背定义。');record(s,0,'opening','课题与主问题','学习目标及流程留在教师备注','原生文字');

knowledge(0);

s=question(1,'同一幅64×64颜色图，A有4096个bytes，B是用A编码得到的，只有38个bytes。先写一个猜测：变小以后，哪些内容可能发生变化？说出你想检查什么。先不给答案。','原图、A/B大小、预测任务','D1课前实测');await img(s,'原颜色图','opening-original.png',64,208,320,320);text(s,'a-size','A：4096 B',450,231,650,64,32,C.ink,true);text(s,'b-size','B：38 B',450,352,650,64,32,C.ink,true);text(s,'origin','B由A编码得到。先预测，再检查。',450,485,740,90);s=reveal(s,1,'evidence','现在把B读回图像。你看到少了哪一块吗？看上去一样，还不够证明每一个数都相同。我们先找一种能变短又能画回的规则，第三问再检查所有bytes。','加入解压还原图；暂不显示相等结果','64×64与码表预先约定；这是颜色编号数据，不冒充PNG。38B是随包记录，现场大小若不同以实际输出为准。','D1');await img(s,'解压得到的图','opening-restored.png',864,208,320,320);text(s,'restored-label','从B读回的图',864,554,330,60);

s=question(2,'这次只看16个颜色。怎样少写一些，又让同桌恢复原来的顺序和数量？发送者看折叠卡，接收者先不看原串。给你们60秒写规则与短消息，30秒画回，再展开卡核对。','原串与顺序/数量约束','A1私有颜色卡');colors(s,col,244);text(s,'a1-task','用短消息传给同桌：顺序不变，内容不漏。',64,414,1148,85);s=reveal(s,2,'answer','先听你们的规则。红绿蓝三个字能找回多少个吗？这一种保留了颜色、连续次数和段的顺序。红8代表连续8个红，不是全图所有红的总数。它把重复展开的依据留了下来。','揭示红8绿5蓝3与RLE','私有变体只给发送者，接收者先画回再展开原卡。写8红5绿3蓝也可，不因格式不同判错。','D2／A1');text(s,'rle-result','红 8     绿 5     蓝 3',64,528,1148,72,32,C.read,true);text(s,'rle-name','游程编码  Run-Length Encoding（RLE）',64,606,1148,48);

s=question(3,'接收者说已经恢复了，你准备怎样检查？先提出方法，再动手对比下面两行。不要只说长度一样。','原串与待检查串，无错误标记','D1／逐位置检验');colors(s,col,234,'原串');const faulty=col.slice();faulty[8]=3;colors(s,faulty,372,'待查');text(s,'check-task','提出检验方法，再检查这份还原结果。',64,520,1148,70);s=reveal(s,3,'focus','把两行按位置对齐。第9个位置原来是绿，待查却是蓝。两串都是16格，也可能有一个数不同。现在回到开场，比较的应是解压结果与原输入。','只标第9处差异','比较对象：还原与原始输入；不是比较原文件与压缩文件。','第9位置');box(s,'first-difference',178+8*63,370,62,56,'none',C.red,4);s=reveal(s,3,'answer','程序逐byte比较，得到True。解压得到4096个bytes，每个位置与输入相同。能完全恢复原始数据，才叫无损。记住检验对象，下一问我们试同一个规则能否一直省空间。','加入bytes一致与无损定义','D1只在本阶段调用opening(True)。','D1精确检查');text(s,'byte-comparison','解压结果 == 原始输入  →  True',64,598,1148,48,24,C.read,true);

s=question(4,'两串都是16个颜色。按连续段存编号和次数：编号1B、次数1B。先投票，再分工数两串各有几段，算编码后的数据量。不要把红绿交替改写为红8绿8。','两串、相同RLE规则','D2反例');colors(s,col,225,'A');colors(s,alt,342,'B');text(s,'rle-rule','每组：颜色编号1 B + 连续次数1 B',64,480,1148,70);s=reveal(s,4,'answer','A有三段，3×2等于6B。B有十六段，每段只有一个颜色，16×2等于32B。它仍能准确恢复，却更大了。无损说的是可恢复，不是保证变小。','加入6B/32B反例','只比payload；双方共享码表。256个相同色需拆255+1，不能让次数溢出。ZIP压JPEG效果需实测。','D2');text(s,'counts','A：16 B → 6 B       B：16 B → 32 B',64,590,1150,64,28,C.read,true);

knowledge(1);

s=question(5,'这一行灰度几乎一样，数却不完全相同。要求完整恢复，除了逐个写8bit，还能怎样记录？先想规则。必要时从第一个120出发，问下一格比它多多少。','八个灰度格、原值、8bit条件','D3／A2');gray(s,gv,219);text(s,'gray-given','灰度0–255，每项8 bit；必须完整恢复。',64,411,1150,75);s=reveal(s,5,'answer','给首值120，前三个差值已经列出。请填末四个，再只看首值与差值读回末三个数。负号不能丢，每次加在刚读回的前值上。变化都还在，才能恢复原来每一项。','首值与完整差值','A2正常版：首值及前三个差值已给，末四个学生填；迟到版仅减少一空。先活动后揭示。','D3');text(s,'deltas','起点120；差值：+1，+1，−1，−1，0，+1，+1',64,527,1150,60,24,C.read,true);s=reveal(s,5,'evidence','这一串差值只有三种，我们另约定−1为00、0为01、+1为10。首值8bit加七个2bit差值，共22bit，装入完整bytes是3B，末尾补2bit。差值项数没有减少，变短来自更合适的编码。','22bit/3B计算和规则边界','长度、模式和码表未计入。一般图像有大差值，不能套三种值码表；PNG可逆滤波仍输出同数量bytes，后续压缩另处理。','D3 payload');text(s,'delta-size','8 + 7 × 2 = 22 bit → 3 B（补2 bit）',64,603,1150,48,24,C.ink,true);

s=question(6,'现在换个规则：归到最近的4的倍数，中点向上取，最高只到252。看到120这一档，能确定原数吗？请写至少两个可能原数，再填A2下半表。','规则、116/120/124数轴，无箭头答案','D4／A2');text(s,'quant-rule','归到最近的4的倍数；中点向上取。',64,205,1150,80);[116,120,124].forEach((n,i)=>text(s,'axis-'+n,''+n,200+i*360,358,160,70,32,C.ink,true,'center'));box(s,'axis-line',180,455,880,2,'#808080');text(s,'quant-ask','看到代表值120，原来可能是多少？',64,523,1150,80);s=reveal(s,6,'focus','120会恢复为120，121也恢复为120。你如果再加1，就会把原来本来是120的情况选错。没有保存区分它们的依据，不能唯一倒回原数。','合流证据120/121→120','119也映射到120。课堂模型不是JPEG，也不是初始数字化过程。','两个输入同一结果');text(s,'many-to-one','120 → 120       121 → 120',64,606,1150,48,28,C.read,true);
s=reveal(s,6,'answer','64个等级只需6bit编号。八格64bit变成48bit，即6B；但变小同时丢失了区分。某些值恰好不变，不代表这种规则能保证精确恢复。这是有损的例子。','48bit/6B与有损结论','还原八项为120,120,124,120,120,120,120,124；不能用明暗看不出代替数字证据。','D4');text(s,'lossy-size','8 × 6 = 48 bit = 6 B；不能保证完整恢复',64,661,1150,36,22,C.ink);

s=question(7,'两图均来自所提供《蒙娜丽莎》JPEG本次解码得到的RGB，尺寸不变。先按正常大小看A和B，说出你能观察到的变化。再判断：看不出变化，足以证明每个像素相同吗？收判断后才查数据。','中性A/B绘画图像；同一输入、同尺寸','D5用户提供图像；本次解码RGB起点');
await img(s,'A图','painting-source.png',128,208,306,350);await img(s,'B图','painting-quality80.jpg',742,208,306,350);
text(s,'image-a','A',128,166,306,40,24,C.ink,true);text(s,'image-b','B',742,166,306,40,24,C.ink,true);
text(s,'painting-baseline','两图均为1020 × 1500像素；以所提供JPEG本次解码的RGB为起点。',64,575,1150,77);
s=reveal(s,7,'answer',`A保存为PNG，回读像素与本次输入一致。B用JPEG quality80保存，有${fmt(photoJPG['变化像素'])}个像素改变。你能否看出差别，都不能代替逐像素检查。输入文件本身已是JPEG，我们没有更早的原图，不能宣称把它恢复成无损原作。`,'格式、逐像素比较结果','保留原文件不改动；quality80不是80%质量。比较目标是本次输入RGB，不是未知的相机或艺术品数字母版。','photo-evidence.json');
s.shapes.items.find(x=>x.name==='painting-baseline').position={left:64,top:564,width:1150,height:43};
s.shapes.items.find(x=>x.name==='painting-baseline').text='比较本次输入RGB；不证明更早的原图无损。';
text(s,'format-a','PNG：本次回读像素一致',128,611,520,40,22,C.read);
text(s,'format-b',`JPEG：${fmt(photoJPG['变化像素'])}个像素改变`,742,611,472,40,22,C.read);
s=reveal(s,7,'focus','同一坐标的脸部细节，最近邻放大4倍，没有锐化。先描述观察到的纹理变化。看不出也可以，以刚才的像素检验为准。若任务只是浏览人物和背景，近似可能合用；若研究细微纹理，就要重新检查要求。','同坐标192×128区域放大4倍','裁切(x,y,w,h)=(368,310,192,128)。quality20仅作为可选明显对照，不能强迫学生在q80中看出指定差异。','D5真实图像裁切');
box(s,'painting-crop-overlay',63,203,1152,408,'#FFFFFF');
await img(s,'A同坐标细节','painting-crop-source.png',64,230,540,324);await img(s,'B同坐标细节','painting-crop-quality80.png',674,230,540,324);
text(s,'painting-crop-caption','同一192 × 128像素区域，最近邻放大4倍',64,563,1150,44);
s=reveal(s,7,'evidence',`本次绘画图像PNG${fmt(photoPNG['完整文件B'])}B，JPEG${fmt(photoJPG['完整文件B'])}B，JPEG较小。换成程序绘制的测试图，PNG4441B，JPEG10766B，大小关系反过来了。两组各自从同一RGB编码，尺寸均不变；不能只靠无损或有损标签判断大小。`,'绘画与测试图两组完整文件大小','原提供JPEG为212536B，不与重编码文件混作同一编码起点的未压缩大小；本次RGB4590000B。两组内同尺寸、直接编码、q80/subsampling0。','D5图像两种数据');
box(s,'painting-size-overlay',63,166,1152,444,'#FFFFFF');
for(const shape of [...s.shapes.items])if(['format-a','format-b'].includes(shape.name))shape.delete();
text(s,'painting-size-heading','这份绘画图像（1020 × 1500）',64,174,1150,45,24,C.ink,true);
text(s,'painting-size-result',`PNG ${fmt(photoPNG['完整文件B'])} B    JPEG ${fmt(photoJPG['完整文件B'])} B`,64,230,1150,55,26,C.read,true);
await img(s,'程序绘制的测试图','test-source.png',64,325,384,216);
text(s,'test-size-heading','程序绘制的测试图（384 × 216）',510,326,704,64,24,C.ink,true);
text(s,'test-size-result','PNG 4,441 B\nJPEG 10,766 B',510,408,704,120,26,C.ink,true);
text(s,'painting-size-conclusion','有损／无损说明能否精确恢复，不能替我们排文件大小。',64,572,1150,70,22,C.read);

knowledge(2);

s=question(8,'先不要报格式名，判断每份材料要保留什么。通知少了一个五，程序少了等号，照片少量像素改变。三件事都能接受吗？同桌写一条理由。程序用60测试。','三个用途及给定变化','A3');table(s,'uses',[['任务','变化'],['通知原文','本周五交作业 → 本周交作业'],['源程序','score >= 60 → score > 60；输入60'],['照片浏览副本','像素略变，人物与活动内容仍清楚']],64,200,1150,323,[280,870]);s=reveal(s,8,'answer','60大于等于60成立，60大于60不成立。符号很少，功能却变了。通知原文与源程序本体都要求无损。照片作为题中浏览副本，可以在质量达标时用有损方式。若要读角落小字，重新检查。','文本/程序必须无损；媒体按用途判断','不把删改内容称为原文件的合格压缩。测量和编辑母版可能同样要求无损。','程序60反例');text(s,'use-answer','文本文档／程序必须无损；媒体要检查用途与质量。',64,573,1150,90,24,C.read,true);

s=question(9,'同学说这几个名字都是有损，图片不能无损。先找一个反例，再改他的说法。配置卡是依据技术文档做的规则表，软件保存设置可能不同。不能只看后缀。','错误说法、PNG已知证据、TIFF中性配置卡','Adobe技术文档；非软件截图');text(s,'format-claim','“JPG、TIF、MP3、MPEG都是有损；图片不能无损。”',64,191,1150,95);table(s,'tiff-config',[['TIFF配置卡','可选方式'],['编码设置','未压缩／LZW无损／JPEG有损']],64,346,1150,156,[280,870]);text(s,'png-recall','已有证据：本课PNG回读像素一致。',64,556,1150,80);
s=reveal(s,9,'answer','PNG已经推翻图片不能无损。TIFF同一后缀可以采用不同方式，所以需要看保存配置。常见照片JPEG通常有损；不能把一个文件格式名字等同唯一压缩算法。','TIFF需看编码；PNG反例','JPEG标准还包含无损模式，本课不要求学生记标准编号。','Q9');text(s,'format-fix','TIF需看编码；图片也能无损压缩。',64,643,1150,42,24,C.read,true);
s=reveal(s,9,'evidence','最后给名字放回常见用途：JPG图像通常有损，TIF图像看设置，MP3音频有损，MPEG视频相关标准常见用途采用有损编码。MPEG是一组标准，MP3是Audio Layer III，不是MPEG-3。长技术边界留在教师材料。','格式/用途/边界速查表','本页替换配置卡区域，不增加新问题。MP4后缀也不能直接等同某一种算法。','Q9常见格式');box(s,'format-overlay',64,180,1150,502,'#FFFFFF');table(s,'format-summary',[['名称','常见用途','本课保留的边界'],['JPG/JPEG','图像','常见照片保存通常有损'],['TIF/TIFF','图像','需看所用编码方式'],['MP3','音频','常见有损音频编码'],['MPEG','视频相关标准','常见视频用途采用有损编码']],64,192,1150,422,[240,310,600]);text(s,'format-key','先看用途与保存方式，再判断。',64,636,1150,50,24,C.read,true);

knowledge(3);

s=question(10,'传送限额100KiB，下面是题目给定的候选结果，不是现场测量。先个人选，再同桌分两列检查：大小是否过关，信息是否过关。请说明另一方案为什么不合格。给90秒。','100KiB限制与候选结果；不显示选项答案','A3给定案例');text(s,'limit','限额100 KiB；1 KiB = 1024 B。以下为题目给定结果。',64,173,1150,65);table(s,'choices',[['任务（原120 KiB）','方案A','方案B'],['源程序，bytes需完整恢复','无损80 KiB\n解压bytes一致','删改内容50 KiB\n不能恢复原bytes'],['照片浏览，人物主题清楚','无损110 KiB\n回读像素一致','有损70 KiB\n人物主题仍清楚']],64,280,1150,278,[360,395,395]);text(s,'decision-prompt','逐份选方案，并说明另一种为什么不合格。',64,598,1150,70);
s=reveal(s,10,'answer','程序A同时满足两关，B虽小但不能交回原bytes。照片B同时满足两关，A虽无损却超限。照片B的合格限于题中浏览用途。回看开场猜测，请把文件变小一定删内容改成更准确的一句。','加入源程序A／照片B的双条件选择','300秒：30读题、90判断、60报告、30回扣、30定义、40出口、20收取。下两页收束只用剩余90秒；出口答案页课后显示。','Q10');text(s,'choice-answer','源程序选A；照片浏览副本选B。两项要求都要满足。',64,660,1150,37,22,C.read);

knowledge(4);

s=base('用两句话检查自己的判断');text(s,'exit-task','独立写40秒：',64,202,1150,64,24,C.ink,true);text(s,'exit-one','无损判断要比较 ______ 与 ______。',64,338,1150,90,28);text(s,'exit-two','照片看不出变化仍可能有损，因为 ______。',64,478,1150,90,28);notes(s,10,'出口检查','现在自己写两句话，不跟同桌讨论。第一句要写出两个比较对象，第二句要区分人的感受与数据相等。40秒后收取，抽看三份。不要现在翻到参考答案页，避免学生照抄。');record(s,10,'exit','两句空栏，独立书写','参考答案下一复制页，收取前不翻','A3出口');
s=reveal(s,10,'exit-answer','这一页只在收取后或课后核对。比较解压结果与原始输入；没有看出变化只说明感知接近，不能证明原值一致。若学生只写原图与压缩图，回到Q3要求说明还原对象；若仍凭肉眼判无损，回到Q6两个原数映到120。','出口参考答案','收取前不投影。作为课后反馈，可直接结束在上一页。','A3评价');text(s,'exit-answer-one','解压结果 与 原始输入',64,420,1150,55,24,C.read,true);text(s,'exit-answer-two','感知相似，不能证明每个原值都相同。',64,602,1150,60,24,C.read,true);

// Review-1 repairs: reserve the bottom content margin without shrinking text.
const positions={
 'origin':[450,598,740,55], 'restored-label':[864,544,330,50],
 'axis-116':[200,326,160,70], 'axis-120':[560,326,160,70], 'axis-124':[920,326,160,70],
 'axis-line':[180,420,880,2], 'quant-ask':[64,458,1150,66],
 'many-to-one':[64,544,1150,50], 'lossy-size':[64,608,1150,48],
 'same-size':[64,565,1150,43], 'format-a':[64,611,540,43], 'format-b':[674,611,540,43],
 'crop-overlay':[63,235,1152,376], 'crop-caption':[64,555,1150,50],
 'use-answer':[64,555,1150,96], 'format-fix':[64,607,1150,46],
 'format-overlay':[63,180,1152,475], 'format-key':[64,607,1150,46],
 'decision-prompt':[64,562,1150,44], 'choice-answer':[64,611,1150,42],
 'exit-answer-one':[64,428,1150,52], 'exit-answer-two':[64,594,1150,58]
};
for(const slide of P.slides.items){
 for(const shape of slide.shapes.items){
  const r=positions[shape.name];if(r)shape.position={left:r[0],top:r[1],width:r[2],height:r[3]};
 }
}
// One phrase per intentional line: avoid an orphan Chinese character in Q10.
for(const slide of P.slides.items)for(const t of slide.tables.items){
 if(t.getCell(0,0).value==='任务（原120 KiB）')t.getCell(1,0).value='源程序\nbytes须完整恢复';
}
// Re-check what students are looking at when the equality result is revealed.
const recovery=findSlide(3,'answer');
recovery.shapes.items.find(x=>x.name==='value-372-8').fill='#14875A';
recovery.shapes.items.find(x=>x.name==='value-372-8').text='绿';
box(recovery,'recovery-caption-overlay',63,500,1152,154,'#FFFFFF');
text(recovery,'recovery-conclusion','16项逐值一致。\n开场：4096 bytes还原一致（True）。\n无损：解压后可完全恢复原始数据。',64,522,1150,130,24,C.read);
notes(recovery,3,'answer','先修正待查串的第9格，再逐位置核对，现在这16项一致。回到开场，用程序比较解压所得4096个bytes与原输入，得到True。这两个检验都比较还原结果和输入。原数据能完全恢复，才叫无损；不能仅看图像外观或文件长度。','上页故障串已修正；本页的True明确属于开场4096B的实测。');
text(findSlide(5,'evidence'),'delta-code-table','本串码表：−1 = 00；0 = 01；+1 = 10',64,478,1150,44,22,C.ink);
await fs.writeFile(path.join(ROOT,'sources/slide-plan.json'),JSON.stringify(plan,null,2));
await fs.writeFile(path.join(build,'table-owners.json'),JSON.stringify([...new Set(tableOwners)]));
const candidate=path.join(build,'candidate.pptx');
await (await PresentationFile.exportPptx(P)).save(candidate);
// Export source text and notes once, shared by the Reveal reference builder.
await fs.writeFile(path.join(build,'presentation.json'),JSON.stringify(P.toProto(),null,2));
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')));
const final=path.join(ROOT,'validation',round,'data-compression.pptx');
await fs.mkdir(path.dirname(final),{recursive:true});
await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath:final,pythonExecutable:PYTHON,
 integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...[...new Set(tableOwners)].flatMap(n=>['--require-native-table-slide',String(n)])],
 requiredNativeTableOwnerSlides:[...new Set(tableOwners)],fontPolicy:{basis:'user_request',families:[REG,BLACK]},verifyArtifactToolImport:true,
 receiptPath:path.join(build,'finalization-receipt.json')});
console.log(JSON.stringify({slides:P.slides.items.length,output:final,tables:[...new Set(tableOwners)]}));
