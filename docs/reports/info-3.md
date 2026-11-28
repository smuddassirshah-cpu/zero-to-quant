# info level 3 (Mutual information): author report

Branch `ai-w1-info`. Brief: `docs/briefs/info.md` Level 3. Generators and the simulation in the scratchpad `info-3` folder (not committed); the number script reruns the simulation itself.

## Files

| File | Screens or items | Quiz | Notes |
|---|---|---|---|
| `l9-information-shared.json` | 11 | 3 | grouped bars of 2 by 2 joint tables (frames over four signals), table of $H$s, `mutual_information` |
| `l10-dependence-as-divergence.json` | 10 | 3 | $Y = X^2$ table with products to fill, `order` proof $I = D(p_{XY} \| p_X p_Y)$, `mi_as_kl`, volatility transfer (correlation 0, 0.125 bits) |
| `l11-features-and-lost-information.json` | 10 | 3 | email feature table, merged buckets, `graph` chain $X \to Y \to Z$, `rank_features`, signal binning transfer |
| `l12-a-signal-and-tomorrow.json` | 11 | 3 | bars of simulated mean estimates (frames), histogram of 2,000 null runs with a cut at 0.00173, `mi_estimate` |
| `review-3.json` | 10 items, `pass: 0.8` | | all 10 if-mutual (one also if-cross), difficulty 2 to 4 |
| `homework-3.json` | 6 items | | `order` ($H(Y \mid X) \le H(Y)$ via MI as KL), `null_mi_quantile` (d5, thresholds, `budget` 3000), longform (50 signals), performance code task, two numeric |
| `problems-3.json` | 3 items, 11 parts | | difficulty 4, 5, 3; a fresh 2 by 3 table, its merge and bias, a relay chain |

## Self-check (SESSION PROTOCOL 4)

1. Validator: 0 errors; no warning on any info file.
2. Voice: `voice-scan.py 35`: 0 over 35 words (two `how` lines were split), 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `docs/reports/info-L3-numbers.py` exits 0, 347 of 347 checks. Every MI by $H(X) + H(Y) - H(X, Y)$ and by $D(p_{XY} \| p_X p_Y)$; the l12 simulation is rerun (`default_rng(2026)`, 2,000 runs at 250, 1,000 and 5,000 days) and its means, shares (73.7%, 30%, 5 runs in 2,000) and the 2,000 histogram values are checked against the JSON; biases by the formula two ways. Code solutions pass their tests in CPython; starters fail. The 36 "check by hand" byKey lines were read.
4. Playthrough: all four lessons, `review-3`, `homework-3` and `problems-3` with `--mobile --local-cdn <pkgs>`: all passed at 1280 and 440 (quizzes 3/3 each; review 10 of 10; homework 6 of 6 with the performance starter failing; problems 3 problems, 11 parts). l12, review-3 and homework-3 were replayed after the last edits. Screenshots read: the histogram's cut line, the chain graph and the joint-table bars read clearly at 440.
- Also: `grade-all.mjs` on the seven files, 0 failures; `fresh-check.mjs --file content/courses/info/problems-3.json`, 0 hits.

## Numbers and sources

All the brief's level 3 figures (0.029049, 1.971, 0.971, 0.9183, 0.3282 and 0.2561, 0.531 and 0.3199, the weak signal 0.001732 bits, the simulated means and shares) are recomputed. Two refinements: on 5,000 days the share of useless runs above the true value is 5 in 2,000, written "0.25%" (the brief's "0.3%" is the same figure rounded up); on 1,000 days it is 29.95%, written "30%". New figures (volatility 0.125, binning 0.0131 and 0.0085, the email features 0.163 and 0.003, review and problem-set values) are in the script both ways.

## Conventions

- Rows are the signal $X$, columns the outcome $Y$, as in `random-vars` l13; $k_X$ and $k_Y$ count the states seen in the sample. A return of exactly 0 counts as down. Seeds: `random.Random(11)` for the l12 null sample, `random.Random(5)` for the performance task, numpy `default_rng(2026)` for the simulation.

## Proposals

- No `course.json` change.
