import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const modules=process.env.ARTIFACT_MODULES ?? path.join(root,'.codex-build/node_modules');
const require=createRequire(path.join(modules,'_resolve.cjs'));
const {Presentation,PresentationFile}=await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const design=await fs.readFile(path.join(root,'course-design.qmd'),'utf8');
const match=design.match(/<!-- panda-v4-model:start -->\s*```json\s*([\s\S]*?)```\s*<!-- panda-v4-model:end -->/);
if(!match) throw new Error('Missing authoritative lesson model');
const model=JSON.parse(match[1]);
const out=path.join(root,'.codex-build/panda-v4'); await fs.mkdir(out,{recursive:true});
const P=Presentation.create({slideSize:{width:1280,height:720}});
const regular='Alibaba PuHuiTi 3.0 55 Regular',black='Alibaba PuHuiTi 3.0 115 Black';
function rect(s,name,x,y,w,h,fill='none',stroke='none',width=0){return s.shapes.add({geometry:'rect',name,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width,style:'solid'}});}
function text(s,name,value,x,y,w,h,size=29.333333,font=regular,color='#262626'){
 const sh=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=value;sh.text.style={typeface:font,fontSize:size,bold:font===black,color,verticalAlignment:'middle',alignment:'left',wrap:'square',autoFit:'none',insets:{left:0,right:0,top:0,bottom:0}};return sh;
}
function frame(title){const s=P.slides.add();s.background.fill='#FFFFFF';rect(s,'top-rail',0,0,1280,10.666667,'#6251B1');rect(s,'bottom-rail',0,709.333333,1280,10.666667,'#6251B1');text(s,'title',title,63.84,63.84,1152,73.92,48,black);return s;}
function addNode(s,index){const n=model.nodes[index],y=230+60*index;const label=text(s,'node-'+n.id,`${index+1}. ${n.label}`,345,y,245,50,29.333333,black);text(s,'detail-'+n.id,n.detail,600,y,615,50);const rootShape=s.shapes.items.find(x=>x.name==='tree-root');s.shapes.connect(rootShape,label,{kind:'elbow',fromSide:'right',toSide:'left',line:{fill:'#8C64E1',width:2,style:'solid'}});}
function treeBase(prior){const s=frame('我们已能解释图像的哪些问题？');text(s,'summary-instruction','先说结论和证据，再补充这张树。',64,163,1150,50);const sh=rect(s,'tree-root',64,355,190,70,'none','#8C64E1',3);sh.text='图像编码';sh.text.style={typeface:black,fontSize:32,bold:true,color:'#262626',alignment:'center',verticalAlignment:'middle',autoFit:'none'};for(let i=0;i<prior;i++)addNode(s,i);return s;}
const extras=[];
function register(s,entry,script){const e={extra:extras.length+1,...entry};extras.push(e);s.speakerNotes.textFrame.setText(`[问题 / 页面目的] ${entry.title}\n[内部编号] ${entry.q}\n[阶段] ${entry.stage}\n[教师逐字稿] ${script}\n[课堂操作] ${entry.stage==='question'?'先收集学生独立总结和证据，再翻页。':'只说明当前新增焦点，先前内容保持可见。'}\n[来源] course-design.qmd C4a／${entry.q}；熊猫实验数据与技术边界见C4。`);}
for(const cp of model.checkpoints){let s=treeBase(cp.prior);const title='我们已能解释图像的哪些问题？';register(s,{q:cp.id,stage:'question',title,after:cp.after,nodes:cp.prior,focus:null,visible:'仅中性根节点和已建立的枝；先学生总结',withheld:'本检查点新增枝、未来枝及其解释'},`${cp.prompt} 先自己想20秒，再请两位同学各说一条结论和依据。若只有术语没有依据，追问是哪张网格、色块、码表或算式支持它。教师归纳准确后才依次揭示。本检查点含总结与更新约${cp.seconds}秒。`);
 for(const id of cp.add){s=s.duplicate();for(const sh of s.shapes.items){if(sh.name.startsWith('focus-'))sh.line={fill:'none',width:0};if(sh.name==='new-label')sh.text='';}
 const index=model.nodes.findIndex(x=>x.id===id);addNode(s,index);rect(s,'focus-'+id,337,226+60*index,878,57,'none','#FF0000',3);text(s,'new-label','新学',64,595,190,50,29.333333,black,'#8C64E1');register(s,{q:cp.id,stage:'answer',title,after:cp.after,nodes:index+1,focus:id,visible:`在已有树上新增${model.nodes[index].label}及对应关系`,withheld:'所有未建立的后续枝'},model.nodes[index].script);}
}
const e=model.exit;let s=frame(e.title);text(s,'exit-givens',e.given,90,180,1100,115,32);text(s,'exit-task',e.task,90,315,1100,105,29.333333);register(s,{q:e.id,stage:'question',title:e.title,after:e.after,nodes:7,focus:null,visible:'新参数和独立任务；无算式或答案',withheld:'码长、数据量、预算结论和PNG边界答案'},'换一组没有算过的数据。请独立写最少位数、判断依据、数据量和预算结论，再写一句这个结果能否当作完整PNG文件大小。给60秒；不讨论、不先报答案。教师先收齐或拍下原答，再揭示。');
s=s.duplicate();text(s,'exit-calculation',e.answer,90,445,1100,105,34,black,'#8C64E1');register(s,{q:e.id,stage:'answer',title:e.title,after:e.after,nodes:7,focus:'capacity-payload',visible:'容量与像素数据量的联合判断',withheld:'PNG完整文件边界答案'},'两位的四种状态不足以区分五色，三位够用。120个像素各三位，是360bit，换成45B，满足50B预算。先核对前三项，不让学生覆盖原答案。再请一人解释还剩下的文件大小问题。');
s=s.duplicate();text(s,'exit-boundary',e.boundary,90,565,1100,82,29.333333);register(s,{q:e.id,stage:'evidence',title:e.title,after:e.after,nodes:7,focus:'file-boundary',visible:'只新增像素有效载荷与完整PNG边界',withheld:'课后答案'},'45B只计理想像素码字。PNG还有格式结构与压缩，不能据此得到完整文件大小。容量、列式单位、预算、文件边界各一项，至少三项且容量正确视为达到本次退出标准。记录实际匿名错误类别；本次文件构建不能填写学生达标人数。');
await (await PresentationFile.exportPptx(P)).save(path.join(out,'additions.pptx'));
await fs.writeFile(path.join(out,'additions-plan.json'),JSON.stringify(extras,null,2));
console.log(JSON.stringify({addedSlides:extras.length,output:out}));
