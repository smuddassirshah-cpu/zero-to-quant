/* Numeric entry widget (docs/AUTHORING.md 3, design-research 5.3 no. 3).
   One field with an optional unit (a currency sign sits before the number, a word or % after it). Accepts integers,
   decimals, fractions a/b, mixed numbers and percentages. With unit "%" the learner types 16.7 and the engine
   compares 0.167. The accepted-answer line shows after a correct answer, a reveal, or a final (one-try) grade.
   Optional wrong[].canvas: a state patch that showWhy(key) applies to the screen canvas.
   A set answer (answers: [..], unordered: true; ENGINE-BACKLOG 832): the learner types the values separated by commas, in any
   order ("2, -5", "x = 2 or x = -5", ± for both of a ± b); each value is graded as the single answer would be, a wrong number of
   values returns key "count" (grade.js numSetGrade), and wrong[].value is a comma-separated list. */
(function () {
  'use strict';
  const Z = window.ZQ;
  const G = () => Z.grade;

  Z.widgets.register('numeric', (host, spec, ctx) => {
    const unit = spec.unit || '';
    const pre = /^[£$€]$/.test(unit);
    const pct = unit === '%';
    const isSet = G().isSetSpec(spec) && spec.unordered === true;
    const el = Z.h(`<div class="wd-num">
      <label class="field wd-field">${pre ? `<span class="unit wd-pre">${Z.esc(unit)}</span>` : ''}<input type="text" inputmode="${isSet ? 'text' : 'decimal'}" autocomplete="off" spellcheck="false" aria-label="${Z.esc(spec.label || 'Your answer')}" placeholder="${Z.esc(spec.placeholder || '')}">${unit && !pre ? `<span class="unit">${Z.esc(unit)}</span>` : ''}</label>
      <p class="t-caption wd-help" hidden>${isSet ? 'Type the values separated by commas, for example 2, -5. A fraction such as 3/4 or a decimal is fine.' : 'Type a number, a fraction such as 3/4, or a decimal such as 0.75.'}</p>
      <p class="t-caption wd-accept" hidden></p>
    </div>`);
    const dp = Z.widgets.dataPanel(spec); if (dp) el.prepend(dp);   // performance task "data": the file to read
    host.append(el);
    const field = el.querySelector('.field'), input = el.querySelector('input'), help = el.querySelector('.wd-help'), acc = el.querySelector('.wd-accept');
    let undoWhy = null;
    const parsed = () => {
      const t = input.value.trim();
      if (!t) return NaN;
      if (isSet) { const sv = G().numSetValues(t, { percent: pct }); return sv.length && sv.every(Number.isFinite) ? sv[0] : NaN; }
      const v = G().parseNum(t);
      return pct && !t.includes('%') ? v / 100 : v;
    };
    const syncHelp = () => { const t = input.value.trim(); help.hidden = !t || Number.isFinite(parsed()) || (isSet ? /[,;]\s*$|[-−+]\s*$|\/\s*$|\b(?:o|or|a|an|and)\s*$/.test(t) : /^[-−]?[\d.,]*\/?$/.test(t)); };
    input.addEventListener('input', () => { syncHelp(); ctx.change && ctx.change({ text: input.value }); });
    const acceptText = () => {
      if (spec.accept) return 'Accepted: ' + G().inline(spec.accept);
      if (isSet) { const st = spec.tol || { abs: 0 }; return `Accepted: ${G().setAnswerText(spec)}, in either order${st.rel ? ` (each within ${G().fmtNum(st.rel * 100)}%)` : st.abs ? ` (each within ${G().fmtNum(st.abs)})` : ''}`; }
      const t = spec.tol || { abs: 0 }, a = +spec.answer, k = pct ? 100 : 1;
      if (t.rel) return `Accepted: ${G().fmtNum(a * k * (1 - t.rel))} to ${G().fmtNum(a * k * (1 + t.rel))}`;
      if (t.abs) return `Accepted: ${G().fmtNum((a - t.abs) * k)} to ${G().fmtNum((a + t.abs) * k)}`;
      return `Accepted: ${G().fmtNum(a * k)} exactly`;
    };
    const showAccept = () => { acc.innerHTML = acceptText(); acc.hidden = false; Z.mathify && Z.mathify(acc); };
    const mark = (k) => { field.classList.remove('correct', 'wrong', 'wd-rev'); if (k) field.classList.add(k); };
    const clearWhy = () => { if (undoWhy) { undoWhy(); undoWhy = null; } };
    const answerText = () => (isSet ? G().setAnswerText(spec) : G().fmtNum(pct ? +spec.answer * 100 : +spec.answer));

    return {
      el, input,
      value: () => input.value.trim(),
      set(v) { input.value = v == null ? '' : String(v); syncHelp(); ctx.change && ctx.change({ text: input.value }); },
      answer: answerText,
      ready: () => Number.isFinite(parsed()),
      dirty: () => input.value !== '',
      grade() {
        if (isSet) { const r = G().numSetGrade(spec, input.value); return { ok: r.ok, key: r.key, line: r.line, detail: r.detail }; }
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
