#!/usr/bin/env node
/* Concept audit integrals L1-3, round 3: sweep of every feedback.byKey.test-N line on the Python code widgets in scope
   (l12-no-formula screens 4 and 9, homework-3 item 5). For each line, two or three natural codings of the named mistake are graded
   through the page's own harness (tools/code-runner.mjs, Pyodide 0.27.7 from the local CDN). A line passes when most of its codings
   fail test N first. Also submits obvious wrong programs and reports any that pass every hidden test.
   Run from the repo root:  node docs/reports/integrals-L1-3-test-line-sweep-r3.mjs <pkgs>
   Exit 0 when every line holds and no wrong program passes; 1 otherwise. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '../../app');
const pkgs = process.argv[2] || process.env.ZQ_LOCAL_CDN;
if (!pkgs) { console.error('usage: node integrals-L1-3-test-line-sweep-r3.mjs <pkgs>'); process.exit(2); }
const { makeRunner } = await import(pathToFileURL(path.join(APP, 'tools/code-runner.mjs')).href);
const runner = makeRunner({ pkgs, root: APP, jobs: 2 });
const load = (f) => JSON.parse(fs.readFileSync(path.join(APP, 'content/courses/integrals', f), 'utf8'));

const TRAP = `def trapezium(f, a, b, n):
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        left = a + i * h
        total += h * (f(left) + f(left + h)) / 2
    return total
`;
const PHI = `import math

${TRAP}
def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
`;
const trap = (body) => `def trapezium(f, a, b, n):\n${body}\n`;

const l12 = load('l12-no-formula.json'), hw3 = load('homework-3.json');
const W = {
  trapezium: l12.screens[3].widget,
  phi: l12.screens[8].widget,
  nneeded: hw3.items[4].widget,
};

/* [widget, line key or 'none' (must pass) or 'any' (must fail somewhere), label, source] */
const CASES = [
  // ---- l12 screen 4: trapezium ----
  ['trapezium', 'test-1', 'starter (no loop)', W.trapezium.starter],
  ['trapezium', 'test-1', 'one strip short: range(n - 1)', trap('    h = (b - a) / n\n    total = 0.0\n    for i in range(n - 1):\n        left = a + i * h\n        total += h * (f(left) + f(left + h)) / 2\n    return total')],
  ['trapezium', 'test-1', 'one strip too many: range(n + 1)', trap('    h = (b - a) / n\n    total = 0.0\n    for i in range(n + 1):\n        left = a + i * h\n        total += h * (f(left) + f(left + h)) / 2\n    return total')],
  ['trapezium', 'test-1', 'strips from 1 to n - 1: range(1, n)', trap('    h = (b - a) / n\n    total = 0.0\n    for i in range(1, n):\n        left = a + i * h\n        total += h * (f(left) + f(left + h)) / 2\n    return total')],
  ['trapezium', 'test-3', 'guard that skips a single strip', trap('    if n < 2:\n        return 0.0\n    h = (b - a) / n\n    total = 0.0\n    for i in range(n):\n        left = a + i * h\n        total += h * (f(left) + f(left + h)) / 2\n    return total')],
  ['trapezium', 'test-3', 'inside points only when n = 1 (ends added in the loop)', trap('    h = (b - a) / n\n    total = 0.0\n    for i in range(1, n):\n        total += f(a + i * h)\n        if i == 1:\n            total += (f(a) + f(b)) / 2\n    return h * total')],
  ['trapezium', 'test-3', 'ends added only when n > 1', trap('    h = (b - a) / n\n    total = h * (f(a) + f(b)) / 2 if n > 1 else 0.0\n    for i in range(1, n):\n        total += h * f(a + i * h)\n    return total')],
  ['trapezium', 'test-6', 'edges built from 0: left = i * h', trap('    h = (b - a) / n\n    total = 0.0\n    for i in range(n):\n        left = i * h\n        total += h * (f(left) + f(left + h)) / 2\n    return total')],
  ['trapezium', 'test-6', 'point list from 0, ends halved', trap('    h = (b - a) / n\n    xs = [i * h for i in range(n + 1)]\n    total = (f(xs[0]) + f(xs[-1])) / 2\n    for x in xs[1:-1]:\n        total += f(x)\n    return h * total')],
  ['trapezium', 'test-6', 'edges from 0 with right = (i + 1) * h', trap('    h = (b - a) / n\n    total = 0.0\n    for i in range(n):\n        total += h * (f(i * h) + f((i + 1) * h)) / 2\n    return total')],
  ['trapezium', 'none', 'each point once, ends halved (correct)', trap('    h = (b - a) / n\n    total = (f(a) + f(b)) / 2\n    for i in range(1, n):\n        total += f(a + i * h)\n    return h * total')],
  ['trapezium', 'any', 'WRONG: left rectangles', trap('    h = (b - a) / n\n    total = 0.0\n    for i in range(n):\n        total += h * f(a + i * h)\n    return total')],
  ['trapezium', 'any', 'WRONG: midpoint rule', trap('    h = (b - a) / n\n    total = 0.0\n    for i in range(n):\n        total += h * f(a + (i + 0.5) * h)\n    return total')],
  ['trapezium', 'any', 'WRONG: Jo, range(n) points', trap('    h = (b - a) / n\n    xs = [a + i * h for i in range(n)]\n    total = (f(xs[0]) + f(xs[-1])) / 2\n    for x in xs[1:-1]:\n        total += f(x)\n    return h * total')],
  ['trapezium', 'any', 'WRONG: h = b / n', trap('    h = b / n\n    total = 0.0\n    for i in range(n):\n        left = a + i * h\n        total += h * (f(left) + f(left + h)) / 2\n    return total')],
  ['trapezium', 'any', 'WRONG: Simpson weights', trap('    h = (b - a) / n\n    total = f(a) + f(b)\n    for i in range(1, n):\n        total += (4 if i % 2 else 2) * f(a + i * h)\n    return h * total / 3')],
  // ---- l12 screen 9: phi and prob_within ----
  ['phi', 'test-1', 'starter (returns 0.0)', W.phi.starter],
  ['phi', 'test-1', 'no square root: / (2 * pi)', `import math\n\n${TRAP}\ndef phi(x):\n    return math.exp(-x * x / 2) / (2 * math.pi)\n\ndef prob_within(z, n):\n    return trapezium(phi, -z, z, n)\n`],
  ['phi', 'test-1', 'root of 2 only: sqrt(2) * pi', `import math\n\n${TRAP}\ndef phi(x):\n    return math.exp(-x * x / 2) / (math.sqrt(2) * math.pi)\n\ndef prob_within(z, n):\n    return trapezium(phi, -z, z, n)\n`],
  ['phi', 'test-1', 'no constant at all', `import math\n\n${TRAP}\ndef phi(x):\n    return math.exp(-x * x / 2)\n\ndef prob_within(z, n):\n    return trapezium(phi, -z, z, n)\n`],
  ['phi', 'test-4', 'integrates from 0 to z', `${PHI}\ndef prob_within(z, n):\n    return trapezium(phi, 0, z, n)\n`],
  ['phi', 'test-4', 'calls phi()', `${PHI}\ndef prob_within(z, n):\n    return trapezium(phi(), -z, z, n)\n`],
  ['phi', 'test-4', 'passes phi(z)', `${PHI}\ndef prob_within(z, n):\n    return trapezium(phi(z), -z, z, n)\n`],
  ['phi', 'test-4', 'prob_within left as the starter', `${PHI}\ndef prob_within(z, n):\n    return 0.0\n`],
  ['phi', 'any', 'WRONG: exponent -x*x (no half)', `import math\n\n${TRAP}\ndef phi(x):\n    return math.exp(-x * x) / math.sqrt(2 * math.pi)\n\ndef prob_within(z, n):\n    return trapezium(phi, -z, z, n)\n`],
  ['phi', 'any', 'WRONG: n hard-coded at 1000', `${PHI}\ndef prob_within(z, n):\n    return trapezium(phi, -z, z, 1000)\n`],
  ['phi', 'any', 'WRONG: math.erf closed form, ignoring n', `${PHI}\ndef prob_within(z, n):\n    return math.erf(z / math.sqrt(2))\n`],
  ['phi', 'any', 'twice the half range (2n strips in effect)', `${PHI}\ndef prob_within(z, n):\n    return 2 * trapezium(phi, 0, z, n)\n`],
  ['phi', 'error', 'syntax error (missing bracket)', `${PHI}\ndef prob_within(z, n):\n    return trapezium(phi, -z, z, n\n`],
  // ---- homework-3 item 5: trapezium and n_needed ----
  ['nneeded', 'test-1', 'starter (pass)', W.nneeded.starter],
  ['nneeded', 'test-1', 'one strip short', `${trap('    h = (b - a) / n\n    total = 0.0\n    for i in range(n - 1):\n        left = a + i * h\n        total += h * (f(left) + f(left + h)) / 2\n    return total')}\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, n) - exact) >= tol:\n        n *= 2\n    return n\n`],
  ['nneeded', 'test-1', 'h = 1 / n (width not from the interval) with left rule', `${trap('    h = (b - a) / n\n    total = 0.0\n    for i in range(n):\n        total += h * f(a + i * h)\n    return total')}\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, n) - exact) >= tol:\n        n *= 2\n    return n\n`],
  ['nneeded', 'test-3', 'returns the n before', `${TRAP}\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, n) - exact) >= tol:\n        n *= 2\n    return n // 2 if n > 1 else n\n`],
  ['nneeded', 'test-3', 'doubles after the check passes', `${TRAP}\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while True:\n        err = abs(trapezium(f, a, b, n) - exact)\n        n *= 2\n        if err < tol:\n            return n\n`],
  ['nneeded', 'test-3', 'steps n by 1 instead of doubling', `${TRAP}\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, n) - exact) >= tol:\n        n += 1\n    return n\n`],
  ['nneeded', 'test-4', 'starts the search at n = 2', `${TRAP}\ndef n_needed(f, a, b, exact, tol):\n    n = 2\n    while abs(trapezium(f, a, b, n) - exact) >= tol:\n        n *= 2\n    return n\n`],
  ['nneeded', 'test-4', 'doubles before testing', `${TRAP}\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while True:\n        n *= 2\n        if abs(trapezium(f, a, b, n) - exact) < tol:\n            return n\n`],
  ['nneeded', 'test-4', 'do-while: always one doubling', `${TRAP}\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    n *= 2\n    while abs(trapezium(f, a, b, n) - exact) >= tol:\n        n *= 2\n    return n\n`],
  ['nneeded', 'test-8', 'stops when T_2n and T_n agree', `${TRAP}\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, 2 * n) - trapezium(f, a, b, n)) >= tol:\n        n *= 2\n    return n\n`],
  ['nneeded', 'test-8', 'compares with the estimate before, returns the earlier n', `${TRAP}\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    prev = trapezium(f, a, b, 1)\n    while True:\n        n *= 2\n        cur = trapezium(f, a, b, n)\n        if abs(cur - prev) < tol:\n            return n // 2\n        prev = cur\n`],
  ['nneeded', 'any', 'WRONG: relative error against exact', `${TRAP}\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, n) - exact) / abs(exact) >= tol:\n        n *= 2\n    return n\n`],
  ['nneeded', 'any', 'WRONG: successive estimates, returns the finer n', `${TRAP}\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, 2 * n) - trapezium(f, a, b, n)) >= tol:\n        n *= 2\n    return 2 * n\n`],
  ['nneeded', 'any', 'WRONG: signed error (no abs)', `${TRAP}\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while trapezium(f, a, b, n) - exact >= tol:\n        n *= 2\n    return n\n`],
  ['nneeded', 'any', 'WRONG: error <= tol (non-strict)', `${TRAP}\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, n) - exact) > tol:\n        n *= 2\n    return n\n`],
  ['nneeded', 'error', 'syntax error', `${TRAP}\ndef n_needed(f, a, b, exact, tol)\n    return 1\n`],
];

let bad = 0;
const tally = {};
for (const [w, want, label, src] of CASES) {
  const r = await runner.grade(W[w], src, 'tests');
  const got = r.ok ? 'pass' : r.key;
  let verdict;
  if (want === 'none') verdict = r.ok ? 'ok' : 'BAD (correct program refused)';
  else if (want === 'any') verdict = r.ok ? 'NOTE (passes every hidden test)' : 'ok (caught)';
  else {
    const k = `${w}:${want}`; tally[k] = tally[k] || [0, 0]; tally[k][1]++;
    if (got === want) { tally[k][0]++; verdict = 'ok'; } else verdict = `differs (first fails ${got})`;
  }
  if (verdict.startsWith('BAD')) bad++;
  console.log(`${w.padEnd(10)} ${String(want).padEnd(7)} ${String(got).padEnd(7)} ${verdict.padEnd(34)} ${label}`);
}
console.log('\nper line: codings that fail the named test first');
for (const [k, [hit, n]] of Object.entries(tally)) {
  const ok = hit * 2 > n; if (!ok) bad++;
  console.log(`  ${k.padEnd(20)} ${hit}/${n} ${ok ? 'holds' : 'DOES NOT HOLD'}`);
}
await runner.close();
process.exit(bad ? 1 : 0);
