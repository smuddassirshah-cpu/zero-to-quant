/* Arithmetic generator shared by the Today warm-up and generated exam items (ENGINE-BACKLOG 452; AUTHORING.md section 5).
   The operations come from content/warmup.json (Zetamac defaults): addition, subtraction as addition reversed,
   multiplication and division as multiplication reversed.
     ZQ.arith.ready                      resolves once content/warmup.json is read (a built-in copy stands in if it is not)
     ZQ.arith.config()                   the operations, as the warm-up sees them
     ZQ.arith.problem(ops, rng, prev)    one problem { id, tex, ans, a, b, ... } (rng defaults to Math.random; the same
                                         problem never follows itself)
     ZQ.arith.rng(seed)                  a seeded generator (mulberry32)
     ZQ.arith.options(p, k, rng)         the right answer and k - 1 near-miss distractors, as strings in no order
     ZQ.arith.expand(items, seed)        a paper's items with every { generator: "arith", ... } entry replaced by n
                                         single-choice items; the same seed gives the same items
   Near misses: the reverse operation (what a hurried solver does instead), a misplaced decimal point (times or over
   ten) and a slipped digit (one digit of the answer off by one). */
(function () {
  'use strict';
  const Z = window.ZQ = window.ZQ || {};

  const DEFAULT = {
    operations: [
      { id: 'add', symbol: '+', tex: '+', a: [2, 100], b: [2, 100] },
      { id: 'sub', symbol: '-', tex: '-', inverseOf: 'add' },
      { id: 'mul', symbol: '×', tex: '\\times', a: [2, 12], b: [2, 100] },
      { id: 'div', symbol: '÷', tex: '\\div', inverseOf: 'mul' },
    ],
  };
  const CONF = { operations: DEFAULT.operations.map(o => ({ ...o })) };
  const ready = fetch('content/warmup.json', { cache: 'no-cache' })
    .then(r => (r.ok ? r.json() : null))
    .then(j => { if (j && Array.isArray(j.operations) && j.operations.length) CONF.operations = j.operations; })
    .catch(() => { /* keep the built-in operations */ });

  const APPLY = { add: (a, b) => a + b, mul: (a, b) => a * b };
  const rngFrom = (seed) => { let a = (Number(seed) || 0) >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
  const hash = (s) => { let h = 2166136261; for (const c of String(s)) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; };
  const pick = (rng, a, b) => a + Math.floor(rng() * (b - a + 1));
  const clean = (n) => Number(Number(n).toPrecision(12));

  /* One problem. ops: the operation list (an optional weight per operation as { op: weight }). */
  const problem = (ops, rng = Math.random, prev = null, weights = null) => {
    const usable = (ops || CONF.operations).filter(o => APPLY[o.inverseOf || o.id]);
    const bag = [];
    usable.forEach(o => { const w = weights ? (weights[o.id] != null ? +weights[o.id] : 0) : 1; for (let i = 0; i < Math.round(w * 100); i++) bag.push(o); });
    const from = bag.length ? bag : usable;
    for (let guard = 0; guard < 200; guard++) {
      const op = from[Math.floor(rng() * from.length)];
      const base = op.inverseOf ? usable.find(o => o.id === op.inverseOf) : op;
      const a = pick(rng, base.a[0], base.a[1]), b = pick(rng, base.b[0], base.b[1]), f = APPLY[base.id];
      const p = op.inverseOf ? { id: op.id, tex: `${f(a, b)} ${op.tex} ${a}`, plain: `${f(a, b)} ${op.symbol || op.tex} ${a}`, ans: b, a, b, whole: f(a, b), base: base.id } : { id: op.id, tex: `${a} ${op.tex} ${b}`, plain: `${a} ${op.symbol || op.tex} ${b}`, ans: f(a, b), a, b, base: op.id };
      if (!prev || p.tex !== prev.tex) return p;
    }
    return problem(ops, rng, null, weights);
  };

  /* ---------- Near-miss distractors ---------- */
  const reverse = (p) => {
    if (p.id === 'add') return Math.abs(p.a - p.b);
    if (p.id === 'sub') return p.whole + p.a;
    if (p.id === 'mul') return p.a + p.b;
    if (p.id === 'div') return p.whole - p.a;
    return null;
  };
  const point = (p, rng) => (rng() < 0.5 || p.ans < 10 ? p.ans * 10 : clean(p.ans / 10));
  const slip = (ans, rng) => {
    if (!Number.isInteger(ans) || ans < 10) return ans + (rng() < 0.5 ? 1 : -1) * pick(rng, 1, 2);
    const s = String(ans), i = pick(rng, 0, s.length - 1);
    let d = (+s[i] + (rng() < 0.5 ? 1 : -1) + 10) % 10;
    if (i === 0 && d === 0) d = 2;
    return Number(s.slice(0, i) + d + s.slice(i + 1));
  };
  const options = (p, k, rng = Math.random) => {
    const ans = p.ans, seen = new Set([ans]), out = [];
    const add = (v) => { if (v == null || !Number.isFinite(v) || v < 0 || seen.has(clean(v))) return false; seen.add(clean(v)); out.push(clean(v)); return true; };
    const kinds = [() => add(reverse(p)), () => add(point(p, rng)), () => add(slip(ans, rng)), () => add(slip(ans, rng))];
    const order = kinds.slice();
    if (k - 1 < kinds.length) for (let i = order.length - 1; i > 0; i--) { const j = Math.floor(rng() * (i + 1)); [order[i], order[j]] = [order[j], order[i]]; }
    order.forEach(f => { if (out.length < k - 1) f(); });
    for (let g = 0; out.length < k - 1 && g < 60; g++) add(g < 20 ? slip(ans, rng) : ans + pick(rng, -12, 12));
    for (let v = 1; out.length < k - 1; v++) add(ans + v);
    const all = out.slice(0, k - 1).concat(ans);
    for (let i = all.length - 1; i > 0; i--) { const j = Math.floor(rng() * (i + 1)); [all[i], all[j]] = [all[j], all[i]]; }
    return all.map(v => String(v));
  };

  /* ---------- Generated exam items ---------- */
  const LETTERS = 'abcdefgh';
  const ONE = (spec, rng, prev, idx, pi) => {
    const p = problem(CONF.operations, rng, prev, spec.mix && typeof spec.mix === 'object' ? weightsOf(spec.mix) : null);
    const k = Math.min(6, Math.max(2, Math.round(+spec.options || 4)));
    const opts = options(p, k, rng);
    const right = String(p.ans);
    return {
      p,
      item: {
        id: `gen-${pi}-${idx + 1}`, generated: true, difficulty: spec.difficulty || 3, skills: Array.isArray(spec.skills) ? spec.skills.slice() : [],
        title: p.plain, question: `$${p.tex}$`,
        widget: { kind: 'choice', layout: 'grid', label: 'Answer options', options: opts.map((t, i) => ({ id: LETTERS[i], text: `$${t}$`, correct: t === right })) },
        feedback: { correct: '', generic: `$${p.tex} = ${right}$.` },
        explain: { text: `$${p.tex} = ${right}$.` },
      },
    };
  };
  /* A mix value is a weight, or { weight } */
  const weightsOf = (mix) => { const w = {}; Object.keys(mix).forEach(id => { const v = mix[id]; w[id] = typeof v === 'number' ? v : v && typeof v === 'object' && v.weight != null ? +v.weight : 1; }); return w; };
  /* A mix entry may also narrow one operation's ranges: { weight, a: [lo, hi], b: [lo, hi] } */
  const opsFor = (mix) => CONF.operations.map(o => {
    const v = mix && mix[o.id];
    if (!v || typeof v !== 'object' || (!v.a && !v.b)) return o;
    return { ...o, ...(v.a ? { a: v.a } : {}), ...(v.b ? { b: v.b } : {}) };
  });

  /* Replace each generator entry with n items. seed: any number or string; each generator entry has its own stream
     (seed and its position), so changing one entry does not move the others. */
  const expand = (items, seed = 0, pi = 0) => {
    const out = [];
    (items || []).forEach((it, at) => {
      if (!it || it.generator == null) { out.push(it); return; }
      if (it.generator !== 'arith') return;
      const rng = rngFrom(hash(`${seed}/${pi}/${at}`));
      const saved = CONF.operations;
      CONF.operations = opsFor(it.mix);
      try {
        let prev = null;
        for (let i = 0; i < Math.max(1, Math.round(+it.n || 1)); i++) { const o = ONE(it, rng, prev, out.length, `${pi + 1}`); prev = o.p; out.push(o.item); }
      } finally { CONF.operations = saved; }
    });
    return out;
  };

  Z.arith = { ready, config: () => CONF, problem, options, expand, rng: rngFrom, seedOf: hash, ops: () => CONF.operations.map(o => o.id) };
})();
