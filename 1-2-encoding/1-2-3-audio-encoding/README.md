# 音频数字化课堂包

45分钟；教师演示，学生纸笔与讨论。Windows + WPS + JupyterLab，教室音箱。

## 上课入口

1. WPS打开`exports/1-2-3-audio-encoding-v1.pptx`。40页含19组提问／揭示；先停在题目页，作答后再翻页。Speaker Notes含逐字稿、预期回答、技术边界和来源。
2. JupyterLab从本课程目录打开`demo-lab-teacher.ipynb`，运行准备单元。课前清除旧输出，折叠教师说明及代码。课堂仅显示问题和当前输出。
3. 打印`exports/reference/student-activities.html`或打开`student-activities.qmd`，学生不需要电脑。`demo-lab-student.ipynb`是观察／课后阅读版，无保存输出、无教师答案。
4. 课前试听音乐A/B、4bit模型及6kHz纯音，确定音箱可播放且音量合适。每段音乐6秒，纯音3秒。保持同一音量，听不出差别时用频率条件和误差图解释。

核心文件是`course-design.qmd`和PPTX。`slides.qmd`和`exports/reference/slides.html`为参考Reveal实现。Notebook运行需要现有conda环境提供`numpy`、`matplotlib`、`IPython`；本包不会联网安装依赖。WPS/PPTX不需Python才能放映。

## 四次演示

|位置|演示|离线替代|
|---|---|---|
|Q3–Q4／D1|连续曲线→采样点，比较12／24点|PPTX第6–9页，`assets/fallback/D1.png`|
|Q8／D2|音乐44.1k／8k；6kHz纯音正常低通后降采样|`assets/audio/`预制WAV及PPTX第16–17页|
|Q10／D3|2／4bit近似与误差；试听4bit有效模型|PPTX第20–21页及预制WAV|
|Q17／D4|实际WAV参数、样本数据与完整字节数|PPTX第34–35页，`assets/fallback/D4.png`|

需要逐个取样动画时，在Notebook最后的备用单元显示`demos/audio-lab.html`；也可直接用浏览器离线打开。动画和试听不自动启动，必须由教师点击。HTML无法加载时不要现场排障，使用PPTX静态证据和预制WAV。课件不嵌入音频，音频演示由JupyterLab负责，因此搬到Windows时复制**整个课程目录**，保持相对路径；不需复制制作缓存`.build/`。

## 音频及计算边界

《逆战》来自用户提供的`assets/nizhan-zhangjie.m4a`。保留原文件，以45–51秒共6秒的同一片段制作对照。该文件是有损AAC，解码成PCM WAV不恢复此前损失。原文件及派生证据SHA256、共同增益与精确参数见`assets/audio-manifest.json`。

`effective2/4/8-stored16`表示课堂有效量化模型装入16bit PCM。用于看／听量化误差；实际WAV数据量按**存储16bit**算。正常降采样先低通；`tone-alias-naive-at8000.wav`是故意不滤波的混叠备用诊断，不是正常转换范例。

公式只计算固定存储位数的未压缩PCM**样本数据量**，不含WAV文件头及其他chunk。32,044B样例中44B只是本文件开销。kHz用1000；KiB／MiB用1024。

## 编辑与验证

修改教学内容先改`course-design.qmd`，再运行`python scripts/build_views.py`同步Notebook／Reveal／活动单。课件制作时先运行`build_deck.mjs`，再运行`patch_font_defaults.py`补齐默认字体，最后运行`finalize_deck.mjs`；修订需给finalizer新的输出及报告路径，避免覆盖审查证据。`scripts/build_deck.mjs`从同一教学依据读取问题、必要条件、结论和Notes，并调用Artifact Tool生成原生可编辑PPTX；题目页使用实际duplicate生成揭示页。波形、采样点、码字和误差线均为原生对象。

课件制作环境使用Codex捆绑Node／Artifact Tool；`scripts/finalize_deck.mjs`为该制作环境的校验入口，并非要求课堂电脑安装的程序。课堂无需重新生成PPTX。重做音乐证据先在本地解码原M4A为`.build/nizhan-decoded.wav`，再运行`python scripts/prepare_audio.py`。Windows不需要这个临时解码文件，也不需要ffmpeg。

审查结果、修复记录和实测边界见`validation/audit-report.md`。未在本地安装的WPS／PowerPoint和教室音箱不写成已验收；授课前检查字体、Notes、投影和声音。
