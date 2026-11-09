"""random-vars level 1 performance task h-build-pmf: every number recomputed.

Run from the repository root: python3 -I docs/reports/random-vars-1-perf-numbers.py
Exits 0 when every check passes.

1. The item's shape: homework size, tests against examples, the code fields.
2. A harness that mirrors code.js __zq_cmp (isclose on dicts: same keys, values within
   rel 1e-9 / abs 1e-12; raises by exception name) runs the shipped solution, an
   independent solution by another route, the starter and ten planted wrong solutions.
3. Every expected pmf in the tests, two ways by exact enumeration with Fractions
   (route A: the space read exactly and added per value; route B: a closed form or a
   hand count), and once by a seeded simulation of 200,000 draws.
4. The float totals quoted in the feedback, recomputed as the engine's Python would
   (a running total, built-in sum, and the exact Fraction sum).
"""
import json
import math
import os
import random
import sys
from fractions import Fraction
from itertools import product

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'random-vars', 'homework-1.json')
ITEM_ID = 'h-build-pmf'

FAILS = []
CHECKS = 0


def check(cond, msg):
    global CHECKS
    CHECKS += 1
    if not cond:
        FAILS.append(msg)
        print('FAIL', msg)


hw = json.load(open(HW, encoding='utf-8'))
items = hw['items']
item = next(it for it in items if it['id'] == ITEM_ID)
w = item['widget']

# 1. Shape ------------------------------------------------------------------------
check(6 <= len(items) <= 12, f'homework holds {len(items)} items')
check(sum(1 for it in items if it.get('performance')) == 1, 'one performance item in the homework')
check(item['performance'] == 'code' and w['kind'] == 'code' and w['language'] == 'python', 'kind code, Python')
check(len(w['tests']) >= 3 and len(w['tests']) > len(w['examples']) and len(w['tests']) <= 15,
      f"{len(w['tests'])} tests against {len(w['examples'])} examples")
check(f"{len(w['tests'])} hidden tests" in w['how'], 'how states the test count')
check(all(ex in w['tests'] for ex in w['examples']), 'each example repeats a test')
check(3 <= item['difficulty'] <= 5 and any(it['difficulty'] == 5 for it in items), 'homework difficulty rule')
check('parts' not in item and 'hints' not in item, 'no parts, no hints')
check(not any(k.startswith('test-') and int(k[5:]) > len(w['tests']) for k in item['feedback']['byKey']),
      'every byKey test exists')


# 2. Harness ------------------------------------------------------------------------
def close(a, e):
    if isinstance(a, dict) or isinstance(e, dict):
        return isinstance(a, dict) and isinstance(e, dict) and set(a) == set(e) and all(close(a[k], e[k]) for k in a)
    if isinstance(a, str) and not isinstance(e, str):
        return False
    try:
        return math.isclose(float(a), float(e), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return a == e


def run_case(src, case):
    ns = {}
    try:
        exec(src, ns)
    except Exception:
        return False
    try:
        if case.get('setup'):
            exec(case['setup'], ns)
        if case['compare'] == 'raises':
            try:
                eval(case['call'], ns)
            except Exception as x:
                return case['expect'] in [k.__name__ for k in type(x).__mro__]
            return False
        a = eval(case['call'], ns)
        e = eval(case['expect'], ns)
        return close(a, e)
    except Exception:
        return False


def results(src):
    return [run_case(src, c) for c in w['tests']]


sol = results(w['solution'])
check(all(sol), f'shipped solution passes every test: {sol}')
check(all(run_case(w['solution'], c) for c in w['examples']), 'shipped solution passes the example')
start = results(w['starter'])
check(not any(start), f'starter fails every test: {start}')

ALT = '''
from fractions import Fraction
from itertools import groupby
def pmf_of(space, X):
    items = list(space.items())
    for _, p in items:
        if p < 0:
            raise ValueError
    total = Fraction(0)
    for _, p in items:
        total += Fraction(p)
    if not math.isclose(total, 1, rel_tol=0, abs_tol=1e-9):
        raise ValueError
    pairs = sorted(((X(o), p) for o, p in items if p != 0), key=lambda t: t[0])
    return {x: sum(p for _, p in g) for x, g in groupby(pairs, key=lambda t: t[0])}
import math
'''
alt = results(ALT)
check(all(alt), f'independent solution (sort and group, exact total) passes every test: {alt}')

BODY = '''
def pmf_of(space, X):
{checks}
    pmf = {{}}
    for o, p in space.items():
{loop}
    return pmf
'''
GOOD_CHECKS = ('    if any(p < 0 for p in space.values()):\n        raise ValueError\n'
               '    if abs(sum(space.values()) - 1) > 1e-9:\n        raise ValueError')
GOOD_LOOP = '        if p > 0:\n            pmf[X(o)] = pmf.get(X(o), 0) + p'


def bug(checks=GOOD_CHECKS, loop=GOOD_LOOP):
    return BODY.format(checks=checks, loop=loop)


BUGS = {
    'equally likely: 1/len(space) per outcome': bug(
        loop='        if p > 0:\n            pmf[X(o)] = pmf.get(X(o), 0) + 1 / len(space)'),
    'exact running total != 1': bug(checks=(
        '    t = 0\n    for p in space.values():\n        if p < 0:\n            raise ValueError\n        t += p\n'
        '    if t != 1:\n        raise ValueError')),
    'exact sum(...) != 1': bug(checks=(
        '    if any(p < 0 for p in space.values()):\n        raise ValueError\n'
        '    if sum(space.values()) != 1:\n        raise ValueError')),
    'keeps values of chance 0': bug(loop='        pmf[X(o)] = pmf.get(X(o), 0) + p'),
    'drops the value 0 instead of chance 0': bug(
        loop='        if X(o) != 0:\n            pmf[X(o)] = pmf.get(X(o), 0) + p'),
    'no negative check': bug(checks='    if abs(sum(space.values()) - 1) > 1e-9:\n        raise ValueError'),
    'no checks at all': bug(checks='    pass'),
    'total rounded to 3 places': bug(checks=(
        '    if any(p < 0 for p in space.values()):\n        raise ValueError\n'
        '    if round(sum(space.values()), 3) != 1:\n        raise ValueError')),
    'only a total over 1 raises': bug(checks=(
        '    if any(p < 0 for p in space.values()):\n        raise ValueError\n'
        '    if sum(space.values()) > 1 + 1e-9:\n        raise ValueError')),
    'overwrites instead of adding': bug(loop='        if p > 0:\n            pmf[X(o)] = p'),
    'keyed by outcome, not value': bug(loop='        if p > 0:\n            pmf[o] = p'),
}
for name, src in BUGS.items():
    r = results(src)
    failed = [i + 1 for i, ok in enumerate(r) if not ok]
    print(f'planted: {name}: fails tests {failed}')
    check(failed, f'planted bug "{name}" fails a test')

# which byKey line a planted bug sees (the first failing test)
first = {name: next((i + 1 for i, ok in enumerate(results(src)) if not ok), None) for name, src in BUGS.items()}
check(first['equally likely: 1/len(space) per outcome'] == 3, 'equal-chance slip meets the test-3 line')
check(first['exact running total != 1'] == 4, 'running-total slip meets the test-4 line')
check(first['exact sum(...) != 1'] == 7, 'built-in sum slip meets the test-7 line')
check(first['keeps values of chance 0'] == 5, 'chance-0 slip meets the test-5 line')
check(first['total rounded to 3 places'] == 9, 'rounded-total slip meets the test-9 line')
check(first['no negative check'] == 10, 'negative slip meets the test-10 line')


# 3. Every expected pmf, two exact routes and a simulation ---------------------------
def exact(v):
    return v if isinstance(v, Fraction) else Fraction(str(v)) if isinstance(v, float) else Fraction(v)


def route_a(space, X):
    """Each chance read exactly (a float as its decimal literal), added per value."""
    out = {}
    for o, p in space.items():
        p = exact(p)
        if p:
            out[X(o)] = out.get(X(o), Fraction(0)) + p
    return out


def simulate(space, X, n=200_000, seed=11):
    rng = random.Random(seed)
    outs = list(space)
    wts = [float(space[o]) for o in outs]
    draws = rng.choices(outs, wts, k=n)
    freq = {}
    for o in draws:
        freq[X(o)] = freq.get(X(o), 0) + 1
    return {x: c / n for x, c in freq.items()}, n


die = {k: Fraction(1, 6) for k in range(1, 7)}
dice = {(a, b): Fraction(1, 36) for a in range(1, 7) for b in range(1, 7)}
cards = {(a, b): Fraction(1, 12) for a in range(1, 5) for b in range(1, 5) if a != b}
tosses = {s: 0.7 ** s.count('H') * 0.3 ** s.count('T') for s in map(''.join, product('HT', repeat=3))}
longest = lambda s: max(len(run) for run in s.split('T'))
# the toss chances exactly, from the stated 0.7 and 0.3 (the float products are rounded)
tosses_exact = {s: Fraction(7, 10) ** s.count('H') * Fraction(3, 10) ** s.count('T') for s in tosses}
EXACT_SPACE = {7: tosses_exact}

p, q = Fraction(7, 10), Fraction(3, 10)
prod_b = {n: Fraction(sum(1 for a in range(1, 7) if n % a == 0 and 1 <= n // a <= 6), 36)
          for n in range(1, 37)}
prod_b = {k: v for k, v in prod_b.items() if v}
CASES = {
    1: (die, lambda k: 3 if k == 6 else -1, {3: Fraction(1, 6), -1: Fraction(5, 6)}),
    2: (dice, lambda w_: w_[0] * w_[1], prod_b),
    3: ({'red': 0.5, 'blue': 0.3, 'green': 0.2}, lambda c: 2 if c == 'blue' else -1,
        {2: Fraction(3, 10), -1: Fraction(5, 10) + Fraction(2, 10)}),
    4: ({k: 0.1 for k in range(10)}, lambda k: k // 4,
        {0: Fraction(len(range(0, 4)), 10), 1: Fraction(len(range(4, 8)), 10), 2: Fraction(len(range(8, 10)), 10)}),
    5: ({'H': 0.5, 'T': 0.5, 'edge': 0}, lambda s: {'H': 1, 'T': 0, 'edge': 5}[s],
        {1: Fraction(1, 2), 0: Fraction(1, 2)}),
    6: (cards, sum, {s: Fraction(sum(1 for a in range(1, 5) for b in range(1, 5) if a != b and a + b == s), 12)
                     for s in range(3, 8)}),
    7: (tosses, longest, {3: p ** 3, 2: 2 * p ** 2 * q, 0: q ** 3, 1: 1 - p ** 3 - 2 * p ** 2 * q - q ** 3}),
}
check(sum(prod_b.values()) == 1 and len(prod_b) == 18, 'product of two dice: 18 values, chances add to 1')
check(CASES[7][2][1] == p * q * p + 3 * p * q * q, 'longest run 1: HTH plus HTT, THT, TTH')
for k, (space, X, b) in CASES.items():
    t = w['tests'][k - 1]
    ns = {'Fraction': Fraction}
    e = eval(t['expect'], ns)
    a = route_a(EXACT_SPACE.get(k, space), X)
    check(a == b, f'test {k}: route A equals route B exactly: {a} vs {b}')
    check(sum(b.values()) == 1, f'test {k}: the pmf adds to 1 exactly')
    check(set(e) == set(b) and all(abs(Fraction(e[x]) - b[x]) < Fraction(1, 10 ** 12) for x in b),
          f'test {k}: the shipped expect matches the exact pmf')
    sim, n = simulate(space, X)
    check(set(sim) == set(b), f'test {k}: simulation sees exactly the values of the pmf')
    for x, px in b.items():
        se = math.sqrt(float(px) * (1 - float(px)) / n)
        check(abs(sim.get(x, 0) - float(px)) <= 5 * se + 1e-12,
              f'test {k}: simulated P(X = {x}) {sim.get(x, 0):.4f} within 5 se of {float(px):.4f}')
    print(f'test {k}: exact {dict(sorted((x, str(v)) for x, v in b.items()))}')
# the example in prose form
check(w['examples'][0]['expect'] == '{3: 1/6, -1: 5/6}', 'example expect as stated')
check(CASES[7][2] == {0: Fraction(27, 1000), 1: Fraction(336, 1000), 2: Fraction(294, 1000), 3: Fraction(343, 1000)},
      'longest run pmf 0.027, 0.336, 0.294, 0.343')

# 4. Float totals quoted in the feedback and the raising tests ------------------------
fb = item['feedback']['byKey']


def running(vals):
    t = 0
    for v in vals:
        t += v
    return t


tenths = [0.1] * 10
check(repr(running(tenths)) == '0.9999999999999999' and '`0.9999999999999999`' in fb['test-4'],
      'ten 0.1s added one at a time give 0.9999999999999999')
check(sum(tenths) == 1.0 or sys.version_info < (3, 12), 'built-in sum of ten 0.1s is 1.0 (compensated, Python 3.12+)')
check(abs(sum(Fraction(v) for v in tenths) - 1) < Fraction(1, 10 ** 15), 'ten float 0.1s are within 1e-15 of 1 exactly')
tv = list(tosses.values())
check(repr(sum(tv)) == '0.9999999999999998' and '`0.9999999999999998`' in fb['test-7'],
      'built-in sum of the toss chances is 0.9999999999999998')
check(running(tv) != 1 and abs(sum(tv) - 1) <= 1e-9, 'toss chances: not exactly 1 by either total, within 1e-9')
check(sum(Fraction(v) for v in tv) != 1, 'toss chances as stored floats do not add to exactly 1')
check(abs((0.5 + 0.4) - 1) > 1e-9, 'test 8: 0.9 is outside 1e-9')
check(Fraction('0.5') + Fraction('0.4999') == Fraction('0.9999') and '0.9999' in fb['test-9'], 'test 9: total 0.9999')
check(abs(sum([0.6, 0.6, -0.2]) - 1) <= 1e-9 and Fraction('0.6') * 2 - Fraction('0.2') == 1,
      'test 10: the chances add to 1, one is negative')
check(abs(sum([0.5, 0.3, 0.2]) - 1) <= 1e-9 and abs(sum([0.5, 0.5, 0]) - 1) <= 1e-9, 'tests 3 and 5 pass the total check')
check('1e-9' in item['question'], 'question states the tolerance')

print(f'{CHECKS} checks, failures: {len(FAILS)}')
sys.exit(1 if FAILS else 0)
