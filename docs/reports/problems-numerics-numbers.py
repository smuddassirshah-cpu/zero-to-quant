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

# ---------------------------------------------------------------- report
for lv in LEVELS:
    L = Level('numerics', lv)
    L.check_wrongs(f'problems-{lv}')
    bad = [r for r in L.results if not r[0]]
    ok(not bad, f'L{lv} check_wrongs: {len(bad)} bad')

print(f'{checks - len(fails)} of {checks} checks passed')
sys.exit(1 if fails else 0)
