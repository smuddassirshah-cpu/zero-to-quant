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
    const W = 540;
    const mats = (params.matrices || []).map((m, i) => ({ ...m, id: m.id || String.fromCharCode(65 + i) }));
    const ops = params.ops || [];
    const maxRows = Math.max(1, ...mats.map((m) => (m.rows || []).length));
    const cellH = params.cellHeight || 36;
    const H = maxRows * cellH + 64;
    const text = (v) => (v == null ? '' : typeof v === 'number' ? K.fmt(v, 3) : String(v));
    const cellW = (rows) => Math.max(38, ...rows.flat().map((v) => K.tw(text(v).replace(/\$/g, ''), 15) + 18));
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
      size: () => ({ w: W, h: H }),
      skip: ['rows', 'values', 'product', 'rowOp', 'pivot', 'cell', 'hidden'],
      init: () => ({ highlight: [], pivot: null, rowOp: null, cell: null, hidden: [], rows: {}, values: {}, product: null }),
      hlIds: (view) => (Array.isArray(view.highlight) ? view.highlight.map(String) : []),
      animate(prev, next, a, R) {
        if (a.instant) { a.show(next); return; }
        const newProd = next.product && JSON.stringify(next.product) !== JSON.stringify(prev.product);
        const newCell = next.cell && JSON.stringify(next.cell) !== JSON.stringify(prev.cell);
        if (newProd || newCell) return C.tween(0, 1, newProd ? 1100 : 500, (t) => { if (a.alive()) a.show(t >= 1 ? next : { ...next, _p: t }); }, 'standard');
        const from = R.shown;
        return C.tween(0, 1, 500, (t) => { if (a.alive()) a.show(t >= 1 ? next : K.lerp(from, next, t, def.skip)); });
      },
      render(view, R) {
        const g = R.F.g, p = view._p ?? 1;
        const rowsOf = (m) => (view.rows && view.rows[m.id]) || m.rows || [];
        const layout = mats.map((m) => { const rows = rowsOf(m), cw = cellW(rows); return { m, rows, cw, w: (rows[0] || []).length * cw + 20 }; });
        const opW = 36, rowOpW = view.rowOp ? 120 : 0;
        const total = layout.reduce((s, l) => s + l.w, 0) + Math.max(0, layout.length - 1) * opW + rowOpW;
        let x = Math.max(8, (W - total) / 2);
        const top = 18;
        const hiddenSet = new Set([].concat(view.hidden || []));
        const shown = new Set(toIds(view.cell, 'cells').concat(view.product ? [`${view.product.c}-${view.product.i}-${view.product.j}`] : []));
        const emph = toIds(K.isObj(view.highlight) ? view.highlight : null);
        const pivots = new Set(toIds(view.pivot, 'cells'));
        const prod = view.product;
        layout.forEach((L, li) => {
          const { m, rows, cw } = L, nr = rows.length, nc = (rows[0] || []).length;
          const mx = x + 10, my = top + (maxRows - nr) * cellH / 2, mh = nr * cellH;
          const mg = K.obj(m.id, 'cvb-mat'); g.append(mg);
          mg.append(K.washRect(mx - 12, my - 6, nc * cw + 24, mh + 12, 6));
          /* coloured emphasis (object highlight, product row and column) */
          const rowW = (r, op = 1) => mg.append(svg('rect', { x: mx - 2, y: my + r * cellH + 2, width: nc * cw + 4, height: cellH - 4, rx: 5, class: 'cvb-row-w', opacity: op }));
          const colW = (c, op = 1) => mg.append(svg('rect', { x: mx + c * cw + 2, y: my - 2, width: cw - 4, height: mh + 4, rx: 5, class: 'cvb-col-w', opacity: op }));
          emph.forEach((id) => { let q; if ((q = id.match(new RegExp(`^${m.id}-r(\\d+)$`)))) rowW(+q[1]); else if ((q = id.match(new RegExp(`^${m.id}-c(\\d+)$`)))) colW(+q[1]); });
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
            if (isEmph) o.append(svg('rect', { x: mx + c * cw + 3, y: my + r * cellH + 3, width: cw - 6, height: cellH - 6, rx: 5, class: 'cvb-cell-w' }));
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
            if (pivots.has(id)) o.append(svg('circle', { cx, cy, r: Math.min(cw, cellH) / 2 - 2, class: 'cvb-pivot' }));
            R.tappable(o, id, `Row ${r + 1}, column ${c + 1}`);
            mg.append(o);
          }
          /* brackets */
          const bx0 = mx - 4, bx1 = mx + nc * cw + 4, by0 = my - 2, by1 = my + mh + 2;
          mg.append(svg('path', { d: `M${bx0 + 6},${by0}L${bx0},${by0}L${bx0},${by1}L${bx0 + 6},${by1}M${bx1 - 6},${by0}L${bx1},${by0}L${bx1},${by1}L${bx1 - 6},${by1}`, class: 'cvb-bracket' }));
          if (m.label) mg.append(K.lab(mx + nc * cw / 2, H - 16, m.label, { w: 120 }));
          /* row operation arrow on the right of this matrix */
          const ro = view.rowOp;
          if (ro && (ro.m || mats[0].id) === m.id) {
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
            g.append(K.txt(x + opW / 2, top + maxRows * cellH / 2, opT.replace('*', '×').replace('-', '−'), { size: 20 }));
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
