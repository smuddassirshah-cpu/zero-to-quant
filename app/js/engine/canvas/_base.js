/* Canvas base: registry and shared SVG helpers for every diagram kind (docs/PLAN.md section 9).
   Loaded after core.js. Each canvas file calls ZQ.canvas.register(kind, factory).
   factory(host, params, ctx) -> { el, set(patch), get(), highlight(ids, on), clone(host2), on(ev, fn), enable(mode), destroy() }

   Shared contract every canvas built on ZQ.canvas.instance() also honours (see engine/canvas/README.md):
   - set(patch, { instant }) merges with ZQ.canvas.merge and animates over 480 to 800ms unless instant or reduced motion.
   - Every id-bearing element carries class `cv-obj` and `data-id`. Tappable ones also carry `data-tap`.
   - Graded classes `is-correct`, `is-notyet`, `is-reveal`, `is-dim` go on `.cv-obj` elements. Widgets should apply them
     through canvas.mark(ids, cls, on) so they survive redraws; canvas.unmark(cls?) clears one class or all four.
   - state.selected: [ids] is the tap selection. enable('tap', { max, only }) lets the learner toggle it; the canvas emits
     'change' with { selected, id, on }. Space toggles, arrow keys move a roving focus, Enter is left for the player.
   - state.highlight: [ids] and highlight(ids, on) pulse a pear wash and a 2px ink ring twice; off clears.
   - state.caption shows under the drawing.
   - flash(ids, { ms = 150, times = 2 }) flashes amber for show-why; unflash() clears what reduced motion left on.
   - lock(on) stops tap and drag input while the player evaluates.
   - Drag canvases emit 'change' with { id, x, y, phase: 'move' | 'end' } in canvas units and expose
     points() -> { id: { x, y } } and place(id, pos, { instant }) where pos is a number (1D) or [x, y].
   - ctx.static (or ctx.mode 'static', as the player's explanation modal passes) means a still copy: no interaction, no timed fades.
   - Explore controls call canvas.setParam(name, value) when it exists (and getParam(name) for their opening value).
   - canvas.derive (any kind, applied by create()): linked values and live captions; see attachDerive below. */
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

  /* Maths detection for labels: "$...$" is TeX, "3/5" becomes \dfrac{3}{5}, anything with a backslash is TeX. */
  const texOf = (v) => {
    if (v == null) return { tex: false, src: '' };
    const s = String(v).trim();
    let m = s.match(/^\$([^$]+)\$$/); if (m) return { tex: true, src: m[1] };
    m = s.match(/^(-?)(\d+(?:\.\d+)?)\s*\/\s*(\d+(?:\.\d+)?)$/); if (m) return { tex: true, src: `${m[1]}\\dfrac{${m[2]}}{${m[3]}}` };
    if (/\$[^$]+\$/.test(s)) return { tex: true, md: true, src: s }; // text with inline maths
    if (s.includes('\\')) return { tex: true, src: s };
    return { tex: false, src: s };
  };
  /* Rough text width for Archivo at a given size, for sizing pills and boxes before layout. */
  const textW = (s, size = 13, weight = 500) => {
    let w = 0;
    for (const ch of String(s)) w += /[il.,:;'|!]/.test(ch) ? 0.28 : /[mwMW]/.test(ch) ? 0.86 : /[A-Z0-9]/.test(ch) ? 0.64 : ch === ' ' ? 0.27 : 0.54;
    return w * size * (weight >= 700 ? 1.06 : 1);
  };

  /* Text with KaTeX: foreignObject holding a rendered formula, sized to its box. Plain text uses <text>.
     tex: 'auto' decides with texOf(), so "3/5" renders as a fraction and "Red" as text. */
  const label = (x, y, text, { anchor = 'middle', cls = '', size = 13, tex = false, w = 80, h = 24, baseline = 'middle' } = {}) => {
    let md = false;
    if (tex === 'auto') { const t = texOf(text); tex = t.tex; md = !!t.md; text = t.src; if (tex && /frac/.test(text)) h = Math.max(h, 36); }
    if (!tex) return svg('text', { x, y, 'text-anchor': anchor, 'dominant-baseline': baseline, class: 'cv-label ' + cls, 'font-size': size }, [String(text)]);
    const fo = svg('foreignObject', { x: anchor === 'middle' ? x - w / 2 : anchor === 'end' ? x - w : x, y: y - h / 2, width: w, height: h, class: 'cv-fo ' + cls });
    const div = document.createElement('div'); div.className = 'cv-fo-in'; div.style.textAlign = anchor === 'middle' ? 'center' : anchor === 'end' ? 'right' : 'left'; div.style.justifyContent = anchor === 'middle' ? 'center' : anchor === 'end' ? 'flex-end' : 'flex-start';
    div.innerHTML = md ? `<span>${Z.md(text)}</span>` : Z.tex(text); fo.append(div); return fo;
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

  /* Animation: tween a number over ms with ease-morph, calling fn(v) each frame. Honour reduced motion.
     Springs (design-research 4.3) are sampled from their CSS linear() approximations. */
  const sampled = (pts) => (t) => { if (t <= 0) return 0; if (t >= 1) return 1; const x = t * (pts.length - 1), i = Math.floor(x); return pts[i] + (pts[i + 1] - pts[i]) * (x - i); };
  const ease = {
    standard: (t) => 1 - Math.pow(1 - t, 3), morph: (t) => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2, linear: (t) => t,
    snap: sampled([0, 0.069, 0.214, 0.379, 0.533, 0.662, 0.764, 0.841, 0.897, 0.936, 0.962, 0.979, 0.990, 0.996, 0.999, 1]),
    bounce: sampled([0, 0.121, 0.366, 0.618, 0.818, 0.952, 1.026, 1.055, 1.057, 1.046, 1.031, 1.017, 1.007, 1.001, 0.998, 0.997, 1]),
    physical: sampled([0, 0.131, 0.407, 0.698, 0.927, 1.068, 1.129, 1.131, 1.101, 1.061, 1.025, 0.999, 0.986, 0.982, 0.984, 0.989, 1]),
  };
  const tween = (from, to, ms, fn, easing = 'morph') => new Promise(res => {
    if (Z.reducedMotion() || ms <= 0 || from === to) { fn(to); return res(); }
    let t0 = null; const e = ease[easing] || ease.morph;
    const step = (now) => { if (t0 === null) t0 = now; const p = Math.min(1, (now - t0) / ms); fn(from + (to - from) * e(p)); if (p < 1) requestAnimationFrame(step); else res(); };
    requestAnimationFrame(step);
  });
  /* A cancellable progress animation: run(ms, fn(eased, raw), easing) stops the previous run of the same animator. */
  const animator = () => {
    let id = 0, raf = 0;
    return {
      run(ms, fn, easing = 'morph') {
        const my = ++id; cancelAnimationFrame(raf);
        if (Z.reducedMotion() || ms <= 0) { fn(1, 1); return Promise.resolve(); }
        const e = ease[easing] || ease.morph; let t0 = null;
        return new Promise(res => {
          const step = (now) => { if (my !== id) return res(); if (t0 === null) t0 = now; const p = Math.min(1, (now - t0) / ms); fn(e(p), p); if (p < 1) raf = requestAnimationFrame(step); else res(); };
          raf = requestAnimationFrame(step);
        });
      },
      stop() { id++; cancelAnimationFrame(raf); },
    };
  };
  const lerp = (a, b, t) => a + (b - a) * t;

  /* Pulse a pear wash and ink ring on an element twice (hint rung 2, 'point'). */
  const pulse = (el, times = 2) => {
    if (!el) return Promise.resolve();
    el.classList.add('cv-hl');
    if (Z.reducedMotion()) return Promise.resolve();
    return new Promise(res => { let i = 0; const tick = () => { el.classList.toggle('cv-hl-on', i % 2 === 0); i++; if (i < times * 2) setTimeout(tick, 220); else res(); }; tick(); });
  };
  const clearHighlight = (root) => root.querySelectorAll('.cv-hl').forEach(n => n.classList.remove('cv-hl', 'cv-hl-on'));
  /* Show-why flash: toggles cls on the elements `times` times at `ms` intervals. Under reduced motion it applies once and stays. */
  const flash = (els, { cls = 'is-flash', ms = 150, times = 2 } = {}) => {
    els = [].concat(els).filter(Boolean);
    if (Z.reducedMotion()) { els.forEach(n => n.classList.add(cls)); return Promise.resolve(); }
    return new Promise(res => { let i = 0; const tick = () => { const on = i % 2 === 0; els.forEach(n => n.classList.toggle(cls, on)); i++; if (i < times * 2) setTimeout(tick, ms); else res(); }; tick(); });
  };

  /* Deep merge for state patches (arrays replace, objects merge). A keyed patch for a list of items with ids,
     { "points": { "p1": { "x": 3 } } }, merges into the item with that id (an unknown id is appended), so explain.canvas,
     option canvas patches and demonstrate steps can move one item without wiping the list, on every kind. */
  const isPlain = (v) => v && typeof v === 'object' && !Array.isArray(v);
  const keyedList = (list, map) => list.map(it => (it && it.id != null && isPlain(map[it.id]) ? merge(it, map[it.id]) : it))
    .concat(Object.entries(map).filter(([id, v]) => isPlain(v) && !list.some(it => it && it.id === id)).map(([id, v]) => ({ id, ...v })));
  const merge = (base, patch) => {
    if (patch == null) return base;
    const out = { ...base };
    for (const [k, v] of Object.entries(patch)) {
      const b = base ? base[k] : undefined;
      if (isPlain(v) && Array.isArray(b) && Object.values(v).every(isPlain) && b.every(it => isPlain(it) && it.id != null)) out[k] = keyedList(b, v);
      else out[k] = (isPlain(v) && isPlain(b)) ? merge(b, v) : v;
    }
    return out;
  };

  /* Frame: a responsive SVG in the 540px column. frame(host, w, h) -> { svg, g } with a caption slot.
     fit: true caps the drawing at its natural width (w px) and centres it, for drawings narrower than the column. */
  const frame = (host, w, h, { cls = '', label: aria = 'Diagram', fit = false } = {}) => {
    const wrap = document.createElement('div'); wrap.className = 'cv ' + cls;
    const s = svg('svg', { viewBox: `0 0 ${w} ${h}`, width: '100%', role: 'img', 'aria-label': aria, class: 'cv-svg' });
    if (fit) s.style.maxWidth = w + 'px';
    const g = svg('g'); s.append(g);
    const cap = document.createElement('div'); cap.className = 't-caption cv-caption'; cap.hidden = true;
    wrap.append(s, cap); host.append(wrap);
    const fr = { wrap, svg: s, g, caption: (t) => { cap.hidden = !t; cap.innerHTML = t ? Z.md(t) : ''; }, w, h };
    fr.resize = (w2, h2) => { fr.w = w2; fr.h = h2; s.setAttribute('viewBox', `0 0 ${w2} ${h2}`); if (fit) s.style.maxWidth = w2 + 'px'; };
    return fr;
  };

  /* Event emitter mixin */
  const emitter = () => { const L = {}; return { on: (e, f) => { (L[e] = L[e] || []).push(f); return () => { L[e] = (L[e] || []).filter(x => x !== f); }; }, emit: (e, d) => (L[e] || []).forEach(f => f(d)) }; };

  /* ---------- Geometry helpers ---------- */
  /* Client coordinates to the SVG's viewBox units. */
  const toLocal = (svgEl, cx, cy) => {
    const m = svgEl.getScreenCTM(); if (!m) return { x: 0, y: 0 };
    const p = new DOMPoint(cx, cy).matrixTransform(m.inverse()); return { x: p.x, y: p.y };
  };
  /* Pointer drag on a handle: start(p, e) may return false to refuse; move(p, e) every frame; end(p, e) on release. */
  const dragger = (handle, svgEl, { start, move, end } = {}) => {
    const down = (e) => {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      const p0 = toLocal(svgEl, e.clientX, e.clientY);
      if (start && start(p0, e) === false) return;
      e.preventDefault();
      try { handle.setPointerCapture(e.pointerId); } catch { /* capture unsupported for this pointer */ }
      const mv = (ev) => move && move(toLocal(svgEl, ev.clientX, ev.clientY), ev);
      const up = (ev) => {
        handle.removeEventListener('pointermove', mv); handle.removeEventListener('pointerup', up); handle.removeEventListener('pointercancel', up);
        end && end(toLocal(svgEl, ev.clientX, ev.clientY), ev);
      };
      handle.addEventListener('pointermove', mv); handle.addEventListener('pointerup', up); handle.addEventListener('pointercancel', up);
    };
    handle.addEventListener('pointerdown', down);
    return () => handle.removeEventListener('pointerdown', down);
  };
  /* Union outline of a set of grid cells as one closed path (several subpaths if the set is not connected).
     cells: [[row, col], ...] zero-based; X(col) and Y(row) map lattice lines to pixels (lines sit in the gutters). */
  const cellOutline = (cells, X, Y) => {
    const has = new Set(cells.map(([r, c]) => r + ',' + c));
    const out = new Map(); const add = (a, b) => { const k = a.join(','); (out.get(k) || out.set(k, []).get(k)).push({ a, b, used: false }); };
    for (const [r, c] of cells) {
      if (!has.has((r - 1) + ',' + c)) add([c, r], [c + 1, r]);
      if (!has.has(r + ',' + (c + 1))) add([c + 1, r], [c + 1, r + 1]);
      if (!has.has((r + 1) + ',' + c)) add([c + 1, r + 1], [c, r + 1]);
      if (!has.has(r + ',' + (c - 1))) add([c, r + 1], [c, r]);
    }
    const loops = [];
    for (const list of out.values()) for (const e0 of list) {
      if (e0.used) continue;
      const pts = [e0.a]; let e = e0;
      while (e && !e.used) {
        e.used = true; pts.push(e.b);
        const nexts = (out.get(e.b.join(',')) || []).filter(x => !x.used);
        if (nexts.length > 1) { // pinch point where cells touch at a corner: keep turning right so loops stay simple
          const dx = e.b[0] - e.a[0], dy = e.b[1] - e.a[1];
          nexts.sort((p, q) => ((q.b[0] - q.a[0]) * dy - (q.b[1] - q.a[1]) * dx) - ((p.b[0] - p.a[0]) * dy - (p.b[1] - p.a[1]) * dx));
        }
        e = nexts[0];
      }
      const simple = pts.filter((p, i) => { if (i === 0 || i === pts.length - 1) return true; const a = pts[i - 1], b = pts[i + 1]; return !((a[0] === p[0] && p[0] === b[0]) || (a[1] === p[1] && p[1] === b[1])); });
      if (simple.length > 2 && simple[0][0] === simple[simple.length - 1][0] && simple[0][1] === simple[simple.length - 1][1]) simple.pop();
      // drop the start point too if it is collinear with its neighbours
      if (simple.length > 3) { const a = simple[simple.length - 1], p = simple[0], b = simple[1]; if ((a[0] === p[0] && p[0] === b[0]) || (a[1] === p[1] && p[1] === b[1])) simple.shift(); }
      loops.push(simple);
    }
    const r = (v) => Math.round(v * 100) / 100;
    return loops.map(l => 'M' + l.map(([c, rr]) => `${r(X(c))} ${r(Y(rr))}`).join('L') + 'Z').join('');
  };

  /* Roving focus: the item nearest in the arrow's direction, preferring items in line with the current one. */
  const DIRS = { ArrowRight: [1, 0], ArrowLeft: [-1, 0], ArrowDown: [0, 1], ArrowUp: [0, -1] };
  const centre = (n) => { const r = n.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; };
  const nextInDirection = (items, cur, key) => {
    const d = DIRS[key]; if (!d || !cur) return null;
    const c = centre(cur); let best = null, bs = Infinity;
    for (const n of items) {
      if (n === cur) continue;
      const p = centre(n), dx = p.x - c.x, dy = p.y - c.y, along = dx * d[0] + dy * d[1];
      if (along <= 2) continue;
      const s = along + Math.abs(dx * d[1] + dy * d[0]) * 3;
      if (s < bs) { bs = s; best = n; }
    }
    return best;
  };

  /* Cross badge on a not-yet answer object (design-research 4.5), top-right of its body. */
  const badge = (obj, type = 'cross') => {
    if (!obj || obj.querySelector(':scope > .cv-badge')) return;
    if (!(obj instanceof SVGElement)) { const b = document.createElement('span'); b.className = 'cv-badge cv-badge-' + type; b.setAttribute('aria-hidden', 'true'); b.innerHTML = Z.icon(type === 'check' ? 'check' : 'cross'); obj.append(b); return; }
    const body = obj.querySelector('.cv-body') || obj;
    let bb, m; try { bb = body.getBBox(); m = obj.getCTM().inverse().multiply(body.getCTM()); } catch { return; }
    if (!bb.width && !bb.height) return;
    const corner = new DOMPoint(bb.x + bb.width - 2, bb.y + 2).matrixTransform(m), x = corner.x, y = corner.y;
    obj.append(svg('g', { class: 'cv-badge cv-badge-' + type, transform: `translate(${x} ${y})`, 'aria-hidden': 'true' }, [
      svg('circle', { r: 9 }), svg('path', { d: type === 'check' ? 'M-4 0.5l2.8 2.8L4.2-3.2' : 'M-3.5-3.5l7 7M3.5-3.5l-7 7' }),
    ]));
    // raise the object so the badge is not covered by a later sibling (focus is never on a canvas object while grading)
    if (obj.parentNode && obj.parentNode.lastElementChild !== obj && document.activeElement !== obj) obj.parentNode.append(obj);
  };

  /* ---------- Shared instance ---------- */
  const GRADED = ['is-correct', 'is-notyet', 'is-reveal', 'is-dim'];
  /* instance(o) builds the PLAN section 9 object around a canvas's draw function.
     o: { kind, factory, params, ctx, fr: frame (or { wrap, caption }), defaults: initial state,
          draw(state, prev, { instant, ms, patch }): bring the drawing to `state` (animate unless instant),
          resolve(id) -> elements to highlight for an id (default: [data-id=id]),
          highlightIds(value) -> id list for a non-array state.highlight,
          onHighlight(ids, on, { instant }) -> true when the canvas drew the highlight itself,
          onEnable(mode, opts, prevMode) for modes other than 'tap', onDestroy(), ms (default 600) }
     Returns { api, emit, later, all, state(), setQuiet(patch), locked(), mode(), isStatic }. */
  const instance = (o) => {
    const fr = o.fr, ctx = o.ctx || {}, wrap = fr.wrap, ms = o.ms || 600;
    const em = emitter(), timers = new Set(), marks = new Map();
    let state = JSON.parse(JSON.stringify(o.defaults || {}));
    let mode = null, modeOpts = {}, locked = false, hlIds = [], instT = 0;
    const isStatic = !!(ctx.static || ctx.mode === 'static');
    wrap.classList.add('cv-' + o.kind);
    if (isStatic) wrap.classList.add('cv-static');
    const all = (id) => Array.from(wrap.querySelectorAll(`[data-id="${CSS.escape(String(id))}"]`));
    const resolve = (id) => (o.resolve ? o.resolve(id) : all(id));
    const later = (fn, t) => { const id = setTimeout(() => { timers.delete(id); fn(); }, t); timers.add(id); return id; };
    const tapItems = () => Array.from(wrap.querySelectorAll('[data-tap]')).filter(n => !modeOpts.only || modeOpts.only.includes(n.dataset.id));

    const applySelected = () => {
      const sel = new Set(state.selected || []);
      wrap.querySelectorAll('[data-tap]').forEach(n => { const on = sel.has(n.dataset.id); n.classList.toggle('is-on', on); if (mode === 'tap') n.setAttribute('aria-pressed', String(on)); });
    };
    const applyMarks = () => {
      wrap.querySelectorAll(GRADED.map(c => '.' + c).join(',')).forEach(n => n.classList.remove(...GRADED));
      wrap.querySelectorAll('.cv-badge').forEach(n => n.remove());
      for (const [cls, ids] of marks) for (const id of ids) all(id).forEach(n => { if (!n.classList.contains('cv-obj')) return; n.classList.add(cls); if (cls === 'is-notyet') badge(n, 'cross'); });
    };
    const normHl = (v) => (v == null ? [] : Array.isArray(v) ? v : o.highlightIds ? o.highlightIds(v) : []);
    const doHighlight = (ids, on, { instant = false } = {}) => {
      if (o.onHighlight && o.onHighlight(ids, on, { instant })) return;
      if (!on) { if (!ids || !ids.length) clearHighlight(wrap); else ids.flatMap(resolve).forEach(n => n.classList.remove('cv-hl', 'cv-hl-on')); return; }
      ids.flatMap(resolve).forEach(n => (instant || isStatic ? n.classList.add('cv-hl') : pulse(n)));
    };
    const setupTap = () => {
      if (mode !== 'tap') return;
      const items = tapItems();
      items.forEach(n => { if (!n.hasAttribute('role')) { n.setAttribute('role', 'button'); n.setAttribute('tabindex', '-1'); if (n.dataset.label) n.setAttribute('aria-label', n.dataset.label); } });
      if (items.length && !items.some(n => n.getAttribute('tabindex') === '0')) items[0].setAttribute('tabindex', '0');
    };
    const toggle = (id) => {
      let sel = (state.selected || []).slice(); const i = sel.indexOf(id);
      if (i >= 0) sel.splice(i, 1);
      else if (modeOpts.max === 1) sel = [id];
      else if (modeOpts.max && sel.length >= modeOpts.max) return;
      else sel.push(id);
      state = { ...state, selected: sel }; applySelected();
      if (Z.sound) Z.sound('tap');
      em.emit('change', { selected: sel.slice(), id, on: i < 0 });
    };
    wrap.addEventListener('click', (e) => {
      if (mode !== 'tap' || locked) return;
      const n = e.target.closest('[data-tap]'); if (!n || !wrap.contains(n)) return;
      if (modeOpts.only && !modeOpts.only.includes(n.dataset.id)) return;
      toggle(n.dataset.id);
    });
    wrap.addEventListener('keydown', (e) => {
      if (mode !== 'tap') return;
      const n = e.target.closest && e.target.closest('[data-tap]'); if (!n) return;
      if (e.key === ' ' || e.key === 'Spacebar') { e.preventDefault(); if (!locked) toggle(n.dataset.id); return; }
      const items = tapItems(), t = nextInDirection(items, n, e.key);
      if (DIRS[e.key]) { e.preventDefault(); if (t) { items.forEach(x => x.setAttribute('tabindex', '-1')); t.setAttribute('tabindex', '0'); t.focus(); } }
    });

    const api = {
      el: wrap, kind: o.kind, params: o.params,
      get: () => JSON.parse(JSON.stringify(state)),
      set(patch, { instant = false } = {}) {
        patch = patch || {};
        const prev = state; state = merge(state, patch);
        const quick = instant || isStatic || Z.reducedMotion();
        if (quick) { wrap.classList.add('cv-instant'); clearTimeout(instT); }
        try { o.draw(state, prev, { instant: quick, ms, patch }); } catch (err) { console.error(err); }
        fr.caption(state.caption || '');
        setupTap(); applySelected(); applyMarks();
        if ('highlight' in patch) { doHighlight(hlIds, false); hlIds = normHl(patch.highlight); if (hlIds.length) doHighlight(hlIds, true, { instant: quick }); }
        else if (hlIds.length) hlIds.flatMap(resolve).forEach(n => n.classList.add('cv-hl'));
        if (quick) instT = setTimeout(() => wrap.classList.remove('cv-instant'), 40);
        return api;
      },
      highlight(ids, on = true) { doHighlight(normHl(ids), on); return api; },
      flash(ids, opts) { return flash([].concat(ids || []).flatMap(all).filter(n => n.classList.contains('cv-obj')), opts); },
      unflash() { wrap.querySelectorAll('.is-flash').forEach(n => n.classList.remove('is-flash')); },
      mark(ids, cls, on = true) {
        if (!marks.has(cls)) marks.set(cls, new Set());
        [].concat(ids || []).forEach(id => (on ? marks.get(cls).add(id) : marks.get(cls).delete(id)));
        applyMarks(); return api;
      },
      unmark(cls) { if (cls) marks.delete(cls); else marks.clear(); applyMarks(); return api; },
      marks: () => Object.fromEntries([...marks].map(([k, v]) => [k, [...v]])),
      caption(t) { fr.caption(t || ''); },
      on: (ev, fn) => em.on(ev, fn),
      enable(m, opts = {}) {
        if (isStatic) return api;
        const prevMode = mode;
        mode = m && m !== 'none' ? m : null; modeOpts = opts || {};
        wrap.classList.toggle('cv-tap', mode === 'tap');
        wrap.classList.toggle('cv-drag', mode === 'drag');
        wrap.querySelectorAll('[data-tap]').forEach(n => { n.removeAttribute('tabindex'); n.removeAttribute('role'); n.removeAttribute('aria-pressed'); n.removeAttribute('aria-label'); });
        setupTap(); applySelected();
        if (o.onEnable) o.onEnable(mode, modeOpts, prevMode);
        return api;
      },
      lock(on = true) { locked = !!on; wrap.classList.toggle('cv-locked', locked); return api; },
      clone(host2) {
        const c = o.factory(host2, o.params, { ...ctx, static: true });
        c.set(api.get(), { instant: true });
        for (const [cls, ids] of marks) if (c.mark) c.mark([...ids], cls);
        return c;
      },
      destroy() { timers.forEach(clearTimeout); timers.clear(); clearTimeout(instT); mode = null; if (o.onDestroy) o.onDestroy(); wrap.remove(); },
    };
    return {
      api, emit: em.emit, later, all,
      state: () => state,
      setQuiet: (patch) => { state = merge(state, patch); },
      locked: () => locked, mode: () => mode, modeOpts: () => modeOpts, isStatic, ms,
    };
  };

  /* Linked state: canvas.derive maps a target to an expression, re-evaluated after every state change and learner
     interaction, so one value follows another or a caption reads a live number.
       "derive": { "p2.x": "0.8 * p1.x", "values.7": "10 - values['3']", "params.b": "2 * a",
                   "caption": "Change: {{round((p1.x / 50 - 1) * 100, 1)}}%" }
     Targets: "<id>.<prop>" for an item with that id in any state list (points, intervals, arrows, markers, vectors,
     segments, pointers...), "values.<key>" (bars), "params.<name>", "caption" or any other state key or dotted path.
     Expressions are arithmetic over: item ids (p1.x, p1.y), state.params and params.params names, top-level numeric
     state keys (angle, ran), `values` (bars heights by label and id), and abs, min, max, sqrt, pow, exp, log, floor,
     ceil, round(v, places), pi. A caption (or any string target) fills each {{expression}}. */
  const DERIVE_FN = { abs: Math.abs, min: Math.min, max: Math.max, sqrt: Math.sqrt, pow: Math.pow, exp: Math.exp, log: Math.log, ln: Math.log, floor: Math.floor, ceil: Math.ceil, sign: Math.sign, pi: Math.PI, round: (v, d = 0) => +(+v).toFixed(d) };
  const deriveCache = {};
  const deriveExpr = (src) => {
    if (deriveCache[src]) return deriveCache[src];
    if (/[;`{}]|=>|\bfunction\b|\bnew\b|\bthis\b|(^|[^=!<>])=(?!=)/.test(src)) throw new Error('derive: not an expression: ' + src);
    // eslint-disable-next-line no-new-func
    const f = new Function('S', 'with (S) { return (' + src + '); }');
    return (deriveCache[src] = f);
  };
  const attachDerive = (inst, spec) => {
    const rules = Object.entries(spec.derive || {});
    if (!rules.length || !inst || !inst.set) return;
    const rawSet = inst.set.bind(inst);
    const scope = () => {
      const st = inst.get ? inst.get() : {}, S = Object.assign({}, DERIVE_FN);
      Object.entries(st).forEach(([k, v]) => { if (typeof v === 'number') S[k] = v; });
      Object.assign(S, (spec.params || {}).params || {}, st.params || {});
      const vals = Object.assign({}, st.values || {}); try { if (typeof inst.values === 'function') Object.assign(vals, inst.values() || {}); } catch { /* no heights */ }
      S.values = vals;
      Object.values(st).forEach(v => { if (Array.isArray(v)) v.forEach(it => { if (it && typeof it === 'object' && it.id != null && /^[A-Za-z_$][\w$]*$/.test(it.id)) S[it.id] = it; }); });
      return S;
    };
    const evalOne = (expr, S) => {
      if (typeof expr !== 'string') return expr;
      if (expr.includes('{{')) return expr.replace(/\{\{([^}]+)\}\}/g, (_, e) => { const v = deriveExpr(e.trim())(S); return typeof v === 'number' ? fmtNum(v, 4) : String(v); });
      return deriveExpr(expr)(S);
    };
    const patchFor = () => {
      const st = inst.get(), S = scope(), patch = {};
      for (const [target, expr] of rules) {
        let v; try { v = evalOne(expr, S); } catch (e) { console.warn(e.message || e); continue; }
        if (typeof v === 'number' && !Number.isFinite(v)) continue;
        const [head, ...rest] = target.split('.');
        const listKey = rest.length ? Object.keys(st).find(k => Array.isArray(st[k]) && st[k].some(it => it && it.id === head)) : null;
        if (listKey) {
          const list = (patch[listKey] || st[listKey]).map(it => (it && it.id === head ? setPath({ ...it }, rest, v) : it));
          const before = st[listKey].find(it => it && it.id === head);
          if (JSON.stringify(getPath(before, rest)) !== JSON.stringify(v)) patch[listKey] = list;
        } else if (JSON.stringify(getPath(st, [head, ...rest])) !== JSON.stringify(v)) {
          setPath(patch, [head, ...rest], v);
        }
      }
      return patch;
    };
    let busy = false;
    const apply = () => {
      if (busy) return;
      busy = true;
      try { const p = patchFor(); if (Object.keys(p).length) rawSet(p, { instant: true }); } catch (e) { console.error(e); } finally { busy = false; }
    };
    inst.set = (patch, o) => { const r = rawSet(patch, o); apply(); return r; };
    if (inst.on) inst.on('change', () => apply());
    apply();
  };
  const getPath = (o, path) => path.reduce((a, k) => (a == null ? undefined : a[k]), o);
  const setPath = (o, path, v) => { let cur = o; path.slice(0, -1).forEach(k => { cur[k] = cur[k] && typeof cur[k] === 'object' ? { ...cur[k] } : {}; cur = cur[k]; }); cur[path[path.length - 1]] = v; return o; };

  /* Registry */
  const kinds = {};
  const register = (kind, factory) => { kinds[kind] = factory; };
  const create = (host, spec, ctx = {}) => {
    const f = kinds[spec.kind];
    if (!f) { host.append(Z.h(`<div class="cv cv-missing t-caption">Canvas "${Z.esc(spec.kind)}" is not available.</div>`)); return null; }
    const inst = f(host, spec.params || {}, { ...ctx, Z, initial: spec.state || {} });
    if (spec.state) inst.set(spec.state, { instant: true });
    if (spec.state && spec.state.caption && inst.caption) inst.caption(spec.state.caption);
    if (spec.derive && !(ctx.static || ctx.mode === 'static')) attachDerive(inst, spec);
    return inst;
  };

  Z.canvas = {
    register, create, kinds, svg, attrs, label, scale, niceTicks, fmtNum, compile, tween, pulse, clearHighlight, merge, frame, emitter, series, SERIES, INK, NS,
    // added by E3: shared instance and helpers (see header)
    instance, GRADED, ease, animator, lerp, flash, badge, texOf, textW, toLocal, dragger, cellOutline, nextInDirection,
  };
})();
