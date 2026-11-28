# rl level 3 (TD and Q-learning): report

## Files written

All in `app/content/courses/rl/`, skill `rl-td`, ids, names and objectives as in `course.json`.

| File | Screens / items | Quiz | Code screens | Shape |
|---|---|---|---|---|
| `l9-learning-from-episodes.json` | 10 | 3 | 1 (`returns_from_episode`, `mc_evaluate`, `random_walk_episode`) | problem hook (three corridor episodes, first-visit average 4), explore (frames: 10 random-walk episodes; edge: A has no estimate after 3), problem (true values $k/6$), ladder ×4 (backward returns, code, standard error of 100 episodes, exploring starts), trap (rewards against returns), generalise, transfer (replayed history) |
| `l10-one-step-ahead.json` | 9 | 3 | 1 (`td0_update`, `td0_random_walk`) | problem hook (one TD step), explore (recorded RMS curves TD and MC, reveal slider), problem (TD error), ladder ×2 (target variance, code), trap ("biased, so worse"), ladder (edge: $\alpha = 0.5$ stalls), generalise, transfer (fair value trade by trade) |
| `l11-q-learning.json` | 11 | 3 | 1 (`q_update`, `q_learning`, `greedy_matches`) | problem hook, explore (frames at 0, 50, 200, 500 episodes), problem (Q update), ladder ×2 (Q-table as a `matrix` heat, edge: untouched cells with a fixed start), ladder (code, the exit check), trap (tied arg-max), ladder ×2 (zero starts are optimistic; why not the slippery grid), generalise, transfer |
| `l12-safe-or-greedy.json` | 9 | 3 | 1 (`sarsa_update`, `cliff_run`) | problem hook (4 by 8 cliff, two routes), explore (recorded reward curves), problem (SARSA update), ladder ×2 (chance of a fall, code), trap, ladder (edge: $\varepsilon = 0$, both −9), generalise, transfer |
| `review-3.json` | 10 items, difficulty 2 to 4, `pass` 0.8 | | | every lesson |
| `homework-3.json` | 6 items, difficulty 3 to 5 | | 2 | performance `code` task `learn_gridworld` (5), `td0_decaying` code (4), `order` TD target from the Bellman equation with one distractor (4), numeric (3), multi (4), longform (5, 10-point rubric) |
| `problems-3.json` | 3 problems, 10 parts, difficulty 5, 4, 3 | | | hand Q-updates along two episodes; SARSA against Q-learning targets; MC against TD on replayed days |

The strand exit (Q-learning whose greedy policy equals value iteration's on the gridworld) is l11's code screen and the homework performance task.

## Gates

1. Validator: 0 errors; my files carry only advisory warnings (`O2-long-sentence`, "ladder usually reuses the previous canvas kind").
2. Voice: `VOICE_BASE=app/content/courses/rl python3 docs/reviews/voice-scan.py 35`: over 35 words 0, lesson ids in code spans 0.
3. Numbers: `docs/reports/rl-L3-numbers.py` with the venv: 207 of 207 checks, exit 0 (about 15 s; it reruns the slippery 20,000-episode check).
4. Playthrough `--local-cdn .../scratchpad/aitiming/pkgs`, desktop and `--mobile`: all four lessons, `review-3`, `homework-3` (performance starter fails), `problems-3`: all passed; files edited after a green run were replayed in both modes. Screenshots in the scratchpad `rl-3/shots*`, read.
5. `grade-all.mjs` on the seven files: 0 failures; `fresh-check --file` on review, homework and problems: 0 hits.

## Numbers and their sources

The number script re-implements every learner as an online loop (update right after each step), different code from the lesson solutions, and reproduces the stated figures and recorded curves; each code widget's solution is run against its tests with its starter failing.

| Number | Where | Check |
|---|---|---|
| Random walk true values $\tfrac16, \dots, \tfrac56$ | l9, l10 | linear solve and closed form |
| Corridor estimates 4, 3, 9; $G_0 = 3.851$; SE 0.05 | l9 | fractions, direct |
| Seed 7: A unvisited after 3 episodes | l9 | replayed |
| RMS after 25 episodes: TD 0.1 0.0581, TD 0.05 0.1098, MC 0.02 0.1588, MC 0.01 0.2138; after 100: TD 0.0553, MC 0.0867; $\alpha = 0.5$: 0.1382 at 10, 0.1528 at 100 (100 seeds) | l10 | online re-implementation |
| Target variance $(\tfrac16)^2 = 0.0278$; mean RMS 0.0625 over seeds 0 to 19 | l10 | direct; replayed |
| Q-learning, deterministic grid, $\alpha = 0.1$, $\varepsilon = 0.2$: optimal for 50 of 50 seeds after 200 and 500 episodes; 2,934 steps a run on average; seed 0 after 50 episodes wrong in 3 cells; max $Q$ at the start after 2,000 episodes 0.3228 | l11, homework | second implementation |
| Fixed start: 10 cells untouched after one episode, all touched after 4 | l11 | replayed |
| Slippery grid ($\alpha = 0.1$, $\varepsilon = 0.1$): 2 of 10 seeds fail within 20,000 episodes, the rest need 4,400 to 15,250; action gaps 0.0073 (r4c3) and 0.0077 (r2c1) | l11, homework | rerun in the script |
| Cliff 4 by 8, $\alpha = 0.5$, $\varepsilon = 0.1$, last 100 of 500 episodes over seeds 0 to 19: SARSA −20.03, Q-learning −31.34, SARSA ahead on every seed; greedy routes 13 and 9 moves; $\varepsilon = 0$: both −9 | l12 | second implementation |
| $1 - 0.975^6 = 0.1409$; transfer £0.60 | l12 | direct |
| Decaying-step TD mean RMS 0.0305 after 1,000 episodes (seeds 0 to 9) | homework | second implementation |

## Deviations and notes

- l10 compares TD with constant-step Monte Carlo (as in Sutton and Barto's Example 6.2), while l9 teaches sample-average first-visit MC; the explore screen says so.
- The exit runs on the deterministic grid, as the brief says; l11 gives the slippery failure and its reason (noisy targets, constant step, gaps under 0.01, the step-size conditions).
- `td0_update` returns the TD error and updates `V[s]` in place. `cliff_run(agent, episodes, seed, alpha=0.5, eps=0.1)` returns the mean reward of the last 100 episodes; its ordering test runs 10 cliff runs and carries a `budget` of 8,000 ms (0.2 s in CPython).
- The homework's TD helper is named `walk_once` so the freshness check does not read it as the l9 task reused.

## course.json

No change proposed.

## rl_ops_l3.py as shipped

`app/content/data/ai/rl_ops_l3.py`, for `ai-safety` L1 (naming rule: `docs/briefs/ai-strand-interfaces.md`). Pure Python, imports only `random`. Shipped through the `data` map of the l11 code widget (`"data": { "rl_ops_l3.py": "content/data/ai/rl_ops_l3.py" }`, `dataPeek: false`, so the learner does not see the model solution), where hidden test 10 imports it and checks it equals the learner's `q_learning`. A widget in `ai-safety` ships it the same way and uses `import rl_ops_l3 as ops`. `docs/reports/rl-L3-numbers.py` checks, bit for bit against its own independent agent, the figures below.

Constants: `ROWS, COLS = 4, 5`; `WALL = {'r2c3'}`; `TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}`; `STEP = -0.04`; `MOVES`, `SIDES`; `ACTIONS = 'URDL'`; `CELLS` (19 names `'r<row>c<col>'`); `OPEN` (the 17 non-end cells).

- `move(s, a) -> str`: the cell reached from `s` by `a`; the edge and the wall leave the agent at `s`.
- `reward(t) -> float`: `TERMINAL.get(t, 0.0) + STEP` for entering `t`.
- `transition(s, a, slip=0.0) -> dict`: `{next cell: chance}`, the intended move with `1 - 2*slip` and each side move with `slip`.
- `sample_next(s, a, slip, rng) -> str`: one draw of the next cell; with `slip` 0 it is `move(s, a)` and uses no random number, otherwise it uses one `rng.random()`.
- `q_update(Q, s, a, r, s2, alpha, gamma, terminal, actions=ACTIONS) -> float`: updates `Q[(s, a)]` in place and returns it; the target is `r` when `terminal` is true, else `r + gamma * max Q(s2, .)`.
- `greedy_action(Q, s, actions=ACTIONS) -> str`: the first best action in the order of `actions` (U, R, D, L).
- `greedy_policy(Q, cells=OPEN, actions=ACTIONS) -> dict`: `{cell: first best action}`.
- `class Gridworld(slip=0.0)`: members `actions` (`'URDL'`), `starts` (`OPEN`), `slip`, `is_end(s) -> bool`, `step(s, a, rng) -> (next cell, reward, done)`. Any other grid can reuse `run_episode` with an object that has these four members (`actions`, `starts`, `is_end`, `step`).
- `run_episode(env, Q, start, alpha, gamma, eps, rng, max_steps=None, learn=True) -> (steps, total reward, reached)`: epsilon-greedy from `start`; per step it draws `rng.random()` for the exploring test, `rng.choice(env.actions)` if exploring, then the slip draw inside `env.step`; it updates `Q` after each step when `learn` is true; it stops at an end cell or after `max_steps` steps (`reached` is False if the cap ended it, so a looping agent still stops); the total reward is undiscounted, step costs included.
- `q_learning(episodes, alpha, eps, seed, gamma=0.9, slip=0.0, max_steps=None) -> dict`: Q from all zeros, each episode starting at `rng.choice(OPEN)`; with `slip=0` and no cap it is rl l11's `q_learning` exactly.

Checked against the course's numbers: `q_learning(500, 0.1, 0.2, s)` equals the independent agent's Q for seeds 0 to 49; 2,934.46 steps an agent over 500 episodes; 0.3228 at the start after 2,000 episodes (seed 0); `slip=0.1` equals the agent for seeds 0 to 4; seed 7 first matches value iteration at episode 4,400 and seed 0 at 7,600 (the lesson's range is 4,400 to 15,250); `q_update` gives 0.096 at an end cell and 0.221 for the l11 hand example; `max_steps=25` ends a looping greedy agent after 25 steps. It carries no ai-safety grid: that world is 5 by 5 with (row, col) from 0, so ai-safety supplies its own `env` (the four members above) and its own step cap.
