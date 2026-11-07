"""measure-prob L1 performance task h-build-space: every number in the item, model and rubric, checked twice.
Run: python3 docs/reports/measure-prob-1-perf-numbers.py (sympy optional; the Fraction half always runs). Exits 0 when all agree."""
import json, os, random, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'measure-prob', 'homework-1.json')
fails = 0; checks = 0
def ok(cond, what):
    global fails, checks
    checks += 1
    if not cond:
        fails += 1; print('FAIL', what)

p = lambda k: F(1, k * (k + 1))
# 1. p_k = 1/k - 1/(k+1), and the partial sums telescope to 1 - 1/(m+1)
for k in range(1, 500):
    ok(p(k) == F(1, k) - F(1, k + 1), f'p_{k} splits')
s = F(0)
for m in range(1, 500):
    s += p(m)
    ok(s == 1 - F(1, m + 1), f'partial sum m={m}')          # route A: running sum
    ok(F(m, m + 1) == 1 - F(1, m + 1), f'closed form m={m}')  # route B: m/(m+1)
ok(1 - s < F(1, 499), 'partial sums approach 1')

# 2. P(T_n) = 1/n by the complement and by the increasing sets {n..m}
for n in range(1, 60):
    comp = sum((p(k) for k in range(1, n)), F(0))
    ok(1 - comp == F(1, n), f'P(T_{n}) by complement')
    ok(comp == 1 - F(1, n), f'P(1..n-1) = 1 - 1/n, n={n}')
    for m in range(n, n + 40):
        ok(sum((p(k) for k in range(n, m + 1)), F(0)) == F(1, n) - F(1, m + 1), f'P(n..m) n={n} m={m}')
# decreasing T_n with P(T_1) = 1 and limit 0; increasing {1..n} rising to 1
ok(all(F(1, n + 1) < F(1, n) for n in range(1, 1000)), 'P(T_n) decreases')
ok(F(1, 10**9) < F(1, 10**8), 'P(T_n) -> 0')
ok(sum((p(k) for k in range(1, 2)), F(0)) == F(1, 2), 'P({1}) = 1/2')
# every k leaves T_{k+1}: the intersection of T_1..T_N inside 1..N is empty
ok(all(not all(k >= n for n in range(1, k + 2)) for k in range(1, 1000)), 'each k leaves T_(k+1), so the intersection is empty')

# 3. countable additivity on finite instances (brute force) and on infinite partitions (tails bounded)
random.seed(1)
for _ in range(300):
    pts = list(range(1, 60)); random.shuffle(pts)
    cuts = sorted(random.sample(range(1, 59), 4))
    parts = [pts[a:b] for a, b in zip([0] + cuts, cuts + [59])]
    whole = sum((p(k) for k in pts), F(0))
    ok(sum((sum((p(k) for k in q), F(0)) for q in parts), F(0)) == whole, 'finite additivity')
# residue classes mod r: truncated sums to K plus the tail bound P(T_{K+1}) = 1/(K+1)
for r in (2, 3, 5):
    K = 4000
    tot = sum(sum(1.0 / (k * (k + 1)) for k in range(c, K + 1, r)) for c in range(1, r + 1))
    ok(abs(tot - (1 - 1 / (K + 1))) < 1e-12, f'mod {r} classes add to P(1..K)')
    ok(abs(1 - tot) <= 1 / (K + 1) + 1e-12, f'mod {r} tail within 1/(K+1)')

# 4. sympy route
try:
    import sympy as sp
    k, m, n = sp.symbols('k m n', integer=True, positive=True)
    ok(sp.simplify(sp.apart(1 / (k * (k + 1)), k) - (1 / k - 1 / (k + 1))) == 0, 'sympy partial fractions')
    ok(sp.simplify(sp.summation(1 / (k * (k + 1)), (k, 1, m)) - (1 - 1 / (m + 1))) == 0, 'sympy telescoping sum')
    ok(sp.summation(1 / (k * (k + 1)), (k, 1, sp.oo)) == 1, 'sympy P(Omega) = 1')
    ok(sp.simplify(sp.summation(1 / (k * (k + 1)), (k, n, sp.oo)) - 1 / n) == 0, 'sympy P(T_n) = 1/n')
    ok(sp.limit(1 / n, n, sp.oo) == 0, 'sympy limit 0')
    j = sp.symbols('j', integer=True, positive=True)
    ev = sp.N(sp.Sum(1 / (2 * j * (2 * j + 1)), (j, 1, sp.oo)), 30); od = sp.N(sp.Sum(1 / ((2 * j - 1) * 2 * j), (j, 1, sp.oo)), 30)
    ok(abs(ev - (1 - sp.log(2))) < 1e-25 and abs(od - sp.log(2)) < 1e-25, 'sympy evens 1 - ln 2, odds ln 2')
    ok(abs(ev + od - 1) < 1e-25, 'sympy evens + odds = 1 (countable additivity on a partition)')
except ImportError:
    print('sympy not found: symbolic half skipped')

# 5. the item: shape, rubric and homework limits
d = json.load(open(HW)); items = d['items']
it = [i for i in items if i['id'] == 'h-build-space']
ok(len(it) == 1, 'one h-build-space'); it = it[0]
ok(items.index(it) == 8, 'index 8')
ok(it['performance'] == 'derivation' and it['kind'] == 'longform', 'kind')
ok(sum(r['points'] for r in it['rubric']) == 10, 'rubric sums to 10')
ok(3 <= len(it['rubric']) <= 5, 'rubric 3 to 5 rows')
ok([bool(r.get('required')) for r in it['rubric']].count(True) == 1, 'one required row')
ok(it['rubric'][2].get('required') is True, 'continuity from below is the required row')
ok(not any(x in it for x in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), 'no scaffold')
ok(sum(1 for i in items if i.get('performance')) == 1, 'one task in the homework')
ok(6 <= len(items) <= 12 and any(i['difficulty'] == 5 for i in items), 'homework limits')
txt = json.dumps(it, ensure_ascii=False)
ok('—' not in txt and '–' not in txt and '!' not in txt, 'no dashes or exclamation marks')
ok('tfrac{1}{k(k+1)}' in txt and r'\tfrac1n' in it['model'] and r'1 - \tfrac{1}{m+1}' in it['model'], 'stated forms present')
print(f'{checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
