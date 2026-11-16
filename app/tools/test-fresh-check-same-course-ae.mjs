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
check('every shape hit is advisory (warn), never an error', hits.filter((h) => ['function', 'pair', 'transform', 'region'].includes(h.kind)).every((h) => h.level === 'warn'));

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

// The same lines through fresh-check.mjs --file (the author-facing command) and the opt-out
{
  const r = spawnSync('node', [FC, '--content', FIX, '--file', join(FIX, 'courses', 'vector-calc', 'problems-2.json')], { encoding: 'utf8' });
  check('fresh-check.mjs --file prints the region hit of p-triangle-flux and exits 0 (advisory)', r.status === 0 && /\[same-course-reuse\] warn .*p-triangle-flux.*region.*multivar\/problems-5/.test(r.stdout), r.stdout + r.stderr);
  const r2 = spawnSync('node', [SC, '--content', FIX, '--all', '--no-shapes'], { encoding: 'utf8' });
  check('--no-shapes drops the four new kinds', !/ (?:function|pair|transform|region) {2}<-/.test(r2.stdout), r2.stdout);
}
console.log(fails ? `${fails} check(s) failed` : 'all checks passed');
process.exit(fails ? 1 : 0);
