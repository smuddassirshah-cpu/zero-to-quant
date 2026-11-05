#!/usr/bin/env node
// PLAN 2c item 7 content transform. Reads the reviewed proposal and writes `why` into every cross-course
// `requires` edge of course.json. Idempotent: run twice, same result.
//   node app/tools/apply-item7-content.mjs [--dir <content dir>] [--proposal <json>] [--dry]
// Proposal rows: { from: "<course>/L<n>", ref, why, action: keep|diagnostic|cut|retarget, retarget? }.
// The main session's review (OVERRIDE below) wins over the proposal; reasons in docs/reports/closure-item7.md.
// Output form per edge: { "ref": "...", "why": "..." } and, for a diagnostic, "gate": false. Intra-course edges stay strings.
// A level that had no explicit requires implicitly needed its previous level; when an edge moves onto it, that
// previous level is written in explicitly so the chain is kept.
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const arg = (k) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const HERE = dirname(fileURLToPath(import.meta.url));
const DIR = arg('--dir') || join(HERE, '..', 'content');
const PROP = arg('--proposal') || join(HERE, '..', '..', 'docs', 'reports', 'closure-item7-proposal.json');
const DRY = process.argv.includes('--dry');

const K = (from, ref) => from + '|' + ref;
// Main-session review. a: action; to: new ref (retarget); move: new dependent level; w: replacement why;
// extra: further edges added to the same level.
const OVERRIDE = {
  // Every L1 keeps at least one gate (DECISIONS "Interview closures under Strict mode": solid foundation first).
  [K('algebra/L1', 'linear-maps/L2')]: { a: 'keep', w: 'Represents symmetries as matrices acting on vectors, so linear maps are used throughout.' },
  [K('arma/L1', 'regression/L3')]: { a: 'retarget', to: 'regression/L1', w: 'The Dickey-Fuller test is a regression on lagged values, read like a fitted line.' },
  [K('arma/L1', 'numpy-pandas/L3')]: { a: 'keep', w: 'Computes returns and differences with pandas shift, pct_change and rolling means.' },
  [K('coding-int/L1', 'algo-think/L3')]: { a: 'keep', w: 'Interval, two-pointer and binary-search patterns assume sorting and searching.' },
  [K('contests/L1', 'graphs-dp/L2')]: { a: 'keep', w: 'Choosing an algorithm from the limits assumes BFS, Dijkstra and union-find are known.' },
  [K('counting/L1', 'equations/L1')]: { a: 'keep', w: 'Writes factorial counts as algebraic expressions and simplifies them.' },
  [K('cpp-pricing/L1', 'cpp/L2')]: { a: 'retarget', to: 'cpp/L1', w: 'Writes C++ programs with doubles, cmath and random number generators.',
    extra: [{ ref: 'cpp/L2', why: 'A few lessons pass by reference and use pointers; refresh references and memory first.', gate: false }] },
  [K('micro/L1', 'markets/L2')]: { a: 'keep', w: 'The order book trades shares at quoted prices, introduced in bonds and shares.' },
  [K('numpy-pandas/L1', 'py-found/L2')]: { a: 'keep', w: 'Array work calls and writes Python functions and relies on mutation rules.' },
  [K('pairs-rep/L1', 'coint/L3')]: { a: 'keep', w: 'Replicates a pairs-trading paper, so the pairs-trading level is the method replicated.' },
  [K('py-found/L1', 'first-python/L3')]: { a: 'keep', w: 'Core types work defines small functions, first written in functions and files.' },
  [K('regression/L1', 'estimation/L1')]: { a: 'keep', w: 'Reads fitted slopes as statistics estimating parameters, and asks whether they are unbiased.' },
  [K('sql/L1', 'equations/L3')]: { a: 'keep', w: 'WHERE clauses filter rows with comparison operators and inequalities.' },
  [K('systems/L1', 'cpp-pricing/L3')]: { a: 'retarget', to: 'cpp/L2', w: 'Cache and layout questions rely on references and contiguous memory in C++.',
    extra: [{ ref: 'cpp-pricing/L3', why: 'The contiguous-memory timing demo in C++ pricing previews the cache questions.', gate: false }] },
  // Rejected retarget: L3 would widen a trader gate on one named idea.
  [K('brainteasers/L1', 'counting-chance/L2')]: { a: 'keep', w: 'Forces coincidences by counting boxes and objects with the counting tools.' },
  // Rejected retargets: a lesson reference is the narrower gate, so it stays.
  [K('measure-prob/L3', 'random-vars/l17-variance-given-information')]: { a: 'keep', w: 'Uses the law of total variance, conditioning on information.' },
  [K('measure-prob/L3', 'least-squares/l5-dropping-a-perpendicular')]: { a: 'keep', w: 'Uses projection onto a line and its perpendicular error as conditional expectation.' },
  [K('measure-prob/L4', 'estimation/l5-which-fits')]: { a: 'keep', w: 'Uses the likelihood ratio to reweight probabilities.' },
  // Edges on the wrong dependent level move to the level that uses them.
  [K('alpha/L1', 'fin-ml/L3')]: { a: 'keep', move: 'alpha/L3', w: 'Sizes positions with costs and deflated Sharpe from finance ML level 3.' },
  [K('backtest/L1', 'fin-ml/L3')]: { a: 'keep', move: 'backtest/L2', w: 'Uses the turnover and cost conventions of finance ML level 3.' },
  [K('integrals/L1', 'limits/L2')]: { a: 'keep', move: 'integrals/L2', w: 'Links areas to antiderivatives, so derivatives are used throughout.' },
  [K('pdes/L1', 'ito/L3')]: { a: 'keep', move: 'pdes/L3', w: 'Derives the Black-Scholes equation from Ito\'s lemma.' },
  [K('regression/L1', 'least-squares/L3')]: { a: 'keep', move: 'regression/L3', w: 'Fits many variables by solving the matrix normal equations.' },
};

const P = JSON.parse(readFileSync(PROP, 'utf8'));
if (P.length !== 248) throw new Error(`proposal has ${P.length} rows, expected 248`);
const docs = {}, raw = {};
const doc = (c) => { if (!docs[c]) { const f = join(DIR, 'courses', c, 'course.json'); raw[c] = readFileSync(f, 'utf8'); docs[c] = JSON.parse(raw[c]); } return docs[c]; };
const refOf = (e) => (typeof e === 'string' ? e : e.ref);
const level = (id) => { const [c, l] = id.split('/'); const lv = doc(c).levels[+l.slice(1) - 1]; if (!lv) throw new Error('no level ' + id); return { c, n: +l.slice(1), lv }; };
const tally = { keep: 0, diagnostic: 0, cut: 0, retarget: 0, moved: 0, extra: 0 };
const log = [];

// Pass 1: rewrite or drop each proposal edge on its own level; collect moves and extras.
const adds = [];
for (const row of P) {
  const o = OVERRIDE[K(row.from, row.ref)] || {};
  const action = o.a || row.action, why = (o.w || row.why || '').trim();
  const { lv } = level(row.from);
  const req = lv.requires || [];
  const i = req.findIndex((e) => refOf(e) === row.ref);
  if (i < 0) throw new Error(`${row.from}: edge ${row.ref} not found`);
  if (action === 'cut' || o.move) {
    req.splice(i, 1);
    if (o.move) { adds.push({ at: o.move, edge: { ref: row.ref, why } }); tally.moved++; log.push(`move ${row.from} -> ${o.move}: ${row.ref}`); }
    else { tally.cut++; log.push(`cut ${row.from}: ${row.ref} (${why})`); }
  } else {
    const ref = action === 'retarget' ? (o.to || row.retarget) : row.ref;
    if (!ref) throw new Error(`${row.from}: retarget without ref`);
    const edge = { ref, why };
    if (action === 'diagnostic') edge.gate = false;
    req[i] = edge; tally[action]++;
    if (action === 'retarget') log.push(`retarget ${row.from}: ${row.ref} -> ${ref}`);
  }
  for (const x of o.extra || []) { adds.push({ at: row.from, edge: x }); tally.extra++; }
  lv.requires = req;
}
// Pass 2: moves and extras. A level with no explicit requires gets its previous level written in first.
for (const { at, edge } of adds) {
  const { c, n, lv } = level(at);
  if (!Array.isArray(lv.requires)) lv.requires = n > 1 ? [`${c}/L${n - 1}`] : [];
  if (!lv.requires.some((e) => refOf(e) === edge.ref)) lv.requires.push(edge);
}
// Dedupe and drop empty lists on L1 (an L1 with requires [] is the same as none).
for (const c in docs) docs[c].levels.forEach((lv, k) => {
  if (!Array.isArray(lv.requires)) return;
  const seen = new Set(); lv.requires = lv.requires.filter((e) => !seen.has(refOf(e)) && seen.add(refOf(e)));
  if (lv.requires.length === 0 && k === 0) delete lv.requires;
});

// Check: every cross-course edge carries a why; every L1 that had a gate still has one.
let missing = 0;
for (const c in docs) docs[c].levels.forEach((lv, k) => (lv.requires || []).forEach((e) => {
  if (refOf(e).split('/')[0] !== c && (typeof e === 'string' || !e.why)) { missing++; console.error(`no why: ${c}/L${k + 1} -> ${refOf(e)}`); }
}));
for (const c in docs) { const l1 = docs[c].levels[0]; const had = JSON.parse(raw[c]).levels[0].requires || [];
  if (had.length && !(l1.requires || []).some((e) => typeof e === 'string' || e.gate !== false)) { missing++; console.error(`L1 lost every gate: ${c}`); } }
if (missing) { console.error(`FAIL: ${missing} problems`); process.exit(1); }

// Text edits only: each changed level's single-line "requires" is replaced (or inserted after its "name" line),
// so the rest of each file keeps its layout. The result is parsed and compared with the intended document.
const fmt = (req, ind) => {
  if (req.every((e) => typeof e === 'string')) return `"requires": ${JSON.stringify(req).replace(/","/g, '", "')}`;
  const item = (e) => (typeof e === 'string' ? JSON.stringify(e) : '{ ' + Object.entries(e).map(([k, v]) => `${JSON.stringify(k)}: ${JSON.stringify(v)}`).join(', ') + ' }');
  return `"requires": [\n${req.map((e) => ind + '  ' + item(e)).join(',\n')}\n${ind}]`;
};
const canon = (x) => JSON.stringify(x, (k, v) => (v && typeof v === 'object' && !Array.isArray(v) ? Object.fromEntries(Object.keys(v).sort().map((q) => [q, v[q]])) : v));
let changed = 0;
for (const c in docs) {
  const before = JSON.parse(raw[c]); let text = raw[c];
  const starts = []; const re = /^(\s*)"n": (\d+),$/gm; let m;
  const from = text.indexOf('"levels"');
  while ((m = re.exec(text))) if (m.index > from) starts.push({ at: m.index, n: +m[2] });
  for (let k = docs[c].levels.length - 1; k >= 0; k--) {
    const a = JSON.stringify(before.levels[k].requires), b = JSON.stringify(docs[c].levels[k].requires);
    if (a === b) continue;
    const st = starts.find((x) => x.n === k + 1); if (!st) throw new Error(`${c}: level ${k + 1} block not found`);
    const end = (starts.find((x) => x.n === k + 2) || { at: text.length }).at;
    let block = text.slice(st.at, end);
    const ind = /^(\s*)"n"/.exec(block)[1];
    const r = /"requires": \[[^\]\n]*\]/;
    const req = docs[c].levels[k].requires;
    if (r.test(block)) {
      if (req === undefined) block = block.replace(/,?\n\s*"requires": \[[^\]\n]*\]/, '');
      else block = block.replace(r, fmt(req, ind));
    } else {
      block = block.replace(/("name": .*,\n)/, `$1${ind}${fmt(req, ind)},\n`);
    }
    text = text.slice(0, st.at) + block + text.slice(end);
  }
  if (canon(JSON.parse(text)) !== canon(docs[c])) throw new Error(`${c}: text edit does not match the intended document`);
  if (text !== raw[c]) { changed++; if (!DRY) writeFileSync(join(DIR, 'courses', c, 'course.json'), text); }
}
console.log(log.join('\n'));
console.log(`keep ${tally.keep}, diagnostic ${tally.diagnostic}, retarget ${tally.retarget}, cut ${tally.cut}, moved ${tally.moved}, extra ${tally.extra}; course files ${DRY ? 'to change' : 'changed'} ${changed}`);
