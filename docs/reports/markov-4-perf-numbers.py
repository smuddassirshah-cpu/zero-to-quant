"""Recompute every number in markov homework-4 item h-mh-network (performance task, code).

Run from the repo root with a Python that has NumPy and SymPy (the scratchpad venv):
    <venv>/bin/python docs/reports/markov-4-perf-numbers.py     exits 0 when every check passes.
Route A: the Metropolis-Hastings matrix built in Fractions in this file, checked for
pi P = pi and detailed balance exactly. Route B: SymPy's null space of P^T - I, which must
be one-dimensional (the stationary law is unique) and spanned by the weights.
Route C: a seeded simulation in this file (NumPy generator), sharing no code with the solution.
Then the solution passes every test, the starter fails every test, each planted bug fails one.
"""
import json, math, os, sys
from fractions import Fraction as F
import numpy as np
import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/markov/homework-4.json')
doc = json.load(open(HW))
item = next(i for i in doc['items'] if i['id'] == 'h-mh-network')
w = item['widget']
fails = []
def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)

ns = {}
exec(w['prelude'], ns)
NETS = {'PATH3': (3, ns['PATH3'], [1, 1, 1]), 'STAR': (4, ns['STAR'], [1, 1, 2, 3]), 'KITE': (5, ns['KITE'], ns['KW']),
        'TWO': (2, [(0, 1)], [1, 3]), 'KITE-flat': (5, ns['KITE'], [1] * 5)}

def route_a(n, edges, wt):
    deg = [sum((u == i) + (v == i) for u, v in edges) for i in range(n)]
    P = [[F(0)] * n for _ in range(n)]
    for u, v in edges:
        for i, j in ((u, v), (v, u)):
            P[i][j] = F(1, deg[i]) * min(F(1), F(wt[j] * deg[i], wt[i] * deg[j]))
    for i in range(n):
        P[i][i] = 1 - sum(P[i][j] for j in range(n) if j != i)
    return P

def connected(n, edges):
    seen, todo = {0}, [0]
    while todo:
        x = todo.pop()
        for u, v in edges:
            for a, b in ((u, v), (v, u)):
                if a == x and b not in seen:
                    seen.add(b); todo.append(b)
    return len(seen) == n

EX = {}
for k, (n, e, wt) in NETS.items():
    P = route_a(n, e, wt)
    EX[k] = P
    pi = [F(x, sum(wt)) for x in wt]
    check(f'{k}: connected, no self-links, links once', connected(n, e) and all(u != v for u, v in e) and len({frozenset(x) for x in e}) == len(e))
    check(f'{k}: entries in [0, 1], rows sum to 1', all(0 <= x <= 1 for r in P for x in r) and all(sum(r) == 1 for r in P))
    check(f'{k}: detailed balance exactly', all(pi[i] * P[i][j] == pi[j] * P[j][i] for i in range(n) for j in range(n)))
    check(f'{k}: pi P = pi exactly', all(sum(pi[i] * P[i][j] for i in range(n)) == pi[j] for j in range(n)))
    M = sp.Matrix([[sp.Rational(str(P[i][j])) for j in range(n)] for i in range(n)])
    null = (M.T - sp.eye(n)).nullspace()
    ok = len(null) == 1
    if ok:
        v = null[0] / sum(null[0])
        ok = all(F(str(v[j])) == pi[j] for j in range(n))
    check(f'{k}: null space of P^T - I is one line, spanned by the weights', ok)
# plain Metropolis (no degree ratio) does not target the weights on the star and the kite
for k in ('STAR', 'KITE'):
    n, e, wt = NETS[k]
    deg = [sum((u == i) + (v == i) for u, v in e) for i in range(n)]
    Pb = [[F(0)] * n for _ in range(n)]
    for u, v in e:
        for i, j in ((u, v), (v, u)):
            Pb[i][j] = F(1, deg[i]) * min(F(1), F(wt[j], wt[i]))
    for i in range(n):
        Pb[i][i] = 1 - sum(Pb[i][j] for j in range(n) if j != i)
    M = sp.Matrix([[sp.Rational(str(Pb[i][j])) for j in range(n)] for i in range(n)])
    v = (M.T - sp.eye(n)).nullspace()[0]; v = v / sum(v)
    gap = max(abs(float(v[j]) - wt[j] / sum(wt)) for j in range(n))
    check(f'{k}: plain Metropolis is off target by more than 0.05', gap > 0.05, f'max gap {gap:.4f}, law {[str(x) for x in v]}')
# the explain's identity w_i P_ij = min(w_i/deg i, w_j/deg j)
n, e, wt = NETS['KITE']
deg = [sum((u == i) + (v == i) for u, v in e) for i in range(n)]
check('explain: w_i P_ij = min(w_i/deg(i), w_j/deg(j)) on every kite link',
      all(wt[i] * EX['KITE'][i][j] == min(F(wt[i], deg[i]), F(wt[j], deg[j])) for u, v in e for i, j in ((u, v), (v, u))))
check('star entries 1/3, 1/6, 1/9 back to the hub', [EX['STAR'][j][0] for j in (1, 2, 3)] == [F(1, 3), F(1, 6), F(1, 9)])

# ---- route C: an independent seeded simulation ----
def sim(n, edges, wt, start, steps, seed):
    rng = np.random.default_rng(seed)
    nb = [[b for u, v in edges for a, b in ((u, v), (v, u)) if a == i] for i in range(n)]
    x, cnt = start, np.zeros(n)
    for _ in range(steps):
        y = nb[x][int(rng.integers(len(nb[x])))]
        if rng.random() * wt[x] * len(nb[y]) < wt[y] * len(nb[x]):
            x = y
        cnt[x] += 1
    return cnt / steps
for k, start in (('STAR', 1), ('KITE', 4), ('TWO', 0)):
    n, e, wt = NETS[k]
    s = sim(n, e, wt, start, 200000, 7)
    gap = max(abs(s[j] - wt[j] / sum(wt)) for j in range(n))
    check(f'simulation {k} from {start}: shares near the weights', gap < 0.01, f'max gap {gap:.4f}')

# ---- tests against the exact answers ----
tests = w['tests']
check('11 tests, 1 example, the example is a test', len(tests) == 11 and len(w['examples']) == 1 and w['examples'][0] in tests)
check('how says 11 hidden tests, 100,000 steps, 0.04', '11 hidden tests' in w['how'] and '100,000' in w['how'] and '0.04' in w['how'])
def flat(v):
    return [x for r in v for x in (r if isinstance(r, (list, tuple)) else [r])]
mats = {0: 'PATH3', 1: 'STAR', 2: 'KITE', 5: 'KITE', 6: 'TWO'}
for idx, k in mats.items():
    exp = eval(tests[idx]['expect'], {})
    check(f'test {idx + 1} expect equals the exact {k} matrix', [F(x).limit_denominator(1000) for x in flat(exp)] == flat(EX[k]))
for idx, k in ((8, 'STAR'), (9, 'KITE')):
    exp = eval(tests[idx]['expect'], {})
    n, e, wt = NETS[k]
    check(f'test {idx + 1} expect equals the normalised weights', [F(x).limit_denominator(1000) for x in exp] == [F(x, sum(wt)) for x in wt])

# ---- run code against the tests with the engine's compare rules ----
def close(x, y, tol):
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(a, b, tol) for a, b in zip(x, y))
    try:
        rt, at = (tol.get('rel', 0), tol.get('abs', 0)) if tol else (1e-9, 1e-12)
        return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
    except Exception:
        return x == y
def run(src, cases=tests):
    res = []
    for c in cases:
        g = {}
        try:
            exec(w['prelude'], g); exec(src, g)
            a = eval(c['call'], g); e = eval(c['expect'], g)
            res.append(bool(close(a, e, c.get('tol'))) if c['compare'] == 'isclose' else bool(a == e))
        except Exception:
            res.append(False)
    return res
r = run(w['solution']); check('solution passes all 11', all(r), str(r))
r = run(w['starter']); check('starter fails all 11', not any(r), str(r))

# the 0.02 band against the spread of a correct run: 40 seeds of the solution's own sampler
g = {}; exec(w['prelude'], g); exec(w['solution'], g)
for idx, (k, start) in ((8, ('STAR', 1)), (9, ('KITE', 4))):
    n, e, wt = NETS[k]
    errs = np.array([np.array(g['mh_network_shares'](n, e, wt, start, 100000, s)) - np.array(wt) / sum(wt) for s in range(100, 140)])
    sd = errs.std(axis=0).max()
    check(f'test {idx + 1}: band 0.04 is at least 6 standard deviations of a correct run', 0.04 / sd >= 6, f'sd {sd:.4f}, band {0.04 / sd:.1f} sd, worst of 40 seeds {abs(errs).max():.4f}')

SOL = w['solution']
def variant(old, new):
    assert old in SOL, old
    return SOL.replace(old, new)
BUGS = {
    'plain Metropolis, no degree ratio': variant("return min(1, (w[j] * len(nb[i])) / (w[i] * len(nb[j])))", "return min(1, w[j] / w[i])"),
    'degree ratio upside down': variant("return min(1, (w[j] * len(nb[i])) / (w[i] * len(nb[j])))", "return min(1, (w[j] * len(nb[j])) / (w[i] * len(nb[i])))"),
    'no min, ratio used as a chance': variant("return min(1, (w[j] * len(nb[i])) / (w[i] * len(nb[j])))", "return (w[j] * len(nb[i])) / (w[i] * len(nb[j]))"),
    'rejections not put on the diagonal': variant("        P[i][i] = 1 - sum(P[i][j] for j in range(n) if j != i)   # rejections stay\n", ""),
    'links one way only': variant("        nb[v].append(u)\n", ""),
    'proposal over every venue': variant("            P[i][j] = _accept(nb, w, i, j) / len(nb[i])", "            P[i][j] = _accept(nb, w, i, j) / (n - 1)"),
    'shares drop rejected steps': variant("        if rng.random() < _accept(nb, w, x, y):\n            x = y\n        visits[x] += 1                   # a rejected step is a visit too",
                                          "        if rng.random() < _accept(nb, w, x, y):\n            x = y\n            visits[x] += 1\n    steps = max(1, sum(visits))"),
    'shares sampler without the Hastings ratio': variant("        if rng.random() < _accept(nb, w, x, y):", "        if rng.random() < min(1, w[y] / w[x]):"),
    'shares returns counts': variant("return [v / steps for v in visits]", "return visits"),
}
for name, src in BUGS.items():
    r = run(src)
    failed = [i + 1 for i, x in enumerate(r) if not x]
    check(f'planted bug fails a test: {name}', bool(failed), f'fails tests {failed}')

# the share bugs miss by far more than the band on every seed, so their failure is not luck
for name in ('shares drop rejected steps', 'shares sampler without the Hastings ratio'):
    gb = {}; exec(w['prelude'], gb); exec(BUGS[name], gb)
    worst = []
    for k, start in (('STAR', 1), ('KITE', 4)):
        n, e, wt = NETS[k]
        gaps = [max(abs(a - b / sum(wt)) for a, b in zip(gb['mh_network_shares'](n, e, wt, start, 100000, s), wt)) for s in range(10)]
        worst.append(min(gaps))
    check(f'{name}: smallest miss over 10 seeds is above 0.08 on the star or the kite', max(worst) > 0.08, f'star {worst[0]:.3f}, kite {worst[1]:.3f}')

items = doc['items']
check('homework has 6 to 12 items', 6 <= len(items) <= 12, str(len(items)))
check('one performance item in the level', sum(1 for i in items if i.get('performance')) == 1)
print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
