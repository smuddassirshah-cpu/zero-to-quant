#!/usr/bin/env python3
"""Blind concept audit, numerics problems-1 to problems-4: independent recomputation
of every key, slip and stated figure. Exits 0 when all content checks pass.
Fix pass: the P4 I0 P0 finding check encoded the old explain text and is re-pointed
to the new sentence; the P2 I0 P1 slip check is unchanged."""
import json, math, os, sys
import numpy as np
import mpmath
from scipy import stats, integrate
from scipy.interpolate import CubicSpline
from scipy.linalg import solve_banded
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'numerics')
bad = []; n = 0
def ck(name, cond, detail=''):
    global n; n += 1
    if not cond: bad.append(name + ' ' + str(detail)); print('FAIL', name, detail)
def near(name, got, want, tol): ck(name, abs(got - want) <= tol, f'got {got!r} want {want!r}')
P = {k: json.load(open(os.path.join(C, f'problems-{k}.json'))) for k in (1, 2, 3, 4)}
def W(k, i, p): return P[k]['items'][i]['parts'][p]['widget']
def key(k, i, p, val, slips=None):
    """val must fall inside the key's band; each named slip inside its own band;
    every slip outside the key band; every authored slip recomputed."""
    w = W(k, i, p); t = w['tol'].get('abs', 0)
    ck(f'P{k} I{i} P{p} key', abs(val - w['answer']) <= t + 1e-12, f"got {val!r} key {w['answer']}")
    ids = {x['id']: x for x in w.get('wrong', [])}
    for sid, sv in (slips or {}).items():
        x = ids.get(sid)
        if x is None: ck(f'P{k} I{i} P{p} slip {sid} exists', False); continue
        ck(f'P{k} I{i} P{p} slip {sid}', abs(sv - x['value']) <= x['tol'].get('abs', 0) + 1e-12, f"got {sv!r} slip {x['value']}")
    if slips is not None:
        for x in w.get('wrong', []):
            ck(f'P{k} I{i} P{p} slip {x["id"]} outside key', abs(x['value'] - w['answer']) > t + x['tol'].get('abs', 0))
            ck(f'P{k} I{i} P{p} slip {x["id"]} recomputed', x['id'] in slips)

# ---------------- problems-1 ----------------
near('f32 gap', float(np.spacing(np.float32(0.75))), 2.0**-24, 0)
near('f32 eps', float(np.finfo(np.float32).eps), 2.0**-23, 0)
key(1, 0, 0, -24, {'eps': -23, 'sign': 24, 'half': -25})
g = 2.0**-24
key(1, 0, 1, g / 1e-4, {'one-factor': g / 2 / 1e-4, 'eps': 2 * g / 1e-4})
key(1, 0, 1, 0.060 / 100)                # learner types 0.060 (3 dp, per cent)
p0, p1 = np.float32(0.9425), np.float32(0.9424)
ck('f32 half-gap bound', abs(float(p0) - 0.9425) <= g / 2 and abs(float(p1) - 0.9424) <= g / 2)
ck('Sterbenz exact', float(p0 - p1) == float(p0) - float(p1))
ck('diff err <= gap', abs(float(p0 - p1) - 1e-4) <= g)
ratio = (g / 1e-4) / (g / 2 / 0.9425)
key(1, 0, 2, ratio, {'one-input': ratio / 2, 'per-cent': 0.0596 / 3.16e-8})
key(1, 0, 2, 5.96e-4 / 3.16e-8)          # the rounded route the feedback prints
near('kappa 18849', (0.9425 + 0.9424) / 1e-4, 18849, 0.5)
near('rel err factor', g / 2 / 0.9425, 3.16e-8, 5e-11)
near('digits lost', math.log10(18850), 4.3, 0.05)
f = 1e-4 * 365 / 0.9424
near('f 3.873%', f, 0.03873, 5e-6)
key(1, 0, 3, f * g / 1e-4 * 1e4, {'eps': f * 2 * g / 1e-4 * 1e4, 'one-factor': f * g / 2 / 1e-4 * 1e4})
key(1, 0, 3, 0.03873 * 5.96e-4 * 1e4)
d32 = np.float32(1) / np.float32(365)
f32 = float((p0 - p1) / (d32 * p1))
ck('f32 forward within the 0.2309 bp bound', abs(f32 - f) * 1e4 <= 0.2309 * 1.001, abs(f32 - f) * 1e4)

# moment recurrence
mpmath.mp.dps = 50
I0 = 1 - math.exp(-1)
I = I0; fw = [I]
for k in range(1, 19): I = 1 - k * I; fw.append(I)
Itrue = [float(mpmath.quad(lambda x, m=m: x**m * mpmath.exp(x - 1), [0, 1])) for m in range(26)]
near('I1 = 1 - I0', Itrue[1], 1 - Itrue[0], 1e-13)
ck('I_n positive, decreasing', all(Itrue[m] > Itrue[m + 1] > 0 for m in range(25)))
print('forward I18', fw[18], 'true', Itrue[18])
ck('forward I18 negative in doubles', fw[18] < 0, fw[18])
ck('forward error same order as 18! u I0', abs(fw[18] - Itrue[18]) < 5 * 0.4493, fw[18] - Itrue[18])
key(1, 1, 0, math.log10(math.factorial(18)), {'one-step': math.log10(18), 'sum': math.log10(171)})
near('18! 6.40e15', math.factorial(18), 6.40e15, 5e12)
u = 2.0**-53
key(1, 1, 1, u * I0 * math.factorial(18), {'eps': 2 * u * I0 * math.factorial(18), 'no-i0': u * math.factorial(18)})
key(1, 1, 1, 1.11e-16 * 0.632 * 6.40e15)
I0c = float(1 - mpmath.exp(-1))
ck('rounded I0 within u I0', abs(mpmath.mpf(I0c) - (1 - mpmath.exp(-1))) <= u * I0)
ck('I18 in [1/19e, 1/19]', 1 / (19 * math.e) < Itrue[18] < 1 / 19)
near('1/19e', 1 / (19 * math.e), 0.019, 5e-4); near('1/19', 1 / 19, 0.053, 5e-4)
bound = lambda N: math.factorial(18) / math.factorial(N + 1)
near('4.1e-10', bound(24), 4.1e-10, 5e-12); near('1.6e-11', bound(25), 1.6e-11, 5e-13)
Nmin = next(N for N in range(18, 60) if bound(N) < 1e-10)
Nns = next(N for N in range(18, 60) if math.factorial(18) / math.factorial(N) < 1e-10)
key(1, 1, 3, Nmin, {'no-start': Nns, 'one-short': Nmin - 1})
b = 0.0; seq = {25: 0.0}
for k in range(25, 18, -1): b = (1 - b) / k; seq[k - 1] = b
key(1, 1, 4, b, {'upper': 1 / 19})
near('I24', seq[24], 0.04, 1e-15); near('I23', seq[23], 0.04, 1e-15); near('I22', seq[22], 0.041739, 5e-7)
ck('backward good to ~1e-11', abs(b - Itrue[18]) < 1.6e-11, b - Itrue[18])

# netting sum
kap = (2400 + 2394) / 6
key(1, 2, 0, kap, {'inflow': 2400 / 6, 'one': 1})
nn = 2**22
key(1, 2, 1, kap * nn * u * 1e7, {'eps': kap * nn * 2 * u * 1e7, 'no-kappa': nn * u * 1e7})
key(1, 2, 2, kap * nn * u * 6e6, {'gross': kap * nn * u * 4794e6, 'eps': 2 * kap * nn * u * 6e6})
key(1, 2, 2, 3.72e-7 * 6e6)
near('nu x gross', nn * u * 4794e6, 2.2324, 1e-3)
key(1, 2, 3, kap * 22 * u * 6e6 * 1e5, {'log10': kap * math.log10(nn) * u * 6e6 * 1e5})
key(1, 2, 3, 799 * 22 * 1.11e-16 * 6e6 * 1e5)
near('five more digits', math.log10(nn / 22), 5.3, 0.1)
rng = np.random.default_rng(7)
def pairwise(a):
    a = a.copy()
    while len(a) > 1: a = a[0::2] + a[1::2]
    return float(a[0])
worst_r = worst_p = 0.0
for rep in range(4):
    m = 2**18
    x = np.concatenate([rng.uniform(0, 1, m // 2), -rng.uniform(0, 1, m // 2)]); rng.shuffle(x)
    ex = math.fsum(x); gross = float(np.abs(x).sum())
    s = 0.0
    for v in x.tolist(): s += v
    worst_r = max(worst_r, abs(s - ex) / gross); worst_p = max(worst_p, abs(pairwise(x) - ex) / gross)
ck('recursive within n u gross', worst_r <= 2**18 * u, worst_r)
ck('pairwise within log2(n) u gross', worst_p <= 18 * u, worst_p)
ck('pairwise beats recursive', worst_p < worst_r, (worst_p, worst_r))

# ---------------- problems-2 ----------------
F = lambda v: 50 * v**3 + 40 * v**2 + 30 * v - 100
dF = lambda v: 150 * v**2 + 80 * v + 30
ddF = lambda v: 300 * v + 80
ck('bracket signs', F(0.5) < 0 < F(1))
near('f(.5)', F(0.5), -68.75, 0); near("f'(.5)", dF(0.5), 107.5, 0)
v1 = 0.5 - F(0.5) / dF(0.5)
key(2, 0, 0, v1, {'sign': 0.5 + F(0.5) / dF(0.5)})
key(2, 0, 1, F(0.75), {'accepted': F(v1), 'endpoint': F(1), 'sign': -F(0.75)})
# FINDING CHECK: the 'accepted' slip says 'That is f(1.1395)'; the carried 4 dp figure must fire it
xa = [x for x in W(2, 0, 1)['wrong'] if x['id'] == 'accepted'][0]
near("P2 I0 P1 slip accepted reachable from the carried 1.1395", F(1.1395), xa['value'], xa['tol']['abs'])
near("f'(.75)", dF(0.75), 174.375, 0)
v2 = 0.75 - F(0.75) / dF(0.75)
key(2, 0, 2, v2, {'sign': 0.75 + F(0.75) / dF(0.75)})
near('17/18', v2, 17 / 18, 1e-15); ck('f(17/18)>0', F(v2) > 0)
vs_mp = mpmath.findroot(lambda v: 50 * v**3 + 40 * v**2 + 30 * v - 100, 0.918)
vs = float(vs_mp)
ck("flatter at 0.5 than at root", dF(0.5) < 0.5 * dF(vs))
near('error 0.026', v2 - vs, 0.026, 5e-4)
near('C 0.77', ddF(vs) / (2 * dF(vs)), 0.77, 5e-3)
e = 0.026; es = []
for k in range(3): e = 0.77 * e * e; es.append(e)
near('5.2e-4', es[0], 5.2e-4, 5e-6); near('2.1e-7', es[1], 2.1e-7, 5e-9); near('3.4e-14', es[2], 3.4e-14, 1e-15)
ck('3 steps needed', es[1] > 1e-12 > es[2])
vm = mpmath.mpf(17) / 18; real = []
for k in range(3):
    vm = vm - (50 * vm**3 + 40 * vm**2 + 30 * vm - 100) / (150 * vm**2 + 80 * vm + 30); real.append(float(abs(vm - vs_mp)))
near('real 5.1e-4', real[0], 5.1e-4, 5e-6); near('real 2.0e-7', real[1], 2.0e-7, 5e-9); near('real 3.2e-14', real[2], 3.2e-14, 1e-15)
near('beats target by ~30', 1e-12 / real[2], 30, 3)
halv = math.ceil(math.log2((v2 - 0.75) / 1e-12))
key(2, 0, 3, 3, {'one-short': 2, 'bisect': halv})
key(2, 0, 4, 1 / vs - 1, {'one-minus': 1 - vs})
key(2, 0, 4, 8.90 / 100)
w = v2 - F(v2) / dF(v2); near('0.918819', w, 0.918819, 5e-7); w = w - F(w) / dF(w); near('0.918305', w, 0.918305, 5e-7)

p = lambda t: 16 + 4.2 * (t - 1) - 0.6 * (t - 1)**3
near('p(2)', p(2), 19.6, 1e-12); dp2 = 4.2 - 1.8
key(2, 1, 0, -3.6, {'sign': 3.6, 'slope': dp2, 'once': -1.8})
cc = lambda pp: 20.4 - 19.6 - 2.4 - 0.5 * pp
key(2, 1, 1, cc(-3.6), {'no-half': 20.4 - 19.6 - 2.4 + 3.6, 'sign': 20.4 - 19.6 - 2.4 - 1.8, 'once': cc(-1.8)})
key(2, 1, 2, -3.6 + 6 * 0.2, {'sign': 2.4, 'natural': 0, 'once': -3.6 + 3 * 0.2, 'no-half': -3.6 + 6 * 2.0})
q = lambda uu: 19.6 + 2.4 * uu - 1.8 * uu**2 + 0.2 * uu**3
dq = lambda uu: 2.4 - 3.6 * uu + 0.6 * uu**2
ddq = lambda uu: -3.6 + 1.2 * uu
near('q(1)', q(1), 20.4, 1e-12); ck("q'(1) < 0", dq(1) < 0)
un = 0.75 - dq(0.75) / ddq(0.75)
key(2, 1, 3, 2 + un, {'sign': 2 + 0.75 + dq(0.75) / ddq(0.75), 'end-curv': 2 + 0.75 - dq(0.75) / -3.6})
upk = 3 - math.sqrt(5); near("q'(peak)=0", dq(upk), 0, 1e-12); ck('within 5e-5', abs(un - upk) < 5e-5)
key(2, 1, 4, q(0.7639) - 20.4, {'peak': q(0.7639), 'start': q(0.75) - 20.4, 'sign': q(0.7361) - 20.4})
key(2, 1, 4, q(upk) - 20.4)
ns = CubicSpline([1, 2, 3], [16, 19.6, 20.4], bc_type='natural')
tt = np.linspace(1, 3, 2001)
ck('natural spline rises all the way to 3y', bool(np.all(ns(tt, 1) > 0)), ns(tt, 1).min())
ck('natural spline changes p', abs(float(ns(2, 2)) + 3.6) > 0.1, float(ns(2, 2)))

Q = lambda t: 0.98 - 0.03 * (t - 1) - 0.0025 * (t - 1) * (t - 3)
for t_, y_ in ((1, .98), (3, .92), (5, .84)): near(f'p({t_})', Q(t_), y_, 1e-14)
key(2, 2, 0, Q(4), {'linear': 0.88})
ts = 3 + (0.92 - 0.90) / (0.92 - Q(4))
key(2, 2, 1, ts, {'linear': 3 + 0.02 / 0.04})
dQ = lambda t: -0.03 - 0.0025 * (2 * t - 4)
tn = 3.5333 - (Q(3.5333) - 0.9) / dQ(3.5333)
key(2, 2, 2, tn, {'sign': 3.5333 + (Q(3.5333) - 0.9) / dQ(3.5333)})
key(2, 2, 2, ts - (Q(ts) - 0.9) / dQ(ts))
near('p(3.5333)', Q(3.5333), 0.9006235, 5e-8); near("p'(3.5333)", dQ(3.5333), -0.037667, 6e-7)
tx = -4 + math.sqrt(57); near('p(t*)=.9', Q(tx), 0.9, 1e-14); ck('within 2e-5', abs(tn - tx) < 2e-5)
prod = abs((3.5499 - 1) * (3.5499 - 3) * (3.5499 - 5))
key(2, 2, 3, prod * 0.0006 / 6 * 1e4, {'no-factorial': prod * 0.0006 * 1e4, 'fourth': prod * 0.0006 / 24 * 1e4})
near("p'(t*)", dQ(3.5499), -0.03775, 5e-6)
key(2, 2, 4, 2.033e-4 / 0.03775 * 365, {'p-at-3': 2.033e-4 / abs(dQ(3)) * 365, 'no-slope': 2.033e-4 * 365})
shifts = []
for sgn in (1, -1):
    Qt = lambda t, sgn=sgn: Q(t) + sgn * 1e-4 * (t - 1) * (t - 3) * (t - 5)
    tc = brentq(lambda t: Qt(t) - 0.9, 3, 4); shifts.append(abs(tc - tx) * 365)
    ck('crossing shift about 1.97 days', abs(abs(tc - tx) * 365 - 1.9658) < 0.05, abs(tc - tx) * 365)

# ---------------- problems-3 ----------------
fg = lambda x: math.exp(-x * x / 2)
Iex = math.sqrt(2 * math.pi) * (stats.norm.cdf(1) - 0.5)
near('I', Iex, 0.8556244, 5e-8); near('f(.5)', fg(.5), 0.882497, 5e-7); near('f(1)', fg(1), 0.606531, 5e-7)
T1 = 0.5 * (fg(0) + fg(1)); T2 = 0.25 * (fg(0) + 2 * fg(.5) + fg(1))
key(3, 0, 0, T2, {'one-strip': T1, 'no-half': 0.5 * (fg(0) + fg(.5) + fg(1))})
near('T2 err .0127', Iex - T2, 0.0127, 5e-5)
key(3, 0, 1, (4 * T2 - T1) / 3, {'swap': (4 * T1 - T2) / 3, 'order-one': 2 * T2 - T1})
key(3, 0, 1, (4 * 0.8429 - 0.8033) / 3)
near('Simpson err', (4 * T2 - T1) / 3 - Iex, 0.00046, 5e-6)
x1, x2 = 0.5 - 0.5 / math.sqrt(3), 0.5 + 0.5 / math.sqrt(3)
G2 = 0.5 * (fg(x1) + fg(x2))
key(3, 0, 2, G2, {'no-factor': fg(x1) + fg(x2), 'unmapped': 2 * fg(1 / math.sqrt(3))})
near('GL2 err', Iex - G2, 0.00031, 5e-6); ck('GL2 beats Simpson', abs(Iex - G2) < abs((4 * T2 - T1) / 3 - Iex))
key(3, 0, 3, 0.5 + G2 / math.sqrt(2 * math.pi), {'no-half': G2 / math.sqrt(2 * math.pi), 'two-pi': 0.5 + G2 / (2 * math.pi)})
key(3, 0, 3, 0.5 + 0.8553 / 2.5066)
near('Phi(1)', stats.norm.cdf(1), 0.841345, 5e-7)
near('err 1.2e-4', stats.norm.cdf(1) - (0.5 + G2 / math.sqrt(2 * math.pi)), 1.2e-4, 5e-6)
xg, wg = np.polynomial.legendre.leggauss(3)
G3 = sum(0.5 * w_ * fg(0.5 + 0.5 * x_) for x_, w_ in zip(xg, wg))
e3 = 0.5 + G3 / math.sqrt(2 * math.pi) - stats.norm.cdf(1)
ck('GL3 Phi error below 1e-6', abs(e3) < 1e-6, e3)

ff = lambda x: -40 * x - 200 * x * x; h = 0.05
Gf = lambda v: v - 0.05 - h * ff(v); dG = lambda v: 1 + h * (40 + 400 * v)
near("f'(.05)", -40 - 400 * 0.05, -60, 0)
xe = lambda t: 2 * math.exp(-40 * t) / (50 - 10 * math.exp(-40 * t))
near('x(0)', xe(0), 0.05, 1e-15)
for t_ in (0.01, 0.05, 0.2):
    d_ = (xe(t_ + 1e-6) - xe(t_ - 1e-6)) / 2e-6
    near('exact path solves ODE', d_, ff(xe(t_)), 1e-6)
n1 = 0.05 - Gf(0.05) / dG(0.05)
key(3, 1, 0, n1, {'explicit': 0.05 + h * ff(0.05), 'no-one': 0.05 - Gf(0.05) / (dG(0.05) - 1), 'sign': 0.05 + Gf(0.05) / dG(0.05)})
n2 = n1 - Gf(n1) / dG(n1)
key(3, 1, 1, n2, {'frozen': n1 - Gf(n1) / 4, 'sign': n1 + Gf(n1) / dG(n1)})
near('a tenth', (n1 - n2) / (0.05 - n1), 0.1, 0.01)
rt = (-3 + math.sqrt(11)) / 20
key(3, 1, 2, rt, {'stopped': n2, 'other-root': (-3 - math.sqrt(11)) / 20, 'disc': (-3 + math.sqrt(7)) / 20})
near('2.5e-5', n2 - rt, 2.5e-5, 5e-7); near('2.9e-3', n1 - rt, 2.9e-3, 5e-5)
near('C about 3', 20 / (2 * dG(rt)), 3, 0.05); near('3 e^2', 3 * (2.9e-3)**2, n2 - rt, 1e-6)
key(3, 1, 3, rt - xe(h), {'sign': xe(h) - rt, 'explicit': -0.075 - xe(h), 'start': 0.05 - xe(h)})
near('x(.05)', xe(h), 0.005564, 5e-7)
key(3, 1, 4, 0.01027 / 2.53e-5, {'first': 0.01027 / 2.9e-3})
key(3, 1, 4, (rt - xe(h)) / (n2 - rt))
vch = vnw = 0.05; ech = []; enw = []
for k in range(5):
    vch = vch - Gf(vch) / 4; ech.append(abs(vch - rt)); vnw = vnw - Gf(vnw) / dG(vnw); enw.append(abs(vnw - rt))
ck('frozen slope is linear (order 1)', 0.05 < ech[4] / ech[3] < 0.5 and abs(ech[4] / ech[3] - ech[3] / ech[2]) < 0.02, ech)
ck('newton quadratic', abs(enw[2] / enw[1]**2 - 3) < 0.2, enw)
ck('explicit Euler outside |1 + h lambda| <= 1', abs(1 + h * -60) > 1)

def euler(N):
    hh = 4 / N; Pv = 1.0
    for k in range(N): Pv *= 1 - hh * (0.02 + 0.01 * k * hh)
    return Pv
E4, E8, E16 = euler(4), euler(8), euler(16)
near('E4', E4, 0.866947, 5e-7); near('E8', E8, 0.859366, 5e-7); near('E16', E16, 0.855710, 5e-7)
g1, g2 = 0.866947 - 0.859366, 0.859366 - 0.855710
key(3, 2, 0, math.log2(g1 / g2), {'ratio': g1 / g2, 'flip': math.log2(g2 / g1)})
key(3, 2, 1, g2, {'p-two': g2 / 3, 'sign': -g2})
Pex = math.exp(-0.16)
near('true err .00357', E16 - Pex, 0.00357, 5e-6)
key(3, 2, 2, 0.855710 - g2, {'added': 0.855710 + g2, 'p-two': 0.855710 - g2 / 3})
ck('Richardson within 1e-4', abs(0.852054 - Pex) < 1e-4); near('9e-5', Pex - 0.852054, 9e-5, 5e-6)
Cc = 0.003656 / 0.25
Ne = math.ceil(4 * Cc / 1e-5)
C2 = 0.003656 / 0.25**2
key(3, 2, 3, Ne, {'p-two': math.ceil(4 / math.sqrt(1e-5 / C2)), 'floor': Ne - 1})
near('5849.6', 4 * Cc / 1e-5, 5849.6, 0.05); near('1.0001e-5', Cc * 4 / 5849, 1.0001e-5, 5e-10)
ck('true Euler error at 5850 steps is below 1e-5', abs(euler(5850) - Pex) < 1e-5, euler(5850) - Pex)
key(3, 2, 4, Pex, {'no-exp': 1 - 0.16, 'no-minus': math.exp(0.16), 'left-end': math.exp(-0.08)})

# ---------------- problems-4 ----------------
K, sg, r, dt = 30.0, 0.5, 0.04, 0.5
j = np.arange(5)
a = -0.5 * dt * (sg**2 * j**2 - r * j); bb = 1 + dt * (sg**2 * j**2 + r); c = -0.5 * dt * (sg**2 * j**2 + r * j)
A = np.array([[bb[1], c[1], 0], [a[2], bb[2], c[2]], [0, a[3], bb[3]]])
ck('matrix as printed', np.allclose(A, [[1.145, -0.0725, 0], [-0.23, 1.52, -0.27], [0, -0.5325, 2.145]]), A)
rhs = np.array([20 - a[1] * K * math.exp(-r * dt), 10, 0.0])
near('rhs1', rhs[0], 21.5438, 5e-5)
V = np.linalg.solve(A, rhs)
cw = lambda jj, usedt=True, sq=True, rr=True: 1 - (dt if usedt else 1) * (sg**2 * (jj**2 if sq else jj) + (r if rr else 0))
key(4, 0, 0, cw(3), {'no-r': cw(3, rr=False), 'no-dt': cw(3, usedt=False), 'diag': 1 + dt * (sg**2 * 9 + r), 'no-square': cw(3, sq=False), 'sign': -cw(3)})
m2 = -0.23 / 1.145; b2 = 1.52 - m2 * -0.0725; d2 = 10 - m2 * 21.5438
key(4, 0, 1, b2, {'plus': 1.52 + m2 * -0.0725, 'wrong-c': 1.52 - m2 * -0.27})
near("d'2", d2, 14.3276, 5e-5)
m3 = -0.5325 / b2; b3 = 2.145 - m3 * -0.27; d3 = 0 - m3 * d2
key(4, 0, 2, d3 / b3, {'no-pivot': d3 / 2.145, 'zero': 0})
near('V3 solve', V[2], d3 / b3, 1e-4)
V2 = (14.3276 + 0.27 * 2.4728) / 1.5054
key(4, 0, 3, V2, {'sign': (14.3276 - 0.27 * 2.4728) / 1.5054, 'skip': 14.3276 / 1.5054, 'no-div': 14.3276 + 0.27 * 2.4728})
near('V2 solve (exact 9.9607, key built on carried figures)', V[1], V2, 5e-4); near('V1 19.45', V[0], 19.45, 5e-3)
def bs_put(S, K, r, s, T):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T)); d2_ = d1 - s * math.sqrt(T)
    return K * math.exp(-r * T) * stats.norm.cdf(-d2_) - S * stats.norm.cdf(-d1)
near('BS put 10.00', bs_put(20, 30, .04, .5, .5), 10.00, 5e-3)
near('errs about 4p', bs_put(20, 30, .04, .5, .5) - V[1], 0.04, 5e-3)
near('1.145 = step over weight condition at j = 3', dt * (sg**2 * 9 + r), 1.145, 1e-12)
# FINDING CHECK (re-pointed in the fix pass): the l13 bound with j = M gives 2.02, not 1.145, so the
# explain must tie 1.145 to the weight condition at j = 3 and not call it the explicit bound
ex4 = P[4]['items'][0]['parts'][0]['explain']['text']
ck("P4 I0 P0 explain no longer calls 1.145 the explicit bound", 'explicit bound allows' not in ex4 and 'keeps the $j = 3$ weight non-negative' in ex4, ex4)
near('l13 bound at j = M: step / longest step = 2.02', dt * (sg**2 * 16 + r), 2.02, 1e-12)
near('1.145 = step over longest step keeping the j = 3 weight non-negative', dt / (1 / (sg**2 * 9 + r)), 1.145, 1e-12)

vy, vx, cv = 64.0, 100.0, 77.0; bh = 0.77
vc = vy - 2 * bh * cv + bh * bh * vx; rho = cv / math.sqrt(vy * vx)
key(4, 1, 0, vc, {'b-one': vy - 2 * cv + vx, 'plus': vy + 2 * bh * cv + bh * bh * vx, 'one-minus-rho': vy * (1 - rho)})
near('64(1-rho^2)', vy * (1 - rho**2), vc, 1e-9); near('b opt', cv / vx, bh, 1e-12)
cl = lambda v: math.ceil(v - 1e-7)
key(4, 1, 1, cl(1.96**2 * 4.71 / 0.02**2), {'no-196': cl(4.71 / 0.02**2), 'two': cl(4 * 4.71 / 0.02**2), 'plain': cl(1.96**2 * 64 / 0.02**2), 'no-square': cl(1.96 * 4.71 / 0.02**2)})
key(4, 1, 2, 614656 / (1.3 * 45235), {'no-cost': 614656 / 45235, 'times': 614656 * 1.3 / 45235})
key(4, 1, 3, 64 / 4.71, {'se': math.sqrt(64 / 4.71), 'gain': 614656 / (1.3 * 45235)})
rng = np.random.default_rng(11)
L = np.linalg.cholesky(np.array([[vy, cv], [cv, vx]]))
reps, m = 4000, 2000
est = np.empty(reps); estf = np.empty(reps)
for i in range(reps):
    Z = rng.standard_normal((m, 2)) @ L.T
    Yv, Xv = Z[:, 0] + 5.0, Z[:, 1] + 3.0
    est[i] = (Yv - bh * (Xv - 3.0)).mean()
ck('fixed-b estimator unbiased', abs(est.mean() - 5.0) < 4 * math.sqrt(vc / m / reps), est.mean())
ck('fixed-b variance 4.71 per path', abs(est.var() * m / vc - 1) < 0.1, est.var() * m)

M0 = math.gcd(math.gcd(76, 92), 276)
key(4, 2, 0, 276 // M0, {'half': 138, 'pound': 276})
ck('nodes 19 and 23', 76 // M0 == 19 and 92 // M0 == 23)
Nb = lambda M, T=0.75, sq=True: math.ceil(T * (0.09 * (M * M if sq else M) + 0.03))
key(4, 2, 1, Nb(69), {'no-T': Nb(69, T=1), 'down': Nb(69) - 1, 'no-square': Nb(69, sq=False)})
def theta_put(S0, K, r, sigma, T, Smax, M, N, theta, implicit_start=0):
    """l14's theta_bs with the put payoff and edges V(0) = K e^{-r tau}, V(Smax) = 0."""
    dS, dtt = Smax / M, T / N
    jj = np.arange(M + 1); S = jj * dS
    Vv = np.maximum(K - S, 0.0)
    al = 0.5 * (sigma**2 * jj**2 - r * jj)[1:-1]; be = -(sigma**2 * jj**2 + r)[1:-1]; ga = 0.5 * (sigma**2 * jj**2 + r * jj)[1:-1]
    for nstep in range(N):
        th = 1.0 if nstep < implicit_start else theta
        bot = K * math.exp(-r * (nstep + 1) * dtt)
        LV = al * Vv[:-2] + be * Vv[1:-1] + ga * Vv[2:]
        rh = Vv[1:-1] + (1 - th) * dtt * LV
        if th == 0: inner = rh
        else:
            rh[0] += th * dtt * al[0] * bot
            ab = np.zeros((3, M - 1)); ab[0, 1:] = (-th * dtt * ga)[:-1]; ab[1] = 1 - th * dtt * be; ab[2, :-1] = (-th * dtt * al)[1:]
            inner = solve_banded((1, 1), ab, rh)
        Vv = np.concatenate(([bot], inner, [0.0]))
    return float(np.interp(S0, S, Vv))
ref = bs_put(76, 92, 0.03, 0.30, 0.75)
e69 = theta_put(76, 92, .03, .3, .75, 276, 69, 322, 0) - ref
e276 = theta_put(76, 92, .03, .3, .75, 276, 276, 5142, 0) - ref
ecn = theta_put(76, 92, .03, .3, .75, 276, 276, 100, 0.5, 2) - ref
print('grid errors', e69, e276, ecn, 'ref', ref)
near('explicit M=69 N=322 error -0.0219', e69, -0.0219, 1.5e-4)
near('explicit M=276 N=5142 error -0.00137', e276, -0.00137, 1.5e-5)
near('CN M=276 N=100 error -0.0015', ecn, -0.0015, 1e-4)
ck('CN inside target', abs(ecn) < 0.002)
kmin = next(k for k in range(1, 50) if 0.0219 / k**2 < 0.002)
klin = next(k for k in range(1, 50) if 0.0219 / k < 0.002)
key(4, 2, 2, 69 * kmin, {'linear': 69 * klin, 'off-node': math.ceil(69 * math.sqrt(0.0219 / 0.002)), 'k3': 207})
near('k3 predicts', 0.0219 / 9, 0.00243, 5e-6); near('k4 predicts', 0.0219 / 16, 0.00137, 5e-6)
key(4, 2, 3, Nb(276), {'scaled': 16 * 322, 'no-T': Nb(276, T=1), 'down': Nb(276) - 1})
key(4, 2, 4, 276 * 5142 / (3 * 276 * 100), {'no-cost': 5142 / 100, 'scaled': 5152 / 300})

pp, pay = 0.2, 48.0
s = pay * math.sqrt(pp * (1 - pp))
key(4, 3, 0, s, {'no-disc': 50 * 0.4, 'p-only': pay * math.sqrt(pp), 'var': s * s})
key(4, 3, 1, s / 160, {'no-disc': 20 / 160, 'by-n': s / 25600, 'var': s * s / 160})
rh_ = -pp * pp / (pp * (1 - pp))
key(4, 3, 2, rh_, {'minus-p': -pp, 'sign': -rh_, 'cov': -pp * pp})
key(4, 3, 3, 1 / (1 + rh_), {'vrf': 1 / (1 - rh_**2), 'inverted': 1 + rh_, 'one-minus': 1 / (1 - rh_)})
pv = 0.5 * s * s * (1 + rh_)
key(4, 3, 4, round(pv / 0.05**2, 6), {'payoffs': round(2 * pv / 0.05**2, 6), 'plain': round(s * s / 0.05**2, 6), 'one-minus': round(0.5 * s * s * (1 - rh_) / 0.05**2, 6)})
near('3 pairs = 8 paths', pv / 3, s * s / 8, 1e-9)
zc = stats.norm.ppf(1 - pp); z = rng.standard_normal(4_000_000)
B1, B2 = (z > zc) * pay, (-z > zc) * pay
ck('pair never pays twice', not np.any((B1 > 0) & (B2 > 0)))
near('MC rho', np.corrcoef(B1, B2)[0, 1], -0.25, 0.004)
near('MC pair-mean var', ((B1 + B2) / 2).var(), 138.24, 1.0)

print(f'{n} checks, {len(bad)} failed')
sys.exit(1 if bad else 0)
