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
  /* JavaScript rejects a unary minus right before **, so -x^2 is rewritten -(x**2) (maths reads it as -(x^2)) */
  const wrapUnaryPow = (src) => {
    const prim = (i) => { // end index of the primary starting at i (after spaces): number, name or name(...), or (...)
      while (src[i] === ' ') i++;
      const close = (j) => { let d = 0; for (; j < src.length; j++) { if (src[j] === '(') d++; else if (src[j] === ')' && --d === 0) return j + 1; } return src.length; };
      if (src[i] === '(') return close(i);
      const m = src.slice(i).match(/^([A-Za-z_][\w.]*|\d*\.?\d+(?:e[+-]?\d+)?)/); if (!m) return -1;
      let j = i + m[0].length; let k = j; while (src[k] === ' ') k++;
      return src[k] === '(' && /^[A-Za-z_]/.test(m[0]) ? close(k) : j;
    };
    const powChain = (i) => { // end of base(**rhs)* where rhs may itself start with a unary minus
      let j = prim(i); if (j < 0) return -1;
      for (;;) { let k = j; while (src[k] === ' ') k++; if (src.slice(k, k + 2) !== '**') return j; k += 2; while (src[k] === ' ') k++; if (src[k] === '-' || src[k] === '+') k++; const e = powChain(k); if (e < 0) return j; j = e; }
    };
    for (let i = 0; i < src.length; i++) {
      if (src[i] !== '-') continue;
      let p = i - 1; while (p >= 0 && src[p] === ' ') p--;
      if (p >= 0 && !/[(,+\-*/%<>=?:&|!]/.test(src[p])) continue; // binary minus
      if (p >= 0 && src[p] === '*' && src[p - 1] === '*') continue; // 2**-x is fine
      const end = powChain(i + 1); if (end < 0) continue;
      const body = src.slice(i + 1, end);
      if (!/\*\*/.test(body.replace(/\([^()]*\)/g, ''))) continue; // no power at this level
      src = src.slice(0, i + 1) + '(' + body + ')' + src.slice(end); i += 1;
    }
    return src;
  };
  const compile = (expr, paramNames = []) => {
    let src = String(expr).replace(/\^/g, '**').replace(/\b(sin|cos|tan|exp|ln|log10|log|sqrt|abs|max|min|floor|ceil|pow|pi|atan|asin|acos|sinh|cosh|tanh|sign|round)\b(?!\s*[:\w])/g, 'F.$1');
    if (!paramNames.includes('e')) src = src.replace(/(^|[^\w.])e(?![\w(])/g, '$1F.e'); // Euler's number, not the e of 1e5
    src = wrapUnaryPow(src);
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
  /* a keyed patch merges by id, adds a new id, and removes an id set to null (item 151) */
  const keyedList = (list, map) => list.filter(it => !(it && it.id != null && map[it.id] === null)).map(it => (it && it.id != null && isPlain(map[it.id]) ? merge(it, map[it.id]) : it))
    .concat(Object.entries(map).filter(([id, v]) => isPlain(v) && !list.some(it => it && it.id === id)).map(([id, v]) => ({ id, ...v })));
  const merge = (base, patch) => {
    if (patch == null) return base;
    const out = { ...base };
    for (const [k, v] of Object.entries(patch)) {
      const b = base ? base[k] : undefined;
      const keyed = isPlain(v) && Array.isArray(b) && b.every(it => isPlain(it) && it.id != null) && Object.values(v).every(x => x === null || isPlain(x))
        && Object.entries(v).some(([id, x]) => isPlain(x) || b.some(it => it.id === id));
      if (keyed) out[k] = keyedList(b, v);
      else out[k] = (isPlain(v) && isPlain(b)) ? merge(b, v) : v;
    }
    return out;
  };

  /* Captions read like prose (item 98): maths, inline code in backticks, **bold** and *italic*, via grade.js's inline() */
  const capHtml = (t) => (Z.grade && Z.grade.inline ? Z.grade.inline(t) : Z.md(t));
  /* Frame: a responsive SVG in the 540px column. frame(host, w, h) -> { svg, g } with a caption slot.
     fit: true caps the drawing at its natural width (w px) and centres it, for drawings narrower than the column. */
  const frame = (host, w, h, { cls = '', label: aria = 'Diagram', fit = false } = {}) => {
    const wrap = document.createElement('div'); wrap.className = 'cv ' + cls;
    const s = svg('svg', { viewBox: `0 0 ${w} ${h}`, width: '100%', role: 'img', 'aria-label': aria, class: 'cv-svg' });
    if (fit) s.style.maxWidth = w + 'px';
    const g = svg('g'); s.append(g);
    const cap = document.createElement('div'); cap.className = 't-caption cv-caption'; cap.hidden = true;
    wrap.append(s, cap); host.append(wrap);
    const fr = { wrap, svg: s, g, caption: (t) => { cap.hidden = !t; cap.innerHTML = t ? capHtml(t) : ''; }, w, h };
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
    if (obj && obj.tagName === 'TR') obj = obj.lastElementChild; // a table row (tap: "rows") wears its badge in its last cell
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
     ceil, round(v, places), fixed(v, places), money(v, symbol), pi. JavaScript's own (expr).toFixed(2) and ternaries
     (a ? b : c) work too. A caption (or any string target) fills each {{expression}}. */
  const grouped = (v, d) => Math.abs(+v).toLocaleString('en-GB', { minimumFractionDigits: d, maximumFractionDigits: d });
  const DERIVE_FN = { abs: Math.abs, min: Math.min, max: Math.max, sqrt: Math.sqrt, pow: Math.pow, exp: Math.exp, log: Math.log, ln: Math.log, log10: Math.log10, floor: Math.floor, ceil: Math.ceil, sign: Math.sign, pi: Math.PI, e: Math.E,
    sin: Math.sin, cos: Math.cos, tan: Math.tan, asin: Math.asin, acos: Math.acos, atan: Math.atan, atan2: Math.atan2, hypot: Math.hypot, round: (v, d = 0) => +(+v).toFixed(d),
    /* for captions: fixed(v, 2) keeps trailing zeros ("3.50"), money(v) is "£1,234.50" or "−£3.50" (money(v, "$") for
       dollars); both write a negative with the minus sign U+2212 */
    fixed: (v, d = 2) => (+v < 0 && Math.abs(+v).toFixed(d) !== (0).toFixed(d) ? '−' : '') + Math.abs(+v).toFixed(d), money: (v, sym = '£', d = 2) => (+v < 0 && grouped(v, d) !== grouped(0, d) ? '−' : '') + sym + grouped(v, d) };
  const deriveCache = {};
  const deriveExpr = (src) => {
    if (deriveCache[src]) return deriveCache[src];
    /* string literals are blanked before the guard, so "=" or ";" inside quotes is allowed (item 90) */
    if (/[;`{}]|=>|\bfunction\b|\bnew\b|\bthis\b|(^|[^=!<>])=(?!=)/.test(src.replace(/"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*'/g, '""'))) throw new Error('derive: not an expression: ' + src);
    // eslint-disable-next-line no-new-func
    const f = new Function('S', 'with (S) { return (' + src + '); }');
    return (deriveCache[src] = f);
  };
  const attachDerive = (inst, spec) => {
    const rules = Object.entries(spec.derive || {});
    if (!rules.length || !inst || !inst.set) return;
    const rawSet = inst.set.bind(inst);
    const sides = inst.sides || null; // a pair: { left, right } and the side widgets drive (inst.activeSide)
    const scopeOf = (one, params) => {
      const st = one.get ? one.get() : {}, S = {};
      Object.entries(st).forEach(([k, v]) => { if (typeof v === 'number') S[k] = v; });
      Object.assign(S, (params || {}).params || {}, st.params || {});
      const vals = Object.assign({}, st.values || {}); try { if (typeof one.values === 'function') Object.assign(vals, one.values() || {}); } catch { /* no heights */ }
      S.values = vals;
      Object.values(st).forEach(v => { if (Array.isArray(v)) v.forEach(it => { if (it && typeof it === 'object' && it.id != null && /^[A-Za-z_$][\w$]*$/.test(it.id)) S[it.id] = it; }); });
      return S;
    };
    /* A pair reads across both sides: ids of either side directly, or left.p1 and right.p1 when they share an id */
    const scope = () => {
      if (!sides) return Object.assign({}, DERIVE_FN, scopeOf(inst, spec.params));
      const L = scopeOf(sides.left, (spec.left || {}).params), R = scopeOf(sides.right, (spec.right || {}).params);
      return Object.assign({}, DERIVE_FN, L, R, { left: L, right: R, values: Object.assign({}, L.values, R.values) });
    };
    const evalOne = (expr, S) => {
      if (typeof expr !== 'string') return expr;
      if (expr.includes('{{')) return expr.replace(/\{\{([^}]+)\}\}/g, (_, e) => { const v = deriveExpr(e.trim())(S); return typeof v === 'number' ? fmtNum(v, 4).replace(/^-/, '−') : String(v).replace(/(^|[\s(=])-(?=\d)/g, '$1−'); });
      return deriveExpr(expr)(S);
    };
    /* Write v at target into patch, against state st (only when it changes) */
    const put = (st, patch, target, v) => {
      const [head, ...rest] = target.split('.');
      const listKey = rest.length ? Object.keys(st).find(k => Array.isArray(st[k]) && st[k].some(it => it && it.id === head)) : null;
      if (listKey) {
        const list = (patch[listKey] || st[listKey]).map(it => (it && it.id === head ? setPath({ ...it }, rest, v) : it));
        const before = st[listKey].find(it => it && it.id === head);
        if (JSON.stringify(getPath(before, rest)) !== JSON.stringify(v)) patch[listKey] = list;
      } else if (JSON.stringify(getPath(st, [head, ...rest])) !== JSON.stringify(v)) setPath(patch, [head, ...rest], v);
    };
    const patchFor = () => {
      const S = scope(), patch = {};
      for (const [target, expr] of rules) {
        let v; try { v = evalOne(expr, S); } catch (e) { console.warn(e.message || e); continue; }
        if (typeof v === 'number' && !Number.isFinite(v)) continue;
        const m = sides && target.match(/^(left|right):(.+)$/);
        if (m) { patch[m[1]] = patch[m[1]] || {}; put(sides[m[1]].get(), patch[m[1]], m[2], v); }
        else if (sides && target !== 'caption') { const a = inst.activeSide || 'left'; patch[a] = patch[a] || {}; put(sides[a].get(), patch[a], target, v); }
        else put(sides ? { caption: inst.get().caption } : inst.get(), patch, target, v);
      }
      Object.keys(patch).forEach(k => { if (sides && (k === 'left' || k === 'right') && !Object.keys(patch[k]).length) delete patch[k]; });
      return patch;
    };
    let busy = false;
    const apply = () => {
      if (busy) return;
      busy = true;
      /* up to three passes, so a rule may read a value another rule derives (a caption reading a derived point) */
      try { for (let k = 0; k < 3; k++) { const p = patchFor(); if (!Object.keys(p).length) break; rawSet(p, { instant: true }); } } catch (e) { console.error(e); } finally { busy = false; }
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
  /* Two canvases side by side: canvas: { kind: "pair", left: { kind, params, state }, right: {...}, active: "left",
     stack: false, derive: {...} }. State patches take { left: {...}, right: {...}, caption }; ids in highlight, mark and
     flash take a "left:" or "right:" prefix (unprefixed ids go to both). Canvas-bound widgets and anything else the pair
     does not define (enable, points, place, cells, removeBoth, ...) reach the `active` side; a patch key other than
     left, right and caption goes there too. Controls bind "left:p1" or "right:a" (unprefixed: the active side). */
  const SIDES = ['left', 'right'];
  const pairOf = (host, spec, ctx) => {
    const wrap = document.createElement('div'); wrap.className = 'cv cv-pair' + (spec.stack ? ' is-stacked' : '');
    const row = document.createElement('div'); row.className = 'cv-pair-row';
    const cap = document.createElement('div'); cap.className = 't-caption cv-caption'; cap.hidden = true;
    wrap.append(row, cap); host.append(wrap);
    const side = {}, active = SIDES.includes(spec.active) ? spec.active : 'left';
    /* item 155: two tables side by side are compact, and stack (each at full width) whenever either would overflow */
    const twoTables = SIDES.every(k => (spec[k] || {}).kind === 'table');
    const hosts = {};
    /* item 185: shareMargins lines up the plot areas of two series (or other kinds with margins()) */
    const build = (k, extra) => { const sp = spec[k] || { kind: 'table', params: {} }; return create(hosts[k], { ...sp, params: { ...(twoTables ? { compact: true } : {}), ...(sp.params || {}), ...(extra || {}) } }, ctx); };
    for (const k of SIDES) {
      const h = document.createElement('div'); h.className = 'cv-pair-side cv-pair-' + k; row.append(h); hosts[k] = h;
      side[k] = build(k);
    }
    if (spec.shareMargins && SIDES.every(k => side[k] && typeof side[k].margins === 'function')) {
      const m = SIDES.map(k => side[k].margins()), want = { left: Math.max(...m.map(x => x.left)), right: Math.max(...m.map(x => x.right)) };
      SIDES.forEach((k, i) => { if (m[i].left !== want.left || m[i].right !== want.right) { side[k].destroy && side[k].destroy(); hosts[k].replaceChildren(); side[k] = build(k, { margins: want }); } });
    }
    if (twoTables && !spec.stack) {
      const fit = () => {
        if (!wrap.isConnected) return;
        wrap.classList.remove('is-stacked');
        const over = SIDES.some(k => { const sc = side[k] && side[k].el && side[k].el.querySelector('.cv-tbl-wrap'); return sc && sc.scrollWidth > sc.clientWidth + 1; });
        wrap.classList.toggle('is-stacked', over);
      };
      if (typeof ResizeObserver === 'function') { let lastW = -1; new ResizeObserver(() => { const w = wrap.clientWidth; if (w !== lastW) { lastW = w; fit(); } }).observe(wrap); }
      requestAnimationFrame(fit);
    }
    const A = side[active];
    let caption = '';
    const route = (ids) => { const out = { left: [], right: [] }; [].concat(ids || []).forEach(id => { const m = String(id).match(/^(left|right):(.+)$/); if (m) out[m[1]].push(m[2]); else { out.left.push(id); out.right.push(id); } }); return out; };
    const each = (ids, fn) => { const r = route(ids); SIDES.forEach(k => { if (side[k] && r[k].length) fn(side[k], r[k]); }); };
    const em = emitter();
    SIDES.forEach(k => side[k] && side[k].on && side[k].on('change', (d) => em.emit('change', d && typeof d === 'object' ? { ...d, side: k } : d)));
    const sideOfName = (name) => { const m = String(name).match(/^(left|right):(.+)$/); return m ? [side[m[1]], m[2]] : [A, String(name)]; };
    const api = {
      el: wrap, kind: 'pair', params: spec, sides: side, activeSide: active,
      get: () => ({ ...(A && A.get ? A.get() : {}), left: side.left && side.left.get(), right: side.right && side.right.get(), caption }),
      set(patch = {}, o = {}) {
        patch = patch || {};
        const rest = {};
        Object.entries(patch).forEach(([k, v]) => { if (SIDES.includes(k)) { if (v && side[k]) side[k].set(v, o); } else if (k === 'caption') { caption = v || ''; cap.hidden = !caption; cap.innerHTML = caption ? capHtml(caption) : ''; } else rest[k] = v; });
        if (Object.keys(rest).length && A) { if ('highlight' in rest) { each(rest.highlight, (c, ids) => c.set({ highlight: ids }, o)); delete rest.highlight; } if (Object.keys(rest).length) A.set(rest, o); }
        return api;
      },
      highlight(ids, on = true) { if (ids == null || (Array.isArray(ids) && !ids.length)) SIDES.forEach(k => side[k] && side[k].highlight(ids, on)); else each(ids, (c, l) => c.highlight(l, on)); return api; },
      mark(ids, cls, on = true) { each(ids, (c, l) => c.mark && c.mark(l, cls, on)); return api; },
      unmark(cls) { SIDES.forEach(k => side[k] && side[k].unmark && side[k].unmark(cls)); return api; },
      flash(ids, o) { const ps = []; each(ids, (c, l) => c.flash && ps.push(c.flash(l, o))); return Promise.all(ps); },
      unflash() { SIDES.forEach(k => side[k] && side[k].unflash && side[k].unflash()); },
      lock(on = true) { SIDES.forEach(k => side[k] && side[k].lock && side[k].lock(on)); return api; },
      caption(t) { api.set({ caption: t }); },
      on: (ev, fn) => em.on(ev, fn),
      setParam(name, v) {
        const [c, n] = sideOfName(name); if (!c) return;
        if (c.setParam && !/^(points|intervals|arrows|markers|vectors|segments|pointers)\./.test(n)) c.setParam(n, v);
        else c.set(n.includes('.') ? n.split('.').reduceRight((acc, k) => ({ [k]: acc }), v) : { params: { [n]: v } }, { instant: true });
        api.set({}, { instant: true }); // a side changed outside the pair's own set: let derive see it
      },
      getParam(name) {
        const [c, n] = sideOfName(name); if (!c) return undefined;
        const v = c.getParam ? c.getParam(n) : undefined; if (v != null) return v;
        let o = c.get ? c.get() : {}; for (const k of n.split('.')) o = o == null ? undefined : Array.isArray(o) ? o.find(it => it && it.id === k) : o[k];
        return typeof o === 'number' ? o : (o == null ? ((c.get() || {}).params || {})[n] : undefined);
      },
      clone(host2) { return create(host2, { ...spec, state: { left: side.left && side.left.get(), right: side.right && side.right.get(), caption } }, { ...ctx, static: true }); },
      destroy() { SIDES.forEach(k => side[k] && side[k].destroy && side[k].destroy()); wrap.remove(); },
    };
    /* item 183: tap: "sides" makes each whole side one tappable object, ids "left" and "right" ("tap the misleading chart") */
    if (spec.tap === 'sides') {
      let selected = [], tapOn = false, locked = false, opts = {};
      const paint = () => SIDES.forEach(k => { const on = selected.includes(k); hosts[k].classList.toggle('is-on', on); if (tapOn) hosts[k].setAttribute('aria-pressed', String(on)); });
      SIDES.forEach(k => {
        const h = hosts[k]; h.classList.add('cv-pair-tap'); h.dataset.id = k; h.dataset.label = spec[k + 'Label'] || (k === 'left' ? 'Left chart' : 'Right chart');
        const toggle = () => {
          if (!tapOn || locked || (opts.only && !opts.only.includes(k))) return;
          const on = !selected.includes(k);
          if (on && opts.max && selected.length >= opts.max) selected = selected.slice(selected.length - opts.max + 1);
          selected = on ? [...selected, k] : selected.filter(x => x !== k);
          paint(); em.emit('change', { type: 'tap', id: k, on, selected: selected.slice() });
        };
        h.addEventListener('click', toggle);
        h.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); } });
      });
      const baseGet = api.get, baseSet = api.set, baseMark = api.mark, baseUnmark = api.unmark, baseLock = api.lock;
      Object.assign(api, {
        enable(m, o) {
          tapOn = m === 'tap'; opts = o || {};
          SIDES.forEach(k => { const h = hosts[k]; if (tapOn) { h.dataset.tap = ''; h.tabIndex = 0; h.setAttribute('role', 'button'); h.setAttribute('aria-label', h.dataset.label); } else { delete h.dataset.tap; h.removeAttribute('tabindex'); h.removeAttribute('role'); h.removeAttribute('aria-pressed'); } });
          wrap.classList.toggle('cv-tap', tapOn); paint(); return api;
        },
        get: () => ({ ...baseGet(), selected: selected.slice() }),
        set(patch = {}, o = {}) { if (patch && 'selected' in patch) { selected = [].concat(patch.selected || []).filter(k => SIDES.includes(k)); paint(); const { selected: _, ...rest } = patch; patch = rest; } return baseSet(patch, o); },
        mark(ids, cls, on = true) { const mine = [].concat(ids || []).filter(k => SIDES.includes(k)); mine.forEach(k => { hosts[k].classList.toggle(cls, on); if (on && cls === 'is-notyet') badge(hosts[k], 'cross'); if (!on) hosts[k].querySelectorAll(':scope > .cv-badge').forEach(b => b.remove()); }); return baseMark([].concat(ids || []).filter(k => !SIDES.includes(k)), cls, on); },
        unmark(cls) { SIDES.forEach(k => { (cls ? [cls] : GRADED).forEach(c => hosts[k].classList.remove(c)); if (!cls) hosts[k].querySelectorAll(':scope > .cv-badge').forEach(b => b.remove()); }); return baseUnmark(cls); },
        lock(on = true) { locked = !!on; wrap.classList.toggle('cv-locked', locked); return baseLock(on); },
        flash(ids, o) { const mine = [].concat(ids || []).filter(k => SIDES.includes(k)).map(k => hosts[k]); return mine.length ? flash(mine, o) : Promise.resolve(); },
      });
    }
    /* Everything else (enable, points, place, cells, sample, removeBoth, ...) is the active side's */
    return new Proxy(api, { get(t, k) { if (k in t) return t[k]; const v = A ? A[k] : undefined; return typeof v === 'function' ? v.bind(A) : v; }, set(t, k, v) { t[k] = v; return true; } });
  };
  const create = (host, spec, ctx = {}) => {
    if (spec.kind === 'pair') {
      const inst = pairOf(host, spec, { ...ctx, Z });
      if (spec.state) inst.set(spec.state, { instant: true });
      if (spec.derive) attachDerive(inst, spec);
      return inst;
    }
    const f = kinds[spec.kind];
    if (!f) { host.append(Z.h(`<div class="cv cv-missing t-caption">Canvas "${Z.esc(spec.kind)}" is not available.</div>`)); return null; }
    const inst = f(host, spec.params || {}, { ...ctx, Z, initial: spec.state || {} });
    if (spec.state) inst.set(spec.state, { instant: true });
    if (spec.state && spec.state.caption && inst.caption) inst.caption(spec.state.caption);
    if (spec.derive) attachDerive(inst, spec); // static copies too: the Why? clone shows values derived from its own (explained) state
    return inst;
  };

  Z.canvas = {
    register, create, kinds, svg, attrs, label, scale, niceTicks, fmtNum, compile, tween, pulse, clearHighlight, merge, frame, emitter, series, SERIES, INK, NS,
    // added by E3: shared instance and helpers (see header)
    instance, GRADED, ease, animator, lerp, flash, badge, texOf, textW, toLocal, dragger, cellOutline, nextInDirection,
  };
})();
