/* Numeric entry widget (docs/AUTHORING.md 3, design-research 5.3 no. 3).
   One field with an optional unit (a currency sign sits before the number, a word or % after it). Accepts integers,
   decimals, fractions a/b, mixed numbers and percentages. With unit "%" the learner types 16.7 and the engine
   compares 0.167. The accepted-answer line shows after a correct answer, a reveal, or a final (one-try) grade.
   Optional wrong[].canvas: a state patch that showWhy(key) applies to the screen canvas. */
(function () {
  'use strict';
  const Z = window.ZQ;
  const G = () => Z.grade;

  Z.widgets.register('numeric', (host, spec, ctx) => {
    const unit = spec.unit || '';
    const pre = /^[£$€]$/.test(unit);
    const pct = unit === '%';
    const el = Z.h(`<div class="wd-num">
      <label class="field wd-field">${pre ? `<span class="unit wd-pre">${Z.esc(unit)}</span>` : ''}<input type="text" inputmode="decimal" autocomplete="off" spellcheck="false" aria-label="${Z.esc(spec.label || 'Your answer')}" placeholder="${Z.esc(spec.placeholder || '')}">${unit && !pre ? `<span class="unit">${Z.esc(unit)}</span>` : ''}</label>
      <p class="t-caption wd-help" hidden>Type a number, a fraction such as 3/4, or a decimal such as 0.75.</p>
      <p class="t-caption wd-accept" hidden></p>
    </div>`);
    host.append(el);
    const field = el.querySelector('.field'), input = el.querySelector('input'), help = el.querySelector('.wd-help'), acc = el.querySelector('.wd-accept');
    let undoWhy = null;
    const parsed = () => {
      const t = input.value.trim();
      if (!t) return NaN;
      const v = G().parseNum(t);
      return pct && !t.includes('%') ? v / 100 : v;
    };
    const syncHelp = () => { const t = input.value.trim(); help.hidden = !t || Number.isFinite(parsed()) || /^[-−]?[\d.,]*\/?$/.test(t); };
    input.addEventListener('input', () => { syncHelp(); ctx.change && ctx.change({ text: input.value }); });
    const acceptText = () => {
      if (spec.accept) return 'Accepted: ' + G().inline(spec.accept);
      const t = spec.tol || { abs: 0 }, a = +spec.answer, k = pct ? 100 : 1;
      if (t.rel) return `Accepted: ${G().fmtNum(a * k * (1 - t.rel))} to ${G().fmtNum(a * k * (1 + t.rel))}`;
      if (t.abs) return `Accepted: ${G().fmtNum((a - t.abs) * k)} to ${G().fmtNum((a + t.abs) * k)}`;
      return `Accepted: ${G().fmtNum(a * k)} exactly`;
    };
    const showAccept = () => { acc.innerHTML = acceptText(); acc.hidden = false; Z.mathify && Z.mathify(acc); };
    const mark = (k) => { field.classList.remove('correct', 'wrong', 'wd-rev'); if (k) field.classList.add(k); };
    const clearWhy = () => { if (undoWhy) { undoWhy(); undoWhy = null; } };
    const answerText = () => G().fmtNum(pct ? +spec.answer * 100 : +spec.answer);

    return {
      el, input,
      value: () => input.value.trim(),
      set(v) { input.value = v == null ? '' : String(v); syncHelp(); ctx.change && ctx.change({ text: input.value }); },
      answer: answerText,
      ready: () => Number.isFinite(parsed()),
      dirty: () => input.value !== '',
      grade() {
        const v = parsed();
        if (!Number.isFinite(v)) return { ok: false, key: null, detail: { value: null } };
        const ok = G().within(v, +spec.answer, spec.tol);
        const w = ok ? null : G().matchWrong(v, spec.wrong, { abs: 1e-9 });
        return { ok, key: w ? w.id : null, detail: { value: v } };
      },
      lock() { input.readOnly = true; },
      unlock() { input.readOnly = false; mark(null); clearWhy(); acc.hidden = true; },
      markGraded(res) { mark(res.ok ? 'correct' : 'wrong'); if (res.ok || res.final) showAccept(); },
      reveal() { clearWhy(); input.value = answerText(); input.readOnly = true; mark('wd-rev'); help.hidden = true; showAccept(); },
      showWhy(key) {
        const w = (spec.wrong || []).find(x => x.id === key);
        if (!w || !w.canvas || !ctx.canvas) return false;
        clearWhy(); undoWhy = G().patchCanvas(ctx.canvas, w.canvas); return true;
      },
      reset() { clearWhy(); input.value = ''; input.readOnly = false; mark(null); acc.hidden = true; help.hidden = true; },
      focus() { input.focus({ preventScroll: true }); },
      destroy() { clearWhy(); },
    };
  });
})();
