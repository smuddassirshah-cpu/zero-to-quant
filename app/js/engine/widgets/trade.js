/* trade widget (ENGINE-BACKLOG 459, inbox E12): a market-making game over the `orderbook` canvas.
   Each turn the learner sets a bid, an ask and a size; a seeded counterparty hits the bid, lifts the ask or stays out;
   cards (and, if authored, the hidden value) arrive on a schedule; a position limit applies; a ledger shows position,
   cash, mark-to-market and realised P&L; after the last turn the hidden value settles the position. The grade is the
   final P&L against a benchmark (or a band) plus rule breaks (limit, crossed or locked quotes, spread outside bounds).
   Contract: docs/AUTHORING.md section 3 ("trade") and canvas/README-B.md ("trade over orderbook").
   The game itself is a pure module (the `api` below): it runs under Node too, so tools/validate.mjs plays the authored
   `strategy` against the benchmark. Everything is deterministic: the counterparty's three random draws for turn t come
   from the seed and t alone, so the same quotes always meet the same counterparty. */
(function () {
  'use strict';
  const MINUS = '−';
  const r9 = (v) => +(+v).toFixed(9);
  const decOf = (v) => { const s = String(v); return s.includes('.') ? s.split('.')[1].length : 0; };

  /* ---------- Pure game ---------- */
  /* three draws in [0, 1) for turn t (1-based), from the seed alone */
  const draws = (seed, t) => {
    let a = (Math.imul(seed | 0, 0x9E3779B1) ^ Math.imul(t, 0x85EBCA6B)) >>> 0;
    const next = () => { a = (a + 0x6D2B79F5) >>> 0; let x = a; x = Math.imul(x ^ (x >>> 15), x | 1); x ^= x + Math.imul(x ^ (x >>> 7), x | 61); return ((x ^ (x >>> 14)) >>> 0) / 4294967296; };
    next();
    return [next(), next(), next()];
  };
  const norm = (spec) => {
    const tick = +spec.tick > 0 ? +spec.tick : 0.5;
    const fair = +spec.fair;
    const size = Object.assign({ min: 1, max: 5, start: 1, step: 1 }, spec.size || {});
    const sp = spec.spread || {};
    const range = Array.isArray(spec.range) ? [+spec.range[0], +spec.range[1]] : [r9(fair - 20 * tick), r9(fair + 20 * tick)];
    const q0 = Object.assign({ bid: r9(fair - 2 * tick), ask: r9(fair + 2 * tick), size: size.start }, spec.quote || {});
    return {
      tick, fair, turns: spec.turns | 0, value: +spec.value, seed: spec.seed | 0, size, range, quote: q0,
      limit: Number.isFinite(+spec.limit) && +spec.limit > 0 ? +spec.limit : Infinity,
      spreadMin: Number.isFinite(+sp.min) ? +sp.min : null, spreadMax: Number.isFinite(+sp.max) ? +sp.max : null,
      cp: Array.isArray(spec.counterparty) ? spec.counterparty : [spec.counterparty || { type: 'noise' }],
      schedule: Array.isArray(spec.schedule) ? spec.schedule : [],
      maxBreaks: Number.isFinite(+spec.maxBreaks) ? +spec.maxBreaks : 0,
      benchmark: Number.isFinite(+spec.benchmark) ? +spec.benchmark : null,
      band: Array.isArray(spec.band) && spec.band.length === 2 ? [+spec.band[0], +spec.band[1]] : null,
    };
  };
  const snap = (N, v) => Math.min(N.range[1], Math.max(N.range[0], r9(Math.round(v / N.tick) * N.tick)));
  const newGame = (N) => ({ t: 0, pos: 0, cash: 0, avg: 0, realised: 0, mark: N.fair, began: 0, cards: [], log: [], breaks: [], done: false, valueShown: false, pnl: null, settlement: 0 });
  /* cards for the coming turn: the mark moves to a card's `fair`; a card with `reveal: true` shows the hidden value */
  const begin = (N, g) => {
    if (g.done || g.began === g.t + 1) return [];
    g.began = g.t + 1;
    const fresh = N.schedule.filter((c) => (c.turn | 0) === g.t + 1);
    fresh.forEach((c) => {
      if (c.reveal) { g.mark = N.value; g.valueShown = true; } else if (Number.isFinite(+c.fair)) g.mark = +c.fair;
      g.cards.push({ turn: g.t + 1, text: c.text || (c.reveal ? 'The value is revealed.' : ''), reveal: !!c.reveal, mark: g.mark });
    });
    return fresh;
  };
  /* what a quote is, before it is sent: snapped prices, the room either side, and the rule flags */
  const assess = (N, g, q) => {
    const bid = snap(N, +q.bid), ask = snap(N, +q.ask), size = Math.min(N.size.max, Math.max(N.size.min, Math.round(+q.size || N.size.min)));
    const roomBuy = Math.max(0, N.limit - g.pos), roomSell = Math.max(0, N.limit + g.pos), flags = [];
    const crossed = bid >= ask;
    if (crossed) flags.push({ kind: 'crossed', text: bid === ask ? 'Your bid equals your ask, a locked quote.' : 'Your bid is above your ask, an inverted quote.' });
    else {
      const s = r9(ask - bid);
      if (N.spreadMin != null && s < N.spreadMin - 1e-9) flags.push({ kind: 'spread', text: `Spread ${s} is under the minimum ${N.spreadMin}.` });
      if (N.spreadMax != null && s > N.spreadMax + 1e-9) flags.push({ kind: 'spread', text: `Spread ${s} is over the maximum ${N.spreadMax}.` });
    }
    if (size > roomBuy || size > roomSell) {
      const sides = [size > roomBuy ? `bid (room to buy ${roomBuy})` : null, size > roomSell ? `ask (room to sell ${roomSell})` : null].filter(Boolean).join(' and ');
      flags.push({ kind: 'limit', text: `Size ${size} is over the position limit on the ${sides}, so it is cut back.` });
    }
    return { bid, ask, size, crossed, flags, roomBuy, roomSell, bidSize: Math.min(size, roomBuy), askSize: Math.min(size, roomSell) };
  };
  const cpFor = (N, t) => N.cp.find((c) => Array.isArray(c.turns) && t >= c.turns[0] && t <= c.turns[1]) || N.cp.find((c) => !Array.isArray(c.turns)) || N.cp[N.cp.length - 1];
  /* the counterparty's wish: { act: 'hit' | 'lift', size } or null. hit = sells to your bid, lift = buys from your ask */
  const decide = (N, g, a, t) => {
    const cp = cpFor(N, t) || { type: 'noise' }, u = draws(N.seed, t), type = cp.type || 'noise';
    if (type === 'scripted') {
      const it = (cp.trades || [])[t - 1];
      if (!it || !it.act || it.act === 'none') return { who: type, act: null };
      if (Number.isFinite(+it.price) && (it.act === 'hit' ? a.bid < +it.price : a.ask > +it.price)) return { who: type, act: null };
      return { who: type, act: it.act, size: Math.max(1, it.size | 0 || 1) };
    }
    const rate = Number.isFinite(+cp.rate) ? +cp.rate : type === 'informed' ? 1 : 0.6;
    if (u[0] >= rate) return { who: type, act: null };
    if (type === 'informed') {
      const edge = Number.isFinite(+cp.edge) ? +cp.edge : 0;
      const buyGain = N.value - a.ask, sellGain = a.bid - N.value;
      const buy = a.askSize > 0 && buyGain > edge + 1e-9, sell = a.bidSize > 0 && sellGain > edge + 1e-9;
      if (!buy && !sell) return { who: type, act: null };
      const act = buy && (!sell || buyGain >= sellGain) ? 'lift' : 'hit';
      return { who: type, act, size: Math.min(Number.isFinite(+cp.maxSize) ? +cp.maxSize : Infinity, act === 'lift' ? a.askSize : a.bidSize) };
    }
    const act = u[1] < 0.5 ? 'lift' : 'hit', reach = Number.isFinite(+cp.reach) ? +cp.reach : Infinity;
    if (act === 'lift' ? a.ask > g.mark + reach : a.bid < g.mark - reach) return { who: type, act: null };
    return { who: type, act, size: 1 + Math.floor(u[2] * (Number.isFinite(+cp.maxSize) ? +cp.maxSize : N.size.max)) };
  };
  /* ledger: average-cost realised P&L */
  const execute = (g, dq, price) => {
    g.cash = r9(g.cash - dq * price);
    if (g.pos !== 0 && Math.sign(dq) !== Math.sign(g.pos)) {
      const close = Math.min(Math.abs(dq), Math.abs(g.pos));
      g.realised = r9(g.realised + close * (price - g.avg) * Math.sign(g.pos));
      const left = r9(Math.abs(dq) - close);
      g.pos = r9(g.pos + dq);
      if (left > 0) g.avg = price; else if (g.pos === 0) g.avg = 0;
    } else {
      g.avg = g.pos + dq === 0 ? 0 : r9((g.avg * Math.abs(g.pos) + price * Math.abs(dq)) / Math.abs(g.pos + dq));
      g.pos = r9(g.pos + dq);
    }
  };
  const mtm = (g, at = g.mark) => r9(g.cash + g.pos * at);
  /* one turn: returns the record (also pushed on g.log); settles when the last turn is played */
  const turn = (N, g, q) => {
    if (g.done) return null;
    begin(N, g);
    const t = g.t + 1, a = assess(N, g, q);
    const rec = { turn: t, bid: a.bid, ask: a.ask, size: a.size, flags: a.flags, fill: null, who: null, mark: g.mark };
    a.flags.forEach((f) => { if (!g.breaks.some((b) => b.turn === t && b.kind === f.kind)) g.breaks.push({ turn: t, kind: f.kind, text: f.text }); });
    const want = a.crossed ? { who: null, act: null } : decide(N, g, a, t);
    rec.who = want.who;
    if (want.act) {
      const qty = Math.min(want.size, want.act === 'hit' ? a.bidSize : a.askSize);
      if (qty > 0) {
        const price = want.act === 'hit' ? a.bid : a.ask, dq = want.act === 'hit' ? qty : -qty;
        execute(g, dq, price);
        rec.fill = { side: dq > 0 ? 'buy' : 'sell', qty, price, edge: r9(dq > 0 ? (N.value - price) * qty : (price - N.value) * qty) };
      }
    }
    g.t = t; rec.pos = g.pos; rec.cash = g.cash; rec.realised = g.realised;
    if (g.t >= N.turns) {
      g.done = true; g.mark = N.value; g.valueShown = true;
      g.settlement = r9(g.pos * (N.value - g.avg));
      g.realised = r9(g.realised + g.settlement);
      g.pnl = r9(g.cash + g.pos * N.value);
    }
    g.log.push(rec);
    return rec;
  };
  const verdict = (N, g) => {
    const pnl = g.pnl == null ? mtm(g) : g.pnl, over = g.breaks.length - N.maxBreaks;
    let key = null;
    if (over > 0) key = g.breaks[N.maxBreaks].kind;
    else if (N.band) key = pnl < N.band[0] - 1e-9 ? 'low' : pnl > N.band[1] + 1e-9 ? 'high' : null;
    else if (N.benchmark != null) key = pnl < N.benchmark - 1e-9 ? 'low' : null;
    return { ok: key == null, key, pnl, breaks: g.breaks.length };
  };
  /* a whole run of quotes (a list of { bid, ask, size }, one per turn; the last is repeated if the list is short) */
  const play = (spec, quotes) => {
    const N = norm(spec), g = newGame(N);
    for (let i = 0; i < N.turns; i++) turn(N, g, (quotes && (quotes[i] || quotes[quotes.length - 1])) || N.quote);
    return { N, g, verdict: verdict(N, g) };
  };
  const api = { norm, newGame, begin, assess, turn, verdict, play, mtm, draws, snap };

  if (typeof window === 'undefined' || !window.ZQ) { if (typeof module !== 'undefined') module.exports = api; return; }

  /* ---------- Widget ---------- */
  const Z = window.ZQ;
  Z.trade = api;
  let uid = 0;

  Z.widgets.register('trade', (host, spec, ctx) => {
    const N = norm(spec), id = 'wdtr' + (++uid);
    const cur = spec.currency || '', dp = spec.dp ?? decOf(N.tick), pd = dp + decOf(N.size.step);
    const num = (v, d = pd) => { const s = Math.abs(v).toFixed(d); return (v < 0 && +s !== 0 ? MINUS : '') + s; };
    const money = (v, d = pd) => (v < 0 && +Math.abs(v).toFixed(d) !== 0 ? MINUS : '') + cur + Math.abs(v).toFixed(d);
    const signed = (v, d = pd) => (v > 0 && +Math.abs(v).toFixed(d) !== 0 ? '+' : '') + money(v, d);
    const px = (v) => cur + v.toFixed(dp);
    const E = Z.esc;
    let g = newGame(N), locked = false, failed = false;
    const q = { bid: N.quote.bid, ask: N.quote.ask, size: N.quote.size };
    const field = (key, label) => `<div class="wd-trade-f"><label class="t-label" for="${id}-${key}">${label}</label><div class="wd-trade-step">
      <button type="button" class="wd-trade-b" data-k="${key}" data-d="-1" aria-label="Lower ${label.toLowerCase()}">${MINUS}</button>
      <input id="${id}-${key}" class="wd-trade-in tnum" data-k="${key}" type="text" inputmode="decimal" autocomplete="off" spellcheck="false" aria-label="${label}">
      <button type="button" class="wd-trade-b" data-k="${key}" data-d="1" aria-label="Raise ${label.toLowerCase()}">+</button></div></div>`;
    const el = Z.h(`<div class="wd wd-trade">
      <div class="wd-trade-head"><span class="t-label wd-trade-turn" aria-live="polite"></span><span class="t-caption wd-trade-limit">${N.limit < Infinity ? `Position limit ${N.limit} either way` : ''}</span></div>
      <ol class="wd-trade-cards" aria-label="Cards" aria-live="polite" hidden></ol>
      <dl class="wd-trade-ledger" aria-label="Ledger">
        <div class="wd-trade-stat"><dt>Position</dt><dd class="tnum" data-s="pos"></dd></div>
        <div class="wd-trade-stat"><dt>Cash</dt><dd class="tnum" data-s="cash"></dd></div>
        <div class="wd-trade-stat"><dt>Mark-to-market</dt><dd class="tnum" data-s="mtm"></dd></div>
        <div class="wd-trade-stat"><dt>Realised</dt><dd class="tnum" data-s="real"></dd></div>
      </dl>
      <div class="wd-trade-quote" role="group" aria-label="Your quote">${field('bid', 'Bid')}${field('ask', 'Ask')}${field('size', 'Size')}</div>
      <p class="t-caption wd-trade-warn" role="status" aria-live="polite"></p>
      <div class="wd-trade-actions"><button type="button" class="btn wd-trade-send">Send quote</button><span class="t-caption wd-trade-hint">Enter sends. Up and down arrows change a value.</span></div>
      <ol class="wd-trade-log" aria-label="Turn by turn" aria-live="polite"></ol>
      <div class="wd-trade-result" hidden tabindex="-1"></div>
    </div>`);
    host.append(el);
    const $ = (s) => el.querySelector(s), $$ = (s) => [...el.querySelectorAll(s)];
    const inputs = Object.fromEntries($$('.wd-trade-in').map((i) => [i.dataset.k, i]));
    const stepOf = (k) => (k === 'size' ? N.size.step : N.tick);

    const pushCanvas = (extra = {}) => {
      if (!ctx.canvas || !ctx.canvas.set) return;
      const a = assess(N, g, q);
      try { ctx.canvas.set(Object.assign({ quotes: { bid: [a.bid, g.done ? 0 : a.bidSize], ask: [a.ask, g.done ? 0 : a.askSize] }, fair: g.mark }, extra), { instant: true }); } catch (e) { console.error(e); }
    };
    const paintLedger = () => {
      const set = (k, t, cls) => { const n = $(`[data-s="${k}"]`); n.textContent = t; n.classList.toggle('is-neg', cls === 'neg'); n.classList.toggle('is-pos', cls === 'pos'); };
      const m = mtm(g), sg = (v) => (v > 0 ? 'pos' : v < 0 ? 'neg' : '');
      set('pos', (g.pos > 0 ? '+' : '') + num(g.pos, decOf(N.size.step)) + (N.limit < Infinity ? ` of ${N.limit}` : ''), sg(g.pos));
      set('cash', signed(g.cash), sg(g.cash));
      set('mtm', signed(m), sg(m));
      set('real', signed(g.realised), sg(g.realised));
      $('[data-s="mtm"]').parentElement.querySelector('dt').textContent = g.done ? 'Settled P&L' : 'Mark-to-market';
      $('[data-s="mtm"]').title = g.done ? `Settled at ${px(N.value)}` : `Marked at ${px(g.mark)}`;
    };
    const paintCards = () => {
      const ol = $('.wd-trade-cards'); ol.hidden = !g.cards.length;
      ol.innerHTML = g.cards.map((c, i) => `<li class="wd-trade-card${c.reveal ? ' is-reveal' : ''}${i === g.cards.length - 1 ? ' is-new' : ''}"><span class="t-label">Turn ${c.turn}</span> <span class="wd-trade-card-t">${Z.grade && Z.grade.inline ? Z.grade.inline(c.text) : E(c.text)}</span></li>`).join('');
      Z.mathify && Z.mathify(ol);
    };
    const paintInputs = () => {
      inputs.bid.value = num(q.bid, dp); inputs.ask.value = num(q.ask, dp); inputs.size.value = num(q.size, decOf(N.size.step));
    };
    const paintWarn = () => {
      const w = $('.wd-trade-warn');
      if (g.done) { w.textContent = ''; return; }
      const a = assess(N, g, q);
      w.textContent = a.flags.length ? a.flags.map((f) => f.text).join(' ') + ' Sending it counts as a rule break.' : '';
      w.hidden = !a.flags.length;
    };
    const paint = () => {
      const head = $('.wd-trade-turn');
      head.textContent = g.done ? `All ${N.turns} turns played` : `Turn ${g.t + 1} of ${N.turns}`;
      paintLedger(); paintCards(); paintInputs(); paintWarn();
      $('.wd-trade-send').disabled = locked || g.done;
      $$('.wd-trade-in, .wd-trade-b').forEach((n) => { n.disabled = locked || g.done; });
      $('.wd-trade-quote').hidden = g.done;
      $('.wd-trade-actions').hidden = g.done;
      paintLog(); paintResult();
      $('.wd-trade-log').hidden = g.done;
    };
    const turnLine = (r) => {
      const quoted = `${px(r.bid)} / ${px(r.ask)} for ${r.size}`;
      const pre = `Turn ${r.turn}: you quoted ${quoted}. `;
      if (r.flags.some((f) => f.kind === 'crossed')) return pre + 'The quote was crossed, so it was rejected and nobody traded.';
      const rule = r.flags.length ? ' Rule break: ' + r.flags.map((f) => f.text).join(' ') : '';
      if (!r.fill) return pre + 'Nobody traded.' + rule;
      const f = r.fill;
      return pre + (f.side === 'buy' ? `Your bid was hit: you bought ${f.qty} at ${px(f.price)}.` : `Your ask was lifted: you sold ${f.qty} at ${px(f.price)}.`) + ` Position ${(r.pos > 0 ? '+' : '') + num(r.pos, decOf(N.size.step))}.` + rule;
    };
    const paintLog = () => {
      $('.wd-trade-log').innerHTML = g.log.slice().reverse().map((r) => `<li class="wd-trade-li${r.fill ? ' is-trade' : ''}${r.flags.length ? ' is-break' : ''}">${E(turnLine(r))}</li>`).join('');
    };
    const paintResult = () => {
      const box = $('.wd-trade-result');
      box.hidden = !g.done;
      if (!g.done) { box.innerHTML = ''; return; }
      const v = verdict(N, g), pnlOk = N.band ? g.pnl >= N.band[0] - 1e-9 && g.pnl <= N.band[1] + 1e-9 : N.benchmark == null || g.pnl >= N.benchmark - 1e-9, target = N.band ? `between ${signed(N.band[0])} and ${signed(N.band[1])}` : N.benchmark != null ? `at least ${signed(N.benchmark)}` : '';
      const rows = g.log.map((r) => {
        const f = r.fill;
        return `<tr><th scope="row">${r.turn}</th><td>${px(r.bid)} / ${px(r.ask)} &times; ${r.size}</td><td>${f ? `${f.side === 'buy' ? 'Bought' : 'Sold'} ${f.qty} at ${px(f.price)}<br><span class="wd-trade-who">${E(r.who)}</span>` : r.flags.some((x) => x.kind === 'crossed') ? 'Rejected' : 'No trade'}</td><td class="tnum wd-trade-edge${f && f.edge < 0 ? ' is-neg' : ''}">${f ? signed(f.edge) : ''}</td></tr>`;
      }).join('');
      box.innerHTML = `<h3 class="t-h3 wd-trade-h">Results</h3>
        <p class="wd-trade-final"><span class="t-stat tnum wd-trade-pnl">${signed(g.pnl)}</span> final P&amp;L. The value was ${px(N.value)}${g.pos ? `; your ${g.pos > 0 ? 'long' : 'short'} of ${num(Math.abs(g.pos), decOf(N.size.step))} settled at that price` : '; you finished flat'}.</p>
        <ul class="wd-trade-facts">${target ? `<li>Target: ${E(target)}. ${pnlOk ? 'Met.' : 'Not met.'}</li>` : ''}
        <li>Rule breaks: ${v.breaks}${N.maxBreaks ? ` (up to ${N.maxBreaks} allowed)` : ''}${g.breaks.length ? ': ' + g.breaks.map((b) => `turn ${b.turn} ${b.kind}`).join(', ') : ''}.</li></ul>
        <div class="wd-trade-tbl" role="region" aria-label="Turn by turn results" tabindex="0"><table><thead><tr><th scope="col">Turn</th><th scope="col">Quote</th><th scope="col">Trade</th><th scope="col">Edge</th></tr></thead><tbody>${rows}</tbody></table></div>
        <p class="t-caption">Edge is what each trade was worth against the final value. A negative edge is a trade made against someone who knew more.</p>`;
    };

    const change = () => ctx.change && ctx.change({ t: g.t });
    const send = () => {
      if (locked || g.done) return null;
      const r = turn(N, g, q);
      if (!g.done) begin(N, g);
      paint();
      pushCanvas();
      change();
      return r;
    };
    const restart = () => {
      g = newGame(N); failed = false; begin(N, g);
      Object.assign(q, { bid: N.quote.bid, ask: N.quote.ask, size: N.quote.size });
      paint(); pushCanvas();
    };
    begin(N, g); paint();
    if (ctx.canvas) pushCanvas({});

    /* controls */
    const nudge = (k, d) => { const s = stepOf(k); q[k] = k === 'size' ? Math.min(N.size.max, Math.max(N.size.min, r9(q[k] + d * s))) : snap(N, q[k] + d * s); paintInputs(); paintWarn(); pushCanvas(); change(); };
    el.addEventListener('click', (e) => {
      const b = e.target.closest('.wd-trade-b'); if (b && !b.disabled) { nudge(b.dataset.k, +b.dataset.d); return; }
      if (e.target.closest('.wd-trade-send')) send();
    });
    Object.entries(inputs).forEach(([k, inp]) => {
      inp.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowUp' || e.key === 'ArrowDown') { e.preventDefault(); nudge(k, e.key === 'ArrowUp' ? 1 : -1); }
        else if (e.key === 'Enter') { e.preventDefault(); e.stopPropagation(); const v = Z.widgets.parseNum(inp.value); if (Number.isFinite(v)) q[k] = k === 'size' ? Math.min(N.size.max, Math.max(N.size.min, Math.round(v))) : snap(N, v); send(); }
      });
      inp.addEventListener('change', () => { const v = Z.widgets.parseNum(inp.value); if (Number.isFinite(v)) q[k] = k === 'size' ? Math.min(N.size.max, Math.max(N.size.min, Math.round(v))) : snap(N, v); paintInputs(); paintWarn(); pushCanvas(); change(); });
    });

    const playAll = (quotes) => { restart(); locked = false; quotes.forEach((x) => { if (!g.done) { Object.assign(q, x); turn(N, g, q); if (!g.done) begin(N, g); } }); paint(); pushCanvas(); change(); };
    const strategy = () => (Array.isArray(spec.strategy) ? spec.strategy.map((x) => ({ bid: +x.bid, ask: +x.ask, size: +x.size || N.size.min })) : null);
    const resultLine = () => { const v = verdict(N, g); return v.ok ? null : v.key === 'low' ? `Final P&L ${signed(g.pnl)}, below the target.` : v.key === 'high' ? `Final P&L ${signed(g.pnl)}, above the band: check the run.` : `A rule was broken: ${g.breaks[0].text}`; };

    return {
      el,
      value: () => ({ quotes: g.log.map((r) => ({ bid: r.bid, ask: r.ask, size: r.size })), pnl: g.pnl, position: g.pos, cash: g.cash, breaks: g.breaks.length, done: g.done }),
      /* what a screen's {{carry.name.pnl}} reads (item 460) */
      carryValue: () => ({ pnl: g.pnl == null ? mtm(g) : g.pnl, position: g.pos, cash: g.cash, realised: g.realised, mtm: mtm(g), breaks: g.breaks.length, turns: g.t, value: N.value }),
      answer: strategy,
      set(v) { const list = Array.isArray(v) ? v : v && Array.isArray(v.quotes) ? v.quotes : null; if (list && list.length) playAll(list); },
      ready: () => g.done,
      dirty: () => g.t > 0,
      grade() {
        if (!g.done) return { ok: false, key: null, detail: { turns: g.t } };
        const v = verdict(N, g);
        return { ok: v.ok, key: v.key, line: resultLine(), detail: { pnl: g.pnl, breaks: g.breaks.map((b) => b.kind), position: g.pos } };
      },
      lock() { locked = true; paint(); },
      unlock() { locked = false; if (failed) restart(); else paint(); },
      markGraded(res) {
        const box = $('.wd-trade-result');
        box.classList.toggle('is-ok', !!res.ok); box.classList.toggle('is-bad', !res.ok);
        if (!res.ok && !res.final) failed = true;
        if (g.done) box.focus({ preventScroll: true });
      },
      reveal() { const s = strategy(); if (s) playAll(s); locked = true; paint(); el.classList.add('is-reveal'); },
      reset() { locked = false; el.classList.remove('is-reveal'); restart(); change(); },
      focus() { inputs.bid.focus({ preventScroll: true }); },
      destroy() { el.remove(); },
    };
  });
})();
