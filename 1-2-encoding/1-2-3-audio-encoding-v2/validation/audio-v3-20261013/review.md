# Audio encoding v3：两轮评审、修复与复查

验收日期：2026-10-13。交付文件：`../../1-2-3-audio-encoding-v3.pptx`。共54页：50页主线、4页可选附录。两轮共发现15项问题，均已修复并逐项复查通过；两轮均未发现p0问题。没有遗留的本次评审问题。

等级：p0为阻断教学或关键事实错误；p1为影响正确理解、揭示顺序或阅读的主要问题；p2为影响图示表达、操作或版面一致性的问题。排名反映修复前的影响。

## 本版改进

- 以同一组时刻和幅度贯通“采样点 → 量化代表值 → 等级编号 → 3bit码字”，码字与对应时刻垂直对齐。
- 采样率对照固定输入与时间范围；量化对照固定输入、时刻、幅度范围和规则。误差使用相同的局部放大比例，并保留“误差上界减小不保证每点都改善”的反例。
- 未压缩PCM先用8个实际16bit样本展开为两组byte，再进入8kHz、2秒的实例；依次揭示“样本数 → 每样本字节数 → 总字节数”，随后增加左右声道。
- 分开PCM样本数据和文件结构开销；通过本例真实WAV块结构验证32,000B与32,044B，再回扣开场A/B。
- 分开编码方法、文件容器和MIDI事件；混叠使用同幅同相余弦的受控示例，并与先滤波再采样的正常流程区分。
- 四次知识树更新均先收集学生总结，旧节点位置保持不变；所有图、码字、表格和知识树均为可编辑原生对象。

## 第一轮

修复前：`history/round1-before.pptx`，SHA256 `80afd40d58967bb20201006522336863d153e11bd1cebbb7b98a66b6db85f23e`。

修复后／第二轮起点：`history/round1-after.pptx`，SHA256 `4ccb9caf34ec3b7aa83abf6db7a67eba751bcd42c12b3c25692864988e6cbd6a`。

| 编号 | 排名 | 页码 | 修复前的问题 | 修复 | 逐项复查结果 |
|---|---|---|---|---|---|
| R1-01 | p1 | 23–24 | “码字”标签挤入第一个bit组；首个等级编号拥挤，码字组间距仅2px。 | 波形与码字整体右移，组间距改为8px；首个编号放到点的右侧。 | pass：两页渲染清楚；10组码字仍与各时刻对齐，标签和bit组无交叠。 |
| R1-02 | p1 | 27 | 分类题在学生判断前就出现PCM装入WAV的提示。 | 提问页改为中性“格式与数据”；PCM例子留到揭示。 | pass：学生可见文本无提前答案；提问稿保留预测，配对页基础几何稳定。 |
| R1-03 | p1 | 28 | PCM、MP3、WMA共用指向WAV的箭头，易被读成统一包装路径。 | 只绘制本课“未压缩PCM → WAV”的实例；MP3/WMA分类放在路径外。 | pass：箭头与标签明确限定为本课实例，MIDI事件另列合成路径。 |
| R1-04 | p1 | 全部 | Native slide text使用Alibaba，但主题、母版及Notes默认值仍有Aptos。 | 每次导出后运行字体默认值修正；保留明确的Regular/Black变体。 | pass：扫描全部OOXML默认值无其他字体；实际注册两种Alibaba字体后重新渲染。 |
| R1-05 | p1 | 16–17 | 0.005误差标签依附7px宽的小括号框，文本超出框宽。 | 标签使用完整局部图宽度，误差括号保留真实比例。 | pass：标签框宽足够、渲染可读；0.13与0.005用同一比例，数值独立核对。 |
| R1-06 | p2 | 21–22 | 揭示页重复添加已有等级编号，产生16条文本框重叠警告。 | 复制原页后只增加bit组，保留原编号对象。 | pass：每页仅12个等级编号；几何检查重叠警告清零。 |
| R1-07 | p2 | 32 | 16bit虽分成两组，但没有明确揭示每组就是1byte。 | 两组下方分别揭示“8bit＝1B”，再显示8×2B的总量。 | pass：16格、两个byte标签与16B结果一致。 |

本轮统计：p0＝0，p1＝5，p2＝2。修复后2,767项结构／数值检查通过，几何findings＝0、warnings＝0。检查了全套montage，并对图示、配对页、树与所有问题修复位置作逐页详细检查；最终版本另完成54/54页全分辨率检查。

## 第二轮

起点为第一轮修复后文件。第二轮修复后的教学内容快照：`history/round2-after.pptx`，SHA256 `f79767cea73f58811d15e538c407745ac7cc2c5d566b5077f720f8ba453d009d`。

| 编号 | 排名 | 页码 | 修复前的问题 | 修复 | 逐项复查结果 |
|---|---|---|---|---|---|
| R2-01 | p1 | 34–36 | 最终总量出现在中间步骤上方，阅读顺序逆转计数逻辑。 | 样本数、每样本字节数、总量自上而下排列；已建立的结果转黑，只突出当前新增结果。 | pass：三步y坐标依次为514、564、614；前序结果的位置在后续build中保持不变。 |
| R2-02 | p1 | 33–38 | “16bit”未明确区分实际存储宽度与前面的3bit等级模型。 | 题面明确“实际存储16bit／样本”；Notes说明模型与真实存储的转换。 | pass：6页条件一致；独立计算单声道32,000B、双声道64,000B、退出题128,000B。 |
| R2-03 | p1 | 1（Notes） | 时间检查点与累计预算矛盾，进入编码被写成第24分钟而非第18分钟。 | 统一到45分钟预算；保留思考、树总结、开场回扣和退出评价。 | pass：独立累加4＋6＋8＋6＋2＋10＋7＋2＝45分钟；检查点与累计时间一致。实际节奏尚待课堂观察。 |
| R2-04 | p2 | 38 | 左右两行虽对齐，但没有标明“同一时刻两份值”的计数组。 | 揭示时用一个竖直红框圈定同一时刻的L/R对，并解释2B＋2B＝4B。 | pass：红框恰好包围一个左右样本对，未跨到其他时刻；讲稿对应这个焦点。 |
| R2-05 | p2 | 43–44 | 混叠示例未明示同幅同相，纵轴也缺少样本值标记。 | 标明同幅同相余弦，两个图都加入＋1／0／−1刻度并保持尺度一致。 | pass：五个样本均独立算得1、0、−1、0、1；直接取样诊断与正常滤波流程的边界在Notes中明确。 |
| R2-06 | p1 | 46 | 红色4kHz边界线穿过坐标刻度数字4。 | 红线结束于轴基线，不延伸到数字。 | pass：全分辨率检查数字无遮挡；线底部y＝386，与基线一致。 |
| R2-07 | p2 | 50 | 退出题算式中多个“2”未标明含义，不能清楚核对声道因子。 | 算式明确写“2秒”和“2声道”，Notes指出要圈的因子。 | pass：可直接定位声道因子；16,000×2×2×2B＝128,000B独立核对正确。 |
| R2-08 | p2 | 22、32、35–36 | 个别底部公式越出统一内容区，离底轨过近。 | 上移容量与toy总量标签，将三步PCM公式放入共享内容区，保留字号。 | pass：相关文本框底部不超过y＝656；渲染无贴轨、遮挡或自动缩字号。 |

本轮统计：p0＝0，p1＝4，p2＝4。2,838项结构／数值检查通过；几何findings＝0、warnings＝0；743组原生文本的实际字体宽度测量无溢出。54页全部在1920×1080图上逐页检查，最终montage已检查。每个问题的机器记录见`round1-issues.json`、`round2-issues.json`。

## 最终交付与验收

最终SHA256：`18079563ab41331b0c024af78879edfc5bc2db53602730091f40a2dc20ffcc58`，341,505 bytes。只在教学内容快照之后补上v3文档属性；变动仅有`docProps/core.xml`。重新导入并渲染交付文件后，54张PNG与逐页检查过的版本逐字节相同；记录见`visual-review.json`。

渲染环境：macOS，Node v24.19.0，`@oai/artifact-tool` 2.8.93，`@napi-rs/canvas` 0.1.100；两种真实字体注册为Alibaba PuHuiTi 3.0 55 Regular（weight400）及115 Black（weight1000）。这是本地渲染字体证据，不能证明WPS/PowerPoint会使用相同字体。

| 检查 | 结果与证据 |
|---|---|
| 幻灯片顺序、Q编号、揭示与计划一致 | pass：`plan.json`、复制页几何与逐页Notes核对。与相邻正式`course-design.qmd`的主要概念和技术边界已对照；完整问题链、编号、活动和评价同步为unverified，差异见下表。 |
| 提问页无提前答案或教师专用提示 | pass：按阶段阅读题面与讲稿；必要规则／条件保留，实际答案在下一build出现。 |
| 证据可读，红色焦点指向正确对象 | pass：全文字、刻度、误差括号、样本对与频率边界逐页检查。图示均为原生模型，未伪装成真实测量截图。 |
| 全页渲染、montage及详细检查 | pass：`render/slide-01.png`至`slide-54.png`、`montage.png`、`visual-review.json`。 |
| 几何、轨线、字体与配对稳定 | pass：`final-validation.json`的package/layout/import通过；`checks.json` 2,838项通过；`text-measurements.json`无宽度问题。 |
| Speaker Notes、技术主张、日期、来源 | pass：54页均有完整目的、阶段稿；来源在Notes。量化使用独立Decimal最近中点算法；混叠用余弦独立复算；PCM计数与真实WAV块直接读取。 |
| WPS／PowerPoint实际显示与Notes | unverified：本次未在这两个应用中完成实机检验。需在授课机安装两种Alibaba字体后检查配对页、码字、Notes与底部公式。 |
| Notebook执行及JupyterLab界面 | 不适用本次交付：未修改或交付Notebook；相邻包的阶段式Notebook不能按本版Q编号直接配套使用。 |
| 投影、声音与实际课堂时间 | unverified：45分钟为预算，无本版课堂实测。本版图示可脱离音频独立理解；若播放相邻包音频，另验扬声器、音量、可闻性及来源权限。 |

原版与v2保持原字节：原版SHA256 `3a13b7546c3d53cff92fe185615882c80eb9288c908cafb2ff4581c86e3566f5`；v2 SHA256 `ab329b5af80bfb9593ece665c38209aa4828c4c50727d09118955b1504a00815`。原版已有的Git修改和v2未跟踪状态未被替换。相邻正式v4、QMD、Notebook、Reveal与活动单均未修改。本版是指定v2目录中的独立修订，不自动升级为正式v4课包。

## 与正式课程设计的对照及边界

| 正式设计内容 | 本版对应页／任务 | 差异与课堂影响 |
|---|---|---|
| Q1开场、Q17-B回扣 | 2–3、41–42；Q1／Q1-return | A/B数值及完整文件与payload的区别一致；本版不嵌入音频，以图示／计算闭环。 |
| Q2波形、Q3–Q4采样 | 4–11；Q2–Q4／T1 | 本版采用5秒、1／2Hz的示意输入，正式设计使用1秒、12／24Hz数学模型；两者都说明取样时刻，不证明听感必然改善。 |
| Q5、Q10量化与误差 | 12–19、53–54；Q5–Q7／T2及附录 | 本版采用同一组10点、2／3bit均匀中点模型及局部放大；正式设计采用另一组手算值、2／4bit误差。不得将数值混用。 |
| Q6、Q11–Q12码字与三步 | 20–26；Q8–Q9／T3 | 本版4／8级状态数与连续码字图；Q编号与正式设计不同，不能按编号直接切换其Notebook。 |
| Q13声道、Q14–Q15结构与计数、Q17文件差额 | 27–28、31–40、47–48；Q10、Q12-A、Q12、Q12-B、Q13／T4 | PCM、实际16bit存储、声道、32,000B与32,044B结论一致；增加原生byte分组图与块结构图。 |
| Q8–Q9频率限制 | 43–46；Q14／Q14-B | 本版先用同幅同相的裸采样展示混叠存在，再给带限规则及正常滤波流程；正式课包核心使用正常低通音频。勿把裸采样图当作正常转换的音频结果。 |
| Q19独立评价 | 49–50；Q15 | 本版收集双声道计数及“编码＝压缩”的改写；正式设计的更多评价目标未在本次同步。 |
| Q7原速播放参数、Q16分钟／MiB换算、Q18容量与频率双约束 | 本版未完整保留这些独立任务 | 本版计算集中在样本、byte、声道与文件结构。若与正式包合并，须恢复这些任务并重新预算、同步问题与评价；本次不声称覆盖完整正式课程设计。 |

## 文件角色与重建

本记录是该独立v3的版本入口；`plan.json`记录54页、问题／阶段、复制关系、输入与量化值。`sources/build.mjs`是本版PPTX的拥有者，未改相邻课程的拥有者；`sources/patch_font_defaults.py`修正导出默认字体；`sources/metadata.py`仅写文档身份。`render/`、JSON检查结果、history和montage为版本绑定证据，不是课堂资源。

依赖：Node、`@oai/artifact-tool`、`@napi-rs/canvas`及两种Alibaba字体；Python和Pillow用于检查／montage。授课本身只需PPTX、相同字体及WPS或PowerPoint。使用本机的Codex bundled runtime；在其他机器替换Node／Python／模块／字体目录即可，不将构建路径当课堂依赖。

重建应使用一个新的试验目录，不覆盖已有交付或验证记录。工作目录为本验证目录；以下`trial_dir`需指向空目录，`font_dir`需含两种真实字体文件，`runtime_modules`指向已安装模块：

```sh
mkdir -p "$trial_dir"
ln -s "$runtime_modules" "$trial_dir/node_modules"
cp sources/build.mjs sources/render.mjs "$trial_dir/"
AUDIO_V3_FONT_DIR="$font_dir" "$runtime_node" "$trial_dir/build.mjs" "$trial_dir"
"$runtime_python" sources/patch_font_defaults.py "$trial_dir/candidate.pptx"
"$runtime_python" sources/metadata.py "$trial_dir/candidate.pptx"
"$runtime_python" sources/check.py "$trial_dir/candidate.pptx" "$trial_dir/checks.json" "$trial_dir/plan.json"
AUDIO_V3_FONT_DIR="$font_dir" "$runtime_node" "$trial_dir/render.mjs" "$trial_dir/candidate.pptx" "$trial_dir/render"
```

生成器会写入指定试验目录的`candidate.pptx`、`plan.json`、`presentation.json`，并替换同名试验输出；字体／身份修正原地替换candidate。它们不会直接写正式v3文件。需重新完成全页视觉评审、结构检查及标准finalizer，之后才能接受新版本。原始两轮生成器快照随history保存；可与最终源对照修改。

## 研究来源及图示用途

借用可视化的教学组织方式，全部图形为本次原生重绘；没有复制网页图片或模拟器截图。已在课件Notes保留来源、检索日期及边界。

| 来源 | 检索日期 | 支持的设计／主张 |
|---|---|---|
| [Khan Academy：Converting analog data to binary](https://www.khanacademy.org/computing/computers-and-internet/xcae6f4a7ff015e7d:digital-information/xcae6f4a7ff015e7d:representing-analog-data-in-binary/a/converting-analog-data-to-binary) | 2026-10-13 | 取样值、近似等级与二进制表示连续呈现；本课数值另行计算。 |
| [Georgia Tech DSP First：Sampling & Aliasing，Lecture 9](https://dspfirst.gatech.edu/archives/lectures/DSPFirst-L09-pp4.pdf) | 2026-10-13 | 连续波形与同一采样时刻对照，说明不同输入可给相同离散记录。 |
| [PhET：Teaching with simulations，Sound例](https://phet.colorado.edu/publications/physics%20teacher_finalwithpicts.pdf) | 2026-10-13 | 将一个位置的信号变化与时间曲线联系，说明横轴是时间而非声音传播距离。 |
| [Xiph.Org：Digital Show & Tell](https://wiki.xiph.org/Videos/Digital_Show_and_Tell) | 2026-10-13 | 区分离散样本与实际重建，避免把取样折线／台阶当成扬声器波形。 |
| [Analog Devices MT-001](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf)；[MT-002](https://www.analog.com/media/en/training-seminars/tutorials/MT-002.pdf) | 2026-10-12 | 均匀量化误差模型、带限采样条件与抗混叠边界。 |
| [Microsoft WAVEFORMATEX](https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/ns-mmeapi-waveformatex) | 2026-10-12 | 采样率、声道数、存储位宽与block alignment；44B开销另由本地fixture读取，不推广所有WAV。 |
| [MIDI Association：Overview](https://midi.org/about-midi-part-1overview)；[Microsoft Windows Media Codecs](https://learn.microsoft.com/en-us/windows/win32/medfound/windows-media-codecs) | 2026-10-12 | MIDI事件与波形编码区分；WMA家族不能笼统视作同一种有损方案。 |

`fixtures/size-check-8000-2s-16-mono.wav`复制自相邻正式包同名资产，仅用于可复现结构计数；未作为新的听觉实验。开场数值也来自该包保存的6秒PCM实例。原始音乐来自已有数字AAC/M4A再处理，不是首次ADC，不声称恢复原始模拟声音；公开再分发权限未在本次审查。
