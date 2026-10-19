/* series: time series lines (prices, returns, P&L) with candles, markers, shaded ranges, a window and a reveal.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js). */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;
  const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  C.register('series', (host, params, ctx) => {
    const K = Z.cvb;
    const W = 540, H = params.height || 300;
    const list = (params.series || []).map((s, i) => ({ ...s, id: s.id || 's' + i, slot: s.colour || i + 1 }));
    const n = Math.max(1, ...list.map((s) => (s.values || s.ohlc || []).length));
    const dates = params.x === 'dates' ? (params.dates || []).map((d) => new Date(d + (String(d).length <= 10 ? 'T00:00:00Z' : ''))) : null;
    const fmtPct = (v, st) => K.fmtTick(v * 100, st * 100) + '%';
    const fmtY = params.format === 'pct' ? fmtPct : params.format === 'money' || params.money ? (v, st) => (v < 0 ? '−' : '') + (params.money || params.currency || '$') + K.fmtTick(Math.abs(v), st) : null;
    /* Marker {value} labels. `decimals` fixes the places and keeps trailing zeros; `money: "£"` is format money with
       that currency and two places unless `decimals` says otherwise */
    const money = params.money || (params.format === 'money' ? params.currency || '$' : null), dec = params.decimals ?? (params.money ? 2 : null);
    const num = (v, dp, d0 = dec) => (d0 != null ? Math.abs(v).toLocaleString('en-GB', { minimumFractionDigits: d0, maximumFractionDigits: d0 }) : K.fmt(Math.abs(v), dp));
    const fmtVal = (v, d0 = dec) => (params.format === 'pct' ? (v < 0 ? '−' : '') + num(v * 100, 1, d0) + '%' : money ? (v < 0 ? '−' : '') + money + num(v, 2, d0) : (v < 0 ? '−' : '') + num(v, 2, d0));
    const valuesOf = (s) => (s.values || (s.ohlc ? s.ohlc.map((c) => c[3]) : []));
    const yRange = (() => {
      if (params.y) return params.y;
      let lo = Infinity, hi = -Infinity;
      for (const s of list) { for (const v of valuesOf(s)) { if (Number.isFinite(v)) { lo = Math.min(lo, v); hi = Math.max(hi, v); } } for (const c of s.ohlc || []) { lo = Math.min(lo, c[2]); hi = Math.max(hi, c[1]); } }
      if (params.yScale === 'log') { // positive values only, padded by a ratio
        let plo = Infinity; for (const s of list) for (const v of valuesOf(s)) if (Number.isFinite(v) && v > 0) plo = Math.min(plo, v);
        return Number.isFinite(plo) ? [plo / 1.08, hi * 1.08] : [1, 10];
      }
      if (params.baseline != null) { lo = Math.min(lo, params.baseline); hi = Math.max(hi, params.baseline); }
      if (!Number.isFinite(lo)) return [0, 1];
      const pad = (hi - lo || 1) * 0.08; const t = C.niceTicks(lo - pad, hi + pad, 5); const st = t[1] - t[0] || 1;
      return [Math.floor((lo - pad) / st) * st, Math.ceil((hi + pad) / st) * st];
    })();
    const labelW = Math.max(0, ...list.filter((s) => s.label).map((s) => K.tw(s.label) + 22));
    const logY = params.yScale === 'log';
    /* item 186: a second y axis on the right; series with axis: 2 use it (params.y2 range, y2Label, y2Format "pct" | "money") */
    const right = list.filter((s) => s.axis === 2);
    const fmtY2 = params.y2Format === 'pct' ? fmtPct : params.y2Format === 'money' ? (v, st) => (v < 0 ? '−' : '') + (params.money || params.currency || '$') + K.fmtTick(Math.abs(v), st) : null;
    const y2Range = !right.length ? null : params.y2 || (() => {
      let lo = Infinity, hi = -Infinity; for (const s2 of right) for (const v of valuesOf(s2)) if (Number.isFinite(v)) { lo = Math.min(lo, v); hi = Math.max(hi, v); }
      if (!Number.isFinite(lo)) return [0, 1];
      const pad = (hi - lo || 1) * 0.08, t = C.niceTicks(lo - pad, hi + pad, 5), st = t[1] - t[0] || 1;
      return [Math.floor((lo - pad) / st) * st, Math.ceil((hi + pad) / st) * st];
    })();
    const y2W = y2Range ? K.yMargin(y2Range[0], y2Range[1], H - 60, fmtY2) : 0;
    /* item 168: a title above the plot */
    const titleH = params.title ? 20 : 0;
    /* item 185: params.margins { left, right } fixes the plot's side margins, so stacked panels line up */
    const M = params.margins || {};
    const ml = M.left ?? K.yMargin(yRange[0], yRange[1], H - 60, fmtY, logY), mt = 26 + titleH, mb = params.xLabel ? 46 : 30, mr = M.right ?? Math.max(14, Math.min(150, labelW + y2W), y2W + 8);
    const hasCandles = list.some((s) => s.ohlc && (params.candles || s.candles)), padI = hasCandles ? 0.7 : 0;
    const sx = C.scale([-padI, n - 1 + padI], [ml, W - mr]), sy = logY ? K.logScale(yRange, [H - mb, mt]) : C.scale(yRange, [H - mb, mt]); // yScale: "log", for log-price charts
    const sy2 = y2Range ? C.scale(y2Range, [H - mb, mt]) : null, syOf = (s2) => (s2.axis === 2 && sy2 ? sy2 : sy);
    /* item 168: dateFormat for date ticks: %Y %y %m %d %e %b %B (for example "%b %Y", "%d/%m", "%Y-%m") */
    const MONTHS_L = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const strf = (d, f) => f.replace(/%([YymdebB%])/g, (_, c) => ({ Y: String(d.getUTCFullYear()), y: String(d.getUTCFullYear()).slice(2), m: String(d.getUTCMonth() + 1).padStart(2, '0'), d: String(d.getUTCDate()).padStart(2, '0'), e: String(d.getUTCDate()), b: MONTHS[d.getUTCMonth()], B: MONTHS_L[d.getUTCMonth()], '%': '%' })[c]);
    const fmtX = dates
      ? (i) => { const d = dates[Math.round(i)]; if (!d) return ''; if (params.dateFormat) return strf(d, String(params.dateFormat)); const span = (dates[dates.length - 1] - dates[0]) / 864e5; return span > 300 ? MONTHS[d.getUTCMonth()] + ' ' + String(d.getUTCFullYear()).slice(2) : d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()]; }
      : (i) => K.fmt(i + (params.indexFrom || 0), 2);
    const idxOf = (v) => { if (typeof v === 'number') return v; if (dates && typeof v === 'string') { const t = new Date(v + (v.length <= 10 ? 'T00:00:00Z' : '')).getTime(); let best = 0; dates.forEach((d, i) => { if (Math.abs(d - t) < Math.abs(dates[best] - t)) best = i; }); return best; } return 0; };
    /* Maximum drawdown: the largest fall from a running peak, as a share of the peak (abs: true measures the fall itself,
       for cumulative P&L that starts at zero) */
    const drawdown = (vals, abs = false) => { let peak = -1, best = { dd: 0, fall: 0, from: 0, to: 0 }; vals.forEach((v, i) => { if (!Number.isFinite(v)) return; if (peak < 0 || v > vals[peak]) peak = i; const fall = vals[peak] - v, dd = abs ? fall : vals[peak] ? fall / vals[peak] : 0; if (dd > best.dd) best = { dd, fall, from: peak, to: i }; }); return best; };

    const def = {
      kind: 'series', aria: params.aria || 'Time series chart',
      modes: ['slider', 'tap'],
      size: () => ({ w: W, h: H }),
      listKeys: ['markers'],
      init: () => ({ markers: [], shade: [], window: null, reveal: 1, highlight: [], drawdown: false }),
      prepare(patch) { if (Array.isArray(patch.window)) patch.window = { from: patch.window[0], to: patch.window[1] }; return patch; },
      render(view, R) {
        const g = R.F.g, x0 = ml, x1 = W - mr, y0 = H - mb, y1 = mt;
        const xt = K.ticksFor(0, n - 1, x1 - x0, { minGap: 56, fmtF: (v) => fmtX(v) });
        xt.ticks = xt.ticks.filter((v) => Number.isInteger(v) && v >= 0 && v <= n - 1);
        K.chartAxes(g, sx, sy, { yLabel: params.yLabel, xLabel: params.xLabel, fmtY, fmtX: (v) => fmtX(v), xTicks: xt, baseline: logY ? null : params.baseline ?? (yRange[0] < 0 && yRange[1] > 0 ? 0 : null) });
        if (params.title) g.append(K.lab(x0, 14, String(params.title), { anchor: 'start', cls: 'cvb-title', size: 14 }));
        if (sy2) { // the right-hand axis
          const t2 = K.ticksFor(y2Range[0], y2Range[1], y0 - y1, { minGap: 24, fmtF: fmtY2, vertical: true }), ax = svg('g', { class: 'cvb-axes' });
          ax.append(svg('line', { x1: x1, x2: x1, y1: y0, y2: y1, class: 'cvb-axis' }));
          t2.ticks.forEach((v) => { const yy = sy2(v); if (yy < y1 - 0.5 || yy > y0 + 0.5) return; ax.append(svg('line', { x1: x1, x2: x1 + 4, y1: yy, y2: yy, class: 'cvb-axis thin' }), K.txt(x1 + 7, yy, fmtY2 ? fmtY2(v, t2.step) : K.fmtTick(v, t2.step), { anchor: 'start', cls: 'cvb-tick', size: 12 })); });
          if (params.y2Label) ax.append(K.lab(x1 + 6, y1 - 16, params.y2Label, { anchor: 'end', cls: 'cvb-axlab' }));
          g.append(ax);
        }
        const back = svg('g'), plot = svg('g', { 'clip-path': R.clipRect(x0 - 1, y1 - 4, x1 - x0 + 2, y0 - y1 + 8) }), over = svg('g');
        g.append(back, plot, over);
        const fixed = [];
        /* shaded ranges, drawdown and the window behind the lines */
        const shades = [].concat(view.shade || []);
        /* drawdown: true labels the fall as a percentage of the peak; drawdown: "money" (or "abs") labels the absolute fall in
           the series' money format, for P&L that starts at zero */
        if (view.drawdown && list[0]) {
          const abs = view.drawdown === 'money' || view.drawdown === 'abs', dd = drawdown(valuesOf(list[0]), abs);
          const amount = view.drawdown === 'money' ? '−' + (money || '£') + num(dd.fall, 2) : abs ? '−' + num(dd.fall, 2) : '−' + K.fmt(dd.dd * 100, 1) + '%';
          if (dd.dd > 0) shades.push({ id: 'drawdown', from: dd.from, to: dd.to, label: (params.drawdownLabel || 'Max drawdown') + ' ' + amount, tone: 'neg' });
        }
        shades.forEach((s, i) => {
          const a = sx(idxOf(s.from)), b = sx(idxOf(s.to)), o = K.obj(s.id || 'shade' + i, '', s.tone === 'neg' ? 'neg' : s.tone === 'pos' ? 'pos' : 'muted');
          o.append(K.washRect(a, y1, b - a, y0 - y1, 0), svg('rect', { x: a, y: y1, width: Math.max(1, b - a), height: y0 - y1, class: 'cvb-shade' }));
          back.append(o);
          if (s.label) { const lx = K.clamp((a + b) / 2, x0 + K.tw(s.label) / 2 + 2, x1 - K.tw(s.label) / 2 - 2); over.append(K.txt(lx, y1 + 10, s.label, { halo: true, size: 12, cls: 'cvb-strong' })); fixed.push(K.boxOf({ x: lx, y: y1 + 10, text: s.label })); }
        });
        if (view.window && view.window.from != null) {
          const a = sx(idxOf(view.window.from)), b = sx(idxOf(view.window.to ?? n - 1)), o = K.obj('window', '', 'manip');
          o.append(K.washRect(a, y1, b - a, y0 - y1, 0), svg('rect', { x: a, y: y1, width: Math.max(1, b - a), height: y0 - y1, class: 'cvb-window' }));
          back.append(o);
          if (view.window.label) { over.append(K.txt((a + b) / 2, y0 - 10, view.window.label, { halo: true, size: 12, cls: 'cvb-strong' })); }
        }
        const reveal = K.clamp(view.reveal ?? 1, 0, 1), last = reveal * (n - 1);
        const ends = [];
        for (const s of list) {
          if ((view.hide || []).includes(s.id)) continue;
          const o = K.obj(s.id, '', s.slot);
          if (s.ohlc && (params.candles || s.candles)) {
            const bw = Math.max(1.5, Math.min(14, (x1 - x0) / n * 0.62));
            s.ohlc.forEach((c, i) => {
              if (i > last + 1e-9) return;
              const up = c[3] >= c[0], cx = sx(i), cg = svg('g', { class: 'cv-obj', 'data-id': `${s.id}-${i}` });
              cg.append(svg('line', { x1: cx, x2: cx, y1: sy(c[1]), y2: sy(c[2]), class: 'cvb-wick ' + (up ? 'up' : 'dn'), 'stroke-width': 1.25 }));
              cg.append(svg('rect', { x: cx - bw / 2, y: sy(Math.max(c[0], c[3])), width: bw, height: Math.max(1, Math.abs(sy(c[0]) - sy(c[3]))), class: 'cvb-candle ' + (up ? 'up' : 'dn'), 'stroke-width': 1.25 }));
              o.append(cg);
            });
          } else {
            const vals = valuesOf(s), syS = syOf(s); let d = '', pen = false;
            const upto = Math.floor(last);
            const pts = []; // runs of finite points, for the line and the fill
            for (let i = 0; i <= Math.min(upto, vals.length - 1); i++) { const v = vals[i]; if (!Number.isFinite(v)) { pen = false; continue; } d += (pen ? 'L' : 'M') + sx(i).toFixed(2) + ',' + syS(v).toFixed(2); if (!pen) pts.push([]); pts[pts.length - 1].push([sx(i), syS(v)]); pen = true; }
            if (last > upto && upto + 1 < vals.length && Number.isFinite(vals[upto]) && Number.isFinite(vals[upto + 1])) { const f = last - upto, v = vals[upto] + (vals[upto + 1] - vals[upto]) * f; d += 'L' + sx(last).toFixed(2) + ',' + syS(v).toFixed(2); if (pts.length) pts[pts.length - 1].push([sx(last), syS(v)]); }
            /* item 171: fill "below" shades between the line and zero (or the baseline), as fill_between does */
            if (s.fill && pts.length) {
              const base = s.fillTo ?? params.baseline ?? 0, by = K.clamp(syS(K.clamp(base, Math.min(...(s.axis === 2 ? y2Range : yRange)), Math.max(...(s.axis === 2 ? y2Range : yRange)))), y1, y0);
              pts.filter((run) => run.length > 1).forEach((run) => o.append(svg('path', { d: `M${run[0][0].toFixed(2)},${by.toFixed(2)}` + run.map((q) => `L${q[0].toFixed(2)},${q[1].toFixed(2)}`).join('') + `L${run[run.length - 1][0].toFixed(2)},${by.toFixed(2)}Z`, class: 'cvb-fill' })));
            }
            o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln' + (s.dashed ? ' cvb-dash' : '') + (s.thin ? ' thin' : '') }));
            const li = Math.min(vals.length - 1, Math.max(0, Math.round(last))); const lv = vals[li];
            if (s.label && Number.isFinite(lv)) ends.push({ x: sx(li), y: syS(lv), text: s.label, slot: s.slot, id: s.id });
          }
          plot.append(o);
        }
        /* direct labels at the line ends, spread so they never overlap */
        K.spread(ends.map((e) => { e.ly = e.y; return e; }).map((e) => Object.assign(e, { y: e.ly })), 16, y1 + 6, y0 - 6);
        for (const e of ends) {
          over.append(svg('circle', { cx: e.x, cy: e.ly, r: 3.5, class: 'cvb-dot ' + K.colourCls(e.slot) }));
          over.append(K.lab(e.x + 9, e.y, e.text, { anchor: 'start', halo: true, cls: 'cvb-strong' }));
        }
        /* markers */
        const labels = [];
        for (const m of view.markers || []) {
          const s = list.find((q) => q.id === m.series) || list[0]; if (!s) continue;
          const i = idxOf(m.i ?? m.at), v = m.y ?? valuesOf(s)[Math.round(i)]; if (!Number.isFinite(v) || i > last + 1e-9) continue;
          const o = K.obj(m.id, '', m.colour || 'ink'), cx = sx(i), cy = syOf(s)(v);
          o.append(K.washCircle(cx, cy, 11), svg('circle', { cx, cy, r: 5, class: 'cvb-dot' }));
          R.tappable(o, m.id, m.label);
          over.append(o);
          if (m.label) labels.push({ x: cx, y: cy + (m.below ? 16 : -15), text: String(m.label).replace('{value}', fmtVal(v, m.decimals)), anchor: 'middle' }); // item 181: per-marker decimals
        }
        K.placeLabels(labels, fixed, { x0, x1: W - 4, y0: y1, y1: y0 });
        for (const l of labels) over.append(K.lab(l.x, l.y, l.text, { anchor: l.anchor, halo: true, cls: 'cvb-strong' }));
      },
      methods: (R) => ({
        margins: () => ({ left: ml, right: mr }),
        maxDrawdown: (id, abs) => { const s = list.find((q) => q.id === id) || list[0]; return s ? drawdown(valuesOf(s), !!abs) : null; },
      }),
    };
    return K.make(host, params, ctx, def);
  });
})();
