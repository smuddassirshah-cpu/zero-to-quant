# Problem sets: validation (brief `docs/briefs/chained.md`, prompts `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/validation/problems-1.json`, `problems-2.json`, `problems-3.json`. Numbers: `docs/reports/problems-validation-numbers.py` (resolves every path from `__file__`; 649 checks, exits 0; also green under `node tools/run-number-scripts.mjs --only docs/reports/problems-validation-numbers.py`).

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

## Level 3: `problems-3.json` (leaks, survivors and selection)

Read first: l9 to l12, review-3 and homework-3. Settings new to the course: a fund's daily net inflows, a fund analyst's target-encoded excess return, a fund-of-funds rule backtested on a database of open funds, and a currency carry rule's 60 lookbacks. The course's own data (the ten days of share volume, the 60-firm panel, the trend rule's 40 lookbacks, the earnings table) are not used.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-3 | p-fund-flows | 5 (4 / 1) | l10, l9 | 3 |
| problems-3 | p-fund-encoding | 4 (3 / 1) | l9, l10, l12 | 4 |
| problems-3 | p-closed-funds | 4 (4 / 0) | l11, l12 | 4 |
| problems-3 | p-carry-lookbacks | 5 (4 / 1) | l12, l11 | 5 |

Typed parts 15 of 18; the three choices are judgements (which step may run before the split, what a leak that clears Bonferroni means, how to read a correlated search). Every lesson appears; every problem draws on at least two.

Chains. Flows: the full-sample mean 21 a leaky scaler subtracts, the training mean 18, a 1.5 move from revising one test day, the 2 test days inside a centred 5-day window read on the last training day, and the log as the only step safe outside the folds. Encoding: $\rho = 1/\sqrt{49} = 0.1429$, the noise hit rate $1 - \arccos(\rho)/\pi = 0.5456$, $t = 3.16$ on 1,200 fund-months, and a leak that clears the Bonferroni bar of 3.02. Closed funds: the survivorship gap $0.26 \times 6.5 = 1.69$ points, an honest Sharpe of 0.476 against 0.617, the noise best of the log's 18 variants (0.607, not the wiki's 4), and a haircut to $-0.13$. Carry: the ceiling 1.43 from $N = 60$ (not the wiki's 9), the independent haircut to 0.32, the correlated mean best 0.52 (about 0.96 left), the Bonferroni Sharpe bar 1.57, and the reading that a correlated search is few real tries and needs one locked test.

Claims checked beside the numbers: $\rho$ between an average of 49 and one of its terms is $1/7$ (simulated); $1 - \arccos(\rho)/\pi$ equals the sign-agreement chance (simulated, and equal to homework-3's $\tfrac12 + \arcsin(\rho)/\pi$); the mean best of 4, 18, 22 and 60 normals (1.03, 1.82, 1.91, 2.319) by integration and Monte Carlo; the correlated best equals $\sqrt{1 - \rho}$ times the independent one (Monte Carlo); Bonferroni bars 3.02 and 3.14 from the normal quantile.

Reuse. `fresh-check.mjs --file content/courses/validation/problems-3.json`: 0 hits, 0 errors, 0 warnings. A first draft drew a same-course error (13 shared words with review-3's "by the survivorship gap formula, how far does the database overstate the average" stem) and an advisory (the formula $\tfrac12 + \arcsin(\rho)/\pi$ shared with homework-3). The stem was rewritten, the formula is now stated as the equal $1 - \arccos(\rho)/\pi$, and the rerun is clean; the slips of that part changed with it. The reported carry Sharpe was moved from 1.45 to 1.48, since 1.45 is l12's mean best of 100. Grep: 252 and 49 occur as trading days and month counts in other contexts; 1.03, 1.82, 1.91 and 1.69 occur only as chart or canvas values in l11 and l12; 1.57 is l12's rule of thumb for 40 over 3 years, here the Bonferroni Sharpe bar for 60 over 4, a coincidence of one value with a different meaning. The sets were rerun together after level 3: fresh-check 0 hits on problems-1, -2 and -3.

Checks. Validator 0 errors, no warnings on the file. `grade-all.mjs --file`: 18 widgets, 0 failures. Playthrough `--why`: green, 34 typed slips routed; `--mobile`: green (both rerun after the 1.48 change). Screens read at 440 px: no layout faults. Voice scan 35: 0 and 0. Number script: exits 0.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under `Raised later (problems validation):` (the over-100 warning on a `wrong` entry of a `%` widget; the shared-formula advisory compares text, not value).
