#!/usr/bin/env python3
"""Concept audit checks for number-sense level 4 (l15 to l19, review-4, homework-4, problems-4, fluency-l15 to l19).

Deterministic checks of the claims the audit ledger rests on (docs/reports/audit-number-sense-4-ledger.md). Nothing here is
Monte Carlo: level 4 makes no statistical claim, so every "always / never / every" claim is checked exhaustively over a range.
Exit 0 when the content is correct. INFO lines back the `imprecise` findings and do not fail the script.

Run from anywhere: python docs/reports/number-sense-L4-concepts.py   (the generated-family section needs `node` on PATH;
without it that section is skipped and says so).
"""
import json, math, os, re, shutil, subprocess, sys
from fractions import Fraction
from itertools import combinations, product

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CDIR = os.path.join(ROOT, 'app', 'content', 'courses', 'number-sense')
fails = []


def load(name):
    with open(os.path.join(CDIR, name + '.json'), encoding='utf-8') as f:
        return json.load(f)


def check(ok, label):
    if not ok:
        fails.append(label)
        print('FAIL', label)


def is_prime(n):
    return n > 1 and all(n % k for k in range(2, int(n ** 0.5) + 1))


def factors(n):
    return [k for k in range(1, n + 1) if n % k == 0]


def primes_of(n):
    out, p = {}, 2
    while n > 1:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    return out


def within(v, k, tol):
    return abs(v - k) <= tol + 1e-9   # app/js/engine/grade.js `within`


# ---------------------------------------------------------------- l15: factors, primes, the sieve, the square-root test
l15 = load('l15-building-blocks')
S = l15['screens']
check(len(factors(36)) == 9 and len(factors(37)) == 2 and len(factors(49)) == 3, 'l15 factor counts 36, 37, 49')
cell = lambda n: 'r%dc%d' % ((n - 1) // 10 + 1, (n - 1) % 10 + 1)
want = {cell(n) for n in range(1, 101) if (n % 2 == 0 or n % 3 == 0 or n % 5 == 0) and n not in (2, 3, 5)}
check(set(S[3]['canvas']['state']['shade']['crossed']) == want, 'l15 s3 sieve shading is the multiples of 2, 3, 5 apart from themselves')
check(set(S[3]['widget']['answer']) == {cell(49), cell(77), cell(91)}, 'l15 s3 unshaded multiples of 7')
check([sum(is_prime(n) for n in range(2, m)) for m in (100, 50, 30)] == [25, 15, 10], 'l15 s3 prime counts 25, 15, 10')
check(set(S[6]['widget']['answer']) == {cell(n) for n in (1, 2, 51, 53, 57, 59, 91) if is_prime(n)}, 'l15 s6 ringed primes')
# "A factor pair always has one member at most the square root": every composite n has a prime factor p with p*p <= n.
check(all(any(n % p == 0 for p in range(2, int(n ** 0.5) + 1) if is_prime(p)) for n in range(4, 20001) if not is_prime(n)),
      'l15 square-root test: every composite to 20,000 has a prime factor at most its root')
# Factor count rule (e1+1)(e2+1)... for every n to 3,000; and "squares are the numbers with an odd count of factors".
check(all(len(factors(n)) == math.prod(e + 1 for e in primes_of(n).values()) for n in range(2, 3001)), 'l15 factor-count rule to 3,000')
check(all((len(factors(n)) % 2 == 1) == (math.isqrt(n) ** 2 == n) for n in range(1, 3001)), 'l15 quiz: odd factor count iff square')
check(primes_of(360) == {2: 3, 3: 2, 5: 1} and primes_of(252) == {2: 2, 3: 2, 7: 1} and len(factors(252)) == 18, 'l15 360 and 252 in primes')
for o in S[9]['widget']['options']:
    d = int(re.match(r'(\d+)', o['text']).group(1))
    check((252 % d == 0) == bool(o.get('correct')), 'l15 s9 option %d days' % d)

# ---------------------------------------------------------------- l16: HCF, LCM, Euclid
check(all(math.gcd(a, b) * math.lcm(a, b) == a * b for a in range(1, 301) for b in range(1, 301)), 'l16 HCF x LCM = product, to 300')
check(all(math.gcd(a, b) <= min(a, b) and math.lcm(a, b) >= max(a, b) for a in range(1, 301) for b in range(1, 301)), 'l16 s8 bounds on HCF and LCM')


def euclid(a, b):
    rem = []
    while b:
        a, b = b, a % b
        rem.append(b)
    return a, rem


check(euclid(252, 198) == (18, [54, 36, 18, 0]) and math.lcm(252, 198) == 2772, 'l16 s7 Euclid on 252 and 198')
check(euclid(1071, 462) == (21, [147, 21, 0]) and math.lcm(1071, 462) == 23562, 'homework Euclid on 1,071 and 462')
check((math.gcd(84, 120), math.lcm(84, 120), math.gcd(150, 240), math.lcm(150, 240)) == (12, 840, 30, 1200), 'l16 84/120 and 150/240')
check(Fraction(5, 12) + Fraction(7, 18) == Fraction(29, 36), 'l16 s6 sum')
# INFO for finding 1: 36ths are the largest common piece, not the smallest (72nds also work and are smaller).
print('INFO l16 s6: 5/12 and 7/18 are both whole numbers of 72nds (%s, %s); 1/72 < 1/36, so 36ths are not "the smallest piece size"'
      % (Fraction(5, 12) / Fraction(1, 72), Fraction(7, 18) / Fraction(1, 72)))

# ---------------------------------------------------------------- l17 to l19, review, homework, problems: keyed values
check(max(range(1, 12), key=lambda x: x * (12 - x)) == 6, 'l17 s0 square encloses most')
check(10 + 3 + 4 + 3 + 6 + 6 == 2 * (10 + 6) == 32, 'l17 s6 L-shape perimeter equals the rectangle')
week = [120, -80, 40, 40, 300, -60, 60]
check(sum(week) == 420 and sorted(week)[3] == 40 and max(week) - min(week) == 380, 'l19 the seven days')
big = [3100 if v == 300 else v for v in week]
check(sum(big) == 3220 and sum(big) / 7 == 460 and sorted(big)[3] == 40, 'l19 s4 outlier')
check(sum(v - 60 for v in week if v > 60) == sum(60 - v for v in week if v < 60) == 300, 'l19 balance distances')
check((10 * 50000 + 30 * 70000) / 40 == 65000, 'l19 s8 weighted mean')
leaf = [18, 22, 20, 19, 21, 20, 23, 17, 20, 22, 18, 200]
check(sum(leaf) == 420 and sorted(leaf)[5] == sorted(leaf)[6] == 20, 'homework leaflet mean and median')
check(math.lcm(*range(1, 11)) == 2520 and len(factors(2520)) == 48, 'homework 2,520')
check(math.gcd(360, 600) == 120 and len(factors(120)) == 16 and len(factors(1800)) == 36, 'problems tiles')
check(math.lcm(48, 18) == 144, 'problems gears')

# INFO for finding 3: making an extreme value more extreme never moves the median, but adding one can.


def median(v):
    s = sorted(v)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


same = all(median(list(c[:-1]) + [c[-1] + 1000]) == median(c) for c in combinations(range(1, 12), 5))
moved = sum(median(list(c) + [1000]) != median(c) for c in combinations(range(1, 12), 5))
check(same, 'stretching the largest of five values leaves the median alone')
print('INFO outlier: stretching the largest value never moves the median; ADDING an outlier moved it in %d of %d five-value lists'
      % (moved, math.comb(11, 5)))

# pi items: an answer worked with pi = 3.14 or 22/7 and rounded as asked must be accepted and must not match a slip.


def pi_item(label, f, dp, key, tol, wrong=()):
    for name, p in (('pi', math.pi), ('3.14', 3.14), ('22/7', 22 / 7)):
        v = round(f(p), dp)
        check(within(v, key, tol), '%s: %s answer %s accepted against %s +/- %s' % (label, name, v, key, tol))
        check(not any(within(v, w, t) for w, t in wrong), '%s: %s answer matches a slip' % (label, name))


pi_item('l18 s1 wheel', lambda p: p * 50, 1, 157.1, 0.15)
pi_item('l18 s3 circumference', lambda p: 10 * p, 2, 31.42, 0.05)
pi_item('l18 s3 area', lambda p: 25 * p, 2, 78.54, 0.1, [(31.42, 0.05)])
pi_item('l18 s4 semicircle', lambda p: 4 * p + 8, 2, 20.57, 0.01)
pi_item('l18 s7 pond', lambda p: 25 * p, 2, 78.54, 0.05)
pi_item('l18 quiz 0', lambda p: 6 * p, 2, 18.85, 0.01)
pi_item('l18 quiz 1', lambda p: 9 * p, 2, 28.27, 0.02)
pi_item('review circle', lambda p: 49 * p, 2, 153.94, 0.1)
pi_item('homework lawn area', lambda p: 60 + 4.5 * p, 2, 74.14, 0.01)
pi_item('homework lawn perimeter', lambda p: 26 + 3 * p, 2, 35.42, 0.01)
pi_item('problems basin', lambda p: 6.25 * p, 2, 19.635, 0.02)
pi_item('problems gear', lambda p: 240 * 6 * p / 100, 0, 45, 0.5, [(90, 0.5)])

# ---------------------------------------------------------------- fluency tables read straight from the JSON (whole range)
PR = [2, 3, 5, 7, 11, 13]
f15 = load('fluency-l15-building-blocks')
for fam in f15['families']:
    for row in fam['vars']['t']['pick']:
        nn, ptex, ctex, es = row[0], row[1], row[2], row[3:9]
        check(math.prod(p ** e for p, e in zip(PR, es)) == nn, 'fluency-l15 %s row %d: exponents multiply to the number' % (fam['id'], nn))
        tex = ' \\times '.join((str(p) if e == 1 else '%d^%d' % (p, e)) for p, e in zip(PR, es) if e)
        check(tex == ptex, 'fluency-l15 %s row %d: prime product text' % (fam['id'], nn))
        check(' \\times '.join('(%d + 1)' % e for e in es if e) == ctex, 'fluency-l15 %s row %d: count text' % (fam['id'], nn))
        if fam['id'] == 'largest-prime':
            lp = max(primes_of(nn))
            check(lp >= 3, 'fluency-l15 largest-prime row %d is not a pure power of 2 (the let falls back to 3)' % nn)
            bigf = nn // min(primes_of(nn))
            # slip line says the largest proper factor "is not prime": must hold whenever it is not itself the answer
            check(bigf == lp or not is_prime(bigf), 'fluency-l15 largest-prime row %d: largest-factor slip line' % nn)
        else:
            key = math.prod(e + 1 for e in es)
            check(key == len(factors(nn)), 'fluency-l15 %s row %d: factor count' % (fam['id'], nn))

f16 = load('fluency-l16-shared-factors')
for fam in f16['families']:
    for g, p in fam['vars']['gp']['pick']:
        check(is_prime(p) and g % p == 0, 'fluency-l16 %s: %d is a prime factor of %d' % (fam['id'], p, g))
    for a, b in fam['vars']['ab']['pick']:
        check(a < b and math.gcd(a, b) == 1, 'fluency-l16 %s: (%d, %d) coprime and ordered' % (fam['id'], a, b))
    for (g, p), (a, b) in product(fam['vars']['gp']['pick'], fam['vars']['ab']['pick']):
        m, n = g * a, g * b
        check(math.gcd(m, n) == g and math.lcm(m, n) == g * a * b, 'fluency-l16 %s keys for %d, %d' % (fam['id'], m, n))

f19 = load('fluency-l19-one-number-for-many')
for fam in f19['families']:
    if 'oo' in fam['vars']:
        for perm in fam['vars']['oo']['pick']:
            check(sorted(perm) == [1, 2, 3, 4, 5], 'fluency-l19 %s order %s is a permutation' % (fam['id'], perm))
            check(perm != [1, 2, 3, 4, 5], 'fluency-l19 %s order is not already sorted' % fam['id'])

# ---------------------------------------------------------------- generated families: sample, recompute independently from the variables
NODE = shutil.which('node')
SAMPLER = os.path.join(ROOT, 'app', 'tools', 'fluency-sample.mjs')


def sample(setid, fam, n=300):
    out = subprocess.run([NODE, SAMPLER, '--set', 'number-sense/' + setid, '--family', fam, '--n', str(n), '--json'],
                         capture_output=True, text=True, cwd=os.path.join(ROOT, 'app'))
    if out.returncode:
        check(False, 'sampler failed for %s %s: %s' % (setid, fam, out.stderr[-200:]))
        return []
    return json.loads(out.stdout)['items']


def num(x):
    return float(Fraction(x)) if isinstance(x, str) else float(x)


def indep(setid, fam, v):
    """The answer, recomputed from the drawn variables alone. Slips: {id: value} where the audit checked the named mistake."""
    if fam == 'hcf':
        m, n = v['g'] * v['a'], v['g'] * v['b']
        return math.gcd(m, n), {'lcm': math.lcm(m, n), 'one-prime': v['p']}
    if fam == 'lcm':
        m, n = v['g'] * v['a'], v['g'] * v['b']
        return math.lcm(m, n), {'product': m * n, 'hcf': math.gcd(m, n)}
    if fam == 'other-number':
        m, n = v['g'] * v['a'], v['g'] * v['b']
        others = [x for x in range(1, 2001) if math.gcd(m, x) == v['g'] and math.lcm(m, x) == math.lcm(m, n)]
        check(others == [n], 'fluency-l16 other-number: the other number is unique for %d' % m)
        return n, {'lcm-over-hcf': math.lcm(m, n) / v['g'], 'product': m * n}
    if fam == 'triangle-area':
        return v['b'] * v['h'] / 2, {'no-half': v['b'] * v['h'], 'sloping-side': v['b'] * (v['h'] + v['k']) / 2}
    if fam == 'parallelogram-area':
        return v['b'] * v['h'], {'slant-side': v['b'] * (v['h'] + v['k']), 'halved': v['b'] * v['h'] / 2}
    if fam == 'trapezium-area':
        a, c, h = v['a'], v['a'] + v['d'], v['h']
        return (a + c) / 2 * h, {'no-half': (a + c) * h, 'longer-side': c * h}
    if fam == 'l-shape-area':
        return v['w'] * v['t'] - v['p'] * v['q'], {'corner-kept': v['w'] * v['t'], 'corner-added': v['w'] * v['t'] + v['p'] * v['q']}
    if fam in ('circumference', 'circle-area'):
        r = v['m'] if v['k'] == 1 else v['m'] / 2
        if fam == 'circumference':
            return 2 * math.pi * r, {'area-rule': math.pi * r * r, 'radius-diameter': math.pi * r if v['k'] == 1 else 4 * math.pi * r}
        return math.pi * r * r, {'diameter-squared': math.pi * 4 * r * r, 'circumference': 2 * math.pi * r}
    if fam == 'speed-units':
        x = v['x']
        if v['dir'] == 1:
            return x * 1000 / 3600, {'wrong-way': x * 3600 / 1000, 'minutes': x * 1000 / 60}
        return x * 3600 / 1000, {'wrong-way': x * 1000 / 3600, 'minutes': x * 60 / 1000}
    if fam == 'area-units':
        a = v['n'] / 10
        return a * 10000, {'length-only': a * 100, 'divided': a / 10000}
    if fam == 'table-mean':
        f = [v['f%d' % i] for i in range(5)]
        tot = sum(i * f[i] for i in range(5))
        return tot / sum(f), {'values-only': 2, 'rows': tot / 5}
    return None, {}


def from_prompt(prompt):
    return [int(x) for x in re.findall(r'\$(-?\d+)\$', prompt)]


if NODE and os.path.exists(SAMPLER):
    sets = {'fluency-l15-building-blocks': f15, 'fluency-l16-shared-factors': f16, 'fluency-l17-around-and-inside': load('fluency-l17-around-and-inside'),
            'fluency-l18-circles-and-units': load('fluency-l18-circles-and-units'), 'fluency-l19-one-number-for-many': f19}
    for setid, doc in sets.items():
        for fam in doc['families']:
            fid = fam['id']
            for it in sample(setid, fid):
                v, ans, tol = it['vars'], num(it['answer']), (it.get('tol') or {}).get('abs', 0)
                tag = '%s %s seed %s' % (setid, fid, it['seed'])
                slips = {}
                if fid == 'largest-prime':
                    pf = primes_of(v['nn'])
                    key = max(pf)
                    slips = {'largest-factor': v['nn'] // min(pf), 'prime-power': key ** pf[key]}
                    for w in it['wrong']:
                        check(not is_prime(int(num(w['value']))), tag + ': slip %s is a prime' % w['id'])
                elif fid in ('count-from-primes', 'count-factors'):
                    key = len(factors(v['nn']))
                    es = [e for e in primes_of(v['nn']).values()]
                    slips = {'indices-multiplied': math.prod(es), 'no-plus-one': math.prod(es), 'indices-added': sum(e + 1 for e in es),
                             'pairs': math.ceil(key / 2)}
                elif fid == 'mean':
                    vals = from_prompt(it['prompt'])
                    key = sum(vals) / 5
                    slips = {'divided-by-four': sum(vals) / 4, 'loss-added': (sum(vals) - 2 * v['a']) / 5}
                elif fid == 'median':
                    vals = from_prompt(it['prompt'])
                    check(len(set(vals)) == 5, tag + ': five distinct readings')
                    key = sorted(vals)[2]
                    slips = {'unsorted': vals[2], 'mean': sum(vals) / 5}
                elif fid == 'range':
                    vals = from_prompt(it['prompt'])
                    key = max(vals) - min(vals)
                    slips = {'first-last': abs(vals[-1] - vals[0]), 'sign-lost': max(vals) - abs(min(vals))}
                else:
                    key, slips = indep(setid, fid, v)
                check(key is not None and within(ans, key, 1e-6), tag + ': key %s, recomputed %s' % (ans, key))
                for w in it['wrong']:
                    wv, wt = num(w['value']), (w.get('tol') or {}).get('abs', tol) if isinstance(w.get('tol'), dict) else tol
                    check(not within(wv, ans, max(tol, wt)), tag + ': slip %s (%s) is within tolerance of the key %s' % (w['id'], wv, ans))
                    if w['id'] in slips:
                        check(within(wv, slips[w['id']], 1e-6), tag + ': slip %s value %s, the named mistake gives %s' % (w['id'], wv, slips[w['id']]))
                    else:
                        check(False, tag + ': slip %s has no independent recomputation' % w['id'])
                if fid in ('circumference', 'circle-area'):
                    r = v['m'] if v['k'] == 1 else v['m'] / 2
                    for p in (3.14, 22 / 7):
                        a = round(2 * p * r if fid == 'circumference' else p * r * r, 1)
                        check(within(a, ans, tol), tag + ': answer %s from pi = %.5f accepted' % (a, p))
                        check(not any(within(a, num(w['value']), (w.get('tol') or {}).get('abs', tol)) for w in it['wrong']), tag + ': rounded-pi answer hits a slip')
    spd = [it for it in sample('fluency-l18-circles-and-units', 'speed-units') if it['vars']['dir'] == 2]
    print('INFO fluency-l18 speed-units: %d of 300 draws go from metres a second to km an hour; their "minutes" slip is x * 60 / 1000 '
          '(seconds changed to minutes only), but the line says "You changed hours into minutes only"' % len(spd))
else:
    print('SKIP generated-family section: node or the sampler was not found')

print('number-sense L4 concepts: %d failure(s)' % len(fails))
sys.exit(1 if fails else 0)
