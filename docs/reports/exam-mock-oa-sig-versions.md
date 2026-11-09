# mock-oa-sig versions 2 and 3: fresh templates (session Y)

Brief: `docs/briefs/mock-versions.md` (PLAN 2d; critical review 3.1). Version 1 (`mock-oa-sig.json`) is unchanged. Files re-authored: `app/content/exams/mock-oa-sig-2.json`, `mock-oa-sig-3.json`. Number script: `docs/reports/exam-mock-oa-sig-versions-numbers.py`.

## Result

- Items replaced: 17 of 17 in version 2 and 17 of 17 in version 3 (34 new problems, 34 new item ids). No item survives, so no surviving id changes.
- Kept per file: `id`, `versionOf`, `name`, `style`, `models`, `description`, `requires`, `skills`, the paper (`minutes` 60, scoring 1/0/0, `passNet` 11), 17 items, and per position the difficulty (4 at 2, 5 at 3, 6 at 4, 2 at 5), `pace` (90/180/240/360 s, 57 minutes), skill and widget kind. Topic weights per version are therefore those of version 1: `pz-expectation` 5, `pz-conditioning` 6, `pz-recursion` 2, `pz-games` 3, `bz-search` 1.
- Widget kinds: `docs/briefs/mocks.md` gives a widget per position ("some take a choice, others a number"), so each position keeps version 1's kind (10 choice, 7 numeric). Choices keep four options and `shuffle: true`; numerics ask for three decimal places with `tol.abs` 0.005 and named `wrong` values.
- Tags: each new item's tag names its own new family, so `tags` no longer repeat version 1's families.

## Checks

| Check | Result |
| --- | --- |
| `exam-mock-oa-sig-versions-numbers.py` (venv Python) | exit 0: 34 keys, each exact (Fractions) and by a second method (enumeration, Fraction linear solve, DP or seeded simulation with stated tolerance); every `wrong` and distractor is its named slip, outside the key's tolerance, options pairwise more than 0.01 apart |
| `node tools/validate.mjs` | 0 errors (warnings on these files: advisory `O2-long-sentence` only) |
| Voice scan, 35-word gate, on both files | 0 over 35 words, 0 explanations over three sentences; no `!`, no em-dash, British spelling, £ |
| Playthrough `--exam mock-oa-sig-2 --local-cdn` | green, desktop and `--mobile` |
| Playthrough `--exam mock-oa-sig-3 --local-cdn` | green, desktop and `--mobile` (440 px shots of all 17 items read: no clipping) |
| `node tools/fresh-check.mjs --exam` (default gate) | 0 hits for each version |
| Closure (`tools/closure.mjs --target mock-oa-sig`) | every item uses ideas from its 19 courses: counting, conditional, random-vars, markov, series, integrals, quadratics, puzzles, brainteasers |

## Template table, before

Before this pass versions 2 and 3 held version 1's template at every position, with changed numbers. Version 1's parameters, then versions 2 and 3:

| Pos | Topic | Setup (v1) | Method | Old v2 | Old v3 |
| --- | --- | --- | --- | --- | --- |
| 1 | expectation | die pays face squared | mean of squares | 4-sided | 8-sided |
| 2 | linearity | hearts in 5 cards | k times the share | aces in 13 | aces in 5 |
| 3 | EV with fee | £3 fee, paid even face | average payout less fee | face if 4 or more | £4 fee |
| 4 | indicators | HH pairs in 10 tosses | adjacent-pair indicators | 21 tosses | 13 tosses |
| 5 | at least one | a six in 4 rolls | complement | 3 rolls | 5 rolls |
| 6 | conditioning | both aces given one | shrink the sample space | picture cards | hearts |
| 7 | binomial | 3 heads in 6 | binomial coefficient | 2 in 7 | 4 in 8 |
| 8 | search | heavy coin among 10 | ceiling of log base 3 | 28 coins | 80 coins |
| 9 | Bayes | 1% base rate test | Bayes, two hypotheses | 90%, 10% | 2% base |
| 10 | waiting | tosses until HH | first-step on prefixes | HTH | HHH |
| 11 | stopping | one reroll of a die | backward induction | two rerolls | 8 faces |
| 12 | order statistics | E[max] of two dice | distribution of the max | min | 8 faces |
| 13 | multi Bayes | coin bag, 3 heads | posterior odds | 4 heads | 4 fair coins |
| 14 | multi Bayes | test taken twice | odds times LR squared | 90%, 10% | 2% base |
| 15 | ruin | fair, £3 to £10 duration | i(N - i) | £2 to £8 | £4 to £9 |
| 16 | ruin | p = 0.6, £2 to £5 | ruin formula | 0.55, £3 to £6 | 2/3 |
| 17 | Bayes and ruin | fair or 3/4 coin, reached £3 | ruin then Bayes | 2/3 | 0.6 |

## Template table, after

Version 1 is the "Setup (v1)" column above. New items (setup in about six words; method in about six words):

| Pos | Diff | Version 2 setup | v2 method | Version 3 setup | v3 method |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | two cards, paid on same colour | fix first card, count matches | two dice, doubles pay double | total plus conditional extra |
| 2 | 2 | record days in random order | indicator chance 1/k, harmonic sum | coin score back at level | indicators at even tosses, binomial |
| 3 | 2 | £1 roll, six pays and rerolls | geometric first-step payout | £10 stake at 4 to 1 | odds to profits, weight outcomes |
| 4 | 2 | calling ranks while dealing | 52 indicators of 1/13 | pairs of orders out of order | pair indicators of 1/2 |
| 5 | 3 | three dice strictly rising | one order per face set | dice coefficients, real root | count discriminant cases |
| 6 | 3 | exactly two aces, first card | placings given the count | first card beats second | relative orders, conditional |
| 7 | 3 | same head count, two people | Vandermonde, sum of squares | third head on fifth toss | negative binomial |
| 8 | 3 | higher-lower guessing to 1,000 | 2^k - 1 settled numbers | heaviest and lightest of 10 | pair first, 3n/2 - 2 |
| 9 | 3 | randomised-response survey | solve share, then Bayes | pooled test of five | divide by pool chance |
| 10 | 4 | running total multiple of 7 | remainders, one face in six | rolls until a drop | first-step m_j, (6/5)^6 |
| 11 | 4 | paid draws, uniform amounts | fixed point, threshold value | ideas spawning, dies out | extinction equation, smaller root |
| 12 | 4 | six before any five | competing faces, wait unchanged | nearest side of a square | tail integral of (1 - 2t)^2 |
| 13 | 4 | ball moved between urns | Bayes on hidden first stage | two failed drawer searches | sequential search update |
| 14 | 4 | order relayed through two desks | compound noise, then Bayes | trader with desk-mates | size bias, then condition |
| 15 | 4 | unfinished match, split pot | play out four games | best-of-five length, p = 0.6 | distribution of series length |
| 16 | 5 | win £2 or lose £1 | three-state first-step solve | craps with a point | race of point against 7 |
| 17 | 5 | knockout with a favourite | split on the random draw | rock, paper, scissors for four | first-step over players left |

No two of the 51 items share a template: within each row the three setups differ, and no new setup in one column repeats a setup or method elsewhere in its own version or in the other. Pairs read closely and judged distinct: v2 q03 (count of sixes before a non-six) against v2 q12 (a conditioned wait); v2 q15 (who wins from 2 to 1) against v3 q15 (how long a series runs); v3 q10 (first drop) against v3 q11 (extinction), both first-step but on different chains.

## Freshness against the app

Setups were checked before writing with a phrase search over `app/content` (`find.py` in the scratchpad), and these first choices were dropped because the app already holds them: product of two dice (puzzles l1), matching cards or hats (random-vars l8, brainteasers), empty boxes and aces before the first king (puzzles l4), secretary and Pig (puzzles l6), first ace and second-card symmetry (puzzles l7), broken stick (puzzles l13), sums exceeding one (puzzles l15), larger die given (puzzles l27), duels (puzzles l28), the doubling cycle (puzzles l23), hedging a series (puzzles l22), Monty Hall (conditional l18), tennis (markov homework 2), birthday pairs (random-vars homework 2), one die or several on a coin (mm-games homework 3), a uniform call (integrals l13, topic-1.3) and three tosses alike (mock-oa-trader-3).

`fresh-check.mjs` at the default gate: 0 hits for each version. At the triage gate (`--min-run 8 --min-share 0`) it first gave seven hits; three were real and were rewritten:

- v2 q10 cube walk matched `exams/topic-3.3.json` item 14, the same bug on a cube. Replaced by the multiple-of-7 total.
- v3 q11 landing on a total matched `exams/stage-3.json` paper 0 item 6 (slices filling 1 or 2 lots, chance the total is exactly 5). Replaced by the extinction item.
- v3 q13 unknown mix matched `courses/puzzles/l24-mixed-set.json` screen 7, whose options name Laplace's rule, the same 3/4. Replaced by the failed drawer searches.

The three hits that remain are stock phrasing, not shared setups:

- v2 q06 against `mental-pressure/l15` screen 0: "cards are dealt from a well-shuffled 52-card deck"; that screen asks for two aces, this item for an ace's place given the count.
- v2 q12 against `limits-thm/l2` quiz 0 ("chance the first six comes on roll 3") and `markov/l19` screen 7 (Wald's identity on the same roll): "you roll a fair die until the first six"; neither conditions on the absence of a five.

Two near-overlaps judged acceptable: v2 q02 records shares the word "record" with `plotting/l7` and `contests/l1`, which count record days in a given series, not their expected number in a random order; v2 q08 is binary search, which `topic-1.8` (outside this mock's closure) uses on sorted ticks, not as a guessing game with a three-way answer.

## Keys (all recomputed by the script)

Version 2: 25, 137/60, -1/5, 4, 5/54, 2/5, 5/16, 10, 1/3, 7, 80, 3, 9/13, 5/12, 44, 5/23, 51/250.
Version 3: 49/6, 19/16, -5/3, 15/2, 19/36, 2/3, 3/16, 13, 10000/40951, (6/5)^6, 1/2, 1/6, 3/53, 4/7, 2541/625, 244/495, 45/14.

## Notes for the reader

- v3 q08 relies on the known bound of 3n/2 - 2 comparisons for both extremes; the script confirms 13 by an exact adversary DP over parcel states (untried, won only, lost only), and the explanation gives the counting argument.
- v3 q11's explanation states why the smaller root applies (mean offspring 5/4) and shows the iteration rising to 1/2.
- `prep.json`, `readiness.json`, engine files and version 1 are untouched.
