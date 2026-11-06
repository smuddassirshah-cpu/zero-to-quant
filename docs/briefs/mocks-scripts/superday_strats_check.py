"""Second route for app/content/exams/mock-superday-strats.json. Exits 1 on any failure.

Route A is superday_strats_build.py (closed forms). Route B here is independent: exact linear solves on Fractions for
the walk, numerical integration (Simpson) for the normal and Brownian items, polynomial Itô generators on Fractions,
summation over the Poisson total, explicit path enumeration on the tree, and a fresh g++ build of the C++ item.
Every code solution passes its hidden tests and every starter fails one. A last pass reads every number in each item's
learner-visible strings: whole numbers 0 to 10 count as structure, every other number must match a route-B or given
value for that item to its printed precision. Then numbers_lib's check_wrongs() and report().
Run: python3 docs/briefs/mocks-scripts/superday_strats_check.py
"""
import itertools
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level, _FRAC, _NUM, normalise  # noqa: E402

EXAM = os.path.join(ROOT, 'app', 'content', 'exams', 'mock-superday-strats.json')
N01 = NormalDist()


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
ITEM, PATH = {}, {}
for pi, p in enumerate(doc['parts']):
    for j, it in enumerate(p.get('items', [])):
        ITEM[it['id']] = it
        PATH[it['id']] = f'parts[{pi}].items[{j}]'
ALLOW = {}


def allow(iid, *vals):
    ALLOW.setdefault(iid, []).extend(float(v) for v in vals)


def rec(ok, label, note=''):
    ex._rec(bool(ok), label, '' if ok else note)


def W(iid, part=None):
    it = ITEM[iid]
    return it['widget'] if part is None else it['parts'][part]['widget']


def key(iid, value, part=None, tol=None):
    w = W(iid, part)
    t = tol if tol is not None else max(w['tol']['abs'] / 10, 1e-9)
    rec(abs(w['answer'] - value) <= t, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {value!r}', 'route B differs')
    ex.expect('exam', f'{PATH[iid]}' + ('' if part is None else f'.parts[{part}]') + '.widget.answer', w['answer'])
    allow(iid, value, w['answer'], w['tol']['abs'])


def wrong(iid, wid, value, part=None, tol=None):
    w = W(iid, part)
    hit = [x for x in w['wrong'] if x['id'] == wid]
    t = tol if tol is not None else max(hit[0]['tol']['abs'] / 10, 1e-9) if hit else 0
    rec(len(hit) == 1 and abs(hit[0]['value'] - value) <= t, f'{iid}{"" if part is None else f" part {part}"} wrong "{wid}" = {value!r}', f'found {hit}')
    allow(iid, value, hit[0]['value'] if hit else value)


def all_wrongs(iid, ids, part=None):
    rec(sorted(x['id'] for x in W(iid, part).get('wrong', [])) == sorted(ids), f'{iid} wrong ids are {sorted(ids)}')


def opt(iid, text_value, part=None, correct=False):
    """the option whose text holds text_value exists; and is the key when correct"""
    w = W(iid, part)
    hit = [o for o in w['options'] if o['text'] == text_value] or [o for o in w['options'] if text_value in o['text']]
    rec(len(hit) == 1 and bool(hit[0].get('correct')) == correct, f'{iid} option "{text_value}" {"is the key" if correct else "is a distractor"}')


def choice_rules(iid, part=None):
    w = W(iid, part)
    rec(w.get('shuffle') is True, f'{iid} shuffle true')
    rec(sum(1 for o in w['options'] if o.get('correct')) == 1, f'{iid} exactly one key')
    rec(all(str(o.get('why', '')).startswith('You ') for o in w['options'] if not o.get('correct')), f'{iid} every why names the learner’s action')
    nums = []
    for o in w['options']:
        m = re.fullmatch(r'\$?£?(-?\d+(?:\.\d+)?)\$?', o['text'].replace(',', ''))
        f = re.fullmatch(r'\$(\d+)/(\d+)\$', o['text'])
        v = float(m.group(1)) if m else (int(f.group(1)) / int(f.group(2)) if f else None)
        nums.append((v, o.get('correct', False)))
    if all(v is not None for v, _ in nums):
        k = [v for v, c in nums if c][0]
        ds = [v for v, c in nums if not c]
        tens = any(abs(a * 10 - b) < 1e-12 or abs(b * 10 - a) < 1e-12 for a, b in itertools.combinations(ds, 2) if min(a, b) < k < max(a, b))
        equal = any(abs((k - a) - (b - k)) < 1e-12 for a, b in itertools.combinations(ds, 2) if a < k < b or b < k < a)
        rec(not tens and not equal, f'{iid} key sits between no times-ten pair and no two equal slips')


def simpson(f, a, b, m=20000):
    h = (b - a) / m
    return h / 3 * (f(a) + f(b) + sum((4 if k % 2 else 2) * f(a + k * h) for k in range(1, m)))


def solve(A, b):
    """exact Gaussian elimination on Fractions"""
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                fac = M[r][c] / M[c][c]
                M[r] = [x - fac * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


# ======================================================================== paper 1
# P1: states 0..6 (stops at 0 and 6), start 2; up 3/5, down 2/5
pu, pd = F(3, 5), F(2, 5)
inner = range(1, 6)
A = [[(1 if i == j else 0) - (pu if j == i + 1 else 0) - (pd if j == i - 1 else 0) for j in inner] for i in inner]
hit = solve(A, [pu if i == 5 else 0 for i in inner])
steps = solve(A, [F(1)] * 5)
P_top, E_T = hit[1], steps[1]
rec(P_top == F(81, 133) and E_T == F(1100, 133), f'p1 linear solve: P = {P_top}, E[T] = {E_T}')
key('p1-drift-ruin', float(P_top), 0)
wrong('p1-drift-ruin', 'fair', 2 / 6, 0, 0.0001)
wrong('p1-drift-ruin', 'one-step', 0.6, 0)
wrong('p1-drift-ruin', 'lower', 1 - float(P_top), 0, 0.0001)
all_wrongs('p1-drift-ruin', ['fair', 'one-step', 'lower'], 0)
key('p1-drift-ruin', float(E_T), 1)
wrong('p1-drift-ruin', 'fair-rule', 4 * 2, 1)
wrong('p1-drift-ruin', 'no-drift', float(E_T * F(1, 5)), 1, 0.005)
all_wrongs('p1-drift-ruin', ['fair-rule', 'no-drift'], 1)
allow('p1-drift-ruin', 50, 54, 48, 0.4, 0.2, 220, 133, 1100, 81, 0.6, 0.4)

# P2: integrate phi(x) Phi(rho x / sqrt(1 - rho^2)) over x > 0
rho = 0.5
orth = simpson(lambda x: N01.pdf(x) * N01.cdf(rho * x / math.sqrt(1 - rho ** 2)), 0, 12)
rec(abs(orth - 1 / 3) < 1e-9, f'p2 quadrant integral {orth:.12f} = 1/3')
opt('p2-orthant', '$1/3$', correct=True)
opt('p2-orthant', '$1/4$')
opt('p2-orthant', '$1/6$')
opt('p2-orthant', '$3/8$')
neg = simpson(lambda x: N01.pdf(x) * N01.cdf(-rho * x / math.sqrt(1 - rho ** 2)), 0, 12)
rec(abs(neg - 1 / 6) < 1e-9 and abs((0.25 + 0.5) / 2 - 3 / 8) < 1e-15, 'p2 distractors: correlation -0.5 gives 1/6; the straight line gives 3/8')
choice_rules('p2-orthant')
allow('p2-orthant', 12, 0.5, 1 / 3, 1 / 4, 1 / 12, 1 / 6, 3 / 8, 1 / 2, -0.5)

# P3: E[max] = int (1 - x^4), E[min] = int (1 - x)^4 on [0, 1], exact by polynomial integration
def integ(coeffs):  # coefficients c_k of x^k on [0, 1]
    return sum(F(c, k + 1) for k, c in enumerate(coeffs))


emax = integ([1, 0, 0, 0, -1])
emin = integ([math.comb(4, k) * (-1) ** k for k in range(5)])
rec(emax == F(4, 5) and emin == F(1, 5), f'p3 E[max] = {emax}, E[min] = {emin}')
key('p3-first-last-gap', float(60 * (emax - emin)))
wrong('p3-first-last-gap', 'last-only', float(60 * emax))
wrong('p3-first-last-gap', 'half', 30)
wrong('p3-first-last-gap', 'three-quarters', 60 * 3 / 4)
all_wrongs('p3-first-last-gap', ['last-only', 'half', 'three-quarters'])
allow('p3-first-last-gap', 60, 48, 12, 4 / 5, 1 / 5, 3 / 5, 1 / 3, 20)

# P4: E[others | 10 cancels] by summing over the total count N ~ Poisson(18)
lam = 18
num = den = 0.0
for n in range(10, 160):
    w = math.exp(-lam) * lam ** n / math.factorial(n) * math.comb(n, 10) * (2 / 3) ** 10 * (1 / 3) ** (n - 10)
    num += w * (n - 10)
    den += w
rec(abs(num / den - 6) < 1e-9, f'p4 E[others | 10 cancels] = {num / den:.10f}')
opt('p4-poisson-thinning', '6', correct=True)
for d in ('8', '5', '18'):
    opt('p4-poisson-thinning', d)
rec(18 - 10 == 8 and 10 / 2 == 5, 'p4 distractors: 18 - 10 and 10 / 2')
choice_rules('p4-poisson-thinning')
allow('p4-poisson-thinning', 18, 2 / 3, 10, 6, 12, 1 / 3, 8, 5)

# P5: E[max(X, Y)] for correlation 0.5 by Simpson over x of the closed-form conditional mean of max(x, rho x + c Z), scaled by 2%
rho5, c5 = 0.5, math.sqrt(1 - 0.5 ** 2)


def cond_max(x):  # E[max(x, b + c Z)] = x + (b - x) Phi(m) + c phi(m), m = (b - x) / c, b = rho x
    m = (rho5 * x - x) / c5
    return x + (rho5 * x - x) * N01.cdf(m) + c5 * N01.pdf(m)


emax5 = 0.02 * simpson(lambda x: cond_max(x) * N01.pdf(x), -12, 12)
eabs = 0.02 * simpson(lambda x: abs(x) * N01.pdf(x), -12, 12)
emax_indep = 0.02 * simpson(lambda x: 2 * x * N01.pdf(x) * N01.cdf(x), -12, 12)
key('p5-max-of-two-normals', emax5, tol=5e-7)
wrong('p5-max-of-two-normals', 'no-correlation', emax_indep, tol=5e-7)
wrong('p5-max-of-two-normals', 'abs-value', eabs, tol=5e-7)
wrong('p5-max-of-two-normals', 'zero', 0)
all_wrongs('p5-max-of-two-normals', ['no-correlation', 'abs-value', 'zero'])
allow('p5-max-of-two-normals', 2, 0.02, 0.5, emax5 * 100, emax5, 0.00798, 0.80, 1)

# ======================================================================== paper 2
# R1: Black-Scholes at r = 0 by integrating the lognormal payoff, against the rule of thumb
S, K, sig, T = 250, 250, 0.2, 0.25
bs = simpson(lambda z: max(S * math.exp(-0.5 * sig ** 2 * T + sig * math.sqrt(T) * z) - K, 0) * N01.pdf(z), -12, 12, 40000)
key('r1-atm-rule', round(bs, 2), tol=0.005)
rec(abs(bs - 10) < 0.1, f'r1 the rule of thumb £10 is inside the tolerance of {bs:.4f}')
wrong('r1-atm-rule', 'full-year', 0.4 * S * sig * 1)
wrong('r1-atm-rule', 'used-T', 0.4 * S * sig * T)
all_wrongs('r1-atm-rule', ['full-year', 'used-T'])
allow('r1-atm-rule', 250, 20, 0.2, 0.25, 0.5, 0.4, 10, round(bs, 2), 0.05, 2)

# R2: cash flows of each listed trade today, and at expiry for three prices
C, P, S2, K2, DF = 7.20, 4.10, 52, 50, 0.98
key_cash = C - P - S2 + K2 * DF
rev_cash = -C + P + S2 - K2 * DF
strike_cash = C - P - S2 + K2
rec(abs(key_cash - 0.10) < 1e-12 and abs(rev_cash + 0.10) < 1e-12 and abs(strike_cash - 1.10) < 1e-12, 'r2 cash today: +0.10, -0.10 reversed, +1.10 borrowing the strike')
rec(all(abs(-max(ST - K2, 0) + max(K2 - ST, 0) + ST - K2) < 1e-12 for ST in (30, 50, 80)), 'r2 the key trade nets 0 at expiry')
rec(all(abs(-max(ST - K2, 0) + max(K2 - ST, 0) + ST - K2 / DF) > 1 for ST in (30, 50, 80)), 'r2 borrowing £50 owes 51.02 and loses at expiry')
opt('r2-parity-arbitrage', 'borrow £49: £0.10 now', correct=True)
opt('r2-parity-arbitrage', 'lend £49')
opt('r2-parity-arbitrage', 'borrow £50: £1.10 now')
choice_rules('r2-parity-arbitrage')
allow('r2-parity-arbitrage', 52, 50, 7.20, 4.10, 0.98, 49, 0.10, 1.10, 3.10, 3.00)

# R3: reprice a value with gamma 0.04 and theta -0.40 over one day: V(S, t) = 0.02 S^2 - 0.40 t, delta-hedged
V = lambda s, t: F(1, 2) * F(4, 100) * s * s + F(-40, 100) * t
S0 = F(100)
delta = F(4, 100) * S0
pnl = 300 * (V(S0 + 5, 1) - V(S0, 0) - delta * 5)
rec(pnl == 30, f'r3 repriced hedged P&L {pnl}')
key('r3-gamma-theta', float(pnl))
wrong('r3-gamma-theta', 'no-theta', float(300 * F(1, 2) * F(4, 100) * 25))
wrong('r3-gamma-theta', 'no-half', float(300 * (F(4, 100) * 25 - F(4, 10))))
wrong('r3-gamma-theta', 'theta-only', float(300 * F(-4, 10)))
all_wrongs('r3-gamma-theta', ['no-theta', 'no-half', 'theta-only'])
allow('r3-gamma-theta', 300, 0.04, 0.40, 5, 0.50, 0.10, 30, 25)

# R4: the scaled call spread's payoff at expiry equals the digital outside (99, 101)
spread = lambda s: (max(s - 99, 0) - max(s - 101, 0)) / 2
rec(all(spread(s) == (1 if s >= 101 else 0) for s in (50, 98, 101, 140)) and spread(100) == 0.5, 'r4 the call spread pays 1 above 101, 0 below 99')
key('r4-digital-spread', (5.40 - 4.30) / 2)
wrong('r4-digital-spread', 'no-width', 5.40 - 4.30)
wrong('r4-digital-spread', 'digital-put', 1 - (5.40 - 4.30) / 2)
all_wrongs('r4-digital-spread', ['no-width', 'digital-put'])
allow('r4-digital-spread', 5.40, 4.30, 99, 101, 100, 0.55, 1, 2)

# R5: standard error by float route; paths by solving 2 * 27 / sqrt(n) = 0.06 with bisection
key('r5-mc-error', 2 * 27 / math.sqrt(90000), 0)
wrong('r5-mc-error', 'one-se', 27 / math.sqrt(90000), 0)
wrong('r5-mc-error', 'over-n', 2 * 27 / 90000, 0, 1e-12)
all_wrongs('r5-mc-error', ['one-se', 'over-n'], 0)
lo, hi = 1.0, 1e9
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if 54 / math.sqrt(mid) > 0.06 else (lo, mid)
key('r5-mc-error', round(lo), 1)
wrong('r5-mc-error', 'linear', 90000 * 3, 1)
wrong('r5-mc-error', 'no-square', 54 / 0.06, 1, 1e-6)
all_wrongs('r5-mc-error', ['linear', 'no-square'], 1)
allow('r5-mc-error', 90000, 27, 8.41, 95, 0.09, 0.18, 300, 8.41 - 0.18, 8.41 + 0.18, 0.06, 54, 900, 810000, 3, 9)

# R6: error model e(h) = c h^2; measure the order from two runs, then predict
c6 = 0.0048 * 100 ** 2
order = math.log((c6 / 100 ** 2) / (c6 / 200 ** 2)) / math.log(2)
pred = c6 / 400 ** 2
rec(abs(order - 2) < 1e-12 and abs(pred - 0.0003) < 1e-15, f'r6 order {order}, prediction {pred}')
opt('r6-convergence-order', '0.0003', correct=True)
opt('r6-convergence-order', '0.0012')
opt('r6-convergence-order', '0.000075')
opt('r6-convergence-order', '0.0024')
rec(abs(0.0048 / 4 - 0.0012) < 1e-15 and abs(0.0048 / 64 - 0.000075) < 1e-15 and abs(0.0048 / 2 - 0.0024) < 1e-15, 'r6 distractors: /4, /64, /2')
choice_rules('r6-convergence-order')
allow('r6-convergence-order', 0.0048, 100, 400, 16, 0.0003, 0.0012, 0.000075, 0.0024, 64)

# R7: Black-Scholes gamma at the money (r = 0) by the formula and by a second difference of the price, then the summed daily P&L
S_, K_, sg_, T_ = 100.0, 100.0, 0.2, 1 / 12


def bs_call(s, k, sg, t):
    d1 = (math.log(s / k) + 0.5 * sg * sg * t) / (sg * math.sqrt(t))
    return s * N01.cdf(d1) - k * N01.cdf(d1 - sg * math.sqrt(t))


gam_formula = N01.pdf((0.5 * sg_ * sg_ * T_) / (sg_ * math.sqrt(T_))) / (S_ * sg_ * math.sqrt(T_))
hh = 0.01
gam_diff = (bs_call(S_ + hh, K_, sg_, T_) - 2 * bs_call(S_, K_, sg_, T_) + bs_call(S_ - hh, K_, sg_, T_)) / hh ** 2
rec(abs(gam_formula - 0.0691) < 5e-5 and abs(gam_diff - gam_formula) < 1e-5 and round(gam_formula, 2) == 0.07,
    f'r7 Black-Scholes gamma {gam_formula:.5f} by the formula, {gam_diff:.5f} by a second difference: 0.07 to two decimals')
days = 21
dt = (1 / 12) / days
daily = [0.5 * 0.07 * 100 ** 2 * (0.25 ** 2 * dt - 0.2 ** 2 * dt) for _ in range(days)]
rec(abs(sum(daily) - 0.65625) < 1e-12 and round(sum(daily), 2) == 0.66, f'r7 summed P&L {sum(daily):.6f}')
allow('r7-realised-vs-implied', 20, 25, 0.07, 100, 0.0625, 0.04, 0.66, 0.65, 12, 250, 0)

# ======================================================================== paper 3
# S1: E[f(t, W_t)] for f = (w + a t) e^{w - t/2} by Simpson over the normal density: it equals (1 + a) t, so only a = -1 keeps it at 0
def mean_f(a, t):
    sd = math.sqrt(t)
    return simpson(lambda z: (sd * z + a * t) * math.exp(sd * z - t / 2) * N01.pdf(z), -14, 14, 40000)


sols = [a for a in range(-5, 6) if all(abs(mean_f(a, t)) < 1e-6 for t in (0.5, 1, 2, 3))]
rec(sols == [-1], f's1 the mean stays 0 at t = 0.5, 1, 2, 3 only for a = {sols}')
rec(all(abs(mean_f(a, 2) - (1 + a) * 2) < 1e-6 for a in (-2, 0, 1)), 's1 the mean is (1 + a) t')
key('s1-exponential-correction', -1, 0)
wrong('s1-exponential-correction', 'sign-slip', 1, 0)
wrong('s1-exponential-correction', 'zero', 0, 0)
all_wrongs('s1-exponential-correction', ['sign-slip', 'zero'], 0)
sd2 = math.sqrt(2)
we = simpson(lambda z: sd2 * z * math.exp(sd2 * z - 1) * N01.pdf(z), -14, 14, 40000)
we_no = simpson(lambda z: sd2 * z * math.exp(sd2 * z) * N01.pdf(z), -14, 14, 40000)
key('s1-exponential-correction', we, 1, tol=5e-4)
wrong('s1-exponential-correction', 'independent', 0, 1)
wrong('s1-exponential-correction', 'no-compensator', we_no, 1, 5e-4)
all_wrongs('s1-exponential-correction', ['independent', 'no-compensator'], 1)
allow('s1-exponential-correction', 1, 2, 0.5, 1)

# S2: median of the lognormal by bisection on its CDF
m_, s_ = math.log(40) + (0.10 - 0.08) * 2, 0.40 * math.sqrt(2)
lo, hi = 1.0, 200.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if N01.cdf((math.log(mid) - m_) / s_) < 0.5 else (lo, mid)
mean2 = simpson(lambda z: math.exp(m_ + s_ * z) * N01.pdf(z), -12, 12)
opt('s2-gbm-median', f'£{lo:.2f}', correct=True)
opt('s2-gbm-median', f'£{mean2:.2f}')
opt('s2-gbm-median', f'£{40 * math.exp((0.10 - 0.16) * 2):.2f}')
opt('s2-gbm-median', f'£{40 * math.exp(0.02):.2f}')
choice_rules('s2-gbm-median')
allow('s2-gbm-median', 10, 40, 0.10, 0.08, 0.04, 0.2, lo, mean2, 40 * math.exp(-0.12), 40 * math.exp(0.02))

# S3: first-passage density of a level 3 for volatility 2, integrated to 1 day
dens = lambda t: 3 / (2 * math.sqrt(2 * math.pi * t ** 3)) * math.exp(-9 / (8 * t)) if t > 0 else 0.0
touch = simpson(dens, 0, 1, 40000)
key('s3-touch', touch, tol=5e-5)
wrong('s3-touch', 'no-reflection', touch / 2, tol=5e-5)
wrong('s3-touch', 'stays-below', 1 - touch, tol=5e-5)
all_wrongs('s3-touch', ['no-reflection', 'stays-below'])
rec(round(N01.cdf(1.5), 4) == 0.9332 and abs(2 * (1 - 0.9332) - touch) < 5e-4, f's3 the given Phi(1.5) = {N01.cdf(1.5):.5f} rounds to 0.9332 and gives {2 * (1 - 0.9332):.4f}')
allow('s3-touch', 2, 3, 1.5, touch, touch / 2, 1 - touch, 0.9332)

# S4: E[ln S_T] under Q by integrating ln of the lognormal; discount
Elog = simpson(lambda z: (math.log(100) + (0.02 - 0.02) * 1 + 0.2 * z) * N01.pdf(z), -12, 12)
price4 = math.exp(-0.02) * Elog
rec(abs(Elog - 4.6052) < 5e-5 and abs(price4 - 4.5140) < 5e-5, f's4 E[ln S] = {Elog:.6f}, price {price4:.6f}')
allow('s4-log-contract', 100, 2, 20, 250, 0.02, Elog, price4, round(price4, 2), 250)

# ======================================================================== paper 4: code
def close(a, b, tol):
    return math.isclose(a, b, rel_tol=tol.get('rel', 0), abs_tol=tol.get('abs', 0))


def run_py(src, tests):
    passed = 0
    for t in tests:
        ns = {}
        try:
            exec(src, ns)
            if t['compare'] == 'raises':
                try:
                    eval(t['call'], ns)
                    ok = False
                except Exception as e:  # noqa: BLE001
                    ok = type(e).__name__ == t['expect']
            else:
                ok = close(float(eval(t['call'], ns)), float(eval(t['expect'])), t.get('tol', {'rel': 1e-9}))
        except Exception:  # noqa: BLE001
            ok = False
        passed += bool(ok)
    return passed


c1 = ITEM['c1-barrier-tree']
w1, w2 = c1['parts'][0]['widget'], c1['parts'][1]['widget']
t1, t2 = w1['tests'], w1['tests'] + w2['tests']
rec(run_py(w1['solution'], t1) == len(t1), f'c1 part 1 solution passes {len(t1)} tests')
rec(run_py(w1['starter'], t1) < len(t1), 'c1 part 1 starter fails a test')
rec(run_py(w2['solution'], t2) == len(t2), f'c1 part 2 solution passes {len(t2)} merged tests')
rec(run_py(w2['starter'], t2) < len(t2), 'c1 part 2 starter fails a test')
rec(len(t2) <= 15, f'c1 merged tests {len(t2)} <= 15')
rec(run_py(w2['solution'], w1['examples'] + w2['examples']) == 4, 'c1 the examples pass')
rec(w1['starter'] != w1['solution'] and 'raise' not in w1['starter'] and 'call' not in [l for l in w1['starter'].split('\n') if l.startswith('def ')][0],
    'c1 the part 1 starter is a working call pricer with no checks and no flag')


def crr_args(call):
    return eval(call.replace('crr_value', '_pack'), {'_pack': lambda *a, **k: (a, k)})


def crr_paths(S, K, T, r, sigma, n, call=True, barrier=None):
    """route B: sum over every path of the tree with its risk-neutral weight (2^n paths)"""
    dt = T / n
    u = math.exp(sigma * math.sqrt(dt))
    p = (math.exp(r * dt) - 1 / u) / (u - 1 / u)
    sign = 1 if call else -1
    tot = 0.0
    for path in itertools.product((0, 1), repeat=n):
        k, alive = 0, barrier is None or S > barrier
        for step in path:
            k += 1 if step else -1
            alive = alive and (barrier is None or S * u ** k > barrier)
        ups = sum(path)
        tot += p ** ups * (1 - p) ** (n - ups) * (max(sign * (S * u ** k - K), 0) if alive else 0)
    return math.exp(-r * T) * tot


ns1 = {}
exec(w1['solution'], ns1)
for t in t2:
    a, k = crr_args(t['call'])
    if t['compare'] == 'isclose' and a[5] <= 12:
        b = crr_paths(*a, **k)
        rec(abs(b - float(t['expect'])) < 1e-9, f'c1 {t["call"]} = {b:.10f} by path enumeration')
    if t['compare'] == 'isclose' and k.get('call') is False and 'barrier' not in k:
        # put-call parity on the same tree: P = C - S + K e^{-rT}
        S_, K_, T_, r_ = a[0], a[1], a[2], a[3]
        c_ = ns1['crr_value'](*a)
        rec(abs(float(t['expect']) - (c_ - S_ + K_ * math.exp(-r_ * T_))) < 1e-9, f'c1 {t["call"]} obeys put-call parity on the tree')
bs1 = 100 * N01.cdf((math.log(1) + (0.05 + 0.02) * 1) / 0.2) - 100 * math.exp(-0.05) * N01.cdf((0.05 - 0.02) / 0.2)
big = [t for t in t1 if t['call'] == 'crr_value(100, 100, 1, 0.05, 0.2, 1000)'][0]
rec(abs(float(big['expect']) - bs1) < 0.005, f'c1 1,000 steps {float(big["expect"]):.4f} is within 0.005 of Black-Scholes {bs1:.4f}')
same = [t for t in t2 if t['call'] == 'crr_value(100, 100, 1, 0.05, 0.2, 200, barrier=1)'][0]
rec(abs(float(same['expect']) - ns1['crr_value'](100, 100, 1, 0.05, 0.2, 200)) < 1e-12, 'c1 a barrier at 1 changes nothing')
rootb = [t for t in t2 if t['call'].endswith('50, barrier=100)')][0]
rec(float(rootb['expect']) == 0.0, 'c1 a barrier at the start level kills the start: 0')
ex_ = [t for t in w2['examples'] if '4, barrier=95' in t['call']][0]
rec(abs(float(ex_['expect']) - crr_paths(100, 100, 1, 0.05, 0.2, 4, barrier=95)) < 5e-7
    and abs(crr_paths(100, 100, 1, 0.05, 0.2, 4, barrier=95) - crr_paths(100, 100, 1, 0.05, 0.2, 4)) > 1, 'c1 the first part 2 example differs from the vanilla price by over 1')
ns2 = {}
exec(w2['solution'].replace('S * u ** j * d ** (n - j)', 'S * u ** (2 * j - n)').replace('S * u ** j * d ** (step - j)', 'S * u ** (2 * j - step)'), ns2)
rec(all(abs(ns2['crr_value'](*crr_args(t['call'])[0], **crr_args(t['call'])[1]) - float(t['expect'])) < 1e-9
        for t in w2['tests']), 'c1 another node formula, u ** (2j - n), gives the same barrier prices')
allow('c1-barrier-tree', 1000, 2, 1e-12, 1e-9, 1, 0, 1.5)

# planted wrong versions of C1: each must fail at least one hidden test
sol2 = w2['solution']
C1_WRONGS = {
    'barrier checked at the last layer only': sol2.replace('if alive(S * u ** j * d ** (step - j)) else 0.0', ''),
    'knocked out only strictly below the barrier': sol2.replace('price > barrier', 'price >= barrier'),
    'root never checked': sol2.replace('if alive(S * u ** j * d ** (step - j)) else 0.0', 'if (step == 0 or alive(S * u ** j * d ** (step - j))) else 0.0'),
    'p below 0 not checked': sol2.replace('if not 0 < p < 1:', 'if p >= 1:'),
    'discounted once, at the end': sol2.replace('disc * (p * values[j + 1] + (1 - p) * values[j])', '(p * values[j + 1] + (1 - p) * values[j])').replace('return values[0]', 'return values[0] * disc'),
    'put flag ignored': sol2.replace('sign = 1 if call else -1', 'sign = 1'),
}
rec('(step == 0 or' in C1_WRONGS['root never checked'] and C1_WRONGS['barrier checked at the last layer only'] != sol2, 'c1 the planted versions differ from the solution')
for name, src in C1_WRONGS.items():
    rec(src != sol2 and run_py(src, t2) < len(t2), f'c1 planted wrong "{name}" fails {len(t2) - run_py(src, t2)} of {len(t2)} tests')


def run_cpp(src, tests):
    passed = 0
    with tempfile.TemporaryDirectory() as td:
        for t in tests:
            lits = []
            for a, ty in zip(t['args'], t['types']):
                lits.append(ty + '{' + ', '.join(repr(float(x)) for x in a) + '}' if isinstance(a, list) else repr(float(a)))
            main = src + '\n#include <cstdio>\nint main() { std::printf("%.17g\\n", (double)' + t['call'] + '(' + ', '.join(lits) + ')); }\n'
            open(os.path.join(td, 'm.cpp'), 'w').write(main)
            if subprocess.run(['g++', '-std=c++17', '-O1', '-Wall', os.path.join(td, 'm.cpp'), '-o', os.path.join(td, 'm')], capture_output=True).returncode:
                continue
            out = subprocess.run([os.path.join(td, 'm')], capture_output=True, text=True, timeout=20).stdout.strip()
            passed += close(float(out), float(t['expect']), t.get('tol', {'rel': 1e-9}))
    return passed


c2 = ITEM['c2-variance-interpolation']['widget']
rec(run_cpp(c2['solution'], c2['tests']) == len(c2['tests']), f'c2 C++ solution passes {len(c2["tests"])} tests (g++)')
rec(run_cpp(c2['starter'], c2['tests']) < len(c2['tests']), 'c2 the draft starter fails a test')
rec(run_cpp(c2['solution'], c2['examples']) == len(c2['examples']), 'c2 the examples pass')
rec('try' not in c2['solution'] and 'catch' not in c2['solution'], 'c2 uses no try or catch')
with tempfile.TemporaryDirectory() as td:
    open(os.path.join(td, 'm.cpp'), 'w').write(c2['solution'])
    r_ = subprocess.run(['clang++', '-std=c++17', '-O1', '-fno-exceptions', '-Wall', '-c', os.path.join(td, 'm.cpp'), '-o', os.path.join(td, 'm.o')], capture_output=True, text=True)
    rec(r_.returncode == 0 and not r_.stderr.strip(), 'c2 the solution compiles with clang++ -fno-exceptions and no warning', r_.stderr[:200])
sol_c = c2['solution']
LOOP = """    for (std::size_t i = 1; i < n; ++i)
        if (vols[i] * vols[i] * T[i] < vols[i - 1] * vols[i - 1] * T[i - 1]) return -1.0;
"""
C2_WRONGS = {
    'arbitrage checked only on the bracketing interval': sol_c.replace(LOOP, '').replace(
        '    const double w = w0 +', '    if (w1 < w0) return -1.0;\n    const double w = w0 +'),
    'total variance held flat after the last pillar': sol_c.replace(
        'if (t >= T[n - 1]) return vols[n - 1];', 'if (t >= T[n - 1]) return std::sqrt(vols[n - 1] * vols[n - 1] * T[n - 1] / t);'),
    'flat total variance treated as arbitrage': sol_c.replace('T[i] < vols[i - 1]', 'T[i] <= vols[i - 1]'),
    'vols squared but not times T': sol_c.replace('const double w0 = vols[i - 1] * vols[i - 1] * T[i - 1];', 'const double w0 = vols[i - 1] * vols[i - 1];').replace(
        'const double w1 = vols[i] * vols[i] * T[i];', 'const double w1 = vols[i] * vols[i];'),
}
for name, src in C2_WRONGS.items():
    rec(src != sol_c, f'c2 planted version "{name}" differs from the solution')
    rec(run_cpp(src, c2['tests']) < len(c2['tests']), f'c2 planted wrong "{name}" fails a test')



def vol_b(T, v, t):
    """route B: forward variances between pillars must be at least 0; integrate the piecewise-flat forward variance"""
    w = [x * x * y for x, y in zip(v, T)]
    if any(b < a for a, b in zip(w, w[1:])):
        return -1.0
    if t <= T[0]:
        return v[0]
    if t >= T[-1]:
        return v[-1]
    acc = w[0]
    for i in range(1, len(T)):
        fwd = (w[i] - w[i - 1]) / (T[i] - T[i - 1])
        acc += fwd * (min(t, T[i]) - T[i - 1])
        if t <= T[i]:
            break
    return math.sqrt(acc / t)


rec(all(abs(vol_b(*t['args']) - t['expect']) < 1e-12 for t in c2['tests']), 'c2 every expected vol matches the forward-variance route')
d_ = 0.2 + 0.05 * (0.25 / 0.75)
allow('c2-variance-interpolation', 0.25, 1, 0.01, 0.0625, 0.0275, 0.0525, 0.055, math.sqrt(0.055), d_, 3, 1.0)

allow('f1-why-strats', 200, 90, 2)
allow('f2-model-disagrees', 200)

# ======================================================================== structure
rec([p.get('minutes') for p in doc['parts'] if p['kind'] == 'paper'] == [30, 45, 30, 45, 15], 'papers 30, 45, 30, 45, 15 minutes')
rec(sum(len(p.get('items', [])) for p in doc['parts']) == 20, '20 items')
paper = {p['id']: p for p in doc['parts'] if p['kind'] == 'paper'}
# stochastic: S1 two parts, S2, S3, S4 longform (marked at 7 of 10); coding: C1 three parts, C2 one item
sto = paper['stochastic']
rec(sto['pass'] == 0.6, 'stochastic pass 0.6')
rec((1 + 1) / 4 < sto['pass'] and (1 + 1 + 0.5) / 4 >= sto['pass'] and (0.5 + 0.5 + 1) / 4 < sto['pass'], 'stochastic: S2 and S3 alone fail; S2, S3 and one part of S1 pass')
cod = paper['coding']
rec(cod['pass'] == 0.75, 'coding pass 0.75')
rec(1.0 / 2 < cod['pass'] and (1 + 1 / 3) / 2 < cod['pass'] and (1 + 2 / 3) / 2 >= cod['pass'], 'coding: C1 alone and C2 with one part fail; C2 with two parts passes')
rec(sum(it['pace'] for it in paper['coding']['items']) <= paper['coding']['minutes'] * 60 - 120, 'coding paces leave at least 120 s for the compiler start')
rec(sum(1 for it in ITEM.values() if it.get('kind') == 'longform') == 4, 'four longform items')
rec(all(sum(r['points'] for r in it['rubric']) == 10 for it in ITEM.values() if it.get('kind') == 'longform'), 'every rubric sums to 10')
for it in ITEM.values():
    for w in ([it['widget']] if 'widget' in it else [p['widget'] for p in it.get('parts', [])]):
        if w['kind'] == 'choice':
            rec(w.get('shuffle') is True, f'{it["id"]}: every choice shuffled')
firms = ('Goldman', 'Morgan Stanley', 'JP Morgan', 'Citadel', 'Jane Street', 'Optiver')
rec(not any(f in json.dumps(it) for it in ITEM.values() for f in firms), 'no firm named outside models and description')
rec('Reported' in doc['models'] and 'JP Morgan' in doc['models'] and 'This mock is built from reports' in doc['description'], 'models and description state only the reported format')
rec('Reported' in doc['models'] and 'Nov 2026' in doc['models'] and 'Nov 2026' in doc['description'], 'models and description say reported, Nov 2026')
rec(len(doc['models']) <= 200, f'models is {len(doc["models"])} characters')

# no shared item with another mock: ids, titles and question texts
others = [json.load(open(os.path.join(ROOT, 'app', 'content', 'exams', f))) for f in sorted(os.listdir(os.path.join(ROOT, 'app', 'content', 'exams')))
          if f.startswith('mock-') and f != 'mock-superday-strats.json']


def all_items(d):
    for p in d.get('parts', [d]):
        for it in p.get('items', []) or []:
            if isinstance(it, dict):
                yield it


seen_q = {re.sub(r'\W+', ' ', str(it.get('question', it.get('prompt', '')))).strip().lower() for d in others for it in all_items(d)}
seen_t = {it.get('tags', [''])[0] for d in others for it in all_items(d) if it.get('tags')}
mine_q = [re.sub(r'\W+', ' ', str(it.get('question', it.get('prompt', '')))).strip().lower() for it in ITEM.values()]
rec(not ((set(mine_q) & seen_q) - {''}), 'no question text repeats another mock')
rec(not ({it['tags'][0] for it in ITEM.values()} & seen_t), f'no family tag repeats another mock ({sorted({it["tags"][0] for it in ITEM.values()} & seen_t)})')

# ======================================================================== every number in every learner-visible string
SKIP = {'id', 'tags', 'kind', 'layout', 'answer', 'starter', 'solution', 'tests', 'examples', 'skills', 'placeholder', 'how', 'signature', 'label'}


def strings(o, k=None):
    if isinstance(o, str):
        if k not in SKIP:
            yield o
    elif isinstance(o, dict):
        for kk, v in o.items():
            if kk not in SKIP:
                yield from strings(v, kk)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v, k)


def tokens(s):
    s = re.sub(r'```.*?```', ' ', s, flags=re.S)
    s = re.sub(r'`[^`]*`', ' ', s)
    s = _FRAC.sub(lambda m: f' {m.group(1) or m.group(3)} {m.group(2) or m.group(4)} ', s)
    for m in _NUM.finditer(normalise(s)):
        t = m.group(0).rstrip('.')
        yield abs(float(t)), (len(t.split('.')[1]) if '.' in t and 'e' not in t.lower() else 0), t


for iid, it in ITEM.items():
    vals = [abs(v) for v in ALLOW.get(iid, [])]
    bad = []
    for s in strings({k: v for k, v in it.items() if k not in ('difficulty', 'pace')}):
        for v, dec, t in tokens(s):
            if dec == 0 and v == int(v) and v <= 10:
                continue
            half = 0.5 * 10 ** -dec
            if not any(abs(v - a_) < half * (1 - 1e-9) + 1e-12 for a_ in vals):
                bad.append(t)
    rec(not bad, f'{iid}: every stated number matches route B or a given', f'unmatched {sorted(set(bad))}' if bad else '')

ex.check_wrongs()
ex.report()
