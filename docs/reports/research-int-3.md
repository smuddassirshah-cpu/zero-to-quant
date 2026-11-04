# research-int level 3 report: The open case

Author: content agent, 4 November 2026. Brief: `docs/briefs/research-int.md` `## Level 3` plus its shared sections. Files in `app/content/courses/research-int/`. `course.json`, the data files, the engine and other levels are untouched. The six data files in `app/content/data/` were only read.

## Files

| File | Screens | Quiz / items | Canvases and widgets | Notes |
| --- | --- | --- | --- | --- |
| `l11-framing-the-question.json` | 10 | 4 | `series` of the futures close; `bars` of horizon spread (21-day bar hidden until the answer); `table`; `scatter` of today's against tomorrow's close; `series` of 100, 110, 99; `bars` of gross edge, cost, net; widgets `choice`, `code` (with `data`), `numeric`, `table`, `order` with distractor | hook, code (`framing`), horizon ladder, three scores, trap (R² 0.994), edge (percentages do not add), generalise, derive ($\sigma\sqrt{h}$), transfer (profit after costs), "The follow-up" |
| `l12-features-and-data.json` | 10 | 4 | `table` canvas with `tap: "rows"`, `table`, `bars` of correlations, `series` with `hlines`; `tap-regions`, `table`, `code`, `multi`, `choice`, `numeric`, `order` | hook (tap the leaking rows), rolling then shifted, code (`feature_corrs`), vendor `multi`, trap, edge (statistics from the future), generalise, derive ($1/\sqrt{3}$), transfer (four vendor fields), "The follow-up" (`order` with distractor) |
| `l13-baseline-first.json` | 11 | 4 | `bars` (three forecasts, three test errors, futures errors); `numeric`, two `code` screens (spread, futures), `choice`, `order` | hook (persistence error, $\varphi = 0.9$), code, gain ladder, code, out-of-sample R², trap (ship it), edge (baseline that saw the test days), generalise, derive ($2\sigma^2/(1+\varphi)$), transfer (desk spread, $\varphi = 0.95$), "The follow-up" |
| `l14-house-price-case.json` | 11 | 4 | `table` of eight raw rows with a tap on cells; `table` of coefficients with standard errors; `scatter` of all 400 rows (grouped by units); `bars` of band premiums; four `code` screens with a shared hidden `prelude` | hook (tap the four cells), six ladder screens (baseline, area only, all features, forest and log model, bedrooms coefficient, the four prices), trap, edge (peeking at the test set), transfer (rents by postcode), "The follow-up" |
| `l15-presenting-a-result.json` | 10 | 4 | `bars` histogram of 5,000 bootstrap RMSEs with `cut`; `bars` of two RMSEs; `choice`, `numeric`, `order` with distractor, `multi` | hook, half-width, out-of-sample R², report skeleton, trap (point estimate only), edge (four times the rows), generalise, derive (bootstrap steps), transfer (spread model report), "The follow-up" (`multi`) |
| `review-3.json` | | 10 items, difficulty 2 to 4 | untimed; E11 `parts` on `r3-parts-baseline` | every item has `skills`, `tags`, `pace` |
| `homework-3.json` | | 8 items, difficulty 3 to 5, three at 5 | E11 `parts` (first item), `order` derivation, three `code` items (all with `data`), `longform` with a 10-point rubric and model answer, two `numeric` | every item has `skills`, `tags`, `pace` |

Every lesson has `minutes: 15`, the objective from `course.json`, one `trap` with a `byKey` line naming the blurt, one edge case, a "Say it aloud" screen (`generalise` with a `choice` over spoken answers), a `derive` screen with a distractor line, a quant `transfer`, and a closing `ladder` titled "The follow-up". The first prose of each lesson states the pace; l14 also says "about 50 minutes with the code screens". Skills: `rq-case` on l11, l12, l14, l15 and `rq-case` with `rq-ml` on l13 (and on the l13 review and homework items).

### Tags and pace

Families used: `target-horizon-loss`, `price-vs-return` (l11); `feature-leakage`, `shift-rolling` (l12); `baseline-first`, `persistence-baseline` (l13); `house-price-case`, `collinear-features` (l14); `report-uncertainty`, `bootstrap-interval` (l15); `leakage-window` on H3.7 as the brief says.

| File | Paced screens (sum) | Quiz (sum) |
| --- | --- | --- |
| l11 | 10: 9 at 180 s and 1 code at 600 s (2,220 s) | 4 at 180 s (720 s) |
| l12 | 10: 9 at 150 s and 1 code at 600 s (1,950 s) | 4 at 150 s (600 s) |
| l13 | 11: 9 at 150 s and 2 code at 600 s (2,550 s) | 4 at 150 s (600 s) |
| l14 | 11: 240 s for non-code, code screens 300, 300, 420, 420 s (3,120 s) | 4 at 240 s (960 s) |
| l15 | 10 at 180 s (1,800 s) | 4 at 180 s (720 s) |
| review-3 | 10 items, 1,410 s (untimed, pace shown) | |
| homework-3 | 3,630 s: parts 420, order 240, code 600, code 600, code 900, longform 600, numeric 150, numeric 120 | |

### E3 example draw (for the exam author; no level file holds a `draw`)

- `{ "from": "bank/research-3", "tags": ["target-horizon-loss", "baseline-first"], "difficulty": [2, 4], "n": 3 }`

## Validator, voice, playthrough

- `node tools/validate.mjs`: **0 errors** (451 warnings in all; none are errors). Warnings in this level's files: code screens and ladders without a canvas, a "point hint usually highlights the canvas" on five screens, and "a ladder screen usually reuses the previous canvas kind" on two follow-ups. The brief requires the closing screen to be a ladder.
- Voice: `VOICE_BASE=<abs>/app/content/courses/research-int python3 docs/reviews/voice-scan.py`: **0 sentences over 20 words, 0 explanations over three sentences**, also for `how` lines and model answers. No `!`, no em-dash, no emoji. Choice keys: no key is more than 8% longer than the longest distractor (checked by script in the builder; 70 options rebalanced).
- Playthrough with `--local-cdn <scratchpad>/pkgs`, five lessons and both sets, desktop and `--mobile` (390 px): **all passed**.

| Lesson or set | Desktop | 390 px |
| --- | --- | --- |
| l11-framing-the-question | 14 checks, quiz 4/4 | 14 checks, quiz 4/4 |
| l12-features-and-data | 14 checks, quiz 4/4 | 14 checks, quiz 4/4 |
| l13-baseline-first | 15 checks, quiz 4/4 | 15 checks, quiz 4/4 |
| l14-house-price-case | 15 checks, quiz 4/4 | 15 checks, quiz 4/4 |
| l15-presenting-a-result | 14 checks, quiz 4/4 | 14 checks, quiz 4/4 |
| review-3 | 12 items, 10 of 10 recorded | same |
| homework-3 | 11 items, 8 of 8 right, 39 of 39 marks; parts check passes | same |

Screenshots (desktop and 390 px, every lesson screen, review and homework items) were looked at. Fixed from them: the l14 hook table was wider than a phone and clipped the mistyped price (the `id` column went, headers shortened); a dash used for a blank age (an em-dash) became the word "blank"; the l13 hook prose read badly and was rewritten. One real fault came from the run itself: a `numeric` with `unit: "%"` compares fractions, so the playthrough typed 5800 for a key written as 58.0 (every `%` numeric is now scaled by 0.01; see the backlog).

### Code in Pyodide

Every `code` widget (eleven: l11 1, l12 1, l13 2, l14 4, homework 3) was run in Pyodide 0.27.7 (numpy 2.0.2, pandas 2.2.3, scikit-learn 1.6.1, statsmodels 0.14.4) under Node with `docs/briefs/research-int-scripts/l3_codecheck.mjs`: the model solution passes every hidden test and example, and the untouched starter fails them (the only passes are the "input frame unchanged" test of H3.2, 1 of 8, and nothing else). The playthrough also runs each solution in the app's worker. The two timings that matter: the l14 forest screen takes about 1.2 s in the check harness.

| Widget | Solution | Starter passes |
| --- | --- | --- |
| l11 `framing` | 5 of 5 | 0 of 5 |
| l12 `feature_corrs` | 5 of 5 | 0 of 5 |
| l13 `baseline_scores` and `futures_baselines` | 4 of 4 and 4 of 4 | 0 and 0 |
| l14 `baseline_rmse`, `area_only_rmse`, `fit_all`, `forest_rmse` with `log_rmse` | 3, 3, 4, 3 of the same | 0, 0, 0, 0 |
| H3.2 `add_features`, H3.3 `baseline_mses`, H3.5 `fit_log_houses` | 8 of 8, 4 of 4, 3 of 3 | 1 of 8, 0, 0 |

## Numbers, with sources

Every number was computed twice. Brief numbers: `l3_open_case.py` (re-run in Pyodide: 49 pairs, ALL AGREE). Mine: `l3_aux.py` and `l3_aux2.py` in `docs/briefs/research-int-scripts/` (method A hand formula, pure Python, `fractions` or normal equations; method B pandas, statsmodels or scikit-learn; 136 and 24 pairs, ALL AGREE, run in Pyodide). Review and homework items with plain formulas are asserted twice (fractions against floats) in the builder, which is in my scratchpad folder only; the values are repeated here.

**l11.** On `futures-daily.csv`: R² of close on previous close 0.994395, of return on previous return 0.015253 (slope 0.1235, $t$ 3.928), miss of "tomorrow equals today" 57.7804 points on a mean close of 5,561.88, root mean square return 0.010374 (l3_open_case; aux). Spread by horizon with 1% daily: 5 days 2.236, 21 days 4.583, 252 days 15.875 (aux, formula against the square root of a summed variance). Loss example: MSE 0.1267, hit rate 1/3, profit +0.2% (both methods). Log returns of +10% and −10%: $\ln 1.1 + \ln 0.9 = \ln 0.99 = -1.005\%$. Transfer: 52% right on 8 bp with 0.5 bp cost: $0.32 - 0.5 = -0.18$ bp. Tiny test file (200, 204, 202, 207, 205, 210, 208, 213): 0.2485294118, 0.9908097898, 3.8359204520, 0.0185851398 (aux, A and B).
Quiz: 30-day spread of 0.7% daily 3.834% (aux); forecasts 0.4, 0.2, −0.3 against 0.1, −0.2, −0.1: profit 0, hit rate 2/3 (aux); 100, 102, 101: 0.995% (aux); 55 against 58 points: 5.17% (hand).

**l12.** On the 994 common rows: 0.126083, 0.028533, 0.030337, 0.608603 (l3_open_case; aux A pure Python against B pandas). Mini series 1.0, −0.5, 0.2, 0.8, −0.3, 0.4: rolling mean on day 6 0.3, shifted 0.2333, first shifted day 4. Centred three-day mean against its label: $1/\sqrt{3} = 0.57735$ (simulation of 2,000,000 draws agrees to 0.0015; `1/sqrt(2)` and `1/sqrt(5)` likewise). Edge: 6 − mean(2, 4, 6) = 2, against 6 − 8 = −2. Twelve-row test file: 0.7981286388 for the centred mean on 6 rows (aux). Quiz: shifted two-day mean 0.2 (unshifted 0.45); $1/\sqrt{2} = 0.7071$.

**l13.** Spread, first 400 rows to fit and all 200 later rows tested: persistence 1.207112, mean 6.819594, AR(1) 1.153271 (params 3.8129, 0.9246); gain 4.46%; without the first test row 1.2128 and 1.1574 (aux2, A and B); fitted on all 600 rows the AR(1) scores 1.1518. Population: $2/(1+\varphi)$ equals $2(1-\varphi)/(1-\varphi^2)$ and $(1-\varphi)^2/(1-\varphi^2) + 1$ for $\varphi$ = 0.9, 0.8, 0.7, 0.6, 0.95 (aux; 1.0526, 1.1111, 1.1765, 1.25, 1.0256); gain of the AR(1) $(1-\varphi)/2$: 5, 10, 15, 20, 2.5%. Futures, 749 to fit and 250 to test (×10⁻⁴): zero 1.0135, mean 1.0167, AR(1) 1.0227, slope 0.1458, out-of-sample R² −0.00907, in-sample $t$ 4.024, $R^2$ 0.0212 (aux, polyfit against statsmodels). With 500 to fit: 1.0272, 1.0274, 1.0322. Quiz: $1/(1-0.49) = 1.9608$, 5% gain.

**l14.** `houses.csv`: 400 rows, 20 blank ages, 4 prices above 5,000, 396 clean, median age 42, 297 train and 99 test (`train_test_split(test_size=0.25, random_state=0)`). Baseline RMSE 85.0489, area only 46.8608, all features 29.6582 (a 65.1% cut), forest 40.4417, log model 32.9514; coefficients 2.6745, 6.6594, −0.7510, −5.0826, 17.6867, −26.405, −39.6218, −53.9074, intercept 115.775 (normal equations against `LinearRegression` and statsmodels to 1e-7). Standard errors 8.19, 0.10, 2.39, 0.06, 0.62, 3.29, 5.24, 5.25, 5.43 (aux2, normal equations against statsmodels). Bedrooms: $(9 - 6.6594)/2.393 = 0.978$; area and bedrooms correlation 0.7638, VIF 2.4002, root 1.5493. Area-only slope 2.8078 on 396 clean rows against 71.6999 on all 400 (ratio 25.5). Forest leaf sizes 1, 3, 5, 10: 40.5988, 40.4417, 41.5049, 43.8436 (aux2; `forest.predict` against the mean of the trees). Postcode difference: $120\sqrt{1/4 + 1/4} = 84.85$. Quiz: 650 − 5 = 645; $1 - (16.4/41.0)^2 = 0.84$; $\sqrt{1/(1-0.81)} = 2.294$.

**l15.** Test RMSE 29.6582 and 5,000 bootstrap resamples (`default_rng(99).integers(0, 99, (5000, 99))`): 2.5th and 97.5th percentiles 24.8738 and 34.2232 (a pure-Python sort of the same values gives 24.8743 and 34.2368, which is within a rank step); width 9.35, half-width 4.675; 4 times the rows halves it. Out-of-sample R² 0.8784 from the RMSE ratio and from the errors; per-row squared-error gain over the baseline 6,353.7, 95% interval 4,486.9 to 8,445.0, paired $t$ 6.28. Spread model gain per day 0.0538, $t$ 1.865, bootstrap interval −0.0019 to 0.1113 (seed 99). Quiz: $\sqrt{256/64} = 2$, $1 - (28/40)^2 = 0.51$.

**Review and homework** (fresh numbers; all asserted twice): R3.1 errors 0.2, 0.3, −0.1, −0.2: 0.045; R3.3 $0.8\sqrt{10} = 2.5298$; R3.5 mean of days 2 to 5 of 0.6, −0.3, 0.5, 0.2, 0.7, −0.4 is 0.275 (unshifted 0.25); R3.6 $2/1.65 = 1.2121$ (mean forecast 1.7316); R3.7 $1 - 3.19/3.10 = -0.0290$, $0.95 \times 3.10 = 2.945$; R3.8 $1 - 24.9/62.4 = 60.1\%$; R3.9 $\sqrt{1/(1-0.5625)} = 1.5119$; H3.4 530 rows, $1 - 131/312 = 58.0\%$, R² 0.8237, $(35-21)/14 = 1$, VIF 3.05; H3.6 $1 - (212/498)^2 = 0.8188$, cut 57.4%; H3.7 $1/\sqrt{5} = 0.4472$; H3.8 $2/1.8 = 1.1111$. Code values: H3.2 `mean10` row 25 0.0010172140, `vol_rel` row 100 0.3826938053, `y` row 500 0.0085630247, `ret` row 1 0.0021417192, 980 complete rows (hand mean against pandas rolling to 1e-12); H3.3 (350 to fit, 250 to test) 1.1942044, 7.4129795, 1.1482173; H3.5 RMSE 28.76694, garden 7.2518% (log-price normal equations against `LinearRegression`).

## Departures from the brief

- **Fresh numbers.** DECISIONS "Fresh numbers in reviews and homework" overrules the brief where it repeats a lesson: R3.1 (four forecasts), R3.2 (R² 0.981), R3.3 (ten days at 0.8%), R3.4 (other features), R3.5 (four-day mean), R3.6 ($\varphi$ 0.65), R3.7, R3.8 (62.4 and 24.9), R3.9 (correlation 0.75), R3.10 (12.4, 10.0 to 14.8, 31.0), H3.1 (gold futures), H3.2 (`mean10` and `vol_rel` in place of `mean5`), H3.3 (350 and 250 in place of 400 and 200), H3.4, H3.5, H3.7 (a five-day mean). The lesson quizzes also take fresh numbers.
- **R3.7 and H3.4** cannot ask a learner to recompute futures or house numbers without code, so R3.7 gives the three errors (3.10, 3.12, 3.19) and asks for out-of-sample R², the verdict and the 5% target; H3.4 is a rental case (530 flats, 24 blank areas, 6 rents in pence) with the same four steps (rows kept, cut, R², why the coefficient is below the expected). H3.6 supplies its numbers (a rental result) so it tests reporting, not recall.
- **H3.5** models the log of the price with an 80/20 split (`random_state=1`) and returns the RMSE and the garden effect in per cent, since the brief's linear RMSE 29.66 and bedrooms 6.66 are the lesson's.
- **l12 hook** shows a "Built from" column, not a "known at the close" column, so the answer is not on the table.
- **l13 hook** is numeric with the long-run variance given in the prose, so the learner derives the persistence error rather than looking it up; the edge screen is a `choice` with 1.1518 against 1.1533.
- **l14 hook** taps the four cells that need attention (three blank ages and one price in pounds) instead of asking for 396; the 396 appears in the first ladder screen. Four of the six ladder screens are code screens (baseline, area only, all features, forest and log model); the bedrooms and four-prices screens are numeric with a coefficient table and a scatter of all 400 rows.
- **l11** has one code screen returning four numbers (`framing`) rather than separate code for each worked number.
- **l15 transfer** reports the l13 spread model with a paired bootstrap on the 200 test days; the interval just touches zero, so the supportable sentence is "unproven". The brief's hook interval numbers are used (24.87 to 34.22 on 5,000 resamples at seed 99).
- **l14 explanation of the bedrooms coefficient** says collinearity widens the error and does not bias the estimate (brief); the full-model VIF 2.43 is not quoted on a screen, only the two-variable 2.40.
- **E3**: nothing authored; the example draw is above.

## Coincidences with other items

A scan of every numeric key in `app/content/` against this level's keys (`dups.py`, scratchpad) found three equal keys with unrelated stems: 0.7071 (l12 quiz, $1/\sqrt{2}$, a constant that also keys items in `ito`, `puzzles` and `mental-pressure`), 0.3333 (l11, the brief's hit rate 1/3) and 0.275 (R3.5, against `trees`, `stat-learning` and `analysis` items with different numbers). No stem repeats another item's numbers. Earlier collisions (1.25, 2.28, 520, 0.4375, 0.225, 0.325, 1.6667) were changed.

## Proposed `course.json` change

None.
