import math
import py5

# ============================================================
# 编码实验室：M <= 2^n
# 5 个课堂演示：二进制开关 / 编码停车场 / 8→9 临界点 / 像素量化 / 声音量化
# v4：所有实验从 1 bit 起步，并优化图像量化区的视觉对比
# ============================================================

DESIGN_W, DESIGN_H = 1200, 675
MIN_WINDOW_W, MIN_WINDOW_H = 800, 450

# 与 Violet-Rail PPT 一致的语义色
FRAME_VIOLET = '#6251B1'
ACCENT_VIOLET = '#8C64E1'
TECH_CYAN = '#00B0F0'
FOCUS_RED = '#FF0000'
TITLE_BLACK = '#262626'
BODY_BLACK = '#000000'
MUTED_GRAY = '#808080'
LIGHT_GRAY = '#E9E9EE'
VERY_LIGHT = '#F7F7FA'
WHITE = '#FFFFFF'

mode = 1
ui_font = None
initial_fit_done = False

# Demo 1
switch_bits = 1
switch_values = [0, 0, 0, 0]

# Demo 2
parking_bits = 1
parking_objects = ['甲', '乙', '丙', '丁', '戊']
parking_assignments = []
selected_object = None

# Demo 3
critical_m = 2
slider_dragging = False

# Demo 4
pixel_bits = 1

# Demo 5
sound_bits = 1
sound_samples = 16


def settings():
    # 先创建标准 16:9 画布；setup() 后会自动扩大到当前屏幕可用范围。
    # 不使用 full_screen()，这样可保留系统标题栏、最小化按钮和鼠标拖拽缩放。
    py5.size(DESIGN_W, DESIGN_H)


def setup():
    global ui_font
    py5.frame_rate(30)
    py5.rect_mode(py5.CORNER)
    py5.text_align(py5.LEFT, py5.BASELINE)

    # 使用普通可缩放窗口，而不是独占全屏：
    # 1) 默认会自动适应当前屏幕；2) 保留标题栏最小化按钮；3) 可拖动窗口边缘缩放。
    py5.window_title('信息编码 · py5 编码实验室')
    py5.window_resizable(True)

    # 优先使用课件字体；若机房未安装则自动回退到常见中文字体。
    available = set(py5.Py5Font.list())
    candidates = [
        'Alibaba PuHuiTi 3.0 55 Regular',
        'Alibaba PuHuiTi 3.0',
        'Microsoft YaHei UI',
        'Microsoft YaHei',
        'SimHei',
        'Arial Unicode MS',
        'SansSerif',
    ]
    for name in candidates:
        if name == 'SansSerif' or name in available:
            try:
                ui_font = py5.create_font(name, 32)
                break
            except Exception:
                pass
    if ui_font is not None:
        py5.text_font(ui_font)

    reset_current_demo()


def _view_transform():
    """把固定的 1200×675 教学设计等比缩放到任意窗口大小。"""
    scale = min(py5.width / DESIGN_W, py5.height / DESIGN_H)
    scale = max(scale, 0.01)
    offset_x = (py5.width - DESIGN_W * scale) / 2
    offset_y = (py5.height - DESIGN_H * scale) / 2
    return scale, offset_x, offset_y


def mouse_design():
    """把真实窗口中的鼠标坐标换算回 1200×675 的设计坐标。"""
    scale, offset_x, offset_y = _view_transform()
    return ((py5.mouse_x - offset_x) / scale,
            (py5.mouse_y - offset_y) / scale)


def fit_window_to_screen():
    """尽量铺满当前屏幕，同时保留标题栏、任务栏和窗口缩放能力。"""
    # 给 Windows 标题栏 / 任务栏留出空间，避免窗口控制按钮跑到屏幕外。
    target_w = max(MIN_WINDOW_W, int(py5.display_width - 16))
    target_h = max(MIN_WINDOW_H, int(py5.display_height - 96))
    py5.window_resize(target_w, target_h)
    py5.window_move(0, 0)


def restore_design_window():
    """恢复到标准 1200×675 窗口，并尽量置于屏幕中央。"""
    target_w = min(DESIGN_W, max(MIN_WINDOW_W, py5.display_width - 80))
    target_h = int(target_w * DESIGN_H / DESIGN_W)
    max_h = max(MIN_WINDOW_H, py5.display_height - 120)
    if target_h > max_h:
        target_h = max_h
        target_w = int(target_h * DESIGN_W / DESIGN_H)
    py5.window_resize(int(target_w), int(target_h))
    x = max(0, int((py5.display_width - target_w) / 2))
    y = max(0, int((py5.display_height - target_h) / 2 - 20))
    py5.window_move(x, y)


def minimize_window():
    """Windows/JAVA2D 下尝试通过快捷键最小化；失败时仍可用标题栏最小化按钮。"""
    try:
        # Py5Surface 当前封装的底层 Processing PSurface；JAVA2D 原生对象为 SmoothCanvas。
        surface = py5.get_surface()
        native = surface._instance.getNative()
        frame = native.getFrame()
        Frame = py5.JClass('java.awt.Frame')
        frame.setState(Frame.ICONIFIED)
    except Exception as exc:
        print('快捷键最小化不可用，请使用窗口标题栏的最小化按钮。', exc)


def draw():
    global initial_fit_done

    # 第一次真正开始绘制后再扩大窗口，兼容不同系统 / JupyterLab 启动方式。
    if not initial_fit_done and py5.frame_count >= 2:
        fit_window_to_screen()
        initial_fit_done = True

    # 窗口比例变化时，空白区域使用浅灰；教学画布始终保持 16:9 并居中。
    py5.background(VERY_LIGHT)
    scale, offset_x, offset_y = _view_transform()

    py5.push_matrix()
    py5.translate(offset_x, offset_y)
    py5.scale(scale)

    py5.no_stroke()
    py5.fill(WHITE)
    py5.rect(0, 0, DESIGN_W, DESIGN_H)

    draw_frame()
    draw_header()

    if mode == 1:
        draw_switch_demo()
    elif mode == 2:
        draw_parking_demo()
    elif mode == 3:
        draw_critical_demo()
    elif mode == 4:
        draw_pixel_demo()
    elif mode == 5:
        draw_sound_demo()

    draw_nav()
    py5.pop_matrix()


def draw_frame():
    py5.no_stroke()
    py5.fill(FRAME_VIOLET)
    py5.rect(0, 0, DESIGN_W, 8)
    py5.rect(0, DESIGN_H - 8, DESIGN_W, 8)


def draw_header():
    titles = {
        1: ('增加 1 bit，究竟增加了多少种可能？', '点击每一位切换 0 / 1，观察编码空间。'),
        2: ('编码空间可以有空位，但能不能“撞码”？', '先用 2 bit 尝试，再增加到 3 bit。'),
        3: ('只增加第 9 种状态，为什么突然要多 1 bit？', '拖动 M，观察“最少位数”在哪里发生跳变。'),
        4: ('图像为什么也服从 M ≤ 2^n？', '改变每像素位数，观察可区分的灰度等级。'),
        5: ('连续的声音，怎样变成有限个可以编码的状态？', '分别改变采样点数量与量化位数，观察它们各自影响什么。'),
    }
    title, subtitle = titles[mode]
    py5.fill(TITLE_BLACK)
    py5.text_size(36)
    py5.text(title, 58, 62)
    py5.fill(MUTED_GRAY)
    py5.text_size(18)
    py5.text(subtitle, 60, 92)


def draw_nav():
    labels = ['1 二进制开关', '2 编码停车场', '3 8→9 临界点', '4 像素量化', '5 声音量化']
    x0, y, w, h, gap = 46, 615, 172, 34, 10
    for i, label in enumerate(labels, start=1):
        draw_button(x0 + (i - 1) * (w + gap), y, w, h, label, active=(mode == i), text_size=14)

    py5.fill(MUTED_GRAY)
    py5.text_size(11)
    py5.text('1–5 切换 · R 重置 · F 适应屏幕 · W 标准窗口 · M 最小化', 962, 638)


def draw_button(x, y, w, h, label, active=False, text_size=16, danger=False):
    py5.stroke_weight(2)
    if active:
        py5.stroke(ACCENT_VIOLET)
        py5.fill(ACCENT_VIOLET)
        txt = WHITE
    else:
        py5.stroke(FOCUS_RED if danger else FRAME_VIOLET)
        py5.fill(WHITE)
        txt = FOCUS_RED if danger else TITLE_BLACK
    py5.rect(x, y, w, h)
    py5.fill(txt)
    py5.no_stroke()
    py5.text_size(text_size)
    py5.text_align(py5.CENTER, py5.CENTER)
    py5.text(label, x + w / 2, y + h / 2 + 1)
    py5.text_align(py5.LEFT, py5.BASELINE)


def hit(x, y, w, h):
    mx, my = mouse_design()
    return x <= mx <= x + w and y <= my <= y + h


def formula_box(main_text, sub_text=None, x=720, y=490, w=410, h=86, danger=False):
    py5.stroke_weight(3)
    py5.stroke(FOCUS_RED if danger else ACCENT_VIOLET)
    py5.fill(WHITE)
    py5.rect(x, y, w, h)
    py5.no_stroke()
    py5.fill(FOCUS_RED if danger else ACCENT_VIOLET)
    py5.text_align(py5.CENTER, py5.CENTER)
    py5.text_size(30)
    py5.text(main_text, x + w / 2, y + 32)
    if sub_text:
        py5.fill(MUTED_GRAY)
        py5.text_size(16)
        py5.text(sub_text, x + w / 2, y + 65)
    py5.text_align(py5.LEFT, py5.BASELINE)


# ============================================================
# Demo 1 — 二进制开关
# ============================================================

def draw_switch_demo():
    py5.fill(BODY_BLACK)
    py5.text_size(20)
    py5.text('位数 n', 66, 160)
    draw_button(150, 132, 46, 34, '−', text_size=22)
    draw_button(206, 132, 46, 34, '+', text_size=22)

    # bit switches
    start_x = 88
    gap = 122
    y = 215
    for i in range(switch_bits):
        x = start_x + i * gap
        py5.stroke_weight(3)
        py5.stroke(ACCENT_VIOLET)
        py5.fill(WHITE)
        py5.rect(x, y, 92, 92)
        py5.no_stroke()
        py5.fill(TITLE_BLACK)
        py5.text_align(py5.CENTER, py5.CENTER)
        py5.text_size(52)
        py5.text(str(switch_values[i]), x + 46, y + 46)
        py5.fill(MUTED_GRAY)
        py5.text_size(13)
        py5.text(f'第 {i + 1} 位', x + 46, y + 114)

    py5.text_align(py5.LEFT, py5.BASELINE)
    current = ''.join(str(switch_values[i]) for i in range(switch_bits))
    py5.fill(MUTED_GRAY)
    py5.text_size(17)
    py5.text('当前编码', 88, 388)
    py5.fill(ACCENT_VIOLET)
    py5.text_size(42)
    py5.text(current, 88, 435)

    # all possible codes
    cap = 2 ** switch_bits
    py5.fill(BODY_BLACK)
    py5.text_size(20)
    py5.text(f'{switch_bits} 位一共能形成多少种不同编码？', 585, 160)

    cols = 4
    cell_w, cell_h = 116, 55
    gx, gy = 590, 196
    for idx in range(cap):
        row, col = divmod(idx, cols)
        x = gx + col * (cell_w + 12)
        yy = gy + row * (cell_h + 12)
        code = format(idx, f'0{switch_bits}b')
        active = (code == current)
        py5.stroke_weight(3 if active else 2)
        py5.stroke(FOCUS_RED if active else ACCENT_VIOLET)
        py5.fill(WHITE)
        py5.rect(x, yy, cell_w, cell_h)
        py5.no_stroke()
        py5.fill(FOCUS_RED if active else TITLE_BLACK)
        py5.text_align(py5.CENTER, py5.CENTER)
        py5.text_size(22)
        py5.text(code, x + cell_w / 2, yy + cell_h / 2)

    py5.text_align(py5.LEFT, py5.BASELINE)
    py5.fill(ACCENT_VIOLET)
    py5.text_size(24)
    py5.text('每增加 1 bit，原来的每一种情况都会再分成 2 种。', 88, 530)
    formula_box(f'n = {switch_bits}   →   2^{switch_bits} = {cap}', 'n 位二进制最多形成 2^n 种不同编码', 692, 492, 438, 88)


# ============================================================
# Demo 2 — 编码停车场 + 撞码
# ============================================================

def reset_parking():
    global parking_assignments, selected_object
    parking_assignments = [[] for _ in range(2 ** parking_bits)]
    selected_object = None


def object_slot_of(obj_index):
    for s, items in enumerate(parking_assignments):
        if obj_index in items:
            return s
    return None


def draw_parking_demo():
    cap = 2 ** parking_bits
    py5.fill(BODY_BLACK)
    py5.text_size(20)
    py5.text(f'现在有 M = {len(parking_objects)} 种状态', 66, 155)
    py5.text(f'编码位数 n = {parking_bits}，容量 = {cap}', 66, 185)

    draw_button(66, 205, 96, 34, '− 1 bit', text_size=15)
    draw_button(172, 205, 96, 34, '+ 1 bit', text_size=15)
    draw_button(282, 205, 110, 34, '自动尝试', text_size=15)
    draw_button(402, 205, 82, 34, '清空', text_size=15)

    # objects
    py5.fill(MUTED_GRAY)
    py5.text_size(15)
    py5.text('点击对象，再点击右侧编码槽', 66, 278)
    for i, obj in enumerate(parking_objects):
        x = 70 + i * 78
        y = 305
        selected = (selected_object == i)
        py5.stroke_weight(3 if selected else 2)
        py5.stroke(FOCUS_RED if selected else ACCENT_VIOLET)
        py5.fill(WHITE)
        py5.rect(x, y, 58, 58)
        py5.no_stroke()
        py5.fill(FOCUS_RED if selected else TITLE_BLACK)
        py5.text_align(py5.CENTER, py5.CENTER)
        py5.text_size(28)
        py5.text(obj, x + 29, y + 29)
        slot = object_slot_of(i)
        if slot is not None:
            py5.fill(MUTED_GRAY)
            py5.text_size(12)
            py5.text(format(slot, f'0{parking_bits}b'), x + 29, y + 76)

    # code slots
    py5.text_align(py5.LEFT, py5.BASELINE)
    py5.fill(BODY_BLACK)
    py5.text_size(20)
    py5.text('编码空间', 560, 155)

    cols = 4
    cell_w, cell_h = 132, 93
    gx, gy = 560, 190
    collision = False
    assigned_count = 0
    for idx in range(cap):
        row, col = divmod(idx, cols)
        x = gx + col * (cell_w + 14)
        y = gy + row * (cell_h + 18)
        items = parking_assignments[idx]
        assigned_count += len(items)
        is_collision = len(items) > 1
        collision = collision or is_collision
        py5.stroke_weight(3 if is_collision else 2)
        py5.stroke(FOCUS_RED if is_collision else ACCENT_VIOLET)
        py5.fill(WHITE)
        py5.rect(x, y, cell_w, cell_h)
        py5.no_stroke()
        py5.fill(TITLE_BLACK)
        py5.text_align(py5.CENTER, py5.CENTER)
        py5.text_size(20)
        py5.text(format(idx, f'0{parking_bits}b'), x + cell_w / 2, y + 25)
        label = ' / '.join(parking_objects[j] for j in items) if items else '空位'
        py5.fill(FOCUS_RED if is_collision else (MUTED_GRAY if not items else ACCENT_VIOLET))
        py5.text_size(19 if items else 14)
        py5.text(label, x + cell_w / 2, y + 61)
        if is_collision:
            py5.text_size(12)
            py5.text('撞码', x + cell_w / 2, y + 82)

    py5.text_align(py5.LEFT, py5.BASELINE)
    all_assigned = assigned_count == len(parking_objects)
    if collision:
        py5.fill(FOCUS_RED)
        py5.text_size(23)
        py5.text('冲突：同一个编码对应了两个不同状态，计算机无法区分。', 66, 500)
        formula_box(f'{len(parking_objects)} > 2^{parking_bits} = {cap}', '容量不足时，想“硬塞进去”就会撞码', 692, 490, 438, 88, danger=True)
    elif all_assigned and cap >= len(parking_objects):
        py5.fill(ACCENT_VIOLET)
        py5.text_size(23)
        py5.text(f'成功：{len(parking_objects)} 种状态都拥有唯一编码；空位可以保留。', 66, 500)
        formula_box(f'{len(parking_objects)} ≤ 2^{parking_bits} = {cap}', '编码空间可以有空位，但不同状态不能撞码', 692, 490, 438, 88)
    else:
        py5.fill(MUTED_GRAY)
        py5.text_size(19)
        py5.text('还没有完成编码。可以点击“自动尝试”快速观察结果。', 66, 500)
        formula_box(f'M = {len(parking_objects)}    ?    2^{parking_bits} = {cap}', '先判断容量，再判断是否能建立唯一编码', 692, 490, 438, 88)


# ============================================================
# Demo 3 — 8→9 临界点
# ============================================================

def min_bits(m):
    return max(1, math.ceil(math.log2(m)))


def draw_critical_demo():
    n = min_bits(critical_m)
    cap = 2 ** n
    prev_cap = 2 ** (n - 1) if n > 1 else 1

    py5.fill(BODY_BLACK)
    py5.text_size(20)
    py5.text('拖动滑块改变需要区分的状态数 M', 66, 155)

    # slider
    sx1, sx2, sy = 110, 790, 220
    py5.stroke_weight(4)
    py5.stroke(LIGHT_GRAY)
    py5.line(sx1, sy, sx2, sy)
    t = (critical_m - 2) / 18
    hx = sx1 + t * (sx2 - sx1)
    py5.stroke(ACCENT_VIOLET)
    py5.line(sx1, sy, hx, sy)
    py5.no_stroke()
    py5.fill(ACCENT_VIOLET)
    py5.circle(hx, sy, 22)

    py5.fill(MUTED_GRAY)
    py5.text_size(14)
    py5.text('2', sx1 - 5, sy + 33)
    py5.text('20', sx2 - 8, sy + 33)
    py5.fill(TITLE_BLACK)
    py5.text_size(30)
    py5.text(f'M = {critical_m}', 850, 230)
    draw_button(1000, 198, 48, 34, '−', text_size=22)
    draw_button(1058, 198, 48, 34, '+', text_size=22)

    # capacity staircase
    py5.fill(BODY_BLACK)
    py5.text_size(18)
    py5.text('不同位数能够提供的最大编码容量', 66, 302)

    bx, by = 230, 330
    unit = 18
    for bits in range(1, 6):
        c = 2 ** bits
        yy = by + (bits - 1) * 48
        is_current = bits == n
        py5.fill(TITLE_BLACK if not is_current else ACCENT_VIOLET)
        py5.text_size(16)
        py5.text_align(py5.RIGHT, py5.CENTER)
        py5.text(f'{bits} bit', bx - 18, yy + 12)
        py5.stroke_weight(3 if is_current else 1.5)
        py5.stroke(ACCENT_VIOLET if is_current else LIGHT_GRAY)
        py5.fill(WHITE)
        py5.rect(bx, yy, c * unit, 24)
        py5.no_stroke()
        py5.fill(ACCENT_VIOLET if is_current else MUTED_GRAY)
        py5.text_align(py5.LEFT, py5.CENTER)
        py5.text_size(14)
        py5.text(f'2^{bits} = {c}', bx + c * unit + 12, yy + 12)

        # M marker on the same scale
        mx = bx + critical_m * unit
        py5.stroke(FOCUS_RED)
        py5.stroke_weight(2)
        py5.line(mx, yy - 3, mx, yy + 27)

    py5.text_align(py5.LEFT, py5.BASELINE)

    # explicit 8 -> 9 reasoning
    if critical_m == 8:
        msg = '8 种状态正好填满 3 bit 的全部容量。'
        color = ACCENT_VIOLET
    elif critical_m == 9:
        msg = '第 9 种状态越过了 3 bit 的上限 8，只能升级到 4 bit。'
        color = FOCUS_RED
    elif critical_m > prev_cap:
        msg = f'{prev_cap} < {critical_m} ≤ {cap}，因此最少需要 {n} bit。'
        color = ACCENT_VIOLET
    else:
        msg = f'{critical_m} ≤ {cap}，当前最少需要 {n} bit。'
        color = ACCENT_VIOLET

    py5.fill(color)
    py5.text_size(22)
    py5.text(msg, 66, 575)
    formula_box(f'{prev_cap} < {critical_m} ≤ {cap}', f'最小 n = {n}，使 M ≤ 2^n', 760, 472, 370, 92, danger=(critical_m == 9))


# ============================================================
# Demo 4 — 像素量化
# ============================================================

def draw_pixel_demo():
    levels = 2 ** pixel_bits

    py5.fill(BODY_BLACK)
    py5.text_size(20)
    py5.text('每像素位数 n', 66, 155)
    draw_button(205, 128, 46, 34, '−', text_size=22)
    draw_button(261, 128, 46, 34, '+', text_size=22)
    py5.fill(ACCENT_VIOLET)
    py5.text_size(24)
    py5.text(f'{pixel_bits} bit / pixel  →  {levels} 个灰度等级', 340, 155)

    # 两条灰度带共享同一几何位置，便于直接比较；
    # 额外加入边界、浅灰承托区和离散分隔线，避免白色量化区域融入白色画布。
    x0, y0, gw, gh = 100, 235, 1000, 72
    py5.fill(MUTED_GRAY)
    py5.text_size(16)
    py5.text('理想的连续灰度（用于比较）', x0, y0 - 18)

    # 承托区：不是装饰卡片，只用于建立图形—背景对比与共同边界。
    py5.no_stroke()
    py5.fill(VERY_LIGHT)
    py5.rect(x0 - 8, y0 - 8, gw + 16, gh + 16)

    py5.no_stroke()
    for x in range(gw):
        gray = int(255 * x / (gw - 1))
        py5.fill(gray)
        py5.rect(x0 + x, y0, 1.2, gh)
    # 明确边界，让最右端白色仍然可见。
    py5.no_fill()
    py5.stroke(TITLE_BLACK)
    py5.stroke_weight(1.8)
    py5.rect(x0, y0, gw, gh)

    # Quantized gradient
    qy, qh = 405, 92
    py5.no_stroke()
    py5.fill(MUTED_GRAY)
    py5.text_size(16)
    py5.text(f'数字化后：只能选择 {levels} 个离散等级', x0, qy - 18)

    # 浅灰承托区 + 深色外框形成对比，尤其解决白色等级“消失”在白背景的问题。
    py5.fill(VERY_LIGHT)
    py5.rect(x0 - 8, qy - 8, gw + 16, qh + 16)

    for x in range(gw):
        v = x / (gw - 1)
        level_index = round(v * (levels - 1))
        q = int(255 * level_index / max(1, levels - 1))
        py5.fill(q)
        py5.no_stroke()
        py5.rect(x0 + x, qy, 1.2, qh)

    # 离散等级之间用细分隔线明确“这是若干块，而不是连续渐变”。
    if levels <= 16:
        for i in range(1, levels):
            boundary = x0 + (i - 0.5) / max(1, levels - 1) * gw
            py5.stroke(MUTED_GRAY)
            py5.stroke_weight(1.4)
            py5.line(boundary, qy, boundary, qy + qh)

    py5.no_fill()
    py5.stroke(TITLE_BLACK)
    py5.stroke_weight(2.2)
    py5.rect(x0, qy, gw, qh)

    # 低位深度时标出实际可用灰度等级的位置。
    if levels <= 16:
        for i in range(levels):
            xx = x0 + (i / max(1, levels - 1)) * gw
            py5.stroke(TECH_CYAN)
            py5.stroke_weight(2)
            py5.line(xx, qy + qh + 3, xx, qy + qh + 14)

    # 端点标签既提供语义，也强化白色端仍属于量化条的一部分。
    py5.no_stroke()
    py5.fill(MUTED_GRAY)
    py5.text_size(14)
    py5.text_align(py5.LEFT, py5.BASELINE)
    py5.text('黑 0', x0, qy + qh + 32)
    py5.text_align(py5.RIGHT, py5.BASELINE)
    py5.text('白 255', x0 + gw, qy + qh + 32)
    py5.text_align(py5.LEFT, py5.BASELINE)

    py5.fill(ACCENT_VIOLET)
    py5.text_size(22)
    py5.text('位数越多 → 可区分状态越多 → 量化更细。', 100, 585)
    formula_box(f'2^{pixel_bits} = {levels}', 'n bit / pixel → 最多 2^n 种像素状态', 760, 535, 340, 72)


# ============================================================
# Demo 5 — 声音：采样 + 量化
# ============================================================

def _sound_wave_value(t):
    """教学用复合波：范围大致落在 [-1, 1]，比单纯正弦更接近“声音波形”的观感。"""
    return 0.72 * math.sin(t * math.tau * 1.35) + 0.20 * math.sin(t * math.tau * 3.1 + 0.6)


def _quantize_wave(v, levels):
    """把 [-1, 1] 的连续幅度量化到 levels 个离散等级，并返回量化后的 [-1, 1] 值。"""
    v01 = max(0.0, min(1.0, (v + 1.0) / 2.0))
    idx = int(round(v01 * (levels - 1)))
    q01 = idx / max(1, levels - 1)
    return q01 * 2.0 - 1.0, idx


def draw_sound_demo():
    levels = 2 ** sound_bits

    # Controls — sampling and quantization deliberately separated
    py5.fill(BODY_BLACK)
    py5.text_size(18)
    py5.text('采样点数', 66, 150)
    draw_button(155, 124, 42, 32, '−', text_size=20)
    draw_button(205, 124, 42, 32, '+', text_size=20)
    py5.fill(TECH_CYAN)
    py5.text_size(22)
    py5.text(f'{sound_samples} 个 / 屏', 270, 150)

    py5.fill(BODY_BLACK)
    py5.text_size(18)
    py5.text('量化位数 n', 485, 150)
    draw_button(600, 124, 42, 32, '−', text_size=20)
    draw_button(650, 124, 42, 32, '+', text_size=20)
    py5.fill(ACCENT_VIOLET)
    py5.text_size(22)
    py5.text(f'{sound_bits} bit / sample  →  {levels} 个量化等级', 715, 150)

    # Plot geometry
    x0, x1 = 90, 1110
    w = x1 - x0
    top_y, top_h = 205, 135
    bot_y, bot_h = 402, 135
    mid_top = top_y + top_h / 2
    mid_bot = bot_y + bot_h / 2
    amp = 52

    py5.fill(MUTED_GRAY)
    py5.text_size(15)
    py5.text('① 连续波形 + 离散采样点', x0, top_y - 15)
    py5.text('② 每个采样点只能落到有限的量化等级', x0, bot_y - 15)

    # light axes
    py5.stroke(LIGHT_GRAY)
    py5.stroke_weight(1.5)
    py5.line(x0, mid_top, x1, mid_top)
    py5.line(x0, mid_bot, x1, mid_bot)

    # Continuous wave
    py5.no_fill()
    py5.stroke(TITLE_BLACK)
    py5.stroke_weight(2.2)
    py5.begin_shape()
    for px in range(x0, x1 + 1, 3):
        t = (px - x0) / w
        v = _sound_wave_value(t)
        py5.vertex(px, mid_top - v * amp)
    py5.end_shape()

    # Quantization guide levels (violet), only show all lines for manageable depth
    if levels <= 16:
        for j in range(levels):
            q = -1.0 + 2.0 * j / max(1, levels - 1)
            yy = mid_bot - q * amp
            py5.stroke(ACCENT_VIOLET)
            py5.stroke_weight(1)
            py5.line(x0, yy, x1, yy)
    else:
        # At high bit depths the levels are too dense to draw individually; show representative band lines.
        for j in range(9):
            q = -1.0 + 2.0 * j / 8
            yy = mid_bot - q * amp
            py5.stroke(LIGHT_GRAY)
            py5.stroke_weight(1)
            py5.line(x0, yy, x1, yy)

    # sampled & quantized points
    samples = []
    for i in range(sound_samples):
        t = i / max(1, sound_samples - 1)
        px = x0 + t * w
        v = _sound_wave_value(t)
        qv, idx = _quantize_wave(v, levels)
        y_sample = mid_top - v * amp
        y_quant = mid_bot - qv * amp
        samples.append((px, y_quant))

        # vertical sampling marker on upper graph
        py5.stroke(TECH_CYAN)
        py5.stroke_weight(1.2)
        py5.line(px, mid_top - amp - 8, px, mid_top + amp + 8)
        py5.no_stroke()
        py5.fill(TECH_CYAN)
        py5.circle(px, y_sample, 8)

        # quantized point on lower graph
        py5.fill(ACCENT_VIOLET)
        py5.circle(px, y_quant, 9)

    # connect quantized values as a step-like digital trace
    if len(samples) > 1:
        py5.no_fill()
        py5.stroke(ACCENT_VIOLET)
        py5.stroke_weight(2.6)
        for i in range(len(samples) - 1):
            x_a, y_a = samples[i]
            x_b, y_b = samples[i + 1]
            mid_x = (x_a + x_b) / 2
            py5.line(x_a, y_a, mid_x, y_a)
            py5.line(mid_x, y_a, mid_x, y_b)
            py5.line(mid_x, y_b, x_b, y_b)

    # Compact explanation and formula
    py5.no_stroke()
    py5.fill(TECH_CYAN)
    py5.text_size(17)
    py5.text('采样点数：决定“横向取多少次”', 90, 570)
    py5.fill(ACCENT_VIOLET)
    py5.text('量化位数：决定“每次采样有多少个纵向等级可选”', 395, 570)
    formula_box(f'2^{sound_bits} = {levels}', 'n bit / sample → 最多 2^n 个量化等级', 840, 542, 270, 58)


# ============================================================
# Interaction
# ============================================================

def reset_current_demo():
    global switch_bits, switch_values, parking_bits, critical_m, pixel_bits, sound_bits, sound_samples, slider_dragging
    # 所有实验统一从 1 bit 的认知起点开始。
    if mode == 1:
        switch_bits = 1
        switch_values = [0, 0, 0, 0]
    elif mode == 2:
        parking_bits = 1
        reset_parking()
    elif mode == 3:
        # M=2 时恰好需要 1 bit；再逐步拖动到 8→9 的临界点。
        critical_m = 2
        slider_dragging = False
    elif mode == 4:
        pixel_bits = 1
    elif mode == 5:
        sound_bits = 1
        sound_samples = 16


def auto_parking():
    global parking_assignments
    cap = 2 ** parking_bits
    parking_assignments = [[] for _ in range(cap)]
    for i in range(len(parking_objects)):
        if i < cap:
            parking_assignments[i].append(i)
        else:
            # 容量不足：故意让额外对象撞到最后一个编码槽，用来制造认知冲突
            parking_assignments[-1].append(i)


def place_object(obj_index, slot_index):
    # 先把对象从旧位置移走，再放入新槽。若槽已有对象，就会形成“撞码”。
    for items in parking_assignments:
        if obj_index in items:
            items.remove(obj_index)
    parking_assignments[slot_index].append(obj_index)


def update_slider_from_mouse():
    global critical_m
    sx1, sx2 = 110, 790
    mx, _ = mouse_design()
    x = max(sx1, min(sx2, mx))
    t = (x - sx1) / (sx2 - sx1)
    critical_m = int(round(2 + t * 18))
    critical_m = max(2, min(20, critical_m))


def mouse_pressed():
    global slider_dragging
    mx, my = mouse_design()
    if mode == 3 and 190 <= my <= 250 and 90 <= mx <= 810:
        slider_dragging = True
        update_slider_from_mouse()


def mouse_dragged():
    if mode == 3 and slider_dragging:
        update_slider_from_mouse()


def mouse_released():
    global slider_dragging
    slider_dragging = False


def mouse_clicked():
    global mode, switch_bits, parking_bits, selected_object, critical_m, pixel_bits, sound_bits, sound_samples

    # navigation
    x0, y, w, h, gap = 46, 615, 172, 34, 10
    for i in range(1, 6):
        if hit(x0 + (i - 1) * (w + gap), y, w, h):
            mode = i
            reset_current_demo()
            return

    if mode == 1:
        if hit(150, 132, 46, 34):
            switch_bits = max(1, switch_bits - 1)
            return
        if hit(206, 132, 46, 34):
            switch_bits = min(4, switch_bits + 1)
            return
        start_x, gap2, yy = 88, 122, 215
        for i in range(switch_bits):
            if hit(start_x + i * gap2, yy, 92, 92):
                switch_values[i] = 1 - switch_values[i]
                return

    elif mode == 2:
        if hit(66, 205, 96, 34):
            parking_bits = max(1, parking_bits - 1)
            reset_parking()
            return
        if hit(172, 205, 96, 34):
            parking_bits = min(4, parking_bits + 1)
            reset_parking()
            return
        if hit(282, 205, 110, 34):
            auto_parking()
            return
        if hit(402, 205, 82, 34):
            reset_parking()
            return
        for i in range(len(parking_objects)):
            if hit(70 + i * 78, 305, 58, 58):
                selected_object = i
                return
        cap = 2 ** parking_bits
        cols = 4
        cell_w, cell_h = 132, 93
        gx, gy = 560, 190
        for idx in range(cap):
            row, col = divmod(idx, cols)
            x = gx + col * (cell_w + 14)
            yy = gy + row * (cell_h + 18)
            if hit(x, yy, cell_w, cell_h) and selected_object is not None:
                place_object(selected_object, idx)
                selected_object = None
                return

    elif mode == 3:
        if hit(1000, 198, 48, 34):
            critical_m = max(2, critical_m - 1)
            return
        if hit(1058, 198, 48, 34):
            critical_m = min(20, critical_m + 1)
            return

    elif mode == 4:
        if hit(205, 128, 46, 34):
            pixel_bits = max(1, pixel_bits - 1)
            return
        if hit(261, 128, 46, 34):
            pixel_bits = min(8, pixel_bits + 1)
            return

    elif mode == 5:
        if hit(155, 124, 42, 32):
            sound_samples = max(6, sound_samples - 2)
            return
        if hit(205, 124, 42, 32):
            sound_samples = min(40, sound_samples + 2)
            return
        if hit(600, 124, 42, 32):
            sound_bits = max(1, sound_bits - 1)
            return
        if hit(650, 124, 42, 32):
            sound_bits = min(8, sound_bits + 1)
            return


def key_pressed():
    global mode
    k = str(py5.key).lower()
    if k in ('1', '2', '3', '4', '5'):
        mode = int(k)
        reset_current_demo()
    elif k == 'r':
        reset_current_demo()
    elif k == 'f':
        fit_window_to_screen()
    elif k == 'w':
        restore_design_window()
    elif k == 'm':
        minimize_window()


# 在 JupyterLab 中异步启动窗口；Notebook 仍可继续操作。
py5.run_sketch(block=False)
