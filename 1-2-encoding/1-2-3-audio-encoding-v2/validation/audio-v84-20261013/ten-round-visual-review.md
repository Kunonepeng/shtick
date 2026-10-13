# 声音、音视频编码与压缩 v8.4：十轮视觉优化记录

## 范围、版本与使用原则

基线：GitHub \`main\` 分支上的 \`1-2-3-audio-encoding-v8.3.10.pptx\`（70页）。
本轮连续发布 \`1-2-3-audio-encoding-v8.4.1.pptx\` 至 \`v8.4.10.pptx\`。每轮都从**前一轮正式PPTX**构建，先检查结构并生成分级审计，再提交与推送GitHub，然后才进入下一轮。

教学依据：高中信息科技，两个45分钟课时；保留问题页/答案页的渐进揭示、70页Speaker Notes、紫色上下轨道、中文表达与学生可解释的图示。禁止将任何“预测页”改成提前透露答案的页面。

**关于生成图片的方法**：曾尝试调用 ChatGPT 图像生成工具，但本轮没有获得可供嵌入的模型成品图像。因此没有宣称使用了新的AI生成图片。最终采用基于提示词设计、由Python Pillow及PPT原生对象程序化绘制的教学插图，全部已实际嵌入PPTX。相比装饰性插画，这保证了波形、采样点、等级及编码数据与教学内容可以核对。

## 逐轮 P0/P1/P2 评审、改动与复验

| 轮次／输出 | 优先级 | 原页码及发现的问题 | 修改及意义 | 回归检查 |
|---|---|---|---|---|
| 1：v8.4.1 | P1 | **第3页**：文字描述声源与麦克风，空气变化不直观 | 音叉、波阵面与麦克风示意图，使学生区分振动、声压变化及接收 | 示意图包含三种对象，无虚假的“空间正弦传播轨迹” |
| 2：v8.4.2 | P1 | **第8页**：空间传播与时间波形容易混淆 | 并排绘制“向外传播的波阵面”与“固定位置的幅度-时间曲线” | 两种图形的物理意义和坐标轴不同 |
| 3：v8.4.3 | P1 | **第12页**：无法一眼区分整体概览和实际数字样本 | 增加局部放大对照、明确蓝色采样点 | 波形概览与局部采样点有不同的图注 |
| 4：v8.4.4 | **P0** | **第16页**：0到7容易只数成7级，后续区间概念缺视觉基础 | 8格并列量化尺，标明L0—L7；不提前透露第17页3.71归属答案 | 计数页只讲8级，下一页仍保留独立预测 |
| 5：v8.4.5 | P1 | **第22页**：10个样本、10组等级和二进制码字表过于密集 | 横向时间序列与码字同列对齐，高亮示例 | 与原数据等级3、5、7、6、4、2、0、1、3、4逐一一致 |
| 6：v8.4.6 | P1 | **第27页**：PCM样本和WAV容器差异难以看懂 | 文件头与PCM字节区块分色，解释“文件说明”与“声音数据” | 不把WAV容器误称压缩算法 |
| 7：v8.4.7 | P1 | **第49页**：6.44 GiB的未压缩视频为什么与日常经验冲突，缺视觉证据 | 多帧数据示意与“未知大小的日常文件？”形成对照，故意留出解释空间 | 无虚构压缩率，无“压缩编码”提前揭示 |
| 8：v8.4.8 | P1 | **第41页**：编辑音轨与输出声道偏抽象 | 两条独立音轨波形→左右两路输出，并以扬声器图标落地 | 混音后可仍为双声道；不会把音轨数当声道数 |
| 9：v8.4.9 | P1 | **第58页**：无损/有损的区别仅由句子说明 | 原始像素图→完全相同恢复→有可见差异的近似恢复 | 教学图明示“差异经放大，仅用于理解概念” |
| 10：v8.4.10 | P1 | **第63页**：同一原图和低质量JPEG的差别投影时不明显 | 生成完全同位置的局部裁切放大并排图 | 两图出自同一程序；JPEG quality=3仅作示意 |

## 最终预测页的质量补丁

完成上述10轮提交后，最终审计额外发现**第16页底部小字仍提示了下一页的“3.71”**，虽然未直接透露归属等级，也影响预测页的揭示节奏。按照P0的优先级，使用 \`final_visual_fix.py\` 将底部改为“下一页再研究具体采样值属于哪个区间”，并更新第10轮审计SHA。**未修改第1至第9轮文件**。见 [最终复验GitHub Actions](https://github.com/Kunonepeng/shtick/actions/runs/38420621496)。

## 文件与复现

- 课件：\`1-2-3-audio-encoding-v8.4.1.pptx\` … \`1-2-3-audio-encoding-v8.4.10.pptx\`，均在原音频编码课程目录。
- 源码：\`validation/audio-v84-20261013/build_ten_visual_rounds.py\`。
- 固定绘图辅助：\`validation/audio-v84-20261013/v831_base.py\`。
- 后补预测页修订：\`validation/audio-v84-20261013/final_visual_fix.py\`。
- 每轮审计：\`validation/audio-v84-20261013/round-01-audit.json\` … \`round-10-audit.json\`。
- [十轮顺序生成工作流](https://github.com/Kunonepeng/shtick/actions/runs/38420179778) 确实在每轮构建后分别提交、推送了10次；其末尾附加验证因提前暴露提示小字而失败，问题已由上方成功的最终补丁工作流解决。
- 版本链与最终页的全部结构核验：成功。每轮70页、70份讲者备注、6对题目与答案均保留。

## 图像模型提示词（教学视觉任务）

以下提示词可用于未来需要照片质感的图像模型。所有提示都应**不含中文文字**，由PPT后期加入中文说明，避免模型生成不可靠的字符与技术标注。涉及刻度、位数、码字等严格数据时，不允许用模型绘制数值，必须使用程序化精确图。

1. **声源与麦克风**：\`Minimal school-science illustration on a white background: a vibrating tuning fork at left, transparent curved sound-pressure wavefronts in air, desktop microphone at right; no wavy propagation path, violet and cyan palette, no text.\`
2. **空间与时间**：\`Educational split-panel illustration: expanding pressure wavefronts in physical space at left, a stationary sensor recording amplitude over time at right; clear difference between phenomena, white background, no text, no numbers.\`
3. **真实采样点**：\`Clean waveform visualization showing a broad overview and a magnified window containing clearly separated samples, sky-blue circular dots; no invented measurement numbers, white engineering classroom style.\`
4. **量化**：\`Eight equally spaced horizontal quantization bins on a clean ruler, violet outlines, neutral contrast, no text and no arbitrary input values.\`
5. **编码**：\`A horizontal row of ten discrete sampled sound values matched vertically to individual short binary groups, diagram layout only, no invented digits or captions.\`
6. **WAV/PCM**：\`Flat technical educational illustration of an audio file split into a small metadata header and a large block of repeated digital audio samples, clean white background, no words.\`
7. **视频容量冲突**：\`Eight successive small frames from the same simple animation, pointing toward one small question-mark file; the difference is a mystery, do not show compression as an answer; white background.\`
8. **音轨与声道**：\`Two distinct sound-editing waveforms on separate layers at left leading to stereo left and right output speakers at right, educational flow graphic, avoid equating each track to a speaker, no text.\`
9. **无损和有损**：\`Three identical-size simple pixel-art panels: original, exact copy, slightly altered reconstruction; the differing area is visibly highlighted, no words, no invented filenames.\`
10. **局部有损伪影**：\`Comparison of the same precisely aligned crop from original lossless pixel artwork and low-quality JPEG reconstruction, enlarged enough for students to see block artifacts; no words.\`

## 课堂前仍需实测的项目

PPTX结构检查和本地10页视觉抽样，**不能**替代完整的Windows PowerPoint投影检查。请重点核查第3、8、12、16、22、27、41、49、58、63页及6组答案页。JupyterLab的真实Mac→Windows浏览器联动属于独立环境验收，不在本次视觉优化自动测试范围内。
