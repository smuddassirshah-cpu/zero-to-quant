# Problem sets: validation (brief `docs/briefs/chained.md`, prompts `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/validation/problems-1.json`, `problems-2.json`. Numbers: `docs/reports/problems-validation-numbers.py` (resolves every path from `__file__`; exits 0).

## Level 1: `problems-1.json` (splits, folds and tuning)

Read first: l1 to l4, review-1 and homework-1 (prose, questions, numbers and code). Settings new to the course: household insurance claims with rare flood claims, used-van resale prices, small-business arrears, flat rents resplit by a consultant. The course's own story (200 to 400 loans, `make_loans`, the noise loans) is not used.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-flood-claims | 5 (5 / 0) | l1, l2 | 5 |
| problems-1 | p-van-prices | 5 (5 / 0) | l2, l3, l1 | 4 |
| problems-1 | p-arrears-grid | 5 (4 / 1) | l3, l4 | 4 |
| problems-1 | p-rent-seeds | 4 (4 / 0) | l1, l4 | 3 |

Typed parts 18 of 19; the one choice is a judgement (what to report and deploy after nested CV). Every lesson appears; every problem draws on at least two.

Chains. Flood claims: the test size 288 that gives an sd of 0.03, the 648 training claims left by a 3 to 1 split, 4-fold CV fitting on 864, the hypergeometric 0.0311 that a fold of 288 holds none of 12 flood claims, then inclusion and exclusion to 0.123 that some fold does. Vans: the CV mean 2.02, the fold sd 0.149 (`np.std`), the one-standard-error limit 2.169, the pick $\alpha = 10$, and the locked test MSE 2.25 read as a £1,500 typical miss. Arrears: 109 fits for a 6-fold search of 18 settings, 436 nested, 400 accounts per inner fit, the 8.6% flattery of 0.412 against 0.451, and what to report and deploy. Rents: one split's sd 0.0468, the typical best of 16 seeds 0.727, a 10.2% flattery, and 3,899 test flats (more than exist) to bring it under 4%. Each later part restates the value it uses; `carried` slips hold the value that follows from the commonest slip in the part before.

Form. Every non-whole numeric part names its form (decimal places or a percentage to 1 place), and each tolerance takes the value its feedback prints (`printed` checks in the script).

Reuse. `node tools/fresh-check.mjs --file content/courses/validation/problems-1.json`: 0 hits, 0 errors, 0 warnings (no function, pair, transform or region advisory). Second check by grep over the course folder for each key number, each letter ($\sigma$, $n$, $\alpha$, $K$, $G$) and each noun: the formulas $\sigma^2\sqrt{2/n}$ and $K(K_{\text{in}}G + 1)$ are the lessons' own (the same standard task with new numbers, allowed); 0.0311 occurs once as a chart value in l1's canvas data, not a stated number; no story is shared (flood claims, vans, arrears and letting agencies occur nowhere in the course, and arrears elsewhere in `app/content/` only in a conditional-probability lesson).

Checks. Validator 0 errors, no warnings on the file. `grade-all.mjs --file`: 19 widgets, 0 failures. Playthrough `--problems validation/problems-1 --why`: green, 37 typed slips routed; `--mobile`: green. Screens read at 440 px: no layout faults. Voice scan 35: 0 and 0. Number script: exits 0.

## Level 2: `problems-2.json` (time order, purging and breaks)

Read first: l5 to l8, review-2 and homework-2. Settings new to the course: a gas utility's demand above the seasonal norm, a share desk's 15-day forward label with 30-day features, a rates desk's direction signal over 1,600 days, a market maker's bond bid-ask spread over 24 days. The course's own data (`make_vol`, `make_signals`, `make_flip`, the 15-day and 1,000-day pictures) are not used.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-2 | p-gas-demand | 4 (4 / 0) | l5, l6 | 4 |
| problems-2 | p-forward-label | 5 (5 / 0) | l6, l7 | 5 |
| problems-2 | p-signal-break | 5 (4 / 1) | l8, l6 | 4 |
| problems-2 | p-spread-blocks | 4 (4 / 0) | l5, l7 | 3 |

Typed parts 17 of 18; the one choice is a judgement (what a full-history refit does after a break). Every lesson appears; every problem draws on at least two.

Chains. Gas: $\hat\rho(1) = 26/52 = 0.5$ on six cold-snap days, so time order; `TimeSeriesSplit(6)` on 1,400 days trains its last fold on 1,200; the joined MSE 5.30 of six 200-day blocks and 75 newer days; 2.50 times the shuffled 2.12. Forward label: 14 rows purged before a middle block, 29 rows of 30-day features after it, 1,063 rows left, then `TimeSeriesSplit(8, test_size=140, gap=14)` ending fold 1's training on day 125 and training fold 8 on 1,106 days with no embargo. Break: one fold's standard error 0.0354, fold 6 at $-1.4$ of them, the two-fold alarm at fold 6 (break near day 1,000), the misleading mean 0.535, and the refit that keeps the old sign. Spread: 5 sandwiched test days in a shuffled fold, 12 later training days for an unshuffled block, 10 training days after a 4-day label's purge and an embargo of 2, and the 20.0% rise from purging.

Reuse. `fresh-check.mjs --file content/courses/validation/problems-2.json`: 0 hits, 0 errors, 0 warnings. A first draft drew the advisory "2 shared parameters (0.57 0.58)" against l8's quiz; the fold hit rates were changed (0.565, 0.605, 0.575), and the rerun is clean. Grep: 1,260 days also appears in l12's code as five trading years (252 x 5), a calendar constant, not a shared setting; 125 and 29 occur in other contexts (a fit count, row counts); 3.85 occurs in l11's chart data only. No story is shared: gas demand appears elsewhere in `app/content/` only in a trigonometry cycle lesson, and the bid-ask spread only in backtesting and pairs lessons, none about validation.

Checks. Validator 0 errors, no warnings on the file. `grade-all.mjs --file`: 18 widgets, 0 failures. Playthrough `--why`: green, 38 typed slips routed; `--mobile`: green. Screens read at 440 px: no layout faults. Voice scan 35: 0 and 0. Number script: exits 0.
