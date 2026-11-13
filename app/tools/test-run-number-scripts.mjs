#!/usr/bin/env node
/* Test for tools/run-number-scripts.mjs (ENGINE-BACKLOG 971): builds a small repository in a temporary folder and checks the verdicts:
   a pass is green; a new failure and a timeout are red; a listed failure is green; a listed script that passes, and a listed path that is gone, are red;
   --only does not judge the list; --changed picks a script by its own file or by the course it names; a script runs in its own folder.
     node tools/test-run-number-scripts.mjs        (needs python3 and git on the PATH; exit 0 all pass) */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const RUNNER = path.join(HERE, 'run-number-scripts.mjs');
const PY = process.env.ZQ_PYTHON || 'python3';
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-rns-'));
let bad = 0, n = 0;
const check = (ok, name, extra = '') => { n++; if (!ok) { bad++; console.log(`FAIL ${name}${extra ? ': ' + extra : ''}`); } else console.log(`ok   ${name}`); };
const w = (rel, text) => { const p = path.join(root, rel); fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p, text); };
const run = (...args) => { const r = spawnSync('node', [RUNNER, '--root', root, '--python', PY, '--allow', path.join(root, 'known.txt'), ...args], { encoding: 'utf8' }); return { code: r.status, out: (r.stdout || '') + (r.stderr || '') }; };
const git = (...a) => spawnSync('git', ['-C', root, '-c', 'user.email=t@example.invalid', '-c', 'user.name=t', ...a], { encoding: 'utf8' });

w('docs/reports/ok-numbers.py', 'print("fine")\n');
w('docs/reports/bad-numbers.py', 'import sys\nprint("a check failed")\nsys.exit(1)\n');
w('docs/reports/slow-numbers.py', 'import time\ntime.sleep(30)\n');
w('docs/reports/not-a-script.py', 'raise SystemExit(1)\n');                       // name has no "-numbers": not run
w('docs/briefs/x-scripts/check_numbers.py', 'print(open("sibling.txt").read())\n'); // runs in its own folder
w('docs/briefs/x-scripts/sibling.txt', 'beside me\n');
w('docs/reviews/y-scripts/other.py', 'raise SystemExit(1)\n');                      // not a number script
w('docs/reports/ci-cpp-numbers.py', 'print("names course ci")\n');
w('app/content/courses/ci/l1.json', '{}\n');
w('known.txt', '');

let r = run('--only', 'docs/reports/ok-');
check(r.code === 0 && /1 of 5 scripts, 1 passed/.test(r.out), 'a passing script is green', r.out);

r = run('--list');
check(r.code === 0 && /5 number scripts/.test(r.out) && !/not-a-script|other\.py/.test(r.out), 'only number scripts are found', r.out);

r = run('--only', 'docs/reports/bad-');
check(r.code === 1 && /FAILED\s+docs\/reports\/bad-numbers\.py \(exit 1\)/.test(r.out) && /a check failed/.test(r.out) && /1 new failure/.test(r.out), 'a new failure is red and shows its last lines', r.out);

r = run('--only', 'docs/reports/slow-', '--timeout', '1');
check(r.code === 1 && /timed out after 1 s/.test(r.out), 'a timeout is red', r.out);

r = run('--only', 'docs/briefs/');
check(r.code === 0 && /1 passed/.test(r.out), 'a script runs in its own folder', r.out);

w('known.txt', '# comment\n\ndocs/reports/bad-numbers.py | content finding, see the report\n');
r = run('--only', 'docs/reports/bad-');
check(r.code === 0 && /1 known failing, 0 new failures/.test(r.out) && !/FAILED/.test(r.out), 'a listed failure is green and silent', r.out);

w('docs/reports/bad-numbers.py', 'print("repaired")\n');
r = run('--only', 'docs/reports/bad-');
check(r.code === 1 && /PASSES NOW\s+docs\/reports\/bad-numbers\.py/.test(r.out), 'a listed script that passes is red', r.out);

w('known.txt', 'docs/reports/gone-numbers.py | was removed\n');
r = run('--only', 'docs/reports/ok-');
check(r.code === 1 && /MISSING\s+docs\/reports\/gone-numbers\.py/.test(r.out), 'a listed path that no longer exists is red', r.out);

w('known.txt', 'no separator here\n');
r = run('--only', 'docs/reports/ok-');
check(r.code === 2, 'a malformed list line is a setup error (exit 2)', r.out);

w('known.txt', '');
fs.writeFileSync(path.join(root, 'docs/reports/slow-numbers.py'), 'print("fast now")\n');
r = run();
check(r.code === 0 && /^run-number-scripts: 5 scripts, 5 passed/m.test(r.out), 'a full run counts every script', r.out);

/* --changed, in a git repository */
git('init', '-q'); git('add', '-A'); git('commit', '-q', '-m', 'one');
w('docs/reports/ok-numbers.py', 'print("edited")\n');
git('add', '-A'); git('commit', '-q', '-m', 'two');
r = run('--changed', 'HEAD~1');
check(r.code === 0 && /1 of 5 scripts, 1 passed/.test(r.out), 'changed: a script whose own file changed runs alone', r.out);

w('app/content/courses/ci/l1.json', '{"edited": true}\n');
git('add', '-A'); git('commit', '-q', '-m', 'three');
r = run('--changed', 'HEAD~1');
check(r.code === 0 && /1 of 5 scripts, 1 passed/.test(r.out) && !/FAILED/.test(r.out), 'changed: a course edit runs the script that names the course', r.out);

r = run('--changed', 'no-such-ref');
check(/running every script/.test(r.out) && /^run-number-scripts: 5 scripts, 5 passed/m.test(r.out), 'changed: an unknown base ref runs everything', r.out);

fs.rmSync(root, { recursive: true, force: true });
console.log(`test-run-number-scripts: ${n - bad} of ${n} checks pass`);
process.exit(bad ? 1 : 0);
