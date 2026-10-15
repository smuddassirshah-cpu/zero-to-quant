/* sketch widget: the learner drags control points of a curve on a `plane` canvas to match a target function.
   spec: { kind: 'sketch', control: 5, target: 'max(x - 100, 0)', xRange: [80, 120], band: 2, start, snap,
           wrong: [{ id, expr, band }] }
   grade() samples 20 x values evenly across xRange (both ends included) and needs every one within `band`
   (y units) of the target. `key` is the first wrong[] entry the whole curve matches within its band, else null.
   answer() puts every control point on the target curve, for the test hook. */
(function () {
  'use strict';
  const Z = window.ZQ;

  Z.widgets.register('sketch', (host, spec, ctx) => {
    const canvas = ctx.canvas;
    const el = Z.h(`<div class="wd wd-sketch t-caption">${Z.esc(spec.prompt || 'Drag the blue points up or down to shape the curve.')}</div>`);
    host.append(el);
    if (!canvas || typeof canvas.sample !== 'function') {
      el.textContent = 'This sketch needs a plane canvas.';
      return { el, value: () => null, grade: () => ({ ok: false, key: null, detail: null }) };
    }
    const range = spec.xRange || (canvas.params && canvas.params.x) || [-5, 5];
    const band = +(spec.band ?? 1);
    const fn = (expr) => { const f = Z.cvb.fnOf(String(expr), []); return (x) => f(x, {}); };
    const target = fn(spec.target);
    const opts = { control: spec.control || 5, xRange: range, target: spec.target, band, start: spec.start, snap: spec.snap };
    canvas.enable('sketch', opts);
    const off = canvas.on('change', (d) => { if (d && d.type === 'sketch') ctx.change({ points: d.points, phase: d.phase }); });

    const xs = Array.from({ length: 20 }, (_, i) => range[0] + (range[1] - range[0]) * i / 19);
    const errors = (f) => { const ys = canvas.sample(xs); return xs.map((x, i) => ys[i] - f(x)); };
    const points = () => ((canvas.get().sketch || {}).points || []).map((p) => p.slice());
    const unmarkAll = () => { if (canvas.unmark) { canvas.unmark('is-correct'); canvas.unmark('is-notyet'); canvas.unmark('is-reveal'); } };

    return {
      el,
      value: points,
      /* The control points placed on the target curve (the same points reveal() moves to) */
      answer: () => points().map(([x]) => [x, target(x)]),
      set(v) { if (Array.isArray(v) && v.length) canvas.set({ sketch: { points: v.map((p) => p.slice()) } }, { instant: true }); },
      grade() {
        const e = errors(target);
        let worst = 0; e.forEach((v, i) => { if (Math.abs(v) > Math.abs(e[worst])) worst = i; });
        const ok = e.every((v) => Number.isFinite(v) && Math.abs(v) <= band + 1e-9);
        let key = null;
        if (!ok) for (const w of spec.wrong || []) { const ew = errors(fn(w.expr)); if (ew.every((v) => Math.abs(v) <= (w.band ?? band) + 1e-9)) { key = w.id; break; } }
        return { ok, key, detail: { worstX: xs[worst], worstError: e[worst], errors: e } };
      },
      lock() { canvas.lock(true); },
      unlock() { canvas.lock(false); unmarkAll(); canvas.highlight(null, false); },
      markGraded(res) { unmarkAll(); if (res) canvas.mark('sketch', res.ok ? 'is-correct' : 'is-notyet'); },
      reveal() {
        unmarkAll(); canvas.highlight(null, false); canvas.mark('sketch', 'is-reveal');
        const pts = points().map(([x]) => [x, target(x)]);
        return canvas.set({ sketch: { points: pts }, showTarget: true });
      },
      showWhy() {
        const e = errors(target); let worst = 0; e.forEach((v, i) => { if (Math.abs(v) > Math.abs(e[worst])) worst = i; });
        const pts = points(), n = pts.length; if (n < 2) return;
        const h = (range[1] - range[0]) / (n - 1), seg = Math.min(n - 2, Math.max(0, Math.floor((xs[worst] - range[0]) / h)));
        canvas.highlight(['seg' + seg]);
      },
      reset() { unmarkAll(); canvas.highlight(null, false); canvas.set({ showTarget: false }, { instant: true }); canvas.enable('sketch', { ...opts, reset: true }); },
      focus() { const h = canvas.el.querySelector('[data-drag="k0"]'); if (h) h.focus(); },
      destroy() { if (typeof off === 'function') off(); el.remove(); },
    };
  });
})();
