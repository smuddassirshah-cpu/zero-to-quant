/* orderbook: price ladder with bid sizes (left, green side) and ask sizes (right, red side), the spread, and a
   market order walking the book level by level.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js).
   Pass 7 (items 352, 353, 370, 376, 421): the levels live in state (seeded from params): a list replaces a side, a map
   keyed by price sets a size ({ "100.5": 300 }), adds a level, or removes one (null); a map keyed by index patches a
   level ({ "0": { "1": 350 } }, which a control bound to "bids.0.1" writes). A level may carry a third entry, a label
   (an order id "#17", "You"). state.quotes { bid: [p, s], ask: [p, s] } shows the learner's own quotes in the book,
   state.fair a fair value in the spread row; decimals (average fill), midDecimals and spreadUnit "pence" | "bp". */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  C.register('orderbook', (host, params, ctx) => {
    const K = Z.cvb;
    const W = 540, rowH = 30;
    const norm = (list) => (Array.isArray(list) ? list : []).map((l) => (Array.isArray(l) ? l.slice() : l && typeof l === 'object' ? [+l.price, +l.size, l.label ?? l.id] : null)).filter((l) => l && Number.isFinite(+l[0]) && Number.isFinite(+l[1])).map((l) => [+l[0], +l[1], ...(l[2] != null ? [String(l[2])] : [])]);
    const bids0 = norm(params.bids), asks0 = norm(params.asks);
    const decOf = (v) => { const s = String(v); return s.includes('.') ? s.split('.')[1].length : 0; };
    const dp = params.dp ?? Math.max(0, ...[...bids0, ...asks0].map((l) => decOf(l[0])));
    const top = 30;
    const priceW = 96, sideW = (W - priceW) / 2 - 8, cx = W / 2;
    const fmtP = (p, d = dp) => (params.currency || '') + (+p).toFixed(d);
    const fmtS = (s) => K.fmt(s, 2);
    /* the book as drawn from a state: each side sorted best first and cut at depth, the learner's quotes merged in */
    const bookOf = (view) => {
      const q = view.quotes || {};
      const withQ = (list, side) => { const out = list.map((l) => l.slice()); const mine = q[side]; if (Array.isArray(mine) && Number.isFinite(+mine[0]) && +mine[1] > 0) out.push([+mine[0], +mine[1], mine[2] != null ? String(mine[2]) : (params.youLabel || 'You'), 'you']); return out; };
      const bids = withQ(norm(view.bids ?? bids0), 'bid').sort((a, b) => b[0] - a[0]), asks = withQ(norm(view.asks ?? asks0), 'ask').sort((a, b) => a[0] - b[0]);
      const depth = params.depth || Math.max(bids0.length, asks0.length, 1);
      const B = bids.slice(0, depth), A = asks.slice(0, depth);
      return { B, A, rows: params.depth ? params.depth : Math.max(bids0.length, asks0.length, 1), maxSize: params.maxSize || Math.max(1, ...B.map((l) => l[1]), ...A.map((l) => l[1]), ...bids0.map((l) => l[1]), ...asks0.map((l) => l[1])) };
    };
    /* the frame is sized for depth rows a side (params.depth, else the opening book), so levels can come and go */
    const nRows = params.depth || Math.max(bids0.length, asks0.length, 1);
    const H = top + (2 * nRows + 1) * rowH + 44;
    let B = bids0, A = asks0;

    /* Walk the book: fills per level for a market order. */
    const walk = (order) => {
      if (!order || !order.size) return { fills: [], filled: 0, left: 0, cost: 0 };
      const book = order.side === 'sell' ? B : A, pre = order.side === 'sell' ? 'bid' : 'ask';
      let left = order.size, cost = 0; const fills = [];
      for (let i = 0; i < book.length && left > 0; i++) { const q = Math.min(left, book[i][1]); fills.push({ id: pre + i, price: book[i][0], qty: q }); left -= q; cost += q * book[i][0]; }
      return { fills, filled: order.size - left, left, cost, side: order.side };
    };
    const rowY = (id) => { const m = id.match(/^(bid|ask)(\d+)$/); if (!m) return null; const i = +m[2]; return m[1] === 'ask' ? top + (nRows - 1 - i) * rowH : top + (nRows + 1 + i) * rowH; };
    /* a side patch: a list replaces; keys that are level indices with an object or array value patch that level; other
       keys are prices: a number sets that level's size (adding the level), [size, label] sets both, null removes it */
    const patchSide = (cur, pt) => {
      if (Array.isArray(pt)) return norm(pt);
      if (!pt || typeof pt !== 'object') return cur;
      let out = cur.map((l) => l.slice());
      for (const [k, v] of Object.entries(pt)) {
        if (/^\d+$/.test(k) && +k < out.length && v && typeof v === 'object') { const l = out[+k]; Object.entries(v).forEach(([j, x]) => { if (/^[0-2]$/.test(j)) l[+j] = j === '2' ? String(x) : +x; }); continue; }
        const price = +k; if (!Number.isFinite(price)) continue;
        const i = out.findIndex((l) => Math.abs(l[0] - price) < 1e-9);
        if (v === null || v === 0) { if (i >= 0) out.splice(i, 1); continue; }
        const [size, label] = Array.isArray(v) ? v : [v, undefined];
        if (i >= 0) { out[i][1] = +size; if (label !== undefined) out[i][2] = String(label); } else out.push([price, +size, ...(label != null ? [String(label)] : [])]);
      }
      return out;
    };

    const def = {
      kind: 'orderbook', aria: params.aria || 'Order book',
      modes: ['tap'],
      size: () => ({ w: W, h: H }),
      init: () => ({ order: null, highlight: [], fills: true, selected: [], bids: bids0.map((l) => l.slice()), asks: asks0.map((l) => l.slice()) }),
      prepare(patch, state) { for (const k of ['bids', 'asks']) if (k in patch) patch[k] = patchSide(norm(state[k] ?? (k === 'bids' ? bids0 : asks0)), patch[k]); return patch; },
      skip: ['bids', 'asks', 'quotes'],
      animate(prev, next, a, R) {
        const changed = JSON.stringify(prev.order) !== JSON.stringify(next.order);
        if (a.instant || !changed || !next.order) { a.show(next); return; }
        const w = walk(next.order), levels = Math.max(1, w.fills.length);
        return C.tween(0, levels, Math.min(1800, 420 * levels + 200), (t) => { if (a.alive()) a.show(t >= levels ? next : { ...next, _p: t }); }, 'linear');
      },
      render(view, R) {
        const bk = bookOf(view); B = bk.B; A = bk.A; const maxSize = bk.maxSize;
        const g = R.F.g, w = walk(view.order), p = view._p ?? Infinity, sel = new Set(view.selected || []);
        const consumed = {}; let curId = null, takenSoFar = 0;
        const whole = [...B, ...A].every((l) => Number.isInteger(l[1])) && Number.isInteger(+(view.order && view.order.size) || 0);
        w.fills.forEach((f, k) => { const frac = K.clamp(p - k, 0, 1); consumed[f.id] = whole ? Math.round(f.qty * frac) : f.qty * frac; takenSoFar += f.qty * frac; if (frac > 0 && frac < 1) curId = f.id; });
        g.append(K.txt(cx - priceW / 2 - 8, 12, params.bidLabel || 'Bid size', { anchor: 'end', size: 12, cls: 'cvb-tick' }), K.txt(cx, 12, 'Price', { size: 12, cls: 'cvb-tick' }), K.txt(cx + priceW / 2 + 8, 12, params.askLabel || 'Ask size', { anchor: 'start', size: 12, cls: 'cvb-tick' }));
        const row = (side, i, lvl) => {
          const id = side + i, y = rowY(id), best = i === 0, mine = lvl[3] === 'you', o = K.obj(id, 'cvb-level' + (sel.has(id) ? ' is-on' : '') + (mine ? ' is-mine' : ''), mine ? 'manip' : side === 'bid' ? 'cvb-cbid' : 'cvb-cask');
          o.append(K.washRect(4, y + 1, W - 8, rowH - 2, 4));
          if (R.mode === 'tap') o.append(svg('rect', { x: 4, y: y + 1, width: W - 8, height: rowH - 2, rx: 4, class: 'cvb-selw' }));
          if (curId === id) o.append(svg('rect', { x: 4, y: y + 1, width: W - 8, height: rowH - 2, rx: 4, class: 'cvb-cell-w', style: 'fill: var(--manip-wash)' }));
          const size = lvl[1], taken = consumed[id] || 0, rest = size - taken, bw = (s) => (s / maxSize) * (sideW - 46);
          if (side === 'bid') {
            const xr = cx - priceW / 2 - 6;
            o.append(svg('rect', { x: xr - bw(rest), y: y + 5, width: bw(rest), height: rowH - 10, rx: 3, class: 'cvb-size' + (best ? ' best' : '') }));
            if (taken) o.append(svg('rect', { x: xr - bw(size), y: y + 5, width: bw(taken), height: rowH - 10, rx: 3, class: 'cvb-size filled' }));
            o.append(K.txt(xr - bw(size) - 6, y + rowH / 2, fmtS(rest), { anchor: 'end', size: 13, weight: best ? 700 : 500, cls: 'cvb-outink' }));
            if (lvl[2] != null && !(taken && view.fills !== false)) o.append(K.txt(cx + priceW / 2 + 8, y + rowH / 2, String(lvl[2]), { anchor: 'start', size: 12, weight: 600, cls: 'cvb-muted cvb-olabel' }));
          } else {
            const xl = cx + priceW / 2 + 6;
            o.append(svg('rect', { x: xl + bw(taken), y: y + 5, width: bw(rest), height: rowH - 10, rx: 3, class: 'cvb-size' + (best ? ' best' : '') }));
            if (taken) o.append(svg('rect', { x: xl, y: y + 5, width: bw(taken), height: rowH - 10, rx: 3, class: 'cvb-size filled' }));
            o.append(K.txt(xl + bw(size) + 6, y + rowH / 2, fmtS(rest), { anchor: 'start', size: 13, weight: best ? 700 : 500, cls: 'cvb-outink' }));
            if (lvl[2] != null && !(taken && view.fills !== false)) o.append(K.txt(cx - priceW / 2 - 8, y + rowH / 2, String(lvl[2]), { anchor: 'end', size: 12, weight: 600, cls: 'cvb-muted cvb-olabel' }));
          }
          o.append(svg('rect', { x: cx - priceW / 2 + 4, y: y + 2, width: priceW - 8, height: rowH - 4, rx: 4, class: 'cvb-tapbox cvb-pricebox cv-body' }));
          o.append(K.txt(cx, y + rowH / 2, fmtP(lvl[0]), { size: 14, weight: best ? 700 : 500, cls: 'cvb-price' + (best ? ' cvb-c' : '') }));
          if (taken && view.fills !== false) {
            const t = (w.side === 'sell' ? 'sold ' : 'bought ') + fmtS(Math.round(taken * 1000) / 1000);
            o.append(side === 'ask' ? K.txt(cx - priceW / 2 - 8, y + rowH / 2, t, { anchor: 'end', size: 12, cls: 'cvb-strong cvb-outink' }) : K.txt(cx + priceW / 2 + 8, y + rowH / 2, t, { anchor: 'start', size: 12, cls: 'cvb-strong cvb-outink' }));
          }
          R.tappable(o, id, `${side === 'bid' ? 'Bid' : 'Ask'} ${fmtS(size)} at ${fmtP(lvl[0])}`);
          g.append(o);
          g.append(svg('line', { x1: 4, x2: W - 4, y1: y + rowH, y2: y + rowH, class: 'cvb-rowline' }));
        };
        A.forEach((l, i) => row('ask', i, l));
        /* spread row */
        const sy = top + nRows * rowH, so = K.obj('spread', '', 'ink');
        so.append(svg('rect', { x: 4, y: sy + 2, width: W - 8, height: rowH - 4, rx: 4, class: 'cvb-spreadrow' }), K.washRect(4, sy + 1, W - 8, rowH - 2, 4));
        /* item 124: spreadValue: false keeps the label but hides the computed number (the learner works it out) */
        /* spreadUnit "pence" (x100, "p") or "bp" (of the mid); midDecimals (default the price places plus one when the mid
           falls between ticks); fair (state or params) adds the fair value */
        const spr = A.length && B.length ? A[0][0] - B[0][0] : null, mid = spr != null ? (A[0][0] + B[0][0]) / 2 : null;
        const sprT = spr == null ? '' : params.spreadUnit === 'pence' ? K.fmt(spr * 100, 2) + 'p' : params.spreadUnit === 'bp' ? K.fmt(spr / mid * 1e4, 1) + ' bp' : K.fmt(spr, dp + 2);
        const midDp = params.midDecimals ?? (mid != null && Math.abs(+mid.toFixed(dp) - mid) > 1e-9 ? dp + 1 : dp);
        const fair = view.fair ?? params.fair;
        const sprLine = (params.spreadLabel || 'Spread') + (params.spreadValue === false ? '' : ' ' + sprT) + (params.showMid && params.spreadValue !== false && mid != null ? '   mid ' + fmtP(mid, midDp) : '') + (Number.isFinite(+fair) && fair !== null ? '   fair ' + fmtP(+fair, params.fairDecimals ?? midDp) : '');
        if (A.length && B.length) so.append(K.txt(cx, sy + rowH / 2, sprLine, { size: 13, weight: 600, cls: 'cvb-muted' }));
        g.append(so);
        B.forEach((l, i) => row('bid', i, l));
        /* order summary */
        if (view.order && view.order.size) {
          const yb = top + (2 * nRows + 1) * rowH + 22, done = p >= w.fills.length;
          const left = view.order.size - takenSoFar;
          const t = done
            ? `${view.order.side === 'sell' ? 'Sold' : 'Bought'} ${fmtS(w.filled)} at average ${fmtP(w.filled ? w.cost / w.filled : 0, params.decimals ?? dp)}` + (w.left > 0 ? `, ${fmtS(w.left)} unfilled` : '')
            : `Market ${view.order.side === 'sell' ? 'sell' : 'buy'} ${fmtS(view.order.size)}: remaining ${fmtS(Math.round(left))}`;
          const o = K.obj('order', '', 'manip'); o.append(K.txt(cx, yb, t, { size: 14, weight: 600 })); g.append(o);
        }
      },
      methods: (R) => ({
        /* Fills for a market order: { fills: [{ id, price, qty }], filled, left, cost } */
        walk: (order) => { const bk = bookOf(R.state); B = bk.B; A = bk.A; return walk(order); },
        spread: () => { const bk = bookOf(R.state); return bk.A.length && bk.B.length ? bk.A[0][0] - bk.B[0][0] : null; },
        /* controls: "bids.0.1" (a level's size), "fair", "quotes.bid.0" and any other dotted state path or free param */
        setParam: (name, v) => R.inst.set(Z.canvas.paramPatch(String(name), v), { instant: true }),
        getParam: (name) => { let o = R.state; for (const k of String(name).split('.')) o = o == null ? undefined : o[k]; return typeof o === 'number' ? o : (R.state.params || {})[String(name)]; },
      }),
    };
    return K.make(host, params, ctx, def);
  });
})();
