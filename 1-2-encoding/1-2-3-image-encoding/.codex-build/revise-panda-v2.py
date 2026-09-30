from pathlib import Path
p=Path('.codex-build/build-panda.mjs');s=p.read_text()
s=s.replace('lesson-teaching-panda.json','lesson-teaching-panda-v2.json').replace('slide-plan-panda.json','slide-plan-panda-v2.json').replace('candidate-panda.pptx','candidate-panda-v2.pptx')
# Replace teaching refinements after applying the original adaptation.
pos=s.index('function note(')
s=s[:pos]+'''const revision={
4:{ask:'先只看红框这一格。我们把这块区域的颜色取平均，得到右边的样本色。现在规定只能从下方四种颜色里选一种，你会选哪一个？先比较，再说理由。',tell:'这一格在第2行第3列，平均色更接近第三种可选色。把取得的样本映射到规定的有限等级，叫量化。请注意：取了哪些位置的样本，与最后允许用哪些颜色，是两个决定。下一页把同一规则用到全部64个位置。',task:'用一个真实区域的平均色作中间证据，再观察有限颜色的映射。',expected:'会选接近的浅色，也可能认为平均色必须原样保存。',follow:'如果平均色不在四种颜色里，这个实验允许直接保存它吗？'},
6:{ask:'先只看红框中的第四行，其他行暂时不读。把颜色编号换成码字，每个像素都要保留几位？试着把0、1、2、3各找一个出来。',tell:'第四行的3、3、2、0、1、2、1、1，分别换成11、11、10、00、01、10、01、01。下面各行照同一规则处理。编号换成二进制码字叫编码；每个像素使用2bit，这个位数叫位深度。整幅图的总位数还要乘像素个数。',task:'聚焦第四行，核对编号与二进制码字，不要求一次读完整幅矩阵。'},
11:{title:'三幅图的像素码字，各占几 bit？',ask:'这次只统计未压缩的像素码字，不算文件头或调色板。三轮分别有多少个像素，每个像素用了几位？先列出三个乘法。'},
15:{title:'R=138，怎样写成8位二进制？',ask:'红框中心的像素读出R为138、G为179、B为111。先只换算R通道。下表从左到右给出8个位权，哪些位置填1，合起来正好是138？给30秒写在纸上。',tell:'138等于128加8加2。对应的三个位置填1，其余填0，得到10001010。每个通道固定8位；请用同样方法检查G和B。下一页给出完整的三个通道，尤其留意B通道前面的0。',task:'用位权表逐步推导真实R通道的8位表示。',expected:'可能遗漏某一位或把十进制数字逐个编码。',follow:'如果把最左边的1改成0，表示的数少了多少？'},
17:{title:'放大熊猫图，就能看清新细节吗？'},
19:{title:'这些例子主要随时间还是空间变化？',ask:'看清每一行指定的观察情境：同一地点一天的气温、固定位置的声波、水下不同深度的压强、房间不同位置的光照。分别主要看时间变化，还是空间变化？同一种物理量可以换一种观察方式，所以不要只背名称。',tell:'前两行在同一位置比较不同时刻，因此主要随时间；后两行在不同位置比较，因此主要随空间。分类取决于这次观察的情境。接下来还要问：这些量只能取几个固定数值吗？连续变化才是建立模拟量概念的关键。',expected:'能按给定情境分类；可能以为温度只能随时间、光照只能随空间。',follow:'如果改看同一时刻不同地点的温度，横轴还应该是时间吗？',task:'按指定观察情境分类，避免按物理量名称机械分类。'},
};
for(const q of qs){Object.assign(q,revision[q.id]||{});if([11,12,13,16].includes(q.id))q.caveat=(q.caveat||'')+' 理想像素有效载荷按总bit数除以8；实际按整字节存放时，不足8bit的末尾需补位并向上取整。本课数值计算例均整除8；文件头、调色板、行对齐与压缩另计。';}
function meanGrid(s,means,x,y,z){means.forEach((row,r)=>row.forEach((rgb,c)=>rect(s,x+c*z,y+r*z,z,z,'#'+rgb.map(v=>Math.round(v).toString(16).padStart(2,'0')).join(''),C.grid,1)));}
function newEvidence(q,title,draw,talk,visible){const s=frame(title);draw(s);register(s,{...q,title},'evidence',visible,talk);return s;}
''' + s[pos:]
# Specific differentiated teaching pauses.
s=s.replace("stage==='question'?'先停留20–40秒，听学生预测或理由后再翻页。'", "stage==='question'?(q.id===16?'独立计算60–90秒，听两种解法后翻页。':q.id===15?'R通道换算留30秒；其余通道口头核对。':q.id===21?'综合应用留60秒，要求写条件和单位。':'短问停留15–25秒；先听理由，再翻页。')")
s=s.replace('完整数据与算法见panda-deck-design.md和.codex-build/panda-data.json。','完整数据与算法见panda-deck-design.md和.codex-build/panda-data.json；本次审查修订见panda-v2-audit.md。')
# case helper preserving other cases exactly.
def case(n,replacement):
 global s
 st=s.index('case '+str(n)+':');en=s.index('case ',st+5)
 s=s[:st]+replacement+'\n '+s[en:]
case(4,"""case 4:ans=pair(q,t=>{panda(t,80,205,320);mesh(t,80,205,320,8);rect(t,160,245,40,40,'none',C.red,4);text(t,'第2行，第3列',80,555,400,55,32);text(t,'这一格的平均色',550,180,540,55,34);const m=D.means8[1][2];rect(t,550,255,150,120,'#'+m.map(v=>Math.round(v).toString(16).padStart(2,'0')).join(''));text(t,'只能从下方4色中\\n选一种近似。',760,250,430,130,33);palette.slice(0,4).forEach((c,i)=>rect(t,550+i*142,430,78,78,c,C.grid,1));},t=>{rect(t,550+2*142,430,78,78,'none',C.red,4);text(t,'映射到有限等级：量化',550,570,650,65,36,C.accent,F.black);},'一个采样区域、实际平均色与四个选择','框出最近代表色，命名量化');
newEvidence(q,'把同一规则应用到64个样本',t=>{panda(t,80,240,280);meanGrid(t,D.means8,490,240,35);grid(t,four,900,240,35);text(t,'原图同一区域',80,175,340,50,31);text(t,'每格的平均色',490,175,340,50,31);text(t,'限制为4种颜色',900,175,310,50,31);text(t,'→',390,340,80,90,48,C.accent,F.black);text(t,'→',800,340,80,90,48,C.accent,F.black);text(t,'采样确定位置；量化选择有限颜色。',90,590,1100,65,36,C.accent,F.bold);},'从左到右看：先确定8×8个位置，取得每个区域的样本，这里用区域平均色表示；再把每一个平均色映射到四种可选颜色。中间图还没有限制成四种颜色。我们在已存在的数字图片上演示这两种作用，真实相机的采集过程更复杂。现在取得了有限颜色，下一步才讨论每种颜色至少用几位来编码。','原图、样本均值、四色量化结果并列');break;""")
# Q6: one focused row, remove redundant three-word recap build.
s=s.replace("grid(s,four,90,225,44,'number');text", "grid(s,four,90,225,44,'number');rect(s,90,357,352,44,'none',C.red,3);text")
s=s.replace("grid(s,four,745,225,48,'binary');text", "grid(s,four,745,225,48,'binary');rect(s,745,369,384,48,'none',C.red,3);text")
a=s.index('continuation(q,ans,',s.index('case 6:'));b=s.index('break;',a);s=s[:a]+s[b:]
# Q9 reveal: add an actual sample comparison with location.
needle="'相同样本增加两种中间色，得到六彩图');{"
s=s.replace(needle,"""'相同样本增加两种中间色，得到六彩图');
newEvidence(q,'同一个样本，增加两种近似选择',t=>{grid(t,fine,80,230,18);rect(t,80+12*18,230+9*18,18,18,'none',C.red,4);text(t,'第10行，第13列',80,555,430,50,30);const m=D.means16[9][12];const colors=['#'+m.map(v=>Math.round(v).toString(16).padStart(2,'0')).join(''),palette[0],palette[4]];['样本平均色','四色量化','六色量化'].forEach((label,i)=>{text(t,label,490+i*235,235,215,50,30);rect(t,490+i*235,315,180,150,colors[i],C.grid,1);});text(t,'位置和样本相同，改变的是可选颜色。',465,555,750,90,33,C.accent,F.bold);},'红框指向第10行第13列。把它的样本平均色单独放大。四色时，最近的是原调色板编号0；增加两种中间色后，编号4更接近这个样本。样本没有重算，取样位置也没有变。即使投影颜色不容易分清，也能用这个规则解释：原来的选择都保留，多两个选择不会让最近距离更大。这里不要求学生计算颜色距离。','16×16实际位置与同一平均色的四色、六色近似');{
""")
# Distinguish payload from file from first arithmetic page.
s=s.replace("case 11:ans=pair(q,s=>{table", "case 11:ans=pair(q,s=>{text(s,'只计未压缩像素码字，不含文件头和调色板。',90,163,1100,45,29.333);table")
s=s.replace("text(s,'1 B = 8 bit',90,185,1100,60,35)","text(s,'1 B = 8 bit（只计未压缩像素数据）',90,185,1100,60,35)")
# RGB process: retain real values, teach one channel; all channels then given as evidence.
case(15,"""case 15:ans=pair(q,t=>{panda(t,90,225,300);sourceFocus(t,90,225,300,{x:D.pixel.x-3,y:D.pixel.y-3,size:7});text(t,'RGB = (138, 179, 111)',490,180,710,60,37);text(t,'R通道：哪些位填1？',490,265,710,55,34);table(t,[['128','64','32','16','8','4','2','1'],['？','？','？','？','？','？','？','？']],490,360,704,140);text(t,'每一格是一位，固定写满8位。',490,550,720,60,32);text(t,'红框中心的一个像素',80,585,430,50,30);},t=>{revealCells(t,Array.from('10001010',(v,i)=>[1,i,v]));text(t,'138 = 128 + 8 + 2',490,620,710,40,35,C.accent,F.bold);},'真实RGB读数与R通道位权空表','填写8位，解释138的位权分解');
newEvidence(q,'一个RGB像素：三个8位通道',t=>{rect(t,110,275,245,200,'#8AB36F');text(t,'RGB = (138, 179, 111)',90,550,510,60,32);['R  10001010','G  10110011','B  01101111'].forEach((v,i)=>text(t,v,610,210+i*105,580,70,46,C.ink,F.black));text(t,'24 bit = 3 bytes',610,555,580,70,40,C.accent,F.black);},'这是同一个眼睛像素的完整RGB表示。R刚才已经算过，G等于128加32加16加2加1，B等于64加32加8加4加2加1。注意B前面的0也必须写，它让每个通道都保持8位。三个通道总共24bit，也就是3bytes。这里读取的是JPEG解码后的像素，不是说JPEG内部直接按这个顺序存放每像素的三个字节。','真实像素色块、三个8位码字和总位数');break;""")
# Make Q17 question neutral and let the answer supply conclusion.
s=s.replace("text(s,'仍是已有的16×16个像素',695,575,520,50,31,C.accent,F.bold)","text(s,'放大已有像素，不增加原始细节',665,590,550,65,30,C.accent,F.bold)")
# Bridge two representation models after RGB explanation, before Q15.
needle="'揭示256级、24bit与组合总数');break;"
s=s.replace(needle,"""'揭示256级、24bit与组合总数');{
const bridge={...q,title:'同一种颜色，为什么有2bit和24bit？',ask:'同一块深色，刚才可以用00表示，现在又能写成三个8位通道。它的颜色没变，为什么位数不同？先想：00本身能告诉别人这是什么颜色吗？',tell:'2bit记录的是四色表里的编号，还必须知道约定的码表才能查到颜色。24位RGB直接记录R、G、B三个通道值。这块颜色是36、33、27，所以是三个8位。两种表示的规则不同；位深度不能脱离表示方案来讨论。',task:'比较调色板编号与RGB通道值，衔接两个位深度模型。',expected:'可能以为所有颜色都只需2bit，或认为同色位数必须相同。',follow:'如果把同一四色图保存成24位RGB，每像素仍只占2bit吗？',transition:'用眼睛里的真实像素练习RGB通道编码。',caveat:'这里只比较本课理想固定长度模型。调色板自身也需要保存或事先共享，不计入前面的像素码字数据量。'};
pair(bridge,t=>{rect(t,90,260,230,180,palette[0]);text(t,'同一块深色',90,490,340,55,34);text(t,'00',490,250,600,80,58,C.ink,F.black);text(t,'00100100 00100001 00011011',490,405,710,75,33,C.ink,F.black);},t=>{text(t,'查四色表的编号：2 bit',490,335,710,55,33,C.accent,F.bold);text(t,'RGB通道值：8+8+8 = 24 bit',490,490,710,55,33,C.accent,F.bold);text(t,'位数取决于采用的表示方案',90,610,1100,45,35,C.accent,F.bold);},'同色的两种码字，询问位数为何不同','区分查表编号与RGB通道值');}break;""")
# AI four-stage simplification must explicitly conclude with inference boundary.
s=s.replace("frame('用四步理解照片修复')", "frame('照片修复：推断缺损处的像素')")
s=s.replace("110,205+i*97,1080,70,36", "110,190+i*82,1080,65,35")
s=s.replace("register(s,{...q,title:'用四步理解照片修复'}", "text(s,'补全是推断，不能证明历史原样。',110,570,1080,75,38,C.accent,F.black);register(s,{...q,title:'照片修复：推断缺损处的像素'}")
s=s.replace("'四步课堂解释，采用准确的补全措辞'", "'四步课堂解释与修复结论的真实性边界'")
# Classifying temporal/spatial variation must be contextual.
s=s.replace("['温度','？'],['声波','？'],['海水压强','？'],['光照强度','？']", "['同一地点，一天的气温','？'],['固定位置，不同时刻的声波','？'],['水下不同深度的压强','？'],['房间不同位置的光照','？']")
s=s.replace("['例子','主要观察的变化']", "['观察情境','主要观察的变化']")
a=s.index(" const s=frame('模拟量的关键：连续变化')");b=s.index('}break;',a)
s=s[:a]+""" const temp={...q,title:'温度从25到26，只能跳着变化吗？',ask:'某处温度在这段时间由25摄氏度变成26摄氏度。中间可能经过25.5吗？还可能经过25.51吗？不要先看温度计显示了几位，要想实际温度的变化。',tell:'在本课的连续模型里，温度可以经过这些中间值。仪表只显示整数或一位小数，是读数方式的限制。我们用连续变化的物理量描述温度、声波或光照，称为模拟量。下一页对照图像中的取样位置和有限颜色等级。',task:'从可取中间值的具体问题形成连续量的模型。',expected:'学生可能把数字温度计显示的跳变当成实际温度只能跳变。',follow:'仪表只显示一位小数，能证明实际温度只能取这些数吗？',transition:'回看图像采样和量化，说明哪些选择变得离散。',caveat:'曲线是课堂概念示意，不是测量数据；不以“任意点有值”作为数学连续性的定义。'};
 pair(temp,t=>{line(t,130,520,760,520,C.ink,2);line(t,130,520,130,210,C.ink,2);text(t,'温度（摄氏度）',90,160,320,45,31);text(t,'时间',660,550,130,50,31);ellipse(t,190,450,14,14,C.ink);ellipse(t,690,260,14,14,C.ink);text(t,'25',145,400,100,50,32);text(t,'26',675,210,100,50,32);text(t,'中间能否取25.5、25.51？',820,270,390,140,34);text(t,'概念示意',90,610,300,45,22,C.muted);},t=>{line(t,197,457,697,267,C.cyan,4);text(t,'模拟量：连续变化',820,475,385,120,35,C.accent,F.bold);},'25到26的两个时刻，先判断是否存在中间值','连接示意并解释连续模型');"""+s[b:]
# Transfer: same question chain plus one-minute exit diagnostic.
needle="'揭示信息数字化链');break;"
s=s.replace(needle,"""'揭示信息数字化链');{
const exitq={...q,title:'只允许32 B，该怎样选择参数？',ask:'离开前完成这一题。仍用四种颜色，采用固定长度编码，只算未压缩像素码字，最多32B。四个方案可以选哪些？写出像素数乘位深度再除8，别只看像素个数。',tell:'A是16乘16乘2除8，等于64B，超过限制。B是16乘8乘2除8，等于32B，可以。C虽然只有32B，但1bit只能区分两种颜色，达不到四种颜色的要求。D是8乘8乘2除8，等于16B，也可以。B比D保留更多采样位置，但长宽采样数不同。决定之前要同时核对颜色容量和数据量，不能只看字节数。',task:'同时运用颜色容量与像素数据量，诊断不满足条件的方案。',expected:'容易只算字节数而误选C，或只选恰好32B的B而漏选D。',follow:'最多32B是否要求一定用满32B？',transition:'课后继续练习并写明单位。',caveat:'四个方案覆盖同一取景范围，M、N分别为横纵采样数；本题只比较能否满足约束，不宣称B在所有视觉目标上最好。'};
pair(exitq,t=>{text(t,'需表示4种颜色；固定长度编码；最多32 B。',90,165,1100,60,32);table(t,[['方案','横向×纵向','每像素位数','是否满足'],['A','16×16','2 bit','？'],['B','16×8','2 bit','？'],['C','16×16','1 bit','？'],['D','8×8','2 bit','？']],90,255,1100,320);text(t,'只计未压缩像素码字。写出理由。',90,610,1100,45,31);},t=>{revealCells(t,[[1,3,'64 B，超出'],[2,3,'32 B，满足'],[3,3,'仅2色，不足'],[4,3,'16 B，满足']]);},'颜色数与数据预算约束下选择方案','核对字节数和颜色容量，B与D均满足');}break;""")
Path('.codex-build/build-panda-v2.mjs').write_text(s)
