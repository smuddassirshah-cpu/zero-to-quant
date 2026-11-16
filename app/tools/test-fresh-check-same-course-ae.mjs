#!/usr/bin/env node
// Test for the reuse shapes of tools/same-course-reuse.mjs and tools/reuse-shapes.mjs (engine pass AE part 1, ENGINE-BACKLOG 993): a function with its interval or factorisation,
// a key number pair, a shifted or scaled set, a region with its integrand. The fixtures under tools/fixtures/same-course-ae/content hold the pre-fix text of the eight reuse findings of the
// session AD reviews (review-problems-analysis-4-5, -odes-4, -vector-calc-1-3: items rebuilt from `git show <fix commit>^`, sources copied unchanged) and four rulings that must stay silent
// (a single common fraction, a simple quadratic with small whole roots shared with another topic's factorising screen, a taught definition or basis, a two-state chain across two topics).
// Run from app/: node tools/test-fresh-check-same-course-ae.mjs   (about two seconds)
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const HERE = dirname(fileURLToPath(import.meta.url));
const SC = join(HERE, 'same-course-reuse.mjs'), FC = join(HERE, 'fresh-check.mjs');
const FIX = join(HERE, 'fixtures', 'same-course-ae', 'content');
let fails = 0;
const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : `  ${String(detail).slice(0, 600)}`}`); if (!ok) fails++; };
const scan = (content, extra = ['--all']) => { const r = spawnSync('node', [SC, '--content', content, ...extra, '--json', '--no-waivers'], { encoding: 'utf8' }); try { return JSON.parse(r.stdout); } catch { check('the scan prints JSON', false, r.stdout + r.stderr); return []; } };
const hits = scan(FIX);
const has = (file, id, kind, src) => hits.some((h) => h.file === `courses/${file}.json` && h.itemId === id && h.kind === kind && (!src || src.test(h.source)));

// The eight true positives
check('1 function with its factorisation, variable renamed: analysis p-accumulated-cubic against l18', has('analysis/problems-5', 'p-accumulated-cubic', 'function', /analysis\/l18/), JSON.stringify(hits.filter((h) => h.itemId === 'p-accumulated-cubic')));
check('2 key pair 0.7 and 0.3: analysis p-diamond-ball against l23 "1 - 0.7 = 0.3"', has('analysis/problems-5', 'p-diamond-ball', 'pair', /analysis\/l23/));
check('3 function with its interval across courses: analysis p-root-sums against integrals l2 and review-1', has('analysis/problems-5', 'p-root-sums', 'function', /integrals\/l2/) && has('analysis/problems-5', 'p-root-sums', 'function', /integrals\/review-1/));
check('4 worked example shifted and scaled: odes p-test-rig against l15', has('odes/problems-4', 'p-test-rig', 'transform', /odes\/l15/));
check('5 circle with its integrand under another field: vector-calc p-bead-semicircle against review-1 r4-clockwise', has('vector-calc/problems-1', 'p-bead-semicircle', 'region', /vector-calc\/review-1/));
check('6 end points with a second route: vector-calc p-two-routes-cubic against homework-1 h1-two-paths', has('vector-calc/problems-1', 'p-two-routes-cubic', 'region', /vector-calc\/homework-1/));
check('7 a potential cut from a function of another course: vector-calc p-cubic-potential against multivar review-1', has('vector-calc/problems-1', 'p-cubic-potential', 'function', /multivar\/review-1/));
check('8 corners across courses and a plane\'s intercepts: vector-calc p-triangle-flux against multivar problems-5 and homework-3', has('vector-calc/problems-2', 'p-triangle-flux', 'region', /multivar\/problems-5/) && has('vector-calc/problems-2', 'p-triangle-flux', 'region', /vector-calc\/homework-3/));
check('every shape hit is an error (ENGINE-BACKLOG 1059), none a warning', hits.some((h) => ['function', 'pair', 'transform', 'region'].includes(h.kind)) && hits.filter((h) => ['function', 'pair', 'transform', 'region'].includes(h.kind)).every((h) => h.level === 'error'));

// The rulings that must not fire (DECISIONS sessions AC and AD)
const silent = (file, why) => { const h = hits.filter((x) => x.file === `courses/${file}.json`); check(`no hit: ${why}`, h.length === 0, JSON.stringify(h.map((x) => `${x.kind} ${x.evidence}`))); };
silent('frac/problems-1', 'a single common fraction (3/8) in a lesson and a problem of one course');
silent('quad-a/problems-1', 'a simple quadratic with small whole roots shared with a factorising screen of another topic');
silent('lin-a/problems-1', 'a taught definition or basis ((1, x, x^2, x^3), d-infinity)');
silent('eigen/problems-4', 'a two-state chain shared with another topic (eigen against markov)');
check('the same two-state chain in one course does fire (the pair kind is same-course)', (() => {
  const tmp = mkdtempSync(join(tmpdir(), 'zq-ae-'));
  try {
    const put = (rel, o) => { const p = join(tmp, rel); mkdirSync(dirname(p), { recursive: true }); writeFileSync(p, JSON.stringify(o)); };
    const num = (a) => ({ kind: 'numeric', answer: a, tol: { abs: 0.001 } });
    put('courses/markov/l2.json', { id: 'l2', screens: [{ type: 'ladder', title: 'Stay or go', prose: 'It fails with probability $r = 1 - 0.7 = 0.3$.', question: 'Failure probability?', widget: num(0.3), feedback: { correct: 'Yes.', generic: 'No.' } }] });
    put('courses/markov/problems-2.json', { id: 'problems-2', items: [{ id: 'p-a', prose: 'A machine keeps working with probability 0.7.', parts: [{ question: 'Keeps working?', widget: num(0.7), feedback: { correct: 'Yes.', generic: 'No.' } }, { question: 'Stops?', widget: num(0.3), feedback: { correct: 'Yes.', generic: 'No.' } }] }] });
    return scan(tmp).some((h) => h.kind === 'pair');
  } finally { rmSync(tmp, { recursive: true, force: true }); }
})());

// Number sets under x -> a x + b (kind c), and what stays silent
{
  const tmp = mkdtempSync(join(tmpdir(), 'zq-ae-'));
  try {
    const put = (rel, o) => { const p = join(tmp, rel); mkdirSync(dirname(p), { recursive: true }); writeFileSync(p, JSON.stringify(o)); };
    const num = (a) => ({ kind: 'numeric', answer: a, tol: { abs: 0.001 } });
    const fb = { correct: 'Yes.', generic: 'No.' };
    put('courses/stats/l1.json', { id: 'l1', screens: [{ type: 'ladder', title: 'A sample', prose: 'Six deliveries took 12, 15, 19, 24, 30 and 31 minutes. An arithmetic run is 2, 4, 6, 8, 10.', question: 'Median?', widget: num(21.5), feedback: fb }] });
    put('courses/stats/problems-1.json', { id: 'problems-1', items: [
      { id: 'p-shifted', prose: 'Six parcels took 40, 46, 54, 64, 76 and 78 minutes.', parts: [{ question: 'Median?', widget: num(59), feedback: fb }] },
      { id: 'p-progression', prose: 'Five sizes are 3, 6, 9, 12, 15.', parts: [{ question: 'Median?', widget: num(9), feedback: fb }] },
      { id: 'p-fresh', prose: 'Six waits were 13, 17, 18, 29, 33 and 47 minutes.', parts: [{ question: 'Median?', widget: num(23.5), feedback: fb }] }] });
    const h = scan(tmp);
    check('a number set shifted and scaled (x -> 2x + 16) is a transform hit', h.some((x) => x.itemId === 'p-shifted' && x.kind === 'transform'), JSON.stringify(h));
    check('an arithmetic progression and an unrelated set are silent', !h.some((x) => x.itemId === 'p-progression' || x.itemId === 'p-fresh'), JSON.stringify(h));
  } finally { rmSync(tmp, { recursive: true, force: true }); }
}

// Tightened rules R1 to R5 (ENGINE-BACKLOG 1053 to 1057) and the aM + bI matrix (1058): each class has a fixture that must stay silent and, where the rule keeps a true case, one that must fire
{
  const fb = { correct: 'Yes.', generic: 'No.' };
  const num = (a, extra = {}) => ({ kind: 'numeric', answer: a, tol: { abs: 0.001 }, ...extra });
  const run = (files) => {
    const tmp = mkdtempSync(join(tmpdir(), 'zq-ae-'));
    try {
      for (const [rel, o] of Object.entries(files)) { const p = join(tmp, rel); mkdirSync(dirname(p), { recursive: true }); writeFileSync(p, JSON.stringify(o)); }
      return scan(tmp);
    } finally { rmSync(tmp, { recursive: true, force: true }); }
  };
  const screen = (prose, widget = num(1)) => ({ type: 'ladder', title: 'A screen', prose, question: 'Value?', widget, feedback: fb });
  const set = (items) => ({ id: 'problems-1', items });
  const item = (id, prose, parts) => ({ id, prose, parts: parts.map((w) => ({ question: 'Value?', widget: w, feedback: fb })) });
  const list = (h, id) => JSON.stringify(h.filter((x) => x.itemId === id).map((x) => `${x.kind} ${x.evidence}`));
  const fires = (h, id, kind) => h.some((x) => x.itemId === id && x.kind === kind);

  // R1: a function under a fraction bar is keyed on the whole quotient
  let h = run({ 'courses/c/l1.json': { id: 'l1', screens: [screen('The integral $\\int_0^9 \\frac{1}{\\sqrt{x}}\\,dx$ is improper, and $\\int_0^4 \\frac{1}{\\sqrt{x}}\\,dx = 4$.')] },
    'courses/c/problems-1.json': set([item('p-root', 'A rate is $f(x) = \\sqrt{x}$ on $[0, 9]$.', [num(18)]), item('p-same', 'A rate is $f(x) = \\frac{1}{\\sqrt{x}}$ on $[0, 9]$.', [num(6)])]) });
  check('R1: sqrt(x) on [0, 9] against 1/sqrt(x) on [0, 9] is silent', !h.some((x) => x.itemId === 'p-root'), list(h, 'p-root'));
  check('R1: 1/sqrt(x) on [0, 9] against the same quotient still fires', fires(h, 'p-same', 'function'), JSON.stringify(h));

  // R2: no shape from a wrong entry or the feedback written for one
  h = run({ 'courses/c/l1.json': { id: 'l1', screens: [], quiz: [{ id: 'q1', prose: 'Factorise $x^2 - 1$.', question: 'Which?', widget: { kind: 'expression', answer: '(x-1)(x+1)', wrong: [{ id: 'slip', tex: '(x-1)(x+2)(x+3)' }], keyboard: 'algebra' }, feedback: { correct: 'Yes.', generic: 'No.', byKey: { slip: 'That is $x^3 + 4x^2 + x - 6$, not it.' } } }] },
    'courses/c/problems-1.json': set([item('p-slip', 'A crate has volume $V(x) = x^3 + 4x^2 + x - 6$ cubic metres.', [num(0)])]) });
  check('R2: a cubic that appears only in a wrong entry and its feedback is silent', !h.some((x) => x.itemId === 'p-slip'), list(h, 'p-slip'));
  h = run({ 'courses/c/l1.json': { id: 'l1', screens: [screen('Expand $(x - 1)(x + 2)(x + 3) = x^3 + 4x^2 + x - 6$.')] },
    'courses/c/problems-1.json': set([item('p-slip', 'A crate has volume $V(x) = x^3 + 4x^2 + x - 6$ cubic metres.', [num(0)])]) });
  check('R2: the same cubic in a lesson screen still fires', fires(h, 'p-slip', 'function'), JSON.stringify(h));

  // R3: a pair sentence holds no decimal but the two keys, and one of them is a key of the source unit
  h = run({ 'courses/c/l1.json': { id: 'l1', screens: [screen('Each minute it stays with 0.6, moves on with 0.3 and leaves with 0.1.', num(0.1)), screen('First-step analysis gives $h = 0.3 + 0.5h$, so $h = 0.6$.', num(0.6)), screen('The slopes give $r^2 = 2 \\times 0.3 = 0.6$.', num(2))] },
    'courses/c/problems-1.json': set([item('p-pair', 'A chain.', [num(0.6), num(0.3)])]) });
  check('R3: a row of chances, a sentence with a stock decimal, and a unit keyed on neither value are silent', !fires(h, 'p-pair', 'pair'), list(h, 'p-pair'));
  h = run({ 'courses/c/l1.json': { id: 'l1', screens: [screen('It fails with probability $r = 1 - 0.7 = 0.3$.', num(0.3))] },
    'courses/c/problems-1.json': set([item('p-pair', 'A machine works with chance 0.7.', [num(0.7), num(0.3)])]) });
  check('R3: two keys alone in a sentence, one a key of the source unit, still fires', fires(h, 'p-pair', 'pair'), JSON.stringify(h));

  // R4: a plane's intercepts projected on z = 0 run in the same course only; plain corner sets stay app-wide
  const corners = 'The corners of the triangle are (0, 0), (4, 0) and (0, 2).', plane = 'The plane meets the axes at the intercepts (4, 0, 0), (0, 2, 0) and (0, 0, 4).';
  h = run({ 'courses/a/problems-1.json': set([item('p-tri', corners, [num(4)])]), 'courses/b/homework-1.json': { id: 'homework-1', items: [item('h-plane', plane, [num(1)])] } });
  check('R4: corners against a plane\'s intercepts of another course are silent', !h.some((x) => x.itemId === 'p-tri'), list(h, 'p-tri'));
  h = run({ 'courses/a/problems-1.json': set([item('p-tri', corners, [num(4)])]), 'courses/b/homework-1.json': { id: 'homework-1', items: [item('h-tri', corners, [num(1)])] } });
  check('R4: the same plain corners in another course still fire', fires(h, 'p-tri', 'region'), JSON.stringify(h));
  h = run({ 'courses/a/problems-1.json': set([item('p-tri', corners, [num(4)])]), 'courses/a/homework-1.json': { id: 'homework-1', items: [item('h-plane', plane, [num(1)])] } });
  check('R4: corners against a plane\'s intercepts of the same course still fire', fires(h, 'p-tri', 'region'), JSON.stringify(h));

  // R5: the interval's named variable must occur in the function; a level set keeps its right-hand side
  h = run({ 'courses/c/l1.json': { id: 'l1', screens: [screen('The cylinder $x^2 + y^2 = 4$ stands on $0 \\le z \\le 2$.'), screen('The radius satisfies $x^2 + y^2 = 4$ on $[0, 2]$.')] },
    'courses/c/problems-1.json': set([item('p-cyl', 'Integrate $x^2 + y^2$ for $0 \\le x \\le 2$.', [num(8)]), item('p-cyl2', 'Integrate $f(x, y) = x^2 + y^2$ on $[0, 2]$.', [num(8)])]) });
  check('R5: x^2 + y^2 against a cylinder with 0 <= z <= 2, and a level set with its right-hand side, are silent', !h.some((x) => ['p-cyl', 'p-cyl2'].includes(x.itemId)), list(h, 'p-cyl') + list(h, 'p-cyl2'));
  h = run({ 'courses/c/l1.json': { id: 'l1', screens: [screen('The potential is $x^2 + y^2$ for $0 \\le x \\le 2$.')] },
    'courses/c/problems-1.json': set([item('p-cyl', 'Integrate $x^2 + y^2$ for $0 \\le x \\le 2$.', [num(8)])]) });
  check('R5: the same function over an interval of its own variable still fires', fires(h, 'p-cyl', 'function'), JSON.stringify(h));

  // the cubic reflected (x -> -x) is a transform hit; it is how the pre-fix quadratics crate meets the review's cubic
  h = run({ 'courses/c/l1.json': { id: 'l1', screens: [screen('Factorise $x^3 - 4x^2 + x + 6$ fully.')] }, 'courses/c/problems-1.json': set([item('p-refl', 'A crate has $V(x) = x^3 + 4x^2 + x - 6$.', [num(0)])]) });
  check('a cubic reflected (x -> -x) is a transform hit', fires(h, 'p-refl', 'transform'), JSON.stringify(h));

  // aM + bI: a symmetric 2 by 2 matrix equal to another after a M + b I has its eigenvectors
  const mat = (a, b, d) => `$\\begin{pmatrix}${a}&${b}\\\\${b}&${d}\\end{pmatrix}$`;
  h = run({ 'courses/e/l5.json': { id: 'l5', screens: [screen(`The covariance is ${mat('1.1', '0.3', '1.9')}.`)] }, 'courses/e/problems-1.json': set([item('p-shift', `A pond has ${mat(9, 3, 17)}.`, [num(8)]), item('p-stock', `A pond has ${mat(5, 4, 5)}.`, [num(9)]), item('p-other', `A pond has ${mat(9, 3, 11)}.`, [num(2)])]) });
  check('aM + bI: [[9, 3], [3, 17]] against [[1.1, 0.3], [0.3, 1.9]] (10M - 2I) is a matrix error', h.some((x) => x.itemId === 'p-shift' && x.kind === 'matrix' && x.level === 'error' && /aM \+ bI/.test(x.evidence)), JSON.stringify(h));
  check('aM + bI: a matrix with equal diagonal (stock eigenvectors) and one with other eigenvectors are silent', !h.some((x) => ['p-stock', 'p-other'].includes(x.itemId)), list(h, 'p-stock') + list(h, 'p-other'));
}

// The same lines through fresh-check.mjs --file (the author-facing command) and the opt-out
{
  const r = spawnSync('node', [FC, '--content', FIX, '--file', join(FIX, 'courses', 'vector-calc', 'problems-2.json')], { encoding: 'utf8' });
  check('fresh-check.mjs --file prints the region hit of p-triangle-flux as an error and exits 1', r.status === 1 && /\[same-course-reuse\] error .*p-triangle-flux.*region.*multivar\/problems-5/.test(r.stdout), r.stdout + r.stderr);
  const r2 = spawnSync('node', [SC, '--content', FIX, '--all', '--no-shapes'], { encoding: 'utf8' });
  check('--no-shapes drops the four shape kinds', !/ (?:function|pair|transform|region) {2}<-/.test(r2.stdout), r2.stdout);
}
console.log(fails ? `${fails} check(s) failed` : 'all checks passed');
process.exit(fails ? 1 : 0);
