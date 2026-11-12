#!/usr/bin/env python3
"""Delta read AC-2: every key, band, wrong[] value and printed number that the fix passes of review-delta-bank-2 and
review-delta-holes changed, recomputed from the item's own prose by two routes, and checked against the stored values and
the sentences that print them. (The two Fluency families are in fluency_all.py; typed strings are in grade.mjs.)
Usage (repo root, venv python): recompute.py      exit 1 on a FAIL row; FINDING rows are recorded in the review."""
import itertools, json, math, sys
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP, ROUND_DOWN, ROUND_FLOOR
from fractions import Fraction as F
from statistics import NormalDist

import numpy as np

fails = findings = checks = 0


def ok(cond, msg, finding=False):
    global fails, findings, checks
    checks += 1
    if cond:
        print('ok      ' + msg)
    elif finding:
        findings += 1
        print('FINDING ' + msg)
    else:
        fails += 1
        print('FAIL    ' + msg)


def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def item(path, iid, part=None):
    it = next(i for i in json.load(open('app/content/' + path))['items'] if i['id'] == iid)
    return it if part is None else it['parts'][part - 1]


def text(it):
    return json.dumps({k: it.get(k) for k in ('prose', 'question', 'feedback', 'explain')} | {'accept': it['widget'].get('accept')}, ensure_ascii=False)


def wrongs(it):
    return {w['id']: w for w in it['widget'].get('wrong', [])}


def band_checks(name, it, key, slips):
    """slips: {id: exact value}. The stored key band takes the exact key and its asked rounding; each stored wrong value is
    the slip to its own band; no slip (exact) is inside the key band; every wrong id has a line and the other way round."""
    w = it['widget']
    kt = w['tol']['abs']
    ok(abs(w['answer'] - float(key)) <= kt, f'{name}: stored answer {w["answer"]} within its band of the exact key {float(key):.6g}')
    ws = wrongs(it)
    ok(set(ws) == set(slips), f'{name}: wrong ids {sorted(ws)} are the slips recomputed')
    ok(set(it['feedback'].get('byKey', {})) == set(ws), f'{name}: every wrong id has a byKey line and every line an id')
    for k, v in slips.items():
        if k not in ws:
            continue
        ok(abs(ws[k]['value'] - float(v)) <= ws[k]['tol']['abs'] + 1e-12, f'{name}: wrong {k} stored {ws[k]["value"]}, slip recomputed {float(v):.6g}, inside its band')
        ok(abs(float(v) - float(key)) > kt + ws[k]['tol']['abs'], f'{name}: slip {k} is clear of the key band')
    for a, b in itertools.combinations(ws, 2):
        ok(abs(ws[a]['value'] - ws[b]['value']) > ws[a]['tol']['abs'] + ws[b]['tol']['abs'], f'{name}: bands of {a} and {b} do not meet')


# ------------------------------------------------------------------ bank: collinear-features-inflation-factor
it = item('bank/statistics-2.json', 'collinear-features-inflation-factor')
r = F(1, 2)
vif = 1 / (1 - r * r)                                         # route A: 1/(1 - r^2)
vif_b = np.linalg.inv(np.array([[1, 0.5], [0.5, 1]]))[0, 0]   # route B: diagonal of the inverse correlation matrix
rng = np.random.default_rng(7)
ok(vif == F(4, 3) and close(vif, vif_b), 'collinear: VIF 4/3 by 1/(1 - r^2) and by the inverse correlation matrix')
band_checks('collinear', it, vif, {'one-minus-r': 1 / (1 - r), 'standard-error-factor': math.sqrt(vif)})
t = text(it)
ok('0.5^2 = 0.25' in t and '1/0.75' in t and 'a third larger' in t and vif - 1 == F(1, 3), 'collinear: explain prints 0.25, 1/0.75 and "a third larger" (4/3 - 1 = 1/3)')
ok('1.5625' not in t and '0.6' not in t and '2.5' not in t, 'collinear: no number of the old version left')

# ------------------------------------------------------------------ bank: weak-signal-daily-edge
it = item('bank/statistics-3.json', 'weak-signal-daily-edge')
mean, sd, n = F(7, 100), F(14, 10), 1225
ok(math.isqrt(n) ** 2 == n and math.isqrt(n) == 35, 'weak-signal: 1,225 = 35 squared')
tstat = mean / (sd / 35)                                      # route A: exact
tstat_b = 0.07 * math.sqrt(1225) / 1.4                        # route B: floats, the other order
ok(tstat == F(7, 4) and close(tstat, tstat_b), 'weak-signal: t = 1.75 two ways')
band_checks('weak-signal', it, tstat, {'no-root': mean / sd, 'annual-sharpe': float(mean / sd) * math.sqrt(252)})
t = text(it)
ok(sd / 35 == F(4, 100) and '0.04%' in t and '0.07/0.04 = 1.75' in t, 'weak-signal: standard error 0.04% and 0.07/0.04 = 1.75 as printed')
n2 = next(k for k in range(1, 10**5) if mean / (sd / F(math.sqrt(k)).limit_denominator(10**6)) >= F(35, 10))
ok(n2 == 4900 and 4 * n == 4900 and '4,900 days' in t and 'To double it to 3.5' in t, f'weak-signal: t = 3.5 first reached at {n2} days = 4 x 1,225, as printed')

# ------------------------------------------------------------------ bank: ht-pvalue (choice)
it = item('bank/statistics-2.json', 'ht-pvalue-z-two-and-a-half')
tail = 1 - NormalDist().cdf(2.05)                             # route A
tail_b = 0.5 * math.erfc(2.05 / math.sqrt(2))                 # route B
xs = np.linspace(2.05, 12, 2_000_001)
tail_c = float(np.trapezoid(np.exp(-xs * xs / 2) / math.sqrt(2 * math.pi), xs))  # route C: the integral
ok(close(tail, tail_b, 1e-12) and close(tail, tail_c, 1e-8), f'ht-pvalue: one tail beyond 2.05 is {tail:.5f} three ways')
opts = {o['text']: o for o in it['widget']['options']}
key = [o for o in it['widget']['options'] if o.get('correct')]
ok(len(key) == 1 and key[0]['text'] == 'About 0.040' and round(2 * tail, 3) == 0.040, f'ht-pvalue: one key, "About 0.040"; two-sided p = {2 * tail:.4f}')
ok(round(tail, 3) == 0.020 and 'About 0.020' in opts and 'one tail' in opts['About 0.020']['why'], 'ht-pvalue: 0.020 is the one-tail slip')
ok(round(1 - NormalDist().cdf(1.96), 3) == 0.025 and 'About 0.025' in opts and '1.96' in opts['About 0.025']['why'], 'ht-pvalue: 0.025 is the tail beyond 1.96, as its line says')
ok('About 0.050' in opts and len(opts) == 4 and len({round(float(k.split()[-1]), 3) for k in opts}) == 4, 'ht-pvalue: four different options')
ok(0.01 < 2 * tail < 0.05 and 'significant at 5% but not at 1%' in text(it) and '0.0202' in text(it) and round(tail, 4) == 0.0202, 'ht-pvalue: explain: 0.0202, significant at 5% and not at 1%')
ok(not any(w in json.dumps(it) for w in ('2.2', '0.028', '0.014', '0.0139', '0.0278')), 'ht-pvalue: no number of the old version left')
ok(not any(p in json.dumps(it['widget']) + json.dumps(it['feedback']) + json.dumps(it['explain']) for p in ('first option', 'last option', 'option a', 'option b', 'above', 'below')), 'ht-pvalue: no option named by place (choices shuffle)')

# ------------------------------------------------------------------ bank: sample-size-for-signal-sharpe-years
it = item('bank/statistics-1.json', 'sample-size-for-signal-sharpe-years')
S = F(11, 10)
T = (3 / S) ** 2                                              # route A
lo, hi = 0.0, 100.0
for _ in range(200):                                          # route B: bisection on 1.1 sqrt(T) = 3
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if 1.1 * math.sqrt(mid) < 3 else (lo, mid)
ok(T == F(900, 121) and close(T, lo, 1e-9), f'sharpe-years: T = 900/121 = {float(T):.4f} two ways')
band_checks('sharpe-years', it, T, {'no-square': 3 / S, 'aimed-at-two': (2 / S) ** 2})
ok(round(float(T), 1) == 7.4 and round(float(T), 2) == 7.44 and '7.44' in text(it) and '7.4 years' in text(it), 'sharpe-years: 7.4 and 7.44 as printed')
# a third route for the claim itself: simulate daily returns with annual Sharpe 1.1 and look at the mean t statistic
sims = rng.normal(1.1 / math.sqrt(252), 1.0, size=(4000, int(round(float(T) * 252))))
tsim = sims.mean(axis=1) / (sims.std(axis=1, ddof=1) / math.sqrt(sims.shape[1]))
ok(abs(tsim.mean() - 3) < 0.06, f'sharpe-years: simulated mean t over {float(T):.2f} years of daily returns is {tsim.mean():.3f}')

# ------------------------------------------------------------------ bank: short strangle
it = item('bank/finance-3.json', 'op-payoff-short-strangle-loss')
prem = F(320, 100) + F(280, 100)
pnl = prem - max(90 - 81, 0) - max(81 - 110, 0)               # route A
pnl_b = (3.20 - max(90 - 81, 0)) + (2.80 - max(81 - 110, 0))  # route B: leg by leg
ok(pnl == -3 and close(pnl, pnl_b), 'strangle: profit -3 two ways')
band_checks('strangle', it, pnl, {'no-premium': -F(9), 'premium-only': prem, 'unsigned': -pnl})

# ------------------------------------------------------------------ bank: round-half-even (the new code line)
it = item('bank/coding-1.json', 'pf-types-round-half-even')
line = it['prose'].split('```python\n')[1].split('\n```')[0]
ok(line == 'int(-1.5) + round(-1.5) + round(-4.5) + (-9 // 2)', 'round: the code line is the one the fix pass lists')
val = eval(line)                                              # route A: run it
D = Decimal
q = lambda x, mode: int(D(x).quantize(D(1), rounding=mode))
terms = [q('-1.5', ROUND_DOWN), q('-1.5', ROUND_HALF_EVEN), q('-4.5', ROUND_HALF_EVEN), q('-4.5', ROUND_FLOOR)]  # route B
ok(val == -12 and terms == [-1, -2, -4, -5] and sum(terms) == -12, f'round: key -12, terms {terms}')
half_up = lambda x: math.floor(float(x) + 0.5)
half_away = lambda x: q(x, ROUND_HALF_UP)
slips = {
    'all-towards-zero': q('-1.5', ROUND_DOWN) + q('-1.5', ROUND_DOWN) + q('-4.5', ROUND_DOWN) + q('-4.5', ROUND_DOWN),
    'half-up': -1 + half_up('-1.5') + half_up('-4.5') + -5,
    'half-away': -1 + half_away('-1.5') + half_away('-4.5') + -5,
}
band_checks('round', it, val, slips)
ok(slips == {'all-towards-zero': -10, 'half-up': -11, 'half-away': -13}, f'round: slips {slips}')
# which single misreadings of one term reach each wrong value?
alts = [{'int cuts towards zero': -1, 'int rounds down': -2, 'int rounds to nearest': -2},
        {'half to even': -2, 'half up': -1, 'round cuts towards zero': -1},
        {'half to even': -4, 'half away from zero': -5},
        {'// rounds down': -5, '// cuts towards zero': -4}]
right = ['int cuts towards zero', 'half to even', 'half to even', '// rounds down']
single = {}
for i, a in enumerate(alts):
    for nm, v in a.items():
        if nm != right[i]:
            single.setdefault(-12 - terms[i] + v, []).append(nm)
print('        round: one term misread ->', single)
ok(set(single.get(-11, [])) <= {'half up'}, f'round: -11 gets the line "You rounded each half up", but one misread term reaches -11 by {single.get(-11)}', finding=True)
ok(set(single.get(-13, [])) <= {'half away from zero'}, f'round: -13 gets the line "You rounded each half away from zero", but one misread term reaches -13 by {single.get(-13)}', finding=True)

# ------------------------------------------------------------------ bank: es-mle (prose only)
it = item('bank/statistics-1.json', 'es-mle-waits-between-trades')
gaps = [4, 9, 2, 7, 5, 3]
lam = F(len(gaps), sum(gaps))                                 # route A
grid = np.linspace(0.01, 1, 9901)
lam_b = grid[np.argmax(len(gaps) * np.log(grid) - sum(gaps) * grid)]   # route B: the log-likelihood on a grid
ok(lam == F(1, 5) and close(lam, lam_b, 1e-4) and 'six gaps' in it['prose'] and all(str(x) in it['prose'] for x in gaps), 'es-mle: six gaps listed, total 30, estimate 0.2 two ways')
band_checks('es-mle', it, lam, {'mean-wait': 1 / lam, 'five-gaps': F(5, 30)})

# ------------------------------------------------------------------ holes: p-lawn-pond part 3
it = item('courses/number-sense/problems-4.json', 'p-lawn-pond', 3)
paving = F(13437, 100)
tins = math.ceil(paving / 12)                                 # route A
tins_b = next(k for k in range(1, 100) if 12 * k >= paving)   # route B: count up
ok(tins == tins_b == 12, 'lawn-pond 3: 12 tins two ways')
band_checks('lawn-pond 3', it, tins, {'rounded-down': math.floor(paving / 12), 'whole-courtyard': math.ceil(F(154) / 12)})
t = text(it)
ok(round(float(paving / 12), 2) == 11.20 and '11.20' in t and 11 * 12 == 132 and '132' in t and 12 * 12 == 144 and '144' in t, 'lawn-pond 3: 11.20, 132 and 144 as printed')
ok(round(paving / 12) == 11, 'lawn-pond 3: rounding to the nearest gives 11, so the part separates rounding up from rounding')
ok(math.ceil(F(13829, 100) / 12) == 12, 'lawn-pond 3: the carried slip of part 2 (138.29) also gives 12, so its entry was rightly removed')
whole = item('courses/number-sense/problems-4.json', 'p-lawn-pond')
ok('12 m²' in it['question'] and not any(s in json.dumps(it, ensure_ascii=False) for s in ('15 m²', '8.96', ' 9 tins')), 'lawn-pond 3: no figure of the old tin size left')

# ------------------------------------------------------------------ holes: p-windy-ride part 4, p-disk-failures part 5
it = item('courses/quadratics/problems-4.json', 'p-windy-ride', 4)
ws = wrongs(it)
import sympy as sp
v = sp.symbols('v')
ratio = sp.together((sp.Integer(9) / (v - 2)) / (sp.Integer(16) / v))
ok(sp.simplify(ratio - 9 * v / (16 * (v - 2))) == 0 and it['widget']['answer'] == '9v', 'windy-ride 4: time home over time out is 9v/(16(v - 2)), top 9v')
sol = sp.solve(sp.Eq(16 / v + 9 / (v - 2), 3.5), v) if False else None
ok(ws['number']['tex'] == '72' and 9 * 8 == 72 and 'v = 8' in it['feedback']['byKey']['number'], 'windy-ride 4: new wrong `number` is 72 = 9 x 8')
p3 = item('courses/quadratics/problems-4.json', 'p-windy-ride', 3)
p5 = item('courses/quadratics/problems-4.json', 'p-windy-ride', 5)
ok(float(p3['widget']['answer']) == 8 and close(float(p5['widget']['answer']), 72 / 96), 'windy-ride: part 3 gives v = 8 and part 5 puts it in (72/96 = 0.75), as the new line says')
it = item('courses/testing/problems-4.json', 'p-disk-failures', 5)
nmin = next(n for n in range(3, 10**4) if F(n - 2, n) >= F(99, 100))    # route A: search
ok(nmin == 200 == math.ceil(2 / 0.01) and it['widget']['answer'] == 200 and 'smallest number of gaps' in it['question'], 'disk-failures 5: 200 is the smallest n with (n - 2)/n >= 0.99, by search and by 2/0.01')
band_checks('disk-failures 5', it, 200, {'numerator': 198, 'efficiency-now': F(38, 40)})

# ------------------------------------------------------------------ holes: exams e-odds-update
it = item('exams/topic-2.1.json', 'e-odds-update')
p1, beta, d = 0.40, -0.6, 2
odds1 = p1 / (1 - p1)
odds3 = odds1 * math.exp(beta * d)
p3 = odds3 / (1 + odds3)                                      # route A: odds
p3_b = 1 / (1 + math.exp(-(math.log(p1 / (1 - p1)) + beta * d)))   # route B: logistic of the log-odds
ok(close(p3, p3_b, 1e-12) and round(p3, 5) == 0.16722, f'odds-update: fill probability {p3:.5f} two ways')
up = odds1 * math.exp(-beta * d)
band_checks('odds-update', it, p3, {'prob-times': p1 * math.exp(beta * d), 'odds-as-prob': odds3, 'sign': up / (1 + up), 'decimal': p3 / 100})
t = text(it)
ok(round(odds1, 3) == 0.667 and round(odds3, 3) == 0.201 and round(math.exp(-1.2), 3) == 0.301 and all(s in t for s in ('0.667', '0.201', '0.301', '16.7')), 'odds-update: 0.667, 0.301, 0.201 and 16.7 as printed')
ok(round(0.201 / 1.201, 3) == 0.167, 'odds-update: the printed last step 0.201/1.201 gives 16.7%')
w = wrongs(it)['decimal']
inside = {nm: x / 100 for nm, x in (('the odds 0.201 typed as a decimal', odds3), ('prob-times 0.12 typed as a decimal', p1 * math.exp(beta * d)))
          if abs(x / 100 - w['value']) <= w['tol']['abs']}
ok(not inside, f'odds-update: the `decimal` band {w["value"]} +- {w["tol"]["abs"]} also takes {list(inside)}; its line then says "That is the probability as a fraction of 1" and gives 16.7', finding=True)
for tol in (0.00006,):
    takes = [x for x in (0.166, 0.167, 0.1672, 0.168, 0.17) if abs(x / 100 - w['value']) <= tol]
    leaves = [x for x in (0.2, 0.201, 0.2008, 0.12, 0.1205, 0.15, 0.4, 0.689) if abs(x / 100 - w['value']) > tol]
    ok(len(takes) == 5 and len(leaves) == 8, f'odds-update, proposed `decimal` band {tol}: takes 0.166 to 0.17 typed, leaves 0.2, 0.201, 0.12, 0.15, 0.4, 0.689')
ok(not any(s in t for s in ('leverage', '0.215', '0.246', '0.273')), 'odds-update: no figure of the old version left')

# ------------------------------------------------------------------ holes: exams e-diameter-ends
it = item('exams/topic-0.2.json', 'e-diameter-ends')
A, B = (-7, -9), (9, 21)
C = (F(A[0] + B[0], 2), F(A[1] + B[1], 2))
r2 = (C[0] - A[0]) ** 2 + (C[1] - A[1]) ** 2                   # route A: centre to A
r2_b = F((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2, 4)           # route B: half of AB, squared
ok(C == (1, 6) and r2 == r2_b == 289 and math.isqrt(289) == 17, 'diameter-ends: centre (1, 6), r^2 = 289 two ways, r = 17')
x, y = sp.symbols('x y')
key = (x - 1) ** 2 + (y - 6) ** 2 - 289
ok(it['widget']['answer'] == '(x-1)^2+(y-6)^2=289', 'diameter-ends: stored key')
ok(sp.expand(key - (x ** 2 + y ** 2 - 2 * x - 12 * y - 252)) == 0 and it['widget']['accept'] == ['x^2+y^2-2x-12y-252=0'], 'diameter-ends: the accept form expands from the key')
ok(key.subs({x: A[0], y: A[1]}) == 0 and key.subs({x: B[0], y: B[1]}) == 0, 'diameter-ends: both ends lie on the circle')
ok((sp.Matrix([A[0] - 1, A[1] - 6]) + sp.Matrix([B[0] - 1, B[1] - 6])) == sp.zeros(2, 1), 'diameter-ends: A and B are opposite ends (third route: C is their midpoint as vectors)')
ws = wrongs(it)
ok(ws['signs']['tex'] == '(x+1)^2+(y+6)^2=289' and ws['radius-not-squared']['tex'].endswith('=17') and ws['full-diameter']['tex'].endswith('=1156') and 34 ** 2 == 1156, 'diameter-ends: three wrong forms (signs, 17, 34^2 = 1156)')
t = text(it)
ok(abs(C[0] - A[0]) == 8 and abs(C[1] - A[1]) == 15 and B[0] - A[0] == 16 and B[1] - A[1] == 30 and math.isqrt(16 ** 2 + 30 ** 2) == 34 and all(s in t for s in ('8^2 + 15^2', '16^2 + 30^2', '34', '8 across and 15 down')), 'diameter-ends: 8, 15, 17, 16, 30, 34 as printed; A is 8 across and 15 down from C')
ok(not any(s in t for s in ('169', '676', '13^2', '26', '132')), 'diameter-ends: no figure of the old version left')

# ------------------------------------------------------------------ holes: text-only edits
it = item('courses/number-sense/problems-4.json', 'p-hall-tiles', 2)
nf = sum(1 for k in range(1, 121) if 120 % k == 0)
ok(nf == 16 == (3 + 1) * (1 + 1) * (1 + 1) and it['widget']['answer'] == 16 and 'factors of 120' in it['feedback']['generic'] and '108' not in json.dumps(it), 'hall-tiles 2: 120 has 16 factors two ways; the generic line names 120')

print(f'recompute: {checks} checks, {fails} failures, {findings} FINDING rows')
sys.exit(1 if fails else 0)
