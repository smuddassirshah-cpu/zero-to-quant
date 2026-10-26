/* scatter: points with an optional least squares line, a given or learner-placed line, and residuals.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js).
   Pass 7: curves take thin and opacity (item 350); a point with exclude: true is drawn as a ring and joins neither the
   fit nor the residuals (an (x-bar, y-bar) marker); showSAE adds the sum of absolute residuals; xTicks "integer";
   state.lines [{ id, m, b, label, colour, dashed }] draws more straight lines (item 358); points carry a group (an
   object's group, or a third array entry) and are coloured by it with a legend (item 365). */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  const lsq = (pts) => {
    const n = pts.length; if (n < 2) return { m: 0, b: n ? pts[0].y : 0 };
    const mx = pts.reduce((s, p) => s + p.x, 0) / n, my = pts.reduce((s, p) => s + p.y, 0) / n;
    let sxy = 0, sxx = 0; for (const p of pts) { sxy += (p.x - mx) * (p.y - my); sxx += (p.x - mx) ** 2; }
    const m = sxx ? sxy / sxx : 0; return { m, b: my - m * mx };
  };

  C.register('scatter', (host, params, ctx) => {
    const K = Z.cvb;
    const W = 540, H = params.height || 320;
    const norm = (list) => (list || []).map((p, i) => (Array.isArray(p) ? { id: 'p' + i, x: +p[0], y: +p[1], ...(p[2] != null ? { group: String(p[2]) } : {}) } : { ...p, id: p.id || 'p' + i, x: +p.x, y: +p.y }));
    /* item 365: groups in order of params.groups (labels), else of first appearance; slots 1, 2, 3, ... */
    const groupsOf = (pts) => { const order = (params.groups || []).map((q) => String(q && typeof q === 'object' ? q.id : q)); pts.forEach((q) => { if (q.group != null && !order.includes(String(q.group))) order.push(String(q.group)); }); return order; };
    const groupLabel = (gid) => { const q = (params.groups || []).find((x) => String(x && typeof x === 'object' ? x.id : x) === gid); return q && typeof q === 'object' ? String(q.label ?? q.id) : gid; };
    /* item 296: sim: { n, rho, seed, mx, my, sx, sy } draws n seeded normal pairs with correlation rho; a control on
       "rho" (state.params.rho) re-correlates the same draws, so a live correlation slider needs no derive */
    const sim = params.sim && typeof params.sim === 'object' ? params.sim : null;
    const simZ = sim ? (() => { const r = K.rngFor(sim.seed ?? 1), n = Math.max(2, Math.round(sim.n || 60)), z = []; for (let i = 0; i < n; i++) z.push([K.gauss(r), K.gauss(r)]); return z; })() : null;
    const simPts = (rho) => { const q = K.clamp(+rho, -1, 1), c = Math.sqrt(1 - q * q), mx = +(sim.mx ?? 0), my = +(sim.my ?? 0), sdx = +(sim.sx ?? 1), sdy = +(sim.sy ?? 1); return simZ.map(([a, b], i) => ({ id: 'p' + i, x: mx + sdx * a, y: my + sdy * (q * a + c * b) })); };
    const rhoOf = (view) => { const v = view && view.params && view.params.rho != null ? view.params.rho : sim.rho ?? 0; return Number.isFinite(+v) ? +v : 0; };
    const base = sim ? simPts(sim.rho ?? 0) : norm(params.points);
    const lbl = (v, fb) => (typeof v === 'string' ? v : fb);
    const xLabel = params.xLabel ?? lbl(params.x, null), yLabel = params.yLabel ?? lbl(params.y, null);
    const rangeOf = (key, given) => {
      if (Array.isArray(given)) return given;
      if (sim) { const m = +(sim[key === 'x' ? 'mx' : 'my'] ?? 0), sd = +(sim[key === 'x' ? 'sx' : 'sy'] ?? 1), t = C.niceTicks(m - 3.4 * sd, m + 3.4 * sd, 6); return [t[0], t[t.length - 1]]; }
      const vs = base.map((p) => p[key]); if (!vs.length) return [0, 1];
      const lo = Math.min(...vs), hi = Math.max(...vs), pad = (hi - lo || 1) * 0.08;
      const t = C.niceTicks(lo - pad, hi + pad, 6); const st = t.length > 1 ? t[1] - t[0] : 1;
      return [Math.min(t[0], Math.floor((lo - pad) / st) * st), Math.max(t[t.length - 1], Math.ceil((hi + pad) / st) * st)];
    };
    const xr = rangeOf('x', params.xRange || (Array.isArray(params.x) ? params.x : null));
    const yr = rangeOf('y', params.yRange || (Array.isArray(params.y) ? params.y : null));
    const ml = K.yMargin(yr[0], yr[1], H - 60), mt = yLabel ? 26 : 14, mb = xLabel ? 46 : 30, mr = 14;
    const sx = C.scale(xr, [ml, W - mr]), sy = C.scale(yr, [H - mb, mt]);
    const lineEnds = () => [xr[0] + (xr[1] - xr[0]) * 0.12, xr[1] - (xr[1] - xr[0]) * 0.12];
    const eq = (l) => `$\\hat{y} = ${K.fmt(l.m, 3)}x ${l.b < 0 ? '-' : '+'} ${K.fmt(Math.abs(l.b), 3)}$`;

    const def = {
      kind: 'scatter', aria: params.aria || 'Scatter plot',
      modes: ['drag', 'tap'],
      size: () => ({ w: W, h: H }),
      listKeys: ['points'],
      init: () => ({ points: base.map((p) => ({ ...p })), line: null, residuals: false, highlight: [], showFit: !!params.fit }),
      render(view, R) {
        const g = R.F.g, pts = sim ? simPts(rhoOf(view)) : view.points || [];
        const x0 = ml, x1 = W - mr, y0 = H - mb, y1 = mt;
        /* xTicks "integer": whole-number ticks only */
        const xInt = params.xTicks === 'integer' ? (() => { const n = Math.floor(xr[1]) - Math.ceil(xr[0]) + 1, every = Math.max(1, Math.ceil(n / Math.max(2, Math.floor((x1 - x0) / 46)))); const t = []; for (let v = Math.ceil(xr[0]); v <= xr[1]; v += every) t.push(v); return { ticks: t, step: every }; })() : null;
        K.chartAxes(g, sx, sy, { yLabel, xLabel, baseline: yr[0] < 0 && yr[1] > 0 ? 0 : null, ...(xInt ? { xTicks: xInt } : {}) });
        if (xr[0] < 0 && xr[1] > 0) g.append(svg('line', { x1: sx(0), x2: sx(0), y1: y0, y2: y1, class: 'cvb-axis thin' }));
        const plot = svg('g', { 'clip-path': R.clipRect(x0, y1, x1 - x0, y0 - y1) }); g.append(plot);
        const over = svg('g'); g.append(over);
        const labels = [];
        const fit = lsq(pts.filter((q) => !q.exclude));
        const lines = [];
        if (view.showFit ?? params.fit) lines.push({ id: 'fit', l: fit, colour: 'ink', label: params.fitLabel === 'auto' ? eq(fit) : params.fitLabel });
        if (view.line) lines.push({ id: 'line', l: view.line, colour: R.active('drag') ? 'manip' : (view.line.colour || 2), label: view.line.label === 'auto' ? eq(view.line) : view.line.label, dashed: view.line.dashed });
        [].concat(view.lines || params.lines || []).forEach((q, k) => { if (q && Number.isFinite(+q.m) && Number.isFinite(+q.b)) lines.push({ id: q.id || 'line' + (k + 2), l: { m: +q.m, b: +q.b }, colour: q.colour || 4 + k, label: q.label === 'auto' ? eq(q) : q.label, dashed: q.dashed }); });
        /* item 259: curves over the cloud: { id, expr: "f(x)" }, { id, x: "...", y: "...", t: [a, b] } (parametric) or
           { id, implicit: "F(x, y)" } (a risk ellipse), with colour, dashed and label */
        const P = { ...(params.params || {}), ...(view.params || {}) }, pn = Object.keys(P);
        for (const cv of [].concat(view.curves || params.curves || [])) {
          if (!cv) continue;
          let d = '';
          if (cv.implicit != null) { const c = K.fnOf(String(cv.implicit), ['y', ...pn]); d = K.contourLines((x, y) => c(x, { ...P, y }), xr, yr).map((ln) => 'M' + ln.map(([x, y]) => `${sx(x).toFixed(1)},${sy(y).toFixed(1)}`).join('L')).join(''); }
          else if (cv.x != null && cv.y != null) { const fx = K.fnOf(String(cv.x), ['t', ...pn]), fy = K.fnOf(String(cv.y), ['t', ...pn]), tr = cv.t || [0, 2 * Math.PI]; d = 'M' + Array.from({ length: 241 }, (_, i) => { const t = tr[0] + (tr[1] - tr[0]) * i / 240; return `${sx(fx(0, { ...P, t })).toFixed(1)},${sy(fy(0, { ...P, t })).toFixed(1)}`; }).join('L'); }
          else if (cv.expr != null) { const f = K.fnOf(String(cv.expr), pn); d = K.brokenPath(Array.from({ length: 241 }, (_, i) => { const x = xr[0] + (xr[1] - xr[0]) * i / 240; return [sx(x), sy(f(x, P))]; }), H, y1, y0); }
          if (!d) continue;
          const o = K.obj(cv.id || 'curve', '', cv.colour || 3); o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln' + (cv.dashed ? ' cvb-dash' : '') + (cv.thin ? ' thin' : ''), ...(cv.opacity != null ? { 'stroke-opacity': K.clamp(+cv.opacity, 0.05, 1) } : {}) })); plot.append(o);
          if (cv.label && Array.isArray(cv.labelAt)) labels.push({ x: sx(cv.labelAt[0]), y: sy(cv.labelAt[1]), text: cv.label, anchor: 'start' });
        }
        const resid = view.residuals ? (view.residuals === 'fit' || !view.line ? fit : view.line) : null;
        let sse = 0, sae = 0;
        if (resid) {
          const rg = svg('g');
          pts.filter((q) => !q.exclude).forEach((p) => {
            const yh = resid.m * p.x + resid.b, r = p.y - yh; sse += r * r; sae += Math.abs(r);
            const o = K.obj('r-' + p.id, '', r >= 0 ? 'pos' : 'neg');
            const d = `M${sx(p.x)},${sy(p.y)}L${sx(p.x)},${sy(yh)}`;
            o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln thin' }));
            rg.append(o);
          });
          plot.append(rg);
        }
        for (const L of lines) {
          const a = xr[0], b = xr[1], d = `M${sx(a)},${sy(L.l.m * a + L.l.b)}L${sx(b)},${sy(L.l.m * b + L.l.b)}`;
          const o = K.obj(L.id, '', L.colour); o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln' + (L.dashed ? ' cvb-dash' : '') })); plot.append(o);
          if (L.label) { const lx = xr[1] - (xr[1] - xr[0]) * 0.02; labels.push({ x: sx(lx), y: sy(L.l.m * lx + L.l.b) + (L.l.m >= 0 ? 16 : -16), text: L.label, anchor: 'end' }); }
        }
        /* line handles first so point handles stay on top where they overlap */
        if (view.line && R.active('drag') && params.dragLine !== false) {
          lineEnds().forEach((x, i) => over.append(K.handle(sx(x), sy(view.line.m * x + view.line.b), 'l' + i, { r: 6, shape: 'diamond', label: i ? 'Line right end' : 'Line left end' })));
        }
        const sel = new Set(view.selected || []), groups = groupsOf(pts);
        if (groups.length && params.legend !== false) groups.forEach((gid, k) => { const lx = x1 - 8 - (groups.length - 1 - k) * 0, ly = y1 + 8 + k * 18, t = groupLabel(gid), o = K.obj('legend-' + gid, '', k + 1); o.append(svg('circle', { cx: lx - K.tw(t, 12) - 10, cy: ly, r: 4.5, class: 'cvb-dot' }), K.txt(lx, ly, t, { anchor: 'end', size: 12, halo: true })); over.append(o); });
        for (const p of pts) {
          const o = K.obj(p.id, sel.has(p.id) ? 'is-on' : '', p.colour || (p.group != null ? groups.indexOf(String(p.group)) + 1 : 1)), cx = sx(p.x), cy = sy(p.y);
          o.append(K.washCircle(cx, cy, 11));
          const dragOk = R.active('drag') && (!params.drag || params.drag === true || [].concat(params.drag).includes(p.id));
          if (dragOk) o.append(K.handle(cx, cy, p.id, { r: 6, label: `Point ${p.label || p.id}` }));
          else { if (R.mode === 'tap') o.append(svg('circle', { cx, cy, r: 9, class: 'cvb-tapbox', fill: 'transparent', stroke: 'none' })); o.append(p.exclude ? svg('circle', { cx, cy, r: 6, class: 'cvb-dot open cv-body' }) : svg('circle', { cx, cy, r: 4.5, class: 'cvb-dot cv-body' })); }
          R.tappable(o, p.id, p.label || p.id);
          over.append(o);
          if (p.label) labels.push({ x: cx + 8, y: cy - 11, text: p.label, anchor: 'start' });
        }
        const reads = [];
        if (resid && view.showSSE) reads.push((params.sseLabel || 'Sum of squared residuals') + ' ' + K.fmt(sse, 3));
        if (resid && view.showSAE) reads.push((params.saeLabel || 'Sum of absolute residuals') + ' ' + K.fmt(sae, 3));
        reads.forEach((t, k) => over.append(K.txt(x1 - 4, y1 + 10 + 18 * k + (groups.length && params.legend !== false ? 18 * groups.length : 0), t, { anchor: 'end', halo: true, cls: 'cvb-strong' })));
        if (reads.length) labels.forEach((l) => { if (l.y < y1 + 6 + 18 * reads.length) l.y += 18 * reads.length; });
        K.placeLabels(labels, [], { x0, x1, y0: y1, y1: y0 });
        for (const l of labels) over.append(K.lab(l.x, l.y, l.text, { anchor: l.anchor, halo: true, cls: 'cvb-strong' }));
      },
      drag: {
        start(id, p, R) {
          if (!R.active('drag')) return null;
          if (/^l[01]$/.test(id) && R.state.line) { const [a, b] = lineEnds(); const l = R.state.line; return { line: +id[1], fixed: id === 'l0' ? [b, l.m * b + l.b] : [a, l.m * a + l.b] }; }
          return (R.state.points || []).some((q) => q.id === id) ? { id } : null;
        },
        move(info, p, R, end) {
          const phase = end ? 'end' : 'move';
          if (info.line != null) {
            const [a, b] = lineEnds(), x = info.line ? b : a, y = K.clamp(sy.invert(p.y), yr[0], yr[1]);
            const m = (y - info.fixed[1]) / (x - info.fixed[0]), bb = y - m * x;
            const line = { ...R.state.line, m: K.round(m, 6), b: K.round(bb, 6) };
            R.commit({ line }); R.emit({ type: 'drag', id: 'line', m: line.m, b: line.b, phase });
            return;
          }
          let x = K.clamp(sx.invert(p.x), xr[0], xr[1]), y = K.clamp(sy.invert(p.y), yr[0], yr[1]);
          if (params.snap) { x = K.snapTo(x, params.snap); y = K.snapTo(y, params.snap); }
          x = K.round(x, 6); y = K.round(y, 6);
          R.commit({ points: { [info.id]: { x, y } } }); R.emit({ type: 'drag', id: info.id, x, y, phase });
        },
        key(id, dx, dy, R) {
          const st = params.snap || (C.niceTicks(xr[0], xr[1], 10)[1] - C.niceTicks(xr[0], xr[1], 10)[0]) / 2;
          if (/^l[01]$/.test(id)) { const info = def.drag.start(id, {}, R); const [a, b] = lineEnds(); const x = id === 'l1' ? b : a; const y = R.state.line.m * x + R.state.line.b + dy * (yr[1] - yr[0]) / 50; def.drag.move(info, { x: sx(x), y: sy(y) }, R, true); return; }
          const q = (R.state.points || []).find((r) => r.id === id); if (q) def.drag.move({ id }, { x: sx(q.x + dx * st), y: sy(q.y + dy * st) }, R, true);
        },
      },
      methods: (R) => ({
        /* the sample correlation of the points shown, for derive and captions (values.r) */
        values: () => { const P2 = sim ? simPts(rhoOf(R.state)) : R.state.points || []; const n = P2.length; if (n < 2) return {}; const mx = P2.reduce((t, q) => t + q.x, 0) / n, my = P2.reduce((t, q) => t + q.y, 0) / n; let sxy = 0, sxx = 0, syy = 0; P2.forEach((q) => { sxy += (q.x - mx) * (q.y - my); sxx += (q.x - mx) ** 2; syy += (q.y - my) ** 2; }); return { r: sxx && syy ? sxy / Math.sqrt(sxx * syy) : 0 }; },
        /* item 250: controls and derive reach line.m and line.b directly (a missing line starts flat at 0) */
        setParam: (name, v) => { const n = String(name), m = n.match(/^line\.(m|b)$/); if (m) { const l = R.state.line || { m: 0, b: 0 }; R.inst.set({ line: { ...l, [m[1]]: +v } }, { instant: true }); return; } R.inst.set(Z.canvas.paramPatch(n, v), { instant: true }); },
        getParam: (name) => { const n = String(name), m = n.match(/^line\.(m|b)$/); if (m) return R.state.line ? R.state.line[m[1]] : undefined; return (R.state.params || {})[n]; },
        fit: () => lsq((R.state.points || []).filter((q) => !q.exclude)),
        points: () => Object.fromEntries((R.state.points || []).map((q) => [q.id, { x: q.x, y: q.y }])),
        place: (id, pos, opts = {}) => (id === 'line' && K.isObj(pos) ? R.inst.set({ line: pos }, opts) : R.inst.set({ points: { [id]: { x: pos[0], y: pos[1] } } }, opts)),
      }),
    };
    return K.make(host, params, ctx, def);
  });
})();
