/* Expression manipulator over an authored state graph (docs/AUTHORING.md 3, design-research 5.3 no. 11).
   The current equation sits large; each operation is a lipped chip. Tapping one animates the equation to the next
   state (old fades out over 120ms, new fades in and rises 8px over 200ms). A breadcrumb shows the path; Undo
   steps back. Any path that reaches target is correct. An op with "why" is a recorded misstep: its why becomes the
   feedback line on the next Check if the target has not been reached; else the current state's why is used. */
(function () {
  'use strict';
  const Z = window.ZQ;

  Z.widgets.register('manipulate', (host, spec, ctx) => {
    const S = spec.states || {};
    const el = Z.h(`<div class="wd-man">
      <div class="wd-man-stage"><div class="wd-man-eq" aria-live="polite"></div></div>
      <ol class="wd-man-path" aria-label="Your steps"></ol>
      <div class="wd-man-ops" role="group" aria-label="Operations"></div>
      <div class="wd-man-foot"><button type="button" class="link-btn wd-man-undo" disabled>Undo</button></div>
    </div>`);
    host.append(el);
    const eq = el.querySelector('.wd-man-eq'), ops = el.querySelector('.wd-man-ops'), pathEl = el.querySelector('.wd-man-path'), undoBtn = el.querySelector('.wd-man-undo'), stage = el.querySelector('.wd-man-stage');
    let path = [spec.start], steps = [], locked = false;
    const cur = () => path[path.length - 1];
    const drawEq = (animate) => {
      const html = Z.tex(S[cur()]?.tex || '', true);
      if (!animate || Z.reducedMotion()) { eq.innerHTML = html; return; }
      const old = eq.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 120, easing: 'cubic-bezier(0.3, 0, 0.8, 0.15)', fill: 'forwards' });
      old.onfinish = () => { eq.innerHTML = html; old.cancel(); eq.animate([{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }], { duration: 200, easing: 'cubic-bezier(0.05, 0.7, 0.1, 1)' }); };
    };
    const draw = (animate) => {
      drawEq(animate);
      const st = S[cur()] || {};
      const list = st.ops || [];
      ops.innerHTML = list.length ? list.map((o, i) => `<button type="button" class="wd-chip wd-op" data-i="${i}">${Z.grade.inline(o.label)}</button>`).join('')
        : `<p class="t-caption wd-man-end">${cur() === spec.target ? 'No more steps. Check your answer.' : 'No steps from here. Undo to try another route.'}</p>`;
      ops.querySelectorAll('.wd-op').forEach(b => { b.disabled = locked; });
      pathEl.innerHTML = path.length > 1 ? path.map((id, i) => `<li class="${i === path.length - 1 ? 'cur' : ''}">${Z.tex(S[id]?.tex || id)}</li>`).join('') : '';
      pathEl.hidden = path.length < 2;
      undoBtn.disabled = locked || path.length < 2;
    };
    const apply = (i) => {
      if (locked) return;
      const op = ((S[cur()] || {}).ops || [])[i];
      if (!op || !S[op.to]) return;
      path.push(op.to); steps.push(op);
      Z.sound('tap');
      draw(true);
      ctx.change && ctx.change({ path: path.slice() });
      ops.querySelector('.wd-op')?.focus({ preventScroll: true });
    };
    ops.addEventListener('click', (e) => { const b = e.target.closest('.wd-op'); if (b) apply(+b.dataset.i); });
    undoBtn.addEventListener('click', () => { if (locked || path.length < 2) return; path.pop(); steps.pop(); draw(true); ctx.change && ctx.change({ path: path.slice() }); });
    draw(false);
    const mark = (k) => { stage.classList.remove('correct', 'wrong', 'wd-rev'); if (k) stage.classList.add(k); };
    const setPath = (p) => {
      const ok = Array.isArray(p) && p[0] === spec.start && p.every((id, i) => i === 0 || ((S[p[i - 1]] || {}).ops || []).some(o => o.to === id));
      path = ok ? p.slice() : [spec.start];
      steps = path.slice(1).map((id, i) => ((S[path[i]] || {}).ops || []).find(o => o.to === id));
      draw(false);
    };
    return {
      el,
      value: () => path.slice(),
      set(v) { setPath(v); ctx.change && ctx.change({ path: path.slice() }); },
      answer: () => Z.grade.manipulatePath(spec),
      ready: () => path.length > 1,
      grade() {
        if (cur() === spec.target) return { ok: true, key: null, detail: { path: path.slice() } };
        const mis = [...steps].reverse().find(o => o && o.why);
        if (mis) return { ok: false, key: mis.to, line: mis.why, detail: { path: path.slice() } };
        return { ok: false, key: cur(), line: S[cur()]?.why || null, detail: { path: path.slice() } };
      },
      lock() { locked = true; draw(false); },
      unlock() { locked = false; mark(null); draw(false); },
      markGraded(res) { mark(res.ok ? 'correct' : 'wrong'); },
      reveal() { setPath(Z.grade.manipulatePath(spec)); locked = true; draw(false); mark('wd-rev'); },
      reset() { locked = false; mark(null); setPath([spec.start]); ctx.change && ctx.change({ path: path.slice() }); },
      focus() { ops.querySelector('.wd-op')?.focus({ preventScroll: true }); },
      destroy() {},
    };
  });
})();
