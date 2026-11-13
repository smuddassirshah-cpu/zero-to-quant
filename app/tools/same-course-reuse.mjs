#!/usr/bin/env node
// Same-course reuse (ENGINE-BACKLOG 972). A new problem set must not reuse its own course's lessons, quizzes, reviews, homework or other problem sets:
// the numbers, a matrix (up to a scalar and a transpose) or a run of sentences (DECISIONS session AB reuse rule, session AC reuse rulings).
// fresh-check.mjs ran against exams, the bank and drills and against other courses; it did not compare a set with its own course.
//
// Usage (from app/): node tools/same-course-reuse.mjs [--all | --file <json>] [--json] [--no-waivers] [--content <dir>]
//   --all            every problems-<n>.json of every course (the gate: exit 1 on an unwaived error)
//   --file <json>    one file of any kind (a review, homework or lesson too); fresh-check.mjs --file runs this by default for problems-<n>.json (--no-same-course to skip)
//   --numbers n      shared distinctive numbers needed for a numbers hit (default 3)       --df n   a number or matrix held by more than n units of the app is not distinctive (default 40)
//   --warn-run n     shared words in one run for a text warning (default 10)                 --error-run n   for a text error (default 12)
//   --boiler n       a shingle held by more than n units of the app is boilerplate (default 20)
// Kinds: numbers (warning), matrix (error), text (warning from --warn-run words, error from --error-run). The sources are every other file of the course (lessons with their quizzes,
// reviews, homework, problem sets; the generated fluency-* files are left out). Waivers: tools/same-course-waivers.json, or "reuseWaiver": "reason" on the item.
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname, resolve, relative, isAbsolute, sep } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const APP = join(HERE, '..');
const rd = (p) => JSON.parse(readFileSync(p, 'utf8'));
const jsonFiles = (d) => (existsSync(d) ? readdirSync(d).filter((f) => f.endsWith('.json')).sort() : []);

// ---- text of a unit ----
const TEXT_KEYS = new Set(['prose', 'question', 'prompt', 'brief', 'definition', 'constraints', 'stem', 'text', 'title', 'columns', 'name']);
const SKIP_TEXT = new Set(['feedback', 'explain', 'hints', 'hint', 'why', 'wrong', 'solution', 'starter', 'tests', 'examples', 'canvas', 'rubric', 'answer', 'skills', 'tags', 'id']);
const NOT_DATA = new Set(['starter', 'solution', 'tests', 'examples', 'id', 'skills', 'tags', 'rubric', 'model', 'data', 'fn']);
function collect(node, out, on) {
  if (typeof node === 'string') { if (on) out.push(node); return; }
  if (Array.isArray(node)) { for (const v of node) collect(v, out, on); return; }
  if (node && typeof node === 'object') for (const [k, v] of Object.entries(node)) {
    if (SKIP_TEXT.has(k)) continue;
    if (k === 'options' && Array.isArray(v) && node.shuffle !== false && (node.kind === 'choice' || node.kind === 'multi')) { for (const o of v) { collect(o, out, on); out.push(' | '); } continue; }
    collect(v, out, on || TEXT_KEYS.has(k));
  }
}
// everything the learner or the key shows: text, options, answers, slips, explanations (code and ids left out), for numbers and matrices
function allStrings(node, out = [], numOut = []) {
  if (typeof node === 'string') { out.push(node); return { out, numOut }; }
  if (typeof node === 'number') { numOut.push(node); return { out, numOut }; }
  if (Array.isArray(node)) { for (const v of node) allStrings(v, out, numOut); return { out, numOut }; }
  if (node && typeof node === 'object') for (const [k, v] of Object.entries(node)) { if (!NOT_DATA.has(k)) allStrings(v, out, numOut); }
  return { out, numOut };
}
// Boilerplate sentences of AUTHORING are cut out and break a run (the same list as fresh-check.mjs STOPLIST, plus the common answer-format lines)
const STOPLIST = [
  /put the (?:lines|steps|proof|derivation|argument|lines of the \w+) in order(?:, a reason in each line)?\.?/g,
  /(?:leave out|move|drop) the (?:\w+ )?(?:lines?|steps?|ones?) (?:that )?(?:do(?:es)? not belong|(?:is|are) flawed)\.?/g,
  /select all that apply:?\.?/g,
  /give (?:your answer |the answer |it )?(?:to |as |in )?(?:\w+ )?(?:decimal places?|significant figures|a fraction or a decimal|a decimal|a percentage|pounds)\.?/g,
  /say the (?:reasoning|argument) aloud (?:first|before you answer)\.?/g,
  /which statements? (?:is|are) (?:right|true)\?/g,
  /what does (?:it|that) (?:print|return)\?/g,
];
// Sentences: maths spans, commands and numbers become "#"; an answer-format sentence (give, type, enter, round, express, using ...) is cut out, and so is any
// sentence held by BOILER_SENT or more units of the app (a stock instruction, found by frequency); the rest is one token list with a "|" between sentences.
// A sentence that asks the stock question (what is, how many, which, find ...) or says how to answer is the task or the format, not the setting: the ruling allows the same standard task.
const FORMAT_LEAD = /^(?:give|type|enter|round|answer|express|using|use|state|report|quote|input|what|how|which|why|who|find|work out|calculate|compute|by how|is |does |do |can |are |write down)\b|\b(?:decimal places?|significant figures?|nearest (?:penny|pound|whole|integer|cent|hundredth|tenth)|as a (?:fraction|decimal|percentage)|exact fraction|minus sign)\b/;
export function sentences(strings) {
  let s = strings.join(' \n ').toLowerCase().replace(/```[a-z+]*/g, ' ');
  for (const re of STOPLIST) s = s.replace(re, ' | ');
  s = s.replace(/\$\$[\s\S]*?\$\$|\$[^$]*\$/g, ' # ').replace(/\\[a-z]+|\\[\\,;:!{}()[\]]/g, ' # ').replace(/\d+(?:[.,]\d+)*(?:e[+-]?\d+)?/g, ' # ');
  const out = [];
  for (const sen of s.split(/(?<=[.?!;:])\s+|\s*\|\s*|\n/)) {
    const tk = (sen.match(/[a-z]+|#/g) ?? []).filter((t, i, o) => !(t === '#' && o[i - 1] === '#'));
    if (!tk.some((t) => t !== '#') || FORMAT_LEAD.test(tk.join(' '))) continue;
    out.push(tk.join(' '));
  }
  return out;
}
const BOILER_SENT = 5;
const MAT_STOCK = 40;   // a matrix (up to a scalar and a transpose) held by more than this many files of other courses and the exams is a textbook staple
const tokensOf = (sens, sdf) => sens.filter((x) => (sdf.get(x) ?? 0) < BOILER_SENT).flatMap((x, i) => (i ? ['|', ...x.split(' ')] : x.split(' ')));
const STOP = new Set('what is the of and a an to in on for with that this which be are by it its at as from has have then give find how many much do does you your one two'.split(' '));
const informative = (g) => new Set(g.filter((t) => t !== '#' && !STOP.has(t))).size >= 3;
const NG = 8;
function shingles(tk) { const o = []; for (let i = 0; i + NG <= tk.length; i++) { const g = tk.slice(i, i + NG); if (!g.includes('|') && informative(g)) o.push(g.join(' ')); } return o; }
function longestRun(a, b) {   // longest common run, scored in words ("#" joins a run and does not count)
  let best = 0, end = 0, endLen = 0, prev = new Array(b.length + 1).fill(0), prevL = prev.slice();
  for (let i = 1; i <= a.length; i++) {
    const cur = new Array(b.length + 1).fill(0), curL = cur.slice();
    for (let j = 1; j <= b.length; j++) if (a[i - 1] === b[j - 1] && a[i - 1] !== '|') {
      cur[j] = prev[j - 1] + (a[i - 1] === '#' ? 0 : 1); curL[j] = prevL[j - 1] + 1;
      if (cur[j] > best) { best = cur[j]; end = i; endLen = curL[j]; }
    }
    prev = cur; prevL = curL;
  }
  return { len: best, text: a.slice(end - endLen, end).join(' ') };
}

// ---- numbers ----
// Distinctive: not a whole number up to 20, not a year, not a standard constant, not a number held by more than DF units of the app.
const CONSTS = new Set(['0.5', '0.25', '0.75', '0.1', '0.05', '0.01', '0.001', '0.025', '0.975', '0.95', '0.99', '0.9', '1.5', '1.96', '1.645', '2.576', '2.33', '3.14', '3.1416', '2.718', '1.414', '0.693', '0.6931', '0.0001', '0.005', '0.0005', '0.2', '0.3', '0.4', '0.6', '0.7', '0.8', '0.15', '0.35', '0.45', '0.55', '0.65', '0.85', '0.02', '0.03', '0.04', '0.06', '0.07', '0.08', '0.09', '2.5', '3.5', '4.5', '0.125', '0.375', '0.625', '0.875', '0.2', '1.2', '1.25']);
const stockInt = (v) => Number.isInteger(v) && (Math.abs(v) <= 20 || (v >= 1900 && v <= 2100) || [25, 30, 40, 50, 60, 75, 100, 200, 250, 500, 1000, 10000, 365, 252, 12, 24, 120, 150, 300, 400, 600, 1200].includes(Math.abs(v)));
function numberSet(strs, nums) {
  const out = new Map();   // key -> value
  const add = (v) => { if (!Number.isFinite(v) || v === 0 || stockInt(v)) return; const key = String(+Math.abs(v).toPrecision(9)); if (CONSTS.has(key)) return; out.set(key, Math.abs(v)); };
  for (const s of strs) {
    const t = s.replace(/(?<=\d)(?:,|\{,\}|\\,|\\;| )(?=\d{3}(?!\d))/g, '').replace(/\\frac\{(\d+)\}\{(\d+)\}|\\[td]frac\{(\d+)\}\{(\d+)\}/g, ' ');   // thousands separators; a typed fraction is not a number here
    for (const m of t.matchAll(/(?<![\w.])\d+(?:\.\d+)?(?![\w])/g)) add(Number(m[0]));
  }
  for (const v of nums) add(v);
  return out;
}

// Values within 0.2% of each other (2249, 2250, 2251; 0.5833, 0.583333) are one number: a rounding or a band, not a second figure.
function cluster(entries) {
  const s = [...entries].sort((a, b) => a[1] - b[1]), out = [];
  for (const e of s) { const l = out[out.length - 1]; if (l && Math.abs(e[1] - l[1]) <= 2e-3 * Math.abs(l[1])) continue; out.push(e); }
  return out;
}
// A simple scale: a whole number from 2 to 12, 1.5 or 2.5, or the reciprocal of one (a decimal shift, times 10 or 100, is how probabilities and percentages relate: not counted).
const niceScale = (r) => { if (!(r > 0)) return false; const ok = (x) => [1.5, 2.5].some((v) => Math.abs(x - v) < 1e-6 * v) || (Math.abs(x - Math.round(x)) < 1e-6 * x && Math.round(x) >= 2 && Math.round(x) <= 12); return ok(r) || ok(1 / r); };
function sharedClustered(tn, s) { return cluster(tn.filter(([k]) => s.nums.has(k))); }

// ---- matrices ----
function cellValue(c) {
  let s = c.trim().replace(/\\[td]?frac\{(-?[\d.]+)\}\{(-?[\d.]+)\}/g, '($1/$2)').replace(/\\[,;! ]|\s+/g, '').replace(/^\+/, '');
  const m = s.match(/^(-?)\(?(-?[\d.]+)(?:\/(-?[\d.]+))?\)?$/);
  if (!m) { const n = s.match(/^-?\d*\.?\d+$/); return n ? Number(s) : NaN; }
  const v = Number(m[2]) / (m[3] === undefined ? 1 : Number(m[3]));
  return m[1] ? -v : v;
}
function parseLatexMatrices(s) {
  const out = [];
  for (const m of s.matchAll(/\\begin\{([pbv]?)matrix\}([\s\S]*?)\\end\{\1matrix\}/g)) out.push(m[2].split(/\\\\/).map((r) => r.split('&').map(cellValue)).filter((r) => r.length && !(r.length === 1 && Number.isNaN(r[0]) && false)));
  for (const m of s.matchAll(/\[\s*\[[^[\]]*\](?:\s*,\s*\[[^[\]]*\])+\s*\]/g)) { try { const a = JSON.parse(m[0]); if (Array.isArray(a) && a.every(Array.isArray)) out.push(a.map((r) => r.map((x) => (typeof x === 'number' ? x : NaN)))); } catch { /* not a matrix */ } }
  return out;
}
function jsonMatrices(node, out) {   // canvas matrices ({ rows }) and state.matrix
  if (Array.isArray(node)) { for (const v of node) jsonMatrices(v, out); return; }
  if (!node || typeof node !== 'object') return;
  for (const [k, v] of Object.entries(node)) {
    if ((k === 'rows' || k === 'matrix') && Array.isArray(v) && v.length && v.every((r) => Array.isArray(r) && r.every((x) => typeof x === 'number'))) out.push(v);
    else if (v && typeof v === 'object') jsonMatrices(v, out);
  }
}
const fmt = (x) => String(+x.toPrecision(9));
function canonOne(rows) {   // divide by the first non-zero entry (row-major), so a non-zero multiple, negative ones too, gives one form
  const flat = rows.flat(), p = flat.find((x) => Math.abs(x) > 1e-12);
  return `${rows.length}x${rows[0].length}:` + flat.map((x) => fmt(x / p + 0)).join(',');
}
export function matrixKey(rows) {   // null when it is not a numeric matrix of two or more rows and columns, or is stock (identity, zero, fewer than three distinct non-zero sizes)
  if (!rows.length || rows.length < 2 || rows.some((r) => r.length !== rows[0].length) || rows[0].length < 2 || rows.flat().some((x) => !Number.isFinite(x))) return null;
  const flat = rows.flat();
  if (flat.every((x) => Math.abs(x) < 1e-12)) return null;
  const t = rows[0].map((_, j) => rows.map((r) => r[j]));
  const a = canonOne(rows), b = canonOne(t);
  const p = flat.find((x) => Math.abs(x) > 1e-12);
  const norm = flat.map((x) => Math.abs(x / p));
  const identity = rows.length === rows[0].length && rows.every((r, i) => r.every((x, j) => (i === j ? Math.abs(x - p) < 1e-12 : Math.abs(x) < 1e-12)));
  if (identity) return null;
  if (new Set(norm.filter((x) => x > 1e-12).map(fmt)).size < 3) return null;
  return a < b ? a : b;
}

// Numeric keys (answer, answers, wrong[].value): a whole number or one of three significant figures or fewer (a computed tail such as 0.0406 is a consequence of the setting, not part of it).
function keyNums(node, out = []) {
  if (Array.isArray(node)) { for (const v of node) keyNums(v, out); return out; }
  if (node && typeof node === "object") for (const [k, v] of Object.entries(node)) {
    const ok = (x) => typeof x === "number" && (Number.isInteger(x) || String(+Math.abs(x).toPrecision(9)).replace(".", "").replace(/^0+/, "").length <= 3);
    if (k === "answer" && ok(v)) out.push(v);
    else if (k === "answers" && Array.isArray(v)) v.forEach((x) => ok(x) && out.push(x));
    else if (k === "wrong" && Array.isArray(v)) v.forEach((w) => w && ok(w.value) && out.push(w.value));
    else if (v && typeof v === "object" && !NOT_DATA.has(k)) keyNums(v, out);
  }
  return out;
}
const isFluency = (f) => /^fluency-/.test(f);
function unitsOfFile(doc, rel) {
  const u = [];
  const add = (path, node, stem) => {
    const sec = [], mats = [];
    for (const n of stem ? [stem, node] : [node]) { collect(n, sec, false); }
    const { out, numOut } = allStrings(stem ? [stem, node] : node);
    for (const s of out) for (const m of parseLatexMatrices(s)) mats.push(m);
    jsonMatrices(stem ? [stem, node] : node, mats);
    if (!sec.length && !out.length) return;
    u.push({ file: rel, path, sens: sentences(sec), nums: numberSet(sec, keyNums([stem, node])), mats: new Set(mats.map(matrixKey).filter(Boolean)) });
  };
  const withParts = (path, q) => {
    add(path, q);
    if (Array.isArray(q.parts)) { const { parts, ...stem } = q; q.parts.forEach((p, j) => add(`${path}.parts[${j}]`, p, stem)); }
  };
  (doc.screens ?? []).forEach((s, i) => add(`screens[${i}]`, s));
  (Array.isArray(doc.quiz) ? doc.quiz : doc.quiz?.items ?? []).forEach((q, i) => add(`quiz[${i}]`, q));
  (doc.items ?? []).forEach((q, i) => withParts(`items[${i}]`, q));
  return u;
}
const courseFiles = (C, c) => jsonFiles(join(C, 'courses', c)).filter((f) => f !== 'course.json' && !isFluency(f));

// Frequencies count distinct files (a part repeats its item's stem, so units would count one item several times).
export function loadCorpus(C) {
  const df = { num: new Map(), mat: new Map(), sh: new Map(), sen: new Map() };
  const bump = (m, k, f) => { let a = m.get(k); if (!a) m.set(k, (a = new Set())); a.add(f); };
  const byFile = new Map(), all = [], courses = existsSync(join(C, 'courses')) ? readdirSync(join(C, 'courses')).sort() : [];
  const add = (rel, units) => { all.push(...units); return units; };
  for (const c of courses) for (const f of courseFiles(C, c)) { const rel = `courses/${c}/${f}`; byFile.set(rel, add(rel, unitsOfFile(rd(join(C, rel)), rel))); }
  for (const sub of ['exams', 'bank']) for (const f of jsonFiles(join(C, sub))) add(`${sub}/${f}`, unitsOfFile(rd(join(C, sub, f)), `${sub}/${f}`));
  for (const x of all) for (const sn of x.sens) bump(df.sen, sn, x.file);
  const sdf = new Map([...df.sen].map(([k, v]) => [k, v.size]));
  for (const x of all) {
    x.tk = tokensOf(x.sens, sdf); x.sh = new Set(shingles(x.tk));
    for (const k of x.nums.keys()) bump(df.num, k, x.file);
    for (const k of x.mats) bump(df.mat, k, x.file);
    for (const k of x.sh) bump(df.sh, k, x.file);
  }
  for (const m of [df.sh]) for (const [k, v] of m) m.set(k, v.size);
  return { df, byFile, courses, sdf };
}

// ---- scan ----
const O = (argv, k, d) => { const i = argv.indexOf(k); return i >= 0 && argv[i + 1] !== undefined ? argv[i + 1] : d; };
export function scanSet(corpus, rel, doc, opts = {}) {
  const { numbers = 3, df: DF = 15, warnRun = 10, errorRun = 12, boiler = 5 } = opts;
  const course = rel.split('/')[1], hits = [];
  const mine = corpus.byFile.get(rel) ?? unitsOfFile(doc, rel);
  if (!corpus.byFile.has(rel)) for (const x of mine) { x.tk = tokensOf(x.sens, corpus.sdf); x.sh = new Set(shingles(x.tk)); }
  const sources = [...corpus.byFile.entries()].filter(([f]) => f !== rel && f.startsWith(`courses/${course}/`)).flatMap(([, us]) => us);
  const outside = (m, k) => [...(m.get(k) ?? [])].filter((f) => !f.startsWith(`courses/${course}/`)).length;   // files of other courses and exams: a figure the course alone repeats is the reuse, not a stock number
  const dfn = (k) => outside(corpus.df.num, k);
  // an index of shingles over the sources, for the text kind
  const idx = new Map();
  sources.forEach((s, i) => { for (const g of s.sh) if ((corpus.df.sh.get(g) ?? 0) <= boiler) { let a = idx.get(g); if (!a) idx.set(g, (a = [])); a.push(i); } });
  const best = new Map();   // item|source file|kind -> hit
  const keep = (t, s, kind, score, evidence) => {
    const item = t.path.replace(/\.parts\[\d+\]$/, ''), part = t.path.includes('.parts[') ? Number(t.path.match(/parts\[(\d+)\]$/)[1]) + 1 : null;
    const k = `${item}|${s.file}|${kind}`, o = best.get(k);
    if (!o || score > o.score || (score === o.score && part && !o.part)) best.set(k, { file: rel, item, itemPath: item, part, kind, source: `${s.file}:${s.path}`, score, evidence });
  };
  for (const t of mine) {
    // numbers
    const tn = [...t.nums].filter(([k]) => dfn(k) <= DF);
    const tset = new Map(tn);
    for (const s of sources) {
      if (!t.nums.size || !s.nums.size) continue;
      const sn = [...s.nums].filter(([k]) => dfn(k) <= DF);
      const shared = sharedClustered(tn, s).map(([k]) => k);
      if (shared.length >= numbers) keep(t, s, 'numbers', shared.length, `${shared.length} shared distinctive numbers (${shared.slice(0, 6).join(' ')})`);
      else if (sn.length && tn.length) {   // the same numbers under one common, simple scale factor (a homework figure times four)
        const tc = cluster(tn), sc = cluster(sn);
        const cnt = new Map();
        for (const [, x] of tc) for (const [, y] of sc) { const r = x / y; if (!niceScale(r)) continue; const kk = String(+r.toPrecision(5)); let a = cnt.get(kk); if (!a) cnt.set(kk, (a = new Set())); a.add(x); }
        let top = null;
        for (const [kk, a] of cnt) if (a.size >= numbers && (!top || a.size > top[1])) top = [kk, a.size];
        if (top && top[1] >= Math.max(numbers, Math.ceil(0.5 * Math.min(tc.length, sc.length)))) {
          const f = Number(top[0]), pairs = [];
          for (const [a, x] of tc) { const y = sc.find(([, y]) => Math.abs(x / y - f) < 1e-4 * f); if (y) pairs.push(`${a}=${top[0]}x${y[0]}`); }
          if (pairs.length >= numbers) keep(t, s, 'numbers', pairs.length, `${pairs.length} numbers share the scale factor ${top[0]} (${pairs.slice(0, 5).join(' ')})`);
        }
      }
    }
    // matrices
    for (const mk of t.mats) { if (outside(corpus.df.mat, mk) > MAT_STOCK) continue; for (const s of sources) if (s.mats.has(mk)) keep(t, s, 'matrix', 1, `matrix ${mk.replace(/^\d+x\d+:/, '[').replace(/,/g, ' ')}] equal up to a scalar and a transpose`); }
    // text
    const cand = new Set();
    for (const g of t.sh) for (const i of idx.get(g) ?? []) cand.add(i);
    for (const i of cand) {
      const s = sources[i], r = longestRun(t.tk, s.tk);
      if (r.len >= warnRun) keep(t, s, 'text', r.len, `${r.len} shared words: "${r.text.slice(0, 90)}"`);
    }
  }
  const waive = waivers(rel, doc);
  for (const h of best.values()) {
    h.level = h.kind === 'matrix' || (h.kind === 'text' && h.score >= errorRun) ? 'error' : 'warn';
    const w = waive(h);
    if (w) { h.waived = w; }
    hits.push(h);
  }
  return hits.sort((a, b) => a.item.localeCompare(b.item, undefined, { numeric: true }) || a.kind.localeCompare(b.kind));
}

// Waivers: tools/same-course-waivers.json ([{ file, item, kind (or "*"), reason }]) and "reuseWaiver": "reason" on an item.
let waiverList = null;
function waivers(rel, doc) {
  if (!waiverList) { const p = join(HERE, 'same-course-waivers.json'); waiverList = existsSync(p) && !process.env.ZQ_NO_WAIVERS ? rd(p) : []; }
  const byItem = new Map((doc.items ?? []).filter((q) => typeof q.reuseWaiver === 'string' && q.reuseWaiver.trim()).map((q) => [q.id, q.reuseWaiver]));
  return (h) => {
    const id = (doc.items?.[Number(h.item.match(/\d+/)[0])] ?? {}).id;
    if (byItem.has(id)) return byItem.get(id);
    const w = waiverList.find((x) => x.file === rel && x.item === id && (x.kind === '*' || x.kind === h.kind));
    return w ? w.reason : null;
  };
}

export const fmtHit = (h, doc) => `[same-course-reuse] ${h.waived ? 'waived' : h.level}  ${h.file}  ${(doc?.items?.[Number(h.item.match(/\d+/)[0])] ?? {}).id ?? h.item}  ${h.item}${h.part ? ` part ${h.part}` : ''}  ${h.kind}  <-  ${h.source}  ${h.evidence}`;

const main = () => {
  const argv = process.argv.slice(2), has = (k) => argv.includes(k);
  const C = O(argv, '--content', join(APP, 'content'));
  const opts = { numbers: Number(O(argv, '--numbers', 3)), df: Number(O(argv, '--df', 15)), warnRun: Number(O(argv, '--warn-run', 10)), errorRun: Number(O(argv, '--error-run', 12)), boiler: Number(O(argv, '--boiler', 5)) };
  if (has('--no-waivers')) process.env.ZQ_NO_WAIVERS = '1';
  const corpus = loadCorpus(C);
  let rels = [];
  if (O(argv, '--file', null)) { const abs = resolve(O(argv, '--file')), r = relative(resolve(C), abs); rels = [r.split(sep).join('/')]; }
  else if (has('--all')) rels = [...corpus.byFile.keys()].filter((f) => /\/problems-\d+\.json$/.test(f));
  else { console.error('usage: same-course-reuse.mjs --all | --file <json> [--json] [--no-waivers] [--numbers n] [--df n] [--warn-run n] [--error-run n] [--content dir]'); process.exit(2); }
  const all = [];
  for (const rel of rels) { const doc = rd(join(C, rel)); for (const h of scanSet(corpus, rel, doc, opts)) all.push({ ...h, line: fmtHit(h, doc), itemId: (doc.items?.[Number(h.item.match(/\d+/)[0])] ?? {}).id }); }
  if (has('--json')) console.log(JSON.stringify(all.map(({ line, ...h }) => h), null, 1));
  else for (const h of all) console.log(h.line);
  const errs = all.filter((h) => h.level === 'error' && !h.waived), warns = all.filter((h) => h.level === 'warn' && !h.waived), waived = all.filter((h) => h.waived);
  const by = (l) => ['numbers', 'matrix', 'text'].map((k) => `${k} ${l.filter((h) => h.kind === k).length}`).join(', ');
  if (!has('--json')) console.log(`[same-course-reuse] ${rels.length} file(s): ${errs.length} error(s) (${by(errs)}), ${warns.length} warning(s) (${by(warns)}), ${waived.length} waived`);
  process.exitCode = errs.length ? 1 : 0;
};
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) main();
