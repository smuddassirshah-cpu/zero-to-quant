#!/usr/bin/env node
/* Test for tools/grade-all.mjs: one fixture per failure kind, and a clean file that must pass.
   Run from app/: node tools/test-grade-all.mjs [--local-cdn <pkgs>]   (the Compute Engine as grade-all.mjs finds it: --local-cdn, ZQ_LOCAL_CDN, else the network)
   Exit 0 pass, 1 failure. Fixtures are written to a temporary folder, not to app/content. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2), ci = argv.indexOf('--local-cdn');
const cdn = ci >= 0 ? ['--local-cdn', argv[ci + 1]] : [];
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-grade-all-'));
let pass = 0, fail = 0;
const say = (ok, name, extra = '') => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${ok ? '' : ' | ' + extra}`); ok ? pass++ : fail++; };
const run = (file, ...more) => { const r = spawnSync('node', [path.join(HERE, 'grade-all.mjs'), ...cdn, '--jobs', '2', '--file', file, ...more], { encoding: 'utf8', timeout: 110000 }); return { out: (r.stdout || '') + (r.stderr || ''), code: r.status }; };
const write = (name, widgets) => { const f = path.join(tmp, name); fs.writeFileSync(f, JSON.stringify({ screens: widgets.map((widget) => ({ widget })) })); return f; };
const num = (extra) => ({ kind: 'numeric', answer: 5, tol: { abs: 0.01 }, ...extra });
const opts = (...c) => c.map((x, i) => ({ id: 'o' + i, text: 'Option ' + i, ...(x ? { correct: true } : {}) }));

/* the failing fixtures, one widget each */
const BAD = [
  ['key-refused', num({ tol: { abs: -1 } })],                                                                   // a band that refuses its own key
  ['wrong-grades-right', num({ tol: { abs: 0.5 }, wrong: [{ id: 'near', value: 5.2, tol: { abs: 0.5 } }] })],      // the slip sits inside the key's band
  ['wrong-misrouted', num({ wrong: [{ id: 'a', value: 8, tol: { abs: 0.5 } }, { id: 'b', value: 8.2, tol: { abs: 0.5 } }] })],   // b is taken by a's band first
  ['wrong-unrouted', num({ wrong: [{ id: 'x', value: 8, tol: { abs: -1 } }] })],                                // its own band refuses it: the generic miss
  ['accept-refused', { kind: 'expression', answer: '2(x+2)', form: 'factorised-fully', accept: ['2x+4'] }],               // an accept form that fails the form the answer must take
  ['wrong-misrouted', { kind: 'expression', answer: 'x+1', wrong: [{ id: 'p', tex: '2x' }, { id: 'q', tex: 'x+x' }] }],   // x+x is 2x: p takes it
  ['choice-key', { kind: 'choice', shuffle: false, options: opts(true, true, false) }],                         // two correct options
  ['key-refused', { kind: 'table', rows: [['a', { edit: true, answer: 3, tol: { abs: -1 } }]] }],               // a table cell that refuses its key
  ['wrong-misrouted', { kind: 'table', rows: [['a', { edit: true, answer: 3, tol: { abs: 0 }, wrong: [{ id: 'm', value: 4, tol: { abs: 0 } }, { id: 'n', value: 4, tol: { abs: 0 } }] }]] }],
];
const bad = write('bad.json', BAD.map((b) => b[1]));
const r = run(bad);
say(r.code === 1, 'the failing fixtures exit 1', `exit ${r.code}`);
BAD.forEach(([kind], i) => say(new RegExp(`bad\\.json#screens\\[${i}\\]\\.widget: ${kind}: `).test(r.out), `screens[${i}] is reported as ${kind}`, r.out.split('\n').slice(0, 14).join(' | ')));
const counts = {}; BAD.forEach(([k]) => { counts[k] = (counts[k] || 0) + 1; });
say(r.out.includes(`grade-all: ${BAD.length} failures: ${Object.entries(counts).map(([k, n]) => `${k} ${n}`).join(', ')}`) || Object.entries(counts).every(([k, n]) => r.out.includes(`${k} ${n}`)), 'the summary counts every kind', r.out.split('\n').slice(-3).join(' | '));

/* the clean file: right keys, accept forms and routed slips of every covered kind */
const good = write('good.json', [
  num({ wrong: [{ id: 'ten', value: 10, tol: { abs: 0.5 } }, { id: 'half', value: 2.5, tol: { abs: 0.1 } }] }),
  { kind: 'numeric', answer: 0.25, unit: '%', tol: { abs: 0.001 }, wrong: [{ id: 'dec', value: 0.0025, tol: { abs: 0.0001 } }] },
  { kind: 'numeric', answers: [2, -5], unordered: true, tol: { abs: 0 }, wrong: [{ id: 'flip', value: '-2, 5' }] },
  { kind: 'expression', answer: '(x+1)^2', accept: ['x^2+2x+1'], wrong: [{ id: 'drop', tex: 'x^2+1' }] },
  { kind: 'choice', shuffle: false, options: [{ id: 'a', text: 'A', correct: true }, { id: 'b', text: 'B', why: 'No.' }, { id: 'c', text: 'C' }] },
  { kind: 'multi', shuffle: false, options: [{ id: 'a', text: 'A', correct: true }, { id: 'b', text: 'B', correct: true }, { id: 'c', text: 'C', why: 'No.' }] },
  { kind: 'table', columns: ['k', 'v'], rows: [['a', { edit: true, answer: 3, tol: { abs: 0.01 }, wrong: [{ id: 'four', value: 4 }] }], ['b', { edit: true, answer: 'O(n log n)', accept: ['n log n'], wrong: [{ id: 'lin', text: 'O(n)' }] }]] },
  { kind: 'longform', prompt: 'Not covered, so skipped.' },
]);
const g = run(good);
say(g.code === 0 && /grade-all: 0 failures/.test(g.out), 'a clean file of every covered kind passes', g.out.split('\n').slice(-6).join(' | '));
say(/7 widgets checked/.test(g.out), 'the seven covered widgets are counted and the longform is not', g.out.split('\n').slice(-3).join(' | '));
const missing = run(path.join(tmp, 'nope.json'));
say(missing.code === 2, 'a named file that is missing is a setup problem (exit 2)', `exit ${missing.code}`);
const sh = spawnSync('node', [path.join(HERE, 'grade-all.mjs'), ...cdn, '--shard', '3/2'], { encoding: 'utf8' });
say(sh.status === 2 && /--shard needs i\/n/.test(sh.stderr), 'a bad --shard is refused', `exit ${sh.status} ${sh.stderr}`);

fs.rmSync(tmp, { recursive: true, force: true });
console.log(`test-grade-all: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
