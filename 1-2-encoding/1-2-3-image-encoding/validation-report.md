# 图像编码课堂材料验证报告

更新版本：2026-09-29 修订版

## 已完成的修订

- PPTX 已重排为 26 页：Q1 与 Q2 的证据页先只展示图像，结论页在学生观察之后再揭示。
- PPTX 标题几何与字号已按当前反馈收紧：标准标题统一放在 `y=0.48 in` 附近，采用 30 pt；封面主标题为 60 pt。
- Q1 证据页拆为两页三图比较：`256 / 64 / 32` 与 `32 / 16 / 8`，32×32 作为跨页衔接。
- Q2 反例图已重建为同一 4:3 场景构图：`1600×1200` Gaussian blur simulation 与 `800×600` sharp image，避免 16:9 / 4:3 导致的形变干扰。
- Q3 图片与 PPTX 证据使用同一批 notebook 导出的 fallback 文件；接缝 `(72,40)` / `(73,40)` 的结果为：16-color 两侧不同，2-color 两侧相同。
- 教师版 notebook 已恢复 Q6 Demo C（RGB → bits）和可选 BMP `biBitCount` 检查。
- 学生版 notebook 在 Q6 代码前加入了书面预测提示。
- Reveal.js 参考版 `slides.qmd` 已同步新的 Q1/Q2/Q4/Q12 揭示顺序。

## 本地生成与核查

本次材料包在当前环境中完成生成：

- fallback PNG：已生成；
- Q2 PNG：已生成并检查尺寸；
- Q7 BMP：已生成并检查 `pixel-data offset = 54`、文件大小 `78 bytes`；
- PPTX：可由 LibreOffice headless 转为 PDF，并生成 26 页；
- Speaker Notes：PPTX 26 页均包含 notes；
- notebooks：教师版与学生版为可运行结构，包含路径检查和必要断言。

## 仍待课堂交付前确认

- Windows 10 + conda `pt` 环境下实际运行两版 notebook；
- WPS / PowerPoint 中检查 Alibaba PuHuiTi 字体替换、字号和版式；
- 教室投影环境下检查 Q1、Q2、Q3 图像对比是否足够清晰；
- 若使用 PPTX 作为正式授课材料，应在目标环境中逐页放映一次，确认 notes、图片和中文字体均正常。

## 备注

当前报告只确认本地材料生成与逻辑一致性，不能替代教室 Windows/WPS 环境验收。
