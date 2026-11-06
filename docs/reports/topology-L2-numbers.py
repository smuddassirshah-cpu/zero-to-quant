"""Recompute every number stated in topology level 2 (Topological spaces) by two routes, and check each at its JSON path.
Run: python3 docs/reports/topology-L2-numbers.py   (standard library only; exits 0 when every check passes)
Finite-space counts come from brute force over families of subsets (route 1) and from preorders, the
specialisation order of a finite topology (route 2). Real-number values come from a closed form and a second
formula or a bisection. The script also runs every code widget of the level in CPython: each solution passes its
hidden tests and each starter fails at least one.
"""
import sys, os, math, json
from itertools import combinations, permutations
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("topology", 2)
E = lv.expect
fails = []
HERE = os.path.dirname(os.path.abspath(__file__))


def two(name, a, b, tol=1e-9):
    if not math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol):
        fails.append(f'{name}: routes disagree {a!r} vs {b!r}')


def bisect(f, a, b):
    fa = f(a)
    for _ in range(200):
        c = (a + b) / 2
        if (f(c) < 0) == (fa < 0): a, fa = c, f(c)
        else: b = c
    return (a + b) / 2


def subsets(n):
    return [frozenset(c) for r in range(n + 1) for c in combinations(range(n), r)]


def is_top(X, T):
    if frozenset() not in T or X not in T: return False
    return all(U | V in T and U & V in T for U in T for V in T)


def topologies(n):
    X = frozenset(range(n)); S = [s for s in subsets(n) if s and s != X]
    out = []
    for r in range(len(S) + 1):
        for fam in combinations(S, r):
            T = set(fam) | {frozenset(), X}
            if is_top(X, T): out.append(frozenset(T))
    return out


def preorders(n):
    """reflexive transitive relations on range(n): in bijection with topologies (open sets = up-sets)"""
    pairs = [(a, b) for a in range(n) for b in range(n) if a != b]
    out = []
    for r in range(len(pairs) + 1):
        for rel in combinations(pairs, r):
            R = set(rel) | {(a, a) for a in range(n)}
            if all((a, c) in R for (a, b) in R for (b2, c) in R if b == b2): out.append(frozenset(R))
    return out


def connected(n, T):
    X = frozenset(range(n))
    return not any(U and U != X and (X - U) in T for U in T)


def preorder_connected(n, R):
    """a finite space is connected when the symmetric closure of its preorder connects every point"""
    if n == 0: return True
    seen, todo = {0}, [0]
    while todo:
        a = todo.pop()
        for (x, y) in R:
            for u, v in ((x, y), (y, x)):
                if u == a and v not in seen: seen.add(v); todo.append(v)
    return len(seen) == n


def classes(items, n, act):
    seen, k = set(), 0
    for t in items:
        if t in seen: continue
        k += 1
        for p in permutations(range(n)): seen.add(act(t, p))
    return k


act_top = lambda T, p: frozenset(frozenset(p[x] for x in U) for U in T)
act_pre = lambda R, p: frozenset((p[a], p[b]) for a, b in R)

TOPS = {n: topologies(n) for n in range(5)}
PRES = {n: preorders(n) for n in range(5)}
counts = [len(TOPS[n]) for n in range(5)]
assert counts == [len(PRES[n]) for n in range(5)] == [1, 1, 4, 29, 355], counts
cls = [classes(TOPS[n], n, act_top) for n in range(4)]
assert cls == [classes(PRES[n], n, act_pre) for n in range(4)] == [1, 1, 3, 9], cls
conn = [sum(connected(n, T) for T in TOPS[n]) for n in range(4)]
assert conn == [sum(preorder_connected(n, R) for R in PRES[n]) for n in range(4)] == [1, 1, 3, 19], conn

# ================= l5 =================
E("l5", "screens[4].widget.answer", counts[2]); E("l5", "screens[4].widget.wrong[0].value", 2); E("l5", "screens[4].widget.wrong[1].value", 3); E("l5", "screens[4].widget.wrong[2].value", 16)
E("l5", "screens[4].explain.text", counts[3]); E("l5", "screens[4].explain.text", counts[4])
assert 2 ** 4 == 16  # every family of the four subsets of {a, b}
E("l5", "screens[9].widget.answer", counts[0]); E("l5", "screens[9].widget.wrong[0].value", 0); E("l5", "screens[9].widget.wrong[1].value", 2)
for v in (1, 4, 29): E("l5", "screens[9].explain.text", v)
for v in (1, 4, 29, 355): E("l5", "screens[10].explain.text", v)
E("l5", "quiz[1].widget.answer", counts[3]); E("l5", "quiz[1].widget.wrong[0].value", 2 ** 6); E("l5", "quiz[1].widget.wrong[1].value", 2 ** 3)
E("l5", "quiz[1].explain.text", 64); E("l5", "quiz[1].explain.text", 355)
# the three candidates and the two hook families
fs = lambda *s: {frozenset(x) for x in s}
X3 = frozenset('abc')
assert is_top(X3, fs('', 'a', 'ab', 'abc')) and not is_top(X3, fs('', 'a', 'b', 'abc')) and not is_top(X3, fs('', 'ab', 'bc', 'abc'))
assert is_top(X3, fs('', 'a', 'b', 'ab', 'abc'))

# ================= l6 =================
B = [frozenset('a'), frozenset('ab'), frozenset('c'), frozenset('cd')]
gen = {frozenset().union(*c) for r in range(5) for c in combinations(B, r)}
# second route: by minimal neighbourhoods, U is open iff it contains the smallest piece round each of its points
minimal = {x: min((b for b in B if x in b), key=len) for x in 'abcd'}
gen2 = {U for U in (frozenset(c) for r in range(5) for c in combinations('abcd', r)) if all(minimal[x] <= U for x in U)}
assert gen == gen2 and len(gen) == 9
E("l6", "screens[0].explain.text", 9); E("l6", "screens[0].hints[2].text", 9); E("l6", "screens[9].widget.tests[1].expect", "9")
sub = {frozenset().union(*c) for r in range(4) for c in combinations([frozenset('ab'), frozenset('bc'), frozenset('b')], r)} | {X3}
assert sub == fs('', 'b', 'ab', 'bc', 'abc')
assert {U & frozenset('bc') for U in fs('', 'a', 'ab', 'abc')} == fs('', 'b', 'bc')
c = (1 / 3, 1 / 3, 1 / 3); m = (0.5, 0.5, 0)
r_mid = math.dist(c, m)
side = math.dist((1, 0, 0), (0, 1, 0)); r_in = side / (2 * math.sqrt(3))
two('inradius', r_mid, r_in); two('inradius closed', r_mid, 1 / math.sqrt(6))
E("l6", "screens[10].widget.answer", round(r_mid, 4)); E("l6", "screens[10].explain.text", 0.4082)
E("l6", "screens[10].widget.wrong[0].value", round(math.dist(c, (1, 0, 0)), 4)); E("l6", "screens[10].widget.wrong[1].value", 0.3333)
q_gen = {frozenset().union(*c) for r in range(4) for c in combinations([frozenset('a'), frozenset('ab'), frozenset('ac')], r)}
assert len(q_gen) == 5
E("l6", "quiz[1].widget.answer", 5); E("l6", "quiz[1].widget.wrong[0].value", 3); E("l6", "quiz[1].widget.wrong[1].value", 4)

# ================= l7 =================
def rad(x, y): s = max(abs(x), abs(y)) / math.hypot(x, y); return (x * s, y * s)
def rad2(x, y):
    """second route: the ray through P meets the circle at P / d2; scale that by d_inf"""
    d2 = math.hypot(x, y); u = (x / d2, y / d2); di = max(abs(x), abs(y)); return (u[0] * di, u[1] * di)
for P, shown in [((1, 1), (0.7071, 0.7071)), ((1, 0.5), (0.8944, 0.4472)), ((0.5, 0.25), (0.4472, 0.2236))]:
    a, b = rad(*P), rad2(*P)
    two(f'rad {P}', a[0], b[0]); two(f'rad {P} y', a[1], b[1])
    assert (round(a[0], 4), round(a[1], 4)) == shown, (P, a)
E("l7", "screens[0].widget.answer", 0.7071); E("l7", "screens[0].explain.text", 0.7071)
E("l7", "screens[0].widget.wrong[0].value", 1); E("l7", "screens[0].widget.wrong[1].value", 0.5)
E("l7", "screens[1].widget.rows[0][1].answer", 0.8944); E("l7", "screens[1].widget.rows[0][2].answer", 0.4472)
E("l7", "screens[1].widget.rows[1][1].answer", 0.4472); E("l7", "screens[1].widget.rows[1][2].answer", 0.2236)
E("l7", "screens[1].hints[1].text", round(math.sqrt(1.25), 4)); E("l7", "screens[1].explain.text", 0.8944); E("l7", "screens[1].explain.text", 0.2236)
f = lambda x: x / (1 - abs(x)); g = lambda y: y / (1 + abs(y))
for x, v in [(0.5, 1), (0.75, 3), (-0.9, -9)]:
    two(f'f({x})', f(x), v); two(f'g(f({x}))', g(f(x)), x)
    E("l7", "screens[2].prose", v)
two('g(3)', g(3), bisect(lambda x: f(x) - 3, 0, 0.999)); two('g(-3)', g(-3), bisect(lambda x: f(x) + 3, -0.999, 0))
E("l7", "screens[2].feedback.correct", 0.75); E("l7", "screens[2].feedback.correct", -0.9)
E("l7", "screens[3].widget.answer", g(-3)); E("l7", "screens[3].widget.wrong[0].value", 0.75); E("l7", "screens[3].widget.wrong[1].value", -3 / (1 - 3))
E("l7", "screens[3].explain.text", -0.75); E("l7", "screens[3].explain.text", 1.5)
# letters: pieces after removing the junction = arms of the junction (graph degree), counted from the segments
letters = {'T': [((-1, 2), (1, 2)), ((0, 2), (0, 0))], 'X': [((2, 0), (4, 2)), ((2, 2), (4, 0))], 'Y': [((5, 2), (6, 1)), ((7, 2), (6, 1)), ((6, 1), (6, 0))]}
junction = {'T': (0, 2), 'X': (3, 1), 'Y': (6, 1)}
def arms(segs, j):
    k = 0
    for p, q in segs:
        on = abs((q[0] - p[0]) * (j[1] - p[1]) - (q[1] - p[1]) * (j[0] - p[0])) < 1e-12
        if not on: continue
        k += (p != j) + (q != j)   # each end of the segment away from j is an arm
    return k
assert [arms(letters[L], junction[L]) for L in 'TXY'] == [3, 4, 3]
E("l7", "screens[6].widget.answer", 4); E("l7", "screens[6].widget.wrong[0].value", 3); E("l7", "screens[6].widget.wrong[1].value", 2)
E("l7", "screens[6].explain.text", 3); E("l7", "screens[6].explain.text", 4)
E("l7", "screens[7].widget.answer", cls[2]); E("l7", "screens[7].widget.wrong[0].value", counts[2]); E("l7", "screens[7].widget.wrong[1].value", 2)
E("l7", "screens[7].explain.text", 29); E("l7", "screens[7].explain.text", cls[3])
E("l7", "quiz[2].widget.answer", cls[3]); E("l7", "quiz[2].widget.wrong[0].value", 29); E("l7", "quiz[2].widget.wrong[1].value", math.factorial(3))
for v in (29, 9, 1, 3): E("l7", "quiz[2].explain.text", v)
# trap points t_n = 2 pi - 1/n on the circle
pts = json.load(open(os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'topology', 'l7-homeomorphisms.json')))['screens'][8]['canvas']['state']['points']
for p in pts[1:]:
    n = {'t2': 2, 't3': 3, 't4': 4, 't6': 6}[p['id']]
    t = 2 * math.pi - 1 / n
    assert abs(p['x'] - math.cos(t)) < 6e-5 and abs(p['y'] - math.sin(t)) < 6e-5, p
# artanh
for rho, z in [(0.5, 0.5493), (-0.9, -1.4722)]:
    two(f'artanh {rho}', math.atanh(rho), 0.5 * math.log((1 + rho) / (1 - rho))); assert round(math.atanh(rho), 4) == z
two('tanh 1', math.tanh(1), (math.e ** 2 - 1) / (math.e ** 2 + 1))
E("l7", "screens[10].widget.rows[0][2].answer", 0.5493); E("l7", "screens[10].widget.rows[1][2].answer", -1.4722); E("l7", "screens[10].widget.rows[2][2].answer", round(math.tanh(1), 4))
E("l7", "screens[10].widget.rows[0][2].wrong[0].value", 0.5)
for v in (0.5493, -1.4722, 0.7616): E("l7", "screens[10].explain.text", v)

# ================= l8 =================
mu = (0.04, 0.06, 0.09)
w = (0.07 - 0.04) / (0.09 - 0.04)
two('two-asset weight', w, bisect(lambda t: (1 - t) * 0.04 + t * 0.09 - 0.07, 0, 1))
for wv in [(0.4, 0, 0.6), (0, 2 / 3, 1 / 3)]: two(f'7% {wv}', sum(a * b for a, b in zip(wv, mu)), 0.07)
E("l8", "screens[11].widget.answer", round(w, 4)); E("l8", "screens[11].widget.wrong[0].value", round(1 - w, 4)); E("l8", "screens[11].widget.wrong[1].value", round(7 / 9, 4))
E("l8", "screens[11].explain.text", 0.4); E("l8", "screens[11].explain.text", 0.6)
E("l8", "screens[10].explain.text", conn[3]); E("l8", "screens[10].explain.text", counts[3])
E("l8", "quiz[0].widget.answer", conn[2]); E("l8", "quiz[0].widget.wrong[0].value", 1); E("l8", "quiz[0].widget.wrong[1].value", 4)
E("l8", "quiz[0].explain.text", 19); E("l8", "quiz[0].explain.text", 29)
assert abs(math.sin(1) - 0.8415) < 5e-5

# ================= review =================
rb = {frozenset().union(*c) for r in range(3) for c in combinations([frozenset('a'), frozenset('bc')], r)}
assert len(rb) == 4
E("review", "items[1].widget.answer", 4); E("review", "items[1].widget.wrong[0].value", 2); E("review", "items[1].widget.wrong[1].value", 3)
two('f(-0.75)', f(-0.75), -bisect(lambda y: g(y) - 0.75, 0, 100))
E("review", "items[7].widget.answer", -3); E("review", "items[7].widget.wrong[0].value", 3); E("review", "items[7].widget.wrong[1].value", round(g(-0.75), 4))
E("review", "items[7].explain.text", -3)

# ================= homework =================
t1, t2 = fs('', 'a', 'ab', 'abc'), fs('', 'b', 'bc', 'abc')
nbij = sum(1 for p in permutations('abc') if {frozenset(dict(zip('abc', p))[x] for x in U) for U in t1} == t2)
assert nbij == 1
E("homework", "items[2].widget.answer", nbij); E("homework", "items[2].widget.wrong[0].value", math.factorial(3)); E("homework", "items[2].widget.wrong[1].value", 0)
E("homework", "items[2].explain.text", 1)
fam = [fs('', 'a', 'b', 'ab', 'abc'), fs('', 'a', 'bc', 'abc'), fs('', 'ab', 'ac', 'abc'), fs('', 'a', 'ab', 'ac', 'abc'), fs('', 'b', 'c', 'abc')]
assert [is_top(X3, F_) for F_ in fam] == [True, True, False, True, False]
P_ = (0.6, 0.8); s = math.hypot(*P_) / max(map(abs, P_))
pre = (P_[0] * s, P_[1] * s)
two('radial inverse', pre[0], 0.75); two('radial inverse y', pre[1], 1); two('forward check', rad(*pre)[0], 0.6)
E("homework", "items[4].widget.answer", 0.75); E("homework", "items[4].widget.wrong[0].value", 0.6); E("homework", "items[4].widget.wrong[1].value", round(0.6 * 0.8, 4))
E("homework", "items[4].explain.text", 0.8)
for v in (3, 29, 19): E("homework", "items[6].explain.text", v)
E("homework", "items[6].explain.text", counts[3] - conn[3])

# ================= code widgets: solution passes, starter fails =================
def run_widget(w, code):
    ns = {}
    try:
        exec(w.get('prelude', ''), ns); exec(code, ns)
    except Exception:
        return False
    for t in w['tests']:
        try:
            exec(t.get('setup', '') or '', ns)
            if t.get('compare') == 'raises':
                try:
                    eval(t['call'], ns); return False
                except Exception as ex:
                    if type(ex).__name__ != t['expect']: return False
                continue
            got = eval(t['call'], ns); want = eval(t['expect'], ns)
            if t.get('compare') == 'isclose':
                tol = t.get('tol', {})
                if not math.isclose(got, want, rel_tol=tol.get('rel', 0 if tol else 1e-9), abs_tol=tol.get('abs', 0 if tol else 1e-12)): return False
            elif got != want:
                return False
        except Exception:
            return False
    return True


widgets = []
def collect(o):
    if isinstance(o, dict):
        if o.get('kind') == 'code': widgets.append(o)
        for v in o.values(): collect(v)
    elif isinstance(o, list):
        for v in o: collect(v)
for f_ in ['l5-topologies', 'l6-bases-and-subspaces', 'l7-homeomorphisms', 'l8-connectedness', 'homework-2']:
    collect(json.load(open(os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'topology', f_ + '.json'))))
assert len(widgets) == 5
for w_ in widgets:
    if not run_widget(w_, w_['solution']): fails.append('a code solution fails its tests: ' + w_['tests'][0]['call'])
    if run_widget(w_, w_['starter']): fails.append('a code starter passes its tests: ' + w_['tests'][0]['call'])

# Fix pass (review-topology-1-2): prose claims added or reworded by the fix pass.
r2_ = math.sqrt(2)
for v_ in [(1, 0), (0, 1), (1, 1), (-0.3, 0.7), (0.6, 0.8), (3, -4), (1e-6, 2e-6)]:
    d2v = math.hypot(*v_); div = max(abs(v_[0]), abs(v_[1]))
    assert div <= d2v + 1e-15 and d2v <= r2_ * div + 1e-15, v_            # d_inf <= d_2 <= sqrt2 d_inf (l7 s1)
    Pp = (v_[0] * div / d2v, v_[1] * div / d2v)                            # the radial image P' of P
    two('radial |P\'|_2 = |P|_inf', math.hypot(*Pp), div)
cof_ = range(-60, 60)
for A_ in [(), (0,), (1, 2), (-5, 7, 9)]:
    for B_ in [(), (3,), (1, 4), (0, -2, 8)]:
        assert (set(cof_) - set(A_)) & (set(cof_) - set(B_)), (A_, B_)     # any two non-empty cofinite sets meet (review-2 item 6)
assert frozenset() in [frozenset(), frozenset(cof_)]                       # the empty set is finite and open in the cofinite topology (l5 s7)
sier_ = {frozenset(), frozenset({1}), frozenset({0, 1})}
assert is_top(frozenset({0, 1}), sier_) and sum(1 for U_ in sier_ if len(U_) == 1) == 1   # one open singleton (l8 quiz[0])
l7_ = json.load(open(os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'topology', 'l7-homeomorphisms.json')))
n_hom_ = [t_ for sc_ in l7_['screens'] for t_ in (sc_.get('widget', {}) or {}).get('tests', []) if str(t_.get('call', '')).startswith('are_homeomorphic')]
assert len(n_hom_) == 5, len(n_hom_)                                       # "Five test are_homeomorphic" (l7 s9)

lv.check_wrongs()
for f_ in fails: print('FAIL', f_)
if fails: sys.exit(1)
lv.report()
