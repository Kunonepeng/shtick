# 音频数字化课堂包

本文件是课程入口。45分钟；教师操作，学生纸笔与讨论。正式课堂课件为 **`exports/1-2-3-audio-encoding-v4-final.pptx`，62页，Q1–Q19**。新版增加四项独立推理的问答阶段、Q15逐层计数和四次知识树总结；这些翻页不分别增加讨论回合。时长是设计预算，未实测。Windows + WPS + JupyterLab + 投影／音箱是目标环境，本机验证不能代替该环境验收。

## 上课入口与分发

1. WPS打开上述v4 PPTX。每问先停在问题页，按提问稿等待作答；随后翻到复制的揭示页。树更新前先听学生总结与证据。所有页面有分阶段Speaker Notes。PowerPoint为替代应用，尚未验收。
2. 从**本课程目录**启动JupyterLab，只打开`notebooks/staged/`中的当前文件，仍由教师操作。按下面顺序逐单元运行；准备代码在未投影时运行，进入当前题面后再投影。不要Run All。主问题结论形成后才打开`-B`文件。完整`demo-lab-teacher.ipynb`供备课，完整`demo-lab-student.ipynb`供阅读／试跑；两者都包含未来题面，整份不投影。
3. 分发三份活动材料：A在Q3，B在Q10主问题揭示后、Q10-B前，exit在Q19。打印`exports/reference-v4/student-activities-{a,b,exit}.html`。`student-activities.qmd`是教师组合源，整份不提前发；答案与评分在`student-activities-teacher.md`。
4. 课前试听A/B音乐（各6秒）与纯音基准（3秒），固定系统和播放器音量。基准听不到、音乐差异听不清，改用题目条件、误差图和字节证据；不要把听不见解释成绝对零。演示异常持续30秒即用备用；不现场安装或长时间排障。
5. 交付Notebook均无输出／执行计数。运行后重新放映前清除输出、重启内核并回到当前文件。source_hidden只是一项元数据：本机JupyterLab实测折叠仍显示首行；本次首行使用中性函数名，音频文件名留在共享实现中。投影时收起文件浏览器，确认标题、参数、同屏对照和播放器完整可见。

|当前阶段|文件与证据|静态／备用与能力损失|
|---|---|---|
|Q1|`opening-student.ipynb`，匿名A/B播放器|预制WAV，保持A/B标签；不显示参数文件名|
|Q3／D1|`D1-student.ipynb`：曲线→预测→12点|PPTX p6–7；HTML `?stage=D1`可动画。静态失去重新选择取点数|
|Q8／D2|`D2-student.ipynb`：已知参数对照与纯音基准|PPTX p23–24；HTML `?stage=D2`为可选音乐对照。不开场绑定A/B身份|
|Q8-B／D2-B|`D2-B-student.ipynb`：先代入6kHz条件，再运行过滤结果|p25–26；HTML `?stage=D2-B`结果初始隐藏；预制纯音不能改频率|
|Q10／D3|`D3-student.ipynb`：同一48时刻，同屏2／4bit|p29–30；HTML `?stage=D3`改位数后须重新揭示，试听也按按钮揭示|
|Q10-B／D3-B|`D3-B-student.ipynb`：先算绝对差，再数值核对／可选音乐|p31–32。数值核对保留；超时取消音乐，仍保留误差推理|
|Q17／D4|`D4-student.ipynb`：先猜文件大小，再只读2秒样例表|p49–50；静态不能换文件，但能解释32,000／32,044B|
|Q17-B／D4-B|`D4-B-student.ipynb`：先回看猜测，再读A/B参数|p51–52；不能取消这个开场闭环|

Q5独立填表、Q6互读码字、Q16独立列式、Q18双条件表均留下可收集证据。Q19独立60秒：必改③两处，再选①或②；写依据，先收全班答卷再揭示。六个目标的行为／判据／持续误解回应见设计C1、C8。第8／15／21／27／30／38分钟裁剪点及树总结预算见C2；优先取消24点、重复试听和混叠拓展，保留关键思考与退出评价。

## 文件角色与历史身份

|路径|角色／编辑点|
|---|---|
|`course-design.qmd`|教学依据，保留认知理由、Q链、脚本、边界；C8定义树与独立子问题共享数据|
|`scripts/lesson_model.py`|读取设计，编译逐页计划；`validation/v4/slide-plan.json`记录可见／暂缓／备注／证据／焦点／树|
|`scripts/build_views.py`|同时拥有两版QMD/IPYNB、八份阶段IPYNB、Reveal源和活动单输出。改输出须回写设计／生成器|
|`demos/audio_core.py`|共用采样／量化／PCM／图表与播放实现；中文教学标签是有理由的字面量|
|`scripts/build_deck.mjs`|从设计／逐页计划生成原生PPTX，实际duplicate后追加排序；不固定40页|
|`scripts/patch_font_defaults.py`|补齐主题／母版／Notes默认Alibaba字体，每次构建必跑；这是源端构建步骤|
|`scripts/finalize_deck.mjs`|校验候选并复制到明确新路径，已有正式文件拒绝覆盖；依赖制作运行时，不属课堂依赖|
|`slides.qmd` → `exports/reference-v4/slides.html`|62阶段Reveal参考。v4使用最终渲染PNG作背景、同步阶段Notes；静态镜像保持几何与树顺序，互动由Notebook／HTML承担。PPTX仍是正式课堂格式|
|`assets/audio-manifest.json`、`assets/audio/`|既有11份音频的精确参数、hash和统一变换；未覆盖|
|`assets/source/excerpt-45-51-decoded-pcm16.wav`、`assets/audio-provenance-v4.json`|旧PCM缓存的无损6秒摘取，是制作的确定性输入；保留原M4A、记录来源与解码差异|
|`demos/audio-lab.html`|指定D阶段的离线备用实验台，不是第五个必做演示；D1可在教师Notebook备用IFrame运行|
|`exports/*v1*`、`*v2*`、`*v3*`；`exports/reference/`|历史交付／历史参考，保留原身份，不能作为v4通过证据|
|`validation/history/v3-sources/`|本次修改前的源快照；原始版本审查记录仍保留原位置|
|`validation/v4/`|v4独立计算、真实内核副本、渲染／montage、GUI证据和hash；执行副本含答案，不发学生|
|`.build/`、`.quarto/`、Notebook checkpoints|制作／试验缓存或恢复材料；包括失败试验，不能当正式交付，不需课堂复制|

当前版本及复审入口：`validation/course-design-review-v4-2026-10-01.md`。v3为`course-design-review-round3-2026-10-01.md`，v2为`course-design-review-2026-10-01.md`，v1为`audit-report.md`。历史源、媒体、课件和对应报告未删除或改名。

## 音频、技术与许可边界

原《逆战》M4A由用户提供，AAC／44.1kHz／双声道，afinfo报告约275.6422秒、65536bit/s。**公开再分发许可未确认**。同一45–51秒片段先取双声道均值形成mono，对所有对照使用同一增益0.7490779781559563和10ms淡入／淡出，再按参数重处理。对照不单独归一化；IPython从文件嵌入播放。试听判断不能代替相等检验。

数学波形、已解码音频的重新处理均非真实ADC实验。12／24点图支持时刻计数与采样规则，不能证明某一听感。理想带限模型用fs > 2fmax；实际滤波须留余量。正常降采样采用教学FFT低通与插值，通／阻带边缘为目标Nyquist的0.82／0.96，不是工业重采样器。`tone-alias-naive-at8000.wav`故意裸丢点产生2kHz混叠，仅作诊断；低通结果以测得RMS和条件解释，不能断言绝对无声。

`effective2/4/8-stored16`是有效量化等级装入16bit整数PCM，真实文件按存储16bit计数。课堂无符号等级码与真实有符号little-endian PCM分开；负幅度是相对基准的值，非“负音量”。均匀中点量化的半步长误差界只在给定范围／无过载条件内成立；上界减小不意味着每点都严格减小。

公式 fs×秒×实际存储bit×声道数÷8只计固定宽度未压缩PCM样本数据。真实计数优先采用帧数×block alignment。kHz／Hz用1000，KiB／MiB用1024。32,044B样例中44B属于当前简单RIFF布局，不能概括所有WAV。WAV容器并不保证未压缩。

读写检验的精确目标是已记录的交错int16样本字节；整数转换使用ties-to-even舍入和−32768..32767饱和。原浮点输入允许舍入／削波，不能要求无条件浮点相等。AAC新解码与历史缓存存在测得≤1 LSB差异；不会据此说解码恢复AAC前信息。提高采样率或存储位数也不恢复未记录信息。主张／原始资料的版本、章节、检索日期与支持限制在v4复审记录。

## 复制与运行

复制整个课程目录可保留所有资料；课堂不需要`.build/`、`.quarto/`、`validation/`及checkpoints。最小运行集合：v4 PPTX、两版Notebook、`notebooks/staged/`、`demos/`、完整`assets/audio/`，以及三份活动HTML；参考放映再带上完整`exports/reference-v4/`。保留demos与assets的兄弟目录关系。原M4A及source片段只用于来源核查／制作，不是课堂播放依赖。

WPS不需Python。Notebook课堂依赖：现有Python3.11+、numpy、matplotlib、IPython、ipykernel、JupyterLab。授课前在选定环境从本课目录运行`jupyter lab --ServerApp.root_dir=.`。不联网安装。教师备用IFrame使用`/files/demos/audio-lab.html?stage=D1`，依赖该服务器根目录；本机已实际点击验证。若服务器使用额外base_url前缀，应调整IFrame路径，或直接浏览器打开HTML。旧执行副本可能未受信任，播放器／IFrame会被清理；课堂从清洁源重新运行，不使用旧执行证据放映。

浏览器直接离线打开`demos/audio-lab.html?stage=D1`等指定阶段；无query默认D1。`?stage=D2-B`仅纯音条件任务，结果按钮之后才显示。文件协议的实际支持及Windows播放器仍需课前核对；HTTP本机检查与复制依赖检查不替代此项。

## 制作顺序与覆盖行为

以下命令均在本课程目录运行。制作依赖与课堂依赖分开：制作另需Quarto1.10.18、Node24／Artifact Tool、python依赖nbformat／nbclient／Pillow／fontTools／pypdf，LibreOffice／pdftoppm及Alibaba PuHuiTi 3.0 115 Black／55 Regular。`.build/node_modules`链接到现有Artifact Tool依赖；finalizer的本机默认位置可用`PRESENTATIONS_SKILL_DIR`、`ARTIFACT_PYTHON`覆盖。渲染器用`AUDIO_SOFFICE`、`AUDIO_FONT_DIR`覆盖。具体已验环境见v4记录。

本机实际验证：Notebook／views／audit使用`/Users/chran/miniconda3/envs/shtick/bin/python`；render／finalizer的PDF检查使用`/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`；Node使用同一runtime的`dependencies/node/bin/node`，Artifact Tool版本2.8.71。render前将`dependencies/bin/override`加入PATH以找到pdftoppm。下文的python／node指相应制作环境，不能拿默认base Python的名称当作内核已对齐的证据。新制作环境先建`.build`，把已安装Artifact Tool所在node_modules链接到`.build/node_modules`；已有链接先核对，不覆盖。课堂复制不需要这些本机制作路径。

```sh
python scripts/build_views.py
node scripts/build_deck.mjs
python scripts/patch_font_defaults.py
node scripts/finalize_deck.mjs exports/NEW-VERSION.pptx validation/NEW-VERSION-finalization.json
```

build_views会覆盖当前两版QMD/IPYNB、八阶段文件、活动QMD／答案、slides.qmd及v4逐页计划；先保存人工修改并回写正确源。build_deck只覆盖`.build/v4/audio-candidate.pptx`和v4 deck-map。finalizer默认v4正式文件已存在时拒绝覆盖；修订必须明确新版本路径。render_v4和当前audit入口绑定本次v4，下一版本同时更新路径／证据位置，不静默覆盖本次验收。

本次v4的渲染与参考构建：

```sh
python scripts/render_v4.py
python scripts/build_views.py --rendered-slides validation/v4/render
quarto render
python scripts/check_notebooks.py
python scripts/check_review_evidence.py
python scripts/audit_package.py
python scripts/check_source_output.py
python scripts/check_text_fit.py
python scripts/check_copy.py
python scripts/check_diff.py
```

render_v4重新写`validation/v4/render/`全62页、PDF和7套montage；Quarto写`exports/reference-v4/`，保留原`exports/reference/`。check_notebooks每份fresh kernel，timeout120秒，记录实际内核环境并保存执行副本；覆盖v4同名证据，因此历史证据已归档。源／输出一致性见当前检查及hash清单；改完PPTX必须重渲染、重建Reveal并刷新检查，单改输出不成立。

音频重制作优先试写，**prepare_audio默认会覆盖assets/audio及原manifest，勿直接运行默认命令替换已审查媒体**：

```sh
python scripts/prepare_audio.py --output-dir .build/v4/audio-repro --manifest validation/v4/audio-reproduction-manifest.json
```

默认读取已保存的45–51秒PCM摘取；完全重做解码可使用本机`afconvert -f WAVE -d LEI16 assets/nizhan-zhangjie.m4a .build/v4/source-decoded-verified.wav`，再显式传`--decoded ... --decoded-start 0`试写另一个目录。AAC解码器／整数转换可能有版本依赖，不能覆盖原媒体后沿用旧hash。audit中的新解码对比需要上述full cache与历史缓存；缺失时应单列unverified，不使课堂依赖制作缓存。

当前课程文件、生成输出及v4验证材料可纳入Git；`.build/`、`.quarto/`、`__pycache__/`、checkpoints按仓库规则ignored。输出是否已跟踪由Git状态确认；本次任务未提交、推送或发布。
