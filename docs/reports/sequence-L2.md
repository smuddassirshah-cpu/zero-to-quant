# sequence level 2 (Attention as a soft lookup): author report

Branch `ai-w5-sequence`. Skill `sqn-attend` on every file.

## Files

| File | Screens or items | Code widgets (mutants) |
|---|---|---|
| `l5-lookup-table.json` | 9 screens, quiz 3 | `hard_lookup` + `knn_lookup` + `lookup_gradient_zero` (3) |
| `l6-soft-neighbours.json` | 10 screens, quiz 3 | `stable_softmax` + `soft_lookup` + `best_tau` (4) |
| `l7-queries-keys-values.json` | 10 screens, quiz 3 | `attention` + `attention_shapes` (4), `attention_autograd` (3) |
| `l8-scaled-dot-product.json` | 10 screens (one `order` derive), quiz 3 | `dot_variance` + `scaled_attention` + `softmax_saturation` (4) |
| `review-2.json` | 9 items, `pass` 0.8 | none |
| `homework-2.json` | 8 items (one `order`, one `longform`, two `code`) | `kernel_grad` (3), `attention_backward` performance task (5) |
| `problems-2.json` | 4 chained items, 16 parts, one at difficulty 5 | none |
| `app/content/data/ai/seq_ops_l2.py` | new module, 1,444 bytes, SHA-256 `fa2bed08afe4...` | |

Number script `docs/reports/sequence-L2-numbers.py`; performance report `docs/reports/sequence-2-perf.md`. The setting is stat-learning l4's ten grid days (keys: yesterday's return and the volume ratio, standardised; values: next-day returns in per cent) and its `make_knn(300, 11)` data split 200 and 100.

## Self-check (SESSION PROTOCOL 4)

1. Validator: 0 errors; no `[source-ban]` or `[ai-mutants]` warning on these files.
2. Voice: `voice-scan.py 35` on the course folder: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `node tools/run-number-scripts.mjs --python <venv> --only sequence-L2`: passed (strict coverage; every `wrong` value read against its `why`: 47 lines checked by hand, all match).
4. Playthrough with `--local-cdn`, desktop and `--mobile`: all 4 lessons, `review-2`, `homework-2` (performance starter fails, longform marked) and `problems-2` passed; l8 and `problems-2` replayed after their last edits, both modes.

Also: `grade-all.mjs --code --file` on every file, 0 failures (7 Python widgets, 26 mutants each failing its named test first); `same-course-reuse.mjs --all` lists nothing for the course (a first `problems-2` item retold l8 and was replaced by a capital-allocation problem).

## Numbers and their sources

- l5: nearest day to today 0.4 (distance 0.5; then 0.71 and 1), 3-NN $(0.4 + 0.2 - 0.3)/3 = 0.1$, the tie at $(0.25, -0.5)$ at distance $\sqrt{0.3125} = 0.559$ (argsort against a sorted list).
- l6: soft forecast at today, $\tau = 0.5$: 0.283 (direct against log-sum-exp). Softmax of 2, 1, 0: 0.665, 0.245, 0.090 at $\tau = 1$; 0.506 at $\tau = 2$ (against $e^2/(e^2 + e + 1)$ and $e/(e + e^{0.5} + 1)$). Held-out sweep on `make_knn(300, 11)`: 1.0229, 0.8991, 0.7357, 0.6519, 0.6058, 0.6224, 0.7115, 0.8327, 0.9484 for $\tau$ from 0.01 to 5, best $\tau = 0.2$ (vectorised against a loop; training mean 1.0082 as stat-learning states). Slope at today: $-0.116$ and $0.055$ along each axis (formula against central differences). Stable softmax of $(1000, 999)$: 0.7311.
- l7: score 2; 15 scores; output $(11e + 4)/(2e + 1) = 5.2670$; row softmax 0.7311 against the column slip 0.1192.
- l8: 20,000-draw variances 63.73, 15.94, 4.02 at $d = 64, 16, 4$ (`default_rng(1)`; `np.var` against a hand mean of squares; the brief writer's 63.7 reproduced); sigmoid slope at 8: 0.000335; seed 4 saturation: top weight 0.9996 raw, 0.2927 scaled, 0.0792 divided by $d$, against 0.3424 raw at $d = 4$.
- Review, problems, homework: each answer and slip recomputed (0.8438; 2.1213, 0.5035 and 22.55; 0.7214, 1.3050, 1.0180, 1.5813; $e^2/(e^2 + 11) = 0.4018$ and $e^{10}/(e^{10} + 11) = 0.9995$; the Jacobian entries 0.21, $-0.14$, $-0.07$ by matrix and by rule; $\sqrt{128} = 11.31$; 0.9820). The homework's `attention_backward` equals the autograd with `seq_ops_l2` on four planted cases to $10^{-9}$, including one key and scores in the hundreds.

## Timing of graded cases (Pyodide, desktop, one worker)

Slowest case per widget: l5 18 ms, l6 61 ms, l7 13 and 37 ms, l8 82 ms (the 20,000-draw simulation), homework 24 and 25 ms. Every case is far under a third of its limit.

## Module `seq_ops_l2.py` (frozen once merged)

Public names and signatures, for `sequence` L3 and L4, `gpt` and `interp`:

- `softmax(x, axis=-1) -> Tensor`: softmax of a `Tensor` (or array) along `axis`, largest entry subtracted first; backward $\mathbf s \odot (\mathbf g - \sum_{\text{axis}} \mathbf g \odot \mathbf s)$. Any number of dimensions.
- `swap_last(x) -> Tensor`: swaps the last two axes of a `Tensor` of 2 or more dimensions ($\mathbf K^\top$ for a stack of matrices); backward swaps back. Raises `ValueError` below 2 dimensions.
- `__version__ = "1.0"`. It imports `Tensor` and `_wrap` from `autograd.py` v1.0.

Gradient checks in the number script: five shapes from 1-D to 3-D on several axes and scales (relative error under $10^{-6}$ against central differences), finite output at scores of $\pm 1{,}000$, `swap_last` on a 3-D stack, and a node used twice ($\mathbf B\mathbf B^\top$).

## course.json

No change proposed.

## Backlog

One bullet under "Raised later (sequence level 2)" in `docs/BACKLOG-INBOX.md`.
