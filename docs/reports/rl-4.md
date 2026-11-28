# rl level 4 (Policy gradients): report

## Files written

All in `app/content/courses/rl/`, skill `rl-pg`, ids, names and objectives as in `course.json`. Shared code: `app/content/data/ai/rl_ops_l4.py` (new, v1.0, frozen from now; contract below). `autograd.py` (v1.0, SHA-256 `5917d4ec91f7`) and `rl_ops_l3.py` (SHA-256 `eba4d2b39835`) are unchanged.

| File | Screens / items | Quiz | Code | Shape |
|---|---|---|---|---|
| `l13-a-policy-with-dials.json` | 10 | 3 | `softmax`, `corridor_value`, `best_p` | problem hook (corridor `graph`: always-right loops), explore (drag on $J(p)$, `plane`), problem ($J(0.5) = -12$), ladder ×3 (dial gap $\ln\sqrt2$, epsilon-greedy $J(0.95)$, code), trap (deterministic is best only with full state information), ladder edge (equal dials are uniform), generalise, transfer (randomised execution time, £300) |
| `l14-reinforce.json` | 10 | 3 | `grad_log_softmax`, `reinforce_bandit`, `reinforce_corridor` | problem hook ($\partial J/\partial\theta_A = -0.25$), explore (bars with a $\pi_A$ slider), problem (score), derive (`order`, log-derivative trick, one distractor), ladder ×3 (variance 27.5625, reward-to-go, code), trap (differentiating the reward), generalise (edge: zero return), transfer (P&L estimate £84) |
| `l15-baselines.json` | 10 | 3 | `score_estimates`, `variance_of_estimate`, `reinforce_with_baseline` | problem hook ($b = 10$), explore (baseline slider, live variance), problem ($E[\text{score}] = 0$), ladder ×4 (0.0625, $b^* = 10.2$, advantage and actor-critic, code), trap (action-dependent baseline), generalise (edge: equal returns), transfer (control variate, 76) |
| `l16-a-policy-network.json` | 10 | 3 | `policy_loss`, `train_policy` (+ ungraded `trainer`) | problem hook (schedule 2, 2, 0, 0, 0 = £31), explore (`trainer`, 200 batches), problem (DP optimum £33), ladder ×5 (loss by hand, code, normalising, KL leash; trap on reward scale between), generalise, transfer (DP where the model is known) |
| `review-4.json` | 10 items, difficulty 2 to 4, `pass` 0.8 | | | every lesson |
| `homework-4.json` | 6 items, difficulty 3 to 5 | | 2 | performance `code` `train_corridor` (5), `best_baseline` code (4), `order` unbiasedness with a distractor (4), numeric (3), multi (4), longform (5, 10-point rubric) |
| `problems-4.json` | 3 problems, 12 parts, difficulty 3, 4, 5 | | | router scores, estimate, gradient, variance; best baseline and the variance left; corridor advantage to a policy step |

Performance task: `docs/reports/rl-4-perf.md`.

## Gates

1. Validator: 0 errors; no `[ai-mutants]` warning on rl files. My files carry advisory warnings only (`O2-long-sentence`, point hints, ladder canvas kind).
2. Voice: `VOICE_BASE=app/content/courses/rl python3 docs/reviews/voice-scan.py 35`: over 35 words 0, lesson ids in code spans 0.
3. Numbers: `docs/reports/rl-L4-numbers.py` with the venv: 253 of 253, exit 0 (about 20 s).
4. `grade-all.mjs --code --local-cdn <pkgs>` on all seven files: 6 Python widgets, 0 failures; 19 mutants, each failing its named test first (one, the reversed reward-to-go in l14, by timing out: marked `timeout`).
5. Playthrough with `--local-cdn .../scratchpad/aitiming/pkgs`, desktop and `--mobile`: all four lessons, `review-4`, `homework-4` (performance starter fails), `--problems rl/problems-4`: all passed; files edited after a green run were replayed in both modes. Run after merging `caf31d32` (engine 1266). Screens read at 440 px; fix made: the $J(p)$ plane now keeps its x axis at the bottom.
6. `fresh-check --file` on review, homework and problems: 0 hits (one review stem reworded after a hit against the l14 quiz).

## Numbers and their sources

Every stated number is checked at its path by the script. Two routes each:

| Number | Where | Check |
|---|---|---|
| $J(p) = (2p - 4)/(p(1 - p))$; $-12$, $-11.657$ at $2 - \sqrt2 = 0.5858$, $-82.11$, $-44.21$, $-18.67$, $-12.38$, $-11.67$ | l13, review, problems | 3 by 3 linear solve and closed form; best $p$ by grid search; mean walk length simulated |
| Dial gap $\ln\sqrt2 = 0.3466$ | l13 | odds $(2-\sqrt2)/(\sqrt2-1) = \sqrt2$ |
| $-0.25$, estimates 5 and $-5.5$, variance 27.5625 | l14 | formula and central differences; enumeration and the two-point formula |
| Variances 0.0625 ($b = 10$ and 11), 0 ($b = 10.5$); $b^*$ 10.2, 10.5, 6, 3, 11 | l15, review, problems | enumeration and $(10.5 - b)^2/4$; formula and a grid search over $b$ |
| 76, KL 0.0201 (reverse 0.0204), loss 0.3466, 2.7726, $-0.6931$, normalised 1.3887 | l15, l16 | direct, two forms each |
| Optimum £33 for 1, 1, 1, 1, 0; 31, 32.5, 10 | l16 | backward induction (`rl_ops_l4.exec_dp`) and all 243 schedules |
| Seeded runs: plain REINFORCE on the venues (lr 0.01, 2,000 pulls) mean final $p_B$ over seeds 0 to 9 above 0.85 (test line 0.8; seeds 0 to 19 min 0.534); corridor (lr 0.001, 1,000 episodes) mean $p$ inside 0.55 to 0.62 (test 0.53 to 0.64); baselined venues seeds 0 to 4 $p_B > 0.97$, ratio $< 0.15$ (tests 0.95, 0.25); homework ratio 0.173 to 0.3225 on seeds 0 to 19 (test 0.5) | l14, l15, homework | re-implemented with a dial difference instead of two dials, same random draws |
| Network: untrained seed 0 £28.21; 960 episodes give £32.885 to £32.979 on seeds 0 to 9 (test £32.5 on seeds 0 to 2); rewards ×100 at lr 0.5 collapse to £31.00 on seeds 1, 7 and 9; normalised pence and pounds runs agree within $10^{-6}$ | l16 | own loss from a one-hot mask (not indexing), same batches; `grad_check` below $10^{-6}$ on the softmax policy gradient |

Every result from a seeded run is stated as that seed's (or those seeds') result.

## Deviations and notes

- The two-venue bandit pays a fixed £10 and £11, as in the brief; I call the arms venues.
- l16 uses the toy execution task (sell 4 lots in 5 steps, proceeds $k(10 - k)$, £0.50 a lot held, £5 a lot dumped at the end). It learns within the budget: 960 episodes cost 0.05 s in CPython; the graded run trains three seeds with a 10 s budget. The longer curve is the ungraded `trainer` (200 batches).
- The policy loss needs per-row weights, which `cross_entropy` does not take, so `rl_ops_l4.log_softmax` composes a differentiable log-softmax from `exp`, `sum` and `log`, with the row maximum as a constant.
- KL appears once (l16 screen 8) as "a leash", with $\mathrm{KL}(\pi \| \pi_{\text{ref}})$ in the direction RLHF uses; the entropy bonus is one sentence in the trap's explanation.

## course.json

No change proposed.

## rl_ops_l4.py as shipped

`app/content/data/ai/rl_ops_l4.py`, `__version__ = "1.0"`, imports `math`, NumPy and `autograd.Tensor`; shipped with `autograd.py` through a widget's `data` map (`{"autograd.py": "content/data/ai/autograd.py", "rl_ops_l4.py": "content/data/ai/rl_ops_l4.py"}`), as l16's code and trainer screens do.

- Corridor: `GOAL = 3`; `corridor_move(s, right) -> int` (states 0 S, 1 B with moves swapped, 2 C); `corridor_value(p) -> float` (closed form); `corridor_episode(p, rng, max_steps=100000) -> list` of 1 (right) and 0, one `rng.random()` a move.
- Softmax: `softmax(theta) -> list` (max subtracted); `grad_log_softmax(theta, a) -> list` ($[b = a] - \pi_b$); `sample(pi, rng) -> int` (one `rng.random()`).
- Execution task: `LOTS, STEPS, HOLD, DUMP = 4, 5, 0.5, 5.0`; `ACTIONS = (0, 1, 2)`; `proceeds(k)`; `exec_step(lots, steps, k) -> (lots, steps, reward, done)`; `exec_dp() -> (33.0, [1, 1, 1, 1, 0])`; `features(lots, steps) -> ndarray (3,)`; `policy_value(probs) -> float` (exact expected proceeds of `probs(lots, steps)`).
- Network: `log_softmax(z: Tensor) -> Tensor`; `init_policy(seed, hidden=8) -> [W1, b1, W2, b2]` (`default_rng(seed)`, sd 0.5); `policy_logits(params, X) -> Tensor`; `policy_probs(params, X) -> ndarray`; `run_batch(params, batch, rng) -> (X, A, G, totals)` with `rng` a NumPy generator, rows episode by episode; `network_value(params) -> float`.

Checked in the number script: `log_softmax` through the network passes `grad_check` below $10^{-6}$; `grad_log_softmax` matches central differences; `exec_dp` matches enumeration; `corridor_value` matches the linear solve.
