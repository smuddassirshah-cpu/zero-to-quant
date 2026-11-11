/* Expression entry widget (docs/AUTHORING.md 3, design-research 5.3 no. 4).
   MathLive's <math-field> with the virtual keyboard off by default and a keyboard toggle; the CortexJS Compute
   Engine decides equivalence (isEqual after simplify, with a 5-point numeric second opinion for one variable).
   Both load lazily on the first expression widget with a 6 s budget. If either fails, the widget falls back to a
   plain text field compared, after normExpr, against the answer and the authored accept[] forms.
   form: "expanded" | "factorised" | "factorised-fully" | "completed-square" | "simplified" | "rectangular" also asks for a shape, judged on the Compute Engine's canonical
   MathJSON of the input: expanded has no sum inside a product or power (an Add of monomials, or one monomial);
   factorised is a Multiply with a sum among its factors, or a power of a sum (a leading minus is allowed);
   simplified has no more nodes than its own simplify(), and a constant answer is also evaluated (no sum of two plain numbers, no
   division by a complex number, no bracket holding i inside a product); rectangular (a constant answer) is a + bi in that
   sense, so retyping the prompt's \frac{4+7i}{2-3i} does not score (ENGINE-BACKLOG 596). An equal answer in the wrong shape returns key "form".
   factorised-fully is factorised with no bracket left holding a common whole-number factor or a quadratic that factorises;
   completed-square is a(x+p)^2 + q (grade.js shapeFullyFactorised, shapeCompletedSquare; ENGINE-BACKLOG 830, 831).
   A set answer (answers: [...], unordered: true) takes the values separated by commas, in any order, \pm for both values; a wrong
   number of values returns key "count" (grade.js exprSetGrade; ENGINE-BACKLOG 832).
   Complex answers (an i in either side) compare real and imaginary parts at every seeded point; a vector or matrix
   answer ((2, -1, 3) or a pmatrix) compares entry by entry and a wrong size returns key "length" (grade.js).
   Without the engine the text fallback already demands a normalised match with answer or accept[], which authors
   write in the asked form. */
(function () {
  'use strict';
  const Z = window.ZQ;
  const G = () => Z.grade;
  const KB = '<svg class="icon sm" viewBox="0 0 24 24" aria-hidden="true"><path d="M3.5 7h17v10h-17zM7 10h.01M10 10h.01M13 10h.01M16 10h.01M8 14h8"/></svg>';

  /* The shape checks and the whole grade of one typed expression live in grade.js (exprGrade, exprForms), shared with the tests and
     tools/grade-regression.mjs (ENGINE-BACKLOG 898 to 908). */
  Z.widgets.exprForms = G().exprForms;

  Z.widgets.register('expression', (host, spec, ctx) => {
    const isSet = G().isSetSpec(spec) && spec.unordered === true;
    const el = Z.h(`<div class="wd-expr is-loading">
      <div class="field wd-field wd-expr-field"><span class="wd-expr-load t-caption">Loading the maths editor</span></div>
      <p class="t-caption wd-expr-note" hidden></p>
      <p class="t-caption wd-accept" hidden></p>
    </div>`);
    host.append(el);
    const box = el.querySelector('.wd-expr-field'), note = el.querySelector('.wd-expr-note'), acc = el.querySelector('.wd-accept');
    let mf = null, txt = null, ce = null, loaded = false, locked = false, pending = null, alive = true;

    const mark = (k) => { box.classList.remove('correct', 'wrong', 'wd-rev'); if (k) box.classList.add(k); };
    const changed = () => ctx.change && ctx.change({ latex: latex() });
    const latex = () => (mf ? mf.value : txt ? txt.value : pending || '');
    const ascii = () => {
      if (mf) { try { return mf.getValue('ascii-math'); } catch { return mf.value; } }
      return txt ? txt.value : '';
    };
    const setValue = (v) => {
      if (mf) mf.value = v || '';
      else if (txt) txt.value = v || '';
      else pending = v;
    };
    const build = (m) => {
      if (!alive) return;
      ce = m.ce; loaded = true; el.classList.remove('is-loading');
      box.innerHTML = '';
      if (m.mathlive) {
        try {
          const MF = window.MathfieldElement;
          if (MF) { MF.soundsDirectory = null; MF.plonkSound = null; }
        } catch { /* older build */ }
        mf = document.createElement('math-field');
        mf.className = 'wd-mf';
        mf.setAttribute('aria-label', spec.label || 'Your expression');
        mf.mathVirtualKeyboardPolicy = 'manual';
        mf.setAttribute('math-virtual-keyboard-policy', 'manual');
        box.append(mf);
        const kb = Z.h(`<button type="button" class="icon-btn wd-kb" aria-pressed="false" aria-label="Show the maths keyboard">${KB}</button>`);
        box.append(kb);
        kb.addEventListener('click', () => {
          const vk = window.mathVirtualKeyboard; if (!vk) return;
          const show = !vk.visible;
          mf.focus();
          setKeyboard(vk);
          if (show) vk.show(); else vk.hide();
          kb.setAttribute('aria-pressed', String(show));
        });
        mf.addEventListener('input', changed);
        mf.addEventListener('keydown', (e) => {
          // Enter belongs to the player's primary button
          if (e.key === 'Enter') { e.preventDefault(); e.stopPropagation(); document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true })); }
        }, true);
      } else {
        txt = Z.h(`<input type="text" class="wd-expr-txt" autocomplete="off" spellcheck="false" aria-label="${Z.esc(spec.label || 'Your expression')}" placeholder="For example (x+1)/2">`);
        box.append(txt);
        txt.addEventListener('input', changed);
        note.textContent = 'Type the expression as text: use / for fractions, ^ for powers and * for products.';
        note.hidden = false;
      }
      if (pending != null) { setValue(pending); pending = null; }
      if (locked) lockNow(true);
      changed();
    };
    /* a set answer needs a comma and a plus-or-minus (ENGINE-BACKLOG 832): its own layout, and the default back for any other item */
    const SET_KEYBOARD = [{
      label: '123', tooltip: 'Numbers, comma and plus or minus', rows: [
        ['[7]', '[8]', '[9]', '[+]', '\\pm', '[,]', '[backspace]'],
        ['[4]', '[5]', '[6]', '[-]', '\\sqrt{#0}', '\\frac{#@}{#?}', '[left]'],
        ['[1]', '[2]', '[3]', '[*]', 'x', 'y', '[right]'],
        ['[0]', '[.]', '[(]', '[)]', '[=]', '#@^{#?}', '[hide-keyboard]'],
      ],
    }];
    const setKeyboard = (vk) => {
      try {
        if (isSet) { vk.layouts = SET_KEYBOARD; Z.setKeyboardActive = true; }
        else if (Z.setKeyboardActive) { vk.layouts = 'default'; Z.setKeyboardActive = false; }
      } catch { /* the default keyboard stays */ }
    };
    const loadP = G().maths().then(build, () => build({ mathlive: false, ce: null }));

    const lockNow = (v) => { if (mf) mf.readOnly = v; if (txt) txt.readOnly = v; };
    const answerLatex = () => (isSet ? G().setAnswerText(spec) : spec.answer);
    const acceptText = () => isSet ? 'Accepted: ' + G().inline('$' + G().setAnswerText(spec) + '$') + ', in either order.' : 'Accepted: any expression equal to ' + G().inline('$' + spec.answer + '$') + (spec.accept && spec.accept.length ? ', for example ' + spec.accept.slice(0, 2).map(a => G().inline("$" + a + "$")).join(' or ') : '') + '.';
    const showAccept = () => { acc.innerHTML = acceptText(); acc.hidden = false; };

    const api = {
      el,
      value: () => latex(),
      set(v) { setValue(v); changed(); },
      answer: () => (mf || !txt ? answerLatex() : (spec.accept && spec.accept[0]) || answerLatex()),
      /* item 105: a value set while the editor loads (the test hook's answerCorrect) counts; grading then waits for the load */
      ready: () => latex().trim() !== '',
      grade() {
        if (!loaded) return loadP.then(() => api.grade());
        const L = latex(), A = ascii();
        if (!L.trim()) return { ok: false, key: null };
        if (isSet) { const r = G().exprSetGrade(ce, spec, L); return { ok: r.ok, key: r.key, line: r.line, detail: { latex: L, ascii: A, engine: ce ? 'compute-engine' : 'text', form: null } }; }
        const { ok: shaped, key, line } = G().exprGrade(ce, spec, L, A);
        return { ok: shaped, key, line, detail: { latex: L, ascii: A, engine: ce ? 'compute-engine' : 'text', form: spec.form || null } };
      },
      lock() { locked = true; lockNow(true); },
      unlock() { locked = false; lockNow(false); mark(null); acc.hidden = true; },
      markGraded(res) { mark(res.ok ? 'correct' : 'wrong'); if (res.ok || res.final) showAccept(); },
      reveal() { setValue(mf || !txt ? answerLatex() : (spec.accept && spec.accept[0]) || answerLatex()); locked = true; lockNow(true); mark('wd-rev'); showAccept(); },
      reset() { setValue(''); locked = false; lockNow(false); mark(null); acc.hidden = true; changed(); },
      focus() { (mf || txt)?.focus?.(); },
      destroy() { alive = false; try { if (window.mathVirtualKeyboard && window.mathVirtualKeyboard.visible) window.mathVirtualKeyboard.hide(); } catch { /* none */ } },
    };
    return api;
  });
})();
