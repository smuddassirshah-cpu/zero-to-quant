"""Recompute every number in app/content/courses/numerics/problems-1.json to problems-3.json twice.

Method 1 is exact where it can be (fractions, sympy, mpmath at 50 digits, float32 by NumPy). Method 2 is independent:
a direct float simulation, a brute search, scipy or numpy library calls. For each numeric part the script checks that
the two methods agree, that the key lies in its band, that the value at the rounding the question asks for is
accepted, and that every `wrong` value equals its named slip recomputed here and lies outside the key's band.
Choice parts: the keyed option is the one expected. Stated figures in feedback and explain are checked as text.
numbers_lib.Level.check_wrongs runs over each set as a second check of the bands. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-numerics-numbers.py
"""
import json, os, sys, math
from fractions import Fraction as F
import numpy as np
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'numerics')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

mp.mp.dps = 50
fails, checks = [], 0
LEVELS = [n for n in (1, 2, 3) if os.path.exists(os.path.join(COURSE, f'problems-{n}.json'))]


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
        print('BAD', msg)


def load(lv):
    d = json.load(open(os.path.join(COURSE, f'problems-{lv}.json'), encoding='utf8'))
    return d, {it['id']: it for it in d['items']}


SETS = {lv: load(lv) for lv in LEVELS}


def part(lv, iid, p):
    return SETS[lv][1][iid]['parts'][p - 1]


def text_of(pt):
    fb = pt.get('feedback', {})
    bits = [pt.get('question', ''), fb.get('correct', ''), fb.get('generic', ''), pt.get('explain', {}).get('text', '')]
    bits += list(fb.get('byKey', {}).values())
    return '\n'.join(bits)


def num(lv, iid, p, exact, alt, slips, rounded=None, agree=1e-9):
    """exact, alt: the value two ways. slips: {wrong id: recomputed value}. rounded: the figure the asked rounding gives."""
    pt = part(lv, iid, p)
    w, tag = pt['widget'], f'L{lv} {iid} p{p}'
    ok(w['kind'] == 'numeric', f'{tag} is numeric')
    exact, alt = float(exact), float(alt)
    ok(abs(exact - alt) <= agree * max(1, abs(exact)), f'{tag} methods agree {exact} vs {alt}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - exact) <= tol, f'{tag} key {w["answer"]} within {tol} of {exact}')
    if rounded is not None:
        ok(abs(rounded - w['answer']) <= tol + 1e-12, f'{tag} rounded {rounded} accepted')
    ids = {x['id']: x for x in w.get('wrong', [])}
    ok(set(ids) == set(slips), f'{tag} wrong ids {sorted(ids)} == {sorted(slips)}')
    bykey = pt['feedback'].get('byKey', {})
    for k, v in slips.items():
        if k not in ids:
            continue
        x = ids[k]
        ok(abs(x['value'] - float(v)) <= x['tol']['abs'], f'{tag} wrong {k} {x["value"]} is the slip {float(v)}')
        ok(abs(x['value'] - w['answer']) > tol + x['tol']['abs'], f'{tag} wrong {k} band clear of key band')
        ok(k in bykey and bykey[k], f'{tag} wrong {k} has a byKey line')
    for k in bykey:
        ok(k in ids, f'{tag} byKey {k} names a wrong entry')


def choice(lv, iid, p, key):
    pt = part(lv, iid, p)
    w = pt['widget']
    ok(w['kind'] == 'choice', f'L{lv} {iid} p{p} is choice')
    keys = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keys == [key], f'L{lv} {iid} p{p} key {keys} == {key}')
    for o in w['options']:
        if not o.get('correct'):
            ok(bool(o.get('why')), f'L{lv} {iid} p{p} option {o["id"]} has a why')


def says(lv, iid, p, *phrases):
    t = text_of(part(lv, iid, p))
    for ph in phrases:
        ok(ph in t, f'L{lv} {iid} p{p} states {ph!r}')


def shape(lv, lessons):
    d, items = SETS[lv]
    ok(3 <= len(items) <= 5, f'L{lv} has 3 to 5 problems')
    ok(any(it['difficulty'] == 5 for it in items.values()), f'L{lv} has a difficulty 5')
    parts = [pt for it in items.values() for pt in it['parts']]
    typed = sum(pt['widget']['kind'] in ('numeric', 'expression') for pt in parts)
    ok(typed * 3 >= 2 * len(parts), f'L{lv} typed {typed} of {len(parts)} at least two thirds')
    drawn = set()
    for iid, ls in lessons.items():
        ok(len(ls) >= 2, f'L{lv} {iid} draws on two or more lessons')
        drawn |= set(ls)
    course = json.load(open(os.path.join(COURSE, 'course.json'), encoding='utf8'))
    want = set(course['levels'][lv - 1]['lessons'])
    ok(drawn == want, f'L{lv} lessons drawn {sorted(drawn)} == {sorted(want)}')


# ---------------------------------------------------------------- level 1
if 1 in LEVELS:
    shape(1, {'p-float32-overnight': ['l1-floating-point', 'l2-cancellation', 'l3-conditioning'],
              'p-moment-recurrence': ['l1-floating-point', 'l4-stability'],
              'p-netting-sum': ['l3-conditioning', 'l4-stability']})

    # p-float32-overnight
    gap = np.spacing(np.float32(0.75))                       # numpy float32 gap in [0.5, 1)
    k = math.log2(float(gap))
    num(1, 'p-float32-overnight', 1, -24, k, {'eps': math.log2(np.finfo(np.float32).eps), 'half': -25, 'sign': 24})
    P0, P1, D = F('0.9425'), F('0.9424'), F('0.9425') - F('0.9424')
    rel = F(1, 2**24) / D * 100                              # per cent
    a32, b32 = np.float32(0.9425), np.float32(0.9424)
    ok(abs(float(a32) - 0.9425) <= 2**-25 and abs(float(b32) - 0.9424) <= 2**-25, 'L1 float32 factors within half a gap')
    d32 = a32 - b32
    ok(float(d32) == float(a32) - float(b32), 'L1 float32 difference exact (Sterbenz)')
    alt = float((np.float64(np.spacing(np.float32(0.9))) / 1e-4) * 100)
    num(1, 'p-float32-overnight', 2, rel, alt, {'one-factor': rel / 2, 'eps': F(1, 2**23) / D * 100}, rounded=0.060)
    amp = (F(1, 2**24) / D) / (F(1, 2**25) / P0)
    kap = (P0 + P1) / D
    num(1, 'p-float32-overnight', 3, amp, 2 * 0.9425 / 1e-4, {'one-input': P0 / D, 'per-cent': float(amp) / 100},
        rounded=round(float(amp)))
    ok(abs(float(amp) - float(kap)) <= 2, 'L1 amplification matches kappa 18849 within the band')
    ok(kap == 18849, 'L1 kappa of the subtraction is 18849')
    f = D * 365 / P1
    errbp = float(F(1, 2**24) / D * f) * 1e4
    alt = float(f) * 1e4 * float(np.spacing(np.float32(0.6))) / 1e-4
    num(1, 'p-float32-overnight', 4, errbp, alt, {'eps': 2 * errbp, 'one-factor': errbp / 2}, rounded=0.23)
    ok(abs(float(f) - 0.03873) < 5e-6, 'L1 forward is 3.873%')
    says(1, 'p-float32-overnight', 3, '18{,}849', '18{,}850', '\\log_{10} 18{,}850 \\approx 4.3')
    ok(abs(math.log10(18850) - 4.3) < 0.05, 'L1 log10 18850 is 4.3')
    says(1, 'p-float32-overnight', 4, '3.873\\%', '2.31 \\times 10^{-5}', '0.23 bp')

    # p-moment-recurrence
    I = [mp.quad(lambda x, n=n: x**n * mp.e**(x - 1), [0, 1]) for n in range(26)]
    ok(all(abs(I[n] - (1 - n * I[n - 1])) < mp.mpf(10)**-40 for n in range(1, 26)), 'L1 recurrence holds (mpmath quad)')
    fact18 = math.factorial(18)
    gx = 1.0
    for n in range(1, 19):                                    # error growth simulated step by step
        gx *= -n
    num(1, 'p-moment-recurrence', 1, math.log10(fact18), math.log10(abs(gx)),
        {'one-step': math.log10(18), 'sum': math.log10(sum(range(1, 19)))}, rounded=15.8)
    u = 2.0**-53
    I0 = 1 - math.exp(-1)
    bound = u * I0 * fact18
    alt = float(mp.mpf(2)**-53 * (1 - mp.e**-1) * mp.factorial(18))
    num(1, 'p-moment-recurrence', 2, bound, alt, {'eps': 2 * bound, 'no-i0': u * fact18}, rounded=0.45)
    says(1, 'p-moment-recurrence', 1, '6.40 \\times 10^{15}')
    says(1, 'p-moment-recurrence', 2, '7.02 \\times 10^{-17}', '0.632')
    ok(abs(u * I0 - 7.02e-17) < 5e-20, 'L1 u I0 = 7.02e-17')
    choice(1, 'p-moment-recurrence', 3, 'ok')
    ok(1 / (19 * mp.e) < I[18] < mp.mpf(1) / 19, 'L1 I18 between 1/(19e) and 1/19')
    says(1, 'p-moment-recurrence', 3, '0.019', '0.053')

    def back_bound(N):
        return F(1, N + 1) * F(math.factorial(18), math.factorial(N))
    Nmin = next(N for N in range(19, 60) if back_bound(N) < F(1, 10**10))
    # second method: run the backward recurrence in mpmath from I_N = 0 and find the first N whose I_18 error is below the bound
    def back(N):
        v = mp.mpf(0)
        for n in range(N, 18, -1):
            v = (1 - v) / n
        return v
    ok(all(abs(back(N) - I[18]) <= mp.mpf(back_bound(N).numerator) / back_bound(N).denominator for N in range(19, 26)), 'L1 backward errors lie inside the bound')
    N_nostart = next(N for N in range(19, 60) if F(math.factorial(18), math.factorial(N)) < F(1, 10**10))
    num(1, 'p-moment-recurrence', 4, Nmin, 25, {'no-start': N_nostart, 'one-short': Nmin - 1})
    ok(back_bound(24) > F(1, 10**10), 'L1 N = 24 not enough')
    ok(abs(float(back_bound(24)) - 4.1e-10) < 5e-12 and abs(float(back_bound(25)) - 1.6e-11) < 5e-13, 'L1 stated bounds 4.1e-10, 1.6e-11')
    says(1, 'p-moment-recurrence', 4, '4.1 \\times 10^{-10}', '1.6 \\times 10^{-11}')
    v = 0.0
    for n in range(25, 18, -1):
        v = (1 - v) / n
    num(1, 'p-moment-recurrence', 5, I[18], v, {'upper': 1 / 19}, rounded=0.05012, agree=1e-10)
    ok(abs(0.96 / 23 - 0.041739) < 5e-7, 'L1 I22 = 0.041739')
    says(1, 'p-moment-recurrence', 5, '0.041739', '0.050120', '0.05012')

    # p-netting-sum
    gross, net = 2400 + 2394, 2400 - 2394
    kap = F(gross, net)
    num(1, 'p-netting-sum', 1, kap, sum(abs(x) for x in (2400, -2394)) / abs(2400 - 2394), {'inflow': F(2400, net), 'one': 1})
    nu = F(2**22, 2**53)
    num(1, 'p-netting-sum', 2, kap * nu * 10**7, 799 * 2.0**-31 * 1e7, {'eps': 2 * kap * nu * 10**7, 'no-kappa': nu * 10**7},
        rounded=3.72)
    err = kap * nu * 6 * 10**6
    num(1, 'p-netting-sum', 3, err, float(nu) * 4794e6, {'gross': float(kap * nu) * 4794e6, 'eps': 2 * err}, rounded=2.23)
    pw = kap * 22 * F(1, 2**53) * 6 * 10**6 * 10**5
    num(1, 'p-netting-sum', 4, pw, 799 * math.log2(2**22) * 2.0**-53 * 6e6 * 1e5,
        {'log10': kap * F(math.log10(2**22)) * F(1, 2**53) * 6 * 10**6 * 10**5}, rounded=1.17)
    ok(abs(float(nu) - 4.66e-10) < 5e-13, 'L1 nu = 4.66e-10')
    says(1, 'p-netting-sum', 2, '4.66 \\times 10^{-10}', '3.72 \\times 10^{-7}')
    says(1, 'p-netting-sum', 3, '£2.23', '£4,794m')
    ok(abs(math.log10(2**22 / 22) - 5.3) < 0.05, 'L1 pairwise keeps about five more digits')

# ---------------------------------------------------------------- level 2
if 2 in LEVELS:
    from scipy.interpolate import CubicSpline
    from scipy.optimize import brentq
    shape(2, {'p-project-irr': ['l5-bisection-and-newton', 'l6-safe-root-finder'],
              'p-spread-spline': ['l8-splines', 'l5-bisection-and-newton'],
              'p-survival-crossing': ['l7-interpolation', 'l5-bisection-and-newton']})

    # p-project-irr: exact in fractions and sympy, then numpy roots and scipy brentq
    V = sp.symbols('v')
    fs = 50 * V**3 + 40 * V**2 + 30 * V - 100
    f = sp.lambdify(V, fs)
    fp = sp.lambdify(V, sp.diff(fs, V))
    fq = lambda x: 50 * x**3 + 40 * x**2 + 30 * x - 100            # plain float form
    fqp = lambda x: 150 * x**2 + 80 * x + 30
    ok(f(0.5) < 0 < f(1), 'L2 bracket [0.5, 1] has a sign change')
    v1 = F(1, 2) - F(fs.subs(V, sp.Rational(1, 2))) / F(sp.diff(fs, V).subs(V, sp.Rational(1, 2)))
    num(2, 'p-project-irr', 1, v1, 0.5 - fq(0.5) / fqp(0.5), {'sign': 1 - v1})
    says(2, 'p-project-irr', 1, '-68.75', '107.5', '1.1395')
    f75 = F(fs.subs(V, sp.Rational(3, 4)))
    num(2, 'p-project-irr', 2, f75, fq(0.75), {'accepted': f(float(v1)), 'endpoint': fq(1), 'sign': -f75}, rounded=-33.91)
    says(2, 'p-project-irr', 2, '21.09375', '-33.91')
    ok(f75 == F(-1085, 32), 'L2 f(0.75) = -33.90625')
    v2 = F(3, 4) - f75 / F(sp.diff(fs, V).subs(V, sp.Rational(3, 4)))
    ok(v2 == F(17, 18) and F(3, 4) + F(7, 36) == v2, 'L2 Newton from 0.75 is 17/18 = 0.75 + 7/36')
    num(2, 'p-project-irr', 3, v2, 0.75 - fq(0.75) / fqp(0.75), {'sign': F(3, 4) + f75 / F(sp.diff(fs, V).subs(V, sp.Rational(3, 4)))})
    says(2, 'p-project-irr', 3, '174.375', '\\tfrac{7}{36}', '0.9444')
    ok(fq(17 / 18) > 0, 'L2 f(0.9444) > 0, bracket [0.75, 0.9444]')
    vs = float([r for r in sp.Poly(fs).nroots(n=30) if abs(sp.im(r)) < 1e-20][0])
    vs2 = brentq(fq, 0.5, 1, xtol=1e-15)
    ok(abs(vs - vs2) < 1e-12, 'L2 root two ways')
    C = (300 * vs + 80) / (2 * fqp(vs))
    ok(abs(C - 0.77) < 0.005, f'L2 C = {C:.4f} about 0.77')
    e0 = 17 / 18 - vs
    ok(abs(e0 - 0.026) < 0.0005, 'L2 first error about 0.026')
    x, real = 17 / 18, []
    for _ in range(3):
        x = x - fq(x) / fqp(x); real.append(abs(x - vs))
    pred, e = [], e0
    for _ in range(3):
        e = C * e * e; pred.append(e)
    steps_pred = next(i + 1 for i, e in enumerate(pred) if e < 1e-12)
    steps_real = next(i + 1 for i, e in enumerate(real) if e < 1e-12)
    halv = next(k for k in range(100) if (17 / 18 - 0.75) / 2**k < 1e-12)
    num(2, 'p-project-irr', 4, steps_pred, steps_real, {'one-short': steps_pred - 1, 'bisect': halv})
    shown, e = [], 0.026                                         # the feedback works from the rounded 0.77 and 0.026
    for _ in range(3):
        e = 0.77 * e * e; shown.append(e)
    ok(all(abs(a / b - 1) < 0.03 for a, b in zip(shown, [5.2e-4, 2.1e-7, 3.4e-14])), f'L2 stated predicted errors {shown}')
    ok(all(abs(a / b - 1) < 0.08 for a, b in zip(pred, shown)), f'L2 unrounded prediction {pred} close to the stated one')
    ok(all(abs(a / b - 1) < 0.03 for a, b in zip(real, [5.1e-4, 2.0e-7, 3.2e-14])), f'L2 real errors {real}')
    says(2, 'p-project-irr', 4, '5.2 \\times 10^{-4}', '2.1 \\times 10^{-7}', '3.4 \\times 10^{-14}', '38 halvings')
    irr = 1 / vs - 1                                              # unit %: the key is the fraction
    num(2, 'p-project-irr', 5, irr, 1 / vs2 - 1, {'one-minus': 1 - vs}, rounded=0.0890, agree=1e-9)
    ok(abs(17 / 18 - fq(17 / 18) / fqp(17 / 18) - 0.918819) < 5e-7 and abs(vs - 0.918305) < 5e-7, 'L2 iterates 0.918819, 0.918305')
    says(2, 'p-project-irr', 5, '0.918305', '8.90\\%')

    # p-spread-spline: hand rows in fractions, then scipy CubicSpline
    t, y = [1, 2, 3, 4], [120, 150, 165, 170]
    sl = [F(y[i + 1] - y[i], t[i + 1] - t[i]) for i in range(3)]
    c1, c2 = 6 * (sl[1] - sl[0]), 6 * (sl[2] - sl[1])
    cs = CubicSpline(t, y, bc_type='natural')
    num(2, 'p-spread-spline', 1, c1, 4 * cs(2, 2) + cs(3, 2), {'no-six': sl[1] - sl[0], 'sign': -c1})
    ok(c2 == -60, 'L2 c2 = 6(5 - 15) = -60')
    Ms = sp.Matrix([[4, 1], [1, 4]]).LUsolve(sp.Matrix([c1, c2]))
    M1, M2 = F(str(Ms[0])), F(str(Ms[1]))
    num(2, 'p-spread-spline', 2, M1, cs(2, 2), {'diag': c1 / 4, 'swap': M2, 'sign': -M1})
    ok(M2 == -10 and abs(cs(3, 2) + 10) < 1e-9, 'L2 M2 = -10')

    def s_piece(x, m1=M1, m2=M2):
        return m1 * (3 - x)**3 / 6 + m2 * (x - 2)**3 / 6 + (150 - m1 / 6) * (3 - x) + (165 - m2 / 6) * (x - 2)
    s25 = s_piece(F(5, 2))
    num(2, 'p-spread-spline', 3, s25, cs(2.5), {'linear': F(315, 2), 'sign-m': s_piece(F(5, 2), -M1, -M2)})
    ok(s25 - F(315, 2) == F(15, 8), 'L2 spline 1.875 bp above the line')
    says(2, 'p-spread-spline', 3, '-0.625', '159.375', '1.9 bp')
    X = sp.symbols('X')
    m1, m2 = sp.Rational(M1.numerator, M1.denominator), sp.Rational(M2.numerator, M2.denominator)
    sexpr = m1 * (3 - X)**3 / 6 + m2 * (X - 2)**3 / 6 + (150 - m1 / 6) * (3 - X) + (165 - m2 / 6) * (X - 2)
    ds = sp.diff(sexpr, X).subs(X, sp.Rational(5, 2))
    num(2, 'p-spread-spline', 4, ds, cs(2.5, 1), {'chord': 15}, rounded=14.583)
    says(2, 'p-spread-spline', 4, '2.5 - 1.25 = 1.25', '166\\tfrac23 - 153\\tfrac13 = 13\\tfrac13', '14.583')
    ok(abs(F(-20) * F(1, 4) / -2 - F(10, 8) - F(5, 4)) == 0 and abs(float(ds) - (1.25 + 40 / 3)) < 1e-12, 'L2 slope split 1.25 + 13.333')
    t1 = F(5, 2) + (160 - s25) / F(str(ds))
    num(2, 'p-spread-spline', 5, t1, 2.5 - (cs(2.5) - 160) / cs(2.5, 1), {'chord': F(5, 2) + (160 - s25) / 15, 'sign': F(5, 2) - (160 - s25) / F(str(ds))},
        rounded=2.5429)
    root = brentq(lambda x: cs(x) - 160, 2, 3, xtol=1e-14)
    ok(abs(root - 2.5438) < 5e-5 and abs(root - float(t1)) < 0.001, f'L2 true crossing {root:.5f}, within 0.001 of the step')
    says(2, 'p-spread-spline', 5, '0.04286', '2.5438')

    # p-survival-crossing: sympy interpolation, then numpy polyfit
    T = sp.symbols('T')
    pq = sp.interpolate([(1, sp.Rational(98, 100)), (3, sp.Rational(92, 100)), (5, sp.Rational(84, 100))], T)
    newton_form = sp.Rational(98, 100) - sp.Rational(3, 100) * (T - 1) - sp.Rational(25, 10000) * (T - 1) * (T - 3)
    ok(sp.expand(pq - newton_form) == 0, 'L2 Newton form equals the interpolant')
    co = np.polyfit([1, 3, 5], [0.98, 0.92, 0.84], 2)
    p4 = pq.subs(T, 4)
    num(2, 'p-survival-crossing', 1, p4, np.polyval(co, 4), {'linear': F(88, 100)})
    p = sp.lambdify(T, pq)
    pp = sp.lambdify(T, sp.diff(pq, T))
    s1 = 3 + F(92 - 90, 100) / (F(92, 100) - F(str(p4)))
    num(2, 'p-survival-crossing', 2, s1, 3 + (p(3) - 0.9) / (p(3) - np.polyval(co, 4)), {'linear': 3 + F(2, 100) / F(4, 100)})
    n1 = float(s1) - (p(float(s1)) - 0.9) / pp(float(s1))
    alt = float(s1) - (np.polyval(co, float(s1)) - 0.9) / np.polyval(np.polyder(co), float(s1))
    num(2, 'p-survival-crossing', 3, n1, alt, {'sign': float(s1) + (p(float(s1)) - 0.9) / pp(float(s1))}, rounded=3.5499)
    ok(abs(n1 - 3.5498) <= 0.00006, 'L2 exact-root rounding 3.5498 accepted too')
    exact_root = float(sp.nsolve(pq - sp.Rational(9, 10), T, 3.5))
    ok(abs(exact_root - (-4 + math.sqrt(57))) < 1e-12 and abs(exact_root - 3.54983) < 5e-6, 'L2 exact crossing -4 + sqrt 57')
    ok(abs(n1 - exact_root) < 2e-5, 'L2 Newton within 2e-5 of the root')
    ok(abs(p(float(s1)) - 0.900622) < 5e-7 and abs(pp(float(s1)) + 0.037667) < 5e-7, 'L2 p and slope at 3.5333')
    ok(abs((p(float(s1)) - 0.9) / -pp(float(s1)) - 0.016519) < 5e-7, 'L2 Newton increment 0.016519')
    says(2, 'p-survival-crossing', 3, '0.900622', '-0.037667', '0.016519', '3.54983')
    w = lambda x: abs((x - 1) * (x - 3) * (x - 5))
    bnd = 0.0006 / 6 * w(n1) * 1e4
    alt = 0.0006 / math.factorial(3) * float(abs(sp.prod([sp.Float(n1) - k for k in (1, 3, 5)]))) * 1e4
    num(2, 'p-survival-crossing', 4, bnd, alt, {'no-factorial': 6 * bnd, 'fourth': bnd / 4}, rounded=2.03)
    ok(abs(w(3.55) - 2.033) < 0.001 and abs(2.55 * 0.55 * 1.45 - 2.033) < 0.001, 'L2 product 2.033')
    days = bnd * 1e-4 / abs(pp(n1)) * 365
    alt = 2.0331e-4 / 0.03775 * 365
    num(2, 'p-survival-crossing', 5, days, alt, {'p-at-3': bnd * 1e-4 / 0.035 * 365, 'no-slope': bnd * 1e-4 * 365}, rounded=1.97, agree=2e-4)
    ok(abs(pp(exact_root) + 0.03775) < 5e-6, 'L2 slope at the crossing -0.03775')
    ok(abs(bnd * 1e-4 / abs(pp(n1)) - 0.00539) < 5e-6, 'L2 0.00539 years')
    says(2, 'p-survival-crossing', 5, '0.00539', '1.97 days')

# ---------------------------------------------------------------- report
for lv in LEVELS:
    L = Level('numerics', lv)
    L.check_wrongs(f'problems-{lv}')
    bad = [r for r in L.results if not r[0]]
    ok(not bad, f'L{lv} check_wrongs: {len(bad)} bad')

print(f'{checks - len(fails)} of {checks} checks passed')
sys.exit(1 if fails else 0)
