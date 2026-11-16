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
LEVELS = [n for n in (1, 2, 3, 4) if os.path.exists(os.path.join(COURSE, f'problems-{n}.json'))]


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

# ---------------------------------------------------------------- level 3
if 3 in LEVELS:
    from scipy.integrate import quad
    from scipy.special import ndtr
    shape(3, {'p-normal-cdf-quadrature': ['l9-quadrature', 'l10-gaussian-quadrature'],
              'p-stiff-credit-trapezoid': ['l9-quadrature', 'l11-step-size', 'l12-stiff-equations'],
              'p-rate-path-euler': ['l9-quadrature', 'l11-step-size']})

    # p-normal-cdf-quadrature: mpmath at 50 digits, then plain floats and numpy leggauss
    fm = lambda x: mp.e**(-mp.mpf(x)**2 / 2)
    ff = lambda x: math.exp(-x * x / 2)
    Im = mp.quad(fm, [0, 1])
    ok(abs(float(Im) - quad(ff, 0, 1, epsabs=1e-14)[0]) < 1e-13 and abs(float(Im) - 0.8556244) < 5e-8, 'L3 I = 0.8556244 two ways')
    ok(abs(float(Im) - float((ndtr(1) - 0.5) * math.sqrt(2 * math.pi))) < 1e-12, 'L3 I = sqrt(2 pi)(Phi(1) - 1/2)')
    ok(abs(ff(0.5) - 0.882497) < 5e-7 and abs(ff(1) - 0.606531) < 5e-7, 'L3 f(0.5), f(1) as printed')
    T1m, T2m = (fm(0) + fm(1)) / 2, (fm(0) + 2 * fm(0.5) + fm(1)) / 4
    T2f = np.trapezoid([ff(0), ff(0.5), ff(1)], dx=0.5) if hasattr(np, 'trapezoid') else np.trapz([ff(0), ff(0.5), ff(1)], dx=0.5)
    num(3, 'p-normal-cdf-quadrature', 1, T2m, T2f, {'one-strip': T1m, 'no-half': (fm(0) + fm(0.5) + fm(1)) / 2}, rounded=0.8429)
    says(3, 'p-normal-cdf-quadrature', 1, '3.371524', '0.0127')
    ok(abs(float(4 * T2m - (fm(0) + 2 * fm(0.5) + fm(1)))) < 1e-12 and abs(float(fm(0) + 2 * fm(0.5) + fm(1)) - 3.371524) < 5e-7, 'L3 bracket sum 3.371524')
    ok(abs(float(Im - T2m) - 0.0127) < 5e-5 and all(-(1 - x * x) * ff(x) < 0 for x in np.linspace(0, 0.999, 50)), 'L3 T2 0.0127 below, f concave')
    S2m = (4 * T2m - T1m) / 3
    simpson = 0.5 / 3 * (ff(0) + 4 * ff(0.5) + ff(1))
    num(3, 'p-normal-cdf-quadrature', 2, S2m, simpson, {'swap': (4 * T1m - T2m) / 3, 'order-one': 2 * T2m - T1m}, rounded=0.8561)
    ok(abs((4 * 0.8429 - 0.8033) / 3 - float(S2m)) < 0.00006, 'L3 rounded inputs still accepted in part 2')
    ok(abs(float(S2m - Im) - 0.00046) < 5e-6 and abs(float(S2m - Im) - 0.0005) < 5e-5, 'L3 Simpson 0.00046 above I')
    says(3, 'p-normal-cdf-quadrature', 2, '0.856086', '0.00046')
    g = mp.mpf(1) / (2 * mp.sqrt(3))
    Gm = (fm(mp.mpf(0.5) - g) + fm(mp.mpf(0.5) + g)) / 2
    xg, wg = np.polynomial.legendre.leggauss(2)
    Gf = sum(0.5 * wi * ff(0.5 + 0.5 * xi) for xi, wi in zip(xg, wg))
    num(3, 'p-normal-cdf-quadrature', 3, Gm, Gf, {'no-factor': 2 * Gm, 'unmapped': 2 * fm(1 / mp.sqrt(3))}, rounded=0.8553)
    ok(abs(float(mp.mpf(0.5) - g) - 0.211325) < 5e-7 and abs(float(fm(mp.mpf(0.5) - g)) - 0.977918) < 5e-7
       and abs(float(fm(mp.mpf(0.5) + g)) - 0.732711) < 5e-7, 'L3 nodes and values as printed')
    ok(abs(float(Im - Gm) - 0.00031) < 5e-6 and abs(float(Im - Gm)) < abs(float(Im - S2m)), 'L3 Gauss off by 0.00031, less than Simpson')
    says(3, 'p-normal-cdf-quadrature', 3, '0.211325', '0.788675', '0.977918', '0.732711', '0.855315', '0.00031')
    Phim = mp.mpf(0.5) + Gm / mp.sqrt(2 * mp.pi)
    num(3, 'p-normal-cdf-quadrature', 4, Phim, 0.5 + Gf / math.sqrt(2 * math.pi), {'no-half': Gm / mp.sqrt(2 * mp.pi), 'two-pi': 0.5 + Gm / (2 * mp.pi)}, rounded=0.8412)
    ok(abs(0.5 + 0.8553 / math.sqrt(2 * math.pi) - float(Phim)) < 0.00006, 'L3 rounded I = 0.8553 accepted in part 4')
    ok(abs(float(ndtr(1)) - 0.841345) < 5e-7 and abs(float(ndtr(1)) - float(Phim) - 1.2e-4) < 5e-6, 'L3 library 0.841345, error 1.2e-4')
    x3, w3 = np.polynomial.legendre.leggauss(3)
    G3 = sum(0.5 * wi * ff(0.5 + 0.5 * xi) for xi, wi in zip(x3, w3))
    ok(abs(float(Im) - G3) / math.sqrt(2 * math.pi) < 1e-6, 'L3 three-node rule below 1e-6 in Phi(1)')
    says(3, 'p-normal-cdf-quadrature', 4, '2.506628', '0.841345', '1.2 \\times 10^{-4}')

    # p-stiff-credit-trapezoid: exact amplification factors in fractions and closed forms, then a 2 by 2 trapezoidal run
    l1, l2, TT = -0.3, -2500, 5
    trR = lambda z: (1 + z / 2) / (1 - z / 2)
    errs = {h: trR(l1 * h)**round(TT / h) - math.exp(l1 * TT) for h in (0.5, 0.25)}
    A2 = np.diag([l1, l2]); I2 = np.eye(2)
    def trap_run(h, n):
        y = np.array([1.0, 1.0]); Mx = np.linalg.solve(I2 - h / 2 * A2, I2 + h / 2 * A2)
        for _ in range(n): y = Mx @ y
        return y
    for h in (0.5, 0.25):
        ok(abs(trap_run(h, round(TT / h))[0] - math.exp(l1 * TT) - errs[h]) < 1e-12, f'L3 slow error at h={h} two ways')
    ok(abs(errs[0.5] + 6.288e-4) < 5e-8 and abs(errs[0.25] + 1.570e-4) < 5e-8, f'L3 stated errors {errs}')
    pB = math.log2(6.288 / 1.570)
    num(3, 'p-stiff-credit-trapezoid', 1, pB, math.log(6.288e-4 / 1.570e-4) / math.log(2), {'ratio': 6.288 / 1.570, 'log10': math.log10(6.288 / 1.570)}, rounded=2.00)
    ok(abs(math.log2(errs[0.5] / errs[0.25]) - 2) < 0.01, 'L3 unrounded errors also show order 2')
    says(3, 'p-stiff-credit-trapezoid', 1, '4.005')
    CB = F('1.570e-4') / F(1, 16)
    nB = math.ceil(TT / math.sqrt(1e-5 / float(CB)))
    nB2 = next(n for n in range(1, 10**5) if float(CB) * (TT / n)**2 < 1e-5)
    num(3, 'p-stiff-credit-trapezoid', 2, nB, nB2, {'order-one': math.ceil(TT / (1e-5 / (1.570e-4 / 0.25))), 'floor': nB - 1})
    ok(CB == F('2.512e-3') and abs(float(CB) * (TT / 79)**2 - 1.006e-5) < 5e-9, 'L3 C = 2.512e-3, 79 steps predict 1.006e-5')
    ok(abs(trap_run(TT / 80, 80)[0] - math.exp(l1 * TT)) < 1e-5 and abs(TT / math.sqrt(1e-5 / float(CB)) - 79.2) < 0.05, 'L3 80 real steps meet 1e-5; n >= 79.2')
    rk4R = lambda z: 1 + z + z * z / 2 + z**3 / 6 + z**4 / 24
    zb = brentq(lambda z: rk4R(z) - 1, -3, -2.5)
    ok(abs(zb + 2.7853) < 5e-5 and math.ceil(TT * 2500 / -zb) == 4488 and abs(TT * 2500 / 2.7853 - 4488) < 0.5, f'L3 RK4 limit {zb}, 4,488 steps')
    says(3, 'p-stiff-credit-trapezoid', 2, '2.512 \\times 10^{-3}', '0.0631', '79.2', '4{,}488', '1.006 \\times 10^{-5}')
    zB = F(TT, 80) * l2
    RB = (1 + zB / 2) / (1 - zB / 2)
    Mx = np.linalg.solve(I2 - TT / 160 * A2, I2 + TT / 160 * A2)
    num(3, 'p-stiff-credit-trapezoid', 3, RB, Mx[1, 1], {'sign': -RB, 'implicit': 1 / (1 - zB), 'euler': 1 + zB}, rounded=-0.9747)
    ok(zB == F(-625, 4) and RB == F(-617, 633), 'L3 z = -156.25, factor -77.125/79.125')
    says(3, 'p-stiff-credit-trapezoid', 3, '-156.25', '78.125', '-77.125', '79.125')
    left = float(RB)**80
    num(3, 'p-stiff-credit-trapezoid', 4, left, trap_run(TT / 80, 80)[1], {'sign': -left, 'true': math.exp(-12500)}, rounded=0.129)
    ok(abs(0.9747**80 - left) < 0.0006, 'L3 rounded factor 0.9747 still accepted')
    ok(abs(left / 1e-5 - 13000) < 200 and 1 - zB == F(629, 4), 'L3 13,000 times the tolerance; implicit factor 1/157.25')
    says(3, 'p-stiff-credit-trapezoid', 4, '0.129', '13%', '13,000', '157.25')

    # p-rate-path-euler: Euler products in exact fractions, then a float loop
    def euler_exact(n):
        h, P = F(4, n), F(1)
        for k in range(n): P *= 1 - h * (F(2, 100) + F(1, 100) * k * h)
        return P
    def euler_float(n):
        h, P = 4 / n, 1.0
        for k in range(n): P += h * -(0.02 + 0.01 * k * h) * P
        return P
    ys = {n: euler_exact(n) for n in (4, 8, 16)}
    for n in ys:
        ok(abs(float(ys[n]) - euler_float(n)) < 1e-12, f'L3 Euler {n} steps two ways')
    ok(ys[4] == F(8669472, 10**7), 'L3 four steps 0.98 x 0.97 x 0.96 x 0.95')
    y4, y8, y16 = (F(f'{float(ys[n]):.6f}') for n in (4, 8, 16))
    ok((y4, y8, y16) == (F('0.866947'), F('0.859366'), F('0.855710')), 'L3 printed runs')
    pC = math.log2((y4 - y8) / (y8 - y16))
    num(3, 'p-rate-path-euler', 1, pC, math.log((ys[4] - ys[8]) / (ys[8] - ys[16])) / math.log(2), {'ratio': (y4 - y8) / (y8 - y16), 'flip': -pC},
        rounded=1.05, agree=1e-3)
    says(3, 'p-rate-path-euler', 1, '0.007581', '0.003656', '2.074')
    est = (y8 - y16) / (2**1 - 1)
    num(3, 'p-rate-path-euler', 2, est, float(ys[8] - ys[16]), {'p-two': est / 3, 'sign': -est}, agree=1e-6)
    Pex = mp.e**(-mp.mpf('0.16'))
    trueP = float(mp.quad(lambda t: 0.02 + 0.01 * t, [0, 4]))
    ok(abs(trueP - 0.16) < 1e-15, 'L3 integral of r is 0.16')
    ok(abs(float(ys[16]) - float(Pex) - 0.00357) < 5e-6, 'L3 true error of the 16-step value about 0.00357')
    ex = y16 - est
    num(3, 'p-rate-path-euler', 3, ex, 2 * float(ys[16]) - float(ys[8]), {'added': y16 + est, 'p-two': y16 - est / 3}, rounded=0.85205, agree=1e-6)
    ok(abs(float(ex) - float(Pex)) < 1e-4 and float(y16) - float(Pex) > 3e-3, 'L3 extrapolated within 1e-4; runs off by over 3e-3')
    Cc = est / F(1, 4)
    nC = math.ceil(4 / (1e-5 / float(Cc)))
    nC2 = next(n for n in range(5000, 7000) if float(Cc) * 4 / n < 1e-5)
    num(3, 'p-rate-path-euler', 4, nC, nC2, {'p-two': math.ceil(4 / math.sqrt(1e-5 / float(est / F(1, 16)))), 'floor': nC - 1})
    ok(Cc == F('0.014624') and abs(float(Cc) * 4 / 5849 - 1.0001e-5) < 5e-10 and abs(float(est) / 1e-5 - 365.6) < 1e-9, 'L3 C, 5,849 predicts 1.0001e-5, ratio 365.6')
    ok(abs(euler_float(5850) - float(Pex)) < 1e-5, 'L3 5,850 real Euler steps meet 1e-5')
    says(3, 'p-rate-path-euler', 4, '0.014624', '6.84 \\times 10^{-4}', '5{,}849.6', '365.6')
    trap1 = F(4, 2) * (F(2, 100) + F(6, 100))
    num(3, 'p-rate-path-euler', 5, mp.e**(-mp.mpf(float(trap1))), math.exp(-trueP),
        {'no-exp': 1 - trap1, 'no-minus': math.exp(0.16), 'left-end': math.exp(-0.08)})
    ok(trap1 == F(16, 100) and abs(float(ex) - float(Pex) + 9e-5) < 5e-6, 'L3 one strip exact; Richardson off by 9e-5')
    says(3, 'p-rate-path-euler', 5, '0.852144', '9 \\times 10^{-5}')

# ---------------------------------------------------------------- level 4 (second author, appended)
if 4 in LEVELS:
    from scipy.linalg import lu, solve_banded
    from scipy.optimize import brentq
    from scipy.stats import norm as _norm
    shape(4, {'p-hand-implicit-put': ['l13-finite-differences', 'l14-implicit-and-crank-nicolson'],
              'p-pilot-control': ['l15-monte-carlo-error', 'l16-control-variates'],
              'p-grid-node-budget': ['l13-finite-differences', 'l14-implicit-and-crank-nicolson', 'l17-three-ways'],
              'p-digital-pairs': ['l15-monte-carlo-error', 'l16-control-variates']})

    # p-hand-implicit-put: the matrix rebuilt from sigma, r, dtau, then Thomas in fractions, numpy LU and solve
    sg2, rr, dt = F(1, 4), F(4, 100), F(1, 2)
    al = lambda j: dt * (sg2 * j * j - rr * j) / 2
    ga = lambda j: dt * (sg2 * j * j + rr * j) / 2
    dg = lambda j: 1 + dt * (sg2 * j * j + rr)
    Amat = [[dg(1), -ga(1), 0], [-al(2), dg(2), -ga(2)], [0, -al(3), dg(3)]]
    ok(Amat == [[F('1.145'), F('-0.0725'), 0], [F('-0.23'), F('1.52'), F('-0.27')], [0, F('-0.5325'), F('2.145')]], 'L4 A matrix from the coefficients')
    rhs1 = 20 + al(1) * 30 * mp.e**(-mp.mpf('0.02'))
    ok(abs(float(rhs1) - 21.5438) < 5e-5, 'L4 A first right side 21.5438 holds the bottom edge 30e^-0.02')
    cw = 1 - dt * (sg2 * 9 + rr)
    num(4, 'p-hand-implicit-put', 1, cw, 2 - float(dg(3)),
        {'no-r': 1 - dt * sg2 * 9, 'no-dt': 1 - (sg2 * 9 + rr), 'diag': dg(3), 'no-square': 1 - dt * (sg2 * 3 + rr), 'sign': -cw})
    says(4, 'p-hand-implicit-put', 1, '-0.145', '2.29', '2.145')
    An = np.array([[float(x) for x in row] for row in Amat])
    P_, L_, U_ = lu(An)
    ok(np.allclose(P_, np.eye(3)), 'L4 A no pivoting in LU')
    m2 = F('-0.23') / F('1.145')
    b2 = F('1.52') - m2 * F('-0.0725')
    num(4, 'p-hand-implicit-put', 2, b2, U_[1, 1],
        {'plus': F('1.52') + m2 * F('-0.0725'), 'wrong-c': F('1.52') - m2 * F('-0.27')}, rounded=1.5054)
    d1 = F('21.5438')
    d2 = 10 - m2 * d1
    ok(abs(float(d2) - 14.3276) < 5e-5, 'L4 A d2 prints 14.3276')
    says(4, 'p-hand-implicit-put', 2, '-0.20087', '1.5054', '14.3276', '0.0146')
    m3 = F('-0.5325') / F('1.5054')
    b3 = F('2.145') - m3 * F('-0.27')
    d3 = -m3 * F('14.3276')
    V3 = d3 / b3
    Vn = np.linalg.solve(An, np.array([21.5438, 10.0, 0.0]))
    num(4, 'p-hand-implicit-put', 3, V3, Vn[2], {'no-pivot': d3 / F('2.145'), 'zero': 0}, rounded=2.473, agree=1e-4)
    ok(abs(float(m3) + 0.35373) < 5e-6 and abs(float(b3) - 2.0495) < 5e-5 and abs(float(d3) - 5.0681) < 5e-5, 'L4 A m3, b3, d3 printed')
    V2 = (F('14.3276') + F('0.27') * F('2.4728')) / F('1.5054')
    num(4, 'p-hand-implicit-put', 4, V2, Vn[1],
        {'sign': (F('14.3276') - F('0.27') * F('2.4728')) / F('1.5054'), 'skip': F('14.3276') / F('1.5054'),
         'no-div': F('14.3276') + F('0.27') * F('2.4728')}, rounded=9.96, agree=1e-4)
    ok(abs(Vn[0] - 19.45) < 0.005 and abs(float(F('14.3276') + F('0.27') * F('2.4728')) - 14.9953) < 5e-5, 'L4 A V1 19.45 and 14.9953')

    def bs_put(S, K, r, s, T):
        d1_ = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T))
        return K * math.exp(-r * T) * _norm.cdf(-(d1_ - s * math.sqrt(T))) - S * _norm.cdf(-d1_)

    def grid_put(S0, K, r, s, T, Smax, M, Nst, theta, start):
        dS, dtt = Smax / M, T / Nst
        j = np.arange(M + 1)
        V = np.maximum(K - j * dS, 0.0)
        a_, b_, c_ = 0.5 * (s * s * j * j - r * j), -(s * s * j * j + r), 0.5 * (s * s * j * j + r * j)
        for n in range(Nst):
            th = 1.0 if n < start else theta
            v0 = K * math.exp(-r * (n + 1) * dtt)
            LV = a_[1:-1] * V[:-2] + b_[1:-1] * V[1:-1] + c_[1:-1] * V[2:]
            rhs = V[1:-1] + (1 - th) * dtt * LV
            rhs[0] += th * dtt * a_[1] * v0
            if th == 0:
                V[1:-1] = rhs
            else:
                ab = np.zeros((3, M - 1))
                ab[0, 1:], ab[1, :], ab[2, :-1] = -th * dtt * c_[1:-2], 1 - th * dtt * b_[1:-1], -th * dtt * a_[2:-1]
                V[1:-1] = solve_banded((1, 1), ab, rhs)
            V[0], V[-1] = v0, 0.0
        return float(np.interp(S0, j * dS, V))

    ok(abs(bs_put(20, 30, 0.04, 0.5, 0.5) - 10.00) < 0.005 and abs(grid_put(20, 30, 0.04, 0.5, 0.5, 40, 4, 1, 1.0, 1) - float(V2)) < 1e-3,
       'L4 A formula 10.00 and one implicit step 9.96, error about 4p')
    says(4, 'p-hand-implicit-put', 4, '9.96', '19.45', '£10.00', '4p')

    # p-pilot-control: fractions, then the rho form, brute searches and a root find
    vy, vx, cv, bh = F(64), F(100), F(77), F('0.77')
    res = vy - 2 * bh * cv + bh * bh * vx
    rho = F(77, 80)                                          # 77 / sqrt(64 x 100)
    num(4, 'p-pilot-control', 1, res, float(vy * (1 - rho**2)),
        {'b-one': vy - 2 * cv + vx, 'plus': vy + 2 * bh * cv + bh * bh * vx, 'one-minus-rho': vy * (1 - rho)})
    ok(res == F('4.71') and bh == cv / vx and abs(math.sqrt(64 * 100) - 80) < 1e-12, 'L4 B 4.71, b = Cov/Var(X), rho 77/80')
    says(4, 'p-pilot-control', 1, '118.58', '59.29', '0.9625', '0.0736')
    z2 = F('1.96') ** 2
    ceil = lambda q: -((-q.numerator) // q.denominator)
    ncv = ceil(z2 * F('4.71') / F('0.02') ** 2)
    ncv2 = next(n for n in range(40000, 50000) if 1.96 * math.sqrt(4.71 / n) <= 0.02 + 1e-15)
    npl = ceil(z2 * 64 / F('0.02') ** 2)
    num(4, 'p-pilot-control', 2, ncv, ncv2,
        {'no-196': ceil(F('4.71') / F('0.0004')), 'two': ceil(4 * F('4.71') / F('0.0004')), 'plain': npl,
         'no-square': ceil(F('1.96') * F('4.71') / F('0.0004'))})
    ok(npl == 614656 and abs(float(z2 * F('4.71') / F('0.0004')) - 45234.84) < 1e-9, 'L4 B 614,656 and 45,234.8')
    gain = F(npl) / (F('1.3') * ncv)
    num(4, 'p-pilot-control', 3, gain, float(64 / 4.71 / 1.3), {'no-cost': F(npl, ncv), 'times': F(npl) * F('1.3') / ncv}, rounded=10.45, agree=1e-4)
    says(4, 'p-pilot-control', 3, '58{,}805.5', '13.59', '10.45')
    be = brentq(lambda c: c * 4.71 - 64, 1, 100)
    num(4, 'p-pilot-control', 4, F(64) / F('4.71'), be, {'se': math.sqrt(13.59), 'gain': gain}, rounded=13.59)

    # p-grid-node-budget: gcd and divisor search, bound by fractions and loops, a real explicit and CN grid
    Mn = 276 // math.gcd(math.gcd(76, 92), 276)
    Mn2 = min(M for M in range(1, 300) if all((x * M) % 276 == 0 for x in (76, 92)))
    num(4, 'p-grid-node-budget', 1, Mn, Mn2, {'half': 138, 'pound': 276})
    Tq, s2q, rq = F(3, 4), F(9, 100), F(3, 100)
    nbound = lambda M: Tq * (s2q * M * M + rq)
    nmin = lambda M: next(n for n in range(1, 10000) if Tq / n <= 1 / (s2q * M * M + rq))
    num(4, 'p-grid-node-budget', 2, ceil(nbound(69)), nmin(69),
        {'no-T': ceil(s2q * 69 * 69 + rq), 'down': nbound(69).numerator // nbound(69).denominator, 'no-square': ceil(Tq * (s2q * 69 + rq))})
    ok(abs(float(nbound(69)) - 321.39) < 5e-3 and float(s2q * 69 * 69 + rq) == 428.52, 'L4 C 428.52 and 321.39')
    ex = bs_put(76, 92, 0.03, 0.3, 0.75)
    e69 = grid_put(76, 92, 0.03, 0.3, 0.75, 276, 69, 322, 0.0, 0) - ex
    ok(abs(e69 + 0.0219) < 5e-5, f'L4 C explicit error at M = 69 is -0.0219 ({e69})')
    kk = next(k for k in range(1, 20) if 0.0219 / k**2 < 0.002)
    e207 = grid_put(76, 92, 0.03, 0.3, 0.75, 276, 207, ceil(nbound(207)), 0.0, 0) - ex
    e276 = grid_put(76, 92, 0.03, 0.3, 0.75, 276, 276, ceil(nbound(276)), 0.0, 0) - ex
    real_M = min(M for M in (69, 138, 207, 276, 345) if abs(grid_put(76, 92, 0.03, 0.3, 0.75, 276, M, ceil(nbound(M)), 0.0, 0) - ex) < 0.002)
    num(4, 'p-grid-node-budget', 3, 69 * kk, real_M,
        {'linear': 69 * next(k for k in range(1, 30) if 0.0219 / k < 0.002), 'off-node': math.ceil(69 * math.sqrt(0.0219 / 0.002)), 'k3': 207})
    ok(abs(e207) > 0.002 and abs(e276 + 0.00137) < 5e-6 and abs(0.0219 / 9 - 0.00243) < 5e-6 and abs(0.0219 / 16 - 0.00137) < 5e-6,
       'L4 C k = 3 fails, k = 4 meets; grid at 276 is -0.00137')
    num(4, 'p-grid-node-budget', 4, ceil(nbound(276)), nmin(276),
        {'scaled': 16 * 322, 'no-T': ceil(s2q * 276 * 276 + rq), 'down': nbound(276).numerator // nbound(276).denominator})
    ok(float(s2q * 276 * 276 + rq) == 6855.87 and abs(float(nbound(276)) - 5141.9) < 5e-2, 'L4 C 6,855.87 and 5,141.9')
    ecn = grid_put(76, 92, 0.03, 0.3, 0.75, 276, 276, 100, 0.5, 2) - ex
    ok(abs(ecn) < 0.002 and abs(ecn + 0.0015) < 5e-5, f'L4 C Crank-Nicolson 100 steps errs -0.0015 ({ecn})')
    num(4, 'p-grid-node-budget', 5, F(276 * 5142, 3 * 276 * 100), 5142 / 300,
        {'no-cost': F(5142, 100), 'scaled': F(5152, 300)}, rounded=17.14)
    ok(276 * 5142 == 1419192 and 3 * 276 * 100 == 82800, 'L4 C work 1,419,192 and 82,800')
    says(4, 'p-grid-node-budget', 5, '1{,}419{,}192', '82{,}800', '-0.0015')

    # p-digital-pairs: fractions, then the 2 by 2 joint table of a pair and a normal-quantile check
    p, D = F(1, 5), F(48)
    sd = D * F(2, 5)
    ok(sd * sd == D * D * p * (1 - p), 'L4 D s squared is 48^2 x 0.16')
    ok(F('0.96') * 50 == D, 'L4 D 0.96 x 50 = 48')
    num(4, 'p-digital-pairs', 1, sd, math.sqrt(48**2 * 0.2 * 0.8),
        {'no-disc': 50 * F(2, 5), 'p-only': 48 * math.sqrt(0.2), 'var': sd * sd})
    num(4, 'p-digital-pairs', 2, sd / 160, 19.2 / math.sqrt(25600),
        {'no-disc': F(20) / 160, 'by-n': sd / 25600, 'var': sd * sd / 160})
    c_ = _norm.ppf(1 - 0.2)
    ok(c_ > 0, 'L4 D strike above the median, so a pair cannot pay twice')
    joint = {(1, 1): F(0), (1, 0): p, (0, 1): p, (0, 0): 1 - 2 * p}
    eb1b2 = sum(pr * a * b for (a, b), pr in joint.items())
    rho_pair = (eb1b2 - p * p) / (p * (1 - p))
    num(4, 'p-digital-pairs', 3, rho_pair, -0.2 / 0.8, {'minus-p': -p, 'sign': -rho_pair, 'cov': -p * p})
    eff = 1 / (1 + rho_pair)
    num(4, 'p-digital-pairs', 4, eff, (0.5 * 368.64) / (0.5 * 368.64 * 0.75),
        {'vrf': 1 / (1 - rho_pair**2), 'inverted': 1 + rho_pair, 'one-minus': 1 / (1 - rho_pair)})
    pv = F(1, 2) * sd * sd * (1 + rho_pair)
    pairs = pv / F(1, 400)
    pairs2 = next(m for m in range(50000, 60000) if math.sqrt(138.24 / m) <= 0.05 + 1e-15)
    num(4, 'p-digital-pairs', 5, pairs, pairs2,
        {'payoffs': 2 * pairs, 'plain': sd * sd / F(1, 400), 'one-minus': F(1, 2) * sd * sd * (1 - rho_pair) / F(1, 400)})
    ok(pv == F('138.24') and F(147456, 110592) == eff, 'L4 D pair variance 138.24; 147,456 / 110,592 is the efficiency')
    says(4, 'p-digital-pairs', 5, '138.24', '55{,}296', '110,592', '147,456')

# ---------------------------------------------------------------- report
for lv in LEVELS:
    L = Level('numerics', lv)
    L.check_wrongs(f'problems-{lv}')
    bad = [r for r in L.results if not r[0]]
    ok(not bad, f'L{lv} check_wrongs: {len(bad)} bad')

print(f'{checks - len(fails)} of {checks} checks passed')
sys.exit(1 if fails else 0)
