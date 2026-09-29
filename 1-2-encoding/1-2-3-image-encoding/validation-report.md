# 图像编码课堂材料验证报告

更新版本：2026-09-29，course-design v1.4.9

## 本次修订

- PPTX 保持 26 页。所有页面的紫色轨道贴合画布边缘；标准问题标题统一为 `x=0.665 in`、`y=0.665 in`、`36 pt`，内容从 `y≥1.63 in` 开始。
- PPTX 原生文本、母版和主题字体明确指定 Alibaba PuHuiTi 3.0 的 115 Black、85 Bold 或 55 Regular 字体变体。
- Q7 的 BMP 说明缩短为适合投影的两行；Speaker Notes 将“第 54 个 byte”改为“从 offset 54 开始；按零起算是第 55 个 byte”。
- course-design.qmd 更新了已提交素材与本地验证状态，合并重复的材料对齐说明。
- 复核确认：Q3 第 12 页原本就有原生 RGB 数值表，16-color 和 2-color 的接缝数值与 course-design.qmd、slides.qmd 一致；因此没有增页。

## 本地核查结果

| 核查项 | 结果 |
|---|---|
| PPTX 包结构与页数 | ZIP 校验通过；26 页可由 LibreOffice 转为 PDF。 |
| 版式与字体 | 26 页轨道、标题坐标和字号、内容起点、画布边界均通过程序检查；所有原生文本使用上述三个字体变体。 |
| 证据与 Notes | Q3 原生表格数值核对通过；26 页均有 Speaker Notes；Q7 offset 措辞已核对。 |
| 视觉检查 | 26 页全部渲染为图片并检查整套缩略图；Q1、Q2、Q3、Q7、Q12 等页面另以单页尺寸检查。未见裁切或异常换行。 |
| Notebook | 在临时副本中按顺序执行教师版 11 个、学生版 6 个代码单元，均无异常。此次使用本地 Python 顺序执行，未验证 JupyterLab 界面操作。 |
| Quarto | course-design.qmd 可渲染为 HTML；slides.qmd 可渲染为 Reveal.js。 |

## 教室环境待验收

- 在 Windows 10 + conda `pt` 的教室机器上，通过 JupyterLab 完整运行教师版和学生版 notebook，并检查素材相对路径。
- 在 WPS / PowerPoint 中逐页放映 PPTX，检查字体实际解析、Speaker Notes、图像清晰度和投影效果。
- 教师确认 Q1、Q2、Q3 的观察停顿与整节课节奏。

本地渲染与程序检查不能替代上述教室环境验收。
