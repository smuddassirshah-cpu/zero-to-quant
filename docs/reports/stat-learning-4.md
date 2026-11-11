# stat-learning level 4 ("Other learners"): report

## Files

| file | screens | quiz / items | code screens |
|---|---:|---:|---:|
| `l15-widest-street.json` | 11 | 4 | 3 (`margin_width` + `support_points`, `svm_report`, `pick_gamma`) |
| `l16-groups-nobody-labelled.json` | 11 | 4 | 2 (`kmeans_step` + `inertia`, `cluster_report` + `merge_heights`) |
| `l17-a-small-network.json` | 12 | 4 | 3 (`forward` + `n_params`, `gd_step`, `mlp_width_report`) |
| `l18-bending-the-line.json` | 11 | 4 | 2 (`hinge_features` + `fit_linear_spline`, `spline_r2` + `additive_r2`) |
| `l19-which-learner.json` | 10 | 3 | 2 (`fit_table`, `choose_on_validation`) |
| `review-4.json` | | 10, `pass` 0.8, difficulty 2 to 4 | |
| `homework-4.json` | | 9, difficulty 3 to 5 (two at 5) | 2 (`h-kmeans` performance task, `h-rbf-decision` at 5) |

Homework also holds the ISLP-style items the brief names: a margin and its edge points from six points (`h-margin-table`), a dendrogram cut at 0.35 and 0.65, a 2-3-1 parameter count and forward pass, the 8 degrees of freedom of a cubic spline with four interior knots, an `order` derivation that a network with no activation is linear, and the longform `h-cluster-story` (10-point rubric, full model). Skills as the brief sets them; `sl-flexible` does not exist in `course.json`, so it is not used.

## Gates (SESSION PROTOCOL 4)

1. `cd app && node tools/validate.mjs`: 0 errors. Level warnings left: point hints without a highlight, ladder canvas changes, a few sentences of 20 to 34 words, one problem without a canvas (l18 screen 4, a count).
2. `VOICE_BASE=app/content/courses/stat-learning python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences.
3. `<venv>/bin/python docs/reports/stat-learning-L4-numbers.py`: exit 0, 378 of 378 checks (`Level("stat-learning", 4)`, `expect`, `claim`, `check_wrongs`; 45 "check by hand" byKey lines read, each names the slip with other numbers). `docs/reports/stat-learning-4-perf-numbers.py`: exit 0.
4. Playthrough `--local-cdn <pkgs>` of all five lessons, `review-4` and `homework-4`: All passed without flags, with `--mobile` and with `--tablet`. Shots read at 440 px for every lesson; fixed: overlapping street-edge labels (l15), a question whose formula ran off a phone (l18), a Markdown table cut at 440 px (l19, now a `table` canvas), the hook plane range (l18), the step-size plane range (l17).

`fresh-check --file`: review-4 0 hits (one advisory: 0.1, 0.5, 0.9 shared with an l17 option); homework-4 0 hits. Performance task: `docs/reports/stat-learning-4-perf.md`.

## Methods, conditions and sources (for the second reader and the concept audit)

- **Maximal margin, support vectors, $C$** (ISLP 9.1 to 9.2): derivation in l15 screen 10 (distance $|w \cdot x + b|/\lVert w\rVert$, free scale, margin $1/\lVert w\rVert$, minimise $\lVert w\rVert$ subject to $s_i(w\cdot x_i+b)\ge 1$); hard margin needs separable classes (quiz q3 shows one mislabelled loan breaking it, slack 2 under $C=1$); $C$ is a price per unit of intrusion, small $C$ wide and stable (simulation: three $C$ rows on `make_street`).
- **Kernels** (ISLP 9.3): a choice of similarity, not magic; the explicit column $x_1^2+x_2^2$ against the RBF kernel; $\gamma$ is reach, chosen on a validation split with ties to the smaller $\gamma$; scaling stated (both generated columns already share a scale; a column times 100 drops RBF test accuracy 0.965 to 0.795); `decision_function` is a signed distance in margins, not a probability.
- **k-means and hierarchical clustering** (ISLP 12.4.1, 12.4.2): derivation l16 screen 10 (the mean minimises a group's sum of squares, both steps lower the inertia, finitely many groupings, so it stops at a local minimum); dependence on starts (58 against 10; `n_init`) and on scaling (purity 0.75 raw, 1.0 scaled); linkage and cut height as choices; no labels, so no test error; inertia falls on noise.
- **Networks** (ISLP 10.1, 10.2, 10.7): hidden layer as built features, ReLU as the bend, logistic output; parameter count $ab+b$ per layer; gradient descent by the single-variable chain rule with the other weight held fixed (derivation l17 screen 11); step size watched (0.3042 at 0.1, 45.125 at 0.5); dead unit; no activation collapses to one linear map (quiz q2, homework order item); overfitting on few noisy rows (simulation on `make_noise`); seeds and scaling.
- **Splines and additive models** (ISLP 7.3, 7.4, 7.7): a spline is features for a linear model; linear spline continuity and running-sum slopes (derivation l18 screen 10); cubic spline $K+4$ basis functions, `SplineTransformer` counts boundary knots ($5+3-1=7$); knots on validation; extrapolation beyond the boundary knots; ridge on many knots and the smoothing spline (quiz q3); additive models cannot express an interaction (simulation, 0.3292 falling to 0.172 with more knots).
- **Comparing learners** (ISLP 2.2, 4.5, 9.5): the five-by-five table; choice by validation, ties to the simpler learner; the $t$ statistic against the base rate.

## Numbers (CPython 3.12 + scikit-learn 1.6.1; Pyodide 0.27.7 local build)

Every value below is identical in both runtimes unless a Pyodide value is shown. Pyodide values come from the hidden tests passing in the playthrough and from a node run of the same build (`pyo.mjs`, scratchpad).

- l15: $w=(0.5,0.5)$, $b=-2$, support vectors $(1,1),(2,0),(3,3)$, margin 1.4142, street 2.83 (SVC $C=10^6$ and exact); vertical street 1; opening slider street 1.79; moved support vector: slope $-0.75$, street 2.5; street $C$ rows (94, 0.965, 0.975, 2.78), (24, 0.965, 0.965, 1.07), (21, 0.97, 0.95, 0.80); rings linear 0.65 (298 SVs), logistic 0.5067, feature column 0.9733 with circle radius 1.41; RBF $\gamma$ 0.01 to 1000: (300, 0.6333, 0.61), (76, 0.99, 0.97), (44, 0.9967, 0.98), (177, 0.9967, 0.97), (289, 1.0, 0.87), (300, 1.0, 0.64); validation grid ($C$ 0.1, 1, 10, 100): [0.7, 0.98, 0.99, 0.94], [0.7, 0.99, 1.0, 0.99], [0.95, 1.0, 0.99, 0.98], [1.0, 1.0, 0.98, 0.98], so `pick_gamma` gives 1, 1, 0.1, 0.01; unscaled 0.795.
- l16: centres 10, 25.6 then 12, 34; inertias 790, 64, 10, 4; bad start 58 (also `KMeans(n_init=1, random_state=1)`); sds 0.336, 13.04; purity 0.75 and 1.0; scaled inertias 120, 62.39, 14.16, 11.24, 9.79, 7.92, 6.47; $k=4$ sizes 6, 14, 20, 20; noise inertias 600, 402.4, 277.8, 216.2, 179.0, 148.9, 128.9 (no elbow), $k=3$ 277.77 with 88, 98, 114; linkage heights single [0.2, 0.3, 0.6, 0.8], complete [0.2, 0.3, 0.75, 0.95], average [0.2, 0.3, 0.675, 0.875]; cut 0.70: 2 single, 3 complete; pairs 1,770 and 570.
- l17: corners $z=-2,2,2,-2$, $p$ 0.1192 and 0.8808; $(0.5,0.8)$: $z=0.8$, $p=0.69$; counts 9, 33, 465; steps 0.3042 and 45.125 (slopes $-4$, $-1$); width sweep test accuracy, Pyodide 0.6567, 0.6467, 0.82, 0.97, 0.97 (CPython 0.6567, 0.6467, 0.82, **0.9733**, 0.97); seeds 0, 1, 2 at 8 units, Pyodide 0.97, 0.9667, 0.96 (CPython **0.9733**, 0.9667, 0.96); noise, 8 units, seeds 0 to 2, Pyodide train 0.5833, 0.6033, 0.65 and test 0.5567, 0.5000, 0.4967 (CPython train 0.5767, 0.6033, 0.65, test 0.5667, 0.4867, 0.4967); the brief's "0.54 to 0.56" is not what this build gives, so the lesson states the Pyodide table and says the values move in the third place.
- l18: line 18.59 at 1%, test $R^2$ 0.9088; degree 12 (with `StandardScaler`) 0.9381 and 216.23 at 55, truth 74.16; hinge 8, 16, 20; linear splines: knots 5 and 20 coefficients 5.789, 3.822, $-2.459$, $-0.488$ (slopes 3.822, 1.363, 0.875), test $R^2$ 0.9088, 0.9289, 0.9426, 0.9428 for no knot, 5, 5 and 20, 10 and 30; cubic splines (train, test): 2 (0.9575, 0.9424), 3 (0.9586, 0.9439), 5 (0.9598, 0.9417), 10 (0.9613, 0.938), 40 (0.9652, 0.9347); validation on rows 151 to 200 picks 5 knots (0.9495 against 0.9494); linear tail 85.13 at 55; additive 0.3744 against 0.9101 (14 columns); interaction 0.1213 linear, 0.3292, 0.2373, 0.172 at 5, 10, 20 knots; splitting saves 5 bp above 3.0% (grid 3.02, bisection agrees; the true law 2.91); ridge on 40 knots $\alpha=1$: 0.8868.
- l19: the table (street 0.9633, 0.9633, 0.9633, 0.9567, 0.96; rings 0.5067, 0.9767, 0.9767, 0.9733, 0.98; quadrants 0.4767, 0.86, 0.8567, **0.8467**, 0.4567; wide 0.9233, 0.89, 0.92, 0.9067, 0.9167; noise 0.5567, 0.4967, 0.5567, **0.5367**, 0.5333), network cells Pyodide (CPython 0.8433 and 0.5633); $t=0.23$; rings seeds (9,10) 0.48, 0.98, 0.98, 0.9733, 0.9833 and (11,12) 0.5167, 0.9633, 0.9667, 0.9567, 0.9567; validation choices street logistic 0.9633, rings additive 0.98, quadrants SVM 0.8567, wide logistic 0.9233, noise k-NN 0.4967.
- Review and homework: street 0.4; k-means 15.33; $p=0.5$; 51; 21; $t=1.60$; average linkage 0.675; margin 2.12 with $w=(1/3,1/3)$, $b=-2$; 13 and $z=3.5$; 8; 18; 517; RBF decision values 2.127469, $-0.082931$, $-1.539442$, 5.539871 (equal to `decision_function`).

## Seeds, data and network tolerances

The brief's generators, unchanged, in each `prelude`; training on the first seed and testing on the second (street 4/5 at 200 rows in l15 and 300 in l19, rings 7/8, quadrants 3/4, wide 60 rows seed 4 against 300 rows seed 5, noise 4/5, stocks 11, impact 21/22, additive 31/32). Every scikit-learn fit carries `random_state` where it has one. Network tests use bands only: `mlp_width_report` widths 1 and 2 under 0.75, width 3 within 0.03 of 0.82, widths 8 and 64 and seeds 0 to 2 in [0.93, 0.99); `fit_table`'s network cell in [0.95, 0.99]. No exact network weight or score is tested.

## Deviations from the brief, and proposals

- `margin_width(w, b)` returns the margin $1/\lVert w\rVert$ ($b$ does not change it); `gd_step` returns the new weights and the loss after the step; `choose_on_validation` takes the test arrays as arguments and refits the winner on all training rows; `mlp_width_report` uses `make_rings` with no scaler, as the brief's numbers do.
- The ridge-on-spline "one screen" is l18 quiz q3, to keep l18 at 11 screens; on this data a penalty does not beat five knots, which the quiz says.
- l19's wide row shows all five learners (the additive model scores 0.9167 there).
- No `course.json` change proposed.
