# gpt level 4: Scale (report)

Author: content agent, wave 6, branch `ai-w6-gpt`. Brief: `docs/briefs/gpt.md` Level 4. Skill `gpt-scale` throughout; ids, names and objectives from `course.json`. This level also holds the old `ai-papers` scaling level (F4); `ai-papers` L2 can build its Chinchilla replication on l15 and l16.

## Files

| File | Screens or items | Quiz | Code widgets (mutants) |
|---|---|---|---|
| `l13-counting-parameters.json` | 11 | 3 | `gpt_params` (4) |
| `l14-counting-compute.json` | 12 | 3 | `train_flops` + `attention_flops` + `days_to_train` (4) |
| `l15-power-laws.json` | 12 | 3 | `fit_power_law` + `predict_loss` (4) |
| `l16-a-fixed-budget.json` | 11 | 3 | `chinchilla_loss` + `optimal_split` (4) |
| `review-4.json` | 10 items, `pass` 0.8 | | difficulty 2 to 4, every lesson at least twice |
| `homework-4.json` | 6 items | | `h-scaling-fitter` performance task (4 mutants), `config_costs` (3), order with a distractor (the derivation of $6ND$), longform (10-point rubric), numeric, choice |
| `problems-4.json` | 3 problems, 10 parts | | parameters to FLOPs to days to pounds (d5), two pilot runs (d4), the 20-tokens rule at a budget (d3) |

No data file and no module: everything is arithmetic and small NumPy fits. Canvases: `table`, `bars` with frames (parameter shares by width; forward and backward shares), `plane` (log-log line with an exponent slider, the floor curve, loss along a fixed budget with a point on the curve). Performance report: `docs/reports/gpt-4-perf.md`.

## Self-check (SESSION PROTOCOL 4)

1. Validator: 0 errors; no `[source-ban]` or `[ai-mutants]` warning on these files.
2. Voice: `voice-scan.py 35` on the course folder: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `node tools/run-number-scripts.mjs --python <venv> --only gpt-L4`: passed, 2 s; strict coverage, 0 uncovered, 23 literals with reasons; 194 checks.
4. Playthrough, `--local-cdn`, `--why`, desktop and `--mobile`, all seven files: all passed (lessons 14 to 15 checks, review 10 of 10, homework 6 of 6 with the performance starter failing and the longform marked). problems-4 failed once on a slip the field could not type (a value of 83 billion billions); the slip was replaced by leaving out the 20, and the replay passed.

Also `grade-all.mjs --file <each> --code --local-cdn`: 0 failures (6 Python widgets, 23 mutants each failing its named test). `same-course-reuse.mjs --all`: nothing for the course (after rewording one problem explanation that echoed a review item).

## Numbers and sources (two ways each, in the script)

- Parameters (formula against summing `gpt_ops_l2.shapes`): GPT-2 small 124,439,808 (tied, no head bias; block 7,087,872; embeddings 31.6%); untied without a head bias 163,037,184; tiny GPT tied the GPT-2 way 15,872; rule $12d^2$ misses 416 = $13d$ at $d = 32$; GPT-3 by $12Ld^2$ 173.9 billion; a "7B" configuration 6.70 billion; review 236,406,784; problem 1,315,723,264.
- Compute: GPT-3 $3.15 \times 10^{23}$ (the paper's table says $3.14 \times 10^{23}$; we quote the rule's 3.15 and name the table's); Chinchilla $5.88 \times 10^{23}$, 20 tokens per parameter; the tiny GPT's actual run of 5,000 steps (2,560,000 tokens): $2.77 \times 10^{11}$, 131.8 s at 2.1 GFLOP/s against 280 s at the measured 56 ms a step (0.99 GFLOP/s effective); attention $2LTd$ is 11.1% of GPT-2 small's block FLOPs at $T = 1{,}024$ and equals them at $T = 12d = 9{,}216$; GPT-3 on 1,000 GPUs at 312 TFLOP/s and 40%: 29.2 days, about £1,052,000 at £1.50 an hour.
- Power laws: $5N^{-0.1}$ (factor 0.7943 a decade, slope $-0.1$, $a = 5$); noisy fit, seed 0, 2% noise: $\alpha = 0.0979$ (np.polyfit and covariance over variance); Kaplan 2.8300, 2.3756, 1.9943 and 1.6741 at $10^8$ to $10^{11}$, factor 0.8395.
- Chinchilla's fitted law ($E = 1.69$, $A = 406.4$, $B = 410.7$, $\alpha = 0.34$, $\beta = 0.28$): 1.9366 at (70B, 1.4T), 2.0023 at (175B, 300B); at $5.76 \times 10^{23}$ FLOPs (Gopher's budget, which Chinchilla was sized for) $N = 3.22 \times 10^{10}$, $D = 2.98 \times 10^{12}$, 92.6 tokens per parameter (closed form against a grid of 400,001 sizes). At the brief's $5.88 \times 10^{23}$ the ratio is 92.8; both "about 93". Ten times the compute grows the model 2.83 times and the data 3.53 times. 8B on 15T: 1,875 tokens per parameter.

## Brief deviations and notes

- l14 uses the tiny GPT's real run (5,000 steps), so its compute is $2.77 \times 10^{11}$, not the brief's 2,000-step $1.107 \times 10^{11}$.
- `gpt_params(..., tied)` follows GPT-2: a tied head has no bias of its own, so the tiny GPT tied is 15,872. l5's quiz kept the head bias (15,937); l13 screens[8] names the difference.
- The 20-tokens rule is taught as Chinchilla's headline and the fitted law's 93 as l16's trap, with Besiroglu et al. (2024) named as the re-fit of the third approach, which comes out near 20.
- The homework fits the full two-variable law with NumPy (grid over the exponents, least squares for the rest): no SciPy import.

## Proposed course.json change

None.

## Backlog

No new bullets for this level (the `plane` log-axis limitation is raised under level 3).
