/* tap-regions widget (docs/AUTHORING.md 3, design-research 5.3 no. 8): the learner taps cells, regions or branches on
   the screen's canvas (ctx.canvas.enable('tap')). The value is the selected id set.
   grade: exact set against `answer`; key = the id of a wrong[] entry whose set matches exactly, else the first wrongly
   selected id, else the first missed answer id (so byKey can speak to an extra cell or a missed one).
   markGraded: on a correct answer the selection turns green; otherwise wrong picks turn amber with a cross and right
   picks dim to grey, while missed cells stay neutral. reveal selects the answer in hint indigo. showWhy flashes the
   extra ids of the matched wrong[] set (the double-counted cells) or the wrongly selected ids.
   Count mode ({ count: k, among: [ids] }): ok when exactly k regions are selected, all of them in `among` when it is
   given ("shade any 3 of the 4"); `answer` may be omitted. Keys: a matching wrong[] set, else the first selected id
   outside `among`, else "too-few" or "too-many". reveal selects the first k of `among` (else the first k tappable).
   The player shows the running count in the question line ("2 of 3 shaded" in count mode); ctx.countEl or ctx.count
   are honoured when given. `countWord` replaces the noun in the count. */
(function () {
  'use strict';
  const Z = window.ZQ;

  Z.widgets.register('tap-regions', (host, spec, ctx) => {
    const cv = ctx.canvas;
    const el = Z.h('<div class="wd-tap"><p class="t-caption wd-tap-msg" hidden></p></div>');
    host.append(el);
    const msg = el.querySelector('.wd-tap-msg');
    const count = Number.isInteger(spec.count) && spec.count > 0 ? spec.count : null;
    const among = Array.isArray(spec.among) ? spec.among.map(String) : null;
    const word = spec.countWord || (cv && cv.kind === 'grid' ? 'shaded' : 'selected');
    if (!cv || typeof cv.enable !== 'function') {
      msg.hidden = false; msg.textContent = 'This task needs its diagram, which could not be drawn.';
      return { el, value: () => [], grade: () => ({ ok: false, key: null, detail: null }) };
    }
    cv.enable('tap', { max: spec.max || null, only: spec.only || null });
    /* The answer set: authored, or in count mode the first k of `among` (else of the tappable ids) */
    const tappable = () => Array.from(cv.el.querySelectorAll('[data-tap]')).map(n => n.dataset.id).filter(id => !spec.only || spec.only.includes(id));
    const answer = (spec.answer && spec.answer.length) || !count ? (spec.answer || []).map(String) : (among || tappable()).slice(0, count);
    const inAmong = (id) => !among || among.includes(id);
    const sel = () => ((cv.get() || {}).selected || []).map(String);
    const showCount = (n, text) => {
      const t = text || (count ? `${n} of ${count} ${word}` : `${n} ${word}`);
      if (ctx.countEl) { ctx.countEl.hidden = false; ctx.countEl.textContent = t; }
      if (ctx.count && text) ctx.count(t); // the player keeps the live count itself; only the reveal text is pushed
    };
    if (ctx.countEl) showCount(sel().length);
    cv.on('change', (e) => { if (e && 'selected' in e) { showCount(e.selected.length); ctx.change && ctx.change({ selected: e.selected.slice() }); } });

    const GRADED = ['is-correct', 'is-notyet', 'is-reveal', 'is-dim'];
    const mark = (ids, cls) => {
      if (!ids.length) return;
      if (cv.mark) cv.mark(ids, cls);
      else ids.forEach(id => cv.el.querySelectorAll(`[data-id="${CSS.escape(id)}"]`).forEach(n => n.classList.add(cls)));
    };
    const unmark = () => { if (cv.unmark) cv.unmark(); else cv.el.querySelectorAll(GRADED.map(c => '.' + c).join(',')).forEach(n => n.classList.remove(...GRADED)); };
    const unflash = () => { if (cv.unflash) cv.unflash(); else cv.el.querySelectorAll('.is-flash').forEach(n => n.classList.remove('is-flash')); };
    const sameSet = (a, b) => { const A = new Set(a), B = new Set(b); return A.size === B.size && [...A].every(x => B.has(x)); };
    const split = (s) => (count
      ? { wrong: s.filter(x => !inAmong(x)), hit: s.filter(inAmong), missing: [] }
      : { wrong: s.filter(x => !answer.includes(x)), hit: s.filter(x => answer.includes(x)), missing: answer.filter(x => !s.includes(x)) });

    return {
      el,
      value: () => sel().slice().sort(),
      set(v) { cv.set({ selected: (v || []).map(String) }, { instant: true }); showCount((v || []).length); ctx.change && ctx.change({ selected: (v || []).slice() }); },
      answer: () => answer.slice(),
      ready: () => sel().length > 0,
      dirty: () => sel().length > 0,
      grade() {
        const s = sel(), d = split(s);
        if (count ? s.length === count && !d.wrong.length : sameSet(s, answer)) return { ok: true, key: null, detail: d };
        const w = (spec.wrong || []).find(x => sameSet((x.set || []).map(String), s));
        if (count) return { ok: false, key: w ? w.id : d.wrong[0] ?? (s.length < count ? 'too-few' : 'too-many'), detail: d };
        return { ok: false, key: w ? w.id : d.wrong[0] ?? d.missing[0] ?? null, detail: d };
      },
      lock() { cv.lock && cv.lock(true); },
      unlock() { cv.lock && cv.lock(false); unmark(); unflash(); },
      markGraded(res) {
        unmark();
        const d = split(sel());
        if (res && res.ok) mark(d.hit, 'is-correct');
        else { mark(d.wrong, 'is-notyet'); mark(d.hit, 'is-dim'); }
      },
      reveal() {
        unmark(); unflash();
        cv.set({ selected: answer.slice() });
        mark(answer, 'is-reveal');
        cv.lock && cv.lock(true);
        showCount(answer.length, count ? `${answer.length} of ${count} ${word}` : `${answer.length} ${answer.length === 1 ? 'region' : word === 'shaded' ? 'cells' : 'regions'}`);
      },
      showWhy(key) {
        const w = (spec.wrong || []).find(x => x.id === key);
        const ids = w ? (w.flash || (w.set || []).filter(x => (count ? !inAmong(String(x)) : !answer.includes(String(x))))).map(String) : split(sel()).wrong;
        if (!ids.length) return false;
        if (cv.flash) cv.flash(ids); else return false;
        return true;
      },
      reset() { unmark(); unflash(); cv.lock && cv.lock(false); cv.set({ selected: [] }, { instant: true }); showCount(0); },
      focus() { const n = cv.el.querySelector('[data-tap][tabindex="0"]'); if (n) n.focus({ preventScroll: true }); },
      destroy() { if (cv.enable) cv.enable(null); },
    };
  });
})();
