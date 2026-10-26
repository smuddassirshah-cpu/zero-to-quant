/* array: cells with index labels and pointer arrows; ranges; animated swaps; stack, queue and linked list modes;
   tap on cells and drag to reorder.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js).
   Pass 7: pointers are tap targets (item 384); the layout follows the current number of cells and their widest text
   (items 387, 397; params.cellWidth fixes it); state.insert { at, value } and state.remove (an index) shift the cells
   along, animated (item 393); a cell may be { v, label } with a small label above its value (item 405); params.steps
   (a list of state patches) with a control bound to "step" is a built-in stepper with a step counter (item 387). */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  C.register('array', (host, params, ctx) => {
    const K = Z.cvb;
    const W = 540, mode = params.mode || 'array', from = params.indexFrom ?? 0;
    const n0 = (params.cells || []).length;
    const cap = Math.max(n0, params.capacity || 0, 1);
    const linked = mode === 'linked', stack = mode === 'stack';
    const valOf = (v) => (v && typeof v === 'object' && !Array.isArray(v) ? (v.v ?? v.value) : v);
    const text0 = (v) => { v = valOf(v); return v == null ? '' : typeof v === 'number' ? K.fmt(v, 3) : String(v); };
    /* item 119: cells widen to their text (dates, 102.50) as far as the column allows */
    const wOf = (list) => Math.max(0, ...(list || []).map((v) => K.tw(text0(v).replace(/\$/g, ''), 13) + 24));
    const widest0 = Math.max(wOf(params.cells), ...(Array.isArray(params.steps) ? params.steps.map((q) => wOf(q && q.cells)) : [0]));
    /* item 313: wrap (a number of cells per row, or true for as many as fit at 34px) puts a long array on several rows */
    let perRow, rowsN, cw;
    const lay = (n, list) => {
      const capN = Math.max(n, params.capacity || 0, n0, 1), widest = params.cellWidth ? +params.cellWidth : Math.max(widest0, wOf(list));
      perRow = !linked && !stack && params.wrap ? Math.max(1, params.wrap === true ? Math.floor((W - 40) / Math.max(34, Math.min(52, widest || 34))) : Math.round(+params.wrap) || capN) : capN;
      rowsN = Math.ceil(capN / perRow);
      cw = params.cellWidth ? +params.cellWidth : linked ? Math.min(Math.max(58, widest), (W - 60) / capN - 26) : Math.min(Math.max(52, widest), Math.max(rowsN > 1 ? 34 : 30, (W - 40) / Math.min(capN, perRow)));
    };
    lay(n0, params.cells);
    const ch = 44, rowPitch = ch + 40;
    const H = params.height || (stack ? Math.max(200, cap * ch + 80) : 150 + (rowsN - 1) * rowPitch);
    const text = text0;
    let pendingSwap = null, dragView = null, pendingIns = null;

    const geom = (n) => {
      if (stack) { const x = W / 2 - cw / 2 - 20, yb = H - 34; return { pos: (k) => [x, yb - (k + 1) * ch], n }; }
      const gap = linked ? 26 : 0, m = Math.min(n, perRow), total = m * cw + Math.max(0, m - 1) * gap + (linked ? 40 : 0);
      const x0 = Math.max(10, (W - total) / 2), y = params.pointersBelow ? 30 : 58;
      return { pos: (k) => [x0 + (k % perRow) * (cw + gap), y + Math.floor(k / perRow) * rowPitch], n, gap };
    };

    const def = {
      kind: 'array', aria: params.aria || (stack ? 'Stack' : mode === 'queue' ? 'Queue' : linked ? 'Linked list' : 'Array'),
      modes: ['tap', 'drag'],
      size: () => ({ w: W, h: H }),
      skip: ['cells', 'pointers'],
      listKeys: ['pointers'],
      init: () => ({ cells: (params.cells || []).slice(), pointers: [], highlight: [], selected: [], active: null, done: [] }),
      hlIds: (view) => (Array.isArray(view.highlight) ? view.highlight.map(String) : K.isObj(view.highlight) ? (view.highlight.ids || []).map(String) : []),
      prepare(patch, state) {
        /* item 387: step k applies params.steps[k] (a state patch) over the opening state */
        if (patch.step != null && Array.isArray(params.steps) && params.steps.length) { const k = Math.max(0, Math.min(params.steps.length - 1, Math.round(+patch.step))); Object.assign(patch, { cells: (params.cells || []).slice(), pointers: [], highlight: [], active: null, done: [], ...params.steps[k], step: k }); if (params.stepCounter !== false && !('caption' in params.steps[k])) patch.caption = `Step ${k + 1} of ${params.steps.length}`; }
        /* item 393: insert { at, value } shifts the later cells right; remove (an index) closes the gap */
        if (patch.insert && typeof patch.insert === 'object') { const at = Math.round(+patch.insert.at - from), c = (patch.cells || state.cells).slice(); c.splice(Math.max(0, Math.min(c.length, at)), 0, patch.insert.value); patch.cells = c; pendingIns = { at, kind: 'in' }; delete patch.insert; }
        else if (patch.remove != null && Number.isFinite(+patch.remove)) { const at = Math.round(+patch.remove - from), c = (patch.cells || state.cells).slice(); if (at >= 0 && at < c.length) { c.splice(at, 1); patch.cells = c; pendingIns = { at, kind: 'out', before: state.cells.slice() }; } delete patch.remove; }
        if (Array.isArray(patch.swap)) {
          const [i, j] = patch.swap.map((v) => v - from);
          if (!patch.cells) { const c = state.cells.slice(); [c[i], c[j]] = [c[j], c[i]]; patch.cells = c; }
          pendingSwap = { i, j, before: state.cells.slice() };
          delete patch.swap;
        }
        return patch;
      },
      animate(prev, next, a, R) {
        const sw = pendingSwap; pendingSwap = null;
        const ins = pendingIns; pendingIns = null;
        if (a.instant) { a.show(next); return; }
        if (ins) return C.tween(0, 1, 560, (t) => { if (a.alive()) a.show(t >= 1 ? next : { ...next, _ins: { ...ins, t } }); });
        if (sw) return C.tween(0, 1, 640, (t) => { if (a.alive()) a.show(t >= 1 ? next : { ...next, cells: sw.before, _swap: { ...sw, t } }); });
        const start = R.shown;
        return C.tween(0, 1, 480, (t) => { if (a.alive()) a.show(t >= 1 ? next : K.lerp(start, next, t, def.skip)); });
      },
      render(view, R) {
        const g = R.F.g, cells = view.cells || [], n = cells.length;
        lay(n, cells); const G = geom(n);
        const hlRange = K.isObj(view.highlight) && Array.isArray(view.highlight.range) ? view.highlight.range : null;
        const sel = new Set(view.selected || []), done = new Set((view.done || []).map(Number));
        const act = view.active;
        /* cell positions, adjusted by a running swap or a drag */
        const P = (k) => {
          let [x, y] = G.pos(k);
          const s = view._swap;
          const ins = view._ins;
          if (ins && ins.kind === 'in') { const e = 1 - (1 - ins.t) ** 3; if (k > ins.at) { const [px, py] = G.pos(k - 1); return [px + (x - px) * e, py + (y - py) * e]; } if (k === ins.at) return [x, y - 30 * (1 - e)]; }
          if (ins && ins.kind === 'out' && k >= ins.at) { const e = 1 - (1 - ins.t) ** 3, [px, py] = G.pos(k + 1); return [px + (x - px) * e, py + (y - py) * e]; }
          if (s && (k === s.i || k === s.j)) { const other = k === s.i ? s.j : s.i, [ox, oy] = G.pos(other), e = s.t < 0.5 ? 4 * s.t ** 3 : 1 - (-2 * s.t + 2) ** 3 / 2, lift = Math.sin(Math.PI * e) * (stack ? 36 : 34) * (k === s.i ? -1 : 1); return stack ? [x + lift, y + (oy - y) * e] : [x + (ox - x) * e, y + lift]; }
          if (dragView) {
            const { i, to, px } = dragView;
            if (k === i) return [px - cw / 2, y - 8];
            if (i < to && k > i && k <= to) return G.pos(k - 1);
            if (i > to && k >= to && k < i) return G.pos(k + 1);
          }
          return [x, y];
        };
        /* range wash behind the cells */
        if (hlRange && n) {
          const a = hlRange[0] - from, b = hlRange[1] - from, [ax, ay] = G.pos(Math.max(0, a)), [bx, by] = G.pos(Math.min(n - 1, b));
          const o = K.obj('range', '', 1);
          if (stack) o.append(svg('rect', { x: ax - 6, y: by - 6, width: cw + 12, height: ay - by + ch + 12, rx: 8, class: 'cvb-range' }));
          else { // one band per row the range covers (wrapped arrays)
            const lo = Math.max(0, a), hi = Math.min(n - 1, b);
            for (let r0 = Math.floor(lo / perRow); r0 <= Math.floor(hi / perRow); r0++) { const s0 = Math.max(lo, r0 * perRow), s1 = Math.min(hi, r0 * perRow + perRow - 1), [sx0, sy0] = G.pos(s0), [sx1] = G.pos(s1); o.append(svg('rect', { x: sx0 - 6, y: sy0 - 6, width: sx1 - sx0 + cw + 12, height: ch + 12, rx: 8, class: 'cvb-range' })); }
          }
          g.append(o);
          if (view.highlight.label) g.append(K.txt(stack ? ax + cw + 14 : (ax + bx + cw) / 2, stack ? (ay + by + ch) / 2 : ay + ch + 34, view.highlight.label, { anchor: stack ? 'start' : 'middle', size: 12, cls: 'cvb-strong' }));
        }
        const order = [...Array(n).keys()];
        if (dragView) { order.splice(order.indexOf(dragView.i), 1); order.push(dragView.i); }
        const idxG = svg('g'), cellsG = svg('g'); g.append(idxG, cellsG);
        for (const k of order) {
          const [x, y] = P(k), idx = k + from, id = 'c' + idx;
          const dim = act && (idx < act[0] || idx > act[1]);
          const o = K.obj(id, 'cvb-cell-o' + (sel.has(id) ? ' is-on' : '') + (dim ? ' is-dim' : ''), done.has(idx) ? 3 : 'ink');
          o.append(K.washRect(x - 4, y - 4, cw + 8, ch + 8, 8));
          if (linked) {
            o.append(svg('rect', { x, y, width: cw + 18, height: ch, rx: 6, class: 'cvb-cell cvb-tapbox cv-body' }), svg('line', { x1: x + cw, x2: x + cw, y1: y, y2: y + ch, class: 'cvb-ln thin' }), svg('circle', { cx: x + cw + 9, cy: y + ch / 2, r: 3, class: 'cvb-dot' }));
          } else o.append(svg('rect', { x, y, width: cw, height: ch, rx: 6, class: 'cvb-cell cvb-tapbox cv-body' + (cells[k] == null ? ' ghost' : '') }));
          const t = text(cells[k]), cl = cells[k] && typeof cells[k] === 'object' && !Array.isArray(cells[k]) && cells[k].label != null ? String(cells[k].label) : null;
          const fs = t.length > 4 ? Math.max(10, Math.min(13, Math.floor(13 * (cw - 6) / Math.max(1, K.tw(t, 13))))) : 16;
          const vy = cl ? y + ch / 2 + 6 : y + ch / 2;
          if (cl) o.append(K.txt(x + cw / 2, y + 10, cl, { size: 10, weight: 600, cls: 'cvb-muted' }));
          o.append(t.includes('$') ? K.lab(x + cw / 2, vy, t, { w: cw }) : K.txt(x + cw / 2, vy, t, { size: cl ? Math.min(fs, 14) : fs, weight: done.has(idx) ? 700 : 500 }));
          if (view._ins && view._ins.kind === 'in' && k === view._ins.at) o.setAttribute('opacity', Math.max(0, view._ins.t).toFixed(2));
          if (params.showIndex !== false && !linked) { const [gx, gy] = G.pos(k); idxG.append(stack ? K.txt(gx - 10, gy + ch / 2, String(idx), { anchor: 'end', size: 12, cls: 'cvb-tick' }) : K.txt(gx + cw / 2, gy + ch + 14, String(idx), { size: 12, cls: 'cvb-tick' })); }
          if (R.active('drag') && !stack && !linked) { o.dataset.drag = String(k); o.classList.add('cvb-handle'); o.setAttribute('tabindex', '0'); o.setAttribute('role', 'button'); o.setAttribute('aria-label', `Cell ${idx}, value ${t}`); }
          R.tappable(o, id, `Cell ${idx}, value ${t}`);
          cellsG.append(o);
        }
        /* linked list arrows and the null terminator */
        if (linked && n) {
          for (let k = 0; k < n; k++) {
            const [x, y] = P(k), sx = x + cw + 9, sy = y + ch / 2;
            if (k < n - 1) { const [nx] = P(k + 1); g.append(K.arrow(sx, sy, nx - 2, sy, { cls: 'cvb-ln thin', head: 8 })); }
            else { g.append(K.arrow(sx, sy, sx + 26, sy, { cls: 'cvb-ln thin', head: 8 }), K.txt(sx + 30, sy, params.nullLabel || 'null', { anchor: 'start', size: 13, cls: 'cvb-muted' })); }
          }
        }
        /* stack top and queue ends */
        if (stack && n) { const [x, y] = P(n - 1); g.append(K.arrow(x + cw + 56, y + ch / 2, x + cw + 6, y + ch / 2, { cls: 'cvb-ln thin', head: 8 }), K.txt(x + cw + 60, y + ch / 2, params.topLabel || 'top', { anchor: 'start', cls: 'cvb-strong' })); }
        if (stack) { const [x] = G.pos(0); g.append(svg('path', { d: `M${x - 6},${G.pos(0)[1] - (cap - 1) * ch - 6}L${x - 6},${H - 30}L${x + cw + 6},${H - 30}L${x + cw + 6},${G.pos(0)[1] - (cap - 1) * ch - 6}`, class: 'cvb-ln thin', style: 'stroke: var(--line-strong)' })); }
        if (mode === 'queue' && n) {
          const [fx, fy] = P(0), [bx] = P(n - 1), y = fy + ch + 34;
          g.append(K.txt(fx + cw / 2, y, params.frontLabel || 'front', { cls: 'cvb-strong', size: 12 }));
          if (n > 1) g.append(K.txt(bx + cw / 2, y, params.backLabel || 'back', { cls: 'cvb-strong', size: 12 }));
        }
        /* pointers: labelled arrows above the cells (right of the stack) */
        const groups = {};
        (view.pointers || []).forEach((p) => { const k = Math.round(p.at - from); (groups[k] = groups[k] || []).push(p); });
        for (const [k, ps] of Object.entries(groups)) {
          ps.forEach((p, j) => {
            const kk = +k, inside = kk >= 0 && kk < Math.max(n, 1);
            const [x, y] = inside ? P(kk) : G.pos(kk);
            const o = K.obj(p.id, 'cvb-ptr', p.colour || j + 1);
            if (stack) { const ax = x + cw + 6 + 90 + j * 0, ay = y + ch / 2 + (j - (ps.length - 1) / 2) * 14; o.append(K.washRect(x + cw + 4, ay - 10, 120, 20, 6), K.arrow(ax, ay, x + cw + 6, y + ch / 2, { cls: 'cvb-ln thin', head: 7 }), K.txt(ax + 4, ay, p.label ?? p.id, { anchor: 'start', size: 13 })); }
            else {
              const dx = (j - (ps.length - 1) / 2) * 22, below = !!p.below, cx = x + cw / 2;
              const ly = below ? y + ch + 40 : y - 36, ay0 = below ? y + ch + 27 : y - 24, ay1 = below ? y + ch + 20 : y - 4;
              o.append(K.washRect(cx + dx - 16, Math.min(ly, ay1) - 10, 32, Math.abs(ay1 - ly) + 20, 6), K.arrow(cx + dx * 0.6, ay0, cx + dx * 0.25, ay1, { cls: 'cvb-ln thin', head: 7 }), K.txt(cx + dx, ly, p.label ?? p.id, { size: 13 }));
            }
            R.tappable(o, String(p.id), `Pointer ${p.label ?? p.id}`); // item 384: pointers are tap targets
            g.append(o);
          });
        }
      },
      drag: {
        start: (id, p, R) => (R.active('drag') ? { i: +id } : null),
        move(info, p, R, end) {
          const n = (R.state.cells || []).length, G = geom(n), xs = [...Array(n).keys()].map((k) => G.pos(k)[0] + cw / 2);
          let to = 0, best = Infinity; xs.forEach((x, k) => { if (Math.abs(x - p.x) < best) { best = Math.abs(x - p.x); to = k; } });
          if (!end) { dragView = { i: info.i, to, px: K.clamp(p.x, xs[0] - cw, xs[n - 1] + cw) }; R.redraw(); return; }
          dragView = null; reorder(R, info.i, to);
        },
        key(id, dx, dy, R) { const i = +id, n = (R.state.cells || []).length, to = K.clamp(i + Math.sign(dx || -dy), 0, n - 1); if (to !== i) reorder(R, i, to, true); },
      },
      methods: (R) => ({
        order: () => (R.state._order || [...Array((R.state.cells || []).length).keys()].map((k) => 'c' + (k + from))),
        /* item 411: put the opening cells in the order of these ids (c0, c2, c1, ...), for the place widget's array mode */
        setOrder: (ids, opts = { instant: true }) => { const base = (params.cells || []).slice(), ord = [].concat(ids || []).map(String).filter((id) => /^c-?\d+$/.test(id) && base[+id.slice(1) - from] !== undefined); if (ord.length !== base.length) return; R.inst.set({ cells: ord.map((id) => base[+id.slice(1) - from]), _order: ord }, opts); },
        setParam: (name, v) => R.inst.set(String(name) === 'step' ? { step: +v } : Z.canvas.paramPatch(String(name), v), { instant: String(name) !== 'step' }),
        getParam: (name) => (String(name) === 'step' ? (R.state.step ?? 0) : (R.state.params || {})[String(name)]),
      }),
    };
    const reorder = (R, i, to, keyMove) => {
      const cells = R.state.cells.slice(), [v] = cells.splice(i, 1); cells.splice(to, 0, v);
      const prevOrder = R.state._order || [...Array(cells.length).keys()].map((k) => 'c' + (k + from));
      const ord = prevOrder.slice(), [o] = ord.splice(i, 1); ord.splice(to, 0, o);
      R.commit({ cells, _order: ord });
      R.emit({ type: 'order', order: ord, cells, phase: 'end' });
      if (keyMove) { const el = R.F.g.querySelector(`[data-drag="${to}"]`); if (el) el.focus({ preventScroll: true }); }
    };
    return K.make(host, params, ctx, def);
  });
})();
