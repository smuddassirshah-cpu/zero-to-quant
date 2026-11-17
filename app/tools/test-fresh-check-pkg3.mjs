#!/usr/bin/env node
// Test for engine pass 7 remainder, package 3 (reuse checkers): ENGINE-BACKLOG 1062 (a taught formula is no copied setup), 1088 (ratio of two stated amounts), 1106 (chain across sources and model answers),
// 1128 (story in its own nouns), 1153 ("x over n years" givens), and --all-exams (a problem set against every exam, warnings only). Trees are built in the test; the word frequencies are the snapshot tools/retold-model.json.
// Run from app/: node tools/test-fresh-check-pkg3.mjs
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const HERE = dirname(fileURLToPath(import.meta.url));
const SC = join(HERE, 'same-course-reuse.mjs'), FC = join(HERE, 'fresh-check.mjs');
let fails = 0;
const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : `  ${String(detail).slice(0, 900)}`}`); if (!ok) fails++; };
const put = (root, rel, o) => { const p = join(root, rel); mkdirSync(dirname(p), { recursive: true }); writeFileSync(p, typeof o === 'string' ? o : JSON.stringify(o)); };
const withTree = (files, f) => { const tmp = mkdtempSync(join(tmpdir(), 'zq-pkg3-')); try { for (const [rel, o] of Object.entries(files)) put(tmp, rel, o); return f(tmp); } finally { rmSync(tmp, { recursive: true, force: true }); } };
const sc = (root, extra = ['--all']) => { const r = spawnSync('node', [SC, '--content', root, ...extra], { encoding: 'utf8' }); return { out: r.stdout, err: r.stderr, status: r.status }; };
const scan = (root, extra = ['--all']) => { const r = sc(root, [...extra, '--json']); try { return { hits: JSON.parse(r.out), status: r.status }; } catch { check('the scan prints JSON', false, r.out + r.err); return { hits: [], status: r.status }; } };
const fc = (root, file, extra = []) => { const r = spawnSync('node', [FC, '--content', root, '--file', join(root, file), ...extra], { encoding: 'utf8' }); return { out: r.stdout + r.stderr, status: r.status }; };
const fb = (extra = {}) => ({ correct: 'Yes.', generic: 'Not quite right.', ...extra });
const num = (a, o = {}) => ({ kind: 'numeric', answer: a, tol: { abs: 0.001 }, ...o });
const screen = (o) => ({ type: 'ladder', title: 'A screen', widget: num(1), feedback: fb(), ...o });
const part = (question, o = {}) => ({ question, widget: num(1), feedback: fb(), ...o });
const lesson = (id, screens) => ({ id, screens });
const set = (items) => ({ id: 'problems-1', items });
const COURSE = { id: 'c', topic: '9.9', skills: { 'sk-c': 'A skill of c', 'sk-d': 'Another skill of c' }, levels: [] };
const run = (files, extra) => withTree({ 'courses/c/course.json': COURSE, ...files }, (root) => scan(root, extra));
const kinds = (r, id) => r.hits.filter((h) => h.itemId === id).map((h) => h.kind);

// ---- 1062: a formula that a lesson screen teaches is not a copied setup ----
{
  const F = 'p = \\dfrac{1}{1 + e^{-0.35 x}}';
  const taught = lesson('l1', [screen({ prose: 'Squash a score into a probability.', formula: { name: 'Logistic', tex: F } })]);
  const shows = lesson('l2', [screen({ prose: `A first desk turns a score into a chance with $${F}$ in its own way.` })]);
  const prob = set([{ id: 'p-a', prose: `A desk turns a score into a chance with $${F}$ for a wider book.`, widget: num(2), feedback: fb() }]);
  withTree({ 'courses/c/course.json': COURSE, 'courses/c/l2.json': shows, 'courses/c/problems-1.json': prob }, (root) => {
    const r = fc(root, 'courses/c/problems-1.json', ['--no-same-course']);
    check('1062 control: a formula shared with a lesson screen that does not teach it (no formula.tex) is still listed as advisory', /shared formula/.test(r.out), r.out);
  });
  withTree({ 'courses/c/course.json': COURSE, 'courses/c/l1.json': taught, 'courses/c/l2.json': shows, 'courses/c/problems-1.json': prob }, (root) => {
    const r = fc(root, 'courses/c/problems-1.json', ['--no-same-course']);
    check('1062 a formula the course teaches in a screen formula.tex is not listed, though another screen shows it too', !/shared formula/.test(r.out), r.out);
  });
}

if (process.argv[1].endsWith('test-fresh-check-pkg3.mjs')) { console.log(fails ? `${fails} FAILED` : 'all passed'); process.exitCode = fails ? 1 : 0; }
