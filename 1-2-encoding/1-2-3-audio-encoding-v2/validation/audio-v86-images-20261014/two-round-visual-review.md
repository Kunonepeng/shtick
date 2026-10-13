# v8.6.with-images-by-gpt：素材筛选、两轮评审与复验

**输入：** GitHub main 的 v8.6.gpt.pptx（77页）与 v8.4.10-searched-images/source.md（70页参考映射，assets目录52份素材）。**输出：** v8.6.with-images-by-gpt.pptx（79页）。不改旧课件的77页原文、原生数据图、练习题与已有备注。原v8.6.gpt不覆盖。

## 素材匹配：按照教学内容，而不是直接按页号

| 选用图像 | 来源source.md推荐位置 | 对应v8.6原页 | 最终版页 | 课堂作用 |
|---|---|---|---|---|
| microphone-studio.svg | 5 | 5 | 5 | 识别声波转模拟电信号的实际设备 |
| speaker-high.svg | 28 | 28 | 28 | 识别DAC后面的声音输出设备 |
| computer-disk.svg | 35、57等 | 54 | 56 | 表示本地数据存储需求 |
| smartphone.svg | 51等 | 54 | 56 | 表示网络传输的应用设备 |
| audacity-multitrack-mixing.png | 39–41 | 44之后 | 45、46 | 真实软件中1条Mono轨道显示1路波形，1条Stereo轨道显示2路波形。借此区分编辑音轨与输出声道 |

未使用全部52份素材。采样点、量化等级、二进制编码、PCM及视频数据量、无损/有损图等已有更准确的原生证据，强行添加外部图片只会增加负担。尤其没有使用带复杂英文电磁结构标注的speaker-soundwave动画帧，避免偏离高中课程目标。

## 第一轮：筛选图片并建立真实情境

| 级别 | 问题 | 采取的修订 | 审计证据 |
|---|---|---|---|
| **P0** | 真实截图中上下共3行波形，易让学生误认为输出文件一定是3个声道 | 将截图放在原44页混音关系图后，先提问学生数“音轨”与“波形”，Speaker Notes指出不能据此推断导出声道数量 | 页序检查、源页文本不变、备注正确 |
| **P1** | 抽象的麦克风/扬声器文字框与物理设备联系较弱 | 在原5、28页流程下放相关图标，不遮挡现有箭头和解释 | 渲染两页确认关系清晰 |
| **P2** | 节省空间和传输效率只有文字，不便快速联系经验 | 在原54页分列放磁盘、手机两图标 | 保留两列原文字及结论 |

**Round 1：** 78页；原77页文字逐页一致；78页含Notes。独立文件round-1-with-images.pptx，审计audit-round-1.json。

## 第二轮：理解检验、中文揭示和视觉复核

| 级别 | 复查问题 | 修订 | 复验 |
|---|---|---|---|
| **P0** | 单张截图的观察任务缺少明确的后续揭示，可能让“音轨=声道”的误读持续 | 制作同版式的第46页答案页，第45页仍仅观察，让学生先判断再翻页；明确两条编辑音轨并不等于两个或三个导出声道 | 问题与答案页的截图、标题均原位；原练习题3答案仍在第47页 |
| **P1** | Audacity截图英文小标签使部分高中生不易区分Mono与Stereo | 紫色/青色聚焦框突出上下一条轨，并显示中文“上：一条单声道音轨；下：一条立体声音轨（L/R两路）” | 渲染中两框围住正确区域，且没有涂改原截图 |
| **P2** | 磁盘和手机可能沦为装饰图 | 增加“本地存储”及“在线传输”短标签，在备注中说明图片是情境不是压缩率证明 | 图标/标签中心对齐，原结论可见 |

**Round 2：** 79页；79页Notes；输出与第二轮快照字节相同。audit-round-2.json包含源SHA、最终SHA和三项分级修订清单。

## 图像来源及许可

- OpenMoji contributors / HfG Schwäbisch Gmünd，CC BY-SA 4.0；使用microphone-studio、speaker-high、computer-disk、smartphone SVG，按原图形转换为高分辨率PNG嵌入。原链接与授权见source.md，具体来源标记在相应幻灯片Speaker Notes；复用与改编须遵守署名与ShareAlike要求。
- Audacity Manual contributors，CC BY 3.0；audacity-multitrack-mixing.png，原图：https://github.com/audacity/audacity-manual/blob/master/manual/m/images/f/fb/tracks_for_mixing.png。截图来自历史版本，只用作音轨/声道概念解释，不代替最新版软件操作说明。两页Speaker Notes列出来源。
- KyleThayer声波动画（CC0）本次未使用。

## 验证与局限

GitHub Actions对两轮源文件、原版SHA256、全部原页文本完整性、两轮Notes、分级问题修复记录、答案揭示顺序、79页最终PPTX与第二轮文件字节一致进行核验。两轮重点页用带中文字体的LibreOffice渲染并人工查看：麦克风、扬声器、Audacity两页渐进揭示以及存储/传输两列均清晰，无明显遮挡。

保留实机验收边界：实际Windows PowerPoint/WPS字体换行、Mac远程Jupyter演示、校园网络、投影与课堂45分钟节奏未在此轮测试，不能仅凭CI通过判定这些已验证。
