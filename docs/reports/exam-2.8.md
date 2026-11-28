# Topic 2.8 exam: Reinforcement learning

File: `app/content/exams/topic-2.8.json` (90 minutes, pass 0.7, 30 items). Scripts: `docs/briefs/exam-2.8-scripts/` (`build.py` route A, `check_numbers.py` route B, strict coverage).

## Result

- Ramp 6, 15, 6, 3 at difficulties 2 to 5. Pace 5,145 s (86 min); each code item takes 10 minutes.
- Skills: rl-bandit 6, rl-mdp 7 (exit shared), rl-td 6, rl-pg 6, rl-search 6.
- Kinds: 18 numeric, 3 choice, 7 parts, 2 Python code with 5 mutants each.
- Exit: `q_learn` on a new 3 by 5 grid; its greedy policy must lie in value iteration's optimal sets (one tie at r3c1). It has exact seeded sums, one at `q0 = 0.5` for the terminal mask, and a test that a tie taken the other way still passes.
- Second code item: REINFORCE with one baseline per state, with exact short seeded runs. No shared module is shipped.

## Gates

- Validator 0 errors; topic-2.8 warnings are only 24 advisory long sentences.
- Voice scan 35: 0 and 0.
- `check_numbers.py`, strict, venv: 646 of 646, exit 0.
- `grade-all --code`: 0 failures. Slowest graded case 189 ms in Pyodide.
- Playthrough green with and without `--mobile`.
- `fresh-check`: 0 hits.
