/* Canvases B (E4). This file holds two things:
   1. ZQ.cvb, the small kit every Canvases B kind builds on (instance lifecycle, state tweening,
      highlight, graded-class preservation, drag and tap plumbing, axes, labels). Kinds read it
      lazily inside their factories, so script order between B files does not matter.
   2. The `plane` canvas: coordinate plane with functions, points, segments, tangents, areas,
      Riemann rectangles, vectors and the sketch mode. Contract: docs/AUTHORING.md section 4,
      details per kind in canvas/README-B.md. */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  const isObj = (v) => v != null && typeof v === 'object' && !Array.isArray(v);
  const deep = (v) => (v == null ? v : structuredClone(v));
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const snapTo = (v, s) => (s ? Math.round(v / s) * s : v);
  const round = (v, dp = 6) => +(+v).toFixed(dp);

  /* Interpolate two states. Numbers tween, arrays of equal length and objects tween member-wise,
     arrays of objects with ids are matched by id; anything else jumps to the target. */
  const lerp = (a, b, t, skip) => {
    if (t >= 1) return b;
    if (typeof a === 'number' && typeof b === 'number' && Number.isFinite(a) && Number.isFinite(b)) return a + (b - a) * t;
    if (Array.isArray(a) && Array.isArray(b)) {
      if (b.length && isObj(b[0]) && 'id' in b[0]) return b.map((v) => { const o = a.find((x) => isObj(x) && x.id === v.id); return o ? lerp(o, v, t, skip) : v; });
      if (a.length === b.length) return b.map((v, i) => lerp(a[i], v, t, skip));
      return b;
    }
    if (isObj(a) && isObj(b)) {
      const o = {};
      for (const k of Object.keys(b)) o[k] = (skip && skip.includes(k)) || !(k in a) ? b[k] : lerp(a[k], b[k], t, skip);
      return o;
    }
    return b;
  };

  /* Numbers: British grouping, true minus sign, trailing zeros trimmed. */
  const fmt = (v, dp = 3) => {
    if (v == null || !Number.isFinite(+v)) return '';
    let n = +(+v).toFixed(dp); if (Object.is(n, -0)) n = 0;
    const s = Math.abs(n) >= 1000 ? Math.abs(n).toLocaleString('en-GB', { maximumFractionDigits: dp }) : C.fmtNum(Math.abs(n), dp);
    return (n < 0 ? '−' : '') + s;
  };
  const stepDp = (step) => { const s = String(+step.toFixed(10)); const i = s.indexOf('.'); return i < 0 ? 0 : s.length - i - 1; };
  const fmtTick = (v, step) => {
    const dp = stepDp(step); let n = +v.toFixed(dp); if (Object.is(n, -0)) n = 0;
    const s = Math.abs(n).toLocaleString('en-GB', { minimumFractionDigits: dp, maximumFractionDigits: dp, useGrouping: Math.abs(n) >= 10000 });
    return (n < 0 ? '−' : '') + s;
  };
  /* Approximate text width at a font size (Archivo is narrow; 0.56em per glyph is a safe overestimate). */
  const tw = (s, size = 13) => String(s).replace(/\$|\\[a-z]+/gi, '').length * size * 0.56;

  /* Ticks that never collide: start from the pixel budget and drop the count until labels fit. */
  const ticksFor = (min, max, px, { minGap = 46, fmtF } = {}) => {
    let n = Math.max(2, Math.floor(px / minGap));
    for (; n >= 2; n--) {
      const t = C.niceTicks(min, max, n); if (t.length < 2) return { ticks: t, step: (max - min) || 1 };
      const step = t[1] - t[0]; const labels = t.map((v) => (fmtF ? fmtF(v, step) : fmtTick(v, step)));
      const each = px / ((max - min) / step); const widest = Math.max(...labels.map((l) => tw(l, 12)));
      if (each >= widest + 10 || n === 2) return { ticks: t, step, labels };
    }
    return { ticks: [min, max], step: max - min };
  };

  /* Text. Plain strings become <text>; '$...$' alone is KaTeX through ZQ.canvas.label; mixed text and maths go through ZQ.md. */
  const txt = (x, y, s, o = {}) => svg('text', {
    x, y, 'text-anchor': o.anchor || 'middle', 'dominant-baseline': o.baseline || 'central',
    class: 'cvb-t' + (o.cls ? ' ' + o.cls : '') + (o.halo ? ' cvb-halo' : ''),
    style: `font-size:${o.size || 13}px` + (o.weight ? `;font-weight:${o.weight}` : ''),
  }, [String(s)]);
  const lab = (x, y, s, o = {}) => {
    s = String(s ?? '');
    if (!s.includes('$')) return txt(x, y, s, o);
    const w = o.w || Math.max(40, tw(s) + 40), h = o.h || 26, anchor = o.anchor || 'middle';
    const m = s.match(/^\$([^$]+)\$$/);
    if (m) {
      const fo = C.label(x, y, m[1], { anchor, tex: true, w, h, cls: 'cvb-fo' + (o.cls ? ' ' + o.cls : '') + (o.halo ? ' cvb-fo-halo' : '') });
      return fo;
    }
    const fo = svg('foreignObject', { x: anchor === 'middle' ? x - w / 2 : anchor === 'end' ? x - w : x, y: y - h / 2, width: w, height: h, class: 'cv-fo cvb-fo' + (o.cls ? ' ' + o.cls : '') + (o.halo ? ' cvb-fo-halo' : '') });
    const d = document.createElement('div'); d.className = 'cv-fo-in'; d.style.textAlign = anchor === 'middle' ? 'center' : anchor === 'end' ? 'right' : 'left';
    d.style.justifyContent = anchor === 'middle' ? 'center' : anchor === 'end' ? 'flex-end' : 'flex-start';
    d.innerHTML = `<span>${Z.md(s)}</span>`; fo.append(d); return fo; // one inline run: a flex box would drop the spaces around the maths
  };

  /* An id-bearing object: <g class="cv-obj" data-id=..> with a colour class setting --c for its marks. */
  const COLOUR = { 1: 'cvb-c1', 2: 'cvb-c2', 3: 'cvb-c3', 4: 'cvb-c4', 5: 'cvb-c5', 6: 'cvb-c6', ink: 'cvb-ci', manip: 'cvb-cm', hint: 'cvb-ch', neg: 'cvb-cneg', pos: 'cvb-cpos', muted: 'cvb-cmu' };
  const colourCls = (c) => COLOUR[c] || (typeof c === 'string' && c.startsWith('cvb-') ? c : COLOUR.ink);
  const obj = (id, cls = '', colour) => svg('g', { class: 'cv-obj ' + (colour != null ? colourCls(colour) + ' ' : '') + cls, 'data-id': id });
  /* Highlight wash shapes: hidden until the group carries .cv-hl. */
  const washRect = (x, y, w, h, r = 4) => svg('rect', { x, y, width: Math.max(0, w), height: Math.max(0, h), rx: r, class: 'cvb-hlw' });
  const washPath = (d) => svg('path', { d, class: 'cvb-hlw ln' });
  const washCircle = (cx, cy, r) => svg('circle', { cx, cy, r, class: 'cvb-hlw' });

  /* Arrow from (x1,y1) to (x2,y2) with a filled head; the shaft stops at the head's base. */
  const arrow = (x1, y1, x2, y2, { cls = 'cvb-ln', head = 9, width = 0.55 } = {}) => {
    const dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L, hh = Math.min(head, L * 0.6);
    const bx = x2 - ux * hh, by = y2 - uy * hh, wx = -uy * hh * width, wy = ux * hh * width;
    return svg('g', {}, [
      svg('line', { x1, y1, x2: bx + ux * 0.5, y2: by + uy * 0.5, class: cls }),
      svg('path', { d: `M${x2},${y2}L${bx + wx},${by + wy}L${bx - wx},${by - wy}Z`, class: 'cvb-head' }),
    ]);
  };

  /* Movable handle: manipulable blue, 2px white ring, 1px ink outline, 44px hit area. */
  const handle = (x, y, dragId, { r = 8, label: aria = 'Movable point', shape = 'circle' } = {}) => {
    const g = svg('g', { class: 'cvb-handle', 'data-drag': dragId, tabindex: 0, role: 'slider', 'aria-label': aria });
    g.append(svg('circle', { cx: x, cy: y, r: 22, class: 'cvb-hit' }));
    if (shape === 'diamond') {
      const k = r + 1.5;
      g.append(svg('path', { d: `M${x},${y - k - 2}L${x + k},${y}L${x},${y + k + 2}L${x - k},${y}Z`, class: 'cvb-hd-o' }),
        svg('path', { d: `M${x},${y - k}L${x + k - 2},${y}L${x},${y + k}L${x - k + 2},${y}Z`, class: 'cvb-hd' }));
    } else {
      g.append(svg('circle', { cx: x, cy: y, r: r + 3, class: 'cvb-hd-o' }), svg('circle', { cx: x, cy: y, r, class: 'cvb-hd' }));
    }
    return g;
  };

  /* Spread labels vertically so none overlap: items [{y, h}] mutated in place, kept within [lo, hi]. */
  const spread = (items, gap = 15, lo = -Infinity, hi = Infinity) => {
    const s = items.slice().sort((a, b) => a.y - b.y);
    for (let i = 1; i < s.length; i++) if (s[i].y - s[i - 1].y < gap) s[i].y = s[i - 1].y + gap;
    if (s.length && s[s.length - 1].y > hi) { s[s.length - 1].y = hi; for (let i = s.length - 2; i >= 0; i--) if (s[i + 1].y - s[i].y < gap) s[i].y = s[i + 1].y - gap; }
    if (s.length && s[0].y < lo) { s[0].y = lo; for (let i = 1; i < s.length; i++) if (s[i].y - s[i - 1].y < gap) s[i].y = s[i - 1].y + gap; }
    return items;
  };

  /* Place labels without overlapping each other or fixed boxes. labels: [{ x, y, text, anchor }] (mutated: y moves);
     fixed: [{ x0, y0, x1, y1 }]; bounds: { x0, y0, x1, y1 } keeps labels inside the plot. */
  const boxOf = (l) => { const w = (l.w || tw(l.text)) + 4, h = l.h || 16, a = l.anchor || 'middle'; const x0 = a === 'start' ? l.x - 2 : a === 'end' ? l.x - w + 2 : l.x - w / 2; return { x0, x1: x0 + w, y0: l.y - h / 2, y1: l.y + h / 2 }; };
  const hit = (a, b) => a.x0 < b.x1 && b.x0 < a.x1 && a.y0 < b.y1 && b.y0 < a.y1;
  /* Small boxes along a drawn line (pixel points [[x, y]]), as obstacles so labels keep clear of the line */
  const lineBoxes = (pts, every = 10, pad = 3) => { const out = []; let last = null; for (const [x, y] of pts) { if (!Number.isFinite(y)) { last = null; continue; } if (last && Math.hypot(x - last[0], y - last[1]) < every) continue; out.push({ x0: x - pad, x1: x + pad, y0: y - pad, y1: y + pad }); last = [x, y]; } return out; };
  const placeLabels = (labels, fixed = [], bounds) => {
    const placed = fixed.slice();
    for (const l of labels) {
      const y0 = l.y; let best = null;
      if (bounds) { const w = (l.w || tw(l.text)) + 4; if (l.anchor === 'start') l.x = Math.min(l.x, bounds.x1 - w); else if (l.anchor === 'end') l.x = Math.max(l.x, bounds.x0 + w); else l.x = clamp(l.x, bounds.x0 + w / 2, bounds.x1 - w / 2); }
      for (const dy of (l.side === 1 ? [0, 16, -16, 32, -32, 48, -48, 64, -64] : [0, -16, 16, -32, 32, -48, 48, -64, 64])) { // side 1: try below first
        l.y = y0 + dy;
        const b = boxOf(l);
        if (bounds && (b.y0 < bounds.y0 || b.y1 > bounds.y1)) continue;
        if (!placed.some((q) => hit(b, q))) { best = l.y; break; }
      }
      l.y = best ?? clamp(y0, bounds ? bounds.y0 + 8 : -Infinity, bounds ? bounds.y1 - 8 : Infinity); placed.push(boxOf(l));
    }
    return labels;
  };

  /* Chart axes (left and bottom, horizontal gridlines). Returns the tick info used. */
  const chartAxes = (g, sx, sy, o = {}) => {
    const [x0, x1] = sx.range, [y0, y1] = sy.range; // y0 bottom pixel, y1 top pixel
    const yt = o.yTicks || (sy.log ? logTicks(sy.domain[0], sy.domain[1], Math.abs(y0 - y1), { minGap: 24 }) : ticksFor(sy.domain[0], sy.domain[1], Math.abs(y0 - y1), { minGap: 30, fmtF: o.fmtY }));
    const gg = svg('g', { class: 'cvb-axes' });
    for (const v of yt.ticks) {
      const y = sy(v); if (y < y1 - 0.5 || y > y0 + 0.5) continue;
      if (o.grid !== false) gg.append(svg('line', { x1: x0, x2: x1, y1: y, y2: y, class: 'cvb-grid' }));
      const st = yt.log ? Math.pow(10, Math.floor(Math.log10(v))) : yt.step;
      gg.append(txt(x0 - 7, y, o.fmtY ? o.fmtY(v, st) : fmtTick(v, st), { anchor: 'end', cls: 'cvb-tick', size: 12 }));
    }
    if (!o.noX) {
      const xt = o.xTicks || ticksFor(sx.domain[0], sx.domain[1], Math.abs(x1 - x0), { minGap: 48, fmtF: o.fmtX });
      for (const v of xt.ticks) {
        const x = sx(v); if (x < x0 - 0.5 || x > x1 + 0.5) continue;
        gg.append(svg('line', { x1: x, x2: x, y1: y0, y2: y0 + 4, class: 'cvb-axis thin' }));
        gg.append(txt(x, y0 + 15, o.fmtX ? o.fmtX(v, xt.step) : fmtTick(v, xt.step), { cls: 'cvb-tick', size: 12 }));
      }
    }
    const base = o.baseline != null && o.baseline >= sy.domain[0] && o.baseline <= sy.domain[1] ? sy(o.baseline) : y0;
    gg.append(svg('line', { x1: x0, x2: x0, y1: y0, y2: y1, class: 'cvb-axis' }));
    gg.append(svg('line', { x1: x0, x2: x1, y1: base, y2: base, class: 'cvb-axis' }));
    if (o.yLabel) gg.append(lab(x0 - 6, y1 - 16, o.yLabel, { anchor: 'start', cls: 'cvb-axlab' }));
    if (o.xLabel) gg.append(lab(x1, y0 + 33, o.xLabel, { anchor: 'end', cls: 'cvb-axlab' }));
    g.append(gg);
    return yt;
  };
  /* Left margin a chart needs for its y tick labels. */
  const yMargin = (min, max, px, fmtY, log = false) => {
    const t = log ? logTicks(min, max, px, { minGap: 24 }) : ticksFor(min, max, px, { minGap: 30, fmtF: fmtY });
    return 14 + Math.max(...t.ticks.map((v) => tw(fmtY ? fmtY(v, t.step) : fmtTick(v, t.step), 12)));
  };

  /* Log scale (yScale: "log"): positive values only; ticks at 1, 2 and 5 times powers of ten that fit, thinned to minGap px */
  const logScale = (domain, range) => {
    const [d0, d1] = domain.map((v) => Math.log(Math.max(1e-12, v))), [r0, r1] = range, k = (r1 - r0) / ((d1 - d0) || 1);
    const f = (v) => (v > 0 ? r0 + (Math.log(v) - d0) * k : NaN);
    f.invert = (p) => Math.exp(d0 + (p - r0) / k); f.domain = domain; f.range = range; f.log = true; return f;
  };
  const logTicks = (lo, hi, px, { minGap = 30 } = {}) => {
    const all = [];
    for (let e = Math.floor(Math.log10(lo)) - 1; e <= Math.ceil(Math.log10(hi)); e++) [1, 2, 5].forEach((m) => { const v = +(m * Math.pow(10, e)).toPrecision(12); if (v >= lo * (1 - 1e-9) && v <= hi * (1 + 1e-9)) all.push(v); });
    const perPx = px / (Math.log(hi / lo) || 1);
    let ticks = all, keep = [1, 2, 5];
    const gapOk = (list) => list.every((v, i) => i === 0 || (Math.log(v / list[i - 1]) * perPx) >= minGap);
    if (!gapOk(ticks)) { keep = [1, 5]; ticks = all.filter((v) => keep.includes(+String(v.toExponential()).split('e')[0][0])); }
    if (!gapOk(ticks)) ticks = all.filter((v) => /^1/.test(v.toExponential()));
    if (!ticks.length) ticks = [lo, hi];
    return { ticks, step: Math.pow(10, Math.floor(Math.log10(Math.min(...ticks)))), log: true };
  };

  /* Plane axes through the origin (or along the edges), arrowheads at the positive ends. */
  const planeAxes = (g, sx, sy, o = {}) => {
    const [px0, px1] = sx.range, [py0, py1] = sy.range; // py0 bottom
    const xt = ticksFor(sx.domain[0], sx.domain[1], px1 - px0, { minGap: 40 });
    const yt = sy.log ? logTicks(sy.domain[0], sy.domain[1], py0 - py1, { minGap: 26 }) : ticksFor(sy.domain[0], sy.domain[1], py0 - py1, { minGap: 34 });
    const ax = !sy.log && sy.domain[0] <= 0 && sy.domain[1] >= 0 ? sy(0) : py0; // x axis pixel y
    const ay = sx.domain[0] <= 0 && sx.domain[1] >= 0 ? sx(0) : px0; // y axis pixel x
    const gg = svg('g', { class: 'cvb-axes' });
    if (o.grid !== false) {
      const gx = typeof o.grid === 'number' ? C.niceTicks(sx.domain[0], sx.domain[1], Math.round((sx.domain[1] - sx.domain[0]) / o.grid)) : xt.ticks;
      const gy = typeof o.grid === 'number' && !sy.log ? C.niceTicks(sy.domain[0], sy.domain[1], Math.round((sy.domain[1] - sy.domain[0]) / o.grid)) : yt.ticks;
      for (const v of gx) gg.append(svg('line', { x1: sx(v), x2: sx(v), y1: py0, y2: py1, class: 'cvb-grid' }));
      for (const v of gy) gg.append(svg('line', { x1: px0, x2: px1, y1: sy(v), y2: sy(v), class: 'cvb-grid' }));
    }
    gg.append(arrow(px0, ax, px1 + 6, ax, { cls: 'cvb-axis', head: 8 }));
    gg.append(arrow(ay, py0, ay, py1 - 6, { cls: 'cvb-axis', head: 8 }));
    const below = ax + 14 > py0 + 18 ? ax - 12 : ax + 14;
    const origin = !sy.log && sx.domain[0] <= 0 && sx.domain[1] >= 0 && sy.domain[0] <= 0 && sy.domain[1] >= 0, yAt0 = origin, xAt0 = origin;
    const boxes = [];
    for (const v of xt.ticks) {
      const x = sx(v); if ((yAt0 && Math.abs(x - ay) < 2) || x > px1 - 14) continue;
      gg.append(svg('line', { x1: x, x2: x, y1: ax - 3, y2: ax + 3, class: 'cvb-axis thin' }));
      const t = fmtTick(v, xt.step);
      gg.append(txt(x, below, t, { cls: 'cvb-tick', size: 12, halo: true }));
      boxes.push(boxOf({ x, y: below, text: t, h: 14 }));
    }
    for (const v of yt.ticks) {
      const y = sy(v); if ((xAt0 && Math.abs(y - ax) < 2) || y < py1 + 12) continue;
      gg.append(svg('line', { x1: ay - 3, x2: ay + 3, y1: y, y2: y, class: 'cvb-axis thin' }));
      const t = o.fmtY ? o.fmtY(v, yt.step) : fmtTick(v, yt.log ? Math.pow(10, Math.floor(Math.log10(v))) : yt.step);
      gg.append(txt(ay - 7, y, t, { anchor: 'end', cls: 'cvb-tick', size: 12, halo: true }));
      boxes.push(boxOf({ x: ay - 7, y, text: t, anchor: 'end', h: 14 }));
    }
    if (origin && sx.domain[0] < 0 && sy.domain[0] < 0) gg.append(txt(ay - 7, ax + 12, '0', { anchor: 'end', cls: 'cvb-tick', size: 12, halo: true }));
    const xl = o.xLabel ?? '$x$', yl = o.yLabel ?? '$y$';
    gg.append(lab(px1 + 2, ax - 14, xl, { anchor: 'end', cls: 'cvb-axlab', halo: true }));
    gg.append(lab(ay + 10, py1 - 2, yl, { anchor: 'start', cls: 'cvb-axlab', halo: true }));
    boxes.push(boxOf({ x: px1 + 2, y: ax - 14, text: xl, anchor: 'end', h: 20 }), boxOf({ x: ay + 10, y: py1 - 2, text: yl, anchor: 'start', h: 20 }));
    g.append(gg);
    return { xt, yt, ax, ay, boxes };
  };

  /* ---------- Instance lifecycle shared by every Canvases B kind ----------
     Honours the shared contract in canvas/_base.js (E3): mark/unmark, flash/unflash, lock, tap selection with
     { selected, id, on }, drag payloads { id, x, y, phase }, points()/place() on drag kinds, ctx.static clones.
     Drawing is a pure function of state: set() tweens a copy of the state and redraws every frame. */
  const GRADED = ['is-correct', 'is-notyet', 'is-reveal', 'is-dim'];
  const KEEP = [...GRADED, 'is-flash'];
  let uidN = 0;
  const make = (host, params, ctx = {}, def) => {
    const uid = 'cvb' + (++uidN);
    const size = def.size ? def.size(params) : { w: 540, h: 320 };
    const F = C.frame(host, size.w, size.h, { cls: 'cvb cv-' + def.kind, label: def.aria || def.kind });
    F.svg.classList.add('cvb-svg');
    const defs = svg('defs'); F.svg.insertBefore(defs, F.g);
    const extra = document.createElement('div'); extra.className = 'cvb-extra'; F.wrap.insertBefore(extra, F.svg.nextSibling);
    const em = C.emitter();
    let state = deep(def.init ? def.init(params) : {});
    let shown = state, gen = 0, mode = null, modeOpts = {}, locked = false, destroyed = false, lastTap = null;
    const isStatic = !!ctx.static;
    if (isStatic) F.wrap.classList.add('cv-static', 'cvb-static');
    const hl = new Set(), marks = new Map();
    const modes = def.modes || [];

    const R = {
      uid, F, params, ctx, defs, extra, svg, emit: (d) => em.emit('change', d),
      get state() { return state; }, get shown() { return shown; }, get mode() { return mode; }, get modeOpts() { return modeOpts; },
      /* Input allowed: not a clone, not locked, and (no mode asked for, or the current mode is one of m). */
      active: (m) => !isStatic && !locked && (m == null || mode === m || (Array.isArray(m) && m.includes(mode))),
      get static() { return isStatic; }, get locked() { return locked; },
      clipRect(x, y, w, h, key = 'plot') {
        const id = uid + '-' + key; let cp = defs.querySelector('#' + id);
        if (!cp) { cp = svg('clipPath', { id }, [svg('rect')]); defs.append(cp); }
        C.attrs(cp.firstChild, { x, y, width: Math.max(0, w), height: Math.max(0, h) });
        return `url(#${id})`;
      },
      commit(patch, opts = { instant: true }) { return inst.set(patch, opts); },
      redraw() { draw(shown); },
      /* Tap target: the id-bearing group itself takes data-tap so selection, marks and focus share one element. */
      tappable(el, id, aria) { if (mode === 'tap' && !isStatic && (!modeOpts.only || modeOpts.only.includes(id))) { el.dataset.tap = id; if (aria) el.dataset.label = aria; } return el; },
    };

    const all = (id) => [...F.g.querySelectorAll(`[data-id="${CSS.escape(String(id))}"]`)];
    const find = (id) => (def.alias ? def.alias(String(id), R) : [String(id)]).flatMap(all);
    const applyMarks = () => {
      F.g.querySelectorAll('.cv-badge').forEach((n) => n.remove());
      for (const [cls, ids] of marks) for (const id of ids) all(id).forEach((n) => { if (!n.classList.contains('cv-obj')) return; n.classList.add(cls); if (cls === 'is-notyet' && C.badge && !isStatic && def.badges !== false) C.badge(n, 'cross'); });
    };
    const applyTap = () => {
      const sel = new Set(state.selected || []);
      const items = [...F.g.querySelectorAll('[data-tap]')];
      items.forEach((n) => {
        const on = sel.has(n.dataset.tap); n.classList.toggle('is-on', on);
        n.setAttribute('role', 'button'); n.setAttribute('tabindex', '-1'); n.setAttribute('aria-pressed', String(on));
        if (n.dataset.label) n.setAttribute('aria-label', n.dataset.label);
      });
      if (items.length) (items.find((n) => n.dataset.tap === lastTap) || items[0]).setAttribute('tabindex', '0');
    };

    const draw = (view) => {
      if (destroyed) return;
      const keep = new Map();
      F.g.querySelectorAll('[data-id]').forEach((el) => { const k = KEEP.filter((c) => el.classList.contains(c)); if (k.length) keep.set(el.dataset.id, k); });
      const act = F.svg.contains(document.activeElement) ? document.activeElement : null;
      const focused = act ? (act.dataset.drag ? '[data-drag="' + CSS.escape(act.dataset.drag) + '"]' : act.dataset.tap ? '[data-tap="' + CSS.escape(act.dataset.tap) + '"]' : null) : null;
      F.g.replaceChildren();
      def.render(view, R);
      for (const [id, cls] of keep) all(id).forEach((el) => el.classList.add(...cls));
      applyMarks();
      const ids = new Set([...(def.hlIds ? def.hlIds(view, R) : (Array.isArray(view.highlight) ? view.highlight.map(String) : [])), ...hl]);
      for (const id of ids) find(id).forEach((el) => el.classList.add('cv-hl'));
      if (mode === 'tap') applyTap();
      if (focused) { const el = F.g.querySelector(focused); if (el) el.focus({ preventScroll: true }); }
    };

    /* Pointer and keyboard plumbing for drag handles ([data-drag]) and tap targets ([data-tap]). */
    const toView = (e) => C.toLocal(F.svg, e.clientX, e.clientY);
    let dragging = null;
    const onDown = (e) => {
      if (!def.drag || (e.pointerType === 'mouse' && e.button !== 0) || isStatic || locked) return;
      const t = e.target.closest('[data-drag]'); if (!t || !F.svg.contains(t)) return;
      const info = def.drag.start(t.dataset.drag, toView(e), R); if (!info) return;
      e.preventDefault(); dragging = info; try { F.svg.setPointerCapture(e.pointerId); } catch { /* no capture for this pointer */ }
      F.wrap.classList.add('cvb-dragging');
    };
    const onMove = (e) => { if (!dragging) return; e.preventDefault(); def.drag.move(dragging, toView(e), R, false); };
    const onUp = (e) => {
      if (!dragging) return; const d = dragging; dragging = null; F.wrap.classList.remove('cvb-dragging');
      try { F.svg.releasePointerCapture(e.pointerId); } catch { /* already released */ }
      def.drag.move(d, toView(e), R, true);
    };
    const tapToggle = (id) => {
      let sel = (state.selected || []).slice(); const i = sel.indexOf(id);
      if (i >= 0) sel.splice(i, 1);
      else if (modeOpts.max === 1) sel = [id];
      else if (modeOpts.max && sel.length >= modeOpts.max) return;
      else sel.push(id);
      lastTap = id;
      state = { ...state, selected: sel }; shown = { ...shown, selected: sel }; draw(shown);
      if (Z.sound) Z.sound('tap');
      em.emit('change', { type: 'tap', selected: sel.slice(), id, on: i < 0 });
    };
    const onKey = (e) => {
      const t = e.target;
      if (!t.dataset) return;
      if (t.dataset.drag && def.drag && def.drag.key && !locked && !isStatic) {
        const k = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, 1], ArrowDown: [0, -1] }[e.key];
        if (k) { e.preventDefault(); def.drag.key(t.dataset.drag, k[0] * (e.shiftKey ? 10 : 1), k[1] * (e.shiftKey ? 10 : 1), R); }
        return;
      }
      if (t.dataset.tap && mode === 'tap') {
        if (e.key === ' ' || e.key === 'Spacebar') { e.preventDefault(); if (!locked) tapToggle(t.dataset.tap); return; }
        if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
          e.preventDefault(); const items = [...F.g.querySelectorAll('[data-tap]')], n = C.nextInDirection(items, t, e.key);
          if (n) { items.forEach((x) => x.setAttribute('tabindex', '-1')); n.setAttribute('tabindex', '0'); lastTap = n.dataset.tap; n.focus(); }
        }
      }
    };
    const onClick = (e) => {
      if (mode !== 'tap' || locked || isStatic) return;
      const t = e.target.closest('[data-tap]'); if (t && F.svg.contains(t)) tapToggle(t.dataset.tap);
    };
    F.svg.addEventListener('pointerdown', onDown);
    F.svg.addEventListener('pointermove', onMove);
    F.svg.addEventListener('pointerup', onUp);
    F.svg.addEventListener('pointercancel', onUp);
    F.svg.addEventListener('keydown', onKey);
    F.svg.addEventListener('click', onClick);

    const inst = {
      el: F.wrap,
      kind: def.kind,
      params,
      set(patch = {}, opts = {}) {
        if (destroyed || patch == null) return Promise.resolve();
        patch = { ...patch };
        if (def.prepare) patch = def.prepare(patch, state, R) || patch;
        for (const k of def.listKeys || []) {
          if (isObj(patch[k]) && Array.isArray(state[k])) patch[k] = state[k].map((it) => (isObj(it) && it.id in patch[k] ? { ...it, ...patch[k][it.id] } : it));
        }
        const prev = state;
        state = C.merge(state, patch);
        if ('highlight' in patch) hl.clear();
        if ('caption' in patch) F.caption(patch.caption || '');
        const instant = !!opts.instant || Z.reducedMotion() || isStatic;
        const my = ++gen;
        let p;
        if (def.animate) p = Promise.resolve(def.animate(prev, state, { instant, alive: () => my === gen && !destroyed, show: (v) => { if (my === gen && !destroyed) { shown = v; draw(v); } }, patch }, R));
        else if (instant) { shown = state; draw(state); p = Promise.resolve(); }
        else {
          const from = shown, to = state, ms = opts.ms || (def.ms ? def.ms(from, to) : 600);
          p = C.tween(0, 1, ms, (t) => { if (my !== gen || destroyed) return; shown = t >= 1 ? to : lerp(from, to, t, def.skip); draw(shown); });
        }
        if ('highlight' in patch && !instant) {
          const ids = def.hlIds ? def.hlIds(state, R) : (Array.isArray(state.highlight) ? state.highlight.map(String) : []);
          ids.flatMap(find).forEach((el) => C.pulse(el));
        }
        return p;
      },
      get: () => deep(state),
      highlight(ids, on = true) {
        ids = ids == null ? [] : [].concat(ids).map(String);
        if (!on) {
          if (!ids.length) { hl.clear(); C.clearHighlight(F.g); if (state.highlight) state = { ...state, highlight: [] }; shown = { ...shown, highlight: [] }; return inst; }
          ids.forEach((id) => { hl.delete(id); find(id).forEach((el) => el.classList.remove('cv-hl', 'cv-hl-on')); });
          if (Array.isArray(state.highlight)) { state = { ...state, highlight: state.highlight.filter((h) => !ids.includes(String(h))) }; shown = { ...shown, highlight: state.highlight }; }
          return inst;
        }
        ids.forEach((id) => { hl.add(id); find(id).forEach((el) => (isStatic ? el.classList.add('cv-hl') : C.pulse(el))); });
        return inst;
      },
      flash(ids, opts) { const els = [].concat(ids || []).flatMap(find).filter((n) => n.classList.contains('cv-obj')); return C.flash(els, opts); },
      unflash() { F.g.querySelectorAll('.is-flash').forEach((n) => n.classList.remove('is-flash')); },
      mark(ids, cls, on = true) {
        if (!marks.has(cls)) marks.set(cls, new Set());
        [].concat(ids || []).forEach((id) => { if (on) marks.get(cls).add(String(id)); else { marks.get(cls).delete(String(id)); all(id).forEach((n) => n.classList.remove(cls)); } });
        applyMarks(); return inst;
      },
      unmark(cls) {
        const list = cls ? [cls] : GRADED;
        list.forEach((c) => { marks.delete(c); F.g.querySelectorAll('.' + c).forEach((n) => n.classList.remove(c)); });
        if (!cls) F.g.querySelectorAll('.cv-badge').forEach((n) => n.remove());
        applyMarks(); return inst;
      },
      marks: () => Object.fromEntries([...marks].map(([k, v]) => [k, [...v]])),
      lock(on = true) { locked = !!on; F.wrap.classList.toggle('cv-locked', locked); draw(shown); return inst; },
      clone(host2) {
        const c = C.create(host2, { kind: def.kind, params: deep(params), state: deep(state) }, { ...ctx, static: true });
        if (c && c.mark) for (const [cls, ids] of marks) c.mark([...ids], cls);
        return c;
      },
      on: (ev, fn) => em.on(ev, fn),
      enable(m, opts) {
        if (isStatic) return inst;
        const off = m === false || m == null || m === 'none';
        if (!off && !modes.includes(m)) { console.warn(`Canvas "${def.kind}" has no "${m}" mode`); return inst; }
        mode = off ? null : m; modeOpts = opts || {};
        F.wrap.classList.toggle('cv-tap', mode === 'tap'); F.wrap.classList.toggle('cv-drag', mode === 'drag');
        F.wrap.classList.toggle('cvb-int', !!mode);
        if (mode && def.onEnable) def.onEnable(mode, modeOpts, R);
        draw(shown);
        return inst;
      },
      caption: (t) => F.caption(t || ''),
      destroy() {
        destroyed = true; gen++;
        F.svg.removeEventListener('pointerdown', onDown); F.svg.removeEventListener('pointermove', onMove);
        F.svg.removeEventListener('pointerup', onUp); F.svg.removeEventListener('pointercancel', onUp);
        F.svg.removeEventListener('keydown', onKey); F.svg.removeEventListener('click', onClick);
        if (def.destroy) def.destroy(R);
        F.wrap.remove();
      },
    };
    R.inst = inst;
    if (def.methods) Object.assign(inst, def.methods(R, inst));
    if (state.caption) F.caption(state.caption);
    draw(state);
    return inst;
  };

  /* Normalise effective params: base params overlaid with numeric state.params. */
  const eff = (params, view) => ({ ...params, ...(isObj(view.params) ? view.params : {}) });

  /* Small numerics */
  const lgamma = (z) => {
    if (z < 0.5) return Math.log(Math.PI / Math.abs(Math.sin(Math.PI * z))) - lgamma(1 - z);
    const g = 7, c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
    z -= 1; let x = c[0]; for (let i = 1; i < g + 2; i++) x += c[i] / (z + i);
    const t = z + g + 0.5; return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
  };
  const erf = (x) => { // Abramowitz and Stegun 7.1.26 refined with one Newton-free series switch near 0
    const s = Math.sign(x); x = Math.abs(x);
    if (x < 0.5) { let sum = 0, term = x, n = 0; while (Math.abs(term) > 1e-15 && n < 60) { sum += term / (2 * n + 1); n++; term *= -x * x / n; } return s * 2 / Math.sqrt(Math.PI) * sum; }
    const t = 1 / (1 + 0.5 * x);
    const y = 1 - t * Math.exp(-x * x - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))));
    return s * y;
  };
  const simpson = (f, a, b, n = 400) => {
    if (!(b > a)) return 0; if (n % 2) n++; const h = (b - a) / n; let s = f(a) + f(b);
    for (let i = 1; i < n; i++) { const v = f(a + i * h); s += (Number.isFinite(v) ? v : 0) * (i % 2 ? 4 : 2); }
    return s * h / 3;
  };
  /* Standard normal draw from a uniform rng (Box-Muller), local so canvases need only ZQ.sim.rng. */
  const gauss = (rng) => { let u = 0; while (u <= 1e-12) u = rng(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * rng()); };
  /* Seeded rng: ZQ.sim.rng when present, else a local mulberry32 so a canvas never fails to draw. */
  const rngFor = (seed) => {
    if (Z.sim && typeof Z.sim.rng === 'function') return Z.sim.rng(seed);
    let a = (seed >>> 0) || 1;
    return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  };

  const compiled = new Map();
  const fnOf = (expr, names) => { const k = expr + '|' + names.join(','); if (!compiled.has(k)) { try { compiled.set(k, C.compile(expr, names)); } catch (e) { console.warn(e.message); compiled.set(k, () => NaN); } } return compiled.get(k); };

  /* Path through sampled pixel points, broken at NaN, asymptotes and jumps. pts: [[px, py|NaN]] */
  const brokenPath = (pts, H, top, bottom) => {
    const mid = (top + bottom) / 2, far = (bottom - top);
    let d = '', pen = false;
    const dy = (i) => (i >= 0 && i + 1 < pts.length && Number.isFinite(pts[i][1]) && Number.isFinite(pts[i + 1][1]) ? Math.abs(pts[i + 1][1] - pts[i][1]) : 0);
    for (let i = 0; i < pts.length; i++) {
      const [x, y] = pts[i];
      if (!Number.isFinite(y)) { pen = false; continue; }
      const yc = clamp(y, top - far * 2, bottom + far * 2);
      if (pen) {
        const py = pts[i - 1][1], j = dy(i - 1);
        const opposite = (py - mid) * (y - mid) < 0 && j > far;
        const outBoth = (py < top - far && y < top - far) || (py > bottom + far && y > bottom + far);
        const spike = j > 10 && j > 12 * Math.max(dy(i - 2), dy(i), 0.6);
        if (opposite || spike) pen = false;
        else if (outBoth) { pen = false; d += `M${x.toFixed(2)},${yc.toFixed(2)}`; pen = true; continue; }
      }
      d += (pen ? 'L' : 'M') + x.toFixed(2) + ',' + yc.toFixed(2); pen = true;
    }
    return d;
  };

  Z.cvb = { isObj, deep, clamp, snapTo, round, lerp, fmt, fmtTick, tw, ticksFor, txt, lab, obj, colourCls, washRect, washPath, washCircle, arrow, handle, spread, chartAxes, yMargin, planeAxes, make, eff, placeLabels, boxOf, lineBoxes, logScale, logTicks, lgamma, erf, simpson, gauss, rngFor, fnOf, brokenPath };
})();

/* ===== plane ===== */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  const W = 540;
  const sizeOf = (p) => {
    const [x0, x1] = p.x || [-5, 5], [y0, y1] = p.y || [-5, 5];
    if (p.height) return { w: W, h: p.height };
    if (p.equal) return { w: W, h: Math.round(Math.max(220, Math.min(540, (W - 28) * (y1 - y0) / (x1 - x0) + 28))) };
    return { w: W, h: 360 };
  };

  /* Uniform Catmull-Rom through points with evenly spaced x, as a function of x. */
  const crY = (pts, x) => {
    const n = pts.length; if (!n) return NaN; if (n === 1) return pts[0][1];
    const x0 = pts[0][0], xn = pts[n - 1][0], h = (xn - x0) / (n - 1);
    if (x <= x0) return pts[0][1]; if (x >= xn) return pts[n - 1][1];
    const i = Math.min(n - 2, Math.floor((x - x0) / h)), t = (x - pts[i][0]) / h;
    const y = (k) => (k < 0 ? 2 * pts[0][1] - pts[1][1] : k >= n ? 2 * pts[n - 1][1] - pts[n - 2][1] : pts[k][1]);
    const p0 = y(i - 1), p1 = y(i), p2 = y(i + 1), p3 = y(i + 2);
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t * t * t);
  };

  C.register('plane', (host, params, ctx) => {
    const K = Z.cvb;
    let xr = params.x || [-5, 5], yr = params.y || [-5, 5];
    const size = sizeOf(params);
    /* equal: true with a height: keep the height and widen the x or y range about its centre so units stay square */
    if (params.equal && params.height) {
      const pw = size.w - 28, ph = size.h - 28, k = pw / ph, sx0 = xr[1] - xr[0], sy0 = yr[1] - yr[0];
      if (sx0 / sy0 < k) { const c = (xr[0] + xr[1]) / 2, h = sy0 * k / 2; xr = [c - h, c + h]; }
      else { const c = (yr[0] + yr[1]) / 2, h = sx0 / k / 2; yr = [c - h, c + h]; }
    }
    const exprParams = (view) => ({ ...(params.params || {}), ...(view.params || {}) });

    const geom = (R) => {
      const xLabelRoom = yr[0] > 0 || yr[1] < 0 ? 22 : 0, yLabelRoom = xr[0] >= 0 || xr[1] <= 0 ? 34 : 0;
      const m = { l: 14 + yLabelRoom, r: 18, t: 18, b: 14 + xLabelRoom };
      /* yScale: "log" (positive y range): log-price charts; ticks at 1, 2, 5 times powers of ten, labelled as prices with yFormat */
      return { m, sx: C.scale(xr, [m.l, size.w - m.r]), sy: params.yScale === 'log' ? K.logScale([Math.max(1e-9, yr[0]), yr[1]], [size.h - m.b, m.t]) : C.scale(yr, [size.h - m.b, m.t]) };
    };
    const functionsOf = (view) => {
      const list = (params.functions || []).map((f, i) => ({ ...f, slot: f.colour || i + 1 }));
      for (const f of view.functions || []) {
        const j = list.findIndex((g) => g.id === f.id);
        if (j >= 0) list[j] = { ...list[j], ...f }; else list.push({ ...f, slot: f.colour || list.length + 1 });
      }
      const hide = new Set(view.hide || []);
      return list.filter((f) => !hide.has(f.id));
    };
    const evaluator = (view) => {
      const P = exprParams(view), names = Object.keys(P);
      const fns = {};
      for (const f of functionsOf(view)) { const c = K.fnOf(f.expr, names); fns[f.id] = (x) => c(x, P); fns[f.id].def = f; }
      return fns;
    };
    const pointXY = (view, ref) => {
      if (Array.isArray(ref)) return ref;
      const p = (view.points || []).find((q) => q.id === ref); return p ? [p.x, p.y] : [0, 0];
    };
    const deriv = (f, x) => { const h = Math.max(1e-6, (xr[1] - xr[0]) * 1e-5); return (f(x + h) - f(x - h)) / (2 * h); };
    /* One-sided slopes, to find a corner (a piecewise-linear function at its join) */
    const sides = (f, x) => { const h = Math.max(1e-6, (xr[1] - xr[0]) * 1e-5); return [(f(x) - f(x - h)) / h, (f(x + h) - f(x)) / h]; };

    const def = {
      kind: 'plane', aria: params.aria || 'Coordinate plane',
      modes: ['drag', 'slider', 'sketch', 'tap'],
      size: () => size,
      listKeys: ['points', 'vectors', 'segments', 'polygons', 'angles', 'vlines', 'hlines'],
      init: () => ({ points: [], segments: [], vectors: [], params: { ...(params.params || {}) }, highlight: [], showTarget: false }),
      render(view, R) {
        const { m, sx, sy } = geom(R);
        const g = R.F.g, fns = evaluator(view);
        const px0 = m.l, px1 = size.w - m.r, py0 = size.h - m.b, py1 = m.t;
        /* axes: false draws no axes, ticks or grid (a geometry figure) */
        const fmtYp = params.yFormat === 'money' || params.money ? (v, st) => (v < 0 ? '−' : '') + (params.money || '£') + K.fmtTick(Math.abs(v), st) : null;
        const axInfo = params.axes === false ? { boxes: [] } : K.planeAxes(g, sx, sy, { grid: params.grid ?? true, xLabel: params.xLabel, yLabel: params.yLabel, fmtY: fmtYp });
        const fixed = axInfo.boxes.slice();
        if (params.axes !== false) { const ax = !sy.log && yr[0] <= 0 && yr[1] >= 0 ? sy(0) : py0, ay = xr[0] <= 0 && xr[1] >= 0 ? sx(0) : px0; fixed.push({ x0: px0, x1: px1, y0: ax - 2, y1: ax + 2 }, { x0: ay - 2, x1: ay + 2, y0: py1, y1: py0 }); }
        const clip = R.clipRect(px0, py1 - 2, px1 - px0, py0 - py1 + 4);
        const plot = svg('g', { 'clip-path': clip }); g.append(plot);
        const over = svg('g'); g.append(over);
        const labels = [];

        /* Sketch band and target under everything else */
        const sk = view.sketch || {};
        if (sk.target && (view.showTarget || sk.showBand)) {
          const tf = K.fnOf(sk.target, Object.keys(exprParams(view)));
          const P = exprParams(view);
          const xs = []; for (let px = px0; px <= px1; px += 1) xs.push(px);
          if (sk.showBand && sk.band) {
            const up = xs.map((px) => [px, sy(tf(sx.invert(px), P) + sk.band)]), dn = xs.map((px) => [px, sy(tf(sx.invert(px), P) - sk.band)]).reverse();
            plot.append(svg('path', { d: 'M' + up.concat(dn).filter((p) => Number.isFinite(p[1])).map((p) => p[0] + ',' + p[1].toFixed(1)).join('L') + 'Z', class: 'cvb-band' }));
          }
          if (view.showTarget) {
            const o = K.obj('target', '', 'ink');
            const d = K.brokenPath(xs.map((px) => [px, sy(tf(sx.invert(px), P))]), size.h, py1, py0);
            o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln cvb-dash' })); plot.append(o);
          }
        }

        /* Areas and Riemann rectangles */
        for (const a of [].concat(view.area || [])) {
          const f = fns[a.f]; if (!f) continue;
          const gF = a.g ? fns[a.g] : () => 0;
          const lo = Math.max(Math.min(a.from, a.to), xr[0]), hi = Math.min(Math.max(a.from, a.to), xr[1]);
          if (!(hi > lo)) continue;
          const n = Math.max(2, Math.ceil(sx(hi) - sx(lo)));
          const top = [], bot = [];
          for (let i = 0; i <= n; i++) { const x = lo + (hi - lo) * i / n; const y = f(x), y2 = gF(x); if (Number.isFinite(y) && Number.isFinite(y2)) { top.push([sx(x), sy(y)]); bot.push([sx(x), sy(y2)]); } }
          if (!top.length) continue;
          const d = 'M' + top.concat(bot.reverse()).map((p) => p[0].toFixed(2) + ',' + K.clamp(p[1], py1 - 400, py0 + 400).toFixed(2)).join('L') + 'Z';
          const o = K.obj(a.id || 'area', '', a.colour || f.def.slot);
          o.append(svg('path', { d, class: 'cvb-hlw' }), svg('path', { d, class: 'cvb-wash-f' }));
          plot.append(o);
          if (a.label) {
            const val = K.simpson((x) => f(x) - gF(x), lo, hi, 400) * (a.to < a.from ? -1 : 1);
            const text = a.label === 'auto' ? '≈ ' + K.fmt(val, a.dp ?? 3) : String(a.label).replace('{value}', K.fmt(val, a.dp ?? 3));
            const xm = (lo + hi) / 2, ym = (f(xm) + gF(xm)) / 2;
            over.append(K.lab(sx(xm), K.clamp(sy(ym), py1 + 12, py0 - 12), text, { halo: true, cls: 'cvb-strong' }));
          }
        }
        if (view.riemann && fns[view.riemann.f]) {
          const r = view.riemann, f = fns[r.f], n = Math.max(1, Math.round(r.n || 4)), lo = r.from ?? xr[0], hi = r.to ?? xr[1], w = (hi - lo) / n;
          const id = r.id || 'riemann', grp = K.obj(id, '', r.colour || f.def.slot); let sum = 0;
          for (let i = 0; i < n; i++) {
            const a = lo + i * w, b = a + w;
            const rule = r.rule || 'left';
            if (rule === 'trap') {
              const ya = f(a), yb = f(b); sum += (ya + yb) / 2 * w;
              const d = `M${sx(a)},${sy(0)}L${sx(a)},${sy(ya)}L${sx(b)},${sy(yb)}L${sx(b)},${sy(0)}Z`;
              const o = K.obj(`${id}-${i}`, 'cvb-rect'); o.append(svg('path', { d, class: 'cvb-hlw' }), svg('path', { d, class: 'cvb-rect-f' })); grp.append(o);
              continue;
            }
            const xs = rule === 'right' ? b : rule === 'mid' ? (a + b) / 2 : a;
            const y = f(xs); if (!Number.isFinite(y)) continue; sum += y * w;
            const y0p = sy(0), y1p = sy(y), top = Math.min(y0p, y1p), hgt = Math.abs(y1p - y0p);
            const o = K.obj(`${id}-${i}`, 'cvb-rect');
            o.append(K.washRect(sx(a) - 2, top - 2, sx(b) - sx(a) + 4, hgt + 4, 2), svg('rect', { x: sx(a), y: top, width: Math.max(0, sx(b) - sx(a)), height: hgt, class: 'cvb-rect-f' }));
            grp.append(o);
          }
          plot.append(grp);
          if (r.showSum) {
            const t = (r.sumLabel || 'Sum') + ' ≈ ' + K.fmt(sum, r.dp ?? 3), lx = px1 - 4, ly = py1 + 12;
            over.append(K.txt(lx, ly, t, { anchor: 'end', halo: true, cls: 'cvb-strong' })); fixed.push(K.boxOf({ x: lx, y: ly, text: t, anchor: 'end' }));
          }
        }

        /* Functions */
        for (const [id, f] of Object.entries(fns)) {
          const fd = f.def, dom = fd.domain || xr;
          const lo = Math.max(dom[0], xr[0]), hi = Math.min(dom[1], xr[1]); if (!(hi > lo)) continue;
          const a = sx(lo), b = sx(hi), n = Math.max(2, Math.ceil((b - a) * 2));
          const pts = []; for (let i = 0; i <= n; i++) { const px = a + (b - a) * i / n; pts.push([px, sy(f(sx.invert(px)))]); }
          const d = K.brokenPath(pts, size.h, py1, py0);
          fixed.push(...K.lineBoxes(pts.filter((p) => p[1] >= py1 && p[1] <= py0))); // labels keep clear of every curve
          const o = K.obj(id, 'cvb-fn', fd.slot);
          o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln' + (fd.dashed ? ' cvb-dash' : '') }));
          plot.append(o);
          if (fd.endpoints) {
            [[lo, fd.endpoints[0]], [hi, fd.endpoints[1]]].forEach(([x, kind]) => { if (kind && kind !== 'none') { const y = f(x); if (Number.isFinite(y)) over.append(svg('circle', { cx: sx(x), cy: sy(y), r: 4.5, class: 'cvb-end ' + K.colourCls(fd.slot) + (kind === 'open' ? ' open' : '') })); } });
          }
          if (fd.label) {
            let lx = fd.labelAt != null ? fd.labelAt : null, ly;
            if (lx == null) { // last visible sample
              for (let i = pts.length - 4; i >= 0; i--) { const p = pts[i]; if (Number.isFinite(p[1]) && p[1] >= py1 + 6 && p[1] <= py0 - 6) { lx = sx.invert(p[0]); ly = p[1]; break; } }
            } else ly = sy(f(lx));
            /* labelSide "above" (default) or "below" the curve, and labelOffset [dx, dy] in px to nudge it */
            const off = Array.isArray(fd.labelOffset) ? fd.labelOffset : [0, 0];
            if (lx != null && Number.isFinite(ly)) labels.push({ x: sx(lx) + (+off[0] || 0), y: ly + ((fd.labelSide || fd.labelPos) === 'below' ? 16 : -14) + (+off[1] || 0), text: fd.label, id, anchor: fd.labelAnchor === 'start' ? 'start' : fd.labelAnchor === 'middle' ? 'middle' : 'end', side: (fd.labelSide || fd.labelPos) === 'below' ? 1 : -1 });
          }
        }

        /* Tangent lines */
        for (const tg of [].concat(view.tangent || [])) {
          const f = fns[tg.f]; if (!f) continue;
          const x0 = typeof tg.x === 'string' ? pointXY(view, tg.x)[0] : tg.x;
          const y0 = f(x0); let mm = deriv(f, x0); if (!Number.isFinite(y0) || !Number.isFinite(mm)) continue;
          /* at a corner the two one-sided slopes differ: use the side asked for (side: "left" | "right"), else draw none */
          const [sl, sr] = sides(f, x0);
          if (Math.abs(sl - sr) > 1e-3 * Math.max(1, Math.abs(sl), Math.abs(sr))) { if (tg.side === 'left') mm = sl; else if (tg.side === 'right') mm = sr; else continue; }
          /* length in x units, or lengthPx in pixels along the line */
          const pxPerX = Math.hypot(sx(1) - sx(0), mm * (sy(0) - sy(1)));
          const half = tg.lengthPx ? (tg.lengthPx / 2) * Math.sqrt(1 + mm * mm) / (pxPerX || 1) : tg.length ? tg.length / 2 : null;
          const xa = half ? x0 - half / Math.sqrt(1 + mm * mm) : xr[0], xb = half ? x0 + half / Math.sqrt(1 + mm * mm) : xr[1];
          const o = K.obj(tg.id || 'tangent', 'cvb-tangent', tg.colour || 'ink');
          const d = `M${sx(xa)},${sy(y0 + mm * (xa - x0))}L${sx(xb)},${sy(y0 + mm * (xb - x0))}`;
          o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln' + (tg.dashed ? ' cvb-dash' : '') }), svg('circle', { cx: sx(x0), cy: sy(y0), r: 4, class: 'cvb-dot' }));
          plot.append(o);
          if (tg.label) {
            const text = tg.label === 'slope' || tg.label === true ? 'slope ' + K.fmt(mm, tg.dp ?? 2) : String(tg.label).replace('{slope}', K.fmt(mm, tg.dp ?? 2));
            labels.push({ x: sx(x0) + 10, y: sy(y0) + (mm > 0 ? 16 : -16), text, anchor: 'start', id: tg.id || 'tangent' });
          }
        }

        /* Reference lines x = a and y = b: vlines [{ id, x, label, dashed, colour }], hlines [{ id, y, ... }] */
        for (const [list, vert] of [[view.vlines || params.vlines || [], true], [view.hlines || params.hlines || [], false]]) {
          for (const l of list) {
            const v = vert ? l.x : l.y; if (!Number.isFinite(+v)) continue;
            const o = K.obj(l.id || (vert ? 'x' : 'y') + '=' + v, 'cvb-seg', l.colour || 'ink');
            const d = vert ? `M${sx(+v)},${py0}L${sx(+v)},${py1}` : `M${px0},${sy(+v)}L${px1},${sy(+v)}`;
            o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln' + (l.dashed !== false ? ' cvb-dash thin' : '') }));
            plot.append(o);
            if (l.label) labels.push(vert ? { x: sx(+v) + 6, y: py1 + 12, text: l.label, anchor: 'start', id: l.id } : { x: px1 - 4, y: sy(+v) - 10, text: l.label, anchor: 'end', id: l.id });
          }
        }

        /* Polygons: [{ id, points: [[x, y] | pointId, ...], colour, label, vertexLabels: ["A", "B", "C"], dashed }]: a filled
           shape (a series wash) with its vertices labelled outside the shape */
        for (const pg of view.polygons || params.polygons || []) {
          const vs = (pg.points || []).map((q) => pointXY(view, q)).filter((q) => Array.isArray(q) && q.length === 2);
          if (vs.length < 2) continue;
          const o = K.obj(pg.id, 'cvb-poly', pg.colour || 1);
          const d = 'M' + vs.map(([x, y]) => `${sx(x).toFixed(2)},${sy(y).toFixed(2)}`).join('L') + 'Z';
          o.append(K.washPath(d), svg('path', { d, class: 'cvb-poly-f' }), svg('path', { d, class: 'cvb-ln' + (pg.dashed ? ' cvb-dash' : '') }));
          plot.append(o);
          const cxm = vs.reduce((a, q) => a + q[0], 0) / vs.length, cym = vs.reduce((a, q) => a + q[1], 0) / vs.length;
          (pg.vertexLabels || []).forEach((t, k) => {
            if (!t || !vs[k]) return;
            const vx = sx(vs[k][0]), vy = sy(vs[k][1]), dx = vx - sx(cxm), dy = vy - sy(cym), L0 = Math.hypot(dx, dy) || 1;
            labels.push({ x: vx + dx / L0 * 14, y: vy + dy / L0 * 14, text: t, anchor: Math.abs(dx / L0) < 0.35 ? 'middle' : dx > 0 ? 'start' : 'end', id: pg.id + '-v' + k });
          });
          if (pg.label) labels.push({ x: sx(cxm), y: sy(cym), text: pg.label, anchor: 'middle', id: pg.id });
        }
        /* Angle markers: [{ id, at: vertex, from: point, to: point, label, right: true, radius: px }]: an arc (or a square
           for a right angle) between the rays at -> from and at -> to, the smaller angle, labelled on its bisector */
        for (const an of view.angles || params.angles || []) {
          const [ax, ay] = pointXY(view, an.at), [fx, fy] = pointXY(view, an.from), [tx, ty] = pointXY(view, an.to);
          const A = [sx(ax), sy(ay)], a1 = Math.atan2(sy(fy) - A[1], sx(fx) - A[0]), a2 = Math.atan2(sy(ty) - A[1], sx(tx) - A[0]);
          let da = a2 - a1; while (da > Math.PI) da -= 2 * Math.PI; while (da < -Math.PI) da += 2 * Math.PI;
          const r = an.radius || 22, o = K.obj(an.id || 'angle', 'cvb-angle', an.colour || 'ink'), mid = a1 + da / 2;
          let d;
          if (an.right) { const u = [Math.cos(a1), Math.sin(a1)], v = [Math.cos(a2), Math.sin(a2)], k = r * 0.55; d = `M${A[0] + u[0] * k},${A[1] + u[1] * k}L${A[0] + (u[0] + v[0]) * k},${A[1] + (u[1] + v[1]) * k}L${A[0] + v[0] * k},${A[1] + v[1] * k}`; }
          else d = `M${A[0] + r * Math.cos(a1)},${A[1] + r * Math.sin(a1)}A${r} ${r} 0 0 ${da > 0 ? 1 : 0} ${A[0] + r * Math.cos(a2)},${A[1] + r * Math.sin(a2)}`;
          o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln thin' }));
          over.append(o);
          if (an.label) labels.push({ x: A[0] + (r + 12) * Math.cos(mid), y: A[1] + (r + 12) * Math.sin(mid), text: an.label, anchor: 'middle', id: an.id || 'angle' });
        }

        /* Segments */
        for (const s of view.segments || []) {
          const [ax, ay] = pointXY(view, s.from), [bx, by] = pointXY(view, s.to);
          const o = K.obj(s.id, 'cvb-seg', s.colour || 'ink');
          const d = `M${sx(ax)},${sy(ay)}L${sx(bx)},${sy(by)}`;
          o.append(K.washPath(d));
          if (s.arrow) o.append(K.arrow(sx(ax), sy(ay), sx(bx), sy(by), { cls: 'cvb-ln' + (s.dashed ? ' cvb-dash' : '') }));
          else o.append(svg('path', { d, class: 'cvb-ln' + (s.dashed ? ' cvb-dash thin' : '') }));
          plot.append(o);
          /* label at the midpoint, nudged by labelOffset [dx, dy] in px (default 8 right and 10 up) */
          const so = Array.isArray(s.labelOffset) ? s.labelOffset : [8, -10];
          if (s.label) labels.push({ x: (sx(ax) + sx(bx)) / 2 + (+so[0] || 0), y: (sy(ay) + sy(by)) / 2 + (+so[1] || 0), text: s.label, anchor: (+so[0] || 0) < 0 ? 'end' : (+so[0] || 0) === 0 ? 'middle' : 'start', id: s.id });
        }

        /* Vectors */
        for (const [i, v] of (view.vectors || []).entries()) {
          const from = v.from ? pointXY(view, v.from) : [0, 0], to = [from[0] + v.v[0], from[1] + v.v[1]];
          const o = K.obj(v.id, 'cvb-vec', v.colour || i + 1);
          o.append(K.washPath(`M${sx(from[0])},${sy(from[1])}L${sx(to[0])},${sy(to[1])}`), K.arrow(sx(from[0]), sy(from[1]), sx(to[0]), sy(to[1]), { cls: 'cvb-ln' }));
          plot.append(o);
          if (v.label) labels.push({ x: sx(to[0]) + 8, y: sy(to[1]) - 10, text: v.label, anchor: 'start', id: v.id });
        }

        /* Sketch curve and control points */
        if (Array.isArray(sk.points) && sk.points.length > 1) {
          const pts = sk.points;
          const segs = svg('g');
          for (let i = 0; i < pts.length - 1; i++) {
            const o = K.obj('seg' + i, 'cvb-seg-wash');
            o.append(K.washRect(sx(pts[i][0]), py1, sx(pts[i + 1][0]) - sx(pts[i][0]), py0 - py1, 0)); segs.append(o);
          }
          plot.insertBefore(segs, plot.firstChild);
          const a = sx(pts[0][0]), b = sx(pts[pts.length - 1][0]), samples = [];
          for (let px = a; px <= b + 0.01; px += 1.5) samples.push([px, sy(crY(pts, sx.invert(px)))]);
          const d = K.brokenPath(samples, size.h, py1, py0);
          const o = K.obj('sketch', 'cvb-sketch', 'manip');
          o.append(K.washPath(d), svg('path', { d, class: 'cvb-ln bold' }));
          plot.append(o);
          const live = R.active('sketch');
          pts.forEach((p, i) => {
            if (live) over.append(K.handle(sx(p[0]), sy(p[1]), 'k' + i, { r: 7, label: `Control point ${i + 1}` }));
            else over.append(svg('circle', { cx: sx(p[0]), cy: sy(p[1]), r: 3.5, class: 'cvb-dot cvb-cm' }));
          });
        }

        /* Points */
        for (const p of view.points || []) {
          const x = sx(p.x), y = sy(p.y);
          const o = K.obj(p.id, 'cvb-pt', p.drag ? 'manip' : (p.colour || 'ink'));
          o.append(K.washCircle(x, y, p.drag ? 15 : 11));
          if (p.drag && R.active() && (R.mode == null || R.mode === 'drag' || R.mode === 'slider')) o.append(K.handle(x, y, p.id, { label: p.ariaLabel || `Point ${p.label || p.id}` }));
          else if (p.drag) o.append(svg('circle', { cx: x, cy: y, r: 10, class: 'cvb-hd-o' }), svg('circle', { cx: x, cy: y, r: 7, class: 'cvb-hd' }));
          else o.append(svg('circle', { cx: x, cy: y, r: R.mode === 'tap' ? 6 : 4.5, class: 'cvb-dot' + (p.open ? ' open' : '') + (R.mode === 'tap' ? ' cv-body' : '') }));
          if (R.mode === 'tap' && !p.drag) { o.append(svg('circle', { cx: x, cy: y, r: 16, class: 'cvb-tapbox', fill: 'transparent' })); R.tappable(o, p.id, p.ariaLabel || `Point ${p.label || p.id} at (${K.fmt(p.x, 2)}, ${K.fmt(p.y, 2)})`); }
          over.append(o);
          if (p.label) {
            const pos = p.labelPos || 'ne', dx = pos.includes('e') ? 12 : pos.includes('w') ? -12 : 0, dy = pos.includes('n') ? -13 : pos.includes('s') ? 14 : 0;
            labels.push({ x: x + dx, y: y + dy, text: String(p.label).replace('{x}', K.fmt(p.x, 2)).replace('{y}', K.fmt(p.y, 2)), anchor: dx > 0 ? 'start' : dx < 0 ? 'end' : 'middle', id: p.id });
          }
        }

        /* Labels last, placed clear of each other and of the axis labels, inside the plot */
        for (const l of labels) l.anchor = l.anchor || 'end';
        K.placeLabels(labels, fixed, { x0: px0, x1: px1, y0: py1, y1: py0 });
        for (const l of labels) over.append(K.lab(l.x, l.y, l.text, { anchor: l.anchor, halo: true, cls: 'cvb-strong' }));
      },
      drag: {
        start(id, p, R) {
          if (id.startsWith('k') && R.active('sketch')) return { sketch: +id.slice(1) };
          const pt = (R.state.points || []).find((q) => q.id === id);
          return pt && pt.drag && R.active() ? { id } : null;
        },
        move(info, p, R, end) {
          const { sx, sy } = geom(R);
          if (info.sketch != null) {
            const sk = R.state.sketch, pts = sk.points.map((q) => q.slice());
            pts[info.sketch][1] = K.round(K.clamp(K.snapTo(sy.invert(p.y), sk.snap || 0), yr[0], yr[1]), 4);
            R.commit({ sketch: { points: pts } }); R.emit({ type: 'sketch', points: pts, phase: end ? 'end' : 'move' });
            return;
          }
          movePoint(R, info.id, sx.invert(p.x), sy.invert(p.y), end);
        },
        key(id, dx, dy, R) {
          if (id.startsWith('k') && R.state.sketch) {
            const sk = R.state.sketch, i = +id.slice(1), pts = sk.points.map((q) => q.slice());
            const st = sk.snap || C.niceTicks(yr[0], yr[1], 8)[1] - C.niceTicks(yr[0], yr[1], 8)[0];
            pts[i][1] = K.round(K.clamp(pts[i][1] + dy * st / (sk.snap ? 1 : 4), yr[0], yr[1]), 4);
            R.commit({ sketch: { points: pts } }); R.emit({ type: 'sketch', points: pts, phase: 'end' });
            return;
          }
          const pt = (R.state.points || []).find((q) => q.id === id); if (!pt) return;
          const st = pt.snap || (C.niceTicks(xr[0], xr[1], 10)[1] - C.niceTicks(xr[0], xr[1], 10)[0]) / 2;
          movePoint(R, id, pt.x + dx * st, pt.y + dy * st, true);
        },
      },
      onEnable(m, opts, R) {
        if (m !== 'sketch') return;
        const sk = R.state.sketch || {};
        const n = opts.control || (sk.points && sk.points.length) || 5;
        const range = opts.xRange || sk.xRange || xr;
        let pts = sk.points;
        if (!pts || pts.length !== n || opts.reset) {
          const y0 = opts.start != null ? opts.start : yr[0] <= 0 && yr[1] >= 0 ? 0 : (yr[0] + yr[1]) / 2;
          pts = Array.from({ length: n }, (_, i) => [K.round(range[0] + (range[1] - range[0]) * i / (n - 1), 6), y0]);
        }
        R.commit({ sketch: { ...sk, points: pts, target: opts.target ?? sk.target, band: opts.band ?? sk.band, snap: opts.snap ?? sk.snap, xRange: range } });
      },
      methods: (R) => ({
        /* Curve y values of the sketch at xs, for grading. */
        sample: (xs) => { const pts = (R.state.sketch || {}).points || []; return xs.map((x) => crY(pts, x)); },
        /* Evaluate a named function at x with the current params. */
        evaluate: (id, x) => { const f = evaluator(R.state)[id]; return f ? f(x) : NaN; },
        /* Shared drag contract: positions of the movable points, and placing one (reveal, reset, resume). */
        points: () => Object.fromEntries((R.state.points || []).filter((q) => q.drag).map((q) => [q.id, { x: q.x, y: q.y }])),
        place: (id, pos, opts = {}) => { const [x, y] = Array.isArray(pos) ? pos : [pos, (R.state.points || []).find((q) => q.id === id)?.y ?? 0]; return R.inst.set({ points: { [id]: { x, y } } }, opts); },
      }),
    };

    const movePoint = (R, id, x, y, end) => {
      const pt = (R.state.points || []).find((q) => q.id === id); if (!pt) return;
      x = K.clamp(x, xr[0], xr[1]); y = K.clamp(y, yr[0], yr[1]);
      if (pt.snap) { x = K.snapTo(x, pt.snap); y = K.snapTo(y, pt.snap); }
      if (pt.snapX) x = K.snapTo(x, pt.snapX);
      if (pt.on) { const f = evaluator(R.state)[pt.on]; if (f) { const dom = f.def && f.def.domain; if (dom) x = K.clamp(x, dom[0], dom[1]); y = f(x); } } // a point on f stays inside f's domain
      if (pt.lockX) x = pt.x; if (pt.lockY) y = pt.y;
      x = K.round(x, 6); y = K.round(y, 6);
      R.commit({ points: { [id]: { x, y } } });
      R.emit({ type: 'drag', id, x, y, phase: end ? 'end' : 'move' });
    };

    return K.make(host, params, ctx, def);
  });

  /* Shared for the sketch widget */
  Z.cvb.catmullRomY = crY;
})();
