# Report: validation level 1 (Cross-validation)

## Files written

All in `app/content/courses/validation/`. The build scripts that write each JSON file, the reference solutions, the test cases and every generator are in `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/validation-1/` (`b_l1.py` to `b_l4.py`, `b_sets.py`, `bc.py`, `common.py`, `cases.py`, `sol/`, `vnums.py`).

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l1-holding-back.json` | 12 screens, 4 quiz | `split_three`, `test_mse_for_seeds`, `is_touched` | vl-cv, vl-overfit |
| `l2-rotating-folds.json` | 12 screens, 4 quiz | `kfold_indices`, `cv_mean_sd`, `loo_mse` | vl-cv |
| `l3-tuning.json` | 12 screens, 4 quiz | `validation_curve_ridge`, `pick_one_se`, `grid_search_best` | vl-cv, vl-overfit |
| `l4-nested.json` | 12 screens, 4 quiz | `nested_cv_mse`, `selection_gap`, `count_fits` | vl-cv, vl-overfit |
| `review-1.json` | 8 items, difficulty 2 to 4, two per lesson | | |
| `homework-1.json` | 9 items, difficulty 3 to 5 | `honest_procedure` (5), `paired_fold_diff` (4) | |

l1's first screen says the loans are an exchangeable cross-section and that time-ordered data is level 2. Traps: best of 20 random splits (l1), unshuffled folds on a size-sorted file (l2), the best CV score read as the expected score (l3), `best_score_` reported instead of the nested score (l4). Edge cases: a 5-loan test set and a 40-loan book (l1), a fold with no defaults and k = 2 (l2), a grid of one and a tie (l3 quiz), every outer fold picking a different α (l4). The other traps in the brief sit in quizzes: tuning on the test set, models compared on different folds, the fold sd read as a confidence interval, tuning on all rows then cross-validating, and a shared fold seed inside and out (explained as harmless).

Homework: the complete honest procedure as code at difficulty 5 (split, Pipeline, GridSearchCV on train, one test score, nested CV on train, returning `(alpha, test_mse, nested_mse)`); paired fold differences as code; an `order` item (the steps of nested CV through to the deployed model); a `longform` item (the colleague's "5-fold CV MSE 0.18 after 40 settings, no held-out set" note, 10-point rubric, full model answer); four numeric items and two choice items.

Canvases: bars (seed-to-seed test MSEs, 20 seeds with the minimum highlighted, 5-row test sets, fold MSEs with a mean line, sorted against shuffled folds as grouped bars, defaults per fold, 15 noise signals against a mean-only line, inner best against nested for three searches), series (sd and average of the test MSE against test share on two axes, with a slider-driven marker pair; k-NN training and CV MSE against k), boxes (three jobs dragged into training, validation and test), grid (20 loans with a fold slider whose derive reshades the test fold; tap fold 3 from the shuffled order; a degree × α grid, tap the best cell), plane (the ridge validation curve with fold-sd error bars, tap the lowest and the one-SE pick; the same curve cut off at the grid's edge, widened in the explanation), tree (outer folds holding inner folds, with outer and inner sliders and a live fit count), array, console and table canvases, and table widgets.

## Validator

`node app/tools/validate.mjs`: 0 errors, and no warnings in my six files. The remaining warnings belong to other courses and to validation levels 2 and 3.

## Playthrough

`node app/tools/playthrough.mjs --lesson ... --set ... --local-cdn .../scratchpad/pkgs --shots .../validation-1/shots --mobile` (Pyodide 0.27.7, scikit-learn 1.6.1). Final run, after the last edit:

| File | Result |
|---|---|
| l1 | 16 checks, quiz 4/4 |
| l2 | 16 checks, quiz 4/4 |
| l3 | 16 checks, quiz 4/4 |
| l4 | 16 checks, quiz 4/4 |
| review-1 | 8 of 8 recorded |
| homework-1 | 9 of 9 right, 40 of 40 marks |

The screenshots (1280 and 390 px) are in `.../scratchpad/validation-1/shots` and `shots1`. I fixed these after looking at them: job cards that overlapped in a `row` container, and the same canvas overflowing at 390 px. I also fixed the plane's y axis, which crossed the middle of the validation curve until I set `yAxis: "left"`, inner-fold labels that collided on a 4 × 4 tree, a second-axis label on the l1 series, and a hint containing `!=`, which the validator read as an exclamation mark.

## Numbers: computed twice

- **Code tests.** All 78 cases ran with the reference solutions in CPython 3.13 (scikit-learn 1.6.1 installed in the scratchpad, NumPy 2.5) and in Pyodide 0.27.7 under Node (NumPy 2.0.2, scikit-learn 1.6.1). The two gave identical outputs on every case (`exp_cpy.json` and `exp_pyo.json`). The playthrough then passed every solution in the browser.
- **Canvas and prose numbers.** Every number on a canvas or in prose came from one script (`vnums.py`), which I ran in both interpreters. The two outputs were identical.
- **Independent checks.**
  - `kfold_indices` is compared with scikit-learn's `KFold` output.
  - `loo_mse` is compared with `LeaveOneOut`.
  - `count_fits` was checked by counting `fit` calls on a subclassed `Ridge` inside `cross_val_score(GridSearchCV(...))`: 255, 39, 755 and 6.
  - The selection-gap bars were computed twice: with a NumPy implementation of the subset search, and again with scikit-learn loops in Pyodide (0.1681/0.1721, 0.1647/0.1719, 0.1630/0.1809).
  - The hypergeometric chances were computed two ways each.
  - The arithmetic answers were checked by hand: 1.35 for the best of 20 Sharpes, 820 test loans, 0.0203, √0.21 = 0.458, 15%, 2,010 fits, 125 fits and 75 fits.

## Dataset generators (seeded, in hidden preludes and in `common.py`)

- **`make_loans(n, p, seed)`.** Loan spread over base rate in percentage points: 2.5 + 0.6 · leverage − 0.4 · interest cover + 0.3 · sector risk + N(0, 0.45²). All features are N(0, 1) rounded to 3 places, and columns 4 onwards are pure noise (σ² = 0.2025). Instances used:
  - l1: `(200, 8, 11)`. Ten seeds give test MSEs from 0.143 to 0.286, mean 0.2224 and sd 0.0451. Twenty seeds give a minimum of 0.142 at seed 15 and a mean of 0.210.
  - l2: `(400, 8, 21)`. With ridge α = 1 the fold MSEs are 0.157 to 0.234, mean 0.1815 and sd 0.0277. With random_state 1 the mean is 0.1927.
  - l2, LOO: `(200, 3, 7)`. LOO gives 0.2121 and 5-fold gives 0.2133.
  - l3 and l4: `(200, 15, 52)`. The ridge curve's minimum is 0.2010 at α = 10 (sd 0.0214), and the one-SE rule picks α = 30. In nested CV the outer folds pick 3, 3, 1, 10 and 3, with a mean of 0.2002.
  - Homework: `(400, 12, 81)`. The honest procedure gives (1, 0.2253, 0.2165).
- **`make_spreads(n, p, seed)`.** The same loans with a convex leverage term, + 0.25 · leverage². l3's 3 × 5 degree × α grid uses `(200, 7, 61)`: the best is degree 2 at α = 10 (0.277), and degree 3's best is 0.356 at α = 100.
- **`make_noise(n, p, seed)`.** Spread = 2.5 + N(0, 0.45²), with every signal pure noise. l4 uses `(200, 15, 71)`:
  - The 15 one-signal models score from 0.1647 to 0.1722 against 0.1684 for mean-only.
  - On 5,000 fresh loans (seed 72) the winner scores 0.2010 and mean-only 0.1971.
  - Inner best against nested: 0.1681/0.1721 for ridge over 6 α values, 0.1647/0.1719 for the best of 15 signals, and 0.1630/0.1809 for the best of 105 pairs.
  - Over seeds 0 to 19 the average gaps are 1.0%, 4.4% and 6.2%.
- **l2 trap: `make_firms(400, 31)`.** Size, leverage and interest cover, with the size effect −0.5 · min(size, 0.5), sorted by size. Unshuffled folds give 0.409, 0.232, 0.233, 0.262 and 0.490; shuffled folds give 0.217 to 0.264.
- **l1 explore.** The test-share curves (10% to 50%, 200 seeds each) run from an sd of 0.058 to 0.022, while the average MSE drifts from 0.207 to 0.215.

## Design decision worth knowing

With 200 to 600 rows, tuning one ridge α flatters the inner best by only about 1% on average. Across 20 pure-noise datasets the gap was 1.0%, and it was often zero, because the largest α wins both inside and out. That gap is not visible on a chart.

So the l4 bars put the ridge search beside two feature-subset searches on the same dataset, the best of 15 signals and the best of 105 pairs, and the gap grows from 0.004 to 0.018. The lesson says honestly that the gap grows with the search and shrinks with the rows. `selection_gap(X, y, alphas, k, seed)` keeps the brief's ridge signature. It returns (0.1681, 0.1721) on the noise loans and −0.0008 on a real dataset, and the explanation uses that to say the gap is random with a positive mean.

The transfer's "15% better" is kept as the colleague's reported numbers, 0.170 against 0.200. The explanation reads such a gap as a sign that the search had a lot of freedom for 300 rows.

## Longest case wall time

Measured in Pyodide 0.27.7 under Node:

- The longest single case was 4.6 s: `honest_procedure` on 400 loans, which runs a 5-fold grid of 5 α values and then 5 × 5 nested CV. I gave that item `budget: 40000`.
- Nested CV and selection-gap cases took up to 2.0 s each.
- In the browser playthrough the whole homework set took 17 s.

## course.json

No change proposed.

## Engine and canvas limitations

There are five bullets under "Raised later (validation level 1):" in `docs/BACKLOG-INBOX.md`:

- **series:** no error bars or numeric or log x, so the validation curve was drawn on a plane.
- **boxes:** four containers overflow the column, and card text spills over its border.
- **bars:** `hlines` labels are drawn over the bars.
- **tree:** compact 16-leaf labels overlap.
- **code widget:** another vote for a per-case `tol`.
