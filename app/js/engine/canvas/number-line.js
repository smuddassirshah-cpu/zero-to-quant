/* number-line canvas: ticks and labels, points (draggable in drag mode, snapping to `snap` or `step`; tappable in tap
   mode), intervals with open or closed ends, and jump arrows. Ids are the authored point, interval and arrow ids.
   Labels: `labelPos` ("above", "below", "left", "right") on points and intervals; without it a point label moves to
   the side away from any jump arrow that starts or ends there, and labels that would overlap are stacked in tiers.
   `points`, `intervals` and `arrows` accept keyed patches ({ "points": { "p1": { "x": 3 } } }) as well as arrays.
   Params and state: engine/canvas/README.md. */
(function () {
  'use strict';
  const Z = window.ZQ, C = Z.canvas, { svg, attrs, lerp } = C;

  const toFrac = (x, maxDen = 16) => {
    if (Number.isInteger(x)) return String(x);
    for (let d = 2; d <= maxDen; d++) { const n = Math.round(x * d); if (Math.abs(n / d - x) < 1e-9) return `${n}/${d}`; }
    return C.fmtNum(x, 3);
  };

  function numberLine(host, params, ctx = {}) {
    const P = params || {};
    const min = P.min ?? 0, max = P.max ?? 10, step = P.step || 1, snap = P.snap ?? step;
    const W = 540, x0 = 30, x1 = 510, sx = C.scale([min, max], [x0, x1]);
    const fmt = (v) => (P.format === 'fraction' ? toFrac(v) : C.fmtNum(v, 3));
    const fr = C.frame(host, W, 120, { label: P.label || `Number line from ${min} to ${max}` });
    const g = fr.g;
    const axisG = svg('g', { class: 'cv-axis' }), intG = svg('g', { class: 'cv-intervals' }), arrG = svg('g', { class: 'cv-jumps' }), ptG = svg('g', { class: 'cv-points' });
    g.append(axisG, intG, arrG, ptG);
    let axisY = 60, H = 120;

    /* Ticks every step; labels thinned so they never collide */
    const ticks = []; for (let v = min, k = 0; v <= max + 1e-9 && k < 2000; v = +(min + (++k) * step).toFixed(10)) ticks.push(+v.toFixed(10));
    const labelList = Array.isArray(P.labels) ? P.labels.map(l => (typeof l === 'object' ? l : { x: l, text: fmt(l) })) : P.labels === false ? [] : (() => {
      const every = typeof P.labels === 'number' ? P.labels : Math.max(1, Math.ceil(Math.max(30, ...ticks.map(t => C.textW(fmt(t)) + 12)) / ((x1 - x0) / Math.max(1, ticks.length - 1))));
      return ticks.filter((_, i) => i % every === 0).map(t => ({ x: t, text: fmt(t) }));
    })();
    const fracLabels = labelList.some(l => C.texOf(l.text).tex);
    const drawAxis = () => {
      axisG.replaceChildren(
        svg('line', { class: 'cv-axisline', x1: x0 - 14, y1: axisY, x2: x1 + 14, y2: axisY }),
        P.ends === false ? null : svg('path', { class: 'cv-axisend', d: `M${x1 + 8} ${axisY - 5}L${x1 + 15} ${axisY}L${x1 + 8} ${axisY + 5}M${x0 - 8} ${axisY - 5}L${x0 - 15} ${axisY}L${x0 - 8} ${axisY + 5}` }),
        ...ticks.map(t => svg('line', { class: 'cv-tick', x1: sx(t), x2: sx(t), y1: axisY - 6, y2: axisY + 6 })),
        ...labelList.map(l => C.label(sx(l.x), axisY + (fracLabels ? 28 : 21), l.text, { tex: 'auto', w: 60, h: 36, cls: 'cv-ticklabel' })),
      );
    };

    const pts = new Map(), ints = new Map(), jumps = new Map();
    let dragIds = null; // null: decided per point
    /* A point is a drag handle only when a widget asked for it (enable('drag', { ids })) or the author set drag: true
       (an explore point, movable without a widget). Never in tap mode or a static copy: then it is a plain dot. */
    const isDraggable = (p) => !I.isStatic && I.mode() !== 'tap' && (dragIds ? dragIds.includes(p.id) : p.drag === true);
    const canDrag = () => !I.locked() && (I.mode() === 'drag' || I.mode() == null);
    const ROW = 16; // interval rows stack this far apart

    const mkPoint = (p) => {
      const e = { g: svg('g', { class: 'cv-obj cv-pt', 'data-id': p.id, 'data-tap': '', 'data-label': `Point ${p.label ? C.texOf(p.label).src : p.id}` }), x: p.x };
      e.dot = svg('circle', { class: 'cv-body', r: 6 });
      e.hit = svg('circle', { class: 'cv-hit', r: 22 }); e.disc = svg('circle', { class: 'cv-hl-disc', r: 15 });
      e.knob = svg('circle', { class: 'cv-knob', r: 9 }); e.ring = svg('circle', { class: 'cv-knob-ring', r: 10 });
      e.lab = svg('g', { class: 'cv-ptlabel' });
      e.g.append(e.hit, e.disc, e.dot, e.knob, e.ring, e.lab);
      ptG.append(e.g);
      C.dragger(e.g, fr.svg, {
        start: () => canDrag() && !!e.drag,
        move: (q) => moveTo(p.id, q.x, 'move'),
        end: (q) => moveTo(p.id, q.x, 'end'),
      });
      e.g.addEventListener('keydown', (ev) => {
        if (!canDrag() || !e.drag) return;
        const k = { ArrowRight: 1, ArrowUp: 1, ArrowLeft: -1, ArrowDown: -1 }[ev.key]; if (!k) return;
        ev.preventDefault(); const v = clamp(e.x + k * (snap || step) * (ev.shiftKey ? 10 : 1));
        setX(p.id, v); I.emit('change', { id: p.id, x: v, y: 0, phase: 'end' });
      });
      return e;
    };
    const clamp = (v) => Math.min(max, Math.max(min, snap ? +(Math.round((v - min) / snap) * snap + min).toFixed(10) : v));
    const setX = (id, v) => {
      const e = pts.get(id); e.x = v; paintPoint(e);
      I.setQuiet({ points: (I.state().points || []).map(q => (q.id === id ? { ...q, x: v } : q)) });
    };
    const moveTo = (id, px, phase) => { const v = clamp(sx.invert(px)); if (v !== pts.get(id).x || phase === 'end') { setX(id, v); I.emit('change', { id, x: v, y: 0, phase }); } };
    const paintPoint = (e) => attrs(e.g, { transform: `translate(${sx(e.x)} ${axisY})` });

    /* Label layout, from the target positions: side per label, then tiers so no two labels overlap. Offsets are from
       the point (or from the interval's bar) in px; above-band labels share one row and stack upwards by 18px. */
    const near = (a, b) => Math.abs(a - b) < 1e-9;
    const setSlot = (el, k) => { for (let i = 1; i <= 6; i++) el.classList.toggle('cv-k' + i, i === k); };
    const rowOf = (iv, k) => (Number.isInteger(iv.row) && iv.row >= 0 ? iv.row : k); // row 0 sits on the axis
    const estW = (t) => { const x = C.texOf(t); return x.tex ? Math.min(80, C.textW(x.src.replace(/\\[a-zA-Z]+|[{}^_]/g, ''), 13) + 14) : C.textW(String(x.src), 13, 600) + 10; };
    const layout = (P2, I2, A2) => {
      const pt = {}, iv = {}, boxes = [];
      const place = (b) => {
        const hits = (o) => b.band === o.band && b.x0 < o.x1 + 4 && o.x0 < b.x1 + 4 && Math.abs(b.y - o.y) < 16;
        let guard = 0;
        while (boxes.some(hits) && guard++ < 8) b.y += b.band === 'below' ? 18 : -18;
        boxes.push(b); return b.y;
      };
      A2.forEach(a => { if (!a.label) return; const xa = sx(a.from), xb = sx(a.to), h = Math.max(20, Math.min(48, Math.abs(xb - xa) * 0.35)), w = estW(a.label); boxes.push({ band: 'above', x0: (xa + xb) / 2 - w / 2, x1: (xa + xb) / 2 + w / 2, y: -8 - h - 10 }); });
      const items = [];
      P2.forEach(p => {
        if (!p.label) return;
        let side = p.labelPos;
        if (!side) {
          const busy = new Set();
          A2.forEach(a => { if (near(a.from, p.x)) busy.add(a.to >= a.from ? 'right' : 'left'); if (near(a.to, p.x)) busy.add(a.from <= a.to ? 'left' : 'right'); });
          side = !busy.size ? 'above' : busy.size === 2 ? 'below' : busy.has('right') ? 'left' : 'right';
        }
        const x = sx(Math.min(max, Math.max(min, p.x))), w = estW(p.label);
        const b = side === 'left' ? { x0: x - 9 - w, x1: x - 9, y: -15, anchor: 'end', dx: -9 } : side === 'right' ? { x0: x + 9, x1: x + 9 + w, y: -15, anchor: 'start', dx: 9 } : { x0: x - w / 2, x1: x + w / 2, y: side === 'below' ? 0 : -22, anchor: 'middle', dx: 0 };
        items.push({ kind: 'pt', id: p.id, band: side === 'below' ? 'below' : 'above', ...b });
      });
      I2.forEach((it, k) => {
        if (!it.label) return;
        const side = it.labelPos || 'above';
        const fa = it.from == null || it.from === '-inf' ? x0 - 12 : sx(it.from), fb = it.to == null || it.to === 'inf' ? x1 + 12 : sx(it.to), w = estW(it.label);
        if (side === 'left' || side === 'right') { iv[it.id] = { side, dy: 0 }; return; }
        const mid = (fa + fb) / 2;
        const row = rowOf(it, k);
        items.push({ kind: 'iv', id: it.id, side, band: side === 'below' ? 'below' : 'above', x0: mid - w / 2, x1: mid + w / 2, y: side === 'below' ? 0 : -14 - ROW * row, base: side === 'below' ? 0 : -14 - ROW * row });
      });
      let up = 0, down = 0;
      items.sort((a, b) => a.x0 - b.x0).forEach(b => {
        const y0 = b.y, y = place(b);
        if (b.band === 'above') up = Math.max(up, y0 - y); else down = Math.max(down, 22 + y);
        if (b.kind === 'pt') pt[b.id] = { dx: b.dx, dy: y, anchor: b.anchor, below: b.band === 'below' };
        else iv[b.id] = { side: b.side, dy: y - y0 };
      });
      return { pt, iv, up, down };
    };
    let lay = { pt: {}, iv: {}, up: 0, down: 0 };
    const belowY = () => (fracLabels ? 48 : 36) + 6; // under the tick labels

    const draw = (st, prev, { instant, ms }) => {
      const P2 = st.points || [], I2 = st.intervals || [], A2 = st.arrows || [];
      lay = layout(P2, I2, A2);
      const anyLabel = P2.some(p => p.label && !(lay.pt[p.id] && lay.pt[p.id].below));
      const top = 10 + (A2.length ? 66 : 0) + (anyLabel ? 22 + lay.up : 0) + ROW * Math.max(0, ...I2.map((iv, k) => rowOf(iv, k)));
      const nextAxis = top + 12; H = nextAxis + (fracLabels ? 48 : 36) + lay.down;
      if (nextAxis !== axisY || H !== fr.h) { axisY = nextAxis; fr.resize(W, H); drawAxis(); }
      if (!axisG.childNodes.length) drawAxis();

      /* intervals: thick series bars, row 0 on the axis, later rows stacked above */
      const seenI = new Set();
      I2.forEach((iv, k) => {
        seenI.add(iv.id);
        let e = ints.get(iv.id);
        if (!e) {
          e = { g: svg('g', { class: 'cv-obj cv-int cv-k' + Math.min(6, (iv.colour || k + 1)), 'data-id': iv.id }), bar: svg('line', { class: 'cv-body' }), a: svg('circle', { class: 'cv-end', r: 5 }), b: svg('circle', { class: 'cv-end', r: 5 }), lab: svg('g'), from: iv.from, to: iv.to };
          e.g.append(e.bar, e.a, e.b, e.lab); intG.append(e.g); ints.set(iv.id, e); e.fresh = true;
        }
        e.row = rowOf(iv, k); e.spec = iv;
        setSlot(e.g, Math.min(6, Math.max(1, iv.colour || k + 1))); // colour: a series slot 1 to 6, patchable
      });
      for (const [id, e] of ints) if (!seenI.has(id)) { e.g.remove(); ints.delete(id); }

      /* jumps: arcs over the axis with an arrowhead and a label at the apex */
      const seenA = new Set();
      A2.forEach((a) => {
        seenA.add(a.id || `${a.from}-${a.to}`);
        const id = a.id || `${a.from}-${a.to}`;
        let e = jumps.get(id);
        if (!e) { e = { g: svg('g', { class: 'cv-obj cv-jump', 'data-id': id }), path: svg('path', { class: 'cv-arc' }), head: svg('path', { class: 'cv-head' }), lab: svg('g'), fresh: true }; e.g.append(e.path, e.head, e.lab); arrG.append(e.g); jumps.set(id, e); }
        e.spec = a;
      });
      for (const [id, e] of jumps) if (!seenA.has(id)) { e.g.remove(); jumps.delete(id); }

      /* points */
      const seenP = new Set();
      P2.forEach((p, k) => {
        seenP.add(p.id);
        let e = pts.get(p.id); if (!e) { e = mkPoint(p); e.fresh = true; }
        pts.set(p.id, e);
        e.from = e.fresh ? p.x : e.x; e.to = p.x; e.spec = p;
        e.drag = isDraggable(p);
        e.g.classList.toggle('cv-handle', e.drag);
        setSlot(e.g, p.colour ? Math.min(6, Math.max(1, +p.colour)) : 0);
        const L = lay.pt[p.id];
        e.lab.replaceChildren(p.label && L ? C.label(L.dx, L.below ? belowY() + L.dy : L.dy, p.label, { tex: 'auto', cls: 'cv-halo', w: 80, h: 30, anchor: L.anchor }) : '');
        if (e.drag && I.mode() === 'drag' && !I.isStatic) { e.g.setAttribute('tabindex', '0'); e.g.setAttribute('role', 'slider'); e.g.setAttribute('aria-label', p.label || p.id); e.g.setAttribute('aria-valuenow', p.x); }
        else ['tabindex', 'role', 'aria-label', 'aria-valuenow'].forEach(a => e.g.removeAttribute(a));
      });
      for (const [id, e] of pts) if (!seenP.has(id)) { e.g.remove(); pts.delete(id); }

      const frame = (t) => {
        for (const e of pts.values()) { e.x = lerp(e.from, e.to, t); paintPoint(e); }
        for (const e of ints.values()) {
          const iv = e.spec, y = axisY - ROW * e.row;
          const f0 = e.fresh ? iv.from : e.from, t0 = e.fresh ? iv.to : e.to;
          const fa = iv.from == null || iv.from === '-inf' ? x0 - 12 : sx(lerp(f0 ?? min, iv.from, t)), fb = iv.to == null || iv.to === 'inf' ? x1 + 12 : sx(lerp(t0 ?? max, iv.to, t));
          attrs(e.bar, { x1: fa, x2: fb, y1: y, y2: y });
          const open = iv.open || [false, false];
          attrs(e.a, { cx: fa, cy: y, class: 'cv-end' + (open[0] ? ' open' : '') }); e.a.style.display = iv.from == null || iv.from === '-inf' ? 'none' : '';
          attrs(e.b, { cx: fb, cy: y, class: 'cv-end' + (open[1] ? ' open' : '') }); e.b.style.display = iv.to == null || iv.to === 'inf' ? 'none' : '';
          if (t === 1) { e.from = iv.from; e.to = iv.to; e.fresh = false; }
          const L = lay.iv[iv.id] || { side: 'above', dy: 0 };
          /* beside a ray's open end there is no room: the label sits above the bar at the drawing's edge instead */
          const rayL = iv.from == null || iv.from === '-inf', rayR = iv.to == null || iv.to === 'inf';
          e.lab.replaceChildren(!iv.label ? '' : L.side === 'left' ? (rayL ? C.label(4, y - 14, iv.label, { tex: 'auto', cls: 'cv-halo', w: 80, h: 28, anchor: 'start' }) : C.label(fa - 10, y, iv.label, { tex: 'auto', cls: 'cv-halo', w: 80, h: 28, anchor: 'end' }))
            : L.side === 'right' ? (rayR ? C.label(W - 4, y - 14, iv.label, { tex: 'auto', cls: 'cv-halo', w: 80, h: 28, anchor: 'end' }) : C.label(fb + 10, y, iv.label, { tex: 'auto', cls: 'cv-halo', w: 80, h: 28, anchor: 'start' }))
            : L.side === 'below' ? C.label((fa + fb) / 2, axisY + belowY() + L.dy, iv.label, { tex: 'auto', cls: 'cv-halo', w: 80, h: 28 })
            : C.label((fa + fb) / 2, y - 14 + L.dy, iv.label, { tex: 'auto', cls: 'cv-halo', w: 80, h: 28 }));
        }
        for (const e of jumps.values()) {
          const a = e.spec, xa = sx(a.from), xb = sx(a.to), h = Math.max(20, Math.min(48, Math.abs(xb - xa) * 0.35)), y = axisY - 8;
          const cy = y - h * 4 / 3, d = `M${xa} ${y}C${xa} ${cy} ${xb} ${cy} ${xb} ${y - 1}`;
          attrs(e.path, { d });
          const dir = Math.sign(xb - xa) || 1;
          attrs(e.head, { d: `M${xb - 4.5} ${y - 8}L${xb} ${y}L${xb + 4.5} ${y - 8}`.replace(/NaN/g, '0') });
          e.head.setAttribute('transform', `rotate(${dir * -12} ${xb} ${y})`);
          e.lab.replaceChildren(a.label ? C.label((xa + xb) / 2, y - h - 10, a.label, { tex: 'auto', cls: 'cv-halo', w: 80, h: 28 }) : '');
          if (e.fresh && !instant) { const L = e.path.getTotalLength ? e.path.getTotalLength() : 200; e.path.style.strokeDasharray = L; e.path.style.strokeDashoffset = L * (1 - t); e.head.style.opacity = t > 0.9 ? 1 : 0; if (t === 1) { e.path.style.strokeDasharray = ''; e.path.style.strokeDashoffset = ''; e.fresh = false; } }
          else { e.head.style.opacity = 1; e.fresh = false; }
        }
        if (t === 1) for (const e of pts.values()) e.fresh = false;
      };
      if (instant) { anim.stop(); frame(1); } else anim.run(ms, frame);
    };
    const anim = C.animator();
    const I = C.instance({
      kind: 'number-line', factory: numberLine, params, ctx, fr, draw,
      onEnable: (mode, opts) => { dragIds = mode === 'drag' && opts.ids ? opts.ids : null; I.api.set({}, { instant: true }); },
    });
    const api = I.api;
    /* Keyed list patches: { points: { p1: { x: 3 } } } changes p1 (and adds an id not yet listed) */
    const rawSet = api.set;
    const isMap = (v) => v && typeof v === 'object' && !Array.isArray(v);
    api.set = (patch, o) => {
      if (patch && ['points', 'intervals', 'arrows'].some(k => isMap(patch[k]))) {
        patch = { ...patch };
        ['points', 'intervals', 'arrows'].forEach(k => {
          if (!isMap(patch[k])) return;
          const cur = I.state()[k] || [], map = patch[k];
          patch[k] = cur.map(q => (map[q.id] ? { ...q, ...map[q.id] } : q)).concat(Object.entries(map).filter(([id]) => !cur.some(q => q.id === id)).map(([id, v]) => ({ id, ...v })));
        });
      }
      return rawSet(patch, o);
    };
    api.getParam = (name) => { const q = (I.state().points || []).find(p => p.id === name); return q ? q.x : (I.state().params || {})[name]; };
    api.points = () => Object.fromEntries((I.state().points || []).map(p => [p.id, { x: p.x, y: 0 }]));
    api.place = (id, pos, { instant = false } = {}) => api.set({ points: (I.state().points || []).map(p => (p.id === id ? { ...p, x: typeof pos === 'number' ? pos : pos[0] } : p)) }, { instant });
    /* item 134: a name that is no point is a free parameter in state.params, for a derive block to read */
    api.setParam = api.param = (name, v) => { if ((I.state().points || []).some(p => p.id === name)) api.place(name, v, { instant: true }); else api.set({ params: { [name]: +v } }, { instant: true }); };
    api.set({}, { instant: true });
    return api;
  }

  C.register('number-line', numberLine);
})();
