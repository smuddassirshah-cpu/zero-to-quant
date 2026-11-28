#!/usr/bin/env node
/* Test for `grade-all.mjs --code` and tools/code-runner.mjs (ENGINE-BACKLOG 1031, 1028, 1032): each failure kind from one scratch widget, and a clean one.
   Run from app/: node tools/test-grade-code.mjs --local-cdn <pkgs>   (needs <pkgs>/pyodide-0.27.7; without it the test says so and exits 0)
   Fixtures go to a temporary folder, not to app/content. Takes about a minute (one test waits out a 5 s limit, one a 10 s cap). */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2), ci = argv.indexOf('--local-cdn');
const cdnDir = ci >= 0 ? argv[ci + 1] : process.env.ZQ_LOCAL_CDN;
if (!cdnDir || !fs.existsSync(path.join(cdnDir, 'pyodide-0.27.7', 'package', 'pyodide.mjs'))) { console.log('test-grade-code: no local Pyodide (give --local-cdn <pkgs>); skipped'); process.exit(0); }
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-grade-code-'));
let pass = 0, fail = 0;
const say = (ok, name, extra = '') => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${ok ? '' : ' | ' + extra}`); ok ? pass++ : fail++; };
const run = (name, widget, feedback = null, extra = []) => {
  const f = path.join(tmp, name + '.json'); fs.writeFileSync(f, JSON.stringify({ screens: [{ widget: { kind: 'code', ...widget }, ...(feedback ? { feedback } : {}) }] }));
  const r = spawnSync('node', [path.join(HERE, 'grade-all.mjs'), '--local-cdn', cdnDir, '--jobs', '1', '--file', f, '--code', ...extra], { encoding: 'utf8', timeout: 170000 });
  return (r.stdout || '') + (r.stderr || '');
};
const base = { solution: 'def f(x):\n    return 2 * x', starter: 'def f(x):\n    pass', tests: [{ call: 'f(1)', expect: '2' }, { call: 'f(3)', expect: '6' }, { call: 'f(0)', expect: '0' }], examples: [{ call: 'f(2)', expect: '4' }] };

let o = run('clean', { ...base, mutants: [{ source: 'def f(x):\n    return x + x + 1', test: 1 }, { source: 'def f(x):\n    return 2 * x if x else 1', test: 3 }] });
say(/grade-all: 0 failures/.test(o) && /1 Python code widgets run/.test(o), 'a clean widget with two mutants passes', o.split('\n').slice(-4).join(' | '));

o = run('badsolution', { ...base, solution: 'def f(x):\n    return 3 * x' });
say(/solution-fails: the solution fails test 1/.test(o) && /examples-fail/.test(o), 'a wrong solution fails its tests and its examples', o);

o = run('starterpasses', { ...base, starter: base.solution });
say(/starter-passes/.test(o), 'a starter that passes is reported', o);

o = run('mutants', { ...base, mutants: [
  { source: base.solution, test: 1 },                                         // passes everything
  { source: 'def f(x):\n    return 2 * x if x else 9', test: 1 },             // fails test 3, not test 1
  { source: 'def f(x:\n    return', test: 1 },                                // does not load
  { source: 'def f(x):\n    return 7', test: 9 },                             // names a test that is not there
] });
say(/mutants\[0\] passes every hidden test/.test(o) && /mutants\[1\] first fails test 3, not test 1/.test(o) && /mutants\[2\] stops before the tests/.test(o) && /mutants\[3\] needs a source string and test/.test(o), 'each mutant failure is named', o);

const slowTest = { call: 'f(10)', expect: '20' };
const slowSol = 'def f(x):\n    return 2 * x';
o = run('timeout', { ...base, tests: [...base.tests, slowTest], solution: slowSol, mutants: [
  { source: 'def f(x):\n    while x == 10:\n        pass\n    return 2 * x', test: 4, timeout: true, factor: 2 },   // never finishes: passes the margin (10 s cap, 5 s limit)
  { source: 'def f(x):\n    while x == 10:\n        pass\n    return 2 * x', test: 4 },                          // times out but not marked
  { source: 'def f(x):\n    return 2 * x + 1 if x == 10 else 2 * x', test: 4, timeout: true },                  // fails on its answer, not on time
] });
say(!/mutants\[0\]/.test(o) && /mutants\[1\] fails test 4 by running out of time/.test(o) && /mutants\[2\] is marked timeout/.test(o), 'a timeout mutant is held to its margin', o);

o = run('slowsol', { ...base, tests: [...base.tests, { call: 'f(10)', expect: '20' }], solution: 'import time\ndef f(x):\n    if x == 10:\n        time.sleep(3)\n    return 2 * x', mutants: [{ source: 'def f(x):\n    while x == 10:\n        pass\n    return 2 * x', test: 4, timeout: true, factor: 2 }] });
say(/the solution takes \d+ ms on test 4, more than 1\/2 of its 5 s limit/.test(o), 'a solution close to the limit fails the margin', o);

/* 1037: zq_no_sort is there without a definition in the widget, and holds a merge to a real merge */
const merge = 'def merge(a, b):\n    out = []\n    i = j = 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]:\n            out.append(a[i]); i += 1\n        else:\n            out.append(b[j]); j += 1\n    return out + a[i:] + b[j:]\n';
const nosort = { tests: [{ call: 'merge([1, 3], [2])', expect: '[1, 2, 3]' }, { call: 'zq_no_sort()', expect: 'True' }], solution: merge, starter: 'def merge(a, b):\n    return []\n', mutants: [{ source: 'def merge(a, b):\n    return sorted(a + b)', test: 2 }, { source: 'def merge(a, b):\n    return (a + b).sort() or sorted(a)  # not sorted(\n', test: 1 }] };
o = run('nosort', nosort);
say(/grade-all: 0 failures/.test(o), 'zq_no_sort passes a real merge and fails sorted()', o);
o = run('nosort-script', { ...nosort, tests: [{ call: 'merge([1, 3], [2])', expect: '[1, 2, 3]' }, { call: 'zq_no_sort()', expect: 'True' }, { compare: 'stdout', expect: '' }], mutants: [{ source: 'def merge(a, b):\n    return sorted(a + b)', test: 2 }] });
say(/grade-all: 0 failures/.test(o), 'zq_no_sort in script mode', o);

/* 1268: zq_uses / zq_no read the syntax tree: comments and strings never count, bytes() is caught beside .encode, E[idx] is not '@', an explicit '@' is */
const ast1 = { starter: 'def f(x):\n    # np.convolve and corrcoef are not used; no for loops, no @ here\n    return 0\n', tests: [{ call: 'f(1)', expect: '2' }, { call: "zq_no('convolve', 'corrcoef', 'bytes', loops=True, attrs=('.encode',), ops=('@',))", expect: 'True' }, { call: "zq_uses('bytes', 'convolve', attrs=('encode',), ops=('@',))", expect: '[]' }] };
o = run('ast-comments', { ...ast1, solution: 'def f(x):\n    """Uses np.convolve? No: corrcoef, bytes(, .encode and a @ b are only words here."""\n    E = [1, 2, 3]\n    idx = x\n    s = "for x in y: bytes(s).encode()"\n    # np.convolve, for i in x, a @ b\n    return E[idx]', mutants: [{ source: 'import numpy as np\ndef f(x):\n    np.convolve([1], [1])\n    return [1, 2, 3][x]', test: 2 }, { source: 'def f(x):\n    return [1, 2, 3][x] if bytes("a", "utf-8") else 0', test: 2 }, { source: 'def f(x):\n    return [1, 2, 3][x] if "a".encode() else 0', test: 2 }, { source: 'def f(x):\n    return sum(1 for _ in range(1)) + [1, 2, 3][x] - 1', test: 2 }, { source: 'def f(x):\n    return [x * 2 @ 1][0]', test: 1 }, { source: 'def f(x):\n    import numpy as n\n    n.corrcoef([1, 2], [1, 3])\n    return [1, 2, 3][x]', test: 2 }] });
say(/grade-all: 0 failures/.test(o), 'zq_no ignores comments and strings, catches np.x, bytes(), .encode, loops', o);
o = run('ast-ops', { solution: 'def f(a, b):\n    E = [[1, 2], [3, 4]]\n    return E[a][b] + a * b', starter: 'def f(a, b):\n    return 0\n', tests: [{ call: 'f(1, 1)', expect: '5' }, { call: "zq_uses(ops=('@', '**'))", expect: '[]' }, { call: "zq_no(ops=('@',))", expect: 'True' }], mutants: [{ source: 'def f(a, b):\n    return [[1, 2], [3, 4]][a][b] + a * b + (a @ b if False else 0)', test: 2 }, { source: 'def f(a, b):\n    x = 1\n    x **= 2\n    return [[1, 2], [3, 4]][a][b] + a * b', test: 2 }] });
say(/grade-all: 0 failures/.test(o), 'zq_uses reports ops from the tree: E[idx] is not @, an explicit @ and **= are caught', o);
o = run('ast-numpy-alias', { solution: 'import numpy as np\ndef f(x):\n    return float(np.sum([x]))', starter: 'def f(x):\n    return 0\n', tests: [{ call: 'f(2)', expect: '2.0' }, { call: "zq_uses('sum', 'dot')", expect: "['sum']" }], mutants: [{ source: 'def f(x):\n    return 0.0', test: 1 }] });
say(/grade-all: 0 failures/.test(o), 'zq_uses reads np.x as x', o);

/* 976: an expected Fraction needs no import by the learner */
o = run('fraction', { tests: [{ call: 'f()', expect: 'Fraction(1, 3)', compare: 'fraction' }], solution: 'from fractions import Fraction as Fr\ndef f():\n    return Fr(1, 3)\n', starter: 'def f():\n    return 0\n' });
say(/grade-all: 0 failures/.test(o), 'a fraction expect evaluates without the learner importing Fraction', o);

/* ENGINE-BACKLOG 1264: --strand ai keeps only ai courses; --local-cdn also takes fetch-vendor.sh's layout */
{
  const root = path.join(tmp, 'app'); fs.mkdirSync(path.join(root, 'content', 'courses'), { recursive: true });
  for (const d of fs.readdirSync(path.join(HERE, '..'))) if (d !== 'content') fs.symlinkSync(path.join(HERE, '..', d), path.join(root, d));
  const bad = { screens: [{ widget: { kind: 'code', ...base, solution: 'def f(x):\n    return 3 * x' } }] };
  for (const [id, strand] of [['ca', 'ai'], ['cb', 'quant']]) {
    fs.mkdirSync(path.join(root, 'content', 'courses', id));
    fs.writeFileSync(path.join(root, 'content', 'courses', id, 'course.json'), JSON.stringify({ id, strand }));
    fs.writeFileSync(path.join(root, 'content', 'courses', id, 'l1-x.json'), JSON.stringify(bad));
  }
  const go2 = (extra) => { const r = spawnSync('node', [path.join(HERE, 'grade-all.mjs'), '--local-cdn', cdnDir, '--root', root, '--jobs', '1', '--code', ...extra], { encoding: 'utf8', timeout: 170000 }); return (r.stdout || '') + (r.stderr || ''); };
  fs.mkdirSync(path.join(root, 'content', 'exams'));
  fs.writeFileSync(path.join(root, 'content', 'curriculum.json'), JSON.stringify({ stages: [{ topics: [{ id: 'T1', courses: ['ca'] }, { id: 'T2', courses: ['ca', 'cb'] }] }] }));
  for (const t of ['T1', 'T2']) fs.writeFileSync(path.join(root, 'content', 'exams', 'topic-' + t + '.json'), JSON.stringify({ topic: t, ...bad }));
  o = go2(['--strand', 'ai']);
  say(/topic-T1\.json#.*solution-fails/.test(o) && !/topic-T2/.test(o) && /2 Python code widgets run/.test(o), '--strand ai includes an exam of an AI topic only', o);
  const vend = path.join(tmp, 'vend'); fs.mkdirSync(path.join(vend, 'compute-engine'), { recursive: true });
  fs.symlinkSync(path.join(cdnDir, 'pyodide-0.27.7', 'package'), path.join(vend, 'pyodide'));
  const ce = path.join(cdnDir, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
  if (fs.existsSync(ce)) fs.symlinkSync(ce, path.join(vend, 'compute-engine', 'compute-engine.min.umd.js'));
  const go = (cdn, extra) => { const r = spawnSync('node', [path.join(HERE, 'grade-all.mjs'), '--local-cdn', cdn, '--root', root, '--jobs', '1', '--code', ...extra], { encoding: 'utf8', timeout: 170000 }); return (r.stdout || '') + (r.stderr || ''); };
  o = go(cdnDir, ['--strand', 'ai']);
  say(/ca\/l1-x\.json#.*solution-fails/.test(o) && !/cb\/l1-x/.test(o) && /2 Python code widgets run/.test(o), '--strand ai runs only the ai course', o);
  o = go(cdnDir, []);
  say(/cb\/l1-x/.test(o) && /4 Python code widgets run/.test(o), 'without --strand both courses run', o);
  if (fs.existsSync(ce)) { o = go(vend, ['--strand', 'ai']); say(/ca\/l1-x\.json#.*solution-fails/.test(o) && /2 Python code widgets run/.test(o), '--local-cdn takes the fetch-vendor.sh layout', o); }
}

/* ENGINE-BACKLOG 1269: byKey lines no mutant reaches, and tests a mutant fails with no line. Only in a strand-ai course (a temporary content root). */
{
  const root = path.join(tmp, 'fbroot'), cd = path.join(root, 'content', 'courses', 'cai');
  fs.mkdirSync(cd, { recursive: true });
  for (const d of fs.readdirSync(path.join(HERE, '..'))) if (d !== 'content') fs.symlinkSync(path.join(HERE, '..', d), path.join(root, d));
  fs.writeFileSync(path.join(cd, 'course.json'), JSON.stringify({ id: 'cai', strand: 'ai' }));
  const w = { kind: 'code', ...base, mutants: [{ source: 'def f(x):\n    return x + x + 1', test: 1 }, { source: 'def f(x):\n    return 2 * x if x else 1', test: 3 }] };
  const go = (name, feedback, extra = []) => {
    fs.writeFileSync(path.join(cd, name + '.json'), JSON.stringify({ screens: [{ widget: w, feedback }] }));
    const r = spawnSync('node', [path.join(HERE, 'grade-all.mjs'), '--local-cdn', cdnDir, '--root', root, '--jobs', '1', '--file', path.join(cd, name + '.json'), '--code', ...extra], { encoding: 'utf8', timeout: 170000 });
    fs.unlinkSync(path.join(cd, name + '.json')); return { out: (r.stdout || '') + (r.stderr || ''), code: r.status };
  };
  let r = go('ok', { byKey: { 'test-1': 'a', 'test-3': 'b' } });
  say(r.code === 0 && !/feedback/.test(r.out), 'lines for every reached test pass', r.out);
  r = go('unreach', { byKey: { 'test-1': 'a', 'test-3': 'b', 'test-2': 'c' } });
  say(r.code === 0 && /warning feedback-unreachable: byKey "test-2"/.test(r.out) && /cai unreachable 1/.test(r.out), 'a test-2 line no mutant reaches warns and the run passes', r.out);
  r = go('unreach', { byKey: { 'test-1': 'a', 'test-3': 'b', 'test-2': 'c' } }, ['--strict-feedback']);
  say(r.code === 1 && /feedback-unreachable/.test(r.out), '--strict-feedback fails an unreachable line', r.out);
  r = go('missing', { byKey: { 'test-1': 'a' } });
  say(r.code === 0 && /warning feedback-missing: a mutant first fails test 3/.test(r.out), 'a mutant failing test 3 with no line warns', r.out);
  r = go('missing', { byKey: { 'test-1': 'a' } }, ['--strict-feedback']);
  say(r.code === 1 && /feedback-missing/.test(r.out), '--strict-feedback fails a missing line', r.out);
}

console.log(`test-grade-code: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
