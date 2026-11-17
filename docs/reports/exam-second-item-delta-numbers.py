"""Delta read of the exam second items that a fix pass replaced or reworked (session AG, task 4).

Scope: the items whose text or numbers were written by a second reader and applied by a fixer,
so nobody but that reader had checked them. Every key, `wrong` value and printed number is
recomputed here by a route that is not the explanation's: exact fractions, enumeration, a
linear solve, a grid scan, numerical integration or a matching. Bands, rounding ties and the
values a learner would type are checked on every numeric widget, part and table cell.
The last block recomputes, for the 17 exams of the task, that every (exam, essential skill)
pair has at least two auto items.

Standard library only. Run from anywhere:
    python3 docs/reports/exam-second-item-delta-numbers.py [--scripts]
`--scripts` also runs the six author and six reader scripts and reports exit code and FINDING lines.
Exit 0 always; a FINDING line is printed for each failing check.
"""
import glob
import itertools
import json
import math
import os
import subprocess
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
CONTENT = os.path.join(ROOT, 'app', 'content')

N_OK = 0
N_BAD = 0


def check(label, cond, detail=''):
    global N_OK, N_BAD
    if cond:
        N_OK += 1
    else:
        N_BAD += 1
        print(f'FINDING {label} {detail}'.rstrip())


def close(a, b, eps=1e-9):
    return abs(a - b) <= eps


def exam(name):
    with open(os.path.join(CONTENT, 'exams', name + '.json'), encoding='utf-8') as fh:
        return json.load(fh)


EXAMS = {}


def item(ex, iid):
    if ex not in EXAMS:
        EXAMS[ex] = exam(ex)
    hit = [i for i in EXAMS[ex]['items'] if i['id'] == iid]
    check(f'{ex} {iid}: item present once', len(hit) == 1)
    return hit[0]


def band(label, w, key, wrongs, typed=None, refused=None):
    """w: a numeric widget or table cell. key: my value. wrongs: {id: my value}.
    typed: values a learner types for a right answer; refused: values that must not pass."""
    tol = w.get('tol', {}).get('abs', 0)
    ans = w['answer']
    check(f'{label}: stored key {ans} is my {key}', abs(ans - key) <= max(tol, 1e-12), f'diff {abs(ans - key):.6g}')
    stored = {x['id']: x for x in w.get('wrong', [])}
    check(f'{label}: wrong ids {sorted(stored)}', sorted(stored) == sorted(wrongs), f'mine {sorted(wrongs)}')
    for wid, val in wrongs.items():
        if wid not in stored:
            continue
        x = stored[wid]
        wt = x.get('tol', {}).get('abs', 0)
        check(f'{label}: wrong {wid} stored {x["value"]} is my {val:.6g}', abs(x['value'] - val) <= max(wt, 1e-12))
        check(f'{label}: wrong {wid} outside the key band', abs(x['value'] - ans) > tol + wt)
    vals = sorted((x['value'], x.get('tol', {}).get('abs', 0)) for x in stored.values())
    for (v1, t1), (v2, t2) in zip(vals, vals[1:]):
        check(f'{label}: wrong bands {v1} and {v2} apart', v2 - v1 > t1 + t2)
    for t in typed or []:
        check(f'{label}: typed {t} is accepted', abs(t - ans) <= tol + 1e-12)
    for t in refused or []:
        check(f'{label}: {t} is refused', abs(t - ans) > tol)


def no_tie(label, value, places):
    """the digit after the asked place is not an exact 5"""
    scaled = F(value).limit_denominator(10 ** 12) * 10 ** places
    frac = scaled - math.floor(scaled)
    check(f'{label}: no rounding tie at {places} places', frac != F(1, 2))


def solve(A, b):
    """Gaussian elimination in fractions; returns None when singular"""
    n = len(A)
    M = [[F(x) for x in row] + [F(v)] for row, v in zip(A, b)]
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return None
        M[c], M[p] = M[p], M[c]
        M[c] = [x / M[c][c] for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                M[r] = [x - M[r][c] * y for x, y in zip(M[r], M[c])]
    return [M[r][n] for r in range(n)]


def rank(M):
    M = [[F(x) for x in row] for row in M]
    r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
    return r


def Phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def text_of(node):
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return ' '.join(text_of(x) for x in node)
    if isinstance(node, dict):
        return ' '.join(text_of(v) for v in node.values())
    return ''


# ---------------------------------------------------------------- topic-1.4
it = item('topic-1.4', 'a-reachable-k')
A = [[1, 2, 1], [2, 5, 3], [1, 4, 3]]
check('reach: prose prints my A and b', '1 & 2 & 1 \\\\ 2 & 5 & 3 \\\\ 1 & 4 & 3' in it['prose'] and '(3, k, 1)' in it['prose'])
ks = [k for k in range(-50, 51) if rank([row + [bv] for row, bv in zip(A, (3, k, 1))]) == rank(A)]
check('reach: rank test over k in -50..50 gives one k', ks == [5], str(ks))
check('reach: A has rank 2', rank(A) == 2)
# slips, by running the wrong row steps on the right-hand side only: b3 after R3 - R1 is 1 - 3 = -2
stale = [k for k in range(-50, 51) if -2 - 2 * k == 0]          # subtracts twice the original k
added = [k for k in range(-50, 51) if -2 + 2 * (k - 6) == 0]    # adds twice row 2
band('reach', it['widget'], 5, {'stale-right': stale[0], 'added-row': added[0]})
check('reach: last row is 10 - 2k', all(1 - 3 - 2 * (k - 6) == 10 - 2 * k for k in range(-5, 6)))
check('reach: b = 3 c1 + c2 - 2 c3', [3 * A[r][0] + A[r][1] - 2 * A[r][2] for r in range(3)] == [3, 5, 1])
check('reach: explain names that combination', '3 times column 1, plus column 2, minus 2 times column 3' in it['explain']['text'])
cols = [[A[r][c] for r in range(3)] for c in range(3)]
check('reach: b is no column and no multiple of one for any k (not read by eye)',
      all(rank([col, [3, k, 1]]) == 2 for col in cols for k in range(-50, 51)))
check('reach: b is no sum or difference of two columns at k = 5',
      all([s * x + t * y for x, y in zip(cols[i], cols[j])] != [3, 5, 1]
          for i in range(3) for j in range(3) if i != j for s in (1, -1) for t in (1, -1)))

it = item('topic-1.4', 'a-qr-solve')
Q = [[F(2, 3), F(2, 3)], [F(-1, 3), F(2, 3)], [F(2, 3), F(-1, 3)]]
R = [[2, -2], [0, 4]]
b = [1, 5, 6]
check('qr: prose prints my Q, R and b', '2 & 2 \\\\ -1 & 2 \\\\ 2 & -1' in it['prose'] and '2 & -2 \\\\ 0 & 4' in it['prose'] and '(1, 5, 6)' in it['prose'])
QtQ = [[sum(Q[r][i] * Q[r][j] for r in range(3)) for j in range(2)] for i in range(2)]
check('qr: Q has orthonormal columns', QtQ == [[1, 0], [0, 1]])
Am = [[sum(Q[r][k] * R[k][c] for k in range(2)) for c in range(2)] for r in range(3)]
AtA = [[sum(Am[r][i] * Am[r][j] for r in range(3)) for j in range(2)] for i in range(2)]
Atb = [sum(Am[r][i] * b[r] for r in range(3)) for i in range(2)]
xhat = solve(AtA, Atb)                      # normal equations on A = QR, not the R route
check('qr: normal equations on A = QR give (2, 1/2)', xhat == [2, F(1, 2)], str(xhat))
Qtb = [sum(Q[r][i] * b[r] for r in range(3)) for i in range(2)]
check('qr: Q^T b = (3, 2)', Qtb == [3, 2])
raw = solve(R, [1, 5])[0]
noback = F(Qtb[0], R[0][0])
unscaled = solve(R, [3 * v for v in Qtb])[0]
band('qr', it['widget'], 2, {'raw-b': float(raw), 'no-back': float(noback), 'unscaled': float(unscaled)})
check('qr: R has a positive diagonal and A has full column rank', R[0][0] > 0 and R[1][1] > 0 and rank(Am) == 2)

it = item('topic-1.4', 'a-desk-lengths')
ax, ay = 5.0, 0.0                           # explicit vectors with the stated lengths and dot product
bx = 28 / 5
by = math.sqrt(144 - bx * bx)
check('desk: vectors with |a| = 5, |b| = 12, a.b = 28 exist', close(math.hypot(bx, by), 12) and close(ax * bx + ay * by, 28))
band('desk', it['widget'], math.hypot(ax + bx, ay + by),
     {'add-lengths': 17, 'no-cross': math.sqrt(169), 'cross-once': math.sqrt(197)}, typed=[15])
x = [w for w in it['widget']['wrong'] if w['id'] == 'cross-once'][0]
check('desk: cross-once typed 14.04 meets its band', abs(14.04 - x['value']) <= x['tol']['abs'])

# ---------------------------------------------------------------- topic-1.3
it = item('topic-1.3', 'c-terms-needed')
check('terms: prose prints 0.3, 10^-5 and 1.35', '|x| \\le 0.3' in it['prose'] and '10^{-5}' in it['prose'] and 'e^{0.3} < 1.35' in it['prose'])
check('terms: e^0.3 < 1.35', math.exp(0.3) < 1.35)


def first_n(bound):
    return next(n for n in range(0, 60) if bound(n) < 1e-5)


lag = lambda n: 1.35 * 0.3 ** (n + 1) / math.factorial(n + 1)
n_key = first_n(lag)
n_last = first_n(lambda n: 0.3 ** n / math.factorial(n))
n_last135 = first_n(lambda n: 1.35 * 0.3 ** n / math.factorial(n))
n_nofact = first_n(lambda n: 1.35 * 0.3 ** (n + 1))
n_nofact1 = first_n(lambda n: 0.3 ** (n + 1))
check('terms: last-kept slip is 6 with or without the 1.35', n_last == n_last135 == 6)
check('terms: no-factorial slip is 9 with or without the 1.35', n_nofact == n_nofact1 == 9)
check('terms: counting terms of T_5 gives 6', len(range(0, 5 + 1)) == 6)
band('terms', it['widget'], n_key, {'last-kept': n_last, 'no-factorial': n_nofact})


def true_err(n):
    worst = 0.0
    for i in range(-300, 301):
        xv = i / 1000
        worst = max(worst, abs(math.exp(xv) - sum(xv ** k / math.factorial(k) for k in range(n + 1))))
    return worst


check('terms: the true worst error at degree 4 is above 10^-5, at degree 5 below (5 is no artefact of the bound)',
      true_err(4) > 1e-5 > true_err(5), f'{true_err(4):.3g} {true_err(5):.3g}')
check('terms: printed 2.7e-5 and 1.4e-6', round(lag(4) * 1e5, 1) == 2.7 and round(lag(5) * 1e6, 1) == 1.4)
check('terms: feedback and explain print those two', all('2.7 \\times 10^{-5}' in s and '1.4 \\times 10^{-6}' in s for s in (it['feedback']['correct'], it['explain']['text'])))

it = item('topic-1.3', 'c-quotient-partial')
f = lambda x, y: F(x) * F(y) ** 2 / (F(x) + F(y))
h = F(1, 10 ** 8)
fy = (f(2, 1 + h) - f(2, 1 - h)) / (2 * h)       # central difference in exact fractions
fx = (f(2 + h, 1) - f(2 - h, 1)) / (2 * h)
check('quot: central difference gives 10/9', abs(fy - F(10, 9)) < F(1, 10 ** 12))
check('quot: partial in x is 1/9', abs(fx - F(1, 9)) < F(1, 10 ** 12))
band('quot', it['widget'], 10 / 9,
     {'swapped': -10 / 9, 'split': (2 * 2 * 1) / 1, 'const-bottom': (2 * 2 * 1) / 3, 'wrong-variable': float(fx)},
     typed=[1.1111, 10 / 9], refused=[1.11])
check('quot: question asks 4 places', 'decimal to 4 places' in it['question'])
no_tie('quot', F(10, 9), 4)

# ---------------------------------------------------------------- topic-1.5
it = item('topic-1.5', 'e-ticket-pair')
pairs = list(itertools.combinations(range(1, 16), 2))
even = [p for p in pairs if sum(p) % 2 == 0]
rows = it['widget']['rows']
check('ticket: prose says 15 tickets, drawn together', 'numbered 1 to 15' in it['prose'] and 'order does not matter' in it['prose'])
band('ticket (a)', rows[0][1], len(pairs), {})
band('ticket (b)', rows[1][1], len(even), {})
check('ticket: ordered count 210 printed', len(list(itertools.permutations(range(1, 16), 2))) == 210 and '210' in it['feedback']['byKey']['r0c1'])
odd = [t for t in range(1, 16) if t % 2]
check('ticket: 8 odd, 7 even, 28 + 21', len(odd) == 8 and math.comb(8, 2) == 28 and math.comb(7, 2) == 21)
check('ticket: explain prints 105, 28, 21, 49', all(s in it['explain']['text'] for s in ('105', '28', '21', '49')))
check('ticket: row labels name one quantity each', 'sample space' in rows[0][0] and 'even sum' in rows[1][0])

it = item('topic-1.5', 'e-coin-again')
joint = {}                                   # (kind, call 1 right, call 2 right) -> chance
for kind, p in (('careful', F(8, 10)), ('careless', F(5, 10))):
    for c1 in (0, 1):
        for c2 in (0, 1):
            joint[(kind, c1, c2)] = F(1, 2) * (p if c1 else 1 - p) * (p if c2 else 1 - p)
p_first = sum(v for (k, c1, c2), v in joint.items() if c1)
p_careful = sum(v for (k, c1, c2), v in joint.items() if c1 and k == 'careful') / p_first
p_second = sum(v for (k, c1, c2), v in joint.items() if c1 and c2) / p_first
check('coin: P(first right) 0.65, posterior 8/13, second 89/130', (p_first, p_careful, p_second) == (F(13, 20), F(8, 13), F(89, 130)))
rows = it['widget']['rows']
band('coin (a)', rows[0][1], float(p_careful), {}, typed=[0.6154], refused=[0.5, 0.8, 0.62])
band('coin (b)', rows[1][1], float(p_second), {}, typed=[0.6846, 0.6154 * 0.8 + 0.3846 * 0.5], refused=[0.65, 0.8, 0.68])
no_tie('coin (a)', p_careful, 4)
no_tie('coin (b)', p_second, 4)
check('coin: prose prints 0.5, 0.8, 0.5 and the first call right', all(s in it['prose'] for s in ('chance 0.5', 'chance 0.8', 'first call is right')))
check('coin: explain prints 0.65, 8/13, 89/130', all(s in it['explain']['text'] for s in ('0.65', '\\tfrac{8}{13}', '\\tfrac{89}{130}', '0.6154', '0.6846')))

it = item('topic-1.5', 'e-fill-times')
sd_mean = 16 / math.sqrt(64)
kk = 5 / sd_mean
rows = it['widget']['rows']
check('fill: Phi(2.5) = 0.9938', round(Phi(2.5), 4) == 0.9938 and '0.9938' in it['prose'])
band('fill (a)', rows[0][1], (16 ** 2 / 64) / 5 ** 2, {}, typed=[0.16], refused=[1 / (5 / 16) ** 2, 0.0124])
band('fill (b)', rows[1][1], 2 * (1 - 0.9938), {}, typed=[0.0124, 2 * (1 - Phi(2.5))], refused=[0.0062, 0.16])
check('fill: k = 2.5', close(kk, 2.5))
check('fill: prose prints 64, 30 ms, 16 ms', all(s in it['prose'] for s in ('64 independent', '30 ms', '16 ms')))

it = item('topic-1.5', 'e-floor-walk')
# unknowns E0, E1, E2; E3 = 0
E = solve([[1, -1, 0], [F(-1, 2), 1, F(-1, 2)], [0, F(-1, 2), 1]], [1, 1, 1])
check('walk: linear solve gives E = (9, 8, 5)', E == [9, 8, 5], str(E))
v = [0.0, 0.0, 0.0, 0.0]
for _ in range(5000):                        # value iteration, a second route
    v = [1 + v[1], 1 + 0.5 * v[0] + 0.5 * v[2], 1 + 0.5 * v[1] + 0.5 * v[3], 0.0]
check('walk: value iteration gives 9', close(v[0], 9, 1e-6))
lost = solve([[1, -1, 0], [F(-1, 2), 1, F(-1, 2)], [0, F(-1, 2), 1]], [0, 1, 1])   # E0 = E1
band('walk', it['widget'], 9, {'straight-up': 3, 'lost-step': float(lost[0]), 'from-one': float(E[1])})
check('walk: no canvas left on the item', 'canvas' not in it and 'drawn below' not in it['prose'])

it = item('topic-1.5', 'e-neither-market')
band('neither', it['widget'], 1 - (F(45, 100) + F(30, 100) - F(12, 100)), {'no-overlap': 0.25, 'union': 0.63})

# ---------------------------------------------------------------- topic-0.3
it = item('topic-0.3', 'e-double-angle-roots')
g = lambda d: math.sin(math.radians(2 * d)) - math.sqrt(3) * math.cos(math.radians(d))
roots = [d / 100 for d in range(0, 36000) if abs(g(d / 100)) < 1e-9]
check('trig: grid scan gives 60, 90, 120, 270', roots == [60.0, 90.0, 120.0, 270.0], str(roots))
signs = sum(1 for d in range(0, 36000) if g((d + 0.5) / 100) * g((d + 1.5) / 100) < 0)
check('trig: four sign changes on the half-step grid, so no root is missed', signs == 4, str(signs))
check('trig: stored answers', sorted(it['widget']['answers']) == [60, 90, 120, 270])
w = {x['id']: sorted(float(s) for s in x['value'].split(',')) for x in it['widget']['wrong']}
check('trig: cos-pair slip is 60, 90, 270, 300', w.get('cos-pair') == [60, 90, 270, 360 - 60])
cosr = [d for d in range(360) if abs(math.cos(math.radians(d)) - math.sqrt(3) / 2) < 1e-9 or abs(math.cos(math.radians(d))) < 1e-9]
check('trig: cos-root slip is 30, 90, 270, 330', w.get('cos-root') == cosr, str(cosr))
check('trig: prose prints the equation and the range', '\\sin 2x = \\sqrt{3}\\cos x' in it['prose'] and '0^\\circ \\le x < 360^\\circ' in it['prose'])

it = item('topic-0.3', 'e-parallelogram-midpoint')
a, c = complex(-4, 2), complex(3, 5)
bpt = a + c
m = (bpt + c) / 2
check('para: B = (-1, 7), M = (1, 6), AM = (5, 4)', (bpt, m, m - a) == (complex(-1, 7), complex(1, 6), complex(5, 4)))
check('para: OABC in order is a parallelogram (AB = OC)', bpt - a == c)
m_bad = ((a - c) + c) / 2
band('para', it['widget'], abs(m - a),
     {'b-minus': abs(m_bad - a), 'om': abs(m), 'no-root': abs(m - a) ** 2}, typed=[6.40, 6.4], refused=[6.5, 6.3])
for x in it['widget']['wrong']:
    val = {'b-minus': abs(m_bad - a), 'om': abs(m), 'no-root': 41.0}[x['id']]
    check(f'para: slip {x["id"]} typed to 2 places meets its band', abs(round(val, 2) - x['value']) <= x['tol']['abs'])
check('para: prose prints (-4, 2) and (3, 5)', '(-4, 2)' in it['prose'] and '(3, 5)' in it['prose'])

it = item('topic-0.3', 'e-desk-meetings')
tri = list(itertools.combinations(range(10), 3))
band('circle', it['widget'], len(tri),
     {'ordered': len(list(itertools.permutations(range(10), 3))), 'third': 720 / 3, 'pairs': len(list(itertools.combinations(range(10), 2)))})
pts = [(math.cos(2 * math.pi * i / 10), math.sin(2 * math.pi * i / 10)) for i in range(10)]
flat = [t for t in tri if abs((pts[t[1]][0] - pts[t[0]][0]) * (pts[t[2]][1] - pts[t[0]][1]) - (pts[t[2]][0] - pts[t[0]][0]) * (pts[t[1]][1] - pts[t[0]][1])) < 1e-12]
check('circle: no three of the points are in line, so every triple is a triangle', not flat)

# ---------------------------------------------------------------- topic-0.2
it = item('topic-0.2', 'e-two-rates')
check('rates: 25,000 x 1.08 x 1.16 = 31,320', F(25000) * F(108, 100) * F(116, 100) == 31320)
grow = lambda r: 25000 * (1 + r) * (1 + 2 * r) - 31320
lo, hi = 0.0, 1.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if grow(mid) < 0 else (lo, mid)
lo2, hi2 = -3.0, -1.0
for _ in range(200):
    mid = (lo2 + hi2) / 2
    lo2, hi2 = (mid, hi2) if grow(mid) > 0 else (lo2, mid)
simple = (31320 / 25000 - 1) / 3
one = math.sqrt(31320 / 25000) - 1
band('rates', it['widget'], lo, {'simple': simple, 'one-rate': one, 'other-root': lo2}, typed=[0.08])
for x in it['widget']['wrong']:
    val = {'simple': simple, 'one-rate': one, 'other-root': lo2}[x['id']]
    check(f'rates: slip {x["id"]} typed as a percentage to 2 places meets its band', abs(round(val * 100, 2) / 100 - x['value']) <= x['tol']['abs'] + 1e-12)
check('rates: discriminant 11.0224 = 3.32^2', F(9) + 8 * F(2528, 10000) == F(110224, 10000) == F(332, 100) ** 2)
check('rates: unit %, over100', it['widget'].get('unit') == '%' and it['widget'].get('over100') is True)
check('rates: -158% leaves a negative balance', 25000 * (1 + lo2) < 0)
check('rates: prose prints the two amounts', '£25,000' in it['prose'] and '£31,320' in it['prose'])

# ---------------------------------------------------------------- topic-3.2
it = item('topic-3.2', 'e-heat-grid-steps')
sig, T, dx = F(35, 100), F(6, 10), F(4, 100)
tau = sig ** 2 * T / 2
p1, p2 = it['parts']
check('heat: prose prints 35%, 0.6 and 0.04', all(s in it['prose'] for s in ('35\\%', 'T = 0.6', '\\Delta x = 0.04')))
band('heat p1', p1['widget'], float(tau), {'no-half': float(sig ** 2 * T), 'sigma-unsquared': float(sig * T / 2), 'calendar': float(T)}, typed=[0.03675])
steps = next(n for n in range(1, 10000) if tau / n / dx ** 2 <= F(1, 2))
steps1 = next(n for n in range(1, 10000) if tau / n / dx ** 2 <= 1)
band('heat p2', p2['widget'], steps, {'lambda-one': steps1, 'round-down': steps - 1})
check('heat: 45.94 and lambda 0.4993, 0.5104', round(float(tau / (dx ** 2 / 2)), 2) == 45.94 and round(float(tau / 46 / dx ** 2), 4) == 0.4993 and round(float(tau / 45 / dx ** 2), 4) == 0.5104)
check('heat: part 2 restates tau', '0.03675' in p2['question'])
# the course turns time round: tau = (1/2) sigma^2 (T - t), so tau is 0 at expiry and 0.03675 today
with open(os.path.join(CONTENT, 'courses', 'pdes', 'l9-black-scholes-to-heat.json'), encoding='utf-8') as fh:
    l9 = fh.read()
check('heat: the course says expiry is tau = 0', 'expiry is $\\\\tau = 0$' in l9)
check('heat: tau at expiry (t = T) is 0 by the item\'s own byKey formula', sig ** 2 * (T - T) / 2 == 0)
check('heat p1: the question does not call the 0.03675 the heat time "at expiry"', 'at expiry' not in p1['question'], repr(p1['question']))
check('heat p2: the question does not say "Heat time at expiry is 0.03675"', 'Heat time at expiry is' not in p2['question'], repr(p2['question'])[:60])
# stability by the scheme itself: the top mode's factor 1 - 4 lambda stays in [-1, 1] at 46 steps and not at 45
check('heat: top mode factor', abs(1 - 4 * float(tau / 46 / dx ** 2)) <= 1 < abs(1 - 4 * float(tau / 45 / dx ** 2)))

# ---------------------------------------------------------------- topic-2.3


def emax(n, steps_=40000, lim=10.0):
    """E[max of n standard normals] = integral of z n phi(z) Phi(z)^(n-1), trapezium rule"""
    tot = 0.0
    hstep = 2 * lim / steps_
    for i in range(steps_ + 1):
        z = -lim + i * hstep
        val = z * n * math.exp(-z * z / 2) / math.sqrt(2 * math.pi) * Phi(z) ** (n - 1)
        tot += val * (0.5 if i in (0, steps_) else 1.0)
    return tot * hstep


it = item('topic-2.3', 'e-honest-bar')
e12, e60 = emax(12), emax(60)
check('bar: best of 12 normals 1.629, best of 60 2.319', round(e12, 3) == 1.629 and round(e60, 3) == 2.319, f'{e12:.5f} {e60:.5f}')
check('bar: prose prints 5 x 12 = 60, 0.84, 0.39, 1.629, 2.319', 5 * 12 == 60 and all(s in it['prose'] for s in ('five futures', '12 settings', '60 runs', '0.84', '0.39', '1.629', '2.319')))
p1, p2 = it['parts']
band('bar p1', p1['widget'], 0.39 * e60, {'one-contract': 0.39 * e12, 'no-scale': e60},
     typed=[0.90, round(0.39 * 2.319, 4)], refused=[0.84, 0.91, 0.89])
x = [w for w in p1['widget']['wrong'] if w['id'] == 'one-contract'][0]
check('bar: one-contract typed 0.64 or 0.6353 meets its band', all(abs(t - x['value']) <= x['tol']['abs'] for t in (0.64, round(0.39 * 1.629, 4))))
opts = {o['id']: o for o in p2['widget']['options']}
check('bar p2: one correct option, a', [k for k, o in opts.items() if o.get('correct')] == ['a'])
check('bar p2: option figures 0.90 and 0.64, and 0.84 is below 0.90 and above 0.64',
      '0.90' in opts['a']['text'] and '0.64' in text_of(p2) and round(0.39 * e12, 2) == 0.64 < 0.84 < round(0.39 * e60, 2) == 0.90)

# ---------------------------------------------------------------- topic-2.6
it = item('topic-2.6', 'e-two-fund-shrink')
mu, tau_h = F(2), F(5, 2)


def post(y, s):                              # precision-weighted mean, not the 1 - B form
    return (F(y) / F(s) ** 2 + mu / tau_h ** 2) / (1 / F(s) ** 2 + 1 / tau_h ** 2)


def slips(y, s):
    B = F(s) ** 2 / (F(s) ** 2 + tau_h ** 2)
    Bl = F(s) / (F(s) + tau_h)
    return {'raw': float(y), 'inverted': float(mu + B * (y - mu)), 'se-not-squared': float(mu + (1 - Bl) * (y - mu))}


pA, pB = post(11, F(15, 2)), post(6, 1)
check('shrink: A 29/10, B 158/29', (pA, pB) == (F(29, 10), F(158, 29)), f'{pA} {pB}')
p1, p2 = it['parts']
band('shrink A', p1['widget'], float(pA), slips(11, F(15, 2)), typed=[2.9])
band('shrink B', p2['widget'], float(pB), slips(6, 1), typed=[5.45, 2 + 0.8621 * 4, 2 + 0.862 * 4])
no_tie('shrink B', pB, 2)
check('shrink: prose prints 2, 2.5, 11, 7.5, 6, 1', all(s in it['prose'] for s in ('\\hat\\mu = 2', '\\hat\\tau = 2.5', '11 bp', '7.5 bp', '6 bp', 'error 1 bp')))
check('shrink: units bp on both parts', p1['widget'].get('unit') == 'bp' == p2['widget'].get('unit'))
check('shrink: B ends with the larger error; A keeps a tenth, B over four fifths', pB > pA and (pA - mu) / 9 == F(1, 10) and (pB - mu) / 4 > F(4, 5))
check('shrink: printed 0.1379 and 0.8621', round(float(1 / (1 + tau_h ** 2)), 4) == 0.1379 and round(float(1 - 1 / (1 + tau_h ** 2)), 4) == 0.8621)
# a right method that keeps B_B to two places (0.14) lands on 5.44
two_place = 2 + (1 - 0.14) * 4
check('shrink B: a working that keeps B_B = 0.14 (5.44) is accepted', abs(two_place - p2['widget']['answer']) <= p2['widget']['tol']['abs'],
      f'5.44 is {abs(two_place - p2["widget"]["answer"]):.4f} from the key, band {p2["widget"]["tol"]["abs"]}')

# ---------------------------------------------------------------- topic-2.1
it = item('topic-2.1', 'e-pd-two-trees')
lines = it['canvas']['params']['lines']
data = [tuple(float(v) for v in ln.split()[1:]) for ln in lines if ln and ln.split()[0] in ('1', '2', '3', '4')]
check('pd: four rows read from the console', data == [(0.2, 0.4), (1.1, 1.6), (-0.6, 0.3), (0.9, 1.3)], str(data))
check('pd: console prints the two trees as I coded them',
      lines[0].split() == ['tree', '1:', 'volume_z', '>', '0.5', '->', '3.0'] and lines[1].split() == ['else', 'gap_z', '>', '1', '->', '2.0']
      and lines[2].split() == ['else', '->', '-1.0'] and lines[3].split() == ['tree', '2:', 'gap_z', '>', '1', '->', '4.0']
      and lines[4].split() == ['else', 'volume_z', '>', '0.5', '->', '1.0'] and lines[5].split() == ['else', '->', '0.0'])
t1 = lambda v, gp: 3.0 if v > 0.5 else (2.0 if gp > 1 else -1.0)
t2 = lambda v, gp: 4.0 if gp > 1 else (1.0 if v > 0.5 else 0.0)
forest = lambda v, gp: (t1(v, gp) + t2(v, gp)) / 2
mean = lambda xs: sum(xs) / len(xs)
pd = lambda v, fn: mean([fn(v, gp) for _, gp in data])
at1 = [forest(1, gp) for _, gp in data]
at0 = [forest(0, gp) for _, gp in data]
check('pd: forecasts at 1 are 2, 3.5, 2, 3.5 and at 0 are -0.5, 3, -0.5, 3', at1 == [2, 3.5, 2, 3.5] and at0 == [-0.5, 3, -0.5, 3])
hi_rows = [forest(v, gp) for v, gp in data if v > 0.5]
lo_rows = [forest(v, gp) for v, gp in data if v <= 0.5]
band('pd', it['widget'], pd(1, forest) - pd(0, forest),
     {'conditional-means': mean(hi_rows) - mean(lo_rows), 'one-tree': pd(1, t1) - pd(0, t1),
      'summed': pd(1, lambda v, gp: t1(v, gp) + t2(v, gp)) - pd(0, lambda v, gp: t1(v, gp) + t2(v, gp))}, typed=[1.5])
check('pd: accept prints 1.25 and 2.75', mean(at0) == 1.25 and mean(at1) == 2.75 and '1.25' in it['widget']['accept'] and '2.75' in it['widget']['accept'])
check('pd: no vol_z left, story is a borrow fee', 'vol_z' not in text_of(it) and 'borrow fee' in it['prose'])
check('pd: tree 2 alone would give 0.5 (not a keyed value, not the key)', close(pd(1, t2) - pd(0, t2), 0.5))

# ---------------------------------------------------------------- topic-3.3
it = item('topic-3.3', 'e-second-price-win')
# exact: payment = highest rival value y when y < 0.6; density of the highest of three uniforms is 3 y^2
pay = 100 * 3 * F(6, 10) ** 4 / 4
check('auction: exact integral gives 243/25 = 9.72', pay == F(243, 25))
Ngrid = 60                                   # a lattice route: rivals on a 60-point midpoint grid in (0, 100)
tot = 0.0
cnt = Ngrid ** 3
for i, j, k in itertools.product(range(Ngrid), repeat=3):
    top = (max(i, j, k) + 0.5) * 100 / Ngrid
    if top < 60:
        tot += top
check('auction: lattice average is 9.72 to 0.05', abs(tot / cnt - 9.72) < 0.05, f'{tot / cnt:.4f}')
p_win = F(6, 10) ** 3
given = pay / p_win
seller = 100 * F(4 - 1, 4 + 1)               # expected second highest of four uniforms on 0 to 100
exante = 100 * F(3, 4) * F(1, 5)             # integral over own value v of v^3 x (3/4) v
band('auction', it['widget'], float(pay), {'given-win': float(given), 'own-bid': float(p_win * 60), 'seller-share': float(seller / 4)}, typed=[9.72])
check('auction: a bidder who does not know their value expects to pay 15, a quarter of the seller 60', exante == 15 == seller / 4 and seller == 60)
check('auction: prose prints four bidders, 0 to 100, value 60', all(s in it['prose'] for s in ('four bidders', '£0 to £100', 'value is £60')))
ss = it['feedback']['byKey']['seller-share']
check('auction: byKey.seller-share says whose £60 it is (expected revenue), apart from the value £60',
      'revenue' in ss or 'expected price' in ss, repr(ss))

it = item('topic-3.3', 'e-alerts-close')
a18, half = F(18, 60), F(1, 2)
closeA = 1 - (1 - a18) ** 2
both = half ** 2 - (half - a18) ** 2
G = 600                                      # midpoint lattice, a second route
c_close = c_both = 0
for i in range(G):
    for j in range(G):
        if abs(i - j) < a18 * G:
            c_close += 1
            if i < G / 2 and j < G / 2:
                c_both += 1
check('alerts: exact 51/100, 21/100, 7/17', (closeA, both, both / closeA) == (F(51, 100), F(21, 100), F(7, 17)))
check('alerts: lattice gives 0.4118 to 0.003', abs(c_both / c_close - 7 / 17) < 0.003, f'{c_both / c_close:.4f}')
band('alerts', it['widget'], 7 / 17,
     {'unconditional': 0.25, 'joint': float(both), 'no-corners': float(F(1, 4) / closeA), 'condition': float(closeA)}, typed=[0.4118], refused=[0.41, 0.4])
no_tie('alerts', F(7, 17), 4)
no_tie('alerts no-corners', F(25, 51), 4)
check('alerts: corner legs 1/5', half - a18 == F(1, 5))

it = item('topic-3.3', 'e-divides-forty')
nums = list(range(11, 41))
adj = {u: [v for v in nums if v > u and v % u == 0] for u in nums}     # comparability, already transitive
match = {}


def aug(u, seen):
    for v in adj[u]:
        if v in seen:
            continue
        seen.add(v)
        if v not in match or aug(match[v], seen):
            match[v] = u
            return True
    return False


msize = sum(1 for u in nums if aug(u, set()))
widest = len(nums) - msize                   # Dilworth: largest antichain = least chain cover
check('divides: largest pair-free set in 11..40 has 20 numbers', widest == 20, str(widest))
check('divides: 21..40 is pair-free', all(b_ % a_ for a_, b_ in itertools.combinations(range(21, 41), 2)))
oddpart = lambda n: n if n % 2 else oddpart(n // 2)
check('divides: 20 odd parts, 1 to 39, all occur', sorted({oddpart(n) for n in nums}) == list(range(1, 40, 2)))
band('divides', it['widget'], widest + 1, {'boxes': widest, 'half': len(nums) // 2 + 1, 'all': len(nums) + 1})
check('divides: prose 11 to 40, question asks the fewest', '11 to 40' in it['prose'] and 'fewest' in it['question'])

it = item('topic-3.3', 'e-bags-any-fake')
takes = [1, 2, 4, 8, 16]
sums = {sum(t for t, on in zip(takes, mask) if on) for mask in itertools.product((0, 1), repeat=5)}
check('bags: 1, 2, 4, 8, 16 give 32 different excesses, 0 to 31', sums == set(range(32)))
best = min(sum(c) for c in itertools.product(range(0, 17), repeat=5)
           if sum(c) <= 31 and len({sum(t for t, on in zip(c, mask) if on) for mask in itertools.product((0, 1), repeat=5)}) == 32)
band('bags', it['widget'], best, {'k-from-k': 15, 'patterns': 32, 'one-each': 5})
check('bags: prose says five large bags', 'Five large bags' in it['prose'])

# ---------------------------------------------------------------- topic-1.6
it = item('topic-1.6', 's-three-traders')
rec = {'kiln': (20, 20), 'loom': (68, 70), 'moss': (252, 270)}
pm = {k: F(27 + s, 30 + n) for k, (s, n) in rec.items()}
check('sellers: posterior means 47/50, 95/100, 279/300', pm == {'kiln': F(47, 50), 'loom': F(95, 100), 'moss': F(279, 300)})
opts = {o['id']: o for o in it['widget']['options']}
check('sellers: one correct option and it is my top', [k for k, o in opts.items() if o.get('correct')] == [max(pm, key=pm.get)])
check('sellers: raw rate picks Kiln, longest record picks Moss, both keyed wrong',
      max(rec, key=lambda k: F(*rec[k])) == 'kiln' and max(rec, key=lambda k: rec[k][1]) == 'moss' and 'why' in opts['kiln'] and 'why' in opts['moss'])
check('sellers: prior mean 90%, worth 30', F(27, 30) == F(9, 10) and 27 + 3 == 30 and 'Beta}(27, 3)' in it['prose'])
check('sellers: prose prints the three records', all(s in it['prose'] for s in ('20 of 20', '68 of 70', '252 of 270')))
check('sellers: printed 0.94, 0.95, 0.93 and Loom raw 97%', [float(pm[k]) for k in ('kiln', 'loom', 'moss')] == [0.94, 0.95, 0.93] and round(68 / 70 * 100) == 97)
check('sellers: explain posteriors', all(s in it['explain']['text'] for s in ('(47, 3)', '(95, 5)', '(279, 21)')))

# ---------------------------------------------------------------- topic-1.7
it = item('topic-1.7', 'e-just-paid')
pv = sum(3.20 * 1.05 ** t / 1.09 ** t for t in range(1, 4000))    # the dividend stream itself
check('paid: summing the stream gives 84.00', abs(pv - 84) < 1e-6, f'{pv:.6f}')
band('paid', it['widget'], pv, {'last-div': 3.20 / 0.04, 'no-growth': 3.36 / 0.09, 'plus-g': 3.36 / 0.14}, typed=[84, 84.00])
x = [w for w in it['widget']['wrong'] if w['id'] == 'no-growth'][0]
check('paid: no-growth typed 37.33 meets its band', abs(37.33 - x['value']) <= x['tol']['abs'])
check('paid: prose prints £3.20, 5%, 9%', all(s in it['prose'] for s in ('£3.20', '5%', '9%')))
check('paid: unit £', it['widget'].get('unit') == '£')

# ---------------------------------------------------------------- topic-1.9
it = item('topic-1.9', 'e-swapped-d')


def bs(S, K, r, sg, T, swap=False, put=False):
    d1 = (math.log(S / K) + (r + sg * sg / 2) * T) / (sg * math.sqrt(T))
    d2 = d1 - sg * math.sqrt(T)
    if put:
        return K * math.exp(-r * T) * Phi(-d2) - S * Phi(-d1)
    if swap:
        d1, d2 = d2, d1
    return S * Phi(d1) - K * math.exp(-r * T) * Phi(d2)


def tests(swap):
    c = bs(100, 100, 0.05, 0.2, 1, swap)
    p = bs(100, 100, 0.05, 0.2, 1, put=True)
    fwd = 100 - 100 * math.exp(-0.05)
    return {'known': abs(c - 10.4506) <= 1e-4, 'parity': abs(c - p - fwd) <= 1e-9, 'bounds': 0 <= c <= 100,
            'limit': abs(bs(100, 100, 0.05, 1e-8, 1, swap) - fwd) <= 1e-6, 'finite': math.isfinite(c)}


check('swap: all five tests pass on the correct pricer', all(tests(False).values()), str(tests(False)))
failing = sorted(k for k, ok in tests(True).items() if not ok)
opts = {o['id']: o for o in it['widget']['options']}
check('swap: options keyed correct are the failing tests', sorted(k for k, o in opts.items() if o.get('correct')) == failing, str(failing))
sw = bs(100, 100, 0.05, 0.2, 1, True)
check('swap: swapped call -4.62, d1 0.35, d2 0.15', round(sw, 2) == -4.62)
check('swap: printed N(0.35), N(0.15), e^-0.05, 10.4506',
      round(Phi(0.35), 6) == 0.636831 and round(Phi(0.15), 6) == 0.559618 and round(math.exp(-0.05), 6) == 0.951229 and round(bs(100, 100, 0.05, 0.2, 1), 4) == 10.4506
      and all(s in it['prose'] for s in ('0.636831', '0.559618', '0.951229', '10.4506')))
check('swap: the printed figures alone give -4.62', round(100 * 0.559618 - 95.123 * 0.636831, 2) == -4.62 and round(100 * 0.559618 - 100 * 0.951229 * 0.636831, 2) == -4.62)

# ---------------------------------------------------------------- reuse: shared sentences with the course


def course_strings(course):
    out = []
    for path in sorted(glob.glob(os.path.join(CONTENT, 'courses', course, '*.json'))):
        if path.endswith('course.json'):
            continue
        with open(path, encoding='utf-8') as fh:
            out.append((os.path.basename(path), fh.read()))
    return out


it = item('topic-2.3', 'e-honest-bar')
q2 = it['parts'][1]['question']
shared = [name for name, txt in course_strings('backtest') if json.dumps(q2, ensure_ascii=False)[1:-1] in txt]
check('bar p2: its question sentence is in no backtest file', not shared, f'"{q2}" is also in backtest/{", ".join(shared)}')

# ---------------------------------------------------------------- pairs: two auto items for every essential skill
TOUCHED = ['topic-0.2', 'topic-0.3', 'topic-0.4', 'topic-1.3', 'topic-1.4', 'topic-1.5', 'topic-1.6', 'topic-1.7', 'topic-1.8',
           'topic-1.9', 'topic-1.10', 'topic-1.11', 'topic-2.1', 'topic-2.3', 'topic-2.6', 'topic-3.2', 'topic-3.3']


def is_auto(itm):
    kinds = [itm.get('kind'), (itm.get('widget') or {}).get('kind')] + [(p.get('widget') or {}).get('kind') for p in itm.get('parts', [])]
    return 'longform' not in kinds


courses = {}
for path in glob.glob(os.path.join(CONTENT, 'courses', '*', 'course.json')):
    with open(path, encoding='utf-8') as fh:
        co = json.load(fh)
    courses[co['id']] = co

total_pairs = 0
short = []
for ex in TOUCHED:
    doc = exam(ex)
    topic = ex.split('-', 1)[1]
    count = {}
    for itm in doc['items']:
        if is_auto(itm):
            for sk in itm.get('skills', []):
                count[sk] = count.get(sk, 0) + 1
    ess = {}
    mine = [co for co in courses.values() if str(co.get('topic')) == topic]
    check(f'pairs {ex}: the topic has a course', bool(mine))
    for co in mine:
        for lv in co['levels']:
            rv = lv.get('review')
            rp = os.path.join(CONTENT, 'courses', co['id'], f'{rv}.json')
            if not rv or not os.path.exists(rp):
                continue
            with open(rp, encoding='utf-8') as fh:
                rdoc = json.load(fh)
            for ri in rdoc.get('items', []):
                for sk in ri.get('skills', []):
                    if sk:
                        ess.setdefault(sk, set()).add(f'{co["id"]}/L{lv["n"]}')
    for sk in sorted(ess):
        total_pairs += 1
        n = count.get(sk, 0)
        if n < 2:
            short.append((ex, sk, n))
        check(f'pairs {ex}: essential skill {sk} has two auto items', n >= 2, f'has {n} ({", ".join(sorted(ess[sk]))})')
    lo_n, hi_n = 20, 36
    check(f'pairs {ex}: item count {len(doc["items"])} within 20 to 36', lo_n <= len(doc['items']) <= hi_n)
print(f'pairs: {total_pairs} (exam, essential skill) pairs over {len(TOUCHED)} exams, {len(short)} under two auto items')

# ---------------------------------------------------------------- the twelve earlier scripts
if '--scripts' in sys.argv:
    for path in sorted(glob.glob(os.path.join(HERE, 'exam-second-item-*-numbers*.py'))):
        if os.path.basename(path) == os.path.basename(__file__):
            continue
        res = subprocess.run([sys.executable, path], capture_output=True, text=True, cwd=ROOT)
        nf = sum(1 for ln in (res.stdout + res.stderr).splitlines() if ln.startswith('FINDING'))
        check(f'script {os.path.basename(path)}: exit 0 and no FINDING line', res.returncode == 0 and nf == 0, f'exit {res.returncode}, {nf} FINDING')
        print(f'script {os.path.basename(path)}: exit {res.returncode}, {nf} FINDING')

print(f'{N_OK} ok, {N_BAD} FINDING')
sys.exit(0)
