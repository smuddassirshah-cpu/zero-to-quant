"""Recompute every figure of options homework-2 item h-strategy-card (performance task, L2).

Route 1: the item's own solution run through every example and hidden test, as the code widget grades.
Route 2: an independent card in exact fractions. Profit is evaluated on a grid of eighths from 0 to 400
(every strike and break-even in the tests is on it or between two grid points); a zero is found by
solving the straight piece between neighbouring grid points exactly; the limits come from the profit at
10**6 and 2 * 10**6, not from a slope formula. Every expect must equal route 2.
Route 3: hand formulas for each test (spread K1 + D, straddle K -/+ premium, and so on), written below.
The starter fails every test; each planted wrong solution fails at least one test, first at the test
its byKey line names where it has one.
Run: python3 -I docs/reports/options-2-perf-numbers.py (standard library only).
"""
import json, math, os
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'options', 'homework-2.json')
doc = json.load(open(HW, encoding='utf-8'))
item = next(i for i in doc['items'] if i['id'] == 'h-strategy-card')
w = item['widget']
fails = 0


def check(ok, msg):
    global fails
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        fails += 1


# ---- a copy of the code widget's isclose compare (dicts by key set, lists by length, then math.isclose) ----
def close(a, b, rel, ab):
    if isinstance(a, dict) or isinstance(b, dict):
        return isinstance(a, dict) and isinstance(b, dict) and set(a) == set(b) and all(close(a[k], b[k], rel, ab) for k in a)
    if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
        return (isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)) and len(a) == len(b)
                and all(close(x, y, rel, ab) for x, y in zip(a, b)))
    if isinstance(a, str):
        return False
    try:
        return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=ab)
    except Exception:
        return False


def run_case(src, t):
    env = {}
    try:
        exec(src, env)
        act = eval(t['call'], env)
    except Exception as e:
        return False
    tol = t.get('tol', {})
    return close(act, eval(t['expect'], {}), tol.get('rel', 0.0), tol.get('abs', 0.0))


def results(src):
    return [run_case(src, t) for t in w['tests']]


tests, examples = w['tests'], w['examples']

# ---- shape ----
check(item['performance'] == 'code' and 'parts' not in item, 'performance kind is code, no parts')
check(len(tests) == 12 and len(examples) == 2 and len(tests) > len(examples), '12 tests against 2 examples')
check('12 hidden tests' in w['how'], 'how says 12 hidden tests')
check(all(t['compare'] == 'isclose' and t['tol'] == {'abs': 1e-09} for t in tests + examples), 'every case isclose within abs 1e-9')
check(examples[0]['call'] == tests[0]['call'] and examples[1]['call'] == tests[1]['call'], 'the two examples are tests 1 and 2')
check(len(doc['items']) <= 12, 'homework within 12 items (%d)' % len(doc['items']))
check(any(i.get('difficulty') == 5 for i in doc['items']), 'homework keeps a difficulty 5')
check(sum(1 for i in doc['items'] if i.get('performance')) == 1, 'one performance item in homework-2')

# ---- route 2: exact fractions on a grid, limits from far prices ----
def legs_of(call):
    inner = call[len('strategy_card('):-1]
    return eval(inner)


def exact_profit(legs, S):
    S = F(S)
    tot = F(0)
    for kind, q, k, p in legs:
        k, p = F(str(k)), F(str(p))
        if kind == 'call':
            tot += q * (max(S - k, 0) - p)
        elif kind == 'put':
            tot += q * (max(k - S, 0) - p)
        else:
            tot += q * (S - k)
    return tot


def route2(legs):
    cost = sum(F(q) * F(str(k if kind == 'stock' else p)) for kind, q, k, p in legs)
    grid = [F(i, 8) for i in range(0, 400 * 8 + 1)]
    vals = [exact_profit(legs, s) for s in grid]
    far1, far2 = exact_profit(legs, 10 ** 6), exact_profit(legs, 2 * 10 ** 6)
    up = far2 - far1  # change over a million pounds: the slope's sign beyond every strike
    best = math.inf if up > 0 else float(max(vals))
    worst = -math.inf if up < 0 else float(min(vals))
    roots = []
    for i, v in enumerate(vals):
        if v == 0:
            roots.append(grid[i])
        elif i + 1 < len(vals) and vals[i + 1] != 0 and (v < 0) != (vals[i + 1] < 0):
            a, b, va, vb = grid[i], grid[i + 1], v, vals[i + 1]
            roots.append(a + (b - a) * va / (va - vb))
    # beyond 400: the profit is a straight line, so solve it from the two far prices
    if vals[-1] != 0 and (far1 < 0) != (vals[-1] < 0):
        slope = up / 10 ** 6
        roots.append(F(10 ** 6) - far1 / slope)
    return {'cost': float(cost), 'best': best, 'worst': worst, 'breakevens': [float(r) for r in roots]}, roots


route2_cards = []
for i, t in enumerate(tests, 1):
    legs = legs_of(t['call'])
    card, exact_roots = route2(legs)
    route2_cards.append((card, exact_roots))
    expect = eval(t['expect'], {})
    check(close(card, expect, 0.0, 1e-12), f'test {i}: expect equals route 2 {card}')

# ---- route 3: hand formulas ----
hand = [
    # 1 bull call spread 120/130, D = 7.40 - 3.15
    {'cost': 7.40 - 3.15, 'best': (130 - 120) - (7.40 - 3.15), 'worst': -(7.40 - 3.15), 'breakevens': [120 + (7.40 - 3.15)]},
    # 2 straddle at 100, premium 5.25 + 4.75: break-evens K -/+ premium, worst at K
    {'cost': 10.0, 'best': math.inf, 'worst': -10.0, 'breakevens': [100 - 10.0, 100 + 10.0]},
    # 3 long put: best at S = 0 is K - p
    {'cost': 3.5, 'best': 95 - 3.5, 'worst': -3.5, 'breakevens': [95 - 3.5]},
    # 4 two long calls: break-even K + p (per call)
    {'cost': 2 * 6.0, 'best': math.inf, 'worst': -12.0, 'breakevens': [100 + 6.0]},
    # 5 short strangle: credit 5.5; break-evens 90 - 5.5 and 110 + 5.5; worst at S = 0 is 5.5 - 90 but above is unlimited
    {'cost': -(2.5 + 3.0), 'best': 5.5, 'worst': -math.inf, 'breakevens': [90 - 5.5, 110 + 5.5]},
    # 6 butterfly 95/100/105 at 7.5, 4.0, 1.5: cost 7.5 - 8 + 1.5, tent 5, break-evens 95 + D, 105 - D
    {'cost': 1.0, 'best': 5 - 1.0, 'worst': -1.0, 'breakevens': [95 + 1.0, 105 - 1.0]},
    # 7 covered call: cost 100 - 3, capped at 110 - 100 + 3, worst at S = 0, break-even 100 - 3
    {'cost': 97.0, 'best': 13.0, 'worst': -97.0, 'breakevens': [97.0]},
    # 8 collar: share 50, put 45 at 1.25, call 60 at 1.75; net premium -0.5
    {'cost': 50 + 1.25 - 1.75, 'best': (60 - 50) + 0.5, 'worst': (45 - 50) + 0.5, 'breakevens': [50 - 0.5]},
    # 9 calls 100 and 105 at 4 and 1: S - 105 between the strikes, so zero exactly at 105
    {'cost': 5.0, 'best': math.inf, 'worst': -5.0, 'breakevens': [105.0]},
    # 10 sell the 100 call at 6, buy two 105 calls at 0.5: credit 5; 5 - (S - 100) hits 0 at 105, then slope +1
    {'cost': -6.0 + 1.0, 'best': math.inf, 'worst': 0.0, 'breakevens': [105.0]},
    # 11 buy the 100 call at 5.5, sell four 110 calls at 1.25: cost 0.5; at 110 profit 9.5; slope 1 - 4 = -3
    {'cost': 5.5 - 4 * 1.25, 'best': 10 - 0.5, 'worst': -math.inf, 'breakevens': [100 + 0.5, 110 + 9.5 / 3]},
    # 12 short share at 100 and a long 100 call at 6: a synthetic long put, 94 at S = 0, -6 above 100
    {'cost': -100 + 6.0, 'best': 100 - 6.0, 'worst': -6.0, 'breakevens': [100 - 6.0]},
]
for i, (t, h) in enumerate(zip(tests, hand), 1):
    check(close(h, eval(t['expect'], {}), 0.0, 1e-12), f'test {i}: expect equals the hand formula')

# grid-search catch: test 11's upper break-even is not a multiple of 0.01
r = route2_cards[10][1][-1]
check(r == F(679, 6) and (r * 100).denominator != 1, 'test 11: break-even 679/6 = 113.1667 is off any 0.01 grid')
check(route2_cards[9][0]['worst'] == 0.0 and route2_cards[9][1] == [105], 'test 10: touches 0 at 105 only')
check(route2_cards[8][1] == [105], 'test 9: crosses 0 at the strike 105 only')

# ---- route 1: the solution passes every example and test; the starter fails every test ----
for i, t in enumerate(examples, 1):
    check(run_case(w['solution'], t), f'solution passes example {i}')
sol = results(w['solution'])
check(all(sol), f'solution passes all 12 tests ({sum(sol)})')
st = results(w['starter'])
check(not any(st), 'starter fails every test')

# ---- planted wrong solutions ----
SOL = w['solution']


def mutate(old, new, src=SOL):
    assert old in src, old
    return src.replace(old, new, 1)


bugs = {
    # strikes only: no price of 0, so a put's best and a lower break-even are lost
    'no S = 0': (mutate('sorted({0.0} | {', 'sorted(set() | {'), 2),
    # no slope test: the extremes come from the listed prices only
    'no slope': (mutate('best = float("inf") if slope > 0 else max(values)\n    worst = float("-inf") if slope < 0 else min(values)',
                        'best = max(values)\n    worst = min(values)'), 2),
    # a far price instead of the slope: finite best for an unlimited position
    'far price': (mutate('best = float("inf") if slope > 0 else max(values)\n    worst = float("-inf") if slope < 0 else min(values)',
                         'far = _profit(10 * points[-1])\n    best = max(values + [far])\n    worst = min(values + [far])'), 2),
    # premium taken as always paid, whatever the side
    'abs qty in cost': (mutate('cost += qty * (strike if kind == "stock" else premium)',
                               'cost += abs(qty) * (strike if kind == "stock" else premium)'), 1),
    # the share's purchase price left out of the cost
    'share not in cost': (mutate('cost += qty * (strike if kind == "stock" else premium)',
                                 'cost += qty * (0 if kind == "stock" else premium)'), 7),
    # the share left out of the slope
    'share not in slope': (mutate('if kind != "put")', 'if kind == "call")'), 7),
    # strikes in the order given
    'unsorted strikes': (mutate('points = sorted({0.0} | {float(k) for kind, q, k, p in legs if kind != "stock"})',
                                'points = [0.0] + [float(k) for kind, q, k, p in legs if kind != "stock"]'), 6),
    # a zero at a strike counted from both sides
    'double root': (mutate('elif abs(pb) >= zero and (pa < 0) != (pb < 0):',
                           'if abs(pb) < zero or (pa < 0) != (pb < 0):'), 9),
    # sign changes only: a touch at 0 is missed
    'touch missed': (mutate('    if abs(last) < zero:\n        roots.append(points[-1])\n    elif',
                            '    if False:\n        pass\n    elif'), 9),
    # only between strikes: no break-even above the top strike
    'no top root': (mutate('elif slope != 0 and (last < 0) != (slope < 0):', 'elif False:'), 2),
    # a grid search to the penny
    'grid 0.01': ('''def strategy_card(legs):
    def profit(S):
        t = 0.0
        for kind, qty, strike, premium in legs:
            if kind == "call":
                t += qty * (max(S - strike, 0) - premium)
            elif kind == "put":
                t += qty * (max(strike - S, 0) - premium)
            else:
                t += qty * (S - strike)
        return t
    cost = sum(q * (k if kind == "stock" else p) for kind, q, k, p in legs)
    grid = [i / 100 for i in range(0, 40001)]
    vals = [profit(s) for s in grid]
    slope = sum(q for kind, q, k, p in legs if kind != "put")
    best = float("inf") if slope > 0 else max(vals)
    worst = float("-inf") if slope < 0 else min(vals)
    roots = [round(s, 2) for s, v in zip(grid, vals) if abs(v) < 0.005]
    return {"cost": cost, "best": best, "worst": worst, "breakevens": roots}
''', 11),
    # a sign-change test without the zero tolerance, on exact-zero kinks
    'touch at top missed by strict sign test': (mutate('elif abs(pb) >= zero and (pa < 0) != (pb < 0):',
                                                       'elif pa * pb <= 0:'), 9),
}
for name, (src, first_expected) in bugs.items():
    res = results(src)
    failed = [i + 1 for i, ok in enumerate(res) if not ok]
    check(len(failed) > 0, f'planted bug "{name}" fails tests {failed}')
    if failed:
        check(failed[0] == first_expected, f'planted bug "{name}" fails first at test {first_expected} (got {failed[0]})')
check(len(bugs) >= 3, f'{len(bugs)} planted bugs, at least 3')

# byKey lines name tests that exist
for k in item['feedback']['byKey']:
    n = int(k.split('-')[1])
    check(1 <= n <= len(tests), f'byKey {k} names an existing test')

print('failures:', fails)
raise SystemExit(1 if fails else 0)
