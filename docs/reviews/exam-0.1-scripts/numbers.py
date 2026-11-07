"""Second reader's number script for app/content/exams/topic-0.1.json (review-exam-0.1.md).

Recomputes every graded key and every wrong[] value with exact fractions, every number in prose, feedback, why lines and
explanations, the order and choice keys, and the typed forms a learner would enter (fractions, mixed numbers, a trailing %,
a leading £, thousands commas), parsed as app/js/engine/grade.js parseNum and numeric.js do.
A check that fails because the content is wrong stays failing; each such check is a finding in the review:
  - "taught" checks pass once the item no longer needs an idea that number-sense and ratio do not teach
    (findings 1 to 4, and the word "terminating" in finding 9);
  - one grading check (finding 5: a wrongly rounded 1.34 graded right);
  - "fresh" checks pass once the repeated setup is gone (findings 6 to 13);
  - one claim_text check passes once the sentence is reworded (finding 16).
Pure standard library. Run: python3 docs/reviews/exam-0.1-scripts/numbers.py
"""
import os
import sys

# This file is named numbers.py, which shadows the standard library's `numbers` (fractions imports it).
# Drop the script's own folder from the path before any other import.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or os.getcwd()) != HERE]

import glob  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
from fractions import Fraction as F  # noqa: E402

sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk  # noqa: E402

ROOT = os.path.join(HERE, '..', '..', '..', 'app', 'content')
EXAM = os.path.join(ROOT, 'exams', 'topic-0.1.json')


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


def half(tol):
    t = {'abs': tol} if isinstance(tol, (int, float)) else (tol or {'abs': 0})
    return t.get('abs', 0) + 1e-9


def key(iid, value, path='widget'):
    """The graded answer equals the exact recomputed value (within float noise)."""
    w = node(f'{P(iid)}.{path}')
    ok = abs(w['answer'] - float(value)) <= 1e-9 * max(1, abs(float(value)))
    ex._rec(ok, f'{iid} {path} answer {w["answer"]!r} = {float(value):.10g}', '' if ok else 'recomputed value differs')


def wrong(iid, wid, value, path='widget'):
    w = node(f'{P(iid)}.{path}')
    v = next((x for x in w.get('wrong', []) if x.get('id') == wid), None)
    if v is None:
        return ex._rec(False, f'{iid} wrong "{wid}" exists', 'no such wrong id')
    ok = abs(v['value'] - float(value)) <= 1e-6 * max(1, abs(float(value)))
    ex._rec(ok, f'{iid} wrong "{wid}" {v["value"]!r} = {float(value):.10g}', '' if ok else 'recomputed slip differs')


def parse(t, pct_unit=False):
    """grade.js parseNum plus numeric.js's unit-% rule."""
    s = t.strip().replace('−', '-')
    m = re.match(r'^(-?\d+)\s+(\d+)/(\d+)$', s)
    if m:
        a, b, c = int(m[1]), int(m[2]), int(m[3])
        v = (a + (1 if a >= 0 else -1) * b / c)
        return v / 100 if pct_unit else v
    v = re.sub(r'\s+', '', s)
    v = re.sub(r'^[£$€]', '', v)
    if re.match(r'^-?\d{1,3}(,\d{3})+(\.\d+)?$', v):
        v = v.replace(',', '')
    pct = v.endswith('%')
    if pct:
        v = v[:-1]
    m = re.match(r'^(-?\d+(?:\.\d+)?)/(-?\d+(?:\.\d+)?)$', v)
    n = float(m[1]) / float(m[2]) if m else float(v)
    if pct or pct_unit:
        n /= 100
    return n


def typed(iid, text, expect, path='widget'):
    """What a typed answer grades as: 'right', a wrong id, or 'generic'."""
    w = node(f'{P(iid)}.{path}')
    v = parse(text, w.get('unit') == '%' and '%' not in text)
    if abs(v - w['answer']) <= half(w.get('tol')):
        got = 'right'
    else:
        got = next((x['id'] for x in w.get('wrong', []) if abs(v - x['value']) <= half(x.get('tol', {'abs': 1e-9}))), 'generic')
    ex._rec(got == expect, f'{iid} typed {text!r} grades {expect}', '' if got == expect else f'grades {got}')


def cell(iid, r, c, value, typed_ok=(), typed_bad=()):
    w = node(f'{P(iid)}.widget')
    cl = w['rows'][r][c]
    ok = abs(cl['answer'] - float(value)) <= 1e-9 * max(1, abs(float(value)))
    ex._rec(ok, f'{iid} r{r}c{c} answer {cl["answer"]!r} = {float(value):.10g}', '' if ok else 'recomputed value differs')
    for t in typed_ok:
        g = abs(parse(t) - cl['answer']) <= half(cl.get('tol'))
        ex._rec(g, f'{iid} r{r}c{c} typed {t!r} graded right', '' if g else 'outside the tolerance')
    for t in typed_bad:
        g = abs(parse(t) - cl['answer']) > half(cl.get('tol'))
        ex._rec(g, f'{iid} r{r}c{c} typed {t!r} (a wrong answer at the precision asked) graded wrong',
                '' if g else 'graded right: the tolerance is wider than the rounding asked for')


def correct_ids(iid):
    return sorted(o['id'] for o in IT[iid]['widget']['options'] if o.get('correct'))


def say(iid, path, value, fmt=None):
    ex.expect('exam', f'{P(iid)}.{path}', value, fmt=fmt)


def terminates(fr):
    d = fr.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def course_text(course, pattern):
    """Every string of a course's lessons, reviews and homework that matches a regular expression."""
    out = []
    for f in glob.glob(os.path.join(ROOT, 'courses', course, '*.json')):
        if f.endswith('course.json'):
            continue
        out += re.findall(pattern, open(f, encoding='utf8').read())
    return out


def _texts(n):
    if isinstance(n, str):
        return [n]
    if isinstance(n, dict):
        return [s for v in n.values() for s in _texts(v)]
    if isinstance(n, list):
        return [s for v in n for s in _texts(v)]
    return []


def exam_has(iid, pattern):
    """Search the item's raw strings (not json.dumps, which doubles every backslash)."""
    return any(re.search(pattern, s) for s in _texts(IT[iid]))


def taught(iid, exam_pattern, course, course_pattern, label):
    """While the item still uses the idea (exam_pattern), the course must teach it (course_pattern)."""
    if not exam_has(iid, exam_pattern):
        return ex._rec(True, f'{iid} taught: {label}', 'the item no longer uses it')
    ok = bool(course_text(course, course_pattern))
    ex._rec(ok, f'{iid} taught: {label}', '' if ok else f'not taught in {course}')


def fresh(iid, exam_pattern, label):
    """A marker of a repeated lesson, review or homework setup: passes once the item no longer carries it."""
    ok = not exam_has(iid, exam_pattern)
    ex._rec(ok, f'{iid} fresh: {label}', '' if ok else 'repeats the setup')


# ---------------------------------------------------------------- [0] e-mixed-subtract
a, b = F(10, 3), F(7, 4)
key('e-mixed-subtract', a - b)                                   # 19/12
ex.claim(a - b == F(19, 12) == 1 + F(7, 12), 'e-mixed-subtract 19/12 = 1 7/12')
wrong('e-mixed-subtract', 'smaller-from-larger', (3 - 1) + (F(3, 4) - F(1, 3)))   # 2 5/12
say('e-mixed-subtract', 'explain.text', 10)
say('e-mixed-subtract', 'explain.text', 7)
ex.claim(F(10, 3) == F(40, 12) and F(7, 4) == F(21, 12), 'e-mixed-subtract 40/12 and 21/12')
for t in ('19/12', '1 7/12', '38/24', '1.583'):
    typed('e-mixed-subtract', t, 'right')
typed('e-mixed-subtract', '2 5/12', 'smaller-from-larger')
typed('e-mixed-subtract', '29/12', 'smaller-from-larger')

# ---------------------------------------------------------------- [1] e-percent-build
key('e-percent-build', F(39, 100) * 360)                         # 140.4
wrong('e-percent-build', 'tenth', F(39, 1000) * 360)             # 14.04 = 3.9%
wrong('e-percent-build', 'forty', F(40, 100) * 360)              # 144
wrong('e-percent-build', 'added-one', F(40, 100) * 360 + F(1, 100) * 360)   # 147.6
say('e-percent-build', 'feedback.correct', 144)
say('e-percent-build', 'feedback.correct', 3.6)
say('e-percent-build', 'explain.text', 36)
say('e-percent-build', 'explain.text', 144)
say('e-percent-build', 'explain.text', 3.6)
say('e-percent-build', 'explain.text', 140.4)
say('e-percent-build', 'feedback.byKey.tenth', 3.9)
ex.claim(F(144) - F(36, 10) == F(1404, 10) == F(39, 100) * 360, 'e-percent-build 144 - 3.60 = 140.40')
for t in ('140.4', '£140.40', '140.40'):
    typed('e-percent-build', t, 'right')
typed('e-percent-build', '14.04', 'tenth')
typed('e-percent-build', '144', 'forty')
typed('e-percent-build', '147.6', 'added-one')
fresh('e-percent-build', r'35%', 'ratio review-1 items[1] asks "What is 35% of £120?"')

# ---------------------------------------------------------------- [2] e-pnl-close
w2 = IT['e-pnl-close']['widget']
ex.claim(w2['points'][0]['target'] == -3 - 5, 'e-pnl-close target -3 - 5 = -8')
ex.claim(w2['wrong'][0]['region']['x'][0] < -3 + 5 < w2['wrong'][0]['region']['x'][1], 'e-pnl-close "rose" region holds -3 + 5 = 2')
ex.claim(w2['wrong'][1]['region']['x'][0] < 3 - 5 < w2['wrong'][1]['region']['x'][1], 'e-pnl-close "ignored-start" region holds 3 - 5 = -2')
cv = IT['e-pnl-close']['canvas']['params']
ex.claim(cv['min'] <= -8 <= cv['max'] and cv['min'] <= 2 <= cv['max'], 'e-pnl-close line -10 to 4 holds the key and the slip')
ex.claim(all(abs(t - w2['points'][0]['target']) > w2['points'][0]['tol'] for r in (w2['wrong'][0], w2['wrong'][1]) for t in r['region']['x']),
         'e-pnl-close slip regions clear of the key tolerance')

# ---------------------------------------------------------------- [3] e-decimal-order
w3 = IT['e-decimal-order']['widget']
vals = {ln['id']: float(ln['text'].replace('£', '')) for ln in w3['lines']}
ex.claim(w3['answer'] == sorted(vals, key=vals.get), 'e-decimal-order answer is smallest first')
ex.claim(len(set(vals.values())) == len(vals), 'e-decimal-order no ties')
say('e-decimal-order', 'explain.text', '0.0455 has 4 hundredths and 0.054 has 5')

# ---------------------------------------------------------------- [4] e-ratio-units
ex.claim(correct_ids('e-ratio-units') == ['a'], 'e-ratio-units key a')
g = math.gcd(math.gcd(120, 45), 15)
ex.claim((120 // g, 45 // g, 15 // g) == (8, 3, 1) and g == 15, 'e-ratio-units 120 : 45 : 15 = 8 : 3 : 1, HCF 15')
ex.claim(F(12, 10) * 100 == 120, 'e-ratio-units £1.20 is 120p')
ex.claim(F(12, 10) * 20 == 24 and F(45) * 20 == 900 and F(15) * 20 == 300 and (24 // 12, 900 // 12, 300 // 12) == (2, 75, 25),
         'e-ratio-units option b 1.20 : 45 : 15 = 24 : 900 : 300 = 2 : 75 : 25')
ex.claim(math.gcd(math.gcd(24, 9), 3) == 3 and (24 // 3, 9 // 3, 3 // 3) == (8, 3, 1), 'e-ratio-units option d 24 : 9 : 3 shares a factor of 3')
ex.claim((1, 3, 8)[::-1] == (8, 3, 1), 'e-ratio-units option c is the reverse of 8 : 3 : 1')
fresh('e-ratio-units', r'price : dividend', 'ratio l10 quiz[0]: mixed units to simplest form, with unconverted, unsimplified and reversed distractors')
fresh('e-ratio-units', r'2\.40', 'the two-part price and dividend setup')

# ---------------------------------------------------------------- [5] e-tranches
cnt = F(9, 2) / F(5, 8)                                          # 36/5 = 7 1/5
full = cnt.numerator // cnt.denominator                          # 7
left = F(9, 2) - full * F(5, 8)
key('e-tranches', left)                                          # 1/8
ex.claim(cnt == F(36, 5) == 7 + F(1, 5) and full == 7, 'e-tranches 9/2 x 8/5 = 36/5 = 7 1/5, 7 full tranches')
ex.claim(full * F(5, 8) == F(35, 8) == 4 + F(3, 8), 'e-tranches 7 x 5/8 = 35/8 = 4 3/8')
ex.claim(F(9, 2) == 4 + F(4, 8) and 4 + F(4, 8) - (4 + F(3, 8)) == F(1, 8) == F(1, 5) * F(5, 8), 'e-tranches 4 4/8 - 4 3/8 = 1/8, and 1/5 of a tranche agrees')
wrong('e-tranches', 'tranche-share', F(1, 5))
wrong('e-tranches', 'count', full)
wrong('e-tranches', 'count-exact', cnt)
wrong('e-tranches', 'multiplied', F(9, 2) * F(5, 8))             # 45/16
ex.claim(F(1, 8) * 1_000_000 == 125_000, 'e-tranches 1/8 million is £125,000')
for t, e in (('1/8', 'right'), ('0.125', 'right'), ('125/1000', 'right'), ('1/5', 'tranche-share'), ('7', 'count'), ('7.2', 'count-exact'),
             ('36/5', 'count-exact'), ('45/16', 'multiplied')):
    typed('e-tranches', t, e)
fresh('e-tranches', r'How many tranches does it fill', 'number-sense homework-1 items[4] divides a mixed number by a fraction to a whole answer (2 1/2 / 5/8 = 4)')
ex.claim(not exam_has('e-tranches', r'tranches of £\$\\tfrac\{3\}\{8\}'), 'e-tranches no longer divides by 3/8 to a whole 12')

# ---------------------------------------------------------------- [6] e-terminating
opts6 = {'a': F(13, 80), 'b': F(9, 75), 'c': F(21, 56), 'd': F(7, 24), 'e': F(11, 30)}
ex.claim(correct_ids('e-terminating') == sorted(k for k, v in opts6.items() if terminates(v)), 'e-terminating keys are the terminating fractions')
ex.claim(F(9, 75) == F(3, 25) and F(21, 56) == F(3, 8), 'e-terminating explain 9/75 = 3/25, 21/56 = 3/8')
ex.claim(F(13, 80) == F(1625, 10000) and 80 == 2 ** 4 * 5 and math.gcd(13, 80) == 1, 'e-terminating 13/80 = 0.1625, 80 = 2^4 x 5, lowest terms')
ex.claim(f'{7 / 24:.6f}' == '0.291667' and math.gcd(7, 24) == 1 and 24 == 8 * 3 and not terminates(F(7, 24)),
         'e-terminating 7/24 = 0.291666..., 24 = 8 x 3, lowest terms, recurs')
ex.claim(f'{11 / 30:.6f}' == '0.366667' and F(11, 30).denominator == 30 and not terminates(F(11, 30)),
         'e-terminating 11/30 = 0.3666..., already in lowest terms, so its 3 stays')
ex.claim(24 % 3 == 0 and 30 % 3 == 0, 'e-terminating explain: 24 and 30 keep a factor of 3')
fresh('e-terminating', r'\{7\}\{40\}', 'number-sense fractions-to-decimals lesson screens[9]: "Which fraction gives a decimal that stops?", key 7/40, distractor 5/12')
fresh('e-terminating', r'\{5\}\{12\}', 'the lesson screens[9] distractor 5/12')
ex.claim(exam_has('e-terminating', r'called a terminating decimal'), 'e-terminating defines the word "terminating" where it first uses it')

# ---------------------------------------------------------------- [7] e-tick-count
n7 = F(6 * 10**5) / F(8, 1000)
ex.claim(n7 == 75_000_000, 'e-tick-count 6e5 / 8e-3 = 7.5e7')
ex.claim(correct_ids('e-tick-count') == ['a'], 'e-tick-count key a (7.5 x 10^7)')
ex.claim(F(75, 100) * 10**8 == n7 and F(75, 10) * 10**9 == 100 * n7, 'e-tick-count option b equals the count but is not standard form; c is 100 times too big')
ex.claim(F(6, 8) * 10**(5 + (-3)) == F(75, 10) * 10**1, 'e-tick-count option d = adding the powers, 0.75 x 10^2 = 7.5 x 10^1')
ex.claim(5 - (-3) == 8, 'e-tick-count why: 5 - (-3) = 8')

# ---------------------------------------------------------------- [8] e-fraction-power
ex.claim(F(2, 3) ** 3 == F(8, 27), 'e-fraction-power the cube root of 8/27 is 2/3 (2/3 cubed = 8/27)')
key('e-fraction-power', F(2, 3) ** 2)                            # 4/9
wrong('e-fraction-power', 'top-only', F(2 ** 2, 27))     # root and square taken on the 8 only
wrong('e-fraction-power', 'doubled', F(2, 3) * 2)
wrong('e-fraction-power', 'no-root', F(8, 27) ** 2)
ex.claim(F(2, 3) * F(2, 3) == F(4, 9) and 3 ** 3 == 27, 'e-fraction-power 2/3 x 2/3 = 4/9, 3^3 = 27')
for t, e in (('4/9', 'right'), ('0.444', 'right'), ('0.4444', 'right'), ('4/27', 'top-only'), ('4/3', 'doubled'), ('64/729', 'no-root')):
    typed('e-fraction-power', t, e)
ex.claim(not exam_has('e-fraction-power', r'frac\{2\}\{3\}\}\\right\)') and not exam_has('e-fraction-power', r'\^\{-\\frac'),
         'e-fraction-power no longer uses a fractional or negative fractional index')
taught('e-fraction-power', r'\^\{-\\frac\{2\}\{3\}\}', 'number-sense', r'\^\{\\[dt]?frac|\^\{-\\[dt]?frac|fractional (power|index)',
       'a fractional index (taught first in exp-log, topic 0.3)')

# ---------------------------------------------------------------- [9] e-operation-order
key('e-operation-order', 20 - F(4 * (1 - 4) ** 2, 6))            # 14
wrong('e-operation-order', 'left-to-right', F((20 - 4) * (1 - 4) ** 2, 6))   # 24
wrong('e-operation-order', 'negative-square', 20 - F(4 * -9, 6))  # 26
say('e-operation-order', 'explain.text', 6)
say('e-operation-order', 'explain.text', 14)
say('e-operation-order', 'feedback.byKey.negative-square', -9)

# ---------------------------------------------------------------- [10] e-estimate
est = F(10) * F(5, 100) / F(2, 1000)
ex.claim(est == 250 and correct_ids('e-estimate') == ['a'], 'e-estimate 10 x 0.05 / 0.002 = 250, key a')
ex.claim(F(9) * F(5, 100) / F(2, 1000) == F(225), 'e-estimate option b: 9.62 rounded down to 9 gives 225')
ex.claim(F(10) * F(5, 10) / F(2, 1000) == 2500, 'e-estimate option c: 0.0487 rounded to 0.5 gives 2500')
ex.claim(F(10) * F(5, 100) * F(2, 1000) == F(1, 1000), 'e-estimate option d: multiplying by 0.002 gives 0.001')
ex.claim(F(10) * F(5, 100) == F(1, 2), 'e-estimate 10 x 0.05 = 0.5')
exact10 = 9.62 * 0.0487 / 0.00213
ex.claim(round(exact10, -1) == 220, f'e-estimate explain "about 220" ({exact10:.2f})')
fresh('e-estimate', r'0\.198', 'number-sense estimating lesson screens[5] estimates (38.7 x 5.12) / 0.198, the same three-number shape and denominator')
fresh('e-estimate', r'587', 'the old 587 numerator')

# ---------------------------------------------------------------- [11] e-before-fall
mult = F(85, 100) * F(120, 100)                                  # 1.02
ex.claim(mult == F(102, 100), 'e-before-fall 0.85 x 1.2 = 1.02')
key('e-before-fall', F(306) / mult)                              # 300
wrong('e-before-fall', 'net-five', F(306) / F(105, 100))         # 291.428571
wrong('e-before-fall', 'one-move', F(306) / F(85, 100))          # 360
wrong('e-before-fall', 'net-five-off', F(306) * F(95, 100))      # 290.7
wrong('e-before-fall', 'reapplied', F(306) * mult)               # 312.12
ex.claim(F(300) * F(85, 100) == 255 and F(255) * F(12, 10) == 306, 'e-before-fall check: 300 falls to 255, a 20% rise gives 306')
say('e-before-fall', 'explain.text', 255)
for t, e in (('300', 'right'), ('£300', 'right'), ('291.43', 'net-five'), ('360', 'one-move'), ('290.7', 'net-five-off'), ('312.12', 'reapplied')):
    typed('e-before-fall', t, e)
fresh('e-before-fall', r'After a 15% fall', 'ratio review-2 items[1] (after 15% off, £68, same two slips) and the before-the-discount lesson quiz[2] (after a 75% fall)')

# ---------------------------------------------------------------- [12] e-three-moves
m12 = F(70, 100) * F(120, 100) * F(125, 100)
key('e-three-moves', m12 - 1)                                    # 0.05
wrong('e-three-moves', 'added', F(-30 + 20 + 25, 100))
wrong('e-three-moves', 'multiplier', m12)                        # 105 typed into a % box
ex.claim(m12 == F(105, 100) and F(70, 100) * F(120, 100) == F(84, 100), 'e-three-moves 0.7 x 1.2 = 0.84, x 1.25 = 1.05')
for t, e in (('5', 'right'), ('5%', 'right'), ('15', 'added'), ('105', 'multiplier'), ('105%', 'multiplier'), ('110', 'generic')):
    typed('e-three-moves', t, e)
fresh('e-three-moves', r'rises 25%,? (and )?then falls 20%', 'ratio up-then-down lesson quiz[3]: "rises 25% and then falls 20%", ending back at the start')
fresh('e-three-moves', r'cancel exactly', 'the old explain: the first two moves cancel')

# ---------------------------------------------------------------- [13] e-ratio-gap
part = F(960, 6 - 2)                                             # 240
key('e-ratio-gap', part * 11)                                    # 2640
wrong('e-ratio-gap', 'a-minus-b', F(960, 6 - 3) * 11)            # 3520
wrong('e-ratio-gap', 'gap-as-share', F(960, 6) * 11)             # 1760
wrong('e-ratio-gap', 'gap-as-total', 960)
wrong('e-ratio-gap', 'two-desks', part * (6 + 2))                # 1920
ex.claim(part == 240 and part * 6 == 1440 and part * 3 == 720 and part * 2 == 480 and 1440 - 480 == 960 and 1440 + 720 + 480 == 2640,
         'e-ratio-gap explain: part 240, shares 1,440, 720 and 480, A - C = 960')
say('e-ratio-gap', 'explain.text', 1440)
say('e-ratio-gap', 'explain.text', 720)
say('e-ratio-gap', 'explain.text', 480)
say('e-ratio-gap', 'explain.text', 2640)
for t, e in (('2,640', 'right'), ('£2,640', 'right'), ('3520', 'a-minus-b'), ('1760', 'gap-as-share'), ('960', 'gap-as-total'), ('1920', 'two-desks')):
    typed('e-ratio-gap', t, e)
fresh('e-ratio-gap', r'7 : 4', 'ratio homework-3 items[0]: a bonus pool in the ratio 7 : 4, the larger share £1,260 more, find the whole pool')

# ---------------------------------------------------------------- [14] e-two-currencies
usd, eur = F(125, 100), F(115, 100)
cell('e-two-currencies', 0, 1, F(500) / usd, typed_ok=('400', '400.00'))
cell('e-two-currencies', 0, 2, F(500) / usd * eur, typed_ok=('460',))
cell('e-two-currencies', 1, 1, F(1840) / eur, typed_ok=('1,600', '1600'))
say('e-two-currencies', 'explain.text', 400)
say('e-two-currencies', 'explain.text', 460)
say('e-two-currencies', 'explain.text', 1600)
ex.claim(IT['e-two-currencies']['widget']['rows'][1][0] == '€1,840' and '€1.15' in IT['e-two-currencies']['prose'] and '€1,840 fee' in IT['e-two-currencies']['prose'],
         'e-two-currencies writes euros with the symbol, as the currencies lesson does')

# ---------------------------------------------------------------- [15] e-loss-share
key('e-loss-share', F(85, 1250))                                 # 0.068
wrong('e-loss-share', 'flipped', round(1250 / 85 / 100, 3))      # 14.7% typed as 14.7
wrong('e-loss-share', 'decimal', F(85, 1250) / 100)              # 0.068 typed into a % box
ex.claim(abs(1250 / 85 - 14.70588) < 1e-4, 'e-loss-share 1250 / 85 = 14.706')
for t, e in (('6.8', 'right'), ('6.8%', 'right'), ('14.7', 'flipped'), ('14.71', 'flipped'), ('0.068', 'decimal')):
    typed('e-loss-share', t, e)
ex.claim(F(85, 1250) == F(68, 1000), 'e-loss-share explain 85/1250 = 6.8/100')
ex.claim(F(10, 100) * 1250 == 125 and F(6, 10) < F(85, 125) < F(7, 10) and abs(float(F(85, 125)) - 2 / 3) < 0.02,
         'e-loss-share check: 10% of 1,250 is 125, and 85 is 68% of that, about two thirds')
say('e-loss-share', 'explain.text', 'about two thirds of that')
ex.claim(not exam_has('e-loss-share', r'a bit over half'), 'e-loss-share no longer says "a bit over half"')

# ---------------------------------------------------------------- [16] e-fill-rate
rate = F(1800, 150)
key('e-fill-rate', F(4500) / rate)                               # 375
wrong('e-fill-rate', 'minutes', F(4500) / rate / 60)             # 6.25
ex.claim(rate == 12, 'e-fill-rate 12 shares a second')
for t, e in (('375', 'right'), ('6.25', 'minutes'), ('6 1/4', 'minutes')):
    typed('e-fill-rate', t, e)

# ---------------------------------------------------------------- [17] e-depreciation
key('e-depreciation', F(10240) / F(8, 10) ** 3)                  # 20000
wrong('e-depreciation', 'simple', F(10240) / F(4, 10))           # 25600
wrong('e-depreciation', 'added-back', F(10240) * F(12, 10) ** 3)  # 17694.72
ex.claim([20000 * F(8, 10) ** k for k in range(4)] == [20000, 16000, 12800, 10240], 'e-depreciation check 20,000, 16,000, 12,800, 10,240')
ex.claim(F(8, 10) ** 3 == F(512, 1000), 'e-depreciation 0.8^3 = 0.512')

# ---------------------------------------------------------------- [18] e-inverse-square (now inverse proportion both ways)
k18 = 2 * 12                                                     # xy = 24
ex.claim(k18 == 24, 'e-inverse-square xy = 2 x 12 = 24')
cell('e-inverse-square', 1, 1, F(k18, 3), typed_ok=('8', '8.00'), typed_bad=('8.01', '8.05'))
cell('e-inverse-square', 2, 1, F(k18, 5), typed_ok=('4.8', '24/5', '4 4/5'), typed_bad=('4.81', '4.9'))
cell('e-inverse-square', 3, 0, F(k18, 40), typed_ok=('0.6', '3/5'), typed_bad=('0.61', '0.7'))
ex.claim(F(k18, 5) == F(24, 5) and F(k18, 40) == F(3, 5), 'e-inverse-square 24/5 = 4.8 and 24/40 = 0.6')
ws = {(r, c): IT['e-inverse-square']['widget']['rows'][r][c]['wrong'][0] for r, c in ((1, 1), (2, 1), (3, 0))}
ex.claim(ws[(1, 1)]['id'] == 'direct-3' and abs(ws[(1, 1)]['value'] - 12 * 3 / 2) < 1e-9, 'e-inverse-square direct slip at x = 3: 12 x 3/2 = 18')
ex.claim(ws[(2, 1)]['id'] == 'direct-5' and abs(ws[(2, 1)]['value'] - 12 * 5 / 2) < 1e-9, 'e-inverse-square direct slip at x = 5: 12 x 5/2 = 30')
ex.claim(ws[(3, 0)]['id'] == 'direct-x' and abs(ws[(3, 0)]['value'] - 2 * 40 / 12) < 1e-6, 'e-inverse-square direct slip at y = 40: 2 x 40/12 = 6.666667')
say('e-inverse-square', 'explain.text', 24)
say('e-inverse-square', 'explain.text', 8)
say('e-inverse-square', 'explain.text', 4.8)
say('e-inverse-square', 'explain.text', 0.6)
ex.claim(all(IT['e-inverse-square']['widget']['rows'][r][c]['tol']['abs'] == 0.005 for r, c in ((1, 1), (2, 1), (3, 0))),
         'e-inverse-square every typed cell has tol.abs 0.005, so a wrongly rounded 2 d.p. answer is not graded right')
taught('e-inverse-square', r'square of \$x\$', 'ratio', r'inversely proportional to the square|\\[dt]?frac\{k\}\{x\^2\}',
       'inverse proportion to a square (ratio teaches only y = c/x)')
ex.claim(not exam_has('e-inverse-square', r'square of'), 'e-inverse-square no longer needs the square')

# ---------------------------------------------------------------- [19] e-minus-eight
opts19 = {'a': F(-2) ** 3, 'b': -(F(2) ** 3), 'c': F(-4) ** 2 / F(-2), 'd': -(F(4) ** 2) / F(-2), 'e': -(F(-2) ** 3)}
ex.claim(correct_ids('e-minus-eight') == sorted(k for k, v in opts19.items() if v == -8) == ['a', 'b', 'c'], 'e-minus-eight keys are the options equal to -8')
ex.claim(opts19['c'] == -8 and F(-4) ** 2 == 16, 'e-minus-eight (-4)^2 / (-2) = 16 / (-2) = -8')
ex.claim(opts19['d'] == 8 and -(F(4) ** 2) == -16 and F(-16) / F(-2) == 8, 'e-minus-eight -4^2 / (-2) = -16 / (-2) = 8')
ex.claim(opts19['e'] == 8, 'e-minus-eight -(-2)^3 = 8')
say('e-minus-eight', 'explain.text', 16)
say('e-minus-eight', 'explain.text', -16)
taught('e-minus-eight', r'2\^\{-3\}|\)\^\{-3\}', 'number-sense', r'(?<![0-9])[2-9]\^\{-[0-9]|\)\^\{-[0-9]',
       'a negative power of a base other than 10 (number-sense shows only 10^-n; exp-log, topic 0.3, teaches 2^-3)')
ex.claim(not exam_has('e-minus-eight', r'\^\{-3\}'), 'e-minus-eight no longer uses a negative power')

# ---------------------------------------------------------------- [20] e-chain-ratio
A, B, C = 2 * 4, 3 * 4, 5 * 3                                    # 8 : 12 : 15
key('e-chain-ratio', F(1400 * C, A + B + C))                     # 600
wrong('e-chain-ratio', 'joined', F(1400 * 5, 2 + 3 + 5))         # 700
wrong('e-chain-ratio', 'two-only', F(1400 * 5, 4 + 5))           # 777.78
ex.claim(F(A, B) == F(2, 3) and F(B, C) == F(4, 5) and A + B + C == 35 and F(1400, 35) == 40, 'e-chain-ratio 8 : 12 : 15, 35 parts, £40 a part')

# ---------------------------------------------------------------- [21] e-fund-fees
inv = F(10000) * F(985, 1000)
grown = inv * F(112, 100)
fee = F(20, 100) * (grown - 10000)
key('e-fund-fees', grown - fee)                                  # 10825.6
g2 = F(10000) * F(112, 100)
wrong('e-fund-fees', 'skipped-entry', g2 - F(20, 100) * (g2 - 10000))   # 10960
wrong('e-fund-fees', 'fee-on-growth', grown - F(20, 100) * (grown - inv))  # 10795.6
wrong('e-fund-fees', 'fee-on-all', grown * F(80, 100))           # 8825.6
ex.claim(inv == 9850 and grown == 11032 and fee == F(20640, 100), 'e-fund-fees 9,850 invested, 11,032 grown, fee 206.40')
say('e-fund-fees', 'feedback.correct', 11032)
say('e-fund-fees', 'feedback.correct', 206.40)
say('e-fund-fees', 'explain.text', 1032)
for t, e in (('10825.6', 'right'), ('£10,825.60', 'right'), ('10960', 'skipped-entry'), ('10795.6', 'fee-on-growth'), ('8825.6', 'fee-on-all')):
    typed('e-fund-fees', t, e)

# ---------------------------------------------------------------- [22] e-recurring-proof (now a sum of two recurring decimals)
s22 = F(5, 6) + F(7, 15)
ex.claim(s22 == F(39, 30) == F(13, 10) == F(13, 10) and F(5, 6) == F(25, 30) and F(7, 15) == F(14, 30) and math.gcd(39, 30) == 3,
         'e-recurring-proof 5/6 + 7/15 = 25/30 + 14/30 = 39/30 = 13/10, HCF 3')
ex.claim(f'{5 / 6:.4f}' == '0.8333' and f'{7 / 15:.4f}' == '0.4667' and abs(7 / 15 - 0.46666666) < 1e-7, 'e-recurring-proof 5/6 = 0.8333..., 7/15 = 0.4666...')
ex.claim(0.8333333333 + 0.4666666667 - 1.3 < 1e-9 and F(13, 10) == F(13, 10) and terminates(F(13, 10)) and 10 == 2 * 5, 'e-recurring-proof the sum is 1.3, and 10 = 2 x 5')
ex.claim(F(5 + 7, 6 + 15) == F(12, 21) == F(4, 7) and F(12, 21) != s22, 'e-recurring-proof distractor d1: 12/21 = 4/7, not the sum')
ex.claim(not terminates(F(5, 6)) and not terminates(F(7, 15)) and terminates(s22), 'e-recurring-proof both parts recur but the sum stops (distractor d2 is false)')
w22 = IT['e-recurring-proof']['widget']
ex.claim(w22['answer'] == ['common', 'add', 'cancel', 'rule', 'end'] and w22['distractors'] == ['d1', 'd2'] and 'same' not in w22,
         'e-recurring-proof order, distractors, and no same group')
ex.claim(all(next(l for l in w22['lines'] if l['id'] == d).get('why') for d in w22['distractors']), 'e-recurring-proof every distractor has a why')
say('e-recurring-proof', 'explain.text', 39)
say('e-recurring-proof', 'explain.text', 13)
ex.claim(not exam_has('e-recurring-proof', r'1000x|990x|\\dot'), 'e-recurring-proof no longer needs the multiply-and-subtract method or dot notation')
taught('e-recurring-proof', r'1000x', 'number-sense', r'1000x|100x|99x|990x',
       'turning a recurring decimal into a fraction by subtracting multiples')
taught('e-recurring-proof', r'\\dot\{3\}\\dot\{6\}', 'number-sense', r'\\dot\{[0-9]\}[0-9]*\\dot',
       'dot notation over a block of two or more digits (the course shows only 0.\\dot{3})')

# ---------------------------------------------------------------- metadata, ramp, skills
items = doc['items']
ramp = [sum(1 for it in items if it['difficulty'] == d) for d in (2, 3, 4, 5)]
ex.claim(20 <= len(items) <= 30, f'{len(items)} items, within 20 to 30')
ex.claim(ramp == [5, 12, 4, 2], f'ramp {ramp} (22%, 52%, 17%, 9% against 20, 50, 20, 10)')
used = {s for it in items for s in it['skills']}
ex.claim(used == set(doc['skills']), 'every skill of the topic is tested and no other')
maps = {}
for c in ('number-sense', 'ratio'):
    maps.update(json.load(open(os.path.join(ROOT, 'courses', c, 'course.json'), encoding='utf8'))['skills'])
ex.claim(doc['skills'] == maps, 'the skills map equals the union of the two course.json maps')
PACE = {'e-mixed-subtract': 60, 'e-percent-build': 45, 'e-pnl-close': 45, 'e-decimal-order': 60, 'e-ratio-units': 80,
        'e-tranches': 110, 'e-terminating': 150, 'e-tick-count': 90, 'e-fraction-power': 90, 'e-operation-order': 75,
        'e-estimate': 90, 'e-before-fall': 95, 'e-three-moves': 90, 'e-ratio-gap': 90, 'e-two-currencies': 150,
        'e-loss-share': 90, 'e-fill-rate': 90, 'e-depreciation': 150, 'e-inverse-square': 180, 'e-minus-eight': 150,
        'e-chain-ratio': 150, 'e-fund-fees': 300, 'e-recurring-proof': 300}
ex.claim(all(IT[k].get('pace') == v for k, v in PACE.items()), 'every item stores the reader pace')
ex.claim(doc['minutes'] == 50 and sum(PACE.values()) == 2730, 'minutes 50 against paces summing to 2,730 s (45.5 min) plus time to check')
ex.claim(set(PACE) == set(IT), 'a reader pace for every item')
total = sum(PACE.values())
ex.claim(total <= doc['minutes'] * 60, f'reader paces sum to {total} s ({total / 60:.1f} min) within {doc["minutes"]} minutes')

# ---------------------------------------------------------------- wrong values against the answer bands (rule 581)
ex.check_wrongs()
ex.report()
