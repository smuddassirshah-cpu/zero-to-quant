#!/usr/bin/env node
/* Second read, eigen problems-4: what the engine's own graders do with each typed part.
   Loads app/js/engine/grade.js and the local Compute Engine (the harness of review-problems-1.4-c-scripts/grade-probe.mjs),
   then, per typed part: the key grades correct (also with one more place, after a letter and "=", with a true minus sign,
   with its unit); every accept[] grades correct; every wrong[] is refused on its own key and has a byKey line; and the
   reader's own strings (ROWS): T accepted, F refused on no wrong line, a wrong id = refused on that line.
   A row with a note is behaviour the reader holds to be a fault (printed as FINDING, not a failure).
   The +-0.5 bands on the slips of the three whole-number parts are by design (the validator's wrong-band rule: the slip
   rounded as the question asks must reach its line), so 4, 6, -1 and 1 are expected on those lines.

   node docs/reviews/review-problems-eigen-4-scripts/grade-probe.mjs --local-cdn <pkgs> [--all]      (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const ALL = argv.includes('--all');
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'), 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const isSet = (w) => Array.isArray(w.answers) && w.answers.length > 0;
const num = (w, t) => { const r = isSet(w) ? G.numSetGrade(w, t) : G.numGrade(w, t); return { ok: !!r.ok, key: r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null), line: r.line }; };
const expr = (w, t) => { try { const r = G.exprGrade(ce, w, t, t); return { ok: !!r.ok, key: r.key || null, line: r.line }; } catch (e) { return { ok: false, key: 'THROW ' + e.message }; } };

const T = true, F = false, ANY = 'ANY';
const CARRY = 'the answer carried from the no-root slip of part 1 (L22 = 9, so -6/9) lands in the +-0.5 band of `carried` and is told "That divides by sqrt 34"';
/* ROWS[item][part] = [[text, expected, note?], ...] */
const ROWS = {
  'p-linked-lagoons': {
    1: [['-5.0', T], ['−5', T], ['5', 'sign'], ['-4', 'unchanged'], ['-3', 'reversed'], ['-2', F], ['0', F], ['1', F]],
    2: [['-5, -2', T], ['-2,-5', T], ['−5, −2', T], ['-5 and -2', T], ['(-5, -2)', T], ['5, 2', 'sign'], ['2, 5', 'sign'], ['-7, 10', 'trace-det'], ['-4, -3', 'a-diagonal'], ['-5, 2', F], ['-5', 'count'], ['-5, -2, 0', 'count']],
    3: [['(2,-1)', T], ['(2, -1.0)', T], ['\\begin{pmatrix}2\\\\-1\\end{pmatrix}', T], ['(4,-1)', 'inverse'], ['(3,-1)', 'unmoved'], ['(-2,1)', F], ['(4,-2)', F], ['(1,1)', F], ['(-1,2)', F]],
    4: [['(3,1)', T], ['(3.0, 1)', T], ['3, 1', T], ['(1,3)', 'swapped'], ['(3,2)', 'w-coords'], ['(5,2)', F], ['(1,1)', F], ['(3,-1)', F]],
    5: [['0.819', T], ['0.8188', T], ['0.81875', T], ['.819', T], ['0.819 kg', T], ['0.8185', T], ['0.818', T], ['0.82', T], ['0.817', F], ['0.821', F], ['0.413', 'coefficients-only'], ['0.419', 'u1-only'], ['0.176', 'rates-swapped'], ['0.291', 'carried'], ['0.812', F], ['0.393', F], ['819', F]],
  },
  'p-wind-pair': {
    1: [['3.0', T], ['L_{22}=3', T], ['5.831', 'no-subtract'], ['5.83', 'no-subtract'], ['3.742', 'subtract-sigma'], ['3.74', 'subtract-sigma'], ['9', 'no-root'], ['4', 'subtract-sigma'], ['6', 'no-subtract'], ['5', F], ['-3', F], ['14', F]],
    2: [['-2.0', T], ['−2', T], ['w_2=-2', T], ['2', 'sign'], ['-12', 'used-x1'], ['1.333', 'no-subtract'], ['1.33', 'no-subtract'], ['4/3', 'no-subtract'], ['-1.029', 'carried'], ['-1.03', 'carried'], ['-0.667', 'carried', CARRY], ['-0.67', 'carried', CARRY], ['-1', 'carried'], ['1', 'no-subtract'], ['-1.604', F], ['-6', F], ['0', F]],
    3: [['2.828', T], ['2.8284', T], ['2.829', T], ['2.83', F], ['2.8', F], ['8', 'squared'], ['2.114', 'ignore-correlation'], ['12.166', 'carried'], ['12.17', F], ['2.404', F], ['2.686', F], ['4', F], ['0', F]],
    4: [['0.0183', T], ['0.01832', T], ['.0183', T], ['0.018', F], ['0.02', F], ['0.2431', 'used-d'], ['0.0003', 'no-half'], ['0.000335', 'no-half'], ['0.107', 'carried'], ['0.1070', 'carried'], ['0.0556', F], ['1.83', F], ['0.1353', F], ['54.6', F]],
  },
  'p-track-laps': {
    1: [['0.0', T], ['L_{22}=0', T], ['6', 'root-36'], ['4.243', 'subtract-entry'], ['4.24', 'subtract-entry'], ['4', 'subtract-entry'], ['3', F], ['18', F], ['-0', T]],
    2: [['45.0', T], ['\\lambda=45', T], ['36', 'diagonal'], ['9', 'first-entry'], ['0', F], ['6.708', F], ['54', F], ['27', F]],
    3: [['(1,2)', T], ['(1.0, 2)', T], ['\\begin{pmatrix}1\\\\2\\end{pmatrix}', T], ['(5,0)', 'all-km'], ['(0,2.5)', 'all-laps'], ['(0,\\frac{5}{2})', 'all-laps'], ['(0, 5/2)', 'all-laps'], ['(2,1)', F], ['(2,4)', F], ['(3,6)', F], ['(15,30)', F], ['(0.447,0.894)', F]],
    4: [['15.0', T], ['15 minutes', T], ['9', 'laps-as-km'], ['3', 'km-only'], ['12', F], ['7.5', F], ['30', F]],
  },
  'p-machine-stops': {
    1: [['0, -0.8', T], ['-0.8, 0', T], ['-.8,0', T], ['0, −0.8', T], ['-4/5, 0', T], ['0 and -0.8', T], ['0, 0.8', 'sign'], ['0.8, 0', 'sign'], ['-0.2, -0.6', 'diagonal'], ['-0.6,-0.2', 'diagonal'], ['-0.8', 'count'], ['0, -0.4', F], ['0.2, 0.6', F]],
    2: [['(0.75,0.25)', T], ['(.75, .25)', T], ['(0.750, 0.250)', T], ['(3/4,1/4)', T], ['(\\frac34,\\frac14)', T], ['\\frac{1}{4}(3,1)', T], ['(0.25,0.75)', 'swapped'], ['(1/4,3/4)', 'swapped'], ['(3,1)', 'unscaled'], ['(1,3)', F], ['(0.6,0.2)', F], ['(0.5,0.5)', F], ['(1,-1)', F]],
    4: [['0.318', T], ['0.3180', T], ['.318', T], ['0.31804', T], ['0.32', F], ['0.773', 'running-chance'], ['0.068', 'no-steady'], ['0.374', 'restart-rate'], ['0.587', 'one-hour'], ['0.682', F], ['0.227', F], ['0.25', F], ['31.8', F]],
    5: [['5.40', T], ['5.4', T], ['5.397', T], ['5.396', T], ['5.4 hours', T], ['5.41', T], ['5.39', T], ['5.3', F], ['5', F], ['4.02', 'running-start'], ['5.76', 'no-coefficient'], ['7.2', 'restart-rate'], ['7.20', 'restart-rate'], ['3.45', 'multiplied'], ['5.03', F], ['5.04', F], ['2.34', F]],
  },
};

let checks = 0, fails = 0, findings = 0, nNum = 0, nSet = 0, nExpr = 0, nRows = 0;
const say = (ok, note, msg) => { checks++; if (!ok) { fails++; console.log('FAIL    ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); return; } if (ALL) console.log('ok      ' + msg); };
const doc = JSON.parse(fs.readFileSync('app/content/courses/eigen/problems-4.json', 'utf8'));
for (const it of doc.items) it.parts.forEach((p, i) => {
  const k = i + 1, w = p.widget, where = `${it.id} ${k}`;
  const by = (p.feedback && p.feedback.byKey) || {};
  let grade;
  if (w.kind === 'numeric' && isSet(w)) {
    nSet++; grade = (t) => num(w, t);
    const a = w.answers.map(String);
    say(grade(a.join(', ')).ok, null, `${where}: key ${a.join(', ')} grades correct`);
    say(grade([...a].reverse().join(',')).ok, null, `${where}: key in the other order grades correct`);
    for (const x of w.wrong || []) {
      const r = grade(String(x.value));
      say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value} lands on its key (got ok=${r.ok} key=${r.key})`);
      say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
    }
  } else if (w.kind === 'numeric') {
    nNum++; grade = (t) => num(w, t);
    const a = String(w.answer);
    say(grade(a).ok, null, `${where}: key ${a} grades correct`);
    say(grade(a.includes('.') ? a + '0' : a + '.0').ok, null, `${where}: key with one more place grades correct`);
    say(grade('x = ' + a).ok, null, `${where}: key after a letter and = grades correct`);
    if (w.answer < 0) say(grade(a.replace('-', '−')).ok, null, `${where}: key with a true minus sign grades correct`);
    if (w.unit) say(grade(a + ' ' + w.unit).ok, null, `${where}: key with its unit ${w.unit} grades correct`);
    for (const x of w.wrong || []) {
      const r = grade(String(x.value));
      say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value} lands on its key (got ok=${r.ok} key=${r.key})`);
      say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
    }
  } else if (w.kind === 'expression') {
    nExpr++; grade = (t) => expr(w, t);
    say(grade(w.answer).ok, null, `${where}: key grades correct`);
    for (const a of w.accept || []) say(grade(a).ok, null, `${where}: accept "${a}" grades correct`);
    for (const x of w.wrong || []) {
      const r = grade(x.tex);
      say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.tex} lands on its key (got ok=${r.ok} key=${r.key})`);
      say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
    }
  } else return;
  const rows = (ROWS[it.id] || {})[k] || [];
  if (!rows.length) { fails++; console.log(`FAIL    ${where}: no reader rows`); }
  for (const [text, want, note] of rows) {
    nRows++;
    const r = grade(text);
    const desc = `${where}: typed "${text}" is ${r.ok ? 'accepted' : 'refused'} (key ${r.key}${r.line ? ', line "' + r.line + '"' : ''})`;
    if (want === ANY) { checks++; console.log('NOTE    ' + desc); continue; }
    const good = want === true ? r.ok : want === false ? (!r.ok && r.key === null) : (!r.ok && r.key === want);
    say(good, note, `${desc}, expected ${want === true ? 'accepted' : want === false ? 'refused on no wrong line' : 'refused on ' + want}`);
  }
});
console.log(`\ngrade-probe: ${checks} checks over ${nNum} numeric, ${nSet} set and ${nExpr} expression parts, ${nRows} reader rows, ${fails} failures, ${findings} rows held to be faults`);
process.exit(fails ? 1 : 0);
