# nn-train level 4 (Experiments you can trust): report

Branch `ai-w5-nn-train`, from `ccf3e7e7` with `e8119d24` merged (the stricter `claim(True, covers=...)` rule). Skill `nt-experiment` on every lesson and item. Lesson ids, names and objectives as in `course.json`.

## Files written

| File | Screens or items | Notes |
|---|---|---|
| `l13-one-seed-one-draw.json` | 11 screens, 4 quiz | ten seeds in `bars` (tap the runs under a one-run "improvement"), range, mean and sd by hand (table), what a seed controls (multi), split seed against training seed (grouped bars, cites `validation` l1), trap "best of ten", edge case two stalled seeds (narrow net), code `seed_summary`, code `set_all_seeds`, standard error, transfer (a 0.5% claim) |
| `l14-ablations.json` | 11 screens, 3 quiz | hook "which change did the work", removal bars (tap), the effect defined, ranking from the removal table (order), the add-one direction and the interaction (2 by 2 table widget), runs needed, trap "one seed each" (seed 6), edge case "helps only with another" (a supposed table), rule, code `ablation_table` + `interaction`, transfer (five features and a loss) |
| `l15-training-log.json` | 11 screens, 3 quiz | two logs differing in the split seed (tap the row), what a log holds (multi), write an entry (table widget), audit a log, Karpathy's recipe (order with a distractor), overfit one batch (`series`, zero start stuck at $\ln 2$), trap "test scored twice", edge case stopped and resumed (three resumes, three losses), code `audit_log`, code `overfit_one_batch`, transfer (a bad month) |
| `l16-paired-seeds.json` | 12 screens, 3 quiz | A and B per seed (grouped bars), A against B scatter with the diagonal (tap), the paired $t$, five pairs by hand, Welch on the same runs, the interval (`number-line`), twenty set-ups, trap "wrong test, one pair", edge case batches not fixed, code `paired_t` + `compare_configs`, code `runs_needed`, transfer (Sharpe for the committee) |
| `review-4.json` | 8 items, `pass` 0.8 | every lesson, difficulty 2 to 4 |
| `homework-4.json` | 8 items | performance task `h4-report` (code, difficulty 5), `h4-logdiff` (code), `h4-order` (order with two distractors), `h4-slide` (longform, 10-point rubric), three numerics, one choice |
| `problems-4.json` | 3 problems, 13 parts | difficulty 5, 4, 3; every lesson used (P1: l16 and l13; P2: l14; P3: l13 and l15) |
| `app/content/data/ai/nt_ops_l4.py` | module, 6,317 bytes | public names at the end |
| `app/content/data/ai/nn-train-seeds.json` | data, 110,211 bytes | 130 runs: per run the configuration, seed, split seed, final validation, test and training loss, and both curves thinned to 50 points |
| `docs/reports/nn-train-L4-numbers.py`, `docs/reports/nn-train-4-perf.md` | | the script writes the data file with `--write` |

## Gates

1. Validator: 0 errors. Warnings on the level's files: point hints without a highlight, problem screens without a canvas, `O2-long-sentence` advisories.
2. Voice: `voice-scan.py 35` on the course folder: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans.
3. Numbers: `node tools/run-number-scripts.mjs --python <venv> --only nn-train-L4`: passed, 422 of 422 checks, strict coverage 0 uncovered (4 literals with reasons: two tolerances or invented settings, a step count in an invented quiz). No `claim(True, covers=...)`: every covered number comes from a two-route comparison or a recomputation. The 31 byKey lines that state other numbers were read by hand.
4. Code widgets: `grade-all.mjs --code` on all seven files: 9 Python widgets, 0 failures in Pyodide; 33 mutants, each failing its named test first (also checked in the number script).
5. Playthrough with `--local-cdn <pkgs> --mobile` (desktop and 440 px): the four lessons, review-4, homework-4 ("1 performance starter fail", longform marked by the button) and problems-4 all passed; l15, l16, review-4 and problems-4 were replayed after their last edits. Screenshots read at 440 px: no overlaps or empty canvases.
6. `fresh-check.mjs --file` on review-4, homework-4, problems-4: 0 hits (advisories only: the stock 0.975 and 2.262). `same-course-reuse.mjs --all`: no errors on nn-train. A text hit (review-4 item 8 retold l14's quiz 2x2) was rewritten, and review-4 item 1's numbers moved off l10's.

## Decisions a reader should know

- **Model and data.** The level 1 spiral net (2-16-16-2 tanh), on 600 points from `spirals(600, seed=0, noise=0.05)` split 400/100/100 by `default_rng(split_seed).permutation(600)`; 300 steps of batch 32. One seed gives three generators (`SeedSequence(seed).spawn(3)`: weights, batches, dropout masks), so turning dropout off leaves the batches alone; the split has its own seed.
- **Configurations shipped.** A (Adam 0.01) and B (Adam 0.015) on seeds 0 to 9; B with batches from seed + 100 (the l16 edge case); a narrow net (6 units, Adam 0.03); the eight mixes of {SGD 0.5, Adam 0.02} × layer norm × dropout 0.1 for the ablation; A on seed 0 over split seeds 1 to 9.
- **Stability.** A 1e-13 change to the starting weights moves every shipped run's final loss by at most 5e-7 relative (the high-rate SGD runs that fail on some seeds were chaotic, 150% moves, and were not used: the bimodal edge case is the narrow net instead, stable to 4e-13). So the number script retrains all 130 runs and requires the file to 1e-6 relative; it compares `train_run` with a hand-written backward (layer norm and dropout included) on 20-step runs of all 12 configurations to 1e-9. Every figure the lessons state is a statistic of the file, computed by NumPy and by the `statistics` module (and SciPy for $t$, $p$ and intervals).
- **Dropout hurt.** On this small net dropout raised the validation loss in every mix, so the ablation teaches a change that cost the full set-up. No mix showed a change that helps only with another, so l14's edge case is a supposed 2 by 2 table, said as such.
- **sd convention.** Seed sds divide by $n - 1$ throughout (the paired $t$ needs it); `validation` l1 used `np.std` (divide by $n$), so l13 says which and a mutant takes the other.
- **l16's pair.** B beats A on all 10 seeds, not 9 as the brief's example; the lesson says so.

## Numbers and their sources (recomputed by the number script)

- l13: A mean 0.108, sd 0.0457, range 0.065 to 0.199 (0.134); seeds 2 and 5 under 0.073; five seeds 0.0992 and 0.0373; split-seed sd 0.029; narrow net: seeds 4 and 9 at 0.42, the other eight 0.114, all ten 0.176; standard error 0.0145; $0.006\sqrt 2 = 0.0085$.
- l14: means 0.205 (SGD) to 0.022 (Adam + layer norm); full 0.045; removal effects 0.058 (Adam, sd 0.066), 0.111 (layer norm, sd 0.047), $-0.024$ (dropout, sd 0.015); Adam's gain 0.121 without layer norm and 0.064 with it, interaction 0.057; seed 6: 0.237 against 0.118; 40, 80, 35 and 15 runs.
- l15: split 0 against split 1, 0.093 and 0.041; B seed 4, 0.099; one batch of 8 from 0.650 to 0.00041 in 200 Adam steps, zeros stuck at $\ln 2 = 0.693$; resume 0.0927 (all state), 0.1279 (batch stream restarted), 0.1101 (Adam reset too).
- l16: $\bar d = -0.0206$, $s_d = 0.0180$, $t = -3.63$, $p = 0.0055$; Welch $t = -1.03$, $p = 0.32$; interval $-0.0334$ to $-0.0078$; five pairs $-0.0258$, 0.0212, $-2.72$; batches not fixed: correlation 0.92 to 0.65, $s_d = 0.0346$, $t = -2.22$, $p = 0.053$; $1 - 0.95^{20} = 0.642$; 7 and 24 seeds for a 0.02 gain (formula and a power search agree); Sharpe interval 0.036 to 0.204.
- Review, problems, homework: every key and slip at its path (see the script).

## Training cases and their desktop time

CPython per case (Pyodide is about 3 to 5 times slower): `set_all_seeds` 5-step runs 2 to 9 ms (budget 3,000 ms); `overfit_one_batch` 200 steps 70 to 100 ms, 5-step exact runs 2 ms (budget 3,000 ms); `paired_t`'s SciPy check imports `scipy.stats` in the prelude (636 ms in CPython, load not charged to the tests; budget 8,000 ms); every other case under 10 ms. Whole files in the Pyodide playthrough: l15 29 s and l16 43 s including the package loads. Exact learning-loop tests: `set_all_seeds` (5 steps, relative $10^{-7}$) and `overfit_one_batch` (5 steps, twice).

## Proposed course.json change

None.

## nt_ops_l4.py public names as shipped

Version 1.0, 6,317 bytes, SHA-256 `788be546681f9a2434e1a6296056da0df6087414046446f0b3093e20bb01e4db`; imports NumPy, `autograd` (v1.0), `nt_ops_l1`, `nt_ops_l2` (layernorm) and `nt_ops_l3` (dropout). `from nt_ops_l4 import ...`
- `course_data(split_seed=0) -> (X (600, 2), y (600,), tr (400,), va (100,), te (100,))`: `spirals(600, seed=0)`, rows split by `default_rng(split_seed).permutation(600)`.
- `seed_streams(seed) -> (init_rng, batch_rng, dropout_rng)`: `default_rng` of each child of `SeedSequence(seed).spawn(3)`.
- `init_params(rng, hidden=16, ln=False) -> list`: `[W1, b1, W2, b2, W3, b3]` for 2-h-h-2, W drawn $N(0, 1/\text{fan\_in})$ in that order, b zeros; with `ln`, `[g1, c1, g2, c2]` (ones, zeros) appended.
- `net_logits(params, X, ln=False, p=0.0, rng=None) -> Tensor`: per hidden layer `X @ W + b`, layernorm when `ln`, tanh, dropout when `p > 0` and `rng` is given.
- `train_run(config, seed, split_seed=0, steps=300, batch=32, every=6, batch_seed=None) -> dict(val, test, train, val_curve, train_curve)`: `config` keys `opt` ("sgd" or "adam"), `lr`, `ln`, `p`, `hidden`; each step `batch_rng.choice(400, batch, replace=False)`; `batch_seed` takes the batch stream from `seed_streams(batch_seed)`.
- `t_cdf(x, df) -> float`, `t_quantile(q, df) -> float`: Student's $t$ by the regularised incomplete beta and bisection; within $10^{-10}$ of `scipy.stats.t` (checked by the script).
