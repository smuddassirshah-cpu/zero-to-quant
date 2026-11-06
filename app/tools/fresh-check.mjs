#!/usr/bin/env node
// Freshness check (ENGINE-BACKLOG 588). Flags items whose prose, question or widget prompt text
// copies a lesson screen, quiz, review, homework or other exam item, even with changed numbers.
// Usage (from app/): node tools/fresh-check.mjs --exam <id> | --drill <id> | --bank <file> | --all-exams
//                    [--threshold n] [--min-run n] [--min-share x] [--ngram n] [--json] [--content <dir>] [--file <json> [--as exams]]
// Exit 1 on any hit. A hit is a shared word n-gram (default 8 tokens, numbers normalised to "#")
// or a 5-word shingle Jaccard at or above the threshold (default 0.5).
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const argv = process.argv.slice(2);
const opt = (k, d) => { const i = argv.indexOf(k); return i >= 0 && argv[i + 1] !== undefined ? argv[i + 1] : d; };
const has = (k) => argv.includes(k);
const APP = join(dirname(fileURLToPath(import.meta.url)), '..');
const C = opt('--content', join(APP, 'content'));
const MIN_RUN = Number(opt('--min-run', 8)), MIN_SHARE = Number(opt('--min-share', 0));
const THRESH = Number(opt('--threshold', 0.5));
const NGRAM = Number(opt('--ngram', 8));
const SHINGLE = Number(opt('--shingle', 5)), BOILER = Number(opt('--boiler', 20)), MIN_SHINGLES = 8, MIN_WORDS = 3, MIN_WORDS_N = 3;
const rd = (p) => JSON.parse(readFileSync(p, 'utf8'));
const jsonFiles = (d) => (existsSync(d) ? readdirSync(d).filter((f) => f.endsWith('.json')).sort() : []);

// Text that counts: the question side of an item. Answers, feedback, hints and code are skipped.
const TEXT_KEYS = new Set(['prose', 'question', 'prompt', 'brief', 'definition', 'constraints', 'stem', 'text', 'title', 'columns', 'name']);
const SKIP_KEYS = new Set(['feedback', 'explain', 'hints', 'hint', 'why', 'wrong', 'solution', 'starter', 'tests', 'examples', 'canvas', 'rubric', 'answer', 'skills', 'tags', 'id']);
function collect(node, out, on) {
  if (typeof node === 'string') { if (on) out.push(node); return; }
  if (Array.isArray(node)) { for (const v of node) collect(v, out, on); return; }
  if (node && typeof node === 'object') {
    for (const [k, v] of Object.entries(node)) {
      if (SKIP_KEYS.has(k)) continue;
      collect(v, out, on || TEXT_KEYS.has(k));
    }
  }
}
// Lower-case, strip KaTeX delimiters and markup, numbers become "#".
function tokens(strings) {
  let s = strings.join(' \n ').toLowerCase();
  s = s.replace(/```[a-z+]*/g, ' ');
  s = s.replace(/\\([a-z]+)/g, ' $1 ').replace(/\\[\\,;:!{}()[\]]/g, ' ');
  s = s.replace(/\d+(?:[.,]\d+)*(?:e[+-]?\d+)?/g, ' # ');
  // Words, variables and LaTeX command names; a run of numbers collapses to one "#".
  return (s.match(/[a-z]+|#/g) ?? []).filter((t, i, o) => !(t === '#' && o[i - 1] === '#'));
}
// A window of repeated symbols (x # y # x # y #) is not shared phrasing: it needs enough distinct tokens.
const STOP = new Set('what is the of and a an to in on for with that this which be are by it its at as from has have then give find how many much do does you your one two'.split(' '));
const informative = (g) => new Set(g.filter((t) => t !== '#' && !STOP.has(t))).size >= (g.length >= NGRAM ? MIN_WORDS_N : MIN_WORDS);
function grams(tk, n) { const o = []; for (let i = 0; i + n <= tk.length; i++) o.push(tk.slice(i, i + n)); return o; }

// Units: one lesson screen / quiz item / review item / homework item / exam item / drill / bank item.
function unitsOf(file, rel) {
  const d = rd(file), u = [];
  const add = (path, node) => { const out = []; collect(node, out, false); const tk = tokens(out); if (tk.length) u.push({ file: rel, path, tk }); };
  if (rel.startsWith('courses/')) {
    (d.screens ?? []).forEach((s, i) => add(`screens[${i}]`, s));
    const qz = Array.isArray(d.quiz) ? d.quiz : d.quiz?.items ?? [];
    qz.forEach((q, i) => add(`quiz[${i}]`, q));
    (d.items ?? []).forEach((q, i) => add(`items[${i}]`, q));
  } else if (rel.startsWith('exams/')) {
    const walk = (items, base) => (items ?? []).forEach((q, i) => add(`${base}items[${i}]`, q));
    walk(d.items, '');
    (d.parts ?? []).forEach((p, i) => walk(p.items, `parts[${i}].`));
  } else if (rel.startsWith('bank/')) (d.items ?? []).forEach((q, i) => add(`items[${i}]`, q));
  else if (rel.startsWith('drills/')) add('', d);
  return { id: d.id, units: u };
}
function listAll() {
  const files = [];
  for (const c of existsSync(join(C, 'courses')) ? readdirSync(join(C, 'courses')).sort() : []) {
    for (const f of jsonFiles(join(C, 'courses', c))) if (f !== 'course.json') files.push(`courses/${c}/${f}`);
  }
  for (const sub of ['exams', 'bank', 'drills']) for (const f of jsonFiles(join(C, sub))) files.push(`${sub}/${f}`);
  return files;
}

// Corpus. Boilerplate is counted in units (screens, items), so a stock phrase used in a few long files still drops out.
const corpus = [];
const fileIds = {};
for (const rel of listAll()) { const r = unitsOf(join(C, rel), rel); fileIds[rel] = r.id; for (const x of r.units) corpus.push({ ...x, id: r.id }); }
const dfN = new Map(), dfS = new Map();
{
  const seen = new Map();
  for (const x of corpus) {
    for (const [pre, n] of [['n', NGRAM], ['s', SHINGLE]]) {
      for (const g of grams(x.tk, n)) { const k = pre + g.join(' '); let s = seen.get(k); if (!s) seen.set(k, (s = new Set())); s.add(x.file + ':' + x.path); }
    }
  }
  for (const [k, s] of seen) (k[0] === 'n' ? dfN : dfS).set(k.slice(1), s.size);
}
const keepN = (tk) => new Set(grams(tk, NGRAM).filter(informative).map((g) => g.join(' ')).filter((g) => (dfN.get(g) ?? 0) <= BOILER));
const keepS = (tk) => new Set(grams(tk, SHINGLE).filter(informative).map((g) => g.join(' ')).filter((g) => (dfS.get(g) ?? 0) <= BOILER));
const idxN = new Map(), idxS = new Map();
corpus.forEach((x, i) => {
  x.ngrams = keepN(x.tk); x.shingles = keepS(x.tk);
  for (const g of x.ngrams) { let a = idxN.get(g); if (!a) idxN.set(g, (a = [])); a.push(i); }
  for (const g of x.shingles) { let a = idxS.get(g); if (!a) idxS.set(g, (a = [])); a.push(i); }
});

// Longest run of tokens the two texts share (longest common substring), with its text.
function longestRun(a, b) {
  let best = 0, end = 0, prev = new Array(b.length + 1).fill(0);
  for (let i = 1; i <= a.length; i++) {
    const cur = new Array(b.length + 1).fill(0);
    for (let j = 1; j <= b.length; j++) if (a[i - 1] === b[j - 1]) { cur[j] = prev[j - 1] + 1; if (cur[j] > best) { best = cur[j]; end = i; } }
    prev = cur;
  }
  return { len: best, text: a.slice(end - best, end).slice(0, 30).join(' ') };
}

function scan(rel, targetUnits, selfId) {
  const hits = [];
  for (const t of targetUnits) {
    const ng = keepN(t.tk), sh = keepS(t.tk);
    const common = new Map();
    for (const g of sh) for (const i of idxS.get(g) ?? []) common.set(i, (common.get(i) ?? 0) + 1);
    const cand = new Set(common.keys());
    const gramHit = new Map();
    for (const g of ng) for (const i of idxN.get(g) ?? []) { cand.add(i); if (!gramHit.has(i)) gramHit.set(i, g); }
    for (const i of cand) {
      const s = corpus[i];
      if (s.file === rel || (selfId && s.id === selfId && s.file.startsWith('exams/') && rel.startsWith('exams/'))) continue;
      const inter = common.get(i) ?? 0;
      const score = +(inter / (sh.size + s.shingles.size - inter || 1)).toFixed(2);
      const big = Math.min(sh.size, s.shingles.size) >= MIN_SHINGLES;
      if (gramHit.has(i)) {
        const r = longestRun(t.tk, s.tk), share = +(r.len / t.tk.length).toFixed(2);
        if (r.len >= MIN_RUN && share >= MIN_SHARE) hits.push({ target: `${rel}:${t.path}`, source: `${s.file}:${s.path}`, kind: 'ngram', ngram: r.text, run: r.len, share, score });
      }
      else if (big && score >= THRESH) hits.push({ target: `${rel}:${t.path}`, source: `${s.file}:${s.path}`, kind: 'jaccard', score });
    }
  }
  return hits;
}

// Targets.
const targets = [];
const direct = opt('--file', null);
if (direct) {
  const rel = `${opt('--as', 'exams')}/${direct.split('/').pop()}`;
  const r = unitsOf(direct, rel);
  targets.push({ rel, units: r.units, id: r.id });
} else if (has('--all-exams')) {
  for (const f of jsonFiles(join(C, 'exams'))) { const rel = `exams/${f}`; targets.push({ rel, units: unitsOf(join(C, rel), rel).units, id: fileIds[rel] }); }
} else {
  let rel = null;
  if (opt('--exam')) rel = `exams/${opt('--exam')}.json`;
  else if (opt('--drill')) rel = `drills/${opt('--drill')}.json`;
  else if (opt('--bank')) rel = `bank/${opt('--bank').replace(/^.*\//, '').replace(/\.json$/, '')}.json`;
  if (!rel || !existsSync(join(C, rel))) {
    console.error('usage: fresh-check.mjs --exam <id> | --drill <id> | --bank <file> | --all-exams [--threshold n] [--min-run n] [--min-share x] [--json]');
    process.exit(2);
  }
  targets.push({ rel, units: unitsOf(join(C, rel), rel).units, id: fileIds[rel] });
}
// One line per target item and source file: the best hit (an n-gram hit beats a score, then the higher score).
const best = new Map();
for (const t of targets) for (const h of scan(t.rel, t.units, t.id)) {
  const k = `${h.target}|${h.source.split(':')[0]}`, o = best.get(k);
  if (!o || (h.kind === 'ngram' && o.kind !== 'ngram') || (h.kind === o.kind && (h.run ?? 0) > (o.run ?? 0)) || (h.kind === o.kind && h.run === o.run && h.score > o.score)) best.set(k, h);
}
const all = [...best.values()];
if (has('--json')) console.log(JSON.stringify(all, null, 1));
else {
  for (const h of all) console.log(`${h.target}  <-  ${h.source}  ${h.kind === 'ngram' ? `ngram "${h.ngram}" run ${h.run}, share ${h.share}, jaccard ${h.score}` : `jaccard ${h.score}`}`);
  console.log(`${all.length} hit(s) in ${targets.length} target file(s)`);
}
process.exitCode = all.length ? 1 : 0;   // not process.exit: piped output must flush
