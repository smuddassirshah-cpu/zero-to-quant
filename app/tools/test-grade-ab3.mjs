#!/usr/bin/env node
/* Engine pass AB part 3 (ENGINE-BACKLOG 931 to 939): grader faults found by second readers, tested in the real grade.js with the local
   Compute Engine, no browser.
     Part 1 (931): a vector or matrix typed in any documented form ([[a, b], [c, d]], ((a, b), (c, d)), pmatrix, MathLive spellings)
                   reaches its `wrong` line, and has a shape, as the key does.
     Part 2 (932): a number times a vector or matrix, and factored entries, are read.
     Part 3 (933): a unit in words or with a caret after the number.
     Part 4 (934, 937): a leading plus sign and a `\ell(\lambda) =` style label.
     Part 5 (935): form "simplified" is the same verdict for 3(x-4) and 2(4x-13).
   Usage: node tools/test-grade-ab3.mjs [--local-cdn <pkgs>]   Exit 0 pass, 1 failure, 2 setup problem. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');
const argv = process.argv.slice(2);
const arg = (k) => { const i = argv.indexOf(k); return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? path.resolve(argv[i + 1]) : null; };
const cdn = arg('--local-cdn') || (process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null);
const ceFile = cdn && path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
if (!ceFile || !fs.existsSync(ceFile)) { console.error('test-grade-ab3: give --local-cdn <pkgs> (or ZQ_LOCAL_CDN)'); process.exit(2); }
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = {};
vm.runInContext(fs.readFileSync(path.join(APP, 'js/engine/grade.js'), 'utf8'), g);
const G = g.ZQ.grade;
const fails = []; let n = 0;
const check = (name, ok, detail = '') => { n++; if (!ok) { fails.push(name); console.log(`FAIL ${name}  ${detail}`); } };
const ex = (spec, t) => G.exprGrade(ce, { kind: 'expression', ...spec }, t, t);
const nv = (spec, t) => G.numGrade({ kind: 'numeric', ...spec }, t);
const lb = '\\left\\lbrack', rb = '\\right\\rbrack';
/* every typing form of a matrix given as rows of strings */
const forms = (rows) => ({
  asked: `[[${rows.map(r => r.join(', ')).join('], [')}]]`,
  tight: `[[${rows.map(r => r.join(',')).join('],[')}]]`,
  mathlive: `${lb}${rows.map(r => `${lb}${r.join(',')}${rb}`).join(',')}${rb}`,
  round: `((${rows.map(r => r.join(', ')).join('), (')}))`,
  pmatrix: `\\begin{pmatrix}${rows.map(r => r.join('&')).join('\\\\')}\\end{pmatrix}`,
  brace: `\\left(\\left(${rows.map(r => r.join(',')).join('\\right),\\left(')}\\right)\\right)`,
});

/* ---------- Part 1 (931): a wrong matrix in any typing form reaches its wrong line ---------- */
const mat = {
  answer: '\\begin{pmatrix}1&0.25\\\\0&1\\end{pmatrix}', accept: ['[[1, 0.25], [0, 1]]'],
  wrong: [{ id: 'rows', tex: '\\begin{pmatrix}1&0\\\\0.25&1\\end{pmatrix}' }, { id: 'order', tex: '[[1.5, 0.25], [0, 1]]' }],
};
for (const [name, t] of Object.entries(forms([['1', '0'], ['0.25', '1']]))) check(`931 wrong matrix (${name}) lands on its key`, ex(mat, t).key === 'rows', JSON.stringify(ex(mat, t)));
for (const [name, t] of Object.entries(forms([['1', '0.25'], ['0', '1']]))) check(`931 right matrix (${name}) is accepted`, ex(mat, t).ok === true, JSON.stringify(ex(mat, t)));
for (const [name, t] of Object.entries(forms([['1.5', '0.25'], ['0', '1']]))) check(`931 wrong matrix stored in the asked form (${name}) lands on its key`, ex(mat, t).key === 'order', JSON.stringify(ex(mat, t)));
check('931 an unnamed wrong 2x2 matrix is not told it is a single value', !/single value/.test(ex(mat, '[[4, -1], [-2, 3]]').line || '') && ex(mat, '[[4, -1], [-2, 3]]').key == null, JSON.stringify(ex(mat, '[[4, -1], [-2, 3]]')));
check('931 a matrix of the wrong shape still gets the length line, in any form', ex(mat, '[[1, 2, 3], [4, 5, 6]]').key === 'length' && /2 rows and 3 columns/.test(ex(mat, '[[1, 2, 3], [4, 5, 6]]').line) && ex(mat, '[[1, 2]]').key === 'length' && ex(mat, '(3, 4)').key === 'length' && ex(mat, '5').key === 'length');
check('931 a bracketed row of numbers is still a vector', ex({ answer: '(3, 4)' }, '[3, 4]').ok && ex({ answer: '[3, 4]' }, '\\begin{pmatrix}3\\\\4\\end{pmatrix}').ok && ex({ answer: '(3, 4)' }, '[4, 3]').ok === false);
const sym = { answer: '\\begin{pmatrix}2k+6&k+2\\\\5&2\\end{pmatrix}', wrong: [{ id: 'order', tex: '[[7, 3k+1], [5, 2k+1]]' }] };
check('931 a matrix in k typed as asked: right, wrong line', ex(sym, '[[2k+6, k+2], [5, 2]]').ok && ex(sym, '[[7, 3k+1], [5, 2k+1]]').key === 'order' && ex(sym, '\\begin{pmatrix}7&3k+1\\\\5&2k+1\\end{pmatrix}').key === 'order');
const vec = { answer: '(3, 4)', wrong: [{ id: 'swap', tex: '(4, 3)' }, { id: 'neg', tex: '\\begin{pmatrix}-3\\\\-4\\end{pmatrix}' }] };
check('931 vectors in every form land on wrong keys', ['(4, 3)', '[4, 3]', '\\langle 4, 3\\rangle', '\\begin{pmatrix}4\\\\3\\end{pmatrix}', '4, 3'].every(t => ex(vec, t).key === 'swap') && ['(-3, -4)', '[-3,-4]', '\\begin{pmatrix}-3&-4\\end{pmatrix}'].every(t => ex(vec, t).key === 'neg'));
const m3 = { answer: '[[1, 2], [3, 4]]', wrong: [{ id: 'tr', tex: '[[1, 3], [2, 4]]' }] };
check('931 answer stored as a bracket matrix: pmatrix typed, wrong from a pmatrix', ex(m3, '\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}').ok && ex(m3, '\\begin{pmatrix}1&3\\\\2&4\\end{pmatrix}').key === 'tr' && ex(m3, '((1, 3), (2, 4))').key === 'tr');

/* ---------- Part 2 (932): a number times a vector or matrix; factored entries ---------- */
const eng = { answer: '\\begin{pmatrix}2k+6&k+2\\\\5&2\\end{pmatrix}', wrong: [{ id: 'order', tex: '[[7, 3k+1], [5, 2k+1]]' }] };
for (const t of ['[[2(k+3), k+2], [5, 2]]', '[[2(3+k), 2+k], [5, 2]]', '[[6+k\\cdot2, 2+k], [5, 2]]', '\\begin{pmatrix}2(k+3)&k+2\\\\5&2\\end{pmatrix}']) check(`932 factored entries: ${t}`, ex(eng, t).ok === true, JSON.stringify(ex(eng, t)));
const inv = { answer: '[[0.3, -0.1], [-0.2, 0.4]]', wrong: [{ id: 'no-divide', tex: '[[3, -1], [-2, 4]]' }] };
for (const t of ['\\frac{1}{10}[[3, -1], [-2, 4]]', '0.1[[3,-1],[-2,4]]', '\\frac{1}{10}\\begin{pmatrix}3&-1\\\\-2&4\\end{pmatrix}', '\\frac{1}{10}\\left(\\begin{matrix}3&-1\\\\-2&4\\end{matrix}\\right)', '[[3, -1], [-2, 4]]/10', '\\frac{[[3, -1], [-2, 4]]}{10}']) check(`932 number times matrix: ${t}`, ex(inv, t).ok === true, JSON.stringify(ex(inv, t)));
check('932 a number times a wrong matrix still reaches its line; a wrong factor is refused', ex(inv, '1[[3, -1], [-2, 4]]').key === 'no-divide' && ex(inv, '\\frac{1}{5}[[3, -1], [-2, 4]]').ok === false);
const dv = { answer: '(0.6, 0.8)', wrong: [{ id: 'raw', tex: '(3, 4)' }] };
for (const t of ['\\frac{1}{5}(3,4)', '\\frac{1}{5}\\begin{pmatrix}3\\\\4\\end{pmatrix}', '0.2(3, 4)', '(3, 4)/5', '\\frac{(3,4)}{5}', '\\frac{1}{5}\\langle 3, 4\\rangle']) check(`932 number times vector: ${t}`, ex(dv, t).ok === true, JSON.stringify(ex(dv, t)));
check('932 a number times a vector of the wrong length is a length key', ex(dv, '\\frac{1}{5}(3,4,0)').key === 'length' && ex(dv, '2(3, 4)').ok === false);

/* ---------- Part 3 (933): a unit in words or with a caret after the number ---------- */
const area = { answer: 234, tol: { abs: 0 }, unit: 'm²' };
for (const t of ['234', '234 m²', '234 m^2', '234m^2', '234 m^{2}', '234 m2', '234 square metres', '234 square meters', '234 sq m', '234 metres squared', '234 sq. m', '234 SQUARE METRES', 'A = 234 m^2', '234 m^2.']) check(`933 area: ${t}`, nv(area, t).ok === true, JSON.stringify(nv(area, t)));
const kmh = { answer: 20, tol: { abs: 0 }, unit: 'km/h' };
for (const t of ['20 km/h', '20 km an hour', '20 km per hour', '20 kilometres per hour', '20 kph', '20 km/hr', '20 km a hour']) check(`933 speed: ${t}`, nv(kmh, t).ok === true, JSON.stringify(nv(kmh, t)));
check('933 a wrong value with a unit in words still routes', nv({ ...kmh, wrong: [{ id: 'w', value: 25 }] }, '25 km an hour').key === 'w' && nv(kmh, '25 km an hour').ok === false);
const perDay = { answer: 0.4, tol: { abs: 0 }, unit: 'per day' };
for (const t of ['0.4', '0.4 per day', '0.4 a day', '0.4 per day.']) check(`933 rate: ${t}`, nv(perDay, t).ok === true, JSON.stringify(nv(perDay, t)));
check('933 words after a number: GWh per °C, a year, a month, percentage points, a million', nv({ answer: -12, tol: { abs: 0 }, unit: 'GWh per °C' }, '-12 GWh per °C').ok && nv({ answer: -1480, tol: { abs: 0 }, unit: '£' }, '-£1,480 a year').ok && nv({ answer: 0.0035, tol: { abs: 1e-9 }, unit: '%' }, '0.35% a month').ok && nv({ answer: 0.0196, tol: { abs: 1e-9 }, unit: '%' }, '1.96 percentage points').ok && nv({ answer: 21, tol: { abs: 0 }, unit: 'million shares' }, '21 million shares').ok);
check('933 own unit written another way: 7 h for hours, 5 mins for minutes, 3 metres for m', nv({ answer: 7, tol: { abs: 0 }, unit: 'hours' }, '7 h').ok && nv({ answer: 5, tol: { abs: 0 }, unit: 'minutes' }, '5 mins').ok && nv({ answer: 3, tol: { abs: 0 }, unit: 'm' }, '3 metres').ok && nv({ answer: 3, tol: { abs: 0 }, unit: 'm' }, '3 m').ok);
check('933 3x is not 3; 1e-5, 1 1/2 and 3/4 still read', G.numValue('3x', {}) !== 3 && Math.abs(G.numValue('4.86e-5', {}) - 4.86e-5) < 1e-15 && G.numValue('1 1/2', {}) === 1.5 && G.numValue('3/4', {}) === 0.75 && G.numValue('2 e', { unit: 'm' }) !== 2);

/* ---------- Part 4 (934): a leading plus sign and an \ell(\lambda) = label ---------- */
const plus = { answer: 42, tol: { abs: 0 } };
for (const t of ['+42', '+ 42', '+42.0', '+42 cm', '42']) check(`934 plus: ${t}`, nv(plus, t).ok === true, JSON.stringify(nv(plus, t)));
check('934 plus: money and per cent', nv({ answer: 250, tol: { abs: 0 }, unit: '£' }, '+£250').ok && nv({ answer: 250, tol: { abs: 0 }, unit: '£' }, '£+250').ok && nv({ answer: 0.02, tol: { abs: 1e-9 }, unit: '%' }, '+2%').ok && nv({ answer: 0.02, tol: { abs: 1e-9 }, unit: '%' }, '+2').ok && nv({ answer: -3, tol: { abs: 0 } }, '+3').ok === false && nv({ answer: -3, tol: { abs: 0 }, wrong: [{ id: 'sign', value: 3 }] }, '+3').key === 'sign');
const ll = { answer: '-\\lambda+5\\ln\\lambda' };
for (const t of ['-\\lambda+5\\ln\\lambda', '\\ell(\\lambda)=-\\lambda+5\\ln\\lambda', '\\ell(\\lambda) = -\\lambda+5\\ln\\lambda', '\\ell = -\\lambda+5\\ln\\lambda', 'l(\\lambda)=-\\lambda+5\\ln\\lambda', 'L(\\lambda)=-\\lambda+5\\ln\\lambda', '\\mathcal{L}(\\lambda)=-\\lambda+5\\ln\\lambda', '\\ell(\\lambda)=5\\ln\\lambda-\\lambda']) check(`934 label: ${t}`, ex(ll, t).ok === true, JSON.stringify(ex(ll, t)));
check('934 label: a wrong expression after the label is still wrong, and a call of the answer\'s own letters is not a label', ex(ll, '\\ell(\\lambda)=-\\lambda+4\\ln\\lambda').ok === false && ex({ answer: '5' }, 'x(x+1)=5').ok === false);

/* ---------- Part 5 (935): form "simplified" gives one verdict for a number times a bracket ---------- */
const sf = (spec, t) => ex({ form: 'simplified', ...spec }, t);
const e1 = { answer: '3x-12' }, e2 = { answer: '8x-26' }, e3 = { answer: '6t-9' };
for (const [spec, t] of [[e1, '3(x-4)'], [e2, '2(4x-13)'], [e3, '3(2t-3)'], [{ answer: '8y-24' }, '8(y-3)'], [e1, '-3(4-x)'], [e1, '\\frac{3(x-4)}{1}'], [e2, '0.5(16x-52)']]) check(`935 simplified refuses an unopened bracket: ${t}`, sf(spec, t).ok === false && sf(spec, t).key === 'form', JSON.stringify(sf(spec, t)));
for (const [spec, t] of [[e1, '3x-12'], [e1, '-12+3x'], [e2, '8x-26'], [e3, '6t-9'], [e1, '3x - 12'], [{ answer: '2x+6', accept: ['2(x+3)'] }, '2(x+3)'], [{ answer: '5n-100', accept: ['5(n-20)'] }, '5(n-20)'], [{ answer: '\\frac{x+1}{2}' }, '\\frac{1}{2}(x+1)']]) check(`935 simplified passes: ${t}`, sf(spec, t).ok === true, JSON.stringify(sf(spec, t)));

console.log(`test-grade-ab3: ${n - fails.length}/${n} passed${fails.length ? ', ' + fails.length + ' FAILED' : ''}`);
process.exit(fails.length ? 1 : 0);
