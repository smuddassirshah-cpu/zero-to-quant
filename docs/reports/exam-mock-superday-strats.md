# Report: mock-superday-strats

Written from `## mock-superday-strats` in `docs/briefs/mocks.md` (the brief was written first, in the shape of `mock-superday-trader` and `mock-superday-research`).

## Files

- `app/content/exams/mock-superday-strats.json`: 5 papers and 2 checks, 20 items, 165 minutes.
- `docs/briefs/mocks-scripts/superday_strats_build.py` (route A, writes the file), `superday_strats_check.py` (route B), `superday_lib.py` (item constructors and a voice stop, shared with the developer mock). The scripts follow the `oa_quant_data_build.py` naming (the id without `mock-`); none is called `numbers.py`.
- `docs/readiness.md`: the two `mock-superday-strats` status rows now read `exists`; `node app/tools/readiness-sums.mjs --write` then changed `app/content/readiness.json` only in the two `mocks.present` and `mocks.missing` lists (checked with `git diff`).

| Paper | Minutes | Items | Kinds | Difficulty | Pass |
| --- | --- | --- | --- | --- | --- |
| Probability | 30 | 5 | 1 `parts` (2 numeric), 2 numeric, 2 choice | 3, 4, 4, 4, 4 | 0.6 |
| Derivatives pricing and risk | 45 | 7 | 3 numeric, 2 choice, 1 `parts` (2 numeric), 1 `longform` | 3, 3, 4, 3, 3, 3, 5 | 0.6 |
| Stochastic calculus | 30 | 4 | 1 `parts` (2 numeric), 1 choice, 1 numeric, 1 `longform` | 4, 3, 4, 5 | 0.5 |
| Coding | 45 | 2 | 1 `parts` (Python code, Python code, choice), 1 C++ code | 4, 4 | 0.5 |
| Fit and motivation | 15 | 2 | 2 `longform` | 3, 3 | 0.5 |

Families (first tags), all new to the mocks: `ruin-with-drift`, `orthant-correlation`, `range-of-uniforms`, `poisson-thinning`, `max-of-two-normals`, `atm-approximation`, `parity-arbitrage`, `gamma-theta-pnl`, `digital-from-calls`, `mc-interval-paths`, `convergence-order`, `realised-vs-implied`, `martingale-correction`, `gbm-median`, `reflection-touch`, `log-contract`, `barrier-tree`, `variance-interpolation`, `why-strats`, `model-versus-market`.

## Results

- Validator: 0 errors; no warning names this file.
- Voice scan on a copy (`VOICE_BASE=<scratchpad>/exam-superday/vs-strats/`): 0 sentences over 20 words of 463, 0 explanations over three sentences.
- `python3 docs/briefs/mocks-scripts/superday_strats_check.py`: `numbers_lib: 202 of 202 checks passed`, exit 0. `check_wrongs()` lists 15 "check by hand" lines: each is a `byKey` line that names the slip's arithmetic (for example "4 times 2") rather than the slip's value; all were read and are right.
- `node tools/fresh-check.mjs --exam mock-superday-strats --min-run 10`: 0 hits. The first draft had 18: a Poisson buy-and-sell setup and a "40,000 paths, standard deviation £12" setup that matched `markov/review-4` and `topic-2.5` (both rewritten with new setups and numbers), the longform opening line shared with the other superdays, the tree formula skeleton and two phrasings. All were rewritten.
- Playthrough `--exam mock-superday-strats --local-cdn <pkgs>`: ok, 25 items (parts counted), scored 20 of 20, passed; mock checks ok. With `--mobile`: ok, the same. One note at 440 px: the time-up results page is wider than the window, an engine matter (the research mock does the same at 390 px).
- `node tools/readiness-sums.mjs`: OK after the status rows above.
- Screenshots (1280 and 390 px, `<scratchpad>/exam-superday/sh/`, by `shots.mjs` because the playthrough names exam shots by item index only): the start card, a `parts` numeric item, a choice, the four-option arbitrage choice, a longform, the Python `parts` code item, the C++ item and the results page. Fixes made from them: the C++ draft's comment lines were wrapped to fit the editor.

## Every number and its source

Route A is the build script, route B the check script; both are in `docs/briefs/mocks-scripts/`.

| Item | Key | Route A | Route B |
| --- | --- | --- | --- |
| P1 part 1 | 0.6090 | $(1 - (2/3)^2)/(1 - (2/3)^6) = 81/133$ | exact linear solve over states 1 to 5 |
| P1 part 2 | 8.27 | Wald: $(220/133)/0.2 = 1100/133$ | exact linear solve for expected steps |
| P2 | $1/3$ | $1/4 + \arcsin(0.5)/(2\pi)$ | Simpson on $\varphi(x)\Phi(x/\sqrt3)$; $-0.5$ gives $1/6$ |
| P3 | 36 | $60 \times 3/5$ | exact integrals: $E[\max] = 4/5$, $E[\min] = 1/5$ |
| P4 | 6 | $18 \times 1/3$ | sum over the Poisson total with the binomial split |
| P5 | 0.011284 | $0.02/\sqrt\pi$ | Simpson on $2x\varphi(x)\Phi(x)$; $E\lvert X\rvert = 0.015958$ |
| R1 | 9.97 | $250(2\Phi(0.05) - 1) = 9.9695$; rule 10 | Simpson on the lognormal payoff |
| R2 | £0.10 now | $3.10 - 3.00$ on `Fraction`s | cash today of each trade, payoff at expiry at 30, 50, 80 |
| R3 | 20 | $200(0.40 - 0.30)$ | repricing a quadratic value over a day |
| R4 | 0.55 | $(5.40 - 4.30)/2$ | call-spread payoff checked at expiry |
| R5 | 0.18, 810,000 | $2 \times 27/300$; $(54/0.06)^2$ | float; bisection on $54/\sqrt n = 0.06$ |
| R6 | 0.0003 | $0.0048/16$ | order measured from $ch^2$ at two steps |
| R7 | about £0.375 | $\tfrac12 \times 0.04 \times 10^4 \times 0.0225/12$ | the daily P&L summed over 21 days |
| S1 | 6, 3 | Itô by hand | generator on polynomials, search over $a, b \le 19$ |
| S2 | £41.63 | $40e^{0.04}$; mean $40e^{0.2} = 48.86$ | bisection on the lognormal CDF; Simpson for the mean |
| S3 | 0.1336 | $2(1 - \Phi(1.5))$ | Simpson on the first-passage density |
| S4 | about 4.514 | $e^{-0.02}\ln 100$ | Simpson on $\ln S_T$ |
| C1 | 13 test values | reference run in CPython | path enumeration for $n \le 12$; 1,000 steps within 0.005 of Black-Scholes 10.4506; a second node formula |
| C2 | 9 test values | reference compiled by g++ | g++ again; piecewise-flat forward variance |

Every `wrong` value is asserted by route B at its id, and the last pass of the check matches every number in every learner-visible string of each item to a route-B or given value.

## Prerequisites cited (gated by `requires`)

markov L5 (`l10-gamblers-ruin`, `l11-reflection`, `l16-arrivals`, `l19-optional-stopping`), options L3 (`l9-put-call-parity`), trees L4 (`l8-python-pricer`, `l12-delta-hedging`, `l13-rules-of-thumb`, `l15-digitals`, `l18-gamma-and-hedging`), ito L4 (`l4-gbm`, `l6-ito-lemma`, `l11-prices-as-expectations`, `l12-barrier-option`, `l13-martingale-or-not`, `l14-hitting-and-exit`, `l16-pricing-in-a-minute`), numerics L4 (`l14`, `l15`), cpp-pricing L2, recruiting L3.

## Proposals

- No `prep.json` change: the mock is named on `superday-strats` and three firm paths.
- The parallel author of `mock-oa-strats` also changes the strats rows of `docs/readiness.md` and the same lists in `readiness.json`; rerun `readiness-sums.mjs --write` after the merge.
