/* area canvas: a rectangle, square or circle split into a grid of cells (or sectors), for fraction and multiplication
   area models and geometric probability. Up to three shadings overlay (set 1 solid wash, later sets hatched), so
   2/3 of 3/4 reads as the crossed region. Cell ids c{i}{j}, one-based from the top left (c{i}-{j} when either index
   is 10 or more); a circle's sectors are c1{j} clockwise from twelve o'clock. state.grid re-cuts the shape into a new
   grid (the cells are rebuilt; a fractional shade then lands on the new cells), state.split draws dashed cut lines.
   Explore controls bind to them through setParam: "split" (the number of columns cut, or sectors on a circle),
   "split.rows", "split.cols", "grid" (columns, or sectors), "grid.rows", "grid.cols", and "shade" (a fraction). Grid lines inside shaded cells
   are drawn again over the shading so they stay visible. Text on a piece: labels keyed by cell id, in params.labels
   or state.labels ({ "c11": "3n" }). Signed pieces: a negative entry in colSizes or rowSizes lays out by its size and
   marks the pieces of that strip negative (dashed and hatched: subtracted), so (x + 5)(x - 2) stays on one model.
   state.colLabels / rowLabels / labels (top, bottom, left, right) patch the edge labels. state.move: { from, to } (or a
   list, each with an optional id) slides a copy of the piece from one cell to another (its place is left empty), for
   rearrangements. state.diagonal: { "c11": "/" | "\\" } draws a dashed diagonal; shade ids "c11/ul", "c11/lr",
   "c11/ur", "c11/ll" fill the triangle on that side. Params and state: engine/canvas/README.md. */
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
    const sizes = (list, n) => { const a = (list && list.length === n ? list : Array(n).fill(1)).map(v => Math.abs(+v) || 1); const s = a.reduce((x, y) => x + y, 0); let acc = 0; return [0, ...a.map(v => (acc += v) / s)]; };
    const signOf = (list, k) => (list && +list[k] < 0 ? -1 : 1);
    /* items 127, 130, 191: colSizes and rowSizes may come from state (a patch or a control binding colSizes.0), so a cut
       moves at true proportions */
    let colS = P.colSizes, rowS = P.rowSizes;
    let cx = sizes(colS, cols), cy = sizes(rowS, rows);
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
    defs.append(svg('pattern', { id: `cv-hatch-${id}-neg`, patternUnits: 'userSpaceOnUse', width: 7, height: 7, patternTransform: 'rotate(-45)' }, [svg('line', { class: 'cv-neg-hatch', x1: 0, y1: 0, x2: 0, y2: 7 })]));
    g.append(defs);

    const cellG = svg('g', { class: 'cv-acells' }), shadeG = svg('g', { class: 'cv-shades' }), lineG = svg('g', { class: 'cv-alines' }), inG = svg('g', { class: 'cv-ainner' }), splitG = svg('g', { class: 'cv-split' }), ptG = svg('g', { class: 'cv-apoints' }), labG = svg('g', { class: 'cv-alabels' });
    const cellLabG = svg('g', { class: 'cv-acelllabels' }), coverG = svg('g', { class: 'cv-acover' }), diagG = svg('g', { class: 'cv-split cv-adiag' }), moveG = svg('g', { class: 'cv-amoves' });
    const dimG = svg('g', { class: 'cv-adim' });
    g.append(cellG, shadeG, coverG, dimG, lineG, inG, splitG, diagG, cellLabG, moveG, ptG, labG);
    const movePos = new Map(); // move id -> current top-left, for animating from there
    const cells = new Map();
    let order = [], n = 0, gridKey = '', sizeKey = '';
    /* Cells and grid lines for rows x cols (a circle: sectors); called again when state.grid re-cuts the shape */
    const build = (r2, c2) => {
      if (shape === 'circle') { sectors = Math.max(1, c2); rows = 1; cols = sectors; } else { rows = Math.max(1, r2); cols = Math.max(1, c2); }
      const same = (list, k) => list && list.length === k;
      cx = sizes(same(colS, cols) ? colS : null, cols); cy = sizes(same(rowS, rows) ? rowS : null, rows);
      cellG.replaceChildren(); lineG.replaceChildren(); cells.clear();
      for (let i = 1; i <= rows; i++) for (let j = 1; j <= cols; j++) {
        const cid = cellId(i, j);
        const neg = shape !== 'circle' && signOf(same(colS, cols) && colS, j - 1) * signOf(same(rowS, rows) && rowS, i - 1) < 0;
        const grp = svg('g', { class: 'cv-obj cv-acell' + (neg ? ' is-neg' : ''), 'data-id': cid, 'data-tap': '', 'data-label': (shape === 'circle' ? `Sector ${j} of ${sectors}` : `Row ${i}, column ${j}`) + (neg ? ', subtracted' : '') }, [cellShape(i, j, 'cv-body')]);
        cellG.append(grp); cells.set(cid, { grp, i, j });
      }
      if (shape === 'circle') {
        if (sectors > 1) for (let j = 0; j < sectors; j++) lineG.append(svg('line', { class: 'cv-gline', x1: ccx, y1: ccy, x2: ccx + R * Math.cos(ang(j)), y2: ccy + R * Math.sin(ang(j)) }));
        lineG.append(svg('circle', { class: 'cv-outline-shape', cx: ccx, cy: ccy, r: R }));
      } else {
        for (let j = 1; j < cols; j++) lineG.append(svg('line', { class: 'cv-gline', x1: ox + cx[j] * w, x2: ox + cx[j] * w, y1: oy, y2: oy + h }));
        for (let i = 1; i < rows; i++) lineG.append(svg('line', { class: 'cv-gline', y1: oy + cy[i] * h, y2: oy + cy[i] * h, x1: ox, x2: ox + w }));
        lineG.append(svg('rect', { class: 'cv-outline-shape', x: ox, y: oy, width: w, height: h, rx: 2 }));
        /* subtracted pieces: hatched over any shading, with a dashed edge */
        for (const c of cells.values()) if (c.grp.classList.contains('is-neg')) { const b = cellBox(c.i, c.j); lineG.append(svg('rect', { class: 'cv-negpiece', x: b.x + 1, y: b.y + 1, width: Math.max(0, b.w - 2), height: Math.max(0, b.h - 2), fill: `url(#cv-hatch-${id}-neg)` })); }
      }
      n = rows * cols; order = [...cells.keys()]; gridKey = `${rows}x${cols}`; sizeKey = JSON.stringify([cx, cy]);
    };
    build(rows, cols);
    /* Edge labels and per-row / per-column labels: from params, patchable through state (colLabels, rowLabels, labels) */
    const lab = (x, y, t, anchor = 'middle') => labG.append(C.label(x, y, t, { tex: 'auto', anchor, w: 160, h: 36 }));
    const drawEdges = (st) => {
      const E = { ...L, ...Object.fromEntries(Object.entries(st.labels || {}).filter(([k]) => ['top', 'bottom', 'left', 'right'].includes(k))) };
      const colL = st.colLabels || P.colLabels, rowL = st.rowLabels || P.rowLabels;
      const key = JSON.stringify([E.top, E.bottom, E.left, E.right, colL, rowL, gridKey, sizeKey]);
      if (labG.dataset.key === key) return;
      labG.dataset.key = key; labG.replaceChildren();
      if (E.top) lab(ox + w / 2, oy - 18, E.top);
      if (E.bottom) lab(ox + w / 2, oy + h + 20, E.bottom);
      if (E.left) lab(ox - 12, oy + h / 2, E.left, 'end');
      if (E.right) lab(ox + w + 12, oy + h / 2, E.right, 'start');
      if (colL && shape !== 'circle') colL.slice(0, cols).forEach((t, j) => lab(ox + (cx[j] + cx[j + 1]) / 2 * w, oy - 16, t));
      if (rowL && shape !== 'circle') rowL.slice(0, rows).forEach((t, i) => lab(ox - 10, oy + (cy[i] + cy[i + 1]) / 2 * h, t, 'end'));
    };

    /* Shading: ids, a fraction (cells in reading order when it lands on whole cells, else a continuous strip or sector),
       { rows: k }, { cols: k } */
    const shapesFor = (spec, frac) => {
      if (Array.isArray(spec)) return spec.map(String).filter(x => cells.has(x) || (shape !== 'circle' && cells.has(x.split('/')[0]))).map(x => {
        const [cid, half] = x.split('/'), c = cells.get(cid);
        if (!half) return cellShape(c.i, c.j, 'cv-shade-shape');
        const b = cellBox(c.i, c.j), TL = [b.x, b.y], TR = [b.x + b.w, b.y], BL = [b.x, b.y + b.h], BR = [b.x + b.w, b.y + b.h];
        const tri = { ul: [TL, TR, BL], lr: [TR, BR, BL], ur: [TL, TR, BR], ll: [TL, BR, BL] }[half] || [TL, TR, BR, BL];
        return svg('path', { class: 'cv-shade-shape', d: 'M' + tri.map(p => p.join(' ')).join('L') + 'Z' });
      });
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
      const cs = st.colSizes || P.colSizes, rs = st.rowSizes || P.rowSizes;
      if (JSON.stringify([cs, rs]) !== JSON.stringify([colS, rowS])) { colS = cs; rowS = rs; build(rows, cols); shown = null; }
      /* item 189: dim: [ids] fades pieces (a dropped row, the part not counted) */
      const dimSet = new Set([].concat(st.dim || []).map(String));
      dimG.replaceChildren(...[...dimSet].filter(cid => cells.has(cid)).map(cid => { const c = cells.get(cid); return cellShape(c.i, c.j, 'cv-dim-shape'); }));
      cells.forEach((c, cid) => c.grp.classList.toggle('is-out', dimSet.has(cid)));
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
      drawEdges(st);
      /* diagonals: { c11: "/" } runs bottom left to top right, "\\" top left to bottom right */
      const dg = st.diagonal || {}, dk = JSON.stringify(dg) + gridKey;
      if (diagG.dataset.key !== dk) {
        diagG.dataset.key = dk;
        diagG.replaceChildren(...Object.entries(dg).filter(([cid]) => cells.has(cid) && shape !== 'circle').map(([cid, dir]) => { const c = cells.get(cid), b = cellBox(c.i, c.j); return dir === '/' ? svg('line', { class: 'cv-splitline', x1: b.x, y1: b.y + b.h, x2: b.x + b.w, y2: b.y }) : svg('line', { class: 'cv-splitline', x1: b.x, y1: b.y, x2: b.x + b.w, y2: b.y + b.h }); }));
      }
      /* moving pieces: a copy of the from piece (its first shading's colour and its text) slides to the to cell */
      const mv = st.move == null ? [] : [].concat(st.move).filter(m => m && cells.has(m.from) && cells.has(m.to) && shape !== 'circle');
      const shadeOf = (cid) => { const k = list.findIndex(sp => Array.isArray(sp) && sp.map(String).includes(cid)); return k >= 0 ? k + 1 : 0; };
      const textOf = (cid) => (st.labels && st.labels[cid]) ?? L[cid];
      coverG.replaceChildren(...mv.map(m => { const c = cells.get(m.from); return cellShape(c.i, c.j, 'cv-cover'); }));
      const keep = new Set();
      mv.forEach((m, k) => {
        const mid = m.id || 'move' + (k + 1); keep.add(mid);
        const fc = cells.get(m.from), tc = cells.get(m.to), fb = cellBox(fc.i, fc.j), tb = cellBox(tc.i, tc.j);
        let grpEl = moveG.querySelector(`[data-id="${CSS.escape(mid)}"]`);
        const slot = m.colour || shadeOf(m.from) || 1;
        if (!grpEl || grpEl.dataset.from !== m.from) {
          grpEl = svg('g', { class: `cv-obj cv-apiece cv-k${slot}`, 'data-id': mid, 'data-from': m.from }, [svg('rect', { class: 'cv-body', x: 0, y: 0, width: fb.w, height: fb.h })]);
          const t = textOf(m.from); if (t) grpEl.append(C.label(fb.w / 2, fb.h / 2, t, { tex: 'auto', cls: 'cv-halo cv-alabel', w: 90, h: 30 }));
          moveG.querySelector(`[data-id="${CSS.escape(mid)}"]`)?.remove(); moveG.append(grpEl); movePos.set(mid, [fb.x, fb.y]);
        }
        const [x0, y0] = movePos.get(mid) || [fb.x, fb.y], x1 = tb.x, y1 = tb.y;
        movePos.set(mid, [x1, y1]);
        if (instant || (x0 === x1 && y0 === y1)) grpEl.setAttribute('transform', `translate(${x1} ${y1})`);
        else { const el = grpEl; C.animator().run(Math.max(ms, 700), (t) => el.setAttribute('transform', `translate(${lerp(x0, x1, t)} ${lerp(y0, y1, t)})`)); }
      });
      moveG.querySelectorAll('.cv-apiece').forEach(n => { if (!keep.has(n.dataset.id)) { n.remove(); movePos.delete(n.dataset.id); } });
      /* text on a piece: params.labels and state.labels keyed by cell id ({ "c11": "3n" }); the state wins */
      const movedFrom = new Set(mv.map(m => m.from));
      const pieceText = Object.assign({}, ...[L, st.labels || {}].map(m => Object.fromEntries(Object.entries(m || {}).filter(([k]) => (cells.has(k) || spanOf(k)) && !movedFrom.has(k)))));
      const ptKey = JSON.stringify(pieceText) + gridKey + sizeKey + [...movedFrom].join();
      if (cellLabG.dataset.key !== ptKey) {
        cellLabG.dataset.key = ptKey;
        cellLabG.replaceChildren(...Object.entries(pieceText).filter(([, t]) => t != null && t !== '').map(([cid, t]) => {
          const c = cells.get(cid), sp = c ? null : spanOf(cid);
          let x, y;
          if (sp) { x = sp.x + sp.w / 2; y = sp.y + sp.h / 2; }
          else if (shape === 'circle') { const a = (ang(c.j - 1) + ang(c.j)) / 2; x = ccx + R * 0.62 * Math.cos(a); y = ccy + R * 0.62 * Math.sin(a); }
          else { const b = cellBox(c.i, c.j); x = b.x + b.w / 2; y = b.y + b.h / 2; }
          return C.label(x, y, t, { tex: 'auto', cls: 'cv-halo cv-alabel', w: 90, h: 30 });
        }));
      }
      /* points: [x, y] or [[x, y], ...] or [{ id, x, y }] in unit coordinates, y up */
      const raw = st.point == null ? [] : Array.isArray(st.point) && typeof st.point[0] === 'number' ? [st.point] : [].concat(st.point);
      ptG.replaceChildren(...raw.map((p, k) => {
        const q = Array.isArray(p) ? { id: 'pt' + (k + 1), x: p[0], y: p[1] } : { id: p.id || 'pt' + (k + 1), ...p };
        const X = shape === 'circle' ? ccx + q.x * R : ox + q.x * w, Y = shape === 'circle' ? ccy - q.y * R : oy + (1 - q.y) * h;
        return svg('g', { class: 'cv-obj cv-apt' + (q.colour ? ' cv-k' + q.colour : ''), 'data-id': q.id, transform: `translate(${X} ${Y})` }, [svg('circle', { class: 'cv-body', r: 5 })]);
      }));
    };
    /* item 130: a label keyed "c11-c16" spans the rectangle from the first cell to the second */
    function spanOf(key) {
      if (shape === 'circle') return null;
      const m = String(key).match(/^(c\d+(?:-\d+)?)-(c\d+(?:-\d+)?)$/); if (!m || !cells.has(m[1]) || !cells.has(m[2])) return null;
      const a = cells.get(m[1]), b = cells.get(m[2]), i0 = Math.min(a.i, b.i), i1 = Math.max(a.i, b.i), j0 = Math.min(a.j, b.j), j1 = Math.max(a.j, b.j);
      const p = cellBox(i0, j0), q = cellBox(i1, j1); return { x: p.x, y: p.y, w: q.x + q.w - p.x, h: q.y + q.h - p.y };
    }
    const I = C.instance({ kind: 'area', factory: area, params, ctx, fr, draw });
    I.api.cells = () => [...cells.keys()];
    /* Explore controls: re-cut with split or grid (see the header) */
    const curSplit = () => { const sp = I.state().split; if (sp == null) return null; const a = [].concat(sp); return a.length === 1 ? [1, +a[0]] : [+a[0], +a[1]]; };
    const curGrid = () => [rows, cols];
    I.api.setParam = (name, v) => {
      const [base, part] = String(name).split('.');
      if ((base === 'colSizes' || base === 'rowSizes') && part != null) { // one entry, keeping its sign
        const list = (I.state()[base] || P[base] || Array(base === 'colSizes' ? cols : rows).fill(1)).slice(), k = +part;
        if (k >= 0 && k < list.length) { list[k] = (+list[k] < 0 ? -1 : 1) * Math.max(0.01, Math.abs(+v)); I.api.set({ [base]: list }, { instant: true }); }
        return;
      }
      if (base === 'shade') { I.api.set({ shade: Math.max(0, Math.min(1, +v)) }, { instant: true }); return; }
      v = Math.max(1, Math.round(+v));
      if (base === 'split') { const sp = curSplit() || [1, 1]; const next = part === 'rows' ? [v, sp[1]] : [sp[0], v]; I.api.set({ split: shape === 'circle' ? [next[1]] : next }, { instant: true }); }
      else if (base === 'grid') { const gr = curGrid(); const next = part === 'rows' ? [v, gr[1]] : [gr[0], v]; I.api.set({ grid: shape === 'circle' ? [next[1]] : next }, { instant: true }); }
    };
    { /* item 134: any other name is a free parameter in state.params, for a derive block to read */
      const own = I.api.setParam;
      I.api.setParam = (name, v) => (['shade', 'split', 'grid', 'colSizes', 'rowSizes'].includes(String(name).split('.')[0]) ? own(name, v) : I.api.set({ params: { [name]: +v } }, { instant: true }));
    }
    I.api.getParam = (name) => {
      const [base, part] = String(name).split('.');
      const pair = base === 'split' ? curSplit() : base === 'grid' ? curGrid() : null;
      if (base === 'shade') { const sh = I.state().shade; return typeof sh === 'number' ? sh : undefined; }
      if ((base === 'colSizes' || base === 'rowSizes') && part != null) { const list = I.state()[base] || P[base]; return list ? Math.abs(+list[+part]) : undefined; }
      return pair ? (part === 'rows' ? pair[0] : pair[1]) : (I.state().params || {})[name];
    };
    I.api.set({}, { instant: true });
    return I.api;
  }

  C.register('area', area);
})();
