/* Expression entry widget (docs/AUTHORING.md 3, design-research 5.3 no. 4).
   MathLive's <math-field> with the virtual keyboard off by default and a keyboard toggle; the CortexJS Compute
   Engine decides equivalence (isEqual after simplify, with a 5-point numeric second opinion for one variable).
   Both load lazily on the first expression widget with a 6 s budget. If either fails, the widget falls back to a
   plain text field compared, after normExpr, against the answer and the authored accept[] forms. */
(function () {
  'use strict';
  const Z = window.ZQ;
  const G = () => Z.grade;
  const KB = '<svg class="icon sm" viewBox="0 0 24 24" aria-hidden="true"><path d="M3.5 7h17v10h-17zM7 10h.01M10 10h.01M13 10h.01M16 10h.01M8 14h8"/></svg>';

  Z.widgets.register('expression', (host, spec, ctx) => {
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
    G().maths().then(build, () => build({ mathlive: false, ce: null }));

    const lockNow = (v) => { if (mf) mf.readOnly = v; if (txt) txt.readOnly = v; };
    const forms = () => [spec.answer, ...(spec.accept || [])].filter(Boolean);
    const equal = (inputLatex, inputAscii, target) => {
      if (ce && G().exprEqual(ce, inputLatex, target)) return true;
      const n = G().normExpr(inputAscii || inputLatex);
      return !!n && (n === G().normExpr(target));
    };
    const acceptText = () => 'Accepted: any expression equal to ' + G().inline('$' + spec.answer + '$') + (spec.accept && spec.accept.length ? ', for example ' + spec.accept.slice(0, 2).map(a => `<code class="lsn-ic">${Z.esc(a)}</code>`).join(' or ') : '') + '.';
    const showAccept = () => { acc.innerHTML = acceptText(); acc.hidden = false; };

    return {
      el,
      value: () => latex(),
      set(v) { setValue(v); changed(); },
      answer: () => (mf || !txt ? spec.answer : (spec.accept && spec.accept[0]) || spec.answer),
      ready: () => loaded && latex().trim() !== '',
      grade() {
        const L = latex(), A = ascii();
        if (!L.trim()) return { ok: false, key: null };
        const ok = forms().some(f => equal(L, A, f));
        let key = null;
        if (!ok) { const w = (spec.wrong || []).find(x => x.tex && equal(L, A, x.tex)); key = w ? w.id : null; }
        return { ok, key, detail: { latex: L, ascii: A, engine: ce ? 'compute-engine' : 'text' } };
      },
      lock() { locked = true; lockNow(true); },
      unlock() { locked = false; lockNow(false); mark(null); acc.hidden = true; },
      markGraded(res) { mark(res.ok ? 'correct' : 'wrong'); if (res.ok || res.final) showAccept(); },
      reveal() { setValue(mf || !txt ? spec.answer : (spec.accept && spec.accept[0]) || spec.answer); locked = true; lockNow(true); mark('wd-rev'); showAccept(); },
      reset() { setValue(''); locked = false; lockNow(false); mark(null); acc.hidden = true; changed(); },
      focus() { (mf || txt)?.focus?.(); },
      destroy() { alive = false; try { if (window.mathVirtualKeyboard && window.mathVirtualKeyboard.visible) window.mathVirtualKeyboard.hide(); } catch { /* none */ } },
    };
  });
})();
