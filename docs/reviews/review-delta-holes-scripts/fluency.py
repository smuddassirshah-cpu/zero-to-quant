"""Delta read of the two holes fix passes, Fluency families. Reads the engine's own draws (draw.sh, 200 a family).

two-by-two and poisson-ratio-test (2 places, band 0.05):
  - the reader's own value of each draw against the engine's answer (two routes)
  - whether the band takes the workings the prompt promises (expected counts to 2 places; logarithms to 4 places), the
    solution's own printed figures, and the final answer rounded to 2 places
  - whether the band still refuses a wrong method: the share of draws in which each wrong method's 2-place answer is accepted,
    now (0.05) and under tighter bands
  - poisson-ratio-test is also run over every parameter set the family can draw (3,120 before `where`)
The other changed families: the claims of the fix pass on each draw (percent-sign entries clear, whole entries, where clauses,
prompt wording).

<scratchpad>/venv/bin/python docs/reviews/review-delta-holes-scripts/fluency.py <draws dir>      (from the repo root)"""
import json
import math
import re
import sys
from fractions import Fraction as F
from itertools import product

D = sys.argv[1]
checks = fails = 0
notes = []


def ok(c, msg):
    global checks, fails
    checks += 1
    if not c:
        fails += 1
        print('FAIL   ', msg)


def note(s):
    notes.append(s)
    print('NOTE   ', s)


def draws(f):
    return json.load(open(f'{D}/{f}.json'))['items']


def r2(x):
    return float(f'{x:.2f}')


def share(n, tot):
    return f'{n} of {tot}'


# ------------------------------------------------------------------ two-by-two
def x2_parts(a, b, c, d, dp=None, rnd=None):
    n = a + b + c + d
    O = [a, b, c, d]
    E = [(a + b) * (a + c) / n, (a + b) * (b + d) / n, (c + d) * (a + c) / n, (c + d) * (b + d) / n]
    if dp is not None:
        E = [round(e, dp) for e in E]
    return O, E


def x2(a, b, c, d, dp=None):
    O, E = x2_parts(a, b, c, d, dp)
    return sum((o - e) ** 2 / e for o, e in zip(O, E))


def two_methods(a, b, c, d):
    n = a + b + c + d
    O, E = x2_parts(a, b, c, d)
    m = {}
    m['G statistic 2 sum O ln(O/E)'] = 2 * sum(o * math.log(o / e) for o, e in zip(O, E))
    m['Yates correction'] = sum((abs(o - e) - 0.5) ** 2 / e for o, e in zip(O, E))
    m['divided by the observed counts'] = sum((o - e) ** 2 / o for o, e in zip(O, E))
    m['first row only (two cells)'] = sum((o - e) ** 2 / e for o, e in list(zip(O, E))[:2])
    m['first column only (two cells)'] = sum((o - e) ** 2 / e for o, e in [(O[0], E[0]), (O[2], E[2])])
    m['three cells'] = sum((o - e) ** 2 / e for o, e in list(zip(O, E))[:3])
    m['unsquared gaps over E'] = sum(abs(o - e) / e for o, e in zip(O, E))
    m['shortcut without the leading n'] = (a * d - b * c) ** 2 / ((a + b) * (c + d) * (a + c) * (b + d))
    m['expected counts as n/4'] = sum((o - n / 4) ** 2 / (n / 4) for o in O)
    m['one-cell (wrong entry)'] = (O[0] - E[0]) ** 2 / E[0]
    m['no-divide (wrong entry)'] = sum((o - e) ** 2 for o, e in zip(O, E))
    return m


def two_workings(a, b, c, d, key):
    n = a + b + c + d
    w = {}
    for dp in (3, 2, 1, 0):
        w[f'expected counts to {dp} places'] = x2(a, b, c, d, dp)
    O, E = x2_parts(a, b, c, d)
    gap3, E2 = round(abs(O[0] - E[0]), 3), [round(e, 2) for e in E]
    w['the solution\'s printed figures (gap to 3 places, counts to 2)'] = gap3 ** 2 * sum(1 / e for e in E2)
    # each cell's term rounded to 2 places before adding, counts to 2 places
    w['counts to 2 places and each term to 2 places'] = sum(round((o - e) ** 2 / e, 2) for o, e in zip(O, E2))
    w['counts to 2 places and each term to 3 places'] = sum(round((o - e) ** 2 / e, 3) for o, e in zip(O, E2))
    return w


def two_by_two():
    its = draws('two-by-two')
    N = len(its)
    band = its[0]['tol']['abs']
    ok(band == 0.05, 'two-by-two band 0.05')
    work_ref, meth_acc, meth_acc_t = {}, {}, {0.02: {}, 0.01: {}, 0.005: {}}
    small = 0
    worst = {}
    for it in its:
        v = it['vars']
        a, b, c, d = v['a'], v['b'], v['c'], v['d']
        key = x2(a, b, c, d)
        n = a + b + c + d
        short = n * (a * d - b * c) ** 2 / ((a + b) * (c + d) * (a + c) * (b + d))
        ok(abs(key - short) < 1e-9 and abs(key - it['answer']) < 1e-9, f'two-by-two {a},{b},{c},{d}: my X2 two routes equal the answer')
        ok(0.5 <= key <= 20, 'two-by-two key within the where range')
        ok(abs(r2(key) - key) <= band, 'two-by-two: the 2-place answer is in the band')
        ok('Keep at least 2 decimal places in each expected count' in it['prompt'] and 'Give 2 decimal places' in it['prompt'], 'two-by-two prompt wording')
        sol = ' '.join(it['solution'])
        mm = re.search(r'X\^2 \\approx ([0-9.]+)', sol)
        ok(mm and abs(float(mm.group(1)) - key) <= band and f'{key:.2f}' == mm.group(1), 'two-by-two: the solution prints the 2-place answer')
        for name, val in two_workings(a, b, c, d, key).items():
            typed = r2(val)
            e = abs(typed - key)
            worst[name] = max(worst.get(name, 0), e)
            if e > band:
                work_ref[name] = work_ref.get(name, 0) + 1
        for name, val in two_methods(a, b, c, d).items():
            typed = r2(val)
            if abs(typed - key) <= band:
                meth_acc[name] = meth_acc.get(name, 0) + 1
            for t in meth_acc_t:
                if abs(typed - key) <= t:
                    meth_acc_t[t][name] = meth_acc_t[t].get(name, 0) + 1
        for x in it['wrong']:
            ok(abs(x['value'] - key) > 2 * band, f'two-by-two: wrong {x["id"]} is more than twice the band from the answer')
        small += key < 2
    print(f'two-by-two, {N} draws, band {band}:')
    for name in two_workings(20, 30, 40, 25, 0):
        print(f'   working "{name}": refused in {share(work_ref.get(name, 0), N)}, worst error {worst[name]:.4f}')
    for name in two_methods(20, 30, 40, 25):
        print(f'   wrong method "{name}": accepted in {share(meth_acc.get(name, 0), N)} at 0.05; ' + ', '.join(f'{meth_acc_t[t].get(name, 0)} at {t}' for t in meth_acc_t))
    ok(work_ref.get('expected counts to 2 places', 0) == 0 and work_ref.get('expected counts to 3 places', 0) == 0, 'two-by-two: counts kept to 2 or 3 places are never refused')
    ok(work_ref.get('the solution\'s printed figures (gap to 3 places, counts to 2)', 0) == 0, 'two-by-two: the solution\'s own printed figures are never refused')
    return meth_acc, N


def two_by_two_wide(K=30000, seed=20261111):
    """the reader's own tables, drawn as the family draws them (15 to 70 a cell, a*d != b*c, 0.5 <= X2 <= 20)"""
    import random
    rnd = random.Random(seed)
    tabs = []
    while len(tabs) < K:
        a, b, c, d = (rnd.randint(15, 70) for _ in range(4))
        if a * d != b * c and 0.5 <= x2(a, b, c, d) <= 20:
            tabs.append((a, b, c, d))
    worst2 = worst_terms = 0
    acc = {t: {'G': 0, 'obs': 0} for t in (0.05, 0.03, 0.02, 0.005, 0.0005)}
    keep = keepg = 0
    for a, b, c, d in tabs:
        key = x2(a, b, c, d)
        w = two_workings(a, b, c, d, key)
        worst2 = max(worst2, abs(r2(w['expected counts to 2 places']) - key))
        worst_terms = max(worst_terms, abs(r2(w['counts to 2 places and each term to 2 places']) - key))
        m = two_methods(a, b, c, d)
        gv, ov = m['G statistic 2 sum O ln(O/E)'], m['divided by the observed counts']
        for t in acc:
            dp = 2 if t >= 0.005 else 3
            acc[t]['G'] += abs(round(gv, dp) - key) <= t
            acc[t]['obs'] += abs(round(ov, dp) - key) <= t
        keep += abs(key - ov) > 0.11
        keepg += abs(key - ov) > 0.11 and abs(key - gv) > 0.11
    print(f'two-by-two, {K} tables of the reader\'s own:')
    print(f'   counts to 2 places: worst error {worst2:.4f}; counts and every term to 2 places: worst error {worst_terms:.4f} (band 0.05)')
    for t in acc:
        print(f'   band {t}: the G statistic is accepted in {100 * acc[t]["G"] / K:.1f}% of tables, the sum divided by observed counts in {100 * acc[t]["obs"] / K:.1f}%')
    print(f'   a where clause abs(key - obs) > 0.11 keeps {100 * keep / K:.1f}% of tables; with abs(key - G) > 0.11 as well, {100 * keepg / K:.1f}%')
    ok(worst2 <= 0.05 and worst_terms <= 0.05, 'two-by-two, wide: the promised working is inside the band in every table')


# ------------------------------------------------------------------ poisson-ratio-test
def lr(n, lam0, dv, lndp=None, ratdp=None):
    s = n * lam0 + dv
    ratio = s / (n * lam0)
    if ratdp is not None:
        ratio = round(ratio, ratdp)
    ln = math.log(ratio)
    if lndp is not None:
        ln = round(ln, lndp)
    return 2 * (s * ln - dv)


def lr_methods(n, lam0, dv):
    s = n * lam0 + dv
    lam = s / n
    m = {}
    m['score statistic (s - n lam0)^2 / (n lam0)'] = dv ** 2 / (n * lam0)
    m['Wald statistic (s - n lam0)^2 / s'] = dv ** 2 / s
    m['ratio upside down, ln(lam0/lam hat)'] = 2 * (s * math.log(n * lam0 / s) - dv)
    m['n in place of the total in front of the log'] = 2 * (n * math.log(lam / lam0) - dv)
    m['mean term as lam hat - lam0 (no n)'] = 2 * (s * math.log(lam / lam0) - (lam - lam0))
    m['log to base 10'] = 2 * (s * math.log10(lam / lam0) - dv)
    m['not-doubled (wrong entry)'] = s * math.log(lam / lam0) - dv
    m['no-mean-term (wrong entry)'] = 2 * s * math.log(lam / lam0)
    return m


def lr_workings(n, lam0, dv):
    s = n * lam0 + dv
    w = {}
    for dp in (5, 4, 3):
        w[f'logarithm to {dp} places'] = lr(n, lam0, dv, lndp=dp)
    w['ratio to 4 places, then its logarithm to 4 places'] = lr(n, lam0, dv, lndp=4, ratdp=4)
    w['ratio to 3 places, then its logarithm to 4 places'] = lr(n, lam0, dv, lndp=4, ratdp=3)
    lam2 = round(s / n, 2)
    w['lam hat to 2 places, logarithm to 4 places, mean term from the rounded lam hat'] = 2 * (s * round(math.log(lam2 / lam0), 4) - n * (lam2 - lam0))
    w['logarithm to 4 places, truncated not rounded'] = 2 * (s * (math.trunc(math.log(s / (n * lam0)) * 1e4) / 1e4) - dv)
    return w


def tally(sets, band, label):
    N = len(sets)
    ref, acc, worst = {}, {}, {}
    accT = {0.02: {}, 0.01: {}, 0.005: {}}
    for n, lam0, dv in sets:
        key = lr(n, lam0, dv)
        for name, val in lr_workings(n, lam0, dv).items():
            e = abs(r2(val) - key)
            worst[name] = max(worst.get(name, 0), e)
            ref[name] = ref.get(name, 0) + (e > band)
        for name, val in lr_methods(n, lam0, dv).items():
            acc[name] = acc.get(name, 0) + (abs(r2(val) - key) <= band)
            for t in accT:
                accT[t][name] = accT[t].get(name, 0) + (abs(r2(val) - key) <= t)
    print(f'poisson-ratio-test, {label}, {N} sets, band {band}:')
    for name in ref:
        print(f'   working "{name}": refused in {share(ref[name], N)}, worst error {worst[name]:.4f}')
    for name in acc:
        print(f'   wrong method "{name}": accepted in {share(acc[name], N)} at 0.05; ' + ', '.join(f'{accT[t][name]} at {t}' for t in accT))
    return ref, acc, worst


def poisson():
    its = draws('poisson-ratio-test')
    band = its[0]['tol']['abs']
    ok(band == 0.05, 'poisson band 0.05')
    sets = []
    for it in its:
        v = it['vars']
        n, lam0, dv = v['n'], v['lam0'], v['dv']
        key = lr(n, lam0, dv)
        s = n * lam0 + dv
        ll = lambda lam: s * math.log(lam) - n * lam
        ok(abs(key - 2 * (ll(s / n) - ll(lam0))) < 1e-9 and abs(key - it['answer']) < 1e-8, f'poisson {n},{lam0},{dv}: my value two routes equals the answer')
        ok(0.2 <= key <= 15 and s >= 5, 'poisson within where')
        ok('Keep at least 4 decimal places in any logarithm' in it['prompt'], 'poisson prompt wording')
        sol = ' '.join(it['solution'])
        mm = re.search(r'\\approx ([0-9.]+)\$', sol)
        ok(mm and mm.group(1) == f'{key:.2f}', 'poisson: the solution prints the 2-place answer')
        for x in it['wrong']:
            ok(abs(x['value'] - key) > 2 * band, f'poisson: wrong {x["id"]} more than twice the band away')
        sets.append((n, lam0, dv))
    ref, acc, worst = tally(sets, band, 'engine draws')
    ok(ref['logarithm to 4 places'] == 0 and ref['logarithm to 5 places'] == 0, 'poisson draws: a logarithm kept to 4 or 5 places is never refused')
    allsets = [(n, l0, dv) for n in range(20, 81, 5) for l0 in (1, 2, 3, 4) for dv in range(-30, 31) if dv and n * l0 + dv >= 5 and 0.2 <= lr(n, l0, dv) <= 15]
    ref2, acc2, worst2 = tally(allsets, band, 'every parameter set the family can draw')
    ok(ref2['logarithm to 4 places'] == 0, 'poisson, every set: a logarithm kept to 4 places is never refused')
    ok(worst2['logarithm to 4 places'] <= 2 * 350 * 0.00005 + 0.005 + 1e-9, 'poisson: worst error within the bound 2 x 350 x 0.00005 + 0.005 = 0.04')
    return acc2, len(allsets)


# ------------------------------------------------------------------ the other changed families
def others():
    its = draws('volatility-se')
    for it in its:
        k = it['answer']
        v = it['vars']
        ok(abs(k - v['sig'] / math.sqrt(2 * v['n'])) < 1e-9, 'volatility-se key')
        w = {x['id']: x['value'] for x in it['wrong']}
        ok(abs(w['percent-sign'] - k / 100) < 1e-12, 'volatility-se percent-sign is key/100')
        vals = [k] + list(w.values())
        ok(all(abs(p - q) > 2 * 5e-05 for i, p in enumerate(vals) for q in vals[i + 1:]), f'volatility-se: answer and wrong bands all clear ({vals})')
    its = draws('assign-and-update')
    pct = 0
    for it in its:
        v = it['vars']
        pts = [v['v1']]
        for gname in ('g2', 'g3', 'g4', 'g5'):
            pts.append(pts[-1] + v[gname])
        c1, c2 = v['c1'], v['c1'] + v['gc']
        grp = [p for p in pts if abs(p - c2) < abs(p - c1)]
        k = sum(grp) / len(grp)
        ok(abs(k - it['answer']) < 1e-9, 'assign-and-update key by assignment')
        w = {x['id']: x['value'] for x in it['wrong']}
        ok(abs(w['percent-sign'] - k / 100) < 1e-12, 'assign-and-update percent-sign is key/100')
        vals = [k] + list(w.values())
        ok(all(abs(p - q) > 0.01 for i, p in enumerate(vals) for q in vals[i + 1:]), f'assign-and-update bands clear ({vals})')
        pct += v['unit'] == '%'
    print(f'assign-and-update: {pct} of {len(its)} draws state the values in %')
    its = draws('wilks-df')
    one = 0
    for it in its:
        v = it['vars']
        free = v['p'] - v['r']
        ok(it['answer'] == v['r'] and f'{free} of them stay free' in it['prompt'] and 'fixes' not in it['prompt'] and f' {v["r"]} ' not in it['prompt'].replace(f'has {v["p"]} parameters', '').replace(f'{free} of them', '') , f'wilks-df prompt prints the free count only: {it["prompt"][:90]}')
        one += free == 1
    if one:
        note(f'wilks-df: {one} of {len(its)} draws read "1 of them stay free" (number agreement)')
    for it in draws('slope-in-a-region'):
        ok('left of its first knot' in it['prompt'], 'slope-in-a-region wording')
    for it in draws('linkage-distance'):
        ok('Give the exact value.' in it['prompt'], 'linkage-distance wording')
        v = it['vars']
        a, b = it['prompt'], None
    for fam in ('add-tops', 'subtract-tops'):
        nb = 0
        for it in draws(fam):
            ok('with no brackets' in it['prompt'], f'{fam} wording')
            w = {x['id']: x['tex'] for x in it['wrong']}
            ok('whole' in w and w['whole'].startswith('\\frac{' + it['answer'] + '}'), f'{fam}: whole entry is the answer over the bottom')
            v = it['vars']
            sgn = 1 if fam == 'add-tops' else -1
            m, c0 = v['p'] + sgn * v['q'], v['p'] * v['b'] + sgn * v['q'] * v['a']
            g_ = math.gcd(m, abs(c0))
            nb += g_ > 1
        print(f'{fam}: in {nb} of 200 draws the top has a common factor, so a factorised top such as 2(4x - 13) is a form the prompt now rules out in words')
    for it in draws('quotient'):
        ok(it['prompt'].endswith('Give the quotient multiplied out.'), 'quotient wording')
    for it in draws('conjugate-bottom'):
        v = it['vars']
        ok(it['answer'] == v['p'] ** 2 - v['q'] >= 1, 'conjugate-bottom: new bottom is 1 or more')
    ok(sum(1 for p in range(2, 10) for q in (2, 3, 5, 6, 7, 10, 11, 13) if p * p > q) == 55, 'conjugate-bottom: 55 pairs')
    for it in draws('other-number'):
        mm = re.search(r'HCF of \$(\d+)\$ and another number is \$(\d+)\$, and their LCM is \$(\d+)\$', it['prompt'])
        m_, g_, l_ = map(int, mm.groups())
        ok(m_ != g_ and it['answer'] != l_ and it['answer'] == g_ * l_ // m_ and math.gcd(m_, it['answer']) == g_ and m_ * it['answer'] // g_ == l_,
           f'other-number: given {m_} is not the HCF {g_}, the answer {it["answer"]} is not the LCM {l_}, and the pair is consistent')
    for it in draws('count-factors'):
        v = it['vars']
        es = [v[k] for k in ('e2', 'e3', 'e5', 'e7', 'e11', 'e13')]
        nfac = sum(1 for d in range(1, v['nn'] + 1) if v['nn'] % d == 0)
        ok(it['answer'] == nfac, 'count-factors key by counting')
        ids = [x['id'] for x in it['wrong']]
        ok(('no-plus-one' in ids) == (max(es) > 1), 'count-factors: no-plus-one only when some index is above 1')
        ok(all(x['value'] != it['answer'] for x in it['wrong']), 'count-factors wrong values differ from the answer')
    for it in draws('table-mean'):
        v = it['vars']
        fs = [v[f'f{i}'] for i in range(5)]
        ok(re.search(r'counted over \$%d\$ \w+: \$%d\$ \w+ had 0, \$%d\$ had 1, \$%d\$ had 2, \$%d\$ had 3 and \$%d\$ had 4' % (sum(fs), *fs), it['prompt']) is not None, f'table-mean prompt: {it["prompt"][:80]}')
        ok(abs(it['answer'] - sum(i * f for i, f in enumerate(fs)) / sum(fs)) < 1e-9, 'table-mean key')


m2, N2 = two_by_two()
two_by_two_wide()
mp_, Np = poisson()
others()
print(f'fluency: {checks} checks, {fails} failures, {len(notes)} notes')
raise SystemExit(1 if fails else 0)
