/* bars: bar chart or histogram, with exact value lines and a seeded simulation that fills the bars.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js). */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  C.register('bars', (host, params, ctx) => {
    const K = Z.cvb;
    const W = 540, H = params.height || 280;
    const binned = !!params.bins;
    /* item 167: bins can be re-cut from state.binWidth (a control binds "binWidth"); with params.data (raw
       observations) the bars are its counts in the current bins */
    const binsFor = (width) => { const { min, max } = params.bins, w = Math.max(1e-9, +width || params.bins.width); const n = Math.max(1, Math.round((max - min) / w)); return Array.from({ length: n }, (_, i) => ({ id: 'b' + i, label: K.fmt(min + i * w, 4), lo: min + i * w, hi: min + (i + 1) * w })); };
    let binW = binned ? params.bins.width : null;
    let cats = binned
      ? binsFor(binW)
      : (params.categories || []).map((c) => (K.isObj(c) ? { id: c.id || 'x' + c.label, label: String(c.label ?? c.id), colour: c.colour } : { id: 'x' + c, label: String(c) }));
    const rebin = (view) => { if (!binned) return; const w = (view && view.binWidth) || params.bins.width; if (w !== binW) { binW = w; cats = binsFor(w); } };
    const catIndex = (key) => {
      if (key == null) return -1; const k = String(key);
      let i = cats.findIndex((c) => c.id === k || c.label === k);
      if (i < 0 && binned) { const v = +k; i = cats.findIndex((c) => v >= c.lo - 1e-9 && v < c.hi - 1e-9); }
      if (i < 0 && !binned && Number.isFinite(+k)) i = cats.findIndex((c) => +c.label === +k);
      return i;
    };
    const exact = (params.exact || []).map((e) => ({ i: catIndex(e.x), y: +e.y })).filter((e) => e.i >= 0);
    const sim = params.sim || null;
    const proportion = params.proportion ?? (exact.length > 0);
    /* item 279: groups: [{ id, label, colour }] draws two or more bars per category side by side, with a legend; their
       heights come from state.values.<group id> ({ category: value }) or, with a sim whose outcome is a list
       ([X, Y], item 303), from the list's entries in order */
    const groups = Array.isArray(params.groups) && params.groups.length ? params.groups.map((q, i) => ({ id: String(q.id ?? 'g' + i), label: String(q.label ?? q.id ?? ''), colour: q.colour ?? i + 1 })) : null;
    const G = groups ? groups.length : 1;

    /* Seeded outcomes: outcomes[i] is the same trial every time, so 10 then 100 shows the first 110. Items 326, 321,
       286: the outcome reads params and state.params by name (a slider on n re-runs the stream), sim.let binds names
       per trial, and sim.filter discards trials (they are not counted) */
    let outcomes = [], discarded = 0, simRng = null, simErr = null, simKey = null, trialFn = null;
    const simVars = (view) => ({ ...(params.params || {}), ...((view && view.params) || {}) });
    const ensure = (n, view) => {
      if (!sim || simErr) return;
      const vars = simVars(view); delete vars.trials;
      const key = JSON.stringify(vars);
      if (key !== simKey) { simKey = key; outcomes = []; discarded = 0; simRng = null; trialFn = null; }
      try {
        if (!simRng) simRng = K.rngFor(sim.seed ?? 1);
        if (!trialFn) trialFn = Z.sim.trial ? Z.sim.trial(sim, vars) : ((r) => ({ value: Z.sim.outcome(sim.outcome, r), keep: true }));
        let guard = 0;
        while (outcomes.length < n && guard++ < 50 * n + 1000) { const t = trialFn(simRng); if (t.keep) outcomes.push(t.value); else discarded++; }
      } catch (e) { simErr = e; console.warn('bars sim:', e.message); }
    };
    const tally = (n, view, g = 0) => {
      ensure(n, view); const counts = new Array(cats.length).fill(0);
      for (let i = 0; i < Math.min(n, outcomes.length); i++) { let v = outcomes[i]; if (Array.isArray(v)) v = v[g]; const j = binned ? catIndex(+v) : catIndex(typeof v === 'boolean' ? +v : v); if (j >= 0) counts[j]++; }
      return counts;
    };
    /* heights of group g (0 without groups) */
    const heights = (view, g = 0) => {
      rebin(view);
      if (binned && Array.isArray(params.data)) { // raw observations: counts (or proportions) in the current bins
        const counts = new Array(cats.length).fill(0); params.data.forEach((v) => { const j = catIndex(+v); if (j >= 0) counts[j]++; else if (+v === params.bins.max) counts[cats.length - 1]++; });
        return counts.map((c) => (proportion ? (params.data.length ? c / params.data.length : 0) : c));
      }
      if (sim && view.ran != null && !(view.values && Object.keys(view.values).length && !view.ran)) {
        const n = Math.round(view.ran), counts = tally(n, view, g);
        return counts.map((c) => (proportion ? (n ? c / n : 0) : c));
      }
      const v0 = view.values || {}, v = groups ? (K.isObj(v0[groups[g].id]) ? v0[groups[g].id] : {}) : v0; const out = new Array(cats.length).fill(0);
      for (const [k, val] of Object.entries(v)) { const i = catIndex(k); if (i >= 0) out[i] = Array.isArray(val) ? (+val[g] || 0) : (+val || 0); }
      for (const [i, c] of (params.categories || []).entries()) if (K.isObj(c) && c.value != null && !(c.label in v) && !((c.id || 'x' + c.label) in v)) out[i] = Array.isArray(c.value) ? (+c.value[g] || 0) : +c.value;
      return out;
    };
    const allHeights = (view) => (groups ? groups.flatMap((_, g) => heights(view, g)) : heights(view, 0));
    /* item 272: yScale "log": positive heights on a log axis (ticks at 1, 2, 5 times powers of ten) */
    const logY = params.yScale === 'log';
    /* the numeric value of category i (its label), for value axes, curves and cuts */
    const valOf = (i) => (binned ? (cats[i].lo + cats[i].hi) / 2 : Number(String(cats[i].label).replace('−', '-')));
    const yTop = (view, hs) => {
      if (params.yMax != null) return params.yMax;
      if (logY) { const m = Math.max(...hs.filter((h) => h > 0), 1); return Math.pow(10, Math.ceil(Math.log10(m * 1.05))); }
      const m = Math.max(...hs, ...exact.map((e) => e.y * (sim ? 1.6 : 1.1)), proportion ? 0.05 : 1);
      const t = C.niceTicks(0, m * 1.08, 5); return t[t.length - 1] >= m * 1.02 ? t[t.length - 1] : m * 1.15;
    };
    /* item 133: negative values hang below a zero baseline; the axis runs down to a nice tick under the lowest bar */
    const yBot = (hs) => {
      if (logY) { const m = Math.min(...hs.filter((h) => h > 0), 1); return params.yMin > 0 ? params.yMin : Math.pow(10, Math.floor(Math.log10(m))); }
      if (params.yMin != null) return params.truncate ? params.yMin : Math.min(0, params.yMin); // item 184: truncate: true keeps a yMin above 0 (the truncated-axis trick)
      const m = Math.min(0, ...hs); if (m >= 0) return 0;
      const t = C.niceTicks(m * 1.08, 0, 4); return t[0] <= m * 1.02 ? t[0] : m * 1.15;
    };
    const fmtY = proportion ? (v, st) => K.fmtTick(v, st) : (v, st) => K.fmtTick(v, st);
    /* Value labels (showValues): `decimals` fixes the places and keeps trailing zeros; `money: "£"` prefixes the
       currency (two places unless `decimals` says otherwise) */
    const fmtV = (v) => {
      const fixed = (x, d) => Math.abs(x).toLocaleString('en-GB', { minimumFractionDigits: d, maximumFractionDigits: d });
      if (params.money) return (v < 0 ? '−' : '') + params.money + fixed(v, params.decimals ?? 2);
      if (params.decimals != null) return (v < 0 ? '−' : '') + fixed(v, params.decimals);
      return K.fmt(v, 3);
    };

    /* Run controls, built once and kept across redraws */
    const chips = [];
    let countEl = null;
    const buildControls = (R) => {
      if (!sim || R.static) return;
      for (const n of sim.trials || [10, 100, 1000]) {
        const b = document.createElement('button'); b.type = 'button'; b.className = 'cvb-chip'; b.textContent = 'Run ' + n.toLocaleString('en-GB');
        b.addEventListener('click', () => { if (!R.locked) { const ran = Math.round(R.state.ran || 0) + n; R.inst.set({ ran }); R.emit({ type: 'run', ran, added: n }); } });
        chips.push(b); R.extra.append(b);
      }
      const r = document.createElement('button'); r.type = 'button'; r.className = 'cvb-chip quiet'; r.textContent = 'Reset';
      r.addEventListener('click', () => { if (!R.locked) { R.inst.set({ ran: 0 }, { instant: true }); R.emit({ type: 'run', ran: 0, added: 0 }); } });
      chips.push(r); R.extra.append(r);
      countEl = document.createElement('span'); countEl.className = 'cvb-count'; countEl.setAttribute('aria-live', 'polite'); R.extra.append(countEl);
    };

    let geo = null;
    const canDrag = (view, R) => R.active('drag') || (!!(view.drag ?? params.drag) && R.active());
    const def = {
      kind: 'bars', aria: params.aria || 'Bar chart',
      modes: ['tap', 'slider', 'drag'],
      drag: {
        start: (id, p, R) => (id === 'pivot' && canDrag(R.state, R) && geo && geo.pxOf ? { id } : null),
        move(info, p, R, end) {
          let lo = -1e6, hi = 1e6; for (let k = 0; k < 60; k++) { const m = (lo + hi) / 2; if (geo.pxOf(m) < p.x) lo = m; else hi = m; }
          const v = K.round(K.snapTo((lo + hi) / 2, params.snap || 0.1), 6);
          R.commit({ pivot: v }); R.emit({ type: 'drag', id: 'pivot', x: v, y: 0, phase: end ? 'end' : 'move' });
        },
        key(id, dx, dy, R) { const v = K.round(+R.state.pivot + (dx || dy) * (params.snap || 0.1), 6); R.commit({ pivot: v }); R.emit({ type: 'drag', id: 'pivot', x: v, y: 0, phase: 'end' }); },
      },
      size: () => ({ w: W, h: H }),
      listKeys: ['hlines', 'curves'],
      init: () => ({ values: {}, ran: sim ? 0 : undefined, highlight: [], params: {}, hlines: [], curves: [] }),
      prepare(patch) {
        if (patch.params && patch.params.trials != null) patch.ran = Math.round(patch.params.trials);
        if (patch.reset) { patch.ran = 0; delete patch.reset; }
        return patch;
      },
      animate(prev, next, a, R) {
        if ((prev.binWidth || 0) !== (next.binWidth || 0)) { a.show(next); return; } // a re-cut jumps
        if (sim && JSON.stringify(prev.params || {}) !== JSON.stringify(next.params || {})) { a.show(next); return; } // new params re-run the stream: jump
        const hs0 = allHeights(R.shown), hs1 = allHeights(next), y0 = R.shown._yMax ?? yTop(R.shown, hs0), y1 = yTop(next, hs1);
        if (a.instant) { a.show(next); return; }
        if (sim && next.ran !== prev.ran) {
          const from = Math.round(R.shown.ran || 0), to = Math.round(next.ran || 0);
          if (to < from) { a.show(next); return; }
          const ms = Math.min(1200, 360 + 280 * Math.log10(Math.max(1, to - from)));
          return C.tween(0, 1, ms, (t) => { if (!a.alive()) return; a.show(t >= 1 ? next : { ...next, ran: Math.round(from + (to - from) * t), _yMax: y0 + (y1 - y0) * t }); }, 'standard');
        }
        const start = R.shown;
        return C.tween(0, 1, 600, (t) => { if (!a.alive()) return; a.show(t >= 1 ? next : { ...K.lerp(start, next, t), _yMax: y0 + (y1 - y0) * t }); });
      },
      render(view, R) {
        if (!chips.length && sim && !R.static) buildControls(R);
        const g = R.F.g, hsAll = allHeights(view), hsG = groups ? groups.map((_, k) => heights(view, k)) : [heights(view, 0)];
        const top = view._yMax ?? yTop(view, hsAll), bot = yBot(hsAll);
        const yLabel = params.yLabel ?? (proportion ? 'Proportion' : 'Count');
        const legendH = groups ? 18 : 0;
        const ml = K.yMargin(bot, top, H - 70, fmtY, logY), mt = 26 + legendH, mb = params.xLabel ? 46 : 30, mr = 12;
        const sy = logY ? K.logScale([bot, top], [H - mb, mt]) : C.scale([bot, top], [H - mb, mt]);
        const pw = W - ml - mr, n = cats.length;
        /* item 298: xAxis "value" sets each category at its value on a numeric axis (params.x), and state.transform
           { a, b } moves it to a*x + b, so aX + b slides along the axis */
        const valueAxis = !binned && (params.xAxis === 'value' || Array.isArray(params.x));
        const tf = view.transform || {}, ta = Number.isFinite(+tf.a) ? +tf.a : 1, tb = Number.isFinite(+tf.b) ? +tf.b : 0;
        const vals0 = valueAxis ? cats.map((_, k) => valOf(k)) : [];
        const xr = valueAxis ? (Array.isArray(params.x) ? params.x : (() => { const lo = Math.min(...vals0), hi = Math.max(...vals0), pad = (hi - lo || 1) * 0.15; return [lo - pad, hi + pad]; })()) : null;
        const sxv = valueAxis ? C.scale(xr, [ml, W - mr]) : null;
        const minGap = valueAxis ? Math.max(1e-9, Math.min(...vals0.slice().sort((u, w) => u - w).slice(1).map((v, k, arr) => v - (k ? arr[k - 1] : Math.min(...vals0))).filter((d) => d > 1e-9), 1)) : 1;
        const band = valueAxis ? Math.abs(sxv(xr[0] + minGap * ta) - sxv(xr[0])) : pw / Math.max(1, n), gap = binned ? 0 : Math.min(14, band * 0.22);
        const x = (i) => (valueAxis ? sxv(ta * vals0[i] + tb) - band / 2 + gap / 2 : ml + i * band + gap / 2), bw = Math.max(1, band - gap);
        const sub = bw / G;
        if (valueAxis) K.chartAxes(g, sxv, sy, { yLabel, xLabel: params.xLabel, fmtY, baseline: bot > 0 ? bot : 0 });
        else K.chartAxes(g, { range: [ml, W - mr], domain: [0, 1] }, sy, { yLabel, xLabel: params.xLabel, fmtY, noX: true, xTicks: binned ? null : { ticks: [], step: 1 }, baseline: logY ? null : bot > 0 ? bot : 0 });
        /* category labels or bin edges */
        const every = Math.max(1, Math.ceil(Math.max(...cats.map((c) => K.tw(c.label, 12))) / (band - 4)));
        if (binned) {
          const edges = cats.map((c) => c.lo).concat(cats.length ? [cats[cats.length - 1].hi] : []);
          const ev = Math.max(1, Math.ceil(Math.max(...edges.map((e) => K.tw(K.fmt(e, 4), 12) + 8)) / band));
          edges.forEach((e, i) => { if (i % ev) return; const px = ml + i * band; g.append(svg('line', { x1: px, x2: px, y1: H - mb, y2: H - mb + 4, class: 'cvb-axis thin' }), K.txt(px, H - mb + 15, K.fmt(e, 4), { cls: 'cvb-tick', size: 12 })); });
        } else if (!valueAxis) {
          cats.forEach((c, i) => { if (i % every) return; g.append(K.lab(x(i) + bw / 2, H - mb + 15, c.label, { cls: 'cvb-tick', size: 12, h: 22 })); });
        }
        if (groups) { // legend, top right
          let lx = W - mr; [...groups].reverse().forEach((q) => { const w = K.tw(q.label, 12) + 22; lx -= w; const o = K.obj('legend-' + q.id, '', q.colour); o.append(svg('rect', { x: lx, y: 8, width: 11, height: 11, rx: 2, class: 'cvb-bar' }), K.txt(lx + 15, 14, q.label, { anchor: 'start', size: 12 })); g.append(o); });
        }
        const sel = new Set(view.selected || []);
        /* item 322: cut: { at, side: "above" | "below", colour } recolours every bar beyond a cut on the category value
           (a slider binds "cut.at") */
        const cut = view.cut && Number.isFinite(+view.cut.at) ? view.cut : null;
        const beyond = (i) => cut && (cut.side === 'below' ? valOf(i) <= +cut.at + 1e-9 : valOf(i) >= +cut.at - 1e-9);
        const bars = svg('g'), vals = svg('g');
        const base = logY ? bot : bot > 0 ? bot : 0;
        cats.forEach((c, i) => {
          const faded = [].concat(view.dim || []).map(String).some((k) => k === c.id || k === c.label) || (params.categories || []).some((q) => K.isObj(q) && q.dim && (q.id || 'x' + q.label) === c.id); // item 266
          const colour0 = ((view.colours || {})[c.id] ?? (view.colours || {})[c.label]) || (beyond(i) ? cut.colour || 3 : null);
          hsG.forEach((hs, k) => {
            const v = hs[i] || 0; if (logY && !(v > 0)) return;
            const y = sy(Math.max(base, v)), h = Math.abs(sy(Math.min(base, v)) - y), id = groups ? `${c.id}-${groups[k].id}` : c.id, xb = x(i) + k * sub;
            const o = K.obj(id, 'cvb-bar-o' + (sel.has(id) ? ' is-on' : '') + (faded ? ' is-faded' : ''), (groups ? (colour0 && !beyond(i) ? colour0 : beyond(i) ? colour0 : groups[k].colour) : colour0 || c.colour || params.colour || 1)); // per-category colour (series slot), patchable through state.colours
            o.append(K.washRect(xb - 3, sy(top) - 2, sub + 6, sy(bot) - sy(top) + 4, 4));
            if (R.mode === 'tap') o.append(svg('rect', { x: xb, y: sy(top), width: sub, height: sy(bot) - sy(top), class: 'cvb-selw' }));
            o.append(svg('rect', { x: xb + (binned ? 0.5 : 0), y, width: Math.max(0, sub - (binned ? 1 : groups ? 1 : 0)), height: h, rx: binned ? 0 : 2, class: 'cvb-bar cv-body' }));
            if (R.mode === 'tap') o.append(svg('rect', { x: xb, y: sy(top), width: sub, height: sy(bot) - sy(top), class: 'cvb-tapbox', fill: 'transparent' }));
            if (params.showValues && (v || sim)) vals.append(K.txt(xb + sub / 2, v < 0 ? Math.min(sy(v) + 11, H - mb - 8) : Math.min(y - 9, sy(base) - 9), fmtV(v), { size: groups ? 11 : 12, cls: 'cvb-muted', halo: true })); // item 263: never on the category labels
            R.tappable(o, id, groups ? `${c.label}, ${groups[k].label}` : c.label);
            bars.append(o);
          });
        });
        g.append(bars, vals);
        /* the x pixel of a value on the category axis: bins and value axes are linear; numeric categories interpolate */
        const pxOf = (() => {
          if (valueAxis) return (v) => sxv(ta * v + tb);
          if (binned) return (v) => ml + (v - params.bins.min) / (binW || params.bins.width) * band;
          const num = cats.map((_, k) => [valOf(k), x(k) + bw / 2]).filter(([v]) => Number.isFinite(v));
          if (num.length < 2) return null;
          const [v0, p0] = num[0], [v1, p1] = num[num.length - 1];
          return (v) => p0 + (v - v0) / ((v1 - v0) || 1) * (p1 - p0);
        })();
        /* items 308, 309, 316: curves over the bars, { id, expr: "f(x)", colour, dashed, label, shade: { from, to } };
           the expression reads params, state.params and w (the bin width), so it follows sliders; shade fills under it */
        const P = { ...(params.params || {}), ...(view.params || {}), w: binned ? (binW || params.bins.width) : minGap };
        const cplot = svg('g', { 'clip-path': R.clipRect(ml, sy(top) - 2, pw, sy(bot) - sy(top) + 4, 'curves') }), clabs = [];
        for (const cv of [].concat(params.curves || [], view.curves || [])) {
          if (!cv || !pxOf || cv.expr == null) continue;
          const f = K.fnOf(String(cv.expr), Object.keys(P)), inv = (px) => { let lo = -1e6, hi = 1e6; for (let k = 0; k < 60; k++) { const m = (lo + hi) / 2; if (pxOf(m) < px) lo = m; else hi = m; } return (lo + hi) / 2; };
          const vA = inv(ml), vB = inv(W - mr), N = 240, pts = [];
          for (let k = 0; k <= N; k++) { const v = vA + (vB - vA) * k / N, y = f(v, P); if (Number.isFinite(y) && (!logY || y > 0)) pts.push([pxOf(v), sy(y), v]); }
          if (pts.length < 2) continue;
          const o = K.obj(cv.id || 'curve', 'cvb-curve', cv.colour || 'ink');
          if (cv.shade && (cv.shade.from != null || cv.shade.to != null)) {
            const a = cv.shade.from ?? -Infinity, b = cv.shade.to ?? Infinity, inside = pts.filter((q) => q[2] >= a && q[2] <= b);
            if (inside.length > 1) { const dd = `M${inside[0][0].toFixed(1)},${sy(base).toFixed(1)}` + inside.map((q) => `L${q[0].toFixed(1)},${q[1].toFixed(1)}`).join('') + `L${inside[inside.length - 1][0].toFixed(1)},${sy(base).toFixed(1)}Z`; const so = K.obj((cv.id || 'curve') + '-shade', 'cvb-under', cv.shade.colour || cv.colour || 3); so.append(svg('path', { d: dd, class: 'cvb-hlw' }), svg('path', { d: dd, class: 'cvb-wash-f cvb-hatch' })); cplot.append(so); }
          }
          const d = 'M' + pts.map((q) => `${q[0].toFixed(1)},${q[1].toFixed(1)}`).join('L');
          o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln' + (cv.dashed === false ? '' : ' cvb-dash') }));
          cplot.append(o);
          if (cv.label) { const q = pts[Math.floor(pts.length * 0.75)]; clabs.push(K.lab(q[0] + 6, q[1] - 12, cv.label, { anchor: 'start', halo: true, cls: 'cvb-strong' })); }
        }
        g.append(cplot); clabs.forEach((l) => g.append(l));
        /* item 332: horizontal reference lines, hlines: [{ id, y, label, dashed, colour }] in params or state */
        [].concat(params.hlines || [], view.hlines || []).forEach((hl, k) => {
          if (!hl || !Number.isFinite(+hl.y)) return; const yy = sy(+hl.y); if (yy < sy(top) - 0.5 || yy > sy(bot) + 0.5) return;
          const o = K.obj(hl.id || 'hline' + k, '', hl.colour || 'muted');
          o.append(svg('line', { x1: ml, x2: W - mr, y1: yy, y2: yy, class: 'cvb-ln thin' + (hl.dashed === false ? '' : ' cvb-dash') }));
          if (hl.label) o.append(K.lab(W - mr - 4, yy - 10, String(hl.label), { anchor: 'end', halo: true, cls: 'cvb-strong', size: 12 }));
          g.append(o);
        });
        /* item 322: the cut line itself, with its label */
        if (cut && pxOf && cut.line !== false) { const px = pxOf(+cut.at) + (binned ? 0 : (cut.side === 'below' ? 1 : -1) * band / 2); const o = K.obj('cut', '', 'ink'); o.append(svg('line', { x1: px, x2: px, y1: sy(bot), y2: sy(top), class: 'cvb-ln thin cvb-dash' })); if (cut.label) o.append(K.lab(px + 4, sy(top) + 8, String(cut.label).replace('{at}', K.fmt(+cut.at, 3)), { anchor: 'start', halo: true, cls: 'cvb-strong' })); g.append(o); }
        /* item 301: a balance point. state.pivot (a value on the category axis) draws a fulcrum under the axis, draggable
           in drag mode or with drag: true (a drag-point target is then a number); showMean draws the weighted mean */
        geo = { pxOf: valueAxis ? sxv : pxOf, ml, mr, band, binned };
        const bottomPx = sy(bot);
        if (pxOf && (view.showMean ?? params.showMean)) {
          let sw = 0, sv = 0; hsG[0].forEach((h, k) => { const v = valOf(k); if (Number.isFinite(v) && h > 0) { sw += h; sv += h * (valueAxis ? ta * v + tb : v); } });
          if (sw > 0) { const m = sv / sw, px = valueAxis ? sxv(m) : pxOf(m), o = K.obj('mean', '', 'ink'); o.append(svg('line', { x1: px, x2: px, y1: bottomPx, y2: sy(top), class: 'cvb-ln thin cvb-dash' }), K.lab(px + 4, sy(top) + 8, `$\\text{mean} = ${K.fmt(m, 3)}$`, { anchor: 'start', halo: true })); g.append(o); }
        }
        if (pxOf && view.pivot != null && Number.isFinite(+view.pivot)) {
          const pv = +view.pivot, px = valueAxis ? sxv(pv) : pxOf(pv), o = K.obj('pivot', 'cvb-pivot', canDrag(view, R) ? 'manip' : 'ink');
          o.append(svg('path', { d: `M${px},${bottomPx}L${px - 9},${bottomPx + 14}L${px + 9},${bottomPx + 14}Z`, class: 'cvb-head' }));
          g.append(o);
          if (canDrag(view, R)) g.append(K.handle(px, bottomPx + 8, 'pivot', { r: 9, label: 'Balance point' }));
        }
        /* exact value lines over each bar: dashed ink */
        if (exact.length && view.showExact !== false) {
          const eg = K.obj('exact', 'cvb-exact-g', 'ink');
          for (const e of exact) {
            const y = sy(e.y), o = K.obj('exact-' + cats[e.i].id, '', 'ink');
            o.append(K.washRect(x(e.i) - 6, y - 5, bw + 12, 10, 3), svg('line', { x1: x(e.i) - 4, x2: x(e.i) + bw + 4, y1: y, y2: y, class: 'cvb-exact' }));
            eg.append(o);
          }
          g.append(eg);
          if (params.exactLabel !== false && exact.length) {
            const last = exact.reduce((a, b) => (sy(b.y) < sy(a.y) ? b : a));
            const t = params.exactLabel || 'exact';
            const lx = x(last.i) + bw + 8, anchor = lx + K.tw(t) > W - 4 ? 'end' : 'start';
            g.append(K.txt(anchor === 'start' ? lx : x(last.i) - 8, sy(last.y), t, { anchor, size: 12, halo: true, cls: 'cvb-muted' }));
          }
        }
        if (countEl) {
          const n = Math.round(view.ran || 0);
          countEl.textContent = simErr ? 'Simulation unavailable' : n.toLocaleString('en-GB') + (n === 1 ? ' trial' : ' trials') + (sim.filter != null && discarded && n ? ` (${discarded.toLocaleString('en-GB')} discarded)` : '');
          chips.forEach((b) => { b.disabled = R.locked || R.static; });
        }
      },
      methods: (R) => ({
        /* Run n more trials (as the chips do). Returns the animation promise. */
        run: (n) => R.inst.set({ ran: Math.round(R.state.ran || 0) + n }),
        reset: () => R.inst.set({ ran: 0 }, { instant: true }),
        /* Current heights by category id: proportions or counts as drawn. */
        values: () => (groups ? Object.fromEntries(groups.flatMap((q, k) => { const hs = heights(R.state, k); return cats.map((c, i) => [`${c.id}-${q.id}`, hs[i]]); })) : Object.fromEntries(cats.map((c, i) => [c.id, heights(R.state)[i]]))),
        counts: () => Object.fromEntries(cats.map((c, i) => [c.id, tally(Math.round(R.state.ran || 0), R.state)[i]])),
        discarded: () => discarded,
        points: () => (R.state.pivot != null ? { pivot: { x: +R.state.pivot, y: 0 } } : {}),
        place: (id, pos, opts = {}) => (id === 'pivot' ? R.inst.set({ pivot: Array.isArray(pos) ? pos[0] : +pos }, opts) : Promise.resolve()),
        /* Explore controls: bind a category (its label or id, or "values.<label>") to move that bar's height */
        /* a name that is no category is a free parameter in state.params, for a derive block to read */
        setParam: (name, v) => { if (binned && (name === 'binWidth' || name === 'bins.width')) { R.inst.set({ binWidth: +v }, { instant: true }); return; } const i = catIndex(String(name).replace(/^values\./, '')); if (i >= 0) R.inst.set({ values: { [cats[i].label]: +v } }, { instant: true }); else R.inst.set(Z.canvas.paramPatch(name, v), { instant: true }); },
        getParam: (name) => { if (binned && (name === 'binWidth' || name === 'bins.width')) return R.state.binWidth || params.bins.width; const i = catIndex(String(name).replace(/^values\./, '')); return i >= 0 ? heights(R.state)[i] : ((R.state.params || {})[name]); },
      }),
    };
    return K.make(host, params, ctx, def);
  });
})();
