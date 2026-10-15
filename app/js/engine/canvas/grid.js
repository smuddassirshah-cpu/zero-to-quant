/* grid canvas: an n by m cell grid for sample spaces, two-dice tables, area models and Punnett squares.
   Reproduces the prototype's DiceGrid: dashed union outlines in the gutters, the fading "point" box, the show-why flash.
   Ids: r{i}c{j}, one-based (r5c1 is row 5, column 1). Names usable wherever ids are listed: row5, col3, cross5,
   cross5-3 (row 5 and column 3), all. Params, state and events are documented in engine/canvas/README.md. */
(function () {
  'use strict';
  const Z = window.ZQ, C = Z.canvas, { svg, attrs } = C;

  function grid(host, params, ctx = {}) {
    const P = params || {};
    const rows = Math.max(1, P.rows || 6), cols = Math.max(1, P.cols || 6), compact = !!P.compact;
    const range = (n) => Array.from({ length: n }, (_, i) => i + 1);
    const rowHeads = P.rowHeads === false ? null : (P.rowHeads || range(rows)).map(String);
    const colHeads = P.colHeads === false ? null : (P.colHeads || range(cols)).map(String);
    const rh = (i) => (rowHeads ? rowHeads[i - 1] : String(i)), ch = (j) => (colHeads ? colHeads[j - 1] : String(j));
    const num = (s) => { const v = parseFloat(s); return Number.isFinite(v) ? v : 0; };
    const cellText = (i, j) => {
      const c = P.cells;
      if (Array.isArray(c)) { const row = c[i - 1] || []; return row[j - 1] == null ? '' : String(row[j - 1]); }
      if (c === 'pair') return `${rh(i)}, ${ch(j)}`;
      if (c === 'sum') return C.fmtNum(num(rh(i)) + num(ch(j)));
      if (c === 'product') return C.fmtNum(num(rh(i)) * num(ch(j)));
      if (c === 'diff') return C.fmtNum(Math.abs(num(rh(i)) - num(ch(j))));
      if (c === 'max') return C.fmtNum(Math.max(num(rh(i)), num(ch(j))));
      if (c === 'min') return C.fmtNum(Math.min(num(rh(i)), num(ch(j))));
      return '';
    };

    /* Geometry: square cells, prototype proportions (420px wide, 344px compact, 6px gutters). */
    const gap = compact ? 5 : 6, m = gap / 2 + 3;
    const labelW = P.rowLabel ? 20 : 0, labelH = P.colLabel ? 22 : 0;
    const headW = rowHeads ? Math.max(20, Math.ceil(Math.max(...rowHeads.map(t => C.textW(t, 14, 700)))) + 8) : 0;
    const headH = colHeads ? 24 : 0;
    const target = Math.min(540, (compact ? 344 : 420) + Math.max(0, cols - 6) * 48);
    const s = Math.max(24, Math.min(compact ? 56 : 72, Math.floor((target - 2 * m - labelW - headW - (cols - 1) * gap) / cols)));
    const x0 = m + labelW + headW, y0 = m + labelH + headH, pitch = s + gap;
    const W = x0 + cols * s + (cols - 1) * gap + m, H = y0 + rows * s + (rows - 1) * gap + m;
    const cx = (j) => x0 + (j - 1) * pitch, cy = (i) => y0 + (i - 1) * pitch;
    const X = (c) => x0 + c * pitch - gap / 2, Y = (r) => y0 + r * pitch - gap / 2; // lattice lines in the gutters

    const fr = C.frame(host, W, H, { cls: compact ? 'is-compact' : '', label: P.label || `Grid of ${rows} by ${cols} outcomes`, fit: true });
    const g = fr.g;
    if (P.text === 'marked') fr.wrap.classList.add('text-marked');

    /* Labels and heads */
    if (P.colLabel) g.append(C.label(x0 + (cols * s + (cols - 1) * gap) / 2, m + 9, P.colLabel, { cls: 'cv-muted cv-axis-label' }));
    if (P.rowLabel) { const ty = y0 + (rows * s + (rows - 1) * gap) / 2; const t = C.label(m + 8, ty, P.rowLabel, { cls: 'cv-muted cv-axis-label' }); t.setAttribute('transform', `rotate(-90 ${m + 8} ${ty})`); g.append(t); }
    if (colHeads) colHeads.forEach((t, k) => g.append(C.label(cx(k + 1) + s / 2, y0 - headH / 2 - 1, t, { cls: 'cv-head', size: 14 })));
    if (rowHeads) rowHeads.forEach((t, k) => g.append(C.label(x0 - headW / 2 - 2, cy(k + 1) + s / 2, t, { cls: 'cv-head', size: 14 })));

    /* Cells */
    const cellsG = svg('g', { class: 'cv-cells' }); g.append(cellsG);
    const cell = new Map();
    const fs = s >= 64 ? 14 : s >= 40 ? 12 : 11;
    for (let i = 1; i <= rows; i++) for (let j = 1; j <= cols; j++) {
      const id = `r${i}c${j}`, txt = cellText(i, j);
      const lab = `${P.rowLabel || 'Row'} ${rh(i)}, ${(P.colLabel || 'Column').toLowerCase()} ${ch(j)}${txt && P.cells !== 'pair' ? ': ' + txt : ''}`;
      const n = svg('g', { class: 'cv-obj cv-cell', 'data-id': id, 'data-tap': '', 'data-label': lab, 'data-r': i, 'data-c': j }, [
        svg('rect', { class: 'cv-body', x: cx(j) + 1, y: cy(i) + 1, width: s - 2, height: s - 2, rx: compact ? 5 : 6 }),
        svg('rect', { class: 'cv-ring', x: cx(j) + 4, y: cy(i) + 4, width: s - 8, height: s - 8, rx: 3 }),
        txt ? C.label(cx(j) + s / 2, cy(i) + s / 2 + 0.5, txt, { cls: 'cv-ctext', size: fs }) : null,
      ]);
      cellsG.append(n); cell.set(id, n);
    }
    const outline = svg('path', { class: 'cv-outline', d: '' });
    const hlLayer = svg('g', { class: 'cv-hl-layer' }), ptLayer = svg('g', { class: 'cv-pt-layer' }), markLayer = svg('g', { class: 'cv-mark-layer' });
    g.append(outline, hlLayer, ptLayer, markLayer);

    /* Id lists accept names: row5, col3, cross5, cross5-3, all */
    const expand = (list) => [].concat(list || []).flatMap((id) => {
      const k = String(id); let mm;
      if (k === 'all') return [...cell.keys()];
      if ((mm = k.match(/^row(\d+)$/))) return range(cols).map(j => `r${mm[1]}c${j}`);
      if ((mm = k.match(/^col(\d+)$/))) return range(rows).map(i => `r${i}c${mm[1]}`);
      if ((mm = k.match(/^cross(\d+)(?:-(\d+))?$/))) { const r = +mm[1], c = +(mm[2] || mm[1]); return [...new Set([...range(cols).map(j => `r${r}c${j}`), ...range(rows).map(i => `r${i}c${c}`)])]; }
      return [k];
    }).filter(id => cell.has(id));
    const rc = (id) => { const n = cell.get(id); return [+n.dataset.r, +n.dataset.c]; };
    const pathFor = (ids) => C.cellOutline(expand(ids).map(id => { const [i, j] = rc(id); return [i - 1, j - 1]; }), X, Y);
    const boxFor = (ids) => {
      const list = expand(ids).map(rc); if (!list.length) return null;
      const r0 = Math.min(...list.map(p => p[0])), r1 = Math.max(...list.map(p => p[0])), c0 = Math.min(...list.map(p => p[1])), c1 = Math.max(...list.map(p => p[1]));
      return { x: X(c0 - 1), y: Y(r0 - 1), w: X(c1) - X(c0 - 1), h: Y(r1) - Y(r0 - 1) };
    };

    let outlineKey = null, dimSet = new Set(), delays = 0;
    const draw = (st, prev, { instant, patch }) => {
      /* shade: { setName: [ids] } or [ids]; slots in order, a second set shows as an inner ring */
      const sets = Array.isArray(st.shade) ? [st.shade] : Object.values(st.shade || {});
      const first = new Map(), second = new Map();
      sets.forEach((ids, k) => expand(ids).forEach(id => { if (!first.has(id)) first.set(id, k + 1); else if (!second.has(id)) second.set(id, k + 1); }));
      cell.forEach((n, id) => {
        for (let k = 1; k <= 6; k++) n.classList.toggle('cv-sh' + k, first.get(id) === k), n.classList.toggle('cv-rg' + k, second.get(id) === k);
        n.classList.toggle('is-shaded', first.has(id));
      });
      /* dim: cells fade one row after another, as in the prototype's shrink */
      const nextDim = new Set(expand(st.dim));
      clearTimeout(delays);
      cell.forEach((n, id) => {
        const on = nextDim.has(id);
        if (on !== dimSet.has(id) && !instant) { const [i, j] = rc(id); n.style.transitionDelay = `${(i - 1) * 50 + (j - 1) * 12}ms`; }
        n.classList.toggle('is-out', on);
      });
      const grew = [...nextDim].some(id => !dimSet.has(id));
      dimSet = nextDim;
      if (!instant) delays = setTimeout(() => cell.forEach(n => { n.style.transitionDelay = ''; }), 1000);
      /* outline: "row5" | "col3" | "cross5" | [ids] | null, dashed in the gutters as one path */
      const key = JSON.stringify(st.outline || null);
      if (key !== outlineKey) {
        outlineKey = key;
        const d = st.outline ? pathFor(st.outline) : '';
        if (instant) { attrs(outline, { d }); outline.classList.toggle('on', !!d); }
        else {
          outline.classList.remove('on');
          I.later(() => { attrs(outline, { d }); outline.classList.toggle('on', !!d); }, grew && 'dim' in patch ? 520 : outline.getAttribute('d') ? 160 : 0);
        }
      }
      /* mark: { id: "✓" | { text, tone } } glyph badges */
      markLayer.replaceChildren();
      for (const [id, v] of Object.entries(st.mark || {})) {
        if (!cell.has(id)) continue;
        const t = typeof v === 'object' && v ? v : { text: String(v) }, [i, j] = rc(id);
        const w = Math.max(18, C.textW(t.text, 11, 800) + 10), x = cx(j) + s - 2, y = cy(i) + 2;
        markLayer.append(svg('g', { class: 'cv-mark' + (t.tone ? ' tone-' + t.tone : '') + (instant ? '' : ' pop'), 'data-for': id }, [
          svg('rect', { x: x - w / 2, y: y - 9, width: w, height: 18, rx: 9 }), C.label(x, y + 0.5, t.text, { size: 11, cls: 'cv-mark-t' }),
        ]));
      }
      if ('point' in patch) point(st.point);
    };

    /* point: the prototype's hint box around the cells' bounding box; pulses twice and fades after 3.2s */
    const point = (ids) => {
      ptLayer.replaceChildren();
      const b = boxFor(ids); if (!b) return;
      const grp = svg('g', { class: 'cv-point' }, [
        svg('rect', { class: 'cv-point-ring', x: b.x, y: b.y, width: b.w, height: b.h, rx: 8 }),
        svg('rect', { class: 'cv-point-box', x: b.x, y: b.y, width: b.w, height: b.h, rx: 8 }),
      ]);
      ptLayer.append(grp);
      if (I.isStatic) return;
      I.later(() => { grp.classList.add('out'); I.later(() => grp.remove(), 320); }, 3200);
    };
    /* highlight: the union of the cells as one washed shape with an ink ring that pulses twice */
    const hl = new Map();
    const onHighlight = (ids, on, { instant }) => {
      if (!on) {
        if (!ids || !ids.length) { hlLayer.replaceChildren(); hl.clear(); }
        else { const k = JSON.stringify(expand(ids)); hl.get(k)?.remove(); hl.delete(k); }
        return true;
      }
      const list = expand(ids); if (!list.length) return true;
      const k = JSON.stringify(list); hl.get(k)?.remove();
      const d = pathFor(list);
      const p = svg('g', { class: 'cv-hlshape' + (instant || I.isStatic || Z.reducedMotion() ? '' : ' pulse') }, [svg('path', { class: 'cv-hl-ring', d }), svg('path', { class: 'cv-hl-main', d })]);
      hlLayer.append(p); hl.set(k, p);
      return true;
    };

    const I = C.instance({ kind: 'grid', factory: grid, params, ctx, fr, draw, onHighlight, defaults: {} });
    const api = I.api;
    api.flash = (ids, opts) => C.flash(expand(ids).map(id => cell.get(id)), opts);
    api.point = (ids) => point(ids);
    api.peek = (ms = 1000) => { if (Z.reducedMotion()) return; fr.wrap.classList.add('is-peek'); I.later(() => fr.wrap.classList.remove('is-peek'), ms); };
    api.cell = (id) => cell.get(id);
    api.ids = () => [...cell.keys()];
    api.expand = expand;
    api.set({}, { instant: true });
    return api;
  }

  C.register('grid', grid);
})();
