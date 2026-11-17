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
const run = (name, widget) => {
  const f = path.join(tmp, name + '.json'); fs.writeFileSync(f, JSON.stringify({ screens: [{ widget: { kind: 'code', ...widget } }] }));
  const r = spawnSync('node', [path.join(HERE, 'grade-all.mjs'), '--local-cdn', cdnDir, '--jobs', '1', '--file', f, '--code'], { encoding: 'utf8', timeout: 170000 });
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

/* 976: an expected Fraction needs no import by the learner */
o = run('fraction', { tests: [{ call: 'f()', expect: 'Fraction(1, 3)', compare: 'fraction' }], solution: 'from fractions import Fraction as Fr\ndef f():\n    return Fr(1, 3)\n', starter: 'def f():\n    return 0\n' });
say(/grade-all: 0 failures/.test(o), 'a fraction expect evaluates without the learner importing Fraction', o);

console.log(`test-grade-code: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
