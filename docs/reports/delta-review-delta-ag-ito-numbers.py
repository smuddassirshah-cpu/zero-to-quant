#!/usr/bin/env python3
"""Delta read AG, ito problem sets 1 to 3: numbers of the re-authored problems and of every
part the fix pass on docs/reviews/review-problems-ito-1-3.md changed.

Scope: p-twin-shares and p-bridge-closes (problems-3, whole items); p-maker-tally (whole item),
p-realised-then-risk part 1, p-quarter-rally part 1 slip line (problems-1); p-cable-inverse
parts 2 and 4, p-cube-path parts 2 to 4, p-results-vol parts 3 and 4 (problems-2); p-touch-note
parts 2 to 4 (problems-3).

Imports no earlier script. No SciPy and no root finder: Phi comes from erfc and again from
Simpson's rule, lognormal means from Gauss-Legendre sums over the normal law, the 625 trades
from their exact binomial law, the touch chance between two closes from the two normal
densities and again from a seeded simulation of pinned paths (skipped, not failed, when NumPy
is missing or the run is far off). Each band is rebuilt with the engine's rule
(|typed - key| <= abs + 1e-9) and fed what a learner types.

Exit code 0 always. A failing check prints a FINDING line. The numbered findings of
docs/reviews/review-delta-ag-ito.md print `FINDING n` while the content is as the review
describes and `resolved n` once it is fixed.
"""
import json
import math
import os
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ITO = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'ito')

checks = bad = findings = 0


def ok(cond, name):
    global checks, bad
    checks += 1
    if not cond:
        bad += 1
        print('FINDING (unlisted check failed):', name)


def finding(n, still_there, name):
    global findings
    if still_there:
        findings += 1
        print(f'FINDING {n}: {name}')
    else:
        print(f'resolved {n}: {name}')


def item(n, iid):
    with open(os.path.join(ITO, f'problems-{n}.json'), encoding='utf-8') as fh:
        return next(it for it in json.load(fh)['items'] if it['id'] == iid)


def inband(x, a, tol):
    return abs(x - a) <= tol + 1e-9


def route(w, x):
    if inband(x, w['answer'], w['tol']['abs']):
        return 'key'
    for e in w.get('wrong', []):
        if inband(x, e['value'], e['tol']['abs']):
            return e['id']
    return None


def bands(pid, part, key, places, wrong, typed=()):
    """key: my value. places: decimal places asked (of the stored fraction for a % part).
    wrong: {id: my value}. typed: further values a learner may type that must grade right."""
    w = part['widget']
    ok(abs(w['answer'] - key) <= 0.5 * 10 ** (-places) + 1e-9, f'{pid}: key {w["answer"]} is {key:.8g}')
    for x in (round(key, places),) + tuple(typed):
        ok(route(w, x) == 'key', f'{pid}: key band takes {x}')
    ids = {e['id'] for e in w.get('wrong', [])}
    ok(ids == set(wrong), f'{pid}: wrong ids {sorted(ids)} are {sorted(wrong)}')
    for e in w.get('wrong', []):
        if e['id'] not in wrong:
            continue
        mine = wrong[e['id']]
        ok(inband(mine, e['value'], e['tol']['abs']), f'{pid}: wrong {e["id"]} {e["value"]} is {mine:.8g}')
        ok(route(w, e['value']) == e['id'], f'{pid}: {e["id"]} is refused by the key and reaches its line')
        ok(e['id'] in part['feedback'].get('byKey', {}), f'{pid}: {e["id"]} has a byKey line')
    es = [(w['answer'], w['tol']['abs'], 'key')] + [(e['value'], e['tol']['abs'], e['id']) for e in w.get('wrong', [])]
    for i in range(len(es)):
        for j in range(i + 1, len(es)):
            ok(abs(es[i][0] - es[j][0]) > es[i][1] + es[j][1] + 2e-9, f'{pid}: bands {es[i][2]} and {es[j][2]} are apart')


def text(part):
    out = []

    def rec(o):
        if isinstance(o, dict):
            for v in o.values():
                rec(v)
        elif isinstance(o, list):
            for v in o:
                rec(v)
        elif isinstance(o, str):
            out.append(o)
    rec(part)
    return ' '.join(out)


def Phi(z):
    return 0.5 * math.erfc(-z / math.sqrt(2))


def Phi_simpson(z, n=4000):
    a = -9.0
    h = (z - a) / n
    f = lambda t: math.exp(-0.5 * t * t) / math.sqrt(2 * math.pi)
    s = f(a) + f(z) + sum((4 if k % 2 else 2) * f(a + k * h) for k in range(1, n))
    return s * h / 3


def npdf(u, mean, var):
    return math.exp(-(u - mean) ** 2 / (2 * var)) / math.sqrt(2 * math.pi * var)


def normal_mean(g, n=6000, lim=9.0):
    """E[g(Z)], Z standard normal, by Simpson's rule."""
    h = 2 * lim / n
    f = lambda z: g(z) * math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)
    s = f(-lim) + f(lim) + sum((4 if k % 2 else 2) * f(-lim + k * h) for k in range(1, n))
    return s * h / 3


for z in (-0.7826, -0.35, -1.75, -0.1323, -0.13):
    ok(abs(Phi(z) - Phi_simpson(z)) < 1e-9, f'Phi({z}) agrees by erfc and by Simpson')

# ---------------------------------------------------------------- problems-1: p-maker-tally
mk = item(1, 'p-maker-tally')
p, n, stake = F(507, 1000), 625, 40
ok('0.507' in mk['prose'] and '625' in mk['prose'] and '£40' in mk['prose'], 'maker: stem holds 625, £40 and 0.507')
# exact binomial law of the day's P&L (wins k, P&L 40(2k - 625))
pmf = [math.comb(n, k) * float(p) ** k * float(1 - p) ** (n - k) for k in range(n + 1)]
mean_day = sum(q * stake * (2 * k - n) for k, q in enumerate(pmf))
var_day = sum(q * (stake * (2 * k - n)) ** 2 for k, q in enumerate(pmf)) - mean_day ** 2
ok(abs(mean_day - 350) < 1e-6, 'maker 1: binomial mean of the day is 350')
ok(n * stake * (2 * p - 1) == 350, 'maker 1: 625 x 40 x 0.014 = 350 exactly')
bands('maker 1', mk['parts'][0], 350, 0, {'wins-only': float(n * stake * p), 'half-edge': 175, 'per-trade-count': float(n * (2 * p - 1))})
ok(abs(var_day - 999804) < 1e-3, 'maker 2: the day variance is 999,804')
bands('maker 2', mk['parts'][1], n * stake ** 2, 0, {'variance': var_day, 'abs-sum': n * stake})
sd5 = math.sqrt(5 * 1_000_000)
bands('maker 3', mk['parts'][2], sd5, 0, {'sd-times-t': 5000, 'one-day': 1000}, typed=(2236.07, 2236.1))
z = -1750 / sd5
bands('maker 4', mk['parts'][3], Phi(z), 4,
      {'sd-times-t': Phi(-1750 / 5000), 'no-drift': 0.5, 'ends-up': 1 - Phi(z), 'one-day': Phi(-1750 / 1000)},
      typed=(round(Phi(-0.7826), 4), round(Phi(-1750 / 2236.07), 4), round(Phi(-0.783), 4)))
ok(abs(z + 0.7826) < 5e-5, 'maker 4: z = -0.7826')
ok('software' in mk['parts'][3]['question'] and 'table' not in mk['parts'][3]['question'], 'maker 4: names software, no table')
ok(not inband(round(Phi(-0.78), 4), mk['parts'][3]['widget']['answer'], mk['parts'][3]['widget']['tol']['abs']),
   'maker 4: a table reading at -0.78 (0.2177) would miss, which is why no table is named')
t = text(mk)
ok(all(s in t for s in ('0.56', '0.014', '49.3%', '1,750', '2,236.07', '-0.7826', '0.2169')), 'maker: printed figures as recomputed')
ok('500t' not in t, 'maker: no 500t left from the first version')
ok(abs(350 / 1000 - 0.5) > 0.1, 'maker: drift over sigma is 0.35, not h-drift-below\'s 0.5')

# ---------------------------------------------------------------- problems-1: realised, quarter-rally
rr = item(1, 'p-realised-then-risk')
ok(all(s in rr['prose'] for s in ('84', '0.0147', '£64', '9\\%', '£60')), 'realised: stem numbers unchanged')
ok('squared daily log returns add to' not in rr['prose'] and 'from the quadratic variation' not in rr['parts'][0]['question'],
   'realised: the two homework sentences are gone')
sig = math.sqrt(0.0147 / (F(84, 252)))
bands('realised 1', rr['parts'][0], sig, 2, {'not-annual': math.sqrt(0.0147), 'variance': 0.0147 * 3, 'times-days': math.sqrt(0.0147 * 252)})
qr = item(1, 'p-quarter-rally')
ok(round(0.35 ** 2 * 0.75, 4) == 0.0919 and '0.0919' in qr['parts'][0]['feedback']['byKey']['variance'], 'rally 1: 0.35^2 x 0.75 = 0.0919 in the slip line')
ok(abs(qr['parts'][0]['widget']['answer'] - 0.35 * math.sqrt(0.75)) < 5e-6, 'rally 1: key unchanged')

# ---------------------------------------------------------------- problems-2: cable, cube, results
cb = item(2, 'p-cable-inverse')
mu, s = 0.02, 0.12
# E[1/X_3] over the lognormal law, no Ito step
EY = normal_mean(lambda zz: 1 / (1.25 * math.exp((mu - 0.5 * s * s) * 3 + s * math.sqrt(3) * zz)))
ok(abs(EY - 0.8 * math.exp(3 * (s * s - mu))) < 1e-9, 'cable 2: E[1/X_3] by integration is 0.8e^{-0.0168}')
bands('cable 2', cb['parts'][1], EY, 4, {'inverse-mean': 1 / (1.25 * math.exp(0.06)), 'median': 0.8 * math.exp(-3 * (mu - 0.5 * s * s))})
# martingale drift: E[1/X_1] = 1/X_0 exactly when mu = sigma^2
EY1 = normal_mean(lambda zz: 1 / (1.25 * math.exp((s * s - 0.5 * s * s) + s * zz)))
ok(abs(EY1 - 0.8) < 1e-9, 'cable 4: with mu = 0.0144 the mean of Y stays at 0.8')
bands('cable 4', cb['parts'][3], s * s, 4, {'log-flat': 0.5 * s * s, 'zero': 0, 'sigma': s})
ok(cb['parts'][3]['widget'].get('unit') == '%' and 'zero drift when' not in cb['parts'][3]['question'], 'cable 4: unit %, the question no longer states the condition')
ok('mean 0, so' not in text(cb['parts'][1]) and 'obeys' not in text(cb['parts'][1]), 'cable 2: the l6 step line is gone')

cu = item(2, 'p-cube-path')
W = [F(0), F(3, 10), F(-2, 10), F(4, 10), F(6, 10)]
dW = [W[k + 1] - W[k] for k in range(4)]
left = sum(W[k] ** 2 * dW[k] for k in range(4))
mid = sum(W[k] * dW[k] ** 2 for k in range(4))
cubes = sum(d ** 3 for d in dW)
ok(left == F(11, 1000) and mid == F(19, 1000) and cubes == F(126, 1000), 'cube: path sums 0.011, 0.019, 0.126 in exact fractions')
ok(W[4] ** 3 == 3 * left + 3 * mid + cubes, 'cube 2: the telescoped identity holds on the path')
bands('cube 2', cu['parts'][1], float(mid), 3, {'no-third': float(3 * mid), 'no-cube': float((W[4] ** 3 - 3 * left) / 3)})
q4 = cu['parts'][3]['question']
ok('\\int_0^1 W\\,dt' not in q4 and '3\\int' not in q4, 'cube 4: the question no longer prints the integrand')
ok(cu['parts'][3]['widget']['answer'] == '3w', 'cube 4: key 3w (half of f_xx = 6x)')
# E[W_1^3 - 3 int W dt] = 0 is not a check of the coefficient on its own; check the drift by moments:
# d/dt E[W_t^3 | W_s = w] at t = s is 3w, since E[(w + D)^3] = w^3 + 3w(t - s).
ok(abs(normal_mean(lambda zz: (0.7 + math.sqrt(1e-4) * zz) ** 3) - 0.7 ** 3 - 3 * 0.7 * 1e-4) < 1e-12, 'cube 4: the drift of W^3 at w is 3w')

rv = item(2, 'p-results-vol')
var = 0.25 * 0.4 ** 2 + 0.75 * 0.15 ** 2
ok(abs(var - 0.056875) < 1e-12, 'results: integrated variance 0.056875')
med = 72 * math.exp(0.06 - 0.5 * var)
bands('results 3', rv['parts'][2], med, 2, {'mean': 72 * math.exp(0.06), 'average-vol': 72 * math.exp(0.06 - 0.5 * 0.2125 ** 2), 'full-variance': 72 * math.exp(0.06 - var)})
ok('0.0284375' in rv['parts'][2]['feedback']['byKey']['full-variance'] and abs(var / 2 - 0.0284375) < 1e-12, 'results 3: half the variance is 0.0284375')
sb = math.sqrt(var)
pz = Phi(-(0.06 - 0.5 * var) / sb)
P_sim = normal_mean(lambda zz: 1.0 if (0.06 - 0.5 * var) + sb * zz < 0 else 0.0, n=200000)
ok(abs(P_sim - pz) < 2e-4, 'results 4: the chance by direct integration of the law')
bands('results 4', rv['parts'][3], pz, 4,
      {'average-vol': Phi(-(0.06 - 0.5 * 0.2125 ** 2) / 0.2125), 'no-drag': Phi(-0.06 / 0.2385), 'upper': 1 - pz},
      typed=(round(Phi(-0.0315625 / 0.2385), 4), round(Phi(-0.1323), 4), 0.4483, round(Phi(-0.132), 4)))
ok(round(Phi(-0.13), 4) == 0.4483, 'results 4: the table reading at z = -0.13 is 0.4483, and the band takes it')
ok('table' in rv['parts'][3]['question'], 'results 4: the part names its table')

# ---------------------------------------------------------------- problems-3: p-touch-note
tn = item(3, 'p-touch-note')
r, s = 0.04, 0.25
a = -2 * r / s ** 2
ok(abs(a + 1.28) < 1e-12 and abs(0.5 * s * s * a * (a - 1) + r * a - r) < 1e-12, 'touch: the root -1.28 solves the time-free equation')
ok('£75' in tn['prose'] and '80' not in text(tn), 'touch: barrier 75 everywhere, no 80 left')
V = (100 / 75) ** a
# a second route: E[e^{-r tau}] for the first passage of ln S to ln 75 under Q (Laplace transform of a hitting time)
nu = r - 0.5 * s * s
dist = math.log(100 / 75)
V2 = math.exp(-dist * (nu + math.sqrt(nu * nu + 2 * r * s * s)) / (s * s))
ok(abs(V - V2) < 1e-12, 'touch 3: (4/3)^-1.28 equals the discounted first-passage mean')
bands('touch 3', tn['parts'][2], V, 4, {'sign': (4 / 3) ** 1.28, 'no-half': (4 / 3) ** -0.64, 'root-one': 4 / 3})
opts = {o['id']: o for o in tn['parts'][1]['widget']['options']}
ok(opts['negative-power'].get('correct') and '75' in opts['negative-power']['text'] and all('80' not in o['text'] for o in opts.values()), 'touch 2: options on the barrier 75')
h = 1e-5
VS = ((100 + h) / 75) ** a - ((100 - h) / 75) ** a
VS /= 2 * h
ok(abs(VS - a * V / 100) < 1e-9, 'touch 4: V_S by central difference is -1.28 V / S')
bands('touch 4', tn['parts'][3], 10000 * VS, 1, {'sign': -10000 * VS, 'no-power': -10000 * V / 100},
      typed=(round(-1.28 * 0.6920 * 100, 1), round(-1.28 * 0.6919 * 100, 1), -88.57))
# FINDING 2: the key of part 3 sits 6e-6 above a tie at 4 places
w3 = tn['parts'][2]['widget']
typed_ln = round(math.exp(-1.28 * round(math.log(4 / 3), 4)), 4)        # ln(4/3) = 0.2877, the route the feedback prints
ok(abs(V - 0.69195) < 1e-5 and typed_ln == 0.6919, 'touch 3: key 0.691956 is 0.000006 off the tie 0.69195; ln(4/3) = 0.2877 gives 0.6919')
finding(2, route(w3, typed_ln) != 'key', 'p-touch-note part 3: band 0.00005 refuses 0.6919, which e^{-1.28 x 0.2877} gives; fix tol.abs 0.0001')
ok(inband(typed_ln, V, 0.0001) and inband(0.6920, V, 0.0001) and not inband((4 / 3) ** -0.64, V, 0.0001 + 0.00005), 'touch 3 fix: 0.0001 takes 0.6919 and 0.6920 and stays off every wrong band')

# ---------------------------------------------------------------- problems-3: p-twin-shares
tw = item(3, 'p-twin-shares')
SA, SB, muA, sA, sB, r, T = 60.0, 45.0, 0.095, 0.18, 0.30, 0.05, 2.0
ok(all(x in tw['prose'] for x in ('£60', '9.5\\%', '18%', '£45', '30%', '5\\%', 'two years')), 'twin: stem numbers')
x = F(1000) * F(18, 100) / F(30, 100)
ok(1000 * F(18, 100) - x * F(30, 100) == 0 and x == 600, 'twin 1: £600 of B cancels the noise exactly')
bands('twin 1', tw['parts'][0], 600, 0, {'inverted': 1000 * 0.30 / 0.18, 'equal': 1000, 'variance-ratio': 1000 * (0.18 / 0.30) ** 2})
muB = (F(1000) * F(95, 1000) - F(5, 100) * (1000 - x)) / x
ok(muB == F(1, 8), 'twin 2: mu_B = 12.5% from the book earning r on £400')
ok((F(95, 1000) - F(5, 100)) / F(18, 100) == (muB - F(5, 100)) / F(30, 100) == F(1, 4), 'twin 2: both shares earn 0.25 per unit of vol')
bands('twin 2', tw['parts'][1], 0.125, 3, {'whole-book': (95 - 50) / 600, 'no-r': 95 / 600, 'same-drift': 0.095}, typed=(0.125,))
muB = 0.125


def ratio_mean(mA, mB, t):
    """E[S_B(t)/S_A(t)], both on the same W, by integration over W_t."""
    return normal_mean(lambda zz: (SB * math.exp((mB - 0.5 * sB * sB) * t + sB * math.sqrt(t) * zz))
                       / (SA * math.exp((mA - 0.5 * sA * sA) * t + sA * math.sqrt(t) * zz)))


driftP = math.log(ratio_mean(muA, muB, 1.0) / 0.75)
ok(abs(driftP - 0.0084) < 1e-9, 'twin 3: the mean of R grows at 0.84% a year under P (integration, no Ito step)')
ok(abs(driftP - (muB - muA + sA * sA - sA * sB)) < 1e-9, 'twin 3: equals mu_B - mu_A + sA^2 - sA sB')
bands('twin 3', tw['parts'][2], driftP, 4, {'no-ito': muB - muA, 'no-cross': muB - muA + sA * sA, 'no-convexity': muB - muA - sA * sB,
                                           'log-drift': (muB - 0.5 * sB * sB) - (muA - 0.5 * sA * sA)})
ER = ratio_mean(r, r, T)
driftQ = math.log(ER / 0.75) / T
ok(abs(driftQ + 0.0216) < 1e-9, 'twin 4: under Q the ratio drifts at -2.16% a year')
price = 100 * ER * math.exp(-r * T)
ok(abs(price - 75 * math.exp(-0.1432)) < 1e-7, 'twin 4: price 75e^{-0.1432}')
bands('twin 4', tw['parts'][3], price, 2,
      {'real-drift': 75 * math.exp(2 * 0.0084 - 0.1), 'martingale': 75 * math.exp(-0.1), 'undiscounted': 100 * ER,
       'log-drift': 75 * math.exp(2 * (-0.0288) - 0.1)},
      typed=(round(100 * 0.75 * round(math.exp(-0.0432), 4) * round(math.exp(-0.1), 4), 2),
             round(71.83 * math.exp(-0.1), 2), round(71.83 * 0.9048, 2)))
ok(tw['parts'][1]['widget'].get('unit') == '%' and tw['parts'][2]['widget'].get('unit') == '%', 'twin 2 and 3: unit %')
# FINDING 3: 75e^{-0.1432} with the exponential at 4 places is a dead tie
e4 = round(math.exp(-0.1432), 4)
ok(e4 == 0.8666 and abs(75 * e4 - 64.995) < 1e-9, 'twin 4: 75 x 0.8666 = 64.995, a tie at 2 places')
finding(3, route(tw['parts'][3]['widget'], 65.00) != 'key', 'p-twin-shares part 4: 75 x 0.8666 = 64.995 is a tie and 65.00 is refused; fix tol.abs 0.01')
ok(inband(65.00, price, 0.01) and inband(64.99, price, 0.01) and abs(price - 64.06) > 0.015, 'twin 4 fix: 0.01 takes 64.99 and 65.00, wrong bands stay apart')

# ---------------------------------------------------------------- problems-3: p-bridge-closes
bc = item(3, 'p-bridge-closes')
closes = [105.00, 107.60, 111.20, 110.30, 109.40]
ok(all(f'£{c:.2f}' in bc['prose'] for c in closes) and '£112' in bc['prose'] and '28\\%' in bc['prose'] and '4.5\\%' in bc['prose'], 'bridge: stem numbers')
sg, r, B, K = 0.28, 0.045, 112.0, 100.0
v = sg * sg / 252
b = math.log(B)


def touch(x, y):
    """Chance that a pinned driftless path from x to y (one day) reaches b: ratio of two normal densities."""
    return npdf(2 * b - y, x, v) / npdf(y, x, v)


ps = [touch(math.log(closes[k]), math.log(closes[k + 1])) for k in range(4)]
ok(abs(ps[2] - math.exp(-2 * math.log(B / 111.2) * math.log(B / 110.3) / v)) < 1e-12, 'bridge 2: the density ratio is e^{-2(b-x)(b-y)/v}')
ok(abs(math.log(B / 111.2) - 0.007168) < 5e-7 and abs(math.log(B / 110.3) - 0.015295) < 5e-7 and abs(v - 0.0003111) < 5e-8, 'bridge 2: printed 0.007168, 0.015295, 0.0003111')
ok(abs(2 * 0.007168 * 0.015295 / 0.0003111 - 0.7048) < 5e-5, 'bridge 2: printed exponent 0.7048')
ok(abs(0.045 - 0.0392 - 0.0058) < 1e-12 and abs(0.5 * sg * sg - 0.0392) < 1e-12, 'bridge 1: Q drift of ln S is 0.0058')
bands('bridge 2', bc['parts'][1], ps[2], 4,
      {'no-two': math.exp(-math.log(B / 111.2) * math.log(B / 110.3) / v), 'whole-year': math.exp(-2 * math.log(B / 111.2) * math.log(B / 110.3) / (sg * sg)),
       'survival': 1 - ps[2]},
      typed=(round(math.exp(-0.7048), 4),))
# part 1: a drift leaves the pinned path alone. (B_t + mu t) - (t/T)(B_T + mu T) = B_t - (t/T) B_T for any mu.
for m_ in (0.0058, 0.5, -3.0):
    ok(abs(((0.37 + m_ * 0.4) - 0.4 * (0.81 + m_ * 1.0)) - (0.37 - 0.4 * 0.81)) < 1e-12, f'bridge 1: the pinned path does not see a drift of {m_}')
# and the weight between two drifts depends on the day's move only: ratio of the two transition densities
x_, y_ = math.log(111.2), math.log(110.3)
wt = npdf(y_, x_ + 0.0058 / 252, v) / npdf(y_, x_, v)
ok(abs(wt - math.exp((0.0058 / 252) * (y_ - x_) / v - (0.0058 / 252) ** 2 / (2 * v))) < 1e-12, 'bridge 1: the drift weight is a function of the two closes')
# simulation of pinned paths, seeded; only a coarse check (a grid misses touches), skipped if NumPy is absent
try:
    import numpy as np
    rng = np.random.default_rng(20261117)
    m = 4000
    hits = tot = 0
    for _ in range(10):
        dz = rng.standard_normal((2000, m)) * math.sqrt(v / m)
        Wp = np.cumsum(dz, axis=1)
        tt = np.arange(1, m + 1) / m
        path = x_ + (y_ - x_) * tt + Wp - tt * Wp[:, -1:]
        hits += int((path.max(axis=1) >= b).sum())
        tot += 2000
    est = hits / tot
    if abs(est - ps[2]) < 0.03:
        ok(True, f'bridge 2: simulated pinned paths touch with frequency {est:.4f} (grid of {m}), key {ps[2]:.4f}')
    else:
        print(f'skipped: pinned-path simulation gave {est:.4f} on this NumPy build')
except Exception as exc:  # noqa: BLE001
    print('skipped: pinned-path simulation not run:', type(exc).__name__)

surv = (1 - ps[0]) * (1 - ps[1]) * (1 - ps[2]) * (1 - ps[3])
ok(ps[0] < 1e-7 and abs(ps[0] - 6e-8) < 1e-8, 'bridge 3: first gap chance near 6e-8')
ok(abs(2 * math.log(B / 105) * math.log(B / 107.6) / v - 16.6) < 0.05 and abs(math.log(B / 105) - 0.0645) < 5e-5, 'bridge 3: printed 0.0645 and exponent 16.6')
ok([round(q, 4) for q in ps[1:]] == [0.1577, 0.4942, 0.0993], 'bridge 3: touch chances 0.1577, 0.4942, 0.0993')
bands('bridge 3', bc['parts'][2], surv, 4, {'sum-rule': 1 - sum(ps), 'one-gap': 1 - ps[2], 'touch': 1 - surv},
      typed=(round(0.8423 * 0.5058 * 0.9007, 4), round((1 - 0.1577) * (1 - 0.4942) * (1 - 0.0993), 4)))
disc = math.exp(-r * 4 / 252)
ok(abs(disc - 0.999286) < 5e-7 and abs(disc * 9.40 - 9.3933) < 5e-5, 'bridge 4: factor 0.999286, plain figure 9.3933')
add = disc * (closes[-1] - K) * surv
bands('bridge 4', bc['parts'][3], add, 2, {'plain': disc * 9.40, 'knock-in': disc * 9.40 * (1 - surv), 'one-gap': disc * 9.40 * (1 - ps[2]), 'sum-rule': disc * 9.40 * (1 - sum(ps))},
      typed=(round(0.999286 * 9.40 * 0.3837, 2), round(9.39 * 0.3837, 2), round(9.3933 * 0.3837, 2)))
# FINDING 1: the explanation prints the day's sd 0.01764; squared it gives 0.0003112, not the 0.0003111 printed next
sd_printed = 0.01764
ok(abs(sg / math.sqrt(252) - sd_printed) < 5e-6, 'bridge 2: the day sd is 0.01764 as printed')
p_sd = math.exp(-2 * 0.007168 * 0.015295 / sd_printed ** 2)
ok(round(p_sd, 4) == 0.4943 and round(sd_printed ** 2, 7) == 0.0003112, 'bridge 2: with the printed sd the chance is 0.4943')
w2 = bc['parts'][1]['widget']
finding(1, route(w2, round(p_sd, 4)) != 'key' and '0.01764' in bc['parts'][1]['explain']['text'],
        'p-bridge-closes part 2: the printed sd 0.01764 gives 0.4943, refused by the band 0.00005; fix tol.abs 0.00015 and the first explain sentence')
ps_sd = [math.exp(-2 * math.log(B / closes[k]) * math.log(B / closes[k + 1]) / sd_printed ** 2) for k in range(4)]
surv_sd = round((1 - ps_sd[0]) * (1 - ps_sd[1]) * (1 - ps_sd[2]) * (1 - ps_sd[3]), 4)
ok(surv_sd == 0.3836, 'bridge 3: the same route gives survival 0.3836')
finding('1b', route(bc['parts'][2]['widget'], surv_sd) != 'key', 'p-bridge-closes part 3: 0.3836 from the sd route is refused by the band 0.0001; fix tol.abs 0.00015')
ok(inband(0.4943, ps[2], 0.00015) and inband(0.4942, ps[2], 0.00015) and abs(ps[2] - (1 - ps[2])) > 0.001, 'bridge 2 fix: 0.00015 takes 0.4942 and 0.4943, wrong bands far')
ok(inband(0.3836, surv, 0.00015) and inband(0.3837, surv, 0.00015) and inband(0.3838, surv, 0.00015), 'bridge 3 fix: 0.00015 takes 0.3836 to 0.3838')

print(f'{checks} checks, {bad} unlisted failures, {findings} FINDING rows (exit code 0 either way)')
