"""Recompute every number in conditional homework-2 item h-two-filters (performance task, derivation).

Run from the repo root with any Python 3 (standard library only):
    python3 docs/reports/conditional-2-perf-numbers.py      exits 0 when every check passes.
Route A: exact enumeration in Fractions of the eight outcomes (kind of tick, jump flag, venue flag),
then conditioning by counting chance inside the event. Route B: the closed forms and the odds form.
Route C: a seeded simulation of 2,000,000 ticks for each model (independent flags, and the shared stale quote).
Then every number printed in the item is checked against these, every passing tick set of the rubric is
listed, and no pass may skip a part the prompt names (parts 1 to 4).
"""
import itertools, json, os, random, re, sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/conditional/homework-2.json')
doc = json.load(open(HW))
item = next(i for i in doc['items'] if i['id'] == 'h-two-filters')
fails = []
def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)

b, hJ, fJ, hV, fV = F(2, 100), F(9, 10), F(6, 100), F(7, 10), F(3, 100)

# ---- route A: the joint law of (bad, J, V) as eight outcomes ----
def joint_independent():
    law = {}
    for bad, j, v in itertools.product((1, 0), repeat=3):
        pk = b if bad else 1 - b
        pj = (hJ if bad else fJ) if j else 1 - (hJ if bad else fJ)
        pv = (hV if bad else fV) if v else 1 - (hV if bad else fV)
        law[(bad, j, v)] = pk * pj * pv
    return law

def joint_stale():
    """Bad ticks: independent flags. Good ticks: V only together with J, P(V | G) = fV, P(J | G) = fJ."""
    law = {}
    for bad, j, v in itertools.product((1, 0), repeat=3):
        if bad:
            pj = hJ if j else 1 - hJ
            pv = hV if v else 1 - hV
            law[(bad, j, v)] = b * pj * pv
        else:
            # good: (J, V) = (1, 1) with fV, (1, 0) with fJ - fV, (0, 0) with 1 - fJ, (0, 1) impossible
            p = {(1, 1): fV, (1, 0): fJ - fV, (0, 0): 1 - fJ, (0, 1): F(0)}[(j, v)]
            law[(bad, j, v)] = (1 - b) * p
    return law

def cond(law, target, given):
    top = sum(p for o, p in law.items() if target(o) and given(o))
    bot = sum(p for o, p in law.items() if given(o))
    return top / bot

for name, law in (('independent', joint_independent()), ('stale', joint_stale())):
    check(f'{name}: the eight outcomes sum to 1', sum(law.values()) == 1)
    check(f'{name}: margins match the stated rates',
          cond(law, lambda o: o[1], lambda o: o[0] == 1) == hJ and cond(law, lambda o: o[1], lambda o: o[0] == 0) == fJ
          and cond(law, lambda o: o[2], lambda o: o[0] == 1) == hV and cond(law, lambda o: o[2], lambda o: o[0] == 0) == fV)

LI, LS = joint_independent(), joint_stale()
A_J = cond(LI, lambda o: o[0] == 1, lambda o: o[1] == 1)
A_JV = cond(LI, lambda o: o[0] == 1, lambda o: o[1] == 1 and o[2] == 1)
A_JS = cond(LS, lambda o: o[0] == 1, lambda o: o[1] == 1)
A_JVS = cond(LS, lambda o: o[0] == 1, lambda o: o[1] == 1 and o[2] == 1)
check('stale model leaves P(B | J) unchanged', A_JS == A_J)
check('stale model: on good ticks V lies inside J', LS[(0, 0, 1)] == 0)
check('stale model: P(J and V | G) = 0.03', cond(LS, lambda o: o[1] == 1 and o[2] == 1, lambda o: o[0] == 0) == F(3, 100))

# ---- route B: closed forms and odds ----
B_J = hJ * b / (hJ * b + fJ * (1 - b))
B_JV = hJ * hV * b / (hJ * hV * b + fJ * fV * (1 - b))
odds = b / (1 - b) * (hJ / fJ) * (hV / fV)
B_JV_odds = odds / (1 + odds)
B_JVS = hJ * hV * b / (hJ * hV * b + fV * (1 - b))
oddsJ = A_J / (1 - A_J)
second_lr = hV / (fV / fJ)            # P(V | J, B) / P(V | J, G) in the stale model
B_JVS_odds = oddsJ * second_lr / (1 + oddsJ * second_lr)

check('P(B | J) = 15/64 by both routes', A_J == B_J == F(15, 64), str(A_J))
check('P(B | J and V) = 50/57 by three routes', A_JV == B_JV == B_JV_odds == F(50, 57), str(A_JV))
check('stale: P(B | J and V) = 3/10 by three routes', A_JVS == B_JVS == B_JVS_odds == F(3, 10), str(A_JVS))
check('odds after both are 50/7', odds == F(50, 7))
check('prior odds 1/49, LR_J 15, LR_V 70/3', b / (1 - b) == F(1, 49) and hJ / fJ == 15 and hV / fV == F(70, 3))
check('odds after J are 15/49', oddsJ == F(15, 49))
check('stale: V follows J on good ticks with chance 0.5', fV / fJ == F(1, 2))
check('stale: second ratio 1.4, odds 3/7', second_lr == F(7, 5) and oddsJ * second_lr == F(3, 7))

# the shown arithmetic, each line recomputed
shown = {
    '0.02 x 0.9 = 0.018': (b * hJ, F(18, 1000)),
    '0.98 x 0.06 = 0.0588': ((1 - b) * fJ, F(588, 10000)),
    'P(J) = 0.0768': (b * hJ + (1 - b) * fJ, F(768, 10000)),
    '0.018 / 0.0768 = 15/64': (F(18, 1000) / F(768, 10000), F(15, 64)),
    '0.02 x 0.9 x 0.7 = 0.0126': (b * hJ * hV, F(126, 10000)),
    '0.98 x 0.06 x 0.03 = 0.001764': ((1 - b) * fJ * fV, F(1764, 1000000)),
    '0.0126 + 0.001764 = 0.014364': (F(126, 10000) + F(1764, 1000000), F(14364, 1000000)),
    '0.0126 / 0.014364 = 50/57': (F(126, 10000) / F(14364, 1000000), F(50, 57)),
    '1/49 x 15 x 70/3 = 50/7': (F(1, 49) * 15 * F(70, 3), F(50, 7)),
    'f_J f_V = 0.0018': (fJ * fV, F(18, 10000)),
    '0.98 x 0.03 = 0.0294': ((1 - b) * fV, F(294, 10000)),
    '0.0126 + 0.0294 = 0.042': (F(126, 10000) + F(294, 10000), F(42, 1000)),
    '0.0126 / 0.042 = 3/10': (F(126, 10000) / F(42, 1000), F(3, 10)),
    '0.03 / 0.06 = 0.5': (fV / fJ, F(1, 2)),
    '0.7 / 0.5 = 1.4': (F(7, 10) / F(1, 2), F(14, 10)),
}
for k, (x, y) in shown.items():
    check(f'shown: {k}', x == y, str(x))
check('rounded: 15/64 ~ 0.234, 50/57 ~ 0.877', round(float(F(15, 64)), 3) == 0.234 and round(float(F(50, 57)), 3) == 0.877)

# ---- route C: seeded simulation ----
def simulate(stale, n, seed):
    rng = random.Random(seed)
    cJ = cJb = cJV = cJVb = 0
    for _ in range(n):
        bad = rng.random() < 0.02
        if bad or not stale:
            j = rng.random() < (0.9 if bad else 0.06)
            v = rng.random() < (0.7 if bad else 0.03)
        else:
            u = rng.random()                 # good tick, shared stale quote
            j, v = u < 0.06, u < 0.03        # V only with J
        if j:
            cJ += 1; cJb += bad
            if v:
                cJV += 1; cJVb += bad
    return cJb / cJ, cJVb / cJV, cJ, cJV
for stale, seed, exact in ((False, 11, (A_J, A_JV)), (True, 12, (A_JS, A_JVS))):
    pj, pjv, nj, njv = simulate(stale, 2_000_000, seed)
    se_j = (float(exact[0]) * (1 - float(exact[0])) / nj) ** 0.5
    se_jv = (float(exact[1]) * (1 - float(exact[1])) / njv) ** 0.5
    check(f'simulation ({"stale" if stale else "independent"}): P(B | J) within 4 se',
          abs(pj - float(exact[0])) < 4 * se_j, f'{pj:.4f} vs {float(exact[0]):.4f}, se {se_j:.4f}')
    check(f'simulation ({"stale" if stale else "independent"}): P(B | J and V) within 4 se',
          abs(pjv - float(exact[1])) < 4 * se_jv, f'{pjv:.4f} vs {float(exact[1]):.4f}, se {se_jv:.4f}')

# ---- the numbers printed in the item ----
text = item['prompt'] + '\n' + item['model'] + '\n' + '\n'.join(r['text'] for r in item['rubric'])
for tok in ['b = 0.02', 'h_J = 0.9', 'f_J = 0.06', 'h_V = 0.7', 'f_V = 0.03', '0.018', '0.0588', '0.0768', '\\frac{15}{64}', '0.234',
            '0.0126', '0.001764', '0.014364', '\\frac{50}{57}', '0.877', '\\tfrac{50}{7}', '0.0018', '0.0294', '0.042', '\\frac{3}{10}',
            '\\tfrac{15}{49}', '\\tfrac{3}{7}', '1.4', '\\tfrac{70}{3}', '\\tfrac{1}{49}']:
    check(f'item states {tok}', tok in text)
nums = set(re.findall(r'\d+\.\d+', text))
known = {'0.02', '0.9', '0.06', '0.7', '0.03', '0.018', '0.0588', '0.0768', '0.234', '0.0126', '0.001764', '0.014364', '0.877',
         '0.0018', '0.98', '0.0294', '0.042', '0.5', '1.4', '0.3'}
check('every decimal in the item is one recomputed here', nums <= known, str(sorted(nums - known)))

# ---- rubric: every passing tick set, and the named parts ----
rub = item['rubric']
check('rubric sums to 10 with 5 rows', sum(r['points'] for r in rub) == 10 and len(rub) == 5)
check('not every row is required', not all(r.get('required') for r in rub))
parts = {1: 0, 2: 1, 3: 2, 4: 3}    # prompt part -> rubric row (0-based) that grades it
passing = []
for ticks in itertools.product((0, 1), repeat=len(rub)):
    pts = sum(r['points'] for r, t in zip(rub, ticks) if t)
    if pts >= 7 and all(t for r, t in zip(rub, ticks) if r.get('required')):
        passing.append(ticks)
for t in passing:
    rows = [i + 1 for i, x in enumerate(t) if x]
    skipped = [p for p, row in parts.items() if not t[row]]
    print('     passing set: rows', rows, 'points', sum(rub[i - 1]['points'] for i in rows), 'skips parts', skipped or 'none')
    check(f'pass {rows} skips no named part', not skipped)
check('two passing sets', len(passing) == 2)

items = doc['items']
check('homework has 6 to 12 items', 6 <= len(items) <= 12, str(len(items)))
check('one performance item in the homework', sum(1 for i in items if i.get('performance')) == 1)
check('item is last, difficulty 5, longform derivation', items[-1]['id'] == 'h-two-filters' and item['difficulty'] == 5
      and item['kind'] == 'longform' and item['performance'] == 'derivation')
check('no starter, steps, order, derive, hints or parts', not any(k in item for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')))
print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
