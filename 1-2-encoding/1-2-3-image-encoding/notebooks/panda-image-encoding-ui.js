/* Standalone JupyterLab browser presentation. No network, notebook widgets, or external JS. */
function mountPandaEncoding(mount, payload, config) {
  const features = new Set(config.features || []);
  const state = {
    stage: Number(config.stage || 0),
    grid: Number(config.grid || 8),
    levels: Number(config.levels || 4),
    selected: 0
  };
  const labels = ["① 原图", "② 采样", "③ 量化", "④ 编码"];
  const questions = [
    "观察这只熊猫：要让计算机保存这幅图，我们先要决定什么？",
    "同一区域从 8×8 改为 16×16：增加的是取样位置，还是可选颜色？",
    "保持位置不变：从 4 色改为 6 色，改变了什么？",
    "颜色等级确定后，怎样把它写成等长二进制码字？"
  ];
  const explanations = [
    "先观察原图，预测。暂不显示数字化的后续结果。",
    "采样：在有限的二维空间位置获取样本；本模型每块记录一个 RGB 平均值。",
    "量化：从固定调色板中选择一个代表色，记录对应的等级编号。",
    "编码：按颜色编号写出固定长度的二进制码字，按行优先排列。"
  ];
  function make(tag, className, content) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (content !== undefined) node.textContent = String(content);
    return node;
  }
  function add(parent, ...nodes) { for (const n of nodes) parent.appendChild(n); return parent; }
  function rgb(vals) { return 'rgb(' + vals.map(v => Math.round(v)).join(',') + ')'; }
  function setClass(root) {
    root.className = 'panda-demo'
      + (features.has('largeType') ? ' pd-large-type' : '')
      + (features.has('fixedAlignment') ? ' pd-align' : '')
      + (features.has('highContrast') ? ' pd-contrast' : '')
      + (features.has('largeTargets') ? ' pd-big-target' : '')
      + (features.has('projectionCompact') ? ' pd-projection' : '');
  }
  const root = make('section', 'panda-demo');
  setClass(root);
  mount.replaceChildren(root);
  function current() { return payload.states[String(state.grid)][String(state.levels)]; }
  function swatchLabel(index) {
    return state.levels + '色表｜编号 ' + index + '｜RGB ' + payload.palette[index].join(',');
  }
  function draw() {
    root.replaceChildren();
    const currentState = current();
    const count = currentState.pixel_count;
    state.selected = Math.min(state.selected, count - 1);
    const rowIndex = Math.floor(state.selected / state.grid);
    const columnIndex = state.selected % state.grid;
    const sample = currentState.samples[rowIndex][columnIndex];
    const index = currentState.indices[rowIndex][columnIndex];
    const code = currentState.codes[state.selected];

    add(root, make('div','pd-eyebrow','信息科技｜图像编码｜交互观察'));
    add(root, make('h2','', '一只熊猫，怎样变成数字数据？'));
    add(root, make('div','pd-intro muted', '请先预测，再由教师揭示下一阶段；每次只改变一个条件。'));

    const tabs = make('div','pd-stages');
    labels.forEach((name, i) => {
      const button = make('button','',name);
      button.type = 'button';
      button.setAttribute('aria-pressed', String(state.stage === i));
      button.addEventListener('click', () => { state.stage = i; draw(); });
      tabs.appendChild(button);
    });
    add(root,tabs);

    const controls = make('div','pd-controlbar');
    const gridLabel = make('label','','采样网格');
    const gridSelect = make('select');
    [8,16].forEach(n => { const opt = make('option','',n+'×'+n); opt.value=n; gridSelect.appendChild(opt); });
    gridSelect.value=String(state.grid);
    gridSelect.disabled = state.stage < 1;
    gridSelect.setAttribute('aria-label','采样网格');
    gridSelect.addEventListener('change', () => { state.grid=Number(gridSelect.value); state.selected=0; draw(); });
    add(gridLabel,gridSelect);

    const paletteLabel = make('label','','可选颜色');
    const levelSelect = make('select');
    [4,6].forEach(n => { const opt=make('option','',n+' 色'); opt.value=n; levelSelect.appendChild(opt); });
    levelSelect.value=String(state.levels);
    levelSelect.disabled = state.stage < 2;
    levelSelect.setAttribute('aria-label','调色板颜色数');
    levelSelect.addEventListener('change', () => { state.levels=Number(levelSelect.value); draw(); });
    add(paletteLabel,levelSelect);
    controls.appendChild(gridLabel);
    controls.appendChild(paletteLabel);
    add(root,controls);

    if (features.has('questionEmphasis')) add(root,make('div','pd-eyebrow','先写出你的预测，再运行验证'));
    const question=make('div','pd-question',questions[state.stage]);
    if(features.has('focusMarker')) question.style.borderLeftColor='#ff0000';
    add(root,question);

    const layout=make('div','pd-layout');
    const originalPanel=make('div','pd-panel');
    add(originalPanel,make('div','pd-panel-title','原图｜同一块熊猫区域'));
    const img=make('img','pd-preview');
    img.src=payload.preview;
    img.alt='原始熊猫图局部，未经本次演示网格或调色板处理';
    originalPanel.appendChild(img);
    add(originalPanel,make('div','pd-stephelp','源图像素已是数字数据；下方演示是在解码后的 JPEG 上进行的数字化概念模型。'));
    layout.appendChild(originalPanel);

    const resultPanel=make('div','pd-panel');
    add(resultPanel,make('div','pd-panel-title', state.stage === 0 ? '待揭示结果'
      : state.stage === 1 ? '采样后的 RGB 样本'
      : state.stage === 2 ? '有限调色板的量化结果' : '量化像素与对应码字'));
    if(state.stage === 0) {
      add(resultPanel,make('div','pd-no-yet','先讨论：图像中的哪些信息需要记录？'));
    } else {
      const grid=make('div','pd-grid');
      grid.style.gridTemplateColumns='repeat('+state.grid+',minmax(0,1fr))';
      for(let i=0;i<count;i++){
        const r=Math.floor(i/state.grid),c=i%state.grid;
        const color=state.stage===1 ? rgb(currentState.samples[r][c]) : rgb(payload.palette[currentState.indices[r][c]]);
        const cell=make('button','pd-cell'+(state.selected===i?' is-selected':''));
        cell.type='button';cell.style.backgroundColor=color;
        cell.setAttribute('aria-label','第'+(r+1)+'行第'+(c+1)+'列样本');
        cell.setAttribute('aria-pressed',String(state.selected===i));
        cell.addEventListener('click',()=>{state.selected=i;draw();});
        grid.appendChild(cell);
      }
      resultPanel.appendChild(grid);
      const sourceBlock=288/state.grid;
      const countSummary=make('div','pd-stephelp',
        '固定原 JPEG 同一 288×288 像素区域；每格覆盖 '+sourceBlock+'×'+sourceBlock+' 个源像素。'
        +' 网格 '+state.grid+'×'+state.grid+'：共 '+count+' 个样本位置。'
        +(state.stage>=2 ? ' 此时可选颜色为 '+state.levels+' 种。' : ' 此时尚未做有限色表量化。'));
      resultPanel.appendChild(countSummary);
    }
    layout.appendChild(resultPanel);
    root.appendChild(layout);

    if(state.stage>=1) {
      const detail=make('div','pd-evidence');
      function pair(name,value) { detail.appendChild(make('dt','',name));detail.appendChild(make('dd','',value));}
      pair('选中位置','第 '+(rowIndex+1)+' 行，第 '+(columnIndex+1)+' 列');
      pair('采样的 RGB 均值',sample.map(x=>x.toFixed(2)).join('，'));
      if(state.stage>=2) {
        pair('量化后的代表色编号',String(index));
        pair('代表色 RGB',payload.palette[index].join('，'));
        if(features.has('sampleMagnifier')) {
          const mag=make('dd');
          const sq=make('span','pd-mag');sq.style.backgroundColor=rgb(payload.palette[index]);
          mag.appendChild(sq);mag.appendChild(make('span','', '选中代表色'));
          detail.appendChild(make('dt','','代表色放大观察'));detail.appendChild(mag);
        }
      }
      if(state.stage>=3) {
        pair('该色表的最短固定码长',currentState.bits+' bit / 像素');
        pair('颜色编号 → 二进制码字',index+' → '+code);
        pair('理想像素码字数据量',currentState.ideal_payload_bits+' bit = '+(currentState.ideal_payload_bits/8)+' B');
      }
      root.appendChild(detail);
    }
    if(state.stage>=2 && features.has('paletteLegend')) {
      const legend=make('div','pd-legend');
      for(let i=0;i<state.levels;i++){
        const entry=make('span');
        const swatch=make('span','pd-swatch');swatch.style.backgroundColor=rgb(payload.palette[i]);
        add(entry,swatch,make('span','', 'L'+i));
        legend.appendChild(entry);
      }
      root.appendChild(legend);
    }
    if(state.stage>=2 && state.levels===6) {
      add(root,make('div','pd-subtitle','六色表保留原四色并新增两色；这只扩大可选颜色集合，不改变采样位置。'));
    }
    if(state.stage===3){
      if(features.has('codeFocus')) add(root,make('div','pd-binaryfocus','L'+index+' → '+code));
      add(root,make('div','pd-stephelp','同一行的码字（从左到右）；点击码字可定位相应像素。'));
      const band=make('div','pd-codeband');
      const left=rowIndex*state.grid;
      for(let c=0;c<state.grid;c++){
        const i=left+c;
        const btn=make('button',i===state.selected?'is-selected':'',currentState.codes[i]);
        btn.type='button';btn.setAttribute('aria-label','本行第'+(c+1)+'个码字');
        btn.setAttribute('aria-pressed',String(i===state.selected));
        btn.addEventListener('click',()=>{state.selected=i;draw();});
        band.appendChild(btn);
      }
      root.appendChild(band);
      add(root,make('div','pd-summary','采样确定位置 → 量化确定等级 → 编码确定数字表示'));
      add(root,make('div','pd-subtitle','2 bit 可表示 4 种状态；6 色表需至少 3 bit。码字是编号表示，不是新的颜色。'));
    }
    if(features.has('responsiveAid')) add(root,make('div','pd-subtitle','窄屏布局会纵向排列；投影时建议浏览器全屏。'));
    const footer=make('div','pd-footer');
    add(footer,make('span','',explanations[state.stage]+' '));
    add(footer,make('span','',payload.model_notice));
    add(footer,make('div','', '边界：未压缩理想码字数据量不等于 PNG/JPEG 完整文件大小；模型不模拟真实传感器和色彩管理。'));
    root.appendChild(footer);
  }
  draw();
}
