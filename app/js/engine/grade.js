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
     exprEqual(ce, a, b, { functions })  symbolic equivalence after simplify, with a 6-point numeric second opinion; real and
                                   imaginary parts both compared when an i appears; vectors and matrices entry by entry
     exprShape(ce, s)              undefined (no parse), null (one value) or { n, r, c, vec } for a vector or matrix
     exprShapeLine(ce, ans, input) the "wrong size" feedback line for a vector or matrix answer, else null
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
  /* item 426: ten significant figures, not six decimal places, so a tiny answer (9.5e-7) survives Show solution and the
     test hook and passes its own tolerance; float noise (0.30000000000000004) still prints 0.3 */
  const fmtNum = (v) => {
    if (!Number.isFinite(v)) return '';
    if (Number.isInteger(v)) return String(v);
    return String(+v.toPrecision(10));
  };
  /* Readout formats for sliders and explore controls: "fraction" (3/8), "percent" (0.375 -> 37.5%), else the number */
  /* decimals: fixed places for the plain and percent readouts (trailing zeros kept), whatever the step */
  const fmtAs = (v, format, decimals) => {
    const fx = (n) => (decimals != null ? (n < 0 ? '−' : '') + Math.abs(n).toFixed(decimals) : fmtNum(n).replace(/^-/, '−'));
    return format === 'fraction' ? fmtFrac(v).replace(/^-/, '−') : format === 'percent' ? fx(+(v * 100).toFixed(6)) + '%' : fx(v);
  };
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
    .replace(/\s+/g, '').replace(/varepsilon|ε|ϵ/g, 'epsilon').replace(/^\((-?[\w.]+)\)\/\((-?[\w.]+)\)$/, '$1/$2');

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
  /* Item 230: Compute Engine's simplify().isEqual() can call x and sqrt(x) equal (they agree at 0 and 1), and it also
     misses true identities (e^{x+y} and e^x e^y, ln(xy) and ln x + ln y). So whenever both sides evaluate, the deciding
     test is numeric: agreement at 6 seeded points with every free symbol drawn from 0.3 to 3 (away from 0 and 1), with
     any number of variables; a point where both sides are undefined is skipped, one side undefined fails. Only when
     neither side evaluates to a number anywhere (an equation, a set) does the symbolic check decide. */
  /* item 267: \binom{n}{k} (and \dbinom, \tbinom, {n \choose k}) becomes n!/(k!(n-k)!), which Compute Engine parses */
  const braced = (t, i) => { if (t[i] !== '{') return null; let d = 0; for (let j = i; j < t.length; j++) { if (t[j] === '{') d++; else if (t[j] === '}' && --d === 0) return [t.slice(i + 1, j), j + 1]; } return null; };
  const unbinom = (t) => {
    t = String(t).replace(/\{([^{}]*)\\choose([^{}]*)\}/g, '\\binom{$1}{$2}');
    for (let guard = 0; guard < 20; guard++) {
      const m = t.match(/\\[dt]?binom\s*/); if (!m) break;
      const i = m.index + m[0].length, A = braced(t, i); if (!A) break; const B = braced(t, A[1]); if (!B) break;
      t = t.slice(0, m.index) + `\\frac{(${A[0]})!}{(${B[0]})!((${A[0]})-(${B[0]}))!}` + t.slice(B[1]);
    }
    return t;
  };
  /* Item 437: lone capital N and D (the engine reads them as its own functions), \epsilon and \varepsilon (and the
     Unicode letters) as one symbol, and \min and \max (whose result type the engine will not add to anything) as
     (a + b -/+ |a - b|)/2, folded over any number of arguments. Item 429: with an imaginary unit on either side, i
     becomes the symbol \iota (the engine folds 1/(1 + i) into a wrong constant at parse time) and \bar is \overline. */
  const IMAG = /(?<![A-Za-z\\])(?<!_)(?<!_\{)i/;
  const normI = (s) => String(s).replace(/\\mathrm\{i\}|\\imaginaryI(?![A-Za-z])/g, 'i');
  const hasImag = (s) => IMAG.test(normI(s));
  const matching = (t, from) => {
    const args = []; let depth = 1, last = from;
    for (let k = from; k < t.length; k++) {
      const c = t[k];
      if (c === '(' || c === '[' || c === '{') depth++;
      else if (c === ')' || c === ']' || c === '}') {
        if (--depth === 0) { args.push(t.slice(last, k)); return { end: k + 1, args: args.map((x, n) => (n === args.length - 1 ? x.replace(/\\right\s*\\?$/, '') : x)) }; }
      } else if (c === ',' && depth === 1) { args.push(t.slice(last, k)); last = k + 1; }
    }
    return null;
  };
  const minmax = (t) => {
    const re = /\\(min|max)(?![A-Za-z])|\\operatorname\{(min|max)\}/g;
    let out = '', pos = 0, m;
    while ((m = re.exec(t))) {
      if (m.index < pos) continue;
      const fn = m[1] || m[2], after = m.index + m[0].length;
      const o = /^\s*(?:\\left\s*)?(\(|\[|\\\{|\\lbrace)/.exec(t.slice(after));
      const g = o && matching(t, after + o[0].length);
      if (!g) continue;
      const args = g.args.map(minmax).filter(x => x.trim());
      if (!args.length) continue;
      const sign = fn === 'min' ? '-' : '+';
      const one = args.reduce((a, x) => `\\frac{(${a})+(${x})${sign}\\left|(${a})-(${x})\\right|}{2}`);
      out += t.slice(pos, m.index) + `\\left(${one}\\right)`;
      pos = re.lastIndex = g.end;
    }
    return out + t.slice(pos);
  };
  /* P32-expr-exp: \exp, \operatorname{exp} and \mathrm{exp} (what MathLive's "exp" shortcut types) with a bracketed
     argument ((..), \left(..\right), {..}) or one token (a letter, number or \command) become (\exponentialE^{(arg)}).
     The engine reads \exp(x) as the tuple ["Tuple", "Exp", "x"]. */
  const unexp = (t) => {
    const re = /\\(?:operatorname|mathrm)\{exp\}|\\exp(?![A-Za-z])/;
    for (let guard = 0; guard < 40; guard++) {
      const m = re.exec(t); if (!m) break;
      const at = m.index + m[0].length, rest = t.slice(at);
      const o = /^\s*(?:\\left\s*)?(\(|\{|\[)/.exec(rest);
      let arg, end;
      if (o) {
        const g = matching(t, at + o[0].length); if (!g) break;
        arg = t.slice(at + o[0].length, g.end - 1).replace(/\\right\s*\\?$/, ''); end = g.end;
      } else {
        const k = /^\s*(\\[A-Za-z]+|[A-Za-z0-9.])/.exec(rest); if (!k) break;
        arg = k[1]; end = at + k[0].length;
      }
      t = t.slice(0, m.index) + `\\left(\\exponentialE^{(${arg})}\\right)` + t.slice(end);
    }
    return t;
  };
  /* P32-expr-callhead: a lone Latin or Greek letter (optional subscript or superscript) directly before ( or \left(
     is a product, not a call, unless the screen lists it in `functions`. Compute Engine would read it as a function and
     keep the symbol a function for the rest of the page. */
  const GREEK = 'alpha|beta|gamma|delta|varepsilon|epsilon|zeta|eta|theta|vartheta|iota|kappa|lambda|mu|nu|xi|rho|varrho|sigma|varsigma|tau|upsilon|phi|varphi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Upsilon|Phi|Psi|Omega';
  const CALLHEAD = new RegExp(`(?<![A-Za-z\\\\])([A-Za-z]|\\\\(?:${GREEK})(?![A-Za-z]))((?:_(?:[A-Za-z0-9]|\\{[^{}]*\\}))?(?:\\^(?:[A-Za-z0-9]|\\{[^{}]*\\}))?)(\\s*)(?=\\\\left\\s*\\(|\\()`, 'g');
  const uncall = (t, fns) => t.replace(CALLHEAD, (m, b, sc, sp) => ((fns || []).includes(b) || (fns || []).includes(b.replace(/^\\/, '')) ? m : `${b}${sc}\\cdot `));
  const prep = (s, cx, fns) => {
    let t = normI(s).replace(/(?:\\left\s*)?\\langle\s*/g, '(').replace(/(?:\\right\s*)?\\rangle/g, ')').replace(/\\epsilon(?![A-Za-z])|[εϵ]/g, '\\varepsilon')
      .replace(/(?<![A-Za-z\\])(?<!\\(?:mathbb|mathcal|mathrm|mathbf|mathit|mathsf|text|operatorname)\{)([ND])(?![A-Za-z])/g, '\\mathrm{$1}');
    t = uncall(unexp(unbinom(minmax(t))), fns);
    if (cx) t = t.replace(/(?<![A-Za-z\\])(?<!_)(?<!_\{)i/g, '\\iota ').replace(/\\bar\s*\{/g, '\\overline{');
    return t;
  };
  /* Complex arithmetic on [re, im] pairs. Our own evaluator over MathJSON, because the engine's complex division is wrong. */
  const cxm = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
  const cxd = (a, b) => { const d = b[0] * b[0] + b[1] * b[1]; return [(a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d]; };
  const cxln = (a) => [Math.log(Math.hypot(a[0], a[1])), Math.atan2(a[1], a[0])];
  const cxexp = (a) => { const r = Math.exp(a[0]); return [r * Math.cos(a[1]), r * Math.sin(a[1])]; };
  const cxsqrt = (a) => { const r = Math.hypot(a[0], a[1]), re = Math.sqrt((r + a[0]) / 2), im = Math.sqrt(Math.max(0, (r - a[0]) / 2)); return [re, a[1] < 0 ? -im : im]; };
  const cxpow = (a, b) => {
    if (b[1] === 0 && Number.isInteger(b[0]) && Math.abs(b[0]) <= 64) { let r = [1, 0]; for (let k = Math.abs(b[0]); k > 0; k--) r = cxm(r, a); return b[0] < 0 ? cxd([1, 0], r) : r; }
    if (a[1] === 0 && a[0] > 0 && b[1] === 0) return [Math.pow(a[0], b[0]), 0];
    if (a[0] === 0 && a[1] === 0) return b[0] > 0 ? [0, 0] : [NaN, NaN];
    return cxexp(cxm(b, cxln(a)));
  };
  const cxsin = (a) => [Math.sin(a[0]) * Math.cosh(a[1]), Math.cos(a[0]) * Math.sinh(a[1])];
  const cxcos = (a) => [Math.cos(a[0]) * Math.cosh(a[1]), -Math.sin(a[0]) * Math.sinh(a[1])];
  const cxsinh = (a) => [Math.sinh(a[0]) * Math.cos(a[1]), Math.cosh(a[0]) * Math.sin(a[1])];
  const cxcosh = (a) => [Math.cosh(a[0]) * Math.cos(a[1]), Math.sinh(a[0]) * Math.sin(a[1])];
  const NOPE = new Error('unsupported');
  const cxEval = (j, env) => {
    if (typeof j === 'number') return [j, 0];
    if (j && typeof j === 'object' && !Array.isArray(j)) { if (j.num != null) return [parseFloat(j.num), 0]; if (j.sym != null) return cxEval(j.sym, env); throw NOPE; }
    if (typeof j === 'string') {
      if (j in env) return env[j];
      if (j === 'ExponentialE') return [Math.E, 0];
      if (j === 'Pi') return [Math.PI, 0];
      if (j === 'ImaginaryUnit') return [0, 1];
      throw NOPE;
    }
    if (!Array.isArray(j)) throw NOPE;
    const h = j[0], v = j.slice(1).map(x => cxEval(x, env)), x = v[0];
    switch (h) {
      case 'Complex': return [v[0][0], v[1][0]];
      case 'Rational': case 'Divide': return v.slice(1).reduce(cxd, x);
      case 'Add': return v.reduce((a, b) => [a[0] + b[0], a[1] + b[1]], [0, 0]);
      case 'Subtract': return v.slice(1).reduce((a, b) => [a[0] - b[0], a[1] - b[1]], x);
      case 'Negate': return [-x[0], -x[1]];
      case 'Multiply': return v.reduce(cxm, [1, 0]);
      case 'Square': return cxm(x, x);
      case 'Power': return cxpow(x, v[1]);
      case 'Sqrt': return cxsqrt(x);
      case 'Root': { const n = v[1][0]; if (x[1] === 0 && x[0] < 0 && Number.isInteger(n) && n % 2) return [-Math.pow(-x[0], 1 / n), 0]; return cxpow(x, [1 / n, 0]); }
      case 'Exp': return cxexp(x);
      case 'Ln': return cxln(x);
      case 'Log': return cxd(cxln(x), v[1] ? cxln(v[1]) : [Math.LN10, 0]);
      case 'Lb': return cxd(cxln(x), [Math.LN2, 0]);
      case 'Sin': return cxsin(x);
      case 'Cos': return cxcos(x);
      case 'Tan': return cxd(cxsin(x), cxcos(x));
      case 'Sinh': return cxsinh(x);
      case 'Cosh': return cxcosh(x);
      case 'Tanh': return cxd(cxsinh(x), cxcosh(x));
      case 'Abs': return [Math.hypot(x[0], x[1]), 0];
      case 'Conjugate': case 'OverBar': return [x[0], -x[1]];
      case 'Re': return [x[0], 0];
      case 'Im': return [x[1], 0];
      case 'Arg': case 'Argument': return [Math.atan2(x[1], x[0]), 0];
      default: throw NOPE;
    }
  };
  /* Vectors and matrices (item 433): a Tuple, List or Matrix. A column, a row and (a, b, c) are the same vector. */
  const itemsOf = (ce, E) => {
    const j = E.json; const h = Array.isArray(j) ? j[0] : null, a = Array.isArray(j) ? j.slice(1) : [];
    let list = null, r = 0, c = 0;
    if ((h === 'Tuple' || h === 'List') && a.length > 1 && !a.some(x => Array.isArray(x) && x[0] === 'List')) { list = a; r = 1; c = a.length; }
    else if (h === 'Matrix' && Array.isArray(a[0])) { const rows = a[0].slice(1).map(x => x.slice(1)); r = rows.length; c = r ? rows[0].length : 0; list = [].concat(...rows); }
    if (!list || !list.length) return null;
    return { items: list.map(x => ce.box(x)), vec: r === 1 || c === 1, n: list.length, r, c };
  };
  const sameShape = (p, q) => p.vec && q.vec ? p.n === q.n : !p.vec && !q.vec && p.r === q.r && p.c === q.c;
  const parseLatex = (ce, s, fns) => { const cx = hasImag(s); const E = ce.parse(prep(s, cx, fns)); return E.isValid === false ? undefined : E; };
  /* exprShape: undefined when the input does not parse, null for one value, else { n, r, c, vec } */
  const exprShape = (ce, s, fns) => {
    try { const E = parseLatex(ce, s, fns); if (!E) return undefined; const it = itemsOf(ce, E); return it ? { n: it.n, r: it.r, c: it.c, vec: it.vec } : null; } catch { return undefined; }
  };
  const shapeWord = (p) => p.vec ? `${p.n} component${p.n === 1 ? '' : 's'}` : `${p.r} rows and ${p.c} columns`;
  /* The feedback line when the learner's vector or matrix has the wrong shape (key "length"), else null */
  const exprShapeLine = (ce, answer, input, fns) => {
    const want = exprShape(ce, answer, fns), got = exprShape(ce, input, fns);
    if (got === undefined || want === undefined || (!want && !got)) return null;
    if (want && got && sameShape(want, got)) return null;
    if (want && !got) return `That is a single value. The answer has ${shapeWord(want)}.`;
    if (!want && got) return `The answer is a single value, not ${got.vec ? 'a vector' : 'a matrix'}.`;
    return `Your answer has ${shapeWord(got)}. The answer has ${shapeWord(want)}.`;
  };
  const scalarEqual = (ce, A, B, counting, cx, ints) => {
    let sym = false;
    try { sym = !!A.simplify().isEqual(B.simplify()); } catch { sym = false; }
    let vars = [];
    try { vars = [...new Set([...(A.unknowns || []), ...(B.unknowns || [])])].filter(v => !(cx && v === 'iota')); } catch { vars = []; }
    const num = (E, sub) => { try { const v = (sub ? E.subs(sub) : E).N(); const x = v.re ?? v.valueOf(); return typeof x === 'number' ? x : NaN; } catch { return NaN; } };
    /* complex mode: [re, im] from our evaluator; an unsupported function falls back to the engine's N() */
    const val = (E, p) => {
      if (!cx) return [num(E, p), 0];
      const env = { iota: [0, 1] }; for (const k in p || {}) env[k] = [p[k], 0];
      try { return cxEval(E.json, env); } catch { /* engine fallback below */ }
      try { const v = E.subs({ ...(p || {}), iota: ce.box(['Complex', 0, 1]) }).N(); return [typeof v.re === 'number' ? v.re : NaN, typeof v.im === 'number' ? v.im : 0]; } catch { return [NaN, NaN]; }
    };
    const fin = (z) => Number.isFinite(z[0]) && Number.isFinite(z[1]);
    const close = (x, y) => Math.abs(x - y) <= 1e-9 * Math.max(1, Math.abs(x), Math.abs(y));
    let seed = 20240531; const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
    const draw = () => { let v; do { v = 0.3 + 2.7 * rnd(); } while (Math.abs(v - 1) < 0.08); return +v.toFixed(6); };
    const drawInt = () => 1 + Math.floor(rnd() * 12);
    /* P32-expr-int: a symbol listed in `integers` takes six distinct whole numbers from 1 to 9 (its own fixed order, so two
       integer symbols differ), the rest keep 0.3 to 3. Own generator: draws for other symbols are unchanged. */
    const useInts = ints && ints.length ? vars.filter(v => ints.includes(v)) : [];
    const orders = {};
    useInts.forEach((v, j) => { let s2 = 1013 + 7919 * (j + 1); const r2 = () => { s2 = (s2 * 1103515245 + 12345) % 2147483648; return s2 / 2147483648; }; const pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]; for (let n = 8; n > 0; n--) { const m = Math.floor(r2() * (n + 1)); [pool[n], pool[m]] = [pool[m], pool[n]]; } orders[v] = pool; });
    const pts = !vars.length ? [null] : counting ? Array.from({ length: 24 }, () => Object.fromEntries(vars.map(v => [v, drawInt()]))) : Array.from({ length: 6 }, (_, i) => Object.fromEntries(vars.map(v => [v, orders[v] ? orders[v][i] : draw()])));
    let checked = 0, numeric = true;
    for (const p of pts) {
      const x = val(A, p), y = val(B, p), fx = fin(x), fy = fin(y);
      if (!fx && !fy) continue;
      if (counting && (!fx || !fy)) continue; // outside a factorial's domain (a negative factorial): not a counting point
      if (fx !== fy || !close(x[0], y[0]) || !close(x[1], y[1])) { numeric = false; break; }
      checked++;
    }
    if (!checked && numeric) return sym; // nothing numeric to compare: the symbolic answer stands
    if (counting && checked < 4 && numeric) return sym; // too few whole-number points where both sides are defined
    return numeric;
  };
  /* Item 429: real and imaginary parts are both compared at every seeded point. Item 433: a vector or matrix answer is
     compared entry by entry (the same shape is required), each entry by the same seeded-point method. */
  /* P32-expr-callhead: every comparison runs in its own scope, so a symbol the engine declares while parsing (a function
     after f(x)) cannot change what it means on the next screen. */
  const scoped = (ce, fn) => {
    let pushed = false;
    try { if (ce.pushScope) { ce.pushScope(); pushed = true; } } catch { pushed = false; }
    try { return fn(); } finally { if (pushed) { try { ce.popScope(); } catch { /* none */ } } }
  };
  /* withParsed(ce, s, functions, fn): fn(parsedExpression) in a scope, on the same prepared text the comparison reads */
  const withParsed = (ce, s, fns, fn) => scoped(ce, () => fn(ce.parse(prep(s, hasImag(s), fns))));
  const exprEqual = (ce, a, b, opts) => {
    if (!ce || a == null || b == null || a === '' || b === '') return false;
    return scoped(ce, () => exprEqualIn(ce, a, b, opts && opts.functions, opts && opts.integers));
  };
  const exprEqualIn = (ce, a, b, fns, ints) => {
    let A, B;
    const counting = /!|\\[dt]?binom|\\choose/.test(String(a) + String(b)); // factorials only evaluate at whole numbers
    const cx = hasImag(a) || hasImag(b);
    try { A = ce.parse(prep(a, cx, fns)); B = ce.parse(prep(b, cx, fns)); } catch { return false; }
    if (A.isValid === false || B.isValid === false) return false;
    let IA = null, IB = null;
    try { IA = itemsOf(ce, A); IB = itemsOf(ce, B); } catch { IA = IB = null; }
    if (IA || IB) return !!(IA && IB && sameShape(IA, IB) && IA.items.every((x, k) => scalarEqual(ce, x, IB.items[k], counting, cx, ints)));
    return scalarEqual(ce, A, B, counting, cx, ints);
  };

  /* Item 200: equal up to an added constant (antiderivatives). Symbols in the learner's answer that the target lacks
     (C, c, K) are set to 0, and the difference must be the same number at every sample point. */
  const exprEqualUpToConstant = (ce, a, b, opts) => {
    if (!ce || a == null || b == null || a === '' || b === '') return false;
    return scoped(ce, () => upToConstantIn(ce, a, b, opts && opts.functions, opts && opts.integers));
  };
  const upToConstantIn = (ce, a, b, fns, ints) => {
    let A, B;
    try { A = ce.parse(prep(a, undefined, fns)); B = ce.parse(prep(b, undefined, fns)); } catch { return false; }
    if (A.isValid === false || B.isValid === false) return false;
    let va = [], vb = [];
    try { va = [...(A.unknowns || [])]; vb = [...(B.unknowns || [])]; } catch { /* none */ }
    const extra = va.filter(v => !vb.includes(v)), vars = vb;
    const num = (E, sub) => { try { const v = E.subs(sub).N(); const x = v.re ?? v.valueOf(); return typeof x === 'number' ? x : NaN; } catch { return NaN; } };
    let seed = 7919; const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
    const pts = Array.from({ length: 6 }, (_, i) => Object.fromEntries([...vars.map((v, j) => { if (ints && ints.includes(v)) return [v, 1 + ((j * 4 + i * 5) % 9)]; let x; do { x = 0.3 + 2.7 * rnd(); } while (Math.abs(x - 1) < 0.08); return [v, +x.toFixed(6)]; }), ...extra.map(v => [v, 0])]));
    let d0 = null, checked = 0;
    for (const p of pts) {
      const x = num(A, p), y = num(B, p); if (!Number.isFinite(x) || !Number.isFinite(y)) { if (Number.isFinite(x) !== Number.isFinite(y)) return false; continue; }
      const d = x - y; if (d0 == null) d0 = d; else if (Math.abs(d - d0) > 1e-7 * Math.max(1, Math.abs(x), Math.abs(y))) return false;
      checked++;
    }
    return checked >= 3;
  };

  /* ---------- Authored answers, in the shape each widget's set() accepts ---------- */
  const manipulatePath = (spec) => {
    const S = spec.states || {}, start = spec.start, target = spec.target;
    const prev = { [start]: null }, q = [start];
    while (q.length) {
      const s = q.shift();
      if (s === target) break;
      const ops = ((S[s] || {}).ops || []).slice().sort((a, b) => (a.why ? 1 : 0) - (b.why ? 1 : 0));
      for (const op of ops) if (!op.reject && op.to != null && !(op.to in prev)) { prev[op.to] = s; q.push(op.to); }
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
      if (allowed.has('remove-unknown-part')) new Set([...Object.keys(L.u), ...Object.keys(R.u)]).forEach(lab => { // item 295: take the coefficient one pan has
        new Set([L.u[lab], R.u[lab]].filter(v => v && Math.abs(v) > 1e-9)).forEach(k => { const dec = (u) => { const o = { ...u, [lab]: r6((u[lab] || 0) - k) }; if (Math.abs(o[lab]) < 1e-9) delete o[lab]; return o; }; out.push([{ op: 'remove-unknown-part', n: lab, k }, { u: dec(L.u), w: L.w }, { u: dec(R.u), w: R.w }, true]); });
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
        (spec.rows || []).forEach((row, i) => row.forEach((c, j) => { if (c && typeof c === 'object' && c.edit) out[`r${i}c${j}`] = typeof c.answer === 'string' && !Number.isFinite(parseNum(c.answer)) ? c.answer : fmtNum(+c.answer); }));
        return out;
      }
      case 'manipulate': return manipulatePath(spec);
      case 'tap-regions': return spec.count != null && !(spec.answer || []).length ? (spec.among || []).slice(0, spec.count) : (spec.answer || []).slice();
      case 'slider': return spec.answer;
      case 'sliders': return Object.assign({}, spec.answer || spec.show || {});
      case 'drag-point': return Object.fromEntries((spec.points || []).map(p => [p.id, p.target && typeof p.target === 'object' && !Array.isArray(p.target) && (p.target.line || p.target.expr) ? (p.target.show || (p.target.line ? p.target.line[0] : [0, 0])) : p.target]));
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
  /* Maths is set aside as placeholders first, so **bold** and *italic* may wrap a formula ("**the mean $\mu$**").
     Code spans are set aside in the same left-to-right pass, so `$` and `*` inside backticks stay literal (item 104). */
  /* items 229, 246: a long inline formula (about 34 characters of rendered maths) gets lsn-wide: it may scroll
     sideways within the line's width on a phone instead of widening the order line, Why? sheet or model answer */
  const texLen = (t) => String(t).replace(/\\(?:frac|dfrac|tfrac|sqrt|left|right|mathrm|text|operatorname|mathbf|bigl|bigr|Bigl|Bigr)\b/g, '').replace(/\\[a-zA-Z]+/g, 'x').replace(/[{}^_\s]/g, '').length;
  const inline = (s, { br = false } = {}) => {
    const src = String(s ?? '');
    const maths = [];
    const held = src.replace(/`([^`\n]+)`|\$\$([^$]+)\$\$|\$([^$]+)\$([.,:;?)]?)/g, (all, c, d, t, p) => { maths.push(c != null ? `<code class="lsn-ic">${esc(c)}</code>` : d != null ? tex(d, true) : `<span class="lsn-nw${texLen(t) > 34 ? ' lsn-wide' : ''}">${tex(t, false)}${esc(p || '')}</span>`); return `\u0000${maths.length - 1}\u0000`; });
    let out = styleText(held);
    if (br) out = out.replace(/\n/g, '<br>'); // line breaks only outside maths: KaTeX SVG keeps its newlines
    return out.replace(/\u0000(\d+)\u0000/g, (_, k) => maths[+k]);
  };
  /* item 146: output-only blocks (```text, ```output) have nothing to copy, so no Copy button */
  const codeBlock = (code, lang) => `<div class="lsn-code${/^(text|output|out|plain)$/i.test(lang || '') ? ' is-output' : ''}" data-lang="${esc(lang || '')}">${/^(text|output|out|plain)$/i.test(lang || '') ? '' : '<button type="button" class="link-btn lsn-copy" aria-label="Copy code">Copy</button>'}<pre class="t-code"><code>${esc(code.replace(/\n$/, ''))}</code></pre></div>`;
  /* item 178: Markdown lists. Lines starting "- " or "* " make a bulleted list and "1. " a numbered one; other lines
     around them stay paragraphs */
  const LI = /^\s*(?:([-*])|(\d+)[.)])\s+(.*)$/;
  /* item 381: a Markdown table (| a | b | rows with a |---| separator line) in prose, item prompts and model answers */
  const isTableRow = (l) => /^\s*\|.*\|\s*$/.test(l);
  const cellsOf = (l) => l.trim().replace(/^\|/, '').replace(/\|$/, '').split(/(?<!\\)\|/).map((c) => c.trim().replace(/\\\|/g, '|'));
  const mdTable = (lines) => {
    const sep = cellsOf(lines[1]), align = sep.map((c) => (/^:-+:$/.test(c) ? 'center' : /^-+:$/.test(c) ? 'right' : 'left'));
    const head = cellsOf(lines[0]), body = lines.slice(2).map(cellsOf);
    const td = (t, k, tag) => `<${tag}${align[k] && align[k] !== 'left' ? ` style="text-align:${align[k]}"` : ''}>${inline(t)}</${tag}>`;
    return `<div class="lsn-mdtbl"><table><thead><tr>${head.map((t, k) => td(t, k, 'th')).join('')}</tr></thead><tbody>${body.map((r) => `<tr>${r.map((t, k) => td(t, k, 'td')).join('')}</tr>`).join('')}</tbody></table></div>`;
  };
  const block = (p, cls) => {
    const lines = p.split('\n');
    { const ti = lines.findIndex((l, i) => isTableRow(l) && lines[i + 1] != null && /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/.test(lines[i + 1]));
      if (ti >= 0) { let te = ti + 2; while (te < lines.length && isTableRow(lines[te])) te++; const before = lines.slice(0, ti).join('\n').trim(), after = lines.slice(te).join('\n').trim(); return (before ? block(before, cls) : '') + mdTable(lines.slice(ti, te)) + (after ? block(after, cls) : ''); } }
    if (!lines.some(l => LI.test(l) && !/^\s*\*\*/.test(l))) return `<p class="${cls}">${inline(p, { br: true })}</p>`;
    let out = '', para = [], list = null;
    const flushP = () => { if (para.length) out += `<p class="${cls}">${inline(para.join('\n'), { br: true })}</p>`; para = []; };
    const flushL = () => { if (list) out += `<${list.tag} class="lsn-list ${cls}">${list.items.map(t => `<li>${inline(t)}</li>`).join('')}</${list.tag}>`; list = null; };
    lines.forEach(l => {
      const m = l.match(LI);
      if (m && !/^\s*\*\*/.test(l)) { flushP(); const tag = m[2] ? 'ol' : 'ul'; if (!list || list.tag !== tag) { flushL(); list = { tag, items: [] }; } list.items.push(m[3]); }
      else if (list && /^\s{2,}\S/.test(l)) list.items[list.items.length - 1] += ' ' + l.trim(); // a wrapped item line
      else { flushL(); para.push(l); }
    });
    flushL(); flushP();
    return out;
  };
  /* Block copy: paragraphs split on blank lines, fenced code blocks, display maths. */
  const prose = (s, cls = 't-prose') => {
    const src = String(s ?? '');
    const parts = src.split(/```([\w+-]*)\n([\s\S]*?)```/g);
    let out = '';
    for (let i = 0; i < parts.length; i += 3) {
      parts[i].split(/\n\s*\n/).map(p => p.trim()).filter(Boolean).forEach(p => { out += block(p, cls); });
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
  window.ZQ.grade = { parseNum, within, matchWrong, sameSet, sameList, fmtNum, fmtFrac, fmtAs, normExpr, loadScript, maths, withParsed, exprEqual, exprShape, exprShapeLine, exprEqualUpToConstant, correctValue, manipulatePath, balanceMoves, sketchPoints, inline, prose, esc, patchCanvas, LIBS };
})();
