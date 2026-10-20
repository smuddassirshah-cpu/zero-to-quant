/* sliders widget (item 226): two or more sliders graded together, for "find a and b that reach the target".
   spec: { kind: 'sliders', sliders: [{ id, bind, min, max, step, start, label, format, decimals, unitLabel }],
           answer: { a: 2, b: 3 }, tol: 0.05 (or { a: 0.05, b: 0.1 }),
           or check: "a * b" with value: 6 and tol (any pair whose expression is within tol of value) and show: { a, b },
           wrong: [{ id, check: "a > b" }] }
   Each slider drives the canvas as a plain slider does (bind). Key on a miss: the first wrong[] whose check holds,
   else the id of the first slider off its answer (answer form) or "off" (check form). */
(function () {
  'use strict';
  const Z = window.ZQ;

  Z.widgets.register('sliders', (host, spec, ctx) => {
    const list = (spec.sliders || []).map((s, i) => ({ ...s, id: String(s.id || s.bind || 's' + i) }));
    const el = Z.h('<div class="wd wd-sliders"></div>');
    host.append(el);
    let touched = false;
    const kids = list.map((s) => {
      const h = Z.h('<div class="wd-sliders-row"></div>'); el.append(h);
      const { answer, ...plain } = s; // each one is an explore slider; the pair is graded here
      return { s, w: Z.widgets.kinds.slider(h, plain, { ...ctx, change: (d) => { touched = true; ctx.change && ctx.change({ id: s.id, ...d }); } }) };
    });
    const values = () => Object.fromEntries(kids.map(({ s, w }) => [s.id, w.value()]));
    const compiled = {};
    const evalIn = (src, v) => {
      if (!compiled[src]) { try { compiled[src] = Z.canvas.compile(src, Object.keys(v)); } catch { compiled[src] = () => NaN; } }
      return compiled[src](0, v);
    };
    const tolOf = (id) => (spec.tol && typeof spec.tol === 'object' ? +(spec.tol[id] ?? 0) : +(spec.tol || 0));
    const target = () => spec.answer || spec.show || {};
    const results = () => {
      const v = values();
      if (spec.check) { const r = evalIn(spec.check, v), ok = Number.isFinite(r) && Math.abs(r - (+spec.value || 0)) <= (+spec.tol || 0) + 1e-9; return kids.map(({ s }) => ({ id: s.id, ok })); }
      return kids.map(({ s }) => ({ id: s.id, ok: spec.answer && spec.answer[s.id] != null ? Math.abs(v[s.id] - spec.answer[s.id]) <= tolOf(s.id) + 1e-9 : true }));
    };
    return {
      el,
      value: values,
      set(v) { kids.forEach(({ s, w }) => { if (v && v[s.id] != null) w.set(v[s.id]); }); touched = true; ctx.change && ctx.change({ set: true }); },
      answer: () => ({ ...target() }),
      ready: () => touched,
      dirty: () => touched,
      grade() {
        const r = results(), ok = r.every((x) => x.ok), v = values();
        if (ok) return { ok, key: null, detail: { values: v } };
        for (const w of spec.wrong || []) if (w.check && evalIn(w.check, v)) return { ok: false, key: w.id, detail: { values: v } };
        return { ok: false, key: spec.check ? 'off' : r.find((x) => !x.ok).id, detail: { values: v } };
      },
      lock() { kids.forEach(({ w }) => w.lock()); },
      unlock() { kids.forEach(({ w }) => w.unlock()); },
      markGraded(res) { const r = results(); kids.forEach(({ s, w }) => w.markGraded({ ok: !!(res && res.ok) || !!(r.find((x) => x.id === s.id) || {}).ok })); },
      reveal() { const t = target(); return Promise.all(kids.map(({ s, w }) => (t[s.id] != null ? (w.set(t[s.id]), w.el.classList.add('is-reveal')) : null))); },
      reset() { kids.forEach(({ w }) => w.reset()); touched = false; },
      focus() { kids[0] && kids[0].w.focus(); },
      destroy() { kids.forEach(({ w }) => w.destroy && w.destroy()); el.remove(); },
    };
  });
})();
