# Problem sets: equations (brief `docs/briefs/chained.md`)

Files: `app/content/courses/equations/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-equations-numbers.py` (exits 0, 801 checks).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-family-tickets | 4 (4 / 0) | l1, l2, l3, l4 | 3 |
| problems-1 | p-food-van | 4 (4 / 0) | l1, l2, l3 | 4 |
| problems-1 | p-number-trick | 4 (3 / 1) | l1, l2, l3, l4 | 5 |
| problems-1 | p-market-pitch | 4 (4 / 0) | l1, l2, l3, l4 | 4 |
| problems-2 | p-climbing-wall | 4 (4 / 0) | l5, l6, l9 | 3 |
| problems-2 | p-cottage-share | 4 (4 / 0) | l6, l8, l9 | 4 |
| problems-2 | p-power-tariffs | 4 (3 / 1) | l5, l7, l9 | 4 |
| problems-2 | p-interest-split | 4 (4 / 0) | l6, l8, l9 (and l3) | 5 |
| problems-3 | p-bakery-stock | 4 (3 / 1) | l10, l11, l12 | 4 |
| problems-3 | p-fridge-temperature | 4 (4 / 0) | l10, l11, l12, l13 | 4 |
| problems-3 | p-van-value | 5 (4 / 1) | l10, l11, l12, l13 | 5 |
| problems-3 | p-fund-weight | 4 (4 / 0) | l12, l13 (and l10) | 4 |

Typed parts: level 1 15 of 16, level 2 15 of 16, level 3 15 of 17. Every lesson of the level appears in at least one problem, and every problem draws on at least two. Choice parts are judgements: whether two tricks always agree, which tariff suits a household, which number line, which double inequality.

Level 1 (expressions only; no part solves an equation). Tickets: a child price, the bill expanded and collected, factorised, then evaluated through the factorised form. Food van: a profit from words, a bracket with a decimal multiplier, two days collected, the weekend at 90 burgers. Number trick: two brackets with a negative multiplier, factorised, evaluated, then expanding settles that a second trick always agrees (the l2 point that one test does not prove it). Market pitch: a letter outside the bracket, $s(7s + 6)$, and $7s^2$ at $s = 4$ with the power-first slip.

Level 2. Climbing wall: form, solve, then two l9 roundings that go down (31 climbers; £7.28 in whole pence). Cottage: shares as fractions, cleared by 30, then a seventh friend to the nearest penny. Tariffs: a one-step solve (l5), the match by unknowns on both sides (l7), the judgement, then the saving past the match. Interest split: bond amount, equation, decimals cleared by 1000 (l8), then a second year's split.

Level 3. Bakery: form, flip, number line, then $4 < h \le 10$ counted. Fridge: Celsius as subject, 41 °F, the inequality that confirms it, then a freezer band counted in Fahrenheit. Van: $t$ as subject, an age, a flipped strict inequality, a flipped double inequality whose ends swap, then a count. Fund weight: the subject appears twice ($a = \tfrac{wb}{1 - w}$), the two ends of a band, then whole £250 blocks counted.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures (801 checks for the three sets) | same | same |
| validator | 0 errors, 0 warnings on the file | same | same |
| playthrough `--local-cdn` | green (16 parts) | green (16 parts) | green (17 parts) |
| playthrough `--mobile` | green; 440 px shots of every part read, no fault | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

Census: "Problem sets 39 (items 151)".

Besides the script, every answer, accept form, wrong form and about 130 typed strings were put through the engine's own graders in node (`grade.js` with the local Compute Engine, and the form checks of `expression.js`). That found two things now fixed: a `wrong` equation for interest that graded correct, and a band of 0.001 that refused 0.83 for the slip 0.8333.

## Review 1.3 (a) faults avoided

- Bands take the printed working. Each numeric part's last printed figure in `feedback.correct` is accepted (checked in the script). Two parts end on a rounding decision, so their last printed figure is the unrounded value (climbing parts 3 and 4); there the answer is the rounded one, stated in the same line. The nearest-penny part (cottage part 4) has band 0.005 on 115.71, which takes 115.714 and 810/7.
- Each `accept` line on a numeric part is the plain number the field takes; none promises a form `parseNum` cannot read.
- No `%` units. Money answers say "in pounds"; decimal answers say "Give a decimal".
- Slips from the part before carry their own `wrong` where a learner would carry them (the bracket that does not reach in tickets, food van and pitch; $\tfrac{x}{5} + 20$ in the cottage).

## Fresh-check

All three sets: 0 hits at the gate. At `--min-run 8 --min-share 0`: problems-1 and problems-2 0 hits; problems-3 one hit, "make # the subject of # the letter # appears twice" against `homework-3` `hw3-subject-twice`, share 0.09: the stock sentence l13 uses. The formula there is $y = \tfrac{x + 2}{x - 1}$; here it is a fund weight.

Read by hand against the course's lessons, quizzes, reviews, homework and `topic-0.2`:
- No setting repeats. The course uses brokers, shares, taxis, phone contracts, gyms and break-even. These sets use theatre tickets, a food van, a number trick, market pitches, a climbing wall, a cottage, tariffs, an interest split, a bakery, a fridge, a van and a fund.
- Shapes that recur, judged acceptable: two plans that cost the same (tariffs part 2) is the idea of `review-2` `rv-two-brokers` and l7's transfer, with new numbers and a new story; it appears once in level 2. A decreasing value held in a band (van parts 3 to 5) is l12's idea, as in `review-3` `r3-bond-band`; here it comes through a formula made subject first and asks a count. A count of whole sizes in a band (fund part 4) meets `homework-3` `hw3-margin-range`; the count here is 9, not 5, from £250 blocks. Two brackets with a minus between them (number trick) is `homework-1` `h-simplify` and `topic-0.2` `e-expand-two`'s skill, with other numbers, a story, and a factorise and a proof after it.

## Engine limits

Three bullets to `docs/BACKLOG-INBOX.md` under "Raised later (problems equations)": `form: "simplified"` takes a factorised answer; the Accepted line on a `form` widget; an equation `wrong` with the key's root grades correct.
