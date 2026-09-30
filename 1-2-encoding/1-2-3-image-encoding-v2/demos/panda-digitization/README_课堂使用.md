# 熊猫图像数字化课堂 Demo

这个目录保存本课可直接运行的交互演示。它与课件构建用的 `scripts/` 分开，避免把“课堂运行程序”和“生成课件的工具脚本”混在一起。

## 学习目标

用同一只熊猫的采样数据，让学生通过控制变量看到：

**采样 → 量化 → 编码**

建议课堂主路径只有三步：

```text
8×8，4色
→ 16×16，4色
→ 16×16，6色
```

这正好对应课件“三轮熊猫实验”。

## 文件

- `panda_digitization_demo.py`：课堂主程序
- `panda_samples.json`：从本课 `assets/pandas.jpg` 同一裁切区域预计算出的 8×8 / 16×16 平均 RGB 样本
- `AUDIT.md`：部署与教学审核记录

程序**不需要 Pillow、numpy、matplotlib 或 py5**；运行时只使用 Python 标准库。

## 教室运行（Windows 10 / Miniconda / pt）

从仓库根目录复制整个目录到：

```text
D:\dt\panda-digitization
```

然后在 Anaconda Prompt 中：

```bat
conda activate pt
cd /d D:\dt\panda-digitization
python panda_digitization_demo.py --self-test
python panda_digitization_demo.py
```

若课前检查出现：

```text
SELF-TEST PASS
```

说明数据文件与程序结构完整。

## 建议课堂流程（约 6–8 分钟）

先显示默认状态：**8×8、4色**。

先问学生：

> 这只数字熊猫为什么这么粗糙？如果只允许改一个参数，你会改什么？

然后只把采样从：

```text
8×8 → 16×16
```

保持 4 色不变。追问：

> 可选颜色没有增加，为什么轮廓和五官仍然能表达得更细？

收束：**采样位置更多，空间细节表达更细。**

接着保持 16×16 不变，只把：

```text
4色 → 6色
```

追问：

> 格子数量完全没变，这一次改善的是什么？

收束：**可选颜色更多，量化时有更多近似选择。**

最后点击任意格子，让学生读底部链条：

```text
采样 RGB
→ 量化后的颜色编号
→ 固定长度二进制码字
```

4 色时每像素需要 2 bit；6 色时最少需要 3 bit。

## 快捷键

```text
1 / 2       → 8×8 / 16×16
Q / W       → 4色 / 6色
Ctrl + R    → 重置
```

## 为什么左边不是再次显示原始照片？

课件已经负责展示原始熊猫图。本 Demo 从“采样已经发生”这一环节开始：

- 左边：每个采样区域留下的**平均 RGB 样本**；
- 右边：把这些样本映射到有限调色板后的**量化结果**。

这样学生能直接比较“采样改变了什么”和“量化改变了什么”，不会把演示变成单纯的图像滤镜。

## 数据来源与技术边界

`panda_samples.json` 来自本课已有的 `assets/pandas.jpg`，使用与课件一致的裁切区域与平均 RGB 采样数据；四色/六色调色板也沿用本课构建数据。

这是课堂概念模型，不模拟真实相机的曝光、Bayer 阵列、去马赛克、噪声、色彩管理等物理过程。这里的“采样”指在二维空间中取得有限位置/区域的代表值；“量化”指把样本映射到有限等级；“编码”指把颜色编号写成固定长度 bit。

## 仓库位置

```text
1-2-encoding/
└── 1-2-3-image-encoding-v2/
    ├── assets/
    ├── scripts/              # 课件构建工具
    └── demos/
        └── panda-digitization/
            ├── panda_digitization_demo.py
            ├── panda_samples.json
            ├── README_课堂使用.md
            └── AUDIT.md
```
