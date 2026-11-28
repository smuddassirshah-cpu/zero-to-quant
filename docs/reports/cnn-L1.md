# cnn level 1 (Convolution as a sliding dot product): report

## Files written

All in `app/content/courses/cnn/`, skill `cnn-conv` throughout. Plus `app/content/data/ai/cnn_ops_l1.py` (version 1.0, imports the frozen `autograd.py` v1.0 only).

| File | Screens / items | Code widgets |
|---|---|---|
| `l1-rolling-mean-is-convolution.json` | 11 screens, 3 quiz, 14 min | `conv1d_valid`, `rolling_mean_as_conv`, `ewm_kernel` |
| `l2-kernels-that-detect.json` | 12 screens, 3 quiz, 15 min | `pad_same`, `second_difference`, `detect` |
| `l3-convolution-in-2d.json` | 11 screens, 3 quiz, 15 min | `conv2d_valid`, `conv2d_multi`, `edge_map` |
| `l4-learning-a-kernel.json` | 12 screens, 3 quiz, 18 min | `conv1d_backward`, `learn_kernel` (autograd), `kernel_gradient_check` (autograd) |
| `review-1.json` | 9 items, difficulty 2 to 4, `pass: 0.8` | none |
| `homework-1.json` | 8 items, difficulty 3 to 5 | performance `conv2d(img, kernels, bias)` (5), `conv1d_full` (4); `order` (gradient of a kernel weight, one distractor); `longform` "just a moving-average crossover" (10-point rubric, three required rows); four numeric or choice |
| `problems-1.json` | 3 problems, 12 parts, difficulty 3, 4, 5 | none |

Lesson shapes follow the brief. l1: the `numpy-pandas` closes, the mean on row 6 as a dot product, a 10-frame slide (10 outputs), $n - k + 1$ (231 for 250 and 20), two weighted outputs by hand (12.400, 12.443), the truncated EWM kernel (0.516), alignment with pandas (row $t + k - 1$), trap the flip ($(1, 0, -1)$: $-1$ against 1), generalise with a stepped spike (shift-equivariance). l2: match three kernels to three outputs (`place`), a matched kernel (peak 11 at $t = 4$), the sliding cosine (0.572), change and bend kernels, a threshold (0.7 flags 2 positions, one false), trap a positive kernel on a trending price (raw peaks at the end, normalised 0.918 at the bump), edge case zero padding ($-12.25$ against 0.15). l3: a noisy 7 (seed 8) with the vertical-edge kernel stepped on a `matrix`, $(n - k + 1)^2$, two maps, channels out and in, trap `patch @ K` (1 against $-3$), edge case 1 by 1 kernel (5). l4: guess the kernel family, the loss parabola in $k_2$ (`plane` with a slider), the gradient by hand (0.75), the op's backward, descent to the noise floor (0.0108), trap the summed loss, edge case a 5-weight truth fitted with 3 (floor 0.35), a transfer on AR filters ($k/n = 2\%$).

## Ops added: `cnn_ops_l1.py`

`correlate1d(x, k)`, `correlate2d(x, k)` (plain arrays, forward only), `conv1d(x, k)` and `conv2d(x, k)` (`Tensor` ops: no flip, valid positions; `conv2d` is one channel). Backward: `conv1d` gives `dk = correlate1d(x, g)` and `dx = np.convolve(g, k)` (full); `conv2d` gives `dk` by `einsum` over sliding windows and adds `k[a, b] * g` back into `dx`. Gradient checks in float64 (number script, two routes: `grad_check` and the script's own central differences): `conv1d` 3.8e-11, 8.1e-12, 1.5e-11 (own 2.5e-11, 1.9e-11, 2.1e-11); `conv2d` 2.7e-11, 1.8e-11, 1.6e-11 (own 2.9e-11, 1.8e-11, 1.8e-11), on signals 20/4, 9/3, 5/5 and images 7x6/3x2, 8x8/3x3, 4x4/4x4. Shipped verbatim beside `autograd.py` through `files` on the two autograd screens of l4; the number script checks both SHA-256s for every shipped copy. Names are stable for level 2.

## Gates

1. Validator: `node tools/validate.mjs` 0 errors; no `[ai-mutants]` warning. Advisory warnings on cnn files: point hints without highlight, ladder canvas-kind changes (a series after an array of the same closes), 18 `O2-long-sentence`.
2. Voice: `VOICE_BASE=app/content/courses/cnn python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `docs/reports/cnn-L1-numbers.py` with the venv: 357 of 357 checks, exit 0, under 1 s. Route A is the generators (`np.correlate`, sliding windows, the shipped autograd); route B plain loops, `np.convolve` of the reversed kernel, pandas `rolling` and `corr`, normal equations for the learned kernels, closed forms. It checks every lesson, review, homework and problem number at its JSON path, every numeric `wrong`, the shipped files, both ops' gradients, and every code widget (14 widgets, 41 mutants: model passes, starter fails, each mutant first fails its named test).
4. Code in Pyodide: `node tools/grade-all.mjs --code --local-cdn <pkgs>` on all seven files: 70 widgets graded and 14 Python widgets run, 0 failures.
5. Playthrough: all seven files with `--local-cdn <pkgs> --mobile` (desktop and 440 px): all passed; homework "1 performance starter fail" as required. Screens read at 440 px. Fixes made: a pair of grids with `tap: "sides"` never became ready under the test hook (replaced by a choice, inbox bullet); an inline `pmatrix` in prose replaced by words.
6. Performance task: `docs/reports/cnn-1-perf.md`.

Timing (desktop, CPython; Pyodide is slower by a small factor): `learn_kernel` 100 steps on 198 outputs 0.05 s natively; `kernel_gradient_check` well under 0.1 s. Both carry a `budget` (4000 and 2000 ms) for a phone; no case trains a CNN.

## Data and seeds

Twelve closes of `numpy-pandas` l10; price path `default_rng(22)`, $N(0, 0.4)$ steps from 100 with a £3 one-day spike on day 18; minute volumes `default_rng(3)`, Poisson(200) with minute 40 tripled; the 7 image plus `default_rng(8)` noise of 0 or 1; l4 signal `default_rng(20)` (200 values, kernel $(0.2, 0.3, 0.5)$, noise sd 0.1); the short-kernel case `default_rng(21)` (1,000 values). Test seeds 4 to 44 as named in each `setup`.

## Proposed course.json change

None.

## Notes for level 2

`cnn_ops_l1.py` stays frozen; level 2 adds `cnn_ops_l2.py` (stride, padding, channels, im2col, pooling), importing level 1 names where useful.
