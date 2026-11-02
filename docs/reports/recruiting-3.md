# Report: recruiting level 3 ("Interviews and after")

Status: done. Authored 2 November 2026. No firm is named anywhere in level 3 (orchestrator's rule): firm facts are pointers to l4 or l2 with their date, or third-party sources cited by title and firm type ("one high-frequency firm", "a bank and an asset manager"). Invented candidates: Tom (the failure story), Maya (the charity quiz), Leo, Priya, Ana, Ravi, Ella, and Nadia, reused from levels 1 and 2 for the six stories, the final-round day, the offers and every model answer. Invented firms: Firm A, Firm B, Bank C.

## Files written (`app/content/courses/recruiting/`)

| File | Contents |
|---|---|
| `l11-stories-that-answer.json` | 12 screens: problem (Tom's 8-sentence failure story, `table` widget labelling S, T, A, R with `accept` lists), problem (STAR named; the reflection line), ladder (tap the "we" sentence), ladder (the result with a number), two ladders (coverage grid of six stories against six question types, 3 columns a screen, Yes/No text cells), ladder (one story opened three ways), trap ("I would" and the disguised strength), ladder (edge case: a supermarket job), generalise (15 + 10 + 60 + 20 + 15 = 120 s, 130 words of action), follow-up problem ("How do you know it would not happen again?"), transfer (multi: six of Nadia's nine experiences). 4 quiz. `rk-behave`. |
| `l12-reasoning-aloud.json` | 12 screens: problem (`pair` of two `console` transcripts, `tap: "sides"`: silent 4.25 against the five moves), problem (tap the anchor line), ladder `order` (first head, distractor "stay silent"), ladder (tap the line that ignores a hint), ladder (the check that catches "worth 6"), ladder (stuck: say what you know), trap (Ravi's digit stream), ladder (edge case: fixing your own slip), generalise ($\min X \le E[X] \le \max X$), speaking practice (coin game aloud, phone timer, then tick the model's moves), follow-up problem (two rerolls: 14/3), transfer (`console` market on a novel's word count, tap the assumption). 4 quiz. `rk-behave`, `rk-assess`. |
| `l13-the-final-round.json` | 12 screens: problem (`number-line` 9 to 17 with four 45-minute rounds and lunch; drag "Bad round" onto round 2), problem (round 3 starts at zero; the three parts named), ladder `order` (the 60-second reset, distractor "replay the mistake now"), ladder (answer, check, offer depth), ladder (round 4 behavioural: pick the l11 story), problem (`boxes`: Ask and Do not ask, `place` boxes mode), trap (apologising for round 2), ladder (edge case: a question seen before), generalise ($1 - (1 - p)^n$, five rounds 0.672), problem (remote final round set-up, multi), follow-up problem ("What would you want to own?"), transfer (`order` the day-before checklist, distractor "a new puzzle book"). 4 quiz. `rk-assess`, `rk-behave`. |
| `l14-offers-and-deadlines.json` | 12 screens: problem (`number-line` days 0 to 21; drag "Tell B" to day 1, `tol` 1), problem (`order` of the offer moves, distractor "say nothing"), ladder (the extension email), ladder (4-column `table` widget comparing two offers, numeric cell £43,500), ladder (accepting means withdrawing; reneging), ladder (multi: what counts towards a return offer), trap (accept to be safe and renege, or let the deadline pass), ladder (edge case: a summer 2027 offer while planning 2028), ladder (edge case: a conditional offer), generalise (yearly × w/52, £60,000 for 9 weeks), follow-up problem (B can decide by day 12), transfer (29 of 55 return offers: 52.7%). 4 quiz. `rk-offer`. |
| `l15-after-a-rejection.json` | 11 screens: problem (three rejection emails, tap the one after a final round), problem (`order` of the rejection cycle, distractor "reply that it was unfair"), ladder (the feedback request), ladder (`number-line` of months: November 2026 to July 2027 is 8), ladder (multi: off-cycle and other routes), ladder (`table` widget: what failed, the skill, the app course), trap (resend next week, or read one no as a verdict; link to l5), ladder (edge case: two firms that share a name, l2), generalise ($(1 - p)^n$ with n = 20: 0.358 against 0.12), follow-up problem (one line of feedback), transfer (`order` of the next 30 dated days, distractor "40 more firms with the same CV"). 4 quiz. `rk-offer`. |
| `review-3.json` | 9 items, difficulty 2 to 4, every item with `skills` and `tags`: STAR labels on a new 4-sentence story (table text cells); the "we" sentence (table, tap); the missing move in a transcript (console, choice: the check); a final-round question to ask; the day to tell another firm (drag-point, new numbers); 18 of 24 return offers (75%); December 2026 to July 2027 (7 months); three rounds at 0.25 (0.578); the shared weakness after ten rejections. No longform. |
| `homework-3.json` | 9 items, every item with `skills` and `tags`: six behavioural stories in the brief's order (project, failure, decision with incomplete information, team, disagreement, learning fast under pressure), each `longform` with a 10-point rubric tuned in its last line, models for Nadia in six settings (a project, study, a contest, a sports team, a part-time job, a society), difficulty 4 and 5 for the failure; an `order` of the reasoning moves on a new puzzle (5 or 6: E = 3), difficulty 4; a `multi` on an offer with a deadline, difficulty 4; the optional final-round plan (`longform`, difficulty 3, rubric of 10). |

Interview form, as in level 2: each lesson has one screen opening "**Follow-up.**" with a pace in its prose, and l12 has a speaking-practice screen ("answer aloud now ... nothing is recorded ... then mark this model"). `tags` (kebab-case families: `star-story`, `star-follow-up`, `reasoning-aloud`, `reasoning-follow-up`, `final-round`, `final-round-follow-up`, `offer-deadline`, `offer-follow-up`, `return-offer`, `after-rejection`, `rejection-follow-up`) sit on every review and homework item and on each lesson's follow-up, speaking-practice and transfer screen. Every `choice` and `multi` has `shuffle: true` except the ordered date options in the l14 quiz. Each lesson's last screen says what homework 3 asks for. No audio anywhere; every spoken task says "answer aloud" and "use a phone timer; nothing is recorded".

Helper scripts are in the scratchpad folder `recruiting-3`: `common.py`, `l11.py` to `l15.py`, `sets.py` (generators), `lint.py` (sentence length, em-dashes, `!`, American spellings, sentences per explanation, prose words), `rc3_numbers.py` (every number twice), `scroll.mjs` (scrolled 390 px captures).

## Validator and playthrough

- `node tools/validate.mjs`: **0 errors**; no warnings on any recruiting file (the course's "not yet written" warning is gone: all 15 lessons, 3 reviews and 3 homework files exist).
- `node tools/playthrough.mjs --lesson recruiting/<id> --local-cdn <pkgs>`: l11 16 checks, l12 16, l13 16, l14 16, l15 15; every quiz 4/4; all passed. The same five again with `--mobile`: all passed. `--set recruiting/review-3`: 9 of 9 recorded, passed. `--set recruiting/homework-3`: 9 of 9, 78 of 78 marks, passed. All rerun after the last edits.
- Screenshots: every screen at 1280 and 390 px with `--mobile --why` (518 files), plus scrolled 390 px captures of the l11 coverage tables, the l13 day line and Ask cards, the l14 offer table, and the l15 email table, months line and course table. Faults found and fixed: the l11 coverage widget ran off the right edge at 390 px (headers cut to one word, placeholders to "?", "Treasurer" renamed "Society"; it still scrolls about 20 px, see the inbox); the l13 Ask cards overflowed their outlines in a two-column deck (labels cut to 12 characters or fewer, deck one column); the l13 hook title gave the answer ("A bad round at 10:30", now "A final-round day"); the "Bad round" label sat on the round bars (now below the axis); the l15 "2028 postings open" label ran into the interval label (dropped; the interval names it); the l12 4.25 marker hid under the "Allowed" bar (bar moved up a row).

## Deviations from the brief

- No firm is named in level 3 (orchestrator's rule). F10 is "one trading firm's official rule: no retake within 8 months (l4, read October 2026)"; F8 is "another's official posting says reapply when the next season opens (October 2026)"; F16 is "two firms that share a name, a hedge fund and a market maker (l2, as reported 2026)"; F13's 29 of 55 is "one high-frequency firm"; F4 is "a bank and an asset manager list official 2027 off-cycle roles in London".
- l11's coverage grid states that every column holds two or more stories, rather than "six stories answer twenty questions": the brief's twenty is not a count the grid shows, so it is not stated as a number.
- l11's hook asks for S, T, A, R only; the reflection line is named on the next screen, as the brief's "plus one line of reflection" suggests.
- l13's hook drag and its "what happens to round 3" choice are two screens (one widget a screen).
- l14's offer table and its "pay gap matters less than the return rate" point share one screen: the numeric cell is graded and the point is in the explanation; the choice on what you can control is the l14 quiz item `q-control`.
- l15's hook table has the columns stage reached, what the email says, and sent by. The brief's third column, "what you may ask for", would have given the answer in the table.
- l12's market-making preview uses a word count of a 300-page novel (300 × 300 = 90,000); the brief left the quantity open.
- The final-round plan (homework item i, optional) is included, so the homework has 9 items.

## Firm and source references (all dated)

| Reference | Where | Date given | Source line |
|---|---|---|---|
| Final days of three to five interviews (three back-to-back at one bank, up to five 45-minute at one trading firm) | l13 hook | October 2026 | l4 |
| One trading firm: no retake within 8 months (official, F10, F14) | l15 waits ladder, review `r3-months-retry` | read October 2026 | l4 |
| Another trading firm's posting: reapply when the next season opens (official, F8) | l15 waits ladder | October 2026 | the firm's posting, as in the fact table |
| Most firms publish no rule; about 12 months reported (F14) | l15 waits ladder | 2022 to 2026 | forums |
| Exploding offers average about two weeks; extension requests often refused (F15) | l14 name screen, l14 email ladder | April 2004 (old: said so) | eFinancialCareers, "How to handle an exploding job offer" |
| Offers with one- to two-week deadlines (F2) | l14 name screen | 2026 | Quantt's UK guide to quant internships |
| £4,350 a week at one London trading firm (F12) | l14 table ladder, generalise | September 2026 | TraderMath salary guide |
| Bank summer analysts about £65,000 a year pro rata (F12) | l14 table ladder, generalise | 2026 | a 2026 London salary blog |
| Return rates 70% to 80% at top trading firms, about 50% at banks; decisions in the last weeks (F13) | l14 table and return-offer ladders, review `r3-return-rate` | 2026 | Quantt guides, no named sources |
| 29 return offers to 55 interns in a weak year (F13) | l14 transfer | November 2023 | eFinancialCareers, anonymous insiders |
| Official 2027 London off-cycle roles of 3 to 6 months at a bank and an asset manager (F4) | l15 routes ladder | read October 2026 | the two postings in the fact table |
| Two firms that share a name are separate employers (F16) | l15 edge case | as reported 2026 | l2 |
| Netherlands right to work as an offer condition (pattern from F8) | l14 conditional-offer edge case | invented offer letter | none needed (no firm) |

## Numbers (each computed by script, `rc3_numbers.py`, and by a second route)

| Number | Where | Route 1 | Route 2 |
|---|---|---|---|
| 15 + 10 + 60 + 20 + 15 = 120 s; actions 130 words; S and T 25 s = 54 words | l11 generalise, summary | sum; 130 × 60/60 | half of 260; 130 × 25/60 = 54.17 |
| £1,900 raised, £400 more than last year (£1,500) | l11 ladder | subtraction | £1,500 + £400 |
| One free reroll: 2.5 + 1.75 = 4.25 | l12 hook, name, check | floats | Fraction 17/4 |
| Two rerolls: 11/6 + (4/6) × 4.25 = 14/3 ≈ 4.67 | l12 follow-up | floats | Fraction 14/3 |
| Flips to first head 2; rolls to first six 6; to a 5 or 6, 3 | l12 order, hint ladder; homework order | $E = 1 + (1 - p)E$ | $1/p$ |
| All six faces: 6(1 + 1/2 + ... + 1/6) = 14.7 | l12 stuck ladder | float sum | Fraction sum |
| Two red from 3 red, 2 blue: 3/5 × 2/4 = 0.3 | l12 trap | float | Fraction 3/10 |
| Total of 7: 6 of 36 = 1/6 (not 3/36 = 1/12) | l12 edge case | enumeration of 36 pairs | Fraction 6/36 |
| Coin +£2/−£1: £0.50; +£3/−£2: £0.50 | l12 speaking practice, quiz | 0.5 × 2 − 0.5 × 1 | Fraction 1/2 |
| Model answer 64 words = 29.5 s | l12 speaking practice | word count | 64/130 min |
| 300 × 300 = 90,000 words; market 70,000 to 110,000 | l12 transfer | product | ±20,000 about 90,000 |
| Two aces: 12/2652 = 1/221 ≈ 0.45% | l13 pacing ladder | float | Fraction 1/221 |
| $1 - 0.8^n$: 0.20, 0.36, 0.488, 0.5904, 0.67232 | l13 generalise | float | Fraction (and a 200,000-day simulation: 0.673) |
| $1 - 0.9^3 = 0.271$; $1 - 0.75^3 = 0.578$ | l13 quiz; review | float | Fraction 271/1000, 37/64 |
| Broken stick makes a triangle: 1/4 | l13 edge case | known result | Fraction |
| £4,350 × 10 = £43,500; £65,000 × 10/52 = £12,500 | l14 table, generalise | product | Fraction 650,000/52 |
| £60,000 × 9/52 = £10,384.6 (wrong keys 10 weeks £11,538.5, 9 months £45,000); £1,154 a week | l14 generalise | float | Fraction |
| £3,200 × 12 = £38,400 | l14 quiz | product | £32,000 + £6,400 |
| 29/55 = 0.527; 26/55 = 0.473 | l14 transfer | float | Fraction |
| Day 0 = 2 March 2027: day 14 16 March, day 18 20 March, day 19 21 March, day 21 23 March | l14 email ladder | date arithmetic | count of days |
| 3 May + 10 = 13 May; 9 to 13 May is 4 days; 1 to 15 March is 14 days | l14 quiz; homework offer | date arithmetic | count of days |
| Day 1 or 2 leaves 12 or more days to day 14; review: 9 and 4 days to day 10 | l14 hook; review | subtraction | count on the line |
| November 2026 to July 2027: 8 months; October: 9; December: 7; December + 8 months = August 2027 | l15 ladder and quiz; review | month arithmetic | month count by hand |
| $0.95^{20} = 0.358$; $0.9^{20} = 0.122$; $0.85^{20} = 0.039$; cut by about two thirds (0.66) | l15 generalise, summary | float | Fraction powers |
| 1 December + 30 days = 31 December | l15 transfer | date arithmetic | count of days |
| 18/24 = 0.75; 5 members to 18 | review | float | Fraction 3/4 |
| Module mark 0.25 × 52 + 0.75 × 71 = 66.25 | homework failure model | float | Fraction 265/4 |
| Trading game: 100 shares × (£100 − £70) = £3,000; 15% fall to £85 loses £750 on 50 shares, £1,500 on 100 | homework decision model | products | by hand per share (£15) |
| Model stories: 174, 150, 169, 155, 169, 155 words = 80, 69, 78, 72, 78, 72 s at 130 a minute | homework | regex word count | `wc -w` on the extracted text |

The 0.2 and 0.25 chances of a bad round are stated as illustrations, not reported rates.

## Proposed change to `course.json`

None.

## Engine limits (4 bullets in `docs/BACKLOG-INBOX.md` under "Raised later (recruiting level 3):")

Table widget inputs too wide for a 4-column grid of Yes/No cells at 390 px; table widget cells always centred; no word count or spoken-time estimate under a `longform` answer; a number-line point label drawn over stacked interval bars. Already raised and not repeated: the hard-coded longform placeholder and the homework time estimate (recruiting level 2), lesson countdowns E6 (recruiting level 2), follow-up parts and a pace field E11 and E9 (mental-pressure level 2), `tags` undocumented and unchecked (puzzles level 2), a table cell's own `wrong[]` id refused as a `byKey` key (recruiting level 1, puzzles level 2; l14's one-week slip is keyed on the cell id instead), and E19 dates on lessons (recruiting level 1).
