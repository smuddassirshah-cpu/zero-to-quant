/* Shared grading and text helpers for the player and the answer widgets (docs/PLAN.md sections 7 and 8).
   Loaded after core.js and before the canvas and widget registries, so it only touches ZQ at call time.
   ZQ.grade exposes:
     parseNum(text, { percent })   integers, decimals, fractions a/b, mixed numbers, percentages, thousands commas
     within(v, answer, tol)        tol is { abs } or { rel } or a bare number (absolute)
     matchWrong(v, wrong, tol)     the first wrong[] entry whose value matches, or null
     sameSet(a, b), sameList(a, b)
     normExpr(s)                   normalised typed expression for the fallback comparison
     loadScript(url, ms)           lazy script loader with a timeout; one promise per url
     maths()                       Promise<{ mathlive: bool, ce: ComputeEngine|null }> for the expression widget, 6 s budget
     exprEqual(ce, a, b)           symbolic equivalence after simplify, with a 5-point numeric second opinion
     fmtNum(v), fmtFrac(v), fmtAs(v, format)   a number for display; fmtFrac writes 0.375 as 3/8; fmtAs applies a slider
                                   or control `format`: "fraction" (3/8) or "percent" (37.5%)
     correctValue(spec)            the authored answer in the shape the widget's set() takes (test hook)
     balanceMoves(spec)            the moves that take the authored pans to the balance target
     sketchPoints(spec)            the sketch control points placed on the target curve
     inline(s), prose(s)           copy to HTML: KaTeX, **bold**, *italic*, `code`, fenced code blocks; prose turns a
                                   single newline into <br> outside maths only
     patchCanvas(canvas, patch)    applies a state patch and returns a function that reverts it */
(function () {
  'use strict';
  const Z = () => window.ZQ;

  /* ---------- Numbers ---------- */
  const parseNum = (s, { percent = false } = {}) => {
    const mixed = String(s ?? '').trim().replace(/[−–]/g, '-').match(/^(-?\d+)\s+(\d+)\/(\d+)$/); // mixed number 1 1/2
    if (mixed) return +mixed[3] ? (+mixed[1] + Math.sign(+mixed[1] || 1) * (+mixed[2] / +mixed[3])) / (percent ? 100 : 1) : NaN;
    let v = String(s ?? '').trim().replace(/[\s ]+/g, '').replace(/[−–]/g, '-').replace(/^[£$€]/, '').replace(/^(-)[£$€]/, '$1');
    if (!v) return NaN;
    if (/^-?\d{1,3}(,\d{3})+(\.\d+)?$/.test(v)) v = v.replace(/,/g, ''); // 1,000 and 12,345.6
    let pct = false;
    if (v.endsWith('%')) { pct = true; v = v.slice(0, -1); }
    let n = NaN, m;
    if ((m = v.match(/^(-?\d+(?:\.\d+)?)\/(-?\d+(?:\.\d+)?)$/))) n = +m[2] ? +m[1] / +m[2] : NaN;
    else if (/^-?(\d+\.?\d*|\.\d+)(e-?\d+)?$/i.test(v)) n = parseFloat(v);
    if (!Number.isFinite(n)) return NaN;
    if (pct || percent) n /= 100;
    return n;
  };
  const normTol = (tol) => (typeof tol === 'number' ? { abs: tol } : tol || { abs: 0 });
  const within = (value, answer, tol) => {
    if (!Number.isFinite(value) || !Number.isFinite(+answer)) return false;
    const t = normTol(tol);
    if (t.rel != null) return Math.abs(value - answer) <= Math.abs(answer) * t.rel + 1e-12;
    return Math.abs(value - answer) <= (t.abs ?? 0) + 1e-9;
  };
  const matchWrong = (value, wrong = [], fallbackTol) => (wrong || []).find(w => w && w.value != null && within(value, +w.value, w.tol ?? fallbackTol ?? { abs: 1e-9 })) || null;
  const sameSet = (a = [], b = []) => { const A = new Set(a), B = new Set(b); return A.size === B.size && [...A].every(x => B.has(x)); };
  const sameList = (a = [], b = []) => a.length === b.length && a.every((x, i) => x === b[i]);
  const fmtNum = (v) => {
    if (!Number.isFinite(v)) return '';
    if (Number.isInteger(v)) return String(v);
    return String(+v.toFixed(6));
  };
  /* Readout formats for sliders and explore controls: "fraction" (3/8), "percent" (0.375 -> 37.5%), else the number */
  const fmtAs = (v, format) => (format === 'fraction' ? fmtFrac(v) : format === 'percent' ? fmtNum(+(v * 100).toFixed(4)) + '%' : fmtNum(v));
  /* A number as a fraction a/b in lowest terms (denominator up to maxDen), else fmtNum: 0.375 -> "3/8", 2 -> "2" */
  const fmtFrac = (v, maxDen = 100) => {
    if (!Number.isFinite(v)) return '';
    if (Number.isInteger(v)) return String(v);
    for (let d = 2; d <= maxDen; d++) { const n = Math.round(v * d); if (Math.abs(n / d - v) < 1e-9) return `${n}/${d}`; }
    return fmtNum(v);
  };

  /* ---------- Expressions ---------- */
  const normExpr = (s) => String(s ?? '').toLowerCase()
    .replace(/\\left|\\right/g, '').replace(/\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}/g, '($1)/($2)')
    .replace(/\\cdot|\\times/g, '*').replace(/\\div/g, '/').replace(/\\,|\;|\\!|\\ /g, '')
    .replace(/[{]/g, '(').replace(/[}]/g, ')').replace(/\\/g, '')
    .replace(/\*\*/g, '^').replace(/×|·/g, '*').replace(/÷/g, '/').replace(/[−–]/g, '-')
    .replace(/\s+/g, '').replace(/^\((-?[\w.]+)\)\/\((-?[\w.]+)\)$/, '$1/$2');

  const scripts = {};
  const loadScript = (url, ms = 6000) => {
    if (scripts[url]) return scripts[url];
    scripts[url] = new Promise((res) => {
      const el = document.createElement('script');
      let done = false;
      const end = (ok) => { if (done) return; done = true; clearTimeout(t); res(ok); };
      const t = setTimeout(() => end(false), ms);
      el.src = url; el.async = true; el.crossOrigin = 'anonymous';
      el.onload = () => end(true); el.onerror = () => end(false);
      document.head.append(el);
    });
    return scripts[url];
  };
  const LIBS = {
    mathlive: 'https://cdn.jsdelivr.net/npm/mathlive@0.105.0/mathlive.min.js',
    // The 0.30.2 package ships its browser build as compute-engine.min.umd.js (there is no compute-engine.min.js in dist/)
    ce: 'https://cdn.jsdelivr.net/npm/@cortex-js/compute-engine@0.30.2/dist/compute-engine.min.umd.js',
  };
  let mathsP = null;
  const maths = () => {
    if (mathsP) return mathsP;
    const deadline = new Promise(r => setTimeout(() => r('timeout'), 6000));
    const ml = loadScript(LIBS.mathlive, 6000).then(ok => ok && !!window.customElements.get('math-field'));
    const ce = loadScript(LIBS.ce, 6000).then(ok => {
      try { const C = window.ComputeEngine && (window.ComputeEngine.ComputeEngine || window.ComputeEngine); return ok && typeof C === 'function' ? new C() : null; } catch { return null; }
    });
    mathsP = Promise.race([Promise.all([ml, ce]), deadline]).then(r => (r === 'timeout' ? { mathlive: false, ce: null } : { mathlive: r[0], ce: r[1] }));
    return mathsP;
  };
  const exprEqual = (ce, a, b) => {
    if (!ce || a == null || b == null || a === '' || b === '') return false;
    let A, B;
    try { A = ce.parse(String(a)); B = ce.parse(String(b)); } catch { return false; }
    if (A.isValid === false || B.isValid === false) return false;
    try { if (A.simplify().isEqual(B.simplify())) return true; } catch { /* fall through to the numeric check */ }
    // Second opinion: numeric agreement at 5 points (single variable) or at one point (no variables)
    let vars = [];
    try { vars = [...new Set([...(A.unknowns || []), ...(B.unknowns || [])])]; } catch { vars = []; }
    if (vars.length > 1) return false;
    const num = (E, sub) => { try { const v = (sub ? E.subs(sub) : E).N(); const x = v.re ?? v.valueOf(); return typeof x === 'number' ? x : NaN; } catch { return NaN; } };
    const close = (x, y) => Number.isFinite(x) && Number.isFinite(y) && Math.abs(x - y) <= 1e-9 * Math.max(1, Math.abs(x), Math.abs(y));
    if (!vars.length) return close(num(A), num(B));
    const pts = [0.37, 1.61, 2.93, -0.83, 4.27];
    return pts.every(p => close(num(A, { [vars[0]]: p }), num(B, { [vars[0]]: p })));
  };

  /* ---------- Authored answers, in the shape each widget's set() accepts ---------- */
  const manipulatePath = (spec) => {
    const S = spec.states || {}, start = spec.start, target = spec.target;
    const prev = { [start]: null }, q = [start];
    while (q.length) {
      const s = q.shift();
      if (s === target) break;
      const ops = ((S[s] || {}).ops || []).slice().sort((a, b) => (a.why ? 1 : 0) - (b.why ? 1 : 0));
      for (const op of ops) if (!(op.to in prev)) { prev[op.to] = s; q.push(op.to); }
    }
    if (!(target in prev)) return [start];
    const path = []; for (let s = target; s != null; s = prev[s]) path.unshift(s);
    return path;
  };
  /* balance: the shortest list of the allowed moves that takes the authored pans to `target` (breadth first over
     unknown counts and weight totals, as the balance canvas does them). Moves are in the widget's set() shape. */
  const balanceMoves = (spec = {}) => {
    /* A pan is { u: { label: total coefficient }, w: total weight }; several unknown kinds stay apart */
    const all = [...(spec.left || []), ...(spec.right || [])];
    const X = (all.find(i => i.kind === 'unknown') || {}).label || 'x';
    const r6 = (v) => +v.toFixed(9);
    const side = (list) => { const u = {}; (list || []).filter(i => i.kind === 'unknown').forEach(i => { const l = i.label || X; u[l] = r6((u[l] || 0) + (i.coef ?? 1)); }); return { u, w: r6((list || []).filter(i => i.kind !== 'unknown').reduce((a, i) => a + (+i.value || 0), 0)) }; };
    const want = (list) => { const u = {}; (list || []).filter(t => typeof t === 'string').forEach(t => { const l = t === 'unknown' ? X : t; u[l] = (u[l] || 0) + 1; }); return { u, w: (list || []).filter(t => typeof t === 'number').reduce((a, v) => a + v, 0) }; };
    const tgt = spec.target || { left: ['unknown'], right: [] };
    const A = want(tgt.left), B = want(tgt.right);
    const eqU = (p, q) => [...new Set([...Object.keys(p), ...Object.keys(q)])].every(k => Math.abs((p[k] || 0) - (q[k] || 0)) < 1e-9);
    const eq = (p, q) => eqU(p.u, q.u) && Math.abs(p.w - q.w) < 1e-9;
    const done = (L, R) => (eq(L, A) && eq(R, B)) || (eq(L, B) && eq(R, A));
    const allowed = new Set(spec.moves || ['remove-both', 'halve-both']);
    const mapU = (u, f) => Object.fromEntries(Object.entries(u).map(([k, v]) => [k, r6(f(v, k))]).filter(([, v]) => Math.abs(v) > 1e-9));
    /* Signed pans (negative weights, coefficients, or after a subtract or add) work on totals, as the canvas does */
    const signed0 = spec.signed === true || all.some(i => (i.kind === 'unknown' && i.coef != null && i.coef !== 1) || (i.kind !== 'unknown' && +i.value < 0));
    const isInt = (u) => Object.values(u).every(Number.isInteger);
    const next = (L, R, sg) => {
      const out = [], S = (l, r) => sg || l.w < -1e-9 || r.w < -1e-9 || !isInt(l.u) || !isInt(r.u);
      if (allowed.has('remove-both')) new Set([Math.min(L.w, R.w), L.w, R.w]).forEach(n => { if (n > 1e-9 && (sg || (L.w >= n - 1e-9 && R.w >= n - 1e-9))) { const l = { u: L.u, w: r6(L.w - n) }, r = { u: R.u, w: r6(R.w - n) }; out.push([{ op: 'remove-both', n }, l, r, S(l, r)]); } });
      if (allowed.has('remove-unknown-both')) new Set([...Object.keys(L.u), ...Object.keys(R.u)]).forEach(lab => {
        if (!sg && !((L.u[lab] || 0) >= 1 && (R.u[lab] || 0) >= 1)) return;
        const dec = (u) => { const o = { ...u, [lab]: r6((u[lab] || 0) - 1) }; if (Math.abs(o[lab]) < 1e-9) delete o[lab]; return o; };
        const l = { u: dec(L.u), w: L.w }, r = { u: dec(R.u), w: R.w }; out.push([{ op: 'remove-both', n: lab }, l, r, S(l, r)]);
      });
      ['subtract-both', 'add-both'].forEach(op => { if (!allowed.has(op)) return; new Set([L.w, R.w]).forEach(v => { if (Math.abs(v) < 1e-9) return; const n = op === 'subtract-both' ? v : -v, d = op === 'subtract-both' ? -n : n; out.push([{ op, n }, { u: L.u, w: r6(L.w + d) }, { u: R.u, w: r6(R.w + d) }, true]); }); });
      const div = (k, op) => {
        if (!Number.isFinite(k) || k === 0 || k === 1) return;
        if (!sg && !(k > 1 && isInt(mapU(L.u, v => v / k)) && isInt(mapU(R.u, v => v / k)))) return;
        const l = { u: mapU(L.u, v => v / k), w: r6(L.w / k) }, r = { u: mapU(R.u, v => v / k), w: r6(R.w / k) };
        out.push([op === 'halve-both' ? { op } : { op, n: k }, l, r, S(l, r)]);
      };
      if (allowed.has('halve-both')) div(2, 'halve-both');
      if (allowed.has('divide-both')) new Set([...Object.values(L.u), ...Object.values(R.u), 2, 3, 4, 5, 6, 7, 8, 9, 10, -1, -2, -3, -4, -5]).forEach(k => div(k, 'divide-both'));
      return out;
    };
    const key = (P) => Object.keys(P.u).sort().map(k => `${k}:${P.u[k]}`).join(';') + '/' + P.w;
    const q = [[side(spec.left), side(spec.right), [], signed0]], seen = new Set();
    while (q.length) {
      const [L, R, path, sg] = q.shift();
      if (done(L, R)) return path;
      const k = `${key(L)}|${key(R)}|${sg}`;
      if (seen.has(k) || path.length >= 6) continue;
      seen.add(k);
      next(L, R, sg).forEach(([m, L2, R2, sg2]) => q.push([L2, R2, path.concat([m]), sg2]));
    }
    return null;
  };
  /* sketch: the control points (evenly spaced over xRange, as the plane canvas places them) on the target curve */
  const sketchPoints = (spec = {}) => {
    const n = spec.control || 5, r = spec.xRange || [-5, 5], C = Z() && Z().cvb;
    if (!C || !C.fnOf) return null;
    const f = C.fnOf(String(spec.target), []);
    return Array.from({ length: n }, (_, i) => { const x = +(r[0] + (r[1] - r[0]) * i / (n - 1)).toFixed(6); return [x, f(x, {})]; });
  };
  const correctValue = (spec = {}) => {
    switch (spec.kind) {
      case 'choice': return (spec.options || []).find(o => o.correct)?.id ?? null;
      case 'multi': return (spec.options || []).filter(o => o.correct).map(o => o.id);
      case 'numeric': return spec.unit === '%' ? fmtNum(spec.answer * 100) : fmtNum(+spec.answer);
      case 'expression': return spec.answer;
      case 'order': return (spec.answer || []).slice();
      case 'place': return spec.mode === 'boxes' ? JSON.parse(JSON.stringify(spec.answer || {})) : spec.mode === 'order' ? (spec.order || []).slice() : Object.fromEntries((spec.slots || []).map(s => [s.id, (s.accepts || []).slice()]));
      case 'table': {
        const out = {};
        (spec.rows || []).forEach((row, i) => row.forEach((c, j) => { if (c && typeof c === 'object' && c.edit) out[`r${i}c${j}`] = fmtNum(+c.answer); }));
        return out;
      }
      case 'manipulate': return manipulatePath(spec);
      case 'tap-regions': return spec.count != null && !(spec.answer || []).length ? (spec.among || []).slice(0, spec.count) : (spec.answer || []).slice();
      case 'slider': return spec.answer;
      case 'drag-point': return Object.fromEntries((spec.points || []).map(p => [p.id, p.target]));
      case 'code': return spec.solution ?? null;
      case 'balance': return balanceMoves(spec);
      case 'sketch': return sketchPoints(spec);
      case 'longform': return { text: 'Model answer followed.', ticks: (spec.rubric || []).map((_, i) => i), marked: true };
      default: return null;
    }
  };

  /* ---------- Copy to HTML ---------- */
  const esc = (s) => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const tex = (src, display) => (Z() && Z().tex ? Z().tex(src, display) : `<code>${esc(src)}</code>`);
  const styleText = (t) => esc(t)
    .replace(/\((\d), (\d)\)/g, '($1,&nbsp;$2)')                     // keep cell pairs such as (5, 5) together
    .replace(/`([^`]+)`/g, '<code class="lsn-ic">$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
    .replace(/(^|[^*\w])\*([^*\s][^*]*?)\*(?!\w)/g, '$1<i>$2</i>');
  /* Inline copy: text with $maths$ and $$display$$. Punctuation that follows a formula stays on its line. */
  const inline = (s, { br = false } = {}) => {
    const src = String(s ?? '');
    const text = (t) => (br ? styleText(t).replace(/\n/g, '<br>') : styleText(t)); // line breaks only outside maths: KaTeX SVG keeps its newlines
    let out = '', last = 0;
    const re = /\$\$([^$]+)\$\$|\$([^$]+)\$([.,:;?)]?)/g;
    let m;
    while ((m = re.exec(src))) {
      out += text(src.slice(last, m.index));
      if (m[1] != null) out += tex(m[1], true);
      else out += `<span class="lsn-nw">${tex(m[2], false)}${esc(m[3] || '')}</span>`;
      last = re.lastIndex;
    }
    return out + text(src.slice(last));
  };
  const codeBlock = (code, lang) => `<div class="lsn-code" data-lang="${esc(lang || '')}"><button type="button" class="link-btn lsn-copy" aria-label="Copy code">Copy</button><pre class="t-code"><code>${esc(code.replace(/\n$/, ''))}</code></pre></div>`;
  /* Block copy: paragraphs split on blank lines, fenced code blocks, display maths. */
  const prose = (s, cls = 't-prose') => {
    const src = String(s ?? '');
    const parts = src.split(/```([\w+-]*)\n([\s\S]*?)```/g);
    let out = '';
    for (let i = 0; i < parts.length; i += 3) {
      parts[i].split(/\n\s*\n/).map(p => p.trim()).filter(Boolean).forEach(p => { out += `<p class="${cls}">${inline(p, { br: true })}</p>`; });
      if (i + 2 < parts.length) out += codeBlock(parts[i + 2], parts[i + 1]);
    }
    return out;
  };
  /* Copy buttons in fenced blocks (delegated once) */
  document.addEventListener('click', (e) => {
    const b = e.target.closest && e.target.closest('.lsn-copy');
    if (!b) return;
    const code = b.parentElement.querySelector('code');
    const txt = code ? code.textContent : '';
    const done = () => { b.textContent = 'Copied'; setTimeout(() => { b.textContent = 'Copy'; }, 1400); };
    try { navigator.clipboard.writeText(txt).then(done, done); } catch { done(); }
  });

  /* ---------- Canvas patches with an undo ---------- */
  const emptyLike = (v) => (Array.isArray(v) ? [] : v && typeof v === 'object' ? {} : null);
  const patchCanvas = (canvas, patch) => {
    if (!canvas || !patch || typeof canvas.set !== 'function') return () => {};
    let before = {};
    try { before = canvas.get ? (canvas.get() || {}) : {}; } catch { before = {}; }
    const undo = {};
    Object.keys(patch).forEach(k => { undo[k] = k in before ? before[k] : emptyLike(patch[k]); });
    try { canvas.set(patch); } catch (e) { console.error(e); }
    return () => { try { canvas.set(undo); } catch (e) { console.error(e); } };
  };

  window.ZQ = window.ZQ || {};
  window.ZQ.grade = { parseNum, within, matchWrong, sameSet, sameList, fmtNum, fmtFrac, fmtAs, normExpr, loadScript, maths, exprEqual, correctValue, manipulatePath, balanceMoves, sketchPoints, inline, prose, esc, patchCanvas, LIBS };
})();
