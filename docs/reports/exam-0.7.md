# Topic 0.7 exam: getting hired

File: `app/content/exams/topic-0.7.json` (id `topic-0.7`, 70 minutes, pass 0.7). One course: `recruiting`, lessons l1 to l15, reviews and homework 1 to 3.
Generator and checks: `scratchpad/exam-0.7/` (`gen.py` builds the file, `calc.py` recomputes every number, `lint.py` checks the copy rules, `dump.py` extracted the course text read before writing).

## Shape

30 items (the validator cap), ordered by difficulty.

| Difficulty | Items | Share | Ramp |
|---|---|---|---|
| 2 | 6 | 20% | 20% |
| 3 | 15 | 50% | 50% |
| 4 | 6 | 20% | 20% |
| 5 | 3 | 10% | 10% |

Widgets: 14 choice, 7 multi, 4 numeric, 2 tap-regions (table rows), 1 order (with a distractor line), 2 longform (10-point rubrics, full model answers). Every `choice` and `multi` has `shuffle: true`.

| # | id | d | skills | lesson(s) | decision tested | widget |
|---|---|---|---|---|---|---|
| 1 | e-posting-tasks | 2 | landscape | l1 | Prepare by tasks, not title (developer tasks under a trader title) | choice, table |
| 2 | e-whose-money | 2 | landscape | l2 | Firm type that fits own-money quoting with same-day feedback | choice |
| 3 | e-days-to-close | 2 | landscape | l3 | Days from 2 Nov 2026 to a 10 Jan 2027 deadline | numeric |
| 4 | e-cv-cut | 2 | apply | l6 | Lines to cut or rewrite | tap-regions, table |
| 5 | e-video-opening | 2 | assess, behave | l10 | First sentence on camera | choice |
| 6 | e-aloud-opening | 2 | behave, assess | l12 | Say the plan, then the count | choice |
| 7 | e-cycle-penultimate | 3 | landscape | l3 | Third year of four today: apply now to open summer 2027 roles | choice |
| 8 | e-month-pay | 3 | landscape, offer | l2, l14 | Monthly pay over 10 weeks | numeric |
| 9 | e-research-prep | 3 | landscape, assess | l4 | Invented fund's page into a preparation list | multi, table |
| 10 | e-dated-notes | 3 | landscape | l4 | Dated, official, reported and disputed facts next July | choice, table |
| 11 | e-cv-rewrite | 3 | apply | l6 | Duty line rewritten as verb, task, tool, number | choice |
| 12 | e-uk-cv | 3 | apply | l6 | UK CV conventions | multi |
| 13 | e-why-research | 3 | apply, behave | l8 | Why us for research: fact, evidence, research reason | choice |
| 14 | e-attempt-protect | 3 | assess | l9 | Steps that protect the one real attempt | multi |
| 15 | e-video-slip | 3 | assess, behave | l10, l12 | One-take slip: fix in one clause | choice |
| 16 | e-star-faults | 3 | behave | l11 | "We", a numberless result, a disguised strength | multi, table |
| 17 | e-aloud-fix | 3 | behave, assess | l12 | Catching a double count aloud (11/36) | choice |
| 18 | e-five-rounds | 3 | assess | l13 | Chance of at least one bad round | numeric |
| 19 | e-intern-week-six | 3 | offer | l14 | Return offer: finish the project you own | choice |
| 20 | e-test-rejection | 3 | offer | l15, l9 | After an automated test rejection; no second account | order |
| 21 | e-msc-routes | 3 | offer, landscape | l15, l3, l5 | Off-cycle after the course, other firms, one request | multi |
| 22 | e-target-rows | 4 | landscape, apply | l5 | Eligibility, then fit, for one candidate | tap-regions, table |
| 23 | e-fewer-better | 4 | landscape, apply | l5, l15 | 20 at 5% against 10 at 12% | choice |
| 24 | e-guess-policy | 4 | assess | l9 | Guess with two out, leave blind items blank | numeric |
| 25 | e-final-day | 4 | assess, behave | l13 | Reset, start at zero, honesty, questions to ask | multi |
| 26 | e-conditional-offer | 4 | offer | l14, l2 | Check an open work condition before comparing | choice, table |
| 27 | e-pairs-follow-up | 4 | apply, behave | l7 | Defending an out-of-sample number | choice |
| 28 | e-week-mistakes | 5 | all five | l2, l3, l6, l8, l9, l14, l15 | A week's log: pick the four mistakes | multi, table |
| 29 | e-cycle-plan | 5 | landscape, apply, assess | l3, l4, l5, l9 | A dated plan to July 2027 | longform |
| 30 | e-star-disagree | 5 | behave, assess | l11, l12 | A STAR answer from notes, plus a follow-up | longform |

Skills: all 5 covered (`skills` map copied from `recruiting/course.json`): rk-landscape 12, rk-assess 12, rk-behave 10, rk-apply 9, rk-offer 6. Every lesson objective l1 to l15 is tested by at least one item.

## Content rules followed

- No firm is named. l4 facts appear only as firm types ("a trading firm's official rule: no retake within 8 months"). Every firm in an item is invented and says so.
- Dated facts match the lessons as of 2 November 2026: postings July and August, rolling review, offers late October to mid-December; spring weeks two years from graduation; off-cycle 3 to 6 months; recorded rounds about 30 s preparation, about 2 minutes, usually one take; 8-month official retake rule at one firm; offer deadlines of one to two weeks; return rates 70% to 80% at trading firms and about 50% at banks, as reported.
- No lesson, review or homework item is reused. A string comparison against every recruiting file found only short shared fragments (a table header, "Which answer is strongest?"); two shared `why` lines were reworded.
- Copy lint (`lint.py`): no `!`, no em or en dashes, no sentence of 20 words or more, explanations at most three sentences, no listed American spellings.

## Numbers computed twice (`calc.py`)

| Item | Value | First method | Second method |
|---|---|---|---|
| 3 | 69 days | `date` difference | 28 + 31 + 10; 2 Nov + 59 days = 31 Dec |
| 8 | £27,692 | 12,000 × 12 × 10/52 | 12,000/(52/12) × 10; £144,000/52 = £2,769 a week |
| 6 | 6/36 | enumeration of 36 cells | 3 + 2 + 1 |
| 17 | 11/36 | enumeration | 1 − 25/36 and 12/36 − 1/36 |
| 18 | 0.556 | 1 − 0.85⁵ = 0.5563 | sum over all 31 bad-round patterns; wrong keys 0.75, 0.444, 0.478 (four rounds) |
| 23 | 0.358 and 0.279 | 0.95²⁰, 0.88¹⁰ | expected offers 1.0 and 1.2 |
| 24 | 2 marks | exact fractions: two left 1/4, one out 0, blind −1/8 | all 14 guessed 5/4; no penalty 4 |
| 26 | £38,000 and £11,538 | 3,800 × 10; 60,000 × 10/52 | 60,000/52 × 10 |
| 11 | 8 times | 120/15 | |
| 15 | 50 s left | 120 − 70 | |
| 20 | 20 July 2027 | 8 months on from 20 Nov 2026 | month list Dec to Jul |
| 29 | 241 days, 34 weeks | `date` difference | 28+31+31+28+31+30+31+30+1; 241 = 7 × 34 + 3 |
| 29 | −0.5, 6 s | 1/4 − 3/4 | 480/80 |
| 30 | about 150 words | word count of the model's part (a): 147 | 147/130 ≈ 1.1 minutes |

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors, no warning for this file; the manifest now lists `exams/topic-0.7.json`.
- `playthrough.mjs --exam topic-0.7 --local-cdn <pkgs>`: 30 of 30, passed. With `--mobile`: 30 of 30, passed.
- Screenshots reviewed (`scratchpad/exam-0.7/shots`, desktop and 390 px). Fixes made from them: the target-list table's programme names shortened so the dates wrap less at 390 px; "Scroll the table to the end" moved into the prose of the three long tables, since a caption under a scrolling table is out of sight; the one KaTeX option in item 17 rewritten as plain text, because it was the only typeset option and gave the answer away.
- The `--why` results page screenshot stops painting after item 21 (the rest of the 28,463 px capture is blank), so the two longform model answers, including the Markdown table in item 29's model, were not seen rendered. AUTHORING section 2 says tables render in long-form model answers.

## Engine notes

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (exam 0.7)".
