# nn-train level 3 (Generalisation in networks): report

Branch `ai-w4-nn-train`, on top of level 2 (`895d4ff3`). Skill `nt-general` on every lesson and item.

## Files written

| File | Screens or items | Notes |
|---|---|---|
| `l9-weight-decay.json` | 9 screens, 3 quiz | fits under a penalty slider (plane frames), the factor $1 - \eta\lambda$, a decayed step by hand, choosing $\lambda$ (bars), Adam against AdamW, trap "tuned on the test set", code, transfer |
| `l10-early-stopping.json` | 8 screens, 3 quiz | training and validation curves over 3,000 steps with a stop slider, $\lambda \approx 1/(\eta t)$, patience, two dips, descent and ridge paths side by side (plane), trap "validation loss as the result", code, transfer |
| `l11-dropout.json` | 9 screens, 3 quiz | fits under a dropout slider, the scale $1/(1 - p)$, one mask by hand, the expectation, trap "dropout at inference", forward code, backward and Monte Carlo spread code, transfer |
| `l12-double-descent.json` | 9 screens, 3 quiz | predict-then-reveal double-descent curve with a ridge comparison, the minimum-norm fit, the ridge curve at the peak, condition numbers, trap "bigger is always better", implicit bias (generalise), code, transfer |
| `review-3.json` | 7 items, `pass` 0.8 | every lesson, difficulty 2 to 4 |
| `homework-3.json` | 6 items | performance task `h3-select` (code, difficulty 5), `h3-decay-ridge` (code), `h3-step-order` (order), a numeric, a choice, `h3-cannot-overfit` (longform, 10-point rubric) |
| `problems-3.json` | 3 problems, 12 parts | difficulty 5, 4, 3; every lesson used |
| `app/content/data/ai/nt_ops_l3.py` | module | public names at the end |
| `docs/reports/nn-train-L3-numbers.py`, `docs/reports/nn-train-3-perf.md` | | |

## Gates

1. Validator: 0 errors. Warnings on the level's files: point hints on canvas-free screens, problem screens without a canvas, `O2-long-sentence` advisories.
2. Voice: `voice-scan.py 35` on the course folder: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans.
3. Numbers: `ZQ_NUMBERS_STRICT=1 <venv>/bin/python docs/reports/nn-train-L3-numbers.py`: 230 of 230 checks, coverage 0 uncovered (15 literals with reasons), exit 0. The 25 byKey lines that state other numbers were read by hand; one wrong slip line (l10 screen 1, `inv`) was fixed.
4. Code widgets: `grade-all.mjs --code` on all seven files: 7 Python widgets, 0 failures in Pyodide; 28 mutants, each failing its named test first.
5. Playthrough with `--local-cdn <pkgs> --mobile`: the four lessons, review-3, homework-3 ("1 performance starter fail") and problems-3 all passed; l9, l10 and homework-3 were replayed after the last edits.
6. `fresh-check.mjs --file` on review-3, homework-3, problems-3: 0 hits. `same-course-reuse.mjs --all`: no errors on nn-train. Two findings were fixed on the way: problems-3 retold l12's sentences about the threshold (reworded), and review-3 shared four losses with an l10 quiz item (new list, same answers).

## Decisions a reader should know

- **Data.** 30 training and 200 validation points of $\sin 3x$ plus noise of sd 0.3 (`default_rng(0)`), a 1-64-64-1 tanh net from LeCun starts (seed 0), 2,000 full-batch Adam steps at 0.01; the penalty is on the weights only, in the loss; dropout masks come from `default_rng(100)`.
- **Two routes agree to 0.5%, not to $10^{-9}$.** A net that can memorise 30 points amplifies rounding over 2,000 steps: with no penalty the validation error is 0.17458 with autograd and 0.17425 with the hand-written backward. The lessons show the autograd run's figures; the number script requires the hand route within 0.5% and the same winners (penalty 0.01, dropout 0.2), and the early-stopping step within 50 (660 against the hand route's).
- **The near-constant edge case is $\lambda = 1$, not 0.1.** At 0.1 the fit is stiff but still a curve (validation 0.2553 against a target variance of 0.5183); at 1 every weight is crushed and the net predicts one number (validation 0.5702: the variance plus the squared gap between the training and validation means).
- **Double descent uses ten inputs.** On one input, random ReLU features are nearly collinear and the minimum-norm error spikes at many $p$; with 10 Gaussian inputs, a linear signal and noise sd 0.5, every one of five seeds peaks near $p = n = 40$ and falls again, and ridge 0.1 removes the peak. `random_relu_features` therefore takes an $(n, d)$ array (a 1-D array is read as one input).
- **l10 has no graded net-training case.** Its code screen is `early_stop` and `gd_vs_ridge_path` (descent compared exactly after 1, 5 and 40 steps, so the loop rule holds). Training a net with early stopping is part of the homework's performance task budget instead. A proposal, not a change: the brief's `train_with_early_stopping` could return in a later fix pass if a reader wants it.

## Numbers and their sources (recomputed by the number script)

- l9: validation error 0.1746, 0.1395, 0.1055, 0.1048, 0.1143, 0.2553 at $\lambda$ = 0, 0.0001, 0.001, 0.01, 0.03, 0.1; 0.999; 1.948; AdamW 0.989 against 0.990; $0.9999^{1000} = 0.9048$; 0.9999 in the quiz.
- l10: best step 660 (validation 0.1029, training 0.0528), 0.1668 at step 3,000; $\lambda \approx 0.25$; patience stops at 6 (best 3) and 3 (two dips); step 40 against ridge 0.25 within 25%.
- l11: validation 0.1746, 0.1333, 0.1205, 0.1413, 0.1566 at $p$ = 0, 0.1, 0.2, 0.3, 0.5; 1.25; 10.667; 3; Monte Carlo spread 0.119 at $x = 0.5$ and 0.122 at 1.5 (500 passes, `default_rng(1)`).
- l12: seed 0 errors 0.874, 10.99, 0.388 at $p$ = 10, 40, 200 (minimum norm; `pinv` and `lstsq` agree); ridge 0.913 at 40; condition numbers 10, 71, 4,095, 115, 30 at $p$ = 10, 30, 40, 50, 200.
- Review, problems, homework: every key and slip at its path.

## Training cases and their desktop time

l12's `double_descent_curve` (three feature counts, a 2,000-row test set) runs in tens of milliseconds; the l11 Monte Carlo cases in under 20 ms. The homework task trains up to four 300-step nets per call, about 0.4 s in CPython and an estimated 1 to 2 s in Pyodide, with `budget` 8,000 ms (a 13 s limit per case). Everything longer (the 2,000 and 3,000-step runs behind the curves) is trained in the number script and shipped as data inside the lessons.

## Ops added to nt_ops_l3.py

The dropout op's backward (the mask held fixed) against central differences: relative error below $10^{-9}$; over 400,000 draws the mean stays within 0.02 of the input and the share dropped within 0.005 of $p$.

## Proposed course.json change

None.

## nt_ops_l3.py public names as shipped

Version 1.0, 2,851 bytes, SHA-256 `52c79ff41ccd14b5eb6e09a23fbc9399c80116f939b704b778426939ee468c7f`; imports NumPy and `autograd` (v1.0). `from nt_ops_l3 import ...`
- `decayed_sgd_step(w, g, lr, lam) -> ndarray`: $(1 - \eta\lambda)w - \eta g$.
- `adamw_step(params, grads, m, v, t, lr, lam, b1=0.9, b2=0.999, eps=1e-8) -> (params, m, v)`: Adam with the decay $\eta\lambda p$ outside the rescaling; `t` from 1.
- `early_stop(val_losses, patience) -> (stop index, best index)`: stops at the first index `patience` evaluations past the best; only a strictly lower loss is a new best; never stopping returns the last index.
- `dropout(x, p, mode="train", rng=None) -> (Tensor, mask)`: inverted dropout as a `Tensor` op; mask entries 0 or $1/(1 - p)$, drawn as `rng.random(shape) >= p`; backward multiplies by the mask; `mode="eval"` or `p = 0` returns `x` and `None`; `p` must be in $[0, 1)$.
- `random_relu_features(X, p, seed) -> ndarray`: $\max(0, \mathbf{X}\mathbf{W})$ with $\mathbf{W}$ of shape $(d, p)$ drawn $N(0, 1/d)$ from `default_rng(seed)`; a 1-D `X` is one input.
- `min_norm_fit(F, y) -> ndarray`: `np.linalg.pinv(F) @ y`.
