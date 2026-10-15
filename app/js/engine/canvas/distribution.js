/* distribution: pmf bars or pdf curve for a named family, with a shaded probability, mean and sd markers.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js). */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  const pick = (p, names, d) => { for (const n of names) if (p && p[n] != null && Number.isFinite(+p[n])) return +p[n]; return d; };
  /* Each family: discrete flag, pmf/pdf, cdf, mean, sd, default x range, tex name */
  const family = (name, p, K) => {
    switch (name) {
      case 'binomial': {
        const n = Math.max(0, Math.round(pick(p, ['n'], 10))), q = K.clamp(pick(p, ['p'], 0.5), 0, 1);
        const lc = (k) => K.lgamma(n + 1) - K.lgamma(k + 1) - K.lgamma(n - k + 1);
        const f = (k) => (k < 0 || k > n || k !== Math.round(k) ? 0 : q === 0 ? +(k === 0) : q === 1 ? +(k === n) : Math.exp(lc(k) + k * Math.log(q) + (n - k) * Math.log(1 - q)));
        return { discrete: true, f, lo: 0, hi: n, mean: n * q, sd: Math.sqrt(n * q * (1 - q)), range: [-0.5, n + 0.5], tex: `\\text{Bin}(${n}, ${K.fmt(q, 3)})` };
      }
      case 'geometric': {
        const q = K.clamp(pick(p, ['p'], 0.3), 1e-6, 1);
        const f = (k) => (k < 1 || k !== Math.round(k) ? 0 : Math.pow(1 - q, k - 1) * q);
        const hi = Math.max(5, Math.ceil(Math.log(0.005) / Math.log(Math.max(1e-9, 1 - q))));
        return { discrete: true, f, lo: 1, hi, mean: 1 / q, sd: Math.sqrt(1 - q) / q, range: [0.5, Math.min(hi, 60) + 0.5], tex: `\\text{Geo}(${K.fmt(q, 3)})` };
      }
      case 'poisson': {
        const l = Math.max(1e-9, pick(p, ['lambda', 'λ', 'mu', 'rate'], 3));
        const f = (k) => (k < 0 || k !== Math.round(k) ? 0 : Math.exp(k * Math.log(l) - l - K.lgamma(k + 1)));
        const hi = Math.ceil(l + 4.5 * Math.sqrt(l) + 3);
        return { discrete: true, f, lo: 0, hi, mean: l, sd: Math.sqrt(l), range: [-0.5, hi + 0.5], tex: `\\text{Pois}(${K.fmt(l, 3)})` };
      }
      case 'uniform': {
        let a = pick(p, ['a', 'min'], 0), b = pick(p, ['b', 'max'], 1); if (b <= a) b = a + 1e-6;
        const f = (x) => (x >= a && x <= b ? 1 / (b - a) : 0), w = b - a;
        return { discrete: false, f, cdf: (x) => K.clamp((x - a) / w, 0, 1), mean: (a + b) / 2, sd: w / Math.sqrt(12), range: [a - w * 0.25, b + w * 0.25], tex: `U(${K.fmt(a, 3)}, ${K.fmt(b, 3)})`, jumps: [a, b] };
      }
      case 'exponential': {
        const l = Math.max(1e-9, pick(p, ['lambda', 'λ', 'rate'], 1));
        return { discrete: false, f: (x) => (x < 0 ? 0 : l * Math.exp(-l * x)), cdf: (x) => (x < 0 ? 0 : 1 - Math.exp(-l * x)), mean: 1 / l, sd: 1 / l, range: [0, 5 / l], tex: `\\text{Exp}(${K.fmt(l, 3)})`, jumps: [0] };
      }
      case 't': {
        const v = Math.max(0.1, pick(p, ['nu', 'ν', 'df'], 5));
        const c = Math.exp(K.lgamma((v + 1) / 2) - K.lgamma(v / 2)) / Math.sqrt(v * Math.PI);
        const f = (x) => c * Math.pow(1 + x * x / v, -(v + 1) / 2);
        const cdf = (x) => 0.5 + Math.sign(x) * K.simpson(f, 0, Math.abs(x), 600);
        return { discrete: false, f, cdf, mean: v > 1 ? 0 : NaN, sd: v > 2 ? Math.sqrt(v / (v - 2)) : NaN, range: [-5, 5], tex: `t_{${K.fmt(v, 2)}}` };
      }
      case 'normal': default: {
        const mu = pick(p, ['mu', 'μ', 'mean'], 0), s = Math.max(1e-9, pick(p, ['sigma', 'σ', 'sd'], 1));
        return { discrete: false, f: (x) => Math.exp(-0.5 * ((x - mu) / s) ** 2) / (s * Math.sqrt(2 * Math.PI)), cdf: (x) => 0.5 * (1 + K.erf((x - mu) / (s * Math.SQRT2))), mean: mu, sd: s, range: [mu - 4 * s, mu + 4 * s], tex: `N(${K.fmt(mu, 3)}, ${K.fmt(s, 3)}^2)` };
      }
    }
  };

  C.register('distribution', (host, params, ctx) => {
    const K = Z.cvb;
    const W = 540, H = params.height || 300;
    const famName = params.family || 'normal';
    const fam = (view) => family(view.family || famName, { ...(params.params || {}), ...(view.params || {}) }, K);
    let seenPeak = 0, seenRange = null;

    const prob = (F, from, to) => {
      const lo = from == null ? -Infinity : +from, hi = to == null ? Infinity : +to;
      if (F.discrete) { let s = 0; for (let k = Math.max(F.lo, Math.ceil(lo - 1e-9)); k <= Math.min(F.hi + 200, Math.floor(hi + 1e-9)); k++) s += F.f(k); return Math.min(1, s); }
      return K.clamp((hi === Infinity ? 1 : F.cdf(hi)) - (lo === -Infinity ? 0 : F.cdf(lo)), 0, 1);
    };
    const probTex = (F, from, to, v) => {
      const X = params.variable || 'X', le = '\\le ';
      const lhs = from == null && to == null ? 'P(\\text{all})' : from == null ? `P(${X} ${le}${K.fmt(to, 3)})` : to == null ? `P(${X} \\ge ${K.fmt(from, 3)})` : (F.discrete && Math.round(from) === Math.round(to)) ? `P(${X} = ${K.fmt(from, 0)})` : `P(${K.fmt(from, 3)} ${le}${X} ${le}${K.fmt(to, 3)})`;
      return `$${lhs} = ${K.fmt(v, params.dp ?? 4)}$`;
    };
    const geom = (view) => {
      const F = fam(view);
      let range = params.x || F.range;
      if (!params.x) { seenRange = seenRange ? [Math.min(seenRange[0], range[0]), Math.max(seenRange[1], range[1])] : range.slice(); range = view._range || seenRange; }
      let peak = 0;
      if (F.discrete) for (let k = Math.max(F.lo, Math.ceil(range[0])); k <= Math.min(F.hi, Math.floor(range[1])); k++) peak = Math.max(peak, F.f(k));
      else for (let i = 0; i <= 200; i++) { const v = F.f(range[0] + (range[1] - range[0]) * i / 200); if (Number.isFinite(v)) peak = Math.max(peak, v); }
      for (const o of [].concat(view.overlay || [])) { const G = family(o.family, o.params, K); for (let i = 0; i <= 200; i++) { const v = G.f(G.discrete ? Math.round(range[0] + (range[1] - range[0]) * i / 200) : range[0] + (range[1] - range[0]) * i / 200); if (Number.isFinite(v)) peak = Math.max(peak, v); } }
      seenPeak = Math.max(seenPeak, Math.min(peak, 50));
      const yMax = params.yMax || (() => { const t = C.niceTicks(0, seenPeak * 1.18, 5); return t[t.length - 1] >= seenPeak * 1.12 ? t[t.length - 1] : seenPeak * 1.2; })();
      const ml = K.yMargin(0, yMax, H - 60), mt = 26, mb = params.xLabel ? 46 : 30, mr = 14;
      return { F, range, yMax, ml, mt, mb, mr, sx: C.scale(range, [ml, W - mr]), sy: C.scale([0, yMax], [H - mb, mt]) };
    };

    const def = {
      kind: 'distribution', aria: params.aria || 'Probability distribution',
      modes: ['drag', 'slider'],
      size: () => ({ w: W, h: H }),
      init: () => ({ shade: null, params: {}, highlight: [], showMean: params.showMean ?? false, showSd: params.showSd ?? false }),
      render(view, R) {
        const { F, range, yMax, sx, sy, ml, mr } = geom(view);
        const g = R.F.g, x0 = ml, x1 = W - mr, base = sy(0), top = sy(yMax);
        const xt = K.ticksFor(range[0], range[1], x1 - x0, { minGap: 44 });
        if (F.discrete && xt.step < 1) { xt.ticks = C.niceTicks(range[0], range[1], Math.max(2, Math.floor((range[1] - range[0])))).filter((v) => Number.isInteger(v)); xt.step = 1; }
        if (F.discrete) xt.ticks = xt.ticks.filter((v) => Number.isInteger(v));
        K.chartAxes(g, sx, sy, { yLabel: params.yLabel ?? (F.discrete ? 'Probability' : 'Density'), xLabel: params.xLabel, xTicks: xt });
        const clip = R.clipRect(x0, top - 2, x1 - x0, base - top + 4);
        const plot = svg('g', { 'clip-path': clip }); g.append(plot);
        const over = svg('g'); g.append(over);
        const sh = view.shade, hasShade = sh && (sh.from != null || sh.to != null);
        const lo = hasShade && sh.from != null ? +sh.from : -Infinity, hi = hasShade && sh.to != null ? +sh.to : Infinity;
        let shadeTopY = base, shadeMid = null;

        if (F.discrete) {
          const unit = sx(1) - sx(0), bw = Math.max(2, Math.min(40, unit * 0.72));
          for (let k = Math.max(F.lo, Math.ceil(range[0])); k <= Math.min(F.hi, Math.floor(range[1])); k++) {
            const v = F.f(k), y = sy(v), cx = sx(k), on = !hasShade || (k >= lo - 1e-9 && k <= hi + 1e-9);
            const o = K.obj('x' + k, '', params.colour || 1);
            o.append(K.washRect(cx - bw / 2 - 3, top, bw + 6, base - top, 3), svg('rect', { x: cx - bw / 2, y, width: bw, height: Math.max(0, base - y), rx: 1.5, class: 'cvb-bar' + (on ? ' on' : '') }));
            plot.append(o);
            if (params.showValues && unit > 34) over.append(K.txt(cx, y - 9, K.fmt(v, 3), { size: 11, cls: 'cvb-muted' }));
            if (hasShade && on) { shadeTopY = Math.min(shadeTopY, y); shadeMid = shadeMid == null ? [cx, cx] : [Math.min(shadeMid[0], cx), Math.max(shadeMid[1], cx)]; }
          }
          if (hasShade) { const o = K.obj('shade', '', params.colour || 1); o.append(K.washRect(sx(Math.max(lo, range[0]) - 0.5), top, sx(Math.min(hi, range[1]) + 0.5) - sx(Math.max(lo, range[0]) - 0.5), base - top, 2)); plot.insertBefore(o, plot.firstChild); }
        } else {
          const n = Math.ceil((x1 - x0) * 1.5), pts = [];
          for (let i = 0; i <= n; i++) { const x = range[0] + (range[1] - range[0]) * i / n; pts.push([sx(x), sy(F.f(x))]); }
          if (hasShade) {
            const a = Math.max(lo, range[0]), b = Math.min(hi, range[1]);
            if (b > a) {
              const m = Math.max(2, Math.ceil(sx(b) - sx(a))), ar = [];
              for (let i = 0; i <= m; i++) { const x = a + (b - a) * i / m; const y = sy(F.f(x)); ar.push([sx(x), y]); shadeTopY = Math.min(shadeTopY, y); }
              const d = `M${sx(a)},${base}` + ar.map((p) => `L${p[0].toFixed(2)},${p[1].toFixed(2)}`).join('') + `L${sx(b)},${base}Z`;
              const o = K.obj('shade', '', params.colour || 1);
              o.append(svg('path', { d, class: 'cvb-hlw' }), svg('path', { d, class: 'cvb-wash-f' }));
              if (lo > range[0]) o.append(svg('line', { x1: sx(a), x2: sx(a), y1: base, y2: sy(F.f(a)), class: 'cvb-ln thin' }));
              if (hi < range[1]) o.append(svg('line', { x1: sx(b), x2: sx(b), y1: base, y2: sy(F.f(b)), class: 'cvb-ln thin' }));
              plot.append(o); shadeMid = [sx(a), sx(b)];
            }
          }
          const d = 'M' + pts.map((p) => p[0].toFixed(2) + ',' + p[1].toFixed(2)).join('L');
          const o = K.obj('curve', '', params.colour || 1); o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln' })); plot.append(o);
        }

        /* Overlays: dashed comparison curves in the next series slots */
        [].concat(view.overlay || []).forEach((ov, j) => {
          const G = family(ov.family, ov.params, K), slot = ov.colour || j + 2, o = K.obj(ov.id || 'overlay' + j, '', slot);
          let d = '';
          if (G.discrete) { const ks = []; for (let k = Math.max(G.lo, Math.ceil(range[0])); k <= Math.min(G.hi, Math.floor(range[1])); k++) ks.push(k); d = 'M' + ks.map((k) => sx(k).toFixed(2) + ',' + sy(G.f(k)).toFixed(2)).join('L'); ks.forEach((k) => o.append(svg('circle', { cx: sx(k), cy: sy(G.f(k)), r: 3, class: 'cvb-dot' }))); }
          else { const n = Math.ceil(x1 - x0); d = 'M' + Array.from({ length: n + 1 }, (_, i) => { const x = range[0] + (range[1] - range[0]) * i / n; return sx(x).toFixed(2) + ',' + sy(G.f(x)).toFixed(2); }).join('L'); }
          o.prepend(K.washPath(d), svg('path', { d, class: 'cvb-ln cvb-dash' })); plot.append(o);
          if (ov.label) { const xe = range[0] + (range[1] - range[0]) * 0.8; over.append(K.lab(sx(xe) + 6, sy(G.f(G.discrete ? Math.round(xe) : xe)) - 12, ov.label, { anchor: 'start', halo: true, cls: 'cvb-strong' })); }
        });

        /* Mean marker and sd bracket */
        const showMean = view.showMean ?? params.showMean, showSd = view.showSd ?? params.showSd;
        if (showMean && Number.isFinite(F.mean) && F.mean >= range[0] && F.mean <= range[1]) {
          const o = K.obj('mean', '', 'ink'), x = sx(F.mean);
          o.append(K.washPath(`M${x},${base}L${x},${top + 14}`), svg('line', { x1: x, x2: x, y1: base, y2: top + 14, class: 'cvb-ln thin cvb-dash' }));
          o.append(K.lab(x + 4, top + 4, `$\\mu = ${K.fmt(F.mean, 3)}$`, { anchor: 'start', halo: true }));
          over.append(o);
        }
        if (showSd && Number.isFinite(F.sd) && Number.isFinite(F.mean)) {
          const y = top + 34, a = sx(F.mean - F.sd), b = sx(F.mean + F.sd), o = K.obj('sd', '', 'ink');
          o.append(K.washPath(`M${a},${y}L${b},${y}`), svg('path', { d: `M${a},${y - 5}L${a},${y + 5}M${a},${y}L${b},${y}M${b},${y - 5}L${b},${y + 5}`, class: 'cvb-ln thin' }));
          o.append(K.lab(b + 6, y, `$\\pm\\sigma = ${K.fmt(F.sd, 3)}$`, { anchor: 'start', halo: true }));
          over.append(o);
        }

        /* Shaded probability label */
        if (hasShade && shadeMid && view.showProb !== false) {
          const v = prob(F, sh.from, sh.to), text = view.probLabel || probTex(F, sh.from, sh.to, v);
          const cx = (shadeMid[0] + shadeMid[1]) / 2, w = K.tw(text.replace(/\\le|\\ge/g, '<')) + 30;
          const lx = K.clamp(cx, x0 + w / 2, x1 - w / 2), ly = Math.max(top + (showMean ? 60 : 12), shadeTopY - 18);
          const o = K.obj('prob', 'cvb-prob'); o.append(K.lab(lx, ly, text, { halo: true, w: w + 20, cls: 'cvb-strong' })); over.append(o);
        }

        /* Drag handles on the shade bounds */
        if (hasShade && R.active('drag')) {
          if (sh.from != null && sh.from >= range[0] - 0.5) over.append(K.handle(sx(+sh.from + (F.discrete ? -0.5 : 0)), base, 'from', { r: 7, shape: 'diamond', label: 'Lower bound' }));
          if (sh.to != null && sh.to <= range[1] + 0.5) over.append(K.handle(sx(+sh.to + (F.discrete ? 0.5 : 0)), base, 'to', { r: 7, shape: 'diamond', label: 'Upper bound' }));
        }
      },
      drag: {
        start: (id, p, R) => (R.active('drag') && R.state.shade ? { id } : null),
        move(info, p, R, end) {
          const { F, sx, range } = geom(R.state);
          let v = sx.invert(p.x) + (F.discrete ? (info.id === 'from' ? 0.5 : -0.5) : 0);
          v = F.discrete ? Math.round(v) : K.round(K.snapTo(v, params.snap || 0.01), 6);
          setBound(R, info.id, K.clamp(v, Math.floor(range[0]), Math.ceil(range[1])), end);
        },
        key(id, dx, dy, R) { const st = fam(R.state).discrete ? 1 : (params.snap || 0.1); setBound(R, id, +R.state.shade[id] + (dx || dy) * st, true); },
      },
      methods: (R) => ({
        /* Probability of the current shade, or of [from, to] if given. */
        probability: (from, to) => { const F = fam(R.state); return from !== undefined || to !== undefined ? prob(F, from, to) : R.state.shade ? prob(F, R.state.shade.from, R.state.shade.to) : 1; },
        stats: () => { const F = fam(R.state); return { mean: F.mean, sd: F.sd }; },
        points: () => { const s = R.state.shade || {}; const o = {}; if (s.from != null) o.from = { x: s.from, y: 0 }; if (s.to != null) o.to = { x: s.to, y: 0 }; return o; },
        place: (id, pos, opts = {}) => R.inst.set({ shade: { [id]: Array.isArray(pos) ? pos[0] : pos } }, opts),
      }),
    };
    const setBound = (R, id, v, end) => {
      const s = { ...R.state.shade };
      if (id === 'from' && s.to != null) v = Math.min(v, s.to);
      if (id === 'to' && s.from != null) v = Math.max(v, s.from);
      s[id] = v;
      R.commit({ shade: s });
      R.emit({ type: 'drag', id, x: v, y: 0, from: s.from, to: s.to, phase: end ? 'end' : 'move' });
    };
    return K.make(host, params, ctx, def);
  });
})();
