/* walk: random walks or price paths from the seeded RNG; many faint paths, one bold, barriers and the mean path.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js). */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  C.register('walk', (host, params, ctx) => {
    const K = Z.cvb;
    const W = 540, H = params.height || 300;
    const seed = (params.sim && params.sim.seed) ?? params.seed ?? 1;
    const P = (view) => K.eff(params, view);

    /* Uniform draws are fixed per (run, path, step), so changing p, mu or sigma morphs the same paths. */
    const cache = new Map();
    const draws = (run, paths, steps) => {
      const key = run + ':' + paths + ':' + steps;
      if (!cache.has(key)) {
        if (cache.size > 12) cache.clear();
        const rng = K.rngFor((seed * 7919 + run * 104729) >>> 0);
        const u = [], z = [];
        for (let j = 0; j < paths; j++) { const uj = new Float64Array(steps), zj = new Float64Array(steps); for (let i = 0; i < steps; i++) { uj[i] = rng(); zj[i] = K.gauss(rng); } u.push(uj); z.push(zj); }
        cache.set(key, { u, z });
      }
      return cache.get(key);
    };
    const build = (view) => {
      const p = P(view), steps = Math.max(1, Math.round(p.steps || 50)), paths = Math.max(1, Math.round(p.paths || 1)), start = +(p.start ?? 0);
      const model = p.model || (p.mu != null || p.sigma != null ? 'normal' : 'coin');
      const d = draws(Math.round(view.run || 0), paths, steps), up = p.p ?? 0.5, step = p.step ?? 1, mu = p.mu ?? 0, sigma = p.sigma ?? 1;
      const out = [];
      for (let j = 0; j < paths; j++) {
        const a = new Float64Array(steps + 1); a[0] = start;
        for (let i = 0; i < steps; i++) a[i + 1] = a[i] + (model === 'normal' ? mu + sigma * d.z[j][i] : (d.u[j][i] < up ? step : -step));
        out.push(a);
      }
      const drift = model === 'normal' ? mu : (2 * up - 1) * step, vol = model === 'normal' ? sigma : 2 * step * Math.sqrt(up * (1 - up));
      return { p, steps, paths, start, model, out, drift, vol };
    };
    const barriers = (p) => { const b = p.barriers || []; return { lo: b[0] ?? null, hi: b[1] ?? null }; };
    const firstHit = (a, bar) => { for (let i = 0; i < a.length; i++) if ((bar.hi != null && a[i] >= bar.hi) || (bar.lo != null && a[i] <= bar.lo)) return i; return -1; };
    let seen = null;

    const def = {
      kind: 'walk', aria: params.aria || 'Random walk paths',
      modes: ['slider', 'tap'],
      size: () => ({ w: W, h: H }),
      skip: ['run'],
      init: () => ({ run: 0, showMean: false, highlight: [], params: Object.fromEntries(['p', 'mu', 'sigma', 'steps', 'paths', 'start', 'step'].filter((k) => typeof params[k] === 'number').map((k) => [k, params[k]])), reveal: 1 }),
      hlIds: (view) => (view.highlight || []).map((h) => (typeof h === 'number' ? 'path' + h : String(h))),
      animate(prev, next, a, R) {
        if (a.instant) { a.show(next); return; }
        if (Math.round(prev.run || 0) !== Math.round(next.run || 0)) {
          return C.tween(0, 1, 800, (t) => { if (a.alive()) a.show(t >= 1 ? next : { ...next, reveal: t }); }, 'standard');
        }
        const from = R.shown;
        return C.tween(0, 1, 600, (t) => { if (a.alive()) a.show(t >= 1 ? next : K.lerp(from, next, t, ['run'])); });
      },
      render(view, R) {
        const g = R.F.g, B = build(view), bar = barriers(B.p);
        let lo = Infinity, hi = -Infinity;
        for (const a of B.out) for (const v of a) { if (v < lo) lo = v; if (v > hi) hi = v; }
        if (bar.lo != null) lo = Math.min(lo, bar.lo); if (bar.hi != null) hi = Math.max(hi, bar.hi);
        let yr = params.y;
        if (!yr) { const pad = (hi - lo || 2) * 0.1; const t = C.niceTicks(lo - pad, hi + pad, 8), st = t[1] - t[0] || 1; yr = [Math.floor((lo - pad) / st) * st, Math.ceil((hi + pad) / st) * st]; seen = seen && !view._fresh ? [Math.min(seen[0], yr[0]), Math.max(seen[1], yr[1])] : yr; yr = seen; }
        const ml = K.yMargin(yr[0], yr[1], H - 60), mt = 26, mb = params.xLabel ? 46 : 30, mr = 70;
        const sx = C.scale([0, B.steps], [ml, W - mr]), sy = C.scale(yr, [H - mb, mt]);
        const x0 = ml, x1 = W - mr, y0 = H - mb, y1 = mt;
        K.chartAxes(g, sx, sy, { yLabel: params.yLabel ?? (B.model === 'normal' ? 'Value' : 'Position'), xLabel: params.xLabel ?? 'Step', baseline: B.start >= yr[0] && B.start <= yr[1] ? B.start : null });
        const plot = svg('g', { 'clip-path': R.clipRect(x0, y1 - 3, x1 - x0 + 3, y0 - y1 + 6) }), over = svg('g');
        g.append(plot, over);
        const right = [];
        /* barriers */
        [['barrier-down', bar.lo], ['barrier-up', bar.hi]].forEach(([id, v]) => {
          if (v == null) return; const y = sy(v), o = K.obj(id, '', 'ink');
          o.append(K.washPath(`M${x0},${y}L${x1},${y}`), svg('line', { x1: x0, x2: x1, y1: y, y2: y, class: 'cvb-ln thin cvb-dash' }));
          over.append(o); const t = (id === 'barrier-up' ? params.upLabel : params.downLabel) || K.fmt(v, 3);
          right.push({ y, text: t });
        });
        const reveal = K.clamp(view.reveal ?? 1, 0, 1), upto = reveal * B.steps;
        const em = new Set(def.hlIds(view));
        const pathD = (a) => { let d = ''; const last = Math.floor(upto); for (let i = 0; i <= last && i < a.length; i++) d += (i ? 'L' : 'M') + sx(i).toFixed(1) + ',' + sy(a[i]).toFixed(1); if (upto > last && last + 1 < a.length) { const f = upto - last; d += 'L' + sx(upto).toFixed(1) + ',' + sy(a[last] + (a[last + 1] - a[last]) * f).toFixed(1); } return d; };
        const stop = view.stopAtBarrier;
        let hits = 0;
        B.out.forEach((a, j) => {
          const h = (bar.lo != null || bar.hi != null) ? firstHit(a, bar) : -1; if (h >= 0) hits++;
          const arr = stop && h >= 0 ? a.slice(0, h + 1) : a;
          const main = j === (params.bold ?? 0), o = K.obj('path' + j, '', main ? (params.colour || 1) : (params.colour || 1));
          const d = pathD(arr);
          o.append(K.washPath(d), svg('path', { d, class: 'cvb-path' + (main ? ' main' : '') + (em.has('path' + j) ? ' em' : '') }));
          if (view.showHits && h >= 0 && h <= upto) o.append(svg('circle', { cx: sx(h), cy: sy(a[h]), r: main ? 4.5 : 3, class: 'cvb-dot' }));
          R.tappable(o, 'path' + j, 'Path ' + (j + 1));
          if (main) plot.append(o); else plot.insertBefore(o, plot.firstChild);
        });
        /* mean path and optional spread envelope */
        if (view.showMean) {
          const o = K.obj('mean', '', 'ink'), d = `M${sx(0)},${sy(B.start)}L${sx(B.steps)},${sy(B.start + B.drift * B.steps)}`;
          o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln thin cvb-dash' })); plot.append(o);
          right.push({ y: K.clamp(sy(B.start + B.drift * B.steps), y1 + 8, y0 - 8), text: params.meanLabel || 'mean' });
        }
        if (view.showSpread) {
          const o = K.obj('spread', '', 'muted'); let up = '', dn = '';
          for (let i = 0; i <= B.steps; i++) { const m = B.start + B.drift * i, s = B.vol * Math.sqrt(i) * (view.showSpread === true ? 1 : +view.showSpread); up += (i ? 'L' : 'M') + sx(i).toFixed(1) + ',' + sy(m + s).toFixed(1); dn += (i ? 'L' : 'M') + sx(i).toFixed(1) + ',' + sy(m - s).toFixed(1); }
          o.append(svg('path', { d: up, class: 'cvb-ln thin cvb-dash' }), svg('path', { d: dn, class: 'cvb-ln thin cvb-dash' })); plot.append(o);
        }
        /* end label of the bold path */
        const main = B.out[params.bold ?? 0];
        if (main && params.label) right.push({ y: K.clamp(sy(main[Math.min(main.length - 1, Math.round(upto))]), y1 + 8, y0 - 8), text: params.label });
        K.spread(right, 15, y1 + 6, y0 - 6);
        for (const l of right) over.append(K.txt(x1 + 6, l.y, l.text, { anchor: 'start', size: 12, cls: 'cvb-strong', halo: true }));
        if (view.showHits && (bar.lo != null || bar.hi != null) && B.paths > 1) {
          const t = view.hitsLabel ? String(view.hitsLabel).replace('{hits}', hits).replace('{paths}', B.paths) : `${hits} of ${B.paths} paths hit`;
          over.append(K.txt(x0 + 6, y1 + 10, t, { anchor: 'start', cls: 'cvb-strong', halo: true }));
        }
      },
      methods: (R) => ({
        /* Re-sample: the next run of the seeded generator. */
        run: () => R.inst.set({ run: Math.round(R.state.run || 0) + 1 }),
        paths: () => build(R.state).out.map((a) => Array.from(a)),
        hits: () => { const B = build(R.state), bar = barriers(B.p); return B.out.map((a) => firstHit(a, bar)); },
      }),
    };
    return K.make(host, params, ctx, def);
  });
})();
