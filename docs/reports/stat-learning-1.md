# Report: stat-learning level 1 ("What learning means")

## Files written

All in `app/content/courses/stat-learning/`:

- `l1-predict-or-explain.json` (11 screens, 4 quiz items, skill `sl-setup`)
- `l2-training-error-lies.json` (10 screens, 4 quiz items, skill `sl-setup`)
- `l3-bias-variance.json` (10 screens, 3 quiz items, skill `sl-tradeoff`)
- `l4-nearest-neighbours.json` (12 screens, 3 quiz items, skill `sl-tradeoff`)
- `review-1.json` (8 items, difficulty 2 to 4, every lesson interleaved)
- `homework-1.json` (8 items, difficulty 3 to 5: two `code` items, one at 5; one `order`; one `longform` at 5 with a 10-point rubric and full model answer)

Generators, data and check scripts are in `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/stat-learning-1/` (`data.py`, `gen_l1.py` to `gen_l4.py`, `gen_sets.py`, `compute_*.py`, `runboth.sh`). Re-running a generator rewrites its file.

## What each lesson does

- **l1**: hook on a fitted line's training MSE (0.664) against its test MSE (1.207); explore on the noise sd (the true line's MSE is sigma squared, the irreducible error); features, target and loss; MSE against MAE and why squared; time-ordered split (tap the test days); `code`: `mse`/`mae`, `train_test_split_rows`, `fit_line_mse` with `np.polyfit` on the seeded `make_days`; trap: a same-day factor regression (R² 0.437, t 13.9) used to forecast tomorrow scores test MSE 1.441 against 1.437 for the mean; derive: the mean is the best constant and its MSE is Var(Y) (edge case: no signal); transfer: four desk requests sorted into predict or explain.
- **l2**: 30 seeded intraday spread snapshots, a degree slider from 0 to 15 switching precomputed fits on a `plane`, 60 held-out snapshots in a second colour; training MSE never rises, test MSE bottoms at degree 5 (0.307) and reaches 80.15 at degree 15; `series` U-shape (log scale) and a `table` the learner fills for degrees 1, 3, 9, 15; degrees of freedom (degree 29 interpolates 30 points; degree 0 is the mean); 30 against 300 training days; `code`: `fit_poly_mse` (x rescaled to [−1, 1] with the training min and max, said why) and `best_degree` over 0 to 12; trap: adding terms until in-sample error is zero; derive: why nested training error cannot rise; transfer: a 40-parameter backtest tuned and scored on 2014 to 2023.
- **l3**: 200 seeded resamples; 20 fitted curves per degree (0 to 9) on a `plane` with x0 = 1 hour; bias and variance named from the spread of predictions; `table` for degrees 1, 5, 9 (7.051, 0.519, 1.111); `order` derivation of noise + variance + bias² with a reason per line, linked to the `estimation` course's MSE split; trade-off `series`; edge cases (constant rule: zero variance; true f: zero bias); `code`: `decompose` and `bias_variance_at`; trap: more data cuts the line's variance (0.547 to 0.036) but not its bias (5.56), and noise is not bias; transfer: averaging ten independent volatility models (1.15 to 0.43), a preview of `ensembles`. k-NN's k previewed in the quiz.
- **l4**: `grid` feature plane (yesterday's return and volume ratio, standardised); tap the 3 nearest, average them, k = 1 and k = n, majority vote; `code`: `knn_predict` in NumPy with ties broken by index order; scaling (£ millions against per cent); scikit-learn's `fit`/`predict` with `KNeighborsRegressor` (`knn_test_mse`), U-shape in k (best k = 7, test MSE 0.6079), `best_k` over 1 to 25; trap: test rows inside the training set give 0 error at k = 1; curse of dimensionality `bars` (exact ball volumes, 0.0025 at d = 10); transfer: the desk "analogue" model as 20-NN. Edge cases: k larger than the training set (ValueError, checked), ties in distance.

## Validator

`node app/tools/validate.mjs`: 0 errors overall; no warnings from my six files (the remaining warnings belong to other courses and unwritten lessons).

## Playthrough (`--local-cdn .../scratchpad/pkgs`, with `--why`; also once with `--mobile`)

- l1-predict-or-explain: ok, 15 checks, quiz 4/4
- l2-training-error-lies: ok, 14 checks, quiz 4/4
- l3-bias-variance: ok, 13 checks, quiz 3/3
- l4-nearest-neighbours: ok, 15 checks, quiz 3/3
- review-1: ok, 8 of 8
- homework-1: ok, 8 of 8, 37 of 37 marks

Screenshots (desktop, 390 px, Why? sheets, wrong-answer sheets) are in the scratchpad folder `stat-learning-1/shots` and `shots2`; I looked at them and fixed what they showed (two trap explanations that passed a whole canvas instead of a patch, an overlapping series marker, a crowded grid).

## scikit-learn load time

Measured with a timed copy of the playthrough: the first Check on the first screen that imports scikit-learn (l4 screen 7, 6 tests) took **24.7 s** with NumPy already loaded; NumPy's own first load (l4 screen 5) took 6.6 s. That is from a local CDN, so a real network will be slower. Every `how` on a scikit-learn screen says the first run takes 20 to 40 seconds. Later scikit-learn checks took 0.1 to 0.5 s (`best_k`: 125 fits in 0.5 s).

## How the numbers were checked

Every dataset is a seeded `np.random.default_rng` generator described in prose. Each stated number was computed twice: in CPython (NumPy 2.5.3) and in Pyodide 0.27.7 (NumPy 2.0.2) run under Node, and the outputs compared as JSON (identical for every NumPy value). CPython here has no scikit-learn, so every scikit-learn value was computed in Pyodide's scikit-learn 1.6.1 and checked against an independent NumPy k-NN (regression MSE for k = 1 to 25 and the classifier hit rates matched exactly). Every code test's expected value comes from running the solution, and the playthrough runs each solution against its tests in the browser. The playthrough caught one hand-computed expected value in `knn_predict` (fixed).

## Proposed change to course.json

None.

## Engine or canvas limitations

Five, added to `docs/BACKLOG-INBOX.md` under "Raised later (stat-learning level 1):". The main one: a slider cannot pick one of several precomputed curves. I worked round it with a ternary chain inside a single `expr`. It works, but l3's 20 curves times 10 degrees make the file 140 KB.
