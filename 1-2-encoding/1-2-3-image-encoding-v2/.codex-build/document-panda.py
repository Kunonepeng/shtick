from pathlib import Path
import json
r=Path(__file__).resolve().parent.parent; d=json.loads((r/'.codex-build/panda-data.json').read_text()); plan=json.loads((r/'.codex-build/slide-plan-panda.json').read_text())
text='''# 图像编码：熊猫版课堂改编说明

## 版本与依据

- 课堂文件：`exports/1-2-3-image-encoding-panda-v1.pptx`。
- 教学依据：`course-design.qmd` 的 Q0–Q22；保留认知困惑、问题链、活动顺序、位图与矢量图的短比较、RGB、数据量、AI修复、模拟量与数字量的收束。
- 本版是另一套素材实施方案。原课史料及原花朵矩阵继续由 `course-design.qmd` 记录。本说明集中列明经用户确认的素材与参数变化，避免把熊猫数据误认成原课堂记录。
- `slides.qmd` 不参与本次制作。旧PPTX保留。
- 56页；25组问答页通过复制原问题页后添加答案形成。所有教学页都有逐字稿，教师问题、预期回答、追问、技术边界及来源置于Speaker Notes。

## 熊猫素材与取样

用户提供 `assets/pandas.jpg`，原尺寸886×1000。它是数字角色插图。Q2使用“把图打印在纸上，再由相机拍摄”的思想实验连接反射光与传感器。

所有三轮网格使用同一头部区域：左上角(x,y)=(280,100)，宽高288×288。源坐标从0开始；课堂行列从1开始。原图通过PPT原生裁切显示，原文件未修改。8×8和16×16分别将该区域分成36×36、18×18源像素大小的块，对各块的解码RGB通道取算术平均，再选距平均颜色最近的调色板颜色。距离为三个通道平方差之和，平局选择较小编号。

这些网格是原图片计算所得的教学模型，使用可编辑PPT矩形表示；不是手画的熊猫编码，也不是AI生成的技术证据。RGB平均没有在线性光空间完成，不能当作真实相机采集流程的精确模拟。提高采样分辨率时重新读取原图，保持取样范围、显示大小和调色板不变。

## 三轮实验与计算

|轮次|分辨率|可选颜色|每像素最少位数|像素数据量|
|---|---|---|---|---|
|建立编码模型|8×8|4|2 bit|128 bit = 16 B|
|只增加采样位置|16×16|4|2 bit|512 bit = 64 B|
|只增加颜色等级|16×16|6|3 bit|768 bit = 96 B|

这些是固定长度码字紧密排列的理论像素数据量，不包含调色板、文件头、对齐填充或压缩影响。示例不是某一种实际文件格式的大小。

## 固定码表

前四种颜色按从深到浅编号。六色版本保留前四色及其颜色编号，增加两种中间色；所有码字统一扩为3bit。

|编号|RGB|Hex|四色码字|六色码字|
|---:|---|---|---|---|
'''
for i,(rgb,hx) in enumerate(zip(d['paletteRgb'],d['palette'])):text+=f"|{i}|{', '.join(map(str,rgb))}|{hx}|{format(i,'02b') if i<4 else '不使用'}|{format(i,'03b')}|\n"
text+=f'''\n三幅网格实际使用了4、4、6种颜色。两种16×16网格采用相同的块均值。六色调色板是四色的超集，因此最近颜色的距离不会增加。本例RGB通道均方误差由{d['mse4']:.6f}降至{d['mse6']:.6f}，下降{100*(1-d['mse6']/d['mse4']):.2f}%。这是本次计算模型的误差，仅用于核对颜色近似，不作为感知质量指标。\n'''
for key,label in [('coarse','8×8、四色'),('fine','16×16、四色'),('six','16×16、六色')]:text+=f"\n### {label}颜色编号矩阵\n\n从上到下、从左到右；每个数字为一个像素的颜色编号。\n\n```text\n"+'\n'.join(d[key])+"\n```\n"
text+='''
## 学生读码练习

为保持投影可读性，从16×16四色图取**第6行、第5–12列**的8个像素。原图标红框，右侧显示相同的8格色条，问题页仅给码表，下一页才揭示编码。

- 编号：3、3、1、0、0、1、3、0。
- 码字：11、11、01、00、00、01、11、00。
- 8个像素，每像素2bit，共16bit = 2B。

## 像素放大与RGB证据

Q1和Q17均放大原JPEG中(x,y)=(417,220)开始的16×16源像素。每个PPT矩形填入对应源像素的实际RGB值，不插值，也不增加细节。

Q15读取零起始坐标(422,230)处的RGB值：

|通道|十进制|8位二进制|
|---|---:|---|
|R|138|10001010|
|G|179|10110011|
|B|111|01101111|

红框中心对应被读取的像素，色块显示同一RGB值。每像素24bit = 3bytes。这是JPEG解码后的RGB视图；JPEG文件本身不逐像素直接存放这样的三个连续通道字节。

Q16继续采用课程设计中的500×333、24bit计算题，明确写成假设条件，避免误当熊猫原图尺寸。结果499500B≈487.79KiB；删除原花图的Photoshop与487KB属性截图，改为可编辑的像素数据／文件信息说明。

Q18沿用原课人物破损照片与修复结果，保持原课“修复是推断”的论证，未替换或生成新的修复证据。

## 教学节奏

沿用课程设计的45分钟安排。56页中大量是同一问题的揭示页，不应按56个独立话题讲授。先预测再翻页：Q1、Q3–Q7、Q9、Q11–Q16为主要思考与计算停留点；Q8短讲，Q18根据课堂时间控制讨论。备注可直接作为授课讲稿使用。

## 可复算文件

- `.codex-build/analyze-panda.py`：读取原素材，计算区域均值、颜色编号、真实像素、读码练习及误差。
- `.codex-build/panda-data.json`：完整数据，包含源图SHA-256、原图尺寸、取样区域和RGB均值。
- `.codex-build/build-panda.mjs`：从课程讲述数据和熊猫数据创建PPTX，所有问答页调用duplicate()。
- `.codex-build/lesson-teaching-panda.json`：本版Q1–Q21讲述数据。
- `.codex-build/check-panda.py`：字体、备注、原问题页几何与计算检查。
- `.codex-build/finalize-panda.mjs`：最终PPTX包与布局验证。

未使用AI生成或修改图片，无新增生成提示词。原图仅以原生PPT裁切取景；精确网格由数据驱动的原生PPT对象构成。

## 技术核对来源

- [Pillow：模式、RGB三通道、坐标](https://pillow.readthedocs.io/en/stable/handbook/concepts.html)
- [Microsoft：Bitmap Storage](https://learn.microsoft.com/en-us/windows/win32/gdi/bitmap-storage)
- [NIST：二进制前缀](https://physics.nist.gov/cuu/Units/binary.html)
- 原课堂逐字稿和投影照片、`course-design.qmd` 中的原始证据及技术注解。

## 逐页对应

|页|问题|阶段|学生此刻看到|
|---:|---|---|---|
'''
for s in plan['slides']:text+=f"|{s['slide']}|{s['q']} {s['title']}|{s['stage']}|{s['visible']}|\n"
(r/'panda-deck-design.md').write_text(text)
