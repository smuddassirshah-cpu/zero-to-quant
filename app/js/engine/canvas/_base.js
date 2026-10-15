/* Canvas base: registry and shared SVG helpers for every diagram kind (docs/PLAN.md section 9).
   Loaded after core.js. Each canvas file calls ZQ.canvas.register(kind, factory).
   factory(host, params, ctx) -> { el, set(patch), get(), highlight(ids, on), clone(host2), on(ev, fn), enable(mode), destroy() } */
(function () {
  'use strict';
  const Z = window.ZQ;
  const NS = 'http://www.w3.org/2000/svg';

  /* Diagram palette (design-research 2.6). Series slots are assigned in order and never cycle. */
  const SERIES = ['var(--s1)', 'var(--s2)', 'var(--s3)', 'var(--s4)', 'var(--s5)', 'var(--s6)'];
  const INK = {
    primary: 'var(--ink)', muted: 'var(--text-muted)', grid: 'var(--grid)', axis: 'var(--axis)',
    movable: 'var(--manip)', target: 'var(--ink)', wash: 'var(--pear-200)', correct: 'var(--green-strong)', notyet: 'var(--amber-text)', reveal: 'var(--hint)',
    surface: 'var(--bg-surface)', canvas: 'var(--bg-canvas)',
  };
  const series = (i) => SERIES[Math.min(i, SERIES.length - 1)];

  /* Element creation: svg('circle', { cx: 1, cy: 2, r: 3, class: 'x' }, [children]) */
  const svg = (tag, attrs = {}, children = []) => {
    const el = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) if (v != null && v !== false) el.setAttribute(k, v === true ? '' : v);
    for (const c of [].concat(children)) if (c != null) el.append(typeof c === 'string' ? document.createTextNode(c) : c);
    return el;
  };
  const attrs = (el, a) => { for (const [k, v] of Object.entries(a)) if (v == null || v === false) el.removeAttribute(k); else el.setAttribute(k, v === true ? '' : v); return el; };
  /* Text with KaTeX: foreignObject holding a rendered formula, sized to its box. Plain text uses <text>. */
  const label = (x, y, text, { anchor = 'middle', cls = '', size = 13, tex = false, w = 80, h = 24, baseline = 'middle' } = {}) => {
    if (!tex) return svg('text', { x, y, 'text-anchor': anchor, 'dominant-baseline': baseline, class: 'cv-label ' + cls, 'font-size': size }, [text]);
    const fo = svg('foreignObject', { x: anchor === 'middle' ? x - w / 2 : anchor === 'end' ? x - w : x, y: y - h / 2, width: w, height: h, class: 'cv-fo ' + cls });
    const div = document.createElement('div'); div.className = 'cv-fo-in'; div.style.textAlign = anchor === 'middle' ? 'center' : anchor === 'end' ? 'right' : 'left';
    div.innerHTML = Z.tex(text); fo.append(div); return fo;
  };

  /* Linear scales: scale([d0, d1], [r0, r1]) -> fn with .invert */
  const scale = (domain, range) => {
    const [d0, d1] = domain, [r0, r1] = range, k = (r1 - r0) / ((d1 - d0) || 1);
    const f = (v) => r0 + (v - d0) * k; f.invert = (p) => d0 + (p - r0) / k; f.domain = domain; f.range = range; return f;
  };
  const niceTicks = (min, max, n = 6) => {
    const span = max - min || 1, raw = span / n, mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const step = [1, 2, 2.5, 5, 10].map(m => m * mag).find(s => span / s <= n) || mag * 10;
    const out = []; for (let v = Math.ceil(min / step) * step; v <= max + 1e-9; v += step) out.push(+v.toFixed(10)); return out;
  };
  const fmtNum = (v, dp = 2) => Number.isInteger(v) ? String(v) : (+v.toFixed(dp)).toString();

  /* Expression evaluation for plane functions: 'x^2 + a*x' with params. Safe subset: numbers, x, params, + - * / ^, functions. */
  const FN = { sin: Math.sin, cos: Math.cos, tan: Math.tan, exp: Math.exp, ln: Math.log, log: Math.log, log10: Math.log10, sqrt: Math.sqrt, abs: Math.abs, max: Math.max, min: Math.min, floor: Math.floor, ceil: Math.ceil, pow: Math.pow, pi: Math.PI, e: Math.E, atan: Math.atan, asin: Math.asin, acos: Math.acos, sinh: Math.sinh, cosh: Math.cosh, tanh: Math.tanh, sign: Math.sign, round: Math.round };
  const compile = (expr, paramNames = []) => {
    const src = String(expr).replace(/\^/g, '**').replace(/\b(sin|cos|tan|exp|ln|log10|log|sqrt|abs|max|min|floor|ceil|pow|pi|atan|asin|acos|sinh|cosh|tanh|sign|round)\b(?!\s*[:\w])/g, 'F.$1').replace(/\bF\.e\b/g, 'F.e');
    if (/[^\w\s+\-*/().,<>=?:!&|%]/.test(src.replace(/F\./g, ''))) throw new Error('Bad expression: ' + expr);
    // eslint-disable-next-line no-new-func
    const f = new Function('F', 'x', ...paramNames, 'return (' + src + ');');
    return (x, params = {}) => { try { const v = f(FN, x, ...paramNames.map(n => params[n])); return Number.isFinite(v) ? v : NaN; } catch { return NaN; } };
  };

  /* Animation: tween a number over ms with ease-morph, calling fn(v) each frame. Honour reduced motion. */
  const ease = { standard: (t) => 1 - Math.pow(1 - t, 3), morph: (t) => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2 };
  const tween = (from, to, ms, fn, easing = 'morph') => new Promise(res => {
    if (Z.reducedMotion() || ms <= 0 || from === to) { fn(to); return res(); }
    let t0 = null; const e = ease[easing] || ease.morph;
    const step = (now) => { if (t0 === null) t0 = now; const p = Math.min(1, (now - t0) / ms); fn(from + (to - from) * e(p)); if (p < 1) requestAnimationFrame(step); else res(); };
    requestAnimationFrame(step);
  });
  /* Pulse a pear wash and ink ring on an element twice (hint rung 2, 'point'). */
  const pulse = (el, times = 2) => {
    if (!el) return Promise.resolve();
    el.classList.add('cv-hl');
    if (Z.reducedMotion()) return Promise.resolve();
    return new Promise(res => { let i = 0; const tick = () => { el.classList.toggle('cv-hl-on', i % 2 === 0); i++; if (i < times * 2) setTimeout(tick, 220); else res(); }; tick(); });
  };
  const clearHighlight = (root) => root.querySelectorAll('.cv-hl').forEach(n => n.classList.remove('cv-hl', 'cv-hl-on'));

  /* Deep merge for state patches (arrays replace, objects merge). */
  const merge = (base, patch) => {
    if (patch == null) return base;
    const out = { ...base };
    for (const [k, v] of Object.entries(patch)) out[k] = (v && typeof v === 'object' && !Array.isArray(v) && base[k] && typeof base[k] === 'object' && !Array.isArray(base[k])) ? merge(base[k], v) : v;
    return out;
  };

  /* Frame: a responsive SVG in the 540px column. frame(host, w, h) -> { svg, g } with a caption slot. */
  const frame = (host, w, h, { cls = '', label: aria = 'Diagram' } = {}) => {
    const wrap = document.createElement('div'); wrap.className = 'cv ' + cls;
    const s = svg('svg', { viewBox: `0 0 ${w} ${h}`, width: '100%', role: 'img', 'aria-label': aria, class: 'cv-svg' });
    const g = svg('g'); s.append(g);
    const cap = document.createElement('div'); cap.className = 't-caption cv-caption'; cap.hidden = true;
    wrap.append(s, cap); host.append(wrap);
    return { wrap, svg: s, g, caption: (t) => { cap.hidden = !t; cap.innerHTML = t ? Z.md(t) : ''; }, w, h };
  };

  /* Event emitter mixin */
  const emitter = () => { const L = {}; return { on: (e, f) => { (L[e] = L[e] || []).push(f); }, emit: (e, d) => (L[e] || []).forEach(f => f(d)) }; };

  /* Registry */
  const kinds = {};
  const register = (kind, factory) => { kinds[kind] = factory; };
  const create = (host, spec, ctx = {}) => {
    const f = kinds[spec.kind];
    if (!f) { host.append(Z.h(`<div class="cv cv-missing t-caption">Canvas "${Z.esc(spec.kind)}" is not available.</div>`)); return null; }
    const inst = f(host, spec.params || {}, { ...ctx, Z, initial: spec.state || {} });
    if (spec.state) inst.set(spec.state, { instant: true });
    if (spec.state && spec.state.caption && inst.caption) inst.caption(spec.state.caption);
    return inst;
  };

  Z.canvas = { register, create, kinds, svg, attrs, label, scale, niceTicks, fmtNum, compile, tween, pulse, clearHighlight, merge, frame, emitter, series, SERIES, INK, NS };
})();
