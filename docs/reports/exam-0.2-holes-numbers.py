"""topic-0.2, quadratics level 4 items (Option B, skill quad-rational): every new key computed twice, every wrong value checked.

Run: <scratchpad>/venv/bin/python docs/reports/exam-0.2-holes-numbers.py   (exit 0 when all pass)
Route 1 is the working the item prints; route 2 is independent (exact Fractions, brute force over a grid, polynomial
multiplication, evaluation at many points). The script then reads app/content/exams/topic-0.2.json.
"""
import json, math, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import _numbers  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', 'app', 'content', 'exams', 'topic-0.2.json')
doc = json.load(open(EXAM, encoding='utf8'))
items = {i['id']: i for i in doc['items']}
fails, n = [], [0]


def check(ok, label):
    n[0] += 1
    print(('ok  ' if ok else 'BAD ') + label)
    if not ok:
        fails.append(label)


def band(t):
    return t.get('abs', 0) if isinstance(t, dict) else t


def numeric(where, w, fb, explain, key, wrongs):
    a, t = w['answer'], band(w['tol'])
    check(abs(a - key) <= max(t, 1e-9), f'{where} key {a} = computed {key}')
    got = {x['id']: x for x in w.get('wrong', [])}
    check(set(got) == set(wrongs), f'{where} wrong ids {sorted(got)}')
    for k, v in wrongs.items():
        x = got[k]
        check(abs(x['value'] - v) <= band(x['tol']) + 1e-9, f'{where} wrong {k} {x["value"]} = slip {v}')
        check(abs(x['value'] - a) > t + band(x['tol']), f'{where} wrong {k} outside the key band')
        check(k in fb['byKey'], f'{where} wrong {k} has a byKey line')
    check(any(abs(x - a) <= max(t, 1e-9) for x in _numbers(explain)), f'{where} explanation states the key')


# e-surd-difference: sqrt75 - sqrt12 = 3 sqrt3
def simplest(m):
    """largest square factor: m = s^2 * r"""
    s = max(k for k in range(1, math.isqrt(m) + 1) if m % (k * k) == 0)
    return s, m // (s * s)
(s1, r1), (s2, r2) = simplest(75), simplest(12)
check((s1, r1, s2, r2) == (5, 3, 2, 3) and s1 - s2 == 3, 'e-surd-difference 5 root 3 - 2 root 3 = 3 root 3')
check(abs(math.sqrt(75) - math.sqrt(12) - 3 * math.sqrt(3)) < 1e-12, 'e-surd-difference numerically 3 root 3')
opts = {o['id']: o for o in items['e-surd-difference']['widget']['options']}
check(opts['a'].get('correct') and opts['a']['text'] == '$3\\sqrt{3}$', 'e-surd-difference key option')
check(abs(math.sqrt(75 - 12) - math.sqrt(63)) < 1e-12 and abs(math.sqrt(63) - 3 * math.sqrt(3)) > 0.1, 'slip root of the difference, sqrt 63, differs')
check(s1 + s2 == 7 and 25 - 4 == 21, 'slips: sum 7 root 3; square factors not rooted 25 - 4 = 21')
check(abs(math.sqrt(75) + math.sqrt(12) - 7 * math.sqrt(3)) < 1e-12, '7 root 3 is the sum')

# e-two-desks: 1/x + 1/(x+3) = 1/2
a_, b_, c_ = 1, -1, -6                     # x^2 - x - 6 = 0 from 2(x+3) + 2x = x(x+3)
disc = b_ * b_ - 4 * a_ * c_
r = sorted([(-b_ - math.isqrt(disc)) / 2, (-b_ + math.isqrt(disc)) / 2])
check(disc == 25 and r == [-2, 3], f'e-two-desks formula roots {r}')
grid = [F(k, 10) for k in range(-100, 101) if k not in (0, -30)]
sols = [x for x in grid if F(1) / x + F(1) / (x + 3) == F(1, 2)]
check(sols == [-2, 3], f'e-two-desks grid search over tenths {sols}')
check(all(2 * (x + 3) + 2 * x == x * (x + 3) for x in (F(3), F(-2))), 'e-two-desks cleared equation holds at both roots')
slip = [x for x in grid if 2 * x + 3 != 0 and F(2) / (2 * x + 3) == F(1, 2)]
check(slip == [F(1, 2)], 'e-two-desks tops-and-bottoms slip gives 0.5')
it = items['e-two-desks']
numeric('e-two-desks', it['widget'], it['feedback'], it['explain']['text'], 3, {'kept-negative': -2, 'tops-and-bottoms': 0.5, 'desk-b': 6})

# e-diameter-ends: centre given, radius from the distance rule, against half the diameter and against every lattice point
P, Q, Cc = (-4, -6), (6, 18), (1, 6)
r1 = math.sqrt((P[0] - Cc[0]) ** 2 + (P[1] - Cc[1]) ** 2)           # centre to an end: 5 across, 12 down
r2 = math.dist(P, Q) / 2                                             # half the distance between the ends
check(r1 == r2 == 13 and 5 ** 2 + 12 ** 2 == 13 ** 2, f'e-diameter-ends radius {r1} and {r2}')
check(Cc == ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2), 'e-diameter-ends the given centre is the midpoint of the ends')
check(all((x - 1) ** 2 + (y - 6) ** 2 == 169 for x, y in (P, Q)), 'e-diameter-ends both ends on (x-1)^2 + (y-6)^2 = 169')
# the angle in a semicircle: a third point on the circle sees AB at a right angle
R = (13 + 1, 6)   # (14-1)^2 + 0 = 169
check((R[0] - 1) ** 2 + (R[1] - 6) ** 2 == 169 and (P[0] - R[0]) * (Q[0] - R[0]) + (P[1] - R[1]) * (Q[1] - R[1]) == (-18) * (-8) + (-12) * 12 == 0,
      'e-diameter-ends second route: (14, 6) on the circle sees the diameter at a right angle')
# expanded form: x^2 + y^2 - 2x - 12y + 1 + 36 - 169 = 0, checked at every lattice point near the circle
check(1 + 36 - 169 == -132, 'e-diameter-ends expanded constant -132')
ok = all(((x - 1) ** 2 + (y - 6) ** 2 == 169) == (x * x + y * y - 2 * x - 12 * y - 132 == 0) for x in range(-20, 22) for y in range(-20, 32))
on = [(x, y) for x in range(-20, 22) for y in range(-20, 32) if (x - 1) ** 2 + (y - 6) ** 2 == 169]
check(ok and P in on and Q in on, f'e-diameter-ends accept form agrees on a grid ({len(on)} lattice points on the circle)')
w = items['e-diameter-ends']['widget']
check(w['answer'] == '(x-1)^2+(y-6)^2=169' and w['accept'] == ['x^2+y^2-2x-12y-132=0'], 'e-diameter-ends key and accept')
slips = {'signs': '(x+1)^2+(y+6)^2=169', 'radius-not-squared': '(x-1)^2+(y-6)^2=13', 'full-diameter': '(x-1)^2+(y-6)^2=676'}
check({x['id']: x['tex'] for x in w['wrong']} == slips, 'e-diameter-ends wrong entries')
check(13 ** 2 == 169 and 26 ** 2 == 676 and math.dist(P, Q) == 26 and (-Cc[0], -Cc[1]) == (-1, -6), 'e-diameter-ends slips 169, 13, 676, signs')
for k in slips:
    check(k in items['e-diameter-ends']['feedback']['byKey'], f'e-diameter-ends wrong {k} has a line')
check('midpoint' not in json.dumps(items['e-diameter-ends']) and 'halfway' not in items['e-diameter-ends']['prose'], 'e-diameter-ends needs no midpoint')


# e-cubic-remainder
def p(x, k):
    return x ** 3 + k * x ** 2 - 4 * x - 12
k1 = -12 - (1 - 4 - 12)                                    # p(1) = k - 15 = -12
# route 2: long division by (x - 1) with k unknown, scanned over integers
def remainder(coeffs, a):
    acc = 0
    for c in coeffs:
        acc = acc * a + c
    return acc
k2 = [k for k in range(-50, 51) if remainder([1, k, -4, -12], 1) == -12]
check(k1 == 3 and k2 == [3], f'e-cubic-remainder k = 3 both routes ({k2})')
check([k for k in range(-50, 51) if p(1, k) == 0] == [15] and [k for k in range(-50, 51) if p(-1, k) == -12] == [-3], 'e-cubic-remainder slips 15 and -3')
it = items['e-cubic-remainder']
part = it['parts'][0]
numeric('e-cubic-remainder p1', part['widget'], part['feedback'], part['explain']['text'], 3, {'set-to-zero': 15, 'wrong-sign': -3})
# factorised form: expand (x-2)(x+2)(x+3) and compare coefficients; roots by integer search
def mul(A, B):
    out = [0] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            out[i + j] += a * b
    return out
check(mul(mul([1, -2], [1, 2]), [1, 3]) == [1, 3, -4, -12], 'e-cubic-remainder (x-2)(x+2)(x+3) expands to the cubic')
check([x for x in range(-12, 13) if p(x, 3) == 0] == [-3, -2, 2], 'e-cubic-remainder integer roots -3, -2, 2')
check(p(3, 3) == 30 and p(-3, 3) == 0, 'e-cubic-remainder p(3) = 30 (signs slip line), p(-3) = 0')
check(it['parts'][1]['widget']['answer'] == '(x-2)(x+2)(x+3)', 'e-cubic-remainder part 2 key')

# exam shape
cnt = {d: sum(1 for i in doc['items'] if i['difficulty'] == d) for d in (2, 3, 4, 5)}
N = len(doc['items'])
for d, s in {2: .2, 3: .5, 4: .2, 5: .1}.items():
    check(abs(cnt[d] / N - s) <= 0.1 + 1e-9, f'ramp d{d} {cnt[d]}/{N}')
check(N <= 30 and 'e-one-root' not in items, f'{N} items, e-one-root replaced')
used = {s for i in doc['items'] for s in i.get('skills', [])}
check(set(doc['skills']) <= used, 'every exam skill covered')
check(sum('quad-solve' in i.get('skills', []) for i in doc['items']) >= 4, 'quad-solve still examined by several items')
print(f'{n[0] - len(fails)} of {n[0]} checks passed')
sys.exit(1 if fails else 0)
