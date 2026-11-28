#!/usr/bin/env node
/* Test for the trainer widget's Python side (ENGINE-BACKLOG 1237): the harness that js/engine/widgets/code.js builds (`trainPlan`) is run in
   Pyodide with the page worker's own grader (the GRADER string of js/screens/drill-worker.js), and the events it streams are checked.
   Run from app/: node tools/test-trainer.mjs --local-cdn <pkgs>   (needs <pkgs>/pyodide-0.27.7; without it the test says so and exits 0)
     report() rows stream in order, with extra series and null for a non-finite loss; the step cap ends the run at exactly that many reports;
     printed lines "step N loss X" count as reports; the wall-clock cap stops a loop that keeps reporting; a learner error keeps the rows
     already sent and gives a traceback of the learner's lines; a loop that ends by itself says so; a supplied prelude and data file are seen.
   Takes about ten seconds (one case waits out a 1 s cap). */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { pathToFileURL, fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url)), ROOT = path.join(HERE, '..');
const argv = process.argv.slice(2), ci = argv.indexOf('--local-cdn');
const cdnDir = ci >= 0 ? argv[ci + 1] : process.env.ZQ_LOCAL_CDN;
const indexDir = cdnDir && [path.join(cdnDir, 'pyodide-0.27.7', 'package'), path.join(cdnDir, 'pyodide')].find((d) => fs.existsSync(path.join(d, 'pyodide.mjs')));
if (!indexDir || !fs.existsSync(path.join(indexDir, 'pyodide.mjs'))) { console.log('test-trainer: no local Pyodide (give --local-cdn <pkgs>); skipped'); process.exit(0); }

const g = { console, setTimeout, clearTimeout, document: {}, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
g.ZQ = { widgets: { register() {} }, esc: (s) => String(s), h: () => ({}) };
vm.runInContext(fs.readFileSync(path.join(ROOT, 'js/engine/widgets/code.js'), 'utf8'), g, { filename: 'code.js' });
const trainPlan = g.ZQ.widgets.trainPlan;
if (typeof trainPlan !== 'function') { console.error('FAIL code.js does not export widgets.trainPlan'); process.exit(1); }

const workerSrc = fs.readFileSync(path.join(ROOT, 'js/screens/drill-worker.js'), 'utf8');
const graderSrc = /const GRADER = String\.raw`([\s\S]*?)`;/.exec(workerSrc)[1];
const { loadPyodide } = await import(pathToFileURL(path.join(indexDir, 'pyodide.mjs')).href);
const py = await loadPyodide({ indexURL: indexDir + '/', stdout: () => {}, stderr: () => {} });
py.runPython(graderSrc);
const runFn = py.globals.get('drl_run');

let pass = 0, fail = 0;
const say = (ok, name, extra = '') => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${ok ? '' : ' | ' + extra}`); ok ? pass++ : fail++; };
const train = (spec, src, files) => {
  const plan = trainPlan(spec, src, files);
  const ev = [];
  runFn(plan.code, JSON.stringify({ fn: '__zq_train', compare: 'isclose', prelude: '', tests: [{ args: '(0,)', expected: 1 }] }), (s) => ev.push(JSON.parse(s)));
  const rows = ev.filter(e => e.kind === 'steps').flatMap(e => e.rows);
  return { ev, rows, stopped: ev.find(e => e.kind === 'stopped'), test: ev.find(e => e.kind === 'test'), err: ev.find(e => e.kind === 'error') };
};

let r = train({ steps: 50 }, 'for s in range(1000):\n    report(s, 1.0 / (s + 1), val=2.0 * s)\n');
say(r.stopped && r.stopped.why === 'steps' && r.stopped.n === 50 && r.rows.length === 50, 'the step cap ends the run at exactly 50 reports', JSON.stringify(r.stopped) + ' ' + r.rows.length);
say(r.rows.every((x, k) => x.i === k) && r.rows[3].loss === 0.25 && r.rows[3].val === 6, 'rows arrive in order with the extra series', JSON.stringify(r.rows[3]));
say(r.test && r.test.ok && !r.test.error, 'a capped run is a clean test event, not an error', JSON.stringify(r.test));

r = train({ steps: 10 }, 'report(0, float("nan"))\nreport(1, float("inf"))\nreport(2, 0.5)\n');
say(r.rows.length === 3 && r.rows[0].loss === null && r.rows[1].loss === null && r.rows[2].loss === 0.5 && r.stopped.why === 'done', 'a non-finite loss goes through as null (valid JSON) and the loop that ends says done', JSON.stringify(r.rows));

r = train({ steps: 100 }, 'for s in range(5):\n    print(f"step {s} loss {1/(s+1):.3f}")\nprint("not a step line")\nprint("Step 9, loss: 1e-3")\n');
say(r.rows.length === 6 && r.rows[0].step === 0 && r.rows[5].loss === 0.001 && /not a step line/.test(r.test.stdout), 'printed "step N loss X" lines count as reports and all output is kept', JSON.stringify(r.rows) + r.test.stdout);

const t0 = Date.now();
r = train({ steps: 20000, maxSeconds: 1 }, 'import time\nt = time.time()\ns = 0\nwhile True:\n    s += 1\n    if s % 1000 == 0:\n        report(s, 1.0)\n    time.sleep(0) if False else None\n');
say(r.stopped && r.stopped.why === 'time' && Date.now() - t0 < 6000, 'the wall-clock cap stops a loop that keeps reporting', JSON.stringify(r.stopped) + ' ' + (Date.now() - t0) + ' ms');

r = train({ steps: 100 }, 'for s in range(10):\n    report(s, 1.0)\nraise ValueError("boom")\n');
say(r.test && r.test.error && /ValueError: boom/.test(r.test.error) && /solution\.py/.test(r.test.error) && r.rows.length === 10, 'a learner error keeps the rows already sent and shows a learner traceback', JSON.stringify(r.test));

r = train({ steps: 100 }, 'x = (\n');
say(r.test && r.test.error && /SyntaxError/.test(r.test.error) && r.rows.length === 0, 'a syntax error is reported as an error with no rows', JSON.stringify(r.test || r.err));

r = train({ steps: 5, prelude: 'BASE = 7\n' }, 'data = open("t.txt").read()\nfor s in range(3):\n    report(s, BASE + len(data))\n', { 't.txt': 'abcd' });
say(r.rows.length === 3 && r.rows[0].loss === 11, 'a prelude and a data file are visible to the loop', JSON.stringify(r.rows) + JSON.stringify(r.test));

r = train({ steps: 5 }, 'try:\n    report(0, 1.0)\n    for s in range(1, 100):\n        report(s, 1.0)\nexcept Exception:\n    print("caught")\n');
say(r.stopped && r.stopped.why === 'steps' && r.rows.length === 5, 'the stop is not swallowed by a learner except Exception', JSON.stringify(r.stopped));

console.log(`test-trainer: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
