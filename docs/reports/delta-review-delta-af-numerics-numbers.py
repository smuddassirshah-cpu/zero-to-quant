#!/usr/bin/env python3
"""Delta read AF, numerics problem sets 1 to 4: the two re-authored problems and every part the two fix passes changed.

Imports no earlier script. Routes: exact fractions for the cubic pieces, the Newton iterates and the quadratic through
three points; mpmath for the square roots, the exact path and its ODE; numpy float32 for the gap; a brute search for each
whole-number key. Each band is rebuilt with the engine's rule (abs tolerance plus 1e-9; unit "%" divides a bare number by
100) and fed what a learner types from the rounded numbers the part prints.

Exit 0 always. A FINDING line prints while the content is as the review describes and `resolved` once it is fixed.
The numerics-problems concept-audit fix pass re-pointed the finding 5 text check to the new explain sentence.
"""
import json
import math
import os
import sys
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
from fractions import Fraction as F

import mpmath as mp
import numpy as np

mp.mp.dps = 40
HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'numerics')
SETS = {n: json.load(open(os.path.join(COURSE, f'problems-{n}.json'), encoding='utf-8')) for n in (1, 2, 3, 4)}

checks = 0
failed = []
findings = []


def check(name, ok, detail=''):
    global checks
    checks += 1
    if not ok:
        failed.append(name)
        print(f'FAIL {name} {detail}')


def finding(tag, still, text):
    findings.append(tag)
    print(f'FINDING {tag}: {text}' if still else f'FINDING {tag}: resolved')


def part(n, pid, k):
    it = next(i for i in SETS[n]['items'] if i['id'] == pid)
    return it['parts'][k - 1]


def item(n, pid):
    return next(i for i in SETS[n]['items'] if i['id'] == pid)


def typed_value(text, w):
    """The engine's numValue for a plain decimal, with the percent rule."""
    t = text.strip()
    pct = t.endswith('%')
    v = float(t.rstrip('%').replace(',', ''))
    if pct or w.get('unit') == '%':
        v /= 100
    return v


def grade(w, text):
    """'ok', a slip id, or 'no', as numGrade returns."""
    v = typed_value(text, w)
    if abs(v - w['answer']) <= w['tol'].get('abs', 0) + 1e-9:
        return 'ok'
    for x in w.get('wrong', []):
        if abs(v - x['value']) <= x.get('tol', {'abs': 1e-9}).get('abs', 0) + 1e-9:
            return x['id']
    return 'no'


def rnd(x, places, mode=ROUND_HALF_UP):
    q = Decimal(1).scaleb(-places)
    return str(Decimal(str(x)).quantize(q, rounding=mode))


def key_is(n, pid, k, value, tol=None, places=None):
    w = part(n, pid, k)['widget']
    check(f'{pid} part {k} key', abs(w['answer'] - float(value)) <= (tol if tol is not None else 0.51 * 10 ** -(places or 6)),
          f"file {w['answer']} mine {float(value)}")
    return w


def slip_is(w, pid, k, sid, value, places):
    x = next((s for s in w.get('wrong', []) if s['id'] == sid), None)
    check(f'{pid} part {k} slip {sid} exists', x is not None)
    if x is None:
        return
    check(f'{pid} part {k} slip {sid} value', abs(x['value'] - float(value)) <= 0.51 * 10 ** -places, f"file {x['value']} mine {float(value)}")
    check(f'{pid} part {k} slip {sid} typed', grade(w, rnd(float(value), places)) == sid, rnd(float(value), places))
    check(f'{pid} part {k} slip {sid} clear of key', abs(x['value'] - w['answer']) > x['tol']['abs'] + w['tol']['abs'] + 2e-9)


def has(n, pid, k, field, text):
    p = part(n, pid, k)
    blob = json.dumps(p if field is None else p[field], ensure_ascii=False)
    return text in blob


# ---------------------------------------------------------------------------------------------------------------------
# Set 1: p-float32-overnight part 2 (finding 1), lines of findings 4, 5, N2, N3
# ---------------------------------------------------------------------------------------------------------------------
gap = float(np.spacing(np.float32(0.9425)))
check('float32 gap near 0.9425 is 2^-24', gap == 2.0 ** -24 and float(np.spacing(np.float32(0.9424))) == 2.0 ** -24)
share = F(1, 2 ** 24) / F(1, 10 ** 4)            # two half gaps over the difference, as a fraction
w = key_is(1, 'p-float32-overnight', 2, share, tol=5e-7)
check('float32 part 2 unit', w.get('unit') == '%' and w['tol']['abs'] == 5e-6)
for sid, val in (('one-factor', share / 2), ('eps', share * 2)):
    x = next(s for s in w['wrong'] if s['id'] == sid)
    check(f'float32 part 2 slip {sid} value', abs(x['value'] - float(val)) < 5e-7 and x['tol']['abs'] == 5e-6, str(float(val)))
    check(f'float32 part 2 slip {sid} clear of key', abs(x['value'] - w['answer']) > 1.1e-5)
for s, want in (('0.060', 'ok'), ('0.060%', 'ok'), ('0.06%', 'ok'), ('0.06', 'ok'), ('0.0596', 'ok'), ('0.0596%', 'ok'),
                ('0.059', 'no'), ('0.059%', 'no'), ('0.061', 'no'), ('0.061%', 'no'), ('0.000596', 'no'), ('0.6', 'no'),
                ('0.030', 'one-factor'), ('0.030%', 'one-factor'), ('0.0298%', 'one-factor'), ('0.03%', 'one-factor'),
                ('0.119', 'eps'), ('0.119%', 'eps'), ('0.1192', 'eps'), ('0.1192%', 'eps')):
    check(f'float32 part 2 typed {s}', grade(w, s) == want, grade(w, s))
check('float32 part 2 not on a tie', abs(float(share) * 100 * 1000 % 1 - 0.5) > 0.05)       # 0.059605 per cent at 3 places
# parts 3 and 4 restate 0.0596% and still give their keys
w3 = part(1, 'p-float32-overnight', 3)['widget']
check('float32 part 3 exact ratio 18,850', F(1, 2 ** 24) / F(1, 10 ** 4) / (F(1, 2 ** 25) / F(9425, 10000)) == 18850 and w3['answer'] == 18850)
restated = 5.96e-4 / 3.16e-8                     # the two rounded values the question hands over
finding('E (wrong) p-float32-overnight part 3 refuses the answer its own restated values give',
        grade(w3, str(round(restated))) != 'ok' or has(1, 'p-float32-overnight', 3, 'feedback', '10^{-8} \\\\approx 18{,}850'),
        f"5.96e-4 / 3.16e-8 = {restated:.2f}, typed {round(restated)}, graded '{grade(w3, str(round(restated)))}' "
        f"(band {w3['answer']} +/- {w3['tol']['abs']}); the feedback prints that quotient as 18,850")
pc = next(s for s in w3['wrong'] if s['id'] == 'per-cent')
slip_typed = 0.0596 / 3.16e-8                    # "You divided the percentage itself"
finding('F (misleading) p-float32-overnight part 3 slip per-cent',
        grade(w3, str(round(slip_typed))) != 'per-cent',
        f"dividing the percentage itself gives 0.0596 / 3.16e-8 = {slip_typed:,.0f} (1,885,000 unrounded); the entry is {pc['value']}, "
        "which is 5.96e-6 / 3.16e-8, and the line is never reached")
check('float32 part 3 slip one-input from exact values', grade(w3, '9425') == 'one-input')
one_in = 2.98e-4 / 3.16e-8                       # one-input from the rounded 0.0298%
print(f'note: one-input slip from rounded values, {one_in:.1f}, grades as {grade(w3, str(round(one_in)))}')
kappa = (F(9425, 10000) + F(9424, 10000)) / F(1, 10000)
check('float32 kappa 18,849', kappa == 18849)
w4 = part(1, 'p-float32-overnight', 4)['widget']
fwd = F(1, 10000) * 365 / F(9424, 10000)
check('float32 part 4 from restated 0.0596%', grade(w4, rnd(float(fwd) * 5.96e-4 * 1e4, 2)) == 'ok')
check('finding 4 applied', 'A curve library built for single precision' in item(1, 'p-float32-overnight')['prose'])
check('finding 5 applied', has(1, 'p-float32-overnight', 3, 'explain', 'the sensitivity of a difference to its two inputs'))
check('note N3 applied', has(1, 'p-float32-overnight', 3, 'feedback', 'Compare $'))
check('note N2 applied', has(1, 'p-moment-recurrence', 2, 'explain', 'Later roundings add errors of their own'))
# N2 claim: the forward recurrence, with every rounding, strays further than 18! u I_0 allows for I_0 alone? (it need not: check only the stated bound)
u = mp.mpf(2) ** -53
I0 = 1 - mp.e ** -1
check('moment part 2 bound 0.45', abs(mp.factorial(18) * u * I0 - mp.mpf('0.4493')) < 5e-4)

# ---------------------------------------------------------------------------------------------------------------------
# Set 2: p-vol-curve-extension (new)
# ---------------------------------------------------------------------------------------------------------------------
PID = 'p-vol-curve-extension'
p = lambda t: 16 + F(42, 10) * (t - 1) - F(6, 10) * (t - 1) ** 3
dp = lambda t: F(42, 10) - F(18, 10) * (t - 1) ** 2
ddp = lambda t: -F(36, 10) * (t - 1)
h = F(1, 10 ** 6)
check('vol p(1) = 16, p(2) = 19.6', p(1) == 16 and p(2) == F(196, 10))
check('vol p\'(2) = 2.4 by a difference', abs((p(2 + h) - p(2 - h)) / (2 * h) - F(24, 10)) < F(1, 10 ** 9) and dp(2) == F(24, 10))
check('vol p\'\'(1) = 0 and p\'\'(2) = -3.6 by a difference', ddp(1) == 0 and abs((p(2 + h) - 2 * p(2) + p(2 - h)) / h ** 2 + F(36, 10)) < F(1, 10 ** 5))
w = key_is(2, PID, 1, ddp(2), places=1)
slip_is(w, PID, 1, 'sign', -ddp(2), 1)
slip_is(w, PID, 1, 'slope', dp(2), 1)
slip_is(w, PID, 1, 'once', -F(6, 10) * 3, 1)
check('vol part 1 typed', grade(w, '-3.6') == 'ok')

def c_for(curv_coeff):
    return F(204, 10) - F(196, 10) - F(24, 10) - curv_coeff

c = c_for(ddp(2) / 2)
w = key_is(2, PID, 2, c, places=1)
check('vol c = 0.2', c == F(1, 5) and grade(w, '0.2') == 'ok')
slip_is(w, PID, 2, 'no-half', c_for(ddp(2)), 1)
slip_is(w, PID, 2, 'sign', c_for(-ddp(2) / 2), 1)
slip_is(w, PID, 2, 'once', c_for(F(-18, 10) / 2), 1)

q = lambda u, c=c: F(196, 10) + F(24, 10) * u - F(18, 10) * u ** 2 + c * u ** 3
dq = lambda u, c=c: F(24, 10) - F(36, 10) * u + 3 * c * u ** 2
ddq = lambda u, c=c: -F(36, 10) + 6 * c * u
check('vol q matches p at the join and the quote', q(0) == p(2) and dq(0) == dp(2) and ddq(0) == ddp(2) and q(1) == F(204, 10))
w = key_is(2, PID, 3, ddq(1), places=1)
check('vol part 3 typed', grade(w, '-2.4') == 'ok')
slip_is(w, PID, 3, 'sign', -ddq(1), 1)
slip_is(w, PID, 3, 'natural', 0, 1)
slip_is(w, PID, 3, 'once', -F(36, 10) + 3 * c, 1)
slip_is(w, PID, 3, 'no-half', ddq(1, c=F(2)), 1)
check('vol q\'(1) < 0 so a peak lies before 3 years', dq(1) == F(-6, 10))

u0 = F(3, 4)
check('vol printed q\'(0.75) = 0.0375, q\'\'(0.75) = -2.7', dq(u0) == F(375, 10000) and ddq(u0) == F(-27, 10))
u1 = u0 - dq(u0) / ddq(u0)
check('vol printed step 0.013889', rnd(float(u1 - u0), 6) == '0.013889')
w = key_is(2, PID, 4, 2 + u1, places=6)
check('vol part 4 typed 2.7639', grade(w, rnd(float(2 + u1), 4)) == 'ok' and rnd(float(2 + u1), 4) == '2.7639')
slip_is(w, PID, 4, 'sign', 2 + u0 + dq(u0) / ddq(u0), 4)
slip_is(w, PID, 4, 'end-curv', 2 + u0 - dq(u0) / ddq(0), 4)
peak_u = 3 - mp.sqrt(5)
check('vol exact peak 3 - sqrt 5 solves q\' = 0', abs(mp.mpf(24) / 10 - mp.mpf(36) / 10 * peak_u + mp.mpf(6) / 10 * peak_u ** 2) < mp.mpf(10) ** -30)
check('vol exact peak printed 0.763932', mp.nstr(peak_u, 6) == '0.763932')
check('vol one step within 5e-5 of the peak', abs(peak_u - mp.mpf(u1.numerator) / u1.denominator) < 5e-5)

ur = F(7639, 10000)                                     # the value part 5 restates
terms = [F(24, 10) * ur, F(18, 10) * ur ** 2, F(2, 10) * ur ** 3]
check('vol part 5 printed terms', [rnd(float(x), 5) for x in terms] == ['1.83336', '1.05038', '0.08915'], str([float(x) for x in terms]))
rise = q(ur) - F(204, 10)
w = key_is(2, PID, 5, rise, places=6)
check('vol part 5 from the unrounded step too', grade(w, rnd(float(q(u1) - F(204, 10)), 4)) == 'ok' and grade(w, rnd(float(rise), 4)) == 'ok')
check('vol part 5 exact peak height gives the key', grade(w, mp.nstr(mp.mpf('19.6') + 2.4 * peak_u - 1.8 * peak_u ** 2 + 0.2 * peak_u ** 3 - mp.mpf('20.4'), 3)) == 'ok')
slip_is(w, PID, 5, 'peak', q(ur), 4)
slip_is(w, PID, 5, 'start', q(u0) - F(204, 10), 4)
slip_is(w, PID, 5, 'sign', q(F(7361, 10000)) - F(204, 10), 4)
# explain claims: a natural spline through the three quotes changes p and rises all the way to 3 years
M2 = F(6) * ((F(204, 10) - F(196, 10)) - (F(196, 10) - 16)) / 4          # 4 M2 = 6 (slope change), unit spacing
check('vol natural refit has M2 = -4.2, not -3.6', M2 == F(-42, 10) and M2 != ddp(2))
s2 = lambda t: M2 * (3 - t) ** 3 / 6 + (F(196, 10) - M2 / 6) * (3 - t) + F(204, 10) * (t - 2)
ds2 = lambda t: -M2 * (3 - t) ** 2 / 2 - (F(196, 10) - M2 / 6) + F(204, 10)
check('vol natural refit passes its knots', s2(2) == F(196, 10) and s2(3) == F(204, 10))
check('vol natural refit rises on [2, 3]', all(ds2(2 + F(i, 1000)) > 0 for i in range(1001)), str(float(ds2(2))))
s1 = lambda t: M2 * (t - 1) ** 3 / 6 + 16 * (2 - t) + (F(196, 10) - M2 / 6) * (t - 1)
ds1 = lambda t: M2 * (t - 1) ** 2 / 2 - 16 + (F(196, 10) - M2 / 6)
check('vol natural refit: slopes meet at 2 and it rises on [1, 2]', ds1(2) == ds2(2) and all(ds1(1 + F(i, 1000)) > 0 for i in range(1001)))
check('vol height error is the square of the place error', abs(float(q(u1)) - float(mp.mpf('19.6') + 2.4 * peak_u - 1.8 * peak_u ** 2 + 0.2 * peak_u ** 3)) < 1e-8)

# ---------------------------------------------------------------------------------------------------------------------
# Set 2: p-survival-crossing parts 1, 3, 5 (findings 6 to 9); p-project-irr part 4 (finding 10)
# ---------------------------------------------------------------------------------------------------------------------
PID = 'p-survival-crossing'
pts = [(F(1), F(98, 100)), (F(3), F(92, 100)), (F(5), F(84, 100))]

def lag(t):
    s = F(0)
    for i, (xi, yi) in enumerate(pts):
        term = yi
        for j, (xj, _) in enumerate(pts):
            if j != i:
                term *= (t - xj) / (xi - xj)
        s += term
    return s

check('survival p(4) = 0.8825 by Lagrange', lag(F(4)) == F(8825, 10000))
newton_form = lambda t: F(98, 100) - F(3, 100) * (t - 1) - F(25, 10000) * (t - 1) * (t - 3)
check('survival printed form is the Lagrange quadratic', all(newton_form(F(i, 7)) == lag(F(i, 7)) for i in range(7, 36)))
second = lag(F(2)) - 2 * lag(F(3)) + lag(F(4))          # p'' exactly, unit differences of a quadratic
check('survival p\'\' = -0.005 a year', second == F(-5, 1000))
finding('A (misleading) p-survival-crossing part 1 explain',
        has(2, PID, 1, 'explain', 'they change by') ,
        f"the explain says the slopes change by -0.0025 a year; the slope of p changes by p'' = {float(second)} a year "
        "(-0.0025 is the coefficient of (t - 1)(t - 3), half of that)")
t2 = F(35333, 10000)                                    # the value part 3 restates
pv = lag(t2)
dpv = (lag(t2 + h) - lag(t2 - h)) / (2 * h)             # exact for a quadratic
check('survival p(3.5333) = 0.90062348', rnd(float(pv), 8) == '0.90062348', str(float(pv)))
check('ruling on finding 7: 0.9006235 is right, 0.900624 is not', rnd(float(pv), 7) == '0.9006235' and rnd(float(pv), 6) == '0.900623')
check('survival p\'(3.5333) = -0.0376665', dpv == F(-376665, 10 ** 7))
step = -(pv - F(9, 10)) / dpv
check('ruling on finding 7: step 0.016553', rnd(float(step), 6) == '0.016553', str(float(step)))
check('printed quotient 0.0006235/0.037667', rnd(0.0006235 / 0.037667, 6) == '0.016553')
check('reader\'s quotient 0.000624/0.037667 is 0.016566, which the fixer was right to refuse', rnd(0.000624 / 0.037667, 6) == '0.016566')
w = key_is(2, PID, 3, t2 + step, places=6)
check('survival part 3: 3.5333 + 0.016553 types 3.5499', rnd(3.5333 + 0.016553, 4) == '3.5499' and grade(w, '3.5499') == 'ok')
check('survival part 3 printed lines', has(2, PID, 3, 'feedback', '0.9006235') and has(2, PID, 3, 'feedback', '0.016553') and has(2, PID, 3, 'explain', '0.0006235'))
slip_is(w, PID, 3, 'sign', t2 - step, 4)
check('survival sign slip from the unrounded secant point', grade(w, rnd(float(F(53, 15) - (-(lag(F(53, 15)) - F(9, 10)) / ((lag(F(53, 15) + h) - lag(F(53, 15) - h)) / (2 * h)))), 4)) == 'sign')
cross = -4 + mp.sqrt(57)
check('survival exact crossing within 2e-5', abs(cross - mp.mpf(float(t2 + step))) < 2e-5)
w5 = part(2, PID, 5)['widget']
days = 2.033e-4 / 0.03775 * 365
check('survival part 5 from the restated 2.033e-4', grade(w5, rnd(days, 2)) == 'ok' and rnd(days, 2) == '1.97' and rnd(2.033e-4 / 0.03775, 5) == '0.00539', str(days))
check('survival part 5 text restates 2.033', has(2, PID, 5, 'question', '2.033') and has(2, PID, 5, 'feedback', '2.033') and has(2, PID, 5, 'explain', '2.033'))
prod = abs((3.5499 - 1) * (3.5499 - 3) * (3.5499 - 5))
check('survival part 4 product 2.033', rnd(prod, 3) == '2.033')
check('finding 9 applied', has(2, PID, 1, 'feedback', 'One way to write it is') and not has(2, PID, 1, None, 'divided difference') and not has(2, PID, 1, None, 'Newton form'))

PID = 'p-project-irr'
e = 0.026
chain = []
for _ in range(3):
    e = 0.77 * e * e
    chain.append(e)
check('irr printed chain', [f'{x:.1e}' for x in chain] == ['5.2e-04', '2.1e-07', '3.4e-14'], str(chain))
check('irr third step beats the target by about 30', 25 < 1e-12 / 3.4e-14 < 35 and has(2, PID, 4, 'explain', 'by a factor of about 30'))
f = lambda v: 50 * v ** 3 + 40 * v ** 2 + 30 * v - 100
root = mp.findroot(lambda v: f(v), 0.92)
v = mp.mpf(17) / 18
real = []
for _ in range(3):
    v = v - f(v) / (150 * v ** 2 + 80 * v + 30)
    real.append(abs(v - root))
check('irr real third error 3.2e-14, factor 31', mp.nstr(real[2], 2) == '3.2e-14' and 28 < 1e-12 / real[2] < 34, mp.nstr(real[2], 5))

# ---------------------------------------------------------------------------------------------------------------------
# Set 3: p-normal-cdf-quadrature part 2 explain (finding 11); p-implicit-newton-step (new)
# ---------------------------------------------------------------------------------------------------------------------
PID = 'p-normal-cdf-quadrature'
fn = lambda x: mp.e ** (-x * x / 2)
T1 = (fn(0) + fn(1)) / 2
T2 = (fn(0) + 2 * fn(mp.mpf(1) / 2) + fn(1)) / 4
I = mp.quad(fn, [0, 1])
R = (4 * T2 - T1) / 3
check('richardson weights 1/6, 4/6, 1/6', (F(4) * F(1, 4) - F(1, 2)) / 3 == F(1, 6) and F(4) * F(1, 2) / 3 == F(4, 6))
check('richardson value 0.856086 and errors 0.0127, 0.00046', mp.nstr(R, 6) == '0.856086' and rnd(float(I - T2), 4) == '0.0127' and rnd(float(R - I), 5) == '0.00046')
w = part(3, PID, 2)['widget']
check('richardson from the restated 0.8429 and 0.8033', grade(w, rnd((4 * 0.8429 - 0.8033) / 3, 4)) == 'ok')
check('finding 11 applied', has(3, PID, 2, 'explain', 'come out as'))

PID = 'p-implicit-newton-step'
fx = lambda x: -40 * x - 200 * x * x
dfx = lambda x: -40 - 400 * x
hh = F(1, 20)
x0 = F(1, 20)
check('implicit: rate -60 and h lambda = -3', dfx(x0) == -60 and hh * dfx(x0) == -3)
G = lambda v: v - x0 - hh * fx(v)
dG = lambda v: 1 - hh * dfx(v)
check('implicit: G(v) = 10 v^2 + 3 v - 0.05', all(G(F(i, 13)) == 10 * F(i, 13) ** 2 + 3 * F(i, 13) - F(1, 20) for i in range(-5, 6)))
check('implicit: G\'(v) = 3 + 20 v', all(dG(F(i, 13)) == 3 + 20 * F(i, 13) for i in range(-5, 6)))
check('implicit printed G(0.05) = 0.125, G\' = 4', G(x0) == F(1, 8) and dG(x0) == 4)
v1 = x0 - G(x0) / dG(x0)
w = key_is(3, PID, 1, v1, places=6)
check('implicit iterate 1 = 0.01875 exactly', v1 == F(3, 160) and grade(w, '0.01875') == 'ok')
slip_is(w, PID, 1, 'explicit', x0 + hh * fx(x0), 5)
slip_is(w, PID, 1, 'no-one', x0 - G(x0) / (dG(x0) - 1), 5)
slip_is(w, PID, 1, 'sign', x0 + G(x0) / dG(x0), 5)
check('implicit printed G(0.01875) = 0.0097656, parts 0.0035156 and 0.05625, G\' = 3.375',
      G(v1) == F(5, 512) and rnd(float(G(v1)), 7) == '0.0097656' and rnd(float(10 * v1 ** 2), 7) == '0.0035156' and 3 * v1 == F(5625, 100000) and dG(v1) == F(27, 8))
st2 = G(v1) / dG(v1)
v2 = v1 - st2
check('implicit printed step 0.0028935 and iterate 0.0158565', rnd(float(st2), 7) == '0.0028935' and rnd(float(v2), 7) == '0.0158565' and v2 == F(137, 8640))
w = part(3, PID, 2)['widget']
import re
pl = int(re.search(r'Give (\d) decimal places', part(3, PID, 2)['question']).group(1))     # 6 as read; 7 once fixed
check('implicit part 2 key takes the exact iterate at the stated places', grade(w, rnd(float(v2), pl)) == 'ok', rnd(float(v2), pl))
printed = Decimal('0.01875') - Decimal('0.0028935')            # the sum the feedback prints
up = str(printed.quantize(Decimal(1).scaleb(-pl), rounding=ROUND_HALF_UP))
tie_gap = abs(float(v2) - 0.0158565)
finding('B (misleading) p-implicit-newton-step part 2 key on a rounding tie',
        grade(w, up) != 'ok',
        f"the iterate is 137/8640 = {float(v2):.10f}, {tie_gap:.1e} below the 6-place tie 0.0158565; the feedback's own sum "
        f"0.01875 - 0.0028935 = {printed} rounds half up to {up}, which the key band refuses")
slip_is(w, PID, 2, 'frozen', v1 - G(v1) / dG(x0), pl)
slip_is(w, PID, 2, 'sign', v1 + st2, pl)
for s_ in (Decimal('0.01875') - Decimal('0.0097656') / 4, Decimal('0.01875') + Decimal('0.0028935')):   # slips from the printed rounded values
    check('implicit part 2 slip from printed values is routed', grade(w, rnd(float(s_), pl)) in ('frozen', 'sign'), str(s_))
check('implicit: second step is about a tenth of the first', 0.08 < float(st2 / (G(x0) / dG(x0))) < 0.12)
rootv = (-3 + mp.sqrt(11)) / 20
check('implicit root solves G', abs(10 * rootv ** 2 + 3 * rootv - mp.mpf('0.05')) < mp.mpf(10) ** -30)
w = key_is(3, PID, 3, rootv, places=7)
check('implicit part 3 typed', grade(w, mp.nstr(rootv, 6)) == 'ok' and mp.nstr(rootv, 6) == '0.0158312')
slip_is(w, PID, 3, 'stopped', v2, 7)
slip_is(w, PID, 3, 'other-root', (-3 - mp.sqrt(11)) / 20, 7)
slip_is(w, PID, 3, 'disc', (-3 + mp.sqrt(7)) / 20, 7)
e1 = mp.mpf(3) / 160 - rootv
e2 = mp.mpf(137) / 8640 - rootv
check('implicit printed Newton errors 2.9e-3 and 2.5e-5', mp.nstr(e1, 2) == '0.0029' and mp.nstr(e2, 2) == '2.5e-5', f'{e1} {e2}')
Cn = 20 / (2 * (3 + 20 * rootv))
check('implicit Newton constant about 3 and 3 e1^2 near e2', abs(Cn - 3) < 0.05 and abs(3 * mp.mpf('2.9e-3') ** 2 - e2) < 2e-6, str(Cn))
# frozen slope converges at order 1: ratio 1 - G'(root)/4
r1 = (v1 - G(v1) / 4)
check('implicit frozen slope: error ratio near 1 - G\'(r)/4', abs((mp.mpf(r1.numerator) / r1.denominator - rootv) / e1 - (1 - (3 + 20 * rootv) / 4)) < 0.01)
# exact path
xt = lambda t: 2 * mp.e ** (-40 * t) / (50 - 10 * mp.e ** (-40 * t))
check('implicit exact path starts at 0.05', abs(xt(0) - mp.mpf('0.05')) < mp.mpf(10) ** -30)
check('implicit exact path solves the ODE', all(abs(mp.diff(xt, t) - (-40 * xt(t) - 200 * xt(t) ** 2)) < mp.mpf(10) ** -12 for t in (mp.mpf('0.001'), mp.mpf('0.01'), mp.mpf('0.03'), mp.mpf('0.05'), mp.mpf('0.2'))))
sol = mp.odefun(lambda t, y: -40 * y - 200 * y * y, 0, mp.mpf('0.05'))
check('implicit exact path against a Taylor ODE solve', abs(sol(mp.mpf('0.05')) - xt(mp.mpf('0.05'))) < mp.mpf(10) ** -15)
xh = xt(mp.mpf('0.05'))
check('implicit printed x(0.05) = 0.005564', mp.nstr(xh, 4) == '0.005564', mp.nstr(xh, 10))
w = key_is(3, PID, 4, rootv - xh, places=7)
check('implicit part 4 from the restated 0.0158312 and printed 0.005564', grade(w, rnd(0.0158312 - 0.005564, 5)) == 'ok' and rnd(float(mp.mpf('0.0158312') - xh), 5) == '0.01027')
slip_is(w, PID, 4, 'sign', -(rootv - xh), 5)
slip_is(w, PID, 4, 'explicit', mp.mpf('-0.075') - xh, 5)
slip_is(w, PID, 4, 'start', mp.mpf('0.05') - xh, 5)
w = part(3, PID, 5)['widget']
check('implicit part 5 printed difference 2.53e-5', abs(Decimal('0.0158565') - Decimal('0.0158312') - Decimal('0.0000253')) == 0)
for num, den in ((0.01027, 2.53e-5), (0.0102672, 2.53e-5), (float(rootv - xh), float(e2)), (0.01027, 2.5e-5 * 1.012)):
    check(f'implicit part 5 ratio {num}/{den}', grade(w, str(round(num / den))) == 'ok', str(num / den))
check('implicit part 5 key 406', w['answer'] == 406 and round(0.01027 / 2.53e-5) == 406)
x5 = next(s for s in w['wrong'] if s['id'] == 'first')
for num, den in ((0.01027, 2.9e-3), (0.01027, float(e1))):
    check('implicit part 5 slip first', grade(w, rnd(num / den, 2)) == 'first' and grade(w, str(round(num / den))) == 'first', str(num / den))
check('implicit part 5 slip clear of key', x5['value'] + x5['tol']['abs'] < 404)
finding('C (continuity) p-implicit-newton-step part 2 slip frozen',
        has(3, PID, 2, 'feedback', 'simplified Newton') or has(3, PID, 2, 'feedback', 'linearly'),
        '"simplified Newton" and "converges only linearly" are used nowhere else in the course, which says "order 1"')
finding('D (reuse) p-implicit-newton-step part 1 slip sign',
        has(3, PID, 1, 'feedback', 'You added the correction. Newton subtracts'),
        "the line retells exams/stage-2 c-newton-yield: \"You added $f/f'$. Newton subtracts it, and here $f' < 0$, so $y$ rises.\"")

# ---------------------------------------------------------------------------------------------------------------------
# Set 4: the seven findings
# ---------------------------------------------------------------------------------------------------------------------
PID = 'p-pilot-control'
var_c = F(64) - 2 * F(77, 100) * 77 + F(77, 100) ** 2 * 100
check('pilot variance 4.71', var_c == F(471, 100))
n_need = next(n for n in range(45000, 46000) if 1.96 * math.sqrt(4.71 / n) <= 0.02)
w = part(4, PID, 2)['widget']
check('pilot part 2 key 45,235 by search', n_need == 45235 == w['answer'] and has(4, PID, 2, 'question', '1.96'))
exact_z = 1.959963984540054
check('pilot part 2: the exact normal point would give 45,234 (why 1.96 is stated)', math.ceil(exact_z ** 2 * 4.71 / 0.0004) == 45234)
check('pilot part 2 slip two', grade(w, str(math.ceil(4 * 4.71 / 0.0004))) == 'two')
ratio = F(64) / F(471, 100)
w = key_is(4, PID, 4, ratio, tol=6e-6)
check('pilot part 4 tol 0.005 and typed forms', w['tol']['abs'] == 0.005 and [grade(w, s) for s in ('13.59', '13.588', '13.58', '13.60', '3.69', '3.686', '10.45')] == ['ok', 'ok', 'no', 'no', 'se', 'se', 'gain'])
slip_is(w, PID, 4, 'se', math.sqrt(float(ratio)), 2)
slip_is(w, PID, 4, 'gain', 614656 / (1.3 * 45235), 2)
check('pilot part 4 question no longer prints its key', not has(4, PID, 4, 'question', '13.59'))
check('pilot break-even: c x 4.71 < 64', float(ratio) * 4.71 <= 64 + 1e-9 and 13.6 * 4.71 > 64)
check('finding 7 applied', has(4, PID, 4, 'feedback', 'scale with the variance itself, not its root'))

PID = 'p-digital-pairs'
pp = F(1, 5)
# joint law of the two 0 or 1 parts of a pair that never pays twice
EB1B2 = F(0)
rho = (EB1B2 - pp * pp) / (pp * (1 - pp))
check('pairs rho = -p/(1 - p) = -0.25', rho == F(-1, 4) == -pp / (1 - pp))
sep = F(1, 4) * 2                      # variance of a mean of two separate payoffs, in units of s^2
pair = F(1, 4) * (2 + 2 * rho)
w = key_is(4, PID, 4, sep / pair, places=6)
check('pairs quotient 4/3 and the printed halves', sep == F(1, 2) and pair == F(1, 2) * F(3, 4) and grade(w, '1.33') == 'ok')
check('three pairs do the work of eight separate paths', pair / 3 == F(1, 8))
slip_is(w, PID, 4, 'inverted', pair / sep, 2)
rng = np.random.default_rng(20261116)
z = rng.standard_normal(2_000_000)
from statistics import NormalDist
k = NormalDist().inv_cdf(0.8)
a, b = (z > k).astype(float), (-z > k).astype(float)
check('pairs rho by simulation', abs(np.corrcoef(a, b)[0, 1] + 0.25) < 0.005, str(np.corrcoef(a, b)[0, 1]))
check('rho is small when few paths pay', all(abs(-x / (1 - x)) < abs(-y / (1 - y)) for x, y in ((0.05, 0.2), (0.2, 0.4), (0.4, 0.5))) and -0.5 / 0.5 == -1)
check('findings 3 and 4 applied', has(4, PID, 4, 'question', 'What is the first variance divided by the second') and has(4, PID, 4, 'explain', 'is small when few paths pay'))

PID = 'p-hand-implicit-put'
br = F(1, 4) * 9 + F(4, 100)
check('put centre weight -0.145 and 1.145 times the bound', 1 - F(1, 2) * br == F(-145, 1000) and F(1, 2) / (1 / br) == F(1145, 1000))
check('finding 5 applied', has(4, PID, 1, 'feedback', 'not 2.25') and has(4, PID, 1, 'explain', '1.145 times the longest that keeps the $j = 3$ weight non-negative'))
w = part(4, PID, 1)['widget']
check('put part 1 slip no-r', grade(w, rnd(float(1 - F(1, 2) * F(9, 4)), 3)) == 'no-r')

PID = 'p-grid-node-budget'
kk = next(k for k in range(1, 50) if 0.0219 / k ** 2 < 0.002)
w = part(4, PID, 3)['widget']
check('grid fewest M = 276 by search', kk == 4 and 69 * kk == w['answer'] == 276)
check('grid printed predictions', rnd(0.0219 / 9, 5) == '0.00243' and rnd(0.0219 / 16, 5) == '0.00137')
kx = math.sqrt(0.0219 / 0.002)
check('grid k = 3.31 puts the strike between nodes', rnd(kx, 2) == '3.31' and abs(92 / (4 / 3.31) - round(92 / (4 / 3.31))) > 0.05 and math.ceil(69 * 3.31) == 229)
check('finding 6 applied', has(4, PID, 3, 'question', 'comes out 0.0219 too low') and has(4, PID, 3, 'explain', 'could not be trusted'))

# ---------------------------------------------------------------------------------------------------------------------
print(f'{checks} checks, {len(failed)} failed, {len(findings)} FINDING row(s)')
sys.exit(0)
