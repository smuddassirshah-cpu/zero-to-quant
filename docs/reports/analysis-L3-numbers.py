"""Second read of analysis level 3 (Series): recompute every number stated in l11 to l14, review-3 and homework-3.
Run: python3 docs/reports/analysis-L3-numbers.py   (standard library only; exits 0 only on correct content)
Written by the second reader (docs/reviews/review-analysis-3-4.md). Route 1 is exact (fractions.Fraction or a closed form);
route 2 is a float sum or a second formula; `two` asserts the routes agree and `E` (lv.expect) checks the value where it is stated.
Checks that encode a fix from the review check the NEW value only, so they fail until the fix lands:
  - l13 quiz[3].widget.wrong[1].value must be 1000 (review finding: 999 does not match its feedback "you solved 1/(n+1) < 0.001");
  - homework-3 items[2] must use the series 3/(k(k+3)) (review finding: freshness, it repeated review-3 items[0]).
The script also runs every code widget in CPython (solution passes every hidden test, starter fails one), checks canvas
dots and bars against their formulas, and runs check_wrongs (rule 581).
"""
import sys, os, math, json, re
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("analysis", 3)
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


def pts(ref, path):
    return {p['id']: (p['x'], p.get('y')) for p in node(ref, path)['canvas']['state']['points']}


def rnd(x, k):
    return float(f'{float(x):.{k}f}')


H = lambda n: sum(F(1, k) for k in range(1, n + 1))
Hf = lambda n: math.fsum(1 / k for k in range(1, n + 1))
alt = lambda n: sum(F((-1) ** (k + 1), k) for k in range(1, n + 1))
LN2 = math.log(2)
GAMMA = 0.5772156649015329

# ================= l11 =================
S = lambda n: sum(F(1, k * (k + 1)) for k in range(1, n + 1))
for n in range(1, 41):
    assert S(n) == 1 - F(1, n + 1) == F(n, n + 1)
for i, v in enumerate([F(1, 2), F(2, 3), F(3, 4), F(4, 5)]):
    E('l11', f'screens[0].widget.rows[{i}][1].answer', rnd(v, 6))
two('S10', S(10), 10 / 11); E('l11', 'screens[1].explain.text', 0.9091)
for eps, N in [(F(1, 4), 4), (F(1, 10), 10), (F(1, 20), 20), (F(1, 25), 25), (F(1, 100), 100)]:
    first = next(n for n in range(1, 1000) if all(1 - S(m) < eps for m in range(n, n + 200)))
    two(f'band N eps={eps}', first, N)
for k, N in enumerate([4, 10, 20, 25]):
    E('l11', f'screens[2].canvas.controls[0].frames[{k}].caption', N)
E('l11', 'screens[2].widget.answer', 100)
ok('l11 s2 byKey.edge: S_99 gap is exactly 0.01', 1 - S(99) == F(1, 100))
ok('l11 s2 byKey.late: 1/101 < 0.01', F(1, 101) < F(1, 100))
# 'sq' wrong 10 comes from sqrt(100); 1/n^2 < 0.01 gives n = 11 (review finding: the feedback text, not the value)
ok('l11 s2 sq: 1/n^2 < 0.01 first at n = 11, so the wrong value 10 is sqrt(100)', next(n for n in range(1, 50) if F(1, n * n) < F(1, 100)) == 11)
p = pts('l11', 'screens[2]')
ok('l11 s2 dots are S_n', all(abs(p[f's{n}'][1] - float(S(n))) < 1e-6 for n in range(1, 31)))
p = pts('l11', 'screens[6]')
ok('l11 s6 dots are n/(n+1)', all(abs(p[f'a{n}'][1] - n / (n + 1)) < 1e-6 for n in range(1, 21)))
ok('l11 s6 S_n >= n/2', all(sum(F(k, k + 1) for k in range(1, n + 1)) >= F(n, 2) for n in range(1, 60)))
# grouping table and bound
tab = node('l11', 'screens[7]')['canvas']['params']['rows']
for row in tab[:5]:
    k = int(row[0]); two(f'S_2^{k}', float(row[2]), rnd(H(2 ** k), 4)); two(f'1+k/2 k={k}', float(row[3]), 1 + k / 2)
ok('S_{2^k} >= 1 + k/2 up to k = 14', all(Hf(2 ** k) >= 1 + k / 2 for k in range(0, 15)))
E('l11', 'screens[7].widget.answer', 6)
h1024 = Hf(1024); two('H_1024 by sum and by ln n + gamma + 1/2n', h1024, math.log(1024) + GAMMA + 1 / 2048 - 1 / (12 * 1024 ** 2), 1e-9)
two('H_1024 = 7.5092', rnd(h1024, 4), 7.5092); E('l11', 'screens[7].widget.wrong[2].value', 7.5092)
E('l11', 'screens[7].widget.wrong[1].value', 512)
ok('block j has 2^(j-1) terms, each >= 1/2^j', all(sum(F(1, m) for m in range(2 ** (j - 1) + 1, 2 ** j + 1)) >= F(1, 2) for j in range(1, 12)))
# code: first_exceeding
def first_exceeding_exact(t):
    tot, n = F(0), 0
    while tot <= t:
        n += 1; tot += F(1, n)
    return n
for t, n in [(2, 4), (3, 11), (4, 31), (5, 83), (1, 2), (F(3, 2), 3), (0, 1)]:
    two(f'first H_n > {t}', first_exceeding_exact(t), n)
two('first H_n > 10 (float sum)', next(n for n in range(12000, 13000) if Hf(n) > 10), 12367)
ok('H_12366 < 10 < H_12367 with margin', Hf(12366) < 10 - 1e-5 and Hf(12367) > 10 + 1e-5)
# dividend model
r = F(103, 108)
price = F(500, 108) / (1 - r); two('dividend price', price, 100)
ten = sum(F(5) * F(103, 100) ** (n - 1) / F(108, 100) ** n for n in range(1, 11))
two('first ten by sum and formula', ten, 100 * (1 - (1.03 / 1.08) ** 10)); two('37.75', rnd(ten, 2), 37.75)
E('l11', 'screens[11].widget.answer', 37.75); E('l11', 'screens[11].hints[2].text', 0.6225)
two('r^10', rnd(r ** 10, 4), 0.6225); two('5/1.08', rnd(F(5, 100) * 100 / F(108, 100), 2), 4.63)
two('ratio 0.9537', rnd(r, 4), 0.9537)
E('l11', 'screens[11].widget.wrong[0].value', 50)
two('grown', rnd(sum(5 * 1.03 ** (n - 1) for n in range(1, 11)), 2), 57.32); E('l11', 'screens[11].widget.wrong[1].value', 57.32)
two('flat', rnd(10 * 5 / 1.08, 2), 46.30); E('l11', 'screens[11].widget.wrong[2].value', 46.3)
bars = node('l11', 'screens[11]')['canvas']['state']['values']
ok('l11 bars are 5*1.03^(n-1)/1.08^n', all(abs(bars[str(n)] - 5 * 1.03 ** (n - 1) / 1.08 ** n) < 6e-5 for n in range(1, 11)))
ok('37.75 under two fifths of 100', ten < 40)
# quiz
two('q0 new sum', 15 + (1 - S(3)), 15.25); two('q0 shift', 15 - S(3), 14.25); E('l11', 'quiz[0].explain.text', 14.25)
two('q1 tail', 1 - S(4), 0.2); two('q1 early', 1 - S(3), 0.25); two('q1 late', rnd(1 - S(5), 6), 0.166667)
for n in range(2, 30):
    assert (2 - F(1, n)) - (2 - F(1, n - 1)) == F(1, n * (n - 1))
two('q3 S2-S1', (2 - F(1, 2)) - 1, 0.5)

# ================= l12 =================
T = lambda n: sum(F(1, 2 ** k + k) for k in range(1, n + 1))
for k, n in enumerate([1, 2, 3, 4, 6, 8, 10, 12]):
    cap = lv.text('l12', f'screens[0].canvas.controls[0].frames[{k}].caption')
    ok(f'l12 s0 caption T_{n}, B_{n}', f'{float(T(n)):.4f}' in cap and f'{1 - 2 ** -n:.4f}' in cap, cap)
Tinf = math.fsum(1 / (2 ** k + k) for k in range(1, 80)); two('T limit 0.6973', rnd(Tinf, 4), 0.6973)
E('l12', 'screens[0].explain.text', 0.6973)
p = pts('l12', 'screens[0]')
ok('l12 s0 dots', all(abs(p[f't{n}'][1] - float(T(n))) < 1e-6 and abs(p[f'b{n}'][1] - (1 - 2 ** -n)) < 1e-6 for n in range(1, 13)))
# ratio test example
ok('(n+1)/(2n) < 3/4 exactly when n > 2', all((F(n + 1, 2 * n) < F(3, 4)) == (n > 2) for n in range(1, 50)))
two('n/2^n sum', math.fsum(n / 2 ** n for n in range(1, 200)), 2); two('S10 of n/2^n', sum(F(n, 2 ** n) for n in range(1, 11)), F(509, 256))
two('509/256', rnd(F(509, 256), 4), 1.9883)
ok('a_{N+k} <= a_N r^k for n/2^n, N=3, r=3/4', all(F(3 + k, 2 ** (3 + k)) <= F(3, 8) * F(3, 4) ** k for k in range(0, 60)))
# n!/n^n
q = lambda n: (n / (n + 1)) ** n
two('ratio n=10', rnd(q(10), 4), 0.3855); two('ratio n=100', rnd(q(100), 4), 0.3697); two('1/e', rnd(1 / math.e, 4), 0.3679)
two('ratio identity', math.factorial(11) / 11 ** 11 / (math.factorial(10) / 10 ** 10), q(10))
for path, v in [('screens[7].widget.rows[2][1].answer', 0.3855), ('screens[7].widget.rows[3][1].answer', 0.3697), ('screens[7].widget.rows[4][1].answer', 0.3679)]:
    E('l12', path, v)
two('row n=2', rnd(q(2), 4), 0.4444)
tot = math.fsum(math.factorial(n) / n ** n for n in range(1, 120)); two('sum n!/n^n', rnd(tot, 4), 1.8799)
p = pts('l12', 'screens[7]')
ok('l12 s7 dots are (n/(n+1))^n', all(abs(p[f'q{n}'][1] - q(n)) < 1e-6 for n in range(1, 31)))
# integral bounds
for m in (1, 2, 5, 10, 20, 50, 100):
    tail = math.pi ** 2 / 6 - math.fsum(1 / k ** 2 for k in range(1, m + 1))
    ok(f'1/(m+1) < tail < 1/m at m={m}', 1 / (m + 1) < tail < 1 / m)
two('quiz3 integral', 1 / 0.1, 10)
z11 = math.fsum(n ** -1.1 for n in range(1, 2000000)) + (2000000 ** -0.1) / 0.1  # tail by the integral
ok('sum n^-1.1 lies between 10 and 11', 10 < z11 < 11, z11)
two('sum 1/(n^2+n) = 1', math.fsum(1 / (n * n + n) for n in range(1, 10 ** 6)) + 1e-6, 1, 1e-6)
two('pi^2/6', rnd(math.pi ** 2 / 6, 4), 1.6449)
# code sum_with_bounds
s10 = sum(F(1, k * k) for k in range(1, 11))
for v, ex in [(s10, 1.549768), (s10 + F(1, 11), 1.640677), (s10 + F(1, 10), 1.649768)]:
    two(f'bounds {ex}', rnd(v, 6), ex)
for path in ['screens[10].feedback.correct', 'screens[10].explain.text']:
    for v in (1.640677, 1.649768):
        E('l12', path, v)
two('pi^2/6 6dp', rnd(math.pi ** 2 / 6, 6), 1.644934)
ok('bounds width at n = 10 below 0.01', F(1, 10) - F(1, 11) < F(1, 100))
# Merton
lam = 2
w = lambda n: math.exp(-lam) * lam ** n / math.factorial(n)
tail10 = 1 - math.fsum(w(n) for n in range(0, 11)); tail10b = math.fsum(w(n) for n in range(11, 60))
two('Merton tail two ways', tail10, tail10b, 1e-12); two('tail 8.3e-6', float(f'{tail10:.1e}'), 8.3e-6)
two('w10 3.8e-5', float(f'{w(10):.1e}'), 3.8e-5)
two('price bound', 100 * 8.3e-6, 0.00083); E('l12', 'screens[11].widget.answer', 0.00083)
two('pence', 100 * 0.00083, 0.083); E('l12', 'screens[11].widget.wrong[0].value', 0.083)
bars = node('l12', 'screens[11]')['canvas']['state']['values']
ok('l12 Merton bars', all(abs(bars[str(n)] - w(n)) < 6e-7 for n in range(0, 11)))

# ================= l13 =================
for k, (a, b) in enumerate([(1, 2), (2, 3), (3, 4), (5, 6), (10, 11), (20, 21), (29, 30)]):
    cap = lv.text('l13', f'screens[0].canvas.controls[0].frames[{k}].caption')
    ok(f'l13 s0 caption S_{a}, S_{b}', f'{float(alt(a)):.4f}' in cap and f'{float(alt(b)):.4f}' in cap and f'{{{b}}}' in cap, cap)
p = pts('l13', 'screens[0]')
ok('l13 s0 dots', all(abs(p[f's{n}'][1] - float(alt(n))) < 1e-6 for n in range(1, 31)))
ok('even sums rise, odd fall, evens below odds (n < 200)', all(alt(2 * n + 2) >= alt(2 * n) and alt(2 * n + 1) <= alt(2 * n - 1) and alt(2 * n) <= alt(2 * n + 1) for n in range(1, 100)))
s10 = alt(10); two('S10', rnd(s10, 6), 0.645635); two('ln2', rnd(LN2, 6), 0.693147); two('err', rnd(LN2 - float(s10), 6), 0.047512)
two('S11', rnd(alt(11), 6), 0.736544); two('1/11', rnd(F(1, 11), 6), 0.090909); two('1/22', rnd(F(1, 22), 6), 0.045455)
tab = node('l13', 'screens[3]')['canvas']['params']['rows']
two('table S10', float(tab[0][1]), 0.645635); two('table ln2', float(tab[1][1]), 0.693147); two('table err', float(tab[2][1]), 0.047512)
E('l13', 'screens[3].widget.answer', 0.090909); E('l13', 'screens[3].widget.wrong[1].value', 0.045455)
two('pi^2/12', rnd(math.pi ** 2 / 12, 6), 0.822467); two('alt n^2 sum', math.fsum((-1) ** (n + 1) / n ** 2 for n in range(1, 200001)), math.pi ** 2 / 12, 1e-9)
# trap series: odd places 1/k, even places 1/k^2
terms = []
for k in range(1, 21):
    terms += [F(1, k), -F(1, k * k)]
part = [sum(terms[:n]) for n in range(1, 41)]
two('S40 trap', rnd(part[39], 4), 2.0016); two('S40 trap 6dp', rnd(part[39], 6), 2.001576)
p = pts('l13', 'screens[8]')
ok('l13 s8 dots', all(abs(p[f's{n}'][1] - float(part[n - 1])) < 1e-6 for n in range(1, 41)))
ok('trap: a_{2n+1} - a_{2n+2} >= 0 always (so the odd-to-even step is NOT where it fails)', all(F(1, n + 1) - F(1, (n + 1) ** 2) >= 0 for n in range(1, 100)))
ok('trap: a_{2n} - a_{2n+1} < 0 for n >= 2 (the failing step: a_4 = 1/4 < 1/3 = a_5)', all(F(1, n * n) - F(1, n + 1) < 0 for n in range(2, 100)))
# code: terms_needed and actual_needed
tn = lambda e: next(n for n in range(0, 10 ** 6) if F(1, n + 1) < e)
for e, n in [(F(1, 1000), 1000), (F(1, 10), 10), (F(3, 1000), 333), (F(1, 2), 2)]:
    two(f'terms_needed {e}', tn(e), n)
errs = [abs(LN2 - float(alt(n))) for n in range(1, 1201)]
ok('true error strictly decreasing to n = 1200', all(errs[i + 1] < errs[i] for i in range(len(errs) - 1)))
an = lambda e: next(n for n in range(1, 1201) if errs[n - 1] < e)
for e, n in [(0.1, 5), (0.05, 10), (0.01, 50), (0.001, 500), (0.0005, 1000)]:
    two(f'actual_needed {e}', an(e), n)
two('error at 500', rnd(errs[499], 6), 0.000999)
two('alt_partial(1000)', float(alt(1000)), 0.6926474305598203, 1e-12)
# transfer
for n, net, gross in [(10, '645.63', '2,928.97'), (100, '688.17', '5,187.38')]:
    two(f'net {n}', rnd(1000 * alt(n), 2), float(net)); two(f'gross {n}', rnd(1000 * H(n), 2), float(gross.replace(',', '')))
two('net 1000', rnd(1000 * float(alt(1000)), 2), 692.65)
two('gross 1000', rnd(1000 * Hf(1000), 0), 7485); two('H1000 4dp', rnd(Hf(1000), 4), 7.4855)
two('H1000 ~ ln + gamma', rnd(math.log(1000) + GAMMA, 4), 7.4850, 1e-3)
two('1000 ln 1000', rnd(1000 * math.log(1000), 0), 6908); two('1000 ln2', rnd(1000 * LN2, 0), 693)
two('1% after 1000', rnd(10 * Hf(1000), 2), 74.85); two('1% after 1e6', rnd(10 * (math.log(1e6) + GAMMA + 1 / 2e6), 2), 143.93)
# quiz
s5 = sum(F((-1) ** (n + 1), n * n) for n in range(1, 6)); two('S5 n^2', rnd(s5, 6), 0.838611); two('err S5', rnd(float(s5) - math.pi ** 2 / 12, 6), 0.016144)
two('1/36', rnd(F(1, 36), 6), 0.027778); two('1/25', F(1, 25), 0.04)
two('q3 n', next(n for n in range(1, 100) if F(1, (n + 1) ** 2) < F(1, 1000)), 31)
two('q3 lin', next(n for n in range(1, 2000) if F(1, n + 1) < F(1, 1000)), 1000)
E('l13', 'quiz[3].widget.wrong[1].value', 1000)   # NEW value (review finding): fails until 999 becomes 1000

# ================= l14 =================
def greedy(target, n):
    target = F(target); tot, pos, neg, out = F(0), 1, 2, []
    for _ in range(n):
        if tot <= target:
            t = F(1, pos); pos += 2
        else:
            t = F(-1, neg); neg += 2
        tot += t; out.append(t)
    return out
def two_up(n):
    out, pos, neg = [], 1, 2
    while len(out) < n:
        out += [F(1, pos), F(1, pos + 2), F(-1, neg)]; pos += 4; neg += 2
    return out[:n]
tu = two_up(3000)
ps = []
acc = F(0)
for t in tu[:60]:
    acc += t; ps.append(acc)
for k, n in enumerate([3, 12, 30, 60]):
    E('l14', f'screens[0].canvas.controls[0].frames[{k}].caption', rnd(ps[n - 1], 4))
two('3000 terms', rnd(math.fsum(float(t) for t in tu), 4), 1.0395); E('l14', 'screens[0].canvas.controls[0].frames[4].caption', 1.0395)
two('3/2 ln 2', rnd(1.5 * LN2, 6), 1.039721)
p = pts('l14', 'screens[0]')
ok('l14 s0 dots', all(abs(p[f'r{n}'][1] - float(ps[n - 1])) < 1e-6 for n in range(1, 61)))
ok('two-up-one-down: from the third term on, totals stay below 1.2', all(float(v) < 1.2 for v in ps[2:]))
g = greedy(F(3, 2), 2000)
tots = []
acc = F(0)
for t in g[:12]:
    acc += t; tots.append(acc)
ok('greedy 1.5 first twelve', g[:12] == [F(1), F(1, 3), F(1, 5), F(-1, 2), F(1, 7), F(1, 9), F(1, 11), F(1, 13), F(1, 15), F(-1, 4), F(1, 17), F(1, 19)])
for i, v in [(2, 1.5333), (3, 1.0333), (4, 1.1762), (5, 1.2873), (6, 1.3782), (7, 1.4551), (8, 1.5218), (9, 1.2718)]:
    two(f'greedy total step {i + 1}', rnd(tots[i], 4), v)
for path, v in [('screens[2].widget.rows[1][1].answer', 0.142857), ('screens[2].widget.rows[1][2].answer', 1.17619), ('screens[2].widget.rows[5][1].answer', 0.066667),
                ('screens[2].widget.rows[5][2].answer', 1.5218), ('screens[2].widget.rows[6][1].answer', -0.25), ('screens[2].widget.rows[6][2].answer', 1.2718)]:
    E('l14', path, v)
two('2000 terms to 1.5', float(sum(g)), 1.4995173610186217, 1e-12); two('1.4995', rnd(sum(g), 4), 1.4995)
# overshoots above 1.5 for the claim "each swing past 1.5 is smaller than the last" (explain of screens[2])
acc, prev, peaks, side = F(0), None, [], None
for t in g:
    acc += t
    if acc > F(3, 2):
        if side != 'up': peaks.append(acc - F(3, 2)); side = 'up'
        else: peaks[-1] = max(peaks[-1], acc - F(3, 2))
    else:
        side = 'down'
ok('l14 s2: the overshoots above 1.5 shrink every time (first 12 crossings)', all(peaks[i + 1] < peaks[i] for i in range(min(11, len(peaks) - 1))), [round(float(x), 4) for x in peaks[:8]])
gz = greedy(0, 8)
ok('greedy 0 first eight', gz == [F(1), F(-1, 2), F(-1, 4), F(-1, 6), F(-1, 8), F(1, 3), F(-1, 10), F(-1, 12)])
zt = [sum(gz[:n]) for n in range(1, 7)]
for v, ex in zip(zt, [1, 0.5, 0.25, 0.0833, -0.0417, 0.2917]):
    two(f'greedy 0 total {ex}', rnd(v, 4), ex)
ok('greedy -1/2 first five', greedy(F(-1, 2), 5) == [F(-1, 2), F(1), F(-1, 4), F(-1, 6), F(-1, 8)])
two('pi^2/8', rnd(math.pi ** 2 / 8, 4), 1.2337); two('pi^2/8 by sum', math.fsum(1 / (2 * k - 1) ** 2 for k in range(1, 10 ** 6)) + 1 / (4 * 10 ** 6), math.pi ** 2 / 8, 1e-8)
two('pi^2/24 by sum', math.fsum(1 / (2 * k) ** 2 for k in range(1, 10 ** 6)), math.pi ** 2 / 24, 1e-6)
two('pi^2/12 4dp', rnd(math.pi ** 2 / 12, 4), 0.8225)
two('gap from ln2', rnd(1.5 * LN2 - LN2, 2), 0.35)
two('average of the two nets', rnd((LN2 + 1.5 * LN2) / 2, 2), 0.87)
two('q3 half', rnd(LN2 / 2, 6), 0.346574)

# ================= review-3 =================
two('r0 sum', math.fsum(2 / (n * (n + 2)) for n in range(1, 10 ** 6)) + 2e-6, 1.5, 1e-6)
for n in range(1, 40):
    assert sum(F(2, k * (k + 2)) for k in range(1, n + 1)) == F(3, 2) - F(1, n + 1) - F(1, n + 2)
two('r0 S2', F(2, 3) + F(1, 4), F(11, 12))
two('r1 sum n^2/3^n', math.fsum(n * n / 3 ** n for n in range(1, 200)), 1.5); two('r1 closed form', F(1, 3) * F(4, 3) / F(2, 3) ** 3, 1.5)
ok('r1 n=2: 4/9 > 1/4', F(4, 9) > F(1, 4))
two('r2 n', next(n for n in range(1, 500) if F(1, 2 * n + 1) < F(1, 100)), 50)
two('r2 1/99', rnd(F(1, 99), 4), 0.0101); two('r2 1/101', rnd(F(1, 101), 4), 0.0099); two('r2 4x', rnd(4 * F(1, 101), 2), 0.04)
two('r2 double = bound 1/(n+1) < 0.01', next(n for n in range(1, 500) if F(1, n + 1) < F(1, 100)), 100)
ok('r3 sizes decrease', all(F(n + 1, n * n) > F(n + 2, (n + 1) ** 2) for n in range(1, 200)))
ok('r4 greedy T=1', greedy(1, 3) == [F(1), F(1, 3), F(-1, 2)])
two('r4 totals', rnd(F(4, 3), 4), 1.3333); two('r4 totals 2', rnd(F(4, 3) - F(1, 2), 4), 0.8333)
two('r6 sum', F(1, 2) / (1 + F(1, 2)), F(1, 3)); two('r6 pos', F(1, 2) / (1 - F(1, 4)), F(2, 3)); two('r6 neg', F(1, 4) / (1 - F(1, 4)), F(1, 3))
s20 = sum(F(1, n * n) for n in range(1, 21)); two('r7 S20', rnd(s20, 6), 1.596163)
mid = s20 + (F(1, 21) + F(1, 20)) / 2
two('r7 mid', rnd(mid, 5), 1.64497); two('r7 low', rnd(s20 + F(1, 21), 5), 1.64378); two('r7 high', rnd(s20 + F(1, 20), 5), 1.64616)
two('r7 midpoint', rnd((F(1, 21) + F(1, 20)) / 2, 6), 0.048810); two('r7 off', rnd(float(mid) - math.pi ** 2 / 6, 5), 0.00004)
two('r7 pi2/6 5dp', rnd(math.pi ** 2 / 6, 5), 1.64493)
two('r8 k', next(k for k in range(0, 40) if 1 + F(k, 2) >= 10), 18); two('r8 2^18', 2 ** 18, 262144)

# ================= homework-3 =================
two('h1 e^3 - 1', rnd(math.e ** 3 - 1, 4), 19.0855); two('h1 by 59 terms', math.fsum(3 ** n / math.factorial(n) for n in range(1, 60)), math.e ** 3 - 1, 1e-12)
two('h1 with 0', rnd(math.e ** 3, 4), 20.0855); two('h1 /3', rnd(math.e ** 3 / 3, 4), 6.6952)
# h2 NEW series (review finding, freshness): 3/(k(k+3)) = 1/k - 1/(k+3), S_n = 11/6 - 1/(n+1) - 1/(n+2) - 1/(n+3)
for n in range(1, 40):
    assert sum(F(3, k * (k + 3)) for k in range(1, n + 1)) == F(11, 6) - F(1, n + 1) - F(1, n + 2) - F(1, n + 3)
E('homework', 'items[2].prose', '\\tfrac{3}{k(k+3)}')     # NEW value: fails until the fix lands
E('homework', 'items[2].widget.answer', '\\frac{11}{6}-\\frac{1}{n+1}-\\frac{1}{n+2}-\\frac{1}{n+3}')
two('h3 m', next(m for m in range(1, 10 ** 5) if F(1, m) < F(3, 10000)), 3334); two('h3 1/3333', rnd(F(1, 3333), 8), 0.00030003)
two('h3 sq', next(m for m in range(1, 10 ** 5) if F(1, m * m) < F(3, 10000)), 58)
ok('h4 sup n/(n+1) is 1', all(F(n, n + 1) < 1 for n in range(1, 100)) and 1 - F(10 ** 6, 10 ** 6 + 1) < F(1, 10 ** 5))
# h7 code target -1
gm = greedy(-1, 2000)
two('h7 total after 2000', float(sum(gm)), -0.9958227585810074, 1e-12); two('h7 -0.9958', rnd(sum(gm), 4), -0.9958)
two('h7 -1.0417', rnd(-(F(1, 2) + F(1, 4) + F(1, 6) + F(1, 8)), 4), -1.0417); two('h7 -0.0417', rnd(1 - (F(1, 2) + F(1, 4) + F(1, 6) + F(1, 8)), 4), -0.0417)
ok('h7 within 0.005', abs(float(sum(gm)) + 1) < 0.005)
s20 = alt(20); two('h8 S20', rnd(s20, 6), 0.668771); two('h8 err', rnd(LN2 - float(s20), 6), 0.024376); two('h8 1/21', rnd(F(1, 21), 6), 0.047619)
two('h8 1/21 4dp', rnd(F(1, 21), 4), 0.0476); two('h8 err 4dp', rnd(LN2 - float(s20), 4), 0.0244)
ok('h8 rubric sums to 10', sum(r['points'] for r in node('homework', 'items[8]')['rubric']) == 10)

# ================= code widgets: solution passes every test, starter fails one =================
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
        except Exception:
            good = False; continue
        if t.get('compare') == 'isclose':
            tol = t.get('tol') or {}
            ab, rel = tol.get('abs', 0), tol.get('rel', 1e-9 if 'abs' not in tol else 0)
            try:
                pair = list(zip(got, exp)) if isinstance(exp, (list, tuple)) else [(got, exp)]
                good = good and all(math.isclose(a, b, rel_tol=rel, abs_tol=ab) for a, b in pair) and (not isinstance(exp, (list, tuple)) or len(got) == len(exp))
            except TypeError:
                good = False
        else:
            good = good and got == exp
    return good
codes = [('l11', 'screens[10]'), ('l12', 'screens[10]'), ('l13', 'screens[9]'), ('l14', 'screens[10]'), ('homework', 'items[7]')]
for ref, path in codes:
    w = node(ref, path)['widget']
    ok(f'{ref} {path}: solution passes all {len(w["tests"])} tests', run_code(w, w['solution']))
    ok(f'{ref} {path}: starter fails a test', not run_code(w, w['starter']))
    ok(f'{ref} {path}: the solution meets every shown example', run_code({'tests': w.get('examples', [])}, w['solution']))
    m = re.search(r'runs (\d+) hidden tests', w.get('how', ''))
    ok(f'{ref} {path}: how states the test count', m and int(m.group(1)) == len(w['tests']))

lv.check_wrongs()
lv.report()
