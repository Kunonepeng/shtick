# v7 三轮质量评审与修订记录

评审对象：\`1-2-3-audio-encoding-v7.pptx\`、\`remote-demos-v7/\` 的4个Jupyter Notebook、Python数据模型与浏览器绘制代码。目标环境：Mac上的JupyterLab服务端；教室Windows 10通过浏览器访问、播放声音及投影。

等级：**P0** = 阻塞构建或课堂核心演示；**P1** = 明显影响教学理解、交互或稳健性；**P2** = 可维护性、表述或小幅体验改进。每轮先检查，再修改，再复验；复验只能证明已执行的检查，不能代替教室实测。

## Round 1：架构、计算与交互正确性

| 等级 | 问题 | 修订 | 复验与结论 |
|---|---|---|---|
| P0 | 只有本地生成文件，没有在GitHub中可复现的发布流程。 | 添加\`.github/workflows/publish-audio-v7.yml\`，上传构建源码，CI从真实v6重建v7，自动校验并推送。 | GitHub Actions run **38387700351** success：安装、样本测试、Notebook验证、PPTX构建和推送全部成功。**已解决**。 |
| P1 | Demo B点击整段波形时，忽略Canvas左侧坐标轴空白，观察位置偏移。 | 按真实绘图区 \`[x0,x1]\` 而不是整块Canvas宽度换算时间位置。 | Chromium交互回归覆盖点击图形两端，定位范围符合预期，无JS页面异常。**已解决**。 |
| P1 | 代码对播放器和量化结果缺少系统性单元测试。 | 加入\`tests/test_core.py\`，覆盖WAV参数、包络、采样点数、量化码字边界、压缩实验。 | 6项单元测试通过；远程GitHub CI重复通过。**已解决**。 |
| P2 | 压缩测试中留有无用的临时数据生成代码。 | 去除死代码，仅保留带固定种子的伪随机数据。 | \`test_compression_theory\`验证两份原始数据均为1000字节且压缩差异符合预期。**已解决**。 |

## Round 2：教学问题链、图示与学生认知

| 等级 | 问题 | 修订 | 复验与结论 |
|---|---|---|---|
| P1 | 原v7的Demo C插在学生认识“3 bit → 8级”之前，就提问“3 bit变4 bit会怎样”，概念铺垫不足。 | 将演示C移到“一个样本需要几个二进制位”之后，即最终第22页；重定位教师备注，保留v6内容顺序。 | 渲染第22页核查前后逻辑；CI逐页比较v6与v7内容，原64页顺序全部保留，演示引导位于第9、12、22页。**已解决**。 |
| P1 | 浏览器图形的右侧“时间”标签与最右侧刻度容易重叠。 | 将“时间 (s)”移到底部中央，左右刻度分开。 | Chromium实际截图检查Demo A/B/C；没有发现时间标签覆盖。**已解决**。 |
| P2 | 学生可能把完整波形的极值概览误认为一个个原始采样点，或将实验台的[-1,1]幅度误认为幻灯片的0～7等级值。 | Notebook和Speaker Notes明确区分“全局极值包络/局部真实样本”“归一化演示模型/0～7课堂教学模型”。 | 检查Notebook讲解文字、样本数据和对应备注；模型数据测试通过。**已解决**。 |

## Round 3：投影、运行开销、部署与最终回归

| 等级 | 问题 | 修订 | 复验与结论 |
|---|---|---|---|
| P1 | 播放器无论状态如何按显示刷新率重绘，可能导致教室浏览器无意义的高CPU占用。 | 重绘上限约15FPS，页面隐藏时跳过重绘；播放仍由浏览器\`HTMLAudioElement\`维护。 | Chromium三种组件的交互测试与JS异常监测通过。**已解决**。 |
| P1 | Demo B的两张波形在投影低分辨率时可能超出一屏。 | 缩短两张Canvas的高度、保留文字可读性，README建议F11全屏或适当页面缩放。 | 检查浏览器截图及实际布局；相比初版减少纵向占用，必要时仍可滚动。**已改进**。 |
| P1 | 远程Jupyter认证与代码执行权限的风险需要更明确告知任课教师。 | README明确只允许教师登录、保留token/密码，避免公网映射，优先校园受控网络/HTTPS/VPN。 | 查阅README对应章节，配置建议完整。**文档已解决；校园实际网络安全需管理员确认**。 |
| P2 | 最终文件集缺少可重复的浏览器交互检查方法。 | 增加可选\`tests/browser_smoke.py\`（Playwright/Chromium），检查三个演示组件、音频数据URL、放大区控制、量化控件、截图和JS错误。 | 本地Chromium无页面错误；GitHub Actions安装\`anywidget\`后实际实例化三个Widget通过。**已解决**。 |

### 最终自动化复验

- 远程构建：[GitHub Actions run 38387700351](https://github.com/Kunonepeng/shtick/actions/runs/38387700351) → **success**。
- 课件：**67页、67页非空Speaker Notes**，原v6的64页全部在原先顺序上保留，新增3页演示锚点（第9、12、22页）。
- JupyterLab：4个Notebook均通过\`nbformat.validate\`；3个\`anywidget\`对象成功实例化。
- Python：6项基础数据模型测试通过；JavaScript通过\`node --check\`；本地Chromium交互与截图检测无未处理JS异常。
- 浏览器音频使用内嵌WAV，声源和声音输出在**Windows浏览器端**；Mac执行Python计算，不依赖py5独立窗口或Mac扬声器。

### 尚需真实教室验收（不是已验证结果）

自动化测试不能代替“教室Windows浏览器访问实际Mac Jupyter服务”的整链路演示。授课前必须在最终校园网络环境中验证：Jupyter认证与访问权限、Windows音箱输出、播放暂停和拖动、4毫秒放大图、Widget通信、Mac防休眠及投影字体。此项属于**部署验收门槛**，在实际测试前不得视为完成。若失败，回退到PPT静态图示，核心课程不依赖Notebook在线运行。

### 手动运行检查

\`\`\`bash
# 在Mac项目目录 remote-demos-v7 内，使用Jupyter的Python环境
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
# 已另行安装 playwright 与 chromium 的开发机：
PYTHONPATH=. python tests/browser_smoke.py
\`\`\`

该记录对应的是针对这份v7项目源码的三轮具体评审，并非声称已经在教室Windows机器上完成实机测试。
