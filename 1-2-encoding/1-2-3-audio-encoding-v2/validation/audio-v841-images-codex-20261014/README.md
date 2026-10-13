# v8.4.1 图片修订副本入口

本记录只服务本次用户指定的`1-2-3-audio-encoding-v8.4.1.with-images-by-codex.pptx`。[教学约定](course-design.qmd)、[两轮问题与验收](review-and-acceptance.md)、[图片来源](image-provenance.md)、[完整阶段逐字稿](transcripts.md)。不改变本课其他正式版本的身份。

|路径（相对本目录）|角色/所有者|
|---|---|
|../../1-2-3-audio-encoding-v8.4.1.with-images-by-codex.pptx|本任务交付PPTX，108页，可编辑原生文本/曲线/树；SHA `d14ff8fd862846d144c705c1ecd69890c1e56185a8abaf4ca2adda0ec17a3ab9`|
|../../1-2-3-audio-encoding-v8.4.1.pptx|用户明确保护的70页原件；SHA `89c98e5bdf3fea00b39c159af52ea9d1061e7be3c126fd0deaf7f2df5c8c955e`|
|../../1-2-3-audio-encoding-v8.4.10-searched-images/source.md 与 assets/|既有52项图像及逐页候选，本次只读；来源身份见image-provenance|
|course-design.qmd|本副本的教学逻辑/新增阶段权威，手工维护|
|sources/build-fragments.mjs|第一方Artifact Tool作者：新增图片、原生数学图、提问给定和树片段|
|sources/package_deck.py|lxml原生PPTX克隆/片段嫁接作者；不写原件，不用python-pptx|
|sources/finalize.mjs、audit.py、render.mjs、inspect_zip.py、montage.py|验证/渲染，不拥有教学内容|
|snapshots/round1-before.pptx、round1-after.pptx|历史审查快照，70/105页，不是最终授课副本|
|final-slide-plan.json、final-render/、final-montage.png|版本绑定108页计划和本地渲染证据|
|../../remote-demos-v7/|历史演示；本次未更新/执行，不声称与108页页号全面对齐|

## 构建和覆盖边界

在新临时目录运行sources/rebuild.sh，先生成阶段0/1/2片段，再克隆原件、嫁接原生对象、独立验证、finalize；最后全页渲染和montage。QMD不是PPT生成器输入；教学修改要先更新QMD，再改相应JS/Python教学字面量并对齐。最终plan/Notes查阅文件是从最终PPT提取，不能覆盖QMD教学决定。

`rebuild.sh`创建全新临时目录，所有候选、导出、报告、PNG都写到那里；不会覆盖本目录的 accepted evidence、原件、搜图文件或交付deck。最后打印新临时输出位置，需重新逐页视觉审查后才能替换交付副本。ZIP时间戳可使重建字节散列不同，不能将新散列冒充本次验收身份。

构建依赖：Node、@oai/artifact-tool、@napi-rs/canvas、Python/lxml/Pillow、Presentations技能验证脚本，以及安装的两种Alibaba字型。本机命令（从repo根执行；路径只用于构建）：

```bash
AUDIO_NODE=/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node \
AUDIO_PYTHON=/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
RUNTIME_NODE_MODULES=/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules \
bash 1-2-encoding/1-2-3-audio-encoding-v2/validation/audio-v841-images-codex-20261014/sources/rebuild.sh
```

## 课堂操作

PPTX中的所有图片已经嵌入，不依赖网上加载；复制这一PPTX并安装项目字体即可查看静态页与Notes。现场演示另需完整复制remote-demos-v7及其相对assets，先按其README准备；本次没有确认它在目标教室的内核/UI/音响状态。Demo打不开20秒就用本页原生图/软件例图解释观察对象，不宣称完成实测。

主要问题先停顿再翻下一页；52页收学生总结再展示53～55；102页收所有退出票再展示103～105。106～108为课后扩展。许可署名存于PPT Notes与image-provenance.md，OpenMoji素材继续适用CC BY-SA 4.0；软件截图只说明历史界面结构。

所有文件作为本次task record纳入Git；没有提交node_modules、外部下载、私有工作目录或其他课件改动。本地检查通过；实际WPS/PowerPoint、课堂投影/音响和节奏仍unverified，见验收记录。
