"""Recompute every number in markov homework-2 item hw-absorb-code (performance task, code).

Run from the repo root with a Python that has NumPy and SymPy (the scratchpad venv):
    <venv>/bin/python docs/reports/markov-2-perf-numbers.py     exits 0 when every check passes.
Route A: exact Fractions, Gauss-Jordan on (I - Q) written in this file.
Route B: SymPy's exact inverse, and closed forms for the tennis chain.
Route C: a seeded simulation in this file, sharing no code with the item's solution.
Then the item's solution must pass every test, the starter must fail every test,
and each planted bug must fail at least one hidden test.
"""
import json, math, os, random, sys
from fractions import Fraction as F
import itertools
import numpy as np
import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/markov/homework-2.json')
doc = json.load(open(HW))
item = next(i for i in doc['items'] if i['id'] == 'hw-absorb-code')
w = item['widget']
fails = []
def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)

# ---- the chains, exactly (read from the prelude as decimals, then made exact) ----
ns = {}
exec(w['prelude'], ns)
CH = {k: [[F(str(x)) for x in row] for row in ns[k]] for k in ('WALK', 'TENNIS', 'SIX', 'CYCLE', 'DIRECT', 'STUCK')}
for k, P in CH.items():
    check(f'{k} rows sum to 1', all(sum(r) == 1 for r in P))
    check(f'{k} entries in [0, 1]', all(0 <= x <= 1 for r in P for x in r))

def route_a(P):
    """Gauss-Jordan on (I - Q) | R | 1 in Fractions."""
    n = len(P)
    ends = [i for i in range(n) if P[i][i] == 1]
    mov = [i for i in range(n) if P[i][i] != 1]
    m = len(mov)
    A = [[(F(1) if a == b else F(0)) - P[mov[a]][mov[b]] for b in range(m)]
         + [P[mov[a]][e] for e in ends] + [F(1)] for a in range(m)]
    for c in range(m):
        piv = next(r for r in range(c, m) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(m):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    H = [[F(0)] * n for _ in range(n)]
    t = [F(0)] * n
    for e in ends:
        H[e][e] = F(1)
    for a, i in enumerate(mov):
        for k, e in enumerate(ends):
            H[i][e] = A[a][m + k]
        t[i] = A[a][m + len(ends)]
    return H, t

def route_b(P):
    n = len(P)
    ends = [i for i in range(n) if P[i][i] == 1]
    mov = [i for i in range(n) if P[i][i] != 1]
    H = [[F(0)] * n for _ in range(n)]
    t = [F(0)] * n
    for e in ends:
        H[e][e] = F(1)
    if mov:
        Q = sp.Matrix([[sp.Rational(str(P[i][j])) for j in mov] for i in mov])
        R = sp.Matrix([[sp.Rational(str(P[i][e])) for e in ends] for i in mov])
        N = (sp.eye(len(mov)) - Q).inv()
        B, tt = N * R, N * sp.ones(len(mov), 1)
        for a, i in enumerate(mov):
            t[i] = F(str(tt[a]))
            for k, e in enumerate(ends):
                H[i][e] = F(str(B[a, k]))
    return H, t

EX = {}
for k, P in CH.items():
    A, B = route_a(P), route_b(P)
    check(f'{k} exact routes agree', A == B)
    EX[k] = A
    H, t = A
    check(f'{k} absorption rows sum to 1', all(sum(r) == 1 for r in H))
    # first-step equations hold: h = P h and t = 1 + P t at moving states
    n = len(P)
    for i in range(n):
        if P[i][i] != 1:
            ok = all(H[i][j] == sum(P[i][k] * H[k][j] for k in range(n)) for j in range(n))
            ok = ok and t[i] == 1 + sum(P[i][k] * t[k] for k in range(n))
            check(f'{k} first-step equations at {i}', ok)

# closed forms for tennis: p^2/(p^2+q^2) and 2/(p^2+q^2)
p, q = F(3, 5), F(2, 5)
win = p * p / (p * p + q * q)
dur = 2 / (p * p + q * q)
check('tennis win from deuce 9/13', EX['TENNIS'][0][2][1] == win == F(9, 13))
check('tennis points from deuce 50/13', EX['TENNIS'][1][2] == dur == F(50, 13))
check('adv server 1 + q*t_D = 33/13 and win p + q*9/13 = 57/65', EX['TENNIS'][1][0] == 1 + q * dur == F(33, 13) and EX['TENNIS'][0][0][1] == p + q * win == F(57, 65))
check('adv receiver 1 + p*t_D = 43/13 and win p*9/13 = 27/65', EX['TENNIS'][1][4] == 1 + p * dur == F(43, 13) and EX['TENNIS'][0][4][1] == p * win == F(27, 65))
check('cycle: t0 = 1 + t1, t1 = 1 + 0.9 t0 gives 20 and 19', EX['CYCLE'][1][:2] == [20, 19] and F(20) == 1 + 19 and F(19) == 1 + F(9, 10) * 20)
check('explain decimals 0.692 and 3.85', round(float(win), 3) == 0.692 and round(float(dur), 2) == 3.85)

# ---- route C: seeded simulation, written independently (inverse-CDF by bisect) ----
import bisect
def sim(P, start, runs, seed):
    rng = np.random.default_rng(seed)
    n = len(P)
    cum = [list(itertools.accumulate(float(x) for x in r)) for r in P]
    cnt = [0] * n
    steps = 0
    for _ in range(runs):
        s = start
        while P[s][s] != 1:
            s = min(bisect.bisect_right(cum[s], rng.random()), n - 1)
            steps += 1
        cnt[s] += 1
    return [c / runs for c in cnt], steps / runs
for k, start in [('WALK', 1), ('TENNIS', 2), ('TENNIS', 0), ('SIX', 4), ('SIX', 0), ('CYCLE', 0), ('DIRECT', 0)]:
    shares, mean_steps = sim(CH[k], start, 100000, 11)
    H, t = EX[k]
    err = max(abs(a - float(b)) for a, b in zip(shares, H[start]))
    terr = abs(mean_steps - float(t[start]))
    check(f'simulation {k} from {start}', err < 0.01 and terr < 0.05 * max(1, float(t[start])), f'share err {err:.4f}, steps {mean_steps:.3f} vs {float(t[start]):.4f}')

# ---- every test expectation equals the exact answer ----
def ev(s):
    return eval(s, {})
tests = w['tests']
check('12 tests, 2 examples, examples are tests', len(tests) == 12 and len(w['examples']) == 2 and all(e in tests for e in w['examples']))
check('how says 12 hidden tests and 0.02', '12 hidden tests' in w['how'] and '0.02' in w['how'])
want = {
    'absorb_chances(WALK)': EX['WALK'][0], 'absorb_chances(TENNIS)': EX['TENNIS'][0], 'absorb_chances(SIX)': EX['SIX'][0],
    'absorb_chances(STUCK)': EX['STUCK'][0], 'steps_to_absorb(WALK)': EX['WALK'][1], 'steps_to_absorb(TENNIS)': EX['TENNIS'][1],
    'steps_to_absorb(CYCLE)': EX['CYCLE'][1], 'steps_to_absorb(SIX)': EX['SIX'][1],
    'simulate_absorb(TENNIS, 2, 30000, 1)': EX['TENNIS'][0][2], 'simulate_absorb(SIX, 4, 30000, 5)': EX['SIX'][0][4],
    'simulate_absorb(TENNIS, 1, 10, 3)': EX['TENNIS'][0][1], 'simulate_absorb(DIRECT, 0, 30000, 2)': EX['DIRECT'][0][0],
}
for c in tests:
    exp = ev(c['expect'])
    tgt = want[c['call']]
    flat = lambda v: [x for r in v for x in (r if isinstance(r, list) else [r])]
    check(f"expect of {c['call']}", all(abs(float(a) - float(b)) < 1e-12 for a, b in zip(flat(exp), flat(tgt))) and len(flat(exp)) == len(flat(tgt)))

# a correct sampler fails a 0.02 band with negligible chance: the band is at least 6 standard errors
for c in tests:
    if c.get('tol'):
        runs = int(c['call'].split(',')[2])
        se = max(math.sqrt(float(h) * (1 - float(h)) / runs) for h in ev(c['expect']))
        check(f"band {c['call']} is {0.02 / se:.1f} standard errors", 0.02 / se >= 6)

# ---- run code against the tests, with the engine's compare rules ----
def close(x, y, tol):
    x = x.tolist() if hasattr(x, 'tolist') else x
    y = y.tolist() if hasattr(y, 'tolist') else y
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(a, b, tol) for a, b in zip(x, y))
    try:
        rt, at = (tol.get('rel', 0), tol.get('abs', 0)) if tol else (1e-9, 1e-12)
        return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
    except Exception:
        return False
def run(src):
    res = []
    for c in tests:
        g = {}
        try:
            exec(w['prelude'], g)
            exec(src, g)
            a = eval(c['call'], g)
            e = eval(c['expect'], g)
            res.append(bool(close(a, e, c.get('tol'))))
        except Exception:
            res.append(False)
    return res
r = run(w['solution'])
check('solution passes all 12', all(r), str(r))
r = run(w['starter'])
check('starter fails all 12', not any(r), str(r))

SOL = w['solution']
def variant(old, new):
    assert old in SOL, old
    return SOL.replace(old, new)
BUGS = {
    'absorbing states taken as the last ones': variant(
        "    ends = [i for i in range(len(P)) if P[i, i] == 1]      # absorbing, wherever they sit\n    moving = [i for i in range(len(P)) if P[i, i] != 1]",
        "    k = int(sum(P[i, i] == 1 for i in range(len(P))))\n    ends = list(range(len(P) - k, len(P)))\n    moving = list(range(len(P) - k))"),
    'any self-loop read as absorbing': variant(
        "    ends = [i for i in range(len(P)) if P[i, i] == 1]      # absorbing, wherever they sit\n    moving = [i for i in range(len(P)) if P[i, i] != 1]",
        "    ends = [i for i in range(len(P)) if P[i, i] > 0]\n    moving = [i for i in range(len(P)) if P[i, i] == 0]"),
    'H from R alone (one step)': variant("B = N @ P[np.ix_(moving, ends)]", "B = P[np.ix_(moving, ends)]"),
    'H from Q, not I - Q': variant("np.linalg.inv(np.eye(len(moving)) - P[np.ix_(moving, moving)])", "np.linalg.inv(np.eye(len(moving)) + P[np.ix_(moving, moving)])"),
    'times drop the +1 (Q N 1)': variant("t[moving] = N @ np.ones(len(moving))", "t[moving] = P[np.ix_(moving, moving)] @ N @ np.ones(len(moving))"),
    'absorbing rows left at 0': variant("        H[a, a] = 1.0                                       # already absorbed", "        pass"),
    'simulation returns counts': variant("return [c / runs for c in counts]", "return counts"),
    'simulation draws each entry on its own coin': variant(
        "            u, acc = rng.random(), 0.0\n            for j in range(n):\n                acc += P[s][j]\n                if u < acc:\n                    break\n            s = j",
        "            for j in range(n):\n                if rng.random() < P[s][j]:\n                    break\n            s = j"),
    'simulation stops after 3 steps': variant(
        "        s = start\n        while P[s][s] != 1:",
        "        s = start\n        k = 0\n        while P[s][s] != 1 and k < 3:\n            k += 1"),
}
for name, src in BUGS.items():
    r = run(src)
    failed = [i + 1 for i, x in enumerate(r) if not x]
    check(f'planted bug fails a test: {name}', bool(failed), f'fails tests {failed}')

# homework shape after the change
items = doc['items']
check('homework has 6 to 12 items', 6 <= len(items) <= 12, str(len(items)))
check('one performance item in the level', sum(1 for i in items if i.get('performance')) == 1)
print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
