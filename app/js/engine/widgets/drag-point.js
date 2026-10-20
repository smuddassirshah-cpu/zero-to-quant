/* drag-point widget (docs/AUTHORING.md 3, design-research 5.3 no. 6): the learner drags points on the screen's canvas
   (ctx.canvas.enable('drag', { ids })). Works with any canvas that emits drag events; it reads positions through
   canvas.points() when present (else state.points) and moves points through canvas.place(id, pos) (else a state patch).
   A target is [x, y] on 2D canvases, or one number on 1D ones (number-line x, circle angle).
   grade: every point within its tol (default 0.25) of its target; key = the id of the first wrong[] region holding a
   point ({ x: [a, b], y: [c, d] } or { angle: [a, b] }), else the first point that is off target.
   markGraded rings each point green or amber; reveal animates the points to their targets in hint indigo.
   Plane extras: `tol: [dx, dy]` is a per-axis tolerance, `tolX` checks x alone, and a target `{ "on": "f", "x": 12.3 }`
   is the point of function f at that x (graded on x alone, for dragging along a steep curve). Item 254: { "line": [[x1, y1],
   [x2, y2]] } and { "expr": "2*x + y", "value": 0 } accept a whole line or level set; `show` is the reveal position. */
(function () {
  'use strict';
  const Z = window.ZQ;

  Z.widgets.register('drag-point', (host, spec, ctx) => {
    const cv = ctx.canvas;
    const el = Z.h('<div class="wd-drag"><p class="t-caption wd-drag-msg" hidden></p></div>');
    host.append(el);
    const msg = el.querySelector('.wd-drag-msg');
    const pts = spec.points || [];
    if (!cv || typeof cv.enable !== 'function') {
      msg.hidden = false; msg.textContent = 'This task needs its diagram, which could not be drawn.';
      return { el, value: () => ({}), grade: () => ({ ok: false, key: null, detail: null }) };
    }
    const ids = pts.map(p => p.id);
    cv.enable('drag', { ids });
    const oneD = (p) => typeof p.target === 'number';
    const obj = (p) => p.target && typeof p.target === 'object' && !Array.isArray(p.target);
    const onF = (p) => obj(p) && p.target.on != null;
    /* item 254: a line target { line: [[x1, y1], [x2, y2]] } accepts any point within tol of the line; an expression target
       { expr: "2*x + y", value: 0 } any point where the expression is within tol of value. `show: [x, y]` is where
       Show solution puts the point (a line defaults to its first point). */
    const lineT = (p) => obj(p) && Array.isArray(p.target.line);
    const exprT = (p) => obj(p) && typeof p.target.expr === 'string';
    const exprFn = (p) => { if (!p._f) { try { const c = Z.canvas.compile(p.target.expr, ['y']); p._f = (x, y) => c(x, { y }); } catch { p._f = () => NaN; } } return p._f; };
    /* the [x, y] a target means: { on, x } reads y from the canvas's function */
    const tgtOf = (p) => (onF(p) ? [+p.target.x, cv.evaluate ? cv.evaluate(p.target.on, +p.target.x) : 0] : lineT(p) || exprT(p) ? (p.target.show || (lineT(p) ? p.target.line[0] : [0, 0])) : p.target);
    const lineDist = (p, v) => { const [[a, b], [c, d]] = p.target.line, dx = c - a, dy = d - b, L = Math.hypot(dx, dy) || 1; return Math.abs((v[0] - a) * dy - (v[1] - b) * dx) / L; };
    const raw = (id) => {
      if (cv.points) return (cv.points() || {})[id] || null;
      const q = ((cv.get() || {}).points || []).find(p => p.id === id); return q ? { x: q.x, y: q.y } : null;
    };
    const valueOf = (p) => { const r = raw(p.id); if (!r) return null; return oneD(p) ? (r.angle ?? r.x) : [r.x, r.y ?? 0]; };
    const place = (id, pos, o = {}) => {
      if (cv.place) return cv.place(id, pos, o);
      const st = cv.get() || {}, [x, y] = typeof pos === 'number' ? [pos, 0] : pos;
      cv.set({ points: (st.points || []).map(p => (p.id === id ? { ...p, x, y } : p)) }, o);
    };
    const start = Object.fromEntries(pts.map(p => [p.id, valueOf(p)]));
    let moved = false;
    cv.on('change', (e) => { if (e && ids.includes(e.id)) { if (e.phase === 'end') moved = true; ctx.change && ctx.change({ id: e.id, phase: e.phase }); } });

    const dist = (p, v) => (v == null ? Infinity : oneD(p) ? Math.abs(v - p.target) : lineT(p) ? lineDist(p, v) : exprT(p) ? Math.abs(exprFn(p)(v[0], v[1]) - (+p.target.value || 0)) : Math.hypot(v[0] - tgtOf(p)[0], v[1] - tgtOf(p)[1]));
    const near = (p, v) => {
      if (v == null) return false;
      if (oneD(p)) return Math.abs(v - p.target) <= (p.tol ?? 0.25) + 1e-9;
      if (lineT(p) || exprT(p)) { const d0 = dist(p, v); return Number.isFinite(d0) && d0 <= (typeof p.tol === 'number' ? p.tol : 0.25) + 1e-9; }
      const t = tgtOf(p), dx = Math.abs(v[0] - t[0]), dy = Math.abs(v[1] - t[1]);
      if (Array.isArray(p.tol)) return dx <= p.tol[0] + 1e-9 && dy <= p.tol[1] + 1e-9;
      if (p.tolX != null) return dx <= p.tolX + 1e-9;
      if (onF(p)) return dx <= (p.tol ?? 0.25) + 1e-9;
      return Math.hypot(dx, dy) <= (p.tol ?? 0.25) + 1e-9;
    };
    const inRegion = (r, v, p) => {
      if (v == null || !r) return false;
      const x = oneD(p) ? v : v[0], y = oneD(p) ? null : v[1];
      if (r.angle && !(x >= r.angle[0] && x <= r.angle[1])) return false;
      if (r.x && !(x >= r.x[0] && x <= r.x[1])) return false;
      if (r.y && (y == null || !(y >= r.y[0] && y <= r.y[1]))) return false;
      return true;
    };
    const mark = (list, cls) => { if (!list.length) return; if (cv.mark) cv.mark(list, cls); else list.forEach(id => cv.el.querySelectorAll(`[data-id="${CSS.escape(id)}"]`).forEach(n => n.classList.add(cls))); };
    const unmark = () => { if (cv.unmark) cv.unmark(); else cv.el.querySelectorAll('.is-correct, .is-notyet, .is-reveal').forEach(n => n.classList.remove('is-correct', 'is-notyet', 'is-reveal')); };
    const results = () => pts.map(p => ({ id: p.id, v: valueOf(p), ok: near(p, valueOf(p)), dist: dist(p, valueOf(p)) }));

    return {
      el,
      value: () => Object.fromEntries(pts.map(p => [p.id, valueOf(p)])),
      set(v) { for (const [id, pos] of Object.entries(v || {})) if (ids.includes(id) && pos != null) place(id, pos, { instant: true }); moved = true; ctx.change && ctx.change({ set: true }); },
      answer: () => Object.fromEntries(pts.map(p => [p.id, tgtOf(p)])),
      ready: () => moved,
      dirty: () => moved,
      grade() {
        const r = results(), ok = r.every(x => x.ok);
        if (ok) return { ok, key: null, detail: r };
        for (const w of spec.wrong || []) for (const p of pts) if (inRegion(w.region, valueOf(p), p)) return { ok: false, key: w.id, detail: r };
        return { ok: false, key: r.find(x => !x.ok).id, detail: r };
      },
      lock() { cv.lock && cv.lock(true); },
      unlock() { cv.lock && cv.lock(false); unmark(); },
      markGraded() { unmark(); const r = results(); mark(r.filter(x => x.ok).map(x => x.id), 'is-correct'); mark(r.filter(x => !x.ok).map(x => x.id), 'is-notyet'); },
      reveal() { unmark(); pts.forEach(p => place(p.id, tgtOf(p))); mark(ids, 'is-reveal'); cv.lock && cv.lock(true); },
      showWhy(key) {
        const w = (spec.wrong || []).find(x => x.id === key);
        if (!w || !w.canvas) return false;
        cv.set(w.canvas); return true;
      },
      reset() { unmark(); cv.lock && cv.lock(false); pts.forEach(p => { if (start[p.id] != null) place(p.id, start[p.id], { instant: true }); }); moved = false; },
      focus() { const n = cv.el.querySelector('.cv-handle[tabindex="0"]'); if (n) n.focus({ preventScroll: true }); },
      destroy() { if (cv.enable) cv.enable(null); },
    };
  });
})();
