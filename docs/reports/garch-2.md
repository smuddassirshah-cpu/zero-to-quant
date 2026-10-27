# Report: garch level 2 (Models)

## Files written

All in `app/content/courses/garch/`. `l5-recent-days-more.json` was kept as triaged (`docs/reports/triage-27oct.md`) and not edited.

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l6-arch.json` | 12 screens, 4 quiz | `simulate_arch1` + `arch1_uncond_var`, `arch1_kurtosis`, `fit_arch1` (SLSQP, β bound (0, 0)) | gv-models |
| `l7-garch11.json` | 12 screens, 4 quiz | `garch_variance` + `neg_loglik`, `fit_garch` + `persistence_and_halflife` | gv-models |
| `l8-long-run-variance.json` | 12 screens, 4 quiz | `long_run_variance` + `long_run_annual_vol` + `variance_half_life`, `fit_variance_targeted` | gv-models, gv-forecast |
| `review-2.json` | 10 items: difficulty 2 (4), 3 (4), 4 (2); l5 to l8 interleaved | | |
| `homework-2.json` | 9 items: difficulty 3 (4), 4 (3), 5 (2) | `forecast_mse` with `ewma_variance` (4), `fit_and_report` (5) | |

Homework also has an `order` item (fitting GARCH by maximum likelihood, from closes to a checked fit), a `longform` (a fit with α̂ + β̂ = 0.999 on 504 days; 10-point rubric, full model answer), numerics (a long-run vol, the excess left after 252 days at persistence 0.995, ω in decimal units) and two choices (a stalled decimal fit; EWMA λ = 0.97 as GARCH).

Lesson shapes:

- l6: drag yesterday's return on the ARCH news-impact parabola to a variance of 2.5 %² (either ±2); explore three ARCH paths with the same shocks, α = 0, 0.3, 0.5 and ω = 1 − α (sd 1.00, 1.01, 1.00; raw kurtosis 3.02, 3.74, 5.29); name ARCH(1) (Engle 1982) with a one-step volatility (√5 = 2.24%); the expected-variance dots and the level ω/(1 − α) (0.2/0.4 = 0.5); `simulate_arch1` code (seed 11 sd 0.010013); `arch1_kurtosis` code with a number line (theory 9; seed 11 5.29; 20 seeds 6.06, range 4.12 to 13.62); r² correlograms ARCH against B (0.42, 0.14, 0.05 against 0.36, 0.29, 0.27); trap: a loop that reads `r[t]` from `np.zeros` (sd 0.007084, kurtosis 3.02, lag-1 r² ACF 0.015); `fit_arch1` code (ω̂ = 0.487, α̂ = 0.535; on B α̂ = 0.225); edge cases α = 0, 0.9, ≥ 1 on an expected-variance plane with stops (multi); derive the unconditional variance (`order`); transfer: an earnings day under ARCH (√33.6 = 5.80% a day), Engle's 2003 Nobel prize.
- l7: hook on B's slow r² memory (what to add: yesterday's variance); explore the expected variance after a 5% shock with α and β sliders (β sets the fade, α the jump); name GARCH(1,1) (Bollerslev 1986), ARMA(1,1) in r² (`arma` l10), one step 1.64 %²; five storm days by hand in a `table` (3.2346 to 3.0426, 4.6398, 6.8041, 7.4991, 7.4080); two daily log-likelihood scores (−5.200, −3.123); `garch_variance` + `neg_loglik` code (2625.3778 at the truth); drag along the log-likelihood profile in α to its peak, 0.063 (−2623.83), the truth 0.08 marked; `fit_garch` + `persistence_and_halflife` code, with the `arch` package sentence and why % units; the decimal fit stalls (table); trap: 0.9864 against 0.98 on a 20-path histogram; 1,000 days and series A (multi); transfer: an index fit with persistence 0.99 (half-life 68.97 days) and a pegged currency.
- l8: drag the level two models head for (1 %²); explore ω, α, β with a live level (β = 0.91 doubles it to 2.0); name V_L with its derivation, 15.87% a year; the fit's 14.96% from 6-place inputs; half-life 50.62 days at 0.9864; three closed-form functions in code; V_L against persistence near 1 (0.995 gives 24.69% a year), IGARCH and EWMA; 20-path histogram of long-run vols (13.1% to 18.2%); `fit_variance_targeted` code; trap: ω read as the long run (1.75%) or a storm window (38.6%); derive V_L (`order`); transfer: the `trees` l10 one-year call at the long run (£8.91, against £10.4506 at 20%).

## Validator

`node tools/validate.mjs` from `app/`: 0 errors in the garch files. The last run reported 0 errors overall (306 warnings). One run in between showed 6 errors in `content/exams/topic-1.9.json`, which another agent was writing. The garch level 2 files have 26 warnings, all deliberate: a ladder that changes canvas kind and point hints without a highlight.

## Playthrough

Final run, after the last edit: `node tools/playthrough.mjs --lesson garch/l5-recent-days-more --lesson garch/l6-arch --lesson garch/l7-garch11 --lesson garch/l8-long-run-variance --set garch/review-2 --set garch/homework-2 --local-cdn <scratchpad>/pkgs --shots <scratchpad>/garch-2/final --mobile`. No console errors.

| File | Result |
|---|---|
| l5-recent-days-more | 15 checks, quiz 4/4 |
| l6-arch | 16 checks, quiz 4/4 |
| l7-garch11 | 16 checks, quiz 4/4 |
| l8-long-run-variance | 16 checks, quiz 4/4 |
| review-2 | 10 of 10 recorded |
| homework-2 | 9 of 9 right, 39 of 39 marks |

One earlier run of the two sets failed with "0 items" and a timeout while another playthrough was running. The same command passed alone straight afterwards, and in both later runs. I also ran the lessons with `--why` and read the explanation sheets. I looked at the screenshots at 1280 and 390 px and fixed these: an x-axis title printed over the caption (l6 hook, l8 sensitivity plane); a flat edge-case curve that started at its own level (l6, now from 4 %²); starter lines over 54 characters (l6, l7, l8 code); an empty first bin (l8 histogram); and a misplaced "fit" label (l8 transfer). Every code solution passes its hidden tests in CPython (`harness.py`), and no starter passes any.

## Numbers and their sources

I computed every number in CPython (NumPy 2.5.3, SciPy 1.18.1, statsmodels 0.15.0) in the builders. I computed them again in Pyodide 0.27.7 under Node (`pyrun.mjs`, local wheels: NumPy 2.0.2, SciPy 1.14.1, statsmodels 0.14.4), and the browser playthrough ran every hidden test in Pyodide. The two runtimes agree on every number stated in the lessons, except the two platform differences below, which the lessons describe.

- Course facts reproduced: fit (0.0121, 0.0629, 0.9235) in 15 iterations, minus log-likelihood 2623.8302 (2625.3778 at the truth, 2657.1722 at the start); 1,000 days (0.0430, 0.0602, 0.8663), persistence 0.9265; V_L 0.8885 %², 0.9426% a day, 14.96% a year; half-lives 34.31 (0.98) and 50.62 (0.9864); day 1,999 fitted 0.923% against a true 0.9649%.
- Fitted against true variance: correlation 0.9962 (of σ_t: 0.9969). The lessons quote the variance figure, as l5 does.
- Half-life at full precision (0.986421): 50.70 days. The lessons give 50.62 from the rounded 0.9864, as the brief and l9 do, and l8 states both.
- V_L arithmetic: 0.0121/(1 − 0.9864) = 0.8897, not 0.8885. The 0.8885 needs the unrounded fit, so l8 gives 6-place inputs (0.012065/0.013579) and teaches the rounding as sensitivity.
- ARCH path `simulate_arch1(5e-5, 0.5, 2000, 11)`: sample sd 0.010013 (population 0.01001); raw kurtosis 5.2945; seeds 11 to 30 mean 6.058 (median 4.976, range 4.121 to 13.621); r² ACF lags 1 to 10: 0.4246, 0.1376, 0.0505, 0.0069, 0.0351, 0.0954, 0.0456, 0.0085, −0.018, −0.0309; ARCH fit (β held at 0) ω̂ = 0.4867, α̂ = 0.5350; on B (0.7928, 0.2251).
- Explore paths, ω = (1 − α)·10⁻⁴, seed 11: sd 1.00, 1.01, 1.00 % and raw kurtosis 3.02, 3.74, 5.29 for α = 0, 0.3, 0.5.
- Trap loop (reads `r[t]` from `np.zeros`): sd 0.007084, raw kurtosis 3.0205, lag-1 r² ACF 0.0149.
- Storm days 1,454 to 1,459 (true model, 4-place returns): 3.2346, 3.0426, 4.6398, 6.8041, 7.4991, 7.4080 %²; scores ℓ: −5.3402, −5.1997, −3.1228.
- Log-likelihood profile in α (ω, β at the fit): −2687.57 at 0.040, −2623.83 at 0.063, −2641.00 at 0.080, −2650.62 at 0.085.
- Decimal fit from the same start: Pyodide (7.01e-5, 0.2461, 0.2756), log-likelihood in % terms −2800.14, "success". CPython (8.34e-5, 0.1694, 0.0827), also "success". Both are about 176 below the peak.
- Series A fit: Pyodide (1.0253, 0.0000, 0.0050), success True; CPython (1e-6, 0.0000, 1.0000), success False ("Inequality constraints incompatible"). Minus log-likelihoods 2868.779 and 2868.776, against 2868.779 for a constant variance. l7 teaches this as β not being identified once α̂ = 0.
- Unconstrained BFGS on B: (−905.6, −64.9, −494.3), log-likelihood `nan`, the same in both runtimes (l7 quiz).
- 20 paths, seeds 7 to 26: persistence mean 0.9778, sd 0.0079, range 0.9603 to 0.9867, 16 of 20 within one sd of 0.98; α̂ mean 0.0822 (sd 0.0118); β̂ mean 0.8955 (sd 0.0164); V_L 0.68 to 1.32 %²; long-run vol 13.10% to 18.25% a year, mean 15.74%, sd 1.33 points. Twenty fits take 3.0 s in Pyodide under Node, so no test does it.
- Variance targeting on B: ω = 0.0109, α̂ = 0.0658, β̂ = 0.9238, persistence 0.9897, half-life 66.8 days, long run 1.0585 %² (16.33% a year), minus log-likelihood 0.28 above the full fit's. First 1,000 days: (0.0592, 0.8667); seed 11: (0.0920, 0.8825).
- Black-Scholes, S = K = 100, r = 5%, T = 1: £10.4506 at 20%, £8.9136 at 15.87%, £8.5781 at 14.96%.
- Storm window days 1,380 to 1,479: sd 2.4305% a day, 38.58% a year.
- Homework: EWMA (λ = 0.94) against the fitted GARCH, one-step mean squared error against B's true variance from day 20: 0.06919 and 0.008506 (%²)²; λ = 0.90: 0.067523. Seed 11 fit (0.0251, 0.0933, 0.8825): persistence 0.9758, half-life 28.26, 16.14% a year. Share N, `simulate_garch(2e-7, 0.06, 0.939, 2000, 3)`, fits persistence 0.99967 in both runtimes, so it is refused. $0.995^{252} = 0.2834$; ln 0.5/ln 0.999 = 692.8.

## Deviations from the brief, stated honestly

- l6's α ≥ 1 edge case: a short simulation does not show an explosion. An ARCH(1) path stays strictly stationary up to α ≈ 3.56, and α = 1 or 1.2 paths look calm over 200 days. Only the expected variance grows. The screen therefore plots $E[\sigma^2_{t+h}]$ for α at 0, 0.5, 0.9, 1.1 and 1.3, and says that a single path can look calm.
- l6's "a 20-seed average is closer": it is closer, but only to 6.06 against 9, and the prose says so.
- l6's trap is a concrete version of the brief's: a simulation loop that reads `r[t]` (still 0) instead of `r[t − 1]`, which removes the clustering.
- `arch1_kurtosis` has its own code screen; the brief's three l6 functions are spread over two screens.
- l7's brief mentions "about 4 s in Pyodide" for the 20 fits. The histogram is precomputed (3.0 s measured), and no test fits more than 12 series.
- The homework `fit_and_report` has a third refusal rule, α̂ < 0.01, because the two SciPy builds disagree on whether series A's fit converged. The rule refuses A on both.
- The homework has 9 items, and `forecast_mse` is the brief's "EWMA against GARCH one-step forecasts" item.

## Conventions

- Data: `r, s2 = simulate_garch(2e-6, 0.08, 0.90, 2000, 7)`, the brief's function verbatim in every code prelude, with `rp = 100 * r`, `s2p = 1e4 * s2` and `iid` (series A, seed 8) as in l5. `garch_variance`, `neg_loglik` and the reference `fit_garch` are verbatim where loaded. ARCH path `simulate_arch1(5e-5, 0.5, 2000, 11)`, started at ω/(1 − α). `params` is the fit to full precision, as in l9.
- Returns in % in every model screen. Fitted parameters are tested to 3 places within 0.003, plus interval checks. Recursions, likelihoods and closed forms are tested exactly (9 places, or 6 for derived values).
- Every `how` that imports SciPy says "a few seconds". No level 2 screen imports statsmodels.

## Load times

Measured under Node with the local wheels: NumPy, OpenBLAS and SciPy load in 3.8 to 5.8 s from cold. One fit takes about 0.15 s, and 20 fits take 3.0 s. In the browser each lesson played in 30 to 35 s, and homework-2 (which has 12 fits in one check) in 16.5 s.

## course.json

No change needed. Each lesson's first objective is the course.json objective, word for word.

## Engine and canvas limitations

Five bullets in `docs/BACKLOG-INBOX.md` under "Raised later (garch level 2):". Two are votes for level 3's bullets: the plane x-axis title, and set playthroughs under a concurrent run.

Scratch files: `/tmp/claude-0/-home-user-zero-to-quant/3e0ee4d9-5633-56bc-b89e-00d7263b2d42/scratchpad/garch-2/`: `common.py`, `build_l6.py`, `build_l7.py`, `build_l8.py`, `build_sets.py`, `facts*.py` (with `py_*.py` copies for Pyodide), `pyrun.mjs`, `harness.py`, `voice.py`, `shots/`, `why/` and `final/`.
