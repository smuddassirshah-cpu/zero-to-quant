"""Second reader's number script for app/content/exams/topic-0.2.json (review-exam-0.2.md).

Recomputes every graded key and every wrong[] value, and the numbers in prose, feedback, explanations and the longform
model, each by two routes: exact algebra in Fraction (formula, Cramer's rule, completing the square) and a second,
independent route (brute force over integers or quarters, a fine grid search, substitution back, or evaluation of both
expressions at random points). Expression keys are checked by evaluating the stored LaTeX at 40 random points with a
small converter written here (no SymPy on this machine). A check that fails because the content is wrong stays failing;
each such check is a finding in the review.
Pure standard library. Run: python3 docs/reviews/exam-0.2-scripts/numbers.py
"""
import os
import sys

# This file is named numbers.py, which shadows the standard library's `numbers` (fractions imports it).
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or os.getcwd()) != HERE]

import json  # noqa: E402
import math  # noqa: E402
import random  # noqa: E402
import re  # noqa: E402
from fractions import Fraction as F  # noqa: E402

sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-0.2.json')
COURSES = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'courses')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
idx = {it['id']: k for k, it in enumerate(doc['items'])}
IT = {it['id']: it for it in doc['items']}


def P(iid):
    return f'items[{idx[iid]}]'


def node(path):
    return _walk(doc, path)[0]


def W(iid):
    return IT[iid]['widget']


def near(a, b, t=1e-9):
    return abs(a - b) <= t


def key(iid, value, t=None):
    w = W(iid)
    tol = w.get('tol', {}).get('abs', 0)
    t = t if t is not None else max(tol / 10, 1e-9)
    ok = near(w['answer'], float(value), t)
    ex._rec(ok, f'{iid} answer {w["answer"]!r} = {float(value):.6g}', '' if ok else 'recomputed value differs')


def wrong(iid, wid, value, typed=None):
    ws = [x for x in W(iid).get('wrong', []) if x['id'] == wid]
    if not ws:
        return ex._rec(False, f'{iid} wrong "{wid}" exists', 'no such wrong id')
    v = ws[0]
    ok = near(v['value'], float(value), max(v.get('tol', {}).get('abs', 1e-9) / 10, 1e-9))
    ex._rec(ok, f'{iid} wrong "{wid}" {v["value"]!r} = {float(value):.6g}', '' if ok else 'recomputed slip differs')
    if typed is not None:
        ok2 = abs(typed - v['value']) <= v.get('tol', {}).get('abs', 1e-9) + 1e-9
        ex._rec(ok2, f'{iid} wrong "{wid}" catches a typed {typed!r}', '' if ok2 else 'typed slip misses its own band')


def inband(iid, typed):
    w = W(iid)
    ok = abs(typed - w['answer']) <= w['tol']['abs'] + 1e-9
    ex._rec(ok, f'{iid} a typed {typed!r} is graded right', '' if ok else 'outside the answer tolerance')


def correct_ids(iid):
    return sorted(o['id'] for o in W(iid)['options'] if o.get('correct'))


def opt(iid, oid):
    return next(o for o in W(iid)['options'] if o['id'] == oid)


# ---------------------------------------------------------------- a small LaTeX to Python evaluator
def _frac(s):
    while '\\frac' in s:
        i = s.index('\\frac')
        j = i + 5
        parts = []
        for _ in range(2):
            if s[j] != '{':                       # \frac12
                parts.append(s[j]); j += 1; continue
            depth, k = 0, j
            while True:
                depth += {'{': 1, '}': -1}.get(s[k], 0)
                if depth == 0:
                    break
                k += 1
            parts.append(s[j + 1:k]); j = k + 1
        s = s[:i] + f'(({parts[0]})/({parts[1]}))' + s[j:]
    return s


def py(tex):
    s = tex.replace('\\left', '').replace('\\right', '').replace('\\cdot', '*').replace('\\times', '*').replace(' ', '')
    s = s.replace('\\sqrt{3}', '(3**0.5)')
    s = _frac(s).replace('{', '(').replace('}', ')').replace('^', '**')
    s = re.sub(r'(?<=[0-9a-z)])(?=[a-z(])', '*', s)
    return s


def ev(tex, env):
    return eval(py(tex), {}, dict(env))


def same_expr(a, b, letters, label, rnd=random.Random(7)):
    ok = True
    for _ in range(40):
        env = {c: rnd.uniform(-3, 3) for c in letters}
        try:
            va, vb = (ev(a, env) if isinstance(a, str) else a(**env)), (ev(b, env) if isinstance(b, str) else b(**env))
        except ZeroDivisionError:
            continue
        if not math.isclose(va, vb, rel_tol=1e-9, abs_tol=1e-9):
            ok = False
            break
    return ex.claim(ok, label)


def differ_expr(a, b, letters, label, rnd=random.Random(11)):
    env = {c: rnd.uniform(0.5, 3) for c in letters}
    va, vb = (ev(a, env) if isinstance(a, str) else a(**env)), (ev(b, env) if isinstance(b, str) else b(**env))
    return ex.claim(not math.isclose(va, vb, rel_tol=1e-6), label)


def quad_roots(a, b, c):
    d = b * b - 4 * a * c
    return d, sorted([(-b - math.sqrt(d)) / (2 * a), (-b + math.sqrt(d)) / (2 * a)]) if d >= 0 else []


# ---------------------------------------------------------------- metadata, shape, coverage
ex.claim(doc['minutes'] == 90 and doc['pass'] == 0.7, 'minutes 90 and pass 0.7 as stored')
ex.claim(20 <= len(doc['items']) <= 30, f'{len(doc["items"])} items, inside 20 to 30')
ramp = {d: sum(1 for it in doc['items'] if it['difficulty'] == d) for d in (2, 3, 4, 5)}
ex.claim(ramp == {2: 5, 3: 13, 4: 5, 5: 3}, f'ramp {ramp} (19%, 50%, 19%, 12% against 20, 50, 20, 10)')
union = {}
for c in ('equations', 'functions', 'quadratics'):
    with open(os.path.join(COURSES, c, 'course.json'), encoding='utf8') as f:
        union.update(json.load(f)['skills'])
ex.claim(doc['skills'] == union, 'skills map equals the union of the three course.json maps')
used = {s for it in doc['items'] for s in it['skills']}
ex.claim(used == set(union), 'every skill is tested by at least one item')
rub = sum(r['points'] for r in IT['e-spread-model']['rubric'])
ex.claim(rub == 10, f'longform rubric sums to {rub}')
ex.claim(not any('versions' in doc or 'draw' in doc or 'parts' in it for it in doc['items']), 'one paper: no versions, draw pools or parts')

# ---------------------------------------------------------------- [0] e-expand-two: 3(2x - 5) - 2(x - 4)
src0 = lambda x: 3 * (2 * x - 5) - 2 * (x - 4)  # noqa: E731
same_expr(W('e-expand-two')['answer'], src0, 'x', 'e-expand-two key 4x-7 equals 3(2x-5)-2(x-4)')
for a in W('e-expand-two')['accept']:
    same_expr(a, src0, 'x', f'e-expand-two accept {a} equals the source')
same_expr(W('e-expand-two')['wrong'][0]['tex'], lambda x: 6 * x - 15 - 2 * x - 8, 'x', 'e-expand-two minus-sign 4x-23 is -2 x -4 taken as -8')
ex.claim(src0(0) == -7 and 6 * 1 - 15 == -9, 'e-expand-two constants: 6x - 15 and -2x + 8 give -7')

# ---------------------------------------------------------------- [1] e-bracket-equation: 4(x - 3) = 2x + 9
x1 = F(9 + 12, 4 - 2)
key('e-bracket-equation', x1)
ex.claim(4 * (x1 - 3) == 2 * x1 + 9 and 4 * (x1 - 3) == 30 and x1 - 3 == F(15, 2), 'e-bracket-equation check: 4 x 7.5 = 30 = 21 + 9')
ex.claim([x / 2 for x in range(-100, 100) if 4 * (x / 2 - 3) == 2 * (x / 2) + 9] == [10.5], 'e-bracket-equation second route: halves scan finds only 10.5')
wrong('e-bracket-equation', 'bracket', F(9 + 3, 4 - 2), typed=6)           # 4x - 3 = 2x + 9
wrong('e-bracket-equation', 'moved-sign', F(9 - 12, 4 - 2), typed=-1.5)    # 2x = 9 - 12
ex.expect('exam', f'{P("e-bracket-equation")}.feedback.correct', 21)

# ---------------------------------------------------------------- [2] e-gradient
g2 = F(-5 - 7, 4 - (-2))
key('e-gradient', g2)
ex.claim(g2 == -2 and (7 - (-5)) / (-2 - 4) == -2, 'e-gradient second route: (7 - (-5))/(-2 - 4) = -2')
wrong('e-gradient', 'flipped', F(4 - (-2), -5 - 7), typed=-0.5)
wrong('e-gradient', 'sign', -g2, typed=2)
ex.expect('exam', f'{P("e-gradient")}.explain.text', -12)
ex.expect('exam', f'{P("e-gradient")}.feedback.correct', 12)

# ---------------------------------------------------------------- [3] e-evaluate
f3 = lambda x: 3 * x ** 2 - 2 * x  # noqa: E731
key('e-evaluate', f3(-2))
ex.claim(3 * 4 + 4 == 16, 'e-evaluate second route: 3 x 4 + 4 = 16')
wrong('e-evaluate', 'negative-square', 3 * (-4) - 2 * (-2), typed=-8)
wrong('e-evaluate', 'squared-3x', (3 * -2) ** 2 - 2 * (-2), typed=40)

# ---------------------------------------------------------------- [4] e-factorise
q4 = lambda x: x ** 2 - 4 * x - 21  # noqa: E731
same_expr(lambda x: (x - 7) * (x + 3), q4, 'x', 'e-factorise key (x-7)(x+3) expands to x^2-4x-21')
ex.claim(correct_ids('e-factorise') == ['a'], 'e-factorise key is option a')
same_expr(lambda x: (x + 7) * (x - 3), lambda x: x * x + 4 * x - 21, 'x', 'e-factorise b expands to x^2+4x-21 (its why)')
ex.claim(-21 * 1 == -21 and -21 + 1 == -20, 'e-factorise c: product -21, sum -20')
ex.claim((-7) * (-3) == 21, 'e-factorise d: constant +21')
ex.claim([(p, q) for p in range(-30, 31) for q in range(p, 31) if p * q == -21 and p + q == -4] == [(-7, 3)], 'e-factorise second route: the only pair is -7 and 3')

# ---------------------------------------------------------------- [5] e-clear-fractions
x5 = F(24 - 10, 5)
ex.claim((2 * x5 + 1) / 3 - (x5 - 2) / 4 == 2 and x5 == F(14, 5), 'e-clear-fractions x = 2.8 solves the start equation')
states = W('e-clear-fractions')['states']
lin = {'s0': lambda x: (2 * x + 1) / 3 - (x - 2) / 4 - 2, 's1': lambda x: 4 * (2 * x + 1) - 3 * (x - 2) - 24,
       's2': lambda x: 8 * x + 4 - 3 * x + 6 - 24, 's3': lambda x: 5 * x + 10 - 24, 's4': lambda x: 5 * x - 14, 's5': lambda x: x - F(14, 5)}
ex.claim(all(lin[s](x5) == 0 and lin[s](x5 + 1) != 0 for s in lin), 'e-clear-fractions every state s0 to s5 has the one root 2.8')
ex.claim(states['s5']['tex'] == 'x = 2.8', 'e-clear-fractions target state reads x = 2.8')
ex.claim(F(24 + 2, 5) != x5, 'e-clear-fractions rejected expansion (-6) leads to 5x - 2 = 24, another root (5.2)')
ex.claim(2 * F(28, 10) + 1 == F(66, 10) and F(28, 10) - 2 == F(8, 10) and F(66, 30) - F(8, 40) == 2, 'e-clear-fractions check line: 6.6/3 - 0.8/4 = 2.2 - 0.2 = 2')
ex.claim(math.lcm(3, 4) == 12, 'e-clear-fractions 12 is the LCM of 3 and 4')

# ---------------------------------------------------------------- [6] e-whole-numbers
sol6 = [n for n in range(-100, 101) if -5 < 3 - 2 * n <= 9]
ids6 = {p['id']: p['x'] for p in IT['e-whole-numbers']['canvas']['state']['points']}
ex.claim(sol6 == [-3, -2, -1, 0, 1, 2, 3], f'e-whole-numbers brute force over -100..100: {sol6}')
ex.claim(sorted(ids6[i] for i in W('e-whole-numbers')['answer']) == sol6, 'e-whole-numbers answer ids are -3 to 3')
slip6 = sorted(ids6[i] for i in W('e-whole-numbers')['wrong'][0]['set'])
ex.claim(slip6 == [n for n in range(-5, 6) if -3 < n <= 4] and 4 in slip6 and -3 not in slip6, 'e-whole-numbers no-flip-ends set is -3 < n <= 4 (keeps 4, drops -3)')
ex.claim(3 - 2 * 4 == -5 and 3 - 2 * (-4) == 11, 'e-whole-numbers p4 gives -5, m4 gives 11')
ex.claim(min(ids6.values()) == -5 and max(ids6.values()) == 5, 'e-whole-numbers line runs -5 to 5 and holds both traps')
# GCSE: a set with negatives is "integers", not "whole numbers" (equations L3 review finding 4, fixed in the course)
ex.claim_text('exam', f'{P("e-whole-numbers")}', 'whole number', min(sol6) >= 0, 'e-whole-numbers says "whole number" for a set that holds -3, -2 and -1 (the course says integer)')

# ---------------------------------------------------------------- [7] e-option-prices: 4c + 3p = 36, 2c + 5p = 32
det = 4 * 5 - 3 * 2
c7, p7 = F(36 * 5 - 3 * 32, det), F(4 * 32 - 2 * 36, det)
key('e-option-prices', c7)
ex.claim(4 * c7 + 3 * p7 == 36 and 2 * c7 + 5 * p7 == 32, 'e-option-prices substitution back: both orders hold')
ex.claim([(c, p) for c in range(0, 3700) for p in range(0, 3700) if 4 * c + 3 * p == 3600 and 2 * c + 5 * p == 3200] == [(600, 400)], 'e-option-prices brute force over pence: £6 and £4')
wrong('e-option-prices', 'gave-put', p7, typed=4)
ex.claim(64 - 36 == 28 and 10 - 3 == 7 and 4 * 3 == 12 and 4 * c7 == 24, 'e-option-prices explain: 7p = 28, 4c + 12 = 36, 4c = 24')

# ---------------------------------------------------------------- [8] e-subject
rnd = random.Random(3)
ok8 = True
for _ in range(40):
    m, n, p, q = (rnd.uniform(1, 9) for _ in range(4))
    a = (m * p + n * q) / (m + n)
    if not math.isclose(ev(W('e-subject')['answer'], dict(a=a, m=m, n=n, p=p)), q, rel_tol=1e-9):
        ok8 = False
ex.claim(ok8, 'e-subject key returns q from a, m, n, p (40 random buys)')
for a8 in W('e-subject')['accept']:
    same_expr(a8, W('e-subject')['answer'], 'amnp', f'e-subject accept {a8} equals the key')
same_expr(W('e-subject')['wrong'][0]['tex'], lambda a, m, n, p: (a * (m + n) - m * p) / (m + n), 'amnp', 'e-subject divided-first is the key with m + n below')
same_expr(W('e-subject')['wrong'][1]['tex'], lambda a, m, n, p: (a * m + n - m * p) / n, 'amnp', 'e-subject dropped-bracket is a(m + n) read as am + n')
for w8 in W('e-subject')['wrong']:
    differ_expr(w8['tex'], W('e-subject')['answer'], 'amnp', f'e-subject wrong {w8["id"]} differs from the key')

# ---------------------------------------------------------------- [9] e-cubic-line: x^3 - 3x = 1
h = lambda x: x ** 3 - 3 * x - 1  # noqa: E731
grid = [i / 1000 for i in range(-3000, 3001)]
changes = sum(1 for a, b in zip(grid, grid[1:]) if h(a) * h(b) < 0)
trig = sorted(2 * math.cos(math.radians(20 + 120 * k)) for k in range(3))
ex.claim(changes == 3 and all(abs(h(r)) < 1e-12 for r in trig), f'e-cubic-line 3 sign changes on [-3, 3]; trigonometric roots {[round(r, 3) for r in trig]}')
ex.claim(correct_ids('e-cubic-line') == ['d'] and opt('e-cubic-line', 'd')['text'] == '3', 'e-cubic-line key is 3')
ex.claim([round(r, 1) for r in trig] == [-1.5, -0.3, 1.9], 'e-cubic-line explain: near -1.5, -0.3 and 1.9')
cub = lambda x: x ** 3 - 3 * x  # noqa: E731
ex.claim(max(cub(x) for x in grid if x < 0) == cub(-1) == 2 and min(cub(x) for x in grid if x > 0) == cub(1) == -2, 'e-cubic-line peak 2 at x = -1 and dip -2 at x = 1')
ex.claim(sum(1 for r in trig if r > 1) == 1 and sum(1 for r in trig if r < 1) == 2, 'e-cubic-line option b why: one crossing on the right, two further left')
ex.claim(-4 <= cub(-2.1) <= 4, f'e-cubic-line label point x = -2.1 is in frame (y = {cub(-2.1):.2f})')

# ---------------------------------------------------------------- [10] e-shifted-peak
f10 = lambda x: 5 - (x - 2) ** 2  # noqa: E731
g10 = lambda x: f10(x + 3) - 2  # noqa: E731
xs = [i / 100 for i in range(-600, 701)]
xm = max(xs, key=g10)
ex.claim(near(xm, -1) and near(g10(xm), 3), f'e-shifted-peak grid maximum of f(x + 3) - 2 at ({xm}, {g10(xm)})')
ex.claim(W('e-shifted-peak')['points'][0]['target'] == [-1, 3], 'e-shifted-peak target (-1, 3)')
cent = {w['id']: (sum(w['region']['x']) / 2, sum(w['region']['y']) / 2) for w in W('e-shifted-peak')['wrong']}
ex.claim(cent == {'right-shift': (5, 3), 'up': (-1, 7), 'both-wrong': (5, 7)}, f'e-shifted-peak slip regions centre on (5, 3), (-1, 7), (5, 7): {cent}')
ex.claim(max(xs, key=lambda x: f10(x - 3) - 2) == 5 and max(xs, key=lambda x: f10(x + 3) + 2) == -1, 'e-shifted-peak slips: f(x - 3) - 2 peaks at x = 5, f(x + 3) + 2 at x = -1')
ex.claim(f10(2) == 5 and max(xs, key=f10) == 2, 'e-shifted-peak prose: highest point (2, 5)')

# ---------------------------------------------------------------- [11] e-composite
fc = lambda x: 2 * x + 1  # noqa: E731
gc = lambda x: x * x - 3  # noqa: E731
same_expr(W('e-composite')['answer'], lambda x: gc(fc(x)), 'x', 'e-composite key equals g(f(x))')
for a11 in W('e-composite')['accept']:
    same_expr(a11, lambda x: gc(fc(x)), 'x', f'e-composite accept {a11} equals g(f(x))')
same_expr(W('e-composite')['wrong'][0]['tex'], lambda x: fc(gc(x)), 'x', 'e-composite wrong-order 2x^2-5 is f(g(x))')
same_expr(W('e-composite')['wrong'][1]['tex'], lambda x: (2 * x) ** 2 + 1 - 3, 'x', 'e-composite square-terms 4x^2-2 squares each term')
ex.claim(fc(1) == 3 and gc(3) == 6 and ev(W('e-composite')['answer'], {'x': 1}) == 6, 'e-composite check at x = 1: f(1) = 3, g(3) = 6')

# ---------------------------------------------------------------- [12] e-inverse
f12 = lambda x: (3 * x - 4) / 5  # noqa: E731
same_expr(lambda x: f12(ev(opt('e-inverse', 'a')['text'].strip('$').replace('\\dfrac', '\\frac'), {'x': x})), lambda x: x, 'x', 'e-inverse key a undoes f')
ex.claim(correct_ids('e-inverse') == ['a'], 'e-inverse key is option a')
same_expr(opt('e-inverse', 'b')['text'].strip('$').replace('\\dfrac', '\\frac'), lambda x: 1 / f12(x), 'x', 'e-inverse b is 1/f(x)')
for o in 'cd':
    differ_expr(lambda x: f12(ev(opt('e-inverse', o)['text'].strip('$').replace('\\dfrac', '\\frac'), {'x': x})), lambda x: x, 'x', f'e-inverse option {o} is not the inverse')
same_order = lambda x: 5 * (x / 3 + 4)  # undo x3, -4, /5 in the same order: /3, +4, x5  # noqa: E731
c12 = opt('e-inverse', 'c')['text'].strip('$').replace('\\dfrac', '\\frac')
ex.claim_text('exam', f'{P("e-inverse")}.widget.options[2].why', 'You undid the steps in the same order',
              all(math.isclose(ev(c12, {'x': x}), same_order(x)) for x in (0.5, 1.7, 2.9)),
              'e-inverse option c why: undoing in the same order gives 5x/3 + 20, not 5x/3 + 4 (c divides by 3 before adding 4)')
ex.claim(f12(2) == 0.4 and (5 * 0.4 + 4) / 3 == 2, 'e-inverse check: f(2) = 2/5 and the inverse gives 6/3 = 2')

# ---------------------------------------------------------------- [13] e-two-roots: 2x^2 + 5x - 12 = 0
d13, r13 = quad_roots(2, 5, -12)
ex.claim(d13 == 121 and [round(r, 9) for r in r13] == [-4, 1.5], f'e-two-roots formula roots {r13}')
same_expr(lambda x: (2 * x - 3) * (x + 4), lambda x: 2 * x * x + 5 * x - 12, 'x', 'e-two-roots (2x - 3)(x + 4) expands back')
ex.claim(correct_ids('e-two-roots') == ['a', 'b'], 'e-two-roots keys a (3/2) and b (-4)')
ex.claim(2 * 3 == 6 and 8 - 3 == 5 and 2 * -12 == -24 and 8 * -3 == -24, 'e-two-roots split: 8x - 3x, 8 x -3 = 2 x -12')

# ---------------------------------------------------------------- [14] e-complete-table: x^2 + 10x + 7
p14, q14 = F(10, 2), 7 - F(10, 2) ** 2
ex.claim(W('e-complete-table')['rows'][0][0]['answer'] == p14 and W('e-complete-table')['rows'][0][1]['answer'] == q14, f'e-complete-table p = {p14}, q = {q14}')
same_expr(lambda x: (x + 5) ** 2 - 18, lambda x: x * x + 10 * x + 7, 'x', 'e-complete-table (x + 5)^2 - 18 expands back')
ex.claim(min(i / 100 for i in range(-1000, 1001)) and min((i / 100) ** 2 + 10 * i / 100 + 7 for i in range(-1000, 1001)) == -18, 'e-complete-table second route: grid minimum -18 at x = -5')

# ---------------------------------------------------------------- [15] e-vertex: y = x^2 + 2x - 8
y15 = lambda x: x * x + 2 * x - 8  # noqa: E731
xs15 = [i / 100 for i in range(-500, 401)]
xm15 = min(xs15, key=y15)
ex.claim(near(xm15, -1) and near(y15(xm15), -9), f'e-vertex grid minimum ({xm15}, {y15(xm15)})')
ex.claim(W('e-vertex')['points'][0]['target'] == [-1.0, -9.0], 'e-vertex target (-1, -9)')
cent15 = {w['id']: (sum(w['region']['x']) / 2, sum(w['region']['y']) / 2) for w in W('e-vertex')['wrong']}
ex.claim(cent15 == {'sign': (1, -9), 'intercept': (0, -8), 'root': (2, 0)}, f'e-vertex regions centre on (1, -9), (0, -8), (2, 0): {cent15}')
ex.claim(quad_roots(1, 2, -8)[1] == [-4, 2] and (2 + -4) / 2 == -1 and y15(0) == -8, 'e-vertex roots 2 and -4, halfway -1; y-intercept -8')
# the other root (-4, 0) is also on the canvas but has no slip region
ex.claim(all(not (w['region']['x'][0] <= -4 <= w['region']['x'][1]) for w in W('e-vertex')['wrong']) and -5 <= -4, 'e-vertex (note) the root (-4, 0) is in frame with no slip region')

# ---------------------------------------------------------------- [16] e-one-root: 2x^2 - 8x + k = 0
k16 = F(64, 8)
key('e-one-root', k16)
ex.claim([k for k in range(-50, 51) if (-8) ** 2 - 4 * 2 * k == 0] == [8], 'e-one-root integer scan of the discriminant')
same_expr(lambda x: 2 * x * x - 8 * x + 8, lambda x: 2 * (x - 2) ** 2, 'x', 'e-one-root 2x^2 - 8x + 8 = 2(x - 2)^2')
wrong('e-one-root', 'forgot-a', F(64, 4), typed=16)
wrong('e-one-root', 'b-squared', 64, typed=64)

# ---------------------------------------------------------------- [17] e-floor-area: w(w + 4) = 96
d17, r17 = quad_roots(1, 4, -96)
key('e-floor-area', r17[1])
ex.claim([w for w in range(1, 100) if w * (w + 4) == 96] == [8] and r17 == [-12, 8], 'e-floor-area integer scan and formula: 8 (and -12)')
wrong('e-floor-area', 'negative', r17[0], typed=-12)
wrong('e-floor-area', 'square-root', math.sqrt(96), typed=9.80)
ex.expect('exam', f'{P("e-floor-area")}.explain.text', 12)
ex.claim(8 + 4 == 12 and 8 * 12 == 96, 'e-floor-area length 12 m, area 96')

# ---------------------------------------------------------------- [18] e-perpendicular
m18 = F(-1, 2)
c18 = 1 - m18 * 4
ex.claim(c18 == 3 and m18 * 2 == -1, 'e-perpendicular gradient -1/2 (product with 2 is -1), c = 3')
same_expr(W('e-perpendicular')['answer'], lambda x: -x / 2 + 3, 'x', 'e-perpendicular key equals -x/2 + 3')
for a18 in W('e-perpendicular')['accept']:
    same_expr(a18, lambda x: -x / 2 + 3, 'x', f'e-perpendicular accept {a18} equals the key')
ex.claim(ev(W('e-perpendicular')['answer'], {'x': 4}) == 1, 'e-perpendicular key passes through (4, 1)')
same_expr(W('e-perpendicular')['wrong'][0]['tex'], lambda x: -2 * x + (1 + 8), 'x', 'e-perpendicular negative-only -2x + 9 goes through (4, 1)')
same_expr(W('e-perpendicular')['wrong'][1]['tex'], lambda x: x / 2 + (1 - 2), 'x', 'e-perpendicular reciprocal-only x/2 - 1 goes through (4, 1)')

# ---------------------------------------------------------------- [19] e-formula: 2x^2 - 3x - 7 = 0
d19, r19 = quad_roots(2, -3, -7)
key('e-formula', r19[1], t=1e-9)
x = 2.0
for _ in range(30):
    x -= (2 * x * x - 3 * x - 7) / (4 * x - 3)
ex.claim(near(x, r19[1], 1e-12) and d19 == 65, f'e-formula Newton {x:.6f} agrees; discriminant 65')
inband('e-formula', 2.77)
wrong('e-formula', 'no-2a', (3 + math.sqrt(65)) / 2, typed=5.53)
wrong('e-formula', 'sign-b', (-3 + math.sqrt(65)) / 4, typed=1.27)
ex.claim(round(math.sqrt(65), 3) == 8.062 and round(r19[0], 2) == -1.27 and 9 + 56 == 65, 'e-formula explain: sqrt 65 = 8.062, other root -1.27')

# ---------------------------------------------------------------- [20] e-quad-inequality: x^2 + 2x - 15 < 0
neg = [i / 4 for i in range(-80, 81) if (i / 4) ** 2 + 2 * (i / 4) - 15 < 0]
ex.claim(min(neg) == -4.75 and max(neg) == 2.75 and len(neg) == 31, 'e-quad-inequality quarter scan: negative exactly on -5 < x < 3')
ex.claim(correct_ids('e-quad-inequality') == ['a'] and quad_roots(1, 2, -15)[1] == [-5, 3], 'e-quad-inequality key a, roots -5 and 3')
ex.claim(0 + 0 - 15 < 0, 'e-quad-inequality check x = 0 gives -15')

# ---------------------------------------------------------------- [21] e-fg-equation: f(x) = x^2 + 1, g(x) = 3x - 2
f21 = lambda x: x * x + 1  # noqa: E731
g21 = lambda x: 3 * x - 2  # noqa: E731
roots21 = [F(2), F(-2, 3)]
ex.claim(all(f21(g21(r)) == 17 for r in roots21), 'e-fg-equation f(g(2)) = f(g(-2/3)) = 17')
ex.claim(sorted(n / 3 for n in range(-60, 61) if f21(g21(n / 3)) == 17) == [-2 / 3, 2], 'e-fg-equation thirds scan finds only 2 and -2/3')
ex.claim(correct_ids('e-fg-equation') == ['a', 'b'], 'e-fg-equation keys a and b')
ex.claim(math.isclose(g21(f21(4 / math.sqrt(3))), 17) and not math.isclose(f21(g21(4 / math.sqrt(3))), 17), 'e-fg-equation c: 4/sqrt 3 solves g(f(x)) = 17 only')
ex.claim((-4 - 2) / 3 == -2 and (16 + 2) / 3 == 6, 'e-fg-equation d: 3x = -6 gives -2; e: 3x - 2 = 16 gives 6')

# ---------------------------------------------------------------- [22] e-odd-squares
ex.claim(all((2 * n + 3) ** 2 - (2 * n + 1) ** 2 == 8 * (n + 1) for n in range(-50, 51)), 'e-odd-squares identity holds for every integer n from -50 to 50')
ex.claim(all(((2 * n + 3) ** 2 - (2 * n + 1) ** 2) % 8 == 0 for n in range(-50, 51)), 'e-odd-squares always a multiple of 8')
ex.claim(7 ** 2 - 5 ** 2 == 24 == 8 * (2 + 1), 'e-odd-squares check 7^2 - 5^2 = 24 (n = 2)')
ex.claim_text('exam', f'{P("e-odd-squares")}.widget.lines[0].text', 'whole number', False,
              'e-odd-squares "for a whole number n": GCSE writes "for an integer n" (the course now says integer)')

# ---------------------------------------------------------------- [23] e-tangent-line
k23 = 1 - F(25, 4)
x23 = F(5, 2)
y23 = 2 * x23 + k23
ex.claim([W('e-tangent-line')['rows'][0][j]['answer'] for j in range(3)] == [float(k23), float(x23), float(y23)], f'e-tangent-line k = {k23}, x = {x23}, y = {y23}')
ex.claim(x23 ** 2 - 3 * x23 + 1 == y23 and 25 - 4 * (1 - k23) == 0, 'e-tangent-line point on both graphs; discriminant zero')
ks = [F(i, 4) for i in range(-40, 41) if 25 - 4 * (1 - F(i, 4)) == 0]
ex.claim(ks == [F(-21, 4)], 'e-tangent-line quarter scan of k: only -5.25 gives one meeting point')
ex.claim(F(25, 4) - F(15, 2) + 1 == F(-1, 4), 'e-tangent-line byKey r0c2: 6.25 - 7.5 + 1 = -0.25')

# ---------------------------------------------------------------- [24] e-lattice-region
pts = [(x, y) for x in range(-20, 21) for y in range(-20, 41) if x * x <= y <= x + 2]
key('e-lattice-region', len(pts))
ex.claim(len(pts) == 8, f'e-lattice-region brute force: {pts}')
cols = [sum(1 for p in pts if p[0] == c) for c in (-1, 0, 1, 2)]
ex.claim(cols == [1, 3, 3, 1], 'e-lattice-region columns 1, 3, 3, 1')
wrong('e-lattice-region', 'strict', sum(1 for x in range(-20, 21) for y in range(-20, 41) if x * x < y < x + 2), typed=2)
wrong('e-lattice-region', 'curve-only', sum(1 for p in pts if p[1] == p[0] ** 2), typed=4)
shown = sorted((p['x'], p['y']) for p in IT['e-lattice-region']['explain']['canvas']['points'])
ex.claim(shown == sorted(pts), 'e-lattice-region explain marks exactly the 8 points')
ex.claim(quad_roots(1, -1, -2)[1] == [-1, 2], 'e-lattice-region graphs meet at x = -1 and 2')
ex.claim_text('exam', f'{P("e-lattice-region")}', 'whole-number', min(p[0] for p in pts) >= 0,
              'e-lattice-region "whole-number coordinates" for a set that holds x = -1 (GCSE: integer coordinates)')

# ---------------------------------------------------------------- [25] e-spread-model: P = 60s - 4s^2 - 200
Pm = lambda s: 60 * s - 4 * s * s - 200  # noqa: E731
same_expr(lambda s: 25 - 4 * (s - 7.5) ** 2, Pm, 's', 'e-spread-model P = 25 - 4(s - 7.5)^2')
same_expr(lambda s: -4 * (s * s - 15 * s) - 200, Pm, 's', 'e-spread-model P = -4(s^2 - 15s) - 200')
same_expr(lambda s: (s - 7.5) ** 2 - 56.25, lambda s: s * s - 15 * s, 's', 'e-spread-model s^2 - 15s = (s - 7.5)^2 - 56.25')
ss = [i / 100 for i in range(0, 2001)]
sm = max(ss, key=Pm)
ex.claim(near(sm, 7.5) and near(Pm(sm), 25), f'e-spread-model grid maximum at {sm}p, £{Pm(sm)}')
pos = [s for s in ss if Pm(s) > 0]
ex.claim(near(min(pos), 5.01) and near(max(pos), 9.99) and Pm(5) == 0 and Pm(10) == 0, 'e-spread-model profit only for 5 < s < 10; £0 at 5p and 10p')
ex.claim(4 * 56.25 == 225 and 225 - 200 == 25 and 25 / 4 == 6.25 and math.sqrt(6.25) == 2.5, 'e-spread-model model numbers 225, 25, 6.25, 2.5')
ex.claim(Pm(0) == -200, 'e-spread-model at zero spread the model loses £200 (the "fixed costs" of part 4 are not named in the prompt)')

# ---------------------------------------------------------------- the review's proposed replacements (pass whatever the content says)
# finding 1: -7 <= 5 - 3n < 11
s1 = [n for n in range(-100, 101) if -7 <= 5 - 3 * n < 11]
ex.claim(s1 == [-1, 0, 1, 2, 3, 4] and [n for n in range(-5, 6) if -2 <= n < 4] == [-2, -1, 0, 1, 2, 3], 'proposal 1: integers -1 to 4 (six); no-flip-ends slip -2 to 3')
ex.claim(5 - 3 * -2 == 11 and 5 - 3 * 5 == -10 and 5 - 3 * 4 == -7 and -7 - 5 == -12 and 11 - 5 == 6, 'proposal 1: n = -2 gives 11, n = 5 gives -10, n = 4 gives -7; -12 <= -3n < 6')
# finding 2: 3x^2 + 5x - 12 = (3x - 4)(x + 3)
same_expr(lambda x: (3 * x - 4) * (x + 3), lambda x: 3 * x * x + 5 * x - 12, 'x', 'proposal 2: (3x - 4)(x + 3) = 3x^2 + 5x - 12')
ex.claim([round(r, 9) for r in quad_roots(3, 5, -12)[1]] == [-3, round(4 / 3, 9)] and 9 - 4 == 5 and 3 * -12 == 9 * -4, 'proposal 2: roots 4/3 and -3; split 9x - 4x')
# finding 3: x^2 + 3x - 18 < 0
neg3 = [i / 4 for i in range(-80, 81) if (i / 4) ** 2 + 3 * (i / 4) - 18 < 0]
ex.claim(min(neg3) == -5.75 and max(neg3) == 2.75 and quad_roots(1, 3, -18)[1] == [-6, 3], 'proposal 3: x^2 + 3x - 18 < 0 exactly on -6 < x < 3')
# finding 4: x^2 <= y <= 3 - 2x
pts4 = [(x, y) for x in range(-20, 21) for y in range(-20, 41) if x * x <= y <= 3 - 2 * x]
ex.claim(len(pts4) == 15 and [sum(1 for p in pts4 if p[0] == c) for c in (-3, -2, -1, 0, 1)] == [1, 4, 5, 4, 1], 'proposal 4: 15 points, columns 1, 4, 5, 4, 1')
ex.claim(sum(1 for x in range(-20, 21) for y in range(-20, 41) if x * x < y < 3 - 2 * x) == 7 and sum(1 for p in pts4 if p[1] == p[0] ** 2) == 5, 'proposal 4: strict 7, on the curve 5')
ex.claim(quad_roots(1, 2, -3)[1] == [-3, 1] and 3 - 2 * -3 == 9 and 3 - 2 * 1 == 1, 'proposal 4: graphs meet at (-3, 9) and (1, 1)')
# finding 5: f(x) = x^2 + 2, g(x) = 2x - 5, fg(x) = 27
f5, g5 = (lambda x: x * x + 2), (lambda x: 2 * x - 5)
ex.claim(f5(g5(5)) == 27 and f5(g5(0)) == 27 and sorted(n / 2 for n in range(-60, 61) if f5(g5(n / 2)) == 27) == [0, 5], 'proposal 5: fg(x) = 27 only at x = 5 and x = 0')
ex.claim(math.isclose(g5(f5(math.sqrt(14))), 27) and not math.isclose(f5(g5(math.sqrt(14))), 27) and (-5 - 5) / 2 == -5 and (25 + 5) / 2 == 15, 'proposal 5: sqrt 14 solves gf(x) = 27 only; slips -5 and 15')
# finding 6: line through (-1, 2) and (1, 8); perpendicular through (6, 1)
m6 = F(8 - 2, 1 - (-1))
c6 = 8 - m6 * 1
ex.claim(m6 == 3 and c6 == 5 and 2 == m6 * -1 + c6, 'proposal 6: the given line is y = 3x + 5')
ex.claim(1 - F(-1, 3) * 6 == 3 and 1 - (-3) * 6 == 19 and 1 - F(1, 3) * 6 == -1 and F(-1, 3) * 3 == -1, 'proposal 6: y = -x/3 + 3; slips -3x + 19 and x/3 - 1')
# finding 7: f(x) = 4 - (x - 3)^2, the root (1, 0) under f(x + 3) - 2
f7 = lambda x: 4 - (x - 3) ** 2  # noqa: E731
ex.claim(f7(1) == 0 and f7(5) == 0 and f7(-2 + 3) - 2 == -2 and f7(4 - 3) - 2 == -2 and f7(-2 + 3) + 2 == 2, 'proposal 7: (1, 0) goes to (-2, -2); slips (4, -2), (-2, 2), (4, 2)')
ex.claim(-4 <= f7(0.4) and f7(5.6) >= -4, 'proposal 7: the drawn domain 0.4 to 5.6 stays inside y from -4')
# finding 14: inputs 1, 3, 4, 7 give -4, 2, 5, 14
rows14 = [(1, -4), (3, 2), (4, 5), (7, 14)]
ex.claim(all(3 * x - 7 == y for x, y in rows14) and [6 * x - 10 == y for x, y in rows14] == [True, False, False, False], 'proposal 14: 3x - 7 fits every row; 6x - 10 fits only the first')
# finding 8: x^2 - 16x + 9 = (x - 8)^2 - 55, with slips p = 8, q = 73 and q = 55
same_expr(lambda x: (x - 8) ** 2 - 55, lambda x: x * x - 16 * x + 9, 'x', 'proposal 8: x^2 - 16x + 9 = (x - 8)^2 - 55')
ex.claim(9 - 64 == -55 and 9 + 64 == 73 and 64 - 9 == 55 and min(x * x - 16 * x + 9 for x in range(-50, 51)) == -55, 'proposal 8: q = 9 - 64 = -55 (grid minimum); slips 73 and 55')
# finding 18: tangent sign slip
ex.claim(25 - 4 * (1 + F(21, 4)) == 0, 'proposal 18: k sign slip 5.25 solves 25 - 4(1 + k) = 0')
# finding 13: paces
paces = [60, 60, 45, 45, 60, 120, 120, 120, 120, 75, 90, 120, 90, 120, 90, 120, 75, 120, 180, 150, 150, 180, 180, 300, 300, 720]
ex.claim(len(paces) == len(doc['items']) and sum(paces) == 3810, f'proposal 13: paces sum {sum(paces)} s = {sum(paces) / 60:.1f} min; with the new item at 90 s, {(sum(paces) + 90) / 60:.0f} min')

# ---------------------------------------------------------------- wrong values against the answer bands (rule 581)
ex.check_wrongs()
ex.report()
