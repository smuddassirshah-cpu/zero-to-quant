# Topic 1.6 (statistics): second-reader findings

Scope: every lesson, review and homework file in `estimation`, `testing` and `regression`, plus `app/content/exams/topic-1.6.json`.
Method: I recomputed every stated number in Python with numpy, scipy and statsmodels 0.15.0. Seeded engine simulations were reproduced with the engine's mulberry32 through `simh.js` and `barsim.js`. Python `random.Random(seed)` claims were re-run. Every code item's solution was run against its tests, and each statsmodels figure quoted in prose was reproduced from the item's own data. Each distractor's value was re-derived from its `why` or byKey line. I also scanned for tolerance overlaps (`tolcheck.py`), numeric `unit: "%"` scaling (`pctscan.py`), wrong ids with no byKey line, and style (`style.py`, `sentcount.py`, `poundmath.py`).
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation or teaching issue; note = style.

## estimation

- app/content/courses/estimation/l1-sample-population.json | screens[1] wrong 'dropped-minus' (0.0082) | error | The why says the learner dropped the minus signs. The absolute values of the ten returns add to 10.6, which gives 1.06%, and no slip gives 0.82%. So a learner who drops the signs gets the generic line. | Value 0.0106.
- app/content/courses/estimation/homework-2.json | hw2-code explain | error | "5,000 densities of about 40 each": the N(0, 0.01²) density at a typical return of 0.01 is 24.2, and 39.9 is the peak at 0. | "about 24 each".
- app/content/courses/estimation/l2-estimates-vary.json | screens[2] wrong 'variance' (0.1, so a typed 10) | warning | The why, "You typed 10% or so", names no action. The natural variance slip, σ²/n = 0.1, would be typed 0.1, and that is caught by 'over-n'. | Drop 'variance', or point it at σ² = 1 typed as 1 (value 0.01 is taken by 'sigma'). Add "or you gave the variance, 0.1" to over-n.
- app/content/courses/estimation/l3-right-target.json | screens[9] wrong 'points' (0.036) | note | This value needs a typed 3.6. A learner who subtracts the two volatilities, 1.414 − 1.378, types 0.036, which the engine reads as 0.00036. | Value 0.00036 with the current why, or reword the why for a typed 3.6.
- app/content/courses/estimation/l4-bias-against-variance.json | screens[1] explain | note | "Bias grows only as 1 − w" compares the wrong pair. The trade-off is variance against bias², and both are quadratic. The real reason is that at w = 1 the variance slope is 0.08 while the bias² slope is 0. | "Near w = 1, shrinking cuts variance at once, while the squared bias starts flat."
- app/content/courses/estimation/l7-taking-logs.json | screens[8] explain | note | Cites the internal course id "`least-squares`" in code font. | "Orthogonality and Least Squares".
- app/content/courses/estimation/l11-bootstrap.json | screens[3] wrong 'rank24' | note | rank25 and rank24 are both −0.295 with the same tolerance, so rank24 never fires, and it has no byKey line. | Drop rank24, or give it the 24th value.
- app/content/courses/estimation/l12-updating-a-belief.json | screens[3] wrong 'noprior' (0.75) | note | The why, "a/(a + b) for Beta(9, 3)", names no learner action. The slip is adding the prior heads but not the prior tails, 9/12. | "You added the prior's heads but not its tails."
- app/content/courses/estimation/homework-1.json | h-pnl-se explain | note | A bare £ inside maths (`$\mathrm{SE} = £12{,}000 / \sqrt{64} = £1{,}500$`) renders in italic maths type. | Move the amounts outside the maths, or use `\text{£}`.
- app/content/courses/estimation/l3-right-target.json, l4-bias-against-variance.json | screens[0], screens[6] explain | note | Four sentences each (limit 3). | Merge two sentences in each.
- app/content/courses/estimation/homework-1.json items[3] explain (26 words), l5-which-fits.json s5 prose (26), l8-volatility-mle.json s10 prose (25), l11-bootstrap.json s4 widget.how (30) | — | note | Sentences over 20 words. | Split, at the semicolon where there is one.
- app/content/courses/estimation/l1 s4, l2 s6/s8/summary.trap, l8 s1/s9, l10 s7, review-2 item1, homework-1 items 6 and 7, homework-3 rubric 6 | — | note | Eleven more sentences of 21 to 24 words. | Split where the text allows.
- app/content/courses/estimation/l9-how-precise.json | quiz[1] explain and three labels | note | "percent" (American). | "per cent".

## testing

- app/content/courses/testing/l4-t-test.json | screens[0] canvas table, Fund C | note | z printed as 1.46: 2.57/(5/√8) = 1.454. | 1.45.
- app/content/courses/testing/l6-power.json | screens[9] feedback and explain | note | "6.18 × 400 ≈ 2,473": 6.18 × 400 = 2,472, and 2,473 comes only from the unrounded 6.1826. | "6.18 × 400 ≈ 2,472", or quote 6.183.
- app/content/courses/testing/homework-3.json | h-sidak explain | note | "Bonferroni's 0.0005 is 2.6% smaller": it is 2.5% smaller than Šidák's 0.000513. Šidák is 2.6% larger. | "Šidák's bar is 2.6% larger."
- app/content/courses/testing/l12-data-snooping.json | screens[0] lookback table | note | The seed-74 table cannot be reproduced: neither the generator nor the model is stated. The equity curve does check (in-sample Sharpe 0.857, out-of-sample −0.027). | Name the generator in the caption, or drop "seed 74".
- app/content/courses/testing/l9-twenty-tests.json | p-value grid caption | note | Says only "seed 30". The grid is Python `random.Random(30).random()` to 2 places, not the engine's mulberry32. | "Python random, seed 30".
- app/content/courses/testing/homework-2.json | items[0] wrong 'alarms-only' 299.4 ± 1 and 'all-trades' 300 ± 1 | note | The two tolerances overlap, so a value of 299.5 to 300.4 matches both. | Tolerance 0.3 on each.
- app/content/courses/testing/l2-measuring-surprise.json | quiz[0] explain | note | A bare £ inside maths renders in italic type. | Move the £ outside the maths.
- app/content/courses/testing/homework-2.json | items[5] wrong 'one-minus-alpha' | note | No byKey line, so the named slip gets the generic text. | Add "0.95 is 1 − α, the chance a dud fails. Weigh passes by the base rate."
- app/content/courses/testing/review-2.json | items[6] wrong 'prior' | note | No byKey line. | Add "0.05 is the base rate before the test. A significant result should raise it."
- app/content/courses/testing/l6-power.json | quiz[0] 'old', quiz[2] 'same' | note | No byKey lines. | Add one line each: "That is the power at 100 orders" and "A smaller effect needs more days, not the same".
- app/content/courses/testing/homework-3.json items 7 and 8, l11-is-sharpe-real.json s9, l12-data-snooping.json s2, l9-twenty-tests.json quiz[2] | explain | note | Four sentences each (limit 3). | Trim to three.
- app/content/courses/testing/l3 s8, l4 s8, l6 s8, l8 s8, homework-1 items[5], homework-2 items[4] | widget.how | note | "math.isclose" in prose without code format (it flags as American "math"). | `math.isclose`.
- app/content/courses/testing/l9-twenty-tests.json s9 prose (27 words), l10-correcting.json quiz[0] prose (25) | — | note | Sentences over 20 words. | Split at the colon or semicolon.
- app/content/courses/testing/l3 s1/s2, l4 s2, l6 s6, l8 s4, l12 s5 and s6 hint, homework-3 items[5] and rubric 2 and 5 | — | note | Ten more sentences of 21 to 24 words. | Split where the text allows.
- app/content/courses/testing/homework-1.json items[4], l8-two-groups.json quiz[2], review-2.json items[1] | — | note | "in percent" (American). | "in per cent".

## regression

- app/content/courses/regression/l8-alpha-and-beta.json | screens[0], screens[2], screens[3], quiz[1] numeric | error | `unit: "%"` with answers written in percentage points (0.25, 3.0, 0.1667, 0.2). The engine divides a typed % by 100 (numeric.js), so a learner typing 0.25 is graded as 0.0025 and marked wrong. The playthrough types 25, 300, 16.67 and 20, so it passes. | Divide each answer, tolerance and wrong value by 100 (0.0025, 0.03, 0.001667, 0.002), or set `unit: ""` and keep the numbers.
- app/content/courses/regression/l9-several-predictors.json | screens[10] numeric | error | Same scaling fault: answer 0.88 with `unit: "%"` needs a typed 88. | Answer 0.0088 (wrong values 0.0109, 0.013, 0.0087; tolerance 0.00005), or `unit: ""`.
- app/content/courses/regression/review-2.json | r-raw-intercept | error | Same scaling fault: answer −0.15 with `unit: "%"` needs a typed −15. | Answer −0.0015 (wrong values 0.0015, 0, 0.003; tolerances / 100), or `unit: ""`.
- app/content/courses/regression/l7-summary-table.json | screens[3] wrong 'k' (0.1018) | error | Charging for two predictors gives 1 − 0.8688 × 59/57 = 0.1007. That lies inside 'by-n' (0.1012 ± 0.0006), so this learner gets the by-n line. | k = 0.1007, tolerance 0.0002; by-n tolerance 0.0002.
- app/content/courses/regression/l9-several-predictors.json | screens[6] wrong 'over-n' (0.9694) | error | The why says n = 6 went on top: 1 − 0.0204 × 6/2 = 0.9388. 0.9694 is 1 − 0.0204 × 6/4, which matches no slip. | Value 0.9388.
- app/content/courses/regression/l11-assumptions-fail.json | screens[5] prose, hint and explain | error | "d = 1.87": the 60 plotted residuals give d = 1.81. | 1.81 throughout. The answer is unchanged.
- app/content/courses/regression/l12-matching-statsmodels.json | quiz q-f-r2 wrong 'n1' (4.556) | error | The why says n − 1 = 43 went underneath, which gives (0.25/3)/(0.75/43) = 4.778. 4.556 comes from n − k = 41. | Value 4.778, or why "You used n − k = 41; the intercept costs one too".
- app/content/courses/regression/review-1.json | rv-flat wrong 'median' (10.25) | error | The why says "You used the median, 0.5". The median of 2, −1, 0, 3 is 1, equal to the mean, so it gives the right answer, 10. A line at 0.5 gives 11, and 10.25 matches a = 0.75 or 1.25. | Replace it with 'zero', value 14 (squares about 0): "You squared the returns themselves. Subtract the mean, 1, first."
- app/content/courses/regression/homework-3.json | h-s2-trap wrong 'n1' (0.9177) | error | The why says n − k = 17: √(17/20) = 0.9220, outside 0.9177 ± 0.002. 0.9177 is √(16/19). | Value 0.922.
- app/content/courses/regression/l5-how-sure.json | screens[5] | warning | The prose says "the noise estimate stays near s = 1.102", but the 40 plotted points give s = 1.178 and SE 0.0648. The answer, 0.0607 ± 0.001, rejects a learner who computes from the plot. | State s = 1.102 as given, not as the plot's, or regenerate the points so s = 1.102.
- app/content/courses/regression/l10-collinearity.json | screens[5] explain | warning | "NumPy's solve returns nan or raises, depending on the build" is false here. On this X'X (determinant −7e−15 after rounding) `np.linalg.solve` silently returns a finite, arbitrary [2.505, 0.0015, 0.05]. That silent answer is the real danger. | "NumPy's solve may raise, or silently return an arbitrary answer like [2.505, 0.0015, 0.05]."
- app/content/courses/regression/l3-how-much-explained.json | screens[8] hint | note | "a low signal then a fall", but p39 is (1.42, 2.32), a high signal then a rise. | "a high signal then a rise".
- app/content/courses/regression/l11-assumptions-fail.json | screens[6] hint, feedback | note | "t = 1.69": 0.1970/0.116 = 1.70. | 1.70.
- app/content/courses/regression/l11-assumptions-fail.json | screens[2] bars | note | The 10,000-sample funnel figures (0.109, 0.071, 0.105; 80% and 94% coverage) give no model or seed, so they cannot be reproduced. They are plausible: the 35% shortfall matches 0.071/0.109. | Name the model and seed in the caption.
- app/content/courses/regression/l12-matching-statsmodels.json | screens[4] wrong 'normal', feedback, explain | note | The two-sided normal p for t = 2.069 is 0.0385. 0.0386 is twice the rounded 0.0193. | 0.0385.
- app/content/courses/regression/l12-matching-statsmodels.json | screens[2] hint[1] | note | Says "the Df Residuals line" and highlights l3 to l5, but this console holds only the coefficient rows. | Drop the highlight, or point back to screen 0's l5.
- app/content/courses/regression/l8-alpha-and-beta.json | screens[9] wrong 'se-only' | note | No byKey line. | Add "0.333 is the error alone. Divide the monthly alpha by it."
- app/content/courses/regression/homework-3.json | h-vif-n wrong 'plus' (126) | note | No byKey line. | Add "VIF multiplies the variance; it does not add months."
- app/content/courses/regression/l12-matching-statsmodels.json s1, l6-is-slope-zero.json s0 | explain | note | Four sentences each (limit 3). | Trim to three.
- app/content/courses/regression/l6 s9, l7 s8, l8 s10, l9 s4, l10 s10, homework-2 items[4] | widget.how | note | "math.isclose" in prose without code format. | `math.isclose`.
- app/content/courses/regression/l10 summary.trap (32 words), l9 summary.trap (27), l2 s6 explain (25), l6 s6 explain (25), l4 s8 widget.how (29), l7 s8 widget.how (first sentence 22), l11 s4 prose (first sentence) | — | note | Sentences over 20 words. | Split, at the colon where there is one.
- app/content/courses/regression/l1 s0/s2/s7, l2 s4/summary.trap, l3 s0/s3/s6/s8/quiz[2], l4 s4/quiz[2]/quiz[3], l6 s1, l7 s6/s9, l9 s10/quiz[3], l10 s8, l11 quiz[3]/summary.trap, l12 summary.trap/s2 how, homework-1 items 1/4/5/7, homework-3 items 3 and rubric 3 and 5 | — | note | 33 more sentences of 21 to 24 words. | Split where the text allows.

## exam (app/content/exams/topic-1.6.json)

- app/content/exams/topic-1.6.json | s-track-record model | warning | The JSON holds an escaped `\\n\\n` before "**(d)**" and "**(e)**", so the model answer shows a literal "\n\n" and runs (c), (d) and (e) into one paragraph. | Replace it with a real paragraph break (`\n\n` in the JSON).
- app/content/exams/topic-1.6.json | s-hedge-ratio | warning | The core is identical to regression/review-1 rv-r-slope: correlation 0.8, sds 1.5% and 1.0%, slope 1.2, and the same three distractors scaled by £2m. It tests recall. | New numbers, e.g. correlation 0.7 with sds 2.0% and 1.4%.
- app/content/exams/topic-1.6.json | whole exam | warning | The exit line asks the learner to "explain every number in its summary table". Item 23 rebuilds the numbers in NumPy, but no item shows a statsmodels summary and asks what a line means (Df, F, Prob (F), Durbin-Watson, Omnibus or Cond. No.). | Add one console item, e.g. tap the line that answers "do the factors matter jointly?" or "are the residuals autocorrelated?".
- app/content/exams/topic-1.6.json | s-beta-posterior | note | es-bayes is tested by this one item, with one conjugate update. | Fine at 26 items. A second Bayes item (posterior interval, or prior worth n trades) would balance the map.
- app/content/exams/topic-1.6.json | items[22], items[23] widget.how | note | "math.isclose" without code format. | `math.isclose`.
- app/content/exams/topic-1.6.json | s-welch explain | note | "a tenth of a percent" (American). | "a tenth of a per cent".
- app/content/exams/topic-1.6.json | items[22] prose and widget.how | note | 22- and 24-word sentences. | Split.

## Automated checks (no finding)

- Every other stated number checks. The best-of-100 Sharpe figure, 1.12 (testing l11, engine seed 77: mean 1.119; E[max of 100 normals] = 2.5076), is cited consistently in validation/l12-too-many-models and fin-ml/l11-deflated-sharpe.
- Sharpe and hit-rate inference all check: SE ≈ 1/√T in years, √252 and √12 annualisation, t = SR√T, the exam's 36-year alpha record, the 1,719 trades, and the 0.0359 and 0.023 p-values.
- Multiple testing checks: Bonferroni, Šidák (0.00256, 0.00103, 0.005116) and BH (testing l10: 3 against 1; the 500-stock screen: 4; exam s-bh-tap: ranks 1 to 5, with every byKey bar right). FWER 0.6415 matches the engine's seed 9 (0.642).
- HAC and overlap: the l11 statsmodels expectations ([0.1115, 0.1047, 0.1648], [0.07, 0.105, 0.0868] and the two other tests) reproduce exactly, and the plotted residuals are exactly ret on sig (d = 0.380, t 2.13 → 1.44). A 600-run simulation of 20-day overlapping returns gives naive-t sd 3.76, 58% beyond 1.96, and 13% with 40-lag HAC, in line with 3.63, 0.60 and 0.12. The factor √(1 + 2Σ(1 − j/h)²) gives 2.588 (h = 10) and 3.74 (h = 21) as stated. HC1's n/(n − k − 1) matches statsmodels.
- statsmodels output quoted in prose reproduces from the item data: regression l7 (with and without a constant), l8 (0.250024/1.199952, SE α 0.8387), l10 VIFs (34.9197/36.3583/1.3979), l12 (whole summary: 0.1648/1.0192/0.7941, scale 4.2889, F 16.78, p 0.000334, (X'X)⁻¹ entries), the review-2 factor console, and homework-3 HC1 [0.6519, 0.1108, 0.3589]. Console tap and highlight ids are 1-based and correct everywhere checked.
- Every code item's solution passes its own tests, including exam items 22 and 23, whose factor_report matches statsmodels to 6 places.
- MLE checks: normal mean and volatility (0.927%, 0.975%, 16.0%, exam 22.45%), the exponential rate 1/m, and Bernoulli log-likelihoods. Bayesian updating checks: Beta(30, 30) and the estimation l12 posteriors.
- Seeded figures reproduced: estimation l2 (seed 1610), l11 (Python seeds; engine seed 1), homework-3 bootstrap (equal to the l11 histogram); testing l1 (seed 143 → 57 of 1,000), l9 (seeds 15/4/5, engine seed 9), l11 (seed 77), l12 (seed 50: Python gauss/√5).
- Order derivations are consistent with their `same` groups. Longform rubrics sum to 10. No "!" and no "$" currency.

## Coverage against the curriculum (Cover and Exit lines)

- Covered: estimators and sampling distributions, bias, variance and MSE, maximum likelihood (Bernoulli, normal mean and variance, exponential), confidence intervals (z, t, proportion, bootstrap), hypothesis tests (z, one- and two-sample t, Welch, paired), p-values and their misreadings, power and sample size, multiple testing (FWER, Bonferroni, Šidák, BH, data snooping, best-of-N Sharpe), simple and multiple regression, R² and adjusted R², inference on coefficients, F, collinearity and VIF, omitted variables, residual diagnostics, heteroscedasticity and HC1, autocorrelation, Durbin-Watson and HAC, overlapping returns, and Bayesian updating (Beta-binomial).
- Exit line: regression l12 and exam item 23 fit a regression in NumPy and match statsmodels to 4 to 6 places. Regression l7 explains each summary line, Omnibus, Jarque-Bera and Cond. No. included. The exam does not test the "explain every number" part (see the exam warning).
- Thin spots against DeGroot and Schervish: Bayesian updating is one lesson with one conjugate family (no normal-normal update, no credible interval against a confidence interval). Sufficiency, Fisher information and the Cramér-Rao bound, and likelihood-ratio tests and the chi-square family, do not appear. None of these is named in the Cover line.
- Skills map: all 13 exam skills are tested (rg-inference 5, ht-pvalue 4, es-intervals 4, ht-setup 3, ht-errors 3, ht-multiple 3, es-estimators 2, es-biasvar 2, es-mle 2, rg-fit 2, rg-diagnostics 2, rg-multiple 2, es-bayes 1), and each is taught by its course's lessons.

## Fix pass

I recomputed every corrected number before writing it (Python with numpy, scipy and statsmodels 0.15.0; the reviewer's seeds and the original generators in the scratchpad for the two unreproducible figures). After the edits, an interval-overlap check finds no overlap between an answer and a misconception, or between two misconceptions, in any topic 1.6 file. `sentcount.py` finds no explanation over three sentences, and `style.py` raises no American-spelling or bare-£ flag; its remaining long-sentence flags are sentences the counter joins (see lines 11, 12, 27 and 50). `node tools/validate.mjs`: 0 errors in topic 1.6 files. Every touched file passes the playthrough.

The `unit: "%"` convention: every `%` widget now stores the fraction and keeps `unit: "%"`, so the learner types the number of per cent (0.25 for 0.25%). The surrounding prose already asks for answers "in %", and estimation and testing already worked this way. Fed through the engine's own `parseNum`, `within` and `matchWrong`, each of the 32 `%` widgets in topic 1.6 accepts its answer as a learner types it, and each distractor typed the same way returns its own key.

Status: fixed 56, disputed 0, deferred 1. Four lines were fixed in part, with the rest disputed (11, 12, 27, 50). Where a fix differs from the proposal, the line says why.

### estimation (13 fixed)

1. l1 s1 `dropped-minus`: fixed, value 0.0082 → 0.0106 (7.4 + 3.2 = 10.6, so 1.06%).
2. homework-2 hw2-code explain: fixed, "about 24 each" (the N(0, 0.01²) density at 0.01 is 24.2).
3. l2 s2 `variance`: fixed. The distractor and its byKey line are dropped. The `over-n` line now says "or gave the variance $\sigma^2/n = 0.1$", since a typed 0.1 lands there.
4. l3 s9 `points`: fixed, value 0.036 → 0.00036 (tolerance 0.00005), so a typed 0.036 gets the subtraction line. `other-way` tolerance 0.0002 → 0.00015, because it met the answer's band at 0.0255.
5. l4 s1 explain: fixed, wording as proposed. Checked: the slope of $0.04w^2$ at $w = 1$ is 0.08, and the slope of $(1 - w)^2\mu^2$ is 0.
6. l7 s8 explain: fixed, "Regression in Orthogonality and Least Squares".
7. l11 s3 `rank24`: fixed, dropped. The table shows rank 24 as −0.295 too, so a 24th value cannot be given.
8. l12 s3 `noprior`: fixed, "You added the prior's 2 heads but not its 2 tails: $9/12$."
9. homework-1 h-pnl-se: fixed, "The SE is £12,000 over $\sqrt{64} = 8$, or £1,500."
10. l3 s0 and l4 s6 explains: fixed, three sentences each.
11. Over-20 sentences: fixed in homework-1 items[3] (now three sentences), l8 s10 and l11 s4 `how`. Disputed for l5 s5: Ana's sentence is 18 words. The counter joins it to the next sentence because it ends inside a closing quote.
12. Eleven sentences of 21 to 24 words: fixed in l2 s8, l8 s1, l8 s9 (still three sentences), review-2 items[1], homework-1 items[6] and [7], and homework-3 rubric 6. Disputed for l1 s4, l2 s6 `sd`, l2 summary.trap and l10 s7. Each is under 20 words, and the counter joins it to a neighbour that starts with a digit or follows display maths.
13. l9 quiz[1] "percent": fixed. All 19 uses of "percent" in topic 1.6 labels, placeholders and prose are now "per cent". Ids, `format` values and code are unchanged.

### testing (15 fixed)

14. l4 s0 table: fixed, Fund C 1.46 → 1.45. Fund B had the same fault: 1.12 → 1.13 (1.99/(5/√8) = 1.126). The $t$ column checks.
15. l6 s9: fixed, "$6.18 \times 400 = 2{,}472$" in the feedback, explain and accept line. The graded answer stays 2,473 (rel 0.002), which accepts both.
16. homework-3 h-sidak: fixed, "Šidák's bar is 2.6% larger than Bonferroni's 0.0005".
17. l12 s0: fixed. The generator is now named: "independent normal months with sd 4% ... (Python `random`, seed 74)". Re-running the lesson's generator reproduces all 12 in-sample and out-of-sample Sharpe ratios.
18. l9 grid caption: fixed, "(Python `random`, seed 30)".
19. homework-2 items[0]: fixed with tolerance 0.25 on `alarms-only` and `all-trades`, not the proposed 0.3. With 0.3 the two bands still meet at 299.7.
20. l2 quiz[0]: fixed, "£0.40 over $\sqrt{64} = 8$, or £0.05".
21. homework-2 items[5] `one-minus-alpha`: fixed, byKey line added as proposed.
22. review-2 items[6] `prior`: fixed, byKey line added as proposed.
23. l6 quiz[0] `old` and quiz[2] `same`: fixed, byKey lines added. Each names the slip.
24. homework-3 items 7 and 8, l11 s9, l12 s2 and l9 quiz[2]: fixed, three sentences each.
25. `math.isclose`: fixed, in code formatting in all six. The two "needs only math" became `math`, and the full `math.isclose(...)` call is in code.
26. l9 s9 and l10 quiz[0]: fixed, split.
27. Ten sentences of 21 to 24 words: fixed in l3 s1 and s2, l8 s4, l12 s5, l12 s6 hint, homework-3 items[5], and rubric 2 and 5. l12 s6 prose also lost the inverted "Survivorship bias you met in". Disputed for l4 s2 and l6 s6: the sentence ends inside display maths, and the words outside it number under 20.
28. "in percent": fixed, "in per cent" in all three.

Also: homework-3 h-vendor had both `prose` and a longform `prompt`, so its task list never showed on screen (validator warning). The scenario now opens the prompt, and `prose` is gone.

### regression (22 fixed)

29. l8 s0, s2, s3, quiz[1] `%`: fixed. The fraction is stored and `unit: "%"` kept. Answers are 0.0025 (tolerance 0.0001), 0.03 (0.0005, so 3.04% still passes), 0.001667 (0.00003) and 0.002 (0.00005). Every distractor is divided by 100 the same way. A typed 0.25, 3, 0.1667 and 0.2 are accepted; a typed 25 now gets the generic line.
30. l9 s10 `%`: fixed, answer 0.0088 (0.00005). Wrong values are 0.0109, 0.013 and 0.0087 (0.00003), and the accept line now reads "0.88%".
31. review-2 r-raw-intercept `%`: fixed, answer −0.0015 (0.00005). Wrong values are 0.0015, 0 and 0.003, and the accept line now reads "$-0.15$%".
32. l7 s3 `k`: fixed, value 0.1007 (1 − 0.8688 × 59/57), tolerance 0.0002. `by-n` tolerance is now 0.0002 (0.1012), so they no longer overlap.
33. l9 s6 `over-n`: fixed, value 0.9388 (1 − 0.0204 × 6/2).
34. l11 s5: fixed, $d = 1.81$ in the prose, hint and explain (the 60 plotted residuals give 1.8127).
35. l12 q-f-r2 `n1`: fixed, value 4.778 ((0.25/3)/(0.75/43)).
36. review-1 rv-flat: fixed. `median` is replaced by `zero`, value 14 (4 + 1 + 0 + 9), with the byKey line as proposed.
37. homework-3 h-s2-trap `n1`: fixed, value 0.922 (√(17/20) = 0.9220).
38. l5 s5: fixed. The prose now says to keep $s = 1.102$ from before, and that this draw happens to give 1.18. The answer, 0.0607, is unchanged.
39. l10 s5 explain: fixed with different wording. The proposed vector depends on an $\mathbf{X}^T\mathbf{y}$ the screen never shows. Checked: on this $\mathbf{X}^T\mathbf{X}$ (det −7.0e−15) NumPy 2.5 returns finite answers without an error. The explain now says rounding can leave a tiny nonzero determinant, and `solve` then silently returns one arbitrary point on the line.
40. l3 s8 hint: fixed with a wider change than proposed. p39 (1.42, 2.32) is a high signal then a rise, but p58 (−1.35, −3.92) really is a low signal then a fall. The hint now names both.
41. l11 s6: fixed, $t = 1.70$ in the hint and feedback.
42. l11 s2: fixed. The prose now names the model and the seed: $x \sim N(0, 1)$, noise sd $0.5(0.5 + |x|)$, NumPy seed 11. Re-running the lesson's simulation gives sd 0.1087, usual SE 0.0713 and HC SE 0.1050, with coverage of 80.3% and 93.8%.
43. l12 s4: fixed, the normal $p$ is 0.0385 in the wrong value, feedback and explain.
44. l12 s2 hint[1]: fixed another way. With the highlight dropped, the validator warns about a point hint with no highlight. The hint now highlights the three coefficient rows on this console and reads "$n$ less one for each of the three coefficients here".
45. l8 s9 `se-only`: fixed, byKey line added as proposed.
46. homework-3 h-vif-n `plus`: fixed, byKey line added, with "So $n$ grows 6.25 times."
47. l12 s1 and l6 s0: fixed, three sentences each.
48. `math.isclose`: fixed, in code formatting in all six.
49. Over-20 sentences: fixed in l10 trap, l9 trap, l2 s6, l6 s6, l4 s8 `how`, l7 s8 `how` and l11 s4. l11 s7's inline five-point list is now a numbered list.
50. Thirty-three sentences of 21 to 24 words: fixed in all except l2 s4 and l3 s3. Those two are disputed, because the counter joins them across display maths or an italic link and each is under 20 words. Where a split pushed an explanation to four sentences, it was rewritten in three (homework-1 items[1], l1 s7, l2 s6, l3 s6 and s8, l4 s4, l6 s1 and s6, l7 s6).

Also: review-3 items[7] `raw` (0.343) and `swap` (0.333) met at 0.338. Both tolerances went from 0.005 to 0.004.

### exam (6 fixed, 1 deferred)

51. s-track-record model: fixed. The two escaped `\\n\\n` are now real paragraph breaks, so (c), (d) and (e) are separate paragraphs.
52. s-hedge-ratio: fixed with different numbers from the ones proposed. Correlation 0.7 with sds 2.0% and 1.4% gives a slope of exactly 1.0, the same number as the one-for-one hedge slip. The item is now £5m of stock, sds 1.8% and 1.2%, correlation 0.6, so the slope is 0.9 and the answer is £4.5m. The distractors are £7.5m (no $r$), £2.0m (flipped, slope 0.4) and £3.0m ($r$ alone), and the explain and feedback were rewritten to match.
53. Whole exam, summary-table line: fixed. A new item, s-summary-dw (difficulty 3, rg-diagnostics), comes after s-overlap-hac. It shows a statsmodels `summary()` of a fund holding illiquid loans: 60 months on market and credit factors, NumPy seed 3, AR(1) residuals with coefficient 0.6. The learner taps the line that says whether residuals repeat month to month: Durbin-Watson 0.788 on l16. Every number on the console is statsmodels' own. byKey lines cover Prob(Omnibus), Prob (F), Covariance Type, a coefficient row and Skew. The exam now has 27 items: 5, 14, 5 and 3 at difficulties 2 to 5, within the ramp.
54. s-beta-posterior, a second Bayes item: deferred. The review rates it fine at 26 items, and it is not a wrong claim. Recorded here for the next exam pass.
55. Items 22 and 23 `how`: fixed, `math.isclose` in code formatting. "numpy is available" now starts with a capital, "NumPy".
56. s-welch: fixed, "a tenth of a per cent".
57. Item 22 prose and `how`: fixed, split ("It reports four numbers. They are ...").

### Notation (all three courses and the exam)

`\mathrm{Var}` (82), `\mathrm{Cov}` (16) and `\text{Var}` (1) are now `\operatorname{Var}` and `\operatorname{Cov}`, as in topic 1.5. `\mathrm{SE}` and `\mathrm{MSE}` stay as they are.

No `course.json` was changed, and none needs a change. The three topic 1.6 `course.json` files hold no `\mathrm{Var}`, "percent" or internal course id.
