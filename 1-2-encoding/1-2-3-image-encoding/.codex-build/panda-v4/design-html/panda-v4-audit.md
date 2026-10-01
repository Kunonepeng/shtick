# 熊猫v4：新版AGENTS审查、实施与验收

日期：2026-10-01。唯一教学入口：[course-design.qmd](course-design.qmd) C0／C6。当前交付：[panda-v4 PPTX](exports/1-2-3-image-encoding-panda-v4.pptx)，77页、1,000,022 bytes。

SHA-256：`c88c4e3666873045085a0f23748a1cb39cd666cd6c1b8506198acb0c531c1237`。

本机教学／计算／结构／渲染验证已通过，课堂应用与教室条件仍有未验证项。没有提交、推送或发布。45分钟为预算，未记录真实班级成绩或实测节奏。

## 依据、盘点与版本保留

读取仓库最新版AGENTS.md、slide-style-guide.md、课程入口／设计、历史审查、源数据、生成／检查代码及整个课程包。无适用的 lesson-local AGENTS.md。当前不创建或插入生成图片，因此图片生成提示词流程不适用；不把用户提供的熊猫插图声明为自行生成素材。采用presentations技能的原生新增页、导出与finalize校验，保持本项目既有视觉规范。

起始工作区干净，确认设计指定的是63页panda-v3，不按编号猜测版本。全目录盘点包含隐藏构建目录、输出、历史审查与ignored／untracked状态；见`.codex-build/panda-v4/inventory-before.json`，326个现有文件。修改后320个字节未变，6个现有课程文件按授权更新，无缺失；见`preservation-check.json`。PPTX历史交付、原始PDF／ZIP／JPG、旧生成器、旧检查报告及旧渲染全部保留。根`_quarto.yml`仅修正本课的两个过期-v2渲染入口，未改其他课程。

v3种子SHA-256：`eb85809ebd683e8539624e6873b74cfb376c63d3b37593204757c47eda1cf7f2`。v4保留v3的63个学生可见slide XML和原有media字节，新备注与14个原生页由当前源生成。历史设计、Reveal原稿及旧取整Demo数据分别保存在`references/course-design-panda-v3.qmd`、`references/slides-pre-panda-v4.qmd`、`references/panda-samples-pre-v4.json`；与更新前字节／Git对象核对一致。

## 有证据的发现与已实施改进

|位置／证据|教学或复现影响|实施结果|
|---|---|---|
|v3设计及63页计划没有知识树节点／总结build|新规要求的证据总结与渐进关系没有可执行载体|C4a共享模型定义7枝、关系、Q、提示与4个检查点；新增11个原生树页，只揭示已建立知识，旧节点固定，红框＋“新学”＋编号提供非颜色线索|
|旧C1主要列目标，Q22仅课后作业|不能从志愿者口答证明全体学生掌握，缺课堂内新参数迁移|加入目标—活动—证据—成功标准与误解回应；新增E1独立60秒、先收答后两次揭示；活动单A／B／E1和教师答案分发分层|
|主Q已有深度，但独立子任务散在段落中|容量、表示方案、连续性等独立推理的思考起点不够显式|保留Q1–Q21全部原解释，补形成结论和8个稳定子任务核对；未增加新的主Q|
|旧C3时间段未显式容纳树总结、累计切点和失败阈值|按新增要求授课易占用独立作答时间|重算45分钟，默认跳过6个可选页；纳入思考／反馈／总结，设置23／29／35分钟切点；Tk在加课时／课后，失败30秒回PPTX|
|旧slides.qmd为历史草稿；根入口仍指不存在的-v2路径|参考材料和真实生产版本混用，无法依入口复现|旧稿字节归档；新Reveal由77页计划与最终渲染生成，嵌入全部资源、保留同阶段备注，PPTX继续为正式课堂格式|
|旧build-panda-v3.mjs／finalize路径含-v2绝对目录|旧生成源在当前目录失效，人工更新不可可靠再现|课程相对路径生成器＋不可变原生模板＋明确合并脚本；构建／覆盖／依赖记录见下文|
|Demo先把区域平均RGB转整数，而设计规定未取整均值判最近色|一般输入下可能改变最近颜色；此前历史界面说明不能当当前验收|由原JPEG重建未取整fixture，显示才近似；独立复算当前三幅矩阵与旧整数fixture差异均0，明确这不构成普遍等价；English comments／docstrings／开发者消息同步|
|初次本机LibreOffice试渲染出现替代字体|不能拿外观或字体声明当指定字体渲染证据|拒绝试渲染证据；使用显式Fontconfig后刷新最终77张图与7张montage，PDF字体仅Alibaba Black／Regular|
|完整活动单后段给出Q18码字，与前面的Q7-read答案相同|整份提前发会泄露读码练习，退出题参数也会提前出现|拆成A／B／E1学生视图；Q6／Q18／第74页分发；完整母版仅教师准备，所有阶段仍无教师答案|
|首次新Reveal自动增加封面／空白段|与PPTX阶段位置错位|生成源改用pagetitle、把页标记放入对应段；重新渲染并检查77背景／77备注／77阶段|

## 独立数据与技术核对

生成数据使用NumPy；检查器另用Pillow逐像素整数通道求和，不复用reshape／mean代码。还直接读取当前PPTX原生像素矩形，不能由两份JSON相等推断课件正确。

- 同一零起始裁切：`(280,100,288,288)`；8×8每块36×36、16×16每块18×18；先求RGB均值，再按平方距离量化，平局取小编号。固定位置／样本后四色改六色；相同四色后8×8改16×16。
- 当前三幅矩阵与设计附录、共享数据、实际原生色块一致。16×16第10行第13列均值`(78.25,73.3148148148,68.3981481481)`；四色编号0、六色编号4。
- 在256个区域均值、3通道上的RGB均方误差：281.166316…→192.270917…，减少31.62%。它是该数字重处理模型的距离指标，不是视觉质量或相机性能评分。
- 最短固定码：4色2bit、6色3bit；三轮128／512／768bit＝16／64／96B。24位RGB为三个8位通道，不含alpha；原JPEG解码像素`(422,230)`为`(138,179,111)`，二进制`10001010 / 10110011 / 01101111`。
- Q16：500×333×24÷8＝499500B，÷1024≈487.79KiB。Q21必须同时检验颜色容量与数据量，选B、D；E1的5色最少3bit、12×10×3÷8＝45B。
- Q18实际原生4×2、2×4及结论页4×2三处排列，按从左到右／从上到下读回均得到`11 11 01 00 00 01 11 00`。检查器直接用原生格子的RGB填充映射，不只拼接预写字符串。
- 解码目标是已记录的量化编号与排列；不声称恢复采样前连续信息。数字JPEG区域再次求均值不等同真实物理采样，也未在线性光空间模拟相机。
- 理想连续码字不含头部、调色板、行对齐、补位或压缩。PNG实际索引位深度允许1、2、4、8，5色索引PNG至少4bit；E1的3bit只是最短固定码模型，不能据45B推完整PNG大小。此限定放在教师材料。

复算及4种Demo参数状态证据：`.codex-build/panda-v4/technical-check.json`。`--self-test`通过，但不证明Tk窗口布局。

## 一手来源与素材来源

均于2026-10-01检索。技术参考只放教师材料，学生题面保留推理所需条件。

|来源／版本／章节|支持范围与限制|
|---|---|
|[Microsoft Bitmap Storage](https://learn.microsoft.com/en-us/windows/win32/gdi/bitmap-storage)，页面更新2022-11-19|位图信息、颜色表、像素数据与文件header的关系；仅用来说明完整文件计数需格式条件，不把BMP字段泛化为所有图像|
|[Microsoft BITMAPINFOHEADER](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapinfoheader)，biWidth／biHeight／biBitCount|GDI DIB尺寸、位数与方向约定；视频文档有额外限定，Q18采用显式教学读取规则，不宣称所有格式相同|
|[Pillow Concepts](https://pillow.readthedocs.io/en/stable/handbook/concepts.html)，当前12.3.0文档，Modes／Coordinate system|RGB三通道、P调色板、零起始坐标；本机实际Pillow12.2.0，fixture已按本机独立验证；解码器舍入可能不同|
|[NIST Binary Prefixes](https://physics.nist.gov/cuu/Units/binary.html)，Examples and comparisons with SI prefixes|1byte＝8bit、Ki＝2¹⁰、Mi＝2²⁰；B与KiB不混用，不将KiB写成十进制kB|
|[W3C PNG第三版](https://www.w3.org/TR/2025/REC-png-3-20250624/)，Recommendation 2025-06-24，§11.2.1表12、§11.2.2–4、§10|索引色合法位数、调色板与chunk、压缩；不能把本课最短3bit模型直接当PNG像素布局|

熊猫源图为用户提供的角色插图，原文件不变：SHA-256 `f6679d0c7f119ec953e44be6912f03b2bd35bd032e27579241562b1bb46b5186`。变换记录为C4裁切、均值、量化、既有近邻放大。未创作生成图片，也未推断该角色素材已获公开再分发授权；当前仅本地课程交付，无发布行为。来源PDF／ZIP保持原样，历史课程事实保留在原课复刻记录，历史报告的pass不适用于v4。

## 逐Q语义对应

`.codex-build/panda-v4/slide-plan.json`是完整77页计划：Q／独立task ID、阶段、可见／暂缓内容、备注、证据、焦点、树检查点和可选标记。所有major Q及独立推理先问题页，静态重复后才揭示；37个相邻问答／build配对验证。下表给教师导航，Reveal与PPTX为一对一阶段，并非仅ID数量相同。

|Q／检查点|PPTX页|Reveal|演示／活动／树与语义|
|---|---|---|---|
|Q0|1|同页次／同揭示阶段|教师检查前置知识；只收答案|
|Q1|2、3|同页次／同揭示阶段|预测放大结果，观察同一眼部像素|
|Q2|4、5|同页次／同揭示阶段|打印再拍摄思想实验，区别数字插图与物理光|
|Q3|6、7|同页次／同揭示阶段|8×8位置数与二维排列；T1采样枝|
|Q4|8、9、10|同页次／同揭示阶段|同一样本均值到最近有限代表色；T1量化枝|
|Q5|11、12|同页次／同揭示阶段|四色码表／最短固定2位；T1编码枝|
|Q6|13、14|同页次／同揭示阶段|活动单①第四行编码；T1总结|
|T1|15、16、17、18|同页次／同揭示阶段|活动单①，先学生总结，再逐枝新增采样、量化、编码|
|Q7|19、20、21、22|同页次／同揭示阶段|增加位置，颜色固定；Q7-read局部读码；D-P1／D-P3可选|
|Q8|23、24|同页次／同揭示阶段|可选位图／矢量对照；不属于默认45分钟路径|
|Q9|25、26、27、28、29|同页次／同揭示阶段|样本固定，增加调色板颜色；Q9-capacity；D-P2可选|
|Q10|30、31、32、33|同页次／同揭示阶段|比较三轮控制变量；Q10-capacity容量上限|
|Q11|34、35|同页次／同揭示阶段|三轮像素数据bit；为T2提供算式证据|
|Q12|36、37|同页次／同揭示阶段|bit→B与KiB；活动单T2总结；D-P此后才允许启用|
|T2|38、39|同页次／同揭示阶段|活动单T2，先列式证据，再新增像素数据量|
|Q13|40、41|同页次／同揭示阶段|两色／16／256色容量与同一公式|
|Q14|42、43、44、45、46、47|同页次／同揭示阶段|Q14-formula可选；Q14-rgb／Q14-compare；T3颜色表示枝|
|Q15|48、49、50|同页次／同揭示阶段|活动单②R位权；G／B只核对固定8位|
|Q16|51、52、53|同页次／同揭示阶段|活动单②独立数据量；完整文件边界|
|Q17|54、55|同页次／同揭示阶段|已有像素放大与新采样的区别|
|Q18|56、57、58|同页次／同揭示阶段|活动单③独立画、另一排列、反向读码；T3解码枝|
|T3|59、60、61|同页次／同揭示阶段|活动单③，先解释／读回证据，再新增颜色表示、解码|
|Q19|62、63、64、65|同页次／同揭示阶段|时间／空间分类可选；Q19-continuous保留；连续量模型|
|Q20|66、67|同页次／同揭示阶段|有限位置／等级和多个bit的离散表示|
|Q21|68、69、70、71|同页次／同揭示阶段|三步骤归纳；Q21-budget活动单④双约束；T4边界枝|
|T4|72、73|同页次／同揭示阶段|活动单④，先完整解释，再新增数字化边界；完整树此时才出现|
|E1|74、75、76|同页次／同揭示阶段|活动单⑤，12×10／5色／50B新参数；独立收答后两次反馈|
|Q22|77|同页次／同揭示阶段|作业；答案仅教师材料，不冒充课堂退出评价|

默认可选页为23–24、42–43、62–63；跳过整组提问／揭示。主路径不切换软件。T1为15–18、T2为38–39、T3为59–61、T4为72–73，E1为74–76，Q22为77。树原生文字／形状／连接线可编辑，题面／旧枝稳定；Reveal背景是最终版图像，阶段一致但不可在浏览器中编辑原生对象。

## 文件角色、构建顺序与覆盖规则

课程入口仍是course-design.qmd，无第二个README权威。当前PPTX、活动单、参考HTML和证据路径由C6指定。活动单母版为教师源，由split脚本生成A／B／E1三份Markdown，再由Quarto生成分发用HTML；不提前发母版、B或E1。`pptx-slide-plan.md`、`panda-deck-design.md`、旧quality-report及旧`.codex-build/*`均为此前版本记录，不能当当前操作指令。课程目录当前无IPYNB／教师学生Notebook，v4也未采用Jupyter；相关kernel／JupyterLab验收不适用。将来若改为Notebook主流程，需要先补教师／学生两版及完整kernel／UI验收，不能沿用本次代码检查。

构建依赖：Node＋@oai/artifact-tool；Python＋Pillow＋NumPy；presentations finalize检查器；Quarto；LibreOffice＋pdftoppm；两份指定Alibaba字体。课堂主路径只需PPTX＋字体＋WPS／PowerPoint，活动单A／B／E1分阶段打印件；离线HTML为参考，不是强制课堂依赖。D-P整目录复制，Python标准库Tk，课前self-test与实际窗口验收后才启用。

```bash
# Run from the lesson directory. Preserve human changes before regenerating outputs.
python3 scripts/rebuild-panda-data.py
python3 scripts/split-activities-panda-v4.py
node scripts/build-panda-v4.mjs
python3 scripts/assemble-panda-v4.py
python3 scripts/validate-panda-v4.py
PRESENTATIONS_SKILL=/path/to/presentations BUILD_PYTHON=python3 node scripts/finalize-panda-v4.mjs
python3 scripts/render-panda-v4.py --font-dir /path/to/Alibaba-font-files
quarto render course-design.qmd --output-dir .codex-build/panda-v4/design-html
quarto render slides.qmd --output-dir exports/reference-panda-v4
quarto render activities/panda-v4-student-a.md --output-dir exports/activities-panda-v4
quarto render activities/panda-v4-student-b.md --output-dir exports/activities-panda-v4
quarto render activities/panda-v4-student-exit.md --output-dir exports/activities-panda-v4
python3 scripts/validate-reference-panda-v4.py
python3 scripts/validate-activities-panda-v4.py
```

`split`覆盖三个学生Markdown视图；`rebuild`覆盖当前data.json与Demo fixture，`build`覆盖新增页／计划，`assemble`覆盖candidate、逐页计划、assembly记录和slides.qmd，`render`覆盖当前77图片／PDF／montage。finalize拒绝覆盖已存在的正式PPTX；若已有交付需保留它，选择明确的新版本路径并同步入口，不能直接覆写本版。validate不改课堂PPTX；比较重新生成candidate与当前正式版的全部OOXML字节，ZIP时间不同可以导致容器hash不同，但所有成员完全一致。没有手工patch正式输出；必要的notes和插页变换都在合并源中。

`.codex-build/panda-v4/`和`exports/`未被仓库忽略；当前新文件可纳入版本管理但未提交。当前源代码的实现注释、标识符、docstring及开发者消息为英文；中文仅作教学题面、notes、界面或教学共享数据。旧生成器的中文实现注释仍保留历史身份，不参与当前构建；重启它们需要先整理。课程局部`.gitignore`只排除`.quarto/`、Quarto临时IPYNB和Python缓存。已有node_modules链接保持原状；`ARTIFACT_MODULES`可显式配置可访问依赖。局部_quarto.yml隔离本课渲染，根网站全站构建没有执行。

本机实际值：Node 24.19.0（随Codex运行时），Python 3.12.9、Pillow12.2.0、NumPy2.4.6、Quarto1.10.18。finalize用随技能Python3.12.14运行时；presentations路径为`/Users/chran/.codex/plugins/cache/openai-primary-runtime/presentations/26.921.10847/skills/presentations`，构建Node位于`/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node`，校验Python位于同运行时`dependencies/python/bin/python3`。这些属于构建记录，不写入课堂运行指令。`--font-dir /Users/chran/Library/Fonts`，要求`AlibabaPuHuiTi-3-115-Black.ttf`与`AlibabaPuHuiTi-3-55-Regular.ttf`。Quarto在macOS使用用户Library/Caches的Sass数据库；首次沙箱受限，允许正常缓存写入后渲染成功。zh-CN翻译警告不影响输出，浏览器检查中文内容正常。

## Deck acceptance record（风格指南§21.3）

|Check|Result／evidence|
|---|---|
|Slide order, Q IDs, and reveal stages match the plan and course-design.qmd|pass；77页计划、独立子任务、四树检查点、E1和逐Q语义表；技术检查读取正式版|
|Question slides contain no premature answer or teacher-only text|pass；逐页可见内容与stage notes审阅，T1无未来枝，E1收答后揭示；教师来源和参考在notes／design|
|Evidence is readable and each red focus mark identifies its intended target|pass（当前渲染尺度）；逐页全尺寸检查；灰阶后排投影仍unverified|
|Every slide was rendered; montage and dense slides were inspected|pass；final-render.pdf、render/slide-01…77.png、montage-1…7.jpg；visual-inspection.json记录全部页；最终版hash绑定|
|Geometry, rails, fonts, and question/answer stability passed structural checks|pass；77页canvas、rails、1009 native font script assignments、37组geometry／题面比较，结构finding0；渲染PDF只含指定Alibaba55／115|
|Speaker Notes, technical claims, dates, and sources were checked|pass；77页实际notes与计划一致，完整问题／目的开头、stage scripts不同；独立技术复算与上方一手来源；实体WPS备注显示另验|
|Final PPTX was inspected in WPS / PowerPoint|unverified；WPS已安装，但当前工具无原生应用UI通道；PowerPoint未安装；须在目标教室逐页／notes检查，PDF不能替代|

## 分层证据与待验收动作

|层次|状态／证据|边界／下一步|
|---|---|---|
|教学对齐|pass；设计字段／子任务核对、slide-plan、逐Q表、四树阶段、独立评价与预算|该结论为材料审查，不代表学生学习效果实测|
|结构|pass；validation.json（77页、关系finding0、几何finding0、font policy、正常正文≥22pt、仅两处16.5pt“概念示意”辅助标签、14 native tables、artifact import77）、technical-check.json|通用table加总规则对本课表不适用，其pass不证明公式；公式由独立脚本复算|
|渲染／逐页视觉|pass；LibreOfficeDev26.8.0.0.alpha0 build 2c87e51eeaa2b413ff4ae097b2705eea1995d8e5；77张1601×900、7montage；render-fonts.json／visual-inspection.json|替代字体试渲染不作通过证据；实际WPS／PowerPoint另验|
|代码执行|pass；Demo self-test、4种参数状态、独立像素求和／量化／native roundtrip|不代表Tk按钮、键盘、窗口布局或Windows runtime已实机验证|
|Notebook执行|不适用（未执行）：当前路径无Jupyter和Notebook|未声称fresh kernel、widget或JupyterLab检查通过；不得改用Notebook而沿用本记录|
|Reveal／活动单|pass（渲染与本机浏览器）；77背景／77notes与PNG hash逐页核对，阶段导航及A／B／E1学生题面／作答空间检查，实际HTML检查晚出码字／参数未提前给出|参考是静态图像build，无新增互动保证；实体打印仍unverified|
|课堂应用|unverified；WPS／PowerPoint notes与字体布局、Windows Tk窗口／控制|开目标应用检查全部布局、notes、四色辨识、参数操作；Demo未验收则沿用PPTX主路径|
|教室条件|unverified；投影／后排辨色、活动完成与实测节奏；音频／网络不适用|试讲记录12／23／29／35／42／45分钟检查点、E1独立收答、错误类别与超时，不能把预算填成实测|

最终交付以该hash的PPTX为准，所有版本绑定证据在`.codex-build/panda-v4/`，包括reference-check.json、activity-check.json、preservation-check.json与sources-manifest.json。最终git diff --check通过；新文本亦检查尾随空白。无法开展的实机／教室验收保留unverified；完成后应记录环境、日期、问题／修复和重新验证证据，再判定课堂就绪。
