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
const WIDGETS = new Set(['choice', 'multi', 'numeric', 'expression', 'slider', 'drag-point', 'place', 'tap-regions', 'order', 'table', 'manipulate', 'balance', 'sketch', 'code', 'longform']);
const CANVASES = new Set(['grid', 'tree', 'venn', 'number-line', 'boxes', 'area', 'balance', 'circle', 'plane', 'bars', 'distribution', 'scatter', 'series', 'walk', 'matrix', 'vectors', 'graph', 'array', 'payoff', 'orderbook', 'table']);
const SCREEN_TYPES = new Set(['title', 'explore', 'problem', 'ladder', 'demonstrate', 'trap', 'generalise', 'derive', 'transfer']);
const GRADED = new Set(['problem', 'ladder', 'trap', 'transfer', 'derive']);
const CANVAS_BOUND = new Set(['tap-regions', 'drag-point', 'sketch', 'balance', 'slider']);
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
const EMOJI = /\p{Extended_Pictographic}/u;

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
const readJSON = (file) => {
  let text;
  try { text = fs.readFileSync(file, 'utf8'); } catch { return { missing: true }; }
  try { return { data: JSON.parse(text) }; } catch (e) { err(file, '', `JSON does not parse: ${e.message}`); return { bad: true }; }
};
const listJSON = (dir) => { try { return fs.readdirSync(dir).filter(f => f.endsWith('.json')).sort(); } catch { return []; } };
const isObj = (x) => x && typeof x === 'object' && !Array.isArray(x);
const req = (file, where, obj, fields) => fields.forEach(f => { if (obj == null || obj[f] === undefined || obj[f] === null || obj[f] === '') err(file, where ? `${where}.${f}` : f, 'required field missing'); });

/* Art kinds from js/art.js, so course art always draws */
const ART = (() => {
  try { const src = fs.readFileSync(path.join(APP, 'js', 'art.js'), 'utf8'); const body = src.slice(src.indexOf('const art = {')); return new Set([...body.matchAll(/^\s{4}([a-z]+): \(\)/gm)].map(m => m[1])); } catch { return null; }
})();

/* ---------- Canvas ids ---------- */
const range = (a, b) => Array.from({ length: Math.max(0, b - a + 1) }, (_, i) => a + i);
const regionIds = (canvas) => {
  if (!isObj(canvas)) return null;
  const p = canvas.params || {};
  if (canvas.kind === 'grid' && p.rows && p.cols) {
    const ids = new Set();
    range(0, p.rows).forEach(i => range(0, p.cols).forEach(j => ids.add(`r${i}c${j}`)));
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
  if (canvas.kind === 'number-line' && Array.isArray((canvas.state || {}).points)) {
    return new Set(canvas.state.points.map(q => q && q.id).filter(Boolean)); // tap mode on points
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
  grid: /^(r\d+c\d+|row\d+|col\d+|cross\d+)$/,
  venn: /^(A|B|C|AB|AC|BC|ABC|none|[A-Za-z]{1,3})$/,
  area: /^(c\d+(-\d+)?|pt\d+|shade|split|point)$/,
  table: /^(r\d+|c\d+|r\d+c\d+)$/,
  matrix: /^[A-Za-z][A-Za-z0-9]*(-(r\d+|c\d+|\d+-\d+))?$/,
  walk: /^(path\d+|barrier-up|barrier-down)$/,
  orderbook: /^(bid\d+|ask\d+|spread)$/,
  distribution: /^(mean|shade|x-?\d+)$/,
  scatter: /^(p\d+|line)$/,
  circle: /^(angle|sin|cos|tan|pt)$/,
  bars: /^x[A-Za-z0-9.-]+$/,
  array: /^(c\d+|[a-z][a-z0-9-]*)$/,
};
const plausibleId = (canvas, id) => {
  if (!isObj(canvas)) return true;
  const ids = regionIds(canvas);
  if (ids && ids.has(id)) return true;
  if (canvas.kind === 'grid' && ids) return /^(row|col|cross)\d+$/.test(id);
  const re = PLAUSIBLE[canvas.kind];
  return re ? re.test(String(id)) : /^[A-Za-z0-9][A-Za-z0-9_.-]*$/.test(String(id));
};

/* ---------- Widgets (rule 4) and the keys they can produce (rule 5) ---------- */
const checkWidget = (file, where, w, canvas, ctx = {}) => {
  if (!isObj(w)) { err(file, where, 'widget must be an object'); return null; }
  if (!WIDGETS.has(w.kind)) { err(file, `${where}.kind`, `unknown widget kind "${w.kind}"`); return null; }
  if (w.kind === 'longform' && !ctx.allowLongform) err(file, `${where}.kind`, 'longform belongs in homework and exams');
  const keys = new Set();
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
      break;
    case 'slider':
      ['min', 'max', 'step'].forEach(f => { if (typeof w[f] !== 'number') err(file, `${where}.${f}`, 'must be a number'); });
      if (w.answer != null) { if (typeof w.answer !== 'number') err(file, `${where}.answer`, 'must be a number'); if (typeof w.tol !== 'number') err(file, `${where}.tol`, 'slider tol must be a number'); }
      if (w.answer != null && typeof w.min === 'number' && typeof w.max === 'number' && (w.answer < w.min || w.answer > w.max)) err(file, `${where}.answer`, 'answer outside min..max');
      ids(w.wrong, 'wrong').forEach(k => keys.add(String(k)));
      break;
    case 'drag-point':
      if (!Array.isArray(w.points) || !w.points.length) err(file, `${where}.points`, 'at least one point');
      (w.points || []).forEach((p, i) => {
        if (!p.id) err(file, `${where}.points[${i}].id`, 'required');
        const oneD = canvas && (canvas.kind === 'number-line' || canvas.kind === 'circle');
        if (oneD && typeof p.target === 'number') { /* a bare number: x on a number line, the angle on a circle */ }
        else if (!Array.isArray(p.target) || p.target.length !== 2) err(file, `${where}.points[${i}].target`, oneD ? 'must be a number (or [x, y])' : 'must be [x, y]');
        if (p.tol != null && typeof p.tol !== 'number') err(file, `${where}.points[${i}].tol`, 'must be a number (default 0.25)');
        if (p.id) keys.add(String(p.id)); // the key when this point is off target and in no wrong[] region
      });
      ids(w.wrong, 'wrong').forEach(k => keys.add(String(k)));
      break;
    case 'place': {
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
      if (known) (w.answer || []).forEach(id => { if (!known.has(id)) err(file, `${where}.answer`, `region "${id}" is not on the ${canvas.kind} canvas`); });
      if (known) (w.among || []).forEach(id => { if (!known.has(id)) err(file, `${where}.among`, `region "${id}" is not on the ${canvas.kind} canvas`); });
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
      break;
    }
    case 'table': {
      if (!Array.isArray(w.columns) || !Array.isArray(w.rows)) { err(file, where, 'table needs columns and rows'); break; }
      let editable = 0;
      w.rows.forEach((r, i) => (r || []).forEach((c, j) => { if (isObj(c) && c.edit) { editable++; keys.add(`r${i}c${j}`); keys.add(`r${i + 1}c${j + 1}`); if (typeof c.answer !== 'number') err(file, `${where}.rows[${i}][${j}].answer`, 'editable cell needs a numeric answer'); if (c.tol) tol(c.tol, `${where}.rows[${i}][${j}].tol`); else err(file, `${where}.rows[${i}][${j}].tol`, 'editable cell needs a tol'); } }));
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
    case 'balance':
      req(file, where, w, ['left', 'right', 'target']);
      keys.add('*');
      break;
    case 'sketch':
      req(file, where, w, ['target', 'xRange', 'band']);
      if (w.control != null && (typeof w.control !== 'number' || w.control < 2)) err(file, `${where}.control`, 'control must be a number of points, at least 2');
      keys.add('*');
      break;
    case 'code':
      req(file, where, w, ['language', 'starter']);
      if (!Array.isArray(w.tests) || w.tests.length < 3) err(file, `${where}.tests`, 'at least 3 tests');
      else if (w.tests.length > 15) err(file, `${where}.tests`, 'at most 15 tests');
      (w.tests || []).forEach((t, i) => { if (t.call == null || t.expect == null) err(file, `${where}.tests[${i}]`, 'each test needs call and expect'); if (t.compare && !['isclose', 'equal', 'fraction'].includes(t.compare)) err(file, `${where}.tests[${i}].compare`, 'compare is isclose, equal or fraction'); });
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
  if (!CANVASES.has(c.kind)) err(file, `${where}.kind`, `unknown canvas kind "${c.kind}"`);
  if (c.params != null && !isObj(c.params)) err(file, `${where}.params`, 'must be an object');
  if (c.state != null && !isObj(c.state)) err(file, `${where}.state`, 'must be an object');
  (c.controls || []).forEach((k, i) => {
    if (!k.bind) err(file, `${where}.controls[${i}].bind`, 'required');
    if (k.format != null && !['fraction', 'percent'].includes(k.format)) err(file, `${where}.controls[${i}].format`, 'format is "fraction" or "percent"');
  });
  if (c.derive != null) {
    if (!isObj(c.derive)) err(file, `${where}.derive`, 'derive maps a target ("p2.x", "caption") to an expression');
    else Object.entries(c.derive).forEach(([t, e]) => {
      if (typeof e !== 'string' && typeof e !== 'number') { err(file, `${where}.derive.${t}`, 'must be an expression string or a number'); return; }
      const parts = typeof e === 'string' ? (e.includes('{{') ? [...e.matchAll(/\{\{([^}]+)\}\}/g)].map(m => m[1]) : [e]) : [];
      parts.forEach(x => { if (/[;`{}]|=>|\bfunction\b|\bnew\b|\bthis\b|(^|[^=!<>])=(?!=)/.test(x)) err(file, `${where}.derive.${t}`, `not an expression: ${x}`); else { try { new Function('S', 'with (S) { return (' + x + '); }'); } catch (er) { err(file, `${where}.derive.${t}`, `does not parse: ${x}`); } } });
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
      else if (!(s.canvas.controls || []).length && !(s.widget && CANVAS_BOUND.has(s.widget.kind))) err(file, `${at}.canvas`, 'an explore screen needs an interactive canvas (controls or a canvas-bound widget)');
      if (!s.widget) err(file, `${at}.widget`, 'an explore screen ends with one observation question');
      else checkFeedback(file, `${at}.feedback`, s.feedback, keys);
      checkHints(file, `${at}.hints`, s.hints, s.canvas, false);
    }
    if (s.type === 'generalise') {
      if (!s.prose || !/\$/.test(s.prose)) err(file, `${at}.prose`, 'a generalise screen states the rule in KaTeX');
      if (s.widget) checkFeedback(file, `${at}.feedback`, s.feedback, keys);
    }
    if (GRADED.has(s.type)) {
      if (!s.question) err(file, `${at}.question`, 'required field missing');
      if (!s.widget) err(file, `${at}.widget`, 'required field missing');
      checkFeedback(file, `${at}.feedback`, s.feedback, keys, { requireByKey: s.type === 'trap' });
      checkHints(file, `${at}.hints`, s.hints, s.canvas, true);
      if (s.type === 'derive' && s.widget && !['expression', 'order', 'choice'].includes(s.widget.kind)) err(file, `${at}.widget.kind`, 'a derive screen uses expression, order or choice');
      if (s.type === 'ladder' && s.canvas && prevCanvasKind && s.canvas.kind !== prevCanvasKind) warn(file, `${at}.canvas`, 'a ladder screen usually reuses the previous canvas kind');
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
      if (lr.data) checkLesson(lf, cid, l, lr.data, D).forEach(s => usedSkills.add(s));
    });
    [['review', `review-${i + 1}`], ['homework', `homework-${i + 1}`]].forEach(([kind, expect]) => {
      if (lv[kind] !== expect) err(file, `${at}.${kind}`, `${kind} is "${expect}"`);
      const id = lv[kind] || expect; referenced.add(`${id}.json`);
      const sf = path.join(dir, `${id}.json`), sr = readJSON(sf);
      if (sr.missing) { if (kind === 'review') reviewsMissing++; else homeworkMissing++; return; }
      manifest.push(`courses/${cid}/${id}.json`);
      if (sr.data) checkSet(sf, kind, cid, id, i + 1, sr.data, D);
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
  checkExam(file, id, r.data, cur);
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
  checkDrill(file, id, r.data, cur);
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
