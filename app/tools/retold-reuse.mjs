// Retold screens and rate forms (ENGINE-BACKLOG 1075, 1076, 1078, 1080; engine pass AF part 1). Used by same-course-reuse.mjs (so fresh-check.mjs --file).
// Two kinds, both errors, both waivable like the others:
//   retold  a problem part (or a whole problem with no parts) tells again a screen, quiz or review item, homework item or other problem of its own course, at any level:
//           (i)  sentences: each sentence of the learner-visible text (stem, question, options) and of the lines the learner reads after answering (feedback: correct, generic, byKey; explain; why)
//                is cut to its signal words, the words that are neither numbers and maths, nor function words (held by more than FUNC_FRAC of the files of the content), nor rare words
//                (held by at most RARE_DF files: names and nouns that a retelling changes). Two sentences match when their signal words share an ordered run (LCS) of at least MIN_LCS words
//                that covers at least MIN_COVER of the shorter one. A sentence whose signal words occur in STOCK_DF or more files of the content is stock ("Not quite right.", "Give 2 decimal places.") and never counts.
//                A part is flagged with two matched sentences against one source unit, or with one match of LONG_LCS words or more.
//           (ii) chain: three or more parts of one problem follow, in order, three or more steps of one source (the screens of a lesson, the quiz, the parts of one item): the steps match by their signal words
//                (at least STEP_SHARE of them shared), whatever the nouns and numbers. A standard task asked once in new numbers is one step, not a chain.
//   rate    a rate written as a decimal or a fraction in one file and as a per cent in another (0.4167 and 5/12 against 41.7%), with a second number shared by the two units (the 0.6 of "threshold 0.6").
import { readFileSync } from 'node:fs';

export const PAR = { funcFrac: 0.3, rareDf: 3, funcWeight: 0.25, stockDf: 4, minSig: 4, minInfo: 2, minW: 2.5, fuzzyW: 6, minCover: 0.7, totalW: 4.5, longW: 10, spreadMin: 4, spreadW: 11, stepJaccard: 0.4, stepMin: 6, chainMin: 3, chainGap: 2, rateTol: 3.5e-3 };

const MATH = /\$\$[\s\S]*?\$\$|\$[^$]*\$/g;
const stem = (w) => (w.length > 4 && w.endsWith('s') && !w.endsWith('ss') ? w.slice(0, -1) : w);

// Sentences of some strings, as the learner reads them (maths kept whole, a decimal point is not a full stop).
export function splitSentences(strings) {
  const out = [];
  for (const str of strings) {
    if (typeof str !== 'string') continue;
    const maths = [];
    const t = str.replace(/```[\s\S]*?```/g, ' ').replace(MATH, (m) => { maths.push(m); return `\u0001${maths.length - 1}\u0001`; });
    for (const piece of t.split(/(?<=[.?!;:])\s+|\s*\n\s*|\s+\|\s+/)) {
      const raw = piece.replace(/\u0001(\d+)\u0001/g, (_, i) => maths[+i]).replace(/\s+/g, ' ').trim();
      if (raw) out.push(raw);
    }
  }
  return out;
}
export function wordsOf(raw) {
  const s = raw.toLowerCase().replace(MATH, ' ').replace(/\\[a-z]+/g, ' ').replace(/\d+(?:[.,]\d+)*/g, ' ').replace(/['’]s\b/g, '');
  return (s.match(/[a-z]{3,}/g) ?? []).map(stem);
}
// weighted longest common subsequence of two signal lists: { w: the weight (sum of idf) of the common words, n: how many }
export function lcs(a, b, wa) {
  let pw = new Array(b.length + 1).fill(0), pn = pw.slice();
  for (let i = 1; i <= a.length; i++) {
    const cw = new Array(b.length + 1).fill(0), cn = cw.slice();
    for (let j = 1; j <= b.length; j++) {
      if (a[i - 1] === b[j - 1]) { cw[j] = pw[j - 1] + wa[i - 1]; cn[j] = pn[j - 1] + 1; if (pw[j] > cw[j]) { cw[j] = pw[j]; cn[j] = pn[j]; } if (cw[j - 1] > cw[j]) { cw[j] = cw[j - 1]; cn[j] = cn[j - 1]; } }
      else if (pw[j] >= cw[j - 1]) { cw[j] = pw[j]; cn[j] = pn[j]; } else { cw[j] = cw[j - 1]; cn[j] = cn[j - 1]; }
    }
    pw = cw; pn = cn;
  }
  return { w: pw[b.length], n: pn[b.length] };
}

// ---- the corpus-wide model: word frequencies by file, and the stock sentences ----
// units: every unit of the content (courses, exams, bank), each with .file, .sec (setting strings) and .fbs (feedback, explain and why strings).
// Learned from the whole content (`same-course-reuse.mjs --learn` writes tools/retold-model.json); a scan of the app's own content learns it live, a scan of any other content (test fixtures) reads the snapshot.
const bump = (m, k, f) => { let a = m.get(k); if (!a) m.set(k, (a = new Set())); a.add(f); };
export function modelFrom(snap, par = PAR) {
  const wdf = new Map(Object.entries(snap.wdf));
  return { wdf, N: snap.N, funcDf: Math.max(60, Math.round(par.funcFrac * snap.N)), par, stock: new Map((snap.stock ?? []).map((k) => [k, par.stockDf])) };
}
export function learn(units, par = PAR) {
  const wdf = new Map(), files = new Set();
  for (const u of units) { files.add(u.file); for (const r of splitSentences([...u.sec, ...u.fbs])) for (const w of new Set(wordsOf(r))) bump(wdf, w, u.file); }
  const snap = { N: files.size, wdf: Object.fromEntries([...wdf].filter(([, v]) => v.size > 1).map(([k, v]) => [k, v.size]).sort()), stock: [] };
  const model = modelFrom(snap, par), sk = new Map();
  for (const u of units) { prep(u, model); for (const r of [...u.recs, ...u.orecs]) if (r.sig.length >= par.minSig && r.mass >= par.minW) bump(sk, r.key, u.file); }
  snap.stock = [...sk].filter(([, v]) => v.size >= par.stockDf).map(([k]) => k).sort();
  return snap;
}
export function buildModel(units, snap, par = PAR) {
  const model = modelFrom(snap ?? learn(units, par), par);
  for (const u of units) { prep(u, model); markStock(u, model); }
  return model;
}
const isSignal = (w, m) => (m.wdf.get(w) ?? 1) > m.par.rareDf;   // a rare word (a name, a noun that a retelling changes) is masked: left out of both sentences
// (re)computes the sentence records of a unit: recs = stem and part (what a part is held to), orecs = the unit's own text only
export function prep(u, model) {
  const mk = (strs, kind) => splitSentences(strs).map((raw) => { const sig = wordsOf(raw).filter((w) => isSignal(w, model)); const info = sig.map((x) => (model.wdf.get(x) <= model.funcDf ? 1 : 0)), w = info.map((i) => (i ? 1 : model.par.funcWeight)), idf = sig.map((x) => Math.log(model.N / model.wdf.get(x))); return { raw, sig, w, info, idf, mass: w.reduce((p, q) => p + q, 0), key: sig.join(' '), kind, unit: u }; });
  u.recs = [...mk(u.sec, 'set'), ...mk(u.fbs, 'fb')];
  u.orecs = u.osec === u.sec && u.ofbs === u.fbs ? u.recs : [...mk(u.osec, 'set'), ...mk(u.ofbs, 'fb')];
  u.rates = ratesOf([...u.sec, ...u.fbs]);
}
export function markStock(u, model) {
  for (const r of [...u.recs, ...u.orecs]) r.stock = r.sig.length < model.par.minSig || r.mass < model.par.minW || model.stock.has(r.key);
}

// ---- (i) sentences ----
// An inverted index of the sentence records of the sources of one course: signal word -> record ids.
export function buildSentenceIndex(sourceUnits) {
  const recs = [], post = new Map();
  for (const u of sourceUnits) for (const r of u.recs) { if (r.stock) continue; const id = recs.length; recs.push(r); for (const w of new Set(r.sig)) { let a = post.get(w); if (!a) post.set(w, (a = [])); a.push(id); } }
  const idf = new Map();
  for (const r of recs) r.sig.forEach((w, i) => idf.set(w, r.idf[i]));
  return { recs, post, idf };
}
const cut = (s, n = 160) => (s.length > n ? `${s.slice(0, n - 1)}…` : s);
export function sentenceMatches(t, idx, rel, par) {
  const idf = idx.idf;
  const bySource = new Map();   // source unit -> Map(target record -> best match)
  for (const a of t.recs) {
    if (a.stock) continue;
    // candidates: the source sentences holding one of the three rarest words of this sentence (a changed noun is one word, so two of the three still meet)
    const cnt = new Map();
    for (const w of [...new Set(a.sig)].sort((x, y) => (idf.get(y) ?? 0) - (idf.get(x) ?? 0)).slice(0, 3)) { const p = idx.post.get(w); if (!p || p.length > 800) continue; for (const id of p) cnt.set(id, (cnt.get(id) ?? 0) + 1); }
    for (const [id, c] of cnt) {
      const b = idx.recs[id];
      if (b.unit.file === rel) continue;
      // the same sentence once numbers, maths and names are masked; or one word changed (a noun swap: bond for loan); or, for a longer sentence, a weighted common subsequence of fuzzyW and covering minCover
      let l = a.mass;
      if (a.key !== b.key) {
        const r = lcs(a.sig, b.sig, a.w); l = r.w;
        const near = Math.min(a.sig.length, b.sig.length) >= par.minSig && r.n >= Math.max(a.sig.length, b.sig.length) - 1 && Math.min(a.mass, b.mass) >= par.minW;
        if (!near && (l < par.fuzzyW || l < par.minCover * Math.min(a.mass, b.mass))) continue;
      }
      let m = bySource.get(b.unit); if (!m) bySource.set(b.unit, (m = new Map()));
      const o = m.get(a); if (!o || l > o.l) m.set(a, { a, b, l });
    }
  }
  return bySource;
}

// ---- (ii) chain ----
// a step is the set of signal words (with their weights) of the unit's own sentences, stock ones left out; two steps match on the weighted share of their words (Jaccard)
export const stepSig = (u, par) => { const s = new Map(); for (const r of u.orecs) if (!r.stock) r.sig.forEach((w, i) => { if (r.info[i]) s.set(w, r.idf[i]); }); return s.size >= par.stepMin ? s : null; };
export const stepMatch = (a, b, par) => { let i = 0, un = 0, c = 0; for (const [w, x] of a) { un += x; if (b.has(w)) { i += x; c++; } } for (const [w, x] of b) if (!a.has(w)) un += x; return c >= par.stepMin && un > 0 && i / un >= par.stepJaccard; };
// containers of one file: [{ label, steps: [unit] }], steps in reading order
export function containersOf(units) {
  const m = new Map();
  for (const u of units) { if (!u.cont || u.hasParts || u.cont === 'items') continue; let a = m.get(u.cont); if (!a) m.set(u.cont, (a = [])); a.push(u); }
  for (const a of m.values()) a.sort((x, y) => x.idx - y.idx);
  return m;
}
function chains(t, tSteps, srcFiles, par) {
  const out = [];
  const ts = tSteps.map((u) => stepSig(u, par));
  if (ts.filter(Boolean).length < par.chainMin) return out;
  for (const [file, conts] of srcFiles) for (const [label, steps] of conts) {
    if (steps.length < par.chainMin) continue;
    const ss = steps.map((u) => stepSig(u, par));
    const best = [];   // dp over pairs (i, j)
    let top = null;
    for (let i = 0; i < ts.length; i++) for (let j = 0; j < ss.length; j++) {
      if (!ts[i] || !ss[j] || !stepMatch(ts[i], ss[j], par)) { best[i * 64 + j] = null; continue; }
      let b = { n: 1, prev: null, i, j };
      for (let i2 = Math.max(0, i - par.chainGap); i2 < i; i2++) for (let j2 = Math.max(0, j - par.chainGap); j2 < j; j2++) { const p = best[i2 * 64 + j2]; if (p && p.n + 1 > b.n) b = { n: p.n + 1, prev: p, i, j }; }
      best[i * 64 + j] = b; if (!top || b.n > top.n) top = b;
    }
    if (top && top.n >= par.chainMin) { const seq = []; for (let p = top; p; p = p.prev) seq.unshift([p.i, p.j]); out.push({ file, label, steps, seq, n: top.n }); }
  }
  return out;
}
export function scanRetold({ rel, mine, idx, srcContainers, keep, par = PAR }) {
  const agg = new Map();   // problem|source file -> { first part, source unit, distinct target sentences -> best match }
  for (const t of mine) {
    if (t.hasParts) continue;
    for (const [s, m] of sentenceMatches(t, idx, rel, par)) {
      const ms = [...m.values()].sort((x, y) => y.l - x.l);
      const longest = ms[0].l;
      const total = ms.reduce((p, x) => p + x.l, 0);
      if ((ms.length >= 2 && total >= par.totalW) || longest >= par.longW) {
        const e = `${ms.length} retold sentence${ms.length > 1 ? 's' : ''} (${ms.slice(0, 2).map((x) => `weight ${x.l.toFixed(1)}`).join(', ')}): "${cut(ms[0].a.raw, 90)}" against "${cut(ms[0].b.raw, 90)}"`;
        keep(t, s, 'retold', ms.length + longest / 1000, e, [ms[0].a.raw, ms[0].b.raw]);
      }
      if (t.part) {   // a problem that retells one source across its parts, a sentence or two in each
        const k = `${t.cont}|${s.file}`;
        let g = agg.get(k); if (!g) agg.set(k, (g = { t, s, by: new Map(), parts: new Set() }));
        for (const x of ms) { const o = g.by.get(x.a.raw); if (!o || x.l > o.l) g.by.set(x.a.raw, x); }
        g.parts.add(t.idx + 1);
        if (s.path && (g.s.n ?? 0) < ms.length) { g.s = s; g.s.n = ms.length; }
      }
    }
  }
  for (const g of agg.values()) {
    const ms = [...g.by.values()].sort((x, y) => y.l - x.l), total = ms.reduce((p, x) => p + x.l, 0);
    if (g.parts.size >= 2 && ms.length >= par.spreadMin && total >= par.spreadW) keep(g.t, g.s, 'retold', ms.length + total / 1000, `${ms.length} retold sentences across parts ${[...g.parts].sort((a, b) => a - b).join(', ')} (weight ${total.toFixed(1)}): "${cut(ms[0].a.raw, 90)}" against "${cut(ms[0].b.raw, 90)}"`, [ms[0].a.raw, ms[0].b.raw]);
  }
  // chains: the parts of each problem, in order
  const byItem = new Map();
  for (const t of mine) if (t.part) { let a = byItem.get(t.cont); if (!a) byItem.set(t.cont, (a = [])); a.push(t); }
  for (const parts of byItem.values()) {
    parts.sort((x, y) => x.idx - y.idx);
    for (const c of chains(parts[0], parts, srcContainers, par)) {
      const t0 = parts[c.seq[0][0]], s0 = c.steps[c.seq[0][1]];
      const ex = (u) => cut((u.orecs.find((r) => !r.stock && r.kind === 'set') ?? u.orecs.find((r) => !r.stock) ?? { raw: '' }).raw, 90);
      keep(t0, s0, 'retold', c.n, `chain of ${c.n} steps: parts ${c.seq.map(([i]) => parts[i].idx + 1).join(', ')} follow ${c.label} steps ${c.seq.map(([, j]) => c.steps[j].path.replace(/^.*\[(\d+)\]$/, '$1')).join(', ')} ("${ex(t0)}" against "${ex(s0)}")`, [ex(t0), ex(s0)]);
    }
  }
}

// ---- rate form ----
const sig3 = (s) => s.replace(/^[0.\s]+/, '').replace('.', '').replace(/^0+/, '').length;
export function ratesOf(strings) {
  const rates = [], rest = new Set();
  for (const raw of splitSentences(strings)) {
    let t2 = raw.replace(/\\[td]?frac\{(\d+)\}\{(\d+)\}/g, '$1/$2').replace(/\\left|\\right|\\[,;! ]|\{,\}/g, '').replace(/(?<=\d),(?=\d{3}(?!\d))/g, '');
    const take = (re, f) => { t2 = t2.replace(re, (m, ...g) => { f(m, g); return ' '; }); };
    take(/(\d+(?:\.\d+)?)\s*(?:\\%|%|per ?cent)/g, (m, g) => { const x = Number(g[0]); if (sig3(g[0]) >= 3 && x > 0 && x <= 100) rates.push({ v: x / 100, ulp: 0.5 * 10 ** -(g[0].split('.')[1] ?? '').length / 100, form: 'pct', text: m.trim(), sentence: raw }); });
    take(/(?<![\d./])(\d+)\/(\d+)(?![\d/])/g, (m, g) => { const a = Number(g[0]), b = Number(g[1]); if (a > 0 && a < b && b >= 7) rates.push({ v: a / b, ulp: 0, form: 'frac', text: m.trim(), sentence: raw }); });
    take(/(?<![\d.])0?\.(\d{3,})(?!\d)/g, (m, g) => { if (sig3(`0.${g[0]}`) >= 3) rates.push({ v: Number(`0.${g[0]}`), ulp: 0.5 * 10 ** -g[0].length, form: 'dec', text: m.trim(), sentence: raw }); });
    for (const m of t2.matchAll(/(?<![\w.])\d+(?:\.\d+)?(?![\w])/g)) { const k = String(+m[0]); if (!secondStock(k)) rest.add(k); }
  }
  return { rates, rest };
}
const DEC_STOCK = new Set(['0.5', '0.25', '0.75', '0.05', '0.95', '0.01', '0.99', '0.1', '0.9', '0.025', '0.975', '0.001', '0.999', '1.96', '1.645', '2.576', '0.2', '0.8', '0.3', '0.7', '1.5', '2.5']);
const secondStock = (k) => { const v = Number(k); return DEC_STOCK.has(k) || (Number.isInteger(v) && v <= 20) || (v >= 1900 && v <= 2100 && Number.isInteger(v)) || v === 0 || [25, 30, 40, 50, 60, 75, 100, 200, 250, 500, 1000, 10000, 365, 252, 12, 24, 120, 150, 300, 400, 600, 1200].includes(v); };
export function matchRates(t, s, par = PAR) {
  const a = t.rates, b = s.rates;
  if (!a.rates.length || !b.rates.length) return null;
  const second = [...a.rest].filter((k) => b.rest.has(k));
  if (!second.length) return null;
  for (const x of a.rates) for (const y of b.rates) {
    if ((x.form === 'pct') === (y.form === 'pct')) continue;
    if (Math.abs(x.v - y.v) <= Math.max(x.ulp, y.ulp) * 1.02 + 1e-9) return { x, y, second: second[0] };   // equal to the rounding of the cruder of the two
  }
  return null;
}
export const rateEvidence = (r) => `the rate ${r.x.text} here and ${r.y.text} there, with ${r.second} in both`;
