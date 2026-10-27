# arma level 3 (ARMA): report

The authoring agent stopped before it reported. This report comes from a triage pass: every file was checked, given small fixes, and played again. The original generator scripts were not on disk (its scratchpad folder is gone). Every number below was recomputed from the generators in the files' own preludes.

## Files

All in `app/content/courses/arma/`.

| File | Screens or items | Quiz | Code screens |
|---|---|---|---|
| `l9-shocks-that-linger.json` | 11 screens, difficulty 1 to 3, `order` derive | 4 | 3 (`simulate_ma1`, `ma1_acf`, `theta_from_rho1`) |
| `l10-combining.json` | 12 screens | 3 | 3 (`aic_grid`, `best_order`, `oos_mse`) |
| `l11-forecast-intervals.json` | 12 screens, `order` derive | 3 | 3 (`ar1_forecast`, `ar1_interval_halfwidth`, `arima_fan`) |
| `l12-half-life.json` | 12 screens, `order` derive | 3 | 3 (`days_to_fraction` with `half_life`, `half_life_from_series`, `half_life_ci`) |
| `review-3.json` | 8 items: 2 at difficulty 2, 4 at 3, 2 at 4 | | |
| `homework-3.json` | 8 items: 2 at 3, 4 at 4, 2 at 5 | | 3 (`coverage` d4, `half_life_report` d4, `fit_and_forecast` d5); `order` item `h-cycle` (d3); `longform` (d5, 10-point rubric) |

## Validator

`node tools/validate.mjs`: 0 errors overall, and no errors or warnings on any level 3 file.

## Playthrough

`--local-cdn <scratchpad>/pkgs`, each file run alone, before and after the fixes:
- l9: ok, 15 checks, quiz 4/4
- l10: ok, 15 checks, quiz 3/3
- l11: ok, 15 checks, quiz 3/3
- l12: ok, 15 checks, quiz 3/3
- review-3: ok, 8 of 8 recorded
- homework-3: ok, 8 of 8, 37 of 37 marks

## Code checks

The playthrough runs solutions only. A CPython harness (statsmodels 0.15.0) ran all 15 code widgets with their preludes:
- every solution passes every hidden test and every example;
- every untouched starter fails at least one test.

## Numbers checked

Sources: CPython recomputation from the preludes' `make_ar1`, `make_walk`, `make_wn`, `make_arma` and `make_pair` (`make_pair` matches `docs/briefs/coint.md` line for line). Pyodide values that tests check are confirmed by the browser playthrough. All stated values agree to the places shown. Highlights:
- **l9.** Seed 21 MA(1):
  - ACF 0.4631, 0.0074, −0.0084, 0.0542, 0.0843; PACF 0.4641, −0.2650, 0.1511.
  - MA fit 0.0645, 0.6186, 0.9611, AIC 1405.57, Ljung-Box p 0.78.
  - AR(1) fit AIC 1454.31, Q = 49.16 (p 1.5e−7).
  - Sample variance 1.3513, mean 0.0617.
  - θ̂ from the spike 0.6726; `np.diff(make_wn(3))` ρ̂₁ = −0.515.
  - The overlap figure 0.4998 is from seed 3 (now stated).
- **l10.** Seed 33:
  - AIC grid as the brief; ℓ −710.224 and −709.303; BIC 1445.31.
  - Fit −0.0742, 0.7354, 0.3866, 1.0001; Ljung-Box Q 3.6617, p 0.8863.
  - Seed 32: AIC 1401.19 against 1393.21, BIC 1418.05 against 1418.49.
  - First 400 days: AIC 1107.64 and 1099.26; in-sample MSE 0.9126 and 0.8845 (from day 1); out of sample 1.1122 and 1.1244.
  - ARMA(5, 5): ℓ −540.82, out of sample 1.149.
  - White noise seed 5: 1380.96, 1381.57, 1381.75, 1380.66.
  - Common factor: AIC 1376.23 against 1378.41, coefficients −0.1667 and 0.2265.
- **l11.** Seed 41:
  - Fit −0.0931, 0.7764, 0.9683; half-widths 1.9287, 2.4418, 2.9360, 3.0603; limit 3.0604.
  - MA(1) forecast 1.0735, then 0.0645 with half-width 2.2593.
  - Walk seed 4 as AR(1): φ̂ 0.99559, mean 5.57; caps at ±21.0, against the walk's ±31.3 at 250 days and ±44.2 at 500.
  - Funding spread: 25.65, 0.8781, 8.8105, today 17.94, forecast 23.55 ± 11.70 (limit 12.16).
- **l12.**
  - Half-lives 1.000, 3.106, 6.579, 13.513, 34.31, 68.968.
  - Pairs spread: b −0.0508 (se 0.0099), half-life 13.288, interval 9.52 to 21.72.
  - `make_walk(26, 1000)`: b −0.0051, 137 days, ADF p 0.40.
  - Hook crossings: days 5 and 16; φ = 0.95 on 100 days gives 3.91.
- **Review and homework.** Every closed-form answer was recomputed by hand:
  - θ = −0.46; AIC 2411; half-width 2.191; forecast 2.648.
  - Half-lives 1.943 and 21.5 to 83.8; ρ₂ 0.3571; BIC gap 1.82.
  - The pipeline's seed 32 values: BIC (2, 2) by 0.40 on the training days; Ljung-Box p 0.515 against 0.035.
  - The long-form numbers: 22.8 days, 26%, se 0.0154, 11.2 days, t −1.95, bias 0.016, 46 days.

## Fixes made in this pass

Graded answers did not change; all edits are to wording.
- l9 trap prose: "0.46, A small" was a comma splice; now two sentences.
- Explanations cut to three sentences: l9 hook, l9 transfer, l10 trap, l11 hook, l12 hook.
- Sentences over 20 words split: l9 trap distractor, l9 quiz P&L prose, l10 screens 3, 6 and 9, l12 screens 5, 10 and 11, homework `h-coverage` and `h-fit-forecast` (prose, feedback, explanation).
- l11 trap distractor: "agree closely for the first 60 days" became 20 days. At 60 days the two half-widths differ by 12%; at 20 days by 4%.
- l12 screen 10 explanation: now says the 100-day interval misses the true 13.5.

## Departures from the brief

- l9 trap uses φ = 0.4631 (the sample spike) rather than 0.44, so ρ₂ = 0.2145.
- l11's `coverage` is a homework item (d4), not a lesson screen.
- `half_life` uses |φ| for negative φ and returns 0.0 at φ = 0, rather than raising `ValueError`. The brief allowed this choice.
- The l12 interval is computed from the fitted b and its se: 0.9297 to 0.9686, mapping to 9.52 to 21.72 days. The brief's estimate was 0.931 to 0.969 and 9.7 to 22.0.

## Proposed course.json change

None.
