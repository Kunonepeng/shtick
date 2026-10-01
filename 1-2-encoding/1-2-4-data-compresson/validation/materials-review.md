# 数据压缩入门：配套材料三轮审查（v1历史记录）

当前图像与知识树改进、34页v2课件及复查结果见[improvement-review.md](improvement-review.md)。本文件保留原30页v1验证记录。

本次审查针对45分钟核心课材料，设计阶段的两轮记录另行保留。审查中的问题、修复与复查按轮保存：

1. [第一轮：版面、字体、活动单、基本运行](materials-round-1.md)
2. [第二轮：教学顺序、数值、材料间一致性](materials-round-2.md)
3. [第三轮：提前泄露、最终包与入口](materials-round-3.md)

## 已完成的本地检查

|项目|结果与证据|
|---|---|
|PPTX与设计顺序|30页；Q1–Q10问题页位于2、4、6、9、11、14、17、21、23、26；按题先预测后揭示|
|问题页与复制揭示页|标题文字、字号、坐标和基础几何通过XML比较；问题页无提前答案、计算结果或红色纠错框|
|全部页渲染与视觉检查|LibreOffice转PDF、Poppler渲染30页；全部页逐页检查；最终更改页复查；[总览](review-3-final/montage.png)|
|版面、字体与原生对象|16:9、白底、8pt紫轨、36pt标题、22pt以上正文；原生表格见21–27页；[结构审查](review-3-final/package-audit.json)无问题|
|实际渲染字体|PDF字体资源仅Alibaba PuHuiTi 3.0 55 Regular／115 Black；[记录](review-3-final/rendered-fonts.json)|
|Speaker Notes|所有30页有完整问题／目的、逐字稿、提示、技术边界与来源；不把备注投影给学生|
|Notebook|两版Q1–Q10及D1–D5一致；真实Jupyter内核执行内存副本通过；交付文件无输出、无执行计数；[记录](review-3-final/legacy-notebook-execution.json)|
|数值与可逆性|RLE 16B→6B与32B；差值22bit装3B；近似48bit／6B；JPEG像素与完整大小均实测；输入边界检查通过|
|活动单|四页均渲染并检查；前三页A1–A3与出口，第4页私有颜色卡；预测／答案分开，留有书写空间|
|离线逐步演示|按钮处理程序经Node DOM测试，验证逐段展开、七步读回、重置和输入边界；无联网依赖；[记录](playground-handlers.json)|
|Quarto与引用入口|最终检查记录见[第三轮](materials-round-3.md)|

## 对应环境尚未验收的项目

Windows教室电脑的WPS／PowerPoint、JupyterLab界面操作、浏览器图形显示、投影可读性和本班45分钟实授节奏未在本环境检查。本地LibreOffice渲染和Jupyter内核执行分别证明文件可渲染、代码可运行，不能替代这些验收。

D6的MP3试听样本属于第二课时规格，未制作同源、统一增益、时延对齐的音频包；核心课不依赖它。教师Notebook中的两帧更新模型可执行，但不是完整MPEG码流实现。生产PPTX没有依赖动画才能理解的页面。
