/* array: cells with index labels and pointer arrows; ranges; animated swaps; stack, queue and linked list modes;
   tap on cells and drag to reorder.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js). */
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
    const cw = linked ? Math.min(58, (W - 60) / cap - 26) : Math.min(52, Math.max(30, (W - 40) / cap));
    const ch = 44;
    const H = params.height || (stack ? Math.max(200, cap * ch + 80) : 150);
    const text = (v) => (v == null ? '' : typeof v === 'number' ? K.fmt(v, 3) : String(v));
    let pendingSwap = null, dragView = null;

    const geom = (n) => {
      if (stack) { const x = W / 2 - cw / 2 - 20, yb = H - 34; return { pos: (k) => [x, yb - (k + 1) * ch], n }; }
      const gap = linked ? 26 : 0, total = n * cw + Math.max(0, n - 1) * gap + (linked ? 40 : 0);
      const x0 = Math.max(10, (W - total) / 2), y = params.pointersBelow ? 30 : 58;
      return { pos: (k) => [x0 + k * (cw + gap), y], n, gap };
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
        if (a.instant) { a.show(next); return; }
        if (sw) return C.tween(0, 1, 640, (t) => { if (a.alive()) a.show(t >= 1 ? next : { ...next, cells: sw.before, _swap: { ...sw, t } }); });
        const start = R.shown;
        return C.tween(0, 1, 480, (t) => { if (a.alive()) a.show(t >= 1 ? next : K.lerp(start, next, t, def.skip)); });
      },
      render(view, R) {
        const g = R.F.g, cells = view.cells || [], n = cells.length, G = geom(n);
        const hlRange = K.isObj(view.highlight) && Array.isArray(view.highlight.range) ? view.highlight.range : null;
        const sel = new Set(view.selected || []), done = new Set((view.done || []).map(Number));
        const act = view.active;
        /* cell positions, adjusted by a running swap or a drag */
        const P = (k) => {
          let [x, y] = G.pos(k);
          const s = view._swap;
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
          else o.append(svg('rect', { x: ax - 6, y: ay - 6, width: bx - ax + cw + 12, height: ch + 12, rx: 8, class: 'cvb-range' }));
          g.append(o);
          if (view.highlight.label) g.append(K.txt(stack ? ax + cw + 14 : (ax + bx + cw) / 2, stack ? (ay + by + ch) / 2 : ay + ch + 34, view.highlight.label, { anchor: stack ? 'start' : 'middle', size: 12, cls: 'cvb-strong' }));
        }
        const order = [...Array(n).keys()];
        if (dragView) { order.splice(order.indexOf(dragView.i), 1); order.push(dragView.i); }
        const cellsG = svg('g'); g.append(cellsG);
        for (const k of order) {
          const [x, y] = P(k), idx = k + from, id = 'c' + idx;
          const dim = act && (idx < act[0] || idx > act[1]);
          const o = K.obj(id, 'cvb-cell-o' + (sel.has(id) ? ' is-on' : '') + (dim ? ' is-dim' : ''), done.has(idx) ? 3 : 'ink');
          o.append(K.washRect(x - 4, y - 4, cw + 8, ch + 8, 8));
          if (linked) {
            o.append(svg('rect', { x, y, width: cw + 18, height: ch, rx: 6, class: 'cvb-cell cvb-tapbox cv-body' }), svg('line', { x1: x + cw, x2: x + cw, y1: y, y2: y + ch, class: 'cvb-ln thin' }), svg('circle', { cx: x + cw + 9, cy: y + ch / 2, r: 3, class: 'cvb-dot' }));
          } else o.append(svg('rect', { x, y, width: cw, height: ch, rx: 6, class: 'cvb-cell cvb-tapbox cv-body' + (cells[k] == null ? ' ghost' : '') }));
          const t = text(cells[k]);
          o.append(t.includes('$') ? K.lab(x + cw / 2, y + ch / 2, t, { w: cw }) : K.txt(x + cw / 2, y + ch / 2, t, { size: t.length > 4 ? 13 : 16, weight: done.has(idx) ? 700 : 500 }));
          if (params.showIndex !== false && !linked) o.append(stack ? K.txt(x - 10, y + ch / 2, String(idx), { anchor: 'end', size: 12, cls: 'cvb-tick' }) : K.txt(x + cw / 2, y + ch + 14, String(idx), { size: 12, cls: 'cvb-tick' }));
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
      methods: (R) => ({ order: () => (R.state._order || [...Array((R.state.cells || []).length).keys()].map((k) => 'c' + (k + from))) }),
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
