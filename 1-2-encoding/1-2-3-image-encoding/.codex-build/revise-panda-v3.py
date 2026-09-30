from pathlib import Path
import json,re,hashlib
root=Path(__file__).resolve().parent.parent;b=root/'.codex-build'
old=(root/'course-design.qmd').read_bytes();archive=root/'references/course-design-v2.5-source-record.qmd';archive.parent.mkdir(exist_ok=True)
if not archive.exists():archive.write_bytes(old)
qs=json.loads((b/'lesson-teaching-panda-v2.json').read_text())
qmap={q['id']:q for q in qs}
qmap[17]['transition']='已有像素决定了可还原的内容。把像素码字交给别人，他能唯一画出图像吗？'
qmap[18].update(title='只有这些码字，能唯一画出图像吗？',given='完整小图的码字为11 11 01 00 00 01 11 00；每像素2bit；四色码表已知；从左到右、逐行读取。',kind='decode',src='熊猫版v3新增解码挑战；数据取自Q7读码练习；替代原课该时段的扩展活动。',ask='现在把这8个像素当成一幅完整小图的数据，不要求沿用前面那一行的摆法。每个像素2bit，颜色对应关系已经给出，读取顺序也约定好了。请画出一种符合条件的图，判断别人是否一定会和你画得一样。先独立画，再和同桌比较。',tell='左边每行放4个，共2行；右边每行放2个，共4行。请按从左到右、逐行的顺序把两幅图读回去，得到的都是11、11、01、00、00、01、11、00。两种排列都满足题目给出的条件。因此，像素数相同、码字相同，还不能唯一确定二维排列；需要确定横向和纵向的尺寸。',expected='可能直接沿用先前的一行8格，也可能画4×2或2×4；误以为16bit本身会告诉我们哪里换行。',follow='若约定每行4个像素，8个像素一共有几行？再从图读回码字检验。',task='把一串像素码字还原成小图，通过两种有效排列发现二维尺寸的作用。',transition='规则解释了怎样读回数字图像；再回到图像的来源，比较自然光的连续变化与数字表示。',caveat='本例是未压缩调色板像素码字，不是JPEG文件字节。4×2与2×4只是两个反例，1×8和8×1也可满足原题。给定像素总数与有效行宽可推算行数，不要求两个数都必须独立存入文件。具体格式有不同的元数据、扫描顺序和色彩约定；解码需按格式解释，不能把本课扫描顺序说成所有图像文件的固定规则。解码只能还原已记录的量化像素，不能撤销采样与量化损失。')
qmap[19]['ask']='刚才已经知道怎样按规则读回数字图像。再回到记录之前的自然现象。看清每一行指定的观察情境：同一地点一天的气温、固定位置不同时刻的声波、水下不同深度的压强、房间不同位置的光照。分别主要看时间变化，还是空间变化？先按给定情境分类。'
qmap[21]['transition']='先用32B预算题检查颜色容量和数据量，再布置课后练习。'
(b/'authoring-panda-v3.json').write_text(json.dumps(qs,ensure_ascii=False,indent=2))
# Continue the existing editable deck source; change Q18 and adjacent teacher transitions.
s=(b/'build-panda-v2.mjs').read_text().replace('panda-v2','panda-v3')
s=re.sub(r'const imgs=\{\};.*?function img\(.*?\n','',s,flags=re.S)
# Read the active lesson implementation from the pedagogical source, after legacy defaults.
idx=s.index('function meanGrid')
s=s[:idx]+'''const design=await fs.readFile(path.join(root,'course-design.qmd'),'utf8');
const fieldMap={given:'必要条件',ask:'提问页教师逐字稿',tell:'揭示页教师逐字稿',task:'学生任务',expected:'预期回答与误解',follow:'关键追问',transition:'下一问',caveat:'技术边界',src:'来源与改编'};
for(const q of qs){const marker='# Q'+q.id+' ';const start=design.indexOf(marker);if(start<0)throw new Error('Missing course Q'+q.id);const end=design.indexOf('\\n# ',start+1);const section=design.slice(start,end<0?undefined:end);q.title=section.split('\\n')[0].slice(marker.length).trim();for(const [key,label] of Object.entries(fieldMap)){const m=section.match(new RegExp('\\\\*\\\\*'+label+'\\\\*\\\\*：([^\\\\n]+)'));if(!m)throw new Error('Missing '+q.id+' '+label);q[key]=m[1];}}
''' +s[idx:]
s=s.replace('原课PDF ${q.src}。原课问题链不变，本版熊猫数据为经用户确认的素材与参数改编，不冒充原课原始矩阵。','${q.src}。本版采用course-design.qmd当前课堂实施方案，熊猫数据与新增活动的来源分别注明。')
s=s.replace('完整数据与算法见panda-deck-design.md和.codex-build/panda-data.json','完整数据与算法见course-design.qmd的C4和.codex-build/panda-data.json')
s=s.replace("q.id===16?'独立计算", "q.id===18?'独立画图30–45秒，同桌核对后揭示；整个解码环节约3分钟。':q.id===16?'独立计算")
a=s.index(' case 18:');z=s.index(' case 19:',a)
s=s[:a]+''' case 18:ans=pair(q,t=>{text(t,'11 11 01 00 00 01 11 00',90,175,1100,65,43,C.ink,F.black);text(t,'完整小图的数据：每像素2bit，从左到右、逐行读取。',90,245,1110,55,31);colorKey(t,100,315,true,44);},t=>{text(t,'横4 × 纵2',180,380,400,50,32);text(t,'横2 × 纵4',795,380,400,50,32);grid(t,['3310','0130'],210,440,40);grid(t,['33','10','01','30'],840,440,40);text(t,'像素数相同，还不能确定二维排列。',90,615,1110,42,34,C.accent,F.bold);},'同一码字、已知码表与读取规则，未给二维尺寸','两种有效二维排列；反向读回得到同一码字');
newEvidence(q,'还原图像，需要数据和解释规则',t=>{text(t,'像素码字',90,195,330,60,38,C.ink,F.black);text(t,'11 11 01 00\\n00 01 11 00',90,285,350,125,36);text(t,'＋',390,315,70,65,48,C.accent,F.black);text(t,'解释规则',500,195,365,60,38,C.ink,F.black);['二维尺寸','每像素位数','颜色对应关系','读取顺序'].forEach((v,i)=>text(t,v,500,280+i*67,350,55,32));text(t,'→',855,340,100,75,45,C.accent,F.black);grid(t,['3310','0130'],990,310,40);text(t,'横4 × 纵2',955,435,270,55,30);text(t,'按约定还原像素图',90,600,1100,55,37,C.accent,F.black);},'前面算出的16bit，只是这8个像素的码字。要解释它，还需要知道二维尺寸、每像素几位、颜色怎样对应以及读取顺序。某些信息写在文件中，某些由格式或通信双方约定，不要求都另存一份。本页明确按横4纵2排列，把结果再读回去检查。注意，读回的是已经记录的像素，采样和量化丢掉的信息不会因此回来。下一问回到自然光：在变成这些有限位置、有限等级之前，它怎样变化？','像素码字与四类解释规则共同确定本课像素图');break;
''' +s[z:]
(b/'build-panda-v3.mjs').write_text(s)
for name in ['finalize-panda-v2.mjs','check-panda-v2.py']:
 (b/name.replace('v2','v3')).write_text((b/name).read_text().replace('panda-v2','panda-v3'))
