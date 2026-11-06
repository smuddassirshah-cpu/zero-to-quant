# Report: exam mock-video (recorded video interview)

Brief: `docs/briefs/mocks.md`, section `## mock-video` (written first in this task, appended at the end of the file).

## Files

- `app/content/exams/mock-video.json` (new): 5 papers of one `longform` prompt each, 2 checks.
- `docs/briefs/mocks-scripts/mock_video_build.py` (new): writes the JSON; holds every prompt, rubric, model and timing; asserts each number two ways.
- `docs/briefs/mocks-scripts/mock_video_check.py` (new): second route; imports `app/tools/numbers_lib.py`; 155 checks, exit 0.
- `docs/briefs/mocks.md`: `## mock-video` appended (no other section touched).
- `docs/readiness.md`: the four hand-written `mock-video` rows now read "exists" (lines 263, 526, 653, 781); `node tools/readiness-sums.mjs --write` then regenerated `app/content/readiness.json` (mocks present and missing per role). No generated block in the markdown changed.
- `docs/BACKLOG-INBOX.md`: 5 bullets under `Raised later (mock mock-video):`.

## Shape

| # | Paper | Prompt | Think | Answer (`seconds`) | Paper minutes | Item, family |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `motivation` | What do you expect to find hardest in a quant internship, and how are you preparing for it? | 30 s | 120 s | 2.5 | `v1-hardest-part`, `hardest-part` |
| 2 | `someone-elses-error` | A mistake you found in someone else's numbers | 30 s | 120 s | 2.5 | `v2-others-error`, `others-error` |
| 3 | `more-work-than-time` | A week with more work than time: what you dropped | 30 s | 120 s | 2.5 | `v3-too-much-work`, `too-much-work` |
| 4 | `many-signals` | Technical, researcher: 100 signals at 5%, none with an edge | 30 s | 90 s | 2 | `v4-many-signals`, `many-signals` |
| 5 | `halving-search` | Technical, strats: binary search on 1,000,000 sorted prices | 30 s | 90 s | 2 | `v5-halving-search`, `halving-search` |
| 6 | check `one-take` | I answered every prompt aloud, in one take each | | | | |
| 7 | check `marked-from-recording` | I marked each answer from my recording or a friend's notes | | | | |

5 prompts, 690 s = 11.5 minutes on the clocks, 2 checks. Every paper: `scoring` 1/0/0, `pass: 1`, `navigation: "forward"`, `skip: false`. Every item: difficulty 3, `tags: [family, "recorded-video"]`, `pace` = paper seconds, `seconds` = answer time, a 10-point rubric with one `required` time row and one filler-word row, a model labelled as an example with its word count and spoken time. No `followUps` (a one-way round has no interviewer). `requires: ["recruiting/l10-recorded-video"]`; style `research`.

Pass: the attempt passes when all five prompts reach 7 of 10 with the time row ticked and both checks are ticked. This is the author's line, not a published cut-off.

## Closest faithful version, and the engine gap that blocks it

- No microphone (DECISIONS, 29 Oct). The learner records on a phone or answers to a friend; the app times and gives the rubric.
- No thinking timer before an answer timer: each prompt is its own one-item paper, paper clock = thinking + answer time, which submits at zero (one take, no going back). The learner presses Start the clock when the thinking time is up; the amber last quarter falls inside the answer time.
- **Gap, Must:** an exam paper has no Mark my answer button for a longform item. Probed in Chromium on this mock (a real learner submitting all five papers scores 0 of 5; the results page shows each model and rubric locked at 0 of 10) and on `mock-superday-trader`. The playthrough passes only through the test hook. This mock cannot be passed by a real learner until the engine adds a marking step; bullet 1 in the inbox.

## Sources (what such rounds contain)

- `content/prep.json` (`asOf` 2026-10): JP Morgan official self-recorded video, reported three behavioural questions; Morgan Stanley official on-demand video; Goldman Sachs reported recorded video; IMC reported short recorded video in the first stage.
- `recruiting/l10-recorded-video`: about 30 s to prepare, about 2 minutes to answer, usually one take; 130 words a minute.
- Web, reported Nov 2026: [quantvault.org, JPMorgan HireVue video interview](https://quantvault.org/jpmorgan-hirevue-video-interview.html) (3 questions, about 30 s prep, 2 minutes at most, one retry); [Glassdoor, J.P. Morgan internship interviews](https://clear.glassdoor.nl/Interview/J-P-Morgan-Internship-Program-Interview-Questions-EI_IE145.0,10_KO11,29.htm) (no redo on most questions).
- Firm names appear only in `models` and `description`, with "reported, as of Nov 2026" (the check script asserts it).

## Numbers, each computed twice

| Place | Value | Route A (build) | Route B (check) |
| --- | --- | --- | --- |
| Clocks | 150, 150, 150, 120, 120 s; 690 s; 11.5 min | 30 + answer per prompt; sum | `minutes` × 60 = 30 + `seconds` = `pace`; Fraction sum = 23/2 |
| Models | 147, 144, 143, 139, 138 words; 68, 66, 66, 64, 64 s | `split()`, `round(Fraction(w·60, 130))` | regex `\S+`, integer half-up rounding |
| Prompt 1 | 20 × 6 = 120 problems | product | sum of six 20s |
| Prompt 2 | 1.1 × 0.9 = 0.99, a 1% loss; averaged 0% | Fractions; 100 → 110 → 99 | Decimal |
| Prompt 3 | 6 + 3 + 3 = 12 h, 12 − 3 = 9; 40/6 ≈ 6.7, 10/3 ≈ 3.3, 0 per hour | Fractions | Decimal |
| Prompt 4 | 100 × 0.05 = 5; 1 − 0.95^100 ≈ 99.4%; 0.05/100 = 0.0005 | n·α and a sum of 100 means; power and a product loop | binomial mean summed over k = 0..100; Decimal power |
| Prompt 5 | 20 comparisons; 2^20 = 1,048,576; 2^19 = 524,288; 500,000, 250,000; 50,000 | power, doubling loop, halving loop, `ceil(log2)` | `(10^6 − 1).bit_length()`, shifts |

The check script also confirms that every number in every prompt, model, rubric row, title, check, the description and `models` belongs to the set computed for that place, then runs `check_wrongs()` (no `wrong[]` here) and `report()`.

## Results

- Validator: `node tools/validate.mjs` 0 errors; no warning names `mock-video`.
- Voice scan on a copy (`VOICE_BASE` = scratchpad folder holding only `mock-video.json`): 0 sentences over 20 words, 0 explanations over three sentences (also 0 over 19).
- `python3 -I docs/briefs/mocks-scripts/mock_video_check.py`: 155 of 155, exit 0. The build script's asserts pass.
- `node tools/fresh-check.mjs --exam mock-video --min-run 10`: 0 hits. Grep of the key nouns: "find hardest" appears only in a recruiting homework-3 list of questions to ask an interviewer; "1,000,000 prices" setups in ds, cpp and algo-think are about memory and pointers, not search. Prompts avoid the recruiting course's team, challenge, why-this-role, project, failure, decision, disagreement and learn-fast prompts and the superday fit and case papers.
- Playthrough `--exam mock-video`: ok, 5 of 5, passed; mock checks ok. With `--mobile`: same, all passed.
- Screenshots looked at (scratchpad `exam-mock-video/`): start card at 1280 and 440 (description, Models line, part cards; the 440 part cards wrap narrowly, inbox bullet 4), prompts 1 and 5 with the 2:00 and 1:30 clocks at 1280 and 440, the checks page at 440, the results page passed (1280) and as a real learner (0 of 5, models and rubrics shown locked). No overlap or sideways scroll.
- `node tools/readiness-sums.mjs`: OK after updating the four hand-written rows and `--write`.

## Proposals

- No `prep.json` change (the entries exist). No `course.json` change.
- Engine: inbox bullets 1 (Must, marking in exam papers) and 2 (Should, thinking timer and a locking answer clock) are what make this mock usable and faithful.

## Build script (`docs/briefs/mocks-scripts/mock_video_build.py`)

```python
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
```

The check script is committed beside it (`mock_video_check.py`).
