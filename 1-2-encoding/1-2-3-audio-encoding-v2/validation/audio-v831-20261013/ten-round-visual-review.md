# 音频编码 v8.1 → v8.3.10：十轮视觉迭代评审报告

**对象：** \`1-2-3-audio-encoding-v8.1.pptx\`，普通高中信息科技两课时课件（70页）。
**风格：** 项目\`slide-style-guide.md\`，白底、紫色上下轨道、Alibaba PuHuiTi大字标题、使用语义色、问题/答案保持一致版式。

## 评审原则

- 是否让学生**看见证据、预测变化、解释原因**，而不是只看到装饰图？
- 对抽象概念，首先使用原生可编辑波形、数据表、相同坐标下的前后对照，避免AI图片生成不准确的数值、箭头或坐标。
- 对图像有损效果，使用同一幅真实像素图经JPEG编码后的结果，不凭AI视觉想象“文件压缩后应该长什么样”。
- 保留70页完整教学主线、6组习题题目与答案、Speaker Notes，不覆盖v8.1。
- 每轮按 **发现问题 → P0/P1/P2 → 改图 → 生成对应版本 → PPTX/备注/习题配对/输入输出SHA256审计 → push** 顺序执行，下一轮严格读取刚刚生成并推送的前一版本。

## 各轮改进（独立PPTX＋独立Git提交）

| 轮次 | 优先级 | 评审发现 | 教学意义及修订 | 输出 |
|---|---|---|---|---|
| 1 | P1 | 第4页模拟量/数字量主要靠文字解释 | 改为在可比时间轴上显示连续波形和离散采样点，直观看懂“电脑保存一组数值” | \`v8.3.1\` |
| 2 | P1 | 第5页麦克风转换仍偏抽象 | 图中用振动声源、向麦克风传播的声压变化及输出连续波形串起物理过程，避免把麦克风误解为数字编码器 | \`v8.3.2\` |
| 3 | P1 | 第7页录音和播放流程易混 | 紫色表示ADC录音路径，青色表示DAC播放路径；学生能顺着箭头复述四个阶段 | \`v8.3.3\` |
| 4 | P1 | 第24页时间采样与幅度量化的区分不够醒目 | 时间方向画离散点、幅度方向画量化等级线，并保持波形参照 | \`v8.3.4\` |
| 5 | **P0** | 第17页“3.71属于哪个等级”缺少可观察分界证据 | 0～8数轴、八个区间、红色3.71落点。仍保留先预测的课堂任务，下一页再正式揭示映射规则 | \`v8.3.5\` |
| 6 | P1 | 第31页PCM容量公式缺少清楚的量纲路径 | 四个因子分别对应采样率、时长、声道数、位数，再乘及除8转Byte | \`v8.3.6\` |
| 7 | P1 | 第41页音轨与声道只有空标签 | 两条不同编辑音轨的可读波形、混合箭头、两条输出声道波形，避免把音轨数量误当声道数量 | \`v8.3.7\` |
| 8 | **P0** | 第45页五帧画面的位移在投影上不明显 | 五张统一背景、同一球逐帧右移，只有位置变化；继续说明25fps的意义 | \`v8.3.8\` |
| 9 | P1 | 第63页BMP/JPG差别只有文字 | 使用同一程序生成的640×350 RGB图像，左边原像素图、右边JPEG低质量编码并解码后的实际输出；原位标注参数与限定 | \`v8.3.9\` |
| 10 | P1 | 第60页三组图像规律性太小 | 纯色、重复色块、复杂颜色变化用同尺寸的大图逐列展示，突出无损压缩对可利用规律的依赖；统一六组练习答案的紫色强调 | \`v8.3.10\` |

这里的P0表示**影响该课堂页面关键证据的可观察性**，不是整个PPTX技术损坏。

## 关于图片模型与实际新插图的选择

**已沿用的ChatGPT图像生成资产：** v8.1第3页“音叉振动—空气传播—麦克风接收”的物理场景插图，已足够支持“声音首先是什么”的问题，无须重复添加类似图片。

**新增示意图：** 其余典型波形、位数/等级、PCM公式、音轨/声道、视频逐帧与冗余比较，使用PowerPoint原生矢量图形而非AI位图，以确保具体样本位置、量化区间、数字和技术关系准确。

**新增真实编码结果：** v8.3.9第63页使用Python/Pillow编程绘制同一幅山峦图并经实际JPEG编码（示例使用较低质量设置），将原始像素图和JPEG还原图成对嵌入同一张幻灯片。它**不是**生成式模型臆造的JPEG效果，且不对任意BMP或JPG得出固定文件大小结论。

### 供ChatGPT图像模型创作时使用的提示词

以下提示词仅适合创作**没有精确坐标或必须对应数字的真实场景底图**。对于量化、采样和真正的压缩差异必须通过实际算法得到数据，不能让生成模型凭空画表格或数值：

> 16:9 white-background modern senior-high-school IT classroom illustration. An ordinary sound source such as a tuning fork vibrates on the left; a realistic desktop microphone records sound on the right. Show sound pressure wave fronts as soft, unobtrusive violet curved bands traveling toward the microphone, not a transverse squiggly line representing a sound propagation path. No labels, no letters, no logo, no text, no decorative 3D. Keep the middle uncluttered so Chinese teacher annotations can be added natively in PowerPoint.

> Create one faithful flat educational landscape scene, 640 x 350 composition: a mountain range, stylized vegetation with fine varied details, and a bright sky. Use clean hard-edged forms and distinct color regions, no text and no split-screen. This is the **single source image** for a real PNG-vs-JPEG encoding comparison: the exact original should be encoded by software at chosen JPEG qualities, rather than asking the image model to hallucinate compression artifacts.

> Produce a clear, high-school-friendly illustration of a student using a microphone to record a short sound in a bright computer classroom. The microphone is connected to a laptop, whose screen shows a simple time-amplitude waveform without labels or numbers. Minimal white background, violet/cyan accent only, no product logos or unnecessary floating UI. Leave space for Chinese labels explaining microphone, ADC and digital file.

**视觉取舍：** 对此版本真正需要精确展示的教学图，采用原生绘图或实际编码更适当。这里不把未经数学验证的AI图示用于量化、编码、文件大小等科学证据。

## 自动复验与图形抽查

- 每一轮输出一个完整70页PPTX和一个\`round-XX-audit.json\`，审计包括输入输出SHA256变化、70页/70页Speaker Notes、6组题目答案对应、PPTX ZIP结构完整。GitHub Actions严格等待本轮\`git push\`成功后才生成下一轮。
- 本地使用从课件相同内容构建的70页候选版，单独提取各轮变化的10张页做PDF渲染，并逐一检查文字、坐标图、公式、标注的可读性和对齐关系。远程版本也经过结构审计，但**GitHub Actions结构通过不等于真实PowerPoint投影验收**。
- 完成后保留10个独立版本、全部逐轮审计和原v8.1。请优先使用最后一版\`1-2-3-audio-encoding-v8.3.10.pptx\`。

## 教室最后验收

1. 在Windows PowerPoint中预览第4、5、7、17、24、31、41、45、60、63页，特别确认远距离投影的量化刻度和JPEG细节。
2. 对第63页不要把“低质量JPEG示例”等同于所有JPEG的画质水平，适合先让学生预测是否能完全还原像素值。
3. 需现场检查各版安装的Alibaba PuHuiTi字体、投影颜色对比、2课时真实时间及Windows浏览器端Jupyter演示切换。
