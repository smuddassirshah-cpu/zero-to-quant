#!/usr/bin/env node
// Freshness check (ENGINE-BACKLOG 588). Flags items whose prose, question or widget prompt text
// copies a lesson screen, quiz, review, homework or other exam item, even with changed numbers.
// Problem sets (893): --file courses/<c>/problems-<n>.json also lists, as advisory, a shared displayed formula or two shared parameters with its course (--shared-params n, --no-set-reuse).
// Same-course reuse (972): for problems-<n>.json (any course file with --same-course, off with --no-same-course) each item is also held against every other file of its course: numbers, matrices up to a scalar and a transpose, shared sentences
//   ([same-course-reuse] lines; an error fails the run, a warning does not; waivers in tools/same-course-waivers.json). Thresholds are those of tools/same-course-reuse.mjs, which also runs on its own (--all).
// Usage (from app/): node tools/fresh-check.mjs --exam <id> | --drill <id> | --bank <file> | --all-exams
//                    [--threshold n] [--min-run n] [--min-share x] [--ngram n] [--no-code] [--json] [--content <dir>] [--file <json> [--as exams]]
//   --file content/courses/<c>/review-1.json (or homework-2.json) checks a course set against everything else, code items included, and
//   lists as advisory (exit 0) any item sharing three or more non-trivial numbers with one lesson screen of its course (--shared-numbers n, 0 off).
// Cross-content numbers (protocol 6, review-delta-bank-2 findings 1 to 4): --cross-numbers [n] lists, as advisory, any target item sharing n or more (default 3) distinctive numbers
//   with an item of any other file (course screens, quizzes, sets, exams, the bank), and --cross-numbers-all does it for every item of the content (each pair once). The numbers are those the
//   item states (its prose, question, options, explanation and right-answer line) and its numeric keys and slip values; standard constants (0.05, 1.96, ...) and any number that more than 1000 items hold are left out; a pair needs n shared numbers of which at least two are held by 300 items or fewer (--cross-df, --cross-weak). A lesson screen or quiz item against another lesson's is not listed; --cross-numbers-all lists the pairs, most shared numbers first.
// Exit 1 on any hit. A hit is a shared word n-gram (default 8 tokens, numbers normalised to "#")
// or a 5-word shingle Jaccard at or above the threshold (default 0.5).
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname, resolve, relative, isAbsolute, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadCorpus as loadSameCourse, scanSet as scanSameCourse, fmtHit as fmtSameCourse } from './same-course-reuse.mjs';

const argv = process.argv.slice(2);
const opt = (k, d) => { const i = argv.indexOf(k); return i >= 0 && argv[i + 1] !== undefined ? argv[i + 1] : d; };
const has = (k) => argv.includes(k);
const APP = join(dirname(fileURLToPath(import.meta.url)), '..');
const C = opt('--content', join(APP, 'content'));
// Gate defaults (AUTHORING section 11): a shared run of 12 word tokens that covers 60% of the item's words.
// Triage settings are --min-run 8 --min-share 0.
const MIN_RUN = Number(opt('--min-run', 12)), MIN_SHARE = Number(opt('--min-share', 0.6));
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
      // ENGINE-BACKLOG 927: a shuffled choice or multi shows its options in an order the learner never sees, so each option is read on its own: a break between them keeps
      // a run from joining the end of one option to the start of the next (the order they happen to have in the file)
      if (k === 'options' && Array.isArray(v) && node.shuffle !== false && (node.kind === 'choice' || node.kind === 'multi')) { for (const o of v) { collect(o, out, on); out.push(' | '); } continue; }
      collect(v, out, on || TEXT_KEYS.has(k));
    }
  }
}
// Standard AUTHORING instruction sentences. They are boilerplate by design, so they are cut out (and
// break a run) before tokens are compared. Add a pattern here only for a sentence AUTHORING prescribes.
const STOPLIST = [
  /put the (?:lines|steps|proof|derivation|argument|lines of the \w+) in order(?:, a reason in each line)?\.?/g,
  /(?:leave out|move|drop) the (?:\w+ )?(?:lines?|steps?|ones?) (?:that )?(?:do(?:es)? not belong|(?:is|are) flawed)\.?/g,
  /leave out the (?:\w+ )?(?:flawed lines?|that do not belong)\.?/g,
  /move (?:it|the (?:two )?flawed lines?) to left out\.?/g,
  /(?:one|two) lines? (?:does not belong|do not belong|is flawed|are flawed)[.:]?/g,
  /the two lines may come in either order\.?/g,
  /each line carries its reason\.?/g,
  /give a reason for every line\.?/g,
  /select all that apply:?\.?/g,
  /give (?:a |an )?(?:\w+ )?(?:decimal places?|fraction or a decimal)\.?/g,
  /say the (?:reasoning|argument) aloud (?:first|before you answer)\.?/g,
  /(?:complete|fill in) the (?:three )?(?:functions|answers|table)\.?/g,
  /which statements? (?:is|are) (?:right|true)\?/g,
  /what does (?:it|that) (?:print|return)\?/g,
];
// Lower-case; instruction sentences become a break "|"; every maths span, command and number becomes "#".
function tokens(strings) {
  let s = strings.join(' \n ').toLowerCase();
  s = s.replace(/```[a-z+]*/g, ' ');
  for (const re of STOPLIST) s = s.replace(re, ' | ');
  s = s.replace(/\$\$[\s\S]*?\$\$|\$[^$]*\$/g, ' # ');
  s = s.replace(/\\[a-z]+|\\[\\,;:!{}()[\]]/g, ' # ');
  s = s.replace(/\d+(?:[.,]\d+)*(?:e[+-]?\d+)?/g, ' # ');
  // Words, "#" placeholders and breaks; a run of placeholders collapses to one "#".
  return (s.match(/[a-z]+|#|\|/g) ?? []).filter((t, i, o) => !(t === '#' && o[i - 1] === '#') && !(t === '|' && o[i - 1] === '|'));
}
// A window of repeated symbols (x # y # x # y #) is not shared phrasing: it needs enough distinct tokens.
const STOP = new Set('what is the of and a an to in on for with that this which be are by it its at as from has have then give find how many much do does you your one two'.split(' '));
const informative = (g) => new Set(g.filter((t) => t !== '#' && !STOP.has(t))).size >= (g.length >= NGRAM ? MIN_WORDS_N : MIN_WORDS);
function grams(tk, n) { const o = []; for (let i = 0; i + n <= tk.length; i++) { const g = tk.slice(i, i + n); if (!g.includes('|')) o.push(g); } return o; }

// ENGINE-BACKLOG 614: the non-trivial numbers a unit states (a decimal, or an integer over 20 that is not a round stock number), so a set item
// that reuses a lesson's seed with every sentence reworded still shows. Compared for course sets against lessons of the same course.
const TRIVIAL = new Set([25, 30, 40, 50, 60, 75, 100, 200, 250, 500, 1000, 10000, 365, 252, 12, 24]);
function numbersOf(strings) {
  const s = strings.join(' ').replace(/(?<=\d)(?:,|\{,\})(?=\d{3}(?!\d))/g, '').replace(/```[\s\S]*?```/g, ' ');
  const out = new Set();
  for (const m of s.matchAll(/(?<![\w.])\d+(?:\.\d+)?(?![\w])/g)) { const v = Number(m[0]); if (m[0].includes('.') ? true : (v > 20 && !TRIVIAL.has(v))) out.add(String(v)); }
  return out;
}
const SHARED_NUMS = Number(opt('--shared-numbers', 3));
// Cross-content numbers: the stated numbers plus the numeric answers, slip values and option figures of a unit, minus standard constants.
const CONSTS = new Set(['0.5', '0.25', '0.75', '0.1', '0.05', '0.01', '0.001', '0.025', '0.975', '0.95', '0.99', '0.9', '1.5', '1.96', '1.645', '2.576', '2.33', '3.14', '3.1416', '2.718', '1.414', '0.693', '0.6931', '0.0001', '0.005', '0.0005']);
function keyNumbers(node, out = []) {
  if (Array.isArray(node)) { for (const v of node) keyNumbers(v, out); return out; }
  if (node && typeof node === 'object') {
    for (const [k, v] of Object.entries(node)) {
      if (k === 'answer' && typeof v === 'number') out.push(String(+v.toPrecision(10)));
      else if (k === 'answers' && Array.isArray(v)) v.forEach((x) => typeof x === 'number' && out.push(String(+x.toPrecision(10))));
      else if (k === 'wrong' && Array.isArray(v)) v.forEach((w) => w && typeof w.value === 'number' && out.push(String(+w.value.toPrecision(10))));
      else if (k === 'options' && Array.isArray(v)) v.forEach((o) => typeof o === 'string' && out.push(o));
      else if (k === 'explain' && v && typeof v.text === 'string') out.push(v.text);
      else if (k === 'feedback' && v && typeof v.correct === 'string') out.push(v.correct);
      else if (!['feedback', 'explain', 'hints', 'hint', 'why', 'solution', 'starter', 'tests', 'rubric', 'model'].includes(k)) keyNumbers(v, out);
    }
  }
  return out;
}
// ENGINE-BACKLOG 893: the displayed formulas of a unit (its $..$ and $$..$$ spans, and each side of an = or \approx in them), with spaces, \left \right,
// \, and \tfrac dropped, kept when they hold three or more tokens. A problem-set item that shares one with a lesson, quiz, review, homework, exam or
// other set of its course, or two or more of its stated parameters (--shared-params, default 2), is reported as advisory.
function formulasOf(strings) {
  const out = new Set();
  const norm = (x) => x.replace(/\\(?:left|right)(?![a-z])/g, '').replace(/\\[,;:! ]|~|\s+/g, '').replace(/\\[dt]frac/g, '\\frac').replace(/\\operatorname\{([a-z]+)\}|\\mathrm\{([a-z]+)\}/g, '$1$2');
  for (const m of strings.join(' \n ').matchAll(/\$\$([^$]+)\$\$|\$([^$]+)\$/g)) {
    const whole = norm(m[1] ?? m[2]);
    for (const f of new Set([whole, ...whole.split(/=|\\approx|\\le(?![a-z])|\\ge(?![a-z])|<|>/)])) {
      const tk = f.match(/\\[a-zA-Z]+|[A-Za-z]|\d+(?:\.\d+)?|[^\s]/g) ?? [];
      const sig = tk.filter((t) => !/^[(){}[\],.]$/.test(t));
      // a formula that states something specific: six or more tokens, a letter, an operator and a number (a bare identity such as \frac{c_{n+1}}{c_n} is a taught idea, not a setting)
      if (sig.length >= 6 && /[A-Za-z]/.test(f) && /\d/.test(f) && /[-+^*/=]|\\(?:frac|sqrt|ln|sin|cos|tan|exp|int|sum|binom|cdot|times)/.test(f) && (f.split(/[(){}]/).length - 1) % 1 === 0 && (f.match(/\(/g) ?? []).length === (f.match(/\)/g) ?? []).length) out.add(f);
    }
  }
  return out;
}
const sigLen = (f) => (f.match(/\\[a-zA-Z]+|[A-Za-z]|\d+(?:\.\d+)?|[^\s]/g) ?? []).filter((t) => !/^[(){}[\],.]$/.test(t)).length;
const SHARED_PARAMS = Number(opt('--shared-params', 2)), BOILER_F = Number(opt('--boiler-formula', 3));
// Units: one lesson screen / quiz item / review item / homework item / exam item / drill / bank item.
function unitsOf(file, rel) {
  const d = rd(file), u = [];
  const qOf = (node) => (node && typeof node === 'object' ? [node.prose, node.question, ...(Array.isArray(node.parts) ? node.parts.flatMap((p) => [p && p.prose, p && p.question]) : [])].filter((x) => typeof x === 'string') : []);
  const add = (path, node) => { const out = []; collect(node, out, false); const tk = tokens(out); if (tk.length) u.push({ file: rel, path, tk, qtk: tokens(qOf(node)), nums: numbersOf(out), xn: [...numbersOf([...out, ...keyNumbers(node)])].filter((n) => !CONSTS.has(n)), forms: formulasOf(out) }); };
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
  return { id: d.versionOf || d.id, units: u };   // a mock version (versionOf) shares its family id: versions repeat each other on purpose
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

// Longest run the two texts share (longest common substring), scored in word tokens only: "#" placeholders
// join a run but do not count, and a "|" break never matches.
function longestRun(a, b) {
  let best = 0, end = 0, endLen = 0, prev = new Array(b.length + 1).fill(0), prevL = new Array(b.length + 1).fill(0);
  for (let i = 1; i <= a.length; i++) {
    const cur = new Array(b.length + 1).fill(0), curL = new Array(b.length + 1).fill(0);
    for (let j = 1; j <= b.length; j++) if (a[i - 1] === b[j - 1] && a[i - 1] !== '|') {
      cur[j] = prev[j - 1] + (a[i - 1] === '#' ? 0 : 1); curL[j] = prevL[j - 1] + 1;
      if (cur[j] > best) { best = cur[j]; end = i; endLen = curL[j]; }
    }
    prev = cur; prevL = curL;
  }
  return { len: best, text: a.slice(end - endLen, end).slice(0, 30).join(' ') };
}
const words = (tk) => tk.filter((t) => t !== '#' && t !== '|').length;

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
        const r = longestRun(t.tk, s.tk), share = +(r.len / (words(t.tk) || 1)).toFixed(2);
        if (r.len >= MIN_RUN && share >= MIN_SHARE) hits.push({ target: `${rel}:${t.path}`, source: `${s.file}:${s.path}`, kind: 'ngram', ngram: r.text, run: r.len, share, score });
      }
      else if (big && score >= THRESH) hits.push({ target: `${rel}:${t.path}`, source: `${s.file}:${s.path}`, kind: 'jaccard', score });
    }
  }
  return hits;
}

// ENGINE-BACKLOG 929: for a bank, exam or drill target, a run of QRUN or more words in the stem (`prose` and `question`; options, feedback and code are left out) shared with another unit, whatever its share of the item, as an advisory
// (a reused setup with new numbers and a fresh paragraph around it passes the share gate). Stock phrases are dropped by the same document-frequency filter as the n-grams.
const QRUN = Number(opt('--question-run', 8));
function scanQuestionRuns(rel, targetUnits, selfId) {
  if (!/^(bank|exams|drills)\//.test(rel) || has('--no-question-run') || QRUN < 1) return [];
  const hits = [];
  for (const t of targetUnits) {
    if (!t.qtk || words(t.qtk) < QRUN) continue;
    const cand = new Set();
    for (const g of grams(t.qtk, Math.min(NGRAM, QRUN)).filter(informative).map((x) => x.join(' '))) for (const i of idxN.get(g) ?? []) cand.add(i);
    for (const g of grams(t.qtk, NGRAM)) for (const i of idxN.get(g.join(' ')) ?? []) cand.add(i);
    for (const i of cand) {
      const s = corpus[i];
      if (!s.qtk || s.file === rel || (selfId && s.id === selfId && s.file.startsWith('exams/') && rel.startsWith('exams/'))) continue;
      const r = longestRun(t.qtk, s.qtk);
      if (r.len >= QRUN && (dfN.get(r.text.split(' ').slice(0, NGRAM).join(' ')) ?? 0) <= BOILER) hits.push({ target: `${rel}:${t.path}`, source: `${s.file}:${s.path}`, kind: 'question-run', ngram: r.text, run: r.len, share: +(r.len / (words(t.tk) || 1)).toFixed(2), score: 0 });
    }
  }
  return hits;
}
// Shared numbers (614): a course set item with three or more non-trivial numbers in common with one lesson screen of the same course.
function scanNumbers(rel, targetUnits) {
  const m = rel.match(/^courses\/([^/]+)\/(?:review|homework)/);
  if (!m || SHARED_NUMS < 1) return [];
  const hits = [];
  for (const t of targetUnits) {
    if (!t.nums || t.nums.size < SHARED_NUMS) continue;
    for (const c of corpus) {
      if (!c.nums || !c.file.startsWith(`courses/${m[1]}/l`)) continue;
      const shared = [...t.nums].filter((n) => c.nums.has(n));
      if (shared.length >= SHARED_NUMS) hits.push({ target: `${rel}:${t.path}`, source: `${c.file}:${c.path}`, kind: 'numbers', ngram: shared.slice(0, 6).join(' '), count: shared.length, score: 0 });
    }
  }
  return hits;
}
// Set reuse (893): a problem-set item against the lessons, quizzes, reviews, homework and other sets of its course, and every exam.
const dfForm = new Map();
for (const x of corpus) for (const f of x.forms ?? []) dfForm.set(f, (dfForm.get(f) ?? 0) + 1);
function scanSetReuse(rel, targetUnits) {
  const m = rel.match(/^courses\/([^/]+)\/problems-\d+\.json$/);
  if (!m || has('--no-set-reuse')) return [];
  const hits = [];
  for (const t of targetUnits) {
    const mine = [...t.forms].filter((f) => (dfForm.get(f) ?? 0) <= BOILER_F);
    for (const c of corpus) {
      const exam = c.file.startsWith('exams/');
      if (c.file === rel || !(c.file.startsWith(`courses/${m[1]}/`) || exam)) continue;
      // the same formula, or one that sits inside a longer one of the source (P(t)=40e^{0.06t} inside P(t)=40e^{0.06t}(1+0.02t)); an exam is not tied to a course, so it needs a longer formula and three parameters
      const fs = mine.filter((f) => (!exam || sigLen(f) >= 8) && (c.forms.has(f) || [...c.forms].some((g) => g.length > f.length && g.includes(f))));
      if (fs.length) { hits.push({ target: `${rel}:${t.path}`, source: `${c.file}:${c.path}`, kind: 'formula', ngram: fs.slice(0, 3).join('  '), count: fs.length, score: 0 }); continue; }
      // a stated parameter is a specific number: a whole number over 20, a decimal with two places or more, or three or more significant digits (0.3 and 1.5 are everywhere)
      const shared = [...t.nums].filter((n) => c.nums.has(n) && (n.replace('.', '').replace(/^0+/, '').length >= 3 || /\.\d\d/.test(n) || (!n.includes('.') && +n > 20)));
      if (SHARED_PARAMS >= 1 && shared.length >= SHARED_PARAMS + (exam ? 1 : 0)) hits.push({ target: `${rel}:${t.path}`, source: `${c.file}:${c.path}`, kind: 'params', ngram: shared.slice(0, 6).join(' '), count: shared.length, score: 0 });
    }
  }
  return hits;
}
// Code names (ENGINE-BACKLOG 600): function and class names of code widgets in a target (exam, drill or bank
// item) against every code widget of every lesson, review and homework. A task renamed in prose but with the
// same function (`walk_forward_mse`, `irls_logistic`, `metropolis`) is a reuse the prose scan cannot see.
const GENERIC = new Set(('main solve helper run test check demo example answer result compute calculate fit predict transform ' +
  'mean std var variance median total count update reset push pop peek size empty get set add remove insert erase find ' +
  'init step simulate price payoff value evaluate score loss gradient hessian apply process parse read write load dump ' +
  'len sum min max abs round sorted range print format str int float list dict tuple zip map filter any all enumerate ' +
  'sqrt exp log norm array zeros ones arange linspace dot where cumsum diff append extend isclose allclose assert ' +
  'swap merge sort search partition build reverse flatten uniform normal random seed').split(' '));
const nameOk = (n) => !n.startsWith('_') && !n.startsWith('test_') && !GENERIC.has(n) && (n.length >= 6 || n.includes('_')) && /^[A-Za-z]\w*$/.test(n);
function namesOf(w) {
  const out = new Set(), src = [w.starter, w.solution].filter((x) => typeof x === 'string');
  const defs = [/^[ \t]*(?:async\s+)?def\s+([A-Za-z]\w*)/gm, /^[ \t]*class\s+([A-Za-z]\w*)/gm, /^[ \t]*(?:class|struct)\s+([A-Za-z]\w*)/gm,
    /^[ \t]*(?:template\s*<[^>]*>\s*)?(?:(?:static|inline|constexpr|const|unsigned|long|short)\s+)*[A-Za-z_][\w:<>,*&]*[\s*&]+([A-Za-z]\w*)\s*\([^;{}()]*\)\s*(?:const\s*)?\{/gm];
  for (const code of src) for (const re of defs) for (const m of code.matchAll(re)) if (m[1] !== 'main') out.add(m[1]);
  if (typeof w.fn === 'string') out.add(w.fn);
  for (const t of [...(w.tests ?? []), ...(w.examples ?? [])]) { const m = typeof t?.call === 'string' && t.call.match(/^\s*([A-Za-z]\w*)\s*\(/); if (m) out.add(m[1]); }
  return [...out].filter(nameOk);
}
function codeWidgets(node, path, out) {
  if (Array.isArray(node)) node.forEach((v, i) => codeWidgets(v, `${path}[${i}]`, out));
  else if (node && typeof node === 'object') {
    if (typeof node.starter === 'string' || typeof node.solution === 'string') { const n = namesOf(node); if (n.length) out.push({ path, names: n }); }
    for (const [k, v] of Object.entries(node)) if (v && typeof v === 'object') codeWidgets(v, path ? `${path}.${k}` : k, out);
  }
}
const nameIdx = new Map();
if (!has('--no-code')) {
  for (const rel of listAll()) {
    if (!rel.startsWith('courses/') && !rel.startsWith('drills/')) continue;   // ENGINE-BACKLOG 920: drill code names too (a bank code item is held against drills as well as lessons)
    const ws = []; codeWidgets(rd(join(C, rel)), '', ws);
    for (const w of ws) for (const n of w.names) { let a = nameIdx.get(n); if (!a) nameIdx.set(n, (a = [])); a.push(`${rel}:${w.path}`); }
  }
}
// A name used in IDIOM or more courses is a shared helper idiom (daily_returns, run_tests), not a reused task.
const IDIOM = Number(opt('--idiom', 3));
function scanCode(rel, abs = join(C, rel)) {
  const ws = []; codeWidgets(rd(abs), '', ws);
  const hits = [];
  for (const w of ws) for (const n of new Set(w.names)) {
    const srcs = (nameIdx.get(n) ?? []).filter((x) => !x.startsWith(rel + ':') && (x.startsWith('courses/') || rel.startsWith('bank/')));   // drill names count against bank items only
    if (!srcs.length || new Set(srcs.map((x) => (x.startsWith('drills/') ? 'drills' : x.split('/')[1]))).size >= IDIOM) continue;
    hits.push({ target: `${rel}:${w.path}`, source: srcs[0] + (srcs.length > 1 ? ` (+${srcs.length - 1} more)` : ''), kind: 'code-name', names: [n], ngram: n, score: 0 });
  }
  return hits;
}

// Cross-content numbers (see the header): an inverted index from number to units, so a number held by many units (a stock figure) is dropped.
const CROSS = has('--cross-numbers') || has('--cross-numbers-all');
const CROSS_N = Number(opt('--cross-numbers', 3)) || 3, CROSS_DF = Number(opt('--cross-df', 300)), CROSS_WEAK = Number(opt('--cross-weak', 1000));
const xIdx = new Map();
if (CROSS) corpus.forEach((x, i) => { for (const n of x.xn ?? []) { let a = xIdx.get(n); if (!a) xIdx.set(n, (a = [])); a.push(i); } });
function scanCross(rel, targetUnits, selfId) {
  if (!CROSS) return [];
  const hits = [];
  for (const t of targetUnits) {
    const cnt = new Map();
    for (const n of t.xn ?? []) { const a = xIdx.get(n) ?? []; if (a.length > CROSS_WEAK) continue; for (const i of a) { const s = corpus[i]; if (s.file === rel && s.path === t.path) continue; const c = cnt.get(i) ?? cnt.set(i, { all: [], strong: 0 }).get(i); c.all.push(n); if (a.length <= CROSS_DF) c.strong++; } }
    for (const [i, c] of cnt) {
      const s = corpus[i], shared = c.all;
      if (/^courses\/[^/]+\/l\d/.test(rel) && /^courses\/[^/]+\/l\d/.test(s.file)) continue;   // two lessons teaching their own worked numbers
      if (shared.length < CROSS_N || c.strong < 2 || s.file === rel || (selfId && s.id === selfId && s.file.startsWith('exams/') && rel.startsWith('exams/'))) continue;
      if (has('--cross-numbers-all') && `${rel}:${t.path}` > `${s.file}:${s.path}`) continue;   // each pair once
      hits.push({ target: `${rel}:${t.path}`, source: `${s.file}:${s.path}`, kind: 'cross-numbers', ngram: shared.slice(0, 6).join(' '), count: shared.length, score: 0 });
    }
  }
  return hits;
}

// Targets.
const targets = [];
const direct = opt('--file', null);
if (direct) {
  // A file inside the content folder keeps its own path (courses/<c>/review-1.json), so the scan skips it
  // as a source and reads its code from where it lives. Outside it, --as names the kind (exams, drills, bank).
  const abs = resolve(direct), inC = relative(resolve(C), abs);
  const rel = !inC.startsWith('..') && !isAbsolute(inC) ? inC.split(sep).join('/') : `${opt('--as', 'exams')}/${direct.split('/').pop()}`;
  const r = unitsOf(abs, rel);
  targets.push({ rel, units: r.units, id: r.id, abs });
} else if (has('--cross-numbers-all')) {
  for (const rel of listAll()) targets.push({ rel, units: unitsOf(join(C, rel), rel).units, id: fileIds[rel] });
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
for (const t of targets) for (const h of has('--cross-numbers-all') ? scanCross(t.rel, t.units, t.id) : [...scan(t.rel, t.units, t.id), ...scanNumbers(t.rel, t.units), ...scanQuestionRuns(t.rel, t.units, t.id), ...scanCross(t.rel, t.units, t.id), ...scanSetReuse(t.rel, t.units), ...(has('--no-code') ? [] : scanCode(t.rel, t.abs))]) {
  const k = `${h.target}|${h.kind === 'code-name' ? 'name:' + h.ngram : h.source.split(':')[0]}`, o = best.get(k);
  const RANK = { 'code-name': 4, ngram: 3, jaccard: 2, formula: 1.6, params: 1.5, 'question-run': 1.2, numbers: 1, 'cross-numbers': 0.9 };
  if (!o || RANK[h.kind] > RANK[o.kind] || (h.kind === o.kind && ((h.count ?? 0) > (o.count ?? 0) || (h.run ?? 0) > (o.run ?? 0) || ((h.run ?? 0) === (o.run ?? 0) && h.score > o.score)))) best.set(k, h);
}
const all = [...best.values()];
if (CROSS) all.sort((x, y) => (y.kind === 'cross-numbers') - (x.kind === 'cross-numbers') || (y.kind === 'cross-numbers' ? y.count - x.count : 0));
const ADVISORY = new Set(['numbers', 'formula', 'params', 'question-run', 'cross-numbers']);   // shared numbers, a shared formula and shared parameters are advisory: a table of critical values is shared on purpose
// Same-course reuse (972): a problem set by default, any other course file with --same-course.
const sameLines = [];
let sameErrors = 0;
if (!has('--no-same-course') && !CROSS) {
  const sc = targets.filter((t) => (has('--same-course') ? /^courses\/[^/]+\/[^/]+\.json$/ : /^courses\/[^/]+\/problems-\d+\.json$/).test(t.rel));
  if (sc.length) {
    const corpus = loadSameCourse(C);
    for (const t of sc) { const doc = rd(join(C, t.rel)); for (const h of scanSameCourse(corpus, t.rel, doc)) { sameLines.push(fmtSameCourse(h, doc)); if (h.level === 'error' && !h.waived) sameErrors++; } }
  }
}
const hard = all.filter((h) => !ADVISORY.has(h.kind));
if (has('--json')) console.log(JSON.stringify([...all, ...sameLines.map((l) => ({ kind: 'same-course-reuse', line: l }))], null, 1));
else {
  for (const l of sameLines) console.log(l);
  for (const h of all) console.log(`${h.target}  <-  ${h.source}  ${h.kind === 'code-name' ? `code names ${h.ngram}` : h.kind === 'numbers' || h.kind === 'cross-numbers' ? `${h.count} shared numbers (${h.ngram})` : h.kind === 'formula' ? `shared formula ${h.ngram}` : h.kind === 'params' ? `${h.count} shared parameters (${h.ngram})` : h.kind === 'question-run' ? `stem shares ${h.run} words ("${h.ngram}"), share ${h.share}` : h.kind === 'ngram' ? `ngram "${h.ngram}" run ${h.run}, share ${h.share}, jaccard ${h.score}` : `jaccard ${h.score}`}`);
  console.log(`${hard.length} hit(s) in ${targets.length} target file(s)${all.length > hard.length ? `, ${all.length - hard.length} advisory (shared numbers, formulas, parameters and stem runs: read them, they may be a shared table of constants or a stock phrase)` : ''}`);
}
process.exitCode = hard.length || sameErrors ? 1 : 0;   // not process.exit: piped output must flush
