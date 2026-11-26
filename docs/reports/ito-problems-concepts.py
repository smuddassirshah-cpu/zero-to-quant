#!/usr/bin/env python3
"""Blind concept audit, ito problems-1 to problems-4: recompute every key and slip,
and simulate each SDE or path claim. Exits 0 when every check passes.
Run from anywhere: python docs/reports/ito-problems-concepts.py"""
import json, math, os, sys
import numpy as np
from scipy.stats import norm, binom

HERE = os.path.dirname(os.path.abspath(__file__))
CDIR = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'ito')
rng = np.random.default_rng(20261126)
fails = []
nchk = 0
E, L, S, Phi = math.exp, math.log, math.sqrt, norm.cdf


def chk(name, ok, detail=''):
    global nchk
    nchk += 1
    if not ok:
        fails.append(name)
    print(('ok   ' if ok else 'FAIL ') + name + (' | ' + detail if detail else ''))


def near(name, got, want, tol):
    chk(name, abs(got - want) <= tol, f'got {got:.6g}, content {want:.6g}, tol {tol:g}')


SETS = {n: json.load(open(os.path.join(CDIR, f'problems-{n}.json'))) for n in (1, 2, 3, 4)}


def part(n, item, k):
    it = [i for i in SETS[n]['items'] if i['id'] == item][0]
    return it['parts'][k - 1]


def keys(n, item, k, answer, slips):
    """The answer and each named slip, recomputed here, must sit inside the content's own band."""
    w = part(n, item, k)['widget']
    tag = f'p{n} {item} part {k}'
    if 'answers' in w:
        got = sorted(w['answers'])
        chk(tag + ' keys', all(abs(a - b) <= w['tol']['abs'] for a, b in zip(got, sorted(answer))), str(got))
    else:
        near(tag + ' key', answer, w['answer'], max(w['tol']['abs'], 1e-9))
    wr = {x['id']: x for x in w.get('wrong', [])}
    by = set(part(n, item, k)['feedback'].get('byKey', {}))
    chk(tag + ' slip ids', set(wr) == set(slips) and set(wr) <= by | set(wr) and by >= set(wr), f'{sorted(wr)} vs {sorted(slips)}')
    for sid, val in slips.items():
        if sid not in wr:
            continue
        x = wr[sid]
        if isinstance(val, (list, tuple)):
            got = sorted(float(v) for v in x['value'].split(','))
            chk(tag + ' slip ' + sid, all(abs(a - b) <= x['tol']['abs'] for a, b in zip(got, sorted(val))), str(got))
        else:
            near(tag + ' slip ' + sid, val, x['value'], max(x['tol']['abs'], 1e-9))
            if 'answer' in w:  # a slip must never be graded correct
                chk(tag + ' slip ' + sid + ' outside key band', abs(x['value'] - w['answer']) > w['tol']['abs'])


# ------------------------------------------------------------------ problems-1
p, q, n, g = 0.507, 0.493, 625, 40
keys(1, 'p-maker-tally', 1, n * g * (p - q), {'wins-only': n * g * p, 'half-edge': n * g * (p - q) / 2, 'per-trade-count': n * (p - q)})
dayvar = n * (g * g - (g * (p - q)) ** 2)
keys(1, 'p-maker-tally', 2, n * g * g, {'variance': dayvar, 'abs-sum': n * g})
sd5 = S(5 * 1e6)
keys(1, 'p-maker-tally', 3, sd5, {'sd-times-t': 5000, 'one-day': 1000})
keys(1, 'p-maker-tally', 4, Phi(-1750 / sd5), {'sd-times-t': Phi(-1750 / 5000), 'no-drift': 0.5, 'ends-up': Phi(1750 / sd5), 'one-day': Phi(-1.75)})
# exact walk: a week of 3125 trades loses when wins <= 1562
exact = binom.cdf(1562, 5 * n, p)
chk('p1 maker-tally: exact binomial chance of a losing week is near the diffusion 0.2169', abs(exact - Phi(-1750 / sd5)) < 0.01, f'exact {exact:.4f}')
chk('p1 maker-tally: QV-based sigma^2 = 1,000,000 and the walk variance 999,804 agree inside the key bands',
    abs(S(5 * dayvar) - sd5) < 0.5 and abs(Phi(-1750 / S(5 * dayvar)) - Phi(-1750 / sd5)) < 0.0005, f'sd {S(5*dayvar):.2f} vs {sd5:.2f}')

mu, sg, S0, Sq, tau = 0.13, 0.35, 45, 52, 0.75
sdl = sg * S(tau)
keys(1, 'p-quarter-rally', 1, sdl, {'full-year': sg, 'variance': sg * sg * tau, 'past-quarter': sg * S(0.25)})
ld = (mu - sg * sg / 2) * tau
med = Sq * E(ld)
keys(1, 'p-quarter-rally', 2, med, {'mean': Sq * E(mu * tau), 'from-start': S0 * E(mu - sg * sg / 2), 'whole-year': Sq * E(mu - sg * sg / 2)})
keys(1, 'p-quarter-rally', 3, Sq * E(mu * tau), {'median': med, 'full-factor': med * E(sg * sg * tau), 'full-year': Sq * E(mu)})
z = (L(45 / 52) - ld) / sdl
keys(1, 'p-quarter-rally', 4, Phi(z), {'full-year-sd': Phi((L(45 / 52) - ld) / sg), 'no-rally': Phi(-(mu - sg * sg / 2) / sg), 'upper': 1 - Phi(z)})
N, m = 400000, 300
s = np.full(N, 52.0)
dt = tau / m
for _ in range(m):
    s += mu * s * dt + sg * s * S(dt) * rng.standard_normal(N)
se = s.std() / S(N)
chk('p1 quarter-rally EM: mean of S_1 given 52 is 57.33', abs(s.mean() - Sq * E(mu * tau)) < 4 * se, f'{s.mean():.3f} se {se:.3f}')
chk('p1 quarter-rally EM: median of S_1 given 52 is 54.75', abs(np.median(s) - med) < 0.15, f'{np.median(s):.3f}')
pb = (s < 45).mean()
chk('p1 quarter-rally EM: P(S_1<45) is 0.2588, not 0.2876 or 0.4221', abs(pb - 0.2588) < 0.004, f'{pb:.4f}')

ss, T, mm, mu3 = 0.0147, 1 / 3, 84, 0.09
s2 = ss / T
keys(1, 'p-realised-then-risk', 1, S(s2), {'not-annual': S(ss), 'variance': s2, 'times-days': S(ss * 252)})
sdest = s2 * S(2 / mm)
keys(1, 'p-realised-then-risk', 2, sdest, {'no-sigma': S(2 / mm), 'sum-not-rate': sdest * T, 'variance': sdest ** 2})


def pbelow(sig2, drift=None):
    d = mu3 - sig2 / 2 if drift is None else drift
    return Phi((L(60 / 64) - d) / S(sig2))


keys(1, 'p-realised-then-risk', 3, pbelow(s2), {'no-drag': pbelow(s2, drift=mu3), 'upper': 1 - pbelow(s2), 'not-annual': pbelow(ss)})
near('p1 realised part 3: a four-figure table read at z=-0.63 still lands in the key band', Phi(-0.63), part(1, 'p-realised-then-risk', 3)['widget']['answer'], 0.0005)
s2b = s2 + 2 * sdest
keys(1, 'p-realised-then-risk', 4, pbelow(s2b), {'unchanged': pbelow(s2), 'sd-on-sigma': pbelow((S(s2) + 2 * sdest) ** 2), 'same-drift': pbelow(s2b, drift=mu3 - s2 / 2)})
R = (mu3 - s2 / 2) / 252 + S(s2 / 252) * rng.standard_normal((200000, mm))
est = (R ** 2).sum(axis=1) / T
chk('p1 realised MC: sd of sum r^2 / T is 0.0068 (2 sigma^4/m)', abs(est.std() - sdest) < 0.0001, f'{est.std():.5f}')
chk('p1 realised MC: mean of the estimate is sigma^2 to 1%', abs(est.mean() - s2) < 0.0004, f'{est.mean():.5f}')

# ------------------------------------------------------------------ problems-2
mu, sg, X0 = 0.02, 0.12, 1.25
EY = 0.8 * E(3 * (sg * sg - mu))
keys(2, 'p-cable-inverse', 2, EY, {'inverse-mean': 1 / (X0 * E(3 * mu)), 'median': 0.8 * E(-3 * (mu - sg * sg / 2))})
keys(2, 'p-cable-inverse', 3, X0 * E(3 * mu) * EY, {'one': 1, 'median-y': X0 * E(3 * mu) * 0.8 * E(-3 * (mu - sg * sg / 2))})
near('p2 cable part 3: carrying the rounded 0.7867 stays in band', X0 * E(3 * mu) * 0.7867, part(2, 'p-cable-inverse', 3)['widget']['answer'], 6e-5)
keys(2, 'p-cable-inverse', 4, sg * sg, {'log-flat': sg * sg / 2, 'zero': 0, 'sigma': sg})
chk('p2 cable part 1 expression key', part(2, 'p-cable-inverse', 1)['widget']['answer'].replace(' ', '') == '\\sigma^2-\\mu')
N, m = 400000, 600
x = np.full(N, X0)
dt = 3 / m
for _ in range(m):
    x += mu * x * dt + sg * x * S(dt) * rng.standard_normal(N)
y = 1 / x
se = y.std() / S(N)
chk('p2 cable EM: E[1/X_3] = 0.7867 (drift sigma^2 - mu), not 0.7534 or 0.7699', abs(y.mean() - EY) < 4 * se and se < 0.001, f'{y.mean():.4f} se {se:.4f}')
chk('p2 cable EM: E[X_3]E[Y_3] = e^{3 sigma^2} = 1.0441', abs(x.mean() * y.mean() - E(3 * sg * sg)) < 0.002, f'{x.mean()*y.mean():.4f}')
x = np.full(N, X0)
for _ in range(m):
    x += sg * sg * x * dt + sg * x * S(dt) * rng.standard_normal(N)
chk('p2 cable EM: mu = sigma^2 keeps E[Y_3] at 0.8', abs((1 / x).mean() - 0.8) < 0.001, f'{(1/x).mean():.4f}')

Wp = np.array([0, 0.3, -0.2, 0.4, 0.6])
dW = np.diff(Wp)
left = (Wp[:-1] ** 2 * dW).sum()
keys(2, 'p-cube-path', 1, left, {'right-point': (Wp[1:] ** 2 * dW).sum(), 'ordinary': 0.6 ** 3 / 3, 'no-square': (Wp[:-1] * dW).sum()})
mid = (Wp[:-1] * dW ** 2).sum()
chk('p2 cube part 2: sum of cubed moves is 0.126', abs((dW ** 3).sum() - 0.126) < 1e-12)
keys(2, 'p-cube-path', 2, mid, {'no-third': 3 * mid, 'no-cube': (0.216 - 3 * left) / 3})
chk('p2 cube: telescoping identity on the path', abs(0.216 - (3 * left + 3 * mid + (dW ** 3).sum())) < 1e-12)
errs, cubes, alt1, alt0 = [], [], [], []
for mref in (64, 1024, 16384):
    d = S(1 / mref) * rng.standard_normal((2000, mref))
    Wk = np.cumsum(d, axis=1) - d
    a = (Wk * d * d).sum(axis=1)
    bb = Wk.sum(axis=1) / mref
    errs.append(S(((a - bb) ** 2).mean()))
    cubes.append(S(((d ** 3).sum(axis=1) ** 2).mean()))
    alt1.append(S(((a - (Wk * d).sum(axis=1)) ** 2).mean()))
    alt0.append(S((a ** 2).mean()))
chk('p2 cube MC: sum W(dW)^2 - int W dt shrinks to 0 in L2', errs[2] < 0.02 and errs[2] < errs[0] / 8, str([round(e, 4) for e in errs]))
chk('p2 cube MC: sum (dW)^3 shrinks to 0', cubes[2] < 0.05 and cubes[2] < cubes[0] / 8, str([round(e, 4) for e in cubes]))
chk('p2 cube MC: the limit is not int W dW and not 0', alt1[2] > 0.5 and alt0[2] > 0.4, f'{alt1[2]:.3f} {alt0[2]:.3f}')

v = 0.4 ** 2 * 0.25 + 0.15 ** 2 * 0.75
avg = 0.4 * 0.25 + 0.15 * 0.75
keys(2, 'p-results-vol', 1, v, {'average-first': avg ** 2, 'no-weights': 0.16 + 0.0225, 'not-squared': avg})
keys(2, 'p-results-vol', 2, S(v), {'time-average': avg, 'plain-average': 0.275, 'variance': v})
keys(2, 'p-results-vol', 3, 72 * E(0.06 - v / 2), {'mean': 72 * E(0.06), 'average-vol': 72 * E(0.06 - avg ** 2 / 2), 'full-variance': 72 * E(0.06 - v)})
pk = Phi(-(0.06 - v / 2) / S(v))
keys(2, 'p-results-vol', 4, pk, {'average-vol': Phi(-(0.06 - avg ** 2 / 2) / avg), 'no-drag': Phi(-0.06 / S(v)), 'upper': 1 - pk})
N, m = 400000, 400
s = np.full(N, 72.0)
dt = 1 / m
for k in range(m):
    sig = 0.4 if k * dt < 0.25 else 0.15
    s += 0.06 * s * dt + sig * s * S(dt) * rng.standard_normal(N)
ls = np.log(s / 72)
chk('p2 results-vol EM: variance of ln S_1 is 0.0569, not 0.0452', abs(ls.var() - v) < 0.001, f'{ls.var():.5f}')
chk('p2 results-vol EM: median of S_1 is 74.31', abs(np.median(s) - 72 * E(0.06 - v / 2)) < 0.12, f'{np.median(s):.3f}')
chk('p2 results-vol EM: P(S_1<72) is 0.4474, not 0.4301 or 0.4007', abs((s < 72).mean() - pk) < 0.004, f'{(s<72).mean():.4f}')

# ------------------------------------------------------------------ problems-3
r, sg = 0.04, 0.25
a2 = -2 * r / sg ** 2
keys(3, 'p-touch-note', 1, [1, a2], {'sign': [1, -a2], 'no-half': [1, a2 / 2]})
for a in (1, a2):
    chk(f'p3 touch-note: a={a} solves the time-free equation', abs(0.5 * sg * sg * a * (a - 1) + r * a - r) < 1e-12)
V = (100 / 75) ** a2
keys(3, 'p-touch-note', 3, V, {'sign': (4 / 3) ** (-a2), 'no-half': (4 / 3) ** (a2 / 2), 'root-one': 4 / 3})
keys(3, 'p-touch-note', 4, 10000 * a2 * V / 100, {'sign': -10000 * a2 * V / 100, 'no-power': -10000 * V / 100})
near('p3 touch-note part 4: carrying V=0.6920 stays in band', 10000 * a2 * 0.6920 / 100, part(3, 'p-touch-note', 4)['widget']['answer'], 0.05)
nu = (r - sg * sg / 2) / sg
lt = E(-(L(100 / 75) / sg) * (nu + S(nu * nu + 2 * r)))
near('p3 touch-note: E_Q[e^{-r tau}] by the hitting-time transform equals (S/75)^-1.28', lt, V, 1e-12)
# simulation under Q: exact log steps, bridge test for a touch inside each step, 150 years
N, dt, yrs = 40000, 0.02, 150
x = np.full(N, L(100.0))
b = L(75.0)
alive = np.ones(N, bool)
val = np.zeros(N)
for k in range(int(yrs / dt)):
    idx = np.nonzero(alive)[0]
    if idx.size == 0:
        break
    xo = x[idx]
    xn = xo + (r - sg * sg / 2) * dt + sg * S(dt) * rng.standard_normal(idx.size)
    ptouch = np.where(xn <= b, 1.0, np.exp(-2 * (xo - b) * (np.maximum(xn, b) - b) / (sg * sg * dt)))
    hit = rng.random(idx.size) < ptouch
    val[idx[hit]] = E(-r * (k + 0.5) * dt)
    alive[idx[hit]] = False
    x[idx] = xn
se = val.std() / S(N)
chk('p3 touch-note MC under Q: value at 100 is 0.692, not 0.832 or 1.333', abs(val.mean() - V) < 4 * se + 0.001 and se < 0.004, f'{val.mean():.4f} se {se:.4f}')

sA, sB, mA, rr = 0.18, 0.30, 0.095, 0.05
xB = 1000 * sA / sB
keys(3, 'p-twin-shares', 1, xB, {'inverted': 1000 * sB / sA, 'equal': 1000, 'variance-ratio': 1000 * (sA / sB) ** 2})
mB = (1000 * mA - rr * (1000 - xB)) / xB
keys(3, 'p-twin-shares', 2, mB, {'whole-book': (1000 * mA - rr * 1000) / xB, 'no-r': 1000 * mA / xB, 'same-drift': mA})
chk('p3 twin-shares: equal excess drift per unit of vol, 0.25', abs((mA - rr) / sA - 0.25) < 1e-12 and abs((mB - rr) / sB - 0.25) < 1e-12)
dR = mB - mA + sA * sA - sA * sB
keys(3, 'p-twin-shares', 3, dR, {'no-ito': mB - mA, 'no-cross': mB - mA + sA * sA, 'no-convexity': mB - mA - sA * sB, 'log-drift': (mB - sB * sB / 2) - (mA - sA * sA / 2)})
dQ = sA * sA - sA * sB
price = 100 * 0.75 * E(2 * dQ) * E(-2 * rr)
keys(3, 'p-twin-shares', 4, price, {'real-drift': 75 * E(2 * dR - 0.1), 'martingale': 75 * E(-0.1), 'undiscounted': 75 * E(2 * dQ), 'log-drift': 75 * E(2 * (sA * sA / 2 - sB * sB / 2) - 0.1)})
N, m = 400000, 500
dt = 2 / m
for lab, da, db, want in (('P', mA, mB, 0.75 * E(2 * dR)), ('Q', rr, rr, 0.75 * E(2 * dQ))):
    A = np.full(N, 60.0)
    B = np.full(N, 45.0)
    for j in range(m):
        dw = S(dt) * rng.standard_normal(N)
        if lab == 'P' and j == 0:
            book1 = 1000 * (mA * dt + sA * dw) - 600 * (mB * dt + sB * dw)
        A, B = A + da * A * dt + sA * A * dw, B + db * B * dt + sB * B * dw
    Rr = B / A
    se = Rr.std() / S(N)
    chk(f'p3 twin-shares EM under {lab}: E[R_2] = {want:.4f}', abs(Rr.mean() - want) < 4 * se + 0.0005, f'{Rr.mean():.4f} se {se:.4f}')
    if lab == 'P':
        chk('p3 twin-shares: the 1000/600 book has no noise and earns 5% on 400', book1.std() < 1e-9 and abs(book1.mean() / dt - 20) < 1e-6)
    else:
        chk('p3 twin-shares EM under Q: note price 64.99, not 67.86 or 64.06', abs(100 * Rr.mean() * E(-0.1) - price) < 0.12, f'{100*Rr.mean()*E(-0.1):.3f}')

sg, rr, b = 0.28, 0.045, L(112)
cl = [105.0, 107.6, 111.2, 110.3, 109.4]
vd = sg * sg / 252
pt = [E(-2 * (b - L(x)) * (b - L(y)) / vd) for x, y in zip(cl, cl[1:])]
x_, y_ = L(111.2), L(110.3)
keys(3, 'p-bridge-closes', 2, pt[2], {'no-two': E(-(b - x_) * (b - y_) / vd), 'whole-year': E(-2 * (b - x_) * (b - y_) / sg ** 2), 'survival': 1 - pt[2]})
near('p3 bridge: density ratio n(2b-y)/n(y) equals the exponential form', norm.pdf(2 * b - y_, x_, S(vd)) / norm.pdf(y_, x_, S(vd)), pt[2], 1e-9)
surv = float(np.prod([1 - t for t in pt]))
keys(3, 'p-bridge-closes', 3, surv, {'sum-rule': 1 - sum(pt), 'one-gap': 1 - pt[2], 'touch': 1 - surv})
chk('p3 bridge: gap chances 6e-8, 0.1577, 0.4942, 0.0993', pt[0] < 1e-7 and abs(pt[1] - 0.1577) < 5e-5 and abs(pt[3] - 0.0993) < 5e-5, str([round(t, 5) for t in pt]))
chk('p3 bridge: Q drift of ln S is 0.0058', abs(rr - sg * sg / 2 - 0.0058) < 1e-12)
df = E(-rr * 4 / 252)
keys(3, 'p-bridge-closes', 4, df * 9.40 * surv, {'plain': df * 9.40, 'knock-in': df * 9.40 * (1 - surv), 'one-gap': df * 9.40 * (1 - pt[2]), 'sum-rule': df * 9.40 * (1 - sum(pt))})
near('p3 bridge part 4: a 4/365 discount factor stays in band', E(-rr * 4 / 365) * 9.40 * surv, part(3, 'p-bridge-closes', 4)['widget']['answer'], 0.01)
# One day of ln S on a fine grid under two very different drifts (0.0058 and -6 a year); keep paths ending near y and count
# touches of b. A grid misses some touches (error ~ c sqrt(dt)), so extrapolate from 256 and 1024 steps.
ext = {}
for drift in (rr - sg * sg / 2, -6.0):
    pr = {}
    for sub in (256, 1024):
        hits = tot = 0
        for _ in range(14):
            d = drift / 252 / sub + S(vd / sub) * rng.standard_normal((50000, sub))
            pth = np.cumsum(d, axis=1)
            keep = np.abs(pth[:, -1] - (y_ - x_)) < 0.0004
            hits += int((pth[keep].max(axis=1) >= b - x_).sum())
            tot += int(keep.sum())
        pr[sub] = hits / tot
    ext[drift] = 2 * pr[1024] - pr[256]
    print(f'     drift {drift:.4f}: 256 steps {pr[256]:.4f}, 1024 steps {pr[1024]:.4f} (n={tot}), extrapolated {ext[drift]:.4f}')
dv = list(ext.values())
chk('p3 bridge MC: touch chance between the closes is 0.494, not 0.703 or 0.997', all(abs(d - pt[2]) < 0.035 for d in dv), str([round(d, 4) for d in dv]))
chk('p3 bridge MC: drift 0.0058 and drift -6 a year give the same pinned touch chance', abs(dv[0] - dv[1]) < 0.04, f'{dv[0]-dv[1]:+.4f}')

# ------------------------------------------------------------------ problems-4
x0, Lw, s_ = 30, 50, 2
Pt = x0 / Lw
keys(4, 'p-band-wait', 1, Pt * Lw ** 3, {'start-cube': x0 ** 3, 'swapped': (1 - Pt) * Lw ** 3, 'sure-top': Lw ** 3})
EtX = (Pt * Lw ** 3 - x0 ** 3) / (3 * s_ ** 2)
keys(4, 'p-band-wait', 2, EtX, {'no-half': 48000 / 24, 'sigma-unsquared': 48000 / 6, 'no-start': 75000 / 12, 'unit-c': 48000 / 3})
A = EtX / Lw
keys(4, 'p-band-wait', 3, A, {'squared-level': EtX / Lw ** 2, 'no-divide': EtX})
keys(4, 'p-band-wait', 4, A / Pt, {'times-p': A * Pt, 'joint': A, 'swapped': A / (1 - Pt)})
Et = x0 * (Lw - x0) / s_ ** 2
chk('p4 band-wait: E[tau] = 150 and general formula (L^2-x^2)/(3 sigma^2) = 1600/12', Et == 150 and abs((Lw ** 2 - x0 ** 2) / (3 * s_ ** 2) - A / Pt) < 1e-9)
keys(4, 'p-band-wait', 5, (Et - A) / (1 - Pt), {'wrong-weight': (Et - A / Pt) / (1 - Pt), 'no-condition': Et - A, 'top-chance': (Et - A) / Pt})
# lattice walk: step h pips every h^2/4 minutes, a martingale with (dX)^2 = 4 dt that hits the edges exactly
h = 0.5
N = 60000
pos = np.full(N, int(x0 / h))
top = int(Lw / h)
steps = np.zeros(N)
act = np.ones(N, bool)
k = 0
while act.any():
    idx = np.nonzero(act)[0]
    pos[idx] += rng.integers(0, 2, idx.size) * 2 - 1
    k += 1
    done = (pos[idx] == 0) | (pos[idx] == top)
    steps[idx[done]] = k
    act[idx[done]] = False
tmin = steps * h * h / s_ ** 2
up = pos == top
Xt = np.where(up, 50.0, 0.0)
chk('p4 band-wait MC: P(top) = 0.6', abs(up.mean() - 0.6) < 0.008, f'{up.mean():.4f}')
chk('p4 band-wait MC: E[tau] = 150', abs(tmin.mean() - 150) < 2.5, f'{tmin.mean():.2f}')
chk('p4 band-wait MC: E[tau X_tau] = 4000, not 2000, 8000 or 6250', abs((tmin * Xt).mean() - 4000) < 120, f'{(tmin*Xt).mean():.1f}')
chk('p4 band-wait MC: E[tau | top] = 133.3', abs(tmin[up].mean() - 400 / 3) < 3, f'{tmin[up].mean():.2f}')
chk('p4 band-wait MC: E[tau | floor] = 175, the longer wait', abs(tmin[~up].mean() - 175) < 4, f'{tmin[~up].mean():.2f}')
Xf = 30 + 2 * S(7.0) * rng.standard_normal(4000000)
chk('p4 band-wait MC: E[X_t^3 - 12 t X_t] stays at 27,000 at t = 7 (c = 12, not 6 or 24)', abs((Xf ** 3 - 84 * Xf).mean() - 27000) < 150, f'{(Xf**3-84*Xf).mean():.0f}')

rr, sg = 0.03, 0.30
keys(4, 'p-two-date-product', 1, sg * sg * 1, {'later-time': sg * sg * 2, 'independent': 0, 'unsquared': sg})
var = sg * sg * (1 + 2 + 2)
keys(4, 'p-two-date-product', 2, var, {'no-cov': sg * sg * 3, 'cov-once': sg * sg * 4, 'later-time': sg * sg * (3 + 4)})
mlog = 3 * (rr - sg * sg / 2)
chk('p4 two-date: log mean shift is -0.045', abs(mlog + 0.045) < 1e-12)
EQ = 25 * E(mlog + var / 2)
keys(4, 'p-two-date-product', 3, EQ, {'no-cov': 25 * E(mlog + 0.27 / 2), 'r-drift': 25 * E(3 * rr + var / 2), 'no-half': 25 * E(mlog + var)})
keys(4, 'p-two-date-product', 4, EQ * E(-2 * rr), {'forwards': 25 * E(3 * rr - 2 * rr), 'one-year': EQ * E(-rr), 'undiscounted': EQ})
chk('p4 two-date: covariance is worth about 2.43', abs(EQ * E(-2 * rr) - 25 * E(rr) - 2.43) < 0.005)
N, m = 400000, 250
dt = 1 / m
s = np.full(N, 50.0)
for _ in range(m):
    s += rr * s * dt + sg * s * S(dt) * rng.standard_normal(N)
s1 = s.copy()
for _ in range(m):
    s += rr * s * dt + sg * s * S(dt) * rng.standard_normal(N)
pay = s1 * s / 100
se = pay.std() / S(N)
chk('p4 two-date EM under Q: Cov(ln S_1, ln S_2) = 0.09', abs(np.cov(np.log(s1), np.log(s))[0, 1] - 0.09) < 0.002)
chk('p4 two-date EM under Q: E[S_1 S_2/100] = 29.93, not 27.35', abs(pay.mean() - EQ) < 4 * se + 0.05 and se < 0.05, f'{pay.mean():.3f} se {se:.3f}')

rr, q, S0, Tm = 0.045, 0.02, 120, 0.75
Vp = S0 * E(-q * Tm)
keys(4, 'p-dividend-hedge', 3, q * Vp, {'plus': -q * Vp, 'no-yield': 0, 'no-discount': q * S0})
near('p4 dividend: V_t by finite difference', (S0 * E(-q * (Tm - 1e-6)) - Vp) / 1e-6, q * Vp, 1e-4)
chk('p4 dividend: V = S e^{-q(T-t)} satisfies V_t + (r-q) S V_S - r V = 0', abs(q * Vp + (rr - q) * Vp - rr * Vp) < 1e-12)
K = Vp * E(rr * Tm)
keys(4, 'p-dividend-hedge', 4, K, {'prepaid': Vp, 'no-yield': S0 * E(rr * Tm), 'plus': S0 * E((rr + q) * Tm)})
# Hedge under a real-world drift: sell the claim for V, hold V_S shares, bank dividends, finance at r.
# At T the one share held is delivered, so the cash left over is the book's profit: it must be 0 for any mu.
N, m, mu, sg = 20000, 3000, 0.11, 0.25
dt = Tm / m
s = np.full(N, 120.0)
cash = np.full(N, Vp - E(-q * Tm) * 120.0)
cash_nodiv = cash.copy()
for k in range(m):
    t = k * dt
    d0 = E(-q * (Tm - t))
    sn = s + mu * s * dt + sg * s * S(dt) * rng.standard_normal(N)
    d1 = E(-q * (Tm - t - dt))
    cash_nodiv = cash_nodiv * (1 + rr * dt) - (d1 - d0) * sn
    cash = cash * (1 + rr * dt) + q * d0 * s * dt - (d1 - d0) * sn
    s = sn
chk('p4 dividend hedge EM: short claim + V_S shares + dividends ends flat', abs(cash.mean()) < 0.02 and cash.std() < 0.05, f'mean {cash.mean():.4f} sd {cash.std():.4f}')
chk('p4 dividend hedge EM: without the dividend cash the book ends short', cash_nodiv.mean() < -1.5, f'{cash_nodiv.mean():.3f}')
chk('p4 dividend part 2 key r-q', part(4, 'p-dividend-hedge', 2)['widget']['answer'].replace(' ', '') == 'r-q')
chk('p2 cube part 4 key 3w', part(2, 'p-cube-path', 4)['widget']['answer'] == '3w')
for nset, item, k, cid in ((2, 'p-cube-path', 3, 'time-integral'), (3, 'p-touch-note', 2, 'negative-power'),
                           (3, 'p-bridge-closes', 1, 'end-values'), (4, 'p-dividend-hedge', 1, 'with-yield')):
    o = [x['id'] for x in part(nset, item, k)['widget']['options'] if x.get('correct')]
    chk(f'p{nset} {item} part {k} correct option is {cid}', o == [cid])

print(f'\n{nchk} checks, {len(fails)} failed')
for f in fails:
    print('  FAILED:', f)
sys.exit(1 if fails else 0)
