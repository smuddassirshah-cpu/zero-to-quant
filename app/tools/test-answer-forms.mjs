#!/usr/bin/env node
/* Unit tests for ENGINE-BACKLOG 830 to 832 (the expression forms "factorised-fully" and "completed-square", and set answers),
   in the manner of tools/test-expr-equations.mjs: the real grade.js with the local Compute Engine, no browser.
     Part 1: form "factorised-fully": a product with no bracket left holding a common whole-number factor or a quadratic that
             factorises (so (2x+4)(x+3) fails for 2(x+2)(x+3), and (x^2-4)(x+1) for (x-2)(x+2)(x+1)).
     Part 2: form "completed-square": a(x+p)^2 + q in either order, and nothing else, expanded or otherwise.
     Part 3: set answers for expression and numeric: any order, labels, "or" and "and", braces, \pm, the key "count", wrong sets.
     Part 4: the fixture set (tools/fixtures/fluency): every set family and both new forms draw and grade as the sampler says.
     Part 5: the real widgets in Chromium (skipped with --unit-only): the default lines for form, the count line, the set keyboard
             (a comma and a plus-or-minus) and the default keyboard back for an ordinary item.
   Usage: node tools/test-answer-forms.mjs [--local-cdn <pkgs>] [--unit-only]
   The Compute Engine comes from --local-cdn or ZQ_LOCAL_CDN. Exit 0 pass, 1 failure, 2 setup problem. */
import { spawn, execSync } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');
const argv = process.argv.slice(2);
const arg = (k) => { const i = argv.indexOf(k); return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? path.resolve(argv[i + 1]) : null; };
const cdn = arg('--local-cdn') || (process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null);
const die = (m) => { console.error('test-answer-forms: ' + m); process.exit(2); };
const ceFile = cdn && path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
if (!ceFile || !fs.existsSync(ceFile)) die('give --local-cdn <pkgs> (or ZQ_LOCAL_CDN) with the local Compute Engine');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const C = g.ComputeEngine.ComputeEngine || g.ComputeEngine, ce = new C();
g.ZQ = {};
vm.runInContext(fs.readFileSync(path.join(APP, 'js/engine/grade.js'), 'utf8'), g);
const G = g.ZQ.grade;
const fails = []; let n = 0;
const check = (name, ok, detail = '') => { n++; if (!ok) { fails.push(name); console.log(`FAIL ${name}  ${detail}`); } };

/* ---------- Part 1: factorised-fully (the widget's check: equal first, then the shape) ---------- */
const shaped = (form, key, typed) => G.exprEqual(ce, typed, key) && (form === 'factorised' ? G.withParsed(ce, typed, [], (e) => G.shapeFactorised(e.json)) : G.exprFormOk(ce, form, typed));
check('fully: 2(x+2)(x+3) passes', shaped('factorised-fully', '2(x+2)(x+3)', '2(x+2)(x+3)'));
check('fully: (x+2)(x+3)*2 passes (the number last)', shaped('factorised-fully', '2(x+2)(x+3)', '(x+2)(x+3)\\cdot 2'));
check('fully: (2x+4)(x+3) is equal but not fully factorised', !shaped('factorised-fully', '2(x+2)(x+3)', '(2x+4)(x+3)') && G.exprEqual(ce, '(2x+4)(x+3)', '2(x+2)(x+3)') && G.withParsed(ce, '(2x+4)(x+3)', [], (e) => G.shapeFactorised(e.json)));
check('fully: (x+2)(2x+6) fails', !shaped('factorised-fully', '2(x+2)(x+3)', '(x+2)(2x+6)'));
check('fully: 2(x^2+5x+6) fails (a quadratic with integer roots in the bracket)', !shaped('factorised-fully', '2(x+2)(x+3)', '2(x^2+5x+6)'));
check('fully: the expanded form fails', !shaped('factorised-fully', '2(x+2)(x+3)', '2x^2+10x+12'));
const yesFF = ['(x+2)(x+3)', '3(x+4)(x-4)', '(x-2)(x+2)(x+1)', '(x+1)^2', '2(x+1)^2', '-(x+2)(x+3)', 'x(x+3)', '(2x+1)(x+2)', '(x+2)^2(x-3)', '2x(x-1)(x+4)', '(3x-2)(2x+5)', '(x^2+4)(x+1)', '(x^2+x+1)(x+1)', '5(t+1)(t-2)', '-3(x-1)(x+2)', '(2-x)(x+3)', '(x-\\frac{1}{2})(x+3)'];
const noFF = ['(3x+12)(x-4)', '(x^2-4)(x+1)', '(x^2+5x+6)(x+1)', '(4x^2-9)(x+1)', '(2x+2)^2', '(x^2-2x+1)(x+3)', '(x^2+3x)(x+1)', '(2x^2+4)(x+1)', '(x^2-4)^2', '(6x+9)(2x-4)', '(3x-3)(x+2)', '(-2x-4)(x+3)', '(2x^2+5x+2)(x+1)', '(x+1)(5t+10)'];
yesFF.forEach((t) => check(`fully yes: ${t}`, G.withParsed(ce, t, [], (e) => G.shapeFullyFactorised(e.json))));
noFF.forEach((t) => check(`fully no: ${t}`, !G.withParsed(ce, t, [], (e) => G.shapeFullyFactorised(e.json))));
['x^2+5x+6', '2x+4', '(2x+4)', 'x+3', '12', '2(x+3)+1'].forEach((t) => check(`fully no (not even factorised): ${t}`, !G.withParsed(ce, t, [], (e) => G.shapeFullyFactorised(e.json))));
check('fully: plain factorised still accepts (2x+4)(x+3), as before', shaped('factorised', '2(x+2)(x+3)', '(2x+4)(x+3)'));
check('fully: exprFormOk is true for any other form and without an engine', G.exprFormOk(ce, 'expanded', '(2x+4)(x+3)') && G.exprFormOk(null, 'factorised-fully', '2x+4'));

/* ---------- Part 2: completed-square ---------- */
const cs = (t) => G.withParsed(ce, t, [], (e) => G.shapeCompletedSquare(e.json));
const yesCS = ['(x+3)^2-4', '(x-3)^2+4', '4+(x-3)^2', '-4+(x+3)^2', '2(x+1)^2-5', '-(x+3)^2+4', '4-(x+3)^2', '-2(x-1)^2+3', '3-2(x-1)^2', '\\frac{1}{2}(x+\\frac{1}{2})^2-4', '(x-\\frac{3}{2})^2-\\frac{29}{4}', '(3+x)^2-1', '(x+3)^2', '-(x-1)^2', '\\frac{(x+3)^2}{2}+1', '(t+3)^2-4', '0.5(x-2)^2+1.5', '(x+3)^2+(-4)', '5(x-\\frac{2}{3})^2+\\frac{1}{3}', '(y-0.5)^2-0.25'];
const noCS = ['x^2+6x+5', '(x+3)(x+3)-4', '(2x+3)^2-4', '(x+3)^2-4+1', '(x+3)^2+\\sqrt{2}', 'x^2-4', '(x+3)^3-4', '(x+3)^2-(x+1)', '(x+1)(x+5)', 'x(x+6)+5', '(x+3)^2+(x+3)^2', '(x+p)^2+q', '(x+3)^2-4x', '2x^2+12x+14', '2((x+3)^2-4)', '(x+3)^2-2-2', '3', 'x', '(x+3)^2(x-1)', '\\sqrt{(x+3)^2}-4'];
yesCS.forEach((t) => check(`completed square yes: ${t}`, cs(t)));
noCS.forEach((t) => check(`completed square no: ${t}`, !cs(t)));
check('completed square: the expanded form is equal but refused', shaped('completed-square', '(x+3)^2-4', '(x+3)^2-4') && G.exprEqual(ce, 'x^2+6x+5', '(x+3)^2-4') && !shaped('completed-square', '(x+3)^2-4', 'x^2+6x+5'));
check('completed square: another equal shape is refused', G.exprEqual(ce, '(x+2)(x+4)-1', '(x+3)^2-2') && !shaped('completed-square', '(x+3)^2-2', '(x+2)(x+4)-1'));
check('completed square: either order of the terms', shaped('completed-square', '-(x-2)^2+7', '7-(x-2)^2') && shaped('completed-square', '-(x-2)^2+7', '-(x-2)^2+7'));
check('completed square: a wrong value in the right shape is not equal', !shaped('completed-square', '(x+3)^2-4', '(x+3)^2+4'));

/* ---------- Part 3: set answers ---------- */
const ES = (answers, wrong) => ({ kind: 'expression', answers, unordered: true, ...(wrong ? { wrong } : {}) });
const NS = (answers, tol = { abs: 0 }, wrong) => ({ kind: 'numeric', answers, unordered: true, tol, ...(wrong ? { wrong } : {}) });
const eg = (spec, t) => G.exprSetGrade(ce, spec, t), ng = (spec, t) => G.numSetGrade(spec, t);
const two = ES(['2', '-5']);
['2,-5', '-5,2', '2, -5', '-5, 2', '2;-5', 'x=2, x=-5', 'x = -5, x = 2', 'x=2 or x=-5', 'x = 2\\text{ or }x = -5', 'x=-5\\text{ and }x=2', '\\{2,-5\\}', '\\left\\{-5,2\\right\\}', '\\lbrace 2, -5\\rbrace', '(2,-5)', '\\frac{4}{2}, -5', 'x_1=2, x_2=-5', '2 \\text{ or } -5', '2\\ or\\ -5', '2{,}-5', '\\sqrt{4}, -5', '−5, 2', '2\\,,-5', 'x=2\\operatorname{or}x=-5', '2 \\lor -5'].forEach((t) => check(`expression set yes: ${t}`, eg(two, t).ok === true, JSON.stringify(eg(two, t))));
[['2', 1], ['x=2', 1], ['2,-5,7', 3], ['2,2,-5', 3], ['-5', 1], ['2, -5, ', 2]].forEach(([t, k]) => { const r = eg(two, t); if (k === 2) check(`expression set: a trailing comma is not a value: ${t}`, r.ok === true); else check(`expression set count: ${t}`, r.ok === false && r.key === 'count' && r.line === `This question needs 2 values, separated by commas. You gave ${k}.`, JSON.stringify(r)); });
['2,5', '2,2', '-2,5', '3,-5', 'x=2, x=5', '5,-5', '2,-4'].forEach((t) => { const r = eg(two, t); check(`expression set no: ${t}`, r.ok === false && r.key === null, JSON.stringify(r)); });
check('expression set: an empty answer is not graded', eg(two, '').ok === false && eg(two, '  ').key === null);
const sw = ES(['2', '-5'], [{ id: 'signs', tex: '-2, 5' }, { id: 'one-sign', tex: '2, 5' }]);
check('expression set: a wrong set routes to its key, in any order', eg(sw, '5, -2').key === 'signs' && eg(sw, 'x=2, x=5').key === 'one-sign' && eg(sw, '1, 2').key === null);
const sur = ES(['3+\\sqrt{2}', '3-\\sqrt{2}']);
['3 \\pm \\sqrt{2}', 'x = 3 \\pm \\sqrt{2}', '3\\pm\\sqrt2', '3-\\sqrt{2}, 3+\\sqrt{2}', '\\sqrt{2}+3, 3-\\sqrt{2}', 'x=3+\\sqrt{2}\\text{ or }x=3-\\sqrt{2}', '3 ± \\sqrt{2}', '3 \\pm \\sqrt{2},', '\\frac{6 \\pm 2\\sqrt{2}}{2}'].forEach((t) => check(`surd set yes: ${t}`, eg(sur, t).ok === true, JSON.stringify(eg(sur, t))));
[['3 \\pm \\sqrt{3}', null], ['2 \\pm \\sqrt{2}', null], ['3+\\sqrt{2}', 'count'], ['\\pm\\sqrt{2}', null], ['3 \\pm \\sqrt{2}, 1', 'count'], ['3 \\pm 2', null], ['3 \\pm \\sqrt{2} \\pm 1', 'count']].forEach(([t, k]) => { const r = eg(sur, t); check(`surd set no: ${t}`, r.ok === false && r.key === k, JSON.stringify(r)); });
const pm3 = ES(['3', '-3']);
check('expression set: \\pm 3 and x = \\pm 3 are both values', eg(pm3, '\\pm 3').ok && eg(pm3, 'x=\\pm3').ok && eg(pm3, '\\pm 3, 3').key === 'count');
const frac = ES(['\\frac{1}{2}', '-\\frac{3}{4}', '2']);
check('expression set of three', eg(frac, '2, -0.75, 0.5').ok && eg(frac, '-\\frac{3}{4}, \\frac{2}{4}, 2').ok && !eg(frac, '2, -0.75, 0.6').ok && eg(frac, '2, -0.75').key === 'count');
check('expression set: no engine falls back to the written text', G.exprSetGrade(null, two, '-5, 2').ok === true && G.exprSetGrade(null, two, '2, 5').ok === false && G.exprSetGrade(null, two, 'x=2, x=-5').ok === true);
check('set text for display and the test hook', G.setAnswerText(two) === '2, -5' && G.correctValue({ kind: 'expression', answers: ['2', '-5'], unordered: true }) === '2, -5' && G.correctValue({ kind: 'numeric', answers: [2, -5.5], unordered: true }) === '2, -5.5' && G.correctValue({ kind: 'expression', answer: 'x+1' }) === 'x+1' && G.correctValue({ kind: 'numeric', answer: 0.25, tol: { abs: 0 } }) === '0.25');
check('isSetSpec: only answers makes a set', G.isSetSpec(two) && !G.isSetSpec({ kind: 'expression', answer: '2' }) && !G.isSetSpec(null));

const nset = NS([2, -5]);
['2, -5', '-5, 2', '2,-5', 'x = 2, x = -5', 'x=2 or x=-5', 'x = 2 or x = -5', '{2, -5}', '\\{2,-5\\}', '2 and -5', '4/2, -5', '−5, 2', '2.0, -5.00', '(2, -5)', 'x = 2; x = -5', '-10/2, 2'].forEach((t) => check(`numeric set yes: ${t}`, ng(nset, t).ok === true, JSON.stringify(ng(nset, t))));
[['2', 1], ['2, -5, 1', 3], ['x=2', 1], ['2, 2, -5', 3]].forEach(([t, k]) => { const r = ng(nset, t); check(`numeric set count: ${t}`, r.ok === false && r.key === 'count' && r.line === `This question needs 2 values, separated by commas. You gave ${k}.`, JSON.stringify(r)); });
['2, 5', '-2, 5', '2, 2', '3, -5', 'x=2, x=5'].forEach((t) => { const r = ng(nset, t); check(`numeric set no: ${t}`, r.ok === false && r.key === null, JSON.stringify(r)); });
['', '  ', 'two, five', '2, abc', '2,,'].forEach((t) => check(`numeric set unreadable: "${t}"`, ng(nset, t).ok === false && ng(nset, t).key === null || (t === '2,,' && ng(nset, t).key === 'count'), JSON.stringify(ng(nset, t))));
const ntol = NS([0.5, 1.5], { abs: 0.01 });
check('numeric set: the tolerance applies to each value', ng(ntol, '1.505, 0.495').ok && ng(ntol, '1/2, 3/2').ok && !ng(ntol, '1.52, 0.5').ok && !ng(ntol, '0.5, 1.5, 1.5').ok);
const nrel = NS([100, 2000], { rel: 0.01 });
check('numeric set: a relative tolerance', nrel && ng(nrel, '1995, 100.5').ok && !ng(nrel, '1960, 100').ok);
const npm = NS([5, 1]);
['3 ± 2', '3 \\pm 2', '3 +- 2', '3 +/- 2', 'x = 3 ± 2', '3±2', '1, 5', '3 ± 2'].forEach((t) => check(`numeric set \\pm yes: ${t}`, ng(npm, t).ok === true, JSON.stringify(ng(npm, t))));
['3 ± 3', '± 2', '3 ± 2, 1', '3 ±', '3 ± 2 ± 1'].forEach((t) => check(`numeric set \\pm no: ${t}`, ng(npm, t).ok === false, JSON.stringify(ng(npm, t))));
check('numeric set: ±3 is both 3 and -3', ng(NS([3, -3]), '±3').ok && ng(NS([3, -3]), 'x = \\pm 3').ok);
const nw = NS([2, -5], { abs: 0 }, [{ id: 'signs', value: '-2, 5' }, { id: 'one', value: '2, 5' }]);
check('numeric set: a wrong set routes to its key, in any order', ng(nw, '5, -2').key === 'signs' && ng(nw, 'x=5, x=2').key === 'one' && ng(nw, '7, 8').key === null && ng(nw, '2, -5').ok);
check('numeric set: a three-value set and decimals', ng(NS([0.25, 1, -3]), '-3, 1/4, 1').ok && ng(NS([0.25, 1, -3]), '-3, 0.25').key === 'count');
check('numeric: a single-answer spec is untouched by the set code', G.within(2, 2, { abs: 0 }) && G.parseNum('1,000') === 1000);

/* ---------- Part 4: the fixture set ---------- */
const fix = JSON.parse(fs.readFileSync(path.join(APP, 'tools/fixtures/fluency/fluency-l3-opening-brackets.json'), 'utf8'));
const gen = (await import('node:module')).createRequire(import.meta.url)('../js/engine/gen.js');
const fam = (id) => fix.families.find((f) => f.id === id);
const need = ['factorise-fully', 'complete-the-square', 'roots-numeric', 'roots-expression', 'roots-surd'];
need.forEach((id) => check(`fixture has the family ${id}`, !!fam(id)));
const mathOf = (p) => (String(p).match(/\$[^$]+\$/g) || []).map((x) => x.slice(1, -1));
need.filter(fam).forEach((id) => {
  const f = fam(id), r = gen.sample(f, { seeds: 60, set: fix.id });
  check(`fixture ${id}: draws 60 of 60`, r.failed === 0 && r.items.length === 60, `${r.failed} failed`);
  let bad = 0, badWrong = 0, badForm = 0, badCount = 0, first = '';
  r.items.forEach((it) => {
    const w = { ...it.widget, wrong: it.wrong.map((x) => (x.tex !== undefined ? { id: x.id, tex: x.tex } : { id: x.id, value: x.value })) };
    if (w.answers) {
      const typed = it.widget.kind === 'numeric' ? it.widget.answers.map((a) => G.fmtNum(+a)).join(', ') : it.widget.answers.join(', ');
      const res = w.kind === 'numeric' ? ng(w, typed) : eg(w, typed), rev = w.kind === 'numeric' ? ng(w, typed.split(', ').reverse().join(', ')) : eg(w, it.widget.answers.slice().reverse().join(', '));
      if (!res.ok || !rev.ok) { bad++; first = first || `${it.prompt}: ${typed}`; }
      const short = w.kind === 'numeric' ? ng(w, G.fmtNum(+it.widget.answers[0])) : eg(w, it.widget.answers[0]);
      if (short.key !== 'count') badCount++;
      it.wrong.forEach((x) => { const t = x.tex !== undefined ? x.tex : x.value, rr = w.kind === 'numeric' ? ng({ ...w, wrong: [] }, t) : eg({ ...w, wrong: [] }, t); if (rr.ok) badWrong++; });
    } else {
      if (!G.exprEqual(ce, it.widget.answer, it.widget.answer) || !shaped(it.widget.form, it.widget.answer, it.widget.answer)) { bad++; first = first || `${it.prompt}: ${it.widget.answer}`; }
      it.wrong.forEach((x) => { if (shaped(it.widget.form, it.widget.answer, x.tex)) badWrong++; });
      mathOf(it.prompt).forEach((m) => { if (shaped(it.widget.form, it.widget.answer, m)) badForm++; });
    }
  });
  check(`fixture ${id}: the answer is graded correct (in any order for a set)`, bad === 0, `${bad} failures, first ${first}`);
  check(`fixture ${id}: no wrong is graded correct`, badWrong === 0, `${badWrong}`);
  if (f.widget.form) check(`fixture ${id}: the prompt's own expression typed back fails form ${f.widget.form}`, badForm === 0, `${badForm}`);
  if (f.widget.answers) check(`fixture ${id}: one value alone returns count`, badCount === 0, `${badCount}`);
});

/* ---------- Part 4b (ENGINE-BACKLOG 841): form "fraction" and "exact-angle" ---------- */
const shapedT = (form, key, typed) => G.exprEqual(ce, typed, key) && G.exprFormOk(ce, form, typed);
['\\frac{7}{9}', '-\\frac{7}{9}', '\\frac{-7}{9}', '7/9', '-7/9', '\\dfrac{7}{9}', '\\frac{ 7 }{ 9 }', '\\left(\\frac{7}{9}\\right)'].forEach((t) => check(`fraction yes: ${t}`, G.shapeFraction(t) === (t !== '\\left(\\frac{7}{9}\\right)')));
['0.7778', '\\frac{14}{18}', '14/18', '0.\\dot{7}', '7/9+0', '1\\frac{2}{3}', '\\frac{7}{9}x', '\\frac{4}{1}', '\\frac{0}{5}', '-\\frac{-7}{9}', '', '\\frac{7.5}{9}', '\\frac{7}{9.5}', '\\sqrt{2}', '+3'].forEach((t) => check(`fraction no: "${t}"`, !G.shapeFraction(t)));
['3', '-3', '0', '12'].forEach((t) => check(`fraction yes (a whole number): ${t}`, G.shapeFraction(t)));
check('fraction: equal but unreduced or decimal fails the shape, a wrong value is not equal', shapedT('fraction', '\\frac{7}{9}', '\\frac{7}{9}') && G.exprEqual(ce, '\\frac{14}{18}', '\\frac{7}{9}') && !shapedT('fraction', '\\frac{7}{9}', '\\frac{14}{18}') && !shapedT('fraction', '\\frac{1}{2}', '0.5') && !G.exprEqual(ce, '\\frac{7}{8}', '\\frac{7}{9}'));
check('fraction: a whole-number key', shapedT('fraction', '3', '3') && !shapedT('fraction', '3', '\\frac{6}{2}') && !shapedT('fraction', '3', '3.0'));
['\\pi', '3\\pi', '-\\pi', '-2\\pi', '\\frac{\\pi}{12}', '\\frac{5\\pi}{12}', '-\\frac{\\pi}{4}', '\\frac{-3\\pi}{4}', '\\frac{5}{12}\\pi', '5\\pi/12', '\\pi/12', '0', '\\dfrac{3\\pi}{2}', '\\frac{7\\pi}{6}', '\\frac{\\pi}{ 4 }', 'π', '3π/4'].forEach((t) => check(`exact-angle yes: ${t}`, G.shapeExactAngle(t)));
['15^\\circ', '15\\degree', '15°', '\\frac{15\\pi}{180}', '\\frac{2\\pi}{4}', '\\frac{6\\pi}{8}', '\\frac{3}{6}\\pi', '6\\pi/8', '0.25\\pi', '0.7854', '\\frac{\\pi}{12}+0', '\\frac{\\pi}{1}', '1\\pi', '0\\pi', '\\frac{15}{180}\\pi', ''].forEach((t) => check(`exact-angle no: "${t}"`, !G.shapeExactAngle(t)));
check('exact-angle: 15 degrees typed in any form is equal, only the radian shape passes', shapedT('exact-angle', '\\frac{\\pi}{12}', '\\frac{\\pi}{12}') && !shapedT('exact-angle', '\\frac{\\pi}{12}', '15^\\circ') && !shapedT('exact-angle', '\\frac{\\pi}{12}', '\\frac{15\\pi}{180}') && G.exprEqual(ce, '\\frac{15\\pi}{180}', '\\frac{\\pi}{12}') && !shapedT('exact-angle', '\\frac{\\pi}{12}', '\\frac{\\pi}{6}'));
check('forms: exprFormOk is true for every other form', G.exprFormOk(ce, 'expanded', '0.5') && G.exprFormOk(ce, 'simplified', '15^\\circ'));

/* ---------- Part 5: the real widgets ---------- */
const browser = async () => {
  let pw = null;
  try { pw = await import('playwright'); } catch { /* not local */ }
  if (!pw) {
    const roots = [];
    try { roots.push(execSync('npm root -g', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim()); } catch { /* no npm */ }
    (process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean).forEach((r) => roots.push(r));
    for (const r of roots) { const f = path.join(r, 'playwright', 'index.mjs'); if (!pw && fs.existsSync(f)) pw = await import(pathToFileURL(f).href); }
  }
  if (!pw) { console.log('note: Playwright is not installed; part 5 (the real widgets) is skipped'); return; }
  const port = await new Promise((res, rej) => { const sv = net.createServer(); sv.unref(); sv.on('error', rej); sv.listen(0, '127.0.0.1', () => { const q = sv.address().port; sv.close(() => res(q)); }); });
  const proc = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', APP], { stdio: 'ignore' });
  const base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 100; i++) { try { if ((await fetch(base + '/index.html')).ok) break; } catch { /* not up */ } await new Promise((r) => setTimeout(r, 100)); }
  const CHROMIUM = '/opt/pw-browsers/chromium';
  const b = await pw.chromium.launch({ headless: true, ...(fs.existsSync(CHROMIUM) ? { executablePath: CHROMIUM } : {}) });
  const MIME = { '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.wasm': 'application/wasm' };
  try {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 860 } });
    await ctx.route(/^https:\/\/cdn\.jsdelivr\.net\//, async (route) => {
      const m = new URL(route.request().url()).pathname.match(/^\/npm\/(@[^/]+\/[^@/]+|[^@/]+)@([^/]+)\/(.*)$/);
      const f = m && path.join(cdn, `${m[1].replace(/^@/, '').replace('/', '-')}-${m[2]}`, 'package', m[3]);
      if (f && fs.existsSync(f) && fs.statSync(f).isFile()) return route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
      return route.fulfill({ status: 404, body: '' });
    });
    await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, (r) => r.fulfill({ status: 200, body: '', headers: { 'content-type': 'text/css' } }));
    const page = await ctx.newPage();
    page.on('pageerror', (e) => check('no uncaught error in the page', false, String(e).slice(0, 200)));
    await page.goto(base + '/#today');
    await page.waitForFunction(() => window.ZQ && ZQ.widgets && ZQ.grade, null, { timeout: 30000 });
    const ready = await page.evaluate(() => ZQ.grade.maths().then((m) => !!(m && m.ce && m.mathlive)));
    if (!ready) { console.log('note: MathLive or the Compute Engine did not load; part 5 is skipped'); return; }
    const run = (spec, typed) => page.evaluate(async ([spec, typed]) => {
      const host = document.createElement('div'); document.body.append(host);
      const w = ZQ.widgets.create(host, spec, {});
      const out = [];
      for (const t of typed) { w.reset && w.reset(); w.set(t); const r = await w.grade(); out.push({ ok: !!r.ok, key: r.key ?? null, line: r.line ?? null }); }
      w.reset(); w.set(typed[0]);
      const shown = { answer: w.answer(), ready: w.ready() };
      w.destroy && w.destroy(); host.remove();
      return { out, shown };
    }, [spec, typed]);
    let r = await run({ kind: 'expression', answer: '2(x+2)(x+3)', form: 'factorised-fully' }, ['2(x+2)(x+3)', '(2x+4)(x+3)', '(x+2)(x+3)']);
    check('widget factorised-fully: right, not fully factorised (default line), wrong', r.out[0].ok && !r.out[1].ok && r.out[1].key === 'form' && r.out[1].line === 'Factorise fully: a bracket still has a common factor.' && !r.out[2].ok && r.out[2].key === null, JSON.stringify(r.out));
    r = await run({ kind: 'expression', answer: '(x+3)^2-4', form: 'completed-square' }, ['(x+3)^2-4', '4-(x+3)^2', 'x^2+6x+5', '(x+3)^2+4']);
    check('widget completed-square: right, expanded is refused (default line), a wrong number is wrong', r.out[0].ok && !r.out[1].ok && !r.out[2].ok && r.out[2].key === 'form' && r.out[2].line === 'Write it as a bracket squared plus a number.' && !r.out[3].ok && r.out[3].key === null, JSON.stringify(r.out));
    r = await run({ kind: 'expression', answer: '-(x-2)^2+7', form: 'completed-square' }, ['7-(x-2)^2']);
    check('widget completed-square: either order of the two terms', r.out[0].ok, JSON.stringify(r.out));
    r = await run({ kind: 'expression', answer: '\\frac{1}{2}', form: 'fraction' }, ['\\frac{1}{2}', '1/2', '\\frac{2}{4}', '0.5', '\\frac{1}{3}']);
    check('widget fraction: lowest terms pass, unreduced and decimal return form with the default line, a wrong value is wrong', r.out[0].ok && r.out[1].ok && !r.out[2].ok && r.out[2].key === 'form' && r.out[2].line === 'That is equal, but write it as a whole number or one fraction in lowest terms, with no decimal point.' && !r.out[3].ok && r.out[3].key === 'form' && !r.out[4].ok && r.out[4].key === null, JSON.stringify(r.out));
    r = await run({ kind: 'expression', answer: '\\frac{\\pi}{12}', form: 'exact-angle' }, ['\\frac{\\pi}{12}', '\\frac{15\\pi}{180}', '15^\\circ', '\\frac{\\pi}{6}']);
    check('widget exact-angle: lowest terms pass, an unreduced multiple and degrees return form, a wrong angle is wrong', r.out[0].ok && !r.out[1].ok && r.out[1].key === 'form' && !r.out[2].ok && r.out[2].key === 'form' && !r.out[3].ok && r.out[3].key === null && /radians/.test(r.out[1].line || ''), JSON.stringify(r.out));
    r = await run({ kind: 'expression', answer: '\\frac{\\ln 97}{\\ln 4}', accept: ['ln(97)/ln(4)'], wrong: [{ id: 'quotient', tex: '\\frac{97}{4}' }] }, ['ln(97)/ln(4)', '\\frac{\\ln(97)}{\\ln(4)}', '\\frac{97}{4}', 'log(97)/log(4)']);
    check('widget: a plain-text function name is the function (836), and the letters quotient is the wrong key', r.out[0].ok && r.out[1].ok && !r.out[2].ok && r.out[2].key === 'quotient' && r.out[3].ok, JSON.stringify(r.out));
    r = await run({ kind: 'expression', answers: ['2', '-5'], unordered: true, wrong: [{ id: 'signs', tex: '-2, 5' }] }, ['2, -5', '-5, 2', 'x=2\\text{ or }x=-5', '2', '2, -5, 1', '5, -2', '2, 5']);
    check('widget expression set: any order and "or", count for a missing or extra value, a wrong set routes', r.out[0].ok && r.out[1].ok && r.out[2].ok && !r.out[3].ok && r.out[3].key === 'count' && r.out[4].key === 'count' && r.out[5].key === 'signs' && r.out[6].key === null && r.out.slice(3).every((x) => !x.ok), JSON.stringify(r.out));
    check('widget expression set: the count line says how many values are expected', r.out[3].line === 'This question needs 2 values, separated by commas. You gave 1.' && r.out[4].line === 'This question needs 2 values, separated by commas. You gave 3.', JSON.stringify(r.out[3]));
    check('widget expression set: the test hook types the whole set', r.shown.answer === '2, -5' && r.shown.ready === true, JSON.stringify(r.shown));
    r = await run({ kind: 'expression', answers: ['3+\\sqrt{2}', '3-\\sqrt{2}'], unordered: true }, ['3 \\pm \\sqrt{2}', 'x=3\\pm\\sqrt{2}', '3+\\sqrt{2}', '3 \\pm \\sqrt{3}']);
    check('widget expression set: \\pm stands for both values', r.out[0].ok && r.out[1].ok && !r.out[2].ok && r.out[2].key === 'count' && !r.out[3].ok, JSON.stringify(r.out));
    r = await run({ kind: 'numeric', answers: [2, -5], unordered: true, tol: { abs: 0 }, wrong: [{ id: 'signs', value: '-2, 5' }] }, ['2, -5', '-5,2', 'x = 2 or x = -5', '2', '2, -5, 7', '5, -2', '2, 5']);
    check('widget numeric set: any order and "or", count, a wrong set routes', r.out[0].ok && r.out[1].ok && r.out[2].ok && r.out[3].key === 'count' && r.out[4].key === 'count' && r.out[5].key === 'signs' && !r.out[6].ok && r.out[6].key === null, JSON.stringify(r.out));
    check('widget numeric set: the hook and the readiness', r.shown.answer === '2, -5' && r.shown.ready === true, JSON.stringify(r.shown));
    r = await run({ kind: 'numeric', answers: [5, 1], unordered: true, tol: { abs: 0 } }, ['3 ± 2', '3 \\pm 2', '3 ± 3']);
    check('widget numeric set: ± stands for both values', r.out[0].ok && r.out[1].ok && !r.out[2].ok, JSON.stringify(r.out));
    /* ENGINE-BACKLOG 837: a generated item answered with the widget's own key (length, form, count) shows the stock line and then the solution steps */
    const chips = await page.evaluate(async () => {
      const host = document.createElement('div'); document.body.append(host);
      const mk = (widget, solution) => ZQ.gen.playerItem({ family: 'f', skill: 'a skill', vars: {}, lets: {}, prompt: 'Work out $1 + 1$.', widget, wrong: [], solution }, { id: 'set-x', title: 't' }, 0);
      const out = {};
      for (const [name, widget, how] of [['length', { kind: 'expression', answer: '(4, 6)' }, 'wrong'], ['form', { kind: 'expression', answer: '\\frac{2}{4}', form: 'fraction' }, 'right'], ['count', { kind: 'numeric', answers: [2, -5], unordered: true, tol: { abs: 0 } }, 'wrong'], ['plain', { kind: 'numeric', answer: 4, tol: { abs: 0 } }, 'wrong']]) {
        const run = ZQ.player.runSet(host, { title: 't', items: [mk(widget, ['First step $2 + 2 = 4$.', 'Second step $3 + 3 = 6$.'])] });
        await new Promise((q) => setTimeout(q, 800));
        if (how === 'wrong') ZQ.test.answerWrong(); else ZQ.test.answerCorrect();
        await new Promise((q) => setTimeout(q, 300));
        const r = await ZQ.test.check();
        await new Promise((q) => setTimeout(q, 300));
        out[name] = { key: r && r.key, ok: r && r.ok, chip: (document.querySelector('.lsn-verdict .lsn-chip.is-no') || {}).innerText || '', maths: document.querySelectorAll('.lsn-verdict .lsn-chip.is-no .katex').length };
        run.destroy(); host.innerHTML = '';
      }
      host.remove();
      return out;
    });
    check('player: a generated item answered with key length shows the stock line and the solution steps', chips['length'] && chips['length'].key === 'length' && /First step/.test(chips['length'].chip) && /Second step/.test(chips['length'].chip) && chips['length'].chip.length > 60 && chips['length'].maths > 0, JSON.stringify(chips['length']));
    check('player: key form shows its line and then the steps', chips.form && chips.form.key === 'form' && /lowest terms/.test(chips.form.chip) && /First step/.test(chips.form.chip), JSON.stringify(chips.form));
    check('player: key count shows its line and then the steps', chips.count && chips.count.key === 'count' && /needs 2 values/.test(chips.count.chip) && /First step/.test(chips.count.chip), JSON.stringify(chips.count));
    check('player: an ordinary wrong answer still shows the steps alone', chips.plain && chips.plain.key === null && /First step/.test(chips.plain.chip), JSON.stringify(chips.plain));
    const inputmode = await page.evaluate(() => {
      const host = document.createElement('div'); document.body.append(host);
      ZQ.widgets.create(host, { kind: 'numeric', answers: [2, -5], unordered: true, tol: { abs: 0 } }, {});
      ZQ.widgets.create(host, { kind: 'numeric', answer: 2, tol: { abs: 0 } }, {});
      const m = [...host.querySelectorAll('input')].map((i) => i.getAttribute('inputmode')); host.remove(); return m;
    });
    check('widget numeric set: the phone keyboard is the text one (it has a comma), a single answer keeps decimal', inputmode[0] === 'text' && inputmode[1] === 'decimal', JSON.stringify(inputmode));
    /* the maths keyboard: a set item offers a comma and a plus-or-minus; an ordinary item gets the default back */
    const kb = await page.evaluate(async () => {
      const host = document.createElement('div'); document.body.append(host);
      const mk = async (spec) => { const w = ZQ.widgets.create(host, spec, {}); await ZQ.grade.maths(); await new Promise((q) => setTimeout(q, 400)); return w; };
      const out = {}, flat = () => JSON.stringify(window.mathVirtualKeyboard.layouts);
      const setW = await mk({ kind: 'expression', answers: ['2', '-5'], unordered: true });
      setW.el.querySelector('.wd-kb').click(); await new Promise((q) => setTimeout(q, 600));
      out.setLayout = flat(); out.visible = window.mathVirtualKeyboard.visible;
      setW.el.querySelector('.wd-kb').click(); await new Promise((q) => setTimeout(q, 300));
      const oneW = await mk({ kind: 'expression', answer: 'x+1' });
      oneW.el.querySelector('.wd-kb').click(); await new Promise((q) => setTimeout(q, 600));
      out.defaultLayout = flat();
      try { window.mathVirtualKeyboard.hide(); } catch (e) { /* none */ }
      host.remove();
      return out;
    });
    check('widget expression set: the maths keyboard opens with its own layout holding a comma and a plus-or-minus', kb.visible === true && /\\\\pm/.test(kb.setLayout) && /\[,\]/.test(kb.setLayout) && /\[7\]/.test(kb.setLayout), (kb.setLayout || '').slice(0, 200));
    check('widget expression: an ordinary item opens the default keyboard again', !/\\\\pm/.test(kb.defaultLayout || ''), (kb.defaultLayout || '').slice(0, 200));
    await ctx.close();
  } finally { await b.close(); proc.kill(); }
};
if (!argv.includes('--unit-only')) await browser();

console.log(`test-answer-forms: ${n - fails.length}/${n} passed${fails.length ? ', ' + fails.length + ' FAILED' : ''}`);
process.exit(fails.length ? 1 : 0);
