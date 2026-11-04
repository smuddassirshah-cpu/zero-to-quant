# Prerequisite mapping: `requires` on the mock exams

Content pass under `docs/briefs/prereq-gating.md` sections 5 and 8. Edited field: top-level `requires` on the 11 real mocks in `app/content/exams/mock-*.json` (inserted after `description`; parsed JSON differs from before only in `requires`, checked by script). Topic exams, stage tests and the `"sample": true` mocks are untouched, so test-out stays open.

## Method

- Each level's skills came from the `skills` of its lessons, review and homework in `course.json`; each mock item's `skills` and `tags` were matched to them, and the drawn pools (`draw`) were read through the bank and drill files they can reach.
- The prerequisite lists at the end of each mock's section in `docs/briefs/mocks.md` named the lessons the author meant; each lesson was mapped to its level. Interview mocks gate only on interview courses and the foundations those lists name.
- Direct only: a level already in the closure of another listed level is dropped (a script pruned each list against the effective `requires` graph, with the implicit previous-level default).
- Closure size is the number of levels a fresh profile must clear first, listed levels included, counted from the same graph.
- Version files (`-2`, `-3`) carry the same list as their first version; their items test the same skills.

## Per mock

**mock-oa-arith** (closure 8): `mental-pressure/L3`
- Speed items (`mp-speed`) come from L1 and L3 (`l9-eighty-in-eight`, `l12-mock-test`); fraction and percentage items (`mp-fractions`) from L2 (`l5`, `l6`). L3 carries L1 and L2 by the chain.
- Not listed: L4 (`l13-negative-marking`). It teaches a scoring strategy, not an item skill, and its own references (conditional, limits-thm, counting-chance) would hold an arithmetic test behind probability breadth (closure would be 38).

**mock-oa-sig, -2, -3** (closure 46): `puzzles/L2`, `brainteasers/L1`
- `pz-expectation` and `pz-recursion` items (dice, waiting time, stopping) are L1; `pz-conditioning` (Bayes, cards, largest of several) and the gambler's ruin items (`l10-ruin-in-interviews`) are L2.
- `bz-search` (the weighing item) is `brainteasers/L1` (`l4-weighing-coins`).
- Not listed: `puzzles/L4` (`l24-mixed-set`, a summative set that adds Kelly and hedging, which no item tests) and `mental-pressure/L4` (`l15-probability-at-speed`, cited in the brief but the mock has no `mp-` items).

**mock-oa-trader, -2, -3** (closure 72): `mental-pressure/L4`, `puzzles/L5`
- Sequences (`mp-formats`: `l10` in L3, `l16-harder-sequences` in L4), probability at speed (`mp-fractions`, `l15`), ranking and intervals (`mp-estimate`, `l14`, `l7`, `l8`) all sit in `mental-pressure/L4`, which carries L1 to L3.
- Item `b13-given-the-total` is `puzzles/l27-given-the-total`, in `puzzles/L5`. The brief names it ("once it is written"; it is written). One item of 40 holds the mock behind `puzzles/L5` (closure 72 against 38 without it); flag for the second reader if that is judged too heavy. The other conditioning items need only `puzzles/L2`, already in the closure.

**mock-superday-trader** (closure 107): `puzzles/L5`, `game-theory/L3`, `mm-games/L3`, `brainteasers/L3`, `mental-pressure/L2`, `recruiting/L3`
- `puzzles/L5`: `l25-fair-from-biased` (a4); its chain gives `l2`, `l5` (coupons, hats) and `l20`, `l21`, `l24` (betting, Kelly, card stopping).
- `game-theory/L3`: `l11-pot-odds` (a6, `gm-poker`).
- `mm-games/L3`: paper 3 (`mg-fair`, `mg-update`, `mg-risk`, `mg-quote`) uses `l10-position-limits`, `l12-thinking-aloud`, `l13-full-game`; L1 and L2 follow.
- `brainteasers/L3`: `l13-digits-and-remainders`, `l14-sums-in-one-line` (b6, b7, `bz-quick`).
- `mental-pressure/L2`: paper 2 speed, fractions and Fermi items (`l1`, `l2`, `l7`; `l5`, `l6`).
- `recruiting/L3`: `rk-behave` (c4, d1, d2) from `l8`, `l11`, `l12`, `l13`.

**mock-superday-research** (closure 116, the largest): `research-int/L4`, `coding-int/L4`, `recruiting/L3`
- `research-int/L4`: `rq-stats`, `rq-linalg`, `rq-ml`, `rq-case`, `rq-data` span L1 to L4; the brief lists l1 to l20.
- `coding-int/L4`: paper 3 and the brief's `l17-two-in-sixty`, `l18-talking-while-coding`.
- `recruiting/L3`: behavioural checks (`l11-stories-that-answer`, `l13-the-final-round`).
- The paper 1 draw (`bank/probability`, difficulty 3 to 5, 30 matching items) has no level common to the whole pool (some items name no lesson), so it adds nothing.

**mock-oa-quant-data** (closure 89): `research-int/L4`
- Statistics, linear algebra and data items (`rq-stats` L1, `rq-data` L4: `l16` to `l19`).
- The brief's foundations (`numpy-pandas` `l7`, `l12`; `regression` `l12`; `validation` `l6`) are `numpy-pandas/L3`, `regression/L3`, `validation/L2`. All three already sit in the closure of `research-int/L4`, so they are not listed.

**mock-oa-code** (closure 38): `coding-int/L2`
- The pack `oa` drills (every drill the draw can reach) test `ci-patterns` (L1), `ci-strings` (L2) and `ci-timed` (L2: `l8-simulating-the-rules`). L3 and L4 are not tested; l15 and l17 link to the mock, not the other way round.

## Summary

| Mock | `requires` | Closure |
| --- | --- | --- |
| mock-oa-arith | mental-pressure/L3 | 8 |
| mock-oa-code | coding-int/L2 | 38 |
| mock-oa-sig (+ -2, -3) | puzzles/L2, brainteasers/L1 | 46 |
| mock-oa-trader (+ -2, -3) | mental-pressure/L4, puzzles/L5 | 72 |
| mock-oa-quant-data | research-int/L4 | 89 |
| mock-superday-trader | puzzles/L5, game-theory/L3, mm-games/L3, brainteasers/L3, mental-pressure/L2, recruiting/L3 | 107 |
| mock-superday-research | research-int/L4, coding-int/L4, recruiting/L3 | 116 |

Largest direct list: 6. Skipped samples: `mock-sample*`, `mock-interleave-sample`, `mock-trade-sample`.

## Checks (from `app/`)

- Validator: 0 errors (539 warnings, none new from this pass); no cycles.
- `playthrough --exams --local-cdn`: all passed.
- `playthrough --routes-only --local-cdn`: all passed, including "exam requires".
