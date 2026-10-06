# 音频编码课程 v4 复审与更新记录

日期：2026-10-01。任务：全面审查并实施更新。依据为执行时仓库AGENTS.md、slide-style-guide.md及本课course-design.qmd；未打开或采用其他课程课件。本记录延续v1／v2／v3审查系列，只证明本次明确绑定的v4；旧报告仍属于旧版本。

本次结果是**已完成本机验证的课程包，尚未完成目标教室验收**。正式课件：`exports/1-2-3-audio-encoding-v4-final.pptx`，62页、Q1–Q19，272,053B，SHA256 `eafbf062bad7183479b5904ffc1189b3fc5d75b7bd5eea62302f5fc34207cafd`。PPTX继续是正式课堂格式；Reveal为参考，Notebook由教师操作，学生纸笔与讨论。入口为本课README.md。

## 发现、证据、教学影响与已实施修正

修改前Git工作区清洁；README及设计指定v3-final、40页，不能由编号推选。`v4/inventory-before.json`盘点460个文件，包含隐藏、ignored、untracked、checkpoint、缓存、输出与验证证据。原v1／v2／v3、原媒体、旧参考和旧报告保留；修改前当前源保存于`history/v3-sources/`。最终保留情况见`v4/preservation-check.json`。

|位置与修改前证据|教学／制作影响|实施修正与当前证据|
|---|---|---|
|v3设计／生成器没有新版规定的渐进知识树；历史构建没有树阶段|讨论后的概念和关系缺少学生举证后的整合，不能用历史验收豁免|设计C8明确节点、父关系、Q、学生总结、揭示与时间。Q7／12／17／18后四次总结，9个节点逐次建立；原生可编辑文字、形状、连接线；旧节点固定，新焦点红轮廓加“新增”文字。p18–22、37–39、53–55、58–59与Notebook／活动／Reveal同步|
|v3 Q4、Q8、Q10、Q17在同一揭示中承担间隔换算、频率应用、误差计算、A/B参数回扣；build_deck/finalize/checks固定40页或v3路径|独立推理缺少先作答的机会；旧检查可能验证错误版本|新增Q4-B／Q8-B／Q10-B／Q17-B的提问→复制揭示；Q15样本总数与bit→B分两次建立。lesson_model编译62阶段，实际PPT顺序、Notes和复制基础几何逐项检验|
|完整两版Notebook、原组合活动单及文件名包含后续任务／参数。实际JupyterLab折叠代码仍可见首行|隐藏元数据不能保证不泄题；开场参数可能提前暴露|完整文件改为备课／阅读；课堂8份当前阶段文件。主任务与-B分开；中性函数名，WAV名称留在共享实现；D1前后两单元都不显示采样函数名或12点参数，实际运行先仅波形、后记录点。A／B／exit分阶段分发。B的T4旧提示直接给出候选成败，改为中性双条件总结；Q7不预填码字或提示“缺采样率”|
|设计C3及D2旧表述可能在Q8绑定开场A/B参数；活动Q7标作课后拓展|削弱Q17检验开场猜测的闭环；混淆核心口答和拓展时间|Q8使用已知参数的独立对照，Q17-B才显示开场身份。Q7课堂短口答记依据，画时间轴作为课后拓展|
|原Q19自选改写不能单独覆盖全部目标；原节奏未计入新增树总结|志愿口答／自选项不能证明全班目标掌握；计划可能挤掉独立评价|保留Q19，必改③两处并写证据，再选①或②，60秒独立、先收卷后揭示。Q5／6、Q16、Q18记录一并收集；C1映射行为与判据、持续误解回应。C2独立任务／讨论／证据／Demo／切换／树总计45分钟，明确裁剪点和30秒故障阈值|
|prepare_audio依赖ignored的完整解码缓存；制作脚本默认覆盖音频及manifest；有效2／4／8bit文件实际均存储16bit|换机不能确定性制作；有效等级、实际文件大小和转换恢复容易混淆|保留原M4A及11份WAV；新增历史PCM的45–51秒无损摘取与provenance，试写目录重新生成11份与原hash完全一致。README记录默认覆盖及显式trial命令、解码器版本差异、许可未确认|
|旧finalize路径／工具位置、font defaults补丁及验证写入依赖本机|输出补丁不能保证重建，旧报告可能误用于新文件|候选在.build/v4；字体补丁每次构建必跑；finalizer接受明确路径、从计划取页数、拒绝覆盖已有正式文件，工具路径可配置。render/audit明确绑定当前v4；下一版本需改路径与证据位置|
|首轮v4试制发现Artifact Tool duplicate插入原页后，树更新跑到较早阶段；树文字框原高度使两行缺少余量|未来知识提前出现；树可读性受损|生成器duplicate后显式移动到末尾；树节点高度84px，保持22pt文字，不缩字。试验交付移入.build/v4/trial-*，最终重新渲染，旧节点位置、内容、关系与实际presentation顺序检查通过|
|HTML初始结果／后续试听、IFrame相对路径与Notebook图字号需实际界面检验|备用台可能提前给答案或打不开；图表缩放不可读|HTML仅当前D，采样／量化／转换结果须点击，参数改变重置揭示，禁止autoplay、播放互斥。IFrame改为本课Jupyter root下/files路径并实际点击。量化双图同尺度同屏，增大图表标签并复查最终界面|

保留每个主Q的认知起点、困惑、任务、预期回答、追问、证据、抽象与下一问；不是删除教学理由后生成摘要。`v4/source-output-checks.json`的章节完整性检查只是结构证据；下表的语义核对、阶段稿和教学条件审查另行承担教学对齐。

## Q、证据、产出与阶段的语义对齐

Reveal v4有62个section，与以下PPT页一一对应；每个section的背景字节等于最终渲染PNG，Notes来自同一逐页计划。完整teacher／student QMD/IPYNB包含Q1–19，课堂只展示当前阶段文件。题面、数据、边界与形成结论按设计逐项核对。

|Q／PPT页＝Reveal阶段|学生先做什么、再建立什么|Notebook／活动与树|
|---|---|---|
|Q1 p2–3|同为6秒未压缩，观察529,244／96,044B、匿名试听；提出待核对猜测，暂不公布参数身份|opening；板书猜测，Q17-B回看|
|Q2 p4–5|波形把时间与相对幅度分开；负幅度不等于负音量|两版Q2；数学图不是原音乐测量|
|Q3 p6–7|纸上圈时刻，再看[0,1)的12点，形成时间采样|D1、A；24点／动画可选；T1|
|Q4 p8–9；Q4-B p10–11|8000Hz指每秒每声道记录次数；独立求1/8000秒＝0.125ms|两版Q4／Q4-B；T1，不把声音自身频率混入|
|Q5 p12–13|换一组手算值−0.62／−0.10／0.38／0.84，先选代表值，后核对0–3等级|A四行可收集；T1；不是D1的同一批数据|
|Q6 p14–15|等级至少2bit，先写00／01／10／11，再互读回代表值|A码字空表／同桌检验；T1；无符号等级与真实PCM分开|
|Q7 p16–17|只有码字能否确定原速？联系采样率、位数、声道与编码约定|A短口答及T1举证；课后画时间轴|
|T1 p18–22|先总结Q3／5／6／7证据，按采样→量化→编码→参数逐项补树|两版总结空间、A；60秒预算|
|Q8 p23–24；Q8-B p25–26|相同时长的采样率对照；给出带限理想规则后独立代入6k／8k，运行正常低通结果|D2及D2-B；6kHz／24kHz基准→滤波8kHz；裸丢点2kHz只备用；T2|
|Q9 p27–28|比较输入、保留频段、设备等条件；一次音乐试听不证明普遍音质规律|两版Q9；可裁剪重复试听，保留条件|
|Q10 p29–30；Q10-B p31–32|固定48时刻与范围，比较2／4bit近似；独立算−0.10的0.15／0.0375误差|D3／D3-B；B在主Q10结论后分发，数值表作答后运行；T2|
|Q11 p33–34|先用2^n计数，分清位数加倍与等级数指数增长|两版Q11；2→4bit为4→16级，非仅2倍；T2|
|Q12 p35–36|区分采样的时刻、量化的代表值与编码的表示；读回等于已记录数据|两版Q12；不宣称恢复采样／量化前信息|
|T2 p37–39|学生用D2／D3举证后补频率条件与量化精度|两版总结空间、B；45秒；误差界有范围／无过载条件|
|Q13 p40–41|数三个时刻L／R的3／6个样本，推同参数数据量2倍，不推音量／音质翻倍|两版Q13；Q16独立算式再核对声道乘数；T3|
|Q14 p42–43|区分参数、样本与WAV容器；当前为未压缩整数PCM|两版Q14；不把WAV后缀当未压缩保证；T3|
|Q15 p44–46|先计fs×t×c个样本，再乘存储bit并÷8换B|两版Q15；两次复制揭示保留基础几何；T3|
|Q16 p47–48|独立一分钟44.1k／16bit／双声道算式：10,584,000B，MiB列式|B记录、同桌查单位并收集；T3|
|Q17 p49–50；Q17-B p51–52|先预测2秒样例完整文件是否32,000B，运行32,044B；再检验开场猜测及实际A/B参数|D4／D4-B独立文件；各一张真实计数表，未来表不在同一画面；T3|
|T3 p53–55|用帧计数、算式与差额举证后补payload／容器开销，44B限当前简单布局|两版总结空间、B；45秒|
|Q18 p56–57|先查最高6kHz与65,536B两个条件；8／16／24kHz对应32,000／64,000／96,000B|B双条件三行表收集；仅16k满足当前理想模型，实际滤波有余量要求|
|T4 p58–59|学生依自己的表举证后才补“约束下选择”，完整树此时首次出现|两版总结空间、B中性提示；30秒|
|Q19 p60–61|独立60秒必改③容器／公式两处，再选①或②，依据必填，先收再揭示|exit；目标证据还包括A、B的个人产出，无重复退出测验|
|封面p1、课后p62|角色、任务背景；课后441,000B／16倍／不恢复未记录6kHz|全页均有用途、分阶段稿；课后不是课堂退出评价|

学习目标、学生证据、成功标准及持续误解回应见设计C1；四参数漏乘、bit/byte错换、等级线性增长、负音量、只凭听感或以升采样恢复信息分别有追问和重新独立作答安排。只报结论无依据不达标。

## 独立计算、恢复目标与媒体

`scripts/audit_package.py`用Decimal手算Q5／Q10、独立struct解析RIFF及PCM、独立正弦／档位推导PPT原生坐标，未把生成器和检查器相互同意当成技术证明。

- Q5范围[-1,1)、步长0.5、中点−0.75／−0.25／0.25／0.75，边界归上档、越界饱和；量化误差半步长上界只对范围内无过载成立。2／4／8bit边界及中点均测；−0.10误差0.15／0.0375。反例0.24由2bit改4bit，误差从0.01变0.0725，证明“上界变小”不能改写为“每点严格变小”。
- 采样时刻k/fs，0≤k<fs·t；本例fs·t为整数。非整数时长优先采用实际帧数，不把右端点重复计入。边界等号以正弦零相位采样反例核对，课堂理想模型用fs > 2fmax；不由12／24点图推听感。
- 独立读取11份WAV的格式标记、fs、存储bits、声道、byte rate、block alignment、data chunk、帧数及hash。有效2／4／8bit三份都为22,050Hz、mono、stored16，132,300帧、264,600B payload、264,644B文件。正常低通结果以RMS上限<0.002（归一化幅度）核对，裸丢点峰值2kHz与基准6kHz分别检查。
- 2秒样例16,000帧、32,000B payload、32,044B文件；A／B各264,600／48,000帧，529,200／96,000B payload，加当前44B开销。Q16、Q18上述数据独立复算，分钟／秒、Hz／kHz、bit／byte、B／KiB／MiB分开。
- 写PCM为np.rint(x×32768)，ties-to-even，再饱和至−32768…32767，little-endian交错int16；read除32768。11份音频写回直接比较已记录payload字节完全相等；额外边界／半整数／过载测试与struct预期相等。相等目标是已记录整数样本，不是任意原浮点、采样前声波或AAC编码前信息。
- 原M4A SHA256 `7dc0b09ef6175492528227583e799b7a8db7297fe5b7a03c6bd341f1d1825d84`。历史缓存与本次afconvert解码均12,155,821帧，新解码最大差1 LSB；不能说AAC→PCM恢复此前损失或两个解码器必然逐样本一致。无损摘取保留旧PCM精确字节，使prepare_audio试写的11个hash复现原音频。源、变换、共同增益0.7490779781559563、10ms fade及hash见audio-manifest和audio-provenance-v4.json；原音乐公开再分发许可**unverified**，不得据本次技术检查推定已许可。

控制变量采用同一45–51秒输入、先双声道平均、共同增益和淡入淡出、相同播放音量；文件播放不独立归一化。数学波形／重处理已解码数字音频是教学模型，非真实ADC。FFT滤波／插值是教学重采样器，不作工业性能保证。6kHz基准不可闻时改用条件与测量；音乐差异不可辨时仍可使用误差图和真实字节；不把“听不见”作为唯一证据。

## 一手资料、版本与支持范围

以下于2026-10-01检索；为教师参考，不要求学生课堂联网。只有本地计算／文件测量证明当前例子的实际数值。

|标题／版本／定位|支持内容|限制|
|---|---|---|
|[Analog Devices MT-001](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf)，Rev.A 10/08，p1量化误差|理想均匀量化与半LSB误差界|有模型／无过载条件；不证明每点更小，不引入SNR教学目标|
|[Analog Devices MT-002](https://www.analog.com/media/en/training-seminars/tutorials/MT-002.pdf)，Rev.A 10/08，pp1、4–6|带限、采样／重建和抗混叠滤波需求|本课用严格大于防止边界误读；实际滤波需余量，有限量化仍有误差|
|[Microsoft WAVEFORMATEX](https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/ns-mmeapi-waveformatex)，Win32现行网页，Members／Remarks|每声道采样率、声道数、nBlockAlign、nAvgBytesPerSec、存储bits；MS-ADPCM例子|不以未压缩PCM公式计算压缩格式；容器不等于编码算法|
|[Microsoft Devices and Data Types](https://learn.microsoft.com/en-us/windows/win32/multimedia/devices-and-data-types)，2023-04-26，PCM Waveform-Audio Data Format／PCM Data Packing|16bit有符号值−32768…32767，低字节先、双声道L/R排列|页面使用sample称呼整帧处按本课“音频帧／每声道样本”澄清；不推广到所有PCM容器|
|[Microsoft RIFF](https://learn.microsoft.com/en-us/windows/win32/xaudio2/resource-interchange-file-format--riff-)，2021-01-07，chunk结构／对齐|RIFF容器由chunks组成及word padding|44B仅由当前fmt/data布局测得，非全部WAV常数|
|[Microsoft DirectXTK Wave Formats](https://github.com/microsoft/DirectXTK/wiki/Wave-Formats)，2022-04-26，WAVEFORMATEX／PCMWAVEFORMAT／EXTENSIBLE|PCM、IEEE float、ADPCM等，容器存储宽度与有效bits字段区别|本课effectiveN-stored16是教学量化等级，不声称写了EXTENSIBLE有效bits字段|
|[Python wave](https://docs.python.org/3.12/library/wave.html)，文档3.12.14，简介／getnframes／getsampwidth|未压缩PCM读取、帧数和字节宽度接口|3.12新增EXTENSIBLE PCM支持；本次实际3.11.16仅用传统PCM，未依赖新支持|
|[NIST Binary prefixes](https://physics.nist.gov/cuu/Units/binary.html)，在线表Ki／Mi|Ki=2^10、Mi=2^20|kHz使用SI千，不用Ki换频率|
|[IPython.display.Audio](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#IPython.display.Audio)，本机9.17.1，Audio参数说明|数组默认归一化与文件嵌入播放的区别|浏览器、音箱和播放器仍需实际验收；未用数组独立归一化比较响度|

设计C7的Chapter20保留为2026-09-30原始来源，未把它计作本次新增检索证据。网页版本不确定处以检索日期和具体字段／章节定位，不编造规范版本。

## Deck acceptance record（style guide §21.3）

|Check|Result / evidence|
|---|---|
|Slide order, Q IDs, and reveal stages match the plan and course-design.qmd|**pass**：62实际presentation顺序与计划、完整Q1–19、4个独立子问题、Q15分层和13个树阶段；package及source-output检查、上表语义核对|
|Question slides contain no premature answer or teacher-only text|**pass**：必要条件／中性证据及问题稿逐页检查；问题稿不朗读预期答案。教师参考分区标注“不在提问阶段朗读”；主要课堂Notebook／活动分阶段交付，T4答案泄露已修正|
|Evidence is readable and each red focus mark identifies its intended target|**pass（本机渲染）**：62页图像及全尺寸密集页；Q10红误差段、树单焦点红轮廓＋“新增”文字；目标投影可读性unverified|
|Every slide was rendered; montage and dense slides were inspected|**pass**：LibreOfficeDev 26.8.0.0.alpha0，PDF62页、1601×900 PNG62张、7张montage；全页及问答、波形、误差、计数、树全尺寸检查，修正后刷新；visual-inspection.json逐页hash|
|Geometry, rails, fonts, and question/answer stability passed structural checks|**pass**：16:9白底／紫轨、标准标题与内容区、native字号／边界／复制txBody和几何稳定。593文本script字体检查，PDF实际Alibaba Black／Regular；横向446行glyph测量0issue。WPS不能由此推定|
|Speaker Notes, technical claims, dates, and sources were checked|**pass**：62页以完整问题／目的开头，分阶段自然稿、停顿、回应、下一问；树先收学生总结再更新，退出先收再解答。技术复算与上述一手资料支持范围核对|
|Final PPTX was inspected in WPS / PowerPoint|**unverified**：当前可用环境没有目标Windows WPS／PowerPoint检查；须用同一hash副本实查布局、字体、Notes与翻页，PDF不替代|

原生图形和连接线保留可编辑性，图表／表格由原生形状及文字组成；finalizer中的“native chart/table count=0”是没有专用chart/table部件，并非未检查这些教学图表。它的结构receipt不声称技术／渲染正确，后续独立检查补充这两层。

## 分层验证、环境与证据

|层／状态|方法、证据和边界|
|---|---|
|教学对齐 **pass**|设计C1–C8、上表19Q语义对照、逐页visible/withheld/notes/evidence/focus/tree计划；计划45分钟累计4／8／15／21／27／30／38／45。裁剪可选动画、音乐／混叠、短口答；保留独立记录、四次总结、Q17闭环和Q19|
|结构／技术 **pass**|audit_package 2138检查0失败；source-output 101检查0失败；native-finalization package/layout/import pass；text-fit 446行0issue。每份清洁Notebook无输出／counts；精确源／输出一致性与英文implementation扫描。中文教学标签／题面／原文件名／精确数据为允许字面量；实现注释、docstring、标识符、developer messages及嵌入代码人工复核|
|渲染／人工 **pass（本机）**|render-checks绑定上述PPT hash；PDF SHA256 `3dbd62cb580c3aecf88d507e3e600097d794d5747cd2a6a9ba3a78070ca14f95`。montage1–7及62页PNG在v4/render；树增加空间后重新检查；visual-inspection与实际字体记录|
|真实内核 **pass（本机）**|Python3.11.16／numpy2.4.6／IPython9.17.1／matplotlib3.11.2／ipykernel7.3.0，文档目录，120秒timeout；teacher 13、student 12代码单元，8阶段文件各fresh kernel。实际executable/cwd记录kernel-environments，不依赖launcher自报环境。12项实际观察输出检查：同屏误差图、误差值、标注音频、D4单表。无待完成代码，预期补全路径不适用（学生纸笔）|
|复制运行 **pass（本机）**|check_copy独立目录103个文件，两版各fresh kernel；检查实际ROOT及audio_core来自复制目录、HTML相对资源存在。路径须resolve以处理macOS /var与/private/var别名。执行副本copied-*、copy-checks.json／copy-execution.txt；不含课堂制作缓存依赖|
|Reveal **pass（本机HTTP参考）**|Quarto1.10.18生成7份HTML，62section，无自动标题页；每背景PNG与最终render精确相同。浏览器实际问题／揭示检查、字体呈现、路径与本地依赖。参考采用静态镜像，不能修改其中波形；精确可编辑版本是PPTX，实验交互由Notebook／HTML。成功Quarto本身不作课堂证明|
|JupyterLab GUI **pass（已检查范围）／其余unverified**|macOS JupyterLab4.6.3，实际检查初始折叠仍可见首行、D1中性两单元的纯波形→12点阶段操作、匿名A/B播放器6秒与无media error、同屏D3坐标／图例、IFrame加载并点击12点；截图jupyter-D1-initial／waveform／recorded、jupyter-opening、jupyter-D3-final、jupyter-iframe和iframe DOM。最终完整D3截图已刷新。未逐一在目标Windows操作所有Notebook，故不能给全环境GUI通过|
|HTML GUI **pass（本机HTTP）**|D1初始无点、点击／动画24点、重置隐藏；D3初始无量化结果，切换4bit得到16级与0.125步长，改变参数须重新揭示，试听按钮后播放；D2-B初始只基准，转换结果点击后可见，3秒播放器无media error。截图html-D1／D3／D2-B；不会由浏览器成功播放推定音箱听辨|
|离线file协议 **unverified**|已验证复制依赖全本地；实际file://导航被浏览器URL安全策略禁止，未执行且未绕过。需教师在目标浏览器双击HTML／Reveal并运行相应阶段；HTTP检查不替代双击支持。Notebook IFrame依赖本课作为Jupyter root；自定义base_url前缀仍需调整／验证|
|课堂应用 **unverified**|Windows、WPS／PowerPoint实际排版／Notes与JupyterLab全阶段操作尚无目标环境证据。下一步按README顺序在目标机检查，必要时使用PPT＋预制WAV备用|
|课堂条件 **unverified**|投影、教室音箱固定音量与基准可闻性、学生活动完成时间、全班答卷、45分钟实测节奏未进行。下一步试讲记录实际检查点与作答；计划不能写成实测|

本次Node24.19.0／Artifact Tool 2.8.71用于制作，bundled Python用于PDF字体读取；它们不是课堂运行依赖。LibreOfficeDev alpha只是本地渲染器，不把兼容性推到正式WPS。Quarto有zh-CN／Abstract本地化warning，7个输出均完成。最初sandbox无法绑定内核端口／访问Quarto缓存，已按原授权通过审批后实际执行；早期失败日志不是通过证据。最后一次自动审批服务额度错误导致动作未执行，用户“continue”后同一审批路径重试成功，没有绕过。

## 复现、写入与后续验收

README列明当前源／输出所有权、制作与课堂依赖、命令、相对路径、分发和覆盖行为。顺序是设计／逐页计划→build_views→native build_deck→patch_font_defaults→finalize到新路径→全页render→build_views --rendered-slides→Quarto→fresh kernels／实际输出／audit／source-output／copy检查。字体补丁是每次构建步骤，不是事后手改正式课件。

prepare_audio默认会覆盖assets/audio与manifest；本次只写`.build/v4/audio-repro`和v4 reproduction manifest。build_views会覆盖当前两版QMD/IPYNB、8阶段文件、活动、Reveal与计划；人工修改须保存并回写设计／正确源。finalizer拒绝覆盖已有正式文件；旧试验留.build/v4/trial-*，旧交付与报告身份不变。当前render/audit以v4为明确目标，下次版本必须更新绑定，不能沿用此报告。

`v4/sha256-manifest.json`记录交付、来源、源码与证据hash。`git diff --check`与新增作者文本的空白检查在最后完成；生成vendor依赖／历史源按原始字节保留，不把它们的已有格式当作人工代码修正。没有提交、推送、发布，也没有修改其他课程。

仍需完成：目标WPS／PowerPoint及Windows JupyterLab、file协议、投影音箱、活动收集和试讲节奏，以及公开再分发许可确认。原因与具体动作已分别列出。不存在以未验证项目冒充pass的“课堂就绪”结论。
