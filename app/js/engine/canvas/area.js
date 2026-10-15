/* area canvas: a rectangle, square or circle split into a grid of cells (or sectors), for fraction and multiplication
   area models and geometric probability. Up to three shadings overlay (set 1 solid wash, later sets hatched), so
   2/3 of 3/4 reads as the crossed region. Cell ids c{i}{j}, one-based from the top left (c{i}-{j} when either index
   is 10 or more); a circle's sectors are c1{j} clockwise from twelve o'clock. state.grid re-cuts the shape into a new
   grid (the cells are rebuilt; a fractional shade then lands on the new cells), state.split draws dashed cut lines.
   Explore controls bind to them through setParam: "split" (the number of columns cut, or sectors on a circle),
   "split.rows", "split.cols", "grid" (columns, or sectors), "grid.rows", "grid.cols", and "shade" (a fraction). Grid lines inside shaded cells
   are drawn again over the shading so they stay visible. Params and state: engine/canvas/README.md. */
(function () {
  'use strict';
  const Z = window.ZQ, C = Z.canvas, { svg, attrs, lerp } = C;
  let uid = 0;

  function area(host, params, ctx = {}) {
    const P = params || {};
    const shape = P.shape === 'circle' ? 'circle' : P.shape === 'square' ? 'square' : 'rect';
    let sectors = shape === 'circle' ? (P.sectors || (P.grid ? P.grid[1] : 1)) : 0;
    let rows = shape === 'circle' ? 1 : Math.max(1, (P.grid || [1, 1])[0]), cols = shape === 'circle' ? sectors : Math.max(1, (P.grid || [1, 1])[1]);
    const L = P.labels || {};
    const hasTop = !!(L.top || P.colLabels), hasLeft = !!(L.left || P.rowLabels), hasBottom = !!L.bottom, hasRight = !!L.right;
    const sizes = (list, n) => { const a = list && list.length === n ? list : Array(n).fill(1); const s = a.reduce((x, y) => x + y, 0); let acc = 0; return [0, ...a.map(v => (acc += v) / s)]; };
    let cx = sizes(P.colSizes, cols), cy = sizes(P.rowSizes, rows);
    let w, h;
    if (shape === 'circle') { w = h = 264; }
    else if (shape === 'square') { w = h = 264; }
    else { const [a, b] = P.size || [3, 2]; const k = Math.min(400 / a, 264 / b); w = a * k; h = b * k; }
    const W = 540, ox = (W - w) / 2 + (hasLeft ? 10 : 0) - (hasRight ? 10 : 0), oy = hasTop ? 36 : 12, H = oy + h + (hasBottom ? 38 : 14);
    const fr = C.frame(host, W, H, { label: P.label || 'Area model' });
    const g = fr.g;
    const id = ++uid;
    const R = w / 2, ccx = ox + R, ccy = oy + R;
    const cellId = (i, j) => (i >= 10 || j >= 10 ? `c${i}-${j}` : `c${i}${j}`);
    const ang = (j) => -Math.PI / 2 + (j / sectors) * 2 * Math.PI;
    const sectorPath = (a0, a1) => {
      if (a1 - a0 >= 2 * Math.PI - 1e-6) return `M${ccx - R} ${ccy}A${R} ${R} 0 1 1 ${ccx + R} ${ccy}A${R} ${R} 0 1 1 ${ccx - R} ${ccy}Z`;
      const p0 = [ccx + R * Math.cos(a0), ccy + R * Math.sin(a0)], p1 = [ccx + R * Math.cos(a1), ccy + R * Math.sin(a1)];
      return `M${ccx} ${ccy}L${p0[0]} ${p0[1]}A${R} ${R} 0 ${a1 - a0 > Math.PI ? 1 : 0} 1 ${p1[0]} ${p1[1]}Z`;
    };
    const cellBox = (i, j) => ({ x: ox + cx[j - 1] * w, y: oy + cy[i - 1] * h, w: (cx[j] - cx[j - 1]) * w, h: (cy[i] - cy[i - 1]) * h });
    const cellShape = (i, j, cls, extra = {}) => (shape === 'circle'
      ? svg('path', { class: cls, d: sectorPath(ang(j - 1), ang(j)), ...extra })
      : (() => { const b = cellBox(i, j); return svg('rect', { class: cls, x: b.x, y: b.y, width: b.w, height: b.h, ...extra }); })());

    /* Hatch patterns for sets 2 and 3 */
    const defs = svg('defs');
    [2, 3].forEach(k => defs.append(svg('pattern', { id: `cv-hatch-${id}-${k}`, patternUnits: 'userSpaceOnUse', width: 8, height: 8, patternTransform: `rotate(${k === 2 ? 45 : -45})` }, [svg('rect', { class: `cv-hatch-bg cv-k${k}`, width: 8, height: 8 }), svg('line', { class: `cv-hatch-line cv-k${k}`, x1: 0, y1: 0, x2: 0, y2: 8 })])));
    g.append(defs);

    const cellG = svg('g', { class: 'cv-acells' }), shadeG = svg('g', { class: 'cv-shades' }), lineG = svg('g', { class: 'cv-alines' }), inG = svg('g', { class: 'cv-ainner' }), splitG = svg('g', { class: 'cv-split' }), ptG = svg('g', { class: 'cv-apoints' }), labG = svg('g', { class: 'cv-alabels' });
    g.append(cellG, shadeG, lineG, inG, splitG, ptG, labG);
    const cells = new Map();
    let order = [], n = 0, gridKey = '';
    /* Cells and grid lines for rows x cols (a circle: sectors); called again when state.grid re-cuts the shape */
    const build = (r2, c2) => {
      if (shape === 'circle') { sectors = Math.max(1, c2); rows = 1; cols = sectors; } else { rows = Math.max(1, r2); cols = Math.max(1, c2); }
      const same = (list, k) => list && list.length === k;
      cx = sizes(same(P.colSizes, cols) ? P.colSizes : null, cols); cy = sizes(same(P.rowSizes, rows) ? P.rowSizes : null, rows);
      cellG.replaceChildren(); lineG.replaceChildren(); cells.clear();
      for (let i = 1; i <= rows; i++) for (let j = 1; j <= cols; j++) {
        const cid = cellId(i, j);
        const grp = svg('g', { class: 'cv-obj cv-acell', 'data-id': cid, 'data-tap': '', 'data-label': shape === 'circle' ? `Sector ${j} of ${sectors}` : `Row ${i}, column ${j}` }, [cellShape(i, j, 'cv-body')]);
        cellG.append(grp); cells.set(cid, { grp, i, j });
      }
      if (shape === 'circle') {
        if (sectors > 1) for (let j = 0; j < sectors; j++) lineG.append(svg('line', { class: 'cv-gline', x1: ccx, y1: ccy, x2: ccx + R * Math.cos(ang(j)), y2: ccy + R * Math.sin(ang(j)) }));
        lineG.append(svg('circle', { class: 'cv-outline-shape', cx: ccx, cy: ccy, r: R }));
      } else {
        for (let j = 1; j < cols; j++) lineG.append(svg('line', { class: 'cv-gline', x1: ox + cx[j] * w, x2: ox + cx[j] * w, y1: oy, y2: oy + h }));
        for (let i = 1; i < rows; i++) lineG.append(svg('line', { class: 'cv-gline', y1: oy + cy[i] * h, y2: oy + cy[i] * h, x1: ox, x2: ox + w }));
        lineG.append(svg('rect', { class: 'cv-outline-shape', x: ox, y: oy, width: w, height: h, rx: 2 }));
      }
      n = rows * cols; order = [...cells.keys()]; gridKey = `${rows}x${cols}`;
    };
    build(rows, cols);
    /* Edge labels and per-row / per-column labels */
    const lab = (x, y, t, anchor = 'middle') => labG.append(C.label(x, y, t, { tex: 'auto', anchor, w: 160, h: 36 }));
    if (L.top) lab(ox + w / 2, oy - 18, L.top);
    if (L.bottom) lab(ox + w / 2, oy + h + 20, L.bottom);
    if (L.left) lab(ox - 12, oy + h / 2, L.left, 'end');
    if (L.right) lab(ox + w + 12, oy + h / 2, L.right, 'start');
    if (P.colLabels && shape !== 'circle') P.colLabels.forEach((t, j) => lab(ox + (cx[j] + cx[j + 1]) / 2 * w, oy - 16, t));
    if (P.rowLabels && shape !== 'circle') P.rowLabels.forEach((t, i) => lab(ox - 10, oy + (cy[i] + cy[i + 1]) / 2 * h, t, 'end'));

    /* Shading: ids, a fraction (cells in reading order when it lands on whole cells, else a continuous strip or sector),
       { rows: k }, { cols: k } */
    const shapesFor = (spec, frac) => {
      if (Array.isArray(spec)) return spec.filter(x => cells.has(x)).map(x => { const c = cells.get(x); return cellShape(c.i, c.j, 'cv-shade-shape'); });
      if (typeof spec === 'number') {
        const f = Math.max(0, Math.min(1, frac ?? spec));
        if (shape === 'circle') return f > 0 ? [svg('path', { class: 'cv-shade-shape', d: sectorPath(-Math.PI / 2, -Math.PI / 2 + f * 2 * Math.PI) })] : [];
        if (frac == null && Math.abs(f * n - Math.round(f * n)) < 1e-9 && n > 1) return order.slice(0, Math.round(f * n)).map(x => { const c = cells.get(x); return cellShape(c.i, c.j, 'cv-shade-shape'); });
        return [svg('rect', { class: 'cv-shade-shape', x: ox, y: oy, width: w * f, height: h })];
      }
      if (spec && spec.rows != null) return shape === 'circle' ? [] : [svg('rect', { class: 'cv-shade-shape', x: ox, y: oy, width: w, height: cy[Math.min(rows, spec.rows)] * h })];
      if (spec && spec.cols != null) return shape === 'circle' ? [svg('path', { class: 'cv-shade-shape', d: sectorPath(-Math.PI / 2, ang(Math.min(cols, spec.cols))) })] : [svg('rect', { class: 'cv-shade-shape', x: ox, y: oy, width: cx[Math.min(cols, spec.cols)] * w, height: h })];
      return [];
    };
    const isSetMap = (v) => v && typeof v === 'object' && !Array.isArray(v) && v.rows == null && v.cols == null;
    const anim = C.animator();
    let shown = [];
    /* The grid lines again, in each shading's colour and clipped to it, above the plain lines */
    let clipN = 0;
    const innerLines = (layers) => {
      inG.replaceChildren();
      const lines = [...lineG.querySelectorAll('.cv-gline')];
      if (!lines.length) return;
      layers.forEach(grp => {
        const shapes = [...grp.querySelectorAll('.cv-shade-shape')]; if (!shapes.length) return;
        const cid = `cv-aclip-${id}-${++clipN}`;
        const clip = svg('clipPath', { id: cid }, shapes.map(n2 => { const c = n2.cloneNode(); c.removeAttribute('class'); return c; }));
        inG.append(clip, svg('g', { class: 'cv-gline-in ' + [...grp.classList].filter(c => /^cv-k\d$/.test(c)).join(' '), 'clip-path': `url(#${cid})` }, lines.map(l => l.cloneNode())));
      });
    };
    const draw = (st, prev, { instant, ms }) => {
      /* state.grid re-cuts the shape: [rows, cols], or n columns (n sectors on a circle) */
      if (st.grid != null) {
        const gg = [].concat(st.grid), r2 = gg.length > 1 ? +gg[0] : rows, c2 = +(gg.length > 1 ? gg[1] : gg[0]);
        if (`${shape === 'circle' ? 1 : Math.max(1, r2)}x${Math.max(1, c2)}` !== gridKey && c2 > 0) { build(r2, c2); shown = null; }
      }
      const list = st.shade == null ? [] : isSetMap(st.shade) ? Object.values(st.shade) : [st.shade];
      const before = prev && prev.shade != null ? (isSetMap(prev.shade) ? Object.values(prev.shade) : [prev.shade]) : [];
      const layer = (k, spec, frac) => { const grp = svg('g', { class: `cv-shade cv-k${k + 1}` + (k ? ' is-hatched' : '') }); if (k) grp.style.setProperty('--hatch', `url(#cv-hatch-${id}-${Math.min(3, k + 1)})`); shapesFor(spec, frac).forEach(s => grp.append(s)); return grp; };
      const changed = JSON.stringify(list) !== JSON.stringify(shown);
      if (changed) {
        const tweenable = !instant && list.length === before.length && list.every((s, k) => typeof s === 'number' && typeof before[k] === 'number');
        if (tweenable) {
          anim.run(ms, (t) => { shadeG.replaceChildren(...list.map((s, k) => layer(k, s, lerp(before[k], s, t)))); if (t === 1) shadeG.replaceChildren(...list.map((s, k) => layer(k, s))); innerLines([...shadeG.children]); });
        } else {
          anim.stop();
          shadeG.replaceChildren(...list.map((s, k) => layer(k, s)));
          innerLines([...shadeG.children]);
          if (!instant) shadeG.querySelectorAll('.cv-shade').forEach(s => s.animate([{ opacity: 0 }, { opacity: 1 }], { duration: ms, easing: 'cubic-bezier(0.65, 0, 0.35, 1)' }));
        }
        shown = JSON.parse(JSON.stringify(list));
      }
      /* split lines: [rows, cols] dashed; for a circle, [1, n] radii */
      const sp = st.split ? [].concat(st.split) : null, key = JSON.stringify(sp);
      if (splitG.dataset.key !== key) {
        splitG.dataset.key = key; splitG.replaceChildren();
        if (sp) {
          const [r, c] = sp.length === 1 ? [1, sp[0]] : sp;
          if (shape === 'circle') { for (let j = 0; j < c; j++) { const a = -Math.PI / 2 + j / c * 2 * Math.PI; splitG.append(svg('line', { class: 'cv-splitline', x1: ccx, y1: ccy, x2: ccx + R * Math.cos(a), y2: ccy + R * Math.sin(a) })); } }
          else { for (let j = 1; j < c; j++) splitG.append(svg('line', { class: 'cv-splitline', x1: ox + w * j / c, x2: ox + w * j / c, y1: oy, y2: oy + h })); for (let i = 1; i < r; i++) splitG.append(svg('line', { class: 'cv-splitline', y1: oy + h * i / r, y2: oy + h * i / r, x1: ox, x2: ox + w })); }
          if (!instant) splitG.animate([{ opacity: 0 }, { opacity: 1 }], { duration: ms, easing: 'cubic-bezier(0.65, 0, 0.35, 1)' });
        }
      }
      /* points: [x, y] or [[x, y], ...] or [{ id, x, y }] in unit coordinates, y up */
      const raw = st.point == null ? [] : Array.isArray(st.point) && typeof st.point[0] === 'number' ? [st.point] : [].concat(st.point);
      ptG.replaceChildren(...raw.map((p, k) => {
        const q = Array.isArray(p) ? { id: 'pt' + (k + 1), x: p[0], y: p[1] } : { id: p.id || 'pt' + (k + 1), ...p };
        const X = shape === 'circle' ? ccx + q.x * R : ox + q.x * w, Y = shape === 'circle' ? ccy - q.y * R : oy + (1 - q.y) * h;
        return svg('g', { class: 'cv-obj cv-apt' + (q.colour ? ' cv-k' + q.colour : ''), 'data-id': q.id, transform: `translate(${X} ${Y})` }, [svg('circle', { class: 'cv-body', r: 5 })]);
      }));
    };
    const I = C.instance({ kind: 'area', factory: area, params, ctx, fr, draw });
    I.api.cells = () => [...cells.keys()];
    /* Explore controls: re-cut with split or grid (see the header) */
    const curSplit = () => { const sp = I.state().split; if (sp == null) return null; const a = [].concat(sp); return a.length === 1 ? [1, +a[0]] : [+a[0], +a[1]]; };
    const curGrid = () => [rows, cols];
    I.api.setParam = (name, v) => {
      const [base, part] = String(name).split('.');
      if (base === 'shade') { I.api.set({ shade: Math.max(0, Math.min(1, +v)) }, { instant: true }); return; }
      v = Math.max(1, Math.round(+v));
      if (base === 'split') { const sp = curSplit() || [1, 1]; const next = part === 'rows' ? [v, sp[1]] : [sp[0], v]; I.api.set({ split: shape === 'circle' ? [next[1]] : next }, { instant: true }); }
      else if (base === 'grid') { const gr = curGrid(); const next = part === 'rows' ? [v, gr[1]] : [gr[0], v]; I.api.set({ grid: shape === 'circle' ? [next[1]] : next }, { instant: true }); }
    };
    I.api.getParam = (name) => {
      const [base, part] = String(name).split('.');
      const pair = base === 'split' ? curSplit() : base === 'grid' ? curGrid() : null;
      if (base === 'shade') { const sh = I.state().shade; return typeof sh === 'number' ? sh : undefined; }
      return pair ? (part === 'rows' ? pair[0] : pair[1]) : undefined;
    };
    I.api.set({}, { instant: true });
    return I.api;
  }

  C.register('area', area);
})();
