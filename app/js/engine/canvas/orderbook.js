/* orderbook: price ladder with bid sizes (left, green side) and ask sizes (right, red side), the spread, and a
   market order walking the book level by level.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js). */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  C.register('orderbook', (host, params, ctx) => {
    const K = Z.cvb;
    const W = 540, rowH = 30;
    const bids = (params.bids || []).slice().sort((a, b) => b[0] - a[0]);
    const asks = (params.asks || []).slice().sort((a, b) => a[0] - b[0]);
    const depth = params.depth || Math.max(bids.length, asks.length, 1);
    const B = bids.slice(0, depth), A = asks.slice(0, depth);
    const dp = params.dp ?? Math.max(0, ...[...B, ...A].map((l) => { const s = String(l[0]); return s.includes('.') ? s.split('.')[1].length : 0; }));
    const top = 30, H = top + (A.length + B.length + 1) * rowH + 44;
    const maxSize = Math.max(1, ...B.map((l) => l[1]), ...A.map((l) => l[1]));
    const priceW = 96, sideW = (W - priceW) / 2 - 8, cx = W / 2;
    const fmtP = (p) => (params.currency || '') + (+p).toFixed(dp);
    const fmtS = (s) => K.fmt(s, 2);

    /* Walk the book: fills per level for a market order. */
    const walk = (order) => {
      if (!order || !order.size) return { fills: [], filled: 0, left: 0, cost: 0 };
      const book = order.side === 'sell' ? B : A, pre = order.side === 'sell' ? 'bid' : 'ask';
      let left = order.size, cost = 0; const fills = [];
      for (let i = 0; i < book.length && left > 0; i++) { const q = Math.min(left, book[i][1]); fills.push({ id: pre + i, price: book[i][0], qty: q }); left -= q; cost += q * book[i][0]; }
      return { fills, filled: order.size - left, left, cost, side: order.side };
    };
    const rowY = (id) => { const m = id.match(/^(bid|ask)(\d+)$/); if (!m) return null; const i = +m[2]; return m[1] === 'ask' ? top + (A.length - 1 - i) * rowH : top + (A.length + 1 + i) * rowH; };

    const def = {
      kind: 'orderbook', aria: params.aria || 'Order book',
      modes: ['tap'],
      size: () => ({ w: W, h: H }),
      init: () => ({ order: null, highlight: [], fills: true, selected: [] }),
      animate(prev, next, a, R) {
        const changed = JSON.stringify(prev.order) !== JSON.stringify(next.order);
        if (a.instant || !changed || !next.order) { a.show(next); return; }
        const w = walk(next.order), levels = Math.max(1, w.fills.length);
        return C.tween(0, levels, Math.min(1800, 420 * levels + 200), (t) => { if (a.alive()) a.show(t >= levels ? next : { ...next, _p: t }); }, 'linear');
      },
      render(view, R) {
        const g = R.F.g, w = walk(view.order), p = view._p ?? Infinity, sel = new Set(view.selected || []);
        const consumed = {}; let curId = null, takenSoFar = 0;
        const whole = [...B, ...A].every((l) => Number.isInteger(l[1])) && Number.isInteger(+(view.order && view.order.size) || 0);
        w.fills.forEach((f, k) => { const frac = K.clamp(p - k, 0, 1); consumed[f.id] = whole ? Math.round(f.qty * frac) : f.qty * frac; takenSoFar += f.qty * frac; if (frac > 0 && frac < 1) curId = f.id; });
        g.append(K.txt(cx - priceW / 2 - 8, 12, params.bidLabel || 'Bid size', { anchor: 'end', size: 12, cls: 'cvb-tick' }), K.txt(cx, 12, 'Price', { size: 12, cls: 'cvb-tick' }), K.txt(cx + priceW / 2 + 8, 12, params.askLabel || 'Ask size', { anchor: 'start', size: 12, cls: 'cvb-tick' }));
        const row = (side, i, lvl) => {
          const id = side + i, y = rowY(id), best = i === 0, o = K.obj(id, 'cvb-level' + (sel.has(id) ? ' is-on' : ''), side === 'bid' ? 'cvb-cbid' : 'cvb-cask');
          o.append(K.washRect(4, y + 1, W - 8, rowH - 2, 4));
          if (R.mode === 'tap') o.append(svg('rect', { x: 4, y: y + 1, width: W - 8, height: rowH - 2, rx: 4, class: 'cvb-selw' }));
          if (curId === id) o.append(svg('rect', { x: 4, y: y + 1, width: W - 8, height: rowH - 2, rx: 4, class: 'cvb-cell-w', style: 'fill: var(--manip-wash)' }));
          const size = lvl[1], taken = consumed[id] || 0, rest = size - taken, bw = (s) => (s / maxSize) * (sideW - 46);
          if (side === 'bid') {
            const xr = cx - priceW / 2 - 6;
            o.append(svg('rect', { x: xr - bw(rest), y: y + 5, width: bw(rest), height: rowH - 10, rx: 3, class: 'cvb-size' + (best ? ' best' : '') }));
            if (taken) o.append(svg('rect', { x: xr - bw(size), y: y + 5, width: bw(taken), height: rowH - 10, rx: 3, class: 'cvb-size filled' }));
            o.append(K.txt(xr - bw(size) - 6, y + rowH / 2, fmtS(rest), { anchor: 'end', size: 13, weight: best ? 700 : 500, cls: 'cvb-outink' }));
          } else {
            const xl = cx + priceW / 2 + 6;
            o.append(svg('rect', { x: xl + bw(taken), y: y + 5, width: bw(rest), height: rowH - 10, rx: 3, class: 'cvb-size' + (best ? ' best' : '') }));
            if (taken) o.append(svg('rect', { x: xl, y: y + 5, width: bw(taken), height: rowH - 10, rx: 3, class: 'cvb-size filled' }));
            o.append(K.txt(xl + bw(size) + 6, y + rowH / 2, fmtS(rest), { anchor: 'start', size: 13, weight: best ? 700 : 500, cls: 'cvb-outink' }));
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
        const sy = top + A.length * rowH, so = K.obj('spread', '', 'ink');
        so.append(svg('rect', { x: 4, y: sy + 2, width: W - 8, height: rowH - 4, rx: 4, class: 'cvb-spreadrow' }), K.washRect(4, sy + 1, W - 8, rowH - 2, 4));
        if (A.length && B.length) so.append(K.txt(cx, sy + rowH / 2, (params.spreadLabel || 'Spread') + ' ' + K.fmt(A[0][0] - B[0][0], dp + 2) + (params.showMid ? '   mid ' + fmtP((A[0][0] + B[0][0]) / 2) : ''), { size: 13, weight: 600, cls: 'cvb-muted' }));
        g.append(so);
        B.forEach((l, i) => row('bid', i, l));
        /* order summary */
        if (view.order && view.order.size) {
          const yb = top + (A.length + B.length + 1) * rowH + 22, done = p >= w.fills.length;
          const left = view.order.size - takenSoFar;
          const t = done
            ? `${view.order.side === 'sell' ? 'Sold' : 'Bought'} ${fmtS(w.filled)} at average ${fmtP(w.filled ? w.cost / w.filled : 0)}` + (w.left > 0 ? `, ${fmtS(w.left)} unfilled` : '')
            : `Market ${view.order.side === 'sell' ? 'sell' : 'buy'} ${fmtS(view.order.size)}: remaining ${fmtS(Math.round(left))}`;
          const o = K.obj('order', '', 'manip'); o.append(K.txt(cx, yb, t, { size: 14, weight: 600 })); g.append(o);
        }
      },
      methods: () => ({
        /* Fills for a market order: { fills: [{ id, price, qty }], filled, left, cost } */
        walk: (order) => walk(order),
        spread: () => (A.length && B.length ? A[0][0] - B[0][0] : null),
      }),
    };
    return K.make(host, params, ctx, def);
  });
})();
