/* Generated fluency sets (ENGINE-BACKLOG 800 to 819; author side docs/AUTHORING.md section 16).
   Pure functions, no DOM: loaded by index.html as ZQ.gen and by the node tools (validate, fluency-sample, test-fluency) with
   require('../js/engine/gen.js'). A fluency set is JSON only (content/courses/<course>/fluency-<lesson>.json): families of
   items whose numbers are drawn from a seeded generator, so there is no engine code per family.
     ZQ.gen.parse(src)                         an expression string to a syntax tree (throws GenError)
     ZQ.gen.evaluate(src | tree, env)          the value: an exact rational { n, d } (BigInt), a float (number), a string or a boolean
     ZQ.gen.template(src)                      a compiled template: literal text and {expression:format} placeholders
     ZQ.gen.render(tpl, env, mode)             the text; mode 'tex' (default) or 'num' (a number the numeric widget can read)
     ZQ.gen.format(value, spec)                one value through a format ("+", "c", "+c", "()", "frac", "+frac", "dp2", "+dp2")
     ZQ.gen.checkFamily(family)                the static problems of a family (messages), none when it is well formed
     ZQ.gen.draw(family, rng, opts)            one item { family, vars, lets, prompt, widget, wrong, solution } or { rejected }
     ZQ.gen.generate(set, seed, { n })         the items of one attempt: families round robin by weight, no repeated prompt
     ZQ.gen.sample(family, { seeds, set })     the statistics the validator reads: distinct prompts, rejects, errors, items
     ZQ.gen.playerItem(item, set, k)           an item in the shape ZQ.player.runSet takes (feedback, explain, widget)
     ZQ.gen.rng(seed)                          the seeded generator (ZQ.arith.rng, mulberry32), one stream per string seed
   No eval and no Function: the evaluator is a small recursive-descent parser over + - * / ^ %, comparisons, and / or / not,
   and the functions gcd lcm abs min max floor ceil round sqrt comb fact sign. Numbers are exact rationals (BigInt) until a
   square root or a fractional power makes a float. */
(function (root) {
  'use strict';

  class GenError extends Error {}
  const bad = (m) => { throw new GenError(m); };

  /* ---------- The seeded generator: ZQ.arith.rng in the browser, the same file loaded in a sandbox in node ---------- */
  const arith = () => {
    if (root && root.ZQ && root.ZQ.arith) return root.ZQ.arith;
    if (typeof module !== 'undefined' && module.exports && typeof require === 'function') {
      if (!arith.cached) {
        const fs = require('fs'), vm = require('vm'), path = require('path');
        const g = { fetch: () => Promise.reject(new Error('no network')), console };
        g.window = g; vm.createContext(g);
        vm.runInContext(fs.readFileSync(path.join(__dirname, 'arith.js'), 'utf8'), g, { filename: 'arith.js' });
        arith.cached = g.ZQ.arith;
      }
      return arith.cached;
    }
    return null;
  };
  const rng = (seed) => { const A = arith(); return A.rng(typeof seed === 'number' ? seed : A.seedOf(String(seed))); };

  /* ---------- Exact rationals ---------- */
  const babs = (a) => (a < 0n ? -a : a);
  const bgcd = (a, b) => { a = babs(a); b = babs(b); while (b) { [a, b] = [b, a % b]; } return a; };
  const Q = (n, d = 1n) => {
    if (d === 0n) bad('division by zero');
    if (d < 0n) { n = -n; d = -d; }
    const g = bgcd(n, d) || 1n;
    return { n: n / g, d: d / g };
  };
  const isQ = (v) => v !== null && typeof v === 'object' && typeof v.n === 'bigint';
  const isNum = (v) => isQ(v) || typeof v === 'number';
  const isInt = (v) => isQ(v) && v.d === 1n;
  const toF = (v) => (isQ(v) ? Number(v.n) / Number(v.d) : v);
  const fromDecimal = (s) => {
    const m = /^(-?)(\d+)(?:\.(\d+))?$/.exec(s);
    if (!m) bad(`not a number: ${s}`);
    const frac = m[3] || '';
    const n = BigInt(m[2] + frac), d = 10n ** BigInt(frac.length);
    return Q(m[1] ? -n : n, d);
  };
  /* a JavaScript number from the content (a vars pick) to a rational, through its shortest decimal text */
  const fromJS = (x) => {
    if (typeof x === 'string') return x;
    if (!Number.isFinite(x)) bad('a non-finite number');
    if (Number.isInteger(x)) return Q(BigInt(x));
    const s = String(x);
    if (/e/i.test(s)) return fromDecimal(x.toFixed(12).replace(/0+$/, ''));
    return fromDecimal(s);
  };
  const cmpQ = (a, b) => { const l = a.n * b.d, r = b.n * a.d; return l < r ? -1 : l > r ? 1 : 0; };
  const cmpNum = (a, b) => (isQ(a) && isQ(b) ? cmpQ(a, b) : toF(a) < toF(b) ? -1 : toF(a) > toF(b) ? 1 : 0);
  const bisqrt = (n) => { if (n < 2n) return n; let x = BigInt(Math.floor(Math.sqrt(Number(n)))); while (x * x > n) x--; while ((x + 1n) * (x + 1n) <= n) x++; return x; };
  const MAXDIG = 400;                                    // a power or factorial that would pass this many digits is an error, not a stall
  const needNum = (v, what) => { if (!isNum(v)) bad(`${what} needs numbers`); return v; };
  const needInt = (v, what) => { if (!isInt(v)) bad(`${what} needs a whole number`); return v.n; };

  /* ---------- Tokens and the parser ---------- */
  const TOKEN = /\s*(?:(\d+(?:\.\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|'([^']*)'|(==|!=|<=|>=|[-+*\/^%(),<>])|(=))/y;
  const tokens = (src) => {
    const out = []; TOKEN.lastIndex = 0;
    const s = String(src);
    let m, pos = 0;
    while (pos < s.length && /\S/.test(s.slice(pos))) {
      TOKEN.lastIndex = pos; m = TOKEN.exec(s);
      if (!m) bad(`cannot read "${s.slice(pos).trim().slice(0, 12)}" in "${s}"`);
      pos = TOKEN.lastIndex;
      if (m[1] !== undefined) out.push({ t: 'num', v: m[1] });
      else if (m[2] !== undefined) out.push({ t: 'id', v: m[2] });
      else if (m[3] !== undefined) out.push({ t: 'str', v: m[3] });
      else if (m[4] !== undefined) out.push({ t: 'op', v: m[4] });
      else bad(`a single = is not an operator in "${s}" (write == to compare)`);
    }
    return out;
  };
  const KEYWORDS = new Set(['and', 'or', 'not']);
  const parse = (src) => {
    const tk = tokens(src); let i = 0;
    const peek = () => tk[i], op = (v) => tk[i] && tk[i].t === 'op' && tk[i].v === v, kw = (v) => tk[i] && tk[i].t === 'id' && tk[i].v === v;
    const eat = (v) => { if (!op(v)) bad(`expected "${v}" in "${src}"`); i++; };
    const orE = () => { let a = andE(); while (kw('or')) { i++; a = { t: 'bin', op: 'or', a, b: andE() }; } return a; };
    const andE = () => { let a = notE(); while (kw('and')) { i++; a = { t: 'bin', op: 'and', a, b: notE() }; } return a; };
    const notE = () => { if (kw('not')) { i++; return { t: 'un', op: 'not', a: notE() }; } return cmpE(); };
    const cmpE = () => {
      const a = addE();
      const t = peek();
      if (t && t.t === 'op' && ['==', '!=', '<', '<=', '>', '>='].includes(t.v)) { i++; return { t: 'bin', op: t.v, a, b: addE() }; }
      return a;
    };
    const addE = () => { let a = mulE(); while (op('+') || op('-')) { const o = tk[i++].v; a = { t: 'bin', op: o, a, b: mulE() }; } return a; };
    const mulE = () => { let a = unE(); while (op('*') || op('/') || op('%')) { const o = tk[i++].v; a = { t: 'bin', op: o, a, b: unE() }; } return a; };
    const unE = () => { if (op('-')) { i++; return { t: 'un', op: '-', a: unE() }; } if (op('+')) { i++; return unE(); } return powE(); };
    const powE = () => { const a = atom(); if (op('^')) { i++; return { t: 'bin', op: '^', a, b: unE() }; } return a; };
    const atom = () => {
      const t = tk[i++];
      if (!t) bad(`"${src}" ends too soon`);
      if (t.t === 'num') return { t: 'num', v: fromDecimal(t.v) };
      if (t.t === 'str') return { t: 'str', v: t.v };
      if (t.t === 'id') {
        if (KEYWORDS.has(t.v)) bad(`"${t.v}" is not allowed here in "${src}"`);
        if (op('(')) {
          i++; const args = [];
          if (!op(')')) { for (;;) { args.push(orE()); if (op(',')) { i++; continue; } break; } }
          eat(')');
          return { t: 'call', name: t.v, args };
        }
        return { t: 'id', name: t.v };
      }
      if (t.t === 'op' && t.v === '(') { const e = orE(); eat(')'); return e; }
      bad(`unexpected "${t.v}" in "${src}" (a product needs a * : write 2*a, not 2a)`);
    };
    const tree = orE();
    if (i < tk.length) bad(`unexpected "${tk[i].v}" in "${src}"${tk[i].t !== 'op' || tk[i].v === '(' ? ' (a product needs a *: write 2*a, not 2a)' : ''}`);
    return tree;
  };

  /* ---------- Functions ---------- */
  const roundHalfAway = (n, d) => { const q = (2n * babs(n) + d) / (2n * d); return n < 0n ? -q : q; };   // n/d (d > 0) to a whole number
  const FUNCS = {
    gcd: { min: 2, f: (a) => Q(a.map((v) => needInt(v, 'gcd')).reduce((x, y) => bgcd(x, y), 0n)) },
    lcm: { min: 2, f: (a) => Q(a.map((v) => needInt(v, 'lcm')).reduce((x, y) => (x === 0n || y === 0n ? 0n : babs(x * y) / bgcd(x, y)), 1n)) },
    abs: { n: 1, f: ([v]) => (isQ(needNum(v, 'abs')) ? Q(babs(v.n), v.d) : Math.abs(v)) },
    sign: { n: 1, f: ([v]) => Q(BigInt(cmpNum(needNum(v, 'sign'), Q(0n)))) },
    min: { min: 1, f: (a) => a.map((v) => needNum(v, 'min')).reduce((x, y) => (cmpNum(y, x) < 0 ? y : x)) },
    max: { min: 1, f: (a) => a.map((v) => needNum(v, 'max')).reduce((x, y) => (cmpNum(y, x) > 0 ? y : x)) },
    floor: { n: 1, f: ([v]) => { needNum(v, 'floor'); if (!isQ(v)) return Q(BigInt(Math.floor(v))); const q = v.n / v.d; return Q(v.n < 0n && v.n % v.d !== 0n ? q - 1n : q); } },
    ceil: { n: 1, f: ([v]) => { needNum(v, 'ceil'); if (!isQ(v)) return Q(BigInt(Math.ceil(v))); const q = v.n / v.d; return Q(v.n > 0n && v.n % v.d !== 0n ? q + 1n : q); } },
    round: { min: 1, max: 2, f: ([v, dp]) => {
      needNum(v, 'round');
      const k = dp === undefined ? 0 : Number(needInt(dp, 'round (decimal places)'));
      if (k < 0 || k > 10) bad('round takes 0 to 10 decimal places');
      const scale = 10n ** BigInt(k);
      const q = isQ(v) ? v : fromDecimal(v.toFixed(Math.min(12, k + 6)));
      return Q(roundHalfAway(q.n * scale, q.d), scale);
    } },
    sqrt: { n: 1, f: ([v]) => {
      needNum(v, 'sqrt');
      if (cmpNum(v, Q(0n)) < 0) bad('sqrt of a negative number');
      if (isQ(v)) { const a = bisqrt(v.n), b = bisqrt(v.d); if (a * a === v.n && b * b === v.d) return Q(a, b); }
      return Math.sqrt(toF(v));
    } },
    comb: { n: 2, f: ([a, b]) => {
      const n = needInt(a, 'comb'), k = needInt(b, 'comb');
      if (n < 0n || k < 0n) bad('comb needs non-negative whole numbers');
      if (k > n) return Q(0n);
      if (n > 1000n) bad('comb: n is at most 1000');
      let r = 1n; const kk = k > n - k ? n - k : k;
      for (let i = 1n; i <= kk; i++) r = (r * (n - kk + i)) / i;
      return Q(r);
    } },
    fact: { n: 1, f: ([a]) => {
      const n = needInt(a, 'fact');
      if (n < 0n || n > 170n) bad('fact takes 0 to 170');
      let r = 1n; for (let i = 2n; i <= n; i++) r *= i;
      return Q(r);
    } },
  };
  const FUNC_NAMES = Object.keys(FUNCS);

  /* ---------- Evaluation ---------- */
  const arithmetic = (o, a, b) => {
    needNum(a, `"${o}"`); needNum(b, `"${o}"`);
    if (isQ(a) && isQ(b)) {
      if (o === '+') return Q(a.n * b.d + b.n * a.d, a.d * b.d);
      if (o === '-') return Q(a.n * b.d - b.n * a.d, a.d * b.d);
      if (o === '*') return Q(a.n * b.n, a.d * b.d);
      if (o === '/') return Q(a.n * b.d, a.d * b.n);
    }
    const x = toF(a), y = toF(b);
    const r = o === '+' ? x + y : o === '-' ? x - y : o === '*' ? x * y : x / y;
    if (!Number.isFinite(r)) bad('a result that is not a finite number');
    return r;
  };
  const power = (a, b) => {
    needNum(a, '"^"'); needNum(b, '"^"');
    if (isQ(a) && isInt(b)) {
      const e = b.n < 0n ? -b.n : b.n;
      if (e > 400n) bad('an exponent above 400');
      if (a.n === 0n && b.n < 0n) bad('division by zero');
      if (a.n !== 0n && (BigInt(String(babs(a.n)).length) + BigInt(String(a.d).length)) * e > BigInt(MAXDIG) * 4n) bad('a power that is too large');
      const p = Q(a.n ** e, a.d ** e);
      return b.n < 0n ? Q(p.d, p.n) : p;
    }
    const r = Math.pow(toF(a), toF(b));
    if (!Number.isFinite(r)) bad('a power that is undefined');
    return r;
  };
  const evalTree = (n, env) => {
    switch (n.t) {
      case 'num': return n.v;
      case 'str': return n.v;
      case 'id': {
        if (!Object.prototype.hasOwnProperty.call(env, n.name)) bad(`unknown name "${n.name}"`);
        return env[n.name];
      }
      case 'un': {
        const v = evalTree(n.a, env);
        if (n.op === 'not') { if (typeof v !== 'boolean') bad('not needs a true or false value'); return !v; }
        needNum(v, 'unary minus');
        return isQ(v) ? Q(-v.n, v.d) : -v;
      }
      case 'call': {
        const f = FUNCS[n.name];
        if (!f) bad(`unknown function "${n.name}" (the functions are ${FUNC_NAMES.join(', ')})`);
        const nargs = n.args.length;
        if ((f.n !== undefined && nargs !== f.n) || (f.min !== undefined && nargs < f.min) || (f.max !== undefined && nargs > f.max)) bad(`${n.name} takes ${f.n !== undefined ? f.n : f.max !== undefined ? `${f.min} or ${f.max}` : `at least ${f.min}`} argument${f.n === 1 ? '' : 's'}`);
        return f.f(n.args.map((x) => evalTree(x, env)));
      }
      case 'bin': {
        const o = n.op;
        if (o === 'and' || o === 'or') {
          const a = evalTree(n.a, env);
          if (typeof a !== 'boolean') bad(`${o} needs true or false values`);
          if (o === 'and' && !a) return false;
          if (o === 'or' && a) return true;
          const b = evalTree(n.b, env);
          if (typeof b !== 'boolean') bad(`${o} needs true or false values`);
          return b;
        }
        const a = evalTree(n.a, env), b = evalTree(n.b, env);
        if (o === '==' || o === '!=') {
          const eq = isNum(a) && isNum(b) ? cmpNum(a, b) === 0 : a === b;
          return o === '==' ? eq : !eq;
        }
        if (o === '<' || o === '<=' || o === '>' || o === '>=') {
          needNum(a, `"${o}"`); needNum(b, `"${o}"`);
          const c = cmpNum(a, b);
          return o === '<' ? c < 0 : o === '<=' ? c <= 0 : o === '>' ? c > 0 : c >= 0;
        }
        if (o === '^') return power(a, b);
        if (o === '%') {
          const x = needInt(a, '%'), y = needInt(b, '%');
          if (y === 0n) bad('division by zero');
          const r = x % y;
          return Q(r !== 0n && (r < 0n) !== (y < 0n) ? r + y : r);
        }
        return arithmetic(o, a, b);
      }
      default: bad('unknown syntax');
    }
  };
  const cache = new Map();
  const treeOf = (src) => { if (typeof src !== 'string') return src; let t = cache.get(src); if (!t) { t = parse(src); cache.set(src, t); } return t; };
  const evaluate = (src, env = {}) => evalTree(treeOf(src), env);
  /* the names and function names an expression mentions, for the validator's static checks */
  const refs = (src) => {
    const ids = new Set(), fns = new Set();
    const walk = (n) => { if (n.t === 'id') ids.add(n.name); else if (n.t === 'call') { fns.add(n.name); n.args.forEach(walk); } else if (n.t === 'bin') { walk(n.a); walk(n.b); } else if (n.t === 'un') walk(n.a); };
    walk(treeOf(src));
    return { ids, fns };
  };

  /* ---------- Formatting ---------- */
  const TERMINATING = (d) => { while (d % 2n === 0n) d /= 2n; while (d % 5n === 0n) d /= 5n; return d === 1n; };
  const decimalOf = (q) => {            // a terminating rational as decimal text (the sign included)
    const neg = q.n < 0n, n = babs(q.n);
    let k = 0, scale = 1n;
    while ((n * scale) % q.d !== 0n) { scale *= 10n; k++; }
    const digits = ((n * scale) / q.d).toString().padStart(k + 1, '0');
    return (neg ? '-' : '') + (k ? `${digits.slice(0, -k)}.${digits.slice(-k)}` : digits);
  };
  const floatText = (x) => {
    if (x === 0) return '0';
    let s = String(parseFloat(x.toPrecision(12)));
    if (/e/i.test(s)) s = x.toFixed(12).replace(/0+$/, '').replace(/\.$/, '');
    return s;
  };
  const fracText = (q) => (q.d === 1n ? q.n.toString() : `${q.n < 0n ? '-' : ''}\\frac{${babs(q.n)}}{${q.d}}`);
  const plain = (v, mode) => {
    if (typeof v === 'string') return v;
    if (typeof v === 'boolean') bad('a true or false value cannot be written into text');
    if (typeof v === 'number') return floatText(v);
    if (v.d === 1n) return v.n.toString();
    if (mode === 'num') return TERMINATING(v.d) && v.d <= 10n ** 12n ? decimalOf(v) : `${v.n}/${v.d}`;
    return TERMINATING(v.d) && v.d <= 10n ** 12n ? decimalOf(v) : fracText(v);
  };
  const absOf = (v) => (isQ(v) ? Q(babs(v.n), v.d) : Math.abs(v));
  const negative = (v) => (isQ(v) ? v.n < 0n : v < 0);
  const fixed = (v, k) => {
    if (isQ(v)) {
      const scale = 10n ** BigInt(k), r = roundHalfAway(babs(v.n) * scale, v.d);
      const s = r.toString().padStart(k + 1, '0');
      return (v.n < 0n && r !== 0n ? '-' : '') + (k ? `${s.slice(0, -k)}.${s.slice(-k)}` : s);
    }
    const t = v.toFixed(k);
    return /^-0(\.0*)?$/.test(t) ? t.slice(1) : t;
  };
  const SPEC = /^(\+)?(c|\(\)|frac|dp(\d+))?$/;
  /* One value through a format. spec: "" plain, "+" signed, "c" coefficient, "+c", "()", "frac", "+frac", "dpN", "+dpN". */
  const format = (v, spec = '', mode = 'tex') => {
    const m = SPEC.exec(spec);
    if (!m) bad(`unknown format ":${spec}" (the formats are +, c, +c, (), frac, +frac, dpN, +dpN)`);
    const signed = !!m[1], kind = m[2] || '';
    if (kind === '()' && signed) bad('the format "+()" does not exist');
    if (typeof v === 'string' && (signed || kind)) bad(`a format cannot be applied to the text "${v}"`);
    if (typeof v === 'boolean') bad('a true or false value cannot be written into text');
    let body;
    const mag = signed ? absOf(v) : v;
    if (kind === 'c') {
      if (isQ(v) && v.d === 1n && (v.n === 1n || v.n === -1n)) body = signed ? '' : (v.n === 1n ? '' : '-');
      else body = plain(mag, mode);
    } else if (kind === 'frac') body = isQ(mag) ? fracText(mag) : plain(mag, mode);
    else if (kind.startsWith('dp')) { const k = Number(m[3]); if (k > 10) bad('dp takes 0 to 10'); body = fixed(mag, k); }
    else if (kind === '()') { const t = plain(v, mode); return negative(v) ? `(${t})` : t; }
    else body = plain(mag, mode);
    if (signed) return (negative(v) ? '-' : '+') + body;
    return body;
  };

  /* poly(v; c2, c1, c0): a clean polynomial, highest power first */
  const polyText = (variable, coefs) => {
    let out = '';
    const deg = coefs.length - 1;
    coefs.forEach((c, i) => {
      if (!isQ(c)) bad('poly needs exact coefficients (no square roots or fractional powers)');
      if (c.n === 0n) return;
      const p = deg - i, a = Q(babs(c.n), c.d);
      const one = a.n === 1n && a.d === 1n;
      const num = one && p > 0 ? '' : plain(a, 'tex');
      const v = p === 0 ? '' : p === 1 ? variable : `${variable}^${p > 9 ? `{${p}}` : p}`;
      out += (c.n < 0n ? '-' : out ? '+' : '') + num + v;
    });
    return out || '0';
  };

  /* ---------- Templates ---------- */
  const splitTop = (s, ch) => {
    const out = []; let depth = 0, from = 0, q = false;
    for (let i = 0; i < s.length; i++) {
      const c = s[i];
      if (c === "'") q = !q;
      if (q) continue;
      if (c === '(') depth++; else if (c === ')') depth--;
      else if (c === ch && depth === 0) { out.push(s.slice(from, i)); from = i + 1; }
    }
    out.push(s.slice(from));
    return out;
  };
  const placeholder = (body) => {
    const t = body.trim();
    if (/^poly\s*\(/.test(t)) {
      if (!t.endsWith(')')) bad(`poly( is not closed in "{${body}}"`);
      const inner = t.slice(t.indexOf('(') + 1, -1), semi = inner.indexOf(';');
      if (semi < 0) bad(`poly needs "poly(v; c2, c1, c0)" in "{${body}}"`);
      const v = inner.slice(0, semi).trim(), cs = splitTop(inner.slice(semi + 1), ',').map((x) => x.trim());
      if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(v)) bad(`poly needs a variable name or a letter before the ";" in "{${body}}"`);
      if (cs.some((x) => !x)) bad(`poly has an empty coefficient in "{${body}}"`);
      return { poly: { v, coefs: cs.map((x) => parse(x)) } };
    }
    const colon = splitTop(t, ':');
    if (colon.length > 2) bad(`more than one ":" in "{${body}}"`);
    const spec = colon.length === 2 ? colon[1].trim() : '';
    if (colon.length === 2) { const m = SPEC.exec(spec); if (!m || spec === '' || (m[1] && m[2] === '()')) bad(`unknown format ":${spec}" in "{${body}}" (the formats are +, c, +c, (), frac, +frac, dpN, +dpN)`); }
    if (!colon[0].trim()) bad('an empty {} in a template (write {{ and }} for a literal brace)');
    return { expr: parse(colon[0]), spec, src: colon[0].trim() };
  };
  /* literal text and placeholders; "{{" and "}}" are literal braces, so LaTeX is written \\frac{{1}}{{2}} */
  const template = (src) => {
    const s = String(src), parts = []; let lit = '', i = 0;
    while (i < s.length) {
      const c = s[i];
      if (c === '{' && s[i + 1] === '{') { lit += '{'; i += 2; }
      else if (c === '}' && s[i + 1] === '}') { lit += '}'; i += 2; }
      else if (c === '{') {
        let depth = 0, j = i;
        for (; j < s.length; j++) { if (s[j] === '{') depth++; else if (s[j] === '}') { depth--; if (depth === 0) break; } }
        if (j >= s.length) bad(`a "{" is never closed in "${s}" (write {{ for a literal brace)`);
        if (lit) { parts.push({ lit }); lit = ''; }
        parts.push(placeholder(s.slice(i + 1, j)));
        i = j + 1;
      } else if (c === '}') bad(`a stray "}" in "${s}" (write }} for a literal brace)`);
      else { lit += c; i++; }
    }
    if (lit) parts.push({ lit });
    return { src: s, parts };
  };
  const tcache = new Map();
  const tplOf = (t) => { if (typeof t !== 'string') return t; let c = tcache.get(t); if (!c) { c = template(t); tcache.set(t, c); } return c; };
  const render = (tpl, env, mode = 'tex') => tplOf(tpl).parts.map((p) => {
    if (p.lit !== undefined) return p.lit;
    if (p.poly) {
      const v = Object.prototype.hasOwnProperty.call(env, p.poly.v) ? env[p.poly.v] : p.poly.v;
      return polyText(typeof v === 'string' ? v : plain(v, 'tex'), p.poly.coefs.map((c) => evalTree(c, env)));
    }
    return format(evalTree(p.expr, env), p.spec, mode);
  }).join('');
  const templateRefs = (src) => {
    const ids = new Set(), fns = new Set();
    const add = (t) => { const r = refs(t); r.ids.forEach((x) => ids.add(x)); r.fns.forEach((x) => fns.add(x)); };
    tplOf(src).parts.forEach((p) => { if (p.expr) add(p.expr); else if (p.poly) { p.poly.coefs.forEach(add); } });
    tplOf(src).parts.forEach((p) => { if (p.poly) ids.add(`poly:${p.poly.v}`); });
    return { ids, fns };
  };

  /* ---------- Families ---------- */
  const VAR_NAME = /^[a-z][A-Za-z0-9_]*$/;
  const KEBAB = /^[a-z0-9]+(-[a-z0-9]+)*$/;
  const WIDGET_FIELDS = {
    numeric: ['kind', 'answer', 'tol', 'tolerance', 'unit', 'placeholder', 'accept', 'label'],
    expression: ['kind', 'answer', 'accept', 'form', 'upToConstant', 'tolerance', 'integers', 'functions', 'keyboard', 'label'],
  };
  const FORMS = ['expanded', 'factorised', 'simplified', 'rectangular'];
  const reserved = (n) => KEYWORDS.has(n) || FUNCS[n];
  const intRange = (v) => Array.isArray(v) && v.length === 2 && v.every((x) => Number.isInteger(x)) && v[0] <= v[1];
  const varValues = (spec) => {         // every value a var can take, or null when the range is too wide to list (the static check then only counts)
    const not = (Array.isArray(spec.not) ? spec.not : []).map((x) => String(x));
    if (spec.pick) return spec.pick.filter((x) => !not.includes(String(x)));
    const [lo, hi] = spec.int, step = spec.step || 1, out = [];
    for (let x = lo; x <= hi; x += step) if (!not.includes(String(x))) out.push(x);
    return out;
  };
  const tplMsgs = (msgs, where, text, known, vars) => {
    if (typeof text !== 'string') { msgs.push(`${where}: must be text`); return; }
    try {
      const r = templateRefs(text);
      r.ids.forEach((id) => {
        if (id.startsWith('poly:')) return;
        if (!known.has(id)) msgs.push(`${where}: "${id}" is neither a var nor a let (${[...known].join(', ') || 'none defined'})`);
      });
      r.fns.forEach((f) => { if (!FUNCS[f]) msgs.push(`${where}: unknown function "${f}"`); });
    } catch (e) { msgs.push(`${where}: ${e.message}`); }
  };
  /* The static problems of one family (what can be seen without drawing): messages, none when it is well formed */
  const checkFamily = (f) => {
    const msgs = [];
    if (!f || typeof f !== 'object' || Array.isArray(f)) return ['the family must be an object'];
    if (typeof f.id !== 'string' || !KEBAB.test(f.id)) msgs.push('id must be kebab-case text');
    if (f.weight !== undefined && !(typeof f.weight === 'number' && f.weight > 0 && f.weight <= 20)) msgs.push('weight is a number above 0 and at most 20');
    if (f.skill !== undefined && (typeof f.skill !== 'string' || !f.skill.trim())) msgs.push('skill is a short phrase of text');
    const known = new Set();
    if (!f.vars || typeof f.vars !== 'object' || Array.isArray(f.vars)) msgs.push('vars must be an object');
    else {
      Object.entries(f.vars).forEach(([name, spec]) => {
        const w = `vars.${name}`;
        if (!VAR_NAME.test(name)) msgs.push(`${w}: a var name starts with a lower-case letter and holds letters, digits and _`);
        else if (reserved(name)) msgs.push(`${w}: "${name}" is a reserved word or function name`);
        if (!spec || typeof spec !== 'object' || Array.isArray(spec)) { msgs.push(`${w}: must be an object with int or pick`); return; }
        const kinds = ['int', 'pick'].filter((k) => spec[k] !== undefined);
        Object.keys(spec).forEach((k) => { if (!['int', 'pick', 'not', 'step'].includes(k)) msgs.push(`${w}: unknown field "${k}" (int, pick, not, step)`); });
        if (kinds.length !== 1) { msgs.push(`${w}: give exactly one of int and pick`); return; }
        if (spec.int !== undefined && !intRange(spec.int)) msgs.push(`${w}.int: [low, high] whole numbers with low at most high`);
        if (spec.pick !== undefined && !(Array.isArray(spec.pick) && spec.pick.length && spec.pick.every((x) => typeof x === 'string' || (typeof x === 'number' && Number.isFinite(x))))) msgs.push(`${w}.pick: a non-empty list of numbers or text`);
        if (spec.not !== undefined && !Array.isArray(spec.not)) msgs.push(`${w}.not: a list of excluded values`);
        if (spec.step !== undefined && !(Number.isInteger(spec.step) && spec.step > 0 && spec.int !== undefined)) msgs.push(`${w}.step: a whole number above 0, with int`);
        if (!msgs.some((m) => m.startsWith(w))) { if (!varValues(spec).length) msgs.push(`${w}: every value is excluded`); }
        known.add(name);
      });
    }
    if (f.let !== undefined) {
      if (!f.let || typeof f.let !== 'object' || Array.isArray(f.let)) msgs.push('let must be an object of expressions');
      else Object.entries(f.let).forEach(([name, src]) => {
        const w = `let.${name}`;
        if (!VAR_NAME.test(name)) msgs.push(`${w}: a let name starts with a lower-case letter and holds letters, digits and _`);
        else if (reserved(name)) msgs.push(`${w}: "${name}" is a reserved word or function name`);
        else if (known.has(name)) msgs.push(`${w}: "${name}" is already a var or an earlier let`);
        if (typeof src !== 'string') { msgs.push(`${w}: must be an expression in text`); return; }
        try { const r = refs(src); r.ids.forEach((id) => { if (!known.has(id)) msgs.push(`${w}: "${id}" is not a var or an earlier let`); }); r.fns.forEach((fn) => { if (!FUNCS[fn]) msgs.push(`${w}: unknown function "${fn}"`); }); } catch (e) { msgs.push(`${w}: ${e.message}`); }
        known.add(name);
      });
    }
    if (f.where !== undefined) {
      if (!Array.isArray(f.where)) msgs.push('where must be a list of conditions');
      else f.where.forEach((src, i) => {
        if (typeof src !== 'string') { msgs.push(`where[${i}]: must be a condition in text`); return; }
        try { const r = refs(src); r.ids.forEach((id) => { if (!known.has(id)) msgs.push(`where[${i}]: "${id}" is not a var or a let`); }); r.fns.forEach((fn) => { if (!FUNCS[fn]) msgs.push(`where[${i}]: unknown function "${fn}"`); }); } catch (e) { msgs.push(`where[${i}]: ${e.message}`); }
      });
    }
    tplMsgs(msgs, 'prompt', f.prompt, known);
    const w = f.widget;
    if (!w || typeof w !== 'object' || Array.isArray(w)) msgs.push('widget must be an object');
    else {
      if (!WIDGET_FIELDS[w.kind]) msgs.push(`widget.kind is "numeric" or "expression" (found ${JSON.stringify(w.kind)})`);
      else {
        Object.keys(w).forEach((k) => { if (!WIDGET_FIELDS[w.kind].includes(k)) msgs.push(`widget.${k}: not a field of a ${w.kind} widget here (${WIDGET_FIELDS[w.kind].join(', ')})`); });
        if (w.answer === undefined) msgs.push('widget.answer is required');
        if (w.form !== undefined && (w.kind !== 'expression' || !FORMS.includes(w.form))) msgs.push(`widget.form is one of ${FORMS.join(', ')} (expression only)`);
        if (w.upToConstant !== undefined && (w.kind !== 'expression' || typeof w.upToConstant !== 'boolean')) msgs.push('widget.upToConstant is true or false (expression only)');
        if (w.accept !== undefined && (w.kind === 'expression' ? !(Array.isArray(w.accept) && w.accept.every((x) => typeof x === 'string')) : typeof w.accept !== 'string')) msgs.push(w.kind === 'expression' ? 'widget.accept is a list of accepted forms (text)' : 'widget.accept is one line of text');
        if (w.integers !== undefined && !(Array.isArray(w.integers) && w.integers.every((x) => typeof x === 'string'))) msgs.push('widget.integers is a list of letters');
        const walk = (v, at) => {
          if (typeof v === 'string') { if (at !== 'widget.kind' && at !== 'widget.form' && at !== 'widget.keyboard') tplMsgs(msgs, at, v, known); }
          else if (Array.isArray(v)) v.forEach((x, i) => walk(x, `${at}[${i}]`));
          else if (v && typeof v === 'object') Object.entries(v).forEach(([k, x]) => walk(x, `${at}.${k}`));
        };
        Object.entries(w).forEach(([k, v]) => walk(v, `widget.${k}`));
      }
    }
    if (f.wrong !== undefined) {
      if (!Array.isArray(f.wrong)) msgs.push('wrong must be a list');
      else {
        const ids = new Set();
        f.wrong.forEach((x, i) => {
          const at = `wrong[${i}]`;
          if (!x || typeof x !== 'object') { msgs.push(`${at}: must be an object`); return; }
          if (typeof x.id !== 'string' || !KEBAB.test(x.id)) msgs.push(`${at}.id: kebab-case text`);
          else if (ids.has(x.id)) msgs.push(`${at}.id: "${x.id}" is used twice`); else ids.add(x.id);
          const key = w && w.kind === 'numeric' ? 'value' : 'tex';
          if (x[key] === undefined) msgs.push(`${at}.${key} is required for a ${w && w.kind} widget`);
          Object.keys(x).forEach((k) => { if (!['id', 'line', 'tex', 'value', 'tol'].includes(k)) msgs.push(`${at}.${k}: unknown field (id, tex or value, tol, line)`); });
          if (w && w.kind === 'numeric' && x.tex !== undefined) msgs.push(`${at}.tex: a numeric widget's wrong values use "value"`);
          if (w && w.kind === 'expression' && (x.value !== undefined || x.tol !== undefined)) msgs.push(`${at}: an expression widget's wrong values use "tex"`);
          ['tex', 'value', 'line'].forEach((k) => { if (typeof x[k] === 'string') tplMsgs(msgs, `${at}.${k}`, x[k], known); });
          if (x.tol && typeof x.tol === 'object') Object.entries(x.tol).forEach(([k, v]) => { if (typeof v === 'string') tplMsgs(msgs, `${at}.tol.${k}`, v, known); });
          if (x.line !== undefined && typeof x.line !== 'string') msgs.push(`${at}.line: must be text`);
        });
      }
    }
    if (f.solution === undefined || !Array.isArray(f.solution) || !f.solution.length) msgs.push('solution must be a non-empty list of steps');
    else f.solution.forEach((s, i) => tplMsgs(msgs, `solution[${i}]`, s, known));
    Object.keys(f).forEach((k) => { if (!['id', 'weight', 'skill', 'vars', 'let', 'where', 'prompt', 'widget', 'wrong', 'solution'].includes(k)) msgs.push(`unknown field "${k}"`); });
    return msgs;
  };

  /* ---------- Drawing ---------- */
  const NUMERIC_KEYS = new Set(['answer', 'abs', 'rel', 'value']);
  const asNumber = (text, at) => {
    const s = String(text).trim().replace(/\s+/g, '');
    let m;
    if ((m = /^(-?\d+(?:\.\d+)?)\/(-?\d+(?:\.\d+)?)$/.exec(s)) && Number(m[2]) !== 0) return Number(m[1]) / Number(m[2]);
    if (/^-?(\d+\.?\d*|\.\d+)$/.test(s)) return Number(s);
    return bad(`${at}: "${text}" is not a number`);
  };
  /* the widget spec of one draw: every text field is a template; for a numeric widget answer, tol and the wrong values become numbers */
  const resolveWidget = (f, env) => {
    const w = f.widget, numeric = w.kind === 'numeric', out = {};
    Object.entries(w).forEach(([k, v]) => {
      if (k === 'tolerance') k = 'tol';
      const walk = (x, key, at) => {
        if (typeof x === 'string') {
          if (['kind', 'form', 'keyboard'].includes(at)) return x;
          if (numeric && NUMERIC_KEYS.has(key)) return asNumber(render(x, env, 'num'), `widget.${at}`);
          return render(x, env, numeric ? 'num' : 'tex');
        }
        if (Array.isArray(x)) return x.map((y, i) => walk(y, key, `${at}[${i}]`));
        if (x && typeof x === 'object') return Object.fromEntries(Object.entries(x).map(([kk, y]) => [kk, walk(y, kk, `${at}.${kk}`)]));
        return x;
      };
      out[k] = walk(v, k, k);
    });
    return out;
  };
  const showVar = (v) => (typeof v === 'string' ? v : plain(v, 'num'));
  const MAX_TRIES = 60;
  /* One item. opts.avoid: a Set of prompts already used. Returns the item, or { rejected, error } when no draw was accepted. */
  const draw = (f, r, opts = {}) => {
    const avoid = opts.avoid || null, stats = opts.stats || { attempts: 0, rejected: 0, dup: 0, errors: new Map() };
    const note = (e) => { const m = String(e && e.message || e); stats.errors.set(m, (stats.errors.get(m) || 0) + 1); };
    for (let tries = 0; tries < (opts.maxTries || MAX_TRIES); tries++) {
      stats.attempts++;
      const env = {};
      try {
        Object.entries(f.vars || {}).forEach(([name, spec]) => {
          const vals = varValues(spec);
          const pick = vals[Math.floor(r() * vals.length)];
          env[name] = fromJS(pick);
        });
        Object.entries(f.let || {}).forEach(([name, src]) => { env[name] = evaluate(src, env); });
        let ok = true;
        for (const c of f.where || []) { const v = evaluate(c, env); if (typeof v !== 'boolean') bad(`where "${c}" is not a condition (true or false)`); if (!v) { ok = false; break; } }
        if (!ok) { stats.rejected++; continue; }
        const prompt = render(f.prompt, env);
        if (avoid && avoid.has(prompt)) { stats.rejected++; stats.dup++; continue; }
        const widget = resolveWidget(f, env);
        const wrong = (f.wrong || []).map((x) => {
          const o = { id: x.id };
          if (x.tex !== undefined) o.tex = render(x.tex, env);
          if (x.value !== undefined) o.value = typeof x.value === 'number' ? x.value : asNumber(render(x.value, env, 'num'), `wrong ${x.id} value`);
          if (x.tol !== undefined) o.tol = typeof x.tol === 'object' ? Object.fromEntries(Object.entries(x.tol).map(([k, v]) => [k, typeof v === 'string' ? asNumber(render(v, env, 'num'), `wrong ${x.id} tol`) : v])) : x.tol;
          o.line = x.line !== undefined ? render(x.line, env) : '';
          return o;
        });
        const solution = (f.solution || []).map((s) => render(s, env));
        const vars = {}, lets = {};
        Object.keys(f.vars || {}).forEach((k) => { vars[k] = showVar(env[k]); });
        Object.keys(f.let || {}).forEach((k) => { lets[k] = showVar(env[k]); });
        return { family: f.id, skill: f.skill || '', vars, lets, prompt, widget, wrong, solution, stats };
      } catch (e) { stats.rejected++; note(e); }
    }
    return { rejected: true, stats, error: [...stats.errors.keys()].pop() || 'no draw passed where' };
  };
  /* smooth weighted round robin: families in turn, a weight-2 family twice as often */
  const schedule = (families, n) => {
    const w = families.map((f) => (typeof f.weight === 'number' && f.weight > 0 ? f.weight : 1)), total = w.reduce((a, b) => a + b, 0), cur = w.map(() => 0), out = [];
    for (let k = 0; k < n; k++) {
      cur.forEach((_, i) => { cur[i] += w[i]; });
      let best = 0; cur.forEach((c, i) => { if (c > cur[best]) best = i; });
      cur[best] -= total; out.push(best);
    }
    return out;
  };
  /* The items of one attempt (a set of n, no two with the same prompt). The same seed gives the same items. */
  const generate = (set, seed, o = {}) => {
    const n = o.n || set.n || 20, fams = (set.families || []).filter((f) => f && !checkFamily(f).length);
    if (!fams.length) return [];
    const order = schedule(fams, n), used = new Set(), items = [];
    for (let k = 0; k < n; k++) {
      const first = order[k];
      for (let j = 0; j < fams.length; j++) {
        const f = fams[(first + j) % fams.length];
        const it = draw(f, rng(`${seed}|${set.id}|${k}|${j}`), { avoid: used });
        if (!it.rejected) { used.add(it.prompt); items.push(it); break; }
      }
    }
    return items;
  };
  /* what the validator and the sampling tool read: n draws of one family on seeds 1..seeds */
  const sample = (f, { seeds = 200, set = 'sample', from = 1 } = {}) => {
    const stats = { attempts: 0, rejected: 0, dup: 0, errors: new Map() }, items = [], prompts = new Set();
    let failed = 0;
    for (let s = from; s < from + seeds; s++) {
      const it = draw(f, rng(`${s}|${set}|${f.id}`), { stats });
      if (it.rejected) { failed++; continue; }
      items.push({ seed: s, ...it, stats: undefined });
      prompts.add(it.prompt);
    }
    return { items, distinct: prompts.size, attempts: stats.attempts, rejected: stats.rejected, failed, errors: [...stats.errors.entries()].sort((a, b) => b[1] - a[1]) };
  };
  const passMark = (set, n) => Math.ceil((typeof set.pass === 'number' ? set.pass : 0.9) * n - 1e-9);

  /* ---------- An item for ZQ.player.runSet ---------- */
  const playerItem = (it, set, k) => {
    const steps = it.solution.join(' ');
    const byKey = {};
    it.wrong.forEach((x) => { if (x.line) byKey[x.id] = `${x.line} ${steps}`; });
    const w = JSON.parse(JSON.stringify(it.widget));
    if (it.wrong.length) w.wrong = it.wrong.map((x) => { const o = { id: x.id }; if (x.tex !== undefined) o.tex = x.tex; if (x.value !== undefined) o.value = x.value; if (x.tol !== undefined) o.tol = x.tol; return o; });
    return {
      id: `${set.id}-${k + 1}`, generated: true, fluency: { set: set.id, family: it.family }, difficulty: 2, skills: [],
      title: (it.skill || 'Fluency').replace(/^./, (c) => c.toUpperCase()), source: `Fluency · ${it.skill || set.title || set.id}`,
      question: it.prompt, widget: w,
      feedback: { correct: '', generic: steps, byKey },
      explain: { text: it.solution.join('\n\n') },
    };
  };

  const api = { GenError, parse, evaluate, refs, template, render, templateRefs, format, polyText, checkFamily, draw, schedule, generate, sample, passMark, playerItem, rng, FUNC_NAMES, MAX_TRIES, fromJS, plain };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (root) { root.ZQ = root.ZQ || {}; root.ZQ.gen = api; }
})(typeof window !== 'undefined' ? window : null);
