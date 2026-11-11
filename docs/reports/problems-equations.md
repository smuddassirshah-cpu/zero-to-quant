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

Level 2. Climbing wall: form, solve (21 climbers), then two l9 roundings that go down, each starting from the part before (31 climbers on £300; £7.28 in whole pence for 35 climbers; fix pass: the part 4 question now says whole pence and asks for pounds, and a `pence` slip of 728 has its line). Cottage: shares as fractions, cleared by 30, then a seventh friend to the nearest penny. Tariffs: a one-step solve (l5), the match by unknowns on both sides (l7), the judgement, then the saving past the match. Interest split: bond amount, equation (both parts ask for 12000 typed with no comma, because the expression field does not read a thousands comma), decimals cleared by 1000 (l8, equation restated in the question), then a second year's split.

Level 3. Bakery: form, flip, number line, then $4 < h \le 10$ counted. Fridge: Celsius as subject, 41 °F, the inequality that confirms it, then a freezer band, written with part 1's $C$ (fix pass), counted in Fahrenheit. Van: $t$ as subject, an age, a flipped strict inequality, a flipped double inequality whose ends swap, then a count. Fund weight: the subject appears twice ($a = \tfrac{wb}{1 - w}$), the two ends of a band, then whole £250 blocks counted.

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

## Set 4 (level 4, simultaneous equations; added after sets 1 to 3, whose sections above are unchanged)

File: `app/content/courses/equations/problems-4.json`. Numbers: the level 4 section of `docs/reports/problems-equations-numbers.py` (the script now checks sets 1 to 4: 1137 checks, 0 failures, exit 0). Engine graders: `docs/reports/problems-equations-4-grade.mjs --local-cdn <pkgs>` (138 checks, 0 failures).

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-rowing-current | 4 (4 / 0) | l14, l17 | 3 |
| problems-4 | p-seedling-trays | 4 (4 / 0) | l15, l17 (and l3) | 4 |
| problems-4 | p-remote-cars | 4 (4 / 0) | l15, l16, l17 | 4 |
| problems-4 | p-salt-solutions | 4 (4 / 0) | l14, l17 (and l8) | 5 |

Typed parts 16 of 16; no part is a judgement between options, so there is no choice part. Every lesson of the level appears (l14 twice, l15 twice, l16 once, l17 four times) and every problem draws on at least two. Only ideas taught by l17: the curve parts use the two shapes l15 teaches, $t^2 = 7t$ (gather and take out $t$) and $t^2 = 81$ (two roots).

Rowing: the second equation from words, elimination by adding (opposite signs), $c$ back from $b$, then a launch's time upstream with that current. Trays: "8 more" as $y = x + 8$, the swap with brackets, "twice as many small trays" as $2n$ (the l17 test with one tray), then the order counted against the words. Cars: line and curve by substitution (both times, the set widget), the second crossing read as a point on both graphs (l16), $t^2 = 81$ with $-9$ refused by the words (l17), then the gap. Salt: the salt equation from per cents, elimination after scaling by 0.15, $x$ back, then a 360 g batch through the 3 to 2 ratio every 25% batch keeps (the script derives $x = \tfrac32 y$ from $0.15x + 0.4y = 0.25(x + y)$).

### Checks

| check | problems-4 |
|---|---|
| numbers script | 0 failures, exit 0 (1137 checks for the four sets) |
| validator | 0 errors; 0 warnings on the file (one O2 long sentence in salt part 4 split) |
| playthrough `--local-cdn` | green (16 parts) |
| playthrough `--mobile` | green; 440 px shots of every part read, no fault (an `accept` with `\frac` showed as raw TeX in the Accepted line, so plain forms now come first) |
| voice scan 35 (course folder) | 0 and 0 |

### Review 1.3 faults avoided

- Bands: every answer is a whole number with `tol` 0, and each part names its unit or count ("in km/h", "in hours", "in metres", "in grams", "how many"); the script checks that and that each part's last printed figure in `feedback.correct` is the key. No `accept` line promises a form the field cannot take.
- No loose `wrong` bands: all are 0 except two non-whole slips (2.3333 and 2.625 hours, 5.7931 plants) at 0.005, each clear of the key and of each other.
- Slips from the part before carry their own entry: `carried` in rowing 3 ($b = 24$) and trays 3 (20 and 28), `carried` in cars 4 ($t = -9$), `carried` in salt 3 ($y = 312.5$). No slip gives the key: the script rebuilds every `wrong` from its named slip and finds each outside the band; the one coincidence is salt part 2, where swapped strengths give 300, the value of `other`, and that line covers both.
- No dead end: each part's result is restated and used by the next, and each last part asks for the result the problem is about (the time upstream, the small trays ordered, the gap at the post, the batch size).
- Expression answers use no function names; the key, every accept form, 66 typed strings and every `wrong` were put through `grade.js` with the local Compute Engine.

### Fresh-check

0 hits at the gate and 0 at `--min-run 8 --min-share 0`. Read by hand against the level's lessons, quizzes, `review-4`, `homework-4` and `topic-0.2`: the course uses cinema orders, a café, shares, brokers, data feeds, delta contracts, order books, bonds and options; here a river, seedling trays, two toy cars and salt solutions, none used in sets 1 to 3 either. Numbers chosen to miss the lines the course uses with $y = x^2$ ($2x$, $3x$, $5x$ in `review-4`, $6x$ against $2x^2$ in `homework-4`, $x^2 = 4$): here $7t$ and 81. Shapes that recur, judged acceptable: count and value (salt, as l17's contracts and `homework-4` `hw4-bonds`) with per cents and a ratio after it; "8 more" and "twice as many" (l17's own traps) on trays.

### Engine limits

One bullet to `docs/BACKLOG-INBOX.md` under "Raised later (problems equations)": a single numeric field refuses `b = 12`, where sets and expressions drop the letter. The trailing unit (`600 g`) is already in the inbox.
