/* dice-sim: a seeded dice experiment. Roll n dice, keep a roll when a rule holds, Run 10 / 100 / 1,000 more rolls.
   Shows the dice of the latest roll (kept or filtered out), the counters Rolled / Kept / Filtered out, a share bar
   (kept share of rolls) and a running-share trace over the rolls, converging on an optional exact share.
   Contract: docs/AUTHORING.md section 4; details in canvas/README.md. Builds on ZQ.cvb (canvas/plane.js).
   ENGINE-BACKLOG 1217. */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  /* pips on a 3 x 3 grid, as the prototype drew them */
  const PIPS = { 1: [[2, 2]], 2: [[1, 1], [3, 3]], 3: [[1, 1], [2, 2], [3, 3]], 4: [[1, 1], [3, 1], [1, 3], [3, 3]], 5: [[1, 1], [3, 1], [2, 2], [1, 3], [3, 3]], 6: [[1, 1], [3, 1], [1, 2], [3, 2], [1, 3], [3, 3]] };
  const frac = (v) => { // 0.3056, "11/36" or "11 / 36" -> a number, else null
    if (typeof v === 'number') return Number.isFinite(v) ? v : null;
    const m = String(v == null ? '' : v).trim().match(/^(\d+(?:\.\d+)?)\s*\/\s*(\d+(?:\.\d+)?)$/);
    if (m) return +m[2] ? +m[1] / +m[2] : null;
    return v !== '' && v != null && Number.isFinite(+v) ? +v : null;
  };

  C.register('dice-sim', (host, params, ctx) => {
    const K = Z.cvb;
    const W = 540, H = 346;
    const nDice = Math.max(1, Math.min(6, Math.round(+params.dice || 2)));
    const sides = Math.max(2, Math.min(20, Math.round(+params.sides || 6)));
    const names = Array.from({ length: nDice }, (_, i) => 'd' + (i + 1)).concat(['dice', 'total']);
    /* event: an optional second rule counted among the kept rolls; the share bar and the trace then show the event's share of kept rolls */
    const ev = params.event && typeof params.event === 'object' ? params.event : null;
    const exSrc = ev ? ev.exact : params.exact, exLab = ev ? ev.exactLabel : params.exactLabel;
    const exact = frac(exSrc);
    const exactText = exLab != null ? String(exLab) : typeof exSrc === 'string' && /\//.test(exSrc) ? exSrc.replace(/\s+/g, '') : exact != null ? K.fmt(exact, 3) : '';
    const evLabel = ev ? String(ev.label || 'Event') : '';
    const L = Object.assign({ rolled: 'Rolled', kept: 'Kept', out: 'Filtered out', share: ev ? 'Kept rolls with ' + String(ev.label || 'the event').replace(/^[A-Z](?![A-Z])/, (c) => c.toLowerCase()) : 'Share of rolls kept', last: 'Last roll', run: 'Run', reset: 'Reset', none: 'No rolls yet' }, params.labels || {});
    const trials = (Array.isArray(params.trials) && params.trials.length ? params.trials : [10, 100, 1000]).map((n) => Math.max(1, Math.round(+n)));
    const axMax = Math.min(1, Math.max(0.05, +params.max > 0 ? +params.max : exact != null ? Math.ceil(exact * 15) / 10 : 1));
    const fmtShare = (v) => v.toFixed(3);
    const nf = (n) => Math.round(n).toLocaleString('en-GB');

    /* seeded stream: roll i is the same every time, so 10 then 100 shows the first 110 rolls */
    let rule = null, evRule = null, err = null;
    try { rule = Z.sim.compile(params.keep == null ? 'true' : String(params.keep), names); } catch (e) { err = e; console.warn('dice-sim:', e.message); }
    try { if (ev) evRule = Z.sim.compile(String(ev.rule), names); } catch (e) { err = e; console.warn('dice-sim:', e.message); }
    const rng = Z.sim.rng(params.seed ?? 1);
    const rolls = [], keptTo = [0], evTo = [0], keptEv = [0]; // keptTo[i], evTo[i]: kept rolls and kept rolls with the event among the first i rolls; keptEv[k]: events among the first k kept rolls
    const upTo = (n) => {
      if (err) return;
      while (rolls.length < n) {
        const dice = Array.from({ length: nDice }, () => 1 + Math.floor(rng() * sides));
        const env = { dice, total: dice.reduce((a, b) => a + b, 0) }; dice.forEach((v, i) => { env['d' + (i + 1)] = v; });
        let keep = false; try { keep = !!rule(rng, env); } catch (e) { err = e; console.warn('dice-sim:', e.message); return; }
        let hit = false; if (keep && evRule) { try { hit = !!evRule(rng, env); } catch (e) { err = e; console.warn('dice-sim:', e.message); return; } }
        rolls.push({ dice, keep }); keptTo.push(keptTo[keptTo.length - 1] + (keep ? 1 : 0)); evTo.push(evTo[evTo.length - 1] + (hit ? 1 : 0));
        if (keep) keptEv.push(keptEv[keptEv.length - 1] + (hit ? 1 : 0));
      }
    };

    const chips = []; let liveEl = null;
    const buildControls = (R) => {
      if (R.static) return;
      for (const n of trials) {
        const b = document.createElement('button'); b.type = 'button'; b.className = 'cvb-chip'; b.textContent = L.run + ' ' + n.toLocaleString('en-GB');
        b.addEventListener('click', () => { if (!R.locked) { const ran = Math.round(R.state.ran || 0) + n; R.inst.set({ ran }); R.emit({ type: 'run', ran, added: n }); } });
        chips.push(b); R.extra.append(b);
      }
      const r = document.createElement('button'); r.type = 'button'; r.className = 'cvb-chip quiet'; r.textContent = L.reset;
      r.addEventListener('click', () => { if (!R.locked) { R.inst.set({ ran: 0 }, { instant: true }); R.emit({ type: 'run', ran: 0, added: 0 }); } });
      chips.push(r); R.extra.append(r);
      liveEl = document.createElement('span'); liveEl.className = 'sr-only'; liveEl.setAttribute('aria-live', 'polite'); liveEl.setAttribute('role', 'status'); R.extra.append(liveEl);
    };

    const dieG = (x, y, s, v, kept, blank) => {
      const g = svg('g', { class: 'cvds-die' + (blank ? ' is-blank' : kept ? ' is-kept' : ' is-out') });
      g.append(svg('rect', { x, y, width: s, height: s, rx: s * 0.22 }));
      if (!blank && sides <= 6 && PIPS[v]) PIPS[v].forEach(([px, py]) => g.append(svg('circle', { cx: x + (px * s) / 4, cy: y + (py * s) / 4, r: s * 0.085 })));
      else if (!blank) g.append(K.txt(x + s / 2, y + s / 2, v, { size: s * 0.46, weight: 700, cls: 'cvds-num' }));
      return g;
    };

    const def = {
      kind: 'dice-sim', aria: params.aria || 'Dice experiment',
      size: () => ({ w: W, h: H }),
      init: () => ({ ran: 0, highlight: [] }),
      prepare(patch) { if (patch.reset) { patch.ran = 0; delete patch.reset; } return patch; },
      animate(prev, next, a, R) {
        if (a.instant) { a.show(next); return; }
        const from = Math.round(R.shown.ran || 0), to = Math.round(next.ran || 0);
        if (to <= from) { a.show(next); return; }
        const ms = Math.min(1100, 360 + 250 * Math.log10(Math.max(1, to - from)));
        return C.tween(0, 1, ms, (t) => { if (!a.alive()) return; a.show(t >= 1 ? next : { ...next, ran: Math.round(from + (to - from) * t), _anim: true }); }, 'standard');
      },
      render(view, R) {
        if (!chips.length && !R.static && !liveEl) buildControls(R);
        const g = R.F.g, n = Math.max(0, Math.round(view.ran || 0));
        upTo(n);
        const rolled = err ? 0 : n, kept = keptTo[rolled] || 0, hits = evTo[rolled] || 0, last = rolled ? rolls[rolled - 1] : null;
        const den = ev ? kept : rolled, share = den ? (ev ? hits : kept) / den : null; // the share drawn: kept of rolled, or (with an event) the event among kept

        /* dice and counters */
        const ds = nDice <= 3 ? 46 : nDice <= 4 ? 40 : 34, dgap = 8, dy = 6;
        const dg = K.obj('dice', 'cvds-dice', 'ink');
        for (let i = 0; i < nDice; i++) dg.append(dieG(8 + i * (ds + dgap), dy, ds, last ? last.dice[i] : 0, last && last.keep, !last));
        const tag = !last ? L.none : last.keep ? L.kept : L.out;
        dg.append(K.txt(8, dy + ds + 17, last ? L.last + ': ' + tag : tag, { anchor: 'start', size: 13, weight: last && last.keep ? 700 : 500, cls: 'cvds-tag' + (last && last.keep ? ' is-kept' : '') }));
        g.append(dg);
        const cg = K.obj('counters', 'cvds-counters', 'ink');
        [[L.rolled, rolled, ''], [L.kept, kept, 'is-kept'], [ev ? evLabel : L.out, ev ? hits : rolled - kept, '']].reverse().forEach(([lab, v, cls], i) => {
          const cx = W - 8 - i * 84;
          cg.append(K.txt(cx, 16, lab, { anchor: 'end', size: 13, cls: 'cvb-tick' }), K.txt(cx, 40, nf(v), { anchor: 'end', size: 22, weight: 700, cls: 'cvds-val tnum ' + cls }));
        });
        g.append(cg);

        /* share bar */
        const sg = K.obj('share', 'cvds-share', 'ink'), bx0 = 8, bx1 = W - 8, by = 132, bh = 20, bx = (v) => bx0 + (bx1 - bx0) * Math.min(v, axMax) / axMax;
        sg.append(K.txt(bx0, 102, L.share, { anchor: 'start', size: 13, weight: 600, cls: 'cvds-lab' }), K.txt(bx1, 102, share == null ? (rolled ? 'None kept yet' : L.none) : fmtShare(share), { anchor: 'end', size: 16, weight: 700, cls: 'cvds-val' }));
        sg.append(svg('rect', { x: bx0, y: by, width: bx1 - bx0, height: bh, rx: 6, class: 'cvds-track' }));
        if (share) sg.append(svg('rect', { x: bx0, y: by, width: Math.max(0, bx(share) - bx0), height: bh, rx: 6, class: 'cvds-fill' }));
        if (exact != null) {
          sg.append(svg('line', { x1: bx(exact), x2: bx(exact), y1: by - 6, y2: by + bh + 6, class: 'cvds-exact' }));
          const lx = bx(exact), anchor = lx > W - 60 ? 'end' : 'middle';
          sg.append(K.txt(lx, by - 14, exactText, { anchor, size: 13, weight: 600, cls: 'cvds-lab', halo: true }));
        }
        sg.append(K.txt(bx0, by + bh + 16, '0', { anchor: 'start', size: 13, cls: 'cvb-tick' }), K.txt(bx1, by + bh + 16, K.fmt(axMax, 2), { anchor: 'end', size: 13, cls: 'cvb-tick' }));
        g.append(sg);

        /* running-share trace */
        const tg = K.obj('trace', 'cvds-trace', 'ink'), px0 = 44, px1 = W - 12, py0 = 208, py1 = H - 34;
        const ty = (v) => py1 - (py1 - py0) * Math.min(v, axMax) / axMax, tx = (i) => px0 + (px1 - px0) * (den ? i / den : 0);
        [0, axMax / 2, axMax].forEach((v) => tg.append(svg('line', { x1: px0, x2: px1, y1: ty(v), y2: ty(v), class: 'cvds-grid' }), K.txt(px0 - 6, ty(v), K.fmt(v, 3), { anchor: 'end', size: 13, cls: 'cvb-tick' })));
        tg.append(svg('line', { x1: px0, x2: px0, y1: py0, y2: py1, class: 'cvds-axis' }));
        if (exact != null) {
          tg.append(svg('line', { x1: px0, x2: px1, y1: ty(exact), y2: ty(exact), class: 'cvds-exact' }));
          tg.append(K.txt(px1, ty(exact) - 10, exactText, { anchor: 'end', size: 13, weight: 600, cls: 'cvds-lab', halo: true }));
        }
        if (den) {
          const step = Math.max(1, Math.ceil(den / 300)), at = (i) => (ev ? keptEv[i] : keptTo[i]) / i; let d = '';
          for (let i = 1; i <= den; i += step) d += (d ? 'L' : 'M') + tx(i).toFixed(1) + ' ' + ty(at(i)).toFixed(1);
          if ((den - 1) % step) d += 'L' + tx(den).toFixed(1) + ' ' + ty(share).toFixed(1);
          tg.append(svg('path', { d, class: 'cvds-line' }), svg('circle', { cx: tx(den), cy: ty(share), r: 3.5, class: 'cvds-dot' }));
        }
        tg.append(K.txt(px0, py1 + 16, '0', { anchor: 'middle', size: 13, cls: 'cvb-tick' }), K.txt(px1, py1 + 16, den ? nf(den) + (ev ? ' kept' : ' rolls') : (ev ? 'Kept rolls' : 'Rolls'), { anchor: 'end', size: 13, cls: 'cvb-tick' }));
        tg.append(K.txt(px0, py0 - 12, ev ? 'Running share as kept rolls pile up' : 'Running share kept', { anchor: 'start', size: 13, cls: 'cvb-tick' }));
        g.append(tg);

        R.F.svg.setAttribute('aria-label', (params.aria || 'Dice experiment') + (rolled ? `: ${nf(rolled)} rolled, ${nf(kept)} kept${ev ? ', ' + nf(hits) + ' ' + evLabel : ''}${share == null ? '' : ', share ' + fmtShare(share)}` : ': no rolls yet'));
        if (liveEl && !view._anim) liveEl.textContent = err ? 'Simulation unavailable' : rolled ? `${nf(rolled)} rolled, ${nf(kept)} kept${ev ? ', ' + nf(hits) + ' ' + evLabel : ''}${share == null ? '' : ', share ' + fmtShare(share)}. Last roll ${last.dice.join(' and ')}, ${last.keep ? 'kept' : 'filtered out'}.` : 'No rolls yet.';
        chips.forEach((b) => { if (R.locked) b.disabled = true; else if (!b.dataset.gated) b.disabled = false; });
      },
      methods: (R) => ({
        /* Run n more rolls (as the chips do). Returns the animation promise. */
        run: (n) => R.inst.set({ ran: Math.round(R.state.ran || 0) + n }),
        reset: () => R.inst.set({ ran: 0 }, { instant: true }),
        counts: () => { const n = Math.round(R.state.ran || 0); upTo(n); return { rolled: err ? 0 : n, kept: err ? 0 : keptTo[n] || 0, event: err ? 0 : evTo[n] || 0 }; },
        values: () => { const n = Math.round(R.state.ran || 0); upTo(n); const k = keptTo[n] || 0, den = ev ? k : n; return { share: den && !err ? (ev ? evTo[n] || 0 : k) / den : null }; },
        last: () => { const n = Math.round(R.state.ran || 0); upTo(n); return n && !err ? rolls[n - 1] : null; },
      }),
    };
    return K.make(host, params, ctx, def);
  });
})();
