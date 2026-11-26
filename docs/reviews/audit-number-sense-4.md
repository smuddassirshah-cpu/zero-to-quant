# Concept audit, round 1 (blind): number-sense level 4

Auditor: Fable reader, 26 Nov 2026, at commit `3222a0fe`. Scope: level 4, "Factors, measures and averages": `l15-building-blocks`, `l16-shared-factors`, `l17-around-and-inside`, `l18-circles-and-units`, `l19-one-number-for-many`, `review-4`, `homework-4`, `problems-4` (its header says `level: 4`) and `fluency-l15` to `fluency-l19`, all in `app/content/courses/number-sense/`. Stage 0, topic 0.1, so the reduced ledger depth applies: definitions, rules, "always / never / every" claims, conventions, and every graded key, wrong option and slip.

Blind rule kept: the ledger, the findings below and the concepts script were written and committed (WIP commit) before any `docs/reviews/review-number-sense*`, `docs/reviews/audit-number-sense*`, `docs/reports/number-sense-*` report or `docs/reports/concept-audit-*` file was opened. The level's number scripts were run, not opened.

## Result

- Ledger: `docs/reports/audit-number-sense-4-ledger.md`, 585 rows: 571 correct, 13 imprecise, 1 misleading, 0 wrong, 0 unverified.
- Findings: 8. 0 `wrong`, 7 `imprecise`, 1 `misleading`. 1 `serious`, 7 `minor`.
- No definition, rule, graded numeric key or slip value is wrong. The one `serious` finding is a choice question whose wording makes two "wrong" options true.

## Method

- Every screen, quiz, review, homework and problem item was read in full and every key, wrong option and slip value recomputed by hand. Each slip's feedback was matched to the mistake that gives its value.
- `docs/reports/number-sense-L4-concepts.py` then checks the claims without hand arithmetic. Level 4 makes no statistical claim, so nothing is Monte Carlo: each "always / never / every" claim is checked exhaustively over a range. The square-root test on every composite to 20,000; the factor-count rule and "squares have an odd count of factors" to 3,000; HCF × LCM = product and the two bounds on HCF and LCM for all pairs to 300; the sieve shading cell by cell.
- π convention. The lesson says 157 from π ≈ 3.14 "is fine" and calls 22/7 "handy". The script works every π item (12 fixed items, 2 generated families) with π, 3.14 and 22/7, rounds as the item asks, and confirms the answer is accepted and matches no slip. All pass. The engine's `within` allows 1e-9 beyond the tolerance, which the two 0.01 tolerances (`l18` `screens[4]`, `quiz[0]`) rely on for a 3.14 answer.
- Generated families (18). Pick tables are checked over every row: `fluency-l15` 196 + 160 + 160 rows (exponents, prime text, count text, largest prime, no pure power of 2); `fluency-l16` all 29 × 43 pairs (coprime multipliers, so the stated HCF and LCM are right; the "other number" is unique by brute force); `fluency-l19` orderings are permutations. Integer-range families are sampled at 300 draws each with `fluency-sample.mjs`: the key and every slip are recomputed from the drawn variables alone, and no slip falls within tolerance of the key.
- Definitions and conventions were checked against Hardy and Wright (*An Introduction to the Theory of Numbers*), Euclid and Archimedes for the area rules, and Freedman, Pisani and Purves (*Statistics*, ch. 4) for mean, median and mode. "Factor" includes 1 and the number itself throughout, shown in `l15` `screens[1]` before it is graded. The mode convention (two modes on a tie; no mode when every value appears once) is the UK school one and is stated in the item that grades it.

## Findings

1. `l15-building-blocks.json` | `screens[4].question`, with `widget.options[1]` (`all`) and `options[2]` (`half`) | imprecise, serious | The question asks "Which divisions are enough to show that 97 is prime?" Dividing by every number from 2 to 96, or by every number to 48, is enough: both include 2, 3, 5 and 7. The option's own `why` says "That works". Two options marked wrong are true answers to the question as asked, so a learner who reasons correctly is graded wrong. | Evidence: if no number from 2 to 96 divides 97, then 97 has no factor pair, which is the definition of prime in `screens[3]`. The key is the only right answer to "fewest", not to "enough". | Fix, `screens[4].question`: `Which is the shortest set of divisions that shows 97 is prime?` Basis: a set of trial divisors is sufficient when it holds every prime up to √97; the smallest such set is 2, 3, 5, 7. No option text needs to change; the two `why` lines already say the longer sets work and are wasteful.

2. `l15-building-blocks.json` | `screens[9].hints[2].text` and `screens[9].explain.text` | imprecise, minor | "21, 63, 7 and 12 use only primes 252 has; 5, 8 and 24 do not" and "5, 8 and 24 each need a prime that is not there". 8 = 2³ and 24 = 2³ × 3 use only the primes 2 and 3, which 252 has. They fail on how many 2s, as the `byKey` lines for `d8` and `d24` rightly say. Read plainly, the hint teaches "same primes, so it divides", which is false (8 does not divide 252). | Basis: d divides n exactly when each prime's index in d is at most its index in n (Hardy and Wright, section 1.3 with Theorem 2). | Fix, `hints[2].text`: `21, 63, 7 and 12 fit inside $2^2 \times 3^2 \times 7$. 5 needs a 5; 8 and 24 need a third 2.` Fix, last sentence of `explain.text`: `5 needs a prime 252 lacks, and 8 and 24 need three 2s where 252 has two.`

3. `l15-building-blocks.json` | `screens[9].feedback.correct` and `screens[9].explain.text` | misleading, minor | "7 give 36 weeks". The item counts trading days. 21 and 63 trading days are the practitioner month and quarter, so the learner will take "7 trading days = a week" as the same kind of convention. A trading week is 5 days; 252 trading days are about 50 weeks. | Basis: the 252-day convention is 12 months of 21 trading days, 5 a week (Hull, *Options, Futures and Other Derivatives*, ch. 15, trading days). | Fix, `feedback.correct`: `21, 63, 7 and 12 divide 252: 12 months, 4 quarters, 36 blocks of 7 days or 21 blocks of 12.` Fix, second sentence of `explain.text`: `So 21 days give 12 months, 63 give 4 quarters, 7 give 36 blocks and 12 give 21 blocks.`

4. `l16-shared-factors.json` | `screens[6].prose`, `screens[6].explain.text`, `summary.ideas[2]` | imprecise, minor | "The LCM is the smallest piece size that works". The LCM, 36, is the smallest number of pieces. As a size, a 36th is the largest piece both fractions cut into: 72nds are smaller and also work. A learner who thinks in amounts, which this course asks for, is told the opposite of what is true. | Evidence: 5/12 = 30/72 and 7/18 = 28/72, and 1/72 < 1/36 (script INFO line). | Fix, `screens[6].prose`: `In level 1 you added fractions by cutting both into a common piece size. The LCM of the bottoms gives the largest piece that works, so the fewest pieces. Here $12 = 2 \times 2 \times 3$ and $18 = 2 \times 3 \times 3$.` Fix, first sentence of `explain.text`: `The LCM, 36, gives the largest piece both fractions cut into: 36ths.` Fix, `summary.ideas[2]`: `The HCF cancels a fraction in one step; the LCM of the bottoms gives the largest common piece for adding.`

5. `l19-one-number-for-many.json` | `screens[4].explain.text`; `problems-4.json` | `items[2].parts[2].explain.text` | imprecise, minor | "One extreme day … moves the mean a lot and the median not at all", stated as a general rule. It is exact for what the screen does, which is to make an existing largest day larger. It is not true of an outlier in general: adding one moves the median (2, 3, 4 has median 3; 2, 3, 4, 100 has median 3.5). | Evidence: script, stretching the largest of five values never moves the median; adding an outlier moved it in all 462 lists tried. Basis: the median is resistant, not immune (Freedman, Pisani and Purves, ch. 4 section 3). | Fix, last sentence of `l19` `screens[4].explain.text`: `However large one extreme day, an **outlier**, grows, it drags the mean with it and leaves the median where it was.` Fix, first sentence of `problems-4` `items[2].parts[2].explain.text`: `The puncture day moves the mean a lot and leaves the median at 27.`

6. `fluency-l18-circles-and-units.json` | `families[speed-units].wrong[1].line` (`minutes`) | imprecise, minor | "An hour is 3,600 seconds, not 60. You changed hours into minutes only." The slip value is right in both directions. The second sentence fits km an hour into metres a second. For metres a second into km an hour (about a quarter of draws) the value is x × 60 ÷ 1,000: the learner changed seconds into minutes and stopped, and no hours were changed. | Evidence: script INFO, 74 of 300 draws are that direction. | Fix, `line`: `An hour is 3,600 seconds, not 60. You used 60, so your answer is a speed per minute.` Basis: both slip values, x × 1,000 ÷ 60 and x × 60 ÷ 1,000, are per-minute speeds.

7. `fluency-l15-building-blocks.json` | `families[count-factors].wrong[0].line` (`pairs`) | imprecise, minor | "${pairs}$ is the number of factor pairs, the rectangles. Each pair holds two factors." For the 11 square numbers in the table (36, 100, 144, …) one pair is a number times itself and holds one factor. Following the line for 36 gives 5 × 2 = 10, the very slip `l15` `screens[1]` corrects. | Basis: d(n) is odd exactly when n is a square (script, to 3,000). | Fix, `line`: `${pairs}$ is the number of factor pairs, the rectangles. Count the factors in them: two in each pair, or one where a number pairs with itself.`

8. `l17-around-and-inside.json` | `screens[4].prose` | imprecise, minor | "A **trapezium** has two parallel sides." As a definition it leaves out that the shape has four sides and that the parallel sides are one pair. A parallelogram, or a hexagon, also "has two parallel sides". | Basis: UK usage, a quadrilateral with one pair of parallel sides (the inclusive reading, "at least one pair", also needs "four-sided" and "pair"). | Fix, first sentence of `prose`: `A **trapezium** is a four-sided shape with one pair of parallel sides.`

Notes that are not findings:

- `l19` `quiz[0]`: "There is no mode" is marked wrong for 2, 3, 3, 5, 7, 7, 9. That is wrong under every convention in use; the explain states the tie convention.
- `l18` `screens[9]`: 7.5 trading hours a day is a premise of the item, not a market fact, and is used consistently.
- `fluency-l15` `count-from-primes`: for 144 and 324 the two slips (indices multiplied, choices added) both give 8, and the line shown names the second. The value is a real slip either way.
- `l16` `screens[7]`: Euclid's method is justified in one direction only ("any number dividing both also divides what is left"). That is enough at Stage 0.

## Gates

- Validator: `node tools/validate.mjs`, 0 errors (4,606 warnings, none new: no content was edited).
- Number scripts: `node tools/run-number-scripts.mjs --only number-sense` with the venv Python first on PATH: 7 of 436 scripts, 7 passed, 0 new failures, exit 0.
- Concepts script: `docs/reports/number-sense-L4-concepts.py`, exit 0, 0 failures, 3 INFO lines (findings 4, 5 and 6).
- No playthrough, as instructed. No content, engine or state file was edited.

## Overlap table

Earlier reads of level 4, opened only after the WIP commit `9abdae76`: `docs/reviews/review-number-sense-4.md` (lessons, review, homework; 20 findings, all fixed), `docs/reviews/review-holes-0.1-0.2.md` (problems-4 and the five fluency sets; findings 6 to 10, 15, 20, 21) and `docs/reviews/review-delta-holes.md` (problems-4; findings 1, 7, 8). Conceptual findings are those about meaning or grading: a false statement, a slip whose feedback names another mistake, a key or tolerance that marks a taught method wrong, a true line used as a distractor, a rule without its condition. Freshness, coverage, untaught-term, unit-parsing and layout findings are not counted.

| Conceptual findings | Count | Which |
|---|---|---|
| This audit only | 8 | findings 1 to 8 above |
| Earlier reviews only | 15 | `review-number-sense-4` 1, 2, 3, 4, 5, 7, 8, 9, 11, 19, 20; `review-holes-0.1-0.2` 15, 21; `review-delta-holes` 1, 7 |
| Both | 0 | |

All 15 earlier findings were fixed before this read, so none could be found again. Each fixed line was read here and carries a `correct` row in the ledger: for example `l18` `screens[7]` `two-r`, `l19` `quiz[3]` `first-last` = 40, the `after` rules of `l16` `screens[9]`, the false distractor of `homework-4` `h-euclid`, the widened π tolerances. The earlier fix passes introduced no `wrong`.

What the earlier reads missed, by class:

- Finding 1 is the class of earlier findings 4 and 5 (a valid answer marked wrong), on an item neither read flagged.
- Finding 5's sentence was written by the first review's fix (its finding 10 proposed the exact text), so one of the eight is fix-pass text.
- Findings 6 and 7 are generated-family slip lines that are right for most draws and off for a sub-range (one direction; square numbers). The holes read sampled 20 draws a family and judged values, not each line against each sub-range.
- Findings 2, 3, 4 and 8 are author sentences that number checks cannot see.

Single-read miss rate on this level: the earlier reads found 15 conceptual faults and left 8 (0 `wrong`, 1 `serious`).

## Inbox

Two bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (audit number-sense):". One asks for a validator warning on a non-keyed `choice` option whose `why` concedes it is true (finding 1). The other is a second vote for the π tolerance probe already requested.

## Fix pass

Opus fixer, 26 Nov 2026, content commit `ce4b738f`. Each fix was derived here, not copied from the finding.

1. `l15` `screens[4]` | fixed | Question now `Which is the shortest list of divisions that shows 97 is prime?`. Basis: any divisor set holding every prime up to √97 ≈ 9.8 proves primality, so 2 to 96 and 2 to 48 are sufficient; among the options only {2, 3, 5, 7} is both sufficient and shortest ({2, 5} is shorter but misses 3 and 7). Every option's `why` and `byKey` line still reads correctly ("works, but wasted"; "far too far"; "still need 3 and 7").
2. `l15` `screens[9]` hint 3 and explain | fixed | Hint: `fit inside 2^2 × 3^2 × 7. 5 needs a 5, and 8 and 24 need a third 2.` Explain ends `8 and 24 need three 2s where 252 has two.` Basis: d | n iff each prime's index in d is at most its index in n; 8 = 2³, 24 = 2³ × 3, 252 = 2² × 3² × 7, and 252 ÷ 8 = 31.5.
3. `l15` `screens[9]` feedback and explain | fixed differently | "36 weeks" became "36 periods of 7 days" (feedback) and "36 periods" (explain); "21 blocks" became "21 periods of 12". Basis: the days are trading days and a trading week is Monday to Friday, 5 days; 252 ÷ 5 = 50.4 weeks, not 36. Months (252 ÷ 12 = 21) and quarters (252 ÷ 4 = 63) are the usual conventions and stay.
4. `l16` `screens[6]` prose, explain, `summary.ideas[2]` | fixed | "smallest piece size" became "largest piece size" (prose adds "so the fewest pieces to count"; explain `gives 36ths, the largest piece size`). Basis: 1/m is a common piece of 5/12 and 7/18 iff 12 and 18 both divide m, iff 36 divides m; the largest such piece is 1/36, and 1/72 also works and is smaller.
5. `l19` `screens[4]` explain; `problems-4` `items[2].parts[2]` explain | fixed differently | `l19`: `Stretching the top day into an **outlier**, far from the rest, drags the mean but not the median.` `problems-4`: `The puncture pulls the mean up to 32, but the median stays 27 however slow that ride was.` Basis: raising the largest value keeps the sort order, so the middle value is unchanged while the total and mean rise; a changed value that crosses the middle, or an added value, moves it (2, 3, 4 has median 3; 2, 3, 4, 100 has 3.5). For the rides 24, 26, 27, 31, 52 the median is 27 for any fifth time of 27 or more.
6. `fluency-l18` `speed-units` slip `minutes` | fixed differently | Line now `An hour is 3,600 seconds, not 60. Using 60 gives a speed per minute instead.` Basis: x km an hour is 1,000x m in 60 minutes, x × 1,000 ÷ 60 m a minute; x m a second is 60x m in a minute, x × 60 ÷ 1,000 km a minute. Both slip values are per-minute speeds. Checked on 600 draws (438 km an hour, 162 metres a second; x 5 to 150): the slip value equals that per-minute speed in every draw.
7. `fluency-l15` `count-factors` slip `pairs` | fixed differently | Line now `... Each pair holds two factors, or just one when a number is paired with itself.` Basis: a factor pair a × b with a = b holds one factor, so d(n) = 2 × pairs for non-squares and 2 × pairs − 1 for squares. Checked on 1,500 draws covering all 160 table rows, the 11 squares (36 to 676) included: brute-force factor pairs equal the slip value and rebuild the key in every draw.
8. `l17` `screens[4]` prose | fixed | `A **trapezium** is a four-sided shape with one pair of parallel sides.` Basis: UK school definition, a quadrilateral with one pair of parallel sides; the old sentence also fits a parallelogram or a hexagon.

No key, slip value, tolerance or hidden test changed. Gates on the seven edited files: validator 0 errors (4,606 warnings, as before); voice scan 35, 0 and 0; `number-sense-L4-concepts.py` exit 0 (its three INFO lines still describe the old text); `run-number-scripts.mjs --only number-sense` 7 of 7 passed; `grade-all.mjs --file` 0 failures on each; playthrough desktop and `--mobile` all passed (`--lesson` l15, l16, l17, l19; `--problems` problems-4; `--fluency` fluency-l15, fluency-l18).
