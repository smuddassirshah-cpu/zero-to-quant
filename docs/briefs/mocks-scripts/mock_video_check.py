"""Second route for app/content/exams/mock-video.json. Exits 1 on any failure.

Independent of mock_video_build.py: reads the JSON, recomputes every number by a second method (binomial sums,
bit lengths, Decimal arithmetic, integer rounding of the word counts) and checks, with app/tools/numbers_lib.py,
that each key number appears where it is stated and that every number in every learner-visible string belongs to
the set computed for that place. Also checks the timings (thinking plus answer time is the paper's clock, the
papers sum to 11.5 minutes), the rubric sums and required time rows, and that no firm is named outside `models`
and `description`. Ends with check_wrongs() and report().
Run: python3 -I docs/briefs/mocks-scripts/mock_video_check.py
"""
import json
import math
import os
import re
import sys
from decimal import Decimal as D
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _numbers  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'mock-video.json')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
rec = lambda ok, label, note='': ex._rec(bool(ok), label, note)  # noqa: E731

papers = [p for p in doc['parts'] if p['kind'] == 'paper']
checks = [p for p in doc['parts'] if p['kind'] == 'check']
rec(len(papers) == 5 and len(checks) == 2, 'five papers and two checks')
rec(all(len(p['items']) == 1 for p in papers), 'one prompt per paper')

# ---------- timings, second route ----------
THINK, WPM = 30, 130
answer = {'v1-hardest-part': 120, 'v2-others-error': 120, 'v3-too-much-work': 120, 'v4-many-signals': 90, 'v5-halving-search': 90}
clock_text = {120: '2:00', 90: '1:30'}
total = F(0)
for pi, p in enumerate(papers):
    it = p['items'][0]
    sec = it['seconds']
    rec(sec == answer[it['id']], f"{it['id']} answer time {sec} s")
    rec(F(p['minutes']) * 60 == THINK + sec == it['pace'], f"{it['id']} paper clock {p['minutes']} min = 30 s + {sec} s = pace {it['pace']}")
    rec(p['pass'] == 1 and p['navigation'] == 'forward' and p['skip'] is False and p['scoring'] == {'right': 1, 'wrong': 0, 'blank': 0},
        f"{p['id']} pass 1, forward, no skip, 1/0/0")
    total += F(p['minutes'])
    base = f'parts[{pi}].items[0]'
    ex.expect('exam', f'{base}.prompt', THINK)
    ex.expect('exam', f'{base}.prompt', '2 minutes' if sec == 120 else '90 seconds')
    rows = it['rubric']
    rec(sum(r['points'] for r in rows) == 10, f"{it['id']} rubric sums to 10")
    req = [r for r in rows if r.get('required')]
    rec(len(req) == 1 and clock_text[sec] in req[0]['text'] and req[0]['points'] == 1, f"{it['id']} one required time row naming {clock_text[sec]}")
    rec(len(rows) >= 3 and all(isinstance(r['points'], int) and r['points'] > 0 for r in rows), f"{it['id']} rubric rows are whole points")
rec(total == F(23, 2) and total * 60 == 150 * 3 + 120 * 2, f'papers sum to {float(total)} minutes (690 s)')

# ---------- each model: word count and spoken time ----------
LABEL = re.compile(r'^\*An example answer\. Your own story is the real answer, so use this for its shape\. It is (\d+) words, about (\d+) seconds at 130 words a minute\.\*\n\n')
spoken = {}
for pi, p in enumerate(papers):
    it = p['items'][0]
    m = LABEL.match(it['model'])
    rec(m is not None, f"{it['id']} model opens with the example label")
    if not m:
        continue
    body = it['model'][m.end():]
    w = len(re.findall(r'\S+', body))
    s = (w * 60 * 2 + WPM) // (2 * WPM)                      # round half up, integer route
    rec(int(m.group(1)) == w and int(m.group(2)) == s, f"{it['id']} label {m.group(1)} words, {m.group(2)} s; counted {w}, {s}")
    rec(s <= it['seconds'], f"{it['id']} model fits the answer time ({s} s of {it['seconds']} s)")
    spoken[it['id']] = (w, s)

# ---------- prompt numbers, second route ----------
# Prompt 4: binomial(100, 0.05)
n, p5 = 100, D('0.05')
mean = sum(k * math.comb(n, k) * p5 ** k * (1 - p5) ** (n - k) for k in range(n + 1))
p_none = (1 - p5) ** n
at_least = 1 - p_none
bonf = p5 / n
rec(abs(mean - 5) < D('1e-20'), f'binomial mean {mean:.6f} = 5')
rec(round(at_least * 100, 1) == D('99.4'), f'P(at least one) = {at_least:.6f}, 99.4%')
rec(bonf == D('0.0005'), f'Bonferroni {bonf}')
# Prompt 5: comparisons for 1,000,000 by bit length
N = 10 ** 6
k = (N - 1).bit_length()
rec(k == 20 and (1 << 20) == 1048576 and (1 << 19) == 524288 and (1 << 19) < N <= (1 << 20), 'binary search: 20 comparisons, 2^20 and 2^19')
rec(N >> 1 == 500000 and N >> 2 == 250000 and N // k == 50000, 'halves 500,000 and 250,000; scan 50,000 times as many')
# Prompt 2: compounding in Decimal
two = D('1.1') * D('0.9')
rec(two == D('0.99') and (1 - two) * 100 == 1, 'compounded +10% then -10% is 0.99, a 1% loss')
# Prompt 3: hours and marks per hour, Decimal
rec(D(6) + D(3) + D(3) == 12 and 12 - 3 == 9, 'hours 6 + 3 + 3 = 12; 12 - 3 = 9 free')
rec(round(D(40) / D(6), 1) == D('6.7') and round(D(10) / D(3), 1) == D('3.3'), 'marks per hour 6.7 and 3.3')
# Prompt 1: problems
rec(sum([20] * 6) == 120, '20 a week for six weeks is 120')

# ---------- every number in each learner-visible string belongs to its place ----------
allowed_item = {
    'v1-hardest-part': {20, 25, 120, 31, 19},
    'v2-others-error': {10, 0, 1.1, 0.9, 0.99, 1, 74},
    'v3-too-much-work': {12, 9, 40, 10, 6, 3, 6.7, 3.3, 0, 68},
    'v4-many-signals': {5, 100, 20, 0.05, 1, 0.95, 99.4, 0.0005},
    'v5-halving-search': {20, 1000000, 500000, 250000, 2, 1048576, 19, 524288, 50000},
}
common = {30, 2, 90, 0, 130}                                    # prompt head, clocks (2:00, 1:30), speaking pace
for pi, p in enumerate(papers):
    it = p['items'][0]
    w, s = spoken.get(it['id'], (None, None))
    ok_set = allowed_item[it['id']] | common | {w, s, 1, 3}         # 1:30 gives 1 and 30; "three or fewer" is a word
    for field in ('prompt', 'model', 'title'):
        bad = [x for x in _numbers(it[field]) if not any(abs(x - a) < 1e-9 for a in ok_set if a is not None)]
        rec(not bad, f"{it['id']}.{field}: every number accounted for", f'unexplained {bad}' if bad else '')
    for ri, r in enumerate(it['rubric']):
        bad = [x for x in _numbers(r['text']) if not any(abs(x - a) < 1e-9 for a in ok_set if a is not None)]
        rec(not bad, f"{it['id']}.rubric[{ri}]: every number accounted for", f'unexplained {bad}' if bad else '')
    rec(not _numbers(p['name'].replace(f'Prompt {pi + 1}', '')), f"{p['id']} name holds only its prompt number")
for c in checks:
    rec(not _numbers(c['name'] + ' ' + c['detail']), f"check {c['id']} states no number")
desc_ok = {2026, 4, 5, 30, 2, 90, 7, 10}
bad = [x for x in _numbers(doc['description']) if x not in desc_ok]
rec(not bad, 'description: every number accounted for', f'unexplained {bad}' if bad else '')
rec(set(_numbers(doc['models'])) == {2026}, 'models: only the as-of year')
for want in ('30 seconds', '2 minutes', '90 seconds', '7 of 10', 'Nov 2026', 'Prompts 4 and 5'):
    ex.expect('exam', 'description', want)

# key numbers where they are stated
p4 = 'parts[3].items[0]'
p5x = 'parts[4].items[0]'
for path, v in ((f'{p4}.model', 5), (f'{p4}.model', 99.4), (f'{p4}.model', 0.0005), (f'{p4}.rubric', 99.4), (f'{p4}.rubric', 0.0005),
                (f'{p5x}.model', 1048576), (f'{p5x}.model', 524288), (f'{p5x}.model', 50000), (f'{p5x}.rubric', 1048576), (f'{p5x}.rubric', 524288),
                ('parts[1].items[0].model', 0.99), ('parts[1].items[0].model', 74), ('parts[2].items[0].model', 6.7), ('parts[2].items[0].model', 3.3),
                ('parts[0].items[0].model', 120)):
    ex.expect('exam', path, v)

# ---------- firm names only in models and description ----------
FIRMS = ['JP Morgan', 'J.P. Morgan', 'Morgan Stanley', 'Goldman', 'IMC', 'Jane Street', 'Optiver', 'Citadel', 'SIG']
for f in ('JP Morgan', 'Morgan Stanley', 'Goldman Sachs', 'IMC'):
    rec(f in doc['models'] and f in doc['description'], f'{f} named in models and description')
rec('reported' in doc['models'].lower() and 'report' in doc['description'].lower(), 'models and description say reported')
blob = json.dumps(doc['parts']) + doc['name']
rec(not any(re.search(r'\b' + re.escape(f) + r'\b', blob) for f in FIRMS), 'no firm named in papers, items or checks')

ex.check_wrongs()
ex.report()
