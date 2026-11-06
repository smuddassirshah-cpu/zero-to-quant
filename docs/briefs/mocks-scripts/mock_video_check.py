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
answer = {'v1-hardest-part': 120, 'v2-others-error': 120, 'v3-too-much-work': 120, 'v4-fair-price': 90, 'v5-heads-pairs': 90}
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
    rec(f'When the paper clock shows {clock_text[sec]}, press Start the clock and speak.' in it['prompt'], f"{it['id']} prompt names the clock reading to start at")
    rec(p['name'].split(': ')[1] in ('motivation', 'behavioural', 'technical'), f"{p['id']} paper name shows only the kind of prompt")
    rows = it['rubric']
    rec(sum(r['points'] for r in rows) == 10, f"{it['id']} rubric sums to 10")
    req = [r for r in rows if r.get('required')]
    rec(len(req) == 1 and clock_text[sec] in req[0]['text'] and req[0]['points'] == 1, f"{it['id']} one required time row naming {clock_text[sec]}")
    rec(len(rows) >= 3 and all(isinstance(r['points'], int) and r['points'] > 0 for r in rows), f"{it['id']} rubric rows are whole points")
rec(total == F(23, 2) and total * 60 == 150 * 3 + 120 * 2, f'papers sum to {float(total)} minutes (690 s)')

# ---------- each model: word count and spoken time ----------
LABEL_B = 'Your own story is the real answer, so use this for its shape.'
LABEL_T = 'Match its order and its numbers.'
LABEL = {k: re.compile(r'^\*An example answer\. ' + re.escape(v) + r' It is (\d+) words, about (\d+) seconds at 130 words a minute\.\*\n\n')
         for k, v in (('b', LABEL_B), ('t', LABEL_T))}
spoken = {}
for pi, p in enumerate(papers):
    it = p['items'][0]
    kind = 't' if it['id'] in ('v4-fair-price', 'v5-heads-pairs') else 'b'          # technical models have no story to own
    m = LABEL[kind].match(it['model'])
    rec(m is not None, f"{it['id']} model opens with the {'technical' if kind == 't' else 'behavioural'} example label")
    if not m:
        continue
    body = it['model'][m.end():]
    w = len(re.findall(r'\S+', body))
    s = (w * 60 * 2 + WPM) // (2 * WPM)                      # round half up, integer route
    rec(int(m.group(1)) == w and int(m.group(2)) == s, f"{it['id']} label {m.group(1)} words, {m.group(2)} s; counted {w}, {s}")
    rec(s <= it['seconds'], f"{it['id']} model fits the answer time ({s} s of {it['seconds']} s)")
    rec(w * 60 <= 150 * it['seconds'], f"{it['id']} model fits the answer time at 150 words a minute ({w} words)")
    if kind == 'b':                                          # recruiting/l10: 10 + 80 + 30 s, so a full answer is about 100 s
        rec(85 <= s <= 105, f"{it['id']} behavioural model fills the 2-minute budget ({s} s)")
    spoken[it['id']] = (w, s)

# ---------- prompt numbers, second route ----------
# Prompt 4: expected payout of a fair die, Decimal
payout = sum(D(v) for v in (0, 0, 0, 0, 4, 10)) / 6
rec(round(payout, 2) == D('2.33') and D(14) / 6 == payout, f'fair price {payout:.4f}, about 2.33')
rec(round((D('2.5') - payout) * 100) == 17 and abs((D('2.5') - payout) * 600 - 100) < D('1e-20'), 'at 2.50 the average loss is about 17p a play, 100 pounds over 600 plays')
rec(D(10) - D('2.5') == D('7.5'), 'a six nets 7.50 at a price of 2.50')
# Prompt 5: pairs of heads, exact counting over all 2^n flips for n = 12, then the formula for n = 100
nn = 12
count = sum(sum(1 for i in range(nn - 1) if (f >> i) & 1 and (f >> (i + 1)) & 1) for f in range(1 << nn))
rec(F(count, 1 << nn) == F(nn - 1, 4), 'pairs of heads: brute force on 12 flips equals (n - 1) / 4')
rec(D(99) * D('0.25') == D('24.75') and 100 - 1 == 99, 'pairs of heads in 100 flips: 99 pairs, 24.75')
# Prompt 2: compounding in Decimal
two = D('1.1') * D('0.9')
rec(two == D('0.99') and (1 - two) * 100 == 1, 'compounded +10% then -10% is 0.99, a 1% loss')
# Prompt 3: hours and marks per hour, Decimal
rec(D(6) + D(3) + D(3) == 12 and 12 - 3 == 9, 'hours 6 + 3 + 3 = 12; 12 - 3 = 9 free')
rec(round(D(40) / D(6), 1) == D('6.7') and round(D(10) / D(3), 1) == D('3.3'), 'marks per hour 6.7 and 3.3')
# Prompt 1: problems
rec(sum([20] * 6) == 120, '20 a week for six weeks is 120')

# ---------- story numbers agree with each other ----------
m1 = next(p for p in papers if p['items'][0]['id'] == 'v1-hardest-part')['items'][0]['model']
lim = int(re.search(r'(\d+)-minute limit', m1).group(1))
med = [int(x) for x in re.search(r'median time has fallen from (\d+) minutes to (\d+)', m1).groups()]
rec(med[1] < med[0] <= lim, f'prompt 1: medians {med[0]} and {med[1]} are inside the {lim}-minute limit')
rec(int(re.search(r'solve (\d+) timed', m1).group(1)) * 6 == int(re.search(r'is (\d+) problems', m1).group(1)), 'prompt 1: weekly problems times six weeks')
m3 = next(p for p in papers if p['items'][0]['id'] == 'v3-too-much-work')['items'][0]['model']
h = [int(x) for x in re.search(r'the essay (\d+), the sheet (\d+) and the newsletter (\d+)', m3).groups()]
rec(sum(h) == int(re.search(r'had (\d+) hours of work', m3).group(1)), 'prompt 3: task hours add to the hours of work')
rec(sum(h) - h[2] == int(re.search(r'and (\d+) hours free', m3).group(1)) == int(re.search(r'left (\d+) hours of work', m3).group(1)), 'prompt 3: hours after the drop equal the free hours')

# ---------- each rubric row rewards something its prompt asks for (key noun in the prompt) ----------
KEY = {
    'v1-hardest-part': ['hardest', 'hardest', 'preparing', 'internship', 'internship'],
    'v2-others-error': ['mistake', 'time', 'did', 'mistake', 'numbers', 'did'],
    'v3-too-much-work': ['drop', 'work', 'why', 'drop', 'week', 'time'],
    'v4-fair-price': ['fair price', 'six', 'average', '\u00a32.50', 'one play'],
    'v5-heads-pairs': ['expect', 'pairs', 'head', 'expect', 'overlap'],
}
for p in papers:
    it = p['items'][0]
    q = it['prompt'].lower()
    content_rows = [r for r in it['rubric'] if not r.get('required') and 'filler' not in r['text']]
    rec(len(content_rows) == len(KEY[it['id']]), f"{it['id']} one key noun per content row")
    for r, noun in zip(content_rows, KEY[it['id']]):
        rec(noun in q, f"{it['id']} row key noun '{noun}' appears in the prompt", r['text'][:50])

# ---------- every number in each learner-visible string belongs to its place ----------
allowed_item = {
    'v1-hardest-part': {20, 25, 120, 23, 15, 5},
    'v2-others-error': {10, 0, 1.1, 0.9, 0.99, 1, 74},
    'v3-too-much-work': {12, 9, 40, 10, 6, 3, 6.7, 3.3, 0, 68},
    'v4-fair-price': {10, 4, 6, 14, 2.33, 2.5, 17, 100, 600, 7.5, 0},
    'v5-heads-pairs': {100, 99, 24.75, 0.25, 1, 0},
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
rec('Prompts 4 and 5 are our own' in doc['description'] and 'This pass line is ours' in doc['description'] and 'random variables course' in doc['description'], 'description: technical prompts are ours, pass line is ours, course named')
rec('some platforms' in doc['models'], 'models: states the reported format, technical prompts only as some platforms')
rec('Both state every fact' not in doc['description'], 'description: no claim that prompts state every fact')
bad = [x for x in _numbers(doc['description']) if x not in desc_ok]
rec(not bad, 'description: every number accounted for', f'unexplained {bad}' if bad else '')
rec(set(_numbers(doc['models'])) == {2026}, 'models: only the as-of year')
for want in ('30 seconds', '2 minutes', '90 seconds', '7 of 10', 'Nov 2026', 'Prompts 4 and 5'):
    ex.expect('exam', 'description', want)

# key numbers where they are stated
p4 = 'parts[3].items[0]'
p5x = 'parts[4].items[0]'
for path, v in ((f'{p4}.model', 2.33), (f'{p4}.model', 17), (f'{p4}.model', 100), (f'{p4}.rubric', 2.33), (f'{p4}.rubric', 17),
                (f'{p5x}.model', 24.75), (f'{p5x}.model', 99), (f'{p5x}.rubric', 24.75), (f'{p5x}.rubric', 99),
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
