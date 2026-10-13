# 声音的数字化 v7 · 远程 JupyterLab 课堂演示

## 对应的运行架构

- **macOS**：JupyterLab、Python内核、音频数据生成与采样/量化计算。
- **教室Windows 10**：仅用Edge/Chrome访问Mac的JupyterLab，在浏览器里播放声音、显示波形、点击互动控件。
- 不调用Mac扬声器，不使用Mac的py5独立图形窗口。**Windows不需要安装Python、Java、py5或FFmpeg。**
- 浏览器可视化由 Notebook 代码单元直接输出的 HTML/CSS/JavaScript 构成，不依赖 `anywidget` 或额外前端扩展，也不从CDN加载JavaScript。**需要重新执行代码单元，才能获得可信的动态输出。**不采集麦克风，使用课堂合成音频。

## 安装（只在Mac的Jupyter内核环境中做一次）

在Mac本地仓库的 `1-2-encoding/1-2-3-audio-encoding-v2/remote-demos-v7` 目录运行：

```bash
# 首先激活Mac上用于Jupyter的Python/Conda环境（不是Windows pt环境）
python -m pip install -r requirements.txt
jupyter lab --no-browser --ip="192.168.1.20" --port=8888
```

以上 `192.168.1.20` 仅为示例，请替换为Mac实际所在受控校园局域网的IP，或使用由校方管理的HTTPS/VPN接入方式。**保留Jupyter token/密码认证；不要把端口暴露到公网，也不要禁用认证。** 确保教室Windows能够访问Mac，Mac不要睡眠。

教室电脑浏览器打开 `http://<MAC_LAN_IP>:8888/lab`，登录后打开本目录下的 `notebooks/`，按顺序运行Notebook。

如果在不受信任的网络访问，请部署受信任的HTTPS反向代理或VPN，避免直接传输Jupyter凭据。

## 四个课堂演示

| 文件 | PPT建议位置 | 用时 | 目的 |
|---|---|---:|---|
| `01_听见声音_看见波形.ipynb` | 第一课时“波形图是什么” | 2分钟 | 音频与时间波形建立联系 |
| `02_放大波形_看见采样点.ipynb` | 第一课时“采样” | 3分钟 | 放大直到看到实际样本点 |
| `03_采样_量化_编码实验台.ipynb` | 第一课时“量化与编码” | 5分钟 | 同一条波形比较时间取样、幅度等级和二进制码字 |
| `04_压缩前先预测.ipynb` | 第二课时“冗余与压缩” | 2分钟 | 通过真实压缩结果解释规律性/冗余 |

**时间管理**：第一课时的10分钟演示应替换v6已有的部分静态解释，而不是在原45分钟上加10分钟。第二课时保留原视频计算、音轨冲突等问题链。

## 技术特点与限制

1. 浏览器播放基于原生 `HTMLAudioElement`，必须由教师点击播放；使用其 `currentTime` 驱动播放光标，不依赖Mac与Windows时钟同步。
2. 图像通过浏览器 Canvas 绘制。显示包含两类不同数据：全局波形用极值包络以保留瞬态；局部放大才画真实样本点。
3. 样本在Mac端生成；量化采用均匀mid-rise演示规则，模型可显示2、3、4 bit等级及码字。不代表实际录音系统所有量化算法。
4. 本例2/4/8 kHz采样率只是4毫秒放大教学模型，不建议将其作为日常录音配置。
5. 由于浏览器、Jupyter扩展及音频输出设备差异，课前需在教室Windows浏览器中测试。远程JupyterLab不等于Mac独立GUI远程桌面。
6. 交互界面依赖正在运行的Notebook单元格生成的 JavaScript 输出。首次从其他机器打开时，执行代码单元（JupyterLab可能提示需要信任Notebook）；保存的`.ipynb`不是脱离服务器可直接交互的离线网页。

## 投影建议与操作权限

- 推荐教室Windows使用Edge或Chrome，按F11进入浏览器全屏；Notebook输出区域可适当缩放至80%～90%。
- 仅教师登录远程JupyterLab。**登录Jupyter即意味着可以在Mac上执行Python代码**，不要向学生公开服务器地址、访问Token或Notebook内核访问权限。
- Notebook与浏览器控件代码来自可信仓库；为避免在公网暴露执行环境，不使用无认证的外网端口映射。

## 课前测试（在Windows上）

- 可以登录JupyterLab，Notebook 01运行后出现播放器，声音从教室音箱输出。
- 播放红色光标随音频位置变化，暂停/拖拽播放条后更新。
- Notebook 01可点击重播，观察四段声音的波形变化与红色时间光标。
- Notebook 02能在100/20/4毫秒切换，点击蓝色样本点能读取该点的序号、时间与幅度；上方概览与下方真实样本应区分。
- Notebook 03在2/3/4 bit切换时样本数不变，在2/4/8 kHz切换时样本数改变；等级虚线清楚，点击样本或二进制码字会同步高亮，区间表与量化代表值一致。
- Notebook 04的结果反映高重复内容更容易压缩。
- 关闭Mac屏幕但不要使Mac睡眠；整堂课能保持网络、内核与播放器工作。

## 故障应急

- 若仍出现旧版 `AnyModel` 或 `anywidget` 报错：请在本地 `git pull` 更新文件，清除相关Notebook的旧输出，重启Kernel并重新运行Cell。
- 页面没有控件：确认JupyterLab Notebook为信任状态，执行代码单元后观察是否出现HTML/JavaScript输出；按浏览器F12查看Console报错。不要关闭Jupyter身份认证。
- Windows端音频不自动播放：这是浏览器的正常限制，需要教师主动点击播放键。
- 没有声音：确认是Windows教室音箱、浏览器播放权限、系统音量；**不是查看Mac的声音输出**。
- 网络/内核中断：使用PPT里的静态波形图讲解；核心知识点不依赖演示成功。
