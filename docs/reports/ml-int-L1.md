# ml-int level 1: Theory questions aloud (report)

Branch `ai-w7-ml-int` from `56dd6746`. Brief: `docs/briefs/ml-int.md`, Level 1. The orchestrator named the report `ml-int-L1.md` and the script `ml-int-L1-numbers.py` (the brief says `ml-int-1.md` and `ml-int-1-numbers.py`); the CI runner finds `ml-int-L1`. The performance report keeps the tool's name, `docs/reports/ml-int-1-perf.md`.

## Files

| File | Screens or items | Code widgets (tests, mutants) | Notes |
|---|---|---|---|
| `l1-backprop-on-a-whiteboard.json` | 10 screens, 3 quiz | `two_layer_grads` (6, 4) | `graph` with `valueLines` (forward value, gradient), explore frames through the backward pass, `derive` order, transfer to log loss, follow-up on tanh |
| `l2-why-adam.json` | 11 screens, 3 quiz | `adam_first_step` (7, 5) | `bars` (log y), `series` of the correction factors with frames, AdamW `order` follow-up |
| `l3-double-descent.json` | 11 screens, 3 quiz | `min_norm_test_error` (5, 4), `budget` 4000 ms, generator in `prelude` | `series` on a log10 p axis, hook with the right half hidden, norm explore, ridge edge and follow-up |
| `l4-deep-learning-quickfire.json` | 11 screens, 4 quiz | `sanity_checks` (6, 5) | `console` logs, `bars` with a `stops` control on d and `derive` |
| `review-1.json` | 8 items, timed 600 s, `lockAtZero`, `pass` 0.8 | none | two items per lesson, tags `backprop-by-hand`, `optimisers`, `double-descent`, `dl-quickfire` |
| `homework-1.json` | 7 items | `mlp_backward` (6, 5, difficulty 5), `adamw_step` (6, 4, difficulty 3) | `order` "explain backprop" with a distractor, `longform` double descent (10-point rubric, model answer), performance task `h7-derive-tanh-layer` (`derivation`) |

Every lesson has `minutes: 15`, the real time in its first prose ("about fifteen minutes", per-question interview pace), `pace` on the hook and the follow-up (300, 180, 240 and 60 s as the brief sets; follow-ups 60 to 120 s), and tags with the family first. Lesson shape: hook on the canvas, explore, ladder, trap, edge case, `derive` (l1) or `generalise`, transfer at a fund or lab, code screen, and a closing "The follow-up".

Deviations from the brief, each small: the l1 trap is an `expression` matrix answer with the slip $[[-7, -14], [3.5, 7]]$ as a `wrong` entry (a `numeric` widget takes one number); review-1 and homework-1 carry fresh numbers (a second ReLU network, betas 0.8 and 0.99, 250 points, a 50,257-token vocabulary, fan-in 2,048, a constant gradient, log loss with target 0). Homework 1 gained a seventh item, the performance task, because the l1 objective starts with "Derive" (validator rule, AUTHORING section 5).

## Self-check (SESSION PROTOCOL 4)

1. Validator: `node tools/validate.mjs`: 0 errors. Warnings left on the level's files are advisory (`O2-long-sentence` on four sentences between 20 and 25 words, a point hint without highlight on four screens, one ladder that changes canvas kind).
2. Voice: `VOICE_BASE=app/content/courses/ml-int python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans.
3. Numbers: `docs/reports/ml-int-L1-numbers.py`, through `node tools/run-number-scripts.mjs --python <venv> --only ml-int-L1`: 1 passed, 267 of 267 checks, strict coverage 0 uncovered, 5 literals (beta2 0.999 and 0.99, epsilon and tolerances $10^{-8}$ and $10^{-6}$, the simulation size 20,000).
4. Playthrough with `--local-cdn <scratchpad>/aitiming/pkgs`: the four lessons, `--set ml-int/review-1` and `--set ml-int/homework-1`, all passed on desktop and with `--mobile` (screenshots read; the `graph` node positions were moved twice so the crossing edges' weight labels separate at 440 px).
5. Also: `node tools/grade-all.mjs --code --strict-feedback` on all six files: 0 failures (59 widgets, 6 code widgets, 27 mutants each first failing its named test, every `byKey` test line reached). `same-course-reuse.mjs --all`: no error for ml-int. `fresh-check.mjs --file` on the six files: 0 hits.

## Numbers and their second methods

- Backprop (l1): $\mathbf{h} = (-1, 2.5)$, $\mathbf{a} = (0, 2.5)$, $\hat{y} = -2.5$, $L = 6.125$, $\partial L/\partial \hat{y} = -3.5$, $\partial L/\partial \mathbf{w}_2 = (0, -8.75)$, $\partial L/\partial \mathbf{a} = (-7, 3.5)$, $\partial L/\partial \mathbf{W}_1 = [[0, 0], [3.5, 7]]$. Route A the hand formulas, route B central differences (agree to $10^{-6}$). Log loss: $\sigma(-2.5) - 1 = -0.9241$ (closed form against a central difference of the log loss). Quiz 2 ($\mathbf{x} = (2, 1)$): $-4$.
- Adam (l2): first corrected step 0.001 for $g = 10^{-4}, 1, 100$; uncorrected 3.1623 times larger; noisy case $|\hat{m}_2|/\sqrt{\hat{v}_2} = 1/19 = 0.0526$; $g = 10^{-8}$ gives 0.0005; factor at step 2 is 500.25; step 40's factor for $v$ is 25.49. Route A closed forms, route B the update coded with its moving averages.
- Double descent (l3), scikit-free, NumPy 2.0.2 with one BLAS thread, medians over 20 seeds: 0.316 (5), 0.249 (10), 0.25 (20), 0.355 (30), 0.77 (36), 7.63 (40), 0.589 (44), 0.248 (60), 0.12 (100), 0.0644 (400), 0.0646 (2,000); noise sd 0.2: peak 8.43, floor 0.122. Median norm 1.17 at 10 against 10.1 at 40. Ridge tuned per $p$ on a grid: 0.218 (10), 0.105 (40), 0.0463 (400); fixed $\lambda = 0.01$: 0.472 at 40, still the peak; $\lambda = 0.001$: 1.64 at 40. Route A `pinv` (normal equations for ridge), route B `lstsq` (SVD for ridge). The brief's figures are reproduced exactly; the ridge edge was checked twice before it was stated, as the brief asked.
- Quickfire (l4): $\ln 65 = 4.1744$, $\ln 27 = 3.2958$ (closed form against a coded softmax cross-entropy of uniform logits), He sd 0.0625 (against the Fraction 1/16), dropout 1.25 (against 5/4), dot-product sd 8 exact and 8.037 from 20,000 seeded pairs, 1.005 after scaling (elementwise sum against `einsum`), 9.7 is 2.32 times $\ln 65$.
- Review and homework: 12, 0.64, 2, 250, $\ln 50{,}257 = 10.825$, 1/32 = 0.03125; 0.003, $-0.1517$, 0.899 and the $-0.001$ AdamW gap (against a decay-first AdamW written separately), the five-step AdamW run (two implementations agree to $10^{-12}$).
- Code tests: every widget's solution passes, the starter fails, each mutant first fails its named test, and the stated expects are recomputed by the other route.

## Timing (budget rule)

No graded case trains. `min_norm_test_error` tests 3 to 5 each run 20 pseudo-inverse fits (60 in all take 0.10 s natively); the widget has `budget: 4000`, so each case's limit is 9 s and the measured lesson play time (16.8 s desktop, the same as the lessons without the budget) shows them well under a third of it.

## Shared code

None. No module was needed: the double-descent generator ships in the l3 code widget's `prelude`; no frozen module is imported.

## Proposed course.json change

None.

## Backlog bullets

Two, under "Raised later (ml-int level 1):" in `docs/BACKLOG-INBOX.md`.
