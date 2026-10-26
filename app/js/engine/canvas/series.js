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
    /* item 327: a series may be simulated: sim: { outcome, seed, n: 1000, running: "mean" | "varp" | "var" | "sd" |
       "sum" | "none", let, filter } draws n seeded outcomes (params read by name) and plots the running statistic */
    /* item 443: band: k on a running-mean sim shades mean ± k·sd/√i (the sd of the draws so far) */
    const simValues = (sp, vars) => { try { const r = Z.sim.rng(sp.seed ?? 1), tr = Z.sim.trial(sp, vars), out = []; let guard = 0; const n = Math.max(1, Math.round(sp.n || 1000)); while (out.length < n && guard++ < 50 * n) { const t = tr(r); if (t.keep) out.push(+t.value); } const vals = sp.running === 'none' ? out : Z.sim.running(out, sp.running || 'mean');
      if (+sp.band > 0 && (sp.running || 'mean') === 'mean') { const k = +sp.band, lo = [], hi = []; let sum = 0, sq = 0; out.forEach((v, i) => { sum += v; sq += v * v; const m = sum / (i + 1), sd = i > 0 ? Math.sqrt(Math.max(0, (sq - (i + 1) * m * m) / i)) : NaN, half = k * sd / Math.sqrt(i + 1); lo.push(i > 0 ? m - half : NaN); hi.push(i > 0 ? m + half : NaN); }); vals.band = { lo, hi }; }
      return vals; } catch (e) { console.warn('series sim:', e.message); return []; } };
    const list0 = (params.series || []).map((s, i) => { const id = s.id || 's' + i; if (!s.sim) return { ...s, id, slot: s.colour || i + 1 }; const v = simValues(s.sim, { ...(params.params || {}) }); return { ...s, id, slot: s.colour || i + 1, values: v, band: v.band || s.band || null }; });
    const n = Math.max(1, ...list0.map((s) => (s.values || s.ohlc || []).length));
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
      for (const s of list0) { for (const v of valuesOf(s)) { if (Number.isFinite(v)) { lo = Math.min(lo, v); hi = Math.max(hi, v); } } for (const c of s.ohlc || []) { lo = Math.min(lo, c[2]); hi = Math.max(hi, c[1]); } }
      if (params.yScale === 'log') { // positive values only, padded by a ratio
        let plo = Infinity; for (const s of list0) for (const v of valuesOf(s)) if (Number.isFinite(v) && v > 0) plo = Math.min(plo, v);
        return Number.isFinite(plo) ? [plo / 1.08, hi * 1.08] : [1, 10];
      }
      if (params.baseline != null) { lo = Math.min(lo, params.baseline); hi = Math.max(hi, params.baseline); }
      for (const h of params.hlines || []) if (h && Number.isFinite(+h.y) && h.axis !== 2) { lo = Math.min(lo, +h.y); hi = Math.max(hi, +h.y); } // item 212
      if (!Number.isFinite(lo)) return [0, 1];
      const pad = (hi - lo || 1) * 0.08; const t = C.niceTicks(lo - pad, hi + pad, 5); const st = t[1] - t[0] || 1;
      return [Math.floor((lo - pad) / st) * st, Math.ceil((hi + pad) / st) * st];
    })();
    const labelW = Math.max(0, ...list0.filter((s) => s.label).map((s) => K.tw(s.label) + 22));
    const logY = params.yScale === 'log';
    /* item 186: a second y axis on the right; series with axis: 2 use it (params.y2 range, y2Label, y2Format "pct" | "money") */
    const right = list0.filter((s) => s.axis === 2);
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
    const hasCandles = list0.some((s) => s.ohlc && (params.candles || s.candles)), padI = hasCandles ? 0.7 : 0;
    /* item 310: xScale "log" spaces the index (from indexFrom, default 1) on a log axis, for long simulations; xStep fixes
       the tick spacing (100 ticks every hundred) */
    const logX = params.xScale === 'log' && !dates, ix0 = params.indexFrom ?? (logX ? 1 : 0);
    const lsx = logX ? K.logScale([Math.max(1e-9, ix0), Math.max(ix0 + 1, ix0 + n - 1)], [ml, W - mr]) : null;
    /* items 431, 456: xValues [x0, x1, ...] gives each index its real x (lambda = 0.01, 0.1, 1, 10; n = 100, 200, 400),
       on a linear axis or, with xScale "log", a log one; markers and shades still take indices */
    const XV = Array.isArray(params.xValues) && params.xValues.length >= 2 && !dates ? params.xValues.map(Number) : null;
    const xAt = (i) => { if (!XV) return i; const k = Math.max(0, Math.min(XV.length - 2, Math.floor(i))), f = i - k; return XV[k] + (XV[k + 1] - XV[k]) * f; };
    const iAt = (x) => { for (let k = 0; k + 1 < XV.length; k++) { const a = XV[k], b = XV[k + 1]; if ((x - a) * (x - b) <= 0) return k + (b === a ? 0 : (x - a) / (b - a)); } return x < XV[0] === XV[0] < XV[XV.length - 1] ? 0 : XV.length - 1; };
    const xvLog = XV && params.xScale === 'log' && XV.every((v) => v > 0);
    const xvBase = XV ? (xvLog ? K.logScale([Math.min(...XV), Math.max(...XV)], [ml, W - mr]) : C.scale([Math.min(...XV), Math.max(...XV)], [ml, W - mr])) : null;
    const sx = XV ? Object.assign((i) => xvBase(xAt(i)), { invert: (p) => iAt(xvBase.invert(p)), range: [ml, W - mr], domain: [0, n - 1] })
      : logX ? Object.assign((i) => lsx(i + ix0), { invert: (p) => lsx.invert(p) - ix0, range: [ml, W - mr], domain: [0, n - 1] }) : C.scale([-padI, n - 1 + padI], [ml, W - mr]), sy = logY ? K.logScale(yRange, [H - mb, mt]) : C.scale(yRange, [H - mb, mt]); // yScale: "log", for log-price charts
    const sy2 = y2Range ? C.scale(y2Range, [H - mb, mt]) : null, syOf = (s2) => (s2.axis === 2 && sy2 ? sy2 : sy);
    /* item 168: dateFormat for date ticks: %Y %y %m %d %e %b %B (for example "%b %Y", "%d/%m", "%Y-%m") */
    const MONTHS_L = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const strf = (d, f) => f.replace(/%([YymdebB%])/g, (_, c) => ({ Y: String(d.getUTCFullYear()), y: String(d.getUTCFullYear()).slice(2), m: String(d.getUTCMonth() + 1).padStart(2, '0'), d: String(d.getUTCDate()).padStart(2, '0'), e: String(d.getUTCDate()), b: MONTHS[d.getUTCMonth()], B: MONTHS_L[d.getUTCMonth()], '%': '%' })[c]);
    const fmtX = dates
      ? (i) => { const d = dates[Math.round(i)]; if (!d) return ''; if (params.dateFormat) return strf(d, String(params.dateFormat)); const span = (dates[dates.length - 1] - dates[0]) / 864e5; return span > 300 ? MONTHS[d.getUTCMonth()] + ' ' + String(d.getUTCFullYear()).slice(2) : d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()]; }
      : XV ? (i) => K.fmt(xAt(i), 3) : (i) => K.fmt(i + ix0, 2);
    const idxOf = (v) => { if (typeof v === 'number') return v; if (dates && typeof v === 'string') { const t = new Date(v + (v.length <= 10 ? 'T00:00:00Z' : '')).getTime(); let best = 0; dates.forEach((d, i) => { if (Math.abs(d - t) < Math.abs(dates[best] - t)) best = i; }); return best; } return 0; };
    /* Maximum drawdown: the largest fall from a running peak, as a share of the peak (abs: true measures the fall itself,
       for cumulative P&L that starts at zero) */
    const drawdown = (vals, abs = false) => { let peak = -1, best = { dd: 0, fall: 0, from: 0, to: 0 }; vals.forEach((v, i) => { if (!Number.isFinite(v)) return; if (peak < 0 || v > vals[peak]) peak = i; const fall = vals[peak] - v, dd = abs ? fall : vals[peak] ? fall / vals[peak] : 0; if (dd > best.dd) best = { dd, fall, from: peak, to: i }; }); return best; };

    const def = {
      kind: 'series', aria: params.aria || 'Time series chart',
      modes: ['slider', 'tap'],
      size: () => ({ w: W, h: H }),
      listKeys: ['markers', 'hlines', 'vlines'],
      init: () => ({ markers: [], hlines: [], shade: [], window: null, reveal: 1, highlight: [], drawdown: false }),
      prepare(patch) { if (Array.isArray(patch.window)) patch.window = { from: patch.window[0], to: patch.window[1] }; return patch; },
      render(view, R) {
        const g = R.F.g, x0 = ml, x1 = W - mr, y0 = H - mb, y1 = mt;
        /* item 361, 367: state.series { id: { values, label, ... } } overrides a series (a derive can write values that follow a
           slider, such as ar1(phi, 60, 7)); give params.y so the axis holds still */
        const list = list0.map((s0) => (K.isObj(view.series) && K.isObj(view.series[s0.id]) ? { ...s0, ...view.series[s0.id] } : s0));
        let xt = K.ticksFor(0, n - 1, x1 - x0, { minGap: 56, fmtF: (v) => fmtX(v) });
        /* inbox (fin-ml 2, arma 1): a date format showing only the year puts ticks on the first date of each year (only
           the month: of each month), so a tick under Dec 2016 no longer reads 2016 */
        if (dates && params.dateFormat && /%[Yy]/.test(params.dateFormat) && !/%[mdeb B]/.test(params.dateFormat.replace(/%[Yy]/g, ''))) {
          const firsts = []; dates.forEach((d, i) => { if (i === 0 ? d.getUTCMonth() === 0 && d.getUTCDate() <= 7 : d.getUTCFullYear() !== dates[i - 1].getUTCFullYear()) firsts.push(i); });
          const every = Math.max(1, Math.ceil(firsts.length / Math.max(2, Math.floor((x1 - x0) / 46)))); xt = { ticks: firsts.filter((_, k) => k % every === 0), step: 1 };
        } else if (dates && params.dateFormat && /%[bBm]/.test(params.dateFormat) && !/%[de]/.test(params.dateFormat)) {
          const firsts = []; dates.forEach((d, i) => { if (i > 0 && d.getUTCMonth() !== dates[i - 1].getUTCMonth()) firsts.push(i); });
          if (firsts.length) { const every = Math.max(1, Math.ceil(firsts.length / Math.max(2, Math.floor((x1 - x0) / 56)))); xt = { ticks: firsts.filter((_, k) => k % every === 0), step: 1 }; }
        }
        if (logX) { const lt = K.logTicks(Math.max(1e-9, ix0), ix0 + n - 1, x1 - x0, { minGap: 40 }); xt = { ticks: lt.ticks.map((v) => v - ix0), step: 1 }; }
        else if (params.xStep && !dates) { const st = +params.xStep, t = []; for (let v = Math.ceil(ix0 / st) * st; v <= ix0 + n - 1 + 1e-9; v += st) t.push(Math.round(v - ix0)); xt = { ticks: t, step: 1 }; }
        if (XV) { const lo = Math.min(...XV), hi = Math.max(...XV), t = xvLog ? K.logTicks(lo, hi, x1 - x0, { minGap: 44 }) : params.xStep ? { ticks: (() => { const a = []; for (let v = Math.ceil(lo / +params.xStep) * +params.xStep; v <= hi + 1e-9; v += +params.xStep) a.push(+v.toFixed(10)); return a; })() } : K.ticksFor(lo, hi, x1 - x0, { minGap: 46 }); xt = { ticks: t.ticks.filter((v) => v >= lo - 1e-9 && v <= hi + 1e-9).map(iAt), step: 1 }; }
        else xt.ticks = xt.ticks.filter((v) => Number.isInteger(v) && v >= 0 && v <= n - 1);
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
        /* item 212: horizontal reference lines (params.hlines fixed, state.hlines patchable): { id, y, label, dashed
           (default true), colour, axis: 2 }, for a limit such as pi^2/6 across a partial-sum chart */
        [].concat(params.hlines || [], view.hlines || []).forEach((h, i) => {
          if (!h || !Number.isFinite(+h.y)) return;
          const syH = h.axis === 2 && sy2 ? sy2 : sy, yy = syH(+h.y); if (yy < y1 - 0.5 || yy > y0 + 0.5) return;
          const o = K.obj(h.id || 'hline' + i, '', h.colour || 'muted');
          o.append(svg('line', { x1: x0, x2: x1, y1: yy, y2: yy, class: 'cvb-ln thin' + (h.dashed === false ? '' : ' cvb-dash') }));
          /* inbox (fin-ml 1): reference lines are tap targets ("tap the barrier hit first") */
          if (R.mode === 'tap') { o.append(svg('line', { x1: x0, x2: x1, y1: yy, y2: yy, class: 'cvb-tapbox cv-body', style: 'stroke: transparent; stroke-width: 18px' })); R.tappable(o, h.id || 'hline' + i, h.label ? String(h.label).replace(/\$/g, '') : 'Reference line'); }
          back.append(o);
          if (h.label) {
            /* the label sits above or below the line at the right end, or at the left, wherever no series line passes */
            const lt = String(h.label), lw = Math.max(24, K.tw(lt.replace(/\$/g, '')) + 8);
            const pts = []; list.forEach((s2) => { if ((view.hide || []).includes(s2.id)) return; const sv = syOf(s2); valuesOf(s2).forEach((v, i) => { if (Number.isFinite(v)) pts.push([sx(i), sv(v)]); }); });
            const yAt = (x) => { const ys = []; list.forEach((s2) => { if ((view.hide || []).includes(s2.id)) return; const vals = valuesOf(s2), sv = syOf(s2), u = sx.invert(x); if (u == null) return; const i = Math.floor(u), f = u - i; if (Number.isFinite(vals[i]) && Number.isFinite(vals[i + 1])) ys.push(sv(vals[i] + (vals[i + 1] - vals[i]) * f)); else if (Number.isFinite(vals[Math.round(u)])) ys.push(sv(vals[Math.round(u)])); }); return ys; };
            const clear = (bx) => { for (let x = bx.x0; x <= bx.x1; x += 4) if (yAt(x).some((y) => y > bx.y0 - 3 && y < bx.y1 + 3)) return false; return !pts.some(([px, py]) => px > bx.x0 && px < bx.x1 && py > bx.y0 - 3 && py < bx.y1 + 3); };
            const cands = [[x1 - 4, -11, 'end'], [x1 - 4, 11, 'end'], [x0 + 4, -11, 'start'], [x0 + 4, 11, 'start']].filter(([, dy]) => yy + dy > y1 + 8 && yy + dy < y0 - 8);
            const box = ([x, dy, an]) => K.boxOf({ x, y: yy + dy, w: lw, h: 18, anchor: an });
            const pick = cands.find((q) => clear(box(q))) || cands[0] || [x1 - 4, yy - y1 > 22 ? -11 : 11, 'end'];
            over.append(K.lab(pick[0], yy + pick[1], lt, { anchor: pick[2], halo: true, cls: 'cvb-strong', size: 12 })); fixed.push(box(pick));
          }
        });
        /* inbox (fin-ml 1): vlines [{ id, i, label, colour, dashed }] (params or state, patchable): a vertical reference at an
           index or date, such as a time limit a slider on h moves (bind "vlines.v1.i") */
        [].concat(params.vlines || [], view.vlines || []).forEach((v, k) => {
          if (!v || v.i == null) return; const xx = sx(idxOf(v.i)); if (!(xx >= x0 - 0.5 && xx <= x1 + 0.5)) return;
          const o = K.obj(v.id || 'vline' + k, '', v.colour || 'muted');
          o.append(K.washPath(`M${xx},${y0}L${xx},${y1}`), svg('line', { x1: xx, x2: xx, y1: y0, y2: y1, class: 'cvb-ln thin' + (v.dashed === false ? '' : ' cvb-dash') }));
          if (R.mode === 'tap') { o.append(svg('line', { x1: xx, x2: xx, y1: y0, y2: y1, class: 'cvb-tapbox cv-body', style: 'stroke: transparent; stroke-width: 18px' })); R.tappable(o, v.id || 'vline' + k, v.label ? String(v.label).replace(/\$/g, '') : 'Vertical line'); }
          back.append(o);
          if (v.label) { const t = String(v.label), lx = K.clamp(xx + 4, x0, x1 - K.tw(t) - 2); over.append(K.lab(lx, y1 + 10, t, { anchor: 'start', halo: true, cls: 'cvb-strong', size: 12 })); fixed.push(K.boxOf({ x: lx, y: y1 + 10, text: t.replace(/\$/g, ''), anchor: 'start' })); }
        });
        if (view.window && view.window.from != null) {
          const a = sx(idxOf(view.window.from)), b = sx(idxOf(view.window.to ?? n - 1)), o = K.obj('window', '', 'manip');
          o.append(K.washRect(a, y1, b - a, y0 - y1, 0), svg('rect', { x: a, y: y1, width: Math.max(1, b - a), height: y0 - y1, class: 'cvb-window' + (R.mode === 'tap' ? ' cv-body' : '') }));
          if (R.mode === 'tap') R.tappable(o, 'window', view.window.label || 'Window');
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
            /* item 373: step: true draws a step line (flat, then a jump at the next point), for balances that jump */
            for (let i = 0; i <= Math.min(upto, vals.length - 1); i++) { const v = vals[i]; if (!Number.isFinite(v)) { pen = false; continue; } d += pen ? (s.step ? 'H' + sx(i).toFixed(2) + 'V' + syS(v).toFixed(2) : 'L' + sx(i).toFixed(2) + ',' + syS(v).toFixed(2)) : 'M' + sx(i).toFixed(2) + ',' + syS(v).toFixed(2); if (!pen) pts.push([]); if (s.step && pen) pts[pts.length - 1].push([sx(i), pts[pts.length - 1][pts[pts.length - 1].length - 1][1]]); pts[pts.length - 1].push([sx(i), syS(v)]); pen = true; }
            if (last > upto && upto + 1 < vals.length && Number.isFinite(vals[upto]) && Number.isFinite(vals[upto + 1])) { const f = last - upto, v = vals[upto] + (vals[upto + 1] - vals[upto]) * f; d += 'L' + sx(last).toFixed(2) + ',' + syS(v).toFixed(2); if (pts.length) pts[pts.length - 1].push([sx(last), syS(v)]); }
            /* item 171: fill "below" shades between the line and zero (or the baseline), as fill_between does */
            if (s.fill && pts.length) {
              const base = s.fillTo ?? params.baseline ?? 0, by = K.clamp(syS(K.clamp(base, Math.min(...(s.axis === 2 ? y2Range : yRange)), Math.max(...(s.axis === 2 ? y2Range : yRange)))), y1, y0);
              pts.filter((run) => run.length > 1).forEach((run) => o.append(svg('path', { d: `M${run[0][0].toFixed(2)},${by.toFixed(2)}` + run.map((q) => `L${q[0].toFixed(2)},${q[1].toFixed(2)}`).join('') + `L${run[run.length - 1][0].toFixed(2)},${by.toFixed(2)}Z`, class: 'cvb-fill' })));
            }
            /* item 443: a band { lo: [...], hi: [...] } (from a sim with band: k, or given) shaded behind the line */
            if (s.band && Array.isArray(s.band.lo) && Array.isArray(s.band.hi)) { const up = [], dn = []; for (let i = 0; i <= Math.min(upto, vals.length - 1); i++) { const a = s.band.lo[i], b = s.band.hi[i]; if (Number.isFinite(a) && Number.isFinite(b)) { up.push([sx(i), syS(b)]); dn.push([sx(i), syS(a)]); } } if (up.length > 1) plot.append(svg('path', { d: 'M' + up.concat(dn.reverse()).map((q) => q[0].toFixed(2) + ',' + K.clamp(q[1], y1 - 200, y0 + 200).toFixed(2)).join('L') + 'Z', class: 'cvb-band ' + K.colourCls(s.slot) })); }
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
          fixed.push(K.boxOf({ x: e.x + 9, y: e.y, text: String(e.text).replace(/\$/g, ''), anchor: 'start' }), { x0: e.x - 5, x1: e.x + 5, y0: e.ly - 5, y1: e.ly + 5 }); // item 449: marker labels keep clear of the end labels
        }
        /* markers */
        const labels = [];
        for (const m of view.markers || []) {
          const s = list.find((q) => q.id === m.series) || list[0]; if (!s) continue;
          const i = m.i === 'reveal' || m.at === 'reveal' ? Math.round(last) : idxOf(m.i ?? m.at), v = m.y ?? valuesOf(s)[Math.round(i)]; if (!Number.isFinite(v) || i > last + 1e-9) continue;
          const o = K.obj(m.id, '', m.colour || 'ink'), cx = sx(i), cy = syOf(s)(v);
          o.append(K.washCircle(cx, cy, 11), svg('circle', { cx, cy, r: 5, class: 'cvb-dot' }));
          R.tappable(o, m.id, m.label);
          over.append(o);
          /* item 385: labelSize (px, also params.markerLabelSize) and labelOffset [dx, dy] fit many labelled markers */
          const msz = m.labelSize ?? params.markerLabelSize, mo = Array.isArray(m.labelOffset) ? m.labelOffset : [0, 0];
          if (m.label) labels.push({ x: cx + (+mo[0] || 0), y: cy + (m.below ? 16 : -15) * (msz ? msz / 13 : 1) + (+mo[1] || 0), text: String(m.label).replace('{value}', fmtVal(v, m.decimals)), anchor: 'middle', size: msz, h: msz ? msz + 3 : undefined, w: msz ? K.tw(String(m.label).replace('{value}', fmtVal(v, m.decimals)), msz) : undefined }); // item 181: per-marker decimals
        }
        K.placeLabels(labels, fixed, { x0, x1: W - 4, y0: y1, y1: y0 });
        for (const l of labels) over.append(K.lab(l.x, l.y, l.text, { anchor: l.anchor, halo: true, cls: 'cvb-strong', size: l.size }));
      },
      methods: (R) => ({
        /* item 302: controls bind reveal (0 to 1), revealAt (an index: the series drawn up to that point) and a marker's
           index as "markers.<id>.i"; a marker with i: "reveal" rides the end of the reveal */
        setParam: (name, v) => { const nm = String(name); if (nm === 'reveal') R.inst.set({ reveal: K.clamp(+v, 0, 1) }, { instant: true }); else if (nm === 'revealAt') R.inst.set({ reveal: K.clamp((+v - (params.indexFrom || 0)) / Math.max(1, n - 1), 0, 1) }, { instant: true }); else R.inst.set(Z.canvas.paramPatch(nm, v), { instant: true }); },
        getParam: (name) => { const nm = String(name); if (nm === 'reveal') return R.state.reveal ?? 1; if (nm === 'revealAt') return Math.round((R.state.reveal ?? 1) * (n - 1)) + (params.indexFrom || 0); let o = R.state; for (const k of nm.split('.')) o = o == null ? undefined : Array.isArray(o) ? o.find((it) => it && it.id === k) : o[k]; return typeof o === 'number' ? o : (R.state.params || {})[nm]; },
        margins: () => ({ left: ml, right: mr }),
        maxDrawdown: (id, abs) => { const s = list0.find((q) => q.id === id) || list0[0]; return s ? drawdown(valuesOf(s), !!abs) : null; },
      }),
    };
    return K.make(host, params, ctx, def);
  });
})();
