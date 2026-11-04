# Answer check, research-int level 3, 4 November 2026

**Summary.** 89 items checked: L11 14 (10 screens, 4 quiz), L12 14, L13 15, L14 15, L15 14, review-3 10 (one with 3 parts), homework-3 7 (one with 4 parts, one longform). 11 code widgets run against their hidden tests. Wrong keys: 0. Other mismatches: 2 distractor values that do not match their feedback, 2 wording or number claims, 1 duplicate, 1 grammar slip, 3 voice and key-length notes, plus notes.

Every keyed answer, `wrong` value, tolerance, table cell, canvas figure and quoted statistic was recomputed in Python before I read any explanation or `docs/reports/research-int-3.md`. Scripts are in `/tmp/claude-0/-home-user-zero-to-quant/024bfe09-7a97-56c3-837c-b47a15727adf/scratchpad/answers-research-3/`:

- `c1.py` (futures and spread files, lessons 11 to 13, bootstrap spot checks), `c2.py` (houses file, lesson 14 and 15), `c3.py` (homework and review arithmetic).
- `harness.py` runs every code widget's solution and starter against its tests, with the `prelude`, `setup`, `isclose` tolerances and `equal` compare. Solutions pass 6/6, 6/6, 5/5, 5/5, 4/4, 4/4, 5/5, 4/4, 9/9, 5/5, 4/4. Starters pass 0 tests, except `h3-features-code`, which passes only the input-unchanged test (as its `how` says).
- `dups.py` scores every review and homework item against 18,754 course, exam and bank items. `voice.py` and `lens.py` check voice and choice key lengths.

**Library versions.** I installed pandas 2.2.3 and scikit-learn 1.6.1, the Pyodide versions, with statsmodels 0.15.0 and numpy 2.5.4 (Pyodide 0.27.7 ships numpy 2.0.x). Every code figure, including the random forest at `random_state=0` and `train_test_split(random_state=0 or 1)`, matched to the stored digits. No tolerance sits close to a difference between those numpy versions. The one exception: the bootstrap numbers (see note 2).

## Mismatches

### Wrong keys

None.

### Distractor value does not match its feedback line (key right)

| Path | Item | Stored | Described slip gives | Working |
|---|---|---|---|---|
| `l11-framing-the-question.json` | quiz `q-hit-rate`, wrong `hit` | 0.006667 | 0.6667 | The hit rate is 2/3 = 66.7%, and `unit: "%"` stores the fraction, so a learner typing 66.7 stores 0.667. 0.006667 would be typing 0.6667 into the % box |
| `l14-house-price-case.json` | screen 9 (Rents by postcode), wrong `sum` | 169.7 | 120 | Feedback says "You added the errors". 60 + 60 = 120, which is also the `sd` value. 169.7 is $\sqrt{120^2 + 120^2}$, the slip of using the single-rent sd for both means |

### Wording or number claims that are wrong

| Path | Item | Stored text | Recomputed |
|---|---|---|---|
| `l14-house-price-case.json` | screen 2 feedback.correct | "area alone more than halves the baseline error" | 46.86 / 85.05 = 0.551, so the error falls 44.9%. It does not more than halve |
| `l11-framing-the-question.json` | screen 5 hint (step) | "Their sum is $-0.0100$" | 0.0953 - 0.1054 = -0.0101 to four places; $\ln 0.99 = -0.01005$. Say "$-0.0101$" |
| `homework-3.json` | `h3-baselines-code` explain | "a 3.8% gain over the best baseline" | 1 - 1.1482173 / 1.1942044 = 0.038509, which rounds to 3.9% |

### Duplicates and fresh numbers

| Path | Item | Problem |
|---|---|---|
| `review-3.json` | `r3-report-sentence` | Uses a test RMSE of 12.4 against a baseline of 31.0. `l15-presenting-a-result.json` quiz `q-first-sentence` uses £12.4k against £31.0k. Give the review item new numbers (and the 10.0 to 14.8 interval with them) |

No review or homework item repeats a lesson's numbers otherwise. Grep and `dups.py` over `app/content/` found no item in another course, exam, drill or bank file that shares a question's numbers: the only hits were isolated value coincidences (0.4472, 1.1111, 2.945, 7.25, 0.8237 in unrelated contexts).

### Grammar

| Path | Item | Stored | Fix |
|---|---|---|---|
| `l15-presenting-a-result.json` | screen 9 option `period` | "The test rows come from a different period than use" | "...than the period of use" |

### Voice and key lengths

- No em-dashes, no exclamation marks, no US spellings in prose (`center=True` is code).
- Sentences of 20 words (the limit is under 20): `l11` screen 3 explain ("The same three forecasts look poor by hit rate and fair by profit, because day 1 was large and right."), `l11` screen 9 prose, `l13` screen 1 hints 0 and 2 (22 words), `l13` summary idea 3 and trap, `l14` screen 5 prose (21) and screen 10 prose (22), `l15` screen 9 explain, `homework-3` `h3-features-code` explain (23) and the longform `model` second paragraph (23, model text only).
- Choice key visibly longest: `l15` screen 8 (58 against 43, 57, 39), `l11` screen 9 (70 against 67, 50, 40), `l11` screen 4 (71 against 68, 48, 47), `review-3` `r3-report-sentence` (70 against 44, 65, 52). Trim the key or lengthen the short distractors.
- Explanations: none has more than three sentences.

## Notes (no change required, fixer's call)

1. `review-3` `r3-vif-08` has an id that says 08 but uses a correlation of 0.75. Cosmetic.
2. The bootstrap figures in L15 cannot be reproduced exactly from a seed. I re-ran 5,000 resamples: the percentile interval of the stored histogram data is exactly 24.87 to 34.22 (matches). The per-row gain interval I get is 4,465 to 8,453 (stored 4,487 to 8,445), and the spread gain interval is -0.0006 to 0.108 (stored -0.002 to 0.111). Both are worded "about" and the conclusions (excludes zero; touches zero) hold for every seed I tried.
3. `review-3` `r3-price-r2` is the same lesson as `l11` screen 4, with the same answer text ("Only that prices persist"), and `r3-leaks` option `z-year` restates `l12` quiz `q-zscore-fix`. Numbers differ, so this passes the numbers rule, but the answers repeat in kind.
4. `r3-mse-four` wrong `hit` is 1.0, which catches only the fraction; a learner typing 100 is not matched. Its feedback lists errors as forecast minus actual (0.2, 0.3, -0.1, -0.2), the reverse of "actual minus forecast" in `l11`'s hints. The squares are the same.
5. `l12` quiz `q-shifted-two` has the answer 0.2, which equals the day 5 return. Harmless, but a learner reading the wrong row gets it right.
6. `l12` screen 9 line d, "a score above zero means the pipeline leaks", is loose: a shuffled label gives a score near zero, not exactly zero. "Clearly above zero" would be safer.
7. `l13` screen 5 claim "room for a true coefficient of 0.06" is consistent: out-of-sample R² of about 0.0036 is well inside a standard error of 0.0201 (my bootstrap).

## Per item

### L11 Framing an open question (`l11-framing-the-question.json`)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| screen 0 target | choice `ret` | Level, direction and average distractors all wrong; key length 52 against 52, 49, 51 | OK |
| screen 1 `framing` code | R² 0.9943951, 0.0152529, rmse 57.780408, 0.01037423; tiny file list | Futures file: 0.994395, 0.015253, 57.7804, 0.0103742. Tiny: 0.24853, 0.99081, 3.83592, 0.018585. Solution 6/6, starter 0/6 | OK |
| screen 2 21 days | 4.583 (0.04583) | $\sqrt{21} = 4.5826$; linear 0.21, daily 0.01, five 0.02236; bars 2.236 and 15.875 right | OK |
| screen 3 table | 0.1267, 0.3333, 0.2 | errors 0.3, 0.2, -0.5 give 0.38/3 = 0.12667; one hit in three; 0.5 - 0.1 - 0.2 = 0.2 | OK |
| screen 4 high R² | choice `persist` | R² 0.994395 on 999 pairs; return R² 0.01525; distractors wrong | OK |
| screen 5 two-day log | -1.005% (-0.01005) | ln 1.1 + ln 0.9 = ln 0.99 = -0.0100503; flip 0.01005 right | OK, hint to fix |
| screen 6 opening | choice `good` | names target, horizon, loss, baseline; 81 against 79, 69, 52 | OK |
| screen 7 order | a, b, c, d; x out | variance of sum is $h\sigma^2$, root $\sigma\sqrt{h}$ | OK |
| screen 8 profit | -0.18 bp | 0.52 x 8 - 0.48 x 8 = 0.32; minus 0.5 = -0.18; mixed 0.52 - 0.5 = 0.02 | OK |
| screen 9 horizon | choice `close` | text only; bar values 4.583, 15.875 right | OK |
| quiz `q-thirty-days` | 3.834% | 0.7 x $\sqrt{30}$ = 3.8341; linear 21%, daily 0.7% | OK |
| quiz `q-baseline-miss` | choice `small` | 3/58 = 5.17%; 55 / 5,500 = 1% | OK |
| quiz `q-hit-rate` | 0 | +0.1 - 0.2 + 0.1 = 0; hit rate 2/3; sizes 0.4% = 0.004 | wrong `hit` mismatch (1) |
| quiz `q-two-day-log` | 0.995% | ln(1.01) = 0.0099503; simple 1%; first day ln(1.02) = 1.980% | OK |

### L12 Features and data (`l12-features-and-data.json`)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| screen 0 tap | r0, r1, r2 | centred mean, tomorrow's gap, whole-sample z-score use later data; today's return and volume safe | OK |
| screen 1 table | 0.3, 0.2333, 4 | (0.8 - 0.3 + 0.4)/3 = 0.3; (0.2 + 0.8 - 0.3)/3 = 0.2333; first rolling value day 3, shifted day 4 | OK |
| screen 2 `feature_corrs` | 0.126083, 0.0285335, 0.0303372, 0.6086035; tiny list | 0.126083, 0.028533, 0.030337, 0.608603 on 994 rows; tiny -0.82307, -0.44115, -0.52917, 0.79813. Solution 6/6, starter 0/6 | OK |
| screen 3 multi | restate, members, stamp, fill | four leak; `yvol` and `today` known at the decision | OK |
| screen 4 0.609 | choice `leak` | 0.609² = 0.370 (stated 0.37); bars 0.126, 0.029, 0.03, 0.609 | OK |
| screen 5 so-far mean | 2 | mean 2, 4, 6 = 4; 6 - 4 = 2; full mean 8 gives -2 | OK |
| screen 6 test sentence | choice `time` | text only; 73 against 68, 63, 62 | OK |
| screen 7 order | a, b, c, d | Cov = $\sigma^2/3$, Var(m) = $\sigma^2/3$, corr = $1/\sqrt{3}$ = 0.5774 | OK |
| screen 8 vendor field | choice `close` | 16:31 before 16:35; others after or misstamped | OK |
| screen 9 order | a, b, c, d | method order sound (note 6) | OK |
| quiz `q-safe-average` | choice `trail` | trailing window ends today | OK |
| quiz `q-shifted-two` | 0.2 | days 3 and 4: (-0.3 + 0.7)/2 = 0.2; unshifted (0.7 + 0.2)/2 = 0.45 | OK |
| quiz `q-half-label` | 0.7071 | $1/\sqrt{2}$; half 0.5; quarter 0.3536 is 0.7071/2 | OK |
| quiz `q-zscore-fix` | choice `expand` | statistics from days up to today | OK |

### L13 Baseline first (`l13-baseline-first.json`)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| screen 0 persistence | 1.0526 | $2/1.9$ = 1.05263; long-run variance 1/0.19 = 5.263; hint 0.01 x 5.263 + 1 | OK |
| screen 1 `baseline_scores` | 1.207112, 6.8195945, 1.1532709; tiny 0.45333, 0.15556, 0.13725 | 1.207112, 6.819594, 1.153271; tiny matches; leaving the first row out gives 1.2128 and 1.1574 (stated). Solution 5/5, starter 0/5 | OK |
| screen 2 gain | 4.46% (0.0446) | 1 - 1.1533/1.2071 = 0.04457; diff 0.0538 stored as 0.000538; ratio 0.9554 | OK |
| screen 3 `futures_baselines` | 1.0135, 1.016667, 1.022689; n_fit 500: 1.02721, 1.027422, 1.032173 | 1.013500, 1.016667, 1.022689; 1.027210, 1.027422, 1.032173; slope 0.14582. Solution 5/5, starter 0/5 | OK |
| screen 4 oos R² | -0.0091 | 1 - 1.0227/1.0135 = -0.009066; in-sample t = 4.024 on 748 pairs; standard error about 0.020 | OK |
| screen 5 ship it | choice `notshown` | text only; 62 against 60, 58, 40 | OK |
| screen 6 leaked fit | choice `seen` | fit on all 600 gives 1.15183 (stated 1.1518) against 1.1533 | OK |
| screen 7 say it | choice `base` | text only | OK |
| screen 8 order | a, b, c, d | $(1-\varphi)^2/(1-\varphi^2) = (1-\varphi)/(1+\varphi)$; total $2\sigma^2/(1+\varphi)$ | OK |
| screen 9 desk | 2.5% | 2/1.95 = 1.02564; 1 - 1/1.02564 = 0.025; onemphi 0.05; ratio 0.975 | OK |
| screen 10 margin | choice `margin` | text only | OK |
| quiz `q-mean-forecast` | 1.9608 | 1/(1 - 0.49) = 1.96078; persist 2/1.7 = 1.1765 | OK |
| quiz `q-return-baseline` | choice `zero` | 39 against 41, 30, 22, ratio 1.4 to the mean distractor | OK, note on length |
| quiz `q-gain-five` | 5% | 1 - 3.8/4 = 0.05; diff 0.2 stored as 0.002; ratio 0.95 | OK |
| quiz `q-baseline-mean` | choice `seen` | text only | OK |

### L14 House price case (`l14-house-price-case.json`)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| screen 0 tap | r3c2, r4c2, r6c2, r5c6 | those cells are blank age, blank age, blank age and 319200; the file has 20 blank ages and 4 prices above 5,000 | OK |
| screen 1 `baseline_rmse` | 85.0489 | 85.04887; above the test-mean RMSE; rounds to 85.05; 396 rows, 297 and 99. Solution 4/4, starter 0/4 | OK |
| screen 2 `area_only_rmse` | 46.8608 | 46.86080; rounds 46.9; between 40 and 50. Solution 4/4, starter 0/4 | OK, wording claim (4) |
| screen 3 `fit_all` | 29.6582; coefficients 6.6594, 17.6867, -26.405 | 29.65823; 6.6594, 17.6867, -26.405; also area 2.67, age -0.75, distance -5.08, B, C, D -26.40, -39.62, -53.91; cut 65.1%. Solution 5/5, starter 0/5 | OK |
| screen 4 forest and log | 40.4417, 32.9514 | 40.44171, 32.95140; 33.0 to one place. Solution 4/4, starter 0/4 | OK |
| screen 5 standard errors | 0.98 | (9 - 6.66)/2.39 = 0.979; gap 2.34; se 2.39; t 2.787; table from statsmodels on the training rows; area and bedrooms correlate 0.7638 on the training rows, VIF 2.40, root 1.549 | OK |
| screen 6 slope ratio | 25.5 | slopes 71.700 and 2.8078; ratio 25.54 (tolerance 0.3); gap 68.89 | OK |
| screen 7 fix prices | choice `fix` | key 53 against 51, 52, 38 | OK |
| screen 8 peeking | choice `tuned` | leaf scores 40.60, 40.44, 41.50, 43.84 | OK |
| screen 9 postcode | 84.85 | $\sqrt{60^2 + 60^2}$ = 84.85; gap 90/84.85 = 1.06 | wrong `sum` mismatch (2) |
| screen 10 drift | choice `drift` | bars -26.4, -39.6, -53.9 | OK |
| quiz `q-rows` | 645 | 650 - 5 = 645; both 615; all 650 | OK |
| quiz `q-r2-from-rmse` | 0.84 | 1 - (16.4/41)² = 0.84; cut 0.6; ratio 0.16 | OK |
| quiz `q-inflation` | 2.294 | $\sqrt{1/0.19}$ = 2.2942; VIF 5.263 | OK |
| quiz `q-dummies` | choice `collinear` | 67 against 43, 64, 64 | OK |

### L15 Presenting a result (`l15-presenting-a-result.json`)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| screen 0 interval | choice `wide` | stored 5,000 resamples: 2.5th and 97.5th percentiles 24.8695 and 34.2205; mean of resamples 29.56 | OK |
| screen 1 half-width | 4.675 | (34.22 - 24.87)/2 = 4.675; width 9.35 | OK |
| screen 2 oos R² | 0.8784 | 1 - (29.66/85.05)² = 0.87838; cut 0.6513; left 0.1216; per-row gain 6,353.7 exact; interval see note 2 | OK |
| screen 3 order | a, b, c, d, e | 29.7, 85.1, cut 65% "about two thirds" | OK |
| screen 4 missing | choice `interval` | text only | OK |
| screen 5 more rows | 4.675 | 9.35 / $\sqrt{4}$ = 4.675; quarter 2.34 | OK |
| screen 6 result sentence | choice `good` | numbers 29.7, 25 to 34, 85.1 agree | OK |
| screen 7 order | a, b, c, d | percentile bootstrap | OK |
| screen 8 spread report | choice `unproven` | gain 4.46%; t = 1.865 on 200 days; interval see note 2 | OK |
| screen 9 multi | period, band, tuned | three correct | OK, grammar (6) |
| quiz `q-say-interval` | choice `range` | midpoint (6.9 + 9.6)/2 = 8.25 | OK |
| quiz `q-more-rows` | 3 | $\sqrt{256/64}$ = 2, so 6/2 = 3 | OK |
| quiz `q-oos-r2` | 0.51 | 1 - (28/40)² = 0.51; cut 0.3; left 0.49 | OK |
| quiz `q-first-sentence` | choice `result` | £12.4k against £31.0k | OK, reused by review (5) |

### Review 3 (`review-3.json`)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| `r3-mse-four` | 0.045 | squares 0.04, 0.09, 0.01, 0.04 = 0.18; /4 = 0.045; sum 0.18; all four signs agree | OK, note 4 |
| `r3-leaks` | close-next, z-year, avg-next | three leak; `yret` and `volrel` safe | OK |
| `r3-persist-065` | 1.2121 | 2/1.65 = 1.21212; mean 1/(1 - 0.4225) = 1.7316; 0.35² x 1.7316 + 1 = 1.2121 | OK |
| `r3-cut` | 60.1% (0.601) | 1 - 24.9/62.4 = 0.60096; ratio 0.399; diff 37.5 stored 0.375 | OK |
| `r3-ten-days` | 2.530% | 0.8 x $\sqrt{10}$ = 2.5298; linear 8% = 0.08 | OK |
| `r3-shifted-four` | 0.275 | days 2 to 5: 1.1/4 = 0.275; unshifted days 3 to 6: 1.0/4 = 0.25 | OK |
| `r3-vif-08` | 1.5119 | 1/(1 - 0.5625) = 2.2857; root 1.51185 | OK, note 1 |
| `r3-price-r2` | choice `persist` | text only | OK, note 3 |
| `r3-parts-baseline` a | -0.029 | 1 - 3.19/3.10 = -0.02903; flip 0.029; ratio 1.029 | OK |
| `r3-parts-baseline` b | choice `no` | 3.10 is the lowest; 3.19/3.10 = 2.9% above | OK |
| `r3-parts-baseline` c | 2.945 | 0.95 x 3.10 = 2.945; plus 1.05 x 3.10 = 3.255 | OK |
| `r3-report-sentence` | choice `wide` | 12.4 +/- 2.4; 12.4/31 = 0.40 exactly | OK, duplicate (5), length note |

### Homework 3 (`homework-3.json`)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| `h3-rent-parts` 1 | 530 | nothing dropped; dropped 524; both 530 - 6 - 24 = 500 | OK |
| `h3-rent-parts` 2 | 58% (0.58) | 1 - 131/312 = 0.58013; share 0.4199; diff 181 stored 1.81 | OK |
| `h3-rent-parts` 3 | 0.8237 | 1 - (131/312)² = 0.82371; cut 0.58; left 0.1763 | OK |
| `h3-rent-parts` 4 | choice `se` | (35 - 21)/14 = 1.0; VIF at 0.82 = 3.0525; root 1.747 | OK |
| `h3-frame-order` | a, b, c, d, e | text only | OK |
| `h3-features-code` | `ret[1]` 0.0021417, `mean10[25]` 0.0010172, `vol_rel[100]` 0.3826938, `y[500]` 0.0085630, first valid 10, 980 rows | all agree; 980 rows are indices 19 to 998. Solution 9/9, starter 1/9 | OK |
| `h3-baselines-code` | 1.1942044, 7.4129795, 1.1482173 | 1.194204, 7.412980, 1.148217. Solution 5/5, starter 0/5 | OK, explain 3.9% (3) |
| `h3-log-code` | rmse 28.76694122, garden 7.25177434 | 28.766941, 7.251774. Solution 4/4, starter 0/4 | OK |
| `h3-report-longform` | rubric, model text | 104 words; 1 - 212/498 = 57.4%; R² 1 - (212/498)² = 0.819; rubric points sum to 10 | OK |
| `h3-five-day` | 0.4472 | $1/\sqrt{5}$ = 0.44721; share 0.2; three 0.5774 | OK |
| `h3-persist-08` | 1.1111 | 2/1.8 = 1.1111; mean 1/0.36 = 2.7778 | OK |

## Numbered fix list

1. `l11-framing-the-question.json`, quiz `q-hit-rate`, wrong `hit`: change `value` from 0.006667 to 0.6667 (tolerance 5e-06 can stay).
2. `l14-house-price-case.json`, screen 9 "Rents by postcode", wrong `sum`: the value 169.7 does not match "You added the errors". Change the byKey line to "You used the single-rent spread for both means: $\sqrt{120^2 + 120^2}$." and keep 169.7, or set the value to 120 and merge it with `sd`.
3. `l14-house-price-case.json`, screen 2 `feedback.correct`: replace "more than halves the baseline error" with "cuts the baseline error by 45%".
4. `l11-framing-the-question.json`, screen 5 hint (step): "$-0.0100$" to "$-0.0101$".
5. `homework-3.json`, `h3-baselines-code` explain: "3.8%" to "3.9%".
6. `review-3.json`, `r3-report-sentence`: new numbers in place of 12.4 and 31.0 (lesson 15 `q-first-sentence` uses them), then recompute the interval, the "±" figure, the 40% ratio and the "60% cut" feedback.
7. `l15-presenting-a-result.json`, screen 9, option `period`: "than use" to "than the period of use".
8. Voice: shorten the 20-word and longer sentences listed above.
9. Key lengths: trim or balance `l15` screen 8, `l11` screens 4 and 9, `review-3` `r3-report-sentence`.
