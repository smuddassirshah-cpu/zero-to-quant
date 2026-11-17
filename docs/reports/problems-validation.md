# Problem sets: validation (brief `docs/briefs/chained.md`, prompts `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/validation/problems-1.json`, `problems-2.json`, `problems-3.json`. Numbers: `docs/reports/problems-validation-numbers.py` (resolves every path from `__file__`; 737 checks after the session AF re-author, exits 0; also green under `node tools/run-number-scripts.mjs --only docs/reports/problems-validation-numbers.py`).

## Level 1: `problems-1.json` (splits, folds and tuning)

Read first: l1 to l4, review-1 and homework-1 (prose, questions, numbers and code). Settings new to the course: household insurance claims with rare flood claims, used-van resale prices, small-business arrears, flat rents resplit by a consultant. The course's own story (200 to 400 loans, `make_loans`, the noise loans) is not used.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-flood-claims | 5 (5 / 0) | l1, l2 | 5 |
| problems-1 | p-van-prices | 5 (5 / 0) | l2, l3, l1 | 4 |
| problems-1 | p-arrears-grid | 5 (5 / 0) | l3, l4, l2 | 4 |
| problems-1 | p-rent-seeds | 4 (4 / 0) | l1, l4 | 3 |

Typed parts 19 of 19 since the session AF re-author (the one choice, what to report and deploy after nested CV, is gone). Every lesson appears; every problem draws on at least two.

Chains. Flood claims: the test size 288 that gives an sd of 0.03, the 648 training claims left by a 3 to 1 split, 4-fold CV fitting on 864, the hypergeometric 0.0311 that a fold of 288 holds none of 12 flood claims, then inclusion and exclusion to 0.123 that some fold does. Vans: the CV mean 2.02, the fold sd 0.149 (`np.std`), the one-standard-error limit 2.169, the pick $\alpha = 10$, and the locked test MSE 2.25 read as a £1,500 typical miss. Arrears: 109 fits for a 6-fold search of 18 settings, 436 nested, 400 accounts per inner fit, then (session AF) the 0.0208 by which a learning curve $0.33 + 40/n$ says the nested score overstates the model refitted on all 640, and the 1,090 fits of the cheapest run (10 outer folds) that brings it to 0.007. Rents: one split's sd 0.0468, the typical best of 16 seeds 0.727, a 10.2% flattery, and 3,899 test flats (more than exist) to bring it under 4%. Each later part restates the value it uses; `carried` slips hold the value that follows from the commonest slip in the part before.

Form. Every non-whole numeric part names its form (decimal places or a percentage to 1 place), and each tolerance takes the value its feedback prints (`printed` checks in the script).

Reuse. `node tools/fresh-check.mjs --file content/courses/validation/problems-1.json`: 0 hits, 0 errors, 0 warnings (no function, pair, transform or region advisory). Second check by grep over the course folder for each key number, each letter ($\sigma$, $n$, $\alpha$, $K$, $G$) and each noun: the formulas $\sigma^2\sqrt{2/n}$ and $K(K_{\text{in}}G + 1)$ are the lessons' own (the same standard task with new numbers, allowed); 0.0311 occurs once as a chart value in l1's canvas data, not a stated number; no story is shared (flood claims, vans, arrears and letting agencies occur nowhere in the course, and arrears elsewhere in `app/content/` only in a conditional-probability lesson).

Checks. Validator 0 errors, no warnings on the file. `grade-all.mjs --file`: 19 widgets, 0 failures. Playthrough `--problems validation/problems-1 --why`: green, 37 typed slips routed; `--mobile`: green. Screens read at 440 px: no layout faults. Voice scan 35: 0 and 0. Number script: exits 0.

## Level 2: `problems-2.json` (time order, purging and breaks)

Read first: l5 to l8, review-2 and homework-2. Settings new to the course: a gas utility's demand above the seasonal norm, a share desk's 15-day forward label with 30-day features, a power desk's walk-forward price MSEs over 1,120 days (re-authored in the fix pass), a market maker's bond bid-ask spread over 24 days. The course's own data (`make_vol`, `make_signals`, `make_flip`, the 15-day and 1,000-day pictures) are not used.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-2 | p-gas-demand | 4 (4 / 0) | l5, l6 | 4 |
| problems-2 | p-forward-label | 5 (5 / 0) | l6, l7 | 5 |
| problems-2 | p-signal-break | 5 (5 / 0) | l8, l6 | 4 |
| problems-2 | p-spread-blocks | 4 (4 / 0) | l5, l7 | 3 |

Typed parts 18 of 18 (the last part of the break problem became a typed 2-sd level after delta read AE-3). Every lesson appears; every problem draws on at least two.

Chains. Gas: $\hat\rho(1) = 26/52 = 0.5$ on six cold-snap days, so time order; `TimeSeriesSplit(6)` on 1,400 days trains its last fold on 1,200; the joined MSE 5.30 of six 200-day blocks and 75 newer days; 2.50 times the shuffled 2.12. Forward label: 14 rows purged before a middle block, 29 rows of 30-day features after it, 1,063 rows left, then `TimeSeriesSplit(8, test_size=140, gap=14)` ending fold 1's training on day 125 and training fold 8 on 1,106 days with no embargo. Break (re-authored): one 140-day fold's MSE sd 0.1195, fold 5's 1.31 at 2.6 of them above 1.00, the first fold over 1.239 trained on 700 days, the three newest folds joined at 5.5 sds, and the 2-sd level 1.138 of that joined MSE. Spread: 5 sandwiched test days in a shuffled fold, 12 later training days for an unshuffled block, 10 training days after a 4-day label's purge and an embargo of 2, and the 20.0% rise from purging.

Reuse. `fresh-check.mjs --file content/courses/validation/problems-2.json`: 0 hits, 0 errors, 0 warnings. A first draft drew the advisory "2 shared parameters (0.57 0.58)" against l8's quiz; the fold hit rates were changed (0.565, 0.605, 0.575), and the rerun is clean. Correction after the second read: the claim below that no story is shared was false for the first break problem, which replayed l8's first four screens on a renumbered series (the checker does not read `feedback`, `explain` or `why`). It was re-authored in the fix pass on fold MSEs, with no hit rate, base rate or day 1,000. fresh-check after the fix: 0 hits; the advisory for the formula $\sigma^2\sqrt{2/n}$ shared with level 1's flood claims is the same taught level-1 rule applied to a new quantity. Grep: 1,260 days also appears in l12's code as five trading years (252 x 5), a calendar constant, not a shared setting; 125 and 29 occur in other contexts (a fit count, row counts); 3.85 occurs in l11's chart data only. No story is shared: gas demand appears elsewhere in `app/content/` only in a trigonometry cycle lesson, and the bid-ask spread only in backtesting and pairs lessons, none about validation.

Checks. Validator 0 errors, no warnings on the file. `grade-all.mjs --file`: 18 widgets, 0 failures. Playthrough `--why`: green, 38 typed slips routed; `--mobile`: green. Screens read at 440 px: no layout faults. Voice scan 35: 0 and 0. Number script: exits 0.

## Level 3: `problems-3.json` (leaks, survivors and selection)

Read first: l9 to l12, review-3 and homework-3. Settings after the fix pass: a fund's 16 daily inflows scaled with the spread, not the mean; a fund analyst's target encoding that counts a month's own label twice; a high-yield bond screen backtested on a file of issues still trading, then haircut for 12 screens; 24 position-sizing variants in 4 families of identical Sharpe ratios. The second read found that the first versions of the flows, closed-funds and carry problems replayed l10, l11 and l12 screens with new numbers (the earlier statement in this report that every setting was new was false); all four were re-authored, and the encoding problem was given a different task so that it no longer applies the taught sign-agreement formula to the taught inputs.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-3 | p-fund-flows | 5 (4 / 1) | l10, l6 | 3 |
| problems-3 | p-fund-encoding | 4 (3 / 1) | l9, l10, l12 | 4 |
| problems-3 | p-closed-funds | 5 (4 / 1) | l11, l12 | 4 |
| problems-3 | p-carry-lookbacks | 5 (4 / 1) | l12 | 5 |

Typed parts 15 of 19; the four choices are judgements (the fix for a scaler fitted on all rows, what a leak that clears Bonferroni means, what to report after both corrections, how to count identical variants). Every lesson appears; every problem draws on at least two.

Chains. Flows (card disputes counted weekly, after delta read AE-3): the sd 3.579 a scaler fitted on all 16 weeks divides by, the training sd 1.780, week 13 at 3.37 training sds up (the leaky scaler shows 1.19), 3 of the 4 test weeks flagged beyond 3 sds (the leaky scaler flags none), and the fix. Encoding: $\rho = 2/\sqrt{15} = 0.5164$ for a label counted twice among 13, $R^2 = 4/15 = 0.2667$, $t = 5.97$ on 100 fund-months, and a leak that clears the Bonferroni bar of 3.02. Closed funds: two vendor files (164 survivors at 9.2%, all 200 issues at 6.68%) give the 14.0 points the 36 defaulted issues fell short by, an honest Sharpe of 0.653 against 0.933 (flattered by 2.52 points), the noise best of the log's 12 screens (0.616, not the note's 5), and a haircut to 0.04. Carry: the sd 0.4082 of a 6-year noise Sharpe, the best of 4 independent families at 0.420, a haircut leaving 0.53, the t of the 0.95 (2.33) against the Bonferroni bar of 2.24 for 4 tries, and the reading that identical variants are one try.

Claims checked beside the numbers: $\rho = 2/\sqrt{15}$ between a weighted average and its own label (simulated, and as a covariance over the sds); $t$ of a fit with exactly that correlation on 100 rows (from scipy's p-value); the mean best of 4, 5, 12 and 24 normals (1.03, 1.16, 1.63, 1.95) by integration and Monte Carlo; the best of 24 variants in 4 families of identical Sharpe ratios equals the best of 4 (Monte Carlo); Bonferroni bars 2.24, 3.02 and the t bars of 2.87 for 24 tries and 1.64 for one from the normal quantile. After delta read AE-3 the problem set claims l12 only for `p-carry-lookbacks` (the earlier row also named l11, which it never used): the brief's two lessons a problem is an exception here, and the set still covers l9 to l12.

Reuse. `fresh-check.mjs --file content/courses/validation/problems-3.json`: 0 hits, 0 errors, 0 warnings. Fix pass: fresh-check 0 hits on problems-1, -2 and -3 (advisories: the level-1 formula $\sigma^2\sqrt{2/n}$ in problems-2, and two coincidental parameters, 0.04 and 0.21, against an l2 screen). The earlier version restated the taught sign-agreement formula as an arccos to clear the checker; that was reuse in another form and is gone. Because the checker does not read `feedback`, `explain` or `why`, the re-authored problems were also compared with l8 and l10 to l12 by hand for sentences and for the order of steps. Grep of `app/content/` for each key number and noun: no shared story (a power desk's logistic spike model and a day-ahead regression exist elsewhere, on other tasks; high-yield bonds, position-sizing variants and a weighted target encoding occur nowhere else).

Checks. Validator 0 errors, no warnings on the file. `grade-all.mjs --file`: 19 widgets, 0 failures. Playthrough: green with and without `--mobile` (rerun after the fix pass). Screens read at 440 px: no layout faults. Voice scan 35: 0 and 0. Number script: exits 0.

## Re-author, session AF (`p-arrears-grid` parts 4 and 5)

Ruled `re-author` in `docs/reviews/review-reuse-af-hits.md`: old parts 4 and 5 walked `l4-nested` `screens[11]` (flattery of the best CV MSE as a share of the nested score, then what the card reports). New part 4: on the curve $0.33 + 40/n$ the nested score (models refitted on 480 accounts) overstates the 640-account model by $40/480 - 40/640 = 1/48 \approx 0.0208$. New part 5: the overstatement is $0.0625/(K-1)$, so 10 outer folds are the fewest at or under 0.007, and they cost $10 \times 109 = 1090$ fits. Item id kept. Part 2's `no-refits` line, which was `l4` `quiz[3]`'s sentence, is reworded ("432 counts only the inner fits. Each outer fold then refits its own winner, so add 4.").

Closest material and why it is not a walk: `l2` `screens[5]` (leave-one-out: more folds, bigger training sets, less bias, more fits) is a choice over a table and puts no number on the bias; the new parts price it on a stated curve and solve for the fold count. `l4` `screens[3]`, `screens[10]` and `quiz[3]`, `review-1` `items[6]`, `homework-1` `items[8]` count the fits of a given nested run; part 5 first finds $K$ from a bias bound, then counts. `l4` `screens[6]`, `screens[8]`, `screens[11]` and `homework-1` `items[7]` (report and deploy, the selection gap) are no longer touched: no part compares a best score with a nested one. Topic exam `topic-2.1`: no item on training-size bias or on choosing $K$. Other sets: no learning curve and no fold-count search. Numbers 0.33, 40/n, 0.0208, 0.007, 1,090, 981, 576 shared with nothing in the course (grep; 0.007 occurs only as a code constant in `l11`).

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under `Raised later (problems validation):` (the over-100 warning on a `wrong` entry of a `%` widget; the shared-formula advisory compares text, not value).

## Exceptions recorded (delta AE-4)

`problems-3` `p-closed-funds` part 2 takes 2.52 from the prose and does not use part 1's 14.0 (it feeds only the `whole-gap` slip); accepted, as the flows' contrast step was in AE-3, because the alternative brings `l11` `screens[8]`'s product back into the part.

## Re-author: `problems-2` `p-spread-blocks` (review-pkg3-reuse-hits fault 2)

The 24-day bid-ask version walked l5 screens[1] and [7], `h-count` (with `r-purge`, l7 screens[1] and [2], `p-forward-label`, `a-purged-fold`) and l7 screens[5]. Re-authored with the same id, skills (`vl-time`, `vl-leakage`, `vl-cv`), difficulty 3 and four chained parts. New setting: a credit desk's CDS index spread over 1,800 rows, label the 8-day move (a sum of 8 near-independent daily changes), so two labels correlate by the share of days they have in common.

| Part | Old deciding step | New deciding step | Key | Band | Slips |
|---|---|---|---|---|---|
| 1 | sandwiched test days of a listed shuffled fold | shared label days of rows 3 apart over 8 | 0.625 | ±0.0005 | 0.375 offset, 0.75 one-more |
| 2 | training days after a test block | expected training rows within 7 a side under shuffled 5-fold, $14 \times \tfrac45$ | 11.2 | ±0.05 | 12.8 horizon, 5.6 one-side, 14 all-in |
| 3 | rows left after purge and embargo | smallest `gap` $g$ with correlation $(8 - (g + 1))/8$ below 0.4 | 4 | exact | 5 gap-as-distance, 7 full-purge |
| 4 | percentage rise of the error under purging | most rows of a 200-row test block with no two labels sharing a day, $200 \div 8$ | 25 | exact | 26 fencepost, 29 seven-apart |

Each later part restates part 1's rule. Numbers: `problems-validation-numbers.py` recomputes each key twice (label-day sets against coefficient-vector correlations; $14 \times 0.8$ against real shuffled `KFold` on 1,800 rows, 11.206 for the exact partition, inside the band; the gap rule against `TimeSeriesSplit` distances; $\lceil 200/8 \rceil$ against a brute-force packing), runs `check_slips` and `lv.slip` on every slip, and checks the explain claims (no day shared at 8 apart, effective sample 25.3). No key or slip sits on a rounding tie; 0.4 is not reached by any distance. The reader script `problems-validation-numbers-read.py` and `delta-ae-3-numbers.py` keyed on the old text: their old blocks now run only on the old prose, and the reader script rebuilds the new item by its own route.

Checks: validator 0 errors, no warning on the item; voice scan 35: 0 and 0; `fresh-check --file` and `--all-exams`: no hit on the item (an early prose drew a stock-phrase text hit against l7 screens[0], reworded); `grade-all --file` 18 widgets, 0 failures; playthrough `--problems validation/problems-2` green with and without `--mobile`, 440 px shots read.
