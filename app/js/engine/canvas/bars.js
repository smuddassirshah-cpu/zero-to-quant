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
    const rebin = (view) => { const w = (view && view.binWidth) || params.bins.width; if (binned && w !== binW) { binW = w; cats = binsFor(w); } };
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

    /* Seeded outcomes: outcomes[i] is the same trial every time, so 10 then 100 shows the first 110. */
    const outcomes = [];
    let simRng = null, simErr = null;
    const ensure = (n) => {
      if (!sim || simErr) return;
      try {
        if (!simRng) simRng = K.rngFor(sim.seed ?? 1);
        while (outcomes.length < n) outcomes.push(Z.sim.outcome(sim.outcome, simRng));
      } catch (e) { simErr = e; console.warn('bars sim:', e.message); }
    };
    const tally = (n) => {
      ensure(n); const counts = new Array(cats.length).fill(0);
      for (let i = 0; i < Math.min(n, outcomes.length); i++) { const v = outcomes[i]; const j = binned ? catIndex(+v) : catIndex(typeof v === 'boolean' ? +v : v); if (j >= 0) counts[j]++; }
      return counts;
    };
    const heights = (view) => {
      rebin(view);
      if (binned && Array.isArray(params.data)) { // raw observations: counts (or proportions) in the current bins
        const counts = new Array(cats.length).fill(0); params.data.forEach((v) => { const j = catIndex(+v); if (j >= 0) counts[j]++; else if (+v === params.bins.max) counts[cats.length - 1]++; });
        return counts.map((c) => (proportion ? (params.data.length ? c / params.data.length : 0) : c));
      }
      if (sim && view.ran != null && !(view.values && Object.keys(view.values).length && !view.ran)) {
        const n = Math.round(view.ran), counts = tally(n);
        return counts.map((c) => (proportion ? (n ? c / n : 0) : c));
      }
      const v = view.values || {}; const out = new Array(cats.length).fill(0);
      for (const [k, val] of Object.entries(v)) { const i = catIndex(k); if (i >= 0) out[i] = +val || 0; }
      for (const [i, c] of (params.categories || []).entries()) if (K.isObj(c) && c.value != null && !(c.label in v) && !((c.id || 'x' + c.label) in v)) out[i] = +c.value;
      return out;
    };
    const yTop = (view, hs) => {
      if (params.yMax != null) return params.yMax;
      const m = Math.max(...hs, ...exact.map((e) => e.y * (sim ? 1.6 : 1.1)), proportion ? 0.05 : 1);
      const t = C.niceTicks(0, m * 1.08, 5); return t[t.length - 1] >= m * 1.02 ? t[t.length - 1] : m * 1.15;
    };
    /* item 133: negative values hang below a zero baseline; the axis runs down to a nice tick under the lowest bar */
    const yBot = (hs) => {
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

    const def = {
      kind: 'bars', aria: params.aria || 'Bar chart',
      modes: ['tap', 'slider'],
      size: () => ({ w: W, h: H }),
      init: () => ({ values: {}, ran: sim ? 0 : undefined, highlight: [], params: {} }),
      prepare(patch) {
        if (patch.params && patch.params.trials != null) patch.ran = Math.round(patch.params.trials);
        if (patch.reset) { patch.ran = 0; delete patch.reset; }
        return patch;
      },
      animate(prev, next, a, R) {
        if ((prev.binWidth || 0) !== (next.binWidth || 0)) { a.show(next); return; } // a re-cut jumps
        const hs0 = heights(R.shown), hs1 = heights(next), y0 = R.shown._yMax ?? yTop(R.shown, hs0), y1 = yTop(next, hs1);
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
        const g = R.F.g, hs = heights(view), top = view._yMax ?? yTop(view, hs), bot = yBot(hs);
        const yLabel = params.yLabel ?? (proportion ? 'Proportion' : 'Count');
        const ml = K.yMargin(bot, top, H - 70, fmtY), mt = 26, mb = params.xLabel ? 46 : 30, mr = 12;
        const sy = C.scale([bot, top], [H - mb, mt]);
        const pw = W - ml - mr, n = cats.length;
        const band = pw / Math.max(1, n), gap = binned ? 0 : Math.min(14, band * 0.22);
        const x = (i) => ml + i * band + gap / 2, bw = Math.max(1, band - gap);
        const xAxisTicks = binned ? null : { ticks: [], step: 1 };
        K.chartAxes(g, { range: [ml, W - mr], domain: [0, 1] }, sy, { yLabel, xLabel: params.xLabel, fmtY, noX: true, xTicks: xAxisTicks, baseline: bot > 0 ? bot : 0 });
        /* category labels or bin edges */
        const every = Math.max(1, Math.ceil(Math.max(...cats.map((c) => K.tw(c.label, 12))) / (band - 4)));
        if (binned) {
          const edges = cats.map((c) => c.lo).concat(cats.length ? [cats[cats.length - 1].hi] : []);
          const ev = Math.max(1, Math.ceil(Math.max(...edges.map((e) => K.tw(K.fmt(e, 4), 12) + 8)) / band));
          edges.forEach((e, i) => { if (i % ev) return; const px = ml + i * band; g.append(svg('line', { x1: px, x2: px, y1: H - mb, y2: H - mb + 4, class: 'cvb-axis thin' }), K.txt(px, H - mb + 15, K.fmt(e, 4), { cls: 'cvb-tick', size: 12 })); });
        } else {
          cats.forEach((c, i) => { if (i % every) return; g.append(K.lab(x(i) + bw / 2, H - mb + 15, c.label, { cls: 'cvb-tick', size: 12, h: 22 })); });
        }
        const sel = new Set(view.selected || []);
        const bars = svg('g'), vals = svg('g');
        cats.forEach((c, i) => {
          const base = bot > 0 ? bot : 0, v = hs[i] || 0, y = sy(Math.max(base, v)), h = Math.abs(sy(Math.min(base, v)) - y);
          const o = K.obj(c.id, 'cvb-bar-o' + (sel.has(c.id) ? ' is-on' : ''), ((view.colours || {})[c.id] ?? (view.colours || {})[c.label]) || c.colour || params.colour || 1); // per-category colour (series slot), patchable through state.colours
          o.append(K.washRect(x(i) - 3, sy(top) - 2, bw + 6, sy(bot) - sy(top) + 4, 4));
          if (R.mode === 'tap') o.append(svg('rect', { x: x(i), y: sy(top), width: bw, height: sy(bot) - sy(top), class: 'cvb-selw' }));
          o.append(svg('rect', { x: x(i) + (binned ? 0.5 : 0), y, width: Math.max(0, bw - (binned ? 1 : 0)), height: h, rx: binned ? 0 : 2, class: 'cvb-bar cv-body' }));
          if (R.mode === 'tap') o.append(svg('rect', { x: x(i), y: sy(top), width: bw, height: sy(bot) - sy(top), class: 'cvb-tapbox', fill: 'transparent' }));
          if (params.showValues && (v || sim)) vals.append(K.txt(x(i) + bw / 2, v < 0 ? sy(v) + 11 : y - 9, fmtV(v), { size: 12, cls: 'cvb-muted' }));
          R.tappable(o, c.id, c.label);
          bars.append(o);
        });
        g.append(bars, vals);
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
          countEl.textContent = simErr ? 'Simulation unavailable' : n.toLocaleString('en-GB') + (n === 1 ? ' trial' : ' trials');
          chips.forEach((b) => { b.disabled = R.locked || R.static; });
        }
      },
      methods: (R) => ({
        /* Run n more trials (as the chips do). Returns the animation promise. */
        run: (n) => R.inst.set({ ran: Math.round(R.state.ran || 0) + n }),
        reset: () => R.inst.set({ ran: 0 }, { instant: true }),
        /* Current heights by category id: proportions or counts as drawn. */
        values: () => Object.fromEntries(cats.map((c, i) => [c.id, heights(R.state)[i]])),
        counts: () => Object.fromEntries(cats.map((c, i) => [c.id, tally(Math.round(R.state.ran || 0))[i]])),
        /* Explore controls: bind a category (its label or id, or "values.<label>") to move that bar's height */
        /* a name that is no category is a free parameter in state.params, for a derive block to read */
        setParam: (name, v) => { if (binned && (name === 'binWidth' || name === 'bins.width')) { R.inst.set({ binWidth: +v }, { instant: true }); return; } const i = catIndex(String(name).replace(/^values\./, '')); if (i >= 0) R.inst.set({ values: { [cats[i].label]: +v } }, { instant: true }); else R.inst.set({ params: { [name]: +v } }, { instant: true }); },
        getParam: (name) => { if (binned && (name === 'binWidth' || name === 'bins.width')) return R.state.binWidth || params.bins.width; const i = catIndex(String(name).replace(/^values\./, '')); return i >= 0 ? heights(R.state)[i] : ((R.state.params || {})[name]); },
      }),
    };
    return K.make(host, params, ctx, def);
  });
})();
