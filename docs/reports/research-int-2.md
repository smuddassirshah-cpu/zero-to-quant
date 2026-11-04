# research-int level 2 report: Machine learning questions

Author: content agent, 4 November 2026. Brief: `docs/briefs/research-int.md` `## Level 2` plus its shared sections. Files in `app/content/courses/research-int/` and `app/content/data/`. `course.json` is unchanged. Level 1 files were not touched (written in parallel elsewhere).

## Files

| File | Screens | Quiz / items | Interactive canvas and widgets | Notes |
| --- | --- | --- | --- | --- |
| `l6-bias-variance-aloud.json` | 10 | 4 | `plane` with a dragged point on the error curve (`drag-point`, target on the curve at $c = 0.5$) and a `derive` caption; `scatter` with a `frames` control through the degree 1, 3, 9 fits; grouped `bars` of bias² and variance; `table` widget; two `order` widgets with distractors | hook, ladder, explore, problem, trap, edge (sixteen years), generalise ("Say it aloud", spoken answer as an `order`), derive ($c^*$), transfer (a fund's alpha), "The follow-up" |
| `l7-ridge-against-lasso.json` | 9 | 4 | grouped `bars` (least squares, ridge, lasso) driven by a $\lambda$ control through `derive` (`b / (1 + lam)` and `sign(b) * max(abs(b) - lam, 0)`); `table` canvas of the sparse fits; `table` widgets | hook, ladder, problem (sparse truth), trap (correlated group), edge (units), generalise (spoken answers as `choice`), derive (ridge factor), transfer (200 signals), "The follow-up" (duplicate columns, penalty table) |
| `l8-tree-questions.json` | 11 | 4 | grouped `bars` of a split; `plane` of $\rho\sigma^2 + (1-\rho)\sigma^2/B$ with a $\rho$ control and a derived floor line; `scatter` with step `curves` for boosting; `table` canvases | Gini table, entropy, bagging, floor, out of bag, boosting by hand, trap (parallel boosting), importance (`multi`, holds the edge case), derive (bagged variance), transfer (signal screen), "The follow-up" |
| `l9-pca-questions.json` | 10 | 4 | `bars` of eigenvalues; `matrix`; `scatter` with PC lines (`state.lines`); grouped `bars` of loadings; histogram `bars` of 1,000 noise eigenvalues with a `cut` at the edge | share, two shares, units, trap (90% rule), edge (sign), noise edge, generalise, derive (2 by 2 by trace and determinant), transfer (yield curve), "The follow-up" |
| `l10-weak-signals.json` | 11 | 4 | `plane` of $t$ against $n$ with a dragged point (`snapX: 10`); `scatter` `sim` ($\rho = 0.05$); `bars` `sim` of the best of 50 noise correlations; `series` of the leaky window; `bars` of costs; `series` of the futures file; Python `code` with `data` | hook, table, derive ($n$ needed), Sharpe, trap, best of 50, leakage, edge (costs), generalise, transfer (E14 code on `futures-daily.csv`), "The follow-up" |
| `review-2.json` | | 10 items, difficulty 2 to 4 | `timed: { seconds: 600, lockAtZero: true }`; every item has `skills`, `tags`, `pace: 60` | brief items R2.1 to R2.10, reordered to interleave (see below) |
| `homework-2.json` | | 8 items, difficulty 3 to 5, four at 5 | E11 `parts` on H2.4 and H2.6, a `longform` (10-point rubric, model answer), two `code` items (one with `data`), an `order` derivation, a `table` | every item has `skills`, `tags`, `pace` |
| `app/content/data/*.csv` | | six files | written by `gen_data.py` in Pyodide 0.27.7 | `futures-daily.csv`, `spread-daily.csv`, `houses.csv`, `ticks-gaps.csv`, `towns-temp.csv`, `orders-messy.csv` |

Every lesson: `minutes: 15`, the objective from `course.json`, one `trap` with a `byKey` line naming the blurt, an edge case, a "Say it aloud" or spoken-answer screen (three-sentence answer in prose, then `order` or `choice` over spoken answers), a `derive` screen with a distractor line, a quant `transfer`, and a closing `ladder` titled "The follow-up". The first prose of each lesson states the pace ("About two minutes a question; say your reasoning aloud first"). Skills: `rq-ml` on l6, l7, l8, l10; `rq-ml` and `rq-linalg` on l9 (and on R2.7, H2.5, H2.6).

Review order (brief id → file id): R2.1 `r2-shrink`, R2.2 `r2-degree`, R2.3 `r2-soft`, R2.7 `r2-pca-cov`, R2.4 `r2-ridge`, R2.5 `r2-gini`, R2.6 `r2-bag`, R2.8 `r2-days`, R2.9 `r2-leak`, R2.10 `r2-split`. Homework order: H2.4 `h2-lasso-parts` first (see the playthrough note), then H2.1 `h2-soft-derive`, H2.2 `h2-boost-code`, H2.3 `h2-bv-longform`, H2.5 `h2-pca-table`, H2.6 `h2-pca-parts`, H2.7 `h2-oob`, H2.8 `h2-lag-code`.

### Tags and pace

Families used: `bias-variance`, `shrinkage-mse` (l6); `ridge-lasso`, `soft-threshold` (l7); `gini-split`, `bagging-variance`, `boosting-rounds`, `feature-importance`, `oob` (l8); `pca-share`, `pca-scaling`, `pca-signal-small-component` (l9); `weak-signal`, `sample-size-for-signal`, `leakage-window` (l10). Every task screen, quiz item, review item and homework item carries `tags` and `pace`.

| File | Paced screens (sum) | Paced items (sum) |
| --- | --- | --- |
| l6 | 10 at 120 s (1,200 s) | 4 quiz at 120 s (480 s) |
| l7 | 9 at 150 s (1,350 s) | 4 quiz at 150 s (600 s) |
| l8 | 11 at 120 s (1,320 s) | 4 quiz at 120 s (480 s) |
| l9 | 10 at 120 s (1,200 s) | 4 quiz at 120 s (480 s) |
| l10 | 10 at 150 s and the code screen at 600 s (2,100 s) | 4 quiz at 150 s (600 s) |
| review-2 | | 10 at 60 s (600 s, the timed limit) |
| homework-2 | | 3,720 s: order 240, code 900, longform 600, parts 360, table 240, parts 360, numeric 120, code 900 |

### E3 example draws (for the exam author; no level file holds a `draw`)

- `{ "from": "bank/research-2", "tags": ["ridge-lasso"], "difficulty": [3, 4], "n": 3 }`
- `{ "from": "bank/research-2", "tags": ["bias-variance", "pca-share"], "difficulty": [2, 4], "n": 3 }`

## Data files (E14)

Written once by `docs/briefs/research-int-scripts/gen_data.py`, run in Pyodide 0.27.7 under Node (numpy 2.0.2, pandas 2.2.3; the system Python here has numpy 2.5.3 and pandas 3.0.5, so it was not used), then copied to `app/content/data/`. All six SHA-256 prefixes match the brief.

| File | Bytes | Rows | SHA-256 | Brief prefix |
| --- | --- | --- | --- | --- |
| `futures-daily.csv` | 26,564 | 1,000 | `67fa91b5630be8736ac6c3d0f3ca2886fc3582c5cc928fb7b6296bd39659c5b0` | `67fa91b5630be873` ok |
| `spread-daily.csv` | 10,161 | 600 | `79a4c859319c36d6d7a0865c7b9182cb7fd05fef5149eb78ce9ac28845eea485` | `79a4c859319c36d6` ok |
| `houses.csv` | 10,472 | 400 | `78010e051693cd824349a5d62d5a30ebe356b89fd5d0dda3fd9f5b220f1b6037` | `78010e051693cd82` ok |
| `ticks-gaps.csv` | 4,073 | 312 | `eef04db6d214e5635671221a4a12e549d96a757b09d49939c34ca96b824d9174` | `eef04db6d214e563` ok |
| `towns-temp.csv` | 16,615 | 1,202 | `3d2d6516ac7ce840371052417aadf594068ae71725ac7329ef4d6409d1802377` | `3d2d6516ac7ce840` ok |
| `orders-messy.csv` | 19,904 | 600 | `f556c81a3943f2bdec58697076701e11b51c1b4f1cdb1f8ebb50aa8bd1104fdd` | `f556c81a3943f2bd` ok |

Total 87,789 bytes; the largest is 26,564, well under the 256 KB cap. The files sit flat in `app/content/data/` as the brief and the orchestrator name them (`content/data/futures-daily.csv`); AUTHORING section 3 suggests a course folder (`content/data/<course>/`), which would change every level's paths, so I kept the brief's paths. The brief also says to copy `gen_data.py` to `app/tools/gen-research-data.py` when the files are committed; that is outside my course folder, so I left it for the orchestrator.

## Validator

`node tools/validate.mjs`: **0 errors** (397 warnings in all; level 1's unwritten files only warn). Warnings in this level's files: 2, both "a ladder screen usually reuses the previous canvas kind" on "The follow-up" (l6 after a `plane` transfer, l10 after a code transfer); the brief requires the closing screen to be a ladder.

Voice: `VOICE_BASE=<abs>/app/content/courses/research-int python3 docs/reviews/voice-scan.py`: **0 sentences over 20 words, 0 explanations over three sentences** (also 0 at a limit of 19). No `!`, no em-dash, no emoji; the one "center" is the pandas keyword inside a hidden test.

## Playthrough

`node tools/playthrough.mjs --lesson research-int/<each of l6 to l10> --set research-int/review-2 --set research-int/homework-2 --local-cdn <scratchpad>/pkgs`: all passed, then again with `--mobile`.

| Lesson or set | Desktop | 390 px |
| --- | --- | --- |
| l6-bias-variance-aloud | 14 checks, quiz 4/4 | 14 checks, quiz 4/4 |
| l7-ridge-against-lasso | 13 checks, quiz 4/4 | 13 checks, quiz 4/4 |
| l8-tree-questions | 15 checks, quiz 4/4 | 15 checks, quiz 4/4 |
| l9-pca-questions | 14 checks, quiz 4/4 | 14 checks, quiz 4/4 |
| l10-weak-signals | 15 checks, quiz 4/4 (code screen in the app's Pyodide) | 15 checks, quiz 4/4 |
| review-2 | 10 of 10; timed 600 s, clock at zero ends it | same |
| homework-2 | 8 of 8, 41 of 41 marks; parts checks pass | same |

Screenshots (desktop and 390 px) were looked at. Fixed from them: the boosting screen first drew round 1, which gave the answer away (now the start line only, rounds in the explanation); the `matrix` labels printed `\Sigma` raw (now `$\Sigma$`); the $t$-curve label sat on the 1.96 line (moved); ridge cells at $\lambda = 0.5$ demanded 0.6667 while the bars show 0.67 (tolerance 0.005); the yield-curve caption now names each correlation's pair; a blank ridge row in the sparse table now holds the seeded ridge fit.

### Code: starters and solutions in Pyodide

The brief's code was checked natively. I ran every starter and solution of this level in Pyodide 0.27.7 (numpy 2.0.2, pandas 2.2.3, scikit-learn 1.6.1, SciPy 1.14.1, statsmodels 0.14.4) under Node, with the data file copied into the working directory as the widget does, each test's `setup`, `call`, `expect` and tolerance applied (`codecheck.py` in my scratchpad folder):

| Widget | Solution (tests and examples) | Starter |
| --- | --- | --- |
| l10 transfer `lag1_corr(path)` | 4 of 4 | 0 of 3 |
| homework H2.2 `boost(...)` | 7 of 7 | 0 of 6 |
| homework H2.8 `lag_corr(k)`, `lag_t(k)` | 7 of 7 | 1 of 6 (only the no-rolling-window source check) |

The playthrough also ran each solution in the app's own worker. No difference from the native figures: every value the brief states for H2.2 and H2.8 came out the same in Pyodide.

### The brief's scripts in Pyodide

`l2_ml.py`, `late_check.py` and `items_check.py` were run in Pyodide 0.27.7 (not natively): all print "ALL AGREE", and every printed number matches the brief, including the seeded ones (bias-variance table, single-sample errors, duplicate columns 0.9974 and 1.9455, lasso counts 6, 3, 3, importances 0.467, 0.469, 0.032, 0.032 and 0.373, 0.387, 0.003, −0.003, noise eigenvalue 2.8704, Sharpe simulation 0.7817, best-of-50 simulation 0.1585). statsmodels in Pyodide is 0.14.4, not the 0.15.0 the brief names; the statsmodels checks (H2.8 $t$ by OLS) still agree to 1e-9.

## Numbers, with sources

Every number was computed twice: by the brief's scripts (method A a hand formula, method B a library or seeded simulation) or by my own `aux2.py` and `aux3.py` (same `two()` helper, both "ALL AGREE" in Pyodide). Brief numbers: `l2_ml.py` (L), `late_check.py` (LC), `items_check.py` (IC). Mine: `aux2.py` (A2), `aux3.py` (A3).

**l6.** $(c-1)^2 + c^2$ least at 0.5, error 0.5, 1 at $c = 1$ and $c = 0$ (L; A2). Single sample, seed 11: training 0.2542, 0.0499, 0.0378; against the truth 0.2049, 0.0115, 0.0205 (L, polyfit and sklearn; A2 also checks the pasted polynomial coefficients against sklearn at seven points). 400 refits: bias² 0.2037, 0.0055, 0.0001; variance 0.0087, 0.0159, 0.0410; test with noise 0.3023, 0.1113, 0.1310 (L; the table accepts ±0.0006 so the sums of rounded parts, 0.3024, 0.1114, 0.1311, pass). Sixteen years, $c = 0.5$: 0.25 + 0.0625 = 0.3125; best $c$ 0.8, error 0.2 (A2, formula and grid search). Fund alpha 4%, vol 8%, four years: standard error 4%, error 16 raw and 8 at half weight (A2). Ten times the data (200 points, 400 refits, seeds 203 and 209): degree 9 bias² 0.0000, variance 0.0043; degree 3 bias² 0.0044, variance 0.0017, total 0.0061 (A3, decomposition against the direct mean squared error). Quiz: true mean 2, $c = 0.5$: 1.25, best $c$ 0.8 (A2 plus a 2,000,000-draw simulation); 0.02 + 0.03 + 0.05 = 0.10; limit 0.25.

**l7.** $\lambda = 1$: lasso (2, 0, 0), ridge (1.5, 0.5, −0.25); $\lambda = 0.5$: lasso (2.5, 0.5, 0), ridge (2, 0.6667, −0.3333) (L, soft threshold and `Lasso`/`Ridge` on an orthonormal design). Duplicates: ridge 0.9974 each, lasso 1.9455 and 0; L2 penalties 2 and 4, L1 2 and 2 (L). Sparse truth, seed 8: lasso kept 6, 3, 3 at $\alpha$ = 0.1, 0.3, 1.0 with first three (2.943, −1.907, 1.721), (2.831, −1.706, 1.519), (2.445, −1.040, 0.855); ridge $\alpha = 10$ keeps 10 with (2.716, −1.739, 1.582) (L, own coordinate descent against sklearn; A3, ridge closed form against sklearn). Shrink amounts 0.555, 0.960, 0.645 (by subtraction). Quiz: $b = (1.5, -0.4, 0.9)$, $\lambda = 0.5$: lasso (1.0, 0, 0.4), sum 1.4; ridge −0.2667 (A2, against sklearn on an orthonormal design).

**l8.** Gini 0.5, children 0.32, gain 0.18; entropy child 0.7219 bits, gain 0.2781 (L, fractions and `DecisionTreeClassifier`). Bagging $\sigma^2 = 4$, $\rho = 0.3$: 1.48 at $B = 10$, 1.228 at 100, floor 1.2 (L; A2 by $\mathbf{1}^\top\Sigma\mathbf{1}/B^2$). Out of bag $(1 - 1/n)^n$: 0.3487, 0.3660, 0.3677 for 10, 100, 1,000; $1/e = 0.3679$ (L; A2 by `log1p`). Boosting: 3, 3, 5, 5 then 2.4, 2.4, 5.6, 5.6; learning rate 1 gives 1.5 and 6.5 (L and IC, against `GradientBoostingRegressor`). Importance 0.467, 0.469, 0.032, 0.032 and 0.373, 0.387, 0.003, −0.003 (L, seed 5). Quiz: Gini (6, 4) 0.48, entropy 0.971 (A2, A3); $\rho = 0.5$, $\sigma^2 = 1$, $B = 20$: 0.525 (A2).

**l9.** Equicorrelated 20% vols, $\rho = 0.5$: 0.08, 0.02, 0.02; shares 0.6667 and 0.8333 (L; A2). Variances 100 and 1, covariance 9: 100.8115, 0.1885, share 0.9981; correlation 0.9, share 0.95 (L, quadratic and `eigvalsh`; A2, `np.roots`; A3 correlation by simulation). $x_1, x_2$ at 0.95, $y = x_1 - x_2$: share 0.975, $R^2$ 0 and 1 (L; A2 on the 40 plotted points, seed 12, exact moments). Noise $p/n = 0.5$: top 2.8704, edges 2.9142 and 0.0858 (L; A2 by SVD, seed 0); the 1,000 plotted eigenvalues are that run rounded to three places. Yield curve (sd 5, 6, 6 bp; correlations 0.9, 0.75, 0.9): eigenvalues 87.9111, 7.4896, 1.5993, trace 97, shares 0.9063, 0.0772, 0.0165, loadings (0.487, 0.631, 0.605) and (0.707, 0.122, −0.696) (A2, `eigh` and power iteration; determinant of R 0.0325 by formula and numpy). Quiz: 0.8 at $\rho = 0.6$; 0.7 at $\rho = -0.4$; edge 2.25 at $p/n = 0.25$ (A2 and by hand).

**l10.** $t$ at $r = 0.05$: 0.7884 (250), 1.1172 (500), 1.5815 (1,000), 1.9601 (1,535); $n$ needed 1534.74 so 1,535; $(1.96/0.05)^2 = 1536.64$; p 0.4312 (L and LC, formula against `linregress` on exact-moment samples; A2). Unsquared slip: 785 days (by hand). Sharpe $0.05/\sqrt{1.0025} \times \sqrt{252} = 0.7927$, daily 0.04994, simulation 0.7817; P&L mean 0.05 and variance 1.0025 (L; A3 simulation). Best of 50: $E\max|Z| = 2.5096$, $|r|$ 0.1587, simulation 0.1585, $R^2$ 0.0252 (L). The `bars` sim draws `maxn(50, abs(n())) / sqrt(250)`, whose exact mean is 0.1587. Leakage $1/\sqrt{3} = 0.5774$, $R^2$ 1/3 (L simulation; A3 by covariance). Costs $5 - 2 \times 3 = -1$ bp (A2). Futures file: lag 1 0.12350273, $t$ 3.92775 on 998 pairs; lag 2 0.0181764 ($t$ 0.5734); lag 5 0.0059420 ($t$ 0.18715); simple-return lag 1 would be 0.12410 (IC, `corrcoef` against `autocorr` and OLS; A2 by hand). Small test files: −0.5303528865354435 and −0.9999461364888758 (A2, numpy against pure Python; simple returns differ by 3e-5 and 1e-5, so the relative 1e-9 tests catch them). Quiz: $t$ 1.5827 at $r = 0.1$; $n$ 9,602 at $r = 0.02$ (A2, formula and search); halves at ±0.1 pool to 0 (L).

**Review and homework.** R2.3 −0.6, R2.4 1.2 (IC); R2.5 parent 0.48, children 0.2778 and 0.375, weighted 0.3167, gain 0.1633 (IC, fractions and a fitted tree); R2.6 1.944 (IC); R2.7 eigenvalues 0.043028 and 0.006972, share 0.8606, standardised 0.75 (IC); R2.8 1,535 (IC); R2.9 1/3 (L). H2.1 soft threshold (LC: soft(1.9, 1) = 0.9, soft(−0.8, 1) = 0, soft(3.5, 1) = 2.5). H2.2 five brief cases plus a shuffled-order case (5.6, 2.4, 5.6, 2.4) (IC; A3 against sklearn). H2.5 0.091761, 0.008239, share 0.9176, standardised 0.70 (LC; A3 by the discriminant). H2.6 0.975, 0, second component (IC, L). H2.7 $200 \times 0.98^{50} = 72.83$; $200/e = 73.58$ as a wrong key (IC; A3). H2.8 as above.

## Departures from the brief

- l6 hook: graded with a `drag-point` (the point rides the error curve; target $c = 0.5$, tolerance 0.03 on $x$) instead of a `numeric`, since the screen says "Drag $c$"; the `numeric` (error 0.5) is the next screen.
- l10 transfer: `lag1_corr(path)` only, so the homework's `lag_corr(k)` and `lag_t(k)` (H2.8) still add something; lags 2 and 5 are quoted in the explanation.
- H2.4 (b): the brief says "`choice`: ridge or an elastic net". A `choice` has one right option, so it is a `multi` ("Select all that apply") with ridge and elastic net right.
- Review and homework order changed (above). H2.4 is first in `homework-2` because the playthrough's homework parts check only works when the three-part item is item 1 (backlog bullet).
- The brief's "about 0.37, 0.39, 0.00, 0.00" importances are shown with three places as the script prints them (0.373, 0.387, 0.003, −0.003).

## Proposed `course.json` change

None.

## Backlog

Six bullets in `docs/BACKLOG-INBOX.md` under "Raised later (research-int L2, 4 Nov)".
