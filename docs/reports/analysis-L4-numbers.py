"""Second read of analysis level 4 (Continuity and the derivative): recompute every number stated in l15 to l19,
review-4 and homework-4. Run: python3 docs/reports/analysis-L4-numbers.py   (standard library only; exits 0 on correct content)
Written by the second reader (docs/reviews/review-analysis-3-4.md). Route 1 is exact (Fraction or a closed form), route 2 a
float computation or a second formula (grid search, bisection, statistics.NormalDist). `two` asserts the routes agree; `E`
(lv.expect) checks the value where it is stated. Every code widget is run in CPython (solution passes every hidden test,
starter fails one) and check_wrongs (rule 581) runs at the end. No review finding of this level changes a stated number,
so every check here passes on the current content.
"""
import sys, os, math, re
from fractions import Fraction as F
from statistics import NormalDist
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("analysis", 4)
E = lv.expect
doc = lambda ref: lv._file(ref)[1]


def two(name, a, b, tol=1e-9):
    lv._rec(math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol), f'two routes: {name}', f'{a!r} vs {b!r}')


def ok(name, cond, note=''):
    lv._rec(bool(cond), name, note)


def node(ref, path):
    n = doc(ref)
    for key, idx in re.findall(r'(\w+)(?:\[(\d+)\])?', path):
        n = n[key]
        if idx:
            n = n[int(idx)]
    return n


rnd = lambda x, k: float(f'{float(x):.{k}f}')


def largest_delta(f, a, eps, lo=0.0, hi=1.0):
    """Largest delta with |f(x) - f(a)| < eps on the open window (a - delta, a + delta), by bisection. f is monotone on each
    side of a for every function used here, so checking points just inside both ends and a grid between suffices."""
    def works(d):
        xs = [a - d * (1 - 1e-12), a + d * (1 - 1e-12)] + [a - d + d * 2 * k / 400 for k in range(1, 400)]
        return all(abs(f(x) - f(a)) < eps for x in xs)
    for _ in range(80):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if works(m) else (lo, m)
    return lo

# ================= l15 =================
sq = lambda x: x * x
dmax = math.sqrt(4.1) - 2
two('largest delta x^2 at 2, eps 0.1', largest_delta(sq, 2, 0.1, 0, 0.1), dmax, 1e-5)
two('sqrt(4.1) - 2', rnd(dmax, 6), 0.024846); two('2 - sqrt(3.9)', rnd(2 - math.sqrt(3.9), 6), 0.025158)
E('l15', 'screens[0].explain.text', 0.024846); E('l15', 'screens[0].explain.text', 0.025158)
w = node('l15', 'screens[0]')['widget']
lo, hi = w['answer'] - w['tol'], w['answer'] + w['tol']
reach = [round(w['min'] + k * w['step'], 6) for k in range(int(round((w['max'] - w['min']) / w['step'])) + 1)]
ok('l15 slider: every reachable delta that works is accepted', all(lo <= d <= hi for d in reach if d < dmax))
ok('l15 slider: every reachable delta that fails is outside the band', all(not (lo <= d <= hi) for d in reach if d > dmax))
ok('l15 slider: every failing reachable delta lands in a wrong range', all(any(r['from'] <= d <= r['to'] for r in w['wrong']) for d in reach if d > dmax))
two('2.025^2', 2.025 ** 2, 4.100625)
two('widest window sqrt(4+eps)-2 binds (eps 0.05)', largest_delta(sq, 2, 0.05, 0, 0.1), math.sqrt(4.05) - 2, 1e-5)
ok('3x+1: delta eps/3 works', all(abs(3 * (2 + t) + 1 - 7) < 0.3 for t in [-0.0999, 0.0999]))
two('eps/5 at 0.1', 0.1 / 5, 0.02); E('l15', 'screens[5].explain.text', 0.02); E('l15', 'quiz[0].widget.answer', 0.02)
ok('min(1, eps/5) works for x^2 at 2 (eps 0.1, 1, 3)', all(largest_delta(sq, 2, e, 0, 2) >= min(1, e / 5) - 1e-9 for e in (0.1, 1, 3)))
two('2.09^2', 2.09 ** 2, 4.3681); two('gap', 2.09 ** 2 - 4, 0.3681); E('l15', 'screens[7].widget.answer', 0.3681)
ok('sin(1/x_n) = 1 at x_n = 1/(2 pi n + pi/2)', all(abs(math.sin(2 * math.pi * n + math.pi / 2) - 1) < 1e-9 for n in range(1, 50)))
rec = lambda x: 1 / x
for a, e, d in [(0.5, 1, 0.125), (0.2, 1, 0.02), (0.1, 0.1, 0.0005)]:
    two(f'1/x delta a={a} eps={e}', min(a / 2, a * a * e / 2), d)
    ok(f'1/x delta works a={a} eps={e}', largest_delta(rec, a, e, 0, a * 0.9) >= d)
    two(f'1/x largest delta a={a} eps={e} is a^2 eps/(1 + a eps)', largest_delta(rec, a, e, 0, a * 0.9), a * a * e / (1 + a * e), 1e-5)
E('l15', 'quiz[4].widget.answer', 0.0005); E('l15', 'quiz[4].widget.wrong[1].value', 0.001); E('l15', 'quiz[4].widget.wrong[0].value', 0.05)
two('worst gap 1/0.0995 - 10', rnd(1 / 0.0995 - 10, 4), 0.0503)
two('spot tolerance', 0.03 / 0.6, 0.05); two('times', 0.03 * 0.6, 0.018)
ok('x^2 at 3: cap gives |x+3| < 7', 2 + 3 < 7 and 4 + 3 == 7)
two('2|a|+1 at 3', 2 * 3 + 1, 7)

# ================= l16 =================
f = lambda x: x ** 3 - x - 1
a, b, mids = F(1), F(2), []
for _ in range(10):
    m = (a + b) / 2; mids.append(m)
    if f(m) < 0: a = m
    else: b = m
for i, v in enumerate([1.5, 1.25, 1.375, 1.3125, 1.34375]):
    two(f'midpoint {i + 1}', mids[i], v)
for v, s in zip(mids[:5], ['0.875', '-0.296875', '0.224609', '-0.051514', '0.082611']):
    two(f'f({float(v)})', rnd(f(v), 6), float(s))
two('after 10 left', a, 1.32421875); two('after 10 right', b, 1.3251953125); two('width', b - a, F(1, 1024))
root = 1.5
for _ in range(80):
    root -= f(root) / (3 * root * root - 1)
two('root 1.324718', rnd(root, 6), 1.324718); ok('root inside after 10', a < root < b)
two('1/1024', rnd(F(1, 1024), 6), 0.000977); two('nine', F(1, 512), 0.001953125)
two('2^19 < 10^6 < 2^20', (2 ** 19 < 10 ** 6 < 2 ** 20) * 20, 20)
ok('root irrational: no rational root +-1', f(1) != 0 and f(-1) != 0)
def bs(S, K, T, s):
    d1 = (math.log(S / K) + s * s * T / 2) / (s * math.sqrt(T)); d2 = d1 - s * math.sqrt(T)
    N = NormalDist().cdf
    return S * N(d1) - K * N(d2)
for s, p in [(0.1, 3.99), (0.2, 7.97), (0.3, 11.92)]:
    two(f'BS {s}', rnd(bs(100, 100, 1, s), 2), p)
    two(f'BS closed form {s}', bs(100, 100, 1, s), 100 * (2 * 0.5 * (1 + math.erf(s / 2 / math.sqrt(2))) - 1), 1e-9)
lo_, hi_ = 0.1, 0.3
for _ in range(60):
    m = (lo_ + hi_) / 2
    lo_, hi_ = (m, hi_) if bs(100, 100, 1, m) < 8 else (lo_, m)
two('implied vol', rnd(lo_, 6), 0.200867); two('20.09%', rnd(100 * lo_, 2), 20.09)
two('halvings 0.2 to 1e-4', next(n for n in range(40) if 0.2 / 2 ** n <= 1e-4), 11)
two('0.2/2^11', float(f'{0.2 / 2 ** 11:.3g}'), 0.0000977); two('0.2/2^10', float(f'{0.2 / 2 ** 10:.3g}'), 0.000195)
two('from width 1', next(n for n in range(40) if 1 / 2 ** n <= 1e-4), 14)
two('quiz width 1/16', F(1375, 1000) - F(13125, 10000), F(1, 16))
two('quiz steps 0.001', next(n for n in range(40) if F(1, 2 ** n) <= F(1, 1000)), 10); two('1/512', rnd(F(1, 512), 5), 0.00195)
two('g(+-2)', (-2) ** 3 + 2, -6)

# ================= l17 =================
g = lambda x: x ** 3 - 3 * x
for x, v in [(0, 0), (1, -2), (2, 2), (-1, 2), (-2, -2)]:
    two(f'f({x})', g(x), v)
grid = [-2 + 4 * k / 40000 for k in range(40001)]
two('max on [-2,2]', max(map(g, grid)), 2); two('min on [-2,2]', min(map(g, grid)), -2)
two("f'(2)", 3 * 4 - 3, 9); two('far slip', -8 - 6, -14); E('l17', 'screens[10].widget.answer', 2000); E('l17', 'screens[10].widget.wrong[1].value', 14000)
pq = {p['id']: (p['x'], p['y']) for p in node('l17', 'screens[2]')['canvas']['state']['points']}
ok('l17 s2 candidate dots', all(abs(g(x) - y) < 1e-9 for x, y in pq.values()))

# ================= l18 =================
two('g(x) for x^2 on [1,3]', all(x * x - 1 - 4 * (x - 1) == x * x - 4 * x + 3 for x in range(-5, 6)) * 1, 1)
two('slope slip', all(x * x - 1 - 8 * (x - 1) == x * x - 8 * x + 7 for x in range(-5, 6)) * 1, 1)
two('c for x^3 on [0,3]', rnd(math.sqrt(3), 3), 1.732); two("f'(1.5)", 3 * 1.5 ** 2, 6.75); two('chord', 27 / 3, 9)
two('spread profit', 8.00 - 2.50 - 5, 0.5); two('sum of premiums', 8 + 2.5, 10.5)
ok('call spread payout in [0, 5]', all(0 <= max(S - 100, 0) - max(S - 105, 0) <= 5 for S in range(0, 300)))
ok('x^2 sin(1/x): quotient |x sin(1/x)| <= |x|', all(abs(x * math.sin(1 / x)) <= abs(x) for x in [1e-3 * k for k in range(1, 100)]))

# ================= l19 =================
two('0.9^43', rnd(0.9 ** 43, 5), 0.01078); two('0.9^44', rnd(0.9 ** 44, 5), 0.00970)
two('first n', next(n for n in range(200) if 0.9 ** n < 0.01), 44); two('ln ratio', rnd(math.log(0.01) / math.log(0.9), 1), 43.7)
two('log slip', math.ceil(math.log(0.1) / math.log(0.9)), 22)
bump = lambda n, x: n * x / (1 + n * n * x * x)
ok('bump peak 1/2 at 1/n', all(abs(bump(n, 1 / n) - 0.5) < 1e-12 and max(bump(n, k / 100000) for k in range(100001)) <= 0.5 + 1e-12 for n in (1, 2, 10, 50)))
two('bump at 1', bump(10, 1), 10 / 101); E('l19', 'screens[4].widget.wrong[2].value', 10 / 101)
two('grid n=3 m=10', bump(3, 0.3), F(90, 181)); two('90/181', rnd(F(90, 181), 5), 0.49724)
ok('tail of 1/k^2 below 1/N', all(math.pi ** 2 / 6 - math.fsum(1 / k ** 2 for k in range(1, N + 1)) < 1 / N for N in range(1, 60)))
two('digital error at 100 + 1/n', rnd(100 / (1 + math.e), 2), 26.89); two('smooth value', rnd(100 / (1 + math.exp(-1)), 2), 73.11)
two('triangle area', F(1, 2) * F(2, 5) * 5, 1)
two('sqrt((x-1/2)^2 + 1/n) - |x - 1/2| <= 1/sqrt n', max(math.sqrt((k / 1000 - 0.5) ** 2 + 0.01) - abs(k / 1000 - 0.5) for k in range(1001)), 0.1, 1e-9)

# ================= review-4 =================
h = lambda x: x * x + x
two('r0 delta', min(1, 0.2 / 4), 0.05); two('r0 three', 0.2 / 3, 0.06666666666666667)
two('r0 check', 0.05 * 3.05, 0.1525); two('r0 largest window', rnd(largest_delta(h, 1, 0.2, 0, 0.5), 4), 0.0652)
two('r1 f(1.5)', 1.5 ** 2 - 2, 0.25); two('r1 f(1.25)', 1.25 ** 2 - 2, -0.4375)
two('r3 chord', (F(1, 4) - 1) / 3, F(-1, 4)); two("r3 f'(2.5)", -1 / 2.5 ** 2, -0.16)
two('r7 tail', sum(F(1, 2 ** k) for k in range(6, 80)), F(1, 32)); two('r7 one', F(1, 64), 0.015625)

# ================= homework-4 =================
two('h4 n', next(n for n in range(60) if 0.2 / 2 ** n <= 1e-6), 18)
two('h4 2^17 width', float(f'{0.2 / 2 ** 17:.3g}'), 1.53e-6); two('h4 2^18 width', float(f'{0.2 / 2 ** 18:.3g}'), 7.63e-7)
two('h4 width 1', next(n for n in range(60) if 1 / 2 ** n <= 1e-6), 20); two('h4 per decimal', rnd(math.log2(10), 1), 3.3)
f4 = lambda x: x ** 4 * (1 - x)
two('h5 sup', F(4, 5) ** 4 * F(1, 5), F(256, 3125)); two('h5 sup by grid', max(f4(k / 100000) for k in range(100001)), 0.08192, 1e-8)
two('h5 half', f4(0.5), 0.03125); two('h5 noone', 0.8 ** 4, 0.4096)
ok('h5 sup <= 1/(n+1)', all((n / (n + 1)) ** n / (n + 1) <= 1 / (n + 1) for n in range(1, 100)))
two('h6 halvings', next(n for n in range(80) if (5 - 0.0001) / 2 ** n <= 1e-10), 36)
two('h8 delta', rnd(min(1, 0.1 / 7), 6), 0.014286); two('h8 largest', rnd(math.sqrt(9.1) - 3, 6), 0.016621)
two('h8 largest by search', largest_delta(sq, 3, 0.1, 0, 0.1), math.sqrt(9.1) - 3, 1e-5)
two('h8 left', rnd(3 - math.sqrt(8.9), 6), 0.016713); two('h8 ratio', rnd(100 * (1 / 70) / (math.sqrt(9.1) - 3), 0), 86)
ok('h8 rubric sums to 10', sum(r['points'] for r in node('homework', 'items[8]')['rubric']) == 10)
ok('h6 test prices: bs at 0.1 and 0.3', abs(bs(100, 100, 1, 0.1) - 3.987761167674492) < 1e-9 and abs(bs(100, 100, 1, 0.3) - 11.923538474048499) < 1e-9)

# ================= code widgets =================
def run_code(widget, src):
    ns = {}
    try:
        exec(src, ns)
    except Exception:
        return False
    good = True
    for t in widget['tests']:
        try:
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns); exp = eval(t['expect'], ns)
            if t.get('compare') == 'isclose':
                tol = t.get('tol') or {}
                ab, rel = tol.get('abs', 0), tol.get('rel', 0 if 'abs' in tol else 1e-9)
                pair = list(zip(got, exp)) if isinstance(exp, (list, tuple)) else [(got, exp)]
                good = good and all(math.isclose(x, y, rel_tol=rel, abs_tol=ab) for x, y in pair)
            else:
                good = good and got == exp
        except Exception:
            good = False
    return good
for ref, path in [('l16', 'screens[10]'), ('l19', 'screens[10]'), ('homework', 'items[6]')]:
    w = node(ref, path)['widget']
    ok(f'{ref} {path}: solution passes all {len(w["tests"])} tests', run_code(w, w['solution']))
    ok(f'{ref} {path}: starter fails a test', not run_code(w, w['starter']))
    ok(f'{ref} {path}: the solution meets every shown example', run_code({'tests': w.get('examples', [])}, w['solution']))
    m = re.search(r'runs (\d+) hidden tests', w.get('how', ''))
    ok(f'{ref} {path}: how states the test count', m and int(m.group(1)) == len(w['tests']))
# l19 how: "the rest use coarse grids, where the peak at 1/n falls between grid points" (review finding: false for (1, 1))
w = node('l19', 'screens[10]')['widget']
coarse = [eval(t['call'].replace('sup_gap_bump', '')) for t in w['tests'][5:]]
print('l19 coarse tests where 1/n IS a grid point:', [(n, m) for n, m in coarse if (F(1, n) * m).denominator == 1])

# ================= fix pass (review-analysis-3-4): new values, NEW value only =================
E('l19', 'screens[4].widget.wrong[2].tol.abs', 0.0002)
edge = 1 / 10.1
ok('l19 screens[4]: edge band [0.0988, 0.0992] is disjoint from tenth band [0.0995, 0.1005]', edge + 0.0002 < 0.1 - 0.0005 and edge - 0.0002 > 0)
for a in (1, 10, 100, 1000):
    two(f'x^2 largest delta at a={a}, eps 0.1 is sqrt(a^2+eps)-a', largest_delta(sq, a, 0.1, 0, 0.1), math.sqrt(a * a + 0.1) - a, 1e-5)
ok('x^2 largest delta shrinks as a grows', all(math.sqrt(a * a + 0.1) - a > math.sqrt(b * b + 0.1) - b for a, b in [(1, 10), (10, 100), (100, 1000)]))
rec2 = lambda x: 1 / x
ok('1/x largest delta shrinks to 0 as a -> 0 (eps 0.1)', all(0.01 * 0.01 * 0.1 / (1 + 0.01 * 0.1) < 0.1 * 0.1 * 0.1 / (1 + 0.1 * 0.1) < 0.5 * 0.5 * 0.1 / (1 + 0.05) for _ in [0]))
two('l15 screens[11]: 0.03 / 0.6 = 0.05', 0.03 / 0.6, 0.05)
ok('l15 screens[11] accept uses non-strict', '\\le 0.03' in node('l15', 'screens[11].widget.accept') and 'at most' in node('l15', 'screens[11].prose'))
ok('l19 how: states 12 tests and the m = 1 test', 'Six use coarse' in node('l19', 'screens[10].widget.how') and 'm = 1' in node('l19', 'screens[10].widget.how'))

lv.check_wrongs()
lv.report()
