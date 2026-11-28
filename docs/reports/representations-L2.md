# representations level 2 (Autoencoders): report

Branch `ai-w5-representations` from `dabba415`. Brief: `docs/briefs/representations.md` Level 2. Generators and helpers: scratchpad `representations-2/` (`common2.py`, `lib2.py`, `gen_l5.py` to `gen_l8.py`, `gen_sets2.py`, `timing.mjs`, `play.sh`).

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l5-squeeze-and-rebuild.json` | 11: problem drag the line to the smallest total rebuild distance (`plane`, live caption; 1.38 against 45.12, 16.08 flat), name encoder, code and decoder by hand (`table` widget; $z = 2.44$), ladder three days' error (0.47), ladder bottleneck bars $k = 0..5$ (share left with 2 codes 20%), ladder a trained run (`series`, settles at 1.01, the 2-code bar), trap zero error at full width, ladder edge any invertible pair copies (`multi`), generalise the loss with no labels, code `encode_decode` and `recon_error`, code `train_autoencoder` (autograd and Adam), transfer a 500 by 30 panel in 3 codes (61% of variance, 1,590 numbers). 14 min | 3 |
| `l6-linear-autoencoder-is-pca.json` | 11: problem predict the trained direction on `eigen` l11's days (drag), name the error equals the dropped eigenvalue (1; trained 1.0015 against the sample's 1.0015), ladder share kept $6/7 \approx 85.7\%$, ladder 2 codes from eigenvalues 5, 2, 0.5, trap is it the eigenvector (two starts, encoder lengths 1.01 and 0.73, products 1.00), ladder mixing the codes by $\mathbf A$, ladder edge $2\mathbf I$ (three samples at 130, 3 and 25 degrees, errors near 2), derive the missing line $\sum_{i>k}\lambda_i$, code `pca_recon_error` and `subspace_angle`, code `check_pca`, transfer PCA risk factors. 15 min | 3 |
| `l7-a-curved-bottleneck.json` | 12: problem PCA rebuilds on a chord (`scatter`), explore switch PCA and tanh rebuilds (frames; 0.111 against 0.0031), problem the closed form $\tfrac12 - 4/\pi^2 \approx 0.0947$, ladder codes along the arc (rank correlation 0.972), ladder held-out errors (2.7% of PCA's), trap training error on 15 points (widths 4 and 64), ladder edge a full circle tears near 1 radian, ladder 131 parameters, generalise, code `make_arc` and `compare_with_pca` (shipped weights), code `train_tanh_ae`, transfer bent yield curves. 15 min | 3 |
| `l8-odd-days.json` | 11: problem drag a threshold on the error histogram into the gap (2.37 to 5.46), name anomaly detection with three errors by hand (0.06, 2.83, 0.06), ladder the 0.9 quantile by `np.quantile` (0.95), ladder precision $8/11 \approx 0.727$ with recall 1 (`series` of errors, markers), ladder the day 700 fall rebuilds well (error 0.47; return and rebuild bars), trap threshold set on the reported days (18.43, 2 flags), ladder edge a regime change (54% of later days flagged), generalise 5 false alarms in 500, code `day_errors` and `threshold_from_val`, code `flag_days`, transfer a cross-asset alarm. 15 min | 3 |
| `review-2.json` | 10 items, difficulty 2 to 4, `pass: 0.8`, all four lessons | |
| `homework-2.json` | 8 items, difficulty 3 to 5: performance code `anomaly_detector` (5), code `choose_k` (4), order the dropped-eigenvalue derivation with two distractors (4), longform a deep autoencoder for factor risk (5, rubric 10, two required rows), numeric share lost (3), numeric parameters against PCA (3), numeric precision (3), choice a crash and a quiet alarm (4) | |
| `problems-2.json` | 3 chained problems, 12 parts: a three-stock covariance through eigenvalue, share, error with 1 and 2 codes (l5, l6; 4); an alarm's quantile, flags, precision and recall at a raised threshold (l8, l5; 5); a quarter circle's variance, covariance, PCA error and where the rebuilds lie (l6, l7; 4) | |

New data files: `representations_ops_l2.py` (v1.0, 2.9 KB), `representations-l7-ae.json` (1,672 bytes, the 2-16-1-16-2 tanh net), `representations-l8-model.json` (1,075 bytes, the 3-code linear model). Reused byte-identical: `autograd.py` (SHA-256 `5917d4ec91f7`), `nt_ops_l1.py` (`9c1391a33624`, Adam), `representations_ops_l1.py` (the l5 transfer panel). 10 Python code widgets, 34 mutants (the taught bug among each: mean over entries, missing `zero_grad`, Adam counted from 0, $n - 1$ for $n$, uncentred scoring, PCA fitted on held-out points, `>=` for `>`, the threshold on the test days). Every training widget has an exact seeded test: `train_autoencoder` 5 and 3 steps, `check_pca` 5 steps, `train_tanh_ae` 5 and 3 steps, each to 6 places.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; level warnings are only `O2-long-sentence` advisories and ladder canvas-kind changes.
2. `voice-scan.py 35 --summary` with `VOICE_BASE` the course folder: 0 over 35 words, 0 lesson ids in code spans, 0 doubled words, 0 explanations over three sentences.
3. `node tools/run-number-scripts.mjs --only representations-L2` (strict): 297 of 297 checks, 0 uncovered, 50 literals with reasons, exit 0, about 5 s. Two figures moved to 3 places after route B disagreed in the 4th (the 4,000-step trap runs) and one to a threshold (the full-circle error, 0.019 by the autograd and 0.016 by hand backprop: stated as "under 0.02").
4. `grade-all.mjs --code` on all seven files: 72 widgets and 10 code widgets, 0 failures. Playthrough with `--local-cdn`, desktop and `--mobile`: all passed (results at the end). `fresh-check.mjs --file` on review, homework and problems: 0 hits (two review stems that retold l6 quiz items reworded); `same-course-reuse.mjs --all`: no error for this course.

## Timing (Pyodide 0.27.7 under node, desktop, per hidden test)

`train_tanh_ae` 500 steps 603 ms (budget 6,000, limit 11 s); `train_autoencoder` 300 steps 458 ms (budget 3,000); `check_pca` 137 to 167 ms; `anomaly_detector` 107 to 281 ms (budget 4,000); every other case under 40 ms. Each graded case is under 1 s on a desktop and under a third of its limit at five times slower.

## Numbers and their sources (route A generator, route B number script)

- l5: sums 29.04, 20.16, 16.08 and total 45.12 (Fractions), smallest total 1.38 (quadratic formula); $z = 2.44$, rebuild $(1.952, 1.464)$ (Fractions); 0.16, 0.04, 1.21, mean 0.47 (Fractions); bars 5.04, 2.03, 1.01, 0.51, 0.21, 0 (SVD against `eigh`); 20%; training curve and 1.01 (hand gradient and hand Adam against the autograd and `adam_step`); 61% and 1,590 (SVD of `factor_returns(7)`).
- l6: 6 and 1, $6/7$; trained 1.0015 against the sample's 1.0015 and 5.94, direction $(0.902, 0.432)$ within 0.001 degrees of the sample PC1, near $(2, 1)/\sqrt5$ (hand Adam, quadratic formula); runs A and B (hand Adam); edge angles 130, 3, 25 (hand Adam); 0.9 on the ten days (Fractions).
- l7: $\tfrac12 - 4/\pi^2$ (SciPy `quad`); PCA 0.111 and 0.0967 (SVD); net 0.0031 and 0.0026 from the shipped weights, retrained by hand backprop to $10^{-5}$; 2.7%; rank correlation 0.972 (rank formula); 131 (counts); trap errors to 3 places (hand backprop); tear near 1 radian, error under 0.02.
- l8: model retrained by hand Adam to $10^{-5}$; threshold 1.62 (hand interpolation); 11 flags, 8 planted, 3 false of 141, precision 0.727; gap 2.37 to 5.46; fall 0.47 and 5.5%; trap 18.43 and 2 flags; regime 5 alarms (4 planted) then 54%; 0.95 (Fractions).
- Sets: every key by Fractions, the quadratic formula or quadrature; thresholds of the training widgets checked on four seeds each by route B with margin (tanh held-out error under 0.01 against the 0.02 test; linear within 0.002 of PCA against 0.01).
- Literals (50): scenario givens in prompts, how-line test settings, and the module's planted day-700 move.

## Conventions

- Rows are days; $\mathbf z = \mathbf x\mathbf W_{\text{enc}}$, $\hat{\mathbf x} = \mathbf z\mathbf W_{\text{dec}}$; the reconstruction error is the mean over rows of the squared distance (sum along the row), as `interp` L3's "mean $\lVert h - \hat h\rVert^2$". The l8 model uses `interp`'s bias layout: $\mathbf z = (\mathbf x - \mathbf b_{\text{dec}})\mathbf W_{\text{enc}} + \mathbf b_{\text{enc}}$, $\hat{\mathbf x} = \mathbf z\mathbf W_{\text{dec}} + \mathbf b_{\text{dec}}$.
- PCA error with $n$ (the mean over rows), so `eigen` l11's ten days give 0.9 against the eigenvalue 1 of $\boldsymbol\Sigma$ with $n - 1$; l6 says so.
- Starts: linear weights $0.1\,\mathcal N(0, 1)$ from `default_rng(seed)`, encoder first; tanh nets from `init_tanh_ae`. Adam from `nt_ops_l1.adam_step`, steps counted from 1.
- Seeds: `arc(200, 0.05, 0)` train and seed 1 held out; `odd_day_panel(3)` for the lesson, panels 3, 4 and 7 in the performance tests.

## Deviations from the brief

- l6's second code screen is `check_pca(X, k, steps, lr, seed)` returning the trained error, the closed form and the angle, with l5's `train_autoencoder` in the prelude, instead of a second copy of the training loop as `train_linear_ae`.
- l7's `make_arc` and `compare_with_pca` share one widget; `compare_with_pca` takes the shipped trained weights.
- l8's `flag_days(errors, thr, labels)` takes the labels and returns `(flagged, precision, recall)`.
- l5, l6 and l8 open with an interactive problem (drag or slider) rather than a separate explore screen; l7 has an explore.
- The brief's `rp_ops.py` is `representations_ops_l2.py` (interfaces file). No autograd op was missing: `tanh`, `exp`, `log` and indexing are in v1.0.

## `representations_ops_l2.py` (v1.0): public names

- `arc(n=200, noise=0.05, seed=0, full=False) -> X` of shape `(n, 2)`.
- `init_tanh_ae(d, hidden, k, seed) -> [W1, b1, W2, b2, W3, b3, W4, b4]`.
- `tanh_ae_encode(params, X) -> Z`; `tanh_ae_forward(params, X) -> X_hat` (arrays or `Tensor`s; gradient-checked to relative $10^{-6}$ in the number script).
- `odd_day_panel(seed=3, regime=False) -> (R, kind)`; constants `ODD_DAYS`, `FALL_DAY`.

## Proposed course.json change

None.

## Playthrough with and without --mobile

See the end of this file.

All seven files with `--local-cdn <pkgs>`, desktop and `--mobile` (440 px): all passed. l5 14 checks, l6 14, l7 15, l8 14, quizzes 3/3 each; review-2 10 of 10; homework-2 8 of 8, 36 of 36 marks, performance starter fails, longform marked by the button; problems-2 12 parts with `--why`, 20 typed slips routed. l6, l7 and l8 were replayed on the desktop after their last text edits. Screens read at 440 px: the plane hooks, the error histogram with its threshold, the error path with markers and the fall-day bars fit; marker labels were shortened after the desktop shot showed "false alarm" crossing the line.
