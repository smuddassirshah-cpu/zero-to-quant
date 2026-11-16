# Problem sets: validation (brief `docs/briefs/chained.md`, prompts `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/validation/problems-1.json`. Numbers: `docs/reports/problems-validation-numbers.py` (resolves every path from `__file__`; exits 0).

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
