#!/usr/bin/env python3
"""Delta read review-delta-ag-pdes: pdes problem sets after the re-author and fix pass.

Scope: problems-3 (all of it, new), and the parts the fix pass changed on
problems-1 (p-grid-rod part 4, p-drift-walk wording) and problems-2
(p-grid-modes parts 1, 3, 4; p-exp-series parts 2 and 5).

Imports no earlier script. math and numpy only: no SciPy, no root finder
that can fail to converge. Each key is rebuilt by two routes at full
precision, then the band is fed what a learner types when the printed
rounded values are carried forward, at the rounding the part asks for.

Exit 0 always. A failing check prints a FINDING line.
"""
import json
import math
import os
import re

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PDES = os.path.join(ROOT, 'app', 'content', 'courses', 'pdes')

checks = 0
findings = 0


def check(name, cond, detail=''):
    global checks, findings
    checks += 1
    if not cond:
        findings += 1
        print('FINDING %s %s' % (name, detail))


def close(a, b, tol):
    return abs(a - b) <= tol


def load(n):
    with open(os.path.join(PDES, 'problems-%d.json' % n), encoding='utf-8') as f:
        d = json.load(f)
    return {i['id']: i for i in d['items']}


def Phi(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def Phi_inv(p):
    """Bisection on erf: always converges, no library solver."""
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if Phi(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def rnd(x, places):
    """Round half away from zero on the decimal string, as a learner does."""
    q = 10 ** places
    return math.floor(abs(x) * q + 0.5 + 1e-9) / q * (1 if x >= 0 else -1)


def typed(x, places, pct=False):
    """The value the engine compares when a learner types x at the asked places."""
    if pct:
        return rnd(x * 100, places) / 100.0
    return rnd(x, places)


def in_band(w, v):
    tol = w.get('tol', {}).get('abs', 0)
    return abs(v - w['answer']) <= tol + 1e-12


def slip_hit(w, v):
    hits = []
    for s in w.get('wrong', []):
        if 'value' in s and abs(v - s['value']) <= s.get('tol', {}).get('abs', 0) + 1e-12:
            hits.append(s['id'])
    return hits


def band_checks(tag, w, exact, carried, places, pct=False, slips=None):
    """Key by two routes, the typed forms taken, slips refused by the key and routed."""
    check(tag + ' key equals exact', close(w['answer'], exact, w['tol']['abs']),
          'key %r exact %r' % (w['answer'], exact))
    for label, v in (('exact', exact), ('carried', carried)):
        t = typed(v, places, pct)
        check(tag + ' band takes typed ' + label, in_band(w, t), 'typed %r key %r tol %r' % (t, w['answer'], w['tol']['abs']))
        # no rounding tie: the unrounded value is clear of a half unit at the asked place
        scaled = (v * 100 if pct else v) * 10 ** places
        frac = abs(scaled) - math.floor(abs(scaled))
        check(tag + ' no tie ' + label, abs(frac - 0.5) > 1e-6, 'value %r' % v)
    stored = {s['id']: s for s in w.get('wrong', [])}
    for sid, val in (slips or {}).items():
        check(tag + ' slip %s present' % sid, sid in stored)
        if sid not in stored:
            continue
        s = stored[sid]
        check(tag + ' slip %s value' % sid, close(s['value'], val, s['tol']['abs']),
              'stored %r mine %r' % (s['value'], val))
        t = typed(val, places, pct)
        check(tag + ' slip %s typed is routed' % sid, sid in slip_hit(w, t), 'typed %r' % t)
        check(tag + ' slip %s refused by key' % sid, not in_band(w, t), 'typed %r' % t)
    check(tag + ' slips all rebuilt', set(stored) == set(slips or {}), '%r' % sorted(stored))
    # bands do not overlap
    for s in w.get('wrong', []):
        gap = abs(s['value'] - w['answer']) - s['tol']['abs'] - w['tol']['abs']
        check(tag + ' slip %s band clear of key band' % s['id'], gap > 0, 'gap %r' % gap)


def printed(tag, text, value, shown):
    """A printed figure appears in the text and equals the value at its places."""
    places = len(shown.split('.')[1]) if '.' in shown else 0
    check(tag + ' prints ' + shown, shown in text, 'not in text')
    check(tag + ' printed %s is the value' % shown, abs(rnd(value, places) - float(shown.replace(',', ''))) < 0.5 * 10 ** -places + 1e-12,
          'value %r' % value)


def alltext(part):
    out = [part.get('question', '')]
    fb = part.get('feedback', {})
    out += [fb.get('correct', ''), fb.get('generic', '')] + list(fb.get('byKey', {}).values())
    out.append(part.get('explain', {}).get('text', ''))
    return ' '.join(out)


# --------------------------------------------------------------------------
# Level 3
# --------------------------------------------------------------------------
L3 = load(3)

# ---- p-straddle-vol ------------------------------------------------------
it = L3['p-straddle-vol']
P = it['parts']
K, S0, T, straddle = 80.0, 80.0, 0.75, 9.60
check('straddle prose numbers', all(s in it['prose'] for s in ('80', 'nine months', '9.60', 'r = 0')))

# part 1: the argument at x = 0, a = 1/2 is sqrt(tau/2); tested at several tau
w = P[0]['widget']


def tex_eval(tex, tau):
    s = tex.replace('\\tau', '(T)')
    for _ in range(6):
        s = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
        s = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', s)
    s = s.replace('2(T)', '2*(T)')
    return eval(s, {'sqrt': math.sqrt, 'T': tau})


for tau in (0.004, 0.0113, 0.3, 2.0):
    arg = (0.0 + 2 * 0.5 * tau) / math.sqrt(2 * tau)
    check('straddle p1 key at tau=%g' % tau, close(tex_eval(w['answer'], tau), arg, 1e-12))
    for a in w['accept']:
        check('straddle p1 accept %s' % a, close(tex_eval(a, tau), arg, 1e-12))
    for s in w['wrong']:
        check('straddle p1 slip %s differs' % s['id'], not close(tex_eval(s['tex'], tau), arg, 1e-9))
    check('straddle p1 slip no-half is a = 1', close(tex_eval(w['wrong'][0]['tex'], tau), 2 * tau / math.sqrt(2 * tau), 1e-12))
    check('straddle p1 slip numerator', close(tex_eval(w['wrong'][1]['tex'], tau), tau, 1e-12))
    # no-root: divided by 2 tau, not its root
    check('straddle p1 slip no-root', close(tex_eval(w['wrong'][2]['tex'], tau), tau / (2 * tau), 1e-12))

# the claim C = K(2 Phi(sqrt(tau/2)) - 1) at r = 0, S = K: by the lemma with
# alpha = 1/2, beta = -1/4, and by the usual formula
for tau in (0.0113311, 0.02, 0.2):
    def lemma(a, x=0.0):
        return math.exp(a * x + a * a * tau) * Phi((x + 2 * a * tau) / math.sqrt(2 * tau))
    u = lemma(0.5) - lemma(-0.5)
    c_heat = K * math.exp(-0.25 * tau) * u
    c_claim = K * (2 * Phi(math.sqrt(tau / 2)) - 1)
    sT = math.sqrt(2 * tau)                     # sigma sqrt(T)
    c_bs = S0 * Phi(sT / 2) - K * Phi(-sT / 2)
    check('straddle call form, lemma, tau=%g' % tau, close(c_heat, c_claim, 1e-12))
    check('straddle call form, Black-Scholes, tau=%g' % tau, close(c_bs, c_claim, 1e-12))
    # the start e^{y/2} - e^{-y/2} by quadrature against the kernel
    y = np.linspace(0.0, 6.0, 600001)
    f = (np.exp(0.5 * y) - np.exp(-0.5 * y)) * np.exp(-y * y / (4 * tau)) / math.sqrt(4 * math.pi * tau)
    quad = float(np.sum((f[1:] + f[:-1]) * 0.5) * (y[1] - y[0]))
    check('straddle call form, kernel integral, tau=%g' % tau, close(K * math.exp(-0.25 * tau) * quad, c_claim, 1e-7))

# lesson 10 q-arg has the same slip with the same line (review finding 6)
with open(os.path.join(PDES, 'l10-formula-from-the-kernel.json'), encoding='utf-8') as f:
    qa = {i['id']: i for i in json.load(f)['quiz']}.get('q-arg')
if qa:
    a = P[0]['feedback']['byKey']['no-root']
    b = qa['feedback']['byKey'].get('no-root', '')
    check('straddle p1 no-root line is not the q-arg line retold (review finding 6)',
          not ('You divided by $2\\tau' in a and 'You divided by $2\\tau' in b and 'its square root' in a and 'its square root' in b),
          'set: "%s" | quiz: "%s"' % (a, b))

# part 2
phi_key = (straddle / 2 / K + 1) / 2
band_checks('straddle p2', P[1]['widget'], phi_key, (4.80 / 80 + 1) / 2, 4,
            slips={'whole': (straddle / K + 1) / 2, 'c-over-k': straddle / 2 / K})
printed('straddle p2', alltext(P[1]), straddle / 2, '4.80')
printed('straddle p2', alltext(P[1]), straddle / 2 / K, '0.06')

# part 3: table value, then tau
zq = Phi_inv(0.53)
check('straddle table value 0.07527', abs(rnd(zq, 5) - 0.07527) < 1e-12, 'mine %r' % zq)
check('straddle p3 question prints the table value', '0.07527' in P[2]['question'])
tau_exact = 2 * zq * zq
tau_carried = 2 * 0.07527 ** 2
band_checks('straddle p3', P[2]['widget'], tau_exact, tau_carried, 5,
            slips={'unsquared': 2 * 0.07527, 'halved': 0.07527 ** 2 / 2, 'no-two': 0.07527 ** 2})
# carried forms a learner can reach: squaring first and rounding to 0.0056656 or 0.005666
for sq in (0.0056656, 0.005666):
    t = typed(2 * sq, 5)
    check('straddle p3 takes 2 x %r' % sq, in_band(P[2]['widget'], t), 'typed %r' % t)
printed('straddle p3', alltext(P[2]), 0.07527 ** 2, '0.0056656')
printed('straddle p3', alltext(P[2]), tau_carried, '0.01133')

# part 4
sig_exact = math.sqrt(2 * tau_exact / T)
sig_carried = math.sqrt(2 * 0.01133 / T)
band_checks('straddle p4', P[3]['widget'], sig_exact, sig_carried, 2, pct=True,
            slips={'no-half': math.sqrt(0.01133 / T), 'calendar': math.sqrt(2 * 0.01133), 'no-root': 2 * 0.01133 / T})
check('straddle p4 unit', P[3]['widget'].get('unit') == '%')
# the printed working line, carried with its own rounded figures
t = typed(math.sqrt(0.030213), 2, pct=True)
check('straddle p4 takes sqrt(0.030213)', in_band(P[3]['widget'], t), 'typed %r' % t)
printed('straddle p4', alltext(P[3]), 2 * 0.01133, '0.02266')
printed('straddle p4', alltext(P[3]), 0.02266 / 0.75, '0.030213')
printed('straddle p4', alltext(P[3]), sig_carried, '0.1738')
# the closing claim: priced at 17.38% the straddle comes back at 9.60
sT = 0.1738 * math.sqrt(T)
back = 2 * (S0 * Phi(sT / 2) - K * Phi(-sT / 2))
check('straddle priced back at 17.38% is 9.60', abs(rnd(back, 2) - 9.60) < 1e-9, 'gives %r' % back)
# second route for the whole chain: bisect the Black-Scholes straddle for sigma
lo, hi = 0.01, 1.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    v = 2 * (S0 * Phi(mid * math.sqrt(T) / 2) - K * Phi(-mid * math.sqrt(T) / 2))
    lo, hi = (mid, hi) if v < straddle else (lo, mid)
check('straddle implied vol by bisection on the formula', close(0.5 * (lo + hi), sig_exact, 1e-10), '%r' % lo)
check('straddle key p4 against bisection', close(P[3]['widget']['answer'], 0.5 * (lo + hi), 6e-5))

# ---- p-log-contract ------------------------------------------------------
it = L3['p-log-contract']
P = it['parts']
sig, r, T, K = 0.28, 0.02, 1.5, 64.0
k = 2 * r / sig ** 2
tau = 0.5 * sig ** 2 * T
check('log prose numbers', all(s in it['prose'] for s in ('64', '28', '2\\%', '1.5', '1{,}000')) or
      all(s in it['prose'] for s in ('64', '28', '1.5')))

# part 1: residual of the trial v = e^{-k tau}(x + c tau) by finite differences
def resid(c, kk, x, t, h=1e-4):
    v = lambda xx, tt: math.exp(-kk * tt) * (xx + c * tt)
    vt = (v(x, t + h) - v(x, t - h)) / (2 * h)
    vx = (v(x + h, t) - v(x - h, t)) / (2 * h)
    vxx = (v(x + h, t) - 2 * v(x, t) + v(x - h, t)) / (h * h)
    return vt - (vxx + (kk - 1) * vx - kk * v(x, t))


w = P[0]['widget']
for kk in (0.3, k, 2.5):
    for (x, t) in ((0.0, 0.05), (0.4, 0.2), (-0.7, 1.1)):
        check('log p1 c = k - 1 solves, k=%.3g' % kk, abs(resid(kk - 1, kk, x, t)) < 1e-6)
        for c_bad, sid in ((1 - kk, 'sign'), (kk, 'no-minus'), (kk + 1, 'plus')):
            check('log p1 slip %s does not solve' % sid, abs(resid(c_bad, kk, x, t)) > 1e-3)
check('log p1 key text', w['answer'].replace(' ', '') == 'k-1')
check('log p1 slips', [s['tex'] for s in w['wrong']] == ['1-k', 'k', 'k+1'])

# part 2: value by the heat form and by the expectation in calendar terms
v_heat = 1000 * math.exp(-k * tau) * (k - 1) * tau
v_cal = 1000 * math.exp(-r * T) * (r - 0.5 * sig ** 2) * T
check('log p2 two routes agree', close(v_heat, v_cal, 1e-10))
# third route: Gauss-Hermite style quadrature of the discounted payoff
z = np.linspace(-10, 10, 400001)
dens = np.exp(-z * z / 2) / math.sqrt(2 * math.pi)
lnST = (r - 0.5 * sig ** 2) * T + sig * math.sqrt(T) * z
quad = float(np.sum((lnST * dens)[1:] + (lnST * dens)[:-1]) * 0.5 * (z[1] - z[0]))
check('log p2 quadrature', close(1000 * math.exp(-r * T) * quad, v_heat, 1e-7))
v_carried = 1000 * 0.97045 * (-0.0288)
band_checks('log p2', P[1]['widget'], v_heat, v_carried, 2,
            slips={'no-disc': 1000 * (k - 1) * tau, 'used-k': 1000 * 0.97045 * 0.03, 'sign': -v_heat})
# a learner who carries k = 0.5102 and tau = 0.0588
kc = 0.5102
t = typed(1000 * math.exp(-kc * 0.0588) * (kc - 1) * 0.0588, 2)
check('log p2 takes k = 0.5102 carried', in_band(P[1]['widget'], t), 'typed %r' % t)
txt = alltext(P[1])
printed('log p2', txt, k, '0.5102')
printed('log p2', txt, tau, '0.0588')
printed('log p2', txt, (k - 1) * tau, '-0.0288')
printed('log p2', txt, math.exp(-k * tau), '0.97045')
printed('log p2', txt, -v_heat, '27.95')
check('log p2 k tau = 0.03', close(k * tau, 0.03, 1e-12))

# part 3: break-even rise
x_be = -(k - 1) * tau                       # exact: x + (k-1)tau = 0
rise_exact = math.exp(x_be) - 1
x_car = 27.95 / 970.45
rise_car = math.exp(x_car) - 1
band_checks('log p3', P[2]['widget'], rise_exact, rise_car, 2, pct=True,
            slips={'log-return': 0.0288, 'no-disc': math.exp(27.95 / 1000) - 1})
check('log p3 unit', P[2]['widget'].get('unit') == '%')
txt = alltext(P[2])
printed('log p3', txt, 1000 * math.exp(-k * tau), '970.45')
printed('log p3', txt, x_car, '0.028801')
printed('log p3', txt, math.exp(0.028801), '1.02922')
printed('log p3', txt, 64 * math.exp(0.0288), '65.87')
# the claim is worth 0 there, by the value formula
check('log p3 value is 0 at the break-even', abs(1000 * math.exp(-k * tau) * (x_be + (k - 1) * tau)) < 1e-12)

# part 4: chance of a positive payoff under the Feynman-Kac walk
mean, var = (k - 1) * tau, 2 * tau
check('log p4 variance 2 tau = sigma^2 T', close(var, sig ** 2 * T, 1e-14) and close(var, 0.1176, 1e-12))
sd = math.sqrt(var)
zz = -mean / sd
p_exact = 1 - Phi(zz)
d2 = (math.log(64 / 64) + (r - 0.5 * sig ** 2) * T) / (sig * math.sqrt(T))
check('log p4 equals Phi(d2)', close(p_exact, Phi(d2), 1e-14))
check('log p4 given Phi(0.0840) = 0.5335', abs(rnd(Phi(0.0840), 4) - 0.5335) < 1e-12)
p_car = 1 - 0.5335
band_checks('log p4', P[3]['widget'], p_exact, p_car, 4,
            slips={'wrong-side': 0.5335, 'no-drift': 0.5})
txt = alltext(P[3])
printed('log p4', txt, sd, '0.34293')
printed('log p4', txt, 0.0288 / 0.34293, '0.0840')
printed('log p4', txt, p_car, '0.4665')
check('log p4 band refuses 0.4666, which no route gives (review finding 7)', not in_band(P[3]['widget'], 0.4666) and
      abs(0.4666 - P[3]['widget']['answer']) > P[3]['widget']['tol']['abs'],
      'key %r tol %r: 0.4666 is taken by a float margin; the exact value is %.6f' % (P[3]['widget']['answer'], P[3]['widget']['tol']['abs'], p_exact))
# the walk the question describes: drift k - 1, variance 2 per unit heat time, by simulation-free moments
check('log p4 mean is minus the log return of part 3', close(mean, -0.0288, 1e-12))
# the chance is the pricing walk's (drift r). The question must say so: lesson 10 q-d2 marks
# "the real-world chance" as the wrong reading of Phi(d2).
q4 = P[3]['question'] + ' ' + P[3]['explain']['text']
check('log p4 names the chance as risk-neutral (review finding 1)',
      re.search(r'risk-neutral|pricing walk|pricing measure', q4) is not None,
      'question asks for "the chance that the claim pays a positive amount" with no measure named; '
      'under a real drift of 8%% the chance is %.4f, not %.4f' % (1 - Phi(-((0.08 - 0.5 * sig ** 2) * T) / sd), p_exact))

# ---- p-grid-budget -------------------------------------------------------
it = L3['p-grid-budget']
P = it['parts']


def cn_price(S, K, r, sigma, T, nx, nt, L=1.0):
    """My own Crank-Nicolson solve of u_tau = u_xx on [-L, L]: dense matrices, numpy.linalg.solve.
    Left edge 0, right edge the exact large-S value, as the course's lesson 12 states the scheme."""
    k = 2 * r / sigma ** 2
    a1, a2 = (k + 1) / 2, (k - 1) / 2
    tau_end = 0.5 * sigma ** 2 * T
    x = np.linspace(-L, L, nx + 1)
    h = 2 * L / nx
    dt = tau_end / nt
    lam = dt / (h * h)
    n = nx - 1
    A = np.zeros((n, n))
    B = np.zeros((n, n))
    i = np.arange(n)
    A[i, i] = 1 + lam
    B[i, i] = 1 - lam
    A[i[:-1], i[:-1] + 1] = -lam / 2
    A[i[1:], i[1:] - 1] = -lam / 2
    B[i[:-1], i[:-1] + 1] = lam / 2
    B[i[1:], i[1:] - 1] = lam / 2
    Ainv_B = np.linalg.solve(A, B)
    Ainv_e = np.linalg.solve(A, np.eye(n)[:, -1])
    edge = lambda t: math.exp(a1 * L + a1 * a1 * t) - math.exp(a2 * L + a2 * a2 * t)
    u = np.maximum(np.exp(a1 * x) - np.exp(a2 * x), 0.0)[1:-1]
    t = 0.0
    for _ in range(nt):
        u = Ainv_B @ u + Ainv_e * (lam / 2) * (edge(t) + edge(t + dt))
        t += dt
    mid = n // 2                                  # x = 0 is a node for even nx
    assert abs(x[1:-1][mid]) < 1e-12
    x0 = math.log(S / K)
    return K * math.exp(-a2 * x0 - a1 * a1 * tau_end) * float(u[mid])


def bs_call(S, K, r, sigma, T):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return S * Phi(d1) - K * math.exp(-r * T) * Phi(d1 - sigma * math.sqrt(T))


# calibration against the two prices lesson 12 prints for its own option
check('solver gives lesson 12 price on 100', close(cn_price(100, 100, 0.05, 0.2, 1, 100, 20), 10.4427214, 5e-8))
check('solver gives lesson 12 price on 200', close(cn_price(100, 100, 0.05, 0.2, 1, 200, 40), 10.4486123, 5e-8))

opt = (120.0, 120.0, 0.045, 0.18, 1.25)
check('grid prose numbers', all(s in it['prose'] for s in ('120', '4.5', '18', '1.25', '[-1, 1]', 'n_x/5')))
# Session AH: parts 1 and 2 of p-grid-budget were re-authored (finding 4: a constant C h^2 fitted from runs on 200
# and 300 intervals), and parts 3 and 4 moved with them. The checks below are of the version this read saw and run
# only while it is in the file; the author's script problems-pdes-numbers.py checks the new parts by two solvers.
OLDGRID = '12.9896396' in it['prose']
if OLDGRID:
    V = {}
    for nx, shown in ((100, '12.9896396'), (200, '12.9963192'), (400, '12.9979920')):
        V[nx] = cn_price(*opt, nx, nx // 5)
        check('grid price on %d is %s' % (nx, shown), abs(rnd(V[nx], 7) - float(shown)) < 1e-12 and shown in it['prose'],
              'mine %.9f' % V[nx])
    V[800] = cn_price(*opt, 800, 160)
    V[1600] = cn_price(*opt, 1600, 320)
    bs = bs_call(*opt)
    check('grids converge on the formula', abs(V[1600] - bs) < 5e-5, 'V1600 %.7f formula %.7f' % (V[1600], bs))

    # part 1
    d1f, d2f = V[200] - V[100], V[400] - V[200]
    d1p, d2p = 12.9963192 - 12.9896396, 12.9979920 - 12.9963192
    p_exact = math.log2(d1f / d2f)
    p_car = math.log2(3.993)
    band_checks('grid p1', P[0]['widget'], p_exact, p_car, 1,
                slips={'ratio': d1p / d2p, 'inverted': math.log2(d2p / d1p)})
    txt = alltext(P[0])
    printed('grid p1', txt, d1p, '0.0066796')
    printed('grid p1', txt, d2p, '0.0016728')
    printed('grid p1', txt, d1p / d2p, '3.993')
    check('grid p1 claim: differences shrink by 2^p when the error is c h^p',
          close((1 - 2 ** -2.0) / (2 ** -2.0 - 2 ** -4.0), 4.0, 1e-12))

    # part 2: a third of the last step, by the series and by the limit of my own grids
    short_car = d2p / 3
    series = d2p * sum(0.25 ** j for j in range(1, 60))
    check('grid p2 series is a third', close(series, short_car, 1e-15))
    band_checks('grid p2', P[1]['widget'], d2f / 3 * 1e6, short_car * 1e6, 1,
                slips={'difference': d2p * 1e6, 'quarter': d2p / 4 * 1e6})
    # the claim itself: the limit of the grids, from two further halvings and their own tail
    # the limit of the grids is the formula's price: a wider domain moves nothing, so there is no truncation term
    limit = bs
    check('grid limit by Richardson on 800 and 1,600 is the formula to 3e-6', abs(V[1600] + (V[1600] - V[800]) / 3 - bs) < 3e-6)
    true400, true1600 = (limit - V[400]) * 1e6, (limit - V[1600]) * 1e6
    check('grid true shortfalls are 564.4 and 37.2', close(true400, 564.4, 0.05) and close(true1600, 37.2, 0.05),
          '%.2f %.2f' % (true400, true1600))
    check('grid observed order slips below 2 on finer grids',
          (V[400] - V[200]) / (V[800] - V[400]) < d1f / d2f and (V[800] - V[400]) / (V[1600] - V[800]) < (V[400] - V[200]) / (V[800] - V[400]))
    t2 = P[1]['question'] + ' ' + P[1]['feedback']['correct'] + ' ' + P[1]['explain']['text']
    check('grid p2 states 557.6 as an estimate (review finding 2)', re.search(r'about|estimate|predict', t2) is not None,
          'feedback says "the 400 price is ... 557.6 x 10^-6 below the limit"; this pricer is %.1f below it (%.1f%% more)'
          % (true400, 100 * (true400 / 557.6 - 1)))
    printed('grid p2', alltext(P[1]), short_car * 1e6, '557.6')

    # part 3: 16 times the work is two halvings
    check('grid p3 work is nx * nt = nx^2 / 5', (1600 * 320) == 16 * (400 * 80))
    FIXED3 = close(P[2]['widget']['answer'], 89.216, 0.01)      # the review's replacement: 6.25 times the work
    if FIXED3:
        s3_car = 557.6 / 6.25
        band_checks('grid p3', P[2]['widget'], d2f / 3 / 6.25 * 1e6, s3_car, 2,
                    slips={'per-interval': 557.6 / 6.25 ** 2, 'first-order': 557.6 / 2.5})
    else:
        s3_car = 557.6 / 16
        band_checks('grid p3', P[2]['widget'], d2f / 3 / 16 * 1e6, s3_car, 2,
                    slips={'one-halving': 557.6 / 4, 'per-interval': 557.6 / 256})
    t3 = alltext(P[2])
    check('grid p3 states its answer as a prediction (review finding 2)', re.search(r'about|estimate|predict', t3) is not None,
          'feedback says the shortfall on 1,600 intervals is 34.85 x 10^-6; the 1,600 run is %.1f below the limit (%.1f%% more)'
          % (true1600, 100 * (true1600 / 34.85 - 1)))
    # homework-3 h-sequence: the 400 error, two halvings, divided by 16, on 1,600 intervals (review finding 3)
    with open(os.path.join(PDES, 'homework-3.json'), encoding='utf-8') as f:
        hw = {i['id']: i for i in json.load(f)['items']}
    hs = hw.get('h-sequence')
    if hs:
        a = P[2]['feedback']['correct']
        b = hs['feedback']['correct']
        same = ('two halvings' in a.lower() and 'two halvings' in b.lower() and '1,600' in a and '1,600' in hs['prose']
                and '16' in a and '16' in b and 'n_t = n_x/5' in hs['prose'] and 'n_t = n_x/5' in it['prose'])
        check('grid p3 is not the step of homework h-sequence (review finding 3)', not same,
              'pdes set: "%s" | homework: "%s"' % (a[:110], b[:80]))
    # the replacement the review gives: 6.25 times the work, 1,000 intervals
    V1000 = cn_price(*opt, 1000, 200)
    check('fix text: order 2 predicts 89.22 on 1,000 intervals', close(557.6 / 2.5 ** 2, 89.216, 1e-9) and 1000 * 200 == 6.25 * 400 * 80)
    check('fix text: the 1,000 run is about 93 below the limit', abs(rnd((limit - V1000) * 1e6, 0) - 93) < 1e-9, '%.2f' % ((limit - V1000) * 1e6))
    check('fix text: 39.1 times the paths', abs(rnd(6.25 ** 2, 1) - 39.1) < 1e-9 and abs(rnd((557.6 / 89.22) ** 2, 1) - 39.1) < 1e-9)
    check('fix text: the gap is about 1% above 557.6', abs(rnd(100 * (true400 / 557.6 - 1), 0) - 1) < 1e-9)
    check('fix text: the 1,600 run is about 37 below the limit', abs(rnd(true1600, 0) - 37) < 1e-9)

    # part 4
    if FIXED3:
        fac = 6.25
        band_checks('grid p4', P[3]['widget'], fac ** 2, (557.6 / 89.22) ** 2, 1,
                    slips={'linear': fac, 'root': math.sqrt(fac)})
    else:
        fac = 557.6 / 34.85
        check('grid p4 factor is 16', close(fac, 16.0, 1e-9))
        band_checks('grid p4', P[3]['widget'], fac ** 2, (557.6 / 34.85) ** 2, 0,
                    slips={'linear': fac, 'root': math.sqrt(fac)})
    # 1 / sqrt(n): paths times 256 cuts a standard error 16 times
    check('grid p4 square law', close(1 / math.sqrt(256.0), 1 / 16.0, 1e-15))

# Reuse, another course: numerics problems-3 p-rate-path-euler opens the same way (review finding 2)
num3 = os.path.join(ROOT, 'app', 'content', 'courses', 'numerics', 'problems-3.json')
if os.path.exists(num3):
    with open(num3, encoding='utf-8') as f:
        other = {i['id']: i for i in json.load(f)['items']}
    eu = other.get('p-rate-path-euler')
    if eu:
        a = P[0]['explain']['text']
        b = eu['parts'][0]['explain']['text']
        same = ('also' in a and 'per halving' in a and 'per halving' in b and 'also falls by $2^p$' in b
                and re.search(r'If the error is \$c\s*h\^p\$', a) is not None)
        check('grid p1 explain is not the numerics set line retold (review finding 4)', not same,
              'pdes: "%s" | numerics: "%s"' % (a[:95], b[:120]))

# level 3 shape
diffs = [L3[i]['difficulty'] for i in L3]
check('level 3 has one difficulty 5', diffs.count(5) == 1, '%r' % diffs)
check('level 3 has 3 problems and 12 parts', len(L3) == 3 and sum(len(L3[i]['parts']) for i in L3) == 12)
with open(os.path.join(PDES, 'course.json'), encoding='utf-8') as f:
    course = json.load(f)
check('level 3 skills are the course skills', all(s in course.get('skills', {}) for i in L3 for s in L3[i]['skills']))

# --------------------------------------------------------------------------
# Level 1: the changed parts
# --------------------------------------------------------------------------
L1 = load(1)
P = L1['p-grid-rod']['parts']
# explicit step with lambda = 1/2 on 13 nodes; three steps, then the limit
u = np.full(13, 40.0)
u[0], u[-1] = 15.0, 75.0
hist = []
for n in range(6000):
    u[1:-1] = 0.5 * (u[2:] + u[:-2])
    hist.append(u[1])
check('rod value after three steps', close(hist[2], 24.375, 1e-12))
steady_line = 15 + (75 - 15) / 1.2 * 0.1
check('rod steady value by the line and by the grid limit', close(steady_line, 20.0, 1e-12) and close(hist[-1], 20.0, 1e-9))
band_checks('rod p4', P[3]['widget'], hist[2] - hist[-1], 24.375 - 20, 3,
            slips={'steady': 20.0, 'mean-ends': 24.375 - 45, 'left-end': 24.375 - 15})
check('rod p4 restates 24.375', '24.375' in P[3]['question'])
txt = alltext(P[3])
check('rod p4 printed slope and values', all(s in txt for s in ('50', '$60 \\div 1.2 = 50$', '4.375', '45')))

it = L1['p-drift-walk']
P = it['parts']
dx, dt, q = 0.05, 0.001, 0.6
D = dx * dx / (2 * dt)
c = (2 * q - 1) * dx / dt
check('walk D and c', close(D, 1.25, 1e-12) and close(c, 10.0, 1e-9))
# the walk's own variance rate is 4 q (1 - q) dx^2 / dt = 2.4, not 2 D = 2.5
walk_var = 4 * q * (1 - q) * dx * dx / dt
check('walk variance rate differs from the model', close(walk_var, 2.4, 1e-12) and close(2 * D, 2.5, 1e-12))
check('walk prose says model', 'We model its density by' in it['prose'])
check('walk p3 asks the model', "the model's density" in P[2]['question'] and 'what chance does the model give' in P[2]['question'])
z3 = (2 - c * 0.32) / math.sqrt(2 * D * 0.32)
p3 = Phi(z3)
check('walk p3 given Phi(1.342) = 0.9102', abs(rnd(Phi(1.342), 4) - 0.9102) < 1e-12)
band_checks('walk p3', P[2]['widget'], p3, 1 - 0.9102, 3,
            slips={'no-drift': Phi(2 / math.sqrt(0.8)), 'var-dt': Phi((2 - 3.2) / math.sqrt(0.4))})
# exact binomial walk at t = 0.32 (320 steps): the walker's own chance of being below 2
n = 320
pw = 0.0
for j in range(n + 1):
    if (2 * j - n) * dx < 2 - 1e-12:
        pw += math.exp(math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) + j * math.log(q) + (n - j) * math.log(1 - q))
check('walk: the walker itself is below 2 with chance near 0.0855, not the key', abs(pw - 0.0855) < 0.003 and not in_band(P[2]['widget'], rnd(pw, 3)) or abs(pw - p3) > 0.002,
      'walker %r model %r' % (pw, p3))
# part 4 keeps the model's variance: its key and what the walk's own variance would give
t4 = (2.3263 / (c / math.sqrt(2 * D))) ** 2
t4_walk = (2.3263 / (c / math.sqrt(walk_var))) ** 2
check('walk p4 key is the model time', close(P[3]['widget']['answer'], t4, 6e-4))
check('walk p4: the walk\'s own variance gives another answer', not in_band(P[3]['widget'], rnd(t4_walk, 3)),
      'walk variance gives %r' % t4_walk)
check('walk p4 says whose chance it is (review finding 5)',
      re.search(r"model", P[3]['question']) is not None,
      'part 4 still reads "the chance of being below the start, 0, is" with no model named; '
      'the walk\'s own variance 2.4t gives t = %.4f against the key %.4f' % (t4_walk, t4))

# --------------------------------------------------------------------------
# Level 2: the changed parts
# --------------------------------------------------------------------------
L2 = load(2)
it = L2['p-grid-modes']
P = it['parts']
Dm, dtm, N = 0.75, 0.04, 12
dxm = math.pi / N
lam = Dm * dtm / dxm ** 2
check('modes prose', 'D = 0.75' in it['prose'] and '0.04' in P[0]['question'])
band_checks('modes p1', P[0]['widget'], lam, 0.03 / 0.068539, 4,
            slips={'no-d': 0.04 / 0.068539, 'unsquared': Dm * dtm / dxm})
printed('modes p1', alltext(P[0]), dxm ** 2, '0.068539')
check('modes p1 no-d is exact dt/dx^2 too', close(dtm / dxm ** 2, 0.58361, 6e-5))
# factor as the top eigenvalue of the step matrix (second route), then its 40th power
M = np.zeros((N - 1, N - 1))
i = np.arange(N - 1)
M[i, i] = 1 - 2 * lam
M[i[:-1], i[:-1] + 1] = lam
M[i[1:], i[1:] - 1] = lam
ev = np.linalg.eigvalsh(M)
g = 1 - 4 * lam * math.sin(dxm / 2) ** 2
check('modes factor is the top eigenvalue', close(ev.max(), g, 1e-12) and close(g, 0.970171, 6e-7))
check('modes all factors bounded', np.all(np.abs(ev) < 1))
band_checks('modes p2', P[1]['widget'], g, 1 - 4 * 0.4377 * 0.01704, 4,
            slips={'exact': math.exp(-Dm * dtm), 'no-half': 1 - 4 * 0.4377 * math.sin(dxm) ** 2})
mode = np.sin(np.arange(1, N) * dxm)
v40 = np.linalg.matrix_power(M, 40) @ mode
g40 = float(v40[0] / mode[0])
check('modes 40 steps of the matrix', close(g40, g ** 40, 1e-12))
check('modes 40 steps reach t = 1.6', close(40 * dtm, 1.6, 1e-12))
band_checks('modes p3', P[2]['widget'], g40, 0.9702 ** 40, 3,
            slips={'exact': math.exp(-Dm * 1.6), 'power-t': 0.9702 ** 1.6})
w = P[3]['widget']
exact_mode = math.exp(-Dm * 1.6)
check('modes p4 prints e^{-1.2} = 0.3012', abs(rnd(exact_mode, 4) - 0.3012) < 1e-12 and '0.3012' in P[3]['question'])
check('modes p4 restates 0.298', 'Using 0.298 from part 3' in P[3]['question'])
pct_print = (0.3012 - 0.298) / 0.3012
pct_exact = (exact_mode - g40) / exact_mode
for label, v in (('printed working', pct_print), ('exact', pct_exact), ('carried 0.2982', (0.3012 - 0.2982) / 0.3012),
                 ('carried 0.30119', (0.30119 - 0.298) / 0.30119)):
    t = typed(v, 1, pct=True)
    check('modes p4 band takes %s' % label, in_band(w, t), 'typed %r' % t)
for v in (0.009, 0.012):
    check('modes p4 band refuses %r' % v, not in_band(w, v))
check('modes p4 key', close(w['answer'], pct_print, 1e-4))
check('modes p4 unit', w.get('unit') == '%')
sl = {s['id']: s for s in w['wrong']}
check('modes p4 slip absolute', close(sl['absolute']['value'], 0.3012 - 0.298, 1e-9) and
      'absolute' in slip_hit(w, typed(0.0032, 1, pct=True)) and not in_band(w, 0.003))
check('modes p4 slip ratio', close(sl['ratio']['value'], 0.298 / 0.3012, 2e-4) and
      all('ratio' in slip_hit(w, v) for v in (0.989, 0.990)) and not in_band(w, 0.989))
check('modes p4 slip bands clear of the key band',
      all(abs(s['value'] - w['answer']) > s['tol']['abs'] + w['tol']['abs'] for s in w['wrong']))
txt = alltext(P[3])
check('modes p4 printed 0.011 and 1.1%', '0.011' in txt and '1.1%' in txt and abs(rnd(pct_print, 3) - 0.011) < 1e-12)
check('modes p4 prints e^{-0.03} = 0.9704', '0.9704' in txt and abs(rnd(math.exp(-0.03), 4) - 0.9704) < 1e-12)

it = L2['p-exp-series']
P = it['parts']
xs = np.linspace(-math.pi, math.pi, 2000001)
hq = xs[1] - xs[0]


def trap(f):
    return float(np.sum(f[1:] + f[:-1]) * 0.5 * hq)


b1 = trap(np.exp(xs) * np.sin(xs)) / math.pi
b3 = trap(np.exp(xs) * np.sin(3 * xs)) / math.pi
check('series b1 by quadrature', close(b1, math.sinh(math.pi) / math.pi, 1e-8))
check('series b3 by quadrature and by the rule', close(b3, 0.6 * b1, 1e-8))
band_checks('series p2', P[1]['widget'], b3, 0.6 * 3.6761, 4,
            slips={'sign': -0.6 * 3.6761, 'no-k': 0.2 * 3.6761})
txt = alltext(P[1])
check('series p2 prints 2.2057 and names 2.2056', txt.count('2.2057') == 2 and '2.2056' in txt)
check('series p2 printed product', abs(rnd(0.6 * 3.6761, 4) - 2.2057) < 1e-12 and abs(rnd(0.6 * b1, 4) - 2.2056) < 1e-12)
# part 5: the sum by direct summation with its tail, and by the printed route
Ks = np.arange(1, 2000001, dtype=float)
direct = float(np.sum(1.0 / (1.0 + Ks * Ks))) + 1.0 / 2000000.5
closed = (math.pi / math.tanh(math.pi) - 1) / 2
check('series sum two routes', close(direct, closed, 1e-9))
car = (math.pi * 11.5920 / 11.5487 - 1) / 2
band_checks('series p5', P[4]['widget'], closed, car, 4,
            slips={'no-half': 2 * closed, 'keep-one': (math.pi / math.tanh(math.pi)) / 2,
                   'used-left': (math.pi * math.exp(math.pi) / math.sinh(math.pi) - 1) / 2})
check('series p5 restates both values', '11.5487' in P[4]['question'] and '11.5920' in P[4]['question'])
check('series p5 printed 3.15335', abs(rnd(math.pi / math.tanh(math.pi), 5) - 3.15335) < 1e-12)

print('%d checks, %d FINDING line(s)' % (checks, findings))
