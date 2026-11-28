# cnn level 3 (A CNN on digits): second-reader findings

Scope: `app/content/courses/cnn/` level 3 (`l9-reading-digits`, `l10-training-the-cnn`, `l11-a-residual-block`, `l12-shifted-digits`, `review-3`, `homework-3`, `problems-3`), `app/content/data/ai/cnn_ops_l3.py`, `cnn-digits.txt` and the five `cnn-w-*.json` weight files, at `01b3683f`. Context read: `docs/briefs/cnn.md` Level 3, `docs/reports/cnn-L3.md`, `docs/reports/cnn-3-perf.md`, `docs/reviews/review-cnn.md`, `docs/AUTHORING.md` section 9.
Method: `docs/reports/cnn-L3-numbers.py` run through `node tools/run-number-scripts.mjs --only cnn-L3` (one BLAS thread, 58 s, exit 0) and directly with default threads (4) and `ZQ_NUMBERS_STRICT=1` (2 min 8 s, 595 of 595, 0 uncovered on-screen numbers, 6 literals); the five seed-0 recipes retrained by my own script under 1 and 4 threads and compared with the shipped files entry by entry; the split checked for shared images; every forward pass, confusion count, probability, filter, shift and accuracy quoted in the level recomputed with my own plain-loop convolution and pooling (no im2col, no autograd); the new module's differentiable paths checked by my own float64 central differences (h = 1e-6); `grade-all.mjs --file <f> --code --local-cdn <pkgs>` on each of the 7 files alone (0 failures); every code widget's solution timed per hidden test against its page limit through `tools/code-runner.mjs` (one worker); 57 wrong solutions of my own plus, for each of the 12 code widgets, the model solution with the starter's comments kept, run through the same harness (appendix); three proposed extra tests run against the model solutions and the survivors on scratch specs; `validate.mjs` (0 errors) and `voice-scan.py 35` on the course (0 over 35 words, 0 explanations over three sentences); prose read for false or loose claims, American spelling, em-dashes and exclamation marks (none found).
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, teaching issue or a test that misses what it claims; note = style or small gap.

Counts: 2 errors, 8 warnings, 11 notes. Wrong solutions: 12 of 57 survive (appendix). Leakage: none found.

## Number script, data and weights (no finding unless listed)

- The script recomputes and passes under both thread settings, so every stated figure holds at its stated precision either way. The lessons state the shipped weights' exact figures (from rounded files, every held-out top score at least 1e-7 above the second) and only thresholds over seeds, so a different summation order cannot move them.
- `cnn-digits.txt` is `load_digits` split 70/30 by class (seed 0) and then 20% of train for validation (seed 0); the script rebuilds it line for line. No image appears in two splits (1,005, 252 and 540 unique images, no exact duplicates across them). Class counts are 52 to 55 on test and 24 to 26 on validation.
- Weights: retraining each seed-0 recipe with `cnn_ops_l3.fit` gives arrays that round to the shipped files exactly at 6 decimals (`cnn-w-exit`, `cnn-w-small`, `cnn-w-mlp`, `cnn-w-res`: `round(retrained, 6) == shipped` for every array; `cnn-w-mlp-aug` within 5e-7), under 1 thread and under 4. So the files are what the stated recipes write.
- Leakage: none. The exit net and the MLP train on the 1,005 training digits only; the augmented sets are built from those alone; the rate (0.02 of 0.005, 0.01, 0.02) is chosen on validation; the shipped seed is fixed at 0 in advance and is not the best (test 0.9852, 0.9852, 0.9907 for seeds 0 to 2); the fine-tune is scored on shifted validation digits; every lesson scores fixed weights. The exit accuracy of each seed is read once on test. Two test-side touches remain, neither a model choice (the number-script note below).
- `cnn_ops_l3.py` is correct. My central differences, largest elementwise |a - b| / (|a| + |b|) with a floor of 1e-4 times the array's largest gradient: `conv2d` at padding 1, stride 1 (input, filters, bias) 1.5e-7; at padding 0, stride 2 on a 5 by 6 map (a stride that does not divide) 2.2e-8; `block` with the skip 2.7e-7 and without 1.7e-7; `mlp_logits` with cross-entropy 1.6e-7. Whole nets with cross-entropy, norm-based (the `grad_check` measure): `cnn_logits` 6.5e-10 and `res_logits` (all 8 arrays) 3.2e-9 on random inputs and biases; `cnn_logits` at the shipped exit weights on three held-out digits 5.8e-7, the excess coming from ReLU and max-pool ties on blank regions. All below 1e-6. `conv2d` raises `ValueError` for a bias not of shape (F,), a stride below 1 and a negative padding, as review-cnn asked. `shift_images` equals a pixel loop for every shift up to 3.
- Frozen modules: `autograd.py` (SHA-256 `5917d4ec...`), `cnn_ops_l2.py` (`a783b130...`) and `nt_ops_l1.py` (`9c1391a3...`) are unchanged since their creating commits (`db1e8548`, `10a24f4c`). Every level 3 widget ships them by path through `data`, none inline, so the page loads the canonical bytes; the inline copies in `l4` are byte-identical to the files.
- Timing (solution alone, desktop Node Pyodide, per hidden test against its page limit): the two training cases are the tightest, `l10` screens[5] test 5 at 1,099 ms of 9,000 (8.2 times) and `homework-3` items[1] test 5 at 705 ms of 9,000 (12.8 times); every other case is at least 148 times inside its limit (largest: `homework-3` items[0] test 2, 255 ms of 38,000). None is under 3 times, so a phone 3 to 5 times slower stays inside. `grade-all.mjs --file` alone: l9 4.6 s, l10 13.3 s, l11 6.7 s, l12 6.1 s, review 0.3 s, homework 12.0 s, problems 0.3 s, 0 failures each.
- Exit bar: every file uses 0.98 held out, as the brief and the strand curriculum set it (the wave prompt said 95%; 0.98 meets both). See the `l10` screens[9] warning: a 0.95 bar passes that widget's tests.

## Level 3 lessons

- app/content/courses/cnn/l10-training-the-cnn.json | screens[0] options[2].why, explain | error | "It is still climbing after 10 epochs" and "Too small a rate is still learning after 10 epochs (0.889)": the rate-0.001 curve on the chart is 0.893, 0.889, 0.889, 0.889 over epochs 7 to 10. It has stopped climbing; it ends lowest. | why: "It ends lowest, at 0.889, and has not risen since epoch 7: too slow for 10 epochs." Explain: "Too small a rate ends lowest (0.889); too large a rate wobbles (0.917). So we choose rate 0.01, on validation and never on test."
- app/content/courses/cnn/l11-a-residual-block.json | screens[6] explain, feedback.correct | error | "Either way the identity path carries $x$ unchanged" and "the identity path stays clean" are false for both nets named. The original ResNet block (He et al. 2016) applies a ReLU after the sum, $y = \mathrm{ReLU}(x + F(x))$; the original transformer applies layer norm after the sum, to the stream itself (post-norm). Only the later pre-activation ResNet and pre-norm transformers keep the path clean. The keyed answer (batch norm inside $F$, after each convolution) is right. | Explain: "The original ResNet puts batch norm after each convolution inside $F$, with a ReLU after the sum; later ResNets dropped that ReLU. Most transformers now put layer norm at the start of each $F$, which leaves the identity path clean." feedback.correct: "Inside $F$, after each convolution, never on the identity path."
- app/content/courses/cnn/l10-training-the-cnn.json | screens[9] tests | warning | `exit_check` is tested on the exit and 8-filter nets (0.9852 and 0.9241) and a planted set at exactly 0.98, so nothing sits between 0.9241 and 0.98. Three wrong solutions pass all 5 tests (appendix): scoring the validation split instead of `X_test` (0.992, the trap this lesson teaches), a bar of 0.95 and a bar of 0.97. | Add test 6: `{"setup": "_yf = y_te.copy(); _ok = np.flatnonzero(cnn_logits(exit_params, X_te).data.argmax(axis=1) == y_te)[:6]; _yf[_ok] = (_yf[_ok] + 1) % 10", "call": "exit_check(exit_params, X_te, _yf)", "expect": "False", "compare": "equal"}` (526/540 = 0.9741). Run on a scratch copy: the model solution passes, and all three survivors fail test 6. Add a `test-6` line: "Score the test images you are given, against a bar of 0.98."
- app/content/courses/cnn/l10-training-the-cnn.json | screens[5] tests | warning | A `train_cnn` that keeps the parameters of the epoch with the best test accuracy (early stopping on test, this lesson's trap) passes all 6 tests (appendix). Tests 2 and 3 run 1 and 2 epochs, where the last epoch is also the best on test. | Take the test split out of reach: load with `X_tr, y_tr, X_va, y_va, _, _ = load_split()` in the starter and solution, and make test 6 `zq_no('fit', 'X_te', 'y_te')` with the line "Train and choose on the training and validation splits only; the test split is not for this function."
- app/content/courses/cnn/l10-training-the-cnn.json, homework-3.json | l10 screens[5] tests; homework items[1] tests | warning | Every test passes `lr = 0.01`, so a loop that ignores `lr` and steps at 0.01 passes all 6 tests of both widgets (appendix). The `test-5` line of l10 ("Check the update uses `lr`") can never show for that bug. | Run test 3 of l10 and test 4 of the homework at `lr = 0.02`, with the exact losses from the number script (to $10^{-7}$ relative), and move the `lr` sentence to that test's line.
- app/content/courses/cnn/homework-3.json | items[0] h-perf-report, tests 5 to 8 and how | warning | The performance task never tests the margin threshold. A report whose rule is "any lead" (`gap > 0`) or a gap of 0.05 passes all 8 tests (appendix). The how says test 7 checks "the 8-filter net (held-out bar not met)", but that net also fails the margin (mean shifted 0.5037 against the MLP's 0.4468, a gap of 0.0569), so test 7 passes a report that never checks the bar; only test 8 does. | Add test 9: `{"setup": "_mb = [0.7 * p + 0.3 * q for p, q in zip(mlp, load_weights('cnn-w-mlp-aug.json'))]", "call": "digit_report(cnn, _mb, X_te, y_te)['exit']", "expect": "False", "compare": "equal"}`: an MLP part way to the augmented one, mean shifted 0.5426, gap 0.0755 (claim it in the number script). Run on a scratch copy: the model passes and both survivors fail test 9. Reword the how: "the 8-filter net (both parts fail)".
- app/content/courses/cnn/l11-a-residual-block.json | screens[9] tests | warning | A `block_grad_check` that never calls `grad_check`, runs `backward()` and returns an error of 0.0 passes all 4 tests (appendix): test 2 only asks for an error below $10^{-6}$. A source check cannot help, since the starter imports `grad_check` (a `not zq_no('grad_check')` test still lets it through, run on a scratch copy). | Make test 2 `bool(1e-13 < block_grad_check(x, params, M)[1] < 1e-6)` (the model returns 3.0e-11), with a `test-2` line: "Return the relative error `grad_check` reports."
- app/content/courses/cnn/l11-a-residual-block.json | screens[0] explain, screens[7] prose | warning | The hook shows two extra 16-to-16 layers stuck at guessing, but only because they start at sd 0.01 and train by plain gradient descent (caption). The author measured that with He starts and Adam the plain deeper net trains as well as the shallow one or better (`cnn-L3.md`). The lesson never says so, so a learner takes away that two plain layers break training. | Add to screens[0] explain: "With He starts and Adam these two layers train well: the skip matters most when the start is small or the net is tens of layers deep, as in He et al. 2016."
- app/content/courses/cnn/l12-shifted-digits.json, homework-3.json, problems-3.json | l12 screens[5] explain; homework items[6] options[2].why; problems-3 items[2] parts[3] explain | warning | "Shifted copies teach the MLP what convolution builds in" overclaims. The augmented nets are scored on the same four one-pixel shifts they trained on. At two pixels, which they never saw, the augmented MLP scores 0.356, 0.366, 0.355 against the augmented CNN's 0.458, 0.441, 0.419 (seeds 0 to 2, my run of the script's recipe): the gap returns to 0.065 to 0.10. The homework's "it reappears for shifts the copies did not cover" is true, but no check or screen shows it. | l12 explain: "Shifted copies teach the MLP these four shifts: its accuracy rises from 0.45 to 0.95, and the gap falls under 0.05. At two pixels, which the copies never showed, the gap returns to about 0.07." Have the script compute the two-pixel figures over three seeds and claim them. Problems explain: "Shifted copies teach the MLP the shifts they show."
- app/content/courses/cnn/l9-reading-digits.json | screens[6] explain | warning | "Accuracy is an average over classes" is loose: it averages over the 540 digits, so each class counts by its size. Screen 10 says it correctly ("Accuracy averages over every digit"). | "Accuracy averages over all 540 digits, so one weak class barely moves it: every 0, 1, 4, 6 and 7 is right, while 8 drops to 0.9615. Two of the eight misreads are 8s read as 1."
- app/content/courses/cnn/l9-reading-digits.json | screens[6] prose | note | The colleague says "about 99%" under the title "98% on every digit?", and the headline is 0.9852. | "...reads every digit about 98% of the time."
- app/content/courses/cnn/l9-reading-digits.json | quiz[1] feedback.byKey.col | note | "Every 3 is not read right" reads as "no 3 is read right". The value 1 is the full mark (100%), not a column slip. | Rename the id to `all-right` and write "Not every 3 is read right: 2 of the 50 are misread."
- app/content/courses/cnn/l9-reading-digits.json | screens[5] byKey.test-2; screens[7] byKey.test-2 | note | Both repeat their `test-1` line about rows and columns, but that bug always fails test 1 first, so neither line can show for it. In screens[5], test 2 is the first failure of a cell assigned instead of counted (appendix W2). | screens[5]: "Count with `+=`: two images of class 0 read as 1 make a 2 in that cell." screens[7]: drop the line.
- app/content/courses/cnn/l9-reading-digits.json | screens[8] options[2].why | note | "F7 is strongest along its middle row": its largest weight is -2.0, bottom left, and its middle row over a negative bottom row also rewards ink above background. F13 is still the best answer (4.34 against 3.22 on two inked rows over a blank one). | "F7's middle row is its positive row: it answers a thin horizontal stroke through the centre best."
- app/content/courses/cnn/l11-a-residual-block.json | screens[8] tests | note | Every test input is the output of a ReLU, so a block that adds $\mathrm{ReLU}(x)$ instead of $x$ passes all 6 (appendix W2). It is the same function on this net's inputs, but not the block the prose defines. The `test-4` line can show only for code that passes test 2's exact values yet changes $x$ when $F = 0$. | Add a case on `h - 0.5` (signed inputs) against the model run; drop or keep the `test-4` line.
- app/content/courses/cnn/l11-a-residual-block.json | screens[10] tests | note | Comparing each curve's lowest loss instead of its last passes all 6 (appendix W3): in every curve tested, the minimum is the last entry. | Add `deep_vs_residual({'plain': [2.3, 0.2, 0.5], 'residual': [1.9, 0.3, 0.4]})` expecting `'residual'`.
- app/content/courses/cnn/l12-shifted-digits.json | screens[2] explain; screens[4] prose | note | "The CNN learned shapes, wherever they sit" overclaims: screen 4 says the dense layer after pooling is tied to positions. Screen 4 also says the dense layer "has one weight for each of the 256 pooled positions, just as the MLP has one for each pixel". $\mathbf{V}$ has 10 weights per pooled value and the MLP 40 per pixel. | Screen 2: "The CNN's filters learned strokes wherever they sit, and pooling absorbs part of the move." Screen 4: "After it, the dense layer has its own 10 weights for each of the 256 pooled values, just as the MLP has its own 40 for each pixel."
- app/content/courses/cnn/l12-shifted-digits.json, review-3.json | l12 screens[9] `margin`; review-3 items[8] r-margin | note | No test sits at the boundary, so a strict `> 0.10` passes all 6 (appendix W1). A boundary test would also show a float trap: the model solution gives `margin(0.57, 0.47) == False` ($0.57 - 0.47 = 0.09999999999999998$), while r-margin keys 0.57 as enough. | State the rule with a small tolerance in the solution (`cnn_acc - mlp_acc >= 0.10 - 1e-9`) and in the prose, and add the test `margin(0.57, 0.47)` expecting `True`. Or compare counts of right answers (a gap of 216 of 2,160 shifted images).
- app/content/courses/cnn/review-3.json | whole file | note | 9 items, and `sequence` requires `cnn/L3`. AUTHORING section 11 asks for 10 or more review items in a level that others require, so that a second test-out paper is all new. | Add one item, for example the stride-2, 32-filter projection count of l11 ($32 \times 17 = 544$).
- app/content/courses/cnn/problems-3.json | items[3] parts[3] wrong 'high-last' (24) | note | 24 matches no slip: it is neither the highest nor the last epoch, and its line ("Epoch 24 is lower still") explains nothing. | Replace it with the epoch of lowest training loss if the table gave one, or drop it and keep 'last' (25).
- docs/reports/cnn-L3-numbers.py | sections 5 and 6 | note | Four gaps. (1) The weight files are checked only by accuracy within 0.005 of a retrain, although they equal `round(retrained, 6)` exactly, so the claim can be exact. (2) `TE` scores the rate-sweep candidates (`exitlr`) on test; the scores are never used, but "test once" should hold literally. (3) The clear-margin rule (0.10) and the augmentation statements (above 0.93, above 0.96, under 0.05) are set from test-split results. No model is chosen by them, but the rule is calibrated on the data that judges it. (4) Uncomputed qualitative claims: the gap returning at two pixels (homework items[6]) and "needed no augmentation for most of its tolerance". Also, `save_weights` defaults to 7 decimals while the files and the report use 6. | Claim `all(np.array_equal(np.round(a, 6), b) ...)` for every shipped file. Drop `exitlr` from `KIND`. Set or recheck the margin rule on shifted validation digits, or say in l12 screens[10] that it was set on the held-out runs. Compute the two-pixel augmented figures. Set `digits=6`.

## Appendix: wrong solutions run through the grader

How: each source below was graded by `tools/code-runner.mjs` (the page's own harness, worker grader and per-case limits, the same path `grade-all.mjs --code` uses) against the widget's hidden tests, under the local Pyodide; the line gives the first failing test (the key the page shows) and every failing test, or that the source passes every test. For every widget the first entry (C0) is the model solution with the starter's comment lines kept inside the function, as a learner who types into the starter leaves them; all 12 pass. Results: 57 wrong solutions, 45 caught and 12 that survive: l10 `train_cnn` W2 and W3, l10 `exit_check` W1, W2 and W3, l11 block W2 (the same function on non-negative inputs), l11 `block_grad_check` W1, l11 curves W3, l12 `margin` W1, homework `digit_report` W1 and W2, homework `fine_tune` W1. The classes asked for: accuracy on the validation split reported as test survives in l10 `exit_check` (W1) and is caught in l12 (W4) and the homework (W4); choosing the epoch by test accuracy survives in l10 `train_cnn` (W2); a ReLU between $F$ and the sum (l11 W1), the ReLU between the convolutions dropped (W4) and a ReLU after the sum (the authors' mutant 2) are caught; a ReLU on the identity path survives only because every input is non-negative (W2); normalisation statistics from the whole set are caught (l9 W2, l10 W6, homework W6); no level 3 widget writes a pooling backward, so the max-pool gradient spread to every cell has no target here, and its forward analogue, an average pool, is caught (l9 W1); no code widget counts parameters, and dropping biases is caught where they enter (l9 W4, l11 W3; the numeric no-bias distractors grade correctly in `grade-all`); labels off by one are caught everywhere (l9 confusion W1 and W3, per_class W1, l10 W7 and evaluate W4, l12 W5). The authors' 38 mutants pass `grade-all` on the original files (each first fails its named test).

### l9-reading-digits screens[3] `cnn_forward` (6 hidden tests)
- C0 (model + starter comments): passes every test (correct)

```python
import numpy as np
from autograd import Tensor, softmax
from cnn_ops_l2 import conv2d, maxpool2d
from cnn_ops_l3 import load_split, load_weights

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
params = load_weights('cnn-w-exit.json')   # [W, b, V, c]


def cnn_forward(X, params):
    # X has shape (N, 1, 8, 8); return (N, 10) probabilities
    W, b, V, c = params
    h = conv2d(X, W, b, 1, 1).relu()
    h = maxpool2d(h, 2)
    z = h.reshape(len(X), -1) @ V + c
    return softmax(z)
```
- W1 average pool for max pool: caught, key test-3; failing 3, 4, 5

```python
import numpy as np
from autograd import Tensor, softmax
from cnn_ops_l2 import conv2d, maxpool2d, avgpool2d
from cnn_ops_l3 import load_split, load_weights

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
params = load_weights('cnn-w-exit.json')   # [W, b, V, c]


def cnn_forward(X, params):
    W, b, V, c = params
    h = conv2d(X, W, b, 1, 1).relu()
    h = avgpool2d(h, 2)
    z = h.reshape(len(X), -1) @ V + c
    return softmax(z)
```
- W2 inputs standardised with the statistics of the whole batch passed in: caught, key test-3; failing 3, 4, 5

```python
import numpy as np
from autograd import Tensor, softmax
from cnn_ops_l2 import conv2d, maxpool2d
from cnn_ops_l3 import load_split, load_weights

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
params = load_weights('cnn-w-exit.json')   # [W, b, V, c]


def cnn_forward(X, params):
    W, b, V, c = params
    X = (X - X.mean()) / X.std()
    h = conv2d(X, W, b, 1, 1).relu()
    h = maxpool2d(h, 2)
    z = h.reshape(len(X), -1) @ V + c
    return softmax(z)
```
- W3 softmax down the columns (across images): caught, key test-2; failing 2, 3, 4, 5

```python
import numpy as np
from autograd import Tensor, softmax
from cnn_ops_l2 import conv2d, maxpool2d
from cnn_ops_l3 import load_split, load_weights

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
params = load_weights('cnn-w-exit.json')   # [W, b, V, c]


def cnn_forward(X, params):
    W, b, V, c = params
    h = conv2d(X, W, b, 1, 1).relu()
    h = maxpool2d(h, 2)
    z = h.reshape(len(X), -1) @ V + c
    e = np.exp(z.data - z.data.max())
    return e / e.sum(axis=0)
```
- W4 dense layer without its bias c: caught, key test-4; failing 4

```python
import numpy as np
from autograd import Tensor, softmax
from cnn_ops_l2 import conv2d, maxpool2d
from cnn_ops_l3 import load_split, load_weights

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
params = load_weights('cnn-w-exit.json')   # [W, b, V, c]


def cnn_forward(X, params):
    W, b, V, c = params
    h = conv2d(X, W, b, 1, 1).relu()
    h = maxpool2d(h, 2)
    z = h.reshape(len(X), -1) @ V
    return softmax(z)
```
- W5 stride 2 in the convolution: caught, key test-1; failing 1 (ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc si), 2 (ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc si), 3 (ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc si), 4 (ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc si), 5 (ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc si)

```python
import numpy as np
from autograd import Tensor, softmax
from cnn_ops_l2 import conv2d, maxpool2d
from cnn_ops_l3 import load_split, load_weights

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
params = load_weights('cnn-w-exit.json')   # [W, b, V, c]


def cnn_forward(X, params):
    W, b, V, c = params
    h = conv2d(X, W, b, 2, 1).relu()
    h = maxpool2d(h, 2)
    z = h.reshape(len(X), -1) @ V + c
    return softmax(z)
```

### l9-reading-digits screens[5] `confusion` (5 hidden tests)
- C0 (model + starter comments): passes every test (correct)

```python
import numpy as np


def confusion(y_true, y_pred, k):
    # a k by k array of counts: row = true class, column = predicted class
    cm = np.zeros((k, k), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[t, p] += 1
    return cm
```
- W1 labels off by one (cm[t - 1, p - 1]): caught, key test-1; failing 1, 2, 4

```python
import numpy as np


def confusion(y_true, y_pred, k):
    cm = np.zeros((k, k), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[t - 1, p - 1] += 1
    return cm
```
- W2 assignment instead of a count: caught, key test-2; failing 2, 4, 5

```python
import numpy as np


def confusion(y_true, y_pred, k):
    cm = np.zeros((k, k), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[t, p] = 1
    return cm
```
- W3 predicted label off by one (cm[t, p - 1]): caught, key test-1; failing 1, 2, 4

```python
import numpy as np


def confusion(y_true, y_pred, k):
    cm = np.zeros((k, k), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[t, p - 1] += 1
    return cm
```

### l9-reading-digits screens[7] `per_class_accuracy` (4 hidden tests)
- C0 (model + starter comments): passes every test (correct)

```python
import numpy as np


def per_class_accuracy(cm):
    # the share of each true class (each row) that the net reads right
    cm = np.asarray(cm, dtype=float)
    return np.diag(cm) / cm.sum(axis=1)
```
- W1 diagonal shifted by one (labels off by one): caught, key test-1; failing 1, 2, 3, 4

```python
import numpy as np


def per_class_accuracy(cm):
    cm = np.asarray(cm, dtype=float)
    return np.roll(np.diag(cm), 1) / cm.sum(axis=1)
```
- W2 error rate per class: caught, key test-1; failing 1, 2, 3, 4

```python
import numpy as np


def per_class_accuracy(cm):
    cm = np.asarray(cm, dtype=float)
    return 1 - np.diag(cm) / cm.sum(axis=1)
```

### l10-training-the-cnn screens[5] `train_cnn` (6 hidden tests)
- C0 (model + starter comments): passes every test (correct)

```python
import numpy as np
from autograd import Tensor, cross_entropy
from cnn_ops_l3 import load_split, init_cnn, cnn_logits, accuracy
from nt_ops_l1 import adam_step, minibatch_indices

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()


def train_cnn(X_tr, y_tr, X_va, y_va, epochs, lr, seed):
    # He start, 8 filters
    # one Adam step on this batch
    # validation accuracy of this epoch
    params = init_cnn(8, seed)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t, curve = 0, []
    for epoch in range(epochs):
        for idx in minibatch_indices(len(X_tr), 32, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(cnn_logits(ts, X_tr[idx]), y_tr[idx])
            loss.backward()
            t += 1
            params, m, v = adam_step(params, [p.grad for p in ts], m, v, t, lr)
        curve.append(accuracy(cnn_logits, params, X_va, y_va))
    return params, curve
```
- W1 curve measured on the test split: caught, key test-4; failing 4

```python
import numpy as np
from autograd import Tensor, cross_entropy
from cnn_ops_l3 import load_split, init_cnn, cnn_logits, accuracy
from nt_ops_l1 import adam_step, minibatch_indices

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()


def train_cnn(X_tr, y_tr, X_va, y_va, epochs, lr, seed):
    params = init_cnn(8, seed)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t, curve = 0, []
    for epoch in range(epochs):
        for idx in minibatch_indices(len(X_tr), 32, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(cnn_logits(ts, X_tr[idx]), y_tr[idx])
            loss.backward()
            t += 1
            params, m, v = adam_step(params, [p.grad for p in ts], m, v, t, lr)
        curve.append(accuracy(cnn_logits, params, X_te, y_te))
    return params, curve
```
- W2 keeps the epoch with the best test accuracy (early stopping on test): SURVIVES (passes every test)

```python
import numpy as np
from autograd import Tensor, cross_entropy
from cnn_ops_l3 import load_split, init_cnn, cnn_logits, accuracy
from nt_ops_l1 import adam_step, minibatch_indices

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()


def train_cnn(X_tr, y_tr, X_va, y_va, epochs, lr, seed):
    params = init_cnn(8, seed)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t, curve = 0, []
    best, keep = -1.0, None
    for epoch in range(epochs):
        for idx in minibatch_indices(len(X_tr), 32, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(cnn_logits(ts, X_tr[idx]), y_tr[idx])
            loss.backward()
            t += 1
            params, m, v = adam_step(params, [p.grad for p in ts], m, v, t, lr)
        curve.append(accuracy(cnn_logits, params, X_va, y_va))
        te = accuracy(cnn_logits, params, X_te, y_te)
        if te > best:
            best, keep = te, params
    return keep, curve
```
- W3 learning rate fixed at 0.01, lr ignored: SURVIVES (passes every test)

```python
import numpy as np
from autograd import Tensor, cross_entropy
from cnn_ops_l3 import load_split, init_cnn, cnn_logits, accuracy
from nt_ops_l1 import adam_step, minibatch_indices

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()


def train_cnn(X_tr, y_tr, X_va, y_va, epochs, lr, seed):
    params = init_cnn(8, seed)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t, curve = 0, []
    for epoch in range(epochs):
        for idx in minibatch_indices(len(X_tr), 32, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(cnn_logits(ts, X_tr[idx]), y_tr[idx])
            loss.backward()
            t += 1
            params, m, v = adam_step(params, [p.grad for p in ts], m, v, t, 0.01)
        curve.append(accuracy(cnn_logits, params, X_va, y_va))
    return params, curve
```
- W4 validation accuracy taken before each epoch trains: caught, key test-4; failing 4

```python
import numpy as np
from autograd import Tensor, cross_entropy
from cnn_ops_l3 import load_split, init_cnn, cnn_logits, accuracy
from nt_ops_l1 import adam_step, minibatch_indices

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()


def train_cnn(X_tr, y_tr, X_va, y_va, epochs, lr, seed):
    params = init_cnn(8, seed)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t, curve = 0, []
    for epoch in range(epochs):
        curve.append(accuracy(cnn_logits, params, X_va, y_va))
        for idx in minibatch_indices(len(X_tr), 32, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(cnn_logits(ts, X_tr[idx]), y_tr[idx])
            loss.backward()
            t += 1
            params, m, v = adam_step(params, [p.grad for p in ts], m, v, t, lr)
    return params, curve
```
- W5 trains on training plus validation digits (leak): caught, key test-2; failing 2, 3

```python
import numpy as np
from autograd import Tensor, cross_entropy
from cnn_ops_l3 import load_split, init_cnn, cnn_logits, accuracy
from nt_ops_l1 import adam_step, minibatch_indices

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()


def train_cnn(X_tr, y_tr, X_va, y_va, epochs, lr, seed):
    params = init_cnn(8, seed)
    X_tr = np.concatenate([X_tr, X_va]); y_tr = np.concatenate([y_tr, y_va])
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t, curve = 0, []
    for epoch in range(epochs):
        for idx in minibatch_indices(len(X_tr), 32, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(cnn_logits(ts, X_tr[idx]), y_tr[idx])
            loss.backward()
            t += 1
            params, m, v = adam_step(params, [p.grad for p in ts], m, v, t, lr)
        curve.append(accuracy(cnn_logits, params, X_va, y_va))
    return params, curve
```
- W6 inputs standardised with mean and sd of the whole training set: caught, key test-2; failing 2, 3, 4

```python
import numpy as np
from autograd import Tensor, cross_entropy
from cnn_ops_l3 import load_split, init_cnn, cnn_logits, accuracy
from nt_ops_l1 import adam_step, minibatch_indices

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()


def train_cnn(X_tr, y_tr, X_va, y_va, epochs, lr, seed):
    params = init_cnn(8, seed)
    mu, sd = X_tr.mean(), X_tr.std()
    X_tr = (X_tr - mu) / sd
    X_va = (X_va - mu) / sd
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t, curve = 0, []
    for epoch in range(epochs):
        for idx in minibatch_indices(len(X_tr), 32, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(cnn_logits(ts, X_tr[idx]), y_tr[idx])
            loss.backward()
            t += 1
            params, m, v = adam_step(params, [p.grad for p in ts], m, v, t, lr)
        curve.append(accuracy(cnn_logits, params, X_va, y_va))
    return params, curve
```
- W7 labels off by one in the loss: caught, key test-2; failing 2, 3, 5

```python
import numpy as np
from autograd import Tensor, cross_entropy
from cnn_ops_l3 import load_split, init_cnn, cnn_logits, accuracy
from nt_ops_l1 import adam_step, minibatch_indices

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()


def train_cnn(X_tr, y_tr, X_va, y_va, epochs, lr, seed):
    params = init_cnn(8, seed)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t, curve = 0, []
    for epoch in range(epochs):
        for idx in minibatch_indices(len(X_tr), 32, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(cnn_logits(ts, X_tr[idx]), (y_tr[idx] + 1) % 10)
            loss.backward()
            t += 1
            params, m, v = adam_step(params, [p.grad for p in ts], m, v, t, lr)
        curve.append(accuracy(cnn_logits, params, X_va, y_va))
    return params, curve
```

### l10-training-the-cnn screens[9] `evaluate, exit_check` (5 hidden tests)
- C0 (model + starter comments): passes every test (correct)

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, cnn_logits

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
exit_params = load_weights('cnn-w-exit.json')     # 16 filters, the exit run
small_params = load_weights('cnn-w-small.json')   # 8 filters, 10 epochs


def evaluate(params, X, y):
    # the share of images whose highest score is the true class
    pred = cnn_logits(params, X).data.argmax(axis=1)
    return float((pred == y).mean())


def exit_check(params, X_test, y_test):
    # True when held-out accuracy is at least 0.98
    return evaluate(params, X_test, y_test) >= 0.98
```
- W1 scores the validation split, ignores X_test (validation reported as test): SURVIVES (passes every test)

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, cnn_logits

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
exit_params = load_weights('cnn-w-exit.json')     # 16 filters, the exit run
small_params = load_weights('cnn-w-small.json')   # 8 filters, 10 epochs


def evaluate(params, X, y):
    pred = cnn_logits(params, X).data.argmax(axis=1)
    return float((pred == y).mean())


def exit_check(params, X_test, y_test):
    return evaluate(params, X_va, y_va) >= 0.98
```
- W2 bar at 0.95: SURVIVES (passes every test)

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, cnn_logits

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
exit_params = load_weights('cnn-w-exit.json')     # 16 filters, the exit run
small_params = load_weights('cnn-w-small.json')   # 8 filters, 10 epochs


def evaluate(params, X, y):
    pred = cnn_logits(params, X).data.argmax(axis=1)
    return float((pred == y).mean())


def exit_check(params, X_test, y_test):
    return evaluate(params, X_test, y_test) >= 0.95
```
- W3 bar at 0.97: SURVIVES (passes every test)

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, cnn_logits

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
exit_params = load_weights('cnn-w-exit.json')     # 16 filters, the exit run
small_params = load_weights('cnn-w-small.json')   # 8 filters, 10 epochs


def evaluate(params, X, y):
    pred = cnn_logits(params, X).data.argmax(axis=1)
    return float((pred == y).mean())


def exit_check(params, X_test, y_test):
    return evaluate(params, X_test, y_test) >= 0.97
```
- W4 labels off by one: caught, key test-1; failing 1, 2, 3, 4, 5

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, cnn_logits

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
exit_params = load_weights('cnn-w-exit.json')     # 16 filters, the exit run
small_params = load_weights('cnn-w-small.json')   # 8 filters, 10 epochs


def evaluate(params, X, y):
    pred = cnn_logits(params, X).data.argmax(axis=1)
    return float((pred == (np.asarray(y) + 1) % 10).mean())


def exit_check(params, X_test, y_test):
    return evaluate(params, X_test, y_test) >= 0.98
```
- W5 error rate: caught, key test-1; failing 1, 2, 3, 4, 5

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, cnn_logits

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
exit_params = load_weights('cnn-w-exit.json')     # 16 filters, the exit run
small_params = load_weights('cnn-w-small.json')   # 8 filters, 10 epochs


def evaluate(params, X, y):
    pred = cnn_logits(params, X).data.argmax(axis=1)
    return float((pred != y).mean())


def exit_check(params, X_test, y_test):
    return evaluate(params, X_test, y_test) >= 0.98
```

### l11-a-residual-block screens[8] `residual_block_forward` (6 hidden tests)
- C0 (model + starter comments): passes every test (correct)

```python
import numpy as np
from cnn_ops_l3 import conv2d, load_split, load_weights

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
W, b, A1, a1, A2, a2, V, c = load_weights('cnn-w-res.json')
h = conv2d(X_te[:2], W, b, 1, 1).relu().data   # (2, 16, 8, 8): the block's input


def residual_block_forward(x, params):
    # y = x + F(x), F = conv(ReLU(conv(x))), both 3 by 3 with padding 1
    A1, a1, A2, a2 = params
    F = conv2d(conv2d(x, A1, a1, 1, 1).relu(), A2, a2, 1, 1).data
    if F.shape != np.shape(x):
        raise ValueError('x and F(x) have different shapes')
    return x + F
```
- W1 ReLU on F before the add (x + ReLU(F)): caught, key test-2; failing 2, 3

```python
import numpy as np
from cnn_ops_l3 import conv2d, load_split, load_weights

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
W, b, A1, a1, A2, a2, V, c = load_weights('cnn-w-res.json')
h = conv2d(X_te[:2], W, b, 1, 1).relu().data   # (2, 16, 8, 8): the block's input


def residual_block_forward(x, params):
    A1, a1, A2, a2 = params
    F = conv2d(conv2d(x, A1, a1, 1, 1).relu(), A2, a2, 1, 1).relu().data
    if F.shape != np.shape(x):
        raise ValueError('x and F(x) have different shapes')
    return x + F
```
- W2 ReLU on the identity path (ReLU(x) + F): SURVIVES (passes every test)

```python
import numpy as np
from cnn_ops_l3 import conv2d, load_split, load_weights

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
W, b, A1, a1, A2, a2, V, c = load_weights('cnn-w-res.json')
h = conv2d(X_te[:2], W, b, 1, 1).relu().data   # (2, 16, 8, 8): the block's input


def residual_block_forward(x, params):
    A1, a1, A2, a2 = params
    F = conv2d(conv2d(x, A1, a1, 1, 1).relu(), A2, a2, 1, 1).data
    if F.shape != np.shape(x):
        raise ValueError('x and F(x) have different shapes')
    return np.maximum(x, 0) + F
```
- W3 no biases in F: caught, key test-2; failing 2

```python
import numpy as np
from cnn_ops_l3 import conv2d, load_split, load_weights

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
W, b, A1, a1, A2, a2, V, c = load_weights('cnn-w-res.json')
h = conv2d(X_te[:2], W, b, 1, 1).relu().data   # (2, 16, 8, 8): the block's input


def residual_block_forward(x, params):
    A1, a1, A2, a2 = params
    F = conv2d(conv2d(x, A1, 0 * a1, 1, 1).relu(), A2, 0 * a2, 1, 1).data
    if F.shape != np.shape(x):
        raise ValueError('x and F(x) have different shapes')
    return x + F
```
- W4 no ReLU between the convolutions: caught, key test-2; failing 2, 3

```python
import numpy as np
from cnn_ops_l3 import conv2d, load_split, load_weights

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
W, b, A1, a1, A2, a2, V, c = load_weights('cnn-w-res.json')
h = conv2d(X_te[:2], W, b, 1, 1).relu().data   # (2, 16, 8, 8): the block's input


def residual_block_forward(x, params):
    A1, a1, A2, a2 = params
    F = conv2d(conv2d(x, A1, a1, 1, 1), A2, a2, 1, 1).data
    if F.shape != np.shape(x):
        raise ValueError('x and F(x) have different shapes')
    return x + F
```
- W5 shape checked after the sum (broadcast already done): caught, key test-5; failing 5

```python
import numpy as np
from cnn_ops_l3 import conv2d, load_split, load_weights

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
W, b, A1, a1, A2, a2, V, c = load_weights('cnn-w-res.json')
h = conv2d(X_te[:2], W, b, 1, 1).relu().data   # (2, 16, 8, 8): the block's input


def residual_block_forward(x, params):
    A1, a1, A2, a2 = params
    F = conv2d(conv2d(x, A1, a1, 1, 1).relu(), A2, a2, 1, 1).data
    y = x + F
    if y.shape != np.shape(x):
        raise ValueError('x and F(x) have different shapes')
    return y
```
- W6 the two convolutions in the wrong order of weights (A2 first): caught, key test-2; failing 2, 3, 4

```python
import numpy as np
from cnn_ops_l3 import conv2d, load_split, load_weights

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
W, b, A1, a1, A2, a2, V, c = load_weights('cnn-w-res.json')
h = conv2d(X_te[:2], W, b, 1, 1).relu().data   # (2, 16, 8, 8): the block's input


def residual_block_forward(x, params):
    A1, a1, A2, a2 = params
    F = conv2d(conv2d(x, A2, a2, 1, 1).relu(), A1, a1, 1, 1).data
    if F.shape != np.shape(x):
        raise ValueError('x and F(x) have different shapes')
    return x + F
```

### l11-a-residual-block screens[9] `block_grad_check` (4 hidden tests)
- C0 (model + starter comments): passes every test (correct)

```python
import numpy as np
from autograd import Tensor, grad_check
from cnn_ops_l3 import block

rng = np.random.default_rng(31)
x = rng.standard_normal((1, 2, 4, 4))            # small: grad_check loops over every entry
params = [rng.standard_normal((2, 2, 3, 3)), rng.standard_normal(2), rng.standard_normal((2, 2, 3, 3)), rng.standard_normal(2)]
M = rng.standard_normal((1, 2, 4, 4))            # the loss is sum(block(x) * M)


def block_grad_check(x, params, M):
    # return (the gradient of sum(block(x) * M) with respect to x, grad_check's relative error)
    xt = Tensor(x)
    ts = [Tensor(p) for p in params]
    f = lambda: (block(xt, *ts) * M).sum()
    err = grad_check(f, [xt] + ts)
    return xt.grad.copy(), err
```
- W1 never calls grad_check: backward only, error reported as 0.0: SURVIVES (passes every test)

```python
import numpy as np
from autograd import Tensor, grad_check
from cnn_ops_l3 import block

rng = np.random.default_rng(31)
x = rng.standard_normal((1, 2, 4, 4))            # small: grad_check loops over every entry
params = [rng.standard_normal((2, 2, 3, 3)), rng.standard_normal(2), rng.standard_normal((2, 2, 3, 3)), rng.standard_normal(2)]
M = rng.standard_normal((1, 2, 4, 4))            # the loss is sum(block(x) * M)


def block_grad_check(x, params, M):
    xt = Tensor(x)
    ts = [Tensor(p) for p in params]
    f = lambda: (block(xt, *ts) * M).sum()
    f().backward()
    err = 0.0
    return xt.grad.copy(), err
```
- W2 loss sum(block(x)) * M.sum() (weights summed first): caught, key test-3; failing 3, 4

```python
import numpy as np
from autograd import Tensor, grad_check
from cnn_ops_l3 import block

rng = np.random.default_rng(31)
x = rng.standard_normal((1, 2, 4, 4))            # small: grad_check loops over every entry
params = [rng.standard_normal((2, 2, 3, 3)), rng.standard_normal(2), rng.standard_normal((2, 2, 3, 3)), rng.standard_normal(2)]
M = rng.standard_normal((1, 2, 4, 4))            # the loss is sum(block(x) * M)


def block_grad_check(x, params, M):
    xt = Tensor(x)
    ts = [Tensor(p) for p in params]
    f = lambda: block(xt, *ts).sum() * float(M.sum())
    err = grad_check(f, [xt] + ts)
    return xt.grad.copy(), err
```
- W3 returns M plus the gradient (identity counted twice): caught, key test-3; failing 3, 4

```python
import numpy as np
from autograd import Tensor, grad_check
from cnn_ops_l3 import block

rng = np.random.default_rng(31)
x = rng.standard_normal((1, 2, 4, 4))            # small: grad_check loops over every entry
params = [rng.standard_normal((2, 2, 3, 3)), rng.standard_normal(2), rng.standard_normal((2, 2, 3, 3)), rng.standard_normal(2)]
M = rng.standard_normal((1, 2, 4, 4))            # the loss is sum(block(x) * M)


def block_grad_check(x, params, M):
    xt = Tensor(x)
    ts = [Tensor(p) for p in params]
    f = lambda: (block(xt, *ts) * M).sum()
    err = grad_check(f, [xt] + ts)
    return xt.grad.copy() + M, err
```

### l11-a-residual-block screens[10] `stuck_epochs, deep_vs_residual` (6 hidden tests)
- C0 (model + starter comments): passes every test (correct)

```python
def stuck_epochs(losses, level=2.2):
    # how many epochs, from the first, the loss stays above level
    n = 0
    for v in losses:
        if v > level:
            n += 1
        else:
            break
    return n


def deep_vs_residual(curves):
    # curves = {'plain': [...], 'residual': [...]}: the name of the lower final loss
    if curves['residual'][-1] < curves['plain'][-1]:
        return 'residual'
    return 'plain'
```
- W1 level hard-coded at ln 10 = 2.30: caught, key test-2; failing 2

```python
def stuck_epochs(losses, level=2.2):
    n = 0
    for v in losses:
        if v > 2.30:
            n += 1
        else:
            break
    return n


def deep_vs_residual(curves):
    if curves['residual'][-1] < curves['plain'][-1]:
        return 'residual'
    return 'plain'
```
- W2 compares mean losses, not final: caught, key test-4; failing 4

```python
def stuck_epochs(losses, level=2.2):
    n = 0
    for v in losses:
        if v > level:
            n += 1
        else:
            break
    return n


def deep_vs_residual(curves):
    if sum(curves['residual']) < sum(curves['plain']):
        return 'residual'
    return 'plain'
```
- W3 compares the lowest loss of each curve: SURVIVES (passes every test)

```python
def stuck_epochs(losses, level=2.2):
    n = 0
    for v in losses:
        if v > level:
            n += 1
        else:
            break
    return n


def deep_vs_residual(curves):
    if min(curves['residual']) < min(curves['plain']):
        return 'residual'
    return 'plain'
```
- W4 counts epochs below the level: caught, key test-2; failing 2, 3, 5

```python
def stuck_epochs(losses, level=2.2):
    n = 0
    for v in losses:
        if v < level:
            n += 1
        else:
            break
    return n


def deep_vs_residual(curves):
    if curves['residual'][-1] < curves['plain'][-1]:
        return 'residual'
    return 'plain'
```

### l12-shifted-digits screens[8] `shift_images` (5 hidden tests)
- C0 (model + starter comments): passes every test (correct)

```python
import numpy as np


def shift_images(X, dx, dy):
    # move every image dx pixels right and dy pixels down; empty pixels become 0
    X = np.asarray(X, dtype=float)
    out = np.zeros_like(X)
    h, w = X.shape[-2], X.shape[-1]
    for i in range(h):
        for j in range(w):
            if 0 <= i + dy < h and 0 <= j + dx < w:
                out[..., i + dy, j + dx] = X[..., i, j]
    return out
```
- W1 slicing that handles only positive shifts: caught, key test-2; failing 2 (ValueError: could not broadcast input array from shape (1,1,3,3) into shape (1,1,1,3)), 3 (ValueError: could not broadcast input array from shape (1,1,2,3) into shape (1,1,2,1))

```python
import numpy as np


def shift_images(X, dx, dy):
    X = np.asarray(X, dtype=float)
    out = np.zeros_like(X)
    h, w = X.shape[-2], X.shape[-1]
    out[..., dy:, dx:] = X[..., :h - dy, :w - dx]
    return out
```
- W2 roll, then zero only the first dx columns: caught, key test-2; failing 2, 3

```python
import numpy as np


def shift_images(X, dx, dy):
    X = np.asarray(X, dtype=float)
    out = np.roll(X, (dy, dx), axis=(-2, -1))
    if dx > 0:
        out[..., :, :dx] = 0
    if dy > 0:
        out[..., :dy, :] = 0
    return out
```
- W3 edge-pixel fill (np.pad edge) instead of zeros: caught, key test-1; failing 1, 2, 3, 4

```python
import numpy as np


def shift_images(X, dx, dy):
    X = np.asarray(X, dtype=float)
    h, w = X.shape[-2], X.shape[-1]
    p = max(abs(dx), abs(dy))
    Xp = np.pad(X, [(0, 0)] * (X.ndim - 2) + [(p, p), (p, p)], mode='edge')
    return Xp[..., p - dy:p - dy + h, p - dx:p - dx + w]
```

### l12-shifted-digits screens[9] `shifted_accuracy, margin` (6 hidden tests)
- C0 (model + starter comments): passes every test (correct)

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
cnn_predict = lambda X: predict(cnn_logits, cnn, X)
mlp_predict = lambda X: predict(mlp_logits, mlp, X)
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def shifted_accuracy(predict_fn, X, y, shifts):
    # one accuracy per (dx, dy) in shifts
    return [float((predict_fn(shift_images(X, dx, dy)) == y).mean()) for dx, dy in shifts]


def margin(cnn_acc, mlp_acc):
    # the clear-margin rule on mean shifted accuracies
    return cnn_acc - mlp_acc >= 0.10
```
- W1 strict inequality (> 0.10): SURVIVES (passes every test)

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
cnn_predict = lambda X: predict(cnn_logits, cnn, X)
mlp_predict = lambda X: predict(mlp_logits, mlp, X)
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def shifted_accuracy(predict_fn, X, y, shifts):
    return [float((predict_fn(shift_images(X, dx, dy)) == y).mean()) for dx, dy in shifts]


def margin(cnn_acc, mlp_acc):
    return cnn_acc - mlp_acc > 0.10
```
- W2 rule of 0.05: caught, key test-6; failing 6

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
cnn_predict = lambda X: predict(cnn_logits, cnn, X)
mlp_predict = lambda X: predict(mlp_logits, mlp, X)
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def shifted_accuracy(predict_fn, X, y, shifts):
    return [float((predict_fn(shift_images(X, dx, dy)) == y).mean()) for dx, dy in shifts]


def margin(cnn_acc, mlp_acc):
    return cnn_acc - mlp_acc >= 0.05
```
- W3 any lead counts (> 0): caught, key test-6; failing 6

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
cnn_predict = lambda X: predict(cnn_logits, cnn, X)
mlp_predict = lambda X: predict(mlp_logits, mlp, X)
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def shifted_accuracy(predict_fn, X, y, shifts):
    return [float((predict_fn(shift_images(X, dx, dy)) == y).mean()) for dx, dy in shifts]


def margin(cnn_acc, mlp_acc):
    return cnn_acc > mlp_acc
```
- W4 scores the validation split, ignores X and y: caught, key test-1; failing 1, 2, 3

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
cnn_predict = lambda X: predict(cnn_logits, cnn, X)
mlp_predict = lambda X: predict(mlp_logits, mlp, X)
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def shifted_accuracy(predict_fn, X, y, shifts):
    return [float((predict_fn(shift_images(X_va, dx, dy)) == y_va).mean()) for dx, dy in shifts]


def margin(cnn_acc, mlp_acc):
    return cnn_acc - mlp_acc >= 0.10
```
- W5 labels off by one: caught, key test-1; failing 1, 2, 3, 4

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
cnn_predict = lambda X: predict(cnn_logits, cnn, X)
mlp_predict = lambda X: predict(mlp_logits, mlp, X)
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def shifted_accuracy(predict_fn, X, y, shifts):
    return [float((predict_fn(shift_images(X, dx, dy)) == (y + 1) % 10).mean()) for dx, dy in shifts]


def margin(cnn_acc, mlp_acc):
    return cnn_acc - mlp_acc >= 0.10
```
- W6 np.roll in place of zero fill: caught, key test-1; failing 1, 2

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
cnn_predict = lambda X: predict(cnn_logits, cnn, X)
mlp_predict = lambda X: predict(mlp_logits, mlp, X)
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def shifted_accuracy(predict_fn, X, y, shifts):
    return [float((predict_fn(np.roll(X, (dy, dx), axis=(-2, -1))) == y).mean()) for dx, dy in shifts]


def margin(cnn_acc, mlp_acc):
    return cnn_acc - mlp_acc >= 0.10
```

### homework-3 items[0] `digit_report` (8 hidden tests)
- C0 (model + starter comments): passes every test (correct)

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def digit_report(params_cnn, params_mlp, X_test, y_test):
    # keys: 'cnn', 'mlp', 'cnn_shifted', 'mlp_shifted', 'exit'
    def score(fn, params, X):
        return float((predict(fn, params, X) == y_test).mean())
    rep = {'cnn': score(cnn_logits, params_cnn, X_test), 'mlp': score(mlp_logits, params_mlp, X_test)}
    rep['cnn_shifted'] = [score(cnn_logits, params_cnn, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    rep['mlp_shifted'] = [score(mlp_logits, params_mlp, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    gap = np.mean(rep['cnn_shifted']) - np.mean(rep['mlp_shifted'])
    rep['exit'] = bool(rep['cnn'] >= 0.98 and gap >= 0.10)
    return rep
```
- W1 margin rule any lead (gap > 0): SURVIVES (passes every test)

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def digit_report(params_cnn, params_mlp, X_test, y_test):
    def score(fn, params, X):
        return float((predict(fn, params, X) == y_test).mean())
    rep = {'cnn': score(cnn_logits, params_cnn, X_test), 'mlp': score(mlp_logits, params_mlp, X_test)}
    rep['cnn_shifted'] = [score(cnn_logits, params_cnn, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    rep['mlp_shifted'] = [score(mlp_logits, params_mlp, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    gap = np.mean(rep['cnn_shifted']) - np.mean(rep['mlp_shifted'])
    rep['exit'] = bool(rep['cnn'] >= 0.98 and gap > 0)
    return rep
```
- W2 margin rule 0.05: SURVIVES (passes every test)

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def digit_report(params_cnn, params_mlp, X_test, y_test):
    def score(fn, params, X):
        return float((predict(fn, params, X) == y_test).mean())
    rep = {'cnn': score(cnn_logits, params_cnn, X_test), 'mlp': score(mlp_logits, params_mlp, X_test)}
    rep['cnn_shifted'] = [score(cnn_logits, params_cnn, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    rep['mlp_shifted'] = [score(mlp_logits, params_mlp, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    gap = np.mean(rep['cnn_shifted']) - np.mean(rep['mlp_shifted'])
    rep['exit'] = bool(rep['cnn'] >= 0.98 and gap >= 0.05)
    return rep
```
- W3 held-out bar 0.95: caught, key test-8; failing 8

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def digit_report(params_cnn, params_mlp, X_test, y_test):
    def score(fn, params, X):
        return float((predict(fn, params, X) == y_test).mean())
    rep = {'cnn': score(cnn_logits, params_cnn, X_test), 'mlp': score(mlp_logits, params_mlp, X_test)}
    rep['cnn_shifted'] = [score(cnn_logits, params_cnn, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    rep['mlp_shifted'] = [score(mlp_logits, params_mlp, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    gap = np.mean(rep['cnn_shifted']) - np.mean(rep['mlp_shifted'])
    rep['exit'] = bool(rep['cnn'] >= 0.95 and gap >= 0.10)
    return rep
```
- W4 held-out bar read on the validation split: caught, key test-8; failing 8

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def digit_report(params_cnn, params_mlp, X_test, y_test):
    def score(fn, params, X):
        return float((predict(fn, params, X) == y_test).mean())
    rep = {'cnn': score(cnn_logits, params_cnn, X_test), 'mlp': score(mlp_logits, params_mlp, X_test)}
    rep['cnn_shifted'] = [score(cnn_logits, params_cnn, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    rep['mlp_shifted'] = [score(mlp_logits, params_mlp, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    gap = np.mean(rep['cnn_shifted']) - np.mean(rep['mlp_shifted'])
    rep['exit'] = bool(score(cnn_logits, params_cnn, X_test) * 0 + float((predict(cnn_logits, params_cnn, X_va) == y_va).mean()) >= 0.98 and gap >= 0.10)
    return rep
```
- W5 exit tests the margin on the clean accuracies: caught, key test-6; failing 6

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def digit_report(params_cnn, params_mlp, X_test, y_test):
    def score(fn, params, X):
        return float((predict(fn, params, X) == y_test).mean())
    rep = {'cnn': score(cnn_logits, params_cnn, X_test), 'mlp': score(mlp_logits, params_mlp, X_test)}
    rep['cnn_shifted'] = [score(cnn_logits, params_cnn, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    rep['mlp_shifted'] = [score(mlp_logits, params_mlp, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    gap = rep['cnn'] - rep['mlp'] + 0.1
    rep['exit'] = bool(rep['cnn'] >= 0.98 and gap >= 0.10)
    return rep
```
- W6 test images standardised with their own mean and sd: caught, key test-2; failing 2, 3, 4, 5

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def digit_report(params_cnn, params_mlp, X_test, y_test):
    X_test = (X_test - X_test.mean()) / X_test.std()
    def score(fn, params, X):
        return float((predict(fn, params, X) == y_test).mean())
    rep = {'cnn': score(cnn_logits, params_cnn, X_test), 'mlp': score(mlp_logits, params_mlp, X_test)}
    rep['cnn_shifted'] = [score(cnn_logits, params_cnn, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    rep['mlp_shifted'] = [score(mlp_logits, params_mlp, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    gap = np.mean(rep['cnn_shifted']) - np.mean(rep['mlp_shifted'])
    rep['exit'] = bool(rep['cnn'] >= 0.98 and gap >= 0.10)
    return rep
```
- W7 margin from the worst shift, not the mean: caught, key test-5; failing 5

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def digit_report(params_cnn, params_mlp, X_test, y_test):
    def score(fn, params, X):
        return float((predict(fn, params, X) == y_test).mean())
    rep = {'cnn': score(cnn_logits, params_cnn, X_test), 'mlp': score(mlp_logits, params_mlp, X_test)}
    rep['cnn_shifted'] = [score(cnn_logits, params_cnn, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    rep['mlp_shifted'] = [score(mlp_logits, params_mlp, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    gap = min(rep['cnn_shifted']) - min(rep['mlp_shifted'])
    rep['exit'] = bool(rep['cnn'] >= 0.98 and gap >= 0.10)
    return rep
```
- W8 roll in place of zero fill: caught, key test-3; failing 3

```python
import numpy as np
from cnn_ops_l3 import load_split, load_weights, predict, cnn_logits, mlp_logits, shift_images

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
mlp = load_weights('cnn-w-mlp.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # right, left, down, up


def digit_report(params_cnn, params_mlp, X_test, y_test):
    def score(fn, params, X):
        return float((predict(fn, params, X) == y_test).mean())
    rep = {'cnn': score(cnn_logits, params_cnn, X_test), 'mlp': score(mlp_logits, params_mlp, X_test)}
    rep['cnn_shifted'] = [score(cnn_logits, params_cnn, np.roll(X_test, (dy, dx), axis=(-2, -1))) for dx, dy in SHIFTS]
    rep['mlp_shifted'] = [score(mlp_logits, params_mlp, shift_images(X_test, dx, dy)) for dx, dy in SHIFTS]
    gap = np.mean(rep['cnn_shifted']) - np.mean(rep['mlp_shifted'])
    rep['exit'] = bool(rep['cnn'] >= 0.98 and gap >= 0.10)
    return rep
```

### homework-3 items[1] `fine_tune` (6 hidden tests)
- C0 (model + starter comments): passes every test (correct)

```python
import numpy as np
from autograd import Tensor, cross_entropy
from cnn_ops_l3 import load_split, load_weights, cnn_logits, shift_images, accuracy
from nt_ops_l1 import adam_step, minibatch_indices

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
X_aug = np.concatenate([X_tr] + [shift_images(X_tr, dx, dy) for dx, dy in SHIFTS])   # 5,025 images
y_aug = np.concatenate([y_tr] * 5)


def fine_tune(params, X, y, epochs, lr, seed):
    # Adam from these weights; batches minibatch_indices(len(X), 32, seed + epoch)
    params = [np.array(p, dtype=float) for p in params]
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t = 0
    for epoch in range(epochs):
        for idx in minibatch_indices(len(X), 32, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(cnn_logits(ts, X[idx]), y[idx])
            loss.backward()
            t += 1
            params, m, v = adam_step(params, [p.grad for p in ts], m, v, t, lr)
    return params
```
- W1 learning rate fixed at 0.01, lr ignored: SURVIVES (passes every test)

```python
import numpy as np
from autograd import Tensor, cross_entropy
from cnn_ops_l3 import load_split, load_weights, cnn_logits, shift_images, accuracy
from nt_ops_l1 import adam_step, minibatch_indices

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
X_aug = np.concatenate([X_tr] + [shift_images(X_tr, dx, dy) for dx, dy in SHIFTS])   # 5,025 images
y_aug = np.concatenate([y_tr] * 5)


def fine_tune(params, X, y, epochs, lr, seed):
    params = [np.array(p, dtype=float) for p in params]
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t = 0
    for epoch in range(epochs):
        for idx in minibatch_indices(len(X), 32, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(cnn_logits(ts, X[idx]), y[idx])
            loss.backward()
            t += 1
            params, m, v = adam_step(params, [p.grad for p in ts], m, v, t, 0.01)
    return params
```
- W2 starts from a fresh He init, not the supplied weights: caught, key test-3; failing 3, 4

```python
import numpy as np
from autograd import Tensor, cross_entropy
from cnn_ops_l3 import load_split, load_weights, cnn_logits, shift_images, accuracy
from nt_ops_l1 import adam_step, minibatch_indices

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
X_aug = np.concatenate([X_tr] + [shift_images(X_tr, dx, dy) for dx, dy in SHIFTS])   # 5,025 images
y_aug = np.concatenate([y_tr] * 5)


def fine_tune(params, X, y, epochs, lr, seed):
    from cnn_ops_l3 import init_cnn
    params = init_cnn(16, seed)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t = 0
    for epoch in range(epochs):
        for idx in minibatch_indices(len(X), 32, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(cnn_logits(ts, X[idx]), y[idx])
            loss.backward()
            t += 1
            params, m, v = adam_step(params, [p.grad for p in ts], m, v, t, lr)
    return params
```
- W3 adds the validation digits to training (leak): caught, key test-3; failing 3, 4

```python
import numpy as np
from autograd import Tensor, cross_entropy
from cnn_ops_l3 import load_split, load_weights, cnn_logits, shift_images, accuracy
from nt_ops_l1 import adam_step, minibatch_indices

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
X_aug = np.concatenate([X_tr] + [shift_images(X_tr, dx, dy) for dx, dy in SHIFTS])   # 5,025 images
y_aug = np.concatenate([y_tr] * 5)


def fine_tune(params, X, y, epochs, lr, seed):
    params = [np.array(p, dtype=float) for p in params]
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t = 0
    X = np.concatenate([X, X_va]); y = np.concatenate([y, y_va])
    for epoch in range(epochs):
        for idx in minibatch_indices(len(X), 32, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(cnn_logits(ts, X[idx]), y[idx])
            loss.backward()
            t += 1
            params, m, v = adam_step(params, [p.grad for p in ts], m, v, t, lr)
    return params
```
- W4 epochs ignored (always one): caught, key test-4; failing 4

```python
import numpy as np
from autograd import Tensor, cross_entropy
from cnn_ops_l3 import load_split, load_weights, cnn_logits, shift_images, accuracy
from nt_ops_l1 import adam_step, minibatch_indices

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
X_aug = np.concatenate([X_tr] + [shift_images(X_tr, dx, dy) for dx, dy in SHIFTS])   # 5,025 images
y_aug = np.concatenate([y_tr] * 5)


def fine_tune(params, X, y, epochs, lr, seed):
    params = [np.array(p, dtype=float) for p in params]
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t = 0
    for epoch in range(1):
        for idx in minibatch_indices(len(X), 32, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(cnn_logits(ts, X[idx]), y[idx])
            loss.backward()
            t += 1
            params, m, v = adam_step(params, [p.grad for p in ts], m, v, t, lr)
    return params
```
- W5 Adam moments carried in from nowhere: plain gradient descent: caught, key test-3; failing 3, 4, 5

```python
import numpy as np
from autograd import Tensor, cross_entropy
from cnn_ops_l3 import load_split, load_weights, cnn_logits, shift_images, accuracy
from nt_ops_l1 import adam_step, minibatch_indices

X_tr, y_tr, X_va, y_va, X_te, y_te = load_split()
cnn = load_weights('cnn-w-exit.json')
SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
X_aug = np.concatenate([X_tr] + [shift_images(X_tr, dx, dy) for dx, dy in SHIFTS])   # 5,025 images
y_aug = np.concatenate([y_tr] * 5)


def fine_tune(params, X, y, epochs, lr, seed):
    params = [np.array(p, dtype=float) for p in params]
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t = 0
    for epoch in range(epochs):
        for idx in minibatch_indices(len(X), 32, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(cnn_logits(ts, X[idx]), y[idx])
            loss.backward()
            t += 1
            params = [p - lr * q.grad for p, q in zip(params, ts)]
    return params
```

## Fix pass

I recomputed every changed figure before writing it (the lr 0.02 losses by the module's `fit` and by the script's plain NumPy loss; the signed-input block pixel by `blockB`; the 0.9741 plant as 526/540; the mixture gap 0.0755; the validation gaps). After the edits `docs/reports/cnn-L3-numbers.py` exits 0 through `run-number-scripts.mjs --only cnn-L3` (1 thread, 68 s) and directly with `ZQ_NUMBERS_STRICT=1` (633 of 633 checks, 0 uncovered, 6 literals, no `claim(True, covers=...)`). The 12 surviving wrong solutions are now `mutants` (13 added in all, 51 in the level), each first failing the test it names. Validator 0 errors, no `[ai-mutants]` or `[source-ban]` warning on cnn files; voice scan 0 over 35 words and 0 long explanations; `same-course-reuse.mjs --all` no error for cnn; `grade-all.mjs --file <f> --code --local-cdn <pkgs>` 0 failures on each of the 7 files alone; playthrough green with and without `--mobile` for the four lessons, `review-3`, `homework-3` and `problems-3`.

Status: fixed 21, disputed 0, deferred 0. One part of one fix differs from the proposal, and its line says why.

### Errors
- l10 screens[0] options[2].why, explain | fixed: "It ends lowest, at 0.889, and has not risen since epoch 7: too slow for 10 epochs." Explain: "Too small a rate ends lowest (0.889); too large a rate wobbles (0.917)." Recomputed from the chart: 0.893, 0.889, 0.889, 0.889.
- l11 screens[6] explain, feedback.correct | fixed: the original ResNet has batch norm inside $F$ and a ReLU after the sum (later ResNets dropped it); most transformers now put layer norm at the start of $F$, which leaves the identity path clean. The keyed answer is unchanged.

### Warnings
- l10 screens[9] exit_check | fixed: test 6 plants the exit net on the test digits with six labels changed (526 of 540 = 0.9741) and expects False, with a `test-6` line. Mutants: validation split, bar 0.95, bar 0.97 (all first fail test 6). Graded answer added.
- l10 screens[5] early stopping on test | fixed: `load_split()` assigns `_, _` for the test split in starter and solution, test 6 is `zq_no('fit', 'X_te', 'y_te')`, with its line and `how` updated. Mutant: best-test-epoch keeper (first fails test 6).
- l10 screens[5] and homework items[1] ignored `lr` | fixed: l10 test 3 now runs at lr 0.02 (loss 1.309602203294493, was 1.7500431545973398 at 0.01); homework test 4 runs at 0.02 (0.4566970672338245, was 0.6314950223715697). The `lr` sentence moved from l10 `test-5` to `test-3`, and homework `test-4` names it. Mutants: lr fixed at 0.01 (l10 test 3, homework test 4). Graded answers changed (two expected losses).
- homework items[0] margin never tested | fixed: test 9 (an MLP 0.7 plain plus 0.3 augmented: mean shifted 0.5426, gap 0.0755, claimed in the script) expects False; `how` now says the 8-filter net fails both parts and describes the new plant; `test-9` line added. Mutants: any lead, 0.05 (both first fail test 9). Graded answer added.
- l11 screens[9] block_grad_check never calls `grad_check` | fixed: test 2 is `1e-13 < err < 1e-6` (the model returns about 3e-11), with a `test-2` line and `how` updated. Mutant: backward only, error 0.0 (first fails test 2). Graded answer tightened.
- l11 screens[0] hook | fixed: explain now says the stall comes from the small start and plain descent, that He starts with Adam train these layers well, and that the skip matters most in nets tens of layers deep (He et al. 2016). Three sentences.
- l12 screens[5], homework items[6], problems-3 items[2] parts[3] overclaim | fixed: l12 says the copies teach the MLP these four shifts and that at two pixels the gap returns to between 0.06 and 0.10 on the validation digits (script claim: 0.0585, 0.0764, 0.098 against under 0.03 at one pixel). The reviewer's test-split figures were 0.065 to 0.10 for the same recipe; I used validation so the claim is not made on the data that judges the exit. Homework option c now points to the two-pixel result; problems says "the shifts they show".
- l9 screens[6] explain | fixed: "Accuracy averages over all 540 digits, so one weak class barely moves it".

### Notes
- l9 screens[6] prose 99% | fixed to "about 98%"; script expectation changed to 98.
- l9 quiz[1] byKey.col | fixed: id renamed `all-right`, line "Not every 3 is read right: 2 of the 50 are misread."
- l9 screens[5] and screens[7] test-2 lines | fixed: screens[5] now teaches `+=` counting; the screens[7] line is dropped.
- l9 screens[8] options[2].why | fixed: "F7's middle row is its positive row".
- l11 screens[8] ReLU on the identity path | fixed, decided by the stated contract (y = x + F(x)): a block that adds ReLU(x) is not that block even though it agrees on non-negative inputs. Test 7 runs the block on `h - 0.5` (signed) against the plain NumPy block (pixel checked in the script and checked to differ from the clipped version); `test-7` line; mutant `np.maximum(x, 0) + F` first fails test 7. The `test-4` line stays for code that changes `x` when F is zero.
- l11 screens[10] min loss for final | fixed, decided by the stated contract ("the name of the lower final loss"): test 7 is the reviewer's planted pair expecting 'residual'; `test-7` line; mutant `min(...)` first fails test 7. `how` now says four planted curves.
- l12 screens[2] explain, screens[4] prose | fixed: "The CNN's filters learned strokes wherever they sit" and "its own 10 weights for each of the 256 pooled values, just as the MLP has its own 40 for each pixel".
- l12 screens[9] margin, review-3 r-margin | fixed: solution and hint use `>= 0.10 - 1e-9`, the prose says why (0.57 - 0.47 is a hair under 0.10 in floating point; claimed in the script), test 7 is `margin(0.57, 0.47)` expecting True. Mutants: strict `>` and `>= 0.10` (both first fail test 7). r-margin keys 0.57 and now agrees with the widget.
- review-3 nine items | fixed: tenth item `r-projection` (1 by 1, stride 2 projection from 8 to 16 channels, $16 \times 9 = 144$). I used 8 to 16 rather than 16 to 32 because l11 screens[5] already states $32 \times 17 = 544$ and a repeat would be a same-course reuse.
- problems-3 items[3] parts[3] 'high-last' (24) | fixed: the wrong value and its line are dropped; 'last' (25) stays.
- docs/reports/cnn-L3-numbers.py four gaps | fixed, one part declined. (1) Claims that the exit, small, mlp and residual files are byte for byte what the seed-0 recipes write with `save_weights(..., digits=6)`, and `round(retrained, 6)` equals the arrays; the augmented MLP is claimed within 1e-6 (it is the one file that is not exact). (2) `exitlr` is out of `KIND`: no test score is computed for a rate candidate. (3) The margin rule is now set on shifted validation digits (smallest CNN-minus-MLP gap over nine seed pairs 0.1776, largest augmented gap 0.0278, so 0.10 sits between), l12 screens[10] and screens[9] say so, and the augmentation statements are rechecked on validation. (4) The two-pixel augmented gap is computed and claimed. Declined: changing the default of `save_weights` in `cnn_ops_l3.py` from 7 to 6 digits, because it would change the shipped module's bytes and hash for no lesson; the script passes `digits=6` and proves the files by bytes instead.
- Leakage notes (margin set from test, scores of rate candidates on test) | fixed as above. Exit accuracy is still read once per seed on test, and the exit nets, MLP and augmented sets are unchanged.
