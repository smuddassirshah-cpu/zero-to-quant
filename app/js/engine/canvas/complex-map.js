/* complex-map: a z-plane beside a w-plane showing what w = f(z) does to a grid, the unit circle, curves and points.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js).
   The first half (complex arithmetic and the formula compiler) needs no DOM, so node can require this file to check a
   formula (tools/validate.mjs); the canvas registers only when window.ZQ exists. */
(function () {
  'use strict';

  /* ---------- Complex numbers are [re, im]; a formula compiles to a function of an environment object ---------- */
  const cx = (a) => (typeof a === 'number' ? [a, 0] : Array.isArray(a) ? a : [NaN, NaN]);
  const add = (a, b) => [a[0] + b[0], a[1] + b[1]];
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
  const mul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
  const div = (a, b) => {
    /* Smith's method: no overflow in b.re^2 + b.im^2 for a huge b, and a zero divisor is NaN (a pole, not a number) */
    if (b[0] === 0 && b[1] === 0) return [NaN, NaN];
    if (Math.abs(b[0]) >= Math.abs(b[1])) { const r = b[1] / b[0], d = b[0] + b[1] * r; return [(a[0] + a[1] * r) / d, (a[1] - a[0] * r) / d]; }
    const r = b[0] / b[1], d = b[0] * r + b[1]; return [(a[0] * r + a[1]) / d, (a[1] * r - a[0]) / d];
  };
  const cexp = (a) => { const e = Math.exp(a[0]); return [e * Math.cos(a[1]), e * Math.sin(a[1])]; };
  const clog = (a) => [Math.log(Math.hypot(a[0], a[1])), Math.atan2(a[1], a[0])]; // principal branch: arg in (-pi, pi]
  const csqrt = (a) => { const r = Math.hypot(a[0], a[1]), re = Math.sqrt((r + a[0]) / 2), im = Math.sqrt(Math.max(0, (r - a[0]) / 2)); return [re, a[1] < 0 ? -im : im]; };
  const csin = (a) => [Math.sin(a[0]) * Math.cosh(a[1]), Math.cos(a[0]) * Math.sinh(a[1])];
  const ccos = (a) => [Math.cos(a[0]) * Math.cosh(a[1]), -Math.sin(a[0]) * Math.sinh(a[1])];
  const csinh = (a) => [Math.sinh(a[0]) * Math.cos(a[1]), Math.cosh(a[0]) * Math.sin(a[1])];
  const ccosh = (a) => [Math.cosh(a[0]) * Math.cos(a[1]), Math.sinh(a[0]) * Math.sin(a[1])];
  const cpow = (a, b) => {
    if (b[1] === 0 && Number.isInteger(b[0]) && Math.abs(b[0]) <= 64) { // whole powers by repeated squaring: exact, no branch cut
      let n = Math.abs(b[0]), r = [1, 0], p = a;
      while (n > 0) { if (n & 1) r = mul(r, p); p = mul(p, p); n >>= 1; }
      return b[0] < 0 ? div([1, 0], r) : r;
    }
    if (a[0] === 0 && a[1] === 0) return b[0] > 0 ? [0, 0] : [NaN, NaN];
    return cexp(mul(b, clog(a)));
  };
  const FN = {
    exp: cexp, log: clog, ln: clog, sqrt: csqrt, sin: csin, cos: ccos, tan: (a) => div(csin(a), ccos(a)), sinh: csinh, cosh: ccosh, tanh: (a) => div(csinh(a), ccosh(a)),
    conj: (a) => [a[0], 0 - a[1]], abs: (a) => [Math.hypot(a[0], a[1]), 0], arg: (a) => [Math.atan2(a[1], a[0]), 0], re: (a) => [a[0], 0], im: (a) => [a[1], 0],
    pow: cpow,
  };
  const ARITY = { pow: 2 };
  const CONST = { i: [0, 1], pi: [Math.PI, 0], e: [Math.E, 0] };

  /* Formula grammar: + - * / ^ (or **), unary minus, implicit multiplication (2z, 2(z + 1), a z), constants i, pi, e,
     functions exp, log (ln), sqrt, sin, cos, tan, sinh, cosh, tanh, conj, abs, arg, re, im, pow(a, b), and the names given. */
  const compile = (src, names = []) => {
    const text = String(src), re = /\s*(\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?|[A-Za-z_][A-Za-z_0-9]*|\*\*|[-+*/^(),])/y, toks = [];
    let pos = 0;
    for (;;) {
      re.lastIndex = pos; const m = re.exec(text);
      if (!m) { if (text.slice(pos).trim()) throw new Error(`cannot read "${text.slice(pos).trim().slice(0, 12)}" in ${text}`); break; }
      toks.push(m[1] === '**' ? '^' : m[1]); pos = re.lastIndex;
    }
    let k = 0;
    const peek = () => toks[k], next = () => toks[k++];
    const isNum = (t) => t != null && /^[\d.]/.test(t), isId = (t) => t != null && /^[A-Za-z_]/.test(t);
    const expect = (t) => { if (next() !== t) throw new Error(`expected "${t}" in ${text}`); };
    const atom = () => {
      const t = next();
      if (t == null) throw new Error(`the formula ends too soon: ${text}`);
      if (isNum(t)) { const v = [parseFloat(t), 0]; return () => v; }
      if (t === '(') { const e = expr(); expect(')'); return e; }
      if (isId(t)) {
        if (peek() === '(' && FN[t] && !names.includes(t)) {
          next(); const args = [expr()]; while (peek() === ',') { next(); args.push(expr()); } expect(')');
          if (args.length !== (ARITY[t] || 1)) throw new Error(`${t} takes ${ARITY[t] || 1} argument${(ARITY[t] || 1) > 1 ? 's' : ''}: ${text}`);
          const f = FN[t]; return args.length === 1 ? (env) => f(args[0](env)) : (env) => f(args[0](env), args[1](env));
        }
        if (names.includes(t)) return (env) => cx(env[t]);
        if (CONST[t]) { const v = CONST[t]; return () => v; }
        if (FN[t]) throw new Error(`${t} needs brackets: ${t}(...) in ${text}`);
        throw new Error(`unknown name "${t}" in ${text}`);
      }
      throw new Error(`unexpected "${t}" in ${text}`);
    };
    const power = () => { const base = atom(); if (peek() === '^') { next(); const ex = unary(); return (env) => cpow(base(env), ex(env)); } return base; };
    const unary = () => {
      if (peek() === '-') { next(); const u = unary(); return (env) => { const a = u(env); return [0 - a[0], 0 - a[1]]; }; } // 0 - x, not -x: no signed zero, so log(-1) is +pi
      if (peek() === '+') { next(); return unary(); }
      return power();
    };
    const term = () => {
      let l = unary();
      for (;;) {
        const t = peek();
        if (t === '*' || t === '/') { next(); const r = unary(), a = l; l = t === '*' ? (env) => mul(a(env), r(env)) : (env) => div(a(env), r(env)); }
        else if (isNum(t) || isId(t) || t === '(') { const r = power(), a = l; l = (env) => mul(a(env), r(env)); } // implicit multiplication
        else return l;
      }
    };
    const expr = () => {
      let l = term();
      for (;;) {
        const t = peek();
        if (t === '+' || t === '-') { next(); const r = term(), a = l; l = t === '+' ? (env) => add(a(env), r(env)) : (env) => sub(a(env), r(env)); }
        else return l;
      }
    };
    const f = expr();
    if (k < toks.length) throw new Error(`unexpected "${toks[k]}" in ${text}`);
    return f;
  };
  const api = { compile, cexp, clog };
  if (typeof window === 'undefined' || !window.ZQ) { if (typeof module !== 'undefined') module.exports = api; return; }

  /* ---------- The canvas ---------- */
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;
  Z.complexMap = api;

  C.register('complex-map', (host, params, ctx) => {
    const K = Z.cvb;
    const zx = params.x || [-2, 2], zy = params.y || zx;
    const wxr = params.wx || zx, wyr = params.wy || params.wx || zy;
    const TAU = 2 * Math.PI;
    const mt = 26, mb = 10, gap = 16, mx = 12;
    const niceStep = (raw) => { const e = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / e; return (m < 1.5 ? 1 : m < 3.5 ? 2 : m < 7.5 ? 5 : 10) * e; };

    /* Layout: side by side at 540 wide, stacked (one panel above the other, the frame as wide as the column) under 500 px wide */
    let geo = null, watch = null;
    const layout = (R) => {
      const avail = Math.round((R && R.F && R.F.wrap && R.F.wrap.clientWidth) || 0);
      const stacked = params.stack === true || (params.stack !== false && avail > 0 && avail < 500);
      const W = stacked ? Math.max(300, Math.min(540, avail || 540)) : 540;
      const pw = stacked ? W - 2 * mx : Math.floor((W - 2 * mx - gap) / 2);
      const ratio = (zy[1] - zy[0]) / (zx[1] - zx[0]) || 1;
      const ph = Math.round(params.height ? params.height : K.clamp(pw * ratio, 180, stacked ? 300 : 340));
      const H = stacked ? mt + ph + gap + mt + ph + mb : mt + ph + mb;
      const mk = (x0, y0, xr, yr) => {
        /* equal units: the ranges are minimums, the longer side of the box shows more, so angles stay true */
        const sc = Math.min(pw / (xr[1] - xr[0]), ph / (yr[1] - yr[0])), mxm = (xr[0] + xr[1]) / 2, mym = (yr[0] + yr[1]) / 2;
        const dx = pw / 2 / sc, dy = ph / 2 / sc;
        return { x0, y0, w: pw, h: ph, sx: C.scale([mxm - dx, mxm + dx], [x0, x0 + pw]), sy: C.scale([mym - dy, mym + dy], [y0 + ph, y0]), xd: [mxm - dx, mxm + dx], yd: [mym - dy, mym + dy] };
      };
      const z = mk(mx, mt, zx, zy), w = stacked ? mk(mx, mt + ph + gap + mt, wxr, wyr) : mk(mx + pw + gap, mt, wxr, wyr);
      return { stacked, W, H, pw, ph, z, w, key: [W, H, stacked].join() };
    };

    /* The function: state.f (or params.f) with the numbers in params.params and state.params as names */
    const fOf = (view) => {
      const src = String(view.f ?? params.f ?? 'z'), vals = { ...(params.params || {}), ...(view.params || {}) };
      const names = ['z', ...Object.keys(vals).filter((n) => n !== 'z')];
      try {
        const fn = compile(src, names), env = { ...vals };
        return { src, vals, F: (z) => { env.z = z; return fn(env); } };
      } catch (e) { return { src, vals, error: e.message, F: () => [NaN, NaN] }; }
    };
    const warned = new Set();

    /* ---- sampling a curve through f, clipped to a panel ---- */
    const BIG = 1e7, THR = 9, MAXD = 12;
    const pathOf = (zOf, s0, s1, n, F, P) => {
      const { x0, y0, w, h, sx, sy } = P, x1 = x0 + w, y1 = y0 + h;
      const px = (c) => { const X = sx(c[0]), Y = sy(c[1]); return Number.isFinite(X) && Number.isFinite(Y) && Math.abs(X) < BIG && Math.abs(Y) < BIG ? [X, Y] : null; };
      const at = (s) => { const z = zOf(s); const c = F ? F(z) : z; return px(c); };
      const code = (p) => (p[0] < x0 ? 1 : p[0] > x1 ? 2 : 0) | (p[1] < y0 ? 4 : p[1] > y1 ? 8 : 0);
      let d = '', last = null;
      const emit = (a, b) => { // Liang-Barsky against the panel
        let t0 = 0, t1 = 1; const dx = b[0] - a[0], dy = b[1] - a[1];
        for (const [p, q] of [[-dx, a[0] - x0], [dx, x1 - a[0]], [-dy, a[1] - y0], [dy, y1 - a[1]]]) {
          if (p === 0) { if (q < 0) return; } else { const r = q / p; if (p < 0) { if (r > t1) return; if (r > t0) t0 = r; } else { if (r < t0) return; if (r < t1) t1 = r; } }
        }
        const A = [a[0] + t0 * dx, a[1] + t0 * dy], B = [a[0] + t1 * dx, a[1] + t1 * dy];
        const join = last && Math.abs(last[0] - A[0]) < 0.01 && Math.abs(last[1] - A[1]) < 0.01;
        d += (join ? '' : `M${A[0].toFixed(1)},${A[1].toFixed(1)}`) + `L${B[0].toFixed(1)},${B[1].toFixed(1)}`; last = B;
      };
      const seg = (sa, A, sb, B, depth) => {
        if (!A || !B) { // a pole, or a value too large to draw: close in on it, so a curve runs on towards its limit (log z as z goes to 0)
          last = null;
          if ((A || B) && depth < MAXD) { const sm = (sa + sb) / 2, M = at(sm); seg(sa, A, sm, M, depth + 1); seg(sm, M, sb, B, depth + 1); }
          return;
        }
        if (code(A) & code(B)) { last = null; return; } // wholly beyond one edge
        const dist = Math.hypot(B[0] - A[0], B[1] - A[1]);
        if (dist > THR && depth < MAXD) { const sm = (sa + sb) / 2, M = at(sm); seg(sa, A, sm, M, depth + 1); seg(sm, M, sb, B, depth + 1); return; }
        if (dist > 30 && depth >= MAXD) { last = null; return; } // a jump (a pole, or the branch cut of log): not joined
        emit(A, B);
      };
      let prev = at(s0), sp = s0;
      for (let i = 1; i <= n; i++) { const s = s0 + (s1 - s0) * i / n, cur = at(s); seg(sp, prev, s, cur, 0); prev = cur; sp = s; }
      return d;
    };

    /* the drawing lists: which curves, in z, for the current grid settings and view */
    const curvesOf = (view, fo, g) => {
      const out = [], gridKind = view.grid ?? params.grid ?? 'cartesian', P = g.z;
      const span = Math.min(P.xd[1] - P.xd[0], P.yd[1] - P.yd[0]);
      const step = +(view.gridStep ?? params.gridStep) || niceStep(Math.min(zx[1] - zx[0], zy[1] - zy[0]) / 8 || span / 8);
      if (gridKind === 'cartesian' || gridKind === 'both') {
        for (let c = Math.ceil(P.xd[0] / step - 1e-9); c * step <= P.xd[1] + 1e-9; c++) out.push({ id: 'grid-x', slot: 1, n: 180, s: [P.yd[0], P.yd[1]], z: (t) => [c * step + 0, t] });
        for (let c = Math.ceil(P.yd[0] / step - 1e-9); c * step <= P.yd[1] + 1e-9; c++) out.push({ id: 'grid-y', slot: 2, n: 180, s: [P.xd[0], P.xd[1]], z: (t) => [t, c * step + 0] });
      }
      if (gridKind === 'polar' || gridKind === 'both') {
        const rMax = Math.hypot(Math.max(Math.abs(P.xd[0]), Math.abs(P.xd[1])), Math.max(Math.abs(P.yd[0]), Math.abs(P.yd[1])));
        const rs = (+(view.rStep ?? params.rStep)) || step, nr = Math.min(40, Math.floor(rMax / rs + 1e-9)), rays = Math.max(0, Math.round(view.rays ?? params.rays ?? 12));
        for (let k = 1; k <= nr; k++) out.push({ id: 'grid-r', slot: 3, n: 240, s: [0, TAU], z: (t) => [k * rs * Math.cos(t), k * rs * Math.sin(t)] });
        for (let k = 0; k < rays; k++) { const th = TAU * k / rays; out.push({ id: 'grid-th', slot: 4, n: 120, s: [0, rMax], z: (t) => [t * Math.cos(th), t * Math.sin(th)] }); }
      }
      if (view.unitCircle ?? params.unitCircle) out.push({ id: 'unit', slot: 'ink', dashed: true, n: 240, s: [0, TAU], z: (t) => [Math.cos(t), Math.sin(t)] });
      /* curves: [{ id, z: "formula in t", t: [from, to], colour, dashed, n }] (the formula may use the params too) */
      (view.curves || params.curves || []).forEach((cv, i) => {
        if (!cv || cv.z == null) return;
        const names = ['t', ...Object.keys(fo.vals)];
        let fn; try { fn = compile(String(cv.z), names); } catch (e) { if (!warned.has(cv.z)) { warned.add(cv.z); console.warn('complex-map curve: ' + e.message); } return; }
        const env = { ...fo.vals }, t = Array.isArray(cv.t) ? cv.t : [0, 1];
        out.push({ id: cv.id || 'c' + i, slot: cv.colour ?? 5 + (i % 2), dashed: cv.dashed, n: cv.n || 240, s: [+t[0], +t[1]], z: (s) => { env.t = [s, 0]; return fn(env); } });
      });
      return out;
    };

    let cache = { key: '', paths: [] };
    const pathsFor = (view, fo, g) => {
      const key = JSON.stringify([fo.src, fo.vals, g.key, view.grid ?? params.grid, view.gridStep ?? params.gridStep, view.rStep ?? params.rStep, view.rays ?? params.rays, view.unitCircle ?? params.unitCircle, view.curves || params.curves]);
      if (cache.key === key) return cache.paths;
      const paths = curvesOf(view, fo, g).map((c) => ({ ...c, dz: pathOf(c.z, c.s[0], c.s[1], c.n, null, g.z), dw: pathOf(c.z, c.s[0], c.s[1], c.n, fo.F, g.w) }));
      cache = { key, paths };
      return paths;
    };

    const imageLabel = (p) => (p.imageLabel != null ? String(p.imageLabel) : p.label ? (/^\$.*\$$/.test(p.label) ? `$f(${p.label.slice(1, -1)})$` : `f(${p.label})`) : '');
    const enabledFor = (R, id) => R.mode === 'drag' && Array.isArray(R.modeOpts && R.modeOpts.ids) && R.modeOpts.ids.includes(id);

    const def = {
      kind: 'complex-map', aria: params.aria || 'A complex function as a map from the z-plane to the w-plane',
      modes: ['drag', 'slider'],
      listKeys: ['points', 'curves'],
      size: () => { const g = layout(null); return { w: g.W, h: g.H }; },
      init: () => ({ points: (params.points || []).map((p, i) => ({ ...p, id: p.id || 'p' + i })), hide: [], highlight: [], selected: [] }),
      destroy: () => { if (watch) watch.disconnect(); },
      render(view, R) {
        const g = layout(R); geo = g;
        if (R.F.w !== g.W || R.F.h !== g.H) R.F.resize(g.W, g.H);
        if (!watch && typeof ResizeObserver === 'function') {
          let lastKey = g.key;
          watch = new ResizeObserver(() => { const k = layout(R).key; if (k !== lastKey) { lastKey = k; R.redraw(); } });
          watch.observe(R.F.wrap);
        }
        const root = R.F.g, fo = fOf(view), hide = new Set([].concat(view.hide || []));
        if (fo.error && !warned.has(fo.src)) { warned.add(fo.src); console.warn('complex-map: ' + fo.error); }
        const pl = [['z', g.z], ['w', g.w]];
        const planes = {};
        for (const [key, P] of pl) {
          const pg = svg('g'); root.append(pg);
          pg.append(svg('rect', { x: P.x0, y: P.y0, width: P.w, height: P.h, class: 'cvb-axis thin', fill: 'none', rx: 2 }));
          const inner = svg('g', { 'clip-path': R.clipRect(P.x0, P.y0, P.w, P.h, key) });
          pg.append(inner); // axes and their haloed tick labels go above the grid and curves, so a minus sign is never hidden
          K.planeAxes(pg, P.sx, P.sy, { grid: false, xLabel: params.xLabel ?? 'Re', yLabel: params.yLabel ?? 'Im' });
          const title = key === 'z' ? (params.zLabel ?? 'z-plane') : (params.wLabel ?? 'w-plane');
          pg.append(K.lab(P.x0 + 2, P.y0 - 13, title, { anchor: 'start', cls: 'cvb-strong', halo: true, w: P.w }));
          planes[key] = { P, inner, over: svg('g') };
        }
        /* grid, unit circle and curves: the same samples in z (as drawn) and through f (as mapped) */
        if (!fo.error) {
          const byId = new Map();
          for (const c of pathsFor(view, fo, g)) {
            if (hide.has(c.id)) continue;
            for (const key of ['z', 'w']) {
              const d = key === 'z' ? c.dz : c.dw; if (!d) continue;
              let o = byId.get(key + c.id);
              if (!o) { o = K.obj(c.id, '', c.slot); planes[key].inner.append(o); byId.set(key + c.id, o); }
              o.append(svg('path', { d, class: 'cvb-ln thin' + (c.dashed ? ' cvb-dash' : ''), style: c.id.startsWith('grid') ? 'opacity: 0.8; stroke-width: 1.4px' : c.dashed ? '' : 'stroke-width: 2.4px' }));
            }
          }
        } else {
          root.append(K.lab(g.w.x0 + g.w.w / 2, g.w.y0 + g.w.h / 2, 'Check f(z)', { cls: 'cvb-muted', halo: true }));
        }
        /* points: z where it is, f(z) where it goes (pinned hollow to the edge of the w-plane when it lands outside) */
        const labels = { z: [], w: [] };
        for (const p of view.points || []) {
          if (p.x == null || p.y == null || hide.has(p.id)) continue;
          const canDrag = (p.drag || enabledFor(R, p.id)) && R.active() && (R.mode == null || R.mode === 'drag' || R.mode === 'slider');
          const Pz = planes.z.P, zxp = Pz.sx(p.x), zyp = Pz.sy(p.y);
          const oz = K.obj(p.id, 'cvb-pt', p.drag ? 'manip' : (p.colour || 'ink'));
          oz.append(K.washCircle(zxp, zyp, p.drag ? 15 : 11));
          if (canDrag) oz.append(K.handle(zxp, zyp, p.id, { label: p.ariaLabel || `Point ${p.label || p.id}` }));
          else oz.append(svg('circle', { cx: zxp, cy: zyp, r: p.drag ? 7 : 4.5, class: 'cvb-dot' }));
          planes.z.over.append(oz);
          if (p.label) labels.z.push({ x: zxp + 10, y: zyp - 12, text: String(p.label), P: Pz });
          const w = fo.error ? null : fo.F([+p.x, +p.y]), Pw = planes.w.P;
          if (w && Number.isFinite(w[0]) && Number.isFinite(w[1])) {
            let X = Pw.sx(w[0]), Y = Pw.sy(w[1]), off = false;
            if (X < Pw.x0 || X > Pw.x1 || Y < Pw.y0 || Y > Pw.y1 || !Number.isFinite(X) || !Number.isFinite(Y)) { // slide along the line from the centre out to the edge
              off = true; const mx2 = Pw.x0 + Pw.w / 2, my2 = Pw.y0 + Pw.h / 2, dx = X - mx2, dy = Y - my2, t = Math.min((Pw.w / 2 - 6) / (Math.abs(dx) || 1e-9), (Pw.h / 2 - 6) / (Math.abs(dy) || 1e-9));
              X = mx2 + dx * Math.min(1, t); Y = my2 + dy * Math.min(1, t);
            }
            const ow = K.obj(p.id + '-image', 'cvb-pt', p.colour || (p.drag ? 'manip' : 'ink'));
            ow.append(K.washCircle(X, Y, 11), svg('circle', { cx: X, cy: Y, r: 5.5, class: 'cvb-dot' + (off ? ' open' : '') }));
            planes.w.over.append(ow);
            const lt = imageLabel(p); if (lt) labels.w.push({ x: X + 10, y: Y - 12, text: lt, P: Pw });
          }
        }
        for (const key of ['z', 'w']) {
          const { P, over } = planes[key];
          root.append(over);
          for (const l of labels[key]) { const anchor = l.x > P.x0 + P.w - 50 ? 'end' : 'start', x = anchor === 'end' ? l.x - 20 : l.x; over.append(K.lab(K.clamp(x, P.x0 + 4, P.x0 + P.w - 4), K.clamp(l.y, P.y0 + 10, P.y0 + P.h - 10), l.text, { anchor, halo: true, cls: 'cvb-strong' })); }
        }
      },
      drag: {
        start: (id, p, R) => { const pt = (R.state.points || []).find((q) => q.id === id); return pt && (pt.drag || enabledFor(R, id)) && R.active() ? { id } : null; },
        move(info, p, R, end) { if (geo) movePoint(R, info.id, geo.z.sx.invert(p.x), geo.z.sy.invert(p.y), end); },
        key(id, dx, dy, R) { const pt = (R.state.points || []).find((q) => q.id === id); if (!pt) return; const st = pt.snap || params.snap || niceStep((zx[1] - zx[0]) / 16); movePoint(R, id, pt.x + dx * st, pt.y + dy * st, true); },
      },
      methods: (R) => ({
        /* controls bind a number in state.params (named in f or in a curve) or a path such as points.p1.x */
        setParam: (name, v) => { const n = String(name); R.inst.set(n.includes('.') ? n.split('.').reduceRight((acc, k) => ({ [k]: acc }), +v) : { params: { [n]: +v } }, { instant: true }); },
        getParam: (name) => { const n = String(name); if (n.includes('.')) { let o = R.state; for (const k of n.split('.')) o = Array.isArray(o) && !/^\d+$/.test(k) ? o.find((q) => q && q.id === k) : o == null ? undefined : o[k]; return typeof o === 'number' ? o : undefined; } const v = (R.state.params || {})[n] ?? (params.params || {})[n]; return typeof v === 'number' ? v : undefined; },
        /* f(z) for a point or a complex number as [re, im] with the current f and params, for grading and captions */
        evaluate: (z) => { const fo = fOf(R.state), p = typeof z === 'string' ? (R.state.points || []).find((q) => q.id === z) : null, c = p ? [p.x, p.y] : z; return fo.F([+c[0], +c[1]]); },
        points: () => Object.fromEntries((R.state.points || []).filter((q) => q.drag || enabledFor(R, q.id)).map((q) => [q.id, { x: q.x, y: q.y }])),
        place: (id, pos, opts = {}) => { const [x, y] = Array.isArray(pos) ? pos : [pos, (R.state.points || []).find((q) => q.id === id)?.y ?? 0]; return R.inst.set({ points: { [id]: { x, y } } }, opts); },
      }),
    };

    const movePoint = (R, id, x, y, end) => {
      const pt = (R.state.points || []).find((q) => q.id === id); if (!pt) return;
      x = K.clamp(x, zx[0], zx[1]); y = K.clamp(y, zy[0], zy[1]);
      const sn = pt.snap || params.snap; if (sn) { x = K.snapTo(x, sn); y = K.snapTo(y, sn); }
      x = K.round(x, 6); y = K.round(y, 6);
      R.commit({ points: { [id]: { x, y } } });
      R.emit({ type: 'drag', id, x, y, phase: end ? 'end' : 'move' });
    };

    const inst = K.make(host, params, ctx, def);
    /* derive reads the image: each point in get() carries u and v, the real and imaginary parts of f(z) at the point
       (p1.u, p1.v), worked out from the current f and params. The state itself is untouched. */
    const baseGet = inst.get;
    inst.get = () => {
      const st = baseGet(); if (!Array.isArray(st.points) || !st.points.length) return st;
      const fo = fOf(st); if (fo.error) return st;
      st.points = st.points.map((p) => { if (p == null || p.x == null || p.y == null) return p; const w = fo.F([+p.x, +p.y]); return { ...p, u: w[0], v: w[1] }; });
      return st;
    };
    return inst;
  });
})();
