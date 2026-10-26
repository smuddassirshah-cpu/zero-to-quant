/* Simulation helpers (docs/PLAN.md section 9): a seeded RNG so every lesson replays identically, the usual
   random draws, and a tiny runner for the authored outcome strings in `sim` blocks ("d6()+d6()").
   Loaded after core.js.

   ZQ.sim.rng(seed)              -> function returning a float in [0, 1); seed is a number or a string
   ZQ.sim.d6(rng), d(n, rng), coin(rng), uniform(a, b, rng), normal(mu, sd, rng), binomial(n, p, rng),
   pick(arr, rng), shuffle(arr, rng)   every helper takes the rng last and defaults to Math.random
   ZQ.sim.bind(rng)              -> the same helpers bound to one rng: { d6(), d(n), coin(), u(a, b), n(mu, sd), ... }
   ZQ.sim.compile(expr)          -> (rng) => value; throws on an expression outside the safe subset
   ZQ.sim.outcome(expr, rng)     -> one evaluated outcome; booleans become 1 or 0
   ZQ.sim.run(expr, trials, seedOrRng) -> array of outcomes
   ZQ.sim.tally(values)          -> { value: count }
   ZQ.sim.trial(simSpec, vars)   -> (rng) => { value, keep }: let bindings, outcome (a value or [X, Y]) and filter
   ZQ.sim.running(values, stat)  -> the running mean (or varp, var, sd, sum) after each outcome

   Outcome strings may use numbers, + - * / % ** ^, comparisons, && || !, ?: and these names:
   d6() a fair die, d(n) a fair n-sided die, coin() 1 for heads and 0 for tails, u() or u(a, b) uniform,
   n() or n(mu, sd) normal, binomial(n, p), pick([..]), max, min, abs, floor, ceil, round, sqrt, exp, log, pow,
   sample(k, e), mean, var, varp, sd, sum (of a list, or of k fresh draws of e), len, tstat(k), and the names given.
   Item 342: maxn(k, e) and minn(k, e) (the largest or smallest of k fresh draws), count(k, e) (how many of k draws are
   true or non-zero), repeat(k, e) (an alias of sample), and each of them on a list too. */
(function () {
  'use strict';
  const Z = window.ZQ || (window.ZQ = {});

  /* mulberry32, the generator the prototype used, so seeds carry over */
  const hash = (s) => { let h = 2166136261 >>> 0; for (const ch of String(s)) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619) >>> 0; } return h; };
  const rng = (seed = 1) => {
    let a = (typeof seed === 'number' && Number.isFinite(seed) ? Math.floor(seed) : hash(seed)) >>> 0;
    return () => {
      a = (a + 0x6D2B79F5) >>> 0; let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  };
  const R = (r) => (typeof r === 'function' ? r : Math.random);

  const d = (n, r) => 1 + Math.floor(R(r)() * n);
  const d6 = (r) => d(6, r);
  const coin = (r) => (R(r)() < 0.5 ? 1 : 0);
  const uniform = (a = 0, b = 1, r) => a + (b - a) * R(r)();
  /* Box-Muller; the spare value is dropped so a seed always gives the same sequence whatever came before */
  const normal = (mu = 0, sd = 1, r) => {
    const f = R(r); let u = 0, v = 0;
    while (u === 0) u = f(); v = f();
    return mu + sd * Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };
  const binomial = (n, p, r) => { const f = R(r); let k = 0; for (let i = 0; i < n; i++) if (f() < p) k++; return k; };
  const pick = (arr, r) => arr[Math.floor(R(r)() * arr.length)];
  const shuffle = (arr, r) => { const f = R(r), a = arr.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(f() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  const bind = (r) => {
    const f = R(r);
    return {
      rng: f,
      d6: () => d(6, f), d: (n = 6) => d(n, f), coin: () => coin(f),
      u: (a = 0, b = 1) => uniform(a, b, f), n: (mu = 0, sd = 1) => normal(mu, sd, f),
      binomial: (n, p) => binomial(n, p, f), pick: (arr) => pick(arr, f), shuffle: (arr) => shuffle(arr, f),
    };
  };

  /* Outcome expressions: a whitelist of names, no strings, no assignment, no member access.
     Items 321, 326, 327: sample statistics. sample(k, e) draws e k times (a list); mean, var (divide by k - 1), varp
     (divide by k), sd, sum and len take a list, or (k, e) to draw a fresh sample: mean(10, n()) is the mean of ten
     normal draws. tstat(k) (or tstat(k, mu, sd)) is one t statistic of k normal draws. Lists index with xs[0].
     Extra names (a canvas's params, a sim's let bindings) may be read when compile is given them. */
  const NAMES = ['d6', 'd', 'coin', 'u', 'n', 'binomial', 'pick', 'shuffle', 'max', 'min', 'abs', 'floor', 'ceil', 'round', 'sqrt', 'exp', 'log', 'pow', 'sample', 'mean', 'var', 'varp', 'sd', 'sum', 'len', 'tstat', 'maxn', 'minn', 'count', 'repeat'];
  const MATH = { max: Math.max, min: Math.min, abs: Math.abs, floor: Math.floor, ceil: Math.ceil, round: Math.round, sqrt: Math.sqrt, exp: Math.exp, log: Math.log, pow: Math.pow };
  const LAZY = ['sample', 'mean', 'var', 'varp', 'sd', 'sum', 'maxn', 'minn', 'count', 'repeat'];
  /* fn(k, e) for a lazy helper becomes fn(k, () => (e)) so e is drawn afresh each time (after the guard has run) */
  const lazify = (src) => {
    let out = '', i = 0;
    const re = new RegExp('\\b(' + LAZY.join('|') + ')\\s*\\(', 'g');
    let m;
    while ((m = re.exec(src))) {
      if (m.index < i) continue;
      let depth = 1, j = m.index + m[0].length, cut = -1;
      for (; j < src.length && depth; j++) { const c = src[j]; if (c === '(' || c === '[') depth++; else if (c === ')' || c === ']') depth--; else if (c === ',' && depth === 1 && cut < 0) cut = j; }
      const inner = src.slice(m.index + m[0].length, j - 1);
      out += src.slice(i, m.index) + m[1] + '(' + (cut < 0 ? lazify(inner) : lazify(src.slice(m.index + m[0].length, cut)) + ', () => (' + lazify(src.slice(cut + 1, j - 1)) + ')') + ')';
      i = j; re.lastIndex = j;
    }
    return out + src.slice(i);
  };
  const listOf = (a, f) => (typeof f === 'function' ? Array.from({ length: Math.max(0, Math.round(a)) }, () => f()) : Array.isArray(a) ? a : [a]);
  const STATS = {
    sample: (k, f) => listOf(k, f),
    sum: (a, f) => listOf(a, f).reduce((t, x) => t + +x, 0),
    len: (a) => (Array.isArray(a) ? a.length : 1),
    mean: (a, f) => { const xs = listOf(a, f); return xs.length ? xs.reduce((t, x) => t + +x, 0) / xs.length : NaN; },
    varp: (a, f) => { const xs = listOf(a, f), m = xs.reduce((t, x) => t + +x, 0) / xs.length; return xs.reduce((t, x) => t + (x - m) ** 2, 0) / xs.length; },
    var: (a, f) => { const xs = listOf(a, f), m = xs.reduce((t, x) => t + +x, 0) / xs.length; return xs.length > 1 ? xs.reduce((t, x) => t + (x - m) ** 2, 0) / (xs.length - 1) : NaN; },
  };
  STATS.sd = (a, f) => Math.sqrt(STATS.var(a, f));
  STATS.maxn = (a, f) => Math.max(...listOf(a, f).map(Number));
  STATS.minn = (a, f) => Math.min(...listOf(a, f).map(Number));
  STATS.count = (a, f) => listOf(a, f).filter((x) => !!x && +x !== 0).length;
  STATS.repeat = STATS.sample;
  const cache = new Map();
  const compile = (expr, extra = []) => {
    const names = [...new Set((extra || []).filter((x) => /^[A-Za-z_$][\w$]*$/.test(x) && !NAMES.includes(x)))];
    const key = String(expr) + '|' + names.join(',');
    if (cache.has(key)) return cache.get(key);
    const src0 = String(expr).replace(/\^/g, '**');
    if (/["'`;{}\\]|=>|(^|[^=!<>])=($|[^=])|\.\s*[A-Za-z_$]/.test(src0)) throw new Error('Outcome expression not allowed: ' + expr);
    for (const id of src0.match(/[A-Za-z_$][\w$]*/g) || []) if (!NAMES.includes(id) && !names.includes(id) && id !== 'true' && id !== 'false') throw new Error(`Unknown name "${id}" in outcome: ${expr}`);
    const src = lazify(src0).replace(/\bvar(?=\s*\()/g, 'variance'); // var is a reserved word in JavaScript
    // eslint-disable-next-line no-new-func
    const f = new Function(...NAMES.map((x) => (x === 'var' ? 'variance' : x)), ...names, '"use strict"; return (' + src + ');');
    const run = (r, vars = {}) => {
      const h = bind(r);
      const tstat = (k, mu = 0, s = 1) => { const xs = listOf(k, () => normal(mu, s, h.rng)); return (STATS.mean(xs) - mu) / (STATS.sd(xs) / Math.sqrt(xs.length)); };
      const v = f(h.d6, h.d, h.coin, h.u, h.n, h.binomial, h.pick, h.shuffle, ...['max', 'min', 'abs', 'floor', 'ceil', 'round', 'sqrt', 'exp', 'log', 'pow'].map(k => MATH[k]), STATS.sample, STATS.mean, STATS.var, STATS.varp, STATS.sd, STATS.sum, STATS.len, tstat, STATS.maxn, STATS.minn, STATS.count, STATS.repeat, ...names.map((k) => vars[k]));
      return typeof v === 'boolean' ? (v ? 1 : 0) : Array.isArray(v) ? v.map((x) => (typeof x === 'boolean' ? +x : x)) : v;
    };
    cache.set(key, run);
    return run;
  };
  const outcome = (expr, r, vars) => compile(expr, vars ? Object.keys(vars) : [])(R(r), vars || {});
  /* A whole trial from a sim block: let bindings ({ xs: "sample(10, n())" }, in order, each may read the earlier
     ones and the params), then outcome (a value, or a list such as [X, Y] for two values per trial), and filter
     (item 286: a trial whose filter is false is discarded and not counted). */
  const trial = (spec, vars = {}) => {
    const lets = Object.entries((spec && spec.let) || {}), base = Object.keys(vars), steps = [];
    lets.forEach(([k, e], i) => steps.push([k, compile(e, base.concat(lets.slice(0, i).map((x) => x[0])))]));
    const all = base.concat(lets.map((x) => x[0]));
    const out = compile(spec.outcome, all), flt = spec.filter != null ? compile(spec.filter, all) : null;
    return (r) => { const env = { ...vars }; for (const [k, f] of steps) env[k] = f(r, env); return { value: out(r, env), keep: flt ? !!flt(r, env) : true }; };
  };
  const run = (expr, trials, seed = 1) => {
    const r = typeof seed === 'function' ? seed : rng(seed), f = compile(expr), out = new Array(trials);
    for (let i = 0; i < trials; i++) out[i] = f(r);
    return out;
  };
  const tally = (values) => { const t = {}; for (const v of values) { const k = Array.isArray(v) ? v.join(',') : String(v); t[k] = (t[k] || 0) + 1; } return t; };

  /* item 327: a running statistic over a stream of outcomes: mean, varp (divide by n), var, sd, proportion (mean of 0/1) */
  const running = (xs, stat = 'mean') => {
    const out = []; let s = 0, s2 = 0;
    xs.forEach((x, i) => { const n = i + 1; s += +x; s2 += (+x) * (+x); const m = s / n, vp = Math.max(0, s2 / n - m * m); out.push(stat === 'varp' ? vp : stat === 'var' ? (n > 1 ? vp * n / (n - 1) : NaN) : stat === 'sd' ? (n > 1 ? Math.sqrt(vp * n / (n - 1)) : NaN) : stat === 'sum' ? s : m); });
    return out;
  };
  Z.sim = { rng, d, d6, coin, uniform, normal, binomial, pick, shuffle, bind, compile, outcome, run, tally, trial, running };
})();
