# Problem sets 0.1, ratio levels 1 to 3: second-reader findings

Scope: `app/content/courses/ratio/problems-1.json`, `-2`, `-3`: 12 problems, 48 parts (46 numeric, 2 choice), 107 `wrong` entries. Rules: `docs/briefs/chained.md`. Pattern: `review-problems-1.4-c.md`.

Method. The author's script was run first. Each problem was read whole from its text, then solved again in `review-problems-ratio-1-3-scripts/mine.py`, which imports nothing from the author's script and types every figure from the prose. Route 1 is exact (`fractions`). Route 2 is another method: a percentage built from 10%, 1% and 0.1% blocks, compounding stepped month by month or year by year, a change taken from prices where the part uses multipliers, a unit rate taken the other way round. Every `wrong` value was rebuilt from the slip its line names and checked against its band, the key's band and its neighbours. Each number printed in a `feedback`, `byKey`, `why` or `explain` string was recomputed. Each slip was then rounded in the form its part asks for, to see whether it still reaches its line. Every numeric part went through the engine's own grader in node (`grade-probe.mjs`, `numGrade` of `grade.js`): the key, with one more place, after a letter and `=`, with a true minus sign, with its unit and as its `accept` text; each `wrong` entry on its own key; and 440 strings of my own (more and fewer places, the value a line prints after rounding, a decimal in a per cent box, the answer one step short, the commonest slip, currency written in front). `try-fix.mjs` tries the fixes below on in-memory copies with the same grader, and `proposed.py` computes their numbers twice. Level fit was read against the 13 lessons (what each teaches: percentages under 1% and over 100%, percentage points, multipliers to four places, simple against compound interest, inverse proportion by a fixed product, dividing by a rate) and number-sense level 3 for the square root. Freshness was read by hand with `fresh.py`: the story nouns and key numbers of each problem searched in the ratio course and then in all of `app/content`, on top of `fresh-check.mjs --cross-numbers`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, does not say the form wanted, or refuses a sensible entry; `minor` = weak part, loose `wrong` entry, missing restatement, wording or freshness.

## Tool results

| check | result |
|---|---|
| author's script (scratchpad venv) | `problems-ratio-numbers.py` 981 checks, 0 failures, exit 0; `numbers_lib` 29 of 29 |
| `mine.py` (reader's own keys, slips, stated numbers, set shape, voice) | 1,242 checks, 0 failures, exit 0; 13 CLAIM lines (findings 1, 2, 3, 7, 8, 12, 14 and notes) |
| `grade-probe.mjs` (engine grader, 46 numeric parts) | 926 checks, 440 reader rows, 0 failures, exit 0; 4 rows held to be faults (findings 1, 10, 15) |
| `try-fix.mjs` (fixes of findings 1, 2, 5, 7, 8, 13, 15 on in-memory copies) | 77 checks, 0 failures |
| `proposed.py` (numbers of the fixes of findings 1, 3, 5, 8, 11, 12, 13) | 33 checks, 0 failures |
| `grade-all.mjs --file`, three sets | 17, 15 and 16 widgets, 0 failures each |
| validator | 0 errors; no warning on the three files; `manifest.json` unchanged |
| voice scan 35, course folder | 0 and 0; no exclamation mark, no em-dash, British spelling, £ throughout |
| `fresh-check.mjs --file --cross-numbers`, three sets | 0 hits; 15, 3 and 14 advisories, all read: chance matches of common figures, as the author says. It does not see findings 5, 6, 11 and 13 |
| browser, `playthrough.mjs` | not run (reader prompt) |

Result. All 48 keys agree with mine by two routes, and so do all 107 `wrong` values. Every `wrong` entry lands on its own key in the engine and has a line; no two bands touch and no band is wide enough to pass a wrong method. Every band takes the value its own feedback prints and the honest roundings of it. No learner is marked wrongly and no statement of method is false: there is no `wrong` finding. One line states a figure that does not follow from the figure beside it (finding 3) and one `why` line names a working that leads to the right answer, not to the option it sits on (finding 14). One prompt asks two things of one box (finding 10). The rest is minor: one slip that misses its line when rounded as asked, two bands that end exactly on the rounded slip, one missing restatement, two slips without a line, two unit boxes, and five reuses, three of them inside the ratio course and unseen by `fresh-check`.

Chains. Each later part restates the value it uses, except `p-platform-fee` part 3 (finding 4). The carried slip of the part before has a line in `p-laptop-sale` 2, `p-fund-two-years` 4, `p-print-run` 2 and `p-coffee-suppliers` 4; all four rebuild exactly. Each set has one problem at difficulty 5, three to five parts a problem, and 16 of 17, 15 of 15 and 15 of 16 parts typed.

## A. `problems-1`

1. `minor` | `ratio/problems-1.json` | `p-platform-fee` | `items[1].parts[3].widget.wrong` | a slip, rounded as the part asks, misses its own line.
   The part asks for the nearest whole per cent. The `one-place` slip is $24 \div 294 = 8.163\%$, so that learner types 8. The band is $0.0816 \pm 0.001$ (8.06 to 8.26), so 8 gets the generic line (`grade-probe.mjs`). The `upside-down` slip is exactly 122.5%; 122 and 123 sit on the edges of $1.225 \pm 0.005$ and land today only by floating-point luck.
   Fix (`try-fix.mjs`, `proposed.py`): `one-place` `tol` `{ "abs": 0.002 }`; `upside-down` `tol` `{ "abs": 0.006 }`. Values and lines stay. Nothing touches: the key band is 0.8063 to 0.8263 and `account-base` ends at 0.003.

2. `minor` | `ratio/problems-1.json` | `p-phone-rise` | `items[2].parts[3].widget.wrong` | two bands end exactly on the slip rounded as asked.
   The part asks for 1 decimal place. `upside-down` is 267.75%, so 267.8 (or 267.7); `saving` is 62.652%, so 62.7. Both sit on the edge of a band of $\pm 0.0005$. They reach their lines today (`grade-probe.mjs`), but only because the float difference falls the right side.
   Fix (`try-fix.mjs`): `tol` `{ "abs": 0.001 }` on `upside-down` and `saving`.

3. `minor` | `ratio/problems-1.json` | `p-savings-tax` | `items[3].parts[3].widget.options[2].why` | two figures that do not agree.
   "They differ by 0.03 percentage points, about £5.20." 0.03 points of £18,000 is £5.40. The true gap is 0.0289 points, which is the £5.20 ($702 - 696.80$).
   Fix: "You rounded 3.87% up to 3.9%. The tax-free account pays £702 and the taxed one keeps £696.80, which is £5.20 less."

4. `minor` | `ratio/problems-1.json` | `p-platform-fee` | `items[1].parts[2].question` | no restatement.
   "The fee is taken from the account." The part needs the rate (or the £29.40) and the £8,400 and restates neither; every other part of the set does.
   Fix: "The 0.35% fee is taken from the £8,400 account. Using one multiplier, what is the account worth after the fee, in pounds? Give your answer to the nearest penny."

5. `minor` | `ratio/problems-1.json` | `p-phone-rise` | `items[2]` prose and part 4 | freshness, another course.
   `equations/l9-story-to-equation` asks: "A phone contract costs £30 to connect and £12 a month." Here a phone contract costs £30.00 a month and the SIM-only deal £12.00. The task differs; the noun and both figures are shared.
   Fix (`proposed.py`, `try-fix.mjs`; parts 1 to 3 do not change): the SIM-only deal costs £14.00. Part 4 question: "A SIM-only deal costs £14.00 a month. Using the new price of £32.13, what percentage of it is the SIM-only price? Give your answer to 1 decimal place." `answer` 0.4357, `tol` 0.001, `accept` "43.6%". `wrong`: `old-price` 0.4667, `upside-down` 2.295, `saving` 0.5643, each `tol` 0.001. `correct`: "$14.00 \div 32.13 \approx 0.436$, which is 43.6%." `upside-down`: "You divided £32.13 by £14.00. The SIM-only price is the part: $14.00 \div 32.13$." `saving`: "That is the saving, £18.13, as a share of £32.13. The SIM-only price itself is 43.6%." `old-price` stays. `explain`: "The part is £14.00 and the whole is £32.13. $14.00 \div 32.13 \approx 0.4357$, so 43.6% to 1 decimal place."

6. `minor` | `ratio/problems-1.json` | `p-pension-split` | `items[0].parts[0]` | freshness, same course.
   $\tfrac{3}{8} = 37.5\%$ is the worked conversion of `l1-out-of-a-hundred` (the `derive` screen "turn $\tfrac{3}{8}$ into a percentage"); `number-sense/problems-1` also opens a problem on $\tfrac{3}{8}$. The story and every later number are new.
   Fix: none asked. It is the level's own fact used as a first step. If the ruling is read strictly, the whole problem must be renumbered, which is not worth the risk.

## B. `problems-2`

7. `minor` | `ratio/problems-2.json` | `p-laptop-sale` | `items[1].parts[2].widget.wrong` | a band ends exactly on the slip rounded as asked.
   The part asks for 1 decimal place. `sale-base` is $-6.952\%$, so $-7.0$; the band is $-0.0695 \pm 0.0005$. It lands today by the same luck as finding 2.
   Fix (`try-fix.mjs`): `sale-base` `tol` `{ "abs": 0.001 }`. The key band ends at $-6.55\%$ and `added` at $-5.05\%$, so nothing touches.

8. `minor` | `ratio/problems-2.json` | `p-laptop-sale` | `items[1].parts[0].widget.wrong` | the commonest slip but one has no line.
   The part has one `wrong` entry. A learner who takes 15% off the sale price again (£476.85) gets the generic line, which does not say what went wrong.
   Fix (`try-fix.mjs`, `proposed.py`): add `{ "id": "off-again", "value": 476.85, "tol": { "abs": 0.005 } }` with the line "You took 15% off the sale price. £561.00 is already the price after the cut, so divide by 0.85."

9. `minor` | `ratio/problems-2.json` | `p-share-week` | `items[0].prose` | a term no lesson of the course uses.
   "A small-cap share": the word appears nowhere in the ratio or number-sense courses and does no work in the problem.
   Fix: "A share closes at £72.50 on Monday and at £84.10 on Tuesday. On Wednesday it falls by the same percentage it rose on Tuesday."

## C. `problems-3`

10. `unclear` | `ratio/problems-3.json` | `p-partners-profit` | `items[0].parts[0].question` | two requests, one box.
    "Write the ratio ... in its simplest form. How many parts are there in all?" The box takes only the count. A learner who types `3:4:5`, the first thing asked, is not read and Check stays unavailable (`grade-probe.mjs`).
    Fix: "In its simplest form, how many parts does the ratio $18{,}000 : 24{,}000 : 30{,}000$ have in all?" (With finding 11: the same sentence with the new amounts.)

11. `minor` | `ratio/problems-3.json` | `p-partners-profit` | `items[0]` prose, parts 1 and 3 | freshness, same course, twice.
    `review-3` `r-simplify-three` simplifies £45,000, £60,000 and £75,000 to $3 : 4 : 5$, with the same `thousands` slip and the same closing sentence ("No whole number above 1 divides 3, 4 and 5"). `l9-sharing` `q-profit-total` is part 3 in small: "Two partners split a profit in the ratio 5 : 3. The smaller share is £1,200. What is the total profit?"
    Fix (`proposed.py`; £12,000, £16,000, £32,000 and $3 : 4 : 8$ are in no file of the course). Prose: "Three partners put £12,000, £16,000 and £32,000 into a business. ..." Part 1: key 15; `thousands` 60, "You divided by 1,000 only, giving $12 : 16 : 32$. All three still share a factor of 4."; `halved` 30, "You divided by 2,000, giving $6 : 8 : 16$. All three still share a factor of 2."; `correct` "Each amount divides by 4,000, so the ratio is $3 : 4 : 8$, which has $3 + 4 + 8 = 15$ parts."; `explain` "4,000 divides all three amounts: $3 : 4 : 8$. Nothing else divides 3, 4 and 8, so this is the simplest form. It has 15 parts." Part 2 ("Using 15 parts, ... the partner who put in £32,000 ..."): key 5,120 (one part $9{,}600 \div 15 = 640$, 8 parts); `equal` 3,200; `one-part` 640. Part 3 ("... the partner who put in £12,000 receives £2,850. Using the ratio $3 : 4 : 8$ ..."): key 14,250 ($15 \times 950$); `own-parts` 8,550; `one-part-share` 42,750. Part 4 ("A fourth partner joins with £8,000, so the stakes are now in the ratio $3 : 4 : 8 : 2$. Of an £11,900 profit ..."): 17 parts, one part 700, key 1,400; `old-parts` 1,586.67 (`tol` 0.01, "You divided by the old 15 parts. ... $3 + 4 + 8 + 2 = 17$."); `equal` 2,975. This also removes the clash of finding 12.

12. `minor` | `ratio/problems-3.json` | `p-partners-profit` | `items[0].parts[1].feedback.byKey.equal` | one value, two slips, one line.
    3,200 is the equal three-way split and also 4 parts, the share of the £24,000 partner. A learner who took the wrong partner is told "You split the profit equally."
    Fix if finding 11 is not taken (value and id stay): "That is an equal three-way split, and also the 4 parts of the £24,000 partner. The £30,000 partner holds 5 of the 12 parts: $5 \times 800 = 4{,}000$."

13. `minor` | `ratio/problems-3.json` | `p-print-run` | `items[1].prose`, parts 1 and 2 | freshness, same course.
    `review-3` `r-pumps`: "5 identical pumps empty a tank in 12 hours", 60 pump-hours. Here: "Five identical presses would print the order in 12 hours", 60 press-hours. Same numbers, same sentence, same product.
    Fix (`proposed.py`, `try-fix.mjs`; the product stays 60, so parts 2 to 4 keep their keys): "Four identical presses would print the order in 15 hours." Part 1: `direct` 30, `subtracted` 11; `correct` "The order takes $4 \times 15 = 60$ press-hours, so 8 presses take $60 \div 8 = 7.5$ hours."; `subtracted` "You took 4 hours off for 4 more presses. Presses times hours stays at 60, so the time is 7.5 hours."; `explain` "Presses times hours is fixed at $4 \times 15 = 60$. With 8 presses the time is $60 \div 8 = 7.5$ hours." Part 2: `direct` 3,360 with `tol` 0, "That uses 30 hours, from scaling the time the wrong way. With 7.5 hours the cost is £840."; `explain` second sentence "Four presses for 15 hours also make 60 press-hours, so the cost is the same."

14. `minor` | `ratio/problems-3.json` | `p-print-run` | `items[1].parts[3].widget.options` | the options do the step, and one `why` names the wrong working.
    The options print "at £22.00 per 1,000" and "at £23.33 per 1,000", so the scaling the part is about is already done. The `shop` line says "You compared £2.20 with £23.33 without scaling", but that comparison makes the rival look cheaper, which is the keyed answer.
    Fix: option texts "The rival printer", "The shop's own presses", "They cost the same". `shop` `why`: "Scale the rival's price first. Per 1,000 it charges $10 \times 2.20 = 22.00$ pounds, which is less than £23.33." The `same` line and the `correct` line stay.

15. `minor` | `ratio/problems-3.json` | `p-coffee-suppliers` part 1, `p-villa-split` parts 1 and 3 | `widget.unit` | bare boxes for francs and euros.
    The three parts have no `unit`, so the box shows nothing, while every pound part shows £. "CHF 27.50", the form the prose prints, is not read (`grade-probe.mjs`); "€540" is.
    Fix (`try-fix.mjs`): `"unit": "CHF"` on `p-coffee-suppliers` part 1 and `"unit": "€"` on `p-villa-split` parts 1 and 3. Keys, `accept` and `wrong` entries grade as before.

## Notes, no change asked

- `p-share-week` parts 3 and 4 and `p-fund-six-months` parts 3 and 4 ask the same two things (the net change of equal moves up and down, then the rise that restores the start). The second is harder (three pairs, a six-figure multiplier), so it stands, but the set would cover more with one of them changed in a later pass.
- `p-fund-two-years` part 2 finds a yearly rate with a square root. No screen of `l8-growth-on-growth` does this; the tool comes from `number-sense/l11-undoing-a-square` (the level's stated prerequisite), and the generic line gives the idea. `course.json` says level 2 "uses ... a square root to find a yearly rate", which only this problem does.
- `p-fund-two-years` part 4: the exact value is £11,014.6355, half a penny from a whole penny. The band takes 11,014.63 and 11,014.64, and the printed $6{,}250 \times 1.762342$ gives 11,014.6375, so no route is refused.
- `p-share-week` part 3: a learner who works from the rounded £70.64 of part 2 gets $-2.57\%$; the band takes it.
- `p-fund-six-months` part 2: one month's rise (£42,712.40) has no line; rare, left.

## Engine

- A currency code typed before the number ("CHF 27.50", "EUR 540") is not read by `numValue`, with or without a `unit`; a sign (£, €) or a word after the number is. Not added to `docs/BACKLOG-INBOX.md` by this reader, to keep the worktree to the review and its scripts.

## Verified

- Keys: 48 of 48 by two routes each (`mine.py`). `wrong` values: 107 of 107 rebuilt from the slip named; each inside its band, clear of the key band and of its neighbours.
- Printed numbers: every figure in `correct`, `generic`, `byKey`, `why` and `explain` strings recomputed, including the 1%, 10% and 0.1% blocks, $0.91^3 = 0.753571$, $1.09^3 = 1.295029$, $1.12^5 = 1.762342$, $0.9919^3 \approx 0.9759$, the check lines ($70.644 \times 1.0263$, $7{,}840 \times 1.12^3$, $50{,}746.60 \times 1.0247$) and the £48 saving on the print order. One pair disagrees (finding 3).
- Engine: every key, key with one more place, with a letter and `=`, a true minus sign, its unit and its `accept` text grades correct; every `wrong` entry lands on its own id and has a line; a decimal typed in a per cent box is refused; 436 of 440 reader rows behave as held.
- Bands: each takes the key and the rounding the part asks for, and the value its own line prints; none takes a `wrong` value or a neighbouring whole per cent that a wrong method gives.
- Explanations: all agree with their keys and have at most three sentences. Voice: no sentence over 35 words, no exclamation mark or dash, British spelling, £ for money, euros and francs written as the lessons write them.
- Level: every idea is taught by the end of its level (percentages under 1% in l1 and l2, percentage points in l3, four-place multipliers in l4, simple against compound in l8, fixed products in l11, dividing by a rate in l13), with the square root from the stated prerequisite. Every `skills` id is carried by a lesson of the level.
- Set shape: four problems a set, three to five parts, a 5 in each, 46 of 48 parts typed, both choices are judgements.

## Fix pass

Status: fixed 14 findings, disputed 0, deferred 1 (finding 6, by the orchestrator's ruling: the single common fraction 3/8 may stand). The engine note is now in `docs/BACKLOG-INBOX.md` under `Raised later (problems ratio):`.

1. platform-fee part 4, fixed: `one-place` tol 0.002, `upside-down` tol 0.006 (8 and 122, 123 now sit inside with room; key band and `account-base` untouched).
2. phone-rise part 4, fixed: `upside-down` and `saving` tol 0.001 (reworked with finding 5; typed 229.5 and 56.4 reach their lines).
3. savings-tax part 4, fixed: `same` why now "The tax-free account pays £702 and the taxed one keeps £696.80, which is £5.20 less." (828 - 0.4 x 328 = 696.80; 18,000 x 0.039 = 702; gap 5.20, two routes).
4. platform-fee part 3, fixed: question restates "The 0.35% fee is taken from the £8,400 account."
5. phone-rise, fixed: SIM-only deal £14.00. Key 0.3735 to 0.4357 (14 / 32.13 = 0.43573; exact fractions and float), `old-price` 0.4 to 0.4667, `upside-down` 2.6775 to 2.295, `saving` 0.6265 to 0.5643 (18.13 / 32.13), tols 0.001; accept "37.3%" to "43.6%"; correct, two byKey lines and explain follow. Parts 1 to 3 unchanged. Grep: "SIM-only" with £14.00 is in no other ratio, number-sense or equations file.
6. pension-split part 1, deferred by ruling: 3/8 is a single common fraction and may stand (the level's own fact as a first step); story and later numbers are new.
7. laptop-sale part 3, fixed: `sale-base` tol 0.001.
8. laptop-sale part 1, fixed: `off-again` 476.85 (561 x 0.85, two routes), tol 0.005, with the proposed byKey line.
9. share-week prose, fixed: "A share closes at ...".
10. partners-profit part 1, fixed with finding 11: the question asks only for the count.
11. partners-profit, fixed: stakes £12,000, £16,000, £32,000, ratio 3 : 4 : 8 (gcd 4,000, checked by listing). Part 1 key 15, `thousands` 60 (12+16+32), `halved` 30. Part 2 key 5,120 (9,600 / 15 = 640, x 8), `one-part` 640, `equal` 3,200. Part 3 key 14,250 (2,850 / 3 = 950, x 15), `one-part-share` 42,750. Part 4 key 1,400 (11,900 / 17 = 700, x 2), `old-parts` 1,586.67, `equal` 2,975. All lines and explanations follow. Fresh grep: "12{,}000 : 16", "3 : 4 : 8", 14,250 and 5,120 (ratio) occur in no other course file; £32,000 and £16,000 appear in `ratio/homework-3` as an unrelated £80,000 split, judged chance.
12. partners-profit part 2 `equal`, closed by finding 11: 3,200 is no partner's share (1,920, 2,560 or 5,120).
13. print-run, fixed: four presses, 15 hours (product still 60; parts 3 and 4 and the keys of parts 2 to 4 unchanged). Part 1 `direct` 19.2 to 30, `subtracted` 9 to 11; part 2 `direct` 2,150.4 to 3,360 (8 x 30 x 14), tol 0; correct, byKey and explain follow. `review-3` r-pumps still has the product 60 with other numbers and another story; judged distinct.
14. print-run part 4, fixed: options "The rival printer", "The shop's own presses", "They cost the same"; `shop` why is the proposed line; `same` and `correct` stay.
15. unit boxes, fixed: `CHF` on `p-coffee-suppliers` part 1, `€` on `p-villa-split` parts 1 and 3.

Graded values changed (old to new): p-phone-rise p4 key 0.3735 to 0.4357, old-price 0.4 to 0.4667, upside-down 2.6775 to 2.295, saving 0.6265 to 0.5643; p-laptop-sale p1 wrong +1 (off-again 476.85); p-partners-profit p1 key 12 to 15, thousands 72 to 60, halved 36 to 30; p2 key 4,000 to 5,120, one-part 800 to 640; p3 key 11,400 to 14,250, one-part-share 34,200 to 42,750; p4 key 1,700 to 1,400, old-parts 1,983.33 to 1,586.67; p-print-run p1 direct 19.2 to 30, subtracted 9 to 11; p2 direct 2,150.4 to 3,360. Band-only changes: platform-fee p4 (2), phone-rise p4, laptop-sale p3.

Scripts: `docs/reports/problems-ratio-numbers.py` updated to the new values (1,003 checks, exit 0, tolerances and unit checks added); the reader's `mine.py` updated likewise (1,246 checks, 0 failures, exit 0; its remaining CLAIM lines are findings left or notes). `proposed.py` is unchanged and still passes (33 of 33).

Gates: validator 0 errors, 4,520 warnings, none on the three sets, `manifest.json` unchanged; `grade-all.mjs --local-cdn --file` 0 failures on all three (17, 15, 16 widgets); voice scan 35: 0 and 0; `playthrough --problems ratio/problems-1`, `-2`, `-3`, each desktop and `--mobile`: all six passed.
