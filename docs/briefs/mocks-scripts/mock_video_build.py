"""Build app/content/exams/mock-video.json (docs/briefs/mocks.md, section mock-video). Deterministic: no randomness.

Holds every prompt, rubric, model answer and timing. Asserts each rubric sums to 10, each paper's seconds are the
thinking time plus the answer time, the papers sum to 690 s (11.5 minutes), each model fits its answer time at
130 words a minute (behavioural models fill 85 to 105 s of a 120 s answer, the budget taught in
recruiting/l10-recorded-video), each rubric row's key noun appears in its prompt, story numbers agree with each
other, and every number in the models two ways (Fractions, loops, brute force). Then writes the JSON.
Run from the repository root: python3 -I docs/briefs/mocks-scripts/mock_video_build.py
"""
import itertools
import json
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
# Prompt 1: 20 problems a week for 6 weeks; both medians stay inside the 25-minute limit
assert 20 * 6 == 120 == sum(20 for _ in range(6))
LIMIT, MEDIAN_FROM, MEDIAN_TO = 25, 23, 15
assert MEDIAN_TO < MEDIAN_FROM <= LIMIT
# Prompt 2: +10% then -10%, compounded; the teammate added the two returns
two_day = F(11, 10) * F(9, 10)
step = F(100)
step = step + step * F(10, 100)
step = step - step * F(10, 100)
assert two_day == F(99, 100) == step / 100
assert (1 - two_day) * 100 == 1                        # a 1% loss
assert F(10) + F(-10) == 0                             # the added (wrong) figure, 0%
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
assert sorted(hours, key=lambda k: per_hour[k])[0] == 'newsletter'
# Prompt 4: a fair die; a six pays 10 pounds, a five 4 pounds, the other faces nothing
pay = {1: 0, 2: 0, 3: 0, 4: 0, 5: 4, 6: 10}
ev = sum(F(1, 6) * v for v in pay.values())
assert ev == F(14, 6) == F(7, 3) == F(10 + 4, 6)
assert round(float(ev), 2) == 2.33 == round(14 / 6, 2)
loss = F(5, 2) - ev                                     # price 2.50 minus the average payout
assert loss == F(1, 6) and round(float(loss) * 100) == 17 == round(100 / 6)
assert 600 * loss == 100 == sum(loss for _ in range(600))
assert 10 - F(5, 2) == F(15, 2)                         # a six nets 7.50 at that price
# Prompt 5: expected "head then head" pairs in 100 fair flips, by an indicator sum and by brute force on 12 flips
flips = 100
pairs = flips - 1
assert pairs == 99 == len([i for i in range(flips) if i + 1 < flips])
p_pair = F(1, 2) * F(1, 2)
assert p_pair == F(1, 4) == F(25, 100)
exp_pairs = sum(p_pair for _ in range(pairs))
assert exp_pairs == F(99, 4) == pairs * p_pair and float(exp_pairs) == 24.75
tot = sum(sum(1 for i in range(11) if f[i] and f[i + 1]) for f in itertools.product([0, 1], repeat=12))
assert F(tot, 2 ** 12) == F(11, 4) == 11 * p_pair


PROMPT_HEAD = ('Thinking time {think} seconds, then answer time {answer}, in one take. '
               'When the paper clock shows {clock}, press Start the clock and speak. '
               'Record yourself on your phone, or answer to a friend. '
               'The paper ends when its clock reaches zero.\n\n**{q}**')

LABEL_BEHAVIOURAL = 'Your own story is the real answer, so use this for its shape.'
LABEL_TECHNICAL = 'Match its order and its numbers.'


def label(text, kind):
    w, s = words(text), spoken_seconds(text)
    lead = LABEL_BEHAVIOURAL if kind == 'behavioural' else LABEL_TECHNICAL
    return (f'*An example answer. {lead} '
            f'It is {w} words, about {s} seconds at {WPM} words a minute.*\n\n'), w, s


TIME_ROW = {120: 'Finishes before the 2:00 answer clock reaches zero', 90: 'Finishes before the 1:30 answer clock reaches zero'}
CLOCK = {120: '2:00', 90: '1:30'}
FILLER = 'Uses three or fewer filler words such as "um", "like" or "you know", counted from the recording'

# Each rubric row is (points, text, key noun that must appear in the prompt).
PROMPTS = [
    {
        'paper': 'motivation', 'name': 'Prompt 1: motivation', 'id': 'v1-hardest-part', 'tag': 'hardest-part', 'kind': 'behavioural',
        'answer': 120, 'skills': ['rk-behave'], 'title': 'The hardest part',
        'q': 'What do you expect to find hardest in a quant internship, and how are you preparing for it?',
        'model': (
            'The hardest part will be speed: correct code on real data while the questions keep changing. '
            'At university my code is marked once, a week later. '
            'On a desk, a slow answer is a late answer. '
            'So I have been training for that. '
            'Each week I solve 20 timed problems, with a 25-minute limit on each. '
            'Over six weeks that is 120 problems. '
            'My median time has fallen from 23 minutes to 15. '
            'I log every miss, and most were not hard ideas. '
            'They were slips in the first five minutes, so I now write the input and output down before any code. '
            'I also rebuilt one project in pandas from a blank file, without my old notes. '
            'It took two evenings, not one, and that showed me where my gaps were. '
            'I had never written a merge on dates from memory, so I drilled it until it was routine. '
            'I expect the first month to feel slow anyway. '
            'I will ask for one piece of feedback each Friday and act on it the next week. '
            'I still want this work because the feedback is fast and honest. '
            'That is what will make me better.'),
        'rubric': [
            (1, 'Names one hard thing in the first sentence', 'hardest'),
            (2, 'Says why it is hard for you, from your own experience', 'hardest'),
            (2, 'Says what you are doing about it, with a number such as problems, hours or weeks', 'preparing'),
            (2, 'Ties the hard thing to the daily work of the role', 'internship'),
            (1, 'Closes on why you still want the role', 'internship'),
        ],
    },
    {
        'paper': 'someone-elses-error', 'name': 'Prompt 2: behavioural', 'id': 'v2-others-error', 'tag': 'others-error', 'kind': 'behavioural',
        'answer': 120, 'skills': ['rk-behave'], 'title': "A mistake in someone else's numbers",
        'q': "Tell us about a time you found a mistake in someone else's numbers. What did you do?",
        'model': (
            "I once found an error in a teammate's returns table, and I raised it before our deadline. "
            'In a second-year project, four of us wrote a report on two small-cap shares. '
            'My teammate added two daily returns to get the two-day return. '
            'One share rose 10% and then fell 10%, and the table showed 0%. '
            'I compounded it instead: 1.1 times 0.9 is 0.99, so a 1% loss. '
            'At first I doubted myself, because he is stronger at maths than I am. '
            'So I rechecked it on three other pairs of days. '
            'All three were off in the same direction. '
            'I wrote the working on one page, with the three pairs side by side. '
            'Then I messaged him privately with one worked example, not a list of faults. '
            'I asked him to check my sums too, so it was not a verdict. '
            'He fixed the formula in ten minutes, and we reran every table. '
            'We handed in a day early and scored 74%. '
            'I learned to show the check, not just the claim. '
            'Now I add one compounding test to every returns sheet I build.'),
        'rubric': [
            (1, 'Answers in the first sentence: whose mistake, and that you raised it', 'mistake'),
            (1, 'Gives the situation in at most two sentences', 'time'),
            (2, 'Says at least two things you did, with "I", not "we"', 'did'),
            (2, 'Says how you checked the mistake before you raised it, and how you raised it', 'mistake'),
            (1, 'Gives a result with a number', 'numbers'),
            (1, 'Ends on one thing you now do differently', 'did'),
        ],
    },
    {
        'paper': 'more-work-than-time', 'name': 'Prompt 3: behavioural', 'id': 'v3-too-much-work', 'tag': 'too-much-work', 'kind': 'behavioural',
        'answer': 120, 'skills': ['rk-behave'], 'title': 'More work than time',
        'q': 'Tell us about a week when you had more work than time. What did you drop, and why?',
        'model': (
            'In one exam week I had 12 hours of work and 9 hours free, so I dropped the newsletter. '
            'I had an essay worth 40% of a module and a problem sheet worth 10%. '
            'I also edit the newsletter, which carries no marks. '
            'I listed each task with its hours: the essay 6, the sheet 3 and the newsletter 3. '
            'Marks per hour were about 6.7 for the essay, 3.3 for the sheet, 0 for the newsletter. '
            'So the newsletter went first. '
            'I did not want to let anyone down, so I checked who depended on it that week. '
            'Only the society chair did. '
            'I told her two days before the deadline, so she had time to plan. '
            'I asked her to run a short edition that week, which saved my 3 hours. '
            'That left 9 hours of work for 9 hours free. '
            'I blocked the hours in my diary, essay first, and turned off my phone for each block. '
            'The essay scored 68%, my best mark that year. '
            'The newsletter went out two days late, and the chair told readers why. '
            'Next time I would list the hours on Monday, not on Wednesday.'),
        'rubric': [
            (1, 'Answers in the first sentence: what you dropped', 'drop'),
            (2, 'Gives the tasks and their hours or weights, as numbers', 'work'),
            (2, 'Gives the rule you used to choose, such as marks per hour', 'why'),
            (1, 'Says what you told the person affected', 'drop'),
            (1, 'Gives the result with a number', 'week'),
            (1, 'Says what you would do earlier next time', 'time'),
        ],
    },
    {
        'paper': 'fair-price', 'name': 'Prompt 4: technical', 'id': 'v4-fair-price', 'tag': 'fair-price', 'kind': 'technical',
        'answer': 90, 'skills': ['rv-expect', 'rk-assess'], 'title': 'A fair price',
        'q': 'A fair six-sided die is rolled. A six pays £10, a five pays £4, and any other face pays nothing. '
             'What is a fair price to play, and would you pay £2.50? '
             'What does the average not tell you about one play?',
        'model': (
            'The fair price is about £2.33, because a fair price is the average payout over many plays. '
            'To find it, I weigh each payout by its chance. '
            'A six pays £10 and a five pays £4, each with chance one in six. '
            'The other four faces pay nothing. '
            'So the average is 10 plus 4, over 6, which is 14 over 6, about £2.33. '
            'Pay that, and over many plays you break even. '
            'At £2.50 I would not play. '
            'You lose about 17p a play on average, which is £100 over 600 plays. '
            'One play is different. '
            'Most plays lose £2.50, and a six wins £7.50. '
            'So the average says little about a single game.'),
        'rubric': [
            (1, 'The first sentence gives the fair price: about £2.33', 'fair price'),
            (2, 'Says how: weigh each pay by its chance, $\\frac{10 + 4}{6}$, for a six and a five', 'six'),
            (2, 'Says a fair price is the average over many plays, where you break even', 'average'),
            (2, 'Answers the £2.50 question: no, with the average loss of about 17p a play', '£2.50'),
            (1, 'Says one play can differ a lot from the average', 'one play'),
        ],
    },
    {
        'paper': 'heads-pairs', 'name': 'Prompt 5: technical', 'id': 'v5-heads-pairs', 'tag': 'heads-pairs', 'kind': 'technical',
        'answer': 90, 'skills': ['rv-linearity', 'rk-assess'], 'title': 'Pairs of heads',
        'q': 'A fair coin is flipped 100 times. How many times do you expect a head to be followed at once by another head? '
             'Why does it not matter that neighbouring pairs overlap?',
        'model': (
            'I expect 24.75 such pairs. '
            'I count pairs of neighbouring flips, and 100 flips give 99 pairs, not 100. '
            'Each pair is two heads with chance one half times one half, so one in four. '
            'For each pair I use an indicator that is 1 if both are heads and 0 if not. '
            'Its average is 0.25. '
            'The expected total is the sum of the averages, so 99 times 0.25, which is 24.75. '
            'Overlap does not matter. '
            'The pairs share flips, so they are not independent. '
            'But the expected value of a sum is the sum of the expected values, always. '
            'So I never need independence. '
            'It would matter only for the spread.'),
        'rubric': [
            (1, 'The first sentence gives the expected number of pairs: 24.75', 'expect'),
            (2, 'Counts 99 pairs of neighbours, not 100', 'pairs'),
            (1, 'Gives the chance a pair is two heads: one in four', 'head'),
            (2, 'Adds an indicator for each pair and sums the expected values, $99 \\times 0.25$', 'expect'),
            (2, 'Says why overlap does not matter: the expected value of a sum needs no independence', 'overlap'),
        ],
    },
]

parts = []
total = 0
for p in PROMPTS:
    head, w, s = label(p['model'], p['kind'])
    assert s <= p['answer'], (p['id'], s)
    assert w * 60 <= 150 * p['answer'], (p['id'], 'over the answer time even at 150 words a minute')
    if p['kind'] == 'behavioural':
        assert 85 <= s <= 105 and p['answer'] == 120, (p['id'], s)    # fills the 10 + 80 + 30 s budget
    q = p['q'].lower()
    for pts, text, noun in p['rubric']:
        assert noun.lower() in q, (p['id'], text, noun)               # each row rewards what the prompt asks for
    rows = [{'points': a, 'text': t} for a, t, _ in p['rubric']]
    rows.append({'points': 1, 'text': TIME_ROW[p['answer']], 'required': True})
    rows.append({'points': 1, 'text': FILLER})
    assert sum(r['points'] for r in rows) == 10, p['id']
    paper_s = THINK + p['answer']
    total += paper_s
    answer_txt = '2 minutes' if p['answer'] == 120 else '90 seconds'
    item = {
        'id': p['id'], 'difficulty': 3, 'skills': p['skills'], 'tags': [p['tag'], 'recorded-video'], 'pace': paper_s,
        'title': p['title'], 'kind': 'longform',
        'prompt': PROMPT_HEAD.format(think=THINK, answer=answer_txt, clock=CLOCK[p['answer']], q=p['q']),
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

# paper names show only the kind of prompt, never its topic (the start card and the between-papers screen show them)
for pp, p in zip(parts, PROMPTS):
    assert pp['name'].split(': ')[1] in ('motivation', 'behavioural', 'technical'), pp['name']

parts.append({'kind': 'check', 'id': 'one-take', 'name': 'I answered every prompt aloud, in one take each',
              'detail': 'Tick this only if you spoke each answer in full, to a camera or a friend, with no restarts.'})
parts.append({'kind': 'check', 'id': 'marked-from-recording', 'name': "I marked each answer from my recording or a friend's notes",
              'detail': 'Tick this only if you ticked each rubric from what you actually said, not from memory.'})

MODELS = ('Reported, as of Nov 2026: one-way recorded video rounds at JP Morgan, Morgan Stanley, Goldman Sachs and IMC. '
          'Timed behavioural and motivation prompts; some platforms add technical ones.')
assert len(MODELS) <= 200 and '\n' not in MODELS

DESCRIPTION = (
    'This models a one-way recorded video round, as firms and candidates describe it. '
    'JP Morgan, Morgan Stanley, Goldman Sachs and IMC all list or report one, as of Nov 2026. '
    'Each prompt is its own paper on its own clock, and a finished paper cannot be reopened. '
    'You get 30 seconds to think, then 2 minutes to answer. '
    'Prompts 4 and 5 are our own short technical prompts, with 90 seconds to answer. '
    'They need only expected value, from the random variables course. '
    'The app does not record you. '
    'Record yourself on your phone, or answer to a friend, in one take. '
    'Then mark each answer against its rubric from the recording. '
    'Each answer needs 7 of 10, with its time row ticked. '
    'This pass line is ours; firms do not publish one. '
    'Two checks at the end ask for what the app cannot see.')

doc = {
    'id': 'mock-video', 'name': 'Recorded video interview', 'style': 'research', 'models': MODELS,
    'description': DESCRIPTION,
    'requires': ['recruiting/l10-recorded-video'],
    'skills': {'rk-behave': 'Behavioural answers', 'rk-assess': 'Assessments and video interviews',
               'rv-expect': 'Expectation', 'rv-linearity': 'Linearity and indicators'},
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
