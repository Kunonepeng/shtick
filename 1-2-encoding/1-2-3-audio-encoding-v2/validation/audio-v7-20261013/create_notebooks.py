from pathlib import Path
import nbformat as nbf
root=(Path(__file__).resolve().parent / 'remote_demos' / 'notebooks')
if not (Path(__file__).resolve().parent / 'remote_demos').exists():
    root=Path(__file__).resolve().parents[2] / 'remote-demos-v7' / 'notebooks'
root.mkdir(parents=True,exist_ok=True)

def note(filename,parts):
    n=nbf.v4.new_notebook()
    n.cells=[nbf.v4.new_markdown_cell(a) if typ=='md' else nbf.v4.new_code_cell(a) for typ,a in parts]
    n.metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}}
    nbf.write(n,root/filename)

bootstrap='''from pathlib import Path
import sys
# 允许从项目根目录或notebooks目录打开Notebook。
here = Path.cwd().resolve()
project = here if (here / "lesson_audio_v7").is_dir() else here.parent
if not (project / "lesson_audio_v7").is_dir():
    raise RuntimeError("请从 remote-demos-v7 或其 notebooks 目录启动 JupyterLab")
if str(project) not in sys.path:
    sys.path.insert(0, str(project))
'''
note('01_听见声音_看见波形.ipynb',[
 ('md','# Demo A｜听见声音，看见波形\n\n**对应v7：第一课时“波形图画的是传播路线吗？”之后。**\n\nMac负责生成合成音频，Windows浏览器负责播放并移动红色时间光标；**不是Mac扬声器播放**。\n\n### 先预测\n- 波形横轴表示时间，还是声音传播的距离？\n- 播放光标往右移动时，意味着什么？'),
 ('md','运行下方单元。第一次运行前，请在 **Mac Jupyter内核使用的Python环境** 安装 `anywidget`（参看README）。'),
 ('code',bootstrap+'\nfrom IPython.display import display\nfrom lesson_audio_v7 import listening_demo\n\ndisplay(listening_demo())'),
 ('md','### 观察与解释\n1. 在**教室Windows浏览器**点击播放器上的播放键，确认教室音箱有声音。\n2. 对照红色光标和时间刻度。\n3. 让学生解释：图上横轴是时间；纵轴是数字录音的信号幅度。\n\n**注意**：这是数字样本生成的可见波形，不是声波在空气中前进的轨迹。完整波形使用“分段最大/最小值”概览，不能把概览图每根竖线当作一个采样点。')
])
note('02_放大波形_看见采样点.ipynb',[
 ('md','# Demo B｜放大波形，找到真实采样点\n\n**对应v7：第一课时“每隔相同时间取一个值”之后。**\n\n### 先预测\n- 如果把4秒的图放大到4毫秒，会发生什么？\n- 图上的密集波形是否真的记录了每一个时刻？'),
 ('code',bootstrap+'\nfrom IPython.display import display\nfrom lesson_audio_v7 import zoom_demo\n\ndisplay(zoom_demo())'),
 ('md','### 教师操作（不超过3分钟）\n1. 先让学生观察整段4秒波形。\n2. 将局部范围从**100毫秒 → 20毫秒 → 4毫秒**，观察蓝色小圆点。\n3. 点击完整波形不同位置，比较样本密集程度是否变化。\n4. 请学生说出：采样率指每秒记录多少个样本。\n\n**技术说明（教师用）**：播放和绘图发生在浏览器；Mac只负责生成和传送PCM样本。长波形使用极值包络，放大区实际显示原始样本。图中连接点的细灰线仅用于辅助视觉理解，不代表必须这样还原声音。')
])
note('03_采样_量化_编码实验台.ipynb',[
 ('md','# Demo C｜从连续波形到二进制码字\n\n**对应v7：第一课时“量化 → 编码”。优先使用的课堂核心实验。**\n\n这是**4毫秒的放大教学模型**；可改变采样率(2/4/8 kHz)与量化位数(2/3/4 bit)，用于放大理解，不是推荐的录音参数。\n\n### 两个预测\n- 提高采样率，改变的是点的横向密度，还是量化等级？\n- 保持采样时刻不变，3 bit改4 bit，样本点数量会变吗？'),
 ('code',bootstrap+'\nfrom IPython.display import display\nfrom lesson_audio_v7 import encoding_lab\n\ndisplay(encoding_lab())'),
 ('md','### 操作顺序（约5分钟）\n1. 选择 **① 原波形**：指出横轴（时间）、纵轴（幅度）。\n2. 选择 **② 采样**：固定3 bit，逐步改变采样率，比较横向样本点数量。\n3. 选择 **③ 量化**：固定采样率，比较2、3、4 bit对应的纵向可选等级。\n4. 选择 **④ 编码**：点击任一蓝色样本点，观察等级编号及等长二进制码字。\n5. 最后让学生复述：采样回答“何时记录”，量化回答“记录成哪个近似值”，编码回答“如何表示等级编号”。\n\n**规则**：采用均匀mid-rise量化，仅作教学实例；同一采样值可依据所选位数落入不同区间。灰色平滑线是预先给定的信号参考，并非用采样点简单连线重建的波形。'),
 ('code','''# 可选：在Mac内核直接检查一个量化实例，显示模型的数据依据。
from lesson_audio_v7 import quantize
for bits in (2, 3, 4):
    level, value = quantize(0.37, bits)
    print(f"{bits} bit：等级 {level}，代表值 {value:.3f}，码字 {level:0{bits}b}")''')
])
note('04_压缩前先预测.ipynb',[
 ('md','# Demo D｜同样1000字节，为什么压缩后大小不同？\n\n**对应v7：第二课时“两个文件都1000 Byte，压缩后谁更小？”之后。**\n\n本演示只使用Python标准库 `zlib`；计算发生在Mac，结果显示在Windows浏览器。**无需py5或音频设备。**'),
 ('md','### 先预测\n文件A：1000个重复的`A`。文件B：1000个随机变化的字节。\n\n请学生分别预测：谁压缩后更小？是否可能压缩后反而变大？'),
 ('code',bootstrap+'\nfrom lesson_audio_v7.core import compression_data\nfor row in compression_data():\n    print(f"{row[\'label\']}：原始 {row[\'before\']} Byte → 压缩后 {row[\'after\']} Byte")'),
 ('md','### 追问\n- 为什么两份文件原始大小相同，压缩效果却不同？\n- 无损压缩节省的并不是“字母A本身”，而是更高效地记录重复和规律。\n- 这能否解释纯色图像通常比细节丰富的照片更容易无损压缩？\n\n**教师提示**：随机数据有可能压缩后略大，因为格式本身存在必要的管理开销；这是有效的认知冲突，不应暗示压缩必定减小所有文件。')
])
print('notebooks:',[p.name for p in root.glob('*.ipynb')])
