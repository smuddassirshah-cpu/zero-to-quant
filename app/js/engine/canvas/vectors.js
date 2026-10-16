/* vectors: 2D vectors as arrows with sums (parallelogram), scaling, projection, span and a basis-skewed grid.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js). */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  C.register('vectors', (host, params, ctx) => {
    const K = Z.cvb;
    const xr = params.x || [-5, 5], yr = params.y || [-5, 5];
    const W = 540, inner = W - 28;
    const H = params.height || Math.round(Math.max(240, Math.min(540, inner * (yr[1] - yr[0]) / (xr[1] - xr[0]) + 28)));
    const m = { l: 14, r: 14, t: 14, b: 14 };
    const sx = C.scale(xr, [m.l, W - m.r]), sy = C.scale(yr, [H - m.b, m.t]);
    const base = (params.vectors || []).map((v, i) => ({ ...v, id: v.id || 'v' + i, slot: v.colour || i + 1 }));
    const add = (a, b) => [a[0] + b[0], a[1] + b[1]], mul = (k, a) => [k * a[0], k * a[1]], dot = (a, b) => a[0] * b[0] + a[1] * b[1];

    const def = {
      kind: 'vectors', aria: params.aria || 'Vectors on a plane',
      modes: ['drag', 'slider', 'tap'],
      size: () => ({ w: W, h: H }),
      listKeys: ['vectors', 'points'],
      init: () => ({ vectors: base.map((v) => ({ ...v })), points: (params.points || []).map((p, i) => ({ ...p, id: p.id || 'p' + i })), show: [], scale: Object.fromEntries(base.map((v) => [v.id, 1])), drag: null, basis: null, highlight: [], selected: [] }),
      render(view, R) {
        const g = R.F.g, vs = view.vectors || [], byId = Object.fromEntries(vs.map((v) => [v.id, v]));
        const show = new Set([].concat(view.show || []));
        const x0 = m.l, x1 = W - m.r, y0 = H - m.b, y1 = m.t;
        /* basis grid replaces the standard grid when given */
        const basis = view.basis;
        if (basis) {
          K.planeAxes(g, sx, sy, { grid: false, xLabel: params.xLabel, yLabel: params.yLabel });
          const gg = svg('g', { 'clip-path': R.clipRect(x0, y1, x1 - x0, y0 - y1, 'basis') });
          const [b1, b2] = basis, span = Math.max(xr[1] - xr[0], yr[1] - yr[0]) * 2, N = Math.ceil(span);
          const fam = (dir, step, cls) => { for (let k = -N; k <= N; k++) { const o = mul(k, step), a = add(o, mul(-span, dir)), b = add(o, mul(span, dir)); gg.append(svg('line', { x1: sx(a[0]), y1: sy(a[1]), x2: sx(b[0]), y2: sy(b[1]), class: 'cvb-basis ' + cls })); } };
          fam(b2, b1, 'cvb-c1'); fam(b1, b2, 'cvb-c2');
          g.append(gg);
          [['b1', b1, 1, params.basisLabels?.[0] ?? '$\\mathbf{b}_1$'], ['b2', b2, 2, params.basisLabels?.[1] ?? '$\\mathbf{b}_2$']].forEach(([id, b, slot, lb]) => {
            const o = K.obj(id, '', slot); o.append(K.washPath(`M${sx(0)},${sy(0)}L${sx(b[0])},${sy(b[1])}`), K.arrow(sx(0), sy(0), sx(b[0]), sy(b[1]), { cls: 'cvb-ln bold' })); g.append(o);
            g.append(K.lab(sx(b[0]) + 6, sy(b[1]) + 12, lb, { anchor: 'start', halo: true }));
          });
        } else K.planeAxes(g, sx, sy, { grid: params.grid ?? true, xLabel: params.xLabel, yLabel: params.yLabel });
        const plot = svg('g', { 'clip-path': R.clipRect(x0, y1, x1 - x0, y0 - y1) }); g.append(plot);
        const over = svg('g'); g.append(over);
        const labels = [];
        const head = (v) => { const k = (view.scale && view.scale[v.id]) ?? 1; return mul(k, v.v); };
        const tail = (v) => (v.from ? (typeof v.from === 'string' ? head(byId[v.from]) : v.from) : [0, 0]);

        /* span */
        if (show.has('span') || view.span) {
          const ids = [].concat(view.span || (vs[0] ? [vs[0].id] : [])).filter((id) => byId[id]);
          const dirs = ids.map((id) => byId[id].v);
          const independent = dirs.length >= 2 && Math.abs(dirs[0][0] * dirs[1][1] - dirs[0][1] * dirs[1][0]) > 1e-9;
          const o = K.obj('span', '', byId[ids[0]] ? byId[ids[0]].slot : 1);
          if (independent) o.append(svg('rect', { x: x0, y: y1, width: x1 - x0, height: y0 - y1, class: 'cvb-span' }));
          else if (dirs.length && (dirs[0][0] || dirs[0][1])) { const d = dirs[0], L = (xr[1] - xr[0] + yr[1] - yr[0]) * 2; const p = `M${sx(-d[0] * L)},${sy(-d[1] * L)}L${sx(d[0] * L)},${sy(d[1] * L)}`; o.append(svg('path', { d: p, class: 'cvb-ln', style: 'stroke-width: 16px; opacity: 0.16' }), svg('path', { d: p, class: 'cvb-ln thin cvb-dash' })); }
          plot.append(o);
        }
        /* sum by the parallelogram */
        if (show.has('sum') || view.sum) {
          const [a, b] = [].concat(view.sum || vs.slice(0, 2).map((v) => v.id)).map((id) => byId[id]);
          if (a && b) {
            const ha = head(a), hb = head(b), s = add(ha, hb), o = K.obj('sum', '', view.sumColour || 3);
            const ghost = svg('g', { class: 'cvb-ghost' });
            ghost.append(svg('path', { d: `M${sx(ha[0])},${sy(ha[1])}L${sx(s[0])},${sy(s[1])}`, class: 'cvb-ln thin cvb-dash ' + K.colourCls(b.slot) }), svg('path', { d: `M${sx(hb[0])},${sy(hb[1])}L${sx(s[0])},${sy(s[1])}`, class: 'cvb-ln thin cvb-dash ' + K.colourCls(a.slot) }));
            plot.append(ghost);
            o.append(K.washPath(`M${sx(0)},${sy(0)}L${sx(s[0])},${sy(s[1])}`), K.arrow(sx(0), sy(0), sx(s[0]), sy(s[1]), { cls: 'cvb-ln' }));
            plot.append(o);
            labels.push({ x: sx(s[0]) + 8, y: sy(s[1]) - 12, text: view.sumLabel || params.sumLabel || `${a.label || a.id} + ${b.label || b.id}`.replace(/\$ \+ \$/, ' + '), anchor: 'start' });
          }
        }
        /* projection of one vector onto another, with the perpendicular */
        if (show.has('projection') || view.project) {
          const pr = view.project || (vs[1] ? { of: vs[0].id, onto: vs[1].id } : null);
          const a = pr && byId[pr.of], b = pr && byId[pr.onto];
          if (a && b && dot(b.v, b.v) > 0) {
            const ha = head(a), hb = head(b), k = dot(ha, hb) / dot(hb, hb), p = mul(k, hb);
            const perp = K.obj('perp', '', 'ink'), dp = `M${sx(ha[0])},${sy(ha[1])}L${sx(p[0])},${sy(p[1])}`;
            perp.append(K.washPath(dp), svg('path', { d: dp, class: 'cvb-ln thin cvb-dash' }));
            /* right-angle mark at the foot */
            const ub = [hb[0] / Math.hypot(...hb), hb[1] / Math.hypot(...hb)], ua = [ha[0] - p[0], ha[1] - p[1]], la = Math.hypot(...ua);
            if (la > 1e-6) {
              const s = 10, u1 = [ub[0], -ub[1]], u2 = [ua[0] / la, -ua[1] / la], fx = sx(p[0]), fy = sy(p[1]);
              const dir = k >= 0 ? -1 : 1;
              perp.append(svg('path', { d: `M${fx + dir * u1[0] * s},${fy + dir * u1[1] * s}L${fx + dir * u1[0] * s + u2[0] * s},${fy + dir * u1[1] * s + u2[1] * s}L${fx + u2[0] * s},${fy + u2[1] * s}`, class: 'cvb-ra' }));
            }
            plot.append(perp);
            const o = K.obj('proj', '', view.projColour || 4);
            o.append(K.washPath(`M${sx(0)},${sy(0)}L${sx(p[0])},${sy(p[1])}`), K.arrow(sx(0), sy(0), sx(p[0]), sy(p[1]), { cls: 'cvb-ln bold' }));
            plot.append(o);
            labels.push({ x: sx(p[0]) + 8, y: sy(p[1]) + 16, text: view.projLabel || params.projLabel || 'proj', anchor: 'start' });
          }
        }
        /* the vectors themselves; scaled ones leave a dashed ghost of the original */
        const dragSet = view.drag ? new Set([].concat(view.drag)) : null;
        for (const v of vs) {
          if ((view.hide || []).includes(v.id)) continue;
          const t = tail(v), h = add(t, head(v)), k = (view.scale && view.scale[v.id]) ?? 1;
          if (k !== 1) { const og = add(t, v.v); plot.append(svg('path', { d: `M${sx(t[0])},${sy(t[1])}L${sx(og[0])},${sy(og[1])}`, class: 'cvb-ln thin cvb-dash ' + K.colourCls(v.slot) })); }
          const o = K.obj(v.id, '', v.slot);
          o.append(K.washPath(`M${sx(t[0])},${sy(t[1])}L${sx(h[0])},${sy(h[1])}`), K.arrow(sx(t[0]), sy(t[1]), sx(h[0]), sy(h[1]), { cls: 'cvb-ln bold' }));
          /* tap mode (item 107): the whole arrow is the target, through a wide transparent stroke */
          if (R.mode === 'tap') { o.append(svg('path', { d: `M${sx(t[0])},${sy(t[1])}L${sx(h[0])},${sy(h[1])}`, class: 'cvb-tapbox cv-body', style: 'stroke: transparent; stroke-width: 22px; fill: none' })); R.tappable(o, v.id, `Vector ${String(v.label || v.id).replace(/\$|\\[a-zA-Z]+|[{}]/g, '')}`); }
          plot.append(o);
          const canDrag = !v.from && R.active() && ((dragSet && dragSet.has(v.id)) || (!dragSet && R.mode === 'drag'));
          if (canDrag) over.append(K.handle(sx(h[0]), sy(h[1]), v.id, { r: 7, label: `Head of ${v.label || v.id}` }));
          const lt = k !== 1 && v.label ? (/^\$.*\$$/.test(v.label) ? `$${K.fmt(k, 3)}${v.label.slice(1, -1)}$` : K.fmt(k, 3) + v.label) : v.label;
          if (lt) {
            /* labelPos (item 106): "end" (default, past the head), "mid" (beside the middle) or "start" (by the tail); labelSide flips the side */
            const dx = h[0] - t[0], dy = h[1] - t[1], L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L, side = v.labelSide === 'right' ? -1 : 1;
            const text = params.showCoords ? `${lt} (${K.fmt(h[0], 2)}, ${K.fmt(h[1], 2)})` : lt;
            if (v.labelPos === 'mid' || v.labelPos === 'start') {
              const f = v.labelPos === 'mid' ? 0.5 : 0.18, nx = -uy * side, ny = ux * side; // left normal in maths coordinates
              const px = sx(t[0] + dx * f) + nx * 14, py = sy(t[1] + dy * f) - ny * 14;
              labels.push({ x: px, y: py, text, anchor: nx > 0.35 ? 'start' : nx < -0.35 ? 'end' : 'middle' });
            } else labels.push({ x: sx(h[0]) + ux * 10 + uy * 10 * side, y: sy(h[1]) - uy * 10 + ux * 10 * side, text, anchor: dx >= 0 ? 'start' : 'end' });
          }
        }
        /* points (item 106): labelled dots such as A, B, O, M, with labelPos n, ne, e, se, s, sw, w, nw */
        for (const p of view.points || []) {
          if (p.x == null || p.y == null) continue;
          const x = sx(p.x), y = sy(p.y), o = K.obj(p.id, 'cvb-pt', p.colour || 'ink');
          o.append(K.washCircle(x, y, 11), svg('circle', { cx: x, cy: y, r: R.mode === 'tap' ? 6 : 4.5, class: 'cvb-dot' + (p.open ? ' open' : '') + (R.mode === 'tap' ? ' cv-body' : '') }));
          if (R.mode === 'tap') { o.append(svg('circle', { cx: x, cy: y, r: 16, class: 'cvb-tapbox', fill: 'transparent' })); R.tappable(o, p.id, `Point ${p.label || p.id}`); }
          over.append(o);
          if (p.label) {
            const pos = p.labelPos || 'ne', ddx = pos.includes('e') ? 12 : pos.includes('w') ? -12 : 0, ddy = pos.includes('n') ? -13 : pos.includes('s') ? 14 : 0;
            labels.push({ x: x + ddx, y: y + ddy, text: String(p.label), anchor: ddx > 0 ? 'start' : ddx < 0 ? 'end' : 'middle', id: p.id });
          }
        }
        /* the projection sits along the vector it projects onto, so lift it above the vectors */
        ['perp', 'proj'].forEach((id) => { const el = plot.querySelector(`[data-id="${id}"]`); if (el) plot.append(el); });
        K.placeLabels(labels, [], { x0, x1, y0: y1, y1: y0 });
        for (const l of labels) over.append(K.lab(l.x, l.y, l.text, { anchor: l.anchor, halo: true, cls: 'cvb-strong' }));
      },
      drag: {
        start: (id, p, R) => ((R.state.vectors || []).some((v) => v.id === id) ? { id } : null),
        move(info, p, R, end) { setHead(R, info.id, sx.invert(p.x), sy.invert(p.y), end); },
        key(id, dx, dy, R) { const v = (R.state.vectors || []).find((q) => q.id === id); if (!v) return; const st = params.snap || 0.5; const k = (R.state.scale && R.state.scale[id]) ?? 1; setHead(R, id, v.v[0] * k + dx * st, v.v[1] * k + dy * st, true); },
      },
      methods: (R) => ({
        points: () => Object.fromEntries((R.state.vectors || []).map((v) => [v.id, { x: v.v[0], y: v.v[1] }])),
        place: (id, pos, opts = {}) => R.inst.set({ vectors: { [id]: { v: [pos[0], pos[1]] } } }, opts),
      }),
    };
    const setHead = (R, id, x, y, end) => {
      x = K.clamp(x, xr[0], xr[1]); y = K.clamp(y, yr[0], yr[1]);
      if (params.snap) { x = K.snapTo(x, params.snap); y = K.snapTo(y, params.snap); }
      const k = (R.state.scale && R.state.scale[id]) ?? 1;
      const v = [K.round(x / k, 6), K.round(y / k, 6)];
      R.commit({ vectors: { [id]: { v } } });
      R.emit({ type: 'drag', id, v, x: v[0], y: v[1], phase: end ? 'end' : 'move' });
    };
    return K.make(host, params, ctx, def);
  });
})();
