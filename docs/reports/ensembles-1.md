# Report: ensembles level 1 (Decision trees)

## Files written

All in `app/content/courses/ensembles/`:

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l1-yes-no-questions.json` | 11 screens, 4 quiz | `split_counts`, `best_threshold_by_accuracy`, `tree_depth_2_predict` (scikit-learn) | en-trees, en-interpret |
| `l2-good-split.json` | 12 screens, 4 quiz | `gini` + `entropy`, `split_gain` (checked against scikit-learn's impurity drop at the 12-loan root), `best_split` (checked against scikit-learn's root on two books) | en-trees |
| `l3-memorising.json` | 11 screens, 4 quiz | `train_test_acc_by_depth`, `best_depth_cv` (`cross_val_score`), `leaves_at_alpha` (`ccp_alpha`, with `cost_complexity_pruning_path` on screen) | en-trees |
| `l4-predicting-numbers.json` | 11 screens, 4 quiz | `leaf_mean_predict`, `sse_gain`, `tree_vs_line_mse` (scikit-learn) | en-trees, en-interpret |
| `review-1.json` | 10 items, difficulty 2 to 4, two or three per lesson | | |
| `homework-1.json` | 7 items, difficulty 3 to 5 | `build_tree_depth2` (5: from-scratch depth-2 Gini tree returning nested rules and predictions, every expected value produced by scikit-learn's tree on the same rows), `honest_tree_accuracy` (4: time split, depth by `TimeSeriesSplit` CV on train, refit, test once) | |

Homework also has an `order` item (the cost-complexity pruning procedure, ending with one test-set score), three numeric/choice items (information gain, best regression split, a monotone transform of a feature) and a `longform` item (a risk committee asks why the credit model is a depth-3 tree and not logistic regression) with a 10-point rubric and a full model answer.

Lesson shapes. l1: tap the rule's mistakes in a 12-loan table, tap the best of four candidate questions, the best question inside a branch, a `tree` growing with a depth slider, the `plane` picture (axis-parallel lines, leaf rectangles, a depth slider) where the learner taps the training loans sharing a new loan's leaf, trap, the greedy recipe as an `order` derive (with the XOR counter-example to optimality), three code screens, a desk's credit screen as transfer (with the committee-readability point). l2: two splits with equal mistakes (bars), Gini by hand, Gini/entropy/error-rate curves with a p slider, a table widget for weighted impurity, trap, a split accuracy cannot see, three rating classes, information gain, three code screens, a market-regime split on realised vol as transfer. l3: U-shape of train and test error against depth (`series`), rectangles at depth 1, 3 and unlimited, `min_samples_leaf` and `min_samples_split`, trap, CV, pruning by hand and in code, a bootstrap pair of trees (variance; level 2 preview), a 14-condition trading rule as transfer. l4: drag a leaf level to minimise squared error, tap the best regression split, step functions by depth and by leaf size, extrapolation trap, tree against line on two data sets, the leaf-mean proof as an `order` derive, three code screens, a vol forecast in a crisis as transfer.

Traps: balanced groups over purity (l1; greedy taken as optimal in the derive and quiz), unweighted impurity average (l2; accuracy-based splitting as a ladder screen), depth tuned on the test set (l3; pruned training accuracy in the quiz), extrapolation (l4; tree on a smooth slope with few rows on screen and quiz). Edge cases: a pure node, copied features with `random_state` (l1); a split that moves no rows, three classes (l2); `min_samples_leaf` above half the data gives one leaf, not even a stump, and a book where depth 1 is best (l3); a one-row leaf, a constant target (l4).

`random_state=0` is fixed on every tree and said once (l1 screen 10). Every `how` on a scikit-learn screen says the first load takes 10 to 30 seconds. £ is the only currency used. The counting-chance and random-vars courses do not teach entropy, so l2 introduces it without a link.

## Validator

`node app/tools/validate.mjs`: 0 errors overall. Level 1 files carry only these warnings: two "ladder changes canvas kind" (l2 screen 4, l3 screen 9) and a few "point hint usually highlights the canvas" on code screens.

## Playthrough

`node app/tools/playthrough.mjs --local-cdn .../scratchpad/pkgs` (Pyodide 0.27.7, scikit-learn 1.6.1), all in one run, no console errors:

| File | Result |
|---|---|
| l1-yes-no-questions | 15 checks, quiz 4/4 |
| l2-good-split | 16 checks, quiz 4/4 |
| l3-memorising | 15 checks, quiz 4/4 |
| l4-predicting-numbers | 15 checks, quiz 4/4 |
| review-1 | 10 of 10 recorded |
| homework-1 | 7 of 7 right, 32 of 32 marks |

Screenshots (every screen, and Why sheets) were reviewed in `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/ensembles-1/shots/`; fixed after review: a point label hiding a loan, curve labels swapped by placement, long console and starter lines, a slider whose readout was an index of 0.

## How the numbers were checked

Every expected value comes from my solution run in CPython (scikit-learn 1.6.1, NumPy 2.5 in a scratch venv) and again in Pyodide 0.27.7 under Node (`checkcode.mjs`: every code widget's solution against its examples and tests, all passed), then a third time through the browser playthrough. Gini, entropy, gains, squared-error drops and break-even alphas in prose and numeric items were worked by hand and checked by code. `best_split`, `split_gain` and `build_tree_depth2` were compared with scikit-learn's own trees on the same rows. Pruning tests use alphas away from the break-even values on the path.

## Dataset generators (all `np.random.default_rng(seed)`, stated in the preludes)

- **12 loans** (literal, l1, l2, homework): leverage and interest cover; designed so *leverage > 3* is the unique best root (2 mistakes, Gini gain 0.209921), then *cover ≤ 1.5* and *cover ≤ 4.0* make every leaf pure.
- **`make_loans(seed, n)`**: leverage U(0.5, 6), cover U(0.5, 8), both rounded to 2 places; default probability 0.8 if leverage > 3.5 and cover < 3, 0.3 if leverage > 3.5 and cover ≥ 3, 0.5 if leverage ≤ 3.5 and cover < 1.5, else 0.08 (Bayes error about 0.195). l3 uses seed 3, n = 500, 300 train and 200 test: test error 29.0%, 18.5%, 19.5% at depths 1 to 3, 34% unlimited (79 leaves). `X40` in l2 and the homework is `make_loans(4, 40)` as literal lists.
- **`make_one_threshold(seed, n=300)`**: default probability 0.85 if leverage > 3.5, else 0.1; cover is noise. Seed 2: CV picks depth 1.
- **`make_vol(seed, n=300)`**: yesterday's realised vol U(8, 40)%, volume z-score; next-day vol 12, 20 or 32% by regime (breaks at 16 and 26), +1.5 when volume z > 1, noise sd 2.5. Seed 1, 200 train.
- **`make_linear(seed, n=100)`**: y = 4 + 0.8x + N(0, 3²); **`make_step(seed, n=100)`**: y = 14 + 12·1(x > 25) + N(0, 3²); x U(8, 40); 60 train, 40 test. Seed 1: tree 17.24 against line 10.29 on linear, 11.46 against 21.42 on step.
- **`make_updays(seed, n=400)`** (homework): momentum and volatility z-scores; P(up) = 0.5 + 0.12·1(mom > 0.5) − 0.12·1(mom < −0.5 and volz > 0.5). Honest test accuracy 57% (seed 3), near the 52% always-down rate.

## Proposed change to course.json

None.

## Engine and canvas limitations

The `tree` canvas can draw a decision tree, with one compromise. Node pills take any text and leaves take values, and an inner node's `value` shows only while that node is collapsed, so a depth slider (`derive` writing `collapse`) grows the tree with each collapsed node showing its prediction. But a node's label cannot be patched, so a node cannot show its question while expanded and its counts while a leaf. The pills carry the counts (*4 D · 1 R*), the branch labels (`p`) carry the questions (*leverage > 3*), and the values carry the predictions. The six bullets in `docs/BACKLOG-INBOX.md` under "Raised later (ensembles level 1)" give the details.
