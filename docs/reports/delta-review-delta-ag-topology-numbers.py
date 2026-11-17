"""Delta read review-delta-ag-topology: the four re-authored problems of topology
problems-2 and -3 (p-signal-bands, p-kernel-equation, p-trapping-interval,
p-coin-paths) and the parts the fix pass changed on the kept problems.

Imports no earlier script; standard library only. Routes: every subset, family
and subspace of the three-point and four-point spaces by brute force; the
integral operator applied on a grid by the trapezium rule, next to exact
Fractions; bisection and plain iteration for the trapping interval; paths as
0/1 tuples with Fractions for the coin space; bisection and the quadratic
formula for the cube part. Each numeric band is rebuilt with the engine's rule
(|typed - key| <= abs) and fed the figure the part's own working prints.

Exit 0 always. A failing check prints `FAIL`; a finding of the review prints a
`FINDING` line while the content is as the review describes and `resolved`
once it is fixed.
"""
import json
import math
import os
import random
from fractions import Fraction as Fr
from itertools import combinations, permutations, product

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
TOP = os.path.join(ROOT, 'app', 'content', 'courses', 'topology')
N = [0, 0]


def check(name, cond):
    N[0] += 1
    if not cond:
        N[1] += 1
        print('FAIL', name)


def finding(n, open_, text):
    print(('FINDING %d: ' % n if open_ else 'resolved %d: ' % n) + text)


def load(n):
    return json.load(open(os.path.join(TOP, 'problems-%d.json' % n), encoding='utf-8'))


def item(d, i):
    return [x for x in d['items'] if x['id'] == i][0]


def texts(part):
    fb = part['feedback']
    out = [part['question'], fb['correct'], fb['generic'], part['explain']['text']] + list(fb.get('byKey', {}).values())
    for o in part['widget'].get('options', []):
        out += [o['text'], o.get('why', '')]
    return ' '.join(out)


def numeric(tag, part, key, wrongs, places=None, printed=()):
    """key and wrong values against mine; bands by the engine's rule."""
    w = part['widget']
    check(tag + ' kind', w['kind'] == 'numeric')
    tol = w['tol']['abs']
    check(tag + ' key %r' % key, abs(w['answer'] - float(key)) <= 1e-9)
    got = {x['id']: x for x in w.get('wrong', [])}
    check(tag + ' wrong ids', set(got) == set(wrongs))
    check(tag + ' byKey ids', set(part['feedback'].get('byKey', {})) == set(wrongs))
    bands = [(float(key) - tol, float(key) + tol)]
    for k, v in wrongs.items():
        if k not in got:
            continue
        check(tag + ' wrong %s = %r' % (k, v), abs(got[k]['value'] - float(v)) <= 1e-9)
        wt = got[k]['tol']['abs']
        check(tag + ' wrong %s refused by the key' % k, abs(float(v) - float(key)) > tol)
        bands.append((float(v) - wt, float(v) + wt))
    for (a, b), (c, e) in combinations(bands, 2):
        check(tag + ' bands apart', b < c or e < a)
    if places is not None:
        typed = round(float(key), places)
        check(tag + ' key at %d places taken' % places, abs(typed - float(key)) <= tol)
        frac = abs(float(key)) * 10 ** places % 1
        check(tag + ' key off a rounding tie', abs(frac - 0.5) > 1e-3)
        check(tag + ' form stated', 'decimal places' in part['question'])
    elif not float(key).is_integer():
        check(tag + ' form stated', 'exact fraction' in part['question'])
    for s in printed:
        check(tag + ' prints %s' % s, s in texts(part))


# ---------------------------------------------------------------- set 2: p-signal-bands
P2 = load(2)
sg = item(P2, 'p-signal-bands')
check('signal difficulty', sg['difficulty'] == 4)
LO, HI = 98, 102
if '$x < 60$' in sg['prose']:
    LO, HI = 60, 64
S = ('sell', 'hold', 'buy')


def f(x):
    return 'sell' if x < LO else ('hold' if x <= HI else 'buy')


def subsets(xs):
    xs = list(xs)
    return [frozenset(c) for r in range(len(xs) + 1) for c in combinations(xs, r)]


def pre_open(W):
    # the preimage is a union of the three bands; test every point of a fine grid for a small ball inside it
    e = 1e-6
    for x in [LO - 5 + 0.25 * k for k in range(4 * (HI - LO + 10) + 1)]:
        if f(x) in W and not (f(x - e) in W and f(x + e) in W):
            return False
    return True


tau = [W for W in subsets(S) if pre_open(W)]
check('signal: tau', set(tau) == {frozenset(), frozenset({'sell'}), frozenset({'buy'}), frozenset({'sell', 'buy'}), frozenset(S)})
numeric('signal part 1', sg['parts'][0], 5, {'all-subsets': 8, 'no-ends': 3}, printed=[': 5 sets', 'leaves 5 sets'])
check('signal part 1 key by count', len(tau) == 5)
check('signal part 1: with hold, open only for S', [W for W in tau if 'hold' in W] == [frozenset(S)])


def is_top(fam, X):
    fam = set(fam)
    if frozenset() not in fam or frozenset(X) not in fam:
        return False
    return all((a | b) in fam and (a & b) in fam for a in fam for b in fam)


mid = [W for W in subsets(S) if 0 < len(W) < 3]
all_tops = [set(c) | {frozenset(), frozenset(S)} for r in range(7) for c in combinations(mid, r)]
all_tops = [t for t in all_tops if is_top(t, S)]
check('29 topologies on three points', len(all_tops) == 29)
inside = [t for t in all_tops if t <= set(tau)]
numeric('signal part 2', sg['parts'][1], len(inside), {'all-choices': 8, 'tau-only': 1, 'all-topologies': 29}, printed=['So 7', '2^3 = 8', '7 topologies'])
check('signal part 2 key 7', len(inside) == 7)
tmid = [W for W in tau if 0 < len(W) < 3]
bad = [set(c) | {frozenset(), frozenset(S)} for r in range(4) for c in combinations(tmid, r)]
bad = [t for t in bad if not is_top(t, S)]
check('signal part 2: one family of the 8 fails, the two singletons without their union',
      len(bad) == 1 and bad[0] == {frozenset(), frozenset(S), frozenset({'sell'}), frozenset({'buy'})})
# continuity of f into (S, sigma) is exactly sigma inside tau
check('signal part 2: continuous iff inside tau', all((t <= set(tau)) == all(pre_open(W) for W in t) for t in all_tops))


def connected(A, top):
    sub_ = {U & A for U in top}
    return not any(U and V and not (U & V) and (U | V) == A for U in sub_ for V in sub_)


nonempty = [A for A in subsets(S) if A]
conn = [A for A in nonempty if connected(A, tau)]
numeric('signal part 3', sg['parts'][2], len(conn), {'all': 7, 'singletons': 3, 'no-pairs': 4}, printed=[': 6', '6 of the 7'])
check('signal part 3 key 6', len(conn) == 6 and [A for A in nonempty if A not in conn] == [frozenset({'sell', 'buy'})])
check('signal part 3 slip no-pairs = singletons + S', 3 + 1 == 4)
opts = {o['id']: o for o in sg['parts'][3]['widget']['options']}
check('signal part 4 one correct option', [k for k, o in opts.items() if o.get('correct')] == ['connected-image'])
check('signal part 4: connected subsets with sell and buy', [A for A in conn if {'sell', 'buy'} <= A] == [frozenset(S)])
check('signal part 4: f not continuous into discrete', not pre_open(frozenset({'hold'})))
check('signal part 4: S connected, constant map not onto', connected(frozenset(S), tau))
check('signal part 4: ends', f(LO - 1) == 'sell' and f(HI + 2) == 'buy')

# kept problems of set 2: the parts the fix pass changed
fp = item(P2, 'p-four-point-line')
X4 = 'abcd'
basis = [frozenset('a'), frozenset('c'), frozenset('abc'), frozenset('cd')]
t4 = {frozenset().union(*c) for r in range(5) for c in combinations(basis, r)}
check('four-point: tau is a topology', is_top(t4, X4))
numeric('four-point part 1', fp['parts'][0], len(t4), {'pieces-only': 4, 'no-empty': 7, 'all-subsets': 16})
check('four-point part 1 key 8', len(t4) == 8)
check('four-point part 1 question as the review gave it', fp['parts'][0]['question'] == r'Count the sets of $\tau$, the empty set among them.')
cut = [x for x in X4 if not connected(frozenset(X4) - {x}, t4)]
check('four-point: cut points b, c', cut == ['b', 'c'])
homeo = [p for p in permutations(X4) if {frozenset(p[X4.index(x)] for x in U) for U in t4} == t4]
numeric('four-point part 4', fp['parts'][3], len(homeo), {'reversal': 2, 'every-bijection': 24})
check('four-point part 4 key 1', len(homeo) == 1)
check('four-point part 4 defines cut points', 'Call $b$ and $c$ the cut points' in fp['parts'][3]['question'])
gd = item(P2, 'p-gapped-domain')
numeric('gapped part 2', gd['parts'][1], 3, {'joined': 2, 'one': 1})
check('gapped part 2 defines component', 'A component of $Y$ is a largest connected subset.' in gd['parts'][1]['question'])
check('gapped part 2 no longer lists the pieces', r'\{4\}' not in gd['parts'][1]['question'])
# forced values: union of [-1, 2], [-3, 1] and {5}; length by a grid of 1/100
cells = sum(1 for k in range(-1000, 1000) if any(a <= k / 100 and (k + 1) / 100 <= b for a, b in ((-1, 2), (-3, 1), (5, 5))))
numeric('gapped part 4', gd['parts'][3], Fr(cells, 100), {'one-interval': 8, 'added': 7})
check('gapped part 4 key 5', cells == 500)
rr = item(P2, 'p-right-rays')
A_sup = max(2, 5)                         # sup of (1, 2) u {5}: the smallest closed ray (-inf, t] holding it has t = 5
numeric('right-rays part 1', rr['parts'][0], A_sup, {'ignore-point': 2})
# largest ray (t, inf) inside [3, 8] u (10, inf): smallest t on a grid with the ray inside B


def inB(x):
    return 3 <= x <= 8 or x > 10


ts = [k / 10 for k in range(0, 200)]
good = [t for t in ts if all(inB(t + j / 20) for j in range(1, 400))]
numeric('right-rays part 2', rr['parts'][1], min(good), {'usual': 3, 'closed-end': 8})
check('right-rays parts 1 and 2 give the definitions',
      'the closure of a set is the smallest closed set holding it' in rr['parts'][0]['question']
      and 'the interior of a set is the largest open set inside it' in rr['parts'][1]['question'])

# ---------------------------------------------------------------- set 3
P3 = load(3)
check('set 3: one problem of difficulty 5', [x['difficulty'] for x in P3['items']].count(5) >= 1)
check('set 3: four problems', [x['id'] for x in P3['items']] == ['p-kernel-equation', 'p-trapping-interval', 'p-coin-paths', 'p-cube-delta'])

# p-kernel-equation: T(f)(x) = 1 + (x/2) int_0^1 t f(t) dt
ke = item(P3, 'p-kernel-equation')
GRID = [k / 2000 for k in range(2001)]


def integ(vals):
    h = GRID[1] - GRID[0]
    return h * (sum(vals) - 0.5 * (vals[0] + vals[-1]))


def Tk(fv):
    I = integ([t * v for t, v in zip(GRID, fv)])
    return [1 + x / 2 * I for x in GRID]


def dsup(a, b):
    return max(abs(u - v) for u, v in zip(a, b))


random.seed(7)
ratios = []
for _ in range(200):
    c1 = [random.uniform(-3, 3) for _ in range(4)]
    c2 = [random.uniform(-3, 3) for _ in range(4)]
    f1 = [c1[0] + c1[1] * x + c1[2] * math.sin(5 * x) + c1[3] * x * x for x in GRID]
    f2 = [c2[0] + c2[1] * x + c2[2] * math.cos(7 * x) + c2[3] * x ** 3 for x in GRID]
    ratios.append(dsup(Tk(f1), Tk(f2)) / dsup(f1, f2))
check('kernel part 1: no pair beats 1/4', max(ratios) <= 0.25 + 1e-6)
one, zero = [1.0] * len(GRID), [0.0] * len(GRID)
check('kernel part 1: f - g = 1 attains 1/4', abs(dsup(Tk(one), Tk(zero)) - 0.25) < 1e-6)
numeric('kernel part 1', ke['parts'][0], Fr(1, 4), {'no-t': Fr(1, 2), 'x-averaged': Fr(1, 8)}, printed=[r'q = \tfrac14'])
# fixed point: c = (1/2)(1/2 + c/3) by Fractions, and by iterating T on the grid
c = Fr(1, 4) / (1 - Fr(1, 6))
check('kernel part 2: c = 3/10', c == Fr(3, 10))
fv = one
for _ in range(40):
    fv = Tk(fv)
check('kernel part 2: iterates reach 1 + 0.3x', dsup(fv, [1 + 0.3 * x for x in GRID]) < 1e-6)
numeric('kernel part 2', ke['parts'][1], c, {'one-step': Fr(1, 4), 'no-t': Fr(1, 2) / (1 - Fr(1, 4)), 'no-square': Fr(1, 4) / (1 - Fr(1, 4))},
        printed=[r'c = \tfrac{3}{10}', r'\tfrac14 + \tfrac{c}{6}'])
f1v = Tk(one)
check('kernel part 3: f_1 = 1 + x/4', dsup(f1v, [1 + x / 4 for x in GRID]) < 1e-6)
err = dsup(f1v, [1 + 0.3 * x for x in GRID])
numeric('kernel part 3', ke['parts'][2], Fr(1, 20), {'at-half': Fr(1, 40), 'added': Fr(11, 20)}, printed=[r'\tfrac{1}{20} = 0.05'])
check('kernel part 3 by the grid', abs(err - 0.05) < 1e-6)
q = Fr(1, 4)
move = Fr(1, 4)
bound = q / (1 - q) * move
check('kernel part 4: first move 1/4 on the grid', abs(dsup(f1v, one) - 0.25) < 1e-6)
check('kernel part 4: bound 1/12 holds', bound == Fr(1, 12) and Fr(1, 20) < bound)
numeric('kernel part 4', ke['parts'][3], bound / Fr(1, 20),
        {'no-denominator': q * move / Fr(1, 20), 'inverted': Fr(1, 20) / bound, 'over-one-minus': move / (1 - q) / Fr(1, 20)},
        printed=[r'\tfrac{1}{12}', r'\tfrac53', r'\tfrac{1}{16}'])
check('kernel part 4: 1/(1-q) d bounds d(f_0, f*) = 0.3', Fr(3, 10) <= move / (1 - q))
check('kernel part 4: two thirds too large', bound / Fr(1, 20) - 1 == Fr(2, 3))

# p-trapping-interval: T(x) = 0.2 e^x on [-r, r]
tr = item(P3, 'p-trapping-interval')


def T(x):
    return 0.2 * math.exp(x)


def g(r):
    return (1 - 0.2 * math.exp(r)) * r - 0.2


w1 = tr['parts'][0]['widget']
check('trapping part 1 key form', w1['kind'] == 'expression' and w1['answer'] == '0.2e^{r}')
for r in (0.1, 0.2711, 0.9, 1.5):
    qq = 0.2 * math.exp(r)
    worst = 0
    for _ in range(4000):
        x, y = random.uniform(-r, r), random.uniform(-r, r)
        if abs(x - y) > 1e-9:
            worst = max(worst, abs(T(x) - T(y)) / abs(x - y))
    near = abs(T(r) - T(r - 1e-6)) / 1e-6
    check('trapping part 1: q = 0.2e^r is best at r = %s' % r, worst <= qq + 1e-12 and near > qq * (1 - 1e-5) and qq < 1)
check('trapping part 1 slips', {x['id']: x['tex'] for x in w1['wrong']} == {'left-end': '0.2e^{-r}', 'at-zero': '0.2', 'no-coefficient': 'e^{r}'})
check('trapping: ln 5 is where q reaches 1', abs(0.2 * math.exp(math.log(5)) - 1) < 1e-12)
o2 = {o['id']: o for o in tr['parts'][1]['widget']['options']}
check('trapping part 2 one correct option', [k for k, o in o2.items() if o.get('correct')] == ['triangle'])
for r in (0.2712, 0.3, 0.5, 0.8):       # the condition holds: the image stays inside
    check('trapping part 2: condition at r = %s' % r, g(r) >= 0)
    check('trapping part 2: image inside at r = %s' % r, all(abs(T(-r + 2 * r * k / 500)) <= r for k in range(501)))
check('trapping part 2: no-start is false (T(0) = 0.2 > 0)', T(0) > 0.2 * math.exp(0.5) * 0)
check('trapping part 2: x/2 + 5 sends [-1, 1] to [4.5, 5.5]', (-1 / 2 + 5, 1 / 2 + 5) == (4.5, 5.5))
lo, hi = 0.0, 0.5
for _ in range(80):
    m = (lo + hi) / 2
    lo, hi = (m, hi) if g(m) < 0 else (lo, m)
r0 = hi
check('trapping part 3: g < 0 below the root', all(g(r0 * k / 2000) < 0 for k in range(1, 2000)))
numeric('trapping part 3', tr['parts'][2], r0, {'no-q': 0.2, 'q-at-zero': 0.25}, places=4, printed=[r'r \approx 0.2711', 'about 0.2711', '0.2623', '0.2000', '0.0007'])
check('trapping part 3: short by 0.0007 at 0.27, over at 0.272', abs(-g(0.27) - 0.0007) < 5e-5 and g(0.272) > 0)
check('trapping part 3: q and room at 0.2711', round(0.2 * math.exp(0.2711), 4) == 0.2623 and round((1 - 0.2 * math.exp(0.2711)) * 0.2711, 4) == 0.2)
check('trapping part 3 slip q-at-zero: 0.2 = 0.8 r', abs(0.2 / 0.8 - 0.25) < 1e-12)
xs = [0.0]
for _ in range(60):
    xs.append(T(xs[-1]))
xstar = xs[-1]
check('trapping part 4: fixed point', abs(T(xstar) - xstar) < 1e-14 and abs(xstar) < 0.2711)
numeric('trapping part 4', tr['parts'][3], xstar, {'one-step': 0.2, 'radius': 0.2711}, places=4, printed=['0.2443', '0.2553', '0.2582', r'x^* \approx 0.2592'])
check('trapping part 4 iterates', [round(v, 4) for v in xs[1:5]] == [0.2, 0.2443, 0.2553, 0.2582])
check('trapping part 4: a dozen steps fix 4 places', abs(xs[12] - xstar) < 5e-6)
# the image of B_r by its ends (T increases): inside B_r from r = x*, before the triangle condition holds
check('trapping: B_r is invariant for every r >= x*', all(T(r) <= r and T(-r) >= -r for r in (xstar + 1e-9, 0.265, 0.2711, 0.3)))

# p-coin-paths: paths as 0/1 tuples, d = 2^-k at the first difference
cp = item(P3, 'p-coin-paths')
L = 12


def dist(a, b):
    for k, (u, v) in enumerate(zip(a, b), 1):
        if u != v:
            return Fr(1, 2 ** k)
    return Fr(0)


def V(a, tail=0):
    return sum(Fr(x, 2 ** k) for k, x in enumerate(a, 1)) + tail * Fr(1, 2 ** len(a))


paths = list(product((0, 1), repeat=7))
balls = {frozenset(b for b in paths if dist(a, b) < Fr(1, 10)) for a in paths}
numeric('coin part 1', cp['parts'][0], len(balls), {'four-days': 16, 'two-days': 4}, printed=['2^3 = 8', '2^{-4} = 0.0625', '2^{-3} = 0.125'])
check('coin part 1 key 8, equal or disjoint', len(balls) == 8 and all(a == b or not (a & b) for a in balls for b in balls))
check('coin: d is a metric on the sample (strong triangle inequality)',
      all(dist(a, c) <= max(dist(a, b), dist(b, c)) for a in paths[::5] for b in paths[::7] for c in paths[::3]))
# largest gap for a first difference on day 4: tails u-for-ever (1) or d-for-ever (0) after day L
ends = [(p, t) for p in product((0, 1), repeat=6) for t in (0, 1)]
gap4 = max(abs(V(a, s) - V(b, t)) for a, s in ends for b, t in ends if dist(a, b) == Fr(1, 16))
numeric('coin part 2', cp['parts'][1], gap4, {'day-only': Fr(1, 16), 'day-three': Fr(1, 4)}, printed=[r'\tfrac18', r'2\,d(\omega, \omega'])
check('coin part 2 key 1/8', gap4 == Fr(1, 8))
check('coin part 2: |V - V\'| <= 2d on every pair', all(abs(V(a, s) - V(b, t)) <= 2 * dist(a, b) for a, s in ends[::3] for b, t in ends[::5] if a != b))
# paths scoring 5/8 among paths that are constant after day 8 (a score with a finite binary form needs such a path)
canon = set()
for p in product((0, 1), repeat=8):
    for t in (0, 1):
        if V(p, t) == Fr(5, 8):
            canon.add(p + (t,) * 4)
numeric('coin part 3', cp['parts'][2], len(canon), {'one-path': 1})
check('coin part 3 key 2', canon == {(1, 0, 1) + (0,) * 9, (1, 0, 0) + (1,) * 9})
zero_paths = {p + (t,) * 4 for p in product((0, 1), repeat=8) for t in (0, 1) if V(p, t) == 0}
one_paths = {p + (t,) * 4 for p in product((0, 1), repeat=8) for t in (0, 1) if V(p, t) == 1}
check('coin part 3: scores 0 and 1 have one path each', len(zero_paths) == 1 and len(one_paths) == 1)
om = [tuple(([1, 0] * n + [0] * 40)[:40]) for n in range(1, 15)]
check('coin part 4: omega_m, omega_n agree on 2 min(m, n) days',
      all(dist(om[m - 1], om[n - 1]) == Fr(1, 2 ** (2 * min(m, n) + 1)) for m in range(1, 10) for n in range(1, 10) if m != n))
lim = sum(Fr(1, 2 ** (2 * j - 1)) for j in range(1, 40))
numeric('coin part 4', cp['parts'][3], Fr(2, 3), {'down-first': Fr(1, 3), 'first-day': Fr(1, 2), 'all-days': 1}, printed=[r'\tfrac23', r'\tfrac{1/2}{1 - 1/4}'])
check('coin part 4: series to 2/3', abs(lim - Fr(2, 3)) < Fr(1, 10 ** 20) and V(om[0][:12]) == Fr(1, 2))

# p-cube-delta parts 3 and 4
cd = item(P3, 'p-cube-delta')
w3 = cd['parts'][2]['widget']
grid = [-1 + 3 * k / 300 for k in range(301)]
mx = max(x * x + x * y + y * y for x in grid for y in grid)
check('cube part 3: largest second factor 12, key eps/12', abs(mx - 12) < 1e-9 and w3['answer'] == r'\frac{\varepsilon}{12}')
check('cube part 3 question as the review gave it', 'Give it in terms of $\\varepsilon$, from the largest value of the second factor on $K$.' in cd['parts'][2]['question'])


def h(x):
    return (x + 1 / 12) ** 3 - x ** 3 - 1


lo, hi = 0.0, 5.0
for _ in range(80):
    m = (lo + hi) / 2
    lo, hi = (m, hi) if h(m) < 0 else (lo, m)
root = hi
quad = (-Fr(1, 48) + math.sqrt(Fr(1, 2304) + 4 * Fr(1, 4) * (1 - Fr(1, 1728)))) / (2 * Fr(1, 4))
check('cube part 4: bisection and quadratic agree', abs(root - quad) < 1e-12)
check('cube part 4: expansion', all(abs((x + Fr(1, 12)) ** 3 - x ** 3 - (x * x / 4 + x / 48 + Fr(1, 1728))) == 0 for x in (Fr(0), Fr(1, 3), Fr(2), Fr(7, 5))))
numeric('cube part 4', cd['parts'][3], root, {'slope-only': 2}, places=4, printed=[r'x \approx 1.9582', '2.0415', r'\tfrac{x^2}{4} + \tfrac{x}{48} + \tfrac{1}{1728}'])
check('cube part 4: pair reaches past K', root < 2 < root + 1 / 12 and round(root + 1 / 12, 4) == 2.0415)
check('cube part 4: gap grows further out', all(h(root + k / 10) > h(root + (k - 1) / 10) for k in range(1, 50)))

# lesson ids in learner text, sets 1 to 3
import re
P1 = load(1)
blob = json.dumps([P1, P2, P3], ensure_ascii=False)
check('no lesson id in learner text', not re.search(r'`l\d+`|\bl\d{1,2}\b', blob))
pz = item(P1, 'p-plotter-zone')
y = (2.5, 0.5)
near = (y[0] + 0.4 * 3, y[1] + 0.4 * 1)
check('plotter part 4: nearest point (3.7, 0.9) on 3x + y = 12, distance 1.2649 above 1.1926',
      abs(3 * near[0] + near[1] - 12) < 1e-12 and round(0.4 * math.sqrt(10), 4) == 1.2649 and round(8 / (3 * math.sqrt(5)), 4) == 1.1926
      and abs(pz['parts'][3]['widget']['answer'] - 4 / math.sqrt(10)) < 1e-9)

# ---------------------------------------------------------------- findings of the review
p = sg['parts']
finding(1, 'only member of $\\tau$ holding hold is $S$' in p[2]['explain']['text'] and set(map(len, tau)) == {0, 1, 2, 3},
        'p-signal-bands: tau is the three-point space of l5 screens[0] and l8 screens[1] relabelled, and part 3 gives l8 screens[1]\'s reason')
finding(2, r'\{\text{sell}, \text{buy}\}' not in p[1]['question'] or r'\{\text{sell}\}' not in p[2]['question'],
        'p-signal-bands parts 2 and 3 restate the count 5, not the sets of tau they need')
finding(3, 'f(p(t))' not in p[3]['question'], 'p-signal-bands part 4 uses f o p, which no lesson of the course writes or defines')
finding(4, '98' in sg['prose'] and '104' in p[3]['question'], 'p-signal-bands shares "sell below 98, otherwise hold" and 104 with first-python l5')
finding(5, 'which bounds the distance from $f_0$ to $f^*$' in ke['parts'][3]['feedback']['byKey']['over-one-minus'],
        'p-kernel-equation part 4 slip line over-one-minus paraphrases h3-aposteriori')
finding(6, 'Using $r = 0.2711$ from part 3' in tr['parts'][3]['question'] and g(0.2711) < 0,
        'p-trapping-interval part 4 uses r = 0.2711, where the condition of part 2 fails by %.1e' % -g(0.2711))
finding(7, 'a score with a finite binary form has two paths' in cp['parts'][2]['explain']['text'] and len(zero_paths) == 1,
        'p-coin-paths part 3 explain: scores 0 and 1 have a finite binary form and one path each')
finding(8, 'Using part 3, $V$ is continuous.' in cp['parts'][3]['question'], 'p-coin-paths part 4 credits part 3 with the continuity that part 2 gave')
finding(9, 'the the' in pz['parts'][2]['explain']['text'], 'p-plotter-zone part 3 explain: "the the open balls lesson proof"')
finding(10, "(3.7, 0.9)$, above part 3's floor" in pz['parts'][3]['explain']['text'], 'p-plotter-zone part 4 explain says a point is above a floor')

print('delta-review-delta-ag-topology-numbers: %d checks, %d failed' % (N[0], N[1]))
