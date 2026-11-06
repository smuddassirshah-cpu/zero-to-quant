"""Second route for app/content/exams/mock-oa-strats.json. Exits 1 on any failure.

Independent of mock-oa-strats_build.py: every maths key and every distractor slip is recomputed here with SymPy
(symbolic derivative, series, integral, dsolve, characteristic polynomial, exact enumeration and a PSD scan with
NumPy), each option's KaTeX is turned into a number, and the key must equal route B while each distractor must
equal its named slip and differ from the key. Every number in every learner-visible string of each item must match
a route-B value for that item to its printed precision (whole numbers 0 to 10 are structure). Code items: the
solution passes every hidden test and example in CPython, the starter and planted wrong versions fail at least
one, and each small test's expected value equals a brute-force method. Uses app/tools/numbers_lib.py.
Run: python3 -I docs/briefs/mocks-scripts/mock-oa-strats_check.py
"""
import itertools
import json
import math
import os
import re
import sys
import time

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _FRAC, _NUM, normalise  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'mock-oa-strats.json')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
paths, items = {}, {}
for pi, part in enumerate(doc['parts']):
    for ii, it in enumerate(part.get('items', [])):
        paths[it['id']], items[it['id']] = f'parts[{pi}].items[{ii}]', it
ALLOW = {}


def allow(iid, *vals):
    ALLOW.setdefault(iid, []).extend(abs(float(v)) for v in vals)


def rec(ok, label, note=''):
    ex._rec(bool(ok), label, note)


x, y, r, lam = sp.symbols('x y r lam')


def tex_value(t):
    """KaTeX option text to a SymPy number, or a sorted tuple for 'a and b'."""
    s = t.strip().strip('$')
    if ' and ' in t:
        return tuple(sorted(tex_value(p) for p in re.split(r'\$?\s+and\s+\$?', t.strip().strip('$'))))
    s = re.sub(r'\\tfrac\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', s)
    s = re.sub(r'\\ln\s*(\d+)', r'log(\1)', s)
    s = s.replace('e^2', 'E**2').replace('^', '**')
    s = re.sub(r'(\d)E', r'\1*E', s)
    s = re.sub(r'\be\b', 'E', s)
    return sp.sympify(s, locals={'E': sp.E, 'log': sp.log})


def num(v):
    return tuple(float(u) for u in v) if isinstance(v, tuple) else float(v)


def same(a, b):
    a, b = num(a), num(b)
    if isinstance(a, tuple) or isinstance(b, tuple):
        return isinstance(a, tuple) and isinstance(b, tuple) and len(a) == len(b) and all(abs(p - q) < 1e-9 for p, q in zip(a, b))
    return abs(a - b) < 1e-9 * max(1, abs(b))


def check_choice(iid, key, slips):
    """key: route-B value; slips: list of route-B values, one per distractor in file order."""
    w = items[iid]['widget']
    rec(w.get('shuffle') is True, f'{iid}: shuffle true')
    opts = w['options']
    keys = [o for o in opts if o.get('correct')]
    rec(len(keys) == 1, f'{iid}: exactly one correct option')
    rec(same(tex_value(keys[0]['text']), key), f'{iid}: key {keys[0]["text"]} = route B {num(key)}')
    others = [o for o in opts if not o.get('correct')]
    rec(len(others) == len(slips), f'{iid}: {len(slips)} distractors')
    for o, s in zip(others, slips):
        v = tex_value(o['text'])
        rec(same(v, s) and not same(v, key), f'{iid}: distractor {o["text"]} = its slip {num(s)}, not the key')
        rec(bool(o.get('why')) and o['why'].startswith('You '), f'{iid}: distractor {o["text"]} has a why naming the action')
    def bare(t):
        return re.sub(r'\$|\\tfrac|[{}\\]', '', t)
    kl = len(bare(keys[0]['text']))
    rec(not (kl >= 12 and all(kl > 1.5 * len(bare(o['text'])) for o in others)), f'{iid}: key not far longer')
    for v in [key] + list(slips):
        allow(iid, *(num(v) if isinstance(v, tuple) else [num(v)]))


# ---------------------------------------------------------------- maths, route B (SymPy)
f1 = sp.log(1 + 3 * x ** 2)
k1 = sp.diff(f1, x).subs(x, 1)
s1 = [sp.diff(sp.log(y), y).subs(y, 1 + 3 * x ** 2).subs(x, 1),    # outer only
      sp.diff(1 + 3 * x ** 2, x).subs(x, 1),                        # inner only
      f1.subs(x, 1)]                                                 # the value
check_choice('m1-chain-rule', k1, s1)
allow('m1-chain-rule', 6, 4, 1e-6, 6, 3, 2)
ex.expect('exam', paths['m1-chain-rule'] + '.explain.text', float(k1))

M = sp.Matrix([[5, 4], [1, 2]])
ev = tuple(sorted(M.eigenvals().keys()))
cp = M.charpoly(lam).as_expr()
s2 = [tuple(sorted([M[0, 0], M[1, 1]])), tuple(sorted(sp.solve(cp.subs(lam, -lam), lam))), tuple(sorted([M.det(), M.trace()]))]
check_choice('m2-eigenvalues', ev, s2)
for vv, lv in ((sp.Matrix([4, 1]), 6), (sp.Matrix([1, -1]), 1)):
    rec(M * vv == lv * vv, f'm2: A{tuple(vv)} = {lv}{tuple(vv)}')
rec(sp.expand(cp) == lam ** 2 - 7 * lam + 6, 'm2: characteristic polynomial lam^2 - 7 lam + 6')
allow('m2-eigenvalues', 7, 6, 4, 1, 2, 5)

g3 = (sp.exp(2 * x) - 1 - 2 * x) / x ** 2
k3 = sp.limit(g3, x, 0)
ser = sp.series(sp.exp(2 * x), x, 0, 3).removeO()
rec(sp.expand(ser - (1 + 2 * x + 2 * x ** 2)) == 0, 'm3: e^{2x} = 1 + 2x + 2x^2 + O(x^3)')
s3 = [sp.limit((1 + 2 * x + (2 * x) ** 2 - 1 - 2 * x) / x ** 2, x, 0),     # (2x)^2 with no 1/2!
      sp.limit((1 + 2 * x + x ** 2 / 2 - 1 - 2 * x) / x ** 2, x, 0),       # x^2/2
      sp.Integer(0)]
check_choice('m3-limit', k3, s3)
q3x = float(g3.subs(x, sp.Rational(1, 10 ** 4)).evalf(30))
allow('m3-limit', q3x, 1e-4, 2, 3)
ex.expect('exam', paths['m3-limit'] + '.explain.text', 2.0001)
rec(abs(q3x - 2.0001) < 0.00005, f'm3: quotient at 1e-4 is {q3x:.6f}, stated as 2.0001')

pA, pB, fA, fB = sp.Rational(3, 5), sp.Rational(2, 5), sp.Rational(1, 50), sp.Rational(1, 20)
trades = [('A', bool(i < 12)) for i in range(600)] + [('B', bool(i < 20)) for i in range(400)]   # 1,000 trades
fails = [t for t in trades if t[1]]
k4 = sp.Rational(sum(1 for t in fails if t[0] == 'B'), len(fails))
rec(k4 == pB * fB / (pA * fA + pB * fB), 'm4: count of 1,000 trades = Bayes')
s4 = [1 - k4, fB, sp.Float(round(5 / 7, 3))]
check_choice('m4-probability-tree', k4, s4)
rec(abs(float(sp.Rational(5, 7)) - 0.714) < 0.0005, 'm4: 5/7 printed as 0.714')
allow('m4-probability-tree', 0.6, 0.4, 0.02, 0.05, 0.012, 0.032, 1000, 12, 20, 60, 40, 2, 5, 0.714)
ex.expect('exam', paths['m4-probability-tree'] + '.explain.text', 0.625)

k5 = sp.integrate(sp.log(x) / x ** 2, (x, 1, sp.E))
anti = sp.integrate(sp.log(x) / x ** 2, x)
s5 = [sp.integrate(1 / x ** 2, (x, 1, sp.E)),                     # dropped the boundary term
      -k5,                                                         # v = +1/x
      anti.subs(x, sp.E)]                                          # no lower limit
check_choice('m5-by-parts', k5, s5)
rec(sp.simplify(anti.subs(x, 1)) == -1 and sp.simplify(anti.subs(x, sp.E) + 2 / sp.E) == 0, 'm5: antiderivative -1 at 1 and -2/e at e')
allow('m5-by-parts', 1, 2, float(k5), -2, 1)
ex.expect('exam', paths['m5-by-parts'] + '.explain.text', 0.264)
rec(abs(float(k5) - 0.264) < 0.0005, f'm5: {float(k5):.5f} printed as 0.264')

Y = sp.Function('Y')
sol = sp.dsolve(sp.Eq(Y(x).diff(x), 2 * Y(x) + 4), Y(x), ics={Y(0): 1}).rhs
k6 = sol.subs(x, 1)
s6 = [sp.dsolve(sp.Eq(Y(x).diff(x), 2 * Y(x)), Y(x), ics={Y(0): 1}).rhs.subs(x, 1),
      (sol + 2).subs(x, 1),
      (-4 + (1 + 4) * sp.exp(2 * x)).subs(x, 1)]
check_choice('m6-linear-ode', k6, s6)
rec(sp.simplify(sol - (3 * sp.exp(2 * x) - 2)) == 0, 'm6: y = 3e^{2x} - 2')
allow('m6-linear-ode', 2, 4, 1, 3, -2, 4, -4, 0, float(k6))
ex.expect('exam', paths['m6-linear-ode'] + '.explain.text', 20.17)
rec(abs(float(k6) - 20.17) < 0.005, f'm6: {float(k6):.4f} printed as 20.17')

# route B for m7: count labelled seatings (9! orders, books are positions 0-2, 3-5, 6-8)
hit = tot = 0
for perm in itertools.permutations(range(9)):
    tot += 1
    pos = [perm.index(t) // 3 for t in (0, 1, 2)]
    hit += pos[0] == pos[1] == pos[2]
k7 = sp.Rational(hit, tot)
two = sp.Rational(sum(1 for perm in itertools.permutations(range(9)) if perm.index(0) // 3 == perm.index(1) // 3), tot)
s7 = [sp.Rational(1, 9), sp.Rational(1, math.comb(9, 3)), two]
check_choice('m7-shared-book', k7, s7)
unordered = math.factorial(9) // (math.factorial(3) ** 3 * math.factorial(3))
kept = math.factorial(6) // (math.factorial(3) ** 2 * math.factorial(2))
rec((unordered, kept) == (280, 10) and sp.Rational(kept, unordered) == k7, 'm7: 10 of 280 unordered splits')
allow('m7-shared-book', 2, 8, 1, 7, 2, 56, 1, 28, float(k7), 10, 280, 9, 3, 84)
ex.expect('exam', paths['m7-shared-book'] + '.explain.text', 0.036)
rec(abs(float(k7) - 0.036) < 0.0005, f'm7: {float(k7):.5f} printed as 0.036')


def min_eig(rv):
    C = np.array([[1, 0.8, rv], [0.8, 1, 0.8], [rv, 0.8, 1]])
    return np.linalg.eigvalsh(C)[0]


grid = np.round(np.arange(-100, 101) / 100, 2)
feasible = [g for g in grid if min_eig(g) >= -1e-12]
k8 = sp.Rational(str(min(feasible)))
detr = sp.Matrix([[1, sp.Rational(4, 5), r], [sp.Rational(4, 5), 1, sp.Rational(4, 5)], [r, sp.Rational(4, 5), 1]]).det()
rec(sp.expand(detr) == -r ** 2 + sp.Rational(32, 25) * r - sp.Rational(7, 25), 'm8: determinant -r^2 + 1.28 r - 0.28')
rec(sorted(sp.solve(detr, r)) == [sp.Rational(7, 25), 1], 'm8: determinant roots 0.28 and 1')
s8 = [sp.Rational(16, 25), sp.Rational(4, 5) * 2 - 1, sp.Integer(0)]
check_choice('m8-correlation-bound', k8, s8)
ang = math.degrees(math.acos(0.8))
allow('m8-correlation-bound', 0.8, 3, 3, 1.28, 0.28, 1, round(ang, 1), round(2 * ang, 1), 0.28)
rec(abs(math.cos(math.radians(2 * ang)) - 0.28) < 1e-12, 'm8: cos of twice the angle is 0.28')

# ---------------------------------------------------------------- code items, run in CPython


def run_code(src, case, fn_check=None):
    g = {}
    exec(src, g)
    if case.get('setup'):
        exec(case['setup'], g)
    t0 = time.perf_counter()
    try:
        got = eval(case['call'], g)
    except Exception as e:              # noqa: BLE001
        return False, f'raised {type(e).__name__}', 0
    ms = (time.perf_counter() - t0) * 1000
    want = eval(case['expect'], {})
    return got == want, repr(got)[:60], ms


WRONG = {
    'c1-net-positions': {
        'sell adds': 'def net_positions(fills):\n    net = {}\n    for f in fills:\n        a, s, q = f.split()\n        net[a] = net.get(a, 0) + int(q)\n    return [[a, n] for a, n in sorted(net.items()) if n != 0]\n',
        'zero kept': 'def net_positions(fills):\n    net = {}\n    for f in fills:\n        a, s, q = f.split()\n        net[a] = net.get(a, 0) + (int(q) if s == "B" else -int(q))\n    return [[a, n] for a, n in sorted(net.items())]\n',
        'unsorted': 'def net_positions(fills):\n    net = {}\n    for f in fills:\n        a, s, q = f.split()\n        net[a] = net.get(a, 0) + (int(q) if s == "B" else -int(q))\n    return [[a, n] for a, n in net.items() if n != 0]\n',
    },
    'c2-fewest-days': {
        'more than': 'def fewest_days(volumes, target):\n    best = len(volumes) + 1\n    left, total = 0, 0\n    for right, v in enumerate(volumes):\n        total += v\n        while total > target:\n            best = min(best, right - left + 1)\n            total -= volumes[left]\n            left += 1\n    return best if best <= len(volumes) else 0\n',
        'no-block as n+1': 'def fewest_days(volumes, target):\n    best = len(volumes) + 1\n    left, total = 0, 0\n    for right, v in enumerate(volumes):\n        total += v\n        while total >= target:\n            best = min(best, right - left + 1)\n            total -= volumes[left]\n            left += 1\n    return best\n',
    },
}


def brute_c1(fills):
    accts = sorted({f.split()[0] for f in fills})
    out = []
    for a in accts:
        n = sum((1 if f.split()[1] == 'B' else -1) * int(f.split()[2]) for f in fills if f.split()[0] == a)
        if n:
            out.append([a, n])
    return out


def brute_c2(vols, target):
    best = 0
    for i in range(len(vols)):
        for j in range(i, len(vols)):
            if sum(vols[i:j + 1]) >= target:
                best = j - i + 1 if best == 0 else min(best, j - i + 1)
                break
    return best


for iid, brute in (('c1-net-positions', brute_c1), ('c2-fewest-days', brute_c2)):
    w = items[iid]['widget']
    rec(w['language'] == 'python' and 3 <= len(w['tests']) <= 15, f'{iid}: Python, {len(w["tests"])} tests')
    rec(f'There are {len(w["tests"])} hidden tests.' in w['how'], f'{iid}: how line counts the tests')
    slow = 0
    for k, case in enumerate(w['examples'] + w['tests']):
        ok, got, ms = run_code(w['solution'], case)
        slow = max(slow, ms)
        rec(ok, f'{iid}: solution passes {"example" if k < len(w["examples"]) else "test"} {case["call"][:50]}', '' if ok else got)
        if not case.get('setup') and '*' not in case['call']:
            m = re.match(r'(?:\[list\(p\) for p in )?(\w+)\((.*)\)\]?$', case['call'])
            args = eval('(' + m.group(2) + ',)')
            rec(eval(case['expect']) == brute(*args), f'{iid}: expected {case["expect"][:30]} = brute force')
    rec(slow < 1500, f'{iid}: slowest test {slow:.0f} ms in CPython')
    allow(iid, len(w['tests']))
    start_fails = sum(1 for case in w['tests'] if not run_code(w['starter'], case)[0])
    rec(start_fails >= 1, f'{iid}: starter fails {start_fails} of {len(w["tests"])}')
    for name, src in WRONG[iid].items():
        fails = sum(1 for case in w['tests'] if not run_code(src, case)[0])
        rec(fails >= 1, f'{iid}: wrong version "{name}" fails {fails}')
allow('c1-net-positions', 300, 100000, 7, 0)
allow('c2-fewest-days', 200000)

# ---------------------------------------------------------------- every number in every learner-visible string
SKIP = {'starter', 'solution', 'tests', 'examples', 'id', 'tags', 'skills', 'pace', 'difficulty', 'label', 'layout', 'kind', 'language'}


def strings(o, k=None):
    if isinstance(o, str):
        if k not in SKIP:
            yield o
    elif isinstance(o, dict):
        for kk, vv in o.items():
            if kk not in SKIP:
                yield from strings(vv, kk)
    elif isinstance(o, list):
        for vv in o:
            yield from strings(vv, k)


def tokens(s):
    s = re.sub(r'`[^`]*`', ' ', s)                    # code spans are names and literals, checked by the tests
    s = _FRAC.sub(lambda m: f' {m.group(1) or m.group(3)} {m.group(2) or m.group(4)} ', s)
    s = re.sub(r'10\^\{-?\d+\}', ' ', s)
    for m in _NUM.finditer(normalise(s)):
        t = m.group(0).rstrip('.')
        yield abs(float(t)), (len(t.split('.')[1]) if '.' in t else 0), t


for iid, it in items.items():
    vals = ALLOW.get(iid, [])
    bad = []
    for s in strings(it):
        if '—' in s or '–' in s or '!' in re.sub(r'\$[^$]*\$', '', s):
            bad.append('dash-or-bang')
        for val, dec, t in tokens(s):
            if dec == 0 and val == int(val) and val <= 10:
                continue
            half = 0.5 * 10 ** -dec
            if not any(abs(val - a) < half * (1 - 1e-9) + 1e-12 for a in vals):
                bad.append(t)
    rec(not bad, f'{iid}: every stated number matches route B', f'unmatched {sorted(set(bad))}' if bad else '')

# description, models and paper numbers
ex.expect('exam', 'models', 30)
ex.expect('exam', 'models', 22)
ex.expect('exam', 'description', 22)
rec(doc['parts'][0]['minutes'] == 30 and doc['parts'][1]['minutes'] == 22, 'papers 30 and 22 minutes')
rec(len(doc['parts'][1]['items']) == 8 and len(doc['parts'][0]['items']) == 2, '8 maths and 2 code items')
rec(sum(i['pace'] for i in doc['parts'][0]['items']) <= 1800 and sum(i['pace'] for i in doc['parts'][1]['items']) <= 1320, 'pace within each paper')
rec(len(doc['models']) <= 200 and 'Reported, as of Nov 2026' in doc['models'], 'models: reported, Nov 2026, under 200 characters')

ex.check_wrongs()
ex.report()
