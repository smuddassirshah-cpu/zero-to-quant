"""Recompute every number and identity in markov homework-5 item h-build-lazy-martingales
(performance task, derivation).

Run from the repo root with a Python that has SymPy and NumPy (the scratchpad venv):
    <venv>/bin/python docs/reports/markov-5-perf-numbers.py     exits 0 when every check passes.
Route A: SymPy identities for every line of the model.
Route B: exact enumeration in Fractions of the walk's law and of every one-step conditional mean.
Route C: first-step analysis solved exactly, and the no-pause walk's formula.
Route D: seeded simulations of the walk that pauses.
Last, every passing tick set of the rubric is listed and must hold rows 2, 3 and 4.
"""
import itertools, json, math, os, sys
from fractions import Fraction as F
import numpy as np
import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/markov/homework-5.json')
doc = json.load(open(HW))
item = next(i for i in doc['items'] if i['id'] == 'h-build-lazy-martingales')
fails = []
def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)

# ---- route A: symbolic lines ----
p, q, th, y, z, a, b = sp.symbols('p q theta y z a b')
r = 1 - p - q
law = [(1, p), (-1, q), (0, r)]
EX = sp.expand(sum(x * c for x, c in law))
EX2 = sp.expand(sum(x ** 2 * c for x, c in law))
mu, var = p - q, p + q - (p - q) ** 2
check('E[X] = p - q', sp.simplify(EX - mu) == 0)
check('E[X^2] = p + q', sp.simplify(EX2 - (p + q)) == 0)
check('Var(X) = p + q - (p - q)^2', sp.simplify(EX2 - EX ** 2 - var) == 0)
step = sum(c * (y + x - mu) ** 2 for x, c in law)
check('part 1: E[(Y + X - mu)^2] = Y^2 + sigma^2', sp.simplify(step - y ** 2 - var) == 0)
change = sum(c * ((z + x - a) ** 2 - b * (sp.Symbol('n') + 1)) for x, c in law) - (z ** 2 - b * sp.Symbol('n'))
target = 2 * (mu - a) * z + sum(c * (x - a) ** 2 for x, c in law) - b
check('part 1: general a gives change 2(mu - a)Z + E[(X - a)^2] - b', sp.simplify(change - target) == 0)
check('part 1: with a = mu the change is 0 exactly when b = sigma^2', sp.simplify(target.subs(a, mu) - (var - b)) == 0)
check('part 1 check: no pauses gives 4pq', sp.simplify(var.subs(q, 1 - p) - 4 * p * (1 - p)) == 0)
Eth = sum(c * th ** x for x, c in law)
check('part 2: E[theta^X] = p theta + r + q/theta', sp.simplify(Eth - (p * th + r + q / th)) == 0)
check('part 2: theta (E[theta^X] - 1) = (theta - 1)(p theta - q)', sp.expand(th * (Eth - 1) - (th - 1) * (p * th - q)) == 0)
check('part 2: middle line p theta^2 - (p + q) theta + q', sp.expand(p * th ** 2 + (1 - p - q) * th + q - th - (p * th ** 2 - (p + q) * th + q)) == 0)
roots = sp.solve(sp.Eq(Eth, 1), th)
check('part 2: the roots are 1 and q/p', set(sp.simplify(x) for x in roots) == {1, q / p}, str(roots))

# ---- the numbers of part 3 ----
P_, Q_, R_, I0, TOP = F(3, 10), F(2, 10), F(5, 10), 2, 5
T_ = Q_ / P_
check('r = 0.5 and theta = 2/3', R_ == 1 - P_ - Q_ and T_ == F(2, 3))
check('1 - theta^2 = 5/9 and 1 - theta^5 = 211/243', 1 - T_ ** 2 == F(5, 9) and 1 - T_ ** 5 == F(211, 243))
PA = (1 - T_ ** I0) / (1 - T_ ** TOP)
check('route A: P = 135/211', PA == F(135, 211) and F(5, 9) / F(211, 243) == F(135, 211))
check('P is about 0.640', round(float(PA), 3) == 0.640, f'{float(PA):.6f}')
check('p^5 = 0.00243', P_ ** 5 == F(243, 100000))
check('equation P theta^5 + (1 - P) = theta^2 holds', PA * T_ ** 5 + (1 - PA) == T_ ** 2)

# ---- route C: first-step analysis, exactly ----
h = sp.symbols('h1:5')
hh = {0: 0, 5: 1, **{k: h[k - 1] for k in range(1, 5)}}
eqs = [sp.Eq(hh[k], sp.Rational(3, 10) * hh[k + 1] + sp.Rational(2, 10) * hh[k - 1] + sp.Rational(5, 10) * hh[k]) for k in range(1, 5)]
sol = sp.solve(eqs, h)
check('route C: first-step analysis gives h_2 = 135/211', sol[h[1]] == sp.Rational(135, 211), str(sol[h[1]]))
pp = F(3, 5)
check('route C: no-pause walk with up chance 0.6 gives the same', (1 - ((1 - pp) / pp) ** 2) / (1 - ((1 - pp) / pp) ** 5) == PA)
check('first-step rearranges: 0.3/0.5 = 0.6 and 0.2/0.5 = 0.4', P_ / (1 - R_) == F(3, 5) and Q_ / (1 - R_) == F(2, 5))

# ---- route B: exact enumeration of one-step conditional means and of E[M_n] ----
mu_, var_ = P_ - Q_, P_ + Q_ - (P_ - Q_) ** 2
check('mu = 0.1 and sigma^2 = 0.49', mu_ == F(1, 10) and var_ == F(49, 100))
moves = [(1, P_), (-1, Q_), (0, R_)]
dist = {I0: F(1)}
ok1 = ok2 = True
for n in range(0, 12):
    for s in dist:
        m1 = (s - mu_ * n) ** 2 - var_ * n
        nxt1 = sum(c * ((s + x - mu_ * (n + 1)) ** 2 - var_ * (n + 1)) for x, c in moves)
        ok1 &= nxt1 == m1
        nxt2 = sum(c * T_ ** (s + x) for x, c in moves)
        ok2 &= nxt2 == T_ ** s
    new = {}
    for s, c0 in dist.items():
        for x, c in moves:
            new[s + x] = new.get(s + x, F(0)) + c0 * c
    dist = new
check('route B: square martingale fair at every reachable price, n < 12', ok1)
check('route B: power martingale fair at every reachable price, n < 12', ok2)
check('route B: E[(S_12 - 1.2)^2 - 0.49*12] = 4 exactly', sum(c * ((s - mu_ * 12) ** 2 - var_ * 12) for s, c in dist.items()) == 4)
check('route B: E[theta^S_12] = 4/9 exactly', sum(c * T_ ** s for s, c in dist.items()) == F(4, 9))
# a wrong a fails on some history: a = 0
bad = [s for s in range(-1, 4) if sum(c * ((s + x) ** 2 - var_ * 2) for x, c in moves) != s ** 2 - var_ * 1]
check('route B: a = 0 is not fair at n = 1 for any b = sigma^2 (some price breaks it)', bool(bad))
# exact tail P(T > n) against the block bound (1 - p^5)^k
Qm = [[F(0)] * 4 for _ in range(4)]
for k in range(1, 5):
    for x, c in moves:
        j = k + x
        if 1 <= j <= 4:
            Qm[k - 1][j - 1] += c
v = [F(0)] * 4; v[I0 - 1] = F(1)
okb = True
for n in range(1, 101):
    v = [sum(v[i] * Qm[i][j] for i in range(4)) for j in range(4)]
    if n % 5 == 0:
        okb &= sum(v) <= (1 - P_ ** 5) ** (n // 5)
check('exact P(T > 5k) is below (1 - 0.00243)^k for k up to 20', okb, f'P(T > 100) = {float(sum(v)):.2e}')
check('the stopped power martingale stays between theta^5 and 1', all(T_ ** 5 <= T_ ** s <= 1 for s in range(0, 6)))

# ---- route D: seeded simulations ----
rng = np.random.default_rng(20261109)
runs, hits, steps = 200000, 0, 0
for _ in range(runs):
    s = I0
    while 0 < s < TOP:
        u = rng.random()
        s += 1 if u < 0.3 else (-1 if u < 0.5 else 0)
        steps += 1
    hits += s == TOP
est, se = hits / runs, math.sqrt(float(PA) * (1 - float(PA)) / runs)
check('route D: simulated chance of 5 before 0 within 4 standard errors of 135/211', abs(est - float(PA)) < 4 * se, f'{est:.4f} vs {float(PA):.4f}, se {se:.4f}')
X = rng.choice([1, -1, 0], p=[0.3, 0.2, 0.5], size=(200000, 20))
S20 = I0 + X.sum(axis=1)
m1 = (S20 - 0.1 * 20) ** 2 - 0.49 * 20
m2 = (2 / 3) ** S20
check('route D: mean of the square martingale at n = 20 is near 4', abs(m1.mean() - 4) < 4 * m1.std() / math.sqrt(len(m1)), f'{m1.mean():.4f}')
check('route D: mean of the power martingale at n = 20 is near 4/9', abs(m2.mean() - 4 / 9) < 4 * m2.std() / math.sqrt(len(m2)), f'{m2.mean():.4f}')

# ---- the prompt and model state these numbers ----
pr, md = item['prompt'], item['model']
for s in ('p = 0.3', 'q = 0.2', 'i = 2', 'reaches 5 before 0'):
    check(f'prompt states {s}', s in pr)
for s in ('\\tfrac{135}{211} \\approx 0.640', '0.3^5 = 0.00243', '(1 - 0.00243)^k', '\\theta = q/p = \\tfrac23', '\\frac{5/9}{211/243}', '4pq'):
    check(f'model states {s}', s in md)

# ---- rubric: every passing tick set holds rows 2, 3 and 4 ----
rub = item['rubric']
pts = [row['points'] for row in rub]
req = [bool(row.get('required')) for row in rub]
check('rubric sums to 10 with 3 to 5 rows', sum(pts) == 10 and 3 <= len(rub) <= 5)
check('not every row is required', not all(req))
passes = []
for ticks in itertools.product([0, 1], repeat=len(rub)):
    if sum(t * x for t, x in zip(ticks, pts)) >= 7 and all(t for t, rq in zip(ticks, req) if rq):
        passes.append([k + 1 for k, t in enumerate(ticks) if t])
print('passing tick sets:', passes)
check('every pass holds rows 2, 3 and 4 (parts 1, 2 and 3)', passes and all({2, 3, 4} <= set(s) for s in passes))
items = doc['items']
check('homework has 6 to 12 items', 6 <= len(items) <= 12, str(len(items)))
check('one performance item in the level', sum(1 for i in items if i.get('performance')) == 1)
print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
