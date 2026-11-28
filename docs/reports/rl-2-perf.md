# rl level 2: performance task

- `homework-2.json`, item `h-solve-mdp`, index 0. Kind `code` (Python with NumPy, difficulty 5).
- Matched objective: l7 "Code value iteration and bound its error by the discount factor." (also l8 "Build policy iteration ...").
- Task: from a stub, `solve_mdp(P, R, gamma)` solves any finite MDP given as arrays `[A, S, S]` by value iteration and returns the optimal values and, per state, the set of best actions.
- 9 hidden tests, 1 example: a planted three-state MDP at two discounts (values and action sets), the slippery and deterministic gridworld (values, the L at r3c5, the U/R tie at the start), and the dice game written as an MDP (first-roll values average 55/12; reroll 1 to 4, keep 5 and 6). The grid and dice arrays come from a hidden prelude.
- Overlapping screens: l7 screen 8 codes value iteration for the grid with its own helpers; the task asks for a model-free-of-grid solver on arrays, with ties, which no screen does.

Gates:
1. `node tools/validate.mjs`: 0 errors.
2. `VOICE_BASE=app/content/courses/rl python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script `docs/reports/rl-L2-numbers.py` (venv): exit 0; it runs the solution against every test.
4. Playthrough `--set rl/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the starter fails.
