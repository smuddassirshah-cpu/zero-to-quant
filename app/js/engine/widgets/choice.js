/* Single choice widget (docs/AUTHORING.md 3, design-research 5.3 no. 1 and 4.5).
   Flat option cards: two columns when there are 4 or fewer short options, otherwise stacked. Keys 1 to 9 pick
   (the player calls pick(i)); arrows move a roving focus inside the group. Graded states: the chosen card takes a
   check or cross badge; on a correct answer the unchosen cards dim. reveal() marks the correct card in hint indigo.
   Optional per-option "canvas": a state patch that showWhy(key) applies to the screen canvas after a wrong pick. */
(function () {
  'use strict';
  const Z = window.ZQ;

  /* Shared by choice and multi */
  const plainLen = (t) => String(t ?? '').replace(/\$[^$]*\$/g, 'xxxx').length;
  const optBody = (o) => {
    const img = o.image || (o.text && typeof o.text === 'object' && o.text.image);
    if (img) return `<span class="wd-opt-img" data-track>${window.ZQArt ? window.ZQArt(img, { label: o.alt || '' }) : ''}</span>`;
    /* item 391: a fenced block in an option (```python ... ```) is a multi-line code block, no Copy button */
    const t = String(o.text ?? '');
    if (t.includes('```')) return `<span class="wd-opt-tx">${t.split(/```[\w+-]*\n?([\s\S]*?)```/).map((part, k) => (k % 2 ? `<pre class="wd-opt-code t-code">${Z.esc(part.replace(/\n$/, ''))}</pre>` : part.trim() ? `<span>${Z.grade.inline(part.trim())}</span>` : '')).join('')}</span>`;
    return `<span class="wd-opt-tx">${Z.grade.inline(t)}</span>`;
  };
  const columns = (spec, opts) => {
    if (spec.layout === 'stack') return 1;
    if (spec.layout === 'grid') return 2;
    return opts.length <= 4 && opts.every(o => o.image || plainLen(o.text) <= 28) ? 2 : 1;
  };
  Z.widgets.optBody = optBody; Z.widgets.optColumns = columns;

  Z.widgets.register('choice', (host, spec, ctx) => {
    const opts = spec.shuffle ? Z.widgets.shuffle(spec.options || [], ctx.rng || Math.random) : (spec.options || []).slice();
    const cols = columns(spec, opts);
    const el = Z.h(`<div class="opts wd-opts wd-cols-${cols}" role="radiogroup" aria-label="${Z.esc(spec.label || 'Answer options')}">${opts.map((o, i) =>
      `<button type="button" class="opt wd-opt" role="radio" aria-checked="false" tabindex="${i === 0 ? 0 : -1}" data-id="${Z.esc(o.id)}">${optBody(o)}</button>`).join('')}</div>`);
    host.append(el);
    const btns = [...el.querySelectorAll('.opt')];
    let sel = -1, locked = false, undoWhy = null;

    const roving = (i) => btns.forEach((b, j) => b.setAttribute('tabindex', j === i ? '0' : '-1'));
    const select = (i, fromKey) => {
      if (locked || i < 0 || i >= btns.length) return;
      sel = i;
      btns.forEach((b, j) => { b.classList.toggle('selected', j === i); b.setAttribute('aria-checked', String(j === i)); });
      roving(i);
      if (fromKey) btns[i].focus({ preventScroll: true });
      Z.sound('tap');
      ctx.change && ctx.change({ id: opts[i].id });
    };
    btns.forEach((b, i) => b.addEventListener('click', () => select(i)));
    el.addEventListener('keydown', (e) => {
      const i = btns.indexOf(document.activeElement);
      if (i < 0) return;
      const d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
      if (d) { e.preventDefault(); const j = (i + d + btns.length) % btns.length; locked ? (roving(j), btns[j].focus()) : select(j, true); }
      else if (e.key === ' ') { e.preventDefault(); select(i); }
    });
    const strip = () => btns.forEach(b => { b.classList.remove('correct', 'wrong', 'dim', 'wd-rev'); b.querySelector('.badge')?.remove(); });
    const badge = (b, ok) => b.insertAdjacentHTML('beforeend', `<span class="badge" aria-hidden="true">${Z.icon(ok ? 'check' : 'cross')}</span>`);
    const clearWhy = () => { if (undoWhy) { undoWhy(); undoWhy = null; } };

    return {
      el,
      value: () => (sel >= 0 ? opts[sel].id : null),
      set(v) { const i = opts.findIndex(o => o.id === v); if (i >= 0) { const l = locked; locked = false; select(i); locked = l; } },
      answer: () => (opts.find(o => o.correct) || {}).id ?? null,
      ready: () => sel >= 0,
      pick: (i) => select(i, true),
      grade() {
        if (sel < 0) return { ok: false, key: null, detail: null };
        const o = opts[sel];
        return { ok: !!o.correct, key: o.id, line: o.correct ? null : (o.why || null), detail: { id: o.id } };
      },
      lock() { locked = true; btns.forEach(b => b.setAttribute('aria-disabled', 'true')); },
      unlock() {
        locked = false; clearWhy(); strip();
        btns.forEach(b => b.setAttribute('aria-disabled', 'false'));
        if (sel >= 0) btns[sel].classList.add('selected');
      },
      markGraded(res) {
        if (sel < 0) return;
        const b = btns[sel];
        strip(); b.classList.remove('selected');
        b.classList.add(res.ok ? 'correct' : 'wrong'); badge(b, res.ok);
        if (res.ok) btns.forEach((x, j) => { if (j !== sel) x.classList.add('dim'); });
      },
      reveal() {
        clearWhy(); strip(); locked = true;
        btns.forEach((b, j) => { b.classList.remove('selected'); b.setAttribute('aria-checked', 'false'); b.setAttribute('aria-disabled', 'true'); b.classList.add(opts[j].correct ? 'wd-rev' : 'dim'); });
      },
      showWhy(key) {
        const o = opts.find(x => x.id === key);
        if (!o || !o.canvas || !ctx.canvas) return false;
        clearWhy(); undoWhy = Z.grade.patchCanvas(ctx.canvas, o.canvas); return true;
      },
      reset() { clearWhy(); strip(); sel = -1; btns.forEach(b => { b.classList.remove('selected'); b.setAttribute('aria-checked', 'false'); }); roving(0); },
      focus() { (btns[sel] || btns[0])?.focus({ preventScroll: true }); },
      destroy() { clearWhy(); },
    };
  });
})();
