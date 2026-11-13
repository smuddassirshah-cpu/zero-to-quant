"""Recompute every number in app/content/courses/analysis/problems-1.json to problems-5.json twice.

Method 1 is exact (fractions or sympy: simplify, solve, limit, summation, apart). Method 2 is independent: a brute
search over whole numbers, a float or mpmath simulation, or a large-n table. For each numeric part the script checks
that the two methods agree, that the JSON key lies within its tol of the value, that the value at the rounding the
question asks for is accepted, that every `wrong` value equals its named slip recomputed here, has a byKey line and lies
outside the key's band. Expression parts: the key and every accepted form equal the sympy truth and every wrong form
differs. Choice parts: the keyed option is the one expected. Levels 4 and 5 also check set shape (typed share, difficulty, skills,
lessons drawn on) and numeric sets (`answers`) with their slips. Stated figures in feedback and explain are checked as text.
numbers_lib.Level.check_wrongs runs over each set as a second check of the bands. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-analysis-numbers.py
"""
import json, os, sys, math
from fractions import Fraction as F
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'analysis')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0
n, N, k, q, eps, s = sp.symbols('n N k q varepsilon s', positive=True)


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
        print('BAD', msg)


def load(lv):
    d = json.load(open(os.path.join(COURSE, f'problems-{lv}.json')))
    return {it['id']: it for it in d['items']}


SETS = {lv: load(lv) for lv in (1, 2, 3)}


def part(lv, iid, p):
    return SETS[lv][iid]['parts'][p - 1]


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
    ok(set(ids) == set(slips), f'{tag} wrong ids {sorted(ids)} match slips {sorted(slips)}')
    by = pt['feedback'].get('byKey', {})
    for wid, val in slips.items():
        if wid not in ids:
            continue
        x = ids[wid]
        ok(abs(x['value'] - float(val)) <= max(x['tol']['abs'], 1e-9), f'{tag} wrong {wid} = {x["value"]} matches slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + x['tol']['abs'], f'{tag} wrong {wid} outside the band')
        ok(wid in by, f'{tag} wrong {wid} has a byKey line')
    vals = [x['value'] for x in w.get('wrong', [])]
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            ti, tj = w['wrong'][i]['tol']['abs'], w['wrong'][j]['tol']['abs']
            ok(abs(vals[i] - vals[j]) > ti + tj, f'{tag} wrongs {i} and {j} do not overlap')
    if w['answer'] < 0:
        ok(any(abs(v - abs(w['answer'])) <= 1e-9 + t['tol']['abs'] for v, t in zip(vals, w['wrong'])), f'{tag} negative key has its absolute value as a wrong')


def _group(t, i):
    """Return (content, end) of the brace group that starts at t[i] == '{'."""
    depth = 0
    for j in range(i, len(t)):
        depth += {'{': 1, '}': -1}.get(t[j], 0)
        if depth == 0:
            return t[i + 1:j], j + 1
    raise ValueError(t)


def _plain(t):
    """The small TeX subset these sets use (frac, braces) as sympy text."""
    out, i = '', 0
    while i < len(t):
        if t.startswith('\\frac', i):
            a, i = _group(t, i + 5)
            b, i = _group(t, i)
            out += f'(({_plain(a)})/({_plain(b)}))'
        elif t[i] == '{':
            a, i = _group(t, i)
            out += f'({_plain(a)})'
        else:
            out += t[i]
            i += 1
    return out


def tex(t):
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    t = t.replace('\\varepsilon', 'EPS').replace('\\cdot', '*').replace('\\left', '').replace('\\right', '')
    return parse_expr(_plain(t).replace('^', '**'), local_dict={'EPS': eps, 'n': n, 'N': N, 'k': k},
                      transformations=standard_transformations + (implicit_multiplication_application,))


def expr(lv, iid, p, truth, wrong_truths):
    pt = part(lv, iid, p)
    w, tag = pt['widget'], f'L{lv} {iid} p{p}'
    ok(w['kind'] == 'expression', f'{tag} is an expression')
    for form in [w['answer']] + w['accept']:
        ok(sp.simplify(tex(form) - truth) == 0, f'{tag} form {form} equals truth')
    ids = {x['id']: x['tex'] for x in w['wrong']}
    ok(set(ids) == set(wrong_truths), f'{tag} wrong ids match')
    for wid, wt in wrong_truths.items():
        e = tex(ids[wid])
        ok(sp.simplify(e - wt) == 0, f'{tag} wrong {wid} is the named slip')
        ok(sp.simplify(e - truth) != 0, f'{tag} wrong {wid} differs from the truth')
        ok(wid in pt['feedback'].get('byKey', {}), f'{tag} wrong {wid} has a byKey line')


def choice(lv, iid, p, key):
    w = part(lv, iid, p)['widget']
    right = [o['id'] for o in w['options'] if o.get('correct')]
    ok(right == [key], f'L{lv} {iid} p{p} keyed option {right} is {key}')
    ok(all(o.get('why') for o in w['options'] if not o.get('correct')), f'L{lv} {iid} p{p} every distractor has a why')


def says(lv, iid, p, field, phrase):
    pt = part(lv, iid, p)
    txt = pt['feedback']['correct'] if field == 'correct' else pt['explain']['text'] if field == 'explain' else pt['question']
    ok(phrase in txt, f'L{lv} {iid} p{p} {field} states {phrase!r}')


def first(pred, start=1, stop=10 ** 6):
    return next(m for m in range(start, stop) if pred(m))


def ceil_above(x):
    """Smallest whole number strictly greater than x."""
    return math.floor(x) + 1


# ---------------------------------------------------------------- Level 1
I = 'p-cube-root-twenty'
lo, hi = F(2), F(3)
for _ in range(4):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if mid ** 3 < 20 else (lo, mid)
alt_lo = F(math.floor(16 * 20 ** (1 / 3)), 16)        # the grid of sixteenths holds the cube root in [43/16, 44/16)
two_lo = F(21, 8)                                      # after three halvings: [2.625, 2.75]
num(1, I, 1, lo, alt_lo, {'right-end': hi, 'one-short': two_lo})
ok(hi == F(11, 4) and lo == F(43, 16), 'L1 P1 interval after 4 halvings is [43/16, 11/4]')
miss = 43 ** 3 - 20 * 16 ** 3
ok(miss == -2413, 'L1 P2 miss -2413')
num(1, I, 2, miss, float((F(43, 16) ** 3 - 20) * 4096), {'sign': -miss, 'squares': 43 ** 2 - 20 * 16 ** 2, 'no-twenty': 43 ** 3 - 16 ** 3})
expr(1, I, 3, (2 * k) ** 3 / 4, {'no-divide': (2 * k) ** 3, 'half-only': (2 * k) ** 3 / 2, 'cube-two': k ** 3 / 2})
sv = F(43, 16)
top, bot = 3 * sv ** 2 + 3 * sv + 1, 20 - sv ** 3
bound = top / bot
n1 = ceil_above(bound)
n1_alt = first(lambda m: 2.6875 ** 3 + (3 * 2.6875 ** 2 + 3 * 2.6875 + 1) / m < 20)
num(1, I, 4, n1, n1_alt, {'round-down': n1 - 1, 'no-plus-one': ceil_above((top - 1) / bot), 'no-ones': ceil_above(3 * sv ** 2 / bot)})
ok(n1 == 53 and ceil_above((top - 1) / bot) == 51 and ceil_above(3 * sv ** 2 / bot) == 37, 'L1 P1 p4 key 53, no-plus-one 51, no-ones 37')
ok(abs(float((top - 1) / bot) - 50.47) < 0.005 and abs(float(3 * sv ** 2 / bot) - 36.78) < 0.005, 'L1 P1 p4 slip bounds 50.47 and 36.78')
ok(top == F(3073046875, 10 ** 8) and bot == F(589111328125, 10 ** 12), 'L1 P1 p4 top 30.73046875 and bottom 0.589111328125')
says(1, I, 4, 'correct', 'about 52.16'); ok(abs(float(bound) - 52.16) < 0.005, 'L1 P1 bound ~52.16')
ok(abs((2.6875 + 1 / 53) ** 3 - 19.82) < 0.005 and (2.6875 + 1 / 53) ** 3 < 20, 'L1 P1 (2.6875+1/53)^3 ~ 19.82 < 20')
ok(abs(float(sv ** 3) - 19.410888671875) < 1e-12 and abs(2.75 ** 3 - 20.796875) < 1e-12 and abs(2.625 ** 3 - 18.087890625) < 1e-12, 'L1 P1 cubes 19.4109, 20.7969 and 18.0879')
ok(sp.Integer(20) ** sp.Rational(1, 3) not in (sp.Rational(1),) and sp.Rational(43, 16) < sp.cbrt(20) < sp.Rational(11, 4), 'L1 P1 cube root of 20 in [2.6875, 2.75]')
choice(1, I, 5, 'root')

I = 'p-climbing-fractions'
a = lambda m: F(5 * m - 4, m + 1)
num(1, I, 1, a(1), min(a(m) for m in range(1, 5000)), {'n-zero': a(0), 'sup': 5})
ok(all(a(m) < a(m + 1) for m in range(1, 3000)), 'L1 P2 the terms climb')
ok([a(m) for m in range(1, 5)] == [F(1, 2), 2, F(11, 4), F(16, 5)], 'L1 P2 first terms 1/2, 2, 11/4, 16/5')
an = (5 * n - 4) / (n + 1)
expr(1, I, 2, sp.simplify(5 - an), {'minus-four': 1 / (n + 1), 'sign': -9 / (n + 1)})
ok(sp.simplify(5 - an - 9 / (n + 1)) == 0, 'L1 P2 gap is 9/(n+1)')
thr = sp.solve(sp.Eq(9 / (n + 1), eps), n)[0]
expr(1, I, 3, thr, {'no-minus-one': 9 / eps, 'flip': 9 * eps - 1})
choice(1, I, 4, 'archimedes')
e = F(4, 1000)
n2 = ceil_above(9 / e - 1)
num(1, I, 5, n2, first(lambda m: a(m) > 5 - e), {'equal': n2 - 1, 'no-minus-one': ceil_above(9 / e)})
ok(F(9, 2250) == e and F(9, 2251) < e, 'L1 P2 gap at 2249 is 0.004, at 2250 below')
ok(abs(9 / 2251 - 0.0039982) < 5e-8, 'L1 P2 9/2251 ~ 0.0039982')

I = 'p-diagonal-fraction'
lst = ['70329', '18096', '42571', '96053', '33418']
diag = [int(x[i]) for i, x in enumerate(lst)]
xdig = ''.join('4' if d == 5 else '5' for d in diag)
xv = F(int(xdig), 10 ** 5)
alt_x = sum(F(4 if int(lst[i][i]) == 5 else 5, 10 ** (i + 1)) for i in range(5))
num(1, I, 1, xv, alt_x, {'diagonal': F(int(''.join(map(str, diag))), 10 ** 5), 'all-five': F(55555, 10 ** 5),
                        'swapped': F(int(''.join('5' if d == 5 else '4' for d in diag)), 10 ** 5)})
ok(diag == [7, 8, 5, 5, 8], 'L1 P3 diagonal digits 7, 8, 5, 5, 8')
A, B = xv, xv + F(1, 10 ** 5)
ok(A < A + F(4, 9) / 10 ** 5 and A + F(5, 9) / 10 ** 5 < B, 'L1 P3 any tail of 4s and 5s keeps x inside (a, b)')
nn = ceil_above(1 / (B - A))
num(1, I, 2, nn, first(lambda m: F(1, m) < B - A, 99990), {'equal': 1 / (B - A)})
mm = math.floor(nn * A) + 1
num(1, I, 3, mm, int(nn * 0.55445) + 1, {'floor': mm - 1, 'used-b': math.floor(nn * B) + 1})
fr = F(mm, nn)
num(1, I, 4, fr, mp.mpf(55446) / 100001, {'n-slip': F(mm, 100000)}, rounded=0.5544545)
ok(A < fr < B, 'L1 P3 m/n lies inside (0.55445, 0.55446)')
ok(abs(float(A * nn) - 55445.55445) < 1e-6, 'L1 P3 na = 55445.55445')
choice(1, I, 5, 'uncountable')

# ---------------------------------------------------------------- Level 2
I = 'p-sum-law-band'
A_n, B_n = (8 * n + 3) / (2 * n + 5), (3 * n - 1) / (n + 1)
ok(sp.limit(A_n, n, sp.oo) == 4 and sp.limit(B_n, n, sp.oo) == 3, 'L2 P4 limits 4 and 3')
expr(2, I, 1, sp.simplify(4 - A_n), {'plus-one': 23 / (2 * n + 5), 'sign': -17 / (2 * n + 5)})
ok(sp.simplify(3 - B_n - 4 / (n + 1)) == 0, 'L2 P4 |b_n - 3| = 4/(n+1)')
ga = lambda m: F(17, 2 * m + 5)
gb = lambda m: F(4, m + 1)
N1 = first(lambda m: all(ga(j) < F(1, 50) for j in range(m, m + 50)))
num(2, I, 2, N1, ceil_above(F(850 - 5, 2)), {'round-down': N1 - 1, 'full-band': first(lambda m: ga(m) < F(1, 25))})
ok(N1 == 423, 'L2 P4 N1 = 423')
ok(abs(float(ga(422)) - 0.02002) < 5e-6 and ga(422) > F(1, 50), 'L2 P4 gap at 422 ~ 0.02002')
N2 = first(lambda m: gb(m) < F(1, 50))
ok(N2 == 200 and gb(199) == F(1, 50), 'L2 P4 N2 = 200, gap at 199 exactly 0.02')
num(2, I, 3, N2, ceil_above(200 - 1), {'equal': N2 - 1, 'full-band': first(lambda m: gb(m) < F(1, 25))})
num(2, I, 4, max(N1, N2), sorted([N1, N2])[-1], {'min': min(N1, N2), 'sum': N1 + N2})
true_gap = lambda m: abs(F(8 * m + 3, 2 * m + 5) + F(3 * m - 1, m + 1) - 7)
ok(all(true_gap(m) == ga(m) + gb(m) for m in range(1, 400)), 'L2 P4 both below their limits: true gap is the sum')
NT = first(lambda m: all(true_gap(j) < F(1, 25) for j in range(m, 2000)))
NT_alt = first(lambda m: 17 / (2 * m + 5) + 4 / (m + 1) < 0.04)
num(2, I, 5, NT, NT_alt, {'proof': max(N1, N2), 'round-down': NT - 1})
ok(NT == 311 and N1 == 423 and N2 == 200 and abs(float(true_gap(310)) - 0.04006) < 5e-6 and abs(float(true_gap(311)) - 0.03993) < 5e-6, 'L2 P4 true N 311 (gaps 0.04006 at 310, 0.03993 at 311), proof 423')

I = 'p-root-recursion'
seq = [mp.mpf(1)]
for _ in range(20):
    seq.append(mp.sqrt(4 * seq[-1] + 21))
ok(seq[1] == 5, 'L2 P5 a_2 = 5')
num(2, I, 1, sp.sqrt(41), seq[2], {'no-root': 41, 'a2': 5}, rounded=6.403)
choice(2, I, 2, 'order')
L = sp.symbols('L')
roots = sp.solve(sp.Eq(L ** 2, 4 * L + 21), L)
Lval = [r for r in roots if r >= 1][0]
num(2, I, 3, Lval, round(float(seq[-1])), {'other-root': [r for r in roots if r < 1][0], 'bound-only': 49})
ok(abs(seq[-1] - 7) < 1e-9, 'L2 P5 the terms close in on 7 numerically')
ok(all(seq[i] < seq[i + 1] < 7 for i in range(15)), 'L2 P5 terms rise and stay below 7')
ap = sp.symbols('ap', positive=True)
ok(sp.simplify((7 - sp.sqrt(4 * ap + 21)) - 4 * (7 - ap) / (7 + sp.sqrt(4 * ap + 21))) == 0, 'L2 P5 identity 7 - a_{n+1} = 4(7 - a_n)/(7 + a_{n+1})')
num(2, I, 4, F(4, 7 + 1), sp.maximum(4 / (7 + ap), ap, sp.Interval(1, sp.oo)), {'no-term': F(4, 7), 'used-a2': F(4, 12)})
ok(max(4 / (7 + float(x)) for x in seq[1:]) <= 0.5, 'L2 P5 every factor is at most 0.5')
n5 = first(lambda m: 6 * F(1, 2) ** (m - 1) < F(1, 1000))
n5_alt = math.floor(math.log2(6000)) + 2
num(2, I, 5, n5, n5_alt, {'no-six': first(lambda m: F(1, 2) ** (m - 1) < F(1, 1000)),
                         'power-n': first(lambda m: 6 * F(1, 2) ** m < F(1, 1000)),
                         'slip-4': first(lambda m: 6 * F(4, 7) ** (m - 1) < F(1, 1000))})
ok(2 ** 12 == 4096 and 2 ** 13 == 8192, 'L2 P5 powers 4096 and 8192')
ok(abs(seq[8] - 6.9997) < 5e-5 and 7 - seq[8] < 0.001 < 7 - seq[7], 'L2 P5 a_9 ~ 6.9997 is the first within 0.001')

I = 'p-two-strands-cauchy'
an6 = lambda m: (-1) ** m * (2 - F(3, m))
ok([an6(m) for m in (1, 2, 3, 4)] == [1, F(1, 2), -1, F(5, 4)], 'L2 P6 first terms 1, 0.5, -1, 1.25')
ev = sp.limit(2 - 3 / n, n, sp.oo)
num(2, I, 1, ev, float(an6(10 ** 6)), {'neg': -ev, 'zero': 0}, agree=1e-5)
od = sp.limit(-(2 - 3 / n), n, sp.oo)
num(2, I, 2, od, float(an6(10 ** 6 + 1)), {'sign': -od, 'first': an6(1)}, agree=1e-5)
step = lambda m: abs(an6(m + 1) - an6(m))
ok(all(step(m) == (2 - F(3, m)) + (2 - F(3, m + 1)) for m in range(2, 300)), 'L2 P6 step formula holds for n >= 2')
num(2, I, 3, sp.limit((2 - 3 / n) + (2 - 3 / (n + 1)), n, sp.oo), float(step(10 ** 6)), {'zero': 0, 'two': 2}, agree=1e-5)
n6 = first(lambda m: step(m) >= 3)
n6_alt = first(lambda m: F(3, m) + F(3, m + 1) <= 1)
num(2, I, 4, n6, n6_alt, {'round-down': n6 - 1, 'index-plus': n6 + 1})
ok(all(step(m) >= 3 for m in range(n6, 2000)), 'L2 P6 every step from n = 6 is at least 3')
ok(step(5) == F(29, 10) and abs(float(step(6)) - 3.071) < 5e-4 and abs(float(step(7)) - 3.196) < 5e-4, 'L2 P6 steps 2.9, 3.071, 3.196')
choice(2, I, 5, 'not-cauchy')

# ---------------------------------------------------------------- Level 3
I = 'p-telescoping-tail'
term = 1 / ((n + 1) * (n + 3))
c = sp.simplify(term / (1 / (n + 1) - 1 / (n + 3)))
num(3, I, 1, c, F(1, 2), {'two': 2, 'one': 1})
ok(sp.apart(term, n) == sp.Rational(1, 2) / (n + 1) - sp.Rational(1, 2) / (n + 3), 'L3 P7 apart gives 1/2 split')
SN = sp.summation(term.subs(n, sp.Symbol('j', positive=True)), (sp.Symbol('j', positive=True), 1, N))
SN = sp.simplify(SN)
expr(3, I, 2, SN, {'no-half': 2 * SN, 'one-left': sp.Rational(5, 12) - 1 / (2 * (N + 3)), 'one-start': sp.Rational(1, 4) - 1 / (2 * (N + 3))})
ok(all(sum(F(1, (j + 1) * (j + 3)) for j in range(1, M + 1)) == F(5, 12) - F(1, 2 * (M + 2)) - F(1, 2 * (M + 3)) for M in range(1, 60)), 'L3 P7 formula matches direct sums')
tot = sp.limit(SN, N, sp.oo)
num(3, I, 3, tot, mp.nsum(lambda j: 1 / ((j + 1) * (j + 3)), [1, mp.inf]), {'no-half': 2 * tot, 'one-start': F(1, 4)}, rounded=0.4167)
tail = lambda M: F(1, 2 * (M + 2)) + F(1, 2 * (M + 3))
n7 = first(lambda M: tail(M) < F(1, 1000))
n7_alt = first(lambda M: 5 / 12 - sum(1 / ((j + 1) * (j + 3)) for j in range(1, M + 1)) < 0.001, 990)
num(3, I, 4, n7, n7_alt, {'one-term': first(lambda M: F(1, 2 * (M + 2)) < F(1, 1000)),
                         'no-half': first(lambda M: F(1, M + 2) + F(1, M + 3) < F(1, 1000)), 'round-down': n7 - 1})
ok(abs(float(tail(997)) - 0.0010005) < 5e-8 and abs(float(tail(998)) - 0.0009995) < 5e-8, 'L3 P7 tails 0.0010005 and 0.0009995')
ok(all(0 < F(1, j * j + 4 * j + 7) < F(1, (j + 1) * (j + 3)) for j in range(1, 500)), 'L3 P7 comparison terms smaller')
ok(abs(mp.nsum(lambda j: 1 / (j * j + 4 * j + 7), [1, mp.inf])) < 5 / 12, 'L3 P7 comparison sum below 5/12')
ok(sp.limit((1 / ((n + 1) ** 2 + 4 * (n + 1) + 7)) / (1 / (n ** 2 + 4 * n + 7)), n, sp.oo) == 1, 'L3 P7 ratio test silent on the second series')
choice(3, I, 5, 'below')

I = 'p-alternating-quarters'
size = n / 4 ** n
r = sp.limit(sp.simplify(size.subs(n, n + 1) / size), n, sp.oo)
num(3, I, 1, r, (10 ** 6 + 1) / (4 * 10 ** 6), {'flip': 1 / r, 'no-four': 1}, agree=1e-5)
choice(3, I, 2, 'absolute')
sz = lambda m: F(m, 4 ** m)
ok(all(sz(m + 1) < sz(m) for m in range(1, 200)), 'L3 P8 sizes decrease from n = 1')
num(3, I, 3, sz(5), 5 / 1024, {'a4': sz(4), 'a6': sz(6)}, rounded=0.0049)
n8 = first(lambda m: sz(m + 1) < F(1, 1000))
n8_alt = first(lambda m: (m + 1) / 4 ** (m + 1) < 0.001)
num(3, I, 4, n8, n8_alt, {'index': n8 + 1, 'round-down': n8 - 1})
ok(first(lambda m: sz(m) < F(1, 1000)) == n8 + 1, 'L3 P8 the a_n slip also gives 7')
ok(abs(float(sz(6)) - 0.00146) < 5e-6 and abs(float(sz(7)) - 0.00043) < 5e-6, 'L3 P8 a_6 ~ 0.00146 and a_7 ~ 0.00043')
S = lambda M: sum((-1) ** (j + 1) * sz(j) for j in range(1, M + 1))
S6 = S(6)
num(3, I, 5, S6, sum((-1) ** (j + 1) * j / 4 ** j for j in range(1, 7)), {'s4': S(4), 'sizes': sum(sz(j) for j in range(1, 7)), 's7': S(7), 'sum': F(4, 25)}, rounded=0.1597)
ok(S6 == F(327, 2048) and sum([1024, -512, 192, -64, 20, -6]) == 654, 'L3 P8 S_6 = 654/4096 = 327/2048')
total = sp.summation((-1) ** (sp.Symbol('j') + 1) * sp.Symbol('j') / 4 ** sp.Symbol('j'), (sp.Symbol('j'), 1, sp.oo))
ok(sp.nsimplify(total) == sp.Rational(4, 25) and abs(mp.nsum(lambda j: (-1) ** (j + 1) * j / 4 ** j, [1, mp.inf]) - 0.16) < 1e-12, 'L3 P8 the sum is 4/25 two ways')
ok(abs(F(4, 25) - S6) < sz(7), 'L3 P8 the true error is inside the bound 0.00043')

I = 'p-cube-root-greedy'
mp.mp.dps = 30
true_sum = (1 - mp.mpf(2) ** (mp.mpf(2) / 3)) * mp.zeta(mp.mpf(1) / 3)
ok(abs(true_sum - mp.nsum(lambda j: (-1) ** (j + 1) / mp.cbrt(j), [1, mp.inf])) < 1e-12 and abs(true_sum - 0.5718) < 5e-5, 'L3 P9 usual sum ~ 0.5718 two ways')
choice(3, I, 1, 'conditional')


def greedy(T, count, cr):
    pos, neg, total, out = 1, 2, 0, []
    for _ in range(count):
        if total <= T:
            t, pos = 1 / cr(pos), pos + 2
        else:
            t, neg = -1 / cr(neg), neg + 2
        total += t
        out.append((t, total))
    return out


g1 = greedy(0.2, 8, lambda m: m ** (1 / 3))
g2 = greedy(mp.mpf('0.2'), 8, mp.cbrt)
num(3, I, 2, g1[1][1], g2[1][1], {'positive': 1 + 3 ** (-1 / 3), 'square-root': 1 - 2 ** -0.5}, rounded=0.2063)
num(3, I, 3, g1[2][0], g2[2][0], {'sign': -g1[2][0], 'positive': 3 ** (-1 / 3), 'odd-neg': -3 ** (-1 / 3)}, rounded=-0.63)
ok(abs(g1[2][1] - (-0.4237)) < 5e-5, 'L3 P9 total after three terms ~ -0.4237')
num(3, I, 4, g1[3][1], g2[3][1], {'negative-again': g1[2][1] - 6 ** (-1 / 3), 'skipped': g1[2][1] + 5 ** (-1 / 3)}, rounded=0.2697)
gl = greedy(0.2, 200000, lambda m: m ** (1 / 3))
# Method 1: the theorem (every crossing happens, the overshoot is at most the last size, sizes tend to 0), so the sum is T.
# Method 2: the simulation's largest distance from T shrinks window by window, towards 0 at the rate of the sizes.
dev = lambda lo, hi: max(abs(t - 0.2) for _, t in gl[lo:hi])
ok(dev(10 ** 3, 2 * 10 ** 3) > dev(10 ** 4, 2 * 10 ** 4) > dev(10 ** 5, 2 * 10 ** 5), 'L3 P9 the swings about T shrink')
ok(dev(10 ** 5, 2 * 10 ** 5) < 2 * (10 ** 5) ** (-1 / 3), 'L3 P9 late swings within the size of the terms used')
crossings = sum(1 for i in range(1, len(gl)) if (gl[i - 1][1] - 0.2) * (gl[i][1] - 0.2) < 0)
ok(crossings > 1000, f'L3 P9 the totals cross T again and again ({crossings} times)')
num(3, I, 5, 0.2, round(sum(t for _, t in gl[-50000:]) / 50000, 1), {'original': 0.5718, 'last-total': 0.2697})
ok(abs(true_sum - 0.2) > 0.3, 'L3 P9 the usual sum differs from T')

# ---------------------------------------------------------------- Levels 4 and 5: helpers
X, KK = sp.symbols('x k', positive=True)


def tex45(t):
    """TeX of the level 4 and 5 expression parts as sympy, with e as Euler's number."""
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    t = t.replace('\\left', '').replace('\\right', '')
    return parse_expr(_plain(t).replace('^', '**'), local_dict={'e': sp.E, 'x': X, 'k': KK, 'n': n},
                      transformations=standard_transformations + (implicit_multiplication_application,))


def expr45(lv, iid, p, truth, wrong_truths):
    pt = part(lv, iid, p)
    w, tag = pt['widget'], f'L{lv} {iid} p{p}'
    ok(w['kind'] == 'expression', f'{tag} is an expression')
    for form in [w['answer']] + w['accept']:
        ok(sp.simplify(tex45(form) - truth) == 0, f'{tag} form {form} equals truth')
        for xv, kv, nv in ((0.7, 1.3, 2.2), (2.9, 0.4, 5.0)):  # second route: numeric at two points
            sub = {X: xv, KK: kv, n: nv}
            ok(abs(float(tex45(form).subs(sub)) - float(truth.subs(sub))) < 1e-9, f'{tag} form {form} equals truth numerically')
    ids = {x['id']: x['tex'] for x in w['wrong']}
    ok(set(ids) == set(wrong_truths), f'{tag} wrong ids match')
    for wid, wt in wrong_truths.items():
        e = tex45(ids[wid])
        ok(sp.simplify(e - wt) == 0, f'{tag} wrong {wid} is the named slip')
        ok(sp.simplify(e - truth) != 0, f'{tag} wrong {wid} differs from the truth')
        ok(wid in pt['feedback'].get('byKey', {}), f'{tag} wrong {wid} has a byKey line')


def numset45(lv, iid, p, exact, alt, slips):
    """A numeric part with `answers` (a set): exact and alt are the set two ways; slips {id: set}."""
    pt = part(lv, iid, p)
    w, tag = pt['widget'], f'L{lv} {iid} p{p}'
    ok(w['kind'] == 'numeric' and w.get('unordered') is True, f'{tag} is an unordered numeric set')
    ok(sorted(exact) == sorted(alt), f'{tag} methods agree {sorted(exact)} vs {sorted(alt)}')
    ok(sorted(w['answers']) == sorted(exact), f'{tag} answers {w["answers"]} are {sorted(exact)}')
    ids = {x['id']: x for x in w.get('wrong', [])}
    ok(set(ids) == set(slips), f'{tag} wrong ids match slips')
    by = pt['feedback'].get('byKey', {})
    ok('count' in by, f'{tag} has a count line')
    for wid, val in slips.items():
        got = sorted(float(v) for v in ids[wid]['value'].split(','))
        ok(got == sorted(val), f'{tag} wrong {wid} = {got} matches slip {sorted(val)}')
        ok(got != sorted(exact) and len(got) == len(exact), f'{tag} wrong {wid} differs with the right count')
        ok(wid in by, f'{tag} wrong {wid} has a byKey line')


def says45(lv, iid, p, field, phrase):
    pt = part(lv, iid, p)
    txt = {'correct': pt['feedback']['correct'], 'explain': pt['explain']['text'], 'question': pt['question']}.get(field)
    if txt is None:
        txt = pt['feedback']['byKey'][field]
    ok(phrase in txt, f'L{lv} {iid} p{p} {field} states {phrase!r}')


def shape45(lv, lessons):
    d = json.load(open(os.path.join(COURSE, f'problems-{lv}.json')))
    course = json.load(open(os.path.join(COURSE, 'course.json')))
    level = [L for L in course['levels'] if L.get('n', L.get('level')) == lv][0]
    skills = set()
    for lid in level['lessons']:
        skills |= set(json.load(open(os.path.join(COURSE, lid + '.json')))['skills'])
    parts = [p for it in d['items'] for p in it['parts']]
    typed = sum(p['widget']['kind'] in ('numeric', 'expression') for p in parts)
    ok(3 <= len(d['items']) <= 5 and all(3 <= len(it['parts']) <= 5 for it in d['items']), f'L{lv} set shape')
    ok(typed * 3 >= 2 * len(parts), f'L{lv} typed parts {typed} of {len(parts)}')
    ok(any(it['difficulty'] == 5 for it in d['items']) and all(3 <= it['difficulty'] <= 5 for it in d['items']), f'L{lv} difficulty')
    ok(all(set(it['skills']) <= skills for it in d['items']), f'L{lv} skills from the level lessons')
    drawn = set().union(*lessons.values())
    ok(drawn == set(level['lessons']) and all(len(v) >= 2 for v in lessons.values()), f'L{lv} every lesson drawn on, two or more a problem')
    for p in parts:
        ok(len([s for s in p['explain']['text'].replace('$', '').split('. ') if s.strip()]) <= 3, f'L{lv} explain at most three sentences')


SETS[4], SETS[5] = load(4), load(5)

# ---------------------------------------------------------------- Level 4
I = 'p-cubic-bracket'
f4 = X ** 3 + 6 * X - 13
ok(f4.subs(X, 0) == -13 and f4.subs(X, 2) == 7, 'L4 P1 f(0) = -13, f(2) = 7')
chord = (f4.subs(X, 2) - f4.subs(X, 0)) / 2
ok(chord == 10, 'L4 P1 chord slope 10')
c_exact = [r for r in sp.solve(sp.diff(f4, X) - chord, X) if 0 < r < 2][0]
c_alt = mp.findroot(lambda t: 3 * t ** 2 + 6 - 10, 1)
num(4, I, 1, c_exact, c_alt, {'no-six': math.sqrt(10 / 3), 'no-root': F(4, 3)}, rounded=1.155)
ok(c_exact == 2 / sp.sqrt(3), 'L4 P1 c = 2/sqrt3')
d4 = sp.diff(f4, X)
K_exact = sp.maximum(d4, X, sp.Interval(0, 2))
K_alt = max(3 * (i / 10000) ** 2 + 6 for i in range(0, 20001))
num(4, I, 2, K_exact, K_alt, {'chord': chord, 'left-end': d4.subs(X, 0), 'no-six': 3 * 2 ** 2})
delta = F(9, 1000) / 18
delta_alt = max(i / 10 ** 7 for i in range(1, 20000) if 18 * F(i, 10 ** 7) <= F(9, 1000))
num(4, I, 3, delta, delta_alt, {'times': F(9, 1000) * 18, 'chord': F(9, 1000) / 10, 'no-six': F(9, 1000) / 12})
halv = first(lambda m: F(2, 2 ** m) <= delta)
halv_alt = math.ceil(math.log2(2 / 0.0005))
num(4, I, 4, halv, halv_alt, {'one-short': halv - 1, 'eps': first(lambda m: F(2, 2 ** m) <= F(9, 1000))})
ok(first(lambda m: F(1, 2 ** m) <= delta) == 11, 'L4 P1 width-1 slip also gives 11')
ok(abs(2 / 2 ** 11 - 0.00098) < 5e-6 and abs(2 / 2 ** 12 - 0.00049) < 5e-6, 'L4 P1 widths 0.00098 and 0.00049')
bound = 18 * F(2, 2 ** halv) / 2  # half the final width 2/2^12 = 1/2048
ok(bound == F(9, 2048) and F(2, 2 ** halv) == F(1, 2048), 'L4 P1 bound 9/2048 from width 1/2048')
lo, hi = mp.mpf(0), mp.mpf(2)  # second route: run the 12 halvings and measure
for _ in range(halv):
    m = (lo + hi) / 2
    lo, hi = (m, hi) if (m ** 3 + 6 * m - 13) < 0 else (lo, m)
mid = (lo + hi) / 2
root = mp.findroot(lambda t: t ** 3 + 6 * t - 13, 1.5)
ok(abs(mid - root) <= mp.mpf(1) / 4096 and abs(mid ** 3 + 6 * mid - 13) <= float(bound), 'L4 P1 the real midpoint obeys the bound')
num(4, I, 5, bound, 18 / 4096, {'full-width': 18 * F(1, 2048), 'eps': F(9, 1000), 'chord': 10 * F(1, 4096)}, rounded=0.00439)
says45(4, I, 5, 'correct', '0.00439')

I = 'p-quartic-roots'
h4 = X ** 4 - 8 * X ** 2 + 3
Y = sp.Symbol('y', real=True)
hy = Y ** 4 - 8 * Y ** 2 + 3
crit = [r for r in sp.solve(sp.diff(hy, Y), Y) if -1 < r < 3]
crit_alt = [round(-1 + i / 1000) for i in range(1, 4000) if (lambda a, b: a * b <= 0)(4 * (-1 + i / 1000) ** 3 - 16 * (-1 + i / 1000), 4 * (-1 + (i + 1) / 1000) ** 3 - 16 * (-1 + (i + 1) / 1000)) and abs(4 * (-1 + i / 1000) ** 3 - 16 * (-1 + i / 1000)) < 0.05]
numset45(4, I, 1, [int(r) for r in crit], sorted(set(crit_alt)), {'lost-zero': [-2, 2]})
cands = {t: hy.subs(Y, t) for t in (-1, 0, 2, 3)}
ok(cands == {-1: -4, 0: 3, 2: -13, 3: 12}, 'L4 P2 candidate values -4, 3, -13, 12')
grid = [(-1 + 4 * i / 200000) for i in range(200001)]
hv = [t ** 4 - 8 * t ** 2 + 3 for t in grid]
num(4, I, 2, max(cands.values()), round(max(hv), 6), {'critical': max(cands[0], cands[2]), 'no-three': 81 - 72})
num(4, I, 3, min(cands.values()), round(min(hv), 6), {'sign': 13, 'left-end': cands[-1]})
choice(4, I, 4, 'at-most-three')
real_roots = [r for r in sp.real_roots(sp.Poly(hy, Y)) if -1 <= r <= 3]
sign_changes = sum(1 for a, b in zip(hv, hv[1:]) if a * b < 0)
ok(len(crit) == 2, 'L4 P2 two zeros of h-prime inside, so Rolle allows at most three roots')
num(4, I, 5, len(real_roots), sign_changes, {'ends': 1, 'degree': 4, 'two': 2})
ok([round(float(r), 2) for r in real_roots] == [-0.63, 0.63, 2.76], 'L4 P2 roots near -0.63, 0.63, 2.76')

I = 'p-bump-series'
fk = X * sp.exp(-KK ** 2 * X)
peak = sp.solve(sp.diff(fk, X), X)
ok(peak == [1 / KK ** 2], 'L4 P3 sympy peak 1/k^2')
for kv in (1, 2, 3, 5):  # second route: grid argmax
    xs = [i / 10 ** 5 for i in range(1, 200001)]
    am = max(xs, key=lambda t: t * math.exp(-kv * kv * t))
    ok(abs(am - 1 / kv ** 2) < 2e-5, f'L4 P3 grid peak at 1/k^2 for k = {kv}')
expr45(4, I, 1, peak[0], {'one-k': 1 / KK, 'flip': KK ** 2})
Mk = sp.simplify(fk.subs(X, peak[0]))
ok(sp.simplify(Mk - 1 / (sp.E * KK ** 2)) == 0, 'L4 P3 M_k = 1/(e k^2)')
for kv in (1, 2, 4):
    ok(abs(max(t * math.exp(-kv * kv * t) for t in [i / 10 ** 5 for i in range(1, 200001)]) - 1 / (math.e * kv * kv)) < 1e-6, f'L4 P3 grid sup matches M_k for k = {kv}')
expr45(4, I, 2, Mk, {'no-e': 1 / KK ** 2, 'one-k': sp.exp(-KK) / KK})
Nst = first(lambda m: 1 / (mp.e * m) < mp.mpf('0.01'))
num(4, I, 3, Nst, ceil_above(100 / math.e), {'round-down': Nst - 1, 'no-e': first(lambda m: F(1, m) < F(1, 100)), 'square': first(lambda m: 1 / (math.e * m * m) < 0.01)})
ok(abs(100 / math.e - 36.79) < 0.005 and abs(1 / (36 * math.e) - 0.0102) < 0.00005, 'L4 P3 36.79 and 1/(36e) ~ 0.0102')
ok(mp.nsum(lambda j: 1 / j ** 2, [38, mp.inf]) < mp.mpf(1) / 37, 'L4 P3 tail of 1/k^2 after 37 below 1/37')
S_tail = lambda t: mp.nsum(lambda j: t * mp.exp(-j * j * t), [38, mp.inf])
ok(max(S_tail(mp.mpf(i) / 10 ** 5) for i in range(1, 300, 7)) < 0.01, 'L4 P3 true tail after 37 terms below 0.01 near its peak')
choice(4, I, 4, 'continuous')
dl = F(1, 100) / 37
num(4, I, 5, dl, 0.01 / 37, {'n36': F(1, 100) / 36, 'whole-eps': F(2, 100) / 37, 'one-term': F(1, 100)}, rounded=0.00027)
ok(F(1, 3700) == dl, 'L4 P3 delta = 1/3700')
Sfull = lambda t: mp.nsum(lambda j: t * mp.exp(-j * j * t), [1, mp.inf])
ok(all(Sfull(mp.mpf(float(dl)) * q) < 0.02 for q in (0.1, 0.5, 0.99)), 'L4 P3 |S(x) - S(0)| < 0.02 inside the window')
ok(all(sum(float(t) * math.exp(-j * j * float(t)) for j in range(1, 38)) <= 37 * float(t) for t in (0.0001, 0.00027, 0.01)), 'L4 P3 S_37(x) <= 37x')
shape45(4, {'p-cubic-bracket': {'l15-epsilon-delta', 'l16-intermediate-value', 'l18-mean-value-proved'},
            'p-quartic-roots': {'l16-intermediate-value', 'l17-extreme-value', 'l18-mean-value-proved'},
            'p-bump-series': {'l19-uniform-convergence', 'l15-epsilon-delta'}})

# ---------------------------------------------------------------- Level 5
I = 'p-root-sums'
U9 = sum(sp.sqrt(j) for j in range(1, 10))
L9 = sum(sp.sqrt(j) for j in range(0, 9))
num(5, I, 1, U9, sum(math.sqrt(j) for j in range(1, 10)), {'lower': L9, 'ninth': U9 / 9}, rounded=19.3060)
ok(U9 - L9 == 3, 'L5 P4 lower sum is 3 less')
says45(5, I, 1, 'correct', '2.82843 + 3 = 19.3060')
ok(abs((1 + 1.41421 + 1.73205 + 2 + 2.23607 + 2.44949 + 2.64575 + 2.82843 + 3) - 19.3060) < 5e-5, 'L5 P4 printed five-place sum gives 19.3060')
j = sp.Symbol('j', integer=True, positive=True)
gap = 9 / n * (sp.sqrt(9 * n / n) - sp.sqrt(0 * n / n))  # the shifted sums cancel but for the last and first heights
ok(sp.simplify(gap - 27 / n) == 0, 'L5 P4 telescoped gap 27/n by sympy')
for nv in (3, 10, 37):
    Uv = sum(9 / nv * math.sqrt(9 * i / nv) for i in range(1, nv + 1))
    Lv_ = sum(9 / nv * math.sqrt(9 * i / nv) for i in range(0, nv))
    ok(abs(Uv - Lv_ - 27 / nv) < 1e-12, f'L5 P4 numeric gap 27/n at n = {nv}')
expr45(5, I, 2, 27 / n, {'unit-width': 3 / n, 'no-height': 9 / n})
integral = sp.integrate(sp.sqrt(X), (X, 0, 9))
ok(sp.diff(sp.Rational(2, 3) * X ** sp.Rational(3, 2), X) == sp.sqrt(X), 'L5 P4 G-prime = sqrt x')
num(5, I, 3, integral, mp.quad(mp.sqrt, [0, 9]), {'no-coeff': 9 ** 1.5, 'flip': 1.5 * 9 ** 1.5}, rounded=18.0000, agree=1e-8)
ok(L9 < integral < U9, 'L5 P4 L9 < 18 < U9')
num(5, I, 4, U9 - integral, sum(math.sqrt(i) for i in range(1, 10)) - 18, {'gap': U9 - L9, 'lower': integral - L9}, rounded=1.3060)
# the part says "Using U_9 ~ 19.3060 ... and 18": that rounded input gives the same 4-place answer
ok(round(19.3060 - 18, 4) == 1.3060 and abs(1.3060 - 1.3060005) <= 5e-5, 'L5 P4 stated input 19.3060 - 18 = 1.3060 is accepted')
says45(5, I, 4, 'explain', '19.30600 - 18 = 1.30600')
nn = first(lambda m: F(27, m) < F(5, 100))
num(5, I, 5, nn, ceil_above(27 / 0.05), {'equal': 540, 'unit-width': first(lambda m: F(3, m) < F(5, 100)), 'no-height': first(lambda m: F(9, m) < F(5, 100))})
ok(nn == 541, 'L5 P4 smallest n is 541')

I = 'p-diamond-ball'
p5 = (F(15, 100), F(-40, 100))
d1 = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])
d1p = d1((0, 0), p5)
num(5, I, 1, d1p, abs(0.15) + abs(-0.4), {'signs': p5[0] + p5[1], 'signs-size': abs(p5[0] + p5[1]), 'straight': math.sqrt(0.1825), 'largest': 0.4})
r5 = 1 - d1p
def fits_d1(rr):
    # corners of the diamond B_1(p, rr) are its extreme points; U is convex
    return all(abs(a) + abs(b) <= 1 + 1e-12 for a, b in ((0.15 + rr, -0.4), (0.15 - rr, -0.4), (0.15, -0.4 + rr), (0.15, -0.4 - rr)))
r_alt = max(i / 10000 for i in range(1, 10000) if fits_d1(i / 10000))
num(5, I, 2, r5, r_alt, {'whole': d1p, 'straight': 1 - math.sqrt(0.1825)})
ok(d1((F(375, 1000), F(-625, 1000)), p5) == F(45, 100) and abs(F(375, 1000)) + abs(F(-625, 1000)) == 1, 'L5 P5 (0.375, -0.625) is at d1 0.45 from p and on the edge')
s5 = sp.Rational(45, 100) / sp.sqrt(2)
s_line = (1 - (0.15 - (-0.4))) / math.sqrt(2)  # distance from p to the edge y1 - y2 = 1
num(5, I, 3, s5, s_line, {'times': 0.45 * math.sqrt(2), 'same': 0.45, 'half': 0.225}, rounded=0.3182)
ok(abs(round(0.45 / 1.414, 4) - 0.3182) < 1e-12 and abs(0.3182 - 0.3181981) <= 6e-5, 'L5 P5 part 3 takes 0.3182 (also from sqrt2 = 1.414)')
t5 = F(45, 100) / 2
t_alt = max(i / 10000 for i in range(1, 10000) if all(abs(0.15 + a * i / 10000) + abs(-0.4 + b * i / 10000) <= 1 + 1e-12 for a in (-1, 1) for b in (-1, 1)))
num(5, I, 4, t5, t_alt, {'times': 0.9, 'root-two': 0.45 / math.sqrt(2), 'same': 0.45})
choice(5, I, 5, 'all')
ok(all(abs(1 - 1 / k_) + 0 < 1 for k_ in range(2, 50)), 'L5 P5 points (1 - 1/n, 0) lie in U')

I = 'p-accumulated-cubic'
t = sp.Symbol('t')
fF = t ** 2 - 12 * t + 27
Fx = sp.integrate(fF, (t, 0, X))
for xv in (0.5, 2.0, 11.5):
    ok(abs(float(Fx.subs(X, xv)) - float(mp.quad(lambda u: u ** 2 - 12 * u + 27, [0, xv]))) < 1e-9, f'L5 P6 F({xv}) by quadrature')
expr45(5, I, 1, Fx, {'no-third': X ** 3 - 6 * X ** 2 + 27 * X, 'no-half': X ** 3 / 3 - 12 * X ** 2 + 27 * X, 'derivative': 2 * X - 12})
ok(sp.factor(Fx) == X * (X - 9) ** 2 / 3, 'L5 P6 F = x(x-9)^2/3')
zf = sorted(sp.solve(fF, t))
zf_alt = sorted({round(i / 1000) for i in range(1, 15000) if abs((i / 1000) ** 2 - 12 * i / 1000 + 27) < 1e-9})
numset45(5, I, 2, [int(z) for z in zf], zf_alt, {'zeros-of-big-f': [0, 9]})
vals = {xv: Fx.subs(X, xv) for xv in (0, 3, 9, 15)}
ok(vals == {0: 0, 3: 36, 9: 0, 15: 180}, 'L5 P6 F at 0, 3, 9, 15')
Fgrid = max(float(Fx.subs(X, i / 1000)) for i in range(0, 15001, 5))
num(5, I, 3, max(vals.values()), Fgrid, {'critical': 36, 'no-third': max(xv ** 3 - 6 * xv ** 2 + 27 * xv for xv in (0, 3, 9, 15))}, rounded=180.0, agree=1e-9)
ok(15 ** 3 - 6 * 15 ** 2 + 27 * 15 == 2430 and sp.Rational(15 ** 3, 3) - 1350 + 405 == 180, 'L5 P6 F(15) arithmetic')
choice(5, I, 4, 'not-closed')
ok(round(float(Fx.subs(X, sp.Rational(29, 2))), 2) == 146.21, 'L5 P6 F(14.5) = 146.21')
ok(all(Fx.subs(X, sp.Rational(i, 100)) < 180 for i in range(0, 1500)), 'L5 P6 no point of [0, 15) reaches 180')
ok(max(abs(float(fF.subs(t, i / 1000))) for i in range(0, 15001)) == 72.0 and fF.subs(t, 0) == 27, 'L5 P6 |f| <= 72 on [0, 15], reached at 15; f(0) = 27')
n6 = first(lambda m: F(72, m) < F(7, 100))
num(5, I, 5, n6, ceil_above(72 / 0.07), {'round-down': n6 - 1, 'left-end': first(lambda m: F(27, m) < F(7, 100)), 'no-bound': first(lambda m: F(1, m) < F(7, 100))})
ok(n6 == 1029 and abs(72 / 1028 - 0.07004) < 5e-6 and abs(72 / 0.07 - 1028.6) < 0.05, 'L5 P6 72/1028 ~ 0.07004 and 72/0.07 ~ 1028.6')
ok(180 - Fx.subs(X, 15 - sp.Rational(1, n6)) < sp.Rational(7, 100), 'L5 P6 the true gap at n = 1029 is below 0.07')
shape45(5, {'p-root-sums': {'l20-riemann-integral', 'l21-fundamental-theorem-proved'},
            'p-diamond-ball': {'l22-metric-spaces', 'l23-open-and-closed'},
            'p-accumulated-cubic': {'l21-fundamental-theorem-proved', 'l23-open-and-closed', 'l24-compactness'}})

# ---------------------------------------------------------------- second check of the bands
for lv in (1, 2, 3, 4, 5):
    Lv = Level('analysis', lv)
    Lv.check_wrongs(f'problems-{lv}')
    bad = [r for r in Lv.results if not r[0]]
    ok(not bad, f'numbers_lib check_wrongs level {lv}: {len(bad)} bad')

print(f'{checks - len(fails)} of {checks} checks passed')
sys.exit(1 if fails else 0)
