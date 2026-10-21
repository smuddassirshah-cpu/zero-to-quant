#!/usr/bin/env node
/* Content validator for Zero to Quant (docs/AUTHORING.md section 7, docs/PLAN.md section 11). Node, no dependencies.

   node tools/validate.mjs              validate everything under content/, print one line per problem, exit 1 on any error
   node tools/validate.mjs --summary    also print lesson counts per course and every mapped lesson not yet written
   node tools/validate.mjs --no-manifest   do not rewrite content/manifest.json

   It loads curriculum.json, every course.json, every lesson, level review, homework, exam and drill file, and checks
   the schema and the semantic rules. Missing lesson, review and homework files are warnings (they show as "Not yet
   written" in the app). When there are no errors it refreshes content/manifest.json, the list of authored files that
   js/content.js reads so the app never requests a file that is not there. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');
const CONTENT = path.join(APP, 'content');
const args = new Set(process.argv.slice(2));
const SUMMARY = args.has('--summary');
const WRITE_MANIFEST = !args.has('--no-manifest');

/* ---------- Reporting ---------- */
const problems = [];
const rel = (f) => path.relative(APP, f) || f;
const err = (file, where, msg) => problems.push({ level: 'error', file: rel(file), where, msg });
const warn = (file, where, msg) => problems.push({ level: 'warning', file: rel(file), where, msg });

/* ---------- Vocabulary ---------- */
const KEBAB = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const WIDGETS = new Set(['choice', 'multi', 'numeric', 'expression', 'slider', 'sliders', 'drag-point', 'place', 'tap-regions', 'order', 'table', 'manipulate', 'balance', 'sketch', 'code', 'longform']);
const CANVASES = new Set(['pair', 'grid', 'tree', 'venn', 'number-line', 'boxes', 'area', 'balance', 'circle', 'plane', 'bars', 'distribution', 'scatter', 'series', 'walk', 'matrix', 'vectors', 'graph', 'array', 'payoff', 'orderbook', 'table', 'console']);
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
const CPP_TYPES = ['int', 'long long', 'double', 'bool', 'std::string', 'std::vector<int>', 'std::vector<double>', 'std::vector<std::string>', 'std::vector<std::vector<double>>'];
const cppValue = (v) => (typeof v === 'number' && Number.isFinite(v)) || typeof v === 'boolean' || typeof v === 'string' || (Array.isArray(v) && v.every(cppValue));
const cppNumbers = (v) => (typeof v === 'number' && Number.isFinite(v)) || (Array.isArray(v) && v.every(cppNumbers));
const cppCodeWidget = (file, where, w) => {
  if (!Array.isArray(w.tests) || w.tests.length < 3) err(file, `${where}.tests`, 'at least 3 tests');
  else if (w.tests.length > 15) err(file, `${where}.tests`, 'at most 15 tests');
  if (w.examples != null && !Array.isArray(w.examples)) err(file, `${where}.examples`, 'examples is a list of cases');
  const cases = [...(Array.isArray(w.tests) ? w.tests.map((t, i) => [t, `${where}.tests[${i}]`]) : []), ...(Array.isArray(w.examples) ? w.examples.map((t, i) => [t, `${where}.examples[${i}]`]) : [])];
  const isOut = (t) => t.compare === 'stdout' || (t.call == null && t.expect != null && t.compare == null);
  const objs = cases.filter(([t]) => t && typeof t === 'object');
  const script = objs.some(([t]) => isOut(t) || t.stdin != null || t.argv != null || (t.compare === 'raises' && t.call == null));
  cases.forEach(([t, at]) => {
    if (!t || typeof t !== 'object') { err(file, at, 'each case is an object'); return; }
    if (t.compare && !['isclose', 'equal', 'stdout', 'raises'].includes(t.compare)) err(file, `${at}.compare`, 'a C++ case compares isclose, equal, stdout or raises');
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
      if (typeof t.expect !== 'string') err(file, `${at}.expect`, 'a stdout case needs expect: the printed text, as a string ("Return: 5.00%\\n")');
      if (t.call != null) err(file, `${at}.call`, 'a stdout case has no call (it compares what the whole program prints)');
    } else {
      if (typeof t.call !== 'string' || !t.call.trim()) err(file, `${at}.call`, 'a value case needs call: a C++ expression ("mean({1.0, 2.0})") or a function name with args');
      if (t.expect === undefined || t.expect === null) err(file, `${at}.expect`, 'a value case needs expect, a JSON value (2.5, true, "abc", [1, 2])');
      else if (!cppValue(t.expect)) err(file, `${at}.expect`, 'expect is a number, a boolean, a string or a list of those');
      else if (t.compare === 'isclose' && !cppNumbers(t.expect)) err(file, `${at}.expect`, 'isclose needs a number (or a list of numbers) as expect, not text: write 2.5, not "2.5"');
      else if (typeof t.expect === 'string' && /^-?\d+(\.\d+)?([eE][+-]?\d+)?$/.test(t.expect.trim())) warn(file, `${at}.expect`, `expect is the text "${t.expect}"; C++ cases take JSON values, so a number is written without quotes`);
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

/* A canvas the learner can work without a widget: points with drag: true (plane, number-line), vectors in state.drag,
   or a simulation's run chips (bars, walk) */
const authorMovable = (c) => {
  if (isObj(c) && c.kind === 'pair') return authorMovable(c.left) || authorMovable(c.right) || (Array.isArray(c.controls) && c.controls.length > 0);
  if (isObj(c) && c.kind === 'circle' && ((isObj(c.state) && c.state.drag === true) || (isObj(c.params) && c.params.drag === true))) return true;
  const st = isObj(c && c.state) ? c.state : {}, p = isObj(c && c.params) ? c.params : {};
  return (Array.isArray(st.points) && st.points.some(q => isObj(q) && q.drag === true)) || (Array.isArray(st.drag) && st.drag.length > 0) || isObj(p.sim);
};

/* ---------- Canvas ids ---------- */
const range = (a, b) => Array.from({ length: Math.max(0, b - a + 1) }, (_, i) => a + i);
const regionIds = (canvas) => {
  if (!isObj(canvas)) return null;
  if (canvas.kind === 'pair') { // the side widgets drive, plus every id of either side with its "left:" or "right:" prefix
    const a = ['left', 'right'].includes(canvas.active) ? canvas.active : 'left', out = new Set();
    ['left', 'right'].forEach(k => { const ids = regionIds(canvas[k]); if (ids) ids.forEach(id => { out.add(`${k}:${id}`); if (k === a) out.add(id); }); });
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
  if ((canvas.kind === 'number-line' || canvas.kind === 'plane') && Array.isArray((canvas.state || {}).points)) {
    const ids = new Set(canvas.state.points.map(q => q && q.id).filter(Boolean)); // tap mode on points
    if (canvas.kind === 'plane') { (canvas.state.segments || []).concat(canvas.state.vectors || [], canvas.state.vlines || [], canvas.state.hlines || [], (canvas.params || {}).functions || []).forEach(q => { if (isObj(q) && q.id) ids.add(q.id); }); ['tangent', 'area', 'riemann', 'target', 'sketch'].forEach(k => ids.add(k)); }
    return ids;
  }
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
  walk: /^(path\d+|barrier-up|barrier-down)$/,
  orderbook: /^(bid\d+|ask\d+|spread)$/,
  distribution: /^(mean|median|sd|prob|curve|cdf|rug|shade\d*|observed\d*|x-?[\d.]+|overlay\d+)$/,
  scatter: /^(p\d+|line)$/,
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
  /* Shapes first, so a field of the wrong type is one error line and never a crash further down */
  const LISTS = ['options', 'among', 'tokens', 'slots', 'lines', 'points', 'wrong', 'tests', 'examples', 'moves', 'rubric', 'order', 'same'];
  const badShape = LISTS.filter(f => w[f] != null && !Array.isArray(w[f]));
  if (['tap-regions', 'order'].includes(w.kind) && w.answer != null && !Array.isArray(w.answer)) badShape.push('answer');
  if (w.kind === 'expression' && w.accept != null && !Array.isArray(w.accept)) badShape.push('accept');
  if (w.kind === 'place' && w.mode === 'boxes' && w.answer != null && (!isObj(w.answer) || Object.values(w.answer).some(v => !Array.isArray(v)))) badShape.push('answer');
  if (badShape.length) { badShape.forEach(f => err(file, `${where}.${f}`, f === 'answer' && w.kind === 'place' ? 'answer must map each container id to a list of item ids' : `${f} must be a list`)); keys.add('*'); return keys; }
  if (['options', 'tokens', 'slots', 'lines', 'points', 'wrong'].some(f => (w[f] || []).some(x => !isObj(x)))) { err(file, where, 'every entry of options, tokens, slots, lines, points and wrong is an object'); keys.add('*'); return keys; }
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
      if (w.kind === 'multi' && ctx.question != null && !/select all that apply/i.test(ctx.question)) warn(file, where, 'a multi question should say "Select all that apply"');
      break;
    }
    case 'numeric':
      if (typeof w.answer !== 'number' || !Number.isFinite(w.answer)) err(file, `${where}.answer`, 'numeric answer must be a number');
      tol(w.tol, `${where}.tol`);
      ids(w.wrong, 'wrong').forEach(k => keys.add(String(k)));
      (w.wrong || []).forEach((x, i) => { if (typeof x.value !== 'number') err(file, `${where}.wrong[${i}].value`, 'must be a number'); if (x.tol) tol(x.tol, `${where}.wrong[${i}].tol`); });
      text(w.accept, `${where}.accept`);
      break;
    case 'expression':
      if (typeof w.answer !== 'string' || !w.answer) err(file, `${where}.answer`, 'expression answer must be a TeX string');
      if (!Array.isArray(w.accept) || !w.accept.length) warn(file, `${where}.accept`, 'list the accepted plain-text forms for the fallback grader');
      ids(w.wrong, 'wrong').forEach(k => keys.add(String(k)));
      checkText(file, `${where}.answer`, `$${w.answer || ''}$`, { copy: false });
      if (w.form != null) { if (!['expanded', 'factorised', 'simplified'].includes(w.form)) err(file, `${where}.form`, 'form is "expanded", "factorised" or "simplified"'); keys.add('form'); }
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
    case 'tap-regions': {
      const countMode = w.count != null;
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
      if (!Array.isArray(a) || a.length !== lines.size || new Set(a).size !== a.length || a.some(x => !lines.has(x))) err(file, `${where}.answer`, 'answer must be a permutation of the line ids');
      (w.lines || []).forEach((l, i) => text(l.text, `${where}.lines[${i}].text`));
      if (w.same != null) { const gs = Array.isArray(w.same) && w.same.length && Array.isArray(w.same[0]) ? w.same : [w.same]; gs.forEach((g, i) => { if (!Array.isArray(g) || g.length < 2 || g.some(x => !lines.has(x))) err(file, `${where}.same[${i}]`, 'each same group lists two or more line ids'); }); }
      break;
    }
    case 'table': {
      if (!Array.isArray(w.columns) || !Array.isArray(w.rows)) { err(file, where, 'table needs columns and rows'); break; }
      let editable = 0;
      w.rows.forEach((r, i) => (r || []).forEach((c, j) => { if (isObj(c) && c.edit) { editable++; keys.add(`r${i}c${j}`); keys.add(`r${i + 1}c${j + 1}`); if (typeof c.answer === 'string' && c.answer.trim() && !Number.isFinite(+c.answer)) { if (c.accept != null && !(Array.isArray(c.accept) && c.accept.every(x => typeof x === 'string'))) err(file, `${where}.rows[${i}][${j}].accept`, 'accept is a list of other spellings'); return; } /* item 118: a text answer, graded ignoring case */ if (typeof c.answer !== 'number') err(file, `${where}.rows[${i}][${j}].answer`, 'editable cell needs a numeric answer, or a text one such as "True"'); if (c.tol) tol(c.tol, `${where}.rows[${i}][${j}].tol`); else err(file, `${where}.rows[${i}][${j}].tol`, 'editable cell needs a tol'); } }));
      if (!editable) err(file, `${where}.rows`, 'no editable cell');
      break;
    }
    case 'manipulate': {
      const S = w.states || {};
      if (!isObj(S) || !S[w.start]) { err(file, `${where}.start`, 'start must name a state'); break; }
      if (!S[w.target]) { err(file, `${where}.target`, 'target must name a state'); break; }
      Object.entries(S).forEach(([k, s]) => { keys.add(k); (s.ops || []).forEach((o, i) => { if (!S[o.to]) err(file, `${where}.states.${k}.ops[${i}].to`, `unknown state "${o.to}"`); text(o.label, `${where}.states.${k}.ops[${i}].label`); text(o.why, `${where}.states.${k}.ops[${i}].why`); }); });
      const seen = new Set([w.start]), q = [w.start];
      while (q.length) { const k = q.shift(); (S[k].ops || []).forEach(o => { if (S[o.to] && !seen.has(o.to)) { seen.add(o.to); q.push(o.to); } }); }
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
        if (t.setup != null && typeof t.setup !== 'string') err(file, `${at}.setup`, 'setup is a line of Python run before call ("prices = [100, 90]")');
        if (t.compare === 'raises') {
          if (typeof t.expect !== 'string' || !/^[A-Za-z_][\w.]*$/.test(t.expect.trim())) err(file, `${at}.expect`, 'a raises case names the exception: "ValueError"');
          if (t.call != null && typeof t.call !== 'string') err(file, `${at}.call`, 'call is a Python expression');
        } else if (out) {
          if (typeof t.expect !== 'string') err(file, `${at}.expect`, 'a stdout case needs expect: the printed text, as a string ("Return: 5.00%\\n")');
          if (t.call != null) err(file, `${at}.call`, 'a stdout case has no call (it compares what the whole program prints)');
        } else if (t.call == null || t.expect == null) err(file, at, 'each test needs call and expect (or compare: "stdout" with expect)');
        if (t.stdin != null && typeof t.stdin !== 'string') err(file, `${at}.stdin`, 'stdin is a string, one line per input() call ("250\\n262.5\\n")');
        if (t.exact != null && typeof t.exact !== 'boolean') err(file, `${at}.exact`, 'exact is true or false');
        if (t.argv != null && !(Array.isArray(t.argv) && t.argv.every(x => typeof x === 'string' || typeof x === 'number'))) err(file, `${at}.argv`, 'argv is a list of strings, the words after python3 main.py');
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
      if (w.budget != null && !(typeof w.budget === 'number' && w.budget >= 0 && w.budget <= 120000)) err(file, `${where}.budget`, 'budget is extra milliseconds for a run, 0 to 120000');
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
    x.rubric.forEach((r, i) => checkText(file, `${where}.rubric[${i}].text`, r.text));
  }
};

const checkCanvas = (file, where, c) => {
  if (c == null) return;
  if (!isObj(c)) { err(file, where, 'canvas must be an object'); return; }
  if (c.kind === 'pair') {
    ['left', 'right'].forEach(k => { if (!isObj(c[k])) err(file, `${where}.${k}`, 'a pair needs a left and a right canvas'); else if (c[k].kind === 'pair') err(file, `${where}.${k}.kind`, 'a pair cannot hold a pair'); else checkCanvas(file, `${where}.${k}`, c[k]); });
    if (c.active != null && !['left', 'right'].includes(c.active)) err(file, `${where}.active`, 'active is "left" or "right"');
  }
  if (!CANVASES.has(c.kind)) err(file, `${where}.kind`, `unknown canvas kind "${c.kind}"`);
  if (c.params != null && !isObj(c.params)) err(file, `${where}.params`, 'must be an object');
  if (c.state != null && !isObj(c.state)) err(file, `${where}.state`, 'must be an object');
  /* pass 3 canvas options (items 89 to 107): shapes only, never a crash */
  const P = isObj(c.params) ? c.params : {}, S = isObj(c.state) ? c.state : {};
  const slotOk = (v) => v == null || (Number.isInteger(+v) && +v >= 1 && +v <= 6);
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
      if (f.expr == null && !(f.x != null && f.y != null) && f.implicit == null) err(file, `${where}.params.functions[${i}]`, 'a function needs expr, or x and y (parametric, with t: [from, to]), or implicit (F(x, y) = 0)');
      if (f.holes != null && !(Array.isArray(f.holes) && f.holes.every(x => typeof x === 'number'))) err(file, `${where}.params.functions[${i}].holes`, 'holes is a list of x values');
      if (f.t != null && !(Array.isArray(f.t) && f.t.length === 2 && f.t.every(x => typeof x === 'number'))) err(file, `${where}.params.functions[${i}].t`, 't is [from, to]');
    });
    listOf(S.points).forEach((q, i) => { if (isObj(q) && q.tap != null && typeof q.tap !== 'boolean') err(file, `${where}.state.points[${i}].tap`, 'tap is true or false'); if (isObj(q) && q.trace != null && ![true, false, 'x'].includes(q.trace)) err(file, `${where}.state.points[${i}].trace`, 'trace is true (the path as it went) or "x" (sorted by x)'); });
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
  if (c.kind === 'console' && P.lines == null && typeof P.text !== 'string') err(file, `${where}.params`, 'a console needs lines (a list of strings) or text');
  if (c.kind === 'console' && P.lines != null && !(Array.isArray(P.lines) && P.lines.every(l => typeof l === 'string'))) err(file, `${where}.params.lines`, 'lines is a list of strings, one per line');
  if (c.kind === 'table' && P.tap != null && P.tap !== 'rows') err(file, `${where}.params.tap`, 'tap is "rows" (or leave it out to tap cells)');
  if (c.kind === 'tree' && S.current != null && typeof S.current !== 'string') err(file, `${where}.state.current`, 'current is a branch path such as "a-b", or "root"');
  if (c.kind === 'vectors' && P.points != null && !(Array.isArray(P.points) && P.points.every(q => isObj(q) && typeof q.x === 'number' && typeof q.y === 'number'))) err(file, `${where}.params.points`, 'points is a list of { id, x, y, label }');
  (c.controls || []).forEach((k, i) => {
    if (!k.bind) err(file, `${where}.controls[${i}].bind`, 'required');
    if (k.format != null && !['fraction', 'percent'].includes(k.format)) err(file, `${where}.controls[${i}].format`, 'format is "fraction" or "percent"');
    if (k.scale != null && k.scale !== 'log') err(file, `${where}.controls[${i}].scale`, 'scale is "log" (or leave it out for a linear slider)');
    if (k.scale === 'log' && !(+k.min > 0 && +k.max > +k.min)) err(file, `${where}.controls[${i}]`, 'a log slider needs 0 < min < max (stops at powers of ten from min)');
  });
  if (c.maxHeight != null && !(typeof c.maxHeight === 'number' && c.maxHeight >= 120)) err(file, `${where}.maxHeight`, 'maxHeight is a number of pixels, 120 or more');
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
    checkText(file, `${where}.byKey.${k}`, v);
    const sentences = stripMathsAndCode(v).split(/[.?]\s/).filter(s => s.trim()).length;
    if (sentences > 3) warn(file, `${where}.byKey.${k}`, 'at most three sentences');
  });
};
const checkExplain = (file, where, ex, { required = false } = {}) => {
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

/* An item: a problem screen without hints (quiz, review, homework, exam) */
const checkItem = (file, where, it, ctx) => {
  if (!isObj(it)) { err(file, where, 'item must be an object'); return null; }
  if (!it.id || !KEBAB.test(String(it.id))) err(file, `${where}.id`, 'item id must be kebab-case');
  if (it.difficulty != null || ctx.needDifficulty !== false) checkDifficulty(file, `${where}.difficulty`, it.difficulty, ctx.lo, ctx.hi, ctx.label);
  if (it.hints) err(file, `${where}.hints`, `${ctx.label} items have no hints`);
  /* item 297: on a longform item, prose takes the place of prompt on screen, so the prompt would never show */
  if (typeof it.prose === 'string' && it.prose.trim() && typeof (it.prompt || (isObj(it.widget) && it.widget.kind === 'longform' && it.widget.prompt)) === 'string' && String(it.prompt || it.widget.prompt).trim()) warn(file, where, 'this item has both prose and prompt: prose replaces prompt on screen, so the prompt is never shown (merge them into one)');
  if (ctx.skillsRequired && (!Array.isArray(it.skills) || !it.skills.length)) err(file, `${where}.skills`, 'name at least one skill');
  (it.skills || []).forEach(s => { if (ctx.skills && !ctx.skills.has(s)) err(file, `${where}.skills`, `unknown skill "${s}"`); });
  if (it.kind === 'longform' || (it.widget && it.widget.kind === 'longform')) {
    if (!ctx.allowLongform) err(file, where, 'longform items belong in homework and exams');
    checkLongform(file, where, it.kind === 'longform' ? it : it.widget);
    return 'longform';
  }
  checkCanvas(file, `${where}.canvas`, it.canvas);
  checkText(file, `${where}.prose`, it.prose); checkText(file, `${where}.question`, it.question);
  if (!it.question) err(file, `${where}.question`, 'required field missing');
  if (!it.widget) { err(file, `${where}.widget`, 'required field missing'); return null; }
  const keys = checkWidget(file, `${where}.widget`, it.widget, it.canvas, { question: it.question, allowLongform: ctx.allowLongform });
  checkFeedback(file, `${where}.feedback`, it.feedback, keys);
  checkExplain(file, `${where}.explain`, it.explain, { required: true });
  if (ctx.warnInteractive && (CANVAS_BOUND.has(it.widget.kind) || (it.canvas && (it.canvas.controls || []).length))) warn(file, where, 'a quiz item with an interactive canvas: concreteness should have faded by the quiz');
  return it.widget.kind;
};

/* ---------- Lesson (rules 1 to 9 and the warnings) ---------- */
const checkLesson = (file, courseId, lessonId, L, course) => {
  const skills = new Set(Object.keys(course.skills || {}));
  req(file, '', L, ['id', 'course', 'title', 'minutes', 'objectives', 'skills', 'screens', 'summary', 'quiz']);
  if (L.id !== lessonId) err(file, 'id', `id "${L.id}" must match the file name "${lessonId}"`);
  if (L.course !== courseId) err(file, 'course', `course "${L.course}" must match the folder "${courseId}"`);
  checkText(file, 'title', L.title);
  if (typeof L.minutes !== 'number' || L.minutes < 10 || L.minutes > 15) err(file, 'minutes', 'minutes is 10 to 15');
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
    if (s.prose && words(s.prose) > 60) warn(file, `${at}.prose`, `prose over 60 words (${words(s.prose)})`);
    checkCanvas(file, `${at}.canvas`, s.canvas);
    if (s.difficulty != null || GRADED.has(s.type)) checkDifficulty(file, `${at}.difficulty`, s.difficulty, 1, 3, 'lesson screen');
    let keys = null;
    if (s.widget) keys = checkWidget(file, `${at}.widget`, s.widget, s.canvas, { question: s.question });
    if (s.type === 'title') { if (!s.prose) err(file, `${at}.prose`, 'a title screen needs one framing sentence'); if (s.widget) err(file, `${at}.widget`, 'a title screen has no widget'); }
    if (s.type === 'demonstrate') {
      if (s.widget) err(file, `${at}.widget`, 'a demonstrate screen has no widget');
      if (!Array.isArray(s.steps) || s.steps.length < 3 || s.steps.length > 6) err(file, `${at}.steps`, '3 to 6 steps');
      (s.steps || []).forEach((st, j) => { if (!st.caption) err(file, `${at}.steps[${j}].caption`, 'required field missing'); checkText(file, `${at}.steps[${j}].caption`, st.caption); });
    }
    if (s.type === 'explore') {
      if (!s.canvas) err(file, `${at}.canvas`, 'an explore screen needs a canvas');
      else if (!(s.canvas.controls || []).length && !(s.widget && (CANVAS_BOUND.has(s.widget.kind) || (s.widget.kind === 'place' && s.widget.mode === 'boxes'))) && !authorMovable(s.canvas)) err(file, `${at}.canvas`, 'an explore screen needs an interactive canvas (controls or a canvas-bound widget)');
      if (!s.widget) err(file, `${at}.widget`, 'an explore screen ends with one observation question');
      else checkFeedback(file, `${at}.feedback`, s.feedback, keys);
      checkHints(file, `${at}.hints`, s.hints, s.canvas, false);
    }
    if (s.type === 'generalise') {
      /* item 101: in a programming course (a topic on the code track) a fenced code block states the rule as well as KaTeX does */
      const codeCourse = (C.stages || []).some(st => (st.topics || []).some(t => t.track === 'code' && (t.courses || []).includes(courseId)));
      if (!s.prose || !(/\$/.test(s.prose) || (codeCourse && /```[\w+-]*\n[\s\S]*?```/.test(s.prose)))) err(file, `${at}.prose`, codeCourse ? 'a generalise screen states the rule in KaTeX or a fenced code block' : 'a generalise screen states the rule in KaTeX');
      if (s.widget) checkFeedback(file, `${at}.feedback`, s.feedback, keys);
    }
    if (GRADED.has(s.type)) {
      if (!s.question) err(file, `${at}.question`, 'required field missing');
      if (!s.widget) err(file, `${at}.widget`, 'required field missing');
      checkFeedback(file, `${at}.feedback`, s.feedback, keys, { requireByKey: s.type === 'trap' });
      checkHints(file, `${at}.hints`, s.hints, s.canvas, true);
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
const checkSet = (file, kind, courseId, id, level, doc, course) => {
  const skills = new Set(Object.keys(course.skills || {}));
  req(file, '', doc, kind === 'review' ? ['id', 'course', 'level', 'items'] : ['id', 'course', 'level', 'dueDays', 'items']);
  if (doc.id !== id) err(file, 'id', `id "${doc.id}" must match the file name "${id}"`);
  if (doc.course !== courseId) err(file, 'course', `course must be "${courseId}"`);
  if (doc.level !== level) err(file, 'level', `level must be ${level}`);
  const items = Array.isArray(doc.items) ? doc.items : [];
  const [lo, hi, nlo, nhi] = kind === 'review' ? [2, 4, 6, 10] : [3, 5, 6, 12];
  if (items.length < nlo || items.length > nhi) err(file, 'items', `${nlo} to ${nhi} items (found ${items.length})`);
  const kinds = items.map((it, i) => checkItem(file, `items[${i}]`, it, { lo, hi, label: kind, skills, skillsRequired: true, allowLongform: kind === 'homework' }));
  const qids = new Set(); items.forEach((it, i) => { if (it && it.id) { if (qids.has(it.id)) err(file, `items[${i}].id`, `duplicate id "${it.id}"`); qids.add(it.id); } });
  if (kind === 'homework') {
    if (!items.some(it => it && it.difficulty === 5)) err(file, 'items', 'homework needs at least one item at difficulty 5');
    if (!kinds.includes('longform')) err(file, 'items', 'homework needs at least one longform item');
    const track = course.track;
    const hasCode = kinds.includes('code'), hasDerive = kinds.includes('order') || kinds.includes('expression');
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
const checkExam = (file, id, doc, cur) => {
  const topicExam = id.startsWith('topic-');
  if (doc.id !== id) err(file, 'id', `id "${doc.id}" must match the file name "${id}"`);
  if (topicExam) {
    req(file, '', doc, ['id', 'topic', 'name', 'minutes', 'pass', 'skills', 'items']);
    const t = cur.topics.get(String(doc.topic));
    if (!t) { err(file, 'topic', `unknown topic "${doc.topic}"`); return; }
    if (id !== `topic-${doc.topic}`) err(file, 'id', `a topic exam for ${doc.topic} is named topic-${doc.topic}`);
    const topicSkills = new Set(t.courses.flatMap(c => Object.keys((cur.courseDocs[c] || {}).skills || {})));
    const examSkills = new Set(Object.keys(doc.skills || {}));
    examSkills.forEach(s => { if (!topicSkills.has(s)) err(file, 'skills', `"${s}" is not a skill of a course in topic ${doc.topic}`); });
    topicSkills.forEach(s => { if (!examSkills.has(s)) err(file, 'skills', `topic skill "${s}" is not covered by the exam`); });
    const items = Array.isArray(doc.items) ? doc.items : [];
    if (items.length < 20 || items.length > 30) err(file, 'items', `20 to 30 items (found ${items.length})`);
    items.forEach((it, i) => checkItem(file, `items[${i}]`, it, { lo: 2, hi: 5, label: 'exam', skills: examSkills, skillsRequired: true, allowLongform: true }));
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
        req(file, `parts[${i}]`, p, ['minutes', 'pass', 'items']);
        const items = Array.isArray(p.items) ? p.items : [];
        items.forEach((it, j) => checkItem(file, `parts[${i}].items[${j}]`, it, { lo: 2, hi: 5, label: 'exam', skills: allSkills, skillsRequired: true, allowLongform: true }));
        if (items.length >= 10) checkRamp(file, `parts[${i}].items`, items);
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
};

/* ---------- Main ---------- */
const curFile = path.join(CONTENT, 'curriculum.json');
const curDoc = readJSON(curFile);
if (curDoc.missing) err(curFile, '', 'curriculum.json is missing');
const C = curDoc.data || { stages: [], courses: {}, tracks: {} };
const cur = { topics: new Map(), stages: new Set(), courseDocs: {}, courseTopic: {} };

/* Curriculum */
if (!Array.isArray(C.stages)) err(curFile, 'stages', 'must be an array');
if (C.tracks) TRACKS.forEach(t => { if (!C.tracks[t]) err(curFile, `tracks.${t}`, 'track name missing'); });
(C.stages || []).forEach((s, i) => {
  const at = `stages[${i}]`;
  req(curFile, at, s, ['name', 'hours', 'exit', 'topics']);
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

/* Courses */
const manifest = [];
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
  let reviewsMissing = 0, homeworkMissing = 0, lessonTotal = 0;
  levels.forEach((lv, i) => {
    const at = `levels[${i}]`;
    if (lv.n !== i + 1) err(file, `${at}.n`, `levels are numbered from 1 in order (expected ${i + 1})`);
    if (!lv.name) err(file, `${at}.name`, 'required field missing');
    checkText(file, `${at}.name`, lv.name);
    const ls = Array.isArray(lv.lessons) ? lv.lessons : [];
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
      if (lr.missing) { unwritten.push(l); return; }
      written.push(l); manifest.push(`courses/${cid}/${l}.json`);
      if (lr.data) guard(lf, () => checkLesson(lf, cid, l, lr.data, D).forEach(s => usedSkills.add(s)));
    });
    [['review', `review-${i + 1}`], ['homework', `homework-${i + 1}`]].forEach(([kind, expect]) => {
      if (lv[kind] !== expect) err(file, `${at}.${kind}`, `${kind} is "${expect}"`);
      const id = lv[kind] || expect; referenced.add(`${id}.json`);
      const sf = path.join(dir, `${id}.json`), sr = readJSON(sf);
      if (sr.missing) { if (kind === 'review') reviewsMissing++; else homeworkMissing++; return; }
      manifest.push(`courses/${cid}/${id}.json`);
      if (sr.data) guard(sf, () => checkSet(sf, kind, cid, id, i + 1, sr.data, D));
    });
  });
  listJSON(dir).forEach(f => { if (!referenced.has(f)) err(path.join(dir, f), '', 'file is not referenced by course.json'); });
  if (!unwritten.length) skills.forEach(s => { if (!usedSkills.has(s)) err(file, `skills.${s}`, 'no lesson uses this skill'); });
  if (unwritten.length || reviewsMissing || homeworkMissing) {
    warn(file, '', `not yet written: ${unwritten.length} of ${lessonTotal} lessons, ${reviewsMissing} of ${levels.length} reviews, ${homeworkMissing} of ${levels.length} homework`);
  }
  summary.push({ cid, topic: meta.topic, lessons: lessonTotal, levels: levels.length, written: written.length, unwritten, reviews: levels.length - reviewsMissing, homework: levels.length - homeworkMissing });
});

/* Exams */
const examDir = path.join(CONTENT, 'exams');
listJSON(examDir).forEach(f => {
  const id = f.replace(/\.json$/, ''), file = path.join(examDir, f);
  if (!/^(topic-\d+\.\d+|stage-\d+)$/.test(id)) { err(file, '', 'exam files are topic-<topic>.json or stage-<n>.json'); return; }
  const r = readJSON(file); if (!r.data) return;
  manifest.push(`exams/${f}`);
  guard(file, () => checkExam(file, id, r.data, cur));
});

/* Drills */
const drillDir = path.join(CONTENT, 'drills');
const idxFile = path.join(drillDir, 'index.json');
const idx = readJSON(idxFile);
const listed = new Set();
if (idx.missing) warn(idxFile, '', 'drills/index.json is missing; the drill list will be empty');
else if (idx.data && !Array.isArray(idx.data)) err(idxFile, '', 'index.json is an array of drill ids or { id, ... } entries');
else (idx.data || []).forEach((e, i) => { const id = typeof e === 'string' ? e : e && e.id; if (!id) err(idxFile, `[${i}]`, 'entry needs an id'); else listed.add(id); });
listJSON(drillDir).filter(f => f !== 'index.json').forEach(f => {
  const id = f.replace(/\.json$/, ''), file = path.join(drillDir, f);
  const r = readJSON(file); if (!r.data) return;
  manifest.push(`drills/${f}`);
  guard(file, () => checkDrill(file, id, r.data, cur));
  if (!listed.has(id)) warn(file, '', 'drill is not listed in drills/index.json');
  listed.delete(id);
});
listed.forEach(id => err(idxFile, '', `drill "${id}" is listed but drills/${id}.json does not exist`));

/* Warm-up settings */
const wu = readJSON(path.join(CONTENT, 'warmup.json'));
if (wu.missing) warn(path.join(CONTENT, 'warmup.json'), '', 'warmup.json is missing');
else if (wu.data) { req(path.join(CONTENT, 'warmup.json'), '', wu.data, ['seconds', 'operations']); }

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
  const body = JSON.stringify({ note: 'Written by tools/validate.mjs: every authored lesson, review, homework, exam and drill file. js/content.js reads it so it never requests a file that does not exist. Run the validator after adding content.', files: manifest.sort() }, null, 2) + '\n';
  let old = ''; try { old = fs.readFileSync(mf, 'utf8'); } catch { /* first run */ }
  if (old !== body) { fs.writeFileSync(mf, body); console.log(`manifest: wrote content/manifest.json (${manifest.length} files)`); }
}
console.log(`\n${errors.length} error${errors.length === 1 ? '' : 's'}, ${warnings.length} warning${warnings.length === 1 ? '' : 's'}`);
process.exit(errors.length ? 1 : 0);
