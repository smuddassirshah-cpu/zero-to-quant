/* Multiple select widget (docs/AUTHORING.md 3, design-research 5.3 no. 2). Same flat cards as choice, each with a
   square check. Exact set match; key is the first wrong pick, else the first missing option. On not-yet the wrong
   picks take the amber cross and the right picks the learner kept dim to grey, so the answer is never given away. */
(function () {
  'use strict';
  const Z = window.ZQ;

  Z.widgets.register('multi', (host, spec, ctx) => {
    const opts = Z.widgets.orderOptions(spec, ctx);
    const cols = Z.widgets.optColumns(spec, opts);
    const el = Z.h(`<div class="opts wd-opts wd-multi wd-cols-${cols}" role="group" aria-label="${Z.esc(spec.label || 'Answer options. Select all that apply.')}">${opts.map((o, i) =>
      `<button type="button" class="opt wd-opt" role="checkbox" aria-checked="false" tabindex="${i === 0 ? 0 : -1}" data-id="${Z.esc(o.id)}"><span class="wd-check" aria-hidden="true">${Z.icon('check')}</span>${Z.widgets.optBody(o)}</button>`).join('')}</div>`);
    host.append(el);
    const btns = [...el.querySelectorAll('.opt')];
    const on = new Set();
    let locked = false, undoWhy = null;
    const sync = () => btns.forEach((b, i) => { const v = on.has(i); b.classList.toggle('selected', v); b.setAttribute('aria-checked', String(v)); });
    const toggle = (i, fromKey) => {
      if (locked || i < 0 || i >= btns.length) return;
      if (on.has(i)) on.delete(i); else on.add(i);
      sync(); if (fromKey) btns[i].focus({ preventScroll: true });
      Z.sound('tap'); ctx.change && ctx.change({ ids: [...on].map(j => opts[j].id) });
    };
    btns.forEach((b, i) => b.addEventListener('click', () => toggle(i)));
    el.addEventListener('keydown', (e) => {
      const i = btns.indexOf(document.activeElement);
      if (i < 0) return;
      const d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
      if (d) { e.preventDefault(); const j = (i + d + btns.length) % btns.length; btns.forEach((b, k) => b.setAttribute('tabindex', k === j ? '0' : '-1')); btns[j].focus(); }
      else if (e.key === ' ') { e.preventDefault(); toggle(i); }
    });
    const strip = () => btns.forEach(b => { b.classList.remove('correct', 'wrong', 'dim', 'wd-rev'); b.querySelector('.badge')?.remove(); });
    const badge = (b, ok) => b.insertAdjacentHTML('beforeend', `<span class="badge" aria-hidden="true">${Z.icon(ok ? 'check' : 'cross')}</span>`);
    const ids = () => [...on].sort((a, b) => a - b).map(j => opts[j].id);
    const clearWhy = () => { if (undoWhy) { undoWhy(); undoWhy = null; } };

    return {
      el,
      value: ids,
      set(v) { on.clear(); (v || []).forEach(id => { const i = opts.findIndex(o => o.id === id); if (i >= 0) on.add(i); }); sync(); ctx.change && ctx.change({ ids: ids() }); },
      answer: () => opts.filter(o => o.correct).map(o => o.id),
      ready: () => on.size > 0,
      pick: (i) => toggle(i, true),
      grade() {
        const wrong = opts.find((o, i) => on.has(i) && !o.correct);
        const missing = opts.find((o, i) => !on.has(i) && o.correct);
        const ok = !wrong && !missing && on.size > 0;
        const k = wrong || missing;
        return { ok, key: ok ? null : k ? k.id : null, line: ok ? null : wrong ? (wrong.why || null) : null, detail: { ids: ids() } };
      },
      lock() { locked = true; btns.forEach(b => b.setAttribute('aria-disabled', 'true')); },
      unlock() { locked = false; clearWhy(); strip(); btns.forEach(b => b.setAttribute('aria-disabled', 'false')); sync(); },
      markGraded(res) {
        strip();
        btns.forEach((b, i) => {
          const o = opts[i];
          if (!on.has(i)) { if (res.ok) b.classList.add('dim'); return; }
          b.classList.remove('selected');
          if (res.ok) { b.classList.add('correct'); badge(b, true); }
          else if (!o.correct) { b.classList.add('wrong'); badge(b, false); }
          else b.classList.add('dim');
        });
      },
      reveal() {
        clearWhy(); strip(); locked = true; on.clear();
        btns.forEach((b, i) => { b.classList.remove('selected'); b.setAttribute('aria-checked', String(!!opts[i].correct)); b.setAttribute('aria-disabled', 'true'); b.classList.add(opts[i].correct ? 'wd-rev' : 'dim'); });
      },
      showWhy(key) {
        const o = opts.find(x => x.id === key);
        if (!o || !o.canvas || !ctx.canvas) return false;
        clearWhy(); undoWhy = Z.grade.patchCanvas(ctx.canvas, o.canvas); return true;
      },
      reset() { clearWhy(); strip(); on.clear(); sync(); },
      focus() { btns[0]?.focus({ preventScroll: true }); },
      destroy() { clearWhy(); },
    };
  });
})();
