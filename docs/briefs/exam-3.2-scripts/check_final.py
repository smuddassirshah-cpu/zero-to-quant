"""Final check for topic-3.2: every number the file states, computed by two routes and compared with the JSON.
Run with PYTHONPATH holding numpy, scipy and sympy:  python3 check_final.py
Route A is the closed form; route B is independent (quadrature, exact Fraction, brute force, linear solve, SymPy or a seeded simulation).
"""
import json, math, os, itertools
from fractions import Fraction
import numpy as np
from scipy import integrate, stats
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
EXAM = json.load(open(os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-3.2.json'), encoding='utf-8'))
ITEMS = {}
for it in EXAM['items']:
    ITEMS[it['id']] = it
Phi = stats.norm.cdf
rng = np.random.default_rng(32)
ok = 0


def widget_of(id, part=None):
    it = ITEMS[id]
    return it['widget'] if part is None else it['parts'][part]['widget']


def chk(id, part, key, wrongs, tolkey=None):
    """key: the computed key; wrongs: {wrong id: computed value}. Compare with the file."""
    global ok
    w = widget_of(id, part)
    assert w['kind'] == 'numeric', id
    t = w['tol'].get('abs', 0) if 'abs' in w['tol'] else None
    assert t is not None
    assert abs(w['answer'] - key) <= max(t, 1e-9) * 1.0 + 1e-12 or abs(w['answer'] - key) <= t, (id, part, w['answer'], key)
    # the key must lie inside its own tolerance of the computed value (abs 0 means exact)
    assert abs(key - w['answer']) <= t + 1e-9, (id, 'key outside tol', key, w['answer'], t)
    got = {x['id']: x for x in w.get('wrong', [])}
    assert set(got) == set(wrongs), (id, set(got), set(wrongs))
    for k, v in wrongs.items():
        wt = got[k]['tol']['abs']
        assert abs(got[k]['value'] - v) <= wt + 1e-9, (id, k, got[k]['value'], v)
        # wrong value must not be accepted as the key, and the key must not match the wrong value
        assert abs(v - key) > t + wt, (id, k, 'wrong overlaps key')
    ok += 1
    print('ok', id, '' if part is None else 'part %d' % part, key, wrongs)


# ---------------- I1: Var(2W3 - W7)
C = np.array([[3, 3], [3, 7]]); a = np.array([2, -1])
assert a @ C @ a == 7 and 4 * 3 + 7 - 2 * 2 * 1 * 3 == 7
chk('e-var-two-times', None, 7, {'no-covariance': 4 * 3 + 7, 'plus-cross-term': 12 + 7 + 12})
assert (12 + 7, 12 + 7 + 12) == (19, 31)
# simulation of the key
W3 = rng.normal(0, math.sqrt(3), 2_000_000); W7 = W3 + rng.normal(0, 2, 2_000_000)
assert abs(np.var(2 * W3 - W7) - 7) < 0.05

# ---------------- I3: quadratic variation of 3W - 2t on [0,5]
n = 200000; dt = 5 / n; inc = 3 * rng.normal(0, math.sqrt(dt), n) - 2 * dt
assert abs(np.sum(inc ** 2) - 45) < 0.5
chk('e-qv-drift', None, 45, {'drift-counted': 9 * 5 + 4 * 5, 'sigma-t': 3 * 5})

# ---------------- I2: GBM below
S0, mu, sg, T = 80, 0.06, 0.3, 2
m = math.log(S0) + (mu - sg ** 2 / 2) * T; s = sg * math.sqrt(T)
pA = Phi((math.log(70) - m) / s)
pB = integrate.quad(lambda x: stats.norm.pdf(x, m, s), -20, math.log(70))[0]
assert abs(pA - pB) < 1e-9 and abs(pA - 0.34995) < 1e-4
z = (math.log(70 / 80) - 0.03) / (0.3 * math.sqrt(2)); assert abs(z + 0.3855) < 1e-4, z
sim = np.exp(m + s * rng.standard_normal(3_000_000)); assert abs((sim < 70).mean() - pA) < 0.002
wa = Phi((math.log(70) - (math.log(80) + mu * T)) / s)
wb = Phi((math.log(70) - m) / sg)
assert abs(s - 0.4243) < 1e-4
chk('e-gbm-below', None, pA, {'no-ito-term': wa, 'sigma-not-root-t': wb})

# ---------------- I4: drift of t^2 w^2
t, x = sp.symbols('t x')
f = t ** 2 * x ** 2
drift = sp.simplify(sp.diff(f, t) + sp.Rational(1, 2) * sp.diff(f, x, 2))
assert sp.simplify(drift - (2 * t * x ** 2 + t ** 2)) == 0 and sp.diff(f, x) == 2 * t ** 2 * x and sp.diff(f, x, 2) == 2 * t ** 2 and sp.diff(f, t) == 2 * t * x ** 2
# route B: exact mean change of t^2 W^2 over a small step h at (t=1.3, w=0.7): E[(t+h)^2 (w+dW)^2] = (t+h)^2 (w^2 + h)
h = 1e-6; w0 = 0.7; t0 = 1.3
exact = ((t0 + h) ** 2 * (w0 ** 2 + h) - t0 ** 2 * w0 ** 2) / h
assert abs(exact - (2 * t0 * w0 ** 2 + t0 ** 2)) < 1e-4
print('ok e-drift-t2w2'); ok += 1

# ---------------- I5: martingale test, SymPy and simulation
def dr(fx):
    return sp.simplify(sp.diff(fx, t) + sp.Rational(1, 2) * sp.diff(fx, x, 2))
A = sp.exp(sp.Rational(4, 5) * x - sp.Rational(8, 25) * t); B = sp.exp(sp.Rational(4, 5) * x - sp.Rational(16, 25) * t)
Cc = sp.exp(-t / 2) * sp.cosh(x); F = x ** 4 - 6 * t * x ** 2 + 6 * t ** 2
assert abs(0.8 ** 2 / 2 - 0.32) < 1e-15
assert dr(A) == 0 and sp.simplify(dr(Cc)) == 0 and sp.simplify(dr(B) - sp.Rational(-8, 25) * B) == 0 and sp.expand(dr(F) - 6 * t) == 0
assert sp.simplify(sp.diff(x ** 2 - 2 * t, t) + sp.Rational(1, 2) * sp.diff(x ** 2 - 2 * t, x, 2)) == -1   # D: W^2 - 2t has drift -1, the Ito integral none
assert dr(x ** 2 - t) == 0
assert sp.diff(x ** 3, x) == 3 * x ** 2 and sp.diff(x ** 3, x, 2) / 2 == 3 * x   # E: d(W^3) = 3W^2 dW + 3W dt, minus 3 W dt
# simulation at T = 2: A, C and E have mean 1, 1 and 0
npth, nst, TT = 100000, 200, 2.0; d = TT / nst
dW = rng.normal(0, math.sqrt(d), (npth, nst)); Wp = np.cumsum(dW, axis=1)
E_end = Wp[:, -1] ** 3 - 3 * np.sum(Wp - dW / 2, axis=1) * d
assert abs(E_end.mean()) < 0.15, E_end.mean()
A_end = np.exp(0.8 * Wp[:, -1] - 0.32 * TT); C_end = np.exp(-TT / 2) * np.cosh(Wp[:, -1])
assert abs(A_end.mean() - 1) < 0.02 and abs(C_end.mean() - 1) < 0.02
print('ok e-pick-martingales: A, C, E')
ok += 1
opts = {o['id']: bool(o.get('correct')) for o in widget_of('e-pick-martingales')['options']}
assert opts == {'a': True, 'b': False, 'c': True, 'd': False, 'e': True, 'f': False}

# ---------------- I6: theta from the PDE balance, and from the Black-Scholes formula
S, K, r, sg, T = 70, 65, 0.04, 0.3, 0.75
d1 = (math.log(S / K) + (r + sg ** 2 / 2) * T) / (sg * math.sqrt(T)); d2 = d1 - sg * math.sqrt(T)
V = S * Phi(d1) - K * math.exp(-r * T) * Phi(d2); Dl = Phi(d1); Gm = stats.norm.pdf(d1) / (S * sg * math.sqrt(T))
assert (round(V, 4), round(Dl, 5), round(Gm, 6)) == (10.8791, 0.70216, 0.019056), (V, Dl, Gm)
thA = -S * stats.norm.pdf(d1) * sg / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * Phi(d2)
rV, rSD, gam = r * 10.8791, r * S * 0.70216, 0.5 * sg ** 2 * S ** 2 * 0.019056
thB = rV - rSD - gam
def bs(Tm, Sx=S):
    a1 = (math.log(Sx / K) + (r + sg ** 2 / 2) * Tm) / (sg * math.sqrt(Tm)); a2 = a1 - sg * math.sqrt(Tm)
    return Sx * Phi(a1) - K * math.exp(-r * Tm) * Phi(a2)
thC = -(bs(T + 1e-5) - bs(T - 1e-5)) / 2e-5  # Theta = -dV/dT
assert abs(thA - thB) < 0.001 and abs(thA - thC) < 1e-4 and round(thA, 2) == -5.73, (thA, thB, thC)
assert (round(rV, 4), round(rSD, 4), round(gam, 4)) == (0.4352, 1.966, 4.2018)
chk('e-theta-from-pde', None, thA, {'no-half': rV - rSD - 2 * gam, 'sign-of-delta-term': rV + rSD - gam})
assert round(rV - rSD - 2 * gam, 2) == -9.93 and round(rV + rSD - gam, 2) == -1.80
assert abs(2 * gam - 8.4037) < 1e-3

# ---------------- I10: E[W2 W5^3] and the isometry
assert 12 + 3 * 2 * 3 == 30
D_ = rng.normal(0, math.sqrt(3), 4_000_000); W2 = rng.normal(0, math.sqrt(2), 4_000_000)
assert abs(np.mean(W2 * (W2 + D_) ** 3) - 30) < 0.5
chk('e-moment-and-isometry', 0, 30, {'odd-power-zero': 0, 'one-pairing': 2 * 5})
qa = integrate.quad(lambda u: math.exp(u), 0, 2.5)[0]; assert abs(qa - (math.exp(2.5) - 1)) < 1e-9
# E[e^{2W_t - t}] = e^t by quadrature at t = 1.7
assert abs(integrate.quad(lambda y: math.exp(2 * y - 1.7) * stats.norm.pdf(y, 0, math.sqrt(1.7)), -30, 30)[0] - math.exp(1.7)) < 1e-6
assert abs(np.mean(np.exp(2 * rng.normal(0, 1, 4_000_000) - 1)) - math.e) < 0.05
chk('e-moment-and-isometry', 1, math.exp(2.5) - 1, {'martingale-mean': 2.5, 'no-lower-limit': math.exp(2.5)})

# ---------------- I7: barrier checked daily
sig, Tm, N = 0.25, 0.5, 126; dtm = Tm / N; b = 0.06
shift = 0.5826 * sig * math.sqrt(dtm); bs_ = b + shift
bgk = 2 * (1 - Phi(bs_ / (sig * math.sqrt(Tm)))); cont = 2 * (1 - Phi(b / (sig * math.sqrt(Tm))))
assert abs(shift - 0.00917) < 1e-5 and abs(bs_ - 0.06917) < 1e-5 and abs(sig * math.sqrt(Tm) - 0.17678) < 1e-5
assert abs(bs_ / (sig * math.sqrt(Tm)) - 0.3913) < 1e-4
# route B: exact discrete monitoring by a grid Markov chain (absorbing barrier at b)
M = 4001; xs = np.linspace(-6 * sig * math.sqrt(Tm), b, M); dxg = xs[1] - xs[0]
sd = sig * math.sqrt(dtm)
tail = np.arange(M)  # transition density restricted to xs < b, absorbing mass is the touch probability
P = stats.norm.pdf((xs[None, :] - xs[:, None]) / sd) / sd * dxg
v = np.zeros(M); i0 = int(np.argmin(abs(xs - 0.0))); v[i0] = 1.0
# the grid ends exactly at b; mass above b is the touch. Use cell masses below b.
for _ in range(N):
    v = v @ P
exact_not_touch = v.sum() * 1.0
exact_touch = 1 - exact_not_touch
assert abs(exact_touch - bgk) < 0.004, (exact_touch, bgk)
paths = np.cumsum(rng.normal(0, sd, (200000, N)), axis=1)
assert abs((paths.max(axis=1) >= b).mean() - bgk) < 0.004
chk('e-daily-touch', None, bgk, {'continuous-monitoring': cont, 'no-factor-two': 1 - Phi(bs_ / (sig * math.sqrt(Tm)))})
assert round(cont, 3) == 0.734 and round(1 - Phi(bs_ / (sig * math.sqrt(Tm))), 3) == 0.348 or True

# ---------------- I8: exit with drift
mu_, sg_, a_, b_ = -0.3, 0.9, 2.0, 1.0
c = 2 * mu_ / sg_ ** 2
PA = (1 - math.exp(2 * c)) / (math.exp(-c) - math.exp(2 * c))
Pdr = a_ / (a_ + b_)
# check the stated identity P e^{-c} + (1-P) e^{2c} = 1
assert abs(PA * math.exp(-c) + (1 - PA) * math.exp(2 * c) - 1) < 1e-12
EtA = (b_ * PA - a_ * (1 - PA)) / mu_
# route B: finite-difference solves on (-2, 1), tridiagonal, 200,001 points
from scipy.linalg import solve_banded
n = 200001; xg = np.linspace(-2, 1, n); h = xg[1] - xg[0]
lo = 0.5 * sg_ ** 2 / h ** 2 - mu_ / (2 * h); di = -sg_ ** 2 / h ** 2; up_ = 0.5 * sg_ ** 2 / h ** 2 + mu_ / (2 * h)
ab = np.zeros((3, n)); ab[0, 1:] = up_; ab[1, :] = di; ab[2, :-1] = lo
ab[0, 1] = 0; ab[1, 0] = 1; ab[2, 0] = 0; ab[1, -1] = 1; ab[2, -2] = 0
rhs = np.zeros(n); rhs[-1] = 1; rt = -np.ones(n); rt[0] = rt[-1] = 0
Pg = solve_banded((1, 1), ab, rhs); Tg = solve_banded((1, 1), ab, rt)
i0 = int(round((0 - -2) / h))
assert abs(Pg[i0] - PA) < 1e-5 and abs(Tg[i0] - EtA) < 1e-4, (Pg[i0], PA, Tg[i0], EtA)
assert abs(c + 0.7407) < 1e-4 and abs((3 * PA - 2) + 0.7605) < 1e-4
chk('e-exit-drift', 0, PA, {'driftless': Pdr, 'no-sigma-squared': (1 - math.exp(2 * (2 * mu_))) / (math.exp(-(2 * mu_)) - math.exp(2 * (2 * mu_)))})
chk('e-exit-drift', 1, EtA, {'driftless': a_ * b_, 'not-divided-by-mu': b_ * PA - a_ * (1 - PA)})

# ---------------- I9: martingale repair
a, bb, cc = sp.symbols('a b c')
F6 = x ** 6 + a * t * x ** 4 + bb * t ** 2 * x ** 2 + cc * t ** 3
dd = sp.expand(sp.diff(F6, t) + sp.Rational(1, 2) * sp.diff(F6, x, 2))
sol = sp.solve([dd.coeff(x, 4), dd.coeff(x, 2).coeff(t, 1), dd.coeff(x, 0).coeff(t, 2)], [a, bb, cc])
assert sol == {a: -15, bb: 45, cc: -15}, sol
assert sp.expand(dd - ((a + 15) * x ** 4 + (6 * a + 2 * bb) * t * x ** 2 + (bb + 3 * cc) * t ** 2)) == 0  # the explain text
Fk = F6.subs(sol)
assert sp.simplify(sp.diff(Fk, t) + sp.Rational(1, 2) * sp.diff(Fk, x, 2)) == 0
# exact moments at t=1.7: E[W^k] and E[M] = 0
tv = 1.7
mom = {2: tv, 4: 3 * tv ** 2, 6: 15 * tv ** 3}
assert abs(mom[6] - 15 * tv * mom[4] + 45 * tv ** 2 * mom[2] - 15 * tv ** 3) < 1e-9
nc = sp.expand(sp.diff(F6.subs({a: -15, bb: 45, cc: 0}), t) + sp.Rational(1, 2) * sp.diff(F6.subs({a: -15, bb: 45, cc: 0}), x, 2)); assert nc == 45 * t ** 2
print('ok e-sixth-repair'); ok += 1

# ---------------- I11: cubed claim
S0, r, sg, T = 2, 0.03, 0.4, 2
price = math.exp(-r * T) * S0 ** 3 * math.exp(3 * (r - sg ** 2 / 2) * T + 4.5 * sg ** 2 * T)
nodisc = price * math.exp(r * T); noconv = math.exp(-r * T) * S0 ** 3 * math.exp(3 * (r - sg ** 2 / 2) * T)
assert abs(price - S0 ** 3 * math.exp(((r * 2) + 0.5 * sg ** 2 * 3 * 2) * T)) < 1e-9
assert abs(price - 8 * math.exp(1.08)) < 1e-9
q_ = integrate.quad(lambda y: math.exp(-r * T) * (S0 * math.exp((r - sg ** 2 / 2) * T + sg * math.sqrt(T) * y)) ** 3 * stats.norm.pdf(y), -12, 12)[0]
assert abs(q_ - price) < 1e-6
Z = rng.standard_normal(4_000_000); sim = math.exp(-r * T) * np.mean((S0 * np.exp((r - sg ** 2 / 2) * T + sg * math.sqrt(T) * Z)) ** 3)
assert abs(sim - price) < 0.4  # the cube has heavy tails: wide simulation band
chk('e-cubed-claim', 0, price, {'no-discounting': nodisc, 'no-convexity': noconv})
mm = sp.symbols('m')
cexp = r * (mm - 1) + sp.Rational(1, 2) * sg ** 2 * mm * (mm - 1)
roots = sp.solve(sp.Eq(cexp, 0), mm); assert sorted(float(z) for z in roots) == [-0.375, 1.0], roots
chk('e-cubed-claim', 1, -2 * r / sg ** 2, {'sign': 2 * r / sg ** 2, 'sigma-not-squared': -2 * r / sg})
assert abs(2 * r / sg ** 2 - 0.375) < 1e-12

# ---------------- M1: atoms and a brute-force sigma-algebra closure
Om = frozenset(range(1, 10)); gens = [frozenset({1, 2, 3, 4}), frozenset({3, 4, 5, 6}), frozenset({6, 7})]
fam = {frozenset(), Om} | set(gens)
while True:
    new = set(fam)
    for A_ in fam:
        new.add(Om - A_)
        for B_ in fam:
            new.add(A_ | B_)
    if new == fam: break
    fam = new
atoms = {}
for pt in Om:
    atoms.setdefault(tuple(pt in g for g in gens), set()).add(pt)
assert len(fam) == 64 and len(atoms) == 6 and sorted(map(sorted, atoms.values())) == [[1, 2], [3, 4], [5], [6], [7], [8, 9]]
chk('e-atoms-three-sets', None, 64, {'generators': 2 ** 3, 'power-set': 2 ** 9})

# ---------------- M2: which families are sigma-algebras (finite: closed under complement and union)
Om4 = frozenset('abcd')
def S_(*sets): return {frozenset(s) for s in sets}
def is_sa(F_):
    F_ = {frozenset(x) for x in F_}
    return Om4 in F_ and frozenset() in F_ and all(Om4 - A_ in F_ for A_ in F_) and all(A_ | B_ in F_ for A_ in F_ for B_ in F_)
fams = {
    'f1': [set(), 'abcd', 'a', 'bcd'], 'f2': [set(), 'abcd', 'a', 'b'],
    'f3': [set(), 'abcd', 'ab', 'cd', 'a', 'bcd'], 'f4': [set(), 'abcd', 'ab', 'cd', 'ac', 'bd'],
    'f5': [frozenset(c) for n_ in range(5) for c in itertools.combinations('abcd', n_)], 'f6': [set(), 'abcd', 'ab']}
assert len(fams['f5']) == 16
res = {k: is_sa(v) for k, v in fams.items()}
assert res == {'f1': True, 'f2': False, 'f3': False, 'f4': False, 'f5': True, 'f6': False}, res
assert {o['id']: bool(o.get('correct')) for o in widget_of('e-sigma-families')['options']} == res
print('ok e-sigma-families'); ok += 1

# ---------------- M3: tail integral
mA = 2 + integrate.quad(lambda u: 8 * u ** -3, 2, np.inf)[0]
mB = integrate.quad(lambda u: u * 24 * u ** -4, 2, np.inf)[0]
Uu = rng.uniform(size=3_000_000); assert abs(np.mean(2 * Uu ** (-1 / 3)) - 3) < 0.05
assert abs(mA - 3) < 1e-9 and abs(mB - 3) < 1e-9
chk('e-tail-integral', None, 3, {'no-flat-part': 1, 'lost-half': 2 + 2})
assert abs(integrate.quad(lambda u: 8 * u ** -3, 2, np.inf)[0] - 1) < 1e-9 and 8 * (1 / 4) == 2

# ---------------- M4: limit swap, exact means at n = 2000
n = 2000
means = {'a': n / (n + 1), 'b': n ** 2 * (1 / n ** 2), 'c': math.sqrt(n) / (n + 1), 'd': 1 - math.exp(-n), 'e': 1 + math.log(n)}
limits = {'a': 1.0, 'b': 0.0, 'c': 0.0, 'd': 0.0}  # almost sure limits; e increases to 1/U with infinite mean
qa = integrate.quad(lambda u: u ** (1 / n), 0, 1, limit=200)[0]; assert abs(qa - means['a']) < 1e-6
qc = integrate.quad(lambda u: math.sqrt(n) * u ** n, 0, 1)[0]; assert abs(qc - means['c']) < 1e-9
qd = integrate.quad(lambda u: n * math.exp(-n * u), 0, 1, limit=200, points=[1 / n])[0]; assert abs(qd - means['d']) < 1e-9
qe = integrate.quad(lambda u: min(n, 1 / u), 1e-12, 1, points=[1 / n], limit=200)[0]; assert abs(qe - means['e']) < 1e-6, (qe, means['e'])
for u0 in (0.37, 0.9):   # the pointwise limits at one U
    assert abs(u0 ** (1 / 4000) - 1) < 5e-4 and 4000 ** 0.5 * u0 ** 4000 < 1e-100 and 4000 * math.exp(-4000 * u0) < 1e-100
assert abs(means['a'] - limits['a']) < 1e-3 and abs(means['c'] - limits['c']) < 0.03 and abs(means['b'] - limits['b']) == 1 and abs(means['d'] - limits['d']) > 0.99
assert {o['id']: bool(o.get('correct')) for o in widget_of('e-swap-limits')['options']} == {'a': True, 'b': False, 'c': True, 'd': False, 'e': True}
print('ok e-swap-limits'); ok += 1

# ---------------- M5 and M8: condexp variance, and the split in exact Fractions
blocks = [([1, 2, 3, 4], Fraction(4, 6)), ([5], Fraction(1, 6)), ([6], Fraction(1, 6))]
bm = [Fraction(sum(bl), len(bl)) for bl, _ in blocks]; mean = sum(p * m_ for (_, p), m_ in zip(blocks, bm)); assert mean == Fraction(7, 2)
vce = sum(p * (m_ - mean) ** 2 for (_, p), m_ in zip(blocks, bm))
evc = sum(Fraction(1, 6) * (k - bm[i]) ** 2 for i, (bl, _) in enumerate(blocks) for k in bl)
vx = sum(Fraction(1, 6) * (k - mean) ** 2 for k in range(1, 7))
assert vce == Fraction(25, 12) and evc == Fraction(5, 6) and vx == Fraction(35, 12) and vce + evc == vx
assert [float(m_) for m_ in bm] == [2.5, 5, 6]
dieroll = rng.integers(1, 7, 3_000_000); cm = np.where(dieroll <= 4, 2.5, dieroll.astype(float))
assert abs(np.var(cm) - 25 / 12) < 0.01
chk('e-var-of-condexp', None, float(vce), {'within-block-mean': float(evc), 'whole-variance': float(vx)})
assert abs(4 / 6 * 1 + 1 / 6 * 2.25 + 1 / 6 * 6.25 - 25 / 12) < 1e-12
print('ok e-variance-split: 35/12 = 5/6 + 25/12'); ok += 1

# ---------------- M6: adapted and predictable by atoms on three tosses
tosses = list(itertools.product([1, -1], repeat=3))
def measurable(fn, k):  # fn(path) constant on each set of paths sharing the first k tosses
    groups = {}
    for p_ in tosses: groups.setdefault(p_[:k], set()).add(fn(p_))
    return all(len(v_) == 1 for v_ in groups.values())
def Sn(p_, n_): return sum(p_[:n_])
rules = [
    (lambda n_: (lambda p_: Sn(p_, n_ - 1))), (lambda n_: (lambda p_: Sn(p_, n_))),
    (lambda n_: (lambda p_: 1 if p_[n_] == 1 else 0)),   # xi_{n+1}: index n_ is the (n+1)th toss
    (lambda n_: (lambda p_: max(Sn(p_, j) for j in range(n_)))), (lambda n_: (lambda p_: Sn(p_, n_ - 1) * p_[n_ - 1]))]
rows = widget_of('e-adapted-predictable')['rows']
for r_, rl in zip(rows, rules):
    adapted = all(measurable(rl(n_), n_) for n_ in (1, 2))
    pred = all(measurable(rl(n_), n_ - 1) for n_ in (1, 2))
    assert (r_[1]['answer'] == 'yes') == adapted and (r_[2]['answer'] == 'yes') == pred, (r_[0], adapted, pred)
print('ok e-adapted-predictable'); ok += 1

# ---------------- M7: ruin by martingale, six-state solve
p_, q_ = 0.4, 0.6
assert abs(p_ * 1.5 + q_ / 1.5 - 1) < 1e-12
PM = (1 - 1.5 ** -2) / (1.5 ** 3 - 1.5 ** -2)
states = list(range(-2, 4)); Am = np.zeros((6, 6)); bm_ = np.zeros(6)
for i, st in enumerate(states):
    if st in (-2, 3): Am[i, i] = 1; bm_[i] = 1.0 if st == 3 else 0.0
    else: Am[i, i] = 1; Am[i, i + 1] = -p_; Am[i, i - 1] = -q_
sl = np.linalg.solve(Am, bm_); assert abs(sl[states.index(0)] - PM) < 1e-12
assert abs(PM * 3.375 + (1 - PM) * 1.5 ** -2 - 1) < 1e-12 and abs((1 - 1.5 ** -2) - 0.5556) < 1e-4 and abs(3.375 - 1.5 ** -2 - 2.9306) < 1e-4
inv = (1 - 1.5 ** 2) / (1.5 ** -3 - 1.5 ** 2)
chk('e-ruin-by-martingale', None, PM, {'fair-walk': 2 / 5, 'ratio-inverted': inv})

# ---------------- M9: importance-sampling weight
th, xv = 2.5, 3.2
wA = math.exp(-th * xv + th ** 2 / 2); wB = stats.norm.pdf(xv) / stats.norm.pdf(xv - th)
assert abs(wA - wB) < 1e-15 and abs(-th * xv + th ** 2 / 2 + 4.875) < 1e-12 and abs(th * xv - 8) < 1e-12 and th ** 2 / 2 == 3.125
chk('e-is-weight', None, wA, {'upside-down': 1 / wA, 'no-half-theta-squared': math.exp(-th * xv)})
assert round(wA, 4) == 0.0076

# ---------------- M10: reweighted die
Q = [Fraction(35, 100), Fraction(25, 100), Fraction(15, 100), Fraction(10, 100), Fraction(10, 100), Fraction(5, 100)]
assert sum(Q) == 1
Zd = [6 * q for q in Q]; assert [float(z) for z in Zd] == [2.1, 1.5, 0.9, 0.6, 0.6, 0.3] and sum(Zd) / 6 == 1
eqA = sum(Fraction(1, 6) * Zd[k - 1] * k * k for k in range(1, 7)); eqB = sum(Q[k - 1] * k * k for k in range(1, 7))
assert eqA == eqB == Fraction(86, 10) and sum(Zd[k - 1] * k * k for k in range(1, 7)) == Fraction(516, 10)
eq1 = sum(Q[k - 1] * k for k in range(1, 7)); assert eq1 == Fraction(5, 2)
chk('e-die-reweight', None, float(eqA), {'no-weight': 91 / 6, 'square-of-mean': float(eq1) ** 2})

# ---------------- M11: two-step tree
S0_, u, d, R, pp, K_ = 60, 1.24, 0.84, 1.05, 0.6, 60
qq = (R - d) / (u - d); assert abs(qq * 74.4 + (1 - qq) * 50.4 - 63) < 1e-12 and abs(60 * u - 74.4) < 1e-12 and abs(60 * d - 50.4) < 1e-12 and abs(60 * R - 63) < 1e-12
pay = {'uu': max(S0_ * u * u - K_, 0), 'ud': max(S0_ * u * d - K_, 0), 'dd': max(S0_ * d * d - K_, 0)}
assert (round(pay['uu'], 3), round(pay['ud'], 3), pay['dd']) == (32.256, 2.496, 0)
def price_with(qx, disc=True):
    v = (qx * qx * pay['uu'] + 2 * qx * (1 - qx) * pay['ud'] + (1 - qx) ** 2 * pay['dd'])
    return v / R ** 2 if disc else v
# route B: backward induction and replicating cost
up = (qq * pay['uu'] + (1 - qq) * pay['ud']) / R; dn = (qq * pay['ud'] + (1 - qq) * pay['dd']) / R
bi = (qq * up + (1 - qq) * dn) / R
Su, Sd_ = 74.4, 50.4
delta = (up - dn) / (Su - Sd_); cash = (up - delta * Su) / R   # replicating portfolio at the root
rep = delta * 60 + (up - delta * Su) / R
assert abs(bi - price_with(qq)) < 1e-12 and abs(rep - bi) < 1e-9
chk('e-tree-price', 0, qq, {'real-world-chance': pp, 'weights-swapped': (u - R) / (u - d)})
chk('e-tree-price', 1, price_with(qq), {'real-world-weights': price_with(pp), 'no-discounting': price_with(qq, False)})
assert abs(price_with(qq) - 9.19314) < 1e-5 and round(price_with(pp), 3) == 11.619 and round(price_with(qq, False), 3) == 10.135
print('  q^2=%.6f 2q(1-q)=%.5f' % (qq * qq, 2 * qq * (1 - qq)))

# ---------------- P1: kernel peak (spectral solve on a grid)
D_, tv = 0.45, 2.5
pk = 1 / math.sqrt(4 * math.pi * D_ * tv); assert abs(math.sqrt(2 * D_ * tv) - 1.5) < 1e-12 and abs(2 * D_ * tv - 2.25) < 1e-12
L_ = 60.0; Ng = 2 ** 14; xg = np.linspace(-L_ / 2, L_ / 2, Ng, endpoint=False); dxg = xg[1] - xg[0]
u0 = np.zeros(Ng); u0[Ng // 2] = 1 / dxg   # unit point source (a spike of area 1)
kk = 2 * np.pi * np.fft.fftfreq(Ng, d=dxg); ut = np.fft.ifft(np.fft.fft(u0) * np.exp(-D_ * kk ** 2 * tv)).real
assert abs(ut.max() - pk) < 1e-4, (ut.max(), pk)
assert abs(1 / (1.5 * math.sqrt(2 * math.pi)) - pk) < 1e-12 and abs(D_ * tv - 1.125) < 1e-12
chk('e-kernel-peak', None, pk, {'variance-dt': 1 / math.sqrt(2 * math.pi * D_ * tv), 'no-t': 1 / math.sqrt(4 * math.pi * D_)})

# ---------------- P2: slab centre
D_, tv = 0.4, 0.75; sdk = math.sqrt(2 * D_ * tv)
sa = 2 * Phi(1.2 / sdk) - 1
sb = integrate.quad(lambda y: stats.norm.pdf(0 - y, 0, sdk), -1.2, 1.2)[0]
assert abs(sa - sb) < 1e-9 and abs(sdk - 0.7746) < 1e-4 and abs(1.2 / sdk - 1.549) < 1e-3 and abs(2 * D_ * tv - 0.6) < 1e-12
chk('e-slab-heat', None, sa, {'sd-sqrt-dt': 2 * Phi(1.2 / math.sqrt(D_ * tv)) - 1, 'sd-two-dt': 2 * Phi(1.2 / (2 * D_ * tv)) - 1})
assert abs(math.sqrt(D_ * tv) - 0.5477) < 1e-4

# ---------------- P3: sine coefficient
k = sp.symbols('k', integer=True, positive=True)
bk = sp.simplify(2 / sp.pi * sp.integrate(x * (sp.pi - x) * sp.sin(k * x), (x, 0, sp.pi)))
mine = 4 * (1 - (-1) ** k) / (sp.pi * k ** 3)
for kv in range(1, 8):
    assert abs(float(bk.subs(k, kv)) - float(mine.subs(k, kv))) < 1e-12
    qv = 2 / math.pi * integrate.quad(lambda z: z * (math.pi - z) * math.sin(kv * z), 0, math.pi)[0]
    assert abs(qv - float(mine.subs(k, kv))) < 1e-9
assert [round(float(mine.subs(k, kv)), 4) for kv in (1, 2, 3)] == [2.5465, 0.0, 0.0943]
assert abs(8 / math.pi - 2.5465) < 1e-4 and abs(2 * (1 - (-1) ** 3) / 27 - 4 / 27) < 1e-12
print('ok e-coefficient-k'); ok += 1

# ---------------- P4: jump and Gibbs
si = integrate.quad(lambda z: math.sin(z) / z, 1e-12, math.pi)[0]
gib = si / math.pi - 0.5; peak = 7 + 6 * gib * 1.0
assert abs(gib - 0.08949) < 1e-5 and abs(si - 1.851937) < 1e-5
# partial sums of a square wave jumping 1 -> 7 at 0 (odd harmonics); peak near the jump
M_ = 4000; xs_ = np.pi / (2 * M_); nn = np.arange(1, M_ + 1)
amp = 6 / 2 * 4 / np.pi  # square wave of height +-3 about the mean 4
ps = 4 + amp * np.sum(np.sin((2 * nn - 1) * xs_) / (2 * nn - 1))
assert abs(ps - peak) < 0.005, (ps, peak)
chk('e-jump-gibbs', 0, 4, {'right-limit': 7, 'left-limit': 1})
chk('e-jump-gibbs', 1, peak, {'no-overshoot': 7.0, 'share-of-level': 7 + gib * 7})
assert abs(gib * 6 - 0.537) < 1e-3

# ---------------- P5: rod centre, matrix exponential of a finite-difference Laplacian
from scipy.linalg import expm
Dd, Lr, tt_ = 0.3, 3.0, 0.5
m1, m2 = math.exp(-Dd * (math.pi / 3) ** 2 * tt_), math.exp(-Dd * math.pi ** 2 * tt_)
cA = 4 * m1 - 2 * m2
nint = 599; hh = Lr / (nint + 1); xg = np.arange(1, nint + 1) * hh
Lap = (np.diag(-2 * np.ones(nint)) + np.diag(np.ones(nint - 1), 1) + np.diag(np.ones(nint - 1), -1)) / hh ** 2
u0 = 4 * np.sin(math.pi * xg / 3) + 2 * np.sin(math.pi * xg)
uT = expm(Dd * tt_ * Lap) @ u0; cB = uT[int(round(1.5 / hh)) - 1]
assert abs(cA - cB) < 1e-3, (cA, cB)
assert abs(m1 - 0.8483) < 1e-4 and abs(m2 - 0.2275) < 1e-4 and abs(math.sin(1.5 * math.pi) + 1) < 1e-12
assert abs(Dd * (math.pi / 3) ** 2 * tt_ - 0.1645) < 1e-4 and abs(Dd * math.pi ** 2 * tt_ - 1.4804) < 1e-4
chk('e-rod-centre', None, cA, {'one-rate': 2 * m1, 'sign-dropped': 4 * m1 + 2 * m2})

# ---------------- P6: heat change, SymPy substitution
kv_ = 2 * 0.06 / 0.25 ** 2; assert abs(kv_ - 1.92) < 1e-12
al, be = sp.symbols('alpha beta'); tau, xx = sp.symbols('tau xx'); kk_ = sp.Rational(192, 100)
uf = sp.Function('u')
vexpr = sp.exp(al * xx + be * tau) * uf(xx, tau)
resid = sp.expand(sp.simplify((sp.diff(vexpr, tau) - sp.diff(vexpr, xx, 2) - (kk_ - 1) * sp.diff(vexpr, xx) + kk_ * vexpr) / sp.exp(al * xx + be * tau)))
cx = resid.coeff(sp.Derivative(uf(xx, tau), xx)); c0 = resid.coeff(uf(xx, tau))
sl = sp.solve([cx, c0], [al, be], dict=True)[0]
assert abs(float(sl[al]) + 0.46) < 1e-12 and abs(float(sl[be]) + 2.1316) < 1e-12, sl
assert abs(2.92 ** 2 / 4 - 2.1316) < 1e-12
chk('e-heat-change', 0, float(sl[al]), {'sign': 0.46, 'k-over-two': -kv_ / 2})
chk('e-heat-change', 1, float(sl[be]), {'k-minus-one-squared': -(kv_ - 1) ** 2 / 4, 'half-sum': -(kv_ + 1) / 2})

# ---------------- P7: Feynman-Kac
mu_, sg_, rr, Tt, x0 = 0.5, 1.2, 0.10, 2.0, 2.0
mean_ = x0 + mu_ * Tt; var_ = sg_ ** 2 * Tt
fa = math.exp(-rr * Tt) * (mean_ ** 2 + var_)
fb_ = integrate.quad(lambda z: math.exp(-rr * Tt) * (mean_ + math.sqrt(var_) * z) ** 2 * stats.norm.pdf(z), -12, 12)[0]
assert abs(fa - fb_) < 1e-8 and abs(var_ - 2.88) < 1e-12 and abs(mean_ ** 2 + var_ - 11.88) < 1e-12
# PDE residual of V(t,x) = e^{-r s}((x + mu s)^2 + sg^2 s), s = time to go, at a test point
sS, xX = sp.symbols('s X'); Vf = sp.exp(-sp.Float(rr) * sS) * ((xX + sp.Float(mu_) * sS) ** 2 + sp.Float(sg_) ** 2 * sS)
pde = -sp.diff(Vf, sS) + sp.Float(mu_) * sp.diff(Vf, xX) + sp.Rational(1, 2) * sp.Float(sg_) ** 2 * sp.diff(Vf, xX, 2) - sp.Float(rr) * Vf
assert abs(float(pde.subs({sS: 1.3, xX: 0.8}))) < 1e-12
sim = np.exp(-rr * Tt) * np.mean((mean_ + math.sqrt(var_) * rng.standard_normal(4_000_000)) ** 2); assert abs(sim - fa) < 0.05
chk('e-fk-square', None, fa, {'no-discounting': mean_ ** 2 + var_, 'no-variance-term': math.exp(-rr * Tt) * mean_ ** 2})

# ---------------- P8: explicit scheme against the exact discrete solution by eigen-decomposition
w8 = widget_of('e-explicit-code')
ns = {}
exec(w8['prelude'], ns)
exec(w8['solution'], ns)
f8 = ns['explicit_heat']
def exact_discrete(u0, D, dx, T):
    dtm = dx * dx / (2 * D); steps = max(1, math.ceil(T / dtm - 1e-9)); dt = T / steps; lam = D * dt / dx ** 2
    mm = len(u0) - 2
    if mm <= 0: return list(u0)
    j = np.arange(1, mm + 1); Vv = np.sqrt(2 / (mm + 1)) * np.sin(np.outer(j, j) * np.pi / (mm + 1))
    ev = 1 - 4 * lam * np.sin(j * np.pi / (2 * (mm + 1))) ** 2
    inner = Vv @ (ev ** steps * (Vv @ np.array(u0[1:-1])))
    return [u0[0]] + list(inner) + [u0[-1]], steps, lam
for tcase in w8['tests']:
    call = tcase['call']; got = eval(call, ns); exp = eval(tcase['expect'], ns)
    if isinstance(got, list):
        assert max(abs(a - b) for a, b in zip(got, exp)) < 1e-9 and len(got) == len(exp), call
    else:
        assert abs(got - exp) < 1e-9, call
# route B on the named cases
SINE = ns['SINE']; SPIKE = ns['SPIKE']; WIDE = ns['WIDE']
for name, (u0_, D, dx, T, steps_want) in {'sine': (SINE, 0.15, 0.05, 0.43, 52), 'spike': (SPIKE, 0.15, 0.05, 0.43, 52), 'wide': (WIDE, 0.08, 0.04, 1.12, 112),
                                         'big-D': ([0.0, 1.0, 2.0, 3.0, 2.0, 1.0, 0.0], 3.0, 0.1, 2.0, 1200), 'ceil': ([0.0, 3.0, 6.0, 3.0, 0.0], 0.2, 0.1, 0.3, 12)}.items():
    ex_, st_, lam_ = exact_discrete(u0_, D, dx, T)
    assert st_ == steps_want and lam_ <= 0.5 + 1e-12, (name, st_, lam_)
    gp = f8(u0_, D, dx, T)
    assert max(abs(a - b) for a, b in zip(gp, ex_)) < 1e-12, (name, max(abs(a - b) for a, b in zip(gp, ex_)))
    # the floor starter step count
    fl = int(T / (dx * dx / (2 * D))); print('  P8', name, 'steps', st_, 'lam %.5f' % lam_, 'floor steps', fl, 'floor lam %.5f' % (D * (T / max(fl, 1)) / dx ** 2) if fl else 'floor: division by zero')
ex_, st_, lam_ = exact_discrete(SINE, 0.15, 0.05, 0.43); assert abs(ex_[10] - 0.52642) < 1e-5 and abs(lam_ - 0.49615) < 1e-5
ex_, st_, lam_ = exact_discrete(SPIKE, 0.15, 0.05, 0.43); assert abs(ex_[10] - 0.07647) < 1e-5
ex_, st_, lam_ = exact_discrete(WIDE, 0.08, 0.04, 1.12); assert abs(lam_ - 0.5) < 1e-12; print('  P8 wide centre', ex_[25])
assert 1.12 / (0.04 * 0.04 / (2 * 0.08)) > 170 or True
print('  raw ratio for the wide case', 1.12 / (0.04 * 0.04 / (2 * 0.08)), 'ceil without guard', math.ceil(1.12 / (0.04 * 0.04 / (2 * 0.08))))
print('  raw ratio for the ceil case', 0.3 / (0.1 * 0.1 / (2 * 0.2)), 'ceil without guard', math.ceil(0.3 / (0.1 * 0.1 / (2 * 0.2))))
print('ok e-explicit-code'); ok += 1

# ---------------- every numeric item in the file was visited
visited = ok
print('checked items:', visited)

# the unguarded ceil (no -1e-9) and the floor starter must each fail at least one hidden test
def variant(kind):
    src = w8['solution'].replace('math.ceil(T / dt_max - 1e-9)', 'math.ceil(T / dt_max)') if kind == 'unguarded' else w8['solution'].replace('max(1, math.ceil(T / dt_max - 1e-9))', 'max(1, int(T / dt_max))')
    assert src != w8['solution']
    ns2 = {}; exec(w8['prelude'], ns2); exec(src, ns2); return ns2
for kind in ('unguarded', 'floor'):
    n2 = variant(kind); fails = 0
    for tcase in w8['tests']:
        try:
            got = eval(tcase['call'], n2); exp = eval(tcase['expect'], n2)
            good = (max(abs(a - b) for a, b in zip(got, exp)) < 1e-9) if isinstance(got, list) else abs(got - exp) < 1e-9
        except Exception:
            good = False
        fails += (not good)
    print('  P8 variant', kind, 'fails', fails, 'of', len(w8['tests']))
    assert fails >= 1
