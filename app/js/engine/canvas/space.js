/* space: a rotatable 3D view in plain SVG (no WebGL): axes, a box and back-wall grid, points, vectors, parametric curves,
   polylines, surfaces z = f(x, y) or (x, y, z)(u, v) as shaded quads, planes and spans as translucent patches, and a
   vector field as arrows on a grid. Orthographic by default, weak perspective with params.perspective.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md ("space"). Builds on ZQ.cvb (canvas/plane.js).

   How it draws. scene(view) turns the state into 3D primitives (quads, segments, arrowheads, dots) once per state change
   and caches them. Each frame (a drag, a key, a patch) projects the primitives through the camera, sorts them by depth
   (painter's algorithm: far first, nearer pieces draw over farther ones) and rebuilds the SVG. Neighbouring pieces of one
   object share a <g class="cv-obj" data-id> so highlight, marks and tap work on whole objects. Labels are cached
   elements that only move. Surfaces and planes are cut into small cells and vectors into short pieces so ordinary
   intersections (a vector through a plane, a curve over a surface) sort correctly. */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  /* ---------- Styles: injected once, scoped to .cv-space, written against the shared tokens ---------- */
  const LEVELS = 16;
  const lightCss = Array.from({ length: LEVELS }, (_, k) => {
    const mix = `color-mix(in srgb, var(--c) ${Math.round(38 + 62 * k / (LEVELS - 1))}%, var(--cv-bg))`;
    return `.cv-space .l${k} { fill: ${mix}; stroke: ${mix}; }`;
  }).join('\n');
  const heightCss = Array.from({ length: LEVELS }, (_, k) => {
    const mix = `color-mix(in srgb, var(--c2, var(--ink)) ${Math.round(100 * k / (LEVELS - 1))}%, var(--c))`;
    return `.cv-space .h${k} { fill: ${mix}; stroke: ${mix}; }`;
  }).join('\n');
  const CSS = `
.cv-space .cv-svg { cursor: grab; user-select: none; -webkit-user-select: none; }
.cv-space.cv-static .cv-svg { cursor: default; }
.cv-space.cvb-dragging .cv-svg { cursor: grabbing; }
.cv-space .cv-svg:focus { outline: none; }
.cv-space .cv-svg.cvs-kb:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; border-radius: 4px; }
.cv-space .cvs-wall { fill: var(--grid); fill-opacity: 0.14; stroke: none; }
.cv-space .cvs-gl { fill: none; stroke: var(--grid); stroke-width: 1; }
.cv-space .cvs-edge { fill: none; stroke: var(--axis); stroke-width: 1; stroke-opacity: 0.5; }
.cv-space .cvs-axis { fill: none; stroke: var(--axis); stroke-width: 1.6; stroke-linecap: round; }
.cv-space .cvs-axhead { fill: var(--axis); stroke: none; }
.cv-space .cvs-ln { fill: none; stroke: var(--c, var(--ink)); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.cv-space .cvs-ln.thin { stroke-width: 1.3; }
.cv-space .cvs-ln.bold { stroke-width: 3; }
.cv-space .cvs-ln.faint { stroke-width: 3.5; stroke-opacity: 0.45; }
.cv-space .cvs-ln.dash { stroke-dasharray: 5 4; stroke-linecap: butt; }
.cv-space .cvs-ln.drop { stroke-width: 1.2; stroke-dasharray: 3 3; stroke-linecap: butt; stroke-opacity: 0.7; }
.cv-space .cvs-head { fill: var(--c, var(--ink)); stroke: none; }
.cv-space .cvs-arrow { fill: var(--c, var(--ink)); stroke: var(--c, var(--ink)); stroke-width: 1.3; stroke-linejoin: round; }
.cv-space .cvs-dot { fill: var(--c, var(--ink)); stroke: var(--cv-bg); stroke-width: 1.5; }
.cv-space .cvs-dot.open { fill: var(--cv-bg); stroke: var(--c, var(--ink)); stroke-width: 2; }
${Array.from({ length: LEVELS }, (_, k) => `.cv-space .l${k}, .cv-space .h${k}`).join(', ')}, .cv-space .qf { stroke-width: 0.7; stroke-linejoin: round; }
${lightCss}
${heightCss}
.cv-space .qf { fill: var(--c); stroke: var(--c); }
.cv-space .qw { fill: var(--cv-bg); stroke: var(--c); stroke-width: 0.9; stroke-linejoin: round; }
.cv-space .pl { fill: var(--c); fill-opacity: var(--fo, 0.22); stroke: var(--c); stroke-opacity: 0.18; stroke-width: 0.6; stroke-linejoin: round; }
.cv-space .cvs-t path { fill-opacity: var(--fo, 0.5); stroke-opacity: var(--fo, 0.5); }
.cv-space .cvs-wire path { stroke: color-mix(in srgb, var(--c) 45%, var(--ink)); stroke-opacity: 0.6; stroke-width: 0.6; }
.cv-space .cv-hl { filter: drop-shadow(0 0 4px var(--pear-300, #e6ec9c)) drop-shadow(0 0 1.2px var(--ink)); }
.cv-space .cv-hl-on { filter: drop-shadow(0 0 8px var(--pear-300, #e6ec9c)) drop-shadow(0 0 1.5px var(--ink)); }
.cv-space .cv-hl .cvs-ln { stroke-width: 3.2; }
.cv-space .cvs-lab, .cv-space .cvs-lab * { pointer-events: none; }
.cv-space .cvs-hit { fill: transparent; stroke: transparent; stroke-width: 20; stroke-linecap: round; stroke-linejoin: round; cursor: pointer; }
.cv-space .is-on > .cvs-hit { fill: var(--manip-wash, rgba(60, 120, 255, 0.18)); stroke: var(--manip-wash, rgba(60, 120, 255, 0.18)); }
.cv-space [data-tap]:focus-visible .cvs-hit { stroke: var(--focus); stroke-width: 3; }
.cv-space.cv-static .cvs-hit { pointer-events: none; }
.cv-space .cvs-sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
`;
  const injectCss = () => {
    if (document.getElementById('cv-space-css')) return;
    const s = document.createElement('style'); s.id = 'cv-space-css'; s.textContent = CSS; document.head.append(s);
  };

  /* ---------- Small maths ---------- */
  const D2R = Math.PI / 180;
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
  const mul = (k, a) => [k * a[0], k * a[1], k * a[2]];
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const norm = (a) => Math.hypot(a[0], a[1], a[2]);
  const unit = (a) => { const n = norm(a); return n > 1e-12 ? mul(1 / n, a) : [0, 0, 0]; };
  const r1 = (v) => Math.round(v * 10) / 10;
  const isObj = (v) => v != null && typeof v === 'object' && !Array.isArray(v);
  const LIGHT = unit([-0.45, -0.6, 0.66]);
  const stripTex = (s) => String(s == null ? '' : s).replace(/\$|\\[a-zA-Z]+|[{}]/g, '');

  /* Sutherland-Hodgman against the six faces of an axis-aligned box (lo, hi), in data space */
  const clipPoly = (poly, lo, hi) => {
    const eps = 1e-9;
    for (let a = 0; a < 3 && poly.length; a++) {
      for (const side of [0, 1]) {
        const c = side ? hi[a] : lo[a], inside = (v) => (side ? v[a] <= c + eps : v[a] >= c - eps), out = [];
        for (let i = 0; i < poly.length; i++) {
          const cur = poly[i], prev = poly[(i + poly.length - 1) % poly.length], ci = inside(cur), pi = inside(prev);
          if (ci !== pi) { const t = (c - prev[a]) / (cur[a] - prev[a]); out.push(add(prev, mul(t, sub(cur, prev)))); }
          if (ci) out.push(cur);
        }
        poly = out;
        if (!poly.length) break;
      }
    }
    return poly;
  };
  /* a line (base + s * dir) cut to the box: [sMin, sMax] or null */
  const clipLine = (base, dir, lo, hi) => {
    let s0 = -Infinity, s1 = Infinity;
    for (let a = 0; a < 3; a++) {
      if (Math.abs(dir[a]) < 1e-12) { if (base[a] < lo[a] - 1e-9 || base[a] > hi[a] + 1e-9) return null; continue; }
      const t0 = (lo[a] - base[a]) / dir[a], t1 = (hi[a] - base[a]) / dir[a];
      s0 = Math.max(s0, Math.min(t0, t1)); s1 = Math.min(s1, Math.max(t0, t1));
    }
    return s0 < s1 ? [s0, s1] : null;
  };
  const hull = (pts) => { // monotone chain on [x, y]
    const p = pts.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]); if (p.length < 3) return p;
    const cr = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]), lower = [], upper = [];
    for (const q of p) { while (lower.length >= 2 && cr(lower[lower.length - 2], lower[lower.length - 1], q) <= 0) lower.pop(); lower.push(q); }
    for (const q of p.slice().reverse()) { while (upper.length >= 2 && cr(upper[upper.length - 2], upper[upper.length - 1], q) <= 0) upper.pop(); upper.push(q); }
    return lower.slice(0, -1).concat(upper.slice(0, -1));
  };

  const esc = (v) => String(v).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const mk = (tag, a) => { const el = document.createElementNS(C.NS, tag); for (const k in a) el.setAttribute(k, a[k]); return el; };
  const LISTS = ['points', 'vectors', 'curves', 'lines', 'surfaces', 'planes', 'fields'];

  C.register('space', (host, params, ctx) => {
    const K = Z.cvb;
    injectCss();
    const W = 540, H = Math.round(Math.max(240, Math.min(640, +params.height || 420)));
    const rng = (v, d) => (Array.isArray(v) && v.length === 2 && v.every((q) => Number.isFinite(+q)) && +v[1] > +v[0] ? [+v[0], +v[1]] : d);
    const xr = rng(params.x, [-5, 5]), yr = rng(params.y, [-5, 5]), zr = rng(params.z, [-5, 5]);
    const lo = [xr[0], yr[0], zr[0]], hi = [xr[1], yr[1], zr[1]], spans = lo.map((l, i) => hi[i] - l), mid = lo.map((l, i) => (l + hi[i]) / 2);
    /* box proportions: a cube by default; equal: true keeps units equal (orthogonality reads true); aspect: [a, b, c] sets them */
    const asp = Array.isArray(params.aspect) && params.aspect.length === 3 && params.aspect.every((q) => +q > 0) ? params.aspect.map(Number) : params.equal ? spans.map((s) => s / Math.max(...spans)) : [1, 1, 1];
    const kk = asp.map((a, i) => 2 * a / spans[i]);
    const toS = (p) => [(p[0] - mid[0]) * kk[0], (p[1] - mid[1]) * kk[1], (p[2] - mid[2]) * kk[2]];
    const Rad = Math.hypot(...asp), S0 = (Math.min(W, H) / 2 - 22) / (Rad * 0.8);
    const bounds = { x0: 8, x1: W - 8, y0: 10, y1: H - 10 };
    const HOME = { az: -60, el: 25, zoom: 1, ...(isObj(params.camera) ? params.camera : {}), ...(isObj((ctx.initial || {}).camera) ? ctx.initial.camera : {}) };
    HOME.az = ((+HOME.az || 0) + 540) % 360 - 180; HOME.el = K.clamp(+HOME.el || 0, -89, 89); HOME.zoom = K.clamp(+HOME.zoom || 1, 0.4, 3);
    const camOf = (view) => { const c = { ...HOME, ...(isObj(view.camera) ? view.camera : {}) }; return { az: +c.az || 0, el: K.clamp(+c.el || 0, -89, 89), zoom: K.clamp(+c.zoom || 1, 0.4, 3) }; };
    const sameCam = (a, b) => Math.abs(a.az - b.az) < 0.05 && Math.abs(a.el - b.el) < 0.05 && Math.abs(a.zoom - b.zoom) < 0.001;
    const ui = {};

    /* ---------- Scene: state to 3D primitives (cached until anything but the camera changes) ---------- */
    const build = (view) => {
      const P = { ...(params.params || {}), ...(isObj(view.params) ? view.params : {}) }, names = Object.keys(P);
      const ev = (v) => (typeof v === 'number' ? v : typeof v === 'string' && v.trim() ? K.fnOf(v, names)(0, P) : NaN);
      const vec = (a) => (Array.isArray(a) && a.length >= 3 ? [ev(a[0]), ev(a[1]), ev(a[2])] : [NaN, NaN, NaN]);
      const fin = (p) => p.every(Number.isFinite);
      const hideSet = new Set([].concat(view.hide || []).map(String)), showSet = new Set([].concat(view.show || []).map(String));
      const vis = (it) => isObj(it) && it.id != null && !hideSet.has(String(it.id)) && (!it.hidden || showSet.has(String(it.id)));
      const list = (k) => (Array.isArray(view[k]) ? view[k].filter(isObj) : []);
      const prims = [], labels = [], taps = [];
      let cellMax = 0; // the largest cell edge of any surface or plane, in scene units
      const opt = (k, d) => (hideSet.has(k) ? false : view[k] !== undefined ? view[k] : params[k] !== undefined ? params[k] : d);

      /* colours: explicit slots are reserved, the rest take the first free ones in order (vectors, curves, lines, surfaces, planes, fields) */
      const used = new Set(LISTS.flatMap((k) => list(k).map((it) => it.colour)).filter((c) => Number.isInteger(c)));
      let nxt = 0; const free = () => { for (let n = 0; n < 6; n++) { nxt = (nxt % 6) + 1; if (!used.has(nxt)) { used.add(nxt); return nxt; } } nxt = (nxt % 6) + 1; return nxt; };
      const slot = {}; const slotFor = (it, fallback) => (slot[it.id] ??= (it.colour ?? (fallback ?? free())));
      const G = (it, extra = {}) => ({ id: String(it.id), slot: slotFor(it, extra.slot), cls: extra.cls || '', style: extra.style || '' });
      const addSeg = (a, b, g, o = {}) => prims.push({ k: 's', a, b, g, cls: o.cls || 'cvs-ln', bias: o.bias ?? 0.02, trim: o.trim || 0 });
      const addLabel = (o) => { if (o.text != null && String(o.text) !== '') labels.push(o); };
      const sampleLine = (pts, g, o = {}) => { // a polyline as short pieces; dashed: runs of pieces on and off
        const dash = o.dashed ? 3 : 0;
        for (let i = 0; i + 1 < pts.length; i++) {
          if (!pts[i] || !pts[i + 1]) continue;
          if (dash && Math.floor(i / dash) % 2) continue;
          addSeg(pts[i], pts[i + 1], g, { cls: o.cls, bias: o.bias });
        }
      };

      /* axes through the origin (or along the low edges when 0 is out of range), arrowheads at the high ends, tick labels */
      const axG = { id: null, slot: 'ink', cls: 'cvs-axis' };
      const org = [0, 1, 2].map((i) => (lo[i] <= 0 && hi[i] >= 0 ? 0 : lo[i]));
      const axes = [];
      if (opt('axes', true) !== false) {
        for (let i = 0; i < 3; i++) {
          const a = org.slice(), b = org.slice(); a[i] = lo[i]; b[i] = hi[i];
          const pts = Array.from({ length: 7 }, (_, j) => toS(add(a, mul(j / 6, sub(b, a)))));
          for (let j = 0; j < 6; j++) addSeg(pts[j], pts[j + 1], axG, { cls: 'cvs-axis', bias: 0.012, trim: j === 5 ? 6 : 0 });
          prims.push({ k: 'h', tip: pts[6], back: pts[5], tail: pts[0], g: axG, cls: 'cvs-axhead', size: 8, bias: 0.02 });
          axes.push({ i, a: toS(a), b: toS(b) });
        }
      }
      const axLabels = Array.isArray(params.axisLabels) ? params.axisLabels : ['$x$', '$y$', '$z$'];
      const axisNames = axes.map((ax) => ({ p: ax.b, q: ax.a, text: axLabels[ax.i], cls: 'cvb-axlab', off: 14 }));
      const tickG = { id: null, slot: 'ink', cls: 'cvs-ticks' };
      if (opt('ticks', true) !== false && opt('axes', true) !== false) {
        for (let i = 0; i < 3; i++) {
          for (const v of C.niceTicks(lo[i], hi[i], 4)) {
            if (v < lo[i] - 1e-9 || v > hi[i] + 1e-9) continue;
            if (Math.abs(v) < 1e-9 && org.every((o) => o === 0) && i > 0) continue; // one zero at the origin
            const p = org.slice(); p[i] = v; prims.push({ k: 't', p: toS(p), text: K.fmt(v, 3), axis: i, g: tickG, bias: 0.045 });
          }
        }
      }

      /* evaluators other objects may ride */
      const surfFn = {}, curveFn = {};
      for (const s of list('surfaces')) {
        if (typeof s.z !== 'string' || typeof s.x === 'string') continue;
        const f = K.fnOf(s.z, ['y', ...names]), Q = { ...P };
        surfFn[s.id] = (x, y) => { Q.y = y; return f(x, Q); };
      }
      for (const c of list('curves')) {
        const fx = K.fnOf(String(c.x), ['t', ...names]), fy = K.fnOf(String(c.y), ['t', ...names]), fz = K.fnOf(String(c.z ?? 0), ['t', ...names]), Q = { ...P };
        curveFn[c.id] = (t) => { Q.t = t; return [fx(0, Q), fy(0, Q), fz(0, Q)]; };
      }

      /* points */
      const ptPos = {};
      for (const pt of list('points')) {
        let p = pt.p ? vec(pt.p) : vec([pt.x, pt.y, pt.z ?? 0]);
        if (pt.on && surfFn[pt.on]) p[2] = surfFn[pt.on](p[0], p[1]);
        if (pt.at && curveFn[pt.at]) p = curveFn[pt.at](ev(pt.t ?? 0));
        ptPos[pt.id] = p;
      }
      /* vectors: heads and tails, chained through `from` (a point id, a vector id or a triple) */
      const vAll = list('vectors'), vById = Object.fromEntries(vAll.map((v) => [v.id, v]));
      const head = (v) => vec(v.v);
      const tail = (v, depth = 0) => {
        if (v.from == null) return [0, 0, 0];
        if (Array.isArray(v.from)) return vec(v.from);
        if (ptPos[v.from]) return ptPos[v.from];
        const u = vById[v.from]; return u && depth < 12 ? add(tail(u, depth + 1), head(u)) : [0, 0, 0];
      };
      const vecEnd = {}; // resolved tail, tip per id, for planes and spans that name a vector
      for (const v of vAll) { const t = tail(v), h = head(v); vecEnd[v.id] = { t, h, tip: add(t, h) }; }
      for (const v of vAll) slotFor(v);
      for (const v of vAll) {
        if (!vis(v)) continue;
        const { t, tip } = vecEnd[v.id]; if (!fin(t) || !fin(tip)) continue;
        const a = toS(t), b = toS(tip), g = G(v), len = norm(sub(b, a)), n = K.clamp(Math.ceil(len / 0.32), 2, 9);
        const pts = Array.from({ length: n + 1 }, (_, j) => add(a, mul(j / n, sub(b, a))));
        const arrow = v.head !== false;
        for (let j = 0; j < n; j++) { if (v.dashed && j % 2) continue; addSeg(pts[j], pts[j + 1], g, { cls: 'cvs-ln bold', bias: 0.03, trim: arrow && j === n - 1 ? 7 : 0 }); }
        if (arrow) prims.push({ k: 'h', tip: b, back: pts[n - 1], tail: a, g, cls: 'cvs-head', size: 11, bias: 0.04 });
        if (v.drop) addSeg(b, toS([tip[0], tip[1], lo[2]]), g, { cls: 'cvs-ln drop', bias: 0.01 });
        if (v.label) addLabel({ p: b, q: v.labelPos === 'mid' ? null : a, mid: v.labelPos === 'mid' ? [a, b] : null, text: v.label, cls: 'cvb-strong', mode: v.labelPos === 'mid' ? 'side' : 'dir', off: 12, id: v.id });
        taps.push({ id: v.id, kind: 'line', pts: [a, b], aria: 'Vector ' + stripTex(v.label || v.id) });
      }
      for (const pt of list('points')) {
        if (!vis(pt)) continue;
        const p = ptPos[pt.id]; if (!fin(p)) continue;
        const s = toS(p), g = G(pt, { slot: 'ink' });
        prims.push({ k: 'p', p: s, r: pt.r || 5, open: !!pt.open, g, bias: 0.06 });
        if (pt.drop) addSeg(s, toS([p[0], p[1], lo[2]]), g, { cls: 'cvs-ln drop', bias: 0.01 });
        if (pt.label) addLabel({ p: s, text: pt.label, cls: 'cvb-strong', mode: 'at', pos: pt.labelPos || 'ne', id: pt.id });
        taps.push({ id: pt.id, kind: 'dot', pts: [s], aria: 'Point ' + stripTex(pt.label || pt.id) });
      }

      /* curves r(t) and polylines */
      for (const c of list('curves')) {
        if (!vis(c)) continue;
        const f = curveFn[c.id], t0 = ev((c.t || [0, 6.2832])[0]), t1 = ev((c.t || [0, 6.2832])[1]);
        if (!Number.isFinite(t0) || !Number.isFinite(t1)) continue;
        const N = K.clamp(Math.round(c.n || 160), 8, 600), g = G(c);
        let pts = Array.from({ length: N + 1 }, (_, i) => { const p = f(t0 + (t1 - t0) * i / N); return fin(p) ? toS(p) : null; });
        sampleLine(pts, g, { dashed: c.dashed, cls: 'cvs-ln' + (c.width === 'bold' ? ' bold' : '') });
        if (c.label) { const L = [...pts].reverse().find(Boolean), at = c.labelAt != null ? f(ev(c.labelAt)) : null, q = pts.filter(Boolean); const pp = at && fin(at) ? toS(at) : L; if (pp && q.length > 1) addLabel({ p: pp, q: q[Math.max(0, q.length - 4)], text: c.label, cls: 'cvb-strong', mode: 'dir', off: 12, id: c.id }); }
        pts = pts.filter(Boolean); if (pts.length > 1) taps.push({ id: c.id, kind: 'line', pts: pts.filter((_, i) => i % Math.ceil(pts.length / 40) === 0).concat([pts[pts.length - 1]]), aria: 'Curve ' + stripTex(c.label || c.id) });
      }
      for (const l of list('lines')) {
        if (!vis(l) || !Array.isArray(l.pts)) continue;
        let pts = l.pts.slice(0, 2000).map((p) => { const q = vec(p); return fin(q) ? toS(q) : null; });
        if (l.closed && pts.length > 2) pts = pts.concat([pts[0]]);
        const g = G(l); sampleLine(pts, g, { dashed: l.dashed, cls: 'cvs-ln' + (l.width === 'bold' ? ' bold' : '') });
        const q = pts.filter(Boolean);
        if (l.label && q.length > 1) addLabel({ p: q[q.length - 1], q: q[q.length - 2], text: l.label, cls: 'cvb-strong', mode: 'dir', off: 12, id: l.id });
        if (q.length > 1) taps.push({ id: l.id, kind: 'line', pts: q, aria: 'Line ' + stripTex(l.label || l.id) });
      }

      /* surfaces: the cells of all surfaces and planes together stay near 1600 so a drag stays smooth on a phone */
      const wantCells = list('surfaces').filter(vis).reduce((t, q) => { const n = Array.isArray(q.n) ? q.n : [q.n || 24, q.n || 24]; return t + K.clamp(+n[0] || 24, 2, 40) * K.clamp(+n[1] || +n[0] || 24, 2, 40); }, 0) + list('planes').filter(vis).reduce((t, q) => t + K.clamp(+q.res || 10, 3, 24) ** 2, 0);
      const squeeze = wantCells > 1600 ? Math.sqrt(1600 / wantCells) : 1;
      const nCap = (v, d) => K.clamp(Math.round((+v || d) * squeeze), 2, 40);
      for (const s of list('surfaces')) {
        if (!vis(s)) continue;
        const param = typeof s.x === 'string', g0 = G(s);
        let nu, nv, at;
        if (param) {
          const fx = K.fnOf(String(s.x), ['u', 'v', ...names]), fy = K.fnOf(String(s.y), ['u', 'v', ...names]), fz = K.fnOf(String(s.z), ['u', 'v', ...names]);
          const ur = (s.u || [0, 1]).map(ev), vr = (s.v || [0, 1]).map(ev); if (![...ur, ...vr].every(Number.isFinite)) continue;
          nu = Array.isArray(s.n) ? nCap(s.n[0], 28) : nCap(s.n, 28); nv = Array.isArray(s.n) ? nCap(s.n[1], 28) : nu;
          const Q = { ...P };
          at = (i, j) => { Q.u = ur[0] + (ur[1] - ur[0]) * i / nu; Q.v = vr[0] + (vr[1] - vr[0]) * j / nv; return [fx(0, Q), fy(0, Q), fz(0, Q)]; };
        } else {
          const sx = rng(s.x, xr), sy = rng(s.y, yr), f = surfFn[s.id]; if (!f) continue;
          nu = Array.isArray(s.n) ? nCap(s.n[0], 24) : nCap(s.n, 24); nv = Array.isArray(s.n) ? nCap(s.n[1], 24) : nu;
          at = (i, j) => { const x = sx[0] + (sx[1] - sx[0]) * i / nu, y = sy[0] + (sy[1] - sy[0]) * j / nv; return [x, y, f(x, y)]; };
        }
        const clip = s.clip || (param ? 'none' : 'clamp'), grid = [];
        for (let i = 0; i <= nu; i++) { grid.push([]); for (let j = 0; j <= nv; j++) grid[i].push(at(i, j)); }
        const mode = s.shade || 'light', wire = s.wire, opacity = s.opacity == null ? 1 : K.clamp(+s.opacity, 0.05, 1);
        const c2 = s.colour2 ?? (Number.isInteger(s.colour) ? (s.colour % 6) + 1 : 3);
        const g = { ...g0, cls: (opacity < 1 ? 'cvs-t ' : '') + (wire === true ? 'cvs-wire' : ''), style: `--fo:${opacity};--c2:var(--s${c2})` };
        const zOut = (p) => (p[2] < lo[2] - 1e-9 ? -1 : p[2] > hi[2] + 1e-9 ? 1 : 0), boxOut = (p) => [0, 1, 2].some((a) => p[a] < lo[a] - 1e-9 || p[a] > hi[a] + 1e-9);
        /* vertex normals from neighbouring vertices (central differences), so one quad's light is the mean of its corners */
        const sg = grid.map((col) => col.map((p) => (fin(p) ? toS(clip === 'clamp' ? [p[0], p[1], K.clamp(p[2], lo[2], hi[2])] : p) : null)));
        const vn = (i, j) => {
          const a = sg[Math.max(0, i - 1)][j] && sg[Math.min(nu, i + 1)][j] ? sub(sg[Math.min(nu, i + 1)][j], sg[Math.max(0, i - 1)][j]) : null, b = sg[i][Math.max(0, j - 1)] && sg[i][Math.min(nv, j + 1)] ? sub(sg[i][Math.min(nv, j + 1)], sg[i][Math.max(0, j - 1)]) : null;
          return a && b ? unit(cross(a, b)) : null;
        };
        const nrmG = grid.map((col, i) => col.map((_, j) => (sg[i][j] ? vn(i, j) : null)));
        for (let i = 0; i < nu; i++) for (let j = 0; j < nv; j++) {
          let q = [grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]];
          if (!q.every(fin)) continue;
          if (clip === 'clamp') { const zo = q.map(zOut); if (zo.every((v) => v === zo[0] && v !== 0)) continue; q = q.map((p) => [p[0], p[1], K.clamp(p[2], lo[2], hi[2])]); }
          else if (clip === 'drop' && q.some(boxOut)) continue;
          const v = q.map(toS), ns = [nrmG[i][j], nrmG[i + 1][j], nrmG[i + 1][j + 1], nrmG[i][j + 1]].filter(Boolean);
          const shade = ns.length ? ns.reduce((t, n) => t + Math.abs(dot(n, LIGHT)), 0) / ns.length : Math.abs(dot(unit(cross(sub(v[2], v[0]), sub(v[3], v[1]))), LIGHT));
          const lit = 0.3 + 0.7 * shade, zc = (q[0][2] + q[1][2] + q[2][2] + q[3][2]) / 4;
          const cls = wire === 'only' ? 'qw' : mode === 'flat' ? 'qf' : mode === 'height' ? 'h' + K.clamp(Math.round((LEVELS - 1) * (zc - lo[2]) / spans[2]), 0, LEVELS - 1) : 'l' + K.clamp(Math.round((LEVELS - 1) * lit), 0, LEVELS - 1);
          prims.push({ k: 'q', v, cls, g, bias: 0 }); cellMax = Math.max(cellMax, norm(sub(v[1], v[0])), norm(sub(v[3], v[0])));
        }
        const tp = []; for (let i = 0; i <= nu; i += Math.max(1, Math.floor(nu / 8))) for (let j = 0; j <= nv; j += Math.max(1, Math.floor(nv / 8))) if (fin(grid[i][j])) tp.push(toS(grid[i][j]));
        if (s.label) { const lx = Array.isArray(s.labelAt) ? s.labelAt : null, p = !param && lx && surfFn[s.id] ? [lx[0], lx[1], surfFn[s.id](lx[0], lx[1])] : null; if (p && fin(p)) addLabel({ p: toS(p), text: s.label, cls: 'cvb-strong', mode: 'at', pos: 'n', id: s.id }); else if (tp.length) addLabel({ cands: tp, text: s.label, cls: 'cvb-strong', mode: 'top', id: s.id }); }
        taps.push({ id: s.id, kind: 'hull', pts: tp, aria: 'Surface ' + stripTex(s.label || s.id) });
      }

      /* planes and spans */
      for (const pl of list('planes')) {
        if (!vis(pl)) continue;
        const sp = (Array.isArray(pl.span) ? pl.span : []).map((e) => (Array.isArray(e) ? vec(e) : vecEnd[e] ? vecEnd[e].h : [NaN, NaN, NaN]));
        const firstVec = Array.isArray(pl.span) && typeof pl.span[0] === 'string' ? vById[pl.span[0]] : null;
        const g0 = G(pl, { slot: firstVec ? slotFor(firstVec) : undefined });
        const base = pl.through ? vec(pl.through) : [0, 0, 0]; if (!fin(base)) continue;
        const res = K.clamp(Math.round((pl.res || 10) * squeeze), 3, 24), opacity = pl.opacity == null ? 0.22 : K.clamp(+pl.opacity, 0.03, 1);
        const g = { ...g0, style: `--fo:${opacity}` };
        let e1 = null, e2 = null, finite = null, tp = [];
        if (sp.length >= 2 && sp.slice(0, 2).every(fin) && norm(cross(sp[0], sp[1])) > 1e-9 * Math.max(1, norm(sp[0]) * norm(sp[1]))) {
          if (Array.isArray(pl.extent)) { e1 = sp[0]; e2 = sp[1]; const x = pl.extent; finite = x.length >= 4 ? [x[0], x[1], x[2], x[3]] : [x[0], x[1], x[0], x[1]]; }
          else { e1 = unit(sp[0]); e2 = unit(sub(sp[1], mul(dot(sp[1], e1), e1))); }
        } else if (Array.isArray(pl.normal)) {
          const n = vec(pl.normal); if (!fin(n) || norm(n) < 1e-9) continue;
          const nu = unit(n), pt0 = pl.through ? base : mul(ev(pl.d ?? pl.offset ?? 0) / norm(n), nu);
          e1 = unit(cross(nu, Math.abs(nu[2]) < 0.9 ? [0, 0, 1] : [1, 0, 0])); e2 = cross(nu, e1);
          base[0] = pt0[0]; base[1] = pt0[1]; base[2] = pt0[2];
        } else if (sp.length >= 1 && fin(sp[0]) && norm(sp[0]) > 1e-9) { // one vector (or dependent ones): a line
          const rg = clipLine(base, sp[0], lo, hi); if (!rg) continue;
          const pts = Array.from({ length: 9 }, (_, j) => toS(add(base, mul(rg[0] + (rg[1] - rg[0]) * j / 8, sp[0]))));
          const gl = { ...g0, style: '' };
          for (let j = 0; j < 8; j++) addSeg(pts[j], pts[j + 1], gl, { cls: 'cvs-ln faint', bias: 0.015 });
          for (let j = 0; j < 8; j++) addSeg(pts[j], pts[j + 1], gl, { cls: 'cvs-ln thin dash', bias: 0.016 });
          if (pl.label) addLabel({ p: pts[8], q: pts[6], text: pl.label, cls: 'cvb-strong', mode: 'dir', off: 12, id: pl.id });
          taps.push({ id: pl.id, kind: 'line', pts: [pts[0], pts[8]], aria: 'Span ' + stripTex(pl.label || pl.id) });
          continue;
        } else continue;
        let a0, a1, b0, b1;
        if (finite) [a0, a1, b0, b1] = finite;
        else {
          const L = norm(spans) * 2, big = [[-L, -L], [L, -L], [L, L], [-L, L]].map(([a, b]) => add(base, add(mul(a, e1), mul(b, e2))));
          const poly = clipPoly(big, lo, hi); if (poly.length < 3) continue;
          const ab = poly.map((p) => [dot(sub(p, base), e1), dot(sub(p, base), e2)]);
          a0 = Math.min(...ab.map((q) => q[0])); a1 = Math.max(...ab.map((q) => q[0])); b0 = Math.min(...ab.map((q) => q[1])); b1 = Math.max(...ab.map((q) => q[1]));
        }
        const at = (a, b) => add(base, add(mul(a, e1), mul(b, e2))), all = [];
        for (let i = 0; i < res; i++) for (let j = 0; j < res; j++) {
          const A0 = a0 + (a1 - a0) * i / res, A1 = a0 + (a1 - a0) * (i + 1) / res, B0 = b0 + (b1 - b0) * j / res, B1 = b0 + (b1 - b0) * (j + 1) / res;
          const poly = clipPoly([at(A0, B0), at(A1, B0), at(A1, B1), at(A0, B1)], lo, hi);
          if (poly.length < 3) continue;
          const v = poly.map(toS); prims.push({ k: 'q', v, cls: 'pl', g, bias: 0 }); all.push(...v); cellMax = Math.max(cellMax, norm(sub(v[1], v[0])), norm(sub(v[v.length - 1], v[0])));
          if ((i + j) % 3 === 0) tp.push(...v);
        }
        if (!all.length) continue;
        if (pl.label) { if (Array.isArray(pl.labelAt)) addLabel({ p: toS(vec(pl.labelAt)), text: pl.label, cls: 'cvb-strong', mode: 'at', pos: 'n', id: pl.id }); else addLabel({ cands: all.filter((_, q) => q % Math.ceil(all.length / 60) === 0), text: pl.label, cls: 'cvb-strong', mode: 'top', id: pl.id }); }
        taps.push({ id: pl.id, kind: 'hull', pts: tp, aria: 'Plane ' + stripTex(pl.label || pl.id) });
      }

      /* vector fields: F = [fx, fy, fz] in x, y, z (and params); n per axis, capped at 343 arrows */
      for (const fd of list('fields')) {
        if (!vis(fd) || !Array.isArray(fd.F) || fd.F.length < 3) continue;
        const fs = fd.F.slice(0, 3).map((e) => K.fnOf(String(e), ['y', 'z', ...names])), Q = { ...P };
        const nn = Array.isArray(fd.n) ? fd.n.slice(0, 3).map((v) => K.clamp(Math.round(+v || 1), 1, 9)) : [K.clamp(Math.round(+fd.n || 5), 1, 7), K.clamp(Math.round(+fd.n || 5), 1, 7), K.clamp(Math.round(+fd.n || 5), 1, 7)];
        while (nn.length < 3) nn.push(nn[0]);
        const total = nn[0] * nn[1] * nn[2]; if (total > 343) { const f = Math.cbrt(343 / total); for (let a = 0; a < 3; a++) nn[a] = Math.max(1, Math.floor(nn[a] * f)); }
        const fixed = Array.isArray(fd.at) ? fd.at : [], g = G(fd);
        const coord = (a, i) => (nn[a] === 1 ? (Number.isFinite(+fixed[a]) ? +fixed[a] : (lo[a] + hi[a]) / 2) : lo[a] + spans[a] * (i + 0.5) / nn[a]);
        const arr = [];
        for (let i = 0; i < nn[0]; i++) for (let j = 0; j < nn[1]; j++) for (let k2 = 0; k2 < nn[2]; k2++) {
          const p = [coord(0, i), coord(1, j), coord(2, k2)]; Q.y = p[1]; Q.z = p[2];
          const v = [fs[0](p[0], Q), fs[1](p[0], Q), fs[2](p[0], Q)]; if (fin(v)) arr.push({ p, v });
        }
        if (!arr.length) continue;
        const sv = (v) => [v[0] * kk[0], v[1] * kk[1], v[2] * kk[2]], cell = Math.min(...nn.map((n, a) => (n > 1 ? 2 * asp[a] / n : 2))) * 0.9;
        const mags = arr.map((q) => norm(sv(q.v))), maxM = Math.max(...mags, 1e-12), unitLen = fd.normalise === true || fd.normalize === true;
        const kScale = (Number.isFinite(+fd.scale) && +fd.scale > 0 ? +fd.scale : 1) * cell;
        arr.forEach((q, ix) => {
          const m = mags[ix]; if (m < 1e-12) return;
          const len = (unitLen ? 1 : m / maxM) * kScale, a = toS(q.p), d = mul(len / m, sv(q.v)), b = add(a, d);
          prims.push({ k: 'a', a, b, g, size: 7, bias: 0.03 });
        });
        if (fd.label) addLabel({ p: toS([hi[0], hi[1], hi[2]]), text: fd.label, cls: 'cvb-strong', mode: 'at', pos: 'nw', id: fd.id });
        taps.push({ id: fd.id, kind: 'hull', pts: arr.map((q) => toS(q.p)), aria: 'Field ' + stripTex(fd.label || fd.id) });
      }

      /* a line, dot or arrow lying on a curved surface may sit a little under its cells' far corners: lift it by a tenth of a cell */
      for (const p of prims) if (p.k !== 'q') p.bias += 0.1 * cellMax;
      const desc = ['vectors', 'points', 'curves', 'lines', 'surfaces', 'planes', 'fields'].map((k) => { const l = list(k).filter(vis); return l.length ? `${k} ${l.map((it) => stripTex(it.label || it.id)).join(', ')}` : ''; }).filter(Boolean).join('; ');
      /* what derive reads as values.<id>: a point's [x, y, z] (as placed on its curve or surface) and a vector's tip */
      const values = {};
      for (const pt of list('points')) if (fin(ptPos[pt.id])) values[pt.id] = ptPos[pt.id].map((v) => +v.toFixed(6));
      for (const v of vAll) if (fin(vecEnd[v.id].tip)) values[v.id] = vecEnd[v.id].tip.map((q) => +q.toFixed(6));
      return { prims, labels, taps, axes, axisNames, desc, values };
    };

    /* ---------- Frame: project, sort, draw ---------- */
    let cache = { key: null, sc: null };
    const sceneOf = (view) => {
      const rest = { ...view }; for (const k of ['camera', 'highlight', 'selected', 'caption']) delete rest[k]; // only the camera, highlight and tap selection change without a rebuild
      const key = JSON.stringify(rest);
      if (cache.key !== key) cache = { key, sc: build(view) };
      return cache.sc;
    };
    const labelCache = new Map();
    const labelEl = (text, cls, anchor) => {
      const key = anchor + '|' + cls + '|' + text; let el = labelCache.get(key);
      if (!el) {
        el = svg('g', { class: 'cvs-lab' }); el.append(K.lab(0, 0, text, { anchor, cls, halo: true }));
        labelCache.set(key, el); if (labelCache.size > 300) labelCache.delete(labelCache.keys().next().value);
      }
      return el;
    };
    const geo = { proj: null, cam: null, label: '' };

    const def = {
      kind: 'space', aria: params.aria || 'Three-dimensional view',
      modes: ['tap', 'slider'],
      badges: false,
      size: () => ({ w: W, h: H }),
      listKeys: LISTS,
      init: () => ({ camera: { ...HOME }, points: (params.points || []).map((p, i) => ({ ...p, id: p.id || 'p' + i })), vectors: (params.vectors || []).map((v, i) => ({ ...v, id: v.id || 'v' + i })), curves: (params.curves || []).map((c, i) => ({ ...c, id: c.id || 'c' + i })), lines: (params.lines || []).map((c, i) => ({ ...c, id: c.id || 'l' + i })), surfaces: (params.surfaces || []).map((s, i) => ({ ...s, id: s.id || 's' + i })), planes: (params.planes || []).map((p, i) => ({ ...p, id: p.id || 'pl' + i })), fields: (params.fields || []).map((f, i) => ({ ...f, id: f.id || 'f' + i })), show: [], hide: [], params: { ...(params.params || {}) }, highlight: [], selected: [] }),
      render(view, R) {
        const sc = sceneOf(view), cam = camOf(view);
        const a = cam.az * D2R, e = cam.el * D2R, ca = Math.cos(a), sa = Math.sin(a), ce = Math.cos(e), se = Math.sin(e);
        const rv = [-sa, ca, 0], uv = [-se * ca, -se * sa, ce], dv = [ce * ca, ce * sa, se];
        const S = S0 * cam.zoom, persp = K.clamp(+(view.perspective ?? params.perspective ?? 0) || 0, 0, 1);
        const proj = (p) => { const dz = dv[0] * p[0] + dv[1] * p[1] + dv[2] * p[2], f = persp ? 1 / (1 - persp * dz / (2 * Rad)) : 1; return [W / 2 + S * f * (rv[0] * p[0] + rv[1] * p[1]), H / 2 - S * f * (uv[0] * p[0] + uv[1] * p[1] + uv[2] * p[2]), dz]; };
        const g = R.F.g, bg = svg('g'), layer = svg('g'), tapL = svg('g'), labL = svg('g'), hid = new Set([].concat(view.hide || []).map(String));

        /* background: the box edges and the grids on the faces that face away from the camera */
        const gridOpt = hid.has('grid') ? false : view.grid !== undefined ? view.grid : params.grid !== undefined ? params.grid : 'back';
        const ex = asp;
        const corner = (i, j, k) => [(i ? 1 : -1) * ex[0], (j ? 1 : -1) * ex[1], (k ? 1 : -1) * ex[2]];
        const pl = (pts, cls) => mk('path', { d: 'M' + pts.map((q) => r1(q[0]) + ',' + r1(q[1])).join('L') + (cls === 'cvs-wall' ? 'Z' : ''), class: cls });
        if (!hid.has('box') && (view.box ?? params.box ?? true) !== false) {
          for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) {
            bg.append(pl([proj(corner(i, j, 0)), proj(corner(i, j, 1))], 'cvs-edge'), pl([proj(corner(i, 0, j)), proj(corner(i, 1, j))], 'cvs-edge'), pl([proj(corner(0, i, j)), proj(corner(1, i, j))], 'cvs-edge'));
          }
        }
        if (gridOpt) {
          const tk = [0, 1, 2].map((ax) => C.niceTicks(lo[ax], hi[ax], 4).map((v) => (v - mid[ax]) * kk[ax]));
          for (let ax = 0; ax < 3; ax++) for (const side of [-1, 1]) {
            const nrm = [0, 0, 0]; nrm[ax] = side; if (dot(nrm, dv) >= -1e-6) continue; // faces turned to us are not drawn
            if (gridOpt === 'floor' && ax !== 2) continue;
            const [u1, u2] = [0, 1, 2].filter((q) => q !== ax), pt = (c1, c2) => { const p = [0, 0, 0]; p[ax] = side * ex[ax]; p[u1] = c1; p[u2] = c2; return proj(p); };
            bg.append(pl([pt(-ex[u1], -ex[u2]), pt(ex[u1], -ex[u2]), pt(ex[u1], ex[u2]), pt(-ex[u1], ex[u2])], 'cvs-wall'));
            for (const t of tk[u1]) bg.append(pl([pt(t, -ex[u2]), pt(t, ex[u2])], 'cvs-gl'));
            for (const t of tk[u2]) bg.append(pl([pt(-ex[u1], t), pt(ex[u1], t)], 'cvs-gl'));
          }
        }

        /* tick numbers sit beside their axis, away from the middle of the drawing (an edge-on axis has none) */
        const tickDir = sc.axes.map((ax) => {
          const A = proj(ax.a), B = proj(ax.b), c0 = proj([0, 0, 0]); let dx = B[0] - A[0], dy = B[1] - A[1]; const L = Math.hypot(dx, dy); if (L < 20) return null;
          dx /= L; dy /= L; let nx = -dy, ny = dx; const mx = (A[0] + B[0]) / 2 - c0[0], my = (A[1] + B[1]) / 2 - c0[1], side = nx * mx + ny * my;
          if (side < 0 || (Math.abs(side) < 1 && ny < 0)) { nx = -nx; ny = -ny; }
          return { nx, ny };
        });

        /* the sorted pieces */
        const items = sc.prims.map((p) => {
          if (p.k === 'q') { const v = p.v.map(proj); let zmin = Infinity; for (const q of v) if (q[2] < zmin) zmin = q[2]; return { p, v, z: zmin }; } // a cell sorts by its farthest corner: anything lying in a flat cell draws after it
          if (p.k === 's' || p.k === 'a') { const A = proj(p.a), B = proj(p.b); return { p, A, B, z: (A[2] + B[2]) / 2 + p.bias }; }
          if (p.k === 'h') { const T = proj(p.tip); return { p, T, Bk: proj(p.back), Tl: proj(p.tail), z: T[2] + p.bias }; }
          const Pp = proj(p.p); return { p, P: Pp, z: Pp[2] + p.bias };
        });
        items.sort((x, y) => x.z - y.z);
        const headD = (T, Bk, Tl, size) => {
          let dx = T[0] - Bk[0], dy = T[1] - Bk[1], L = Math.hypot(dx, dy);
          if (L < 0.5) { dx = T[0] - Tl[0]; dy = T[1] - Tl[1]; L = Math.hypot(dx, dy); }
          let ux = 0, uy = -1; if (L > 0.5) { ux = dx / L; uy = dy / L; }
          const full = Math.hypot(T[0] - Tl[0], T[1] - Tl[1]), hh = K.clamp(full * 0.5, Math.min(4, size), size), w = hh * 0.5, bx = T[0] - ux * hh, by = T[1] - uy * hh;
          return `M${r1(T[0])},${r1(T[1])}L${r1(bx - uy * w)},${r1(by + ux * w)}L${r1(bx + uy * w)},${r1(by - ux * w)}Z`;
        };
        /* the pieces go in as one markup string (far faster than creating a thousand elements a frame); a run of pieces of one
           object shares a <g class="cv-obj" data-id> */
        let curG = null, html = '';
        for (const it of items) {
          const p = it.p;
          if (p.g !== curG) {
            if (curG) html += '</g>';
            curG = p.g;
            html += curG.id != null ? `<g class="cv-obj ${K.colourCls(curG.slot)}${curG.cls ? ' ' + curG.cls : ''}" data-id="${esc(curG.id)}"${curG.style ? ` style="${curG.style}"` : ''}>` : `<g${curG.cls ? ` class="${curG.cls}"` : ''}>`;
          }
          if (p.k === 'q') {
            let d = 'M'; for (let i = 0; i < it.v.length; i++) d += (i ? 'L' : '') + r1(it.v[i][0]) + ',' + r1(it.v[i][1]);
            html += `<path d="${d}Z" class="${p.cls}"/>`;
          } else if (p.k === 's') {
            let { A, B } = it;
            if (p.trim) { const dx = B[0] - A[0], dy = B[1] - A[1], L = Math.hypot(dx, dy); if (L > 0.5) { const t = Math.min(p.trim, L * 0.8) / L; B = [B[0] - dx * t, B[1] - dy * t]; } }
            html += `<line x1="${r1(A[0])}" y1="${r1(A[1])}" x2="${r1(B[0])}" y2="${r1(B[1])}" class="${p.cls}"/>`;
          } else if (p.k === 'h') {
            html += `<path d="${headD(it.T, it.Bk, it.Tl, p.size)}" class="${p.cls}"/>`;
          } else if (p.k === 'a') { // a field arrow: shaft and head in one path
            const dx = it.B[0] - it.A[0], dy = it.B[1] - it.A[1], L = Math.hypot(dx, dy) || 1, t = Math.min(4, L * 0.7) / L;
            html += `<path d="M${r1(it.A[0])},${r1(it.A[1])}L${r1(it.B[0] - dx * t)},${r1(it.B[1] - dy * t)}${headD(it.B, it.A, it.A, p.size)}" class="cvs-arrow"/>`;
          } else if (p.k === 't') {
            const d = tickDir[p.axis]; if (!d) continue;
            html += `<text x="${r1(it.P[0] + d.nx * 11)}" y="${r1(it.P[1] + d.ny * 9)}" text-anchor="${d.nx > 0.5 ? 'start' : d.nx < -0.5 ? 'end' : 'middle'}" dominant-baseline="central" class="cvb-t cvb-tick cvb-halo" style="font-size:11px">${esc(p.text)}</text>`;
          } else html += `<circle cx="${r1(it.P[0])}" cy="${r1(it.P[1])}" r="${p.r}" class="cvs-dot${p.open ? ' open' : ''}"/>`;
        }
        if (curG) html += '</g>';
        layer.innerHTML = html;

        /* tap targets: one transparent shape per object */
        if (R.mode === 'tap' && !R.static) {
          const order = { hull: 0, line: 1, dot: 2 }; // big shapes underneath, so a dot or an arrow on a surface stays tappable
          for (const t of sc.taps.slice().sort((x, y) => order[x.kind] - order[y.kind])) {
            const pts = t.pts.map(proj); let shape;
            if (t.kind === 'dot') shape = mk('circle', { cx: r1(pts[0][0]), cy: r1(pts[0][1]), r: 12, class: 'cvs-hit' });
            else if (t.kind === 'line') shape = mk('path', { d: 'M' + pts.map((q) => r1(q[0]) + ',' + r1(q[1])).join('L'), class: 'cvs-hit', style: 'fill:none' });
            else { const h = hull(pts.map((q) => [q[0], q[1]])); if (h.length < 3) continue; shape = mk('path', { d: 'M' + h.map((q) => r1(q[0]) + ',' + r1(q[1])).join('L') + 'Z', class: 'cvs-hit', style: 'stroke-width:4' }); }
            const o = svg('g', { class: 'cv-obj cvs-tapobj', 'data-id': t.id }); o.append(shape); R.tappable(o, t.id, t.aria); tapL.append(o);
          }
        }

        /* labels: item labels avoid each other; tick numbers are sorted with the drawing so a surface hides them */
        const specs = [];
        for (const an of sc.axisNames) {
          const A = proj(an.p), B = proj(an.q); let dx = A[0] - B[0], dy = A[1] - B[1]; const L = Math.hypot(dx, dy) || 1; dx /= L; dy /= L;
          specs.push({ x: A[0] + dx * an.off, y: A[1] + dy * an.off, text: an.text, anchor: dx > 0.4 ? 'start' : dx < -0.4 ? 'end' : 'middle', cls: an.cls, fixed: true });
        }
        const cardinal = { n: [0, -13], ne: [11, -12], e: [13, 0], se: [11, 13], s: [0, 15], sw: [-11, 13], w: [-13, 0], nw: [-11, -12] };
        for (const lb of sc.labels) {
          const A = lb.p ? proj(lb.p) : [0, 0]; let x = A[0], y = A[1], anchor = 'middle';
          if (lb.mode === 'dir' && lb.q) { const B = proj(lb.q); let dx = A[0] - B[0], dy = A[1] - B[1]; const L = Math.hypot(dx, dy) || 1; dx /= L; dy /= L; x += dx * lb.off; y += dy * lb.off - 2; anchor = dx > 0.35 ? 'start' : dx < -0.35 ? 'end' : 'middle'; }
          else if (lb.mode === 'top') { let best = A, by = Infinity; for (const c of lb.cands) { const q = proj(c); if (q[1] < by) { by = q[1]; best = q; } } x = best[0]; y = best[1] - 13; }
          else if (lb.mode === 'side' && lb.mid) { const A2 = proj(lb.mid[0]), B2 = proj(lb.mid[1]); let dx = B2[0] - A2[0], dy = B2[1] - A2[1]; const L = Math.hypot(dx, dy) || 1; dx /= L; dy /= L; x = (A2[0] + B2[0]) / 2 + dy * 13; y = (A2[1] + B2[1]) / 2 - dx * 13; anchor = dy > 0.35 ? 'start' : dy < -0.35 ? 'end' : 'middle'; }
          else { const o = cardinal[lb.pos] || cardinal.ne; x += o[0]; y += o[1]; anchor = o[0] > 0 ? 'start' : o[0] < 0 ? 'end' : 'middle'; }
          specs.push({ x, y, text: lb.text, anchor, cls: lb.cls });
        }
        const movable = specs.filter((s) => !s.fixed);
        K.placeLabels(movable, specs.filter((s) => s.fixed).map((s) => K.boxOf(s)), bounds);
        for (const s of specs) { const el = labelEl(s.text, s.cls, s.anchor); el.setAttribute('transform', `translate(${r1(s.x)} ${r1(s.y)})`); labL.append(el); }

        g.append(bg, layer, tapL, labL);
        geo.proj = proj; geo.cam = cam;
        const label = `${params.aria || 'Three-dimensional view'}. ${sc.desc ? 'Shows ' + sc.desc + '. ' : ''}${R.static ? '' : 'Drag, or use the arrow keys, to rotate; plus and minus zoom; 0 resets.'}`;
        if (label !== geo.label) { geo.label = label; R.F.svg.setAttribute('aria-label', label); }
        if (ui.sync) ui.sync(cam);
      },
      methods: (R) => {
        const el = R.F.svg;
        const rotate = (az, el2, zoom, end) => { R.commit({ camera: { az: ((az + 540) % 360) - 180, el: K.clamp(el2, -89, 89), zoom: K.clamp(zoom, 0.4, 3) } }); R.emit({ type: 'rotate', az: R.state.camera.az, el: R.state.camera.el, zoom: R.state.camera.zoom, end: !!end }); };
        const cur = () => camOf(R.state);
        if (!R.static) {
          el.setAttribute('tabindex', '0'); el.setAttribute('role', 'group'); el.setAttribute('aria-roledescription', '3D view');
          if (params.touchScroll) el.style.touchAction = 'pan-y';
          const live = document.createElement('span'); live.className = 'cvs-sr'; live.setAttribute('role', 'status'); live.setAttribute('aria-live', 'polite'); R.F.wrap.append(live);
          const chip = document.createElement('button'); chip.type = 'button'; chip.className = 'cvb-chip quiet'; chip.textContent = 'Reset view';
          if (params.resetButton !== false) R.extra.append(chip);
          const reset = () => { R.inst.set({ camera: { ...HOME } }, { ms: 420 }); R.emit({ type: 'rotate', ...HOME, end: true }); live.textContent = 'View reset.'; };
          chip.addEventListener('click', reset);
          ui.reset = reset;
          ui.sync = (cam) => { chip.disabled = sameCam(cam, HOME); };
          const ptrs = new Map(); let drag = null, pinch = null, pend = null, raf = 0;
          const flush = (end) => { raf = 0; if (pend) { const p = pend; pend = null; rotate(p.az, p.el, p.zoom, end); } };
          el.addEventListener('pointerdown', (e) => {
            el.classList.remove('cvs-kb');
            if (R.locked || (e.pointerType === 'mouse' && e.button !== 0)) return;
            ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
            const c = cur();
            if (ptrs.size === 1) drag = { x: e.clientX, y: e.clientY, az: c.az, el: c.el, id: e.pointerId, on: false };
            else if (ptrs.size === 2) { const [p, q] = [...ptrs.values()]; pinch = { d: Math.hypot(p.x - q.x, p.y - q.y) || 1, zoom: c.zoom }; if (drag && !drag.on) { try { el.setPointerCapture(drag.id); } catch { /* no capture */ } } drag = null; R.F.wrap.classList.add('cvb-dragging'); }
          });
          el.addEventListener('pointermove', (e) => {
            if (!ptrs.has(e.pointerId)) return;
            ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
            const c = cur();
            if (pinch && ptrs.size >= 2) { const [p, q] = [...ptrs.values()]; pend = { az: c.az, el: c.el, zoom: pinch.zoom * (Math.hypot(p.x - q.x, p.y - q.y) / pinch.d) }; if (!raf) raf = requestAnimationFrame(() => flush(false)); e.preventDefault(); return; }
            if (!drag || drag.id !== e.pointerId) return;
            const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
            if (!drag.on) { if (Math.hypot(dx, dy) < 5) return; drag.on = true; try { el.setPointerCapture(e.pointerId); } catch { /* no capture */ } R.F.wrap.classList.add('cvb-dragging'); }
            e.preventDefault();
            pend = { az: drag.az - dx * 0.5, el: params.touchScroll && e.pointerType === 'touch' ? c.el : K.clamp(drag.el + dy * 0.5, -89, 89), zoom: c.zoom };
            if (!raf) raf = requestAnimationFrame(() => flush(false));
          });
          const up = (e) => {
            if (!ptrs.has(e.pointerId)) return;
            ptrs.delete(e.pointerId);
            const was = drag && drag.on || pinch;
            if (ptrs.size < 2) pinch = null;
            if (drag && drag.id === e.pointerId) drag = null;
            if (raf) { cancelAnimationFrame(raf); raf = 0; }
            if (was) { if (pend) flush(true); else R.emit({ type: 'rotate', ...cur(), end: true }); try { el.releasePointerCapture(e.pointerId); } catch { /* released */ } }
            if (!ptrs.size) R.F.wrap.classList.remove('cvb-dragging');
          };
          el.addEventListener('pointerup', up); el.addEventListener('pointercancel', up);
          el.addEventListener('keydown', (e) => {
            if (R.locked || e.target !== el) return; // a tap target keeps its own arrow-key focus moves
            if (e.key.length > 1 || /[+=_0-]/.test(e.key)) el.classList.add('cvs-kb');
            const c = cur(), st = e.shiftKey ? 15 : 5; let done = true;
            if (e.key === 'ArrowLeft') rotate(c.az + st, c.el, c.zoom, true);
            else if (e.key === 'ArrowRight') rotate(c.az - st, c.el, c.zoom, true);
            else if (e.key === 'ArrowUp') rotate(c.az, c.el - st, c.zoom, true);
            else if (e.key === 'ArrowDown') rotate(c.az, c.el + st, c.zoom, true);
            else if (e.key === '+' || e.key === '=') rotate(c.az, c.el, c.zoom * 1.15, true);
            else if (e.key === '-' || e.key === '_') rotate(c.az, c.el, c.zoom / 1.15, true);
            else if (e.key === '0' || e.key === 'Home') reset();
            else done = false;
            if (done) { e.preventDefault(); const n = cur(); if (e.key !== '0' && e.key !== 'Home') live.textContent = `Azimuth ${Math.round(n.az)} degrees, elevation ${Math.round(n.el)} degrees, zoom ${n.zoom.toFixed(2)}.`; }
          });
        } else ui.sync = null;
        return {
          /* az, el and zoom bind the camera (a slider can turn the view); a dotted name is a state path; anything else is a free parameter */
          setParam: (name, v) => {
            const n = String(name);
            if (n === 'az' || n === 'el' || n === 'zoom') R.inst.set({ camera: { [n]: +v } }, { instant: true });
            else R.inst.set(C.paramPatch(n, v), { instant: true });
          },
          getParam: (name) => { const n = String(name); if (n === 'az' || n === 'el' || n === 'zoom') return camOf(R.state)[n]; if (n.includes('.')) { let o = R.state; for (const k of n.split('.')) o = o == null ? undefined : Array.isArray(o) ? o.find((q) => q && q.id === k) : o[k]; return typeof o === 'number' ? o : undefined; } return (R.state.params || {})[n]; },
          /* positions for derive: values.P is the point P as [x, y, z] (a point on a curve or surface included), values.u a vector's tip */
          values: () => ({ ...sceneOf(R.state).values }),
          /* the camera as { az, el, zoom }, the home view, and a way back to it */
          camera: () => ({ ...camOf(R.state) }),
          reset: () => { R.inst.set({ camera: { ...HOME } }, { ms: 420 }); },
          /* screen position of a data point in the drawing's own units (the 540-wide viewBox): { x, y, depth } */
          project: (x, y, z) => { const p = geo.proj ? geo.proj(toS([x, y, z])) : [0, 0, 0]; return { x: p[0], y: p[1], depth: p[2] }; },
        };
      },
    };
    /* the player's Why? sheet passes ctx.mode 'static' (not ctx.static, which is all ZQ.cvb.make reads): a still copy */
    return K.make(host, params, ctx.mode === 'static' && !ctx.static ? { ...ctx, static: true } : ctx, def);
  });
})();
