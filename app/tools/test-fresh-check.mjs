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

rmSync(root, { recursive: true, force: true });
console.log(fails ? `${fails} failed` : 'all passed');
process.exit(fails ? 1 : 0);
