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
        return { discrete: true, f, lo: 0, hi: n, mean: n * q, sd: Math.sqrt(n * q * (1 - q)), range: [-0.8, n + 0.8], tex: `\\text{Bin}(${n}, ${K.fmt(q, 3)})` };
      }
      case 'geometric': {
        const q = K.clamp(pick(p, ['p'], 0.3), 1e-6, 1);
        const f = (k) => (k < 1 || k !== Math.round(k) ? 0 : Math.pow(1 - q, k - 1) * q);
        const hi = Math.max(5, Math.ceil(Math.log(0.005) / Math.log(Math.max(1e-9, 1 - q))));
        return { discrete: true, f, lo: 1, hi, mean: 1 / q, sd: Math.sqrt(1 - q) / q, range: [0.2, Math.min(hi, 60) + 0.8], tex: `\\text{Geo}(${K.fmt(q, 3)})` };
      }
      case 'poisson': {
        const l = Math.max(1e-9, pick(p, ['lambda', 'λ', 'mu', 'rate'], 3));
        const f = (k) => (k < 0 || k !== Math.round(k) ? 0 : Math.exp(k * Math.log(l) - l - K.lgamma(k + 1)));
        const hi = Math.ceil(l + 4.5 * Math.sqrt(l) + 3);
        return { discrete: true, f, lo: 0, hi, mean: l, sd: Math.sqrt(l), range: [-0.8, hi + 0.8], tex: `\\text{Pois}(${K.fmt(l, 3)})` };
      }
      case 'uniform': {
        let a = pick(p, ['a', 'min'], 0), b = pick(p, ['b', 'max'], 1); if (b <= a) b = a + 1e-6;
        const f = (x) => (x >= a && x <= b ? 1 / (b - a) : 0), w = b - a;
        return { discrete: false, f, cdf: (x) => K.clamp((x - a) / w, 0, 1), mean: (a + b) / 2, median: (a + b) / 2, sd: w / Math.sqrt(12), range: [a - w * 0.25, b + w * 0.25], tex: `U(${K.fmt(a, 3)}, ${K.fmt(b, 3)})`, jumps: [a, b] };
      }
      case 'exponential': {
        const l = Math.max(1e-9, pick(p, ['lambda', 'λ', 'rate'], 1));
        return { discrete: false, f: (x) => (x < 0 ? 0 : l * Math.exp(-l * x)), cdf: (x) => (x < 0 ? 0 : 1 - Math.exp(-l * x)), mean: 1 / l, median: Math.LN2 / l, sd: 1 / l, range: [0, 5 / l], tex: `\\text{Exp}(${K.fmt(l, 3)})`, jumps: [0] };
      }
      case 't': {
        const v = Math.max(0.1, pick(p, ['nu', 'ν', 'df'], 5));
        const c = Math.exp(K.lgamma((v + 1) / 2) - K.lgamma(v / 2)) / Math.sqrt(v * Math.PI);
        const f = (x) => c * Math.pow(1 + x * x / v, -(v + 1) / 2);
        const cdf = (x) => 0.5 + Math.sign(x) * K.simpson(f, 0, Math.abs(x), 600);
        return { discrete: false, f, cdf, mean: v > 1 ? 0 : NaN, sd: v > 2 ? Math.sqrt(v / (v - 2)) : NaN, range: [-5, 5], tex: `t_{${K.fmt(v, 2)}}` };
      }
      case 'hypergeometric': { // item 300: N items, K successes among them, n drawn without replacement
        const N = Math.max(1, Math.round(pick(p, ['N', 'population'], 20))), Ks = K.clamp(Math.round(pick(p, ['K', 'successes'], 7)), 0, N), n = K.clamp(Math.round(pick(p, ['n', 'draws'], 5)), 0, N);
        const lc = (a, b) => (b < 0 || b > a ? -Infinity : K.lgamma(a + 1) - K.lgamma(b + 1) - K.lgamma(a - b + 1));
        const lo = Math.max(0, n - (N - Ks)), hi = Math.min(n, Ks);
        const f = (k) => (k < lo || k > hi || k !== Math.round(k) ? 0 : Math.exp(lc(Ks, k) + lc(N - Ks, n - k) - lc(N, n)));
        const mean = n * Ks / N, v = N > 1 ? n * (Ks / N) * ((N - Ks) / N) * ((N - n) / (N - 1)) : 0;
        return { discrete: true, f, lo, hi, mean, sd: Math.sqrt(v), range: [lo - 0.8, hi + 0.8], tex: `\\text{Hyp}(${N}, ${Ks}, ${n})` };
      }
      case 'discrete': case 'custom': { // item 291: a custom support, values with their probabilities
        const xs = (p && Array.isArray(p.values) ? p.values : [0, 1]).map(Number), ps = (p && Array.isArray(p.probs) ? p.probs : xs.map(() => 1 / xs.length)).map(Number);
        const pairs = xs.map((x, i) => [x, Number.isFinite(ps[i]) ? ps[i] : 0]).filter(([x]) => Number.isFinite(x)).sort((u, w) => u[0] - w[0]);
        const f = (x) => pairs.reduce((t, [v, q]) => t + (Math.abs(v - x) < 1e-9 ? q : 0), 0);
        const mean = pairs.reduce((t, [v, q]) => t + v * q, 0), v2 = pairs.reduce((t, [v, q]) => t + q * (v - mean) ** 2, 0);
        const lo = pairs.length ? pairs[0][0] : 0, hi = pairs.length ? pairs[pairs.length - 1][0] : 1, gap = Math.max(1e-9, Math.min(1, ...pairs.slice(1).map(([v], i) => v - pairs[i][0]).filter((d) => d > 1e-9)));
        return { discrete: true, f, lo, hi, support: [...new Set(pairs.map(([v]) => v))], gap, mean, sd: Math.sqrt(v2), range: [lo - 0.8 * gap, hi + 0.8 * gap], tex: 'X' };
      }
      case 'beta': { // item 344: Beta(a, b) on [0, 1], for posteriors and credible intervals
        const a = Math.max(1e-3, pick(p, ['a', 'alpha', 'α'], 2)), b = Math.max(1e-3, pick(p, ['b', 'beta', 'β'], 2));
        const lB = K.lgamma(a) + K.lgamma(b) - K.lgamma(a + b);
        const f = (x) => (x <= 0 || x >= 1 ? (x === 0 && a === 1 ? Math.exp(-lB) : x === 1 && b === 1 ? Math.exp(-lB) : 0) : Math.exp((a - 1) * Math.log(x) + (b - 1) * Math.log(1 - x) - lB));
        const cdf = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : K.clamp(K.simpson(f, 1e-9, x, 800), 0, 1));
        const mean = a / (a + b), v = a * b / ((a + b) ** 2 * (a + b + 1));
        return { discrete: false, f, cdf, mean, median: a > 1 && b > 1 ? (a - 1 / 3) / (a + b - 2 / 3) : NaN, sd: Math.sqrt(v), range: [0, 1], tex: `\text{Beta}(${K.fmt(a, 3)}, ${K.fmt(b, 3)})`, jumps: [0, 1] };
      }
      case 'lognormal': { // item 305: log X ~ N(mu, sigma^2)
        const mu = pick(p, ['mu', 'μ'], 0), s = Math.max(1e-9, pick(p, ['sigma', 'σ'], 0.5));
        const f = (x) => (x <= 0 ? 0 : Math.exp(-0.5 * ((Math.log(x) - mu) / s) ** 2) / (x * s * Math.sqrt(2 * Math.PI)));
        const mean = Math.exp(mu + s * s / 2);
        return { discrete: false, f, cdf: (x) => (x <= 0 ? 0 : 0.5 * (1 + K.erf((Math.log(x) - mu) / (s * Math.SQRT2)))), mean, median: Math.exp(mu), sd: Math.sqrt(Math.expm1(s * s)) * mean, range: [0, Math.exp(mu + 2.6 * s)], tex: `\\text{LogN}(${K.fmt(mu, 3)}, ${K.fmt(s, 3)}^2)`, jumps: [0] };
      }
      case 'normal': default: {
        const mu = pick(p, ['mu', 'μ', 'mean'], 0), s = Math.max(1e-9, pick(p, ['sigma', 'σ', 'sd'], 1));
        return { discrete: false, f: (x) => Math.exp(-0.5 * ((x - mu) / s) ** 2) / (s * Math.sqrt(2 * Math.PI)), cdf: (x) => 0.5 * (1 + K.erf((x - mu) / (s * Math.SQRT2))), mean: mu, median: mu, sd: s, range: [mu - 4 * s, mu + 4 * s], tex: `N(${K.fmt(mu, 3)}, ${K.fmt(s, 3)}^2)` };
      }
    }
  };

  /* the support points of a discrete family within [a, b] (integers lo..hi, or a custom list) */
  const supportIn = (F, a, b) => (F.support ? F.support.filter((x) => x >= a - 1e-9 && x <= b + 1e-9) : (() => { const out = []; for (let k = Math.max(F.lo, Math.ceil(a - 1e-9)); k <= Math.min(F.hi, Math.floor(b + 1e-9), F.lo + 2000); k++) out.push(k); return out; })());

  C.register('distribution', (host, params, ctx) => {
    const K = Z.cvb;
    const W = 540, H = params.height || 300;
    const famName = params.family || 'normal';
    const P0 = (view) => ({ ...(params.params || {}), ...(view.params || {}) });
    /* item 291: a custom discrete support may come straight from params (values, probs) */
    const fam = (view) => { const P = P0(view); if (!P.values && params.values) { P.values = params.values; P.probs = params.probs; } return family(view.family || famName, P, K); };
    /* an expression in the family's params ("mu + sigma", "n * p"), or a number */
    const num = (v, P) => { if (v == null || v === '') return null; if (typeof v === 'number') return v; const n = Number(v); if (Number.isFinite(n)) return n; try { const r = K.fnOf(String(v), Object.keys(P))(0, P); return Number.isFinite(r) ? r : null; } catch { return null; } };
    /* items 308, 325: an overlay's params may be expressions in the main params, so it follows the sliders */
    const ovFam = (ov, view) => { const P = P0(view), q = {}; for (const [k, v] of Object.entries(ov.params || {})) q[k] = typeof v === 'string' && !Number.isFinite(Number(v)) ? num(v, P) : v; return family(ov.family, { ...q, values: (ov.params || {}).values, probs: (ov.params || {}).probs }, K); };
    /* items 305, 320, 330: shade is one region or a list; bounds may be expressions; under: "<overlay id>" shades that curve */
    const shadesOf = (view) => { const P = P0(view); return [].concat(view.shade || []).filter((x) => x && typeof x === 'object').map((x, i) => ({ ...x, id: x.id || (i ? 'shade' + i : 'shade'), from: num(x.from, P), to: num(x.to, P) })).filter((x) => x.from != null || x.to != null); };
    let seenPeak = 0, seenRange = null, lastKey = null;

    const prob = (F, from, to) => {
      const lo = from == null ? -Infinity : +from, hi = to == null ? Infinity : +to;
      if (F.discrete) { let s = 0; for (const k of supportIn(F, Math.max(lo, F.lo), Math.min(hi, F.hi))) s += F.f(k); return Math.min(1, s); }
      return K.clamp((hi === Infinity ? 1 : F.cdf(hi)) - (lo === -Infinity ? 0 : F.cdf(lo)), 0, 1);
    };
    const lhsTex = (F, from, to) => {
      const X = params.variable || 'X', le = '\\le ';
      return from == null && to == null ? 'P(\\text{all})' : from == null ? `P(${X} ${le}${K.fmt(to, 3)})` : to == null ? `P(${X} \\ge ${K.fmt(from, 3)})` : (F.discrete && Math.abs(from - to) < 1e-9) ? `P(${X} = ${K.fmt(from, 3)})` : `P(${K.fmt(from, 3)} ${le}${X} ${le}${K.fmt(to, 3)})`;
    };
    const geom = (view) => {
      const F = fam(view), cdfMode = !!(view.cdf ?? params.cdf);
      /* item 299: a discrete family's axes follow its support as a slider moves n (axes: "grow" keeps the old way);
         continuous axes only grow, so shapes can be compared (axes: "follow" to track them) */
      const follow = (params.axes || (F.discrete ? 'follow' : 'grow')) === 'follow';
      let range = params.x || F.range;
      if (!params.x && !follow) { seenRange = seenRange ? [Math.min(seenRange[0], range[0]), Math.max(seenRange[1], range[1])] : range.slice(); range = view._range || seenRange; }
      let peak = 0;
      if (F.discrete) for (const k of supportIn(F, range[0], range[1])) peak = Math.max(peak, F.f(k));
      else for (let i = 0; i <= 200; i++) { const v = F.f(range[0] + (range[1] - range[0]) * i / 200); if (Number.isFinite(v)) peak = Math.max(peak, v); }
      for (const o of [].concat(view.overlay || [])) { const G = ovFam(o, view); if (G.discrete) { for (const k of supportIn(G, range[0], range[1])) peak = Math.max(peak, G.f(k)); } else for (let i = 0; i <= 200; i++) { const v = G.f(range[0] + (range[1] - range[0]) * i / 200); if (Number.isFinite(v)) peak = Math.max(peak, v); } }
      const key = JSON.stringify([range, F.discrete]);
      seenPeak = follow ? (key === lastKey ? Math.max(seenPeak, peak) : peak) : Math.max(seenPeak, Math.min(peak, 50)); lastKey = key;
      const yMax = cdfMode ? 1.08 : params.yMax || (() => { const t = C.niceTicks(0, seenPeak * 1.18, 5); return t[t.length - 1] >= seenPeak * 1.12 ? t[t.length - 1] : seenPeak * 1.2; })();
      const ml = K.yMargin(0, yMax, H - 60), mt = 26, mb = params.xLabel ? 46 : 30, mr = 14;
      return { F, cdfMode, range, yMax, ml, mt, mb, mr, sx: C.scale(range, [ml, W - mr]), sy: C.scale([0, yMax], [H - mb, mt]) };
    };
    /* item 299: on a discrete support every integer gets a tick when there is room, else every 2nd, 5th, 10th... */
    const discreteTicks = (F, range, sx) => {
      const unitPx = sx(1) - sx(0), lw = K.tw(String(Math.round(Math.max(Math.abs(range[0]), Math.abs(range[1]))))) + 12;
      if (F.support && !F.support.every(Number.isInteger)) {
        const sp = supportIn(F, range[0], range[1]), gaps = sp.slice(1).map((v, i) => sx(v) - sx(sp[i]));
        const dp = Math.max(0, ...sp.map((v) => (String(+v.toFixed(6)).split('.')[1] || '').length));
        if (sp.length && (!gaps.length || Math.min(...gaps) >= Math.max(...sp.map((v) => K.tw(K.fmt(v, 3)))) + 8)) return { ticks: sp, step: 10 ** -dp };
        return null;
      }
      const steps = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000];
      const step = steps.find((st) => st * unitPx >= lw) || 1000, ticks = [];
      for (let v = Math.ceil(range[0] / step) * step; v <= range[1] + 1e-9; v += step) ticks.push(Math.round(v));
      return { ticks, step };
    };

    const def = {
      kind: 'distribution', aria: params.aria || 'Probability distribution',
      modes: ['drag', 'slider'],
      size: () => ({ w: W, h: H }),
      listKeys: ['overlay'],
      init: () => ({ shade: null, params: { ...(params.params || {}) }, highlight: [], showMean: params.showMean ?? false, showSd: params.showSd ?? false, overlay: params.overlay || [], observed: null, rug: null }),
      render(view, R) {
        const { F, cdfMode, range, yMax, sx, sy, ml, mr } = geom(view);
        const g = R.F.g, x0 = ml, x1 = W - mr, base = sy(0), top = sy(yMax);
        let xt = K.ticksFor(range[0], range[1], x1 - x0, { minGap: 44 });
        if (F.discrete) { const dt = discreteTicks(F, range, sx); if (dt) xt = dt; }
        K.chartAxes(g, sx, sy, { yLabel: params.yLabel ?? (cdfMode ? `P(${params.variable || 'X'} ≤ x)` : F.discrete ? 'Probability' : 'Density'), xLabel: params.xLabel, xTicks: xt });
        const clip = R.clipRect(x0, top - 2, x1 - x0, base - top + 4);
        const plot = svg('g', { 'clip-path': clip }); g.append(plot);
        const over = svg('g'); g.append(over);
        const P = P0(view), shades = cdfMode ? [] : shadesOf(view), mainShades = shades.filter((x) => !x.under), hasShade = mainShades.length > 0;
        const inShade = (x) => mainShades.some((q) => x >= (q.from ?? -Infinity) - 1e-9 && x <= (q.to ?? Infinity) + 1e-9);
        const shadeOf = (x) => mainShades.find((q) => x >= (q.from ?? -Infinity) - 1e-9 && x <= (q.to ?? Infinity) + 1e-9);
        let shadeMid = null;
        const sup = F.discrete ? supportIn(F, range[0], range[1]) : [];
        const unit = F.discrete ? (sx(F.gap || 1) - sx(0)) : 0;

        if (cdfMode) {
          /* item 291: the CDF as steps (closed dot where a step lands, open dot where it leaves) or as a curve */
          const o = K.obj('cdf', '', params.colour || 1);
          if (F.discrete) {
            const all = supportIn(F, F.lo, F.hi); let cum = 0, prevX = range[0], prevY = 0;
            const pts = all.map((x) => { cum += F.f(x); return [x, Math.min(1, cum)]; });
            pts.forEach(([x, y], i) => {
              if (x > range[1] + 1e-9) return;
              o.append(svg('line', { x1: sx(prevX), x2: sx(x), y1: sy(prevY), y2: sy(prevY), class: 'cvb-ln' }));
              if (x >= range[0]) o.append(svg('circle', { cx: sx(x), cy: sy(prevY), r: 4, class: 'cvb-dot open' }), svg('circle', { cx: sx(x), cy: sy(y), r: 4, class: 'cvb-dot' }));
              prevX = x; prevY = y;
              if (i === pts.length - 1) o.append(svg('line', { x1: sx(x), x2: sx(range[1]), y1: sy(y), y2: sy(y), class: 'cvb-ln' }));
            });
          } else {
            const n = Math.ceil((x1 - x0) * 1.5); const d = 'M' + Array.from({ length: n + 1 }, (_, i) => { const x = range[0] + (range[1] - range[0]) * i / n; return sx(x).toFixed(2) + ',' + sy(F.cdf(x)).toFixed(2); }).join('L');
            o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln' }));
          }
          plot.append(o);
        } else if (F.discrete) {
          const bw = Math.max(2, Math.min(40, unit * 0.72));
          for (const k of sup) {
            const v = F.f(k), y = sy(v), cx = sx(k), on = !hasShade || inShade(k), q = shadeOf(k);
            const o = K.obj('x' + k, '', (q && q.colour) || params.colour || 1);
            o.append(K.washRect(cx - bw / 2 - 3, top, bw + 6, base - top, 3), svg('rect', { x: cx - bw / 2, y, width: bw, height: Math.max(0, base - y), rx: 1.5, class: 'cvb-bar' + (on ? ' on' : '') }));
            plot.append(o);
            if (params.showValues && unit > 34) over.append(K.txt(cx, y - 9, K.fmt(v, 3), { size: 11, cls: 'cvb-muted' }));
            if (hasShade && on) shadeMid = shadeMid == null ? [cx, cx] : [Math.min(shadeMid[0], cx), Math.max(shadeMid[1], cx)];
          }
          const half = (F.gap || 1) / 2;
          mainShades.forEach((q) => { const a = Math.max(q.from ?? -Infinity, range[0] + half), b = Math.min(q.to ?? Infinity, range[1] - half); if (b < a - 1e-9) return; const o = K.obj(q.id, '', q.colour || params.colour || 1); o.append(K.washRect(sx(a - half), top, sx(b + half) - sx(a - half), base - top, 2)); plot.insertBefore(o, plot.firstChild); });
        } else {
          const n = Math.ceil((x1 - x0) * 1.5), pts = [];
          for (let i = 0; i <= n; i++) { const x = range[0] + (range[1] - range[0]) * i / n; pts.push([sx(x), sy(F.f(x))]); }
          mainShades.forEach((q) => {
            const lo = q.from ?? -Infinity, hi = q.to ?? Infinity, a = Math.max(lo, range[0]), b = Math.min(hi, range[1]);
            if (!(b > a)) return;
            const m = Math.max(2, Math.ceil(sx(b) - sx(a))), ar = [];
            for (let i = 0; i <= m; i++) { const x = a + (b - a) * i / m; ar.push([sx(x), sy(F.f(x))]); }
            const d = `M${sx(a)},${base}` + ar.map((p) => `L${p[0].toFixed(2)},${p[1].toFixed(2)}`).join('') + `L${sx(b)},${base}Z`;
            const o = K.obj(q.id, '', q.colour || params.colour || 1);
            o.append(svg('path', { d, class: 'cvb-hlw' }), svg('path', { d, class: 'cvb-wash-f' }));
            if (lo > range[0]) o.append(svg('line', { x1: sx(a), x2: sx(a), y1: base, y2: sy(F.f(a)), class: 'cvb-ln thin' }));
            if (hi < range[1]) o.append(svg('line', { x1: sx(b), x2: sx(b), y1: base, y2: sy(F.f(b)), class: 'cvb-ln thin' }));
            plot.append(o); shadeMid = shadeMid ? [Math.min(shadeMid[0], sx(a)), Math.max(shadeMid[1], sx(b))] : [sx(a), sx(b)];
          });
          const d = 'M' + pts.map((p) => p[0].toFixed(2) + ',' + p[1].toFixed(2)).join('L');
          const o = K.obj('curve', '', params.colour || 1); o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln' })); plot.append(o);
        }

        /* Overlays: dashed comparison curves in the next series slots; a shade with under: "<overlay id>" fills
           under that curve (a continuity-correction strip, or beta under the alternative) */
        [].concat(view.overlay || []).forEach((ov, j) => {
          if (!ov) return;
          const G = ovFam(ov, view), slot = ov.colour || j + 2, oid = ov.id || 'overlay' + j, o = K.obj(oid, '', slot);
          for (const q of shades.filter((x) => x.under === oid)) {
            const a = Math.max(q.from ?? -Infinity, range[0]), b = Math.min(q.to ?? Infinity, range[1]); if (!(b > a)) continue;
            const m = Math.max(2, Math.ceil(sx(b) - sx(a))), ar = []; for (let i = 0; i <= m; i++) { const x = a + (b - a) * i / m; ar.push([sx(x), sy(G.discrete ? G.f(Math.round(x)) : G.f(x))]); }
            const dd = `M${sx(a)},${base}` + ar.map((p) => `L${p[0].toFixed(2)},${p[1].toFixed(2)}`).join('') + `L${sx(b)},${base}Z`;
            const so = K.obj(q.id, 'cvb-under', q.colour || slot); so.append(svg('path', { d: dd, class: 'cvb-hlw' }), svg('path', { d: dd, class: 'cvb-wash-f cvb-hatch' })); plot.append(so);
            if (q.label) { const v = G.discrete ? prob(G, q.from, q.to) : K.clamp((q.to == null ? 1 : G.cdf(q.to)) - (q.from == null ? 0 : G.cdf(q.from)), 0, 1); const xm = (a + b) / 2; over.append(K.lab(sx(xm), Math.max(top + 10, sy(G.f(G.discrete ? Math.round(xm) : xm)) - 14), String(q.label).replace('{value}', K.fmt(v, params.dp ?? 4)), { halo: true, cls: 'cvb-strong' })); }
          }
          let d = '';
          if (G.discrete) { const ks = supportIn(G, range[0], range[1]); d = 'M' + ks.map((k) => sx(k).toFixed(2) + ',' + sy(G.f(k)).toFixed(2)).join('L'); ks.forEach((k) => o.append(svg('circle', { cx: sx(k), cy: sy(G.f(k)), r: 3, class: 'cvb-dot' }))); }
          else { const n = Math.ceil(x1 - x0); d = 'M' + Array.from({ length: n + 1 }, (_, i) => { const x = range[0] + (range[1] - range[0]) * i / n; return sx(x).toFixed(2) + ',' + sy(cdfMode ? G.cdf(x) : G.f(x)).toFixed(2); }).join('L'); }
          o.prepend(K.washPath(d), svg('path', { d, class: 'cvb-ln' + (ov.dashed === false ? '' : ' cvb-dash') })); plot.append(o);
          if (ov.label) { const xe = range[0] + (range[1] - range[0]) * 0.8; over.append(K.lab(sx(xe) + 6, sy(cdfMode ? G.cdf(xe) : G.f(G.discrete ? Math.round(xe) : xe)) - 12, ov.label, { anchor: 'start', halo: true, cls: 'cvb-strong' })); }
        });

        /* item 317: a data rug, sticks at given x values (sticks: true runs each up to the density, for likelihood pictures) */
        const rug = view.rug ?? params.rug;
        if (rug) {
          const xs = (Array.isArray(rug) ? rug : rug.x || []).map(Number).filter((x) => Number.isFinite(x) && x >= range[0] && x <= range[1]), o = K.obj('rug', 'cvb-rug', (rug && rug.colour) || 'ink');
          xs.forEach((x) => { const yt = rug.sticks ? sy(F.discrete ? F.f(Math.round(x)) : F.f(x)) : base - 9; o.append(svg('line', { x1: sx(x), x2: sx(x), y1: base, y2: yt, class: 'cvb-ln' + (rug.sticks ? '' : ' thin') })); if (rug.sticks) o.append(svg('circle', { cx: sx(x), cy: yt, r: 3, class: 'cvb-dot' })); });
          over.append(o);
        }

        /* Mean, median and sd markers */
        const showMean = view.showMean ?? params.showMean, showSd = view.showSd ?? params.showSd, showMedian = view.showMedian ?? params.showMedian;
        let markTop = top + 4;
        let lastMark = null;
        const vmark = (id, xv, tex) => {
          const o = K.obj(id, '', 'ink'), x = sx(xv); o.append(K.washPath(`M${x},${base}L${x},${top + 14}`), svg('line', { x1: x, x2: x, y1: base, y2: top + 14, class: 'cvb-ln thin cvb-dash' }));
          /* two close markers put their labels on opposite sides of their lines */
          const right = lastMark && Math.abs(x - lastMark.x) < 110 ? lastMark.anchor === 'end' : x <= (x0 + x1) / 2 + 120;
          const anchor = right ? 'start' : 'end', y = lastMark && Math.abs(x - lastMark.x) < 110 && lastMark.anchor !== anchor ? lastMark.y : markTop;
          o.append(K.lab(x + (right ? 4 : -4), y, tex, { anchor, halo: true })); if (y === markTop) markTop += 22; lastMark = { x, anchor, y }; over.append(o);
        };
        if (!cdfMode && showMean && Number.isFinite(F.mean) && F.mean >= range[0] && F.mean <= range[1]) vmark('mean', F.mean, `$\\mu = ${K.fmt(F.mean, 3)}$`);
        if (!cdfMode && showMedian && Number.isFinite(F.median) && F.median >= range[0] && F.median <= range[1]) vmark('median', F.median, `$\\text{median} = ${K.fmt(F.median, 3)}$`);
        if (!cdfMode && showSd && Number.isFinite(F.sd) && Number.isFinite(F.mean)) {
          const y = top + 34 + (showMedian ? 22 : 0), a = sx(F.mean - F.sd), b = sx(F.mean + F.sd), o = K.obj('sd', '', 'ink');
          o.append(K.washPath(`M${a},${y}L${b},${y}`), svg('path', { d: `M${a},${y - 5}L${a},${y + 5}M${a},${y}L${b},${y}M${b},${y - 5}L${b},${y + 5}`, class: 'cvb-ln thin' }));
          o.append(K.lab(b + 6, y, `$\\pm\\sigma = ${K.fmt(F.sd, 3)}$`, { anchor: 'start', halo: true }));
          over.append(o);
        }
        /* Shaded probability label: above the marks under it, else in a free top corner, on a backing pill. Several
           regions are summed: P(X ≤ a) + P(X ≥ b) = v */
        let pillBox = null;
        if (hasShade && shadeMid && view.showProb !== false) {
          const v = Math.min(1, mainShades.reduce((t, q) => t + prob(F, q.from, q.to), 0));
          const text = view.probLabel || `$${mainShades.map((q) => lhsTex(F, q.from, q.to)).join(' + ')} = ${K.fmt(v, params.dp ?? 4)}$`;
          const w = K.tw(text.replace(/\\(le|ge|text)/g, ' ')) * 1.12 + 8;
          const reserved = markTop + 8 + (showSd ? 26 : 0);
          const marksTop = (a, b) => {
            let m = base;
            if (F.discrete) { for (const k of supportIn(F, sx.invert(a) - 0.5, sx.invert(b) + 0.5)) m = Math.min(m, sy(F.f(k))); }
            else for (let i = 0; i <= 30; i++) { const x = sx.invert(a + (b - a) * i / 30); m = Math.min(m, sy(F.f(x))); }
            for (const ov of [].concat(view.overlay || [])) { if (!ov) continue; const G = ovFam(ov, view); for (let i = 0; i <= 30; i++) { const x = sx.invert(a + (b - a) * i / 30); m = Math.min(m, sy(G.f(G.discrete ? Math.round(x) : x))); } }
            return m;
          };
          const cx = K.clamp((shadeMid[0] + shadeMid[1]) / 2, x0 + w / 2 + 4, x1 - w / 2 - 4);
          const cands = mainShades.length > 1 ? [(x0 + x1) / 2, x0 + w / 2 + 8, x1 - w / 2 - 4] : [cx, x0 + w / 2 + 8, x1 - w / 2 - 4];
          let lx = cands[1], ly = top + 12, found = false;
          for (const c of cands) { const yy = marksTop(c - w / 2, c + w / 2) - 18; if (yy >= reserved) { lx = c; ly = Math.min(yy, base - 40); found = true; break; } }
          if (!found) { ly = top + 12; lx = Math.abs(cands[1] - (showMean ? sx(F.mean) : -1e9)) > Math.abs(cands[2] - (showMean ? sx(F.mean) : -1e9)) ? cands[1] : cands[2]; }
          const o = K.obj('prob', 'cvb-prob'); pillBox = [lx - w / 2 - 6, lx + w / 2 + 6, ly + 12];
          o.append(svg('rect', { x: lx - w / 2 - 6, y: ly - 12, width: w + 12, height: 24, rx: 12, class: 'cvb-pill' }), K.lab(lx, ly, text, { w: w + 20, cls: 'cvb-strong' }));
          over.append(o);
        }

        /* item 320: observed-value marker lines: observed: 2.1, { x, label } or a list */
        [].concat(view.observed ?? []).forEach((ob, j) => {
          const xv = num(typeof ob === 'object' && ob ? ob.x : ob, P); if (xv == null || xv < range[0] || xv > range[1]) return;
          const o = K.obj((ob && ob.id) || (j ? 'observed' + j : 'observed'), 'cvb-observed', (ob && ob.colour) || 'ink'), x = sx(xv);
          o.append(K.washPath(`M${x},${base}L${x},${top}`), svg('line', { x1: x, x2: x, y1: base, y2: top, class: 'cvb-ln' }));
          const lt = ob && typeof ob === 'object' && ob.label != null ? String(ob.label).replace('{x}', K.fmt(xv, 3)) : `observed ${K.fmt(xv, 3).replace('-', '−')}`;
          const lyO = pillBox && x > pillBox[0] - 120 && x < pillBox[1] + 120 ? pillBox[2] + 14 + 22 * j : top + 8 + 22 * j;
          o.append(K.lab(x + (x > x1 - 110 ? -6 : 6), lyO, lt, { anchor: x > x1 - 110 ? 'end' : 'start', halo: true, cls: 'cvb-strong' }));
          over.insertBefore(o, over.firstChild); // under the probability pill
        });

        /* Drag handles on the first region's bounds: in drag mode, or (item 307) with drag: true on an explore screen */
        const sh0 = mainShades[0];
        if (sh0 && canDrag(view, R)) {
          const half = F.discrete ? (F.gap || 1) / 2 : 0;
          if (sh0.from != null && sh0.from >= range[0] - half) over.append(K.handle(sx(+sh0.from - half), base, 'from', { r: 7, shape: 'diamond', label: 'Lower bound' }));
          if (sh0.to != null && sh0.to <= range[1] + half) over.append(K.handle(sx(+sh0.to + half), base, 'to', { r: 7, shape: 'diamond', label: 'Upper bound' }));
        }
      },
      drag: {
        start: (id, p, R) => (canDrag(R.state, R) && shadesOf(R.state).length ? { id } : null),
        move(info, p, R, end) {
          const { F, sx, range } = geom(R.state), half = F.discrete ? (F.gap || 1) / 2 : 0;
          let v = sx.invert(p.x) + (info.id === 'from' ? half : -half);
          if (F.discrete) { const sp = supportIn(F, F.lo, F.hi); v = sp.length ? sp.reduce((b, x) => (Math.abs(x - v) < Math.abs(b - v) ? x : b), sp[0]) : Math.round(v); } else v = K.round(K.snapTo(v, params.snap || 0.01), 6);
          setBound(R, info.id, K.clamp(v, Math.floor(range[0]), Math.ceil(range[1])), end);
        },
        key(id, dx, dy, R) { const F = fam(R.state), st = F.discrete ? (F.gap || 1) : (params.snap || 0.1); const s0 = shadesOf(R.state)[0]; if (s0) setBound(R, id, +s0[id] + (dx || dy) * st, true); },
      },
      methods: (R) => ({
        /* Probability of the current shade (every region), or of [from, to] if given. */
        probability: (from, to) => { const F = fam(R.state); if (from !== undefined || to !== undefined) return prob(F, from, to); const ss = shadesOf(R.state).filter((q) => !q.under); return ss.length ? Math.min(1, ss.reduce((t, q) => t + prob(F, q.from, q.to), 0)) : 1; },
        stats: () => { const F = fam(R.state); return { mean: F.mean, sd: F.sd, median: F.median }; },
        points: () => { const s = shadesOf(R.state)[0] || {}; const o = {}; if (s.from != null) o.from = { x: s.from, y: 0 }; if (s.to != null) o.to = { x: s.to, y: 0 }; return o; },
        place: (id, pos, opts = {}) => { const v = Array.isArray(pos) ? pos[0] : pos; const sh = R.state.shade; return R.inst.set({ shade: Array.isArray(sh) ? sh.map((q, i) => (i ? q : { ...q, [id]: v })) : { [id]: v } }, opts); },
      }),
    };
    const canDrag = (view, R) => R.active('drag') || (!!(view.drag ?? params.drag) && R.active());
    const setBound = (R, id, v, end) => {
      const cur = R.state.shade, s = { ...(Array.isArray(cur) ? cur[0] : cur) }, P = P0(R.state);
      const other = (k) => num(s[k], P);
      if (id === 'from' && other('to') != null) v = Math.min(v, other('to'));
      if (id === 'to' && other('from') != null) v = Math.max(v, other('from'));
      s[id] = v;
      R.commit({ shade: Array.isArray(cur) ? [s, ...cur.slice(1)] : s });
      R.emit({ type: 'drag', id, x: v, y: 0, from: num(s.from, P), to: num(s.to, P), phase: end ? 'end' : 'move' });
    };
    return K.make(host, params, ctx, def);
  });
})();
