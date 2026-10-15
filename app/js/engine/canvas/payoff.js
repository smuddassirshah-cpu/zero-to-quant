/* payoff: option payoff or P&L at expiry against the underlying; legs, combined line, strikes, breakevens, spot.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js). */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  C.register('payoff', (host, params, ctx) => {
    const K = Z.cvb;
    const W = 540, H = params.height || 320;
    const range = params.range || [80, 120];
    const baseLegs = (params.legs || []).map((l, i) => ({ ...l, id: l.id || 'leg' + i, slot: l.colour || i + 2 }));

    const legsOf = (view) => baseLegs.map((l) => ({ ...l, strike: view.strike && view.strike[l.id] != null ? +view.strike[l.id] : +(l.strike ?? l.price ?? 0), premium: view.premium && view.premium[l.id] != null ? +view.premium[l.id] : +(l.premium || 0) }));
    const legValue = (l, S, pl) => {
      const sign = l.side === 'short' ? -1 : 1, q = l.qty ?? 1;
      if (l.type === 'stock') return sign * q * (S - l.strike);
      const pay = l.type === 'put' ? Math.max(l.strike - S, 0) : Math.max(S - l.strike, 0);
      return sign * q * (pay - (pl ? l.premium : 0));
    };
    const total = (legs, S, pl) => legs.reduce((s, l) => s + legValue(l, S, pl), 0);
    /* Piecewise linear: breakpoints at strikes, so roots are exact per segment. */
    const breakevens = (legs, pl) => {
      const xs = [range[0], ...legs.filter((l) => l.type !== 'stock').map((l) => l.strike).filter((k) => k > range[0] && k < range[1]), range[1]].sort((a, b) => a - b);
      const out = [];
      for (let i = 0; i < xs.length - 1; i++) {
        const a = xs[i], b = xs[i + 1], fa = total(legs, a, pl), fb = total(legs, b, pl);
        if (Math.abs(fa) < 1e-12) { if (!out.some((v) => Math.abs(v - a) < 1e-9)) out.push(a); continue; }
        if (fa * fb < 0) out.push(a + (b - a) * fa / (fa - fb));
      }
      if (Math.abs(total(legs, range[1], pl)) < 1e-12 && !out.some((v) => Math.abs(v - range[1]) < 1e-9)) out.push(range[1]);
      return out.filter((v) => { const e = 1e-6 * (range[1] - range[0]); return !(Math.abs(total(legs, v - e, pl)) < 1e-9 && Math.abs(total(legs, v + e, pl)) < 1e-9); });
    };
    const yRangeFor = (view) => {
      if (params.y) return params.y;
      const pl = view.pl ?? params.pl ?? true, legs = legsOf(view);
      let lo = 0, hi = 0;
      const xs = [range[0], range[1], ...legs.map((l) => l.strike)];
      for (const x of xs) { if (x < range[0] || x > range[1]) continue; const t = total(legs, x, pl); lo = Math.min(lo, t); hi = Math.max(hi, t); if (legs.length > 1) for (const l of legs) { const v = legValue(l, x, pl); lo = Math.min(lo, v); hi = Math.max(hi, v); } }
      const pad = (hi - lo || 2) * 0.12; const t = C.niceTicks(lo - pad, hi + pad, 5), st = t[1] - t[0] || 1;
      return [Math.floor((lo - pad) / st) * st, Math.ceil((hi + pad) / st) * st];
    };
    let yFixed = null;

    const def = {
      kind: 'payoff', aria: params.aria || 'Option payoff diagram',
      modes: ['drag', 'slider', 'tap'],
      size: () => ({ w: W, h: H }),
      init: () => ({ strike: Object.fromEntries(baseLegs.map((l) => [l.id, +(l.strike ?? l.price ?? 0)])), premium: Object.fromEntries(baseLegs.map((l) => [l.id, +(l.premium || 0)])), spot: null, highlight: [], pl: params.pl ?? true }),
      prepare(patch) { if (patch.params) { if (patch.params.spot != null) patch.spot = patch.params.spot; for (const l of baseLegs) if (patch.params[l.id] != null) patch.strike = { ...(patch.strike || {}), [l.id]: patch.params[l.id] }; } return patch; },
      render(view, R) {
        const g = R.F.g, pl = view.pl ?? params.pl ?? true, legs = legsOf(view);
        if (!yFixed || view._rescale) yFixed = yRangeFor(view);
        const yr = params.y || (() => { const now = yRangeFor(view); return [Math.min(now[0], yFixed[0]), Math.max(now[1], yFixed[1])]; })();
        const ml = K.yMargin(yr[0], yr[1], H - 60), mt = 26, mb = 46, mr = 16;
        const sx = C.scale(range, [ml, W - mr]), sy = C.scale(yr, [H - mb, mt]);
        const x0 = ml, x1 = W - mr, y0 = H - mb, y1 = mt;
        K.chartAxes(g, sx, sy, { yLabel: params.yLabel ?? (pl ? 'Profit and loss' : 'Payoff'), xLabel: params.xLabel ?? 'Underlying price at expiry' });
        const zero = sy(0);
        if (zero > y1 && zero < y0) g.append(svg('line', { x1: x0, x2: x1, y1: zero, y2: zero, class: 'cvb-zero' }));
        const plot = svg('g', { 'clip-path': R.clipRect(x0, y1 - 3, x1 - x0, y0 - y1 + 6) }), over = svg('g');
        g.append(plot, over);
        const pts = (f) => { const xs = [range[0], ...legs.map((l) => l.strike).filter((k) => k > range[0] && k < range[1]), range[1]].sort((a, b) => a - b); return 'M' + xs.map((x) => sx(x).toFixed(2) + ',' + sy(f(x)).toFixed(2)).join('L'); };
        const showLegs = view.showLegs ?? (legs.length > 1);
        const labels = [], fixed = [];
        if (showLegs) legs.forEach((l) => {
          const o = K.obj(l.id, '', l.slot), d = pts((S) => legValue(l, S, pl));
          o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln faint cvb-dash' }));
          plot.append(o);
          if (l.label) { const lx = range[0] + (range[1] - range[0]) * 0.06; labels.push({ x: sx(lx), y: sy(legValue(l, lx, pl)) - 11, text: l.label, anchor: 'start' }); }
        });
        const comb = K.obj(legs.length > 1 ? 'total' : (legs[0] ? legs[0].id : 'total'), '', params.colour || 1), dC = pts((S) => total(legs, S, pl));
        comb.append(K.washPath(dC), svg('path', { d: dC, class: 'cvb-ln bold' }));
        plot.append(comb);
        if (params.label) { const lx = range[1] - (range[1] - range[0]) * 0.03; labels.push({ x: sx(lx), y: sy(total(legs, lx, pl)) - 14, text: params.label, anchor: 'end' }); }
        /* strike ticks and the kinks they make */
        const seenK = new Set();
        legs.filter((l) => l.type !== 'stock' && l.strike >= range[0] && l.strike <= range[1]).forEach((l) => {
          const dup = seenK.has(l.strike); seenK.add(l.strike);
          const x = sx(l.strike), o = K.obj('strike-' + l.id, '', 'ink');
          o.append(svg('line', { x1: x, x2: x, y1: y0 - 5, y2: y0 + 5, class: 'cvb-ln thin' }));
          const yk = sy(total(legs, l.strike, pl));
          o.append(svg('circle', { cx: x, cy: yk, r: 3.5, class: 'cvb-dot' }));
          over.append(o);
          fixed.push({ x0: x - 6, x1: x + 6, y0: yk - 6, y1: yk + 6 });
          if (view.kinkLabels !== false && !dup) labels.push({ x, y: yk + 18, text: (l.strikeLabel || 'K') + ' = ' + K.fmt(l.strike, 2), anchor: 'middle' });
        });
        /* breakevens on the zero line */
        if ((view.breakeven ?? pl) && zero > y1 && zero < y0) breakevens(legs, pl).forEach((b) => {
          const o = K.obj('breakeven', '', 'ink'); o.append(K.washCircle(sx(b), zero, 11), svg('circle', { cx: sx(b), cy: zero, r: 5, class: 'cvb-be' }));
          over.append(o); fixed.push({ x0: sx(b) - 7, x1: sx(b) + 7, y0: zero - 7, y1: zero + 7 }); labels.push({ x: sx(b), y: zero - 16, text: K.fmt(b, 2), anchor: 'middle' });
        });
        /* spot */
        if (view.spot != null && view.spot >= range[0] && view.spot <= range[1]) {
          const x = sx(view.spot), v = total(legs, view.spot, pl), o = K.obj('spot', '', 'manip');
          o.append(K.washPath(`M${x},${y0}L${x},${y1}`), svg('line', { x1: x, x2: x, y1: y0, y2: y1 + 14, class: 'cvb-ln thin cvb-dash' }), svg('circle', { cx: x, cy: sy(v), r: 5, class: 'cvb-dot' }));
          over.append(o);
          const t = (params.spotLabel || 'S') + ' = ' + K.fmt(view.spot, 2) + (view.spotValue === false ? '' : ', ' + (pl ? 'P&L ' : 'payoff ') + K.fmt(v, 2));
          const lx = K.clamp(x, x0 + K.tw(t) / 2 + 2, x1 - K.tw(t) / 2 - 2);
          over.append(K.txt(lx, y1 + 6, t, { halo: true, cls: 'cvb-strong' })); fixed.push(K.boxOf({ x: lx, y: y1 + 6, text: t }));
        }
        K.placeLabels(labels, fixed, { x0, x1, y0: y1, y1: y0 });
        for (const l of labels) over.append(K.lab(l.x, l.y, l.text, { anchor: l.anchor, halo: true, cls: 'cvb-strong', size: 12 }));
        /* strike handles on the axis */
        if (R.active('drag')) legs.filter((l) => l.type !== 'stock' && (!params.drag || [].concat(params.drag).includes(l.id))).forEach((l) => over.append(K.handle(sx(l.strike), y0, l.id, { r: 7, shape: 'diamond', label: `Strike of ${l.label || l.id}` })));
        R._sx = sx;
      },
      drag: {
        start: (id, p, R) => (R.active('drag') && baseLegs.some((l) => l.id === id) ? { id } : null),
        move(info, p, R, end) { setStrike(R, info.id, R._sx.invert(p.x), end); },
        key(id, dx, dy, R) { const l = legsOf(R.state).find((q) => q.id === id); if (l) setStrike(R, id, l.strike + (dx || dy) * (params.snap || 1), true); },
      },
      methods: (R) => ({
        value: (S) => { const st = R.state; return total(legsOf(st), S, st.pl ?? params.pl ?? true); },
        breakevens: () => breakevens(legsOf(R.state), R.state.pl ?? params.pl ?? true),
        points: () => Object.fromEntries(legsOf(R.state).filter((l) => l.type !== 'stock').map((l) => [l.id, { x: l.strike, y: 0 }])),
        place: (id, pos, opts = {}) => R.inst.set({ strike: { [id]: Array.isArray(pos) ? pos[0] : pos } }, opts),
      }),
    };
    const setStrike = (R, id, v, end) => {
      v = K.round(K.clamp(K.snapTo(v, params.snap ?? 1), range[0], range[1]), 6);
      R.commit({ strike: { [id]: v } });
      R.emit({ type: 'drag', id, strike: v, x: v, y: 0, phase: end ? 'end' : 'move' });
    };
    return K.make(host, params, ctx, def);
  });
})();
