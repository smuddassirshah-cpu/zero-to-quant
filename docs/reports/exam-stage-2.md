# Stage 2 exit test

File: `app/content/exams/stage-2.json`. Data: `app/content/data/stage-2/` (six CSV files, written by `build.py` from fixed seeds). Scripts: `docs/briefs/exam-stage-2-scripts/` (`build.py` route A, `check_numbers.py` route B, `fresh.py`).

## Design (written before the build)

Source: the `**Exit:**` lines of topics 2.1, 2.2, 2.5 and 2.6, the project and contest text of 2.3 and 2.4, and the track table at the top of Stage 2 in `docs/curriculum.md`. What the app can mark becomes paper items; what it cannot becomes a `check`.

| Exit line | Paper items (auto) | Check (self-ticked) |
|---|---|---|
| 2.1 one tabular problem end to end with time-ordered CV; explain leakage, regularisation, bias-variance | A: walk-forward ridge code item on a data file, scaler fitted per fit (a leaky version fails); leakage multi, learning-curve choice, shrinkage, lasso, purge, lambda chosen on validation blocks only; trees, boosting, labels, sizing, PSR | the project in a repository; the three ideas explained aloud |
| 2.2 test a pair for cointegration; why returns, not prices | B: Engle-Granger code item on a price file, then the half-life; a Dickey-Fuller t by hand; the returns choice; ARMA, ACF, GARCH, EWMA, ES, pair P&L | none |
| 2.3 three projects with tests and a results note | D: backtest (fills, survivorship, a Sharpe interval, held-out period, Sortino), alpha (signal weights, the fundamental law, costs, an IC and turnover code item on a panel file), options (gamma P&L, a butterfly density, a parity-fit code item, an ATM volatility) | one check per project |
| 2.4 weekly contests, rating towards 1400 | D: counting, prefix sums, constraints, rating odds; one drawn `drills/oa` problem | contests entered, rating recorded |
| 2.5 one option by FD, quadrature and MC with a control variate, each error explained; KKT mean-variance by hand and matched to a solver | C: three-part code item (explicit grid, Simpson split at the strike, MC with control variates); an error-rate table; KKT by hand (parts) and a KKT code item checked against SLSQP; float, conditioning, Newton, LP duality, convexity, projected gradient | none |
| 2.6 logistic and Poisson by own IRLS, matched to statsmodels; MCMC with a convergence check | C: two-part IRLS code item on two data files; an MCMC sampler and R-hat code item; GLM, factorial, signed-rank, conjugate, batch-means and hierarchical items | none |

Papers, pass 0.7 each (the stage-exam pass in DECISIONS), minutes 1.25 times the summed `pace`, rounded up to 5. Four papers by area: A machine learning and validation (2.1), B time series (2.2), C numerical methods, optimisation and statistical modelling (2.5, 2.6), D backtesting, alpha, options and contests (2.3, 2.4). Validation is time-ordered everywhere (DECISIONS): walk-forward blocks, a purge, a held-out final block; no shuffled folds. The bank holds no stage-2 family (its files are probability, market making, mental maths, brainteasers and behavioural), so the only draw is `drills/oa`, the contest-style coding pool.

## Result

- **Paper A, machine learning and validation**: 90 min, 16 items (12 numeric, 1 choice, 1 multi, 1 parts, 1 code), ramp 3, 8, 4, 1. The 2.1 exit is `nested_walk_forward`: walk-forward ridge on `factor-days.csv`, the penalty chosen on a time-ordered validation tail before each block, every fit scaled by its own training rows. A full-sample scaler, a test-block penalty choice and a sample standard deviation each fail a hidden test.
- **Paper B, time series**: 75 min, 15 items (11 numeric, 2 choice, 2 parts), ramp 3, 8, 3, 1. The 2.2 exit is `adf1_spread`: Engle-Granger with one lagged change on `pair-closes.csv` (a-b rejects at $t = -5.28$, a-c does not at $-3.04$), then the spread's half-life. A plain Dickey-Fuller without the lag fails a test. The returns-not-prices choice is item 1.
- **Paper C, numerical methods, optimisation and statistical modelling**: 155 min, 19 items (10 numeric, 1 choice, 1 multi, 1 table with slip ids, 5 parts, 1 code), ramp 2, 9, 5, 3. The 2.5 exit is a three-part code item: an explicit grid in log price, Simpson over the lognormal density from the strike, Monte Carlo with $S_T$ and $S_T^2$ as controls (a one-control estimator fails the error bound). KKT by hand (two parts) and `mv_weights` (checked against SLSQP). The 2.6 exit is `irls_grouped_logit` plus `poisson_irls_se` (coefficients and standard errors), then `gibbs_normal` plus `rhat` on `chains.csv`.
- **Paper D, backtesting, alpha, options and contests**: 135 min, 18 authored items (13 numeric, 3 choice, 2 code: `ic_and_turnover` on `signal-panel.csv`, `parity_fit`) plus 1 drawn drill (19).
- **Six checks**: the 2.1 project with time-ordered CV, the 2.1 explanations aloud, the backtesting engine, the alpha research, the options dashboard (the live data handler on the developer track), weekly Codeforces contests with the rating recorded.
- Every topic 2.1 to 2.6 has at least two auto-graded items, and every one of the 66 Stage 2 skills is on an item; `check_numbers.py` asserts both from `curriculum.json`.

## Draws (tags used)

- D: `drills/oa`, difficulty 3 to 4, n 1, pool 8, no tag filter (patterns dp, greedy, graphs, binary-search, two-pointers, windows, stacks-queues, heaps-tries). Counted at 1,800 s in the paper's minutes.
- No bank draw: no bank family fits Stage 2.

## Gates

- Validator: 0 errors, no warning on `stage-2.json`.
- Voice scan on a copy (`VOICE_BASE=<scratch>/voice2/`): 0 sentences over 20 words, 0 explanations over three sentences, 1,344 sentences. No exclamation marks, em-dashes or en-dashes.
- `check_numbers.py`: 823 of 823, exit 0. Route B: grid searches, bisection and brentq, Fractions, companion-matrix roots, scipy SLSQP for the KKT weights, HiGHS duals for the LP, scipy root on the score equations for both GLMs with the Fisher information for the standard errors, an expanded one-row-per-order logistic fit, `scipy.stats` for ranks, the inverse-gamma posterior and the chi-squared points, Simpson tail integrals, a numerical gamma, brute-force counts, a separate S-grid showing the table's rates (4.0 and 16). Every code solution passes its tests and every starter fails one. Each code task's expected values are recomputed by a second implementation or by route B, and the named flawed versions fail. A last pass reads every number in every learner-visible string.
- Playthrough with `--local-cdn`: green with and without `--mobile` (78 items, 69 of 69 scored, passed). Screenshots at 440 px checked per paper: long formulas moved to display maths or split into coefficients, code specs moved into prose.
- `readiness-sums.mjs`: OK.

## Freshness

`fresh-check.mjs --exam stage-2` ends on 53 hits, all stock notation or phrasing: `x_t = ... + \varepsilon_t`, `\mathbf w^T\boldsymbol\Sigma\mathbf w subject to`, `S = 80, K = 84, r = ...`, "half-life in days, give 2 decimal places", the R-hat formula and the code signature `(S0, K, r, sigma, T, n, seed)`. Cleared in the first build, as reused setups:

- The lasso soft-threshold on orthonormal features (`mock-superday-research`) became the penalty where the lasso path starts; the ARMA(1,1) $\rho_2$ (arma homework 3) became a Yule-Walker $\hat\phi_2$; the Calmar from growth and drawdown (backtest l10, review 3) became a Sortino ratio; the decaying contest score (contests review 4) became rating odds; a Gibbs $\rho^2$ idea (stat-models l17) and the R-hat by hand became a batch-means error.
- `fresh.py` found code tasks repeating lessons: `walk_forward_mse` with ridge (validation l6, l10) became the nested walk-forward; the purge count of 695 (validation l6) became 830 on new blocks; `irls_logistic`/`irls_poisson` (stat-models l4) became a grouped binomial fit and a Poisson fit with standard errors; `metropolis` (stat-models l16) became a Gibbs sampler; `implied_vol` with bounds (opt-dash l9) became `parity_fit`; the share-only control variate (numerics l16, opt-dash l7) became two controls; the S-grid explicit scheme (numerics l13) became a log-price grid; the plain Dickey-Fuller of `engle_granger_by_hand` (coint l4) became ADF(1); SHAP values summing to 0.35 (stat-models review 1 uses 0.35 and 0.5866 as wrong values) were changed.
- Remaining `fresh.py` hits are common values in unrelated items (0.025, 1.05, 830, 5.16, 9.80, 0.0909).

## Notes for the main session

- The exit tasks of 2.1, 2.2, 2.5 and 2.6 are each taught as code in their courses (numerics l17 and homework 4 are "the exit task"), so the exam's code items are variants, not new kinds of task.
- `curriculum.json` stage 2 `exitTests` lists only the three projects; the exam follows the per-topic exit lines. Not edited here.
