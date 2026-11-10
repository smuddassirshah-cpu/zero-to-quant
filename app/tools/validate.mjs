#!/usr/bin/env node
/* Content validator for Zero to Quant (docs/AUTHORING.md section 7, docs/PLAN.md section 11). Node, no dependencies.

   node tools/validate.mjs              validate everything under content/, print one line per problem, exit 1 on any error
   node tools/validate.mjs --summary    also print lesson counts per course and every mapped lesson not yet written
   node tools/validate.mjs --no-manifest   do not rewrite content/manifest.json
   node tools/validate.mjs --prep <file>   check <file> instead of content/prep.json (and leave the manifest alone)

   It loads curriculum.json, every course.json, every lesson, level review, homework, exam and drill file, and checks
   the schema and the semantic rules. Missing lesson, review and homework files are warnings (they show as "Not yet
   written" in the app). When there are no errors it refreshes content/manifest.json, the list of authored files that
   js/content.js reads so the app never requests a file that is not there. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import { scanO2, O2_CODES, orderedOptionsWhy } from './o2-rules.mjs';
import { checkCapstones } from './capstone-rules.mjs';
import { statedMinutes, ignoreList as durationIgnore, FLOOR as DURATION_FLOOR } from './duration-prose.mjs';
import { checkTask, howOf as perfHow, checkLevel as perfCheckLevel, matchVerb, optionalRows } from './perf-rules.mjs';
import { checkSet as checkFluencySet, fixtureFiles as fluencyFixtures } from './fluency-rules.mjs';   // generated fluency sets (ENGINE-BACKLOG 812 to 816)
const hoursLib = createRequire(import.meta.url)('../js/hours.js');   // SESSION_RANGE: the minutes each lesson session accepts (item 10)
const cmap = createRequire(import.meta.url)('../js/engine/canvas/complex-map.js'); // { compile }: formula check for complex-map (item 432)
const tradeSim = createRequire(import.meta.url)('../js/engine/widgets/trade.js'); // { norm, play, ... }: the trade widget's game, so the authored strategy is played against the benchmark (item 459)
const interleaveEngine = createRequire(import.meta.url)('../js/engine/canvas/interleave.js'); // { check, idsOf, ... }: the interleave canvas's spec rules, schedule replay and enumeration limit (item 471)

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');
const CONTENT = path.join(APP, 'content');
const args = new Set(process.argv.slice(2));
const SUMMARY = args.has('--summary');
const prepArg = process.argv.indexOf('--prep');
const PREP_FILE = prepArg > 0 && process.argv[prepArg + 1] ? path.resolve(process.argv[prepArg + 1]) : null; // a scratch copy of prep.json to check instead
const STRICT_WHY = !args.has('--lax-why');   // a cross-course requires entry without a why is an error (ENGINE-BACKLOG 551; strict since 2c item 7 content, 5 Nov); --lax-why makes it a warning
const WRITE_MANIFEST = !args.has('--no-manifest') && !PREP_FILE;

/* ---------- Reporting ---------- */
const problems = [];
const rel = (f) => path.relative(APP, f) || f;
const err = (file, where, msg) => problems.push({ level: 'error', file: rel(file), where, msg });
const warn = (file, where, msg) => problems.push({ level: 'warning', file: rel(file), where, msg });

/* ---------- Vocabulary ---------- */
const KEBAB = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const WIDGETS = new Set(['choice', 'multi', 'numeric', 'expression', 'slider', 'sliders', 'drag-point', 'place', 'tap-regions', 'order', 'table', 'manipulate', 'balance', 'sketch', 'code', 'longform', 'trade']);
const CANVASES = new Set(['pair', 'grid', 'tree', 'venn', 'number-line', 'boxes', 'area', 'balance', 'circle', 'plane', 'bars', 'distribution', 'scatter', 'series', 'walk', 'matrix', 'vectors', 'complex-map', 'graph', 'array', 'payoff', 'orderbook', 'table', 'console', 'space', 'interleave']);
const SCREEN_TYPES = new Set(['title', 'explore', 'problem', 'ladder', 'demonstrate', 'trap', 'generalise', 'derive', 'transfer']);
const GRADED = new Set(['problem', 'ladder', 'trap', 'transfer', 'derive']);
const CANVAS_BOUND = new Set(['tap-regions', 'drag-point', 'sketch', 'balance', 'slider', 'sliders']);
const RUNGS = ['nudge', 'point', 'step'];
const TRACKS = ['maths', 'prob', 'code', 'fin', 'ml', 'speed'];
const AMERICAN = [
  [/\bcolor(s|ed|ing|ful)?\b/i, 'colour'], [/\bcenter(s|ed|ing)?\b/i, 'centre'], [/\bfavorite/i, 'favourite'], [/\banalyz/i, 'analyse'],
  [/\boptimiz/i, 'optimise'], [/\bbehavior/i, 'behaviour'], [/\bmodeling\b/i, 'modelling'], [/\bmodeled\b/i, 'modelled'], [/\blabeled\b/i, 'labelled'],
  [/\bmath class\b/i, 'maths class'], [/\bmath\b/, 'maths'], [/\bnormaliz/i, 'normalise'], [/\bstandardiz/i, 'standardise'], [/\bminimiz/i, 'minimise'],
  [/\bmaximiz/i, 'maximise'], [/\brecogniz/i, 'recognise'], [/\brealiz/i, 'realise'], [/\bsummariz/i, 'summarise'], [/\borganiz/i, 'organise'],
  [/\bparameteriz/i, 'parametrise'], [/\bgray\b/i, 'grey'], [/\bfiber\b/i, 'fibre'], [/\bdefense\b/i, 'defence'], [/\bcatalog\b/i, 'catalogue'],
  [/\btraveled\b/i, 'travelled'], [/\bcanceled\b/i, 'cancelled'], [/\bliter\b/i, 'litre'], [/\bmeters?\b/i, 'metre'], [/\bjewelry\b/i, 'jewellery'],
  [/\bcheck(s)? (?=out of)/i, 'cheque'], [/\bsquare off\b/i, null],
].filter(([, b]) => b);
const EMOJI_RAW = /\p{Extended_Pictographic}/u;
/* items 271, 274: plain geometric symbols and card suits used as tokens (stars and bars, a hand of cards) are text,
   unless written with the emoji presentation selector U+FE0F */
const TOKEN_SYMBOLS = /[★☆●○■□▲△▼◀▶◆♠♥♦♣♤♡♢♧](?!\uFE0F)/gu;
const EMOJI = { test: (s) => EMOJI_RAW.test(String(s).replace(TOKEN_SYMBOLS, '')) };

/* ---------- Text helpers ---------- */
const stripMathsAndCode = (s) => String(s).replace(/```[\s\S]*?```/g, ' ').replace(/`[^`]*`/g, ' ').replace(/\$\$[\s\S]*?\$\$/g, ' ').replace(/\$[^$]*\$/g, ' ');
const words = (s) => stripMathsAndCode(s).split(/\s+/).filter(w => /[A-Za-z0-9]/.test(w)).length;

/* Session V pass 7 (item 605): [shown-arithmetic]. A maths span that writes "number op number = number" (op x, /, +, -, ^, brackets, \frac) is
   recomputed. The stated result must be the left side at the result's own decimal places (for \approx, within one unit of its last digit).
   Three readers found sums and products worked on rounded inputs that print the unrounded result (coint 0.9956, opt-dash 3.05 against 3.07).
   Any letter, command or % in a segment skips it, so only pure arithmetic is judged; a miss over 2% is read as a deliberate wrong claim and skipped. Warning only. */
const arithTokens = (seg) => {
  let t = seg.replace(/\\left|\\right|\\,|\\;|\\!|\\ /g, ' ').replace(/\{,\}/g, '');
  t = t.replace(/\\times|\\cdot/g, '*').replace(/\\div/g, '/').replace(/[−–]/g, '-').replace(/×/g, '*');
  for (let k = 0; k < 4; k++) t = t.replace(/\\[dt]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g, '(($1)/($2))');
  t = t.replace(/\^\s*\{([^{}]*)\}/g, '^($1)').replace(/\{/g, '(').replace(/\}/g, ')');
  if (/[A-Za-z\\%£$&_]/.test(t)) return null;
  return t.replace(/\s+/g, '');
};
const arithEval = (t) => {
  let i = 0;
  const peek = () => t[i];
  const num = () => { const m = t.slice(i).match(/^\d+(?:\.\d+)?|^\.\d+/); if (!m) throw 0; i += m[0].length; return +m[0]; };
  const atom = () => {
    if (peek() === '(') { i++; const v = add(); if (peek() !== ')') throw 0; i++; return v; }
    if (peek() === '-') { i++; return -pow(); }
    return num();
  };
  const pow = () => { const b = atom(); if (peek() === '^') { i++; const e = peek() === '-' ? (i++, -atom()) : atom(); return Math.pow(b, e); } return b; };
  const mul = () => { let v = pow(); while (peek() === '*' || peek() === '/') { const o = t[i++]; const r = pow(); v = o === '*' ? v * r : v / r; } return v; };
  const add = () => { let v = mul(); while (peek() === '+' || peek() === '-') { const o = t[i++]; const r = mul(); v = o === '+' ? v + r : v - r; } return v; };
  const v = add();
  if (i !== t.length || !Number.isFinite(v)) throw 0;
  return v;
};
const shownArithmetic = (file, where, noCode) => {
  for (const m of noCode.match(/\$\$[\s\S]*?\$\$|\$[^$]*\$/g) || []) {
    const body = m.replace(/^\$+|\$+$/g, '');
    const parts = body.split(/(=|\\approx|\\simeq)/);
    for (let k = 0; k + 2 < parts.length; k += 2) {
      const lt = arithTokens(parts[k]), rt = arithTokens(parts[k + 2]), approx = parts[k + 1] !== '=';
      if (lt == null || rt == null || !/^-?\d+(?:\.\d+)?$/.test(rt) || !/\d[-+*/^]|\)[-+*/^(]|\)\(/.test(lt) || /^-?\d+(?:\.\d+)?$/.test(lt)) continue;
      let lv; try { lv = arithEval(lt); } catch { continue; }
      const dp = (rt.split('.')[1] || '').length, tz = !dp && approx ? (rt.match(/0+$/) || [''])[0].length : 0, unit = Math.pow(10, tz - dp), c = +rt;   // \approx 6{,}780 is three figures
      if (Math.abs(lv - c) > 0.02 * Math.max(Math.abs(c), unit)) continue;   // a wide miss is a deliberate wrong claim (a distractor, a slip shown), not rounding drift
      if (Math.abs(lv) >= 1e15 || Math.abs(lv - c) <= unit * (approx ? 1 : 0.5) + 1e-9 * Math.max(1, Math.abs(c))) continue;
      warn(file, where, `[shown-arithmetic] "${parts[k].trim()} ${approx ? '\\approx' : '='} ${parts[k + 2].trim()}": the left side works out to ${+lv.toPrecision(7)}, not ${rt}; recompute from the numbers as printed, or print the unrounded inputs`);
      return;
    }
  }
};
/* Session V: float artefacts (and, ENGINE-BACKLOG 611, a signed zero) in shown text */
const floatArtefacts = (file, where, noCode) => {
  const art = noCode.match(/(?<![\d.])\d*\.\d*(?:0{7,}|9{7,})\d{0,3}(?!\d)/);
  if (art) warn(file, where, `[float-artefact] "${art[0]}" is a floating-point artefact; round it to the digits that mean something`);
  /* ENGINE-BACKLOG 611: a signed zero ("-0.00", a rounded -0.0042) is a rounding artefact: write 0.00 */
  const sz = noCode.match(/(?<![\d.])[-\u2212]0\.0+(?!\d)/);
  if (sz) warn(file, where, `[float-artefact] "${sz[0]}" is a signed zero from rounding a small negative number; write ${sz[0].replace(/^[-\u2212]/, '')} (or say it is slightly negative)`);
};
/* Copy rules (rule 8) and KaTeX (rule 9) on one text field */
const checkText = (file, where, s, { copy = true } = {}) => {
  if (typeof s !== 'string') return;
  const outside = stripMathsAndCode(s);
  if (copy) {
    if (outside.includes('!')) err(file, where, 'no exclamation marks');
    if (EMOJI.test(outside)) err(file, where, 'no emoji');
    if (/it can be shown/i.test(outside)) err(file, where, 'no "it can be shown": derive it');
    for (const [re, uk] of AMERICAN) { const m = outside.match(re); if (m) err(file, where, `American spelling "${m[0]}": use "${uk}"`); }
  }
  if (s.includes('\u2014')) err(file, where, 'no em-dashes');
  const noCode = s.replace(/```[\s\S]*?```/g, '').replace(/`[^`]*`/g, '').replace(/\\\$/g, '');
  const dollars = (noCode.replace(/\$\$/g, '').match(/\$/g) || []).length;
  if ((noCode.match(/\$\$/g) || []).length % 2) err(file, where, 'unbalanced $$...$$');
  if (dollars % 2) err(file, where, 'unbalanced $...$');
  if (/[\b\f\v\r\t]/.test(s)) err(file, where, 'control character in text: a KaTeX backslash was not escaped in the JSON (write \\\\frac, not \\frac)');
  const maths = noCode.match(/\$[^$]*\$/g) || [];
  /* Session V: float artefacts in shown text, and a thousands comma inside maths (KaTeX spaces it as a list separator: write 10{,}000) */
  floatArtefacts(file, where, noCode);
  for (const m of noCode.match(/\$\$[\s\S]*?\$\$|\$[^$]*\$/g) || []) {
    const c = m.match(/(?<![\d.,{])(?<open>[(\[{]?)\d{1,3}(?:,\d{3})+(?![\d]|,\d)(?!\d)/g) || [];
    const bad = c.find(x => !/^[(\[{]/.test(x) || /,\d{3},\d{3}/.test(x));
    if (bad) { warn(file, where, `[math-thousands-comma] "${bad}" inside maths: KaTeX puts a space after the comma; write ${bad.replace(/,/g, '{,}')} (or no separator)`); break; }
  }
  shownArithmetic(file, where, noCode);
  if (maths.some(m => /\n[a-z]/.test(m))) err(file, where, 'newline inside maths: write \\\\neq, \\\\nu, \\\\nabla with a doubled backslash in JSON');
};

/* ---------- File loading ---------- */
/* A malformed file (a half-written one, or a field of the wrong type) is one error line, never a crash */
const guard = (file, fn) => { try { fn(); } catch (e) { err(file, '', `could not be checked (a field has the wrong shape): ${String(e.message || e).split('\n')[0]}`); } };
const readJSON = (file) => {
  let text;
  try { text = fs.readFileSync(file, 'utf8'); } catch { return { missing: true }; }
  try { return { data: JSON.parse(text) }; } catch (e) { err(file, '', `JSON does not parse: ${e.message}`); return { bad: true }; }
};
const listJSON = (dir) => { try { return fs.readdirSync(dir).filter(f => f.endsWith('.json')).sort(); } catch { return []; } };
const isObj = (x) => x && typeof x === 'object' && !Array.isArray(x);
/* item 304: the C++ code widget (docs/AUTHORING.md section 3, C++). Function mode: call (a C++ expression, or a
   function name with args as JSON values and optional types), expect as a JSON value. Script mode (a stdout case,
   stdin, argv, or a raises case without call): the program's own main runs once per case. */
const CPP_TYPES = ['int', 'long long', 'double', 'bool', 'std::string', 'std::vector<int>', 'std::vector<double>', 'std::vector<std::string>', 'std::vector<std::vector<double>>',
  'std::vector<long long>', 'std::vector<std::vector<int>>', 'std::vector<std::vector<long long>>']; // the last three: item 472 (nested integer vectors, long long)
/* engine pass (item 430): a std::complex result is expected as { re, im } (alone, or inside a list) */
const cppComplex = (v) => !!v && typeof v === 'object' && !Array.isArray(v) && Object.keys(v).length === 2 && Number.isFinite(v.re) && Number.isFinite(v.im);
const cppExpect = (v) => cppValue(v) || cppComplex(v) || (Array.isArray(v) && v.every(cppExpect));
const cppValue = (v) => (typeof v === 'number' && Number.isFinite(v)) || typeof v === 'boolean' || typeof v === 'string' || (Array.isArray(v) && v.every(cppValue));
const cppNumbers = (v) => (typeof v === 'number' && Number.isFinite(v)) || cppComplex(v) || (Array.isArray(v) && v.every(cppNumbers));
/* items 378, 425, 464: a case's tol is { rel, abs } (either or both, numbers 0 or more), for isclose */
/* item 581: a wrong[] value the grader can never return. grade.js within(): rel is |v-a| <= |a|*rel, abs is |v-a| <= abs; the answer is graded first, so a wrong value inside
   the answer's tolerance is graded correct. WRONG_FIRE_LEVEL is "error" unless existing content must be downgraded. */
const WRONG_FIRE_LEVEL = 'error'; // error since session T: the 14 hits in docs/reports/engine-pass-T.md are fixed
const halfWidth = (a, t) => { const o = typeof t === 'number' ? { abs: t } : (t || {}); return o.rel != null ? Math.abs(a) * o.rel + 1e-12 : (o.abs ?? 0) + 1e-9; };
const wrongCannotFire = (file, where, answer, tolA, wrong) => {
  if (typeof answer !== 'number' || !Number.isFinite(answer) || !Array.isArray(wrong)) return;
  const ha = halfWidth(answer, tolA), put = WRONG_FIRE_LEVEL === 'error' ? err : warn, seen = [];
  wrong.forEach((x, i) => {
    if (!x || typeof x.value !== 'number' || !Number.isFinite(x.value)) return;
    const hw = halfWidth(x.value, x.tol ?? { abs: 1e-9 }), d = Math.abs(x.value - answer);
    if (d <= ha) put(file, `${where}.wrong[${i}]`, `wrong value ${x.value} lies inside the answer ${answer} tolerance (+-${+ha.toPrecision(6)}), so it is graded correct and "${x.id}" can never fire`);
    else if (d <= ha + hw) put(file, `${where}.wrong[${i}]`, `wrong "${x.id}" (${x.value} +-${+hw.toPrecision(6)}) overlaps the answer ${answer} tolerance (+-${+ha.toPrecision(6)}); the overlap is graded correct`);
    seen.forEach(([j, y, hy]) => { if (Math.abs(x.value - y.value) <= hw + hy) warn(file, `${where}.wrong[${i}]`, `wrong "${x.id}" overlaps wrong[${j}] "${y.id}"; the earlier entry takes the key where they overlap`); });
    seen.push([i, x, hw]);
  });
};
/* Session V: [wrong-band] a numeric wrong value with more decimals than the rounding the question asks for, whose band is narrower than half a rounding step:
   a learner who follows the slip and rounds as asked misses it, so its byKey line never fires (12 lines in stage-3). */
const WORD_NUM = { zero: 0, one: 1, two: 2, three: 3, four: 4, five: 5, six: 6 };
const roundingAsked = (text) => {
  const t = stripMathsAndCode(text || '').toLowerCase();
  let m = t.match(/\b(zero|one|two|three|four|five|six|\d)\s*(?:decimal places?|decimal points?|d\.?\s?p\.?)/);
  if (m) return WORD_NUM[m[1]] ?? +m[1];
  if (/nearest (?:whole number|integer|pound|dollar|basis point|bp|unit|day|share)\b|whole number\b/.test(t)) return 0;
  if (/nearest (?:penny|pence|cent|0\.01)\b/.test(t)) return 2;
  if (/nearest 0\.1\b/.test(t)) return 1;
  return null;
};
const decimalsOf = (v) => { const m = String(v).match(/\.(\d+)(?:e([+-]?\d+))?$/i); return m ? Math.max(0, m[1].length - (m[2] ? +m[2] : 0)) : (/e-(\d+)/i.test(String(v)) ? +String(v).match(/e-(\d+)/i)[1] : 0); };
const wrongBandNarrow = (file, where, w, ctx) => {
  if (!Array.isArray(w.wrong)) return;
  const d = roundingAsked(ctx.question) ?? roundingAsked(ctx.prose);
  if (d == null) return;
  const scale = w.unit === '%' ? 100 : 1, half = 0.5 * Math.pow(10, -d) / scale;
  w.wrong.forEach((x, i) => {
    if (!isObj(x) || typeof x.value !== 'number' || !Number.isFinite(x.value)) return;
    if (decimalsOf(x.value) <= d + (scale === 100 ? 2 : 0)) return;
    const hw = halfWidth(x.value, x.tol ?? { abs: 1e-9 });
    /* ENGINE-BACKLOG 610: judge the slip as a learner rounds it: the value at the asked places must sit outside the band, else it still fires */
    const step = Math.pow(10, -d) / scale, rounded = Math.round(x.value / step) * step;
    if (Math.abs(rounded - x.value) <= hw + 1e-12) return;
    if (hw < half * 0.999) warn(file, `${where}.wrong[${i}]`, `[wrong-band] wrong "${x.id || i}" (${x.value}, band +-${+hw.toPrecision(3)}) is narrower than the rounding the question asks for (${d} decimal place${d === 1 ? '' : 's'}, +-${+half.toPrecision(3)}), so a learner who rounds this slip as asked misses it; widen its tol or give the value at the asked rounding`);
  });
};
const FLOAT_EXPECT = /(?:^|[\[(,\s])-?\d+\.\d*[1-9]\d*(?:e[+-]?\d+)?(?=[\]),\s]|$)/i;
const tolCase = (file, at, t) => {
  if (t.tol == null) return;
  if (!(isObj(t.tol) && (typeof t.tol.rel === 'number' || typeof t.tol.abs === 'number') && Object.values(t.tol).every(v => typeof v === 'number' && v >= 0))) err(file, `${at}.tol`, 'tol is { "rel": r } or { "abs": x } (or both), for compare: "isclose"');
  else if (t.compare && t.compare !== 'isclose') warn(file, `${at}.tol`, 'tol only applies to compare: "isclose"');
  if (t.budget != null && !(typeof t.budget === 'number' && t.budget >= 0 && t.budget <= 120000)) err(file, `${at}.budget`, 'a case budget is extra milliseconds for that case, 0 to 120000');
};
/* ENGINE-BACKLOG 469 (E14): data { "name.csv": "content/data/<path>" } on a Python code widget or a drill file. Each path must be under
   content/data/, exist and hold at most DATA_CAP bytes of UTF-8 text; the name is the bare file name the code and the tests read. */
const DATA_CAP = 256 * 1024;
const dataFiles = (file, where, w, { cpp = false } = {}) => {
  if (w.dataPeek != null && typeof w.dataPeek !== 'boolean') err(file, `${where}.dataPeek`, 'dataPeek is true or false (false hides the first-rows panel under the editor)');
  if (w.data == null) return;
  if (cpp) { err(file, `${where}.data`, 'data is for Python code items only: C++ has no file system, so pass the data as call arguments or inside the prelude'); return; }
  if (!isObj(w.data) || !Object.keys(w.data).length) { err(file, `${where}.data`, 'data maps bare file names to paths under content/data/ ({ "houses.csv": "content/data/houses.csv" })'); return; }
  Object.entries(w.data).forEach(([name, p]) => {
    const at = `${where}.data["${name}"]`;
    if (!/^[A-Za-z0-9][\w.-]*$/.test(name) || name === '.' || name === '..') err(file, at, 'the name is a bare file name (letters, digits, dot, dash, underscore), as the code opens it');
    else if (isObj(w.files) && name in w.files) err(file, at, 'the name is also a key of files');
    if (typeof p !== 'string' || !/^content\/data\/[\w./-]+$/.test(p) || /(^|\/)\.\.?(\/|$)/.test(p)) { err(file, at, 'the path starts with content/data/ and has no .. ("content/data/houses.csv")'); return; }
    const abs = path.join(APP, p);
    let st = null; try { st = fs.statSync(abs); } catch { /* reported below */ }
    if (!st || !st.isFile()) { err(file, at, `${p} does not exist (paths are relative to app/)`); return; }
    if (st.size > DATA_CAP) err(file, at, `${p} is ${st.size} bytes, over the ${DATA_CAP / 1024} KB cap for a data file`);
    else { try { new TextDecoder('utf-8', { fatal: true }).decode(fs.readFileSync(abs)); } catch { err(file, at, `${p} is not UTF-8 text (data files are text: csv, tsv, json, txt, hex)`); } }
  });
};
const cppCodeWidget = (file, where, w) => {
  dataFiles(file, where, w, { cpp: true });
  if (!Array.isArray(w.tests) || w.tests.length < 3) err(file, `${where}.tests`, 'at least 3 tests');
  else if (w.tests.length > 15) err(file, `${where}.tests`, 'at most 15 tests');
  if (w.examples != null && !Array.isArray(w.examples)) err(file, `${where}.examples`, 'examples is a list of cases');
  const cases = [...(Array.isArray(w.tests) ? w.tests.map((t, i) => [t, `${where}.tests[${i}]`]) : []), ...(Array.isArray(w.examples) ? w.examples.map((t, i) => [t, `${where}.examples[${i}]`]) : [])];
  const isOut = (t) => t.compiles == null && (t.compare === 'stdout' || (t.call == null && t.expect != null && t.compare == null));
  const objs = cases.filter(([t]) => t && typeof t === 'object');
  const script = objs.some(([t]) => t.compiles == null && (isOut(t) || t.stdin != null || t.argv != null || (t.compare === 'raises' && t.call == null)));
  /* pass 7 (items 402, 403, 437, 438, 455): widget options */
  const FLAG_OK = /^-(W[\w=+-]*|O[0-3sz]|D[A-Za-z_]\w*(=[\w.+-]*)?|U[A-Za-z_]\w*|f(no-)?fast-math|std=c\+\+(14|17|20))$/;
  if (w.flags != null && !(Array.isArray(w.flags) && w.flags.every(f => typeof f === 'string'))) err(file, `${where}.flags`, 'flags is a list of compiler flags ("-Wall", "-O2", "-DNDEBUG")');
  else (w.flags || []).forEach((f, k) => { if (!FLAG_OK.test(f)) err(file, `${where}.flags[${k}]`, `flag ${f} is not allowed: use -W..., -O0 to -O3, -Os, -DNAME[=v], -UNAME, -ffast-math or -std=c++14/17/20`); });
  ['leakCheck', 'testkit', 'allocCheck'].forEach(k => { if (w[k] != null && typeof w[k] !== 'boolean') err(file, `${where}.${k}`, `${k} is true or false`); });
  if (w.signature != null && !(typeof w.signature === 'string' && /^.+?\b[A-Za-z_]\w*\s*\([\s\S]*\)\s*$/.test(w.signature.trim()))) err(file, `${where}.signature`, 'signature is a declaration such as "double total(const std::vector<double>&)"');
  if (w.allocCheck === true) { // item 470: the harness defines alloc_count(), reset_alloc_count() and the global operator new; a hidden prelude must not
    const hidden = [w.prelude, w.postlude, ...(isObj(w.files) ? Object.values(w.files) : [])].filter(x => typeof x === 'string').join('\n');
    if (/\boperator\s+new\b/.test(hidden)) err(file, `${where}.allocCheck`, 'allocCheck supplies the global operator new: remove the replacement operator new from the prelude, postlude or files');
    if (/\b(?:(?:reset_)?alloc_count|free_count|live_blocks)\s*\(\s*\)\s*\{/.test(hidden)) err(file, `${where}.allocCheck`, 'allocCheck defines alloc_count(), reset_alloc_count(), free_count() and live_blocks(): do not define them in the prelude');
    if (!(w.tests || []).some(t => t && typeof t === 'object' && /\b(?:alloc_count|free_count|live_blocks)\s*\(/.test(`${t.call || ''} ${t.setup || ''}`))) warn(file, `${where}.allocCheck`, 'allocCheck is on but no test reads alloc_count(), free_count() or live_blocks()');
  }
  if (w.files != null && !(isObj(w.files) && Object.entries(w.files).every(([k, v]) => /^[\w.-]+\.(cpp|cc|h|hpp)$/.test(k) && k !== 'main.cpp' && typeof v === 'string'))) err(file, `${where}.files`, 'files maps hidden file names (pricer.h, pricer.cpp) to C++ source');
  cases.forEach(([t, at]) => {
    if (!t || typeof t !== 'object') { err(file, at, 'each case is an object'); return; }
    if (t.compare && !['isclose', 'equal', 'stdout', 'raises'].includes(t.compare)) err(file, `${at}.compare`, 'a C++ case compares isclose, equal, stdout or raises');
    tolCase(file, at, t);
    if (t.defines != null && !(isObj(t.defines) && Object.entries(t.defines).every(([k, v]) => /^[A-Za-z_]\w*$/.test(k) && ['number', 'string', 'boolean'].includes(typeof v)))) err(file, `${at}.defines`, 'defines maps macro names to values ({ "BUGGY": 1 })');
    if (t.compiles != null) { // item 474: a snippet that must (or must not) compile after the learner's code
      if (typeof t.compiles !== 'string' || !t.compiles.trim()) err(file, `${at}.compiles`, 'compiles is C++ statements ("Connection b = a;")');
      if (t.expect != null && typeof t.expect !== 'boolean') err(file, `${at}.expect`, 'a compile check expects true (it compiles) or false (it must not)');
      if (t.call != null) err(file, `${at}.call`, 'a compile check has no call');
      return;
    }
    if ((t.lines != null || t.match != null) && !isOut(t)) err(file, at, 'lines and match apply to a stdout case');
    if (t.match != null) { try { new RegExp(String(t.match), 'm'); } catch (e) { err(file, `${at}.match`, `match is not a regular expression: ${e.message}`); } }
    if (t.stdin != null && typeof t.stdin !== 'string') err(file, `${at}.stdin`, 'stdin is a string, the text std::cin reads ("250\\n262.5\\n")');
    if (t.exact != null && typeof t.exact !== 'boolean') err(file, `${at}.exact`, 'exact is true or false');
    if (t.exact != null && !isOut(t)) warn(file, `${at}.exact`, 'exact only applies to compare: "stdout"');
    if (t.argv != null && !(Array.isArray(t.argv) && t.argv.every(x => typeof x === 'string' || typeof x === 'number'))) err(file, `${at}.argv`, 'argv is a list of strings, the words after ./main');
    if (t.setup != null && typeof t.setup !== 'string') err(file, `${at}.setup`, 'setup is C++ statements run before call ("std::vector<double> xs{1, 2};")');
    if (script && t.call != null) err(file, `${at}.call`, 'this widget is in script mode (a stdout, stdin, argv or whole-program raises case), where the program runs its own main; a C++ case cannot also have call');
    if (script && t.setup != null) err(file, `${at}.setup`, 'setup needs function mode (cases with call)');
    if (t.compare === 'raises') {
      if (t.expect != null && (typeof t.expect !== 'string' || !/^[A-Za-z_][\w:]*$/.test(t.expect.trim()))) err(file, `${at}.expect`, 'a raises case names the exception type ("std::invalid_argument"), or leaves expect out to accept any error exit');
    } else if (isOut(t)) {
      if (typeof t.expect !== 'string' && t.match == null) err(file, `${at}.expect`, 'a stdout case needs expect: the printed text, as a string ("Return: 5.00%\\n")');
      if (t.call != null) err(file, `${at}.call`, 'a stdout case has no call (it compares what the whole program prints)');
    } else {
      if (typeof t.call !== 'string' || !t.call.trim()) err(file, `${at}.call`, 'a value case needs call: a C++ expression ("mean({1.0, 2.0})") or a function name with args');
      if (t.expect === undefined || t.expect === null) err(file, `${at}.expect`, 'a value case needs expect, a JSON value (2.5, true, "abc", [1, 2])');
      else if (!cppExpect(t.expect)) err(file, `${at}.expect`, 'expect is a number, a boolean, a string, a complex { re, im } or a list of those');
      else if (t.compare === 'isclose' && !cppNumbers(t.expect)) err(file, `${at}.expect`, 'isclose needs a number (or a list of numbers) as expect, not text: write 2.5, not "2.5"');
      else if (typeof t.expect === 'string' && t.text !== true && /^-?\d+(\.\d+)?([eE][+-]?\d+)?$/.test(t.expect.trim())) warn(file, `${at}.expect`, `expect is the text "${t.expect}": is the call's result a std::string? If so add "text": true to this case; if it is a number, write it without quotes`); // item 472
      if (typeof t.expect === 'number' && !Number.isInteger(t.expect) && t.compare !== 'isclose') warn(file, `${at}.compare`, 'equal compares a double exactly; use compare: "isclose" for a computed double');
    }
    if (t.args != null) {
      if (!Array.isArray(t.args)) err(file, `${at}.args`, 'args is a list of JSON values, one per parameter');
      else {
        if (typeof t.call === 'string' && !/^[A-Za-z_][\w:]*$/.test(t.call.trim())) err(file, `${at}.call`, 'with args, call is the function name alone ("mean")');
        t.args.forEach((v, k) => { if (!cppValue(v)) err(file, `${at}.args[${k}]`, 'an argument is a number, a boolean, a string or a list of those'); });
      }
    }
    if (t.types != null) {
      if (!Array.isArray(t.args)) err(file, `${at}.types`, 'types goes with args (one C++ type per argument)');
      else if (!Array.isArray(t.types) || t.types.length !== t.args.length || !t.types.every(x => x == null || typeof x === 'string')) err(file, `${at}.types`, 'types is a list of C++ type names, one per argument (null to infer one)');
      else t.types.forEach((x, k) => { if (x != null && !CPP_TYPES.includes(x.replace(/\s+/g, ' ').replace(/\s*([<>,])\s*/g, '$1').replace('long long', 'long long'))) warn(file, `${at}.types[${k}]`, `${x} is not one of the supported types (${CPP_TYPES.join(', ')}); it is written as ${x}{...} or ${x}(value)`); });
    }
  });
  ['prelude', 'postlude'].forEach(k => { if (w[k] != null && typeof w[k] !== 'string') err(file, `${where}.${k}`, `${k} is C++ source, a string`); });
  if (w.solution == null) warn(file, `${where}.solution`, 'no solution: Show solution and the playthrough need one');
  if (w.budget != null && !(typeof w.budget === 'number' && w.budget >= 0 && w.budget <= 120000)) err(file, `${where}.budget`, 'budget is extra milliseconds for each case, 0 to 120000');
  if (!w.how) warn(file, `${where}.how`, 'say how it is checked');
};
const req = (file, where, obj, fields) => fields.forEach(f => { if (obj == null || obj[f] === undefined || obj[f] === null || obj[f] === '') err(file, where ? `${where}.${f}` : f, 'required field missing'); });

/* Drill pattern vocabulary (item 472): the PATTERNS array in js/screens/drill-lib.js, the one list the app and the validator share */
const DRILL_PATTERNS = (() => {
  try {
    const src = fs.readFileSync(path.join(APP, 'js', 'screens', 'drill-lib.js'), 'utf8');
    const m = /const PATTERNS = (\[[\s\S]*?\]);\n/.exec(src);
    return JSON.parse(m[1]).map(x => x[0]);
  } catch { return []; }
})();
/* Art kinds from js/art.js, so course art always draws */
const ART = (() => {
  try { const src = fs.readFileSync(path.join(APP, 'js', 'art.js'), 'utf8'); const body = src.slice(src.indexOf('const art = {')); return new Set([...body.matchAll(/^\s{4}([a-z]+): \(\)/gm)].map(m => m[1])); } catch { return null; }
})();

/* ---------- The engine's grading helpers (js/engine/grade.js), loaded in a sandbox for checks that need them ---------- */
const ENGINE = (() => {
  try {
    const src = fs.readFileSync(path.join(APP, 'js', 'engine', 'grade.js'), 'utf8');
    const ctx = { window: {}, document: { addEventListener() {} }, console };
    vm.createContext(ctx); vm.runInContext(src, ctx);
    return ctx.window.ZQ && ctx.window.ZQ.grade;
  } catch { return null; }
})();

/* The simulation helpers (js/engine/sim.js), so a sim block's outcome, let and filter are compiled as the engine will */
const SIM = (() => {
  try {
    const src = fs.readFileSync(path.join(APP, 'js', 'engine', 'sim.js'), 'utf8');
    const ctx = { window: {}, console };
    vm.createContext(ctx); vm.runInContext(src, ctx);
    return ctx.window.ZQ && ctx.window.ZQ.sim;
  } catch { return null; }
})();
const checkSim = (file, where, sim, names) => {
  if (!SIM || !isObj(sim)) return;
  if (sim.outcome == null) { err(file, `${where}.outcome`, 'a sim needs an outcome expression'); return; }
  try { SIM.trial(sim, Object.fromEntries(names.map(n => [n, 1]))); } catch (e) { err(file, where, `simulation does not compile: ${e.message}`); }
};

/* A canvas the learner can work without a widget: points with drag: true (plane, number-line), vectors in state.drag,
   or a simulation's run chips (bars, walk) */
const authorMovable = (c) => {
  if (isObj(c) && c.kind === 'pair') return authorMovable(c.left) || authorMovable(c.right) || (Array.isArray(c.controls) && c.controls.length > 0);
  if (isObj(c) && c.kind === 'circle' && ((isObj(c.state) && c.state.drag === true) || (isObj(c.params) && c.params.drag === true))) return true;
  if (isObj(c) && c.kind === 'interleave') return true; // the lanes' Step buttons are its own input (item 471)
  const st = isObj(c && c.state) ? c.state : {}, p = isObj(c && c.params) ? c.params : {};
  return (Array.isArray(st.points) && st.points.some(q => isObj(q) && q.drag === true)) || (Array.isArray(st.drag) && st.drag.length > 0) || isObj(p.sim);
};

/* ---------- Canvas ids ---------- */
const range = (a, b) => Array.from({ length: Math.max(0, b - a + 1) }, (_, i) => a + i);
const regionIds = (canvas) => {
  if (!isObj(canvas)) return null;
  if (canvas.kind === 'pair') { // the side widgets drive, plus every id of either side with its "left:" or "right:" prefix
    const a = ['left', 'right'].includes(canvas.active) ? canvas.active : 'left', out = new Set();
    let unknown = false;
    ['left', 'right'].forEach(k => { const ids = regionIds(canvas[k]); if (!ids) unknown = true; else ids.forEach(id => { out.add(`${k}:${id}`); if (k === a) out.add(id); }); });
    if (unknown) return null; // a side whose ids the validator cannot list (array, scatter...): no check
    if (canvas.tap === 'sides') { out.add('left'); out.add('right'); } // whole sides (item 183)
    return out.size ? out : null;
  }
  const p = canvas.params || {};
  if (canvas.kind === 'bars' && isObj(p.bins) && p.bins.width > 0) { // histogram bins b0, b1, ... (zero-based)
    const n = Math.max(1, Math.round((p.bins.max - p.bins.min) / p.bins.width)), ids = new Set(['exact']);
    range(0, n - 1).forEach(i => { ids.add('b' + i); ids.add('exact-b' + i); });
    return ids;
  }
  if (canvas.kind === 'bars' && Array.isArray(p.categories)) { // object categories keep their own id, plain ones are x{label}
    const ids = new Set(['exact', 'pivot', 'mean', 'cut']);
    const gs = Array.isArray(p.groups) ? p.groups.map((q, i) => String(isObj(q) && q.id != null ? q.id : 'g' + i)) : [];
    p.categories.forEach(c => { const id = isObj(c) ? (c.id || 'x' + c.label) : 'x' + c; ids.add(String(id)); ids.add('exact-' + id); gs.forEach(g => { ids.add(`${id}-${g}`); ids.add('legend-' + g); }); });
    [].concat(p.curves || [], (canvas.state || {}).curves || [], p.hlines || [], (canvas.state || {}).hlines || []).forEach(q => { if (isObj(q) && q.id) { ids.add(String(q.id)); ids.add(q.id + '-shade'); } });
    return ids;
  }
  if (canvas.kind === 'grid' && p.population) { // item 282: population groups are the regions
    return new Set([].concat((canvas.state || {}).groups || [], (canvas.enter || {}).groups || []).map((q, i) => String(isObj(q) && q.id != null ? q.id : 'g' + i)));
  }
  if (canvas.kind === 'grid' && p.rows && p.cols) {
    const ids = new Set();
    if (p.margins) { range(0, p.rows).forEach(i => ids.add('rsum' + i)); range(0, p.cols).forEach(j => ids.add('csum' + j)); ids.add('total'); }
    range(0, p.rows).forEach(i => range(0, p.cols).forEach(j => ids.add(`r${i}c${j}`)));
    const routes = (canvas.state || {}).paths; // routes drawn over the grid (item 93) answer to their ids
    (Array.isArray(routes) ? routes.map((q, k) => (isObj(q) && q.id != null ? q.id : 'path' + (k + 1))) : isObj(routes) ? Object.keys(routes) : []).forEach(id => ids.add(String(id)));
    return ids;
  }
  if (canvas.kind === 'venn') {
    const n = Array.isArray(p.sets) ? p.sets.length : 2;
    const L = ['A', 'B', 'C'].slice(0, Math.max(2, Math.min(3, n)));
    const named = Array.isArray(p.sets) ? p.sets.map(String) : [];
    const ids = new Set(['none']);
    const subsets = (arr) => { const out = []; for (let m = 1; m < 1 << arr.length; m++) out.push(arr.filter((_, i) => m & (1 << i)).join('')); return out; };
    subsets(L).forEach(x => ids.add(x)); if (named.every(x => x.length === 1)) subsets(named).forEach(x => ids.add(x));
    return ids;
  }
  if (canvas.kind === 'area' && (Array.isArray(p.grid) || (p.shape === 'circle' && p.sectors))) {
    /* one-based from the top left, c{i}{j}, or c{i}-{j} when either index is 10 or more; circle sectors are c1{j} */
    const [r, c] = p.shape === 'circle' ? [1, p.sectors || p.grid[1]] : p.grid, ids = new Set();
    const st = canvas.state || {}, g2 = st.grid != null ? [].concat(st.grid) : null; // a re-cut grid in the state
    const [R2, C2] = g2 ? (p.shape === 'circle' ? [1, +g2[g2.length - 1]] : g2.length > 1 ? [+g2[0], +g2[1]] : [r, +g2[0]]) : [r, c];
    range(1, R2).forEach(i => range(1, C2).forEach(j => ids.add(i >= 10 || j >= 10 ? `c${i}-${j}` : `c${i}${j}`)));
    return ids;
  }
  if ((canvas.kind === 'number-line' && Array.isArray((canvas.state || {}).points)) || canvas.kind === 'plane') {
    const st = canvas.state || {}, pp = canvas.params || {}, en = canvas.enter || {};
    const ids = new Set((Array.isArray(st.points) ? st.points : []).map(q => q && q.id).filter(Boolean)); // tap mode on points
    /* item 413: number-line intervals are tap targets with tapIntervals (or tap: true) */
    if (canvas.kind === 'number-line') (Array.isArray(st.intervals) ? st.intervals : []).forEach(q => { if (isObj(q) && q.id && (pp.tapIntervals || q.tap === true)) ids.add(q.id); });
    /* item 467: polygons (tap targets since pass 5), angles, areas and riemann pieces by id, from state, enter or params */
    if (canvas.kind === 'plane') { [st.segments, st.vectors, st.vlines, st.hlines, pp.vlines, pp.hlines, pp.functions, st.functions, st.polygons, pp.polygons, en.polygons, st.angles, pp.angles, en.points].forEach(L => (Array.isArray(L) ? L : []).forEach(q => { if (isObj(q) && q.id) ids.add(String(q.id)); })); [].concat(st.area || [], st.riemann || []).forEach(q => { if (isObj(q) && q.id) ids.add(String(q.id)); }); ['tangent', 'area', 'riemann', 'target', 'sketch'].forEach(k => ids.add(k)); }
    return ids;
  }
  if (canvas.kind === 'space') { // every object id, from params, state and enter (tap mode: points, vectors, curves, lines, surfaces, planes, fields)
    const st = canvas.state || {}, en = canvas.enter || {}, ids = new Set();
    ['points', 'vectors', 'curves', 'lines', 'surfaces', 'planes', 'fields'].forEach(k => [p[k], st[k], en[k]].forEach(L => { if (Array.isArray(L)) L.forEach(q => { if (isObj(q) && q.id != null) ids.add(String(q.id)); }); else if (isObj(L)) Object.keys(L).forEach(id => ids.add(id)); }));
    return ids.size ? ids : null;
  }
  if (canvas.kind === 'interleave' && Array.isArray(p.lanes)) return interleaveEngine.idsOf(p); // step ids (a1, t1-2), lane-<id>, var-<name>, lock-<name> (item 471)
  if (canvas.kind === 'console' && (Array.isArray(p.lines) || typeof p.text === 'string')) { // one-based line ids
    const st = canvas.state || {}, n = Array.isArray(st.lines) ? Math.max(st.lines.length, (p.lines || String(p.text || '').replace(/\n$/, '').split('\n')).length) : (p.lines || String(p.text).replace(/\n$/, '').split('\n')).length;
    return new Set(range(1, n).map(i => `l${i}`));
  }
  if (canvas.kind === 'table' && Array.isArray(p.rows)) {
    const r = p.rows.length, c = Array.isArray(p.columns) ? p.columns.length : (p.rows[0] || []).length, ids = new Set();
    range(0, r).forEach(i => { ids.add(`r${i}`); range(0, c).forEach(j => ids.add(`r${i}c${j}`)); });
    range(0, c).forEach(j => ids.add(`c${j}`));
    return ids;
  }
  return null;
};
const PLAUSIBLE = {
  grid: /^(r\d+c\d+|row\d+|col\d+|cross\d+|path\d+)$/,
  venn: /^(A|B|C|AB|AC|BC|ABC|none|[A-Za-z]{1,3})$/,
  area: /^(c\d+(-\d+)?|pt\d+|shade|split|point)$/,
  table: /^(r\d+|c\d+|r\d+c\d+)$/,
  console: /^l\d+$/,
  matrix: /^[A-Za-z][A-Za-z0-9]*(-(r\d+|c\d+|\d+-\d+))?$/,
  walk: /^(path\d+|barrier-up|barrier-down|mean|mean-level|spread|envelope|stop-time|stopped-ref|stopped-[\w-]+|ov-[\w-]+)$/, // inbox (arma 1): README-B's mean and spread; item 436: overlays and the stopped average
  orderbook: /^(bid\d+|ask\d+|spread)$/,
  distribution: /^(mean|median|sd|prob|curve|cdf|rug|shade\d*|observed\d*|x-?[\d.]+|overlay\d+)$/,
  scatter: /^(p\d+|line|line\d+|fit|r-p\d+|legend-.+|curve|[A-Za-z][\w-]*)$/, // item 351: the fit, curve ids and residuals r-p{i}
  circle: /^(angle|sin|cos|tan|pt|arc|radius)$/,
  bars: /^(exact-)?(x[A-Za-z0-9.-]+|b\d+)$/,
  array: /^(c\d+|[a-z][a-z0-9-]*)$/,
};
const plausibleId = (canvas, id) => {
  if (!isObj(canvas)) return true;
  if (canvas.kind === 'pair' && canvas.tap === 'sides' && ['left', 'right'].includes(String(id))) return true;
  if (canvas.kind === 'pair') { const m = String(id).match(/^(left|right):(.+)$/); const a = ['left', 'right'].includes(canvas.active) ? canvas.active : 'left'; return m ? plausibleId(canvas[m[1]], m[2]) : plausibleId(canvas[a], id) || plausibleId(canvas[a === 'left' ? 'right' : 'left'], id); }
  const ids = regionIds(canvas);
  if (ids && ids.has(id)) return true;
  if (canvas.kind === 'grid' && ids) return id === 'all' || /^(row|col|cross)\d+(-\d+)?$/.test(id); // item 329: "all" highlights every cell
  if (canvas.kind === 'distribution' && [(canvas.params || {}).overlay, (canvas.state || {}).overlay, (canvas.enter || {}).overlay].some((L) => Array.isArray(L) && L.some((o, j) => String(isObj(o) && o.id ? o.id : 'overlay' + j) === String(id)))) return true; // overlay ids in params or state (items 170, 329)
  if (canvas.kind === 'distribution' && [(canvas.state || {}).shade, (canvas.state || {}).observed].some((L) => Array.isArray(L) && L.some((o) => isObj(o) && String(o.id) === String(id)))) return true; // named shade regions and observed markers
  const re = PLAUSIBLE[canvas.kind];
  return re ? re.test(String(id)) : /^[A-Za-z0-9][A-Za-z0-9_.-]*$/.test(String(id));
};

/* ---------- Widgets (rule 4) and the keys they can produce (rule 5) ---------- */
const checkWidget = (file, where, w, canvas, ctx = {}) => {
  if (!isObj(w)) { err(file, where, 'widget must be an object'); return null; }
  if (!WIDGETS.has(w.kind)) { err(file, `${where}.kind`, `unknown widget kind "${w.kind}"`); return null; }
  if (w.kind === 'longform' && !ctx.allowLongform) err(file, `${where}.kind`, 'longform belongs in homework and exams');
  const keys = new Set();
  if (w.carry != null && w.kind !== 'trade' && !(typeof w.carry === 'string' && /^[A-Za-z][A-Za-z0-9]*$/.test(w.carry))) err(file, `${where}.carry`, 'carry is a name of letters and digits');
  /* Shapes first, so a field of the wrong type is one error line and never a crash further down */
  const LISTS = ['options', 'among', 'tokens', 'slots', 'lines', 'points', 'wrong', 'tests', 'examples', 'moves', 'rubric', 'order', 'same'];
  const badShape = LISTS.filter(f => w[f] != null && !Array.isArray(w[f]));
  if (['tap-regions', 'order'].includes(w.kind) && w.answer != null && !Array.isArray(w.answer)) badShape.push('answer');
  if (w.kind === 'expression' && w.accept != null && !Array.isArray(w.accept)) badShape.push('accept');
  if (w.kind === 'place' && w.mode === 'boxes' && w.answer != null && (!isObj(w.answer) || Object.values(w.answer).some(v => !Array.isArray(v)))) badShape.push('answer');
  if (badShape.length) { badShape.forEach(f => err(file, `${where}.${f}`, f === 'answer' && w.kind === 'place' ? 'answer must map each container id to a list of item ids' : `${f} must be a list`)); keys.add('*'); return keys; }
  if (['options', 'tokens', 'slots', 'lines', 'points', 'wrong'].some(f => (w[f] || []).some(x => !isObj(x)))) { err(file, where, 'every entry of options, tokens, slots, lines, points and wrong is an object'); keys.add('*'); return keys; }
  ['options', 'wrong'].forEach(f => (w[f] || []).forEach((x, i) => wholeCanvasPatch(file, `${where}.${f}[${i}].canvas`, x.canvas)));
  const ids = (arr, label) => { const seen = new Set(); (arr || []).forEach((x, i) => { if (!x || x.id == null) err(file, `${where}.${label}[${i}].id`, 'required field missing'); else if (seen.has(x.id)) err(file, `${where}.${label}[${i}].id`, `duplicate id "${x.id}"`); else seen.add(x.id); }); return seen; };
  const tol = (t, at) => { if (!isObj(t) || (typeof t.abs !== 'number' && typeof t.rel !== 'number')) err(file, at, 'tol must be { "abs": x } or { "rel": r }'); };
  const text = (s, at) => checkText(file, at, s);
  switch (w.kind) {
    case 'choice': case 'multi': {
      if (!Array.isArray(w.options) || w.options.length < 2) { err(file, `${where}.options`, 'at least two options'); break; }
      ids(w.options, 'options').forEach(k => keys.add(String(k)));
      const correct = w.options.filter(o => o && o.correct === true).length;
      if (w.kind === 'choice' && correct !== 1) err(file, `${where}.options`, `exactly one option must be correct (found ${correct})`);
      if (w.kind === 'multi' && correct < 1) err(file, `${where}.options`, 'at least one option must be correct');
      w.options.forEach((o, i) => {
        if (!o) return;
        if (o.text == null && o.image == null) err(file, `${where}.options[${i}]`, 'option needs text or image');
        if (o.image != null && ART && !ART.has(o.image)) err(file, `${where}.options[${i}].image`, `unknown art id "${o.image}"`);
        if (w.kind === 'choice' && !o.correct && !o.why) err(file, `${where}.options[${i}].why`, 'every distractor needs a why naming its misconception');
        text(o.text, `${where}.options[${i}].text`); text(o.why, `${where}.options[${i}].why`);
      });
      checkKeyLength(file, where, w);
      checkShuffleFalse(file, where, w);
      if (w.kind === 'multi' && ctx.question != null && !/select all that apply/i.test(ctx.question)) warn(file, where, 'a multi question should say "Select all that apply"');
      break;
    }
    case 'numeric':
      /* ENGINE-BACKLOG 832: a set answer, answers: [2, -5] with unordered: true; the learner types the values separated by commas */
      if (w.answers != null || w.unordered != null) {
        if (!(Array.isArray(w.answers) && w.answers.length >= 2 && w.answers.every(a => typeof a === 'number' && Number.isFinite(a)))) err(file, `${where}.answers`, 'numeric answers is a list of two or more numbers');
        if (w.unordered !== true) err(file, `${where}.unordered`, 'unordered must be true with answers (the values are an unordered set)');
        if (w.answer != null) err(file, `${where}.answer`, 'give answers (a set) or answer, not both');
        if (w.unit === '%') err(file, `${where}.unit`, 'unit "%" is not used with answers');
        tol(w.tol, `${where}.tol`);
        ids(w.wrong, 'wrong').forEach(k => keys.add(String(k)));
        keys.add('count');
        (w.wrong || []).forEach((x, i) => {
          const parts = typeof x.value === 'string' ? x.value.split(',').map(t => t.trim()) : [];
          if (parts.length < 2 || parts.some(t => !/^-?(\d+\.?\d*|\.\d+)(\/-?\d+\.?\d*)?$/.test(t))) { err(file, `${where}.wrong[${i}].value`, 'a wrong value of a set is text of two or more numbers separated by commas, for example "2, 5"'); return; }
          if (Array.isArray(w.answers) && parts.length === w.answers.length && isObj(w.tol)) {
            const nums = parts.map(t => { const m = t.split('/'); return m.length === 2 ? +m[0] / +m[1] : +t; }), tl = w.tol.rel != null ? (a) => Math.abs(a) * w.tol.rel : () => w.tol.abs || 0;
            const pool = w.answers.slice(), hit = nums.every(v => { const k = pool.findIndex(a => Math.abs(v - a) <= tl(a) + 1e-9); if (k < 0) return false; pool.splice(k, 1); return true; });
            if (hit) err(file, `${where}.wrong[${i}].value`, 'this wrong set is inside the answer\'s tolerance, so it grades correct and never fires');
          }
        });
        text(w.accept, `${where}.accept`);
        break;
      }
      if ((typeof w.answer !== 'number' || !Number.isFinite(w.answer)) && !(typeof w.answer === 'string' && /^\{\{\s*carry\.[A-Za-z0-9_.]+\s*\}\}$/.test(w.answer))) err(file, `${where}.answer`, 'numeric answer must be a number (or one {{carry.name}} placeholder)');
      tol(w.tol, `${where}.tol`);
      wrongCannotFire(file, where, w.answer, w.tol, w.wrong);
      wrongBandNarrow(file, where, w, ctx);
      ids(w.wrong, 'wrong').forEach(k => keys.add(String(k)));
      (w.wrong || []).forEach((x, i) => { if (typeof x.value !== 'number') err(file, `${where}.wrong[${i}].value`, 'must be a number'); if (x.tol) tol(x.tol, `${where}.wrong[${i}].tol`); });
      text(w.accept, `${where}.accept`);
      /* item 515: with unit "%" the engine divides what the learner types by 100, so the key is the fraction (0.1587, not 15.87) */
      if (w.unit === '%') {
        const accText = typeof w.accept === 'string' ? w.accept : '';
        /* items 516, 517: the accept figure that represents the key: the one after the last "=" or "\\approx" if it is followed by % or "per cent", else the leading figure (first number, before any colon) if followed by % or "per cent" */
        const fig = /(-?[−–]?\d[\d,]*(?:\.\d+)?)(\s*(?:%|per ?cent))?/i, flat = accText.replace(/\\%/g, '%');
        const tailTxt = flat.split(/=|\\approx/).slice(1).pop(), tailM = tailTxt && tailTxt.match(fig);
        const lead = tailM && tailM[2] ? tailM : flat.split(':')[0].match(fig);
        const shown = lead && lead[2] ? [Math.abs(+lead[1].replace(/[−–,]/g, '').replace(/^-/, ''))] : [];
        const pctKey = (v, f, isKey) => {
          if (typeof v !== 'number' || !Number.isFinite(v) || v === 0 || (Math.abs(v) <= 1 && !isKey)) return; // at or below 1, only the key itself (a wrong value may be a real per cent)
          const same = shown.some(n => Math.abs(n - Math.abs(v)) < 1e-9 * Math.max(1, n));
          if (same) err(file, f, `unit "%" divides the typed value by 100, so the key is the fraction: ${v} should be ${+(v / 100).toPrecision(12)} (accept shows ${v}%)`);
          else if (Math.abs(v) > 1 && w.over100 !== true) warn(file, f, `unit "%" key ${v} is above 1: the key is the fraction (1.25 for 125%); if it really is over 100%, add "over100": true`);
        };
        pctKey(w.answer, `${where}.answer`, true);
        (Array.isArray(w.wrong) ? w.wrong : []).forEach((x, i) => x && pctKey(x.value, `${where}.wrong[${i}].value`));
      }
      break;
    case 'expression':
      /* ENGINE-BACKLOG 832: a set answer, answers: ["2", "-5"] with unordered: true; the learner types the values separated by commas */
      if (w.answers != null || w.unordered != null) {
        if (!(Array.isArray(w.answers) && w.answers.length >= 2 && w.answers.every(a => typeof a === 'string' && a.trim()))) err(file, `${where}.answers`, 'expression answers is a list of two or more TeX strings');
        if (w.unordered !== true) err(file, `${where}.unordered`, 'unordered must be true with answers (the values are an unordered set)');
        if (w.answer != null) err(file, `${where}.answer`, 'give answers (a set) or answer, not both');
        if (w.accept != null) err(file, `${where}.accept`, 'accept is not used with answers: list every value in answers');
        if (w.form != null) err(file, `${where}.form`, 'form is not used with answers');
        if (w.upToConstant != null) err(file, `${where}.upToConstant`, 'upToConstant is not used with answers');
        ids(w.wrong, 'wrong').forEach(k => keys.add(String(k)));
        keys.add('count');
        (w.wrong || []).forEach((x, i) => { if (typeof x.tex !== 'string' || !x.tex.includes(',')) err(file, `${where}.wrong[${i}].tex`, 'a wrong value of a set is TeX with the values separated by commas, for example "2, 5"'); });
        (Array.isArray(w.answers) ? w.answers : []).forEach((a, i) => { if (typeof a === 'string') checkText(file, `${where}.answers[${i}]`, `$${a}$`, { copy: false }); });
        break;
      }
      if (typeof w.answer !== 'string' || !w.answer) err(file, `${where}.answer`, 'expression answer must be a TeX string');
      if (!Array.isArray(w.accept) || !w.accept.length) warn(file, `${where}.accept`, 'list the accepted plain-text forms for the fallback grader');
      /* engine pass (items 433, 437): a capital N or D, \min, \max and \epsilon now grade; a vector or matrix answer has the key "length" for a wrong size */
      if (typeof w.answer === 'string' && /^\s*(\\left\s*)?[(\[][^]*,|\\begin\{[pbv]?matrix\}/.test(w.answer)) keys.add('length');
      /* P32-expr-exp: a learner's \exp(...) is graded as e^{...}; an authored form should say e^{...} (the screen shows the answer) */
      [['answer', w.answer], ...(Array.isArray(w.accept) ? w.accept.map((a, i) => [`accept[${i}]`, a]) : [])].forEach(([f, v]) => { if (typeof v === 'string' && /\\(?:exp|operatorname\{exp\}|mathrm\{exp\})(?![A-Za-z])/.test(v)) warn(file, `${where}.${f}`, 'write e^{...} in an authored answer: a learner\'s \\exp(...) is graded as e^{...} already'); });
      if (w.functions != null && !(Array.isArray(w.functions) && w.functions.every(f => typeof f === 'string' && /^(?:[A-Za-z]|\\[A-Za-z]+)$/.test(f)))) err(file, `${where}.functions`, 'functions is a list of single letters or Greek commands, for example ["f", "\\sigma"]');
      /* P32-expr-int: integers lists symbols sampled at whole numbers; an answer with (-1)^{symbol} needs that symbol listed */
      if (w.integers != null && !(Array.isArray(w.integers) && w.integers.every(f => typeof f === 'string' && /^(?:[A-Za-z]|\\[A-Za-z]+)$/.test(f)))) err(file, `${where}.integers`, 'integers is a list of single symbols, for example ["k", "n"]');
      else [['answer', w.answer], ...(Array.isArray(w.accept) ? w.accept.map((a, i) => [`accept[${i}]`, a]) : [])].forEach(([f, v]) => { if (typeof v !== 'string') return; for (const m of v.matchAll(/\(-1\)\^(?:\{\s*(?:-?\s*)?([A-Za-z]|\\[A-Za-z]+)(?![A-Za-z])[^{}]*\}|(?:-?\s*)?([A-Za-z]))/g)) { const sym = m[1] || m[2]; if (!(w.integers || []).includes(sym)) { warn(file, `${where}.${f}`, `(-1)^{${sym}} cannot be graded at non-integer points: add integers: ["${sym}"] to this expression`); break; } } });
      ids(w.wrong, 'wrong').forEach(k => keys.add(String(k)));
      checkText(file, `${where}.answer`, `$${w.answer || ''}$`, { copy: false });
      if (w.form != null) { if (!['expanded', 'factorised', 'factorised-fully', 'completed-square', 'simplified', 'rectangular', 'fraction', 'exact-angle'].includes(w.form)) err(file, `${where}.form`, 'form is "expanded", "factorised", "factorised-fully", "completed-square", "simplified", "rectangular" (a + bi), "fraction" or "exact-angle"'); keys.add('form'); }
      break;
    case 'slider':
      ['min', 'max', 'step'].forEach(f => { if (typeof w[f] !== 'number') err(file, `${where}.${f}`, 'must be a number'); });
      if (w.answer != null) { if (typeof w.answer !== 'number') err(file, `${where}.answer`, 'must be a number'); if (typeof w.tol !== 'number') err(file, `${where}.tol`, 'slider tol must be a number'); }
      if (w.answer != null && typeof w.min === 'number' && typeof w.max === 'number' && (w.answer < w.min || w.answer > w.max)) err(file, `${where}.answer`, 'answer outside min..max');
      ids(w.wrong, 'wrong').forEach(k => keys.add(String(k)));
      break;
    case 'sliders': {
      const ids = (Array.isArray(w.sliders) ? w.sliders : []).map((x, i) => String((x && (x.id || x.bind)) || 's' + i));
      if (ids.length < 2) err(file, `${where}.sliders`, 'at least two sliders');
      (Array.isArray(w.sliders) ? w.sliders : []).forEach((x, i) => { if (!isObj(x) || typeof x.min !== 'number' || typeof x.max !== 'number') err(file, `${where}.sliders[${i}]`, 'each slider needs min and max'); });
      if (!isObj(w.answer) && typeof w.check !== 'string') err(file, `${where}`, 'sliders need answer: { id: value } or check with value');
      if (typeof w.check === 'string' && !isObj(w.show)) err(file, `${where}.show`, 'a check needs show: { id: value } for Show solution and the playthrough');
      if (isObj(w.answer)) Object.keys(w.answer).forEach(k => { if (!ids.includes(k)) err(file, `${where}.answer.${k}`, `no slider "${k}"`); });
      ids.forEach(k => keys.add(k)); keys.add('off'); (w.wrong || []).forEach(x => x && x.id && keys.add(x.id));
      break;
    }
    case 'drag-point':
      if (!Array.isArray(w.points) || !w.points.length) err(file, `${where}.points`, 'at least one point');
      (w.points || []).forEach((p, i) => {
        if (!p.id) err(file, `${where}.points[${i}].id`, 'required');
        const oneD = canvas && (canvas.kind === 'number-line' || canvas.kind === 'circle');
        if (oneD && typeof p.target === 'number') { /* a bare number: x on a number line, the angle on a circle */ }
        else if (isObj(p.target) && (p.target.line != null || p.target.expr != null)) { /* item 254: a line or an expression target */
          const pt2 = (q) => Array.isArray(q) && q.length === 2 && q.every(n => typeof n === 'number');
          if (p.target.line != null && !(Array.isArray(p.target.line) && p.target.line.length === 2 && p.target.line.every(pt2))) err(file, `${where}.points[${i}].target.line`, 'line is [[x1, y1], [x2, y2]]');
          if (p.target.expr != null) { if (typeof p.target.expr !== 'string') err(file, `${where}.points[${i}].target.expr`, 'expr is a formula in x and y'); if (!pt2(p.target.show)) err(file, `${where}.points[${i}].target.show`, 'an expression target needs show: [x, y], a point that satisfies it (Show solution and the playthrough put the point there)'); }
          if (p.target.show != null && !pt2(p.target.show)) err(file, `${where}.points[${i}].target.show`, 'show is [x, y]');
        }
        else if (isObj(p.target)) { /* { on: f, x } on a plane: the point of function f at x */
          const fns = new Set(((canvas && canvas.params || {}).functions || []).filter(isObj).map(f => f.id));
          if (!canvas || canvas.kind !== 'plane') err(file, `${where}.points[${i}].target`, '{ "on", "x" } targets need a plane canvas');
          else if (!fns.has(p.target.on)) err(file, `${where}.points[${i}].target.on`, `"${p.target.on}" is not a function on the plane`);
          if (typeof p.target.x !== 'number') err(file, `${where}.points[${i}].target.x`, 'must be a number');
        }
        else if (!Array.isArray(p.target) || p.target.length !== 2) err(file, `${where}.points[${i}].target`, oneD ? 'must be a number (or [x, y])' : 'must be [x, y], or { "on": "f", "x": number } on a plane');
        if (p.tol != null && typeof p.tol !== 'number' && !(Array.isArray(p.tol) && p.tol.length === 2 && p.tol.every(t => typeof t === 'number'))) err(file, `${where}.points[${i}].tol`, 'must be a number (default 0.25) or [dx, dy]');
        if (p.tolX != null && typeof p.tolX !== 'number') err(file, `${where}.points[${i}].tolX`, 'must be a number');
        if (p.id) keys.add(String(p.id)); // the key when this point is off target and in no wrong[] region
      });
      ids(w.wrong, 'wrong').forEach(k => keys.add(String(k)));
      break;
    case 'place': {
      if (w.mode === 'array') { // item 411: the cells of an array canvas dragged into order
        if (!canvas || canvas.kind !== 'array') err(file, where, 'place mode "array" needs an array canvas');
        const P0 = (canvas && canvas.params) || {}, n = Array.isArray(P0.cells) ? P0.cells.length : 0, from = P0.indexFrom ?? 0, ids0 = Array.from({ length: n }, (_, k) => 'c' + (k + from));
        if (!Array.isArray(w.answer) || w.answer.length !== n || new Set(w.answer).size !== n || w.answer.some(id => !ids0.includes(id))) err(file, `${where}.answer`, `answer lists every cell id (${ids0.join(', ')}) once, in the order wanted`);
        ids0.forEach(k => keys.add(k));
        break;
      }
      if (w.mode === 'boxes') {
        /* items dragged into the containers of a boxes canvas */
        if (!canvas || canvas.kind !== 'boxes') err(file, where, 'place mode "boxes" needs a boxes canvas');
        const conts = (canvas && Array.isArray((canvas.params || {}).containers) ? canvas.params.containers : []).filter(isObj);
        const cids = new Set(conts.map(c => c.id)), iids = new Set(conts.flatMap(c => (Array.isArray(c.items) ? c.items : []).filter(isObj).map(i => i.id)));
        if (w.count != null && (!isObj(w.count) || Object.values(w.count).some(n => !Number.isInteger(n) || n < 0))) err(file, `${where}.count`, 'count maps container ids to whole numbers');
        else if (isObj(w.count)) Object.keys(w.count).forEach(c => { if (canvas && !cids.has(c)) err(file, `${where}.count`, `container "${c}" is not on the boxes canvas`); keys.add('count-' + c); });
        if (w.answer == null && (w.free || isObj(w.count))) { /* free or count only: no answer needed */ }
        else if (!isObj(w.answer) || !Object.keys(w.answer).length) err(file, `${where}.answer`, 'answer maps container ids to the item ids each must hold (or give count, or free: true)');
        else Object.entries(w.answer).forEach(([c, list]) => {
          if (canvas && !cids.has(c)) err(file, `${where}.answer`, `container "${c}" is not on the boxes canvas`);
          list.forEach(id => { if (canvas && !iids.has(id)) err(file, `${where}.answer.${c}`, `item "${id}" is not on the boxes canvas`); });
        });
        iids.forEach(k => keys.add(String(k)));
        break;
      }
      if (w.same != null && !w.same.every(g => typeof g === 'string' || (Array.isArray(g) && g.every(t => typeof t === 'string')))) err(file, `${where}.same`, 'same is a list of token ids, or a list of such lists');
      const tokens = ids(w.tokens, 'tokens');
      tokens.forEach(k => keys.add(String(k)));
      if (!tokens.size) err(file, `${where}.tokens`, 'at least one token');
      if (!Array.isArray(w.slots) || !w.slots.length) err(file, `${where}.slots`, 'at least one slot');
      (w.slots || []).forEach((s, i) => { (s.accepts || []).forEach(t => { if (!tokens.has(t)) err(file, `${where}.slots[${i}].accepts`, `unknown token "${t}"`); }); text(s.label, `${where}.slots[${i}].label`); });
      if (w.mode === 'order') { if (!Array.isArray(w.order) || w.order.some(t => !tokens.has(t))) err(file, `${where}.order`, 'order must list known token ids'); }
      else if ((w.slots || []).every(s => !(s.accepts || []).length)) err(file, `${where}.slots`, 'no slot accepts any token');
      (w.tokens || []).forEach((t, i) => text(t.text, `${where}.tokens[${i}].text`));
      break;
    }
    case 'trade': {
      /* item 459: the market-making game. Shape first, then the authored strategy is played through the same game the widget runs. */
      const TRADE_FIELDS = new Set(['kind', 'seed', 'turns', 'fair', 'value', 'tick', 'range', 'size', 'limit', 'quote', 'spread', 'counterparty', 'schedule', 'benchmark', 'band', 'maxBreaks', 'strategy', 'currency', 'dp', 'carry', 'label']);
      Object.keys(w).forEach(f => { if (!TRADE_FIELDS.has(f)) err(file, `${where}.${f}`, 'unknown trade field'); });
      const fin = (v) => typeof v === 'number' && Number.isFinite(v);
      let ok = true;
      const bad = (f, m) => { ok = false; err(file, `${where}.${f}`, m); };
      if (!Number.isInteger(w.seed)) bad('seed', 'seed must be a whole number (the game is deterministic under it)');
      if (!Number.isInteger(w.turns) || w.turns < 2 || w.turns > 40) bad('turns', 'turns is a whole number from 2 to 40');
      if (!fin(w.fair)) bad('fair', 'fair (the opening mark) must be a number');
      if (!fin(w.value)) bad('value', 'value (the hidden settlement value) must be a number');
      if (w.tick != null && !(fin(w.tick) && w.tick > 0)) bad('tick', 'tick must be a positive number');
      if (w.range != null && (!Array.isArray(w.range) || w.range.length !== 2 || !w.range.every(fin) || w.range[0] >= w.range[1])) bad('range', 'range is [lowest price, highest price]');
      if (w.size != null) { if (!isObj(w.size) || Object.entries(w.size).some(([k, v]) => !['min', 'max', 'start', 'step'].includes(k) || !fin(v) || v <= 0) || (fin(w.size.min) && fin(w.size.max) && w.size.min > w.size.max)) bad('size', 'size is { min, max, start, step }, positive numbers with min at most max'); }
      if (w.limit != null && !(fin(w.limit) && w.limit > 0)) bad('limit', 'limit must be a positive number');
      if (w.quote != null && (!isObj(w.quote) || Object.entries(w.quote).some(([k, v]) => !['bid', 'ask', 'size'].includes(k) || !fin(v)))) bad('quote', 'quote is { bid, ask, size } (the opening values)');
      if (w.spread != null && (!isObj(w.spread) || Object.entries(w.spread).some(([k, v]) => !['min', 'max'].includes(k) || !fin(v) || v < 0) || (fin(w.spread.min) && fin(w.spread.max) && w.spread.min > w.spread.max))) bad('spread', 'spread is { min, max }, with min at most max');
      if (w.maxBreaks != null && !(Number.isInteger(w.maxBreaks) && w.maxBreaks >= 0)) bad('maxBreaks', 'maxBreaks is a whole number, 0 or more');
      if (w.currency != null && typeof w.currency !== 'string') bad('currency', 'currency is a short string such as "£"');
      if (w.dp != null && !(Number.isInteger(w.dp) && w.dp >= 0 && w.dp <= 6)) bad('dp', 'dp is a whole number of decimals');
      if (w.carry != null && !(typeof w.carry === 'string' && /^[A-Za-z][A-Za-z0-9]*$/.test(w.carry))) bad('carry', 'carry is a name of letters and digits');
      const hasB = w.benchmark != null, hasBand = w.band != null;
      if (hasB === hasBand) bad('benchmark', 'give exactly one of benchmark (a number: P&L at least this) or band ([low, high])');
      if (hasB && !fin(w.benchmark)) bad('benchmark', 'benchmark must be a number');
      if (hasBand && (!Array.isArray(w.band) || w.band.length !== 2 || !w.band.every(fin) || w.band[0] >= w.band[1])) bad('band', 'band is [low, high] with low below high');
      const cps = w.counterparty == null ? [] : Array.isArray(w.counterparty) ? w.counterparty : [w.counterparty];
      if (!cps.length) bad('counterparty', 'counterparty is required: { type: "noise" | "informed" | "scripted", ... } or a list of them');
      cps.forEach((c, i) => {
        const at = `counterparty${Array.isArray(w.counterparty) ? `[${i}]` : ''}`;
        if (!isObj(c) || !['noise', 'informed', 'scripted'].includes(c.type)) { bad(at, 'type is "noise", "informed" or "scripted"'); return; }
        const known = { noise: ['type', 'turns', 'rate', 'reach', 'maxSize'], informed: ['type', 'turns', 'rate', 'edge', 'maxSize'], scripted: ['type', 'turns', 'trades'] }[c.type];
        Object.keys(c).forEach(f => { if (!known.includes(f)) bad(`${at}.${f}`, `not a field of a ${c.type} counterparty`); });
        if (c.rate != null && !(fin(c.rate) && c.rate > 0 && c.rate <= 1)) bad(`${at}.rate`, 'rate is a chance above 0 and at most 1');
        if (c.edge != null && !(fin(c.edge) && c.edge >= 0)) bad(`${at}.edge`, 'edge is a price distance, 0 or more');
        if (c.reach != null && !(fin(c.reach) && c.reach >= 0)) bad(`${at}.reach`, 'reach is a price distance, 0 or more');
        if (c.maxSize != null && !(fin(c.maxSize) && c.maxSize >= 1)) bad(`${at}.maxSize`, 'maxSize is a size, 1 or more');
        if (c.turns != null && (!Array.isArray(c.turns) || c.turns.length !== 2 || !c.turns.every(Number.isInteger) || c.turns[0] < 1 || c.turns[0] > c.turns[1] || (Number.isInteger(w.turns) && c.turns[1] > w.turns))) bad(`${at}.turns`, 'turns is [first, last], whole turn numbers from 1 to turns');
        if (c.type === 'scripted') {
          if (!Array.isArray(c.trades) || !c.trades.length) bad(`${at}.trades`, 'a scripted counterparty needs trades: [{ act: "hit" | "lift" | "none", size, price }], one per turn');
          else {
            if (Number.isInteger(w.turns) && c.trades.length > w.turns) bad(`${at}.trades`, `more trades (${c.trades.length}) than turns (${w.turns})`);
            c.trades.forEach((t, j) => { if (!isObj(t) || !['hit', 'lift', 'none'].includes(t.act) || (t.size != null && !(Number.isInteger(t.size) && t.size >= 1)) || (t.price != null && !fin(t.price))) bad(`${at}.trades[${j}]`, 'a scripted trade is { act: "hit" | "lift" | "none", size (whole, optional), price (optional limit) }'); });
          }
        }
      });
      if (w.schedule != null && !Array.isArray(w.schedule)) bad('schedule', 'schedule is a list of cards: { turn, text, fair, reveal }');
      (Array.isArray(w.schedule) ? w.schedule : []).forEach((c, i) => {
        if (!isObj(c) || !Number.isInteger(c.turn) || c.turn < 1 || (Number.isInteger(w.turns) && c.turn > w.turns)) { bad(`schedule[${i}].turn`, 'turn is a whole number from 1 to turns'); return; }
        Object.keys(c).forEach(f => { if (!['turn', 'text', 'fair', 'reveal'].includes(f)) bad(`schedule[${i}].${f}`, 'a card has turn, text, fair and reveal'); });
        if (c.fair != null && !fin(c.fair)) bad(`schedule[${i}].fair`, 'fair must be a number');
        if (c.reveal != null && typeof c.reveal !== 'boolean') bad(`schedule[${i}].reveal`, 'reveal is true or false');
        if (typeof c.text !== 'string' && c.reveal !== true) bad(`schedule[${i}].text`, 'a card needs text (or reveal: true)');
        text(c.text, `${where}.schedule[${i}].text`);
      });
      if (!Array.isArray(w.strategy) || !w.strategy.length) bad('strategy', 'strategy is required: [{ bid, ask, size }] one entry per turn, a run that meets the benchmark (the playthrough plays it)');
      else {
        if (Number.isInteger(w.turns) && w.strategy.length !== w.turns) bad('strategy', `strategy needs one entry per turn (${w.turns}), found ${w.strategy.length}`);
        w.strategy.forEach((x, i) => { if (!isObj(x) || !fin(x.bid) || !fin(x.ask) || !fin(x.size)) bad(`strategy[${i}]`, 'each entry is { bid, ask, size } with numbers'); });
      }
      if (ok) {
        const N = tradeSim.norm(w);
        if (fin(N.fair) && (N.range[0] > Math.min(N.fair, N.value) || N.range[1] < Math.max(N.fair, N.value))) warn(file, `${where}.range`, 'the price range does not cover both fair and value');
        const run = tradeSim.play(w, w.strategy);
        if (!run.verdict.ok) err(file, `${where}.strategy`, `the authored strategy does not meet the target (P&L ${run.verdict.pnl}, ${run.verdict.breaks} rule breaks, key "${run.verdict.key}"), so the playthrough could not pass it`);
        const dflt = tradeSim.play(w, null);
        if (dflt.verdict.ok) warn(file, where, 'leaving the opening quote untouched for every turn already meets the target, so the game checks nothing');
        const needsKeys = { low: true, high: hasBand, crossed: true, limit: N.limit < Infinity, spread: N.spreadMin != null || N.spreadMax != null };
        Object.entries(needsKeys).forEach(([k, on]) => { if (on) keys.add(k); });
        if (!canvas || canvas.kind !== 'orderbook') warn(file, where, 'the trade widget is built over an orderbook canvas');
      } else keys.add('*');
      break;
    }
    case 'tap-regions': {
      const countMode = w.count != null;
      if (w.ordered != null && typeof w.ordered !== 'boolean') err(file, `${where}.ordered`, 'ordered is true or false');
      if (w.ordered === true) { if (countMode) err(file, `${where}.ordered`, 'ordered grades the sequence of answer; it does not combine with count'); keys.add('order'); }
      if (countMode) {
        if (!Number.isInteger(w.count) || w.count < 1) err(file, `${where}.count`, 'count must be a whole number, at least 1');
        if (w.among != null && (!Array.isArray(w.among) || !w.among.length)) err(file, `${where}.among`, 'among must list region ids');
        else if (Array.isArray(w.among) && Number.isInteger(w.count) && w.count > w.among.length) err(file, `${where}.count`, `count ${w.count} is more than the ${w.among.length} regions in among`);
        ['too-few', 'too-many'].forEach(k => keys.add(k));
      } else if (!Array.isArray(w.answer) || !w.answer.length) err(file, `${where}.answer`, 'list the region ids that make up the answer (or give count, with optional among)');
      const known = regionIds(canvas);
      /* item 290: a grid's set names (row5, col3, cross2, cross5-3, all) stand for their cells in answer and among */
      const setName = (id) => isObj(canvas) && canvas.kind === 'grid' && (id === 'all' || /^(row|col|cross)\d+(-\d+)?$/.test(String(id)));
      if (known) (w.answer || []).forEach(id => { if (!known.has(id) && !setName(id)) err(file, `${where}.answer`, `region "${id}" is not on the ${canvas.kind} canvas`); });
      if (known && Array.isArray(w.among)) w.among.forEach(id => { if (!known.has(id) && !setName(id)) err(file, `${where}.among`, `region "${id}" is not on the ${canvas.kind} canvas`); });
      else if (!canvas) err(file, where, 'tap-regions needs a canvas');
      ids(w.wrong, 'wrong').forEach(k => keys.add(String(k)));
      (known || new Set()).forEach(k => keys.add(k));
      if (!known) keys.add('*');
      break;
    }
    case 'order': {
      const lines = ids(w.lines, 'lines');
      lines.forEach(k => keys.add(String(k)));
      const a = w.answer || [];
      /* engine pass (item 434): distractors lists lines that must be left out; answer is a permutation of the rest */
      let dis = [];
      if (w.distractors != null) {
        if (!Array.isArray(w.distractors) || !w.distractors.length || w.distractors.some(x => !lines.has(x)) || new Set(w.distractors).size !== w.distractors.length) err(file, `${where}.distractors`, 'distractors lists one or more line ids, each once');
        else { dis = w.distractors; keys.add('left-out'); }
      }
      if (!Array.isArray(a) || a.length !== lines.size - dis.length || new Set(a).size !== a.length || a.some(x => !lines.has(x) || dis.includes(x))) err(file, `${where}.answer`, dis.length ? 'answer must be a permutation of the line ids that are not distractors' : 'answer must be a permutation of the line ids');
      (w.lines || []).forEach((l, i) => text(l.text, `${where}.lines[${i}].text`));
      /* ENGINE-BACKLOG 616: after: { "line": ["earlier lines it must follow"] } */
      if (w.after != null) {
        if (!isObj(w.after) || !Object.keys(w.after).length) err(file, `${where}.after`, 'after is an object { lineId: [ids of lines that must come before it] }');
        else {
          for (const [k, v] of Object.entries(w.after)) {
            if (!lines.has(k) || dis.includes(k) || !Array.isArray(v) || !v.length || v.some(x => !lines.has(x) || dis.includes(x) || x === k)) err(file, `${where}.after.${k}`, 'a rule names a line (not a distractor) and a non-empty list of other lines (not distractors) that must come before it');
          }
          if (Array.isArray(a) && Object.entries(w.after).every(([k, v]) => Array.isArray(v))) {
            const bad = Object.entries(w.after).find(([k, v]) => a.indexOf(k) >= 0 && v.some(x => a.indexOf(x) > a.indexOf(k)));
            if (bad) err(file, `${where}.answer`, `the answer order breaks the after rule for "${bad[0]}": it must follow ${bad[1].join(', ')}`);
          }
          if (w.same != null) warn(file, `${where}.same`, 'same is ignored when after is set');
        }
      }
      if (w.same != null) { const gs = Array.isArray(w.same) && w.same.length && Array.isArray(w.same[0]) ? w.same : [w.same]; gs.forEach((g, i) => { if (!Array.isArray(g) || g.length < 2 || g.some(x => !lines.has(x))) err(file, `${where}.same[${i}]`, 'each same group lists two or more line ids'); }); }
      break;
    }
    case 'table': {
      if (!Array.isArray(w.columns) || !Array.isArray(w.rows)) { err(file, where, 'table needs columns and rows'); break; }
      let editable = 0;
      w.rows.forEach((r, i) => (r || []).forEach((c, j) => { if (isObj(c) && c.edit) { editable++; keys.add(`r${i}c${j}`); keys.add(`r${i + 1}c${j + 1}`); if (Array.isArray(c.wrong)) c.wrong.forEach(x => { if (isObj(x) && typeof x.id === 'string') keys.add(x.id); }); /* item 576: a cell's own wrong id is the key table.js returns */ if (Array.isArray(c.wrong)) { const ids = c.wrong.filter(x => isObj(x) && typeof x.id === 'string').map(x => x.id); if (ids.length) (keys.slip = keys.slip || new Map()).set(`r${i}c${j}`, ids); } /* item 584: cell id with wrong[] ids, for the dead-key warning */ if (typeof c.answer === 'string' && c.answer.trim() && !Number.isFinite(+c.answer)) { if (c.accept != null && !(Array.isArray(c.accept) && c.accept.every(x => typeof x === 'string'))) err(file, `${where}.rows[${i}][${j}].accept`, 'accept is a list of other spellings'); return; } /* item 118: a text answer, graded ignoring case */ if (typeof c.answer !== 'number') err(file, `${where}.rows[${i}][${j}].answer`, 'editable cell needs a numeric answer, or a text one such as "True"'); wrongCannotFire(file, `${where}.rows[${i}][${j}]`, c.answer, c.tol, c.wrong); if (c.tol) tol(c.tol, `${where}.rows[${i}][${j}].tol`); else err(file, `${where}.rows[${i}][${j}].tol`, 'editable cell needs a tol'); } }));
      if (!editable) err(file, `${where}.rows`, 'no editable cell');
      break;
    }
    case 'manipulate': {
      const S = w.states || {};
      if (!isObj(S) || !S[w.start]) { err(file, `${where}.start`, 'start must name a state'); break; }
      if (!S[w.target]) { err(file, `${where}.target`, 'target must name a state'); break; }
      Object.entries(S).forEach(([k, s]) => { keys.add(k); (s.ops || []).forEach((o, i) => { if (o && o.reject === true) { if (!o.why) err(file, `${where}.states.${k}.ops[${i}].why`, 'a refused step (reject: true) needs its why'); if (o.label != null) text(o.label, `${where}.states.${k}.ops[${i}].label`); return; } if (!S[o.to]) err(file, `${where}.states.${k}.ops[${i}].to`, `unknown state "${o.to}"`); text(o.label, `${where}.states.${k}.ops[${i}].label`); text(o.why, `${where}.states.${k}.ops[${i}].why`); }); });
      const seen = new Set([w.start]), q = [w.start];
      while (q.length) { const k = q.shift(); (S[k].ops || []).forEach(o => { if (o && !o.reject && S[o.to] && !seen.has(o.to)) { seen.add(o.to); q.push(o.to); } }); }
      if (!seen.has(w.target)) err(file, `${where}.target`, 'target is not reachable from start');
      break;
    }
    case 'balance': {
      req(file, where, w, ['left', 'right', 'target']);
      const MOVES = ['remove-both', 'remove-unknown-both', 'remove-unknown-part', 'halve-both', 'divide-both', 'subtract-both', 'add-both', 'remove-item'];
      (w.moves || []).forEach(m => { if (!MOVES.includes(m)) err(file, `${where}.moves`, `unknown move "${m}" (${MOVES.join(', ')})`); });
      /* The target must be reachable with the listed moves: the engine's own solver (js/engine/grade.js) decides */
      if (Array.isArray(w.left) && Array.isArray(w.right) && isObj(w.target) && ENGINE && ENGINE.balanceMoves) {
        let path = null; try { path = ENGINE.balanceMoves(w); } catch { path = null; }
        if (!path) err(file, `${where}.target`, 'the target cannot be reached from the pans with the listed moves (at most six)');
      }
      keys.add('*');
      break;
    }
    case 'sketch':
      req(file, where, w, ['target', 'xRange', 'band']);
      if (w.control != null && (typeof w.control !== 'number' || w.control < 2)) err(file, `${where}.control`, 'control must be a number of points, at least 2');
      keys.add('*');
      break;
    case 'code':
      req(file, where, w, ['language', 'starter']);
      /* item 304: language is "python" (Pyodide) or "cpp" (clang in the browser); a starter with #include is C++ */
      if (w.language != null && !['python', 'cpp'].includes(w.language)) err(file, `${where}.language`, 'language is "python" or "cpp"');
      if (typeof w.starter === 'string' && /^\s*#\s*include\b/m.test(w.starter) && w.language !== 'cpp') err(file, `${where}.language`, 'the starter has #include, so it is C++: set language: "cpp"');
      if (w.language === 'cpp') { cppCodeWidget(file, where, w); keys.add('*'); break; }
      if (!Array.isArray(w.tests) || w.tests.length < 3) err(file, `${where}.tests`, 'at least 3 tests');
      else if (w.tests.length > 15) err(file, `${where}.tests`, 'at most 15 tests');
      /* Item 109: a stdout case needs only expect (a string) and may carry stdin and exact; other cases need call */
      const codeCase = (t, at) => {
        if (!t || typeof t !== 'object') { err(file, at, 'each case is an object'); return; }
        const out = t.compare === 'stdout' || (t.call == null && t.expect != null && t.compare == null);
        if (t.compare && !['isclose', 'equal', 'fraction', 'stdout', 'raises'].includes(t.compare)) err(file, `${at}.compare`, 'compare is isclose, equal, fraction, stdout or raises');
        tolCase(file, at, t);
        if ((t.lines != null || t.match != null) && !out) err(file, at, 'lines and match apply to a stdout case');
        if (t.match != null) { try { new RegExp(String(t.match)); } catch (e) { err(file, `${at}.match`, `match is not a regular expression: ${e.message}`); } }
        if (t.setup != null && typeof t.setup !== 'string') err(file, `${at}.setup`, 'setup is a line of Python run before call ("prices = [100, 90]")');
        if (t.compare === 'raises') {
          if (typeof t.expect !== 'string' || !/^[A-Za-z_][\w.]*$/.test(t.expect.trim())) err(file, `${at}.expect`, 'a raises case names the exception: "ValueError"');
          if (t.call != null && typeof t.call !== 'string') err(file, `${at}.call`, 'call is a Python expression');
        } else if (out) {
          if (typeof t.expect !== 'string' && t.match == null) err(file, `${at}.expect`, 'a stdout case needs expect: the printed text, as a string ("Return: 5.00%\\n")');
          if (t.call != null) err(file, `${at}.call`, 'a stdout case has no call (it compares what the whole program prints)');
        } else if (t.call == null || t.expect == null) err(file, at, 'each test needs call and expect (or compare: "stdout" with expect)');
        if (t.stdin != null && typeof t.stdin !== 'string') err(file, `${at}.stdin`, 'stdin is a string, one line per input() call ("250\\n262.5\\n")');
        if (t.exact != null && typeof t.exact !== 'boolean') err(file, `${at}.exact`, 'exact is true or false');
        if (t.argv != null && !(Array.isArray(t.argv) && t.argv.every(x => typeof x === 'string' || typeof x === 'number'))) err(file, `${at}.argv`, 'argv is a list of strings, the words after python3 main.py');
        if (!out && t.compare == null && typeof t.call === 'string' && t.expect != null && FLOAT_EXPECT.test(String(t.expect)) && /\.examples\[/.test(at)) warn(file, `${at}.compare`, `[float-example] this example expects a float (${String(t.expect).slice(0, 40)}) with no compare, so "Run examples" compares exactly and can mark a correct float solution as failed; add "compare": "isclose"`);
        if (t.exact != null && !out) warn(file, `${at}.exact`, 'exact only applies to compare: "stdout"');
        if (typeof t.call === 'string' && /_getframe|f_locals\[/.test(t.call)) warn(file, `${at}.call`, 'reads the harness frame to get printed output; use { "compare": "stdout", "expect": "..." } instead (and printed in later calls)');
      };
      (w.tests || []).forEach((t, i) => codeCase(t, `${where}.tests[${i}]`));
      if (w.examples != null && !Array.isArray(w.examples)) err(file, `${where}.examples`, 'examples is a list of cases');
      else (w.examples || []).forEach((t, i) => codeCase(t, `${where}.examples[${i}]`));
      {
        const all = [...(Array.isArray(w.tests) ? w.tests : []), ...(Array.isArray(w.examples) ? w.examples : [])].filter(t => t && typeof t === 'object');
        const script = all.some(t => t.compare === 'stdout' || t.stdin != null || t.argv != null || (t.call == null && t.expect != null));
        // a raises case with no call checks the whole program, which needs script mode (it is on whenever such a case exists)
        if (!script && !all.some(t => typeof t.call === 'string' && /printed\s*:=/.test(t.call)) && all.some(t => typeof t.call === 'string' && /\bprinted\b/.test(t.call) && !/_getframe/.test(t.call))) err(file, `${where}.tests`, 'printed is only defined when a case uses compare: "stdout" or stdin (script mode)');
      }
      ['prelude', 'postlude'].forEach(k => { if (w[k] != null && typeof w[k] !== 'string') err(file, `${where}.${k}`, `${k} is Python source, a string`); });
      dataFiles(file, where, w);
      if (w.allocCheck != null) err(file, `${where}.allocCheck`, 'allocCheck is for C++ code items (language: "cpp")');
      if (w.budget != null && !(typeof w.budget === 'number' && w.budget >= 0 && w.budget <= 120000)) err(file, `${where}.budget`, 'budget is extra milliseconds for a run, 0 to 120000');
      if (w.caseBudget != null && !(typeof w.caseBudget === 'number' && w.caseBudget >= 0 && w.caseBudget <= 120000)) err(file, `${where}.caseBudget`, 'caseBudget is extra milliseconds for each case, 0 to 120000');
      if (!w.how) warn(file, `${where}.how`, 'say how it is checked');
      keys.add('*');
      break;
    case 'longform': checkLongform(file, where, w); keys.add('*'); break;
  }
  return keys;
};
const checkLongform = (file, where, x) => {
  req(file, where, x, ['prompt', 'model', 'rubric']);
  checkText(file, `${where}.prompt`, x.prompt); checkText(file, `${where}.model`, x.model);
  if (Array.isArray(x.rubric)) {
    const sum = x.rubric.reduce((a, r) => a + (Number(r.points) || 0), 0);
    if (sum !== 10) err(file, `${where}.rubric`, `rubric points must sum to 10 (found ${sum})`);
    x.rubric.forEach((r, i) => {
      checkText(file, `${where}.rubric[${i}].text`, r.text);
      if (r && r.required !== undefined && typeof r.required !== 'boolean') err(file, `${where}.rubric[${i}].required`, 'required must be true or false');
    });
    if (x.rubric.length && x.rubric.every(r => r && r.required === true)) warn(file, `${where}.rubric`, 'every rubric row is required: drop "required" from the rows that are not essential');
  }
};

/* space canvas (docs/AUTHORING.md section 4, README-B "space"): shapes and formula names only, never a crash */
const SPACE_LISTS = ['points', 'vectors', 'curves', 'lines', 'surfaces', 'planes', 'fields'];
const SPACE_FNS = new Set(['sin', 'cos', 'tan', 'exp', 'ln', 'log', 'log10', 'sqrt', 'abs', 'max', 'min', 'floor', 'ceil', 'pow', 'pi', 'e', 'atan', 'asin', 'acos', 'sinh', 'cosh', 'tanh', 'sign', 'round', 'fact', 'lgamma', 'erf', 'erfc', 'Phi', 'PhiInv', 'Phiinv', 'NormInv', 'normcdf', 'normpdf', 'pnorm', 'dnorm', 'qnorm']);
const checkSpace = (file, where, P, S) => {
  const E = (at, msg) => err(file, `${where}${at}`, msg);
  const num = (v) => typeof v === 'number' && Number.isFinite(v);
  const names = new Set(Object.keys({ ...(isObj(P.params) ? P.params : {}), ...(isObj(S.params) ? S.params : {}) }));
  /* a coordinate or formula: a number, or a string using only its variables, the params and the curve-formula functions */
  const formula = (v, at, vars = []) => {
    if (num(v)) return true;
    if (typeof v !== 'string' || !v.trim()) { E(at, 'a coordinate is a number or a formula string'); return false; }
    if (/\b(sum|prod)\s*\(/.test(v)) return true; // sum(k, a, b, term) binds its own name
    const bad = [...v.replace(/\d+\.?\d*(e[+-]?\d+)?/gi, ' ').matchAll(/[A-Za-z_]\w*/g)].map(m => m[0]).find(w => !SPACE_FNS.has(w) && !vars.includes(w) && !names.has(w));
    if (bad) { E(at, `unknown name "${bad}" in "${v}": a formula here may use ${vars.length ? vars.join(', ') + ', ' : ''}the params${[...names].length ? ' (' + [...names].join(', ') + ')' : ''} and the usual functions`); return false; }
    let d = 0; for (const ch of v) { if (ch === '(') d++; else if (ch === ')' && --d < 0) break; }
    if (d !== 0) { E(at, `unbalanced brackets in "${v}"`); return false; }
    return true;
  };
  const triple = (v, at, vars) => { if (!(Array.isArray(v) && v.length === 3)) { E(at, 'a point or vector is three coordinates [x, y, z] (numbers or formulas)'); return; } v.forEach((q, i) => formula(q, `${at}[${i}]`, vars)); };
  const pair = (v, at, what) => { if (!(Array.isArray(v) && v.length === 2)) { E(at, `${what} is [from, to]`); return; } v.forEach((q, i) => formula(q, `${at}[${i}]`)); };
  const slotOk = (v) => v == null || (Number.isInteger(v) && v >= 1 && v <= 6);
  ['x', 'y', 'z'].forEach(k => { if (P[k] != null && !(Array.isArray(P[k]) && P[k].length === 2 && P[k].every(num) && P[k][1] > P[k][0])) E(`.params.${k}`, `${k} is [min, max] with min below max`); });
  if (P.aspect != null && !(Array.isArray(P.aspect) && P.aspect.length === 3 && P.aspect.every(v => num(v) && v > 0))) E('.params.aspect', 'aspect is three positive numbers [x, y, z]');
  if (P.height != null && !(num(P.height) && P.height >= 240 && P.height <= 640)) E('.params.height', 'height is 240 to 640');
  [['params', P], ['state', S]].forEach(([w, o]) => { if (o.perspective != null && !(num(o.perspective) && o.perspective >= 0 && o.perspective <= 1)) E(`.${w}.perspective`, 'perspective is 0 (flat, the default) to 1'); });
  [['params', P], ['state', S]].forEach(([w, o]) => { if (o.grid != null && !['back', 'floor', false].includes(o.grid)) E(`.${w}.grid`, 'grid is "back", "floor" or false'); ['box', 'axes', 'ticks'].forEach(k => { if (o[k] != null && typeof o[k] !== 'boolean') E(`.${w}.${k}`, `${k} is true or false`); }); });
  if (P.axisLabels != null && !(Array.isArray(P.axisLabels) && P.axisLabels.length === 3 && P.axisLabels.every(v => typeof v === 'string'))) E('.params.axisLabels', 'axisLabels is three strings, such as ["$x_1$", "$x_2$", "$x_3$"]');
  [['params', P.camera], ['state', S.camera]].forEach(([w, cam]) => {
    if (cam == null) return;
    if (!isObj(cam)) { E(`.${w}.camera`, 'camera is { az, el, zoom } (degrees, degrees, 0.4 to 3)'); return; }
    if (cam.az != null && !num(cam.az)) E(`.${w}.camera.az`, 'az (azimuth) is a number of degrees');
    if (cam.el != null && !(num(cam.el) && cam.el >= -89 && cam.el <= 89)) E(`.${w}.camera.el`, 'el (elevation) is -89 to 89 degrees');
    if (cam.zoom != null && !(num(cam.zoom) && cam.zoom >= 0.4 && cam.zoom <= 3)) E(`.${w}.camera.zoom`, 'zoom is 0.4 to 3');
  });
  /* every list entry, from params (whole entries) and state (whole lists, or keyed patches by id) */
  const all = {}, seen = new Map();
  const entries = (k, src, at) => (Array.isArray(src[k]) ? src[k].map((q, i) => [q, `${at}.${k}[${i}]`, true]) : isObj(src[k]) ? Object.entries(src[k]).map(([id, q]) => [isObj(q) ? { id, ...q } : q, `${at}.${k}.${id}`, false]) : []);
  SPACE_LISTS.forEach(k => { all[k] = new Set(); [[P, '.params'], [S, '.state']].forEach(([src, at]) => entries(k, src, at).forEach(([q]) => { if (isObj(q) && q.id != null) all[k].add(String(q.id)); })); });
  SPACE_LISTS.forEach(k => [[P, '.params'], [S, '.state']].forEach(([src, at]) => {
    if (src[k] != null && !Array.isArray(src[k]) && !isObj(src[k])) E(`${at}.${k}`, `${k} is a list of objects with ids`);
    entries(k, src, at).forEach(([q, w, full]) => {
      if (q === null && !full) return; // a keyed patch removing an item
      if (!isObj(q)) { E(w, 'each entry is an object'); return; }
      if (full && (typeof q.id !== 'string' || !q.id)) E(`${w}.id`, 'every entry needs an id (a string), so hints, taps and patches can name it');
      else if (full && at === '.params') { if (seen.has(q.id)) E(`${w}.id`, `duplicate id "${q.id}" (also in ${seen.get(q.id)})`); else seen.set(q.id, `${k}`); }
      if (!slotOk(q.colour)) E(`${w}.colour`, 'colour is a slot 1 to 6');
      if (q.hidden != null && typeof q.hidden !== 'boolean') E(`${w}.hidden`, 'hidden is true or false (state.show: ["id"] reveals it)');
      const need = (cond, msg) => { if (full && !cond) E(w, msg); };
      if (k === 'points') {
        need(q.p != null || (q.x != null && q.y != null) || q.at != null, 'a point needs p: [x, y, z] (or x, y and z, or at and t on a curve)');
        if (q.p != null) triple(q.p, `${w}.p`); else ['x', 'y', 'z'].forEach(a => { if (q[a] != null) formula(q[a], `${w}.${a}`); });
        if (q.on != null && !all.surfaces.has(String(q.on))) E(`${w}.on`, `on names a surface id (one of ${[...all.surfaces].join(', ') || 'none defined'}); the point's z is read from it`);
        if (q.at != null && !all.curves.has(String(q.at))) E(`${w}.at`, `at names a curve id (one of ${[...all.curves].join(', ') || 'none defined'}); t is the parameter value`);
        if (q.at != null && q.t != null) formula(q.t, `${w}.t`);
        if (q.at != null && q.t == null) E(`${w}.t`, 'a point on a curve needs t');
        if (q.labelPos != null && !['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'].includes(q.labelPos)) E(`${w}.labelPos`, 'labelPos is a compass point: n, ne, e, se, s, sw, w or nw');
      } else if (k === 'vectors') {
        need(q.v != null, 'a vector needs v: [dx, dy, dz]');
        if (q.v != null) triple(q.v, `${w}.v`);
        if (q.from != null) { if (Array.isArray(q.from)) triple(q.from, `${w}.from`); else if (!all.points.has(String(q.from)) && !all.vectors.has(String(q.from))) E(`${w}.from`, 'from is [x, y, z] or the id of a point or another vector (a chain starts at its tip)'); }
        if (q.labelPos != null && !['end', 'mid'].includes(q.labelPos)) E(`${w}.labelPos`, 'labelPos is "end" or "mid"');
      } else if (k === 'curves') {
        need(typeof q.x === 'string' && typeof q.y === 'string', 'a curve needs x and y formulas in t (z too, for a space curve), and t: [from, to]');
        ['x', 'y', 'z'].forEach(a => { if (q[a] != null) formula(q[a], `${w}.${a}`, ['t']); });
        if (q.t != null) pair(q.t, `${w}.t`, 't'); else need(false, 'a curve needs t: [from, to]');
        if (q.n != null && !(Number.isInteger(q.n) && q.n >= 8 && q.n <= 600)) E(`${w}.n`, 'n is 8 to 600 samples');
      } else if (k === 'lines') {
        need(Array.isArray(q.pts) && q.pts.length >= 2, 'a line needs pts: at least two [x, y, z] points');
        if (Array.isArray(q.pts)) q.pts.forEach((p, i) => triple(p, `${w}.pts[${i}]`));
      } else if (k === 'surfaces') {
        const param = typeof q.x === 'string';
        if (param) { ['x', 'y', 'z'].forEach(a => { if (typeof q[a] !== 'string') E(`${w}.${a}`, 'a parametric surface has x, y and z formulas in u and v'); else formula(q[a], `${w}.${a}`, ['u', 'v']); }); if (q.u != null) pair(q.u, `${w}.u`, 'u'); if (q.v != null) pair(q.v, `${w}.v`, 'v'); need(q.u != null && q.v != null, 'a parametric surface needs u: [from, to] and v: [from, to]'); }
        else { need(typeof q.z === 'string', 'a surface needs z (a formula in x and y), or x, y and z formulas in u and v'); if (q.z != null) formula(q.z, `${w}.z`, ['x', 'y']); ['x', 'y'].forEach(a => { if (q[a] != null && !(Array.isArray(q[a]) && q[a].length === 2 && q[a].every(num) && q[a][1] > q[a][0])) E(`${w}.${a}`, `${a} is the range [min, max] the surface covers`); }); }
        if (q.n != null && !((Number.isInteger(q.n) && q.n >= 2 && q.n <= 40) || (Array.isArray(q.n) && q.n.length === 2 && q.n.every(v => Number.isInteger(v) && v >= 2 && v <= 40)))) E(`${w}.n`, 'n is 2 to 40 cells each way (or [nu, nv])');
        if (q.shade != null && !['light', 'flat', 'height'].includes(q.shade)) E(`${w}.shade`, 'shade is "light" (default), "flat" or "height"');
        if (q.wire != null && q.wire !== true && q.wire !== 'only' && q.wire !== false) E(`${w}.wire`, 'wire is true (edges over the shading) or "only" (hidden-line wireframe)');
        if (q.opacity != null && !(num(q.opacity) && q.opacity >= 0.05 && q.opacity <= 1)) E(`${w}.opacity`, 'opacity is 0.05 to 1');
        if (q.clip != null && !['clamp', 'drop', 'none'].includes(q.clip)) E(`${w}.clip`, 'clip is "clamp", "drop" or "none"');
        if (q.colour2 != null && !slotOk(q.colour2)) E(`${w}.colour2`, 'colour2 is a slot 1 to 6');
        if (q.labelAt != null && !(Array.isArray(q.labelAt) && q.labelAt.length === 2 && q.labelAt.every(num))) E(`${w}.labelAt`, 'labelAt is [x, y]');
      } else if (k === 'planes') {
        const sp = Array.isArray(q.span) ? q.span : null;
        need(sp || Array.isArray(q.normal), 'a plane needs span (one or two vectors: ids or [x, y, z]) or normal: [a, b, c] with through or d');
        if (sp && !(sp.length >= 1 && sp.length <= 2)) E(`${w}.span`, 'span is one vector (a line) or two (a plane)');
        (sp || []).forEach((e, i) => { if (Array.isArray(e)) triple(e, `${w}.span[${i}]`); else if (!all.vectors.has(String(e))) E(`${w}.span[${i}]`, `"${e}" is not a vector id on this canvas`); });
        if (q.normal != null) triple(q.normal, `${w}.normal`);
        if (q.through != null) triple(q.through, `${w}.through`);
        if (q.d != null) formula(q.d, `${w}.d`);
        if (q.extent != null && !(Array.isArray(q.extent) && [2, 4].includes(q.extent.length) && q.extent.every(num))) E(`${w}.extent`, 'extent is [lo, hi] (both coefficients) or [a0, a1, b0, b1], for a finite patch of a span');
        if (q.res != null && !(Number.isInteger(q.res) && q.res >= 3 && q.res <= 24)) E(`${w}.res`, 'res is 3 to 24 cells each way');
        if (q.opacity != null && !(num(q.opacity) && q.opacity >= 0.03 && q.opacity <= 1)) E(`${w}.opacity`, 'opacity is 0.03 to 1');
      } else if (k === 'fields') {
        need(Array.isArray(q.F) && q.F.length === 3, 'a field needs F: three formulas in x, y and z (the arrow at each grid point)');
        if (Array.isArray(q.F)) q.F.forEach((f, i) => formula(f, `${w}.F[${i}]`, ['x', 'y', 'z']));
        if (q.n != null && !((Number.isInteger(q.n) && q.n >= 1 && q.n <= 7) || (Array.isArray(q.n) && q.n.length === 3 && q.n.every(v => Number.isInteger(v) && v >= 1 && v <= 9)))) E(`${w}.n`, 'n is 1 to 7 arrows each way (or [nx, ny, nz], 1 to 9; the grid is capped at 343 arrows)');
        if (q.at != null && !(Array.isArray(q.at) && q.at.length === 3 && q.at.every(num))) E(`${w}.at`, 'at is [x, y, z]: where a one-arrow-deep grid sits');
        if (q.scale != null && !(num(q.scale) && q.scale > 0)) E(`${w}.scale`, 'scale is a positive number');
      }
    });
  }));
  [S.show, S.hide].forEach((l, i) => { if (l != null && !Array.isArray(l)) E(`.state.${i ? 'hide' : 'show'}`, `${i ? 'hide' : 'show'} is a list of ids`); });
};
const checkCanvas = (file, where, c) => {
  if (c == null) return;
  if (!isObj(c)) { err(file, where, 'canvas must be an object'); return; }
  if (c.kind === 'pair') {
    ['left', 'right'].forEach(k => { if (!isObj(c[k])) err(file, `${where}.${k}`, 'a pair needs a left and a right canvas'); else if (c[k].kind === 'pair') err(file, `${where}.${k}.kind`, 'a pair cannot hold a pair'); else checkCanvas(file, `${where}.${k}`, c[k]); });
    if (c.active != null && !['left', 'right'].includes(c.active)) err(file, `${where}.active`, 'active is "left" or "right"');
  }
  if (!CANVASES.has(c.kind)) err(file, `${where}.kind`, `unknown canvas kind "${c.kind}"`);
  if (c.kind === 'table' && isObj(c.params)) {   // ENGINE-BACKLOG 611: shown cells get the artefact checks (a table cell is not run through checkText)
    (Array.isArray(c.params.rows) ? c.params.rows : []).forEach((r, i) => (Array.isArray(r) ? r : []).forEach((v, j) => { const t = typeof v === 'string' ? v : isObj(v) && typeof v.text === 'string' ? v.text : null; if (t) floatArtefacts(file, `${where}.params.rows[${i}][${j}]`, t); }));
  }
  if (c.params != null && !isObj(c.params)) err(file, `${where}.params`, 'must be an object');
  if (c.state != null && !isObj(c.state)) err(file, `${where}.state`, 'must be an object');
  /* pass 3 canvas options (items 89 to 107): shapes only, never a crash */
  const P = isObj(c.params) ? c.params : {}, S = isObj(c.state) ? c.state : {};
  const slotOk = (v) => v == null || (Number.isInteger(+v) && +v >= 1 && +v <= 6);
  if (c.kind === 'space') checkSpace(file, where, P, S);
  if (c.kind === 'grid') {
    if (P.rowOffsets != null && !(Array.isArray(P.rowOffsets) && P.rowOffsets.every(v => typeof v === 'number' && v >= 0))) err(file, `${where}.params.rowOffsets`, 'rowOffsets is a list of offsets in cell widths, one per row, 0 or more');
    if (S.cells != null && !Array.isArray(S.cells) && !isObj(S.cells)) err(file, `${where}.state.cells`, 'state.cells is { "r1c2": "5" } or a 2D array of strings');
    if (isObj(S.shade)) Object.entries(S.shade).forEach(([k, v]) => { if (isObj(v) && (!Array.isArray(v.ids || v.cells) || !slotOk(v.colour))) err(file, `${where}.state.shade.${k}`, 'a coloured set is { "ids": [...], "colour": 1 to 6 }'); });
    if (S.paths != null) {
      const list = Array.isArray(S.paths) ? S.paths : isObj(S.paths) ? Object.entries(S.paths).map(([id, v]) => (Array.isArray(v) ? { id, cells: v } : { id, ...(isObj(v) ? v : {}) })) : null;
      if (!list) err(file, `${where}.state.paths`, 'paths is a list of { id, cells: [ids], colour } or a map from id to cell ids');
      else list.forEach((q, i) => { if (!isObj(q) || !Array.isArray(q.cells) || q.cells.length < 2) err(file, `${where}.state.paths[${i}]`, 'a path needs cells: at least two cell ids'); else if (!slotOk(q.colour)) err(file, `${where}.state.paths[${i}].colour`, 'colour is a slot 1 to 6'); else if (P.rows && P.cols) q.cells.forEach(id => { const m = String(id).match(/^r(\d+)c(\d+)$/); if (!m || +m[1] < 1 || +m[1] > P.rows || +m[2] < 1 || +m[2] > P.cols) err(file, `${where}.state.paths[${i}].cells`, `no cell "${id}" in a ${P.rows} by ${P.cols} grid`); }); });
    }
  }
  if (c.kind === 'graph') {
    if (P.layout != null && P.layout !== 'ring') err(file, `${where}.params.layout`, 'layout is "ring" (or leave it out and give each node x and y)');
    if (S.labels != null && !isObj(S.labels)) err(file, `${where}.state.labels`, 'labels maps node ids to new labels');
    if (S.rotate != null && typeof S.rotate !== 'number') err(file, `${where}.state.rotate`, 'rotate is a number of seats');
  }
  /* pass 4 options: shapes only */
  const listOf = (v) => Array.isArray(v) ? v : [];
  if (c.kind === 'plane') {
    listOf(P.functions).forEach((f, i) => {
      if (!isObj(f)) return;
      /* items 430, 459, 446, 461, 469, 460: contour, heat, exprs with index, points (a polyline), steps and cells are function entries too */
      const fam = f.expr != null || (f.x != null && f.y != null) || f.implicit != null || f.contour != null || f.heat != null || Array.isArray(f.exprs) || Array.isArray(f.points) || f.steps != null || isObj(f.cells) || isObj(f.grid) || Array.isArray(f.pointsList);
      if (!fam) err(file, `${where}.params.functions[${i}]`, 'a function needs expr (or exprs with index), x and y (parametric, with t: [from, to]), implicit, contour (with levels), heat, points (a polyline), steps or cells');
      if (Array.isArray(f.exprs) && f.index == null) err(file, `${where}.params.functions[${i}].index`, 'exprs needs index: the param (or a number) that picks one');
      if (Array.isArray(f.exprs)) f.exprs.forEach((e, k) => { if (typeof e !== 'string' && typeof e !== 'number') err(file, `${where}.params.functions[${i}].exprs[${k}]`, 'each entry of exprs is a formula'); });
      if (Array.isArray(f.points) && !f.points.every(q => Array.isArray(q) && q.length === 2 && q.every(v => typeof v === 'number'))) err(file, `${where}.params.functions[${i}].points`, 'points is a list of [x, y] pairs');
      if (f.steps != null && ![].concat(f.steps).every(q => isObj(q) && Array.isArray(q.levels) && (q.at == null || Array.isArray(q.at)) && (q.at || []).length + 1 === q.levels.length)) err(file, `${where}.params.functions[${i}].steps`, 'steps is { at: [breaks], levels: [one more than the breaks] } (or a list of them, with index)');
      if (isObj(f.cells) && !(Array.isArray(f.cells.values) && f.cells.values.every(r => Array.isArray(r)))) err(file, `${where}.params.functions[${i}].cells`, 'cells is { x: [x0, x1], y: [y0, y1], values: [[...], ...] } with values[0] the bottom row');
      if (f.contour != null && f.levels != null && !Array.isArray(f.levels)) err(file, `${where}.params.functions[${i}].levels`, 'levels is a list of numbers');
      if (f.holes != null && !(Array.isArray(f.holes) && f.holes.every(x => typeof x === 'number'))) err(file, `${where}.params.functions[${i}].holes`, 'holes is a list of x values');
      if (f.t != null && !(Array.isArray(f.t) && f.t.length === 2 && f.t.every(x => typeof x === 'number'))) err(file, `${where}.params.functions[${i}].t`, 't is [from, to]');
    });
    listOf(S.points).forEach((q, i) => { if (isObj(q) && q.tap != null && typeof q.tap !== 'boolean') err(file, `${where}.state.points[${i}].tap`, 'tap is true or false'); if (isObj(q) && q.trace != null && ![true, false, 'x'].includes(q.trace)) err(file, `${where}.state.points[${i}].trace`, 'trace is true (the path as it went) or "x" (sorted by x)'); });
    /* item 431: field, slopeField and trajectory layers on a plane (in params or state; an object or a list of objects) */
    {
      const COLOURS = ['ink', 'manip', 'hint', 'neg', 'pos', 'muted'], colourOk = (v) => v == null || slotOk(v) || COLOURS.includes(v);
      const num = (v, lo, hi) => typeof v === 'number' && Number.isFinite(v) && v >= lo && v <= hi, pair = (v) => Array.isArray(v) && v.length === 2 && v.every((x) => typeof x === 'number');
      const exprOk = (v) => typeof v === 'string' || typeof v === 'number';
      const merged = (key) => { // as the engine does: a state entry merges over the params entry with the same id
        const m = new Map();
        [['params', P], ['state', S]].forEach(([w, o]) => {
          if (o[key] == null) return;
          const list = Array.isArray(o[key]);
          [].concat(o[key]).forEach((q, i) => {
            const at = `${where}.${w}.${key}${list ? `[${i}]` : ''}`;
            if (!isObj(q)) { err(file, at, `${key} is an object (or a list of objects)`); return; }
            const id = q.id != null ? String(q.id) : i ? `${key}-${i}` : key;
            m.set(id, { ...(m.get(id) || {}), ...q, id, at });
          });
        });
        return m;
      };
      const fields = merged('field'), slopes = merged('slopeField'), trajs = merged('trajectory'), known = new Set([...fields.keys(), ...slopes.keys()]);
      const common = (q) => {
        if (q.grid != null && !(Array.isArray(q.grid) ? q.grid.length === 2 && q.grid.every((n) => num(n, 2, 60)) : num(q.grid, 2, 60))) err(file, `${q.at}.grid`, 'grid is a number of columns (2 to 60) or [columns, rows]');
        if (q.spacing != null && !(Array.isArray(q.spacing) ? q.spacing.length === 2 && q.spacing.every((n) => num(n, 1e-9, Infinity)) : num(q.spacing, 1e-9, Infinity))) err(file, `${q.at}.spacing`, 'spacing is a positive step in data units, or [dx, dy]');
        if (q.length != null && !num(q.length, 1e-9, Infinity)) err(file, `${q.at}.length`, 'length is a positive number (px for arrows and segments; the range of the variable for a trajectory)');
        if (q.maxArrows != null && !num(q.maxArrows, 4, 600)) err(file, `${q.at}.maxArrows`, 'maxArrows is 4 to 600');
        if (q.colourBy != null && q.colourBy !== 'magnitude' && q.colourBy !== true) err(file, `${q.at}.colourBy`, 'colourBy is "magnitude"');
        if (q.range != null && !(pair(q.range) && q.range[0] < q.range[1])) err(file, `${q.at}.range`, 'range is [lo, hi] with lo below hi');
        if (q.anchor != null && !['mid', 'tail'].includes(q.anchor)) err(file, `${q.at}.anchor`, 'anchor is "mid" or "tail"');
        if (q.normalise != null && typeof q.normalise !== 'boolean') err(file, `${q.at}.normalise`, 'normalise is true or false');
        if (!colourOk(q.colour) || !colourOk(q.colourHigh)) err(file, `${q.at}.colour`, 'colour and colourHigh are a slot 1 to 6 or ink, manip, hint, neg, pos, muted');
      };
      fields.forEach((q) => { ['P', 'Q'].forEach((k) => { if (!exprOk(q[k])) err(file, `${q.at}.${k}`, `a field needs P and Q: formulas in x, y and the params`); }); common(q); });
      slopes.forEach((q) => { if (!exprOk(q.f)) err(file, `${q.at}.f`, 'a slopeField needs f: the slope dy/dx as a formula in x, y and the params'); common(q); });
      const ptIds = new Set(listOf(S.points).filter(isObj).map((p) => String(p.id)));
      trajs.forEach((q) => {
        const startOk = (v) => (typeof v === 'string' && v !== '') || (pair(v));
        if (q.from == null && q.starts == null) err(file, q.at, 'a trajectory needs from (a point id or [x, y]) or starts (a list of them)');
        if (q.from != null && !startOk(q.from)) err(file, `${q.at}.from`, 'from is a point id or [x, y]');
        if (q.starts != null && !(Array.isArray(q.starts) && q.starts.length >= 1 && q.starts.length <= 24 && q.starts.every(startOk))) err(file, `${q.at}.starts`, 'starts is a list of 1 to 24 point ids or [x, y] pairs');
        [].concat(q.from ?? [], Array.isArray(q.starts) ? q.starts : []).forEach((s) => { if (typeof s === 'string' && !ptIds.has(s)) warn(file, `${q.at}`, `"${s}" is not a point id in state.points (a later patch may add it)`); });
        if (!known.size) err(file, q.at, 'a trajectory needs a field or slopeField layer to run in');
        else if (q.in != null && !known.has(String(q.in))) err(file, `${q.at}.in`, `in names a field or slopeField id (${[...known].join(', ')})`);
        if (q.step != null && !num(q.step, 1e-12, Infinity)) err(file, `${q.at}.step`, 'step is a positive number');
        if (q.length != null && !num(q.length, 1e-9, Infinity)) err(file, `${q.at}.length`, 'length is a positive number');
        if (q.back != null && typeof q.back !== 'boolean' && !num(q.back, 0, Infinity)) err(file, `${q.at}.back`, 'back is true (as far as length) or a length');
        if (q.by != null && !['arc', 'time'].includes(q.by)) err(file, `${q.at}.by`, 'by is "time" (the default; x for a slope field) or "arc" (length along the curve)');
        if (q.maxSteps != null && !(Number.isInteger(q.maxSteps) && q.maxSteps >= 10 && q.maxSteps <= 5000)) err(file, `${q.at}.maxSteps`, 'maxSteps is a whole number from 10 to 5000');
        ['arrow', 'dashed'].forEach((k) => { if (q[k] != null && typeof q[k] !== 'boolean') err(file, `${q.at}.${k}`, `${k} is true or false`); });
        if (!colourOk(q.colour)) err(file, `${q.at}.colour`, 'colour is a slot 1 to 6 or ink, manip, hint, neg, pos, muted');
      });
    }
  }
  if (c.kind === 'series') {
    if (P.y2 != null && !(Array.isArray(P.y2) && P.y2.length === 2)) err(file, `${where}.params.y2`, 'y2 is [min, max] for the right-hand axis');
    if (P.dateFormat != null && typeof P.dateFormat !== 'string') err(file, `${where}.params.dateFormat`, 'dateFormat is a string such as "%b %Y"');
    if (P.margins != null && !isObj(P.margins)) err(file, `${where}.params.margins`, 'margins is { left, right } in px');
    listOf(P.series).forEach((q, i) => { if (isObj(q) && q.axis != null && ![1, 2].includes(q.axis)) err(file, `${where}.params.series[${i}].axis`, 'axis is 1 or 2'); });
  }
  if (c.kind === 'bars') {
    if (P.data != null && !(Array.isArray(P.data) && P.data.every(x => typeof x === 'number'))) err(file, `${where}.params.data`, 'data is a list of numbers (raw observations)');
    if (P.data != null && !isObj(P.bins)) err(file, `${where}.params.data`, 'data needs bins: { min, max, width }');
    if (P.truncate && typeof P.yMin !== 'number') err(file, `${where}.params.truncate`, 'truncate needs a yMin');
  }
  if (c.kind === 'pair') {
    if (c.tap != null && c.tap !== 'sides') err(file, `${where}.tap`, 'tap is "sides" (each side one tappable object, ids left and right)');
  }
  if (c.kind === 'number-line') listOf(S.arrows).forEach((q, i) => { if (isObj(q) && q.side != null && !['above', 'below'].includes(q.side)) err(file, `${where}.state.arrows[${i}].side`, 'side is "above" or "below"'); });
  if (c.kind === 'graph') listOf(P.nodes).forEach((q, i) => { if (isObj(q) && q.shape != null && !['circle', 'pill', 'rect', 'diamond'].includes(q.shape)) err(file, `${where}.params.nodes[${i}].shape`, 'shape is circle, pill, rect or diamond'); });
  if (['area', 'table'].includes(c.kind) && S.dim != null && !Array.isArray(S.dim)) err(file, `${where}.state.dim`, 'dim is a list of ids');
  /* item 471: interleave, lanes of steps over shared variables; the engine checks names, locks, expressions, state.schedule and the enumeration limit */
  if (c.kind === 'interleave') {
    const r = interleaveEngine.check(isObj(c.params) ? c.params : null, S);
    r.errors.forEach(x => err(file, `${where}.${x.at}`.replace(/\.$/, ''), x.msg));
    r.warnings.forEach(x => warn(file, `${where}.${x.at}`.replace(/\.$/, ''), x.msg));
    if (isObj(c.enter) && c.enter.schedule != null && !r.errors.length) interleaveEngine.check(c.params, { schedule: c.enter.schedule }).errors.forEach(x => err(file, `${where}.enter.${x.at.replace(/^state\./, '')}`, x.msg));
  }
  if (c.kind === 'console' && P.lines == null && typeof P.text !== 'string') err(file, `${where}.params`, 'a console needs lines (a list of strings) or text');
  if (c.kind === 'console' && P.lines != null && !(Array.isArray(P.lines) && P.lines.every(l => typeof l === 'string'))) err(file, `${where}.params.lines`, 'lines is a list of strings, one per line');
  if (c.kind === 'table' && P.tap != null && P.tap !== 'rows') err(file, `${where}.params.tap`, 'tap is "rows" (or leave it out to tap cells)');
  if (c.kind === 'tree' && S.current != null && typeof S.current !== 'string') err(file, `${where}.state.current`, 'current is a branch path such as "a-b", or "root"');
  if (c.kind === 'vectors' && P.points != null && !(Array.isArray(P.points) && P.points.every(q => isObj(q) && typeof q.x === 'number' && typeof q.y === 'number'))) err(file, `${where}.params.points`, 'points is a list of { id, x, y, label }');
  /* item 435: vectors state.matrix [[a, b], [c, d]] (or transform { angle, shear, scale }) moves every vector not marked fixed: true */
  if (c.kind === 'vectors') {
    const okNum = (v) => typeof v === 'number' && Number.isFinite(v);
    if (S.matrix != null && !(Array.isArray(S.matrix) && S.matrix.length === 2 && S.matrix.every(r => Array.isArray(r) && r.length === 2 && r.every(okNum)))) err(file, `${where}.state.matrix`, 'matrix is [[a, b], [c, d]], four numbers (a derive may write it: "matrix": "[[a, b], [c, d]]")');
    if (S.transform != null && !(isObj(S.transform) && Object.values(S.transform).every(okNum))) err(file, `${where}.state.transform`, 'transform is { angle (degrees), shear, scale }, all numbers');
    [...listOf(P.vectors), ...listOf(S.vectors)].forEach((v, i) => { if (isObj(v) && v.fixed != null && typeof v.fixed !== 'boolean') err(file, `${where}.vectors[${i}].fixed`, 'fixed is true or false (true: the matrix does not move this vector)'); });
  }
  /* item 432: complex-map, a z-plane beside the w-plane image of f(z) */
  if (c.kind === 'complex-map') {
    const okNum = (v) => typeof v === 'number' && Number.isFinite(v);
    ['x', 'y', 'wx', 'wy'].forEach(k => { if (P[k] != null && !(Array.isArray(P[k]) && P[k].length === 2 && P[k].every(okNum) && P[k][0] < P[k][1])) err(file, `${where}.params.${k}`, `${k} is [min, max] with min below max`); });
    [['params', P.grid], ['state', S.grid]].forEach(([w, v]) => { if (v != null && !['cartesian', 'polar', 'both', 'none'].includes(v)) err(file, `${where}.${w}.grid`, 'grid is "cartesian", "polar", "both" or "none"'); });
    ['gridStep', 'rStep'].forEach(k => { [['params', P[k]], ['state', S[k]]].forEach(([w, v]) => { if (v != null && !(okNum(v) && v > 0)) err(file, `${where}.${w}.${k}`, `${k} is a number above 0`); }); });
    [['params', P.rays], ['state', S.rays]].forEach(([w, v]) => { if (v != null && !(Number.isInteger(v) && v >= 0)) err(file, `${where}.${w}.rays`, 'rays is a whole number, 0 or more'); });
    [['params', P.unitCircle], ['state', S.unitCircle], ['params', P.stack]].forEach(([w, v], i) => { if (v != null && typeof v !== 'boolean') err(file, `${where}.${w}.${i === 2 ? 'stack' : 'unitCircle'}`, 'true or false'); });
    const named = { ...(isObj(P.params) ? P.params : {}), ...(isObj(S.params) ? S.params : {}) };
    Object.entries(named).forEach(([k, v]) => { if (!(okNum(v) || (Array.isArray(v) && v.length === 2 && v.every(okNum)))) err(file, `${where}.params.params.${k}`, 'a name in f is a number (or [re, im])'); if (!/^[A-Za-z_][A-Za-z_0-9]*$/.test(k) || ['z', 'i', 'e', 'pi'].includes(k)) err(file, `${where}.params.params.${k}`, 'a name in f is letters, digits and _, and not z, i, e or pi'); });
    const names = ['z', ...Object.keys(named).filter(k => k !== 'z')];
    [['params.f', P.f], ['state.f', S.f]].forEach(([w, v]) => { if (v == null) return; if (typeof v !== 'string') { err(file, `${where}.${w}`, 'f is a formula in z, such as "(z - 1)/(z + 1)"'); return; } try { cmap.compile(v, names); } catch (er) { err(file, `${where}.${w}`, `f does not read: ${er.message}`); } });
    [['params', P.curves], ['state', S.curves]].forEach(([w, list]) => listOf(list).forEach((q, i) => {
      if (!isObj(q)) return;
      if (typeof q.z !== 'string') err(file, `${where}.${w}.curves[${i}].z`, 'a curve is { z: "formula in t", t: [from, to] }');
      else { try { cmap.compile(q.z, ['t', ...names.filter(k => k !== 'z')]); } catch (er) { err(file, `${where}.${w}.curves[${i}].z`, `does not read: ${er.message}`); } }
      if (q.t != null && !(Array.isArray(q.t) && q.t.length === 2 && q.t.every(okNum))) err(file, `${where}.${w}.curves[${i}].t`, 't is [from, to]');
    }));
    [['params', P.points], ['state', S.points]].forEach(([w, list]) => listOf(list).forEach((q, i) => { if (isObj(q) && !(okNum(q.x) && okNum(q.y))) err(file, `${where}.${w}.points[${i}]`, 'a point is { id, x, y, label, drag }: x and y are the real and imaginary parts of z'); }));
  }
  (c.controls || []).forEach((k, i) => {
    if (!k.bind && !k.reseed && k.frames == null) err(file, `${where}.controls[${i}].bind`, 'required');
    if (k.frames != null && !(Array.isArray(k.frames) && k.frames.length >= 2 && k.frames.every(isObj))) err(file, `${where}.controls[${i}].frames`, 'frames is a list of at least two state patches');
    else (k.frames || []).forEach((f, j) => wholeCanvasPatch(file, `${where}.controls[${i}].frames[${j}]`, f));
    if (k.format != null && !['fraction', 'percent'].includes(k.format)) err(file, `${where}.controls[${i}].format`, 'format is "fraction" or "percent"');
    if (k.scale != null && k.scale !== 'log') err(file, `${where}.controls[${i}].scale`, 'scale is "log" (or leave it out for a linear slider)');
    if (k.scale === 'log' && !(+k.min > 0 && +k.max > +k.min)) err(file, `${where}.controls[${i}]`, 'a log slider needs 0 < min < max (stops at powers of ten from min)');
    /* items 357, 462: stops (a list of values) and options (a categorical control binding the index) */
    if (k.stops != null && !(Array.isArray(k.stops) && k.stops.length >= 2 && k.stops.every(v => typeof v === 'number'))) err(file, `${where}.controls[${i}].stops`, 'stops is a list of at least two numbers');
    if (k.options != null && !(Array.isArray(k.options) && k.options.length >= 2 && k.options.every(v => typeof v === 'string' || typeof v === 'number'))) err(file, `${where}.controls[${i}].options`, 'options is a list of at least two labels; the control binds the index 0, 1, ...');
    if (k.options != null && k.stops != null) err(file, `${where}.controls[${i}]`, 'a control has stops or options, not both');
  });
  if (c.maxHeight != null && !(typeof c.maxHeight === 'number' && c.maxHeight >= 120)) err(file, `${where}.maxHeight`, 'maxHeight is a number of pixels, 120 or more');
  /* item 326: a bars sim reads params and state.params by name; series sims read params */
  if (c.kind === 'bars' && isObj(P.sim)) checkSim(file, `${where}.params.sim`, P.sim, Object.keys({ ...(P.params || {}), ...(S.params || {}) }));
  if (c.kind === 'series') listOf(P.series).forEach((q, i) => { if (isObj(q) && isObj(q.sim)) checkSim(file, `${where}.params.series[${i}].sim`, q.sim, Object.keys(P.params || {})); });
  if (c.kind === 'distribution' && P.family != null && !['binomial', 'geometric', 'poisson', 'uniform', 'exponential', 't', 'normal', 'hypergeometric', 'discrete', 'custom', 'lognormal', 'beta'].includes(P.family)) err(file, `${where}.params.family`, 'family is binomial, geometric, poisson, hypergeometric, discrete, uniform, normal, lognormal, beta, exponential or t');
  if (c.kind === 'distribution' && ['discrete', 'custom'].includes(P.family)) { const v = P.values ?? (P.params || {}).values, pr = P.probs ?? (P.params || {}).probs; if (!Array.isArray(v) || !v.length) err(file, `${where}.params.values`, 'a discrete family lists its values'); else if (Array.isArray(pr) && Math.abs(pr.reduce((t, x) => t + +x, 0) - 1) > 1e-6) warn(file, `${where}.params.probs`, 'the probabilities do not add to 1'); }
  /* item 436: walk overlays, the average at stopping, slider-bound barriers and the mean-reverting model */
  if (c.kind === 'walk') {
    const num = (v) => typeof v === 'number' && Number.isFinite(v);
    if (P.model != null && !['coin', 'normal', 'markov', 'ou', 'mean-reverting', 'ar1'].includes(P.model)) err(file, `${where}.params.model`, 'model is coin, normal, markov, ou (also mean-reverting or ar1)');
    ['theta', 'stopAt', 'stake', 'fraction', 'bankroll', 'maxBet', 'overlayHeight', 'drawn'].forEach(k => { if (P[k] != null && !(num(P[k]) && P[k] >= 0)) err(file, `${where}.params.${k}`, `${k} is a number, 0 or more`); });
    ['lower', 'upper'].forEach(k => { if (P[k] != null && !num(P[k])) err(file, `${where}.params.${k}`, `${k} is a number (a barrier level; a slider may bind it)`); });
    if (num(P.lower) && num(P.upper) && P.lower >= P.upper) err(file, `${where}.params`, 'lower must be below upper');
    if (P.bet != null && !['fixed', 'double', 'fraction'].includes(P.bet)) err(file, `${where}.params.bet`, 'bet is "fixed", "double" or "fraction"');
    if (P.model === 'ou' || P.model === 'mean-reverting' || P.model === 'ar1') { if (P.p != null || P.step != null) warn(file, `${where}.params`, 'a mean-reverting walk reads theta, mu, sigma and start; p and step are ignored'); }
    const ids = [];
    if (P.overlays != null) {
      if (!Array.isArray(P.overlays)) err(file, `${where}.params.overlays`, 'overlays is a list of "sq", "ratio", "bankroll" or objects { id, type, label, chip, colour, y, expr }');
      else P.overlays.forEach((o, i) => {
        const w = `${where}.params.overlays[${i}]`, ob = isObj(o) ? o : { id: o }, type = ob.type || (ob.expr ? 'expr' : ob.id);
        if (typeof o !== 'string' && !isObj(o)) { err(file, w, 'an overlay is an id string or an object'); return; }
        if (!['sq', 'ratio', 'bankroll', 'expr'].includes(type)) err(file, w, 'an overlay is "sq", "ratio" or "bankroll", or has an expr (type "expr")');
        if (type === 'expr' && typeof ob.expr !== 'string') err(file, `${w}.expr`, 'an expr overlay needs a formula in S, n, x, p, q, start, step and the numeric params');
        if (type === 'expr' && typeof ob.expr === 'string') { try { new Function('F', 'x', 'S', 'n', 'p', 'q', 'start', 'step', 'mu', 'sigma', 'theta', 'return (' + ob.expr.replace(/\^/g, '**') + ');'); } catch { err(file, `${w}.expr`, 'the formula does not parse'); } }
        if (type === 'expr' && !ob.id) warn(file, w, 'give an expr overlay an id (it names the chip, the highlight id ov-<id> and showStopped)');
        if (ob.bet != null && !['fixed', 'double', 'fraction'].includes(ob.bet)) err(file, `${w}.bet`, 'bet is "fixed", "double" or "fraction"');
        if (ob.y != null && !(Array.isArray(ob.y) && ob.y.length === 2 && ob.y.every(num))) err(file, `${w}.y`, 'y is [min, max] for the overlay panel');
        if (ob.colour != null && !(Number.isInteger(ob.colour) && ob.colour >= 1 && ob.colour <= 6)) err(file, `${w}.colour`, 'colour is a series slot, 1 to 6');
        const id = String(ob.id || type); if (ids.includes(id)) err(file, w, `two overlays share the id "${id}"`); ids.push(id);
      });
      if (P.model === 'markov') warn(file, `${where}.params.overlays`, 'overlays are not drawn for a markov walk');
      if (P.model === 'normal' || P.model === 'ou' || P.model === 'mean-reverting' || P.model === 'ar1') { if ((P.overlays || []).some(o => (isObj(o) ? o.type || o.id : o) === 'ratio') && (P.model !== 'normal')) warn(file, `${where}.params.overlays`, 'the ratio overlay is defined for the coin and normal models only'); }
    }
    const known = (id) => id === 'walk' || ids.includes(id);
    if (S.overlays != null && typeof S.overlays !== 'boolean' && !(Array.isArray(S.overlays) && S.overlays.every(x => typeof x === 'string'))) err(file, `${where}.state.overlays`, 'overlays is true, false or a list of overlay ids');
    if (Array.isArray(S.overlays)) S.overlays.forEach(id => { if (typeof id === 'string' && !ids.includes(id)) err(file, `${where}.state.overlays`, `no overlay "${id}" in params.overlays`); });
    if (S.showStopped != null) {
      const list = S.showStopped === true ? ['walk'] : [].concat(S.showStopped);
      if (S.showStopped !== false && !list.every(x => typeof x === 'string')) err(file, `${where}.state.showStopped`, 'showStopped is true ("walk"), an overlay id, or a list of them');
      else list.forEach(id => { if (!known(id)) err(file, `${where}.state.showStopped`, `"${id}" is not "walk" or an overlay id`); });
      if (S.showStopped !== false && !(Array.isArray(P.barriers) || P.lower != null || P.upper != null || P.stopAt != null)) warn(file, `${where}.state.showStopped`, 'showStopped without barriers or stopAt averages the value at the last step');
      if (S.showStopped !== false && !(num(P.paths) && P.paths >= 2)) warn(file, `${where}.params.paths`, 'the average at stopping needs several paths (use 100 or more, and drawn to draw fewer)');
    }
    if (S.bet != null && !['fixed', 'double', 'fraction'].includes(S.bet)) err(file, `${where}.state.bet`, 'bet is "fixed", "double" or "fraction"');
    if (Array.isArray(P.barriers) && (num(P.lower) || num(P.upper))) warn(file, `${where}.params`, 'lower and upper replace the matching entry of barriers');
  }
  if (c.kind === 'walk' && P.model === 'markov' && !(Array.isArray(P.states) && Array.isArray(P.P) && P.P.length === P.states.length)) err(file, `${where}.params`, 'a markov walk needs states and a P matrix with one row per state');
  if (c.kind === 'number-line' && P.scale != null && !['log', 'log-odds'].includes(P.scale)) err(file, `${where}.params.scale`, 'scale is "log" or "log-odds"');
  if (c.kind === 'number-line' && P.scale === 'log-odds' && (P.min != null && !(P.min > 0 && P.min < 1) || P.max != null && !(P.max > 0 && P.max < 1))) err(file, `${where}.params`, 'a log-odds line runs between probabilities strictly inside 0 and 1');
  if (c.kind === 'series' && P.hlines != null && !(Array.isArray(P.hlines) && P.hlines.every(h => isObj(h) && typeof h.y === 'number'))) err(file, `${where}.params.hlines`, 'hlines is a list of { id, y, label, dashed }');
  if (c.kind === 'tree' && S.branching != null && !(typeof S.branching === 'number' || isObj(S.branching) || Array.isArray(S.branching))) err(file, `${where}.state.branching`, 'branching is a number, a list per level or { "0": n, ... }');
  if (c.derive != null) {
    if (!isObj(c.derive)) err(file, `${where}.derive`, 'derive maps a target ("p2.x", "caption") to an expression');
    else Object.entries(c.derive).flatMap(([t, e]) => (t === 'let' && isObj(e) ? Object.entries(e).map(([k, v]) => ['let.' + k, v]) : [[t, e]])).forEach(([t, e]) => {
      if (typeof e !== 'string' && typeof e !== 'number') { err(file, `${where}.derive.${t}`, t === 'let' ? 'let maps names to expressions' : 'must be an expression string or a number'); return; }
      const parts = typeof e === 'string' ? (e.includes('{{') ? [...e.matchAll(/\{\{([^}]+)\}\}/g)].map(m => m[1]) : [e]) : [];
      parts.forEach(x => { if (/\^/.test(x.replace(/"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*'/g, '""'))) warn(file, `${where}.derive.${t}`, `"^" in a derive formula is not a power (it is JavaScript's bitwise XOR): write pow(a, b) or a ** b, or put a curve formula in quotes inside sum() or integral() (${x})`); });
      parts.forEach(x => { if (/[;`{}]|=>|\bfunction\b|\bnew\b|\bthis\b|(^|[^=!<>])=(?!=)/.test(x.replace(/"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*'/g, '""'))) err(file, `${where}.derive.${t}`, `not an expression: ${x}`); else { try { new Function('S', 'with (S) { return (' + x + '); }'); } catch (er) { err(file, `${where}.derive.${t}`, `does not parse: ${x}`); } } });
    });
  }
  if (c.state && typeof c.state.caption === 'string') checkText(file, `${where}.state.caption`, c.state.caption);
};

/* ENGINE-BACKLOG 585: [shuffled-position] a choice or multi with shuffle: true must not name an option by its place in the list */
const PLACE_WORD = 'first|second|third|fourth|fifth|last';
const POSITIONAL = [
  new RegExp(`\\b(?:${PLACE_WORD}) (?:option|answer|choice)s?\\b`, 'i'),
  /\b(?:top|bottom) (?:one|option|choice|answer)\b/i,
  /\bthe one (?:above|below)\b/i,
  /\b(?:[Oo]ptions?|[Cc]hoices?|[Aa]nswers?) \(?[A-E]\)?(?![A-Za-z'])/,
  /(?:^|[\s,;])\([a-e]\)(?=[\s,.;:]|$)/,
];
const positionalHit = (t) => { if (typeof t !== 'string') return null; const x = stripMathsAndCode(t); for (const re of POSITIONAL) { const m = re.exec(x); if (m) return m[0].trim(); } return null; };
/* Session V (600 series): the engine now shuffles every choice and multi unless shuffle is false, so the rule applies to all of them.
   A hit is dropped when the same screen itself uses that place word or label (a table row "answer A", "the top of the stack",
   problem "(c)", a code block), or the host carries noPosCheck: true. */
const PLACE_ANY = /\b(first|second|third|fourth|fifth|last|top|bottom|above|below)\b/i;
const screenContext = (host, parent) => {
  const out = [];
  for (const h of [host, parent]) { if (!isObj(h)) continue; out.push(h.title, h.prose, h.question, h.code, h.canvas ? JSON.stringify(h.canvas) : null); if (isObj(h.widget)) out.push(h.widget.question, h.widget.starter, h.widget.code); }
  return out.filter(x => typeof x === 'string').join('\n').toLowerCase();
};
const posExcluded = (m, host, parent) => {
  if (host.noPosCheck === true || (isObj(host.widget) && host.widget.noPosCheck === true)) return true;
  const ctx = screenContext(host, parent), low = m.toLowerCase();
  if (ctx.includes(low)) return true;
  const letter = /^\(?([a-e])\)?$|(?:option|choice|answer)s? \(?([a-e])\)?$/i.exec(m);
  if (letter) return /\((?:[a-e])\)|\b(?:option|choice|answer)s? [a-e]\b/i.test(ctx) || /\|\s*[a-e]\s*\|/.test(ctx);
  const word = PLACE_ANY.exec(m);
  if (word && new RegExp(`\\b${word[1]}\\b`, 'i').test(ctx)) return true;
  if (/```/.test(String(host.prose || '')) && /\b(?:top|bottom|above|below)\b/i.test(m)) return true;
  if (parent && /\banswer\b/i.test(m)) return true;   // a part's "first answer" is an earlier part's answer
  return false;
};
const checkShuffledPosition = (file, where, host, parent = null) => {
  const w = host && host.widget;
  if (!isObj(w) || !['choice', 'multi'].includes(w.kind) || w.shuffle === false) return;
  const texts = [[`${where}.explain.text`, isObj(host.explain) ? host.explain.text : null]];
  if (Array.isArray(w.options)) w.options.forEach((o, i) => { if (isObj(o)) texts.push([`${where}.widget.options[${i}].why`, o.why]); });
  if (Array.isArray(host.hints)) host.hints.forEach((h, i) => { if (isObj(h)) texts.push([`${where}.hints[${i}].text`, h.text]); });
  if (isObj(host.feedback)) { texts.push([`${where}.feedback.correct`, host.feedback.correct], [`${where}.feedback.generic`, host.feedback.generic]); if (isObj(host.feedback.byKey)) Object.entries(host.feedback.byKey).forEach(([k, v]) => texts.push([`${where}.feedback.byKey.${k}`, v])); }
  texts.forEach(([at, t]) => { const m = positionalHit(t); if (m && !posExcluded(m, host, parent)) warn(file, at, `[shuffled-position] "${m}" names an option by its place, but the options are shuffled; name it by what it says (or set noPosCheck: true if it names something else)`); });
};
/* Session V: [shuffle-false] shuffle: false is for options whose order carries meaning (ordered numbers or intervals) or that refer to each other */
const REFERS = /\b(?:both|all|none|neither|any|either)\s+of\s+(?:the\s+)?(?:above|these|those|them|the\s+(?:above|other|previous|following))\b|\b(?:all|none) of the above\b|\bthe\s+(?:above|other\s+options?)\b|\b(?:options?|answers?)\s+\(?[a-e]\)?\s+(?:and|or)\s+\(?[a-e]\)?\b/i;
const checkShuffleFalse = (file, where, w) => {
  if (w.shuffle != null && typeof w.shuffle !== 'boolean') err(file, `${where}.shuffle`, 'shuffle is true or false (absent means true: the engine shuffles)');
  if (w.shuffle !== false || !Array.isArray(w.options)) return;
  const opts = w.options.filter(isObj);
  if (orderedOptionsWhy(opts) || opts.some(o => REFERS.test(String(o.text ?? '')))) return;
  warn(file, `${where}.shuffle`, '[shuffle-false] shuffle: false stops the engine shuffling; keep it only for ordered numbers or intervals, or options that refer to each other ("both of the above"); otherwise delete it');
};
/* ENGINE-BACKLOG 585: [key-length] a choice whose key is over 1.5 times as long as every distractor gives the answer away */
const optLen = (o) => String(o && o.text != null ? o.text : '').replace(/\\[()[\]]|\$/g, '').trim().length;
const checkKeyLength = (file, where, w) => {
  if (!isObj(w) || w.kind !== 'choice' || !Array.isArray(w.options)) return;
  const key = w.options.find(o => isObj(o) && o.correct === true), others = w.options.filter(o => isObj(o) && o.correct !== true && o.text != null);
  if (!key || key.text == null || !others.length) return;
  const k = optLen(key);
  if (k >= 12 && others.every(o => k > 1.5 * optLen(o))) warn(file, `${where}.options`, `[key-length] the correct option is ${k} characters, more than 1.5 times every distractor (longest ${Math.max(...others.map(optLen))}); the longest option is a giveaway`);
};
/* ENGINE-BACKLOG 585: [multi-keys-uniform] in an exam with four or more multis, a count of keys that never varies is a giveaway */
const checkMultiUniform = (file, where, items) => {
  const counts = [];
  (items || []).forEach(it => { if (!isObj(it)) return; [it.widget, ...(Array.isArray(it.parts) ? it.parts.map(p => isObj(p) && p.widget) : [])].forEach(w => { if (isObj(w) && w.kind === 'multi' && Array.isArray(w.options)) counts.push(w.options.filter(o => isObj(o) && o.correct === true).length); }); });
  if (counts.length >= 4 && counts.every(c => c === counts[0])) warn(file, where, `[multi-keys-uniform] all ${counts.length} multi items have ${counts[0]} keys; vary the number of correct options so "pick ${counts[0]}" does not score`);
};
const checkFeedback = (file, where, fb, keys, { requireByKey = false } = {}) => {
  if (!isObj(fb)) { err(file, where, 'feedback with correct and generic lines is required'); return; }
  if (!fb.correct) err(file, `${where}.correct`, 'required field missing');
  if (!fb.generic) err(file, `${where}.generic`, 'required field missing');
  checkText(file, `${where}.correct`, fb.correct); checkText(file, `${where}.generic`, fb.generic);
  const byKey = fb.byKey || {};
  if (!isObj(byKey)) { err(file, `${where}.byKey`, 'must be an object'); return; }
  if (requireByKey && !Object.keys(byKey).length) err(file, `${where}.byKey`, 'a trap screen needs at least one byKey line naming the misconception');
  Object.entries(byKey).forEach(([k, v]) => {
    if (keys && !keys.has('*') && !keys.has(k)) err(file, `${where}.byKey.${k}`, `the widget cannot return the key "${k}"`);
    if (keys && keys.slip && keys.slip.has(k) && !keys.slip.get(k).some(id => Object.prototype.hasOwnProperty.call(byKey, id))) warn(file, `${where}.byKey.${k}`, `[table-slip-key] key "${k}" is an editable cell id and that cell has wrong[] entries, so table.js returns the wrong id instead and this line never fires for the slip; re-key to ${keys.slip.get(k).map(x => `"${x}"`).join(' or ')}`);
    checkText(file, `${where}.byKey.${k}`, v);
    const sentences = stripMathsAndCode(v).split(/[.?]\s/).filter(s => s.trim()).length;
    if (sentences > 3) warn(file, `${where}.byKey.${k}`, 'at most three sentences');
  });
};
/* item 450: a patch (explain.canvas, a wrong answer's canvas) that holds a whole canvas is ignored by the engine */
const wholeCanvasPatch = (file, where, p) => { if (isObj(p) && p.kind != null && typeof p.kind === 'string' && isObj(p.params)) warn(file, where, 'this is a state patch for the screen\'s canvas; it has kind and params, so it looks like a whole canvas and the Why? sheet will show the canvas unchanged. Give only the state keys to change ({ "shade": [...], "highlight": [...] })'); };
const checkExplain = (file, where, ex, { required = false } = {}) => {
  if (ex != null && isObj(ex)) wholeCanvasPatch(file, `${where}.canvas`, ex.canvas);
  if (ex == null) { if (required) warn(file, where, 'an explanation (explain.text) is expected'); return; }
  if (!ex.text) err(file, `${where}.text`, 'required field missing');
  checkText(file, `${where}.text`, ex.text);
};
const checkHints = (file, where, hints, canvas, required) => {
  if (hints == null) { if (required) err(file, where, 'hints required (1 to 3 rungs: nudge, point, step)'); return; }
  if (!Array.isArray(hints) || hints.length < 1 || hints.length > 3) { err(file, where, '1 to 3 hints'); return; }
  let last = -1;
  hints.forEach((h, i) => {
    if (!isObj(h)) { err(file, `${where}[${i}]`, 'a hint is an object { rung, text, highlight }'); return; }
    if (h.highlight != null && !Array.isArray(h.highlight)) { err(file, `${where}[${i}].highlight`, 'highlight must be a list of ids'); h = { ...h, highlight: [] }; }
    const r = RUNGS.indexOf(h.rung);
    if (r < 0) err(file, `${where}[${i}].rung`, 'rung is nudge, point or step');
    else if (r <= last) err(file, `${where}[${i}].rung`, 'hints must be in rung order nudge, point, step');
    last = Math.max(last, r);
    if (!h.text) err(file, `${where}[${i}].text`, 'required field missing');
    checkText(file, `${where}[${i}].text`, h.text);
    (h.highlight || []).forEach(id => { if (!plausibleId(canvas, id)) err(file, `${where}[${i}].highlight`, `"${id}" is not a plausible id on a ${canvas ? canvas.kind : 'missing'} canvas`); });
    if (h.rung === 'point' && canvas && !(h.highlight || []).length) warn(file, `${where}[${i}]`, 'a point hint usually highlights the canvas');
  });
};
const checkDifficulty = (file, where, d, lo, hi, label) => {
  if (!Number.isInteger(d) || d < 1 || d > 5) { err(file, where, 'difficulty must be an integer 1 to 5'); return; }
  if (d < lo || d > hi) err(file, where, `${label} difficulty runs ${lo} to ${hi} (found ${d})`);
};

/* tags (ENGINE-BACKLOG 456): a non-empty list of kebab-case family names, the first being the item's family. Allowed on lesson
   screens and on every kind of item (quiz, review, homework, exam, bank). Nothing is checked when it is absent. */
const checkTags = (file, where, tags) => {
  if (tags === undefined) return;
  if (!Array.isArray(tags) || !tags.length) { err(file, where, 'tags is a non-empty list of kebab-case family names, for example ["dice-ev"]'); return; }
  const seen = new Set();
  tags.forEach((t, i) => {
    if (typeof t !== 'string' || !KEBAB.test(t)) err(file, `${where}[${i}]`, `${JSON.stringify(t)} is not a kebab-case family name`);
    else if (seen.has(t)) err(file, `${where}[${i}]`, `duplicate tag "${t}"`);
    else seen.add(t);
  });
  if (tags.length > 4) warn(file, where, 'more than 4 tags: the first is the family, the rest only narrow it');
};
/* pace (ENGINE-BACKLOG 457): the seconds an item should take, a positive number; only the results line reads it, never grading */
const checkPace = (file, where, v) => {
  if (v === undefined) return;
  if (typeof v !== 'number' || !Number.isFinite(v) || v <= 0) err(file, where, 'pace is a positive number of seconds');
  else if (v > 1800) warn(file, where, `pace ${v} is over 30 minutes: it is in seconds`);
};

let perfOptionalRows = 0;
/* Performance task (ENGINE-BACKLOG 529, docs/AUTHORING.md section 5): the shape of one item; the level rules run in the course loop (tools/perf-rules.mjs) */
const perfItem = (file, where, it, ctx) => {
  if (!ctx.perf) { err(file, `${where}.performance`, 'performance belongs on a homework or level-review item'); return; }
  checkTask(it).forEach(m => err(file, `${where}.performance`, m));
  const optRows = optionalRows(it);   // item 702: advisory
  if (optRows.length) { perfOptionalRows++; warn(file, where, `[perf-optional-row] ${where} (${it.id}): rubric row${optRows.length === 1 ? '' : 's'} ${optRows.join(', ')} ${optRows.length === 1 ? 'is' : 'are'} optional but the prompt marks no part optional (DECISIONS session X, optional sub-questions)`); }
  const s = isObj(it.widget) ? it.widget : it;
  if (it.performance === 'data' && s.data != null) dataFiles(file, isObj(it.widget) ? `${where}.widget` : where, s);
  if (it.performance === 'aloud') {
    const x = it.kind === 'longform' ? it : it.widget, at = it.kind === 'longform' ? where : `${where}.widget`;
    if (isObj(x) && Array.isArray(x.followUps)) x.followUps.forEach((f, i) => checkText(file, `${at}.followUps[${i}]`, f));
  }
};
/* An item: a problem screen without hints (quiz, review, homework, exam, bank) */
const checkItem = (file, where, it, ctx) => {
  if (!isObj(it)) { err(file, where, 'item must be an object'); return null; }
  checkTags(file, `${where}.tags`, it.tags); checkPace(file, `${where}.pace`, it.pace);
  if (!it.id || !KEBAB.test(String(it.id))) err(file, `${where}.id`, 'item id must be kebab-case');
  if (it.difficulty != null || ctx.needDifficulty !== false) checkDifficulty(file, `${where}.difficulty`, it.difficulty, ctx.lo, ctx.hi, ctx.label);
  if (it.hints) err(file, `${where}.hints`, `${ctx.label} items have no hints`);
  /* item 297: on a longform item, prose takes the place of prompt on screen, so the prompt would never show */
  if (typeof it.prose === 'string' && it.prose.trim() && typeof (it.prompt || (isObj(it.widget) && it.widget.kind === 'longform' && it.widget.prompt)) === 'string' && String(it.prompt || it.widget.prompt).trim()) warn(file, where, 'this item has both prose and prompt: prose replaces prompt on screen, so the prompt is never shown (merge them into one)');
  if (ctx.skillsRequired && (!Array.isArray(it.skills) || !it.skills.length)) err(file, `${where}.skills`, 'name at least one skill');
  (it.skills || []).forEach(s => { if (ctx.skills && !ctx.skills.has(s)) err(file, `${where}.skills`, `unknown skill "${s}"`); });
  if (it.performance !== undefined) perfItem(file, where, it, ctx);
  if (typeof it.title === 'string' && it.title.includes('$')) warn(file, `${where}.title`, 'an item title is shown as plain text, so maths in it is not typeset: write it in words');   // item 538
  if (it.parts !== undefined) return checkParts(file, where, it, ctx);
  if (it.kind === 'longform' || (it.widget && it.widget.kind === 'longform')) {
    if (!ctx.allowLongform) err(file, where, 'longform items belong in homework and exams');
    checkLongform(file, where, it.kind === 'longform' ? it : it.widget);
    return 'longform';
  }
  checkCanvas(file, `${where}.canvas`, it.canvas);
  checkText(file, `${where}.prose`, it.prose); checkText(file, `${where}.question`, it.question);
  if (!it.question) err(file, `${where}.question`, 'required field missing');
  if (!it.widget) { err(file, `${where}.widget`, 'required field missing'); return null; }
  const keys = checkWidget(file, `${where}.widget`, it.widget, it.canvas, { question: it.question, prose: it.prose, allowLongform: ctx.allowLongform });
  checkFeedback(file, `${where}.feedback`, it.feedback, keys);
  checkExplain(file, `${where}.explain`, it.explain, { required: true });
  checkShuffledPosition(file, where, it);
  if (ctx.warnInteractive && (CANVAS_BOUND.has(it.widget.kind) || (it.canvas && (it.canvas.controls || []).length))) warn(file, where, 'a quiz item with an interactive canvas: concreteness should have faded by the quiz');
  return it.widget.kind;
};


/* An item with parts (ENGINE-BACKLOG 467, docs/AUTHORING.md section 5): parts: [{ question, widget, feedback, explain?, prose?, canvas?,
   difficulty?, id? }], 2 to 6, each of any widget kind except longform, opened in turn once the one before is checked. The item
   carries its own id, difficulty, skills, tags and pace, and optionally a title, prose, canvas and question as the stem. Not on a
   quiz item. A code part's tests are cumulative (the earlier code parts' tests run too), so the merged list is held to 15. */
const PART_KEYS = ['id', 'prose', 'canvas', 'question', 'widget', 'feedback', 'explain', 'difficulty', 'noPosCheck'];
const checkParts = (file, where, it, ctx) => {
  if (ctx.label === 'quiz') err(file, `${where}.parts`, 'parts is not allowed on a quiz item (a quiz item is one question with one attempt); use a review, homework, exam or bank item');
  if (!Array.isArray(it.parts) || it.parts.length < 2 || it.parts.length > 6) { err(file, `${where}.parts`, 'parts is a list of 2 to 6 parts (a one-part item is an ordinary item)'); return 'parts'; }
  if (it.widget !== undefined || it.kind !== undefined || it.prompt !== undefined) err(file, `${where}.widget`, 'an item with parts has no widget of its own: each part carries its widget (put the shared setup in prose, canvas and question)');
  if (it.feedback !== undefined) err(file, `${where}.feedback`, 'an item with parts has no feedback of its own: each part carries feedback');
  checkCanvas(file, `${where}.canvas`, it.canvas);
  checkText(file, `${where}.prose`, it.prose); checkText(file, `${where}.question`, it.question);
  if (it.explain != null) checkExplain(file, `${where}.explain`, it.explain);
  else if (!it.parts.some(p => isObj(p) && p.explain)) warn(file, `${where}.explain`, 'an explanation (explain.text) is expected on the item or on its parts');
  it.parts.forEach((p, k) => {
    const at = `${where}.parts[${k}]`;
    if (!isObj(p)) { err(file, at, 'a part is an object { question, widget, feedback }'); return; }
    if (p.kind === 'paper' || p.kind === 'check') err(file, `${at}.kind`, 'this is a stage exam part (paper or check); an item\'s parts are { question, widget, feedback }');
    Object.keys(p).forEach(f => { if (!PART_KEYS.includes(f)) err(file, `${at}.${f}`, `unknown part field "${f}" (allowed: ${PART_KEYS.join(', ')})`); });
    if (p.id != null && !KEBAB.test(String(p.id))) err(file, `${at}.id`, 'a part id is kebab-case');
    if (p.difficulty != null) checkDifficulty(file, `${at}.difficulty`, p.difficulty, 1, 5, 'part');
    checkCanvas(file, `${at}.canvas`, p.canvas);
    checkText(file, `${at}.prose`, p.prose); checkText(file, `${at}.question`, p.question);
    if (!p.question) err(file, `${at}.question`, 'required field missing: each part asks its own question');
    if (!isObj(p.widget)) { err(file, `${at}.widget`, 'required field missing'); return; }
    if (p.widget.kind === 'longform') err(file, `${at}.widget`, 'a part cannot be longform: the learner marks a written answer, which a follow-up cannot wait for');
    if (ctx.label === 'bank' && p.widget.kind === 'code') err(file, `${at}.widget`, 'a code part cannot run in the bank deck');
    const keys = checkWidget(file, `${at}.widget`, p.widget, p.canvas, { question: p.question, prose: p.prose ?? it.prose, allowLongform: false });
    checkFeedback(file, `${at}.feedback`, p.feedback, keys);
    checkExplain(file, `${at}.explain`, p.explain);
    checkShuffledPosition(file, at, p, it);
    if (p.widget.cumulative !== undefined) {
      if (p.widget.kind !== 'code') err(file, `${at}.widget.cumulative`, 'cumulative applies to a code part only');
      else if (typeof p.widget.cumulative !== 'boolean') err(file, `${at}.widget.cumulative`, 'cumulative is true or false (true by default: earlier code parts\' tests run too)');
    }
    if (p.widget.kind === 'code' && p.widget.cumulative !== false) {
      const merged = [];
      const from = it.parts.slice(0, k).reduce((a, q, j) => (isObj(q) && isObj(q.widget) && q.widget.kind === 'code' && q.widget.cumulative === false && (q.widget.language || 'python') === (p.widget.language || 'python') ? j : a), 0);   // an earlier part with cumulative: false starts a fresh merge
      it.parts.slice(from, k + 1).forEach(q => { const w = isObj(q) && q.widget; if (w && w.kind === 'code' && (w.language || 'python') === (p.widget.language || 'python')) (Array.isArray(w.tests) ? w.tests : []).forEach(t => { const j = JSON.stringify(t); if (!merged.includes(j)) merged.push(j); }); });
      if (merged.length > 15) err(file, `${at}.widget.tests`, `the cumulative tests of this part come to ${merged.length} (at most 15): trim an earlier part's tests or set cumulative: false`);
    }
  });
  return 'parts';
};

/* Drawn items (ENGINE-BACKLOG 468, docs/AUTHORING.md section 5): draw: [{ from, tags?, difficulty?, n }] on a mock or stage-exam paper.
   The entries are checked here; whether "from" names real files and has enough matching items is checked once every bank and drill
   file has been read (verifyDraws). */
const DRAW_KEYS = ['from', 'tags', 'difficulty', 'n'];
const drawRefs = [];
const checkDraw = (file, where, draw, { sample = false } = {}) => {
  if (draw === undefined) return 0;
  if (!Array.isArray(draw) || !draw.length) { err(file, where, 'draw is a non-empty list of { "from": "bank/<file>", "tags": [...], "difficulty": [low, high], "n": 3 }'); return 0; }
  let total = 0;
  draw.forEach((d, i) => {
    const at = `${where}[${i}]`;
    if (!isObj(d)) { err(file, at, 'a draw entry is an object { from, tags, difficulty, n }'); return; }
    Object.keys(d).forEach(f => { if (!DRAW_KEYS.includes(f)) err(file, `${at}.${f}`, `unknown draw field "${f}" (allowed: ${DRAW_KEYS.join(', ')})`); });
    if (typeof d.from !== 'string' || !/^(bank|drills)\/(\*|[a-z0-9]+(-[a-z0-9]+)*)$/.test(d.from)) err(file, `${at}.from`, 'from is "bank/<file>" (a bank file, "bank/<prefix>" for <prefix>-1, <prefix>-2 and so on, or "bank/*") or "drills/<pack>" (a pack name, a drill id or "drills/*")');
    if (!Number.isInteger(d.n) || d.n < 1 || d.n > 40) err(file, `${at}.n`, 'n is a whole number of items, 1 to 40');
    checkTags(file, `${at}.tags`, d.tags);
    if (d.difficulty !== undefined) {
      const ok = (v) => Number.isInteger(v) && v >= 1 && v <= 5;
      if (!(ok(d.difficulty) || (Array.isArray(d.difficulty) && d.difficulty.length === 2 && d.difficulty.every(ok) && d.difficulty[0] <= d.difficulty[1]))) err(file, `${at}.difficulty`, 'difficulty is one whole number 1 to 5, or [low, high]');
    }
    if (Number.isInteger(d.n) && d.n > 0) total += d.n;
    drawRefs.push({ file, at, d, sample });
  });
  return total;
};

/* ---------- Lesson (rules 1 to 9 and the warnings) ---------- */
const DURATION_IGNORE = durationIgnore();
const checkLesson = (file, courseId, lessonId, L, course) => {
  const skills = new Set(Object.keys(course.skills || {}));
  req(file, '', L, ['id', 'course', 'title', 'minutes', 'objectives', 'skills', 'screens', 'summary', 'quiz']);
  if (L.id !== lessonId) err(file, 'id', `id "${L.id}" must match the file name "${lessonId}"`);
  if (L.course !== courseId) err(file, 'course', `course "${L.course}" must match the folder "${courseId}"`);
  checkText(file, 'title', L.title);
  /* Item 10: session is short (default), workshop or project; minutes is the true estimate for the session, in its range */
  if (L.session != null && !hoursLib.SESSIONS.includes(L.session)) err(file, 'session', `session is one of ${hoursLib.SESSIONS.join(', ')} (default short)`);
  else {
    const [lo, hi] = hoursLib.SESSION_RANGE[L.session || 'short'];
    if (typeof L.minutes !== 'number' || L.minutes < lo || L.minutes > hi) err(file, 'minutes', `minutes is ${lo} to ${hi} for a ${L.session || 'short'} lesson${L.session ? '' : ' (a longer lesson sets "session": "workshop" or "project")'}`);
  }
  /* duration-prose: a duration of ${DURATION_FLOOR} minutes or more in the opening prose that differs from minutes by more than 5 (tools/duration-prose.mjs, AUTHORING section 1) */
  { const st = typeof L.minutes === 'number' ? statedMinutes(L) : null;
    if (st && Math.abs(st.minutes - L.minutes) > 5 && !DURATION_IGNORE[`${courseId}/${lessonId}`]) warn(file, 'screens[0..1].prose', `duration-prose: the opening prose says "${st.text}" (${st.minutes} min) but minutes is ${L.minutes}; set the true minutes (and "session": "workshop" or "project" above 20), or add the lesson to tools/duration-prose-ignore.json if it is a problem's data`); }
  if (!Array.isArray(L.objectives) || !L.objectives.length) err(file, 'objectives', 'at least one objective');
  (L.objectives || []).forEach((o, i) => checkText(file, `objectives[${i}]`, o));
  if (!Array.isArray(L.skills) || !L.skills.length) err(file, 'skills', 'name at least one skill');
  (L.skills || []).forEach(s => { if (!skills.has(s)) err(file, 'skills', `skill "${s}" is not declared in ${courseId}/course.json`); });
  const screens = Array.isArray(L.screens) ? L.screens : [];
  if (screens.length < 8 || screens.length > 12) err(file, 'screens', `8 to 12 screens (found ${screens.length})`);
  let titles = 0, nonTask = 0, hasTransfer = false, prevCanvasKind = null;
  const trapAt = screens.findIndex(s => s && s.type === 'trap');
  if (trapAt < 0) err(file, 'screens', 'every lesson has one trap screen');
  screens.forEach((s, i) => {
    const at = `screens[${i}]`;
    if (!isObj(s)) { err(file, at, 'screen must be an object'); return; }
    if (!SCREEN_TYPES.has(s.type)) { err(file, `${at}.type`, `unknown screen type "${s.type}"`); return; }
    if (s.type === 'title') titles++;
    if (s.type === 'title' || s.type === 'demonstrate' || (s.type === 'generalise' && !s.widget)) nonTask++;
    if (s.type === 'transfer') hasTransfer = true;
    checkText(file, `${at}.title`, s.title); checkText(file, `${at}.prose`, s.prose); checkText(file, `${at}.question`, s.question);
    checkTags(file, `${at}.tags`, s.tags); checkPace(file, `${at}.pace`, s.pace);
    if (s.prose && words(s.prose) > 60) warn(file, `${at}.prose`, `prose over 60 words (${words(s.prose)})`);
    checkCanvas(file, `${at}.canvas`, s.canvas);
    if (s.difficulty != null || GRADED.has(s.type)) checkDifficulty(file, `${at}.difficulty`, s.difficulty, 1, 3, 'lesson screen');
    let keys = null;
    if (s.widget) keys = checkWidget(file, `${at}.widget`, s.widget, s.canvas, { question: s.question, prose: s.prose });
    if (s.type === 'title') { if (!s.prose) err(file, `${at}.prose`, 'a title screen needs one framing sentence'); if (s.widget) err(file, `${at}.widget`, 'a title screen has no widget'); }
    if (s.type === 'demonstrate') {
      if (s.widget) err(file, `${at}.widget`, 'a demonstrate screen has no widget');
      if (!Array.isArray(s.steps) || s.steps.length < 3 || s.steps.length > 6) err(file, `${at}.steps`, '3 to 6 steps');
      (s.steps || []).forEach((st, j) => { if (!st.caption) err(file, `${at}.steps[${j}].caption`, 'required field missing'); checkText(file, `${at}.steps[${j}].caption`, st.caption); });
    }
    if (s.type === 'explore') {
      if (!s.canvas) err(file, `${at}.canvas`, 'an explore screen needs a canvas');
      else if (!(s.canvas.controls || []).length && !(s.widget && (CANVAS_BOUND.has(s.widget.kind) || (s.widget.kind === 'place' && ['boxes', 'array'].includes(s.widget.mode)) || (s.widget.kind === 'manipulate' && isObj(s.widget.states) && Object.values(s.widget.states).some(q => isObj(q) && isObj(q.canvas))))) && !authorMovable(s.canvas)) err(file, `${at}.canvas`, 'an explore screen needs an interactive canvas (controls or a canvas-bound widget)');
      if (!s.widget) err(file, `${at}.widget`, 'an explore screen ends with one observation question');
      else checkFeedback(file, `${at}.feedback`, s.feedback, keys);
      checkHints(file, `${at}.hints`, s.hints, s.canvas, false);
    }
    if (s.type === 'generalise') {
      /* item 101: in a programming course (a topic on the code track) a fenced code block states the rule as well as KaTeX does */
      /* inbox (backtest 1): a lesson with a code widget (a guided Python build such as backtest) counts too */
      const codeCourse = (C.stages || []).some(st => (st.topics || []).some(t => t.track === 'code' && (t.courses || []).includes(courseId))) || screens.some(q => isObj(q) && isObj(q.widget) && q.widget.kind === 'code');
      if (!s.prose || !(/\$/.test(s.prose) || (codeCourse && /```[\w+-]*\n[\s\S]*?```/.test(s.prose)))) err(file, `${at}.prose`, codeCourse ? 'a generalise screen states the rule in KaTeX or a fenced code block' : 'a generalise screen states the rule in KaTeX');
      if (s.widget) checkFeedback(file, `${at}.feedback`, s.feedback, keys);
    }
    if (GRADED.has(s.type)) {
      if (!s.question) err(file, `${at}.question`, 'required field missing');
      if (!s.widget) err(file, `${at}.widget`, 'required field missing');
      checkFeedback(file, `${at}.feedback`, s.feedback, keys, { requireByKey: s.type === 'trap' });
      checkHints(file, `${at}.hints`, s.hints, s.canvas, true);
      checkShuffledPosition(file, at, s);
      if (s.type === 'derive' && s.widget && !['expression', 'order', 'choice'].includes(s.widget.kind)) err(file, `${at}.widget.kind`, 'a derive screen uses expression, order or choice');
      /* item 177: moving between a table and a chart of the same numbers (or into or out of a pair) is a natural step, not a warning */
      const VIEWS = new Set(['table', 'plane', 'series', 'bars', 'scatter', 'distribution', 'console', 'number-line']);
      const natural = (a, b) => a === 'pair' || b === 'pair' || (VIEWS.has(a) && VIEWS.has(b) && (a === 'table' || b === 'table' || a === 'console' || b === 'console'));
      if (s.type === 'ladder' && s.canvas && prevCanvasKind && s.canvas.kind !== prevCanvasKind && !natural(prevCanvasKind, s.canvas.kind)) warn(file, `${at}.canvas`, 'a ladder screen usually reuses the previous canvas kind (a table next to a chart of the same numbers, or a pair, is fine)');
      if ((s.type === 'problem' || s.type === 'ladder') && !s.canvas && (trapAt < 0 || i < trapAt)) warn(file, at, 'a problem screen without a canvas before the ladder ends');
    }
    if (s.explain) checkExplain(file, `${at}.explain`, s.explain);
    if (s.canvas) prevCanvasKind = s.canvas.kind;
  });
  /* item 460: {{carry.name}} in a screen reads a value an earlier screen's widget stored with carry: "name" */
  const carried = new Set();
  screens.forEach((s, i) => {
    if (!isObj(s)) return;
    [...JSON.stringify(s).matchAll(/\{\{\s*carry\.([A-Za-z][A-Za-z0-9]*)/g)].forEach(m => { if (!carried.has(m[1]) && m[1] !== 'session') err(file, `screens[${i}]`, `{{carry.${m[1]}}} reads a value no earlier screen stores (give an earlier widget carry: "${m[1]}")`); });
    if (isObj(s.widget) && typeof s.widget.carry === 'string') carried.add(s.widget.carry);
  });
  if (titles > 1) err(file, 'screens', 'at most one title screen');
  if (nonTask > 2) err(file, 'screens', `at most two non-task screens (found ${nonTask})`);
  if (!hasTransfer) warn(file, 'screens', 'no transfer screen');
  const S = L.summary || {};
  if (!Array.isArray(S.ideas) || S.ideas.length !== 3) err(file, 'summary.ideas', 'exactly 3 ideas');
  (S.ideas || []).forEach((x, i) => checkText(file, `summary.ideas[${i}]`, x));
  if (!S.trap) err(file, 'summary.trap', 'required field missing');
  checkText(file, 'summary.trap', S.trap);
  if (!S.formula) warn(file, 'summary.formula', 'no formula card for the Notebook');
  else { req(file, 'summary.formula', S.formula, ['name', 'tex']); checkText(file, 'summary.formula.tex', `$${S.formula.tex || ''}$`, { copy: false }); checkText(file, 'summary.formula.note', S.formula.note); }
  const quiz = Array.isArray(L.quiz) ? L.quiz : [];
  if (quiz.length < 3 || quiz.length > 5) err(file, 'quiz', `3 to 5 quiz items (found ${quiz.length})`);
  const qids = new Set();
  quiz.forEach((q, i) => {
    if (q && q.id) { if (qids.has(q.id)) err(file, `quiz[${i}].id`, `duplicate id "${q.id}"`); qids.add(q.id); }
    checkItem(file, `quiz[${i}]`, q, { lo: 2, hi: 3, label: 'quiz', skills, warnInteractive: true });
  });
  return new Set(L.skills || []);
};

/* ---------- Reviews and homework ---------- */
/* A level's problem set (ENGINE-BACKLOG 845 to 851, docs/AUTHORING.md section 5): problems-<n>.json, 3 to 5 chained problems, each an item with 3 to 5 parts (no longform part,
   no code part: a part is a typed or chosen answer the engine grades), difficulty 3 to 5 with at least one 5, skills from the level's lessons. Untimed, no pass mark,
   not a gate: timed, pass and dueDays are refused. Every item-level rule of a review item applies (checkItem). minutes (default 40) is the in-app allowance. */
const checkProblemSet = (file, courseId, doc, items, skills, levelSkills) => {
  Object.keys(doc).forEach(k => { if (!['id', 'course', 'level', 'items', 'title', 'minutes', 'sample'].includes(k)) err(file, k, k === 'timed' || k === 'pass' || k === 'dueDays' ? `${k} does not apply to a problem set: it is untimed, has no pass mark and is not a gate` : `unknown field "${k}" (a problem set has id, course, level, items, and optionally title and minutes)`); });
  if (doc.title != null) { if (typeof doc.title !== 'string' || !doc.title.trim()) err(file, 'title', 'title is a non-empty string'); else checkText(file, 'title', doc.title); }
  if (doc.minutes != null && !(Number.isInteger(doc.minutes) && doc.minutes >= 10 && doc.minutes <= 240)) err(file, 'minutes', 'minutes is a whole number from 10 to 240 (40 where the file states none)');
  if (items.length < 3 || items.length > 5) err(file, 'items', `3 to 5 items (found ${items.length})`);
  items.forEach((it, i) => {
    const at = `items[${i}]`;
    checkItem(file, at, it, { lo: 3, hi: 5, label: 'problem set', skills, skillsRequired: true, allowLongform: false, perf: false });
    if (!isObj(it)) return;
    if (!Array.isArray(it.parts)) { err(file, `${at}.parts`, 'every problem in a problem set uses parts: 3 to 5 chained parts, each graded on its own'); return; }
    if (it.parts.length < 3 || it.parts.length > 5) err(file, `${at}.parts`, `a problem in a problem set has 3 to 5 parts (found ${it.parts.length})`);
    it.parts.forEach((p, k) => { if (isObj(p) && isObj(p.widget) && ['code', 'longform'].includes(p.widget.kind)) err(file, `${at}.parts[${k}].widget`, `a ${p.widget.kind} part cannot be in a problem set: each part is a typed or chosen answer the engine grades`); });
    if (levelSkills && Array.isArray(it.skills)) it.skills.forEach(sk => { if (skills.has(sk) && !levelSkills.has(sk)) err(file, `${at}.skills`, `skill "${sk}" is not taught in this level's lessons (use the skills of the level's own lessons)`); });
  });
  if (!items.some(it => isObj(it) && it.difficulty === 5)) err(file, 'items', 'a problem set needs at least one item at difficulty 5');
  const qids = new Set(); items.forEach((it, i) => { if (it && it.id) { if (qids.has(it.id)) err(file, `items[${i}].id`, `duplicate id "${it.id}"`); qids.add(it.id); } });
};
const checkSet = (file, kind, courseId, id, level, doc, course, { levelSkills = null } = {}) => {
  const skills = new Set(Object.keys(course.skills || {}));
  req(file, '', doc, kind === 'review' || kind === 'problems' ? ['id', 'course', 'level', 'items'] : ['id', 'course', 'level', 'dueDays', 'items']);
  if (doc.id !== id) err(file, 'id', `id "${doc.id}" must match the file name "${id}"`);
  if (doc.course !== courseId) err(file, 'course', `course must be "${courseId}"`);
  if (doc.level !== level) err(file, 'level', `level must be ${level}`);
  /* timed: { seconds, lockAtZero } puts a countdown and a live score on a level review (ENGINE-BACKLOG 454) */
  if (doc.timed != null) {
    if (kind !== 'review') err(file, 'timed', 'timed belongs on a level review (a practice set takes it from the route, a deck from its own file)');
    else if (!isObj(doc.timed)) err(file, 'timed', 'timed is { "seconds": n, "lockAtZero": true }');
    else {
      Object.keys(doc.timed).forEach(k => { if (!['seconds', 'lockAtZero'].includes(k)) err(file, `timed.${k}`, 'timed has seconds and lockAtZero only'); });
      if (!Number.isInteger(doc.timed.seconds) || doc.timed.seconds < 30 || doc.timed.seconds > 7200) err(file, 'timed.seconds', 'seconds is a whole number from 30 to 7200');
      if (doc.timed.lockAtZero != null && typeof doc.timed.lockAtZero !== 'boolean') err(file, 'timed.lockAtZero', 'lockAtZero is true or false (false by default: the clock is a guide)');
    }
  }
  /* pass: the share of a level review that counts as passed (default 0.7); it feeds the prerequisite rules and test-out (ENGINE-BACKLOG 481, 485) */
  if (doc.pass != null) {
    if (kind !== 'review') err(file, 'pass', 'pass belongs on a level review');
    else if (typeof doc.pass !== 'number' || !(doc.pass > 0 && doc.pass <= 1)) err(file, 'pass', 'pass is a share above 0 and at most 1 (0.7 by default)');
  }
  const items = Array.isArray(doc.items) ? doc.items : [];
  if (kind === 'problems') return checkProblemSet(file, courseId, doc, items, skills, levelSkills);
  const [lo, hi, nlo, nhi] = kind === 'review' ? [2, 4, 6, 10] : [3, 5, 6, 12];
  if (items.length < nlo || items.length > nhi) err(file, 'items', `${nlo} to ${nhi} items (found ${items.length})`);
  const kinds = items.map((it, i) => checkItem(file, `items[${i}]`, it, { lo, hi, label: kind, skills, skillsRequired: true, allowLongform: kind === 'homework', perf: true }));
  const qids = new Set(); items.forEach((it, i) => { if (it && it.id) { if (qids.has(it.id)) err(file, `items[${i}].id`, `duplicate id "${it.id}"`); qids.add(it.id); } });
  if (kind === 'homework') {
    if (!items.some(it => it && it.difficulty === 5)) err(file, 'items', 'homework needs at least one item at difficulty 5');
    if (!kinds.includes('longform')) err(file, 'items', 'homework needs at least one longform item');
    const track = course.track;
    /* an item with parts reports 'parts': its parts' widget kinds count as the item's kinds (code and expression often sit in follow-up parts) */
    const partKinds = items.flatMap(it => (it && Array.isArray(it.parts) ? it.parts.map(q => (isObj(q) && isObj(q.widget) ? q.widget.kind : null)) : []));
    const hasCode = kinds.includes('code') || partKinds.includes('code'), hasDerive = [...kinds, ...partKinds].some(k => k === 'order' || k === 'expression');
    if (track === 'code' && !hasCode) err(file, 'items', 'homework in a programming course needs at least one code item');
    else if (track === 'maths' && !hasDerive) err(file, 'items', 'homework in a maths course needs at least one order or expression item');
    else if (!hasCode && !hasDerive) err(file, 'items', 'homework needs at least one code, order or expression item');
  }
};

/* ---------- Exams ---------- */
const RAMP = { 2: 0.2, 3: 0.5, 4: 0.2, 5: 0.1 };
const checkRamp = (file, where, items) => {
  const n = items.length; if (!n) return;
  for (const [d, share] of Object.entries(RAMP)) {
    const got = items.filter(it => it && it.difficulty === Number(d)).length / n;
    if (Math.abs(got - share) > 0.1 + 1e-9) err(file, where, `difficulty ${d} is ${Math.round(got * 100)}% of items; the ramp asks ${share * 100}% ± 10%`);
  }
  const off = items.filter(it => it && !(it.difficulty in RAMP)).length;
  if (off) err(file, where, `${off} item(s) outside difficulty 2 to 5`);
};
/* Paper fields shared by topic, stage and mock exams: scoring, passNet, navigation, skip (ENGINE-BACKLOG 450, 451) */
const MOCK_STYLES = ['trader', 'research', 'developer', 'strats'];
/* Session V: role ids a mock paper's tracks may name: the prep.json tracks and the capstones.json roles */
const roleIds = () => {
  const ids = new Set(['trader', 'research', 'strats', 'developer']);
  try { const c = JSON.parse(fs.readFileSync(path.join(CONTENT, 'capstones.json'), 'utf8')); if (Array.isArray(c)) c.forEach(r => { if (r && typeof r.role === 'string') ids.add(r.role); }); } catch { /* optional */ }
  return ids;
};
const checkTracks = (file, where, p) => {
  if (p.tracks == null) return;
  if (!Array.isArray(p.tracks) || !p.tracks.length) { err(file, `${where}.tracks`, 'tracks is a non-empty list of role ids (a paper that counts only for learners on those tracks)'); return; }
  const known = roleIds();
  p.tracks.forEach(t => { if (!known.has(t)) err(file, `${where}.tracks`, `unknown role "${t}" (known: ${[...known].join(', ')})`); });
};
const SCORING_KEYS = ['right', 'wrong', 'blank'];
const checkPaperRules = (file, where, p, { needPass = false } = {}) => {
  if (p.minutes != null && !(typeof p.minutes === 'number' && p.minutes > 0)) err(file, `${where}.minutes`, 'minutes is a number above 0');
  if (p.pass != null && !(typeof p.pass === 'number' && p.pass > 0 && p.pass <= 1)) err(file, `${where}.pass`, 'pass is a share between 0 and 1');
  let max = (Array.isArray(p.items) ? p.items : []).reduce((a, it) => a + (it && it.generator ? Math.max(1, Math.round(+it.n || 1)) : 1), 0)
    + (Array.isArray(p.draw) ? p.draw.reduce((a, d) => a + (isObj(d) && Number.isInteger(d.n) && d.n > 0 ? d.n : 0), 0) : 0);   // drawn items (ENGINE-BACKLOG 468)
  if (p.scoring != null) {
    if (!isObj(p.scoring)) err(file, `${where}.scoring`, 'scoring is { right, wrong, blank } (numbers)');
    else {
      Object.keys(p.scoring).forEach(k => { if (!SCORING_KEYS.includes(k)) err(file, `${where}.scoring.${k}`, 'scoring has right, wrong and blank only'); else if (typeof p.scoring[k] !== 'number' || !Number.isFinite(p.scoring[k])) err(file, `${where}.scoring.${k}`, 'a mark is a number'); });
      if (typeof p.scoring.right === 'number' && p.scoring.right <= 0) err(file, `${where}.scoring.right`, 'right is the mark for a correct answer: above 0');
      if (typeof p.scoring.wrong === 'number' && p.scoring.wrong > 0) err(file, `${where}.scoring.wrong`, 'wrong is 0 or negative');
      if (typeof p.scoring.blank === 'number' && p.scoring.blank > 0) err(file, `${where}.scoring.blank`, 'blank is 0 or negative');
      if (typeof p.scoring.right === 'number' && p.scoring.right > 0) max *= p.scoring.right;
    }
  }
  if (p.passNet != null) {
    if (typeof p.passNet !== 'number' || !Number.isFinite(p.passNet)) err(file, `${where}.passNet`, 'passNet is a net score (a number)');
    else if (p.passNet > max + 1e-9) err(file, `${where}.passNet`, `passNet ${p.passNet} is above the most the paper can score (${max})`);
    if (p.pass != null) err(file, `${where}.pass`, 'give pass (a share) or passNet (a net score), not both');
  }
  if (needPass && p.pass == null && p.passNet == null) err(file, `${where}.pass`, 'give pass (a share of the marks) or passNet (a net score)');
  if (p.navigation != null && !['forward', 'free'].includes(p.navigation)) err(file, `${where}.navigation`, 'navigation is "forward" or "free"');
  if (p.skip != null && typeof p.skip !== 'boolean') err(file, `${where}.skip`, 'skip is true or false');
  if (p.skip === false && p.navigation !== 'forward') warn(file, `${where}.skip`, 'skip: false with free navigation only stops the learner moving on past an unanswered question; pair it with navigation: "forward" for a no-return test');
};
/* A generated item entry: { generator: "arith", mix, n, options } expands to n single-choice items at run time (ENGINE-BACKLOG 452) */
let WARM_OPS = null;
const warmOps = () => {
  if (WARM_OPS) return WARM_OPS;
  const ops = {};
  try { (JSON.parse(fs.readFileSync(path.join(CONTENT, 'warmup.json'), 'utf8')).operations || []).forEach(o => { ops[o.id] = o; }); } catch { /* the warm-up file has its own check */ }
  return (WARM_OPS = ops);
};
const checkGenerator = (file, where, g, allSkills) => {
  Object.keys(g).forEach(k => { if (!['generator', 'mix', 'n', 'options', 'difficulty', 'skills'].includes(k)) err(file, `${where}.${k}`, 'a generator entry has generator, mix, n, options, difficulty and skills only'); });
  if (g.generator !== 'arith') { err(file, `${where}.generator`, 'the only generator is "arith"'); return; }
  if (!Number.isInteger(g.n) || g.n < 1 || g.n > 200) err(file, `${where}.n`, 'n is a whole number of questions, 1 to 200');
  if (g.options != null && (!Number.isInteger(g.options) || g.options < 2 || g.options > 6)) err(file, `${where}.options`, 'options is 2 to 6 answers per question (default 4)');
  if (g.difficulty != null) checkDifficulty(file, `${where}.difficulty`, g.difficulty, 1, 5, 'generated');
  if (g.skills != null) { if (!Array.isArray(g.skills)) err(file, `${where}.skills`, 'skills is a list of skill ids'); else g.skills.forEach(s => { if (allSkills && !allSkills.has(s)) err(file, `${where}.skills`, `unknown skill "${s}"`); }); }
  if (g.mix != null) {
    const ops = warmOps();
    if (!isObj(g.mix)) { err(file, `${where}.mix`, 'mix is { operation: weight }, for example { "add": 1, "mul": 2 }'); return; }
    let any = false;
    Object.entries(g.mix).forEach(([k, v]) => {
      if (!ops[k]) { err(file, `${where}.mix.${k}`, `unknown operation "${k}" (content/warmup.json has ${Object.keys(ops).join(', ')})`); return; }
      const w = typeof v === 'number' ? v : isObj(v) ? (v.weight == null ? 1 : v.weight) : NaN;
      if (!(typeof w === 'number' && w >= 0 && Number.isFinite(w))) { err(file, `${where}.mix.${k}`, 'a weight is a number, 0 or more, or { weight, a: [lo, hi], b: [lo, hi] }'); return; }
      if (w > 0) any = true;
      if (isObj(v)) {
        Object.keys(v).forEach(f => { if (!['weight', 'a', 'b'].includes(f)) err(file, `${where}.mix.${k}.${f}`, 'an operation entry has weight, a and b only'); });
        ['a', 'b'].forEach(f => { if (v[f] != null && !(Array.isArray(v[f]) && v[f].length === 2 && v[f].every(Number.isInteger) && v[f][0] <= v[f][1] && v[f][0] >= 1)) err(file, `${where}.mix.${k}.${f}`, `${f} is a range [lo, hi] of whole numbers, 1 or more`); });
        if ((v.a || v.b) && ops[k].inverseOf) err(file, `${where}.mix.${k}`, `ranges go on "${ops[k].inverseOf}": "${k}" reverses it and uses the same numbers`);
      }
    });
    if (!any && Object.keys(g.mix).length) err(file, `${where}.mix`, 'at least one operation needs a weight above 0');
  }
};
/* The items of one paper: authored items and generator entries */
const checkPaperItems = (file, where, items, ctx) => {
  (Array.isArray(items) ? items : []).forEach((it, j) => {
    if (isObj(it) && it.generator !== undefined) { if (ctx.generators === false) err(file, `${where}[${j}].generator`, 'generated items belong in mock and stage exams, not topic exams'); else checkGenerator(file, `${where}[${j}]`, it, ctx.skills); }
    else { checkItem(file, `${where}[${j}]`, it, ctx); if (isObj(it) && it.required != null && typeof it.required !== 'boolean') err(file, `${where}[${j}].required`, 'required is true or false: the paper fails if this item is wrong, whatever the share'); }
  });
};
/* A mock exam (ENGINE-BACKLOG 453): exams/mock-<id>.json, papers and optional checks, exempt from the topic skill-coverage rule */
const checkMock = (file, id, doc, cur) => {
  const parted = Array.isArray(doc.parts);
  req(file, '', doc, parted ? ['id', 'name', 'style', 'models', 'parts'] : ['id', 'name', 'style', 'models', 'minutes', 'items']);
  if (!KEBAB.test(id.slice(5))) err(file, 'id', 'a mock id is mock- then kebab-case words');
  if (doc.style != null && !MOCK_STYLES.includes(doc.style)) err(file, 'style', `style is one of ${MOCK_STYLES.join(', ')}`);
  checkText(file, 'name', doc.name);
  if (typeof doc.models === 'string') {
    if (/\n/.test(doc.models) || doc.models.length > 200) err(file, 'models', 'models is one plain line (up to 200 characters) saying what the mock models');
    checkText(file, 'models', doc.models);
  } else if (doc.models != null) err(file, 'models', 'models is one plain line of text');
  if (doc.description != null) checkText(file, 'description', doc.description);
  ['topic', 'stage'].forEach(k => { if (doc[k] != null) err(file, k, `a mock has no ${k}: it mixes topics on purpose`); });
  const allSkills = new Set(Object.values(cur.courseDocs).flatMap(c => Object.keys((c || {}).skills || {})));
  if (doc.skills != null) { if (!isObj(doc.skills)) err(file, 'skills', 'skills is { id: name }'); else Object.keys(doc.skills).forEach(s => { if (!allSkills.has(s)) err(file, 'skills', `"${s}" is not a skill of any course`); }); }
  const ictx = { lo: 1, hi: 5, label: 'mock', skills: allSkills, skillsRequired: false, needDifficulty: false, allowLongform: true };
  const paperOf = (p, where) => {
    checkPaperRules(file, where, p, { needPass: true });
    checkTracks(file, where, p);
    if ((!Array.isArray(p.items) || !p.items.length) && !(Array.isArray(p.draw) && p.draw.length)) err(file, `${where}.items`, 'a paper needs at least one item (or a draw)');
    checkPaperItems(file, `${where}.items`, p.items, ictx);
    checkDraw(file, where ? `${where}.draw` : 'draw', p.draw, { sample: doc.sample === true });
    const seen = new Set();
    (p.items || []).forEach((it, j) => { if (isObj(it) && it.id) { if (seen.has(it.id)) err(file, `${where}.items[${j}].id`, `duplicate id "${it.id}"`); seen.add(it.id); } });
  };
  if (parted) {
    if (!doc.parts.some(p => p && p.kind === 'paper')) err(file, 'parts', 'a mock needs at least one paper');
    const pids = new Set();
    doc.parts.forEach((p, i) => {
      if (!isObj(p)) { err(file, `parts[${i}]`, 'a part is an object'); return; }
      if (!['paper', 'check'].includes(p.kind)) err(file, `parts[${i}].kind`, 'kind is paper or check');
      if (!p.name) err(file, `parts[${i}].name`, 'required field missing');
      checkText(file, `parts[${i}].name`, p.name);
      if (p.id) { if (pids.has(p.id)) err(file, `parts[${i}].id`, `duplicate part id "${p.id}"`); pids.add(p.id); }
      if (p.kind === 'paper') { req(file, `parts[${i}]`, p, ['minutes', 'items']); paperOf(p, `parts[${i}]`); }
    });
  } else paperOf(doc, '');
};
const checkExam = (file, id, doc, cur) => {
  const topicExam = id.startsWith('topic-');
  if (doc.id !== id) err(file, 'id', `id "${doc.id}" must match the file name "${id}"`);
  if (id.startsWith('mock-')) { checkMock(file, id, doc, cur); return; }
  if (topicExam) {
    req(file, '', doc, ['id', 'topic', 'name', 'minutes', 'pass', 'skills', 'items']);
    const t = cur.topics.get(String(doc.topic));
    if (!t) { err(file, 'topic', `unknown topic "${doc.topic}"`); return; }
    if (id !== `topic-${doc.topic}`) err(file, 'id', `a topic exam for ${doc.topic} is named topic-${doc.topic}`);
    const topicSkills = new Set(t.courses.flatMap(c => Object.keys((cur.courseDocs[c] || {}).skills || {})));
    const examSkills = new Set(Object.keys(doc.skills || {}));
    examSkills.forEach(s => { if (!topicSkills.has(s)) err(file, 'skills', `"${s}" is not a skill of a course in topic ${doc.topic}`); });
    topicSkills.forEach(s => { if (!examSkills.has(s)) err(file, 'skills', `topic skill "${s}" is not covered by the exam`); });
    if (doc.draw !== undefined) err(file, 'draw', 'draw belongs in mock and stage exams: a topic exam must cover its skills with items it names');
    const items = Array.isArray(doc.items) ? doc.items : [];
    if (items.length < 20 || items.length > 30) err(file, 'items', `20 to 30 items (found ${items.length})`);
    checkPaperItems(file, 'items', items, { lo: 2, hi: 5, label: 'exam', skills: examSkills, skillsRequired: true, allowLongform: true, generators: false });
    checkMultiUniform(file, 'items', items);
    checkPaperRules(file, '', doc);
    const used = new Set(items.flatMap(it => (it && it.skills) || []));
    examSkills.forEach(s => { if (!used.has(s)) err(file, 'items', `no item tests the skill "${s}"`); });
    checkRamp(file, 'items', items);
    if (typeof doc.pass !== 'number' || doc.pass <= 0 || doc.pass > 1) err(file, 'pass', 'pass is a share between 0 and 1');
  } else {
    req(file, '', doc, ['id', 'stage', 'parts']);
    if (!cur.stages.has(Number(doc.stage))) err(file, 'stage', `unknown stage "${doc.stage}"`);
    if (id !== `stage-${doc.stage}`) err(file, 'id', `a stage exam for stage ${doc.stage} is named stage-${doc.stage}`);
    const allSkills = new Set(Object.values(cur.courseDocs).flatMap(c => Object.keys((c || {}).skills || {})));
    (doc.parts || []).forEach((p, i) => {
      if (!['paper', 'check'].includes(p.kind)) err(file, `parts[${i}].kind`, 'kind is paper or check');
      if (!p.name) err(file, `parts[${i}].name`, 'required field missing');
      checkText(file, `parts[${i}].name`, p.name);
      if (p.kind === 'paper') {
        req(file, `parts[${i}]`, p, p.passNet != null ? ['minutes', 'items'] : ['minutes', 'pass', 'items']);
        const items = Array.isArray(p.items) ? p.items : [];
        checkPaperItems(file, `parts[${i}].items`, items, { lo: 2, hi: 5, label: 'exam', skills: allSkills, skillsRequired: true, allowLongform: true });
        checkMultiUniform(file, `parts[${i}].items`, items);
        checkPaperRules(file, `parts[${i}]`, p, { needPass: true });
        checkDraw(file, `parts[${i}].draw`, p.draw, { sample: doc.sample === true });
        if (items.length >= 10 && !p.draw && !items.some(it => it && it.generator !== undefined)) checkRamp(file, `parts[${i}].items`, items);
      }
    });
  }
};

/* ---------- Drills ---------- */
const checkDrill = (file, id, d, cur) => {
  req(file, '', d, ['id', 'name', 'course', 'skills', 'difficulty', 'brief', 'starter', 'examples', 'tests', 'how', 'solution']);
  if (d.id !== id) err(file, 'id', `id "${d.id}" must match the file name "${id}"`);
  const c = cur.courseDocs[d.course];
  if (!c) err(file, 'course', `unknown course "${d.course}"`);
  else (d.skills || []).forEach(s => { if (!(s in (c.skills || {}))) err(file, 'skills', `skill "${s}" is not declared in ${d.course}`); });
  if (!Number.isInteger(d.difficulty) || d.difficulty < 1 || d.difficulty > 5) err(file, 'difficulty', 'difficulty must be an integer 1 to 5');
  if (!Array.isArray(d.tests) || d.tests.length < 3) err(file, 'tests', 'at least 3 tests');
  else if (d.tests.length > 15) err(file, 'tests', 'at most 15 tests');
  checkText(file, 'name', d.name); checkText(file, 'brief', d.brief); checkText(file, 'how', d.how);
  checkTags(file, 'tags', d.tags); checkPace(file, 'pace', d.pace);
  dataFiles(file, '', d); // item 469: data files, as on a lesson code widget
  /* engine pass C, item 472 (E8, C-drill-patterns): language, pattern, sample; a C++ drill is checked as a C++ code widget */
  if (['index', 'session', 'sessions'].includes(id)) err(file, 'id', `"${id}" is reserved (the drill list and the session route)`);
  if (d.language != null && !['python', 'cpp'].includes(d.language)) err(file, 'language', 'language is "python" (the default) or "cpp"');
  if (d.pattern !== undefined) {
    if (typeof d.pattern !== 'string' || !DRILL_PATTERNS.includes(d.pattern)) err(file, 'pattern', `pattern ${JSON.stringify(d.pattern)} is not in the vocabulary: ${DRILL_PATTERNS.join(', ')} (js/screens/drill-lib.js, docs/AUTHORING.md section 5)`);
  }
  if (d.sample !== undefined && typeof d.sample !== 'boolean') err(file, 'sample', 'sample is true or false: a sample drill is for authors and is never listed');
  if (d.language === 'cpp') {
    if (typeof d.starter === 'string' && !/\S/.test(d.starter)) err(file, 'starter', 'the starter is empty');
    if (Array.isArray(d.tests) && d.tests.length) cppCodeWidget(file, '', { ...d, kind: 'code', language: 'cpp' });
    if (typeof d.solution !== 'string') err(file, 'solution', 'a C++ drill needs its model solution, a string of C++');
    if (d.fn != null) warn(file, 'fn', 'fn is for Python drills; a C++ test names the function in its own call');
    if (Array.isArray(d.examples) && d.examples.length < 1) err(file, 'examples', 'at least 1 example');
  }
  /* item 844: planted wrong solutions, run by tools/planted-check.mjs (no runtime here: shape only) */
  if (d.planted !== undefined) {
    if (!Array.isArray(d.planted)) err(file, 'planted', 'planted is an array of { "code", "slip" } wrong solutions');
    else d.planted.forEach((p, i) => {
      if (!p || typeof p !== 'object' || Array.isArray(p)) { err(file, `planted[${i}]`, 'a planted entry is { "code": "<a wrong solution>", "slip": "<one sentence naming the mistake>" }'); return; }
      if (typeof p.code !== 'string' || !/\S/.test(p.code)) err(file, `planted[${i}].code`, 'code is a non-empty string: the wrong solution');
      if (typeof p.slip !== 'string' || !/\S/.test(p.slip)) err(file, `planted[${i}].slip`, 'slip is a non-empty string: one sentence naming the mistake');
      Object.keys(p).forEach(k => { if (!['code', 'slip'].includes(k)) warn(file, `planted[${i}].${k}`, `unknown field "${k}" in a planted entry`); });
    });
  }
  if (d.pack !== undefined && (typeof d.pack !== 'string' || !KEBAB.test(d.pack))) err(file, 'pack', 'pack is a kebab-case name: the group a mock paper draws from ("drills/<pack>")');   // ENGINE-BACKLOG 468
};

/* Drill sessions: content/drills/sessions/<id>.json = { id, name, drills: [two ids], minutes (10 to 180, default 60), brief, sample } */
const checkDrillSession = (file, id, d, drillIds) => {
  req(file, '', d, ['id', 'name', 'drills']);
  if (d.id !== id) err(file, 'id', `id "${d.id}" must match the file name "${id}"`);
  checkText(file, 'name', d.name); if (d.brief != null) checkText(file, 'brief', d.brief);
  if (!Array.isArray(d.drills) || d.drills.length !== 2) err(file, 'drills', 'drills is a list of exactly two drill ids');
  else {
    if (d.drills[0] === d.drills[1]) err(file, 'drills', 'the two drills must differ');
    d.drills.forEach((x, i) => {
      if (!drillIds.has(x)) err(file, `drills[${i}]`, `drill "${x}" does not exist in content/drills`);
      else if (d.sample !== true && drillData.get(x) && drillData.get(x).sample === true) err(file, `drills[${i}]`, `drill "${x}" is a sample drill, which the drill list hides: a real session cannot name it (mark the session "sample": true)`);
    });
  }
  if (d.minutes != null && !(Number.isInteger(d.minutes) && d.minutes >= 10 && d.minutes <= 180)) err(file, 'minutes', 'minutes is a whole number from 10 to 180 (default 60)');
  if (d.sample !== undefined && typeof d.sample !== 'boolean') err(file, 'sample', 'sample is true or false');
  Object.keys(d).forEach(k => { if (!['id', 'name', 'drills', 'minutes', 'brief', 'sample'].includes(k)) warn(file, k, `unknown field "${k}" in a session file`); });
};

/* ---------- Interview bank: content/bank/<family>.json (ENGINE-BACKLOG 456, docs/AUTHORING.md section 5) ---------- */
const BANK_STYLES = ['mental-maths', 'probability', 'brainteaser', 'market-making', 'statistics', 'finance', 'coding', 'behavioural'];
const checkBank = (file, id, doc, cur) => {
  req(file, '', doc, ['id', 'name', 'items']);
  if (doc.id !== id) err(file, 'id', `id "${doc.id}" must match the file name "${id}"`);
  checkText(file, 'name', doc.name);
  if (doc.description != null) checkText(file, 'description', doc.description);
  if (!Array.isArray(doc.items) || !doc.items.length) { err(file, 'items', 'a bank file needs at least one item'); return; }
  if (doc.items.length > 200) warn(file, 'items', 'over 200 items: split the file by family');
  const allSkills = new Set(Object.values(cur.courseDocs).flatMap(c => Object.keys((c || {}).skills || {})));
  const ictx = { lo: 1, hi: 5, label: 'bank', skills: allSkills, skillsRequired: false, allowLongform: true };
  const seen = new Set();
  doc.items.forEach((it, i) => {
    const at = `items[${i}]`;
    const kind = checkItem(file, at, it, ictx);
    if (!isObj(it)) return;
    if (it.id) { if (seen.has(it.id)) err(file, `${at}.id`, `duplicate id "${it.id}"`); seen.add(it.id); }
    if (kind === 'code') err(file, `${at}.widget`, 'a code item cannot run in the bank deck');
    if (it.tags === undefined) err(file, `${at}.tags`, 'a bank item needs tags: a list of kebab-case family names, the first being its family');
    if (!Array.isArray(it.role) || !it.role.length) err(file, `${at}.role`, `role is a non-empty list drawn from ${MOCK_STYLES.join(', ')}`);
    else it.role.forEach(r => { if (!MOCK_STYLES.includes(r)) err(file, `${at}.role`, `unknown role "${r}" (${MOCK_STYLES.join(', ')})`); });
    if (typeof it.style !== 'string' || !KEBAB.test(it.style)) err(file, `${at}.style`, `style is one kebab-case word drawn from ${BANK_STYLES.join(', ')}`);
    else if (!BANK_STYLES.includes(it.style)) warn(file, `${at}.style`, `style "${it.style}" is not one of ${BANK_STYLES.join(', ')}`);
    if (typeof it.source !== 'string' || !it.source.trim()) err(file, `${at}.source`, 'source is one plain line saying where the question comes from (for example "Original" or "Adapted from probability review 1")');
    else { if (/\n/.test(it.source) || it.source.length > 120) err(file, `${at}.source`, 'source is one plain line of up to 120 characters'); checkText(file, `${at}.source`, it.source); }
    if (it.requires !== undefined) {
      if (!Array.isArray(it.requires) || !it.requires.length) err(file, `${at}.requires`, 'requires is a non-empty list of "course/lesson-id" references');
      else it.requires.forEach(r => {
        const m = /^([a-z0-9-]+)\/([a-z0-9-]+)$/.exec(String(r)), c = m && cur.courseDocs[m[1]];
        if (!m) err(file, `${at}.requires`, `"${r}" is not a "course/lesson-id" reference`);
        else if (!c) err(file, `${at}.requires`, `unknown course "${m[1]}"`);
        else if (!(c.levels || []).some(lv => (lv.lessons || []).includes(m[2]))) err(file, `${at}.requires`, `"${m[2]}" is not a lesson of ${m[1]}`);
      });
    }
  });
};

/* ---------- Main ---------- */
const curFile = path.join(CONTENT, 'curriculum.json');
const curDoc = readJSON(curFile);
if (curDoc.missing) err(curFile, '', 'curriculum.json is missing');
const C = curDoc.data || { stages: [], courses: {}, tracks: {} };
const cur = { topics: new Map(), stages: new Set(), courseDocs: {}, courseTopic: {} };
/* Samples (ENGINE-BACKLOG 467, 468): a top-level "sample": true marks a lesson, review, homework, exam, bank or drill file as an engine
   sample. It is listed under `samples` in the manifest, left out of every learner-facing list and count, and may sit in a course
   folder without being on the course map. Only `true` is allowed (leave the field out for real content). */
const samples = [];
const noteSample = (file, relPath, data) => {
  if (!isObj(data) || data.sample === undefined) return false;
  if (data.sample !== true) { err(file, 'sample', 'sample is true, or the field is left out'); return false; }
  samples.push(relPath);
  return true;
};
const bankData = new Map(), drillData = new Map();

/* Curriculum */
if (!Array.isArray(C.stages)) err(curFile, 'stages', 'must be an array');
if (C.tracks) TRACKS.forEach(t => { if (!C.tracks[t]) err(curFile, `tracks.${t}`, 'track name missing'); });
(C.stages || []).forEach((s, i) => {
  const at = `stages[${i}]`;
  req(curFile, at, s, ['name', 'exit', 'topics']);
  if (s.hours != null) warn(curFile, `${at}.hours`, 'stage hours is derived (the sum of its topic hours, js/hours.js) and the engine ignores this field; remove it with tools/apply-item11-content.mjs');;
  if (!Number.isInteger(s.id)) err(curFile, `${at}.id`, 'stage id is an integer');
  cur.stages.add(s.id);
  checkText(curFile, `${at}.exit`, s.exit);
  (s.topics || []).forEach((t, j) => {
    const tat = `${at}.topics[${j}]`;
    req(curFile, tat, t, ['id', 'name', 'track', 'resource', 'courses']);
    if (typeof t.hours !== 'number') err(curFile, `${tat}.hours`, 'hours is a number');
    if (!TRACKS.includes(t.track)) err(curFile, `${tat}.track`, `unknown track "${t.track}"`);
    if (cur.topics.has(t.id)) err(curFile, `${tat}.id`, `duplicate topic "${t.id}"`);
    cur.topics.set(t.id, { ...t, stage: s.id });
    const res = [t.resource, ...(t.more || [])];
    res.forEach((r, k) => { if (!r || !r.name) err(curFile, `${tat}.resource`, 'every resource has a name'); else if (r.url != null && !/^https?:\/\//.test(r.url)) err(curFile, `${tat}.resource`, `bad url "${r.url}"`); });
    (t.courses || []).forEach(c => {
      if (cur.courseTopic[c]) err(curFile, `${tat}.courses`, `course "${c}" is listed in two topics`);
      cur.courseTopic[c] = t.id;
      if (!C.courses || !C.courses[c]) err(curFile, `${tat}.courses`, `course "${c}" has no entry in courses`);
    });
    checkText(curFile, `${tat}.name`, t.name); checkText(curFile, `${tat}.cover`, t.cover); checkText(curFile, `${tat}.exit`, t.exit);
  });
});
Object.entries(C.courses || {}).forEach(([id, c]) => {
  if (!KEBAB.test(id)) err(curFile, `courses.${id}`, 'course ids are kebab-case');
  if (!cur.courseTopic[id]) err(curFile, `courses.${id}`, 'course is in no topic');
  req(curFile, `courses.${id}`, c, ['name', 'topic', 'art', 'description']);
  if (c.topic !== cur.courseTopic[id]) err(curFile, `courses.${id}.topic`, `topic "${c.topic}" but the course is listed under ${cur.courseTopic[id]}`);
  if (ART && !ART.has(c.art)) err(curFile, `courses.${id}.art`, `unknown art id "${c.art}" (see js/art.js)`);
  checkText(curFile, `courses.${id}.description`, c.description);
});

/* Performance tasks (ENGINE-BACKLOG 529): the verb rule per written level, the one-task rule, the grandfather list (tools/perf-pending.json) and the manifest rows */
let perfPending = new Set(); try { const j = JSON.parse(fs.readFileSync(path.join(path.dirname(fileURLToPath(import.meta.url)), 'perf-pending.json'), 'utf8')); perfPending = new Set(Array.isArray(j.levels) ? j.levels : []); } catch { /* none: nothing is grandfathered */ }
const perfManifest = {};   // "course/L<n>" -> { file, item, kind, how }: js/content.js reads it so the met rule needs no extra fetch
const perfStats = { matched: 0, withTask: 0, pending: 0, levels: new Set() };
const perfLevel = (file, cid, n, objs, lessonsWritten, sets) => {
  const key = `${cid}/L${n}`; perfStats.levels.add(key);
  const written = lessonsWritten && sets.review && sets.homework;   // only a written level is held to the rule; a half-written one is not yet
  const tasks = [];
  ['review', 'homework'].forEach(k => { const st = sets[k]; if (st && Array.isArray(st.data.items)) st.data.items.forEach(it => { if (isObj(it) && it.performance !== undefined) tasks.push({ id: it.id, file: st.file, it }); }); });
  const stage = (cur.topics.get(cur.courseTopic[cid]) || {}).stage;
  const matched = written ? matchVerb(cid, stage, objs) : null;
  if (matched) perfStats.matched++;
  const r = perfCheckLevel({ key, matched, tasks, pending: perfPending.has(key) });
  r.errors.forEach(m => err(file, 'levels', m)); r.warnings.forEach(m => warn(file, 'levels', m));
  if (r.pendingNoTask) perfStats.pending++;
  if (tasks.length) perfStats.withTask++;
  if (tasks.length === 1 && KINDS_OK(tasks[0].it)) perfManifest[key] = { file: path.relative(CONTENT, tasks[0].file).split(path.sep).join('/'), item: tasks[0].id, kind: tasks[0].it.performance, how: perfHow(tasks[0].it), ...(matched ? { gates: true } : {}) };
};
const KINDS_OK = (it) => ['code', 'derivation', 'aloud', 'data'].includes(it.performance);

/* Courses */
const manifest = [];
const fluencyManifest = {};   // ENGINE-BACKLOG 804: "course/set-id" -> { lesson, title, n, pass, minutes, families, sample? }, read by js/content.js fluencyFor
/* A generated fluency set (docs/AUTHORING.md section 16): schema, the lesson on the course map, every family sampled at 200 seeds; voice on the text as drawn */
const checkFluencyFile = (file, cid, fileId, data, D, written, { fixture = false } = {}) => {
  const lessonIds = new Set(((D && D.levels) || []).flatMap(lv => (Array.isArray(lv.lessons) ? lv.lessons : [])));
  const voice = (where, text) => { const before = problems.length; checkText(file, where, text); return problems.splice(before).map(p => ({ level: p.level, where: p.where, msg: p.msg })); };
  const r = checkFluencySet(data, { fileId, lessonIds, written: new Set(written), voice, course: cid });
  r.problems.forEach(p => (p.level === 'error' ? err : warn)(file, p.where, p.msg));
  return r;
};
const problemsManifest = {};   // ENGINE-BACKLOG 845 to 851: "course/problems-n" -> { level, title, items, minutes, sample? }, read by js/content.js problemsFor and the in-app hours
const examMinutesManifest = {};   // ENGINE-BACKLOG 621: exam id -> minutes the exam screen runs, read by js/content.js examMinutes
const sessionManifest = {};   // item 10: "course/lesson" -> { session, minutes } for workshop and project lessons, read by js/content.js and js/hours.js
const lessonMinutesManifest = {};   // session Y: "course/lesson" -> the lesson's authored minutes, for the in-app hours (js/hours.js, read by js/content.js)
const setMinutesManifest = {};   // session Y: "course/review-1" -> minutes, only for a review or homework file that states `minutes` (none does yet); the others take the allowance in js/hours.js
const selfExams = [];   // exam ids that hold a self-marked item or a check part (same test as ZQ.state.provenance); js/content.js reads it to split old exam passes
const holdsSelf = (d) => { const L = (w) => !!w && w.kind === 'longform'; const it = (x) => !!x && (x.kind === 'longform' || L(x.widget) || (Array.isArray(x.parts) && x.parts.some(q => q && L(q.widget)))); return (Array.isArray(d.items) && d.items.some(it)) || (Array.isArray(d.parts) && d.parts.some(p => p && (p.kind === 'check' || (Array.isArray(p.items) && p.items.some(it))))); };
const writtenByCourse = new Map();   // course id -> Set of written lesson ids, for the prerequisite rules
const summary = [];
const skillOwner = new Map();
const courseDir = path.join(CONTENT, 'courses');
let folders = [];
try { folders = fs.readdirSync(courseDir, { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name).sort(); } catch { /* none */ }
folders.forEach(f => { if (!(C.courses || {})[f]) err(path.join(courseDir, f), '', 'course folder not listed in curriculum.json'); });
Object.keys(C.courses || {}).forEach(cid => {
  const dir = path.join(courseDir, cid), file = path.join(dir, 'course.json');
  const r = readJSON(file);
  if (r.missing) { err(file, '', 'course.json is missing'); return; }
  if (!r.data) return;
  const D = r.data;
  const meta = C.courses[cid];
  D.track = (cur.topics.get(cur.courseTopic[cid]) || {}).track;
  cur.courseDocs[cid] = D;
  req(file, '', D, ['id', 'name', 'topic', 'art', 'description', 'skills', 'levels']);
  if (D.id !== cid) err(file, 'id', `id "${D.id}" must match the folder "${cid}"`);
  if (D.topic !== meta.topic) err(file, 'topic', `topic "${D.topic}" differs from curriculum.json (${meta.topic})`);
  if (D.name !== meta.name) warn(file, 'name', 'name differs from curriculum.json');
  if (ART && !ART.has(D.art)) err(file, 'art', `unknown art id "${D.art}"`);
  checkText(file, 'description', D.description); checkText(file, 'name', D.name);
  /* strand ("quant" or "pure") and its roles note: both or neither (docs/AUTHORING.md, strand) */
  if (D.strand !== undefined && D.strand !== 'quant' && D.strand !== 'pure') err(file, 'strand', `strand must be "quant" or "pure" (found ${JSON.stringify(D.strand)})`);
  if (D.strand !== undefined && (typeof D.strandNote !== 'string' || !D.strandNote.trim())) err(file, 'strandNote', 'strandNote (a non-empty string naming the roles) is required when strand is set');
  if (D.strand === undefined && D.strandNote !== undefined) err(file, 'strandNote', 'strandNote needs strand');
  if (typeof D.strandNote === 'string') checkText(file, 'strandNote', D.strandNote);
  const skills = isObj(D.skills) ? Object.keys(D.skills) : [];
  if (skills.length < 3 || skills.length > 6) err(file, 'skills', `3 to 6 skills (found ${skills.length})`);
  skills.forEach(s => {
    if (!KEBAB.test(s)) err(file, `skills.${s}`, 'skill ids are kebab-case');
    if (skillOwner.has(s)) err(file, `skills.${s}`, `skill id also used by ${skillOwner.get(s)}; skill ids are global`);
    skillOwner.set(s, cid);
    checkText(file, `skills.${s}`, D.skills[s]);
  });
  const levels = Array.isArray(D.levels) ? D.levels : [];
  if (levels.length < 3 || levels.length > 5) err(file, 'levels', `3 to 5 levels (found ${levels.length})`);
  const seen = new Set(), referenced = new Set(['course.json']);
  const written = [], unwritten = [], usedSkills = new Set();
  const levelTaught = {};   // level n -> { skills: Set of the skills its written lessons carry, complete: every lesson of the level is written }, for the problem-set skills rule
  let reviewsMissing = 0, homeworkMissing = 0, lessonTotal = 0;
  levels.forEach((lv, i) => {
    const at = `levels[${i}]`;
    if (lv.n !== i + 1) err(file, `${at}.n`, `levels are numbered from 1 in order (expected ${i + 1})`);
    if (!lv.name) err(file, `${at}.name`, 'required field missing');
    checkText(file, `${at}.name`, lv.name);
    const objs = [], sets = {}; let lessonsWritten = true;   // item 529: the level's lesson objectives and its review and homework, for the performance-task rule
    const ls = Array.isArray(lv.lessons) ? lv.lessons : [];
    const taught = levelTaught[lv.n] = { skills: new Set(), complete: true };
    if (ls.length < 4 || ls.length > 6) err(file, `${at}.lessons`, `4 to 6 lessons per level (found ${ls.length})`);
    ls.forEach(l => {
      lessonTotal++;
      if (!KEBAB.test(l)) err(file, `${at}.lessons`, `"${l}" is not kebab-case`);
      if (seen.has(l)) err(file, `${at}.lessons`, `duplicate lesson id "${l}"`);
      seen.add(l); referenced.add(`${l}.json`);
      const name = (D.lessonNames || {})[l];
      if (!name) warn(file, `lessonNames.${l}`, 'no name: the map falls back to the lesson title or the id');
      else { checkText(file, `lessonNames.${l}`, name); if (name.includes('$')) err(file, `lessonNames.${l}`, 'keep maths out of lesson names (they show as plain text)'); }
      checkText(file, `lessonObjectives.${l}`, (D.lessonObjectives || {})[l]);
      const lf = path.join(dir, `${l}.json`), lr = readJSON(lf);
      if (lr.missing) { unwritten.push(l); lessonsWritten = false; taught.complete = false; return; }
      if (lr.data && Array.isArray(lr.data.skills)) lr.data.skills.forEach(sk => taught.skills.add(sk));
      if (lr.data && Array.isArray(lr.data.objectives)) objs.push(...lr.data.objectives.filter(o => typeof o === 'string'));
      written.push(l); manifest.push(`courses/${cid}/${l}.json`);
      if (noteSample(lf, `courses/${cid}/${l}.json`, lr.data)) err(lf, 'sample', 'a sample file cannot be on a course map: leave it out of course.json');
      if (lr.data && typeof lr.data.minutes === 'number') lessonMinutesManifest[`${cid}/${l}`] = lr.data.minutes;
      if (lr.data && (lr.data.session === 'workshop' || lr.data.session === 'project') && typeof lr.data.minutes === 'number') sessionManifest[`${cid}/${l}`] = { session: lr.data.session, minutes: lr.data.minutes };
      if (lr.data) guard(lf, () => checkLesson(lf, cid, l, lr.data, D).forEach(s => usedSkills.add(s)));
    });
    [['review', `review-${i + 1}`], ['homework', `homework-${i + 1}`]].forEach(([kind, expect]) => {
      if (lv[kind] !== expect) err(file, `${at}.${kind}`, `${kind} is "${expect}"`);
      const id = lv[kind] || expect; referenced.add(`${id}.json`);
      const sf = path.join(dir, `${id}.json`), sr = readJSON(sf);
      if (sr.missing) { if (kind === 'review') reviewsMissing++; else homeworkMissing++; return; }
      manifest.push(`courses/${cid}/${id}.json`);
      if (sr.data && typeof sr.data.minutes === 'number' && sr.data.minutes > 0) setMinutesManifest[`${cid}/${id}`] = sr.data.minutes;
      if (noteSample(sf, `courses/${cid}/${id}.json`, sr.data)) err(sf, 'sample', 'a sample file cannot be on a course map: leave it out of course.json');
      if (sr.data) { guard(sf, () => checkSet(sf, kind, cid, id, i + 1, sr.data, D)); sets[kind] = { file: sf, id, data: sr.data }; }
      /* ENGINE-BACKLOG 574: a mapped level review states its pass share (write-review-pass.mjs writes the default 0.8) */
      if (kind === 'review' && sr.data && sr.data.pass == null) err(sf, 'pass', 'a level review needs a pass share (for example "pass": 0.8; node tools/write-review-pass.mjs writes the default)');
    });
    guard(file, () => perfLevel(file, cid, lv.n, objs, lessonsWritten, sets));
    /* ENGINE-BACKLOG 573: a written level's number script must import numbers_lib and read the lesson JSON through numbers_lib (a missing script is out of scope here) */
    if (lessonsWritten && sets.review && sets.homework) {
      const nf = path.join(APP, '..', 'docs', 'reports', `${cid}-L${lv.n}-numbers.py`);
      if (fs.existsSync(nf)) { const t = fs.readFileSync(nf, 'utf8'); if (!/\bLevel\(/.test(t) || !/(^|\n)\s*(from\s+numbers_lib\s+import|import\s+numbers_lib)/.test(t)) warn(nf, '', 'the number script never uses numbers_lib (an import of numbers_lib and Level(): it does not check the stated numbers in the lesson JSON'); }
    }
  });
  listJSON(dir).forEach(f => {
    if (referenced.has(f)) return;
    const uf = path.join(dir, f), ur = readJSON(uf), uid = f.replace(/\.json$/, '');
    if (/^fluency-.+\.json$/.test(f)) {   // a generated fluency set, found by its file name (no course.json entry)
      if (!isObj(ur.data)) { if (!ur.bad) err(uf, '', 'a fluency set is a JSON object'); return; }
      manifest.push(`courses/${cid}/${f}`);
      if (noteSample(uf, `courses/${cid}/${f}`, ur.data)) { /* listed under samples */ }
      guard(uf, () => checkFluencyFile(uf, cid, uid, ur.data, D, written));
      const d = ur.data;
      fluencyManifest[`${cid}/${uid}`] = { lesson: d.lesson, title: d.title, n: Number.isInteger(d.n) ? d.n : 20, pass: typeof d.pass === 'number' ? d.pass : 0.9, minutes: Number.isInteger(d.minutes) ? d.minutes : 10, families: Array.isArray(d.families) ? d.families.length : 0, ...(d.sample === true ? { sample: true } : {}) };
      return;
    }
    if (/^problems-.+\.json$/.test(f)) {   // a level's problem set, found by its file name (no course.json entry; a level without one is not an error)
      if (!isObj(ur.data)) { if (!ur.bad) err(uf, '', 'a problem set is a JSON object'); return; }
      const pm = /^problems-(\d+)$/.exec(uid), pn = pm ? Number(pm[1]) : null;
      if (!pm || String(pn) !== pm[1] || pn < 1 || pn > levels.length) { err(uf, '', `a problem set is problems-<n>.json with n a level of the course (1 to ${levels.length})`); return; }
      manifest.push(`courses/${cid}/${f}`);
      const isSample = noteSample(uf, `courses/${cid}/${f}`, ur.data);
      const lt = levelTaught[pn];
      guard(uf, () => checkSet(uf, 'problems', cid, uid, pn, ur.data, D, { levelSkills: lt && lt.complete ? lt.skills : null }));
      const d = ur.data;
      problemsManifest[`${cid}/${uid}`] = { level: pn, title: typeof d.title === 'string' ? d.title : '', items: Array.isArray(d.items) ? d.items.length : 0, minutes: Number.isInteger(d.minutes) && d.minutes > 0 ? d.minutes : 40, ...(isSample ? { sample: true } : {}) };
      return;
    }
    if (!(ur.data && ur.data.sample === true)) { if (!ur.bad) err(uf, '', 'file is not referenced by course.json (an engine sample says "sample": true at the top)'); return; }
    /* a sample lesson, review or homework in a course folder: checked like the real thing, kept off the map and out of every count */
    noteSample(uf, `courses/${cid}/${f}`, ur.data); manifest.push(`courses/${cid}/${f}`);
    guard(uf, () => { if (/^review-/.test(uid)) checkSet(uf, 'review', cid, uid, ur.data.level, ur.data, D); else if (/^homework-/.test(uid)) checkSet(uf, 'homework', cid, uid, ur.data.level, ur.data, D); else checkLesson(uf, cid, uid, ur.data, D); });
  });
  if (!unwritten.length) skills.forEach(s => { if (!usedSkills.has(s)) err(file, `skills.${s}`, 'no lesson uses this skill'); });
  if (unwritten.length || reviewsMissing || homeworkMissing) {
    warn(file, '', `not yet written: ${unwritten.length} of ${lessonTotal} lessons, ${reviewsMissing} of ${levels.length} reviews, ${homeworkMissing} of ${levels.length} homework`);
  }
  writtenByCourse.set(cid, new Set(written));
  summary.push({ cid, topic: meta.topic, lessons: lessonTotal, levels: levels.length, written: written.length, unwritten, reviews: levels.length - reviewsMissing, homework: levels.length - homeworkMissing });
});

/* The fluency fixtures (tools/fixtures/fluency, never content): checked like a real set, so the sampler and the rules are exercised on every run */
fluencyFixtures().forEach(ff => {
  const fr = readJSON(ff);
  if (!isObj(fr.data)) return;
  const cid = fr.data.course, D = cur.courseDocs[cid];
  if (!D) { err(ff, 'course', `the fixture's course "${cid}" is not a course`); return; }
  guard(ff, () => checkFluencyFile(ff, cid, fr.data.id, fr.data, D, writtenByCourse.get(cid) || [], { fixture: true }));
});

/* The problem-set fixtures (tools/fixtures/problems, never content): checked like a real set, so the rules run on every validation */
{
  const fxDir = path.join(APP, 'tools', 'fixtures', 'problems');
  let fxs = []; try { fxs = fs.readdirSync(fxDir).filter(f => f.endsWith('.json')).sort(); } catch { /* none */ }
  fxs.forEach(f => {
    const ff = path.join(fxDir, f), fr = readJSON(ff);
    if (!isObj(fr.data)) return;
    const cid = fr.data.course, D = cur.courseDocs[cid];
    if (!D) { err(ff, 'course', `the fixture's course "${cid}" is not a course`); return; }
    guard(ff, () => checkSet(ff, 'problems', cid, fr.data.id, fr.data.level, fr.data, D));
  });
}

/* perf-pending.json: a key that is not a level is stale; one count line for the rest */
[...perfPending].filter(k => !perfStats.levels.has(k)).forEach(k => warn(path.join(path.dirname(fileURLToPath(import.meta.url)), 'perf-pending.json'), k, 'not a level on any course map: remove it'));
if (perfStats.pending) warn('tools/perf-pending.json', '', `${perfStats.pending} rule-matched level${perfStats.pending === 1 ? '' : 's'} have no performance task yet (grandfathered; matched ${perfStats.matched}, with a task ${perfStats.withTask}); see docs/AUTHORING.md section 5`);

/* Exams */
const examDocs = new Map();   // exam id -> { file, versionOf }: the mock version rule below (ENGINE-BACKLOG 547)
const examDir = path.join(CONTENT, 'exams');
listJSON(examDir).forEach(f => {
  const id = f.replace(/\.json$/, ''), file = path.join(examDir, f);
  if (!/^(topic-\d+\.\d+|stage-\d+|mock-[a-z0-9]+(-[a-z0-9]+)*)$/.test(id)) { err(file, '', 'exam files are topic-<topic>.json, stage-<n>.json or mock-<id>.json'); return; }
  const r = readJSON(file); if (!r.data) return;
  manifest.push(`exams/${f}`); noteSample(file, `exams/${f}`, r.data);
  if (holdsSelf(r.data)) selfExams.push(id);
  /* ENGINE-BACKLOG 621: the minutes the exam screen runs (a paper's minutes or 60, summed over the papers), for the Learn chip */
  { const d = r.data, ps = Array.isArray(d.parts) ? d.parts.filter(p => p && p.kind === 'paper') : [d]; examMinutesManifest[id] = ps.reduce((a, p) => a + (+p.minutes || 60), 0); }
  examDocs.set(id, { file, versionOf: r.data && r.data.versionOf });
  guard(file, () => checkExam(file, id, r.data, cur));
});

/* Interview bank */
const bankDir = path.join(CONTENT, 'bank');
listJSON(bankDir).forEach(f => {
  const id = f.replace(/\.json$/, ''), file = path.join(bankDir, f);
  if (!KEBAB.test(id)) { err(file, '', 'bank files are <family>.json, kebab-case'); return; }
  const r = readJSON(file); if (!r.data) return;
  manifest.push(`bank/${f}`); noteSample(file, `bank/${f}`, r.data); bankData.set(id, r.data);
  guard(file, () => checkBank(file, id, r.data, cur));
});

/* ---------- Prep paths: content/prep.json (ENGINE-BACKLOG 455, docs/AUTHORING.md section 10) ---------- */
const PREP_KINDS = ['general', 'stage', 'firm'];
const PREP_STAGES = ['oa', 'interview', 'superday'];
const PREP_TRACKS = ['trader', 'research', 'strats', 'developer'];
const PREP_TOP = ['asOf', 'paths'];
const PREP_PATH = ['id', 'name', 'kind', 'stage', 'track', 'description', 'mocks', 'steps', 'asOf', 'source', 'reported'];
const PREP_STEP = ['ref', 'priority', 'why', 'track'];
const PREP_DATE = /^(\d{4})-(0[1-9]|1[0-2])(-(0[1-9]|[12]\d|3[01]))?$/;
/* A ref names a course, one of its levels or one of its lessons (a lesson listed in course.json counts even when unwritten); returns its lessons or null */
const prepRefLessons = (ref) => {
  if (typeof ref !== 'string') return null;
  const [cid, rest, extra] = ref.split('/');
  const D = cur.courseDocs[cid];
  if (extra !== undefined || !D || !Array.isArray(D.levels)) return null;
  const all = D.levels.flatMap(lv => (Array.isArray(lv.lessons) ? lv.lessons : []).map(l => ({ id: l, level: lv.n })));
  if (rest === undefined) return all.map(x => `${cid}/${x.id}`);
  const m = /^level-(\d+)$/.exec(rest);
  if (m) { const pick = all.filter(x => x.level === +m[1]); return pick.length ? pick.map(x => `${cid}/${x.id}`) : null; }
  return all.some(x => x.id === rest) ? [`${cid}/${rest}`] : null;
};
const checkPrep = (file, doc) => {
  const unknown = (where, o, allowed) => Object.keys(o).forEach(k => { if (!allowed.includes(k)) err(file, where ? `${where}.${k}` : k, `unknown field "${k}" (allowed: ${allowed.join(', ')})`); });
  if (!isObj(doc)) { err(file, '', 'prep.json is an object with asOf and paths'); return; }
  unknown('', doc, PREP_TOP);
  if (typeof doc.asOf !== 'string' || !PREP_DATE.test(doc.asOf)) err(file, 'asOf', 'asOf is required as YYYY-MM-DD (or YYYY-MM): the date the mapping was last checked');
  if (!Array.isArray(doc.paths) || !doc.paths.length) { err(file, 'paths', 'paths is a non-empty array'); return; }
  const ids = new Set(), stageKeys = new Map();
  const monthsOld = (d) => { const m = PREP_DATE.exec(d); const now = new Date(); return (now.getFullYear() - +m[1]) * 12 + (now.getMonth() + 1 - +m[2]) - (m[4] && now.getDate() < +m[4] ? 1 : 0); };
  doc.paths.forEach((p, i) => {
    const at = `paths[${i}]`;
    if (!isObj(p)) { err(file, at, 'a path is an object'); return; }
    unknown(at, p, PREP_PATH);
    req(file, at, p, ['id', 'name', 'kind']);
    if (typeof p.id === 'string') {
      if (!KEBAB.test(p.id)) err(file, `${at}.id`, 'path ids are kebab-case');
      if (ids.has(p.id)) err(file, `${at}.id`, `duplicate path id "${p.id}"`);
      ids.add(p.id);
    }
    checkText(file, `${at}.name`, p.name); checkText(file, `${at}.description`, p.description);
    if (p.description !== undefined && (typeof p.description !== 'string' || !p.description.trim())) err(file, `${at}.description`, 'description is a non-empty string (one or two plain sentences)');
    if (typeof p.description === 'string' && words(p.description) > 40) warn(file, `${at}.description`, 'keep the description to one or two short sentences');
    if (!PREP_KINDS.includes(p.kind)) err(file, `${at}.kind`, `kind is one of ${PREP_KINDS.join(', ')}`);
    if (p.kind === 'stage') {
      if (!PREP_STAGES.includes(p.stage)) err(file, `${at}.stage`, `a stage path needs stage: ${PREP_STAGES.join(', ')}`);
      if (!PREP_TRACKS.includes(p.track)) err(file, `${at}.track`, `a stage path needs track: ${PREP_TRACKS.join(', ')}`);
      const key = `${p.stage}/${p.track}`;
      if (stageKeys.has(key)) err(file, at, `stage "${p.stage}" and track "${p.track}" already have a path (${stageKeys.get(key)})`); else stageKeys.set(key, p.id);
    } else {
      if (p.stage !== undefined) err(file, `${at}.stage`, 'stage belongs only to a stage path');
      if (p.track !== undefined && !PREP_TRACKS.includes(p.track)) err(file, `${at}.track`, `track is one of ${PREP_TRACKS.join(', ')}`);
      if (p.track !== undefined && p.kind === 'general') err(file, `${at}.track`, 'a general path has no track');
    }
    if (p.kind === 'firm') {
      if (typeof p.asOf !== 'string' || !PREP_DATE.test(p.asOf)) err(file, `${at}.asOf`, 'a firm path needs asOf (YYYY-MM or YYYY-MM-DD): when its reported formats were last checked');
      else if (monthsOld(p.asOf) > 12) warn(file, `${at}.asOf`, `reported formats are ${monthsOld(p.asOf)} months old: re-check them and re-date`);
      if (typeof p.source !== 'string' || !p.source) err(file, `${at}.source`, 'a firm path needs source: a lesson or course ref, such as recruiting/l4-firm-by-firm');
      else if (!prepRefLessons(p.source)) err(file, `${at}.source`, `source "${p.source}" is not a course, level or lesson`);
      if (p.reported !== true) err(file, `${at}.reported`, 'a firm path needs reported: true (the formats come from candidate reports)');
    } else {
      if (p.source !== undefined) err(file, `${at}.source`, 'source belongs only to a firm path');
      if (p.reported !== undefined) err(file, `${at}.reported`, 'reported belongs only to a firm path');
      if (p.asOf !== undefined && (typeof p.asOf !== 'string' || !PREP_DATE.test(p.asOf))) err(file, `${at}.asOf`, 'asOf is YYYY-MM or YYYY-MM-DD');
    }
    if (p.mocks !== undefined) {
      if (!Array.isArray(p.mocks)) err(file, `${at}.mocks`, 'mocks is a list of mock exam ids');
      else {
        const seen = new Set();
        p.mocks.forEach(m => {
          if (typeof m !== 'string' || !/^mock-[a-z0-9]+(-[a-z0-9]+)*$/.test(m)) err(file, `${at}.mocks`, `"${m}" is not a mock id (mock- then kebab-case words)`);
          else if (seen.has(m)) err(file, `${at}.mocks`, `duplicate mock "${m}"`);
          seen.add(m);
        });
      }
    }
    if (!Array.isArray(p.steps)) { err(file, `${at}.steps`, 'steps is a list (it may be empty while the path is being written)'); return; }
    if (!p.steps.length) warn(file, `${at}.steps`, 'no steps yet');
    const seenRef = new Set(), lessonAt = new Map();
    p.steps.forEach((st, j) => {
      const sat = `${at}.steps[${j}]`;
      if (!isObj(st)) { err(file, sat, 'a step is an object'); return; }
      unknown(sat, st, PREP_STEP);
      req(file, sat, st, ['ref', 'priority', 'why']);
      if (st.priority !== undefined && st.priority !== 'must' && st.priority !== 'should') err(file, `${sat}.priority`, 'priority is "must" or "should"');
      if (st.track !== undefined && !PREP_TRACKS.includes(st.track)) err(file, `${sat}.track`, `track is one of ${PREP_TRACKS.join(', ')}`);
      if (typeof st.why === 'string') {
        checkText(file, `${sat}.why`, st.why);
        if (words(st.why) >= 20) err(file, `${sat}.why`, `why is a line of under 20 words (found ${words(st.why)})`);
      } else if (st.why !== undefined) err(file, `${sat}.why`, 'why is a string');
      if (typeof st.ref !== 'string') { if (st.ref !== undefined) err(file, `${sat}.ref`, 'ref is a string'); return; }
      const ls = prepRefLessons(st.ref);
      if (!ls) err(file, `${sat}.ref`, `ref "${st.ref}" is not a course, "<course>/level-<n>" or "<course>/<lesson-id>" listed in a course.json`);
      else {
        if (seenRef.has(st.ref)) err(file, `${sat}.ref`, `ref "${st.ref}" appears twice in this path`);
        seenRef.add(st.ref);
        ls.forEach(l => { if (lessonAt.has(l) && lessonAt.get(l) !== j) warn(file, `${sat}.ref`, `"${l}" is already in step ${lessonAt.get(l) + 1} of this path`); else lessonAt.set(l, j); });
      }
    });
  });
};
const prepFile = PREP_FILE || path.join(CONTENT, 'prep.json');
const prepDoc = readJSON(prepFile);
if (prepDoc.data) { guard(prepFile, () => checkPrep(prepFile, prepDoc.data)); if (!PREP_FILE) manifest.push('prep.json'); }
else if (prepDoc.missing && PREP_FILE) err(prepFile, '', 'the file given to --prep does not exist');

/* Mock versions (ENGINE-BACKLOG 547, docs/AUTHORING.md section 5 "Versions"): a fixed version of a mock is its own file named
   <base>-<n> with "versionOf": "<base>". The prep screen groups the versions under the base mock the paths name, so each version
   must declare its base, the base must exist, and every version must be reachable: its base is named by a prep path. */
{
  const named = new Set(prepDoc.data && Array.isArray(prepDoc.data.paths) ? prepDoc.data.paths.flatMap(p => (p && Array.isArray(p.mocks) ? p.mocks : [])) : []);
  examDocs.forEach(({ file, versionOf }, id) => {
    if (!/^mock-/.test(id)) { if (versionOf !== undefined) err(file, 'versionOf', 'versionOf belongs only to a mock'); return; }
    const m = /^(mock-.+)-(\d+)$/.exec(id), base = m && examDocs.has(m[1]) ? m[1] : null;
    if (versionOf !== undefined) {
      if (typeof versionOf !== 'string' || !examDocs.has(versionOf)) err(file, 'versionOf', `versionOf "${versionOf}" is not a mock exam file`);
      else if (id !== versionOf + '-' + (m ? m[2] : '')) err(file, 'versionOf', `a version of ${versionOf} is named ${versionOf}-<n>, not ${id}`);
      else if (/^[01]$/.test(m[2])) err(file, 'versionOf', 'version numbers start at 2: the base mock is version 1');
    }
    if (base && versionOf !== base && versionOf === undefined) err(file, 'versionOf', `${id} looks like a version of ${base}: add "versionOf": "${base}"`);
    const b = versionOf !== undefined ? versionOf : base;
    if (b && examDocs.has(b) && !named.has(b)) err(file, 'versionOf', `${id} is unreachable from prep: no path names its base ${b}, so the Prepare screen never offers it`);
  });
}

/* Readiness: content/readiness.json is generated by tools/readiness-sums.mjs --write; here only its shape is checked */
{
  const rf = path.join(CONTENT, 'readiness.json'), rd = readJSON(rf);
  if (rd.data) {
    const d = rd.data, KEYS = ['trader', 'researcher', 'developer', 'strats', 'strats-deriv', 'undecided'];
    const courseIds = fs.readdirSync(path.join(CONTENT, 'courses')).filter(x => fs.existsSync(path.join(CONTENT, 'courses', x, 'course.json')));
    guard(rf, () => {
      if (!isObj(d) || !isObj(d.roles)) { err(rf, '', 'readiness.json is an object with roles'); return; }
      KEYS.forEach(k => {
        const r = d.roles[k];
        if (!isObj(r) || !isObj(r.courses) || !isObj(r.totals) || !isObj(r.mocks)) { err(rf, `roles.${k}`, 'needs courses, totals and mocks'); return; }
        courseIds.forEach(c => { if (!['required', 'recommended', 'optional'].includes(r.courses[c])) err(rf, `roles.${k}.courses.${c}`, 'status must be required, recommended or optional'); });
        Object.keys(r.courses).forEach(c => { if (!courseIds.includes(c)) err(rf, `roles.${k}.courses.${c}`, 'unknown course'); });
        ['required', 'recommended', 'header'].forEach(t => { if (!isObj(r.totals[t]) || typeof r.totals[t].total !== 'number' || typeof r.totals[t].hours !== 'number') err(rf, `roles.${k}.totals.${t}`, 'needs numeric total and hours'); });
      });
      Object.keys(d.limited || {}).forEach(c => { if (!courseIds.includes(c)) err(rf, `limited.${c}`, 'unknown course'); });
    });
    manifest.push('readiness.json');
  }
}

/* Capstone records (ENGINE-BACKLOG 565): content/capstones.json is optional; when present its shape is checked by tools/capstone-rules.mjs */
{
  const cf = path.join(CONTENT, 'capstones.json');
  if (fs.existsSync(cf)) {
    const cr = readJSON(cf);
    if (cr.data !== undefined && cr.data !== null) { guard(cf, () => checkCapstones(cr.data).forEach(x => err(cf, x.where, x.msg))); manifest.push('capstones.json'); }
  }
}

/* Drills */
const drillDir = path.join(CONTENT, 'drills');
const idxFile = path.join(drillDir, 'index.json');
const idx = readJSON(idxFile);
const listed = new Set();
if (idx.missing) warn(idxFile, '', 'drills/index.json is missing; the drill list will be empty');
else if (idx.data && !Array.isArray(idx.data)) err(idxFile, '', 'index.json is an array of drill ids or { id, ... } entries');
else (idx.data || []).forEach((e, i) => { const id = typeof e === 'string' ? e : e && e.id; if (!id) err(idxFile, `[${i}]`, 'entry needs an id'); else listed.add(id); });
const drillMeta = {}; // item 472: language, pattern, pace, tags and sample of each drill file, for manifest.drills
const drillIds = new Set(listJSON(drillDir).filter(f => f !== 'index.json').map(f => f.replace(/\.json$/, '')));
listJSON(drillDir).filter(f => f !== 'index.json').forEach(f => {
  const id = f.replace(/\.json$/, ''), file = path.join(drillDir, f);
  const r = readJSON(file); if (!r.data) return;
  manifest.push(`drills/${f}`); const isSample = noteSample(file, `drills/${f}`, r.data); drillData.set(id, r.data);
  guard(file, () => checkDrill(file, id, r.data, cur));
  const D = r.data, meta = {};
  if (D && typeof D === 'object') {
    if (D.language === 'cpp') meta.language = 'cpp';
    if (typeof D.pattern === 'string') meta.pattern = D.pattern;
    if (typeof D.pace === 'number') meta.pace = D.pace;
    if (Array.isArray(D.tags)) meta.tags = D.tags;
    if (D.sample === true) meta.sample = true;
    if (typeof D.pack === 'string') meta.pack = D.pack;                  // ENGINE-BACKLOG 568: an oa drill counts toward its level's code task
    if (D.level !== undefined) { if (!Number.isInteger(D.level) || D.level < 1) err(file, 'level', 'level is a whole number from 1: the level of its course whose code performance task a verified oa drill counts toward'); else meta.level = D.level; }
    if (Object.keys(meta).length) drillMeta[id] = meta;
  }
  if (!listed.has(id) && !isSample) warn(file, '', 'drill is not listed in drills/index.json');
  listed.delete(id);
});
listed.forEach(id => err(idxFile, '', `drill "${id}" is listed but drills/${id}.json does not exist`));
listJSON(path.join(drillDir, 'sessions')).forEach(f => {
  const id = f.replace(/\.json$/, ''), file = path.join(drillDir, 'sessions', f);
  const r = readJSON(file); if (!r.data) return;
  manifest.push(`drills/sessions/${f}`); noteSample(file, `drills/sessions/${f}`, r.data);
  guard(file, () => checkDrillSession(file, id, r.data, drillIds));
});

/* ---------- Prerequisites (ENGINE-BACKLOG 488, docs/AUTHORING.md section 11) ----------
   level.requires and course.json lessonRequires and a mock's requires: references "<course>/L<n>" (a whole level) or
   "<course>/<lesson-id>". Errors: unknown course, level or lesson, a level requiring itself, a reference from an earlier stage to a later one,
   a cycle (printed). Warnings: a reference to a later topic in the same stage, to a level or lesson that is not written yet, and a written
   level whose implicit previous level has no written lesson. Topics and stages carry no requires. */
guard(courseDir, () => {
  const REF = /^([a-z0-9]+(?:-[a-z0-9]+)*)\/(L[1-9]\d*|[a-z0-9]+(?:-[a-z0-9]+)*)$/;
  const topicIdx = new Map();
  (C.stages || []).forEach(st => (st.topics || []).forEach((t, j) => topicIdx.set(t.id, j)));
  const stageOf = (cid) => (cur.topics.get(cur.courseTopic[cid]) || {}).stage;
  const levelsOf = (cid) => (Array.isArray((cur.courseDocs[cid] || {}).levels) ? cur.courseDocs[cid].levels : []);
  const lessonLevel = (cid, l) => levelsOf(cid).find(lv => Array.isArray(lv.lessons) && lv.lessons.includes(l));
  const writtenIn = (cid, lv) => (lv.lessons || []).filter(l => (writtenByCourse.get(cid) || new Set()).has(l));
  let crossEdges = 0, crossNoWhy = 0;
  const edges = new Map(), where = new Map();   // node "course/L<n>" -> Set of nodes it requires; node -> course.json path
  const addEdge = (a, b) => { if (a === b) return; (edges.get(a) || edges.set(a, new Set()).get(a)).add(b); };
  /* Checks a list of references and returns their level nodes. fromCid and fromNode are null for a mock. */
  /* An entry is a string or { ref, why, gate }. gate: false makes it a diagnostic (shown as "Check first", never locks) and needs a why.
     why: one line, under 20 words, no em-dash. Exam files take plain strings (objectsOk false). The engine normaliser is js/prereq.js (entriesOf). */
  const checkWhy = (file, w, why) => {
    if (typeof why !== 'string' || !why.trim()) { err(file, w, 'why is a non-empty string'); return; }
    if (/[\r\n]/.test(why)) err(file, w, 'why is one line (no line break)');
    if (why.trim().split(/\s+/).length >= 20) err(file, w, `why is ${why.trim().split(/\s+/).length} words; keep it under 20`);
    if (/\u2014/.test(why)) err(file, w, 'why has an em-dash; use a comma, colon or full stop');
  };
  const checkRefs = (file, at, refs, fromCid, fromNode, objectsOk = true) => {
    if (!Array.isArray(refs)) { err(file, at, 'requires is a list of "<course>/L<n>" or "<course>/<lesson-id>" strings, or { "ref", "why", "gate" } objects'); return []; }
    const out = [], seenRef = new Set();
    refs.forEach((entry, k) => {
      const w = `${at}[${k}]`;
      let r = entry, why;
      if (entry && typeof entry === 'object' && !Array.isArray(entry)) {
        if (!objectsOk) { err(file, w, 'an exam file takes plain "<course>/L<n>" strings; { ref, why } objects are for course.json'); return; }
        const bad = Object.keys(entry).filter(x => !['ref', 'why', 'gate'].includes(x));
        if (bad.length) err(file, w, `unknown key ${bad.join(', ')}; an entry has ref, why and optionally gate`);
        r = entry.ref; why = entry.why;
        if (entry.why !== undefined) checkWhy(file, `${w}.why`, entry.why);
        if (entry.gate !== undefined && typeof entry.gate !== 'boolean') err(file, `${w}.gate`, 'gate is true or false');
        if (entry.gate === false && (typeof entry.why !== 'string' || !entry.why.trim())) err(file, `${w}.gate`, 'gate: false (a diagnostic) needs a why, which the learner reads as "Check first"');
      }
      const m = typeof r === 'string' ? REF.exec(r) : null;
      if (!m) { err(file, w, `${JSON.stringify(r)} is not "<course>/L<n>" or "<course>/<lesson-id>"`); return; }
      if (seenRef.has(r)) { warn(file, w, `"${r}" is listed twice`); return; }
      seenRef.add(r);
      const [, c, rest] = m;
      if (fromCid && c !== fromCid) {
        crossEdges++;
        if (typeof why !== 'string' || !why.trim()) { crossNoWhy++; (STRICT_WHY ? err : warn)(file, w, `cross-course requires "${r}" has no why: add { "ref": "${r}", "why": "<one line>" }`); }
      }
      if (!C.courses || !C.courses[c] || !cur.courseDocs[c]) { err(file, w, `unknown course "${c}"`); return; }
      let node, lv, lessonRef = null;
      if (/^L\d+$/.test(rest)) {
        lv = levelsOf(c).find(x => x.n === +rest.slice(1));
        if (!lv) { err(file, w, `${c} has no level ${rest.slice(1)}`); return; }
        node = `${c}/L${lv.n}`;
        if (!writtenIn(c, lv).length) warn(file, w, `"${r}" has no written lesson yet: the dependent stays locked until it is written`);
      } else {
        lv = lessonLevel(c, rest);
        if (!lv) { err(file, w, `${c} has no lesson "${rest}" on its course map`); return; }
        node = `${c}/L${lv.n}`; lessonRef = rest;
        if (!(writtenByCourse.get(c) || new Set()).has(rest)) warn(file, w, `lesson "${rest}" is not written yet: the dependent stays locked until it is written`);
      }
      if (fromNode && node === fromNode && (!lessonRef || !/^lessonRequires/.test(at))) { err(file, w, lessonRef ? `a level cannot require its own lesson "${lessonRef}" (the level locks the lesson)` : 'a level cannot require itself'); return; }
      if (fromCid) {
        const sf = stageOf(fromCid), st = stageOf(c);
        if (st > sf) err(file, w, `"${r}" is in Stage ${st}, later than this course's Stage ${sf}: a reference never points to a later stage`);
        else if (st === sf) {
          const tf = topicIdx.get(cur.courseTopic[fromCid]), tt = topicIdx.get(cur.courseTopic[c]);
          if (tt > tf) warn(file, w, `"${r}" is in topic ${cur.courseTopic[c]}, later than this course's topic ${cur.courseTopic[fromCid]} in Stage ${sf}`);
        }
      }
      out.push(node);
    });
    return out;
  };
  Object.keys(C.courses || {}).forEach(cid => {
    const D = cur.courseDocs[cid]; if (!D) return;
    const file = path.join(courseDir, cid, 'course.json');
    where.set(cid, file);
    const levels = levelsOf(cid);
    levels.forEach((lv, i) => {
      const at = `levels[${i}]`, node = `${cid}/L${lv.n}`;
      if (lv.requires !== undefined) checkRefs(file, `${at}.requires`, lv.requires, cid, node).forEach(n => addEdge(node, n));
      else if (i > 0) {
        addEdge(node, `${cid}/L${levels[i - 1].n}`);
        if (writtenIn(cid, lv).length && !writtenIn(cid, levels[i - 1]).length) warn(file, `${at}`, `written, but its implicit prerequisite level ${levels[i - 1].n} has no written lesson, so it stays locked`);
      }
    });
    if (D.lessonRequires !== undefined) {
      if (!isObj(D.lessonRequires)) err(file, 'lessonRequires', 'lessonRequires is { "<lesson-id>": ["<course>/L<n>", ...] }');
      else Object.entries(D.lessonRequires).forEach(([l, refs]) => {
        const lv = lessonLevel(cid, l);
        if (!lv) { err(file, `lessonRequires.${l}`, `"${l}" is not a lesson on this course map`); return; }
        checkRefs(file, `lessonRequires.${l}`, refs, cid, `${cid}/L${lv.n}`).forEach(n => addEdge(`${cid}/L${lv.n}`, n));
      });
    }
  });
  /* Cycles across all courses: the first one found from each unvisited node is printed */
  const state = new Map(), stack = [], reported = new Set();
  const visit = (n) => {
    state.set(n, 1); stack.push(n);
    for (const m of edges.get(n) || []) {
      if (state.get(m) === 1) {
        const cyc = stack.slice(stack.indexOf(m)).concat(m), key = [...new Set(cyc)].sort().join('|');
        if (!reported.has(key)) { reported.add(key); err(where.get(m.split('/')[0]) || courseDir, 'requires', `prerequisite cycle: ${cyc.join(' -> ')}`); }
      } else if (!state.get(m)) visit(m);
    }
    stack.pop(); state.set(n, 2);
  };
  [...edges.keys()].sort().forEach(n => { if (!state.get(n)) visit(n); });
  /* An exam file (mock, topic exam or stage test) may name requires at its top level; the engine honours it on any of them */
  listJSON(path.join(CONTENT, 'exams')).forEach(f => {
    const ef = path.join(CONTENT, 'exams', f), er = readJSON(ef);
    if (!er.data || er.data.requires === undefined) return;
    if (!/^mock-/.test(f)) warn(ef, 'requires', 'a topic exam or stage test is how a learner tests out; locking it behind requires removes that way round');
    checkRefs(ef, 'requires', er.data.requires, null, null, false);
  });
  console.log(`Requires: ${crossEdges} cross-course edges, ${crossNoWhy} without why (${STRICT_WHY ? 'errors' : 'warnings, --lax-why'})`);
});

/* Draw sources (ENGINE-BACKLOG 468): every `from` must name files, and enough items must match the tags and difficulty. A sample exam may
   draw from sample files too; any other exam draws from real files only (the engine reads the same rule). */
/* mirrors drillItem in js/engine/mock.js: the drill's tags, then its pattern (so a draw can filter by pattern and the family stays the first tag) */
const drillTags = (d) => {
  const t = (Array.isArray(d.tags) ? d.tags : []).filter(x => typeof x === 'string');
  const pat = [d.pattern, ...(Array.isArray(d.patterns) ? d.patterns : [d.patterns])].filter(x => typeof x === 'string').slice(0, 1);
  const all = [...t, ...pat.filter(x => !t.includes(x))];
  return all.length ? all : [d.pack, d.id].filter(x => typeof x === 'string').slice(0, 1);
};
const verifyDraws = () => {
  const papers = new Map();   // exam file -> { pool: Set of uids matched by any entry, sum of n }: the entries of an exam share one `used` set (mock.js), so overlapping pools cannot be drawn twice
  drawRefs.forEach(({ file, at, d, sample }) => {
    if (typeof d.from !== 'string' || !/^(bank|drills)\//.test(d.from)) return;   // a malformed "from" is reported where it is written
    const [kind, name] = d.from.split('/'), want = Array.isArray(d.tags) ? d.tags : [];
    const band = Array.isArray(d.difficulty) ? d.difficulty : Number.isInteger(d.difficulty) ? [d.difficulty, d.difficulty] : null;
    const keep = (tags, diff) => (!want.length || (Array.isArray(tags) && tags.some(t => want.includes(t)))) && (!band || (diff >= band[0] && diff <= band[1]));
    let files = 0, items = 0;
    const uids = [];
    if (kind === 'bank') {
      bankData.forEach((doc, id) => {
        if (!(name === '*' || id === name || id.startsWith(name + '-')) || (doc.sample === true && !sample)) return;
        files++; (Array.isArray(doc.items) ? doc.items : []).forEach(it => { if (isObj(it) && keep(it.tags, it.difficulty)) { items++; uids.push(`bank/${id}/${it.id}`); } });
      });
    } else if (kind === 'drills') {
      drillData.forEach((doc, id) => {
        if (!(name === '*' || doc.pack === name || doc.id === name || String(doc.id).startsWith(name + '-')) || (doc.sample === true && !sample)) return;
        files++; if (keep(drillTags(doc), doc.difficulty)) { items++; uids.push(`drills/${id}`); }
      });
    }
    if (!files) err(file, `${at}.from`, `"${d.from}" matches no ${kind === 'bank' ? 'bank file' : 'drill'}${sample ? '' : ' (sample files are drawn only by a sample exam)'}`);
    else if (items < d.n) err(file, `${at}.n`, `draws ${d.n} but only ${items} item${items === 1 ? '' : 's'} in ${d.from} match the tags and difficulty`);
    else {
      const key = file, P = papers.get(key) || { pool: new Set(), n: 0, file, at: 'draw', entries: 0 };
      uids.forEach(u => P.pool.add(u)); P.n += Number.isInteger(d.n) ? d.n : 0; P.entries++; papers.set(key, P);
    }
    if (files && items >= d.n && items < 2 * d.n) warn(file, `${at}.n`, `only ${items} items match for a draw of ${d.n}: a resit repeats items (aim for at least twice n)`);
  });
  papers.forEach(P => { if (P.entries > 1 && P.n > P.pool.size) err(P.file, P.at, `the entries draw ${P.n} items in all but their pools hold only ${P.pool.size} different items between them (an item is drawn once an exam): the later entries come up short`); });
};
guard(path.join(CONTENT, 'exams'), verifyDraws);

/* Warm-up settings */
const wu = readJSON(path.join(CONTENT, 'warmup.json'));
if (wu.missing) warn(path.join(CONTENT, 'warmup.json'), '', 'warmup.json is missing');
else if (wu.data) { req(path.join(CONTENT, 'warmup.json'), '', wu.data, ['seconds', 'operations']); }

/* O2 rules (ENGINE-BACKLOG 523 to 527): recurring finding classes, warnings only, one code each */
const o2Counts = Object.fromEntries(O2_CODES.map(c => [c, 0]));
{
  const walkJSON = function* (d) { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const q = path.join(d, e.name); if (e.isDirectory()) yield* walkJSON(q); else if (e.name.endsWith('.json') && e.name !== 'manifest.json') yield q; } };
  for (const f of walkJSON(CONTENT)) {
    let j; try { j = JSON.parse(fs.readFileSync(f, 'utf8')); } catch { continue; }
    scanO2(j, (code, where, msg) => { o2Counts[code]++; warn(f, where, `[${code}] ${msg}`); });
  }
}

/* ---------- Output ---------- */
const errors = problems.filter(p => p.level === 'error'), warnings = problems.filter(p => p.level === 'warning');
for (const p of [...errors, ...warnings]) console.log(`${p.level.padEnd(7)} ${p.file}${p.where ? '  ' + p.where : ''}: ${p.msg}`);

if (SUMMARY) {
  console.log('\nLessons per course (written / mapped; reviews and homework written / levels)');
  let tl = 0, tw = 0;
  summary.forEach(s => {
    tl += s.lessons; tw += s.written;
    console.log(`  ${s.topic.padEnd(4)} ${s.cid.padEnd(16)} ${String(s.written).padStart(3)} / ${String(s.lessons).padEnd(3)} lessons in ${s.levels} levels   reviews ${s.reviews}/${s.levels}   homework ${s.homework}/${s.levels}`);
  });
  console.log(`  total: ${tw} of ${tl} lessons written across ${summary.length} courses`);
  console.log('\nMapped but not yet written');
  summary.filter(s => s.unwritten.length).forEach(s => {
    console.log(`  ${s.cid} (${s.unwritten.length}):`);
    for (let i = 0; i < s.unwritten.length; i += 4) console.log('    ' + s.unwritten.slice(i, i + 4).join(', '));
  });
}

if (!errors.length && WRITE_MANIFEST) {
  const mf = path.join(CONTENT, 'manifest.json');
  const body = JSON.stringify({ note: 'Written by tools/validate.mjs: every authored lesson, review, homework, exam, bank and drill file. js/content.js reads it so it never requests a file that does not exist. Run the validator after adding content. selfExams lists the exams that hold a self-marked item or a check part. examMinutes gives the minutes each exam runs. sessions lists the workshop and project lessons with their true minutes. lessonMinutes gives the authored minutes of every lesson and setMinutes the minutes a review or homework file states (the in-app hours). perf lists the levels that carry a performance task. samples lists the engine sample files (sample: true), which every learner-facing list leaves out.', files: manifest.sort(), samples: samples.slice().sort(), selfExams: selfExams.slice().sort(), examMinutes: Object.fromEntries(Object.keys(examMinutesManifest).sort().map(k => [k, examMinutesManifest[k]])), sessions: Object.fromEntries(Object.keys(sessionManifest).sort().map(k => [k, sessionManifest[k]])), lessonMinutes: Object.fromEntries(Object.keys(lessonMinutesManifest).sort().map(k => [k, lessonMinutesManifest[k]])), setMinutes: Object.fromEntries(Object.keys(setMinutesManifest).sort().map(k => [k, setMinutesManifest[k]])), perf: Object.fromEntries(Object.keys(perfManifest).sort().map(k => [k, perfManifest[k]])), drills: Object.fromEntries(Object.keys(drillMeta).sort().map(k => [k, drillMeta[k]])), ...(Object.keys(fluencyManifest).length ? { fluency: Object.fromEntries(Object.keys(fluencyManifest).sort().map(k => [k, fluencyManifest[k]])) } : {}), ...(Object.keys(problemsManifest).length ? { problems: Object.fromEntries(Object.keys(problemsManifest).sort().map(k => [k, problemsManifest[k]])) } : {}) }, null, 2) + '\n';
  let old = ''; try { old = fs.readFileSync(mf, 'utf8'); } catch { /* first run */ }
  if (old !== body) { fs.writeFileSync(mf, body); console.log(`manifest: wrote content/manifest.json (${manifest.length} files)`); }
}
console.log('\nO2 warnings: ' + O2_CODES.map(c => `${c} ${o2Counts[c]}`).join(', '));
console.log(`perf-optional-row warnings: ${perfOptionalRows}`);
console.log(`\n${errors.length} error${errors.length === 1 ? '' : 's'}, ${warnings.length} warning${warnings.length === 1 ? '' : 's'}`);
process.exitCode = errors.length ? 1 : 0; // not process.exit(): it truncates large piped stdout (merge-wave capture)
