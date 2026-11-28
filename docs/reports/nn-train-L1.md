# nn-train level 1 (Optimisers): report

Branch `ai-w4-nn-train` from `f9616b05`. Skill `nt-optim` on every lesson and item.

## Files written

| File | Screens or items | Notes |
|---|---|---|
| `l1-noisy-steps.json` | 10 screens, 4 quiz | histogram hook (bars `dataSets`, predict first), $\sigma/\sqrt B$, a hand step, full batch against batch 32 per epoch, the noise band (series frames), the step sweep, trap on small batches, linear scaling, code, transfer |
| `l2-momentum.json` | 10 screens, 3 quiz | bowl hook with a live heavy-ball path (derive with `matpow`), settled step $1/(1-\beta)$, two hand steps, best heavy ball, momentum on the net, trap $\beta = 0.99$, derivation (`order`), code, transfer |
| `l3-adam.json` | 11 screens, 3 quiz | loss times 1,000 hook, first step, three hand steps, correction factors, Adam against momentum by seed, trap "no tuning", per-coordinate step, two code screens, transfer |
| `l4-schedules.json` | 10 screens, 3 quiz | least-squares hook with the last 50 steps hidden, cosine formula, rates by hand (`table` widget), why decay helps, why warm up, unclamped cosine, trap "judged halfway", two code screens, transfer |
| `review-1.json` | 10 items, `pass` 0.8 | every lesson, difficulty 2 to 4 |
| `homework-1.json` | 6 items | performance task `h1-optimizer` (code, difficulty 5), `h1-sweep` (code), `h1-bias-order` (order), two numeric/choice, `h1-diagnose` (longform, 10-point rubric) |
| `problems-1.json` | 3 problems, 13 parts | difficulty 5, 4, 3; every lesson used |
| `app/content/data/ai/nt_ops_l1.py` | module | public names at the end of this report |
| `docs/reports/nn-train-L1-numbers.py`, `docs/reports/nn-train-1-perf.md` | | |

## Gates

1. Validator: `node tools/validate.mjs` 0 errors. Warnings on the level's files: point hints without a highlight on canvas-free screens, problem screens without a canvas, two ladder canvas-kind changes, `O2-long-sentence` advisories.
2. Voice: `VOICE_BASE=app/content/courses/nn-train python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `ZQ_NUMBERS_STRICT=1 <venv>/bin/python docs/reports/nn-train-L1-numbers.py`: 300 of 300 checks, coverage 0 uncovered (20 literals, each with its reason), exit 0, about 6 s. It checks every byKey line that states another number by hand (49, all consistent).
4. Code widgets: `grade-all.mjs --code` on all seven files: 8 Python widgets, 0 failures in Pyodide. Mutants: 37, each failing its named test first, in CPython (number script) and Pyodide.
5. Playthrough with `--local-cdn <pkgs> --mobile` (desktop and 440 px): the four lessons, review-1, homework-1 ("1 performance starter fail", longform marked by the button) and problems-1 all passed. Screens read at 1280 and 440.

## Decisions a reader should know

- **One turn, not 1.5.** The brief's two-arm spiral is one turn per arm (`t = sqrt(u) 2pi`, noise 0.05, `default_rng(0)`). At 1.5 turns the 2-16-16-2 net sat on a plateau near 0.6 nats for the first 300 steps, so every short comparison was flat.
- **Course rates come from steady sweeps.** SGD 0.5, momentum 0.3 with $\beta = 0.9$, Adam 0.1, each the lowest mean of its 300-step sweep among runs that are steady. Above that the runs are chaotic: SGD at 2 ended at 0.026 on seed 1 in the module and at 0.018 in the number script's hand-written network, a float-rounding difference amplified fifty-fold; at 4 most seeds blow up, but not the same ones in both routes. l1's sweep screen teaches this ("near the edge of stability, results turn to luck") and draws only the steady rates. Every graded training case uses rates whose two routes agree to $10^{-8}$ or better over 300 steps.
- **Momentum on the net.** With the rate matched, momentum at 0.02 ($\beta = 0.9$) ends beside SGD at 0.2 (0.221 against 0.214): on this net momentum is mostly a tenfold step. Its gain is the steady larger step (0.3, a tenfold step of 3, trains on every seed) and the long valley of the bowl, which l2 teaches with the closed forms.
- **Order test.** With the course rates, momentum and Adam end below SGD on all five seeds and Adam is lowest on four of five (momentum on seed 1); l3 says so, and its `train_spiral` widget tests the order on seed 2 plus a threshold and three exact 5-step runs.
- **Schedules.** On the spiral net at 300 steps the constant Adam rate often ends lower than the decays (the net is still learning), so the schedule hook uses l1's least-squares problem, where both decays end about ten times lower on all ten seeds. Warm-up made no reliable difference on the spiral net over five seeds; l4 says so and teaches warm-up as a guard for a large first rate.
- **Batches** in every training loop are 32 distinct rows by `rng.choice(400, 32, replace=False)` from one `default_rng(seed)`; the per-epoch screens use `minibatch_indices` (a permutation cut into batches, 13 an epoch at 32).

## Numbers and their sources (all recomputed by the number script, route B)

- Hook: $\sigma = 0.0409$ (row gradients of the first weight at the start), full gradient $-0.0019$; 200 draws with replacement, `default_rng(5)`: sd 0.0140 at batch 8, 0.0037 at 128; prediction $\sigma/\sqrt{128} = 0.0036$.
- Hand step: gradient $-3$, new $w = 1.3$. Per epoch at $\eta = 0.5$: 13 steps an epoch, 260 steps in 20 epochs; full batch 0.438, batch 32 0.142, batch 8 0.083, batch 128 0.380 after 20 epochs.
- Band (least squares, 1,000 rows, `default_rng(7)`, batch 8, `default_rng(11)`): minimum 0.1218; mean excess over steps 101 to 300: 0.0012, 0.0022, 0.0045, 0.0111 at steps 0.05, 0.1, 0.2, 0.4.
- Sweep (300 steps, seeds 1 to 5): 0.383, 0.166, 0.141, 0.234, 0.279 at 0.1, 0.3, 0.5, 1, 1.5.
- Bowl: 0.1816 after 20 plain steps at $2/11$; best $\beta$ on the slider 0.40 (0.00025); two hand steps (9, 0), (7.6, $-0.5$); $\beta^* = 0.270$, $s^* = 0.231$, rate 0.519; $0.519^{20} \approx 2.0 \times 10^{-6}$, $0.818^{20} \approx 0.018$, measured $2.3 \times 10^{-5}$; $\beta = 0.99$ gives 7.62 after 20 steps and 4.72 after 100; $\kappa = 19$ needs 15 heavy-ball steps against 66.
- Adam: first step $\eta$; three hand steps 0.9, 0.8004, 0.7016; factors 3.16, 6.53, 3.24, 1.26 at steps 1, 10, 100, 1,000; scaled hook: SGD at 55.9 nats after one step, Adam 0.1989 at step 50 either way; Adam sweep 0.226, 0.072, 0.025, 0.019 at 0.003 to 0.1; at 0.5 every seed above 0.2 in both routes.
- Schedules: cosine rate 0.1707 at step 75; table 0.025, 0.05, 0.0146; final excess over ten seeds 0.0058 constant, 0.00056 step, 0.00051 cosine; unclamped 0.1 at step 450; retrain rate 0.0015 at step 1,050.
- Problems and review: every key and slip recomputed at its path (see the script).

## Training cases and their desktop time (Pyodide 0.27.7 under node, local copy)

300 minibatch steps of the course net take 130 to 170 ms (0.5 ms a step). l3 code B: tests 4 to 6 run five 300-step runs in all, under 1 s together, widget `budget` 4000 ms (limit 9 s per case). l4 code B: one 300-step run, 0.17 s, `budget` 4000. homework `h1-sweep`: 1,000 steps of a 3-weight model, under 50 ms. Every exact training test is a 3 to 6 step run compared to $10^{-7}$ relative.

## Ops added

No `nt_ops` ops with a backward in this level. `nt_ops_l1.py` (version 1.0, 4,898 bytes, SHA-256 `9c1391a33624604bf8547607a51ef08c39a9bee2eeef22947aa5126dbc4ff234`) holds the course data, net and optimisers. It imports `autograd` (v1.0) and NumPy, has no side effects, and every function returns new arrays.

## Proposed course.json change

None.

## nt_ops_l1.py public names as shipped

`from nt_ops_l1 import ...`
- `spirals(n=400, seed=0, noise=0.05) -> (X (n, 2), y (n,))`: two arms of one turn, labels 0 and 1, rows shuffled by the same generator.
- `init_net(sizes=(2, 16, 16, 2), seed=0) -> [W1, b1, W2, b2, ...]`: `W` of shape `(fan_in, fan_out)` drawn $N(0, 1/\text{fan\_in})$, biases 0.
- `forward(params, X) -> Tensor`: logits; `X @ W + b`, tanh on every hidden layer; `params` arrays or `Tensor`s.
- `loss_and_grads(params, X, y, scale=1.0) -> (float, [ndarray])`: mean cross-entropy in nats times `scale`, and its gradient per parameter.
- `full_loss(params, X, y) -> float`.
- `minibatch_indices(n, B, seed) -> [ndarray]`: one epoch, `default_rng(seed).permutation(n)` cut into slices of `B`.
- `sgd_step(params, grads, lr) -> list`.
- `momentum_step(params, vels, grads, lr, beta) -> (params, vels)`: heavy ball, $v \leftarrow \beta v - \eta g$, $p \leftarrow p + v$.
- `adam_step(params, grads, m, v, t, lr, b1=0.9, b2=0.999, eps=1e-8) -> (params, m, v)`: `t` from 1, bias-corrected, `eps` outside the root.
- `warmup_cosine(t, lr_max, warmup, total) -> float`: `t` clamped to `[0, total]`; `lr_max * t / warmup` during warm-up, then half a cosine to 0 at `total`.
