#!/usr/bin/env node
// Test for fresh-check.mjs (ENGINE-BACKLOG 588): synthetic fixtures in a temporary content folder.
// Run from app/: node tools/test-fresh-check.mjs
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const TOOL = join(dirname(fileURLToPath(import.meta.url)), 'fresh-check.mjs');
const root = mkdtempSync(join(tmpdir(), 'fresh-check-'));
const put = (rel, obj) => { const p = join(root, rel); mkdirSync(dirname(p), { recursive: true }); writeFileSync(p, JSON.stringify(obj)); };
const num = (n) => ({ kind: 'numeric', answer: n, tol: { abs: 0.01 } });

const setup = (n, p) => `A trader holds a portfolio of ${n} shares. Each day the price moves up by one pound with probability ${p} and down by one pound otherwise. The moves are independent across days.`;
put('courses/c1/l1.json', { id: 'l1', screens: [
  { type: 'ladder', title: 'Walk', prose: setup(10, '0.6'), question: 'What is the expected price change after 5 days?', widget: num(1) },
  { type: 'ladder', title: 'Stock', prose: 'Drift is the average daily move. Which of the following is true? Pick the statement about drift.', question: 'Which of the following is true?', widget: num(1) }] });
put('courses/c1/course.json', { id: 'c1' });
// Exam A copies the walk setup with changed constants. Exam B shares only stock phrasing. Exam C is unrelated.
put('exams/a.json', { id: 'a', items: [{ id: 'x', prose: setup(12, '0.7'), question: 'What is the expected price change after 8 days?', widget: num(3) }] });
put('exams/b.json', { id: 'b', items: [{ id: 'y', prose: 'Which of the following is true?', question: 'Which of the following is true? Choose the claim about variance.', widget: num(1) }] });
put('exams/c.json', { id: 'c', items: [{ id: 'z', prose: 'A bag holds red and blue marbles in the ratio three to five.', question: 'What fraction of the marbles are blue?', widget: num(0.625) }] });

let fails = 0;
const run = (args) => spawnSync('node', [TOOL, '--content', root, ...args], { encoding: 'utf8' });
const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : ` ${detail}`}`); if (!ok) fails++; };

let r = run(['--exam', 'a']);
check('copied setup with changed constants hits (exit 1)', r.status === 1 && /exams\/a\.json:items\[0\]\s+<-\s+courses\/c1\/l1\.json:screens\[0\]/.test(r.stdout), r.stdout);
check("hit reports run length and share", /run (\d+), share [01](?:\.\d+)?/.test(r.stdout) && Number(r.stdout.match(/run (\d+)/)[1]) >= 8, r.stdout);
check('--min-run above the shared run clears the hit', run(['--exam', 'a', '--min-run', '60']).status === 0);
check('--min-share above the share clears the hit', run(['--exam', 'a', '--min-share', '1.01']).status === 0);
const jh = JSON.parse(run(['--exam', 'a', '--json']).stdout)[0];
check('json carries run, share and the run text', jh.run >= 8 && jh.share > 0 && jh.share <= 1 && jh.ngram.split(' ').length === Math.min(jh.run, 30), JSON.stringify(jh));
r = run(['--exam', 'b']);
check('shared stock phrase does not hit (exit 0)', r.status === 0, r.stdout);
r = run(['--exam', 'c']);
check('unrelated exam is clean', r.status === 0, r.stdout);
r = run(['--all-exams', '--json']);
const hits = JSON.parse(r.stdout);
check('--all-exams --json lists only exam a', r.status === 1 && hits.length > 0 && hits.every((h) => h.target.startsWith('exams/a.json')), r.stdout);
put('exams/d.json', { id: 'd', items: [{ id: 'w', prose: setup(20, '0.55'), question: 'What is the variance of the price change after 3 days?', widget: num(3) }] });
r = run(['--exam', 'a']);
check('a second exam copying the setup is reported against the first', /exams\/d\.json/.test(r.stdout), r.stdout);
r = run(['--exam', 'nope']);
check('unknown exam exits 2', r.status === 2, String(r.status));

// Session V (600): word-token runs, stop list, code names.
const stock = 'Put the steps in order. Leave out the two that do not belong. Give four decimal places. Select all that apply.';
put('courses/c1/l2.json', { id: 'l2', screens: [{ type: 'ladder', title: 'Steps', prose: `${stock} Alpha beta gamma delta.`, question: stock, widget: num(1) }] });
put('exams/e.json', { id: 'e', items: [{ id: 'e1', prose: `${stock} Epsilon zeta eta theta.`, question: stock, widget: num(1) }] });
r = run(['--exam', 'e', '--min-run', '4', '--min-share', '0']);
check('stop-list instruction sentences do not hit', r.status === 0, r.stdout);
put('courses/c1/l3.json', { id: 'l3', screens: [{ type: 'ladder', title: 'M', prose: 'Maths.', question: 'Evaluate $\\frac{\\alpha_{1} + \\beta_{2}}{\\gamma^{3}} = \\sum_{k=1}^{n} \\frac{x_k}{y_k}$ for $x = 4$ and $y = 7$.', widget: num(1) }] });
put('exams/f.json', { id: 'f', items: [{ id: 'f1', prose: 'Skeleton.', question: 'Evaluate $\\frac{\\alpha_{2} + \\beta_{5}}{\\gamma^{9}} = \\sum_{k=1}^{m} \\frac{p_k}{q_k}$ for $x = 8$ and $y = 3$.', widget: num(1) }] });
r = run(['--exam', 'f', '--min-run', '3', '--min-share', '0']);
check('a LaTeX skeleton with few words does not hit', r.status === 0, r.stdout);
const codeW = (fn) => ({ kind: 'code', language: 'python', starter: `def ${fn}(xs):\n    pass\n`, solution: `def ${fn}(xs):\n    return sum(xs)\n`, tests: [{ call: `${fn}([1, 2])`, expect: '3' }] });
put('courses/c1/l4.json', { id: 'l4', screens: [{ type: 'code', title: 'Walk', prose: 'Write it.', widget: codeW('walk_forward_mse') }] });
put('exams/g.json', { id: 'g', items: [{ id: 'g1', prose: 'A different story about forecasts.', widget: codeW('walk_forward_mse') }] });
put('exams/h.json', { id: 'h', items: [{ id: 'h1', prose: 'Another story.', widget: codeW('total_of_things') }] });
r = run(['--exam', 'g']);
check('a reused code function name hits', r.status === 1 && /code names walk_forward_mse/.test(r.stdout), r.stdout);
check('a fresh code function name is clean', run(['--exam', 'h']).status === 0);
check('--no-code switches the code names off', run(['--exam', 'g', '--no-code']).status === 0);
for (const k of ['c5', 'c6', 'c1']) put(`courses/${k}/l9.json`, { id: `${k}-l9`, screens: [{ type: 'code', title: 'X', prose: 'Write it.', widget: codeW('shared_helper') }] });
put('exams/i.json', { id: 'i', items: [{ id: 'i1', prose: 'Idiom.', widget: codeW('shared_helper') }] });
r = run(['--exam', 'i']);
check('a name used in three courses is an idiom, not a hit', r.status === 0, r.stdout);

// Session V pass 7 (604): a course review or homework set inside content/, code items included.
put('courses/c1/review-1.json', { id: 'review-1', items: [{ id: 'r1', prose: 'A different story about forecasts.', widget: codeW('walk_forward_mse') }, { id: 'r2', prose: setup(14, '0.65'), question: 'What is the expected price change after 9 days?', widget: num(3) }] });
r = run(['--file', join(root, 'courses/c1/review-1.json')]);
check('a course review set runs (no ENOENT), reports code name and prose reuse, never itself', r.status === 1 && /code names walk_forward_mse/.test(r.stdout) && /courses\/c1\/review-1\.json:items\[1\]\s+<-\s+courses\/c1\/l1\.json/.test(r.stdout) && !/<-\s+courses\/c1\/review-1/.test(r.stdout), r.stdout + r.stderr);
put('courses/c1/l7.json', { id: 'l7', screens: [{ type: 'ladder', title: 'Seed', prose: 'A fund starts with 8431.75 pounds, earns 17.32 in fees and pays 905.5 to its manager.', question: 'What remains?', widget: num(1) }] });
put('courses/c1/review-2.json', { id: 'review-2', items: [{ id: 'q', prose: 'Dealer A quotes 905.5 for a block, a fee of 17.32 applies, and the balance was 8431.75.', question: 'Net?', widget: num(1) }] });
r = run(['--file', join(root, 'courses/c1/review-2.json'), '--no-code']);
check('three shared non-trivial numbers with a lesson screen: advisory line, exit 0 (614)', r.status === 0 && /3 shared numbers/.test(r.stdout) && /1 advisory/.test(r.stdout), r.stdout);
check('--shared-numbers 0 switches it off', !/shared numbers \(/.test(run(['--file', join(root, 'courses/c1/review-2.json'), '--no-code', '--shared-numbers', '0']).stdout));

// ENGINE-BACKLOG 893: a problem-set item that shares a displayed formula, or two stated parameters, with a lesson, quiz, review, homework or exam of its
// course. The first four are the pre-fix texts of reuses the second readers found by hand (docs/reviews/review-problems-1.3-a, -1.3-b, -0.2-a), each
// against the unit of the course it repeated; the tool found none of them before.
const sc = (id, prose, q) => ({ id, prose, question: q, widget: num(1) });
put('courses/s1/course.json', { id: 's1' });
put('courses/s1/homework-1.json', { id: 'homework-1', items: [sc('h-derive-falling-area', 'Take the falling curve $f(x) = 9 - x^2$ on $[1, 3]$ and split the interval into strips of equal width.', 'What is the area?')] });
put('courses/s1/review-3.json', { id: 'review-3', items: [sc('r-log-return-product', 'A price follows $P(t) = 40e^{0.06t}(1 + 0.02t)$ and the desk tracks its growth.', 'What is the rate of growth?')] });
put('courses/s1/l1-tangent.json', { id: 'l1', screens: [{ type: 'ladder', title: 'T', prose: 'Tangent lines.', question: 'The cube root $f(x) = x^{1/3}$ has $f(8) = 2$ and $f\'(x) = \\tfrac13 x^{-2/3}$. Estimate the root of 8.06.', widget: num(2) }], quiz: [] });
put('courses/s1/l9-lines.json', { id: 'l9', screens: [{ type: 'ladder', title: 'L', prose: 'A pipe follows $y = 0.5x + 2$ and another pipe is parallel to it.', question: 'What is the gradient?', widget: num(0.5) }], quiz: [] });
put('courses/s1/l2-vols.json', { id: 'l2', screens: [{ type: 'ladder', title: 'V', prose: 'Asset A has volatility 31.5 and asset B 22.75 with an index of 1604.', question: 'Which is larger?', widget: num(1) }], quiz: [] });
put('courses/s1/problems-1.json', { id: 'problems-1', items: [
  sc('p-falling-parabola', 'Take the falling curve $f(x) = 9 - x^2$ on $[0, 3]$. We split the interval into strips of equal width.', 'What is the area under the curve?'),
  sc('p-relative-strength', 'A price follows $P(t) = 40e^{0.06t}$ and an index follows another curve.', 'What is the ratio?'),
  sc('p-cube-root', 'You want the cube root of 8.06 and take $f(x) = x^{1/3}$ with $f\'(x) = \\tfrac{1}{3}x^{-2/3}$.', 'What is the estimate?'),
  sc('p-path-and-pipe', 'A path follows the line $y = 0.5x + 2$ across the field, and a pipe runs parallel.', 'What is the gradient of the pipe?'),
  sc('p-two-assets', 'A fund holds asset A with volatility 31.5 and asset B with volatility 22.75, so that the index reads 1604.', 'What is the blend?'),
  sc('p-fresh', 'A bag holds 7 red and 5 blue marbles and a child draws three without looking.', 'What is the chance all three are red?'),
] });
r = run(['--file', join(root, 'courses/s1/problems-1.json'), '--no-code']);
const setLines = r.stdout.split('\n');
const line = (id, re) => setLines.some((l) => l.includes(`problems-1.json:items[${id}]`) && re.test(l));
check('set reuse: the same curve as a homework item shares a formula (falling parabola)', line(0, /homework-1\.json:items\[0\].*shared formula f\(x\)=9-x\^2/), r.stdout);
check('set reuse: a formula inside a longer one of a review item (relative strength)', line(1, /review-3\.json:items\[0\].*shared formula P\(t\)=40e\^\{0\.06t\}/), r.stdout);
check('set reuse: the same function as a lesson screen (cube root)', line(2, /l1-tangent\.json:screens\[0\].*shared formula f\(x\)=x\^\{1\/3\}/), r.stdout);
check('set reuse: the same line as a lesson screen (path and pipe)', line(3, /l9-lines\.json:screens\[0\].*shared formula y=0\.5x\+2/), r.stdout);
check('set reuse: two specific parameters shared with a lesson screen (volatilities)', line(4, /l2-vols\.json:screens\[0\].*2 shared parameters \(31\.5 22\.75\)|l2-vols\.json:screens\[0\].*3 shared parameters/), r.stdout);
check('set reuse: an item with nothing shared is clean, and the lines are advisory (exit 0, "advisory")', !setLines.some((l) => l.includes('problems-1.json:items[5]')) && r.status === 0 && /advisory/.test(r.stdout), r.stdout);
check('set reuse: --no-set-reuse switches it off', !/shared formula|shared parameters/.test(run(['--file', join(root, 'courses/s1/problems-1.json'), '--no-code', '--no-set-reuse']).stdout));
check('set reuse: a review or homework set is not scanned for it (only problem sets)', !/shared formula/.test(run(['--file', join(root, 'courses/s1/review-3.json'), '--no-code']).stdout));
check('set reuse: --shared-params 4 needs four specific parameters', !/shared parameters/.test(run(['--file', join(root, 'courses/s1/problems-1.json'), '--no-code', '--shared-params', '4']).stdout));

rmSync(root, { recursive: true, force: true });
console.log(fails ? `${fails} failed` : 'all passed');
process.exit(fails ? 1 : 0);
