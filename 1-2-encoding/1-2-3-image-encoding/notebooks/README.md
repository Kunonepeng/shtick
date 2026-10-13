# 熊猫图像数字化交互实验台

本目录为 `1-2-3-image-encoding-panda-v4-20261011.pptx`（冻结85页）提供**可选教师演示**：原图 → 采样 → 量化 → 编码。不替换或修改冻结PPT、已有实验/图片，也不覆盖原 `demo-lab-student.ipynb`。

- 起始原型：[`panda-image-encoding-v0.ipynb`](panda-image-encoding-v0.ipynb)
- 知识正确性3轮审查基线：[`panda-image-encoding-v1.ipynb`](panda-image-encoding-v1.ipynb)
- 视觉优化第1–10轮：`panda-image-encoding-v1.1.ipynb`、`v1.2.ipynb`、`v1.3.ipynb`、`v1.4.ipynb`、`v1.5.ipynb`、`v1.6.ipynb`、`v1.7.ipynb`、`v1.8.ipynb`、`v1.9.ipynb`、[`panda-image-encoding-v1.10.ipynb`](panda-image-encoding-v1.10.ipynb)
- [知识正确性与十轮视觉审查记录](panda-image-encoding-audit.md)

## 运行方式

需要整个课程目录。Notebook 不是自包含网页；三个共享文件与原图、`demos/panda_lab.py`、`demos/panda-digitization/panda_samples.json` 都要保留。Python 代码/注释是英文；学生提问与显示文字使用中文。

本课已有依赖清单为 `requirements-notebook.txt`。在 Mac 备课环境、课程根目录运行：

```bash
python -m pip install -r requirements-notebook.txt
python -m jupyter lab
```

在浏览器里打开 `notebooks/panda-image-encoding-v1.10.ipynb`，运行准备单元和交互单元。若使用教室 Windows 的本地 `pt` 环境，则先把课程目录完整复制到 Windows 并进入对应目录，在 Anaconda Prompt 中：

```bat
conda activate pt
cd /d D:\dt\1-2-3-image-encoding
python -m pip install -r requirements-notebook.txt
python -m jupyter lab
```

`D:\dt\1-2-3-image-encoding` 是建议的课堂复制目标路径，需要实际将课程目录放到这个位置；不要误把它当作本机已存在的目录。若沿用声音课的远程架构，则 **Mac 负责 Jupyter 内核及计算，Windows Edge/Chrome 只负责打开同一个 JupyterLab 页面与显示控件**；Windows 不需要因此安装 Python。联网登录必须保留 Jupyter Token/密码，不要开放无认证公网服务。

在 Notebook 运行准备单元时会执行 `self_check()`：校验原图 SHA-256、预计算样本、四/六色量化结果、每像素位数和编码-解码往返。若失败，不要将数据结果投影为证据。运行后再用逐步揭示控制：

1. **原图**：先预测二维图像怎样留下样本。
2. **采样**：在固定区域上比较 8×8 与 16×16。
3. **量化**：保持网格不变，在四色与六色之间切换。
4. **编码**：点击一格，核对 RGB 均值 → 颜色等级 → 二进制码字；可点击本行码字反向聚焦格子。

演示只是一种**在既有 JPEG 解码像素上的概念模拟**，不是新拍摄的真实光学信号。码字数据量为未压缩、固定长度、连续打包的理想像素数据量，非文件大小。

## 对应课件与时间

- Q3–Q6（6–14页）：可用来验证采样／量化／编码的区别。
- Q7（19–22页）：优先做 8×8 vs 16×16 的位置对比。
- Q9（25–29页）：优先做固定16×16时的四色 vs 六色对比。

在原有45分钟课中**选一个**60–90秒短操作替代同页静态证据，而不是演示所有功能。交互失败超过30秒，回到已有 PPT 问答页。需要完整操作时放在加课时或课后。

## 版本归档与质量边界

v1.1–v1.10 采用**累积式功能开关**：每轮在上一版基础上启用一项新的投影/交互改进；v1.10 还针对点击面积及投影留白成组优化。所有版本共用 `panda_image_encoding_lab.py`、`panda-image-encoding-ui.js`、`panda-image-encoding-ui.css`，没有复制或替换原 JPEG。各版本的 Notebook JSON 含版本标识、轮次、功能集合；执行输出保持为空。

审查记录对源代码和固定数据有可复核证据，但目前**未**完成真实 Windows/JupyterLab 投影截图、字体检查和完整现场交互测量；不能把源码验收表述成教室视觉验收。下一次实际课堂运行应核对兼容性和投影可读性，并记录结果。
