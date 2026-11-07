#!/usr/bin/env node
/* Scratch cases for ENGINE-BACKLOG 605: [shown-arithmetic] recomputes "number op number = number" inside a maths span.
   Copies app/ to a temp folder and edits the prose of one algo-think screen. Run: node app/tools/test-validate-shown-arithmetic.mjs. Exit 1 on a failure. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-sa-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/]node_modules([\\/]|$)/.test(s) });
const run = () => { try { return { out: execFileSync('node', [path.join(copy, 'tools', 'validate.mjs'), '--no-manifest'], { cwd: copy, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], maxBuffer: 1 << 28 }), code: 0 }; } catch (e) { return { out: String(e.stdout || ''), code: e.status }; } };
const f = path.join(copy, 'content', 'courses', 'algo-think', 'l1-counting-work.json');
const orig = fs.readFileSync(f, 'utf8');
let fails = 0;
const say = (ok, name) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}`); if (!ok) fails++; };
const withProse = (t) => { const j = JSON.parse(orig); j.screens[0].prose = t; fs.writeFileSync(f, JSON.stringify(j, null, 2) + '\n'); return run(); };
const hit = (o) => /algo-think.*\[shown-arithmetic\]/.test(o);
const cases = [
  ['sum of rounded terms off in the last digit: warns', 'Add: $0.6124 + 0.3536 = 0.9659$ here.', true],
  ['\\approx a unit out: warns', 'Ratio $1.38/0.45 \\approx 3.05$ here.', true],
  ['\\frac and \\times, correct at the result places: no warning', 'Work $\\frac{1.38}{0.45} \\approx 3.07$ and $12 \\times 5 = 60$ and $1.02^{36} \\approx 2.04$.', false],
  ['\\approx within one unit: no warning', 'Ratio $1.38/0.45 \\approx 3.06$ here.', false],
  ['three-figure \\approx with trailing zeros: no warning', 'Ratio $6.1/0.0009 \\approx 6{,}780$ here.', false],
  ['a wide miss is a deliberate wrong claim: no warning', 'The slip: $48 \\times 21 = 10{,}080$ here.', false],
  ['letters in a segment skip it: no warning', 'We have $x = 3 + 4 = 7.5$ and $P = 100 \\times 1.05 = 105$ and $y = 7%$.', false],
];
say(run().code === 0, 'untouched copy: 0 errors');
for (const [name, text, expect] of cases) { const r = withProse(text); say(r.code === 0 && hit(r.out) === expect, name); }
fs.rmSync(tmp, { recursive: true, force: true });
process.exit(fails ? 1 : 0);
