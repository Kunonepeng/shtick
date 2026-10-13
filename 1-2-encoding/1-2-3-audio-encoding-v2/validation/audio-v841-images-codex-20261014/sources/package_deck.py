"""Graft Artifact Tool authored evidence onto a new copy of the native deck."""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
import json, hashlib, posixpath, os, sys

ROOT = Path(os.environ.get('AUDIO_BUILD_DIR', '/private/tmp/audio841-images-codex/build'))
LESSON = Path(os.environ.get('AUDIO_LESSON_DIR', Path(__file__).resolve().parents[3]))
SOURCE = LESSON / '1-2-3-audio-encoding-v8.4.1.pptx'
phase = int(sys.argv[1])
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main', 'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
FONT = 'Alibaba PuHuiTi 3.0 55 Regular'
BLACK = 'Alibaba PuHuiTi 3.0 115 Black'
def q(prefix, tag): return '{' + NS[prefix] + '}' + tag
def xml(data): return E.fromstring(data)
def dump(node): return E.tostring(node, xml_declaration=True, encoding='UTF-8', standalone=True)
def relpath(part): return posixpath.join(posixpath.dirname(part), '_rels', posixpath.basename(part) + '.rels')
def target(part, value): return value.lstrip('/') if value.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(part), value))
def alltext(node): return ''.join(node.xpath('.//a:t/text()', namespaces=NS))
def sid(node):
    item = node.find('.//p:cNvPr', NS)
    return item.get('id') if item is not None else ''
def set_note(body, text):
    for node in list(body):
        if node.tag == q('a', 'p'): body.remove(node)
    for line in text.splitlines():
        par = E.SubElement(body, q('a', 'p')); run = E.SubElement(par, q('a', 'r'))
        rp = E.SubElement(run, q('a', 'rPr'))
        for tag in ['latin', 'ea', 'cs']: E.SubElement(rp, q('a', tag), typeface=FONT)
        E.SubElement(run, q('a', 't')).text = line
def set_header(node, text, cover=False):
    body = node.find('p:txBody', NS)
    first = body.find('a:p', NS)
    for par in list(body.findall('a:p', NS)):
        if par is not first: body.remove(par)
    for child in list(first):
        if child.tag != q('a', 'pPr'): first.remove(child)
    pp = first.find('a:pPr', NS)
    if pp is None: pp = E.SubElement(first, q('a', 'pPr'))
    dr = pp.find('a:defRPr', NS)
    if dr is None: dr = E.SubElement(pp, q('a', 'defRPr'))
    dr.set('sz', '6000' if cover else '3600'); dr.set('b', '1')
    for tag in ['latin', 'ea', 'cs']:
        f = dr.find('a:' + tag, NS)
        if f is None: f = E.SubElement(dr, q('a', tag))
        f.set('typeface', BLACK)
    run = E.SubElement(first, q('a', 'r')); E.SubElement(run, q('a', 't')).text = text
    if not cover:
        x = node.find('p:spPr/a:xfrm', NS); x.find('a:off', NS).set('x', str(round(63.84 * 9525))); x.find('a:off', NS).set('y', str(round(63.84 * 9525)))
        x.find('a:ext', NS).set('cx', str(round(1152 * 9525))); x.find('a:ext', NS).set('cy', str(round(74 * 9525)))

with ZipFile(SOURCE) as z: files = {n: z.read(n) for n in z.namelist()}
with ZipFile(ROOT / f'fragments-{phase}.pptx') as z: fragments = {n: z.read(n) for n in z.namelist()}
roster = json.loads((ROOT / f'fragment-roster-{phase}.json').read_text())
fragment_parts = {key: f'ppt/slides/slide{i+1}.xml' for i, key in enumerate(roster)}
content_types = xml(files['[Content_Types].xml'])
presentation = xml(files['ppt/presentation.xml'])
pres_rels = xml(files['ppt/_rels/presentation.xml.rels'])
source_rels = {r.get('Id'): target('ppt/presentation.xml', r.get('Target')) for r in pres_rels}
source_order = [source_rels[r.get(q('r', 'id'))] for r in presentation.find('p:sldIdLst', NS)]
native_headers = {}
for i, part in enumerate(source_order):
    tree = xml(files[part]).find('p:cSld/p:spTree', NS)
    native_headers[i+1] = next(o for o in tree if o.find('.//a:t', NS) is not None)

short_titles = {10: '只能记录有限个数字，选哪些时刻？', 12: '演示B：放大波形，会看见采样点吗？', 24: '演示C：3 bit变4 bit，样本会变多吗？', 41: '编辑音轨和输出声道，有什么不同？', 49: '10分钟视频，为什么远小于6.44 GiB？', 70: '可选拓展：编码与压缩有何区别？'}
image_pages = {2, 5, 8, 9, 41, 65}
replace_pages = {8, 9, 41, 65} | ({3, 12, 13, 14, 17, 18, 22, 24, 28, 31, 43, 53, 58, 69} if phase >= 2 else set())
questions = {3, 4, 5, 6, 8, 13, 14, 16, 17, 19, 21, 22, 25, 27, 29, 31, 36, 43, 44, 46, 51, 52, 53, 57, 58, 59, 63, 64, 65}
if phase >= 2: questions |= {12,24,69}
notes_extra = {
    2: '[图片用途] 手机图只提供录音情境，不展示ADC答案。',
    5: '[图片用途] 用麦克风插画标明接收设备；转换关系由原生图解释。',
    8: '[教师逐字稿补充] 请在图中分别指出“电信号曲线”和“扬声器周围的声波”。先请学生说横轴是什么，再解释曲线记录时间变化；空间传播图中圆弧是波阵面示意，空气质点不会沿曲线行进。\n[图示边界] KyleThayer的同一动画0040帧。不是实测声场；数字曲线不是声压的空间轨迹。',
    9: '[Demo操作] 先收预测，再切换原Demo A观察播放光标。静态红线仅示意播放位置，截图未给时间刻度，不据此读秒。软件例图与Notebook是不同音频，不能直接比较幅度或样本。若20秒无法运行，指着横向时间轴解释光标位置；没有实测扬声器。',
    41: '[教师逐字稿补充] 先在左侧数编辑音轨：有两个独立的音轨控制区。上轨为单声道，下轨为立体声，所以共有三条波形。再看右侧模型，两份输入可以混入L、R两路输出；不是把诗朗诵固定送左、音乐固定送右。容量按导出参数计算，截图不证明本题工程真的导出过。\n[模型] 两输出均示意sin(4πt)+0.5sin(10πt)，仅说明混合；未模拟声像、增益和削波。',
    65: '[图片用途] 文件夹和摄像机只表示两种任务。先请学生按任务说明哪些条件不能牺牲，再揭示对应取舍。',
    12: '[数学证据] 同一0.72sin(10πt+0.3)，右图确为左图[0.30,0.50]的放大；纵轴不变。50 Hz教学采样模型，j=15..25，共11个点；封闭观察窗含两端，不等同0.2秒新产生11个样本。非Notebook实录。',
    13: '[计数条件] 统一使用[0,1)，含0不含1。1 Hz时刻0；2 Hz时刻0、0.5。下一秒的1不重复计入本秒。',
    14: '[控制变量] 同一sin(4πt+0.3)示意信号，在[0,1)分别按8 Hz和20 Hz记录。采样时刻j/Hz，左闭右开，共8和20个样本。只比较记录间隔和数量，不把示意图当作实录音质证据。',
    18: '[技术边界] 本课非负幅度模型：8个区间覆盖[0,8)，L3对应[3,4)，中点3.5是代表幅度，编号3不是幅度值。真实PCM通常为有符号幅度。',
    22: '[计算] 3 bit：Δ=1，3.71归入[3,4)，代表值3.5，误差0.21。4 bit：Δ=0.5，归入[3.5,4)，等级L7，代表值3.75，误差0.04。输入、范围、采样时刻相同。',
    24: '[控制变量证据] 同一10个输入[3.71,5.2,7.1,6.4,4.15,2.3,0.65,1.4,3.2,4.8]、相同采样时刻。空心点是原值；实心点是8/16档中点。两行每一列时间位置相同。此图是教学模型，现场Demo C仍使用原Notebook的归一化实录。',
    30: '[位宽边界] 此处3 bit是紧密按bit打包的教学模型，8个样本共24 bit，即3 Byte，不包含任何文件结构。真实PCM容量使用实际存储位宽，不用较低的有效量化精度替代存储位宽。',
    31: '[公式条件] 固定存储位宽、未压缩PCM样本payload；Hz按每声道每秒样本计。含全部声道，bit÷8换算Byte。不包含WAV头或其他块；完整文件不能统一假设只有44 Byte开销。',
    69: '[数学证据] cos(2πt)与cos(6πt)在t=0、0.5、1上均为[1,-1,1]。封闭观察窗包含两端，与原件BASE-13（本副本第20页）的[0,1)计数目的不同。这里只证明此组三点不足以唯一确定连续波形，不给出通用采样定理的推导。',
}
attribution = {
    2: 'smartphone.svg', 5: 'microphone-studio.svg', 65: 'folder.svg; video-camera.svg',
    8: 'speaker-soundwave-0180.png' if phase >= 1 else 'speaker-soundwave-0040.png', 9: 'audacity-spectrogram-waveform.png', 41: 'audacity-multitrack-mixing.png'
}
source_guide = (LESSON / '1-2-3-audio-encoding-v8.4.10-searched-images/source.md').read_text()
def source_note(n):
    if n not in attribution: return ''
    names = attribution[n].split('; '); rows = [line for line in source_guide.splitlines() if any(f'assets/{name}' in line for name in names) and line.count('|') == 4]
    if n in {2, 5, 65}: credit = 'OpenMoji contributors / HfG Schwäbisch Gmünd；CC BY-SA 4.0；https://github.com/hfg-gmuend/openmoji#license 。SVG仅等比转换为720px透明PNG，未改色或改形。图片许可继续为CC BY-SA 4.0。'
    elif n in {9, 41}: credit = 'Audacity Manual contributors；CC BY 3.0；https://raw.githubusercontent.com/audacity/audacity-manual/master/manual/index.html 。历史软件截图仅解释结构，非最新版操作说明；原PNG未修改。'
    else: credit = 'KyleThayer；CC0 1.0；https://commons.wikimedia.org/wiki/File:Sound_wave_animation.gif 。同一动画帧；原PNG未修改。'
    return '[图片来源]\n' + credit + '\n' + '\n'.join(rows) + '\n[核验日期] 2026-10-14'

media_map = {}
def graft(tree, rels, key):
    if key not in fragment_parts: return
    part = fragment_parts[key]; source = xml(fragments[part]).find('p:cSld/p:spTree', NS)
    fr = {r.get('Id'): r for r in xml(fragments[relpath(part)])}
    max_id = max([int(v.get('id')) for v in tree.findall('.//p:cNvPr', NS)] + [1])
    for j, child in enumerate(source[2:]):
        copied = deepcopy(child); meta = copied.find('.//p:cNvPr', NS)
        if meta is not None: meta.set('id', str(max_id + j + 1)); meta.set('name', f'codex-{key}-{meta.get("name")}')
        for blip in copied.findall('.//a:blip', NS):
            old = blip.get(q('r', 'embed')); source_media = target(part, fr[old].get('Target')); data = fragments[source_media]
            digest = hashlib.sha256(data).hexdigest()
            destination = media_map.setdefault(digest, f'ppt/media/codex-{digest[:18]}.png'); files[destination] = data
            rid = f'rIdCodex{len(rels)+1}'; E.SubElement(rels, '{'+REL+'}Relationship', Id=rid, Type=NS['r']+'/image', Target='../media/'+posixpath.basename(destination)); blip.set(q('r', 'embed'), rid)
        tree.append(copied)

for n, part in enumerate(source_order, 1):
    slide = xml(files[part]); tree = slide.find('p:cSld/p:spTree', NS); rels = xml(files[relpath(part)])
    if n in replace_pages:
        for item in list(tree)[2:]:
            if sid(item) not in {'2', '3', '4'}: tree.remove(item)
    elif n == 5:
        for item in list(tree)[2:]:
            if sid(item) in {'20', '21'}: tree.remove(item)
    if n in image_pages or (phase >= 2 and n in {3,12, 13,14, 17, 18, 22, 24, 28, 31, 43, 53, 58, 69}): graft(tree, rels, f'p{n}')
    if phase >= 2 and n == 19: graft(tree, rels, 'q19')
    if phase >= 2 and n == 21:
        for item in tree:
            if sid(item) == '5': item.find('.//a:t',NS).text='8个等级'
        graft(tree, rels, 'reveal21')
    if phase >= 1:
        if n == 17:
            for item in list(tree)[2:]:
                if sid(item) == '35': tree.remove(item)
        if n == 34:
            for item in list(tree)[2:]:
                if sid(item) in {'6', '8', '10'}: tree.remove(item)
        set_header(next(o for o in tree if o.find('.//a:t', NS) is not None), short_titles.get(n, alltext(native_headers[n])), n in {1, 35})
        # Repair both rails to the canonical eight-point edge-aligned geometry.
        for rid, y in [('2', 0), ('3', 709.3333333333)]:
            rail = next((o for o in tree if sid(o) == rid), None)
            if rail is None:
                rail = deepcopy(xml(files[source_order[0]]).find('p:cSld/p:spTree', NS)[2]); rail.find('.//p:cNvPr', NS).set('id', rid); tree.insert(3, rail)
            x = rail.find('p:spPr/a:xfrm', NS); x.find('a:off', NS).set('x', '0'); x.find('a:off', NS).set('y', str(round(y * 9525))); x.find('a:ext', NS).set('cx', '12191695'); x.find('a:ext', NS).set('cy', '101600')
        for item in tree.findall('p:sp', NS):
            body = item.find('p:txBody', NS)
            if body is None: continue
            bp = body.find('a:bodyPr', NS)
            for auto in list(bp):
                if auto.tag in {q('a', 'spAutoFit'), q('a', 'normAutofit')}: bp.remove(auto)
            if bp.find('a:noAutofit', NS) is None: E.SubElement(bp, q('a', 'noAutofit'))
            for rp in body.xpath('.//a:rPr | .//a:defRPr | .//a:endParaRPr', namespaces=NS):
                for tag in ['latin', 'ea', 'cs']:
                    f = rp.find('a:'+tag, NS)
                    if f is None: f = E.SubElement(rp, q('a', tag), typeface=FONT)
                    elif not f.get('typeface', '').startswith('Alibaba PuHuiTi'): f.set('typeface', FONT)
        # Readable cyan text; cyan outlines retain their technical role.
        for c in tree.xpath('.//p:txBody//a:srgbClr', namespaces=NS):
            if c.get('val', '').upper() == '00B0F0': c.set('val', '007C9B')
    if phase >= 2:
        for effect in list(tree.findall('.//a:effectLst', NS)) + list(tree.findall('.//a:effectDag', NS)): effect.getparent().remove(effect)
        for effect in tree.findall('.//a:effectRef',NS): effect.set('idx','0')
        for text in tree.findall('.//a:t', NS):
            if n == 29 and text.text == '量化位数': text.text = '存储位宽'
            if n == 17 and text.text.startswith('红点落在哪一段？'): text.text = '3.71落在 [3,4)，所以等级编号是3。'
            if n in {36,37,38} and text.text: text.text = text.text.replace('MB','MiB')
            if n == 36 and text.text and text.text.startswith('提醒：'): text.text = '单位换算：1 MiB = 1024² Byte；1 MB = 1,000,000 Byte。'
        if n == 23:
            item=next(o for o in tree if sid(o)=='8'); item.find('p:spPr/a:xfrm/a:ext',NS).set('cx',str(round(64*9525)))
        for item in tree.findall('p:sp',NS):
            box=item.find('p:spPr/a:xfrm',NS)
            if box is None or item.find('p:txBody',NS) is None or not alltext(item).strip(): continue
            off=box.find('a:off',NS); ext=box.find('a:ext',NS)
            y=int(off.get('y'))/9525; h=int(ext.get('cy'))/9525
            if y>=590 and y+h>656.64: off.set('y',str(round((656.64-h)*9525)))
    files[part] = dump(slide); files[relpath(part)] = dump(rels)
    note_rel = next(r for r in rels if r.get('Type').endswith('/notesSlide')); note_part = target(part, note_rel.get('Target')); note = xml(files[note_part])
    body = next(o.find('p:txBody', NS) for o in note.findall('p:cSld/p:spTree/p:sp', NS) if o.find('p:nvSpPr/p:nvPr/p:ph', NS).get('type') == 'body')
    original = '\n'.join(''.join(par.xpath('.//a:t/text()', namespaces=NS)) for par in body.findall('a:p', NS))
    current_title = short_titles.get(n, alltext(native_headers[n])) if phase >= 1 else alltext(native_headers[n])
    extra = notes_extra.get(n, '').replace('0040帧', '0180帧；原生裁剪仅保留x=440..800、y=125..335的扬声器与声波区域' if phase >= 1 else '0040帧')
    note_text = original + '\n\n' + extra + '\n' + source_note(n)
    if phase >= 1:
        stage = '独立作答' if n in {2, 10, 32, 37, 39, 47, 54, 60, 61, 66, 68} else '证据／解释'
        if n == 34:
            stage = '学生总结'; note_text = '先给学生30秒独立整理，再请三人逐问解释并引用刚才的图或计算。此页只呈现问题，不公布总结。听完后再逐页揭示知识树。\n[教师参考，仅总结后使用]\n' + note_text
        if n == 68:
            stage = '独立退出评估'; note_text = '先收每位学生的三个书面解释，给约2分钟。不能只收志愿者回答。收齐后请学生引用证据概括两课时关系，再更新知识树。\n[教师参考，仅收取后使用]\n' + note_text
        note_text = f'[问题] {current_title}\n[内部编号] BASE-{n:02}\n[阶段] {stage}\n[教师逐字稿]\n' + note_text
    set_note(body, note_text.strip()); files[note_part] = dump(note)

plan = []
ordered = []
next_slide = 71
next_note = 71
def clone(n, key, role, fragment_key=None):
    global next_slide, next_note
    part = source_order[n-1]; slide = xml(files[part]); rels = xml(files[relpath(part)]); tree = slide.find('p:cSld/p:spTree', NS)
    for item in list(tree)[2:]:
        if sid(item) not in {'2', '3', '4'}: tree.remove(item)
    if phase >= 2 and role == 'question' and n in {19,21,29,36,59}:
        selected={21:{'5'},29:{'5','7','9','11'},36:{'5','7','9','11'},59:{'5','7','9','11'}}
        for item in xml(files[part]).find('p:cSld/p:spTree',NS):
            keep=sid(item) in selected.get(n,set())
            if n == 19 and sid(item) not in {'2','3','4'} and item.find('p:txBody',NS) is not None:
                off=item.find('p:spPr/a:xfrm/a:off',NS)
                keep=off is not None and int(off.get('y')) < 380*9525
            if keep: tree.append(deepcopy(item))
    if role == 'question' and n == 63:
        oldtree = xml(files[part]).find('p:cSld/p:spTree', NS)
        for item in oldtree:
            if item.tag == q('p', 'pic'): tree.append(deepcopy(item))
    if fragment_key: graft(tree, rels, fragment_key)
    if role == 'tree': set_header(next(o for o in tree if o.find('.//a:t', NS) is not None), '把证据连接起来：数据怎样表示？')
    newpart = f'ppt/slides/slide{next_slide}.xml'; newnote = f'ppt/notesSlides/notesSlide{next_note}.xml'; next_slide += 1; next_note += 1
    nr = next(r for r in rels if r.get('Type').endswith('/notesSlide')); oldnote = target(part, nr.get('Target')); nr.set('Target', '../notesSlides/'+posixpath.basename(newnote))
    note = xml(files[oldnote]); note_rels = xml(files[relpath(oldnote)])
    for r in note_rels:
        if r.get('Type').endswith('/slide'): r.set('Target', '../slides/'+posixpath.basename(newpart))
    body = next(o.find('p:txBody', NS) for o in note.findall('p:cSld/p:spTree/p:sp', NS) if o.find('p:nvSpPr/p:nvPr/p:ph', NS).get('type') == 'body')
    title = alltext(next(o for o in tree if o.find('.//a:t', NS) is not None))
    if role == 'question':
        script = '先请每位学生独立预测或写出方法，停顿约15～20秒。请两人比较理由，暂不确认哪一个答案正确。学生作答后再翻页，用下一页的图或数据核对。先观察当前给出的条件，不提前讲后页的结论。'
        if n == 65: script = '先看两种任务。请分别说出“绝不能丢什么”和“可以权衡什么”，停顿20秒。听理由后再揭示两种取舍；不要在此页宣布一种通用最佳方式。'
        text = f'[问题] {title}\n[内部编号] {key}\n[阶段] 提问\n[教师逐字稿]\n{script}\n' + (source_note(n) if n == 65 else '')
    else:
        stage = int(key[-1]); script = '先请学生用刚才的证据总结新增关系，其他同学补充理由。收到概括后再揭示红框，并说明它和先前节点怎样连接；旧节点保持可见。本次只增加一个分支。'
        text = f'[问题] {title}\n[内部编号] {key}\n[阶段] 知识树更新\n[教师逐字稿]\n{script}\n[当前已建立] 前{stage}个分支；不提前口述尚未建立的节点。'
    set_note(body, text)
    files[newpart] = dump(slide); files[relpath(newpart)] = dump(rels); files[newnote] = dump(note); files[relpath(newnote)] = dump(note_rels)
    for name, kind in [(newpart, 'slide'), (newnote, 'notesSlide')]: E.SubElement(content_types, '{'+CT+'}Override', PartName='/'+name, ContentType='application/vnd.openxmlformats-officedocument.presentationml.'+kind+'+xml')
    return newpart

for n, part in enumerate(source_order, 1):
    if phase >= 1 and n in questions:
        key = f'q{n}'; newpart = clone(n, key, 'question', key if key in fragment_parts else None)
        ordered.append(newpart); plan.append({'key': key, 'basePage': n, 'role': 'question', 'xml': newpart})
    ordered.append(part); plan.append({'key': f'p{n}', 'basePage': n, 'role': 'source/evidence', 'xml': part})
    if phase >= 1 and n in {34, 68}:
        for stage in ([1, 2, 3] if n == 34 else [4, 5, 6]):
            key = f'tree{stage}'; newpart = clone(n, key, 'tree', key); ordered.append(newpart); plan.append({'key': key, 'basePage': n, 'role': 'tree', 'xml': newpart})

slide_list = presentation.find('p:sldIdLst', NS)
for node in list(slide_list): slide_list.remove(node)
for r in list(pres_rels):
    if r.get('Type').endswith('/slide'): pres_rels.remove(r)
for i, part in enumerate(ordered):
    rid = 'rIdCodexSlide'+str(i+1); E.SubElement(pres_rels, '{'+REL+'}Relationship', Id=rid, Type=NS['r']+'/slide', Target='slides/'+posixpath.basename(part))
    E.SubElement(slide_list, q('p', 'sldId'), id=str(256+i), attrib={q('r', 'id'): rid})
    plan[i]['page'] = i+1
presentation.find('p:sldSz', NS).set('type', 'screen16x9')
files['ppt/presentation.xml'] = dump(presentation); files['ppt/_rels/presentation.xml.rels'] = dump(pres_rels)
if not any(d.get('Extension') == 'png' for d in content_types): E.SubElement(content_types, '{'+CT+'}Default', Extension='png', ContentType='image/png')
files['[Content_Types].xml'] = dump(content_types)
app = xml(files['docProps/app.xml'])
for child in app:
    if child.tag.endswith('}Slides'): child.text = str(len(ordered))
files['docProps/app.xml'] = dump(app)
if phase >= 2:
    for name,data in list(files.items()):
        if name.endswith('.xml') and ('/theme/' in name or '/slideMasters/' in name or '/notesMasters/' in name):
            node=xml(data)
            for font in node.xpath('.//a:latin | .//a:ea | .//a:cs',namespaces=NS):
                if not font.get('typeface','').startswith('Alibaba PuHuiTi'): font.set('typeface',FONT)
            for effects in node.findall('.//a:effectStyleLst',NS):
                for effect in effects.findall('.//a:effectLst',NS):
                    for child in list(effect): effect.remove(child)
            files[name]=dump(node)
output = ROOT / f'candidate-{phase}.pptx'
with ZipFile(output, 'w', ZIP_DEFLATED) as z:
    for name, data in files.items(): z.writestr(name, data)
(ROOT / f'plan-{phase}.json').write_text(json.dumps({'phase': phase, 'sourceSha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(), 'slideCount': len(plan), 'slides': plan}, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'phase': phase, 'slideCount': len(plan), 'output': str(output), 'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}))
