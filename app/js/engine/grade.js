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
     correctValue(spec)            the authored answer in the shape the widget's set() takes (test hook)
     inline(s), prose(s)           copy to HTML: KaTeX, **bold**, *italic*, `code`, fenced code blocks
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
  const correctValue = (spec = {}) => {
    switch (spec.kind) {
      case 'choice': return (spec.options || []).find(o => o.correct)?.id ?? null;
      case 'multi': return (spec.options || []).filter(o => o.correct).map(o => o.id);
      case 'numeric': return spec.unit === '%' ? fmtNum(spec.answer * 100) : fmtNum(+spec.answer);
      case 'expression': return spec.answer;
      case 'order': return (spec.answer || []).slice();
      case 'place': return spec.mode === 'order' ? (spec.order || []).slice() : Object.fromEntries((spec.slots || []).map(s => [s.id, (s.accepts || []).slice()]));
      case 'table': {
        const out = {};
        (spec.rows || []).forEach((row, i) => row.forEach((c, j) => { if (c && typeof c === 'object' && c.edit) out[`r${i}c${j}`] = fmtNum(+c.answer); }));
        return out;
      }
      case 'manipulate': return manipulatePath(spec);
      case 'tap-regions': return (spec.answer || []).slice();
      case 'slider': return spec.answer;
      case 'drag-point': return Object.fromEntries((spec.points || []).map(p => [p.id, p.target]));
      case 'code': return spec.solution ?? null;
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
  const inline = (s) => {
    const src = String(s ?? '');
    let out = '', last = 0;
    const re = /\$\$([^$]+)\$\$|\$([^$]+)\$([.,:;?)]?)/g;
    let m;
    while ((m = re.exec(src))) {
      out += styleText(src.slice(last, m.index));
      if (m[1] != null) out += tex(m[1], true);
      else out += `<span class="lsn-nw">${tex(m[2], false)}${esc(m[3] || '')}</span>`;
      last = re.lastIndex;
    }
    return out + styleText(src.slice(last));
  };
  const codeBlock = (code, lang) => `<div class="lsn-code" data-lang="${esc(lang || '')}"><button type="button" class="link-btn lsn-copy" aria-label="Copy code">Copy</button><pre class="t-code"><code>${esc(code.replace(/\n$/, ''))}</code></pre></div>`;
  /* Block copy: paragraphs split on blank lines, fenced code blocks, display maths. */
  const prose = (s, cls = 't-prose') => {
    const src = String(s ?? '');
    const parts = src.split(/```([\w+-]*)\n([\s\S]*?)```/g);
    let out = '';
    for (let i = 0; i < parts.length; i += 3) {
      parts[i].split(/\n\s*\n/).map(p => p.trim()).filter(Boolean).forEach(p => { out += `<p class="${cls}">${inline(p).replace(/\n/g, '<br>')}</p>`; });
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
  window.ZQ.grade = { parseNum, within, matchWrong, sameSet, sameList, fmtNum, normExpr, loadScript, maths, exprEqual, correctValue, manipulatePath, inline, prose, esc, patchCanvas, LIBS };
})();
