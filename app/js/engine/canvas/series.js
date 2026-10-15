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
    const fmtY = params.format === 'pct' ? fmtPct : params.format === 'money' ? (v, st) => (v < 0 ? '−' : '') + (params.currency || '$') + K.fmtTick(Math.abs(v), st) : null;
    const fmtVal = (v) => (params.format === 'pct' ? K.fmt(v * 100, 1) + '%' : params.format === 'money' ? (v < 0 ? '−' : '') + (params.currency || '$') + K.fmt(Math.abs(v), 2) : K.fmt(v, 2));
    const valuesOf = (s) => (s.values || (s.ohlc ? s.ohlc.map((c) => c[3]) : []));
    const yRange = (() => {
      if (params.y) return params.y;
      let lo = Infinity, hi = -Infinity;
      for (const s of list) { for (const v of valuesOf(s)) { if (Number.isFinite(v)) { lo = Math.min(lo, v); hi = Math.max(hi, v); } } for (const c of s.ohlc || []) { lo = Math.min(lo, c[2]); hi = Math.max(hi, c[1]); } }
      if (params.baseline != null) { lo = Math.min(lo, params.baseline); hi = Math.max(hi, params.baseline); }
      if (!Number.isFinite(lo)) return [0, 1];
      const pad = (hi - lo || 1) * 0.08; const t = C.niceTicks(lo - pad, hi + pad, 5); const st = t[1] - t[0] || 1;
      return [Math.floor((lo - pad) / st) * st, Math.ceil((hi + pad) / st) * st];
    })();
    const labelW = Math.max(0, ...list.filter((s) => s.label).map((s) => K.tw(s.label) + 22));
    const ml = K.yMargin(yRange[0], yRange[1], H - 60, fmtY), mt = 26, mb = params.xLabel ? 46 : 30, mr = Math.max(14, Math.min(150, labelW));
    const sx = C.scale([0, n - 1], [ml, W - mr]), sy = C.scale(yRange, [H - mb, mt]);
    const fmtX = dates
      ? (i) => { const d = dates[Math.round(i)]; if (!d) return ''; const span = (dates[dates.length - 1] - dates[0]) / 864e5; return span > 300 ? MONTHS[d.getUTCMonth()] + ' ' + String(d.getUTCFullYear()).slice(2) : d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()]; }
      : (i) => K.fmt(i + (params.indexFrom || 0), 2);
    const idxOf = (v) => { if (typeof v === 'number') return v; if (dates && typeof v === 'string') { const t = new Date(v + (v.length <= 10 ? 'T00:00:00Z' : '')).getTime(); let best = 0; dates.forEach((d, i) => { if (Math.abs(d - t) < Math.abs(dates[best] - t)) best = i; }); return best; } return 0; };
    const drawdown = (vals) => { let peak = 0, best = { dd: 0, from: 0, to: 0 }; vals.forEach((v, i) => { if (v > vals[peak]) peak = i; const dd = (vals[peak] - v) / vals[peak]; if (dd > best.dd) best = { dd, from: peak, to: i }; }); return best; };

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
        xt.ticks = xt.ticks.filter((v) => Number.isInteger(v));
        K.chartAxes(g, sx, sy, { yLabel: params.yLabel, xLabel: params.xLabel, fmtY, fmtX: (v) => fmtX(v), xTicks: xt, baseline: params.baseline ?? (yRange[0] < 0 && yRange[1] > 0 ? 0 : null) });
        const back = svg('g'), plot = svg('g', { 'clip-path': R.clipRect(x0 - 1, y1 - 4, x1 - x0 + 2, y0 - y1 + 8) }), over = svg('g');
        g.append(back, plot, over);
        const fixed = [];
        /* shaded ranges, drawdown and the window behind the lines */
        const shades = [].concat(view.shade || []);
        if (view.drawdown && list[0]) { const dd = drawdown(valuesOf(list[0])); if (dd.dd > 0) shades.push({ id: 'drawdown', from: dd.from, to: dd.to, label: (params.drawdownLabel || 'Max drawdown') + ' −' + K.fmt(dd.dd * 100, 1) + '%', tone: 'neg' }); }
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
            const vals = valuesOf(s); let d = '', pen = false;
            const upto = Math.floor(last);
            for (let i = 0; i <= Math.min(upto, vals.length - 1); i++) { const v = vals[i]; if (!Number.isFinite(v)) { pen = false; continue; } d += (pen ? 'L' : 'M') + sx(i).toFixed(2) + ',' + sy(v).toFixed(2); pen = true; }
            if (last > upto && upto + 1 < vals.length && Number.isFinite(vals[upto]) && Number.isFinite(vals[upto + 1])) { const f = last - upto, v = vals[upto] + (vals[upto + 1] - vals[upto]) * f; d += 'L' + sx(last).toFixed(2) + ',' + sy(v).toFixed(2); }
            o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln' + (s.dashed ? ' cvb-dash' : '') + (s.thin ? ' thin' : '') }));
            const li = Math.min(vals.length - 1, Math.max(0, Math.round(last))); const lv = vals[li];
            if (s.label && Number.isFinite(lv)) ends.push({ x: sx(li), y: sy(lv), text: s.label, slot: s.slot, id: s.id });
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
          const o = K.obj(m.id, '', m.colour || 'ink'), cx = sx(i), cy = sy(v);
          o.append(K.washCircle(cx, cy, 11), svg('circle', { cx, cy, r: 5, class: 'cvb-dot' }));
          R.tappable(o, m.id, m.label);
          over.append(o);
          if (m.label) labels.push({ x: cx, y: cy + (m.below ? 16 : -15), text: String(m.label).replace('{value}', fmtVal(v)), anchor: 'middle' });
        }
        K.placeLabels(labels, fixed, { x0, x1: W - 4, y0: y1, y1: y0 });
        for (const l of labels) over.append(K.lab(l.x, l.y, l.text, { anchor: l.anchor, halo: true, cls: 'cvb-strong' }));
      },
      methods: (R) => ({
        maxDrawdown: (id) => { const s = list.find((q) => q.id === id) || list[0]; return s ? drawdown(valuesOf(s)) : null; },
      }),
    };
    return K.make(host, params, ctx, def);
  });
})();
