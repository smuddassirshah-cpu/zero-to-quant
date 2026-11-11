# stat-learning level 4 (Other learners): second-reader findings

Scope: `l15-widest-street`, `l16-groups-nobody-labelled`, `l17-a-small-network`, `l18-bending-the-line`, `l19-which-learner`, `review-4`, `homework-4` in `app/content/courses/stat-learning/`. Continuity: prerequisites `stat-learning` L1 to L3 (`multivar` L2 is diagnostic only), the later courses `ensembles` and `validation`, exam `topic-2.1`.

Method: every screen and item worked from its text before its answer was read. Scripts in `docs/reviews/stat-learning-4-scripts/`:

- `read-numbers.py`: every key, `wrong[]` value and stated number recomputed by a second route (exact fractions and exhaustive search for the hand examples, a direction search for the widest street, normal equations for the hinge fits, bisection for the saving curve, scikit-learn 1.6.1 for the fits), plus probes of each general claim (20 further seed pairs for the wide row, 200 single starts for raw k-means, a unit change for each learner, a reused pipeline).
- `run-code.py`: each of the 13 `code` widgets run in CPython under the engine's comparison rule: author solution, starter, the reader's own independent solution, and 99 wrong solutions a learner writes (no scaling, a scaler fitted on all rows, the wrong `random_state`, permuted labels, test or seen rows used in tuning, and the slips of each formula).
- `pyodide-network.mjs`: the stated network figures recomputed in the local Pyodide 0.27.7 build (node).
- `dump.py`: the reader used to print each file.

Format: `N. file | screen or item | tag | what is wrong | fix`. Tags: `wrong` = a wrong number, a false statement or wrong grading; `unclear` = teaching that misleads, states a conditional result without its condition, or is true only of the lesson's data; `minor` = wording, coverage, freshness, test strength.

## Tool results

- Author scripts: `docs/reports/stat-learning-L4-numbers.py` exit 0, 378 of 378 checks; `docs/reports/stat-learning-4-perf-numbers.py` exit 0, 0 failures.
- Reader script `read-numbers.py`: 129 of 138 checks pass; exit 1. The nine failing checks (each printed with `CONTENT`) are findings 5, 6, 7, 12, 13, 14, 24, 27 and 31 below and pass once those are fixed.
- `run-code.py`: exit 0. All 13 code widgets: author solution passes, starter fails, reader's solution passes. Of 99 wrong solutions, 90 are caught, 2 are harmless (no rounding inside a band; stopping on unmoved centres) and 7 pass: one in l16 s4 (finding 11), three in l17 s8 (finding 18), one in l19 s7 (finding 24, the reused model), one in l19 s8 (finding 26, the one that matters), and in l18 s7 a scaler fitted on training and test rows before the splines, which changes nothing because the spline basis ignores an affine change of units.
- `pyodide-network.mjs`: every network figure the lessons state is the Pyodide value (width sweep 0.6567, 0.6467, 0.82, 0.97, 0.97; seeds 0.97, 0.9667, 0.96; noise 0.5833/0.5567, 0.6033/0.5, 0.65/0.4967; l19 column 0.9567, 0.9733, 0.8467, 0.9067, 0.5367; seed pairs 0.9733, 0.9567). CPython differs in the cells the report marks, and in the noise table by more than the lesson says (finding 13).
- Validator: 0 errors; 51 advisory warnings on these files (point hints without a highlight, ladder canvas changes, sentences of 20 to 34 words).
- Voice scan (`voice-scan.py 35`): 0 explanations over three sentences, 0 sentences over 35 words. No exclamation mark or em-dash; spelling British; £ where money appears; no option named by place.
- Playthrough with `--local-cdn`: five lessons, `review-4` and `homework-4` pass, with and without `--mobile` (14 runs, one at a time), so every code test, the network bands and the scikit-learn `KMeans` comparisons hold in Pyodide. Shots at 440 px read for l16 s7 and l19 s3 (finding 30).
- `fresh-check --file`: 0 hits on `review-4` and `homework-4`. `perf-reports.mjs`: 0 missing parts.

## Statements checked (reader's own source or derivation)

Reference: James, Witten, Hastie, Tibshirani, Taylor, An Introduction to Statistical Learning with Applications in Python (ISLP), chapters 7, 9, 10 and 12.

- Maximal margin classifier (ISLP 9.1.3, 9.1.4): distance $|w \cdot x + b|/\lVert w \rVert$, free scale, margin $1/\lVert w \rVert$, minimise $\lVert w \rVert$ under $s_i(w \cdot x_i + b) \ge 1$: correct, with the condition (separable classes) stated and broken in quiz q3. Six loans rechecked by a search over 180,000 directions: street $2\sqrt{2}$, support vectors $(1,1)$, $(2,0)$, $(3,3)$; the moved point gives slope $-0.75$, street 2.5. Homework's six points: $x_1 + x_2 = 6$, margin $3/\sqrt{2}$, four points on the edges.
- Support vector classifier and $C$ (ISLP 9.2): scikit-learn's $C$ is a price per unit of slack, so small $C$ is the wide street; the lesson's direction is right for scikit-learn. ISLP's $C$ (equation 9.15) is a budget and runs the other way; the lesson does not say so (finding 1). "Each point inside the street is a support vector" is correct (points on or inside the margin).
- Kernels (ISLP 9.3.2): the explicit column $x_1^2 + x_2^2$ and the RBF kernel, $\gamma$ as reach, decision function $\sum_i \alpha_i y_i K(x, s_i) + b$ equal to `dual_coef_` and `intercept_`: correct, rechecked against `decision_function`. `decision_function` as a signed distance in margins, not a probability: correct for the linear kernel the quiz describes.
- k-means (ISLP 12.4.1, algorithm 12.2): objective, both steps non-increasing, finitely many groupings, local optimum, `n_init`, scaling: correct. The best inertia for $k = 1$ to 4 rechecked by exhaustive search (790, 64, 10, 4). Two statements need their condition: findings 7 and 8.
- Hierarchical clustering (ISLP 12.4.2): single, complete and average linkage, heights, cuts: correct, rechecked with SciPy. That the left-to-right order of leaves carries no meaning is not said (finding 9).
- Networks (ISLP 10.1, 10.2, 10.7): hidden layer as features, ReLU, logistic output, $ab + b$ parameters, chain-rule slopes (rechecked by finite differences: $-4$, $-1$), the overshoot at step 0.5, a dead unit, no activation collapses to one linear map ($w_2 W_1 = (3, 5)$): correct. No claim that a network always beats a linear model. Noise table: findings 13 and 14.
- Splines (ISLP 7.4): hinge basis, continuity, running-sum slopes, $K + 4$ degrees of freedom for a cubic spline, `SplineTransformer` giving `n_knots + degree - 1` columns: correct. Natural splines are not mentioned (finding 20). The ridge-on-spline explanation misdescribes what the penalty does (finding 19).
- Additive models (ISLP 7.7): one least-squares fit on stacked bases, each $f_j$ readable, no interaction by construction: correct, and "no number of knots repairs it" holds (0.3292, 0.2373, 0.172).
- Comparison (ISLP 2.2, 4.5): no leakage in the lesson's own code. Every scaler sits inside a pipeline fitted on training rows only; `pick_gamma` and `choose_on_validation` carve validation rows from the training rows, refit, and touch the test rows once. The table's settings are fixed in advance, not tuned on test rows. Two general statements fail: findings 23 and 27.

## Findings

### l15-widest-street

1. `l15-widest-street.json` | screens[4] explain | unclear | The level's reference defines $C$ the other way: in ISLP (9.15) $C$ is a budget for slack, so a large $C$ gives the wide street. A learner who opens the book meets the opposite rule with no warning. | Replace the first sentence of `explain.text` with: "$C$ is a penalty, like the ridge penalty, but large $C$ means a weak penalty on $\lVert w \rVert$; textbooks that call $C$ a budget for intrusions, as ISLP does, run the other way."
2. `l15-widest-street.json` | screens[1] explain | unclear | "the other three loans could move anywhere outside the street without effect" is false as written: a default moved beyond the repaid edge is outside the street and breaks it. | "...and the other three loans could move anywhere on their own side, outside the street, without effect."
3. `l15-widest-street.json` | screens[0] prose | minor | "Logistic regression would pick yet another line" holds only with a penalty: on separable classes the unpenalised fit has no finite answer, and the line scikit-learn returns depends on its `C`. | "Logistic regression with its default penalty would pick yet another line."
4. `l15-widest-street.json` | screens[3] explain | minor | "rests on three different loans" reads as three new loans; two of them, $(2, 0)$ and $(3, 3)$, are the same as before. | "...has margin 0.5 and rests on $(2, 0)$, $(3, 3)$ and $(3, 5)$."

### l16-groups-nobody-labelled

5. `l16-groups-nobody-labelled.json` | screens[2] widget.wrong[0] `unsq` | wrong | The entry's value is 12, but its own feedback writes the slip as $2 + 0 + 2 + 4 + 2 + 6$, which is 16. A learner who adds plain distances types 16 and gets the generic line; 12 is quiz q4's value for one group. | `"value": 16`.
6. `l16-groups-nobody-labelled.json` | screens[1] widget.wrong `half` | wrong | Halfway from 10 to 12 and from 25.6 to 34 is 11 and 29.8, not "11, 29". The entry never fires for the slip it names. | `"value": "11, 29.8"`.
7. `l16-groups-nobody-labelled.json` | screens[5] options[2].why and feedback.byKey.c | wrong | "Ten starts found the lowest raw inertia" is false. `KMeans(3, n_init=10, random_state=0)` on the raw columns stops at 842.33; 200 single starts, or `n_init=50`, reach 842.15, with purity 0.7333. The teaching point survives and is sharper: more starts make the planted groups worse. | `why`: "You blamed the starts. Fifty starts lower the raw inertia a little, from 842.33 to 842.15, and purity falls to 0.73: the raw inertia itself rewards the wrong cut." `byKey.c`: "That is the trap: more starts minimise the same raw inertia, which is dominated by volatility, and purity falls to 0.73. Scaling changes the objective; starts do not."
8. `l16-groups-nobody-labelled.json` | summary.formula.note; quiz[0] options[0] and explain | unclear | "It always falls as $k$ grows" is true of the best inertia for each $k$. One run can stop in a local minimum, as screen 3 shows, so a computed curve need not fall at every step. | Note: "The best inertia never rises as $k$ grows; look for an elbow, not a minimum." Quiz explain, second sentence: "The best inertia falls for every extra $k$, even on noise."
9. `l16-groups-nobody-labelled.json` | screens[7] explain | minor | Reading a dendrogram (ISLP 12.4.2): only heights carry meaning; the left-to-right order of leaves does not. Not taught anywhere in the level. | Replace the last two sentences with: "The linkage and the height of the cut are choices that change the answer. Only heights mean anything: leaves drawn side by side need not be close."
10. `l16-groups-nobody-labelled.json` | screens[10] explain | minor | "after a cointegration test" uses a term no prerequisite teaches (it first appears in `arma`, `coint` and `pairs-rep`). | "...a pair is worth trading only after its spread is tested, on data the clustering never saw, for pulling back to a steady level."
11. `l16-groups-nobody-labelled.json` | screens[4] tests | minor | A `kmeans_step` that assigns by Manhattan distance passes all nine tests (the only 2-D case agrees under both distances). | Add `{"call": "kmeans_step([[0, 0], [0, 6], [4, 3]], [[0, 5], [3, 3]])[0].tolist()", "expect": "[1, 0, 1]", "compare": "equal"}` (Manhattan gives `[0, 0, 1]`) and make `how` say 10 tests.

### l17-a-small-network

12. `l17-a-small-network.json` | quiz[1] widget.wrong `order` | wrong | The entry's value is 6, but the wrong order, $W_1 w_2$, has second entry $0 \times 3 + 1 \times (-1) = -1$. The value 6 is $3 \times 2$ with the term $(-1) \times 1$ dropped, a different slip. | Two entries: `{"id": "order", "value": -1}` with the present feedback ending "...the second entry is $3 \times 2 + (-1) \times 1$.", and `{"id": "dropped", "value": 6}` with "You stopped at $3 \times 2$. The second hidden unit adds $(-1) \times 1$."
13. `l17-a-small-network.json` | screens[9] explain | wrong | "The exact values move in the third place on another runtime" is false for this table. CPython gives test accuracy 0.5667, 0.4867, 0.4967 against the lesson's 0.5567, 0.5000, 0.4967: moves of 0.010 and 0.013, in the second place. (On the rings the claim is true: 0.97 against 0.9733.) The conclusion still holds on both runtimes and over the whole range 0.49 to 0.57: every test score is within $0.6$ standard errors ($0.0287$) above the 0.55 base rate, or below it. | Last sentence: "On another runtime the scores move by up to four rows in 300; the conclusion does not."
14. `l17-a-small-network.json` | screens[9] options[0] | unclear | "test accuracy sits at or below the 0.55 base rate": seed 0 scores 0.5567, two rows above it (five rows in CPython). The key is right in substance but its wording is not true of the table beside it. | "Nothing: test accuracy is within two rows of the 0.55 base rate or below it; the training edge is fitted noise".
15. `l17-a-small-network.json` | screens[8] prose | minor | "from the playthrough's runtime" is build jargon the learner has never met. Also, the screen fits on unscaled features with no reason given, while the summary says a network needs scaled features. | "The bars show test accuracy as this app's Python computes it. Both features are already on one scale, so we skip the scaler here."
16. `l17-a-small-network.json` | screens[0] explain | minor | "Logistic regression draws a line too, so it is stuck at the same 0.75" states a ceiling as a result. Fitted to these four corners every weight is 0 by symmetry and it scores 0.5. | "Logistic regression draws a line too, so 0.75 is its ceiling as well."
17. `l17-a-small-network.json` | screens[4] explain | minor | "A one-input layer of 3 to 1" is garbled. | "A single layer from 3 units to 1 has $3 + 1 = 4$ parameters."
18. `l17-a-small-network.json` | screens[8] tests | minor | Bands cannot tell these wrong solutions from the key: `random_state` ignored (always 0), default `alpha`, a scaler fitted on training and test rows together. All three pass. Acceptable for a network, but `how` should not suggest the seed is checked. | In `how`, end with: "The bands cannot check your seed or penalty: read your call against the comment."

### l18-bending-the-line

19. `l18-bending-the-line.json` | quiz[2] explain | unclear | A ridge penalty on the spline columns does not penalise wiggle; it pulls every coefficient towards zero, so the fitted curve is pulled towards its mean level. That is why 40 knots with $\alpha = 1$ score 0.8868: the fit is flattened (12.3 bp at 1% where the 5-knot fit gives 9.8; 61.0 at 40% against 62.5), not "too smooth". The smoothing spline of ISLP 7.5 penalises curvature, which leaves a straight trend untouched. | `explain.text`: "A ridge penalty pulls every spline coefficient towards zero, so the curve wiggles less but is also flattened towards its mean: 40 knots with a penalty of 1 gave test $R^2$ 0.8868. A **smoothing spline** penalises curvature instead, with a knot at every point, so it damps wiggle without flattening a trend. Either penalty is tuned on validation, like $k$." Correct option text: "It shrinks the coefficients, so the curve wiggles less but flattens too; tune its size on validation".
20. `l18-bending-the-line.json` | quiz[1] explain | minor | Natural splines (ISLP 7.4.3), the standard answer to the boundary, are never named; `extrapolation="linear"` is not one (it extends the tangent, with no constraint inside the data). | Add as the explanation's second sentence, replacing "but only by luck of shape": "The spline's linear tail is closer to the truth, 85.13 against 74.16, by luck of shape; a **natural spline** goes further and is forced to be linear beyond its boundary knots."
21. `l18-bending-the-line.json` | screens[3] widget | minor | The question asks two things and takes one number; a learner who answers the first, 3, gets the generic line. | Add `{"id": "interior", "value": 3, "tol": {"abs": 0}}` with "You gave the interior knots, $K = 3$. Add 4 for the basis functions."
22. `l18-bending-the-line.json` | screens[10] prose | minor | The saving $\hat f(s) - \hat f(s/2)$ assumes the first half's impact has faded before the second half trades; stated without the condition. | After "instead of $\hat f(s)$" add: ", if the first half's impact has faded before the second trades".

### l19-which-learner

23. `l19-which-learner.json` | screens[5] prose | wrong | "Each score is 1 minus a test error, and a test error splits as $E[\text{error}] = \text{bias}^2 + \text{variance} + \text{noise}$." That split is for squared error (ISLP 2.2.2, equation 2.7, and this course's l3). The scores here are accuracies; a misclassification rate has no such additive split. | "The whole table. Level 1 split a squared error into bias, variance and noise; an accuracy does not split into an exact sum, but the same three forces decide each cell."
24. `l19-which-learner.json` | screens[7] explain | wrong | "reusing one fitted object would carry state between problems" is false for scikit-learn: `fit` starts again each time. A `fit_table` that builds each learner once and refits it for every problem passes all five tests with identical cells. | "Building a model per cell keeps the cells independent of each other. The deterministic cells match to 4 places in any runtime. The network cell is tested only within a band."
25. `l19-which-learner.json` | screens[3] options[2].why | wrong | "behind both linear-boundary learners": the table has one learner with a linear boundary. The SVM here is RBF, and the additive model is not linear either. | "You expected parameter count to decide. The network scored 0.9067, behind logistic regression and the SVM."
26. `l19-which-learner.json` | screens[8] tests | wrong | The tests accept the leak the screen teaches against. A solution that fits each learner on all training rows and "validates" on the last `n_val` of them (rows it has seen) passes all five tests. | Add `{"call": "list(choose_on_validation(*PROBLEMS['street'], {'logistic': LEARNERS['logistic'], 'knn1': lambda: make_pipeline(StandardScaler(), KNeighborsClassifier(1))}, 100))", "expect": "['logistic', 0.9633]", "compare": "isclose"}`: 1-nearest neighbour scores 1.0 on rows it has seen, so the leaking solution returns `('knn1', 0.93)`. Make `how` say 6 tests, "and one with a learner that memorises".
27. `l19-which-learner.json` | screens[3] explain; summary.ideas[1] | unclear | "Few rows and many noisy features favour the simplest learner" is true of this seed pair by two rows. Over 20 further seed pairs of `make_wide` the additive model averages 0.930 and logistic regression 0.924, and the additive model is best in 11 of 20. The robust half of the claim is the other one: nearest neighbours is worst in 18 of 20 (mean 0.865). | Explain: "Few rows and many noisy features hurt the distance-based learner most, 0.89: neighbours in 20 dimensions are mostly neighbours in noise. Logistic regression leads here, 0.9233, with the SVM and the additive model within two rows. On other samples those three swap places; nearest neighbours stays last." Summary: "Few rows per feature and heavy noise punish distance-based learners and reward a penalised, simple one; on pure noise every learner sits at the base rate."
28. `l19-which-learner.json` | screens[1] explain | minor | "The additive model wins here" by one row in 300, which quiz q1 then calls noise. | "The additive model manages it because $x_1^2 + x_2^2$ is a sum of one-feature curves."
29. `l19-which-learner.json` | whole lesson | minor | The brief's ladder step, placing the five learners on the bias and variance axis of l3, is absent (screen 5 is a choice about what decides). Cost and explainability get one clause. | Either add a `place` or `order` screen for the two ends (logistic regression as most bias, 1-nearest neighbour or the $\gamma = 1000$ machine as most variance, with the note that each learner's settings move it along the axis) or record the omission in `docs/reports/stat-learning-4.md`.
30. `l19-which-learner.json` | screens[0] to [3] canvas | minor | At 440 px the hidden bars print "0.00" over each learner beside "Hidden until you answer.", which reads as five scores of zero. | Set `showValues` false in the hidden state and true in `explain.canvas`, if `bars` allows a state change of `showValues`; otherwise see Engine.

### review-4

31. `review-4.json` | `r-few-rows` options[3].why | wrong | "You added 250 spline columns to 80 rows." By the level's own rule `SplineTransformer(n_knots=10)` gives $10 + 3 - 1 = 12$ columns a feature, so 25 features give 300. | "You added 300 spline columns to 80 rows. That is far more columns than rows."

### homework-4

32. `homework-4.json` | `h-kmeans` prose | unclear | "Stop when an assignment repeats the previous one, or after `max_iter` assignments" does not say whether the update after the last assignment is made. The tests need it (centres 10 and 25.6, inertia 587.2 at `max_iter=1`); a solution that stops straight after the `max_iter`-th assignment fails 2 of 10 with no way to know why. The performance report lists this reading as a planted slip, so the prose must rule it out. | "...Stop when an assignment repeats the previous one. Otherwise stop after `max_iter` rounds; each round is one assignment and the update that follows it."
33. `homework-4.json` | coverage | minor | No item on l19 (choosing a learner, choosing on validation, the edge over a base rate); the review has two. The brief's exam replacement "which learner for this data" has no homework practice. | Add one difficulty 4 `choice` or `numeric` item, for example a five-row validation table with a tie to break and a test score to report beside a base rate.
34. `docs/reports/stat-learning-4-perf.md` | "Objective matched" | minor | The validator's verb rule matches l17's "Build a network..." objective, but the product is k-means and proves l16's objective. The report says so in one line; the l17 objective is then proved by no blank-stub task. | Record as a known deviation of the brief in `DECISIONS.md`, or reword l17's objective verb in a later `course.json` pass.

## Counts

- wrong: 10 (5, 6, 7, 12, 13, 23, 24, 25, 26, 31)
- unclear: 7 (1, 2, 8, 14, 19, 27, 32)
- minor: 17 (3, 4, 9, 10, 11, 15, 16, 17, 18, 20, 21, 22, 28, 29, 30, 33, 34)

Total 34 findings.

The ten `wrong`, one line each:

- 5: l16 s2 `unsq` stores 12; its own sum is 16.
- 6: l16 s1 `half` stores "11, 29"; halfway is 11 and 29.8.
- 7: l16 s5 "Ten starts found the lowest raw inertia"; 50 starts go lower (842.15, purity 0.73).
- 12: l17 quiz q2 `order` stores 6; the wrong order gives $-1$.
- 13: l17 s9 "move in the third place"; the noise table moves by 0.010 and 0.013 between runtimes.
- 23: l19 s5 gives the squared-error split for accuracies.
- 24: l19 s7 "reusing one fitted object would carry state"; scikit-learn refits from scratch.
- 25: l19 s3 "both linear-boundary learners"; there is one.
- 26: l19 s8 tests pass a solution that validates on rows it trained on.
- 31: review `r-few-rows` 250 spline columns; 300.

## Verdict by file

| file | verdict |
|---|---|
| `l15-widest-street.json` | Sound. Two wording fixes (1, 2) and two minor. No number wrong. |
| `l16-groups-nobody-labelled.json` | Teaching sound; two dead `wrong[]` entries and one false sentence (5, 6, 7). Fix pass. |
| `l17-a-small-network.json` | Sound. One dead `wrong[]` entry (12); the noise screen's claim holds with the 0.50 to 0.56 range (and with CPython's 0.49 to 0.57), but two sentences about it are not true as written (13, 14). |
| `l18-bending-the-line.json` | Numbers all right. The ridge quiz explains the wrong mechanism (19). |
| `l19-which-learner.json` | Table and code right, no leakage. Three false sentences (23, 24, 25), one test gap that matters (26), one seed-bound generalisation (27). Fix pass. |
| `review-4.json` | One wrong number in a `why` (31). Covers all five lessons, difficulty 2 to 4. |
| `homework-4.json` | Keys, tests and rubric right. The performance task's stop rule needs one more sentence (32); no l19 item (33). |

Performance task `h-kmeans`: stub is blank, 10 hidden tests against 1 example, solution 10 of 10, starter 0 of 10, the author's nine planted slips all fail, and so do five of the reader's six (a call to scikit-learn's `KMeans` from the prelude, permuted labels, labels reassigned after the loop, no empty guard, the literal stop rule of finding 32); the sixth, stopping when the centres stop moving, is the same algorithm. Goes beyond l16 screen 4 (loop, stop rule, cap). Rubric of `h-cluster-story` sums to 10 and the model answer earns each row; $2 \times 64 + 64 + 64 \times 5 + 5 = 517$ checked.

## Continuity

- Prerequisites: every idea used is taught in L1 to L3 (validation split from l4, features from l6, penalty from l7, scaling from l9, logistic function from l10, boundary from l11, base rate from l12, hit-rate $t$ from l14) except "cointegration" (finding 10). $\partial$ appears in l17 s5; l8 and `regression` l2 already use it. No cross-validation, tree or `GridSearchCV` anywhere.
- Freshness: no level 4 item repeats a set-up from L1 to L3, `ensembles`, `validation` or exam `topic-2.1` (which has no SVM, clustering, network or spline item yet). `r-linkage` and l16 s6 share the value 0.675 from different matrices; harmless.
- Review covers l15 to l19 with two items each. Homework covers l15 to l18 (finding 33).

## Engine

- `bars` has no hidden state: a category held at 0 until the answer prints "0.00" (finding 30).
- `numbers_lib.check_wrongs` lists a `byKey` line that states other numbers as "check by hand" (45 lines here). Three of them were wrong in this level (findings 5, 6, 12): the feedback writes out a sum or product that does not equal the stored value. A check that evaluates plain arithmetic written in the `byKey` text and compares it with the `wrong[]` value would have caught all three (SESSION PROTOCOL 6: a class seen three times).
- Code tests cannot see which rows a solution fitted on; a leak is caught only when a test is built so that the leak changes the answer (finding 26). An authoring note in `docs/AUTHORING.md` ("a validation-split item needs one test with a learner that memorises") would do.

## Fix pass

Status: 32 fixed, 0 disputed, 2 deferred (29 recorded in the level report as the finding allows; 34 for the main session's `DECISIONS.md`). Three findings were applied with different wording or numbers from the reader's, on my own runs: 7, 14 and 27. Scratch scripts: `<scratchpad>/fix-stat-learning-4/` (`comp1.py`, `comp2.py`, `comp3.py`, `net1.py`, `net2.py`, `leak.py`, run in CPython and, through `pyo.mjs`, in the local Pyodide 0.27.7 build).

### One line per finding

1. fixed: l15 `screens[4].explain.text` states both directions once, where $C$ first appears. Basis: scikit-learn's `SVC` minimises $\tfrac12\lVert w\rVert^2 + C\sum\xi_i$ (user guide 1.4.7.1), so $C$ is a price; ISLP 9.2.2, equation 9.15, has $\sum \epsilon_i \le C$, a budget.
2. fixed: l15 `screens[1].explain.text`, "anywhere beyond their own edge". Basis: a constraint $s_i(w \cdot x_i + b) \ge 1$ that is slack stays slack only while the point stays on its own side of its edge.
3. fixed: l15 `screens[0].prose`, "with its default penalty". Basis: on separable classes the unpenalised likelihood has no finite maximum (ISLP 4.4.2); scikit-learn's `LogisticRegression` has an L2 penalty by default.
4. fixed: l15 `screens[3].explain.text` names $(2, 0)$, $(3, 3)$, $(3, 5)$. Basis: $s_i(2x_1 - 5) = 1$ only at $x_1 = 2$ for a default and $x_1 = 3$ for a repayment; the screen's own test expects `[2, 3, 5]`.
5. fixed: l16 `screens[2]` `unsq` 12 to 16. $2 + 0 + 2 + 4 + 2 + 6 = 16$, and NumPy's sum of absolute gaps.
6. fixed: l16 `screens[1]` `half` "11, 29" to "11, 29.8"; $(10 + 12)/2 = 11$, $(25.6 + 34)/2 = 29.8$ (fractions: $64/5 + 17 = 149/5$). The line now states the two values.
7. fixed, with my numbers: `KMeans(3, n_init=10, random_state=0)` stops at 842.33 (purity 0.75); `n_init=200` reaches 842.15 (purity 44/60 = 0.7333). My own Lloyd loop from 400 random starts has 842.15 as its lowest stop and 842.33 as a local stop. `n_init=50, random_state=0` still gives 842.33 here, so the text says "more starts", not "fifty starts".
8. fixed: l16 `summary.formula.note`, `quiz[0].explain.text` and option c's `why` say "the best inertia". Derivation: from the best $k$ groups, making one point of a group of two or more its own centre removes its term and cannot raise the rest (ISLP 12.4.1); one run can stop above the best, as screen 3's 58 against the best 10 shows.
9. fixed: l16 `screens[7].explain.text`. Basis: ISLP 12.4.2, on reading a dendrogram: similarity is read from the height of the fusion, not from horizontal position.
10. fixed: l16 `screens[10].explain.text`, no "cointegration"; the spread must keep pulling back to a level on fresh data.
11. fixed: test added to l16 `screens[4]`; squared distance gives `[1, 0, 1]` (25 > 18, 1 < 18, 20 > 1), summed absolute gaps give `[0, 0, 1]` (5 < 6). `how` says 10 tests.
12. fixed: l17 `quiz[1]` `order` 6 to $-1$, new `dropped` 6. $W_1 w_2 = (1, -1)$; $3 \times 2 = 6$.
13. fixed: l17 `screens[9].explain.text`. My runs: Pyodide 167, 150, 149 rows of 300 (the table), CPython 170, 146, 149: moves of 3, 4 and 0 rows.
14. fixed, my wording: "the best test accuracy is two rows in 300 above the 0.55 base rate" ($167 - 165$), true of the table beside it.
15. fixed: l17 `screens[8].prose`. Ring feature sds are 1.20 and 1.17, so no scaler is needed.
16. fixed: l17 `screens[0].explain.text`, "0.75 is its ceiling as well". `LogisticRegression` on the four corners has both weights 0 and scores 0.5; the best line over a grid scores 0.75.
17. fixed: l17 `screens[4].explain.text`; $ab + b$ with $a = 3$, $b = 1$ is 4.
18. fixed, and two of the three wrong solutions now fail: two band tests added to l17 `screens[8]`. Three units on seed 1 score 0.9733 in CPython and Pyodide (seed 0: 0.82), so a seed fixed at 0 fails; three units on seed 5 score 0.7833 in both (default `alpha`: 0.9633 in both), so a missing penalty fails. A scaler fitted on training and test rows together cannot be told apart by any band (0.80 against 0.82 at three units, within 0.01 elsewhere); `how` says the bands cannot check everything.
19. fixed: l18 `quiz[2]` key, `explain.text` and option c's `why`. My runs on 40 knots: the squared second differences of the fit fall from 1.21 to 0.48 at penalty 1, its sd falls from 15.8 to 12.9, the ends are flattened (12.3 against 9.8 at 1%, 61.0 against 62.5 at 40%), a penalty of $10^6$ gives a constant 46.5, the mean of $y$, and a penalty of 0.001 moves the curve by 0.06 bp at most. Smoothing spline: ISLP 7.5.1, $\lambda \to \infty$ gives the least-squares line.
20. fixed: l18 `quiz[1].explain.text` names the natural spline (ISLP 7.4.3: linear beyond the boundary knots).
21. fixed: l18 `screens[3]` new `interior` 3 with its line.
22. fixed: l18 `screens[10].prose` states the condition as its own sentence.
23. fixed: l19 `screens[5].prose`. The validator needs a formula on a `generalise` screen, so the split stays, now said of a squared error (ISLP 2.2.2, equation 2.7), with "an accuracy has no exact sum like it".
24. fixed: l19 `screens[7].explain.text` gives the real reason, and a test counts builds. My runs: a reused pipeline scores the same in all 20 deterministic cells; a fitted model kept from the street and refitted on the rings is one object and then scores 0.05 on the street. The new test counts 2 for the model solution and 1 for a reused model, in CPython and Pyodide. The helper `counted` is added to the prelude of screens 7 and 8, which stay identical.
25. fixed: l19 `screens[3]` option c `why`; 0.9067 is below 0.9233 and 0.92.
26. fixed: the reader's test added to l19 `screens[8]`. Honest validation: logistic 0.97, 1-nearest neighbour 0.96, answer `('logistic', 0.9633)`. Validating on seen rows: 1-nearest neighbour 1.0, answer `('knn1', 0.93)`. Both in CPython and in Pyodide; the model solution passes in the playthrough.
27. fixed, with my numbers: 40 further seed pairs of `make_wide` (training seed $100 + 2i$, test seed $101 + 2i$), identical in CPython and Pyodide: means logistic 0.9182, nearest neighbours 0.8588, SVM 0.9065, network 0.9090, additive 0.9283. Nearest neighbours is strictly last in 35 of 40 and below logistic regression in all 40; the additive model beats logistic regression on average by 0.010 (standard error 0.003). So "favour the simplest learner" is removed from l19 `screens[3].explain.text` and `summary.ideas[1]`, the average claim about nearest neighbours is stated as an average, and review `r-few-rows` option a no longer says "favour it".
28. fixed: l19 `screens[1].explain.text`, "manages it".
29. deferred: recorded in `docs/reports/stat-learning-4.md` with the reason (a learner's place on the axis depends on its settings).
30. fixed in content: `"showZero": false` on the five `bars` canvases of l19 screens 0 to 4 (`README-B.md`, bars: `showZero: false` hides the 0 of an empty bar). The engine note stays in the inbox.
31. fixed: review `r-few-rows` option d, 250 to 300. `SplineTransformer(n_knots=10)` on 25 columns returns 300; $25 \times (10 + 3 - 1)$.
32. fixed: `h-kmeans` prose defines a round. All 10 tests pass for the solution; the 9 planted slips still fail, and a tenth, the reading now ruled out, fails 2 of 10. `stat-learning-4-perf.md` and `stat-learning-4-perf-numbers.py` updated; `perf-reports.mjs` 0 missing parts.
33. fixed: new homework item `h-pick-learner` (difficulty 4, numeric, the last item so that no existing index moves). `fresh-check --file`: 0 hits.
34. deferred: a `DECISIONS.md` line is the main session's to write; the perf report already says it in one line.

The reader's 9 passing wrong solutions: 5 now fail (l16 Manhattan, l17 seed, l17 default `alpha`, l19 reused model, l19 seen rows). 4 still pass: two the reader marked harmless, the l18 scaler (no number changes, as the reader says) and the l17 scaler on all rows (no band can see it). No test was weakened.

### Changed graded values and tests (old, new)

- l16 `screens[1].widget.wrong` `half`: "11, 29" to "11, 29.8".
- l16 `screens[2].widget.wrong` `unsq`: 12 to 16.
- l16 `screens[4].widget.tests[9]`, new: `kmeans_step([[0, 0], [0, 6], [4, 3]], [[0, 5], [3, 3]])[0].tolist()` equals `[1, 0, 1]`. `how`: 9 to 10 tests.
- l17 `quiz[1].widget.wrong` `order`: 6 to -1; new `dropped`: 6.
- l17 `screens[8].widget.tests[5]`, new: `0.93 <= mlp_width_report([3], 1)[0] < 0.99` is `True`. `tests[6]`, new: `mlp_width_report([3], 5)[0] < 0.85` is `True`. `how`: 5 to 7 tests.
- l17 `screens[9]` option a (the key, same option): "test accuracy sits at or below the 0.55 base rate" to "the best test accuracy is two rows in 300 above the 0.55 base rate".
- l18 `screens[3].widget.wrong`, new `interior`: 3.
- l18 `quiz[2]` option a (the key, same option): "It shrinks the coefficients so the curve wiggles less; tune its size on validation" to "It shrinks the coefficients: less wiggle, but a flatter curve too; tune it on validation".
- l19 `screens[7].widget.tests[5]`, new: `(BUILDS.clear(), fit_table({'street': PROBLEMS['street'], 'rings': PROBLEMS['rings']}, {'logistic': counted('logistic')}), len(BUILDS))[2]` equals `2`. Prelude of screens 7 and 8: `BUILDS` and `counted(name)` added. `how`: 5 to 6 tests.
- l19 `screens[8].widget.tests[5]`, new: `list(choose_on_validation(*PROBLEMS['street'], {'logistic': LEARNERS['logistic'], 'knn1': lambda: make_pipeline(StandardScaler(), KNeighborsClassifier(1))}, 100))` is close to `['logistic', 0.9633]`. `how`: 5 to 6 tests.
- l19 screens 0 to 4, bars: `showZero: false` added.
- review `r-few-rows` option a (the key, same option): "few rows per feature favour it" to "with few rows per feature, start simple".
- homework, new item `h-pick-learner` (`items[9]`): answer 1.21, tolerance 0.005 absolute; `wrong` 2.42 (`besttest`), 1.61 (`tie`), 3.6 (`coin`), 2.01 (`valscore`). $0.03/\sqrt{0.56 \times 0.44/400} = 1.2087$, by floats and by fractions.
- No other key, answer or tolerance changed.

### Changed conceptual sentences (old, new)

- l15 s4 explain: "$C$ is a penalty, like the ridge penalty, but large $C$ means a weak penalty on $\lVert w \rVert$." to "scikit-learn's $C$ prices each unit of intrusion, so a small $C$ buys a wide street; ISLP's $C$ is a budget for intrusion and runs the other way."
- l15 s1 explain: "could move anywhere outside the street without effect" to "could move anywhere beyond their own edge without effect".
- l15 s0 prose: "Logistic regression would pick yet another line." to "Logistic regression with its default penalty would pick yet another line."
- l15 s3 explain: "rests on three different loans" to "rests on $(2, 0)$, $(3, 3)$ and $(3, 5)$".
- l16 s1 `half` line: "You moved each centre halfway." to "You moved each centre halfway, to 11 and 29.8."
- l16 s5 option c `why`: "Ten starts found the lowest raw inertia; the raw inertia itself rewards the wrong cut." to "More starts lower the raw inertia only from 842.33 to 842.15, and purity then falls to 0.73. The raw inertia itself rewards the wrong cut."
- l16 s5 `byKey.c`: adds ", and purity falls to 0.73" after "dominated by volatility".
- l16 summary note: "It always falls as $k$ grows" to "The best inertia never rises as $k$ grows".
- l16 q1 explain: "Inertia falls for every extra $k$" to "The best inertia falls for every extra $k$"; option c `why`: "It always falls" to "The best inertia always falls".
- l16 s7 explain: "The linkage is a choice that changes the answer. So is the height of the cut." to "The linkage and the height of the cut are choices that change the answer. Only heights mean anything: leaves drawn side by side need not be close."
- l16 s10 explain: "a pair is worth trading after a cointegration test on data the clustering never saw" to "a pair is worth trading only if its spread, on fresh data, keeps pulling back to a level".
- l16 s4 `how`: adds "The last has three 2-D points where squared distance and summed absolute gaps disagree."
- l17 q2 `order` line: "You multiplied in the wrong order." to "You multiplied in the wrong order: $W_1 w_2$ has second entry $0 \times 3 + 1 \times (-1) = -1$."; new `dropped` line: "You stopped at $3 \times 2$. The second hidden unit adds $(-1) \times 1$."
- l17 s9 explain: "The exact values move in the third place on another runtime; the conclusion does not." to "On another runtime the test scores move by up to four rows in 300; the conclusion does not."
- l17 s8 prose: "The bars show test accuracy from the playthrough's runtime." to "The bars show test accuracy as this app's Python computes it. Both features are already on one scale, so we skip the scaler here."
- l17 s8 `how`: adds "Two more runs of three units check that your seed and penalty are used: seed 1 reaches 0.93, and seed 5 stays under 0.85. The bands cannot check everything else: read your call against the comment."
- l17 s0 explain: "so it is stuck at the same 0.75" to "so 0.75 is its ceiling as well".
- l17 s4 explain: "A one-input layer of 3 to 1" to "A single layer from 3 units to 1".
- l18 q3 explain: "Shrinking the coefficients stops neighbouring pieces swinging apart, so many knots behave like few. A **smoothing spline** takes this to the limit: a knot at every point and a penalty on curvature. Here 40 knots with a penalty of 1 gave test $R^2$ 0.8868, too smooth, so the penalty is tuned like $k$." to "A ridge penalty pulls every spline coefficient towards zero: the curve wiggles less, but it is also flattened towards its mean. Here 40 knots with a penalty of 1 gave test $R^2$ 0.8868. A **smoothing spline** puts a knot at every point and penalises curvature instead: wiggle is damped and a trend is not flattened; either penalty is tuned on validation, like $k$."
- l18 q3 option c `why`: "You took the limit for the rule. Only a huge penalty flattens it." to "You took a limit for the rule, and the wrong one. A huge ridge penalty gives a flat line at the mean, and a small one barely moves the curve."
- l18 q2 explain: "but only by luck of shape." to "by luck of shape; a **natural spline** goes further and is forced to be linear beyond its boundary knots."
- l18 s3 new `interior` line: "You gave the interior knots, $K = 3$. Add 4 for the basis functions."
- l18 s10 prose: adds "That assumes the first half's impact has faded before the second half trades."
- l19 s5 prose: "Each score is 1 minus a test error, and a test error splits as $E[\text{error}] = \text{bias}^2 + \text{variance} + \text{noise}$." to "Level 1 split a squared error as $E[\text{error}] = \text{bias}^2 + \text{variance} + \text{noise}$. An accuracy has no exact sum like it, but the same three forces decide each cell."
- l19 s7 explain: "A fresh model per cell matters: reusing one fitted object would carry state between problems. The deterministic cells match to 4 places in any runtime. The network cell is tested only within a band." to "Each cell builds its own model, so a fitted model you keep is never overwritten by the next fit. scikit-learn's `fit` starts again each time, so a reused object would score the same here; the last test counts builds all the same. The deterministic cells match to 4 places in any runtime, and the network cell is tested within a band."
- l19 s7 `how`: "and the network's rings cell. That cell is checked" to "the network's rings cell, and a count of the models built, one per cell. The network cell is checked".
- l19 s3 option c `why`: "behind both linear-boundary learners" to "behind logistic regression and the SVM".
- l19 s3 explain: "Few rows and many noisy features favour the simplest learner, 0.9233, and hurt the distance-based one most, 0.89. Neighbours in 20 dimensions are mostly neighbours in noise. The SVM scores 0.92, close behind." to "Few rows and many noisy features hurt the distance-based learner most, 0.89: neighbours in 20 dimensions are mostly neighbours in noise. Over 40 other seed pairs nearest neighbours averages 0.86 and comes last in 35. The other four average between 0.90 and 0.93 and swap places, so logistic regression's lead here is this sample's."
- l19 summary idea 2: "Few rows per feature and heavy noise favour the simplest learner; on pure noise every learner sits at the base rate." to "Few rows per feature and many noise columns hurt distance-based learners most, on average over samples; on pure noise every learner sits at the base rate."
- l19 s1 explain: "The additive model wins here because" to "The additive model manages it because".
- l19 s8 `how`: "Check runs 5 hidden tests, one per problem, ... wide problem)." to "Check runs 6 hidden tests: one per problem, ... wide problem), and one with a learner that memorises its training rows."
- review `r-few-rows` option d `why`: "You added 250 spline columns to 80 rows. That is more columns than rows." to "You added 300 spline columns to 80 rows. That is far more columns than rows."
- homework `h-kmeans` prose: "Stop when an assignment repeats the previous one, or after `max_iter` assignments." to "Stop when an assignment repeats the previous one. Otherwise stop after `max_iter` rounds; each round is one assignment and the update that follows it." `how`: "a run stopped after one assignment" to "a run stopped after one round".
- homework `h-pick-learner`: all text new (prose, question, four slip lines, explanation).

### Gates

- `docs/reports/stat-learning-L4-numbers.py`: exit 0, 457 of 457 checks (378 before; a fix-pass block checks every value above by two routes and fails if a fix is reverted). `docs/reports/stat-learning-4-perf-numbers.py`: exit 0, 0 failures.
- Reader's `run-code.py`: exit 0; author solution passes, starter fails and reader's solution passes on all 13 widgets; 95 of 99 wrong solutions caught (90 before); the 4 that pass are listed above.
- Reader's `read-numbers.py`: exit 1, 129 of 138, the same nine `CONTENT` lines as before. Each of those checks compares the reader's recomputed value with the old stored value written into the script itself (12, "11, 29", 6, 250, and the five old sentences), not with the content file, so it cannot pass after the fix; every recomputed value in those nine lines (16, 11 and 29.8, 842.15, -1, 300, and the three probes) is the value the content now holds.
- Validator: 0 errors; 51 warnings on the level's files, the same 51 as before the pass (compared line by line against a copy of the app with the old files).
- Voice scan (`voice-scan.py 35`): 0 explanations over three sentences, 0 sentences over 35 words.
- Playthrough with `--local-cdn`, one at a time: l15, l16, l17, l18, l19, `review-4` and `homework-4`, with and without `--mobile`: 14 runs, all "All passed."
- `fresh-check --file` on `homework-4`: 0 hits. `perf-reports.mjs`: 0 missing parts.
