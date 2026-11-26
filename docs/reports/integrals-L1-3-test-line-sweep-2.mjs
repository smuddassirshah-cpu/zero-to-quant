import fs from 'node:fs'; import path from 'node:path';
const APP = process.argv[2], PKGS = process.argv[3];
const { makeRunner } = await import(path.join(APP, 'tools/code-runner.mjs'));
const C = path.join(APP, 'content/courses/integrals');
const l12 = JSON.parse(fs.readFileSync(path.join(C, 'l12-no-formula.json')));
const hw3 = JSON.parse(fs.readFileSync(path.join(C, 'homework-3.json')));
const W = l12.screens[8].widget, N = hw3.items[4].widget, T0 = l12.screens[3].widget;
const sol = W.solution;
const cases = [
 ['phi() brackets', W, sol.replace('trapezium(phi, -z, z, n)', 'trapezium(phi(), -z, z, n)')],
 ['syntax error', W, sol.replace('return trapezium(phi, -z, z, n)', 'return trapezium(phi, -z, z, n')],
 ['no import math (NameError in phi)', W, sol.replace('import math\n', '')],
 ['phi(x) passed', W, sol.replace('trapezium(phi, -z, z, n)', 'trapezium(phi(x), -z, z, n)')],
 ['trap: divide by zero in loop', T0, T0.solution.replace('/ 2', '/ 0')],
 ['trap: indentation error', T0, T0.solution.replace('        left = a', '      left = a')],
];
const runner = await makeRunner({ pkgs: PKGS, root: APP, jobs: 1 });
for (const [name, w, src] of cases) { const r = await runner.grade(w, src, 'tests', {}); console.log(name, '| key=' + r.key, '| error=' + JSON.stringify(r.error).slice(0,120), '| rows=' + JSON.stringify(r.rows).slice(0,200)); }
const N2 = JSON.parse(JSON.stringify(N)); N2.tests = [{ call: 'n_needed(lambda x: x**2, 0, 1, 1/3, 1.5e-4)', expect: 64, compare: 'equal' }];
const good = N.solution;
const succ = good.replace(/def n_needed[\s\S]*$/, 'def n_needed(f, a, b, exact, tol):\n    n = 1\n    while abs(trapezium(f, a, b, 2 * n) - trapezium(f, a, b, n)) >= tol:\n        n *= 2\n    return n\n');
for (const [name, src] of [['solution on proposed test', good], ['successive-estimates on proposed test', succ]]) { const r = await runner.grade(N2, src, 'tests', {}); console.log(name, '| key=' + r.key, 'ok=' + r.ok); }
await runner.close();
