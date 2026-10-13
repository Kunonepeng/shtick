# v8.5 / v8.6 视觉修订入口

本目录是这次视觉修订的版本记录。推荐查看[最终课件 v8.6](../../1-2-3-audio-encoding-v8.6.codex.pptx)与[复查记录](review-and-acceptance.md)。[v8.5](../../1-2-3-audio-encoding-v8.5.codex.pptx)保留融合检查点，包含首轮发现的问题，不是建议课堂使用副本。没有自动替代其他历史正式包。

| 文件／目录 | 角色／所有者 |
|---|---|
| course-design.qmd | 本次教学设计权威；新增视觉推理、边界、时间、树阶段及完整88页Notes。旧设计保持原样。 |
| sources/build.mjs | 可编辑JS生成源，@oai/artifact-tool；阶段0融合、阶段1首轮修复、阶段2第二轮修复。PPTX由JS直接生成，不是从QMD转换。 |
| assets/、assets-provenance.json | 提供课件提取的4份复用PNG与用途／hash／裁剪边界。历史AI情境从v8.1导入，提示词原文留在原图片记录和Notes。 |
| v85-plan.json、round1-plan.json、v86-plan.json | 版本绑定页码、角色、base81对应映射。内部键只用于教师／构建，不是学生Q ID。 |
| round1-review.json、round2-review.json | 两轮排名、修复动作、最终页与逐项复检证据。 |
| *-render/、*-montage.png | 完整逐页PNG与layout，版本绑定视觉证据。 |
| sources/audit.py | 独立XML／Decimal／Pillow数值和结构检查器；不导入绘图函数。 |
| sources/inspect_zip.py、render.mjs、montage.py | 只读PPTX提取／渲染／montage脚本。 |
| sources/patch_font_defaults.py | 输出后补齐theme、master和Notes默认字体，使导出仍显式使用Alibaba。每次生成自动调用，重生成可保留。 |
| sources/finalize.mjs | 原生包／布局／字体／重导入最终检查；输出和receipt不可覆盖，重试须指定新目录／receipt。 |
| snapshots/round1-candidate.pptx | 首轮闭环后的85页候选，用于审查链；不是课堂副本。 |
| delivery-checksums.json | 两个原始文件与两个新文件的SHA256。 |

## 重生成与安全写入

从本目录运行，选择一个新的临时构建目录。sources/build.mjs只写该目录中的candidate、plan、textfit；按0→1→2生成。它从不可变的v8.1输入，读取本目录assets，自动调用字体补齐脚本。不会改v8.1/v8.4.10、正式包、Notebook、Reveal或已交付PPTX。不要运行历史v84/v831构建器，它们有其他写入／发布行为。

构建依赖：Node 24.x、@oai/artifact-tool 2.8.93、@napi-rs/canvas 0.1.100、Python 3与Pillow。使用Codex load_workspace_dependencies定位环境，不在课堂临时安装。重建主机需AlibabaPuHuiTi-3-55-Regular.ttf和115-Black.ttf；本次在macOS Library/Fonts加载。构建依赖与课堂依赖不同。

```sh
export AUDIO_BUILD_DIR=/private/tmp/audio-v86-rebuild-example
export AUDIO_PYTHON=/path/to/bundled/python3
/path/to/bundled/node sources/build.mjs 0
/path/to/bundled/node sources/build.mjs 1
/path/to/bundled/node sources/build.mjs 2
/path/to/bundled/node sources/render.mjs "$AUDIO_BUILD_DIR/v86-candidate.pptx" "$AUDIO_BUILD_DIR/v86-render"
"$AUDIO_PYTHON" sources/audit.py v86
```

`@oai/artifact-tool`与canvas需要能从sources/解析到其node_modules（本次临时工作目录使用bundled模块的符号链接；不要把本机node_modules提交进课件包）。构建阶段可覆盖临时candidate及plan，因此必须使用独立临时目录；已验收输出与receipt不可覆盖。最后使用sources/finalize.mjs，并设置AUDIO_FINAL_DIR、AUDIO_RECEIPT_PATH与RUNTIME_NODE_MODULES到新路径；确认candidate到交付副本hash一致。

## 课堂操作与范围

复制最终PPTX即可使用其原生静态证据，所有嵌入图片可离线呈现。现场演示仍按[remote-demos-v7入口](../../remote-demos-v7/README.md)准备和复制该包；本次没有改演示依赖或验证现场操作。先停留提问页，收个人预测，再逐页揭示；每次知识树更新先收总结。新增数学示意、PCM网格与JPEG读数的条件写在Notes里，与现场真实波形值有别。

外部演示未改、未重新执行；没有声称PPTX→Reveal或QMD→IPYNB存在通用路径。WPS、PowerPoint、投影、音频、学生完成和真实节奏均unverified，详见复查记录的Deck acceptance record。
