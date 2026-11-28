# cnn level 3 (A CNN on digits): report

## Files written

All in `app/content/courses/cnn/`, skill `cnn-train` throughout, plus data files in `app/content/data/ai/` (course prefix).

| File | Screens / items | Code widgets |
|---|---|---|
| `l9-reading-digits.json` | 12 screens, 3 quiz, 15 min | `cnn_forward` (supplied exit weights), `confusion`, `per_class_accuracy` |
| `l10-training-the-cnn.json` | 12 screens (one ungraded `trainer`), 3 quiz, 16 min | `train_cnn` (exact 3- and 6-step losses, 10-epoch threshold), `evaluate` with `exit_check` |
| `l11-a-residual-block.json` | 12 screens, 3 quiz, 16 min | `residual_block_forward`, `block_grad_check`, `stuck_epochs` with `deep_vs_residual` |
| `l12-shifted-digits.json` | 12 screens, 3 quiz, 15 min | `shift_images`, `shifted_accuracy` with `margin` |
| `review-3.json` | 9 items, difficulty 2 to 4, `pass: 0.8` | none |
| `homework-3.json` | 7 items, difficulty 3 to 5 | performance `digit_report` (5), `fine_tune` (4, exact 4- and 8-step losses, threshold); `order` (an honest run, one distractor); `longform` (a vendor's chart reader, 10-point rubric, full model memo); three numeric or choice |
| `problems-3.json` | 4 problems, 16 parts, difficulty 4, 5, 4, 3 | none |

Lesson shapes follow the brief. l9: two hard held-out digits (a flagged 1 the net reads at 0.69, an 8 it misreads as 1 at 0.73), the forward pass stepped through its shapes, the confusion matrix (532 of 540, 0.9852), trap "98% on every digit" (digit 8 at 0.9615), learned filters (F13 a horizontal edge detector, F3 its mirror), the all-zeros edge case (class 4 at 0.12), transfer: trade tickets (0.97 headline, 0.70 on amendments). l10: three learning rates on validation, the training loop in a `trainer`, one step as an `order`, 32 steps an epoch, 1,280 gradient entries, `train_cnn`, early stopping (epoch 9), trap: reporting the best of five test scores, edge case: Adam at rate 3 (loss above 4, then one class for every digit), the exit net from supplied weights, what to log. l11: a plain net with two extra 16-to-16 convolutions stuck at $\ln 10$; the skip added; $y = x + F(x)$; 4,640 and 7,370 parameters; $\partial y/\partial x = 1 + w_2 w_1 = 0.8$ on a `graph` with value and gradient lines; trap: shapes that differ (1 by 1 projection, 544 parameters); normalisation (one screen); edge case $F = 0$ in the generalise screen and in a hidden test; forward pointer to the residual stream. l12: a held-out 2 moved one pixel (CNN keeps it, MLP reads 3); a frames slider from −2 to +2; equivariance and pooling; bars of 0, 1 and 2 pixel shifts, one bar per seed; why the CNN still drops (dense layer, l6's windows); augmentation (gap under 0.05); trap "shift-invariant"; edge case: a 7 that loses 3 inked pixels off the edge; the margin rule; transfer: a feed stamped one day late.

## Ops and data added

- `cnn_ops_l3.py` (version 1.0, 8,238 bytes, SHA-256 `a7f76ab7a250f5084a07f64004763acf8fd1ac7665a6bebc12ab2d07f46d0743`; imports the frozen `autograd.py` v1.0, `cnn_ops_l2.py` and `nt_ops_l1.py`): `load_split`, `conv2d` (the level 2 op behind the checks review-cnn asked for: `ValueError` for a bias not of shape (F,), a stride below 1, a negative padding), `init_cnn`, `cnn_logits`, `init_mlp`, `mlp_logits`, `init_res`, `block`, `res_logits`, `predict` and `accuracy` (mini-batches of 256, so im2col stays small, per review-cnn), `confusion`, `shift_images`, `fit` (Adam or gradient descent, optional cosine decay, batches of 32), `load_weights`, `save_weights`. No new differentiable op: the block is a composition; its gradient is checked to $7 \times 10^{-11}$ (`grad_check`) and against plain NumPy central differences.
- `cnn-digits.txt` (120,757 bytes): scikit-learn's `load_digits` as text, one image a line with a split letter (1,005 train, 252 validation, 540 test: `train_test_split(test_size=0.3, stratify=y, random_state=0)`, then 20% of train for validation, `random_state=0`). Shipping it removes `import sklearn` (3.6 s, and the scikit-learn and SciPy wheels) from every graded case. The number script rebuilds it from scikit-learn and compares line for line.
- Weights, rounded to 6 places (the number script evaluates the rounded files): `cnn-w-exit.json` 26,359 bytes (2,730 parameters), `cnn-w-small.json` 13,238 (1,370), `cnn-w-mlp.json` 28,680 (3,010), `cnn-w-mlp-aug.json` 28,674 (3,010), `cnn-w-res.json` 74,510 (7,370). For the main session: `app/content/data/ai/README.md` still says digits are "not a file here"; it needs rows for these six files (digits credit: Alpaydin and Kaynak, UCI, CC BY 4.0; the weights are derived from it). I did not edit the shared README.

## Exit figures (number script, three seeds)

Recipes: exit net 16 filters (2,730 parameters), Adam at 0.02 with cosine decay over 30 epochs, batches of 32, trained on the 1,005 training digits (rate chosen on validation from 0.005, 0.01, 0.02 on seed 0); MLP 64-40-10 (3,010), same recipe. Shift: one pixel right, left, down, up, zero fill; the margin is the gap in mean shifted accuracy.

| seed | CNN held out | CNN shifted | MLP held out | MLP shifted | gap | augmented gap |
|---|---|---|---|---|---|---|
| 0 (shipped) | 0.9852 | 0.6181 | 0.9741 | 0.4468 | 0.1713 | 0.0194 |
| 1 | 0.9852 | 0.6292 | 0.9759 | 0.4454 | 0.1838 | 0.0231 |
| 2 | 0.9907 | 0.6384 | 0.9778 | 0.4477 | 0.1907 | 0.0222 |

Smallest gap over all nine CNN and MLP pairs 0.1704, so the rule is set at 0.10. At two pixels both nets fall below 0.2 (shipped: 0.16 and 0.11). The lessons state only the shipped weights' exact figures and thresholds over the seeds (at least 0.98, gap at least 0.15, augmented MLP above 0.93, augmented CNN above 0.96, augmented gap under 0.05), so a different summation order cannot falsify them. Review F8's single-seed figures are not restated.

## Training cases and their desktop time (Pyodide 0.27.7 in Node, the playthrough's runtime)

- l10 `train_cnn` test 5: 10 epochs of the 8-filter net, about 1.36 s (case limit 5 s plus 4 s; its exact tests train 3 and 6 steps, tens of ms). Threshold 0.90 on validation; three seeds give 0.9365, 0.9722, 0.9722.
- homework `fine_tune` test 5: one epoch on 5,025 augmented images, about 0.66 s (limit 5 s plus 4 s). Threshold 0.85 on shifted validation digits; three seeds give 0.90 to 0.905.
- Evaluation cases: residual net on 540 digits 0.39 s, four shifts of both nets 0.11 s, the forward pass on 540 digits 0.04 s.
- l10 `trainer`: about 0.14 s an epoch; 10 epochs reproduce the recorded rate-0.01 curve.
- The exit net (30 epochs at about 0.15 s each) and the residual net (about 1.8 s an epoch in Pyodide) are trained only in the number script; graded cases run them forward or fine-tune one epoch.

## Gates

1. Validator: `node tools/validate.mjs` 0 errors; no `[ai-mutants]` or `[source-ban]` warning on level 3 files. Advisory warnings remain: point hints without highlight, ladder canvas-kind changes, `O2-long-sentence`, three problem screens without a canvas (an `order` and two choice screens).
2. Voice: `voice-scan.py 35` on the course: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `docs/reports/cnn-L3-numbers.py` through `node tools/run-number-scripts.mjs --python <venv> --only cnn-L3`, strict: 595 checks, exit 0, 63 s (about 50 s of it the training runs). Route B: the split rebuilt from scikit-learn; every forward pass on the shipped weights by plain NumPy windows and loops, agreeing with the module to 1e-10, with every held-out top score at least 1e-7 above the second (so predictions do not depend on summation order); counts from arrays; every training figure from three seeds; values recorded once (the lesson curves) checked within 0.02 of the rerun. All 12 code widgets run (38 mutants) and every exact value in their tests is recomputed. Writing it caught one wrong slip value in problems-3 (a column precision of 0.9375 that is 0.9167).
4. Code in Pyodide: `node tools/grade-all.mjs --code --local-cdn <pkgs>` on all seven files: 76 widgets graded, 12 Python widgets run, 0 failures.
5. Playthrough: all seven files with `--local-cdn <pkgs> --mobile` (desktop and 440 px): all passed; homework "1 performance starter fail" as required. See the playthrough line below for the final run.
6. Same-course reuse: `node tools/same-course-reuse.mjs --all` lists nothing for cnn (two retold sentences in problems-3 were reworded).
7. Performance task: `docs/reports/cnn-3-perf.md`; `node tools/perf-reports.mjs` reports no missing part.

Playthrough (final run after the last edit): l9, l10, l11, l12, review-3, homework-3 and problems-3 all passed at desktop and 440 px.

## Choices that differ from the brief

- Exit bar: 0.98 held out, as the brief and `docs/briefs/ai-strand-curriculum.md` set it (the wave prompt said 95%; 0.98 meets both).
- The "spike's 8-filter net" is the course's own layout with 8 filters (padding 1, pool, 1,370 parameters), so one `init_cnn` and `cnn_logits` serve every lesson; the spike's own net had no pool.
- `train_cnn` takes the validation split as arguments: `train_cnn(X_tr, y_tr, X_va, y_va, epochs, lr, seed)`.
- l11's hook: with He starts and Adam, two extra 16-to-16 layers train as well as or better than the shallow net (measured), so the claim in the brief does not hold as written. The recorded curves use plain gradient descent at 0.05 and extra filters started small (sd 0.01), where the plain deep net sits at the guessing loss for 2 to 4 epochs and stays above the shallow net for all 6, while the residual net is below the shallow net throughout (three seeds). The lesson says how the curves were made.
- l10's diverging rate: the stable cross-entropy never gives NaN, so the edge case shows the loss jumping above 4 and the net collapsing to one class (val about 0.10), stated as thresholds.

## Proposed course.json change

None.
