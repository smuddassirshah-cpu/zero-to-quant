# info level 2 (Cross-entropy and KL): author report

Branch `ai-w1-info`. Brief: `docs/briefs/info.md` Level 2. Generators in the scratchpad `info-2` folder (not committed).

## Files

| File | Screens or items | Quiz | Notes |
|---|---|---|---|
| `l5-paying-for-the-wrong-model.json` | 10 | 3 | grouped bars truth against model (frames), table of $p \times (-\log_2 q)$, `cross_entropy_bits` (raises on $q_i = 0 < p_i$) |
| `l6-the-extra-bits.json` | 11 | 3 | five-model explore, table of KL terms (two negative), `order` proof by Jensen with two distractors, equality `derive`, `kl_bits` (returns `math.inf`) |
| `l7-perplexity.json` | 10 | 4 | number line 1 to 27 with a drag point, unit table, `perplexity(avg_loss, unit)` |
| `l8-likelihood-is-cross-entropy.json` | 10 | 3 | plane: average loss of the 7-in-10 coin against $\theta$ with the entropy line, `avg_nll` and `best_theta` |
| `review-2.json` | 10 items, `pass: 0.8` | | if-cross 5, if-likelihood 5, difficulty 2 to 4 |
| `homework-2.json` | 7 items | | `kl_report` (d4), `best_smoothing` (d5), `order` (likelihood to cross-entropy), longform (training KL), performance derivation (d5), two numeric |
| `problems-2.json` | 3 items, 13 parts | | difficulty 4, 3, 5; every lesson used |

## Self-check (SESSION PROTOCOL 4)

1. Validator: 0 errors; no warning on any info file.
2. Voice: `voice-scan.py 35` on the course folder: 0 over 35 words, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `docs/reports/info-L2-numbers.py` exits 0, 437 of 437 checks: every figure by two methods (log2 sums against ln / ln 2; KL as a direct sum against cross-entropy minus entropy; the coin's loss as a cross-entropy against the averaged negative log-likelihood; smoothing by two loss functions). Code solutions pass their tests in CPython and starters fail. The 36 "check by hand" byKey lines were read.
4. Playthrough: all four lessons, `review-2`, `homework-2` and `problems-2` with `--mobile --local-cdn <pkgs>`: all passed at 1280 and 440 (quizzes 3/3, 3/3, 4/4, 3/3; review 10 of 10; homework 7 of 7 with both longform items marked through the button; problems 3 problems, 13 parts). The first run failed homework-2 at 440: the model proof's `aligned` display ran past the column; it is now a numbered list and the rerun passed. Screenshots read: proof lines wrap cleanly at 440, the boundary plane shows the $\theta \le 0.6$ line, the number line's drag point is clear.
- Also: `grade-all.mjs` on the seven files, 0 failures; `fresh-check.mjs --file content/courses/info/problems-2.json`, 0 hits (4 advisory shared-parameter lines); `rubric-passes.mjs` on the performance item (see `info-2-perf.md`).

## Numbers and sources

The brief's header figures (weather 1.1568, 1.2796, 0.1228 bits and 0.0851 nats; $D(a \| b) = 0.531$, $D(b \| a) = 0.737$; perplexities 4, 11.0232, 11.64; the coin 0.8813 bits at 0.7, 1 bit at 0.5) are recomputed by the script. The 11.6 to 8.7 forward link is $e^{2.4514}$ and $e^{2.1609}$ from `docs/briefs/makemore.md`. New figures (risk model 0.558, return buckets 0.041, boundary gap 0.031, log loss 0.673, smoothing answers, problem set) are in the script with both methods.

## Conventions

- Bits unless a screen says nats; perplexity $2^{H_{\text{bits}}} = e^{H_{\text{nats}}}$. `cross_entropy_bits` raises `ValueError` for $q_i = 0 < p_i$; `kl_bits` and `kl_report` return `math.inf` (said in each `how` and prose). Add-$\alpha$ smoothing: $q_i = (c_i + \alpha)/(N + k\alpha)$, ties to the smallest $\alpha$.
- The $(\tfrac12, \tfrac14, \tfrac18, \tfrac18)$ against equal-chances pair is used only as the trap (0.25 both ways); asymmetry is shown with $a = (0.9, 0.1)$, $b = (0.5, 0.5)$.

## Proposals

- No `course.json` change. No backlog bullets this level.
