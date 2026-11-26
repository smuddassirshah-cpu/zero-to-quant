// Code-widget sweep for integrals L3 (audit integrals-1-3-r2). Run: node sweep.mjs <app dir> <pkgs>
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const app = process.argv[2], pkgs = process.argv[3];
const { makeRunner } = await import(pathToFileURL(path.join(app, 'tools/code-runner.mjs')).href);
const runner = makeRunner({ pkgs, root: app, jobs: 2 });
const C = path.join(app, 'content/courses/integrals');
const l12 = JSON.parse(fs.readFileSync(path.join(C, 'l12-no-formula.json')));
const hw3 = JSON.parse(fs.readFileSync(path.join(C, 'homework-3.json')));
const W1 = l12.screens[3].widget, W2 = l12.screens[8].widget, W3 = hw3.items[4].widget;
const TR = `def trapezium(f, a, b, n):
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        left = a + i * h
        total += h * (f(left) + f(left + h)) / 2
    return total
`;
const pre2 = 'import math\n\n' + TR + '\n';
const cases = [
  // ---- l12 screens[3] trapezium ----
  [W1, 't1 too few strips range(n-1)', `def trapezium(f, a, b, n):
    h = (b - a) / n
    total = 0.0
    for i in range(n - 1):
        left = a + i * h
        total += h * (f(left) + f(left + h)) / 2
    return total
`, 'test-1'],
  [W1, 't1 too many strips range(n+1)', `def trapezium(f, a, b, n):
    h = (b - a) / n
    total = 0.0
    for i in range(n + 1):
        left = a + i * h
        total += h * (f(left) + f(left + h)) / 2
    return total
`, 'test-1'],
  [W1, 't1 range(1,n)', `def trapezium(f, a, b, n):
    h = (b - a) / n
    total = 0.0
    for i in range(1, n):
        left = a + i * h
        total += h * (f(left) + f(left + h)) / 2
    return total
`, 'test-1'],
  [W1, 't3 points form, n=1 special (inner loop only, ends forgotten when n==1)', `def trapezium(f, a, b, n):
    h = (b - a) / n
    if n == 1:
        return 0.0
    total = (f(a) + f(b)) / 2
    for i in range(1, n):
        total += f(a + i * h)
    return h * total
`, 'test-3'],
  [W1, 't3 loop while i < n-1 then add last strip only if n>1', `def trapezium(f, a, b, n):
    h = (b - a) / n
    total = 0.0
    i = 0
    while i < n - 1:
        left = a + i * h
        total += h * (f(left) + f(left + h)) / 2
        i += 1
    if n > 1:
        left = a + (n - 1) * h
        total += h * (f(left) + f(left + h)) / 2
    return total
`, 'test-3'],
  [W1, 't6 edges from 0', `def trapezium(f, a, b, n):
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        left = i * h
        total += h * (f(left) + f(left + h)) / 2
    return total
`, 'test-6'],
  [W1, 't6 h = b/n', `def trapezium(f, a, b, n):
    h = b / n
    total = 0.0
    for i in range(n):
        left = a + i * h
        total += h * (f(left) + f(left + h)) / 2
    return total
`, 'test-6?'],
  [W1, 't6 xs from 0 in points form', `def trapezium(f, a, b, n):
    h = (b - a) / n
    xs = [i * h for i in range(n + 1)]
    total = (f(xs[0]) + f(xs[-1])) / 2
    for x in xs[1:-1]:
        total += f(x)
    return h * total
`, 'test-6'],
  [W1, 'wrong: left Riemann', `def trapezium(f, a, b, n):
    h = (b - a) / n
    return sum(h * f(a + i * h) for i in range(n))
`, 'any fail'],
  [W1, 'wrong: midpoint', `def trapezium(f, a, b, n):
    h = (b - a) / n
    return sum(h * f(a + (i + 0.5) * h) for i in range(n))
`, 'any fail'],
  [W1, 'wrong: no halving', `def trapezium(f, a, b, n):
    h = (b - a) / n
    return sum(h * (f(a + i * h) + f(a + (i + 1) * h)) for i in range(n))
`, 'any fail'],
  [W1, 'correct: points form', `def trapezium(f, a, b, n):
    h = (b - a) / n
    total = (f(a) + f(b)) / 2
    for i in range(1, n):
        total += f(a + i * h)
    return h * total
`, 'pass'],
  [W1, 'error: NameError', `def trapezium(f, a, b, n):
    h = (b - a) / n
    return h * totl
`, 'error?'],
  // ---- l12 screens[8] phi / prob_within ----
  [W2, 't1 no sqrt', pre2 + `def phi(x):
    return math.exp(-x * x / 2) / (2 * math.pi)

def prob_within(z, n):
    return trapezium(phi, -z, z, n)
`, 'test-1'],
  [W2, 't1 sqrt(2)*pi', pre2 + `def phi(x):
    return math.exp(-x * x / 2) / (math.sqrt(2) * math.pi)

def prob_within(z, n):
    return trapezium(phi, -z, z, n)
`, 'test-1'],
  [W2, 't1 sqrt(pi) only', pre2 + `def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(math.pi)

def prob_within(z, n):
    return trapezium(phi, -z, z, n)
`, 'test-1'],
  [W2, 'no /2 in exponent (no line: test 2 expected)', pre2 + `def phi(x):
    return math.exp(-x * x) / math.sqrt(2 * math.pi)

def prob_within(z, n):
    return trapezium(phi, -z, z, n)
`, 'test-2 (no byKey line)'],
  [W2, 'precedence -x**2/2 ok', pre2 + `def phi(x):
    return math.exp(-x**2 / 2) / math.sqrt(2 * math.pi)

def prob_within(z, n):
    return trapezium(phi, -z, z, n)
`, 'pass'],
  [W2, '(-x)**2 sign lost: exp(+x^2/2)?', pre2 + `def phi(x):
    return math.exp((-x)**2 / 2) / math.sqrt(2 * math.pi)

def prob_within(z, n):
    return trapezium(phi, -z, z, n)
`, 'test-2 (no line)'],
  [W2, 't4 from 0 to z', pre2 + `def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)

def prob_within(z, n):
    return trapezium(phi, 0, z, n)
`, 'test-4'],
  [W2, 't4 phi(z) called', pre2 + `def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)

def prob_within(z, n):
    return trapezium(phi(z), -z, z, n)
`, 'test-4'],
  [W2, 't4 symmetric doubling 2*T(0,z,n) (correct maths, different h)', pre2 + `def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)

def prob_within(z, n):
    return 2 * trapezium(phi, 0, z, n)
`, 'test-4 (maths right, spec differs)'],
  [W2, 't4 limits swapped z to -z', pre2 + `def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)

def prob_within(z, n):
    return trapezium(phi, z, -z, n)
`, 'test-4'],
  [W2, 'wrong: ignores n (fixed 1000)', pre2 + `def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)

def prob_within(z, n):
    return trapezium(phi, -z, z, 1000)
`, 'any fail'],
  [W2, 'wrong: erf closed form', pre2 + `def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)

def prob_within(z, n):
    return math.erf(z / math.sqrt(2))
`, 'any fail'],
  // ---- homework-3 items[4] n_needed ----
  [W3, 't1 range(n-1)', `def trapezium(f, a, b, n):
    h = (b - a) / n
    total = 0.0
    for i in range(n - 1):
        left = a + i * h
        total += h * (f(left) + f(left + h)) / 2
    return total

def n_needed(f, a, b, exact, tol):
    n = 1
    while abs(trapezium(f, a, b, n) - exact) >= tol:
        n *= 2
    return n
`, 'test-1'],
  [W3, 't1 h=(b-a)/(n+1)', `def trapezium(f, a, b, n):
    h = (b - a) / (n + 1)
    total = 0.0
    for i in range(n):
        left = a + i * h
        total += h * (f(left) + f(left + h)) / 2
    return total

def n_needed(f, a, b, exact, tol):
    n = 1
    while abs(trapezium(f, a, b, n) - exact) >= tol:
        n *= 2
    return n
`, 'test-1'],
  [W3, 't4 start at n=2', TR + `
def n_needed(f, a, b, exact, tol):
    n = 2
    while abs(trapezium(f, a, b, n) - exact) >= tol:
        n *= 2
    return n
`, 'test-4'],
  [W3, 't4 double before testing', TR + `
def n_needed(f, a, b, exact, tol):
    n = 1
    while True:
        n *= 2
        if abs(trapezium(f, a, b, n) - exact) < tol:
            return n
`, 'test-4'],
  [W3, 't4 do-while style returns doubled n', TR + `
def n_needed(f, a, b, exact, tol):
    n = 1
    err = abs(trapezium(f, a, b, n) - exact)
    while True:
        n *= 2
        if err < tol:
            return n
        err = abs(trapezium(f, a, b, n) - exact)
`, 'test-3 or 4'],
  [W3, 't3 returns previous n (n//2)', TR + `
def n_needed(f, a, b, exact, tol):
    n = 1
    while abs(trapezium(f, a, b, n) - exact) >= tol:
        n *= 2
    return max(1, n // 2)
`, 'test-3'],
  [W3, 't3 stops at <= 2*tol? (error within tol*2)', TR + `
def n_needed(f, a, b, exact, tol):
    n = 1
    while abs(trapezium(f, a, b, n) - exact) / 2 >= tol:
        n *= 2
    return n
`, 'test-3'],
  [W3, 't3 relative error instead of absolute', TR + `
def n_needed(f, a, b, exact, tol):
    n = 1
    while abs(trapezium(f, a, b, n) - exact) / abs(exact) >= tol:
        n *= 2
    return n
`, 'test-3'],
  [W3, 't3 n += 1 search (smallest n, not power of 2)', TR + `
def n_needed(f, a, b, exact, tol):
    n = 1
    while abs(trapezium(f, a, b, n) - exact) >= tol:
        n += 1
    return n
`, 'test-3'],
  [W3, 'no abs (signed error)', TR + `
def n_needed(f, a, b, exact, tol):
    n = 1
    while trapezium(f, a, b, n) - exact >= tol:
        n *= 2
    return n
`, 'test-6 (no line)'],
  [W3, 't8 successive, returns coarser n', TR + `
def n_needed(f, a, b, exact, tol):
    n = 1
    while abs(trapezium(f, a, b, 2 * n) - trapezium(f, a, b, n)) >= tol:
        n *= 2
    return n
`, 'test-8'],
  [W3, 't8 successive, returns finer n', TR + `
def n_needed(f, a, b, exact, tol):
    n = 1
    prev = trapezium(f, a, b, n)
    while True:
        n *= 2
        cur = trapezium(f, a, b, n)
        if abs(cur - prev) < tol:
            return n
        prev = cur
`, 'test-8 (or 4 first)'],
  [W3, 't8 Richardson-style |T2n-Tn|/3 < tol, returns 2n', TR + `
def n_needed(f, a, b, exact, tol):
    n = 1
    while abs(trapezium(f, a, b, 2 * n) - trapezium(f, a, b, n)) / 3 >= tol:
        n *= 2
    return 2 * n
`, 'test-8 (or 4 first)'],
  [W3, 'wrong: <= tol in place of < tol', TR + `
def n_needed(f, a, b, exact, tol):
    n = 1
    while abs(trapezium(f, a, b, n) - exact) > tol:
        n *= 2
    return n
`, 'pass (boundary untested)'],
];
for (const [spec, name, src, expect] of cases) {
  const r = await runner.grade(spec, src, 'tests');
  console.log(`${r.ok ? 'PASS' : 'FAIL'} key=${r.key} | expect ${expect} | ${name}`);
}
await runner.close();
