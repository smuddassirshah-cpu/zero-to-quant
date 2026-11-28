# sequence level 1 (Recurrent networks): author report

Branch `ai-w5-sequence`, from `dabba415`. Skill `sqn-rnn` on every file.

## Files

| File | Screens or items | Code widgets (mutants) |
|---|---|---|
| `l1-memory-in-a-loop.json` | 10 screens, quiz 3 | `fit_w` (3), `rnn_linear` + `rnn_tanh` (3) |
| `l2-unrolling.json` | 9 screens, quiz 3 | `unroll` + `bptt_grad` (3), `truncated_bptt` (3) |
| `l3-exploding-and-vanishing.json` | 11 screens, quiz 3 | `grad_norm_through_time` + `spectral_radius` + `explodes` (4) |
| `l4-clipping-and-gates.json` | 11 screens, quiz 3 | `clip_by_norm` + `gated_step` (4), `train_gated_copy` (3) |
| `review-1.json` | 9 items, `pass` 0.8 | none |
| `homework-1.json` | 8 items (one `order`, one `longform`, two `code`) | `linear_bptt` (3), `rnn_bptt` performance task (4) |
| `problems-1.json` | 4 chained items, 15 parts, one at difficulty 5 | none |

Number script `docs/reports/sequence-L1-numbers.py`; performance report `docs/reports/sequence-1-perf.md`. No data file and no ops module: the level needs only the frozen `autograd.py` (v1.0, SHA-256 `5917d4ec91f7...`), shipped by path through `data`. The softmax and axis-swap ops are level 2's (`seq_ops_l2.py`).

## Self-check (SESSION PROTOCOL 4)

1. Validator: `node tools/validate.mjs` 0 errors; no `[source-ban]` or `[ai-mutants]` warning on these files.
2. Voice: `VOICE_BASE=app/content/courses/sequence python3 docs/reviews/voice-scan.py 35`: 0 sentences over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `node tools/run-number-scripts.mjs --python <venv> --only sequence-L1`: passed (395 checks, strict coverage, 57 literals each with a reason, 27 s).
4. Playthrough with `--local-cdn`, desktop and `--mobile`: all 4 lessons, `review-1`, `homework-1` (performance starter fails, longform marked by the button) and `problems-1` passed; l2 and `problems-1` replayed after their last edit, both modes.

Also: `grade-all.mjs --code --file` on all seven files, 0 failures (9 Python widgets, 30 mutants each failing its named test first); `same-course-reuse.mjs --all` lists nothing for the course.

## Numbers and their sources (both routes in the script)

- l1: the hook frames are `simulate_ar1(w, 60, 7)` for $w = 0, 0.1, \dots, 1$ (route B: the closed form $\sum 0.6^{t-k}\varepsilon_k$). Three steps $1, -1.5, -0.25$. Least squares on $1, 0.5, 0.4$: $0.7/1.25 = 0.56$ (against `lstsq`). Seed 5, 500 days: $\hat\phi = 0.6315$ through the origin and 0.6315 with an intercept (arma l7's figure); 200 steps of 0.1 land within $10^{-6}$. Readout $2\tanh(0.6) = 1.0741$. 305 weights for 16 units. EWMA $\sqrt{0.000118} = 0.010863$.
- l2: forward $2, 2, 1, -0.5$; $\partial h_4/\partial w = 2.75$ (sum of terms against central differences); $0.5^4 = 0.0625$; losses 1.274330 and 1.266296 at $w = 0.69, 0.71$, central difference $-0.4017$ against the autograd's $-0.401705$; 510 bars, 17 windows.
- l3: $0.9^{50} = 0.0052$, $1.1^{50} = 117.39$; the broker matrix settles at $\tfrac23\sqrt2 = 0.9428$ (eigen-split against 400 multiplications); $\mathbf B$'s eigenvalue 1.2162; $0.72^{20} = 0.0014$; $\rho = 4.0766$ for `default_rng(2)` 16 by 16, scale 0.233; $\mathbf N^2 = \mathbf 0$; $1.05^{50} = 11.47$; the non-normal matrix peaks at $k = 6$ (10.66; loop against the closed form); $0.95^{60} = 0.0461$.
- l4: hook runs (step 0.003, clip 5) recomputed by a forward-derivative loop and by the closed form of $h_T$; the unclipped run passes 10,000 within 12 steps and overflows within two more (stated as a threshold only); clip factors 0.2 and 0.5; turn 17.1 degrees (arctangents against the angle between vectors); gate 0.67; $0.98^{50} = 0.3642$. Copy task: both units retrained in the script with the autograd on seeds 0 to 2 (300 steps, batch 64, step 0.5, clip 1, noise sd 0.2), gradients checked by central differences, accuracies recomputed by a plain NumPy forward pass. Plain: T 5 (1.0, 1.0, 0.519), T 10 (0.519, 0.481, 0.519), T 20 (0.519 three times), T 40 (0.481, 0.519, 0.519). Gated: 1.0 on every seed to T 20, T 40 (1.0, 1.0, 0.835). So the plain unit fails from $T = 10$ (the brief guessed 10 to 20); the lesson states the measured figure.
- Review, problems, homework: each answer and every numeric slip recomputed (eigenvalues 1.1 and 0.4; $1.1^{20} = 6.7275$; clip factor 0.2973; $0.95^{30} = 0.2146$; 90 steps to 1%; $0.99^{90} = 0.4047$, about five times further; half-life 22.8 days; $\sqrt{20} = 4.4721$; $\rho = 0.7810$, 19 steps). The homework's `rnn_bptt` equals the autograd on four planted nets to $10^{-10}$. Every slip's `why` was read against its value (the script lists 54 lines to check by hand; all read; one slip with no matching why, `diff` in problems item 1, was removed).

## Timing of graded cases (Pyodide, desktop, one worker; `tools/code-runner.mjs`)

Slowest case per widget: l1 `fit_w` 66 ms, `rnn_*` 13 ms; l2 `bptt_grad` 45 ms, `truncated_bptt` 23 ms; l3 12 ms; l4 `clip/gate` 17 ms, `train_gated_copy` 939 ms (150 steps at $T = 10$, widget `budget` 6,000 ms, limit 11 s, 11.7x); homework `linear_bptt` 10 ms, `rnn_bptt` 23 ms. Every case is under a third of its limit.

## Conventions

Seeds: `default_rng(seed)` throughout; AR(1) paths are arma l2's `simulate_ar1` (seed 7 for the hook, 5 for the fit). Copy task: `copy_batch(T, n, rng, noise=0.2)` with a start-flag channel, `init_gated(seed)` draws $0.5 \cdot N(0, 1)$ in the order w, ux, uf, b, ax, af, ah, c, v, d, then sets $w = 0.9$ and the gate bias $c = -3$; training batches from `default_rng(1000 + seed)`, test set `default_rng(99)` of 1,000. Learning-loop widgets carry exact short-run tests (`fit_w` after 1 to 5 steps; `train_gated_copy` losses after 1 to 6 steps, one with a cap of 0.05 that binds, since a cap of 1 never binds early).

## course.json

No change proposed.

## Backlog

Two bullets under "Raised later (sequence level 1)" in `docs/BACKLOG-INBOX.md`.
