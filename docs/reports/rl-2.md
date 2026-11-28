# rl level 2 (MDPs and value iteration): report

## Files written

All in `app/content/courses/rl/`, skill `rl-mdp`, ids, names and objectives as in `course.json`.

| File | Screens / items | Quiz | Code screens | Shape |
|---|---|---|---|---|
| `l5-states-and-rewards.json` | 11 | 3 | 1 (`discounted_return`, `transition`, `dice_value`) | problem hook (unlimited dice game, $55/12$), explore (value of each threshold rule against $\gamma$), problem (names the MDP), ladder ×5 (slip transitions on the grid, a path's return, the discount as interest, trap, code), problem (edge: £1 for ever, $\gamma = 1$ diverges), generalise (Markov property), transfer (execution state) |
| `l6-what-a-policy-is-worth.json` | 10 | 3 | 1 (`policy_matrix`, `evaluate_policy`) | problem hook (two-state Calm/Busy solve), explore ($\gamma$ slider on the graph), problem (Bellman equation checked at r1c4), ladder ×3 (up-then-right path, edge: wall-walker −0.4, sweeps by the contraction bound), trap (where $\gamma$ goes), ladder (code), generalise, transfer (quoting rule) |
| `l7-value-iteration.json` | 11 | 3 | 1 (`value_iteration`, `greedy_policy`) | problem hook (one backup), explore (frames: values spreading sweep by sweep), problem (slippery backup), ladder ×3 (why r3c5 goes L, largest change per sweep on a log axis, dice game as one-state VI), trap (in-place updates), ladder (code), ladder (edge: tied actions, multi), generalise, transfer (American put node) |
| `l8-improving-a-policy.json` | 9 | 3 | 1 (`policy_iteration`, `same_policy`) | problem hook (improving "always U" at the start), explore (frames: 4 policies), problem (improvement theorem), ladder (GPI), trap (tied arg-max), ladder (code), ladder (edge: slip 0.2 flips r2c4 to L), generalise, transfer (skewing quotes) |
| `review-2.json` | 10 items, difficulty 2 to 4, `pass` 0.8 | | | every lesson |
| `homework-2.json` | 6 items, difficulty 3 to 5 | | 2 | performance `code` task `solve_mdp` (5), `vi_with_bound` code (4), `order` contraction proof with one distractor (4), numeric (3), multi (4), longform (5, 10-point rubric) |
| `problems-2.json` | 3 problems, 10 parts, difficulty 5, 4, 3 | | | hold or push (solve, one-step score, improve, solve again); a grid backup chain; the impatient dice game |

The gridworld uses the brief's definition. Grids draw values as cell text and policies with `state.arrows` (engine 1229).

## Gates

1. Validator: 0 errors; my files carry only advisory warnings (`O2-long-sentence`, "ladder usually reuses the previous canvas kind", one point hint without a highlight).
2. Voice: `VOICE_BASE=app/content/courses/rl python3 docs/reviews/voice-scan.py 35`: over 35 words 0, lesson ids in code spans 0.
3. Numbers: `docs/reports/rl-L2-numbers.py` with the venv: all checks pass, exit 0.
4. Playthrough `--local-cdn .../scratchpad/aitiming/pkgs`, desktop and `--mobile`: all four lessons, `review-2`, `homework-2` (performance starter fails) and `problems-2`: all passed; files edited after a green run were replayed in both modes. Screenshots in the scratchpad `rl-2/shots*`, read; the contraction chart's labels were moved after the first look.
5. `grade-all.mjs` on the seven files: 0 failures; `fresh-check --file` on review, homework and problems: 0 hits.

## Numbers and their sources

The number script rebuilds the grid as arrays and gets every optimal value twice (value iteration, and policy iteration's linear solves), the deterministic values a third way (the closed form $V(d)$ over breadth-first distances). Two-state systems by Cramer's rule and `np.linalg.solve`.

| Number | Where | Check |
|---|---|---|
| 4.5833 = 55/12, threshold values 3.50, 3.92, 4.29, 4.55, 4.58, 4.00, 4.125 | l5 | fixed point, first-step equation, fractions |
| 17 decision states; 0.7016, 0.824, 0.3487, 10 | l5 | direct |
| 15.625, 18.75, 14.0625; 165.56, 168.87, 1.67 at $\gamma = 0.99$ | l6 | Cramer and solve |
| Slippery table (the brief's 17 values), 0.1944; deterministic 0.96 to 0.3228 | l6 to l8 | VI, PI and closed form agree to $10^{-9}$ |
| 0.8896 Bellman check; −0.4 wall loop; 132 sweeps; quoting rule £61.31 / £57.38 | l6 | direct and solve |
| Sweeps 8, 25, 38; first positive start value on sweep 7; −0.7896 for U at r3c5; Gauss-Seidel 17 sweeps; dice sweeps 4.075, 4.334, 4.450, 4.503 | l7 | number script |
| Deterministic largest change exactly $0.96 \times 0.9^{k-1}$ to sweep 7, then 0; slippery changes fall about 0.47 a sweep at the end | l7 | number script |
| Policy iteration from "always U": 4 evaluations (slippery), 5 (deterministic, with the keep-on-tie rule); start values −0.3686, 0.0845, 0.1943, 0.1944; changes 13, 5, 1; R at the start scores −0.3573 | l8 | number script |
| 7 cells where PI's and VI's arg-max differ, values equal to $10^{-15}$ | l8 | number script |
| Slip 0.2: r2c4 chooses L (0.2255); step cost 0: r3c5 chooses D | l8 | number script |
| Review, homework and problem figures (0.4502, 5.88, 135, 11.87, 4.1667, −2, 2.6500 bound against error 0.0420 after 10 sweeps, 109, 22.39, 22.63, 23.38, 0.7323, 0.5094, 0.1128) | sets | number script |

## Deviations from the brief (read these)

- The brief says the finite dice values 3.5, 4.25, 4.6667, 4.9444, 5.1296 "rise towards" 4.5833 "so the discount is what keeps the answer finite". They rise past it towards 6 (5.2747 with six rolls): with no discount the unlimited game is worth 6 and is finite. l5 therefore does not make that claim; it teaches the discount as patience, and the infinite case with £1 a step for ever.
- The brief's "plane of the largest change per sweep: a straight line of slope $\log_{10} 0.9$" holds for the deterministic grid only (exactly $0.96 \times 0.9^{k-1}$, then 0 after sweep 8). On the slippery grid the changes fall faster, about 0.47 a sweep near the end. l7 shows both, with the bound as the dashed line.
- `same_policy(p1, p2, values, slip, gamma)` takes the model's slip and discount as well, since the optimal sets depend on them.
- Policy iteration keeps the current action on a tie (within $10^{-9}$); otherwise it can swap tied actions for ever on the deterministic grid. With that rule it takes 5 evaluations there; the brief's 4 is for the slippery grid, which l8 uses.
- `solve_mdp` takes `P` and `R` both shaped `[A, S, S]` (reward per transition); end states absorb with reward 0. The hidden tests build the gridworld and the dice game (states: holding roll 1 to 6, and done) in a hidden prelude.

## course.json

No change proposed.
