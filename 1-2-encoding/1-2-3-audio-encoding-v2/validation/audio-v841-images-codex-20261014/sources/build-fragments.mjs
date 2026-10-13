import fs from 'node:fs/promises';
import path from 'node:path';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
import { GlobalFonts, createCanvas, loadImage } from '@napi-rs/canvas';
import { execFileSync } from 'node:child_process';

const ROOT = path.resolve(process.env.AUDIO_BUILD_DIR ?? '/private/tmp/audio841-images-codex/build');
const LESSON = path.resolve(process.env.AUDIO_LESSON_DIR ?? path.join(path.dirname(new URL(import.meta.url).pathname), '../../..'));
const ASSETS = path.join(LESSON, '1-2-3-audio-encoding-v8.4.10-searched-images/assets');
const phase = Number(process.argv[2] ?? 0);
const F = { regular: 'Alibaba PuHuiTi 3.0 55 Regular', black: 'Alibaba PuHuiTi 3.0 115 Black' };
for (const [file, family] of [['55-Regular', F.regular], ['115-Black', F.black]]) {
  if (!GlobalFonts.registerFromPath(`/Users/chran/Library/Fonts/AlibabaPuHuiTi-3-${file}.ttf`, family)) throw new Error(`Missing font: ${family}`);
}
await fs.mkdir(ROOT, { recursive: true });
const p = Presentation.create({ slideSize: { width: 1279.967979, height: 720 } });
const roster = [];
const textSpecs = [];
const C = { ink: '#262626', violet: '#8C64E1', cyan: '#007C9B', blue: '#00B0F0', gray: '#808080', grid: '#D7D7DE', red: '#FF0000' };
function page(key) { const s = p.slides.add(); s.background.fill = '#FFFFFF'; roster.push(key); return s; }
function txt(s, text, x, y, w = 1152, h = 48, size = 29.333, color = C.ink, strong = false, name = 'image-caption') {
  const o = s.shapes.add({ geometry: 'textbox', name, position: { left: x, top: y, width: w, height: h }, fill: 'none', line: { fill: 'none', width: 0 }, shadow: 'shadow-none' });
  o.text = text; o.text.style = { typeface: strong ? F.black : F.regular, fontSize: size, bold: strong, color, wrap: 'square', autoFit: 'none', insets: 0, verticalAlignment: 'top' };
  textSpecs.push({ key: roster[p.slides.items.indexOf(s)], text, width: w, size, family: strong ? F.black : F.regular, name }); return o;
}
function rect(s, x, y, w, h, color = C.grid, width = 1.5, name = 'evidence-boundary') { return s.shapes.add({ geometry: 'rect', name, position: { left: x, top: y, width: w, height: h }, fill: 'none', line: { fill: color, width }, shadow: 'shadow-none' }); }
function curve(s, points, color = C.gray, width = 2, name = 'signal') {
  const x = Math.min(...points.map(v => v[0])), y = Math.min(...points.map(v => v[1]));
  const w = Math.max(1, Math.max(...points.map(v => v[0])) - x), h = Math.max(1, Math.max(...points.map(v => v[1])) - y);
  return s.shapes.add({ geometry: 'custom', name, position: { left: x, top: y, width: w, height: h }, fill: 'none', line: { fill: color, width }, shadow: 'shadow-none', customPaths: [{ width: w, height: h, commands: points.map((v, i) => ({ [i ? 'lineTo' : 'moveTo']: { x: v[0] - x, y: v[1] - y } })) }] });
}
function line(s, x1, y1, x2, y2, color = C.gray, width = 1.5, name = 'relationship') { return curve(s, [[x1, y1], [x2, y2]], color, width, name); }
function dot(s, x, y, color = C.blue, name = 'sample') { return s.shapes.add({ geometry: 'ellipse', name, position: { left: x - 5, top: y - 5, width: 10, height: 10 }, fill: color, line: { fill: 'none', width: 0 }, shadow: 'shadow-none' }); }
async function image(s, name, x, y, w, h, crop = null) {
  let bytes = await fs.readFile(path.join(ASSETS, name));
  if (name.endsWith('.svg')) {
    const source = bytes.toString().replace('<svg ', '<svg width="720" height="720" ');
    const loaded = await loadImage(Buffer.from(source)); const canvas = createCanvas(720, 720);
    canvas.getContext('2d').drawImage(loaded, 0, 0, 720, 720); bytes = canvas.toBuffer('image/png');
    await fs.writeFile(path.join(ROOT, `${path.parse(name).name}.png`), bytes);
  }
  return s.images.add({ blob: bytes, contentType: 'image/png', alt: name, fit: crop ? 'cover' : 'contain', ...(crop ? { crop } : {}), geometry: 'rect', position: { left: x, top: y, width: w, height: h } });
}
function givens(s, key) {
  if (key === 'q17') txt(s, '范围 [0,8) 分成8段。\n区间 [n,n+1) 的编号为n（n=0～7）。',64,180,1152,98,29.333);
  if (key === 'q22') {
    txt(s,'同一输入3.71；范围 [0,8)，每档中点作代表值。',64,179,1152,58);
    for(const [k,count] of [8,16].entries())txt(s,`${k?4:3} bit：${count}个等级`,100+k*610,264,500,50,32,k?C.cyan:C.violet,true);
  }
  if (key === 'q43') txt(s,'同一录音：采样率、存储位宽和时长不变。\n只将双声道改为单声道。',64,173,1152,100,29.333);
  if (key === 'q53') {
    txt(s,'高度重复的内容',64,185,552,52,32,C.ink,true);txt(s,'变化复杂的内容',706,185,510,52,32,C.ink,true);
    txt(s,'AAAAAAAAAA…',64,288,552,70,32);txt(s,'AX3Q9P8F2…',706,288,510,70,32);
  }
  if (key === 'q12') txt(s,'同一段示意信号：左侧全段，右侧放大红框。',64,173,1152,56);
  if (key === 'q24') txt(s,'输入、采样率和时长不变，只将3 bit改为4 bit。',64,175,1152,58);
  if (key === 'q69') {
    txt(s,'三个样本：时刻0、0.5、1 s，幅度1、−1、1。',64,180,1152,57);
    txt(s,'波形A',64,286,200,46,29.333,C.ink,true);
    line(s,280,346,1170,346);
    for(const [j,v]of [1,-1,1].entries()){dot(s,296+j*420,346-65*v,C.ink,`same-alias-point-0-${j}`);txt(s,['0','0.5','1'][j]+' s',270+j*420,423,110,40,24);}
  }
}

let s = page('p2'); await image(s, 'smartphone.svg', 887, 320, 190, 190);
s = page('p5'); await image(s, 'microphone-studio.svg', 546, 255, 170, 170);
s = page('p8');
txt(s, '扬声器周围：空间中的传播', 64, 183, 570, 78, 32, C.ink, true);
txt(s, '同一位置：信号随时间变化', 706, 183, 510, 78, 32, C.ink, true);
if (phase >= 1) {
  await image(s, 'speaker-soundwave-0180.png', 64, 243, 544, 317.333, { left: .55, top: 125 / 450, right: 0, bottom: 115 / 450 });
  txt(s, '扬声器振膜', 86, 568, 266, 40); txt(s, '声波扰动', 406, 568, 212, 40);
} else await image(s, 'speaker-soundwave-0040.png', 64, 276, 554, 311.625);
line(s, 738, 425, 1165, 425); line(s, 750, 290, 750, 570);
curve(s, Array.from({ length: 121 }, (_, i) => [760 + 394 * i / 120, 425 - 82 * Math.sin(i / 120 * 4 * Math.PI)]), C.violet);
txt(s, '幅度', 738, 270, 100, 43); txt(s, '时间', 1080, phase>=1?551:575, 120, 43);
txt(s, '曲线横轴记录时间，不能把它当作空气的运动路径。', 64, phase >= 1 ? 612 : 628, 1152, 44);

s = page('p9');
txt(s, '先预测：红色光标向右，表示声音向右传播吗？', 64, 176, 1152, 80);
await image(s, 'audacity-spectrogram-waveform.png', 132, 290, 1016, 254.4);
line(s, 825, 295, 825, 545, C.red, 3, 'playback-cursor');
txt(s, '波形显示（Audacity示例）', 64, 240, 1152, 48);
txt(s, phase >= 2 ? '横向是时间' : '播放时间方向', 850, 560, 360, 50);
txt(s, '请观察：播放继续时，光标位置怎样变化？', 64, 625, 1152, 48);

s = page('p41');
txt(s, '编辑工程：2条音轨', 64, 185, 620, 50, 32, C.violet, true);
txt(s, '模型：导出2个声道', 714, 185, 500, 50, 32, C.cyan, true);
await image(s, 'audacity-multitrack-mixing.png', 64, phase >= 2 ? 290 : 265, 600, 600 * 309 / 849);
if (phase >= 2) { txt(s, '看左侧两个独立控制区', 64, 237, 606, 46); rect(s, 64, 290, 107, 600 * 309 / 849, C.red, 3, 'track-control-focus'); }
txt(s, '此例：1条单声道音轨 + 1条立体声音轨', 64, 527, 606, 80);
rect(s, 738, 289, 125, 159, C.violet, 2, 'mixing-operation'); txt(s, '混音', 755, 346, 102, 45, 29.333, C.ink, true);
line(s, 672, 304, 736, 334, C.violet, 2); line(s, 672, 431, 736, 399, C.cyan, 2);
line(s, 863, 368, 899, 368, C.violet, 2); line(s, 899, 305, 899, 438, C.violet, 2);
line(s, 899, 305, 925, 305, C.violet, 2); line(s, 899, 438, 925, 438, C.violet, 2);
for (let k = 0; k < 2; k++) {
  const y = 305 + 133 * k; txt(s, k ? 'R' : 'L', 916, y - 48, 70, 44, 29.333, C.cyan, true);
  curve(s, Array.from({ length: 101 }, (_, j) => { const t = j / 100; return [949 + 245 * t, y - 20 * (Math.sin(4 * Math.PI * t) + .5 * Math.sin(10 * Math.PI * t))]; }), C.blue, 2, `mixed-output-${k}`);
}
txt(s, 'L、R都可包含两条音轨的内容', 714, 527, 500, 82);
txt(s, '容量由导出的声道数决定；编辑工程的音轨数另行统计。', 64, 626, 1152, 48);

s = page('p65');
await image(s, 'folder.svg', 170, 300, 185, 185); await image(s, 'video-camera.svg', 812, 300, 185, 185);
txt(s, '重要文档长期备份', 64, 189, 552, 48, 32, C.ink, true); txt(s, '实时视频通话', 706, 189, 510, 48, 32, C.ink, true);
txt(s, '优先完整恢复、可靠保存', 64, 517, 552, 86); txt(s, '兼顾质量、延迟与传输量', 706, 517, 510, 86);
txt(s, '选择依据是任务要求，文件大小只是其中一个条件。', 64, 625, 1152, 48);

if (phase >= 1) {
  // Neutral givens for the duplicated question stages.
  for (const [key, text] of [['q17', '范围 [0,8) 分成8段。第n段是 [n,n+1)，编号为n。\n请独立判断3.71所在的区间，并说明依据。'], ['q21', '需要表示0～7这8个不同等级。\n至少需要多少bit？请写出你计算的方法。'], ['q22', '输入范围和采样时刻不变。\n把8个等级改为16个等级，会改变什么？'], ['q29', '采样率、存储位宽、声道数、时长。\n这四个参数各在数什么？'], ['q43', '同一录音，采样率、存储位宽和时长都不变。\n只将输出由双声道改为单声道。'], ['q53', 'A：AAAAAAAAAA…\nB：AX3Q9P8F2…\n请分别提出一种简短而能完整恢复的表示方法。']]) { s = page(key); if(phase>=2 && ['q17','q22','q43','q53'].includes(key))givens(s,key);else if(phase<2 || !['q21','q29'].includes(key))txt(s, text, 64, 238, 1152, 260, 32); }
  s = page('q19');
  if(phase<2){txt(s, '已量化的10个等级：', 64, 205, 1152, 50);const levels = [3, 5, 7, 6, 4, 2, 0, 1, 3, 4]; levels.forEach((v, j) => { txt(s, String(j + 1), 76 + j * 112, 306, 95, 45, 24, C.gray); txt(s, String(v), 76 + j * 112, 378, 95, 58, 40); });}
  txt(s, phase >= 2 ? '沿采样顺序，用3 bit写出各等级的码字。' : '沿采样顺序，写出每个等级对应的码字。', 64, 523, 1152, 90, 32);
  s = page('q59'); if(phase<2)['ZIP / RAR', 'MP3', 'WAV', 'MP4'].forEach((t, j) => txt(s, t, 64 + j % 2 * 642, 250 + Math.floor(j / 2) * 165, 500, 70, 40, C.ink, true));
  s = page('q65'); await image(s, 'folder.svg', 170, 300, 185, 185); await image(s, 'video-camera.svg', 812, 300, 185, 185);
  txt(s, '重要文档长期备份', 64, 189, 552, 48, 32, C.ink, true); txt(s, '实时视频通话', 706, 189, 510, 48, 32, C.ink, true);
  s = page('q36'); if(phase<2)[['48,000 Hz', 64, 250], ['16 bit', 706, 250], ['2', 64, 450], ['60 s', 706, 450]].forEach(([v, x, y]) => txt(s, v, x, y, 510, 60, 40));
  if (phase >= 2) {
    for(const key of ['q12','q24','q69']){s=page(key);givens(s,key);}
  }
  // Previously established concepts retain their positions in all six tree builds.
  const nodes = [
    ['录音与播放', '麦克风 / ADC；DAC / 扬声器'],
    ['数字化与表示', '采样定时刻；量化定代表值；码字表示'],
    ['PCM样本数据量', '采样率 × 时长 × 声道数 × 存储位宽 ÷ 8'],
    ['逐帧未压缩视频', '单帧像素数据量 × 总帧数'],
    ['压缩的目的', '节省空间；减少传输数据量'],
    ['压缩的恢复标准', '无损：逐字节一致；有损：允许损失']
  ];
  for (let stage = 1; stage <= 6; stage++) {
    s = page(`tree${stage}`); txt(s, '数据的表示', 64, 185, 240, 50, 36, C.ink, true, 'tree-root');
    line(s, 306, 208, 355, 208, C.violet, 2, 'tree-root-edge'); line(s, 355, 208, 355, 607, C.violet, 2, 'tree-spine');
    for (let j = 0; j < stage; j++) {
      const y = 185 + j * 73; line(s, 355, y + 24, 383, y + 24, C.violet, 2, `tree-edge-${j}`);
      txt(s, nodes[j][0], 394, y, 292, 48, 29.333, C.ink, true, `tree-node-${j}`);
      txt(s, nodes[j][1], 711, y, 492, 66, 24, C.ink, false, `tree-description-${j}`);
    }
    rect(s, 385, 176 + (stage - 1) * 73, 831, 66, C.red, 3, 'tree-new-focus');
    txt(s, '本次新增', 64, 610, 292, 48, 29.333, C.violet, true, 'tree-focus-label');
  }
}

if (phase >= 2) {
  const model = t => .72 * Math.sin(10 * Math.PI * t + .3);
  s = page('p12');
  givens(s,'q12');
  txt(s, '整体：0～1 s', 64, 247, 552, 48, 32, C.ink, true); txt(s, '局部：0.30～0.50 s', 706, 247, 510, 48, 32, C.ink, true);
  for (const [k, x, a, b] of [[0, 112, 0, 1], [1, 750, .3, .5]]) {
    line(s, x, 430, x + 430, 430); line(s, x, 312, x, 548);
    curve(s, Array.from({ length: 201 }, (_, j) => { const t = a + (b - a) * j / 200; return [x + 430 * j / 200, 430 - 110 * model(t)]; }), C.violet);
    txt(s, a.toFixed(k ? 2 : 0), x - 28, 551, 90, 45, 24); txt(s, b.toFixed(k ? 2 : 0), x + 396, 551, 90, 45, 24);
    txt(s, '时间 / s', x + 275, 584, 160, 42, 24); txt(s, '幅度', x - 45, 301, 100, 40, 24);
  }
  rect(s, 112 + 430 * .3, 317, 430 * .2, 228, C.red, 2.5, 'selected-time-window');
  for (let j = 15; j <= 25; j++) { const t = j / 50; dot(s, 750 + 430 * (t - .3) / .2, 430 - 110 * model(t), C.blue, `zoom-point-${j}`); }
  s = page('p13'); txt(s, '比较同一秒 [0,1)：右端1 s不重复计入。', 64, 173, 1152, 55);
  for (const [k, hz] of [1, 2].entries()) {
    const y = 340 + k * 193; txt(s, `${hz} Hz`, 64, y - 72, 220, 44, 32, C.ink, true); line(s, 312, y, 1175, y);
    for (let j = 0; j < hz; j++) { dot(s, 312 + 800 * j / hz, y - 32, k ? C.blue : C.violet, `rate-${hz}-point-${j}`); line(s, 312 + 800 * j / hz, y - 32, 312 + 800 * j / hz, y, C.grid); }
    txt(s, '0 s', 296, y + 18, 80, 43, 24); txt(s, '1 s', 1097, y + 18, 90, 43, 24); if (hz === 2) txt(s, '0.5 s', 682, y + 18, 110, 43, 24);
  }
  txt(s, '采样率在数记录次数：1 Hz取1次，2 Hz取2次。', 64, 635, 1152, 45);
  s = page('p18');
  txt(s, '输入3.71属于 [3,4)，等级编号为L3。', 64, 180, 1152, 58, 32);
  rect(s, 236, 321, 650, 120, C.violet, 2, 'grade-3-interval');
  txt(s, '3', 216, 455, 85, 48); txt(s, '4', 866, 455, 85, 48);
  dot(s, 561, 383, C.violet, 'midpoint-3.5'); txt(s, '代表幅度3.5', 441, 490, 310, 52, 32, C.violet, true);
  dot(s, 697.5, 383, C.red, 'input-3.71'); txt(s, '原值3.71', 673, 251, 262, 52, 32, C.ink, true); line(s, 705, 307, 697.5, 372, C.red, 2);
  txt(s, '按本课规则，以区间中点3.5近似3.71。', 64, 612, 1152, 56);
  s = page('p22');
  givens(s,'q22');
  for (const [k, count] of [8, 16].entries()) {
    const x = 100 + k * 610;
    for (let j = 0; j < count; j++) { line(s, x, 523 - (j + .5) / count * 193, x + 450, 523 - (j + .5) / count * 193, k ? C.blue : C.violet, 1.5, `representative-${count}-${j}`); }
    txt(s, k ? '所在区间 [3.5,4)' : '所在区间 [3,4)', x, 554, 510, 45);
    txt(s, k ? '代表值3.75；误差0.04' : '代表值3.5；误差0.21', x, 609, 510, 50, 29.333, k ? C.cyan : C.violet, true);
  }
  s = page('p31');
  txt(s, 'PCM样本数据量（Byte）\n= 采样率 × 时长 × 声道数 × 存储位宽 ÷ 8', 64, 175, 1152, 104, 32, C.violet, true);
  const factors = [['采样率', '样本 / 秒'], ['时长', '秒'], ['声道数', '每时刻几路'], ['存储位宽', 'bit / 样本']];
  factors.forEach(([label, unit], i) => { const x = 64 + i * 288; rect(s, x, 339, 248, 122, i === 3 ? C.blue : C.violet, 2); txt(s, label, x + 16, 357, 220, 43, 29.333, C.ink, true); txt(s, unit, x + 16, 409, 220, 42, 29.333); if (i < 3) txt(s, '×', x + 257, 375, 42, 44, 29.333); });
  txt(s, '前三项相乘，得到所有声道的样本总数。', 64, 505, 1152, 46);
  txt(s, '再乘存储bit/样本，最后按8 bit = 1 Byte换算。', 64, 559, 1152, 46);
  txt(s, '固定存储位宽的未压缩PCM；不含文件头等结构。', 64, 610, 1152, 46);
  s = page('p24');
  givens(s,'q24');
  const values = [3.71,5.2,7.1,6.4,4.15,2.3,.65,1.4,3.2,4.8];
  for (const [k, bits] of [3,4].entries()) {
    const count = 2 ** bits, base = 390 + k * 180, Y = v => base - 130 * v / 8;
    txt(s, `${bits} bit\n${count}个代表值`, 64, base - 114, 300, 110, 32, k ? C.cyan : C.violet, true);
    for (let j = 0; j < count; j++) line(s, 425, Y((j+.5)*8/count), 1190, Y((j+.5)*8/count), C.grid, 1, `quant-grid-${bits}-${j}`);
    values.forEach((v,j) => { const x=440+j*80, rep=(Math.floor(v/(8/count))+.5)*8/count;
      line(s,x,Y(v),x,Y(rep),C.gray,1);
      s.shapes.add({geometry:'ellipse',name:`original-${bits}-${j}`,position:{left:x-5,top:Y(v)-5,width:10,height:10},fill:'#FFFFFF',line:{fill:C.ink,width:1.5},shadow:'shadow-none'});
      dot(s,x,Y(rep),k?C.blue:C.violet,`quantized-${bits}-${j}`);
    });
  }
  txt(s, '空心点是原值，实心点是代表值；两行的记录时刻一一对应。', 64, 632, 1152, 48);
  s = page('p69');
  givens(s,'q69');
  for(const [k,f] of [1,3].entries()) {
    const y=346+k*189;if(k){txt(s,'波形B',64,y-60,200,46,29.333,C.ink,true);line(s,280,y,1170,y);for(const[j,v]of[1,-1,1].entries())dot(s,296+j*420,y-65*v,C.ink,`same-alias-point-${k}-${j}`);}
    curve(s,Array.from({length:241},(_,j)=>[296+840*j/240,y-65*Math.cos(2*Math.PI*f*j/240)]),k?C.blue:C.violet);
  }
  txt(s, '仅凭这三个点，不能唯一确定中间的连续变化。',64,637,1152,46);
  s=page('p17');givens(s,'q17');
  for(let j=0;j<8;j++){const x=112+j*132;rect(s,x,383,132,95,j===3?C.violet:C.grid,j===3?3:1);txt(s,String(j),x+43,408,60,45,32,j===3?C.violet:C.ink,true);txt(s,String(j),x-15,485,60,40,24);}
  txt(s,'8',1153,485,60,40,24);dot(s,112+3.71*132,346,C.red,'input-3.71');line(s,112+3.71*132,351,112+3.71*132,379,C.red,2);txt(s,'3.71',112+3.71*132-42,288,140,50,32,C.ink,true);
  txt(s,'3.71落在 [3,4)，所以等级编号是3。',64,605,1152,55);
  s=page('p43');givens(s,'q43');txt(s,'双声道：2路',64,311,552,50,32,C.violet,true);txt(s,'单声道：1路',706,311,510,50,32,C.cyan,true);
  rect(s,64,397,510,53,C.violet,2);rect(s,64,475,510,53,C.violet,2);rect(s,706,436,510,53,C.blue,2);
  txt(s,'固定宽度PCM：输出声道数减半，样本数据量随之减半。',64,625,1152,50);
  s=page('p53');givens(s,'q53');txt(s,'能用重复次数简短地表达',64,438,552,100);txt(s,'通常需要更多信息描述变化',706,438,510,100);txt(s,'压缩效果取决于内容和算法；不能仅根据原始文件大小判断。',64,625,1152,50);
  s=page('p28');
  ['数字样本','DAC','连续电信号','扬声器'].forEach((label,j)=>{const x=64+j*296;rect(s,x,271,248,86,j%2?C.blue:C.violet,2);txt(s,label,x+14,293,223,48,29.333,C.ink,true);if(j<3)s.shapes.add({geometry:'rightArrow',name:'playback-flow',position:{left:x+256,top:303,width:32,height:22},fill:C.violet,line:{fill:'none',width:0},shadow:'shadow-none'});});
  txt(s,'播放将数字样本转换为电信号，再让扬声器产生声波。',64,529,1152,80,32);
  s=page('reveal21');txt(s,'= 2³，所以至少需要3 bit',355,176.64,850,73.92,40,C.violet,true);
  s=page('p3');
  const physical=execFileSync(process.env.AUDIO_PYTHON??'/Users/chran/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',['-c','from zipfile import ZipFile;import sys;sys.stdout.buffer.write(ZipFile(sys.argv[1]).read("ppt/media/image4.png"))',path.join(LESSON,'1-2-3-audio-encoding-v8.4.1.pptx')]);
  s.images.add({blob:physical,contentType:'image/png',alt:'Original physical sound diagram; native crop removes white margins',fit:'cover',crop:{left:0,top:60/540,right:0,bottom:30/540},geometry:'rect',position:{left:176,top:246,width:960,height:360}});
  txt(s,'振动声源',210,178,290,48,32,C.violet,true);txt(s,'空气中的声压扰动',499,178,370,48,32,C.ink,true);txt(s,'麦克风接收',910,178,306,48,32,C.cyan,true);
  txt(s,'声压扰动向外传播；圆弧仅作波阵面示意。',64,618,1152,38);
  s=page('p14');txt(s,'比较同一秒 [0,1)：输入、存储位宽和声道数不变。',64,173,1152,56);
  for(const[k,hz]of[8,20].entries()){
    const y=333+k*187;txt(s,`${hz} Hz`,64,y-33,240,58,32,k?C.cyan:C.violet,true);
    line(s,312,y,1176,y);curve(s,Array.from({length:201},(_,j)=>[312+864*j/200,y-52*Math.sin(4*Math.PI*j/200+.3)]),C.gray,1.5);
    for(let j=0;j<hz;j++){const t=j/hz;dot(s,312+864*t,y-52*Math.sin(4*Math.PI*t+.3),k?C.blue:C.violet,`rate-density-${hz}-${j}`);}
    txt(s,'0 s',296,y+65,85,36,24);txt(s,'1 s',1136,y+65,80,36,24);
  }
  txt(s,'记录间隔变短，每秒样本更多。',64,620,1152,36);
  s=page('p58');
  line(s,638,171,638,567,C.grid,2);
  txt(s,'无损压缩',86,182,533,73,37.333,C.violet);
  txt(s,'有损压缩',678,182,510,73,37.333,C.cyan);
  txt(s,'还原以后，与原始数据完全一致。\n\n适合：文档、程序、精确备份。',86,288,533,240,30.667);
  txt(s,'还原以后，不能完全恢复原始数据。\n\n适合：可接受部分失真的音视频。',678,288,538,240,30.667);
  txt(s,'判断标准：解码/解压后，能否完整得到原始数据？',82,610,1133,46,26.667,C.violet,true);
}

const fontContext = createCanvas(10, 10).getContext('2d'); const fit = [];
for (const o of textSpecs) {
  fontContext.font = `${o.size}px "${o.family}"`;
  const maxLine = Math.max(...o.text.split('\n').map(t => fontContext.measureText(t).width));
  if (maxLine > o.width + 1 && !o.text.includes('\n')) fit.push({ key: o.key, name: o.name, text: o.text, width: o.width, measured: maxLine });
}
await (await PresentationFile.exportPptx(p)).save(path.join(ROOT, `fragments-${phase}.pptx`));
await fs.writeFile(path.join(ROOT, `fragment-roster-${phase}.json`), JSON.stringify(roster, null, 2));
await fs.writeFile(path.join(ROOT, `fragment-fit-${phase}.json`), JSON.stringify(fit, null, 2));
console.log(JSON.stringify({ phase, fragmentSlides: roster.length, fitWarnings: fit }));
