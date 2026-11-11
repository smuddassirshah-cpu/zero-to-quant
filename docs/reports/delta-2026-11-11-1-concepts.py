#!/usr/bin/env python3
"""Concept checks for the batched delta audit of 11 November 2026 (batch 1).

Courses: puzzles, game-theory, brainteasers, coding-int, research-int, systems,
ito, measure-prob. Changed content only (performance tasks, review top-ups).
Run from the repo root:  python3 docs/reports/delta-2026-11-11-1-concepts.py
Exits 0 when every check passes. A check that fails because the content is
wrong stays failing and is a finding in docs/reviews/audit-delta-2026-11-11-1.md.
C++ checks need g++ (they are skipped with a note, and counted, if it is absent).
"""
import json, math, os, sys, itertools, random, subprocess, tempfile, shutil, time
from fractions import Fraction as Fr
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C = os.path.join(ROOT, 'app', 'content', 'courses')
fails = []; n_checks = 0; skipped = []


def check(name, ok, detail=''):
    global n_checks
    n_checks += 1
    if not ok:
        fails.append(name)
    print(('ok   ' if ok else 'FAIL ') + name + ((' :: ' + str(detail)) if detail else ''))


def item(course, f, iid):
    j = json.load(open(os.path.join(C, course, f + '.json')))
    for it in j['items']:
        if it['id'] == iid:
            return it
    raise KeyError(iid)


def close(a, b, tol):
    return abs(a - b) <= tol


def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def same(a, b, rel=1e-9):
    if a is None or b is None:
        return a is b
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=rel, abs_tol=1e-12)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(same(x, y, rel) for x, y in zip(a, b))
    return a == b


def run_py(widget, code):
    """Run every hidden test of a Python code widget against code. Returns list of bools."""
    out = []
    for t in widget['tests']:
        ns = {}
        try:
            exec(code + '\n' + widget.get('postlude', ''), ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns)
            want = eval(t['expect'], {}) if isinstance(t['expect'], str) else t['expect']
            out.append(same(got, want) if t.get('compare') == 'isclose' else got == want)
        except Exception as e:  # noqa
            out.append(False)
    return out


# ------------------------------------------------------------------ puzzles
print('== puzzles')
b, p, r, q = 1.2, 0.45, 0.25, 0.30
g = lambda f, p=p, q=q, b=b: p * math.log(1 + b * f) + q * math.log(1 - f)
fs = (p * b - q) / (b * (p + q))
check('kelly f* = 4/15', close(fs, 4 / 15, 1e-12))
grid = max((g(i / 100000), i / 100000) for i in range(0, 99999))
check('kelly f* is the grid maximum of g', close(grid[1], fs, 2e-5), grid)
check('kelly g(f*) = 0.0319 (0.1249 - 0.0930)', close(g(fs), 0.0319, 5e-5) and close(p * math.log(1.32), 0.1249, 5e-5) and close(q * math.log(11 / 15), -0.0930, 5e-5), g(fs))
check('kelly g(2f*) = -0.0060 (0.2226 - 0.2286)', close(g(2 * fs), -0.0060, 5e-5) and close(p * math.log(1.64), 0.2226, 5e-5) and close(q * math.log(7 / 15), -0.2286, 5e-5), g(2 * fs))
lo, hi = 0.3, 0.9
for _ in range(80):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if g(mid) > 0 else (lo, mid)
check('kelly zero of g is about 0.513, below 2f*', close(lo, 0.513, 6e-4) and lo < 2 * fs, lo)
check('kelly slips: -0.0083 and 0.2; mean multiplier 1.128', close(p - (1 - p) / b, -0.0083, 5e-5) and close(p - q / b, 0.2, 1e-12) and close(1 + 2 * fs * (p * b - q), 1.128, 1e-9))
f20 = (0.1 * 20 - 0.9) / 20
check('kelly long shot: g(2f*) = 0.0114 > 0 at 20 to 1, p 0.1', close(g(2 * f20, 0.1, 0.9, 20), 0.0114, 5e-5))
check('kelly identity g = (p+q) h, and parabola peak near f*', close(g(0.2), (p + q) * (p / (p + q) * math.log(1.24) + q / (p + q) * math.log(0.8)), 1e-12))
# Monte Carlo: long-run growth per match at f*, 2f*; wealth at 2f* shrinks
rng = np.random.default_rng(11)
u = rng.random((400, 20000))
def growth(f):
    m = np.where(u < p, 1 + b * f, np.where(u < p + r, 1.0, 1 - f))
    return np.log(m).sum(axis=1) / u.shape[1]
ga, gb, gc = growth(fs), growth(2 * fs), growth(0.2)
check('kelly MC: growth at f* is 0.0319 and beats f = 0.2', close(ga.mean(), 0.0319, 6e-4) and ga.mean() > gc.mean(), (ga.mean(), gc.mean()))
check('kelly MC: growth at 2f* is negative on nearly every path', close(gb.mean(), -0.0060, 8e-4) and (gb < 0).mean() > 0.9, (gb.mean(), (gb < 0).mean()))

e5 = sum(Fr(8, 8 - k) for k in range(5))
check('five of eight stickers: 7.0762', close(float(e5), 7.0762, 5e-5), float(e5))
check('8 H_8 = 21.7429', close(float(sum(Fr(8, k) for k in range(1, 9))), 21.7429, 5e-5))
rng = random.Random(5)
tot = 0
for _ in range(200000):
    s = set(); t = 0
    while len(s) < 5:
        s.add(rng.randrange(8)); t += 1
    tot += t
check('five of eight MC', close(tot / 200000, 7.0762, 0.03), tot / 200000)
w = 0
for _ in range(200000):
    a = b_ = c = None; last = ''
    while True:
        last = (last + rng.choice('HT'))[-3:]
        if last == 'THH':
            w += 1; break
        if last == 'HHH':
            break
check('THH beats HHH with chance 7/8, ticket 14', close(w / 200000, 7 / 8, 0.004) and 16 * 7 / 8 == 14, w / 200000)

# -------------------------------------------------------------- game-theory
print('== game-theory')
A = [[5, -2], [-2, 1]]
pA = Fr(A[1][1] - A[1][0], A[0][0] - A[0][1] - A[1][0] + A[1][1])
v = A[0][0] * pA + A[1][0] * (1 - pA)
check('say-it: no saddle, p = q = 3/10, value 0.10, cell mean 0.50', max(min(r_) for r_ in A) == -2 and min(max(A[i][j] for i in range(2)) for j in range(2)) == 1 and pA == Fr(3, 10) and v == Fr(1, 10) and Fr(5 + 1 - 2 - 2, 4) == Fr(1, 2), (pA, v))
it = item('game-theory', 'homework-1', 'hw1-street-carts'); wd = it['widget']
res = run_py(wd, wd['solution'])
check('street carts: solution passes all %d hidden tests' % len(res), all(res), res)
res0 = run_py(wd, wd['starter'])
check('street carts: starter fails', not any(res0), res0)
# independent recomputation of the tables with exact fractions, and of the best replies
ns = {}; exec(wd['solution'], ns)
def table_ref(homes, xs, ys, a, b):
    T = []
    for x in xs:
        row = []
        for y in ys:
            na = sum(Fr(1) if abs(h - x) < abs(h - y) else Fr(1, 2) if abs(h - x) == abs(h - y) else Fr(0) for h in homes)
            row.append((a * na, b * (len(homes) - na)))
        T.append(row)
    return T
rng = random.Random(3); okT = True
for _ in range(300):
    homes = [rng.randrange(12) for _ in range(rng.randrange(1, 9))]
    xs = rng.sample(range(12), rng.randrange(1, 5)); ys = rng.sample(range(12), rng.randrange(1, 5))
    T = table_ref(homes, xs, ys, 2, 3); S = ns['street_table'](homes, xs, ys, 2, 3)
    okT &= all(S[i][j][0] == T[i][j][0] and S[i][j][1] == T[i][j][1] for i in range(len(xs)) for j in range(len(ys)))
    an, be = ns['best_replies'](S)
    for j in range(len(ys)):
        okT &= an[j] == [i for i in range(len(xs)) if all(T[i][j][0] >= T[k][j][0] for k in range(len(xs)))]
    for i in range(len(xs)):
        okT &= be[i] == [j for j in range(len(ys)) if all(T[i][j][1] >= T[i][k][1] for k in range(len(ys)))]
check('street carts: tables and best replies agree with an independent exact version', okT)
# rv1
Aa = [[4, 1], [1, 3]]; Bb = [[1, 3], [2, 0]]
pure = [(i, j) for i in range(2) for j in range(2) if Aa[i][j] >= Aa[1 - i][j] and Bb[i][j] >= Bb[i][1 - j]]
qL = Fr(Aa[1][1] - Aa[0][1], Aa[0][0] - Aa[0][1] - Aa[1][0] + Aa[1][1])
pT = Fr(Bb[1][1] - Bb[1][0], Bb[0][0] - Bb[0][1] - Bb[1][0] + Bb[1][1])
va = Aa[0][0] * qL + Aa[0][1] * (1 - qL); vb = Bb[0][0] * pT + Bb[1][0] * (1 - pT)
check('rv1: no pure equilibrium; q = 2/5, Ana 2.2; p = 1/2, Ben 1.5; mean 2.25', pure == [] and qL == Fr(2, 5) and va == Fr(11, 5) and pT == Fr(1, 2) and vb == Fr(3, 2) and Fr(4 + 1 + 1 + 3, 4) == Fr(9, 4), (pure, qL, va, pT, vb))
k = next(k for k in range(1, 50) if 100 * 0.5 ** k < 1)
check('rv2: bound first below 1 at round 7 (1.5625 then 0.78125)', k == 7 and 100 / 64 == 1.5625 and 100 / 128 == 0.78125)

# ------------------------------------------------------------- brainteasers
print('== brainteasers')
base = [(0, 0), (1, 0), (2, 0), (2, 1)]
def orients(cells):
    out = set(); cur = cells
    for flip in range(2):
        for rot in range(4):
            cur = [(y, -x) for x, y in cur]
            mx = min(x for x, y in cur); my = min(y for x, y in cur)
            out.add(tuple(sorted((x - mx, y - my) for x, y in cur)))
        cur = [(-x, y) for x, y in cur]
    return out
O = orients(base)
okc = oks = okr = True; cnt = 0
for o in O:
    for dr in range(6):
        for dc in range(10):
            cells = [(x + dr, y + dc) for x, y in o]
            if any(x >= 6 or y >= 10 for x, y in cells):
                continue
            cnt += 1
            okc &= sum((x + y) % 2 for x, y in cells) == 2
            oks &= sum(y % 2 for x, y in cells) in (1, 3)
            okr &= sum(x % 2 for x, y in cells) in (1, 3)
check('L pieces: 8 orientations, every placement is 2-2 on the chessboard', len(O) == 8 and okc, cnt)
check('L pieces: every placement is 3-1 on column stripes and on row stripes', oks and okr)
check('L pieces: 4a - 30 is never 0 for a in 0..15; nearest is +-2 at a = 7, 8', all(4 * a - 30 != 0 for a in range(16)) and 4 * 7 - 30 == -2 and 4 * 8 - 30 == 2)
it = item('brainteasers', 'homework-2', 'hw9-circle-hats'); wd = it['widget']
res = run_py(wd, wd['solution']); res0 = run_py(wd, wd['starter'])
check('circle hats: solution passes all %d hidden tests' % len(res), all(res), res)
check('circle hats: starter fails', not any(res0), res0)
# no plan beats floor(n/2): exhaustive over all deterministic plans for n = 3 and n = 4
def best_worst(n):
    best = 0
    cols = list(itertools.product((0, 1), repeat=n))
    views = [[(h[(i - 1) % n] * 2 + h[(i + 1) % n], h[i]) for h in cols] for i in range(n)]
    # per person, table of right-count vector per strategy (16 strategies)
    vecs = []
    for i in range(n):
        vi = []
        for s in range(16):
            vi.append(np.array([1 if ((s >> v) & 1) == own else 0 for v, own in views[i]]))
        vecs.append(vi)
    for combo in itertools.product(range(16), repeat=n):
        tot_ = sum(vecs[i][combo[i]] for i in range(n))
        best = max(best, int(tot_.min()))
    return best
check('circle hats: best worst case over every plan is 1 at n = 3 and 2 at n = 4', best_worst(3) == 1 and best_worst(4) == 2)
def bfs(first=None):
    start = (0, 0); seen = {start: 0}; fr = [start]
    if first == 'fill7':
        seen = {(7, 0): 1}; fr = [(7, 0)]
    while fr:
        nx = []
        for a, c in fr:
            d = seen[(a, c)]
            if c == 8:
                return d
            pour1 = min(a, 11 - c); pour2 = min(c, 7 - a)
            for s in [(7, c), (a, 11), (0, c), (a, 0), (a - pour1, c + pour1), (a + pour2, c - pour2)]:
                if s not in seen:
                    seen[s] = d + 1; nx.append(s)
        fr = nx
check('jugs 7 and 11: fewest steps to 8 in the 11 is 6; 8 if the 7 is filled first', bfs() == 6 and bfs('fill7') == 8, (bfs(), bfs('fill7')))

# --------------------------------------------------------------- coding-int
print('== coding-int')
it = item('coding-int', 'homework-3', 'h3-notes-drive'); wd = it['widget']
t0 = time.time(); res = run_py(wd, wd['solution']); dt = time.time() - t0
check('notes drive: solution passes all %d hidden tests (%.1f s native)' % (len(res), dt), all(res), res)
res0 = run_py(wd, wd['starter'])
check('notes drive: starter fails', not any(res0), res0)
# an independent naive version (flat dict of paths, sizes by scanning) must agree on the tests
NAIVE = r'''
class NotesDrive:
    def __init__(self):
        self.files = {}; self.dirs = {()}
    def _n(self, p): return tuple(x for x in p.split('/') if x)
    def _exists(self, n): return n in self.files or n in self.dirs
    def _mk(self, n):
        for i in range(len(n) + 1): self.dirs.add(n[:i])
    def mkdir(self, path): self._mk(self._n(path))
    def write(self, path, text):
        n = self._n(path); self._mk(n[:-1]); self.files[n] = text
    def read(self, path): return self.files.get(self._n(path))
    def ls(self, path):
        n = self._n(path)
        if n in self.files: return [n[-1]]
        if n not in self.dirs: return []
        return sorted({m[len(n)] for m in list(self.files) + list(self.dirs) if len(m) > len(n) and m[:len(n)] == n})
    def rm(self, path):
        n = self._n(path)
        if not n or not self._exists(n): return
        self.files = {m: t for m, t in self.files.items() if m[:len(n)] != n}
        self.dirs = {m for m in self.dirs if m[:len(n)] != n}
    def mv(self, src, dst):
        s, d = self._n(src), self._n(dst)
        if not s or not self._exists(s) or self._exists(d) or d[:len(s)] == s: return False
        self._mk(d[:-1])
        self.files = {(d + m[len(s):] if m[:len(s)] == s else m): t for m, t in self.files.items()}
        self.dirs = {(d + m[len(s):] if m[:len(s)] == s else m) for m in self.dirs}
        return True
    def size(self, path):
        n = self._n(path)
        return sum(len(t) for m, t in self.files.items() if m[:len(n)] == n)
'''
wd_small = dict(wd); wd_small['tests'] = wd['tests'][:-1] + [{'call': 'big_case(4000)', 'expect': '0', 'compare': 'equal'}]
ns1 = {}; exec(wd['solution'] + '\n' + wd['postlude'], ns1); ns2 = {}; exec(NAIVE + '\n' + wd['postlude'], ns2)
resn = run_py(dict(wd, tests=wd['tests'][:-1]), NAIVE)
check('notes drive: an independent flat-dict version passes the nine rule tests', all(resn), resn)
check('notes drive: it also agrees with the solution on a 4,000-step random case', ns1['big_case'](4000) == ns2['big_case'](4000))
refused = sum(1 for op in eval(wd['tests'][5]['call'][len('run_drive('):-1]) if op[0] == 'mv')
check('notes drive: feedback test-6 says four refused moves; the test has that many', 'four moves' in it['feedback']['byKey']['test-6'] and refused == 4, 'refused moves in test 6: %d' % refused)
# size() must not depend on the number of files: time size('/') with 2,000 and 64,000 files
def size_time(nf):
    d = ns1['NotesDrive']()
    for i in range(nf):
        d.write('/a/b%d/f%d' % (i % 50, i), 'xx')
    t0 = time.perf_counter()
    for _ in range(20000):
        d.size('/a')
    return time.perf_counter() - t0
t_small, t_big = size_time(2000), size_time(64000)
check('notes drive: size cost does not grow with the files stored', t_big < 3 * t_small, (t_small, t_big))

it = item('coding-int', 'homework-4', 'h4-pairs-aloud'); model = it['widget']['model']
code = model[model.index('```python') + 9:model.index('```', model.index('```python') + 9)]
ns = {}; exec(code, ns); cp = ns['count_pairs']
check('count pairs: model code gives 5 on the example', cp([4, 6, 5, 5, 1, 9, 5], 10) == 5)
rng = random.Random(8); okp = True
for _ in range(500):
    xs = [rng.randrange(-6, 7) for _ in range(rng.randrange(0, 14))]; t = rng.randrange(-8, 9)
    brute = sum(1 for i in range(len(xs)) for j in range(i + 1, len(xs)) if xs[i] + xs[j] == t)
    cnts = {}
    for x in xs: cnts[x] = cnts.get(x, 0) + 1
    multi = sum(cnts[v_] * cnts.get(t - v_, 0) for v_ in cnts if v_ < t - v_) + sum(c * (c - 1) // 2 for v_, c in cnts.items() if v_ == t - v_)
    # two pointers with runs
    s = sorted(xs); i, j, tp = 0, len(s) - 1, 0
    while i < j:
        sm = s[i] + s[j]
        if sm < t: i += 1
        elif sm > t: j -= 1
        elif s[i] == s[j]:
            kk = j - i + 1; tp += kk * (kk - 1) // 2; break
        else:
            a_ = 1; b2 = 1
            while s[i + a_] == s[i]: a_ += 1
            while s[j - b2] == s[j]: b2 += 1
            tp += a_ * b2; i += a_; j -= b2
    okp &= cp(xs, t) == brute == multi == tp
check('count pairs: dict plan, two-pointer run rule and many-target formula all equal brute force', okp)
check('count pairs: n(n-1)/2 at 200,000 is 19,999,900,000, above INT_MAX', 200000 * 199999 // 2 == 19999900000 > 2147483647)

# ------------------------------------------------------------- research-int
print('== research-int')
t = math.sqrt(5)
check('signal: t = 2.24, two-sided p = 0.025', close(t, 2.24, 5e-3) and close(2 * (1 - Phi(t)), 0.025, 6e-4), 2 * (1 - Phi(t)))
check('signal: power 0.61 against Sharpe 1', close(1 - Phi(1.96 - t) + Phi(-1.96 - t), 0.61, 5e-3))
check('signal: best of twenty reaches p <= 0.025 about four times in ten', close(1 - 0.975 ** 20, 0.4, 0.01), 1 - 0.975 ** 20)
check('signal: 80% power needs 2.8^2 = 7.84 years', close((1.96 + 0.8416) ** 2, 7.84, 0.02))
rng = np.random.default_rng(2); okbh = True; seen_pass = 0
for _ in range(20000):
    kk = rng.integers(0, 20)
    ps = np.sort(np.concatenate([[0.025], rng.uniform(0.025, 0.05, kk), rng.uniform(0.05, 1, 19 - kk)]))
    passed = np.any(ps <= 0.05 * np.arange(1, 21) / 20)
    seen_pass += passed
    if passed and (ps <= 0.05).sum() < 10:
        okbh = False
ps = np.sort(np.concatenate([[0.025], np.linspace(0.03, 0.049, 19)]))
check('signal: Benjamini-Hochberg passes a best p of 0.025 only with ten or more versions under 0.05; all twenty under 0.05 pass', okbh and seen_pass > 0 and bool(np.any(ps <= 0.05 * np.arange(1, 21) / 20)), seen_pass)
ev = [20.6, 3.1, 2.4] + list(np.linspace(0.85, 0.17, 47))
check('pca: eigenvalues sum to about 50; shares 41%, 6%, 5%', close(sum(ev), 50, 0.1) and close(20.6 / 50, 0.41, 0.005) and round(3.1 / 50 * 100) == 6 and round(2.4 / 50 * 100) == 5, sum(ev))
cum = np.cumsum(ev) / 50
check('pca: 23 components are the first to reach 80%', int(np.argmax(cum >= 0.8)) + 1 == 23, int(np.argmax(cum >= 0.8)) + 1)
edge = (1 + math.sqrt(50 / 500)) ** 2
check('pca: noise edge 1.73; residual mean 0.51; rescaled bar 0.88; fourth (0.85) below both', close(edge, 1.73, 5e-3) and close((50 - 26.1) / 47, 0.51, 5e-3) and close((50 - 26.1) / 47 * edge, 0.88, 5e-3) and 0.85 < 0.88)
check('pca: the rescaled bar 0.88 is called stricter, so it must be the higher bar', not ('stricter bar' in item('research-int', 'homework-2', 'h2-pca-aloud')['widget']['model'] and 0.88 < edge), 'content calls 0.88 a stricter bar than 1.73; it is the lower one')
rng = np.random.default_rng(9); tops = []
for _ in range(300):
    X = rng.standard_normal((500, 50))
    tops.append(np.linalg.eigvalsh(np.corrcoef(X, rowvar=False))[-1])
tops = np.array(tops)
check('pca MC: largest eigenvalue of pure noise (50 by 500) sits near 1.73 and far below 2.4', 1.55 < tops.mean() < 1.80 and tops.max() < 2.0, (tops.mean(), tops.max()))
# three-factor data: three eigenvalues clear the edge, the fourth does not
hit = 0
for _ in range(100):
    f = rng.standard_normal((500, 3)); L = np.column_stack([np.full(50, 0.63), np.where(np.arange(50) < 25, 0.25, -0.25), np.where(np.arange(50) % 2 == 0, 0.22, -0.22)])
    X = f @ L.T + rng.standard_normal((500, 50)) * math.sqrt(0.5)
    e = np.linalg.eigvalsh(np.corrcoef(X, rowvar=False))[::-1]
    hit += (e[2] > edge) and (e[3] < edge)
check('pca MC: with three planted factors, exactly three eigenvalues clear the edge', hit >= 95, hit)
# PCA ranks variance, not prediction: target loaded on the smallest component
X = rng.standard_normal((5000, 2)) * np.array([3.0, 0.3]); y = X[:, 1] + 0.05 * rng.standard_normal(5000)
check('pca MC: a small-variance component can carry the whole forecast', abs(np.corrcoef(X[:, 0], y)[0, 1]) < 0.05 and np.corrcoef(X[:, 1], y)[0, 1] > 0.95)
R = np.full((50, 50), 0.6); np.fill_diagonal(R, 1)
check('pca: equicorrelation first eigenvalue 1 + 49 rho: 20.6 at 0.4, 30.4 at 0.6 (61%)', close(np.linalg.eigvalsh(R)[-1], 30.4, 1e-9) and close(1 + 49 * 0.4, 20.6, 1e-9) and round(30.4 / 50 * 100) == 61)
it = item('research-int', 'homework-4', 'h4-quote-at'); wd = it['widget']
res = run_py(wd, wd['solution']); res0 = run_py(wd, wd['starter'])
check('quote_at: solution passes all %d hidden tests' % len(res), all(res), res)
check('quote_at: starter fails', not any(res0), res0)
REF = r'''
def quote_at(quotes, times, max_gap):
    from fractions import Fraction
    d = {}
    for t, p in quotes:
        if p is not None: d.setdefault(t, []).append(p)
    pts = sorted((t, sum(v) / len(v)) for t, v in d.items())
    out = []
    for t in times:
        if not pts: out.append(None); continue
        exact = [y for x, y in pts if x == t]
        if exact: out.append(exact[0]); continue
        lo = [(x, y) for x, y in pts if x < t]; hi = [(x, y) for x, y in pts if x > t]
        if not lo: out.append(hi[0][1] if hi[0][0] - t <= max_gap else None)
        elif not hi: out.append(lo[-1][1] if t - lo[-1][0] <= max_gap else None)
        elif hi[0][0] - lo[-1][0] > max_gap: out.append(None)
        else:
            (x0, y0), (x1, y1) = lo[-1], hi[0]
            w = (t - x0) / (x1 - x0); out.append(y0 * (1 - w) + y1 * w)
    return out
'''
resr = run_py(dict(wd, tests=wd['tests'][:-1] + [{'call': 'big_case(1500)', 'expect': repr((lambda n_: (exec(wd['solution'] + '\n' + wd['postlude'], n_), n_['big_case'](1500))[1])({})), 'compare': 'isclose'}]), REF)
check('quote_at: an independent linear-scan version (other interpolation form) passes the rule tests and a random case', all(resr), resr)
# look-ahead: the interpolated value at t changes when a later quote changes
ns = {}; exec(wd['solution'], ns)
la = ns['quote_at']([(0, 100.0), (10, 101.0)], [4], 60)[0] != ns['quote_at']([(0, 100.0), (10, 105.0)], [4], 60)[0]
txt = json.dumps(it, ensure_ascii=False).lower()
warn = any(s in txt for s in ('later quote', 'after the fact', 'look-ahead', 'not known at', 'live'))
check('quote_at: the answer at t reads a later quote, so the item must say it is not a live value', (not la) or warn, 'value at second 4 depends on the quote at second 10; the item carries no warning')
u_ = np.array([2, 1, 2, 4.0]); Am = np.eye(4) + np.outer(u_, u_)
check('rank one: det 26, trace 29, u.u 25', close(np.linalg.det(Am), 26, 1e-9) and close(np.trace(Am), 29, 1e-12) and u_ @ u_ == 25)

# ------------------------------------------------------------------ systems
print('== systems')
check('branch: 3,000,000 misses, 15 ms of 25 ms (60%), 2.5 times; 99%: 0.5 ms; half: 25 ms', close(10_000_000 * 0.3 * 5e-9, 0.015, 1e-12) and close(15 / 25, 0.6, 1e-12) and 25 / 10 == 2.5 and close(1e7 * 0.01 * 5e-6, 0.5, 1e-9) and close(1e7 * 0.5 * 5e-6, 25, 1e-9))
pi = np.array([(3 / 7) ** i for i in range(4)]); pi /= pi.sum()
exact2 = pi[2:].sum() * 0.7 + pi[:2].sum() * 0.3
rng = np.random.default_rng(1); taken = rng.random(2_000_000) < 0.3; st = 0; miss = 0
for tk in taken.tolist():
    miss += (st >= 2) != tk
    st = min(3, st + 1) if tk else max(0, st - 1)
check('branch: two-bit counter is wrong about 36 in 100 at 30 in 100 passes (exact %.4f, sim %.4f), about 18 ms' % (exact2, miss / 2e6), close(exact2, 0.36, 5e-3) and close(miss / 2e6, exact2, 2e-3) and close(exact2 * 1e7 * 5e-6, 18, 0.2))
# branchless rewrite equals the branchy loop and never writes past kept + 1
rng = random.Random(4); okb = True
for _ in range(300):
    pr = [rng.randrange(100) for _ in range(rng.randrange(0, 30))]; lim = rng.randrange(100)
    want = [x for x in pr if x <= lim]; out = [None] * (len(pr) + 1); kk = 0; hi_w = -1
    for x in pr:
        out[kk] = x; hi_w = max(hi_w, kk); kk += (x <= lim)
    okb &= out[:kk] == want and hi_w <= min(len(pr) - 1, len(want))
check('branch: the rewrite keeps the same prices; its highest store is at most index kept, inside n slots', okb)
check('process: 0.4 + 5 = 5.4 us; 108 ms a second; 11% of a core; wake is 93%; wait 3.4 us', close(2 * 0.2 + 2 + 1 + 2, 5.4, 1e-12) and close(20000 * 5.4 / 1000, 108, 1e-9) and round(10.8) == 11 and round(100 / 108 * 100) == 93 and close(1 + 2 + 0.4, 3.4, 1e-12))
check('r1 branch budget: 10% (slips 20 and 0.1)', 200 * 0.5 * 5 / 5000 * 100 == 10 and 200 * 5 / 5000 * 100 == 20)
check('r2 queue fills after 12 ms (slips 2.4 and 3)', close(600 / (250000 - 200000) * 1000, 12, 1e-9) and close(600 / 250000 * 1000, 2.4, 1e-9) and close(600 / 200000 * 1000, 3, 1e-9))
def offs(sizes, align):
    o = 0; res_ = []
    for s in sizes:
        if align: o = (o + s - 1) // s * s
        res_.append(o); o += s
    return res_
check('r3 offset: 13 packed, 16 with natural alignment', offs([1, 4, 8, 4, 4], False)[3] == 13 and offs([1, 4, 8, 4, 4], True)[3] == 16)
check('r4 burst: 1,000 arrive, 800 handled, 200 wait, 100 a millisecond', close(500000 * 0.002, 1000, 1e-9) and close(2000 / 2.5, 800, 1e-9) and close(500000 / 1000 - 1000 / 2.5, 100, 1e-9))

it = item('systems', 'homework-4', 'h4-spsc-ring'); wd = it['widget']
gxx = shutil.which('g++')
if not gxx:
    skipped.append('SPSC ring C++ checks (no g++)')
else:
    tmp = tempfile.mkdtemp(prefix='delta1-')
    PRE = '#include <cstdlib>\n#include <new>\n#include <cstdio>\n#include <thread>\nstatic long g_allocs = 0;\nvoid* operator new(std::size_t n) { ++g_allocs; void* p_ = std::malloc(n); if (!p_) std::abort(); return p_; }\nvoid operator delete(void* p_) noexcept { std::free(p_); }\nvoid operator delete(void* p_, std::size_t) noexcept { std::free(p_); }\nstatic void reset_alloc_count() { g_allocs = 0; }\nstatic long alloc_count() { return g_allocs; }\n'
    def cxx(src, flags=(), run=True):
        pth = os.path.join(tmp, 'a.cpp'); exe = os.path.join(tmp, 'a.out')
        open(pth, 'w').write(src)
        c = subprocess.run([gxx, '-std=c++17', '-O1', '-pthread', *flags, pth, '-o', exe], capture_output=True, text=True)
        if c.returncode != 0:
            return None
        if not run:
            return ''
        r_ = subprocess.run([exe], capture_output=True, text=True, timeout=300)
        return r_.stdout if r_.returncode == 0 else 'RC%d %s' % (r_.returncode, r_.stderr[-300:])
    def run_cpp(code):
        out = []
        for t_ in wd['tests']:
            if 'compiles' in t_:
                got = cxx(PRE + code + '\nint main(){ ' + t_['compiles'] + ' return 0; }\n', run=False)
                out.append((got is not None) == t_['expect'])
                continue
            body = t_.get('setup', '') + '\n auto res__ = (' + t_['call'] + ');\n'
            exp = t_['expect']
            if isinstance(exp, list):
                body += 'std::vector<long long> want__{' + ','.join(str(int(x)) for x in exp) + '}; bool ok__ = res__.size() == want__.size(); for (std::size_t i__ = 0; ok__ && i__ < want__.size(); ++i__) ok__ = res__[i__] == want__[i__];'
            else:
                body += 'bool ok__ = (static_cast<long long>(res__) == %d);' % (int(exp))
            got = cxx(PRE + code + '\nint main(){ ' + body + ' std::printf(ok__ ? "PASS" : "MISS"); return 0; }\n')
            out.append(got == 'PASS')
        return out
    res = run_cpp(wd['solution'])
    check('spsc ring: solution passes all %d hidden tests under g++' % len(res), all(res), res)
    res0 = run_cpp(wd['starter'])
    check('spsc ring: starter fails (at least the behaviour tests)', not all(res0) and sum(res0) <= 3, res0)
    STRESS = PRE + wd['solution'] + r'''
int main() {
    static TickRing<64> r; const long long M = 2000000; long long bad = 0, sum = 0;
    r.head_.store(4294967295u - 1000); r.tail_.store(4294967295u - 1000);
    std::thread prod([&] { for (long long v = 1; v <= M;) if (r.try_push(v)) ++v; });
    std::thread cons([&] { long long want = 1, x = 0; std::vector<long long> buf; buf.reserve(64);
        while (want <= M) {
            if (want % 3 == 0) { buf.clear(); int n = r.drain(buf, 5); for (int i = 0; i < n; ++i) { if (buf[i] != want) ++bad; sum += buf[i]; ++want; } }
            else if (r.try_pop(x)) { if (x != want) ++bad; sum += x; ++want; }
            int s = r.size(); if (s < 0 || s > 64) ++bad;
        } });
    prod.join(); cons.join();
    std::printf((bad == 0 && sum == M * (M + 1) / 2) ? "PASS" : "MISS"); return 0; }
'''
    got = cxx(STRESS, flags=('-O2',))
    check('spsc ring: two-thread stress across the counter wrap keeps every tick in order', got == 'PASS', got)
    got = cxx(STRESS.replace('2000000', '200000'), flags=('-fsanitize=thread', '-g'))
    if got is None or (got or '').startswith('RC') and 'ThreadSanitizer' not in (got or '') and 'data race' not in (got or ''):
        if got is None or 'unexpected memory mapping' in got or 'FATAL' in got or got.startswith('RC'):
            skipped.append('SPSC ring ThreadSanitizer run (tsan unavailable here: %s)' % (str(got)[:80]))
        else:
            check('spsc ring: ThreadSanitizer reports no data race', False, got)
    else:
        check('spsc ring: ThreadSanitizer reports no data race', got == 'PASS', got)
    LAY = PRE + wd['solution'] + '\nint main(){ TickRing<8> r; long long d = (const char*)&r.tail_ - (const char*)&r.head_; std::printf((alignof(TickRing<8>) == 64 && (d == 64 || d == -64) && sizeof(unsigned) == 4) ? "PASS" : "MISS"); }\n'
    check('spsc ring: counters are 64-aligned, 64 bytes apart, and unsigned is 32 bits', cxx(LAY) == 'PASS')
    shutil.rmtree(tmp, ignore_errors=True)
check('spsc ring: masked slot order survives the wrap because N divides 2^32', all(((2 ** 32 - 3 + i) % 2 ** 32) & 7 == ((2 ** 32 - 3) % 8 + i) % 8 for i in range(20)) and (3 - 4294967291) % 2 ** 32 == 8)

# ---------------------------------------------------------------------- ito
print('== ito')
rng = np.random.default_rng(6)
W = rng.standard_normal(2_000_000)  # W_1
check('ito: E[exp(W_t - t/2)] = 1 at t = 1, not exp(-1/2)', close(np.exp(W - 0.5).mean(), 1.0, 0.01), np.exp(W - 0.5).mean())
ss = np.linspace(0, 1, 2001); check('ito: integral of E exp(2W_s - s) over [0, 1] is e - 1', close(np.trapezoid(np.exp(ss), ss), math.e - 1, 1e-6))
# quadratic-variation weights: Var(sum g_i((dW)^2 - dt)) <= 2 sup g^2 t dt
nst = 200; dW = rng.standard_normal((20000, nst)) * math.sqrt(1 / nst); Wp = np.cumsum(dW, axis=1) - dW
gw = np.clip(Wp, -1, 1); sm = (gw * (dW ** 2 - 1 / nst)).sum(axis=1)
check('ito: weighted squared increments have mean 0 and variance under 2 sup g^2 t dt', abs(sm.mean()) < 4 * sm.std() / math.sqrt(20000) and sm.var() <= 2 * 1 * 1 / nst, (sm.mean(), sm.var(), 2 / nst))
# why-not-chain: sum of simple returns minus log return is about sigma^2 T / 2 on every path
mu, sg = 0.08, 0.2
for steps in (252, 252 * 16):
    z = rng.standard_normal((2000, steps)); ret = mu / steps + sg * math.sqrt(1 / steps) * z
    gap = ret.sum(axis=1) - np.log1p(ret).sum(axis=1)
    check('ito: Euler gap at %d steps is 0.02 on every path (sd %.5f)' % (steps, gap.std()), close(gap.mean(), 0.02, 4e-4) and gap.std() < 0.004)
check('ito: seeded numbers 0.2799 - 0.2599 = 0.0199 (0.27986 - 0.25992), ln(1.296833) = 0.2599', close(math.log(1.296833), 0.2599, 5e-5) and close(0.27986 - 0.25992, 0.0199, 5e-5))
check('ito: median growth zero at 8% drift and 40% volatility; drag 2 and 8 points', close(0.08 - 0.5 * 0.4 ** 2, 0, 1e-12) and close(0.5 * 0.2 ** 2, 0.02, 1e-12) and close(0.5 * 0.4 ** 2, 0.08, 1e-12))
# Black's equation: V_t + 0.5 s^2 F^2 V_FF - r V = 0 for the forward claim and for Black-76
r_, s_, T_, K_ = 0.04, 0.25, 1.0, 100.0
def black76(t_, F):
    tau = T_ - t_; d1 = (math.log(F / K_) + 0.5 * s_ ** 2 * tau) / (s_ * math.sqrt(tau)); d2 = d1 - s_ * math.sqrt(tau)
    return math.exp(-r_ * tau) * (F * Phi(d1) - K_ * Phi(d2))
def pde(V, t_, F, h=1e-3):
    Vt = (V(t_ + h, F) - V(t_ - h, F)) / (2 * h); hf = 0.05
    Vff = (V(t_, F + hf) - 2 * V(t_, F) + V(t_, F - hf)) / hf ** 2
    return Vt + 0.5 * s_ ** 2 * F ** 2 * Vff - r_ * V(t_, F)
check('black: e^{-r(T-t)}(F - K) solves the equation', all(abs(pde(lambda a, F: math.exp(-r_ * (T_ - a)) * (F - K_), 0.3, F)) < 1e-6 for F in (80, 100, 130)))
check('black: the Black-76 call solves the equation (and would not with a +rFV_F term)', all(abs(pde(black76, 0.3, F)) < 1e-4 for F in (80, 100, 130)) and abs(pde(black76, 0.3, 100) + r_ * 100 * (black76(0.3, 100.05) - black76(0.3, 99.95)) / 0.1) > 0.5)
# hedge: discrete delta hedge of the Black-76 call with e^{r(TF-t)} V_F shares replicates the payoff
TF = 1.5; nst = 2000; npth = 4000; dt_ = T_ / nst; mu_ = 0.11
S = np.full(npth, 100 * math.exp(-r_ * TF)); F = S * math.exp(r_ * TF)
vPhi = np.vectorize(Phi)
def VF(t_, F):
    tau = T_ - t_; d1 = (np.log(F / K_) + 0.5 * s_ ** 2 * tau) / (s_ * math.sqrt(tau)); return math.exp(-r_ * tau) * vPhi(d1)
V0 = black76(0.0, 100.0); delta = math.exp(r_ * TF) * VF(0.0, F); cash = V0 - delta * S
for i in range(nst):
    t_ = i * dt_
    S = S * np.exp((mu_ - 0.5 * s_ ** 2) * dt_ + s_ * math.sqrt(dt_) * rng.standard_normal(npth)); cash = cash * math.exp(r_ * dt_)
    if i < nst - 1:
        F = S * math.exp(r_ * (TF - t_ - dt_)); nd = math.exp(r_ * (TF - t_ - dt_)) * VF(t_ + dt_, F); cash -= (nd - delta) * S; delta = nd
F = S * math.exp(r_ * (TF - T_)); err = cash + delta * S - np.maximum(F - K_, 0)
check('black MC: holding e^{r(T_F - t)} V_F shares replicates the claim under a real-world drift of 11%', abs(err.mean()) < 0.05 and err.std() < 0.5, (err.mean(), err.std()))
check('black: e^{0.06} = 1.0618; forward drift mu - r by Ito', close(math.exp(0.06), 1.0618, 5e-5))

# ------------------------------------------------------------- measure-prob
print('== measure-prob')
check('space: partial sums 1 - 1/(m+1); tail P(T_n) = 1/n', all(sum(Fr(1, k * (k + 1)) for k in range(1, m + 1)) == 1 - Fr(1, m + 1) for m in range(1, 40)) and all(1 - sum(Fr(1, k * (k + 1)) for k in range(1, n)) == Fr(1, n) for n in range(1, 40)) and all(sum(Fr(1, k * (k + 1)) for k in range(n, m + 1)) == Fr(1, n) - Fr(1, m + 1) for n in range(1, 8) for m in range(n, 20)))
okE = True
for n in range(1, 9):
    N = 2 ** n
    okE &= sum(Fr(k, N) * Fr(2 * k + 1, N * N) for k in range(N)) == Fr((N - 1) * (4 * N + 1), 6 * N * N)
    okE &= Fr(2, 3) - Fr((N - 1) * (4 * N + 1), 6 * N * N) == Fr(3 * N + 1, 6 * N * N)
check('integral: E[phi_n] = (N-1)(4N+1)/(6N^2), shortfall (3N+1)/(6N^2); 3/8 and 231/384', okE and Fr(1 * 9, 24) == Fr(3, 8) and Fr(7 * 33, 384) == Fr(231, 384) and close(231 / 384, 0.6016, 5e-5))
U = np.random.default_rng(12).random(2_000_000); Xs = np.sqrt(U)
okm = all(np.all(np.floor(2 ** n * Xs) / 2 ** n <= np.floor(2 ** (n + 1) * Xs) / 2 ** (n + 1)) and np.all(Xs - np.floor(2 ** n * Xs) / 2 ** n < 2.0 ** -n) for n in range(1, 8))
check('integral MC: phi_n rises with n, lies within 2^-n below X, and E[X] = 2/3', okm and close(Xs.mean(), 2 / 3, 1e-3))
Y = 2 * Xs - 1
check('integral MC: E[Y+] = 5/12, E[Y-] = 1/12, E[Y] = 1/3', close(np.maximum(Y, 0).mean(), 5 / 12, 1e-3) and close(np.maximum(-Y, 0).mean(), 1 / 12, 1e-3) and close(Y.mean(), 1 / 3, 2e-3))
# urn: exact enumeration over every string of draws
okU = True; okR = True
for n in range(0, 9):
    for s in itertools.product((0, 1), repeat=n):
        Rn = 1 + sum(s); Mn = Fr(Rn, n + 2)
        nxt = Mn * Fr(Rn + 1, n + 3) + (1 - Mn) * Fr(Rn, n + 3)
        okU &= nxt == Mn and 0 < Mn < 1
        okR &= Mn * (Rn + 1) + (1 - Mn) * Rn == Rn + Mn
def pstr(s):
    pr = Fr(1); Rn = 1
    for i, d in enumerate(s):
        pr *= Fr(Rn, i + 2) if d else 1 - Fr(Rn, i + 2); Rn += d
    return pr
okP = all(sum(pstr(s) for s in itertools.product((0, 1), repeat=n) if s[-1] == 1) == Fr(1, 2) for n in range(1, 10))
check('urn: E[M_{n+1} | atom] = M_n on every atom up to n = 8, with 0 < M_n < 1', okU)
check('urn: every draw is red with chance 1/2; E[R_{n+1} | F_n] = R_n + M_n', okP and okR and Fr(3, 4) * Fr(4, 5) + Fr(1, 4) * Fr(3, 5) == Fr(3, 4))

print()
for s in skipped:
    print('SKIPPED: ' + s)
print('%d checks, %d failed%s' % (n_checks, len(fails), (': ' + '; '.join(fails)) if fails else ''))
sys.exit(1 if fails else 0)
