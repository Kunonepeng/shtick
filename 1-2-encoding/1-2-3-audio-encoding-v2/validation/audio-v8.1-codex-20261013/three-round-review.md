# Audio v8.1.codex — 三轮视觉审查与交付记录

交付文件：`../../1-2-3-audio-encoding-v8.1.codex.pptx`，77页。任务日期2026-10-13；最终本地验收约23:24（Asia/Shanghai）。原v8为用户指定的GitHub版本，blob为`8ce6f8a6506de03d24ed0db849c97cb7e0f76d1c`，本地与GitHub一致。

- 原v8 SHA256：`c2b7a67ee9bbaa06af78fb0d3d6d3bdd6e0be16c9826a76fe86672389bb95181`。
- v8.1 SHA256：`d6e6676b68e958c21606df78a45027557eaa35971e1beba684a47c3314d18dbc`。
- 原文件及既有生成器、remote-demos-v7、历史验证记录均保留。本次不提交或推送GitHub。
- 三张新生成情境图：最终2页手机录音、68页文档备份/实时通话。精确波形、样本、码字、字节、计算、比例条和树均为原生可编辑对象。
- 六个知识树/总结复制页和一个欠采样证据复制页新增；原70个逻辑页全部映射保留。第一课时为最终1–37页，第二课时38–74页，75–77页可选。
- 本版本入口就是本记录；`course-design.qmd`限定本版本修订的教学逻辑，`final-slide-plan.json`列完整当前文字、阶段与Notes；未宣称替代历史发布包。

## 三轮优先级与关闭情况

P0：会使观察证据形成错误结论；P1：妨碍辨认核心关系、计算或揭示阶段；P2：影响阅读路径、一致性、间距或情境表达。每项在本轮修复后复查；后轮继续检查前轮没有退化。

| 轮次 | P0 | P1 | P2 | 结果 |
|---|---:|---:|---:|---|

| 1 | 1 | 7 | 4 | 全部pass |
| 2 | 0 | 4 | 4 | 全部pass |
| 3 | 0 | 4 | 5 | 全部pass |

## 第1轮：问题 → 修复 → 复查

前：`c2b7a67ee9bbaa06af78fb0d3d6d3bdd6e0be16c9826a76fe86672389bb95181`；后：`404239cc589fc732374f35a8d746adec5888235f9d5dfce6d7726dc985228b66`。页码指原v8逻辑页，最终页码参见映射。

| ID/等级 | 原页 | 问题 | 实际修复 | 修复后复查 | 状态 |
|---|---|---|---|---|---|
| R1-01/P0 | [13] | 1秒1Hz/2Hz的图实际画出4/8个点，计数证据与题意矛盾。 | 明确[0,1)区间，改画1/2个实际采样点及秒刻度。 | 独立核对点数、时刻和相同波形。 | pass |
| R1-02/P1 | all | 中文文本缺少显式East Asian字体；结构检查报401项未解析字体。 | 原生文字显式设置Alibaba Regular/Black及导出默认字体。 | 扫描所有字体声明并验证实际注册字体渲染。 | pass |
| R1-03/P1 | all cyan text | 白底青色#00B0F0文字仅约2.48:1对比度。 | 必要文字改用#007C9B，保留原生图形的青色语义。 | 对比度独立复算；关键码字、标签逐页检查。 | pass |
| R1-04/P1 | [8, 9, 12, 14, 23, 69] | 振幅标签贴近标题/分组名；时间标签与波形走线冲突。 | 调整标签位置、背景和叠放顺序。 | 全分辨率检查各轴与曲线、组名分离。 | pass |
| R1-05/P1 | [27] | 文件头说明与PCM示例挤在同一视觉行，难分辨归属。 | 说明按各自原生框的列位置重新排布。 | 两段说明分别位于文件头/样本列，无混读。 | pass |
| R1-06/P1 | [33, 38, 48] | 计算压在一条长式子中，样本计数、bit到byte和单位换算难定位。 | 将推导排为有单位的短步骤，保留题干位置。 | 独立计算三个结果并检查题目/答案页几何。 | pass |
| R1-07/P2 | all | 轨线略内缩且多个原生框/点有默认阴影。 | 轨线贴齐画布上下边，统一8pt高度，清除阴影。 | 检查画布与轨线边界、全部效果列表及渲染。 | pass |
| R1-08/P2 | all titles | 普通标题34/35pt与封面52pt不符合统一36/60pt层次。 | 标题统一36pt、封面60pt，必要处精简标题而不缩字号。 | 实际字体测量、共同基线与配对标题检查。 | pass |
| R1-09/P2 | [58] | 无损标签出现旧描边效果，正文孤立句号换行。 | 清除描边并精简同义描述。 | 无损/有损对照无孤立标点和字体效果。 | pass |
| R1-10/P2 | [68] | 退出条三个问题的垂直间距不均，第二/三项挤在一起。 | 三项等间距排列。 | 三项坐标间隔一致，学生可逐项阅读。 | pass |
| R1-11/P1 | [18] | 图把等级编号3画成幅度代表值，尽管规则说明代表值可取3.5。 | 用[0,8)区间图分别标原值3.71、代表值3.5与等级L3。 | 独立检查区间、幅度位置和标签的不同含义。 | pass |
| R1-12/P1 | [30] | 3bit算成3Byte的图缺少连续打包条件，容易与16bit实际PCM存储混读。 | 在图上明确3bit连续打包教学模型与实际PCM的边界。 | 24bit/3Byte算式与模型条件同时可读，Notes保留存储位宽条件。 | pass |

证据：`round1-issues.json`、`round1-audit.json`、`round1-after-geometry.json`、`round1-measurements.json`、`round1-render/`与`round1-montage.png`。

## 第2轮：问题 → 修复 → 复查

前：`404239cc589fc732374f35a8d746adec5888235f9d5dfce6d7726dc985228b66`；后：`12774e2d926ca4bc079a684e6f5af2d07ce43ec96ce6d3f8df4ddb8f25271a11`。页码指原v8逻辑页，最终页码参见映射。

| ID/等级 | 原页 | 问题 | 实际修复 | 修复后复查 | 状态 |
|---|---|---|---|---|---|
| R2-01/P2 | [2, 65] | 抽象的文字/图像/声音与备份/通话场景缺少可见情境。 | 加入三张生成情境插图，保留原生标题、问题与比较标准。 | 查验图片比例、位置、非事实用途及提示词出处。 | pass |
| R2-02/P2 | [19] | 十列样本/等级/码字缺少一个连续观察焦点。 | 红框标出第一列1→3→011。 | 框与三行同列，码字值未改。 | pass |
| R2-03/P2 | [26] | 16bit存储只显示两行0/1，Byte分组关系不直观。 | 每行标8bit=1B，总计2B。 | 独立点数16与字节2。 | pass |
| R2-04/P1 | [41] | 并列音轨与声道图没有汇合/分流，容易误读一一对应。 | 原生绘制两轨汇入混音，再分到L/R。 | 走线无交叠文字，两轨共同混音。 | pass |
| R2-05/P1 | [43] | 双/单声道只有空框，无法直接数同一时刻的样本。 | 同三个时刻分别画6/3个样本。 | 核对共同时间与2:1数量关系。 | pass |
| R2-06/P1 | [56] | 1000B→17B/1011B仅文字，体量差异不能直接比较。 | 按同一比例尺绘制原始/压缩条与多11B部分。 | 独立检查17/1000、1011/1000比例与zlib示例。 | pass |
| R2-07/P1 | [31] | 容量公式因素并列，样本计数与每时刻字节数的乘法关系不清。 | 原生分组两部分，黑色乘号连接。 | 因素、存储位宽与单位完整；结果不含结构开销。 | pass |
| R2-08/P2 | [44] | 图像/音频比较只有行名，列归属需猜测。 | 增加空间采样/时间采样列名。 | 列标题与对应数据对齐。 | pass |

证据：`round2-issues.json`、`round2-audit.json`、`round2-after-geometry.json`、`round2-measurements.json`、`round2-render/`与`round2-montage.png`。

## 第3轮：问题 → 修复 → 复查

前：`12774e2d926ca4bc079a684e6f5af2d07ce43ec96ce6d3f8df4ddb8f25271a11`；后：`d6e6676b68e958c21606df78a45027557eaa35971e1beba684a47c3314d18dbc`。页码指原v8逻辑页，最终页码参见映射。

| ID/等级 | 原页 | 问题 | 实际修复 | 修复后复查 | 状态 |
|---|---|---|---|---|---|
| R3-01/P1 | [34, 68] | 两课时总结只有分散问答，缺少可逐步累积的关系树。 | 保留三问与退出条，增加六个原生总结/知识树构建页。 | 按0→1→2→3、3→4→5检查；原70页保留。 | pass |
| R3-02/P1 | [69] | 欠采样拓展图没有实际采样点，无法看到两个波形如何共享观测值。 | 先显示三个观测点，再复制揭示两个不同数学波形通过相同点。 | 独立复算1Hz/3Hz余弦在0、0.5、1秒同为1、−1、1，静态揭示。 | pass |
| R3-03/P1 | [9, 47, 61] | 若干预测/练习页以彩色结论或方法提示提前引导答案。 | 保留必要题意；方法与答案移至后续证据及Notes。 | 题干/配对几何不变，先独立作答后揭示。 | pass |
| R3-04/P1 | [57, 70] | 压缩一定用更少bit的措辞与B增加11Byte的证据不一致。 | 将减少数据量明确为目标，保留具体数据可能增大。 | 视觉核心结论不再承诺所有输入均变小。 | pass |
| R3-05/P2 | [18] | 代表值3.5只有底部解释，蓝点缺少直接标签。 | 蓝点旁加代表值3.5标签，区分原值和等级。 | 标签和引线不穿过量化编号。 | pass |
| R3-06/P2 | [43, 44] | 时刻标签贴住样本框；比较表分隔线贴近文字。 | 时刻上移，分隔线置于行间空白。 | 全分辨率检查标签/框及行分隔间距。 | pass |
| R3-07/P2 | [45, 55, 60] | 部分原生图表和演示框逼近右边界。 | 在不改字体和样本数的前提下调整几何到安全边距。 | 图表等比宽高、相同格数与最终边界。 | pass |
| R3-08/P2 | [59] | 格式分类呈四块散列表，类别关系仍需读长说明。 | 重排为归档格式、音频编码、容器的原生比较表。 | 类型与例子对应，WAV/MP4不被误标固定压缩算法。 | pass |
| R3-09/P2 | [13, 29] | 秒刻度贴近轴名称；量化位数与实际存储位宽的视觉称呼未统一。 | 分离秒单位与刻度；容量页直接写存储位宽条件。 | 计数图与PCM公式使用一致单位和存储条件。 | pass |

证据：`round3-issues.json`、`round3-audit.json`、`round3-after-geometry.json`、`round3-measurements.json`、`round3-render/`与`round3-montage.png`。

第一轮全70页逐页全分辨率查看；发现58页Black文字在本机渲染中有残留形状后，重建为Alibaba Regular比较标题并再次全页渲染，确认缺陷消失。第二轮全70页渲染，9个变更页逐页查看，另61页PNG与第一轮逐字节一致。第三轮全77页渲染，16个原页变更及7个新页逐页查看，其余54个原页PNG与第二轮逐字节一致。每轮查看全景蒙太奇；最终图片、图表、练习对和全部树构建另作单页检查。相同像素的页沿用已完成的全分辨率检查，比较记录可复核。

## Deck acceptance record

| Check | Result / evidence |
|---|---|
| Slide order, Q IDs, reveal stages match plan and course-design.qmd | pass：77页映射；70个原页保留；六组练习与两段树顺序检查。当前目录原无QMD，本版设计补充在本记录旁。 |
| Question slides contain no premature answer or teacher-only text | pass：六个练习题干稳定；9/47/61去除提前提示；34/72总结先收学生解释；75先给点、76才补曲线。既有短解释页仍按证据页处理。 |
| Evidence readable and red focus identifies intended target | pass：采样点数、量化区间/代表值、第一列、同一时刻L/R、混音汇合/分流、同尺度比例条与树新分支人工核对。 |
| Every slide rendered, montage/dense slides inspected | pass：1920×1080全套图片，三轮全景与逐页/像素一致性检查；最终等同round3候选文件的字节副本。 |
| Geometry, rails, fonts, question/answer stability | pass：最终2549项独立检查；602文本组实字体宽度测量无溢出；几何0 findings/0 warnings；拉丁/中文/复杂文字显式Alibaba字体，正文字号未以auto-fit缩小。 |
| Speaker Notes, technical claims, dates, sources | pass：全部页具完整目的与教师逐字稿；新图精确提示词、模型边界与教师来源；PCM、视频、采样/代表值、zlib结果独立复算。 |
| Final PPTX inspected in WPS / PowerPoint | unverified：本次使用@oai/artifact-tool2.8.93导入/渲染；未操作目标WPS或PowerPoint。不能由本机渲染推断目标应用换行、Notes或字体。 |

| 验证层 | 结果与限制 |
|---|---|
| 教学对齐 | pass（本轮范围）：原例值、六组练习、A/B/C/D演示关系保留；逐步树及图示条件写入版本绑定设计；完整课程包未被重新发布。 |
| 结构/原生性 | pass：最终器完整性、导入、布局与字体声明通过；3张PNG嵌入，其余技术证据原生；没有用动画承载唯一含义。 |
| 渲染/人工检查 | pass：记录上述逐页与像素比较方法，字体在macOS可用并人工核对中文/拉丁/数字/符号；原生字体的目标应用显示仍unverified。 |
| Notebook执行 | unverified（范围外）：remote-demos-v7未改，未重跑角色Notebook或课堂浏览器。本轮只独立复算与图相关的确定值。 |
| 课堂应用 | unverified：WPS/PowerPoint/Windows远程JupyterLab没有本轮实测。 |
| 课堂条件 | unverified：投影、扬声器、学生完成情况与90分钟实测节奏未验证。不能称为已完成课堂验收。 |

## 文件角色、编辑点与再生成

| 文件/目录 | 角色 |
|---|---|
| ../../1-2-3-audio-encoding-v8.pptx | 不变的GitHub输入/历史身份 |
| ../../1-2-3-audio-encoding-v8.1.codex.pptx | 本次指定交付的独立版本 |
| course-design.qmd、final-slide-plan.json | 本版教学/显露设计与原逻辑页映射 |
| sources/build.mjs | 原生编辑生成器；stage1字体/几何与图示修复，stage2图像/关系图，stage3精修与复制构建 |
| sources/build-round1.mjs、build-round2.mjs | 每轮结束时的生成器快照 |
| snapshots/round1-after.pptx、round2-after.pptx | 已审查的中间候选身份；不作为课堂交付文件 |
| ../../assets/generated/audio-v8.1.codex/ | 三张原始生成PNG与provenance.json |
| ../../assets/generated/image-prompts.md | 生成前记录的完整生产提示词与工具文件标识；相同提示词亦在对应Notes中 |
| baseline-render/、round1/2/3-render/及*-montage.png | 完整视觉审查证据 |
| sources/audit.py、measure.mjs、qa.py | 独立数值/结构、实际字体测量、几何与比较/蒙太奇检查 |
| finalizer-validation.json | 最终PPTX完整性、字体声明、尺寸与重新导入检查；不能证明WPS实际显示 |

在隔离临时目录再生成，避免覆盖交付或历史文件：复制sources中的脚本；复制baseline-inspection.json，以及baseline-render中的layout.json文件到临时目录相同名称目录；将原v8复制为baseline.pptx；把三张生成PNG复制到images/；复制image-prompts.json。Node环境需@oai/artifact-tool2.8.93及@napi-rs/canvas0.1.100，并使脚本能够解析这些模块。构建字体是Alibaba PuHuiTi3.0 Regular/Black；本次脚本记录当前macOS字体位置，迁移构建机时调整字体路径即可，不是课堂运行依赖。Python3.12及Pillow用于检查与蒙太奇。native字体默认值的OOXML修补只补全主题/母版/Notes默认字体，已在每轮导出后执行，记录于patch_font_defaults.py；再次生成不会丢失。

```sh
node build.mjs 1
node render.mjs round1-after.pptx round1-render
python3 qa.py 1
node build.mjs 2
node render.mjs round2-after.pptx round2-render
python3 qa.py 2
node build.mjs 3
node render.mjs round3-after.pptx round3-render
python3 qa.py 3
```

写入范围是该临时工作目录的round候选、plan、inspect、render和audit等文件；既有临时候选会重写，执行前保留必要人工编辑。工具自动ID可能变化，重新生成须复查当前候选，不能沿用旧SHA或旧验收结果。交付PPTX已嵌入图片，课堂仅携带PPTX即可看到静态视觉；实时演示仍需既有remote-demos-v7及其资产/服务。新增总结页要求教师先收回应再翻页，不依赖动画。新增树尚未同步到既有Notebook/Reveal，课堂兼容时在PPT中完成这些总结；全包同步不在本次视觉修订范围，保留为后续工作。

## 来源与计算证据

检索日期均为2026-10-13；URL仅放教师材料与Notes。

| 来源 | 支持的具体修订 | 限制 |
|---|---|---|
| [Microsoft WAVEFORMATEX](https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/ns-mmeapi-waveformatex)，2021-04-02，nBlockAlign/nAvgBytesPerSec/wBitsPerSample | PCM每时刻字节数、采样率、声道、存储位宽条件 | 非PCM不套同一公式；容器位宽不一定等于有效精度。 |
| [Microsoft RIFF overview](https://learn.microsoft.com/en-us/windows/win32/xaudio2/resource-interchange-file-format--riff-)，2021-01-07，fmt/data chunks | PCM样本数据与WAV结构区别 | 图是结构示意，不声称全部WAV只有固定44B文件头。 |
| [MDN Media container formats](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Containers)，MP4/WAV/codec关系 | 格式分类表与容器边界 | 本轮不据此承诺具体浏览器兼容性。 |
| [RFC2361 WAVE registry](https://www.rfc-editor.org/rfc/rfc2361)，1998 | WAV可承载不同编码，不固定等于PCM | 历史登记资料，不作为当前产品行为表。 |
| [Python3.12 zlib](https://docs.python.org/3.12/library/zlib.html)，compress/decompress | 可复算实验方法 | 17/1011B是本次fixture与默认zlib设置的结果，不是普遍压缩率。 |

独立计算在audit.py：16000×5×2×8÷8=160000B；48000×60×2×16÷8=11520000B≈10.99MiB；480×320×24÷8=460800B/帧，25×600=15000帧，总量6912000000B≈6.44GiB；17/1000与1011/1000按500px对应1000B绘图。采样点坐标、量化边界与cos例值也从实际原生对象复核。无损恢复逐字节比较；不依赖听感或画面相似。

当前所有29项视觉问题已关闭。课堂应用/条件与伴随材料同步边界仍如上标为unverified或范围外。
