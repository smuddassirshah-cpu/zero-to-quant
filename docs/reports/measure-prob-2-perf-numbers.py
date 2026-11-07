"""measure-prob L2 performance task h-build-integral: every number in the item, model and rubric, checked twice.
Run: python3 docs/reports/measure-prob-2-perf-numbers.py (sympy optional; the exact Fraction half always runs). Exits 0 when all agree."""
import json, os, sys, math
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'measure-prob', 'homework-2.json')
fails = 0; checks = 0
def ok(cond, what):
    global fails, checks
    checks += 1
    if not cond:
        fails += 1; print('FAIL', what)

closed = lambda N: F((N - 1) * (4 * N + 1), 6 * N * N)
def band_sum(N):          # route A: sum of value times chance over the bands
    return sum((F(k, N) * F((k + 1) ** 2 - k ** 2, N * N) for k in range(N)), F(0)) + 1 * F(0)
def floor_phi(N, u):      # floor(N sqrt(u)) / N exactly, for rational u in [0, 1]: floor(sqrt(x)) = isqrt(floor(x))
    x = F(N * N) * u
    return F(math.isqrt(x.numerator // x.denominator), N)

# 1. band chances (2k+1)/N^2, intervals [k^2/N^2, (k+1)^2/N^2), total 1
for n in range(0, 11):
    N = 2 ** n
    ok(sum((F(2 * k + 1, N * N) for k in range(N)), F(0)) == 1, f'band chances add to 1, n={n}')
    for k in range(min(N, 64)):
        lo, hi = F(k * k, N * N), F((k + 1) ** 2, N * N)
        ok(floor_phi(N, lo) == F(k, N) and (hi == 1 or floor_phi(N, hi) == F(k + 1, N)), f'band {k} interval ends n={n}')
        ok(hi - lo == F(2 * k + 1, N * N), f'band {k} length n={n}')
    ok(floor_phi(N, F(1)) == 1, f'value 1 only at U = 1, n={n}')
    ok(floor_phi(N, F(10**6 - 1, 10**6)) < 1, f'value below 1 just under U = 1, n={n}')

# 2. E[phi_n]: band sum (route A) against the closed form (route B), and a midpoint sum of floor(N sqrt u)/N (route C)
for n in range(0, 13):
    N = 2 ** n
    ok(band_sum(N) == closed(N), f'E[phi_{n}] closed form')
    ok(sum((F(2 * k * k + k) for k in range(N)), F(0)) / N ** 3 == closed(N), f'(1/N^3) sum(2k^2 + k), n={n}')
for n in (1, 2, 3):
    N = 2 ** n; M = 40000
    mid = sum(math.floor(N * math.sqrt((i + 0.5) / M)) / N for i in range(M)) / M
    ok(abs(mid - float(closed(N))) < 2e-4, f'midpoint sum agrees, n={n}')
ok(closed(2) == F(3, 8) and F(1, 2) * F(3, 4) == F(3, 8), 'n = 1 gives 3/8 = 1/2 * 3/4')
ok(closed(8) == F(231, 384) and round(231 / 384, 4) == 0.6016, 'n = 3 gives 231/384 = 0.6016')
for N in range(1, 300):
    ok(sum(k * k for k in range(N)) == (N - 1) * N * (2 * N - 1) // 6 and sum(range(N)) == (N - 1) * N // 2, f'power sums N={N}')

# 3. properties on an exact grid of U: 0 <= phi_n <= X < phi_n + 1/N, and phi_n <= phi_(n+1); 2 floor(y) <= floor(2y)
grid = [F(i, 997) for i in range(998)]
for n in range(0, 9):
    N = 2 ** n
    for u in grid:
        a, b = floor_phi(N, u), floor_phi(2 * N, u)
        ok(a >= 0 and a * a <= u and (a + F(1, N)) ** 2 > u, f'0 <= phi <= X < phi + 1/N, n={n}, u={u}')
        ok(a <= b, f'phi_{n} <= phi_{n+1} at u={u}')
for i in range(-3000, 3000):
    y = F(i, 37)
    ok(2 * math.floor(y) <= math.floor(2 * y), f'2 floor(y) <= floor(2y), y={y}')

# 4. limit 2/3, shortfall (3N+1)/(6N^2), about 2^(-n-1)
for n in range(1, 30):
    N = 2 ** n
    ok(F(2, 3) - closed(N) == F(3 * N + 1, 6 * N * N), f'shortfall n={n}')
    ok(closed(N) < closed(2 * N), f'means increase n={n}')
ok(abs(float(F(2, 3) - closed(2 ** 20)) * 2 ** 21 - 1) < 1e-5, 'shortfall about 2^(-n-1)')
ok(abs(float(closed(2 ** 40)) - 2 / 3) < 1e-11, 'means tend to 2/3')

# 5. E[X] two routes, and Y = 2 sqrt U - 1 by layer cake and by direct integrals, with exact antiderivatives
# layer cake for X: int_0^1 (1 - t^2) dt
ok(1 - F(1, 3) == F(2, 3), 'layer cake 2/3')
ok(F(2, 3) == F(2, 3) * 1, 'int_0^1 sqrt(u) du = 2/3 (antiderivative (2/3) u^(3/2))')
# Y+: int_0^1 1 - (1+t)^2/4 dt = 1 - (8 - 1)/12
ok(F(8 - 1, 12) == F(7, 12) and 1 - F(7, 12) == F(5, 12), 'E[Y+] = 5/12 by layer cake')
# direct: int_{1/4}^1 (2 sqrt u - 1) du = [(4/3) u^(3/2) - u]
G = lambda r: F(4, 3) * r ** 3 - r ** 2     # with u = r^2, u^(3/2) = r^3
ok(G(F(1)) - G(F(1, 2)) == F(5, 12), 'E[Y+] = 5/12 directly')
ok(F(1, 4) - F(4, 3) * F(1, 8) == F(1, 12), 'E[Y-] = 1/12 directly')
ok(F(1, 4) * F(1, 3) == F(1, 12), 'E[Y-] = 1/12 by layer cake')
ok(F(5, 12) - F(1, 12) == F(1, 3) == 2 * F(2, 3) - 1, 'E[Y] = 1/3 = 2(2/3) - 1')
M = 200000
yp = sum(max(2 * math.sqrt((i + .5) / M) - 1, 0) for i in range(M)) / M
ym = sum(max(1 - 2 * math.sqrt((i + .5) / M), 0) for i in range(M)) / M
ok(abs(yp - 5 / 12) < 1e-6 and abs(ym - 1 / 12) < 1e-6, 'midpoint sums for Y+ and Y-')
ok(all(0 <= max(2 * math.sqrt(i / 1000) - 1, 0) <= 1 and 0 <= max(1 - 2 * math.sqrt(i / 1000), 0) <= 1 for i in range(1001)), 'Y+ and Y- lie in [0, 1]')

try:
    import sympy as sp
    t, u = sp.symbols('t u', nonnegative=True); N = sp.symbols('N', positive=True); k = sp.symbols('k', integer=True)
    ok(sp.simplify(sp.summation((k / N) * (2 * k + 1) / N ** 2, (k, 0, N - 1)) - (N - 1) * (4 * N + 1) / (6 * N ** 2)) == 0, 'sympy band sum')
    ok(sp.limit((N - 1) * (4 * N + 1) / (6 * N ** 2), N, sp.oo) == sp.Rational(2, 3), 'sympy limit 2/3')
    ok(sp.simplify(sp.Rational(2, 3) - (N - 1) * (4 * N + 1) / (6 * N ** 2) - (3 * N + 1) / (6 * N ** 2)) == 0, 'sympy shortfall')
    ok(sp.integrate(1 - t ** 2, (t, 0, 1)) == sp.Rational(2, 3) and sp.integrate(sp.sqrt(u), (u, 0, 1)) == sp.Rational(2, 3), 'sympy E[X]')
    ok(sp.integrate((1 + t) ** 2 / 4, (t, 0, 1)) == sp.Rational(7, 12), 'sympy 7/12')
    ok(sp.integrate(1 - (1 + t) ** 2 / 4, (t, 0, 1)) == sp.Rational(5, 12), 'sympy E[Y+] layer cake')
    ok(sp.integrate(2 * sp.sqrt(u) - 1, (u, sp.Rational(1, 4), 1)) == sp.Rational(5, 12), 'sympy E[Y+] direct')
    ok(sp.integrate((1 - t) ** 2 / 4, (t, 0, 1)) == sp.Rational(1, 12), 'sympy E[Y-] layer cake')
    ok(sp.integrate(1 - 2 * sp.sqrt(u), (u, 0, sp.Rational(1, 4))) == sp.Rational(1, 12), 'sympy E[Y-] direct')
    ok(sp.integrate(2 * sp.sqrt(u) - 1, (u, 0, 1)) == sp.Rational(1, 3), 'sympy E[Y] by linearity')
except ImportError:
    print('sympy not found: symbolic half skipped')

d = json.load(open(HW)); items = d['items']
it = [i for i in items if i['id'] == 'h-build-integral']
ok(len(it) == 1, 'one h-build-integral'); it = it[0]
ok(items.index(it) == 9, 'index 9')
ok(it['performance'] == 'derivation' and it['kind'] == 'longform', 'kind')
ok(sum(r['points'] for r in it['rubric']) == 10 and 3 <= len(it['rubric']) <= 5, 'rubric 10 points in 3 to 5 rows')
ok([bool(r.get('required')) for r in it['rubric']].count(True) == 1 and it['rubric'][3].get('required') is True, 'one required row: the limit')
ok(not any(x in it for x in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), 'no scaffold')
ok(sum(1 for i in items if i.get('performance')) == 1 and 6 <= len(items) <= 12 and any(i['difficulty'] == 5 for i in items), 'homework limits')
txt = json.dumps(it, ensure_ascii=False)
ok('—' not in txt and '–' not in txt and '!' not in txt, 'no dashes or exclamation marks')
for s in (r'\tfrac{2k+1}{N^2}', r'\frac{(N-1)(4N+1)}{6N^2}', r'\tfrac38 = 0.375', r'\tfrac{231}{384} \approx 0.6016', r'\tfrac{3N+1}{6N^2}', r'1 - \tfrac{7}{12} = \tfrac{5}{12}', r'E[Y^-] = \tfrac{1}{12}'):
    ok(s in it['model'], 'stated in model: ' + s)
print(f'{checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
