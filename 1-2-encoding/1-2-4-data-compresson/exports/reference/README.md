# 数据压缩入门

高中信息科技，45分钟核心课。教师操作PPTX和Jupyter，学生用纸笔参与；不要求学生会Python。

|文件|用途|
|---|---|
|`course-design.qmd`|教学设计依据：问题链、逐字稿、活动意图、技术边界与来源|
|`exports/data-compression-v1.pptx`|正式课堂课件，30页，10个独立问题页及复制揭示页，逐页教师备注|
|`demo-lab-teacher.qmd` / `.ipynb`|教师演示：D1–D5、预期结果、控制顺序及帧间变化拓展|
|`demo-lab-student.qmd` / `.ipynb`|学生观察与记录：预测栏、分阶段运行，无预存输出|
|`student-activities.qmd`|可编辑的A1、A2、A3与出口记录|
|`exports/print/student-activities.pdf`|可打印活动单：1–3页学生记录；第4页教师剪下私有颜色卡|
|`demos/compression-playground.html`|离线按钮演示：RLE逐段展开、差值逐项读回、近似值映射|
|`slides.qmd` / `exports/reference/slides.html`|与PPTX逐页对应的Reveal.js参考版，教师备注可查|
|`assets/evidence/`|随包精确数据图与同坐标JPEG对照，演示失败时用静态页|
|`sources/`|课件与配套材料生成源码、页计划和证据清单|
|`validation/materials-review.md`|三轮整包审查的问题、修复与复查证据|

## 上课前

1. 将整个文件夹复制到教室电脑。安装项目规定的Alibaba PuHuiTi 3.0字体：55 Regular、115 Black。用WPS打开PPTX，确认中文换行、备注和两图对照。文件没有必须播放的动画；逐页翻页即可。
2. A1、A2、A3按顺序发放：A1在Q2发，A2在Q5收集方案后发，A3在Q8发。第4页只给教师，剪下卡片仅交发送者；接收者画回后再展开核对。
3. Jupyter环境需要Python 3.10+、JupyterLab、Pillow。可在现有教学环境执行`python -m pip install jupyterlab pillow`，然后在本课目录运行`jupyter lab`。课堂中不安装软件。先试运行教师Notebook，再清空全部输出、保存，并重新从头逐格演示。
4. 只需准备PPTX与教师Notebook。Q1先用`opening(False)`，Q3再用`opening(True)`。不要提前运行整本学生Notebook；其中代码单元会在运行后产生当前答案。
5. 核心课到第40分钟进入Q10。最后停在“用两句话检查自己的判断”；收取活动单后才显示末页参考答案。Q7 quality20、大差值反例和帧间变化均可跳过。

## 演示控制与备用

|节点|先收什么|再运行什么|失败时|
|---|---|---|---|
|Q1／D1|文件变小的猜测|原图与大小，然后读回图；不验相等|PPTX第2–3页|
|Q2／D2|私有串的规则与消息|RLE编码、逐段展开|第4–5页与私有颜色卡|
|Q3／D1|比较对象与核对方法|修正错误后，检验解压bytes|第6–8页|
|Q4／D2|两串段数与大小|同规则16B→6B／32B|第9–10页|
|Q5／D3|完整差值与末三项读回|22bit装3B的模型|第11–13页|
|Q6／D4|能映到120的两个原数|6bit等级与代表值|第14–16页|
|Q7／D5|外观判断与数据判断|同源像素、完整文件大小、同坐标放大|第17–20页|

`compression-playground.html`可用本机浏览器双击打开，不联网、不需要Jupyter widgets。选择输入会清除旧结果；按钮逐次揭示，教师决定停顿。它不是压缩文件格式转换工具。

## 计数与范围

RLE、差值和位深近似只比较数据部分，共享规则与长度未计入；D5比较完整PNG／JPEG文件。开场4096B是颜色编号数据，不是RGB或PNG大小。压缩图像的无损检验比较像素；通用文件压缩比较解压bytes与原输入。

本包完成45分钟核心课。D6的MP3听辨样本只保留实施规格，不作为已验证材料；第二课时需按课程设计另行制作同源、统一增益、时延对齐的样本。

本地渲染、程序验证与课堂验收分开记录。Windows教室电脑的WPS／PowerPoint、JupyterLab界面、投影可读性和实际45分钟节奏需要在对应环境复核；当前环境未进行这些检查。

## 复现材料

`sources/build_materials.py`生成两份QMD／Notebook、活动单PDF与证据清单；`sources/build_deck.mjs`生成原生可编辑PPTX及页计划，需要Codex的Artifact Tool运行时（路径配置在文件开头）。`sources/build_reference.py`从已审查PPTX、页计划和逐页渲染图生成参考版，避免问题编号和数值漂移。

教师只改输入时使用`demos/compression_lab.py`提供的函数。`save_jpeg_trial`只写`demos/scratch/`，不覆盖教学证据。PPTX或教材数据更改后，同步更新课程设计并重新检查所有派生材料。
