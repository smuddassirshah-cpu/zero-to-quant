"""Second reader's number script for app/content/exams/topic-0.3.json (review-exam-0.3.md).

Recomputes every graded key and every wrong[] value, and the numbers in prose, feedback and explanations, each by
two routes: a closed form, and brute force (enumeration, a loop or a recursion) or exact fractions. Counts are
enumerated in full (tickets, seatings, tech picks, account codes); sums are added term by term; the cosine rule is
checked from the canvas coordinates; trigonometric solutions are found by scanning every whole degree.
A check that fails because the content is wrong stays failing; each such check is a finding in the review.
Standard library only. Run: python3 docs/reviews/exam-0.3-scripts/numbers.py
"""
import os
import sys

# This file is named numbers.py, which shadows the standard library's `numbers` (fractions imports it).
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or os.getcwd()) != HERE]

import itertools  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
from fractions import Fraction as F  # noqa: E402

sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-0.3.json')
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


def near(a, b, t):
    return abs(a - b) <= t


def key(iid, value, t=None):
    """The graded answer equals the recomputed value, within a tenth of its tolerance (or t)."""
    w = IT[iid]['widget']
    tol = w.get('tol', {}).get('abs', 0)
    t = t if t is not None else max(tol / 10, 1e-9)
    ok = near(w['answer'], value, t)
    ex._rec(ok, f'{iid} answer {w["answer"]!r} = {value:.8g}', '' if ok else 'recomputed value differs')


def inband(iid, typed, label='typed answer', want=True):
    """A value typed at the precision asked lies inside (want=True) or outside the answer's tolerance."""
    w = IT[iid]['widget']
    ok = (abs(typed - w['answer']) <= w['tol']['abs'] + 1e-9) == want
    ex._rec(ok, f'{iid} {label} {typed!r} graded {"right" if want else "wrong"}', '' if ok else 'grading differs from the claim')


def wrong(iid, wid, value, t=None):
    ws = [x for x in IT[iid]['widget'].get('wrong', []) if x['id'] == wid]
    if not ws:
        return ex._rec(False, f'{iid} wrong "{wid}" exists', 'no such wrong id')
    v = ws[0]
    tt = t if t is not None else max(v.get('tol', {}).get('abs', 1e-9), 1e-9)
    ok = near(v['value'], value, tt)
    ex._rec(ok, f'{iid} wrong "{wid}" {v["value"]!r} = {value:.8g}', '' if ok else 'recomputed slip differs')


def correct_ids(iid):
    return sorted(o['id'] for o in IT[iid]['widget']['options'] if o.get('correct'))


def opt(iid, oid):
    return [o for o in IT[iid]['widget']['options'] if o['id'] == oid][0]


def X(iid, path, value, fmt=None):
    ex.expect('exam', f'{P(iid)}.{path}', value, fmt=fmt)


# ---------------------------------------------------------------- metadata, shape, coverage
ex.claim(doc['pass'] == 0.7, 'pass 0.7 as section 5 asks')
ex.claim(20 <= len(doc['items']) <= 30, f'{len(doc["items"])} items, inside 20 to 30')
ramp = {d: sum(1 for it in doc['items'] if it['difficulty'] == d) for d in (2, 3, 4, 5)}
ex.claim(ramp == {2: 5, 3: 13, 4: 5, 5: 2}, f'ramp {ramp} (20%, 52%, 20%, 8% against 20, 50, 20, 10)')
union = {}
for c in ('exp-log', 'series', 'trig', 'counting'):
    with open(os.path.join(COURSES, c, 'course.json'), encoding='utf8') as f:
        union.update(json.load(f)['skills'])
ex.claim(doc['skills'] == union, 'skills map equals the union of the four course.json maps (20 ids)')
used = {s for it in doc['items'] for s in it['skills']}
ex.claim(used == set(union), 'every skill is tested by at least one item')
# Timing (finding 22): the reader's paces (review, Coverage and time) sum to 3,300 s, 55 minutes; topic-0.6 (Stage 0,
# 24 items) paces to 52.5 minutes under a 60-minute clock. 90 minutes is 1.6 times the paced need.
READER_PACE = 3300
ex.claim(doc['minutes'] * 60 <= 1.25 * READER_PACE,
         f'minutes {doc["minutes"]} within 1.25 times the paced need of {READER_PACE / 60:.0f} min (finding 22)')

# ---------------------------------------------------------------- e-log-thousandth
key('e-log-thousandth', math.log10(0.001))
ex.claim(F(1, 1000) == F(1, 10 ** 3), 'e-log-thousandth 0.001 = 10^-3 exactly')
wrong('e-log-thousandth', 'pos', math.log10(1000))
wrong('e-log-thousandth', 'zeros', math.log10(0.01))

# ---------------------------------------------------------------- e-ticket-count (enumeration and product)
tickets = set(itertools.product(range(5), ('buy', 'sell'), ('market', 'limit', 'stop')))
key('e-ticket-count', len(tickets))
ex.claim(len(tickets) == 5 * 2 * 3, 'e-ticket-count enumeration 30 = 5 x 2 x 3')
wrong('e-ticket-count', 'add', 5 + 2 + 3)
wrong('e-ticket-count', 'side', len(set(itertools.product(range(5), range(3)))))
X('e-ticket-count', 'feedback.byKey.side', 15)

# ---------------------------------------------------------------- e-arc-length
r, th = 4, 2.5
key('e-arc-length', r * th)
ex.claim(near(r * th, 2 * math.pi * r * th / (2 * math.pi), 1e-12), 'e-arc-length arc as the fraction of the circumference')
wrong('e-arc-length', 'add', r + th)
wrong('e-arc-length', 'degrees', r * th * math.pi / 180)
wrong('e-arc-length', 'divide', r / th)
# byKey "divide" says "You divided the angle by the radius": that is 2.5 / 4 = 0.625; the stored 1.6 is 4 / 2.5 (finding 1)
ex.claim_text('exam', f'{P("e-arc-length")}.feedback.byKey.divide', 'divided the angle by the radius',
              near(th / r, IT['e-arc-length']['widget']['wrong'][0]['value'], 0.01),
              'e-arc-length byKey divide names the slip that gives the stored 1.6')

# ---------------------------------------------------------------- e-geom-eighth (iteration and closed form)
u = 7
for _ in range(7):
    u *= 2
key('e-geom-eighth', u)
ex.claim(u == 7 * 2 ** 7, 'e-geom-eighth iteration 896 = 7 x 2^7')
wrong('e-geom-eighth', 'power-n', 7 * 2 ** 8)
wrong('e-geom-eighth', 'times-n', 7 * 2 * 8)

# ---------------------------------------------------------------- e-four-falls
p = 1.0
for _ in range(4):
    p -= 0.03 * p
ex.claim(near(p, 0.97 ** 4, 1e-12), f'e-four-falls loop {p:.6f} = 0.97^4')
ex.claim(correct_ids('e-four-falls') == ['a'] and opt('e-four-falls', 'a')['text'] == '$0.97^4$', 'e-four-falls key 0.97^4')
X('e-four-falls', 'feedback.correct', round(p, 3))
X('e-four-falls', 'explain.text', round(p, 4))
X('e-four-falls', 'explain.text', round((1 - p) * 100, 1))
X('e-four-falls', 'widget.options[1].text', 1 - 4 * 0.03)
ex.claim(1 - 4 * 0.03 < p, 'e-four-falls "a little less than 12%": the true fall 11.47% is below 12%')

# ---------------------------------------------------------------- e-fraction-powers (exact)
a27 = round(27 ** (1 / 3)) ** 2
q16 = F(1, round(16 ** 0.25))
ex.claim(a27 ** 3 == 27 ** 2 and q16 ** -4 == 16, 'e-fraction-powers 27^(2/3) = 9 and 16^(-1/4) = 1/2 exactly (cubed and fourth powers)')
key('e-fraction-powers', float(a27 * q16))
wrong('e-fraction-powers', 'negative', a27 * -2)
wrong('e-fraction-powers', 'no-flip', a27 * 2)

# ---------------------------------------------------------------- e-weekly-savings (loop and Gauss)
weeks = [20 + 5 * (k - 1) for k in range(1, 31)]
key('e-weekly-savings', sum(weeks))
ex.claim(sum(weeks) == 15 * (20 + 165) and weeks[-1] == 165, 'e-weekly-savings loop 2775 = 15 x 185, week 30 is 165')
wrong('e-weekly-savings', 'last', 15 * (20 + 20 + 30 * 5))
wrong('e-weekly-savings', 'flat', 20 * 30)
wrong('e-weekly-savings', 'term', weeks[-1])
X('e-weekly-savings', 'explain.text', 185)

# ---------------------------------------------------------------- e-cosine-rule (formula and canvas coordinates)
c2 = 25 + 64 - 2 * 5 * 8 * F(1, 2)
key('e-cosine-rule', math.sqrt(c2))
pts = {q['id']: (q['x'], q['y']) for q in IT['e-cosine-rule']['canvas']['state']['points']}
dQ = math.dist(pts['D'], pts['Q'])
dPQ = math.dist(pts['P'], pts['Q'])
ang = math.degrees(math.atan2(pts['Q'][1], pts['Q'][0]))
ex.claim(near(dQ, 8, 1e-3) and near(math.dist(pts['D'], pts['P']), 5, 1e-9) and near(ang, 60, 0.01),
         f'e-cosine-rule canvas legs 5 and {dQ:.4f} at {ang:.3f} degrees')
ex.claim(near(dPQ, 7, 1e-3), f'e-cosine-rule canvas distance {dPQ:.4f} = 7')
wrong('e-cosine-rule', 'pythag', math.sqrt(89))
wrong('e-cosine-rule', 'plus', math.sqrt(89 + 40))
X('e-cosine-rule', 'feedback.correct', 49)

# ---------------------------------------------------------------- e-years-to-target (loop and logs)
bal, n = 5000.0, 0
while bal <= 8000:
    bal *= 1.06
    n += 1
key('e-years-to-target', n)
nlog = math.log(1.6) / math.log(1.06)
ex.claim(n == math.floor(nlog) + 1, f'e-years-to-target loop {n} = floor({nlog:.4f}) + 1')
X('e-years-to-target', 'feedback.correct', round(nlog, 2))
X('e-years-to-target', 'explain.text', round(5000 * 1.06 ** 8, 2))
X('e-years-to-target', 'explain.text', round(5000 * 1.06 ** 9, 2))
X('e-years-to-target', 'feedback.byKey.floor', round(5000 * 1.06 ** 8, 2))
wrong('e-years-to-target', 'floor', math.floor(nlog))
wrong('e-years-to-target', 'simple', 3000 / 300)
ex.claim(5000 + 300 * 10 == 8000, 'e-years-to-target simple interest reaches exactly £8,000 at year 10 (first above at 11; finding 26)')

# ---------------------------------------------------------------- e-continuous-four (exp and power series)
v = 2000 * math.exp(0.2)
vs = 2000 * sum(0.2 ** k / math.factorial(k) for k in range(30))
ex.claim(near(v, vs, 1e-9), 'e-continuous-four 2000e^0.2 by its power series')
key('e-continuous-four', round(v, 2), t=1e-9)
wrong('e-continuous-four', 'annual', round(2000 * 1.05 ** 4, 2), t=1e-9)
wrong('e-continuous-four', 'simple', 2000 + 4 * 100)
inband('e-continuous-four', 2442.80, 'truncated 2442.80 (true 2442.806; finding 24)', want=False)

# ---------------------------------------------------------------- e-wave-fit (sample the drawn curve)
xs = [k / 1000 for k in range(24001)]
ys = [3 * math.sin(math.pi * x / 6) + 5 for x in xs]
peaks = [xs[k] for k in range(1, len(xs) - 1) if ys[k] > ys[k - 1] and ys[k] >= ys[k + 1]]
ex.claim(near(max(ys), 8, 1e-9) and near(min(ys), 2, 1e-6), 'e-wave-fit curve runs between 2 and 8')
ex.claim([round(q, 3) for q in peaks] == [3.0, 15.0], f'e-wave-fit peaks at {peaks}: period 12')
ex.claim(near(2 * math.pi / (math.pi / 6), 12, 1e-12) and near(2 * math.pi / (math.pi / 12), 24, 1e-12),
         'e-wave-fit b = pi/6 gives period 12; option d (pi/12) gives 24')
ex.claim(near(2 * math.pi / 12, 0.5236, 1e-4), 'e-wave-fit option b sin(12x) has period 0.52 h, not 12')
ex.claim(correct_ids('e-wave-fit') == ['a'], 'e-wave-fit key a')

# ---------------------------------------------------------------- e-sigma-odd (term by term and formula)
terms = [2 * k - 1 for k in range(4, 16)]
key('e-sigma-odd', sum(terms))
ex.claim(len(terms) == 12 and terms[0] == 7 and terms[-1] == 29 and sum(terms) == 6 * 36 == 15 ** 2 - 9,
         'e-sigma-odd 12 terms 7..29, 6 x 36 = 225 - 9')
wrong('e-sigma-odd', 'count', 11 * (7 + 29) / 2)
wrong('e-sigma-odd', 'from-one', sum(2 * k - 1 for k in range(1, 16)))

# ---------------------------------------------------------------- e-desk-block (all 720 seatings)
people = 'PTABCD'
seat = [s for s in itertools.permutations(people) if abs(s.index('P') - s.index('T')) == 1]
key('e-desk-block', len(seat))
ex.claim(len(seat) == math.factorial(5) * 2, 'e-desk-block enumeration 240 = 5! x 2')
wrong('e-desk-block', 'no-swap', sum(1 for s in seat if s.index('P') < s.index('T')))
wrong('e-desk-block', 'all', math.factorial(6))

# ---------------------------------------------------------------- e-double-angle-solve (scan every degree)
sols = [x for x in range(360) if near(math.cos(math.radians(2 * x)), 0.5, 1e-9)]
ex.claim(sols == [30, 150, 210, 330], f'e-double-angle-solve scan gives {sols}')
txt = {o['id']: o['text'] for o in IT['e-double-angle-solve']['widget']['options']}
keyed = sorted(int(txt[i].strip('$').replace('^\\circ', '')) for i in correct_ids('e-double-angle-solve'))
ex.claim(keyed == sols, f'e-double-angle-solve keyed options {keyed}')
for oid, x, c in (('b', 60, -0.5), ('c', 120, -0.5), ('f', 300, -0.5)):
    ex.claim(near(math.cos(math.radians(2 * x)), c, 1e-9), f'e-double-angle-solve option {oid}: cos(2 x {x}) = {c}')
ex.claim(near(math.cos(math.radians(240)), -0.5, 1e-9), 'e-double-angle-solve option c why: cos 240 = -1/2')

# ---------------------------------------------------------------- e-binomial-cube (polynomial multiplication)
poly = [1]
for _ in range(6):
    poly = [(poly[k] if k < len(poly) else 0) * 2 + (poly[k - 1] if k >= 1 else 0) * -1 for k in range(len(poly) + 1)]
key('e-binomial-cube', poly[3])
ex.claim(poly[3] == math.comb(6, 3) * 2 ** 3 * (-1) ** 3, 'e-binomial-cube expansion -160 = C(6,3) 2^3 (-1)^3')
wrong('e-binomial-cube', 'sign', -poly[3])
wrong('e-binomial-cube', 'binom-only', math.comb(6, 3))
wrong('e-binomial-cube', 'binom-sign', -math.comb(6, 3))

# ---------------------------------------------------------------- e-tech-pick (all 120 sets)
shares = range(10)
tech = set(range(4))
sets = list(itertools.combinations(shares, 3))
good = sum(1 for s in sets if len(tech & set(s)) == 2)
key('e-tech-pick', good / len(sets))
ex.claim(good == math.comb(4, 2) * math.comb(6, 1) == 36 and len(sets) == 120, 'e-tech-pick enumeration 36 of 120')
wrong('e-tech-pick', 'other', math.comb(4, 2) / 120)
wrong('e-tech-pick', 'replace', 3 * 0.4 ** 2 * 0.6)
seq = [s for s in itertools.permutations(shares, 3)]
wrong('e-tech-pick', 'one-order', sum(1 for s in seq if s[0] in tech and s[1] in tech and s[2] not in tech) / len(seq))

# ---------------------------------------------------------------- e-log-returns (sum and product of e^r)
lr = [0.04, -0.07, 0.01]
prod = 1.0
for q in lr:
    prod *= math.exp(q)
key('e-log-returns', prod - 1)
ex.claim(near(prod - 1, math.exp(sum(lr)) - 1, 1e-12), 'e-log-returns product of e^r = e^(sum)')
inband('e-log-returns', -0.0198, 'typed -0.0198')
wrong('e-log-returns', 'sum', sum(lr))
wrong('e-log-returns', 'compound', 1.04 * 0.93 * 1.01 - 1)
X('e-log-returns', 'explain.text', round(math.exp(-0.02), 4))

# ---------------------------------------------------------------- e-two-u-minus-v
uu, vv = (3, -1), (2, 4)
w2 = (2 * uu[0] - vv[0], 2 * uu[1] - vv[1])
key('e-two-u-minus-v', math.hypot(*w2), t=0.0012)
ex.claim(w2 == (4, -6) and w2[0] ** 2 + w2[1] ** 2 == 52, 'e-two-u-minus-v 2u - v = (4, -6), squared length 52')
inband('e-two-u-minus-v', 7.21, 'typed 7.21')
wrong('e-two-u-minus-v', 'mags', 2 * math.hypot(*uu) - math.hypot(*vv))
wrong('e-two-u-minus-v', 'plus', math.hypot(2 * uu[0] + vv[0], 2 * uu[1] + vv[1]))
wrong('e-two-u-minus-v', 'abs-sum', abs(w2[0]) + abs(w2[1]))

# ---------------------------------------------------------------- e-tan-third-quadrant (exact and by angle)
cth = F(-8, 17)
sth = -F(15, 17)
ex.claim(sth ** 2 + cth ** 2 == 1, 'e-tan-third-quadrant (15/17)^2 + (8/17)^2 = 1 exactly')
theta = 180 + math.degrees(math.acos(8 / 17))
ex.claim(180 < theta < 270 and near(math.cos(math.radians(theta)), -8 / 17, 1e-12) and math.sin(math.radians(theta)) < 0,
         f'e-tan-third-quadrant theta = {theta:.3f} degrees, cos -8/17, sin negative')
key('e-tan-third-quadrant', math.tan(math.radians(theta)))
ex.claim(sth / cth == F(15, 8), 'e-tan-third-quadrant tan = 15/8 exactly')
wrong('e-tan-third-quadrant', 'sign', -15 / 8)
wrong('e-tan-third-quadrant', 'flip', 8 / 15)
wrong('e-tan-third-quadrant', 'sine', -15 / 17)
inband('e-tan-third-quadrant', 1.88, 'typed 1.88 (two places; finding 23)', want=True)

# ---------------------------------------------------------------- e-log-quotient (exact and back-substitution)
xq = F(6, 8)
ex.claim((xq + 6) / xq == 9, 'e-log-quotient (x + 6)/x = 9 at x = 3/4')
ex.claim(near(math.log(6.75, 3) - math.log(0.75, 3), 2, 1e-12), 'e-log-quotient check log_3 6.75 - log_3 0.75 = 2')
key('e-log-quotient', float(xq))
wrong('e-log-quotient', 'cube', 6 / 7)
wrong('e-log-quotient', 'double', 6 / 5)

# ---------------------------------------------------------------- e-perpetuity-now (partial sums and closed form)
part = sum(60 / 1.04 ** k for k in range(3000))
key('e-perpetuity-now', 60 * 1.04 / 0.04, t=1e-6)
ex.claim(near(part, 1560, 1e-6), f'e-perpetuity-now 3,000 terms sum to {part:.6f}')
wrong('e-perpetuity-now', 'today', 60 / 0.04)
wrong('e-perpetuity-now', 'minus', 60 / 0.04 - 60)
wrong('e-perpetuity-now', 'ratio', 60 / (1 - 0.04))

# ---------------------------------------------------------------- e-vector-ratio (coordinates)
A, B = (5, 1), (1, 4)
Xp = (A[0] + (B[0] - A[0]) / 3, A[1] + (B[1] - A[1]) / 3)
ex.claim(near(math.dist(A, Xp) / math.dist(Xp, B), 0.5, 1e-12), 'e-vector-ratio X splits AB 1 : 2')
cx = {q['id']: (q['x'], q['y']) for q in IT['e-vector-ratio']['canvas']['params']['points']}
ex.claim(near(cx['X'][0], Xp[0], 1e-3) and near(cx['X'][1], Xp[1], 1e-3), f'e-vector-ratio canvas X {cx["X"]} = {Xp}')
lin = (2 / 3 * A[0] + 1 / 3 * B[0], 2 / 3 * A[1] + 1 / 3 * B[1])
ex.claim(near(lin[0], Xp[0], 1e-12) and near(lin[1], Xp[1], 1e-12) and correct_ids('e-vector-ratio') == ['a'], 'e-vector-ratio key 2/3 a + 1/3 b')
D = ((A[0] + B[0]) / 3, (A[1] + B[1]) / 3)
cross = (B[0] - A[0]) * (D[1] - A[1]) - (B[1] - A[1]) * (D[0] - A[0])
ex.claim(abs(cross) > 1e-6, 'e-vector-ratio option d point 1/3(a + b) is not on AB')

# ---------------------------------------------------------------- e-code-repeat (all 65,536 codes)
chars = '0123456789ABCDEF'
rep = sum(1 for c in itertools.product(chars, repeat=4) if len(set(c)) < 4)
key('e-code-repeat', rep)
ex.claim(rep == 16 ** 4 - 16 * 15 * 14 * 13, 'e-code-repeat enumeration 21856 = 16^4 - 16 x 15 x 14 x 13')
wrong('e-code-repeat', 'distinct', math.perm(16, 4))
wrong('e-code-repeat', 'all', 16 ** 4)

# ---------------------------------------------------------------- e-accounts-meet (bisection and logs)
lo, hi = 0.0, 50.0
for _ in range(200):
    mid = (lo + hi) / 2
    if 1000 * math.exp(0.05 * mid) < 1200 * math.exp(0.03 * mid):
        lo = mid
    else:
        hi = mid
tm = math.log(1.2) / 0.02
ex.claim(near(lo, tm, 1e-9), f'e-accounts-meet bisection {lo:.6f} = ln 1.2 / 0.02')
key('e-accounts-meet', round(tm, 2), t=1e-9)
X('e-accounts-meet', 'explain.text', round(math.log(1.2), 4))
X('e-accounts-meet', 'explain.text', round(1000 * math.exp(0.05 * tm)))
wrong('e-accounts-meet', 'add', math.log(1.2) / 0.08)
wrong('e-accounts-meet', 'simple', 200 / (50 - 36))
inband('e-accounts-meet', 9.11, 'typed 9.11 (true 9.116; finding 24)', want=False)

# ---------------------------------------------------------------- e-loan-payment (closed form and amortisation)
pay = 10000 * 0.05 / (1 - 1.05 ** -10)
key('e-loan-payment', round(pay, 2), t=1e-9)
balance = 10000.0
for _ in range(10):
    balance = balance * 1.05 - round(pay, 2)
inband('e-loan-payment', 1295.04, 'truncated 1295.04 (true 1295.046; finding 24)', want=False)
ex.claim(abs(balance) < 0.10, f'e-loan-payment paying £1,295.05 ten times leaves {balance:.4f} ("clears the balance")')
wrong('e-loan-payment', 'no-interest', 1000)
wrong('e-loan-payment', 'simple', 1000 + 500)
wrong('e-loan-payment', 'future', round(10000 * 1.05 ** 10 / 10, 2), t=1e-9)

# ---------------------------------------------------------------- freshness: setups repeated from the courses (findings 2 to 20)
def _texts(x):
    if isinstance(x, str):
        return [x]
    if isinstance(x, dict):
        return [t for v in x.values() for t in _texts(v)]
    if isinstance(x, list):
        return [t for v in x for t in _texts(v)]
    return []


def has(iid, *phrases):
    s = '\n'.join(_texts(IT[iid]))
    return all(ph in s for ph in phrases)


REPEATS = [
    ('e-years-to-target', ('5,000', '8,000', '6%'), 'exp-log review-2 items[6]: £5,000.00 at 6% first above £8,000.00, answer 9'),
    ('e-desk-block', ('Six traders', 'next to each other'), 'counting l6 quiz[0]: six people in a row, two side by side, 240'),
    ('e-double-angle-solve', ('2x', '0^\\circ \\le x'), 'trig l11 screens[7]: solve sin 2x = 0.5 on 0 to 360 with u = 2x'),
    ('e-tech-pick', ('10 shares', '4 of them', 'pick 3', 'exactly 2'), 'mock-oa-trader-2 b09-committee: 10 with 4 marked, team of 3, exactly 2'),
    ('e-geom-eighth', ('7, 14, 28, 56',), 'series l3 screens[4] (3, 6, 12, 24, u_8) and mock-oa-trader-2 a02-geometric (7, 14, 28, 56)'),
    ('e-code-repeat', ('4 characters', 'at least one character repeated'), 'counting homework-2 h-pin-repeat: 4-digit PIN, at least one repeat'),
    ('e-loan-payment', ('£10,000', 'equal payments', 'end of each year'), 'series homework-3 items[7]: £10,000 loan, equal end-of-year payments'),
    ('e-tan-third-quadrant', ('\\cos\\theta = -', 'tan'), 'trig l10 quiz[0] and quiz[2], homework-2 items[3]: one ratio and the quadrant'),
    ('e-cosine-rule', ('60^\\circ', '5 km', '8 km'), 'trig l5 quiz[0] (6 and 8 at 60) and homework-1 items[6] (5 km and 8 km)'),
    ('e-continuous-four', ('continuous rate', 'for 4 years'), 'exp-log l9 quiz[0] and screens[5]: a sum at a continuous rate for t years'),
    ('e-log-returns', ('daily log returns over three days',), 'exp-log l11 quiz[1] (three daily log returns) with screens[5] (e^x - 1)'),
    ('e-fraction-powers', ('27^{2/3}',), 'exp-log l3 screens[7]: which value is 27^{2/3}'),
    ('e-arc-length', ('2.5 radians',), 'trig homework-2 items[1] (a wheel turns through 2.5 radians) and l7 quiz[2]'),
    ('e-log-thousandth', ('\\log_{10} 0.001',), 'exp-log l7 quiz[0]: what is log 0.01'),
    ('e-four-falls', ('falls 3% a day for 4 days',), 'exp-log l2 screens[6]: falls 10% every day for 10 days'),
    ('e-weekly-savings', ('£20 in week 1', '£5 more each week'), 'series l5 screens[1]: save £3 in week 1, then £2 more each week'),
    ('e-binomial-cube', ('coefficient of $x^3$',), 'series l11 quiz[0]: the number in front of x^3 in (x + 2)^5'),
    ('e-wave-fit', ('Which equation fits the graph',), 'trig review-2 items[7] and l13 screens[6]: read max, min and period, pick the model'),
    ('e-sigma-odd', ('(2k - 1)',), 'series l5 quiz[2]: sum of (2k - 1)'),
]
for iid, phrases, where in REPEATS:
    ex.claim(not has(iid, *phrases), f'{iid} fresh against {where}')

# ---------------------------------------------------------------- wrong values against the answer bands (rule 581)
ex.check_wrongs()
ex.report()
