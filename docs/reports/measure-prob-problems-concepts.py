#!/usr/bin/env python3
"""Blind concept audit, measure-prob problems-1 to problems-4.
Recomputes every numeric key and every named slip (exactly where possible), checks
every expression key at sample points, and runs a Monte Carlo check for each
empirical or limit claim. Exits 0 when every check passes.
Run from anywhere: python docs/reports/measure-prob-problems-concepts.py"""
import itertools, json, math, os, sys
from fractions import Fraction as F
import numpy as np
from scipy.stats import norm
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
CDIR = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'measure-prob')
rng = np.random.default_rng(20261126)
fails, nchk = [], 0
E, S = math.exp, math.sqrt


def chk(name, ok, detail=''):
    global nchk
    nchk += 1
    if not ok:
        fails.append(name)
    print(('ok   ' if ok else 'FAIL ') + name + (' | ' + detail if detail else ''))


SETS = {n: json.load(open(os.path.join(CDIR, f'problems-{n}.json'))) for n in (1, 2, 3, 4)}


def part(n, item, k):
    it = [i for i in SETS[n]['items'] if i['id'] == item][0]
    return it['parts'][k - 1]


def keys(n, item, k, answer, slips=None, strict=True):
    """answer and each named slip, recomputed here, must lie inside the content's band;
    every slip in the content must be recomputed here (none left unchecked);
    slip bands must not overlap the key band."""
    w = part(n, item, k)['widget']
    tag = f'p{n} {item} part {k}'
    assert w['kind'] == 'numeric', tag
    a, t = w['answer'], w['tol']['abs']
    chk(f'{tag} key', abs(float(answer) - a) <= t + 1e-12, f'got {float(answer):.7g}, content {a}, tol {t}')
    slips = slips or {}
    have = {s['id']: s for s in w.get('wrong', [])}
    chk(f'{tag} slips all recomputed', set(have) == set(slips), f'content {sorted(have)}, script {sorted(slips)}')
    for sid, val in slips.items():
        if sid not in have:
            continue
        s = have[sid]
        st = s['tol']['abs']
        chk(f'{tag} slip {sid}', abs(float(val) - s['value']) <= st + 1e-12,
            f'got {float(val):.7g}, content {s["value"]}, tol {st}')
        if strict:
            chk(f'{tag} slip {sid} clear of key', abs(s['value'] - a) > t + st, f'gap {abs(s["value"] - a):.4g}')


def choice(n, item, k, right):
    w = part(n, item, k)['widget']
    got = [o['id'] for o in w['options'] if o.get('correct')]
    chk(f'p{n} {item} part {k} choice key', got == [right], f'content {got}, script {right}')


def tex_eval(tex, **v):
    """tiny evaluator for the few expression keys of these sets"""
    import re
    s = tex
    s = s.replace('\\left', '').replace('\\right', '').replace('\\cdot', '*')
    for _ in range(6):
        s = re.sub(r'\^\{([^{}]*)\}', r'**(\1)', s)
        s = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
        s = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', s)
    s = s.replace('^', '**')
    s = re.sub(r'(\d)([a-z(])', r'\1*\2', s)
    s = re.sub(r'\)\(', ')*(', s)
    return eval(s, {'sqrt': math.sqrt}, v)


def expr(n, item, k, fn, var, pts, slipfns):
    w = part(n, item, k)['widget']
    tag = f'p{n} {item} part {k}'
    for tex in [w['answer']] + w.get('accept', []):
        ok = all(abs(tex_eval(tex, **{var: p}) - fn(p)) < 1e-9 for p in pts)
        chk(f'{tag} expr {tex}', ok)
    have = {s['id']: s['tex'] for s in w.get('wrong', [])}
    chk(f'{tag} expr slips all recomputed', set(have) == set(slipfns))
    for sid, f in slipfns.items():
        ok = all(abs(tex_eval(have[sid], **{var: p}) - f(p)) < 1e-9 for p in pts)
        differs = any(abs(f(p) - fn(p)) > 1e-6 for p in pts)
        chk(f'{tag} expr slip {sid}', ok and differs)


# ====================================================================== problems-1
# ---- fat Cantor
rem = lambda n: F(2) ** (n - 1) * F(1, 4) ** n
keys(1, 'p-fat-cantor', 1, rem(3), {'one-gap': F(1, 64), 'eight-gaps': F(8, 64)})
lenC = lambda n: 1 - sum(rem(k) for k in range(1, n + 1))
expr(1, 'p-fat-cantor', 2, lambda n: float(lenC(n)), 'n', [1, 2, 3, 6],
     {'shift': lambda n: 0.5 + 2.0 ** -n, 'last-only': lambda n: 1 - 2.0 ** -(n + 1), 'removed': lambda n: 2.0 ** -(n + 1)})
chk('p1 fat-cantor: C_1 = 3/4 and the stage-1 gap is (3/8, 5/8)', lenC(1) == F(3, 4) and F(5, 8) - F(3, 8) == F(1, 4))
keys(1, 'p-fat-cantor', 3, 0.5, {'zero': 0, 'stage-three': lenC(3)})
# every stage can be carried out: the gap is shorter than the interval it is cut from
chk('p1 fat-cantor: gap 4^-n fits each interval at every stage',
    all(lenC(n - 1) / 2 ** (n - 1) > F(1, 4) ** n for n in range(1, 40)))
# C holds no interval: the 2^n intervals of C_n have length below 2^-n
chk('p1 fat-cantor: intervals of C_n shorter than 2^-n', all(lenC(n) / 2 ** n < F(1, 2 ** n) for n in range(1, 40)))
choice(1, 'p-fat-cantor', 4, 'fin')


def in_fat_cantor(x, depth=22):
    lo, hi = np.zeros_like(x), np.ones_like(x)
    alive = np.ones(x.shape, bool)
    for n in range(1, depth + 1):
        mid, g = (lo + hi) / 2, 4.0 ** -n / 2
        gone = (x > mid - g) & (x < mid + g)
        alive &= ~gone
        left = x <= mid - g
        hi = np.where(left, mid - g, hi)
        lo = np.where(left, lo, mid + g)
    return alive


x = rng.random(2_000_000)
pc = in_fat_cantor(x).mean()
chk('MC p1 fat-cantor: uniform pick lands in C_22 with chance about 1/2 (not 0)', abs(pc - 0.5) < 0.003, f'{pc:.4f}')

# ---- ball machine
w = {o: F(o, 78) for o in range(1, 13)}
chk('p1 ball: chances add to 1', sum(w.values()) == 1)
X = lambda o: o % 4
Y = lambda o: 1 if o >= 10 else 0
atomsX = {}
for o in w:
    atomsX.setdefault(X(o), set()).add(o)
atomsXY = {}
for o in w:
    atomsXY.setdefault((X(o), Y(o)), set()).add(o)
keys(1, 'p-ball-machine', 1, 2 ** len(atomsX), {'atoms': len(atomsX), 'all': 2 ** 12})
keys(1, 'p-ball-machine', 2, 2 ** len(atomsXY), {'product': 2 ** 8, 'side-by-side': 2 ** (4 + 2)})
chk('p1 ball: {1,5,9} is the atom Y does not split', atomsXY.get((1, 0)) == {1, 5, 9} and (1, 1) not in atomsXY)
pX = {k: sum(w[o] for o in a) for k, a in atomsX.items()}
chk('p1 ball: P(X=k) = 24,15,18,21 over 78', [pX[k] * 78 for k in range(4)] == [24, 15, 18, 21])
FX = lambda x: sum(p for k, p in pX.items() if k <= x)
keys(1, 'p-ball-machine', 3, FX(2.5), {'uniform': F(9, 12), 'strict': sum(p for k, p in pX.items() if k < 2), 'complement': pX[3]})
smallest = min(k for k in range(4) if FX(k) >= F(3, 4))
unif = min(k for k in range(4) if F(sum(1 for o in w if X(o) <= k), 12) >= F(3, 4))
keys(1, 'p-ball-machine', 4, smallest, {'equal-chances': unif})
meas = lambda f: all(len({f(o) for o in a}) == 1 for a in atomsX.values())
chk('p1 ball part 5: only parity is sigma(X)-measurable',
    meas(lambda o: o % 2 == 0) and not meas(Y) and not meas(lambda o: math.ceil(o / 4)) and not meas(lambda o: o % 3))
choice(1, 'p-ball-machine', 5, 'parity')
chk('p1 ball part 5 whys: V(1)=1,V(9)=3; R(4)=1,R(8)=2', math.ceil(1 / 4) == 1 and math.ceil(9 / 4) == 3 and 4 % 3 == 1 and 8 % 3 == 2)

# ---- quote ladder
pN = lambda k: 0.4 ** k - 0.4 ** (k + 1)
keys(1, 'p-quote-ladder', 1, pN(2), {'rung': 0.16, 'next-rung': 0.064, 'swap': 0.4 * 0.6 ** 2})
expr(1, 'p-quote-ladder', 2, pN, 'k', [0, 1, 2, 5],
     {'tail': lambda k: 0.4 ** k, 'shift': lambda k: 0.4 ** (k + 1), 'swap': lambda k: 0.4 * 0.6 ** k})
tot = sum(pN(3 * j) for j in range(200))
keys(1, 'p-quote-ladder', 3, tot, {'no-zero': tot - 0.6, 'third': 1 / 3, 'two-terms': pN(0) + pN(3)})
chk('p1 ladder part 3: 25/39', abs(tot - 25 / 39) < 1e-12)
choice(1, 'p-quote-ladder', 4, 'all-b')
keys(1, 'p-quote-ladder', 5, sum(0.5 * 0.4 ** k for k in range(400)), {'half-band': 0.5, 'complement': 1 / 6})
U = 1 - rng.random(2_000_000)
N = np.floor(np.log(U) / math.log(0.4) + 1e-12).astype(int)
Xq = 0.4 ** N
chk('MC p1 ladder: quote is at or above the level', bool(np.all(Xq >= U * (1 - 1e-9))))
chk('MC p1 ladder: P(N=2) about 0.096', abs((N == 2).mean() - 0.096) < 0.001, f'{(N == 2).mean():.4f}')
chk('MC p1 ladder: P(N in 3Z) about 0.6410', abs((N % 3 == 0).mean() - 25 / 39) < 0.0015, f'{(N % 3 == 0).mean():.4f}')
chk('MC p1 ladder: P(X <= 2U) about 5/6', abs((Xq <= 2 * U).mean() - 5 / 6) < 0.0012, f'{(Xq <= 2 * U).mean():.4f}')

# ---- no double four
def count_no44(n):
    return sum(1 for s in itertools.product(range(10), repeat=n) if all(not (s[i] == 4 and s[i + 1] == 4) for i in range(n - 1)))


a = {1: 10, 2: 99}
for n in range(3, 401):
    a[n] = 9 * a[n - 1] + 9 * a[n - 2]
chk('p1 44: recursion matches brute force for n = 3, 4, 5', all(count_no44(n) == a[n] for n in (3, 4, 5)))
keys(1, 'p-no-double-four', 1, F(a[3], 1000), {'overlap': F(980, 1000), 'first-pair': F(99, 100)})
keys(1, 'p-no-double-four', 2, F(a[4], 10 ** 4),
     {'one-term': F(9 * a[3], 10 ** 4), 'square': 0.981 ** 2, 'independent': 0.981 * 0.99})
keys(1, 'p-no-double-four', 3, 0.99 ** 100, {'all-places': 0.99 ** 199, 'all-digits': 0.99 ** 200})
pD200 = a[200] / 10 ** 200
chk('p1 44 part 3: 0.99^100 is a valid upper bound on P(D_200)', pD200 <= 0.99 ** 100, f'P(D_200) = {pD200:.4f}')
chk('p1 44 part 3 slip: 0.99^199 is NOT a valid upper bound (feedback says so)', pD200 > 0.99 ** 199, f'{pD200:.4f} > {0.99 ** 199:.4f}')
chk('p1 44 part 4: P(D_2m) <= 0.99^m for m to 200', all(a[2 * m] / 10 ** (2 * m) <= 0.99 ** m for m in range(1, 201)))
keys(1, 'p-no-double-four', 4, 0, {'complement': 1})
choice(1, 'p-no-double-four', 5, 'sub')
d = rng.integers(0, 10, size=(40_000, 200))
no44 = ~((d[:, :-1] == 4) & (d[:, 1:] == 4)).any(axis=1)
chk('MC p1 44: P(D_200) matches the recursion', abs(no44.mean() - pD200) < 0.008, f'MC {no44.mean():.4f}, exact {pD200:.4f}')

# ====================================================================== problems-2
# ---- settlement fails
pk = lambda k: 0.64 * (k + 1) * 0.2 ** k
K = range(0, 600)
chk('p2 fails: chances add to 1', abs(sum(pk(k) for k in K) - 1) < 1e-12)
EN = sum(k * pk(k) for k in K)
G = lambda s: sum(0.64 * (k + 1) * (0.2 * s) ** k for k in K)
keys(2, 'p-settlement-fails', 1, G(1.25), {'jensen': 1.25 ** EN, 'no-k': 0.64 / 0.75})
chk('p2 fails: G(s) = 16/(5-s)^2 at s = 0.3, 1.25, 4', all(abs(G(s) - 16 / (5 - s) ** 2) < 1e-6 for s in (0.3, 1.25, 4)))
Gp = lambda s: sum(k * s ** (k - 1) * pk(k) for k in K if k >= 1)
chk("p2 fails: G'(s) = 32/(5-s)^3 and rises with s on [0,1)",
    all(abs(Gp(s) - 32 / (5 - s) ** 3) < 1e-9 for s in (0, 0.5, 0.9)) and Gp(0.2) < Gp(0.6) < Gp(0.99) < EN)
choice(2, 'p-settlement-fails', 2, 'mct')
keys(2, 'p-settlement-fails', 3, EN, {'one': 1, 'at-zero': pk(1), 'square': 32 / 16})
chk("p2 fails: G'(0) = 32/125 = P(N=1)", abs(32 / 125 - pk(1)) < 1e-12)
EN2 = sum(k * k * pk(k) for k in K)
keys(2, 'p-settlement-fails', 4, EN2, {'falling': EN2 - EN, 'variance': EN2 - EN ** 2, 'mean-sq': EN ** 2})
chk('p2 fails: 96/4^4 = E[N(N-1)]', abs(96 / 256 - (EN2 - EN)) < 1e-12)
part6 = [6 ** k * pk(k) for k in range(0, 60)]
chk('p2 fails part 5: terms 0.64(k+1)1.2^k grow, series diverges', all(part6[i + 1] > part6[i] for i in range(59)))
choice(2, 'p-settlement-fails', 5, 'inf')
# N is negative binomial: number of failures before the 2nd success, success chance 0.8
Nmc = rng.negative_binomial(2, 0.8, size=2_000_000)
chk('MC p2 fails: law is NB(2, 0.8); E[N] 0.5, E[N^2] 0.875, E[1.25^N] 1.1378',
    abs(Nmc.mean() - 0.5) < 0.003 and abs((Nmc ** 2.0).mean() - 0.875) < 0.008 and abs((1.25 ** Nmc).mean() - 256 / 225) < 0.002,
    f'{Nmc.mean():.4f}, {(Nmc ** 2.0).mean():.4f}, {(1.25 ** Nmc).mean():.4f}')

# ---- compounding
m2, m4 = 0.25, 3 * 0.25 ** 2
keys(2, 'p-compounding', 1, 1 + m2 / 4, {'no-square': 1, 'half-square': 1 + m2 / 2})
EG4 = 1 + 6 * m2 / 16 + m4 / 256
keys(2, 'p-compounding', 2, EG4, {'no-fourth': 1 + 6 * m2 / 16, 'fourth-one': 1 + 6 * m2 / 16 + 0.25 ** 2 / 256})
dens = lambda r: norm.pdf(r, scale=0.5)
exact_abs = integrate.quad(lambda r: E(abs(r)) * dens(r), -12, 12)[0]
chk('p2 compounding: E[e^|R|] = 2 e^{1/8} Phi(0.5) (quadrature)', abs(exact_abs - 2 * E(0.125) * norm.cdf(0.5)) < 1e-9, f'{exact_abs:.6f}')
keys(2, 'p-compounding', 3, 2 * E(0.125) * 0.6915, {'no-abs': E(0.125), 'no-phi': 2 * E(0.125)})
chk('p2 compounding part 4 why: G_1,G_2,G_3 at R=-3 are -2, 0.25, 0', [(1 - 3 / n) ** n for n in (1, 2, 3)] == [-2, 0.25, 0])
choice(2, 'p-compounding', 4, 'dct')
keys(2, 'p-compounding', 5, E(0.125), {'jensen': 1, 'no-half': E(0.25), 'bound': 2 * E(0.125) * 0.6915})
EGn = lambda n: integrate.quad(lambda r: (1 + r / n) ** n * dens(r), -12, 12, limit=400)[0]
chk('p2 compounding: E[G_2], E[G_4] by quadrature', abs(EGn(2) - 1.0625) < 1e-7 and abs(EGn(4) - EG4) < 1e-7)
chk('p2 compounding: E[G_n] -> e^{1/8} from below (n = 2, 4, 50, 400)',
    EGn(2) < EGn(4) < EGn(50) < EGn(400) < E(0.125) and E(0.125) - EGn(400) < 1e-3, f'{EGn(400):.5f}')
R = 0.5 * rng.standard_normal(1_000_000)
chk('MC p2 compounding: |G_n| <= e^|R| on every draw, n = 1, 2, 3, 7, 50',
    all(bool(np.all(np.abs((1 + R / n) ** n) <= np.exp(np.abs(R)) * (1 + 1e-12))) for n in (1, 2, 3, 7, 50)))
chk('MC p2 compounding: G_1 is negative on about 2.3% of draws, so G_n is not non-negative', abs(((1 + R) < 0).mean() - norm.cdf(-2)) < 0.001)

# ---- boom bust
r1 = (S(1.6) + S(0.4)) / 2
chk('p2 boom: E sqrt(M_1) = sqrt(0.9) = 3/sqrt(10)', abs(r1 - S(0.9)) < 1e-12 and abs(r1 - 3 / S(10)) < 1e-12)
expr(2, 'p-boom-bust', 1, lambda n: r1 ** n, 'n', [1, 2, 4, 7],
     {'geo': lambda n: 0.8 ** n, 'no-half': lambda n: (S(1.6) + S(0.4)) ** n, 'squared': lambda n: 0.9 ** n})
keys(2, 'p-boom-bust', 2, r1 ** 4 / S(0.5), {'no-root': r1 ** 4, 'epsilon': r1 ** 4 / 0.5, 'markov-m': 1 / 0.5})
from math import comb
pm4 = lambda pred: sum(comb(4, k) for k in range(5) if pred(1.6 ** k * 0.4 ** (4 - k))) / 16
keys(2, 'p-boom-bust', 3, pm4(lambda m: m > 0.5), {'two-ups': 11 / 16, 'all-up': 1 / 16, 'three-only': 4 / 16})
tail = sum(10 * r1 ** n for n in range(200, 3000))
keys(2, 'p-boom-bust', 4, tail, {'one-day': 10 * r1 ** 200, 'no-root': tail / 10, 'epsilon': tail * 10})
keys(2, 'p-boom-bust', 5, 1.36 ** 10, {'mean-sq': 1, 'added': 13.6, 'one-day': 1.36})
chk('p2 boom: E[M_1^2] = 1.36, E[M_1] = 1', abs((2.56 + 0.16) / 2 - 1.36) < 1e-12 and (1.6 + 0.4) / 2 == 1)
ups = rng.random((20_000, 600)) < 0.5
logM = np.cumsum(np.where(ups, math.log(1.6), math.log(0.4)), axis=1)
late = (logM[:, 199:] > math.log(0.01)).any(axis=1).mean()
chk('MC p2 boom: P(M_n > 0.01 for some n in 200..600) is below the bound 0.00518', late <= 0.005176, f'{late:.5f}')
chk('MC p2 boom: M_600 < 1e-6 on nearly every path (a.s. limit 0), though E[M_n] = 1',
    (logM[:, -1] < math.log(1e-6)).mean() > 0.999)
ups10 = rng.random((4_000_000, 10)) < 0.5
M10 = np.prod(np.where(ups10, 1.6, 0.4), axis=1)
chk('MC p2 boom: E[M_10^2] about 21.65 and E[M_10] about 1', abs((M10 ** 2).mean() - 1.36 ** 10) < 1.2 and abs(M10.mean() - 1) < 0.01,
    f'{(M10 ** 2).mean():.2f}, {M10.mean():.4f}')

# ---- random maturity
V = lambda r: integrate.quad(lambda t: E(-r * t) / 4, 0, 4)[0]
keys(2, 'p-random-maturity', 1, V(0.05), {'mean-time': E(-0.1), 'end': E(-0.2)})
chk('p2 maturity: closed form (1-e^{-4r})/(4r)', abs(V(0.05) - (1 - E(-0.2)) / 0.2) < 1e-12)
choice(2, 'p-random-maturity', 2, 'four')
hh = [(r, h) for r in np.linspace(0, 1, 21) for h in (-0.3, -0.01, 1e-4, 0.2) if 0 <= r + h <= 1]
tt = np.linspace(0, 4, 401)
q = max(np.max(np.abs((np.exp(-(r + h) * tt) - np.exp(-r * tt)) / h)) for r, h in hh)
chk('p2 maturity part 2: quotients bounded by 4 but not by 1', 1 < q <= 4 + 1e-9, f'max |quotient| {q:.4f}')
mV = integrate.quad(lambda t: t * E(-0.05 * t) / 4, 0, 4)[0]
keys(2, 'p-random-maturity', 3, mV, {'jensen': 2 * E(-0.1), 'no-discount': 2})
chk("p2 maturity: -V'(0.05) by central difference and by the closed form",
    abs(-(V(0.05 + 1e-5) - V(0.05 - 1e-5)) / 2e-5 - mV) < 1e-7 and abs((1 - 1.2 * E(-0.2)) / 0.01 - mV) < 1e-10)
keys(2, 'p-random-maturity', 4, mV / V(0.05), {'mean': 2, 'no-divide': mV, 'inverse': V(0.05) / mV})
chk('p2 maturity part 4: the carried rounded values give the same answer', abs(1.7523 / 0.9063 - mV / V(0.05)) < 0.004)

# ====================================================================== problems-3
# ---- nested forecasts
p = [F(1, 10), F(15, 100), F(25, 100), F(2, 10), F(2, 10), F(1, 10)]
xv = [-3, 1, 5, 2, 6, -4]
chk('p3 nested: chances add to 1', sum(p) == 1)
Gat = [[0], [1, 2], [3, 4], [5]]
Hat = [[0, 1, 2], [3, 4, 5]]


def cond(vals, atoms):
    out = [None] * 6
    for A in atoms:
        m = sum(p[i] * vals[i] for i in A) / sum(p[i] for i in A)
        for i in A:
            out[i] = m
    return out


Ex = lambda v: sum(pi * vi for pi, vi in zip(p, v))
EG_, EH_ = cond(xv, Gat), cond(xv, Hat)
keys(3, 'p-nested-forecasts', 1, 2 ** 4 - 2 ** 2, {'all': 16, 'atoms': 2})
keys(3, 'p-nested-forecasts', 2, EG_[1], {'unweighted': 3, 'no-divide': p[1] * 1 + p[2] * 5})
tower = cond(EG_, Hat)
chk('p3 nested: tower property E[E[X|G]|H] = E[X|H] on every scenario', tower == EH_)
keys(3, 'p-nested-forecasts', 3, tower[0], {'unweighted': F(-3) / 2 + F(35, 20), 'finer': EG_[1]})
chk('p3 nested: E[X|G] = -3, 3.5, 4, -4 and E[X|H] = 2.2, 2.4', [EG_[0], EG_[1], EG_[3], EG_[5]] == [-3, F(7, 2), 4, -4] and [EH_[0], EH_[3]] == [F(11, 5), F(12, 5)])
mseG = Ex([(a - b) ** 2 for a, b in zip(xv, EG_)])
var = Ex([(a - Ex(xv)) ** 2 for a in xv])
keys(3, 'p-nested-forecasts', 4, mseG, {'one-atom': p[1] * F(25, 4) + p[2] * F(9, 4), 'overall-mean': var})
mseH = Ex([(a - b) ** 2 for a, b in zip(xv, EH_)])
gap = Ex([(a - b) ** 2 for a, b in zip(EG_, EH_)])
chk('p3 nested: Pythagoras, MSE_H = MSE_G + gap', mseH == mseG + gap)
keys(3, 'p-nested-forecasts', 5, gap, {'mse-h': mseH, 'one-side': sum(p[i] * (EG_[i] - EH_[i]) ** 2 for i in range(3))})

# ---- Doob split
pu = F(7, 10)
paths3 = list(itertools.product((1, -1), repeat=3))
pr = lambda w_: math.prod(pu if s == 1 else 1 - pu for s in w_)
drift = lambda s: (pu * ((s + 1) ** 2 - s * s) + (1 - pu) * ((s - 1) ** 2 - s * s))
expr(3, 'p-doob-split', 1, lambda s: float(drift(F(s))), 's', [-2, 0, 1, 3],
     {'fair': lambda s: 1.0, 'no-square': lambda s: 0.8 * s, 'half-drift': lambda s: 0.4 * s + 1})


def A_of(w_, n, shift=0, upto=None):
    Svals = [0]
    for s in w_:
        Svals.append(Svals[-1] + s)
    ks = range(shift, (upto if upto is not None else n) + shift)
    return sum(F(8, 10) * Svals[k] + 1 for k in ks)


uud = (1, 1, -1)
keys(3, 'p-doob-split', 2, A_of(uud, 3), {'one-more': A_of(uud, 3, upto=4), 'shifted': A_of(uud, 3, shift=1), 'fair': 3})
chk('p3 doob part 3 why: A_3 on down, down, up is 0.6', A_of((-1, -1, 1), 3) == F(6, 10))
choice(3, 'p-doob-split', 3, 'pred')
# martingale check at every node: E[M_{n+1} | F_n] = M_n
ok = True
for n in range(0, 3):
    for pre in itertools.product((1, -1), repeat=n):
        s = sum(pre)
        Mn = s * s - A_of(pre + (1,) * (3 - n), n)
        nxt = sum((pu if st == 1 else 1 - pu) * ((s + st) ** 2 - A_of(pre + (st,) + (1,) * (2 - n), n + 1)) for st in (1, -1))
        ok &= (nxt == Mn)
chk('p3 doob: M = S^2 - A is a martingale at every node to n = 3', ok)
ES3sq = sum(pr(w_) * sum(w_) ** 2 for w_ in paths3)
chk('p3 doob: E[A_3] = E[S_3^2]', sum(pr(w_) * A_of(w_, 3) for w_ in paths3) == ES3sq)
keys(3, 'p-doob-split', 4, ES3sq, {'fair': 3, 'mean-squared': F(12, 10) ** 2, 'path': A_of(uud, 3)})

# ---- two ups stop
def stopT(w_):
    for n in range(2, 5):
        if w_[n - 2] == 1 and w_[n - 1] == 1:
            return n
    return 4


paths4 = list(itertools.product((1, -1), repeat=4))
T = {w_: stopT(w_) for w_ in paths4}
ST = {w_: sum(w_[:T[w_]]) for w_ in paths4}
PT = lambda n: F(sum(1 for w_ in paths4 if T[w_] == n), 16)
keys(3, 'p-two-ups-stop', 1, PT(3), {'any-pair': F(1, 4), 'four-days': F(1, 16)})
chk('p3 two-ups: P(T=2) = 1/4, P(T=4) = 5/8', PT(2) == F(1, 4) and PT(4) == F(5, 8))
ET = sum(F(T[w_], 16) for w_ in paths4)
keys(3, 'p-two-ups-stop', 2, ET, {'any-pair': 2 * F(1, 4) + 3 * F(1, 4) + 4 * F(1, 2), 'equal': 3})
EST = sum(F(ST[w_], 16) for w_ in paths4)
early = sum(F(ST[w_], 16) for w_ in paths4 if T[w_] < 4)
keys(3, 'p-two-ups-stop', 3, EST, {'early-only': early})
EST2 = sum(F(ST[w_] ** 2, 16) for w_ in paths4)
chk('p3 two-ups: E[S_T^2] = E[T] by enumeration', EST2 == ET)
keys(3, 'p-two-ups-stop', 4, EST2, {'fixed-day': 4, 'square-of-mean': EST ** 2}, strict=False)
late = sum(F(ST[w_], 16) for w_ in paths4 if T[w_] == 4)
keys(3, 'p-two-ups-stop', 5, late, {'sign': -late, 'conditional': late / PT(4)})

# ---- trial stake
leaf = {('f',): (F(4, 10), 20), ('s', 'r'): (F(6, 10) * F(1, 4), 40),
        ('s', 'a', 'w'): (F(6, 10) * F(3, 4) * F(2, 10), 50), ('s', 'a', 'g'): (F(6, 10) * F(3, 4) * F(8, 10), 100)}
chk('p3 trial: leaf chances add to 1', sum(v[0] for v in leaf.values()) == 1)


def Mn(pre):
    sub = [(pp, x) for k, (pp, x) in leaf.items() if k[:len(pre)] == pre[:len(k)][:len(pre)] and (len(k) >= len(pre) or k == pre[:len(k)])]
    sub = [(pp, x) for k, (pp, x) in leaf.items() if k[:min(len(k), len(pre))] == pre[:min(len(k), len(pre))]]
    return sum(pp * x for pp, x in sub) / sum(pp for pp, x in sub)


keys(3, 'p-trial-stake', 1, Mn(('s',)), {'approved': Mn(('s', 'a')), 'no-refusal': F(3, 4) * 90, 'unweighted': F(190, 3)})
chk('p3 trial: M_0 = 54.5, M_2(approved) = 90', Mn(()) == F(109, 2) and Mn(('s', 'a')) == 90)


def sale(rule):
    """returns list of (chance, sale price, time) per leaf under a first-passage rule on M"""
    out = []
    for k, (pp, x) in leaf.items():
        for n in (1, 2, 3):
            m = Mn(k[:n])
            if rule(m) or n == 3:
                out.append((pp, m, n))
                break
    return out


s1, s2 = sale(lambda m: m >= 80), sale(lambda m: m <= 45)
keys(3, 'p-trial-stake', 2, sum(pp for pp, m, n in s1 if n == 2), {'at-success': F(6, 10), 'strong': F(36, 100), 'approval': F(3, 4)})
chk('p3 trial part 3: E[M_T] = 54.5 for both rules', sum(pp * m for pp, m, n in s1) == F(109, 2) == sum(pp * m for pp, m, n in s2))
chk('p3 trial part 3 whys: rule 1 pays 90/20/40; rule 2 sells at 20 or 40 before the end',
    sorted({m for pp, m, n in s1}) == [20, 40, 90] and {(m, n) for pp, m, n in s2 if n < 3} == {(20, 1), (40, 2)})
choice(3, 'p-trial-stake', 3, 'both')
EM2 = sum(pp * m * m for pp, m, n in s1)
varX = sum(pp * x * x for pp, x in leaf.values()) - F(109, 2) ** 2
vMT = EM2 - F(109, 2) ** 2
keys(3, 'p-trial-stake', 4, vMT, {'hold': varX, 'no-mean': EM2, 'gap': varX - vMT})

# ====================================================================== problems-4
# ---- recovery reweight
expr(4, 'p-recovery-reweight', 1, lambda x: 4 * x ** 3 / (2 * x), 'x', [0.2, 0.5, 0.9],
     {'reversed': lambda x: 1 / (2 * x * x), 'q-only': lambda x: 4 * x ** 3, 'product': lambda x: 8 * x ** 4})
qd = lambda f, a, b, **kw: integrate.quad(f, a, b, **kw)[0]
QA = qd(lambda x: 2 * x * x * 2 * x, 0.8, 1)
keys(4, 'p-recovery-reweight', 2, QA, {'no-weight': qd(lambda x: 2 * x, 0.8, 1), 'frozen': 2 * 0.64 * 0.36, 'complement': 0.8 ** 4})
EZ = qd(lambda x: 2 * x * x * 2 * x, 0, 1)
EZ2 = qd(lambda x: (2 * x * x) ** 2 * 2 * x, 0, 1)
keys(4, 'p-recovery-reweight', 3, EZ2 - EZ ** 2, {'second-moment': EZ2, 'under-q': qd(lambda x: (2 * x * x) ** 2 * 4 * x ** 3, 0, 1) - 1})
chk('p4 recovery part 4: E_Q[(dP/dQ)^2] over (eps,1) = ln(1/eps), unbounded',
    all(abs(qd(lambda x: (1 / (2 * x * x)) ** 2 * 4 * x ** 3, e, 1, limit=200) - math.log(1 / e)) < 1e-6 for e in (1e-2, 1e-4, 1e-6)))
choice(4, 'p-recovery-reweight', 4, 'infinite')
u = rng.random(4_000_000)
xp, xq = np.sqrt(u), u ** 0.25
est_fwd = (2 * xp ** 2 * (xp > 0.8)).mean()
chk('MC p4 recovery: P-draws weighted by 2X^2 give Q(X > 0.8) = 0.5904', abs(est_fwd - 0.5904) < 0.002, f'{est_fwd:.4f}')
chk('MC p4 recovery: Var_P(Z) about 1/3', abs((2 * xp ** 2).var() - 1 / 3) < 0.002)
wrev = 1 / (2 * xq ** 2)
chk('MC p4 recovery: reverse sampler is unbiased (mean weight about 1)', abs(wrev.mean() - 1) < 0.02, f'{wrev.mean():.4f}')
# infinite mean square: the sample mean square keeps growing like (1/4) ln n instead of settling
ms = [np.mean(wrev[:n] ** 2) for n in (4_000, 400_000, 4_000_000)]
# median over blocks is steadier than one run
blocks = lambda n: np.median((wrev[: (len(wrev) // n) * n].reshape(-1, n) ** 2).mean(axis=1))
b = [blocks(n) for n in (100, 10_000, 1_000_000)]
chk('MC p4 recovery: sample mean square of dP/dQ under Q grows with n (no finite limit)', b[0] < b[1] < b[2], f'{b[0]:.2f}, {b[1]:.2f}, {b[2]:.2f}')
# error does not shrink like 1/sqrt(n): sqrt(n) * (interquantile spread of the mean) grows
spread = []
for n in (100, 10_000):
    mm = wrev[: (len(wrev) // n) * n].reshape(-1, n).mean(axis=1)
    spread.append(S(n) * (np.quantile(mm, 0.99) - np.quantile(mm, 0.01)))
chk('MC p4 recovery: sqrt(n) x spread of the reverse estimate grows with n', spread[1] > 1.15 * spread[0], f'{spread[0]:.2f} -> {spread[1]:.2f}')

# ---- share numeraire
u_, d_, Rr, S0 = 1.25, 0.85, 1.02, 48.0
q_ = (Rr - d_) / (u_ - d_)
chk('p4 numeraire: q = 0.425', abs(q_ - 0.425) < 1e-12)
paths = list(itertools.product((1, 0), repeat=3))
S3 = lambda w_: S0 * math.prod(u_ if s else d_ for s in w_)
Qp = lambda w_: math.prod(q_ if s else 1 - q_ for s in w_)
Z3 = lambda w_: S3(w_) / (S0 * Rr ** 3)
keys(4, 'p-share-numeraire', 1, Z3((1, 0, 0)), {'no-discount': S3((1, 0, 0)) / S0, 'one-discount': S3((1, 0, 0)) / S0 / Rr})
chk('p4 numeraire part 2: E_Q[Z_3] = 1, Z_3 in (0, 2)', abs(sum(Qp(w_) * Z3(w_) for w_ in paths) - 1) < 1e-12 and all(0 < Z3(w_) < 2 for w_ in paths))
choice(4, 'p-share-numeraire', 2, 'mart')
QS = lambda w_: Qp(w_) * Z3(w_)
qS = sum(QS(w_) for w_ in paths if w_[0] == 1)
chk('p4 numeraire: steps are i.i.d. under Q^S with up chance 25/48',
    all(abs(QS(w_) - math.prod(qS if s else 1 - qS for s in w_)) < 1e-12 for w_ in paths) and abs(qS - 25 / 48) < 1e-12)
keys(4, 'p-share-numeraire', 3, qS, {'no-cash': q_ * u_, 'down-factor': q_ * d_ / Rr, 'down-chance': 1 - qS})
chk('p4 numeraire part 3 slip: q*1.25 plus the down weight exceeds 1', q_ * u_ + (1 - q_) * d_ > 1)
price = sum(Qp(w_) * S3(w_) for w_ in paths if S3(w_) > 50) / Rr ** 3
pS = sum(QS(w_) for w_ in paths if S3(w_) > 50)
chk('p4 numeraire part 4: price = 48 Q^S(S_3 > 50); the three wrong options differ',
    abs(price - 48 * pS) < 1e-10 and abs(price - 48 * sum(Qp(w_) for w_ in paths if S3(w_) > 50)) > 1
    and abs(price - pS / Rr ** 3) > 1 and abs(price - sum(QS(w_) * S3(w_) for w_ in paths if S3(w_) > 50) / Rr ** 3) > 1)
choice(4, 'p-share-numeraire', 4, 'qs')
keys(4, 'p-share-numeraire', 5, price,
     {'q-chance': 48 * sum(Qp(w_) for w_ in paths if S3(w_) > 50), 'top-only': 48 * qS ** 3, 'discount': price / Rr ** 3})
chk('p4 numeraire: end prices 43.35, 63.75, 93.75', [round(S3(w_), 4) for w_ in ((1, 0, 0), (1, 1, 0), (1, 1, 1))] == [43.35, 63.75, 93.75])

# ---- ten trades
wgt = lambda k: 0.625 ** k * 2.5 ** (10 - k)
PA = sum(comb(10, k) for k in (8, 9, 10)) / 1024
chk('p4 trades: P(A) = 7/128', abs(PA - 7 / 128) < 1e-15)
keys(4, 'p-ten-trades', 1, wgt(8), {'reversed': 1 / wgt(8), 'wins-only': 0.625 ** 8})
EY2 = sum(comb(10, k) * wgt(k) for k in (8, 9, 10)) / 1024
EY2q = sum(comb(10, k) * 0.8 ** k * 0.2 ** (10 - k) * wgt(k) ** 2 for k in (8, 9, 10))
chk('p4 trades: E_Q[Y^2] = E_P[1_A dP/dQ]', abs(EY2 - EY2q) < 1e-15)
keys(4, 'p-ten-trades', 2, EY2, {'no-weight': PA, 'eight-only': 45 * wgt(8) / 1024})
chk('p4 trades: weights 0.14552, 0.03638, 0.00909', [round(wgt(k), 5) for k in (8, 9, 10)] == [0.14552, 0.03638, 0.00909])
c = 0.00676  # the value carried forward
rel = S(c - PA ** 2) / PA
keys(4, 'p-ten-trades', 3, rel, {'no-mean': S(c) / PA, 'no-root': (c - PA ** 2) / PA ** 2})
chk('p4 trades part 3: the unrounded E_Q[Y^2] gives the same 2 d.p. answer', abs(S(EY2 - PA ** 2) / PA - rel) < 0.001 and round(S(EY2 - PA ** 2) / PA, 2) == 1.12)
plain2 = (1 - PA) / PA
keys(4, 'p-ten-trades', 4, plain2 / 1.12 ** 2, {'not-squared': S(plain2) / 1.12, 'plain-only': plain2})
chk('p4 trades part 4: unrounded ratio also rounds to 14', round(plain2 / ((EY2 - PA ** 2) / PA ** 2)) == 14)
wins = rng.binomial(10, 0.8, size=4_000_000)
Ymc = np.where(wins >= 8, 0.625 ** wins * 2.5 ** (10 - wins), 0.0)
chk('MC p4 trades: Q-sampler is unbiased for P(A) and has relative error about 1.12 per draw',
    abs(Ymc.mean() - PA) < 0.0002 and abs(Ymc.std() / PA - 1.1225) < 0.01, f'{Ymc.mean():.5f}, {Ymc.std() / PA:.4f}')
hit = rng.binomial(10, 0.5, size=4_000_000) >= 8
chk('MC p4 trades: plain relative error per draw about 4.16, variance ratio about 14',
    abs(hit.std() / PA - S(121 / 7)) < 0.03 and abs(hit.var() / Ymc.var() - 13.72) < 0.4, f'{hit.var() / Ymc.var():.2f}')

# ---- premium weight
pP = F(6, 10)
qQ = (F(40) * F(101, 100) - 34) / (48 - 34)
keys(4, 'p-premium-weight', 1, qQ, {'no-cash': F(6, 14), 'down': 1 - qQ})
Zu, Zd = qQ / pP, (1 - qQ) / (1 - pP)
keys(4, 'p-premium-weight', 2, Zd, {'up': Zu, 'inverse': 1 / Zd, 'no-cash': (1 - F(3, 7)) / (1 - pP)})
EZS = pP * Zu * 48 + (1 - pP) * Zd * 34
ES1 = pP * 48 + (1 - pP) * 34
chk('p4 premium: E_P[Z_1] = 1, E_P[Z_1 S_1] = 40.4, E_P[S_1] = 42.4', pP * Zu + (1 - pP) * Zd == 1 and EZS == F(404, 10) and ES1 == F(424, 10))
keys(4, 'p-premium-weight', 3, EZS - ES1, {'sign': ES1 - EZS, 'no-mean': EZS})
EZ1sq = pP * Zu ** 2 + (1 - pP) * Zd ** 2
chk('p4 premium part 4 why: E_Q[Z_1] = E_P[Z_1^2] about 1.085', abs(float(EZ1sq) - 1.085) < 5e-4 and qQ * Zu + (1 - qQ) * Zd == EZ1sq)
choice(4, 'p-premium-weight', 4, 'any')
two = list(itertools.product((1, 0), repeat=2))
P2 = lambda w_: math.prod(pP if s else 1 - pP for s in w_)
Z2 = lambda w_: math.prod(Zu if s else Zd for s in w_)
S2 = lambda w_: 40 * math.prod(F(12, 10) if s else F(85, 100) for s in w_)
cov2 = sum(P2(w_) * Z2(w_) * S2(w_) for w_ in two) - sum(P2(w_) * Z2(w_) for w_ in two) * sum(P2(w_) * S2(w_) for w_ in two)
keys(4, 'p-premium-weight', 5, cov2, {'doubled': 2 * (EZS - ES1), 'sign': -cov2, 'cash-once': F(404, 10) - sum(P2(w_) * S2(w_) for w_ in two)})
chk('p4 premium: Z_2 is smallest on up, up; E_P[S_2] = 44.944', min(two, key=Z2) == (1, 1) and sum(P2(w_) * S2(w_) for w_ in two) == F(44944, 1000))

# ---- answers a learner types to the stated places must land in the key band
def typed(n, item, k, places):
    w = part(n, item, k)['widget']
    v = round(w['answer'], places)
    chk(f'p{n} {item} part {k}: answer typed to {places} d.p. is accepted', abs(v - w['answer']) <= w['tol']['abs'] + 1e-12, f'{v}')
    for s in w.get('wrong', []):
        sv = round(s['value'], places)
        chk(f'p{n} {item} part {k}: slip {s["id"]} typed to {places} d.p. is caught',
            abs(sv - s['value']) <= s['tol']['abs'] * (1 + 1e-9), f'{sv} vs {s["value"]}')


for args in [(1, 'p-ball-machine', 3, 4), (1, 'p-quote-ladder', 3, 4), (1, 'p-quote-ladder', 5, 4), (1, 'p-no-double-four', 2, 3),
             (1, 'p-no-double-four', 3, 3), (2, 'p-settlement-fails', 1, 4), (2, 'p-compounding', 2, 4), (2, 'p-compounding', 3, 3),
             (2, 'p-compounding', 5, 4), (2, 'p-boom-bust', 2, 4), (2, 'p-boom-bust', 4, 5), (2, 'p-boom-bust', 5, 2),
             (2, 'p-random-maturity', 1, 4), (2, 'p-random-maturity', 3, 4), (2, 'p-random-maturity', 4, 2),
             (3, 'p-trial-stake', 1, 2), (3, 'p-trial-stake', 4, 2), (4, 'p-recovery-reweight', 2, 4), (4, 'p-recovery-reweight', 3, 4),
             (4, 'p-share-numeraire', 1, 4), (4, 'p-share-numeraire', 3, 4), (4, 'p-share-numeraire', 5, 2), (4, 'p-ten-trades', 1, 4),
             (4, 'p-ten-trades', 2, 5), (4, 'p-ten-trades', 3, 2), (4, 'p-premium-weight', 1, 4), (4, 'p-premium-weight', 2, 4)]:
    typed(*args)

print(f'\n{nchk} checks, {len(fails)} failed')
for f_ in fails:
    print('  FAILED:', f_)
sys.exit(1 if fails else 0)
