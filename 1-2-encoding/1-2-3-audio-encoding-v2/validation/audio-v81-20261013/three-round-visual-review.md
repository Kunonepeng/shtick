# 声音编码 v8 → v8.1：三轮视觉评审（2026-10-13）

基线：GitHub main中的1-2-3-audio-encoding-v8.pptx（70页）。
结果：1-2-3-audio-encoding-v8.1.pptx（70页，70页Speaker Notes）。
原则：依据slide-style-guide.md保留白底与紫色上下轨道；增加教学证据，而非装饰；不变更两课时知识顺序和题目文本。
CI与审计：https://github.com/Kunonepeng/shtick/actions/runs/38411442844

## Round 1：证据图是否清楚

| 级别 | v8问题 | 修订 | 复验 |
|---|---|---|---|
| P0 | 第45页五帧小球的位置差别不明显，无法直观展示帧间变化 | 增大小球、拉开位置差、各帧增加同位置的浅灰参考线 | 代码验证逐帧相对坐标递增；渲染复查 |
| P1 | 第3页只有抽象的三步文字框，声音传播缺少可观察图形 | 增加音叉振动—空气中声压变化—麦克风的教育图，并设置中文标签 | PPTX第3页存在图片，图像可放大观察 |
| P1 | 第16页量化等级线偏淡 | 加粗0～7等级线、编号调整为23pt | 8条等级线和包含0的8个等级清晰 |
| P2 | 采样曲线在投影上偏细 | 调整第8、11、14、15页波形线宽 | 点与输入曲线依旧分明 |

## Round 2：比较与数字信息层次

| 级别 | v8问题 | 修订 | 复验 |
|---|---|---|---|
| P1 | 第22页10组二进制码字文字偏小 | 码字20pt青色加粗；行标题23pt | 仍与样本序号、等级逐列对齐 |
| P1 | 第44页图像/声音比较表阅读层次偏弱 | 三行同基线的“位置—记录什么—数据量”对照、22pt文字 | 视觉复核行距与对齐 |
| P1 | 第59页ZIP/MP3/WAV/MP4分类难一眼区分 | 类别名30pt，解释22pt，语义色区分 | 未错误地把容器当成固定压缩算法 |
| P2 | 第50页数据压缩前后对照不醒目 | 提升标签至25pt、正文22pt | 阅读焦点更集中 |

## Round 3：练习揭示与整体一致性

| 级别 | v8问题 | 修订 | 复验 |
|---|---|---|---|
| P1 | 6组答案缺少稳定的视觉落点 | 保持全部题干位置；答案页底部增加浅紫底与紫色强调条；结果26pt | 6组题答配对和位置核对，防止遮住文字 |
| P1 | 第65页两种压缩应用情境主次不清 | 情境标题27pt，解释23pt | 双栏视觉层次一致 |
| P2 | 优化中容易破坏页序或超出页面 | 审计70页顺序、70页备注、练习、图像、边界、PPTX结构 | 三轮JSON与PPTX构建均通过；最终PDF为70页 |

## AI图像模型提示词

A clean, minimalist vector diagram on a white background illustrates sound traveling from a vibrating silver tuning fork on the left to a modern desktop microphone on the right. Soft, translucent lavender and violet wave bands move across the open space between them, while the shaded microphone—with mesh grille, stand, base, and trailing cable—faces the fork to capture the incoming sound.

模型已生成图像参考。为了在教室投影时维持清晰、便于GitHub重建，实际加入第3页的是依据生成图构图制作的可缩放SVG教育图的高分辨率渲染，不是原始AI位图。图示中的传播部分明确设计为竖向声压扰动带，避免误导学生认为声波在空气中沿着一条正弦线前进。
图形源文件：validation/audio-v81-20261013/assets/sound-vibration-to-microphone.svg。

## 质量控制与待完成事项

构建脚本：validation/audio-v81-20261013/build_v81.py。各轮中间PPTX保存在GitHub Actions artifact（14天），各轮JSON审计长期保存在仓库。
通过：原v8未覆盖、70页、70页备注、6组题答、PPTX ZIP无损、插图存在、越界检查、PDF 70页。
本地重点渲染抽查：3、16、22、33、44、45、48、50、59、65、67页。
仍需Windows课堂实机核对Alibaba字体、投影清晰度及与JupyterLab演示切换；CI渲染不代表教室实机已验收。