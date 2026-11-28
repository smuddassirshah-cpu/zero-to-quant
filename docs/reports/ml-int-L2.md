# ml-int level 2: From-scratch coding under time (report)

Branch `ai-w7-ml-int`. Brief: `docs/briefs/ml-int.md`, Level 2. Report and script named `ml-int-L2.md` and `ml-int-L2-numbers.py` as the orchestrator asked; the performance report is `docs/reports/ml-int-2-perf.md` (the name `perf-reports.mjs` reads).

## Files

| File | Screens or items | Code widgets (tests, mutants) |
|---|---|---|
| `l5-stable-softmax.json` | 12 screens, 3 quiz | `max_shift` (5, 3), `log_sum_exp_rows` (6, 3) |
| `l6-attention-from-scratch.json` | 12 screens, 3 quiz | `mi_split_heads` (5, 3), `mi_causal_mask` (5, 3) |
| `l7-k-means-against-the-clock.json` | 11 screens, 3 quiz | `assign_nearest` (5, 3), `update_centres` (5, 3) |
| `l8-a-layers-backward-pass.json` | 12 screens, 3 quiz | `relu_gate` (4, 3), `mi_grad_check` (4, 3) |
| `review-2.json` | 8 items, `pass` 0.8, untimed (the brief sets no clock), `pace` per item | none |
| `homework-2.json` | 6 items | `mlp_train_step` (7, 6, difficulty 5, performance task `code`), `top_k_attention_weights` (6, 3); `order` 15-minute plan with a distractor; `longform` session review (10-point rubric, model answer) |
| `app/content/drills/mi-*.json` | 6 drills, pack `mi`, skills `mi-code`, Python, NumPy | row softmax (9 tests), cross-entropy (9), causal attention (9), k-means (9), linear and ReLU backward (8), layer-norm backward (8); each two examples, constraint objects for every argument, three planted solutions with one `nearMiss` |
| `app/content/drills/sessions/mi-sixty.json` | the set session as the brief writes it | |
| `app/content/drills/index.json` | six rows appended (`id`, `name`, `course`, `difficulty`) | |

Names: `split_heads` and `causal_mask` are already lesson functions in `sequence` l11 and l10, so the l6 code screens use `mi_split_heads` and `mi_causal_mask`; `layernorm_backward` is used by `nn-train` homework-2, so the drill's function is `mi_layernorm_backward` (the drill id stays `mi-layernorm-backward`). `grad_check` is a lesson function in four other courses (`fresh-check` flagged it against `rl` l16), so l8's is `mi_grad_check`. No lesson and drill share a function name. Pattern: `PATTERNS` in `drill-lib.js` has no ML slug and content agents do not edit engine files, so the drills carry no `pattern` (optional per AUTHORING section 5); raised in the inbox. Each lesson's last screens send the learner to its drills by route (`#drill/mi-row-softmax` and so on, with paces 10, 15, 20, 15 and 20 minutes); l8 ends with `#drill/session/mi-sixty` and reads `{{carry.session.minutes1|none}}`, `minutes2` and `solved`.

## Self-check (SESSION PROTOCOL 4)

1. Validator: 0 errors. Advisory warnings left: four `O2-long-sentence`, a few point hints without highlight, two ladders that change canvas kind.
2. Voice: `voice-scan.py 35` with `VOICE_BASE` the course folder: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans. The six drills, scanned from a scratch copy, also 0 and 0.
3. Numbers: `ml-int-L2-numbers.py` through the CI runner: 1 passed, 254 of 254 checks, strict coverage 0 uncovered, 12 literals (tolerances and steps, a drill pace, story details, the invented session minutes of the model answer).
4. Playthrough with the local CDN: the four lessons, `--set ml-int/review-2` and `--set ml-int/homework-2`, all passed with and without `--mobile` (the performance starter fails as required); the six drills with `--drill`, with and without `--mobile`: all passed (starter fails, model passes every test); `--session` (the sample session, the only one the tool sits): passed. `planted-check.mjs --near-miss --require` on the six drills: 0 failures (18 planted). `grade-all.mjs --code --strict-feedback` on the six course files: 0 failures (10 code widgets, 33 mutants). `same-course-reuse.mjs`: no error for ml-int. `fresh-check.mjs` on the six course files and the six drills: 0 hits after two fixes (review-2 item 3 reworded, as it repeated an l6 quiz question; `grad_check` renamed).

## Numbers and their second methods

- Softmax (l5, drills 1 and 2): $(1000, 1001, 1002)$ gives $(0.0900, 0.2447, 0.6652)$, log-sum-exp $1002.4076$, cross-entropy $2.4076$ (target 0) and $0.4076$ (target 2); route A $e^{-2}$, $e^{-1}$, 1 over their sum, route B `scipy.special.softmax` and `logsumexp`. float16 overflow above $\ln 65{,}504 = 11.09$; $e^{1000}$ has 435 digits (closed form and `Decimal`).
- Attention (l6, drill 3): scores $[[0.7071, 0], [0.7071, 1.4142]]$, weights $[[1, 0], [0.3302, 0.6698]]$; route A $1/(1 + e^{1/\sqrt 2})$, route B a NumPy forward pass. Per-head scale $\sqrt 8 = 2.8284$. The unmasked first row is $(0.6698, 0.3302)$, the trap's numbers.
- k-means (l7, drill 4): centres $(1/3, 1/3)$ and $(16/3, 16/3)$, inertia $8/3 = 2.6667$ after three passes, first update $(4, 4.25)$; route A Fractions, route B the coded loop. The script found and confirms the near-miss case: points $(2, 7), (5, 5), (8, 0), (2, 3), (9, 0), (4, 4), (0, 4)$ with $k = 2$ change labels on pass 4 and stop on pass 5 at $(2.6, 4.6)$ and $(8.5, 0)$, inertia 24.9; three fixed passes give other centres. Stocks: $\|a - b\|^2 = 2T(1 - \rho) = 200$ (checked on a simulated standardised pair).
- Backward passes (l8, drills 5 and 6): $\mathbf{Z} = [[5, 3, -1], [1, 0, -3]]$, linear $d\mathbf{X} = [[-1, 2], [-1, -1]]$, with the gate $[[1, 2], [-1, -2]]$, $d\mathbf{W} = [[-2, 0, 0], [3, 0, 0]]$; at the kink central differences give $-1.5$ against $-2$ (convention $>$) and $-1$ ($\ge$). Layer norm $d\mathbf{x}$, $d\boldsymbol\gamma$, $d\boldsymbol\beta$ as in the brief, to six places. Route A the formulas, route B central differences. SiLU slope at 2: $1.0908$. A one-sided difference on $e^{5x}$ at step $10^{-4}$ is off by 1 part in 4,000 (the first draft said 400; the script caught it).
- Review and homework: 0.75, $\ln 4 = 1.3863$, 4, 2, 3, the $d\mathbf{W}$ entry 3, layer-norm value $1.3363$, $2048^2 \times 1024 \approx 4.29$ billion, top-k $(0.625, 0.375, 0)$; `mlp_train_step`'s exact 3-step loss recomputed by steps taken with central-difference gradients (agree to $10^{-7}$), and 20 steps halve the loss.

## Timing

No graded case trains beyond `mlp_train_step`'s 3 and 20 steps on a batch of 8 (milliseconds). Drills keep each test to small arrays; the drill page has no `budget`.

## Shared code

None; every task is self-contained, as drills must be.

## Proposed course.json change

None.

## Backlog bullets

Five, under "Raised later (ml-int level 2):".
