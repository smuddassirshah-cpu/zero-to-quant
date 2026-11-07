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
key('e-percent-build', F(35, 100) * 360)                         # 126
wrong('e-percent-build', 'tenth', F(35, 1000) * 360)             # 12.6 = 3.5%
wrong('e-percent-build', 'thirty', F(30, 100) * 360)             # 108
say('e-percent-build', 'feedback.correct', 108)
say('e-percent-build', 'feedback.correct', 18)
say('e-percent-build', 'explain.text', 36)
say('e-percent-build', 'explain.text', 126)
say('e-percent-build', 'feedback.byKey.tenth', 3.5)
for t in ('126', '£126', '126.00'):
    typed('e-percent-build', t, 'right')
typed('e-percent-build', '12.6', 'tenth')
typed('e-percent-build', '108', 'thirty')
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
g = math.gcd(240, 90)
ex.claim((240 // g, 90 // g) == (8, 3) and g == 30, 'e-ratio-units 240 : 90 = 8 : 3, HCF 30')
ex.claim(F(24, 10) / 90 == F(2, 75), 'e-ratio-units option b 2.40 : 90 = 2 : 75')
ex.claim(math.gcd(24, 9) == 3 and F(24, 9) == F(8, 3), 'e-ratio-units option d 24 : 9 shares a factor of 3')
fresh('e-ratio-units', r'price : dividend', 'ratio l10 quiz[0]: mixed units to simplest form, with unconverted, unsimplified and reversed distractors')

# ---------------------------------------------------------------- [5] e-tranches
key('e-tranches', F(9, 2) / F(3, 8))                             # 12
wrong('e-tranches', 'multiplied', F(9, 2) * F(3, 8))             # 27/16
wrong('e-tranches', 'flipped-first', F(2, 9) * F(3, 8))          # 1/12
ex.claim(F(9, 2) * F(8, 3) == F(72, 6) == 12 and 12 * F(3, 8) == F(9, 2), 'e-tranches explain 72/6 = 12 and the check')
for t, e in (('12', 'right'), ('27/16', 'multiplied'), ('1/12', 'flipped-first'), ('0.083', 'flipped-first')):
    typed('e-tranches', t, e)
fresh('e-tranches', r'How many tranches does it fill', 'number-sense homework-1 items[4] divides a mixed number by a fraction to a whole answer (2 1/2 / 5/8 = 4)')

# ---------------------------------------------------------------- [6] e-terminating
opts6 = {'a': F(7, 40), 'b': F(9, 75), 'c': F(21, 56), 'd': F(5, 12), 'e': F(11, 30)}
ex.claim(correct_ids('e-terminating') == sorted(k for k, v in opts6.items() if terminates(v)), 'e-terminating keys are the terminating fractions')
ex.claim(F(9, 75) == F(3, 25) and F(21, 56) == F(3, 8), 'e-terminating explain 9/75 = 3/25, 21/56 = 3/8')
ex.claim(f'{5 / 12:.6f}' == '0.416667' and f'{11 / 30:.6f}' == '0.366667', 'e-terminating 5/12 = 0.41666..., 11/30 = 0.3666...')
ex.claim(F(11, 30).denominator == 30, 'e-terminating 11/30 is already in lowest terms, so its 3 stays')
fresh('e-terminating', r'\{7\}\{40\}', 'number-sense fractions-to-decimals lesson screens[9]: "Which fraction gives a decimal that stops?", key 7/40, distractor 5/12')
taught('e-terminating', r'are terminating decimals', 'number-sense', r'[Tt]erminat', 'the word "terminating" (the lesson says "a decimal that stops")')

# ---------------------------------------------------------------- [7] e-tick-count
n7 = F(6 * 10**5) / F(8, 1000)
ex.claim(n7 == 75_000_000, 'e-tick-count 6e5 / 8e-3 = 7.5e7')
ex.claim(correct_ids('e-tick-count') == ['a'], 'e-tick-count key a (7.5 x 10^7)')
ex.claim(F(75, 100) * 10**8 == n7 and F(75, 10) * 10**9 == 100 * n7, 'e-tick-count option b equals the count but is not standard form; c is 100 times too big')
ex.claim(F(6, 8) * 10**(5 + (-3)) == F(75, 10) * 10**1, 'e-tick-count option d = adding the powers, 0.75 x 10^2 = 7.5 x 10^1')
ex.claim(5 - (-3) == 8, 'e-tick-count why: 5 - (-3) = 8')

# ---------------------------------------------------------------- [8] e-fraction-power
v8 = F(27, 8)
ex.claim(F(3, 2) ** 3 == v8 and F(3, 2) ** 2 == F(9, 4), 'e-fraction-power (27/8)^(2/3) = (3/2)^2 = 9/4')
key('e-fraction-power', F(9, 4))
wrong('e-fraction-power', 'no-flip', F(4, 9))
wrong('e-fraction-power', 'negative', -F(4, 9))
for t, e in (('9/4', 'right'), ('2 1/4', 'right'), ('2.25', 'right'), ('4/9', 'no-flip'), ('-4/9', 'negative')):
    typed('e-fraction-power', t, e)
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
est = F(600) * F(5, 100) / F(2, 10)
ex.claim(est == 150 and correct_ids('e-estimate') == ['a'], 'e-estimate 600 x 0.05 / 0.2 = 150, key a')
ex.claim(F(600) * F(5, 100) / 2 == 15, 'e-estimate option b: divided by 2 gives 15')
ex.claim(F(600) * F(5, 100) * F(2, 10) == 6, 'e-estimate option c: multiplied by 0.2 gives 6')
ex.claim(F(600) * F(5, 10) / F(2, 10) == 1500, 'e-estimate option d: 0.0487 rounded to 0.5 gives 1500')
exact10 = 587 * 0.0487 / 0.198
ex.claim(round(exact10) == 144, f'e-estimate explain "about 144" ({exact10:.2f})')
fresh('e-estimate', r'0\.198', 'number-sense estimating lesson screens[5] estimates (38.7 x 5.12) / 0.198, the same three-number shape and denominator')

# ---------------------------------------------------------------- [11] e-before-fall
key('e-before-fall', F(306) / F(85, 100))                        # 360
wrong('e-before-fall', 'added-back', F(306) * F(115, 100))       # 351.9
wrong('e-before-fall', 'took-off', F(306) * F(85, 100))          # 260.1
ex.claim(F(15, 100) * 360 == 54 and 360 - 54 == 306, 'e-before-fall check: 15% of 360 is 54, 360 - 54 = 306')
fresh('e-before-fall', r'After a 15% fall', 'ratio review-2 items[1] (after 15% off, £68, same two slips) and the before-the-discount lesson quiz[2] (after a 75% fall)')

# ---------------------------------------------------------------- [12] e-three-moves
m12 = F(125, 100) * F(8, 10) * F(11, 10)
key('e-three-moves', m12 - 1)                                    # 0.1
wrong('e-three-moves', 'added', F(25 - 20 + 10, 100))
ex.claim(F(125, 100) * F(8, 10) == 1, 'e-three-moves explain: 1.25 x 0.8 = 1')
for t, e in (('10', 'right'), ('10%', 'right'), ('15', 'added')):
    typed('e-three-moves', t, e)
fresh('e-three-moves', r'rises 25%, then falls 20%', 'ratio up-then-down lesson quiz[3]: "rises 25% and then falls 20%", ending back at the start')

# ---------------------------------------------------------------- [13] e-ratio-gap
part = F(960, 7 - 4)
key('e-ratio-gap', part * 11)                                    # 3520
wrong('e-ratio-gap', 'gap-as-share', F(960, 7) * 11)
wrong('e-ratio-gap', 'gap-as-total', 960)
ex.claim(part == 320 and part * 7 == 2240 and part * 4 == 1280 and 2240 - 1280 == 960, 'e-ratio-gap explain: part 320, shares 2,240 and 1,280')
say('e-ratio-gap', 'explain.text', 2240)
say('e-ratio-gap', 'explain.text', 1280)
for t, e in (('3,520', 'right'), ('£3,520', 'right'), ('1508.57', 'gap-as-share'), ('960', 'gap-as-total')):
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

# ---------------------------------------------------------------- [15] e-loss-share
key('e-loss-share', F(85, 1250))                                 # 0.068
wrong('e-loss-share', 'flipped', round(1250 / 85 / 100, 3))      # 14.7% typed as 14.7
wrong('e-loss-share', 'decimal', F(85, 1250) / 100)              # 0.068 typed into a % box
ex.claim(abs(1250 / 85 - 14.70588) < 1e-4, 'e-loss-share 1250 / 85 = 14.706')
for t, e in (('6.8', 'right'), ('6.8%', 'right'), ('14.7', 'flipped'), ('14.71', 'flipped'), ('0.068', 'decimal')):
    typed('e-loss-share', t, e)
ex.claim(F(85, 1250) == F(68, 1000), 'e-loss-share explain 85/1250 = 6.8/100')
ex.claim_text('exam', f'{P("e-loss-share")}.explain.text', 'a bit over half', 0.5 < F(85, 125) <= F(6, 10),
              'e-loss-share explain: 85 is "a bit over half" of 125 (it is 68%, about two thirds)')

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

# ---------------------------------------------------------------- [18] e-inverse-square
if exam_has('e-inverse-square', r'square of \$x\$'):        # the shipped inverse-square table (findings 4 and 5)
    k18 = 12 * 2 ** 2
    cell('e-inverse-square', 0, 1, F(k18, 1 ** 2), typed_ok=('48',))
    cell('e-inverse-square', 2, 1, F(k18, 4 ** 2), typed_ok=('3',))
    cell('e-inverse-square', 3, 1, F(k18, 6 ** 2), typed_ok=('1.33', '4/3', '1 1/3'), typed_bad=('1.34',))
    ex.claim(k18 == 48 and F(k18, 36) == F(4, 3), 'e-inverse-square k = 48, 48/36 = 4/3')
else:
    ex.claim(False, 'e-inverse-square was rewritten: add checks for the new table here')
taught('e-inverse-square', r'square of \$x\$', 'ratio', r'inversely proportional to the square|\\[dt]?frac\{k\}\{x\^2\}',
       'inverse proportion to a square (ratio teaches only y = c/x)')

# ---------------------------------------------------------------- [19] e-minus-eight
opts19 = {'a': F(-2) ** 3, 'b': -(F(2) ** 3), 'c': F(-1, 2) ** -3, 'd': F(2) ** -3, 'e': -(F(-2) ** 3)}
ex.claim(correct_ids('e-minus-eight') == sorted(k for k, v in opts19.items() if v == -8), 'e-minus-eight keys are the options equal to -8')
ex.claim(opts19['d'] == F(1, 8) and opts19['e'] == 8, 'e-minus-eight 2^-3 = 1/8, -(-2)^3 = 8')
taught('e-minus-eight', r'2\^\{-3\}', 'number-sense', r'(?<![0-9])[2-9]\^\{-[0-9]|\)\^\{-[0-9]',
       'a negative power of a base other than 10 (number-sense shows only 10^-n; exp-log, topic 0.3, teaches 2^-3)')

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

# ---------------------------------------------------------------- [22] e-recurring-proof
x = F(236, 1000) + F(36, 99000)                                   # 0.2 363636...
ex.claim(x == F(13, 55), 'e-recurring-proof 0.2(36 recurring) = 13/55')
ex.claim(1000 * x - 10 * x == 234 and F(234, 990) == F(13, 55) and math.gcd(234, 990) == 18, 'e-recurring-proof 990x = 234, cancel 18')
ex.claim(f'{13 / 55:.7f}' == '0.2363636', 'e-recurring-proof 13/55 = 0.2363636...')
w22 = IT['e-recurring-proof']['widget']
ex.claim(w22['answer'] == ['let', 'big', 'small', 'sub', 'end'] and w22['same'] == [['big', 'small']], 'e-recurring-proof order and same group')
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
PACE = {'e-mixed-subtract': 60, 'e-percent-build': 45, 'e-pnl-close': 45, 'e-decimal-order': 60, 'e-ratio-units': 60,
        'e-tranches': 90, 'e-terminating': 150, 'e-tick-count': 90, 'e-fraction-power': 90, 'e-operation-order': 75,
        'e-estimate': 90, 'e-before-fall': 75, 'e-three-moves': 90, 'e-ratio-gap': 90, 'e-two-currencies': 150,
        'e-loss-share': 90, 'e-fill-rate': 90, 'e-depreciation': 150, 'e-inverse-square': 180, 'e-minus-eight': 150,
        'e-chain-ratio': 150, 'e-fund-fees': 300, 'e-recurring-proof': 300}
ex.claim(set(PACE) == set(IT), 'a reader pace for every item')
total = sum(PACE.values())
ex.claim(total <= doc['minutes'] * 60, f'reader paces sum to {total} s ({total / 60:.1f} min) within {doc["minutes"]} minutes')

# ---------------------------------------------------------------- wrong values against the answer bands (rule 581)
ex.check_wrongs()
ex.report()
