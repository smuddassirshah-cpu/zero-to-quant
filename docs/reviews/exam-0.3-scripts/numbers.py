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


# ---------------------------------------------------------------- metadata, shape, coverage, timing
def _texts(x):
    if isinstance(x, str):
        return [x]
    if isinstance(x, dict):
        return [t for v in x.values() for t in _texts(v)]
    if isinstance(x, list):
        return [t for v in x for t in _texts(v)]
    return []


def has(iid, *phrases, head=False):
    src = {k: IT[iid].get(k, '') for k in ('prose', 'question')} if head else IT[iid]
    s = '\n'.join(_texts(src))
    return all(ph in s for ph in phrases)


ex.claim(doc['pass'] == 0.7, 'pass 0.7 as section 5 asks')
ex.claim(20 <= len(doc['items']) <= 30, f'{len(doc["items"])} items, inside 20 to 30')
ramp = {d: sum(1 for it in doc['items'] if it['difficulty'] == d) for d in (2, 3, 4, 5)}
ex.claim(ramp == {2: 5, 3: 13, 4: 6, 5: 2}, f'ramp {ramp} of {len(doc["items"])} (19%, 50%, 23%, 8% against 20, 50, 20, 10)')
union = {}
for c in ('exp-log', 'series', 'trig', 'counting'):
    with open(os.path.join(COURSES, c, 'course.json'), encoding='utf8') as f:
        union.update(json.load(f)['skills'])
ex.claim(doc['skills'] == union, 'skills map equals the union of the four course.json maps (20 ids)')
used = {s for it in doc['items'] for s in it['skills']}
ex.claim(used == set(union), 'every skill is tested by at least one item')
# Timing (finding 22): AUTHORING section 5 says `minutes` is shown as written, so it is the time the paper really needs.
# Rule used: the sum of the items' `pace` (Stage 0 paces of topic-0.6: d2 45 to 60 s, d3 90 to 150 s, d4 150 to 180 s,
# d5 300 and 360 s), rounded up to the next whole 5 minutes. 3,525 s is 58.75 minutes, so the clock is 60.
paces = [it.get('pace') for it in doc['items']]
ex.claim(all(isinstance(p, (int, float)) and p > 0 for p in paces), 'every item has a positive pace')
need = sum(paces)
ex.claim(need == 3525, f'paces sum to {need} s ({need / 60:.2f} min)')
ex.claim(doc['minutes'] == math.ceil(need / 300) * 5 == 60, f'minutes {doc["minutes"]} = paced need {need / 60:.2f} min rounded up to 5')
ex.claim(need <= doc['minutes'] * 60 <= 1.05 * need, 'the clock covers the paces and is within 5% of them (no slack of 30 minutes as before)')
for it in doc['items']:
    ws = {w['id'] for w in it['widget'].get('wrong', [])}
    bk = set(it['feedback'].get('byKey', {}))
    ex.claim(ws == bk, f'{it["id"]} byKey ids equal wrong ids')

# ---------------------------------------------------------------- e-log-thousandth (now log_4 0.0625, finding 15)
key('e-log-thousandth', math.log(0.0625, 4))
ex.claim(F(1, 16) == F(1, 4 ** 2) and F(625, 10000) == F(1, 16), 'e-log-thousandth 0.0625 = 1/16 = 4^-2 exactly')
wrong('e-log-thousandth', 'pos', math.log(16, 4))
wrong('e-log-thousandth', 'places', math.log(0.0625, 2))
ex.claim(len('0625') == 4 and math.log(0.0625, 2) == -4, 'e-log-thousandth "places" slip: 4 decimal places and log_2 give -4, away from -2')
X('e-log-thousandth', 'explain.text', 16)

# ---------------------------------------------------------------- e-ticket-count (enumeration and product)
tickets = set(itertools.product(range(5), ('buy', 'sell'), ('market', 'limit', 'stop')))
key('e-ticket-count', len(tickets))
ex.claim(len(tickets) == 5 * 2 * 3, 'e-ticket-count enumeration 30 = 5 x 2 x 3')
wrong('e-ticket-count', 'add', 5 + 2 + 3)
wrong('e-ticket-count', 'side', len(set(itertools.product(range(5), range(3)))))
X('e-ticket-count', 'feedback.byKey.side', 15)

# ---------------------------------------------------------------- e-arc-length (6 cm, 1.8 rad; findings 1 and 14)
r, th = 6, 1.8
key('e-arc-length', r * th)
ex.claim(near(r * th, 2 * math.pi * r * (th / (2 * math.pi)), 1e-12), 'e-arc-length arc as the fraction of the circumference')
wrong('e-arc-length', 'add', r + th)
wrong('e-arc-length', 'degrees', r * th * math.pi / 180)
wrong('e-arc-length', 'divide', r / th)
tx = ex.text('exam', f'{P("e-arc-length")}.feedback.byKey.divide')
ex.claim('divided the radius by the angle' in tx and 'divided the angle by the radius' not in tx
         and near(r / th, IT['e-arc-length']['widget']['wrong'][0]['value'], 0.001),
         'e-arc-length byKey divide names the slip that gives the stored 3.3333 (radius over angle), not 1.6-style angle over radius (finding 1)')
X('e-arc-length', 'explain.text', 10.8)

# ---------------------------------------------------------------- e-geom-eighth (3rd term 12, 6th term 96; finding 6)
rr = F(96, 12) ** F(1, 3)
ex.claim(rr == 2 and 2 ** 3 == 8, 'e-geom-eighth r^3 = 96 / 12 = 8, so r = 2')
a1 = F(12, 2 ** 2)
u = a1
terms = [u]
for _ in range(9):
    u *= 2
    terms.append(u)
ex.claim(a1 == 3 and terms[2] == 12 and terms[5] == 96, 'e-geom-eighth first term 3, 3rd term 12, 6th term 96 by iteration')
key('e-geom-eighth', terms[9])
ex.claim(terms[9] == 96 * 2 ** 4 == 3 * 2 ** 9 == 1536, 'e-geom-eighth 10th term 1536 = 96 x 2^4 = 3 x 2^9')
wrong('e-geom-eighth', 'power-n', 3 * 2 ** 10)
wrong('e-geom-eighth', 'first-term', 12 * 2 ** 9)
wrong('e-geom-eighth', 'arith', 96 + 4 * ((96 - 12) // 3))
ex.claim((96 - 12) / 3 == 28, 'e-geom-eighth arithmetic slip adds 28 a step')

# ---------------------------------------------------------------- e-four-falls (four falls then four rises; finding 16)
p = 1.0
for _ in range(4):
    p *= 0.97
for _ in range(4):
    p *= 1.03
ex.claim(near(p, (0.97 * 1.03) ** 4, 1e-12), f'e-four-falls loop of eight days {p:.6f} = (0.97 x 1.03)^4')
ex.claim(correct_ids('e-four-falls') == ['a'] and opt('e-four-falls', 'a')['text'] == '$(0.97 \\times 1.03)^4$', 'e-four-falls key (0.97 x 1.03)^4')
X('e-four-falls', 'feedback.correct', round(p, 4))
X('e-four-falls', 'explain.text', round(p, 4))
X('e-four-falls', 'explain.text', round(0.97 * 1.03, 4))
X('e-four-falls', 'explain.text', round((1 - p) * 100, 2))
X('e-four-falls', 'widget.options[1].why', round(0.97 * 1.03, 4))
ex.claim(0.97 * 1.03 < 1 and round(0.97 * 1.03, 4) == 0.9991, 'e-four-falls a fall then a rise of 3% is 0.9991, below 1')
ex.claim(not near(0.97 ** 4 * 1.03, p, 0.01) and not near((0.9991) ** 8, p, 1e-4) and (0.9991) ** 8 < p,
         f'e-four-falls option c {0.97 ** 4 * 1.03:.4f} and option d {0.9991 ** 8:.4f} differ from the key {p:.4f}')
ex.claim(near(0.9991 ** 4, 0.9964, 1e-5), 'e-four-falls 0.9991^4 = 0.9964')

# ---------------------------------------------------------------- e-fraction-powers (125^(2/3) x 625^(-1/4); finding 13)
a125 = round(125 ** (1 / 3)) ** 2
q625 = F(1, round(625 ** 0.25))
ex.claim(round(125 ** (1 / 3)) ** 3 == 125 and a125 == 25 and q625 ** -4 == 625, 'e-fraction-powers 125^(2/3) = 25 and 625^(-1/4) = 1/5 exactly')
key('e-fraction-powers', float(a125 * q625))
wrong('e-fraction-powers', 'negative', a125 * -5)
wrong('e-fraction-powers', 'no-flip', a125 * 5)

# ---------------------------------------------------------------- e-weekly-savings (find d from the total; finding 17)
d_exact = (F(2 * 2775, 30) - 2 * 20) / 29
ex.claim(d_exact == 5, 'e-weekly-savings Gauss backwards: (2 x 2775 / 30 - 40) / 29 = 5')
weeks = [20 + 5 * k for k in range(30)]
ex.claim(sum(weeks) == 2775 == 15 * (20 + 165) and weeks[-1] == 165, 'e-weekly-savings loop at d = 5 gives 2775 = 15 x 185, week 30 is 165')
ex.claim(all(sum(20 + dd * k for k in range(30)) != 2775 for dd in range(0, 20) if dd != 5), 'e-weekly-savings d = 5 is the only whole-pound step that gives 2775')
key('e-weekly-savings', float(d_exact))
wrong('e-weekly-savings', 'steps', (2775 / 15 - 40) / 30)
wrong('e-weekly-savings', 'average', (2775 / 30 - 20) / 29)
wrong('e-weekly-savings', 'flat', 2775 / 30 - 20)
X('e-weekly-savings', 'feedback.byKey.average', 92.5)
X('e-weekly-savings', 'explain.text', 185)
X('e-weekly-savings', 'explain.text', 165)

# ---------------------------------------------------------------- e-cosine-rule (3 and 5 at 120 degrees; finding 10)
cos120 = F(-1, 2)
ex.claim(near(math.cos(math.radians(120)), float(cos120), 1e-12), 'e-cosine-rule cos 120 = -1/2')
c2 = 9 + 25 - 2 * 3 * 5 * cos120
key('e-cosine-rule', math.sqrt(c2))
ex.claim(c2 == 49 and 34 + 15 == 49, 'e-cosine-rule c^2 = 9 + 25 + 15 = 49')
pts = {q['id']: (q['x'], q['y']) for q in IT['e-cosine-rule']['canvas']['state']['points']}
dQ = math.dist(pts['D'], pts['Q'])
dPQ = math.dist(pts['P'], pts['Q'])
ang = math.degrees(math.atan2(pts['Q'][1], pts['Q'][0]))
ex.claim(near(dQ, 5, 1e-3) and near(math.dist(pts['D'], pts['P']), 3, 1e-9) and near(ang, 120, 0.01),
         f'e-cosine-rule canvas legs 3 and {dQ:.4f} at {ang:.3f} degrees')
ex.claim(near(dPQ, 7, 1e-3), f'e-cosine-rule canvas distance {dPQ:.4f} = 7')
cp = IT['e-cosine-rule']['canvas']['params']
ex.claim(all(cp['x'][0] <= x <= cp['x'][1] and cp['y'][0] <= y <= cp['y'][1] for x, y in pts.values()), 'e-cosine-rule every canvas point lies inside the plane window')
ex.claim(has('e-cosine-rule', '$120^\\circ$', '3 km', '5 km') and not has('e-cosine-rule', '60^\\circ'), 'e-cosine-rule labels 3 km, 5 km and 120 degrees; no 60')
wrong('e-cosine-rule', 'pythag', math.sqrt(34))
wrong('e-cosine-rule', 'acute', math.sqrt(34 - 15))
ex.claim(IT['e-cosine-rule']['skills'] == ['tr-triangles', 'tr-circle'], 'e-cosine-rule skills tr-triangles and tr-circle (the sign of cos 120)')
X('e-cosine-rule', 'feedback.correct', 49)
X('e-cosine-rule', 'explain.text', 49)
X('e-cosine-rule', 'explain.text', 34)

# ---------------------------------------------------------------- e-truss-angle (new, finding 25)
ex.claim(doc['items'][idx['e-cosine-rule'] + 1]['id'] == 'e-truss-angle', 'e-truss-angle sits straight after e-cosine-rule')
base_ang = math.degrees(math.acos(5 / 7))
key('e-truss-angle', base_ang, t=1e-4)
cos_base = F(7 ** 2 + 10 ** 2 - 7 ** 2, 2 * 7 * 10)
ex.claim(cos_base == F(5, 7), 'e-truss-angle cosine rule at the base: (7^2 + 10^2 - 7^2) / (2 x 7 x 10) = 5/7')
apex = math.degrees(math.acos(F(7 ** 2 + 7 ** 2 - 10 ** 2, 2 * 7 * 7)))
ex.claim(near(2 * base_ang + apex, 180, 1e-9), f'e-truss-angle angle sum {base_ang:.4f} x 2 + {apex:.4f} = 180')
wrong('e-truss-angle', 'apex', apex)
wrong('e-truss-angle', 'vertical', math.degrees(math.asin(5 / 7)))
wrong('e-truss-angle', 'radians', math.acos(5 / 7), t=0.05)
ex.claim(round(math.acos(5 / 7), 1) == 0.8 and near(0.8, 0.7752, 0.05), 'e-truss-angle the radians slip rounded as asked (0.8) is inside its band')
ex.claim(near(math.degrees(math.asin(5 / 7)), 90 - base_ang, 1e-9), 'e-truss-angle sin = 5/7 gives 90 minus the base angle')
inband('e-truss-angle', 44.4, 'typed 44.4')
inband('e-truss-angle', 44.5, 'typed 44.5', want=False)
inband('e-truss-angle', 44.3, 'typed 44.3', want=False)
ex.claim(math.sqrt(7 ** 2 - 5 ** 2) > 0 and near(math.sqrt(24), 4.899, 1e-3), 'e-truss-angle the truss rises 4.899 m, so the triangle exists (7 + 7 > 10)')
X('e-truss-angle', 'feedback.correct', 44.4)
X('e-truss-angle', 'explain.text', 44.4)

# ---------------------------------------------------------------- e-years-to-target (a car at 12% a year; finding 2)
bal, n = 18000.0, 0
while bal >= 5000:
    bal *= 0.88
    n += 1
key('e-years-to-target', n)
nlog = math.log(5 / 18) / math.log(0.88)
ex.claim(n == math.floor(nlog) + 1 and near(math.log(5 / 18, 10) / math.log(0.88, 10), nlog, 1e-12), f'e-years-to-target loop {n} = floor({nlog:.4f}) + 1, log and ln agree')
X('e-years-to-target', 'feedback.correct', round(nlog, 2))
X('e-years-to-target', 'explain.text', round(nlog, 2))
X('e-years-to-target', 'explain.text', round(18000 * 0.88 ** 10, 2))
X('e-years-to-target', 'explain.text', round(18000 * 0.88 ** 11, 2))
X('e-years-to-target', 'feedback.byKey.floor', round(18000 * 0.88 ** 10, 2))
ex.claim(18000 * 0.88 ** 10 > 5000 > 18000 * 0.88 ** 11, 'e-years-to-target £5,013.02 after 10 years is above £5,000, £4,411.46 after 11 is below')
wrong('e-years-to-target', 'floor', math.floor(nlog))
simple_n = next(k for k in range(1, 40) if 18000 - 2160 * k < 5000)
wrong('e-years-to-target', 'simple', simple_n)
ex.claim(18000 * 12 // 100 == 2160, 'e-years-to-target 12% of £18,000 is £2,160')
X('e-years-to-target', 'feedback.byKey.simple', 2160)
ex.claim('ln' not in ' '.join(_texts(IT['e-years-to-target'])).replace('\\ln', 'LN').replace('\\ne', ''), 'e-years-to-target uses log, as exp-log l8 and review-2 do (ln is taught in L3)')

# ---------------------------------------------------------------- e-continuous-four (5% for 2 years then 3% for 3; finding 11)
v = 2000 * math.exp(0.05 * 2) * math.exp(0.03 * 3)
vs = 2000 * sum(0.19 ** k / math.factorial(k) for k in range(30))
ex.claim(near(v, vs, 1e-9) and near(v, 2000 * math.exp(0.19), 1e-9), f'e-continuous-four e^0.10 x e^0.09 = e^0.19, by its power series: {v:.4f}')
key('e-continuous-four', round(v, 2), t=1e-9)
ex.claim(near(IT['e-continuous-four']['widget']['answer'], v, IT['e-continuous-four']['widget']['tol']['abs']),
         f'e-continuous-four stored 2418.5 is within its 0.005 of the unrounded {v:.4f} (finding 24)')
wrong('e-continuous-four', 'average', round(2000 * math.exp(0.04 * 5), 2), t=1e-9)
wrong('e-continuous-four', 'annual', round(2000 * 1.05 ** 2 * 1.03 ** 3, 2), t=1e-9)
wrong('e-continuous-four', 'simple', 2000 + 2000 * 0.19)
inband('e-continuous-four', 2418.50, 'typed 2418.50')
inband('e-continuous-four', 2418.49, 'truncated 2418.49', want=False)
inband('e-continuous-four', 2418.51, 'typed 2418.51', want=False)
X('e-continuous-four', 'explain.text', 2418.5)
X('e-continuous-four', 'feedback.correct', 2418.5)

# ---------------------------------------------------------------- e-wave-fit (a falling wave; finding 19)
xs = [k / 1000 for k in range(24001)]
f = lambda x: -3 * math.sin(math.pi * x / 6) + 5
ys = [f(x) for x in xs]
troughs = [xs[k] for k in range(1, len(xs) - 1) if ys[k] < ys[k - 1] and ys[k] <= ys[k + 1]]
peaks = [xs[k] for k in range(1, len(xs) - 1) if ys[k] > ys[k - 1] and ys[k] >= ys[k + 1]]
ex.claim(near(max(ys), 8, 1e-9) and near(min(ys), 2, 1e-6), 'e-wave-fit curve runs between 2 and 8')
ex.claim([round(q, 3) for q in troughs] == [3.0, 15.0] and [round(q, 3) for q in peaks] == [9.0, 21.0],
         f'e-wave-fit troughs at {troughs} and peaks at {peaks}: period 12')
ex.claim(ys[1] < ys[0] and f(0) == 5 and f(1) < 5, 'e-wave-fit the curve leaves the midline going down')
ex.claim(IT['e-wave-fit']['canvas']['params']['functions'][0]['expr'] == '-3*sin(pi*x/6)+5', 'e-wave-fit canvas draws -3 sin(pi x / 6) + 5')
MODEL = {'a': (-3, math.pi / 6), 'b': (3, math.pi / 6), 'c': (-6, math.pi / 6), 'd': (-3, math.pi / 12)}
TXT = {o['id']: o['text'] for o in IT['e-wave-fit']['widget']['options']}
MODEL_AMP = {'a': '-3', 'b': '3', 'c': '-6', 'd': '-3'}
MODEL_DEN = {'a': '6', 'b': '6', 'c': '6', 'd': '12'}
fits = [k for k, (am, bb) in MODEL.items() if all(near(am * math.sin(bb * x) + 5, f(x), 1e-9) for x in xs[::97])]
ex.claim(fits == ['a'] and correct_ids('e-wave-fit') == ['a'], f'e-wave-fit only option a matches the drawn curve (matches: {fits})')
ex.claim(all(TXT[k].replace(' ', '').startswith('$y=' + MODEL_AMP[k] + '\\sin') and TXT[k].replace(' ', '').endswith('+5$') and ('\\pi x}{' + MODEL_DEN[k] + '}') in TXT[k] for k in 'abcd'),
         'e-wave-fit option texts match the models a (-3, pi/6), b (3, pi/6), c (-6, pi/6), d (-3, pi/12)')
ex.claim(near(2 * math.pi / (math.pi / 6), 12, 1e-12) and near(2 * math.pi / (math.pi / 12), 24, 1e-12), 'e-wave-fit b = pi/6 gives period 12; option d (pi/12) gives 24')
ex.claim(near(-6 * -1 + 5, 11, 0) and near(min(-6 * math.sin(math.pi * x / 6) + 5 for x in xs[::50]), -1, 1e-6), 'e-wave-fit option c reaches 11 and -1, not 8 and 2')

# ---------------------------------------------------------------- e-sigma-odd (sum of 3k + 2 from k = 5; finding 20)
terms = [3 * k + 2 for k in range(5, 21)]
key('e-sigma-odd', sum(terms))
ex.claim(len(terms) == 16 == 20 - 5 + 1 and terms[0] == 17 and terms[-1] == 62 and sum(terms) == 8 * 79 == 632, 'e-sigma-odd 16 terms 17..62, 8 x 79 = 632')
wrong('e-sigma-odd', 'count', 15 * (17 + 62) / 2)
wrong('e-sigma-odd', 'from-one', sum(3 * k + 2 for k in range(1, 21)))
ex.claim(sum(3 * k + 2 for k in range(1, 5)) == 5 + 8 + 11 + 14 == 38 and 670 - 38 == 632, 'e-sigma-odd the first four terms 5, 8, 11, 14 add to 38; 670 - 38 = 632')
X('e-sigma-odd', 'explain.text', 38)
X('e-sigma-odd', 'explain.text', 670)

# ---------------------------------------------------------------- e-desk-block (all 720 seatings; finding 3)
people = 'PTSABC'
adj = [s for s in itertools.permutations(people) if abs(s.index('P') - s.index('T')) == 1]
seat = [s for s in adj if s.index('S') not in (0, 5)]
key('e-desk-block', len(seat))
ex.claim(len(adj) == math.factorial(5) * 2 == 240, 'e-desk-block enumeration 240 seatings with the pair together = 5! x 2')
ends = sum(1 for s in adj if s.index('S') in (0, 5))
one = sum(1 for s in adj if s.index('S') == 0)
ex.claim(one == 4 * 3 * 2 * 1 * 2 == 48 and ends == 96 and len(adj) - ends == 144, 'e-desk-block Sam at one end 48, at both ends 96, so 240 - 96 = 144')
ex.claim(len(seat) == 5 * 4 * 3 * 2 * 1 * 2 - 2 * 4 * 3 * 2 * 1 * 2, 'e-desk-block formula 240 - 96 = 144')
wrong('e-desk-block', 'no-sam', len(adj))
wrong('e-desk-block', 'one-end', len(adj) - one)
wrong('e-desk-block', 'no-swap', sum(1 for s in seat if s.index('P') + 1 == s.index('T')))
ex.claim(IT['e-desk-block']['difficulty'] == 4, 'e-desk-block difficulty 4 (two conditions)')
X('e-desk-block', 'feedback.correct', 96)
X('e-desk-block', 'explain.text', 48)
X('e-desk-block', 'explain.text', 96)
X('e-desk-block', 'feedback.byKey.one-end', 48)

# ---------------------------------------------------------------- e-double-angle-solve (cos 3x = 1/2; finding 5)
sols = [x for x in range(180) if near(math.cos(math.radians(3 * x)), 0.5, 1e-9)]
ex.claim(sols == [20, 100, 140], f'e-double-angle-solve scan of 0 to 179 gives {sols}')
us = [u for u in range(0, 540) if near(math.cos(math.radians(u)), 0.5, 1e-9)]
ex.claim(us == [60, 300, 420] and 660 > 540 and near(math.cos(math.radians(660)), 0.5, 1e-9), 'e-double-angle-solve u = 3x in [0, 540): 60, 300, 420; next is 660, past 540')
ex.claim(len(IT['e-double-angle-solve']['widget']['options']) == 6, 'e-double-angle-solve six options (g deleted)')
txt = {o['id']: o['text'] for o in IT['e-double-angle-solve']['widget']['options']}
keyed = sorted(int(txt[i].strip('$').replace('^\\circ', '')) for i in correct_ids('e-double-angle-solve'))
ex.claim(keyed == sols, f'e-double-angle-solve keyed options {keyed}')
ex.claim(sorted(txt) == list('abcdef') and [int(txt[k].strip('$').replace('^\\circ', '')) for k in 'abcdef'] == [20, 40, 60, 100, 140, 160],
         'e-double-angle-solve options are 20, 40, 60, 100, 140, 160')
for oid, x, c in (('b', 40, -0.5), ('c', 60, -1.0), ('f', 160, -0.5)):
    ex.claim(near(math.cos(math.radians(3 * x)), c, 1e-9) and x not in sols, f'e-double-angle-solve option {oid}: cos(3 x {x}) = {c}, not a solution')
ex.claim(near(math.cos(math.radians(120)), -0.5, 1e-9) and 180 - 60 == 120 and 120 + 360 == 480 == 3 * 160, 'e-double-angle-solve option b and f whys: 180 - 60 = 120; 120 + 360 = 480 = 3 x 160')
X('e-double-angle-solve', 'feedback.correct', 420)
X('e-double-angle-solve', 'explain.text', 540)
X('e-double-angle-solve', 'explain.text', 660)

# ---------------------------------------------------------------- e-binomial-cube ((1 + ax)^6, coefficient of x^2 = 135; finding 18)
def coef2(a):
    poly = [1]
    for _ in range(6):
        poly = [(poly[k] if k < len(poly) else 0) + (poly[k - 1] * a if k >= 1 else 0) for k in range(len(poly) + 1)]
    return poly[2]
ex.claim(coef2(3) == 135 == math.comb(6, 2) * 9 and math.comb(6, 2) == 15, 'e-binomial-cube (1 + 3x)^6 multiplied out has x^2 coefficient 135 = 15 x 9')
ex.claim([a for a in range(-20, 21) if coef2(a) == 135] == [-3, 3], 'e-binomial-cube coefficient 135 for a = -3 and 3 only, so a > 0 picks 3')
key('e-binomial-cube', 3)
wrong('e-binomial-cube', 'square', 9)
wrong('e-binomial-cube', 'six', math.sqrt(135 / 6))
X('e-binomial-cube', 'explain.text', 15)

# ---------------------------------------------------------------- e-tech-pick (12 shares, 5 tech, pick 4; finding 4)
sets = list(itertools.combinations(range(12), 4))
tech = set(range(5))
good = sum(1 for s in sets if len(tech & set(s)) == 2)
key('e-tech-pick', good / len(sets))
ex.claim(good == math.comb(5, 2) * math.comb(7, 2) == 210 and len(sets) == math.comb(12, 4) == 495, 'e-tech-pick enumeration 210 of 495')
ex.claim(F(210, 495) == F(14, 33), 'e-tech-pick 210/495 = 14/33')
wrong('e-tech-pick', 'other', math.comb(5, 2) / 495)
wrong('e-tech-pick', 'replace', 6 * (5 / 12) ** 2 * (7 / 12) ** 2)
seq = list(itertools.permutations(range(12), 4))
wrong('e-tech-pick', 'one-order', sum(1 for s in seq if s[0] in tech and s[1] in tech and s[2] not in tech and s[3] not in tech) / len(seq))
ex.claim(6 * F(5, 12) * F(4, 11) * F(7, 10) * F(6, 9) == F(14, 33) and math.comb(4, 2) == 6, 'e-tech-pick six orders of the one-order slip give the key')
inband('e-tech-pick', 0.424, 'typed 0.424')
inband('e-tech-pick', 0.425, 'typed 0.425', want=False)
X('e-tech-pick', 'explain.text', 495)
X('e-tech-pick', 'explain.text', 210)
X('e-tech-pick', 'feedback.byKey.other', 21)

# ---------------------------------------------------------------- e-log-returns (there and back; finding 12)
mon = 0.05
tue = -mon
ex.claim(near(math.exp(mon) * math.exp(tue), 1, 1e-12), 'e-log-returns Monday and Tuesday log returns multiply to 1: the price is back where it began')
key('e-log-returns', math.exp(tue) - 1)
inband('e-log-returns', -0.0488, 'typed -0.0488')
inband('e-log-returns', -0.0487, 'typed -0.0487', want=False)
wrong('e-log-returns', 'log', tue)
wrong('e-log-returns', 'flip', -(math.exp(mon) - 1))
ex.claim(abs(math.exp(tue) - 1) < math.exp(mon) - 1, 'e-log-returns the fall 0.0488 is smaller than the rise 0.0513')
X('e-log-returns', 'explain.text', round(math.exp(tue) - 1, 4))
X('e-log-returns', 'explain.text', round(math.exp(mon) - 1, 4))
X('e-log-returns', 'feedback.byKey.flip', round(math.exp(mon) - 1, 4))

# ---------------------------------------------------------------- e-two-u-minus-v
uu, vv = (3, -1), (2, 4)
w2 = (2 * uu[0] - vv[0], 2 * uu[1] - vv[1])
key('e-two-u-minus-v', math.hypot(*w2), t=0.0012)
ex.claim(w2 == (4, -6) and w2[0] ** 2 + w2[1] ** 2 == 52, 'e-two-u-minus-v 2u - v = (4, -6), squared length 52')
ex.claim(52 == 4 * 13 and near(math.sqrt(52), 2 * math.sqrt(13), 1e-12), 'e-two-u-minus-v sqrt(52) = 2 sqrt(13) (finding 29)')
ex.claim('2√13' in IT['e-two-u-minus-v']['widget']['accept'], 'e-two-u-minus-v accept line names 2 sqrt(13)')
inband('e-two-u-minus-v', 7.21, 'typed 7.21')
wrong('e-two-u-minus-v', 'mags', 2 * math.hypot(*uu) - math.hypot(*vv))
wrong('e-two-u-minus-v', 'plus', math.hypot(2 * uu[0] + vv[0], 2 * uu[1] + vv[1]))
wrong('e-two-u-minus-v', 'abs-sum', abs(w2[0]) + abs(w2[1]))

# ---------------------------------------------------------------- e-tan-third-quadrant (tan = 15/8, find cos - sin; finding 9)
ex.claim(15 ** 2 + 8 ** 2 == 17 ** 2 and 64 + 225 == 289, 'e-tan-third-quadrant 8, 15, 17 triangle: 64 + 225 = 289 = 17^2')
theta = 180 + math.degrees(math.atan(15 / 8))
ex.claim(180 < theta < 270 and near(math.tan(math.radians(theta)), 15 / 8, 1e-12), f'e-tan-third-quadrant theta = {theta:.3f} degrees, tan 15/8')
cth, sth = math.cos(math.radians(theta)), math.sin(math.radians(theta))
ex.claim(near(cth, -8 / 17, 1e-12) and near(sth, -15 / 17, 1e-12), 'e-tan-third-quadrant cos -8/17 and sin -15/17 from the angle')
key('e-tan-third-quadrant', cth - sth)
ex.claim(F(-8, 17) - F(-15, 17) == F(7, 17), 'e-tan-third-quadrant cos - sin = 7/17 exactly')
wrong('e-tan-third-quadrant', 'sign', 8 / 17 - 15 / 17)
wrong('e-tan-third-quadrant', 'second', -8 / 17 - 15 / 17)
wrong('e-tan-third-quadrant', 'fourth', 8 / 17 + 15 / 17)
inband('e-tan-third-quadrant', 0.4118, 'typed 0.4118')
inband('e-tan-third-quadrant', 0.4117, 'typed 0.4117', want=False)
X('e-tan-third-quadrant', 'explain.text', 225)
X('e-tan-third-quadrant', 'explain.text', 17)

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
ex.claim('Its sum to infinity is' in IT['e-perpetuity-now']['explain']['text'] and 'Its sum is' not in IT['e-perpetuity-now']['explain']['text'],
         'e-perpetuity-now explain says "sum to infinity", as series l8 does (finding 28)')
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
ex.claim('\\vec{' not in json.dumps(IT['e-vector-ratio']) and '\\overrightarrow{OX}' in json.dumps(IT['e-vector-ratio']), 'e-vector-ratio writes \\overrightarrow, as counting l9 and l12 do (finding 27)')

# ---------------------------------------------------------------- e-code-repeat (four different characters, at least one letter; finding 7)
chars = '0123456789ABCDEF'
codes = list(itertools.product(chars, repeat=4))
letter = lambda c: any(ch in 'ABCDEF' for ch in c)
good = sum(1 for c in codes if len(set(c)) == 4 and letter(c))
key('e-code-repeat', good)
digits_only = sum(1 for c in codes if len(set(c)) == 4 and not letter(c))
ex.claim(good == 16 * 15 * 14 * 13 - 10 * 9 * 8 * 7 and digits_only == 5040 and len(codes) == 65536, 'e-code-repeat enumeration 38640 = 43680 - 5040 of 65,536 codes')
wrong('e-code-repeat', 'distinct', sum(1 for c in codes if len(set(c)) == 4))
wrong('e-code-repeat', 'repeat-ok', sum(1 for c in codes if letter(c)))
wrong('e-code-repeat', 'total-minus', 16 ** 4 - 5040)
ex.claim(sum(1 for c in codes if letter(c)) == 16 ** 4 - 10 ** 4, 'e-code-repeat repeat-ok slip: 16^4 - 10^4 = 55536')
X('e-code-repeat', 'explain.text', 43680)
X('e-code-repeat', 'explain.text', 5040)
X('e-code-repeat', 'feedback.correct', 5040)

# ---------------------------------------------------------------- e-accounts-meet (bisection and logs; finding 24)
lo, hi = 0.0, 50.0
for _ in range(200):
    mid = (lo + hi) / 2
    if 1000 * math.exp(0.05 * mid) < 1200 * math.exp(0.03 * mid):
        lo = mid
    else:
        hi = mid
tm = math.log(1.2) / 0.02
ex.claim(near(lo, tm, 1e-9), f'e-accounts-meet bisection {lo:.6f} = ln 1.2 / 0.02')
key('e-accounts-meet', 9.1161, t=1e-9)
ex.claim(near(IT['e-accounts-meet']['widget']['answer'], tm, 1e-4) and IT['e-accounts-meet']['widget']['tol']['abs'] == 0.005,
         'e-accounts-meet stores the unrounded 9.1161 with tol 0.005 (finding 24)')
X('e-accounts-meet', 'explain.text', round(math.log(1.2), 4))
X('e-accounts-meet', 'explain.text', round(1000 * math.exp(0.05 * tm)))
wrong('e-accounts-meet', 'add', math.log(1.2) / 0.08)
wrong('e-accounts-meet', 'simple', 200 / (50 - 36))
inband('e-accounts-meet', 9.12, 'typed 9.12')
inband('e-accounts-meet', 9.11, 'typed 9.11 (true 9.1161; finding 24)', want=False)
inband('e-accounts-meet', 9.13, 'typed 9.13', want=False)

# ---------------------------------------------------------------- e-loan-payment (first payment today; finding 8)
pay = 10000 / sum(1.05 ** -k for k in range(10))
ex.claim(near(pay, 10000 * 0.05 / (1.05 * (1 - 1.05 ** -10)), 1e-9), f'e-loan-payment sum of ten values today and the closed form agree: {pay:.4f}')
key('e-loan-payment', round(pay, 2), t=1e-9)
ex.claim(near(IT['e-loan-payment']['widget']['answer'], pay, IT['e-loan-payment']['widget']['tol']['abs']),
         f'e-loan-payment stored 1233.38 is within its 0.005 of the unrounded {pay:.4f} (finding 24)')
balance = 10000.0
for i in range(10):
    if i:
        balance *= 1.05
    balance -= round(pay, 2)
ex.claim(abs(balance) < 0.10 and near(balance, -0.04, 0.005), f'e-loan-payment paying £1,233.38 from today leaves {balance:.4f} after the tenth payment')
end_pay = 10000 * 0.05 / (1 - 1.05 ** -10)
ex.claim(near(end_pay / 1.05, pay, 1e-9) and round(end_pay, 2) == 1295.05, 'e-loan-payment 1295.05 (end of year) divided by 1.05 gives the payment from today')
inband('e-loan-payment', 1233.38, 'typed 1233.38')
inband('e-loan-payment', 1233.37, 'truncated 1233.37 (true 1233.377; finding 24)', want=False)
wrong('e-loan-payment', 'end', end_pay)
wrong('e-loan-payment', 'no-interest', 1000)
wrong('e-loan-payment', 'simple', 1000 + 500)
wrong('e-loan-payment', 'future', round(10000 * 1.05 ** 10 / 10, 2), t=1e-9)
X('e-loan-payment', 'explain.text', 1295.05)
X('e-loan-payment', 'explain.text', 1.05)

# ---------------------------------------------------------------- freshness (findings 2 to 20)
# (item, phrases that made up the repeated setup, where): the rewrite must no longer contain all of them.
REPEATS = [
    ('e-years-to-target', ('5,000', '8,000', '6%'), 'exp-log review-2 items[6]: £5,000.00 at 6% first above £8,000.00, answer 9'),
    ('e-desk-block', ('Two of them, Priya and Tom',), 'counting l6 quiz[0]: six people in a row, two side by side, 240'),
    ('e-double-angle-solve', ('2x', '0^\\circ \\le x'), 'trig l11 screens[7]: solve sin 2x = 0.5 on 0 to 360 with u = 2x'),
    ('e-tech-pick', ('10 shares', '4 of them', 'pick 3', 'exactly 2'), 'mock-oa-trader-2 b09-committee: 10 with 4 marked, team of 3, exactly 2'),
    ('e-geom-eighth', ('7, 14, 28, 56',), 'series l3 screens[4] (3, 6, 12, 24, u_8) and mock-oa-trader-2 a02-geometric (7, 14, 28, 56)'),
    ('e-code-repeat', ('4 characters', 'at least one character repeated'), 'counting homework-2 h-pin-repeat: 4-digit PIN, at least one repeat'),
    ('e-loan-payment', ('£10,000', 'equal payments', 'end of each year'), 'series homework-3 items[7]: £10,000 loan, equal end-of-year payments'),
    ('e-cosine-rule', ('60^\\circ', '5 km', '8 km'), 'trig l5 quiz[0] (6 and 8 at 60) and homework-1 items[6] (5 km and 8 km)'),
    ('e-continuous-four', ('continuous rate', 'for 4 years'), 'exp-log l9 quiz[0] and screens[5]: a sum at a continuous rate for t years'),
    ('e-log-returns', ('daily log returns over three days',), 'exp-log l11 quiz[1] (three daily log returns) with screens[5] (e^x - 1)'),
    ('e-fraction-powers', ('27^{2/3}',), 'exp-log l3 screens[7]: which value is 27^{2/3}'),
    ('e-arc-length', ('2.5 radians',), 'trig homework-2 items[1] (a wheel turns through 2.5 radians) and l7 quiz[2]'),
    ('e-log-thousandth', ('\\log_{10} 0.001',), 'exp-log l7 quiz[0]: what is log 0.01'),
    ('e-four-falls', ('4 days in a row',), 'exp-log l2 screens[6]: falls 10% every day for 10 days'),
    ('e-weekly-savings', ('£20 in week 1', '£5 more each week'), 'series l5 screens[1]: save £3 in week 1, then £2 more each week'),
    ('e-binomial-cube', ('coefficient of $x^3$',), 'series l11 quiz[0]: the number in front of x^3 in (x + 2)^5'),
    ('e-sigma-odd', ('(2k - 1)',), 'series l5 quiz[2]: sum of (2k - 1)'),
]
for iid, phrases, where in REPEATS:
    ex.claim(not has(iid, *phrases), f'{iid} fresh against {where}')
ex.claim(not has('e-tan-third-quadrant', '\\cos\\theta = -', head=True) and has('e-tan-third-quadrant', '\\tan\\theta = \\tfrac{15}{8}', head=True),
         'e-tan-third-quadrant fresh: given tan and the quadrant, not cos and the quadrant (trig l10 quiz[0], quiz[2], homework-2 items[3])')
ex.claim(IT['e-wave-fit']['canvas']['params']['functions'][0]['expr'].startswith('-3*sin') and 'Which equation fits the graph' in IT['e-wave-fit']['question'],
         'e-wave-fit fresh: a falling wave (a = -3), not the rising 3 sin(pi x / 6) + 5 of trig review-2, l8, l9, l11, l13')
# The new setups are present.
NEW = [
    ('e-years-to-target', ('£18,000', '12%', '£5,000')), ('e-desk-block', ('Sam must not sit at either end',)),
    ('e-double-angle-solve', ('\\cos 3x', '180^\\circ')), ('e-tech-pick', ('12 shares', '5 of them tech', '4 at random')),
    ('e-geom-eighth', ('3rd term 12', '6th term 96', '10th term')), ('e-code-repeat', ('four different characters', 'at least one letter')),
    ('e-loan-payment', ('The first payment is today',)), ('e-cosine-rule', ('120^\\circ', '3 km', '5 km')),
    ('e-continuous-four', ('5% a year for 2 years', '3% a year for 3 more years')), ('e-log-returns', ('Monday', 'Tuesday', 'opening price')),
    ('e-fraction-powers', ('125^{2/3}', '625^{-1/4}')), ('e-arc-length', ('radius 6 cm', '1.8 radians')),
    ('e-log-thousandth', ('\\log_4 0.0625',)), ('e-four-falls', ('then rises 3% a day',)),
    ('e-weekly-savings', ('£2,775', 'fixed amount more')), ('e-binomial-cube', ('(1 + ax)^6', '135')),
    ('e-sigma-odd', ('\\sum_{k=5}^{20} (3k + 2)',)), ('e-truss-angle', ('roof truss', '10 m', '7 m')),
]
for iid, phrases in NEW:
    ex.claim(has(iid, *phrases), f'{iid} carries its new setup {phrases}')

# ---------------------------------------------------------------- wrong values against the answer bands (rule 581)
ex.check_wrongs()
ex.report()
