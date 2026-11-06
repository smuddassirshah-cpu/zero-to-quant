"""Build app/content/exams/mock-video.json (docs/briefs/mocks.md, section mock-video). Deterministic: no randomness.

Holds every prompt, rubric, model answer and timing. Asserts each rubric sums to 10, each paper's seconds are the
thinking time plus the answer time, the papers sum to 690 s (11.5 minutes), each model fits its answer time at
130 words a minute, and every number in the models two ways (Fractions, loops). Then writes the JSON.
Run from the repository root: python3 -I docs/briefs/mocks-scripts/mock_video_build.py
"""
import json
import math
import os
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'mock-video.json')

THINK = 30          # seconds to think, every prompt
WPM = 130           # calm speaking pace taught in recruiting/l10-recorded-video


def words(text):
    return len(text.split())


def spoken_seconds(text):
    return round(F(words(text) * 60, WPM))


# ---------- numbers, each two ways ----------
# Prompt 1: 20 problems a week for 6 weeks
assert 20 * 6 == 120 == sum(20 for _ in range(6))
# Prompt 2: +10% then -10%, compounded
two_day = F(11, 10) * F(9, 10)
step = F(100)
step = step + step * F(10, 100)
step = step - step * F(10, 100)
assert two_day == F(99, 100) == step / 100
assert (1 - two_day) * 100 == 1                        # a 1% loss
assert (F(10) + F(-10)) / 2 == 0                       # the averaged (wrong) figure, 0%
# Prompt 3: hours and marks per hour
hours = {'essay': 6, 'sheet': 3, 'newsletter': 3}
marks = {'essay': 40, 'sheet': 10, 'newsletter': 0}
free = 9
assert sum(hours.values()) == 12 == 6 + 3 + 3
assert sum(hours.values()) - hours['newsletter'] == free == 12 - 3
per_hour = {k: F(marks[k], hours[k]) for k in hours}
assert round(float(per_hour['essay']), 1) == 6.7 and round(float(F(40) / 6), 1) == 6.7
assert round(float(per_hour['sheet']), 1) == 3.3 and round(10 / 3, 1) == 3.3
assert per_hour['newsletter'] == 0
assert sorted(hours, key=lambda k: per_hour[k]) [0] == 'newsletter'
# Prompt 4: 100 signals with no edge at the 5% level
n, alpha = 100, F(5, 100)
assert n * alpha == 5 == sum(alpha for _ in range(n))  # expected false passes: n alpha, and a sum of n indicator means
assert F(1, 20) == alpha                               # one time in 20
none_pass = F(95, 100) ** n
loop = F(1)
for _ in range(n):
    loop *= F(95, 100)
assert loop == none_pass
at_least_one = 1 - none_pass
assert round(float(at_least_one) * 100, 1) == 99.4 == round((1 - 0.95 ** 100) * 100, 1)
bonf = alpha / n
assert bonf == F(5, 10000) and float(bonf) == 0.0005
# Prompt 5: binary search on 1,000,000 sorted prices
N = 1_000_000
assert 2 ** 20 == 1_048_576
d = 1
for _ in range(20):
    d *= 2
assert d == 2 ** 20 and 2 ** 19 == 524_288 == d // 2
k, left = 0, N                                          # halving loop: comparisons until one price is left
while left > 1:
    left = math.ceil(left / 2)
    k += 1
assert k == 20 == math.ceil(math.log2(N))
assert 2 ** 19 < N <= 2 ** 20
assert N // 2 == 500_000 and N // 4 == 250_000
assert N // 20 == 50_000 and 20 * 50_000 == N


PROMPT_HEAD = ('Thinking time {think} seconds, then answer time {answer}, in one take. '
               'When the thinking time is up, press Start the clock and speak. '
               'Record yourself on your phone, or answer to a friend. '
               'The paper ends when its clock reaches zero.\n\n**{q}**')


def label(text):
    w, s = words(text), spoken_seconds(text)
    return (f'*An example answer. Your own story is the real answer, so use this for its shape. '
            f'It is {w} words, about {s} seconds at {WPM} words a minute.*\n\n'), w, s


TIME_ROW = {120: 'Finishes before the 2:00 answer clock reaches zero', 90: 'Finishes before the 1:30 answer clock reaches zero'}
FILLER = 'Uses three or fewer filler words such as "um", "like" or "you know", counted from the recording'

PROMPTS = [
    {
        'paper': 'motivation', 'name': 'Prompt 1: motivation', 'id': 'v1-hardest-part', 'tag': 'hardest-part',
        'answer': 120, 'skills': ['rk-behave'], 'title': 'The hardest part',
        'q': 'What do you expect to find hardest in a quant internship, and how are you preparing for it?',
        'model': (
            'The hardest part will be speed: correct code on real data while the questions keep changing. '
            'At university my code is marked once, a week later. '
            'On a desk, a slow answer is a late answer. '
            'So I have been training for that. '
            'Each week I solve 20 timed problems, with a 25-minute limit on each. '
            'Over six weeks that is 120 problems. '
            'My median time has fallen from 31 minutes to 19. '
            'I also rebuilt one project in pandas from a blank file, without my old notes. '
            'It took two evenings, not one, and that showed me where my gaps were. '
            'I expect the first month to feel slow anyway. '
            'I will ask for one piece of feedback each Friday and act on it the next week. '
            'I still want this work because the feedback is fast and honest. '
            'That is what will make me better.'),
        'rubric': [
            (1, 'Names one hard thing in the first sentence'),
            (2, 'Says why it is hard for you, from your own experience'),
            (2, 'Says what you are doing about it, with a number such as problems, hours or weeks'),
            (2, 'Ties the hard thing to the daily work of the role'),
            (1, 'Closes on why you still want the role'),
        ],
    },
    {
        'paper': 'someone-elses-error', 'name': 'Prompt 2: a mistake you found', 'id': 'v2-others-error', 'tag': 'others-error',
        'answer': 120, 'skills': ['rk-behave'], 'title': "A mistake in someone else's numbers",
        'q': "Tell us about a time you found a mistake in someone else's numbers. What did you do?",
        'model': (
            "I once found an error in a teammate's returns table, and I raised it before our deadline. "
            'In a second-year project, four of us wrote a report on two funds. '
            'My teammate averaged two daily returns to get the two-day return. '
            'One fund rose 10% and then fell 10%, and the table showed 0%. '
            'I compounded it instead: 1.1 times 0.9 is 0.99, so a 1% loss. '
            'Before saying anything, I rechecked it on three other pairs of days. '
            'All three were off in the same direction. '
            'Then I messaged him privately with one worked example, not a list of faults. '
            'He fixed the formula in ten minutes, and we reran every table. '
            'We handed in a day early and scored 74%. '
            'I learned to show the check, not just the claim. '
            'Now I add one compounding test to every returns sheet I build.'),
        'rubric': [
            (1, 'Answers in the first sentence: whose mistake, and that you raised it'),
            (1, 'Gives the situation in at most two sentences'),
            (2, 'Says at least two things you did, with "I", not "we"'),
            (2, 'Says how you checked the mistake before you raised it, and how you raised it'),
            (1, 'Gives a result with a number'),
            (1, 'Ends on one thing you now do differently'),
        ],
    },
    {
        'paper': 'more-work-than-time', 'name': 'Prompt 3: more work than time', 'id': 'v3-too-much-work', 'tag': 'too-much-work',
        'answer': 120, 'skills': ['rk-behave'], 'title': 'More work than time',
        'q': 'Tell us about a week when you had more work than time. What did you drop, and why?',
        'model': (
            'In one exam week I had 12 hours of work and 9 hours free, so I dropped the newsletter. '
            'I had an essay worth 40% of a module and a problem sheet worth 10%. '
            'I also edit the newsletter, which carries no marks. '
            'I listed each task with its hours: the essay 6, the sheet 3 and the newsletter 3. '
            'Marks per hour were about 6.7 for the essay, 3.3 for the sheet, 0 for the newsletter. '
            'So the newsletter went first. '
            'I asked the society chair to run a short edition that week, which saved my 3 hours. '
            'That left 9 hours of work for 9 hours free. '
            'The essay scored 68%, my best mark that year. '
            'The newsletter went out two days late, and the chair told readers why. '
            'Next time I would list the hours on Monday, not on Wednesday.'),
        'rubric': [
            (1, 'Answers in the first sentence: what you dropped'),
            (2, 'Gives the tasks and their hours or weights, as numbers'),
            (2, 'Gives the rule you used to choose, such as marks per hour'),
            (1, 'Says what you told the person affected'),
            (1, 'Gives the result with a number'),
            (1, 'Says what you would do earlier next time'),
        ],
    },
    {
        'paper': 'many-signals', 'name': 'Prompt 4: technical, researcher', 'id': 'v4-many-signals', 'tag': 'many-signals',
        'answer': 90, 'skills': ['ht-multiple', 'rk-assess'], 'title': 'One hundred signals',
        'q': 'A colleague tests 100 trading signals at the 5% level. None has a real edge. '
             'Explain how many will look significant, and what you would do before trusting one.',
        'model': (
            'About 5 of the 100 will look significant by chance alone. '
            'A signal with no edge still passes a 5% test one time in 20. '
            'So 100 tests give 100 times 0.05, which is 5 false finds on average. '
            'The chance that at least one passes is 1 minus 0.95 to the power 100, about 99.4%. '
            'So one significant signal out of 100 tells us almost nothing. '
            'Before trusting one, I would do three things. '
            'First, raise the bar for the number of tests: a Bonferroni cut-off is 0.05 over 100, so 0.0005. '
            'Second, test the best signal on data it has never seen, such as the last two years held back. '
            'Third, ask whether there is a reason for the effect, not only a p-value. '
            'If it survives all three, I would trade it small and watch it.'),
        'rubric': [
            (1, 'The first sentence gives the number: about 5 of the 100'),
            (2, 'Says why: each signal with no edge passes a 5% test one time in 20, so $100 \\times 0.05$'),
            (2, 'Says at least one false pass is almost certain: $1 - 0.95^{100}$, about 99.4%'),
            (2, 'Names a fix for many tests, such as the cut-off $0.05 / 100 = 0.0005$ or a false discovery rate'),
            (1, 'Names a check on data held back from the search'),
        ],
    },
    {
        'paper': 'halving-search', 'name': 'Prompt 5: technical, strats', 'id': 'v5-halving-search', 'tag': 'halving-search',
        'answer': 90, 'skills': ['at-search', 'rk-assess'], 'title': 'Twenty comparisons',
        'q': 'Explain why binary search finds a price in a sorted list of 1,000,000 prices in at most 20 comparisons. '
             'What goes wrong if the list is not sorted?',
        'model': (
            'Twenty is enough because each comparison halves the part of the list that can still hold the price. '
            'We look at the middle price first. '
            'If ours is smaller, the whole top half is ruled out at once. '
            'After one comparison 500,000 prices remain, after two 250,000, and so on. '
            'Twenty halvings divide by 2 to the 20, which is 1,048,576. '
            'That is more than a million, so 20 comparisons always finish. '
            'Nineteen are not always enough, because 2 to the 19 is only 524,288. '
            'A scan from the start could need all 1,000,000 comparisons, 50,000 times as many. '
            'The catch is the sorting. '
            'On an unsorted list, ruling out half is not safe, so the search can miss the price. '
            'Sorting first costs about $n \\log n$ steps, so it pays only when we search many times.'),
        'rubric': [
            (2, 'The first sentence gives 20 and the halving reason'),
            (1, 'Shows the halving with numbers: 500,000, then 250,000'),
            (2, 'Uses $2^{20} = 1{,}048{,}576 \\ge 1{,}000{,}000$ and says why 19 is not enough, $2^{19} = 524{,}288$'),
            (1, 'Compares with a scan of up to 1,000,000 comparisons'),
            (2, 'Says the list must be sorted, and what goes wrong otherwise'),
        ],
    },
]

items_out, parts = [], []
total = 0
for p in PROMPTS:
    head, w, s = label(p['model'])
    assert s <= p['answer'], (p['id'], s)
    rows = [{'points': a, 'text': t} for a, t in p['rubric']]
    rows.append({'points': 1, 'text': TIME_ROW[p['answer']], 'required': True})
    rows.append({'points': 1, 'text': FILLER})
    assert sum(r['points'] for r in rows) == 10, p['id']
    paper_s = THINK + p['answer']
    total += paper_s
    answer_txt = '2 minutes' if p['answer'] == 120 else '90 seconds'
    item = {
        'id': p['id'], 'difficulty': 3, 'skills': p['skills'], 'tags': [p['tag'], 'recorded-video'], 'pace': paper_s,
        'title': p['title'], 'kind': 'longform',
        'prompt': PROMPT_HEAD.format(think=THINK, answer=answer_txt, q=p['q']),
        'seconds': p['answer'],
        'model': head + p['model'],
        'rubric': rows,
    }
    p['words'], p['spoken'] = w, s
    parts.append({'kind': 'paper', 'id': p['paper'], 'name': p['name'], 'minutes': paper_s / 60,
                  'scoring': {'right': 1, 'wrong': 0, 'blank': 0}, 'pass': 1, 'navigation': 'forward', 'skip': False,
                  'items': [item]})
assert total == 690 == 3 * 150 + 2 * 120
assert F(total, 60) == F(23, 2)                         # 11.5 minutes
assert sum(F(int(pp['minutes'] * 2), 2) for pp in parts) == F(23, 2)
for pp in parts:
    if pp['minutes'] == int(pp['minutes']):
        pp['minutes'] = int(pp['minutes'])

parts.append({'kind': 'check', 'id': 'one-take', 'name': 'I answered every prompt aloud, in one take each',
              'detail': 'Tick this only if you spoke each answer in full, to a camera or a friend, with no restarts.'})
parts.append({'kind': 'check', 'id': 'marked-from-recording', 'name': "I marked each answer from my recording or a friend's notes",
              'detail': 'Tick this only if you ticked each rubric from what you actually said, not from memory.'})

MODELS = ('Reported, as of Nov 2026: one-way recorded video rounds at JP Morgan, Morgan Stanley, Goldman Sachs and IMC. '
          'Timed behavioural, motivation and short technical prompts.')
assert len(MODELS) <= 200 and '\n' not in MODELS

DESCRIPTION = (
    'This models a one-way recorded video round, as firms and candidates describe it. '
    'JP Morgan, Morgan Stanley, Goldman Sachs and IMC all list or report one, as of Nov 2026. '
    'Each prompt is its own paper on its own clock, and a finished paper cannot be reopened. '
    'You get 30 seconds to think, then 2 minutes to answer. '
    'Prompts 4 and 5 are short technical ones for researchers and strats, with 90 seconds to answer. '
    'Both state every fact they need. '
    'The app does not record you. '
    'Record yourself on your phone, or answer to a friend, in one take. '
    'Then mark each answer against its rubric from the recording. '
    'Each answer needs 7 of 10, with its time row ticked. '
    'Two checks at the end ask for what the app cannot see.')

doc = {
    'id': 'mock-video', 'name': 'Recorded video interview', 'style': 'research', 'models': MODELS,
    'description': DESCRIPTION,
    'requires': ['recruiting/l10-recorded-video'],
    'skills': {'rk-behave': 'Behavioural answers', 'rk-assess': 'Assessments and video interviews',
               'ht-multiple': 'Multiple testing', 'at-search': 'Binary search'},
    'parts': parts,
}

FIRMS = ['JP Morgan', 'Morgan Stanley', 'Goldman Sachs', 'IMC']
for pp in parts:
    blob = json.dumps(pp)
    for f in FIRMS:
        assert f not in blob, (pp.get('id'), f)

with open(OUT, 'w', encoding='utf8') as fh:
    json.dump(doc, fh, indent=2, ensure_ascii=False)
    fh.write('\n')

print('mock-video: 5 papers, 5 prompts, 2 checks,', total, 's =', float(F(total, 60)), 'min')
for p in PROMPTS:
    print(f"  {p['id']:<20} think {THINK} s, answer {p['answer']} s, model {p['words']} words, {p['spoken']} s spoken")
