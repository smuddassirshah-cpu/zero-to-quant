// Sweep of feedback.byKey.test-N lines for the integrals L3 code widgets, under the page's Pyodide (code-runner.mjs).
import fs from 'node:fs';
import path from 'node:path';
const APP = process.argv[2], PKGS = process.argv[3];
const { makeRunner } = await import(path.join(APP, 'tools/code-runner.mjs'));
const C = path.join(APP, 'content/courses/integrals');
const l12 = JSON.parse(fs.readFileSync(path.join(C, 'l12-no-formula.json')));
const hw3 = JSON.parse(fs.readFileSync(path.join(C, 'homework-3.json')));
const W = { trap: l12.screens[3].widget, phi: l12.screens[8].widget, need: hw3.items[4].widget };
const T = (body) => `def trapezium(f, a, b, n):\n    h = (b - a) / n\n    total = 0.0\n${body}\n    return total\n`;
const GOODT = T('    for i in range(n):\n        left = a + i * h\n        total += h * (f(left) + f(left + h)) / 2');
const PRE = 'import math\n\n' + GOODT + '\n';
const cases = [
  // l12 s3 trapezium
  ['trap', 'solution', W.trap.solution, null],
  ['trap', 'starter', W.trap.starter, 'test-1'],
  ['trap', 'test-1: range(n+1) extra strip', T('    for i in range(n + 1):\n        left = a + i * h\n        total += h * (f(left) + f(left + h)) / 2'), 'test-1'],
  ['trap', 'test-1: range(n-1) short', T('    for i in range(n - 1):\n        left = a + i * h\n        total += h * (f(left) + f(left + h)) / 2'), 'test-1'],
  ['trap', 'test-1: range(1, n)', T('    for i in range(1, n):\n        left = a + i * h\n        total += h * (f(left) + f(left + h)) / 2'), 'test-1'],
  ['trap', 'left Riemann', T('    for i in range(n):\n        total += h * f(a + i * h)'), 'test-1'],
  ['trap', 'midpoint', T('    for i in range(n):\n        total += h * f(a + (i + 0.5) * h)'), 'test-1'],
  ['trap', 'test-3: composite needing n>=2 (guard)', 'def trapezium(f, a, b, n):\n    h = (b - a) / n\n    if n < 2:\n        return 0.0\n    total = (f(a) + f(b)) / 2\n    for i in range(1, n):\n        total += f(a + i * h)\n    return h * total\n', 'test-3'],
  ['trap', 'test-3: inside-only loop then ends added in loop', 'def trapezium(f, a, b, n):\n    h = (b - a) / n\n    total = 0.0\n    for i in range(1, n):\n        total += f(a + i * h)\n        if i == 1:\n            total += (f(a) + f(b)) / 2\n    return h * total\n', 'test-3'],
  ['trap', 'test-6: edges from 0', T('    for i in range(n):\n        left = i * h\n        total += h * (f(left) + f(left + h)) / 2'), 'test-6'],
  ['trap', 'test-6: h = b / n', 'def trapezium(f, a, b, n):\n    h = b / n\n    total = 0.0\n    for i in range(n):\n        left = a + i * h\n        total += h * (f(left) + f(left + h)) / 2\n    return total\n', 'test-6?'],
  ['trap', 'test-6: abs(left)', T('    for i in range(n):\n        left = abs(a) + i * h\n        total += h * (f(left) + f(left + h)) / 2'), 'test-6'],
  ['trap', 'Jo range(n) points', 'def trapezium(f, a, b, n):\n    h = (b - a) / n\n    xs = [a + i * h for i in range(n)]\n    total = (f(xs[0]) + f(xs[-1])) / 2\n    for x in xs[1:-1]:\n        total += f(x)\n    return h * total\n', 'test-1'],
  ['trap', 'Jo fixed (each point once)', 'def trapezium(f, a, b, n):\n    h = (b - a) / n\n    xs = [a + i * h for i in range(n + 1)]\n    total = (f(xs[0]) + f(xs[-1])) / 2\n    for x in xs[1:-1]:\n        total += f(x)\n    return h * total\n', null],
  // l12 s8 phi / prob_within
  ['phi', 'solution', W.phi.solution, null],
  ['phi', 'starter', W.phi.starter, 'test-1'],
  ['phi', 'test-1: no sqrt', PRE + 'def phi(x):\n    return math.exp(-x * x / 2) / (2 * math.pi)\n\ndef prob_within(z, n):\n    return trapezium(phi, -z, z, n)\n', 'test-1'],
  ['phi', 'test-1: sqrt(pi) only', PRE + 'def phi(x):\n    return math.exp(-x * x / 2) / math.sqrt(math.pi)\n\ndef prob_within(z, n):\n    return trapezium(phi, -z, z, n)\n', 'test-1'],
  ['phi', 'test-1: sqrt(2)*pi', PRE + 'def phi(x):\n    return math.exp(-x * x / 2) / (math.sqrt(2) * math.pi)\n\ndef prob_within(z, n):\n    return trapezium(phi, -z, z, n)\n', 'test-1'],
  ['phi', 'exp(-x^2) no half', PRE + 'def phi(x):\n    return math.exp(-x * x) / math.sqrt(2 * math.pi)\n\ndef prob_within(z, n):\n    return trapezium(phi, -z, z, n)\n', 'test-2'],
  ['phi', 'test-4: 0 to z', PRE + 'def phi(x):\n    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)\n\ndef prob_within(z, n):\n    return trapezium(phi, 0, z, n)\n', 'test-4'],
  ['phi', 'test-4: -inf-ish (-10) to z', PRE + 'def phi(x):\n    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)\n\ndef prob_within(z, n):\n    return trapezium(phi, -10, z, n)\n', 'test-4'],
  ['phi', 'test-4: 2 * (0 to z), n strips', PRE + 'def phi(x):\n    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)\n\ndef prob_within(z, n):\n    return 2 * trapezium(phi, 0, z, n)\n', 'test-4'],
  ['phi', 'error: phi() called', PRE + 'def phi(x):\n    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)\n\ndef prob_within(z, n):\n    return trapezium(phi(), -z, z, n)\n', 'error'],
  // hw3 i4
  ['need', 'solution', W.need.solution, null],
  ['need', 'starter', W.need.starter, 'test-1'],
  ['need', 'test-1: range(n+1)', T('    for i in range(n + 1):\n        left = a + i * h\n        total += h * (f(left) + f(left + h)) / 2') + '\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, n) - exact) >= tol:\n        n *= 2\n    return n\n', 'test-1'],
  ['need', 'test-1: left sum', T('    for i in range(n):\n        total += h * f(a + i * h)') + '\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, n) - exact) >= tol:\n        n *= 2\n    return n\n', 'test-1'],
  ['need', 'test-4: start at n = 2', GOODT + '\ndef n_needed(f, a, b, exact, tol):\n    n = 2\n    while abs(trapezium(f, a, b, n) - exact) >= tol:\n        n *= 2\n    return n\n', 'test-4'],
  ['need', 'test-4: double before test', GOODT + '\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while True:\n        n *= 2\n        if abs(trapezium(f, a, b, n) - exact) < tol:\n            return n\n', 'test-4'],
  ['need', 'test-4: do-while returning doubled n', GOODT + '\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    err = abs(trapezium(f, a, b, n) - exact)\n    while True:\n        n *= 2\n        if err < tol:\n            return n\n        err = abs(trapezium(f, a, b, n) - exact)\n', 'test-3/4'],
  ['need', 'test-3: returns previous n', GOODT + '\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, n) - exact) >= tol:\n        n *= 2\n    return n // 2 if n > 1 else 1\n', 'test-3'],
  ['need', 'test-3: stops one early (tests 2n ahead... tol*4)', GOODT + '\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, n) - exact) >= 4 * tol:\n        n *= 2\n    return n\n', 'test-3'],
  ['need', 'test-3: stop when successive estimates agree', GOODT + '\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, 2 * n) - trapezium(f, a, b, n)) >= tol:\n        n *= 2\n    return n\n', 'test-3'],
  ['need', 'no abs (signed error)', GOODT + '\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while trapezium(f, a, b, n) - exact >= tol:\n        n *= 2\n    return n\n', 'test-6'],
  ['need', 'n += 1 instead of doubling', GOODT + '\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, n) - exact) >= tol:\n        n += 1\n    return n\n', 'test-3'],
  ['need', '<= tol stop (equivalent here)', GOODT + '\ndef n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, n) - exact) > tol:\n        n *= 2\n    return n\n', null],
];
const runner = await makeRunner({ pkgs: PKGS, root: APP, jobs: 1 });
for (const [w, name, src, expect] of cases) {
  const r = await runner.grade(W[w], src, 'tests', {});
  console.log(`${w} | ${name} | key=${r.key} ok=${r.ok} | expected ${expect}`);
}
await runner.close();
