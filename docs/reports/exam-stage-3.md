# Stage 3 exit test

File: `app/content/exams/stage-3.json`. Scripts: `docs/briefs/exam-stage-3-scripts/` (`build.py` route A, `check_numbers.py` route B, `fresh.py`).

## Design (written before the build)

Source: the `**Exit:**` lines of 3.1 and 3.5, the 3.3 exit test block, and the Stage 3 `exitTests` in `curriculum.json`. As in Stage 1, what the app can mark becomes paper items and what it cannot becomes a `check`.

| Source | Paper (auto) | Check (self-ticked) |
|---|---|---|
| 3.3 exit: 80% of Zhou's probability chapter cold | A: probability and expected value at interview pace, pass 0.8, 12 fresh authored items plus 6 drawn from `bank/probability` | Zhou's chapter at 80% |
| 3.3 exit: Zetamac 50 or more | B: the `arith` generator on Zetamac's default ranges, 80 items in 2 minutes, +1/−1/0, forward only, no skip, `passNet` 50 | Zetamac 50 |
| 3.3 exit: ten mock interviews, three with a stranger | none (spoken) | ten mocks; the 3.5 role extras (open case in 45 minutes, feed handler defence) go in its detail |
| 3.1 exit: a replication with an out-of-sample extension | C: research papers and their traps, 15 items at the 3, 8, 3, 1 ramp: survivorship and backfill, look-ahead in code and in plans, point-in-time accounts, multiple testing, costs, out-of-sample power, a point-in-time join in Python | replication on GitHub with a note |
| 3.5 exit: two medium coding problems in 60 minutes | D: two Python mediums drawn from `drills/oa` and the coding-int Python drills, 60 minutes, pass 1 (both) | none (the paper is the exit) |

Left out on purpose:

- 3.2 (stochastic calculus) and 3.4 (pure maths) are optional with hours not counted. A stage paper on them would gate the pass on optional work, so they stay in `topic-3.2` and `topic-3.4`.
- The research and systems rounds of 3.5 are role-specific. A gating check for them would block every other role, so the curriculum's two spoken extras sit in the detail of the mock-interview check.

Paper A minutes are the summed `pace` (interview pace, factor 1.0, drawn items at 180 s); Paper C's are 1.25 times the pace, as in Stage 1. Every authored setup is new against every Stage 3 file (`fresh.py`, `tools/fresh-check.mjs`), and every number is recomputed by `check_numbers.py`.

## Result

- Paper A, probability and expected value at interview pace: 50 min, pass 0.8. 12 authored items (8 numeric, 1 choice, 3 parts items) at difficulties 2, 6, 3, 1, plus 6 drawn from `bank/probability`. Setups: conditioning on an even product, a roll that repeats the one before, a series won by a lead of two, two desk heads at a round table, $P(XY < \tfrac12)$, a 2 by 2 quoting game with no saddle point, a six against a total of 9 or more, wins before a third loss, an all-pay auction, an edge over 100 bets, two independent regime flags, and a buyer who may be informed (three parts: chance of a buy, posterior, value of the sale).
- Paper B, mental arithmetic at Zetamac pace: 2 min, one `arith` entry of 80 items on the default ranges of `warmup.json` (which are Zetamac's), +1/−1/0, forward only, no skip, `passNet` 50 (the Stage 3 target in `warmup.json`).
- Paper C, research papers and their traps: 70 min, pass 0.7, 15 items at the 3, 8, 3, 1 ramp (4 choice, 4 numeric, 1 multi, 1 order, 4 parts items, 1 Python code item). Backfill and survivorship in fund databases, look-ahead in a pandas line and in a plan, Fama and French's June rule, a frozen out-of-sample run of the pairs method, break-even cost on turnover, a factor against Harvey, Liu and Zhu's bar of 3, equal against value weights, the note's sentence, alpha against a reversal factor, the best of 20 no-edge variants, the false share of passing factors at bars of 2 and 3, a point-in-time join `as_of` with restatements, and the power of an out-of-sample test.
- Paper D, two medium coding problems in an hour: 60 min, pass 1 (both), drawn from `drills/oa` (difficulty 3, pool 4) and the Python coding-int drills `pair-gaps`, `digit-sum-pairs`, `split-points` (difficulty 3, pool 3).
- Four checks: Zhou's probability chapter at 80% cold, Zetamac 50, ten mock interviews aloud with three strangers (role extras in the detail), the replication on GitHub with a note.
- 124 items in a full sitting (115 scored entries; parts counted once).

## Draws (bank tags used)

Six entries of `bank/probability`, difficulty 3 to 5, n 1 each, at most four tags each (the validator's limit). Families not drawn by Stage 1: `waiting-for-hh`, `who-wins`, `ruin-in-interviews` (pool 7); `when-to-stop`, `duels`, `betting-on-sequences` (5); `broken-stick`, `semicircle`, `random-chords`, `meeting` (5); `exceeding-one`, `expected-distance`, `largest-of-several`, `buffon` (5); `kelly`, `when-to-hedge`, `doubling-up` (4); `fair-from-biased`, `cards-and-colours` (3). Every pool holds at least twice n.

## Gates

- Validator: 0 errors, no warning on `stage-3.json` (3,990 warnings elsewhere, unchanged).
- Voice scan on a copy (`VOICE_BASE=<scratch>/voice3/`): 0 sentences over 20 words, 0 explanations over three sentences, 696 sentences. No exclamation marks or em-dashes.
- `check_numbers.py`: 238 of 238, exit 0. Route B: full enumeration of 36 rolls and of 9! seatings, a Markov chain solve for the lead of two, truncated series, grid searches for the game's maximin mix and the all-pay best response, Simpson integration, exact binomial sums in Fractions, Fractions over the hidden number and the trader's type, seeded simulations beside each normal tail, bisection, and a second, sorting implementation of `as_of`. The solution passes all 7 tests; the starter fails. Every number in every learner-visible string matches route B or a given. `check_wrongs()` passes; its "check by hand" lines are byKey texts that name the action, not the value.
- Playthrough with `--local-cdn`: green with and without `--mobile` (124 items, 115 of 115 scored, passed). Screenshots at 440 px checked: the order item, the code editor, an arithmetic item, the checks page and the result page lay out cleanly, with no sideways scroll.
- `readiness-sums.mjs`: OK (6 roles, 79 courses).

## Freshness

`tools/fresh-check.mjs --exam stage-3 --min-run 10`: 2 hits, both the instruction "Put the steps in order. Leave out the two that do not belong" (game-theory l9, topic-3.5). Boilerplate, kept. A first hit, "with $\varepsilon_t$ independent noise of", was reworded.

`fresh.py --stage3` and a dump of every Stage 3 question text were grepped before and after the build. Reused setups found and replaced:

- One die against two dice, first six wins: its key $\tfrac{36}{91}$ is the three-player first-six problem of puzzles l19, l30, homework 4 and mock-oa-trader-3 in disguise. Now a six against a total of 9 or more ($\tfrac{18}{43}$).
- Four aces before every king shared its setup with puzzles l4 ("Aces before the first king"). Now two desk heads at a round table.
- A spread's half-life from $\phi = 0.92$ was the inverse of pairs-rep l5 and review 1. Now equal against value weights in one decile.
- Dropped at design time after the grep: Bonferroni and Benjamini-Hochberg (research-int l4, review 1), first heart and first ace (puzzles l7), every-coupon waits, pot odds with 9 outs (game-theory homework 3), today's index members (momentum-rep l6), first-price bids (game-theory l8), Pig, distinct faces, adjacent red pairs.
- Remaining hits are common values in unrelated items (4.8, 2.75, 0.23, 1.41, 0.0465) and the name `as_of` in validation l11, a Stage 2 index-membership task, not a restated-accounts join.

## Notes for the main session

- Paper D's pool is small: four Python mediums in `oa` and three in coding-int. A learner who verified them in the drill library sees "previously seen" labels on a resit.
- Screenshots name items by index within a paper, so later papers overwrite earlier ones in `--shots`; Paper A was checked through the green playthrough, not by screenshot.
