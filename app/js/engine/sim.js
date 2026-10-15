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

   Outcome strings may use numbers, + - * / % ** ^, comparisons, && || !, ?: and these names:
   d6() a fair die, d(n) a fair n-sided die, coin() 1 for heads and 0 for tails, u() or u(a, b) uniform,
   n() or n(mu, sd) normal, binomial(n, p), pick([..]), max, min, abs, floor, ceil, round, sqrt, exp, log, pow. */
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

  /* Outcome expressions: a whitelist of names, no strings, no assignment, no member access. */
  const NAMES = ['d6', 'd', 'coin', 'u', 'n', 'binomial', 'pick', 'shuffle', 'max', 'min', 'abs', 'floor', 'ceil', 'round', 'sqrt', 'exp', 'log', 'pow'];
  const MATH = { max: Math.max, min: Math.min, abs: Math.abs, floor: Math.floor, ceil: Math.ceil, round: Math.round, sqrt: Math.sqrt, exp: Math.exp, log: Math.log, pow: Math.pow };
  const cache = new Map();
  const compile = (expr) => {
    const key = String(expr);
    if (cache.has(key)) return cache.get(key);
    const src = key.replace(/\^/g, '**');
    if (/["'`;{}\\]|=>|(^|[^=!<>])=($|[^=])|\.\s*[A-Za-z_$]/.test(src)) throw new Error('Outcome expression not allowed: ' + key);
    for (const id of src.match(/[A-Za-z_$][\w$]*/g) || []) if (!NAMES.includes(id) && id !== 'true' && id !== 'false') throw new Error(`Unknown name "${id}" in outcome: ${key}`);
    // eslint-disable-next-line no-new-func
    const f = new Function(...NAMES, '"use strict"; return (' + src + ');');
    const run = (r) => {
      const h = bind(r);
      const v = f(h.d6, h.d, h.coin, h.u, h.n, h.binomial, h.pick, h.shuffle, ...['max', 'min', 'abs', 'floor', 'ceil', 'round', 'sqrt', 'exp', 'log', 'pow'].map(k => MATH[k]));
      return typeof v === 'boolean' ? (v ? 1 : 0) : v;
    };
    cache.set(key, run);
    return run;
  };
  const outcome = (expr, r) => compile(expr)(R(r));
  const run = (expr, trials, seed = 1) => {
    const r = typeof seed === 'function' ? seed : rng(seed), f = compile(expr), out = new Array(trials);
    for (let i = 0; i < trials; i++) out[i] = f(r);
    return out;
  };
  const tally = (values) => { const t = {}; for (const v of values) { const k = Array.isArray(v) ? v.join(',') : String(v); t[k] = (t[k] || 0) + 1; } return t; };

  Z.sim = { rng, d, d6, coin, uniform, normal, binomial, pick, shuffle, bind, compile, outcome, run, tally };
})();
