/* matrix: matrices with brackets and operators; row, column and cell highlights; pivots; row operation arrows;
   the product cell animation (a row and a column light up and the result cell fills).
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js). */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  C.register('matrix', (host, params, ctx) => {
    const K = Z.cvb;
    /* item 251: fit: true (the default inside a pair) narrows the frame to the matrices, so a side of a pair is not a
       540-wide drawing shrunk to half; wider later content (a row operation) scales to the frame as before */
    const fitW = params.fit === true;
    let W = 540;
    const mats = (params.matrices || []).map((m, i) => ({ ...m, id: m.id || String.fromCharCode(65 + i) }));
    const ops = params.ops || [];
    const maxRows = Math.max(1, ...mats.map((m) => (m.rows || []).length));
    const cellH = params.cellHeight || 36;
    const H = maxRows * cellH + 64;
    /* item 234: numbers and text that starts as a negative number use the minus sign; item 235: {{expr}} in a cell is
       filled live from params (and state.params, which controls write) */
    const minus = (t) => t.replace(/^-(?=\d|\.\d)/, '−');
    let names = {};
    const text = (v) => (v == null ? '' : typeof v === 'number' ? K.fmt(v, 3) : minus(String(v).includes('{{') ? C.template(String(v), names) : String(v)));
    /* items 247, 252: KaTeX cells are measured as rendered, not guessed from their source */
    const measured = new Map();
    const texW = (t) => {
      if (measured.has(t)) return measured.get(t);
      let w = K.tw(t.replace(/\$|\\[a-zA-Z]+|[{}^_]/g, ''), 15) + 4;
      try {
        if (typeof document !== 'undefined' && document.body) {
          const sp = document.createElement('span'); sp.className = 'cv-fo-in cvb-measure'; sp.style.cssText = 'position:absolute;visibility:hidden;left:-9999px;top:0;display:inline-block;width:auto;height:auto;font-size:15px';
          sp.innerHTML = /^\$[^$]+\$$/.test(t) ? Z.tex(t.slice(1, -1)) : Z.md(t); document.body.append(sp); const r = sp.getBoundingClientRect().width; sp.remove(); if (r > 0) w = r;
        }
      } catch { /* estimate */ }
      measured.set(t, w); return w;
    };
    const t0w = (v) => { const t = text(v); return t.includes('$') ? texW(t) : K.tw(t, 15); };
    const cellW = (rows) => Math.max(38, ...rows.flat().map((v) => { const t = text(v); return (t.includes('$') ? texW(t) : K.tw(t, 15)) + 18; }));
    const toIds = (v, kind) => {
      if (!v) return [];
      if (Array.isArray(v)) return v.map(String);
      const out = [];
      for (const [m, o] of Object.entries(v)) {
        if (Array.isArray(o)) { o.forEach((c) => out.push(Array.isArray(c) ? `${m}-${c[0]}-${c[1]}` : `${m}-${kind === 'cells' ? c : 'r' + c}`)); continue; }
        (o.rows || []).forEach((r) => out.push(`${m}-r${r}`));
        (o.cols || []).forEach((c) => out.push(`${m}-c${c}`));
        (o.cells || []).forEach((c) => out.push(`${m}-${c[0]}-${c[1]}`));
      }
      return out;
    };

    const def = {
      kind: 'matrix', aria: params.aria || 'Matrices',
      modes: ['tap'],
      size: () => { if (!fitW) return { w: W, h: H }; const L = mats.map((m) => { const rows = m.rows || []; return (rows[0] || []).length * cellW(rows) + 20 + (Array.isArray(m.rowLabels) ? 60 : 0) + (m.scale != null ? 50 : 0); }); W = Math.max(160, Math.min(540, Math.ceil(L.reduce((a, b) => a + b, 0) + Math.max(0, L.length - 1) * 36 + 24))); return { w: W, h: H, fit: true }; },
      skip: ['rows', 'values', 'product', 'rowOp', 'pivot', 'cell', 'hidden'],
      init: () => ({ highlight: null, pivot: null, rowOp: null, cell: null, hidden: [], rows: {}, values: {}, product: null }),
      hlIds: (view) => (Array.isArray(view.highlight) ? view.highlight.filter((x) => typeof x !== 'object').map(String) : []),
      /* item 236: the object form ({ "A": { "rows": [1] } }) becomes a list of groups, which a later patch replaces
         whole (a keyed merge into [] used to swallow it); item 242: a matrix may take several groups, each with a colour:
         { "A": [{ "rows": [0], "cols": [0], "colour": 2 }, { "cells": [[1, 1], [1, 2]], "colour": 3 }] } */
      prepare(patch) {
        const h = patch.highlight;
        if (K.isObj(h)) patch.highlight = Object.entries(h).flatMap(([m, o]) => (Array.isArray(o) && o.length && o.every(K.isObj) ? o : [o]).map((g) => (Array.isArray(g) ? { m, list: g } : { m, ...g })));
        return patch;
      },
      animate(prev, next, a, R) {
        if (a.instant) { a.show(next); return; }
        const newProd = next.product && JSON.stringify(next.product) !== JSON.stringify(prev.product);
        const newCell = next.cell && JSON.stringify(next.cell) !== JSON.stringify(prev.cell);
        if (newProd || newCell) return C.tween(0, 1, newProd ? 1100 : 500, (t) => { if (a.alive()) a.show(t >= 1 ? next : { ...next, _p: t }); }, 'standard');
        const from = R.shown;
        return C.tween(0, 1, 500, (t) => { if (a.alive()) a.show(t >= 1 ? next : K.lerp(from, next, t, def.skip)); });
      },
      render(view, R) {
        const g = svg('g'), p = view._p ?? 1; R.F.g.append(g); // drawn into one group, so wide matrices can scale to the column (item 144)
        const rowsOf = (m) => (view.rows && view.rows[m.id]) || m.rows || [];
        /* item 248: rowLabels and colLabels; item 260: a scalar factor before the brackets (scale: "\\tfrac{1}{\\sqrt{2}}") */
        const lw = (m) => (Array.isArray(m.rowLabels) ? Math.max(0, ...m.rowLabels.map((t) => (String(t).includes('$') ? texW(String(t)) : K.tw(String(t), 13)))) + 12 : 0);
        const sw = (m) => (m.scale != null ? (String(m.scale).includes('$') || /\\/.test(String(m.scale)) ? texW(/\$/.test(String(m.scale)) ? String(m.scale) : `$${m.scale}$`) : K.tw(String(m.scale), 16)) + 10 : 0);
        const layout = mats.map((m) => { const rows = rowsOf(m), cw = cellW(rows); return { m, rows, cw, lw: lw(m), sw: sw(m), w: (rows[0] || []).length * cw + 20 + lw(m) + sw(m) }; });
        const opW = 36, rowOpW = view.rowOp ? 120 : 0;
        const total = layout.reduce((s, l) => s + l.w, 0) + Math.max(0, layout.length - 1) * opW + rowOpW;
        let x = Math.max(8, (W - total) / 2);
        const top = 18 + (mats.some((m) => Array.isArray(m.colLabels)) ? 18 : 0);
        if (total > W - 16) { const k = (W - 16) / total; g.setAttribute('transform', `translate(${(8 * (1 - k)).toFixed(2)} ${(top * (1 - k)).toFixed(2)}) scale(${k.toFixed(4)})`); }
        const hiddenSet = new Set([].concat(view.hidden || []));
        const shown = new Set(toIds(view.cell, 'cells').concat(view.product ? [`${view.product.c}-${view.product.i}-${view.product.j}`] : []));
        names = { ...(params.params || {}), ...(view.params || {}) };
        const groups = (Array.isArray(view.highlight) ? view.highlight.filter(K.isObj) : []).map((g) => (g.m ? g : g.id ? { ...g, m: g.id } : g)); // a keyed merge elsewhere may have turned { A: {...} } into [{ id: 'A', ... }]
        const emphOf = (g) => toIds({ [g.m]: g.list || { rows: g.rows, cols: g.cols, cells: g.cells } });
        const emph = groups.flatMap(emphOf), colourOf = new Map(); groups.forEach((g) => emphOf(g).forEach((id) => { if (g.colour != null && !colourOf.has(id)) colourOf.set(id, g.colour); }));
        const pivots = new Set(toIds(view.pivot, 'cells'));
        const prod = view.product;
        layout.forEach((L, li) => {
          const { m, rows, cw } = L, nr = rows.length, nc = (rows[0] || []).length;
          const mx = x + 10 + L.lw + L.sw, my = top + (maxRows - nr) * cellH / 2, mh = nr * cellH;
          const mg = K.obj(m.id, 'cvb-mat'); g.append(mg);
          mg.append(K.washRect(mx - 12, my - 6, nc * cw + 24, mh + 12, 6));
          /* coloured emphasis (object highlight, product row and column) */
          const tint = (cls, id) => (colourOf.has(id) ? cls + ' has-c ' + K.colourCls(colourOf.get(id)) : cls);
          const rowW = (r, op = 1, id) => mg.append(svg('rect', { x: mx - 2, y: my + r * cellH + 2, width: nc * cw + 4, height: cellH - 4, rx: 5, class: tint('cvb-row-w', id), opacity: op }));
          const colW = (c, op = 1, id) => mg.append(svg('rect', { x: mx + c * cw + 2, y: my - 2, width: cw - 4, height: mh + 4, rx: 5, class: tint('cvb-col-w', id), opacity: op }));
          emph.forEach((id) => { let q; if ((q = id.match(new RegExp(`^${m.id}-r(\\d+)$`)))) rowW(+q[1], 1, id); else if ((q = id.match(new RegExp(`^${m.id}-c(\\d+)$`)))) colW(+q[1], 1, id); });
          if (prod && prod.a === m.id) rowW(prod.i, Math.min(1, p * 3));
          if (prod && prod.b === m.id) colW(prod.j, K.clamp((p - 0.25) * 3, 0, 1));
          /* row and column groups for hint highlights */
          for (let r = 0; r < nr; r++) { const o = K.obj(`${m.id}-r${r}`, ''); o.append(K.washRect(mx - 4, my + r * cellH + 1, nc * cw + 8, cellH - 2, 5)); mg.append(o); }
          for (let c = 0; c < nc; c++) { const o = K.obj(`${m.id}-c${c}`, ''); o.append(K.washRect(mx + c * cw + 1, my - 4, cw - 2, mh + 8, 5)); mg.append(o); }
          /* cells */
          for (let r = 0; r < nr; r++) for (let c = 0; c < nc; c++) {
            const id = `${m.id}-${r}-${c}`, cx = mx + c * cw + cw / 2, cy = my + r * cellH + cellH / 2;
            const o = K.obj(id, 'cvb-cell-o', 'ink');
            o.append(K.washRect(mx + c * cw + 3, my + r * cellH + 3, cw - 6, cellH - 6, 5));
            const isEmph = emph.includes(id) || (shown.has(id) && !(prod && id === `${prod.c}-${prod.i}-${prod.j}` && p < 0.6));
            if (isEmph) o.append(svg('rect', { x: mx + c * cw + 3, y: my + r * cellH + 3, width: cw - 6, height: cellH - 6, rx: 5, class: tint('cvb-cell-w', id) }));
            o.append(svg('rect', { x: mx + c * cw + 1, y: my + r * cellH + 1, width: cw - 2, height: cellH - 2, rx: 5, class: 'cvb-cellbox cvb-tapbox cv-body' }));
            const hidden = (hiddenSet.has(m.id) || hiddenSet.has(id)) && !shown.has(id);
            const val = view.values && view.values[id] != null ? view.values[id] : rows[r][c];
            if (hidden) o.append(svg('rect', { x: cx - cw / 2 + 7, y: cy - cellH / 2 + 6, width: cw - 14, height: cellH - 12, rx: 4, class: 'cvb-empty' }));
            else {
              let op = 1;
              if (prod && id === `${prod.c}-${prod.i}-${prod.j}`) op = K.clamp((p - 0.55) / 0.45, 0, 1);
              else if (shown.has(id) && view._p != null && !prod) op = p;
              const t = text(val);
              const el = t.includes('$') ? K.lab(cx, cy, t, { w: cw, h: cellH }) : K.txt(cx, cy, t, { size: 15, weight: isEmph ? 700 : null });
              if (op < 1) el.setAttribute('opacity', op.toFixed(3));
              o.append(el);
            }
            if (pivots.has(id)) o.append(svg('ellipse', { cx, cy, rx: Math.max(cellH / 2 - 2, Math.min(cw / 2 - 3, (t0w(val) + 14) / 2)), ry: cellH / 2 - 2, class: 'cvb-pivot' })); // item 238: grows with a wide entry
            R.tappable(o, id, `Row ${r + 1}, column ${c + 1}`);
            mg.append(o);
          }
          /* brackets */
          const bx0 = mx - 4, bx1 = mx + nc * cw + 4, by0 = my - 2, by1 = my + mh + 2;
          mg.append(svg('path', { d: `M${bx0 + 6},${by0}L${bx0},${by0}L${bx0},${by1}L${bx0 + 6},${by1}M${bx1 - 6},${by0}L${bx1},${by0}L${bx1},${by1}L${bx1 - 6},${by1}`, class: 'cvb-bracket' }));
          /* item 238: an augmented bar before column k */
          if (Number.isInteger(m.bar) && m.bar > 0 && m.bar < nc) mg.append(svg('line', { x1: mx + m.bar * cw, x2: mx + m.bar * cw, y1: by0 + 2, y2: by1 - 2, class: 'cvb-augbar' }));
          if (L.sw) { const st = String(m.scale); mg.append(K.lab(bx0 - 6, my + mh / 2, /\$/.test(st) ? st : /\\/.test(st) ? `$${st}$` : st, { anchor: 'end', size: 16, w: L.sw + 10, h: 40 })); }
          if (Array.isArray(m.rowLabels)) m.rowLabels.slice(0, nr).forEach((t, r) => mg.append(K.lab(bx0 - 6 - L.sw, my + r * cellH + cellH / 2, String(t), { anchor: 'end', size: 13, cls: 'cvb-muted', w: L.lw + 10 })));
          if (Array.isArray(m.colLabels)) m.colLabels.slice(0, nc).forEach((t, c) => mg.append(K.lab(mx + c * cw + cw / 2, my - 14, String(t), { size: 13, cls: 'cvb-muted', w: cw })));
          if (m.label) mg.append(K.lab(mx + nc * cw / 2, H - 16, m.label, { w: 120 }));
          /* row operation arrow on the right of this matrix */
          const ro = view.rowOp;
          const roM = ro && (ro.m || (mats.find((q) => rowsOf(q).length > Math.max(ro.from ?? 0, ro.to ?? 0)) || mats[0]).id); // item 238: the matrix that has those rows
          if (ro && roM === m.id) {
            const ax = bx1 + 12, fy = my + ro.from * cellH + cellH / 2, ty = my + ro.to * cellH + cellH / 2;
            const o = K.obj('rowop', '', 'ink');
            if (ro.from === ro.to) {
              o.append(K.arrow(ax, fy - 9, ax + 2, fy - 2, { cls: 'cvb-ln thin', head: 7 }));
              o.append(svg('path', { d: `M${ax + 2},${fy + 9}C${ax + 22},${fy + 9} ${ax + 22},${fy - 9} ${ax},${fy - 9}`, class: 'cvb-ln thin' }));
            } else {
              const bend = Math.min(40, 14 + Math.abs(ty - fy) / 3);
              const d = `M${ax},${fy}C${ax + bend},${fy} ${ax + bend},${ty} ${ax + 6},${ty}`;
              o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln thin' }), svg('path', { d: `M${ax},${ty}L${ax + 9},${ty - 5}L${ax + 9},${ty + 5}Z`, class: 'cvb-head' }));
              if (ro.swap) o.append(svg('path', { d: `M${ax},${fy}L${ax + 9},${fy - 5}L${ax + 9},${fy + 5}Z`, class: 'cvb-head' }));
            }
            const k = ro.k ?? 1, kt = Math.abs(k) === 1 ? '' : K.fmt(Math.abs(k), 3).replace('−', '');
            const lt = ro.label || (ro.swap ? `$R_{${ro.from + 1}} \\leftrightarrow R_{${ro.to + 1}}$` : ro.from === ro.to ? `$R_{${ro.to + 1}} \\to ${k < 0 ? '-' : ''}${kt}R_{${ro.to + 1}}$` : `$R_{${ro.to + 1}} \\to R_{${ro.to + 1}} ${k < 0 ? '-' : '+'} ${kt}R_{${ro.from + 1}}$`);
            o.append(K.lab(ax + 30, (fy + ty) / 2, lt, { anchor: 'start', w: 120, halo: true }));
            mg.append(o);
          }
          x += L.w;
          if (li < layout.length - 1) {
            const opT = ops[li] || '';
            /* item 264: an operator may be KaTeX ("$\\cdot$", "\\otimes") */
            const isTex = /\$|\\/.test(opT);
            g.append(isTex ? K.lab(x + opW / 2, top + maxRows * cellH / 2, /\$/.test(opT) ? opT : `$${opT}$`, { w: opW + 10, h: 32 }) : K.txt(x + opW / 2, top + maxRows * cellH / 2, opT.replace('*', '×').replace('-', '−'), { size: 20 }));
            x += opW;
          }
        });
      },
      methods: (R) => ({
        /* The result of multiplying named matrices: product('A', 'B') -> rows. */
        product: (a, b) => { const A = (R.state.rows && R.state.rows[a]) || mats.find((m) => m.id === a)?.rows, B = (R.state.rows && R.state.rows[b]) || mats.find((m) => m.id === b)?.rows; if (!A || !B) return null; return A.map((row) => B[0].map((_, j) => row.reduce((s, v, k) => s + v * B[k][j], 0))); },
      }),
    };
    return K.make(host, params, ctx, def);
  });
})();
