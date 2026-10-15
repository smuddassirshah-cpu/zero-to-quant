/* balance widget (docs/AUTHORING.md 3, design-research 5.3 no. 12): operation chips under the balance canvas.
   spec.moves lists the chips: "remove-both" (with a number field), "remove-unknown-both", "halve-both",
   "divide-both" (with a number field), and "remove-item" (no chip: tapping a block removes it from its pan alone). The value is the list of moves; the pans live in the canvas.
   grade: the pans match spec.target ({ left: ["unknown"], right: [4] }, either way round, weights compared by total);
   key "unbalanced" when the beam is not level (a single item was removed), else "unsolved".
   reveal animates the pans to the target in hint indigo. answer() returns the moves that reach the target
   (ZQ.grade.balanceMoves: breadth first over the allowed moves), which set() replays on the canvas. */
(function () {
  'use strict';
  const Z = window.ZQ;

  const REASON = {
    'not-enough': (n) => `Each pan needs at least ${n} to take away.`,
    'no-unknown': (n, x) => `Each pan needs an ${x} to take away.`,
    uneven: () => 'The unknown blocks do not split evenly between the halves.',
    'bad-number': () => 'Type a number first.',
    locked: () => '',
  };

  Z.widgets.register('balance', (host, spec, ctx) => {
    const cv = ctx.canvas;
    const x = (spec.left || []).concat(spec.right || []).find(i => i.kind === 'unknown')?.label || 'x';
    const moves = spec.moves || ['remove-both', 'halve-both'];
    const chip = {
      'remove-both': `<div class="wd-bal-op"><button type="button" class="btn secondary wd-bal-btn" data-op="remove-both">Take away</button><label class="field wd-bal-n"><input type="text" inputmode="decimal" autocomplete="off" aria-label="Amount to take away from both pans" placeholder="n" data-for="remove-both"></label><span class="t-label">from both</span></div>`,
      'remove-unknown-both': `<div class="wd-bal-op"><button type="button" class="btn secondary wd-bal-btn" data-op="remove-unknown-both">Take away ${Z.tex(x)} from both</button></div>`,
      'halve-both': `<div class="wd-bal-op"><button type="button" class="btn secondary wd-bal-btn" data-op="halve-both">Halve both</button></div>`,
      'divide-both': `<div class="wd-bal-op"><button type="button" class="btn secondary wd-bal-btn" data-op="divide-both">Divide both by</button><label class="field wd-bal-n"><input type="text" inputmode="decimal" autocomplete="off" aria-label="Divide both pans by" placeholder="k" data-for="divide-both"></label></div>`,
    };
    const el = Z.h(`<div class="wd-bal">
      <p class="wd-bal-eq" aria-live="polite"></p>
      <div class="wd-bal-ops">${moves.map(m => chip[m] || '').join('')}</div>
      <p class="t-caption wd-bal-msg" aria-live="polite" hidden></p>
    </div>`);
    host.append(el);
    const eq = el.querySelector('.wd-bal-eq'), msg = el.querySelector('.wd-bal-msg');
    if (!cv || typeof cv.removeBoth !== 'function') {
      msg.hidden = false; msg.textContent = 'This task needs its balance, which could not be drawn.';
      return { el, value: () => [], grade: () => ({ ok: false, key: null, detail: null }) };
    }
    let locked = false;
    /* "remove-item": tapping one block takes it off its pan alone (the misconception the beam then shows) */
    if (moves.includes('remove-item')) {
      cv.enable('tap', { max: 1 });
      cv.on('change', (e) => { if (e && e.selected && e.selected.length && !locked) { const id = e.selected[0]; cv.set({ selected: [] }, { instant: true }); cv.removeItem(id); } });
    } else cv.enable('balance');

    const side = (list) => {
      const n = list.filter(i => i.kind === 'unknown').length, w = list.filter(i => i.kind === 'weight').reduce((s, i) => s + (+i.value || 0), 0);
      const terms = [];
      if (n) terms.push(n === 1 ? x : `${n}${x}`);
      if (w || !n) terms.push(Z.canvas.fmtNum(w, 3));
      return { n, w, tex: terms.join(' + ') };
    };
    const showEq = () => { const st = cv.get(); eq.innerHTML = Z.tex(`${side(st.left || []).tex} ${cv.isLevel && !cv.isLevel() ? '\\neq' : '='} ${side(st.right || []).tex}`); };
    const say = (t) => { msg.hidden = !t; msg.textContent = t || ''; };
    cv.on('change', (e) => { if (e && e.moves) { showEq(); ctx.change && ctx.change({ moves: e.moves }); } });
    showEq();

    const numFor = (op) => { const inp = el.querySelector(`[data-for="${op}"]`); const v = Z.widgets.parseNum(inp ? inp.value : ''); return { inp, v }; };
    const run = (op) => {
      if (locked) return;
      let r;
      if (op === 'remove-both') { const { v } = numFor(op); r = Number.isFinite(v) ? cv.removeBoth(v) : { ok: false, reason: 'bad-number' }; if (!r.ok) say((REASON[r.reason] || (() => ''))(v, x)); }
      else if (op === 'remove-unknown-both') { r = cv.removeBoth(x); if (!r.ok) say(REASON[r.reason]?.(0, x) || ''); }
      else if (op === 'halve-both') { r = cv.halveBoth(); if (!r.ok) say(REASON[r.reason]?.() || ''); }
      else if (op === 'divide-both') { const { v } = numFor(op); r = Number.isFinite(v) ? cv.divideBoth(v) : { ok: false, reason: 'bad-number' }; if (!r.ok) say(REASON[r.reason]?.() || ''); }
      if (r && r.ok) say('');
    };
    el.addEventListener('click', (e) => { const b = e.target.closest('[data-op]'); if (b) run(b.dataset.op); });
    el.addEventListener('keydown', (e) => { if (e.key === 'Enter' && e.target.dataset && e.target.dataset.for) { e.preventDefault(); e.stopPropagation(); run(e.target.dataset.for); } });

    const tgt = spec.target || { left: ['unknown'], right: [] };
    const want = (list) => ({ n: list.filter(t => t === 'unknown').length, w: list.filter(t => typeof t === 'number').reduce((s, v) => s + v, 0) });
    const matches = (a, b) => a.n === b.n && Math.abs(a.w - b.w) < 1e-9;
    const itemIds = () => { const st = cv.get(); return [...(st.left || []), ...(st.right || [])].map(i => i.id); };
    const replay = (list) => {
      cv.reset();
      for (const m of list || []) {
        if (m.op === 'remove-both') cv.removeBoth(m.n);
        else if (m.op === 'halve-both') cv.halveBoth();
        else if (m.op === 'divide-both') cv.divideBoth(m.n);
        else if (m.op === 'remove-item') cv.removeItem(m.id);
      }
      showEq();
    };
    const targetItems = (list, s) => list.map((t, k) => (t === 'unknown' ? { id: `${s}-x${k + 1}`, kind: 'unknown', label: x } : { id: `${s}-w${k + 1}`, kind: 'weight', value: t }));
    const setLocked = (on) => { locked = on; el.querySelectorAll('button, input').forEach(n => { n.disabled = on; }); cv.lock && cv.lock(on); };

    return {
      el,
      value: () => (cv.moves ? cv.moves() : []),
      set(v) { replay(Array.isArray(v) ? v : v && v.moves); ctx.change && ctx.change({ moves: cv.moves() }); },
      /* The authored target reached by the allowed moves (the test hook applies it through set) */
      answer: () => Z.grade.balanceMoves({ ...spec, left: spec.left || (cv.params || {}).left, right: spec.right || (cv.params || {}).right }),
      ready: () => cv.moves().length > 0,
      dirty: () => cv.moves().length > 0,
      grade() {
        const st = cv.get(), L = side(st.left || []), R = side(st.right || []), a = want(tgt.left || []), b = want(tgt.right || []);
        const ok = (matches(L, a) && matches(R, b)) || (matches(L, b) && matches(R, a));
        if (ok) return { ok, key: null, detail: { moves: cv.moves() } };
        const level = cv.isLevel ? cv.isLevel() : true;
        return { ok: false, key: level ? 'unsolved' : 'unbalanced', detail: { moves: cv.moves() } };
      },
      lock() { setLocked(true); },
      unlock() { setLocked(false); cv.unmark && cv.unmark(); cv.unflash && cv.unflash(); say(''); },
      markGraded(res) { cv.unmark && cv.unmark(); if (cv.mark) cv.mark(itemIds(), res && res.ok ? 'is-correct' : 'is-notyet'); },
      reveal() {
        cv.unmark && cv.unmark();
        cv.set({ left: targetItems(tgt.left || [], 'l'), right: targetItems(tgt.right || [], 'r') });
        if (cv.mark) cv.mark(itemIds(), 'is-reveal');
        setLocked(true); showEq(); say('');
      },
      showWhy(key) {
        if (key !== 'unbalanced' || !cv.flash) return false;
        const st = cv.get(), tilt = cv.tilt ? cv.tilt() : 0;
        const light = tilt > 0 ? st.left : st.right; // the raised pan lost weight
        cv.flash((light || []).map(i => i.id)); return true;
      },
      reset() { cv.unmark && cv.unmark(); setLocked(false); cv.reset(); el.querySelectorAll('input').forEach(i => { i.value = ''; }); say(''); showEq(); },
      focus() { const b = el.querySelector('button'); if (b) b.focus({ preventScroll: true }); },
      destroy() {},
    };
  });
})();
