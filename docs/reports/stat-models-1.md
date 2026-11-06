# stat-models level 1 (Generalised linear models): author report

Session T, content wave 1. Brief: `docs/briefs/stat-models.md`, preamble and `## Level 1`.

## Files written

| File | Screens / items | Quiz | Notes |
|---|---|---|---|
| `l1-beyond-normal-errors.json` | 10 | 4 | hook: drag a straight line through D1; `place` families and links; `table` variance functions; D3 bars; code `link`, `inverse_link`, `variance_function` (14 tests) |
| `l2-logistic-as-glm.json` | 12 | 3 | hook: D12 `pair` (curve beside the log-likelihood contour, draggable $\boldsymbol\beta$); odds, PD, tangent marginal effect, Wald interval, score derivation; code `neg_log_lik` + `fit_logistic` (SciPy), code `glm_logit` (statsmodels, budget 60000); fills transfer |
| `l3-poisson-regression.json` | 11 | 3 | hook: D2 counts versus rates (`options` + `frames` control); offset, rate ratio, free $\ln t$ check, no-offset trap, zero-count edge; code `poisson_nll` + `fit_poisson`, code `two_ways` (statsmodels offset and exposure, budget 60000) |
| `l4-irls.json` | 12 | 3 | the exit lesson: six points by hand ($z = \pm 2$, slope 14/17.5), weights, SE from $\mathbf{X}^T\mathbf{W}\mathbf{X}$ (`matrix`), Newton derivation with a frozen-weight distractor, D1 iterations on a `frames` slider, frozen-weight trap, Poisson $z$ with the double-offset slip, separation; code `irls_logistic`, code `irls_poisson` + `match_statsmodels` (budget 60000) |
| `l5-deviance.json` | 11 | 3 | D3 bars with a Poisson curve on a slider; deviance by hand; dispersion; $\chi^2_1$ `plane` with `area` `label: "auto"`; quasi-Poisson $F$; trap; NB2; deviance derivation; binary deviance edge; code `poisson_deviance`, `dispersion`, `lr_test`; twenty-signals transfer |
| `review-1.json` | 9 items, difficulty 2 to 4, `pass: 0.8` | | interleaves all five lessons |
| `homework-1.json` | 8 items, difficulty 3 to 5 (two at 5) | | `h-irls` code item (difficulty 5, `performance: "code"`, 7 tests), `h-newton-pois` order derivation, `h-colleague` longform with 10-point rubric and full model answer |

Every lesson has skill `sm-glm` and the course.json objective verbatim. No level-1 objective starts with a rule verb, so the performance task is practice only (it never gates met); it marks the exit task.

## Gates (SESSION PROTOCOL 4)

1. Validator: `node tools/validate.mjs`: **0 errors** (2145 warnings repo-wide; for these files only "ladder reuses the previous canvas kind" and "point hint usually highlights" warnings remain).
2. Voice scan: `VOICE_BASE=app/content/courses/stat-models/ python3 docs/reviews/voice-scan.py`: **0 explanations over three sentences, 0 sentences over 20 words**.
3. Numbers: `python3 docs/reports/stat-models-L1-numbers.py`: **266 of 266 checks passed**, exit 0 (NumPy only).
4. Playthrough: all five lessons, `--set stat-models/review-1` and `--set stat-models/homework-1` with `--mobile --tablet --local-cdn <pkgs>` (desktop, 440, 1032 and 1376): **all passed**; the homework's performance starter fails as required and the longform is marked by the button. Screenshots looked at: the D1 plane, the `pair` (stacked at 440), the counts/rates switch, the D1 iteration frames, the D3 bars with curve, the place and table widgets. Fixes made after looking: hline labels removed, pair prose no longer says "on the right" (it stacks on a phone), a curve label moved clear of the points.

## Numbers and their sources

Every dataset was regenerated in Pyodide 0.27.7 (NumPy 2.0.2, SciPy 1.14.1, statsmodels 0.14.4, scikit-learn 1.6.1) run in Node from the local wheels. Local NumPy 2.5.3 gives byte-identical streams for seeds 11, 13, 23 and 61 (checked by dumping all four datasets). Every planner value in the brief was reproduced exactly in Pyodide; none differed: 106 defaults, OLS $(-0.198849, 1.154923)$, 68 of 300 outside $[0, 1]$, the D12 values $-8.317766$, $-6.263552$, $-6.479063$, $(-3.721962, 6.133700)$, $-5.853041$, D1 $(-5.451164, 8.690639)$ with SE 0.611328 and 0.968994 in 6 iterations, 2.3847, 24.86%, 65.30%, 0.6272, 1.62 and 0.20 points, the penalised $(-3.510915, 5.424648)$, fills $(1.293818, -0.972967)$ with SE 0.202580 and 0.090413, 78.48%, 34.25%, 0.3780, 7,125 trades, D2 $(-0.478593, 0.059135)$ with SE 0.038521 and 0.001534, 1.8064, 30.33, 2.0220, $-0.020324$, 0.8161, 0.976228 (SE 0.022235), 0.9780, 1.0986, 13.5%, the six-point iterates and deviance 4.955974 with SE 2.545711 and 0.912585, the five D1 iterates, 0.835439, 111.228895, the separation slopes, 4.405, 17.117, 28 zeros, $(1.433431, 0.385410)$, 631.371, 625.317, 3.158, 5.557, 0.0184, 0.0191, 1.769, 0.185, 0.5422, 1.183, 0.277, 0.687, 204.639.

Differences worth stating:
- scikit-learn's own `LogisticRegression()` (lbfgs, default tolerance) returns $(-3.510805, 5.424353)$ in Pyodide, not the exact penalised minimum $(-3.510915, 5.424648)$; the quiz says "near $-3.51$ and $5.42$", and the script checks the exact minimum by its own penalised Newton loop. `penalty=None` gives $(-5.449638, 8.687685)$, again lbfgs tolerance.
- Separation (x = 1..6, y = 0,0,0,1,1,1): the plain loop's slope is 1.0286, 1.8172, 2.8825, 4.5016, 6.5394 at iterations 1 to 5 and 16.6352 at 10; it returns NaN at iteration 11 in Pyodide (the brief said "by iteration 15", which holds). statsmodels 0.14.4 in Pyodide stops after 22 iterations at $(-144.318226, 41.233779)$ and emits `PerfectSeparationWarning: Perfect separation or prediction detected, parameter may not be identified` (three times). Nothing tests it.
- Six-point SEs: statsmodels gives 2.545711 and 0.912585 from its last iterate; the script's fully converged loop gives 2.545713 and 0.912586. The lesson quotes statsmodels; the hand computation from the rounded $\mathbf{X}^T\mathbf{W}\mathbf{X}$ gives 0.9126.
- NB2 $\hat\alpha$: statsmodels 0.542248, SciPy 0.5422505, the script's profile likelihood 0.542251; the lesson says 0.5422.
- Iteration counts used in tests (stop when the deviance changes by less than $10^{-10}$, counting updates from $\boldsymbol\beta = \mathbf{0}$): six points 6, D1 7, a `tol` of 1.0 on the six points 2. statsmodels reports 5 and 6 under its own rule.
- Values added beyond the brief, each computed twice (script and a hand or Pyodide check): crossing leverage 0.1722; expected loss £2,962 against $-$£63,496 at $L = 0.05$; log loss 0.4878; Wald lower end 6.7914; $z = 1.73$ on D12; $-1.069$ for the $\ln t$ coefficient against 1; $-10.110$ for a quiet 5-minute interval; 54.79 trades at $v = 30$; weight 0.1050; SE 0.9126; Poisson $z = 1.0208$ (slip 3.7289); deviance 2.6096 of three counts; 2.443 expected zero days; NB2 variance 14.93; 5.38 false signals of 20 (true size 26.9%); the review and homework values (1.4191, 2.7183, 0.0736, 0.42, 0.04, 3.0, 23.70 points, 90.27, 0.2767); D2 Pearson $\chi^2 = 113.064$ on 118 df (0.96) in the model answer.

The numbers script computes each fit by its own IRLS (logistic, Poisson), a grid search (D12 peak), a penalised Newton loop (scikit-learn's objective) and a profile likelihood over $\alpha$ with IRLS inside (NB2), asserts agreement with the Pyodide statsmodels values pasted in `SM`, then checks each stated number with `lv.expect` at its JSON path (prose, `wrong[]` values, feedback, hints, `explain`, canvas text and test expectations).

## Tolerances and runtime

- Coefficient tests: `isclose` with `tol: { "abs": 1e-5 }` for SciPy minimisers (BFGS from zeros, as each `how` says) and `1e-6` for IRLS and statsmodels; arrays compared as lists with `isclose` or rounded with `equal`. Expected values are statsmodels' full-precision Pyodide values. Every starter fails (`...` bodies); every solution passes in the playthrough.
- Screens that import statsmodels carry `"budget": 60000` and a `how` that says the first run loads statsmodels in 20 to 40 seconds (KNOWN_ISSUES figure). Load time measured here, Pyodide in Node from local wheels: NumPy + SciPy + statsmodels 3.1 to 4.5 s; with scikit-learn 7.5 s. The browser over jsDelivr could not be measured in this sandbox.
- Data seeds: D1 seed 11, fills seed 13, D2 seed 23, D3 seed 61, all in the brief's order of draws; hidden tests rebuild them in a `setup` line with NumPy only (`1 / (1 + np.exp(6 - 10 * L))` in place of `expit`, which reproduces the 106 defaults and the same fit).

## Proposed course.json change

None.

## Backlog

Five bullets under `Raised later (stat-models level 1):` in `docs/BACKLOG-INBOX.md` (table `wrong[]` keys, second sighting; no compact data form on `plane`; voice scan reading formulas; no load-time report; pair prose when stacked).
