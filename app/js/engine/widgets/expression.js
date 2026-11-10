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

  /* The shape checks on canonical MathJSON, shared by the widget and tools/test-engine-runtime.mjs (ENGINE-BACKLOG 596).
     A constant answer (no free symbol but the imaginary unit, which the grader reads as the symbol iota) must be evaluated:
     reducible() finds what a learner left undone: two plain numbers added or multiplied, a quotient or power with a complex
     base, a division by a complex number, a product with a bracket that holds i. rectangular() is a + bi: one real part and
     one imaginary term (a number, a surd or a fraction times i), nothing reducible. */
  const hd = (j) => (Array.isArray(j) ? j[0] : null);
  const ar = (j) => (Array.isArray(j) ? j.slice(1) : []);
  const hasI = (j) => j === 'iota' || (Array.isArray(j) && j.some(hasI));
  const isLit = (j) => typeof j === 'number' || (j && typeof j === 'object' && !Array.isArray(j) && 'num' in j) || hd(j) === 'Rational' || (hd(j) === 'Negate' && isLit(ar(j)[0]));
  const isSum = (j) => hd(j) === 'Add' || hd(j) === 'Subtract';
  const reducible = (j) => {
    if (!Array.isArray(j)) return false;
    const h = hd(j), a = ar(j);
    if ((h === 'Add' || h === 'Subtract') && a.filter(isLit).length > 1) return true;
    if (h === 'Multiply' && (a.filter(isLit).length > 1 || a.some(x => isSum(x) && hasI(x)))) return true;
    if (h === 'Divide' && (hasI(a[1]) || (isSum(a[0]) && hasI(a[0])))) return true;
    if (h === 'Power' && hasI(a[0]) && a[0] !== 'iota') return true;
    return a.some(reducible);
  };
  const imagTerm = (j) => {
    if (j === 'iota') return true;
    const h = hd(j), a = ar(j);
    if (h === 'Negate') return imagTerm(a[0]);
    if (h === 'Multiply') { const w = a.filter(hasI); return w.length === 1 && w[0] === 'iota' && a.length === 2; }
    if (h === 'Divide') return imagTerm(a[0]) && !hasI(a[1]);
    return false;
  };
  const rectangular = (j) => {
    if (reducible(j)) return false;
    if (!hasI(j)) return true;                                   // a real number is a + 0i
    const r = hd(j) === 'Negate' && isSum(ar(j)[0]) ? ar(j)[0] : j;
    if (isSum(r)) { const w = ar(r).filter(hasI); return w.length === 1 && imagTerm(w[0]); }
    return imagTerm(r);
  };
  Z.widgets.exprForms = { reducible, rectangular, hasI };

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
    const forms = () => [spec.answer, ...(spec.accept || [])].filter(Boolean);
    const answerLatex = () => (isSet ? G().setAnswerText(spec) : spec.answer);
    const fo = { functions: Array.isArray(spec.functions) ? spec.functions : [], integers: Array.isArray(spec.integers) ? spec.integers : [] }; // letters that are functions here (f(x) stays a call); integers: symbols sampled at whole numbers
    const equal = (inputLatex, inputAscii, target) => {
      if (ce && (spec.upToConstant ? G().exprEqualUpToConstant(ce, inputLatex, target, fo) : G().exprEqual(ce, inputLatex, target, fo))) return true; // item 200: + C need not be listed
      const n = G().normExpr(inputAscii || inputLatex);
      return !!n && (n === G().normExpr(target));
    };
    /* The shape check on canonical MathJSON */
    const FORM_LINE = { 'factorised-fully': 'Factorise fully: a bracket still has a common factor.', 'completed-square': 'Write it as a bracket squared plus a number.', rectangular: 'That is equal, but not in the form a + bi: work out the real and imaginary parts.', expanded: 'That is equal, but not expanded: multiply out every bracket.', factorised: 'That is equal, but not factorised: write it as a product with a bracket.', simplified: 'That is equal, but not simplified: collect like terms and cancel.' };
    const head = (j) => (Array.isArray(j) ? j[0] : null);
    const args = (j) => (Array.isArray(j) ? j.slice(1) : []);
    const hasSum = (j) => head(j) === 'Add' || head(j) === 'Subtract' || args(j).some(hasSum);
    const size = (j) => (Array.isArray(j) ? 1 + args(j).reduce((a, x) => a + size(x), 0) : 1);
    const isSumLike = (j) => head(j) === 'Add' || head(j) === 'Subtract';
    const formOk = (L) => {
      if (!spec.form || !ce) return true;
      try {
        return G().withParsed(ce, L, fo.functions, (e) => {
          const j = e.json;
          if (spec.form === 'expanded') return isSumLike(j) ? args(j).every(t => !hasSum(t)) : !hasSum(j);
          if (spec.form === 'factorised') return G().shapeFactorised(j);
          if (spec.form === 'factorised-fully') return G().shapeFullyFactorised(j);
          if (spec.form === 'completed-square') return G().shapeCompletedSquare(j);
          const constant = !(e.unknowns || []).filter(v => v !== 'iota').length;   // a constant answer must be evaluated, not retyped from the prompt
          if (spec.form === 'rectangular') return constant ? Z.widgets.exprForms.rectangular(j) : true;
          if (spec.form === 'simplified') { if (constant && Z.widgets.exprForms.reducible(j)) return false; try { return size(j) <= size(e.simplify().json); } catch { return true; } }
          return true;
        });
      } catch { return true; }
    };
    const acceptText = () => isSet ? 'Accepted: ' + G().inline('$' + G().setAnswerText(spec) + '$') + ', in either order.' : 'Accepted: any expression equal to ' + G().inline('$' + spec.answer + '$') + (spec.accept && spec.accept.length ? ', for example ' + spec.accept.slice(0, 2).map(a => `<code class="lsn-ic">${Z.esc(a)}</code>`).join(' or ') : '') + '.';
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
        const same = forms().some(f => equal(L, A, f));
        const shaped = same && formOk(L);
        let key = null, line;
        if (same && !shaped) { key = 'form'; line = FORM_LINE[spec.form]; }
        else if (!same) {
          const w = (spec.wrong || []).find(x => x.tex && equal(L, A, x.tex)); key = w ? w.id : null;
          /* item 433: a vector or matrix answer of the wrong size gets its own key and a line saying how many entries */
          if (!w && ce) { const sl = G().exprShapeLine(ce, spec.answer, L, fo.functions); if (sl) { key = 'length'; line = sl; } }
        }
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
