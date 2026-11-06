# Stage 2 exit test

File: `app/content/exams/stage-2.json`. Data: `app/content/data/stage-2/` (three CSV files, written by `build.py` from fixed seeds). Scripts: `docs/briefs/exam-stage-2-scripts/` (`build.py` route A, `check_numbers.py` route B, `fresh.py`). Second read and fix pass: `docs/reviews/review-exam-stage-2.md`.

## Design (written before the build, revised by the fix pass)

Source: the `**Exit:**` lines of topics 2.1, 2.2 and 2.5, the project and contest text of 2.3 and 2.4, and the track table at the top of Stage 2 in `docs/curriculum.md`. What the app can mark becomes paper items; what it cannot becomes a `check`.

Topic 2.6 (statistical modelling) is marked [Quant: researcher track] in the curriculum, so it does not gate the exit test for every track. Decision (DECISIONS, Stage 2 entry, taken by the orchestrator, reversible): its items left the gating papers, as 3.2 and 3.4 left stage-3, and researchers sit `topic-2.6`. The first build held eight 2.6 items (a GLM count, two IRLS code parts, a factorial interaction, a signed-rank test, a gamma posterior, batch means, partial pooling, a Gibbs sampler with R-hat); they are in the git history of `build.py` and were not moved to `topic-2.6`. Their three data files (`fill-buckets.csv`, `jump-days.csv`, `chains.csv`) were removed. `build.py` still draws their random numbers, so `signal-panel.csv` keeps its seed stream.

| Exit line | Paper items (auto) | Check (self-ticked) |
|---|---|---|
| 2.1 one tabular problem end to end with time-ordered CV; explain leakage, regularisation, bias-variance | A: walk-forward ridge code item on a data file, scaler fitted per fit (a leaky version fails); leakage multi, learning-curve choice, shrinkage, lasso, purge, lambda chosen on validation blocks only; trees, boosting, labels, sizing, PSR | the project in a repository; the three ideas explained aloud |
| 2.2 test a pair for cointegration; why returns, not prices | B: Engle-Granger code item on a price file, then the half-life; a Dickey-Fuller t by hand; the returns choice; ARMA, ACF, GARCH, EWMA, ES, pair P&L | none |
| 2.3 three projects with tests and a results note | D: backtest (fills, survivorship, a Sharpe interval, held-out period, Sortino), alpha (signal weights, the fundamental law, costs, an IC and turnover code item on a panel file), options (gamma P&L, a butterfly density, a parity-fit code item, an ATM volatility) | one check per project, each note says what failed |
| 2.4 weekly contests, rating towards 1400 | D: counting, prefix sums, constraints, rating odds; one drawn `drills/oa` problem | contests entered, rating recorded |
| 2.5 one option by FD, quadrature and MC with a control variate, each error explained; KKT mean-variance by hand and matched to a solver | C: three-part code item (explicit grid, Simpson split at the strike, MC with control variates); an error-rate table; KKT by hand (parts) and a KKT code item checked against SLSQP; float, conditioning, Newton, LP duality with a pricing-out part, convexity, projected gradient | none |
| 2.6 logistic and Poisson by own IRLS; MCMC with a convergence check | none on the gating papers (researcher track, `topic-2.6`) | none |

Papers, pass 0.7 each (the stage-exam pass in DECISIONS), minutes 1.25 times the summed `pace`, rounded up to 5. Four papers by area: A machine learning and validation (2.1), B time series (2.2), C numerical methods and optimisation (2.5), D backtesting, alpha, options and contests (2.3, 2.4). Validation is time-ordered everywhere (DECISIONS): walk-forward blocks, a purge, a held-out final block; no shuffled folds. The bank holds no stage-2 family, so the only draw is `drills/oa`.

## Result

- **Paper A, machine learning and validation**: 90 min, 16 items (12 numeric, 1 choice, 1 multi, 1 parts, 1 code), ramp 3, 8, 4, 1. The 2.1 exit is `nested_walk_forward`: walk-forward ridge on `factor-days.csv`, the penalty chosen on a time-ordered validation tail before each block, every fit scaled by its own training rows. The ridge objective is stated. A full-sample scaler, a test-block penalty choice and a sample standard deviation each fail a hidden test.
- **Paper B, time series**: 75 min, 15 items (11 numeric, 2 choice, 2 parts), ramp 3, 8, 3, 1. The 2.2 exit is `adf1_spread`: Engle-Granger with one lagged change on `pair-closes.csv` (a-b rejects at $t = -5.28$, a-c does not at $-3.04$; both log prices have a unit root), then the spread's half-life. A plain Dickey-Fuller without the lag fails a test. The Ljung-Box item uses the degrees of freedom of an AR(1) fit.
- **Paper C, numerical methods and optimisation**: 90 min (4,170 s of pace), 11 items (4 numeric, 1 choice, 1 multi, 1 table with slip ids, 3 parts, 1 code), ramp 2, 5, 3, 1. One paper, since it is under 120 minutes. The 2.5 exit is a three-part code item: an explicit grid in log price, Simpson over the lognormal density from the strike, Monte Carlo with $S_T$ and $S_T^2$ as controls (a one-control estimator fails the error bound), at 1,800 s. KKT by hand (two parts) and `mv_weights` (checked against SLSQP; its visible example is not the hand problem).
- **Paper D, backtesting, alpha, options and contests**: 135 min, 18 authored items (13 numeric, 3 choice, 2 code: `ic_and_turnover` on `signal-panel.csv`, `parity_fit`) plus 1 drawn drill (19).
- **Six checks**: the 2.1 project with time-ordered CV, the 2.1 explanations aloud, the backtesting engine, the alpha research, the options dashboard (the live data handler on the developer track), weekly Codeforces contests with the rating recorded. The backtest, alpha and options notes each say what failed.
- Every topic 2.1 to 2.5 has at least two auto-graded items, no item carries a 2.6 skill, and every Stage 2 skill outside 2.6 is on an item; `check_numbers.py` asserts all three from `curriculum.json`.
- Every code item's visible example is a hidden test with its compare mode and tolerance, so Run examples shows the model solution passing. Every data starter imports pandas under a comment that says why.

## Draws (tags used)

- D: `drills/oa`, difficulty 3 to 4, n 1, pool 8, no tag filter (patterns dp, greedy, graphs, binary-search, two-pointers, windows, stacks-queues, heaps-tries). Counted at 1,800 s in the paper's minutes.
- No bank draw: no bank family fits Stage 2.

## Gates

- Validator: 0 errors, no warning on `stage-2.json`.
- Voice scan on a copy (`VOICE_BASE=<scratch>/voice3/`): 0 sentences over 20 words, 0 explanations over three sentences, 707 sentences. No exclamation marks, em-dashes or en-dashes.
- `check_numbers.py`: 766 of 766, exit 0. Route B: grid searches, bisection and brentq, Fractions, companion-matrix roots, scipy SLSQP for the KKT weights, HiGHS duals for the LP (and an LP with the third bond added), scipy `stats` for ranks and the chi-squared points, a search over centres for the absolute-error split, Simpson tail integrals, a numerical gamma, statsmodels ADF and MacKinnon points, brute-force counts, a separate S-grid showing the table's rates, a digital-call Simpson rate check. Every code solution passes its tests and its examples as Run examples compares them, every starter fails one, and the named flawed versions fail. A last pass reads every number in every learner-visible string.
- Playthrough with `--local-cdn`: green with and without `--mobile` (61 scored items, passed).
- `readiness-sums.mjs`: OK.

## Freshness

`fresh-check.mjs --exam stage-2 --min-run 10` ends on 13 hits, all stock notation or phrasing: the ridge objective, `x_t = ... + \varepsilon_t`, `\mathbf w^T\boldsymbol\Sigma\mathbf w subject to`, `S, K, r, \sigma, T`, "give 2 decimal places". `fresh.py` prints every matching file for each keyed number or phrase; the distinctive phrases of the new items have no hit (the common numbers 0.0175, 0.2764, 2.14 and 2.41 appear in unrelated items).

Items replaced after the second read, each with a new setup, a new twist or both, and its key nouns grepped across `app/content`:

- tree split by absolute error about the median (was squared error); order of fractional differencing that gives $w_2 = -0.1$ (was $w_3$ at a given order); five overlapping labels where the fifth lowers the total; the probability that sizes a bet at half the position (was the size at 0.62); $\omega$ by variance targeting (was the long-run volatility); the correlation at which $\kappa$ reaches $10^4$ (was $\kappa$ at 0.999); Simpson on a digital call; a dedication LP with new liabilities and bonds and a pricing-out part; the IC a target information ratio needs, on new numbers (was the ratio from an IC).
- Earlier clearances from the first build stand: the lasso path start, the Yule-Walker $\hat\phi_2$, the Sortino ratio, rating odds, the nested walk-forward, `parity_fit`, two-control Monte Carlo, the log-price grid, ADF(1).

## Notes for the main session

- The exit tasks of 2.1, 2.2 and 2.5 are each taught as code in their courses, so the exam's code items are variants, not new kinds of task.
- `curriculum.json` stage 2 `exitTests` lists only the three projects; the exam follows the per-topic exit lines. Not edited here.
- Engine items from the second read, open in the inbox: a validator warning for a float example with no `compare`; `importHint` reading each case's `setup`; a `required` flag on a paper item (a paper can still be passed without its code exit task).
