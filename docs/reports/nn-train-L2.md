# nn-train level 2 (Activations, initialisation and normalisation): report

Branch `ai-w4-nn-train`, on top of level 1 (`648914a5`). Skill `nt-signal` on every lesson and item.

## Files written

| File | Screens or items | Notes |
|---|---|---|
| `l5-saturation.json` | 8 screens, 3 quiz | gradient norms by layer (bars, log scale), $0.25^{10}$, slope explorer (plane with a slider), a chain of four slopes, dead units, trap "overfitting", code, transfer (income in pounds) |
| `l6-initialisation.json` | 8 screens, 3 quiz | weight-sd slider over ten linear layers (series frames, log scale), $n\operatorname{Var}(w)\operatorname{Var}(x)$, one layer by hand with the 20,000-draw simulation, He, derivation (`order`), trap "equal starts", code, transfer |
| `l7-batch-norm.json` | 9 screens, 3 quiz | deep net with and without batch norm at step 1 (recorded curves), a batch of 4 by hand, $\gamma$ and $\beta$, running averages, train against inference, trap "batch of one", forward code, backward code (autograd op, `grad_check`), transfer |
| `l8-layer-norm.json` | 8 screens, 3 quiz | per-example normalisation, one vector by hand, the axis count, backward derivation (`order`), trap "wrong axis", forward code with `compare_norms`, the `layernorm` op with its backward, transfer |
| `review-2.json` | 8 items, `pass` 0.8 | every lesson, difficulty 2 to 4 |
| `homework-2.json` | 6 items | performance task `h2-ln-backward` (code, difficulty 5), `h2-fold` (code: folding batch norm into a layer), `h2-relu-order` (order), a numeric, a choice, `h2-time-of-day` (longform, 10-point rubric) |
| `problems-2.json` | 3 problems, 12 parts | difficulty 5, 4, 3; every lesson used |
| `app/content/data/ai/nt_ops_l2.py` | module | public names at the end |
| `docs/reports/nn-train-L2-numbers.py`, `docs/reports/nn-train-2-perf.md` | | |

## Gates

1. Validator: 0 errors. Warnings on the level's files: point hints on canvas-free screens, problem screens without a canvas, ladder canvas-kind changes, `O2-long-sentence` advisories.
2. Voice: `voice-scan.py 35` on the course folder: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans.
3. Numbers: `ZQ_NUMBERS_STRICT=1 <venv>/bin/python docs/reports/nn-train-L2-numbers.py`: 229 of 229 checks, coverage 0 uncovered (13 literals with reasons), exit 0. The 45 byKey lines that state other numbers were read by hand; one inconsistent slip (l6 screen 2, `sd`) was fixed.
4. Code widgets: `grade-all.mjs --code` on all seven files: 8 Python widgets, 0 failures in Pyodide; 35 mutants, each failing its named test first.
5. Playthrough with `--local-cdn <pkgs> --mobile`: the four lessons, review-2, homework-2 ("1 performance starter fail") and problems-2 all passed; the lessons and homework were replayed after the last text edits.
6. `fresh-check.mjs --file` on review-2, homework-2, problems-2: 0 hits (one advisory: problems-2 shares the stated $\epsilon = 10^{-5}$ with l8). `same-course-reuse.mjs --all`: no errors on nn-train.

## Decisions a reader should know

- **The batch-norm hook states only the split.** At step 1 the deep net (2-64-64-64-64-2, tanh) blows up without batch norm on all five seeds (above 1 nat) and trains with it (below 0.25). The exact figures depend on rounding: seed 1 ends at 0.177 with `nt_ops_l2.batchnorm` and at 0.194 with batch norm composed from autograd primitives (default threads; under one BLAS thread, as in CI, they read 0.190 and 0.177: fix pass for the second reader's note). The lesson therefore states the split, which holds in both routes, and labels the chart as one run.
- **Notation.** As in `backprop` L4 and `makemore`, layers are `X @ W + b` with `W` of shape (fan_in, fan_out); `stat-learning` l17 stored `W` transposed.
- **Ops shipped by path.** The l5 code ships `nt_ops_l2.py` (it uses `sigmoid`); the l7 and l8 op screens ship only `autograd.py`, since the op is the exercise. The homework does not ship `nt_ops_l2.py`.
- **Running averages** move a share 0.1 towards each batch, from mean 0 and variance 1, and use the batch variance divided by $N$ (PyTorch keeps $N - 1$ for its running variance; stated in the module's docstring as divided by $N$).

## Numbers and their sources (recomputed by the number script)

- l5: gradient norms of the ten-layer sigmoid stack (`default_rng(1)`, sd 0.1, batch 64): $4.4 \times 10^{-8}$ at layer 1 to 0.123 at layer 10 (autograd and a hand backward agree to $10^{-9}$); $0.25^{10} = 9.5 \times 10^{-7}$; $1 - \tanh^2(3) = 0.0099$; the four-slope chain 0.001213; dead units 3; $1 - \tanh^2(5.2) = 1.22 \times 10^{-4}$, and 0.92 at $z = 0.3$.
- l6: sd after ten linear layers (1,000 rows, `default_rng(0)`): 1.06 at sd 0.1, $1.1 \times 10^{10}$ at sd 1, each within a factor 2 of $(100\,s^2)^5$; simulation 101.0 against 100 (20,000 draws, `default_rng(0)`); He 0.1414 (ReLU sd 1.05 after ten layers, 0.033 at sd 0.1); the equal-start table; 0.006250 in the transfer.
- l7: $\hat x = 1.3416$ for the batch (2, 4, 6, 8); 3.6833 with $\gamma = 2$, $\beta = 1$; running mean 0.95 and variance 1.76 after two batches; 5.314 in inference mode; 2.35 in the transfer; 1.389 in the quiz.
- l8: 1.6036 for (1, 2, 3, 6); 320 means for (32, 10, 64); 1.5811 for (2, 4, 4, 4, 6).
- Review, problems, homework: every key and slip at its path (see the script), including $2.56^5 = 110.0$, $0.25^8 = 1.53 \times 10^{-5}$, $0.1966^8 = 2.23 \times 10^{-6}$, $1.44^6 = 8.92$.

## Training cases and their desktop time

No graded case trains in this level. The deep-net runs (300 steps, five seeds, both routes) live in the number script; the lesson ships their recorded curves inline. The slowest graded cases are the gradient norms of the ten-layer stack (one backward pass, under 50 ms) and the batch-norm and layer-norm `grad_check` calls (tens of milliseconds); widget budgets are 2,000 ms.

## Ops added to nt_ops_l2.py, with gradient-check errors

Route B (central differences, $h = 10^{-6}$, float64) and autograd's `grad_check`, relative error: `sigmoid` $4.4 \times 10^{-10}$; `batchnorm` train $1.4 \times 10^{-10}$, eval $2.6 \times 10^{-10}$; `layernorm` (5, 4) $3.6 \times 10^{-10}$, (2, 3, 4) $9.3 \times 10^{-10}$, one vector $1.0 \times 10^{-9}$.

## Proposed course.json change

None.

## nt_ops_l2.py public names as shipped

Version 1.0, 4,105 bytes, SHA-256 `5712fe43db9bb5060f27dbc076b6d2fdddcbf9a582bf908c69c21e38d2a50c42`; imports NumPy and `autograd` (v1.0). `from nt_ops_l2 import ...`
- `sigmoid(x) -> Tensor`: elementwise $1/(1 + e^{-x})$, stable for large $|x|$; backward $s(1 - s)$.
- `lecun_sd(fan_in) -> float`: $1/\sqrt{\text{fan\_in}}$. `he_sd(fan_in) -> float`: $\sqrt{2/\text{fan\_in}}$.
- `init_layer(fan_in, fan_out, act="tanh", seed=0) -> (W, b)`: `W` of shape (fan_in, fan_out) from `default_rng(seed)` times `he_sd` for `"relu"`, `lecun_sd` otherwise; `b` zeros.
- `batchnorm(x, gamma, beta, eps=1e-5, mode="train", running=None, momentum=0.1) -> (Tensor, (mean, var))`: `x` of shape (N, D); train mode uses the batch mean and variance (over N) and returns the running pair moved a share `momentum` towards them (from (0, 1) when `running` is None); eval mode uses `running` and returns it unchanged; backward in both modes.
- `layernorm(x, gamma, beta, eps=1e-5) -> Tensor`: normalises over the last axis for any leading shape; `gamma` and `beta` of shape (D,); backward to all three. `sequence` L4 reuses this name.
