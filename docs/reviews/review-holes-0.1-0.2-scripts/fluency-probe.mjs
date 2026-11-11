#!/usr/bin/env node
/* Second read of the nine level 4 Fluency sets: every draw made by draw.sh goes through the engine's own graders
   (grade.js numGrade, numSetGrade, exprGrade with the local Compute Engine).
     - the answer (as the accept line prints it, where there is one) grades correct; each wrong lands on its own key
     - other forms a learner who is right would type, and entries one step short, built from each draw's prompt:
       a row marked WANT-OK that is refused, or WANT-NO that is accepted, prints as FINDING and is counted per family
   node docs/reviews/review-holes-0.1-0.2-scripts/fluency-probe.mjs --local-cdn <pkgs> --dir <draws> [--show]   (repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const cdn = argv[argv.indexOf('--local-cdn') + 1], dir = argv[argv.indexOf('--dir') + 1], SHOW = argv.includes('--show');
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;

const specOf = (it) => {
  const w = { kind: it.kind, tol: it.tol, unit: it.unit, form: it.form, wrong: (it.wrong || []).map(x => (x.tex != null ? { id: x.id, tex: x.tex } : { id: x.id, value: x.value, tol: x.tol })) };
  if (it.answers) { w.answers = it.answers; w.unordered = true; } else w.answer = it.answer;
  if (it.kind === 'expression' && Array.isArray(it.accept)) w.accept = it.accept;
  return w;
};
const grade = (w, text) => {
  if (w.kind === 'expression') { const r = G.exprGrade(ce, w, text, text); return { ok: !!r.ok, key: r.key || null }; }
  if (w.answers) { const r = G.numSetGrade(w, text); return { ok: !!r.ok, key: r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null) }; }
  const r = G.numGrade(w, text); return { ok: !!r.ok, key: r.key || (r.detail.value == null ? 'NOPARSE' : null) };
};
const fracs = (p) => [...p.matchAll(/\\dfrac\{([^{}]*)\}\{([^{}]*)\}/g)].map(m => [m[1], m[2]]);
const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; };
const lin = (s) => { const m = /^(-?\d*)([a-z])([+-]\d+)$/.exec(s); if (!m) return null; return { a: m[1] === '' ? 1 : m[1] === '-' ? -1 : +m[1], v: m[2], b: +m[3] }; };
const sg = (n) => (n < 0 ? '' + n : '+' + n);
const r1 = (x, dp) => (Math.round(x * 10 ** dp + 1e-9) / 10 ** dp).toFixed(dp);

/* per family: rows [text, want ok?, note] built from one draw */
const ALT = {
  'add-tops': (it) => {
    const [[p, d1], [q, d2]] = fracs(it.prompt), l = lin(it.answer), rows = [[`${p}(${d2})+${q}(${d1})`, false, 'tops not multiplied out'], [`\\frac{${it.answer}}{(${d1})(${d2})}`, false, 'the whole fraction']];
    if (l) { rows.push([`${l.b}${sg(l.a)}${l.v}`, true, 'constant first']); const k = gcd(l.a, l.b); if (k > 1) rows.push([`${k}(${l.a / k === 1 ? '' : l.a / k}${l.v}${sg(l.b / k)})`, true, 'the top with its common factor taken out']); }
    return rows;
  },
  'subtract-tops': (it) => {
    const [[p, d1], [q, d2]] = fracs(it.prompt), l = lin(it.answer), rows = [[`${p}(${d2})-${q}(${d1})`, false, 'tops not multiplied out'], [`\\frac{${it.answer}}{(${d1})(${d2})}`, false, 'the whole fraction']];
    if (l) { rows.push([`${l.b}${sg(l.a)}${l.v}`, true, 'constant first']); const k = gcd(l.a, l.b); if (k > 1) rows.push([`${k}(${l.a / k === 1 ? '' : l.a / k}${l.v}${sg(l.b / k)})`, true, 'the top with its common factor taken out']); }
    return rows;
  },
  'cancel-common-bracket': (it) => { const [[t, b], [, d]] = fracs(it.prompt); return [[`(${it.answer})`, true, 'in a bracket'], [t, false, 'the top of the question'], [`\\frac{${t}}{${b}}`, false, 'the question typed back'], [`\\frac{${it.answer}}{${d}}`, false, 'the whole fraction']]; },
  'multiply-and-cancel': (it) => { const [[t1, b1], [t2, b2]] = fracs(it.prompt); return [[`\\frac{${t1}}{${b1}}\\times\\frac{${t2}}{${b2}}`, false, 'the question typed back'], [`\\frac{(${t1})(${t2})}{(${b1})(${b2})}`, false, 'one fraction, nothing cancelled'], [it.answer.replace(/^(-?\d+)(\(.*\))$/, '$2$1'), true, 'bracket first']]; },
  'divide-and-cancel': (it) => { const [[t1, b1], [t2, b2]] = fracs(it.prompt); return [[`\\frac{${t1}}{${b1}}\\div\\frac{${t2}}{${b2}}`, false, 'the question typed back'], [`\\frac{${t1}}{${b1}}\\times\\frac{${b2}}{${t2}}`, false, 'flipped, nothing cancelled'], [`\\frac{(${t1})(${b2})}{(${b1})(${t2})}`, false, 'one fraction, nothing cancelled'], [it.answer.replace(/^([a-z])(\(.*\))$/, '$2$1'), true, 'bracket first']]; },
  quotient: (it) => {
    const m = /Divide \$(.*?)\$ by \$\((.*?)\)\$/.exec(it.prompt), q = /^([a-z])\^2([+-]\d*)[a-z]([+-]\d+)$/.exec(it.answer), rows = [[`\\frac{${m[1]}}{${m[2]}}`, false, 'the question typed back'], [`(${it.answer})`, true, 'in a bracket']];
    if (q) { const b = q[2] === '+' ? 1 : q[2] === '-' ? -1 : +q[2], c = +q[3], d = b * b - 4 * c, s = Math.sqrt(d); if (d >= 0 && Number.isInteger(s)) { const r1_ = (-b + s) / 2, r2_ = (-b - s) / 2; if (Number.isInteger(r1_)) rows.push([`(${q[1]}${sg(-r1_)})(${q[1]}${sg(-r2_)})`, true, 'the quotient typed factorised']); } }
    return rows;
  },
  'factorise-cubic': (it) => { const b = it.answer.match(/\([^()]*\)/g) || []; const p = /Factorise \$(.*?)\$ fully/.exec(it.prompt)[1]; return b.length === 3 ? [[b[2] + b[0] + b[1], true, 'brackets in another order'], [p, false, 'the cubic typed back'], [`${b[0]}(${b[1]}${b[2]})`, true, 'two brackets grouped'], [b.join('\\times'), true, 'with times signs']] : []; },
  'solve-two-roots': (it) => [[`${it.answers[1]}, ${it.answers[0]}`, true, 'other order'], [`x=${it.answers[0]} or x=${it.answers[1]}`, true, 'with x ='], [`${it.answers[0]}`, false, 'one root only']],
  'reject-root': (it) => [[`x=${it.answer}`, true, 'with x =']],
  'circle-area': (it) => { const m = /has (radius|diameter) \$([\d.]+)\$/.exec(it.prompt), r = m[1] === 'radius' ? +m[2] : +m[2] / 2; return [[r1(3.14 * r * r, 1), true, 'pi = 3.14'], [r1(22 / 7 * r * r, 1), true, 'pi = 22/7'], [r1(Math.PI * r * r, 2), true, '2 d.p.'], [r1(Math.PI * r * r, 0), Math.abs(+r1(Math.PI * r * r, 0) - it.answer) <= 0.2, 'whole number'], [`${r1(Math.PI * r * r, 1)} ${it.unit}`, true, 'with the unit']]; },
  circumference: (it) => { const m = /has (radius|diameter) \$([\d.]+)\$/.exec(it.prompt), d = m[1] === 'radius' ? 2 * m[2] : +m[2]; return [[r1(3.14 * d, 1), true, 'pi = 3.14'], [r1(22 / 7 * d, 1), true, 'pi = 22/7'], [r1(Math.PI * d, 2), true, '2 d.p.'], [`${r1(Math.PI * d, 1)} ${it.unit}`, true, 'with the unit']]; },
  'speed-units': (it) => [[r1(it.answer, 1), true, '1 d.p.'], [r1(it.answer, 2), true, '2 d.p.'], [`${r1(it.answer, 1)} ${/into metres/.test(it.prompt) ? 'm/s' : 'km/h'}`, true, 'with the unit']],
  'table-mean': (it) => [[r1(it.answer, 2), true, '2 d.p.'], [r1(it.answer, 3), true, '3 d.p.']],
  'area-units': (it) => [[Number(it.answer).toLocaleString('en-GB'), true, 'with a thousands comma'], [`${it.answer} cm²`, true, 'with the unit']],
  mean: (it) => [[`£${it.answer}`.replace('£-', '-£'), true, 'with the pound sign']],
};

let checks = 0, fails = 0; const find = {}; const per = {};
for (const f of fs.readdirSync(dir).filter(x => x.endsWith('.json')).sort()) {
  const doc = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
  for (const it of doc.items) {
    const w = specOf(it), where = `${f.replace('.json', '')} seed ${it.seed}`, fam = it.family;
    per[fam] = per[fam] || { draws: 0, rows: 0 }; per[fam].draws++;
    const bad = (msg) => { fails++; console.log('FAIL    ' + where + ': ' + msg); };
    const ans = it.answers ? it.answers.join(', ') : it.kind === 'numeric' && typeof it.accept === 'string' && /^-?[\d.]+$/.test(it.accept) ? it.accept : String(it.answer);
    checks++; if (!grade(w, ans).ok) bad(`answer "${ans}" does not grade correct`);
    for (const x of w.wrong) { checks++; const r = grade(w, String(x.value ?? x.tex)); if (r.ok || (w.kind === 'expression' && r.key !== x.id)) bad(`wrong ${x.id} "${x.value ?? x.tex}" grades ok=${r.ok} key=${r.key}`); }
    for (const [text, want, why] of (ALT[fam] ? ALT[fam](it) : [])) {
      checks++; per[fam].rows++;
      let r; try { r = grade(w, text); } catch (e) { r = { ok: null, key: 'THROW' }; }
      if (r.ok !== want) { const k = `${fam}: ${why} is ${r.ok ? 'accepted' : 'refused (key ' + r.key + ')'}`; (find[k] = find[k] || []).push(`${text}   [${it.prompt}]`); }
      else if (SHOW) console.log(`ok      ${where}: "${text}" ${r.ok ? 'accepted' : 'refused ' + r.key}`);
    }
  }
}
console.log('rows that went against the reader (FINDING candidates), with the number of draws and one example:');
for (const [k, v] of Object.entries(find)) console.log(`  [${v.length} of ${per[k.split(':')[0]].draws}] ${k}\n        e.g. ${v[0]}`);
console.log(`fluency-probe: ${checks} checks, ${fails} failures, ${Object.keys(find).length} finding classes`);
process.exit(fails ? 1 : 0);
