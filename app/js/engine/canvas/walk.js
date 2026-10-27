/* walk: random walks or price paths from the seeded RNG; many faint paths, one bold, barriers and the mean path.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js).
   Item 436: overlay panels under the walk (S_n^2 - n, (q/p)^S_n, a bankroll, a custom expr), the average at stopping,
   barriers bound to sliders (params lower and upper), a mean-reverting model (model "ou") and values() for derive. */
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
    /* item 436: model "ou" (also "mean-reverting", "ar1"): X(n+1) = X(n) + theta (mu - X(n)) + sigma Z on the normal draws */
    const isOU = (m) => typeof m === 'string' && /^(ou|ar1|mean-?reverting)$/i.test(m);
    const build = (view) => {
      const p = P(view), steps = Math.max(1, Math.round(p.steps || 50)), paths = Math.max(1, Math.round(p.paths || 1)), start = +(p.start ?? 0);
      const model = isOU(p.model) ? 'ou' : p.model || (p.mu != null || p.sigma != null ? 'normal' : 'coin');
      const d = draws(Math.round(view.run || 0), paths, steps), up = p.p ?? 0.5, step = p.step ?? 1, mu = p.mu ?? 0, sigma = p.sigma ?? 1, theta = p.theta ?? 0.1;
      const out = [];
      /* item 315: model "markov": states (labels), P (row-stochastic), start (a state label or index); a path's value is
         its state's index, drawn on a y axis labelled with the states */
      const mk = model === 'markov' ? markovOf(p) : null;
      for (let j = 0; j < paths; j++) {
        const a = new Float64Array(steps + 1); a[0] = mk ? mk.s0 : start;
        for (let i = 0; i < steps; i++) a[i + 1] = mk ? mk.next(a[i], d.u[j][i]) : model === 'ou' ? a[i] + theta * (mu - a[i]) + sigma * d.z[j][i] : a[i] + (model === 'normal' ? mu + sigma * d.z[j][i] : (d.u[j][i] < up ? step : -step));
        out.push(a);
      }
      if (mk) return { p, steps, paths, start: mk.s0, model, out, drift: 0, vol: 0, mk };
      if (model === 'ou') {
        /* the expected path and the spread of an AR(1): mean mu + (x0 - mu) phi^n, variance sigma^2 (1 - phi^2n) / (1 - phi^2) */
        const phi = 1 - theta, meanAt = (i) => mu + (start - mu) * Math.pow(phi, i), sdAt = (i) => (Math.abs(1 - phi * phi) < 1e-12 ? sigma * Math.sqrt(i) : sigma * Math.sqrt((1 - Math.pow(phi, 2 * i)) / (1 - phi * phi)));
        return { p, steps, paths, start, step, model, out, drift: 0, vol: sigma, ou: { mu, theta, sigma }, meanAt, sdAt };
      }
      const drift = model === 'normal' ? mu : (2 * up - 1) * step, vol = model === 'normal' ? sigma : 2 * step * Math.sqrt(up * (1 - up));
      return { p, steps, paths, start, step, model, out, drift, vol };
    };
    const markovOf = (p) => {
      const states = (p.states || []).map(String), M = Array.isArray(p.P) ? p.P : [];
      const s0 = typeof p.start === 'string' ? Math.max(0, states.indexOf(p.start)) : Math.max(0, Math.min(states.length - 1, Math.round(+p.start || 0)));
      const next = (i, u) => { const row = M[Math.round(i)] || []; let c = 0; for (let k = 0; k < row.length; k++) { c += +row[k] || 0; if (u < c) return k; } return Math.max(0, row.length - 1); };
      return { states, s0, next };
    };
    /* item 436: params lower and upper (slider-bindable, state.params overrides) take the place of barriers[0] and [1] */
    const barriers = (p) => { const b = p.barriers || []; return { lo: p.lower != null ? +p.lower : b[0] ?? null, hi: p.upper != null ? +p.upper : b[1] ?? null }; };
    const firstHit = (a, bar) => { for (let i = 0; i < a.length; i++) if ((bar.hi != null && a[i] >= bar.hi) || (bar.lo != null && a[i] <= bar.lo)) return i; return -1; };

    /* ---------- item 436: overlays, the stopping time and the average at stopping ---------- */
    const OV_COLOUR = { sq: 2, ratio: 3, bankroll: 4, expr: 5 }, OV_CHIP = { sq: 'S² − n', ratio: '(q/p)^S', bankroll: 'Bankroll' };
    /* params.overlays: ids "sq" | "ratio" | "bankroll", or objects { id, type, label, chip, colour, y, expr, ... } */
    const ovDefs = (p) => (Array.isArray(p.overlays) ? p.overlays : []).map((o) => (typeof o === 'string' ? { id: o } : o)).filter((o) => o && (o.id || o.expr))
      .map((o) => { const type = o.type || (o.expr ? 'expr' : o.id); return { ...o, type, id: String(o.id || type) }; }).filter((o) => OV_COLOUR[o.type]);
    const visibleOv = (p, view) => { const defs = ovDefs(p), sel = view.overlays; if (sel == null || sel === true) return defs; if (sel === false) return []; const ids = [].concat(sel).map(String); return defs.filter((d) => ids.includes(d.id)); };
    /* state.showStopped: true or "walk" (S_tau), an overlay id, or a list of them */
    const stoppedKeys = (view) => { const s = view.showStopped; if (s == null || s === false) return []; return s === true ? ['walk'] : [].concat(s).map(String); };
    const analyse = (B, view) => {
      const p = B.p, bar = barriers(p), any = bar.lo != null || bar.hi != null;
      const capN = Math.max(0, Math.min(B.steps, p.stopAt != null && Number.isFinite(+p.stopAt) ? Math.round(+p.stopAt) : B.steps));
      const hit = new Int32Array(B.paths), tau = new Int32Array(B.paths); let hits = 0, up = 0, down = 0;
      B.out.forEach((a, j) => { const h = any ? firstHit(a, bar) : -1; hit[j] = h; tau[j] = h >= 0 ? Math.min(h, capN) : capN; if (h >= 0) { hits++; if (bar.hi != null && a[h] >= bar.hi) up++; else down++; } });
      return { bar, any, cap: capN, hit, tau, hits, up, down, ov: {}, B, view };
    };
    /* the overlay's value along each path (a Float64Array per path), or null when it is not defined for the model */
    const ovOf = (A, d) => {
      if (d.id in A.ov) return A.ov[d.id];
      const { B, view } = A, { p, start, step, model } = B, coin = model === 'coin', pu = p.p ?? 0.5, qd = 1 - pu;
      let f = null;
      if (B.mk) f = null;
      else if (d.type === 'sq') {
        /* centred (default): (S - n m)^2 - n v^2, a martingale for the walk's own drift m and variance v^2; at p = 1/2 and step 1 it is S^2 - n */
        const cen = d.centred !== false, m = cen ? B.drift : 0, v2 = cen || !coin ? B.vol * B.vol : step * step;
        f = (a) => { const v = new Float64Array(a.length); for (let i = 0; i < a.length; i++) v[i] = (a[i] - start - i * m) ** 2 - i * v2; return v; };
      } else if (d.type === 'ratio') {
        if (coin && pu > 0 && pu < 1) { const r = qd / pu; f = (a) => { const v = new Float64Array(a.length); for (let i = 0; i < a.length; i++) v[i] = Math.min(1e12, Math.pow(r, (a[i] - start) / step)); return v; }; }
        else if (model === 'normal' && (p.sigma ?? 1) > 0) { const k = -2 * (p.mu ?? 0) / ((p.sigma ?? 1) ** 2); f = (a) => { const v = new Float64Array(a.length); for (let i = 0; i < a.length; i++) v[i] = Math.min(1e12, Math.exp(k * (a[i] - start))); return v; }; }
      } else if (d.type === 'bankroll') {
        /* start bankroll, a bet each step won or lost with the step; rules: fixed (stake), double (stake, doubled after every loss, back to stake after a win), fraction (that share of the bankroll); a bet never exceeds the bankroll or maxBet; at zero the bankroll stays ruined */
        const B0 = +(p.bankroll ?? d.bankroll ?? 100), base = +(p.stake ?? d.stake ?? 1), rule = String(view.bet ?? p.bet ?? d.bet ?? 'fixed'), fr = +(p.fraction ?? d.fraction ?? 0.1), maxBet = p.maxBet != null ? +p.maxBet : Infinity, unit = coin ? step : 1;
        f = (a) => {
          const v = new Float64Array(a.length); let bank = B0, bet = base; v[0] = B0;
          for (let i = 0; i < a.length - 1; i++) {
            if (bank <= 1e-9) { bank = 0; v[i + 1] = 0; continue; }
            const b = Math.min(rule === 'double' ? bet : rule === 'fraction' ? fr * bank : base, maxBet, bank), o = (a[i + 1] - a[i]) / unit;
            bank = Math.max(0, bank + b * o); if (rule === 'double') bet = o < 0 ? bet * 2 : base; v[i + 1] = bank;
          }
          return v;
        };
      } else if (d.type === 'expr' && d.expr) {
        /* names: n (step), x (position), S (position less start, in steps for the coin), p, q, start, step and every numeric param (mu, sigma, theta, sliders) */
        const nums = Object.fromEntries(Object.entries(p).filter(([, v]) => typeof v === 'number')), sc = { ...nums, p: pu, q: qd, start, step: coin ? step : 1 }, names = [...Object.keys(sc), 'n', 'x', 'S'], fn = K.fnOf(String(d.expr), names);
        f = (a) => { const v = new Float64Array(a.length); for (let i = 0; i < a.length; i++) v[i] = fn(0, { ...sc, n: i, x: a[i], S: (a[i] - start) / (coin ? step : 1) }); return v; };
      }
      return (A.ov[d.id] = f ? B.out.map(f) : null);
    };
    /* the value at tau of the walk ("walk") or of an overlay, one per path, and the running mean over paths */
    const atTau = (A, key) => {
      if (key === 'walk') return Float64Array.from(A.B.out, (a, j) => a[A.tau[j]]);
      const d = ovDefs(A.B.p).find((x) => x.id === key), arr = d && ovOf(A, d);
      return arr ? Float64Array.from(arr, (v, j) => v[A.tau[j]]) : null;
    };
    const startOf = (A, key) => { if (key === 'walk') return A.B.start; const d = ovDefs(A.B.p).find((x) => x.id === key), arr = d && ovOf(A, d); return arr ? arr[0][0] : NaN; };
    const runMean = (vals) => { const r = new Float64Array(vals.length); let s = 0; for (let k = 0; k < vals.length; k++) { s += vals[k]; r[k] = s / (k + 1); } return r; };
    const mean = (v) => v.reduce((t, x) => t + x, 0) / (v.length || 1);
    const se = (v) => { if (v.length < 2) return 0; const m = mean(v); return Math.sqrt(v.reduce((t, x) => t + (x - m) ** 2, 0) / (v.length - 1) / v.length); };
    const valuesOf = (B, view) => {
      const A = analyse(B, view), out = { paths: B.paths, hits: A.hits, hitsUp: A.up, hitsDown: A.down, stopAt: A.cap, tau: Array.from(A.tau), tauMean: mean(A.tau), endMean: mean(B.out.map((a) => a[B.steps])) };
      const w = atTau(A, 'walk'); out.stopped = mean(w); out.stoppedSE = se(w); out.stoppedValues = Array.from(w); out.runningMean = Array.from(runMean(w));
      ovDefs(B.p).forEach((d) => {
        const v = atTau(A, d.id), id = d.id.replace(/[^A-Za-z0-9_]/g, '_').replace(/^./, (c) => c.toUpperCase());
        if (!v) return; out['stopped' + id] = mean(v); out['stopped' + id + 'SE'] = se(v); out['runningMean' + id] = Array.from(runMean(v));
        if (d.type === 'bankroll') out['ruined' + id] = v.reduce((t, x) => t + (x <= 1e-9 ? 1 : 0), 0);
      });
      return out;
    };
    /* Overlay and stopped-average panels share the x axis of the walk (steps) or their own (paths averaged) */
    const quant = (v, q) => { const s = Array.from(v).sort((x, y) => x - y); return s.length ? s[Math.min(s.length - 1, Math.max(0, Math.round(q * (s.length - 1))))] : 0; };
    const niceRange = (lo, hi, base) => {
      if (base != null && Number.isFinite(base)) { lo = Math.min(lo, base); hi = Math.max(hi, base); }
      if (!(hi > lo)) { lo -= 1; hi += 1; }
      const pad = (hi - lo) * 0.08, t = C.niceTicks(lo - pad, hi + pad, 5), st = t[1] - t[0] || 1;
      return [Math.floor((lo - pad) / st) * st, Math.ceil((hi + pad) / st) * st];
    };
    const ovLabel = (d, B, rule) => {
      if (d.label != null) return d.label;
      if (d.type === 'sq') return d.centred === false || B.drift === 0 ? (B.vol === 1 || d.centred === false ? '$S_n^2-n$' : '$S_n^2-n\\sigma^2$') : '$(S_n-n\\mu)^2-n\\sigma^2$';
      if (d.type === 'ratio') return B.model === 'coin' ? '$(q/p)^{S_n}$' : '$e^{-2\\mu S_n/\\sigma^2}$';
      if (d.type === 'bankroll') return 'Bankroll (' + (rule === 'double' ? 'doubling after a loss' : rule === 'fraction' ? 'fixed fraction' : 'fixed stake') + ')';
      return String(d.expr);
    };
    const stopLabel = (d, key) => {
      if (key === 'walk') return '$S_\\tau$';
      if (d.stopLabel != null) return d.stopLabel;
      return d.type === 'sq' ? '$S_\\tau^2-\\tau$' : d.type === 'ratio' ? '$(q/p)^{S_\\tau}$' : d.type === 'bankroll' ? 'the bankroll at $\\tau$' : String(d.label || d.expr) + ' at $\\tau$';
    };
    let seen = null, seenKey = null;

    /* Overlay toggles: one chip per overlay, built once (not in static copies) */
    const chips = new Map(); let chipsBuilt = false;
    const buildChips = (R) => {
      if (chipsBuilt || R.static) return; chipsBuilt = true;
      const defs = ovDefs(params); if (!defs.length || params.toggles === false) return;
      for (const d of defs) {
        const b = document.createElement('button'); b.type = 'button'; b.className = 'cvb-chip'; b.textContent = d.chip ?? OV_CHIP[d.type] ?? (d.label ? String(d.label).replace(/\$/g, '') : String(d.expr));
        b.addEventListener('click', () => {
          if (R.locked) return;
          const cur = visibleOv(P(R.state), R.state).map((x) => x.id), on = !cur.includes(d.id), next = ovDefs(params).map((x) => x.id).filter((id) => (id === d.id ? on : cur.includes(id)));
          R.inst.set({ overlays: next }, { instant: true }); R.emit({ type: 'overlay', id: d.id, on, overlays: next });
        });
        chips.set(d.id, b); R.extra.append(b);
      }
    };
    const syncChips = (vis) => { const ids = new Set(vis.map((d) => d.id)); chips.forEach((b, id) => { const on = ids.has(id); b.setAttribute('aria-pressed', String(on)); b.style.background = on ? 'var(--ink)' : ''; b.style.color = on ? 'var(--bg-canvas)' : ''; b.style.borderColor = on ? 'var(--ink)' : ''; }); };

    const def = {
      kind: 'walk', aria: params.aria || 'Random walk paths',
      modes: ['slider', 'tap'],
      size: () => ({ w: W, h: H }),
      skip: ['run'],
      init: () => ({ run: 0, showMean: false, highlight: [], params: Object.fromEntries(['p', 'mu', 'sigma', 'steps', 'paths', 'start', 'step', 'theta', 'lower', 'upper', 'stopAt', 'bankroll', 'stake', 'fraction'].filter((k) => typeof params[k] === 'number' && !(k === 'start' && params.model === 'markov')).map((k) => [k, params[k]])), reveal: 1 }),
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
        const A = analyse(B, view);
        /* item 436: panels under the walk */
        const defsAll = B.mk ? [] : ovDefs(B.p), vis = B.mk ? [] : visibleOv(B.p, view), skeys = B.mk || B.paths < 2 ? [] : stoppedKeys(view).filter((k) => k === 'walk' || defsAll.some((d) => d.id === k));
        buildChips(R); syncChips(vis);
        const panels = [];
        const ph = +(params.overlayHeight || 84), xl = params.xLabel === '' ? '' : params.xLabel ?? 'Step';
        vis.forEach((d) => {
          const arr = ovOf(A, d), colour = d.colour ?? OV_COLOUR[d.type]; let yr = null, note = null, base = null;
          if (!arr) { note = d.type === 'ratio' ? 'not defined for this model or p' : 'not defined for this model'; yr = [0, 1]; }
          else {
            base = arr[0][0];
            if (Array.isArray(d.y)) yr = d.y.slice();
            else {
              const mins = arr.map((v) => Math.min(...v)), maxs = arr.map((v) => Math.max(...v));
              if (d.type === 'sq') yr = niceRange(Math.min(...mins), Math.max(...maxs), 0);
              else { const trim = arr.length > 4; yr = niceRange(d.type === 'ratio' ? 0 : trim ? Math.min(quant(mins, 0.03), 0) : Math.min(...mins), Math.max(trim ? quant(maxs, 0.95) : Math.max(...maxs), d.type === 'ratio' ? 2 : 0) * 1.02, base); }
              if (d.type === 'ratio') yr[0] = Math.min(yr[0], 0);
            }
          }
          panels.push({ kind: 'step', d, arr, colour, yr, note, base, title: ovLabel(d, B, String(view.bet ?? B.p.bet ?? d.bet ?? 'fixed')) });
        });
        const lastStep = panels.length - 1;
        if (lastStep >= 0) panels[lastStep].xl = xl;
        skeys.forEach((key) => {
          const d = key === 'walk' ? { id: 'walk', type: 'walk' } : defsAll.find((x) => x.id === key), vals = atTau(A, key); if (!vals) return;
          const rm = runMean(vals), ref = startOf(A, key), k0 = Math.min(vals.length - 1, Math.max(1, Math.ceil(vals.length * 0.08))), tail = rm.slice(k0);
          panels.push({ kind: 'stop', key, vals, rm, ref, colour: key === 'walk' ? params.colour || 1 : d.colour ?? OV_COLOUR[d.type], yr: niceRange(Math.min(...tail), Math.max(...tail), ref), xl: 'Paths averaged', title: 'Average of ' + stopLabel(d, key), id: 'stopped-' + key });
        });
        /* geometry: panel i sits under the walk, 30 px for its title, ph px of plot, then room for ticks (and an axis label) */
        let cursor = H;
        panels.forEach((q) => { q.top = cursor + 30; q.bottom = q.top + ph; cursor = q.bottom + (q.xl ? 46 : 24); });
        const Htot = Math.round(cursor); if (R.F.h !== Htot) R.F.resize(W, Htot);

        let lo = Infinity, hi = -Infinity;
        /* the range follows the paths that are drawn (params.drawn), and with showStopped and stopAtBarrier only up to tau */
        const nDrawn = params.drawn > 0 ? Math.round(params.drawn) : Infinity, cut = view.stopAtBarrier && view.showStopped;
        B.out.forEach((a, j) => { if (j >= nDrawn && j !== (params.bold ?? 0)) return; const e = cut ? A.tau[j] + 1 : a.length; for (let i = 0; i < e; i++) { const v = a[i]; if (v < lo) lo = v; if (v > hi) hi = v; } });
        if (bar.lo != null) lo = Math.min(lo, bar.lo); if (bar.hi != null) hi = Math.max(hi, bar.hi);
        if (B.ou) { lo = Math.min(lo, B.ou.mu); hi = Math.max(hi, B.ou.mu); }
        let yr = params.y || (B.mk ? [-0.5, Math.max(0.5, B.mk.states.length - 0.5)] : null);
        if (!yr) { const pad = (hi - lo || 2) * 0.1; const t = C.niceTicks(lo - pad, hi + pad, 8), st = t[1] - t[0] || 1; yr = [Math.floor((lo - pad) / st) * st, Math.ceil((hi + pad) / st) * st]; const rk = [bar.lo, bar.hi, cut, nDrawn].join(); if (rk !== seenKey) { seen = null; seenKey = rk; } /* the held range resets when a barrier moves or the drawn set changes */
          seen = seen && !view._fresh ? [Math.min(seen[0], yr[0]), Math.max(seen[1], yr[1])] : yr; yr = seen; }
        let ml = B.mk ? 18 + Math.max(...B.mk.states.map((t) => K.tw(t, 12))) : K.yMargin(yr[0], yr[1], H - 60);
        panels.forEach((q) => { if (q.yr) ml = Math.max(ml, K.yMargin(q.yr[0], q.yr[1], ph)); });
        const mt = 26, mb = params.xLabel === '' || panels.length ? 30 : 46, mr = skeys.length ? 92 : 70;
        const sx = C.scale([0, B.steps], [ml, W - mr]), sy = C.scale(yr, [H - mb, mt]);
        const x0 = ml, x1 = W - mr, y0 = H - mb, y1 = mt;
        /* item 323: xStep fixes the step ticks (1 for whole steps) */
        const xTicks = params.xStep > 0 ? (() => { const t = []; for (let v = 0; v <= B.steps + 1e-9; v += +params.xStep) t.push(Math.round(v * 1e6) / 1e6); return { ticks: t, step: +params.xStep }; })() : undefined;
        const yTicks = B.mk ? { ticks: B.mk.states.map((_, k) => k), step: 1 } : undefined;
        K.chartAxes(g, sx, sy, { yLabel: params.yLabel ?? (B.mk ? 'State' : B.model === 'coin' ? 'Position' : 'Value'), xLabel: panels.length ? '' : xl, xTicks, yTicks, fmtY: B.mk ? (v) => B.mk.states[Math.round(v)] ?? '' : undefined, baseline: B.mk || B.ou ? null : B.start >= yr[0] && B.start <= yr[1] ? B.start : null });
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
        /* a fixed stopping step (params.stopAt), a dashed vertical line */
        if (!B.mk && B.p.stopAt != null && A.cap < B.steps) {
          const x = sx(A.cap), o = K.obj('stop-time', '', 'ink');
          o.append(K.washPath(`M${x},${y1}L${x},${y0}`), svg('line', { x1: x, x2: x, y1, y2: y0, class: 'cvb-ln thin cvb-dash' }));
          over.append(o, K.txt(x, y1 - 9, params.stopLabel ?? 'stop', { cls: 'cvb-strong', size: 12, halo: true }));
        }
        const reveal = K.clamp(view.reveal ?? 1, 0, 1), upto = reveal * B.steps;
        const em = new Set(def.hlIds(view));
        const pathD = (a) => { if (B.mk) { let d = ''; const last = Math.min(a.length - 1, Math.floor(upto)); for (let i = 0; i <= last; i++) d += (i ? `L${sx(i).toFixed(1)},${sy(a[i - 1]).toFixed(1)}L` : 'M') + sx(i).toFixed(1) + ',' + sy(a[i]).toFixed(1); return d; } let d = ''; const last = Math.floor(upto); for (let i = 0; i <= last && i < a.length; i++) d += (i ? 'L' : 'M') + sx(i).toFixed(1) + ',' + sy(a[i]).toFixed(1); if (upto > last && last + 1 < a.length) { const f = upto - last; d += 'L' + sx(upto).toFixed(1) + ',' + sy(a[last] + (a[last + 1] - a[last]) * f).toFixed(1); } return d; };
        const stop = view.stopAtBarrier, boldIdx = params.bold ?? 0, drawn = params.drawn > 0 ? Math.round(params.drawn) : Infinity;
        const showStopDots = !!view.showStopped;
        B.out.forEach((a, j) => {
          const h = A.hit[j];
          if (j >= drawn && j !== boldIdx) return;
          const arr = stop && A.tau[j] + 1 < a.length ? a.slice(0, A.tau[j] + 1) : a;
          const main = j === boldIdx, o = K.obj('path' + j, '', main ? (params.colour || 1) : (params.colour || 1));
          const d = pathD(arr);
          o.append(K.washPath(d), svg('path', { d, class: 'cvb-path' + (main ? ' main' : '') + (em.has('path' + j) ? ' em' : '') }));
          if (view.showHits && h >= 0 && h <= upto) o.append(svg('circle', { cx: sx(h), cy: sy(a[h]), r: main ? 4.5 : 3, class: 'cvb-dot' }));
          if (showStopDots && A.tau[j] <= upto) o.append(svg('circle', { cx: sx(A.tau[j]), cy: sy(a[A.tau[j]]), r: main ? 4.5 : 2.5, class: 'cvb-dot' }));
          R.tappable(o, 'path' + j, 'Path ' + (j + 1));
          if (main) plot.append(o); else plot.insertBefore(o, plot.firstChild);
        });
        /* mean path and optional spread envelope */
        if (B.ou && params.meanLine !== false) {
          /* the level the process reverts to, dashed across the plot */
          const y = sy(B.ou.mu), o = K.obj('mean-level', '', 'ink');
          o.append(K.washPath(`M${x0},${y}L${x1},${y}`), svg('line', { x1: x0, x2: x1, y1: y, y2: y, class: 'cvb-ln thin cvb-dash' }));
          over.append(o); right.push({ y, text: params.levelLabel ?? 'μ = ' + K.fmt(B.ou.mu, 2) });
        }
        if (view.showMean) {
          const o = K.obj('mean', '', 'ink');
          let d, ey;
          if (B.ou) { d = ''; for (let i = 0; i <= B.steps; i++) d += (i ? 'L' : 'M') + sx(i).toFixed(1) + ',' + sy(B.meanAt(i)).toFixed(1); ey = sy(B.meanAt(B.steps)); }
          else { d = `M${sx(0)},${sy(B.start)}L${sx(B.steps)},${sy(B.start + B.drift * B.steps)}`; ey = sy(B.start + B.drift * B.steps); }
          o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln thin cvb-dash' })); plot.append(o);
          if (!(B.ou && params.meanLine !== false && Math.abs(ey - sy(B.ou.mu)) < 3)) right.push({ y: K.clamp(ey, y1 + 8, y0 - 8), text: params.meanLabel || 'mean' });
        }
        if (view.showSpread) {
          const o = K.obj('spread', '', 'muted'); let up = '', dn = '';
          const mAt = B.ou ? B.meanAt : (i) => B.start + B.drift * i, sAt = B.ou ? B.sdAt : (i) => B.vol * Math.sqrt(i);
          for (let i = 0; i <= B.steps; i++) { const m = mAt(i), s = sAt(i) * (view.showSpread === true ? 1 : +view.showSpread); up += (i ? 'L' : 'M') + sx(i).toFixed(1) + ',' + sy(m + s).toFixed(1); dn += (i ? 'L' : 'M') + sx(i).toFixed(1) + ',' + sy(m - s).toFixed(1); }
          o.append(svg('path', { d: up, class: 'cvb-ln thin cvb-dash' }), svg('path', { d: dn, class: 'cvb-ln thin cvb-dash' })); plot.append(o);
        }
        /* end label of the bold path */
        const main = B.out[params.bold ?? 0];
        if (main && params.label) right.push({ y: K.clamp(sy(main[Math.min(main.length - 1, Math.round(upto))]), y1 + 8, y0 - 8), text: params.label });
        K.spread(right, 15, y1 + 6, y0 - 6);
        for (const l of right) over.append(K.txt(x1 + 6, l.y, l.text, { anchor: 'start', size: 12, cls: 'cvb-strong', halo: true }));
        if (view.showHits && (bar.lo != null || bar.hi != null) && B.paths > 1) {
          /* item 323: with both barriers the count splits into the top and the bottom ({up}, {down} in hitsLabel) */
          const both = bar.lo != null && bar.hi != null, hits = A.hits, hitsUp = A.up, hitsDown = A.down;
          const t = view.hitsLabel ? String(view.hitsLabel).replace('{hits}', hits).replace('{paths}', B.paths).replace('{up}', hitsUp).replace('{down}', hitsDown) : both ? `${hitsUp} hit the top, ${hitsDown} the bottom (of ${B.paths})` : `${hits} of ${B.paths} paths hit`;
          over.append(K.txt(x0 + 6, y1 + 10, t, { anchor: 'start', cls: 'cvb-strong', halo: true }));
        }

        /* ---- item 436: overlay panels (against n) and the running average at stopping (against the path count) ---- */
        panels.forEach((q, qi) => {
          const syq = C.scale(q.yr, [q.bottom, q.top]), id = q.kind === 'step' ? 'ov-' + q.d.id : q.id;
          if (q.kind === 'step') {
            K.chartAxes(g, sx, syq, { yLabel: q.title, xLabel: q.xl || '', xTicks, baseline: q.base != null && q.base >= q.yr[0] && q.base <= q.yr[1] ? q.base : null });
            if (q.note) { g.append(K.txt((x0 + x1) / 2, (q.top + q.bottom) / 2, q.note, { cls: 'cvb-tick', size: 12 })); return; }
            const clip = svg('g', { 'clip-path': R.clipRect(x0, q.top - 3, x1 - x0 + 3, ph + 6, 'ov' + qi) }); g.append(clip);
            const grp = K.obj(id, '', q.colour); clip.append(grp);
            const lineD = (a, last) => { let d = ''; const l = Math.min(last, Math.floor(upto)); for (let i = 0; i <= l && i < a.length; i++) d += (i ? 'L' : 'M') + sx(i).toFixed(1) + ',' + syq(a[i]).toFixed(1); if (upto > l && l + 1 <= last && l + 1 < a.length) { const f = upto - l; d += 'L' + sx(upto).toFixed(1) + ',' + syq(a[l] + (a[l + 1] - a[l]) * f).toFixed(1); } return d; };
            q.arr.forEach((a, j) => {
              if (j >= drawn && j !== boldIdx) return;
              const last = stop ? A.tau[j] : B.steps, mainP = j === boldIdx, d = lineD(a, last);
              const el = svg('path', { d, class: 'cvb-path' + (mainP ? ' main' : '') + (em.has('path' + j) ? ' em' : '') });
              if (mainP) grp.append(el); else grp.insertBefore(el, grp.firstChild);
              if (showStopDots && A.tau[j] <= upto) grp.append(svg('circle', { cx: sx(A.tau[j]), cy: syq(a[A.tau[j]]), r: mainP ? 4.5 : 2.5, class: 'cvb-dot' }));
            });
          } else {
            const P2 = q.vals.length, sx2 = C.scale([0, P2], [x0, x1]), shownN = Math.max(1, Math.min(P2, Math.round(reveal * P2)));
            K.chartAxes(g, sx2, syq, { yLabel: q.title, xLabel: q.xl, baseline: null });
            const clip = svg('g', { 'clip-path': R.clipRect(x0, q.top - 3, x1 - x0 + 3, ph + 6, 'ov' + qi) }); g.append(clip);
            const refY = syq(q.ref), ro = K.obj('stopped-ref', '', 'ink'); ro.append(svg('line', { x1: x0, x2: x1, y1: refY, y2: refY, class: 'cvb-ln thin cvb-dash' })); clip.append(ro);
            let d = ''; for (let k = 0; k < shownN; k++) d += (k ? 'L' : 'M') + sx2(k + 1).toFixed(1) + ',' + syq(q.rm[k]).toFixed(1);
            const so = K.obj(id, '', q.colour); so.append(K.washPath(d), svg('path', { d, class: 'cvb-ln' })); clip.append(so);
            const lastV = q.rm[shownN - 1], labs = [{ y: refY, text: 'start ' + K.fmt(q.ref, 2) }, { y: syq(lastV), text: 'mean ' + K.fmt(lastV, 2) }];
            K.spread(labs, 15, q.top + 6, q.bottom - 6);
            for (const l of labs) g.append(K.txt(x1 + 6, l.y, l.text, { anchor: 'start', size: 12, cls: 'cvb-strong', halo: true }));
          }
        });
      },
      methods: (R) => ({
        /* Re-sample: the next run of the seeded generator. */
        run: () => R.inst.set({ run: Math.round(R.state.run || 0) + 1 }),
        paths: () => build(R.state).out.map((a) => Array.from(a)),
        hits: () => { const B = build(R.state), bar = barriers(B.p); return B.out.map((a) => firstHit(a, bar)); },
        hitCounts: () => { const B = build(R.state), bar = barriers(B.p); let up = 0, down = 0; B.out.forEach((a) => { const h = firstHit(a, bar); if (h >= 0) { if (bar.hi != null && a[h] >= bar.hi) up++; else down++; } }); return { up, down, paths: B.paths }; },
        /* item 436: the stopping time per path, the stopped values ("walk" or an overlay id) and their running mean */
        stopTimes: () => Array.from(analyse(build(R.state), R.state).tau),
        stopped: (key = 'walk') => { const B = build(R.state), v = atTau(analyse(B, R.state), key); return v ? Array.from(v) : null; },
        runningMean: (key = 'walk') => { const B = build(R.state), v = atTau(analyse(B, R.state), key); return v ? Array.from(runMean(v)) : null; },
        /* numbers for derive (values.stopped, values.hitsUp, values.runningMean ...): see README-B */
        values: () => valuesOf(build(R.state), R.state),
        /* the effective value of a param: lower and upper fall back to barriers[0] and [1], so a slider opens on the barrier */
        getParam: (k) => { const p = P(R.state); if (k === 'lower' || k === 'upper') { const b = barriers(p); const v = k === 'lower' ? b.lo : b.hi; return v == null ? undefined : v; } return typeof p[k] === 'number' ? p[k] : undefined; },
      }),
    };
    return K.make(host, params, ctx, def);
  });
})();
