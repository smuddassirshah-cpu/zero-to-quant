# ml-int levels 1 to 3 (ML interviews): second-reader findings

Scope: every file in `app/content/courses/ml-int/` (l1 to l12, review-1 to 3, homework-1 to 3), the six `mi` drills in `app/content/drills/` with the session `drills/sessions/mi-sixty.json` and their `drills/index.json` rows, and `app/content/data/ai/ml-int-case-daily-mse.csv`. Branch `review-ml-int` from `ee820037`.
Method (no browser): the three number scripts through `run-number-scripts.mjs --only ml-int` (3 passed, 11 s) and directly with `ZQ_NUMBERS_STRICT=1` under default threads and under one BLAS thread (267, 254 and 174 checks pass; outputs identical); L3's `--write` under both thread settings reproduces the CSV byte for byte (35,653 bytes), so the file is what the script writes and the figures are scikit-learn 1.6.1 results (NumPy 2.0.2, SciPy 1.18.1). `grade-all.mjs --code --strict-feedback` on all 18 files: 0 failures (175 widgets, 22 Python code widgets). `planted-check.mjs --near-miss --require` on the six drills: 0 failures (18 planted). `same-course-reuse.mjs --all`: no ml-int line. `voice-scan.py 35`: 0 and 0; validator 0 errors. Every stated number recomputed by hand or in Python, also from the rounded inputs each screen shows (`case.csv` re-read for the paired tests); autocorrelation and Newey-West t of the daily differences computed with statsmodels; double descent rerun with noise 0. 29 own solutions (27 wrong, 2 controls) run against the hidden tests natively, and every survivor confirmed in Pyodide on a scratch copy (appendix). Read against `docs/briefs/ml-int.md`, AUTHORING sections 5 and 9, and the prerequisites `nn-train` l3, l12, l16, `validation` l5 to l7, `research-int` L2.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, teaching or interview-truth issue, test gap; note = style or small point.

Counts: 5 errors, 19 warnings, 18 notes. Surviving wrong solutions: 4 of 27 tried (one, W26, is an acceptable method, so 3 real test gaps). Leakage: none in the case. The split is a single holdout (350 training days, 150 test days); the target is one day ahead and the generator draws every day independently, so no purge is needed (validation l7's h - 1 = 0). The MLP's early stopping uses a shuffled 10% of training rows, inside the training period only. The plain paired t is the right standard error for this panel: the daily differences have lag-1 to lag-5 autocorrelations within ±0.12, except world B seed 1 at lag 2 (-0.20). The course never says what to do when that fails (warning below).

## Level 1 (l1 to l4, review-1, homework-1)

- app/content/courses/ml-int/l3-double-descent.json | screens[5] trap, options `dd` and `agree`, summary.trap | warning | Bias and variance in deep nets: the keyed reply ("Only up to the threshold") lets the learner say the bias-variance trade-off fails past p = n. A strong interviewer's follow-up is "so is bias-variance wrong?". The expected answer is that the decomposition always holds; what fails is the idea that variance rises with parameter count. Variance peaks at the threshold, where the fit is ill-conditioned, and falls past it as the minimum-norm choice regularises implicitly. Nothing in l3, review-1 or the homework-1 model answer says this. | Add to screens[5] explain: "The decomposition still holds. Variance peaks at p = n and falls past it, because parameter count is the wrong measure of capacity once the fit is chosen by smallest norm." Key the option on that wording.
- app/content/courses/ml-int/l3-double-descent.json | screens[7] prose and option `data` | warning | "Test error peaks where the model can just interpolate the training set, p ≈ n" is right for this random-features fit, but for deep nets Nakkiran et al. place the peak where the effective model complexity (the largest training set the model can fit) is about n, not where parameters equal data points. The `data` why says the learning curve has "no second descent"; Nakkiran et al. also report sample-wise non-monotonicity, where more data can hurt near the threshold. | "...peaks where the model can just interpolate the training set: p = n here, and for a deep net where its effective complexity is about n." Change the `data` why to "That is the usual learning curve. Near the threshold, Nakkiran et al. find more data can even hurt."
- app/content/courses/ml-int/l3-double-descent.json | screens[0] to [6] | warning | Re-teaches `nn-train` l12 almost step for step: the same 40 points in 10 inputs, random ReLU features, pinv minimum-norm fit, the ridge curve and the "bigger always overfits" trap. The interview-level extras (bias-variance reconciled, gradient descent from 0 finding the minimum-norm fit, effective complexity, sample-wise descent) are missing. | Merge screens[1] to [3] into one recap with the medians and spend two screens on the points above.
- app/content/courses/ml-int/l3-double-descent.json | quiz[2] wrong `var` why | warning | "You squared the change in sd. The measured floor roughly doubles; it does not quadruple." This teaches that σ² scaling is a slip, but the noise-driven part does quadruple. Rerun with noise 0 (the prelude generator, 20 seeds, computed once here): floor 0.0461 at 2,000 features, so the noise part goes from 0.0185 to 0.0763 (4.1 times), on top of a fixed approximation floor. | "The noise part does quadruple; the floor also holds an approximation error of about 0.046 that noise does not touch, so the total roughly doubles." Put 0.0461 through the author's script first.
- app/content/courses/ml-int/l3-double-descent.json | screens[8] option `snr` | warning | "Daily returns have an R² of a few per cent" overstates what is learnable. Out-of-sample R² for single-stock returns is well under 1 per cent at daily and monthly horizons (Gu, Kelly and Xiu 2020 report about 0.4 per cent a month). A quant interviewer will pick this up. | "...daily returns have an out-of-sample R² well under 1 per cent."
- app/content/courses/ml-int/l3-double-descent.json | screens[1] hints[2], feedback.correct, explain | warning | "10.1/1.17 ≈ 8.7" is false at the stated precision: 10.1/1.17 = 8.63, so 8.6. The key 8.7 (tol 0.15) comes from the unrounded norms, so both answers are accepted, but the feedback shows wrong arithmetic. | State "10.1/1.17 ≈ 8.6", or give the norms to three figures so the ratio is 8.7 on screen.
- app/content/courses/ml-int/l2-why-adam.json | objectives, screens[7] explain | warning | The objective promises "when SGD with momentum is preferred"; the lesson gives it one clause in an explain and no item asks it. Interviewers who ask "why Adam" usually follow up with when it is worse: it often generalises worse than tuned SGD on vision models (Wilson et al. 2017), it can fail to converge (Reddi et al. 2018, AMSGrad), it stores two extra copies of the weights, and it is usually run with warm-up because v̂ is noisy early (RAdam). | Add a ladder or quiz item on choosing SGD with momentum, with two of these reasons as distractor whys.
- app/content/courses/ml-int/l4-deep-learning-quickfire.json | screens[10] feedback.byKey `test-4` | error | "A logit of 500 overflowed." Test 4 uses a logit of 800, and e^500 (about 1.4 × 10^217) does not overflow float64. | "A logit of 800 overflowed."
- app/content/courses/ml-int/l2-why-adam.json | screens[3] prose | note | "Early versions skip the correction": Adam has had the correction since Kingma and Ba; the uncorrected update is RMSProp with momentum. | "RMSProp with momentum has no correction and uses m₁ and v₁ as they are."
- app/content/courses/ml-int/l3-double-descent.json | screens[4] explain | note | "Noise is what the peak amplifies": with no label noise the median peak at p = 40 is still 2.50 (computed once here). The part of tanh that 40 random features cannot represent acts as noise. | Add: "Even with no label noise the peak is about 2.5: the part of the target the features cannot represent is amplified too."
- app/content/courses/ml-int/l4-deep-learning-quickfire.json | screens[6] | note | "Every centred value is 0" holds for a fully connected layer. A convolutional batch norm also averages over spatial positions, so a batch of one still normalises, and PyTorch raises an error for a (1, C) training batch. | Add "in a fully connected layer" to the prose.
- app/content/courses/ml-int/l4-deep-learning-quickfire.json | screens[9] option `axis` | note | Averaging over the wrong axis at initialisation gives about ln 65 / 65 = 0.064, not a loss near 0.01. | "The loss is divided by the wrong count, for example by V as well."

## Level 2 (l5 to l8, review-2, homework-2, the six drills, mi-sixty)

- app/content/courses/ml-int/l8-a-layers-backward-pass.json | screens[4] feedback.byKey `sign` | error | "Both paths carry a negative gradient here: -1 × 2 and half of -1." The second path is positive: Z₂,₂ gets dout = 1 through W₂,₂ = 1, and the central difference adds half of +1. The total is -2 + 0.5 = -1.5, as the hint says. | "The path through Z₂,₁ gives -2 and the kink adds +½: the total is -1.5, negative."
- app/content/drills/mi-cross-entropy-logits.json | tests | warning | Test gap: shifting by the batch maximum instead of each row's (W4) passes all 9 tests in Pyodide. Every multi-row test has rows of similar scale. On `[[0, 1], [1000, 1001]]` it returns -inf. The softmax drill has exactly this test ("Rows 1,000 apart"). | Add a test `mean_cross_entropy([[0.0, 1.0], [1000.0, 1001.0]], [0, 1])` (expect the mean of 1.3133 and 0.3133, 0.8133) and a fourth planted solution for it.
- app/content/courses/ml-int/l7-k-means-against-the-clock.json | screens[9] widget.tests[3] | warning | Test gap: `new = np.asarray(old, dtype=float)` (W20) aliases a float array `old` and overwrites the caller's centres, yet passes all 5 tests, because test 4 passes `old` as a list of lists, which `asarray` copies. The drill loop passes arrays. | Make test 4's `old` an `np.array` of floats; add W20 as a mutant on test 4.
- app/content/courses/ml-int/l8-a-layers-backward-pass.json | screens[8] widget.tests | warning | Test gap: a copy without a float dtype (W22) passes all 4 tests, but on an integer input every nudge truncates and the gradient is 0. The lesson's hint ("Copy x as a float array first") names the point, but no test checks it. | Add a test `mi_grad_check(lambda v: float((v ** 2).sum()), [1, 2]).tolist()` expecting `[2.0, 4.0]`; add W22 as a mutant.
- app/content/courses/ml-int/review-2.json | items[3] widget.wrong `with-self` | warning | Masking the query's own key plus the later ones also gives 3, which routes to `past` ("You masked the 3 earlier keys"), the wrong diagnosis. The `with-self` entry at 3.0001 is a placeholder no whole number reaches, and it has no byKey line. | Ask about row 2 of 6 instead: answer 4, `with-self` 5, `past` 1, each with its own line.
- app/content/courses/ml-int/l6-attention-from-scratch.json | objectives, screens[0] pace | note | The objective says "inside fifteen minutes" and screens[0] has pace 900, but the drill it leads to, and mi-sixty, give attention 20 minutes. | Make the objective "inside twenty minutes", or explain why the lesson pace is shorter.
- app/content/courses/ml-int/l6-attention-from-scratch.json | screens[5] explain | note | Zeroing after the softmax and then renormalising is mathematically correct (control W8 passes the drill). A strong candidate will say so, and the trap does not say why masking first is still the norm: it saves work and avoids exponentiating scores that will be thrown away. | Add one sentence to the explain.
- app/content/courses/ml-int/l6-attention-from-scratch.json | screens[11] option `flat` why | note | "Wastes B² work": one (BT) × (BT) score matrix costs B times the work of B separate T × T ones, not B². | "...needs a block mask and does B times the work."
- app/content/courses/ml-int/l7-k-means-against-the-clock.json | screens[6] prose | note | "Say the alternatives from l16" is ambiguous in a 12-lesson course. | "from `stat-learning` l16".
- app/content/courses/ml-int/l5-stable-softmax.json | screens[5] explain | note | "The smallest float64 is about 10^-308" is the smallest normal number (2.2 × 10^-308); subnormals reach 4.9 × 10^-324. e^-800 is below both, so the conclusion stands. | "The smallest positive float64 is about 5 × 10^-324".
- app/content/drills/mi-layernorm-backward.json | examples | note | Both examples pass `eps = 0.0`, while the constraints say eps is positive (range 10^-12 to 1). | Use `1e-5` in the examples.

## Level 3 (l9 to l12, review-3, homework-3, case.csv)

- app/content/courses/ml-int/l10-a-fair-comparison.json | screens[3] | error | Grading from the screen's own numbers fails. The mean 0.0414 and the standard error 0.0079 (screens[2]'s key; hint "0.0414/0.0079") give 5.24, but the key is 5.26 with tolerance 0.005, so a learner who follows the hint is marked wrong. 5.26 comes from the unrounded standard error 0.00787. | State the standard error as 0.00787 in the prose and hint (0.0414/0.00787 = 5.26), or widen the tolerance to 0.03.
- app/content/courses/ml-int/l10-a-fair-comparison.json | screens[4] | error | Same fault: 0.0436/0.0079 = 5.52, outside 5.53 ± 0.005. The unrounded standard error is 0.00789. | "mean difference 0.0436 and standard error 0.00789" (5.526, so 5.53).
- app/content/courses/ml-int/l11-when-the-net-wins.json | screens[2] | error | Same fault: -0.0233/0.0068 = -3.43, outside -3.45 ± 0.005. The unrounded standard error is 0.00676. | "standard error 0.00676" (-3.447, so -3.45). The same rounding appears in homework-3 items[3], which is consistent at its 4 decimal places.
- app/content/courses/ml-int/l10-a-fair-comparison.json | screens[2] explain, summary.formula.note, screens[7]; l12 screens[8]; quiz[2] | warning | Standard errors when daily errors are autocorrelated or overlap: the plain paired t is right for the case, as above. The course then applies the same test to 5-day returns (l10 quiz[2]), momentum P&L (l10 screens[8]) and credit spreads (l12 screens[8]) and never mentions a HAC (Newey-West) standard error. A strong interviewer expects one sentence on it, with h - 1 lags for an h-day target, as in the Diebold-Mariano test. World B seed 1 shows how fragile the verdict is: Newey-West with 5 lags (statsmodels HAC) gives t = -2.43 against the plain -1.91. | Add to screens[2] explain: "With an h-day target or autocorrelated daily errors, use a Newey-West standard error with at least h - 1 lags." Add one quiz item on the 5-day case.
- app/content/courses/ml-int/l10-a-fair-comparison.json | quiz[2], screens[10] explain; review-3 items[4] | warning | The purge rule disagrees with the prerequisite. `validation` l7 teaches that an h-day label needs `gap = h - 1`, which is 4 rows for 5-day returns and 346 training days. Here "a 5-day purge" for 5-day returns gives 345, which reads as the rule h. A learner who applies l7's rule (W24) fails `fair_split`'s test 1. Nothing says the case itself needs no purge: its target is one day ahead, so h - 1 = 0, which is why the homework-3 model answer trains on 350 days while the case order says "purged split". | In quiz[2]: "With a 4-day purge (h - 1, as `validation` l7)", key 346; or say that 5 keeps one spare day. In l10 screens[10] explain add: "The case's target is one day ahead, so h - 1 = 0 and all 350 earlier days train."
- app/content/courses/ml-int/l12-the-case-aloud.json | screens[3], quiz[1]; homework-3 items[1]; l10 screens[4]; l11 screens[4] explain | warning | "Seeds" means two different things. In the case a seed redraws the whole panel, which is a new market, and there is no such thing in practice. The interview follow-up "How many seeds would you run?" and `nn-train` l16 mean training seeds. Those measure only optimisation noise on one test period; eight training seeds with t ≥ 2 do not show the gap holds on new data. An interviewer will separate the two. | Add to l12 screens[3] explain: "Training seeds measure the model's own randomness on one period. Whether the gap holds needs fresh periods: walk-forward folds or live shadow days." Call the case's draws "worlds" or "draws" where the text means data.
- app/content/courses/ml-int/l10-a-fair-comparison.json | screens[5] explain, quiz[1] | warning | "Stocks on one day share market shocks, so the 15,000 rows hold about 150 independent pieces of evidence." That is true of markets but false of this case's panel. The generator has no day-level factor (noise is independent for each stock-day), so a pooled-row test on this data would be valid. A learner who checks finds the case contradicting its lesson. | Say "In real data, stocks on one day share market shocks..." or give the generator a common daily factor in a later level.
- app/content/courses/ml-int/l9-net-or-boosting.json | summary.formula, screens[9] (mutant "about 0"), homework-3 | warning | The out-of-sample R² benchmark is the test-period mean (`r2_score`), and dividing by the sum of squares about 0 is coded as a bug. In return forecasting the usual benchmark is zero (Gu, Kelly and Xiu 2020) or the historical training mean (Campbell and Thompson 2008). The test mean uses test-period information, which flatters nothing but is not available when you forecast. The interview answer should name the benchmark. | Add to screens[9] explain: "Return papers often measure R² against 0 or the training mean; the case uses the test mean, so say which." Keep the mutant, since it breaks this widget's stated spec.
- app/content/courses/ml-int/l11-when-the-net-wins.json | screens[6] prose and explain, option `tails`, summary.ideas[2] | warning | "Trees tend to win with ... heavy tails" and "single-feature splits ... are robust to outliers" mix up two things. Trees are invariant to monotone transforms of features, so outlying features do not hurt them. Heavy-tailed noise in the target hurts boosting with squared loss as much as any L2 model. Grinsztajn et al. name irregular targets, uninformative features and non-rotation-invariance, not target tails. | "...thresholds, many useless features, and features with heavy tails or odd scales", and key `tails` on features.
- app/content/courses/ml-int/homework-3.json | items[3] widget.wrong `z` | warning | The 1.96 slip is valued at -0.0101, computed from the unrounded inputs. With the numbers on screen, -0.0233 + 1.96 × 0.0068 = -0.00997, which is outside both the `z` band and the key band, so the "You used 1.96" line never shows. | Value -0.0100, tol 3 × 10^-5 (disjoint from the key band [-0.00995, -0.00985]).
- app/content/courses/ml-int/l9 to l12, review-3 | 20 choice items (validator `key-length`: l9 screens[4], [5], [6], [10]; l10 screens[7], [11], quiz[1]; l11 screens[3], [4], [7], quiz[2]; l12 screens[2], [5], [6], [7], [8], quiz[0], [2]; review-3 items[5], [7]) | warning | The keyed option is more than 1.5 times the longest distractor in 20 items, so the longest option gives the answer away. | Lengthen the distractors to similar specificity (each with its own number or condition), or trim the keys.
- app/content/courses/ml-int/homework-3.json | items[5] model | note | "with equal tuning" is generous: neither model was tuned (fixed settings for all four runs). An interviewer reading the note would ask how the settings were chosen. | "with fixed, untuned settings for both models".
- app/content/courses/ml-int/l10-a-fair-comparison.json | screens[7] prose | note | The interval's upper end is 0.0569 (from the unrounded figures), but the displayed sum 0.0414 + 1.976 × 0.0079 gives 0.0570. | Show 0.00787, or print 0.0570.
- app/content/courses/ml-int/l12-the-case-aloud.json | summary.formula, screens[3] | note | k ≥ (2s/ḡ)² treats 2 as the bar for any k; with 8 seeds the two-sided 5% point is t₀.₉₇₅,₇ = 2.36. | Add to the note: "With few seeds the t bar is above 2."
- app/content/courses/ml-int/l11-when-the-net-wins.json (prelude), docs/reports/ml-int-L3-numbers.py | case generator, MLPRegressor | note | `early_stopping=True` holds out a shuffled 10% of training rows. That is harmless here and inside the training period, but on real panels it is the shuffled-validation leak of `validation` l5. | One sentence in l11 screens[8] explain, or pass a time-ordered validation split in a later level.
- app/content/courses/ml-int/l11, l12, l6, l9 | l11 screens[1] `sign`, l12 screens[1] `A`, l6 screens[6] `zero`, l9 screens[1] `inverse` | note | Four `wrong` entries have no byKey line, so the learner sees only the generic message. | Add a short line for each.

## Number scripts (docs/reports/ml-int-L1 to L3-numbers.py)

- docs/reports/ml-int-L3-numbers.py | the claim "world B signal coefficients 0.5, 1.5 and 0.15 are the generator's" | note | The check reads the script's own source for a string that appears in the claim's own line, so it is always true (a fiat). It should compare against the l11 widget's `prelude`. | `lv.claim('0.5 * np.tanh(1.5 * u) + 0.15 * u * v' in l11_prelude, ...)` with `l11_prelude` read from `lv.files`.
- docs/reports/ml-int-L3-numbers.py | direct run | note | With default BLAS threads (4 cores) the direct run took over 100 s against 12 s single-threaded. The figures are identical. | Keep the docstring's `OPENBLAS_NUM_THREADS=1`; no change needed.
- all three scripts | coverage | note | The scripts compare each stated figure with the unrounded computation, which is why the three l10/l11 grading errors above passed: a key derived from on-screen rounded inputs is never recomputed. This is the first time this class appears here. | Engine idea (BACKLOG-INBOX): a numbers_lib helper that recomputes a numeric key from the rounded inputs the prose or hint shows and checks it lies within tolerance.

## Automated checks (no finding)

- Number scripts: 3 passed through the CI runner; strict coverage 0 uncovered in each; no dead `--write` branch (run under both thread settings, CSV identical, 600 rows, `var_y` about the test-period mean so day sums give `r2_score` exactly).
- L3 figures under scikit-learn 1.6.1: R² A0 0.0386 / 0.0282 / 0.0231, oracle 0.0411; A1 0.0342 / 0.0232 / 0.0184; B0 0.0331 / 0.0386 / 0.0336; B1 0.0231 / 0.0259 / 0.0254; t 5.26, 5.53, -3.45, -1.91; recomputed independently from `case.csv` (paired t by hand).
- Recomputed by hand and agreeing: every l1 forward and backward value, 0.9241 and its row (0.9241, 1.8483), 0.42; Adam 3.1623, 0.0526, 0.0005, 500.25, 25.49; He 0.0625, 0.125, 0.03125, Xavier 0.0442, 0.0221; ln 65, ln 27, ln 50,257; 8.037/8 and 2.32; softmax (0.0900, 0.2447, 0.6652), 1002.4076, 2.4076, 2.2395, -999.3069, 11.09, 435 digits; attention 0.3302, √8, 45, 0.5; k-means passes, (4, 4.25), 8/3, 200; l8 dX, dW, db, -1.5, 1.0908; homework values 0.899, -0.001, 0.0127, -0.1517, 1.3363, 4.29 billion, (0.625, 0.375); L3 0.94, 0.0155, 0.0051, 0.69, 0.0079, 0.25, 0.0055, 0.0023, 0.82, -0.0099, 345, 290, 8, 9.
- Tolerances: no key band overlaps a wrong band (grade-all); paces realistic (drills 10, 15, 20, 15, 20 and 30 minutes; mi-sixty two 20-minute drills in 60).
- Voice: 0 sentences over 35 words, 0 explanations over three sentences, no em-dashes, no exclamation marks, no American spellings ("license" appears only as the British verb).

## Appendix: own wrong solutions

29 solutions written for this read: 27 wrong and 2 correct controls. Each was run against the hidden tests natively (NumPy 2.0.2, scikit-learn 1.6.1, the page's comparison rules via `numbers_lib.ZQ_LIB`). Every survivor was then rerun in Pyodide 0.27.7 on a scratch copy of `app/`, as a planted solution (`planted-check.mjs`) or a mutant (`grade-all.mjs --code`). Survivors: W4, W20 and W22 (test gaps, warnings above) and W26 (an acceptable method). The task's named slips map to W1 (softmax without the max shift), W5 (no √d scale), W6 (mask on the wrong side), W14 and W15 (layer-norm backward missing the mean terms), W9 (an empty cluster), W11 (another start), W21 (a one-sided difference), and W23 and W25 (a split or score that leaks).

### W1 row softmax, no max shift

Target: `app/content/drills/mi-row-softmax.json`, `row_softmax`. Result: fails test 1 "Large logits" (nan row).

```python
import numpy as np


def row_softmax(z):
    e = np.exp(np.asarray(z, dtype=float))
    return e / e.sum(axis=1, keepdims=True)
```

### W2 row softmax, row max without keepdims

Target: `app/content/drills/mi-row-softmax.json`, `row_softmax`. Result: fails test 2 "Rows 1,000 apart" (the row maxima broadcast across columns).

```python
import numpy as np


def row_softmax(z):
    z = np.asarray(z, dtype=float)
    e = np.exp(z - z.max(axis=1))
    return e / e.sum(axis=1, keepdims=True)
```

### W3 cross-entropy, log of a clipped softmax

Target: `app/content/drills/mi-cross-entropy-logits.json`, `mean_cross_entropy`. Result: fails test 6 "A gap of 800, low class" (27.63 against 800).

```python
import numpy as np


def mean_cross_entropy(logits, targets):
    z = np.asarray(logits, dtype=float)
    t = np.asarray(targets)
    e = np.exp(z - z.max(axis=1, keepdims=True))
    p = e / e.sum(axis=1, keepdims=True)
    return float(np.mean(-np.log(np.clip(p[np.arange(len(t)), t], 1e-12, 1))))
```

### W4 cross-entropy, log-sum-exp shifted by the batch maximum

Target: `app/content/drills/mi-cross-entropy-logits.json`, `mean_cross_entropy`. Result: **SURVIVES** all 9 tests, natively and in Pyodide (`planted-check` on a scratch copy: "planted[3] passes all 9 hidden tests"); on `[[0, 1], [1000, 1001]]` it returns -inf.

```python
import numpy as np


def mean_cross_entropy(logits, targets):
    z = np.asarray(logits, dtype=float)
    t = np.asarray(targets, dtype=int)
    m = z.max()
    lse = m + np.log(np.exp(z - m).sum(axis=1))
    return float(np.mean(lse - z[np.arange(len(t)), t]))
```

### W5 attention without the sqrt(d_h) scale

Target: `app/content/drills/mi-causal-attention.json`, `causal_self_attention`. Result: fails test 1 "Two tokens by hand" (0.2689 against 0.3302).

```python
import numpy as np


def causal_self_attention(x, Wq, Wk, Wv, Wo, n_heads):
    x = np.asarray(x, dtype=float)
    T, d = x.shape
    dh = d // n_heads
    split = lambda A: (x @ np.asarray(A, dtype=float)).reshape(T, n_heads, dh).transpose(1, 0, 2)
    Q, K, V = split(Wq), split(Wk), split(Wv)
    S = Q @ K.transpose(0, 2, 1)
    S = S + np.triu(np.full((T, T), -np.inf), k=1)
    S = S - S.max(axis=2, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=2, keepdims=True)
    out = (A @ V).transpose(1, 0, 2).reshape(T, d)
    return out @ np.asarray(Wo, dtype=float)
```

### W6 attention with the mask on the wrong side (the past hidden)

Target: `app/content/drills/mi-causal-attention.json`, `causal_self_attention`. Result: fails test 1 "Two tokens by hand".

```python
import numpy as np


def causal_self_attention(x, Wq, Wk, Wv, Wo, n_heads):
    x = np.asarray(x, dtype=float)
    T, d = x.shape
    dh = d // n_heads
    split = lambda A: (x @ np.asarray(A, dtype=float)).reshape(T, n_heads, dh).transpose(1, 0, 2)
    Q, K, V = split(Wq), split(Wk), split(Wv)
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(dh)
    S = S + np.tril(np.full((T, T), -np.inf), k=-1)
    S = S - S.max(axis=2, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=2, keepdims=True)
    out = (A @ V).transpose(1, 0, 2).reshape(T, d)
    return out @ np.asarray(Wo, dtype=float)
```

### W7 attention, heads merged without the transpose

Target: `app/content/drills/mi-causal-attention.json`, `causal_self_attention`. Result: fails test 2 "The future stays hidden".

```python
import numpy as np


def causal_self_attention(x, Wq, Wk, Wv, Wo, n_heads):
    x = np.asarray(x, dtype=float)
    T, d = x.shape
    dh = d // n_heads
    split = lambda A: (x @ np.asarray(A, dtype=float)).reshape(T, n_heads, dh).transpose(1, 0, 2)
    Q, K, V = split(Wq), split(Wk), split(Wv)
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(dh)
    S = S + np.triu(np.full((T, T), -np.inf), k=1)
    S = S - S.max(axis=2, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=2, keepdims=True)
    out = (A @ V).reshape(T, d)
    return out @ np.asarray(Wo, dtype=float)
```

### W8 attention, mask after the softmax then renormalised (a correct variant, control)

Target: `app/content/drills/mi-causal-attention.json`, `causal_self_attention`. Result: passes, as it should (control: zeroing after the softmax and renormalising is equivalent).

```python
import numpy as np


def causal_self_attention(x, Wq, Wk, Wv, Wo, n_heads):
    x = np.asarray(x, dtype=float)
    T, d = x.shape
    dh = d // n_heads
    split = lambda A: (x @ np.asarray(A, dtype=float)).reshape(T, n_heads, dh).transpose(1, 0, 2)
    Q, K, V = split(Wq), split(Wk), split(Wv)
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(dh)
    A = np.exp(S - S.max(axis=2, keepdims=True)) * np.tril(np.ones((T, T)))
    A = A / A.sum(axis=2, keepdims=True)
    return (A @ V).transpose(1, 0, 2).reshape(T, d) @ np.asarray(Wo, dtype=float)
```

### W9 k-means, mean of an empty cluster (nan)

Target: `app/content/drills/mi-kmeans-fixed-start.json`, `kmeans_fixed_start`. Result: fails test 3 "An empty cluster" (nan centre).

```python
import numpy as np


def kmeans_fixed_start(points, k, max_iter):
    P = np.asarray(points, dtype=float)
    C = P[:k].copy()
    labels = None
    for _ in range(max_iter):
        new = ((P[:, None, :] - C[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
        if labels is not None and (new == labels).all():
            break
        labels = new
        C = np.array([P[labels == j].mean(axis=0) for j in range(k)])
    return C, labels, float(((P - C[labels]) ** 2).sum())
```

### W10 k-means, centres as a view of the points (no copy)

Target: `app/content/drills/mi-kmeans-fixed-start.json`, `kmeans_fixed_start`. Result: fails test 1 "Six points" (updating the view overwrites the first k points).

```python
import numpy as np


def kmeans_fixed_start(points, k, max_iter):
    P = np.asarray(points, dtype=float)
    C = P[:k]
    labels = None
    for _ in range(max_iter):
        new = ((P[:, None, :] - C[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
        if labels is not None and (new == labels).all():
            break
        labels = new
        for j in range(k):
            if (labels == j).any():
                C[j] = P[labels == j].mean(axis=0)
    return C, labels, float(((P - C[labels]) ** 2).sum())
```

### W11 k-means, a farthest-point start instead of the first k points

Target: `app/content/drills/mi-kmeans-fixed-start.json`, `kmeans_fixed_start`. Result: fails test 3 "An empty cluster".

```python
import numpy as np


def kmeans_fixed_start(points, k, max_iter):
    P = np.asarray(points, dtype=float)
    idx = [0]
    while len(idx) < k:
        d = ((P[:, None, :] - P[idx][None, :, :]) ** 2).sum(axis=2).min(axis=1)
        idx.append(int(d.argmax()))
    C = P[idx].copy()
    labels = None
    for _ in range(max_iter):
        new = ((P[:, None, :] - C[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
        if labels is not None and (new == labels).all():
            break
        labels = new
        for j in range(k):
            if (labels == j).any():
                C[j] = P[labels == j].mean(axis=0)
    return C, labels, float(((P - C[labels]) ** 2).sum())
```

### W12 linear-ReLU backward, db as the batch mean

Target: `app/content/drills/mi-linear-relu-backward.json`, `linear_relu_backward`. Result: fails test 6 "Central differences".

```python
import numpy as np


def linear_relu_backward(x, W, b, dout):
    x = np.asarray(x, dtype=float); W = np.asarray(W, dtype=float); b = np.asarray(b, dtype=float)
    dz = np.asarray(dout, dtype=float) * (x @ W + b > 0)
    return dz @ W.T, x.T @ dz, dz.mean(axis=0)
```

### W13 linear-ReLU backward, gate without the bias in Z

Target: `app/content/drills/mi-linear-relu-backward.json`, `linear_relu_backward`. Result: fails test 4 "A batch of one".

```python
import numpy as np


def linear_relu_backward(x, W, b, dout):
    x = np.asarray(x, dtype=float); W = np.asarray(W, dtype=float)
    dz = np.asarray(dout, dtype=float) * (x @ W > 0)
    return dz @ W.T, x.T @ dz, dz.sum(axis=0)
```

### W14 layer-norm backward missing both mean terms

Target: `app/content/drills/mi-layernorm-backward.json`, `mi_layernorm_backward`. Result: fails test 1 "dx".

```python
import numpy as np


def mi_layernorm_backward(x, gamma, dout, eps):
    x = np.asarray(x, dtype=float); g = np.asarray(gamma, dtype=float); dy = np.asarray(dout, dtype=float)
    mu = x.mean(axis=-1, keepdims=True)
    rs = 1 / np.sqrt(x.var(axis=-1, keepdims=True) + eps)
    xh = (x - mu) * rs
    dxh = dy * g
    dx = rs * dxh
    return dx, (dy * xh).sum(axis=0), dy.sum(axis=0)
```

### W15 layer-norm backward missing the mean of dx-hat (the mu term)

Target: `app/content/drills/mi-layernorm-backward.json`, `mi_layernorm_backward`. Result: fails test 1 "dx".

```python
import numpy as np


def mi_layernorm_backward(x, gamma, dout, eps):
    x = np.asarray(x, dtype=float); g = np.asarray(gamma, dtype=float); dy = np.asarray(dout, dtype=float)
    mu = x.mean(axis=-1, keepdims=True)
    rs = 1 / np.sqrt(x.var(axis=-1, keepdims=True) + eps)
    xh = (x - mu) * rs
    dxh = dy * g
    dx = rs * (dxh - xh * (dxh * xh).mean(axis=-1, keepdims=True))
    return dx, (dy * xh).sum(axis=0), dy.sum(axis=0)
```

### W16 layer-norm backward with the sample variance (ddof=1)

Target: `app/content/drills/mi-layernorm-backward.json`, `mi_layernorm_backward`. Result: fails test 1 "dx".

```python
import numpy as np


def mi_layernorm_backward(x, gamma, dout, eps):
    x = np.asarray(x, dtype=float); g = np.asarray(gamma, dtype=float); dy = np.asarray(dout, dtype=float)
    mu = x.mean(axis=-1, keepdims=True)
    rs = 1 / np.sqrt(x.var(axis=-1, ddof=1, keepdims=True) + eps)
    xh = (x - mu) * rs
    dxh = dy * g
    dx = rs * (dxh - dxh.mean(axis=-1, keepdims=True) - xh * (dxh * xh).mean(axis=-1, keepdims=True))
    return dx, (dy * xh).sum(axis=0), dy.sum(axis=0)
```

### W17 log_sum_exp_rows, row max without keepdims

Target: `app/content/courses/ml-int/l5-stable-softmax.json`, `log_sum_exp_rows`. Result: fails test 2 (two small rows).

```python
import numpy as np


def log_sum_exp_rows(z):
    z = np.asarray(z, dtype=float)
    m = z.max(axis=1)
    return m + np.log(np.exp(z - m).sum(axis=1))
```

### W18 sanity_checks, log of a stable softmax

Target: `app/content/courses/ml-int/l4-deep-learning-quickfire.json`, `sanity_checks`. Result: fails test 4 (the logit of 800 gives inf).

```python
import numpy as np


def sanity_checks(logits, targets):
    z = np.asarray(logits, dtype=float); t = np.asarray(targets)
    expected = float(np.log(z.shape[1]))
    e = np.exp(z - z.max(axis=1, keepdims=True))
    p = e / e.sum(axis=1, keepdims=True)
    actual = float(np.mean(-np.log(p[np.arange(len(t)), t])))
    return expected, actual, abs(actual - expected) > 0.5 * expected
```

### W19 mi_causal_mask as -inf times a 0/1 upper triangle

Target: `app/content/courses/ml-int/l6-attention-from-scratch.json`, `mi_causal_mask`. Result: fails test 1 (0 times -inf is nan below the diagonal).

```python
import numpy as np


def mi_causal_mask(T):
    return -np.inf * np.triu(np.ones((T, T)), k=1)
```

### W20 update_centres aliasing old (np.asarray, no copy)

Target: `app/content/courses/ml-int/l7-k-means-against-the-clock.json`, `update_centres`. Result: **SURVIVES** all 5 tests, natively and in Pyodide (`grade-all --code` on a scratch copy: mutant-passes); with `old` a float array it overwrites the caller's centres.

```python
import numpy as np


def update_centres(points, labels, old):
    P = np.asarray(points, dtype=float)
    new = np.asarray(old, dtype=float)
    labels = np.asarray(labels)
    for j in range(len(new)):
        if (labels == j).any():
            new[j] = P[labels == j].mean(axis=0)
    return new
```

### W21 mi_grad_check, one-sided forward difference

Target: `app/content/courses/ml-int/l8-a-layers-backward-pass.json`, `mi_grad_check`. Result: fails test 2 (742.2513 against 742.0658).

```python
import numpy as np


def mi_grad_check(f, x, eps=1e-6):
    x = np.array(x, dtype=float)
    g = np.zeros_like(x)
    base = f(x)
    for i in np.ndindex(x.shape):
        old = x[i]
        x[i] = old + eps
        g[i] = (f(x) - base) / eps
        x[i] = old
    return g
```

### W22 mi_grad_check, copy without a float dtype

Target: `app/content/courses/ml-int/l8-a-layers-backward-pass.json`, `mi_grad_check`. Result: **SURVIVES** all 4 tests, natively and in Pyodide; `mi_grad_check(lambda v: float((v ** 2).sum()), [1, 2])` returns `[0, 0]` because the int copy truncates every nudge.

```python
import numpy as np


def mi_grad_check(f, x, eps=1e-6):
    x = np.array(x)
    g = np.zeros(x.shape)
    for i in np.ndindex(x.shape):
        old = x[i]
        x[i] = old + eps
        up = f(x)
        x[i] = old - eps
        down = f(x)
        x[i] = old
        g[i] = (up - down) / (2 * eps)
    return g
```

### W23 fair_split with no purge (leaks an overlapping label)

Target: `app/content/courses/ml-int/l10-a-fair-comparison.json`, `fair_split`. Result: fails test 1 (trains on day 6, inside the purge).

```python
import numpy as np


def fair_split(n_days, n_test, purge):
    return list(range(0, n_days - n_test)), list(range(n_days - n_test, n_days))
```

### W24 fair_split that purges h - 1 days (validation l7 rule)

Target: `app/content/courses/ml-int/l10-a-fair-comparison.json`, `fair_split`. Result: fails test 1 (the widget defines `purge` as days dropped; see the l10 purge finding).

```python
import numpy as np


def fair_split(n_days, n_test, purge):
    return list(range(0, n_days - n_test - max(purge - 1, 0))), list(range(n_days - n_test, n_days))
```

### W25 small_panel_compare, SST about the full-sample mean (test mean leaks training days)

Target: `app/content/courses/ml-int/l11-when-the-net-wins.json`, `small_panel_compare`. Result: fails test 1 (ridge 0.02334 against 0.02222).

```python
import numpy as np


from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import Ridge


def small_panel_compare(world, seed, assets, days):
    X, y, sig = panel(world, seed, assets, days)
    n_tr = days - days * 3 // 10
    Xtr, ytr = X[:n_tr].reshape(-1, X.shape[2]), y[:n_tr].ravel()
    Xte, yte = X[n_tr:].reshape(-1, X.shape[2]), y[n_tr:].ravel()
    sst = np.sum((yte - y.mean()) ** 2)
    r2 = lambda p: float(1 - np.sum((yte - p) ** 2) / sst)
    models = {'boost': HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, max_leaf_nodes=15, random_state=0),
              'mlp': MLPRegressor(hidden_layer_sizes=(32, 32), alpha=1e-3, max_iter=300, early_stopping=True, random_state=0),
              'ridge': Ridge(alpha=1.0)}
    out = {k: r2(m.fit(Xtr, ytr).predict(Xte)) for k, m in models.items()}
    out['oracle'] = r2(sig[n_tr:].ravel())
    return out
```

### W26 min_norm_test_error via ridge with lambda 1e-8 (normal equations)

Target: `app/content/courses/ml-int/l3-double-descent.json`, `min_norm_test_error`. Result: **SURVIVES** all 5 tests, natively and in Pyodide; acceptable, since ridge as lambda goes to 0 is the minimum-norm fit (not counted as a defect).

```python
import numpy as np


def min_norm_test_error(p, seed):
    X, y, Xt, yt, W = make_data(seed)
    F = np.maximum(X @ W[:, :p], 0)
    Ft = np.maximum(Xt @ W[:, :p], 0)
    beta = np.linalg.solve(F.T @ F + 1e-8 * np.eye(p), F.T @ y)
    return float(np.mean((Ft @ beta - yt) ** 2))
```

### W27 adam_first_step as lr * sign(g), epsilon ignored

Target: `app/content/courses/ml-int/l2-why-adam.json`, `adam_first_step`. Result: fails test 2 (0.001 against 0.00099990).

```python
import numpy as np


def adam_first_step(g, lr, beta1, beta2, eps, corrected):
    g = np.asarray(g, dtype=float)
    r = (1 - beta1) / np.sqrt(1 - beta2)
    return lr * np.sign(g) * (1.0 if corrected else r)
```

### W28 case_report with an unpaired (two-sample) t

Target: `app/content/courses/ml-int/homework-3.json`, `case_report`. Result: fails test 1 (all four verdicts "no change").

```python
import numpy as np


import pandas as pd


def case_report(df):
    out = {}
    for (w, s), g in df.groupby(['world', 'seed']):
        rep = {m: float(1 - g['mse_' + m].sum() / g['var_y'].sum()) for m in ('boost', 'mlp', 'ridge')}
        a, b = g['mse_mlp'].to_numpy(), g['mse_boost'].to_numpy()
        t = float((a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)))
        rep['t'] = t
        rep['verdict'] = 'network' if t <= -2 else ('boosting' if t >= 2 else 'no change')
        out[(w, int(s))] = rep
    return out
```

### W29 two_layer_grads with the gate taken from a > 0 (a correct variant, control)

Target: `app/content/courses/ml-int/l1-backprop-on-a-whiteboard.json`, `two_layer_grads`. Result: passes, as it should (control: `a > 0` and `h > 0` agree).

```python
import numpy as np


def two_layer_grads(x, W1, w2, y):
    a = np.maximum(W1 @ x, 0)
    dy = w2 @ a - y
    return 0.5 * dy ** 2, np.outer(dy * w2 * (a > 0), x), dy * a
```

## Fix pass

Branch `fix-ml-int` from `claude/inspiring-dirac-ckxdoa`. 40 fixed, 1 partly fixed with the rest deferred, 1 needing no change, 0 declined. Graded answers changed: 1 (l10 quiz[2], 345 to 346); the three l10 and l11 keys keep their values, with more inputs shown and a wider tolerance. Purge rule: `validation` l7 is right (row t's label uses days t + 1 to t + h, so h - 1 rows overlap); `ml-int` now uses h - 1, so there is nothing to record for the audit session.

### Level 1

1. l3 screens[5]: fixed. Option `dd` now says the decomposition still holds and variance peaks at p = n and falls past it; hint, explain and the `agree` line say the same.
2. l3 screens[7]: fixed. The prose says p = n here and, for a deep net, effective complexity about n; the `data` line cites sample-wise non-monotonicity.
3. l3 screens[0] to [6]: partly fixed, rest deferred. The missing interview points are added (bias-variance in screens[5], effective complexity and sample-wise descent in screens[7], gradient descent from zero reaching the smallest-norm fit in screens[3]); the merge of screens[1] to [3] is deferred, because it moves screen indexes that the number script and the playthrough key on.
4. l3 quiz[2]: fixed. The `var` line and the explain now say the noise part does quadruple (0.0185 to 0.0763, 4.1 times) on top of a 0.0461 floor; the figures are recomputed in `ml-int-L1-numbers.py` (noise 0 rerun, 20 seeds).
5. l3 screens[8]: fixed, "out-of-sample R² under 1 per cent" in the option and the explain.
6. l3 screens[1]: fixed. The norms are shown as 1.166 and 10.14 (unrounded 1.1658 and 10.1408), so 10.14/1.166 = 8.7 is true as printed; key unchanged.
7. l2 objectives and screens[7]: fixed with a new quiz[3] on choosing SGD with momentum; the Wilson, Reddi and warm-up points are in the options and whys.
8. l4 screens[10] `test-4`: fixed, "A logit of 800 overflowed."
9. l2 screens[3]: fixed, "RMSProp with momentum has no correction".
10. l3 screens[4]: fixed, the no-noise peak of about 2.5 is added (computed: 2.4989).
11. l4 screens[6]: fixed, "In a fully connected layer".
12. l4 screens[9]: fixed, "divided by the wrong count, for example by V as well".

### Level 2

13. l8 screens[4] `sign`: fixed. The path through Z₂,₁ gives -2 and the kink adds +1/2, total -1.5.
14. mi-cross-entropy-logits: fixed. New test "Rows 1,000 apart" (0.8132616875182228) and a planted batch-maximum solution; `planted-check` 0 failures with `--near-miss --require` (the existing near miss is kept as the one near miss).
15. l7 screens[9] test 4: fixed. `old` is now a float `np.array`; the `np.asarray` aliasing solution is recorded as a mutant on test 4.
16. l8 screens[8]: fixed. Test 5 `mi_grad_check(..., [1, 2])` expects [2.0, 4.0]; the no-dtype copy is a mutant on test 5, with a byKey line.
17. review-2 items[3]: fixed. It asks about row 2 of 6: answer 4, `past` 1, `with-self` 5, each with its own line; the script checks all three.
18. l6 objective: fixed, "inside twenty minutes, the pace of the drill after it"; the screen's own prose already says the lesson takes fifteen.
19. l6 screens[5]: fixed, one sentence on zeroing after the softmax and why masking first is the norm.
20. l6 screens[11] `flat`: fixed, "does B times the work".
21. l7 screens[6]: fixed, "`stat-learning` l16".
22. l5 screens[5]: fixed, "smallest positive float64 is about 5 × 10^-324" (checked with `nextafter`).
23. mi-layernorm-backward examples: fixed. They use eps = 1e-5; the first example's dx is 0 only up to a term of order eps (about 5e-6), so its tolerance is 1e-4 and the note says so.

### Level 3

24. l10 screens[3]: fixed. The prose and hint show 0.00787 (0.0414/0.00787 = 5.2605); the tolerance is 0.03 so the 0.0079 route (5.24) is accepted too. The script divides the displayed inputs both ways and checks the tolerance.
25. l10 screens[4]: fixed. Standard error 0.00789 (0.0436/0.00789 = 5.526); tolerance 0.03 (the 0.0079 route gives 5.52).
26. l11 screens[2]: fixed. Standard error 0.00676 (-0.0233/0.00676 = -3.447); tolerance 0.03 (0.0068 gives -3.43).
27. Newey-West: fixed. l10 screens[2] explain says the plain error is right here and an h-day target or autocorrelated errors need a Newey-West (HAC) error with at least h - 1 lags; also in the formula note, screens[8], l12 screens[8] and a new l10 quiz[3]. Recomputed (statsmodels HAC and a hand Bartlett kernel agree): world B seed 1, 5 lags, t = -2.43 against the plain -1.91, so the verdict goes from no change to the network (4 lags give -2.31, also past 2); the quiz explain says so.
28. Purge rule: `validation` l7 is correct and `ml-int` was one day over. l10 quiz[2] now uses a 4-day purge (h - 1), key 346, with a `h` slip at 345; the `fair_split` tests use purge 4 (346 and 345 to 350); screens[10] explain says a 5-day label needs h - 1 = 4 and this case's one-day target needs 0, so 350 days train; review-3 items[4] states the h - 1 rule (answer 290 unchanged).
29. l12 screens[3] and l10/l11: fixed in the places the text means data. l12 screens[3] explain separates training seeds from fresh periods; l10 screens[4] says a second seed is a new market, which real data never offers; l11 screens[3] and [4] say "draw".
30. l10 screens[5] and quiz[1]: fixed. The explain and the `corr` option say "in real data", and the explain says this generator draws each stock-day separately.
31. l9 screens[9] and the formula note: fixed, one sentence on the benchmark (0, the training mean or the test mean); the mutant stays.
32. l11 screens[6], option `tails`, summary: fixed. Trees win on thresholds, useless features and features with heavy tails or odd scales; the key is on features.
33. homework-3 items[3] `z`: fixed. Value -0.0100, tolerance 3e-5 (the slip is -0.009972 from the shown inputs; the key band is [-0.00995, -0.00985]); the script checks both from the displayed inputs.
34. The 20 key-length items: fixed. Each distractor was lengthened to a similar specificity (one new condition or number each) and no item has a key over 1.5 times the longest distractor; the validator shows no `[key-length]` on ml-int.
35. homework-3 items[5] model: fixed, "fixed, untuned settings for both models".
36. l10 screens[7]: fixed, "0.04139 ± 1.976 × 0.00787" gives (0.0258, 0.0569) as printed.
37. l12 formula note and screens[3]: fixed, "With few seeds the t bar is above 2", and the explain gives 2.36 for 8 seeds (t quantile, 7 degrees of freedom).
38. l11 screens[8] explain: fixed, one sentence on the shuffled early-stopping validation set.
39. The four `wrong` entries without a byKey line: fixed (l11 screens[1] `sign`, l12 screens[1] `A`, l6 screens[6] `zero`, l9 screens[1] `inverse`).

### Number scripts

40. L3 world B signal claim: fixed. It now reads the l11 widget's `prelude`.
41. L3 BLAS threads: no change, as the review says.
42. Rounded-input coverage: fixed locally. `ml-int-L3-numbers.py` has a `from_shown` check for the three keys and homework h4; the general helper is raised in `docs/BACKLOG-INBOX.md`.

### Checks

Validator 0 errors, no `[ai-mutants]` or `[source-ban]` on ml-int; `voice-scan.py 35` 0 and 0; the three number scripts pass through the CI runner and directly with `ZQ_NUMBERS_STRICT=1`; `grade-all.mjs --code --strict-feedback` 0 failures on every edited file; `planted-check.mjs --near-miss --require` 0 failures on the two edited drills; `same-course-reuse.mjs --all` lists nothing for ml-int.
