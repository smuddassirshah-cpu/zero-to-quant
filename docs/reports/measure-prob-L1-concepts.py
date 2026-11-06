"""Concept checks for measure-prob level 1 (lessons l1 to l4, review-1, homework-1).

Run from the repo root: python3 -I docs/reports/measure-prob-L1-concepts.py
Each assert names the ledger row it backs (docs/reports/audit-measure-prob-1-3-ledger.md).
A check marked EXPECTED_FAIL fails because the content is wrong; the corrected assert sits
beside it in a comment, ready to enable once the content is fixed.
"""
import json
import math
import os
import sys
from fractions import Fraction
from itertools import product

import numpy as np
from scipy.special import polygamma

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'measure-prob')
rng = np.random.default_rng(20261106)
failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
        print('FAIL', msg)


def load(name):
    with open(os.path.join(COURSE, name + '.json')) as f:
        return json.load(f)


def run_code_widget(widget, code):
    """Run a code widget's hidden tests against `code`. Returns (passed, total)."""
    passed = 0
    tests = widget['tests']
    for t in tests:
        ns = {}
        try:
            exec(code, ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns)
            exp = t['expect']
            if isinstance(exp, str):
                try:
                    exp = eval(exp, ns)
                except Exception:
                    pass
            if t.get('compare') == 'fraction':
                ok = Fraction(got) == Fraction(exp)
            else:
                ok = got == exp
        except Exception:
            ok = False
        passed += ok
    return passed, len(tests)


def code_checks(doc, path, label):
    w = doc
    for p in path:
        w = w[p]
    sp, n = run_code_widget(w, w['solution'])
    st, _ = run_code_widget(w, w['starter'])
    check(sp == n, f'{label}-code-solution: solution passes {sp} of {n} hidden tests')
    check(st < n, f'{label}-code-starter: starter passes {st} of {n}, must fail at least one')


# ---------------------------------------------------------------- l1-why-measure
l1 = load('l1-why-measure')
# l1-cover-sum
s10 = sum(Fraction(1, 100) / 2 ** k for k in range(1, 11))
check(s10 == Fraction(1023, 102400), 'l1-cover-sum: ten cover lengths sum to 1023/102400')
check(abs(float(s10) - 0.00999) < 5e-6, 'l1-cover-sum: 0.00999 to 5 places')

# l1-cover-overlap (screens[3].hints[1] says "countable additivity on the lengths").
# The covering intervals overlap for every eps > 0, so additivity does not apply to them;
# the bound is countable subadditivity. This check states the hint's implicit claim.
def first_rationals(k):
    out = [Fraction(0), Fraction(1)]
    d = 2
    while len(out) < k:
        for n in range(1, d):
            if math.gcd(n, d) == 1:
                out.append(Fraction(n, d))
        d += 1
    return out[:k]


def cover_disjoint(eps):
    """Disjointness of the cover intervals, listed up to denominator 4/eps + 1 so that some
    rational 1/q lies inside the window round 0 (half-width eps/4)."""
    qs = [Fraction(0), Fraction(1)]
    for d in range(2, int(4 / eps) + 2):
        for n in range(1, d):
            if math.gcd(n, d) == 1:
                qs.append(Fraction(n, d))
    ivs = [(float(q) - eps * 2.0 ** -(j + 2), float(q) + eps * 2.0 ** -(j + 2)) for j, q in enumerate(qs)]
    ivs.sort()
    return all(ivs[i][1] < ivs[i + 1][0] for i in range(len(ivs) - 1))


for eps in (0.5, 0.05, 0.01):
    # EXPECTED_FAIL: the cover intervals are not disjoint, so "countable additivity on the lengths"
    # (l1 screens[3].hints[1]) is not the step; countable subadditivity is.
    # Corrected assert, ready to enable:
    # check(not cover_disjoint(eps), f'l1-cover-overlap eps={eps}: cover intervals overlap, use subadditivity')
    check(cover_disjoint(eps),
          f'EXPECTED_FAIL l1-cover-overlap eps={eps}: hint says additivity, but the cover intervals overlap')

# l1-cantor-stage
check(Fraction(2, 3) ** 10 == Fraction(1024, 59049), 'l1-cantor-stage: (2/3)^10 = 1024/59049')
check(abs(float(Fraction(2, 3) ** 10) - 0.0173415) < 5e-8, 'l1-cantor-stage: 0.0173415 to 7 places')

# l1-digital-tree
q = Fraction(105 - 80, 125 - 80)
check(q == Fraction(5, 9), 'l1-digital-tree: q = (1.05 - 0.8)/(1.25 - 0.8) = 5/9')
disc = 1.05 ** 2
p_at = 2 * q * (1 - q)
check(p_at == Fraction(40, 81), 'l1-digital-tree: P(S_T = 100) = 40/81')
check(abs(float(p_at) / disc - 0.4479) < 5e-5, 'l1-digital-tree: difference 0.4479')
check(abs(float(q * q + p_at) / disc - 0.7279) < 5e-5, 'l1-digital-tree: >= digital 0.7279')
check(abs(float(q * q) / disc - 0.2799) < 5e-5, 'l1-digital-tree: > digital 0.2799')
# lognormal example number: e^{-0.05} Phi(0.15)
from scipy.stats import norm
check(abs(math.exp(-0.05) * norm.cdf(0.15) - 0.5323) < 5e-5, 'l1-digital-tree: lognormal digital 0.5323')

code_checks(l1, ['screens', 8, 'widget'], 'l1')

# ---------------------------------------------------------------- l2-sigma-algebras
l2 = load('l2-sigma-algebras')


def generate(omega, events):
    whole = frozenset(omega)
    fam = {frozenset(), whole} | {frozenset(e) for e in events}
    while True:
        new = set(fam)
        for a in fam:
            new.add(whole - a)
            for b in fam:
                new.add(a | b)
        if new == fam:
            return fam
        fam = new


def is_sa(omega, sets):
    whole = frozenset(omega)
    fam = {frozenset(s) for s in sets}
    if whole not in fam:
        return False
    return all(whole - a in fam and all(a | b in fam for b in fam) for a in fam)


om = {1, 2, 3, 4, 5, 6}
check(len(generate(om, [{1, 3, 5}])) == 4, 'l2-generate-sizes: odd/even report gives 4 events')
check(len(generate(om, [{1}, {2, 3}])) == 8, 'l2-generate-sizes: three atoms give 8 events')
check(len(generate(om, [{1, 2}, {2, 3}])) == 16, 'l2-generate-sizes: sigma(A, B) with overlap has 16 events')
check(len(generate(om, [{1}, {2}])) == 8, 'l2-generate-sizes: sigma({1},{2}) has 8 events (quiz q-two)')
check(not is_sa(om, [set(), {1}, {2}, om]), 'l2-generate-sizes: {empty,{1},{2},Omega} is not a sigma-algebra')
A = generate(om, [{1}])
B = generate(om, [{2}])
check(len(A | B) == 6, 'l2-union-of-sigma-algebras: merged family holds 6 sets')
check(not is_sa(om, A | B), 'l2-union-of-sigma-algebras: merged family is not a sigma-algebra')
check(all(om - a in (A | B) for a in (A | B)), 'l2-union-of-sigma-algebras: merged family is closed under complements')
check(frozenset({1, 2}) not in (A | B), 'l2-union-of-sigma-algebras: {1,2} is in neither list')
check(len(generate(om, [{1}, {2}])) == 8, 'l2-union-of-sigma-algebras: sigma(A u B) has 8 sets')
code_checks(l2, ['screens', 10, 'widget'], 'l2')

# ---------------------------------------------------------------- l3-measures
l3 = load('l3-measures')


def hit_prob(n):
    dist = {0: Fraction(1)}
    hit = Fraction(0)
    for _ in range(n):
        new = {}
        for pos, p in dist.items():
            for step in (1, -1):
                qq = pos + step
                if qq == 1:
                    hit += p / 2
                else:
                    new[qq] = new.get(qq, 0) + p / 2
        dist = new
    return hit


# brute force over paths for n <= 12
def hit_brute(n):
    c = 0
    for path in product((1, -1), repeat=n):
        s = 0
        for st in path:
            s += st
            if s == 1:
                c += 1
                break
    return Fraction(c, 2 ** n)


for n in range(0, 11):
    check(hit_prob(n) == hit_brute(n), f'l3-hit-prob: DP equals path count at n={n}')
check([hit_prob(n) for n in (1, 2, 3, 4)] == [Fraction(1, 2), Fraction(1, 2), Fraction(5, 8), Fraction(5, 8)],
      'l3-hit-prob: 1/2, 1/2, 5/8, 5/8')
check(hit_prob(10) == Fraction(193, 256), 'l3-hit-prob: 193/256 at n = 10')
check(hit_prob(100) == 1 - Fraction(math.comb(100, 50), 2 ** 100), 'l3-hit-prob: 1 - C(100,50)/2^100 at n = 100')
check(abs(float(hit_prob(100)) - 0.9204) < 5e-5, 'l3-hit-prob: 0.9204 at n = 100')
check(all(hit_prob(n) <= hit_prob(n + 1) for n in range(30)), 'l3-hit-prob: non-decreasing in n (events grow)')
# recurrence: P(tau_1 > 2m) = C(2m,m)/4^m ~ 1/sqrt(pi m) -> 0, so the limit is 1
check(1 - math.comb(2000, 1000) / 4 ** 1000 > 0.98, 'l3-hit-prob: P(A_2000) > 0.98, tending to 1')
check(1 - math.comb(20000, 10000) / 4 ** 10000 > 0.994, 'l3-hit-prob: P(A_20000) > 0.994, tending to 1')
code_checks(l3, ['screens', 9, 'widget'], 'l3')

# l3-union-bound
check(abs((1 - 0.99 ** 3) - 0.029701) < 1e-6, 'l3-union-bound: independent desks 2.9701% < 3%')
check(abs((1 - 0.995 ** 4) - 0.01985) < 5e-6, 'l3-union-bound: four independent desks 1.985% < 2%')
check(abs((1 - 0.992 ** 5) - 0.039365) < 5e-6, 'r1-union: five independent desks 3.9365% < 4%')
# Monte Carlo: disjoint breaches attain the bound; independent ones fall short
N = 200_000
u = rng.random(N)
disjoint_any = ((u < 0.03)).mean()
indep_any = (rng.random((N, 3)) < 0.01).any(axis=1).mean()
check(abs(disjoint_any - 0.03) < 0.002, 'l3-union-bound: disjoint breaches reach 3% (MC)')
check(abs(indep_any - 0.029701) < 0.001, 'l3-union-bound: independent breaches give 2.9701% (MC); exact value is below the bound')
check(abs((1 - 0.98 ** 10) - 0.1829) < 5e-5 and abs((1 - 0.98 ** 50) - 0.6358) < 5e-5
      and abs((1 - 0.98 ** 20) - 0.3324) < 5e-5 and abs((1 - 0.99 ** 30) - 0.2603) < 5e-5,
      'l3-default: 1 - 0.98^n and 1 - 0.99^30 values')

# ---------------------------------------------------------------- l4-measurable-functions
l4 = load('l4-measurable-functions')
cells = [(a, b) for a in range(1, 7) for b in range(1, 7)]


def const_on_rows(f):
    return all(len({f((a, b)) for b in range(1, 7)}) == 1 for a in range(1, 7))


check(const_on_rows(lambda w: w[0]) and const_on_rows(lambda w: 2 * w[0]) and const_on_rows(lambda w: w[0] ** 2),
      'l4-constant-on-atoms: functions of the first die are constant on rows')
check(not const_on_rows(lambda w: w[0] + w[1]) and not const_on_rows(lambda w: max(w)),
      'l4-constant-on-atoms: sum and max vary along a row')
check(sum(1 for c in cells if c[0] + c[1] <= 7) == 21, 'l4-cdf: F_X(7) = 21/36')
check(sum(1 for c in cells if c[0] + c[1] < 7) == 15, 'l4-cdf: P(X < 7) = 15/36')
check(sum(1 for c in cells if c[0] + c[1] <= 8) == 26, 'l4-cdf: F_X(8) = 26/36')
check(sum(1 for c in cells if c[0] + c[1] >= 11) == 3, 'l4-tail: P(X >= 11) = 3/36')
check(abs(0.9 + 0.1 * (1 - math.exp(-0.5)) - 0.9393) < 5e-5, 'l4-mixed-cdf: F_L(5000) = 0.9393')


def finv(u, atom, mean):
    return 0.0 if u <= atom else -mean * math.log(1 - (u - atom) / (1 - atom))


check(abs(finv(0.95, 0.9, 10000) - 10000 * math.log(2)) < 1e-9, 'l4-inverse-sampling: F^{-1}(0.95) = 10,000 ln 2')
check(abs(10000 * math.log(2) - 6931.47) < 0.005, 'l4-inverse-sampling: £6,931.47')
uu = rng.random(1_000_000)
L = np.where(uu <= 0.9, 0.0, -10000 * np.log(1 - np.clip(uu - 0.9, 0, None) / 0.1))
check(abs((L == 0).mean() - 0.9) < 0.005, 'l4-inverse-sampling: atom mass 0.9 reproduced (MC)')
check(abs(L[L > 0].mean() - 10000) < 200, 'l4-inverse-sampling: positive part has mean 10,000 (MC)')
check(abs(np.quantile(L, 0.95) - 6931.47) < 250, 'l4-inverse-sampling: empirical 95% quantile near £6,931 (MC)')
check(abs((L <= 5000).mean() - 0.9393) < 0.005, 'l4-inverse-sampling: F_L(5000) = 0.9393 reproduced (MC)')
U = rng.random(400_000)
check(abs((-np.log(U) > 2).mean() - math.exp(-2)) < 0.003, 'l4-exp-from-uniform: P(-ln U > 2) = e^{-2} (MC)')
check(abs((-np.log(U) > math.log(2)).mean() - 0.5) < 0.003, 'l4-exp-from-uniform: P(X > ln 2) = 1/2 (MC)')
code_checks(l4, ['screens', 8, 'widget'], 'l4')

# ---------------------------------------------------------------- review-1
om4 = {1, 2, 3, 4}
check(is_sa(om4, [set(), {1, 2}, {3, 4}, om4]), 'r1-which-family: option a is a sigma-algebra')
check(not is_sa(om4, [set(), {1}, {2, 3, 4}, {1, 2}, om4]), 'r1-which-family: option b fails')
check(not is_sa(om4, [set(), {1}, {2}, {3, 4}, om4]), 'r1-which-family: option c fails')
check(not is_sa(om4, [{1, 2}, {3, 4}, om4]), 'r1-which-family: option d fails')
check(sum(1 for c in cells if c[0] * c[1] >= 20) == 8, 'r1-product: 8 cells with product >= 20')
om8 = set(range(1, 9))
check(len(generate(om8, [{1, 2, 3, 4}, {1, 2, 5, 6}, {1, 3, 5, 7}])) == 256, 'r1-events-256: sigma(A,B,C) is the power set')
check(abs(finv(0.95, 0.85, 8000) - 8000 * math.log(3)) < 1e-9 and round(8000 * math.log(3)) == 8789,
      'r1-var: F^{-1}(0.95) = 8,000 ln 3 = £8,789')
check(abs(0.02 * (1 - 2 ** -6) - 0.0196875) < 1e-12, 'r1-cover: six lengths sum to 0.0196875')

# ---------------------------------------------------------------- homework-1
check((2 / 3) ** 17 > 0.001 > (2 / 3) ** 18, 'h1-cantor-stage: length first below 0.001 at stage 18')
check(abs(math.log(1000) / math.log(1.5) - 17.04) < 0.005, 'h1-cantor-stage: ln 1000 / ln 1.5 = 17.04')
# 1/4 in the Cantor set: ternary digits all 0 or 2, and non-terminating (so not an end point)
x = Fraction(1, 4)
digits = []
for _ in range(40):
    x *= 3
    d = int(x)
    digits.append(d)
    x -= d
check(all(d in (0, 2) for d in digits) and digits[:6] == [0, 2, 0, 2, 0, 2],
      'h1-quarter-in-cantor: 1/4 = 0.020202..._3 lies in the Cantor set')
check(Fraction(1, 4).denominator % 3 != 0, 'h1-quarter-in-cantor: 1/4 is not a triadic rational, so not an end point')
tail100 = float(polygamma(1, 100))
tail50 = float(polygamma(1, 50))
check(abs(tail100 - 0.0100502) < 5e-7, 'h1-tail-sum: sum_{k>=100} 1/k^2 = 0.0100502')
check(abs(tail100 - (math.pi ** 2 / 6 - sum(1 / k ** 2 for k in range(1, 100)))) < 1e-12, 'h1-tail-sum: pi^2/6 minus partial sum')
check(abs(1 / 99.5 - 0.01005) < 5e-6 and abs(1 / 99 - 0.0101) < 5e-5, 'h1-tail-sum: 1/99.5 and the cruder 1/99')
check(abs(tail50 - 0.0202) < 5e-5, 'h1-tail-sum: bound from day 50 is 0.0202')
check(abs(0.75 + 0.25 * (1 - math.exp(-0.5)) - 0.8484) < 5e-5, 'h1-var: F_L(10,000) = 0.8484')
check(round(20000 * math.log(25)) == 64378 and abs(finv(0.99, 0.75, 20000) - 20000 * math.log(25)) < 1e-9,
      'h1-var: F^{-1}(0.99) = 20,000 ln 25 = £64,378')
check(finv(0.70, 0.75, 20000) == 0.0, 'h1-var: F^{-1}(0.70) = 0 (atom)')
check(round(-20000 * math.log(1.2)) == -3646, 'h1-var: naive smooth solve at 0.70 gives -3,646')
r = 1.7
Xr = -np.log(U) / r
check(abs((Xr <= 1.0).mean() - (1 - math.exp(-r))) < 0.003, 'h1-exp-rate: -ln U / r has F(x) = 1 - e^{-rx} (MC)')
hw1 = load('homework-1')
code_checks(hw1, ['items', 6, 'widget'], 'h1')

# ---------------------------------------------------------------- Borel-Cantelli 1 (h-long) Monte Carlo
# independent breaches with P = 1/n^2: total count is finite a.s.; mean count sum 1/n^2 = pi^2/6
n = np.arange(1, 5001)
counts = (rng.random((2000, n.size)) < 1 / n ** 2).sum(axis=1)
check(abs(counts.mean() - math.pi ** 2 / 6) < 0.1, 'h1-bc1: mean number of breaches is pi^2/6 (MC, independent case)')
check((counts <= 12).all(), 'h1-bc1: no path has many breaches (finitely many a.s., MC)')

print(f'{len(failures)} failing checks')
sys.exit(1 if failures else 0)
