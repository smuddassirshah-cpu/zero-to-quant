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
     exprFormOk(ce, form, latex)   the shape check of form "factorised-fully" or "completed-square" (shapeFactorised, shapeFullyFactorised,
                                   shapeCompletedSquare are the same checks on MathJSON; ENGINE-BACKLOG 830, 831)
     exprSetGrade(ce, spec, text), numSetGrade(spec, text)   a set answer (spec.answers with unordered: true): { ok, key, line };
                                   the key "count" for a missing or extra value; \pm in the text stands for both values (832)
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
  /* ENGINE-BACKLOG 836: a plain-text function name directly before ( is the function, not a product of letters: ln(97)/ln(4) is
     \ln(97)/\ln(4), not 97/4. Names: ln, log, exp, sin, cos, tan, sqrt. Not touched: a name already behind a backslash (\ln), a name that is
     part of a longer word (arcsin(, sinh(, Dsin() and anything else, so a product of single letters such as s n (x) is still a product. */
  const PLAINFN = /(?<![A-Za-z\\])(ln|log|exp|sin|cos|tan|sqrt)(?=\s*\()/;
  const plainFns = (t) => {
    for (let guard = 0; guard < 60; guard++) {
      const m = PLAINFN.exec(t); if (!m) break;
      const at = m.index + m[0].length, o = /^\s*\(/.exec(t.slice(at));
      if (m[1] === 'sqrt') {
        const g = matching(t, at + o[0].length); if (!g) break;
        t = t.slice(0, m.index) + `\\sqrt{${t.slice(at + o[0].length, g.end - 1)}}` + t.slice(g.end);
      } else t = t.slice(0, m.index) + `\\${m[1]}` + t.slice(at);
    }
    return t;
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
      /* P32-expr-D: D and N are products, whatever follows (Dt, 4Dx, tD, N(0,1), D(t)). The engine reads D and N as its operators
         (D t is the tuple ["Tuple","D","t"]). A screen can keep the operator reading before a letter by listing "D" or "N" in `functions`. */
      .replace(/(?<!\\[A-Za-z]*)(?<!\\(?:mathbb|mathcal|mathrm|mathbf|mathit|mathsf|text|operatorname)\{)([ND])(?=([A-Za-z])?)/g, (m, c, nx) => (nx && (fns || []).includes(c) ? m : `\\mathrm{${c}}`));
    t = uncall(unexp(unbinom(minmax(plainFns(t)))), fns);
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
  const scalarEqual = (ce, A, B, counting, cx, ints, prop) => {
    let sym = false;
    if (!prop) { try { sym = !!A.simplify().isEqual(B.simplify()); } catch { sym = false; } }
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
    let checked = 0, numeric = true, k = null;
    for (const p of pts) {
      const x = val(A, p), y = val(B, p), fx = fin(x), fy = fin(y);
      if (!fx && !fy) continue;
      if (counting && (!fx || !fy)) continue; // outside a factorial's domain (a negative factorial): not a counting point
      if (prop) { /* item 618: equal up to one constant multiple k (x * k = y at every point); real values only */
        if (!fx || !fy || x[1] !== 0 || y[1] !== 0) { numeric = false; break; }
        const zx = Math.abs(x[0]) < 1e-12, zy = Math.abs(y[0]) < 1e-12;
        if (zx !== zy) { numeric = false; break; }
        if (!zx) { if (k == null) k = y[0] / x[0]; else if (!close(x[0] * k, y[0])) { numeric = false; break; } }
        checked++; continue;
      }
      if (fx !== fy || !close(x[0], y[0]) || !close(x[1], y[1])) { numeric = false; break; }
      checked++;
    }
    if (prop) return numeric && checked >= 3 ? { k: k == null ? 1 : k } : false; // both sides zero at every point: the same identity
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
  /* Item 618: equations and inequalities. splitRel(s) -> { l, r, rel } for one top-level relation (rel: eq, lt, le, ne; > and
     >= are turned round into lt and le), null for no relation, 'many' for a chain. Two relations are compared as equations
     by lhs - rhs: an equation equals another when one difference is a nonzero constant multiple of the other, an inequality
     only for the same kind and a positive multiple. Never by truth value at the sample points. */
  const RELS = /<=|>=|!=|\\(?:leqslant|geqslant|leq|geq|neq|le|ge|ne|lt|gt)(?![A-Za-z])|[<>=\u2264\u2265\u2260]/g;
  const splitRel = (s) => {
    const t = String(s); const hits = []; let depth = 0, m;
    const braces = []; for (let i = 0; i < t.length; i++) { if (t[i] === '{') depth++; else if (t[i] === '}') depth--; braces[i] = depth; }
    RELS.lastIndex = 0;
    while ((m = RELS.exec(t))) { if (m.index > 0 && t[m.index - 1] === '\\' && m[0].length === 1) continue; if (!braces[m.index]) hits.push({ i: m.index, tok: m[0] }); }
    if (!hits.length) return null;
    if (hits.length > 1) return 'many';
    const { i, tok } = hits[0], l = t.slice(0, i), r = t.slice(i + tok.length);
    const kind = { '=': 'eq', '<': 'lt', '\\lt': 'lt', '>': 'gt', '\\gt': 'gt', '<=': 'le', '\u2264': 'le', '\\le': 'le', '\\leq': 'le', '\\leqslant': 'le', '>=': 'ge', '\u2265': 'ge', '\\ge': 'ge', '\\geq': 'ge', '\\geqslant': 'ge', '!=': 'ne', '\u2260': 'ne', '\\ne': 'ne', '\\neq': 'ne' }[tok];
    if (!kind) return 'many';
    return kind === 'gt' ? { l: r, r: l, rel: 'lt' } : kind === 'ge' ? { l: r, r: l, rel: 'le' } : { l, r, rel: kind };
  };
  /* Item 620: what may stand beside the "=" and be dropped: a symbol (letter, Greek letter, \text{...}), optionally decorated
     (\hat, \bar, a prime), subscripted (S_\infty, u_{n+1}, x_{\text{max}}); or a call of such a head on symbols (f(x), g(t), f(x,y)). */
  const BRACED = '\\{(?:[^{}]|\\{[^{}]*\\})*\\}';
  const SYM0 = `(?:[A-Za-z]|\\\\(?:${GREEK})|\\\\(?:text|mathrm|operatorname)${BRACED})`;
  const SYM1 = `(?:(?:\\\\(?:hat|bar|tilde|vec|dot|overline)\\s*\\{\\s*${SYM0}\\s*\\})|${SYM0})`;
  const SUB = `(?:_(?:[A-Za-z0-9]|\\\\infty|\\\\(?:${GREEK})|${BRACED}))`;
  const SYM = `${SYM1}${SUB}?(?:'+|\\^\\*|\\^\\{\\\\prime\\}|\\^\\{\\*\\})?`;
  const SYMBOL = new RegExp(`^\\s*${SYM}\\s*$`);
  const CALLSYM = new RegExp(`^\\s*${SYM}\\s*(?:\\\\left\\s*)?\\(\\s*${SYM}(?:\\s*,\\s*${SYM})*\\s*(?:\\\\right\\s*)?\\)\\s*$`);
  /* a name of two or more letters (OB, TM, AB: a segment) is a label too, unless one of its letters is a symbol of the authored answer */
  const nameFree = (t, b) => /^\s*[A-Za-z]{2,}\s*$/.test(t) && !String(b).replace(/\\[A-Za-z]+/g, '').split('').some(c => /[A-Za-z]/.test(c) && t.includes(c));
  const isLabel = (t, b) => SYMBOL.test(t) || CALLSYM.test(t) || nameFree(t, b);
  const relEqual = (ce, ra, rb, cx, fns, ints) => {
    if (ra.rel !== rb.rel) return false;
    const diff = (x) => ce.parse(`\\left(${prep(x.l, cx, fns)}\\right)-\\left(${prep(x.r, cx, fns)}\\right)`);
    const A = diff(ra), B = diff(rb);
    if (A.isValid === false || B.isValid === false) return false;
    const res = scalarEqual(ce, A, B, false, cx, ints, true);
    if (!res || !(Math.abs(res.k) > 1e-12)) return false;
    return ra.rel === 'eq' || ra.rel === 'ne' || res.k > 0;
  };
  const exprEqualIn = (ce, a, b, fns, ints) => {
    const ra = splitRel(a), rb = splitRel(b);
    if (ra || rb) {
      const cx0 = hasImag(a) || hasImag(b);
      if (ra === 'many' || rb === 'many') return String(a).replace(/\s+/g, '') === String(b).replace(/\s+/g, '');
      try {
        if (ra && rb) return relEqual(ce, ra, rb, cx0, fns, ints);
        /* a lone letter and = before or after the learner's formula: grade the formula (answer has no =) */
        if (ra && ra.rel === 'eq') {
          const side = isLabel(ra.l, b) ? ra.r : isLabel(ra.r, b) ? ra.l : null;
          if (side != null && side.trim()) return exprEqualIn(ce, side, b, fns, ints);
          /* item 620: the learner restated the item's own expression ("(x+3)^3 = x^3+9x^2+27x+27"): both sides must be the same
             expression, and the side that is not the learner's own restatement must equal the answer */
          if (ra.l.trim() && ra.r.trim() && exprEqualIn(ce, ra.l, ra.r, fns, ints)) return exprEqualIn(ce, ra.r, b, fns, ints);
        }
      } catch { return false; }
      return false;
    }
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
    if (splitRel(a) || splitRel(b)) return false; // item 618: a relation has no "plus a constant"
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

  /* ---------- Answer shapes for expression `form` (ENGINE-BACKLOG 830, 831) ----------
     Pure functions on canonical MathJSON (the widget's e.json), shared by the expression widget and tools/test-answer-forms.mjs.
       shapeFactorised(j)       a product with a bracketed sum among its factors, or a power of one (a leading minus allowed)
       shapeFullyFactorised(j)  factorised, and no bracketed sum still holds a common whole-number factor or a quadratic that
                                factorises over the integers (rational roots, so (x^2-4), (4x^2-9) and (x^2+3x) all fail)
       shapeCompletedSquare(j)  a(x+p)^2 + q: one squared bracket x + p (x with coefficient 1), times a number a, plus a number q
                                in either order (q may be left out); a, p, q whole numbers, decimals or fractions */
  const jh = (j) => (Array.isArray(j) ? j[0] : null);
  const ja = (j) => (Array.isArray(j) ? j.slice(1) : []);
  const jLit = (j) => {                                         // a plain number's value, else null
    if (typeof j === 'number') return Number.isFinite(j) ? j : null;
    if (j && typeof j === 'object' && !Array.isArray(j) && 'num' in j) { const v = parseFloat(j.num); return Number.isFinite(v) ? v : null; }
    const h = jh(j), a = ja(j);
    if (h === 'Rational' || h === 'Divide') { const n = jLit(a[0]), d = jLit(a[1]); return n != null && d ? n / d : null; }
    if (h === 'Negate') { const v = jLit(a[0]); return v == null ? null : -v; }
    return null;
  };
  const jSum = (j) => (jh(j) === 'Add' ? ja(j) : jh(j) === 'Subtract' ? [ja(j)[0], ['Negate', ja(j)[1]]] : null);   // the terms of a sum, else null
  const jNeg = (j) => (jh(j) === 'Negate' ? ja(j)[0] : j);
  const shapeFactorised = (j) => {
    const r = jNeg(j);
    return (jh(r) === 'Multiply' && ja(r).some(f => jSum(f) || (jh(f) === 'Power' && jSum(ja(f)[0])))) || (jh(r) === 'Power' && !!jSum(ja(r)[0]));
  };
  const gcdI = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; };
  /* the whole-number coefficient of one term (2x gives 2, -x gives 1, 4 gives 4), or null when it is not a whole number */
  const termCoef = (t) => {
    const v = jLit(t); if (v != null) return Number.isInteger(v) ? Math.abs(v) : null;
    if (jh(t) === 'Negate') return termCoef(ja(t)[0]);
    if (jh(t) === 'Multiply') { let c = 1; for (const o of ja(t)) { const x = jLit(o); if (x != null) { if (!Number.isInteger(x)) return null; c *= Math.abs(x); } } return c; }
    return 1;
  };
  const commonNumber = (S) => { const co = jSum(S).map(termCoef); return co.length > 1 && co.every(c => c != null && c > 0) && co.reduce(gcdI) > 1; };
  const jSymbols = (j, out = new Set()) => { if (typeof j === 'string') { if (!/^(Pi|ExponentialE|ImaginaryUnit|iota)$/.test(j)) out.add(j); } else ja(j).forEach(x => jSymbols(x, out)); return out; };
  /* the coefficients [c0, c1, c2, ...] of a polynomial in the one symbol v, else null */
  const polyOf = (j, v) => {
    const add = (p, q) => Array.from({ length: Math.max(p.length, q.length) }, (_, i) => (p[i] || 0) + (q[i] || 0));
    const mul = (p, q) => { const r = Array(p.length + q.length - 1).fill(0); p.forEach((x, i) => q.forEach((y, k) => { r[i + k] += x * y; })); return r; };
    const go = (x) => {
      const n = jLit(x); if (n != null) return [n];
      if (x === v) return [0, 1];
      const h = jh(x), a = ja(x);
      if (h === 'Add') return a.reduce((s, t) => { const p = go(t); return s && p && add(s, p); }, [0]);
      if (h === 'Subtract') { const p = go(a[0]), q = go(a[1]); return p && q && add(p, q.map(c => -c)); }
      if (h === 'Negate') { const p = go(a[0]); return p && p.map(c => -c); }
      if (h === 'Multiply') return a.reduce((s, t) => { const p = go(t); return s && p && mul(s, p); }, [1]);
      if (h === 'Square') { const p = go(a[0]); return p && mul(p, p); }
      if (h === 'Power') { const e = jLit(a[1]), p = go(a[0]); if (!p || e == null || !Number.isInteger(e) || e < 0 || e > 6) return null; let r = [1]; for (let i = 0; i < e; i++) r = mul(r, p); return r; }
      return null;
    };
    const p = go(j);
    return p && p.every(Number.isFinite) ? p : null;
  };
  const quadFactorises = (S) => {
    const syms = [...jSymbols(S)]; if (syms.length !== 1) return false;
    const p = polyOf(S, syms[0]); if (!p) return false;
    while (p.length && Math.abs(p[p.length - 1]) < 1e-12) p.pop();
    if (p.length !== 3) return false;
    let m = 0; for (let k = 1; k <= 60 && !m; k++) if (p.every(c => Math.abs(c * k - Math.round(c * k)) < 1e-9)) m = k;
    if (!m) return false;
    const [c, b, a] = p.map(x => Math.round(x * m)), d = b * b - 4 * a * c;
    return d >= 0 && Number.isInteger(Math.sqrt(d));
  };
  const shapeFullyFactorised = (j) => {
    if (!shapeFactorised(j)) return false;
    const r = jNeg(j);
    return (jh(r) === 'Multiply' ? ja(r) : [r]).every(f => { const b = jh(f) === 'Power' ? ja(f)[0] : f; return !jSum(b) || !(commonNumber(b) || quadFactorises(b)); });
  };
  /* a (x + p)^2 as one term: an optional minus or number in front, then a square of a sum of the symbol and a number */
  const squareTerm = (t) => {
    let c = jNeg(t);
    if (jh(c) === 'Multiply') { const o = ja(c), rest = o.filter(x => jLit(x) == null); if (rest.length !== 1) return false; c = rest[0]; }
    else if (jh(c) === 'Divide' && jLit(ja(c)[1])) c = ja(c)[0];
    if (jh(c) === 'Negate') c = ja(c)[0];
    if (jh(c) !== 'Power' || jLit(ja(c)[1]) !== 2) return false;
    const o = jSum(ja(c)[0]); if (!o || o.length !== 2) return false;
    const [s, n] = typeof o[0] === 'string' ? [o[0], o[1]] : [o[1], o[0]];
    return typeof s === 'string' && !/^(Pi|ExponentialE|ImaginaryUnit|iota)$/.test(s) && jLit(n) != null;
  };
  const shapeCompletedSquare = (j) => {
    if (squareTerm(j)) return true;
    const o = jSum(j);
    return !!o && o.length === 2 && ((squareTerm(o[0]) && jLit(o[1]) != null) || (jLit(o[0]) != null && squareTerm(o[1])));
  };
  /* the whole check for the two new forms on typed LaTeX (the widget calls the same shape functions on its own parse) */
  const exprFormOk = (ce, form, latex, fns) => {
    if (!ce || (form !== 'factorised-fully' && form !== 'completed-square')) return true;
    try { return withParsed(ce, latex, fns, (e) => (form === 'factorised-fully' ? shapeFullyFactorised(e.json) : shapeCompletedSquare(e.json))); } catch { return true; }
  };

  /* ---------- Set answers (ENGINE-BACKLOG 832): answers: [...] with unordered: true ----------
     The learner types the values separated by commas (2, -5), or "x = 2 or x = -5", "x = 2 and x = -5", {2, -5}; a plus-or-minus
     (3 \pm \sqrt{2}, or ± or +- in a numeric field) stands for both values. Each value is graded as a single answer would be,
     in any order; a wrong number of values returns the key "count". */
  const SET_WORD = /(?<![A-Za-z\\])(?:or|and)(?![A-Za-z])/g;
  const unwrapOnce = (t, open, close) => {
    const s = t.trim();
    if (s[0] !== open || s[s.length - 1] !== close) return t;
    let d = 0;
    for (let i = 0; i < s.length; i++) { if (s[i] === open) d++; else if (s[i] === close) { d--; if (d === 0 && i < s.length - 1) return t; } }
    return d === 0 ? s.slice(1, -1) : t;
  };
  const setPieces = (text) => {
    let t = String(text ?? '')
      .replace(/\\(?:left|right)(?![A-Za-z])\s*/g, '').replace(/\\(?:lbrace|\{)/g, '\u0001').replace(/\\(?:rbrace|\})/g, '\u0002')
      .replace(/\{,\}/g, ',').replace(/\\[,;:! ]|~/g, ' ').replace(/[−–]/g, '-').replace(/±/g, '\\pm ')
      .replace(/\\(?:text|textrm|textbf|mathrm|operatorname|mbox)\s*\{\s*(or|and)\s*\}/g, ' $1 ').replace(/\\(?:lor|vee)(?![A-Za-z])/g, ' or ').replace(/\\(?:land|wedge)(?![A-Za-z])/g, ' and ');
    t = t.trim();
    if (t[0] === '\u0001' && t[t.length - 1] === '\u0002') t = t.slice(1, -1);
    t = t.replace(/[\u0001\u0002]/g, '');
    t = unwrapOnce(unwrapOnce(unwrapOnce(t, '{', '}'), '(', ')'), '[', ']');
    t = t.replace(SET_WORD, ',');
    const out = []; let depth = 0, cur = '';
    for (const ch of t) {
      if ('({['.includes(ch)) depth++; else if (')}]'.includes(ch)) depth--;
      if ((ch === ',' || ch === ';') && depth <= 0) { out.push(cur); cur = ''; } else cur += ch;
    }
    out.push(cur);
    return out.map(s => s.trim()).filter(Boolean);
  };
  const LABEL = /^\s*[A-Za-z](?:_(?:[A-Za-z0-9]|\{[^{}]*\}))?\s*=(?!=)\s*/;
  /* the values typed in an expression set: labels dropped, a \pm piece turned into its plus and minus values */
  const exprSetValues = (text) => {
    const out = [];
    setPieces(text).forEach((p) => {
      p = p.replace(LABEL, '');
      const parts = p.split(/\\pm(?![A-Za-z])/);
      if (parts.length === 1 || parts.length > 3) { out.push(p.trim()); return; }
      const signs = parts.length === 2 ? [['+'], ['-']] : [['+', '+'], ['+', '-'], ['-', '+'], ['-', '-']];
      signs.forEach(sg => out.push(parts.reduce((acc, part, i) => acc + (i ? sg[i - 1] : '') + part, '').trim()));
    });
    return out.filter(Boolean);
  };
  /* every pairing of the typed values with the keys, in any order: the equality is the caller's */
  const setMatch = (vals, keys, eq) => {
    if (vals.length !== keys.length) return false;
    const used = keys.map(() => false);
    const go = (i) => { if (i === vals.length) return true; for (let k = 0; k < keys.length; k++) if (!used[k] && eq(vals[i], keys[k])) { used[k] = true; if (go(i + 1)) return true; used[k] = false; } return false; };
    return go(0);
  };
  const countLine = (want, got) => `This question needs ${want} values, separated by commas. You gave ${got}.`;
  const isSetSpec = (spec) => !!spec && Array.isArray(spec.answers) && spec.answers.length > 0;
  const setAnswerText = (spec) => (spec.kind === 'numeric' ? spec.answers.map(a => fmtNum(+a)) : spec.answers.map(String)).join(', ');
  /* expression set: { ok, key, line } on the typed LaTeX (the answers and each wrong[].tex are comma-separated values) */
  const exprSetGrade = (ce, spec, text) => {
    const vals = exprSetValues(text), keys = spec.answers.map(String);
    if (!vals.length) return { ok: false, key: null };
    if (vals.length !== keys.length) return { ok: false, key: 'count', line: countLine(keys.length, vals.length) };
    const fo = { functions: Array.isArray(spec.functions) ? spec.functions : [], integers: Array.isArray(spec.integers) ? spec.integers : [] };
    const eq = (v, k) => (ce && exprEqual(ce, v, k, fo)) || (!!normExpr(v) && normExpr(v) === normExpr(k));
    if (setMatch(vals, keys, eq)) return { ok: true, key: null };
    const w = (spec.wrong || []).find(x => x && typeof x.tex === 'string' && setMatch(vals, exprSetValues(x.tex), eq));
    return { ok: false, key: w ? w.id : null };
  };
  /* numeric set: the typed text is split the same way; each value is a number (a leading "x =" dropped, a ± piece expanded) */
  const numSetValues = (text, { percent = false } = {}) => {
    const out = [];
    setPieces(String(text ?? '').replace(/\+\s*\/\s*[-−]|\+\s*-/g, '\\pm ')).forEach((p) => {
      p = p.replace(LABEL, '').replace(/^\+\s*/, '');
      const parts = p.split(/\\pm(?![A-Za-z])/);
      if (parts.length === 1) { out.push(parseNum(p, { percent })); return; }
      if (parts.length !== 2) { out.push(NaN); return; }
      const a = parts[0].trim() ? parseNum(parts[0], { percent }) : 0, b = parseNum(parts[1], { percent });
      out.push(a + b, a - b);
    });
    return out;
  };
  const numSetGrade = (spec, text) => {
    const vals = numSetValues(text, { percent: spec.unit === '%' });
    if (!vals.length) return { ok: false, key: null, detail: { value: null } };
    if (vals.some(v => !Number.isFinite(v))) return { ok: false, key: null, detail: { value: null } };
    const keys = spec.answers.map(Number);
    if (vals.length !== keys.length) return { ok: false, key: 'count', line: countLine(keys.length, vals.length), detail: { value: vals } };
    const eq = (tol) => (v, k) => within(v, k, tol);
    if (setMatch(vals, keys, eq(spec.tol))) return { ok: true, key: null, detail: { value: vals } };
    const w = (spec.wrong || []).find((x) => {
      if (!x || x.value == null) return false;
      const wv = typeof x.value === 'string' ? numSetValues(x.value).filter(Number.isFinite) : [+x.value];
      return setMatch(vals, wv, eq(x.tol ?? { abs: 1e-9 }));
    });
    return { ok: false, key: w ? w.id : null, detail: { value: vals } };
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
      case 'numeric': return isSetSpec(spec) ? setAnswerText(spec) : spec.unit === '%' ? fmtNum(spec.answer * 100) : fmtNum(+spec.answer);
      case 'expression': return isSetSpec(spec) ? setAnswerText(spec) : spec.answer;
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
  window.ZQ.grade = { plainFns, parseNum, within, matchWrong, sameSet, sameList, fmtNum, fmtFrac, fmtAs, normExpr, loadScript, maths, withParsed, exprEqual, splitRel, exprShape, exprShapeLine, exprEqualUpToConstant, shapeFactorised, shapeFullyFactorised, shapeCompletedSquare, exprFormOk, setPieces, exprSetValues, setMatch, isSetSpec, setAnswerText, exprSetGrade, numSetValues, numSetGrade, countLine, correctValue, manipulatePath, balanceMoves, sketchPoints, inline, prose, esc, patchCanvas, LIBS };
})();
