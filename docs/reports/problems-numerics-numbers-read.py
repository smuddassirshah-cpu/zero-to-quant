"""Second reader's recompute of app/content/courses/numerics/problems-1.json to problems-3.json.

Imports nothing from the author's script. Every key and every `wrong` value is typed from the prose and rebuilt
here by a route of its own (exact fractions, mpmath at 40 digits, brute search, a direct run of the recurrence
or the ODE, numpy float32). Bands: the value rounded as the part asks is accepted, each `wrong` value lies
outside the key band. Stated figures of feedback and explain lines are checked as numbers.

A check that fails on wrong content prints a FINDING line and stays failing; the script still exits 0
(CI runs every script in docs/reports). Run: <scratchpad>/venv/bin/python docs/reports/problems-numerics-numbers-read.py
"""
import json, math, os, sys
from fractions import Fraction as F
import numpy as np
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'numerics')
mp.mp.dps = 40
n_checks = 0
findings = []


def chk(cond, msg):
    global n_checks
    n_checks += 1
    if not cond:
        findings.append(msg)
        print('FINDING', msg)


def items(lv):
    d = json.load(open(os.path.join(COURSE, f'problems-{lv}.json'), encoding='utf8'))
    return {it['id']: it for it in d['items']}


def W(it, k):
    return it['parts'][k - 1]['widget']


def key(it, k, mine, typed=None, name=''):
    """mine: my value of the key; typed: what a learner types at the rounding asked (already in key units)."""
    w = W(it, k)
    a, tol = w['answer'], w['tol']['abs']
    tag = f"{it['id']} part {k} {name}"
    chk(abs(a - mine) <= max(tol, 1e-12) and abs(a - mine) <= 0.51 * 10 ** math.floor(math.log10(abs(a)) - 5 if a else 0) + tol * 0.2 + 1e-12,
        f'{tag}: key {a} against mine {mine}')
    if typed is not None:
        for t in (typed if isinstance(typed, (list, tuple)) else [typed]):
            chk(abs(t - a) <= tol + 1e-12, f'{tag}: typed {t} refused by key {a} tol {tol}')
    return a, tol


def wrong(it, k, wid, mine, slack=None):
    w = W(it, k)
    a, tol = w['answer'], w['tol']['abs']
    e = [x for x in w.get('wrong', []) if x['id'] == wid]
    tag = f"{it['id']} part {k} wrong {wid}"
    chk(len(e) == 1, f'{tag}: entry missing')
    if not e:
        return
    v, wt = e[0]['value'], e[0]['tol']['abs']
    chk(abs(v - mine) <= (slack if slack is not None else max(wt, 1e-9)), f'{tag}: {v} against mine {mine}')
    chk(abs(v - a) > tol + wt, f'{tag}: band reaches the key band')
    chk(wid in it['parts'][k - 1]['feedback'].get('byKey', {}), f'{tag}: no byKey line')


def says(it, k, text, where='any'):
    p = it['parts'][k - 1]
    blob = json.dumps(p['feedback'], ensure_ascii=False) + p['explain']['text'] + p['question']
    chk(text in blob.replace('\\\\', '\\'), f"{it['id']} part {k}: text {text!r} not found (stated figure moved?)")


# ---------------------------------------------------------------- level 1
L1 = items(1)
it = L1['p-float32-overnight']
P0, P1, dl = F(9425, 10000), F(9424, 10000), F(1, 365)
# part 1: float32 gap in [0.5, 1) by numpy
gap = float(np.nextafter(np.float32(0.75), np.float32(1)) - np.float32(0.75))
kk = round(math.log2(gap))
chk(2.0 ** kk == gap, 'float32 gap is a power of two')
key(it, 1, kk, kk)
wrong(it, 1, 'eps', round(math.log2(float(np.finfo(np.float32).eps))))
wrong(it, 1, 'sign', -kk)
wrong(it, 1, 'half', kk - 1)
# every float32 in [0.5, 1) sits within half a gap; the two real factors too
for P in (P0, P1):
    st = F(float(np.float32(float(P))))
    chk(abs(st - P) <= F(1, 2 ** 25), f'float32({float(P)}) within half a gap')
# Sterbenz: the float32 difference of the stored factors is exact
s0, s1 = np.float32(0.9425), np.float32(0.9424)
chk(F(float(s0 - s1)) == F(float(s0)) - F(float(s1)), 'stored difference computed exactly in float32')
# part 2: share of 1e-4, in per cent
rel = F(1, 2 ** 24) / (P0 - P1)
pct = float(rel * 100)
# fix pass: key is now the fraction with unit '%' (review finding 1 applied); typed per cent / 100
a2, t2 = key(it, 2, float(rel), [0.060 / 100, 0.0596 / 100, 0.06 / 100])
wrong(it, 2, 'one-factor', float(rel) / 2)
wrong(it, 2, 'eps', float(rel) * 2)
w2 = W(it, 2)
chk(w2.get('unit') == '%', "p-float32-overnight part 2: unit '%' with the key as a fraction (review finding 1)")
fk, ft = 0.000596, 0.000005
chk(w2['answer'] == fk and w2['tol']['abs'] == ft, 'part 2 key 0.000596 tol 0.000005 as the fix gave')
chk(abs(fk - float(rel)) < 5e-8, 'fix key 0.000596 against 2^-24 / 1e-4')
for typed in (0.060, 0.0596, 0.05960):
    chk(abs(typed / 100 - fk) <= ft, f'fix: {typed}% accepted')
for typed in (0.059, 0.061):
    chk(abs(typed / 100 - fk) > ft, f'fix: {typed}% refused')
for wv, mine in ((0.000298, float(rel) / 2), (0.001192, float(rel) * 2)):
    chk(abs(wv - mine) < 1e-7 and abs(wv - fk) > 2 * ft, f'fix wrong {wv}')
# part 3
ratio = (F(1, 2 ** 24) / (P0 - P1)) / (F(1, 2 ** 25) / P0)
chk(ratio == 18850, 'ratio is exactly 2 * 0.9425 / 1e-4')
key(it, 3, float(ratio), 18850)
chk(abs(5.96e-4 / 3.16e-8 - 18861) < 1 and abs(5.96e-4 / 3.16e-8 - 18850) <= 12, 'part 3 from the printed figures, 5.96e-4 / 3.16e-8')
chk(abs(float(F(1, 2 ** 25) / P0) - 3.16e-8) < 5e-11, 'stated 3.16e-8')
kap = (P0 + P1) / (P0 - P1)
chk(kap == 18849, 'kappa of the subtraction 18,849')
wrong(it, 3, 'one-input', 9425)
wrong(it, 3, 'per-cent', 0.0596 / 3.16e-8, slack=1500)
chk(abs(math.log10(18850) - 4.3) < 0.05, 'log10 18,850 about 4.3')
# part 4
f_true = (P0 - P1) / (dl * P1)
chk(abs(float(f_true) - 0.03873) < 5e-6, 'f about 3.873%')
bp = float(f_true * rel) * 1e4
key(it, 4, bp, [0.23, round(0.03873 * 5.96e-4 * 1e4, 2)])
wrong(it, 4, 'eps', bp * 2)
wrong(it, 4, 'one-factor', bp / 2)

it = L1['p-moment-recurrence']
I = lambda n: mp.quad(lambda x: x ** n * mp.e ** (x - 1), [0, 1])
chk(abs(I(0) - (1 - mp.e ** -1)) < 1e-30, 'I_0')
for n in (1, 5, 18):
    chk(abs(I(n) - (1 - n * I(n - 1))) < 1e-25, f'recurrence at n = {n}')
    chk(I(n) < I(n - 1) and 1 / ((n + 1) * mp.e) < I(n) < mp.mpf(1) / (n + 1), f'I_{n} positive, falling, inside its bounds')
fwd = 1 - math.exp(-1)
for n in range(1, 19):
    fwd = 1 - n * fwd
true18 = float(I(18))
print(f'note: forward recurrence in doubles gives I_18 = {fwd:.6f}; true {true18:.7f}')
chk(abs(fwd - true18) > 0.01, 'forward run in doubles is noise at n = 18')
fac = math.factorial(18)
key(it, 1, math.log10(fac), 15.8)
wrong(it, 1, 'one-step', math.log10(18))
wrong(it, 1, 'sum', math.log10(sum(range(1, 19))))
u = 2.0 ** -53
key(it, 2, u * (1 - math.exp(-1)) * fac, [0.45, round(1.11e-16 * 0.632 * 6.40e15, 2)])
wrong(it, 2, 'eps', 2 * u * (1 - math.exp(-1)) * fac)
wrong(it, 2, 'no-i0', u * fac)
opts = W(it, 3)['options']
chk([o['id'] for o in opts if o.get('correct')] == ['ok'], 'part 3 keyed option is the unstable-recurrence one')
chk(abs(1 / (19 * math.e) - 0.019) < 5e-4 and abs(1 / 19 - 0.053) < 5e-4, 'part 3 stated bounds')
bound = lambda N: F(1, N + 1) * F(fac, math.factorial(N))
Nmin = next(N for N in range(19, 60) if bound(N) < F(1, 10 ** 10))
key(it, 4, Nmin, Nmin)
chk(abs(float(bound(24)) - 4.1e-10) < 5e-12 and abs(float(bound(25)) - 1.6e-11) < 5e-13, 'bounds at N = 24, 25')
wrong(it, 4, 'no-start', next(N for N in range(19, 60) if F(fac, math.factorial(N)) < F(1, 10 ** 10)))
wrong(it, 4, 'one-short', Nmin - 1)
b = F(0)
seq = {}
for n in range(25, 18, -1):
    b = (1 - b) / n
    seq[n - 1] = b
chk(seq[24] == F(1, 25) and seq[23] == F(1, 25) and abs(float(seq[22]) - 0.041739) < 5e-7, 'backward values I_24, I_23, I_22')
key(it, 5, float(seq[18]), 0.05012)
chk(abs(float(seq[18]) - true18) < 2e-11, 'backward I_18 good to about 1e-11')
wrong(it, 5, 'upper', 1 / 19)

it = L1['p-netting-sum']
gross, net, n = 2400 + 2394, 2400 - 2394, 2 ** 22
kappa = F(gross, net)
key(it, 1, float(kappa), 799)
wrong(it, 1, 'inflow', 2400 / 6)
wrong(it, 1, 'one', 1)
nu = F(n, 2 ** 53)
chk(nu == F(1, 2 ** 31) and abs(float(nu) - 4.66e-10) < 5e-13, 'nu = 2^-31')
b2 = float(kappa * nu)
key(it, 2, b2 * 1e7, 3.72)
wrong(it, 2, 'eps', 2 * b2 * 1e7)
wrong(it, 2, 'no-kappa', float(nu) * 1e7)
key(it, 3, b2 * 6e6, [2.23, round(3.72e-7 * 6e6, 2)])
wrong(it, 3, 'gross', 3.72e-7 * 4794e6)
wrong(it, 3, 'eps', 2 * b2 * 6e6)
chk(abs(float(nu) * 4794e6 - b2 * 6e6) < 1e-9, 'same figure as nu times the gross')
p4 = float(kappa) * 22 * u * 6e6
key(it, 4, p4 * 1e5, [1.17, round(799 * 22 * 1.11e-16 * 6e6 * 1e5, 2)])
wrong(it, 4, 'log10', float(kappa) * math.log10(n) * u * 6e6 * 1e5)
chk(4.5 < math.log10(n / 22) < 5.5, 'about five more digits')
# a real run: 2^22 cash flows with these totals, loop against math.fsum
rng = np.random.default_rng(7)
infl = rng.random(n // 2); infl *= 2400e6 / infl.sum()
outf = rng.random(n // 2); outf *= -2394e6 / outf.sum()
xs = np.concatenate([infl, outf]); rng.shuffle(xs)
exact = math.fsum(xs)
loop = float(np.cumsum(xs)[-1])
chk(abs(loop - exact) <= b2 * abs(exact) * 1.01 + 1e-9, 'a real loop sum stays inside the part 3 bound')

# ---------------------------------------------------------------- level 2
L2 = items(2)
it = L2['p-project-irr']
f = lambda v: 50 * v ** 3 + 40 * v ** 2 + 30 * v - 100
df = lambda v: 150 * v ** 2 + 80 * v + 30
ddf = lambda v: 300 * v + 80
chk(f(F(1, 2)) == F(-275, 4) and df(F(1, 2)) == F(215, 2) and f(1) == 20, 'f(0.5), f prime(0.5), f(1)')
n1 = F(1, 2) - f(F(1, 2)) / df(F(1, 2))
key(it, 1, float(n1), 1.1395)
wrong(it, 1, 'sign', float(F(1, 2) + f(F(1, 2)) / df(F(1, 2))))
mid = F(3, 4)
key(it, 2, float(f(mid)), -33.91)
wrong(it, 2, 'accepted', float(f(n1)))
wrong(it, 2, 'endpoint', 20)
wrong(it, 2, 'sign', -float(f(mid)))
n3 = mid - f(mid) / df(mid)
chk(n3 == F(17, 18) and df(mid) == F(1395, 8) and f(n3) > 0, 'step from 0.75 is 17/18, inside, f positive there')
key(it, 3, float(n3), 0.9444)
wrong(it, 3, 'sign', float(mid + f(mid) / df(mid)))
root = mp.findroot(lambda v: f(v), 0.92)
chk(abs(f(float(root))) < 1e-10 and len([r for r in np.roots([50, 40, 30, -100]) if abs(r.imag) < 1e-12]) == 1, 'one real root')
e0 = float(n3) - float(root)
C = float(ddf(root) / (2 * df(root)))
chk(abs(e0 - 0.026) < 5e-4 and abs(C - 0.77) < 5e-3, 'error 0.026 and C 0.77')
e, steps = 0.026, 0
while e >= 1e-12:
    e = 0.77 * e * e; steps += 1
key(it, 4, steps, steps)
v, real = mp.mpf(17) / 18, []
for _ in range(3):
    v = v - f(v) / df(v); real.append(float(abs(v - root)))
chk(real[1] > 1e-12 > real[2], 'real Newton: third step is the first below 1e-12')
chk(abs(real[0] - 5.1e-4) < 5e-6 and abs(real[1] - 2.0e-7) < 5e-9 and abs(real[2] - 3.2e-14) < 5e-16, 'real Newton errors as printed')
wrong(it, 4, 'one-short', steps - 1)
wrong(it, 4, 'bisect', next(k for k in range(1, 99) if (float(n3) - 0.75) / 2 ** k < 1e-12))
r = 1 / float(root) - 1
key(it, 5, r, [0.0890])
chk(W(it, 5).get('unit') == '%', 'IRR part has unit %')
wrong(it, 5, 'one-minus', 1 - float(root))
npv = -100 + 30 / (1 + r) + 40 / (1 + r) ** 2 + 50 / (1 + r) ** 3
chk(abs(npv) < 1e-9, 'NPV at the IRR is zero')

# fix pass: p-spread-spline was re-authored as p-vol-curve-extension (review finding 2); the reader's checks of the
# old problem are removed. The author's script recomputes the new problem; the delta reader checks it next.
chk('p-spread-spline' not in L2 and 'p-vol-curve-extension' in L2, 'set 2: p-spread-spline replaced by p-vol-curve-extension')

it = L2['p-survival-crossing']
co = np.polyfit([1, 3, 5], [0.98, 0.92, 0.84], 2)
p = lambda x: float(np.polyval(co, x)); dp = lambda x: float(np.polyval(np.polyder(co), x))
key(it, 1, p(4), 0.8825)
chk(abs(p(4) - (0.98 - 0.03 * 3 - 0.0025 * 3 * 1)) < 1e-12, 'printed Newton form')
wrong(it, 1, 'linear', 0.88)
s2 = 3 + (0.90 - 0.92) / (p(4) - 0.92)
key(it, 2, s2, 3.5333)
wrong(it, 2, 'linear', 3 + 0.02 / 0.04)
n3 = 3.5333 - (p(3.5333) - 0.9) / dp(3.5333)
key(it, 3, n3, 3.5499)
t3 = 3 + 0.02 / 0.0375  # unrounded secant point, the author's route
chk(abs(p(t3) - 0.900622) < 5e-7 and abs(dp(t3) + 0.037667) < 5e-7 and abs((p(t3) - 0.9) / -dp(t3) - 0.016519) < 5e-7, 'p, slope and step at 3.53333')
# fix pass: the feedback now works from the restated 3.5333 (finding 7; 0.900624 of the review's text corrected to 0.9006235)
fb3 = json.dumps(it['parts'][2], ensure_ascii=False)
chk('0.9006235' in fb3 and '0.016553' in fb3 and '0.016519' not in fb3 and '0.000622 ' not in fb3, 'p-survival-crossing part 3: feedback and explain state 0.9006235 and 0.016553 (finding 7)')
chk(round(3.5333 + 0.016553, 4) == 3.5499 and abs(p(3.5333) - 0.9006235) < 5e-8 and abs((p(3.5333) - 0.9) / -dp(3.5333) - 0.016553) < 5e-7
    and abs(0.0006235 / 0.037667 - 0.016553) < 5e-7, 'fix of finding 7: 0.9006235, 0.016553, sum 3.5499')
wrong(it, 3, 'sign', t3 + (p(t3) - 0.9) / dp(t3))
slip = 3.5333 + (p(3.5333) - 0.9) / dp(3.5333)
ws = [x for x in W(it, 3)['wrong'] if x['id'] == 'sign'][0]
chk(abs(round(slip, 4) - ws['value']) <= ws['tol']['abs'],
    f'p-survival-crossing part 3 wrong sign: from the restated 3.5333 the slip types {round(slip, 4)}, outside {ws["value"]} +- {ws["tol"]["abs"]} (review finding 8)')
chk(all(abs(v - 3.51678) <= 1e-4 for v in (round(slip, 4), 3.5168, 3.516814)) and abs(3.51678 - 3.549853) > 2e-4, 'fix of finding 8: value 3.51678 tol 0.0001')
ex = -4 + math.sqrt(57)
chk(abs(p(ex) - 0.9) < 1e-12 and abs(ex - n3) < 2e-5, 'exact crossing -4 + sqrt 57 within 2e-5')
prod = lambda x: abs((x - 1) * (x - 3) * (x - 5))
key(it, 4, 0.0006 / 6 * prod(3.5499) * 1e4, [2.03])
wrong(it, 4, 'no-factorial', 0.0006 * prod(n3) * 1e4, slack=0.006)
wrong(it, 4, 'fourth', 0.0006 / 24 * prod(n3) * 1e4, slack=0.006)
chk(abs(dp(n3) + 0.03775) < 5e-6, 'slope at t* is -0.03775')
days_full = 0.0006 / 6 * prod(n3) / abs(dp(n3)) * 365
chk('2.033 \\times 10^{-4}' in it['parts'][4]['question'] and '2.03 \\times' not in (it['parts'][4]['question'] + it['parts'][4]['feedback']['correct'] + it['parts'][4]['explain']['text']),
    'p-survival-crossing part 5: question, feedback and explain restate 2.033e-4 (finding 6)')
days_restated = 2.033e-4 / 0.03775 * 365
key(it, 5, days_full, [round(days_restated, 2), days_restated])
chk(round(2.033e-4 / 0.03775, 5) == 0.00539 and round(2.033e-4 / 0.03775 * 365, 2) == 1.97, 'fix: restating 2.033e-4 gives 0.00539 and 1.97')
wrong(it, 5, 'p-at-3', 0.0006 / 6 * prod(n3) / 0.035 * 365)
wrong(it, 5, 'no-slope', 0.0006 / 6 * prod(n3) * 365)

# ---------------------------------------------------------------- level 3
L3 = items(3)
it = L3['p-normal-cdf-quadrature']
g = lambda x: math.exp(-x * x / 2)
Iex = float(mp.sqrt(2 * mp.pi) * (mp.ncdf(1) - mp.mpf(1) / 2))
chk(abs(Iex - 0.8556244) < 5e-8 and abs(g(0.5) - 0.882497) < 5e-7 and abs(g(1) - 0.606531) < 5e-7, 'prose figures')
T1 = 0.5 * (g(0) + g(1)); T2 = 0.25 * (g(0) + 2 * g(0.5) + g(1))
key(it, 1, T2, 0.8429)
wrong(it, 1, 'one-strip', T1); wrong(it, 1, 'no-half', 0.5 * (g(0) + g(0.5) + g(1)))
chk(abs(Iex - T2 - 0.0127) < 5e-5, 'T_2 is 0.0127 below I')
simpson = (g(0) + 4 * g(0.5) + g(1)) / 6
key(it, 2, simpson, [0.8561, round((4 * 0.8429 - 0.8033) / 3, 4)])
chk(abs((4 * T2 - T1) / 3 - simpson) < 1e-15 and abs(simpson - Iex - 0.00046) < 5e-6, 'Richardson is Simpson; error 0.00046')
wrong(it, 2, 'swap', (4 * T1 - T2) / 3); wrong(it, 2, 'order-one', 2 * T2 - T1)
xs2, ws2 = np.polynomial.legendre.leggauss(2)
G2 = float(sum(0.5 * w * g(0.5 + 0.5 * x) for x, w in zip(xs2, ws2)))
key(it, 3, G2, 0.8553)
chk(abs(G2 - Iex + 0.00031) < 5e-6 and abs(G2 - Iex) < abs(simpson - Iex), 'Gauss error 0.00031, below Simpson')
wrong(it, 3, 'no-factor', 2 * G2); wrong(it, 3, 'unmapped', 2 * g(1 / math.sqrt(3)))
Phi = 0.5 + G2 / math.sqrt(2 * math.pi)
key(it, 4, Phi, [0.8412, round(0.5 + 0.8553 / 2.506628, 4)])
wrong(it, 4, 'no-half', Phi - 0.5); wrong(it, 4, 'two-pi', 0.5 + G2 / (2 * math.pi))
chk(abs(float(mp.ncdf(1)) - 0.841345) < 5e-7 and abs(float(mp.ncdf(1)) - Phi - 1.2e-4) < 5e-6, 'library value and error')
xs3, ws3 = np.polynomial.legendre.leggauss(3)
G3 = float(sum(0.5 * w * g(0.5 + 0.5 * x) for x, w in zip(xs3, ws3)))
chk(abs(0.5 + G3 / math.sqrt(2 * math.pi) - float(mp.ncdf(1))) < 1e-6,
    f'p-normal-cdf-quadrature part 4 explain: three-node error in Phi(1) is {abs(0.5 + G3 / math.sqrt(2 * math.pi) - float(mp.ncdf(1))):.2e}, '
    'claimed below 1e-6')

# fix pass: p-stiff-credit-trapezoid was re-authored as p-implicit-newton-step (review finding 3); the reader's checks
# of the old problem are removed, and with them the order-one check of note N1. The delta reader checks the new problem.
chk('p-stiff-credit-trapezoid' not in L3 and 'p-implicit-newton-step' in L3, 'set 3: p-stiff-credit-trapezoid replaced by p-implicit-newton-step')

it = L3['p-rate-path-euler']
def euler(nst):
    hh, P = F(4, nst), F(1)
    for k in range(nst):
        P *= 1 - hh * (F(2, 100) + F(1, 100) * k * hh)
    return float(P)
E4, E8, E16 = euler(4), euler(8), euler(16)
chk(abs(E4 - 0.866947) < 5e-7 and abs(E8 - 0.859366) < 5e-7 and abs(E16 - 0.855710) < 5e-7, 'Euler values in the prose')
g1, g2 = 0.866947 - 0.859366, 0.859366 - 0.855710
key(it, 1, math.log2(g1 / g2), 1.05)
wrong(it, 1, 'ratio', g1 / g2); wrong(it, 1, 'flip', math.log2(g2 / g1))
key(it, 2, g2, 0.003656)
wrong(it, 2, 'p-two', g2 / 3); wrong(it, 2, 'sign', -g2)
exactP = math.exp(-(0.02 * 4 + 0.005 * 16))
chk(abs(E16 - exactP - 0.00357) < 5e-6, 'true error of the 16-step value')
key(it, 3, 0.855710 - g2, 0.852054)
wrong(it, 3, 'added', 0.855710 + g2); wrong(it, 3, 'p-two', 0.855710 - round(g2 / 3, 6))
chk(abs(0.852054 - exactP) < 1e-4 and abs(abs(0.852054 - exactP) - 9e-5) < 5e-6, 'Richardson within 1e-4, off by 9e-5')
Ce = 0.003656 / 0.25
ne = next(k for k in range(5000, 7000) if Ce * 4 / k <= 1e-5)
key(it, 4, ne, ne)
wrong(it, 4, 'floor', ne - 1)
C2 = 0.003656 / 0.25 ** 2
wrong(it, 4, 'p-two', next(k for k in range(1, 9999) if C2 * (4 / k) ** 2 <= 1e-5))
chk(abs(euler(ne) - exactP) < 1.05e-5, 'a real 5,850-step Euler run is at the tolerance')
key(it, 5, exactP, 0.852144)
chk(abs(0.5 * 4 * (0.02 + 0.06) - 0.16) < 1e-15, 'one strip gives 0.16')
wrong(it, 5, 'no-exp', 1 - 0.16); wrong(it, 5, 'no-minus', math.exp(0.16)); wrong(it, 5, 'left-end', math.exp(-0.08))

# ---------------------------------------------------------------- shape
lessons = {1: {'nm-float', 'nm-stability'}, 2: {'nm-roots'}, 3: {'nm-quadrature', 'nm-stability'}}
for lv, L in ((1, L1), (2, L2), (3, L3)):
    chk(3 <= len(L) <= 5, f'set {lv}: three to five problems')
    chk(any(x['difficulty'] == 5 for x in L.values()), f'set {lv}: one problem of difficulty 5')
    typed = total = 0
    for x in L.values():
        chk(3 <= len(x['parts']) <= 5 and 3 <= x['difficulty'] <= 5, f"{x['id']}: parts and difficulty in range")
        chk(set(x['skills']) <= lessons[lv], f"{x['id']}: skills from the level")
        for p in x['parts']:
            total += 1
            typed += p['widget']['kind'] in ('numeric', 'expression')
            chk(len([s for s in p['explain']['text'].replace('e.g.', '').split('. ') if s.strip()]) <= 3,
                f"{x['id']}: explain of at most three sentences: {p['explain']['text'][:40]}")
    chk(typed * 3 >= total * 2, f'set {lv}: two thirds typed')

print(f'{n_checks} checks, {len(findings)} FINDING line(s)')
sys.exit(0)
